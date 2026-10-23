"""Read-only bounded Filter/EQ R4 source/case integrity. No old tools execute."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json,re,sys
P=Path(__file__).resolve().parent;R=P.parents[3];A=P.parent/'filter-eq-source-audit'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def ptr(v,s):
 for k in s.strip('/').split('/') if s else []:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
IDS=['AF-C060','AF-C061','AF-C062','AF-C063','AF-C064','AF-C065','CEQ-C018','EQ8-C034','EQ8-C035','EQ8-C036','EQ8-C037','EQ3-C020']
GUARDS=[
 ['isolated_nonzero_LFO','filter_and_output_response','all_five_wave_selections','actual_Morph_and_Smooth_edits'],
 ['productive_eligible_Res','eligible_before_ineligible','nonzero_source_processed_output'],
 ['productive_eligible_Circuit','eligible_before_each_ineligible','nonzero_source_processed_output'],
 ['internal_external_separate_resets','external_explicitly_enabled_selected','both_monitor_sources_productive'],
 ['all_three_actual_tap_selections','isolated_productive_external_ENV','reconfirm_after_each_tap'],
 ['actual_Frequency_and_Q','productive_isolated_ENV','both_Type_sources_unresolved'],
 ['two_independent_productive_pads','actual_control_on_each','nonzero_source_processed_output'],
 ['all_eight_actual_expanded_edits','admitted_gain_supporting_controls','UI_only_no_signal_required'],
 ['direct_Gain_number_field','direct_Q_number_field','eligible_Peak'],
 ['productive_Low_Shelf','productive_High_Shelf','two_admitted_Scale_values_each','old_Peak_history_retained'],
 ['both_filters_productive_distinguishable','nonzero_source_processed_output','actual_hold_then_release'],
 ['each_band_productive_before_removal','nonzero_input_before_coloration','all_three_lit_LED_histories_retained']]
TOKENS=[
 ['actually select Triangle, Saw, Square, Ramp Up and Ramp Down','actually move its Morph','actually move Smooth'],
 ['eligible Low-pass','genuine Res-related output contribution','explicitly choose Resampling'],
 ['each available SVF, DFM, MS2 and PRD','eligible positive before each branch'],
 ['explicitly set External off','explicitly enable External','independently NONZERO external source'],
 ['actually choose Pre FX, Post FX and Post Mixer','after each admitted choice'],
 ['actually change SC Filter Frequency','actually change Sidechain Filter Q','no Notch admission, seven-entry union'],
 ['TWO actual populated','put a separate Channel EQ on EACH pad','first pad','second'],
 ['actually edit','EACH of the eight filters','single atomic all-band gesture'],
 ['Gain NUMBER FIELD','Q NUMBER FIELD','Do not substitute dial movement'],
 ['genuinely NONZERO Low Shelf','same separate productive history for High Shelf','two admitted Scale settings'],
 ['demonstrate EACH contribution','press and HOLD','then release'],
 ['EACH low, mid and high band','genuinely NONZERO input','ALL THREE EQ3-C005/006/007']]
def catalog(cat):
 old=load(P/'cases.json');a=load(A/'audit.json');ad=load(P/'adoption-r4.json');cs=cat['cases']
 assert len(cs)==140 and cs[:128]==old and [c['id'] for c in cs[128:]]==IDS
 assert len({c['id'] for c in cs})==140
 assert {g:sum(c['provenance']==g for c in cs) for g in ['D12','Dpkg','U']}=={'D12':90,'Dpkg':4,'U':46}
 req={r['id'] for r in load(P/'requirements.json')};assert len(req)==65
 for i,c in enumerate(cs[128:]):
  assert c['audit_group']==f'FEA-G{i+1:02}' and c['status']=='unexecuted' and c['exact_target']=='U'
  assert set(c['requirements'])<=req and c['requirements']
  assert set(c['positive_guard'])==set(GUARDS[i]) and all(v is True for v in c['positive_guard'].values())
  assert all(c[k] is None for k in ['expected','documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
  assert c['setup_action'].startswith(ad['common_current_guard'])
  assert all(t in c['setup_action']+c['positive_baseline'] for t in TOKENS[i]),(c['id'],TOKENS[i])
  texts=[]
  for v in c['source_contexts']:
   assert v['catalog']==str((A/'audit.json').relative_to(R));b=ptr(a,v['json_pointer']);assert b['id']==v['id'];texts.append(b['text'])
  assert texts and c['source_claim']==' '.join(texts)
  group=ad['groups'][i];assert ptr(cat,group['case_pointer'])==c and group['case_id']==c['id']
  original=ptr(a,group['audit_pointer']);assert original['id']==c['audit_group'] and group['remaining']==original['limits'] and group['assessment_ids']==original['assessment_ids']
 return True
def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no write/replay mode'
 inputs=load(P/'inputs-r4.json');prior=load(P/'prior-files-r4.json');ad=load(P/'adoption-r4.json');history=load(P/'consumer-history-r4.json')
 inherited=load(R/inputs['inherited_audit_inputs'])['files'];assert len(prior)==99 and len(inputs['files'])==7 and len(inherited)==105
 watch={p for p in P.rglob('*') if p.is_file()}|{R/x['path'] for x in inputs['files']+inherited}|{R/x['path'] for x in ad['canonical_pages']}|{R/x['file']['path'] for x in history['external_occurrences']};before={str(p):dg(p) for p in watch}
 for n,v in prior.items():assert dg(P/n)==v,n
 for x in inputs['files']+inherited:assert dg(R/x['path'])=={k:x[k] for k in ['bytes','sha256']},x['path']
 assert dg(A/'manifest.json')['sha256']=='cf91b2f3a3825b37532c3a22ef9e517f47c7c959bede81db35391b12ff7c8b00'
 assert dg(P.parent/'reviews/filter-eq-source-audit-review.json')['sha256']=='62c112479723428b2eb5363f461b37e6727c8f4d03ed7671bd8d191e8ff62d18'
 cat=load(P/'cases-r4.json');catalog(cat);a=load(A/'audit.json')
 assert ad['source_questions']==a['source_questions'] and ad['common_future_prerequisites']==a['common_future_prerequisites']
 assert 'independently productive tested-control contribution' in ad['common_current_guard'] and 'UI-only inspection/editing needs no audio' in ad['common_current_guard']
 ids=[];links=0
 for x in ad['canonical_pages']:
  old=(R/x['before_provider']).read_text();out=old.replace('revision: 3\n','revision: 4\n',1)
  end=re.search(r'^# [^\n]+\n\n',out,re.M).end();out=out[:end]+x['insertion_after_title']+out[end:]+x['appended']
  assert out==(R/x['after_provider']).read_text()==(R/x['path']).read_text()
  assert sha256(old.encode()).hexdigest()==x['before_sha256'] and sha256(out.encode()).hexdigest()==x['after_sha256']
  if '/specs/' in x['path']:
   found=list(re.finditer(r'^### (REQ-[A-Z0-9-]+) — ([^\n]+)\n\n\*\*(D12|Dpkg|U)\.\*\* (.*?)\n\nEvidence:',out,re.M|re.S))
   assert [(m[1],m[2],m[3],m[4]) for m in found]==[(r['id'],r['title'],r['provenance'],r['text']) for r in load(P/'requirements.json')];ids=[m[1] for m in found]
 for x in history['external_occurrences']:
  assert dg(R/x['file']['path'])=={k:x['file'][k] for k in ['bytes','sha256']}
  assert ptr(load(R/x['file']['path']),x['json_pointer'])==x['sha256']==dg(R/x['provider'])['sha256']
 raw=(P.parent/'audio-utilities/manual-audio-effects-2026-10-19.html').read_text()
 for b in a['blocks']:assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
 rejected=[]
 for i,keys in enumerate(GUARDS):
  bad=deepcopy(cat);bad['cases'][128+i]['positive_guard'][keys[0]]=False
  try:catalog(bad)
  except AssertionError:rejected.append('missing-'+keys[0])
  else:raise AssertionError('Inactive prerequisite accepted')
 for name,idx,key,value in [('old-case-changed',0,'setup_action','erased'),('invent-output',128,'actual_expected','pass'),('wrong-source',129,'source_claim','invented'),('dial-for-number-field',136,'setup_action',cat['cases'][136]['setup_action'].replace('Gain NUMBER FIELD','Gain dial')),('one-shelf-only',137,'setup_action',cat['cases'][137]['setup_action'].replace('same separate productive history for High Shelf','skip High Shelf'))]:
  bad=deepcopy(cat);bad['cases'][idx][key]=value
  try:catalog(bad)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe fixture accepted '+name)
 docs=[R/x['path'] for x in ad['canonical_pages']]+[P/'README-r4.md']
 for f in docs:
  for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
   if re.match('[A-Za-z]+:',target):continue
   dest,_,anchor=target.partition('#');q=(f.parent/dest).resolve() if dest else f;assert q.exists(),target;links+=1
 for p in P.rglob('*'):
  if p.is_file() and str(p.relative_to(P)) not in prior:
   b=p.read_bytes();assert b.endswith(b'\n') and b'\x00' not in b and all(l.rstrip(b' \t')==l for l in b.splitlines())
 seal=P/'manifest-author-r4.json'
 if seal.exists():
  mf=load(seal)
  for x in mf['files']:assert dg(R/x['path'])=={k:x[k] for k in ['bytes','sha256']}
  listed={x['path'] for x in mf['files'] if x['path'].startswith(str(P.relative_to(R))+'/')}
  assert {str(p.relative_to(R)) for p in P.rglob('*') if p.is_file()}==listed|{str(seal.relative_to(R))}
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),requirements=len(ids),cases=140,old_cases_exact=128,prior_files=99,inherited_pins=105,owned_pins=7,external_asof_hash_occurrences=len(history['external_occurrences']),source_blocks=108,new_cases=12,new_oracle_nonnull=0,complete_profiles=0,negative_fixtures=rejected,links=links,watched_paths=len(watch),all_unchanged=True,writes=False,old_tools_decodes_runtime_hardware_network_candidate=False),indent=2))
if __name__=='__main__':main()
