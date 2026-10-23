"""Independent stdlib static-export artifact audit; no tools or target execution."""
from pathlib import Path
import datetime,hashlib,json,re
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-corpus-x86-selected-entry-preparation-r6';D=B/'depth-corpus-x86-selected-entry-actual-r6';H=B/'reviews/corpus-x86-selected-entry-actual-r6-selected-execution'
OUT=B/'reviews/corpus-x86-selected-entry-original-r6-actual-review-evidence.json'
def j(p):return json.loads(p.read_text())
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for data in iter(lambda:f.read(1048576),b''):h.update(data);n+=len(data)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def inv(root,name,n):
 m=j(root/name);assert len(m['files'])==n and len({r['path'] for r in m['files']})==n
 assert {r['path'] for r in m['files']}=={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p!=root/name}
 for r in m['files']:
  assert not Path(r['path']).is_absolute() and '..' not in Path(r['path']).parts
  v=ident(root/r['path']);assert (v['bytes'],v['sha256'])==(r['bytes'],r['sha256'])
 return m
s=j(H/'selection.json');F=Path(s['fixture_manifest']['path']).parent;FH=Path(s['fixture_outer']['path']).parent
ib=j(D/'before-map.json');ia=j(D/'after-map.json');ob=j(H/'before-map.json');oa=j(H/'after-map.json')
assert len(ib)==216 and len(ob)==2388 and ia==dict(files=ib,unchanged=True) and ob==oa
paths={Path(r['path']) for r in ib+ob}|{Path(__file__).resolve(),B/'reviews/corpus-x86-selected-entry-original-r6-root-assessment.json',Path(s['fixture_actual_review']['path'])}
for root in (P,D,H,F,FH):paths.update(p for p in root.rglob('*') if p.is_file())
before=[ident(p) for p in sorted(paths)]
for row in ib+ob:assert ident(Path(row['path']))==row
pins=j(P/'inputs.json')['pins'];assert len(pins)==201
for row in pins:assert ident(Path(row['path']))==row
inv(P,'manifest-preparation.json',13);inv(D,'manifest.json',38);inv(H,'manifest.json',10);inv(F,'manifest.json',38);inv(FH,'manifest.json',10)
assert ident(D/'manifest.json')['sha256']=='8167afb093c848f4a89e6ad5470b426d80dec508c2094249a7b77f9420ebc76a'
assert ident(H/'manifest.json')['sha256']=='44c932747d2a997ca78ffeec6aa733e44ac5cbc194b32494f2aad393e2dd4aa4'
for k in ('preparation','driver','root_preflight','peer_preflight','fixture_manifest','fixture_actual_review','fixture_outer','wrapper','wrapper_parent'):assert ident(Path(s[k]['path']))==s[k]
assert s['mode']=='actual' and s['original_calls']==0 and s['fixture_independently_approved'] is True
assert j(Path(s['fixture_actual_review']['path']))['fixture_actual_review']['approved'] is True
parent=Path(s['wrapper_parent']['path']).read_text();assert len(s['literal_operations'])==5
for old,new in s['literal_operations']:assert parent.count(old)==1;parent=parent.replace(old,new)
assert parent==(H/'execute-selected-once.py').read_text()
for n in ('CorpusX86SelectedExport.java','run-selected.py'):assert (P/n).read_bytes()==(D/'method'/n).read_bytes()
cfg=j(P/'actual-config.json');run=j(D/'run.json');assert {k:run[k] for k in cfg}==cfg
assert run['preparation_sha256']==s['preparation']['sha256'] and run['method_sha256']==ident(P/'CorpusX86SelectedExport.java')['sha256']
assert run['target']==str(D/'input/Corpus.x86_64') and ident(D/'input/Corpus.x86_64')['sha256']==run['target_sha256']=='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
assert (D/'input/Corpus.x86_64').stat().st_size==250352 and run['source']['offset']==16384 and run['source']['length']==250352
outputs=[]
for a,size,count,state in [(0x23b0,110,32,'exported'),(0x85e0,1774,451,'exported-with-warnings')]:
 q=D/'functions'/hex(a);m=j(q/'metadata.json');text=(q/'pseudocode.c').read_text();listing=(q/'assembly.txt').read_text().splitlines()
 assert m['state']==state and m['body_bytes']==size and m['instruction_count']==count and len(listing)==count
 assert m['completed'] is True and all(m[k] is False for k in ('partial_code','timed_out','cancelled','failed_to_start','auto_analysis','incremental_code_analysis'))
 assert m['target_sha256']==run['target_sha256'] and m['method_sha256']==run['method_sha256'] and int(m['window_end'],16)==a+4095
 ranges=[(int(v['start'],16),int(v['end'],16)) for v in m['body_ranges']];assert sum(z-lo+1 for lo,z in ranges)==size and all(a<=lo<=z<a+4095 for lo,z in ranges)
 addresses=[]
 for line in listing:
  match=re.fullmatch(r'0x([0-9a-f]+): (.+)',line);assert match
  addr=int(match[1],16);assert any(lo<=addr<=z for lo,z in ranges);addresses.append(addr)
 assert addresses==sorted(set(addresses)) and addresses[0]==a
 assert [line.strip() for line in text.splitlines() if 'WARNING' in line.upper()]==m['warnings']
 outputs.append(dict(address=hex(a),body_bytes=size,listing_rows=count,C_lines=len(text.splitlines()),warnings=m['warnings'],body_ranges=m['body_ranges']))
assert len(outputs[1]['warnings'])==4 and outputs[0]['warnings']==[]
status=j(D/'run-status.json');receipt=j(H/'receipt.json');identity=j(D/'actual-identity.json')
assert receipt['inner_status']==status==j(H/'driver.stdout.json') and receipt['outer_pid']==783362 and receipt['driver_pid']==783370 and receipt['driver_exit']==0 and receipt['attempts']==1
assert receipt['exception'] is None and receipt['forced_driver_kill'] is False and receipt['observed_group_residuals']==[] and receipt['unchanged'] is True
assert status['returned_pid']==783379 and status['tool_attempts']==1 and status['exit_code']==0 and status['error'] is None and status['mode']=='actual' and status['guest_execution'] is False and status['automatic_retry'] is False
assert status['cleanup']==dict(cleaned=True,survivors=[]) and status['providers_unchanged'] is True
assert [v['state'] for v in status['items']]==['exported','exported-with-warnings']
assert identity['pid']==783487 and identity['executable_sha256']==run['target_sha256'] and identity['max_heap']==4294967296 and identity['processors']==2 and identity['default_pool']==2
assert identity['language']=='x86:LE:64:default' and identity['compiler']=='gcc' and identity['java_version']=='21.0.12.1' and identity['ghidra_version']=='12.1.4' and int(identity['image_base'],16)==0
assert identity['java_home']==run['jdk'] and identity['user_home']==run['user_home'] and identity['tmp']==run['tmp'] and identity['jvm_arguments'][-1]=='-Dcpu.core.override=2'
cmd=j(D/'command.json');i=j(D/'invocation-before.json');oi=j(H/'invocation-before.json')
assert cmd==i['argv']==j(D/'attempt.json')['argv']==j(D/'process.json')['argv']
assert all(cmd.count(f)==1 for f in ('-readOnly','-deleteProject','-noanalysis')) and cmd[cmd.index('-import')+1]==str(D/'input/Corpus.x86_64')
assert j(D/'process.json')['driver_pid']==783370 and j(D/'process.json')['process_group_id']==783379 and j(H/'driver-pid.json')['pid']==783370
assert oi['argv']==j(H/'attempt.json')['argv'] and oi['argv'][3]=='actual' and oi['argv'][-1]==ident(H/'selection.json')['sha256']
assert oi['original_image_mode'] is True and oi['inherited_core']==[0,0] and oi['stdin']=='DEVNULL' and oi['timeout_seconds']==240 and oi['termination_grace_seconds']==25
assert oi['environment']==dict(PATH='/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8')
assert i['core_limit']==[0,0] and i['stdin']=='DEVNULL' and i['overall_timeout_seconds']==180 and i['per_entry_seconds']==60 and i['guest_execution'] is False
assert i['environment']['GHIDRA_HEADLESS_JAVA_OPTIONS']=='-Dcpu.core.override=2' and i['environment']['GHIDRA_HEADLESS_MAXMEM']=='4G'
samples=[json.loads(v) for v in (D/'resources.jsonl').read_text().splitlines()];assert len(samples)==6
for v in samples:assert v['group_rss_bytes']==sum(row['rss_bytes'] for row in v['members'].values()) and v['group_rss_bytes']<=6*1024**3 and v['free_disk_bytes']>=3*1024**3 and 0<=v['elapsed_seconds']<180
assert any('783487' in v['members'] for v in samples) and (H/'driver.stderr').stat().st_size==0
after=[ident(p) for p in sorted(paths)];assert before==after
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=ident(Path(__file__).resolve()),status='PASS STATIC EXPORT RETENTION ONLY; warnings/ABI unknowns preserved',inventory_payloads=dict(preparation=13,actual=38,outer=10,current_fixture=38,fixture_outer=10),pins=201,paired_maps=dict(inner=216,outer=2388),fresh_watch=len(paths),unchanged=True,watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest(),map_pins=[ident(p) for p in (D/'before-map.json',D/'after-map.json',H/'before-map.json',H/'after-map.json')],additional_watched=[v for v in before if v['path'] not in {r['path'] for r in ob}],outputs=outputs,resource_samples=6,max_sampled_RSS=max(v['group_rss_bytes'] for v in samples),minimum_sampled_free_disk=min(v['free_disk_bytes'] for v in samples),reviewer_tool_or_original_execution=False,opcode_or_deeper_semantic_validation=False)
with OUT.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('additional_watched','map_pins','outputs')},indent=2))
