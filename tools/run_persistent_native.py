#!/usr/bin/env python3
"""Analyst-only, separately profiled and resource-bounded Ghidra checkpoints.

Never executes imported native bytes. Every headless launch starts -noanalysis;
a verified machine handshake is the only path to enabling the finite pass.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import ctypes
from contextlib import contextmanager
from functools import wraps
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from types import MappingProxyType
import uuid

GIB = 1024 ** 3
TARGET_SHA = '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
FIXTURE_BYTES = bytes.fromhex('00008052c0035fd6') # mov w0,#0; ret (data only)
FIXTURE_SHA = hashlib.sha256(FIXTURE_BYTES).hexdigest()
GHIDRA = Path('/opt/homebrew/Cellar/ghidra/12.1.4/libexec')
NATIVE_DECOMPILER=GHIDRA/'Ghidra/Features/Decompiler/os/mac_arm_64/decompile'
JDK = Path('/opt/homebrew/Cellar/openjdk@21/21.0.12.1/libexec/openjdk.jdk/Contents/Home')
LAUNCH_SHA = '302880328a0024ee24cfe0326d4d9a61c2237116d95f2e0e0df090f747f95e30'
SCRIPT_ROOT = Path(__file__).resolve().parent / 'ghidra'
_PROFILE_COMMON = MappingProxyType({'schema':1,'ghidra':'12.1.4','compiler':'default','heap_bytes':4*GIB,
           'processors':2,'pool':2,'jdk_version':'21.0.12.1','start_attach_listener':True,'analysis_seconds':900,'decompile_seconds':60,
           'ordinary_process_reanalyzes_all':True,'default_rea_corpus_merge':False})
# Installed Mach-O opinions select AppleSilicon; BinaryLoader raw fixtures are
# explicitly generic v8A. These are different languages and compiler semantics.
TARGET_PROFILE = MappingProxyType({**_PROFILE_COMMON,'id':'ghidra-persistent-bounded-analysis-apple-silicon-v2',
           'input_format':'mach-o-arm64','language':'AARCH64:LE:64:AppleSilicon'})
FIXTURE_PROFILE = MappingProxyType({**_PROFILE_COMMON,'id':'ghidra-persistent-bounded-analysis-raw-arm64-fixture-v2',
           'input_format':'raw-arm64-fixture','language':'AARCH64:LE:64:v8A'})
SCRIPT_NAMES = ('RecoverySupport.java','RecoveryLaunchGate.java','RecoveryAnalysisOutcome.java',
                'RecoveryNativeExport.java','RecoveryFixtureSetup.java','RecoveryFixtureTimeout.java',
                'RecoveryFixtureCounter.java','RecoveryFixtureExpand.java')
_JOB_CONTEXT=threading.local()


def job_tick():
    guard=getattr(_JOB_CONTEXT,'guard',None)
    if guard:guard.check()


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for data in iter(lambda:f.read(1024*1024),b''):job_tick();h.update(data)
    return h.hexdigest()


def decode_json(text):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result: raise ValueError('duplicate JSON key: '+key)
            result[key]=value
        return result
    return json.loads(text,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))


def read_json(path):
    path=Path(path); no_symlinks(path)
    if path.stat().st_size>16*1024*1024: raise ValueError('oversized JSON')
    return decode_json(path.read_text(encoding='utf-8'))


def publish(path,value):
    """Atomic exclusive publication. Existing captures are never replaced."""
    job_tick();path=Path(path); no_symlinks(path.parent)
    data=(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
    temporary=path.with_name('.'+path.name+'.'+uuid.uuid4().hex)
    with temporary.open('xb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
    try:
        os.link(temporary,path) # CREATE_NEW semantics at the publication point
        fd=os.open(path.parent,os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)
    finally: temporary.unlink()


def no_symlinks(path):
    path=Path(path).absolute()
    for part in (path,*path.parents):
        if part.is_symlink(): raise ValueError('symlink path: '+str(part))
    return path


def fresh(path):
    path=no_symlinks(path); path.mkdir(parents=False,exist_ok=False); return path


def allocated_tree(root):
    root=Path(root); total=0; seen=set()
    for p in (root,*root.rglob('*')):
        try: st=p.lstat()
        except FileNotFoundError: continue # transient owned output rename
        if p.is_symlink(): raise ValueError('symlink in owned tree')
        key=(st.st_dev,st.st_ino)
        if key not in seen: total+=st.st_blocks*512; seen.add(key)
    return total


def project_snapshot(root):
    root=no_symlinks(root)
    if not (root/'recover.gpr').is_file() or not (root/'recover.rep').is_dir():
        raise ValueError('missing closed project pair')
    files=[]
    for p in sorted(root.rglob('*')):
        job_tick()
        no_symlinks(p)
        if p.name.endswith('.lock') or p.name.endswith('.lock~'): raise ValueError('unresolved project lock')
        if p.is_file():
            st=p.stat(); files.append({'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':st.st_size,'allocated_bytes':st.st_blocks*512})
        elif not p.is_dir(): raise ValueError('nonregular project member')
    return {'schema':1,'files':files,'logical_bytes':sum(p['bytes'] for p in files),'allocated_bytes':allocated_tree(root)}


def verify_project(root,manifest):
    actual=project_snapshot(root)
    if [(x['path'],x['sha256'],x['bytes']) for x in actual['files']] != [(x['path'],x['sha256'],x['bytes']) for x in manifest['files']]:
        raise ValueError('checkpoint members changed')
    return actual


def copy_project(source,destination,manifest,*,budget_root=None,budget_limit=None):
    job_tick()
    source=no_symlinks(source); destination=no_symlinks(destination)
    verify_project(source,manifest)
    if destination.exists(): raise FileExistsError(destination)
    planned=manifest['allocated_bytes']+64*1024*1024
    if shutil.disk_usage(destination.parent).free<planned+3*GIB:raise ValueError('copy disk admission above floor failed')
    if budget_root is not None and allocated_tree(budget_root)+planned>budget_limit:raise ValueError('whole job copy allocation budget failed')
    shutil.copytree(source,destination,copy_function=shutil.copy2,symlinks=False)
    job_tick()
    verify_project(destination,manifest); verify_project(source,manifest)
    if budget_root is not None and allocated_tree(budget_root)>budget_limit:raise ValueError('whole job actual copy allocation exceeded')
    return destination


def required_free(mode,baseline=0):
    return max(12*GIB,2*baseline+8*GIB) if mode=='analyze' else 6*GIB


def required_peak_free(mode,baseline=0):
    # Four retained project representations, each with 2 GiB growth; logs/tmp and
    # disk floor plus a separate 64 MiB publication reserve for each copy.
    return max(required_free(mode,baseline),4*baseline+12*GIB+256*1024*1024) if mode=='analyze' else required_free(mode,baseline)


class ResourcePolicy:
    def __init__(self,*,rss_limit=6*GIB,disk_floor=3*GIB,allocation_limit=2*GIB,deadline=600):
        self.rss_limit=rss_limit; self.disk_floor=disk_floor; self.allocation_limit=allocation_limit; self.deadline=deadline; self.hits=0
    def observe(self,elapsed,rss,free,allocated):
        self.hits=self.hits+1 if rss>self.rss_limit else 0
        if free<self.disk_floor: return 'disk-floor'
        if allocated>self.allocation_limit: return 'allocation-limit'
        if self.hits>=2: return 'rss-limit'
        if elapsed>self.deadline: return 'external-deadline'
        return None


class JobGuard:
    """Main-thread cancellation and disk/allocation monitoring across Python phases.

    The final part of the declared deadline is reserved for bounded owned-child
    cleanup. SIGALRM also interrupts non-JVM waits; hash/copy boundaries check
    the same guard. Cleanup is protected, and a late job can never commit.
    """
    def __init__(self,root,seconds):
        if seconds<=0:raise ValueError('positive whole-job deadline required')
        self.root=no_symlinks(root);self.started=time.monotonic();self.seconds=seconds
        self.cleanup_reserve=min(32,seconds/4) if seconds<128 else 32
        self.period=min(1,max(.01,(seconds-self.cleanup_reserve)/4))
        self.next_sample=self.started;self.samples=[];self.paused=0;self.checking=False;self.committed=False;self.stop_reason=None;self.owns_root=False
        self.policy=ResourcePolicy(allocation_limit=2*GIB,deadline=seconds-self.cleanup_reserve)
    def __enter__(self):
        if threading.current_thread() is not threading.main_thread() or getattr(_JOB_CONTEXT,'guard',None):raise RuntimeError('whole-job guard requires an unguarded main thread')
        self.previous_timer=signal.getitimer(signal.ITIMER_REAL)
        if self.previous_timer!=(0.0,0.0):raise RuntimeError('another real-time alarm is already active')
        self.previous_handler=signal.getsignal(signal.SIGALRM)
        signal.signal(signal.SIGALRM,self.alarm);_JOB_CONTEXT.guard=self
        signal.setitimer(signal.ITIMER_REAL,self.period,self.period)
        return self
    def alarm(self,sig,frame):self.check(force=True)
    def check(self,*,force=False):
        if self.paused or self.committed:return
        now=time.monotonic()
        if now-self.started>=self.seconds-self.cleanup_reserve:
            self.stop_reason='whole-job-deadline-cleanup-reserve';raise RuntimeError(self.stop_reason)
        if self.checking or (not force and now<self.next_sample):return
        self.checking=True
        try:
            root=self.root if self.root.exists() else self.root.parent
            free=shutil.disk_usage(root).free;allocated=allocated_tree(self.root) if self.root.exists() else 0
            admission=self.root/'admission.json'
            if admission.is_file():self.policy.allocation_limit=read_json(admission)['allocation_limit_bytes']
            periodic=now>=self.next_sample
            rss=None
            if periodic:
                self.next_sample=now+1
                own=process_table().get(os.getpid())
                if own is None:raise RuntimeError('controller RSS identity unavailable')
                rss=own['rss_bytes'];reason=self.policy.observe(now-self.started,rss,free,allocated)
            else:reason='disk-floor' if free<3*GIB else ('allocation-limit' if allocated>self.policy.allocation_limit else None)
            self.samples.append({'elapsed':now-self.started,'free':free,'allocated_bytes':allocated,'controller_rss_bytes':rss,'periodic':periodic})
            if reason:self.stop_reason='whole-job-'+reason;raise RuntimeError(self.stop_reason)
        finally:self.checking=False
    def report(self,status):
        return {'schema':1,'status':status,'started_monotonic':self.started,'deadline_seconds':self.seconds,'cleanup_reserve_seconds':self.cleanup_reserve,
                'duration_seconds':time.monotonic()-self.started,'stop_reason':self.stop_reason,'samples':self.samples}
    def prepare_commit(self,job):
        self.check(force=True);publish(Path(job)/'job-monitor.json',self.report('checked-before-commit'));self.check(force=True)
        check_job(job)
        # The final filesystem action is guard removal. No alarm can raise
        # between that commit and returning the committed result.
        signal.setitimer(signal.ITIMER_REAL,0)
    def __exit__(self,kind,error,tb):
        try:
            if error is not None and self.owns_root and self.root.is_dir() and (self.root/'.incomplete').exists():
                try:publish(self.root/'job-monitor-failure.json',{**self.report('fail'),'error':repr(error)})
                except (OSError,ValueError,RuntimeError):pass # Deadline cancellation may leave the report absent; the guard rejects this job.
        finally:
            signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,self.previous_handler);_JOB_CONTEXT.guard=None
        return False


def bounded_job(mode):
    def decorate(fn):
        @wraps(fn)
        def run(output,*args,**kwargs):
            seconds=90 if kwargs.get('fixture',False) else (1200 if mode=='analyze' else 600)
            with JobGuard(output,seconds) as guard:
                result=fn(output,*args,**kwargs)
                if not guard.committed:raise RuntimeError('job returned without its final commit')
                return result
        return run
    return decorate


def check_job(job):
    """Strict deadline/resource boundary, including standalone commit helpers."""
    job=Path(job);admission=read_json(job/'admission.json')
    if time.monotonic()-admission['started_monotonic']>=admission['job_deadline_seconds']:raise RuntimeError('whole-job-deadline')
    if shutil.disk_usage(job).free<3*GIB:raise RuntimeError('whole-job-disk-floor')
    if allocated_tree(job)>admission['allocation_limit_bytes']:raise RuntimeError('whole-job-allocation-limit')
    job_tick()


class _BSD(ctypes.Structure):
    _fields_=[(n,ctypes.c_uint32) for n in ('flags','status','xstatus','pid','ppid','uid','gid','ruid','rgid','svuid','svgid','rfu')]+[
        ('comm',ctypes.c_char*16),('name',ctypes.c_char*32)]+[(n,ctypes.c_uint32) for n in ('nfiles','pgid','jobc','tdev','tpgid')]+[
        ('nice',ctypes.c_int32),('start_sec',ctypes.c_uint64),('start_usec',ctypes.c_uint64)]
_LIBPROC=None


def process_identity(pid):
    """PID, microsecond creation identity, group and executable from libproc."""
    global _LIBPROC
    if sys.platform!='darwin': raise RuntimeError('actual ownership requires macOS libproc')
    if _LIBPROC is None: _LIBPROC=ctypes.CDLL('/usr/lib/libproc.dylib',use_errno=True)
    info=_BSD(); n=_LIBPROC.proc_pidinfo(int(pid),3,0,ctypes.byref(info),ctypes.sizeof(info))
    if n!=ctypes.sizeof(info): return None
    executable=ctypes.create_string_buffer(4096)
    length=_LIBPROC.proc_pidpath(int(pid),executable,4096)
    return {'pid':int(pid),'ppid':info.ppid,'pgid':info.pgid,'start_us':info.start_sec*1000000+info.start_usec,
            'exe':executable.value.decode('utf-8',errors='strict') if length>0 else None,'status':info.status,'sid':process_session(int(pid))}


def process_session(pid):
    try:return os.getsid(pid)
    except ProcessLookupError:return None


def same_identity(left,right):
    return bool(left and right and all(left[k]==right[k] for k in ('pid','start_us','pgid')) and ('sid' not in left or left['sid']==right.get('sid')))


def signal_matching(identity,sig):
    if not same_identity(identity,process_identity(identity['pid'])): return False
    try: os.kill(identity['pid'],sig)
    except ProcessLookupError: return False
    return True


def process_table():
    result=subprocess.run(['/bin/ps','-axo','pid=,rss='],capture_output=True,text=True,timeout=3,check=True)
    table={}
    for line in result.stdout.splitlines():
        pid,rss=map(int,line.split()); identity=process_identity(pid)
        if identity: identity['rss_bytes']=rss*1024; table[pid]=identity
    return table


@contextmanager
def defer_launch_signals():
    """Finish Popen construction and registration before main-thread cancellation.

    Callable handlers queue signals; they neither block nor ignore them in the
    child. Exec resets caught handlers normally. Worker-thread launches cannot
    receive Python signal exceptions and are serialized with cleanup by Owner.
    Deferred default termination becomes an exception so owned cleanup can run.
    """
    pending=[]
    if threading.current_thread() is not threading.main_thread():
        yield pending;return
    previous={sig:signal.getsignal(sig) for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGALRM)}
    def queue(sig,frame):pending.append(sig)
    try:
        for sig in previous:signal.signal(sig,queue)
        yield pending
    finally:
        for sig,handler in previous.items():signal.signal(sig,handler)
        for sig in pending:
            handler=previous[sig]
            if handler==signal.SIG_IGN:continue
            if callable(handler):handler(sig,None)
            else:raise RuntimeError('owned-launch-cancelled-signal-'+str(sig))


class Owner:
    def __init__(self):
        self.identities={}; self.roots={}; self.processes=[];self.pending={};self.launch_windows={}; self.lock=threading.RLock(); self.gaps=[];self.closing=False
    def launch(self,argv,*,stdout,stderr,env=None):
        with self.lock,defer_launch_signals() as deferred:
            if self.closing:raise RuntimeError('owned cleanup already started')
            before=time.time_ns()//1000
            p=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,env=env,start_new_session=True)
            # Registration precedes every identity lookup or operation that can fail.
            self.processes.append(p)
            window={'pid':p.pid,'parent_pid':os.getpid(),'before_us':before,'after_us':time.time_ns()//1000,'deferred_signals':deferred}
            self.launch_windows[p.pid]=window;self.pending[p.pid]=p
            try:identity=process_identity(p.pid)
            except BaseException as exc:
                self.gaps.append({'pid':p.pid,'reason':'initial-leader-identity-error','error':repr(exc)})
                raise
            if not self.confirm_launch(identity,window):
                self.gaps.append({'pid':p.pid,'reason':'initial-leader-identity-missing-or-unconfirmed'})
                # No unverified PID signal. A later creation-confirmed sample may
                # recover this unreaped Popen for cleanup, never for acceptance.
                raise RuntimeError('owned leader identity missing or unconfirmed')
            self.roots[p.pid]=identity;self.identities[p.pid]=identity;self.pending.pop(p.pid)
            return p
    @staticmethod
    def confirm_launch(identity,window):
        return bool(identity and identity['pid']==window['pid'] and identity['ppid']==window['parent_pid'] and
                    identity['pgid']==window['pid'] and identity.get('sid')==window['pid'] and
                    window['before_us']<=identity['start_us']<=window['after_us'])
    def sample(self):
        table=process_table()
        with self.lock:
            for pid,p in list(self.pending.items()):
                # Never poll/reap first and then adopt a potentially reused PID.
                if p.returncode is None and self.confirm_launch(table.get(pid),self.launch_windows[pid]):
                    self.roots[pid]=table[pid];self.identities[pid]=table[pid];self.pending.pop(pid)
            active={pid for pid,old in self.identities.items() if same_identity(old,table.get(pid))}
            groups={}
            for pid,old in self.roots.items():
                current=table.get(pid)
                if current and not same_identity(old,current):
                    gap={'pid':pid,'reason':'owned-leader-PID-reused'}
                    if gap not in self.gaps:self.gaps.append(gap)
                    continue
                groups[old['pgid']]=old['start_us']
            changed=True
            while changed:
                changed=False
                for pid,item in table.items():
                    if pid in active: continue
                    if item['ppid'] in active or (item['pgid'] in groups and item.get('sid',item['pgid'])==item['pgid'] and item['start_us']>=groups[item['pgid']]):
                        old=self.identities.get(pid)
                        if old and not same_identity(old,item): self.gaps.append({'pid':pid,'reason':'identity-reused'}); continue
                        self.identities[pid]=item; active.add(pid); changed=True
            return [table[pid] for pid in sorted(active)]
    def close(self):
        # Additional interrupts cannot abandon cleanup. Identity is checked per signal.
        with self.lock:self.closing=True
        handlers={};signaled=[]
        if threading.current_thread() is threading.main_thread():
            for sig in (signal.SIGINT,signal.SIGTERM): handlers[sig]=signal.signal(sig,signal.SIG_IGN)
        try:
            for sig,window in ((signal.SIGTERM,3),(signal.SIGKILL,3)):
                try:active=self.sample()
                except Exception as exc:
                    self.gaps.append({'reason':'cleanup-sampler-failure','error':repr(exc)})
                    active=list(self.identities.values())
                for identity in reversed(active):
                    if signal_matching(identity,sig):signaled.append({'pid':identity['pid'],'start_us':identity['start_us'],'signal':sig})
                until=time.monotonic()+window
                while time.monotonic()<until:
                    for p in self.processes: p.poll()
                    try:active=self.sample()
                    except Exception:active=[x for x in self.identities.values() if same_identity(x,process_identity(x['pid']))]
                    if not [x for x in active if x.get('status')!=5]: break
                    time.sleep(.1)
            for p in self.processes:
                try:p.wait(timeout=.5)
                except subprocess.TimeoutExpired:pass
            try:remaining=self.sample()
            except Exception as exc:
                self.gaps.append({'reason':'final-sampler-failure','error':repr(exc)});remaining=[x for x in self.identities.values() if same_identity(x,process_identity(x['pid']))]
            reaped=all(p.returncode is not None for p in self.processes)
            return {'closed':not remaining and not self.gaps and reaped,'survivors':remaining,'ownership_gaps':self.gaps,
                    'signaled':signaled,'reaped':reaped,'identities':list(self.identities.values()),
                    'unconfirmed_launches':[self.launch_windows[pid] for pid in self.pending],'launch_windows':list(self.launch_windows.values())}
        finally:
            for sig,handler in handlers.items(): signal.signal(sig,handler)


def lineage(record,config):
    if type(record.get('schema')) is not int or record.get('schema')!=1 or record.get('nonce')!=config['nonce'] or record.get('config_sha256')!=config['_sha']:
        raise ValueError('stale/unknown milestone lineage')


def validate_outcome(stage,config):
    out=read_json(stage/'analysis-outcome.json');lineage(out,config)
    gate=read_json(stage/'gate-report.json')
    if out.get('status')!='pass' or out.get('analysis_enabled') is not False or type(out.get('timeout')) is not bool:
        raise ValueError('invalid positive outcome')
    if out.get('gate_sha256')!=sha(stage/'gate-report.json') or out.get('complete_sha256')!=sha(stage/'gate-complete.json'):
        raise ValueError('outcome lineage hash mismatch')
    if out.get('pid')!=gate['pid'] or out.get('start_ms')!=gate['start_ms']:raise ValueError('outcome JVM identity mismatch')
    return out


def validate_milestones(stage,config,log,returncode,readonly):
    if returncode!=0: raise ValueError('nonzero headless exit')
    if 'REPORT SCRIPT ERROR:' in log or 'Script does not exist or encountered problems' in log: raise ValueError('headless script failed')
    if 'ANALYZING changes made by post scripts:' in log: raise ValueError('unbounded post-script analysis detected')
    records={}
    for name in ('gate-report','controller-ack','gate-complete','analysis-outcome'):
        path=stage/(name+'.json')
        if not path.is_file(): raise ValueError('missing positive milestone: '+name)
        record=read_json(path); lineage(record,config); records[name]=record
    gate=records['gate-report']; ack=records['controller-ack']; complete=records['gate-complete']; outcome=records['analysis-outcome']
    if any(type(record.get(field)) is not int for record in records.values() for field in ('pid','start_ms')):raise ValueError('typed PID/creation fields required')
    if type(outcome.get('timeout')) is not bool:raise ValueError('typed timeout field required')
    if gate.get('status')!='pass' or complete.get('status')!='pass' or outcome.get('status')!='pass': raise ValueError('negative milestone')
    for record in (ack,complete,outcome):
        if record.get('gate_sha256')!=sha(stage/'gate-report.json') or record.get('pid')!=gate['pid'] or record.get('start_ms')!=gate['start_ms']:
            raise ValueError('gate identity binding mismatch')
    if complete.get('ack_sha256')!=sha(stage/'controller-ack.json') or outcome.get('complete_sha256')!=sha(stage/'gate-complete.json'):
        raise ValueError('completion binding mismatch')
    if outcome.get('analysis_enabled') is not False: raise ValueError('outcome did not disable analysis')
    enabled=config['mode']=='enable-analysis-after-ack'
    if complete.get('analysis_enabled') is not enabled: raise ValueError('gate final mode differs')
    if enabled and 'ANALYZING all memory and code:' not in log: raise ValueError('analysis milestone missing')
    timed_out='REPORT: Analysis timed out at ' in log;succeeded='REPORT: Analysis succeeded for file:' in log
    if enabled and (timed_out==succeeded or outcome['timeout'] is not timed_out):raise ValueError('analysis completion/timeout milestones disagree')
    if not readonly and not re.search(r'REPORT: Save succeeded for(?: processed file)?:',log): raise ValueError('save milestone missing')
    if 'REPORT: Save failed for:' in log or 'REPORT: Error trying to save' in log: raise ValueError('save failed')
    return records


def verify_diagnostics(outputs,config):
    flags=dict(re.findall(r'-XX:(\w+)=([^\s]+)',outputs['VM.flags']))
    if flags.get('ActiveProcessorCount')!='2' or flags.get('MaxHeapSize')!=str(4*GIB): raise ValueError('effective JVM flags mismatch')
    props={}
    for line in outputs['VM.system_properties'].splitlines():
        if '=' in line:
            key,value=line.split('=',1)
            if key in props: raise ValueError('duplicate diagnostic property')
            props[key]=value
    expected={'cpu.core.override':'2','cpu.core.limit':'2','user.home':config['home'],'java.io.tmpdir':config['tmp'],
              'java.home':config['jdk'],'java.version':'21.0.12.1','sound.recovery.nonce':config['nonce']}
    if any(props.get(k)!=v for k,v in expected.items()): raise ValueError('effective JVM properties mismatch')
    cmd=outputs['VM.command_line']
    if '-Dsound.recovery.nonce='+config['nonce'] not in cmd: raise ValueError('diagnostic command-line nonce missing')
    return {'flags':flags,'properties':{k:props[k] for k in expected}}


def method_pins():
    return {'controller':sha(Path(__file__)),**{name:sha(SCRIPT_ROOT/name) for name in SCRIPT_NAMES},
            'analyzeHeadless':sha(GHIDRA/'support/analyzeHeadless'),'launch.sh':sha(GHIDRA/'support/launch.sh'),
            'java':sha(JDK/'bin/java'),'jcmd':sha(JDK/'bin/jcmd'),'native_decompiler':sha(NATIVE_DECOMPILER)}


def make_config(stage,target,*,fixture,mode,checkpoint=None,export_mode='',entries=(),inventory=None):
    stage=no_symlinks(stage); target=no_symlinks(target)
    for path in (stage,GHIDRA,JDK):
        if re.search(r'\s',str(path)): raise ValueError('whitespace in JVM paths')
    if sha(target)!=(FIXTURE_SHA if fixture else TARGET_SHA): raise ValueError('target bytes do not match selected pinned mode')
    if mode not in ('verify-only','enable-analysis-after-ack'):raise ValueError('unknown gate mode')
    pins=method_pins() if (SCRIPT_ROOT/'RecoverySupport.java').exists() else {}
    profile={**(FIXTURE_PROFILE if fixture else TARGET_PROFILE),'fixture':fixture,'analysis_seconds':1 if fixture else 900,'methods':pins}
    return {'schema':1,'nonce':uuid.uuid4().hex,'mode':mode,'profile':profile,
            'profile_sha256':hashlib.sha256(json.dumps(profile,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'target':str(target),'target_sha256':sha(target),'target_bytes':target.stat().st_size,'program_name':target.name,
            'language':profile['language'],'compiler':profile['compiler'],'ghidra_version':'12.1.4','jdk':str(JDK),
            'native_decompiler':str(NATIVE_DECOMPILER),'home':str(stage/'home'),'tmp':str(stage/'tmp'),'stage':str(stage),'fixture':fixture,
            'gate':str(stage/'gate-report.json'),'ack':str(stage/'controller-ack.json'),'complete':str(stage/'gate-complete.json'),
            'outcome':str(stage/'analysis-outcome.json'),'ack_seconds':10,'checkpoint_sha256':checkpoint or '',
            'export_mode':export_mode,'entries':list(entries),'inventory':str(inventory) if inventory else '',
            'inventory_sha256':sha(inventory) if inventory else '', 'checkpoint_partial':False,
            'methods':pins}


def launch_command(stage,config,project,*,importing=False,fixture_setup=False,fixture_timeout=False,fixture_counter=False,fixture_expand=False,gate_name='RecoveryLaunchGate.java',outcome_name='RecoveryAnalysisOutcome.java'):
    stage=Path(stage); project=Path(project)
    args=[str(GHIDRA/'support/analyzeHeadless'),str(project),'recover','-noanalysis','-max-cpu','2',
          '-scriptPath',str(stage/'scripts'),'-log',str(stage/'application.log'),'-scriptlog',str(stage/'scripts.log')]
    if importing:
        args+=['-import',config['target']]
        if config['fixture']:args+=['-loader','BinaryLoader','-processor',config['language'],'-cspec',config['compiler']]
    else:args+=['-process',config['program_name']]
    if not importing and config['mode']=='verify-only':args+=['-readOnly']
    if config['mode']=='enable-analysis-after-ack':args+=['-analysisTimeoutPerFile',str(config['profile']['analysis_seconds'])]
    script_args=[str(stage/'stage-config.json'),config.get('_sha','')]
    args+=['-preScript',gate_name,*script_args]
    if fixture_setup:args+=['-preScript','RecoveryFixtureSetup.java',*script_args]
    if fixture_expand:args+=['-preScript','RecoveryFixtureExpand.java',*script_args]
    if fixture_timeout:args+=['-preScript','RecoveryFixtureTimeout.java',*script_args]
    args+=['-postScript',outcome_name,*script_args]
    if fixture_counter:args+=['-postScript','RecoveryFixtureCounter.java',*script_args]
    if config['export_mode']:args+=['-postScript','RecoveryNativeExport.java',*script_args]
    env={'JAVA_HOME':str(JDK),'PATH':str(JDK/'bin')+':/usr/bin:/bin:/usr/sbin:/sbin',
         'TMPDIR':config['tmp'],'LANG':'en_US.UTF-8','GHIDRA_HEADLESS_MAXMEM':'4G',
         'JDK_JAVA_OPTIONS':'-Duser.home='+config['home']+' -Djava.io.tmpdir='+config['tmp'],
         'GHIDRA_HEADLESS_JAVA_OPTIONS':' '.join(('-XX:ActiveProcessorCount=2','-XX:+StartAttachListener','-Dcpu.core.override=2','-Dcpu.core.limit=2',
             '-Duser.home='+config['home'],'-Djava.io.tmpdir='+config['tmp'],'-Dsound.recovery.nonce='+config['nonce']))}
    return args,env


def attest(owner,stage,config,gate,*,ack_fault=None):
    lineage(gate,config)
    identity=process_identity(gate['pid'])
    active=owner.sample()
    if not identity or not any(same_identity(identity,x) for x in active):raise ValueError('gate JVM is not owned')
    if identity['start_us']//1000!=gate['start_ms'] or Path(identity['exe'] or '').resolve()!= (JDK/'bin/java').resolve():raise ValueError('gate JVM creation/executable mismatch')
    if gate['status']!='pass':raise ValueError('in-JVM gate failed')
    started=time.monotonic()
    def diagnostic(name):
        out=stage/(name+'.stdout.txt'); err=stage/(name+'.stderr.txt')
        with out.open('xb') as stdout,err.open('xb') as stderr:
            p=owner.launch([str(JDK/'bin/jcmd'),str(gate['pid']),name],stdout=stdout,stderr=stderr,env={'JAVA_HOME':str(JDK),'PATH':str(JDK/'bin')+':/usr/bin:/bin',
                'JDK_JAVA_OPTIONS':'-Duser.home='+config['home']+' -Djava.io.tmpdir='+config['tmp']})
            try: p.wait(timeout=4)
            except subprocess.TimeoutExpired:
                signal_matching(owner.roots[p.pid],signal.SIGKILL);p.wait(timeout=2);raise ValueError('diagnostic deadline')
        publish(stage/(name+'.result.json'),{'schema':1,'argv':[str(JDK/'bin/jcmd'),str(gate['pid']),name],
                'returncode':p.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
        if p.returncode!=0:raise ValueError('diagnostic failed: '+name)
        return name,out.read_text(encoding='utf-8')
    with ThreadPoolExecutor(max_workers=3) as pool:outputs=dict(pool.map(diagnostic,('VM.command_line','VM.flags','VM.system_properties')))
    if time.monotonic()-started>7:raise ValueError('overall diagnostics deadline')
    verified=verify_diagnostics(outputs,config)
    if not same_identity(identity,process_identity(gate['pid'])):raise ValueError('JVM identity changed during diagnostics')
    ack={'schema':1,'nonce':config['nonce'],'config_sha256':config['_sha'],'gate_sha256':sha(stage/'gate-report.json'),
         'pid':gate['pid'],'start_ms':gate['start_ms'],'status':'pass','created_ms':time.time_ns()//1000000,
         'diagnostics':{name:sha(stage/(name+'.result.json')) for name in outputs},'verified':verified}
    if ack_fault:
        if not config['fixture']:raise ValueError('ack faults unavailable on target')
        ack=ack_fault(ack)
    if ack is not None:publish(stage/'controller-ack.json',ack)
    return ack


class LogScanner:
    """Read each immutable append-only log byte once; retain only bounded milestones."""
    TOKENS=('REPORT SCRIPT ERROR:','Script does not exist or encountered problems',
            'ANALYZING changes made by post scripts:','ANALYZING all memory and code:',
            'REPORT: Analysis timed out at ','REPORT: Analysis succeeded for file:', 'REPORT: Save succeeded for:',
            'REPORT: Save succeeded for processed file:','REPORT: Save failed for:',
            'REPORT: Error trying to save')
    def __init__(self,paths):self.paths=paths;self.offsets={p:0 for p in paths};self.tails={p:b'' for p in paths};self.found=set()
    def scan(self):
        for path in self.paths:
            if not path.exists():continue
            with path.open('rb') as stream:
                stream.seek(self.offsets[path])
                while True:
                    chunk=stream.read(1024*1024)
                    if not chunk:break
                    text=(self.tails[path]+chunk).decode('utf-8',errors='replace')
                    for token in self.TOKENS:
                        if token in text:self.found.add(token)
                    self.tails[path]=(self.tails[path]+chunk)[-512:];self.offsets[path]+=len(chunk)
        return '\n'.join(sorted(self.found))


def validate_copied_methods(stage,config):
    for name in SCRIPT_NAMES:
        if sha(stage/'scripts'/name)!=config['methods'][name]:raise ValueError('copied script authority mismatch: '+name)
    for name,key in (('run_persistent_native.py','controller'),('analyzeHeadless','analyzeHeadless'),('launch.sh','launch.sh'),('java','java'),('jcmd','jcmd')):
        if sha(stage/'methods'/name)!=config['methods'][key]:raise ValueError('copied launch authority mismatch: '+name)


def run_stage(stage,project,target,*,fixture=False,mode='verify-only',importing=False,fixture_setup=False,
              fixture_timeout=False,fixture_counter=False,fixture_expanded=False,checkpoint=None,export_mode='',entries=(),inventory=None,
              gate_name='RecoveryLaunchGate.java',outcome_name='RecoveryAnalysisOutcome.java',fixture_fault=None,checkpoint_partial=False,source_profile=None,ack_fault=None,
              allocation_root=None,deadline=None):
    stage=Path(stage); no_symlinks(stage); free=shutil.disk_usage(stage.parent).free
    admission=4*GIB if fixture else (12*GIB if mode=='enable-analysis-after-ack' else 6*GIB)
    if free<admission:raise RuntimeError('fresh launch capacity: '+str(free)+' < '+str(admission))
    stage=fresh(stage); allocation_root=Path(allocation_root or stage)
    config=make_config(stage,target,fixture=fixture,mode=mode,checkpoint=checkpoint,export_mode=export_mode,entries=entries,inventory=inventory)
    if fixture_expanded and not fixture:raise ValueError('expanded fixture unavailable on target')
    config['profile']['fixture_expanded']=fixture_expanded;config['profile_sha256']=hashlib.sha256(json.dumps(config['profile'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    config['checkpoint_partial']=checkpoint_partial
    if source_profile is not None:
        config['execution_profile']=config['profile'];config['execution_profile_sha256']=config['profile_sha256']
        config['profile']=source_profile;config['profile_sha256']=hashlib.sha256(json.dumps(source_profile,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    for name in ('home','tmp','scripts','methods'): (stage/name).mkdir()
    for source in (Path(__file__),GHIDRA/'support/analyzeHeadless',GHIDRA/'support/launch.sh',JDK/'bin/java',JDK/'bin/jcmd'):
        shutil.copy2(source,stage/'methods'/source.name)
    for name in SCRIPT_NAMES:shutil.copy2(SCRIPT_ROOT/name,stage/'scripts'/name)
    if fixture_fault:
        if not fixture:raise ValueError('fixture faults unavailable on target')
        fixture_fault(stage,config)
        original=dict(config['methods'])
        config['methods']={**original,**{name:sha(stage/'scripts'/name) for name in SCRIPT_NAMES}}
        config['fixture_fault']={'name':fixture_fault.__name__,'original_methods':original,'actual_methods':config['methods']}
        config['profile']['methods']=config['methods'];config['profile']['fixture_fault']=fixture_fault.__name__
        config['profile_sha256']=hashlib.sha256(json.dumps(config['profile'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    validate_copied_methods(stage,config)
    if sha(NATIVE_DECOMPILER)!=config['methods']['native_decompiler']:raise ValueError('native decompiler authority mismatch')
    publish(stage/'stage-config.json',config);config['_sha']=sha(stage/'stage-config.json')
    argv,env=launch_command(stage,config,project,importing=importing,fixture_setup=fixture_setup,fixture_timeout=fixture_timeout,
                            fixture_counter=fixture_counter,fixture_expand=fixture_expanded and importing,gate_name=gate_name,outcome_name=outcome_name)
    if sha(GHIDRA/'support/analyzeHeadless')!=LAUNCH_SHA:raise ValueError('headless launcher pin mismatch')
    publish(stage/'command.json',{'schema':1,'argv':argv,'environment':env})
    started=time.monotonic(); owner=Owner(); samples=[]; error=None; closure=None; p=None;records=None
    job_admission=read_json(allocation_root/'admission.json') if (allocation_root/'admission.json').is_file() else {}
    limit=job_admission.get('allocation_limit_bytes',GIB if fixture else (3*GIB if mode=='enable-analysis-after-ack' else 2*GIB))
    stage_deadline=deadline or (90 if fixture else (1200 if mode=='enable-analysis-after-ack' else 600))
    if 'started_monotonic' in job_admission:
        stage_deadline=min(stage_deadline,job_admission['job_deadline_seconds']-(time.monotonic()-job_admission['started_monotonic']))
    guard=getattr(_JOB_CONTEXT,'guard',None)
    if guard:stage_deadline=min(stage_deadline,guard.seconds-guard.cleanup_reserve-(time.monotonic()-guard.started))
    if stage_deadline<=0:raise RuntimeError('whole job deadline expired before launch')
    policy=ResourcePolicy(allocation_limit=limit,deadline=stage_deadline)
    initial_alloc=allocated_tree(allocation_root); initial_project=allocated_tree(project) if Path(project).exists() else 0
    acknowledged=False;executor=ThreadPoolExecutor(max_workers=1);future=None;last_sample=-1
    scanner=LogScanner([stage/'stdout.txt',stage/'stderr.txt']);outcome_watchdog=None
    previous_handlers={}
    if threading.current_thread() is threading.main_thread():
        def interruption(sig,frame):raise RuntimeError('controller-interrupted-'+str(sig))
        for sig in (signal.SIGINT,signal.SIGTERM):previous_handlers[sig]=signal.signal(sig,interruption)
    try:
        with (stage/'stdout.txt').open('xb') as stdout,(stage/'stderr.txt').open('xb') as stderr:
            p=owner.launch(argv,stdout=stdout,stderr=stderr,env=env)
            while True:
                elapsed=time.monotonic()-started
                if elapsed-last_sample>=1:
                    active=owner.sample(); rss=sum(x['rss_bytes'] for x in active); free=shutil.disk_usage(stage).free
                    allocated=allocated_tree(allocation_root)
                    sample={'elapsed':elapsed,'rss':rss,'free':free,'job_allocated_bytes':allocated,'owned':active};samples.append(sample);last_sample=elapsed
                    reason=policy.observe(elapsed,rss,free,allocated)
                    if reason:raise RuntimeError(reason)
                    if not fixture and mode=='enable-analysis-after-ack':
                        if allocated_tree(project)-initial_project>2*GIB:raise RuntimeError('database-growth-limit')
                        if allocated_tree(stage)>GIB:raise RuntimeError('temp-log-limit')
                if (stage/'STOP').exists():raise RuntimeError('operator-pressure-stop')
                log=scanner.scan()
                if 'REPORT SCRIPT ERROR:' in log or 'Script does not exist or encountered problems' in log:raise RuntimeError('script-failure')
                if 'ANALYZING changes made by post scripts:' in log:raise RuntimeError('untimed-postpass')
                if not future and (stage/'gate-report.json').is_file():future=executor.submit(attest,owner,stage,config,read_json(stage/'gate-report.json'),ack_fault=ack_fault)
                if future and future.done() and not acknowledged:future.result();acknowledged=True
                if mode=='enable-analysis-after-ack' and ('REPORT: Analysis timed out at ' in log or 'REPORT: Analysis succeeded for file:' in log):
                    if outcome_watchdog is None:outcome_watchdog=time.monotonic()
                    if (stage/'analysis-outcome.json').is_file():validate_outcome(stage,config)
                    elif time.monotonic()-outcome_watchdog>10:raise RuntimeError('valid-outcome-watchdog')
                if p.poll() is not None:break
                time.sleep(.1)
            if future:future.result()
            log=scanner.scan()
            records=validate_milestones(stage,config,log,p.returncode,not importing and mode=='verify-only')
            if export_mode:
                path=stage/('inventory-summary.json' if export_mode=='inventory' else 'export-summary.json')
                if not path.is_file():raise ValueError('export positive milestone missing')
                export=read_json(path);lineage(export,config)
    except BaseException as exc:error=exc
    finally:
        try:
            if guard:guard.paused+=1
            cleanup_handlers={}
            try:
                if threading.current_thread() is threading.main_thread():
                    for sig in (signal.SIGINT,signal.SIGTERM):cleanup_handlers[sig]=signal.signal(sig,signal.SIG_IGN)
                try:closure=owner.close()
                except BaseException as exc:
                    closure={'closed':False,'cleanup_error':repr(exc)}
                    if error is None:error=exc
                executor.shutdown(wait=True,cancel_futures=True)
                # No diagnostics can launch after closing=True; repeat the sweep after threads stop.
                try:remaining=owner.sample()
                except Exception as exc:
                    remaining=[];closure['closed']=False;closure['final_sweep_error']=repr(exc)
                if remaining:closure['closed']=False;closure['survivors']=remaining
            finally:
                if guard:guard.paused-=1
                for sig,handler in cleanup_handlers.items():signal.signal(sig,handler)
            # Cleanup is over: hashing and publication remain cancellable work.
            job_tick()
            if error is None and closure.get('signaled'):error=RuntimeError('children required cleanup signals after nominal exit')
            try:target_after=sha(target)
            except BaseException as exc:
                target_after=None
                if error is None:error=exc
            if target_after!=config['target_sha256'] and error is None:error=ValueError('target bytes changed during stage')
            result={'target_after_sha256':target_after,'schema':1,'nonce':config['nonce'],'config_sha256':config['_sha'],'status':'pass' if error is None and closure['closed'] else 'fail',
                    'duration_seconds':time.monotonic()-started,'returncode':p.returncode if p else None,'error':repr(error) if error else None,
                    'closure':closure,'samples':samples,'peak_sampled_rss':max((x['rss'] for x in samples),default=0),
                    'minimum_free':min((x['free'] for x in samples),default=None),'readonly':not importing and mode=='verify-only',
                    'captures':{name:{'sha256':sha(stage/name),'bytes':(stage/name).stat().st_size} for name in ('stdout.txt','stderr.txt','application.log','scripts.log') if (stage/name).is_file()},
                    'milestones':{name:sha(stage/(name+'.json')) for name in ('gate-report','controller-ack','gate-complete','analysis-outcome') if (stage/(name+'.json')).is_file()}}
            publish(stage/'stage-result.json',result)
        finally:
            for sig,handler in previous_handlers.items():signal.signal(sig,handler)
    if result['status']!='pass':raise RuntimeError('stage rejected: '+str(stage)+' '+str(error))
    return result,records


def validate_export_entries(records,entries):
    if not 1<=len(entries)<=5 or len(set(entries))!=len(entries):raise ValueError('one to five unique exact qualified entries')
    index={}
    for record in records:
        key=record['key']
        if key in index:raise ValueError('duplicate inventory key')
        if key!=record['entry_space']+':'+record['entry_offset']:raise ValueError('qualified entry inconsistent')
        index[key]=record
    selected=[]
    for key in entries:
        if key not in index or index[key]['external']:raise ValueError('exact nonexternal own inventory entry required')
        selected.append(index[key])
    return selected


def require_committed(root):
    if (Path(root).parent/'.incomplete').exists():raise ValueError('job completion marker remains')


def validate_export_origin(stage,record):
    """Bind inventory/export bytes to a positively closed verify-only stage."""
    stage=Path(stage)
    if not (stage/'stage-config.json').is_file() or not (stage/'stage-result.json').is_file():raise ValueError('export stage origin missing')
    config=read_json(stage/'stage-config.json');config['_sha']=sha(stage/'stage-config.json');lineage(record,config)
    if config['mode']!='verify-only':raise ValueError('export stage was not verify-only')
    result=read_json(stage/'stage-result.json');closure=result.get('closure',{})
    if result.get('schema')!=1 or result.get('status')!='pass' or result.get('returncode')!=0 or result.get('config_sha256')!=config['_sha']:
        raise ValueError('export stage was not positively accepted')
    if closure.get('closed') is not True or closure.get('reaped') is not True or closure.get('survivors') or closure.get('ownership_gaps') or closure.get('signaled'):
        raise ValueError('export owned closure unverified')
    if set(result.get('milestones',{}))!={'gate-report','controller-ack','gate-complete','analysis-outcome'}:raise ValueError('export positive milestones incomplete')
    for name,pin in result['milestones'].items():
        if sha(stage/(name+'.json'))!=pin:raise ValueError('export milestone capture changed')
    log=LogScanner([stage/'stdout.txt',stage/'stderr.txt']).scan()
    outcome=validate_milestones(stage,config,log,0,True)['analysis-outcome']
    if record.get('outcome_sha256')!=sha(stage/'analysis-outcome.json') or record.get('profile_sha256')!=config['profile_sha256'] or record.get('checkpoint_sha256')!=config['checkpoint_sha256']:
        raise ValueError('export outcome/profile/checkpoint origin differs')
    if record.get('partial') is not (outcome['timeout'] or config['checkpoint_partial']):raise ValueError('export partial origin differs')
    return config


def read_inventory(root,checkpoint_sha=None,requested=None,*,precommit=False):
    root=no_symlinks(root)
    if not precommit:require_committed(root)
    summary=read_json(root/'inventory-summary.json');payload=root/'inventory.jsonl'
    if summary.get('schema')!=1 or summary.get('status')!='pass':raise ValueError('unaccepted inventory')
    if sha(payload)!=summary['payload_sha256'] or payload.stat().st_size!=summary['payload_bytes']:raise ValueError('inventory payload pin mismatch')
    if checkpoint_sha and summary['checkpoint_sha256']!=checkpoint_sha:raise ValueError('inventory checkpoint differs')
    records=[];keys=set(); ordinary=external=0
    with payload.open(encoding='utf-8') as stream:
        for line in stream:
            if len(line)>1024*1024:raise ValueError('oversized inventory record')
            record=decode_json(line);key=record['key']
            if key in keys or key!=record['entry_space']+':'+record['entry_offset']:raise ValueError('duplicate/unqualified inventory entry')
            if not re.fullmatch(r'0x(?:0|[1-9a-f][0-9a-f]*)',record['entry_offset']):raise ValueError('noncanonical offset')
            if type(record['external']) is not bool:raise ValueError('external field requires boolean')
            keys.add(key)
            if requested is not None and key in requested:records.append(record)
            if record['external']:external+=1
            else:ordinary+=1
    if (ordinary,external,len(keys))!=(summary['ordinary'],summary['external'],summary['total']):raise ValueError('inventory counts do not reconcile')
    validate_export_origin(root,summary)
    return records,summary


def load_checkpoint(root):
    root=no_symlinks(root);require_committed(root)
    return validate_checkpoint_manifest(root,read_json(root/'manifest.json'))


def validate_checkpoint_manifest(root,manifest):
    """Validate prepared bytes before the final job commit; no success is published here."""
    root=no_symlinks(root)
    if manifest.get('schema')!=1 or manifest.get('status')!='verified-closed':raise ValueError('unverified checkpoint')
    profile=manifest.get('profile')
    if not isinstance(profile,dict) or hashlib.sha256(json.dumps(profile,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=manifest.get('profile_sha256'):
        raise ValueError('checkpoint profile digest mismatch')
    verify_project(root/'project',manifest['project']);stage_names=set();seen=set();primary=None
    for item in manifest['evidence']:
        path=no_symlinks(item['path'])
        if path in seen or not path.is_relative_to(root.parent) or path.name not in ('stage-config.json','stage-result.json','analysis-outcome.json'):
            raise ValueError('checkpoint evidence path/duplicates invalid')
        seen.add(path)
        if sha(path)!=item['sha256']:raise ValueError('checkpoint supporting capture changed')
        stage_names.add(path.parent.name)
        if path.name=='stage-result.json':
            result=read_json(path)
            if result.get('schema')!=1 or result.get('status')!='pass' or result.get('returncode')!=0:raise ValueError('supporting stage was not accepted')
            closure=result.get('closure',{})
            if closure.get('closed') is not True or closure.get('reaped') is not True or closure.get('survivors') or closure.get('ownership_gaps') or closure.get('signaled'):
                raise ValueError('supporting process closure unverified')
            config=read_json(path.parent/'stage-config.json');config['_sha']=sha(path.parent/'stage-config.json')
            if result['config_sha256']!=config['_sha']:raise ValueError('supporting config hash differs')
            for name,pin in result['milestones'].items():
                if name not in ('gate-report','controller-ack','gate-complete','analysis-outcome') or sha(path.parent/(name+'.json'))!=pin:raise ValueError('supporting milestone pin differs')
            if set(result['milestones'])!={'gate-report','controller-ack','gate-complete','analysis-outcome'}:raise ValueError('incomplete supporting milestones')
            scanner=LogScanner([path.parent/'stdout.txt',path.parent/'stderr.txt'])
            records=validate_milestones(path.parent,config,scanner.scan(),0,result['readonly'])
            if config['target_sha256']!=manifest['target_sha256']:raise ValueError('checkpoint target lineage differs')
            if path.parent.name in ('import','analysis'):
                primary=(config,records['analysis-outcome'],path)
    if stage_names not in ({'import','verify-before','verify-after'},{'analysis','verify-before','verify-after'}) or len(seen)!=9 or primary is None:
        raise ValueError('save plus both disposable reopen stages required')
    config,outcome,path=primary
    if config['profile_sha256']!=manifest['profile_sha256'] or config['profile']!=profile or config['methods']!=manifest['methods']:
        raise ValueError('primary profile/method lineage differs')
    if sha(path)!=manifest['result_sha256'] or sha(path.parent/'analysis-outcome.json')!=manifest['outcome_sha256']:
        raise ValueError('primary outcome/result differs')
    if manifest['partial'] is not (outcome['timeout'] or config['checkpoint_partial']):raise ValueError('checkpoint partial provenance differs')
    if manifest.get('completion_protocol')=='source-check-before-commit-v1' and manifest['parent_checkpoint_sha256']:
        source=manifest['source_after'];path=no_symlinks(source['path'])
        if path!=root.parent/'source-after.json' or sha(path)!=source['sha256']:raise ValueError('source-after capture differs')
        report=read_json(path)
        if report.get('status')!='pass' or report.get('manifest_sha256')!=manifest['parent_checkpoint_sha256']:
            raise ValueError('source integrity exit did not complete successfully')
    return manifest


def commit_job_result(job,result):
    """Publish only prepared success bytes, then remove the acceptance guard last.

    No fallible operation follows guard removal. A failed publish/fsync retains
    the guard and its captures for inspection; this is not a power-loss claim.
    """
    job=Path(job)
    if not (job/'.incomplete').is_file():raise ValueError('fresh job acceptance guard required')
    check_job(job)
    publish(job/'job-result.json',result)
    fd=os.open(job,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
    check_job(job)
    guard=getattr(_JOB_CONTEXT,'guard',None)
    if guard:guard.prepare_commit(job)
    (job/'.incomplete').unlink()
    if guard:guard.committed=True


def commit_checkpoint(job,checkpoint,manifest):
    job=Path(job);checkpoint=Path(checkpoint)
    check_job(job)
    manifest=dict(manifest);manifest['completion_protocol']='source-check-before-commit-v1'
    if manifest['parent_checkpoint_sha256']:
        path=job/'source-after.json';manifest['source_after']={'path':str(path.absolute()),'sha256':sha(path)}
    validate_checkpoint_manifest(checkpoint,manifest)
    publish(checkpoint/'manifest.json',manifest)
    commit_job_result(job,{'schema':1,'status':'pass','checkpoint':str(checkpoint.absolute()),
             'manifest_sha256':sha(checkpoint/'manifest.json'),'baseline_allocated_bytes':manifest['project']['allocated_bytes'],'partial':manifest['partial']})
    return checkpoint


def seal_checkpoint(job,project,target,result,records,*,fixture=False,parent=None,defer_commit=False):
    """Verify both disposable reopens; optionally defer acceptance until source exit."""
    job=Path(job); baseline=project_snapshot(project); target_pin=sha(target)
    budget=read_json(job/'admission.json')['allocation_limit_bytes']
    planned=3*(baseline['allocated_bytes']+64*1024*1024)
    free=shutil.disk_usage(job).free;allocated=allocated_tree(job)
    publish(job/'seal-admission.json',{'schema':1,'fresh_free_bytes':free,'source_allocated_bytes':baseline['allocated_bytes'],
             'copies':3,'planned_allocation_bytes':planned,'whole_job_allocated_bytes':allocated,'allocation_limit_bytes':budget})
    if free<planned+3*GIB or allocated+planned>budget:raise ValueError('measured three-copy checkpoint admission failed')
    verify_copy=copy_project(project,job/'verify-before-project',baseline,budget_root=job,budget_limit=budget)
    run_stage(job/'verify-before',verify_copy,target,fixture=fixture,allocation_root=job)
    verify_project(project,baseline)
    checkpoint=fresh(job/'checkpoint'); copy_project(project,checkpoint/'project',baseline,budget_root=job,budget_limit=budget)
    layout=project_snapshot(checkpoint/'project'); verify_copy2=copy_project(checkpoint/'project',job/'verify-after-project',layout,budget_root=job,budget_limit=budget)
    _,after=run_stage(job/'verify-after',verify_copy2,target,fixture=fixture,allocation_root=job)
    verify_project(checkpoint/'project',layout);verify_project(project,baseline)
    if sha(target)!=target_pin:raise ValueError('target source changed')
    if fixture:
        initial=records['analysis-outcome']; final=after['analysis-outcome']
        if initial.get('fixture_setup_marker')!=final.get('fixture_setup_marker') or initial.get('fixture_timeout_marker')!=final.get('fixture_timeout_marker'):
            raise ValueError('fixture save/reopen markers changed')
        if final.get('fixture_counter_marker'):raise ValueError('forbidden postpass fixture counter ran')
    evidence=[]
    for name in ('import','analysis','verify-before','verify-after'):
        stage=job/name
        if stage.exists():
            for member in ('stage-config.json','stage-result.json','analysis-outcome.json'):
                path=stage/member;evidence.append({'path':str(path.absolute()),'sha256':sha(path)})
    primary=job/('analysis' if (job/'analysis').exists() else 'import')
    config=read_json(primary/'stage-config.json');outcome=records['analysis-outcome']
    manifest={'schema':1,'status':'verified-closed','parent_checkpoint_sha256':parent or '',
              'target_sha256':target_pin,'target':str(Path(target).absolute()),'fixture':fixture,
              'profile':config['profile'],'profile_sha256':config['profile_sha256'],'methods':config['methods'],
              'partial':outcome['timeout'] or config['checkpoint_partial'],'outcome_sha256':sha(primary/'analysis-outcome.json'),
              'result_sha256':sha(primary/'stage-result.json'),'project':layout,'evidence':evidence}
    if defer_commit:return checkpoint,manifest
    return commit_checkpoint(job,checkpoint,manifest)


def prepare_job(output,target,*,fixture=False,mode='import',checkpoint=None):
    output=no_symlinks(output);target=no_symlinks(target)
    if sha(target)!=(FIXTURE_SHA if fixture else TARGET_SHA):raise ValueError('pinned target mismatch')
    parent=load_checkpoint(checkpoint) if checkpoint else None
    baseline=parent['project']['allocated_bytes'] if parent else 0
    free=shutil.disk_usage(output.parent).free; required=4*GIB if fixture else required_peak_free(mode,baseline)
    if free<required:raise RuntimeError('capacity gate: '+str(free)+' < '+str(required))
    output=fresh(output)
    guard=getattr(_JOB_CONTEXT,'guard',None)
    if guard and output==guard.root:guard.owns_root=True
    publish(output/'.incomplete',{'schema':1,'status':'working'})
    publish(output/'admission.json',{'schema':1,'mode':mode,'fresh_free_bytes':free,'required_free_bytes':required,
             'baseline_allocated_bytes':baseline,'fixture':fixture,'target_sha256':sha(target),
             'started_monotonic':getattr(_JOB_CONTEXT,'guard',None).started if getattr(_JOB_CONTEXT,'guard',None) else time.monotonic(),'job_deadline_seconds':90 if fixture else (1200 if mode=='analyze' else 600),
             'retained_project_representations':4 if mode in ('import','analyze') else 1,
             'disk_floor_bytes':3*GIB,'rss_limit_bytes':6*GIB,
             'allocation_limit_bytes':GIB if fixture else (free-3*GIB if mode=='analyze' else 2*GIB)})
    return output,parent


@bounded_job('import')
def import_job(output,target,*,fixture=False,fixture_expanded=False):
    job,_=prepare_job(output,target,fixture=fixture);project=fresh(job/'working-project')
    result,records=run_stage(job/'import',project,target,fixture=fixture,importing=True,fixture_setup=fixture,fixture_expanded=fixture_expanded,allocation_root=job)
    return seal_checkpoint(job,project,target,result,records,fixture=fixture)


@contextmanager
def source_integrity(job,checkpoint,parent):
    checkpoint=Path(checkpoint);pin=sha(checkpoint/'manifest.json');verify_project(checkpoint/'project',parent['project'])
    try:yield
    finally:
        try:
            actual=verify_project(checkpoint/'project',parent['project'])
            if sha(checkpoint/'manifest.json')!=pin:raise ValueError('sealed manifest changed')
            report={'schema':1,'status':'pass','manifest_sha256':pin,'project':actual}
        except BaseException as exc:
            publish(Path(job)/'source-after.json',{'schema':1,'status':'fail','error':repr(exc),'manifest_sha256_before':pin});raise
        publish(Path(job)/'source-after.json',report)


@bounded_job('analyze')
def analysis_job(output,checkpoint,*,fixture=False,fixture_timeout=False):
    parent=load_checkpoint(checkpoint)
    if parent['fixture'] is not fixture:raise ValueError('checkpoint mode mismatch')
    target=Path(parent['target']);job,parent=prepare_job(output,target,fixture=fixture,mode='analyze',checkpoint=checkpoint)
    with source_integrity(job,checkpoint,parent):
        project=copy_project(Path(checkpoint)/'project',job/'working-project',parent['project'],budget_root=job,budget_limit=read_json(job/'admission.json')['allocation_limit_bytes'])
        parent_pin=sha(Path(checkpoint)/'manifest.json')
        result,records=run_stage(job/'analysis',project,target,fixture=fixture,mode='enable-analysis-after-ack',
                  fixture_timeout=fixture_timeout,fixture_counter=fixture,checkpoint=parent_pin,allocation_root=job,
                  checkpoint_partial=parent['partial'],fixture_expanded=parent['profile'].get('fixture_expanded',False))
        verify_project(Path(checkpoint)/'project',parent['project'])
        prepared,manifest=seal_checkpoint(job,project,target,result,records,fixture=fixture,parent=parent_pin,defer_commit=True)
    return commit_checkpoint(job,prepared,manifest)


@bounded_job('export')
def export_job(output,checkpoint,*,fixture=False,inventory=None,entries=()):
    parent=load_checkpoint(checkpoint)
    if parent['fixture'] is not fixture:raise ValueError('checkpoint mode mismatch')
    target=Path(parent['target']);job,parent=prepare_job(output,target,fixture=fixture,mode='export',checkpoint=checkpoint)
    pin=sha(Path(checkpoint)/'manifest.json');mode='functions' if entries else 'inventory'
    if entries:
        if not inventory:raise ValueError('own inventory required')
        records,summary=read_inventory(inventory,pin,requested=entries);validate_export_entries(records,entries)
        if summary['profile_sha256']!=parent['profile_sha256']:raise ValueError('inventory profile differs')
    with source_integrity(job,checkpoint,parent):
        project=copy_project(Path(checkpoint)/'project',job/'working-project',parent['project'],budget_root=job,budget_limit=read_json(job/'admission.json')['allocation_limit_bytes'])
        run_stage(job/'export',project,target,fixture=fixture,checkpoint=pin,export_mode=mode,entries=entries,
                  inventory=Path(inventory)/'inventory.jsonl' if inventory else None,allocation_root=job,checkpoint_partial=parent['partial'],source_profile=parent['profile'])
        verify_project(Path(checkpoint)/'project',parent['project'])
        if mode=='inventory':read_inventory(job/'export',pin,precommit=True)
        else:verify_exports(job/'export',parent,checkpoint_sha=pin,expected_entries=entries,expected_records=records,precommit=True)
    commit_job_result(job,{'schema':1,'status':'pass','checkpoint_sha256':pin,'mode':mode})
    return job/'export'


def verify_exports(stage,checkpoint,*,checkpoint_sha=None,expected_entries=None,expected_records=None,precommit=False):
    stage=Path(stage)
    if not precommit:require_committed(stage)
    summary=read_json(stage/'export-summary.json')
    if summary.get('schema')!=1 or summary.get('status')!='pass' or not isinstance(summary.get('captures'),list) or summary.get('total')!=len(summary['captures']):raise ValueError('export summary malformed')
    if summary.get('checkpoint_sha256')!=checkpoint_sha or summary.get('profile_sha256')!=checkpoint['profile_sha256'] or summary.get('partial') is not checkpoint['partial']:
        raise ValueError('export summary checkpoint/profile/partial differs')
    config=validate_export_origin(stage,summary)
    keys=[];ids=set();records_by_key={item['key']:item for item in (expected_records or [])}
    for capture in summary['captures']:
        ident=capture['capture_id']
        if not re.fullmatch(r'capture-[0-9a-f]{32}-[0-9a-f]{16}',ident) or ident in ids:raise ValueError('unsafe/duplicate capture id')
        ids.add(ident);root=stage/'exports'/ident;manifest=read_json(root/'manifest.json')
        if manifest.get('schema')!=1 or manifest.get('capture_id')!=ident or sha(root/'manifest.json')!=capture['manifest_sha256']:raise ValueError('export manifest identity differs')
        names=[]
        for item in manifest['files']:
            if item['path'] not in ('metadata.json','pseudocode.c') or item['path'] in names:raise ValueError('unknown/duplicate export member')
            names.append(item['path']);path=root/item['path'];no_symlinks(path)
            if sha(path)!=item['sha256'] or path.stat().st_size!=item['bytes']:raise ValueError('export member changed')
        if 'metadata.json' not in names or {x.name for x in root.iterdir()}!=set(names)|{'manifest.json'}:raise ValueError('mandatory metadata pin or member completeness differs')
        meta=read_json(root/'metadata.json');key=meta['entry']['key'];keys.append(key)
        lineage(meta,config)
        if meta.get('outcome_sha256')!=summary['outcome_sha256'] or ident.split('-')[1]!=config['nonce']:raise ValueError('export metadata outcome/run binding differs')
        if meta.get('schema')!=1 or meta.get('capture_id')!=ident or meta.get('state')!=capture['state'] or meta.get('profile_sha256')!=checkpoint['profile_sha256'] or meta.get('checkpoint_sha256')!=checkpoint_sha or meta.get('partial') is not checkpoint['partial']:
            raise ValueError('export metadata lineage differs')
        if ident.rsplit('-',1)[-1]!=hashlib.sha256(key.encode('utf-8')).hexdigest()[:16]:raise ValueError('capture id entry binding differs')
        if expected_records is not None and meta['entry']!=records_by_key.get(key):raise ValueError('export entry contradicts pinned own inventory')
        if not isinstance(meta.get('warnings'),list) or any(not isinstance(w,str) for w in meta['warnings']):raise ValueError('typed warning list required')
        state=meta['state'];code=root/'pseudocode.c'
        if state not in ('exported','exported-with-warnings','failed','failed-with-partial-code'):raise ValueError('unknown export state')
        if (state!='failed') is not code.is_file():raise ValueError('state/code presence differs')
        if code.exists():
            code.read_text(encoding='utf-8')
            if sha(code)!=meta.get('code_sha256') or code.stat().st_size!=meta.get('code_bytes'):raise ValueError('code metadata pin differs')
        if state in ('exported','exported-with-warnings') and (meta.get('completed') is not True or meta.get('null_code') is not False):raise ValueError('successful state contradicts completion/code outcome')
        if state=='exported' and meta['warnings']:raise ValueError('warnings lost from state')
        if state=='exported-with-warnings' and not meta['warnings']:raise ValueError('warned export without warnings')
        if any(p.get('closed') is not True for p in meta.get('native_children',[])):raise ValueError('native child closure unverified')
    if expected_entries is None or sorted(keys)!=sorted(expected_entries) or len(keys)!=len(set(keys)):raise ValueError('requested export completeness differs')
    return summary


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('import');p.add_argument('--target',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--fixture',action='store_true');p.add_argument('--fixture-expanded',action='store_true')
    for name in ('analyze','inventory','export'):
        p=sub.add_parser(name);p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--fixture',action='store_true')
        if name=='analyze':p.add_argument('--fixture-timeout',action='store_true')
        if name=='export':p.add_argument('--inventory',type=Path,required=True);p.add_argument('--entry',action='append',required=True)
    args=parser.parse_args(argv)
    import fcntl
    lock_path=Path(__file__).resolve().parents[1]/'analysis/ableton-live-12.4.3/.persistent-native-controller.lock'
    no_symlinks(lock_path)
    with lock_path.open('a+b') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if args.command=='import':result=import_job(args.output,args.target,fixture=args.fixture,fixture_expanded=args.fixture_expanded)
        elif args.command=='analyze':
            if args.fixture_timeout and not args.fixture:raise ValueError('timeout injector requires fixture mode')
            result=analysis_job(args.output,args.checkpoint,fixture=args.fixture,fixture_timeout=args.fixture_timeout)
        else:result=export_job(args.output,args.checkpoint,fixture=args.fixture,inventory=getattr(args,'inventory',None),entries=getattr(args,'entry',()))
        print(json.dumps({'status':'pass','result':str(result)}))
    return 0


if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,RuntimeError,OSError) as exc:print('Persistent analysis rejected: '+str(exc),file=sys.stderr);sys.exit(1)
