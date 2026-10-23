"""Selected physical64B DATA read and eight exact export metadata lookups only."""
from pathlib import Path
import datetime, hashlib, json, struct
ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
QUERY=BASE/'queries/utility-mute-kind7-dispatch-continuation-2026-10-20.json'
RAW=QUERY.with_suffix('.bin')
METHOD=QUERY.with_suffix('.py')
PRIOR=BASE/'queries/utility-mute-kind7-dispatch-block-frontier-2026-10-20.json'
REVIEW=BASE/'reviews/utility-mute-kind7-dispatch-block-review.json'
IMAGE=ROOT/'analysis/ableton-live-12.4.3/derived/Live.arm64'
MANIFEST=Path('/var/tmp/sound-analysis/corpus/indexes/manifest.json')
START,END=0x1067938e0,0x106793920

def identity(path):
 digest=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):digest.update(block)
 return dict(path=str(path),bytes=path.stat().st_size,sha256=digest.hexdigest())

def selected_metadata(entry):
 files=sorted(Path('/var/tmp/sound-analysis/corpus/decomp/chunks').glob('chunk-*.jsonl'))
 lo,hi=0,len(files)
 # First-entry coordinates only; no body text is retained or semantically read.
 while lo<hi:
  mid=(lo+hi)//2
  with files[mid].open('rb') as f:record=json.loads(f.readline())
  if int(record['entry'],16)<=entry:lo=mid+1
  else:hi=mid
 if lo == 0:
  return dict(exact_entry=hex(entry),status="Below first retained entry coordinate; no matching metadata selected, not no-function proof.")
 path=files[lo-1];before=identity(path)
 matches=[]
 with path.open('rb') as f:
  for line,raw in enumerate(f,1):
   record=json.loads(raw)
   if int(record['entry'],16)==entry:
    raw=raw[:-1] if raw.endswith(b'\n') else raw
    keys=('entry','name','signature','thunk','state','error','timed_out','partial_code','warnings','code_bytes','code_sha256')
    matches.append(dict(provider=before,line_1based=line,raw_row_bytes_excluding_LF=len(raw),raw_row_sha256_excluding_LF=hashlib.sha256(raw).hexdigest(),metadata={k:record.get(k) for k in keys},body_text_retained=False,body_text_semantically_read=False))
 assert identity(path)==before
 assert len(matches)<=1
 return matches[0] if matches else dict(exact_entry=hex(entry),status='No exact row in selected containing chunk; not no-function proof.',provider=before)

def main():
 assert not any(p.exists() for p in (QUERY,RAW,METHOD))
 prior=json.loads(PRIOR.read_text());review=json.loads(REVIEW.read_text())
 assert prior['selection']['end_va_exclusive']==hex(START)
 expected=prior['preservation']['before']
 paths={ROOT/r['path'] if not Path(r['path']).is_absolute() else Path(r['path']) for r in expected}|{PRIOR,REVIEW,MANIFEST}
 before=[identity(p) for p in sorted(paths)]
 assert identity(IMAGE)['sha256']=='3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
 assert IMAGE.stat().st_size==149711904
 for row in expected:
  p=ROOT/row['path'] if not Path(row['path']).is_absolute() else Path(row['path'])
  got=identity(p);assert (got['bytes'],got['sha256'])==(row['bytes'],row['sha256'])
 with IMAGE.open('rb') as f:
  header=f.read(32);values=struct.unpack('<IiiIIIII',header)
  assert values==(0xfeedfacf,0x100000c,0,2,53,6944,0xa18085,0)
  commands=f.read(values[5]);assert hashlib.sha256(commands).hexdigest()==prior['load_commands']['sha256']
  assert header.hex()==prior['header']['raw_hex']
  segments=[];cursor=0
  for i in range(values[4]):
   command,size=struct.unpack_from('<II',commands,cursor);assert size>=8 and cursor+size<=len(commands)
   if command==0x19:
    name,va,vs,fo,fs,mp,ip,ns,fl=struct.unpack_from('<16sQQQQiiII',commands,cursor+8)
    assert fo+fs<=IMAGE.stat().st_size
    segments.append(dict(command_index_0based=i,command_file_offset=cursor+32,name=name.rstrip(b'\0').decode(),vmaddr=hex(va),vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=fl))
   cursor+=size
  assert cursor==len(commands) and segments==prior['load_commands']['segments']
  matched=[s for s in segments if int(s['vmaddr'],16)<=START and END<=int(s['vmaddr'],16)+min(s['vmsize'],s['filesize'])]
  assert len(matched)==1 and matched[0]['name']=='__DATA_CONST'
  offset=matched[0]['fileoff']+START-int(matched[0]['vmaddr'],16)
  assert offset==108607712 and offset+64<=IMAGE.stat().st_size
  f.seek(offset);raw=f.read(64)
 assert len(raw)==64
 words=[]
 for i in range(8):
  piece=raw[8*i:8*i+8];value=struct.unpack('<Q',piece)[0]
  words.append(dict(physical_word_index_0based=i,va=hex(START+8*i),file_offset=offset+8*i,raw_hex=piece.hex(),u64_little_endian=hex(value),metadata_lookup=selected_metadata(value),role='Unclassified physical word; no slot or callable semantics assigned.'))
 after=[identity(p) for p in sorted(paths)];assert before==after
 result=dict(retained_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PARTIAL_PHYSICAL64B_AND_EIGHT_EXACT_METADATA_ONLY_PENDING_ROOT_REVIEW',selection=dict(start_va=hex(START),end_va_exclusive=hex(END),bytes=64,word_count=8,scope='Fixed physical continuation only; not table extent, slot roles, callability or same-class proof.'),image=identity(IMAGE),header=prior['header'],load_commands=dict(bytes=len(commands),sha256=hashlib.sha256(commands).hexdigest(),commands_checked=53,all_boundaries_exact=True,segments=segments),mapping=dict(segment=matched[0],file_offset=offset,end_file_offset_exclusive=offset+64,unique_file_backed_matches=1,no_zero_fill=True),block=dict(raw_file=str(RAW),bytes=64,sha256=hashlib.sha256(raw).hexdigest(),raw_hex=raw.hex(),words=words),source_context=dict(prior_query=identity(PRIOR),prior_review=identity(REVIEW),original_firstword_literal='0x1067938a0',association=prior['conditional_construction_association'],limit='Previous source firstwordstore is conditional context only; adjacent physical continuation does not prove same runtime object/table.'),index_manifest=identity(MANIFEST),metadata_scope='Only eight exact entry metadata matches. Binary search inspects navigation first-entry coordinates; selected row code fields are omitted without body-text semantic read. No alias/callee/target/body expansion.',preservation=dict(before=before,after=after,unchanged=True),source_export_utc=None,limits=['No decoder/opcode/instruction/native/runtime execution.','No actual runtime vptr/relocation/extent/dispatch/class identity or actual public Mute/model/processor behavior.','No missing exact metadata row establishes function or route absence.','Existing type/key/admission/helper/ABI and actual map/callback/unit/processor joins remain unknown.'],documentary_expected=None,actual_expected=None,comparison=None,new_normative_ids=0,new_cases_or_grades=0,complete=False)
 with RAW.open('xb') as f:f.write(raw)
 with METHOD.open('xb') as f:f.write(Path(__file__).read_bytes())
 with QUERY.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(dict(query=identity(QUERY),raw=identity(RAW),method=identity(METHOD),values=[r['u64_little_endian'] for r in words],watched=len(paths),unchanged=True),indent=2))

if __name__=='__main__':main()
