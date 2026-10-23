"""Read-only retained static-source reconciliation. Never runs original/helper code.
Run python3 -B validate.py; no mutation or authoring arguments are accepted.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
def load(q):return json.loads(q.read_text())
def sha(q):return sha256(q.read_bytes()).hexdigest()
def check_pin(q,p):assert q.is_file() and q.stat().st_size==p['bytes'] and sha(q)==p['sha256'],str(q)
def pointer(v,p):
 for key in p.strip('/').split('/'):
  key=key.replace('~1','/').replace('~0','~');v=v[int(key)] if isinstance(v,list) else v[key]
 return v

def check():
 before={str(q.relative_to(P)):sha(q) for q in P.rglob('*') if q.is_file()}
 assert not any('__pycache__' in s for s in before),'Use python3 -B'
 # Only this analyst's guarded data derivation is loaded. It reads raw original bytes for hashes,
 # but never imports, decodes, compiles or executes any original/helper/bytecode content.
 a=runpy.run_path(str(P/'author.py'));d=a['build']()
 for name in ['source','evidence','requirements','cases','counts']:
  assert load(P/(name+'.json'))==d['sources' if name=='source' else name],name
 pins=d['sources']['pins'];assert len({p['path'] for p in pins})==len(pins)
 for p in pins:check_pin(ROOT/p['path'],p)
 for e in d['evidence']:
  q=ROOT/e['path']
  if 'json_pointer' in e:
   v=pointer(load(q),e['json_pointer'])
   b=v.encode() if isinstance(v,str) else json.dumps(v,sort_keys=True,separators=(',',':')).encode()
   if isinstance(v,str):assert len(v.splitlines())==e['line_end'] and e['line_start']==1
  else:
   lines=q.read_text().splitlines(keepends=True)
   assert 1<=e['line_start']<=e['line_end']<=len(lines)
   b=''.join(lines[e['line_start']-1:e['line_end']]).encode()
  assert sha256(b).hexdigest()==e['excerpt_sha256'],e['id']
 reqs=d['requirements'];cases=d['cases'];rids={r['id'] for r in reqs};eids={e['id'] for e in d['evidence']}
 assert len(reqs)==len(rids)==30 and len(cases)==len({c['id'] for c in cases})==37 and len(eids)==22
 assert Counter(r['provenance'] for r in reqs)=={'S':21,'I':1,'U':8}
 assert Counter(c['provenance'] for c in cases)=={'S':21,'I':1,'U':15}
 assert set.union(*(set(c['requirement_ids']) for c in cases))==rids
 assert {e for r in reqs for e in r['evidence']}==eids
 for r in reqs:
  assert r['target_grade']=='U' and r['semantic_complete'] is False
  assert set(r['evidence'])<=eids and bool(r['evidence'])==(r['provenance']!='U')
  assert not re.search(r'FUN_|DAT_|0x[0-9a-f]{7,}',r['contract'])
 for c in cases:
  assert c['action'] and 'paired baseline' in c['prerequisites'] and 'Missing capability' in c['prerequisites']
  assert set(c['requirement_ids'])<=rids and c['target_grade']=='U' and c['executed'] is False
  assert all(c[k] is None for k in ['expected','comparison','documentary_expected','documentary_comparator'])
  if c['provenance']=='U':assert c['source_claim'] is None and not c['evidence']
  else:
   r=next(r for r in reqs if r['id']==c['requirement_ids'][0]);assert c['source_claim']==r['contract'] and c['evidence']==r['evidence']
 s,r=a['pages'](d);sp=ROOT/a['SPEC'];rp=ROOT/a['RESEARCH']
 assert sp.read_text()==s==(P/'spec-author-r1.md').read_text()
 assert rp.read_text()==r==(P/'research-author-r1.md').read_text()
 sys.path.insert(0,str(ROOT/'tools'))
 from spec_browser import spec_rows,frontmatter
 browser=spec_rows(sp,s);assert len(browser)==30 and {row['id'] for row in browser}==rids
 links=0
 for q in [sp,rp]:
  assert {'id','type','status','updated','access'}<=set(frontmatter(q.read_text()))
  for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',q.read_text()):
   assert not re.match(r'https?://',target),'No new online sources'
   name,_,fragment=target.partition('#');assert (q.parent/name).is_file(),target;links+=1
 manifest=load(P/'manifest-author-r1.json')
 assert manifest['counts']==d['counts'] and manifest['status']=='partial-author-freeze-awaiting-independent-semantic-review'
 assert set(before)==set(manifest['files'])|{'manifest-author-r1.json'}|({'validation-author-r1.json'}&set(before))|({'freeze-author-r1.json'}&set(before))
 for name,p in manifest['files'].items():check_pin(P/name,p)
 for p in manifest['canonical_snapshots']:
  check_pin(ROOT/p['canonical'],p);check_pin(P/p['snapshot'],p)
 if (P/'freeze-author-r1.json').exists():
  for name,p in load(P/'freeze-author-r1.json')['files'].items():check_pin(P/name,p)
 whitespace=0
 for q in [sp,rp]+[q for q in P.iterdir() if q.is_file()]:
  result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True)
  assert result.returncode in (0,1) and not result.stdout and not result.stderr,str(q);whitespace+=1
 assert before=={str(q.relative_to(P)):sha(q) for q in P.rglob('*') if q.is_file()},'Validator mutated packet'
 return dict(status='pass',scope='static pin/locator/catalog/browser/snapshot/null/link integrity; independent semantics pending',requirements=30,provenance={'S':21,'I':1,'U':8},cases=37,evidence_entries=22,complete=0,executed=0,all_actual_and_documentary_oracles_null=True,exact_browser_ID_set=30,external_pins=len(pins),payloads=len(manifest['files']),canonical_snapshots=2,local_links=links,untracked_whitespace_files=whitespace,writes=False,original_helper_bytecode_runtime_execution=False)
if __name__=='__main__':
 assert not sys.argv[1:],'read-only validator accepts no arguments'
 print(json.dumps(check(),indent=2))
