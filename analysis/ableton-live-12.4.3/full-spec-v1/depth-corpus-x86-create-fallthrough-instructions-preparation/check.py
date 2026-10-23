"""Preparation-only stdlib checks. No collector import/main, decode or window extraction."""
from pathlib import Path
import ast, copy, hashlib, json, struct, sys
HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'depth-corpus-x86-create-fallthrough-instructions'

def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

def source_guard(text):
    tree = ast.parse(text)
    settings = [n for n in tree.body if isinstance(n, ast.Assign) and
                any(isinstance(t, ast.Tuple) and ast.unparse(t) == '(START, LENGTH)' for t in n.targets)]
    assert len(settings) == 1 and ast.literal_eval(settings[0].value) == (0x23e6, 240)
    launches = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and
                isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and
                n.func.value.id == 'subprocess']
    assert len(launches) == 1 and launches[0].func.attr == 'Popen'
    for literal in ["'-NN', '-n', '-x', '-f', '-a', 'x86', '-b', '64'",
                    "'-E', 'little', '-m', hex(START), '-s', hex(START), '-q'",
                    "'pdj 16'", 'child.communicate(timeout=30)', 'if OUT.exists():',
                    'stream.seek(bundle_file_offset)', 'raw = stream.read(LENGTH)',
                    "coverage = validate_prefix(rows, raw)", "save('prefix-coverage.json', coverage)",
                    "save('before-map.json'", "save('after-map.json'", "save('status.json', status)",
                    "save('returned-pid.json'", 'except BaseException as error:',
                    "assert len(piece) == row['size']", 'assert cursor - START <= LENGTH']:
        assert literal in text, literal
    assert text.index('if OUT.exists():') < text.index('OUT.mkdir()')
    assert text.index("save('before-map.json'") < text.index('stream.seek(bundle_file_offset)')
    assert text.index("save('attempt.json'") < text.index("status['attempted_decoder_children'] = 1") < text.index('child = subprocess.Popen')
    assert text.index("status['returned_pid_children'] = 1") > text.index('child = subprocess.Popen')
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and
                   n.func.id in ('exec', 'eval', '__import__') for n in ast.walk(tree))
    return tree

def selected_prefix_function(tree):
    selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'validate_prefix']
    assert len(selected) == 1
    # Only this fully inspected pure analyst definition is compiled, never collector main/imports.
    namespace = {'START': 0x23e6, 'LENGTH': 240}
    exec(compile(ast.Module(body=selected, type_ignores=[]), '<selected-pure-prefix-validator>', 'exec'), namespace)
    return namespace['validate_prefix']

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
    context = inputs['asof_context']
    snapshot = identity(HERE / context['retained_provider'])
    assert (snapshot['bytes'], snapshot['sha256']) == (context['source_identity']['bytes'], context['source_identity']['sha256'])
    pinned = inputs['pins'] + delta['preserved_parent_files']
    watched = {Path(r['path']) for r in pinned} | {p for p in HERE.iterdir() if p.is_file()}
    before = [identity(p) for p in sorted(watched)]
    for row in pinned:
        assert identity(Path(row['path'])) == {k: row[k] for k in ('path', 'bytes', 'sha256')}
    text = (HERE / 'collect-once.py').read_text()
    assert identity(HERE / 'collect-once.py') == delta['collector_after']
    restored = text
    for op in reversed(delta['collector_literal_operations']):
        assert restored.count(op['after']) == op['occurrences']
        restored = restored.replace(op['after'], op['before'])
    assert restored.encode() == Path(delta['collector_before']['path']).read_bytes()
    tree = source_guard(text)
    validate = selected_prefix_function(tree)
    raw = bytes(range(240))
    def rows_for(sizes):
        rows, used = [], 0
        for size in sizes:
            rows.append(dict(offset=0x23e6 + used, size=size, type='synthetic',
                             opcode='synthetic valid row', bytes=raw[used:used + size].hex()))
            used += size
        return rows
    for sizes in ([1] * 16, [15] * 16, list(range(1, 16)) + [1]):
        result = validate(rows_for(sizes), raw)
        assert result['consumed_bytes'] == sum(sizes)
        assert result['uninterpreted_selected_bytes'] == 240 - sum(sizes)
        assert result['body_extent_claim'] is False
    good = rows_for([2] * 16)
    bad = []
    for field, value in [('size', 0), ('size', 16), ('size', True), ('size', '2'),
                         ('offset', 0x23e6), ('offset', True), ('bytes', '00'),
                         ('bytes', 'zzzz'), ('bytes', 'ffff'), ('type', 'ill'),
                         ('type', 'invalid'), ('type', None), ('opcode', None),
                         ('opcode', ''), ('opcode', 'invalid'), ('opcode', 'ill'),
                         ('opcode', 'None'), ('opcode', ' INVALID ')]:
        changed = copy.deepcopy(good); changed[7][field] = value; bad.append(changed)
    for field in ('bytes', 'type', 'opcode', 'offset', 'size'):
        changed = copy.deepcopy(good); del changed[7][field]; bad.append(changed)
    bad.extend([good[:15], good + [copy.deepcopy(good[-1])]])
    # Concatenation still matches raw prefix, but the two declared boundaries are false.
    changed = copy.deepcopy(good)
    changed[0]['bytes'] = raw[:1].hex(); changed[1]['bytes'] = raw[1:4].hex(); bad.append(changed)
    # Sixteen maximum-sized rows already fill all240B; any declared overrun must fail.
    changed = rows_for([15] * 16); changed[-1]['size'] = 16; bad.append(changed)
    assert all(rejects(validate, rows, raw) for rows in bad)
    assert rejects(validate, good, raw[:-1])
    assert rejects(validate, good, b'\xff' + raw[1:])
    mutations = [('0x23e6, 240', '0x23e7, 240'), ('0x23e6, 240', '0x23e6, 241'),
                 ("'pdj 16'", "'pdj 17'"), ("'-NN'", "'-N'"), ("'-x'", "'-w'"),
                 ("'-x', '-f'", "'-x'"), ("'x86'", "'arm'"),
                 ('child.communicate(timeout=30)', 'child.communicate(timeout=31)'),
                 ('if OUT.exists():', 'if False:'),
                 ("assert len(piece) == row['size']", 'assert True')]
    for a, b in mutations:
        changed = text.replace(a, b, 1); assert changed != text
        try: source_guard(changed)
        except AssertionError: pass
        else: raise AssertionError('Unsafe source mutation accepted: ' + a)
    m = json.loads((HERE / 'header-map.json').read_text())
    assert identity(Path(m['bundle']['path'])) == m['bundle']
    # Header/LC reads only; no selected instruction-window seek/read.
    with Path(m['bundle']['path']).open('rb') as stream:
        fat = stream.read(8); assert fat.hex() == m['fat_header_hex']
        magic, count = struct.unpack('>II', fat); assert (magic, count) == (0xcafebabe, 2)
        arches = stream.read(20 * count); assert arches.hex() == m['fat_arch_table_hex']
        matches = [struct.unpack_from('>IIIII', arches, i * 20) for i in range(count)]
        matches = [a for a in matches if a[:2] == (0x1000007, 3)]
        assert len(matches) == 1 and matches[0][2:4] == (16384, 250352)
        stream.seek(16384); header = stream.read(32); assert header.hex() == m['header_hex']
        values = struct.unpack('<IiiIIIII', header); assert values[4:6] == (14, 1696)
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
    matched = [s for s in segments if s['vmaddr'] <= 0x23e6 and 0x24d6 <= s['vmaddr'] + s['filesize']]
    assert matched == [m['selected_segment']] and matched[0]['name'] == '__TEXT' and matched[0]['initprot'] & 4
    assert matched[0]['fileoff'] + 0x23e6 - matched[0]['vmaddr'] == m['slice_file_offset'] == 9190
    assert 16384 + m['slice_file_offset'] == m['bundle_file_offset'] == 25574
    assert m['instruction_window_extracted'] is False
    proposal = json.loads((HERE / 'proposal.json').read_text())
    assert proposal['selected_range'] == ['0x23e6', '0x24d6'] and proposal['selected_bytes'] == 240
    argv = proposal['future_invocation']['tool_argv']
    assert argv == [str(next(Path(r['path']) for r in inputs['pins'] if r['role'] == 'rizin')),
                    '-NN', '-n', '-x', '-f', '-a', 'x86', '-b', '64', '-E', 'little',
                    '-m', '0x23e6', '-s', '0x23e6', '-q', '-c', 'pdj 16', str(OUT / 'create-fallthrough-240.bin')]
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
                         rejected_row_or_raw_controls=len(bad)+2, rejected_source_controls=len(mutations),
                         parent_files_exact=len(delta['preserved_parent_files']), watched=len(watched),
                         unchanged=True, instruction_window_extracted=False, decoder_children=0,
                         original_instruction_execution=False), indent=2))

if __name__ == '__main__':
    main()
