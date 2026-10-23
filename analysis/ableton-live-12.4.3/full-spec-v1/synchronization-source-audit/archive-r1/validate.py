"""Read-only literal-source/pointer/identity reconciliation; no application calls.
No mutation flags, no source fetch, no original/helper/function execution.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];S=P.parent/'synchronization'
def load(q):return json.loads(q.read_text())
def sha(q):return sha256(q.read_bytes()).hexdigest()
def check_pin(q,p):assert q.is_file() and q.stat().st_size==p['bytes'] and sha(q)==p['sha256'],str(q)
def pointer(v,p):
 if not p:return v
 for k in p.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v

def check():
 before={str(q.relative_to(P)):sha(q) for q in P.rglob('*') if q.is_file()}
 assert not any('__pycache__' in name for name in before),'Use python3 -B'
 derive=runpy.run_path(str(P/'derive.py'));expected=derive['build']()
 for name,value in expected.items():assert load(P/(name+'.json'))==value,name
 pins=expected['inputs']['pins'];assert len(pins)==len({p['path'] for p in pins})==36
 for p in pins:check_pin(ROOT/p['path'],p)
 input_before={p['path']:sha(ROOT/p['path']) for p in pins}
 # Replay only the pinned analyst HTML parser's guarded class; no original code.
 dep=load(S/'dependencies.json')[0];parser=runpy.run_path(str(ROOT/dep['path']))['Chapter']()
 source=load(S/'source.json');raw=(S/source['file']).read_bytes();assert len(raw)==261580 and sha256(raw).hexdigest()==source['sha256']=='55dcef3b8171e721c641ab69476a075db8c3c8893055914538f9e4eb801d00ac'
 parser.feed(raw.decode())
 for i,b in enumerate(parser.rows,1):b['id']=f'SYNC-B{i:03}'
 blocks=load(S/'source-blocks.json');assert parser.rows==blocks and len(blocks)==54
 assert len([b for b in blocks if b['tag'].startswith('h')])==12
 assert len([b for b in blocks if b['tag'] in {'p','li'}])==42
 units=expected['source-unit-ledger'];blockrows=expected['source-block-ledger'];gaps=expected['gap-proposals']
 assert [x['id'] for x in blockrows]==[x['id'] for x in blocks]
 assert len(units)==len({u['id'] for u in units})==130
 checked_refs=0
 def reqref(ref):
  nonlocal checked_refs
  q=ROOT/ref['path'];v=pointer(load(q),ref['pointer']);record=pointer(load(q),ref['pointer'].rsplit('/',1)[0]);assert record['id']==ref['id'] and sha256(v.encode()).hexdigest()==ref['contract_sha256'];assert record['target_applicability']=='U';checked_refs+=1
 def caseref(ref):
  nonlocal checked_refs
  q=ROOT/ref['path'];v=pointer(load(q),ref['pointer']);record=pointer(load(q),ref['pointer'].rsplit('/',1)[0]);assert record['id']==ref['id'] and sha256(v.encode()).hexdigest()==ref['action_sha256'];assert record['kind']==ref['kind'] and record['requirements']==ref['requirements']
  for key in ['expected','comparison','documentary_expected','documentary_comparator']:assert (record[key] is None)==ref[key+'_is_null']
  assert record['expected'] is None and record['comparison'] is None and record['target_grade']=='U' and record['executed'] is False;checked_refs+=1
 source_chars=0
 for i,(b,br) in enumerate(zip(blocks,blockrows)):
  us=[u for u in units if u['block_id']==b['id']];assert br['source_units']==[u['id'] for u in us] and us
  covered=set();last=0
  for u in us:
   assert u['source_pointer']==f'/{i}/text' and u['anchor']==b['anchor'] and u['html_line']==b['html_line']
   assert pointer(blocks,u['source_pointer'])==b['text'] and u['source_sha256']==source['sha256']
   a,z=u['normalized_block_character_start'],u['normalized_block_character_end']
   assert 0<=last<=a<z<=len(b['text']) and not b['text'][last:a].strip();last=z
   assert b['text'][a:z]==u['text'] and sha256(u['text'].encode()).hexdigest()==u['text_sha256']
   assert covered.isdisjoint(range(a,z));covered.update(range(a,z))
   assert u['target_applicability']=='U' and u['complete'] is False and u['execution'] is False
   assert u['disposition'] in {derive[x] for x in ['R','U','G','M','E','I']}
   for r in u['requirements']:reqref(r)
   for c in u['cases']:caseref(c)
   if u['disposition'] in {derive['R'],derive['U']}:assert u['requirements'] and u['cases']
   if u['disposition']==derive['G']:assert u['gap_ids']
  assert not b['text'][last:].strip()
  assert {j for j,c in enumerate(b['text']) if not c.isspace()}<=covered
  source_chars+=len(b['text'])
 assert source_chars==12397
 supplemental=expected['supplemental-markup'];assert len(supplemental)==42 and Counter(x['tag'] for x in supplemental)=={'a':14,'img':14,'figcaption':14}
 markup=derive['Markup']();markup.feed(raw.decode());assert not markup.unassigned
 for x in supplemental:
  assert x['complete'] is False and x['execution'] is False and x['target_applicability']=='U'
  if x['tag']=='img':assert x['disposition']==derive['I'] and not x['attributes'].get('alt')
  if x['tag']=='figcaption':assert x['text'] and x['disposition']==derive['E']
 assert len(gaps)==len({g['id'] for g in gaps})==8
 assert {x for u in units for x in u['gap_ids']}=={g['id'] for g in gaps}
 assert sum(bool(u['gap_ids']) for u in units)==9
 for g in gaps:
  assert g['source_units']==[u['id'] for u in units if g['id'] in u['gap_ids']] and g['source_units']
  assert g['clause_delta'] and g['case_delta'] and g['target_grade']=='U' and g['executed'] is False
  assert all(g[k] is None for k in ['expected','comparison','documentary_expected','documentary_comparator'])
  for r in g['current_context_only_requirements']:reqref(r)
  for c in g['current_context_only_cases']:caseref(c)
 rec=expected['catalog-reconciliation'];reqs=load(S/'requirements.json');cases=load(S/'cases.json')
 assert {x['reference']['id'] for x in rec['requirements']}=={r['id'] for r in reqs} and len(rec['requirements'])==26
 assert {x['reference']['id'] for x in rec['cases']}=={c['id'] for c in cases} and len(rec['cases'])==36
 for row in rec['requirements']:reqref(row['reference'])
 for row in rec['cases']:caseref(row['reference'])
 assert len([r for r in rec['requirements'] if r['source_units']])==24
 assert len([c for c in rec['cases'] if c['source_units']])==26
 assert rec['documentary_expected_nonnull_current_cases']==9
 impact=expected['owner-impact'];assert len(impact['owners'])==7
 for owner in impact['owners']:assert owner['path'] in input_before
 downstream_refs=0
 for row in impact['downstream']:
  assert row['path'] in input_before
  for ref in row['references']:assert pointer(load(ROOT/row['path']),ref['pointer'])==ref['value'];downstream_refs+=1
 assert downstream_refs==573
 # All frozen R1 payloads/manifest/review remain exact; canonical bytes still match snapshots.
 for mpath in [S/'manifest-author-r1.json',P.parent/'inventory-revisions/r4-citation-crosswalk/manifest.json']:
  for name,p in load(mpath)['files'].items():check_pin(mpath.parent/name,p)
 review=load(P.parent/'reviews/synchronization-workflows-review.json')
 assert review['reviewed_manifest_sha256']==sha(S/'manifest-author-r1.json') and review['disposition']=='approved-as-partial-analyst-draft'
 for snap,canon in [('spec-r1.md','wiki/specs/synchronization-workflows.md'),('research-r1.md','wiki/research/synchronization-workflows.md')]:assert (S/snap).read_bytes()==(ROOT/canon).read_bytes()
 manifest=load(P/'manifest-author-r1.json');assert manifest['summary']==expected['summary']
 assert set(before)==set(manifest['files'])|{'manifest-author-r1.json'}|({'validation-author-r1.json'}&set(before))|({'freeze-author-r1.json'}&set(before))
 for name,p in manifest['files'].items():check_pin(P/name,p)
 if (P/'freeze-author-r1.json').exists():
  for name,p in load(P/'freeze-author-r1.json')['files'].items():check_pin(P/name,p)
 links=0
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',(P/'README.md').read_text()):
  assert not re.match(r'https?://',target);name,_,fragment=target.partition('#');assert (P/name).is_file(),target;links+=1
 whitespace=0
 for q in P.iterdir():
  if not q.is_file():continue
  result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True)
  assert result.returncode in (0,1) and not result.stdout and not result.stderr,str(q);whitespace+=1
 assert before=={str(q.relative_to(P)):sha(q) for q in P.rglob('*') if q.is_file()},'audit mutation'
 assert input_before=={p['path']:sha(ROOT/p['path']) for p in pins},'input mutation'
 return dict(status='pass',scope='literal text accounting, stable pins and pointer/null consistency; semantic sufficiency pending independent review',original_blocks=54,headings=12,paragraph_list_blocks=42,source_units=130,normalized_source_characters=12397,all_nonwhitespace_source_text_accounted_for=True,caption_image_link_rows=42,gap_spans=9,gap_proposals=8,existing_requirements=26,existing_cases=36,referenced_contract_action_pointers_checked=checked_refs,downstream_R4_pointers=573,external_pins=36,payloads=len(manifest['files']),README_links=links,untracked_whitespace_files=whitespace,all_actual_target_outcomes_null_U_unexecuted=True,canonical_and_frozen_inputs_unchanged=True,writes=False,network_runtime_hardware_original_function_execution=False,app_or_source_topic_complete=False)
if __name__=='__main__':
 assert not sys.argv[1:],'read-only validator accepts no arguments'
 print(json.dumps(check(),indent=2))
