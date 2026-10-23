"""PREPARATION ONLY: one separately selected child, four fixed original call sites."""
from pathlib import Path
import datetime,hashlib,json,os,re,resource,signal,subprocess,sys
ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
PRE=BASE/'depth-utility-xexec-chained-state-preparation'
DEST=BASE/'depth-utility-xexec-chained-state'
BIN=BASE/'depth-utility-xexec-owned-build/xexec'
IMAGE=Path('/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64')
CODE=[('0x104b8c760', 13, '554889e54088b7cf0000005dc3'), ('0x104b8c7b0', 920, '0f57c080bfcf000000000f8577030000554889e58b87c80000004883f8030f87e7010000f20f100ef20f10070f59c1488d0d52030000486304814801c8ffe0f30f12c0e985020000f30f16c0e97c0200000fc6c0e148ff4748f20f104f38f20f1057400f58d10f135738f30f16d0f30f12c00f59c10fc6c9e10f59ca0f58c10fb687cc0000003c0175090fb68fcd000000eb100fb68fcd00000080f9010f852a020000f30f16d00f28caf30f58c8f30f101d9abaee00f30f59cbf30f5cc2f30f59c3f30f109794000000f30f102542b9ee00f30f58e20f28daf30f5edcf30f59156bbaee00f30f102523b9ee00f6c1010f841d0100000f28eaf30f58ec0f28f2f30f59f5f30f58f4440f28c2f3440f5ec60f572d488dfa000f10bf98000000f30f5ccff30f59cb440f28cff3440f58c9f30f10a7a0000000f3440f5ccc0f28f5660f3a21f21cf3440f16d7450f28da66450f3a21d910440f59de66450f3a0cca0e450f58cbf3450f12c0450f59c8f3410f16f1440f28d7440fc6d7fff3410f5cc2f30f59c3f3440f58d0410f16c9410fc6c9d8660f3a21c8300f58c90f58cf0f118f98000000f20f1087a8000000f30f16c8f3440f5cd1660f3a21d510f30f12c866410f3a0cca010f59d10fc6c9e10f58ca410f59c80f28d10f58d10fc6d2e10f58d00f1397a80000000f57d284c0750bf30f12c90f58c1f30f16d0f30f58e60f28cc0f28c2e9b40000000f57c0e9ba0000000f28f2f30f58f40f28eaf30f59eef30f58ec0f28faf30f5efdf30f10a7ac000000f20f10afa4000000440f28c0f3440f5cc5f3410f59d8440f28c5f3440f58c3f3410f5cc0440f28c0f3440f5cc4f3440f16cdf3410f59f1f3410f59d0f3440f5cc6f3440f59c7f3410f58d1f30f59d7f3450f58c80f28f4f30f58f266410f3a21d8100f58db0f58dd0f139fa4000000f30f58d2f30f58d4f30f1197ac000000f3410f5cc1f30f5cc60f28d0f30f58c1f30f5cca660f3a21c11048ff8788000000f20f104f78f20f1097800000000f58d10f1357780f59c180bfce000000010f858e000000f30f109fb0000000f30f591d48b8ee00f30f102504b7ee00f30f58e30f28d3f30f59d4f30f5815edb6ee00f30f12cbf30f5edaf20f10afb4000000f20f10b7bc0000000f28d00f5cd6f30f12e40f59e50f59ca0f5cd4f30f12db0f59d30f28e20f58e20f58e50f58cd0f59cb0f28d90f58d90f58de0f16e30f11a7b40000000f58d50f58ce0f58d20f5cc20f5cc15dc3b7fcffffcdfcffffc0fcffffc9fcffff')]
TOKENS=['--imports', 'dump', '0x104b8c760', '13', 'dump', '0x104b8c7b0', '920', 'call', '0x104b8c7b0', 'hex:0000803f0000803f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803f0000803f0000003f0000803e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000', 'hex:0000803f000000c0', 'd:0x1p+0', 'dump', 'b0', '208', 'call', '0x104b8c7b0', 'ref:b0', 'ref:b1', 'd:0x1p+0', 'dump', 'b0', '208', 'call', '0x104b8c760', 'ref:b0', 'i:1', 'dump', 'b0', '208', 'call', '0x104b8c7b0', 'ref:b0', 'ref:b1', 'd:0x1p+0', 'dump', 'b0', '208', 'dump', 'b1', '8']
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
 """Pure fixed protocol parser; differing state/returns remain counterevidence."""
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
  row=take(r'call ([0-3]) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)')
  k,a,*registers=row.groups();v=[int(x,16) for x in registers]
  if int(k)!=index or int(a,16)!=address or any(x>=1<<64 for x in v):raise ValueError('Call identity/register width mismatch')
  calls.append(dict(index=index,address=hex(address),rax=registers[0],rdx=registers[1],xmm0=registers[2],xmm1=registers[3]))
 def buffer(kind,label,n):
  row=take(kind+r' '+label+r' (0x[0-9a-f]+) ([0-9a-f]+)');a,h=row.groups();a=int(a,16)
  if a==0 or a%16 or a+n>1<<64 or len(h)!=2*n:raise ValueError('Owned buffer pointer/length mismatch')
  return a,h
 call(0,0x104b8c7b0);b0,automatic_state=buffer('out','b0',208);b1,initial_input=buffer('out','b1',8)
 if not (b0+208<=b1 or b1+8<=b0):raise ValueError('Owned buffers overlap')
 states=[]
 for index,address in [(0,None),(1,0x104b8c7b0),(2,0x104b8c760),(3,0x104b8c7b0)]:
  if address is not None:call(index,address)
  pointer,h=buffer('dump','b0',208)
  if pointer!=b0:raise ValueError('State pointer changed')
  raw=bytes.fromhex(h)
  states.append(dict(after_call=index,hex=h,counter48_u64=int.from_bytes(raw[0x48:0x50],'little'),counter88_u64=int.from_bytes(raw[0x88:0x90],'little'),pair38_hex=raw[0x38:0x40].hex(),common78_hex=raw[0x78:0x80].hex(),flag_cf_u8=raw[0xcf]))
 pointer,final_input=buffer('dump','b1',8)
 if pointer!=b1:raise ValueError('Input pointer changed')
 used={}
 while i<len(lines):
  row=take(r'used (\S+) ([1-9]\d*)');name,n=row.groups()
  if name in used or name not in imports or imports[name]['category']!='linux':raise ValueError('Used import identity/category mismatch')
  used[name]=int(n)
 return dict(loaded=dict(rebases=counts[0],linux_slots=counts[1],trap_slots=counts[2],symbols=counts[3]),imports=imports,used=used,code_dumps=code,code_matches=all(r['matches_retained'] for r in code),calls=calls,completed_original_call_rows=4,state_buffer_address=hex(b0),input_buffer_address=hex(b1),automatic_state_after_call0_hex=automatic_state,automatic_input_after_call0_hex=initial_input,states_after_each_call=states,final_input_hex=final_input,observations=dict(automatic_vs_explicit_state0_equal=automatic_state==states[0]['hex'],input_after_history_unchanged=initial_input==final_input,final_helper_low64_xmm0_zero=int(calls[3]['xmm0'],16)==0),actual_expected=None,comparison=None,new_grade=0,limits='Raw observations only; no state/return prediction is a validity or success filter. Even automatic/explicit state differences are retained. Code comparisons are POSTHOC, not a pre-call barrier. Import reports are instrumentation, not exhaustive absence or targetaddress proof.')
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
 result=dict(started_utc=utc(),attempts=0,returned_pid=None,exit=None,timeout=False,exception=None,automatic_retry=False,maximum_selected_top_level_original_calls=4,completed_original_call_rows=0,unobserved_original_execution='unknown until captured evidence',capture_complete=False)
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
  rows=re.findall(rb'^call ([0-3]) (0x104b8c760|0x104b8c7b0) rax=0x[0-9a-f]+ rdx=0x[0-9a-f]+ xmm0=0x[0-9a-f]+ xmm1=0x[0-9a-f]+$',stdout,re.M)
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
