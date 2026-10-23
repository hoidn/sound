"""Bounded exact citation audit. --check is read-only; never product coverage."""
from pathlib import Path
from collections import Counter
from datetime import datetime
import hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=P.parents[4]
assert sys.argv[1:] in ([],['--check'])
CHECKING=sys.argv[1:]==['--check']
if not CHECKING:assert not (P/'manifest.json').exists(),'Frozen crosswalk; use --check or create a new revision'
load=lambda q:json.loads(q.read_text())
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
inputs=load(P/'inputs.json')
assert [c['packet'] for c in inputs['cohort']]==['push-workflows','engine-resources','browser-content','live-concepts']
pins={r['path']:r for r in inputs['pins']}
assert len(pins)==len(inputs['pins'])==148
for name,pin in pins.items():
 q=ROOT/name;assert q.stat().st_size==pin['bytes'] and sha(q)==pin['sha256'],name
r4path=ROOT/inputs['prior_crosswalk_manifest'];r4=load(r4path)
assert sha(r4path)==inputs['prior_crosswalk_sha256']=='82e88e6a8111df62f3b46ef445a5e802087396138481ed331cbd9a964d266fc6'
prior_review=load(ROOT/inputs['prior_crosswalk_review'])
assert prior_review['id']==inputs['prior_crosswalk_review_id'] and prior_review['reviewed_manifest_sha256']==sha(r4path)
assert prior_review['disposition']=='approved-as-citation-navigation-only' and not prior_review['findings']
for name,record in r4['files'].items():assert pins[str((r4path.parent/name).relative_to(ROOT))]['sha256']==record['sha256']
toc=load(ROOT/inputs['toc'])
assert len(toc)==len({t['id'] for t in toc})==len({t['url'] for t in toc})==880
assert sum(t['leaf'] for t in toc)==708 and len({t['number'].split('.')[0] for t in toc})==43
assert sha(ROOT/inputs['toc'])=='1ca19a34ad1c0e97a9dd6582d2f7ebf06c5a16ae9d2bd64c26baab5c0eb46e98'
assert sha(ROOT/inputs['original_toc_source'])=='584d4b61d119c96ecdb7941ef34ac9d4e0282a3e40c8bc474b6cf24892640d80'
original=load(ROOT/inputs['original_inventory_manifest'])
for name in ['manual-toc.json','manual-12-toc-2026-10-19.html']:
 q=(ROOT/inputs['toc']).parent/name;assert sha(q)==original['files'][name]['sha256']
topics=[dict(t,citation_status='no-citation-in-this-four-packet-cohort',full_topic_semantic_coverage='unknown',completion_status='unknown',target_applicability='U',cohort_citations=[]) for t in toc]
byurl={t['url']:t for t in topics}
unmatched=[];unbacked=[];case_index=[];packet_counts=[];all_req=set();all_case=set();all_block=set()


def grade(record):
 key='provenance' if 'provenance' in record else 'strength' if 'strength' in record else None
 return dict(field=key,value=record[key] if key else None)


def flags(case):
 assert all(case[k] is None for k in ['expected','comparison'])
 assert case['target_grade']=='U' and case['executed'] is False
 return dict(expected=None,comparison=None,target_grade='U',executed=False,
  documentary_expected_is_null=case['documentary_expected'] is None,
  documentary_comparator_is_null=case['documentary_comparator'] is None,
  source_claim_is_null=case.get('source_claim') is None,source_claim_field_present='source_claim' in case)


def source_refs(record,lookup,path,index):
 field='evidence' if 'evidence' in record else 'source_blocks'
 refs=record[field];result=[]
 for n,e in enumerate(refs):
  bid=e['block'] if isinstance(e,dict) else e
  b,blockpath,bn,source,sourcecfg,sourcecat=lookup[bid]
  if isinstance(e,dict):
   assert e['anchor']==b['anchor'] and e['html_line']==b['html_line']
   if 'source' in e:assert e['source']==source['id']
  anchor=b['anchor']
  assert anchor is None or isinstance(anchor,str)
  exact=None if anchor is None else source['url']+'#'+anchor
  matched=byurl.get(exact)
  result.append(dict(original_reference=e,reference_catalog=path,reference_json_pointer=f'/{index}/{field}/{n}',block_id=bid,block_catalog=blockpath,block_json_pointer='/'+str(bn),anchor=anchor,html_line=b['html_line'],html_column=b.get('html_column'),heading_context=b.get('heading_context'),section=b.get('section'),source_identity=source,source_catalog=sourcecat,source_record_json_pointer=sourcecfg['source_record_pointer'],source_bytes=sourcecfg['raw'],exact_anchor_url=exact,join_status='exact-TOC-URL-match' if matched else 'null-direct-anchor-unjoined' if anchor is None else 'exact-URL-absent-from-TOC',matched_manual_id=matched['id'] if matched else None))
 return result


for cfg in inputs['cohort']:
 packet=cfg['packet'];mp=ROOT/cfg['manifest'];m=load(mp);review=load(ROOT/cfg['review'])
 assert sha(mp)==cfg['manifest_sha256']==review['reviewed_manifest_sha256']
 assert m['id']==cfg['manifest_id'] and m['revision']==1
 assert review['id']==cfg['review_id'] and review['disposition']==cfg['review_disposition']
 assert review['disposition'] in ['approved-as-partial-analyst-draft','approved-partial-analyst-draft']
 assert not review.get('findings') and not review.get('required_findings')
 for name,pin in m['files'].items():
  q=mp.parent/name;pp=pins[str(q.relative_to(ROOT))];assert pp['bytes']==pin['bytes'] and pp['sha256']==pin['sha256']
 for slug,canonical in [('spec-r1.md',cfg['canonical_spec']),('research-r1.md',cfg['canonical_research'])]:
  assert (mp.parent/slug).read_bytes()==(ROOT/canonical).read_bytes()
 catalog=load(ROOT/cfg['source_catalog']);source_list=catalog if isinstance(catalog,list) else [catalog]
 lookup={};nblocks=0
 for sourcecfg in cfg['sources']:
  source=next(s for s in source_list if s['id']==sourcecfg['source_id'])
  if sourcecfg['source_record_pointer']:
   assert source_list[int(sourcecfg['source_record_pointer'][1:])]==source
  else:assert catalog==source
  assert '#' not in source['url']
  stamp=source.get('capture_utc',source.get('captured_utc'));assert datetime.fromisoformat(stamp).utcoffset().total_seconds()==0
  raw=ROOT/sourcecfg['raw'];assert raw.stat().st_size==source['bytes'] and sha(raw)==source['sha256']
  blocks=load(ROOT/sourcecfg['blocks']);nblocks+=len(blocks)
  for n,b in enumerate(blocks):
   bid=b.get('id',b.get('locator'));assert bid and bid not in lookup
   lookup[bid]=(b,sourcecfg['blocks'],n,source,sourcecfg,cfg['source_catalog']);all_block.add((packet,sourcecfg['blocks'],n,bid))
 reqs=load(ROOT/cfg['requirements']);cases=load(ROOT/cfg['cases']);reqmap={r['id']:r for r in reqs}
 assert len(reqmap)==len(reqs) and len({c['id'] for c in cases})==len(cases)
 assert {rid for c in cases for rid in c['requirements']}==set(reqmap)
 reqpositions={r['id']:n for n,r in enumerate(reqs)};case_refs={rid:[] for rid in reqmap}
 for n,c in enumerate(cases):
  identity=(packet,cfg['cases'],'/'+str(n),c['id']);assert identity not in all_case;all_case.add(identity)
  ownrefs=source_refs(c,lookup,cfg['cases'],n)
  linked_blocks=set()
  for rid in c['requirements']:
   rr=reqmap[rid];linked_blocks.update(e['block'] for e in rr['evidence']) if 'evidence' in rr else linked_blocks.update(rr['source_blocks'])
  assert {e['block_id'] for e in ownrefs}<=linked_blocks,'Unexpected case-only reference requires an explicit new ledger role'
  row=dict(packet=packet,case_id=c['id'],case_catalog=cfg['cases'],case_json_pointer='/'+str(n),case_provenance=grade(c),kind=c['kind'],requirements=[dict(id=rid,catalog=cfg['requirements'],json_pointer='/'+str(reqpositions[rid])) for rid in c['requirements']],source_references=ownrefs,source_reference_count=len(ownrefs),no_source_references=not ownrefs,**flags(c))
  ci=len(case_index);case_index.append(row)
  ref=dict(packet=packet,case_id=c['id'],catalog=cfg['cases'],json_pointer='/'+str(n),case_index_catalog='case-index.json',case_index_pointer='/'+str(ci),kind=c['kind'],case_provenance=grade(c),source_reference_count=len(ownrefs),**flags(c))
  for rid in c['requirements']:case_refs[rid].append(ref)
 req_refs=[]
 for n,r in enumerate(reqs):
  assert r['target_applicability']=='U';g=grade(r);assert g['value'] in ['D12','U']
  assert (packet,cfg['requirements'],'/'+str(n),r['id']) not in all_req;all_req.add((packet,cfg['requirements'],'/'+str(n),r['id']))
  refs=source_refs(r,lookup,cfg['requirements'],n);req_refs.extend(refs)
  identity=dict(packet=packet,requirement_id=r['id'],requirement_provenance=g,requirement_catalog=cfg['requirements'],requirement_json_pointer='/'+str(n),canonical_spec=cfg['canonical_spec'],canonical_research=cfg['canonical_research'],review=dict(path=cfg['review'],id=review['id'],sha256=pins[cfg['review']]['sha256'],disposition=review['disposition'],reviewed_manifest_sha256=sha(mp)),case_references=case_refs[r['id']],target_applicability='U',semantic_coverage='unknown',citation_role='documentary-requirement-reference' if g['value']=='D12' else 'unknown-requirement-source-context-only')
  assert identity['case_references']
  if not refs:
   assert g['value']=='U';unbacked.append(dict(identity,source=None,reason='Original requirement has no source references; no source or parent inferred'))
  for evidence in refs:
   citation=dict(identity,evidence=evidence)
   if evidence['matched_manual_id'] is not None:
    topic=byurl[evidence['exact_anchor_url']];topic['cohort_citations'].append(citation);topic['citation_status']='cited-by-partial-reviewed-draft'
   else:
    reason='Direct block anchor is null; heading_context ancestors retained as context only, never inherited for joining' if evidence['anchor'] is None else 'Exact source URL plus its direct block anchor absent from original TOC; no normalization/title/parent inference'
    unmatched.append(dict(citation,reason=reason))
 packet_counts.append(dict(packet=packet,requirements=len(reqs),requirement_provenance=dict(Counter(grade(r)['value'] for r in reqs)),cases=len(cases),source_records=len(cfg['sources']),source_blocks=nblocks,requirement_source_references=len(req_refs),case_source_references=sum(len(c['source_references']) for c in case_index if c['packet']==packet),cases_without_source_references=sum(c['no_source_references'] for c in case_index if c['packet']==packet),documentary_expected_nonnull_cases=sum(c['documentary_expected'] is not None for c in cases),documentary_comparator_nonnull_cases=sum(c['documentary_comparator'] is not None for c in cases),review_id=review['id'],reviewed_manifest_sha256=sha(mp)))

matched=[c for t in topics for c in t['cohort_citations']]
reqkey=lambda r:(r['packet'],r['requirement_catalog'],r['requirement_json_pointer'],r['requirement_id'])
casekey=lambda c:(c['packet'],c['catalog'],c['json_pointer'],c['case_id'])
matched_req={reqkey(r) for r in matched};unmatched_req={reqkey(r) for r in unmatched};nosource_req={reqkey(r) for r in unbacked}
assert len(all_req)==162 and len(all_case)==221 and len(all_block)==1300
assert sum(c['requirements'] for c in packet_counts)==162 and sum(c['cases'] for c in packet_counts)==221
assert Counter({g:sum(c['requirement_provenance'].get(g,0) for c in packet_counts) for g in ['D12','U']})=={'D12':125,'U':37}
assert matched_req|unmatched_req|nosource_req==all_req
assert {casekey(c) for r in [*matched,*unmatched,*unbacked] for c in r['case_references']}==all_case
assert {(r['packet'],r['case_catalog'],r['case_json_pointer'],r['case_id']) for r in case_index}==all_case
assert [dict((key,row[key]) for key in original) for row,original in zip(topics,toc)]==toc
assert all(row['full_topic_semantic_coverage']=='unknown' and row['completion_status']=='unknown' and row['target_applicability']=='U' and row['complete'] is False for row in topics)
# Finite boundary checks: null anchors never join, direct source hash remains captured,
# and matching URL does not merge distinct Concepts captures or U source contexts.
assert all(c['evidence']['anchor'] is not None and c['evidence']['exact_anchor_url']==t['url'] for t in topics for c in t['cohort_citations'])
assert all(c['evidence']['matched_manual_id'] is None for c in unmatched)
assert sum(c['evidence']['anchor'] is None for c in matched)==0
assert len(matched)==290 and len(unmatched)==376 and len(unbacked)==22
assert Counter(c['evidence']['join_status'] for c in unmatched)=={'null-direct-anchor-unjoined':330,'exact-URL-absent-from-TOC':46}
assert len(matched_req)==77 and len(unmatched_req-matched_req)==63 and len(matched_req&unmatched_req)==3
concept_hashes={c['evidence']['source_identity']['sha256'] for c in [*matched,*unmatched] if c['evidence']['source_identity']['url']=='https://www.ableton.com/en/live-manual/12/live-concepts/'}
assert concept_hashes=={'da51ae19eab185813aac3b4240b7fad6022885421a3794155ca1207fd6e2eed5','611eeb0d7ffa1cb63aacd5bafbfbb3e60803836f4ca02f0e4aabb017fb7cf5c9'}
summary=dict(id='FULL-LIVE-MANUAL-CITATION-CROSSWALK-R6-SUMMARY',scope='Second exact four-packet citation cohort only; navigation/audit, no aggregate/semantic/behavioral coverage claim',cohort=packet_counts,input_requirements=162,input_requirement_provenance={'D12':125,'U':37},input_cases=221,input_source_records=8,input_source_blocks=1300,manual_topics_preserved=880,manual_leaves_preserved=708,manual_chapters_preserved=43,matched_requirement_source_citations=len(matched),matched_citation_provenance=dict(Counter(c['requirement_provenance']['value'] for c in matched)),unmatched_requirement_source_citations=len(unmatched),unmatched_reasons=dict(Counter(c['evidence']['join_status'] for c in unmatched)),distinct_unmatched_nonnull_anchor_URLs=len({c['evidence']['exact_anchor_url'] for c in unmatched if c['evidence']['exact_anchor_url'] is not None}),unmatched_nonnull_anchor_URLs=sorted({c['evidence']['exact_anchor_url'] for c in unmatched if c['evidence']['exact_anchor_url'] is not None}),topics_with_cohort_citations=sum(bool(t['cohort_citations']) for t in topics),leaves_with_cohort_citations=sum(t['leaf'] and bool(t['cohort_citations']) for t in topics),nonleaves_with_cohort_citations=sum(not t['leaf'] and bool(t['cohort_citations']) for t in topics),topics_without_cohort_citations=sum(not t['cohort_citations'] for t in topics),requirements_with_exact_TOC_citations=len(matched_req),requirements_with_only_unmatched_citations=len(unmatched_req-matched_req),requirements_with_both_matched_and_unmatched=len(matched_req&unmatched_req),requirements_without_source_references=len(unbacked),U_source_context_requirements_with_references=sum(c['packet']=='engine-resources' and c['requirement_provenance']['value']=='U' for c in {reqkey(r):r for r in [*matched,*unmatched]}.values()),case_source_references=sum(c['source_reference_count'] for c in case_index),cases_without_source_references=sum(c['no_source_references'] for c in case_index),case_join_statuses=dict(Counter(e['join_status'] for c in case_index for e in c['source_references'])),documentary_expected_nonnull_cases=sum(not c['documentary_expected_is_null'] for c in case_index),documentary_expected_null_cases=sum(c['documentary_expected_is_null'] for c in case_index),requirements_reconciled=len(all_req),cases_reconciled=len(all_case),external_input_pins=len(pins),prior_crosswalk_manifest_sha256=inputs['prior_crosswalk_sha256'],complete_topics_claimed=0,full_topic_semantic_coverage='unknown',target_applicability='U',all_target_case_oracles_null_U_unexecuted=True,work_selector='wiki/research/full-live-specification-plan.md; existing F01-F10 only',original_runtime_service_hardware_or_candidate_execution=False)
summary.update(topics_with_D12_requirement_citations=sum(any(c['requirement_provenance']['value']=='D12' for c in t['cohort_citations']) for t in topics),leaves_with_D12_requirement_citations=sum(t['leaf'] and any(c['requirement_provenance']['value']=='D12' for c in t['cohort_citations']) for t in topics),topics_with_U_source_context_citations=sum(any(c['requirement_provenance']['value']=='U' for c in t['cohort_citations']) for t in topics),leaves_with_U_source_context_citations=sum(t['leaf'] and any(c['requirement_provenance']['value']=='U' for c in t['cohort_citations']) for t in topics),topics_with_only_U_source_context_citations=sum(bool(t['cohort_citations']) and all(c['requirement_provenance']['value']=='U' for c in t['cohort_citations']) for t in topics),case_only_source_references=0)
for cfg in summary['cohort']:
 cfg['matched_requirement_source_citations']=sum(c['packet']==cfg['packet'] for c in matched)
 cfg['unmatched_requirement_source_citations']=sum(c['packet']==cfg['packet'] for c in unmatched)
outputs={'topic-citations.json':topics,'unmatched-citations.json':unmatched,'unbacked-requirements.json':unbacked,'case-index.json':case_index,'summary.json':summary}
for name,value in outputs.items():
 raw=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode();q=P/name
 if CHECKING:assert q.read_bytes()==raw,name
 else:assert not q.exists(),'Refuse overwriting '+name;q.write_bytes(raw)
if CHECKING:
 before={str(q.relative_to(P)):sha(q) for q in P.rglob('*') if q.is_file()}
 manifest=load(P/'manifest.json');assert set(before)==set(manifest['files'])|{'manifest.json'}
 assert manifest['summary']==summary
 for name,pin in manifest['files'].items():
  q=P/name;assert q.stat().st_size==pin['bytes'] and sha(q)==pin['sha256'],name
 for q in P.iterdir():
  if q.suffix in ['.json','.py','.md']:
   check=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True)
   assert check.returncode in (0,1) and not check.stdout and not check.stderr,str(q)
 assert before=={str(q.relative_to(P)):sha(q) for q in P.rglob('*') if q.is_file()}
print(json.dumps(summary,indent=2))
