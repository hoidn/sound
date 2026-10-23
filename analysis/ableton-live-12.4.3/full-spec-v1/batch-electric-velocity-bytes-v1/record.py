#!/usr/bin/env python3
"""Fixed127-child recording; existing unmodified Electric xdev, no old module imports."""
import copy,hashlib,json,math,os,pathlib,re,resource,signal,struct,subprocess,sys,time
from datetime import datetime,timezone
H=pathlib.Path(__file__).resolve().parent
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):
 with pathlib.Path(p).open('w') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def ident(p,offset=None,size=None):
 p=pathlib.Path(p).resolve();h=hashlib.sha256();n=0
 with p.open('rb') as f:
  if offset is not None:f.seek(offset)
  while True:
   b=f.read(min(1048576,size-n) if size is not None else 1048576)
   if not b:break
   h.update(b);n+=len(b)
   if size is not None and n==size:break
 assert size is None or n==size
 d={'path':str(p),'bytes':n,'sha256':h.hexdigest()}
 if offset is not None:d['offset']=offset
 return d
def bits(v):return struct.pack('<f',float(v)).hex()
def script(d,v):
 return '\n'.join(['create','rate 44100']+[f'param {w["index"]} {w["token"]}' for w in d['words']]+[f'event 11264 0x90 60 {v}','event 33314 0x80 60 0','inflag 0','input zero','process 11264 512','process 44100 512','destroy'])+'\n'
def validate(d):
 assert d['schema']=='whole-Electric-P1-note-on-velocity-byte-v1'
 assert len(d['words'])==33 and [w['index'] for w in d['words']]==list(range(33))
 assert all(bits(w['token'])==w['little_endian_hex'] and struct.pack('<d',float(w['token'])).hex()==w['reconstructed_binary64_le'] for w in d['words'])
 assert sha(b''.join(bytes.fromhex(w['little_endian_hex']) for w in d['words']))=='9ef2b39d47ca833730a9bbfd9d26e3bdc08a847df0ead035bd14d948bc35a43a'
 assert [r['velocity_byte'] for r in d['catalog']]==list(range(128)) and all(type(r['velocity_byte']) is int for r in d['catalog'])
 assert [p['velocity_byte'] for p in d['plans']]==[v for v in range(128) if v!=100]
 assert d['counts']=={'logical':128,'inherited':1,'fresh_children':127,'direct_exports':18415,'CalcA':13843,'stereo_bytes':56249824}
 for r in d['catalog']:
  assert r['expected_waveform'] is None and r['portable_expected'] is None and r['portable_comparator'] is None and r['grade'] is None
  assert r['events']==[[11264,144,60,r['velocity_byte']],[33314,128,60,0]]
  assert r['packed16_events_le']==[struct.pack('<qBBBB4x',*e,0).hex() for e in r['events']]
  assert (r['historical'] is not None)==(r['velocity_byte']==100)
 for p in d['plans']:
  assert p['script']==str(H/'scripts'/f'velocity-{p["velocity_byte"]:03}.script')
  assert pathlib.Path(p['script']).read_text()==script(d,p['velocity_byte'])
 assert d['fixture']=={'sample_rate':44100,'frames':44100,'block':512,'last_block':68,'warmup':11264,'key':60,'on_velocity':'catalog_byte','off_velocity':0,'input':'zero','inflag':0,'transport':[0,0,120],'MXCSR':'0x1f80','XDEV_TIME':'0 existing treatment','LIBM_ULP':'absent/unperturbed'}
def controls(d):
 tests=[('drop-endpoint',lambda x:x['catalog'].pop()),('replay-old',lambda x:x['plans'][0].update(velocity_byte=100)),('omit-fresh',lambda x:x['plans'].pop()),('change-word',lambda x:x['words'][0].update(token='29.0')),('wrong-index',lambda x:x['words'][0].update(index=33)),('wrong-count',lambda x:x['counts'].update(fresh_children=126)),('new-oracle',lambda x:x['catalog'][0].update(expected_waveform='silence')),('portable-law',lambda x:x['catalog'][0].update(portable_comparator='exact')),('off-key',lambda x:x['catalog'][0]['events'][1].__setitem__(2,1)),('off-velocity',lambda x:x['catalog'][0]['events'][1].__setitem__(3,1)),('on-frame',lambda x:x['catalog'][0]['events'][0].__setitem__(0,11265)),('fabricated-old',lambda x:x['catalog'][0].update(historical={})),('drop-old',lambda x:x['catalog'][100].update(historical=None)),('block',lambda x:x['fixture'].update(block=256)),('inputflag',lambda x:x['fixture'].update(inflag=1)),('seed',lambda x:x['fixture'].update(XDEV_TIME='12345')),('warmup',lambda x:x['fixture'].update(warmup=0)),('portable-expected',lambda x:x['catalog'][0].update(portable_expected='exact')),('grade',lambda x:x['catalog'][0].update(grade='P')),('on-key',lambda x:x['catalog'][0]['events'][0].__setitem__(2,1)),('on-velocity',lambda x:x['catalog'][0]['events'][0].__setitem__(3,1)),('packed-event',lambda x:x['catalog'][0]['packed16_events_le'].__setitem__(0,'00'*16)),('f64-input',lambda x:x['words'][0].update(reconstructed_binary64_le='00'*8))];out=[]
 for name,mut in tests:
  x=copy.deepcopy(d);mut(x)
  try:validate(x)
  except (AssertionError,KeyError,IndexError):out.append(name)
  else:raise AssertionError('accepted '+name)
 return out
def parse(text,stderr,rc,v,d):
 assert rc==0 and stderr=='' and not re.search(r'\b(TRAP|FAULT)\b',text)
 imports=[];used={};exports={};inits=[];cmd=[]
 for line in text.splitlines():
  if line.startswith('init '):assert re.fullmatch(r'init 0x[0-9a-f]+',line);inits.append(line)
  elif line.startswith('import '):
   m=re.fullmatch(r'import (linux|data|trap) (\S+) slots=(\d+)',line);assert m;imports.append({'kind':m[1],'symbol':m[2],'slots':int(m[3])})
  elif line.startswith('used '):
   m=re.fullmatch(r'used (\S+) (\d+)',line);assert m and m[1] not in used and int(m[2])>0;used[m[1]]=int(m[2])
  elif line.startswith('export '):
   m=re.fullmatch(r'export (\S+) (0x[0-9a-f]+)',line);assert m and m[1] not in exports;exports[m[1]]=m[2]
  else:cmd.append(line)
 assert len(imports)==133 and len({x['symbol'] for x in imports})==133
 assert set(used)<={x['symbol'] for x in imports if x['kind']=='linux'}
 assert set(exports)=={'_CreateInstanceU','_DestroyInstanceU','_SetSampleRateU','_GetPlugInfoU','_CalcA','_SetParameterA','_ResetA'}
 assert not inits
 assert cmd[:2]==['slice offset=16384 size=267648','create ok']
 m=re.fullmatch(r'rate 44100 ret=(-?\d+)',cmd[2]);assert m;rate=int(m[1])
 for w,line in zip(d['words'],cmd[3:36]):
  m=re.fullmatch(r'param (\d+) (\S+)',line);assert m and int(m[1])==w['index'] and bits(m[2])==w['little_endian_hex']
 assert cmd[36:40]==[f'event 11264 0x90 60 {v}','event 33314 0x80 60 0','inflag 0','input zero']
 groups=[]
 for line,nframes,nblocks in [(cmd[40],11264,22),(cmd[41],44100,87)]:
  m=re.fullmatch(r'process '+str(nframes)+r' 512 flags:((?: \d+x\(ret=-?\d+,flag=-?\d+\))+ blocks='+str(nblocks)+')',line);assert m
  g=[list(map(int,x)) for x in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)',line)]
  assert sum(x[0] for x in g)==nblocks and all(x[1]==0 and x[2] in (0,1) for x in g);groups.append({'frames':nframes,'groups':g})
 assert cmd[42:]==['destroy','cxx-failbits 0']
 assert exports=={'_CreateInstanceU':'0xc030','_DestroyInstanceU':'0xc0b0','_SetSampleRateU':'0xc120','_GetPlugInfoU':'0xc190','_CalcA':'0xc240','_SetParameterA':'0xc550','_ResetA':'0xc5d0'}
 return {'imports':imports,'used':used,'exports':exports,'initializers':inits,'commands':cmd,'Rate_return_opaque_integer':rate,'Rate_semantics':None,'CalcA_groups':groups,'direct_export_calls':145,'CalcA':109,'nested_initialization_calls':'not bounded or counted as direct exports'}
def audio(p):
 raw=pathlib.Path(p).read_bytes();assert len(raw)==442912
 finite=True;nonzero=[0,0];negzero=[0,0];same=True;warmzero=True
 for i in range(55364):
  l,r=struct.unpack_from('<ff',raw,8*i);finite &= math.isfinite(l) and math.isfinite(r);same &= raw[8*i:8*i+4]==raw[8*i+4:8*i+8]
  if i<11264:warmzero &= l==0 and r==0
  else:
   for c,v in enumerate((l,r)):
    nonzero[c]+=int(v!=0);negzero[c]+=int(raw[8*i+4*c:8*i+4*c+4]==b'\0\0\0\x80')
 return {'bytes':len(raw),'sha256':sha(raw),'warmup_bytes':90112,'render_bytes':352800,'render_sha256':sha(raw[90112:]),'warmup_frames':11264,'render_frames':44100,'channels':2,'all_finite':finite,'channels_bit_identical':same,'warmup_numeric_zero':warmzero,'render_nonzero_samples':nonzero,'render_negative_zero_samples':negzero,'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None}
def custody(ctx):
 rows=ctx['watched_roles']+json.loads((H/'pre-call-manifest.json').read_text())['frozen_files'];out=[]
 for item in rows:
  x=item.get('identity',item);got=ident(x['path'],x.get('offset'),x['bytes'] if 'offset' in x else None);assert got==x,x['path'];out.append(got)
 return out
def limits():
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));resource.setrlimit(resource.RLIMIT_CPU,(20,20));resource.setrlimit(resource.RLIMIT_FSIZE,(4194304,4194304))
def run(d,prehash):
 assert sha((H/'pre-call-manifest.json').read_bytes())==prehash
 ctx=json.loads((H/'context.json').read_text());(H/'attempts').mkdir(exist_ok=False)
 a={'status':'RUNNING','utc_start':now(),'outer_pid':os.getpid(),'argv':sys.argv,'children':[],'error':None,'phases':{'inputs_validated':True,'custody_before':False,'calls_started':False,'all_children_completed':False,'custody_after':False}};save(H/'results.json',a)
 def stop(sig,frame):raise RuntimeError('outer signal '+str(sig))
 signal.signal(signal.SIGTERM,stop)
 try:
  a['custody_before']=custody(ctx);a['phases']['custody_before']=True
  for plan in d['plans']:
   v=plan['velocity_byte'];folder=H/'attempts'/f'velocity-{v:03}';folder.mkdir();output=folder/'output.f32';argv=[ctx['exe'],ctx['bundle'],plan['script'],str(output),'--imports'];c={'velocity_byte':v,'argv':argv,'utc_start':now(),'pid':None,'exit':None,'timeout':False,'cleanup':None,'status':'PREPARED'};a['children'].append(c);save(H/'results.json',a);proc=None;start=time.monotonic()
   try:
    with (folder/'stdout.txt').open('xb') as out,(folder/'stderr.txt').open('xb') as err:
     proc=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,cwd=H,env=ctx['environment'],preexec_fn=limits,start_new_session=True);c.update(pid=proc.pid,status='RUNNING');a['phases']['calls_started']=True;save(H/'results.json',a)
     try:c['exit']=proc.wait(timeout=20)
     except subprocess.TimeoutExpired:c['timeout']=True;os.killpg(proc.pid,signal.SIGKILL);c['exit']=proc.wait(timeout=5);c['cleanup']='group killed/direct child reaped'
   finally:
    if proc is not None and proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL);c['exit']=proc.wait(timeout=5);c['cleanup']='interrupted group killed/direct child reaped'
    c.update(utc_end=now(),elapsed_seconds=time.monotonic()-start)
    for key,path in [('stdout',folder/'stdout.txt'),('stderr',folder/'stderr.txt'),('audio',output)]:
     if path.exists():c[key]=ident(path)
    save(H/'results.json',a)
   assert not c['timeout'];c['parsed']=parse((folder/'stdout.txt').read_text(),(folder/'stderr.txt').read_text(),c['exit'],v,d);c['audio_summary']=audio(output);save(H/'results.json',a);assert c['audio_summary']['all_finite'] and c['audio_summary']['warmup_numeric_zero'],'nonfinite/nonzero warmup; stop later children'
   c['custody_after']=custody(ctx);assert c['custody_after']==a['custody_before'];c['status']='RECORDED';save(H/'results.json',a);print('velocity',v,'recorded',flush=True)
  a['phases']['all_children_completed']=True;a['custody_after']=a['children'][-1]['custody_after'];a['phases']['custody_after']=True;a['status']='COMPLETE-ONCE-NO-RETRY'
 except BaseException as e:
  a['status']='STOPPED-NO-RETRY';a['error']={'type':type(e).__name__,'message':str(e)}
  try:a['custody_after_failure']=custody(ctx)
  except BaseException as e2:a['custody_error']=str(e2)
  raise
 finally:a['utc_end']=now();save(H/'results.json',a)
if __name__=='__main__':
 d=json.loads((H/'inputs.json').read_text());validate(d);c=controls(d)
 if sys.argv[1:]==['--check-inputs']:print(json.dumps({'status':'PASS','negative_controls':c,'original_calls':0,'runtime_reads':0}))
 else:assert len(sys.argv)==3 and sys.argv[1]=='--run-once';run(d,sys.argv[2])
