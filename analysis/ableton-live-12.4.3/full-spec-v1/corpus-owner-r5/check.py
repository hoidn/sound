"""Owner text/input integrity only; no capture, estimator, old tool or model imports."""
from pathlib import Path
import copy,hashlib,json,math,re,struct,sys
P=Path(__file__).resolve().parent

def load(name):return json.loads((P/name).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(pin):
 b=Path(pin['path']).read_bytes()
 assert len(b)==pin['bytes'] and sha(b)==pin['sha256']
 return b

def cases(text):return [s for s in text.splitlines() if re.match(r'^\| DCO-\d{3} \|',s)]
def norm_ids(text):return re.findall(r'^### (REQ-DEVICE-CORPUS-\d{3}) ',text,re.M)

def validate(cs,ep):
 proposal=load('note60-proposal-asof.json');inputs=load('inputs.json');report=json.loads(verify(inputs['calibration_report']))
 assert len(cs)==2 and [c['id'] for c in cs]==['DCO-030','DCO-031']
 assert ep['DCO-031']['selected_zero_based_indices_per_channel']==list(range(15))
 assert ep['DCO-031']['points']==30 and ep['DCO-031']['measurement_checks']==92
 assert ep['DCO-031']['full_research_records_retained']==32 and not ep['DCO-031']['numeric_budgets_changed'] and not ep['DCO-031']['centers_refitted']
 for index,note in enumerate([60,72]):
  c=cs[index];e=c['evaluation'];base=proposal['evaluation']
  assert c['candidate_or_application_grade'] is None
  assert c['requirements']==['REQ-DEVICE-CORPUS-001','REQ-DEVICE-CORPUS-013']
  for field in ['sample_rate_hz','frames','block_frames','signal','parameters','parameter_order','before_parameters','after_parameters']:assert e[field]==base[field]
  assert len(e['parameters'])==len(e['parameter_order'])==38
  assert e['events']==[{'frame':1537,'kind':'note_on','channel':0,'key':note,'velocity':100}]
  assert c['constant_protocol']==proposal['constant_protocol'] and c['prefix_scope']==proposal['prefix_scope']
  assert c['prefix_scope']['expected_audio'] is None and c['prefix_scope']['finite_prefix_corruption_can_pass']
  assert c['event_convention']==proposal['event_convention'] and c['metric_rules']==proposal['metric_rules_unchanged']
  assert (e['parameters']['MidiPitch'],e['parameters']['MidiGate'],e['parameters']['LfoOnOff'])==(1.,0.,0.)
  expected=base['metric'] if note==60 else {'kind':'modal','modes':[v[:15] for v in report['fixed_navigation_metric_all16']['modes']]}
  assert e['metric']==expected
  raw=(P/e['reference']['path']).read_bytes();assert len(raw)==e['reference']['bytes']==131072 and sha(raw)==e['reference']['sha256']
  frames=list(struct.iter_unpack('<ff',raw));assert all(math.isfinite(v) for row in frames for v in row)
  assert all(math.fsum(row[ch]*row[ch] for row in frames[4096:])>0 for ch in range(2))
  script=(P.parent/'depth-corpus-midi-pitch/raw'/('note'+str(note)+'.script')).read_text()
  parameters=[l.split() for l in script.splitlines() if l.startswith('param ')]
  assert [int(x[1]) for x in parameters]==list(range(38))
  assert [struct.pack('<f',float(x[2])) for x in parameters]==[struct.pack('<f',e['parameters'][k]) for k in e['parameter_order']]
  assert [l for l in script.splitlines() if l.startswith('event ')]==[f'event 1537 0x90 {note} 100']
 for ch in range(2):
  omitted=ep['DCO-031']['omitted'][ch];row=report['reference_mode_fits'][ch]['all16_mode_rows'][15]
  assert omitted['channel']==ch and omitted['mode']==16 and omitted['source_pointer']==f'/reference_mode_fits/{ch}/all16_mode_rows/15'
  assert omitted['diagnostic_full_vs_halves']==row['diagnostic_full_vs_halves']
  assert omitted['center_hz']==row['hypothesis']['center_hz']
  assert len(report['reference_mode_fits'][ch]['all16_mode_rows'])==16
 assert 'POST-OBSERVATION' in ep['DCO-031']['basis'] and ep['application_grade'] is None
 assert not ep['DCO-031']['native_pitch_or_coefficients_recovered'] and not ep['DCO-031']['complete_significant_gap_proved']

def main():
 if sys.argv[1:]!=['--check']:raise SystemExit('Only read-only --check; no write, capture, fit or replay mode.')
 inputs=load('inputs.json')
 for pin in inputs['immutable_pins']:verify(pin)
 if (P/'manifest.json').exists():
  manifest=load('manifest.json')
  assert {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and f.name!='manifest.json'}=={r['path'] for r in manifest['files']}
  for r in manifest['files']:
   b=(P/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
  assert load('eligibility-proposal.json')['method_and_review_frozen']
 before=(P/'spec-before-r4.md').read_text();after=(P/'spec-r5.md').read_text();delta=load('delta.json');rebuilt=before
 assert len(before.encode())==delta['before_bytes']==41194 and sha(before.encode())==delta['before_sha256']=='62ccc40debde55baf7fed54bbbc6eaa803f0d6a12f2a3b4b2841baabae6775d8'
 for op in delta['replacements']:
  if op.get('operation')=='append':rebuilt+=op['after']
  else:assert rebuilt.count(op['before'])==1;rebuilt=rebuilt.replace(op['before'],op['after'])
 assert rebuilt==after and len(after.encode())==delta['after_bytes'] and sha(after.encode())==delta['after_sha256']
 assert norm_ids(before)==norm_ids(after)==[f'REQ-DEVICE-CORPUS-{i:03d}' for i in range(1,14)]
 assert len(cases(before))==29 and cases(after)[:29]==cases(before) and len(cases(after))==31
 assert [r.split('|')[3].strip() for r in cases(after)].count('U')==4
 for i in range(2,13):
  start=f'### REQ-DEVICE-CORPUS-{i:03d} '
  assert before.split(start)[1].split('### REQ-DEVICE-CORPUS-')[0]==after.split(start)[1].split('### REQ-DEVICE-CORPUS-')[0]
 cs=load('cases-additions.json');ep=load('eligibility-proposal.json');validate(cs,ep)
 old=json.loads(Path(next(r['path'] for r in inputs['immutable_pins'] if r['path'].endswith('/handoff/device-corpus-v2/cases.json'))).read_text())
 ev=next(e for c in old['cases'] for e in c['evaluations'] if e['id']=='CORPUS-AUDIO-013-04')
 assert cs[0]['evaluation']['metric']==ev['metric']
 oldraw=Path(next(r['path'] for r in inputs['immutable_pins'] if r['path'].endswith('/reference/CORPUS-AUDIO-013-04.f32'))).read_bytes()
 assert oldraw[4096*8:]==(P/cs[0]['evaluation']['reference']['path']).read_bytes()[4096*8:] and oldraw!=(P/cs[0]['evaluation']['reference']['path']).read_bytes()
 rejected=[]
 def reject(label,c,e):
  try:validate(c,e)
  except AssertionError:rejected.append(label);return
  raise AssertionError('Accepted fixture: '+label)
 bad=copy.deepcopy(cs);bad[1]['evaluation']['events'][0]['frame']=1536;reject('extra-adapter-subtraction',bad,ep)
 bad=copy.deepcopy(cs);bad[1]['evaluation']['parameters']['MidiPitch']=0.;reject('wrong-host-vector',bad,ep)
 bad=copy.deepcopy(cs);bad[0]['prefix_scope']['expected_audio']='silence';reject('graded-prefix',bad,ep)
 bad=copy.deepcopy(cs);bad[1]['evaluation']['metric']['modes'][0].append({'center_hz':8371.840463952978,'cutoff_hz':100.});reject('silently-score-mode16',bad,ep)
 bad=copy.deepcopy(ep);bad['DCO-031']['basis']='Recovered native p1 poles';reject('native-pole-eligibility-promotion',cs,bad)
 bad=copy.deepcopy(ep);bad['DCO-031']['omitted'][1]['source_pointer']='/reference_mode_fits/0/all16_mode_rows/15';reject('wrong-omission-pointer',cs,bad)
 for f in P.rglob('*'):
  if f.is_file() and f.suffix in ['.md','.json','.py']:
   assert all(l==l.rstrip() for l in f.read_text().splitlines())
 print(json.dumps({'status':'PASS owner proposal data integrity only','sealed':(P/'manifest.json').exists(),'requirements':13,'cases':31,'old_rows_exact':29,'finite_proposed':27,'U_cases':4,'mode_points':[32,30],'negative_fixtures':rejected,'native_or_estimator_calls':0,'application_grade':None}))
if __name__=='__main__':main()
