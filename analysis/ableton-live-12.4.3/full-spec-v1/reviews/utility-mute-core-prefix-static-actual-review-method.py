from pathlib import Path
import datetime,hashlib,json,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-utility-mute-core-prefix-instruction-preparation';D=B/'depth-utility-mute-core-prefix-instruction-data';H=B/'reviews/utility-mute-core-prefix-selected-execution';A=B/'reviews/utility-mute-core-prefix-author-actual-assessment.json'
def pin(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x);n+=len(x)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
plan=json.loads((P/'plan.json').read_text());inner=json.loads((D/'before-map.json').read_text());outer=json.loads((H/'before-map.json').read_text());paths=sorted({Path(x['path']) for x in inner+outer}|{x for q in [P,D,H] for x in q.iterdir() if x.is_file()}|{A})
before=[pin(p) for p in paths]
assert pin(D/'manifest.json')['sha256']=='4efaef8c559a4dc4dd60709c4d06e16e044683bfa2545994098525b37b74ee30'
assert pin(H/'manifest.json')['sha256']=='b8881a8fc4a25645ed63eb12bd17f0f865cfe2be4f60dfd305a9b11d17634e9a'
assert inner==json.loads((D/'after-map.json').read_text())['files'] and outer==json.loads((H/'after-map.json').read_text())
for v in inner+outer:assert pin(Path(v['path']))==v
for q in [P,D,H]:
 name='manifest-preparation.json' if q==P else 'manifest.json';m=json.loads((q/name).read_text());assert {x['path'] for x in m['files']}=={x.name for x in q.iterdir() if x.is_file() and x.name!=name}
 for x in m['files']:
  a=pin(q/x['path']);assert(a['bytes'],a['sha256'])==(x['bytes'],x['sha256'])
selection=json.loads((H/'selection.json').read_text());wrapper=(H/'execute-selected-once.py').read_text();restored=wrapper
for op in reversed(selection['wrapper_literal_delta']):assert restored.count(op['new'])==op['count'];restored=restored.replace(op['new'],op['old'])
assert restored==Path(selection['wrapper_parent']['path']).read_text()
for key in ['preparation','collector','root_preflight','peer_preflight','wrapper','wrapper_parent']:assert pin(Path(selection[key]['path']))==selection[key]
status=json.loads((D/'status.json').read_text());receipt=json.loads((H/'receipt.json').read_text());assert status['tool_attempts']==1 and status['tool_exit']==0 and not status['exception'] and receipt['attempted_collector_launches']==1 and receipt['exit']==0 and not receipt['exception'] and not receipt['timeout'] and not receipt['automatic_retry'];assert status['watched']==183 and receipt['watched']==3410
assert (D/'decoder.stderr').stat().st_size==0 and (H/'collector.stderr').stat().st_size==0
assert json.loads((H/'collector.stdout.json').read_text())==status
for x in json.loads((H/'pins.json').read_text()):assert pin(Path(x['path']))==x
image=Path(plan['image']['path']);assert pin(image)==plan['image'];start=0x1047bd790;length=32
with image.open('rb') as f:
 header=f.read(32);assert header.hex()==plan['image_header_hex'];v=struct.unpack('<IiiIIIII',header);assert v[0]==0xfeedfacf and v[1]==0x100000c and v[4:6]==(53,6944)
 commands=f.read(v[5]);assert hashlib.sha256(commands).hexdigest()==plan['load_commands_sha256'];cursor=0;segments=[]
 for i in range(v[4]):
  cmd,size=struct.unpack_from('<II',commands,cursor);assert size>=8 and cursor+size<=len(commands)
  if cmd==0x19:
   assert size>=72
   name,va,vs,off,fs,mp,ip,ns,flags=struct.unpack_from('<16sQQQQiiII',commands,cursor+8);segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=off,filesize=fs,maxprot=mp,initprot=ip))
  cursor+=size
 assert cursor==len(commands);maps=[x for x in segments if x['vmaddr']<=start and start+length<=x['vmaddr']+min(x['filesize'],x['vmsize'])];assert maps==[plan['expected_segment']]
 off=maps[0]['fileoff']+start-maps[0]['vmaddr'];assert off==75224976;f.seek(off);raw=f.read(32)
assert raw==(D/'core-prefix-32.bin').read_bytes() and hashlib.sha256(raw).hexdigest()=='ee0eeccf1a9a7499dfeb7511d72f6d9944c464ec43f6a21a6400de39c606d328'
rows=json.loads((D/'decoder.stdout.json').read_text());assert len(rows)==8 and all(x['offset']==start+4*i and x['size']==4 for i,x in enumerate(rows)) and b''.join(bytes.fromhex(x['bytes']) for x in rows)==raw
words=struct.unpack('<8I',raw);actual=[]
for i,w in enumerate(words):
 d=dict(index=i,va=hex(start+4*i),raw_bytes=raw[i*4:i*4+4].hex(),word=hex(w))
 if i==0:
  assert w&0xffc00000==0x39400000;d.update(kind='LDRB unsigned immediate',rt=w&31,rn=(w>>5)&31,byte_offset=(w>>10)&4095);assert(d['rt'],d['rn'],d['byte_offset'])==(8,0,207)
 elif i in [1,2]:
  assert w&~31==0x2f00e400;d.update(kind='MOVI D literal bitmask',rd=w&31,Q=(w>>30)&1,op=(w>>29)&1,cmode=(w>>12)&15,imm8=(((w>>16)&7)<<5)|((w>>5)&31),literal_low64_hex='0000000000000000');assert d['imm8']==0 and d['rd']==i-1
 elif i==3:
  assert w&0x7f000000==0x37000000;imm=(w>>5)&0x3fff;imm=imm-0x4000 if imm&0x2000 else imm;target=start+4*i+imm*4;d.update(kind='TBNZ',rt=w&31,bit=(((w>>31)&1)<<5)|((w>>19)&31),signed_offset_bytes=imm*4,target=hex(target),fallthrough=hex(start+4*i+4));assert(d['rt'],d['bit'],target)==(8,0,0x1047bda74)
 elif i in [4,5]:
  assert w&0xffc00000==0x2d400000;imm=(w>>15)&127;imm=imm-128 if imm&64 else imm;d.update(kind='LDP scalar S pair offset',width_each_bits=32,rt=w&31,rt2=(w>>10)&31,rn=(w>>5)&31,byte_offset=imm*4);assert(d['rt'],d['rt2'],d['rn'],d['byte_offset'])==((0,1,1,0) if i==4 else (2,3,0,0))
 else:
  assert w&0xffe0fc00==0x1e200800;d.update(kind='FMUL scalar S',width_bits=32,rd=w&31,rn=(w>>5)&31,rm=(w>>16)&31);assert(d['rd'],d['rn'],d['rm'])==((2,0,2) if i==6 else (1,1,3))
 actual.append(d)
author=json.loads(A.read_text());assert actual==author['all8_author_native_fields'];after=[pin(p) for p in paths];assert before==after
known={x['path'] for x in outer};extras=[x for x in before if x['path'] not in known]
out=B/'reviews/utility-mute-core-prefix-static-actual-review-evidence.json'
with out.open('x') as f:json.dump(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_manifest=pin(D/'manifest.json'),outer_manifest=pin(H/'manifest.json'),author=pin(A),watch_source=pin(H/'before-map.json'),watch_extra=extras,watch_count=len(paths),watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),before_after_exact=True,retained_inner_pairs=len(inner),retained_outer_pairs=len(outer),inventories=dict(preparation=8,actual=10,outer=11),image=plan['image'],header_hex=header.hex(),loadcommands_sha256=hashlib.sha256(commands).hexdigest(),mapping=maps[0],file_offset=off,raw_sha256=hashlib.sha256(raw).hexdigest(),all8_independent_fields=actual,author_fields_exact=True,one_attempt_pid_accounting=True,wrapper_exact_four_literal_changes=True,supplied_tools_rerun=False,new_selected_bytes=32,other_words_or_destinations_read=0),f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=pin(out),watch=len(paths),rows=8,bytes=32)))
