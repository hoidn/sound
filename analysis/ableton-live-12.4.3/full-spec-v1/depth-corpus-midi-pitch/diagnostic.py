"""New data-only peak listing AFTER captured pair. No device/model/comparator code."""
from pathlib import Path
import json,math,sys
import numpy as np
HERE=Path(__file__).resolve().parent

def main():
 if sys.argv[1:]!=['--analyze']:raise SystemExit('Read-only --analyze only, after both valid captures; no capture/replay.')
 results=json.loads((HERE/'results.json').read_text());assert len(results['runs'])==2 and all(r['valid_capture'] for r in results['runs'])
 report={'scope':'Exploratory FFT peaks only; no fundamental classifier, estimator tolerance, note-delivery pass or compatibility grade.','frames':[4096,16384],'window':'numpy symmetric Hann12288','fft_points':12288,'sample_rate_hz':44100,'bin_spacing_hz':44100/12288,'source_predicted_nominal_f0_hz':{'60':261.62,'72':523.24},'grade':None,'criterion':None,'channels':[]}
 for name,note in [('note60',60),('note72',72)]:
  p=HERE/'raw'/(name+'.f32');assert p.stat().st_size==131072
  x=np.fromfile(p,dtype='<f4').reshape(16384,2).astype(np.float64);assert np.isfinite(x).all()
  for c in range(2):
   s=x[4096:,c];assert math.fsum(float(v)*float(v) for v in s)>0
   y=np.fft.rfft(s*np.hanning(12288));power=y.real*y.real+y.imag*y.imag;assert np.isfinite(power).all()
   indexes=[i for i in range(1,len(power)-1) if power[i]>power[i-1] and power[i]>=power[i+1]]
   indexes=sorted(indexes,key=lambda i:(-float(power[i]),i))[:16]
   report['channels'].append({'case':name,'note':note,'channel':c,'peaks_descending_power':[{'bin':i,'frequency_hz':i*44100/12288,'power':float(power[i])} for i in indexes]})
 print(json.dumps(report,indent=2,allow_nan=False))
if __name__=='__main__':main()
