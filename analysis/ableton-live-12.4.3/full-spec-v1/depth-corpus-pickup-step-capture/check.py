"""Read-only preparation checks. No collector import/invocation or native calls."""
from pathlib import Path
import ast, copy, hashlib, json, math, re, struct, sys
PRE = Path(__file__).resolve().parent

def ident(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def scripts_from(e, input_path):
    result = {}
    for name, step in [('control', e['parameters']['ListeningXL']), ('left-step', .75)]:
        lines = ['mxcsr 0x1f80', 'transport 0 0 120', 'create', 'rate 44100']
        lines += ['param '+str(i)+' '+repr(float(e['parameters'][key])) for i, key in enumerate(e['parameter_order'])]
        lines += ['inflag 1', 'input '+input_path, 'process 8192 512', 'param 15 '+repr(float(step)), 'process 8192 512', 'destroy']
        result[name] = lines
    return result

def main():
    if sys.argv[1:] != ['--check']: raise SystemExit('Read-only --check only. Collector/native execution is never performed.')
    p = json.loads((PRE/'proposal.json').read_text())
    history = json.loads((PRE/'preservation-inputs.json').read_text())
    pins = list(p['source_pins'].values()) + history
    watched = {Path(r['path']) for r in pins} | {f for f in PRE.iterdir() if f.is_file()}
    before = {str(f): ident(f) for f in watched}
    for r in pins: assert ident(Path(r['path'])) == r
    seal = PRE/'manifest-preflight.json'
    if seal.exists():
        m = json.loads(seal.read_text())
        assert {r['path'] for r in m['files']} == {f.name for f in PRE.iterdir() if f.is_file() and f != seal}
        for r in m['files']:
            assert {k:ident(PRE/r['path'])[k] for k in ['bytes','sha256']} == {k:r[k] for k in ['bytes','sha256']}
    assert not Path(p['final_directory']).exists(), 'Capture destination already exists: no longer preflight-only.'
    source = json.loads(Path(p['source_pins']['released_vector']['path']).read_text())
    e = source['cases'][5]['evaluations'][0]
    assert e['id'] == p['source_evaluation_id'] == 'CORPUS-AUDIO-006-01'
    assert p['source_vector'] == {k:e[k] for k in ['parameters','parameter_order']}
    assert (e['sample_rate_hz'], e['frames'], e['block_frames']) == (44100,16384,512)
    assert [e['parameters'][s] for s in ['ResonanceType','ResonatorQuality','MidiPitch','MidiGate','LfoOnOff']] == [3,3,0,0,0]
    assert p['fixed_protocol'] == {'rate':44100,'frames':16384,'channels':2,'block':512,
       'format':'headerless little-endian binary32 stereo','impulse':4096,'step_host_frame':8192,
       'process_segments':[8192,8192],'inflag_each_block':1,'transport':[0,0,120],'mxcsr':'0x1f80',
       'time':0,'events':[],'fresh_child_and_instance_each':True,'no_info_reset_warmup_seedperturbation':True}
    ancestor = json.loads(Path(p['source_pins']['environment_and_slice_provider']['path']).read_text())
    assert p['child_environment_complete'] == ancestor['child_environment_complete']
    assert p['x86_slice'] == ancestor['x86_slice']
    assert p['run_order'] == ['control','left-step']
    assert p['expected'] is None and p['comparison'] is None and p['grade'] is None
    expected = scripts_from(e, p['source_pins']['input']['path'])
    texts = {n:(PRE/(n+'.script')).read_text().splitlines() for n in expected}
    def validate(texts):
        assert texts == expected == p['scripts']
        for lines in texts.values():
            params = [s.split() for s in lines if s.startswith('param ')]
            assert len(params) == 39 and [int(s[1]) for s in params[:38]] == list(range(38))
            assert sum(s.startswith(('create','rate ','param ','destroy')) for s in lines) + 32 == 74
        assert 2*74 == p['limits']['max_requested_direct_exports_total'] == 148 < 256
    validate(texts)
    negative = []
    def rejects(label, call):
        try: call()
        except AssertionError: negative.append(label)
        else: raise AssertionError('bad fixture accepted: '+label)
    for label, old, new in [
        ('wrong boundary','process 8192 512','process 7680 512'),
        ('wrong block','process 8192 512','process 8192 256'),
        ('wrong step','param 15 0.75','param 15 0.5'),
        ('wrong right pickup','param 16 0.8999999761581421','param 16 0.75'),
        ('extra event','inflag 1','event 1537 0x90 60 100\ninflag 1'),
        ('reset','create','create\nreset'),
        ('input reopened','param 15 0.75','input '+p['source_pins']['input']['path']+'\nparam 15 0.75'),
        ('missing destroy','destroy',''),
        ('missing initial parameter','param 37 0.0',''),
        ('transport changed','transport 0 0 120','transport 1 0 120'),
        ('input flag changed','inflag 1','inflag 0'),
        ('single process','process 8192 512\nparam 15 0.75\nprocess 8192 512','process 16384 512')]:
        bad=copy.deepcopy(texts);s='\n'.join(bad['left-step']);assert old in s
        bad['left-step']=s.replace(old,new).splitlines();rejects(label,lambda:validate(bad))
    inp=Path(p['source_pins']['input']['path']).read_bytes()
    assert [(i,*f) for i,f in enumerate(struct.iter_unpack('<ff',inp)) if any(f)] == [(4096,1.,1.)]
    bundle=Path(p['source_pins']['bundle']['path']).read_bytes();s=p['x86_slice']
    assert hashlib.sha256(bundle[s['offset']:s['offset']+s['bytes']]).hexdigest()==s['sha256']
    # Compile ONLY these two freshly inspected, pure data functions from NEW collector AST.
    # No collector imports, top-level statements, main, Popen or source/native functions run.
    text=(PRE/'capture-once.py').read_text();tree=ast.parse(text)
    pure=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'finite_output','valid_log'}]
    assert len(pure)==2
    assert not any(isinstance(n,ast.Attribute) and n.attr in {'open','Popen','read_bytes','write_bytes','main'} for f in pure for n in ast.walk(f))
    scope={'math':math,'re':re,'struct':struct}
    exec(compile(ast.Module(body=pure,type_ignores=[]),'<new-owned-pure-data-guards>','exec'),scope)
    finite,valid=scope['finite_output'],scope['valid_log']
    assert finite(bytes(131072))  # Silence is structurally valid.
    for label,bad in [('short',bytes(131064)),('extra',bytes(131080)),('NaN',struct.pack('<f',math.nan)+bytes(131068)),('Inf',bytes(131068)+struct.pack('<f',math.inf))]:
        assert not finite(bad);negative.append(label)
    logs={}
    for name,lines in expected.items():
        echoed=[]
        for line in lines:
            if line=='create': line='create ok'
            elif line=='rate 44100': line='rate 44100 ret=1'
            elif line=='process 8192 512': line+=' flags: 16x(ret=0,flag=0) blocks=16'
            echoed.append(line)
        logs[name]='\n'.join(echoed+['cxx-failbits 0','import trap _unused slots=1'])+'\n'
        assert valid(logs[name],'',[s.split()[1:] for s in lines if s.startswith('param ')],p['source_pins']['input']['path'])
    pars=[s.split()[1:] for s in expected['left-step'] if s.startswith('param ')]
    log=logs['left-step'];ip=p['source_pins']['input']['path']
    for label,bad in [('one32segment',log.replace('process 8192 512 flags: 16x(ret=0,flag=0) blocks=16','process 16384 512 flags: 32x(ret=0,flag=0) blocks=32',1)),('missing process',log.replace('process 8192 512 flags: 16x(ret=0,flag=0) blocks=16\n','',1)),('wrong RLE count',log.replace('16x(ret=0','15x(ret=0',1)),('wrong step echo',log.replace('param 15 0.75','param 15 0.5')),('actual trap',log+'TRAP _actual\n'),('cxx failure',log.replace('cxx-failbits 0','cxx-failbits 1')),('extra reset',log+'reset\n')]:
        assert not valid(bad,'',pars,ip);negative.append(label)
    assert not valid(log,'unexpected stderr',pars,ip)
    guard = next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(
        isinstance(t,ast.Subscript) and isinstance(t.slice,ast.Constant) and t.slice.value=='valid_capture' for t in n.targets))
    row = {'exit_code':0,'timeout':False,'exception':None,'log_valid':True,'numeric_valid':True}
    def capture_valid(row):
        return eval(compile(ast.Expression(guard),'<new-owned-status-guard>','eval'),{'__builtins__':{},'row':row})
    assert capture_valid(row)
    for key,bad in [('exit_code',1),('timeout',True),('exception','failed Popen'),('log_valid',False),('numeric_valid',False)]:
        changed=dict(row);changed[key]=bad;assert not capture_valid(changed);negative.append('status '+key)
    assert text.count('subprocess.Popen(')==1 and 'range(2)' not in text
    assert "row['launch_attempted'] = True\n                child = subprocess.Popen" in text
    assert "row['pid'] = child.pid\n                row['popen_returned_pid'] = True" in text
    result=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='result' for t in n.targets))
    fields={k.value:v for k,v in zip(result.keys,result.values) if isinstance(k,ast.Constant)}
    accounting=[]
    for label,pid,ok,want in [('failed Popen',False,False,[1,0,0]),('early loader failure',True,False,[1,1,0]),('timeout',True,False,[1,1,0]),('success',True,True,[1,1,1])]:
        runs=[{'launch_attempted':True,'popen_returned_pid':pid,'valid_capture':ok}];got=[]
        for k,f in [('attempted_launches','launch_attempted'),('returned_pid_children','popen_returned_pid'),('structurally_valid_captures','valid_capture')]:
            assert ast.dump(fields[k])==ast.dump(ast.parse("sum(r['"+f+"'] for r in runs)",mode='eval').body)
            got.append(eval(compile(ast.Expression(fields[k]),'<new-owned-accounting>','eval'),{'__builtins__':{},'sum':sum,'runs':runs}))
        assert got==want;accounting.append({'case':label,'counts':got})
    for f in PRE.iterdir():
        if f.is_file(): assert f.read_text().endswith('\n') and all(line.rstrip()==line for line in f.read_text().splitlines())
    assert before=={str(f):ident(f) for f in watched}
    print(json.dumps({'status':'PASS preparation data/AST only','sealed':seal.exists(),'scripts':2,'direct_exports_max':148,
       'negative_fixtures':negative,'accounting_fixtures':accounting,'silent_zero_flags_valid':True,
       'historical_paths':len(history),'watched':len(watched),'watch_unchanged':True,'collector_imports':0,
       'collector_invocations':0,'native_calls':0,'measurements_or_fits':0,'grade':None},indent=2))

if __name__=='__main__':main()
