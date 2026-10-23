"""Selected original static-import evidence; no tool/native execution or new target."""
from pathlib import Path
import datetime,hashlib,json,re,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-corpus-x86-selected-entry-preparation-r3';A=B/'depth-corpus-x86-selected-entry-actual-r3';O=B/'reviews/corpus-x86-selected-entry-actual-r3-selected-execution'
E=B/'reviews/corpus-x86-selected-entry-original-r3-actual-review-evidence.json';assert not E.exists()
def load(p):return json.loads(p.read_text())
def identity(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for raw in iter(lambda:f.read(1048576),b''):h.update(raw);n+=len(raw)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def verify(folder,m):
 rows=load(folder/m)['files'];assert {r['path'] for r in rows}=={str(q.relative_to(folder)) for q in folder.rglob('*') if q.is_file() and q!=folder/m}
 for r in rows:
  q=folder/r['path'];v=identity(q);assert not q.is_symlink() and (v['bytes'],v['sha256'])==(r['bytes'],r['sha256'])
 return len(rows)
started=datetime.datetime.now(datetime.timezone.utc).isoformat();assert [verify(P,'manifest-preparation.json'),verify(A,'manifest.json'),verify(O,'manifest.json')]==[11,38,10]
ib=load(A/'before-map.json');ia=load(A/'after-map.json');ob=load(O/'before-map.json');oa=load(O/'after-map.json');assert len(ib)==66 and ib==ia['files'] and ia['unchanged'] and len(ob)==3378 and ob==oa
paths={Path(x['path']) for x in ib+ob}|{q for f in (A,O) for q in f.rglob('*') if q.is_file()}|{B/'reviews/corpus-x86-selected-entry-actual-r3-root-assessment.json'}
prior_specs=[('calca-entry','calca-240','0x29c0'),('calca-fallthrough','calca-fallthrough-240','0x29c0'),('create-entry','create-entry-240','0x23b0'),('create-fallthrough','create-fallthrough-240','0x23b0')]
for name,stem,k in prior_specs:
 f=B/('depth-corpus-x86-'+name+'-instructions');paths|={f/'manifest.json',f/(stem+'.bin'),f/(stem+'.stdout.json')}
before=[identity(q) for q in sorted(paths)];idx={x['path']:x for x in before};assert all(idx[x['path']]==x for x in ib+ob)
for x in load(P/'inputs.json')['pins']:assert identity(Path(x['path']))==x
sel=load(O/'selection.json');run=load(A/'run.json');status=load(A/'run-status.json');receipt=load(O/'receipt.json');actual=load(A/'actual-identity.json');inv=load(A/'invocation-before.json')
for k in ['preparation','driver','root_preflight','peer_preflight','fixture_manifest','fixture_actual_review','wrapper_parent','wrapper']:assert identity(Path(sel[k]['path']))==sel[k]
assert sel['mode']=='actual' and sel['fixture_independently_approved'] is True
assert sel['fixture_actual_review']['sha256']=='fb1c67c62fd735c3937bc470df8e592f41b781ed4891ff8c0ff6040ccc9aaa07'
verify(Path(sel['fixture_manifest']['path']).parent,'manifest.json')
wrap=Path(sel['wrapper_parent']['path']).read_text()
for x in sel['wrapper_literal_delta']:assert wrap.count(x['old'])==x['count']==1;wrap=wrap.replace(x['old'],x['new'])
assert wrap==(O/'execute-selected-once.py').read_text() and len(sel['wrapper_literal_delta'])==8
assert receipt['attempts']==1 and receipt['driver_pid']==397023 and receipt['driver_exit']==0 and receipt['exception'] is None and not receipt['forced_driver_kill'] and not receipt['observed_group_residuals'] and receipt['unchanged']
assert status==load(O/'driver.stdout.json')==receipt['inner_status'] and status['tool_attempts']==1 and status['returned_pid']==397024 and status['exit_code']==0 and status['error'] is None and status['providers_unchanged']
assert status['cleanup']==dict(cleaned=True,survivors=[]) and not status['guest_execution'] and not status['automatic_retry']
assert load(O/'attempt.json')['attempt']==load(A/'attempt.json')['attempt']==1
assert load(O/'attempt.json')['argv']==load(O/'invocation-before.json')['argv']
assert inv['argv']==load(A/'command.json')==load(A/'process.json')['argv']==load(A/'attempt.json')['argv']
assert inv['argv'][inv['argv'].index('-import')+1]==str(A/'input/Corpus.x86_64') and all(x in inv['argv'] for x in ['-readOnly','-deleteProject','-noanalysis'])
assert inv['environment']['GHIDRA_HEADLESS_JAVA_OPTIONS']=='-Dcpu.core.override=2' and inv['core_limit']==[0,0] and inv['stdin']=='DEVNULL' and inv['overall_timeout_seconds']==180 and inv['per_entry_seconds']==60
assert (O/'driver.stderr').stat().st_size==0
for n in ['CorpusX86SelectedExport.java','run-selected.py']:assert (A/'method'/n).read_bytes()==(P/n).read_bytes()
raw=(A/'input/Corpus.x86_64').read_bytes();assert len(raw)==250352 and hashlib.sha256(raw).hexdigest()=='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
magic,cpu,sub,kind,ncmd,sz,flags,res=struct.unpack_from('<8I',raw);assert (magic,cpu)==(0xfeedfacf,0x01000007)
off=32;segments=[]
for _ in range(ncmd):
 cmd,n=struct.unpack_from('<II',raw,off);assert n>=8 and off+n<=32+sz
 if cmd==0x19:
  nm=raw[off+8:off+24].rstrip(b'\0').decode();vm,vs,fo,fs=struct.unpack_from('<4Q',raw,off+24);segments.append(dict(name=nm,vmaddr=vm,vmsize=vs,fileoff=fo,filesize=fs))
 off+=n
assert off==32+sz
expect=dict(executable_sha256=run['target_sha256'],language='x86:LE:64:default',compiler='gcc',ghidra_version='12.1.4',java_version='21.0.12.1',max_heap=4294967296,processors=2,default_pool=2,user_home=str(A/'java-home'),tmp=str(A/'java-tmp'),auto_analysis=False,whole_program_available_to_decompiler=True)
assert all(actual[k]==v for k,v in expect.items()) and int(actual['image_base'],16)==0 and actual['pid']==397128 and actual['jvm_arguments'][-1]=='-Dcpu.core.override=2'
results=[];listings={};body_offsets={}
for addr,size,count,state in [('0x23b0',110,32,'exported'),('0x29c0',918,228,'exported-with-warnings')]:
 f=A/'functions'/addr;m=load(f/'metadata.json');start=int(addr,16);end=start+size
 assert m['body_ranges']==[dict(start=addr,end=hex(end-1))] and m['body_bytes']==size and m['instruction_count']==count
 assert start<end<start+1024 and int(m['window_end'],16)==start+1023 and m['seed']==run['seeds'][len(results)]
 assert m['state']==state and m['completed'] is True and not m.get('error') and all(m[k] is False for k in ['partial_code','timed_out','cancelled','failed_to_start','auto_analysis','incremental_code_analysis'])
 assert m['target_sha256']==run['target_sha256'] and m['method_sha256']==run['method_sha256']
 lines=(f/'assembly.txt').read_text().splitlines();entries=[(int(l.split(': ',1)[0],16),l.split(': ',1)[1]) for l in lines]
 assert len(entries)==count and entries[0][0]==start and all(entries[i][0]<entries[i+1][0] for i in range(count-1)) and entries[-1][0]<end
 lengths=[entries[i+1][0]-v[0] if i+1<count else end-v[0] for i,v in enumerate(entries)]
 assert all(1<=n<=15 for n in lengths) and sum(lengths)==size
 for va,op in entries:
  if op.split()[0].startswith('J'):
   dest=int(op.split()[1],16);assert start<=dest<end and dest in {x[0] for x in entries}
 matches=[s for s in segments if s['vmaddr']<=start and end<=s['vmaddr']+s['filesize']];assert len(matches)==1
 seg=matches[0];fileoff=seg['fileoff']+start-seg['vmaddr'];body_offsets[addr]=fileoff
 code=(f/'pseudocode.c').read_text();warnings=[l.strip() for l in code.splitlines() if 'WARNING' in l.upper()];assert warnings==m['warnings']
 listings[addr]=dict(entries)
 results.append(dict(address=addr,body_bytes=size,instructions=count,body_file_offset=fileoff,body_raw_sha256=hashlib.sha256(raw[fileoff:fileoff+size]).hexdigest(),listing_address_structure_valid=True,independent_whole_body_x86_decode=False,state=state,warnings=warnings,C=identity(f/'pseudocode.c'),listing=identity(f/'assembly.txt')))
assert results[1]['warnings']==['/* WARNING: Removing unreachable block (ram,0x00002d51) */',"/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */"]
# Compare only64 already-retained decoder rows; no tool or additional original code bytes.
def normal(op,va,size):
 op=op.lower().replace(' ptr','');op=re.sub(r'\[rip\+0x([0-9a-f]+)\]',lambda m:'['+hex(va+size+int(m.group(1),16))+']',op)
 op=re.sub(r'0x[0-9a-f]+',lambda m:hex(int(m.group(0),16)),op)
 op=op.replace('qword[','[') if op.startswith('lea ') else op
 if op.startswith('lea '):op=op.replace('qword [','[')
 return re.sub(r'\s+','',op).replace('+-','-')
prior=[]
for name,stem,addr in prior_specs:
 f=B/('depth-corpus-x86-'+name+'-instructions');rows=load(f/(stem+'.stdout.json'));oldraw=(f/(stem+'.bin')).read_bytes();assert len(rows)==16 and len(oldraw)==240
 at=rows[0]['offset'];consumed=0
 # Existing metadata fixes retained selected-window mapping; this slice comes from already imported current thin.
 assert body_offsets[addr]==int(addr,16)
 for row in rows:
  va=row['offset'];n=row['size'];rb=bytes.fromhex(row['bytes']);assert va==at+consumed and len(rb)==n and 1<=n<=15
  assert raw[va:va+n]==rb==oldraw[consumed:consumed+n]
  assert normal(row['opcode'],va,n)==normal(listings[addr][va],va,n)
  consumed+=n
 prior.append(dict(provider=name,manifest=identity(f/'manifest.json'),rows=16,consumed_bytes=consumed,start=hex(at),end_exclusive=hex(at+consumed),raw_addresses_operand_text_agreement=True))
resources=[json.loads(l) for l in (A/'resources.jsonl').read_text().splitlines()];assert len(resources)==6
for x in resources:assert sum(m['rss_bytes'] for m in x['members'].values())==x['group_rss_bytes']<=6*1024**3 and x['free_disk_bytes']>=3*1024**3 and x['elapsed_seconds']<180
for name in ['headless.stdout','ghidra.log']:
 text=(A/name).read_text();assert 'Loaded 0 additional files' in text and 'Selected export 0x23b0: exported' in text and 'Selected export 0x29c0: exported-with-warnings' in text and 'SCRIPT ERROR' not in text
 assert 'libc++.1.dylib' in text and 'not found in project' in text
assert any(str(actual['pid']) in x['members'] for x in resources)
after=[identity(q) for q in sorted(paths)];assert before==after
result=dict(status='PASS BOUNDED ORIGINAL STATIC IMPORT WITH RETAINED WARNINGS ONLY',started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=identity(Path(__file__)),actual_manifest=identity(A/'manifest.json'),outer_manifest=identity(O/'manifest.json'),preparation=identity(P/'manifest-preparation.json'),input=identity(A/'input/Corpus.x86_64'),thin_header=dict(ncmds=ncmd,sizeofcmds=sz,segments=segments),exports=results,prior_prefixes=prior,inner_pairs=66,outer_pairs=3378,pairs_equal=True,fresh_watch=len(paths),fresh_watch_equal=True,watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),resource_samples=dict(count=6,sampled_max_RSS=max(x['group_rss_bytes'] for x in resources),sampled_min_free_disk=min(x['free_disk_bytes'] for x in resources)),suppliedcode_tools_or_native_execution=False,new_callee_or_global_or_window_follow=False)
with E.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=identity(E),watch=len(paths))))
