"""Read-only finite source-audit integrity checks. No application/reader/network calls."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,re,runpy,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'keyboard-navigation'
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def check_pin(p,r):assert digest(p)=={k:r[k] for k in ['bytes','sha256']},str(p)
def tree():return {str(p.relative_to(P)):digest(p) for p in P.rglob('*') if p.is_file()}
def deref(path,pointer):
 row=load(ROOT/path)
 for part in pointer.split('/')[1:]:row=row[int(part)] if isinstance(row,list) else row[part.replace('~1','/').replace('~0','~')]
 return row

def check_refs(refs,pins):
 for r in refs:
  assert r['catalog'] in pins
  value=deref(r['catalog'],r['json_pointer']);assert isinstance(value,str) and sha256(value.encode()).hexdigest()==r['value_sha256']
  row=deref(r['catalog'],r['json_pointer'].rsplit('/',1)[0]);assert row['id']==r['id'] and r['basis']==row['basis']
  if r['catalog'].endswith('/cases.json'):
   assert r['legacy_documentary_expected_is_null']==(row['expected'] is None)
   assert r['exact_target']==row['exact_target']=='U' and r['execution']==row['execution']=='not-run'
   assert r['kind']==row['kind'] and r['actual_target_oracle'] is None

def check_claims(claims,blocks,pins):
 assert len({c['id'] for c in claims})==len(claims);byblock={b['id']:[] for b in blocks}
 for c in claims:
  assert c['block'] in byblock;byblock[c['block']].append(c)
  i=int(c['source_locator']['block_json_pointer'][1:]);b=blocks[i];assert b['id']==c['block']
  a,z=c['text_span'];assert 0<=a<z<=len(b['text']) and c['source_excerpt']==b['text'][a:z]
  assert c['source_excerpt_sha256']==sha256(c['source_excerpt'].encode()).hexdigest()
  assert c['source_locator']['literal_anchor']==b['attributes'].get('id') and c['source_locator']['heading_context']==b['heading_context']
  assert c['source_locator']['html_line']==b['html_line'] and c['source_locator']['html_column']==b['html_column']
  if b['kind']=='tr':assert c['source_cell_quotes']==[x['text'] for x in b['cells']] and 'audit-only' in c['excerpt_representation']
  assert c['target']=='U' and c['complete'] is False and c['behavioral_coverage_credit']==0
  check_refs(c['requirements']+c['cases'],pins)
 for b in blocks:
  covered=set()
  for c in byblock[b['id']]:covered.update(range(*c['text_span']))
  assert all(i in covered for i,x in enumerate(b['text']) if not x.isspace()),b['id']
 return sum(len(b['text']) for b in blocks)

def check_proposals(proposals,claims):
 assert len({g['id'] for g in proposals})==len(proposals)
 for g in proposals:
  assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','expected','comparison'])
  assert g['target']=='U' and g['executed'] is False and g['behavioral_coverage_credit']==0
  assert 'positive' in g['positive_guard'] and 'never a negative pass' in g['positive_guard']
  assert g['claim_ids'] and set(g['claim_ids'])=={c['id'] for c in claims if g['id'] in c['gaps']}
 assert {g for c in claims for g in c['gaps']}=={g['id'] for g in proposals}

def main():
 before=tree();pins=load(P/'input-pins.json');pinpaths={r['path'] for r in pins};assert len(pins)==len(pinpaths)==110
 for r in pins:check_pin(ROOT/r['path'],r)
 seal=digest(K/'manifest.json')['sha256'];assert seal=='3f7278083db7c68ff1ed424c025012808961f6c27c4d9e35ddc6bdde6f091787'
 old=load(K/'manifest.json');assert old['revision']==4 and len(old['payloads'])==109
 resolutions=load(P/'historical-input-resolutions.json');assert len(resolutions)==2
 mapped={r['source_path']:r for r in resolutions}
 for i,r in enumerate(old['payloads']):
  if r['path'].startswith('wiki/'):
   x=mapped[r['path']];assert x['manifest_sha256']==seal and x['payload_json_pointer']==f'/payloads/{i}'
   assert {k:x[k] for k in ['bytes','sha256']}=={k:r[k] for k in ['bytes','sha256']};check_pin(P/x['snapshot'],r)
  else:assert r['path'] in pinpaths;check_pin(ROOT/r['path'],r)
 contexts=load(P/'owner-context.json');assert len(contexts)==2
 for r in contexts:check_pin(P/r['snapshot'],r) # As-of provenance is not a live wiki hash assertion.
 review=load(K.parent/'reviews/keyboard-navigation-review-final.json')
 assert review['disposition']=='approved-as-partial-analyst-draft-with-reviewed-corrections' and review['checks']['current_manifest_sha256']==seal
 d=runpy.run_path(str(P/'derive.py'));built=d['build']();assert len(built)==8
 for name,value in built.items():assert load(P/name)==value,name
 blocks=load(P/'source-blocks.json');claims=load(P/'claims.json');sources=load(K/'sources.json')
 assert len(blocks)==541 and len(claims)==641
 assert Counter(b['kind'] for b in blocks)=={'h1':2,'h2':34,'h3':10,'h4':8,'p':110,'li':58,'tr':319}
 assert Counter(b['source_id'] for b in blocks)=={'KN1':152,'KN2':389}
 assert check_claims(claims,blocks,pinpaths)==42741
 for b in blocks:
  s=sources[int(b['source_id'][-1])-1];raw=(ROOT/s['path']).read_text();assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
  assert len(raw[:b['raw_start']].split('\n'))==b['html_line']
 for c in claims:
  s=sources[int(c['block'][2])-1];loc=c['source_locator']
  for a,b in [('source_path','path'),('source_sha256','sha256'),('source_version','version'),('source_capture_utc','captured_utc'),('source_url','url')]:assert loc[a]==s[b]
  anchor=loc['literal_anchor'];assert loc['literal_anchor_url']==(s['url']+'#'+anchor if anchor else None)
 resources=load(P/'resources.json');assert len(resources)==34 and Counter(r['kind'] for r in resources)=={'link':24,'image':5,'caption':5}
 for r in resources:
  s=sources[int(r['source_id'][-1])-1];raw=(ROOT/s['path']).read_text();a=r['raw_start'];z=raw.index('>',a)+1
  assert sha256(raw[a:z].encode()).hexdigest()==r['starttag_sha256'] and r['target']=='U' and r['complete'] is False
 ledger=load(P/'binding-reconciliation.json');bindings=load(K/'shortcut-bindings.json')
 assert len(ledger)==len(bindings)==292 and [x['binding']['id'] for x in ledger]==[x['id'] for x in bindings]
 for i,(r,original) in enumerate(zip(ledger,bindings)):
  b=deref(str((K/'shortcut-bindings.json').relative_to(ROOT)),r['binding']['json_pointer']);assert b==original and r['binding']['json_pointer']==f'/{i}'
  assert [c['text'] for c in r['source_cells']]==[original['command'],original['windows_source'],original['macos_source']]
  assert r['binding']['raw_row_sha256']==original['cell_html_sha256']
  assert all(r[k] is False for k in ['normative_command_contract','command_owner_reconciled','dispatch_tested','complete'])
  assert r['target']=='U' and r['actual_expected'] is r['actual_comparison'] is None
  assert all(x in {b['id'] for b in blocks} for x in r['explicit_context_blocks'])
 assert len({int(r['binding']['id'][6:8]) for r in ledger})==27
 assert sum(c['disposition']=='binding-discovery-not-command-contract' for c in claims)==292
 req=load(K/'requirements.json');cases=load(K/'cases.json');reverse=load(P/'existing-catalog-dispositions.json')
 assert len(req)==21 and Counter(r['basis'] for r in req)=={'D12':19,'U':2}
 assert len(cases)==42 and Counter(r['basis'] for r in cases)=={'D12':34,'U':8}
 for r in cases:assert r['exact_target']=='U' and r['execution']=='not-run' and ((r['expected'] is None)==(r['basis']=='U'))
 for kind,rows in [('requirements',req),('cases',cases)]:
  assert [r['id'] for r in reverse[kind]]==[r['id'] for r in rows]
  for r in reverse[kind]:assert r['claim_ids']==[c['id'] for c in claims if any(a['id']==r['id'] for a in c[kind])]
 spec=(P/'canonical-snapshots/spec-r4.md').read_text()
 assert set(re.findall(r'^### (REQ-KEYBOARD-NAV-\d+)',spec,re.M))=={r['id'] for r in req}
 assert set(re.findall(r'^\| (NAV-\d+) \|',spec,re.M))=={r['id'] for r in cases}
 proposals=load(P/'proposed-deltas-derived.json');assert len(proposals)==23;check_proposals(proposals,claims)
 fixtures=load(P/'fixtures.json');assert fixtures['source_guard']['quote']==next(b['text'] for b in blocks if b['id']==fixtures['source_guard']['block'])
 assert [fixtures['sentence_fixture'][a:z] for a,z in d['spans'](fixtures['sentence_fixture'])]==fixtures['sentence_fixture_expected']
 for f in fixtures['negative_mutations']:
  cc=deepcopy(claims);pp=deepcopy(proposals)
  if f['kind']=='omit-block':cc=[c for c in cc if c['block']!=f['block']]
  elif f['kind']=='change-quote':next(c for c in cc if c['id']==f['claim'])['source_excerpt']+=' altered'
  elif f['kind']=='wrong-pointer':next(c for c in cc if c['id']==f['claim'])['requirements'][0]['json_pointer']='/0/body'
  elif f['kind']=='promote-oracle':next(g for g in pp if g['id']==f['proposal'])['expected']='fabricated target result'
  else:raise AssertionError(f)
  try:
   check_claims(cc,blocks,pinpaths);check_proposals(pp,cc)
  except AssertionError:pass
  else:raise AssertionError('negative fixture not rejected: '+f['kind'])
 links=0
 for dest in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):assert (P/dest).is_file();links+=1
 authored=[p for p in P.rglob('*') if p.is_file() and 'canonical-snapshots' not in p.relative_to(P).parts]
 for p in authored:
  r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True)
  assert r.returncode in (0,1) and not r.stdout and not r.stderr,(str(p),r.stdout,r.stderr)
 sealed=(P/'manifest.json').exists()
 if sealed:
  mf=load(P/'manifest.json');assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and p.name!='manifest.json'}==set(mf['files'])
  for name,r in mf['files'].items():check_pin(P/name,r)
  assert mf['summary']==load(P/'summary.json')
 assert tree()==before,'audit file mutation during read-only validation'
 for r in pins:check_pin(ROOT/r['path'],r)
 print(json.dumps(dict(status='pass',sealed=sealed,scope='static integrity only; independent audit semantic review pending',input_pins=110,historical_payloads=109,historical_canonical_resolutions=2,source_chapters=2,source_blocks=541,source_text_characters=42741,claims=641,bindings=292,tables=27,resources=34,requirements=21,cases=42,gap_groups=23,negative_fixtures=4,decimal_sentence_fixture=True,readme_links=links,authored_whitespace_files=len(authored),all_target_U=True,writes=False,runtime=False),indent=2))
if __name__=='__main__':main()
