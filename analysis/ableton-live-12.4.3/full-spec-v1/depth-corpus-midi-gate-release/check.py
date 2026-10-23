"""Read-only preflight data/AST checks. Never imports or runs the collector/diagnostic."""
from pathlib import Path
import ast, copy, hashlib, json, math, struct, sys
PRE = Path(__file__).resolve().parent
NAMES = ['gate1-held', 'gate1-off', 'gate0-off']

def ident(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def validate(texts, base):
    assert set(texts) == set(NAMES)
    for name in NAMES:
        expected = base.replace('param 13 0.0\n', 'param 13 1.0\n') if name != 'gate0-off' else base
        if name != 'gate1-held':
            expected = expected.replace('event 1537 0x90 60 100\n', 'event 1537 0x90 60 100\nevent 8193 0x80 60 64\n')
        assert texts[name] == expected
        lines = texts[name].splitlines()
        params = [s.split() for s in lines if s.startswith('param ')]
        assert [int(s[1]) for s in params] == list(range(38))
        assert sum(s.startswith('process ') for s in lines) == 1
        assert sum(s.startswith('event ') for s in lines) == (1 if name == 'gate1-held' else 2)
        assert sum(s.startswith(('create', 'rate ', 'param ', 'destroy')) for s in lines) + 32 == 73
    assert len(NAMES) * 73 == 219 < 256

def finite_bytes(b):
    assert len(b) == 131072
    assert all(math.isfinite(v) for f in struct.iter_unpack('<ff', b) for v in f)

def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; collector, native and descriptive calculations are not invoked.')
    proposal = json.loads((PRE / 'proposal.json').read_text())
    pins = proposal['source_pins']
    original_seal = Path(pins['original_preparation_manifest']['path'])
    original = original_seal.parent
    old_manifest = json.loads(original_seal.read_text())
    original_files = {original_seal} | {original/r['path'] for r in old_manifest['files']}
    watched = sorted({p for p in PRE.rglob('*') if p.is_file()} | {Path(r['path']) for r in pins.values()} | original_files)
    before = {str(p): ident(p) for p in watched}
    seal = PRE / 'manifest-preflight.json'
    if seal.exists():
        m = json.loads(seal.read_text())
        assert {r['path'] for r in m['files']} == {p.name for p in PRE.iterdir() if p.is_file() and p.name != seal.name}
        for r in m['files']:
            assert {k: ident(PRE/r['path'])[k] for k in ('bytes', 'sha256')} == {k: r[k] for k in ('bytes', 'sha256')}
    for r in pins.values(): assert ident(Path(r['path'])) == r
    for r in old_manifest['files']:
        assert {k: ident(original/r['path'])[k] for k in ('bytes','sha256')} == {k:r[k] for k in ('bytes','sha256')}
    for name in ['gate1-held.script','gate1-off.script','gate0-off.script','describe.py','source-contexts.json']:
        assert (PRE/name).read_bytes() == (original/name).read_bytes()
    old_proposal = json.loads((original/'proposal.json').read_text())
    assert {k:pins[k] for k in old_proposal['source_pins']} == old_proposal['source_pins']
    for key in ['final_directory','run_order','events','scripts','fixed_protocol','child_environment_complete','timeout_seconds_per_child','core_limit','output_validity','expected_artifacts']:
        assert proposal[key] == old_proposal[key]
    response = json.loads((PRE/'response-r2.json').read_text())
    rebuilt = (original/'capture-once.py').read_text()
    for op in response['collector_literal_changes']:
        assert rebuilt.count(op['before_literal']) == 1
        rebuilt = rebuilt.replace(op['before_literal'], op['after_literal'])
    assert rebuilt == (PRE/'capture-once.py').read_text()
    b = Path(pins['bundle']['path']).read_bytes()
    section = proposal['x86_slice']
    x86 = b[section['offset']:section['offset']+section['bytes']]
    assert hashlib.sha256(x86).hexdigest() == section['sha256']
    assert x86[:4] == b'\xcf\xfa\xed\xfe' and struct.unpack_from('<I', x86, 4)[0] == 0x01000007
    texts = {n: (PRE/(n+'.script')).read_text() for n in NAMES}
    base = Path(pins['historical_script']['path']).read_text()
    validate(texts, base)
    assert not Path(proposal['final_directory']).exists(), 'No capture is selected/executed by this preflight check.'
    rejected = []
    for name, run, old, new in [
        ('wrong gate', 'gate1-off', 'param 13 1.0', 'param 13 0.0'),
        ('wrong off status', 'gate1-off', 'event 8193 0x80', 'event 8193 0x90'),
        ('wrong off velocity', 'gate0-off', '0x80 60 64', '0x80 60 0'),
        ('extra minus1', 'gate1-off', 'event 8193 ', 'event 8192 '),
        ('missing parameter', 'gate1-held', 'param 37 0.0\n', ''),
        ('extra process', 'gate0-off', 'destroy\n', 'process 16384 512\ndestroy\n'),
        ('reset insertion', 'gate1-held', 'create\n', 'create\nreset\n'),
        ('reversed queue order', 'gate1-off', 'event 1537 0x90 60 100\nevent 8193 0x80 60 64', 'event 8193 0x80 60 64\nevent 1537 0x90 60 100'),
    ]:
        changed = copy.deepcopy(texts)
        assert old in changed[run]
        changed[run] = changed[run].replace(old, new)
        try: validate(changed, base)
        except AssertionError: rejected.append(name)
        else: raise AssertionError('bad script accepted: '+name)
    inp = Path(pins['input']['path']).read_bytes()
    finite_bytes(inp)
    assert [(i, *v) for i, v in enumerate(struct.iter_unpack('<ff', inp)) if any(v)] == [(4096, 1., 1.)]
    finite_bytes(bytes(131072))  # Silent finite output is a valid observation, not a rejected capture.
    for name, bad in [('short', bytes(131064)), ('extra', bytes(131080)),
                      ('NaN prefix', struct.pack('<f', math.nan)+bytes(131068)),
                      ('Inf tail', bytes(131068)+struct.pack('<f', math.inf))]:
        try: finite_bytes(bad)
        except AssertionError: rejected.append(name)
        else: raise AssertionError(name)
    contexts = json.loads((PRE/'source-contexts.json').read_text())
    lines = Path(pins['driver_c']['path']).read_text().splitlines(True)
    for span in contexts['spans']:
        assert span['text'] == ''.join(lines[span['start_line']-1:span['end_line']])
    for frame, status, velocity, block in [(1537, 144, 100, 1536), (8193, 128, 64, 8192)]:
        record = struct.pack('<qBBBB4s', frame, status, 60, velocity, 0, b'\0'*4)
        assert len(record) == 16 and record[8:12] == bytes([status, 60, velocity, 0])
        selected = [done for done in range(0, 16384, 512) if done <= frame < done+512]
        assert selected == [block] and frame-block == 1
    collector = ast.parse((PRE/'capture-once.py').read_text())
    assert len([n for n in ast.walk(collector) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'Popen']) == 1
    validity = next(n.value for n in ast.walk(collector) if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Constant) and t.slice.value == 'valid_capture' for t in n.targets))
    assert 'productive' not in ast.unparse(validity) and 'numeric_valid' in ast.unparse(validity)
    old_ast = ast.parse((original/'capture-once.py').read_text())
    old_validity = next(n.value for n in ast.walk(old_ast) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Constant) and t.slice.value == 'valid_capture' for t in n.targets))
    assert ast.dump(validity) == ast.dump(old_validity)
    collector_text = (PRE/'capture-once.py').read_text()
    assert 'actual_original_x86_capture' not in collector_text and 'native_children' not in collector_text
    assert "row['launch_attempted'] = True\n                child = subprocess.Popen" in collector_text
    assert "row['pid'] = child.pid\n                row['popen_returned_pid'] = True" in collector_text
    result_ast = next(n.value for n in ast.walk(collector) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'result' for t in n.targets))
    expressions = {k.value:v for k,v in zip(result_ast.keys,result_ast.values) if isinstance(k,ast.Constant)}
    fields = {'attempted_launches':'launch_attempted','returned_pid_children':'popen_returned_pid','structurally_valid_captures':'valid_capture'}
    for key, field in fields.items():
        expected_ast = ast.parse("sum(r['"+field+"'] for r in runs)",mode='eval').body
        assert ast.dump(expressions[key]) == ast.dump(expected_ast)
    # These fixtures invoke this checker-only pure arithmetic, never the collector.
    def accounting(runs):
        return {'attempted_launches':sum(r['launch_attempted'] for r in runs),
                'returned_pid_children':sum(r['popen_returned_pid'] for r in runs),
                'structurally_valid_captures':sum(r['valid_capture'] for r in runs)}
    accounting_fixtures = []
    for name, pid_returned, valid, expected_counts in [
        ('failed Popen',False,False,[1,0,0]),('early loader failure',True,False,[1,1,0]),
        ('timeout partial unknown',True,False,[1,1,0]),('success',True,True,[1,1,1])]:
        row = {'launch_attempted':True,'popen_returned_pid':pid_returned,'valid_capture':valid}
        counts = accounting([row])
        assert list(counts.values()) == expected_counts
        accounting_fixtures.append({'name':name,'counts':counts,'does_not_infer_original_exports_from_pid':True})
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) and 'capture' in ast.unparse(n) for n in ast.walk(ast.parse(Path(__file__).read_text())))
    for f in PRE.iterdir():
        if f.is_file() and f.suffix in ['.md', '.json', '.py', '.script']:
            t = f.read_text()
            assert t.endswith('\n') and all(not line.endswith((' ', '\t')) for line in t.splitlines()), f
    assert before == {str(p): ident(p) for p in watched}
    print(json.dumps({'status': 'Prepared-data checks pass; no capture authorization or result.', 'sealed': seal.exists(),
          'scripts': 3, 'requested_children': 3, 'requested_direct_exports_max': 219,
          'zero_output_structurally_admitted': True, 'negative_fixtures': rejected,
          'r1_files_exact': len(original_files), 'accounting_fixtures': accounting_fixtures,
          'event_source_offsets': ['1537=>1536+1', '8193=>8192+1'], 'watched': len(watched),
          'unchanged': True, 'original_calls': 0, 'collector_invocations': 0,
          'descriptive_calculations': 0, 'grade': None}, indent=2))

if __name__ == '__main__': main()
