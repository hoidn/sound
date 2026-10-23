"""Independent stdlib DATA audit; never import or execute any supplied method."""
from pathlib import Path
import datetime,hashlib,json,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-corpus-x86-selected-entry-preparation-r6';D=B/'depth-corpus-x86-selected-entry-fixture-r6';H=B/'reviews/corpus-x86-selected-entry-fixture-r6-selected-execution'
OUT=B/'reviews/corpus-x86-selected-entry-fixture-r6-actual-review-evidence.json'
def j(p):return json.loads(p.read_text())
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for v in iter(lambda:f.read(1048576),b''):h.update(v);n+=len(v)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def inv(root,name,n):
 m=j(root/name);rows=m['files'];assert len(rows)==n and len({r['path'] for r in rows})==n
 assert {r['path'] for r in rows}=={str(q.relative_to(root)) for q in root.rglob('*') if q.is_file() and q!=root/name}
 for r in rows:
  assert not Path(r['path']).is_absolute() and '..' not in Path(r['path']).parts
  v=ident(root/r['path']);assert (v['bytes'],v['sha256'])==(r['bytes'],r['sha256'])
 return m
ib=j(D/'before-map.json');ia=j(D/'after-map.json');ob=j(H/'before-map.json');oa=j(H/'after-map.json')
assert len(ib)==216 and len(ob)==2388 and ia==dict(files=ib,unchanged=True) and ob==oa
assert len({r['path'] for r in ib})==216 and len({r['path'] for r in ob})==2388
paths={Path(r['path']) for r in ib+ob}|{Path(__file__).resolve(),B/'reviews/corpus-x86-selected-entry-fixture-r6-root-assessment.json'}
for folder in (P,D,H):paths.update(q for q in folder.rglob('*') if q.is_file())
before=[ident(q) for q in sorted(paths)]
for r in ib+ob:assert ident(Path(r['path']))==r
assert ident(P/'manifest-preparation.json')['sha256']=='45adfe08f027cd47ed32e8c4c59c3ad9d9289912f81fa15f7fa0ea921db6b920'
assert ident(D/'manifest.json')['sha256']=='87e7762a739b5740820e50978ecb2e1c31b7f0b10dd2e678212153608ebb33cb'
assert ident(H/'manifest.json')['sha256']=='4425c6ff2a7628a874068e27f6550f7ca6d6aa30c5e6c9e3bf5eae5f3a488b51'
inv(P,'manifest-preparation.json',13);inv(D,'manifest.json',38);inv(H,'manifest.json',10)
pins=j(P/'inputs.json')['pins'];assert len(pins)==201
for r in pins:assert ident(Path(r['path']))==r
s=j(H/'selection.json');assert s['mode']=='fixture'
for k in ('preparation','driver','root_preflight','peer_preflight','wrapper','wrapper_parent'):assert ident(Path(s[k]['path']))==s[k]
parent=Path(s['wrapper_parent']['path']).read_text();assert len(s['literal_operations'])==5
for old,new in s['literal_operations']:
 assert parent.count(old)==1;parent=parent.replace(old,new)
assert parent==(H/'execute-selected-once.py').read_text()
assert "for folder in [ROOT / 'handoff', PRE]:" in parent and "BASE.glob('depth-*')" not in parent
for n in ('CorpusX86SelectedExport.java','run-selected.py'):assert (P/n).read_bytes()==(D/'method'/n).read_bytes()
# Entire OWNED fixture reconstructed from declared geometry/known instructions.
x=bytearray(65536);x[:32]=struct.pack('<8I',0xfeedfacf,0x1000007,3,8,1,152,0,0)
x[32:104]=struct.pack('<II16sQQQQiiII',25,152,b'__TEXT',0,65536,0,65536,5,5,1,0)
x[104:184]=struct.pack('<16s16sQQIIIIIIII',b'__text',b'__TEXT',8192,57344,8192,4,0,0,0x80000400,0,0,0)
x[8192:]=b'\xcc'*57344;x[0x23b0:0x23b6]=bytes.fromhex('b82a000000c3');x[0x85e0:0x85e3]=bytes.fromhex('31c0c3')
assert bytes(x)==(P/'synthetic-corpus-x86.macho').read_bytes()==(D/'input/Corpus.x86_64').read_bytes()
config=j(P/'fixture-config.json');run=j(D/'run.json');assert {k:run[k] for k in config}==config
assert run['target']==str(D/'input/Corpus.x86_64') and run['preparation_sha256']==s['preparation']['sha256'] and run['method_sha256']==ident(P/'CorpusX86SelectedExport.java')['sha256']
for a,size,asm,code in [(0x23b0,6,'MOV EAX,0x2a','0x2a'),(0x85e0,3,'XOR EAX,EAX','0')]:
 q=D/'functions'/hex(a);m=j(q/'metadata.json');seed=next(v for v in run['seeds'] if v['address']==hex(a))
 assert m['seed']==seed and seed['window_bytes']==4096 and m['state']=='exported' and m['body_bytes']==size and m['instruction_count']==2
 assert m['body_ranges']==[dict(start=hex(a),end=hex(a+size-1))] and int(m['window_end'],16)==a+4095 and a+4096<=65536
 assert m['warnings']==[] and m['completed'] is True and all(m[k] is False for k in ('partial_code','timed_out','cancelled','failed_to_start','auto_analysis','incremental_code_analysis'))
 assert m['method_sha256']==run['method_sha256'] and m['target_sha256']==run['target_sha256']
 assert (q/'assembly.txt').read_text()==f'{hex(a)}: {asm}\n{hex(a+size-1)}: RET\n'
 assert (q/'pseudocode.c').read_text()==f'\nundefined8 FUN_{a:08x}(void)\n\n{{\n  return {code};\n}}\n\n'
status=j(D/'run-status.json');receipt=j(H/'receipt.json');identity=j(D/'actual-identity.json')
assert receipt['inner_status']==status==j(H/'driver.stdout.json') and receipt['attempts']==1 and receipt['outer_pid']==771623 and receipt['driver_pid']==771872 and receipt['driver_exit']==0
assert receipt['exception'] is None and receipt['forced_driver_kill'] is False and receipt['observed_group_residuals']==[] and receipt['unchanged'] is True
assert status['mode']=='fixture' and status['tool_attempts']==1 and status['returned_pid']==771882 and status['exit_code']==0 and status['error'] is None and status['guest_execution'] is False and status['automatic_retry'] is False
assert status['cleanup']==dict(cleaned=True,survivors=[]) and status['providers_unchanged'] is True
assert identity['pid']==771988 and identity['executable_sha256']==run['target_sha256'] and identity['max_heap']==4294967296 and identity['processors']==2 and identity['default_pool']==2
assert identity['language']=='x86:LE:64:default' and identity['compiler']=='gcc' and identity['java_version']=='21.0.12.1' and identity['ghidra_version']=='12.1.4' and int(identity['image_base'],16)==0
assert identity['java_home']==run['jdk'] and identity['user_home']==run['user_home'] and identity['tmp']==run['tmp'] and identity['jvm_arguments'][-1]=='-Dcpu.core.override=2'
cmd=j(D/'command.json');i=j(D/'invocation-before.json');oi=j(H/'invocation-before.json')
assert cmd==i['argv']==j(D/'attempt.json')['argv']==j(D/'process.json')['argv']
assert cmd[cmd.index('-import')+1]==str(D/'input/Corpus.x86_64') and all(cmd.count(f)==1 for f in ('-readOnly','-deleteProject','-noanalysis'))
assert j(D/'process.json')['driver_pid']==771872 and j(D/'process.json')['process_group_id']==771882 and j(H/'driver-pid.json')['pid']==771872
assert oi['argv']==j(H/'attempt.json')['argv'] and oi['argv'][3]=='fixture' and oi['argv'][-1]==ident(H/'selection.json')['sha256']
assert oi['original_image_mode'] is False and oi['inherited_core']==[0,0] and oi['stdin']=='DEVNULL' and oi['timeout_seconds']==240 and oi['termination_grace_seconds']==25
assert oi['environment']==dict(PATH='/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8')
assert i['core_limit']==[0,0] and i['stdin']=='DEVNULL' and i['overall_timeout_seconds']==180 and i['per_entry_seconds']==60 and i['guest_execution'] is False
assert i['environment']['GHIDRA_HEADLESS_JAVA_OPTIONS']=='-Dcpu.core.override=2' and i['environment']['GHIDRA_HEADLESS_MAXMEM']=='4G'
samples=[json.loads(v) for v in (D/'resources.jsonl').read_text().splitlines()];assert len(samples)==6
for v in samples:
 assert v['group_rss_bytes']==sum(m['rss_bytes'] for m in v['members'].values()) and v['group_rss_bytes']<=6*1024**3 and v['free_disk_bytes']>=3*1024**3 and 0<=v['elapsed_seconds']<180
assert any('771988' in v['members'] for v in samples) and (H/'driver.stderr').stat().st_size==0
assert not (B/'depth-corpus-x86-selected-entry-actual-r6').exists()
after=[ident(q) for q in sorted(paths)];assert before==after
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=ident(Path(__file__).resolve()),status='PASS OWN FIXTURE ACTUAL ONLY',inventory_payloads=dict(preparation=13,actual=38,outer=10),pins=201,paired_maps=dict(inner=216,outer=2388),fresh_watch=len(paths),unchanged=True,watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest(),map_pins=[ident(q) for q in (D/'before-map.json',D/'after-map.json',H/'before-map.json',H/'after-map.json')],additional_watched=[v for v in before if v['path'] not in {r['path'] for r in ob}],fixture_reconstructed=True,outer_literal_operations=5,resource_samples=6,max_sampled_RSS=max(v['group_rss_bytes'] for v in samples),minimum_sampled_free_disk=min(v['free_disk_bytes'] for v in samples),tool_original_or_guest_execution=False)
with OUT.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('additional_watched','map_pins')},indent=2))
