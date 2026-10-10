#!/usr/bin/env python3
"""Prepare or explicitly execute a bounded, separate-profile Ghidra selected export."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import time

TARGET_SHA256='3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
PROFILE='ghidra-selected-entry-noanalysis-v1'


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda:stream.read(1024*1024),b''):h.update(data)
    return h.hexdigest()


def validate_seeds(value):
    if not isinstance(value,list) or not 1<=len(value)<=20:raise ValueError('One to twenty explicit seeds required')
    seen=set()
    for seed in value:
        if not isinstance(seed,dict) or set(seed)!={'address','window_bytes','source','label'}:raise ValueError('Each seed requires address, window_bytes, source, label')
        address=seed['address'];size=seed['window_bytes']
        if not isinstance(address,str) or not re.fullmatch(r'0x[0-9a-f]+',address) or address!=hex(int(address,16)) or int(address,16)%4:raise ValueError('Canonical aligned default-space address required')
        if type(size) is not int or not 4<=size<=65536 or size%4:raise ValueError('Window must be aligned and 4..65536 bytes')
        if address in seen:raise ValueError('Duplicate selected entry')
        if not all(isinstance(seed[k],str) and seed[k].strip() for k in ('source','label')):raise ValueError('Seed source and label required')
        if int(address,16)+size-1>2**64-1:raise ValueError('Window overflow')
        seen.add(address)
    # Overlapping windows can share disassembly observations, but selected bodies
    # are independently checked for overlap by the script. Preserve exact order.
    return value


def plan(config,output,ghidra,jdk):
    seeds=validate_seeds(config['seeds']);target=Path(config['target']).resolve()
    if config.get('target_sha256')!=TARGET_SHA256 or digest(target)!=TARGET_SHA256:raise ValueError('Pinned target SHA-256 mismatch')
    if any(char in str(output) for char in ('\"',"'",'\n','\r','\\')):raise ValueError('Output path contains unsupported JVM option quoting characters')
    if any(part.startswith('.') for part in output.resolve().parts):raise ValueError('Ghidra project ancestors must not be dot-prefixed')
    if shutil.disk_usage(output.parent).free<3*1024**3:raise ValueError('Disk reserve below 3GiB before targeted launch')
    properties=(ghidra/'Ghidra/application.properties').read_text()
    version=re.search(r'^application.version=(.+)$',properties,re.M)
    if not version or version[1].strip()!='12.1.4':raise ValueError('Expected Ghidra12.1.4')
    if not (jdk/'bin/java').is_file() or not (ghidra/'support/analyzeHeadless').is_file():raise ValueError('Installed Java/Ghidra launcher missing')
    method=Path(__file__).resolve().parent/'ghidra/SelectedNativeExport.java'
    settings={'schema':1,'profile':PROFILE,'target':str(target),'target_sha256':TARGET_SHA256,
        'architecture':'arm64','ghidra_version':'12.1.4','method_sha256':digest(method),
        'seeds':seeds,'auto_analysis':False,'incremental_code_analysis':False,
        'decompile_timeout_seconds':60,'overall_timeout_seconds':600,'java_heap':'4G',
        'disk_reserve_bytes':3*1024**3,'group_rss_limit_bytes':6*1024**3,'resource_sample_seconds':1,
        'resource_watchdog':'owned-process-group-v1',
        'limitations':['Selected entries only; not the default-profile inventory.',
                      'Custom script output, not REA evidence records.']}
    command=[str(ghidra/'support/analyzeHeadless'),str(output/'project'),'sound-targeted',
        '-import',str(target),'-readOnly','-deleteProject','-noanalysis','-max-cpu','2',
        '-log',str(output/'ghidra.log'),'-scriptlog',str(output/'script.log'),
        '-scriptPath',str(output/'method'),'-postScript',str(output/'method/SelectedNativeExport.java'),
        str(output/'run.json'),str(output)]
    return settings,command,method


def write_json(path,value):
    with path.open('x') as stream:
        json.dump(value,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())


def outcomes(output,seeds,settings):
    items=[]
    for seed in seeds:
        path=output/'functions'/seed['address']/'metadata.json'
        if not path.exists():
            items.append({'address':seed['address'],'state':'missing','error':'No committed selected-entry result'});continue
        try:
            value=json.loads(path.read_text())
            expected={'address':seed['address'],'target_sha256':TARGET_SHA256,'profile':PROFILE,
                      'provider':'ghidra-headless-selected-script','ghidra_version':settings['ghidra_version'],
                      'method_sha256':settings['method_sha256']}
            if any(value.get(key)!=item for key,item in expected.items()):raise ValueError('Script result identity/profile/method/version mismatch')
            if digest(output/'method/SelectedNativeExport.java')!=settings['method_sha256']:raise ValueError('Captured method changed')
            state=value.get('state')
            if state not in ('exported','exported-with-warnings','failed'):raise ValueError('Unknown selected-entry state')
            if state!='failed':
                if not all((path.parent/name).is_file() and (path.parent/name).stat().st_size>0 for name in ('pseudocode.c','assembly.txt')):raise ValueError('Successful result is missing code or assembly')
                if not value.get('body_ranges') or value.get('body_bytes',0)<=0 or value.get('instruction_count',0)<=0:raise ValueError('Successful result is missing body evidence')
                if value.get('error'):raise ValueError('Successful result also declares error')
            items.append({'address':seed['address'],'state':state,'error':value.get('error')})
        except Exception as failure:
            items.append({'address':seed['address'],'state':'invalid','error':str(failure)})
    return items


def group_members(group_id):
    result=subprocess.run(['ps','-axo','pid=,pgid=,rss=,lstart='],capture_output=True,text=True,check=True)
    members={}
    for line in result.stdout.splitlines():
        parts=line.strip().split(None,3)
        if len(parts)==4 and int(parts[1])==group_id:
            members[int(parts[0])]={'started':parts[3],'rss_bytes':int(parts[2])*1024}
    return members


def capture_group(process,owned):
    members=group_members(process.pid)
    anchor=(process.poll() is None and process.pid in members) or any(
        pid in owned and row['started']==owned[pid] for pid,row in members.items())
    if anchor:
        for pid,row in members.items():owned[pid]=row['started']
    return members,anchor


def stop_group(process,owned=None):
    owned={} if owned is None else owned
    members={}
    for sig in (signal.SIGTERM,signal.SIGKILL):
        # Revalidate immediately before each signal, including escalation.
        members,anchor=capture_group(process,owned)
        if not members:return {'cleaned':True,'survivors':[]}
        if not anchor:return {'cleaned':False,'reason':'Group identity unproven; signal refused','survivors':list(members)}
        try:os.killpg(process.pid,sig)
        except ProcessLookupError:pass
        until=time.monotonic()+3
        while time.monotonic()<until:
            # Reap only this known child; descendants are independently checked.
            process.poll()
            members,anchor=capture_group(process,owned)
            if not members:return {'cleaned':True,'survivors':[]}
            if not anchor:return {'cleaned':False,'reason':'Remaining group identity changed; escalation refused','survivors':list(members)}
            time.sleep(.1)
    return {'cleaned':False,'reason':'Owned group survived bounded cleanup','survivors':list(members)}


def supervise(process,output,owned,timeout=600):
    started=time.monotonic()
    with (output/'resources.jsonl').open('x') as stream:
        while True:
            members,anchor=capture_group(process,owned)
            if members and not anchor:raise RuntimeError('Resource monitor lost group identity')
            free=shutil.disk_usage(output).free;rss=sum(row['rss_bytes'] for row in members.values())
            sample={'elapsed_seconds':time.monotonic()-started,'free_disk_bytes':free,'group_rss_bytes':rss,'members':members}
            stream.write(json.dumps(sample)+'\n');stream.flush();os.fsync(stream.fileno())
            if free<3*1024**3:raise RuntimeError('Targeted disk reserve crossed 3GiB floor')
            if rss>6*1024**3:raise RuntimeError('Targeted process-group RSS exceeded 6GiB')
            if time.monotonic()-started>=timeout:raise subprocess.TimeoutExpired(process.args,timeout)
            try:return process.wait(timeout=1)
            except subprocess.TimeoutExpired:pass


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--ghidra',type=Path,default=Path('/opt/homebrew/opt/ghidra/libexec'))
    parser.add_argument('--jdk',type=Path,default=Path('/opt/homebrew/Cellar/openjdk@21/21.0.12.1/libexec/openjdk.jdk/Contents/Home'))
    parser.add_argument('--execute',action='store_true',help='Launch only after coordinator fallback trigger and watchdog setup')
    args=parser.parse_args();output=args.output.resolve()
    settings,command,method=plan(json.loads(args.config.read_text()),output,args.ghidra.resolve(),args.jdk.resolve())
    if not args.execute:
        print(json.dumps({'prepared_only':True,'settings':settings,'command':command},indent=2));return
    output.mkdir(parents=True,exist_ok=False);(output/'method').mkdir();(output/'project').mkdir();(output/'java-home').mkdir();(output/'java-tmp').mkdir()
    shutil.copyfile(method,output/'method/SelectedNativeExport.java');shutil.copyfile(__file__,output/'method/run_targeted_native.py')
    write_json(output/'run.json',settings);write_json(output/'command.json',command)
    env={**os.environ,'JAVA_HOME':str(args.jdk.resolve()),'PATH':str(args.jdk.resolve()/'bin')+os.pathsep+os.environ.get('PATH',''),
        'GHIDRA_HEADLESS_MAXMEM':'4G','GHIDRA_JAVA_OPTIONS':'','GHIDRA_HEADLESS_JAVA_OPTIONS':'',
        'JDK_JAVA_OPTIONS':f'-Duser.home="{output / "java-home"}" -Djava.io.tmpdir="{output / "java-tmp"}"'}
    started=time.monotonic();process=None;owned={};status={'executed':True,'profile':PROFILE}
    def interrupted(signum,frame):raise KeyboardInterrupt(f'Signal {signum}')
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    try:
        with (output/'headless.log').open('xb') as log:
            process=subprocess.Popen(command,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            write_json(output/'process.json',{'driver_pid':os.getpid(),'process_group_id':process.pid,'command':command})
            status['exit_code']=supervise(process,output,owned,timeout=600)
    except (subprocess.TimeoutExpired,KeyboardInterrupt,RuntimeError) as failure:
        status['error']=str(failure);status['interrupted']=True
        # Cleanup and sealing happen together in finally.
    finally:
        try:status['cleanup']=stop_group(process,owned) if process is not None else {'cleaned':True,'survivors':[]}
        except Exception as failure:status['cleanup']={'cleaned':False,'reason':str(failure),'survivors':'unknown'}
        status['elapsed_seconds']=time.monotonic()-started;status['items']=outcomes(output,settings['seeds'],settings)
        write_json(output/'run-status.json',status)
        if status['cleanup']['cleaned']:
            write_json(output/'manifest.json',{str(p.relative_to(output)):digest(p) for p in sorted(output.rglob('*')) if p.is_file()})
        else:write_json(output/'manifest-pending.json',{'reason':'Cleanup unverified; mutable logs are not sealed','cleanup':status['cleanup']})
    print(json.dumps(status,indent=2))
    if not status['cleanup']['cleaned'] or status.get('exit_code')!=0 or any(v['state'] not in ('exported','exported-with-warnings') for v in status['items']):raise SystemExit(1)

if __name__=='__main__':main()
