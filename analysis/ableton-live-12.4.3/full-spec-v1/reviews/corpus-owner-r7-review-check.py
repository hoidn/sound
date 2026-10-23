"""Independent structural/provenance review only; no sample decoding or metric calls."""
from pathlib import Path
import hashlib,json,re,struct,subprocess,sys,datetime
if sys.argv[1:]!=['--check']:
    raise SystemExit('Only --check; no capture, numerical evaluator or write-mode option.')
ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
P=BASE/'corpus-owner-r7'
OUT=BASE/'reviews/corpus-owner-r7-review-evidence.json'
assert not OUT.exists(), 'Exclusive reviewer evidence exists'
def ident(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(p):return json.loads(p.read_bytes())
m=load(P/'manifest.json');assert ident(P/'manifest.json')['sha256']=='8fd118cec70dc0c22cdc8519d69805319f7c22d4738388af16dee995428c1786'
assert {x['path'] for x in m['files']}=={p.name for p in P.iterdir() if p.is_file() and p.name!='manifest.json'}
inputs=load(P/'inputs.json');roles={r['role']:Path(r['path']) for r in inputs['pins']}
watched={*P.iterdir(),Path(__file__),*roles.values(),ROOT/'wiki/specs/device-corpus.md'}
manifest_counts={}
for role in ['before_R6_manifest','capture_manifest','actual_validation_manifest','published_v4_manifest']:
    source=roles[role];records=load(source)['files'];manifest_counts[role]=len(records)
    for r in records:
        path=source.parent/r['path'];actual=ident(path)
        assert actual['bytes']==r['bytes'] and actual['sha256']==r['sha256'];watched.add(path)
for r in m['files']:
    actual=ident(P/r['path']);assert actual['bytes']==r['bytes'] and actual['sha256']==r['sha256']
for r in inputs['pins']:assert ident(Path(r['path']))=={k:r[k] for k in ['path','bytes','sha256']}
watched.add(roles['capture_manifest'].parent/'proposal.json')
before=[ident(p) for p in sorted(watched)]
old=roles['before_R6_spec'].read_text();new=(P/'spec-r7.md').read_text();delta=load(P/'delta.json')
assert len(old.encode())==58472 and ident(roles['before_R6_spec'])['sha256']=='07a89f25de6b3c987d448e0e049bdd7dfaec52f479532b3aca3faddedcd511cd'
assert len(new.encode())==65685 and ident(P/'spec-r7.md')['sha256']=='582404c4d55857b4eb792e3f307478d1f2d31a79257d3f9701bdd89661d14690'
text=old;ops=delta['operations'];assert len(ops)==10
for op in ops:
    if op['kind']=='append':assert op['before']=='';text+=op['after']
    else:
        assert text.count(op['before'])==1
        if op['kind']=='metadata-only':assert (op['before'],op['after'])==('revision: 6\n','revision: 7\n')
        else:assert op['kind']=='insert-before' and op['after'].endswith(op['before'])
        text=text.replace(op['before'],op['after'],1)
assert text==new
for op in reversed(ops):
    if op['kind']=='append':assert text.endswith(op['after']);text=text[:-len(op['after'])]
    else:assert text.count(op['after'])==1;text=text.replace(op['after'],op['before'],1)
assert text==old
rowpat=r'^\| DCO-\d{3} \|.*$';oldrows=re.findall(rowpat,old,re.M);newrows=re.findall(rowpat,new,re.M)
assert len(oldrows)==32 and newrows[:-1]==oldrows and len(newrows)==33
ids=lambda s:re.findall(r'^### (REQ-DEVICE-CORPUS-\d{3}) —',s,re.M)
assert ids(old)==ids(new)==['REQ-DEVICE-CORPUS-'+str(i).zfill(3) for i in range(1,14)]
body=lambda s,i:s.split('### REQ-DEVICE-CORPUS-'+str(i).zfill(3),1)[1].split('\n### REQ-',1)[0].split('\n## Timing and state',1)[0]
assert all(body(old,i)==body(new,i) for i in range(2,12)) and body(old,13)==body(new,13)
assert body(new,1).startswith(body(old,1)) and body(new,12).startswith(body(old,12))
assert sum(r.split('|')[3].strip()=='U' for r in newrows)==4
case,=load(P/'cases-additions.json');e=case['evaluation'];protocol=case['constant_protocol']
assert case['id']=='DCO-033' and case['requirements']==['REQ-DEVICE-CORPUS-001','REQ-DEVICE-CORPUS-012']
old_eval=load(roles['published_v4_cases'])['cases'][5]['evaluations'][0]
assert old_eval['id']=='CORPUS-AUDIO-006-01'
for key in ['sample_rate_hz','frames','block_frames','signal','parameters','parameter_order','before_parameters','after_parameters']:assert e[key]==old_eval[key]
assert len(e['parameter_order'])==len(e['parameters'])==38
capture=roles['capture_manifest'].parent;proposal=load(capture/'proposal.json')
assert e['parameters']==proposal['source_vector']['parameters'] and e['parameter_order']==proposal['source_vector']['parameter_order']
script=(capture/'raw/left-step.script').read_text().splitlines();assert script==proposal['scripts']['left-step']
parameters=[line.split() for line in script if line.startswith('param ')]
assert len(parameters)==39
for i,(command,index,value) in enumerate(parameters[:38]):
    assert int(index)==i and struct.pack('<f',float(value))==struct.pack('<f',e['parameters'][e['parameter_order'][i]])
assert parameters[-1]==['param','15','0.75']
assert [x for x in script if x.startswith('process ')]==['process 8192 512']*2
assert not any(x.startswith(('event ','reset','info','warm')) for x in script)
assert case['parameter_updates']==[{'frame':8192,'index':15,'parameter':'ListeningXL','value':0.75,'coordinate':'absolute host/test boundary after8192processedframes, before next512frameblock; not Live/internalonsetproof'}]
assert protocol['process_segments_frames']==[8192,8192] and protocol['same_instance_across_segments']
assert protocol['transport']=={'playing':0,'position':0,'tempo_bpm':120,'position_advanced':False}
assert protocol['reference_MXCSR']=='0x1f80' and protocol['reference_time_seed']==0 and protocol['reference_libm_perturbation']=='unset'
assert all(protocol[k] for k in ['input_present_each_block','fresh_instance','no_reset','no_warmup','no_input_restart','no_unlisted_events','no_unlisted_parameter_updates'])
assert e['events']==[] and e['reference']['sha256']=='1336d90115bd24c058e556aa95e9140014d168dad7111dec64eb8edd1d977e73'
assert ident(capture/'raw/left-step.f32')['sha256']==e['reference']['sha256'] and e['reference']['bytes']==131072
signal=roles['published_v4_cases'].parent/e['signal'];assert ident(signal)['sha256']==proposal['source_pins']['input']['sha256']
rules=case['metric_rules'];assert rules['axes']==[{'axis':a,'frames_half_open':[lo,hi],'channel':ch} for a,lo,hi,ch in [('preL',4096,8192,0),('preR',4096,8192,1),('postL',8192,16384,0),('postR',8192,16384,1)]]
assert rules['max_relative_RMS']==.01 and rules['acceptance_epsilon']==0
assert rules['positive_reference_and_candidate_energy_in_EACH_axis'] and rules['full_file_finite_and_exact_length'] and rules['reference_identity_required']
assert rules['alignment_gain_phase_offset_fitting_or_channel_mixing'] is False
assert case['prefix_scope']['frames_inclusive']==[0,4095] and case['prefix_scope']['expected_audio'] is None
assert case['candidate_or_application_grade'] is None
results=load(roles['actual_validation_results']);provenance=load(P/'provenance.json')
projections=provenance['all38_actual_results_retained_by_exact_pointer'];assert len(projections)==38
for i,row in enumerate(projections):
    pointer=row['pointer'];value=results
    for part in pointer.split('/')[1:]:value=value[int(part)] if isinstance(value,list) else value[part]
    assert pointer=='/comparisons/'+str(i)
    assert row=={'name':value['name'],'pointer':pointer,'valid':value['result']['valid'],'pass':value['result']['pass'],'axis_order':['preL','preR','postL','postR'],'axis_errors':[v['error'] for v in value['result']['axes']],'axis_validity':[v['valid'] for v in value['result']['axes']]}
assert provenance['axis_records']==sum(len(r['result']['axes']) for r in results['comparisons'])==152
assert provenance['valid_axis_records']==sum(v['valid'] for r in results['comparisons'] for v in r['result']['axes'])==108
assert provenance['invalid_axis_records']==44 and len(results['requirements'])==89 and all(x['pass'] for x in results['requirements'])
review=load(roles['actual_method_review']);assert ident(roles['actual_method_review'])['sha256']=='fad41d66e488702cff011632aedd712f422a9305a519b22038da38a7d2a8518d'
assert review['disposition']=='APPROVED_PARTIAL_FINITE_METHOD_VALIDATION' and review['required_findings']==[]
assert review['reviewed_packet']==ident(roles['actual_validation_manifest']) and review['reviewed_results']==ident(roles['actual_validation_results'])
binding=load(P/'method-review-binding.json');assert binding['actual_method_review']==ident(roles['actual_method_review'])
assert binding['adopted'] is False and binding['owner_review'] is None
runs=[]
for argument in ['--check','--write','--capture']:
    argv=['python3','-B',str(P/'check.py'),argument];r=subprocess.run(argv,capture_output=True,timeout=30)
    runs.append({'argv':argv,'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()})
    assert r.returncode==(0 if argument=='--check' else 1)
after=[ident(p) for p in sorted(watched)];assert before==after
outcome={'retained_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS independent structural/provenance review only','before':before,'after':after,'watch_unchanged':True,'watch_count':len(before),'owner_manifest':ident(P/'manifest.json'),'owner_spec':ident(P/'spec-r7.md'),'payloads':10,'tree_files':11,'provider_pins':len(inputs['pins']),'expanded_manifest_payloads':manifest_counts,'literal_delta_operations':10,'reverse_reconstructs_R6':True,'old_rows_exact':32,'requirement_ids':13,'finite_rows':29,'unknown_rows':4,'new_case':'DCO-033','initial_vector_values_and_order':38,'script_parameter_bits_checked':38,'new_update_index':15,'new_update_frame':8192,'new_update_value':0.75,'actual_projection_pointers':38,'axis_projections':152,'valid_axes':108,'invalid_axes':44,'method_required_checks_reported_true':89,'runs':runs,'numerical_evaluator_calls':0,'audio_sample_decodes':0,'old_tools_or_models':0,'original_calls':0,'grade':None}
with OUT.open('x') as f:json.dump(outcome,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in outcome.items() if k not in ['before','after','runs']},indent=2))
