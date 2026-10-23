"""Verify exact original input bytes, parameter vectors and retained capture hashes."""
import hashlib
import json
import re
from pathlib import Path

import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SOURCE=ROOT/'analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1'
PACKAGE=HERE.with_name('device-corpus-v1')
runs=json.loads((SOURCE/'results/corpus_runs.json').read_text())
trace=json.loads((HERE/'traceability.json').read_text())['evaluations']
cases=json.loads((PACKAGE/'cases.json').read_text())['cases']
evaluations={e['id']:e for c in cases for e in c['evaluations']}
inputs={}
for row in trace:
 e=evaluations[row['evaluation']]
 original=runs['runs'][row['source_run']]['case']
 lines=(ROOT/row['source_script']).read_text().splitlines()
 params=[(int(i),float(v)) for i,v in (re.fullmatch(r'param (\d+) (.+)',s).groups() for s in lines if s.startswith('param '))]
 assert len(params)==38 and [p[0] for p in params]==list(range(38))
 for index,v in params:
  assert np.float32(v)==np.float32(e['parameters'][e['parameter_order'][index]])
 assert original['fs']==e['sample_rate_hz']
 reference=(PACKAGE/e['reference']).read_bytes()
 assert hashlib.sha256(reference).hexdigest()==row['source_render_sha256']
 inputs[row['source_input']]=e['signal']
for name,file in inputs.items():
 n=np.arange(16384)
 if name.startswith('impulse'):
  data=np.zeros((16384,2),np.float32);data[4096]=1
 elif name.startswith('sine'):
  frequency=261.62 if name.startswith('sine261') else float(name.split('_')[0][4:])
  rate=48000 if name.endswith('_48') else 44100
  mono=(.25*np.sin(2*np.pi*frequency*n/rate)).astype(np.float32);data=np.stack([mono,mono],1)
 elif name=='noise44':
  mono=(.1*np.random.default_rng(1214).standard_normal(16384)).astype(np.float32);data=np.stack([mono,mono],1)
 elif name=='dc44':data=np.full((16384,2),.5,np.float32)
 else:raise AssertionError(name)
 assert data.tobytes()==(PACKAGE/file).read_bytes(),name
report={'status':'pass','original_vectors_checked':len(trace),'reference_output_hashes_checked':len(trace),'generated_signals_reproduced_byte_for_byte':len(inputs),'source_manifest_entries_verified_at_build':len(json.loads((SOURCE/'manifest.json').read_text())['files'])}
(HERE/'source-validation.json').write_text(json.dumps(report,indent=1)+'\n');print(report)
