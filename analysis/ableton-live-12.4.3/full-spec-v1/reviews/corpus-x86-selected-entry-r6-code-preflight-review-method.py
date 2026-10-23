"""Independent stdlib metadata/delta checks; current readonly checker only."""
from pathlib import Path
import ast,datetime,hashlib,json,struct,subprocess,sys
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-corpus-x86-selected-entry-preparation-r6';O=B/'depth-corpus-x86-selected-entry-preparation-r5'
OUT=B/'reviews/corpus-x86-selected-entry-r6-code-preflight-review-evidence.json'
def j(p):return json.loads(p.read_text())
def identity(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for raw in iter(lambda:f.read(1048576),b''):h.update(raw);n+=len(raw)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
inputs=j(P/'inputs.json');pins=inputs['pins'];assert len(pins)==201 and len({r['path'] for r in pins})==201
paths={Path(r['path']) for r in pins}|{p for p in P.iterdir() if p.is_file()}|{Path(__file__).resolve()};before=[identity(p) for p in sorted(paths)]
assert identity(P/'manifest-preparation.json')['sha256']=='45adfe08f027cd47ed32e8c4c59c3ad9d9289912f81fa15f7fa0ea921db6b920'
for r in pins:assert identity(Path(r['path']))==r
manifest=j(P/'manifest-preparation.json');assert len(manifest['files'])==13 and {r['path'] for r in manifest['files']}=={p.name for p in P.iterdir() if p.name!='manifest-preparation.json'}
for r in manifest['files']:
 v=identity(P/r['path']);assert (v['bytes'],v['sha256'])==(r['bytes'],r['sha256'])
delta=j(P/'source-delta.json');assert len(delta['files'])==4 and len(delta['parent_files_exact'])==14
for row in delta['parent_files_exact']:assert identity(Path(row['path']))==row
for row in delta['files']:
 assert identity(Path(row['before']['path']))==row['before'] and identity(Path(row['after']['path']))==row['after']
 lines=Path(row['before']['path']).read_text().splitlines(True)
 for e in reversed(row['edits']):
  a,z=e['old_line_start_zero'],e['old_line_end_exclusive'];assert hashlib.sha256(''.join(lines[a:z]).encode()).hexdigest()==e['old_text_sha256'];lines[a:z]=e['replacement'].splitlines(True)
 assert ''.join(lines)==Path(row['after']['path']).read_text()
java=(O/'CorpusX86SelectedExport.java').read_text();driver=(O/'run-selected.py').read_text()
assert java.count('"0xd090"')==1 and java.count('0xd090L')==1
assert java.replace('"0xd090"','"0x85e0"').replace('0xd090L','0x85e0L')==(P/'CorpusX86SelectedExport.java').read_text()
assert len(delta['literal_operations']['driver'])==6
for old,new,n in delta['literal_operations']['driver']:
 assert driver.count(old)==n==1;driver=driver.replace(old,new)
assert driver==(P/'run-selected.py').read_text()
old_fns={n.name:ast.dump(n,include_attributes=False) for n in ast.parse((O/'run-selected.py').read_text()).body if isinstance(n,ast.FunctionDef)}
new_fns={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(driver).body if isinstance(n,ast.FunctionDef)}
assert {k:v for k,v in old_fns.items() if k not in ('destination','selection_path')}=={k:v for k,v in new_fns.items() if k not in ('destination','selection_path')}
# Whole owned fixture independently reconstructed; no supplied builder executed/imported.
x=bytearray(65536);x[:32]=struct.pack('<8I',0xfeedfacf,0x1000007,3,8,1,152,0,0)
x[32:104]=struct.pack('<II16sQQQQiiII',25,152,b'__TEXT',0,65536,0,65536,5,5,1,0)
x[104:184]=struct.pack('<16s16sQQIIIIIIII',b'__text',b'__TEXT',8192,57344,8192,4,0,0,0x80000400,0,0,0)
x[8192:]=b'\xcc'*57344;x[0x23b0:0x23b6]=bytes.fromhex('b82a000000c3');x[0x85e0:0x85e3]=bytes.fromhex('31c0c3')
assert bytes(x)==(P/'synthetic-corpus-x86.macho').read_bytes() and hashlib.sha256(x).hexdigest()=='7b8b11955de655b259787b79c80cd61a19c851ec2fcb137d8aa3b276e0783719'
receipt=j(P/'fixture-build-receipt.json');assert receipt['pid']==755372 and receipt['exit_code']==0 and receipt['owned_builder_attempts']==1 and receipt['stderr_utf8']==''
assert receipt['builder_sha256']==identity(P/'build-fixture.py')['sha256']
assert json.loads(receipt['stdout_utf8'])==identity(P/'synthetic-corpus-x86.macho')|dict(guest_execution=False)
checks=[]
for flag,expected in [('--check',0),('--write',1)]:
 a=[sys.executable,'-B',str(P/'check.py'),flag];v=subprocess.run(a,capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=20);assert v.returncode==expected
 checks.append(dict(argv=a,exit=v.returncode,stdout=v.stdout,stderr=v.stderr))
r=json.loads(checks[0]['stdout']);assert r['valid_configs']==2 and r['valid_commands']==1 and len(r['unsafe_rejections'])==17 and r['pins']==201 and r['watched']==215 and r['unchanged'] is True
assert not (B/'depth-corpus-x86-selected-entry-fixture-r6').exists() and not (B/'depth-corpus-x86-selected-entry-actual-r6').exists()
after=[identity(p) for p in sorted(paths)];assert before==after
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=identity(Path(__file__).resolve()),status='PASS BOUNDED PREPARATION ONLY',preparation=identity(P/'manifest-preparation.json'),payloads=13,pins=201,watch_count=len(paths),before_after_unchanged=True,watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest(),pin_provider=identity(P/'inputs.json'),additional_watched=[r for r in before if r['path'] not in {a['path'] for a in pins}],exact_source_deltas=dict(Java=2,driver=6,delta_file_reconstructions=4,parent_files=14,all_other_driver_function_ASTs_equal=True),fixture_reconstructed=True,checks=checks,tool_or_original_execution=False)
with OUT.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('additional_watched','checks')},indent=2))
