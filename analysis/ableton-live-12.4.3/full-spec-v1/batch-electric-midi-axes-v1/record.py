#!/usr/bin/env python3
"""Fixed142-child recording; existing unmodified Electric xdev, no old module imports."""
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
def eventpair(axis,value):
 assert axis in['matching-channel','note-off-velocity','baseline']
 if axis=='matching-channel':assert 0<=value<16;return [[11264,144+value,60,100],[33314,128+value,60,0]]
 if axis=='note-off-velocity':assert 0<=value<128;return [[11264,144,60,100],[33314,128,60,value]]
 assert value==0;return [[11264,144,60,100],[33314,128,60,0]]
def wholehistory(d,events):
 return {'parameter_f32_bits_le':[w['little_endian_hex']for w in d['words']],'parameter_reconstructed_binary64_le':[w['reconstructed_binary64_le']for w in d['words']],'events':events,'sample_rate':44100,'process_frames':[11264,44100],'block':512,'input':'zero','inflag':0,'transport':[0,0,120],'XDEV_TIME':'0 existing treatment','MXCSR':'0x1f80','LIBM_ULP':'absent/unperturbed'}
def historykey(d,events):return sha(json.dumps(wholehistory(d,events),sort_keys=True,separators=(',',':')).encode())
def script(d,p):
 events=eventpair(p['axis'],p['value'])
 return '\n'.join(['create','rate 44100']+[f'param {w["index"]} {w["token"]}'for w in d['words']]+[f'event {f} {s:#x} {k} {v}'for f,s,k,v in events]+['inflag 0','input zero','process 11264 512','process 44100 512','destroy'])+'\n'
def validate(d):
 assert d['schema']=='whole-Electric-P1-matching-channel-and-offvelocity-v1'
 assert len(d['words'])==33 and [w['index']for w in d['words']]==list(range(33))
 assert all(bits(w['token'])==w['little_endian_hex']and struct.pack('<d',float(w['token'])).hex()==w['reconstructed_binary64_le']for w in d['words'])
 assert sha(bytes.fromhex(''.join(w['little_endian_hex']for w in d['words'])))=='9ef2b39d47ca833730a9bbfd9d26e3bdc08a847df0ead035bd14d948bc35a43a'
 pairs=[('matching-channel',v)for v in range(16)]+[('note-off-velocity',v)for v in range(128)]
 assert[(a['axis'],a['value'])for a in d['aliases']]==pairs and len(d['histories'])==143 and len({z['history_sha256']for z in d['histories']})==143
 byhash={z['history_sha256']:z for z in d['histories']}
 for a in d['aliases']:
  ev=eventpair(a['axis'],a['value']);key=historykey(d,ev);assert a['history_sha256']==key;z=byhash[key];assert z['events']==ev and z['whole_history']==wholehistory(d,ev)
  assert z['packed16_events_le']==[struct.pack('<qBBBB4x',*e,0).hex()for e in ev]
 assert d['aliases'][0]['history_sha256']==d['aliases'][16]['history_sha256']
 assert len({tuple(z['whole_history']['parameter_f32_bits_le'])for z in d['histories']})==1
 old=0
 for z in d['histories']:
  assert all(z[k]is None for k in['expected_waveform','portable_expected','portable_comparator','grade'])
  assert(z['historical']is not None)==(z['axis']=='baseline')
  assert z['events']==eventpair(z['axis'],z['value'])and historykey(d,z['events'])==z['history_sha256']
  if z['historical']is not None:old+=1;assert z['historical']['new_pid']is z['historical']['new_receipt']is None
 assert old==1 and len(d['plans'])==142
 expected=[('matching-channel',v)for v in range(1,16)]+[('note-off-velocity',v)for v in range(1,128)]
 assert[(p['axis'],p['value'])for p in d['plans']]==expected
 for p in d['plans']:
  assert p['id']==('channel-'+f"{p['value']:02}"if p['axis']=='matching-channel'else'offvel-'+f"{p['value']:03}")
  assert p['history_sha256']==historykey(d,eventpair(p['axis'],p['value']))
  assert p['script']==str(H/'scripts'/(p['id']+'.script'))and pathlib.Path(p['script']).read_text()==script(d,p)
 assert d['counts']=={'alias_points':144,'unique_histories':143,'inherited_histories':1,'fresh_children':142,'direct_exports':20590,'CalcA':15478,'stereo_bytes':62893504}
 assert d['fixture']=={'sample_rate':44100,'frames':44100,'block':512,'last_block':68,'warmup':11264,'key':60,'on_frame':11264,'off_frame':33314,'on_velocity':100,'baseline_off_velocity':0,'input':'zero','inflag':0,'transport':[0,0,120],'MXCSR':'0x1f80','XDEV_TIME':'0 existing treatment','LIBM_ULP':'absent/unperturbed'}
def controls(d):
 tests=[('omit-channel15',lambda x:x['aliases'].pop(15)),('omit-off127',lambda x:x['aliases'].pop()),('duplicate-axispoint',lambda x:x['aliases'].__setitem__(1,x['aliases'][2])),('drop-history',lambda x:x['histories'].pop()),('parameter-only-dedup',lambda x:x.update(histories=x['histories'][:1])),('collapse-all-channel-histories',lambda x:x['aliases'][1].update(history_sha256=x['aliases'][0]['history_sha256'])),('collapse-off127',lambda x:x['aliases'][-1].update(history_sha256=x['aliases'][0]['history_sha256'])),('replay-baseline',lambda x:x['plans'][0].update(value=0)),('omit-fresh',lambda x:x['plans'].pop()),('wrong-parameter',lambda x:x['words'][0].update(token='29.0')),('wrong-f64',lambda x:x['words'][0].update(reconstructed_binary64_le='00'*8)),('unmatched-channel',lambda x:x['histories'][1]['events'][1].__setitem__(1,128)),('release-crossproduct',lambda x:x['histories'][1]['events'][1].__setitem__(3,127)),('wrong-offkey',lambda x:x['histories'][1]['events'][1].__setitem__(2,61)),('wrong-history-frame',lambda x:x['histories'][1]['events'][0].__setitem__(0,0)),('bad-event-word',lambda x:x['histories'][1]['packed16_events_le'].__setitem__(0,'00'*16)),('wrong-process-history',lambda x:x['histories'][1]['whole_history'].update(process_frames=[44100])),('invent-oldPID',lambda x:x['histories'][0]['historical'].update(new_pid=1)),('drop-old-reference',lambda x:x['histories'][0].update(historical=None)),('new-waveform-fit',lambda x:x['histories'][1].update(expected_waveform='fit')),('portable-expected',lambda x:x['histories'][1].update(portable_expected='audio')),('portable-comparator',lambda x:x['histories'][1].update(portable_comparator='exact')),('grade',lambda x:x['histories'][1].update(grade='PASS')),('count',lambda x:x['counts'].update(fresh_children=141)),('warmup',lambda x:x['fixture'].update(warmup=0)),('clock',lambda x:x['fixture'].update(XDEV_TIME='1'))];out=[]
 for name,mut in tests:
  x=copy.deepcopy(d);mut(x)
  try:validate(x)
  except(AssertionError,KeyError,IndexError):out.append(name)
  else:raise AssertionError('accepted '+name)
 return out
def parse(text,stderr,rc,plan,d):
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
 assert cmd[36:40]==[f'event {f} {s:#x} {k} {v}'for f,s,k,v in eventpair(plan['axis'],plan['value'])]+['inflag 0','input zero']
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
   case=plan['id'];folder=H/'attempts'/case;folder.mkdir();output=folder/'output.f32';argv=[ctx['exe'],ctx['bundle'],plan['script'],str(output),'--imports'];c={'id':case,'axis':plan['axis'],'value':plan['value'],'argv':argv,'utc_start':now(),'pid':None,'exit':None,'timeout':False,'cleanup':None,'status':'PREPARED'};a['children'].append(c);save(H/'results.json',a);proc=None;start=time.monotonic()
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
   assert not c['timeout'];c['parsed']=parse((folder/'stdout.txt').read_text(),(folder/'stderr.txt').read_text(),c['exit'],plan,d);c['audio_summary']=audio(output);save(H/'results.json',a);assert c['audio_summary']['all_finite'] and c['audio_summary']['warmup_numeric_zero'],'nonfinite/nonzero warmup; stop later children'
   c['custody_after']=custody(ctx);assert c['custody_after']==a['custody_before'];c['status']='RECORDED';save(H/'results.json',a);print('midi-axis',case,'recorded',flush=True)
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
