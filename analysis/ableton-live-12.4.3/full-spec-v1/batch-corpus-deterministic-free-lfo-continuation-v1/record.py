#!/usr/bin/env python3
"""Fixed two-child continuation Corpus recording. Existing xdev only; no old helper imports/build."""
import copy,hashlib,json,math,os,pathlib,platform,re,resource,shutil,signal,struct,subprocess,sys,time
from datetime import datetime,timezone
H=pathlib.Path(__file__).resolve().parent;B=H.parent;T=B.parent/'r2/t12-device-dsp-v1'
NAMES={0:'Sine',1:'Square',2:'Triangle',3:'Ramp Up',4:'Ramp Down'}
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):
 with pathlib.Path(p).open('w') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def ident(p,offset=None,size=None):
 p=pathlib.Path(p).resolve()
 if offset is None:
  h=hashlib.sha256()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b)
  return {'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
 with p.open('rb') as f:f.seek(offset);b=f.read(size)
 assert len(b)==size
 return {'path':str(p),'offset':offset,'bytes':size,'sha256':sha(b),'role':'selected slice hash custody only'}
def bits(v):return f'{struct.unpack("<I",struct.pack("<f",v))[0]:08x}'
def validate(d):
 assert d['schema']=='whole-deterministic-Free-LFO-v1' and d['counts']=={'logical':5,'inherited_no_replay':3,'fresh_children':2,'direct_exports':146,'CalcA':64}
 assert [r['shape'] for r in d['catalog']]==list(range(5)) and [p['shape'] for p in d['plans']]==[2,4]
 assert [x['shape'] for x in d['excluded_random_shapes']]==[5,6]
 base=d['base_script'];assert len(d['base_params'])==38 and d['base_params'][18]==0
 for r in d['catalog']:
  vector=d['base_params'].copy();vector[18]=float(r['shape']);assert r['parameter_bits32']==[bits(v) for v in vector] and r['name']==NAMES[r['shape']]
  assert r['new_expected_waveform'] is None and r['portable_comparator'] is None and (r['historical'] is not None)==(r['shape'] in (0,1,3))
 for p in d['plans']:
  script=pathlib.Path(p['script']);assert script==H/'scripts'/f'shape-{p["shape"]}.script'
  assert script.read_text()==base.replace('param 18 0.0\n',f'param 18 {p["shape"]}.0\n')
  assert p['direct_exports']==73 and p['blocks']==32 and p['frames']==16384 and p['output_bytes']==131072
  assert p['calls']=={'CreateInstanceU':1,'SetSampleRateU':1,'SetParameterA':38,'CalcA':32,'DestroyInstanceU':1}
 assert base.startswith('mxcsr 0x1f80\ntransport 0 0 120\ncreate\nrate 44100\n') and base.endswith('process 16384 512\ndestroy\n')
 assert 'event ' not in base and 'reset' not in base and len(re.findall(r'^param ',base,re.M))==38

def input_controls(d):
 tests=[('omit-shape',lambda x:x['plans'].pop()),('replay-sine',lambda x:x['plans'][0].update(shape=0)),('random-as-deterministic',lambda x:x['catalog'][-1].update(shape=5)),('omit-random-account',lambda x:x['excluded_random_shapes'].pop()),('wrong-input-value',lambda x:x['catalog'][1]['parameter_bits32'].__setitem__(20,'00000000')),('invented-prior',lambda x:x['catalog'][1].update(new_expected_waveform='exact')),('portable-law',lambda x:x['catalog'][1].update(portable_comparator='exact')),('wrong-count',lambda x:x['counts'].update(direct_exports=220)),('added-info',lambda x:x['plans'][0]['calls'].update(GetPlugInfoU=6)),('wrong-blocks',lambda x:x['plans'][0].update(blocks=31)),('non-null-old-receipt',lambda x:x['catalog'][0].update(historical=None)),('changed-base-vector',lambda x:x['base_params'].__setitem__(20,0.1))];out=[]
 for label,mut in tests:
  x=copy.deepcopy(d);mut(x)
  try:validate(x)
  except (AssertionError,KeyError,IndexError):out.append(label)
  else:raise AssertionError('accepted '+label)
 return out

def parse_output(text,stderr,rc,p,d):
 assert rc==0 and stderr=='';imports=[];used={};exports={};inits=[];commands=[]
 for line in text.splitlines():
  if line.startswith('init '):assert re.fullmatch(r'init 0x[0-9a-f]+',line);inits.append(line)
  elif line.startswith('import '):
   m=re.fullmatch(r'import (linux|data|trap) (\S+) slots=(\d+)',line);assert m;imports.append({'kind':m[1],'symbol':m[2],'slots':int(m[3])})
  elif line.startswith('export '):
   m=re.fullmatch(r'export (\S+) (0x[0-9a-f]+)',line);assert m and m[1] not in exports;exports[m[1]]=m[2]
  elif line.startswith('used '):
   m=re.fullmatch(r'used (\S+) (\d+)',line);assert m and m[1] not in used and int(m[2])>0;used[m[1]]=int(m[2])
  else:commands.append(line)
 assert len(imports)==127 and len({x['symbol'] for x in imports})==127 and sum(x['kind']=='trap' for x in imports)==21
 assert set(used)<={x['symbol'] for x in imports if x['kind']=='linux'}
 assert set(exports)=={'_CreateInstanceU','_DestroyInstanceU','_SetSampleRateU','_GetPlugInfoU','_CalcA','_SetParameterA','_ResetA'} and exports['_CreateInstanceU']=='0x23b0' and exports['_CalcA']=='0x29c0'
 assert commands[:4]==['slice offset=16384 size=250352','mxcsr 0x1f80','transport 0 0 120','create ok']
 rate_match=re.fullmatch(r'rate 44100 ret=(-?\d+)',commands[4]);assert rate_match;rate_return=int(rate_match[1])
 params=commands[5:43];assert len(params)==38
 vector=d['base_params'].copy();vector[18]=p['shape']
 for i,line in enumerate(params):
  m=re.fullmatch(r'param (\d+) (\S+)',line);assert m and int(m[1])==i and bits(float(m[2]))==bits(vector[i])
 assert commands[43:]==['inflag 1',next(l for l in commands if l.startswith('input ')),'process 16384 512 flags: 32x(ret=0,flag=1) blocks=32','destroy','cxx-failbits 0']
 assert commands[44]=='input '+d['base_script'].split('\ninput ')[1].splitlines()[0]
 return {'imports':imports,'used':used,'exports':exports,'initializers':inits,'commands':commands,'direct_export_calls':73,'CalcA':32,'shape':p['shape'],'rate_return_observed':rate_return,'rate_return_semantics':None}

def audio(path):
 raw=pathlib.Path(path).read_bytes();assert len(raw)==131072
 channels=[[],[]]
 for i,(v,) in enumerate(struct.iter_unpack('<f',raw)):channels[i%2].append(v)
 stats=[]
 for ch in channels:
  finite=all(math.isfinite(x) for x in ch);stats.append({'finite':finite,'nonzero':sum(x!=0 for x in ch),'post4096_nonzero':sum(x!=0 for x in ch[4096:]),'post4096_energy':math.fsum(x*x for x in ch[4096:]) if finite else None,'peak':max(abs(x) for x in ch) if finite else None})
 return {'bytes':len(raw),'sha256':sha(raw),'frames':16384,'channels':stats}
def validate_roles(ctx):
 roles=ctx['watched_roles'];names=['loader','universal_bundle','python','libc','libm','libstdcxx','elf_interpreter','selected_x86_slice','source_I1_input']
 assert len(roles)==9 and [r['role'] for r in roles]==names
 byrole={r['role']:r['identity'] for r in roles}
 assert byrole['loader']['path']==ctx['exe'] and byrole['loader']['bytes']==149632 and byrole['loader']['sha256']=='4f3ff48d9a599e8c722bbdd8dd60a06cba35f799b113892bb83dcc68daeb9d9b'
 assert byrole['universal_bundle']['path']==ctx['bundle'] and byrole['universal_bundle']['sha256']=='2164ec08805b35f1571687a08b7ce7df9831102981f0e2fdbd07719dbf3ef422'
 assert byrole['selected_x86_slice']['path']==ctx['bundle'] and byrole['selected_x86_slice']['offset']==16384 and byrole['selected_x86_slice']['bytes']==250352 and byrole['selected_x86_slice']['sha256']=='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
 assert byrole['source_I1_input']==ctx['input_source'] and byrole['source_I1_input']['sha256']=='03a7d8daa68e79547578a53d7fed8e6cc872e0e81a22368615f0fa61b7b083f6'
 assert len({byrole[n]['path'] for n in names if n!='selected_x86_slice'})==8

def custody(ctx):
 out=[]
 for p in [item['identity'] for item in ctx['watched_roles']]+json.loads((H/'manifest-before.json').read_text())['frozen_files']:
  got=ident(p['path'],p.get('offset'),p['bytes'] if 'offset' in p else None);assert got==p,p['path'];out.append(got)
 return out

def limits():
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));resource.setrlimit(resource.RLIMIT_CPU,(20,20));resource.setrlimit(resource.RLIMIT_FSIZE,(4194304,4194304))
def run(d):
 ctx=json.loads((H/'context.json').read_text());validate_roles(ctx);(H/'attempts').mkdir(exist_ok=False)
 a={'status':'RUNNING','utc_start':now(),'outer_pid':os.getpid(),'outer_argv':sys.argv,'children':[],'error':None,'phases':{'validated':True,'custody_before':False,'calls_started':False,'all_children_completed':False,'custody_after':False}};save(H/'results.json',a)
 def stop(sig,frame):raise RuntimeError('outer signal '+str(sig))
 signal.signal(signal.SIGTERM,stop)
 try:
  a['custody_before']=custody(ctx);a['phases']['custody_before']=True
  for plan in d['plans']:
   directory=H/'attempts'/f'shape-{plan["shape"]}';directory.mkdir();output=directory/'output.f32';argv=[ctx['exe'],ctx['bundle'],plan['script'],str(output),'--imports'];c={'shape':plan['shape'],'argv':argv,'utc_start':now(),'pid':None,'exit':None,'timeout':False,'cleanup':None,'status':'PREPARED'};a['children'].append(c);save(H/'results.json',a);proc=None;start=time.monotonic()
   try:
    with (directory/'stdout.txt').open('xb') as out,(directory/'stderr.txt').open('xb') as err:
     proc=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,cwd=H,env=ctx['environment'],preexec_fn=limits,start_new_session=True);c['pid']=proc.pid;c['status']='RUNNING';a['phases']['calls_started']=True;save(H/'results.json',a)
     try:c['exit']=proc.wait(timeout=20)
     except subprocess.TimeoutExpired:c['timeout']=True;os.killpg(proc.pid,signal.SIGKILL);c['exit']=proc.wait(timeout=5);c['cleanup']='group killed/direct child reaped'
   finally:
    if proc is not None and proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL);c['exit']=proc.wait(timeout=5);c['cleanup']='interrupted group killed/direct child reaped'
    c.update(utc_end=now(),elapsed_seconds=time.monotonic()-start)
    for key,path in [('stdout',directory/'stdout.txt'),('stderr',directory/'stderr.txt'),('audio',output)]:
     if path.exists():c[key]=ident(path)
    save(H/'results.json',a)
   assert not c['timeout'];c['parsed']=parse_output((directory/'stdout.txt').read_text(),(directory/'stderr.txt').read_text(),c['exit'],plan,d);c['audio_stats']=audio(output);save(H/'results.json',a)
   assert all(s['finite'] for s in c['audio_stats']['channels']),'nonfinite output; preserve and stop later children'
   c['status']='RECORDED';c['custody_after']=custody(ctx);assert c['custody_after']==a['custody_before'];save(H/'results.json',a);print('shape',plan['shape'],'recorded',c['audio_stats']['sha256'],flush=True)
  a['phases']['all_children_completed']=True;a['custody_after']=a['children'][-1]['custody_after'];a['phases']['custody_after']=True;a['status']='COMPLETE-ONCE-NO-RETRY'
 except BaseException as e:
  a['status']='STOPPED-NO-RETRY';a['error']={'type':type(e).__name__,'message':str(e)}
  try:a['custody_after_failure']=custody(ctx)
  except BaseException as e2:a['custody_failure']=str(e2)
  raise
 finally:a['utc_end']=now();save(H/'results.json',a)
if __name__=='__main__':
 d=json.loads((H/'inputs.json').read_text());validate(d);validate_roles(json.loads((H/'context.json').read_text()));controls=input_controls(d)
 if sys.argv[1:]==['--check-inputs']:print(json.dumps({'status':'PASS','input_negatives':controls,'original_calls':0,'runtime_reads':0}))
 else:assert sys.argv[1:]==['--run-once'];run(d)
