"""One fixed sequential222-child existing-harness batch; never build or retry."""
import argparse,datetime,hashlib,json,math,os,resource,signal,struct,subprocess,sys,time
from pathlib import Path
P=Path(__file__).resolve().parent
ENV={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def H(b):return hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def write(p,b):
 if not isinstance(b,bytes):b=(json.dumps(b,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
def identity(path):
 path=Path(path);h=hashlib.sha256();n=0
 with path.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return {'path':str(path),'bytes':n,'sha256':h.hexdigest()}
def verify(pins):
 found=[identity(x['path'])for x in pins];need(found==pins,'custody mismatch');return found
def output(raw):
 need(len(raw)==352800,'output shape')
 values=struct.unpack('<88200f',raw);need(all(math.isfinite(x)for x in values),'nonfinite raw output')
 return {'bytes':len(raw),'sha256':H(raw),'frames':44100,'channels':2,'format':'interleaved little-endian binary32','finite_left':True,'finite_right':True,'channels_identical':all(raw[i:i+4]==raw[i+4:i+8]for i in range(0,len(raw),8)),'peak_left':max(abs(x)for x in values[::2]),'peak_right':max(abs(x)for x in values[1::2])}
def protocol(text,job,allowed):
 lines=text.splitlines();need('create ok'in lines and 'destroy'in lines and 'cxx-failbits 0'in lines,'create/destroy/cxx protocol')
 need(not any('TRAP'in l or 'FAULT'in l or l.startswith('xdev:')for l in lines),'fault/protocol diagnostic')
 need(sum(l.startswith('param ')for l in lines)==129,'setter count')
 need(sum(l.startswith('rate 44100 ret=')for l in lines)==1,'sample rate protocol')
 proc=[l for l in lines if l.startswith('process ')];need(len(proc)==1 and proc[0].startswith('process 44100 512 flags:')and proc[0].endswith('blocks=87'),'process count')
 params=[l.split()for l in lines if l.startswith('param ')];need([int(x[1])for x in params]==[i for i in range(130)if i!=2],'setter order')
 need([struct.pack('<f',float(x[2])).hex()for x in params]==[x['binary32_le']for x in job['parameter_words']],'setter logged binary32 values')
 need([l for l in lines if l.startswith('event ')]==job['event_log'],'events')
 mx=[l for l in lines if l.startswith('mxcsr ')];need(mx==job['mxcsr_log'],'rounding phase')
 used={l.split()[1]:int(l.split()[2])for l in lines if l.startswith('used ')};need(set(used)<=set(allowed),'unexpected used import')
 exports=[l.split()[1]for l in lines if l.startswith('export ')];need(exports==['_CreateInstanceU','_DestroyInstanceU','_SetSampleRateU','_GetPlugInfoU','_CalcA','_SetParameterA','_ResetA'],'export enumeration')
 need('slice offset=16384 size=501392'in lines,'slice identity metadata')
 return {'used_imports':used,'process_line':proc[0],'cxx_failbits':0,'setter_count':129,'CalcA_calls':87,'direct_export_calls':219,'export_lines':[l for l in lines if l.startswith('export ')],'binding_lines':[l for l in lines if l.startswith('import ')]}
def limits():resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def cleanup(c):
 try:os.killpg(c.pid,signal.SIGKILL);return 'SIGKILL-group-sent'
 except ProcessLookupError:return 'group-already-gone'
def selfcheck():
 negatives=[]
 def reject(n,f):
  try:f()
  except(ValueError,KeyError,TypeError):negatives.append(n);return
  raise AssertionError(n)
 raw=bytes(352800);need(output(raw)['channels_identical'],'synthetic positive')
 reject('short stereo',lambda:output(raw[:-4]));reject('extra frame',lambda:output(raw+bytes(8)))
 for label,bits,at in [('leftNaN',0x7fc00000,0),('rightInf',0x7f800000,4),('negativeInf',0xff800000,0)]:
  bad=bytearray(raw);bad[at:at+4]=bits.to_bytes(4,'little');reject(label,lambda bad=bad:output(bytes(bad)))
 need(not output(struct.pack('<ff',1,2)*44100)['channels_identical'],'stereo difference retained')
 job={'event_log':['event 4096 0x90 60 100','event 26146 0x80 60 0'],'mxcsr_log':[],'parameter_words':[{'binary32_le':'00000000'}for _ in range(129)]}
 lines=['slice offset=16384 size=501392']+['export '+n+' 0x1'for n in['_CreateInstanceU','_DestroyInstanceU','_SetSampleRateU','_GetPlugInfoU','_CalcA','_SetParameterA','_ResetA']]+['create ok','rate 44100 ret=9']+[f'param {i} 0'for i in range(130)if i!=2]+job['event_log']+['process 44100 512 flags: 87x(ret=0,flag=0) blocks=87','destroy','used _exp 1','cxx-failbits 0']
 text='\n'.join(lines);protocol(text,job,['_exp'])
 for label,a,b in [('NULLcreate','create ok','create NULL'),('nonzeroCxx','cxx-failbits 0','cxx-failbits 1'),('missingSetter','param 129 0',''),('wrongValue','param 129 0','param 129 1'),('unexpectedImport','used _exp 1','used _alien 1'),('wrongEvent','event 4096','event 4097'),('missingDestroy','destroy',''),('wrongBlockCount','blocks=87','blocks=86')]:
  reject(label,lambda a=a,b=b:protocol(text.replace(a,b),job,['_exp']))
 print(json.dumps({'status':'PASS-synthetic-only','negative_controls':negatives,'children':0,'original_calls':0},indent=2))
def run(expected):
 need(dict(os.environ)==ENV,'minimal outer environment');pb=(P/'pre-call-manifest.json').read_bytes();need(H(pb)==expected,'precall hash');plan=json.loads(pb)
 jobs=json.loads((P/'jobs.json').read_bytes());settings={x['name']:x for x in json.loads((P/'settings.json').read_bytes())}
 need(len(settings)==37 and len(jobs)==222,'whole finite class');need([j['ordinal']for j in jobs]==list(range(222)),'order')
 out=P/'actual';out.mkdir(exist_ok=False);write(out/'before-identities.json',verify(plan['pins']))
 old_term=signal.getsignal(signal.SIGTERM)
 def interrupted(n,f):raise RuntimeError('interrupted by SIGTERM')
 signal.signal(signal.SIGTERM,interrupted)
 status={'started_utc':utc(),'outer_pid':os.getpid(),'outer_argv':sys.argv,'environment':dict(os.environ),'input_manifest_sha256':expected,'planned_children':222,'attempted':0,'completed':0,'native_original_calls_selected':True,'automatic_retry':False,'error':None,'results':[]}
 write(out/'attempt.json',status);resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 try:
  for job in jobs:
   d=out/job['key'];d.mkdir(exist_ok=False);script=P/job['script'];need(identity(script)=={'path':str(script),'bytes':job['script_bytes'],'sha256':job['script_sha256']},'fixed script')
   write(d/'before-identities.json',verify(plan['runtime_pins']))
   argv=[plan['executable']['path'],plan['image']['path'],str(script),str(d/'output.f32'),'--imports']
   r={'ordinal':job['ordinal'],'key':job['key'],'variant':job['variant'],'name':job['name'],'argv':argv,'environment':job['env'],'started_utc':utc(),'timeout_seconds':20,'stdin':'DEVNULL','core_bytes':0,'new_session':True,'attempt':1,'pid':None,'exit_code':None,'timed_out':False,'error':None}
   write(d/'before.json',r);c=None;t=time.monotonic();failure=None
   try:
    with(d/'stdout').open('xb')as so,(d/'stderr').open('xb')as se:
     c=subprocess.Popen(argv,env=job['env'],stdin=subprocess.DEVNULL,stdout=so,stderr=se,start_new_session=True,preexec_fn=limits)
     status['attempted']+=1;r['pid']=c.pid;write(d/'pid.json',{'pid':c.pid,'pgid':c.pid,'utc':utc(),'argv':argv})
     try:c.wait(timeout=20)
     except subprocess.TimeoutExpired:r['timed_out']=True;raise
     finally:
      r['cleanup']=cleanup(c)
      try:c.wait(timeout=5)
      except subprocess.TimeoutExpired:r['cleanup_wait_timeout']=True
      r['exit_code']=c.returncode;so.flush();se.flush();os.fsync(so.fileno());os.fsync(se.fileno())
    need(not r['timed_out']and r['exit_code']==0,'child exit/timeout')
    need((d/'stdout').stat().st_size<=131072 and (d/'stderr').stat().st_size==0,'stdout bound/stderr')
    r['protocol']=protocol((d/'stdout').read_text(),job,settings[job['name']]['allowed_used_imports'])
    raw=(d/'output.f32').read_bytes();r['output']=output(raw)
    with(d/'output.f32').open('rb')as f:os.fsync(f.fileno())
    status['completed']+=1
   except BaseException as e:failure=e;r['error']=type(e).__name__+': '+str(e)
   finally:
    r['finished_utc']=utc();r['elapsed_seconds']=time.monotonic()-t
    try:after=verify(plan['runtime_pins']);write(d/'after-identities.json',after);r['custody_unchanged']=True
    except BaseException as e:r['custody_unchanged']=False;failure=failure or e;r['error']=r['error']or type(e).__name__+': '+str(e)
    for name in ['stdout','stderr','output.f32']:
     f=d/name
     if f.exists():r[name.replace('.','_')+'_identity']=identity(f)
    write(d/'result.json',r);status['results'].append(r)
   print(json.dumps({'completed':status['completed'],'attempted':status['attempted'],'key':job['key'],'error':r['error']}),flush=True)
   if failure:raise failure
 except BaseException as e:status['error']=type(e).__name__+': '+str(e)
 finally:
  try:write(out/'after-identities.json',verify(plan['pins']));status['all_frozen_inputs_unchanged']=True
  except BaseException as e:status['all_frozen_inputs_unchanged']=False;status['error']=status['error']or str(e)
  status['finished_utc']=utc();write(out/'status.json',status);signal.signal(signal.SIGTERM,old_term)
 return 0 if status['error']is None else 1
if __name__=='__main__':
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--self-check',action='store_true');g.add_argument('--run-once');a=ap.parse_args()
 if a.self_check:selfcheck()
 else:raise SystemExit(run(a.run_once))
