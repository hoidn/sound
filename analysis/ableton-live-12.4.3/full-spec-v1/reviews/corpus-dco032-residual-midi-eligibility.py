from pathlib import Path
import json,hashlib,struct,copy,datetime
B=Path('analysis/ableton-live-12.4.3/full-spec-v1');D=B/'reviews';src=D/'corpus-dco032-midi-axis-eligibility.json';raw=src.read_bytes();assert len(raw)==745014 and hashlib.sha256(raw).hexdigest()=='3e2b78c965b23934d56ac5620aa1b699025ca093e839ecfb5a68b9af7e7e6702';r=json.loads(raw)
def sha(x):return hashlib.sha256(x).hexdigest()
def key(events):return json.dumps(events,separators=(',',':'))
lines={x['line']:x['literal'] for x in r['complete_nonparameter_commands']}
for x in r['full_ordered38_words']:lines[x['line']]=f"param {x['index']} {x['token']}"
def script(events):
 ls=dict(lines)
 for lineno,(frame,status,k,v) in zip((43,44),events):ls[lineno]=f'event {frame} 0x{status:02x} {k} {v}'
 return ('\n'.join(ls[i] for i in range(1,49))+'\n').encode()
base=r['baseline_events'];assert base==[[1537,144,60,100],[3073,128,60,64]]
assert len(script(base))==735 and sha(script(base))==r['baseline_script_pin']['sha256']
axes=[('off_key',range(128),1,2,60),('on_channel',range(16),0,1,0),('off_channel',range(16),1,1,0)];aliases=[];hist={}
for axis,domain,ei,field,bv in axes:
 for v in domain:
  e=copy.deepcopy(base);e[ei][field]=(144 if ei==0 else 128)+v if field==1 else v;k=key(e);a=dict(axis=axis,value=v,events=e,history_key=k)
  aliases.append(a)
  if k not in hist:
   bb=script(e);baseline=e==base;hist[k]=dict(id=f'CGR-U{len(hist):03d}',events=e,packed16_events_le=[struct.pack('<qBBB5x',*x).hex() for x in e],script_utf8_bytes=len(bb),script_utf8_sha256=sha(bb),fixed_history=r['fixed_history'],alias_ids=[],provenance='approved-DCO032-input-reference' if baseline else 'missing-in-bounded-input-cut',existing_case_refs=['DCO-032'] if baseline else [],new_pid=None,new_receipt=None,new_metrics=None,waveform_prior=None,portable_expected=None,portable_comparator=None,grade=None,new_application_predicate_proof=False)
  hist[k]['alias_ids'].append(f'{axis}:{v}');a['id']=hist[k]['id']
expected_hist=list(hist.values());existing_events={key(x['events']) for x in r['histories']};intersection=set(hist)&existing_events;assert intersection=={key(base)}
def validate(aa,hh):
 assert len(aa)==160 and len(hh)==158 and len({key(x['events']) for x in hh})==158
 assert aa==aliases and hh==expected_hist
 assert sum(x['provenance']=='approved-DCO032-input-reference' for x in hh)==1 and sum(x['existing_case_refs']==['DCO-032'] for x in hh)==1
 for x in hh:
  e=x['events'];assert e[0][0]==1537 and e[1][0]==3073 and e[0][3]==100 and e[1][3]==64 and x['fixed_history']==r['fixed_history']
  assert x['packed16_events_le']==[struct.pack('<qBBB5x',*v).hex() for v in e] and x['script_utf8_sha256']==sha(script(e))
  assert all(x[k] is None for k in ['new_pid','new_receipt','new_metrics','waveform_prior','portable_expected','portable_comparator','grade']) and x['new_application_predicate_proof'] is False
validate(aliases,expected_hist);neg=[]
for label,field,val in [('wrongOffkey', 'events', [[1537,144,0,100],[3073,128,0,64]]),('wrongframe','events',[[1537,144,60,100],[3074,128,0,64]]),('oldPID','new_pid',1),('criterion','portable_expected',0),('grade','grade','PASS'),('applicationproof','new_application_predicate_proof',True),('roundedscript','script_utf8_sha256','0'*64),('missingpacked','packed16_events_le',[])]:
 h=copy.deepcopy(expected_hist);assert h[0][field]!=val;h[0][field]=val
 try:validate(aliases,h)
 except AssertionError:neg.append(label)
 else:raise AssertionError('accepted '+label)
for label,a,h in [('omitEdge',aliases[:-1],expected_hist),('parameteronlyCollapse',aliases,expected_hist[:1]),('omitHistory',aliases,expected_hist[:-1])]:
 try:validate(a,h)
 except AssertionError:neg.append(label)
 else:raise AssertionError('accepted '+label)
report=dict(schema='corpus-dco032-residual-three-independent-midi-byte-axes-eligibility-v1',author='Root',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='CONCRETE_INPUT_METADATA_ONLY',capture_selected=False,authority=dict(path=str(src),bytes=len(raw),sha256=sha(raw)),admitted_loader=r['admitted_loader'],bundle=r['bundle'],x86_slice=r['x86_slice'],input=r['I1_input'],original_ordered38_words=r['full_ordered38_words'],parameter_vector_sha256=r['parameter_vector_sha256'],parsed_binary64_token_sha256=r['parsed_binary64_token_sha256'],fixed_history=r['fixed_history'],old_recorded_environment=r['old_recorded_environment'],baseline_events=base,baseline_script_pin=r['baseline_script_pin'],counts=dict(aliases=160,whole_histories=158,missing=157,inherited=1,baseline_aliases=3),axes=[dict(axis=axis,domain=[min(domain),max(domain)],varying_event=ei,varying_field=field,baseline=bv) for axis,domain,ei,field,bv in axes],aliases=aliases,histories=expected_hist,bounded_intersections=dict(queued_four_axis_input_catalog=dict(aliases=400,histories=397,overlap='ONE DCO032 baseline only; no old/new actual approval inferred',matched_events=base),older_noevent_and_heldOn='Different eventcount; inherit pinned input-only assessment, no old file read',nine_approved_gate_protocols='Same bounded exclusion as pinned authority; only DCO032 endpoint context matches',no_global_absence_claim=True),input_integrity=dict(status='PASS',negative_controls=neg,exact_original735byte_baseline_reconstructed=True,parameteronly_dedup_forbidden=True),prospective=dict(children=157,selected_direct_exports=157*73,CalcA=157*32,raw_stereo_bytes=157*16384*8,initializers_and_all_nested=None,artifact_budget='Rawminimum20578304B plus logs/scripts/JSON/review/owner overhead; not reserved; no captureselected'),read_scope='Only pinned prior INPUTeligibility metadata, events/originaldecimal/f64/nonparametercommand declarations; no old script/sourcebehavior/raw/audio/numeric/provider/model/actual review or original execution. A read-only metadata discovery printed no matching historical field then StopIteration before any output, no bytes changed.',qualifications=['OffkeyONLY keepsOnkey60; OnchannelONLY keepsOffstatus80; OffchannelONLY keepsOnstatus90. No matchingkey/channelpair or crossproduct/new event type/timing/construction.','Threebaselinealiases ONE inheritedDCO032 INPUTapproval; no newPIDreceiptmetric/oldcriterion/modalbudget transfer. Queued396 actual not reread or treatedapproved.','NULLportablecriteria/grades and newappFalse; no velocity0/unmatchedchannel/key release law, f0fitmetricwindowtolerancecalibration/generalMIDI/publicARM/sourceFP/default/OSexec/provider/ABI/currentreceiver proof. Existing fixedhistory/sourceversion/fsync/cleanup qualifiers persist.'],new_IDs=0,new_original_calls=0,required_unsupported='U',product='OPEN')
out=D/'corpus-dco032-residual-midi-axis-eligibility.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n');out.chmod(0o444);print(len(out.read_bytes()),sha(out.read_bytes()),'PASS',len(neg),'controls')
