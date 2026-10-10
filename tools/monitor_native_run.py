#!/usr/bin/env python3
"""Monitor only an explicitly named analyst transport and its descendants."""
import argparse,datetime,json,os,signal,shutil,subprocess,time,shlex,math
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('spool',type=Path);p.add_argument('--interval',type=float,default=1);p.add_argument('--log-interval',type=float,default=30);a=p.parse_args();spool=a.spool.resolve()
if not all(math.isfinite(v) and v>0 for v in (a.interval,a.log_interval)):raise SystemExit('Intervals must be finite and positive')
def snapshot():
 rows={}
 for line in subprocess.check_output(['ps','-axo','pid=,ppid=,rss=,comm='],text=True).splitlines():
  parts=line.strip().split(None,3)
  if len(parts)==4:
   pid,ppid,rss=map(int,parts[:3]);rows[pid]={'pid':pid,'ppid':ppid,'rss_bytes':rss*1024,'comm':parts[3]}
 return rows
def descendants(rows,parent):
 found={parent};changed=True
 while changed:
  changed=False
  for pid,row in rows.items():
   if row['ppid'] in found and pid not in found:found.add(pid);changed=True
 return found
def identity(pid):
 try:return subprocess.check_output(['ps','-p',str(pid),'-o','lstart='],text=True).strip() or None
 except subprocess.CalledProcessError:return None
def keep_logs(procs):
 dest=spool/'provider-log-captures';dest.mkdir(exist_ok=True)
 for row in procs:
  if Path(row['comm']).name!='java':continue
  try:args=shlex.split(subprocess.check_output(['ps','-p',str(row['pid']),'-o','args='],text=True))
  except (subprocess.CalledProcessError,ValueError):continue
  for flag in ('-log','-scriptlog'):
   if flag not in args or args.index(flag)+1>=len(args):continue
   path=Path(args[args.index(flag)+1])
   if not path.is_file():continue
   stamp=datetime.datetime.now().strftime('%Y%m%dT%H%M%S%f')
   try:
    with path.open('rb') as f:
     size=path.stat().st_size;f.seek(max(0,size-2*1024**2));data=f.read()
    (dest/(stamp+'-'+path.name)).write_bytes(data)
    (dest/(stamp+'-'+path.name+'.json')).write_text(json.dumps({'source':str(path),'source_bytes':size,'retained_tail_bytes':len(data),'complete':size==len(data)})+'\n')
   except OSError:pass
lock=spool/'transport.lock' 
for _ in range(120):
 if lock.exists():break
 time.sleep(.5)
else:raise SystemExit('No transport lock appeared')
owner=int(lock.read_text());owner_identity=identity(owner);args=subprocess.check_output(['ps','-p',str(owner),'-o','args='],text=True)
if 'run_native_analysis.mjs' not in args or str(spool) not in args:raise SystemExit('Owner command does not match spool')
log=spool/('resource-'+datetime.datetime.now().strftime('%Y%m%dT%H%M%S')+'.jsonl');excess=0
remembered={};last_log_capture=0
with log.open('x') as out:
 while lock.exists():
  rows=snapshot()
  if owner not in rows or identity(owner)!=owner_identity:break
  owned=descendants(rows,owner);procs=[rows[x] for x in sorted(owned) if x in rows];free=shutil.disk_usage(spool).free
  remembered.update({x['pid']:(identity(x['pid']),x) for x in procs})
  java=sum(x['rss_bytes'] for x in procs if Path(x['comm']).name=='java');total=sum(x['rss_bytes'] for x in procs);excess=excess+1 if total>6*1024**3 else 0
  reason='disk_floor' if free<3*1024**3 else 'owned_rss' if excess>=2 else None
  row={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner_pid':owner,'free_disk_bytes':free,'java_rss_bytes':java,'owned_rss_bytes':total,'processes':procs,'stop_reason':reason};out.write(json.dumps(row)+'\n');out.flush()
  if reason:
   (spool/'RESOURCE_STOP.json').write_text(json.dumps(row,indent=2)+'\n')
   keep_logs(procs)
   identities={pid:identity(pid) for pid in owned}
   # Stop controller first; it halts scheduling and owns graceful server cleanup.
   if identity(owner)==owner_identity:
    try:os.kill(owner,signal.SIGTERM)
    except ProcessLookupError:pass
   time.sleep(5)
   for sig in (signal.SIGTERM,signal.SIGKILL):
    for pid,start in identities.items():
     if start is None or identity(pid)!=start:continue
     try:os.kill(pid,sig)
     except ProcessLookupError:pass
    time.sleep(2)
   surviving=[pid for pid,start in identities.items() if start is not None and identity(pid)==start]
   out.write(json.dumps({'termination_checked':True,'surviving_owned_pids':surviving})+'\n');out.flush()
   break
  if time.monotonic()-last_log_capture>=a.log_interval:
   keep_logs(procs);last_log_capture=time.monotonic()
  time.sleep(a.interval)
# Check only previously observed owned processes after an unexpected owner exit.
remaining={pid:start for pid,(start,row) in remembered.items() if pid!=owner and start is not None and identity(pid)==start}
if remaining:
 keep_logs([remembered[pid][1] for pid in remaining])
 for sig in (signal.SIGTERM,signal.SIGKILL):
  for pid,start in remaining.items():
   if identity(pid)!=start:continue
   try:os.kill(pid,sig)
   except ProcessLookupError:pass
  time.sleep(2)
 with log.open('a') as out:out.write(json.dumps({'orphan_cleanup':True,'surviving_owned_pids':[pid for pid,start in remaining.items() if identity(pid)==start]})+'\n')
print(log)
