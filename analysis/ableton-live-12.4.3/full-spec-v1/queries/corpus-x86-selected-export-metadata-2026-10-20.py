"""Only fat/thin Mach-O, two selected exports and linker-start metadata; no code decode."""
from pathlib import Path
import struct,json,hashlib,bisect,datetime
ROOT=Path('/home/ollie/Documents/sound');BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
BUNDLE=Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Corpus.bundle/Contents/MacOS/Corpus')
OUT=BASE/'queries/corpus-x86-selected-export-metadata-2026-10-20.json'
NAMES=(b'_CalcA',b'_CreateInstanceU');EXPECTED={b'_CalcA':0x29c0,b'_CreateInstanceU':0x23b0}
def digest(b):return hashlib.sha256(b).hexdigest()
def identity(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=digest(b))
def bound(off,size,limit):assert 0<=off<=limit and 0<=size<=limit-off
def uleb(data,pos,end):
 start=pos;value=0
 for i in range(10):
  assert pos<end,'truncated ULEB';b=data[pos];pos+=1
  assert i!=9 or b<=1,'overflow ULEB';value|=(b&127)<<(7*i)
  if not b&128:
   assert i==0 or b!=0,'noncanonical ULEB'
   return value,pos,data[start:pos]
 raise AssertionError('overlong ULEB')
def map_va(va,segments):
 matches=[s for s in segments if s['vmaddr']<=va<s['vmaddr']+s['filesize']]
 assert len(matches)==1 and matches[0]['initprot']&4
 s=matches[0];return dict(segment=s['name'],slice_file_offset=s['fileoff']+va-s['vmaddr'],bundle_file_offset=16384+s['fileoff']+va-s['vmaddr'],file_backed_entry_byte_only=True)
def export_lookup(blob,name,fileoff):
 offset=0;prefix=b'';visited=set();path=[]
 while True:
  assert offset not in visited and len(visited)<256;visited.add(offset);bound(offset,1,len(blob))
  terminal_size,p,encoded=uleb(blob,offset,len(blob));terminal_start=p;terminal_end=p+terminal_size;bound(p,terminal_size,len(blob))
  if prefix==name:
   if not terminal_size:return dict(status='absent_terminal',path=path)
   flags,t,_=uleb(blob,terminal_start,terminal_end);result=dict(status='present',node_blob_offset=offset,node_slice_file_offset=fileoff+offset,terminal_size=terminal_size,terminal_size_uleb=encoded.hex(),terminal_hex=blob[terminal_start:terminal_end].hex(),flags=flags,path=path)
   if flags&8:
    ordinal,t,_=uleb(blob,t,terminal_end);end=blob.find(b'\0',t,terminal_end);assert end>=0
    result.update(reexport_ordinal=ordinal,reexport_name_hex=blob[t:end].hex(),meaning='reexport; no local entry inferred');t=end+1
   else:
    address,t,_=uleb(blob,t,terminal_end);result['image_relative_address']=address
    if flags&16:resolver,t,_=uleb(blob,t,terminal_end);result['resolver_relative_address']=resolver
   assert t==terminal_end,'unconsumed selected export terminal'
   return result
  p=terminal_end;bound(p,1,len(blob));count=blob[p];p+=1;matching=[]
  for _ in range(count):
   end=blob.find(b'\0',p);assert end>=p
   edge=blob[p:end];assert edge;p=end+1;child,p,childraw=uleb(blob,p,len(blob));bound(child,1,len(blob))
   if name.startswith(prefix+edge):matching.append((edge,child,childraw))
  if not matching:return dict(status='absent_path',path=path)
  assert len(matching)==1,'ambiguous selected trie path';edge,child,childraw=matching[0]
  path.append(dict(node_blob_offset=offset,edge_hex=edge.hex(),child_offset=child,child_offset_uleb=childraw.hex()))
  prefix+=edge;offset=child
assert not OUT.exists()
provider_paths=[Path(__file__).resolve(),BUNDLE,BASE/'depth-corpus-pickup-step-capture/proposal.json',BASE/'reviews/corpus-lfo-harness-readiness-review.json',BASE/'queries/corpus-membrane-state-readout-design-2026-10-20.json',ROOT/'wiki/research/function-starts-design.md',ROOT/'tools/index_macho_function_starts.py',ROOT/'analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1/raw/corpus/mode_membrane_44.log']
watched=set(provider_paths);watched.update(p for p in (ROOT/'handoff').rglob('*') if p.is_file())
before=[identity(p) for p in sorted(watched)]
fat=BUNDLE.read_bytes();assert len(fat)==527152 and digest(fat)=='2164ec08805b35f1571687a08b7ce7df9831102981f0e2fdbd07719dbf3ef422'
magic,narch=struct.unpack_from('>II',fat);assert magic==0xcafebabe;bound(8,20*narch,len(fat));arches=[]
for i in range(narch):
 a=8+20*i;cpu,sub,off,size,align=struct.unpack_from('>5I',fat,a);bound(off,size,len(fat));assert align<64 and off%(1<<align)==0
 arches.append(dict(cpu=cpu,subtype=sub,offset=off,bytes=size,align_power2=align,record_bundle_offset=a,raw_hex=fat[a:a+20].hex()))
x86=[a for a in arches if a['cpu']==0x1000007];assert len(x86)==1;selected=x86[0];assert selected['offset']==16384 and selected['bytes']==250352
data=fat[16384:16384+250352];assert digest(data)=='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
header=struct.unpack_from('<8I',data);magic,cpu,sub,kind,ncmd,cmdbytes,flags,reserved=header
assert magic==0xfeedfacf and cpu==0x1000007 and kind==8 and reserved==0;bound(32,cmdbytes,len(data));assert ncmd<=cmdbytes//8
cursor=32;segments=[];sections=[];commands=[];symtabs=[];exports=[];starts=[]
for i in range(ncmd):
 bound(cursor,8,32+cmdbytes);cmd,size=struct.unpack_from('<II',data,cursor);assert size>=8 and size%8==0;bound(cursor,size,32+cmdbytes)
 item=dict(index=i,command=hex(cmd),slice_file_offset=cursor,bytes=size)
 if cmd==0x19:
  assert size>=72;n,va,vs,fo,fs,mp,ip,ns,fl=struct.unpack_from('<16sQQQQiiII',data,cursor+8)
  assert size==72+80*ns and fs<=vs and va+vs<=1<<64 and ip&~mp==0;bound(fo,fs,len(data))
  seg=dict(name=n.split(b'\0')[0].decode('ascii'),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=fl);segments.append(seg)
  for j in range(ns):
   q=cursor+72+80*j;sn,sg,addr,ssz,so,al,rel,nrel,sfl,r1,r2,r3=struct.unpack_from('<16s16sQQ8I',data,q)
   sections.append(dict(ordinal_1_based=len(sections)+1,name=sn.split(b'\0')[0].decode('ascii'),segment=sg.split(b'\0')[0].decode('ascii'),address=addr,size=ssz,fileoff=so,flags=sfl))
 elif cmd==2:
  assert size==24;_,_,so,nn,st,sz=struct.unpack_from('<6I',data,cursor);bound(so,nn*16,len(data));bound(st,sz,len(data));symtabs.append(dict(command_index=i,symoff=so,nsyms=nn,stroff=st,strsize=sz,raw_command_hex=data[cursor:cursor+size].hex()))
 elif cmd in (0x22,0x80000022):
  assert size==48;fields=struct.unpack_from('<12I',data,cursor)
  for off,sz in zip(fields[2::2],fields[3::2]):bound(off,sz,len(data))
  if fields[11]:exports.append(dict(command_index=i,dataoff=fields[10],datasize=fields[11],raw_command_hex=data[cursor:cursor+size].hex()))
 elif cmd==0x80000033:
  assert size==16;_,_,off,sz=struct.unpack_from('<4I',data,cursor);bound(off,sz,len(data));exports.append(dict(command_index=i,dataoff=off,datasize=sz,raw_command_hex=data[cursor:cursor+size].hex()))
 elif cmd==0x26:
  assert size==16;_,_,off,sz=struct.unpack_from('<4I',data,cursor);bound(off,sz,len(data));starts.append(dict(command_index=i,dataoff=off,datasize=sz,raw_command_hex=data[cursor:cursor+size].hex()))
 commands.append(item);cursor+=size
assert cursor==32+cmdbytes and len(symtabs)==1 and len(exports)<=1 and len(starts)<=1
texts=[s for s in segments if s['name']=='__TEXT'];assert len(texts)==1;assert texts[0]['vmaddr']==0
def link_mapping(off,size):
 matches=[s for s in segments if s['name']=='__LINKEDIT' and s['fileoff']<=off and off+size<=s['fileoff']+s['filesize']]
 assert len(matches)==1,'metadata payload has no unique LINKEDIT mapping'
 return dict(segment='__LINKEDIT',slice_file_offset=off,bundle_file_offset=16384+off,bytes=size)
for row in exports+starts:row['file_mapping']=link_mapping(row['dataoff'],row['datasize'])
sym=symtabs[0];sym['nlist_mapping']=link_mapping(sym['symoff'],sym['nsyms']*16);sym['strings_mapping']=link_mapping(sym['stroff'],sym['strsize']);strings=data[sym['stroff']:sym['stroff']+sym['strsize']];selected_symbols={n:[] for n in NAMES}
for i in range(sym['nsyms']):
 off=sym['symoff']+i*16;sx,typ,sect,desc,value=struct.unpack_from('<IBBHQ',data,off);assert sx<len(strings)
 end=strings.find(b'\0',sx);assert end>=sx;name=strings[sx:end]
 if name in selected_symbols:
  assert typ&0xe0==0 and typ&1 and typ&0xe==0xe and 1<=sect<=len(sections)
  sec=sections[sect-1];assert sec['address']<=value<sec['address']+sec['size']
  assert sec['fileoff']+value-sec['address']==map_va(value,segments)['slice_file_offset']
  selected_symbols[name].append(dict(nlist_index=i,slice_file_offset=off,bundle_file_offset=16384+off,raw_nlist_hex=data[off:off+16].hex(),string_index=sx,string_slice_file_offset=sym['stroff']+sx,name_nul_hex=strings[sx:end+1].hex(),n_type=typ,n_sect=sect,n_desc=desc,n_value=value,section=sections[sect-1],entry_mapping=map_va(value,segments)))
assert all(len(v)==1 for v in selected_symbols.values())
export_info={}
if exports:
 ex=exports[0];blob=data[ex['dataoff']:ex['dataoff']+ex['datasize']]
 for name in NAMES:export_info[name]=export_lookup(blob,name,ex['dataoff'])
else:export_info={name:dict(status='LC export metadata absent; not guessed') for name in NAMES}
start_info=dict(status='LC_FUNCTION_STARTS absent',memberships={})
if starts:
 st=starts[0];blob=data[st['dataoff']:st['dataoff']+st['datasize']];assert blob
 addr=texts[0]['vmaddr'];pos=0;entries=[];terminated=False
 while pos<len(blob):
  begin=pos;delta,pos,encoded=uleb(blob,pos,len(blob))
  if delta==0:assert all(b==0 for b in blob[pos:]);terminated=True;break
  assert addr+delta<1<<64;prev=addr;addr+=delta;mapping=map_va(addr,segments)
  entries.append(dict(index=len(entries),address=addr,previous_address=prev,delta=delta,uleb_blob_offset=begin,uleb_slice_file_offset=st['dataoff']+begin,uleb_hex=encoded.hex(),entry_mapping=mapping))
 assert terminated,'functionstarts lacks terminator'
 addresses=[r['address'] for r in entries];members={}
 for name in NAMES:
  value=selected_symbols[name][0]['n_value'];i=bisect.bisect_left(addresses,value);exact=i<len(entries) and addresses[i]==value
  members[name.decode()]=dict(exact_membership=exact,previous=None if i==0 else entries[i-1],selected=None if not exact else entries[i],next=None if i+int(exact)>=len(entries) else entries[i+int(exact)],not_a_body_range=True)
 start_info=dict(status='present',command=st,payload_sha256=digest(blob),declared_start_count=len(entries),termination_uleb_blob_offset=begin,trailing_zero_padding_bytes=len(blob)-pos,memberships=members,x86_alignment_policy='No arm64 modulo4 constraint. Each start requires only one uniquely mapped executable file-backed entry byte. This is not an instruction/body read.')
results={}
for name in NAMES:
 rec=selected_symbols[name][0];assert rec['n_value']==EXPECTED[name]
 ex=export_info[name]
 if ex['status']=='present':assert ex['flags']==0 and ex['image_relative_address']==rec['n_value']
 results[name.decode()]=dict(nlist=rec,export_trie=ex,retained_old_log_value=EXPECTED[name],log_identity_agrees=True)
for invalid in (b'\x80',b'\x80\x00',b'\xff'*10+b'\x00'):
 try:uleb(invalid,0,len(invalid))
 except AssertionError:pass
 else:raise AssertionError('Malformed ULEB accepted')
assert uleb(b'\x81\x01',0,2)[0]==129
after=[identity(p) for p in sorted(watched)];assert before==after
q=dict(schema='selected-corpus-x86-export-function-start-metadata-v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='FROZEN STRICT METADATA ONLY; independent review pending',source_pins=[identity(p) for p in provider_paths],fat=dict(bytes=len(fat),sha256=digest(fat),header_hex=fat[:8].hex(),arch_records=arches,selected_x86_arch=selected),slice=dict(offset=16384,bytes=len(data),sha256=digest(data),header_hex=data[:32].hex(),header_fields=list(header),architecture='x86_64',filetype='MH_BUNDLE',load_commands_bytes=cmdbytes,load_commands_sha256=digest(data[32:32+cmdbytes]),load_command_records=commands,segments=segments),symbol_table=dict(command=sym,raw_nlist_table_sha256=digest(data[sym['symoff']:sym['symoff']+sym['nsyms']*16]),string_table_sha256=digest(strings),selected_names_only=True),export_metadata=dict(status='present' if exports else 'absent',commands=exports,payload_sha256=None if not exports else digest(data[exports[0]['dataoff']:exports[0]['dataoff']+exports[0]['datasize']])),selected=results,function_starts=start_info,method=dict(own_method=identity(Path(__file__).resolve()),reference_parser=identity(ROOT/'tools/index_macho_function_starts.py'),reference_source_read_only=True,reference_parser_imported_or_run=False,own_stdlib_only=True,uleb_negative_fixtures=3,uleb_positive_control=True,no_other_export_names_retained=True),limits=['Metadata addresses/names and membership only; not body extents, discovered-code inventory, function types, argument ABI, callability or runtime state.','Nearest previous/next linker starts are navigation only. Gaps are NOT body size or permission to read intervening/native bytes.','No arm64 instruction alignment applied to x86; no code window, instruction/body/opcode/decoder or sourcecallee read. Whole fat/slice bytes hashed as data only.','Only _CalcA and _CreateInstanceU exact nlist/export records retained. No originalcalls, observercode/build/toolversionprobe/install or numerical/pole/model work.','Actual selected x86 object/field/slot/count/lane/localtail mapping and observable component remainU. All174+2modalomissions ungraded.'],watch=dict(paths=len(before),scope='eight exact providers plus all publishedhandoff files; scoped metadata extraction only, no future mutablecanonicalgate',before_sha256=digest(json.dumps(before,sort_keys=True).encode()),after_sha256=digest(json.dumps(after,sort_keys=True).encode()),unchanged=True),actual_expected=None,comparison=None,new_REQ_cases_or_grades=0,complete=False,stop='STOP after exact metadata. Root separately reviews/selects any new bounded instruction/source work; no body-size inference or automatic target follow.')
with OUT.open('x') as f:json.dump(q,f,indent=2);f.write('\n')
print(json.dumps(dict(query=identity(OUT),selected={k:dict(nlist_value=hex(v['nlist']['n_value']),export_status=v['export_trie']['status']) for k,v in results.items()},function_starts_status=start_info['status'],function_starts_count=start_info.get('declared_start_count'),watch=len(before),instruction_or_original_execution=False),indent=2))
