"""Independent successful own-fixture evidence review; stdlib data only."""
from pathlib import Path
import datetime,hashlib,json,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P=B/'depth-corpus-x86-selected-entry-preparation-r3';A=B/'depth-corpus-x86-selected-entry-fixture-r3';O=B/'reviews/corpus-x86-selected-entry-fixture-r3-selected-execution'
E=B/'reviews/corpus-x86-selected-entry-fixture-r3-actual-review-evidence.json';assert not E.exists()
def load(p):return json.loads(p.read_text())
def identity(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for raw in iter(lambda:f.read(1048576),b''):h.update(raw);n+=len(raw)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def inventory(folder,name):
 rows=load(folder/name)['files'];assert {r['path'] for r in rows}=={str(q.relative_to(folder)) for q in folder.rglob('*') if q.is_file() and q!=folder/name}
 for row in rows:
  q=folder/row['path'];assert not q.is_symlink();got=identity(q);assert (got['bytes'],got['sha256'])==(row['bytes'],row['sha256'])
 return len(rows)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
counts=[inventory(P,'manifest-preparation.json'),inventory(A,'manifest.json'),inventory(O,'manifest.json')];assert counts==[11,38,10]
ib=load(A/'before-map.json');ia=load(A/'after-map.json');ob=load(O/'before-map.json');oa=load(O/'after-map.json')
assert len(ib)==66 and ib==ia['files'] and ia['unchanged']
assert len(ob)==3338 and ob==oa
paths={Path(x['path']) for x in ib+ob}|{q for d in (A,O) for q in d.rglob('*') if q.is_file()}
before=[identity(q) for q in sorted(paths)];lookup={x['path']:x for x in before}
assert all(lookup[x['path']]==x for x in ib+ob)
for row in load(P/'inputs.json')['pins']:assert identity(Path(row['path']))==row
sel=load(O/'selection.json');status=load(A/'run-status.json');receipt=load(O/'receipt.json');run=load(A/'run.json');actual=load(A/'actual-identity.json');inv=load(A/'invocation-before.json')
for k in ['preparation','driver','root_preflight','peer_preflight','wrapper_parent','wrapper']:assert identity(Path(sel[k]['path']))==sel[k]
wrapper=Path(sel['wrapper_parent']['path']).read_text()
for x in sel['wrapper_literal_delta']:assert wrapper.count(x['old'])==x['count']==1;wrapper=wrapper.replace(x['old'],x['new'])
assert wrapper==(O/'execute-selected-once.py').read_text() and len(sel['wrapper_literal_delta'])==4
assert receipt['attempts']==1 and receipt['outer_pid']==394802 and receipt['driver_pid']==394811 and receipt['driver_exit']==0
assert receipt['exception'] is None and not receipt['forced_driver_kill'] and receipt['observed_group_residuals']==[] and receipt['unchanged']
assert receipt['inner_status']==status==load(O/'driver.stdout.json')
assert status['tool_attempts']==1 and status['returned_pid']==394813 and status['exit_code']==0 and status['error'] is None
assert status['cleanup']==dict(cleaned=True,survivors=[]) and not status['automatic_retry'] and not status['guest_execution'] and status['providers_unchanged']
assert status['items']==[dict(address=x,state='exported',error=None) for x in ['0x23b0','0x29c0']]
assert load(O/'attempt.json')['attempt']==load(A/'attempt.json')['attempt']==1
assert load(O/'attempt.json')['argv']==load(O/'invocation-before.json')['argv']
assert load(O/'driver-pid.json')['pid']==394811
assert (O/'driver.stderr').stat().st_size==0
for n in ['CorpusX86SelectedExport.java','run-selected.py']:assert (A/'method'/n).read_bytes()==(P/n).read_bytes()
raw=(A/'input/Corpus.x86_64').read_bytes();assert len(raw)==12288 and raw==(P/'synthetic-corpus-x86.macho').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='688f2e17c99b0c70aaa55c856cc687c2a28ce54e3dc6909b693f4bd4e0af93d2'
assert struct.unpack_from('<8I',raw)==(0xfeedfacf,0x1000007,3,8,1,152,0,0)
expected=dict(executable_sha256=run['target_sha256'],language='x86:LE:64:default',compiler='gcc',ghidra_version='12.1.4',java_version='21.0.12.1',java_home='/home/ollie/.local/opt/jdk-21.0.12.1+1',max_heap=4294967296,processors=2,default_pool=2,user_home=str(A/'java-home'),tmp=str(A/'java-tmp'),auto_analysis=False,whole_program_available_to_decompiler=True)
assert all(actual[k]==v for k,v in expected.items()) and int(actual['image_base'],16)==0 and actual['pid']==394917
assert actual['jvm_arguments'][-1]=='-Dcpu.core.override=2' and '-Xmx4G' in actual['jvm_arguments'] and '-XX:ActiveProcessorCount=2' in actual['jvm_arguments']
assert actual['executable']==str(Path(actual['java_home'])/'bin/java')
assert inv['environment']['GHIDRA_HEADLESS_JAVA_OPTIONS']=='-Dcpu.core.override=2' and inv['environment']['GHIDRA_HEADLESS_MAXMEM']=='4G'
assert inv['core_limit']==[0,0] and inv['stdin']=='DEVNULL' and inv['overall_timeout_seconds']==180 and inv['per_entry_seconds']==60 and inv['start_new_session']
assert inv['argv']==load(A/'command.json')==load(A/'attempt.json')['argv']==load(A/'process.json')['argv']
assert inv['argv'][inv['argv'].index('-import')+1]==str(A/'input/Corpus.x86_64')
assert all(x in inv['argv'] for x in ['-readOnly','-deleteProject','-noanalysis'])
java=(A/'method/CorpusX86SelectedExport.java').read_text()
assert 'SystemUtilities.getDefaultThreadPoolSize()!=2' in java and '!"2".equals(System.getProperty("cpu.core.override"))' in java and '!"2".equals(System.getProperty("cpu.core.limit"))' in java
assert java.index('Effective JDK/4GiB heap/CPU2 identity mismatch')<java.index('actual-identity.json')<java.index('Files.createDirectory(output.resolve("functions"))')
results=[]
assert {q.name for q in (A/'functions').iterdir()}=={'0x23b0','0x29c0'}
for addr,size,hexbytes,assembly,code in [('0x23b0',6,'b82a000000c3','0x23b0: MOV EAX,0x2a\n0x23b5: RET\n','undefined8 FUN_000023b0(void)\n\n{\n  return 0x2a;\n}'),('0x29c0',3,'31c0c3','0x29c0: XOR EAX,EAX\n0x29c2: RET\n','undefined8 FUN_000029c0(void)\n\n{\n  return 0;\n}')]:
 f=A/'functions'/addr;m=load(f/'metadata.json');start=int(addr,16)
 assert raw[start:start+size].hex()==hexbytes
 assert m['state']=='exported' and m['completed'] is True and m['warnings']==[] and not m.get('error')
 assert all(m[k] is False for k in ['partial_code','timed_out','cancelled','failed_to_start','auto_analysis','incremental_code_analysis'])
 assert m['body_bytes']==size and m['instruction_count']==2 and m['body_ranges']==[dict(start=addr,end=hex(start+size-1))]
 assert m['seed']==run['seeds'][len(results)] and m['address']==addr and int(m['window_end'],16)==start+1023
 assert m['target_sha256']==run['target_sha256'] and m['method_sha256']==run['method_sha256'] and m['decompile_timeout_seconds']==60
 assert (f/'assembly.txt').read_text()==assembly and (f/'pseudocode.c').read_text().strip()==code
 results.append(dict(address=addr,body_bytes=size,instructions=2,C_and_listing_match_owned_bytes=True,metadata=identity(f/'metadata.json')))
for name in ['headless.stdout','ghidra.log']:
 text=(A/name).read_text();assert 'Loaded 0 additional files' in text and 'Using Language/Compiler: x86:LE:64:default:gcc' in text
 assert 'Selected export 0x23b0: exported' in text and 'Selected export 0x29c0: exported' in text
 assert 'SCRIPT ERROR' not in text and 'Processing aborted' not in text
resources=[json.loads(x) for x in (A/'resources.jsonl').read_text().splitlines()];assert len(resources)==5
for x in resources:
 assert x['group_rss_bytes']==sum(y['rss_bytes'] for y in x['members'].values()) and x['group_rss_bytes']<=6*1024**3 and x['free_disk_bytes']>=3*1024**3 and x['elapsed_seconds']<180
assert any(str(actual['pid']) in x['members'] for x in resources)
assert not (B/'depth-corpus-x86-selected-entry-actual-r3').exists()
after=[identity(q) for q in sorted(paths)];assert before==after
result=dict(status='PASS EXACT OWN SYNTHETIC FIXTURE ONLY',started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=identity(Path(__file__)),manifests=[identity(P/'manifest-preparation.json'),identity(A/'manifest.json'),identity(O/'manifest.json')],payload_counts=counts,inner_pairs=66,outer_pairs=3338,pairs_equal=True,fresh_watch=len(paths),fresh_watch_equal=True,watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),effective_identity=identity(A/'actual-identity.json'),fixture_results=results,resources=dict(samples=5,sampled_max_RSS=max(x['group_rss_bytes'] for x in resources),sampled_min_free_disk=min(x['free_disk_bytes'] for x in resources)),property_qualification='override2 and limit2 inferred from unchanged guard completion under executed-source-binding premise; override2 also last JVM option. No separate property fields are in actual-identity.',separate_java_exit_receipt=False,suppliedcode_tools_or_original_execution=False,original_import_selected=False)
with E.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=identity(E),watch=len(paths))))
