"""Read-only focused ARR-R2-REVIEW-001 successor check; no old main replay.
Two inspected own pure assertions and four Browser definitions are AST-selected.
No historical adapter, original source, native/vendor/runtime or report writes.
"""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import ast,json,re,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
assert sys.dont_write_bytecode and sys.argv[1:] in (['--preflight'],['--check'])
pre=sys.argv[1:]==['--preflight'];M=P/'manifest-author-r3.json';assert pre!=M.exists()
load=lambda p:json.loads(p.read_text())
def info(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert info(p)=={k:r[k] for k in ['bytes','sha256']},p
def current_files():return {str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
prior=load(P/'prior-files-r3.json');assert len(prior)==35
oldmanifest=load(P/'manifest-author-r2.json');assert set(prior)==set(oldmanifest['files'])|{'manifest-author-r2.json'}
assert info(P/'manifest-author-r2.json')['sha256']=='66839c8527bf83eb2dbc0262067b8d21a71d2372c0de41823479f68faa491b7c'
inputs=load(P/'inputs-r2.json')+load(P/'inputs-r3.json');assert len(inputs)==109 and len({r['path'] for r in inputs})==109 and not any(r['path'].startswith('wiki/') for r in inputs)
sp=ROOT/'wiki/specs/arrangement-editing.md';rp=ROOT/'wiki/research/arrangement-editing.md'
consumerpaths={ROOT/r['consumer'] for r in load(P/'canonical-consumers-r2.json')['hash_occurrences']}
watched={P/n for n in current_files()}|{ROOT/r['path'] for r in inputs}|consumerpaths|{sp,rp};before={str(q):info(q) for q in watched}
for n,r in prior.items():pin(P/n,r)
for r in inputs:pin(ROOT/r['path'],r)
review=load(P/'inputs-r3.json')[0];assert review['sha256']=='d1e86f3f1231742023ff64bafc5564a6cb4e997210c46ec3625046c21516ecb9'
pin(P/'review-owner-r2.json',review)
assert load(P/'review-owner-r2.json')['required_findings'][0]['id']=='ARR-R2-REVIEW-001'
old=load(P/'cases-r2.json');cases=load(P/'cases-r3.json');req=load(P/'requirements-r2.json');assert len(req)==42
numbers=[10,16,17,24,25,26,27,28,29]
changes=[]
for i,(a,b) in enumerate(zip(old,cases)):
 assert set(a)==set(b)
 for k in a:
  if a[k]!=b[k]:changes.append(dict(pointer=f'/{i}/{k}',before=a[k],after=b[k]))
 expected={'documentary_expected','documentary_comparator'} if i+1 in numbers else set()
 assert {k for k in a if a[k]!=b[k]}==expected,(a['id'],expected)
 for k in expected:assert a[k] is not None and b[k] is None
 assert b['source_claim']==a['source_claim'] and b.get('original_documentary_predicate')==a.get('original_documentary_predicate') and b['setup_and_action']==a['setup_and_action']
delta=load(P/'delta-r3.json');assert len(changes)==18 and sorted(changes,key=lambda d:d['pointer'])==sorted(delta['field_deltas'],key=lambda d:d['pointer'])
assert delta['documentary_named']==43 and delta['documentary_null']==41
# Load only the reviewed pure functions, never old module imports/main/checker.
def own_functions(file,names,env):
 tree=ast.parse(file.read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 assert {n.name for n in defs}==names and all(not n.decorator_list for n in defs)
 exec(compile(ast.Module(body=defs,type_ignores=[]),str(file)+' [selected own pure definitions]','exec'),env)
 return env
oldpure=own_functions(P/'validate-r2.py',{'check_oracles','guards'},{'rm':{r['id']:r for r in req}})
def corrected(rows,named=43,nulls=41):
 oldpure['check_oracles'](rows);oldpure['guards'](rows)
 for n in numbers:assert rows[n-1]['documentary_expected'] is rows[n-1]['documentary_comparator'] is None
 assert sum(c['documentary_expected'] is not None for c in rows)==named==43
 assert sum(c['documentary_expected'] is None for c in rows)==nulls==41
corrected(cases)
# Current focused fixture rejects promoting any corrected numeric pair, including coherent dual mutation.
rejected=[]
for name in ['promote-numeric-pair','false-visible-only-count','actual-result','lost-productive-effect','lost-same-start','flag-only-Follow']:
 rows=deepcopy(cases);named=43;nulls=41
 if name=='promote-numeric-pair':
  rows[9]['documentary_expected']=old[9]['documentary_expected'];rows[9]['documentary_comparator']=old[9]['documentary_comparator'];named=44;nulls=40
 elif name=='false-visible-only-count':named=52;nulls=32
 elif name=='actual-result':rows[9]['actual_expected']='invented numeric runtime result'
 elif name=='lost-productive-effect':rows[22]['setup_and_action']='enabled flag only'
 elif name=='lost-same-start':rows[54]['setup_and_action']='different starts only'
 else:rows[68]['setup_and_action']='Follow visible only'
 try:corrected(rows,named,nulls)
 except AssertionError:rejected.append(name)
 else:raise AssertionError('Unsafe correction accepted: '+name)
assert len(rejected)==6
r=subprocess.run([sys.executable,'-B',str(P/'derive-r3.py'),'--check'],capture_output=True,text=True);assert r.returncode==0,(r.stdout,r.stderr)
assert sp.read_bytes()==(P/'spec-r3.md').read_bytes() and rp.read_bytes()==(P/'research-r3.md').read_bytes()
assert 'revision: 3\n' in sp.read_text() and 'revision: 3\n' in rp.read_text()
browser=own_functions(ROOT/'tools/spec_browser.py',{'anchor','frontmatter','cells','spec_rows'},{'re':re})
rows=browser['spec_rows'](sp,sp.read_text());assert len(rows)==42 and {r['id'] for r in rows}=={r['id'] for r in req}
# Entire requirement Markdown spans remain exact, including all seven public-role clauses.
oldspec=(P/'spec-r2.md').read_text();spec=sp.read_text()
for r in req:
 h='### '+r['id']+' — ';a=oldspec.index(h);b=spec.index(h)
 def body(s,i):return re.split(r'\n##?#[^#]|\n## ',s[i:],maxsplit=1)[0]
 assert body(oldspec,a)==body(spec,b),r['id']
for n in numbers:
 line=next(s for s in spec.splitlines() if s.startswith(f'| AR-{n:03} |'))
 assert 'Source claim only; documentary numeric/duration outcome and comparator null.' in line and cases[n-1]['original_documentary_predicate'] in line
links=0
for p in [sp,rp,P/'README-r3.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',p.read_text()):
  if re.match('[A-Za-z]+:',target):continue
  path,_,fragment=target.partition('#');q=(p.parent/path).resolve() if path else p
  if pre and q==M:continue
  assert q.is_file(),(p,target)
  if fragment and q.suffix=='.md':
   slug=lambda h:re.sub(r'[^\w\- ]','',re.sub(r'<[^>]*>|[`*]','',h).lower()).replace(' ','-')
   assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$',q.read_text(),re.M)},(p,target)
  links+=1
white=0
for q in {P/n for n in current_files() if n not in prior}|{sp,rp}:
 if q.suffix in ['.json','.md','.py']:
  if q.suffix=='.json':load(q)
  raw=q.read_bytes();assert raw.endswith(b'\n') and all(line.rstrip(b' \t')==line for line in raw.splitlines()),q;white+=1
if not pre:
 m=load(M);assert set(current_files())==set(m['files'])|{M.name}
 for n,r in m['files'].items():pin(P/n,r)
 for r in m['canonicals']:pin(ROOT/r['path'],r);pin(P/r['snapshot'],r)
assert before=={str(q):info(q) for q in watched}
print(json.dumps(dict(status='passed-focused-read-only-preflight' if pre else 'passed-focused-read-only-frozen',finding='ARR-R2-REVIEW-001',requirements=42,cases=84,changed_documentary_fields=18,changed_numeric_pairs=9,documentary_named=43,documentary_null=41,source_predicate_action_requirement_changes=0,all_actual_null_U_unexecuted=True,preserved_R1_R2_files=35,preserved_review=True,input_pins=109,unsafe_mutations_rejected=rejected,pure_assertions_only_no_old_main=True,Browser_IDs=42,links=links,authored_whitespace_files=white,watched_paths=len(watched),all_unchanged=True,old_checker_replay_or_adapter=False,original_native_vendor_runtime=False,writes=False,complete=0),indent=2))
