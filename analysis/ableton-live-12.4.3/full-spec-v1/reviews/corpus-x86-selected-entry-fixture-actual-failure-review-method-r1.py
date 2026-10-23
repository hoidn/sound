"""Reviewer-owned stdlib data assertions only; no supplied code invoked."""
from pathlib import Path
import datetime, hashlib, json, struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P=B/'depth-corpus-x86-selected-entry-preparation'
A=B/'depth-corpus-x86-selected-entry-fixture'
O=B/'reviews/corpus-x86-selected-entry-fixture-selected-execution'
R=B/'reviews/corpus-x86-selected-entry-fixture-actual-failure-review-evidence.json'
assert not R.exists()
def load(p):return json.loads(p.read_text())
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def inventory(folder,manifest):
 m=load(folder/manifest);rows=m['files']
 assert {x['path'] for x in rows}=={str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file() and p.name!=manifest}
 for x in rows:
  p=folder/x['path'];assert not p.is_symlink();got=ident(p)
  assert (got['bytes'],got['sha256'])==(x['bytes'],x['sha256'])
 return len(rows)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
counts={str(f.name):inventory(f,m) for f,m in [(P,'manifest-preparation.json'),(A,'manifest.json'),(O,'manifest.json')]}
ib=load(A/'before-map.json');ia=load(A/'after-map.json');ob=load(O/'before-map.json');oa=load(O/'after-map.json')
assert len(ib)==27 and ib==ia['files'] and ia['unchanged']
assert len(ob)==3199 and ob==oa
paths={Path(x['path']) for x in ob+ib}
paths.update(p for f in (A,O) for p in f.rglob('*') if p.is_file())
before=[ident(p) for p in sorted(paths)]
current={x['path']:x for x in before}
assert all(current[x['path']]==x for x in ob+ib)
sel=load(O/'selection.json');s=load(A/'run-status.json');rec=load(O/'receipt.json');proc=load(A/'process.json')
for key in ('preparation','driver','root_preflight','peer_preflight','outer_method'):
 x=sel[key];assert ident(Path(x['path']))==x
assert sel['mode']=='fixture' and sel['original_calls_selected']==0
assert ident(P/'manifest-preparation.json')['sha256']=='194d30df5c0a753fc51f3e066c2707867028df1917f8012904aa030d23f5b6e0'
for name in ('CorpusX86SelectedExport.java','run-selected.py'):assert (A/'method'/name).read_bytes()==(P/name).read_bytes()
raw=(A/'input/Corpus.x86_64').read_bytes();assert raw==(P/'synthetic-corpus-x86.macho').read_bytes()
assert len(raw)==12288 and hashlib.sha256(raw).hexdigest()=='688f2e17c99b0c70aaa55c856cc687c2a28ce54e3dc6909b693f4bd4e0af93d2'
assert struct.unpack_from('<8I',raw)==(0xfeedfacf,0x01000007,3,8,1,152,0,0)
assert raw[0x23b0:0x23b6]==bytes.fromhex('b82a000000c3') and raw[0x29c0:0x29c3]==bytes.fromhex('31c0c3')
assert rec['attempts']==1 and rec['driver_pid']==389456 and rec['driver_exit']==1 and rec['exception'] is None
assert rec['forced_driver_kill'] is False and rec['observed_group_residuals']==[] and rec['unchanged']
assert rec['inner_status']==s==load(O/'driver.stdout.json')
assert s['tool_attempts']==1 and s['returned_pid']==389475 and s['exit_code']==0 and s['error'] is None
assert s['cleanup']==dict(cleaned=True,survivors=[]) and s['automatic_retry'] is False and s['providers_unchanged']
assert proc['driver_pid']==389456 and proc['process_group_id']==389475
assert load(O/'attempt.json')['attempt']==load(A/'attempt.json')['attempt']==1
outerargv=load(O/'attempt.json')['argv'];assert outerargv==load(O/'invocation-before.json')['argv']
assert outerargv[3:]==['fixture',sel['preparation']['sha256'],ident(O/'selection.json')['sha256']]
args=proc['argv'];assert args==load(A/'command.json')==load(A/'attempt.json')['argv']==load(A/'invocation-before.json')['argv']
assert args[args.index('-import')+1]==str(A/'input/Corpus.x86_64')
assert all(x in args for x in ('-readOnly','-deleteProject','-noanalysis'))
assert (O/'driver.stderr').stat().st_size==0
inv=load(A/'invocation-before.json');assert inv['core_limit']==[0,0] and inv['stdin']=='DEVNULL' and inv['overall_timeout_seconds']==180 and inv['per_entry_seconds']==60 and inv['start_new_session']
assert inv['environment']['GHIDRA_HEADLESS_MAXMEM']=='4G'
assert len(s['items'])==2 and [x['address'] for x in s['items']]==['0x23b0','0x29c0']
assert all(x['state']=='invalid' and 'actual-identity.json' in x['error'] for x in s['items'])
assert not (A/'actual-identity.json').exists() and not (A/'functions').exists()
assert not (B/'depth-corpus-x86-selected-entry-actual').exists()
logs=[(A/n).read_text() for n in ('headless.stdout','ghidra.log')]
for text in logs:
 assert 'Effective JDK/4GiB heap/CPU2 identity mismatch' in text
 assert 'CorpusX86SelectedExport.java:43' in text
 assert 'Using Language/Compiler: x86:LE:64:default:gcc' in text
 assert 'Loaded 0 additional files' in text and 'Processing aborted as a result of post-script' in text
 assert str(A/'input/Corpus.x86_64') in text
java=(A/'method/CorpusX86SelectedExport.java').read_text().splitlines()
assert java[42].strip()=='throw new IllegalArgumentException("Effective JDK/4GiB heap/CPU2 identity mismatch");'
assert 'actual-identity.json' in java[69] and 'createDirectory' in java[70]
resources=[json.loads(l) for l in (A/'resources.jsonl').read_text().splitlines()]
assert len(resources)==5
for x in resources:
 assert sum(m['rss_bytes'] for m in x['members'].values())==x['group_rss_bytes']
 assert 0<=x['elapsed_seconds']<180 and x['free_disk_bytes']>=3*1024**3 and x['group_rss_bytes']<=6*1024**3
assert any('389583' in x['members'] for x in resources)
after=[ident(p) for p in sorted(paths)];assert after==before
result=dict(status='PASS RETAINED FAILURE CLASSIFICATION; ORIGINAL GATE CLOSED',started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=ident(Path(__file__)),inventories=counts,manifests=[ident(f/m) for f,m in [(P,'manifest-preparation.json'),(A,'manifest.json'),(O,'manifest.json')]],fixture=ident(A/'input/Corpus.x86_64'),inner_paired_paths=27,outer_paired_paths=3199,reviewer_current_watch=len(before),reviewer_current_unchanged=True,current_map=before,driver_exit=1,headless_launcher_exit=0,java_pid_observed_in_samples=389583,separate_Java_exit_receipt_available=False,resources=dict(samples=len(resources),sampled_max_RSS=max(x['group_rss_bytes'] for x in resources),sampled_min_free_disk=min(x['free_disk_bytes'] for x in resources)),exports=0,actual_identity_record=False,compound_guard_component='UNKNOWN',original_gate='CLOSED',activities=dict(supplied_scripts_tools_import_main=False,original_or_guest_execution=False,new_original_bytes=False))
with R.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=ident(R),watch=len(before),counts=counts)))
