"""Fixed eight-name x86 Mach-O metadata only; exact trailing-NUL names, never decode instructions."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import os
import struct
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent / 'reviews/wavetable-x86-typed8-root-metadata-selection-v2.json'
ROOT_SHA = '01a8c9aba288b4082c86782d1edc23331d78cb6731485e68fc93a56493dc14e1'
U64 = (1 << 64)-1


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def span(offset, size, limit):
    need(type(offset) is int and type(size) is int and 0 <= offset <= limit
         and 0 <= size <= limit-offset, 'metadata span bounds')


def encoded(value):
    return (json.dumps(value, indent=2, allow_nan=False)+'\n').encode()


def save(name, data):
    raw = data if isinstance(data, bytes) else encoded(data)
    with (BASE/name).open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def selection():
    raw = (BASE/'selection-root.json').read_bytes()
    need(sha(raw) == ROOT_SHA and ROOT.read_bytes() == raw, 'exact Root selection')
    plan = json.loads(raw)
    names = [x['type_encoding'] for x in plan['whole_typed_set']]
    need(len(names) == len(set(names)) == 8 and all(0 < len(n) < 512 and n.isascii() for n in names), 'whole eight names')
    need(plan['caps'] == dict(exact_type_names=8,name_matches_total=64,
        typeinfo_candidates_total=32,table_headers_total=64,primary_tables=8,
        slots_per_primary_table=6,total_primary_slots=48,
        retained_selected_metadata_bytes_max=1048576), 'fixed caps')
    need(plan['selected'] is True and plan['required_unsupported'] == 'U'
         and plan['coverage_gate'] == 'OPEN', 'Root selected metadata only')
    pins = []
    for pin in plan['inputs']:
        b = Path(pin['path']).read_bytes()
        need(len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'input document identity')
        pins.append(pin)
    owner = json.loads(Path(plan['inputs'][0]['path']).read_bytes())
    for item in plan['whole_typed_set']:
        rows = [x for x in owner['records'] if x['literal_type_encoding'] == item['type_encoding']]
        need(len(rows) == 6 and {x['slot_index'] for x in rows} == set(range(6)), 'whole ARM prefix metadata')
        row = next(x for x in rows if x['slot_index'] == 3)
        need(row['entry'] == item['ARM_slot3_entry'] and row['address_point'] == item['ARM_address_point'], 'ARM typed identity join')
    return plan, pins


def fixed_name(raw):
    head, sep, tail = raw.partition(b'\0')
    need(not sep or not any(tail), 'nonzero fixed-name padding')
    name = head.decode('ascii')
    need(name and all(32 < ord(x) < 127 for x in name), 'fixed metadata name')
    return name


def macho(data):
    span(0,32,len(data))
    magic,cpu,subtype,kind,count,size,flags,reserved = struct.unpack_from('<8I',data)
    need(magic == 0xfeedfacf and cpu == 0x1000007 and kind == 2 and reserved == 0, 'thin x86_64 MH_EXECUTE')
    need(0 < count <= 4096 and count <= size//8 and size <= 4*1048576, 'bounded command region')
    span(32,size,len(data));cursor,end = 32,32+size
    segments,sections,starts = [],[],[]
    for index in range(count):
        span(cursor,8,end);cmd,n = struct.unpack_from('<II',data,cursor)
        need(n >= 8 and n%8 == 0, 'command size/alignment');span(cursor,n,end)
        if cmd == 0x19:
            need(n >= 72, 'segment header')
            _,_,name,va,vs,fo,fs,mp,ip,ns,segflags = struct.unpack_from('<II16sQQQQiiII',data,cursor)
            need(n == 72+80*ns and vs <= U64-va and fs <= vs and ip & ~mp == 0, 'segment geometry')
            span(fo,fs,len(data));name = fixed_name(name)
            seg = dict(name=name,vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,
                       command_index=index,command_file_offset=cursor,section_count=ns,flags=segflags)
            segments.append(seg)
            for j in range(ns):
                off = cursor+72+80*j
                sn,sg,addr,length,offset,align,reloff,nreloc,fl,r1,r2,r3 = struct.unpack_from('<16s16sQQ8I',data,off)
                need(fixed_name(sg) == name and va <= addr <= va+vs and length <= va+vs-addr, 'section virtual bounds')
                need(align <= 31 and addr % (1<<align) == 0, 'section alignment')
                backed = (fl & 255) not in [1,12,18]
                if backed and length:
                    span(offset,length,len(data))
                    need(fo <= offset and offset+length <= fo+fs and offset == fo+addr-va, 'section file mapping')
                sections.append(dict(segment=name,name=fixed_name(sn),addr=addr,size=length,fileoff=offset,
                    align=align,flags=fl,file_backed=backed,executable=bool(ip&4) and bool(fl&0x80000400),
                    header_file_offset=off,relocation_fileoff=reloff,relocation_count=nreloc,
                    reserved1=r1,reserved2=r2,reserved3=r3))
        elif cmd == 0x26:
            need(n == 16, 'LC_FUNCTION_STARTS size')
            _,_,off,length = struct.unpack_from('<4I',data,cursor);span(off,length,len(data))
            starts.append(dict(command_index=index,command_file_offset=cursor,dataoff=off,datasize=length))
        cursor += n
    need(cursor == end and len(starts) <= 1, 'exact commands/no duplicate starts')
    need(len({s['name'] for s in segments}) == len(segments), 'unique segment names')
    for key,lengthkey in [('fileoff','filesize'),('vmaddr','vmsize')]:
        ranges = sorted((s[key],s[key]+s[lengthkey]) for s in segments if s[lengthkey])
        need(all(a[1] <= b[0] for a,b in zip(ranges,ranges[1:])), 'nonoverlapping segments')
    need(len({(s['segment'],s['name']) for s in sections})==len(sections), 'unique section names per segment')
    for seg in segments:
        sr=sorted((s['addr'],s['addr']+s['size']) for s in sections if s['segment']==seg['name'] and s['size'])
        need(all(a[1]<=b[0] for a,b in zip(sr,sr[1:])), 'nonoverlapping section VM ranges')
    texts = [s for s in segments if s['name'] == '__TEXT' and s['filesize']]
    need(len(texts) == 1, 'one file-backed TEXT')
    if starts:
        x=starts[0]
        need(sum(s['name']=='__LINKEDIT' and s['fileoff'] <= x['dataoff']
            and x['dataoff']+x['datasize'] <= s['fileoff']+s['filesize'] for s in segments)==1, 'starts LINKEDIT mapping')
    return dict(header=dict(magic=hex(magic),cpu=hex(cpu),subtype=hex(subtype),filetype=kind,
        ncmds=count,sizeofcmds=size,flags=hex(flags),reserved=reserved),segments=segments,
        sections=sections,starts_command=starts[0] if starts else None,text=texts[0])


def mapping(info,va,size,names):
    need(type(va) is int and va >= 0 and size >= 0 and va <= U64 and size <= U64-va, 'VA overflow')
    fits=[s for s in info['segments'] if s['name'] in names and s['vmaddr'] <= va
          and va+size <= s['vmaddr']+s['filesize']]
    need(len(fits)==1, 'unique file-backed selected segment')
    s=fits[0]
    return s['fileoff']+va-s['vmaddr']


def qword_refs(data,info,values,cap):
    result={v:[] for v in values};counts={v:0 for v in values};total=0;overcap=False
    for s in info['segments']:
        if s['name'] not in ['__DATA','__DATA_CONST']:
            continue
        first=s['fileoff']+((-s['vmaddr'])%8)
        end=s['fileoff']+s['filesize'];end -= (end-first)%8
        for j,(value,) in enumerate(struct.iter_unpack('<Q',memoryview(data)[first:end])):
            if value in result:
                counts[value]+=1;total+=1
                if total>cap and not overcap:
                    overcap=True;result={v:[] for v in values}
                if not overcap:
                    off=first+8*j;result[value].append(dict(file_offset=off,va=s['vmaddr']+off-s['fileoff'],segment=s['name']))
    return dict(refs=result,counts=counts,total=total,overcap=overcap)


def executable_target(info,address):
    rows=[s for s in info['sections'] if s['segment']=='__TEXT' and s['file_backed']
          and s['executable'] and s['addr'] <= address < s['addr']+s['size']]
    if len(rows)!=1:
        return dict(status='missing-or-ambiguous-executable-TEXT-section',matches=len(rows))
    s=rows[0]
    return dict(status='unique-executable-TEXT-section-metadata',section=s['name'],
                file_offset=s['fileoff']+address-s['addr'],instruction_bytes_read=False)


def uleb(data,offset,end):
    start=offset;value=0
    for i in range(10):
        need(offset<end,'truncated ULEB');byte=data[offset];offset+=1
        need(i!=9 or byte<=1,'ULEB uint64 overflow');value|=(byte&127)<<(7*i)
        if byte<128:
            need(i==0 or byte!=0,'noncanonical ULEB')
            return value,offset,data[start:offset].hex()
    raise ValueError('overlong ULEB')


def starts_metadata(data,info,targets):
    command=info['starts_command']
    if command is None:
        return dict(status='LC_FUNCTION_STARTS-absent',targets=[],body_proof=False)
    need(0<command['datasize']<=4*1048576,'function-start payload cap')
    off,end=command['dataoff'],command['dataoff']+command['datasize'];base=info['text']['vmaddr']
    wanted=sorted(set(targets));cursor=0;previous=None;rows=[];count=0;first=None;last=None;terminated=False
    while off<end:
        start=off;delta,off,raw=uleb(data,off,end)
        if delta==0:
            need(not any(data[off:end]),'nonzero after starts sentinel');terminated=True;break
        need(delta <= U64-base,'cumulative function-start overflow');base+=delta;count+=1
        need(count<=1000000,'function-start entry cap')
        loc=executable_target(info,base);need(loc['status']=='unique-executable-TEXT-section-metadata','start outside executable TEXT section')
        row=dict(address=hex(base),uleb_file_offset=start,uleb_hex=raw,file_offset=loc['file_offset'])
        while cursor<len(wanted) and wanted[cursor]<base:
            target=wanted[cursor];rows.append(dict(target=hex(target),exact_declared_start=bool(previous and int(previous['address'],16)==target),
                previous_or_equal_start=previous,next_start=row,body_range_proven=False));cursor+=1
        previous=row;first=first or row;last=row
    need(terminated,'missing starts sentinel')
    while cursor<len(wanted):
        target=wanted[cursor];rows.append(dict(target=hex(target),exact_declared_start=bool(previous and int(previous['address'],16)==target),
            previous_or_equal_start=previous,next_start=None,body_range_proven=False));cursor+=1
    return dict(status='strict-linker-metadata-only',command=command,payload_sha256=sha(data[command['dataoff']:end]),
        count=count,first=first,last=last,sentinel_file_offset=start,trailing_zero_bytes=end-off,
        targets=rows,body_proof=False,full_payload_retained=False)


def assess(data,info,plan):
    raw_ranges=[]
    def retained(kind,va,size,names):
        off=mapping(info,va,size,names);raw=data[off:off+size]
        raw_ranges.append(dict(kind=kind,va=hex(va),file_offset=off,bytes=size,hex=raw.hex(),sha256=sha(raw)))
        return raw
    text=info['text'];types=[];name_total=0;name_overcap=False
    for item in plan['whole_typed_set']:
        needle=item['type_encoding'].encode()+b'\0';off=text['fileoff'];end=off+text['filesize'];matches=[];name_count=0
        while True:
            at=data.find(needle,off,end)
            if at<0:break
            name_count+=1;name_total+=1
            if name_total>64 and not name_overcap:
                name_overcap=True;matches=[]
                for prior in types:prior['name_matches']=[]
            if not name_overcap:
                matches.append(dict(file_offset=at,va=text['vmaddr']+at-text['fileoff'],
                    preceding_file_offset=at-1 if at>text['fileoff'] else None,
                    preceding_byte_hex=data[at-1:at].hex() if at>text['fileoff'] else None))
            off=at+1
        types.append(dict(**item,name_matches=matches,name_match_count=name_count,typeinfo_candidates=[],
                          unjoined_name_pointer_refs=[],table_headers=[],unjoined_typeinfo_pointer_refs=[],primary_tables=[],status='U'))
    counts=dict(name_matches=name_total)
    def refusal(reason):
        # Complete counts; no firstN materialization or target/slot follow on an exceeded cap.
        return dict(status='REFUSED-U',reason=reason,counts=counts,types=types,selected_ranges=raw_ranges,
                    full_prefix_materialization=False,required_unsupported='U',coverage_gate='OPEN')
    if name_overcap:
        return refusal('all-name-match census exceeds64; no candidate materialization')
    by_name={x['va'] for t in types for x in t['name_matches']};scan=qword_refs(data,info,by_name,32)
    counts['aligned_name_pointer_refs']=scan['total']
    if scan['overcap']:
        for t in types:t['aligned_name_pointer_ref_count']=sum(scan['counts'][x['va']] for x in t['name_matches'])
        return refusal('complete aligned name-pointer census exceeds32; conservative stop before deriving candidates, no firstN')
    refs=scan['refs']
    for t in types:
        for x in t['name_matches']:
            retained('exact-trailing-NUL-type-name',x['va'],len(t['type_encoding'])+1,['__TEXT'])
            if x['preceding_byte_hex'] is not None:
                retained('selected-name-preceding-byte',x['va']-1,1,['__TEXT'])
            for ref in refs[x['va']]:
                va=ref['va']-8
                try:off=mapping(info,va,16,['__DATA','__DATA_CONST'])
                except ValueError as error:
                    t['unjoined_name_pointer_refs'].append(dict(**ref,error=str(error)));continue
                t['typeinfo_candidates'].append(dict(va=va,file_offset=off,name_va=x['va'],name_pointer_field_va=ref['va']))
    counts['typeinfo_candidates']=sum(len(t['typeinfo_candidates']) for t in types)
    if counts['typeinfo_candidates']>32:
        for t in types:t['typeinfo_candidate_count']=len(t['typeinfo_candidates']);t['typeinfo_candidates']=[]
        return refusal('complete typeinfo-candidate census exceeds32; no headers/slots followed')
    ti_values={x['va'] for t in types for x in t['typeinfo_candidates']};scan=qword_refs(data,info,ti_values,64)
    counts['aligned_typeinfo_pointer_refs']=scan['total']
    if scan['overcap']:
        for t in types:t['aligned_typeinfo_pointer_ref_count']=sum(scan['counts'][x['va']] for x in t['typeinfo_candidates'])
        return refusal('complete aligned typeinfo-pointer census exceeds64; conservative stop before headers, no firstN')
    headers=scan['refs']
    for t in types:
        for x in t['typeinfo_candidates']:
            x['header_hex']=retained('candidate-typeinfo-two-qword-head',x['va'],16,['__DATA','__DATA_CONST']).hex()
            x['vptr_unresolved']=hex(struct.unpack_from('<Q',bytes.fromhex(x['header_hex']))[0])
            for ref in headers[x['va']]:
                va=ref['va']-8
                try:off=mapping(info,va,16,['__DATA','__DATA_CONST'])
                except ValueError as error:
                    t['unjoined_typeinfo_pointer_refs'].append(dict(**ref,error=str(error)));continue
                top,ti=struct.unpack_from('<qQ',data,off);need(ti==x['va'],'exact header typeinfo join')
                h=dict(header_va=va,file_offset=off,offset_to_top=top,typeinfo_va=ti,address_point=va+16)
                t['table_headers'].append(h)
                if top==0:t['primary_tables'].append(h)
    counts['table_headers']=sum(len(t['table_headers']) for t in types)
    counts['primary_tables']=sum(len(t['primary_tables']) for t in types)
    if counts['table_headers']>64 or counts['primary_tables']>8:
        for t in types:
            t['table_header_count']=len(t['table_headers']);t['primary_table_count']=len(t['primary_tables'])
            t['table_headers']=[];t['primary_tables']=[]
        return refusal('complete header/primary census exceeds64/8; no prefix truncation')
    for t in types:
        for h in t['table_headers']:h['raw_header_hex']=retained('offset-to-top-and-typeinfo-header',h['header_va'],16,['__DATA','__DATA_CONST']).hex()
    if any(len(t['name_matches'])!=1 or len(t['typeinfo_candidates'])!=1 or len(t['primary_tables'])!=1 for t in types):
        return refusal('missing-or-ambiguous whole eight name/typeinfo/primary joins; all bounded candidates retained')
    prefix_gaps=[]
    for t in types:
        try:mapping(info,t['primary_tables'][0]['address_point'],48,['__DATA','__DATA_CONST'])
        except ValueError as error:prefix_gaps.append(dict(type_encoding=t['type_encoding'],error=str(error)))
    if prefix_gaps:
        counts['whole_prefix_gaps']=len(prefix_gaps)
        result=refusal('at least one whole six-slot prefix is not file-backed; no prefixes materialized')
        result['prefix_gaps']=prefix_gaps;return result
    slots=[]
    for t in types:
        h=t['primary_tables'][0]
        raw=retained('whole-six-qword-primary-prefix',h['address_point'],48,['__DATA','__DATA_CONST'])
        t['slots']=[]
        for index,address in enumerate(struct.unpack('<6Q',raw)):
            row=dict(index=index,field_va=hex(h['address_point']+8*index),target=hex(address),
                mapping=executable_target(info,address),selected_instruction_bytes=0)
            t['slots'].append(row);slots.append(address)
        t['status']='exact-typed-primary-six-slot-metadata-only'
    need(len(slots)==48,'whole48selected slots')
    valid=all(s['mapping']['status']=='unique-executable-TEXT-section-metadata' for t in types for s in t['slots'])
    result=dict(status='COMPLETE-BOUNDED-METADATA' if valid else 'U-TARGET-MAPPING-GAP',counts=dict(**counts,primary_slots=48),
        types=types,selected_ranges=raw_ranges,full_prefix_materialization=True,required_unsupported='U',coverage_gate='OPEN')
    try:result['function_starts']=starts_metadata(data,info,slots)
    except ValueError as error:result['function_starts']=dict(status='U-invalid-or-overcap-metadata',error=str(error),body_proof=False)
    return result


def collect():
    plan,pins=selection()
    marker=dict(started_utc=utc(),selection_sha256=ROOT_SHA,collector_sha256=sha(Path(__file__).read_bytes()),
                acquisition_attempts=1,automatic_retry=False)
    save('acquisition-attempt.json',marker)
    state=dict(**marker,phase='one-image-custody-read',image_opens=0,error=None,original_model_harness_decoder_calls=0)
    try:
        with Path(plan['image']['path']).open('rb') as stream:
            state['image_opens']=1;a=os.fstat(stream.fileno());data=stream.read(plan['image']['bytes']+1);b=os.fstat(stream.fileno())
        need((a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns),'image descriptor custody changed')
        need(len(data)==plan['image']['bytes'] and sha(data)==plan['image']['sha256'],'whole-image exact custody')
        state['image_identity']=dict(**plan['image'],descriptor_before_after_equal=True,device=a.st_dev,inode=a.st_ino,mtime_ns=a.st_mtime_ns,ctime_ns=a.st_ctime_ns)
        state['phase']='strict-metadata-only';info=macho(data);result=assess(data,info,plan)
        metadata=encoded(dict(macho=info,result=result,inputs=pins,selection_sha256=ROOT_SHA,
            no_instruction_decoder_or_original_execution=True,complete_table_or_ABI_proof=False))
        size=32+info['header']['sizeofcmds'];need(size+len(metadata)<=1048576,'retained selected metadata cap')
        save('header-loadcommands.bin',data[:size]);save('metadata.json',metadata)
        state.update(phase='metadata-retained',result_status=result['status'],counts=result['counts'],retained_selected_metadata_bytes=size+len(metadata))
    except BaseException as error:
        state['error']=type(error).__name__+': '+str(error)
        save('failure.json',dict(error=state['error'],phase=state['phase'],partial_files_retained=True,retry=False))
    state['finished_utc']=utc();save('acquisition-receipt.json',state)
    print(json.dumps(state,indent=2));return int(state['error'] is not None)


def check():
    plan,pins=selection();rejected=[]
    def bad(name,action):
        try:action()
        except (ValueError,struct.error,UnicodeError):rejected.append(name);return
        raise ValueError('accepted negative '+name)
    # A tiny wholly synthetic Mach-O has metadata sections, never instructions.
    n=72+80;lc=bytearray();sections=[('__TEXT','__cstring',0x100000000,512,0,512,2),('__DATA','__const',0x100001000,512,512,512,0)]
    for sg,sn,va,vs,fo,fs,fl in sections:
        lc+=struct.pack('<II16sQQQQiiII',0x19,n,sg.encode(),va,vs,fo,fs,7,5 if sg=='__TEXT' else 3,1,0)
        # First section leaves room for header/commands within TEXT mapping.
        addr=va+352 if sg=='__TEXT' else va;off=fo+352 if sg=='__TEXT' else fo;length=fs-352 if sg=='__TEXT' else fs
        lc+=struct.pack('<16s16sQQ8I',sn.encode(),sg.encode(),addr,length,off,0,0,0,fl,0,0,0)
    data=bytearray(1024);data[:32]=struct.pack('<8I',0xfeedfacf,0x1000007,3,2,2,len(lc),0,0);data[32:32+len(lc)]=lc
    info=macho(data);need(mapping(info,0x100001000,16,['__DATA'])==512,'synthetic mapping')
    struct.pack_into('<Q',data,512,0x100000180);need(qword_refs(data,info,{0x100000180},32)['refs'][0x100000180][0]['va']==0x100001000,'aligned name pointer')
    bad('truncated header',lambda:macho(data[:31]))
    for name,offset,value in [('wrong CPU',4,0x100000c),('fat magic',0,0xcafebabe),('wrong filetype',12,6),('reserved header',28,1),('too many commands',16,4097)]:
        altered=bytearray(data);struct.pack_into('<I',altered,offset,value);bad(name,lambda altered=altered:macho(altered))
    for name,offset,value in [('zero command',36,0),('unaligned command',36,151),('section count mismatch',96,2)]:
        altered=bytearray(data);struct.pack_into('<I',altered,offset,value);bad(name,lambda altered=altered:macho(altered))
    bad('missing mapping',lambda:mapping(info,0x400000000,8,['__DATA']))
    bad('VA overflow',lambda:mapping(info,U64,8,['__DATA']))
    ambiguous=copy.deepcopy(info);ambiguous['segments'].append(copy.deepcopy(info['segments'][1]));bad('ambiguous data mapping',lambda:mapping(ambiguous,0x100001000,8,['__DATA']))
    bad('truncated ULEB',lambda:uleb(b'\x80',0,1))
    bad('noncanonical ULEB',lambda:uleb(b'\x81\x00',0,2))
    bad('overflow ULEB',lambda:uleb(b'\xff'*9+b'\x02',0,10))
    bad('overlong ULEB',lambda:uleb(b'\x80'*11,0,11))
    for raw,value in [(b'\x00',0),(b'\x7f',127),(b'\x80\x01',128),(b'\xff'*9+b'\x01',U64)]:need(uleb(raw,0,len(raw))[:2]==(value,len(raw)),'ULEB positive')
    # A pointer-type prefix may share exact terminated suffix bytes.
    need(b'Ptyped\0'.find(b'typed\0')==1 and b'Ptyped\0'.find(b'\0typed\0')==-1,'synthetic suffix predicate distinction')
    need(b'typedX\0'.find(b'typed\0')==-1,'reject nonterminated exact bytes')
    # Complete eight-type/six-slot synthetic join. Target sections contain zero
    # placeholder DATA only; no instruction interpretation is performed.
    z=bytearray(16384);cmds=bytearray()
    cmds+=struct.pack('<II16sQQQQiiII',0x19,232,b'__TEXT',0x100000000,8192,0,8192,7,5,2,0)
    for sn,addr,length,fo,fl in [(b'__cstring',0x100000400,3072,1024,2),(b'__text',0x100001000,4096,4096,0x80000400)]:
        cmds+=struct.pack('<16s16sQQ8I',sn,b'__TEXT',addr,length,fo,0,0,0,fl,0,0,0)
    cmds+=struct.pack('<II16sQQQQiiII',0x19,152,b'__DATA',0x100002000,8192,8192,8192,7,3,1,0)
    cmds+=struct.pack('<16s16sQQ8I',b'__const',b'__DATA',0x100002000,8192,8192,0,0,0,0,0,0,0)
    z[:32]=struct.pack('<8I',0xfeedfacf,0x1000007,3,2,2,len(cmds),0,0);z[32:32+len(cmds)]=cmds
    nameoff=1024
    for i,item in enumerate(plan['whole_typed_set']):
        name=item['type_encoding'].encode()+b'\0';z[nameoff:nameoff+len(name)]=name
        struct.pack_into('<QQ',z,8192+16*i,0,0x100000000+nameoff)
        struct.pack_into('<qQ6Q',z,8192+512+80*i,0,0x100002000+16*i,*[0x100001000+2*(6*i+j) for j in range(6)])
        nameoff+=len(name)
    zi=macho(z);full=assess(z,zi,plan)
    need(full['status']=='COMPLETE-BOUNDED-METADATA' and full['counts']['primary_slots']==48,'whole synthetic48slot join')
    need(all(len(t['name_matches'])==len(t['typeinfo_candidates'])==len(t['primary_tables'])==1 for t in full['types']),'all8exact joins')
    suffix=bytearray(z);suffix[1023]=ord('P');r=assess(suffix,zi,plan)
    need(r['status']=='COMPLETE-BOUNDED-METADATA' and r['types'][0]['name_matches'][0]['preceding_byte_hex']=='50','legitimate P+exact name+NUL accepted with exact pointer')
    nonterminated=bytearray(z);nonterminated[1024+len(plan['whole_typed_set'][0]['type_encoding'])]=ord('X');r=assess(nonterminated,zi,plan)
    need(r['status']=='REFUSED-U' and not r['full_prefix_materialization'] and 'function_starts' not in r,'nonterminated name refuses full set');rejected.append('nonterminated name no first7')
    missing=bytearray(z);missing[1024]=ord('X');r=assess(missing,zi,plan)
    need(r['status']=='REFUSED-U' and not r['full_prefix_materialization'],'missing whole type refuses');rejected.append('missing whole type')
    duplicate=bytearray(z);name=plan['whole_typed_set'][0]['type_encoding'].encode()+b'\0';duplicate[3000:3000+len(name)]=name
    r=assess(duplicate,zi,plan);need(r['status']=='REFUSED-U' and not r['full_prefix_materialization'],'ambiguous exact name refuses');rejected.append('ambiguous exact name')
    ninth=bytearray(z);struct.pack_into('<qQ',ninth,8192+4096,0,0x100002000)
    r=assess(ninth,zi,plan);need(r['status']=='REFUSED-U' and r['counts']['primary_tables']==9 and not r['full_prefix_materialization'],'ninth primary refuses');rejected.append('ninth primary no truncation')
    secondary=bytearray(z);struct.pack_into('<qQ',secondary,8192+4096,-8,0x100002000)
    r=assess(secondary,zi,plan);need(r['counts']['table_headers']==9 and r['counts']['primary_slots']==48,'secondary retained without prefix expansion')
    over=bytearray(z)
    for i in range(33):struct.pack_into('<Q',over,8192+2048+8*i,0x100000400)
    r=assess(over,zi,plan);need(r['status']=='REFUSED-U' and not r['full_prefix_materialization'],'pointer census cap refuses');rejected.append('aligned pointer census cap')
    si=copy.deepcopy(zi);si['starts_command']=dict(dataoff=0,datasize=4)
    sr=starts_metadata(b'\x80\x20\x02\x00',si,[0x100001000,0x100001001,0x100001002])
    need(sr['count']==2 and [x['exact_declared_start'] for x in sr['targets']]==[True,False,True],'strict starts exact and between')
    bad('nonzero after starts sentinel',lambda:starts_metadata(b'\x80\x20\x00\x01',si,[]))
    bad('start outside instruction section',lambda:starts_metadata(b'\x01\x00\x00\x00',si,[]))
    si['starts_command']['datasize']=2
    bad('missing starts sentinel',lambda:starts_metadata(b'\x80\x20',si,[]))
    # All-census caps stop before materialization; synthetic short names only.
    short=copy.deepcopy(plan)
    for i,t in enumerate(short['whole_typed_set']):t['type_encoding']='T'+str(i)
    many=bytearray(z)
    for i in range(65):many[1024+4*i:1024+4*i+3]=b'T0\0'
    r=assess(many,zi,short)
    need(r['status']=='REFUSED-U' and r['counts']['name_matches']==65 and not r['selected_ranges'] and all(not t['name_matches'] for t in r['types']),'65name cap allcounts no firstN');rejected.append('name match cap no first64')
    refs=qword_refs(over,zi,{0x100000400},1)
    need(refs['overcap'] and refs['total']==34 and all(not v for v in refs['refs'].values()),'all reference counts after cap')
    overheaders=bytearray(z)
    for i in range(65):struct.pack_into('<Q',overheaders,8192+2048+8*i,0x100002000)
    r=assess(overheaders,zi,plan)
    need(r['status']=='REFUSED-U' and r['counts']['aligned_typeinfo_pointer_refs']==73 and not r['full_prefix_materialization'],'header reference cap completecount');rejected.append('header pointer cap no first64')
    huge=copy.deepcopy(si);huge['starts_command']['datasize']=4*1048576+1
    bad('function-start payload over4MiB',lambda:starts_metadata(b'',huge,[]))
    need(plan['caps']['total_primary_slots']==8*6,'whole prefix cap')
    need(not (BASE/'acquisition-attempt.json').exists(),'one-shot acquisition already attempted')
    print(json.dumps(dict(status='PASS-synthetic-document-only',negative_count=len(rejected),negatives=rejected,
        input_document_pins=len(pins),exact_types=8,primary_slot_cap=48,image_opens=0,decoder_original_model_harness_calls=0),indent=2))
    return 0


if __name__=='__main__':
    if sys.argv[1:]==['--check']:
        raise SystemExit(check())
    if sys.argv[1:]!=['--collect-once',ROOT_SHA]:
        raise SystemExit('Use --check or the exact separately Root-selected metadata identity; no overrides/retries.')
    raise SystemExit(collect())
