from pathlib import Path
import datetime,hashlib,json,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');D=B/'depth-utility-mute-core-return-word'
def pin(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x);n+=len(x)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
old=json.loads((D/'before-map.json').read_text());assert old==json.loads((D/'after-map.json').read_text());paths={Path(x['path']) for x in old}|{p for p in D.iterdir() if p.is_file()}|{B/'reviews/utility-mute-calcmain-static-actual-review.json'};paths=sorted(paths);before=[pin(p) for p in paths]
for x in old:assert pin(Path(x['path']))==x
m=json.loads((D/'manifest.json').read_text());assert {v['path'] for v in m['files']}=={p.name for p in D.iterdir() if p.is_file() and p.name!='manifest.json'}
for v in m['files']:
 a=pin(D/v['path']);assert(a['bytes'],a['sha256'])==(v['bytes'],v['sha256'])
image=Path(old[0]['path']);assert pin(image)==old[0];va=0x1047bda74
with image.open('rb') as f:
 hdr=f.read(32);fields=struct.unpack('<IiiIIIII',hdr);assert fields[0]==0xfeedfacf and fields[1]==0x100000c and fields[4:6]==(53,6944)
 commands=f.read(fields[5]);assert hashlib.sha256(commands).hexdigest()=='b37084be6877bd6f3afdfea02c3277f04ace94bd551750842397c48fb4ea3fc7';at=0;segments=[]
 for _ in range(fields[4]):
  cmd,n=struct.unpack_from('<II',commands,at);assert n>=8 and at+n<=len(commands)
  if cmd==0x19:
   name,vaddr,vs,off,fs,mp,ip,ns,flags=struct.unpack_from('<16sQQQQiiII',commands,at+8);segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=vaddr,vmsize=vs,fileoff=off,filesize=fs,maxprot=mp,initprot=ip))
  at+=n
 assert at==len(commands);maps=[s for s in segments if s['vmaddr']<=va and va+4<=s['vmaddr']+min(s['vmsize'],s['filesize'])];assert len(maps)==1 and maps[0]['name']=='__TEXT';off=maps[0]['fileoff']+va-maps[0]['vmaddr'];assert off==0x47bda74;f.seek(off);raw=f.read(4)
assert raw==(D/'word.bin').read_bytes() and raw.hex()=='c0035fd6';w=struct.unpack('<I',raw)[0];assert w&0xfffffc1f==0xd65f0000 and (w>>5)&31==30;assert 0xd61f03c0&0xfffffc1f!=0xd65f0000
r=json.loads((D/'result.json').read_text());assert r['word']==hex(w) and r['RET_encoding'] and r['RET_Rn']==30 and r['file_offset']==off
peer=json.loads((B/'reviews/utility-mute-calcmain-static-actual-review.json').read_text());assert peer['required_findings']==[] and peer['independent_verification']['BL_target']=='0x1047bd790'
after=[pin(p) for p in paths];assert before==after
out=B/'reviews/utility-mute-core-return-word-review-evidence.json'
with out.open('x') as f:json.dump(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),watch=before,watch_count=len(paths),unchanged=True,retained_pairs=len(old),inventory_payloads=5,tree=6,image=old[0],header_hex=hdr.hex(),ncmds=53,sizeofcmds=6944,commands_sha256=hashlib.sha256(commands).hexdigest(),unique_mapping=maps[0],va=hex(va),offset=off,raw_hex=raw.hex(),word=hex(w),mask='0xfffffc1f',RET_base='0xd65f0000',Rn=30,BR_counterexample_rejected=True,supplied_method_run=False,decoder_or_original_processes=0,other_data_bytes_or_target_follow=0),f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=pin(out),watch=len(paths),RET_Rn=30)))
