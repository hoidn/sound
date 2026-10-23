"""Read-only private R7 text/JSON/hash check; no audio decoding or evaluator imports."""
from pathlib import Path
import copy, hashlib, json, re, sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REF = '1336d90115bd24c058e556aa95e9140014d168dad7111dec64eb8edd1d977e73'
AXES = [('preL',4096,8192,0),('preR',4096,8192,1),('postL',8192,16384,0),('postR',8192,16384,1)]

def ident(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def reconstruct(before, delta):
    text = before
    for op in delta['operations']:
        if op['kind'] == 'append':
            assert op['before'] == ''
            text += op['after']
        else:
            assert text.count(op['before']) == 1
            if op['kind'] == 'metadata-only':
                assert op['before'] == 'revision: 6\n' and op['after'] == 'revision: 7\n'
            else:
                assert op['kind'] == 'insert-before' and op['after'].endswith(op['before'])
            text = text.replace(op['before'],op['after'],1)
    return text

def rows(text): return re.findall(r'^\| DCO-\d{3} \|.*$',text,re.M)
def ids(text): return re.findall(r'^### (REQ-DEVICE-CORPUS-\d{3}) —',text,re.M)
def clause13(text): return text.split('### REQ-DEVICE-CORPUS-013',1)[1].split('\n## Timing and state',1)[0]

def validate(before, text, delta, case, old_eval, provenance, results):
    assert text == reconstruct(before,delta)
    assert ids(text) == ids(before) and len(ids(text)) == 13
    assert len(rows(before)) == 32 and len(rows(text)) == 33
    assert all(row in rows(text) for row in rows(before))
    assert clause13(text) == clause13(before)
    assert [r.split('|')[1].strip() for r in rows(text)] == ['DCO-'+str(i).zfill(3) for i in range(1,34)]
    assert case['id'] == 'DCO-033' and case['requirements'] == ['REQ-DEVICE-CORPUS-001','REQ-DEVICE-CORPUS-012']
    e = case['evaluation']
    for k in ['sample_rate_hz','frames','block_frames','signal','parameters','parameter_order','before_parameters','after_parameters']:
        assert e[k] == old_eval[k]
    assert e['events'] == [] and e['metric'] == {'kind':'pickup_step_waveform'}
    assert e['reference'] == {'path':'../depth-corpus-pickup-step-capture/raw/left-step.f32','bytes':131072,'sha256':REF}
    updates = case['parameter_updates']
    assert len(updates) == 1 and {k:updates[0][k] for k in ['frame','index','parameter','value']} == {
        'frame':8192,'index':15,'parameter':'ListeningXL','value':0.75}
    p = case['constant_protocol']
    assert p['process_segments_frames'] == [8192,8192] and p['same_instance_across_segments']
    assert p['input_present_each_block'] and p['reference_MXCSR'] == '0x1f80' and p['reference_time_seed'] == 0
    assert p['transport'] == {'playing':0,'position':0,'tempo_bpm':120,'position_advanced':False}
    assert all(p[k] is True for k in ['fresh_instance','no_reset','no_warmup','no_input_restart','no_unlisted_events','no_unlisted_parameter_updates'])
    m = case['metric_rules']
    assert m['kind'] == 'pickup_step_waveform' and m['max_relative_RMS'] == .01 and m['acceptance_epsilon'] == 0
    assert m['axes'] == [dict(axis=a,frames_half_open=[lo,hi],channel=c) for a,lo,hi,c in AXES]
    assert m['positive_reference_and_candidate_energy_in_EACH_axis'] is True
    assert m['full_file_finite_and_exact_length'] is True and m['reference_identity_required'] is True
    assert m['alignment_gain_phase_offset_fitting_or_channel_mixing'] is False
    assert case['prefix_scope']['frames_inclusive'] == [0,4095] and case['prefix_scope']['expected_audio'] is None
    assert case['candidate_or_application_grade'] is None
    limits = case['scope_limits']
    assert limits['4000_frame_movement_or_8_frame_latency_proved'] is False and limits['stored_position_A1_accepted'] is False
    assert limits['general_right_invariance'] is None and limits['new_invariance_claims'] is False
    for token in ['FOUR independent checks','including the first eight equal frames','0.8990030348930524','0.005000000371140732','finite-prefix123','All174old modal omissions']:
        assert token in text,token
    assert provenance['comparison_count'] == results['comparison_count'] == 38
    assert provenance['axis_records'] == results['axis_records'] == 152
    assert provenance['requirements_reported_pass'] == len(results['requirements']) == 89
    assert all(v['pass'] for v in results['requirements'])
    assert provenance['valid_axis_records'] == sum(v['valid'] for r in results['comparisons'] for v in r['result']['axes']) == 108
    assert provenance['invalid_axis_records'] == 44 and provenance['grade'] is None
    ledger = provenance['all38_actual_results_retained_by_exact_pointer']
    assert len(ledger) == 38
    for i,(record,actual) in enumerate(zip(ledger,results['comparisons'])):
        assert record == {'name':actual['name'],'pointer':f'/comparisons/{i}',
            'valid':actual['result']['valid'],'pass':actual['result']['pass'],
            'axis_order':['preL','preR','postL','postR'],
            'axis_errors':[v['error'] for v in actual['result']['axes']],
            'axis_validity':[v['valid'] for v in actual['result']['axes']]}

def main():
    if sys.argv[1:] not in (['--check-draft'],['--check']):
        raise SystemExit('Read-only --check-draft/--check only; no source/evaluator/native replay.')
    inputs = json.loads((HERE/'inputs.json').read_text())
    watched = {Path(r['path']) for r in inputs['pins']} | {p for p in HERE.iterdir() if p.is_file()}
    for r in inputs['pins']: assert ident(Path(r['path'])) == {k:r[k] for k in ['path','bytes','sha256']}
    roles = {r['role']:Path(r['path']) for r in inputs['pins']}
    for role in ['before_R6_manifest','capture_manifest','actual_validation_manifest','published_v4_manifest']:
        parent = roles[role]
        for r in json.loads(parent.read_text())['files']:
            p=parent.parent/r['path']; raw=p.read_bytes()
            assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'];watched.add(p)
    before_watch = {str(p):ident(p) for p in watched}
    before = roles['before_R6_spec'].read_text()
    assert len(before.encode())==58472 and hashlib.sha256(before.encode()).hexdigest()=='07a89f25de6b3c987d448e0e049bdd7dfaec52f479532b3aca3faddedcd511cd'
    text=(HERE/'spec-r7.md').read_text();delta=json.loads((HERE/'delta.json').read_text())
    cases=json.loads((HERE/'cases-additions.json').read_text());assert len(cases)==1
    old_eval=json.loads(roles['published_v4_cases'].read_text())['cases'][5]['evaluations'][0]
    assert old_eval['id']=='CORPUS-AUDIO-006-01'
    provenance=json.loads((HERE/'provenance.json').read_text())
    results=json.loads(roles['actual_validation_results'].read_text())
    validate(before,text,delta,cases[0],old_eval,provenance,results)
    assert delta['after_bytes']==len(text.encode()) and delta['after_sha256']==hashlib.sha256(text.encode()).hexdigest()
    binding=json.loads((HERE/'method-review-binding.json').read_text())
    bound=binding['actual_method_review'] is not None
    if bound:
        row=binding['actual_method_review'];path=Path(row['path']);assert ident(path)==row
        review=json.loads(path.read_text())
        assert review['disposition']=='APPROVED_PARTIAL_FINITE_METHOD_VALIDATION' and review['required_findings']==[]
        assert binding['owner_review'] is None and binding['adopted'] is False
        assert hashlib.sha256(roles['actual_validation_manifest'].read_bytes()).hexdigest() in json.dumps(review)
        assert provenance['actual_method_review_binding']==row
        watched.add(path);before_watch[str(path)]=ident(path)
    if sys.argv[1:] == ['--check']: assert bound,'Actual-method review must be bound before final author freeze.'
    rejected=[]
    def rejects(label, *, changed_case=None, changed_text=None, changed_provenance=None):
        try:validate(before,changed_text or text,delta,changed_case or cases[0],old_eval,changed_provenance or provenance,results)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('unsafe variant accepted: '+label)
    for label,mutate in [
        ('wrong update index',lambda c:c['parameter_updates'][0].update(index=16)),
        ('wrong update boundary',lambda c:c['parameter_updates'][0].update(frame=8200)),
        ('wrong update value',lambda c:c['parameter_updates'][0].update(value=.5)),
        ('wrong reference hash',lambda c:c['evaluation']['reference'].update(sha256='0'*64)),
        ('missing preL',lambda c:c['metric_rules']['axes'].pop(0)),
        ('wrong budget',lambda c:c['metric_rules'].update(max_relative_RMS=.1)),
        ('acceptance epsilon',lambda c:c['metric_rules'].update(acceptance_epsilon=1e-6)),
        ('missing positive guard',lambda c:c['metric_rules'].update(positive_reference_and_candidate_energy_in_EACH_axis=False)),
        ('invented duration',lambda c:c['scope_limits'].update({'4000_frame_movement_or_8_frame_latency_proved':True}))]:
        bad=copy.deepcopy(cases[0]);mutate(bad);rejects(label,changed_case=bad)
    rejects('old013 changed',changed_text=text.replace('### REQ-DEVICE-CORPUS-013 — MIDI side-chain features','### REQ-DEVICE-CORPUS-013 — changed old law',1))
    bad=copy.deepcopy(provenance);bad['all38_actual_results_retained_by_exact_pointer'][33]['pass']=False
    rejects('erased concentrated pass',changed_provenance=bad)
    seal=HERE/'manifest.json'
    if seal.exists():
        m=json.loads(seal.read_text());assert {r['path'] for r in m['files']}=={p.name for p in HERE.iterdir() if p.is_file() and p!=seal}
        for r in m['files']:
            raw=(HERE/r['path']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
    links=0
    for p,origin in [(HERE/'README.md',HERE),(HERE/'spec-r7.md',ROOT/'wiki/specs')]:
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            path=target.split('#',1)[0]
            if path and not path.startswith(('http:','https:')):assert (origin/path).exists(),target;links+=1
    for p in HERE.iterdir():
        if p.is_file():assert p.read_text().endswith('\n') and all(s.rstrip()==s for s in p.read_text().splitlines())
    assert before_watch=={str(p):ident(p) for p in watched}
    print(json.dumps({'status':'PASS private proposed owner integrity only','actual_method_review_bound':bound,
        'sealed':seal.exists(),'requirements':13,'cases':33,'old_rows_preserved':32,'old013_literal':True,
        'new_case':'DCO-033','actual_source_comparisons':38,'actual_source_axis_records':152,
        'unsafe_variants_rejected':rejected,'links':links,'watched':len(watched),'watch_unchanged':True,
        'new_metric_calculations':0,'old_tool_imports_or_replays':0,'native_calls':0,'grade':None},indent=2))

if __name__=='__main__':main()
