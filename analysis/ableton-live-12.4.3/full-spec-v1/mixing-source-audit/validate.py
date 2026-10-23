"""Read-only finite retained Mixing audit checks, no product/network execution."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,re,runpy,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parents[3];M=P.parent/'mixing-workflows'
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def check_pin(p,r):assert digest(p)=={k:r[k] for k in ['bytes','sha256']},str(p)
def tree():return {str(p.relative_to(P)):digest(p) for p in P.rglob('*') if p.is_file()}
def deref(path,pointer):
 value=load(ROOT/path)
 for k in pointer.split('/')[1:]:value=value[int(k)] if isinstance(value,list) else value[k]
 return value

def check_ref(r,pins):
 assert r['catalog'] in pins
 value=deref(r['catalog'],r['json_pointer']);assert sha256(value.encode()).hexdigest()==r['value_sha256']
 row=deref(r['catalog'],r['json_pointer'].rsplit('/',1)[0]);assert row['id']==r['id']
 if 'cases' in Path(r['catalog']).name:
  assert row['expected'] is row['comparison'] is None and row['target_grade']=='U' and row['executed'] is False
  if 'documentary_expected_is_null' in r:
   for k in ['documentary_expected','documentary_comparator','expected','comparison']:assert r[k+'_is_null']==(row[k] is None)
 else:assert row['target_applicability']==r['target_applicability']=='U'

def check_claims(claims,bs,pins):
 assert len({c['id'] for c in claims})==len(claims);byblock={b['locator']:[] for b in bs}
 for c in claims:
  assert c['block'] in byblock;byblock[c['block']].append(c)
  i=int(c['source_locator']['block_json_pointer'][1:]);b=bs[i];assert b['locator']==c['block']
  a,z=c['text_span'];assert 0<=a<z<=len(b['text']) and c['source_excerpt']==b['text'][a:z]
  assert c['source_excerpt_sha256']==sha256(c['source_excerpt'].encode()).hexdigest()
  assert c['source_locator']['literal_anchor']==b['anchor'] and c['source_locator']['heading_context']==b['heading_context']
  assert c['source_locator']['html_line']==b['html_line']
  assert c['target']=='U' and c['complete'] is False and c['behavioral_coverage_credit']==0
  for r in c['requirements']+c['cases']+c['related_recording_cases']:check_ref(r,pins)
  for r in c['related_owner_routes']:check_ref(r['requirement'],pins);check_ref(r['case'],pins)
 for b in bs:
  positions=set()
  for c in byblock[b['locator']]:positions.update(range(*c['text_span']))
  assert all(i in positions for i,t in enumerate(b['text']) if not t.isspace()),b['locator']
 return sum(len(b['text']) for b in bs)

def check_proposals(props,claims):
 for p in props:
  assert all(p[k] is None for k in ['documentary_expected','documentary_comparison','expected','comparison'])
  assert p['target']=='U' and p['executed'] is False and p['complete'] is False
  assert p['claim_ids'] and set(p['claim_ids'])=={c['id'] for c in claims if p['id'] in c['gaps']}
  assert 'genuine' in p['positive_guard'] and 'never a negative pass' in p['positive_guard']
 assert {g for c in claims for g in c['gaps']}=={p['id'] for p in props}

def main():
 before=tree();pins=load(P/'input-pins.json');pinpaths={r['path'] for r in pins};assert len(pins)==len(pinpaths)==31
 for r in pins:check_pin(ROOT/r['path'],r)
 seal=digest(M/'manifest-author-r1.json')['sha256'];assert seal=='7d1fd0bcb36be47060757b3055a8b25dbb633b7a497202306984a984b0c37e2b'
 mf=load(M/'manifest-author-r1.json');assert len(mf['files'])==11
 for name,r in mf['files'].items():check_pin(M/name,r);assert str((M/name).relative_to(ROOT)) in pinpaths
 review=load(M.parent/'reviews/mixing-workflows-review.json');assert review['reviewed_manifest_sha256']==seal and review['disposition']=='approved-as-partial-analyst-draft'
 contexts=load(P/'owner-context.json');assert len(contexts)==9
 for c in contexts:check_pin(P/c['snapshot'],c) # Never compare as-of provenance with current mutable wiki.
 assert (P/'owner-snapshots/wiki/specs/mixing-workflows.md').read_bytes()==(M/'spec-r1.md').read_bytes()
 assert (P/'owner-snapshots/wiki/research/mixing-workflows.md').read_bytes()==(M/'research-r1.md').read_bytes()
 assert 'State: open' in (P/'owner-snapshots/Q046.md').read_text()
 oldpins=load(M/'input-owner-pins.json');policy=load(P/'historical-owner-pin-policy.json');assert len(oldpins)==len(policy)==18
 for i,(o,r) in enumerate(zip(oldpins,policy)):
  assert all(r[k]==o[k] for k in ['path','bytes','sha256']) and r['pin_json_pointer']==f'/{i}'
  if not o['path'].startswith('wiki/'):assert o['path'] in pinpaths;check_pin(ROOT/o['path'],o)
 assert sum(o['path'].startswith('wiki/') for o in oldpins)==12
 d=runpy.run_path(str(P/'derive.py'));built=d['build']();assert len(built)==7
 for name,value in built.items():assert load(P/name)==value,name
 bs=load(M/'source-blocks.json');claims=load(P/'claims.json');assert len(bs)==94 and len(claims)==178
 assert Counter(b['kind'] for b in bs)=={'h1':1,'h2':9,'h3':1,'p':64,'li':19}
 assert check_claims(claims,bs,pinpaths)==19584
 source=load(M/'source.json');check_pin(Path(source['path']),source);raw=Path(source['path']).read_text()
 for c in claims:
  loc=c['source_locator'];assert loc['source_sha256']==source['sha256'] and loc['source_version']==source['version'] and loc['source_capture_utc']==source['captured_utc'] and loc['source_url']==source['url']
  anchor=loc['literal_anchor'];assert loc['literal_anchor_url']==(source['url']+'#'+anchor if anchor else None)
 for r in load(P/'block-reconciliation.json'):
  b=r['raw_block'];assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and r['block']['text']==b['text']
 resources=load(P/'resources.json');assert len(resources)==56 and Counter(r['kind'] for r in resources)=={'image':21,'caption':21,'link':14}
 for r in resources:
  a=r['raw_start'];z=raw.index('>',a)+1;assert sha256(raw[a:z].encode()).hexdigest()==r['starttag_sha256'] and r['target']=='U' and r['complete'] is False
 req=load(M/'requirements.json');cases=load(M/'cases.json');rev=load(P/'existing-catalog-dispositions.json')
 assert len(req)==23 and Counter(r['provenance'] for r in req)=={'D12':18,'U':5} and len(cases)==33
 assert sum(c['documentary_expected'] is not None for c in cases)==13
 for c in cases:assert c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
 for kind,rows in [('requirements',req),('cases',cases)]:
  assert [r['id'] for r in rows]==[r['id'] for r in rev[kind]]
  for r in rev[kind]:assert r['claim_ids']==[c['id'] for c in claims if any(x['id']==r['id'] for x in c[kind])]
 spec=(P/'owner-snapshots/wiki/specs/mixing-workflows.md').read_text();assert set(re.findall(r'^### (REQ-MIXING-WORKFLOW-[\w-]+)',spec,re.M))=={r['id'] for r in req}
 props=load(P/'proposed-deltas-derived.json');assert len(props)==17;check_proposals(props,claims)
 fixtures=load(P/'fixtures.json');assert [fixtures['sentence_fixture'][a:z] for a,z in d['spans'](fixtures['sentence_fixture'])]==fixtures['sentence_fixture_expected']
 for f in fixtures['negative_mutations']:
  cc=deepcopy(claims);pp=deepcopy(props)
  if f['kind']=='omit-block':cc=[c for c in cc if c['block']!=f['block']]
  elif f['kind']=='change-quote':next(c for c in cc if c['id']==f['claim'])['source_excerpt']+=' altered'
  elif f['kind']=='wrong-pointer':next(c for c in cc if c['id']==f['claim'])['requirements'][0]['json_pointer']='/1/contract'
  elif f['kind']=='promote-oracle':next(p for p in pp if p['id']==f['proposal'])['expected']='fabricated target result'
  else:raise AssertionError(f)
  try:check_claims(cc,bs,pinpaths);check_proposals(pp,cc)
  except AssertionError:pass
  else:raise AssertionError('negative mutation not rejected: '+f['kind'])
 links=0
 for path in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):assert (P/path).is_file();links+=1
 authored=[p for p in P.rglob('*') if p.is_file() and 'owner-snapshots' not in p.relative_to(P).parts]
 for p in authored:
  result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True);assert result.returncode in (0,1) and not result.stdout and not result.stderr,(p,result.stdout,result.stderr)
 sealed=(P/'manifest.json').exists()
 if sealed:
  manifest=load(P/'manifest.json');assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and p.name!='manifest.json'}==set(manifest['files'])
  for name,r in manifest['files'].items():check_pin(P/name,r)
  assert manifest['summary']==load(P/'summary.json')
 assert tree()==before,'read-only check mutated audit files'
 for r in pins:check_pin(ROOT/r['path'],r)
 print(json.dumps(dict(status='pass',sealed=sealed,scope='static integrity only; independent semantic review pending',input_pins=31,historical_payloads=11,as_of_contexts=9,source_blocks=94,claims=178,resources=56,requirements=23,cases=33,proposals=17,negative_fixtures=4,decimal_sentence_fixture=True,readme_links=links,authored_whitespace_files=len(authored),target='U',writes=False,runtime=False),indent=2))
if __name__=='__main__':main()
