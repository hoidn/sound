"""Independent stdlib DATA verification only; imports no supplied method or target."""
from pathlib import Path
import datetime, hashlib, json, struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P=B/'depth-corpus-x86-selected-entry-preparation-r5'
D=B/'depth-corpus-x86-selected-entry-fixture-r5'
H=B/'reviews/corpus-x86-selected-entry-fixture-r5-selected-execution'
OUT=B/'reviews/corpus-x86-selected-entry-fixture-r5-actual-review-evidence.json'
def j(p): return json.loads(p.read_text())
def identity(p):
 h=hashlib.sha256(); n=0
 with p.open('rb') as f:
  for data in iter(lambda:f.read(1048576),b''): h.update(data); n+=len(data)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def equal(row): assert identity(Path(row['path']))==row, row['path']
def inventory(root,name,number):
 m=j(root/name); rows=m['files']; assert len(rows)==number
 assert len({r['path'] for r in rows})==number
 assert {r['path'] for r in rows}=={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p!=root/name}
 for r in rows:
  assert Path(r['path']).parts[0]!='..' and not Path(r['path']).is_absolute()
  got=identity(root/r['path']); assert (got['bytes'],got['sha256'])==(r['bytes'],r['sha256'])
 return m
selection=j(H/'selection.json'); ib=j(D/'before-map.json'); ia=j(D/'after-map.json'); ob=j(H/'before-map.json'); oa=j(H/'after-map.json')
assert len(ib)==110 and len(ob)==3599 and ia==dict(files=ib,unchanged=True) and ob==oa
assert len({r['path'] for r in ib})==110 and len({r['path'] for r in ob})==3599
paths={Path(r['path']) for r in ib+ob}
for root in (P,D,H): paths.update(p for p in root.rglob('*') if p.is_file())
paths.update((Path(__file__).resolve(),B/'reviews/corpus-x86-selected-entry-fixture-r5-root-assessment.json'))
before=[identity(p) for p in sorted(paths)]
for r in ib+ob: equal(r)
pm=inventory(P,'manifest-preparation.json',13); dm=inventory(D,'manifest.json',38); hm=inventory(H,'manifest.json',10)
assert identity(P/'manifest-preparation.json')['sha256']=='7a1f153c866e4dbba656594b803d6261dc35d08bb4ec9f0a15ca86f0a0a423f4'
assert identity(D/'manifest.json')['sha256']=='983e4bab0e7d38040c96cbe3380d15d476dfc98f375a99c5de2a871eb464afd1'
assert identity(H/'manifest.json')['sha256']=='9dc6bfd4b7ac74f717d2d0959ed442af477079c0cee8cc241462ee7243e2f795'
pins=j(P/'inputs.json')['pins']; assert len(pins)==95
for r in pins: equal(r)
for k in ('preparation','driver','root_preflight','peer_preflight','wrapper','wrapper_parent'): equal(selection[k])
parent=Path(selection['wrapper_parent']['path']).read_text()
for old,new in selection['literal_operations']:
 assert old in parent
 parent=parent.replace(old,new)
assert len(selection['literal_operations'])==4 and parent==(H/'execute-selected-once.py').read_text()
for n in ('CorpusX86SelectedExport.java','run-selected.py'): assert (P/n).read_bytes()==(D/'method'/n).read_bytes()
# Reconstruct the entire OWNED fixture independently; no supplied builder import/run.
x=bytearray(65536)
x[:32]=struct.pack('<8I',0xfeedfacf,0x1000007,3,8,1,152,0,0)
x[32:104]=struct.pack('<II16sQQQQiiII',25,152,b'__TEXT',0,65536,0,65536,5,5,1,0)
x[104:184]=struct.pack('<16s16sQQIIIIIIII',b'__text',b'__TEXT',8192,57344,8192,4,0,0,0x80000400,0,0,0)
x[8192:]=b'\xcc'*57344
x[0x23b0:0x23b6]=bytes.fromhex('b82a000000c3'); x[0xd090:0xd093]=bytes.fromhex('31c0c3')
assert bytes(x)==(P/'synthetic-corpus-x86.macho').read_bytes()==(D/'input/Corpus.x86_64').read_bytes()
assert hashlib.sha256(x).hexdigest()=='1c514938c8b4b28ee47c0f419acb247e63a65ee988d57b5f195957b3aae4c9de'
config=j(P/'fixture-config.json'); run=j(D/'run.json'); fixed={k:run[k] for k in config}; assert fixed==config
assert [s['address'] for s in run['seeds']]==['0x23b0','0xd090']
assert all(s['window_bytes']==4096 for s in run['seeds'])
assert run['preparation_sha256']==selection['preparation']['sha256']
assert run['method_sha256']==identity(P/'CorpusX86SelectedExport.java')['sha256']
assert run['target']==str(D/'input/Corpus.x86_64')
assert run['auto_analysis'] is False and run['incremental_code_analysis'] is False
for seed,size,asm,code in zip(run['seeds'],(6,3),('0x23b0: MOV EAX,0x2a\n0x23b5: RET\n','0xd090: XOR EAX,EAX\n0xd092: RET\n'),('undefined8 FUN_000023b0(void)\n\n{\n  return 0x2a;\n}\n','undefined8 FUN_0000d090(void)\n\n{\n  return 0;\n}\n')):
 a=int(seed['address'],16); q=D/'functions'/seed['address']; m=j(q/'metadata.json')
 assert m['address']==seed['address'] and m['seed']==seed and m['state']=='exported'
 assert m['body_bytes']==size and m['instruction_count']==2 and m['body_ranges']==[dict(start=hex(a),end=hex(a+size-1))]
 assert int(m['window_end'],16)==a+4095 and a+4096<=len(x)
 assert m['warnings']==[] and m['partial_code'] is False and m['completed'] is True
 assert all(m[k] is False for k in ('timed_out','cancelled','failed_to_start','auto_analysis','incremental_code_analysis'))
 assert m['method_sha256']==run['method_sha256'] and m['target_sha256']==config['target_sha256']
 assert (q/'assembly.txt').read_text()==asm and (q/'pseudocode.c').read_text()==code
status=j(D/'run-status.json'); receipt=j(H/'receipt.json'); actual=j(D/'actual-identity.json')
assert receipt['inner_status']==status==j(H/'driver.stdout.json')
assert receipt['outer_pid']==406483 and receipt['driver_pid']==406485 and receipt['driver_exit']==0 and receipt['attempts']==1
assert receipt['exception'] is None and receipt['forced_driver_kill'] is False and receipt['unchanged'] is True and receipt['observed_group_residuals']==[]
assert status['mode']=='fixture' and status['tool_attempts']==1 and status['returned_pid']==406486 and status['exit_code']==0 and status['error'] is None
assert status['guest_execution'] is False and status['automatic_retry'] is False and status['providers_unchanged'] is True
assert status['cleanup']==dict(cleaned=True,survivors=[])
assert j(H/'driver-pid.json')['pid']==406485 and j(D/'process.json')['driver_pid']==406485 and j(D/'process.json')['process_group_id']==406486
assert actual['pid']==406591 and actual['executable_sha256']==config['target_sha256']
for k,v in dict(language='x86:LE:64:default',compiler='gcc',ghidra_version='12.1.4',java_version='21.0.12.1',max_heap=4294967296,processors=2,default_pool=2,auto_analysis=False,whole_program_available_to_decompiler=True).items(): assert actual[k]==v
assert int(actual['image_base'],16)==0 and actual['java_home']==run['jdk'] and actual['user_home']==run['user_home'] and actual['tmp']==run['tmp']
assert actual['jvm_arguments'][-1]=='-Dcpu.core.override=2'
cmd=j(D/'command.json'); inv=j(D/'invocation-before.json'); oinv=j(H/'invocation-before.json')
assert cmd==inv['argv']==j(D/'attempt.json')['argv']==j(D/'process.json')['argv']
assert cmd[cmd.index('-import')+1]==str(D/'input/Corpus.x86_64') and all(cmd.count(flag)==1 for flag in ('-noanalysis','-readOnly','-deleteProject'))
assert inv['core_limit']==[0,0] and inv['stdin']=='DEVNULL' and inv['start_new_session'] is True
assert inv['overall_timeout_seconds']==180 and inv['per_entry_seconds']==60 and inv['guest_execution'] is False
assert inv['environment']['GHIDRA_HEADLESS_JAVA_OPTIONS']=='-Dcpu.core.override=2' and inv['environment']['GHIDRA_HEADLESS_MAXMEM']=='4G'
assert oinv['argv']==j(H/'attempt.json')['argv'] and oinv['argv'][1]=='-B' and oinv['argv'][3]=='fixture'
assert oinv['argv'][-1]==identity(H/'selection.json')['sha256'] and oinv['argv'][-2]==selection['preparation']['sha256']
assert oinv['environment']==dict(PATH='/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8')
assert oinv['inherited_core']==[0,0] and oinv['stdin']=='DEVNULL' and oinv['timeout_seconds']==240 and oinv['termination_grace_seconds']==25
assert oinv['original_image_mode'] is False and oinv['automatic_retry'] is False and (H/'driver.stderr').stat().st_size==0
samples=[json.loads(s) for s in (D/'resources.jsonl').read_text().splitlines()]; assert len(samples)==5
for s in samples:
 assert s['group_rss_bytes']==sum(m['rss_bytes'] for m in s['members'].values())
 assert s['group_rss_bytes']<=6*1024**3 and s['free_disk_bytes']>=3*1024**3 and 0<=s['elapsed_seconds']<180
assert any(str(actual['pid']) in s['members'] for s in samples)
assert [s['elapsed_seconds'] for s in samples]==sorted(s['elapsed_seconds'] for s in samples)
assert not (B/'depth-corpus-x86-selected-entry-actual-r5').exists()
after=[identity(p) for p in sorted(paths)]; assert before==after
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=identity(Path(__file__).resolve()),status='PASS',inventories=dict(preparation=13,actual=38,outer=10),input_pins=95,paired_maps=dict(inner=110,outer=3599),fresh_watched_paths=len(paths),fresh_unchanged=before==after,watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest(),map_providers=[identity(p) for p in (D/'before-map.json',D/'after-map.json',H/'before-map.json',H/'after-map.json')],extra_watched=[r for r in before if r['path'] not in {row['path'] for row in ob}],fixture_reconstruction=dict(bytes=len(x),sha256=hashlib.sha256(x).hexdigest(),known_bytes={'0x23b0':x[0x23b0:0x23b6].hex(),'0xd090':x[0xd090:0xd093].hex()}),resources=dict(samples=5,max_sampled_rss=max(s['group_rss_bytes'] for s in samples),min_sampled_free_disk=min(s['free_disk_bytes'] for s in samples)),execution='New reviewer stdlib DATA checks only; no supplied code import/run, no Java/Ghidra/decoder/original execution.')
with OUT.open('x') as f: json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('extra_watched','map_providers')},indent=2))
