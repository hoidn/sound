"""Two fixed M points: Mach-O and linker-start metadata, never instructions."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import os
import struct
import sys

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent/'reviews/automation-M-native-root-metadata-selection.json'
ROOT_SHA='eab887f6e30884451b7ec63ca50948ca5a492246a4599a56b38d511e4a6e41ae'
U64=(1<<64)-1


def need(value,message):
    if not value:raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def save(name,value):
    raw=value if isinstance(value,bytes) else (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    with (BASE/name).open('xb') as stream:
        stream.write(raw);stream.flush();os.fsync(stream.fileno())


def span(offset,size,limit):
    need(type(offset) is int and type(size) is int and 0<=offset<=limit and 0<=size<=limit-offset,'metadata bounds')


def selection():
    raw=(BASE/'selection-root.json').read_bytes()
    need(sha(raw)==ROOT_SHA and ROOT.read_bytes()==raw,'exact Root selection')
    plan=json.loads(raw)
    need([(x['architecture'],x['cpu_type'],x['entry']) for x in plan['targets']]==
         [('x86_64',0x1000007,'0x1011f2080'),('arm64',0x100000c,'0x1012132d8')],'exact ordered two points')
    need(plan['caps']==dict(targets=2,header_plus_commands_bytes_each=65536,load_commands_each=256,
         segments_each=32,sections_each=256,LC_function_starts_bytes_each=4194304,start_entries_each=1000000),'fixed metadata caps')
    need(plan['required_unsupported']=='U' and plan['coverage_gate']=='OPEN','no closure')
    for pin in plan['evidence']:
        b=Path(pin['path']).read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'evidence identity')
    return plan


def name(raw):
    head,sep,tail=raw.partition(b'\0');need(not sep or not any(tail),'fixed-name padding')
    s=head.decode('ascii');need(s and all(32<ord(c)<127 for c in s),'metadata name');return s


def point_mapping(info,address):
    rows=[s for s in info['sections'] if s['segment']=='__TEXT' and s['file_backed'] and s['executable']
          and s['addr']<=address<s['addr']+s['size']]
    need(len(rows)==1,'point needs unique file-backed executable TEXT section')
    s=rows[0]
    return dict(section=s['name'],file_offset=s['fileoff']+address-s['addr'],instruction_bytes_read=False)


def header(raw,target):
    span(0,32,len(raw));magic,cpu,subtype,kind,count,size,flags,reserved=struct.unpack_from('<8I',raw)
    need(magic==0xfeedfacf and cpu==target['cpu_type'] and kind==2 and reserved==0,'thin64littleendian selectedCPU executable')
    need(0<count<=256 and count<=size//8 and 32+size<=65536 and len(raw)==32+size,'exact bounded header commands')
    segments=[];sections=[];starts=[];cursor=32
    for index in range(count):
        span(cursor,8,len(raw));cmd,n=struct.unpack_from('<II',raw,cursor)
        need(n>=8 and n%8==0,'command size/alignment');span(cursor,n,len(raw))
        if cmd==0x19:
            need(n>=72,'segment header')
            _,_,sg,va,vs,fo,fs,mp,ip,ns,fl=struct.unpack_from('<II16sQQQQiiII',raw,cursor)
            need(n==72+80*ns and vs<=U64-va and fs<=vs and ip&~mp==0,'segment geometry')
            span(fo,fs,target['bytes']);sg=name(sg)
            segments.append(dict(name=sg,vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,
                initprot=ip,nsects=ns,flags=fl,command_index=index,command_file_offset=cursor))
            need(len(segments)<=32 and len(sections)+ns<=256,'segment/section caps')
            for j in range(ns):
                off=cursor+72+80*j;x=struct.unpack_from('<16s16sQQ8I',raw,off)
                sn,ss,addr,length,fileoff,align,reloff,nreloc,sf,r1,r2,r3=x
                need(name(ss)==sg and va<=addr<=va+vs and length<=va+vs-addr,'section virtual span')
                need(align<=31 and addr%(1<<align)==0,'section alignment')
                backed=(sf&255) not in [1,12,18]
                if backed and length:
                    span(fileoff,length,target['bytes'])
                    need(fo<=fileoff and fileoff+length<=fo+fs and fileoff==fo+addr-va,'section file mapping')
                sections.append(dict(name=name(sn),segment=sg,addr=addr,size=length,fileoff=fileoff,align=align,
                    flags=sf,file_backed=backed,executable=bool(ip&4) and bool(sf&0x80000400),
                    header_file_offset=off,relocation_fileoff=reloff,relocation_count=nreloc,reserved1=r1,reserved2=r2,reserved3=r3))
        elif cmd==0x26:
            need(n==16,'LC_FUNCTION_STARTS command size');_,_,off,length=struct.unpack_from('<4I',raw,cursor)
            need(0<length<=4194304,'LC_FUNCTION_STARTS byte cap');span(off,length,target['bytes'])
            starts.append(dict(command_index=index,command_file_offset=cursor,dataoff=off,datasize=length))
        cursor+=n
    need(cursor==len(raw) and len(starts)<=1,'exact commands and unique starts')
    need(len({s['name'] for s in segments})==len(segments),'unique segment names')
    need(len({(s['segment'],s['name']) for s in sections})==len(sections),'unique section names')
    for k,n in [('fileoff','filesize'),('vmaddr','vmsize')]:
        ranges=sorted((s[k],s[k]+s[n]) for s in segments if s[n]);need(all(a[1]<=b[0] for a,b in zip(ranges,ranges[1:])),'segment overlaps')
    for seg in segments:
        ranges=sorted((s['addr'],s['addr']+s['size']) for s in sections if s['segment']==seg['name'] and s['size'])
        need(all(a[1]<=b[0] for a,b in zip(ranges,ranges[1:])),'section overlaps')
    text=[s for s in segments if s['name']=='__TEXT' and s['filesize']];need(len(text)==1,'one file-backed TEXT')
    if starts:
        c=starts[0];need(sum(s['name']=='__LINKEDIT' and s['fileoff']<=c['dataoff'] and c['dataoff']+c['datasize']<=s['fileoff']+s['filesize'] for s in segments)==1,'starts LINKEDIT span')
    point=int(target['entry'],16);need(target['architecture']!='arm64' or point%4==0,'ARM point alignment')
    info=dict(header=dict(magic=hex(magic),cpu=cpu,subtype=subtype,filetype=kind,ncmds=count,sizeofcmds=size,
        flags=flags,reserved=reserved),segments=segments,sections=sections,text_vmaddr=text[0]['vmaddr'],
        starts_command=starts[0] if starts else None)
    info['selected_point_mapping']=point_mapping(info,point)
    return info


def uleb(raw,offset):
    start=offset;value=0
    for i in range(10):
        need(offset<len(raw),'truncated ULEB');b=raw[offset];offset+=1
        need(i!=9 or b<=1,'ULEB uint64 overflow');value|=(b&127)<<(7*i)
        if b<128:
            need(i==0 or b!=0,'noncanonical ULEB');return value,offset,raw[start:offset].hex()
    raise ValueError('overlong ULEB')


def linker_starts(raw,info,target):
    command=info['starts_command'];need(command is not None,'LC starts missing')
    need(len(raw)==command['datasize']<=4194304,'exact bounded LC table')
    offset=0;address=info['text_vmaddr'];entry=int(target['entry'],16)
    previous=current=nextrow=None;first=last=None;count=0;sentinel=None
    while offset<len(raw):
        start=offset;delta,offset,h=uleb(raw,offset)
        if delta==0:
            need(not any(raw[offset:]),'nonzero after sentinel');sentinel=start;break
        need(delta<=U64-address,'cumulative start overflow');address+=delta;count+=1
        need(count<=1000000,'start-entry cap')
        need(target['architecture']!='arm64' or address%4==0,'ARM declared-start alignment')
        mapping=point_mapping(info,address)
        row=dict(address=hex(address),file_offset=mapping['file_offset'],section=mapping['section'],
            uleb_payload_offset=start,uleb_file_offset=command['dataoff']+start,uleb_hex=h,delta=delta)
        first=first or row;last=row
        if address<entry:previous=row
        elif address==entry:current=row
        elif nextrow is None:nextrow=row
    need(sentinel is not None,'missing zero sentinel')
    return dict(status='exact-declared-start-metadata' if current else 'U-point-not-an-exact-declared-start',
        selected_entry=target['entry'],exact_declared_start=current is not None,previous_start=previous,
        current_start=current,next_start=nextrow,total_declared_starts=count,first_start=first,last_start=last,
        sentinel_payload_offset=sentinel,sentinel_file_offset=command['dataoff']+sentinel,
        trailing_zero_bytes=len(raw)-offset,payload_bytes=len(raw),payload_sha256=sha(raw),
        adjacent_starts_prove_body=False,instruction_bytes_read=False,required_unsupported='U',coverage_gate='OPEN')


def acquire():
    plan=selection();stamp=dict(started_utc=utc(),root_selection_sha256=ROOT_SHA,
        collector_sha256=sha(Path(__file__).read_bytes()),batch_attempts=1,automatic_retry=False)
    save('acquisition-attempt.json',stamp);receipt=dict(**stamp,image_opens=0,points=[],error=None,
        original_model_harness_decoder_calls=0)
    try:
        for target in plan['targets']:
            arch=target['architecture'];state=dict(architecture=arch,entry=target['entry'],started_utc=utc(),image_opens=0,error=None)
            receipt['points'].append(state)
            with Path(target['image_path']).open('rb') as stream:
                receipt['image_opens']+=1;state['image_opens']=1;a=os.fstat(stream.fileno());data=stream.read(target['bytes']+1);b=os.fstat(stream.fileno())
            need((a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns),'same-descriptor custody changed')
            need(len(data)==target['bytes'] and sha(data)==target['sha256'],'one whole-image custody hash')
            state['image_identity']=dict(path=target['image_path'],bytes=len(data),sha256=target['sha256'],
                same_descriptor_metadata_equal=True,device=a.st_dev,inode=a.st_ino,mtime_ns=a.st_mtime_ns,ctime_ns=a.st_ctime_ns)
            span(0,32,len(data));size=struct.unpack_from('<I',data,20)[0];need(32+size<=65536,'header acquisition cap')
            rawheader=data[:32+size];info=header(rawheader,target);command=info['starts_command']
            save(arch+'-header-loadcommands.bin',rawheader)
            if command is None:
                result=dict(status='U-LC_FUNCTION_STARTS-absent',exact_declared_start=False,adjacent_starts_prove_body=False)
            else:
                payload=data[command['dataoff']:command['dataoff']+command['datasize']]
                result=linker_starts(payload,info,target);save(arch+'-LC_FUNCTION_STARTS.bin',payload)
            output=dict(target=target,macho=info,linker_starts=result,no_instruction_or_original_execution=True,
                body_range_proven=False,required_unsupported='U',coverage_gate='OPEN')
            save(arch+'-metadata.json',output);state.update(status=result['status'],finished_utc=utc())
            del data
        need(receipt['image_opens']==2 and len(receipt['points'])==2,'all two acquisitions')
    except BaseException as error:
        receipt['error']=type(error).__name__+': '+str(error)
        if receipt['points']:receipt['points'][-1]['error']=receipt['error']
        save('failure.json',dict(error=receipt['error'],partial_files_retained=True,retry=False))
    receipt['finished_utc']=utc();save('acquisition-receipt.json',receipt)
    print(json.dumps(receipt,indent=2));return int(receipt['error'] is not None)


def synthetic(target):
    t=dict(target,bytes=8192,entry='0x100000410');payload=b'\x80\x08\x10\x10\0';commands=bytearray()
    commands+=struct.pack('<II16sQQQQiiII',0x19,152,b'__TEXT',0x100000000,4096,0,4096,5,5,1,0)
    commands+=struct.pack('<16s16sQQ8I',b'__text',b'__TEXT',0x100000400,3072,1024,0,0,0,0x80000400,0,0,0)
    commands+=struct.pack('<II16sQQQQiiII',0x19,72,b'__LINKEDIT',0x100001000,4096,4096,4096,1,1,0,0)
    commands+=struct.pack('<4I',0x26,16,4096,len(payload))
    raw=struct.pack('<8I',0xfeedfacf,t['cpu_type'],0,2,3,len(commands),0,0)+commands
    return t,raw,payload


def check():
    plan=selection();neg=[]
    def bad(label,action):
        try:action()
        except (ValueError,struct.error,UnicodeError):neg.append(label);return
        raise ValueError('accepted negative '+label)
    for target in plan['targets']:
        t,h,p=synthetic(target);info=header(h,t);r=linker_starts(p,info,t)
        need(r['exact_declared_start'] and [r[k]['address'] for k in ['previous_start','current_start','next_start']]==
             ['0x100000400','0x100000410','0x100000420'],'complete three-start positive')
        between=dict(t,entry='0x100000414');need(not linker_starts(p,info,between)['exact_declared_start'],'between-start stays U')
        bad(target['architecture']+' wrongCPU',lambda:header(h,dict(t,cpu_type=1)))
    t,h,p=synthetic(plan['targets'][0]);info=header(h,t)
    bad('truncated header',lambda:header(h[:31],t))
    for label,off,value in [('fat magic',0,0xcafebabe),('wrong kind',12,6),('reserved header',28,1),
         ('command count cap',16,257),('header byte cap',20,65536),('zero command size',36,0),('bad command alignment',36,151),('section count mismatch',96,2)]:
        x=bytearray(h);struct.pack_into('<I',x,off,value);bad(label,lambda x=x:header(x,t))
    bad('unmapped selected point',lambda:header(h,dict(t,entry='0x100010000')))
    q=copy.deepcopy(info);q['sections'].append(copy.deepcopy(q['sections'][0]));bad('ambiguous section mapping',lambda:point_mapping(q,0x100000410))
    bad('ULEB truncated',lambda:uleb(b'\x80',0));bad('ULEB noncanonical',lambda:uleb(b'\x81\0',0))
    bad('ULEB overflow',lambda:uleb(b'\xff'*9+b'\x02',0));bad('ULEB overlong',lambda:uleb(b'\x80'*11,0))
    for raw,n in [(b'\0',0),(b'\x7f',127),(b'\x80\x01',128),(b'\xff'*9+b'\x01',U64)]:need(uleb(raw,0)[:2]==(n,len(raw)),'ULEB positives')
    bad('wrong LC payload length',lambda:linker_starts(p[:-1],info,t))
    bad('nonzero after sentinel',lambda:linker_starts(b'\x80\x08\0\x01\0',info,t))
    bad('missing sentinel',lambda:linker_starts(b'\x80\x08\x10\x10\x10',info,t))
    bad('start outside instruction section',lambda:linker_starts(b'\x01\0\0\0\0',info,t))
    arm,ah,ap=synthetic(plan['targets'][1]);ai=header(ah,arm)
    bad('ARM misaligned declared start',lambda:linker_starts(b'\x81\x08\x10\x10\0',ai,arm))
    xr=linker_starts(b'\x81\x08\x10\x10\0',info,t);need(xr['total_declared_starts']==3,'x86 byte-aligned starts permitted')
    q=copy.deepcopy(info);q['starts_command']['datasize']=4194305;bad('LC payload byte cap',lambda:linker_starts(b'',q,t))
    q=copy.deepcopy(info);q['text_vmaddr']=U64-1;bad('cumulative start overflow',lambda:linker_starts(p,q,t))
    absent=bytearray(h[:-16]);struct.pack_into('<II',absent,16,2,len(absent)-32)
    need(header(absent,t)['starts_command'] is None,'absent LC remains a metadata gap')
    need(not (BASE/'acquisition-attempt.json').exists(),'exclusive acquisition marker absent')
    print(json.dumps(dict(status='PASS-synthetic-document-only',negative_count=len(neg),negatives=neg,
        positive_architectures=2,point_membership_and_three_neighbors=True,evidence_pins=3,image_opens=0,
        original_model_harness_decoder_calls=0),indent=2));return 0


def retained():
    plan=selection();receipt=json.loads((BASE/'acquisition-receipt.json').read_bytes())
    attempt=json.loads((BASE/'acquisition-attempt.json').read_bytes());source=Path(__file__).read_bytes()
    need(receipt['error'] is None and receipt['image_opens']==2 and len(receipt['points'])==2,'whole two-point receipt')
    need(receipt['collector_sha256']==attempt['collector_sha256']==sha(source),'exact acquired source')
    need(receipt['original_model_harness_decoder_calls']==0 and not receipt['automatic_retry'],'no original/model/decoder/retry')
    rows=[]
    for target,state in zip(plan['targets'],receipt['points']):
        arch=target['architecture'];raw=(BASE/(arch+'-header-loadcommands.bin')).read_bytes();info=header(raw,target)
        meta=json.loads((BASE/(arch+'-metadata.json')).read_bytes());need(meta['target']==target and meta['macho']==info,'all retained header geometry')
        need(all(state['image_identity'][k]==target[v] for k,v in [('path','image_path'),('bytes','bytes'),('sha256','sha256')]) and state['image_identity']['same_descriptor_metadata_equal'] is True and state['image_opens']==1,'recorded image custody')
        if info['starts_command'] is None:
            payload=b'';result=dict(status='U-LC_FUNCTION_STARTS-absent',exact_declared_start=False,adjacent_starts_prove_body=False)
            need(not (BASE/(arch+'-LC_FUNCTION_STARTS.bin')).exists(),'no invented missing LC payload')
        else:
            payload=(BASE/(arch+'-LC_FUNCTION_STARTS.bin')).read_bytes();result=linker_starts(payload,info,target)
        need(meta['linker_starts']==result and meta['body_range_proven'] is False and meta['required_unsupported']=='U' and meta['coverage_gate']=='OPEN','retained LC table/point joins')
        need(result['adjacent_starts_prove_body'] is False,'no body promotion')
        rows.append(dict(architecture=arch,entry=target['entry'],header_bytes=len(raw),LC_table_bytes=len(payload),
            exact_declared_start=result['exact_declared_start'],declared_starts=result.get('total_declared_starts'),
            previous=result.get('previous_start'),current=result.get('current_start'),next=result.get('next_start')))
    print(json.dumps(dict(status='PASS-retained-metadata-only',points=rows,new_image_opens=0,
        original_model_harness_decoder_calls=0,body_proof=False,required_unsupported='U',coverage_gate='OPEN'),indent=2));return 0


if __name__=='__main__':
    if sys.argv[1:]==['--check']:raise SystemExit(check())
    if sys.argv[1:]==['--check-retained']:raise SystemExit(retained())
    if sys.argv[1:]!=['--acquire-once',ROOT_SHA]:raise SystemExit('Fixed metadata selection only; no overrides/retries.')
    raise SystemExit(acquire())
