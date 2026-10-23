"""Read-only data/selected-AST preflight. Never imports or invokes the collector."""
from pathlib import Path
import ast, copy, hashlib, json, math, struct, sys
PRE = Path(__file__).resolve().parent
NAMES = ['gate1-held', 'gate1-off', 'gate0-off']

def ident(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def verify_pin(r):
    assert ident(Path(r['path'])) == r

def finite_bytes(b):
    assert len(b) == 131072
    assert all(math.isfinite(v) for f in struct.iter_unpack('<ff', b) for v in f)

def validate(texts, base):
    assert set(texts) == set(NAMES)
    for name in NAMES:
        expected = base.replace('param 13 0.0\n', 'param 13 1.0\n') if name != 'gate0-off' else base
        if name != 'gate1-held':
            expected = expected.replace('event 1537 0x90 60 100\n', 'event 1537 0x90 60 100\nevent 3073 0x80 60 64\n')
        assert texts[name] == expected
        lines = texts[name].splitlines()
        assert [int(s.split()[1]) for s in lines if s.startswith('param ')] == list(range(38))
        assert sum(s.startswith('process ') for s in lines) == 1
        assert sum(s.startswith('event ') for s in lines) == (1 if name == 'gate1-held' else 2)
        assert sum(s.startswith(('create', 'rate ', 'param ', 'destroy')) for s in lines) + 32 == 73
    assert 3 * 73 == 219 < 256

def assignment(tree, key):
    found = [n.value for n in ast.walk(tree) if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Constant)
                     and t.slice.value == key for t in n.targets)]
    assert len(found) == 1
    return found[0]

def pure_guard(expr, scope):
    # Only the already-inspected current parameter/validity expressions are compiled.
    # Collector imports, definitions, main, callbacks, Popen and numeric loop never run.
    for n in ast.walk(expr):
        if isinstance(n, ast.Call):
            assert (isinstance(n.func, ast.Name) and n.func.id in {'len', 'all', 'float', 'zip'}) or (
                isinstance(n.func, ast.Attribute) and n.func.attr in {'pack', 'startswith'})
    env = {'__builtins__': {}, 'len': len, 'all': all, 'float': float, 'zip': zip, 'struct': struct}
    env.update(scope)
    return eval(compile(ast.Expression(expr), '<selected-current-data-guard>', 'eval'), env)

def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no collector, native or diagnostic invocation.')
    proposal = json.loads((PRE/'proposal.json').read_text())
    pins = proposal['source_pins']
    parent = Path(pins['parent_r2_manifest']['path']).parent
    manifests = [Path(pins[k]['path']) for k in ['original_preparation_manifest', 'parent_r2_manifest', 'prior_gate_capture_manifest']]
    old_files = set()
    for seal in manifests:
        old_files.add(seal)
        for r in json.loads(seal.read_text())['files']:
            p = seal.parent/r['path']
            assert {k: ident(p)[k] for k in ['bytes', 'sha256']} == {k:r[k] for k in ['bytes', 'sha256']}
            old_files.add(p)
    watched = sorted(old_files | {Path(r['path']) for r in pins.values()} | {p for p in PRE.iterdir() if p.is_file()})
    before = {str(p): ident(p) for p in watched}
    for r in pins.values(): verify_pin(r)
    seal = PRE/'manifest-preflight.json'
    if seal.exists():
        m = json.loads(seal.read_text())
        assert {r['path'] for r in m['files']} == {p.name for p in PRE.iterdir() if p.is_file() and p != seal}
        for r in m['files']:
            assert {k:ident(PRE/r['path'])[k] for k in ['bytes','sha256']} == {k:r[k] for k in ['bytes','sha256']}
    assert not Path(proposal['final_directory']).exists(), 'This preflight requires no capture destination yet.'
    old_proposal = json.loads((parent/'proposal.json').read_text())
    assert {k:pins[k] for k in old_proposal['source_pins']} == old_proposal['source_pins']
    for key in ['run_order','fixed_protocol','child_environment_complete','timeout_seconds_per_child','core_limit','launch_accounting','x86_slice']:
        assert proposal[key] == old_proposal[key]
    assert proposal['events']['gate1-held'] == [[1537,144,60,100]]
    assert all(proposal['events'][n] == [[1537,144,60,100],[3073,128,60,64]] for n in NAMES[1:])
    delta = json.loads((PRE/'delta.json').read_text())
    rebuilt = (parent/'capture-once.py').read_text()
    for op in delta['collector_literal_changes']:
        assert rebuilt.count(op['before_literal']) == op['occurrences']
        rebuilt = rebuilt.replace(op['before_literal'], op['after_literal'])
    text = (PRE/'capture-once.py').read_text()
    assert text == rebuilt and 'before_off' not in text and 'productive-before-off' not in text
    texts = {n:(PRE/(n+'.script')).read_text() for n in NAMES}
    base = Path(pins['historical_script']['path']).read_text()
    validate(texts, base)
    for n in NAMES:
        assert texts[n] == (parent/(n+'.script')).read_text().replace('event 8193 0x80 60 64','event 3073 0x80 60 64')
    rejected = []
    def rejects(name, call):
        try: call()
        except AssertionError: rejected.append(name)
        else: raise AssertionError('bad fixture accepted: '+name)
    for label, name, old, new in [
        ('old off frame','gate1-off','event 3073 ','event 8193 '),
        ('extra minus1','gate0-off','event 3073 ','event 3072 '),
        ('wrong gate','gate1-off','param 13 1.0','param 13 0.0'),
        ('wrong off status','gate1-off','event 3073 0x80','event 3073 0x90'),
        ('wrong off velocity','gate0-off','0x80 60 64','0x80 60 0'),
        ('missing parameter','gate1-held','param 37 0.0\n',''),
        ('extra process','gate1-held','destroy\n','process 16384 512\ndestroy\n'),
        ('reset','gate0-off','create\n','create\nreset\n'),
        ('reversed queue','gate1-off','event 1537 0x90 60 100\nevent 3073 0x80 60 64','event 3073 0x80 60 64\nevent 1537 0x90 60 100')]:
        changed = dict(texts); assert old in changed[name]; changed[name] = changed[name].replace(old,new)
        rejects(label, lambda: validate(changed,base))
    finite_bytes(bytes(131072))
    for name,bad in [('short',bytes(131064)),('extra',bytes(131080)),('NaN',struct.pack('<f',math.nan)+bytes(131068)),('Inf',bytes(131068)+struct.pack('<f',math.inf))]:
        rejects(name,lambda:finite_bytes(bad))
    inp = Path(pins['input']['path']).read_bytes();finite_bytes(inp)
    assert [(i,*v) for i,v in enumerate(struct.iter_unpack('<ff',inp)) if any(v)] == [(4096,1.,1.)]
    bundle = Path(pins['bundle']['path']).read_bytes();s=proposal['x86_slice'];part=bundle[s['offset']:s['offset']+s['bytes']]
    assert hashlib.sha256(part).hexdigest() == s['sha256'] and part[:4] == b'\xcf\xfa\xed\xfe' and struct.unpack_from('<I',part,4)[0] == 0x01000007
    wrong_pin = dict(pins['input']);wrong_pin['sha256']='0'*64;rejects('provider hash',lambda:verify_pin(wrong_pin))
    for frame,status,velocity,block in [(1537,144,100,1536),(3073,128,64,3072)]:
        record=struct.pack('<qBBBB4s',frame,status,60,velocity,0,b'\0'*4)
        assert len(record)==16 and record[8:12]==bytes([status,60,velocity,0])
        assert [v for v in range(0,16384,512) if v<=frame<v+512]==[block] and frame-block==1
    tree=ast.parse(text);old_tree=ast.parse((parent/'capture-once.py').read_text())
    assert len([n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='Popen'])==1
    for key in ['parameter_echo_valid','valid_capture']:
        assert ast.dump(assignment(tree,key))==ast.dump(assignment(old_tree,key))
    validity=assignment(tree,'valid_capture');assert 'productive' not in ast.unparse(validity)
    expected_params=[s.split()[1:] for s in texts['gate1-off'].splitlines() if s.startswith('param ')]
    params=copy.deepcopy(expected_params)
    echo=assignment(tree,'parameter_echo_valid')
    assert pure_guard(echo,{'actual_params':params,'expected_params':expected_params})
    params[13][1]='0.0';assert not pure_guard(echo,{'actual_params':params,'expected_params':expected_params})
    params=copy.deepcopy(expected_params);params[13][0]='12';assert not pure_guard(echo,{'actual_params':params,'expected_params':expected_params})
    expected_events=['event 1537 0x90 60 100','event 3073 0x80 60 64']
    row={'exit_code':0,'timeout':False,'exception':None,'fault_or_trap':[], 'cxx_failbits':['cxx-failbits 0'],
         'process_lines':['process 16384 512 flags: 32x(ret=1,flag=1) blocks=32'], 'event_lines':expected_events,
         'parameter_echo_valid':True,'numeric_valid':True,'productive_response_both_channels':False}
    scope={'row':row,'err':'','lines':['create ok','rate 44100 ret=1','destroy'],'expected_events':expected_events}
    assert pure_guard(validity,scope)  # Finite zero-energy observation continues.
    for key,bad in [('numeric_valid',False),('exit_code',1),('timeout',True),('parameter_echo_valid',False),('event_lines',['event 8193 0x80 60 64']),('fault_or_trap',['TRAP']),('cxx_failbits',['cxx-failbits 1']),('process_lines',['process 16384 256 flags:'])]:
        changed=copy.deepcopy(row);changed[key]=bad;assert not pure_guard(validity,{**scope,'row':changed})
    assert not pure_guard(validity,{**scope,'err':'unexpected stderr'})
    assert "row['launch_attempted'] = True\n                child = subprocess.Popen" in text
    assert "row['pid'] = child.pid\n                row['popen_returned_pid'] = True" in text
    assert 'actual_original_x86_capture' not in text
    result=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='result' for t in n.targets))
    fields={k.value:v for k,v in zip(result.keys,result.values) if isinstance(k,ast.Constant)}
    mapping={'attempted_launches':'launch_attempted','returned_pid_children':'popen_returned_pid','structurally_valid_captures':'valid_capture'}
    accounting=[]
    for name,pid,valid,want in [('failed Popen',False,False,[1,0,0]),('early loader failure',True,False,[1,1,0]),('timeout',True,False,[1,1,0]),('success',True,True,[1,1,1])]:
        runs=[{'launch_attempted':True,'popen_returned_pid':pid,'valid_capture':valid}];got=[]
        for key,field in mapping.items():
            assert ast.dump(fields[key])==ast.dump(ast.parse("sum(r['"+field+"'] for r in runs)",mode='eval').body)
            got.append(eval(compile(ast.Expression(fields[key]),'<selected-accounting-data>','eval'),{'__builtins__':{},'sum':sum,'runs':runs}))
        assert got==want;accounting.append({'case':name,'counts':got})
    contexts=json.loads(Path(pins['parent_source_contexts']['path']).read_text());driver=Path(pins['driver_c']['path']).read_text().splitlines(True)
    for s in contexts['spans']:assert s['text']==''.join(driver[s['start_line']-1:s['end_line']])
    for p in PRE.iterdir():
        if p.is_file():assert p.read_text().endswith('\n') and all(not l.endswith((' ','\t')) for l in p.read_text().splitlines()),p
    assert before=={str(p):ident(p) for p in watched}
    print(json.dumps({'status':'Prepared data/AST checks pass; no execution authorization/result.','sealed':seal.exists(),'scripts':3,'event_coordinates':['1537=>1536+1','3073=>3072+1'], 'requested_launch_attempts_max':3,'requested_direct_exports_max':219,'negative_fixtures':rejected,'parameter_guard_negative_fixtures':2,'validity_guard_negative_fixtures':9,'accounting_fixtures':accounting,'zero_energy_structurally_admitted':True,'prior_manifest_files_verified':len(old_files),'watched':len(watched),'watch_unchanged':True,'collector_imports':0,'collector_invocations':0,'original_calls':0,'diagnostics':0,'grade':None},indent=2))

if __name__=='__main__':main()
