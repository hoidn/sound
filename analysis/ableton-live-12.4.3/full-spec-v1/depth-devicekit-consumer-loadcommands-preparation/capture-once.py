"""Fixed thin-consumer header/load-command metadata only; --check never opens images."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import os
import signal
import struct
import sys

HERE=Path(__file__).resolve().parent
ROOT_SELECTION=HERE.parent/'reviews/devicekit-consumer-loadcommands-root-preparation-selection.json'
SELECTION_SHA='7acddc0a74c5ab09aacfdf1b105ac84304c4da6cbf8e67157ee5af9246468852'
DEST=HERE.with_name('depth-devicekit-consumer-loadcommands-v1')
IMAGE='/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64'
IMAGE_SIZE=149711904
IMAGE_SHA='3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
U64=(1<<64)-1


def need(ok,message):
    if not ok:raise ValueError(message)


def sha(data):return hashlib.sha256(data).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()


def identity(path):
    digest=hashlib.sha256();size=0
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):
            digest.update(block);size+=len(block)
    return dict(path=str(path),bytes=size,sha256=digest.hexdigest())


def verify(pin):
    actual=identity(Path(pin['path']))
    need(all(actual[k]==pin[k] for k in ('bytes','sha256')),'immutable document pin changed')
    return actual


def plan():
    raw=ROOT_SELECTION.read_bytes()
    need(len(raw)==3078 and sha(raw)==SELECTION_SHA,'fixed Root selection changed')
    selected=json.loads(raw)
    validate_plan(selected)
    for pin in selected['prerequisites']:verify(pin)
    return selected


def validate_plan(selected):
    need(selected['future_image']==dict(path=IMAGE,bytes=IMAGE_SIZE,sha256=IMAGE_SHA),'fixed thin consumer identity')
    need(selected['maximum_content_bytes']==65568 and selected['future_children']==0 and selected['maximum_capture_attempts']==1 and selected['automatic_retry'] is False,'fixed capture caps')
    need(selected['preparation_directory']==HERE.name and selected['future_capture_directory']==DEST.name,'fixed preparation/destination')
    need(len(selected['prerequisites'])==3,'exact three immutable prerequisite documents')


def header(data,image_size):
    need(len(data)==32,'32-byte header required')
    magic,cpu,subtype,kind,count,size,flags,reserved=struct.unpack('<8I',data)
    need(magic==0xfeedfacf and cpu==0x100000c and kind==2 and reserved==0,'thin little-endian ARM64 MH_EXECUTE required')
    need(1<=count<=512 and 8<=size<=65536 and count<=size//8 and size%8==0,'header command count/size caps')
    need(32+size<=image_size,'header/commands inside image')
    return dict(cpu_subtype=subtype,filetype=kind,ncmds=count,sizeofcmds=size,flags=flags,header_hex=data.hex())


def span(offset,size,image_size):
    need(type(offset) is int and type(size) is int and 0<=offset<=U64 and 0<=size<=U64-offset,'table/segment offset or overflow')
    need(offset+size<=image_size,'table/segment file bounds')
    return dict(file_offset=offset,bytes=size)


def cstring(raw,offset,minimum):
    need(minimum<=offset<len(raw),'command-relative string offset')
    end=raw.find(b'\0',offset)
    need(end>=offset,'unterminated command string')
    return dict(command_relative_offset=offset,bytes_hex=raw[offset:end].hex(),text=raw[offset:end].decode('utf-8',errors='backslashreplace'))


def fixed_name(raw):
    return raw.split(b'\0',1)[0].decode('utf-8',errors='backslashreplace')


def commands(raw,info,image_size):
    need(len(raw)==info['sizeofcmds'],'exact load-command region bytes')
    result=[];cursor=0
    for index in range(info['ncmds']):
        need(cursor+8<=len(raw),'command header bounds')
        cmd,length=struct.unpack_from('<II',raw,cursor)
        need(length>=8 and length%8==0 and cursor+length<=len(raw),'command length/alignment/bounds')
        part=raw[cursor:cursor+length]
        row=dict(index=index,file_offset=32+cursor,cmd=hex(cmd),cmdsize=length,raw_hex=part.hex(),raw_sha256=sha(part),kind='unknown-command-retained-raw',table_locations=[])
        if cmd==0x19:
            need(length>=72,'segment command prefix')
            name,va,vm_size,fo,fs,maximum,initial,nsects,flags=struct.unpack_from('<16sQQQQiiII',part,8)
            need(length==72+80*nsects,'segment section-count extent')
            need(va<=U64-vm_size and fs<=vm_size and 0<=initial<=7 and 0<=maximum<=7 and initial&~maximum==0,'segment virtual/protection bounds')
            span(fo,fs,image_size)
            row.update(kind='LC_SEGMENT_64',segment=dict(name=fixed_name(name),vmaddr=va,vmsize=vm_size,fileoff=fo,filesize=fs,maxprot=maximum,initprot=initial,flags=flags),sections=[])
            for section_index in range(nsects):
                position=72+80*section_index
                sn,sg,addr,sz,off,align,reloff,nreloc,sflags,r1,r2,r3=struct.unpack_from('<16s16sQQIIIIIIII',part,position)
                need(va<=addr and sz<=U64-addr and addr+sz<=va+vm_size,'section virtual bounds')
                zero_fill=(sflags&255) in (1,12,18)
                if not zero_fill:
                    span(off,sz,image_size)
                    need(fo<=off and off+sz<=fo+fs,'section file-backed segment bounds')
                reloc=span(reloff,8*nreloc,image_size)
                row['sections'].append(dict(index=section_index,section_header_file_offset=32+cursor+position,name=fixed_name(sn),segment_name=fixed_name(sg),vmaddr=addr,bytes=sz,file_offset=off,zero_fill=zero_fill,alignment_power=align,flags=sflags,reserved=[r1,r2,r3],relocation_location=reloc))
        elif cmd in (0xc,0xd,0x80000018,0x8000001f,0x20,0x80000023):
            need(length>=24,'dylib command prefix')
            offset,timestamp,current,compatibility=struct.unpack_from('<4I',part,8)
            row.update(kind='dylib-install-name-declaration',name=cstring(part,offset,24),timestamp=timestamp,current_version=current,compatibility_version=compatibility)
        elif cmd in (0x8000001c,0xe,0xf,0x27):
            need(length>=12,'rpath/dylinker command prefix')
            row.update(kind='LC_RPATH' if cmd==0x8000001c else 'dylinker-or-environment-string',name=cstring(part,struct.unpack_from('<I',part,8)[0],12))
        elif cmd==2:
            need(length==24,'LC_SYMTAB command size')
            symoff,nsyms,stroff,strsize=struct.unpack_from('<4I',part,8)
            row.update(kind='LC_SYMTAB',symbol_count=nsyms)
            row['table_locations']=[dict(name='nlist_64',count=nsyms,element_bytes=16,**span(symoff,16*nsyms,image_size)),dict(name='string-table',**span(stroff,strsize,image_size))]
        elif cmd==0xb:
            need(length==80,'LC_DYSYMTAB command size')
            fields=struct.unpack_from('<18I',part,8)
            row.update(kind='LC_DYSYMTAB',symbol_index_ranges=dict(local=[fields[0],fields[1]],external_defined=[fields[2],fields[3]],undefined=[fields[4],fields[5]]))
            for name,pair,width in [('table-of-contents',6,8),('dylib-module64',8,56),('external-reference',10,4),('indirect-symbol',12,4),('external-relocation',14,8),('local-relocation',16,8)]:
                off,count=fields[pair:pair+2]
                row['table_locations'].append(dict(name=name,count=count,element_bytes=width,**span(off,count*width,image_size)))
        elif cmd in (0x22,0x80000022):
            need(length==48,'LC_DYLD_INFO command size')
            fields=struct.unpack_from('<10I',part,8);row['kind']='LC_DYLD_INFO'
            for i,name in enumerate(['rebase','bind','weak-bind','lazy-bind','export']):row['table_locations'].append(dict(name=name,**span(fields[2*i],fields[2*i+1],image_size)))
        elif cmd in (0x1d,0x1e,0x26,0x29,0x2b,0x2e,0x80000033,0x80000034):
            need(length==16,'linkedit-data command size')
            off,size=struct.unpack_from('<II',part,8);row['kind']='linkedit-data-location'
            row['table_locations']=[dict(name={0x1d:'code-signature',0x1e:'segment-split-info',0x26:'function-starts',0x29:'data-in-code',0x2b:'dylib-code-sign-drs',0x2e:'linker-optimization-hint',0x80000033:'exports-trie',0x80000034:'chained-fixups'}[cmd],**span(off,size,image_size))]
        elif cmd==0x80000028:
            need(length==24,'LC_MAIN command size')
            entry,stack=struct.unpack_from('<QQ',part,8);span(entry,1,image_size)
            row.update(kind='LC_MAIN',entry_file_offset=entry,stack_size=stack)
        elif cmd==0x1b:
            need(length==24,'LC_UUID command size');row.update(kind='LC_UUID',uuid_hex=part[8:24].hex())
        result.append(row);cursor+=length
    need(cursor==len(raw),'exact command-region coverage')
    symtabs=[r for r in result if r['kind']=='LC_SYMTAB']
    need(len(symtabs)<=1,'ambiguous symbol table command')
    for r in result:
        if r['kind']=='LC_DYSYMTAB' and symtabs:
            need(all(start+count<=symtabs[0]['symbol_count'] for start,count in r['symbol_index_ranges'].values()),'dynamic symbol indices outside symtab')
    return result


def save(name,value):
    data=value if isinstance(value,bytes) else (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    with (DEST/name).open('xb') as stream:
        stream.write(data);stream.flush();os.fsync(stream.fileno())


def capture(selected):
    need(sys.dont_write_bytecode,'capture requires -B')
    DEST.mkdir()
    state=dict(started_utc=utc(),selection_sha256=SELECTION_SHA,argv=sys.argv,phase='preflight',content_reads=[],content_bytes_read=0,children=0,original_calls=0,error=None,automatic_retry=False)
    save('attempt.json',state);watched=[];before=[];after=[]
    old_term=signal.getsignal(signal.SIGTERM)
    def interrupted(signum,frame):raise RuntimeError('interrupted by signal '+str(signum))
    signal.signal(signal.SIGTERM,interrupted)
    try:
        manifest=json.loads((HERE/'manifest-preparation.json').read_text())
        need({r['path'] for r in manifest['files']}=={p.name for p in HERE.iterdir() if p.is_file() and p.name!='manifest-preparation.json'},'exact preparation file inventory')
        for row in manifest['files']:verify(dict(row,path=str(HERE/row['path'])))
        watched=sorted({Path(IMAGE),ROOT_SELECTION,*[Path(p['path']) for p in selected['prerequisites']],*[p for p in HERE.iterdir() if p.is_file()]})
        before=[identity(p) for p in watched];save('before-identities.json',before)
        need(next(r for r in before if r['path']==IMAGE)==selected['future_image'],'fresh full selected-image identity')
        root_pin=next(r for r in before if r['path']==str(ROOT_SELECTION))
        need(root_pin['bytes']==3078 and root_pin['sha256']==SELECTION_SHA,'fresh fixed Root selection identity')
        for pin in selected['prerequisites']:
            need(next(r for r in before if r['path']==pin['path'])==pin,'fresh immutable document identity')
        state['phase']='two-bounded-metadata-content-reads'
        with Path(IMAGE).open('rb') as stream:
            raw=stream.read(32);state['content_reads'].append(dict(file_offset=0,bytes=len(raw)));state['content_bytes_read']+=len(raw)
            info=header(raw,IMAGE_SIZE);save('header.bin',raw)
            command_bytes=stream.read(info['sizeofcmds']);state['content_reads'].append(dict(file_offset=32,bytes=len(command_bytes)));state['content_bytes_read']+=len(command_bytes)
            need(state['content_bytes_read']<=65568,'total selected content budget')
            save('loadcommands.bin',command_bytes)
        parsed=commands(command_bytes,info,IMAGE_SIZE)
        save('metadata.json',dict(header=info,commands=parsed,content_bytes=state['content_bytes_read'],header_sha256=sha(raw),loadcommands_sha256=sha(command_bytes),tables_read=False,provider_binding='unknown',required_unsupported='U',coverage='OPEN'))
        need(state['content_bytes_read']==32+info['sizeofcmds'] and len(state['content_reads'])==2,'exact two-read content extent')
        state['phase']='captured-header-and-command-locations-only'
    except BaseException as failure:
        state['error']=type(failure).__name__+': '+str(failure)
        save('failure.json',dict(ended_utc=utc(),phase=state['phase'],error=state['error'],partial_artifacts_retained=True,automatic_retry=False))
    finally:
        for path in watched:
            try:after.append(identity(path))
            except Exception as failure:after.append(dict(path=str(path),error=type(failure).__name__+': '+str(failure)))
        state['watch_unchanged']=bool(before) and before==after
        if not state['watch_unchanged'] and state['error'] is None:
            state['error']='watched identities changed or incomplete'
            save('failure.json',dict(ended_utc=utc(),phase=state['phase'],error=state['error'],partial_artifacts_retained=True,automatic_retry=False))
        save('after-identities.json',dict(files=after,unchanged=state['watch_unchanged'],ended_utc=utc()))
        state['finished_utc']=utc();save('status.json',state);signal.signal(signal.SIGTERM,old_term)
    print(json.dumps(state,indent=2))
    return 0 if state['error'] is None and state['watch_unchanged'] else 1


def check():
    selected=plan();negatives=[]
    def rejected(name,action):
        try:action()
        except (ValueError,KeyError,struct.error):negatives.append(name)
        else:raise ValueError('negative accepted: '+name)
    def head(count,size,cpu=0x100000c):return struct.pack('<8I',0xfeedfacf,cpu,0,2,count,size,0,0)
    def parse(raw,count=1):return commands(raw,header(head(count,len(raw)),4096),4096)
    unknown=struct.pack('<II',0x12345678,8)
    need(parse(unknown)[0]['raw_hex']==unknown.hex(),'unknown command exact raw preservation')
    dylib=struct.pack('<6I',0xc,32,24,0,1,1)+b'x.dylib\0'
    need(parse(dylib)[0]['name']['text']=='x.dylib','dylib string inside command')
    rpath=struct.pack('<3I',0x8000001c,16,12)+b'@r\0\0'
    need(parse(rpath)[0]['name']['text']=='@r','rpath string')
    symtab=struct.pack('<6I',2,24,1024,1,2048,16)
    need(parse(symtab)[0]['table_locations'][0]['bytes']==16,'nlist location only')
    segment=struct.pack('<II16sQQQQiiII',0x19,72,b'__TEXT',4096,4096,0,4096,5,5,0,0)
    need(parse(segment)[0]['segment']['fileoff']==0,'synthetic segment mapping')
    section=struct.pack('<16s16sQQIIIIIIII',b'__text',b'__TEXT',4224,64,128,2,0,0,0,0,0,0)
    segment_section=bytearray(segment);struct.pack_into('<I',segment_section,4,152);struct.pack_into('<I',segment_section,64,1)
    segment_section=bytes(segment_section)+section
    need(parse(segment_section)[0]['sections'][0]['file_offset']==128,'file-backed section metadata')
    zero=bytearray(segment_section);struct.pack_into('<I',zero,120,5000);struct.pack_into('<I',zero,136,1)
    need(parse(bytes(zero))[0]['sections'][0]['zero_fill'],'zero-fill has no section payload read')
    dysymfields=[0,1]+[0]*16;dysymfields[12:14]=[1024,1]
    dysym=struct.pack('<20I',0xb,80,*dysymfields)
    need(parse(symtab+dysym,2)[1]['table_locations'][3]['bytes']==4,'indirect-symbol location only')
    dyld=struct.pack('<12I',0x80000022,48,1024,8,0,0,0,0,0,0,0,0)
    need(parse(dyld)[0]['table_locations'][0]['bytes']==8,'dyld-info location only')
    fixups=struct.pack('<4I',0x80000034,16,3072,8)
    need(parse(fixups)[0]['table_locations'][0]['name']=='chained-fixups','chained-fixups location only')

    for name,raw in [('short header',head(1,8)[:-1]),('wrong CPU',head(1,8,0x1000007)),('zero commands',head(0,8)),('excess commands',head(513,65536)),('short command region',head(1,0)),('oversized region',head(1,65544)),('header command-count/size mismatch',head(2,8))]:rejected(name,lambda raw=raw:header(raw,IMAGE_SIZE))
    rejected('header file bounds',lambda:header(head(1,8),39))
    rejected('command region truncation',lambda:commands(unknown[:-1],header(head(1,8),4096),4096))
    rejected('command length below8',lambda:parse(struct.pack('<II',1,0)))
    rejected('unaligned command length',lambda:parse(struct.pack('<II',1,9)+b'\0'*8))
    rejected('command extends region',lambda:parse(struct.pack('<II',1,16)))
    rejected('unaccounted region tail',lambda:parse(unknown+unknown))
    rejected('too many command headers',lambda:commands(unknown,dict(ncmds=2,sizeofcmds=8),4096))
    bad=bytearray(dylib);struct.pack_into('<I',bad,8,23);rejected('name offset inside prefix',lambda:parse(bytes(bad)))
    bad=bytearray(dylib);struct.pack_into('<I',bad,8,32);rejected('name offset outside command',lambda:parse(bytes(bad)))
    bad=bytearray(dylib);bad[-1]=65;rejected('missing name NUL',lambda:parse(bytes(bad)))
    rejected('table overflow arithmetic',lambda:span(U64,1,U64))
    rejected('table beyond file',lambda:parse(struct.pack('<6I',2,24,4090,1,2048,16)))
    bad=bytearray(segment);struct.pack_into('<Q',bad,48,4097);rejected('segment beyond file',lambda:parse(bytes(bad)))
    bad=bytearray(segment);struct.pack_into('<Q',bad,24,U64);rejected('segment virtual overflow',lambda:parse(bytes(bad)))
    bad=bytearray(segment);struct.pack_into('<I',bad,64,1);rejected('segment section count extent',lambda:parse(bytes(bad)))
    bad=bytearray(segment_section);struct.pack_into('<I',bad,120,4090);rejected('section file bounds',lambda:parse(bytes(bad)))
    bad=bytearray(segment);struct.pack_into('<I',bad,60,7);rejected('segment protections exceed maximum',lambda:parse(bytes(bad)))
    bad=bytearray(dysym);struct.pack_into('<I',bad,12,2);rejected('dynamic symbol index bounds',lambda:parse(symtab+bytes(bad),2))
    bad=bytearray(fixups);struct.pack_into('<I',bad,8,4090);rejected('fixup location beyond file',lambda:parse(bytes(bad)))
    badplan=copy.deepcopy(selected);badplan['maximum_content_bytes']=65569;rejected('Root content cap changed',lambda:validate_plan(badplan))
    badplan=copy.deepcopy(selected);badplan['future_image']['path']='/unselected';rejected('unselected image',lambda:validate_plan(badplan))
    badpin=copy.deepcopy(selected['prerequisites'][0]);badpin['sha256']='0'*64;rejected('source pin corruption',lambda:verify(badpin))
    need(not DEST.exists(),'no actual capture destination during preparation')
    print(json.dumps(dict(status='PASS-preparation-documents-and-synthetics-only',root_selection_sha256=SELECTION_SHA,prerequisite_documents=3,synthetic_negative_controls=negatives,positive_controls=['unknown command raw coverage','dylib name','rpath','symbol locations without payload','segment geometry','file-backed section','zero-fill section','indirect-symbol location','dyld-info location','chained-fixups location'],maximum_content_bytes=65568,image_or_binary_opened=False,children=0,original_calls=0,provider_binding='unknown',required_unsupported='U',coverage='OPEN',limits='No real header,command,payload,image hash or capture/failure/deadline path exercised; Root source/readiness/separate actual gates remain.'),indent=2))
    return 0


if __name__=='__main__':
    if sys.argv[1:]==['--check']:raise SystemExit(check())
    need(sys.argv[1:]==['--capture-once',SELECTION_SHA],'use --check or separately selected exact --capture-once digest; no retry/overrides')
    raise SystemExit(capture(plan()))
