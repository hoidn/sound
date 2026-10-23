#!/usr/bin/env python3
"""Fixed208-child recording; existing unmodified Analog xdev, no old module imports."""
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
def words(d,plan):
 i,v=plan['host_index'],plan['host_value']
 return [{**w,'token':str(v)+'.0','little_endian_hex':bits(v),'reconstructed_binary64_le':struct.pack('<d',float(v)).hex()} if w['index']==i else w for w in d['words']]
def script(d,plan):
 return '\n'.join(['create','rate 44100']+[f'param {w["index"]} {w["token"]}' for w in words(d,plan)]+['event 4400 0x90 60 100','event 35270 0x80 60 64','inflag 0','input zero','process 44100 512','destroy'])+'\n'
def validate(d):
 assert d['schema']=='whole-Analog-P1-all-native-kind3-domains-v1'
 assert len(d['words'])==203 and [w['index']for w in d['words']]==list(range(203))
 base=[w['little_endian_hex'] for w in d['words']]
 assert sha(bytes.fromhex(''.join(base)))=='18a94879168c2f73d621883d3a60b14de6f54a2b396fb8a0b11284c799926ed3'
 assert all(bits(w['token'])==w['little_endian_hex'] and struct.pack('<d',float(w['token'])).hex()==w['reconstructed_binary64_le'] for w in d['words'])
 assert base[99]=='0000803f' and len(d['domains'])==85 and sum(x['maximum']+1 for x in d['domains'])==338
 assert len({x['host_index']for x in d['domains']})==85
 pairs=[]
 for x in d['domains']:
  i=x['host_index'];assert 0<=i<203 and x['kind']=='kind3' and isinstance(x['maximum'],int) and x['maximum']>=0
  b=struct.unpack('<f',bytes.fromhex(base[i]))[0];assert b==int(b)==x['baseline'] and 0<=b<=x['maximum']
  pairs.extend((i,v)for v in range(x['maximum']+1))
 assert [(a['host_index'],a['host_value'])for a in d['aliases']]==pairs
 assert len(d['vectors'])==254 and len({x['vector_sha256']for x in d['vectors']})==254
 byhash={x['vector_sha256']:x for x in d['vectors']};hist={'baseline':0,'R3-mode':0,'Transpose-approved':0,'released-DAN029':0,'fresh-selected':0}
 for a in d['aliases']:
  ws=words(d,a);b=[w['little_endian_hex']for w in ws];key=sha(bytes.fromhex(''.join(b)));assert a['vector_sha256']==key
  z=byhash[key];assert z['parameter_bits_le']==b and z['parameter_binary64_le']==[w['reconstructed_binary64_le']for w in ws]
  assert z['events']==[[4400,144,60,100],[35270,128,60,64]] and z['packed16_events_le']==[struct.pack('<qBBBB4x',*e,0).hex()for e in z['events']]
 for z in d['vectors']:
  hist[z['provenance']]+=1
  assert all(z[k]is None for k in ['expected_waveform','portable_expected','portable_comparator','grade'])
  assert (z['historical']is None)==(z['provenance']=='fresh-selected')
  assert z['measurement_only_auxiliary']==(z['changed_host_index']==99 and z['changed_host_value']==0)
  if z['historical']is not None:assert z['historical']['new_pid']is None and z['historical']['new_receipt']is None
 assert hist=={'baseline':1,'R3-mode':20,'Transpose-approved':24,'released-DAN029':1,'fresh-selected':208}
 fresh=[z for z in d['vectors']if z['provenance']=='fresh-selected'];assert len(d['plans'])==208
 assert [(p['host_index'],p['host_value'])for p in d['plans']]==[(z['changed_host_index'],z['changed_host_value'])for z in fresh]
 for p,z in zip(d['plans'],fresh):
  assert p['id']==f"i{p['host_index']:03}-v{p['host_value']:02}" and p['vector_sha256']==z['vector_sha256']
  assert p['script']==str(H/'scripts'/(p['id']+'.script')) and pathlib.Path(p['script']).read_text()==script(d,p)
 assert d['counts']=={'alias_points':338,'unique_vectors':254,'inherited_unique_vectors':46,'fresh_children':208,'direct_exports':60944,'CalcA':18096,'stereo_bytes':73382400}
 assert d['fixture']=={'sample_rate':44100,'frames':44100,'block':512,'last_block':68,'warmup':0,'key':60,'on_frame':4400,'off_frame':35270,'on_velocity':100,'off_velocity':64,'input':'zero','inflag':0,'transport':[0,0,120],'MXCSR':'0x1f80','XDEV_TIME':'0 existing treatment','LIBM_ULP':'absent/unperturbed'}
def controls(d):
 tests=[('omit-domain',lambda x:x['domains'].pop()),('omit-alias',lambda x:x['aliases'].pop()),('duplicate-alias',lambda x:x['aliases'].__setitem__(0,x['aliases'][1])),('wrong-domain-max',lambda x:x['domains'][0].update(maximum=7)),('illegal-baseline',lambda x:x['domains'][0].update(baseline=1)),('missing-vector',lambda x:x['vectors'].pop()),('duplicate-vector',lambda x:x['vectors'].__setitem__(0,x['vectors'][1])),('drop-fresh',lambda x:x['plans'].pop()),('bad-fixed-word',lambda x:x['words'][99].update(token='0.0')),('wrong-index-order',lambda x:x['words'][1].update(index=0)),('wrong-f32',lambda x:x['vectors'][-1]['parameter_bits_le'].__setitem__(0,'00000000')),('wrong-f64',lambda x:x['vectors'][-1]['parameter_binary64_le'].__setitem__(0,'00'*8)),('bad-event',lambda x:x['vectors'][-1]['events'][1].__setitem__(3,0)),('bad-packed-event',lambda x:x['vectors'][-1]['packed16_events_le'].__setitem__(0,'00'*16)),('fit',lambda x:x['vectors'][-1].update(expected_waveform='fit')),('portable-expected',lambda x:x['vectors'][-1].update(portable_expected='audio')),('portable-comparator',lambda x:x['vectors'][-1].update(portable_comparator='exact')),('grade',lambda x:x['vectors'][-1].update(grade='PASS')),('invent-old-pid',lambda x:next(z for z in x['vectors']if z['historical'])['historical'].update(new_pid=123)),('hide-measurement-only',lambda x:next(z for z in x['vectors']if z['measurement_only_auxiliary']).update(measurement_only_auxiliary=False)),('drop-provenance',lambda x:next(z for z in x['vectors']if z['provenance']=='fresh-selected').update(provenance='R3-mode')),('wrong-callcount',lambda x:x['counts'].update(direct_exports=60943)),('wrong-script-pair',lambda x:x['plans'][0].update(host_value=99)),('history',lambda x:x['fixture'].update(off_frame=35271)),('seed',lambda x:x['fixture'].update(XDEV_TIME='1'))];out=[]
 for name,mut in tests:
  x=copy.deepcopy(d);mut(x)
  try:validate(x)
  except (AssertionError,KeyError,IndexError):out.append(name)
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
 assert len(imports)==132 and len({x['symbol'] for x in imports})==132
 assert set(used)<={x['symbol'] for x in imports if x['kind']=='linux'}
 assert set(exports)=={'_CreateInstanceU','_DestroyInstanceU','_SetSampleRateU','_GetPlugInfoU','_CalcA','_SetParameterA','_ResetA'}
 assert inits==['init 0x314d0']
 assert exports=={'_CreateInstanceU':'0x1fd70','_DestroyInstanceU':'0x1fdf0','_SetSampleRateU':'0x1fe60','_GetPlugInfoU':'0x1fed0','_CalcA':'0x1ff80','_SetParameterA':'0x20290','_ResetA':'0x20310'}
 assert cmd[:2]==['slice offset=16384 size=500880','create ok']
 m=re.fullmatch(r'rate 44100 ret=(-?\d+)',cmd[2]);assert m;rate=int(m[1])
 for w,line in zip(words(d,plan),cmd[3:206]):
  m=re.fullmatch(r'param (\d+) (\S+)',line);assert m and int(m[1])==w['index'] and bits(m[2])==w['little_endian_hex']
 assert cmd[206:210]==['event 4400 0x90 60 100','event 35270 0x80 60 64','inflag 0','input zero']
 m=re.fullmatch(r'process 44100 512 flags:((?: \d+x\(ret=-?\d+,flag=-?\d+\))+ blocks=87)',cmd[210]);assert m
 groups=[list(map(int,g)) for g in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)',cmd[210])]
 assert sum(g[0] for g in groups)==87 and all(g[1]==0 and g[2] in (0,1) for g in groups)
 assert cmd[211:]==['destroy','cxx-failbits 0']
 return {'imports':imports,'used':used,'exports':exports,'initializers':inits,'commands':cmd,'Rate_return_opaque_integer':rate,'Rate_semantics':None,'CalcA_groups':groups,'direct_export_calls':293,'CalcA':87,'nested_initialization_calls':'not bounded or counted as direct exports'}
def audio(p):
 raw=pathlib.Path(p).read_bytes();assert len(raw)==352800
 finite=True;nonzero=[0,0];negzero=[0,0];same=True
 for i in range(44100):
  l,r=struct.unpack_from('<ff',raw,8*i);finite &= math.isfinite(l) and math.isfinite(r);same &= raw[8*i:8*i+4]==raw[8*i+4:8*i+8]
  for c,v in enumerate((l,r)):
   nonzero[c]+=int(v!=0);negzero[c]+=int(raw[8*i+4*c:8*i+4*c+4]==b'\0\0\0\x80')
 return {'bytes':len(raw),'sha256':sha(raw),'frames':44100,'channels':2,'all_finite':finite,'channels_bit_identical':same,'nonzero_samples':nonzero,'negative_zero_samples':negzero,'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None}
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
   case=plan['id'];folder=H/'attempts'/case;folder.mkdir();output=folder/'output.f32';argv=[ctx['exe'],ctx['bundle'],plan['script'],str(output),'--imports'];c={'id':case,'host_index':plan['host_index'],'host_value':plan['host_value'],'argv':argv,'utc_start':now(),'pid':None,'exit':None,'timeout':False,'cleanup':None,'status':'PREPARED'};a['children'].append(c);save(H/'results.json',a);proc=None;start=time.monotonic()
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
   assert not c['timeout'];c['parsed']=parse((folder/'stdout.txt').read_text(),(folder/'stderr.txt').read_text(),c['exit'],plan,d);c['audio_summary']=audio(output);save(H/'results.json',a);assert c['audio_summary']['all_finite'],'nonfinite; stop later children'
   c['custody_after']=custody(ctx);assert c['custody_after']==a['custody_before'];c['status']='RECORDED';save(H/'results.json',a);print('kind3',case,'recorded',flush=True)
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
