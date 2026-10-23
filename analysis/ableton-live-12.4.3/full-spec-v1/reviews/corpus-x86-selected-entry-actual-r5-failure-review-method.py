"""Independent DATA-only failure audit; no supplied imports or original body decode."""
from pathlib import Path
import datetime,hashlib,json
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P=B/'depth-corpus-x86-selected-entry-preparation-r5'
D=B/'depth-corpus-x86-selected-entry-actual-r5'
H=B/'reviews/corpus-x86-selected-entry-actual-r5-selected-execution'
OUT=B/'reviews/corpus-x86-selected-entry-actual-r5-failure-review-evidence.json'
def j(p):return json.loads(p.read_text())
def ident(p):
 h=hashlib.sha256();size=0
 with p.open('rb') as f:
  for raw in iter(lambda:f.read(1048576),b''):size+=len(raw);h.update(raw)
 return dict(path=str(p),bytes=size,sha256=h.hexdigest())
def check(row):assert ident(Path(row['path']))==row,row['path']
def inv(root,name,n):
 m=j(root/name);rows=m['files'];assert len(rows)==n and len({r['path'] for r in rows})==n
 assert {r['path'] for r in rows}=={str(q.relative_to(root)) for q in root.rglob('*') if q.is_file() and q!=root/name}
 for r in rows:
  assert not Path(r['path']).is_absolute() and '..' not in Path(r['path']).parts
  got=ident(root/r['path']);assert (got['bytes'],got['sha256'])==(r['bytes'],r['sha256'])
 return m
s=j(H/'selection.json');ib=j(D/'before-map.json');ia=j(D/'after-map.json');ob=j(H/'before-map.json');oa=j(H/'after-map.json')
assert len(ib)==110 and len(ob)==3649 and ia==dict(files=ib,unchanged=True) and ob==oa
assert len({r['path'] for r in ib})==110 and len({r['path'] for r in ob})==3649
paths={Path(r['path']) for r in ib+ob}
for root in (P,D,H):paths.update(q for q in root.rglob('*') if q.is_file())
paths.add(Path(__file__).resolve())
before=[ident(q) for q in sorted(paths)]
for r in ib+ob:check(r)
for r in j(P/'inputs.json')['pins']:check(r)
assert len(j(P/'inputs.json')['pins'])==95
pm=inv(P,'manifest-preparation.json',13);dm=inv(D,'manifest.json',37);hm=inv(H,'manifest.json',10)
assert dm['mode']=='actual' and dm['guest_execution'] is False and hm['synthetic_only'] is False
for k in ('preparation','driver','root_preflight','peer_preflight','fixture_manifest','fixture_actual_review','wrapper','wrapper_parent'):check(s[k])
assert s['fixture_independently_approved'] is True and s['mode']=='actual' and s['original_calls']==0
assert j(Path(s['fixture_actual_review']['path']))['fixture_actual_review']['approved'] is True
assert s['fixture_manifest']['sha256']=='983e4bab0e7d38040c96cbe3380d15d476dfc98f375a99c5de2a871eb464afd1'
assert s['preparation']['sha256']=='7a1f153c866e4dbba656594b803d6261dc35d08bb4ec9f0a15ca86f0a0a423f4'
parent=Path(s['wrapper_parent']['path']).read_text()
assert len(s['literal_operations'])==4
for old,new in s['literal_operations']:
 assert old in parent;parent=parent.replace(old,new)
assert parent==(H/'execute-selected-once.py').read_text()
for n in ('CorpusX86SelectedExport.java','run-selected.py'):assert (P/n).read_bytes()==(D/'method'/n).read_bytes()
cfg=j(P/'actual-config.json');run=j(D/'run.json');assert {k:run[k] for k in cfg}==cfg
assert run['preparation_sha256']==s['preparation']['sha256'] and run['method_sha256']==ident(P/'CorpusX86SelectedExport.java')['sha256']
assert run['target']==str(D/'input/Corpus.x86_64') and run['source']['offset']==16384 and run['source']['length']==250352
assert ident(D/'input/Corpus.x86_64')['sha256']==run['target_sha256']=='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
assert [a['address'] for a in run['seeds']]==['0x23b0','0xd090'] and all(a['window_bytes']==4096 for a in run['seeds'])
m0=j(D/'functions/0x23b0/metadata.json');m1=j(D/'functions/0xd090/metadata.json')
error='IllegalStateException: Incomplete/ambiguous body: [Unresolved computed transfer at 0000db10]'
assert m0['state']=='exported' and m0['body_bytes']==110 and m0['instruction_count']==32 and m0['completed'] is True
assert m0['warnings']==[] and m0['partial_code'] is False
assert m1['state']=='failed' and m1['error']==error and m1['partial_code'] is False and m1['warnings']==[]
assert m1['body_bytes']==2685 and m1['instruction_count']==388 and 'completed' not in m1
assert not (D/'functions/0xd090/pseudocode.c').exists()
assert sum(int(r['end'],16)-int(r['start'],16)+1 for r in m1['body_ranges'])==2685
for m,seed in zip((m0,m1),run['seeds']):
 assert m['seed']==seed and m['target_sha256']==run['target_sha256'] and m['method_sha256']==run['method_sha256']
 assert m['auto_analysis'] is False and m['incremental_code_analysis'] is False and int(m['window_end'],16)==int(seed['address'],16)+4095
status=j(D/'run-status.json');receipt=j(H/'receipt.json');identity=j(D/'actual-identity.json')
assert receipt['inner_status']==status==j(H/'driver.stdout.json')
assert receipt['outer_pid']==410071 and receipt['driver_pid']==410074 and receipt['driver_exit']==1 and receipt['attempts']==1
assert receipt['exception'] is None and receipt['forced_driver_kill'] is False and receipt['observed_group_residuals']==[] and receipt['unchanged'] is True
assert status['mode']=='actual' and status['tool_attempts']==1 and status['returned_pid']==410083 and status['exit_code']==0 and status['error'] is None
assert status['guest_execution'] is False and status['automatic_retry'] is False and status['providers_unchanged'] is True
assert status['cleanup']==dict(cleaned=True,survivors=[]) and status['items']==[dict(address='0x23b0',state='exported',error=None),dict(address='0xd090',state='failed',error=error)]
assert j(D/'process.json')['driver_pid']==410074 and j(D/'process.json')['process_group_id']==410083 and j(H/'driver-pid.json')['pid']==410074
assert identity['pid']==410189 and identity['executable_sha256']==run['target_sha256'] and int(identity['image_base'],16)==0
for k,v in dict(language='x86:LE:64:default',compiler='gcc',java_version='21.0.12.1',ghidra_version='12.1.4',max_heap=4294967296,processors=2,default_pool=2,auto_analysis=False,whole_program_available_to_decompiler=True).items():assert identity[k]==v
assert identity['java_home']==run['jdk'] and identity['user_home']==run['user_home'] and identity['tmp']==run['tmp'] and identity['jvm_arguments'][-1]=='-Dcpu.core.override=2'
c=j(D/'command.json');i=j(D/'invocation-before.json');oi=j(H/'invocation-before.json')
assert c==i['argv']==j(D/'attempt.json')['argv']==j(D/'process.json')['argv']
assert c[c.index('-import')+1]==str(D/'input/Corpus.x86_64') and all(c.count(f)==1 for f in ('-noanalysis','-readOnly','-deleteProject'))
assert oi['argv']==j(H/'attempt.json')['argv'] and oi['argv'][3]=='actual' and oi['argv'][-1]==ident(H/'selection.json')['sha256']
assert oi['original_image_mode'] is True and oi['automatic_retry'] is False and oi['timeout_seconds']==240 and oi['termination_grace_seconds']==25
assert oi['inherited_core']==[0,0] and oi['stdin']=='DEVNULL' and oi['environment']==dict(PATH='/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8')
assert i['core_limit']==[0,0] and i['stdin']=='DEVNULL' and i['overall_timeout_seconds']==180 and i['per_entry_seconds']==60 and i['guest_execution'] is False
assert i['environment']['GHIDRA_HEADLESS_MAXMEM']=='4G' and i['environment']['GHIDRA_HEADLESS_JAVA_OPTIONS']=='-Dcpu.core.override=2'
assert (H/'driver.stderr').stat().st_size==0
samples=[json.loads(row) for row in (D/'resources.jsonl').read_text().splitlines()];assert len(samples)==5
for row in samples:
 assert row['group_rss_bytes']==sum(v['rss_bytes'] for v in row['members'].values())
 assert 0<=row['elapsed_seconds']<180 and row['group_rss_bytes']<=6*1024**3 and row['free_disk_bytes']>=3*1024**3
assert any(str(identity['pid']) in row['members'] for row in samples)
after=[ident(q) for q in sorted(paths)];assert before==after
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=ident(Path(__file__).resolve()),result='PASS FAILURE-ACCOUNTING/INTEGRITY ONLY; R5 export attempt remains FAILED',inventory_payloads=dict(preparation=13,actual=37,outer=10),pins=95,paired_maps=dict(inner=110,outer=3649),fresh_watched_paths=len(paths),unchanged=True,map_pins=[ident(q) for q in (D/'before-map.json',D/'after-map.json',H/'before-map.json',H/'after-map.json')],extra_watched=[r for r in before if r['path'] not in {a['path'] for a in ob}],combined_watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest(),resources=dict(samples=5,max_sampled_rss=max(a['group_rss_bytes'] for a in samples),minimum_sampled_free_disk=min(a['free_disk_bytes'] for a in samples)),original_listing_and_C_semantics_read=False,decoder_or_original_run=False)
with OUT.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('extra_watched','map_pins')},indent=2))
