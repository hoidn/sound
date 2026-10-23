"""Independent selected72-byte data and native bitfield assertions. No tool execution."""
from pathlib import Path
import datetime,hashlib,json,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
A=B/'depth-utility-mute-calcmain-instruction-data';O=B/'reviews/utility-mute-calcmain-selected-execution'
P=B/'depth-utility-mute-calcmain-instruction-preparation';R=B/'reviews/utility-mute-calcmain-static-actual-review-evidence.json'
ASSESS=B/'reviews/utility-mute-calcmain-author-actual-assessment.json'
assert not R.exists()
def load(p):return json.loads(p.read_text())
def identity(p):
 h=hashlib.sha256();size=0
 with p.open('rb') as f:
  for raw in iter(lambda:f.read(1048576),b''):h.update(raw);size+=len(raw)
 return dict(path=str(p),bytes=size,sha256=h.hexdigest())
def inventory(folder):
 x=load(folder/'manifest.json')['files']
 assert {r['path'] for r in x}=={str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file() and p!=folder/'manifest.json'}
 for r in x:
  p=folder/r['path'];assert not p.is_symlink();row=identity(p);assert (row['bytes'],row['sha256'])==(r['bytes'],r['sha256'])
 return len(x)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert inventory(A)==10 and inventory(O)==11
assert identity(A/'manifest.json')['sha256']=='78f01161ff5fadfc96ac6032476628ca0edcb66f162efbd0f2dcc898048d3ca1'
assert identity(O/'manifest.json')['sha256']=='dcc892199ba47faebc5e88ebe800a9390ad2d892f4c0f0efe96cc7396ad4b1ad'
assert identity(ASSESS)['sha256']=='187c974f5d82c2ecf423ef4cba844688aee6ececf4c69486b9823e51c55d2725'
ib=load(A/'before-map.json');ia=load(A/'after-map.json');ob=load(O/'before-map.json');oa=load(O/'after-map.json')
assert len(ib)==210 and ib==ia['files'] and ia['unchanged']
assert [json.loads(l) for l in (A/'before-identities.jsonl').read_text().splitlines()]==ib
assert len(ob)==3394 and ob==oa
plan=load(P/'plan.json');sel=load(O/'selection.json')
paths={Path(x['path']) for x in ob+ib}|{p for d in (A,O) for p in d.rglob('*') if p.is_file()}|{ASSESS}
before=[identity(p) for p in sorted(paths)];index={x['path']:x for x in before}
assert all(index[x['path']]==x for x in ob+ib)
for x in load(O/'pins.json'):assert identity(Path(x['path']))==x
for k in ['preparation','collector','root_preflight','peer_preflight','wrapper','wrapper_parent']:assert identity(Path(sel[k]['path']))==sel[k]
wrap=Path(sel['wrapper_parent']['path']).read_text()
for old,new in sel['wrapper_exact_four_literal_operations']:
 assert wrap.count(old)==1;wrap=wrap.replace(old,new)
assert len(sel['wrapper_exact_four_literal_operations'])==4 and wrap==(O/'execute-selected-once.py').read_text()
s=load(A/'status.json');receipt=load(O/'receipt.json');inv=load(A/'invocation-before.json')
assert s==load(O/'collector.stdout.json') and s['tool_attempts']==1 and s['tool_returned_pid']==392492 and s['tool_exit']==0 and s['exception'] is None
assert s['original_calls']==0 and not s['emulation'] and s['caller_bytes']==0 and s['watch_unchanged']
assert receipt['attempted_collector_launches']==1 and receipt['returned_collector_pid']==392487 and receipt['exit']==0 and receipt['exception'] is None
assert not receipt['timeout'] and not receipt['cleanup_group_killed'] and not receipt['automatic_retry'] and receipt['unchanged']
assert receipt['inherited_RLIMIT_CORE']==[0,0] and receipt['environment']=={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8'}
assert load(O/'attempt.json')['attempt']==1 and load(O/'collector-pid.json')['pid']==392487
assert load(O/'attempt.json')['argv']==load(O/'invocation-before.json')['argv']
assert (O/'collector.stderr').stat().st_size==(A/'decoder.stderr').stat().st_size==0
assert inv['argv']==plan['decoder_argv'] and 'pdj 18' in inv['argv'] and inv['timeout_seconds']==30
assert inv['argv'][1:5]==['-NN','-n','-x','-f'] and not inv['analysis_or_emulation'] and not inv['original_instructions_executed']
image=Path(plan['image']['path']);assert identity(image)==plan['image']
with image.open('rb') as f:
 header=f.read(32);assert header.hex()==plan['image_header_hex']
 magic,cpu,sub,typ,ncmds,sz,flags,res=struct.unpack('<8I',header)
 assert (magic,cpu,ncmds,sz)==(0xfeedfacf,0x0100000c,53,6944)
 commands=f.read(sz);assert hashlib.sha256(commands).hexdigest()==plan['load_commands_sha256']
 segments=[];off=0
 for i in range(ncmds):
  cmd,cmdsize=struct.unpack_from('<II',commands,off);assert cmdsize>=8 and off+cmdsize<=len(commands)
  if cmd==0x19:
   name=commands[off+8:off+24].rstrip(b'\0').decode();vm,vs,fo,fs,mp,ip=struct.unpack_from('<4Q2I',commands,off+24)
   segments.append(dict(name=name,vmaddr=vm,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip))
  off+=cmdsize
 assert off==sz
 start=0x1021658b0;end=start+72
 matches=[x for x in segments if x['vmaddr']<=start and end<=x['vmaddr']+x['filesize']]
 assert len(matches)==1 and matches[0]==plan['expected_segment']
 segment=matches[0];offset=segment['fileoff']+start-segment['vmaddr'];assert offset==35018928
 f.seek(offset);fresh=f.read(72)
raw=(A/'calcmain-72.bin').read_bytes();assert fresh==raw and len(raw)==72
assert hashlib.sha256(raw).hexdigest()=='ec5398a6287334d5ef79880ea5c826b8c49905b125382a03b1893b22723ca519'
rows=load(A/'decoder.stdout.json');assert len(rows)==18
ex=load(A/'extraction.json');assert ex['image_header_hex']==header.hex() and ex['load_commands_sha256']==hashlib.sha256(commands).hexdigest()
assert ex['selected_mapping']==segment and ex['file_offset']==offset and ex['length']==72
fields=[]
for i,row in enumerate(rows):
 assert row['offset']==start+4*i and row['size']==4 and len(bytes.fromhex(row['bytes']))==4 and bytes.fromhex(row['bytes'])==raw[i*4:i*4+4]
 assert row.get('type','').lower() not in ('ill','invalid') and row['opcode'].strip() and row['opcode'].strip().lower()!='invalid'
 w=struct.unpack_from('<I',raw,4*i)[0]
 assert ex['words'][i]==dict(va=hex(start+4*i),bytes=row['bytes'],word=hex(w))
 fields.append(dict(address=hex(start+4*i),word=hex(w),opcode=row['opcode']))
w=list(struct.unpack('<18I',raw))
# Exact immediate64 arithmetic class with no flags, shift0, register identities and immediates.
for i,base,rd,rn,imm in [(0,0xd1000000,31,31,48),(3,0x91000000,29,31,32),(10,0x91000000,0,0,72),(11,0x91000000,1,31,8),(16,0x91000000,31,31,48)]:
 assert w[i]&0xffc00000==base and w[i]&31==rd and (w[i]>>5)&31==rn and (w[i]>>10)&4095==imm
 fields[i].update(kind='immediate64',rd=rd,rn=rn,immediate=imm)
# 64-bit integer offset pairs or32-bit SIMD offset pair; signextend imm7 with class scale.
for i,base,rt,rt2,rn,imm,scale in [(1,0xa9000000,20,19,31,16,8),(2,0xa9000000,29,30,31,32,8),(5,0xa9400000,8,9,0,48,8),(13,0x2d000000,0,1,19,64,4),(14,0xa9400000,29,30,31,32,8),(15,0xa9400000,20,19,31,16,8)]:
 assert w[i]&0xffc00000==base and w[i]&31==rt and (w[i]>>10)&31==rt2 and (w[i]>>5)&31==rn
 v=(w[i]>>15)&127;v=v-128 if v&64 else v;assert v*scale==imm
 fields[i].update(kind='pair_offset',rt=rt,rt2=rt2,rn=rn,offset=imm,width=scale)
assert w[4]&0xffe0ffe0==0xaa0003e0 and w[4]&31==19 and (w[4]>>16)&31==0
fields[4].update(kind='ORR_MOV64',rd=19,rm=0,rn=31)
for i,base,rn,imm in [(6,0xbd400000,8,0),(7,0xbd000000,31,8),(8,0xbd400000,9,0),(9,0xbd000000,31,12)]:
 assert w[i]&0xffc00000==base and w[i]&31==0 and (w[i]>>5)&31==rn and ((w[i]>>10)&4095)*4==imm
 fields[i].update(kind='SIMD_scalar_unsigned32',rt=0,rn=rn,offset=imm,width=4)
assert w[12]&0xfc000000==0x94000000
v=w[12]&0x3ffffff;v=v-(1<<26) if v&(1<<25) else v;target=start+48+v*4
assert target==0x1047bd790 and rows[12]['jump']==target
fields[12].update(kind='BL',target=hex(target),return_address=hex(start+52))
assert w[17]&0xfffffc1f==0xd65f0000 and (w[17]>>5)&31==30
fields[17].update(kind='RET',rn=30)
assert all('kind' in x for x in fields)
after=[identity(p) for p in sorted(paths)];assert after==before
result=dict(status='PASS SELECTED STATICDATA ONLY',started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=identity(Path(__file__)),actual_manifest=identity(A/'manifest.json'),outer_manifest=identity(O/'manifest.json'),author_assessment=identity(ASSESS),payloads=[10,11],same72_original_data_verified=True,image=plan['image'],header=header.hex(),commands_sha256=hashlib.sha256(commands).hexdigest(),ncmds=53,sizeofcmds=6944,mapping=segment,file_offset=offset,raw=identity(A/'calcmain-72.bin'),all18_native_fields_verified=fields,inner_paired_rows=210,outer_paired_rows=3394,all_pairs_equal=True,freshwatch=len(before),freshwatch_equal=True,watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),new_R3_draft_globbed_or_read=False,tools_suppliedcode_or_original_execution=False,helper_body_target_suffix_read=False)
with R.open('x') as out:json.dump(result,out,indent=2);out.write('\n')
print(json.dumps(dict(evidence=identity(R),watch=len(before))))
