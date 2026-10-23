#!/usr/bin/env python3
"""Fixed T11 CRC one-byte recorder; no build/import of old helpers or model changes."""
import copy,hashlib,json,os,pathlib,re,resource,signal,subprocess,sys,time
from datetime import datetime,timezone
H=pathlib.Path(__file__).resolve().parent
ENTRY='0x101191310';HEADER='loaded rebases=789951 binds-linux=103 binds-trap=42781 symbols=1882';OLD={0,183,255}
def now():return datetime.now(timezone.utc).isoformat()
def save(p,d):
 with pathlib.Path(p).open('w') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def identity(p):
 p=pathlib.Path(p).resolve();h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return {'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
def crc16(byte):
 c=byte<<8
 for _ in range(8):c=((c<<1)^0x8005 if c&0x8000 else c<<1)&0xffff
 return c

def validate(d):
 assert d['schema']=='whole-initial-zero-one-byte-crc-v1'
 assert d['counts']=={'logical':256,'inherited':3,'fresh_calls':253,'children':2,'calls_each':[127,126],'buffers_each':[254,252]}
 rows=d['rows'];assert [r['byte'] for r in rows]==list(range(256))
 for r in rows:
  b=r['byte'];assert r['id']==f'CRC-{b:02x}' and r['payload_hex']==f'{b:02x}' and r['input_sha256']==hashlib.sha256(bytes([b])).hexdigest()
  assert r['entry']==ENTRY and r['length']==1 and r['initial_seed_bytes_le']=='00000000' and r['expected_low16']==crc16(b) and r['portable_comparator'] is None and r['expected_full32'] is None and r['expected_low16_hex']==f'{crc16(b):04x}'
  assert r['provenance']==('inherited-summary' if b in OLD else 'fresh-selected') and (r['historical'] is not None)==(b in OLD)
  if b in OLD:assert r['historical']['crc16']==r['expected_low16'] and r['historical']['pid'] is None
 fresh=[r for r in rows if r['byte'] not in OLD];assert len(fresh)==253
 assert len(d['plans'])==2
 for i,p in enumerate(d['plans']):
  selected=fresh[:127] if i==0 else fresh[127:];assert p['child']==i and p['row_ids']==[r['id'] for r in selected]
  tokens=[]
  for j,r in enumerate(selected):tokens+=['call',ENTRY,'hex:'+r['payload_hex'],'i:1','buf:4','dump',f'b{2*j+1}','4']
  assert p['tokens']==tokens and p['calls']==len(selected) and p['buffers']==2*len(selected)<256

def input_controls(d):
 changes=[('missing-byte',lambda x:x['rows'].pop()),('duplicate-byte',lambda x:x['rows'][1].update(byte=0)),('nonzero-seed',lambda x:x['rows'][1].update(initial_seed_bytes_le='01000000')),('wrong-length',lambda x:x['rows'][1].update(length=2)),('wrong-input-hex',lambda x:x['rows'][1].update(payload_hex='02')),('different-entry',lambda x:x['rows'][1].update(entry='0x0')),('oracle-edit',lambda x:x['rows'][1].update(expected_low16=0)),('portable-promotion',lambda x:x['rows'][1].update(portable_comparator='exact')),('replay-old',lambda x:x['plans'][0]['row_ids'].append('CRC-00')),('buffer-cap-overrun',lambda x:x['plans'][0].update(buffers=256)),('seed-buffer-reuse',lambda x:x['plans'][0]['tokens'].__setitem__(12,'ref:b1')),('wrong-dump-pointer',lambda x:x['plans'][0]['tokens'].__setitem__(6,'b0')),('added-patch',lambda x:x['plans'][0]['tokens'].insert(0,'--patch')),('invented-old-pid',lambda x:x['rows'][0]['historical'].update(pid=123))]
 out=[]
 for label,mut in changes:
  x=copy.deepcopy(d);mut(x)
  try:validate(x)
  except (AssertionError,KeyError,IndexError):out.append(label)
  else:raise AssertionError('negative accepted '+label)
 return out

def parse_output(stdout,stderr,rc,p,byid):
 assert rc==0 and stderr=='';lines=stdout.splitlines();assert lines[0]==HEADER
 n=1;imports=[]
 while n<len(lines) and lines[n].startswith('import '):
  m=re.fullmatch(r'import (linux-data|linux|trap) (\S+) slots=(\d+)',lines[n]);assert m
  imports.append({'kind':m[1],'symbol':m[2],'slots':int(m[3])});n+=1
 assert len(imports)==1882 and len({r['symbol'] for r in imports})==1882 and sum(r['kind']=='linux-data' for r in imports)==1
 calls=[];addresses=set()
 for j,rid in enumerate(p['row_ids']):
  r=byid[rid];m=re.fullmatch(r'call (\d+) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)',lines[n]);n+=1
  assert m and int(m[1])==j and m[2]==ENTRY
  carriers={k:f'{int(v,16):016x}' for k,v in zip(('rax','rdx','xmm0','xmm1'),m.groups()[2:])};buffers=[]
  for k,size in ((2*j,1),(2*j+1,4)):
   m=re.fullmatch(r'out b(\d+) (0x[0-9a-f]+) ([0-9a-f]+)',lines[n]);n+=1
   assert m and int(m[1])==k and len(m[3])==size*2 and int(m[2],16)>0 and m[2] not in addresses;addresses.add(m[2])
   buffers.append({'index':k,'address':m[2],'bytes':size,'hex':m[3]})
  assert buffers[0]['hex']==r['payload_hex']
  m=re.fullmatch(r'dump b(\d+) (0x[0-9a-f]+) ([0-9a-f]{8})',lines[n]);n+=1
  assert m and int(m[1])==2*j+1 and m[2]==buffers[1]['address'] and m[3]==buffers[1]['hex']
  word=int.from_bytes(bytes.fromhex(m[3]),'little');calls.append({'row_id':rid,'call_index':j,'entry':ENTRY,'carriers64':carriers,'buffers_after':buffers,'dump':{'expression':f'b{2*j+1}','address':m[2],'hex':m[3]},'result_u32_le':word,'semantic_low16':word&0xffff,'upper16_observed':word>>16,'expected_low16':r['expected_low16'],'agrees':(word&0xffff)==r['expected_low16']})
 # Target's retained isolated route had no counted imports. Reject any additional line/use/trap/patch.
 assert n==len(lines) and len(calls)==p['calls']
 assert all(c['agrees'] for c in calls),'CRC oracle disagreement; preserve all attempted and stop later children'
 return {'imports':imports,'used_imports':{},'calls':calls}

def custody(ctx):
 f=json.loads((H/'manifest-before.json').read_text());out=[]
 for pin in ctx['watched']+f['frozen_files']:
  got=identity(pin['path']);assert got==pin,pin['path'];out.append(got)
 return out

def limits():
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));resource.setrlimit(resource.RLIMIT_CPU,(20,20));resource.setrlimit(resource.RLIMIT_FSIZE,(4194304,4194304))

def main():
 d=json.loads((H/'inputs.json').read_text());validate(d);controls=input_controls(d)
 if sys.argv[1:]==['--check-inputs']:print(json.dumps({'status':'PASS','input_controls':controls,'original_calls':0,'runtime_reads':0}));return
 assert sys.argv[1:]==['--run-once'];ctx=json.loads((H/'context.json').read_text());freeze=json.loads((H/'manifest-before.json').read_text())
 for pin in freeze['frozen_files']:assert identity(pin['path'])==pin
 (H/'attempts').mkdir(exist_ok=False)
 result={'schema':'crc-one-byte-actual-v1','status':'RUNNING','utc_start':now(),'outer_pid':os.getpid(),'outer_argv':sys.argv,'input_controls':controls,'children':[],'error':None,'phases':{'validated':True,'custody_before':False,'calls_started':False,'all_children_completed':False,'custody_after':False}}
 save(H/'results.json',result)
 def terminated(signum,frame):raise RuntimeError('outer signal '+str(signum))
 signal.signal(signal.SIGTERM,terminated)
 try:
  result['custody_before']=custody(ctx);result['phases']['custody_before']=True;byid={r['id']:r for r in d['rows']}
  for p in d['plans']:
   directory=H/'attempts'/f'child-{p["child"]}';directory.mkdir();argv=[ctx['loader'],ctx['image'],'--imports']+p['tokens'];start=time.monotonic()
   c={'child':p['child'],'argv':argv,'utc_start':now(),'pid':None,'exit':None,'timeout':False,'cleanup':None,'status':'PREPARED'};result['children'].append(c);save(H/'results.json',result);proc=None
   try:
    with (directory/'stdout.txt').open('xb') as out,(directory/'stderr.txt').open('xb') as err:
     proc=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,cwd=H,env=ctx['environment'],preexec_fn=limits,start_new_session=True);c['pid']=proc.pid;c['status']='RUNNING';result['phases']['calls_started']=True;save(H/'results.json',result)
     try:c['exit']=proc.wait(timeout=20)
     except subprocess.TimeoutExpired:c['timeout']=True;os.killpg(proc.pid,signal.SIGKILL);c['exit']=proc.wait(timeout=5);c['cleanup']='selected process group killed; direct child reaped'
   finally:
    if proc is not None and proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL);c['exit']=proc.wait(timeout=5);c['cleanup']='interrupted wait group killed/direct child reaped'
    c.update(utc_end=now(),elapsed_seconds=time.monotonic()-start)
    for name in ('stdout','stderr'):
     f=directory/(name+'.txt')
     if f.exists():c[name]=identity(f)
    save(H/'results.json',result)
   assert not c['timeout'];c['parsed']=parse_output((directory/'stdout.txt').read_text(),(directory/'stderr.txt').read_text(),c['exit'],p,byid);c['status']='RECORDED';save(H/'results.json',result)
   c['custody_after']=custody(ctx);assert c['custody_after']==result['custody_before'];save(H/'results.json',result);print(f'child {p["child"]}: {p["calls"]} CRC returns, no counted imports',flush=True)
  result['phases']['all_children_completed']=True;result['custody_after']=result['children'][-1]['custody_after'];result['phases']['custody_after']=True;result['status']='COMPLETE-ONE-ATTEMPT-PER-CHILD'
 except BaseException as e:
  result['status']='STOPPED-NO-RETRY';result['error']={'type':type(e).__name__,'message':str(e)}
  try:result['custody_after_failure']=custody(ctx)
  except BaseException as e2:result['custody_after_failure_error']=str(e2)
  raise
 finally:result['utc_end']=now();save(H/'results.json',result)
if __name__=='__main__':main()
