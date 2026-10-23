"""Exactly one Root-selected static-DATA collector; never original instructions."""
from pathlib import Path
import datetime,hashlib,json,os,resource,signal,subprocess,sys
ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
PRE=BASE/'depth-corpus-x86-create-c18c-instructions-preparation'
ACTUAL=BASE/'depth-corpus-x86-create-c18c-instructions'
OUT=BASE/'reviews/corpus-x86-create-c18c-selected-execution'
EXPECTED='5744accc52962574159ad47a75280b57ca3dd9bbc09eb238323c732055159a16'

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):n+=len(b);h.update(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def save(n,o):
 with (OUT/n).open('x') as f:json.dump(o,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def raw(n,b):
 with (OUT/n).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def no_core():resource.setrlimit(resource.RLIMIT_CORE,(0,0))

def main():
 assert not OUT.exists() and not ACTUAL.exists()
 assert identity(PRE/'manifest.json')['sha256']==EXPECTED
 OUT.mkdir();raw('runner.py',Path(__file__).read_bytes())
 child=None;stdout=b'';stderr=b'';before=[];paths=[]
 receipt=dict(selected_utc=utc(),selection='Root explicit exactly one frozen--collect-selected/c18c240B/pdj16/staticDATA',manifest=identity(PRE/'manifest.json'),collector_attempts=0,returned_pid=None,exit=None,timeout=False,exception=None,original_instruction_execution=False,automatic_retry=False)
 save('selection.json',receipt)
 try:
  inputs=json.loads((PRE/'inputs.json').read_text())['pins']
  preflights=[BASE/'reviews/corpus-x86-create-c18c-root-code-preflight.json',BASE/'reviews/corpus-x86-create-c18c-code-preflight-review.json']
  assert identity(preflights[0])['sha256']=='9a798f57e7eb7ba7980ce4bec95c5d917ad9ba8d085ee6de984c81679484df89'
  assert identity(preflights[1])['sha256']=='c7e96e119271a4399def9ac8a2498dd69e172f773579440b4979776d3ebac79b'
  watched={Path(r['path']) for r in inputs}|set(preflights)|{p for p in PRE.iterdir() if p.is_file()}
  for base in [ROOT/'handoff',ROOT/'analysis/ableton-live-12.4.3/handoff-staging']:
   watched.update(p for p in base.rglob('*') if p.is_file())
  for base in BASE.glob('depth-*'):
   if base.is_dir():watched.update(p for p in base.rglob('*') if p.is_file())
  paths=sorted(watched)
  before=[identity(p) for p in paths];save('before-map.json',dict(utc=utc(),scope='Fixed existing-file set: all handoff/public+staging, all existing full-spec depthtrees, exact inputpins/currentprep/two preflights; excludes newly created outer/actualdest.',files=before))
  for r in inputs:assert identity(Path(r['path']))=={k:r[k] for k in ('path','bytes','sha256')}
  manifest=json.loads((PRE/'manifest.json').read_text())
  for r in manifest['files']:
   got=identity(PRE/r['path']);assert (got['bytes'],got['sha256'])==(r['bytes'],r['sha256'])
  argv=[sys.executable,'-B',str(PRE/'collect-once.py'),'--collect-selected']
  env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL','TZ') if k in os.environ}
  save('invocation.json',dict(utc=utc(),argv=argv,cwd=str(OUT),environment=env,core_limit=[0,0],stdin='DEVNULL',timeout_seconds=55,start_new_session=True,cleanup='On timeout/interruption kill collector processgroup and wait; no retry.'))
  receipt['collector_attempts']=1
  child=subprocess.Popen(argv,cwd=OUT,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=no_core,start_new_session=True)
  receipt['returned_pid']=child.pid;save('collector-pid.json',dict(utc=utc(),pid=child.pid))
  try:stdout,stderr=child.communicate(timeout=55)
  except subprocess.TimeoutExpired:
   receipt['timeout']=True;os.killpg(child.pid,signal.SIGKILL);stdout,stderr=child.communicate();raise
  receipt['exit']=child.returncode
  assert child.returncode==0
  status=json.loads((ACTUAL/'status.json').read_text())
  assert status['attempted_decoder_children']==1 and status['returned_pid_children']==1 and status['exit']==0 and status['exception'] is None and status['providers_unchanged'] is True
  assert status['validation']=='PASS16valid-variable-length-rows/exact-prefix-only'
  receipt['inner_status']=status
 except BaseException as error:
  receipt['exception']=type(error).__name__+': '+str(error)
 finally:
  if child is not None and child.poll() is None:
   os.killpg(child.pid,signal.SIGKILL);stdout,stderr=child.communicate()
  if child is not None:receipt['exit']=child.returncode
  raw('collector.stdout.json',stdout);raw('collector.stderr',stderr)
  after=[]
  for p in paths:
   try:after.append(identity(p))
   except BaseException as error:after.append(dict(path=str(p),identity_error=type(error).__name__+': '+str(error)))
  unchanged=bool(before) and before==after
  save('after-map.json',dict(utc=utc(),files=after,unchanged=unchanged))
  receipt.update(finished_utc=utc(),watched=len(paths),unchanged=unchanged,stdout_bytes=len(stdout),stderr_bytes=len(stderr))
  save('receipt.json',receipt)
 print(json.dumps(receipt,indent=2))
 return 0 if receipt['exception'] is None and receipt['exit']==0 and receipt['unchanged'] else 1
if __name__=='__main__':raise SystemExit(main())
