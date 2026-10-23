"""One selected two-process Corpus X capture. Never rebuilds or imports old tools."""
from pathlib import Path
import datetime, hashlib, json, math, os, resource, signal, struct, subprocess, sys, time
ROOT=Path('/home/ollie/Documents/sound')
PROPOSAL=Path('/tmp/corpus-lfo-depth-proposal.json')
SELECTION=Path('/tmp/corpus-lfo-proposal-source-records.json')
EXPECTED='fadb3e890a943e637f440b83048d80a9153cc428e9c2840775057a0cc383028c'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,value):
 with p.open('x') as f:f.write(json.dumps(value,indent=2)+'\n')
def main():
 if sys.argv[1:]!=['--capture-selected-once']:raise SystemExit('Requires exact selected one-shot invocation; no check/replay mode.')
 assert h(PROPOSAL)['sha256']=='4f9603d32f176ce58eaf093e7a1bfd2dee87766d63f356dced5b7ac16fa6b76d'
 d=json.loads(PROPOSAL.read_text());dest=Path(d['future_output_directory'])
 for pin in d['pins']:assert h(Path(pin['path']))==pin,pin['path']
 assert h(SELECTION)==d['source_records']
 # This is the irreversible one-shot guard: existing or partial destination is NEVER reused.
 dest.mkdir(exist_ok=False);raw=dest/'raw';raw.mkdir(exist_ok=False)
 (dest/'capture-once.py').write_bytes(Path(__file__).read_bytes())
 (dest/'proposal-asof.json').write_bytes(PROPOSAL.read_bytes())
 (dest/'source-selected-records.json').write_bytes(SELECTION.read_bytes())
 context={r['path']:Path(r['path']).read_text() for r in d['pins'] if '/wiki/' in r['path']}
 write(dest/'context-asof.json',context)
 historical=set(Path(r['path']) for r in d['pins'])
 historical.add(Path('/var/tmp/sound-analysis/helpers/Corpus/corpus/decomp/chunks/chunk-00004.jsonl'))
 for rel in ['analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1','analysis/ableton-live-12.4.3/r2/corpus-dsp-v1','handoff/device-corpus-v1','analysis/ableton-live-12.4.3/full-spec-v1/depth-preflight-corpus','analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-modal-observability','analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-modal-calibration']:
  parent=ROOT/rel
  historical.update(p for p in parent.rglob('*') if p.is_file())
 before=[h(p) for p in sorted(historical)];write(dest/'watch-before.json',before)
 env={k:os.environ[k] for k in ['PATH','LANG','LC_ALL','LC_CTYPE','TZ'] if k in os.environ};env['XDEV_TIME']='0'
 assert not set(env)&{'XDEV_LIBM_ULP','XDEV_TRACE_OSTREAM','LD_PRELOAD','LD_LIBRARY_PATH'}
 limits={k:list(resource.getrlimit(getattr(resource,k))) for k in dir(resource) if k.startswith('RLIMIT_')}
 limits['RLIMIT_CORE']=[0,0]
 write(dest/'attempt.json',{'started_utc':now(),'authorization':'Root selected exactly Sine-baseline then RampUp under ADR0003; real shipped x86 calls, not whole Live.','child_environment_complete':env,'inherited_environment_policy':'Only recorded ordinary PATH/locale/TZ values are inherited; no unrelated credentials.','child_limits':limits,'timeout_seconds_per_child':30,'cwd':str(raw),'case_count_max':2,'no_retry':True,'baseline_gate_sha256':EXPECTED,'new_scripts':list(d['scripts'])})
 for name,contents in d['scripts'].items():
  with (raw/name).open('x') as f:f.write(contents)
 assert [(a,b) for a,b in zip(d['scripts']['sine-baseline.script'].splitlines(),d['scripts']['ramp-up.script'].splitlines()) if a!=b]==[('param 18 0.0','param 18 3.0')]
 def core_off():resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 def run(name):
  script=raw/(name+'.script');out=raw/(name+'.f32');stdout=raw/(name+'.stdout');stderr=raw/(name+'.stderr')
  assert not any(p.exists() for p in [out,stdout,stderr])
  argv=[d['future_argvs'][0][0],d['future_argvs'][0][1],str(script),str(out),'--imports']
  status={'name':name,'argv':argv,'started_utc':now(),'executed_original_x86':False,'timeout':False,'exit_code':None,'signal':None,'exception':None}
  start=time.monotonic()
  with stdout.open('xb') as so,stderr.open('xb') as se:
   try:
    child=subprocess.Popen(argv,cwd=raw,env=env,stdout=so,stderr=se,preexec_fn=core_off)
    status['executed_original_x86']=True;status['pid']=child.pid
    try:child.wait(timeout=30)
    except subprocess.TimeoutExpired:
     status['timeout']=True;child.kill();child.wait()
    status['exit_code']=child.returncode
    if child.returncode<0:status['signal']=-child.returncode
   except Exception as exc:status['exception']=repr(exc)
  status['finished_utc']=now();status['elapsed_seconds']=time.monotonic()-start
  status['stdout']=h(stdout);status['stderr']=h(stderr);log=stdout.read_text(errors='replace')+'\n'+stderr.read_text(errors='replace')
  status['used_imports']=[s for s in log.splitlines() if s.startswith('used ')]
  status['declared_imports']=[s for s in log.splitlines() if s.startswith('import ')]
  status['process_lines']=[s for s in log.splitlines() if s.startswith('process ')]
  status['fault_or_trap']=[s for s in log.splitlines() if 'TRAP' in s or 'FAULT' in s or s.startswith('xdev:')]
  status['cxx_failbits_lines']=[s for s in log.splitlines() if s.startswith('cxx-failbits ')]
  status['output_exists']=out.is_file()
  if out.is_file():
   status['output']=h(out);b=out.read_bytes();status['size_valid']=len(b)==131072
   if len(b)%8==0:
    frames=list(struct.iter_unpack('<ff',b));status['frames']=len(frames)
    status['all_finite']=all(math.isfinite(v) for frame in frames for v in frame)
    channels=[]
    for c in range(2):
     values=[f[c] for f in frames];post=values[4096:]
     channels.append({'channel':c,'nonzero_total':sum(v!=0 for v in values),'nonzero_after_impulse':sum(v!=0 for v in post),'peak_abs':max(map(abs,values),default=0),'sum_square_after_impulse':sum(v*v for v in post),'first_nonzero':next((i for i,v in enumerate(values) if v!=0),None)})
    status['channels']=channels
  status['baseline_hash_match']=status.get('output',{}).get('sha256')==EXPECTED if name=='sine-baseline' else None
  status['valid_capture']=status['exit_code']==0 and not status['timeout'] and status['exception'] is None and not status['fault_or_trap'] and status['cxx_failbits_lines']==['cxx-failbits 0'] and status.get('size_valid',False) and status.get('all_finite',False) and all(c['nonzero_after_impulse']>0 and c['sum_square_after_impulse']>0 for c in status.get('channels',[])) and len(status.get('channels',[]))==2
  write(dest/(name+'-result.json'),status);return status
 results=[run('sine-baseline')]
 if results[0]['valid_capture'] and results[0]['baseline_hash_match']:results.append(run('ramp-up'))
 after=[h(p) for p in sorted(historical)];changed=[{'before':a,'after':b} for a,b in zip(before,after) if a!=b]
 write(dest/'watch-after.json',{'checked_utc':now(),'files':after,'changed':changed})
 summary={'finished_utc':now(),'cases':results,'ramp_executed':len(results)==2,'watch_count':len(before),'watch_unchanged':not changed,'not_executed':['whole Live','arm64','old runners/build/imports/fit/model/comparators'],'grade':None,'waveform_or_frequency_criterion':None,'modal174_status':'unchanged ungraded','classification':'New finite X original x86 audio captures for declared host calls only.'}
 write(dest/'results.json',summary)
 print(json.dumps({'directory':str(dest),'watch_count':len(before),'watch_unchanged':not changed,'cases':[{'name':r['name'],'exit':r['exit_code'],'valid_capture':r['valid_capture'],'baseline_hash_match':r['baseline_hash_match'],'sha256':r.get('output',{}).get('sha256'),'bytes':r.get('output',{}).get('bytes')} for r in results]},indent=2))
if __name__=='__main__':main()
