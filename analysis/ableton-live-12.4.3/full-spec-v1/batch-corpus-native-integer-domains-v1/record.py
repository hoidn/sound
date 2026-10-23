#!/usr/bin/env python3
"""Whole57-child native integer-domain Corpus recording. Existing xdev only; no old helper imports/build."""
import copy,hashlib,json,math,os,pathlib,platform,re,resource,shutil,signal,struct,subprocess,sys,time
from datetime import datetime,timezone
H=pathlib.Path(__file__).resolve().parent;B=H.parent;T=B.parent/'r2/t12-device-dsp-v1'

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
def planned_script(u):
 return '\n'.join(['mxcsr 0x1f80','transport 0 0 120','create','rate 44100']+[f'param {w["index"]} {w["token"]}' for w in u['words']]+['inflag 1','input '+str(H/'input.f32'),'process 16384 512','destroy'])+'\n'
def vector_sha(params):return sha(b''.join(struct.pack('<f',float(x)) for x in params))
def validate(d):
 e=json.loads((H/'eligibility.json').read_text());prior=json.loads((H/'approved-prior-summary.json').read_text())
 assert d['schema']=='whole-Corpus-native-integer-domains-v1' and d['domains']==e['domains'] and d['base_params']==e['base_params']
 assert d['counts']=={'aliases':69,'unique_vectors':63,'inherited_vectors':6,'fresh_children':57,'direct_exports':4161,'CalcA':1824,'stereo_bytes':7471104}
 assert [(x['index'],int(x['max'])) for x in d['domains']]==[(0,6),(10,24),(17,1),(18,6),(21,21),(27,1),(33,3)]
 assert d['fixture']=={'rate':44100,'frames':16384,'block':512,'last_block':512,'inflag':1,'I1_impulse_frame':4096,'transport':[0,0,120],'MXCSR':'0x1f80','warmup':0,'XDEV_TIME':'0','XDEV_LIBM_ULP':'0'}
 assert d['baseline_vector_sha256']==vector_sha(d['base_params'])=='9b98e8cab7aae28b01e18de3cd9570db62721f0ecdbf951bd5bd77d8b378e6e2'
 assert ident(H/'input.f32')==d['input'] and d['input']['bytes']==131072 and d['input']['sha256']=='03a7d8daa68e79547578a53d7fed8e6cc872e0e81a22368615f0fa61b7b083f6'
 assert len(d['catalog'])==69 and len(d['vectors'])==63 and len(d['plans'])==57
 expected_pairs=[(x['index'],v) for x in d['domains'] for v in range(int(x['max'])+1)];assert [(r['index'],r['value']) for r in d['catalog']]==expected_pairs
 seen={};aliases={};hist={}
 for p in prior['approved_summary']['approved_points']:
  params=d['base_params'].copy();params[18]=p['shape'];h=vector_sha(params)
  assert [bits(x) for x in params]==p['parameter_bits32'];hist[h]=('approved-summary-no-replay',p)
 params=d['base_params'].copy();params[18]=5.;hist[vector_sha(params)]=('qualified-historical-shape5-metadata-only',prior['shape5_qualified_reference'])
 for i,(row,erow) in enumerate(zip(d['catalog'],e['catalog'])):
  assert row['id']==f'CNI-A{i:03}' and row['index']==erow['index'] and row['value']==erow['value'] and type(row['value']) is int
  params=d['base_params'].copy();params[row['index']]=float(row['value']);h=vector_sha(params);assert row['vector_sha256']==h==erow['vector_sha256']
  if h not in seen:seen[h]=f'CNI-V{len(seen):03}'
  assert row['vector_id']==seen[h];aliases.setdefault(row['vector_id'],[]).append(row['id'])
  assert all(row[k] is None for k in ['new_expected_waveform','portable_expected','portable_comparator','grade'])
 assert [u['id'] for u in d['vectors']]==list(seen.values()) and len(set(u['vector_sha256'] for u in d['vectors']))==63
 fresh=[]
 for u in d['vectors']:
  assert u['alias_ids']==aliases[u['id']] and [w['index'] for w in u['words']]==list(range(38))
  params=[float(w['token']) for w in u['words']];assert vector_sha(params)==u['vector_sha256']
  i=u['first_alias']['index'];v=u['first_alias']['value'];expected=d['base_params'].copy();expected[i]=float(v);assert [bits(x) for x in params]==[bits(x) for x in expected]
  assert all(w['binary32_le']==struct.pack('<f',float(w['token'])).hex() and w['host_reconstructed_binary64_le']==struct.pack('<d',float(w['token'])).hex() for w in u['words'])
  assert all(u[k] is None for k in ['new_expected_waveform','portable_expected','portable_comparator','grade'])
  if u['vector_sha256'] in hist:
   assert u['disposition']=='inherited-no-replay' and 'script' not in u and u['inherited'] is not None
   h=u['inherited'];assert h['kind']==hist[u['vector_sha256']][0] and h['fresh_pid'] is h['fresh_receipt'] is h['new_metrics'] is None
   if h['kind']=='approved-summary-no-replay':assert h['approved_point']==hist[u['vector_sha256']][1]
   else:assert h['historical']==hist[u['vector_sha256']][1] and h['qualification']==h['historical']['qualification']
  else:
   assert u['disposition']=='fresh-selected' and u['inherited'] is None;fresh.append(u['id']);assert ident(u['script']['path'])==u['script'];assert pathlib.Path(u['script']['path'])==H/'scripts'/(u['id']+'.script') and pathlib.Path(u['script']['path']).read_text()==planned_script(u)
 assert [p['vector_id'] for p in d['plans']]==fresh and len(hist)==6
 byid={u['id']:u for u in d['vectors']}
 for p in d['plans']:assert p=={'vector_id':p['vector_id'],'vector_sha256':byid[p['vector_id']]['vector_sha256'],'script':byid[p['vector_id']]['script'],'direct_exports':73,'CalcA':32,'output_bytes':131072}

def input_controls(d):
 tests=[('omit-alias',lambda x:x['catalog'].pop()),('omit-vector',lambda x:x['vectors'].pop()),('omit-plan',lambda x:x['plans'].pop()),('domain-missing',lambda x:x['domains'].pop()),('domain-crossproduct',lambda x:x['domains'][0].update(max=7)),('domain-virtual',lambda x:x['domains'][0].update(virtual=True)),('alias-duplicate',lambda x:x['catalog'][1].update(value=0)),('alias-fractional',lambda x:x['catalog'][0].update(value=.5)),('wrong-vector-link',lambda x:x['catalog'][0].update(vector_id='CNI-V002')),('baseline-dropped',lambda x:x['catalog'][2].update(vector_sha256='0'*64)),('word38-missing',lambda x:x['vectors'][0]['words'].pop()),('fixed-other-word',lambda x:x['vectors'][0]['words'][1].update(token='0.0')),('wrong-f32',lambda x:x['vectors'][0]['words'][0].update(binary32_le='0000803f')),('wrong-f64',lambda x:x['vectors'][0]['words'][0].update(host_reconstructed_binary64_le='000000000000f03f')),('invented-prior',lambda x:x['vectors'][0].update(new_expected_waveform='law')),('portable-expected',lambda x:x['catalog'][0].update(portable_expected='law')),('portable-comparator',lambda x:x['vectors'][0].update(portable_comparator='exact')),('grade',lambda x:x['catalog'][0].update(grade='PASS')),('seed',lambda x:x['fixture'].update(XDEV_TIME='1')),('inflag',lambda x:x['fixture'].update(inflag=0)),('impulse',lambda x:x['fixture'].update(I1_impulse_frame=0)),('rate',lambda x:x['fixture'].update(rate=48000)),('count',lambda x:x['counts'].update(fresh_children=63))]
 old=next(i for i,u in enumerate(d['vectors']) if u['inherited'] is not None);sah=next(i for i,u in enumerate(d['vectors']) if u['inherited'] and u['inherited']['kind']=='qualified-historical-shape5-metadata-only')
 tests += [('replay-inherited',lambda x:x['plans'][0].update(vector_id=x['vectors'][old]['id'])),('invent-old-PID',lambda x:x['vectors'][old]['inherited'].update(fresh_pid=1)),('drop-shape5-qualification',lambda x:x['vectors'][sah]['inherited'].update(qualification='proved'))]
 out=[]
 for name,mut in tests:
  x=copy.deepcopy(d);mut(x)
  try:validate(x)
  except (AssertionError,KeyError,IndexError,ValueError):out.append(name)
  else:raise AssertionError('accepted '+name)
 return out

def parse_output(text,stderr,rc,p,d):
 assert rc==0 and stderr=='' and not re.search(r'\b(TRAP|FAULT)\b',text);imports=[];used={};exports={};inits=[];commands=[]
 for line in text.splitlines():
  if line.startswith('init '):assert re.fullmatch(r'init 0x[0-9a-f]+',line);inits.append(line)
  elif line.startswith('import '):
   m=re.fullmatch(r'import (linux|data|trap) (\S+) slots=(\d+)',line);assert m;imports.append({'kind':m[1],'symbol':m[2],'slots':int(m[3])})
  elif line.startswith('export '):
   m=re.fullmatch(r'export (\S+) (0x[0-9a-f]+)',line);assert m and m[1] not in exports;exports[m[1]]=m[2]
  elif line.startswith('used '):
   m=re.fullmatch(r'used (\S+) (\d+)',line);assert m and m[1] not in used and int(m[2])>0;used[m[1]]=int(m[2])
  else:commands.append(line)
 assert len(imports)==127 and len({x['symbol'] for x in imports})==127 and {k:sum(x['kind']==k for x in imports) for k in ['trap','linux','data']}=={'trap':21,'linux':99,'data':7}
 assert set(used)<={x['symbol'] for x in imports if x['kind']=='linux'}
 assert set(exports)=={'_CreateInstanceU','_DestroyInstanceU','_SetSampleRateU','_GetPlugInfoU','_CalcA','_SetParameterA','_ResetA'} and exports['_CreateInstanceU']=='0x23b0' and exports['_CalcA']=='0x29c0'
 assert commands[:4]==['slice offset=16384 size=250352','mxcsr 0x1f80','transport 0 0 120','create ok']
 rate_match=re.fullmatch(r'rate 44100 ret=(-?\d+)',commands[4]);assert rate_match;rate_return=int(rate_match[1])
 params=commands[5:43];assert len(params)==38
 vector=[float(w['token']) for w in next(u for u in d['vectors'] if u['id']==p['vector_id'])['words']]
 for i,line in enumerate(params):
  m=re.fullmatch(r'param (\d+) (\S+)',line);assert m and int(m[1])==i and bits(float(m[2]))==bits(vector[i])
 assert commands[43:45]==['inflag 1','input '+str(H/'input.f32')] and commands[46:]==['destroy','cxx-failbits 0']
 m=re.fullmatch(r'process 16384 512 flags:((?: [1-9][0-9]*x\(ret=-?\d+,flag=-?\d+\))+ blocks=32)',commands[45]);assert m
 groups=[list(map(int,g)) for g in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)',commands[45])];assert sum(g[0] for g in groups)==32 and all(g[1]==0 and g[2] in (0,1) for g in groups)
 return {'imports':imports,'used':used,'exports':exports,'initializers':inits,'commands':commands,'direct_export_calls':73,'CalcA':32,'vector_id':p['vector_id'],'CalcA_groups':groups,'rate_return_observed':rate_return,'rate_return_semantics':None}

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
 for p in [item['identity'] for item in ctx['watched_roles']]+json.loads((H/'pre-call-manifest.json').read_text())['frozen_files']:
  got=ident(p['path'],p.get('offset'),p['bytes'] if 'offset' in p else None);assert got==p,p['path'];out.append(got)
 return out

def limits():
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));resource.setrlimit(resource.RLIMIT_CPU,(20,20));resource.setrlimit(resource.RLIMIT_FSIZE,(4194304,4194304))
def run(d,prehash):
 assert sha((H/'pre-call-manifest.json').read_bytes())==prehash
 ctx=json.loads((H/'context.json').read_text());validate_roles(ctx);(H/'attempts').mkdir(exist_ok=False)
 a={'status':'RUNNING','utc_start':now(),'outer_pid':os.getpid(),'outer_argv':sys.argv,'children':[],'error':None,'phases':{'validated':True,'custody_before':False,'calls_started':False,'all_children_completed':False,'custody_after':False}};save(H/'results.json',a)
 def stop(sig,frame):raise RuntimeError('outer signal '+str(sig))
 signal.signal(signal.SIGTERM,stop)
 try:
  a['custody_before']=custody(ctx);a['phases']['custody_before']=True
  for plan in d['plans']:
   directory=H/'attempts'/plan['vector_id'];directory.mkdir();output=directory/'output.f32';argv=[ctx['exe'],ctx['bundle'],plan['script']['path'],str(output),'--imports'];c={'vector_id':plan['vector_id'],'argv':argv,'utc_start':now(),'pid':None,'exit':None,'timeout':False,'cleanup':None,'status':'PREPARED'};a['children'].append(c);save(H/'results.json',a);proc=None;start=time.monotonic()
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
   c['status']='RECORDED';c['custody_after']=custody(ctx);assert c['custody_after']==a['custody_before'];save(H/'results.json',a);print('vector',plan['vector_id'],'recorded',c['audio_stats']['sha256'],flush=True)
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
 else:assert len(sys.argv)==3 and sys.argv[1]=='--run-once';run(d,sys.argv[2])
