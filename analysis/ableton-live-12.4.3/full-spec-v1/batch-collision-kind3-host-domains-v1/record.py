#!/usr/bin/env python3
"""Fixed85-child recorder; unchanged Collision xdev/model; stdlib recording only."""
import copy,hashlib,json,math,os,pathlib,re,resource,signal,struct,subprocess,sys,time
from datetime import datetime,timezone
H=pathlib.Path(__file__).resolve().parent
COUNTS={'domains':20,'aliases':105,'unique_histories':86,'historical_input_only':1,'fresh_children':85,'direct_exports':21335,'CalcA':9265,'stereo_bytes':37647520}
DOMAINS=[(0,1,1),(11,1,0),(15,3,0),(25,1,1),(26,6,0),(27,3,2),(58,1,0),(59,5,0),(60,3,2),(91,1,0),(92,1,0),(93,6,0),(94,1,1),(95,1,0),(97,21,4),(106,1,0),(107,6,0),(108,1,1),(109,1,0),(111,21,4)]
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):
 with pathlib.Path(p).open('w')as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def ident(p,offset=None,size=None):
 p=pathlib.Path(p);h=hashlib.sha256();n=0
 with p.open('rb')as f:
  if offset is not None:f.seek(offset)
  while True:
   b=f.read(min(1048576,size-n)if size is not None else 1048576)
   if not b:break
   h.update(b);n+=len(b)
   if size is not None and n==size:break
 assert size is None or n==size
 d={'path':str(p),'bytes':n,'sha256':h.hexdigest()}
 if offset is not None:d['offset']=offset
 return d

def variant(d,p):
 w=copy.deepcopy(d['baseline_words']);i=p['index'];v=p['value'];w[i].update(token=f'{v}.0',f32_le=struct.pack('<f',v).hex(),reconstructed_f64_le=struct.pack('<d',v).hex());return w

def script(d,p):
 i=p['index'];return d['baseline_script_utf8'].replace(f'param {i} {d["baseline_words"][i]["token"]}\n',f'param {i} {p["value"]}.0\n',1)
def validate(d):
 assert d['schema']=='Collision-native-nonvirtual-kind3-preset-c4-v1'and d['counts']==COUNTS
 w=d['baseline_words'];assert len(w)==139 and[x['index']for x in w]==list(range(139))
 assert all(struct.pack('<f',float(x['token'])).hex()==x['f32_le']and struct.pack('<d',float(x['token'])).hex()==x['reconstructed_f64_le']for x in w)
 baseline=sha(bytes.fromhex(''.join(x['f32_le']for x in w)));assert baseline=='1a61d31521973c8eaa9167ca184704b787cda790d43db0c82a459d28caf0d0bc'
 assert[(x['index'],int(x['native_max']),x['baseline'])for x in d['domains']]==DOMAINS and all(x['native_virtual']is False and x['native_min']==0 for x in d['domains'])
 assert d['excluded_virtual_kind3_indices']==[102,104,116,118,121,123,125,127,129,135,137]
 expected=[(i,v)for i,m,b in DOMAINS for v in range(m+1)];assert[(a['index'],a['value'])for a in d['aliases']]==expected
 assert len(d['histories'])==86 and len({x['vector_sha256']for x in d['histories']})==86 and len({x['history_sha256']for x in d['histories']})==86
 byhash={x['vector_sha256']:x for x in d['histories']};seen=set();bases=0
 for a in d['aliases']:
  i,v=a['index'],a['value'];p={'index':i,'value':v};vw=variant(d,p);key=sha(bytes.fromhex(''.join(x['f32_le']for x in vw)));assert a['vector_sha256']==key;z=byhash[key];seen.add(key)
  isbase=key==baseline;assert a['shared_baseline']==isbase and a['id']==z['id']and a['history_sha256']==z['history_sha256'];bases+=isbase
  hh={**d['fixed_history'],'parameter_vector_sha256':key,'parameter_tokens':[x['token']for x in vw],'parameter_f32_le':[x['f32_le']for x in vw],'parameter_reconstructed_f64_le':[x['reconstructed_f64_le']for x in vw]}
  assert z['whole_history']==hh and z['history_sha256']==sha(json.dumps(hh,sort_keys=True,separators=(',',':')).encode())
  assert all(z[k]is None for k in ['expected_waveform','portable_expected','portable_comparator','grade'])
  if isbase:assert z['changed_index']is None and z['historical_input']['approved_actual']is None and z['historical_input']['new_pid']is z['historical_input']['new_receipt']is z['historical_input']['new_metrics']is None and z['provenance']=='historical-retained-input-only-NOT-approved-actual'
  else:assert z['changed_index']==i and z['value']==v and z['historical_input']is None and z['provenance']=='fresh-selected-once'
 assert bases==20 and len(seen)==86
 cmds=['create','rate 44100']+[f'param {x["index"]} {x["token"]}'for x in w]+['inflag 0','input zero','process 11264 512','event 4096 0x90 60 100','event 26146 0x80 60 0','inflag 0','input zero','process 44100 512','destroy']
 assert d['baseline_script_utf8']=='\n'.join(cmds)+'\n'and sha(d['baseline_script_utf8'].encode())=='3b17f74d5f2b6500635628d48db81decdf5bf28ec1f5b18ba63bc3ab2a0e383b'
 assert d['fixed_history']=={'rate':44100,'warmup_before_event_queue':11264,'render_frames':44100,'block':512,'last_render_block':68,'events':[[4096,144,60,100],[26146,128,60,0]],'input':'zero','inflag':0,'transport':[0,0,120],'XDEV_TIME':'0','MXCSR':'0x1f80 source policy; no register trace','LIBM_ULP':'absent/unperturbed','process_commands':['create','rate 44100','inflag 0','input zero','process 11264 512','event 4096 0x90 60 100','event 26146 0x80 60 0','inflag 0','input zero','process 44100 512','destroy']}
 assert len(d['plans'])==85 and[(p['index'],p['value'])for p in d['plans']]==[(i,v)for i,m,b in DOMAINS for v in range(m+1)if v!=b]
 for p in d['plans']:
  assert p['id']==f'i{p["index"]:03d}-v{p["value"]:02d}'and p['script']==str(H/'scripts'/(p['id']+'.script'))
  z=byhash[p['vector_sha256']];assert z['id']==p['id']and z['history_sha256']==p['history_sha256']
  text=script(d,p);assert pathlib.Path(p['script']).read_text()==text and sha(text.encode())==z['script_sha256']and len(text.encode())==z['script_bytes']
  assert p['direct_exports']==251 and p['CalcA']==109 and p['stereo_bytes']==442912

def controls(d):
 tests=[('omit-domain',lambda x:x['domains'].pop()),('extend-native59-to6',lambda x:x['domains'][7].update(native_max=6)),('res1wrongmax5',lambda x:x['domains'][4].update(native_max=5)),('include-virtual',lambda x:x['domains'][0].update(native_virtual=True)),('wrong-baseline-legalinteger',lambda x:x['domains'][0].update(baseline=.5)),('omit-alias',lambda x:x['aliases'].pop()),('duplicate-alias',lambda x:x['aliases'].__setitem__(1,x['aliases'][2])),('omit-vector',lambda x:x['histories'].pop()),('parameter-only-wronghistory',lambda x:x['histories'][0]['whole_history'].update(events=[[4097,144,60,100]])),('wrong-word',lambda x:x['baseline_words'][1].update(token='1.0')),('wrong-f64',lambda x:x['baseline_words'][1].update(reconstructed_f64_le='00'*8)),('replay-baseline',lambda x:x['plans'][0].update(value=1)),('omit-fresh',lambda x:x['plans'].pop()),('crossproduct',lambda x:x['histories'][0]['whole_history']['parameter_tokens'].__setitem__(11,'1.0')),('invent-baseline-approval',lambda x:x['histories'][1]['historical_input'].update(approved_actual='approved')),('invent-baseline-PID',lambda x:x['histories'][1]['historical_input'].update(new_pid=1)),('invent-baseline-metric',lambda x:x['histories'][1]['historical_input'].update(new_metrics=1)),('new-waveform-fit',lambda x:x['histories'][0].update(expected_waveform='fit')),('portable-comparator',lambda x:x['histories'][0].update(portable_comparator='exact')),('portable-expected',lambda x:x['histories'][0].update(portable_expected='audio')),('grade',lambda x:x['histories'][0].update(grade='PASS')),('warmup-order',lambda x:x['fixed_history'].update(warmup_before_event_queue=0)),('wrong-off-event',lambda x:x['fixed_history']['events'][1].__setitem__(0,7168)),('clock',lambda x:x['fixed_history'].update(XDEV_TIME='1')),('count',lambda x:x['counts'].update(fresh_children=84))];out=[]
 for name,mut in tests:
  x=copy.deepcopy(d);mut(x)
  try:validate(x)
  except(AssertionError,IndexError,KeyError):out.append(name)
  else:raise AssertionError('accepted '+name)
 return out

def parse(text,stderr,rc,plan,d):
 assert rc==0 and stderr==''and not re.search(r'\b(TRAP|FAULT)\b',text)
 imports=[];used={};exports={};inits=[];cmd=[]
 for line in text.splitlines():
  if line.startswith('init '):assert re.fullmatch(r'init 0x[0-9a-f]+',line);inits.append(line)
  elif line.startswith('import '):
   m=re.fullmatch(r'import (linux|data|trap) (\S+) slots=(\d+)',line);assert m;imports.append({'kind':m[1],'symbol':m[2],'slots':int(m[3])})
  elif line.startswith('used '):
   m=re.fullmatch(r'used (\S+) (\d+)',line);assert m and m[1]not in used and int(m[2])>0;used[m[1]]=int(m[2])
  elif line.startswith('export '):
   m=re.fullmatch(r'export (\S+) (0x[0-9a-f]+)',line);assert m and m[1]not in exports;exports[m[1]]=m[2]
  else:cmd.append(line)
 assert len(imports)==129 and len({x['symbol']for x in imports})==129 and {k:sum(x['kind']==k for x in imports)for k in ['linux','data','trap']}=={'linux':96,'data':7,'trap':26}
 assert used and set(used)<={x['symbol']for x in imports if x['kind']=='linux'}and len(inits)<=128
 assert set(exports)=={'_CreateInstanceU','_DestroyInstanceU','_SetSampleRateU','_GetPlugInfoU','_CalcA','_SetParameterA','_ResetA'}and len(set(exports.values()))==7
 assert cmd[:2]==['slice offset=16384 size=367488','create ok'];m=re.fullmatch(r'rate 44100 ret=(-?\d+)',cmd[2]);assert m;rate=int(m[1]);words=variant(d,plan)
 for w,line in zip(words,cmd[3:142]):
  m=re.fullmatch(r'param (\d+) (\S+)',line);assert m and int(m[1])==w['index']and struct.pack('<f',float(m[2])).hex()==w['f32_le']
 assert len(cmd)==152 and cmd[142:144]==['inflag 0','input zero']and cmd[145:149]==['event 4096 0x90 60 100','event 26146 0x80 60 0','inflag 0','input zero']and cmd[150:]==['destroy','cxx-failbits 0']
 groups=[]
 for line,nframes,nblocks in[(cmd[144],11264,22),(cmd[149],44100,87)]:
  m=re.fullmatch(r'process '+str(nframes)+r' 512 flags:((?: \d+x\(ret=-?\d+,flag=-?\d+\))+ blocks='+str(nblocks)+')',line);assert m
  g=[list(map(int,x))for x in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)',line)];assert sum(x[0]for x in g)==nblocks and all(x[0]>0 and x[1]==0 and x[2]in(0,1)for x in g);groups.append({'frames':nframes,'groups':g})
 return {'imports':imports,'used':used,'exports':exports,'initializers':inits,'commands':cmd,'Rate_return_opaque_integer':rate,'Rate_semantics':None,'CalcA_groups':groups,'direct_export_calls':251,'CalcA':109,'nested_initialization_calls':'unknown/not bounded by directexports'}

def audio(p):
 raw=pathlib.Path(p).read_bytes();assert len(raw)==442912
 finite=True;same=True;nonzero=[0,0];negativezero=[0,0];warmzero=True
 for i in range(55364):
  l,r=struct.unpack_from('<ff',raw,8*i);finite &= math.isfinite(l)and math.isfinite(r);same &= raw[8*i:8*i+4]==raw[8*i+4:8*i+8]
  if i<11264:warmzero &= l==0 and r==0
  else:
   for c,v in enumerate((l,r)):nonzero[c]+=int(v!=0);negativezero[c]+=int(raw[8*i+4*c:8*i+4*c+4]==b'\0\0\0\x80')
 return {'bytes':len(raw),'sha256':sha(raw),'warmup_bytes':90112,'render_bytes':352800,'render_sha256':sha(raw[90112:]),'warmup_frames':11264,'render_frames':44100,'all_finite':finite,'channels_bit_identical':same,'warmup_numeric_zero':warmzero,'render_nonzero_samples':nonzero,'render_negative_zero_samples':negativezero,'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None}
def custody(ctx):
 rows=ctx['watched_roles']+json.loads((H/'pre-call-manifest.json').read_text())['frozen_files'];out=[]
 for item in rows:
  x=item.get('identity',item);got=ident(x['path'],x.get('offset'),x['bytes']if 'offset'in x else None);assert got==x,x['path'];out.append(got)
 return out
def limits():resource.setrlimit(resource.RLIMIT_CORE,(0,0));resource.setrlimit(resource.RLIMIT_CPU,(20,20));resource.setrlimit(resource.RLIMIT_FSIZE,(4194304,4194304))
def run(d,prehash):
 assert sha((H/'pre-call-manifest.json').read_bytes())==prehash;ctx=json.loads((H/'context.json').read_text());assert ctx['environment']=={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','XDEV_TIME':'0'};(H/'attempts').mkdir(exist_ok=False)
 a={'status':'RUNNING','utc_start':now(),'outer_pid':os.getpid(),'argv':sys.argv,'python':sys.version,'host':list(os.uname()),'children':[],'error':None,'phases':{'inputs_validated':True,'custody_before':False,'calls_started':False,'all_children_completed':False,'custody_after':False}};save(H/'results.json',a)
 def stop(sig,frame):raise RuntimeError('outer signal '+str(sig))
 signal.signal(signal.SIGTERM,stop)
 try:
  a['custody_before']=custody(ctx);a['phases']['custody_before']=True
  for plan in d['plans']:
   case=plan['id'];folder=H/'attempts'/case;folder.mkdir();output=folder/'output.f32';argv=[ctx['exe'],ctx['bundle'],plan['script'],str(output),'--imports'];c={'id':case,'index':plan['index'],'value':plan['value'],'argv':argv,'utc_start':now(),'pid':None,'exit':None,'timeout':False,'cleanup':None,'status':'PREPARED'};a['children'].append(c);save(H/'results.json',a);proc=None;start=time.monotonic()
   try:
    with(folder/'stdout.txt').open('xb')as out,(folder/'stderr.txt').open('xb')as err:
     proc=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,cwd=H,env=ctx['environment'],preexec_fn=limits,start_new_session=True);c.update(pid=proc.pid,status='RUNNING');a['phases']['calls_started']=True;save(H/'results.json',a)
     try:c['exit']=proc.wait(timeout=20)
     except subprocess.TimeoutExpired:c['timeout']=True;os.killpg(proc.pid,signal.SIGKILL);c['exit']=proc.wait(timeout=5);c['cleanup']='group killed/direct child reaped'
   finally:
    if proc is not None and proc.poll()is None:os.killpg(proc.pid,signal.SIGKILL);c['exit']=proc.wait(timeout=5);c['cleanup']='interrupted group killed/direct child reaped'
    c.update(utc_end=now(),elapsed_seconds=time.monotonic()-start)
    for key,path in[('stdout',folder/'stdout.txt'),('stderr',folder/'stderr.txt'),('audio',output)]:
     if path.exists():c[key]=ident(path)
    save(H/'results.json',a)
   assert not c['timeout'];c['parsed']=parse((folder/'stdout.txt').read_text(),(folder/'stderr.txt').read_text(),c['exit'],plan,d);c['audio_summary']=audio(output);save(H/'results.json',a);assert c['audio_summary']['all_finite'],'nonfinite: preserve and stop later children'
   # Quiet/noisy/unequal/stereo/silent/dormant outcomes are discoveries, not guard failures.
   c['custody_after']=custody(ctx);assert c['custody_after']==a['custody_before'];c['status']='RECORDED';save(H/'results.json',a);print(case+' recorded',flush=True)
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
