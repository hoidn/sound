#!/usr/bin/env python3
"""One fixed static data acquisition. No decoder, subprocess or native execution."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import sys

P = Path(__file__).resolve().parent
IMAGE = {'path':'/var/tmp/sound-analysis/helpers/Analog/Analog.arm64','bytes':432640,
         'sha256':'211bd67c47291a4dfd0e76c7b85cf63490dc5df48b67992a154beac0372f09ab'}
RANGES = [('dispatch-bytes', 0x52ec0, 126), ('producer-word', 0x58130, 8)]
ENV = {'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'}

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def need(ok, label):
    if not ok:
        raise ValueError(label)

def store(path, b):
    with path.open('xb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())

def write_json(path, obj):
    store(path, (json.dumps(obj, indent=2)+'\n').encode())

def identity(path):
    # Full file read is solely custody; not interpreted binary/header/code content.
    with Path(path).open('rb') as f:
        digest=hashlib.sha256(); size=0
        for block in iter(lambda:f.read(1024*1024), b''):
            digest.update(block); size+=len(block)
    return {'path':str(path),'bytes':size,'sha256':digest.hexdigest()}

def validate_plan(plan):
    need(plan['image']==IMAGE, 'exact-image')
    need(plan['ranges']==[{'label':n,'VA':hex(a),'file_offset':a,'bytes':b} for n,a,b in RANGES], 'exact-ranges')
    need(plan['total_data_bytes']==134 and plan['new_code_bytes']==0, 'total-data-only')
    need(plan['guard_windows']==[
        {'table':'0x52ec0','index_min':0,'index_max':10,'branch_base':'0x2d34'},
        {'table':'0x52ecb','index_min':0,'index_max':114,'branch_base':'0x2c9c'}], 'whole-guard-windows')

def selfcheck():
    plan={'image':IMAGE,'ranges':[{'label':n,'VA':hex(a),'file_offset':a,'bytes':b} for n,a,b in RANGES],
          'total_data_bytes':134,'new_code_bytes':0,'guard_windows':[
              {'table':'0x52ec0','index_min':0,'index_max':10,'branch_base':'0x2d34'},
              {'table':'0x52ecb','index_min':0,'index_max':114,'branch_base':'0x2c9c'}]}
    validate_plan(plan)
    controls=[]
    for label, edit in [
        ('wrong-image',lambda d:d['image'].update(bytes=432639)),
        ('short-window',lambda d:d['ranges'][0].update(bytes=125)),
        ('extra-word',lambda d:d['ranges'].append(dict(d['ranges'][1]))),
        ('wrong-mapping',lambda d:d['ranges'][1].update(file_offset=0)),
        ('source-code-expansion',lambda d:d.update(new_code_bytes=4)),
        ('wrong-total',lambda d:d.update(total_data_bytes=135)),
        ('firstN-table',lambda d:d['guard_windows'][1].update(index_max=10)),
        ('wrong-branch-base',lambda d:d['guard_windows'][0].update(branch_base='0x2c9c'))]:
        d=json.loads(json.dumps(plan)); edit(d)
        try: validate_plan(d)
        except ValueError: controls.append(label)
        else: raise AssertionError(label)
    need(len(controls)==8,'selfcheck-count')
    print(json.dumps({'status':'PASS','data_only':True,'image_reads':0,'negative_controls':controls},indent=2))

def capture(expected):
    raw=(P/'input-plan.json').read_bytes()
    need(sha(raw)==expected,'exact-frozen-input-plan')
    plan=json.loads(raw); validate_plan(plan)
    out=P/'capture'; out.mkdir(exist_ok=False)
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    status={'started_utc':now(),'pid':os.getpid(),'ppid':os.getppid(),'argv':sys.argv,
            'environment':dict(os.environ),'core_limit_bytes':0,'attempts':1,'automatic_retry':False,
            'children':0,'original_instruction_execution':0,'selected_content_bytes_read':0,
            'input_plan_sha256':expected,'error':None}
    try:
        need(dict(os.environ)==ENV,'minimal-environment')
        before=[identity(x['path']) for x in plan['pins']]
        need(before==plan['pins'],'before-immutable-pins')
        write_json(out/'before-identities.json',before)
        read_ranges=[]
        with Path(IMAGE['path']).open('rb') as f:
            need(os.fstat(f.fileno()).st_size==IMAGE['bytes'],'open-image-size')
            for name, addr, count in RANGES:
                f.seek(addr); b=f.read(count)
                need(len(b)==count,'exact-short-read')
                store(out/(name+'.bin'),b)
                status['selected_content_bytes_read']+=len(b)
                read_ranges.append({'label':name,'VA':hex(addr),'file_offset':addr,'bytes':len(b),'sha256':sha(b)})
        write_json(out/'extraction.json',{'ranges':read_ranges,'content_bytes':134,'code_bytes':0,
                   'mapping':'exact retained H4 sections, file_offset=VA','reads_per_range':1})
        after=[identity(x['path']) for x in plan['pins']]
        write_json(out/'after-identities.json',{'files':after,'unchanged':after==before})
        need(after==before,'after-immutable-pins')
        status['recorded_custody_pairs']=len(before); status['watch_unchanged']=True
    except BaseException as e:
        status['error']=type(e).__name__+': '+str(e)
        raise
    finally:
        status['finished_utc']=now()
        write_json(out/'status.json',status)
    print(json.dumps(status,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--self-check',action='store_true');g.add_argument('--capture-once')
    a=ap.parse_args()
    if a.self_check:selfcheck()
    else:capture(a.capture_once)
