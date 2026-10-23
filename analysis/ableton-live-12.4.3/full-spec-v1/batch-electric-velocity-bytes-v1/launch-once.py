#!/usr/bin/env python3
"""Pre-call-pinned ordinary parent launcher for the one fixed recorder, never retry/resume."""
import hashlib,json,os,pathlib,signal,subprocess,sys
from datetime import datetime,timezone
H=pathlib.Path(__file__).resolve().parent
now=lambda:datetime.now(timezone.utc).isoformat()
def save(d):
 with (H/'outer-receipt.json').open('w') as f:json.dump(d,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
assert len(sys.argv)==2;prehash=sys.argv[1];assert hashlib.sha256((H/'pre-call-manifest.json').read_bytes()).hexdigest()==prehash
assert not (H/'attempts').exists() and not (H/'outer.stdout').exists() and not (H/'outer-receipt.json').exists()
ctx=json.loads((H/'context.json').read_text());argv=[ctx['python'],'-I','-B',str(H/'record.py'),'--run-once',prehash];env=ctx['environment'];p=None
d={'argv':argv,'environment':env,'utc_start':now(),'parent_pid':os.getpid(),'parent_argv':sys.argv,'pid':None,'exit':None,'retry':False,'interrupted':None,'cleanup':None,'precall_sha256':prehash};save(d)
def stop(sig,frame):raise RuntimeError('parent signal '+str(sig))
signal.signal(signal.SIGTERM,stop)
try:
 with (H/'outer.stdout').open('xb') as out,(H/'outer.stderr').open('xb') as err:
  p=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=env,cwd=H,start_new_session=True);d['pid']=p.pid;save(d);d['exit']=p.wait()
except BaseException as e:
 d['interrupted']={'type':type(e).__name__,'message':str(e)}
 if p is not None and p.poll() is None:
  os.killpg(p.pid,signal.SIGTERM)
  try:d['exit']=p.wait(timeout=10);d['cleanup']='SIGTERM sent to recorder group; recorder handles current child cleanup'
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);d['exit']=p.wait(timeout=5);d['cleanup']='recorder group SIGKILL/directrecorder reaped; distinct original child group may survive if recorder failed cleanup'
 raise
finally:
 d['utc_end']=now();d['precall_sha256_after']=hashlib.sha256((H/'pre-call-manifest.json').read_bytes()).hexdigest();save(d)
print(json.dumps(d));sys.exit(d['exit'] if d['exit'] is not None else 1)
