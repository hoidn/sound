from pathlib import Path
import json,hashlib,struct,datetime
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');D=B/'depth-corpus-x86-receiver-setup-table-word';R=B/'reviews';method=R/'corpus-x86-receiver-setup-table-word-read.py';rootselect=R/'corpus-x86-receiver-setup-table-word-root-selection.json'
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for r in iter(lambda:f.read(1048576),b''):n+=len(r);h.update(r)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def load(p):return json.loads(p.read_text())
oldmap=load(D/'before-map.json');assert len(oldmap)==5 and oldmap==load(D/'after-map.json')
selection=load(rootselect);parent=Path(selection['parent']['path']);assert ident(parent)==selection['parent'];assert ident(method)==selection['method'];s=method.read_text()
for a,b in reversed(selection['operations']):assert s.count(b)==1;s=s.replace(b,a)
assert s==parent.read_text() and len(selection['operations'])==6
paths=sorted({Path(x['path']) for x in oldmap}|set(D.iterdir())|{rootselect,parent});before=[ident(p) for p in paths]
for x in oldmap:assert ident(Path(x['path']))==x
manifest=load(D/'manifest.json');assert len(manifest['files'])==4 and {x['path'] for x in manifest['files']}=={p.name for p in D.iterdir() if p.name!='manifest.json'}
for x in manifest['files']:
 g=ident(D/x['path']);assert(g['bytes'],g['sha256'])==(x['bytes'],x['sha256'])
image=Path(oldmap[0]['path']);m=load(Path(oldmap[1]['path']));assert ident(image)['bytes']==250352 and ident(image)['sha256']=='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
# Fresh header/load commands only, plus the sole selected8B. No neighbors/body/target follow.
with image.open('rb') as f:
 h=f.read(32);v=struct.unpack('<IiiIIIII',h);assert v[:3]==(0xfeedfacf,0x1000007,3) and v[4:6]==(14,1696) and h.hex()==m['header_hex'];commands=f.read(v[5]);assert commands.hex()==m['load_commands_hex'] and hashlib.sha256(commands).hexdigest()==m['load_commands_sha256']
 cursor=0;segments=[]
 for _ in range(v[4]):
  cmd,n=struct.unpack_from('<II',commands,cursor);assert n>=8 and cursor+n<=len(commands)
  if cmd==0x19:
   name,va,vs,fo,fs,mp,ip,ns,fl=struct.unpack_from('<16sQQQQiiII',commands,cursor+8);segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=fl))
  cursor+=n
 assert cursor==1696 and segments==m['segments'];c=[s for s in segments if s['vmaddr']<=0x30638 and 0x30640<=s['vmaddr']+s['filesize']];assert len(c)==1 and c[0]['name']=='__DATA';off=c[0]['fileoff']+0x30638-c[0]['vmaddr'];assert off==0x30638;f.seek(off);raw=f.read(8)
assert raw.hex()=='b03a000000000000';value=int.from_bytes(raw,'little');assert value==0x3ab0
result=load(D/'result.json');assert result['raw_hex']==raw.hex() and result['unsigned_little64']==hex(value) and result['va']=='0x30638' and result['decoder_children']==result['original_calls']==0
assert int(load(D/'selection.json')['nominal_firstword'],16)+int(load(D/'selection.json')['slot'],16)==0x30638
for raw_control,expected in [(b'\0'*8,0),(b'\x01'+b'\0'*7,1),(b'\xff'*8,2**64-1)]:assert int.from_bytes(raw_control,'little')==expected
assert before==[ident(p) for p in paths]
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS selected8B data only',manifest=ident(D/'manifest.json'),method=ident(method),selection=ident(rootselect),six_literal_inverse=True,paired_inputs=5,header=dict(bytes=32,ncmds=14,sizeofcmds=1696,load_commands_sha256=hashlib.sha256(commands).hexdigest()),mapping=dict(va='0x30638',end='0x30640',fileoff=hex(off),segment=c[0]),raw_hex=raw.hex(),raw_sha256=hashlib.sha256(raw).hexdigest(),unsigned_little64=hex(value),le_controls=3,before=before,after=[ident(p) for p in paths],unchanged=True,tool_or_original_execution=False,pointed_target_followed=False)
p=R/'corpus-x86-receiver-setup-table-word-review-evidence.json'
with p.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=ident(p),watched=len(paths),raw_hex=raw.hex(),value=hex(value),manifest=ident(D/'manifest.json')),indent=2))
