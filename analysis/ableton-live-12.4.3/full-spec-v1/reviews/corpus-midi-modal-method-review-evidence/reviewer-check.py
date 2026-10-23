"""Reviewer data-only reproduction of two selected frozen metrics; never run a CLI."""
from pathlib import Path
import hashlib, importlib.util, json, math, sys, tempfile
BASE=Path('/home/ollie/Documents/sound')
PACKET=BASE/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-modal-method'
compare_path=BASE/'handoff/device-corpus-v2/compare.py'
assert hashlib.sha256(compare_path.read_bytes()).hexdigest()=='f4d660c0c8a798d99f8e560f9505705dea9517174fdc0d5fb8151dc126ad0c83'
prior=sys.dont_write_bytecode
try:
 sys.dont_write_bytecode=True
 spec=importlib.util.spec_from_file_location('review_selected_public_corpus_pure_functions',compare_path)
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
finally:sys.dont_write_bytecode=prior
p60=json.loads((PACKET/'note60-proposal.json').read_text())
p72=json.loads((PACKET/'note72-proposal.json').read_text())
projection=json.loads((PACKET/'selected-comparison-projection.json').read_text())
a=mod.audio(p60['evaluation']['reference']['retained_source']);b=mod.audio(p72['reference']['retained_source'])
old=mod.audio(BASE/'handoff/device-corpus-v2/reference/CORPUS-AUDIO-013-04.f32')
results={}
for label,value,ref,metric in [('note60_self',a,a,p60['evaluation']['metric']),('old_fixed_pitch_against_note60',old,a,p60['evaluation']['metric']),('note72_self',b,b,p72['metric']),('WRONG_note60_against_note72',a,b,p72['metric'])]:
 r=mod.compare(value,ref,metric,44100)
 results[label]=r
 if label in projection:
  expected=projection[label]
  assert [(z['check'],z['pass']) for z in r['measurements']]==[(z['check'],z['pass']) for z in expected['measurements']]
  assert r['pass']==expected['pass']
  assert [z['tolerance'] for z in r['measurements']]==[z['tolerance'] for z in expected['measurements']]
  results[label]['max_error_difference_from_retained_projection']=max(abs(z['error']-w['error']) for z,w in zip(r['measurements'],expected['measurements']))
assert results['note60_self']['pass'] and results['old_fixed_pitch_against_note60']['pass']
assert len(results['note60_self']['measurements'])==98 and len(results['note72_self']['measurements'])==92
assert sum(not z['pass'] for z in results['WRONG_note60_against_note72']['measurements'])==64
# Exact input values and reference identity, rather than source-state inference.
for tag,note in [('note60',60),('note72',72)]:
 script=Path(p60['evaluation']['reference']['retained_source']).with_name(tag+'.script').read_text().splitlines()
 params=[s.split() for s in script if s.startswith('param ')]
 assert len(params)==38
 import struct
 for index,row in enumerate(params):
  name=p60['evaluation']['parameter_order'][index]
  assert int(row[1])==index and struct.pack('<f',float(row[2]))==struct.pack('<f',p60['evaluation']['parameters'][name])
 assert [s for s in script if s.startswith('event ')]==[f'event 1537 0x90 {note} 100']
checks=[]
def rejected(name,fn):
 try:fn()
 except (ValueError,FloatingPointError,ZeroDivisionError):checks.append(name)
 else:raise AssertionError('not rejected: '+name)
with tempfile.TemporaryDirectory(prefix='corpus-midi-method-review-') as directory:
 q=Path(directory)/'fixture.f32';q.write_bytes(b'\0'*(16384*8-8));rejected('invalid length',lambda:mod.audio(q))
 bad=mod.np.zeros((16384,2),dtype='<f4');bad[0,0]=mod.np.nan;q.write_bytes(bad.tobytes());rejected('nonfinite prefix',lambda:mod.audio(q))
zero=mod.np.zeros(16384);rejected('zero reference denominator',lambda:mod.relative_rms(zero,zero));rejected('unmeasurable zero mode',lambda:mod.mode(zero,523.2406255768716,44100,100))
assert len(checks)==4
print(json.dumps({'scope':'Data-only reviewer reproduction, no candidate grade/new criterion code/original calls; exact pure public functions only. No preparation/hypothesis/private model/FFT/main/run executed.','results':results,'negative_controls':checks,'input_bit_and_event_records_exact':True},indent=2,allow_nan=False))
