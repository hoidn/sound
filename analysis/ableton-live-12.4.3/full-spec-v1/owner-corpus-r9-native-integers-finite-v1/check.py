#!/usr/bin/env python3
"""Only owner/data mapping validation; no actual packet, fixture, provider or execution."""
from pathlib import Path
import argparse,copy,hashlib,json,re
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def objsha(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def need(x,label):
 if not x:raise AssertionError(label)
def load(n):return json.loads((P/n).read_bytes())
def pinned(x):
 p=ROOT/x['path'];b=p.read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'pin '+x['path']);return b
def bodies(t):
 hs=list(re.finditer(r'^### (REQ-DEVICE-CORPUS-\d{3})[^\n]*\n',t,re.M));return {m[1]:t[m.start():hs[i+1].start() if i+1<len(hs) else t.index('\n## Timing and state',m.start())] for i,m in enumerate(hs)}
def validate(cases,cat,joins,qual,summary):
 vs=summary['approved_vectors'];need(len(cases)==57 and len(cat['vectors'])==63 and len(cat['aliases'])==69 and len(joins)==63 and len(vs)==63,'whole catalog')
 need([cat[k] for k in ['logical_aliases','unique_vectors','new_cases','inherited_existing_case_references','qualified_unnumbered_historical_metadata']]==[69,63,57,5,1],'declared units')
 need(cat['aliases']==summary['approved_aliases'] and cat['shared_input']==summary['shared_input'],'shared input and alias rows')
 need([x['case_id'] for x in cases]==[f'DCO-{i:03d}' for i in range(37,94)],'new IDs')
 need([x for x in cat['vectors'] if x['case_id']] == cases,'case projection')
 need(len({x['vector_sha256'] for x in cat['vectors']})==63,'unique vectors')
 refs={0:'DCO-020',1:'DCO-034',2:'DCO-035',3:'DCO-029',4:'DCO-036'}
 nextid=37
 for i,(c,v,j) in enumerate(zip(cat['vectors'],vs,joins)):
  fresh=v['disposition']=='fresh-selected';want=f'DCO-{nextid:03d}' if fresh else None
  if fresh:nextid+=1
  need(c['case_id']==want and c['vector_id']==v['id'] and c['approved_summary_pointer']==f'/approved_summary/approved_vectors/{i}' and c['approved_point_sha256']==objsha(v),'summary join')
  need(c['words']==v['words'] and c['vector_sha256']==v['vector_sha256'] and c['alias_ids']==v['alias_ids'] and c['first_alias']==v['first_alias'],'full input')
  need(c['provenance']==v['disposition'] and c['script']==v.get('script') and c['inherited_metadata']==v.get('inherited'),'provenance')
  need(c['common_qualification']=='qualification.json#/qualification' and c['new_application_predicate_proof'] is False,'common qualification/application U')
  need(all(c[k] is None for k in ['waveform_prior','new_expected_waveform','portable_expected','portable_comparator','grade','new_metrics']),'NULL criteria')
  need(j=={'vector_id':v['id'],'case_id':want,'existing_case_reference':c['existing_case_reference'],'approved_pointer':c['approved_summary_pointer'],'approved_point_sha256':objsha(v),'alias_ids':v['alias_ids']},'mapping row')
  if fresh:
   a=v['actual'];expected={k:a[k] for k in ['receipt_pointer','pid','utc_start','utc_end','audio','audio_stats']}
   expected.update({k:a['parsed'][k] for k in ['rate_return_observed','rate_return_semantics','direct_export_calls','CalcA']})
   need(c['native_observation']==expected and c['new_pid']==a['pid'] and c['new_receipt']==a['receipt_pointer'] and c['requirements']==['REQ-DEVICE-CORPUS-002'],'copied facts only')
   need(c['existing_case_reference'] is None and not c['qualification_only_unnumbered_shape5'],'fresh roles')
  else:
   need(c['native_observation'] is None and c['new_pid'] is None and c['new_receipt'] is None and c['requirements']==[],'no inherited fresh facts')
   is5=v['id']=='CNI-V036';ref=None if is5 else refs[0 if v['id']=='CNI-V002' else v['first_alias']['value']]
   need(c['existing_case_reference']==ref and c['qualification_only_unnumbered_shape5']==is5,'shape refs')
 need(qual['qualification']==summary['post_capture_analysis_qualification'] and qual['historical_shape5_qualification']==summary['historical_shape5_qualification'],'checker history preserved')
 need(qual['qualification']['all_capture_code_parent_pre_call_bound'] is True and qual['qualification']['all_later_analysis_pre_call_bound'] is False,'phase qualification')
def main():
 b=load('owner-before.json');d=load('owner-delta.json');q=load('qualification.json');cat=load('catalog.json');cases=load('new-cases.json');m=load('adoption-map.json');r=json.loads(pinned(q['approved_review']));s=r['approved_summary']
 need(q['approved_review_safe_owned_checks']==r['safe_owned_checks'] and q['inherited_limits']==r['limits'],'approved safe route/limits')
 need(m['approved_review']==q['approved_review'] and m['actual_manifest_citation_only']==r['frozen_packet']['manifest'],'sole review')
 before=pinned(b['owner']).decode();need(d['owner_before']==b['owner'],'base');after=before
 for x in d['replacements']:need(after.count(x['old'])==1,'unique old');after=after.replace(x['old'],x['new'])
 need(len(after.encode())==d['owner_after']['bytes'] and sha(after.encode())==d['owner_after']['sha256'],'target')
 rev=after
 for x in reversed(d['replacements']):need(rev.count(x['new'])==1,'unique new');rev=rev.replace(x['new'],x['old'])
 need(rev==before,'full reversal')
 a=bodies(after);old=bodies(before);need(len(a)==13,'13 requirements')
 for k,v in old.items():
  need(sha(v.encode())==b['requirements'][k]['sha256'],'pre-edit body')
  need(a[k].startswith(v) if k.endswith('002') else a[k]==v,'append-only002/12 whole bodies')
 for row in b['case_rows']:need(before.count(row['text'])==after.count(row['text'])==1 and sha(row['text'].encode())==row['sha256'],'36 old rows')
 need(len(b['case_rows'])==36 and b['old_IDs']==[f'DCO-{i:03d}' for i in range(1,37)],'old IDs')
 for h,v in b['protected_sections'].items():
  st=after.index(h);en=after.find('\n## ',st+1);part=after[st:en if en>=0 else len(after)];need(sha(part.encode())==v['sha256'],'protected section')
 for item in b['old_objects']:need(objsha(json.loads(pinned(item['pin'])))==item['json_object_sha256'],'old owner object')
 rel=json.loads(pinned(b['release_manifest']));need(objsha(rel)==b['release_manifest_object_sha256'] and b['released_evaluations']==73,'release manifest metadata')
 validate(cases,cat,m['joins'],q,s)
 controls=[]
 def reject(label,mut):
  cs,ca,js,qu=copy.deepcopy((cases,cat,m['joins'],q));mut(cs,ca,js,qu)
  try:validate(cs,ca,js,qu,s)
  except AssertionError:controls.append(label)
  else:raise AssertionError('control accepted '+label)
 reject('drop fresh',lambda cs,ca,js,qu:cs.pop())
 reject('drop alias',lambda cs,ca,js,qu:ca['aliases'].pop())
 reject('drop summary join',lambda cs,ca,js,qu:js.pop())
 reject('pad outcome denominator',lambda cs,ca,js,qu:ca.update(unique_vectors=69))
 reject('duplicate ID',lambda cs,ca,js,qu:cs[1].update(case_id=cs[0]['case_id']))
 reject('portable criterion',lambda cs,ca,js,qu:ca['vectors'][0].update(portable_comparator='waveform'))
 reject('native expectation',lambda cs,ca,js,qu:ca['vectors'][0].update(new_expected_waveform='fit'))
 reject('application proof',lambda cs,ca,js,qu:ca['vectors'][0].update(new_application_predicate_proof=True))
 reject('drop qualification',lambda cs,ca,js,qu:ca['vectors'][0].update(common_qualification=None))
 reject('claim all analysis prebound',lambda cs,ca,js,qu:qu['qualification'].update(all_later_analysis_pre_call_bound=True))
 reject('repair failed checker',lambda cs,ca,js,qu:qu['qualification'].update(original_checker_status='PASS'))
 reject('shape5 wrong old ID',lambda cs,ca,js,qu:ca['vectors'][36].update(existing_case_reference='DCO-021'))
 reject('shape5 new metrics',lambda cs,ca,js,qu:ca['vectors'][36].update(new_metrics={}))
 reject('inherited invented PID',lambda cs,ca,js,qu:ca['vectors'][2].update(new_pid=1))
 reject('alter one word',lambda cs,ca,js,qu:ca['vectors'][2]['words'][0].update(binary32_le='00000000'))
 reject('alter alias join',lambda cs,ca,js,qu:js[0].update(approved_pointer='/wrong'))
 reject('wrong output',lambda cs,ca,js,qu:ca['vectors'][0]['native_observation']['audio'].update(sha256='0'*64))
 reject('transfer old criterion',lambda cs,ca,js,qu:ca['vectors'][2].update(portable_comparator='old'))
 for label,mutant in [
  ('old timing mutation',after.replace('**Latency.** None.','**Latency.** Changed.')),
  ('old case mutation',after.replace(b['case_rows'][0]['text'],b['case_rows'][0]['text'].replace('Modal metric.','Changed metric.'))),
  ('old002prefix mutation',after.replace('Whether A1 holds.','A1 holds.')),
 ]:
  restored=mutant
  for replacement in reversed(d['replacements']):restored=restored.replace(replacement['new'],replacement['old'])
  need(restored!=before,label);controls.append(label)
 need(len(d['replacements'])==4 and 'FAIL' in d['replacements'][2]['new'] and 'NOT pre-call-bound' in d['replacements'][2]['new'] and 'not DCO-021' in d['replacements'][2]['new'],'wording limits')
 for x in d['replacements']:
  for link in re.findall(r'\]\(([^)]+)\)',x['new']):need((ROOT/'wiki/specs'/link.split('#')[0]).resolve().exists(),'new link')
 if (P/'manifest.json').exists():
  manifest=load('manifest.json');need({x.name for x in P.iterdir()}=={'manifest.json'}|{x['path'] for x in manifest['payloads']},'exact tree')
  for x in manifest['payloads']:
   raw=(P/x['path']).read_bytes();need(len(raw)==x['bytes'] and sha(raw)==x['sha256'],'payload seal')
 return {'status':'PASS','scope':'NEW owner wording/mapping/IDs/preservation only; approved summary inherited','owner_after':d['owner_after'],'new_IDs':57,'range':['DCO-037','DCO-093'],'logical_aliases':69,'unique_vectors':63,'inherited_case_references':5,'unnumbered_shape5':1,'old_rows_exact':36,'other_whole_requirement_bodies_exact':12,'old002prefix_exact':True,'old_owner_objects_exact':len(b['old_objects']),'released_evaluations_unchanged':73,'full_reverse_exact':True,'common_checker_qualification_every_newcase':True,'negative_controls':controls,'actual_packet_reads':0,'source_raw_numeric_rechecks':0,'original_calls':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',required=True,action='store_true');p.parse_args();print(json.dumps(main(),indent=2))
