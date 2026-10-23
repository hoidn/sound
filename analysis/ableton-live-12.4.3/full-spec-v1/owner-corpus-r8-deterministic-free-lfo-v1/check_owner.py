#!/usr/bin/env python3
"""Owner-only evidence join/preservation checks; no actual/source/audio/provider reads."""
import copy,hashlib,json,pathlib,re,sys
H=pathlib.Path(__file__).resolve().parent;ROOT=H.parents[3]
def load(n):return json.loads((H/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical_hash(d):return sha(json.dumps(d,sort_keys=True,separators=(',',':')).encode())
def fragments():return {n:(H/n).read_text() for n in ['scope-note.md','annex.md','revision-row.md']}
def inserted(op,fr):return op['literal'] if 'literal' in op else fr[op['fragment']]
def forward(text,delta,fr):
 for op in delta['operations']:
  if op['kind']=='replace-once':assert text.count(op['before'])==1;text=text.replace(op['before'],op['after'],1)
  else:assert op['kind']=='insert-before-once' and text.count(op['anchor'])==1;text=text.replace(op['anchor'],inserted(op,fr)+op['anchor'],1)
 return text
def reverse(text,delta,fr):
 for op in reversed(delta['operations']):
  if op['kind']=='replace-once':assert text.count(op['after'])==1;text=text.replace(op['after'],op['before'],1)
  else:
   source=inserted(op,fr)+op['anchor'];assert text.count(source)==1;text=text.replace(source,op['anchor'],1)
 return text

def requirements(text):
 rows=[]
 for m in re.finditer(r'^### (REQ-DEVICE-CORPUS-\d{3})[^\n]*\n',text,re.M):
  end=text.find('\n### ',m.end());end=end if end!=-1 else text.index('\n## Timing and state',m.end());b=text[m.start():end].encode();rows.append({'id':m[1],'bytes':len(b),'sha256':sha(b)})
 return rows

def case_rows(text):return [{'id':l.split('|')[1].strip(),'bytes':len(l.encode()),'sha256':sha(l.encode())} for l in text.splitlines(keepends=True) if re.match(r'^\| DCO-\d{3} \|',l)]
def block(text,heading):
 start=text.index(heading+'\n');end=text.find('\n## ',start+3);return text[start:end if end!=-1 else len(text)].encode()
def preservation(base,after,before,delta,fr):
 assert len(base.encode())==before['owner']['bytes'] and sha(base.encode())==before['owner']['sha256']==delta['base_sha256']
 assert reverse(after,delta,fr)==base and forward(base,delta,fr)==after
 old=requirements(base);new=requirements(after);assert old==before['requirements'] and [r['id'] for r in new]==[r['id'] for r in old] and len(new)==13
 assert all(a==b for a,b in zip(old,new) if a['id']!='REQ-DEVICE-CORPUS-011')
 assert [r for r in case_rows(after) if int(r['id'][4:])<=33]==before['case_rows']==case_rows(base)
 assert [r['id'] for r in case_rows(after)]==[f'DCO-{i:03d}' for i in range(1,37)]
 for q in before['unchanged_scope_blocks']:
  b=block(after,q['heading']);assert len(b)==q['bytes'] and sha(b)==q['sha256'] and b==block(base,q['heading'])
 assert before['released_groups']==len(before['group_hashes'])==27 and before['released_evaluations']==len(before['evaluation_object_hashes'])==73
 assert len({r['id'] for r in before['evaluation_object_hashes']})==73
 assert 'revision: 8\n' in after and 'updated: 2026-10-21\n' in after

def mapping(cat,cases,review,pin,hist):
 assert review['disposition']==pin['disposition']=='APPROVED_TWO_ONCE_ONLY_CONTINUATION_OBSERVATIONS_AND_FULL_FIVE_MEMBER_FINITE_CATALOG' and not review['blocking_findings']
 assert pin['frozen_actual_manifest']==review['frozen_packet']['manifest'] and hist['approved_continuation_history']==review['history']
 assert hist['partial_review']['sha256']=='009f25f09172e6741c6927711d1ea2adc21194a38fddc942ec04ec0f44778df1'
 assert len(cat)==5 and [r['shape'] for r in cat]==list(range(5)) and [c['id'] for c in cases]==['DCO-034','DCO-035','DCO-036'] and [c['shape'] for c in cases]==[1,2,4]
 summary=review['approved_summary'];assert summary['whole_deterministic_finite_catalog_complete'] and summary['logical_members']==5 and [x['shape'] for x in summary['excluded_random_shapes']]==[5,6]
 bycase={c['shape']:c for c in cases};points=summary['approved_points']
 for r,q in zip(cat,points):
  s=r['shape'];assert q['shape']==s and r['name']==q['name'] and len(r['parameter_bits32'])==38 and r['parameter_bits32']==q['parameter_bits32'] and r['supplied_input']==summary['supplied_input']
  base=points[0]['parameter_bits32'];assert all(a==b for i,(a,b) in enumerate(zip(r['parameter_bits32'],base)) if i!=18)
  out=q.get('output') or q['historical']['output'];assert r['output_reference_identity']==out and out['bytes']==131072
  j=r['approved_review_join'];assert j=={'report_sha256':pin['report']['sha256'],'point_pointer':f'/approved_summary/approved_points/{s}','point_canonical_sha256':canonical_hash(q)}
  for key in ['native_waveform_prior_expected','new_waveform_expectation','candidate_comparator','portable_expected','portable_comparator','grade','release']:assert r[key] is None
  if s in (0,3):assert r['new_case_id'] is None and r['existing_case_id']=={0:'DCO-020',3:'DCO-029'}[s]
  else:
   c=bycase[s];assert r['new_case_id']==c['id'] and r['existing_case_id'] is None and c['kind']=='U' and c['evidence']=='X observation / U acceptance criterion' and c['requirement']=='REQ-DEVICE-CORPUS-011'
   for key in ['native_waveform_prior_expected','new_waveform_expectation','candidate_comparator','portable_expected','portable_comparator','grade','release']:assert c[key] is None
   assert c['name']==r['name'] and c['parameter_bits32']==r['parameter_bits32'] and c['supplied_input']==r['supplied_input'] and c['reference']==out and c['approved_review_join']==j
 assert summary['supplied_input']['rate_argument']==44100 and summary['supplied_input']['block']==512 and summary['supplied_input']['frames']==16384
 assert summary['supplied_input']['environment']['XDEV_TIME']=='0' and summary['supplied_input']['environment']['XDEV_LIBM_ULP']=='0'

def controls(cat,cases,review,pin,hist,base,after,before,delta,fr):
 passed=[]
 for label,mut in [('missing-member',lambda x,y,z:x.pop()),('duplicate-shape',lambda x,y,z:x[2].update(shape=1)),('extra-old-ID',lambda x,y,z:x[0].update(new_case_id='DCO-037')),('wrong-ID',lambda x,y,z:y[0].update(id='DCO-099')),('P-candidate-case',lambda x,y,z:y[0].update(kind='P')),('invented-criterion',lambda x,y,z:y[0].update(candidate_comparator={'RMS':0.01})),('waveform-fit',lambda x,y,z:x[1].update(new_waveform_expectation='square')),('portable-exact',lambda x,y,z:x[1].update(portable_comparator='bitexactARM')),('grade-invented',lambda x,y,z:y[0].update(grade='PASS')),('wrong-param18',lambda x,y,z:x[1]['parameter_bits32'].__setitem__(18,'00000000')),('cross-shape-param20',lambda x,y,z:x[1]['parameter_bits32'].__setitem__(20,'00000000')),('wrong-rate-input',lambda x,y,z:y[0]['supplied_input'].update(rate_argument=48000)),('wrong-reference',lambda x,y,z:x[1]['output_reference_identity'].update(sha256='0'*64)),('wrong-point-pointer',lambda x,y,z:x[1]['approved_review_join'].update(point_pointer='/approved_summary/approved_points/2')),('wrong-point-hash',lambda x,y,z:x[1]['approved_review_join'].update(point_canonical_sha256='0'*64)),('unapproved-review',lambda x,y,z:z.update(disposition='PENDING'))]:
  x,y,z=copy.deepcopy(cat),copy.deepcopy(cases),copy.deepcopy(review);mut(x,y,z)
  try:mapping(x,y,z,pin,hist)
  except (AssertionError,KeyError,IndexError,ValueError):passed.append(label)
  else:raise AssertionError('accepted '+label)
 for label,wrong in [('old-case-edit',after.replace('| DCO-001 |','| DCO-099 |',1)),('other-clause-edit',after.replace('### REQ-DEVICE-CORPUS-001 — reference renders define the output','### REQ-DEVICE-CORPUS-001 — changed',1)),('old-metric-edit',after.replace('## Comparison metric','## Changed comparison metric',1))]:
  try:preservation(base,wrong,before,delta,fr)
  except (AssertionError,KeyError,ValueError):passed.append(label)
  else:raise AssertionError('accepted '+label)
 z=copy.deepcopy(hist);z['approved_continuation_history']['Square_retry']=True
 try:mapping(cat,cases,review,pin,z)
 except AssertionError:passed.append('Square-retry-history-erased')
 else:raise AssertionError('accepted history rewrite')
 return passed

def main():
 assert sys.argv[1:]==['--check'];before=load('owner-before.json');delta=load('delta.json');fr=fragments();comp=load('composition.json');p=ROOT/'wiki/specs/device-corpus.md';assert str(p)==before['owner']['path'];text=p.read_text()
 if sha(text.encode())==before['owner']['sha256']:base=text;after=forward(base,delta,fr)
 else:assert sha(text.encode())==comp['owner_after_sha256'];after=text;base=reverse(after,delta,fr)
 preservation(base,after,before,delta,fr);assert len(after.encode())==comp['owner_after_bytes'] and sha(after.encode())==comp['owner_after_sha256']
 assert len(delta['operations'])==7
 pin=load('review-pin.json');reportpath=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-deterministic-free-lfo-continuation-v1-review.json';assert str(reportpath)==pin['report']['path'];raw=reportpath.read_bytes();assert len(raw)==pin['report']['bytes'] and sha(raw)==pin['report']['sha256'];review=json.loads(raw)
 cat=load('catalog.json');cases=load('new-cases.json');hist=load('history-qualification.json');mapping(cat,cases,review,pin,hist);negative=controls(cat,cases,review,pin,hist,base,after,before,delta,fr)
 result={'status':'PASS','whole_catalog':5,'new_observation_only_ids':3,'old_sine_ramp_refs_no_new_ID':2,'all_requirement_IDs':13,'other_whole_bodies_exact':12,'old_REQ011_recoverable_exact':True,'old_rows_exact':33,'old_scope_blocks_exact':4,'released73_evaluation_hashes_unchanged':True,'new_comparators_NULL':3,'negative_controls':negative,'root_actual_approval_inherited':True,'actual_source_audio_numeric_rereview':False,'canonical_writes':0,'original_calls':0,'owner_after_bytes':len(after.encode()),'owner_after_sha256':sha(after.encode())}
 if (H/'manifest.json').exists():
  m=load('manifest.json');assert {p.relative_to(H).as_posix() for p in H.rglob('*') if p.is_file()}=={'manifest.json'}|{f['path'] for f in m['files']}
  for f in m['files']:
   b=(H/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
  assert load('author-check.json')==result
 else:
  with (H/'author-check.json').open('w') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(result))
if __name__=='__main__':main()
