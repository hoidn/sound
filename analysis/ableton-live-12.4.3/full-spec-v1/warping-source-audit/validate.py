"""Read-only finite source-audit integrity checks; no application or network calls."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,re,runpy,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parents[3];W=P.parent/'warping-workflows'
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def tree():return {str(p.relative_to(P)):digest(p) for p in P.rglob('*') if p.is_file()}
def check_pin(p,row):assert digest(p)=={k:row[k] for k in ('bytes','sha256')},str(p)
def deref(path,pointer):
 value=load(ROOT/path)
 for part in pointer.split('/')[1:]:value=value[int(part)] if isinstance(value,list) else value[part.replace('~1','/').replace('~0','~')]
 return value

def check_refs(refs,pins):
 for r in refs:
  assert r['catalog'] in pins and '/wiki/' not in r['catalog']
  value=deref(r['catalog'],r['json_pointer']);assert isinstance(value,str)
  assert sha256(value.encode()).hexdigest()==r['value_sha256']
  row=deref(r['catalog'],r['json_pointer'].rsplit('/',1)[0]);assert row['id']==r['id']
  if r['catalog'].endswith('/cases.json'):
   for key in ['kind','requirements','target_grade','executed']:assert r[key]==row[key]
   for key in ['documentary_expected','documentary_comparator','expected','comparison']:assert r[key+'_is_null']==(row[key] is None)
   assert row['expected'] is row['comparison'] is None and row['target_grade']=='U' and row['executed'] is False
  else:assert r['provenance']==row.get('provenance',row.get('strength')) and r['target_applicability']==row['target_applicability']=='U'

def check_claims(claims,blocks,pins):
 assert len({c['id'] for c in claims})==len(claims)
 byblock={b['locator']:[] for b in blocks}
 for c in claims:
  assert c['block'] in byblock;byblock[c['block']].append(c)
  i=int(c['source_locator']['block_json_pointer'][1:]);b=blocks[i]
  assert b['locator']==c['block'] and c['source_locator']['block_text_json_pointer']==f'/{i}/text'
  a,z=c['text_span'];assert 0<=a<z<=len(b['text'])
  assert c['source_excerpt']==b['text'][a:z]
  assert c['source_excerpt_sha256']==sha256(c['source_excerpt'].encode()).hexdigest()
  assert c['source_locator']['literal_anchor']==b['anchor']
  assert c['source_locator']['heading_context']==b['heading_context']
  assert c['source_locator']['literal_anchor_url']==(c['source_locator']['source_url']+'#'+b['anchor'] if b['anchor'] else None)
  assert c['source_locator']['html_line']==b['html_line']
  assert c['target_applicability']=='U' and c['complete'] is False and c['behavioral_coverage_credit']==0
  check_refs(c['existing_requirements']+c['existing_cases'],pins)
  for route in c['existing_owner_routes']:check_refs([route['requirement'],route['case']],pins)
 for b in blocks:
  covered=set()
  for c in byblock[b['locator']]:covered.update(range(*c['text_span']))
  assert all(i in covered for i,t in enumerate(b['text']) if not t.isspace()),b['locator']
 return sum(len(b['text']) for b in blocks)

def main():
 before=tree();pins=load(P/'input-pins.json');pinpaths={r['path'] for r in pins}
 assert len(pins)==len(pinpaths)==35
 for r in pins:check_pin(ROOT/r['path'],r)
 mf=load(W/'manifest-author-r1.json');assert len(mf['files'])==14
 assert digest(W/'manifest-author-r1.json')['sha256']=='b17efb2eb29b165239bab421e53e49f69117e69fa80f97927ad0e54dac76ba68'
 for name,r in mf['files'].items():check_pin(W/name,r);assert str((W/name).relative_to(ROOT)) in pinpaths
 review=load(P.parent/'reviews/warping-workflows-review.json')
 assert review['reviewed_manifest_sha256']==digest(W/'manifest-author-r1.json')['sha256'] and review['disposition']=='approved-as-partial-analyst-draft'
 context=load(P/'owner-context.json');assert len(context)==10
 for r in context:check_pin(P/r['snapshot'],r) # Historical provenance is deliberately not a live wiki comparison.
 assert (P/'owner-snapshots/wiki/specs/warping-workflows.md').read_bytes()==(W/'spec-r1.md').read_bytes()
 assert (P/'owner-snapshots/wiki/research/warping-workflows.md').read_bytes()==(W/'research-r1.md').read_bytes()
 assert 'open' in (P/'owner-snapshots/Q032.md').read_text().lower()
 d=runpy.run_path(str(P/'derive.py'));built=d['build']()
 for name,value in built.items():assert load(P/name)==value,name
 assert len(built)==7
 source=load(W/'sources.json')[0];check_pin(W/source['path'],source)
 assert source['bytes']==283979 and source['sha256']=='295a442252730b7f1bb6154b9cbfe041f09c6d40d45d487a42e793ae8423c2ad'
 raw=(W/source['path']).read_text();config=load(W/'derivations.json')
 parser=runpy.run_path(str(W/'source_parser.py'));blocks=parser['extract'](raw,config['name'],config['start_anchor'],config['stop_heading_level'])
 assert blocks==load(W/'manual-blocks.json') and len(blocks)==131
 assert (W/'manual.txt').read_text()==''.join(f"{b['locator']} HTML:{b['html_line']} {b['text']}\n" for b in blocks)
 assert Counter(b['kind'] for b in blocks)=={'h1':1,'h2':3,'h3':16,'h4':7,'p':89,'li':15}
 claims=load(P/'claims.json');chars=check_claims(claims,blocks,pinpaths)
 assert chars==24667 and len(claims)==248
 for c in claims:
  loc=c['source_locator'];assert (loc['source_sha256'],loc['source_version'],loc['source_capture_utc'],loc['source_url'])==(source['sha256'],source['declared_version'],source['captured_utc'],source['url'])
 for b in load(P/'block-reconciliation.json'):
  r=b['raw_paragraph_or_heading'];assert raw[r['raw_start']:r['raw_end']]==r['raw_html']
  assert r['text']==b['block']['text'] and b['all_nonwhitespace_text_accounted_for'] is True
 resources=load(P/'resources.json');assert len(resources)==74 and Counter(r['kind'] for r in resources)=={'link':29,'image':24,'caption':21}
 for r in resources:
  start=r['raw_start'];end=raw.index('>',start)+1
  assert sha256(raw[start:end].encode()).hexdigest()==r['starttag_sha256']
  assert r['source_sha256']==source['sha256'] and r['complete'] is False
 req=load(W/'requirements.json');cases=load(W/'cases.json');reverse=load(P/'existing-catalog-dispositions.json')
 assert len(req)==50 and Counter(r['provenance'] for r in req)=={'D12':44,'U':6} and len(cases)==88
 assert sum(c['documentary_expected'] is not None for c in cases)==41
 for c in cases:assert c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
 for key,rows in [('requirements',req),('cases',cases)]:assert [r['id'] for r in reverse[key]]==[r['id'] for r in rows]
 gaps=load(P/'proposed-deltas-derived.json');assert len(gaps)==16 and {g['id'] for g in gaps}=={f'G{i:02}' for i in range(1,17)}
 gapclaims={g for c in claims for g in c['gaps']};assert gapclaims=={g['id'] for g in gaps}
 for g in gaps:
  assert all(g[k] is None for k in ['documentary_expected','documentary_comparator','expected','comparison'])
  assert g['executed'] is False and g['target_grade']=='U' and g['behavioral_coverage_credit']==0
  assert 'positive' in g['positive_guard'] and 'never a negative pass' in g['positive_guard']
  assert set(g['claim_ids'])=={c['id'] for c in claims if g['id'] in c['gaps']}
 assert sum(c['disposition']=='missing-requirement-case-or-context' for c in claims)==41
 fixtures=load(P/'fixtures.json');assert fixtures['source_guard']['quote']==next(b['text'] for b in blocks if b['locator']==fixtures['source_guard']['block'])
 assert [fixtures['sentence_fixture'][a:z] for a,z in d['sentences'](fixtures['sentence_fixture'])]==fixtures['sentence_fixture_expected']
 for f in fixtures['negative_mutations']:
  x=deepcopy(claims)
  if f['kind']=='omit-block':x=[c for c in x if c['block']!=f['block']]
  elif f['kind']=='change-quote':next(c for c in x if c['id']==f['claim'])['source_excerpt']+=' altered'
  elif f['kind']=='wrong-pointer':next(c for c in x if c['id']==f['claim'])['existing_requirements'][0]['json_pointer']='/0/contract'
  else:raise AssertionError(f)
  try:check_claims(x,blocks,pinpaths)
  except AssertionError:pass
  else:raise AssertionError('negative fixture did not fail: '+f['kind'])
 links=0
 for dest in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):assert (P/dest).is_file();links+=1
 authored=[p for p in P.rglob('*') if p.is_file() and 'owner-snapshots' not in p.relative_to(P).parts]
 for p in authored:
  r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True)
  assert r.returncode in (0,1) and not r.stdout and not r.stderr,(p,r.stdout,r.stderr)
 sealed=(P/'manifest.json').exists()
 if sealed:
  seal=load(P/'manifest.json');actual={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and p.name!='manifest.json'}
  assert actual==set(seal['files'])
  for name,r in seal['files'].items():check_pin(P/name,r)
  assert seal['summary']==load(P/'summary.json')
 assert tree()==before,'read-only checker changed audit files'
 for r in pins:check_pin(ROOT/r['path'],r)
 result=dict(status='pass',sealed=sealed,scope='static source-audit integrity only; semantic review pending',input_pins=len(pins),historical_payloads=14,owner_context_snapshots=10,source_blocks=131,source_characters=chars,claims=248,resources=74,requirements=50,cases=88,gap_groups=16,negative_fixtures=3,decimal_sentence_fixture=True,readme_links=links,authored_whitespace_files=len(authored),all_target_U=True,executed=0,writes=False)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
