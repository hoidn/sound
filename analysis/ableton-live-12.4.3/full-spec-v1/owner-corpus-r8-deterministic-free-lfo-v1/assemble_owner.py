#!/usr/bin/env python3
"""Initial narrow owner assembly from canonical R7 + approved Root summary ONLY."""
import hashlib,json,pathlib,re,os
H=pathlib.Path(__file__).resolve().parent;B=H.parent;ROOT=H.parents[3];P=ROOT/'wiki/specs/device-corpus.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):b=p.read_bytes();return {'path':str(p.resolve()),'bytes':len(b),'sha256':sha(b)}
def save(n,d):
 with (H/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
assert not (H/'owner-before.json').exists();raw=P.read_bytes();text=raw.decode();assert 'revision: 7\n' in text
reviewpath=B/'reviews/corpus-deterministic-free-lfo-continuation-v1-review.json';rp=pin(reviewpath);assert rp['bytes']==23871 and rp['sha256']=='6427a0e75470c0758dbfd4ea4afae49d6c6b3261c43d854fa705f69d0bc58f6b';review=json.loads(reviewpath.read_text());assert review['disposition']=='APPROVED_TWO_ONCE_ONLY_CONTINUATION_OBSERVATIONS_AND_FULL_FIVE_MEMBER_FINITE_CATALOG';summary=review['approved_summary'];points=summary['approved_points'];assert [q['shape'] for q in points]==list(range(5))
reqs=[]
for m in re.finditer(r'^### (REQ-DEVICE-CORPUS-\d{3})[^\n]*\n',text,re.M):
 end=text.find('\n### ',m.end());end=end if end!=-1 else text.index('\n## Timing and state',m.end());b=text[m.start():end].encode();reqs.append({'id':m[1],'bytes':len(b),'sha256':sha(b)})
oldrows=[{'id':l.split('|')[1].strip(),'bytes':len(l.encode()),'sha256':sha(l.encode())} for l in text.splitlines(keepends=True) if re.match(r'^\| DCO-\d{3} \|',l)]
assert len(reqs)==13 and len(oldrows)==33 and [r['id'] for r in oldrows]==[f'DCO-{i:03d}' for i in range(1,34)]
blocks=[]
for heading in ['## Timing and state','## R7 scope addition: one pickup-step metric','## Comparison metric','## Open questions']:
 start=text.index(heading+'\n');end=text.find('\n## ',start+3);b=text[start:end if end!=-1 else len(text)].encode();blocks.append({'heading':heading,'bytes':len(b),'sha256':sha(b)})
meta=json.loads((B/'family-corpus-routes-v1/input-sets.json').read_text())['sets']['released-evaluations'];providers=json.loads((B/'family-corpus-routes-v1/pins.json').read_text())['providers'];releasepin=next(p for p in providers if p['id']=='v5-cases');assert meta['groups']==27 and meta['evaluations']==73
save('owner-before.json',{'owner':pin(P),'revision':7,'requirements':reqs,'case_rows':oldrows,'unchanged_scope_blocks':blocks,'release_cases_inherited_pin':releasepin,'released_groups':27,'released_evaluations':73,'evaluation_object_hashes':[{'id':r['id'],'pointer':r['pointer'],'sha256':r['sha256']} for r in meta['records']],'group_hashes':meta['group_sha256'],'scope':'PriorR7bytes hashed; no full snapshot/casebodycopy. Existing tolerances/finiteobjects preserved, no handoff release/audio/source reread.'})
cat=[];cases=[];newids={1:'DCO-034',2:'DCO-035',4:'DCO-036'}
for q in points:
 shape=q['shape'];caseid=newids.get(shape);pointsha=sha(json.dumps(q,sort_keys=True,separators=(',',':')).encode());output=q.get('output') or q['historical']['output']
 row={'shape':shape,'name':q['name'],'new_case_id':caseid,'existing_case_id':{0:'DCO-020',3:'DCO-029'}.get(shape),'parameter_bits32':q['parameter_bits32'],'supplied_input':summary['supplied_input'],'output_reference_identity':output,'native_waveform_prior_expected':None,'new_waveform_expectation':None,'candidate_comparator':None,'portable_expected':None,'portable_comparator':None,'grade':None,'release':None,'approved_review_join':{'report_sha256':rp['sha256'],'point_pointer':f'/approved_summary/approved_points/{shape}','point_canonical_sha256':pointsha},'history':q.get('historical'),'scope':'RetainedfiniteXobservation only; existingDCO020/029criteria unchanged and not transferred'};cat.append(row)
 if caseid:cases.append({'id':caseid,'requirement':'REQ-DEVICE-CORPUS-011','evidence':'X observation / U acceptance criterion','kind':'U','shape':shape,'name':q['name'],'parameter_bits32':q['parameter_bits32'],'supplied_input':summary['supplied_input'],'reference':output,'native_waveform_prior_expected':None,'new_waveform_expectation':None,'candidate_comparator':None,'portable_expected':None,'portable_comparator':None,'grade':None,'release':None,'approved_review_join':row['approved_review_join']})
save('catalog.json',cat);save('new-cases.json',cases);save('review-pin.json',{'report':rp,'disposition':review['disposition'],'frozen_actual_manifest':review['frozen_packet']['manifest'],'summary_pointer':'/approved_summary','sole_new_wording_mapping_ids_preservation_peer':'root','actual_approval_inherited_no_repeat':True});save('history-qualification.json',{'approved_continuation_history':review['history'],'partial_review':{'path':'analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-deterministic-free-lfo-v1-partial-review.json','bytes':33471,'sha256':'009f25f09172e6741c6927711d1ea2adc21194a38fddc942ec04ec0f44778df1','qualification_pointer':'/nonblocking_generator_qualification','frozen_failure_pointer':'/diagnosis'},'qualification':'SquareafterRate0guardfailure remainsapprovedpartial; falsephases/stalechildstatus andunusedpreparetailindex withauthor-reportedmanualpostgenerationinputwatchappend/no independentdurableinitialprepareproof retained. NewcontinuationRateopaque, no semanticclock/status inference. No oldpacket repairs/retries.'})
old='''  are not graded as general waveforms. Only Ramp Up now has the single finite audio
  expectation DCO-029 below; Square, Triangle, Ramp Down, Spin and other Ramp Up
  vectors remain unrendered here.'''
new='''  are not graded as general waveforms. Ramp Up retains the single finite audio
  expectation DCO-029 below. Square, Triangle and Ramp Down now have only the
  supplied-host observations DCO-034–036, with new waveform expectations and
  comparators NULL; Spin and other Ramp Up vectors remain unrendered here.'''
assert text.count(old)==1
addition='''- **X observations; U acceptance criterion.** DCO-034–036 retain the three fixed
  Free-LFO host-input outputs in the finite annex below. Their native waveform
  priors, new waveform expectations and candidate/portable comparators remain
  NULL. They do not recover internal shape laws, add a Hz/RMS budget, extend
  REQ-001's invariance claims or transfer DCO-020/029's criteria. A1, actual Live
  delivery, ARM/Apple, clock and state/lifecycle uncertainties remain unchanged.
'''
ops=[{'kind':'replace-once','before':'updated: 2026-10-20\n','after':'updated: 2026-10-21\n'},{'kind':'replace-once','before':'revision: 7\n','after':'revision: 8\n'},{'kind':'insert-before-once','anchor':'**Current owner disposition — 2026-10-20:**','fragment':'scope-note.md'},{'kind':'replace-once','before':old,'after':new},{'kind':'insert-before-once','anchor':'- **X, U.** Sample & Hold and Random Ramp draw from a generator','literal':addition},{'kind':'insert-before-once','anchor':'\n## Open questions\n','fragment':'annex.md'},{'kind':'insert-before-once','anchor':'\n**Historical R1–R3 release statements, retained as of those freezes.**','fragment':'revision-row.md'}]
save('delta.json',{'schema':'minimal-reversible-corpus-r8-delta-v1','owner_path':'wiki/specs/device-corpus.md','base_sha256':sha(raw),'operations':ops,'no_full_snapshot':True})
print(json.dumps({'owner_before':pin(P),'clauses':13,'old_rows':33,'new_ids':[c['id'] for c in cases],'numeric_or_actual_rereview':False}))
