#!/usr/bin/env python3
"""Fixed three-child Corpus recording. Existing xdev only; no old helper imports/build."""
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
def prepare():
 assert not (H/'inputs.json').exists();proposal=B/'depth-corpus-lfo-ramp-up/proposal-asof.json';p=json.loads(proposal.read_text());reviewpath=B/'reviews/corpus-lfo-ramp-up-review.json';review=json.loads(reviewpath.read_text());assert ident(reviewpath)['sha256']=='b0005dc91623c1f629664d84dfe0bb3dfa5932e7579555dee2dfa48039cbc70d'
 base=p['scripts']['sine-baseline.script'];baseparams=[float(line.split()[2]) for line in base.splitlines() if line.startswith('param ')];assert len(baseparams)==38
 (H/'scripts').mkdir();(H/'protocol').mkdir();shutil.copyfile(T/'inputs/impulse44.f32',H/'input.f32')
 plans=[];catalog=[]
 for c in range(5):
  vector=baseparams.copy();vector[18]=float(c);script=base.replace('param 18 0.0\n',f'param 18 {c}.0\n');assert script!=base or c==0
  old=c in (0,3);row={'shape':c,'name':NAMES[c],'provenance':'inherited-approved-no-replay' if old else 'fresh-selected','parameter_bits32':[bits(v) for v in vector],'new_expected_waveform':None,'portable_comparator':None,'historical':None}
  if old:
   name='sine-baseline' if c==0 else 'ramp-up';oldhash='fadb3e890a943e637f440b83048d80a9153cc428e9c2840775057a0cc383028c' if c==0 else '40b77412adfc4768bd18e76e5df330ecd536544c50553212ba3125a8de7982ec'
   row['historical']={'review_sha256':ident(reviewpath)['sha256'],'review_pointer':'/actual_run_assessment/baseline_gate' if c==0 else '/actual_run_assessment/ramp','output_bytes':131072,'output_sha256':oldhash,'new_pid':None,'new_receipt':None}
  else:
   path=H/'scripts'/f'shape-{c}.script';path.write_text(script);plans.append({'shape':c,'script':str(path),'calls':{'CreateInstanceU':1,'SetSampleRateU':1,'SetParameterA':38,'CalcA':32,'DestroyInstanceU':1},'direct_exports':73,'frames':16384,'blocks':32,'output_bytes':131072})
  catalog.append(row)
 # Only fixed method source copied inertly; no original function body/native/provider content.
 for n in ['xdev.h','xdev.c','xdev_bind.c']:shutil.copyfile(T/'harness'/n,H/'protocol'/n)
 save(H/'inputs.json',{'schema':'whole-deterministic-Free-LFO-v1','catalog':catalog,'plans':plans,'base_params':baseparams,'base_script':base,'counts':{'logical':5,'inherited_no_replay':2,'fresh_children':3,'direct_exports':219,'CalcA':96},'excluded_random_shapes':[{'shape':5,'name':'Sample & Hold','status':'clock/seed-dependentU, retained historicalseed observation; not deterministic class'},{'shape':6,'name':'Random Ramp','status':'clock/seed-dependentU; no exact deterministic criterion'}]})
 authority=[ident(x) for x in [proposal,reviewpath,B/'depth-corpus-lfo-ramp-up/manifest.json',B/'family-corpus-routes-v1/manifest.json',T/'manifest.json',T/'harness/xdev.h',T/'harness/xdev.c',T/'harness/xdev_bind.c',T/'harness/xdev_load.c',T/'harness/xdev_cxx.c',pathlib.Path('wiki/specs/device-corpus.md'),pathlib.Path('wiki/research/corpus-dsp-static.md')]];save(H/'authority-pins.json',authority)
 exe='/var/tmp/sound-analysis/t12-xdev/xdev';bundle='/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Corpus.bundle/Contents/MacOS/Corpus'
 watched=[ident(x) for x in [exe,bundle,sys.executable,'/usr/lib/x86_64-linux-gnu/libc.so.6','/usr/lib/x86_64-linux-gnu/libm.so.6','/usr/lib/x86_64-linux-gnu/libstdc++.so.6','/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2']];watched.append(ident(bundle,16384,250352));watched.append(ident(T/'inputs/impulse44.f32'))
 assert watched[0]['sha256']=='4f3ff48d9a599e8c722bbdd8dd60a06cba35f799b113892bb83dcc68daeb9d9b' and watched[1]['sha256']=='2164ec08805b35f1571687a08b7ce7df9831102981f0e2fdbd07719dbf3ef422' and watched[-1]['sha256']=='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
 assert ident(H/'input.f32')['sha256']=='03a7d8daa68e79547578a53d7fed8e6cc872e0e81a22368615f0fa61b7b083f6'
 save(H/'context.json',{'exe':exe,'bundle':bundle,'watched':watched,'environment':{'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC','XDEV_TIME':'0','XDEV_LIBM_ULP':'0'},'host':{'uname':list(platform.uname()),'python':sys.version,'byteorder':sys.byteorder},'input_source':ident(T/'inputs/impulse44.f32'),'protocol':'Existing xdev sevenexport adapter only; create/rate38params/process/destroy; no info command, GetPlugInfoU lookup is not invocation.73directexports/child+unbounded nested/initializer calls.','custody_role':'Wholebundle/exe/runtime/slice hashes solely custody; no header/native/provider/newstate source acquisition.','substitutions':'Unchanged existing Linux/libm/libstdc++/libc++shim/fixed-time/Park-Miller model; noFP perturbation, no Apple/ARM/public equivalence.'})

def validate(d):
 assert d['schema']=='whole-deterministic-Free-LFO-v1' and d['counts']=={'logical':5,'inherited_no_replay':2,'fresh_children':3,'direct_exports':219,'CalcA':96}
 assert [r['shape'] for r in d['catalog']]==list(range(5)) and [p['shape'] for p in d['plans']]==[1,2,4]
 assert [x['shape'] for x in d['excluded_random_shapes']]==[5,6]
 base=d['base_script'];assert len(d['base_params'])==38 and d['base_params'][18]==0
 for r in d['catalog']:
  vector=d['base_params'].copy();vector[18]=float(r['shape']);assert r['parameter_bits32']==[bits(v) for v in vector] and r['name']==NAMES[r['shape']]
  assert r['new_expected_waveform'] is None and r['portable_comparator'] is None and (r['historical'] is not None)==(r['shape'] in (0,3))
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
 assert commands[:5]==['slice offset=16384 size=250352','mxcsr 0x1f80','transport 0 0 120','create ok','rate 44100 ret=0']
 params=commands[5:43];assert len(params)==38
 vector=d['base_params'].copy();vector[18]=p['shape']
 for i,line in enumerate(params):
  m=re.fullmatch(r'param (\d+) (\S+)',line);assert m and int(m[1])==i and bits(float(m[2]))==bits(vector[i])
 assert commands[43:]==['inflag 1',next(l for l in commands if l.startswith('input ')),'process 16384 512 flags: 32x(ret=0,flag=1) blocks=32','destroy','cxx-failbits 0']
 assert commands[44]=='input '+d['base_script'].split('\ninput ')[1].splitlines()[0]
 return {'imports':imports,'used':used,'exports':exports,'initializers':inits,'commands':commands,'direct_export_calls':73,'CalcA':32,'shape':p['shape']}

def audio(path):
 raw=pathlib.Path(path).read_bytes();assert len(raw)==131072
 channels=[[],[]]
 for i,(v,) in enumerate(struct.iter_unpack('<f',raw)):channels[i%2].append(v)
 stats=[]
 for ch in channels:
  finite=all(math.isfinite(x) for x in ch);stats.append({'finite':finite,'nonzero':sum(x!=0 for x in ch),'post4096_nonzero':sum(x!=0 for x in ch[4096:]),'post4096_energy':math.fsum(x*x for x in ch[4096:]) if finite else None,'peak':max(abs(x) for x in ch) if finite else None})
 return {'bytes':len(raw),'sha256':sha(raw),'frames':16384,'channels':stats}
def custody(ctx):
 out=[]
 for p in ctx['watched']+json.loads((H/'manifest-before.json').read_text())['frozen_files']:
  got=ident(p['path'],p.get('offset'),p['bytes'] if 'offset' in p else None);assert got==p,p['path'];out.append(got)
 return out

def limits():
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));resource.setrlimit(resource.RLIMIT_CPU,(20,20));resource.setrlimit(resource.RLIMIT_FSIZE,(4194304,4194304))
def run(d):
 ctx=json.loads((H/'context.json').read_text());(H/'attempts').mkdir(exist_ok=False)
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
 if sys.argv[1:]==['--prepare']:prepare()
 else:
  d=json.loads((H/'inputs.json').read_text());validate(d);controls=input_controls(d)
  if sys.argv[1:]==['--check-inputs']:print(json.dumps({'status':'PASS','input_negatives':controls,'original_calls':0,'runtime_reads':0}))
  else:assert sys.argv[1:]==['--run-once'];run(d)
