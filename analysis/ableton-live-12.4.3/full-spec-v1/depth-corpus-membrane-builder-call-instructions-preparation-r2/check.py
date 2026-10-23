"""Read-only preparation/AST checks; never import the collector or run rizin."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import struct
import sys

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'depth-corpus-membrane-builder-call-instructions-r2'


def identity(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def source_guard(text):
    tree = ast.parse(text)
    assignments = [n for n in ast.walk(tree) if isinstance(n, ast.Assign) and
                   any(isinstance(t, ast.Tuple) and [v.id for v in t.elts] == ['START', 'LENGTH']
                       for t in n.targets)]
    assert len(assignments) == 1 and ast.literal_eval(assignments[0].value) == (0x24884, 12)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    launches = [n for n in calls if isinstance(n.func, ast.Attribute) and
                isinstance(n.func.value, ast.Name) and n.func.value.id == 'subprocess']
    assert len(launches) == 1 and launches[0].func.attr == 'Popen'
    assert not any(isinstance(n.func, ast.Name) and n.func.id in ('exec', 'eval', '__import__') for n in calls)
    assert "[str(TOOL), '-NN', '-n', '-x', '-f', '-a', 'arm', '-b', '64'," in text
    assert "'-E', 'little', '-m', hex(START), '-s', hex(START), '-q'," in text
    assert "'-c', 'pdj 3', str(OUT / 'call-12.bin')]" in text
    assert "child.communicate(timeout=30)" in text
    assert "stream.seek(metadata['file_offset'])" in text and "raw = stream.read(LENGTH)" in text
    assert "if OUT.exists():" in text and text.index('if OUT.exists():') < text.index('OUT.mkdir()')
    assert "save('before-map.json'" in text and text.index("save('before-map.json'") < text.index("stream.seek(")
    assert text.index("save('attempt.json'") < text.index("status['attempted_decoder_children'] = 1") < text.index('child = subprocess.Popen')
    assert "save('returned-pid.json'" in text and "except BaseException as error:" in text
    assert "save('after-map.json'" in text and "save('status.json', status)" in text
    assert "row.get('type') not in ('invalid', 'ill')" in text
    assert "row['opcode'].strip().lower() not in ('', 'invalid', 'ill', 'none')" in text


def row_metadata_accepts(text, rows):
    tree = ast.parse(text)
    tests = [n.test for n in ast.walk(tree) if isinstance(n, ast.Assert) and
             ((isinstance(n.test, ast.Call) and isinstance(n.test.func, ast.Name) and
               n.test.func.id == 'all' and 'row[' in ast.unparse(n.test)) or
              ast.unparse(n.test) == 'len(rows) == 3')]
    assert len(tests) == 2
    namespace = {'__builtins__': {}, 'rows': rows, 'START': 0x24884,
                 'all': all, 'len': len, 'enumerate': enumerate,
                 'isinstance': isinstance, 'str': str}
    return all(eval(compile(ast.Expression(test), '<synthetic-row-predicate-only>', 'eval'),
                    namespace) for test in tests)


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no collector/decoder/extraction.')
    assert not OUT.exists(), 'Execution destination exists; this preparation check is as-of preexecution only.'
    pins = json.loads((HERE / 'inputs.json').read_text())['pins']
    watched = {Path(row['path']) for row in pins} | {p for p in HERE.iterdir() if p.is_file()}
    correction = json.loads((HERE / 'correction.json').read_text())
    watched.update(Path(row['path']) for row in correction['preserved_R1_files'])
    before = [identity(p) for p in sorted(watched)]
    for row in pins:
        assert identity(Path(row['path'])) == {k: row[k] for k in ('path', 'bytes', 'sha256')}
    mapping = json.loads((HERE / 'header-map.json').read_text())
    image = Path(mapping['image']['path'])
    assert identity(image) == mapping['image']
    with image.open('rb') as stream:
        header = stream.read(32)
        assert header.hex() == mapping['header_hex']
        values = struct.unpack('<IiiIIIII', header)
        assert values[0] == 0xfeedfacf and values[1] == 0x100000c
        commands = stream.read(values[5])
        assert commands.hex() == mapping['load_commands_hex']
        assert hashlib.sha256(commands).hexdigest() == mapping['load_commands_sha256']
    matches = [s for s in mapping['segments'] if s['vmaddr'] <= 0x24884 and
               0x24890 <= s['vmaddr'] + s['filesize']]
    assert matches == [mapping['selected_segment']] and matches[0]['name'] == '__TEXT'
    assert matches[0]['fileoff'] + 0x24884 - matches[0]['vmaddr'] == mapping['file_offset'] == 149636
    assert mapping['length'] == 12 and mapping['instruction_window_extracted'] is False
    text = (HERE / 'collect-once.py').read_text()
    source_guard(text)
    for row in correction['preserved_R1_files']:
        assert identity(Path(row['path'])) == row
    restored = text
    for op in reversed(correction['collector_literal_operations']):
        assert restored.count(op['after']) == 1
        restored = restored.replace(op['after'], op['before'], 1)
    old = Path(correction['collector_before']['path'])
    assert restored.encode() == old.read_bytes()
    assert (HERE / 'header-map.json').read_bytes() == (old.parent / 'header-map.json').read_bytes()
    assert pins[:13] == json.loads((old.parent / 'inputs.json').read_text())['pins']
    oldargv = json.loads((old.parent / 'proposal.json').read_text())['future_invocation']['tool_argv']
    newargv = json.loads((HERE / 'proposal.json').read_text())['future_invocation']['tool_argv']
    assert oldargv[:-1] == newargv[:-1]
    baseline = [{'offset': 0x24884 + 4 * i, 'size': 4, 'type': 'nop',
                 'opcode': 'nop', 'bytes': '00000000'} for i in range(3)]
    assert row_metadata_accepts(text, baseline)
    bad_rows = []
    for field, value in [('type', 'invalid'), ('type', 'ill'), ('opcode', None),
                         ('opcode', ''), ('opcode', 'invalid'), ('opcode', 'ill'),
                         ('opcode', 'None'), ('opcode', ' INVALID ')]:
        rows = copy.deepcopy(baseline)
        rows[1][field] = value
        bad_rows.append(rows)
    absent = copy.deepcopy(baseline)
    del absent[1]['opcode']
    bad_rows.append(absent)
    finding = copy.deepcopy(baseline)
    for row in finding:
        row.update(type='ill', opcode='invalid')
    assert row_metadata_accepts(restored, finding)
    bad_rows.append(finding)
    assert all(not row_metadata_accepts(text, rows) for rows in bad_rows)
    pattern = next(Path(row['path']) for row in pins if row['role'] == 'inspected_corrected_decoder_pattern')
    oldtree = ast.parse(pattern.read_text())
    oldlist = [n.test.comparators[0] for n in ast.walk(oldtree) if isinstance(n, ast.Assert) and
               isinstance(n.test, ast.Compare) and isinstance(n.test.left, ast.Name) and
               n.test.left.id == 'argv' and isinstance(n.test.comparators[0], ast.List)]
    assert len(oldlist) == 1
    oldargv = [ast.literal_eval(n) for n in oldlist[0].elts[1:-1]]
    newargv = json.loads((HERE / 'proposal.json').read_text())['future_invocation']['tool_argv'][1:-1]
    assert len(oldargv) == len(newargv) == 17
    assert [(i + 1, old, new) for i, (old, new) in enumerate(zip(oldargv, newargv)) if old != new] == [
        (12, '0x1026e8e50', '0x24884'),
        (14, '0x1026e8e50', '0x24884'),
        (17, 'pdj 72', 'pdj 3'),
    ]
    mutations = [
        text.replace('0x24884, 12', '0x24880, 12', 1),
        text.replace('0x24884, 12', '0x24884, 16', 1),
        text.replace("'pdj 3'", "'pdj 4'", 1),
        text.replace("'-NN'", "'-N'", 1),
        text.replace("'-x'", "'-w'", 1),
        text.replace("'-x', '-f'", "'-x'", 1),
        text.replace('child.communicate(timeout=30)', 'child.communicate(timeout=31)', 1),
        text.replace('if OUT.exists():', 'if False:', 1),
    ]
    for changed in mutations:
        assert changed != text
        try:
            source_guard(changed)
        except AssertionError:
            pass
        else:
            raise AssertionError('Unsafe preparation mutation accepted')
    manifest = HERE / 'manifest.json'
    if manifest.exists():
        inventory = json.loads(manifest.read_text())['files']
        assert {r['path'] for r in inventory} == {p.name for p in HERE.iterdir() if p.is_file() and p != manifest}
        for row in inventory:
            got = identity(HERE / row['path'])
            assert (got['bytes'], got['sha256']) == (row['bytes'], row['sha256'])
    for p in HERE.iterdir():
        if p.is_file():
            text = p.read_text()
            assert text.endswith('\n') and all(line == line.rstrip() for line in text.splitlines())
    assert before == [identity(p) for p in sorted(watched)]
    print(json.dumps({'status': 'PASS preparation only', 'fixtures_rejected': len(mutations),
                      'focused_invalid_row_fixtures_rejected': len(bad_rows),
                      'valid_synthetic_rows_retained': True,
                      'R1_finding_reproduced_AST_only': True,
                      'R1_eight_files_exact': True, 'collector_two_literal_ops_reversible': True,
                      'argv_flags_exact_inspected_corrected_pattern': True,
                      'range': ['0x24884', '0x24890'], 'future_rows': 3,
                      'watched': len(watched), 'unchanged': True,
                      'instruction_window_extracted': False, 'decoder_children': 0,
                      'original_execution': False}, indent=2))


if __name__ == '__main__':
    main()
