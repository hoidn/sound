"""PREPARATION ONLY: one separately selected child, two fixed original call sites."""
from pathlib import Path
import datetime,hashlib,json,os,re,resource,signal,subprocess,sys
ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
PRE=BASE/'depth-utility-xexec-mute-zero-preparation'
DEST=BASE/'depth-utility-xexec-mute-zero'
BIN=BASE/'depth-utility-xexec-owned-build/xexec'
IMAGE=Path('/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64')
CODE=[('0x104b8c760',13,'554889e54088b7cf0000005dc3'),('0x104b8c7b0',16,'0f57c080bfcf000000000f8577030000'),('0x104b8cb37',1,'c3')]
TOKENS=['--imports','dump','0x104b8c760','13','dump','0x104b8c7b0','16','dump','0x104b8cb37','1','call','0x104b8c760','buf:208','i:1','dump','b0','208','call','0x104b8c7b0','ref:b0','hex:0000803f000000c0','d:0x1p+0','dump','b0','208']
ENV={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C'}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def save(name,value):
 with (DEST/name).open('x') as f:json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def raw(name,value):
 with (DEST/name).open('xb') as f:f.write(value);f.flush();os.fsync(f.fileno())
def no_core():resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def command():return [str(BIN),str(IMAGE),*TOKENS]
def parse_output(stdout,stderr):
 """Pure strict protocol parser; result/state comparisons remain observations."""
 if stderr:raise ValueError('Nonempty stderr; retain trap/fault/loader evidence')
 lines=stdout.splitlines();i=0
 def take(pattern):
  nonlocal i
  if i>=len(lines):raise ValueError('Truncated stdout')
  match=re.fullmatch(pattern,lines[i]);i+=1
  if match is None:raise ValueError('Unexpected protocol line: '+lines[i-1][:120])
  return match
 header=take(r'loaded rebases=(\d+) binds-linux=(\d+) binds-trap=(\d+) symbols=(\d+)')
 counts=list(map(int,header.groups()));imports={}
 while i<len(lines) and lines[i].startswith('import '):
  row=take(r'import (linux|linux-data|trap) (\S+) slots=([1-9]\d*)');kind,name,slots=row.groups()
  if name in imports:raise ValueError('Duplicate import symbol')
  imports[name]=dict(category=kind,slots=int(slots))
 if len(imports)!=counts[3] or len(imports)>8192:raise ValueError('Import count mismatch')
 if sum(r['slots'] for r in imports.values() if r['category']!='trap')!=counts[1] or sum(r['slots'] for r in imports.values() if r['category']=='trap')!=counts[2]:raise ValueError('Import slot totals mismatch')
 code=[]
 for expr,n,expected in CODE:
  row=take(r'dump (\S+) (0x[0-9a-f]+) ([0-9a-f]+)');e,a,h=row.groups()
  if e!=expr or int(a,16)!=int(expr,16) or len(h)!=2*n:raise ValueError('Mapped code dump geometry mismatch')
  code.append(dict(address=expr,bytes=n,hex=h,matches_retained=h==expected))
 calls=[]
 def call(index,address):
  row=take(r'call ([01]) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)')
  k,a,*registers=row.groups();v=list(map(lambda x:int(x,16),registers))
  if int(k)!=index or int(a,16)!=address or any(x>=1<<64 for x in v):raise ValueError('Call identity/register width mismatch')
  calls.append(dict(index=index,address=hex(address),rax=registers[0],rdx=registers[1],xmm0=registers[2],xmm1=registers[3]))
 def buffer(kind,label,n):
  row=take(kind+r' '+label+r' (0x[0-9a-f]+) ([0-9a-f]+)');a,h=row.groups();a=int(a,16)
  if a==0 or a%16 or a+n>1<<64 or len(h)!=2*n:raise ValueError('Owned buffer pointer/length mismatch')
  return a,h
 call(0,0x104b8c760);b0,out0=buffer('out','b0',208);d0,state0=buffer('dump','b0',208)
 call(1,0x104b8c7b0);b1,input1=buffer('out','b1',8);d1,state1=buffer('dump','b0',208)
 if b0!=d0 or b0!=d1 or out0!=state0:raise ValueError('State identity/duplicate snapshot mismatch')
 if not (b0+208<=b1 or b1+8<=b0):raise ValueError('Owned buffers overlap')
 used={}
 while i<len(lines):
  row=take(r'used (\S+) ([1-9]\d*)');name,n=row.groups()
  if name in used or name not in imports or imports[name]['category']!='linux':raise ValueError('Used import identity/category mismatch')
  used[name]=int(n)
 expected_state='00'*207+'01'
 return dict(loaded=dict(rebases=counts[0],linux_slots=counts[1],trap_slots=counts[2],symbols=counts[3]),imports=imports,used=used,code_dumps=code,code_matches=all(r['matches_retained'] for r in code),calls=calls,completed_original_call_rows=2,state_buffer_address=hex(b0),input_buffer_address=hex(b1),state_after_setter_hex=state0,state_after_helper_hex=state1,input_after_helper_hex=input1,observations=dict(setter_expected_state=state0==expected_state,helper_flag_nonzero_predicate_observed=state0[-2:]!='00',helper_state_unchanged=state1==state0,helper_input_unchanged=input1=='0000803f000000c0',helper_low64_xmm0_zero=int(calls[1]['xmm0'],16)==0),limits='Observations only; no zero-only validity filtering/criterion/public Mute law. Code comparisons are POSTHOC, not a pre-call stop barrier. Import categories/slot counts are resolver reports, not raw target addresses or exhaustive absence proof.')
def main():
 if sys.argv[1:]!=['--capture-root-selected-once'] or not sys.dont_write_bytecode:raise SystemExit('REFUSED: exact separate Root selection and python -B required')
 if DEST.exists() or DEST.is_symlink():raise FileExistsError(str(DEST))
 inputs=json.loads((PRE/'inputs.json').read_text());manifest=json.loads((PRE/'manifest.json').read_text())
 for row in inputs['pins']:
  if identity(Path(row['path']))!=row:raise ValueError('Pinned provider changed: '+row['path'])
 if {r['path'] for r in manifest['files']}!={p.name for p in PRE.iterdir() if p.is_file() and p.name!='manifest.json'}:raise ValueError('Preparation inventory changed')
 for row in manifest['files']:
  got=identity(PRE/row['path'])
  if (got['bytes'],got['sha256'])!=(row['bytes'],row['sha256']):raise ValueError('Preparation changed')
 argv=command();plan=json.loads((PRE/'plan.json').read_text())
 if argv!=plan['argv'] or plan['environment']!=ENV or plan['timeout_seconds']!=20:raise ValueError('Only exact fixed recipe selected')
 paths=sorted({Path(r['path']) for r in inputs['pins']}|{p for p in PRE.iterdir() if p.is_file()})
 before=[identity(p) for p in paths];DEST.mkdir();child=None;stdout=b'';stderr=b''
 result=dict(started_utc=utc(),attempts=0,returned_pid=None,exit=None,timeout=False,exception=None,automatic_retry=False,maximum_selected_top_level_original_calls=2,completed_original_call_rows=0,unobserved_original_execution='unknown until captured evidence',capture_complete=False)
 try:
  raw('capture-once.py',Path(__file__).read_bytes());save('before-map.json',before)
  save('invocation.json',dict(utc=utc(),argv=argv,cwd=str(DEST),environment=ENV,stdin='DEVNULL',core_limit=[0,0],start_new_session=True,timeout_seconds=20,posthoc_code_comparison=True))
  result['attempts']=1;save('attempt.json',dict(utc=utc(),attempt=1,argv=argv))
  child=subprocess.Popen(argv,cwd=DEST,env=ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=no_core,start_new_session=True)
  result['returned_pid']=child.pid;save('returned-pid.json',dict(utc=utc(),pid=child.pid))
  try:stdout,stderr=child.communicate(timeout=20)
  except subprocess.TimeoutExpired:
   result['timeout']=True;os.killpg(child.pid,signal.SIGKILL);stdout,stderr=child.communicate();raise
  result['exit']=child.returncode
  if child.returncode!=0:raise RuntimeError('Child nonzero; retain exit86 trap/87 fault/other failure without retry')
  parsed=parse_output(stdout.decode('utf-8'),stderr.decode('utf-8'));save('parsed.json',parsed)
  if not parsed['code_matches']:raise ValueError('POSTHOC mapped code mismatch; calls may already have run, no retry')
  result['capture_complete']=True
 except BaseException as error:result['exception']=type(error).__name__+': '+str(error)
 finally:
  if child is not None and child.poll() is None:os.killpg(child.pid,signal.SIGKILL);stdout,stderr=child.communicate()
  if child is not None:result['exit']=child.returncode
  raw('child.stdout',stdout);raw('child.stderr',stderr)
  # Complete return rows are a lower-bound observation, not absence if a call faults before printing.
  rows=re.findall(rb'^call ([01]) (0x104b8c760|0x104b8c7b0) rax=0x[0-9a-f]+ rdx=0x[0-9a-f]+ xmm0=0x[0-9a-f]+ xmm1=0x[0-9a-f]+$',stdout,re.M)
  result['completed_original_call_rows']=len(rows)
  result['unobserved_original_execution']='unknown for any missing return rows; spawn/exit alone is not original-call proof'
  after=[]
  for p in paths:
   try:after.append(identity(p))
   except BaseException as error:after.append(dict(path=str(p),error=str(error)))
  save('after-map.json',dict(files=after,unchanged=before==after))
  result.update(finished_utc=utc(),watched=len(paths),unchanged=before==after);save('status.json',result)
  files=[]
  for p in sorted(DEST.iterdir()):
   if p.is_file():v=identity(p);files.append(dict(path=p.name,bytes=v['bytes'],sha256=v['sha256']))
  save('manifest.json',dict(files=files,status='capture evidence only; inspect status, not a pass certificate'))
 print(json.dumps(result,indent=2))
 return 0 if result['exception'] is None and result['capture_complete'] and result['exit']==0 and result['unchanged'] else 1
if __name__=='__main__':raise SystemExit(main())
