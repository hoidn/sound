"""Fixed Corpus x86 two-entry STATIC analysis driver. No guest/original execution."""
from pathlib import Path
import datetime, hashlib, json, os, resource, shutil, signal, subprocess, sys, time
ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
PRE=BASE/'depth-corpus-x86-selected-entry-preparation-r6'
GHIDRA=Path('/home/ollie/.local/opt/ghidra_12.1.4_PUBLIC')
JDK=Path('/home/ollie/.local/opt/jdk-21.0.12.1+1')
METHOD=PRE/'CorpusX86SelectedExport.java'
PROFILE='corpus-x86-two-entry-noanalysis-v1'
ACTUAL_SHA='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
FIXTURE_SHA='7b8b11955de655b259787b79c80cd61a19c851ec2fcb137d8aa3b276e0783719'
SEEDS=[{'address':'0x23b0','window_bytes':4096,'label':'_CreateInstanceU','source':'Root-fixed address nomination; fixture shares address only, not original behavior.'},
       {'address':'0x85e0','window_bytes':4096,'label':'nominal-processing-candidate-0x85e0','source':'Root-fixed address nomination; fixture shares address only, not original behavior.'}]

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def identity(path):return dict(path=str(path),bytes=path.stat().st_size,sha256=digest(path))
def write_json(path,value):
 with path.open('x') as f:json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def no_core():resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def destination(mode):
 if mode not in ('fixture','actual'):raise ValueError('Only fixture/actual modes')
 return BASE/('depth-corpus-x86-selected-entry-'+mode+'-r6')
def selection_path(mode):return BASE/'reviews'/('corpus-x86-selected-entry-'+mode+'-r6-selected-execution')/'selection.json'
def expected_config(mode):
 common=dict(schema=1,profile=PROFILE,architecture='x86_64',language='x86:LE:64:default',compiler='gcc',image_base='0x0',ghidra_version='12.1.4',
  seeds=SEEDS,auto_analysis=False,incremental_code_analysis=False,decompile_timeout_seconds=60,overall_timeout_seconds=180,
  java_heap='4G',disk_reserve_bytes=3*1024**3,group_rss_limit_bytes=6*1024**3,cpu=2)
 if mode=='fixture':
  common.update(target_sha256=FIXTURE_SHA,source=dict(kind='analyst-owned-fixture',path=str(PRE/'synthetic-corpus-x86.macho'),bytes=65536,sha256=FIXTURE_SHA))
 elif mode=='actual':
  common.update(target_sha256=ACTUAL_SHA,source=dict(kind='universal-x86-slice',path='/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Corpus.bundle/Contents/MacOS/Corpus',
   bytes=527152,sha256='2164ec08805b35f1571687a08b7ce7df9831102981f0e2fdbd07719dbf3ef422',offset=16384,length=250352))
 else:raise ValueError('Unknown mode')
 return common

def validate_config(config,mode,output):
 if config!=expected_config(mode):raise ValueError('Only fixed target/source/identity/ordered-entry/window/resource config selected')
 for key in ('schema','decompile_timeout_seconds','overall_timeout_seconds','disk_reserve_bytes','group_rss_limit_bytes','cpu'):
  if type(config[key]) is not int:raise ValueError('Integer protocol field required')
 if config['auto_analysis'] is not False or config['incremental_code_analysis'] is not False:raise ValueError('Analysis flags must be booleanfalse')
 if any(type(seed['window_bytes']) is not int for seed in config['seeds']):raise ValueError('Integer bytewindow required')
 if any(type(config['source'][key]) is not int for key in ('bytes','offset','length') if key in config['source']):raise ValueError('Integer source range required')
 if output!=destination(mode) or output.exists() or output.is_symlink():raise ValueError('Only absent exclusive new output selected')
 if any(c in str(output) for c in ('\"',"'",'\n','\r','\\')) or any(part.startswith('.') for part in output.parts):raise ValueError('Unsafe JVM/project path')
 return config

def command(output):
 return [str(GHIDRA/'support/analyzeHeadless'),str(output/'project'),'CorpusX86Selected','-import',str(output/'input/Corpus.x86_64'),
  '-readOnly','-deleteProject','-noanalysis','-max-cpu','2','-log',str(output/'ghidra.log'),'-scriptlog',str(output/'script.log'),
  '-scriptPath',str(output/'method'),'-postScript',str(output/'method/CorpusX86SelectedExport.java'),str(output/'run.json'),str(output)]

def validate_command(argv,output):
 if argv!=command(output) or argv.count('-noanalysis')!=1 or '-analysis' in argv:raise ValueError('Only fixed noanalysis command selected')

def verify_selection(mode,seal,selection_sha):
 path=selection_path(mode)
 if digest(path)!=selection_sha:raise ValueError('Root selection identity mismatch')
 chosen=json.loads(path.read_text())
 if chosen['mode']!=mode or chosen['preparation']['sha256']!=seal:raise ValueError('Wrong selected mode/preparation')
 for key in ['preparation','driver','root_preflight','peer_preflight']:
  if identity(Path(chosen[key]['path']))!=chosen[key]:raise ValueError('Selection/preflight pin changed')
 if chosen['driver']!=identity(Path(__file__).resolve()):raise ValueError('Wrong selected driver')
 if mode=='actual':
  if chosen.get('fixture_independently_approved') is not True:raise ValueError('Actual requires separately approved fixture')
  for key in ['fixture_manifest','fixture_actual_review']:
   if identity(Path(chosen[key]['path']))!=chosen[key]:raise ValueError('Fixture approval pin changed')
  f=destination('fixture');manifest=json.loads((f/'manifest.json').read_text())
  if chosen['fixture_manifest']!=identity(f/'manifest.json'):raise ValueError('Wrong fixture manifest')
  for row in manifest['files']:
   got=identity(f/row['path'])
   if (got['bytes'],got['sha256'])!=(row['bytes'],row['sha256']):raise ValueError('Fixture payload changed')
  status=json.loads((f/'run-status.json').read_text())
  if status['preparation_sha256']!=seal or status.get('exit_code')!=0 or status.get('error') or not status['cleanup']['cleaned'] or len(status['items'])!=2 or any(x['state'] not in ('exported','exported-with-warnings') for x in status['items']):
   raise ValueError('Exact current fixture did not succeed')
 return chosen

def source_bytes(config):
 src=config['source'];p=Path(src['path'])
 if identity(p)!=dict(path=str(p),bytes=src['bytes'],sha256=src['sha256']):raise ValueError('Pinned source changed')
 raw=p.read_bytes()
 if src['kind']=='universal-x86-slice':raw=raw[src['offset']:src['offset']+src['length']]
 if hashlib.sha256(raw).hexdigest()!=config['target_sha256']:raise ValueError('Thin target mismatch')
 return raw

def outcomes(output,seeds,settings,mode):
 items=[]
 for i,seed in enumerate(seeds):
  p=output/'functions'/seed['address']/'metadata.json'
  try:
   if digest(output/'method/CorpusX86SelectedExport.java')!=settings['method_sha256']:raise ValueError('Captured method changed')
   actual=json.loads((output/'actual-identity.json').read_text())
   fixed=dict(executable_sha256=settings['target_sha256'],language='x86:LE:64:default',compiler='gcc',ghidra_version='12.1.4',java_version='21.0.12.1',max_heap=4294967296,processors=2,default_pool=2,java_home=str(JDK),user_home=str(output/'java-home'),tmp=str(output/'java-tmp'),auto_analysis=False)
   if any(actual.get(k)!=v for k,v in fixed.items()) or int(actual['image_base'],16)!=0:raise ValueError('Actual effective identity missing or different')
   value=json.loads(p.read_text());expected=dict(address=seed['address'],seed=seed,profile=PROFILE,target_sha256=settings['target_sha256'],provider='ghidra-headless-selected-script',ghidra_version='12.1.4',method_sha256=settings['method_sha256'])
   if any(value.get(k)!=v for k,v in expected.items()):raise ValueError('Result identity/profile mismatch')
   state=value.get('state')
   if state not in ('exported','exported-with-warnings','failed'):raise ValueError('Unknown state')
   if state!='failed':
    if value.get('error') or value.get('partial_code') or not value.get('body_ranges') or value.get('body_bytes',0)<=0 or value.get('instruction_count',0)<=0:raise ValueError('Invalid success/body evidence')
    if not all((p.parent/n).is_file() and (p.parent/n).stat().st_size>0 for n in ('assembly.txt','pseudocode.c')):raise ValueError('Missing successful payload')
    if mode=='fixture':
     size=(6,3)[i];start=int(seed['address'],16)
     if value['body_bytes']!=size or value['instruction_count']!=2 or value['body_ranges']!=[dict(start=hex(start),end=hex(start+size-1))]:raise ValueError('Synthetic body differs from known two-instruction fixture')
   items.append(dict(address=seed['address'],state=state,error=value.get('error')))
  except Exception as error:items.append(dict(address=seed['address'],state='invalid',error=type(error).__name__+': '+str(error)))
 return items


def group_members(group_id):
    result=subprocess.run(['/usr/bin/ps','-axo','pid=,pgid=,rss=,lstart='],capture_output=True,text=True,check=True,timeout=3,env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C'})
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

def supervise(process,output,owned,timeout=180):
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
 if len(sys.argv)!=4 or sys.argv[1] not in ('fixture','actual') or not sys.dont_write_bytecode:
  raise SystemExit('Root-selected python -B driver.py fixture|actual PREPARATION_SHA SELECTION_SHA only')
 mode,seal,selection_sha=sys.argv[1:];output=destination(mode)
 if digest(PRE/'manifest-preparation.json')!=seal:raise ValueError('Preparation seal mismatch')
 manifest=json.loads((PRE/'manifest-preparation.json').read_text())
 if {r['path'] for r in manifest['files']}!={p.name for p in PRE.iterdir() if p.is_file() and p.name!='manifest-preparation.json'}:raise ValueError('Preparation inventory changed')
 for row in manifest['files']:
  got=identity(PRE/row['path'])
  if (got['bytes'],got['sha256'])!=(row['bytes'],row['sha256']):raise ValueError('Preparation payload changed')
 config=validate_config(json.loads((PRE/(mode+'-config.json')).read_text()),mode,output)
 # This gate precedes source_bytes: actual guest slice cannot be extracted before the independently reviewed fixture.
 chosen=verify_selection(mode,seal,selection_sha)
 inputs=json.loads((PRE/'inputs.json').read_text())
 for row in inputs['pins']:
  if identity(Path(row['path']))!=row:raise ValueError('Input/tool/source pin changed')
 if shutil.disk_usage(output.parent).free<3*1024**3:raise ValueError('Disk below3GiB prelaunch floor')
 properties=(GHIDRA/'Ghidra/application.properties').read_text()
 if 'application.version=12.1.4' not in properties.splitlines():raise ValueError('Ghidra installed version metadata mismatch')
 watched=sorted({Path(row['path']) for row in inputs['pins']}|{p for p in PRE.iterdir() if p.is_file()}|{selection_path(mode)})
 before=[identity(p) for p in watched]
 output.mkdir(exist_ok=False)
 status=dict(started_utc=utc(),mode=mode,preparation_sha256=seal,tool_attempts=0,returned_pid=None,exit_code=None,error=None,guest_execution=False,automatic_retry=False)
 process=None;owned={};started=time.monotonic()
 def interrupted(signum,frame):raise KeyboardInterrupt('Signal '+str(signum))
 try:
  signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
  write_json(output/'before-map.json',before)
  for n in ['method','project','java-home','java-tmp','ghidra-config','ghidra-cache','input']:(output/n).mkdir()
  target=output/'input/Corpus.x86_64'
  with target.open('xb') as f:f.write(source_bytes(config));f.flush();os.fsync(f.fileno())
  shutil.copyfile(METHOD,output/'method/CorpusX86SelectedExport.java');shutil.copyfile(__file__,output/'method/run-selected.py')
  settings={**config,'preparation_sha256':seal,'target':str(target),'method_sha256':digest(METHOD),'jdk':str(JDK),'user_home':str(output/'java-home'),'tmp':str(output/'java-tmp')}
  argv=command(output);validate_command(argv,output)
  write_json(output/'run.json',settings);write_json(output/'command.json',argv)
  env={'PATH':str(JDK/'bin')+':/usr/bin:/bin','JAVA_HOME':str(JDK),'HOME':str(output/'java-home'),'LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC',
   'XDG_CONFIG_HOME':str(output/'ghidra-config'),'XDG_CACHE_HOME':str(output/'ghidra-cache'),'GHIDRA_HEADLESS_MAXMEM':'4G',
   'GHIDRA_JAVA_OPTIONS':'','GHIDRA_HEADLESS_JAVA_OPTIONS':'-Dcpu.core.override=2',
   'JDK_JAVA_OPTIONS':'-XX:ActiveProcessorCount=2 -Dcpu.core.override=2 -Dcpu.core.limit=2 -Duser.home='+str(output/'java-home')+' -Djava.io.tmpdir='+str(output/'java-tmp')}
  write_json(output/'invocation-before.json',dict(utc=utc(),argv=argv,cwd=str(output),environment=env,core_limit=[0,0],stdin='DEVNULL',overall_timeout_seconds=180,per_entry_seconds=60,start_new_session=True,guest_execution=False))
  status['tool_attempts']=1;write_json(output/'attempt.json',dict(utc=utc(),attempt=1,argv=argv))
  with (output/'headless.stdout').open('xb') as stdout,(output/'headless.stderr').open('xb') as stderr:
   process=subprocess.Popen(argv,cwd=output,env=env,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,preexec_fn=no_core,start_new_session=True)
   status['returned_pid']=process.pid
   write_json(output/'process.json',dict(utc=utc(),driver_pid=os.getpid(),process_group_id=process.pid,argv=argv))
   status['exit_code']=supervise(process,output,owned,timeout=180)
 except BaseException as error:
  status['error']=type(error).__name__+': '+str(error)
 finally:
  try:status['cleanup']=stop_group(process,owned) if process is not None else dict(cleaned=True,survivors=[])
  except Exception as error:status['cleanup']=dict(cleaned=False,survivors='unknown',error=str(error))
  status['finished_utc']=utc();status['elapsed_seconds']=time.monotonic()-started;status['items']=outcomes(output,config['seeds'],settings,mode) if 'settings' in locals() else []
  if process is not None:status['exit_code']=process.returncode
  after=[]
  for p in watched:
   try:after.append(identity(p))
   except Exception as error:after.append(dict(path=str(p),error=str(error)))
  status['providers_unchanged']=before==after
  write_json(output/'after-map.json',dict(files=after,unchanged=before==after));write_json(output/'run-status.json',status)
  if status['cleanup']['cleaned']:
   files=[]
   for p in sorted(output.rglob('*')):
    if p.is_file():r=identity(p);files.append(dict(path=str(p.relative_to(output)),bytes=r['bytes'],sha256=r['sha256']))
   write_json(output/'manifest.json',dict(files=files,guest_execution=False,mode=mode,preparation_sha256=seal))
  else:write_json(output/'manifest-pending.json',dict(cleanup=status['cleanup'],not_sealed=True))
 print(json.dumps(status,indent=2))
 return 0 if status['cleanup']['cleaned'] and status.get('exit_code')==0 and not status['error'] and status['providers_unchanged'] and len(status['items'])==2 and all(x['state'] in ('exported','exported-with-warnings') for x in status['items']) else 1
if __name__=='__main__':raise SystemExit(main())
