#!/usr/bin/env python3
"""One fixed44-byte static decode, no native-original execution/target following."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
P=Path(__file__).resolve().parent
START,SIZE,ROWS=0x1888,44,11
IMAGE={'path':'/var/tmp/sound-analysis/helpers/Analog/Analog.arm64','bytes':432640,'sha256':'211bd67c47291a4dfd0e76c7b85cf63490dc5df48b67992a154beac0372f09ab'}
TOOL={'path':'/var/tmp/sound-tools/rizin-v0.9.1/bin/rizin','bytes':59344432,'sha256':'ab5614cf137608cffc5a3f4f471a91c995cfa7c0c35465bfb73876e5b95561ba'}
ENV={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,n):
    if not ok:raise ValueError(n)
def store(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def js(p,d):store(p,(json.dumps(d,indent=2)+'\n').encode())
def identity(p):
    with Path(p).open('rb') as f:
        h=hashlib.sha256();n=0
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b);n+=len(b)
    return {'path':str(p),'bytes':n,'sha256':h.hexdigest()}
def plan_ok(d):
    need(d['image']==IMAGE and d['tool']==TOOL,'image-tool')
    need(d['start']=='0x1888' and d['end_exclusive']=='0x18b4' and d['file_offset']==START,'fixed-mapping')
    need((d['native_bytes'],d['rows'],d['data_bytes'])==(44,11,0),'fixed-counts')
    need(d['C_bytes']==126 and d['C_lines']==11,'complete-source')
def row_ok(rows,raw):
    need(len(rows)==ROWS and len(raw)==SIZE,'row-total')
    for i,r in enumerate(rows):
        need(r['offset']==START+4*i and r['size']==4 and r['bytes']==raw[4*i:4*i+4].hex(),'row-association')
def selfcheck():
    d={'image':IMAGE,'tool':TOOL,'start':'0x1888','end_exclusive':'0x18b4','file_offset':START,'native_bytes':44,'rows':11,'data_bytes':0,'C_bytes':126,'C_lines':11}
    plan_ok(d); raw=bytes(range(SIZE));rows=[{'offset':START+4*i,'size':4,'bytes':raw[4*i:4*i+4].hex()} for i in range(ROWS)];row_ok(rows,raw)
    controls=[]
    def reject(n,fn):
        try:fn()
        except ValueError:controls.append(n)
        else:raise AssertionError(n)
    for k,v in [('start','0x1884'),('end_exclusive','0x18b8'),('file_offset',0),('native_bytes',48),('rows',12),('data_bytes',8),('C_bytes',125),('C_lines',10)]:
        q=json.loads(json.dumps(d));q[k]=v;reject(k,lambda q=q:plan_ok(q))
    reject('missing-row',lambda:row_ok(rows[:-1],raw))
    reject('extra-code-bytes',lambda:row_ok(rows,raw+bytes(4)))
    q=json.loads(json.dumps(rows));q[0]['bytes']='00000000';reject('raw-corruption',lambda:row_ok(q,raw))
    q=json.loads(json.dumps(rows));q[-1]['offset']+=4;reject('wrong-PC',lambda:row_ok(q,raw))
    print(json.dumps({'status':'PASS','negative_controls':controls,'count':12,'image_tool_source_external_reads':0},indent=2))
def cleanup(pid):
    try:os.killpg(pid,signal.SIGKILL);return 'SIGKILL-process-group-sent'
    except ProcessLookupError:return 'process-group-already-gone'
def capture(expected):
    b=(P/'input-plan.json').read_bytes();need(sha(b)==expected,'frozen-plan-hash');plan=json.loads(b);plan_ok(plan)
    out=P/'capture';out.mkdir(exist_ok=False);resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    s={'started_utc':now(),'pid':os.getpid(),'argv':sys.argv,'environment':dict(os.environ),'input_plan_sha256':expected,'attempts':1,'automatic_retry':False,'selected_content_bytes_read':0,'children_started':0,'native_original_execution':0,'error':None}
    try:
        need(dict(os.environ)==ENV,'minimal-env')
        before=[identity(p['path']) for p in plan['pins']];need(before==plan['pins'],'before-pins');js(out/'before-identities.json',before)
        with Path(IMAGE['path']).open('rb') as f:
            need(os.fstat(f.fileno()).st_size==IMAGE['bytes'],'image-size');f.seek(START);raw=f.read(SIZE)
        need(len(raw)==SIZE,'short-image-read');store(out/'1888.bin',raw);s['selected_content_bytes_read']=len(raw)
        js(out/'extraction.json',{'start':hex(START),'end_exclusive':'0x18b4','file_offset':START,'bytes':len(raw),'sha256':sha(raw),'mapping':'retained H4 textsection; file_offset=VA; no header/LC/fixup read'})
        argv=[TOOL['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(START),'-s',hex(START),'-q','-c','pdj 11',str(out/'1888.bin')]
        inv={'argv':argv,'started_utc':now(),'timeout_seconds':30,'stdin':'DEVNULL','environment':ENV,'core_bytes':0,'new_session':True}
        js(out/'invocation-before.json',inv)
        child=subprocess.Popen(argv,env=ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        s['children_started']=1;inv['pid']=child.pid;js(out/'pid.json',{'pid':child.pid,'pgid':child.pid,'spawned_utc':now(),'argv':argv})
        try:
            stdout,stderr=child.communicate(timeout=30);inv.update(timed_out=False,exit_code=child.returncode)
        except subprocess.TimeoutExpired:
            inv['timed_out']=True;inv['cleanup']=cleanup(child.pid);stdout,stderr=child.communicate(timeout=5);inv['exit_code']=child.returncode
        finally:
            inv.setdefault('cleanup',cleanup(child.pid));inv['finished_utc']=now();js(out/'invocation-after.json',inv)
        store(out/'1888.stdout.json',stdout);store(out/'1888.stderr',stderr)
        need(not inv['timed_out'] and inv['exit_code']==0 and not stderr,'decoder-status')
        row_ok(json.loads(stdout),raw);s['validated_rows']=11
        after=[identity(p['path']) for p in plan['pins']];js(out/'after-identities.json',{'files':after,'unchanged':after==before});need(after==before,'after-pins')
        s['recorded_custody_pairs']=len(before);s['watch_unchanged']=True
    except BaseException as e:s['error']=type(e).__name__+': '+str(e);raise
    finally:s['finished_utc']=now();js(out/'status.json',s)
    print(json.dumps(s,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--self-check',action='store_true');g.add_argument('--capture-once');a=ap.parse_args()
    if a.self_check:selfcheck()
    else:capture(a.capture_once)
