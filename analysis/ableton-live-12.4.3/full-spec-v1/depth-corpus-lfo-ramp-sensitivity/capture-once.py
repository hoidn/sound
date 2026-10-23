"""Selected two-call sensitivity capture; no old collector/model/comparator imports."""
from pathlib import Path
import datetime,hashlib,json,math,os,resource,struct,subprocess,sys,time
ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-lfo-ramp-up'
DEST=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-lfo-ramp-sensitivity'
SEAL='b30f110700d57892331dd9b218fc99b765afc97176e25c48de9e89e65733bd26'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def ident(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,d):
 with p.open('x') as f:f.write(json.dumps(d,indent=2)+'\n')
def audio(p):
 b=p.read_bytes();assert len(b)==131072,'wrong byte count'
 x=list(struct.iter_unpack('<ff',b));assert all(math.isfinite(v) for f in x for v in f),'nonfinite data'
 assert all(sum(f[c]*f[c] for f in x[4096:])>0 for c in range(2)),'zero channel energy'
 return x
def rrms(x,r):
 return [math.sqrt(sum((a[c]-b[c])**2 for a,b in zip(x[4096:],r[4096:]))/sum(b[c]**2 for b in r[4096:])) for c in range(2)]
def main():
 if sys.argv[1:]!=['--capture-selected-once']:raise SystemExit('One-shot selected capture only; no replay/regeneration modes.')
 assert ident(BASE/'manifest.json')['sha256']==SEAL
 manifest=json.loads((BASE/'manifest.json').read_text())
 for r in manifest['files']:
  p=BASE/r['path'];assert ident(p)=={'path':str(p),'bytes':r['bytes'],'sha256':r['sha256']}
 proposal=json.loads((BASE/'proposal-asof.json').read_text())
 for r in proposal['pins']:
  if '/wiki/' not in r['path']:assert ident(Path(r['path']))==r
 ramp=audio(BASE/'raw/ramp-up.f32');sine=audio(BASE/'raw/sine-baseline.f32')
 script=(BASE/'raw/ramp-up.script').read_bytes()
 watched={Path(r['path']) for r in json.loads((BASE/'watch-before.json').read_text())}|{p for p in BASE.rglob('*') if p.is_file()}
 before=[ident(p) for p in sorted(watched)];assert len(before)==422
 DEST.mkdir(exist_ok=False);raw=DEST/'raw';raw.mkdir(exist_ok=False)
 (DEST/'capture-once.py').write_bytes(Path(__file__).read_bytes())
 save(DEST/'watch-before.json',before)
 source=ROOT/'analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1/harness/xdev_bind.c'
 lines=source.read_text().splitlines(keepends=True)
 save(DEST/'source-context.json',{'file':ident(source),'fresh_read_spans':[[1,110],[111,175]],'roles':[{'lines':[33,50],'role':'pf/pd nextafter directions and25 selected wrapper families; no inexactness test'},{'lines':[52,60],'role':'fixed sincos/exp10 wrappers also use pf/pd'},{'lines':[153,175],'role':'getenv+atoi, choose perturbed families before ordinary libm; fixed bindings already returned'}],'full_source_asof':source.read_text(),'qualification':'All-up/down family results are finite sensitivity experiments, not a mixed-call rounding envelope, Apple libm or arm64 emulation.'})
 (DEST/'context-asof.json').write_bytes((BASE/'context-asof.json').read_bytes())
 env=json.loads((BASE/'attempt.json').read_text())['child_environment_complete'];assert set(env)<=set(['PATH','LANG','LC_ALL','LC_CTYPE','TZ','XDEV_TIME']) and env['XDEV_TIME']=='0'
 limits={k:list(resource.getrlimit(getattr(resource,k))) for k in dir(resource) if k.startswith('RLIMIT_')};limits['RLIMIT_CORE']=[0,0]
 save(DEST/'attempt.json',{'started_utc':utc(),'scope':'Exactly2 additional actual original-x86 sensitivity calls, +1 then-1; no baseline replay.','base_packet':str(BASE),'base_manifest':ident(BASE/'manifest.json'),'baseline_original_execution':'The previous2capture history remains actualX and untouched.','provider_pins':proposal['pins'],'frozen_provider_files':[ident(BASE/r['path']) for r in manifest['files']],'child_environment_base_complete':env,'child_environments_complete':[{**env,'XDEV_LIBM_ULP':v} for v in ['+1','-1']],'timeout_seconds_per_child':30,'child_limits':limits,'cwd':str(raw),'max_native_children':2,'no_retry':True,'all_scripts_exact_source':ident(BASE/'raw/ramp-up.script'),'numeric_window':[4096,16384],'numeric_dtype':'binary32 decode widened to binary64; no alignment/gainfit/exclusions/demodulation','criterion':None,'grade':None})
 for n in ['plus1','minus1']:
  with (raw/(n+'.script')).open('xb') as f:f.write(script)
 def no_core():resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 def run(n,direction):
  out=raw/(n+'.f32');so=raw/(n+'.stdout');se=raw/(n+'.stderr')
  assert not any(p.exists() for p in [out,so,se])
  childenv={**env,'XDEV_LIBM_ULP':direction}
  argv=[proposal['future_argvs'][0][0],proposal['future_argvs'][0][1],str(raw/(n+'.script')),str(out),'--imports']
  r={'name':n,'direction_ascii':direction,'argv':argv,'child_environment_complete':childenv,'started_utc':utc(),'exit_code':None,'signal':None,'timeout':False,'exception':None,'actual_original_x86_capture':False}
  start=time.monotonic()
  with so.open('xb') as stdout,se.open('xb') as stderr:
   try:
    child=subprocess.Popen(argv,cwd=raw,env=childenv,stdout=stdout,stderr=stderr,preexec_fn=no_core);r['pid']=child.pid;r['actual_original_x86_capture']=True
    try:child.wait(timeout=30)
    except subprocess.TimeoutExpired:r['timeout']=True;child.kill();child.wait()
    r['exit_code']=child.returncode
    if child.returncode<0:r['signal']=-child.returncode
   except Exception as exc:r['exception']=repr(exc)
  r['finished_utc']=utc();r['elapsed_seconds']=time.monotonic()-start;r['stdout']=ident(so);r['stderr']=ident(se)
  text=so.read_text(errors='replace');err=se.read_text(errors='replace');lines=text.splitlines()
  r['imports']=[x for x in lines if x.startswith('import ')];r['used_imports']=[x for x in lines if x.startswith('used ')]
  r['trap_or_fault']=[x for x in (text+'\n'+err).splitlines() if 'TRAP' in x or 'FAULT' in x or x.startswith('xdev:')]
  r['cxx_failbits']=[x for x in lines if x.startswith('cxx-failbits ')];r['process_lines']=[x for x in lines if x.startswith('process ')]
  r['valid_numeric']=False;r['numeric_error']=None
  if out.is_file():
   r['output']=ident(out)
   try:
    x=audio(out);r['valid_numeric']=True
    r['relative_rms_to_frozen_ramp_by_channel']=rrms(x,ramp)
    r['frozen_sine_wrong_shape_relative_rms_to_frozen_ramp_by_channel']=rrms(sine,ramp)
    r['channels']=[{'channel':c,'post_impulse_energy':sum(f[c]*f[c] for f in x[4096:]),'post_impulse_nonzero':sum(f[c]!=0 for f in x[4096:]),'peak_abs':max(abs(f[c]) for f in x)} for c in range(2)]
   except (AssertionError,ValueError,OverflowError) as exc:r['numeric_error']=str(exc)
  r['valid_capture']=r['exit_code']==0 and not r['timeout'] and r['exception'] is None and r['valid_numeric'] and not r['trap_or_fault'] and not err and r['cxx_failbits']==['cxx-failbits 0'] and r['process_lines']==['process 16384 512 flags: 32x(ret=0,flag=1) blocks=32'] and 'create ok' in lines and 'destroy' in lines
  save(DEST/(n+'-result.json'),r);return r
 runs=[run('plus1','+1')]
 if runs[0]['valid_capture']:runs.append(run('minus1','-1'))
 after=[ident(p) for p in sorted(watched)];changed=[{'before':a,'after':b} for a,b in zip(before,after) if a!=b]
 save(DEST/'watch-after.json',{'checked_utc':utc(),'files':after,'changed':changed})
 save(DEST/'results.json',{'finished_utc':utc(),'runs':runs,'native_child_count':len(runs),'watch_count':len(before),'watch_unchanged':not changed,'criterion':None,'grade':None,'confidence_interval':None,'new_normative_ids':0,'modal174_status':'all unchanged ungraded','limitation':'Same-direction family perturbations are not a mixed-error envelope or an Apple/arm64 bound. No default/baseline replay or other provider.'})
 print(json.dumps({'directory':str(DEST),'runs':[{'name':r['name'],'exit':r['exit_code'],'valid':r['valid_capture'],'bytes':r.get('output',{}).get('bytes'),'sha256':r.get('output',{}).get('sha256'),'relative_rms_to_ramp':r.get('relative_rms_to_frozen_ramp_by_channel'),'sine_wrongshape_contrast':r.get('frozen_sine_wrong_shape_relative_rms_to_frozen_ramp_by_channel')} for r in runs],'watch_count':len(before),'watch_unchanged':not changed},indent=2))
if __name__=='__main__':main()
