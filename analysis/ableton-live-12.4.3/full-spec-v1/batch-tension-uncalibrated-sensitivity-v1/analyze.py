"""Offline recorded-data analysis only; exact historical metric function, no original calls."""
from pathlib import Path
import sys,json,hashlib,types,math,datetime
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'method'))
import numpy as np
from scipy.io import wavfile
import compare as C
H=lambda b:hashlib.sha256(b).hexdigest()
def clean(x):
 if isinstance(x,dict):return {k:clean(v)for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v)for v in x]
 if isinstance(x,np.generic):return clean(x.item())
 if isinstance(x,float)and not math.isfinite(x):return {'unknown':'nonfinite metric','raw_repr':repr(x)}
 return x
def compare(name,x,r,meas):
 try:return {'metrics':clean(C.compare(name,x,r,meas)),'error':None}
 except Exception as e:return {'metrics':None,'error':type(e).__name__+': '+str(e),'unknown':'existing metric not available for this exact input/window; no replacement formula or dropped setting'}
def main():
 settings=json.loads((P/'settings.json').read_bytes());jobs=json.loads((P/'jobs.json').read_bytes());old=json.loads((P/'baseline-measurements.json').read_bytes());status=json.loads((P/'actual/status.json').read_bytes())
 assert status['completed']==222 and status['error']is None
 C.cases=types.SimpleNamespace(CASES={s['name']:s for s in settings})
 out={'method':'Exact retained sensitivity.compare +measure/fit semantics; no new f0/tolerance/ARM bound','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'settings':[]}
 for s in settings:
  name=s['name'];fs,ref=wavfile.read(P/f'baselines/{name}.wav');assert fs==44100 and ref.dtype==np.float32 and ref.shape==(44100,)
  oldstereo=np.stack([ref,ref],1).astype('<f4');assert H(oldstereo.tobytes())==s['old_run']['raw_f32_sha256']
  basebytes=(P/f'actual/{name}--baseline/output.f32').read_bytes();base=np.frombuffer(basebytes,dtype='<f4').reshape(-1,2)
  d={'name':name,'old_wav_sha256':s['old_wav_sha256'],'old_raw_stereo_reconstruction_sha256':H(oldstereo.tobytes()),'baseline_exact_old_raw_match':basebytes==oldstereo.tobytes(),'old_vs_fresh_channels_identical':bool(np.array_equal(base[:,0].view(np.uint32),base[:,1].view(np.uint32))),'historical_measured_held_window':old[name]['held']['window'],'historical_held_partials':old[name]['held']['partials'],'fresh_baseline_vs_old':{},'variants':[]}
  for ch in range(2):d['fresh_baseline_vs_old'][str(ch)]=compare(name,base[:,ch].astype(float),ref.astype(float),old[name])
  for j in [j for j in jobs if j['name']==name and j['variant']!='baseline']:
   b=(P/f"actual/{j['key']}/output.f32").read_bytes();x=np.frombuffer(b,dtype='<f4').reshape(-1,2)
   v={'variant':j['variant'],'raw_sha256':H(b),'exact_fresh_control_match':b==basebytes,'channels':{}}
   for ch in range(2):v['channels'][str(ch)]=compare(name,x[:,ch].astype(float),base[:,ch].astype(float),old[name])
   d['variants'].append(v)
  out['settings'].append(d);print(json.dumps({'analyzed_setting':name,'count':len(out['settings']),'fresh_old_exact':d['baseline_exact_old_raw_match']}),flush=True)
 out['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();out['counts']={'settings':37,'baseline_comparisons_channels':74,'fresh_perturbation_comparisons_channels':370,'fresh_historical_exact_matches':sum(s['baseline_exact_old_raw_match']for s in out['settings'])}
 out['limits']='Exact finite x86/recorded Linux substitutions only. No new tolerances, readyX/general stable-chaotic/ARM/Apple/calibration/publicA1A2 claims. None/errors/nonfinite metrics explicit unknown; old missing process custody not repaired.'
 with(P/'observations.json').open('x')as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
if __name__=='__main__':main()
