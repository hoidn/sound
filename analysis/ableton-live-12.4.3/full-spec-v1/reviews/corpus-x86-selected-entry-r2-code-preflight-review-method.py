"""Independent stdlib-only R2 literal reconstruction; no supplied code execution."""
from pathlib import Path
import ast,datetime,hashlib,json
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P=B/'depth-corpus-x86-selected-entry-preparation-r2';OLD=B/'depth-corpus-x86-selected-entry-preparation'
A=B/'depth-corpus-x86-selected-entry-fixture';O=B/'reviews/corpus-x86-selected-entry-fixture-selected-execution'
R=B/'reviews/corpus-x86-selected-entry-r2-code-preflight-review-evidence.json'
assert not R.exists()
def load(p):return json.loads(p.read_text())
def identity(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):n+=len(b);h.update(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def verify_inventory(p,m):
 rows=load(p/m)['files'];paths={p/x['path'] for x in rows}
 assert paths=={q for q in p.rglob('*') if q.is_file() and q!=p/m}
 for x in rows:
  q=p/x['path'];assert not q.is_symlink();got=identity(q);assert (got['bytes'],got['sha256'])==(x['bytes'],x['sha256'])
 return paths|{p/m}
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
pins=load(P/'inputs.json')['pins'];assert len(pins)==32
oldpaths=set()
for q,m in [(OLD,'manifest-preparation.json'),(A,'manifest.json'),(O,'manifest.json')]:oldpaths|=verify_inventory(q,m)
current=verify_inventory(P,'manifest-preparation.json')
assert len(current)==12 and len(oldpaths)==56
watch={Path(x['path']) for x in pins}|current
assert len(watch)==44
watch|=oldpaths
before=[identity(q) for q in sorted(watch)]
for x in pins:assert identity(Path(x['path']))==x
assert identity(P/'manifest-preparation.json')['sha256']=='7f1cbcb640fa6ebe8247c4058f63fcee0ab64ea8555bb5d48747ccc77099e9a8'
delta=load(P/'source-delta.json');reconstructed=[]
for f in delta['files']:
 assert identity(Path(f['before']['path']))==f['before'] and identity(Path(f['after']['path']))==f['after']
 lines=Path(f['before']['path']).read_text().splitlines(keepends=True)
 for e in reversed(f['edits']):
  a,z=e['old_line_start_zero'],e['old_line_end_exclusive'];assert hashlib.sha256(''.join(lines[a:z]).encode()).hexdigest()==e['old_text_sha256']
  lines[a:z]=e['replacement'].splitlines(keepends=True)
 assert ''.join(lines)==Path(f['after']['path']).read_text()
 reconstructed.append(dict(file=Path(f['after']['path']).name,edits=len(f['edits'])))
j0=(OLD/'CorpusX86SelectedExport.java').read_text();j1=(P/'CorpusX86SelectedExport.java').read_text()
d0=(OLD/'run-selected.py').read_text();d1=(P/'run-selected.py').read_text()
oldthrow='throw new IllegalArgumentException("Effective JDK/4GiB heap/CPU2 identity mismatch");'
newthrow='throw new IllegalArgumentException("Effective JDK/4GiB heap/CPU2 identity mismatch: java.version="+System.getProperty("java.version")+", maxMemory="+Runtime.getRuntime().maxMemory()+", availableProcessors="+Runtime.getRuntime().availableProcessors()+", defaultPool="+SystemUtilities.getDefaultThreadPoolSize()+", cpu.core.override="+System.getProperty("cpu.core.override")+", cpu.core.limit="+System.getProperty("cpu.core.limit"));'
assert j0.count(oldthrow)==1 and j1.count(newthrow)==1
expected_java=j0.replace(oldthrow,newthrow)
paths=[("PRE=BASE/'depth-corpus-x86-selected-entry-preparation'","PRE=BASE/'depth-corpus-x86-selected-entry-preparation-r2'"),("return BASE/('depth-corpus-x86-selected-entry-'+mode)","return BASE/('depth-corpus-x86-selected-entry-'+mode+'-r2')"),("('corpus-x86-selected-entry-'+mode+'-selected-execution')","('corpus-x86-selected-entry-'+mode+'-r2-selected-execution')")]
expected_driver=d0
for old,new in paths:assert expected_driver.count(old)==1;expected_driver=expected_driver.replace(old,new)
assert j1==expected_java and d1==expected_driver
start='        if(!"21.0.12.1"';end='            throw new IllegalArgumentException("Effective JDK'
assert j0[j0.index(start):j0.index(end)]==j1[j1.index(start):j1.index(end)]
negative=[]
for name,text in [('guard_weakened',j1.replace('maxMemory()!=4294967296L','maxMemory()!=0L')),('missing_diagnostic_value',j1.replace(', defaultPool=','')),('body_guard_weakened',j1.replace('body.contains(end)','false'))]:
 assert text!=expected_java;negative.append(name)
for name,text in [('old_destination',d1.replace("+mode+'-r2')","+mode)")),('changed_environment',d1.replace("'GHIDRA_HEADLESS_MAXMEM':'4G'","'GHIDRA_HEADLESS_MAXMEM':'5G'")),('removed_fixture_gate',d1.replace("if mode=='actual':","if False:"))]:
 assert text!=expected_driver;negative.append(name)
# All supplied checker code remains data; verify its only added literal block and exact reconstruction above.
c0=(OLD/'check.py').read_text();c1=(P/'check.py').read_text();a0=ast.parse(c0);a1=ast.parse(c1)
assert len([n for n in ast.walk(a1) if isinstance(n,ast.ImportFrom) and n.module=='pathlib'])==1
assert not (P/'build-fixture.py').exists()
assert (P/'synthetic-corpus-x86.macho').read_bytes()==(OLD/'synthetic-corpus-x86.macho').read_bytes()
for mode in ('fixture','actual'):
 v=load(P/(mode+'-config.json'));old=load(OLD/(mode+'-config.json'))
 if mode=='fixture':old['source']['path']=str(P/'synthetic-corpus-x86.macho')
 assert v==old
 assert [(x['address'],x['window_bytes']) for x in v['seeds']]==[('0x23b0',1024),('0x29c0',1024)]
f=load(P/'fixture-config.json');a=load(P/'actual-config.json');assert {k for k in f if f[k]!=a[k]}=={'source','target_sha256'}
assert not (B/'depth-corpus-x86-selected-entry-fixture-r2').exists() and not (B/'depth-corpus-x86-selected-entry-actual-r2').exists()
after=[identity(q) for q in sorted(watch)];assert after==before
result=dict(status='PASS DIAGNOSTIC R2 PREPARATION ONLY',started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=identity(Path(__file__)),manifest=identity(P/'manifest-preparation.json'),payloads=11,tree_files=12,pins=32,current_pin_and_tree_watch=44,preservation_expanded_watch=len(watch),preserved_R1_tree_files=56,all_watched_unchanged=True,before_digest=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),after_digest=hashlib.sha256(json.dumps(after,sort_keys=True).encode()).hexdigest(),reconstructed_files=reconstructed,Java_exception_only=True,compound_guard_byteidentical=True,driver_only_three_paths=True,configs_positive=2,config_difference_fields=['source','target_sha256'],synthetic_copied_byteexact=True,negative_scope_controls=negative,no_supplied_code_functions_main_import_or_tools=True,original_gate='CLOSED')
with R.open('x') as out:json.dump(result,out,indent=2);out.write('\n')
print(json.dumps(dict(evidence=identity(R),watch=len(watch),negative=len(negative))))
