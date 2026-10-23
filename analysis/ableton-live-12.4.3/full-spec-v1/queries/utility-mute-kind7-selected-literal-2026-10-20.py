"""One selected literal-byte read, conditional on exact C-string section metadata."""
from pathlib import Path
import datetime,hashlib,json,struct
ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
STEM=BASE/'queries/utility-mute-kind7-selected-literal-2026-10-20'
Q=STEM.with_suffix('.json');RAW=STEM.with_suffix('.bin');METHOD=STEM.with_suffix('.py')
PARENT=BASE/'queries/utility-mute-kind7-referenced-words-frontier-2026-10-20.json'
REVIEW=BASE/'reviews/utility-mute-kind7-referenced-words-review.json'
IMAGE=ROOT/'analysis/ableton-live-12.4.3/derived/Live.arm64'
TARGET=0x105879dcd

def ident(p):
 digest=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk)
 return dict(path=str(p),bytes=p.stat().st_size,sha256=digest.hexdigest())

def main():
 assert not any(p.exists() for p in (Q,RAW,METHOD))
 parent=json.loads(PARENT.read_text());review=json.loads(REVIEW.read_text())
 assert ident(PARENT)['sha256']=='36b23a4ea7818c6ea231b6c88c476084a649806ca61c098e2e414df49f08a921'
 assert ident(REVIEW)['sha256']=='c5184317c1910946f0145b9c5d48d6dbf3f9054e86680de8ca8249b97cfcb2fa'
 assert review['reviewed_query']==ident(PARENT)
 assert parent['block']['words'][1]['u64_little_endian']==hex(TARGET)
 pins={Path(r['path']) for r in parent['preservation']['before']}|{PARENT,REVIEW,Path(parent['retained_raw']['path'])}
 before=[ident(p) for p in sorted(pins)]
 for r in parent['preservation']['before']:assert ident(Path(r['path']))==r
 assert ident(IMAGE)==parent['image']
 assert parent['image']['bytes']==149711904 and parent['image']['sha256']=='3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
 sections=[];segments=[];command_rows=[]
 with IMAGE.open('rb',buffering=0) as f:
  header=f.read(32);values=struct.unpack('<8I',header)
  assert values==(0xfeedfacf,0x100000c,0,2,53,6944,0xa18085,0)
  commands=f.read(values[5]);assert header.hex()==parent['header']['raw_hex']
  assert hashlib.sha256(commands).hexdigest()==parent['load_commands']['sha256']
  cursor=0
  for index in range(values[4]):
   command,size=struct.unpack_from('<II',commands,cursor)
   assert size>=8 and cursor+size<=len(commands)
   command_rows.append(dict(index_0based=index,file_offset=32+cursor,command=hex(command),cmdsize=size))
   if command==0x19:
    name,va,vs,fo,fs,mp,ip,ns,flags=struct.unpack_from('<16sQQQQiiII',commands,cursor+8)
    name=name.rstrip(b'\0').decode('ascii');assert size==72+80*ns and fo+fs<=IMAGE.stat().st_size
    seg=dict(command_index_0based=index,command_file_offset=32+cursor,name=name,vmaddr=hex(va),vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=flags)
    segments.append(seg)
    for si in range(ns):
     pos=cursor+72+80*si
     sn,sg,sv,ss,so,al,ro,nr,sf,r1,r2,r3=struct.unpack_from('<16s16sQQIIIIIIII',commands,pos)
     sn=sn.rstrip(b'\0').decode('ascii');sg=sg.rstrip(b'\0').decode('ascii')
     sections.append(dict(segment=name,section=sn,section_segment=sg,va=hex(sv),size=ss,file_offset=so,flags=hex(sf),type_low8=sf&255,command_index=index,section_index_0based=si,header_file_offset=32+pos,raw80_hex=commands[pos:pos+80].hex()))
   cursor+=size
  assert cursor==len(commands) and segments==parent['load_commands']['segments'] and command_rows==parent['load_commands']['command_metadata']
  sms=[s for s in segments if int(s['vmaddr'],16)<=TARGET<int(s['vmaddr'],16)+min(s['vmsize'],s['filesize'])]
  candidates=[s for s in sections if int(s['va'],16)<=TARGET<int(s['va'],16)+s['size']]
  result=dict(status='STOP_MAPPING_ONLY',target=hex(TARGET),unique_filebacked_segment_matches=len(sms),section_coordinate_matches=len(candidates),string_read=False,raw_bytes=0,reason='Requires unique fully file-backed S_CSTRING_LITERALS section; metadata only if unavailable.')
  raw=b''
  if len(sms)==1 and len(candidates)==1:
   s=candidates[0];seg=sms[0];sv=int(s['va'],16);gv=int(seg['vmaddr'],16)
   section_full=s['segment']==s['section_segment']==seg['name'] and gv<=sv and sv+s['size']<=gv+min(seg['vmsize'],seg['filesize']) and s['file_offset']==seg['fileoff']+sv-gv and s['file_offset']+s['size']<=IMAGE.stat().st_size
   result.update(selected_section=s,selected_segment=seg,entire_section_file_backed_and_mapping_agrees=section_full)
   if section_full and s['type_low8']==2:
    offset=s['file_offset']+TARGET-sv
    cap=min(256,sv+s['size']-TARGET)
    assert cap>0 and offset==seg['fileoff']+TARGET-gv and offset+cap<=IMAGE.stat().st_size
    f.seek(offset)
    pieces=[];terminated=False
    for i in range(cap):
     byte=f.read(1);assert len(byte)==1;pieces.append(byte)
     if byte==b'\0':terminated=True;break
    raw=b''.join(pieces);prefix=raw[:-1] if terminated else raw
    escaped=''.join(chr(v) if 32<=v<=126 and v!=92 else '\\x%02x'%v for v in prefix)
    result.update(status='RETAINED_LITERAL_BYTES_ONLY' if terminated else 'STOP_UNTERMINATED_LITERAL_UNKNOWN',string_read=True,file_offset=offset,read_cap=cap,raw_bytes=len(raw),raw_hex=raw.hex(),raw_sha256=hashlib.sha256(raw).hexdigest(),prefix_ascii_escaped=escaped,first_NUL_found=terminated,terminator_index_0based=len(raw)-1 if terminated else None,consumed_includes_terminator=terminated,end_va_exclusive=hex(TARGET+len(raw)),reason='Stopped at firstNUL.' if terminated else 'Stopped at256Bcap or sectionend; no text termination/meaning conclusion.',no_later_bytes_read=True,unbuffered_byte_reads=True)
 after=[ident(p) for p in sorted(pins)];assert before==after
 with METHOD.open('xb') as f:f.write(Path(__file__).read_bytes())
 if result['string_read']:
  with RAW.open('xb') as f:f.write(raw)
 report=dict(retained_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),selection='Only selected value105879dcd: metadata first, then unbuffered bytewise until firstNUL/256/sectionend if eligible.',source_export_utc=None,parent_query=ident(PARENT),parent_review=ident(REVIEW),selected_parent_pointer='/block/words/1/u64_little_endian',image=ident(IMAGE),header=dict(raw_hex=header.hex(),bytes=32,sha256=hashlib.sha256(header).hexdigest()),load_commands=dict(bytes=len(commands),sha256=hashlib.sha256(commands).hexdigest(),commands_checked=53,command_metadata=command_rows),mapping=result,method=ident(METHOD),raw=ident(RAW) if result['string_read'] else None,preservation=dict(before=before,after=after,unchanged=True),limits=['Literal bytes only, no RTTI/type-name/demangledclass/object/layout/runtime identity or role inference.','No0x10follow, other string, target body/neighbor/opcode/decoder/native/runtime read or execution.','Underlying source pointer/image correspondence and actual runtime relocation/validity remain unknown; no public Mute behavior, new case or grade.'],actual_expected=None,comparison=None,new_cases_or_grades=0,complete=False)
 with Q.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps(dict(query=ident(Q),method=ident(METHOD),raw=report['raw'],mapping=result,watched=len(pins),unchanged=True),indent=2))

if __name__=='__main__':main()
