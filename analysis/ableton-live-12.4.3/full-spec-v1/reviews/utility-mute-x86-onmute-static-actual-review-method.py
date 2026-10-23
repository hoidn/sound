from pathlib import Path
import datetime,hashlib,json,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-utility-mute-x86-onmute-entry-preparation';D=B/'depth-utility-mute-x86-onmute-entry-instructions';H=B/'reviews/utility-mute-x86-onmute-entry-selected-execution';A=B/'reviews/utility-mute-x86-onmute-entry-root-assessment.json'
def pin(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x);n+=len(x)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
inner=json.loads((D/'before-map.json').read_text())['files'];outer=json.loads((H/'before-map.json').read_text());paths=sorted({Path(x['path']) for x in inner+outer}|{x for q in [P,D,H] for x in q.iterdir() if x.is_file()}|{A});before=[pin(p) for p in paths]
assert pin(D/'manifest.json')['sha256']=='68b0674190d32a05bcbc2b61c746542ea0f6ea1ddade9ec36c8abded3b1932d9';assert pin(H/'manifest.json')['sha256']=='e703eaf20c155cd1997637dc396e1c90e21343b3c34d283af3e606ce3ba9d541'
assert inner==json.loads((D/'after-map.json').read_text())['files'] and outer==json.loads((H/'after-map.json').read_text());assert len(inner)==52 and len(outer)==3495
for x in inner+outer:assert pin(Path(x['path']))==x
for q in [P,D,H]:
 m=json.loads((q/'manifest.json').read_text());assert {x['path'] for x in m['files']}=={x.name for x in q.iterdir() if x.is_file() and x.name!='manifest.json'}
 for x in m['files']:
  a=pin(q/x['path']);assert (a['bytes'],a['sha256'])==(x['bytes'],x['sha256'])
sel=json.loads((H/'selection.json').read_text());s=(H/'execute-selected-once.py').read_text()
for op in reversed(sel['wrapper_literal_delta']):assert s.count(op['new'])==op['count'];s=s.replace(op['new'],op['old'])
assert s==Path(sel['wrapper_parent']['path']).read_text() and len(sel['wrapper_literal_delta'])==9
for key in ['preparation','collector','root_preflight','peer_preflight','wrapper','wrapper_parent']:assert pin(Path(sel[key]['path']))==sel[key]
assert (D/'collect-once.py').read_bytes()==(P/'collect-once.py').read_bytes()
for x in json.loads((H/'pins.json').read_text()):assert pin(Path(x['path']))==x
status=json.loads((D/'status.json').read_text());receipt=json.loads((H/'receipt.json').read_text());assert json.loads((H/'collector.stdout.json').read_text())==status
assert status['attempted_decoder_children']==status['returned_pid_children']==1 and status['exit']==0 and not status['exception'] and status['providers_unchanged'];assert receipt['attempted_collector_launches']==1 and receipt['exit']==0 and not receipt['exception'] and not receipt['timeout']
assert (D/'onmute-entry-240.stderr').stat().st_size==(H/'collector.stderr').stat().st_size==0
meta=json.loads((P/'header-map.json').read_text());image=Path(meta['image']['path']);assert pin(image)==meta['image'];start=0x10224e760
with image.open('rb') as f:
 header=f.read(32);v=struct.unpack('<IiiIIIII',header);assert header.hex()==meta['header_hex'] and v[:3]==(0xfeedfacf,0x1000007,3) and v[4:6]==(54,6832)
 commands=f.read(v[5]);assert hashlib.sha256(commands).hexdigest()==meta['load_commands_sha256'];at=0;segments=[]
 for _ in range(v[4]):
  cmd,size=struct.unpack_from('<II',commands,at);assert size>=8 and at+size<=len(commands)
  if cmd==0x19:
   name,va,vs,fo,fs,mp,ip,ns,fl=struct.unpack_from('<16sQQQQiiII',commands,at+8);segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=fl))
  at+=size
 assert at==len(commands) and segments==meta['segments'];maps=[x for x in segments if x['vmaddr']<=start and start+240<=x['vmaddr']+min(x['vmsize'],x['filesize'])];assert maps==[meta['selected_segment']];offset=maps[0]['fileoff']+start-maps[0]['vmaddr'];assert offset==0x224e760;f.seek(offset);raw=f.read(240)
assert raw==(D/'onmute-entry-240.bin').read_bytes() and hashlib.sha256(raw).hexdigest()=='95a6a34d9e5d369b2e0e8b5e9a7b67a4c4e0c57b60e9969560ad9924bd5b4a59'
# Entire selected raw is compared/hashed; only the following55B occupied prefix is interpreted.
rows=json.loads((D/'onmute-entry-240.stdout.json').read_text());assert len(rows)==16;cursor=start;pieces=[]
for row in rows:
 b=bytes.fromhex(row['bytes']);assert type(row['offset']) is int and row['offset']==cursor and type(row['size']) is int and 1<=row['size']<=15 and len(b)==row['size'];cursor+=len(b);pieces.append(b)
assert cursor==0x10224e797 and b''.join(pieces)==raw[:55];prefix=raw[:55]
expected=['55','4889e5','0f57c9','0f2ec1','0f9ac0','0f95c1','08c1','888f61010000','80bf6201000001','7506','5d','e91997ffff','f30fc2c104','660f7ec6','83e601','4883c748']
assert [x.hex() for x in pieces]==expected
fields=[]
for i,b in enumerate(pieces):
 d=dict(index=i,offset=hex(rows[i]['offset']),bytes=b.hex(),size=len(b))
 if i in [0,10]:d.update(kind='PUSH register64' if i==0 else 'POP register64',register=(b[0]&7));assert d['register']==5
 elif i==1:assert b[0]==0x48 and b[1]==0x89;d.update(kind='MOV reg64 fromreg64',REX_W=1,mod=b[2]>>6,source_reg=(b[2]>>3)&7,dest_rm=b[2]&7);assert(d['mod'],d['source_reg'],d['dest_rm'])==(3,4,5)
 elif i in [2,3,4,5,6,12,13,14,15]:
  modindex={2:2,3:2,4:2,5:2,6:1,12:3,13:3,14:1,15:2}[i];m=b[modindex];d.update(mod=m>>6,reg_or_group=(m>>3)&7,rm=m&7);assert d['mod']==3
  assert (d['reg_or_group'],d['rm'])=={2:(1,1),3:(0,1),4:(0,0),5:(0,1),6:(0,1),12:(0,1),13:(0,6),14:(4,6),15:(0,7)}[i]
  d['kind']={2:'XORPS XMM1,XMM1',3:'UCOMISS XMM0,XMM1',4:'SETP AL (PF)',5:'SETNE CL (notZF)',6:'OR CL,AL byte',12:'CMPSS XMM0,XMM1 immediate4',13:'MOVD ESI fromlow32XMM0',14:'AND ESI immediate1',15:'ADD RDI immediate0x48'}[i]
  if i in [12,14,15]:d['immediate8']=b[-1]
  if i==15:d['REX_W']=1
 elif i in [7,8]:
  m=b[1];d.update(mod=m>>6,reg_or_group=(m>>3)&7,base_rm=m&7,disp32=struct.unpack_from('<i',b,2)[0],kind='MOV byte [RDI+disp],CL' if i==7 else 'CMP byte [RDI+disp],imm8');assert d['mod']==2 and d['base_rm']==7
  if i==8:d['imm8']=b[-1];assert d['reg_or_group']==7 and d['imm8']==1
  else:assert d['reg_or_group']==1
 elif i in [9,11]:
  disp=struct.unpack('<b',b[1:])[0] if i==9 else struct.unpack('<i',b[1:])[0];d.update(kind='JNE rel8' if i==9 else 'JMP rel32',displacement=disp,target=hex(rows[i]['offset']+len(b)+disp),fallthrough=hex(rows[i]['offset']+len(b)));assert d['target']==('0x10224e787' if i==9 else '0x102247ea0');assert rows[i]['jump']==int(d['target'],16)
 fields.append(d)
assert fields[7]['disp32']==0x161 and fields[8]['disp32']==0x162
coverage=json.loads((D/'prefix-coverage.json').read_text());assert coverage['consumed_bytes']==55 and coverage['uninterpreted_selected_bytes']==185 and coverage['body_extent_claim'] is False
assert before==[pin(p) for p in paths];known={x['path'] for x in outer};extras=[x for x in before if x['path'] not in known]
out=B/'reviews/utility-mute-x86-onmute-static-actual-review-evidence.json'
with out.open('x') as f:json.dump(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual=pin(D/'manifest.json'),outer=pin(H/'manifest.json'),assessment=pin(A),watch_source=pin(H/'before-map.json'),watch_extra=extras,watch_count=len(paths),watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),unchanged=True,retained_inner_pairs=52,retained_outer_pairs=3495,wrapper_exact9literalinverse=True,wholeimage=meta['image'],header=header.hex(),ncmds=54,sizeofcmds=6832,mapping=maps[0],file_offset=offset,selected240_sha256=hashlib.sha256(raw).hexdigest(),occupied_prefix_bytes=55,opaque_suffix_bytes=185,all16_manual_fields=fields,branch_targets_only=['0x10224e787','0x102247ea0'],destinations_followed=False,supplied_tools_replayed=False,original_execution=False),f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=pin(out),watch=len(paths),prefix=55,suffix_opaque=185)))
