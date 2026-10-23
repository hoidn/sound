"""Two exact class-token predicates in pinned main Live x86 nlist; metadata only."""
from pathlib import Path
import datetime,hashlib,json,plistlib,struct
ROOT=Path('/home/ollie/Documents/sound');BASE=ROOT/'analysis/ableton-live-12.4.3';Q=BASE/'full-spec-v1/queries/utility-mute-x86-class-token-symbol-metadata-2026-10-20.json'
FAT=Path('/home/ollie/Ableton Live 12 Suite.app/Contents/MacOS/Live');THIN=Path('/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64');PLIST=FAT.parent.parent/'Info.plist'
SLICE=THIN.parent/'slice.json';X1=BASE/'r2/x1-extracted-exec-v1/manifest.json'
PREDICATES={'AStereoGain':(b'AStereoGain',),'OStereoGainProcessor':(b'OStereoGainProcessor',)};CAP=96
assert not Q.exists()
def sha(b):return hashlib.sha256(b).hexdigest()
def identity(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for raw in iter(lambda:f.read(1048576),b''):h.update(raw);n+=len(raw)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def bound(off,size,limit):assert 0<=off<=limit and 0<=size<=limit-off
context=[ROOT/'wiki/research/index.md',ROOT/'wiki/research/sources/ableton-live-12.4.3.md',ROOT/'wiki/research/artifacts/index.md',ROOT/'wiki/research/device-audio-utilities.md',ROOT/'wiki/research/extracted-execution.md',ROOT/'wiki/research/sources/apple-macho-format.md']
context_asof=[identity(p) for p in context]
providers=[FAT,THIN,PLIST,SLICE,X1,BASE/'full-spec-v1/queries/corpus-x86-selected-export-metadata-2026-10-20.py',BASE/'full-spec-v1/depth-apple-macho-format-source/nlist.h',BASE/'full-spec-v1/depth-apple-macho-format-source/manifest.json',Path(__file__).resolve(),BASE/'full-spec-v1/queries/utility-mute-x86-selected-symbol-metadata-2026-10-20.py',BASE/'full-spec-v1/queries/utility-mute-x86-selected-symbol-metadata-2026-10-20.json',BASE/'full-spec-v1/reviews/utility-mute-x86-selected-symbol-root-review.json',BASE/'full-spec-v1/queries/utility-public-binding-minimum-frontier-2026-10-20.json']
before=[identity(p) for p in providers]
assert before[0]['bytes']==313453600 and before[0]['sha256']=='52289af638f1b26590c84a9bc08eabdc35127883087057add909d2718a7a35ef'
assert before[1]['bytes']==163716848 and before[1]['sha256']=='1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0'
slice_record=json.loads(SLICE.read_text());assert slice_record['source_sha256']==before[0]['sha256'] and slice_record['slice_sha256']==before[1]['sha256'] and slice_record['slice_size']==163716848 and slice_record['slice_offset']==16384
assert json.loads(X1.read_text())['slice']['sha256']==before[1]['sha256']
plist=plistlib.loads(PLIST.read_bytes());assert plist['CFBundleShortVersionString']=='12.4.3 (2026-07-07_e3d8be4d07)' and plist['CFBundleExecutable']=='Live'
with FAT.open('rb') as f:
 fh=f.read(8);magic,na=struct.unpack('>II',fh);assert magic==0xcafebabe and na<=20
 ar=f.read(20*na);assert len(ar)==20*na
 arches=[]
 for i in range(na):
  cpu,sub,off,size,align=struct.unpack_from('>5I',ar,20*i);bound(off,size,before[0]['bytes']);assert align<64 and off%(1<<align)==0
  arches.append(dict(cpu=cpu,subtype=sub,offset=off,bytes=size,align_power2=align,raw_record_hex=ar[20*i:20*i+20].hex()))
 members=[x for x in arches if x['cpu']==0x01000007];assert len(members)==1 and members[0]['offset']==16384 and members[0]['bytes']==before[1]['bytes']
with THIN.open('rb') as f:
 header=f.read(32);magic,cpu,sub,typ,ncmds,lcbytes,flags,res=struct.unpack('<8I',header)
 assert magic==0xfeedfacf and cpu==0x01000007 and res==0 and ncmds==54 and lcbytes==6832 and ncmds<=lcbytes//8;bound(32,lcbytes,before[1]['bytes'])
 lc=f.read(lcbytes);assert len(lc)==lcbytes
 commands=[];segments=[];sections=[];symtabs=[];off=0
 for i in range(ncmds):
  cmd,n=struct.unpack_from('<II',lc,off);assert n>=8 and n%8==0;bound(off,n,len(lc));item=dict(index=i,command=hex(cmd),header_file_offset=32+off,bytes=n)
  if cmd==0x19:
   assert n>=72;name,vm,vs,fo,fs,mp,ip,ns,fl=struct.unpack_from('<16s4Q2i2I',lc,off+8);assert n==72+80*ns and fs<=vs and ip&~mp==0;bound(fo,fs,before[1]['bytes'])
   seg=dict(name=name.rstrip(b'\0').decode(),vmaddr=vm,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=fl);segments.append(seg)
   for j in range(ns):
    at=off+72+80*j;sn,sg,va,size,so,al,rel,nrel,sflags,r1,r2,r3=struct.unpack_from('<16s16s2Q8I',lc,at)
    sections.append(dict(ordinal=len(sections)+1,name=sn.rstrip(b'\0').decode(),segment=sg.rstrip(b'\0').decode(),address=va,size=size,file_offset=so,flags=sflags,alignment_power2=al,raw_section_hex=lc[at:at+80].hex()))
  elif cmd==2:
   assert n==24;so,nn,st,ss=struct.unpack_from('<4I',lc,off+8);bound(so,nn*16,before[1]['bytes']);bound(st,ss,before[1]['bytes']);symtabs.append(dict(command_index=i,symoff=so,nsyms=nn,stroff=st,strsize=ss,raw_command_hex=lc[off:off+n].hex()))
  commands.append(item);off+=n
 assert off==len(lc) and len(symtabs)==1
 sym=symtabs[0];assert sym['nsyms']==81311
 def mapping(off,size):
  hit=[x for x in segments if x['name']=='__LINKEDIT' and x['fileoff']<=off and off+size<=x['fileoff']+x['filesize']];assert len(hit)==1
  return dict(segment='__LINKEDIT',slice_file_offset=off,parent_file_offset=16384+off,bytes=size)
 sym['nlist_mapping']=mapping(sym['symoff'],sym['nsyms']*16);sym['string_mapping']=mapping(sym['stroff'],sym['strsize'])
 f.seek(sym['symoff']);nlist=f.read(sym['nsyms']*16);assert len(nlist)==sym['nsyms']*16
 f.seek(sym['stroff']);strings=f.read(sym['strsize']);assert len(strings)==sym['strsize']
def record(i):
 r=nlist[i*16:i*16+16];sx,nt,ns,nd,nv=struct.unpack('<IBBHQ',r);assert sx<len(strings)
 end=strings.find(b'\0',sx);assert end>=sx
 return r,sx,nt,ns,nd,nv,end,strings[sx:end]
# Count all matching nlist rows first, without retaining a first-N subset.
counts={k:0 for k in PREDICATES}
for i in range(sym['nsyms']):
 *_,name=record(i)
 for key,terms in PREDICATES.items():
  if all(term in name for term in terms):counts[key]+=1
selected={k:[] for k in PREDICATES};over=any(n>CAP for n in counts.values())
if not over:
 for i in range(sym['nsyms']):
  raw,sx,nt,ns,nd,nv,end,name=record(i)
  for key,terms in PREDICATES.items():
   if all(term in name for term in terms):
    sec=sections[ns-1] if 1<=ns<=len(sections) else None
    selected[key].append(dict(nlist_index=i,nlist_file_offset=sym['symoff']+16*i,parent_nlist_file_offset=16384+sym['symoff']+16*i,raw_nlist_hex=raw.hex(),string_index=sx,string_file_offset=sym['stroff']+sx,name=name.decode('ascii'),name_NUL_hex=strings[sx:end+1].hex(),n_type=nt,n_type_hex=hex(nt),n_type_mask=hex(nt&0x0e),N_STAB_bits=hex(nt&0xe0),N_EXT=bool(nt&1),N_PEXT=bool(nt&0x10),n_sect=ns,n_desc=nd,n_desc_hex=hex(nd),n_value=nv,n_value_hex=hex(nv),section_metadata=sec))
 for k in counts:assert len(selected[k])==counts[k]
after=[identity(p) for p in providers];assert before==after
q=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='COUNT_CAP_STOP' if over else 'FROZEN TWO CLASS-TOKEN NLIST METADATA NOMINATIONS ONLY; independent review pending',role='Analyst; no implementation/runtime',canonical_context_asof=context_asof,canonical_context_is_not_future_live_hashgate=True,pins=before,target=dict(build='12.4.3 (2026-07-07_e3d8be4d07)',universal=before[0],thin=before[1],plist=before[2],fat_header_hex=fh.hex(),fat_arch_metadata=arches,selected_arch=members[0],thin_header_hex=header.hex(),thin_header_fields=[magic,cpu,sub,typ,ncmds,lcbytes,flags,res],load_commands_sha256=sha(lc),load_command_metadata=commands,segments=segments),table=dict(command=sym,all_nlist_bytes_sha256=sha(nlist),all_string_table_bytes_sha256=sha(strings),section_metadata_count=len(sections)),selection=dict(case_sensitive_literal_substrings=True,predicates={k:[t.decode() for t in v] for k,v in PREDICATES.items()},cap_per_predicate=CAP,count_first=True,counts_are_nlist_rows_not_unique_functions=True,counts=counts,overcap=over,policy='If either count exceeds96, retain counts only and STOP; never firstN or a deduced name.',rows=selected),method=identity(Path(__file__).resolve()),preservation=dict(paths=len(before),before_after_equal=True,before_digest=sha(json.dumps(before,sort_keys=True).encode()),after_digest=sha(json.dumps(after,sort_keys=True).encode()),scope='Exact immutable binary/manifest/format/method providers only; canonical docs captured asof, not mutable future gates.'),read_scope='Fresh full binary identity hashes, universal header/member records, thin header/load commands/segment+section metadata, exact LC_SYMTAB nlist and string tables only. No native instruction bytes were selected/read semantically, no body/global/callee/decompiler/project/process followed. Whole-file hashing is opaque identity only.',limits=['Literal raw symbol names and values only; no mangled-name synthesis, demangling, aliases-to-original-class proof or firstN subset. AStereoGain token and OStereoGainProcessor token are not equivalent classes or public model-to-processor binding. Known OnMute/CalcMain hits are detail::TMemberFuncTypes<...OStereoGainProcessor...>::SProcessorFunc::__invoke wrappers, not plain AStereoGain members.','A matching name/section/address is navigation, not callability, function extent/type/ABI, actual receiver/processor/model or public Utility binding.','No arm64-to-x86 equivalence, original/native execution, tool/decompiler/decoder invocation, sourcecallee, new observer or numerical application claim.','All38 Utility outcomes remainU/null/unexecuted; zero new normative IDs/cases/grades/completedfamilies.','Metadata absence or overcap is finite availability only, not global no-route/absence proof. The pinned public-binding-minimum-frontier query is qualified canonical-only navigation, not native association proof.'],actual_expected=None,comparison=None,grade=None,complete=False,stop='STOP after exact metadata nomination. Any body/window/ABI/feasibility investigation needs separate Root selection.')
with Q.open('x') as f:json.dump(q,f,indent=2);f.write('\n')
print(json.dumps(dict(query=identity(Q),counts=counts,overcap=over,pins=len(before),actual_native_or_tool_execution=False),indent=2))
