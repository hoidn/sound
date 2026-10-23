"""Preparation-only stdlib checks. No collector import/main, decode or window extraction."""
from pathlib import Path
import ast, copy, hashlib, json, struct, sys
HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'depth-corpus-x86-setup-entry-instructions'

def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

def source_guard(text):
    tree = ast.parse(text)
    settings = [n for n in tree.body if isinstance(n, ast.Assign) and
                any(isinstance(t, ast.Tuple) and ast.unparse(t) == '(START, LENGTH)' for t in n.targets)]
    assert len(settings) == 1 and ast.literal_eval(settings[0].value) == (0x3ab0, 96)
    launches = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and
                isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and
                n.func.value.id == 'subprocess']
    assert len(launches) == 1 and launches[0].func.attr == 'Popen'
    for literal in ["'-NN', '-n', '-x', '-f', '-a', 'x86', '-b', '64'",
                    "'-E', 'little', '-m', hex(START), '-s', hex(START), '-q'",
                    "'pDj 96'", 'child.communicate(timeout=30)', 'if OUT.exists():',
                    'stream.seek(slice_file_offset)', 'raw = stream.read(LENGTH)',
                    "coverage = validate_span(rows, raw)", "save('span-coverage.json', coverage)",
                    "save('before-map.json'", "save('after-map.json'", "save('status.json', status)",
                    "save('returned-pid.json'", 'except BaseException as error:',
                    "assert len(piece) == row['size']", 'assert cursor - START <= LENGTH',
                    "assert row['bytes'] == piece.hex()", 'assert cursor == START + LENGTH',
                    "assert b''.join(pieces) == raw", 'assert isinstance(rows, list) and 1 <= len(rows) <= LENGTH']:
        assert literal in text, literal
    assert text.index('if OUT.exists():') < text.index('OUT.mkdir()')
    assert text.index("save('before-map.json'") < text.index('stream.seek(slice_file_offset)')
    assert text.index("save('attempt.json'") < text.index("status['attempted_decoder_children'] = 1") < text.index('child = subprocess.Popen')
    assert text.index("status['returned_pid_children'] = 1") > text.index('child = subprocess.Popen')
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and
                   n.func.id in ('exec', 'eval', '__import__') for n in ast.walk(tree))
    image = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'IMAGE' for t in n.targets)]
    assert len(image) == 1 and ast.unparse(image[0].value) == "HERE.parent / 'depth-corpus-x86-selected-entry-actual-r5/input/Corpus.x86_64'"
    assert 'values[4] == 14 and values[5] == 1696' in text
    assert "metadata['slice_file_offset'] == 0x3ab0" in text
    return tree

def selected_span_function(tree):
    selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'validate_span']
    assert len(selected) == 1
    # Only this fully inspected pure analyst definition is compiled, never collector main/imports.
    namespace = {'START': 0x3ab0, 'LENGTH': 96}
    exec(compile(ast.Module(body=selected, type_ignores=[]), '<selected-pure-span-validator>', 'exec'), namespace)
    return namespace['validate_span']

def rejects(function, rows, raw):
    try:
        function(rows, raw)
    except (AssertionError, ValueError, KeyError, TypeError):
        return True
    return False

def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no collector/decoder/window extraction.')
    assert not OUT.exists(), 'Exclusive future destination must remain absent.'
    inputs = json.loads((HERE / 'inputs.json').read_text())
    delta = json.loads((HERE / 'delta.json').read_text())
    pinned = inputs['pins'] + delta['preserved_parent_files']
    watched = {Path(r['path']) for r in pinned} | {p for p in HERE.iterdir() if p.is_file()}
    before = [identity(p) for p in sorted(watched)]
    for row in pinned:
        assert identity(Path(row['path'])) == {k: row[k] for k in ('path', 'bytes', 'sha256')}
    text = (HERE / 'collect-once.py').read_text()
    assert identity(HERE / 'collect-once.py') == delta['collector_after']
    def reconstruct(current, operations):
        lines = current.splitlines(keepends=True)
        for op in reversed(operations):
            assert lines[op['new_start']:op['new_end']] == op['new_lines']
            lines[op['new_start']:op['new_end']] = op['old_lines']
        return ''.join(lines)
    assert reconstruct(text, delta['collector_line_operations']).encode() == Path(delta['collector_before']['path']).read_bytes()
    assert reconstruct((HERE / 'check.py').read_text(), delta['checker_line_operations']).encode() == Path(delta['checker_before']['path']).read_bytes()
    def validator_source(source):
        fn = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'validate_span')
        return ast.get_source_segment(source, fn)
    assert validator_source(text) == validator_source(Path(delta['collector_before']['path']).read_text())
    tree = source_guard(text)
    validate = selected_span_function(tree)
    raw = bytes(i % 256 for i in range(96))
    def rows_for(sizes):
        rows, used = [], 0
        for size in sizes:
            rows.append(dict(offset=0x3ab0 + used, size=size, type='synthetic',
                             opcode='synthetic valid row', bytes=raw[used:used + size].hex()))
            used += size
        return rows
    varied, remaining, size = [], 96, 1
    while remaining:
        take = min(size, remaining); varied.append(take); remaining -= take
        size = size % 15 + 1
    for sizes in ([1] * 96, [15] * 6 + [6], varied):
        result = validate(rows_for(sizes), raw)
        assert result['rows'] == len(sizes) and result['consumed_bytes'] == 96
        assert result['uninterpreted_selected_bytes'] == 0
        assert result['decoded_prefix_half_open'] == ['0x3ab0', '0x3b10']
        assert result['body_extent_claim'] is False
    good = rows_for([2] * 48)
    bad = []
    for field, value in [('size', 0), ('size', 16), ('size', True), ('size', '2'),
                         ('offset', 0x3ab0), ('offset', True), ('bytes', '00'),
                         ('bytes', 'zzzz'), ('bytes', 'ffff'), ('bytes', '0E0F'),
                         ('type', 'ill'), ('type', 'invalid'), ('type', None),
                         ('opcode', None), ('opcode', ''), ('opcode', 'invalid'),
                         ('opcode', 'ill'), ('opcode', 'None'), ('opcode', ' INVALID ')]:
        changed = copy.deepcopy(good); changed[7][field] = value; bad.append(changed)
    for field in ('bytes', 'type', 'opcode', 'offset', 'size'):
        changed = copy.deepcopy(good); del changed[7][field]; bad.append(changed)
    bad.extend([[], None, good[:-1], good + [copy.deepcopy(good[-1])], rows_for([1] * 97)])
    changed = copy.deepcopy(good)
    changed[0]['bytes'] = raw[:1].hex(); changed[1]['bytes'] = raw[1:4].hex(); bad.append(changed)
    changed = copy.deepcopy(good); changed[0]['bytes'] = '00 01'; bad.append(changed)
    changed = copy.deepcopy(good); changed[-1]['size'] = 1; changed[-1]['bytes'] = raw[-2:-1].hex(); bad.append(changed)
    changed = copy.deepcopy(good); changed[-1]['size'] = 3; changed[-1]['bytes'] = (raw[-2:] + b'\x00').hex(); bad.append(changed)
    assert all(rejects(validate, rows, raw) for rows in bad)
    assert rejects(validate, good, raw[:-1])
    assert rejects(validate, good, raw + b'\x00')
    assert rejects(validate, good, b'\xff' + raw[1:])
    mutations = [('0x3ab0, 96', '0x3ab1, 96'), ('0x3ab0, 96', '0x3ab0, 97'),
                 ("'pDj 96'", "'pdj 96'"), ("'-NN'", "'-N'"), ("'-x'", "'-w'"),
                 ("'-x', '-f'", "'-x'"), ("'x86'", "'arm'"),
                 ('child.communicate(timeout=30)', 'child.communicate(timeout=31)'),
                 ('if OUT.exists():', 'if False:'),
                 ("assert len(piece) == row['size']", 'assert True'),
                 ('assert cursor == START + LENGTH', 'assert True'),
                 ("assert b''.join(pieces) == raw", 'assert True'),
                 ("assert row['bytes'] == piece.hex()", 'assert True'),
                 ('assert isinstance(rows, list) and 1 <= len(rows) <= LENGTH', 'assert isinstance(rows, list)'),
                 ('values[4] == 14 and values[5] == 1696', 'values[4] == 54 and values[5] == 6832'),
                 ("metadata['slice_file_offset'] == 0x3ab0", "metadata['slice_file_offset'] == 0x3ab1")]
    for a, b in mutations:
        changed = text.replace(a, b, 1); assert changed != text
        try: source_guard(changed)
        except AssertionError: pass
        else: raise AssertionError('Unsafe source mutation accepted: ' + a)
    m = json.loads((HERE / 'header-map.json').read_text())
    assert identity(Path(m['image']['path'])) == m['image']
    # Header/LC metadata only; no selected instruction-window seek/read.
    with Path(m['image']['path']).open('rb') as stream:
        header = stream.read(32); assert header.hex() == m['header_hex']
        values = struct.unpack('<IiiIIIII', header)
        assert values[0:3] == (0xfeedfacf, 0x1000007, 3) and values[4:6] == (14, 1696)
        commands = stream.read(values[5]); assert commands.hex() == m['load_commands_hex']
    assert hashlib.sha256(commands).hexdigest() == m['load_commands_sha256']
    segments, cursor = [], 0
    for _ in range(values[4]):
        command, size = struct.unpack_from('<II', commands, cursor)
        assert size >= 8 and cursor + size <= len(commands)
        if command == 0x19:
            n, va, vs, fo, fs, mp, ip, ns, fl = struct.unpack_from('<16sQQQQiiII', commands, cursor + 8)
            segments.append(dict(name=n.rstrip(b'\0').decode(), vmaddr=va, vmsize=vs,
                                 fileoff=fo, filesize=fs, maxprot=mp, initprot=ip, nsects=ns, flags=fl))
        cursor += size
    assert cursor == len(commands) and segments == m['segments']
    matched = [s for s in segments if s['vmaddr'] <= 0x3ab0 and 0x3b10 <= s['vmaddr'] + s['filesize']]
    assert matched == [m['selected_segment']] and matched[0]['name'] == '__TEXT' and matched[0]['initprot'] & 4
    assert matched[0]['vmaddr'] == 0 and matched[0]['fileoff'] == 0
    assert matched[0]['fileoff'] + 0x3ab0 - matched[0]['vmaddr'] == m['slice_file_offset'] == 0x3ab0
    assert m['instruction_window_extracted'] is False
    assert (m['start'], m['end_exclusive'], m['length']) == ('0x3ab0', '0x3b10', 96)
    proposal = json.loads((HERE / 'proposal.json').read_text())
    assert proposal['selected_range'] == ['0x3ab0', '0x3b10'] and proposal['selected_bytes'] == 96
    argv = proposal['future_invocation']['tool_argv']
    assert argv == [str(next(Path(r['path']) for r in inputs['pins'] if r['role'] == 'rizin')),
                    '-NN', '-n', '-x', '-f', '-a', 'x86', '-b', '64', '-E', 'little',
                    '-m', '0x3ab0', '-s', '0x3ab0', '-q', '-c', 'pDj 96', str(OUT / 'setup-entry-96.bin')]
    seal = HERE / 'manifest.json'
    if seal.exists():
        inventory = json.loads(seal.read_text())['files']
        assert {r['path'] for r in inventory} == {p.name for p in HERE.iterdir() if p.is_file() and p != seal}
        for row in inventory:
            got = identity(HERE / row['path']); assert (got['bytes'], got['sha256']) == (row['bytes'], row['sha256'])
    for p in HERE.iterdir():
        if p.is_file():
            content = p.read_text(); assert content.endswith('\n') and all(s == s.rstrip() for s in content.splitlines())
    assert before == [identity(p) for p in sorted(watched)]
    print(json.dumps(dict(status='PASS preparation only', valid_synthetic_prefixes=3,
                         rejected_row_or_raw_controls=len(bad)+3, rejected_source_controls=len(mutations),
                         parent_files_exact=len(delta['preserved_parent_files']), watched=len(watched),
                         unchanged=True, instruction_window_extracted=False, decoder_children=0,
                         original_instruction_execution=False), indent=2))

if __name__ == '__main__':
    main()
