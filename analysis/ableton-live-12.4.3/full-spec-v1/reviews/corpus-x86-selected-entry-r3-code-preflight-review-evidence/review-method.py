"""Independent R3 data reconstruction and one authorized inspected offline checker."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-corpus-x86-selected-entry-preparation-r3';OLD=B/'depth-corpus-x86-selected-entry-preparation-r2'
OUT=B/'reviews/corpus-x86-selected-entry-r3-code-preflight-review-evidence'
assert not OUT.exists();OUT.mkdir()
def load(p):return json.loads(p.read_text())
def identity(p):
 h=hashlib.sha256();size=0
 with p.open('rb') as f:
  for raw in iter(lambda:f.read(1048576),b''):h.update(raw);size+=len(raw)
 return dict(path=str(p),bytes=size,sha256=h.hexdigest())
def verify(folder,manifest):
 rows=load(folder/manifest)['files'];assert {r['path'] for r in rows}=={str(q.relative_to(folder)) for q in folder.rglob('*') if q.is_file() and q!=folder/manifest}
 for row in rows:
  q=folder/row['path'];got=identity(q);assert not q.is_symlink() and (got['bytes'],got['sha256'])==(row['bytes'],row['sha256'])
 return {folder/r['path'] for r in rows}|{folder/manifest}
started=datetime.datetime.now(datetime.timezone.utc).isoformat();pins=load(P/'inputs.json')['pins'];assert len(pins)==53
paths={Path(x['path']) for x in pins}|verify(P,'manifest-preparation.json');assert len(paths)==65
oldcount=0
for rev in ('','-r2'):
 for stem,m in [('depth-corpus-x86-selected-entry-preparation','manifest-preparation.json'),('depth-corpus-x86-selected-entry-fixture','manifest.json'),('reviews/corpus-x86-selected-entry-fixture','manifest.json')]:
  folder=B/(stem+rev+('-selected-execution' if stem.startswith('reviews/') else ''))
  old=verify(folder,m);oldcount+=len(old);paths|=old
before=[identity(p) for p in sorted(paths)]
for row in pins:assert identity(Path(row['path']))==row
assert identity(P/'manifest-preparation.json')['sha256']=='5598da01bb9b8e438abed47e7402efa84d13ccaa399fefa2ee91a03292fe0212'
assert (P/'CorpusX86SelectedExport.java').read_bytes()==(OLD/'CorpusX86SelectedExport.java').read_bytes()
text=(OLD/'run-selected.py').read_text()
changes=[("PRE=BASE/'depth-corpus-x86-selected-entry-preparation-r2'","PRE=BASE/'depth-corpus-x86-selected-entry-preparation-r3'"),("return BASE/('depth-corpus-x86-selected-entry-'+mode+'-r2')","return BASE/('depth-corpus-x86-selected-entry-'+mode+'-r3')"),("('corpus-x86-selected-entry-'+mode+'-r2-selected-execution')","('corpus-x86-selected-entry-'+mode+'-r3-selected-execution')"),("'GHIDRA_HEADLESS_JAVA_OPTIONS':'',","'GHIDRA_HEADLESS_JAVA_OPTIONS':'-Dcpu.core.override=2',")]
for old,new in changes:assert text.count(old)==1;text=text.replace(old,new)
assert text==(P/'run-selected.py').read_text()
reconstructed=[]
for f in load(P/'source-delta.json')['files']:
 assert identity(Path(f['before']['path']))==f['before'] and identity(Path(f['after']['path']))==f['after']
 lines=Path(f['before']['path']).read_text().splitlines(keepends=True)
 for e in reversed(f['edits']):
  a,z=e['old_line_start_zero'],e['old_line_end_exclusive'];assert hashlib.sha256(''.join(lines[a:z]).encode()).hexdigest()==e['old_text_sha256'];lines[a:z]=e['replacement'].splitlines(keepends=True)
 assert ''.join(lines)==Path(f['after']['path']).read_text();reconstructed.append(Path(f['after']['path']).name)
q=B/'queries/ghidra-default-pool-launch-options-source-diagnosis-2026-10-20.json';diag=load(q)
for span in diag['critical_spans']:assert len(span['text'].encode())==span['bytes'] and hashlib.sha256(span['text'].encode()).hexdigest()==span['sha256']
assert len(diag['critical_spans'])==7
assert (P/'synthetic-corpus-x86.macho').read_bytes()==(OLD/'synthetic-corpus-x86.macho').read_bytes()
assert not (B/'depth-corpus-x86-selected-entry-fixture-r3').exists() and not (B/'depth-corpus-x86-selected-entry-actual-r3').exists()
# One permitted read-only checker. Fully inspected: five new pure config/scope functions only;
# no driver main, source_bytes, supervisor, launcher, Java, decoder or original calls.
argv=[sys.executable,'-B',str(P/'check.py'),'--check']
proc=subprocess.run(argv,cwd=B,stdin=subprocess.DEVNULL,capture_output=True,timeout=30)
(OUT/'stdout.json').write_bytes(proc.stdout);(OUT/'stderr').write_bytes(proc.stderr)
assert proc.returncode==0 and not proc.stderr
check=json.loads(proc.stdout);assert check['valid_configs']==2 and check['valid_commands']==1 and len(check['unsafe_rejections'])==15 and check['pins']==53 and check['watched']==65 and check['unchanged']
after=[identity(p) for p in sorted(paths)];assert after==before
result=dict(status='PASS R3 CANDIDATE PREPARATION ONLY',started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=identity(Path(__file__)),preparation=identity(P/'manifest-preparation.json'),pins=53,current_watch=65,expanded_watch=len(paths),all_watched_unchanged=True,preserved_R1_R2_tree_files=oldcount,watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),Java_byteexact_R2=True,driver_only_four_literal_changes=True,reconstructed_files=reconstructed,retained_source_diagnosis_spans_verified=7,checker=dict(argv=argv,exit=proc.returncode,stdout=identity(OUT/'stdout.json'),stderr=identity(OUT/'stderr'),result=check),Ghidra_Java_native_decoder_original_import=False,original_gate='CLOSED')
with (OUT/'evidence.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=identity(OUT/'evidence.json'),watch=len(paths),history=oldcount)))
