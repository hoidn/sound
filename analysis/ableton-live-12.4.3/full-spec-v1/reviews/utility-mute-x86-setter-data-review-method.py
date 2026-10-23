from pathlib import Path
import datetime,hashlib,json,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');D=B/'depth-utility-mute-x86-setter-data'
def pin(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x);n+=len(x)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
old=json.loads((D/'before-map.json').read_text());assert old==json.loads((D/'after-map.json').read_text());paths=sorted({Path(x['path']) for x in old}|{p for p in D.iterdir() if p.is_file()});before=[pin(p) for p in paths]
for x in old:assert pin(Path(x['path']))==x
m=json.loads((D/'manifest.json').read_text());assert {x['path'] for x in m['files']}=={p.name for p in D.iterdir() if p.is_file() and p.name!='manifest.json'}
for x in m['files']:
 q=pin(D/x['path']);assert(q['bytes'],q['sha256'])==(x['bytes'],x['sha256'])
sel=json.loads((D/'selection.json').read_text());assert sel['va']=='0x104b8c760' and sel['length']==8 and pin(Path(sel['method']['path']))==sel['method'] and pin(Path(sel['peer']['path']))==sel['peer']
metadata=json.loads(Path(old[1]['path']).read_text());image=Path(old[0]['path']);assert pin(image)==old[0];va=0x104b8c760
with image.open('rb') as f:
 hdr=f.read(32);v=struct.unpack('<IiiIIIII',hdr);assert hdr.hex()==metadata['header_hex'] and v[:3]==(0xfeedfacf,0x1000007,3) and v[4:6]==(54,6832)
 cmds=f.read(v[5]);assert hashlib.sha256(cmds).hexdigest()==metadata['load_commands_sha256'];at=0;segments=[]
 for _ in range(v[4]):
  c,n=struct.unpack_from('<II',cmds,at);assert n>=8 and at+n<=len(cmds)
  if c==0x19:
   name,addr,vs,off,fs,mp,ip,ns,flags=struct.unpack_from('<16sQQQQiiII',cmds,at+8);segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=addr,vmsize=vs,fileoff=off,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=flags))
  at+=n
 assert at==len(cmds) and segments==metadata['segments'];maps=[s for s in segments if s['vmaddr']<=va and va+8<=s['vmaddr']+min(s['filesize'],s['vmsize'])];assert maps==[metadata['selected_segment']];off=maps[0]['fileoff']+va-maps[0]['vmaddr'];assert off==0x4b8c760;f.seek(off);raw=f.read(8)
assert raw.hex()=='554889e54088b7cf';r=json.loads((D/'result.json').read_text());assert r['bytes']==raw.hex() and r['analysis']['pattern']=='UNKNOWN; stop without expansion'
# Independent literal controls on own synthetic data, without invoking supplied pattern().
valid=bytes.fromhex('4088b7cf000000c3');badret=bytes.fromhex('4088b7cf000000c2');badwidth=bytes.fromhex('4889b7cf000000c3');assert len(valid)==8 and valid[:3]==b'\x40\x88\xb7' and valid[7:]==b'\xc3' and struct.unpack('<i',valid[3:7])[0]==207;assert badret[7:]!=b'\xc3' and badwidth[:3]!=b'\x40\x88\xb7';assert raw[:3]!=valid[:3]
assert raw[:1]==b'\x55' and raw[1:4]==b'\x48\x89\xe5';assert raw[4]==0x40 and raw[5]==0x88 and raw[6]>>6==2
# Only one of four disp32 bytes is present after the REX/opcode/ModRM; do not construct missing bytes.
assert len(raw[7:])==1
assert before==[pin(p) for p in paths]
out=B/'reviews/utility-mute-x86-setter-data-review-evidence.json'
with out.open('x') as f:json.dump(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),watch=before,watch_count=len(paths),unchanged=True,retained_pairs=5,manifest=pin(D/'manifest.json'),header_hex=hdr.hex(),ncmds=54,sizeofcmds=6832,mapping=maps[0],va=hex(va),offset=off,raw_hex=raw.hex(),raw_sha256=hashlib.sha256(raw).hexdigest(),classification='UNKNOWN as retained; stop',complete_instructions=[dict(address=hex(va),bytes='55',kind='PUSH RBP'),dict(address=hex(va+1),bytes='4889e5',kind='MOV RBP,RSP')],incomplete_prefix=dict(address=hex(va+4),bytes='4088b7cf',status='Incomplete instruction; remaining displacement unread'),independent_synthetic_controls=3,supplied_method_or_tool_run=False,original_execution=False,other_word_reads=0),f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=pin(out),watch=len(paths),UNKNOWN=True)))
