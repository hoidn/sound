"""Read-only focused R2 check; preserves all sealed R1 data and tools.
Old canonical inputs resolve explicitly to exact original owner R1 snapshots.
No original/app/helper functions, network or native runtime are invoked.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import copy,json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;A=P/'archive-r1';ROOT=P.parents[3];S=P.parent/'synchronization'
load=lambda q:json.loads(q.read_text())
def sha(q):return sha256(q.read_bytes()).hexdigest()
def pin(q,p):assert q.is_file() and q.stat().st_size==p['bytes'] and sha(q)==p['sha256'],str(q)
def pointer(v,p):
 for key in p.strip('/').split('/'):
  key=key.replace('~1','/').replace('~0','~');v=v[int(key)] if isinstance(v,list) else v[key]
 return v

def check():
 before={str(q.relative_to(P)):sha(q) for q in P.rglob('*') if q.is_file()}
 assert not any('__pycache__' in n for n in before),'Use python3 -B'
 archive=load(P/'archive-r1-manifest.json');assert len(archive['original_files'])==15 and len(archive['files'])==16
 assert set(q.name for q in A.iterdir())==set(archive['files'])
 for name,p in archive['files'].items():pin(A/name,p)
 for name,p in archive['original_files'].items():
  pin(P/name,p);pin(A/name,p);assert (P/name).read_bytes()==(A/name).read_bytes()
 assert sha(A/'manifest-author-r1.json')==archive['original_manifest_sha256']=='72d2b3c6d6229d5f5a0a9f6fcc6f9477811c82637b58740ca14068342a6ba615'
 for name,p in load(A/'manifest-author-r1.json')['files'].items():pin(A/name,p)
 for name,p in load(A/'freeze-author-r1.json')['files'].items():pin(A/name,p)
 review=ROOT/archive['review']['original_path'];pin(review,archive['review']);assert review.read_bytes()==(A/'review-r1.json').read_bytes()
 assert sha(review)=='a1dd4b9faa4dd723e806244c6e6b22193663e5f0035c2e14a1955c24ccae59db'
 finding=load(review)['required_findings'];assert [f['id'] for f in finding]==['SYNC-SOURCE-AUDIT-REVIEW-001'] and finding[0]['source_unit']['id']=='SYNC-A079'
 # An audit of original R1 remains an audit of original R1 when current wiki advances.
 redirects={'wiki/specs/synchronization-workflows.md':S/'spec-r1.md','wiki/research/synchronization-workflows.md':S/'research-r1.md'}
 external=load(A/'inputs.json')['pins'];assert len(external)==36
 input_before={}
 for p in external:
  q=redirects.get(p['path'],ROOT/p['path']);pin(q,p);input_before[str(q)]=sha(q)
 # Only this analyst's guarded finite JSON derivation is loaded.
 d=runpy.run_path(str(P/'derive-r2.py'))['build']()
 for name,value in d.items():assert load(P/(name+'.json'))==value,name
 response=d['response-r2'];assert response['finding']=='SYNC-SOURCE-AUDIT-REVIEW-001' and len(response['field_deltas'])==9
 assert response['review']['sha256']==sha(review) and response['normative_owner_changes'] is False and response['actual_execution'] is False
 mapping={'source-unit-ledger.json':'source-unit-ledger-r2.json','gap-proposals.json':'gap-proposals-r2.json','catalog-reconciliation.json':'catalog-reconciliation-r2.json','summary.json':'summary-r2.json'}
 expected={name:copy.deepcopy(load(A/name)) for name in mapping}
 for delta in response['field_deltas']:
  assert delta['old_file'] in mapping and delta['new_file']==mapping[delta['old_file']]
  keys=delta['pointer'].strip('/').split('/');value=expected[delta['old_file']]
  for key in keys[:-1]:value=value[int(key)] if isinstance(value,list) else value[key]
  key=int(keys[-1]) if isinstance(value,list) else keys[-1]
  if delta['operation']=='add':assert isinstance(value,list) and key==len(value) and delta['old'] is None;value.append(copy.deepcopy(delta['new']))
  else:assert delta['operation']=='replace' and value[key]==delta['old'];value[key]=copy.deepcopy(delta['new'])
 for name,newname in mapping.items():assert load(P/newname)==expected[name],newname
 old=load(A/'source-unit-ledger.json');units=d['source-unit-ledger-r2'];assert len(units)==len(old)==130
 assert units[:78]==old[:78] and units[79:]==old[79:]
 assert set(k for k in old[78] if old[78][k]!=units[78][k])=={'disposition','cases','judgment','gap_ids'}
 u=units[78];assert u['id']=='SYNC-A079' and u['disposition']=='missing-clause-case-or-context' and u['cases']==[] and u['gap_ids']==['SA-G09']
 gaps=d['gap-proposals-r2'];assert len(gaps)==9 and gaps[:8]==load(A/'gap-proposals.json')
 assert gaps[8]['source_units']==['SYNC-A079'] and gaps[8]['current_context_only_cases']==old[78]['cases']
 for g in gaps:
  assert all(g[k] is None for k in ['expected','comparison','documentary_expected','documentary_comparator']) and g['target_grade']=='U' and g['executed'] is False
  assert g['clause_delta'] and g['case_delta']
 assert Counter(x['disposition'] for x in units)=={'represented-partial-source-clause-and-case':29,'documented-but-outcome-U':59,'missing-clause-case-or-context':10,'research-only-protocol-private-or-marketing':15,'editorial':15,'image-or-link-uninspected':2}
 assert sum(bool(x['gap_ids']) for x in units)==10
 # Original source identities/locators/text remain exact and fully accounted for.
 blocks=load(S/'source-blocks.json');assert len(blocks)==54
 for i,b in enumerate(blocks):
  us=[u for u in units if u['block_id']==b['id']];covered=set()
  for u in us:
   a,z=u['normalized_block_character_start'],u['normalized_block_character_end'];assert u['source_pointer']==f'/{i}/text' and b['text'][a:z]==u['text']
   assert u['anchor']==b['anchor'] and u['html_line']==b['html_line'] and u['text_sha256']==sha256(u['text'].encode()).hexdigest()
   assert covered.isdisjoint(range(a,z));covered.update(range(a,z));assert u['target_applicability']=='U' and not u['complete'] and not u['execution']
   for r in u['requirements']:
    text=pointer(load(ROOT/r['path']),r['pointer']);assert sha256(text.encode()).hexdigest()==r['contract_sha256']
   for c in u['cases']:
    text=pointer(load(ROOT/c['path']),c['pointer']);assert sha256(text.encode()).hexdigest()==c['action_sha256']
  assert {j for j,c in enumerate(b['text']) if not c.isspace()}<=covered
 rec=d['catalog-reconciliation-r2'];assert len(rec['requirements'])==26 and len(rec['cases'])==36
 oldrec=load(A/'catalog-reconciliation.json')
 assert rec['requirements']==oldrec['requirements']
 assert rec['cases'][:11]==oldrec['cases'][:11] and rec['cases'][12:]==oldrec['cases'][12:]
 assert rec['cases'][11]['reference']==oldrec['cases'][11]['reference'] and 'SYNC-A079' not in rec['cases'][11]['source_units']
 assert len([c for c in rec['cases'] if c['source_units']])==26
 for c in load(S/'cases.json'):assert c['expected'] is None and c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
 manifest=load(P/'manifest-author-r2.json');assert manifest['revision']==2 and manifest['summary']==d['summary-r2']
 assert set(before)==set(manifest['files'])|{'manifest-author-r2.json'}|({'validation-author-r2.json'}&set(before))|({'freeze-author-r2.json'}&set(before))
 for name,p in manifest['files'].items():pin(P/name,p)
 if (P/'freeze-author-r2.json').exists():
  for name,p in load(P/'freeze-author-r2.json')['files'].items():pin(P/name,p)
 links=0
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',(P/'README-r2.md').read_text()):
  assert not re.match(r'https?://',target);name,_,fragment=target.partition('#');assert (P/name).is_file(),target;links+=1
 whitespace=0
 for q in P.rglob('*'):
  if not q.is_file():continue
  result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True)
  assert result.returncode in (0,1) and not result.stdout and not result.stderr,str(q);whitespace+=1
 assert before=={str(q.relative_to(P)):sha(q) for q in P.rglob('*') if q.is_file()},'packet mutation'
 assert input_before=={q:sha(Path(q)) for q in input_before},'historical input mutation'
 return dict(status='pass',scope='focused auditR2 preservation/exact delta/source-pointer/null integrity; independent semantic rereview pending',original_R1_root_files_preserved=15,archive_R1_files_including_review=16,exact_field_deltas=9,unchanged_other_source_units=129,source_blocks=54,source_units=130,gap_spans=10,gap_proposals=9,existing_requirements=26,existing_cases=36,external_pins=36,explicit_historical_canonical_resolutions=list(redirects),payloads=len(manifest['files']),README_links=links,untracked_whitespace_files=whitespace,all_actual_target_outcomes_null_U_unexecuted=True,normative_or_source_edits=False,writes=False,original_network_app_peer_hardware_function_execution=False)
if __name__=='__main__':
 assert not sys.argv[1:],'read-only validator accepts no arguments'
 print(json.dumps(check(),indent=2))
