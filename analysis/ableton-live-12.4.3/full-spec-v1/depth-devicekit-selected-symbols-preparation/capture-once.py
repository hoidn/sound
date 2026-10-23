"""Fixed27 selected indirect/nlist/name declarations; --check uses documents/synthetic bytes only."""
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
ROOT_SELECTION=HERE.parent/'reviews/devicekit-selected-symbols-root-preparation-selection.json'
SELECTION_SHA='ec4314236c2f52c0e95315ec60d29b34c0aa763c8eaf84089521e87876701927'
DEST=HERE.with_name('depth-devicekit-selected-symbols-v1')
IMAGE='/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64'
IMAGE_SIZE=149711904
IMAGE_SHA='3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
INDIRECT=dict(name='indirect-symbol',count=49180,element_bytes=4,file_offset=138457952,bytes=196720)
NLIST=dict(name='nlist_64',count=50511,element_bytes=16,file_offset=137649776,bytes=808176)
STRINGS=dict(name='string-table',file_offset=138654672,bytes=9877448)
STAGE_CAPS=dict(indirect=108,nlist=432,names=110592)
CONTENT_CAP=111132
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


def span(offset,size,base,length):
    need(all(type(v) is int for v in [offset,size,base,length]) and min(offset,size,base,length)>=0,'nonnegative integer range')
    need(offset<=U64-size and base<=U64-length,'range overflow')
    need(base<=offset and offset+size<=base+length and offset+size<=IMAGE_SIZE,'selected table/image range bounds')
    return offset


def validate_selection(selected,metadata,geometry,boundary):
    need(selected['future_image']==dict(path=IMAGE,bytes=IMAGE_SIZE,sha256=IMAGE_SHA),'fixed thin consumer identity')
    need(selected['preparation_directory']==HERE.name and selected['future_capture_directory']==DEST.name,'fixed preparation/destination')
    need(selected['indirect_table']==INDIRECT and selected['nlist_table']==NLIST and selected['string_table']==STRINGS,'fixed declared tables')
    need(selected['maximum_stubs']==27 and selected['selected_occurrences']==37 and selected['maximum_content_bytes']==CONTENT_CAP and selected['maximum_capture_attempts']==1 and selected['automatic_retry'] is False and selected['future_children']==0,'fixed selection caps')
    need(selected['stage_caps']==dict(indirect_words_bytes=108,nlist_bytes=432,name_bytes_each_including_NUL=4096,total_name_bytes=110592),'fixed stage/name caps')
    need(len(selected['prerequisites'])==5,'five fixed immutable prerequisite documents')
    locations={loc['name']:loc for command in metadata['commands'] for loc in command['table_locations']}
    need(all(locations[t['name']]==t for t in [INDIRECT,NLIST,STRINGS]),'retained exact table locations')
    need(geometry['indirect_table_location']==INDIRECT and geometry['nlist_location']==NLIST and geometry['string_table_location']==STRINGS,'reviewed geometry table association')
    proposed=[{k:v for k,v in row.items() if k!='stub_ordinal'} for row in geometry['rows']]
    need(selected['selected_stub_rows']==proposed and len(proposed)==27,'exact reviewed27 selected stub rows')
    section=geometry['stub_section']
    sections=[s for command in metadata['commands'] for s in command.get('sections',[]) if s['name']=='__stubs']
    need(sections==[section] and section['reserved']==[0,12,0],'retained unique stub section geometry')
    groups={}
    for row in boundary:
        record=row['selected']['record'];groups.setdefault(record['callee'],[]).append(row)
    need(len(boundary)==37 and len(groups)==27,'retained37 occurrences/27stub groups')
    seen=[]
    for row in proposed:
        delta=int(row['stub_address'],16)-section['vmaddr']
        need(0<=delta<section['bytes'] and delta%12==0 and row['indirect_index']==delta//12,'reviewed stub slot arithmetic')
        need(row['bytes']==4 and row['indirect_word_file_offset']==INDIRECT['file_offset']+4*row['indirect_index'],'exact selected indirect-word offset')
        span(row['indirect_word_file_offset'],4,INDIRECT['file_offset'],INDIRECT['bytes'])
        members=groups[row['stub_address']]
        need(row['source_rows']==[r['id'] for r in members] and set(row['external_labels'])=={r['selected']['record']['callee_resolved'] for r in members},'exact source occurrence/label grouping')
        seen.extend(row['source_rows'])
    need(len(set(seen))==len(seen)==37,'no duplicated or omitted source occurrence')
    for table in [INDIRECT,NLIST,STRINGS]:
        span(table['file_offset'],table['bytes'],0,IMAGE_SIZE)
        if 'count' in table:need(table['count']*table['element_bytes']==table['bytes'],'declared table count-width extent')


def plan():
    raw=ROOT_SELECTION.read_bytes()
    need(len(raw)==11827 and sha(raw)==SELECTION_SHA,'fixed Root selection changed')
    selected=json.loads(raw)
    for pin in selected['prerequisites']:verify(pin)
    metadata=json.loads(Path(selected['prerequisites'][1]['path']).read_text())
    geometry=json.loads(Path(selected['prerequisites'][2]['path']).read_text())
    boundary=[json.loads(line) for line in Path(selected['prerequisites'][4]['path']).read_text().splitlines()]
    validate_selection(selected,metadata,geometry,boundary)
    return selected,metadata,geometry,boundary


def indirect(raw):
    need(len(raw)==4,'exact4-byte indirect word')
    value=struct.unpack('<I',raw)[0]
    flags=value&0xc0000000
    if flags:return dict(raw_value=value,special_flags=hex(flags),status='LOCAL/ABS/high-flag combination unresolved; no further lookup',nlist_index=None)
    need(value<NLIST['count'],'ordinary indirect index outside selected nlist table')
    return dict(raw_value=value,special_flags='0x0',status='ordinary raw nlist index; no provider binding',nlist_index=value)


def nlist_offset(index):
    need(type(index) is int and 0<=index<NLIST['count'],'selected nlist index bounds')
    return span(NLIST['file_offset']+16*index,16,NLIST['file_offset'],NLIST['bytes'])


def nlist_fields(raw):
    need(len(raw)==16,'exact16-byte nlist record')
    n_strx,n_type,n_sect,n_desc,n_value=struct.unpack('<IBBHQ',raw)
    need(n_strx<STRINGS['bytes'],'selected string-table index out of bounds')
    return dict(n_strx=n_strx,n_type=n_type,n_sect=n_sect,n_desc=n_desc,n_desc_high8_raw=n_desc>>8,n_value=n_value,status='raw declaration/type bits only; special or unsupported type unresolved; high8 is not universal library ordinal; n_value never followed')


def state_new():return dict(content_bytes_read=0,stage_bytes=dict(indirect=0,nlist=0,names=0),read_operations=0)


def take(reader,offset,size,state,stage):
    span(offset,size,0,IMAGE_SIZE)
    need(state['content_bytes_read']+size<=CONTENT_CAP and state['stage_bytes'][stage]+size<=STAGE_CAPS[stage],'aggregate/stage content cap')
    data=reader(offset,size)
    need(isinstance(data,bytes) and len(data)<=size,'bounded reader result')
    state['content_bytes_read']+=len(data);state['stage_bytes'][stage]+=len(data);state['read_operations']+=1
    return data


def name_bytes(read_byte,n_strx,buffer):
    need(type(n_strx) is int and 0<=n_strx<STRINGS['bytes'],'name string-table index bounds')
    limit=min(4096,STRINGS['bytes']-n_strx)
    for i in range(limit):
        offset=span(STRINGS['file_offset']+n_strx+i,1,STRINGS['file_offset'],STRINGS['bytes'])
        byte=read_byte(offset)
        buffer.extend(byte)
        need(len(byte)==1,'EOF in selected name')
        if byte==b'\0':return bytes(buffer)
    raise ValueError('selected name lacks NUL within4096bytes/declared string table')


def display_name(raw):
    need(raw.endswith(b'\0'),'name display requires terminating NUL')
    return dict(raw_hex=raw.hex(),text=raw[:-1].decode('utf-8',errors='backslashreplace'),empty_name=len(raw)==1,semantics='raw selected name only; empty/unsupported/invalidUTF8 conveys no provider identity')


def save(name,value):
    data=value if isinstance(value,bytes) else (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    with (DEST/name).open('xb') as stream:
        stream.write(data);stream.flush();os.fsync(stream.fileno())


def raw_receipt(tag,stage,offset,raw):
    path=tag+'.'+stage+'.bin';save(path,raw)
    receipt=dict(path=path,file_offset=offset,bytes=len(raw),sha256=sha(raw))
    save(tag+'.'+stage+'.location.json',receipt)
    return receipt


def capture(selected):
    need(sys.dont_write_bytecode,'capture requires -B')
    DEST.mkdir()
    state=dict(started_utc=utc(),selection_sha256=SELECTION_SHA,argv=sys.argv,phase='preflight',children=0,original_calls=0,error=None,automatic_retry=False,**state_new())
    save('attempt.json',state);watched=[];before=[];after=[];rows=[]
    old_term=signal.getsignal(signal.SIGTERM)
    def interrupted(signum,frame):raise RuntimeError('interrupted by signal '+str(signum))
    signal.signal(signal.SIGTERM,interrupted)
    try:
        manifest=json.loads((HERE/'manifest-preparation.json').read_text())
        need({r['path'] for r in manifest['files']}=={p.name for p in HERE.iterdir() if p.is_file() and p.name!='manifest-preparation.json'},'exact preparation inventory')
        for row in manifest['files']:verify(dict(row,path=str(HERE/row['path'])))
        watched=sorted({Path(IMAGE),ROOT_SELECTION,*[Path(p['path']) for p in selected['prerequisites']],*[p for p in HERE.iterdir() if p.is_file()]})
        before=[identity(p) for p in watched];save('before-identities.json',before)
        need(next(r for r in before if r['path']==IMAGE)==selected['future_image'],'fresh full selected-image identity')
        root_pin=next(r for r in before if r['path']==str(ROOT_SELECTION))
        need(root_pin['bytes']==11827 and root_pin['sha256']==SELECTION_SHA,'fresh fixed Root selection identity')
        for pin in selected['prerequisites']:need(next(r for r in before if r['path']==pin['path'])==pin,'fresh immutable document identity')
        # Unbuffered reads ensure selected names stop exactly at their first NUL.
        with Path(IMAGE).open('rb',buffering=0) as stream:
            def reader(offset,size):stream.seek(offset);return stream.read(size)
            state['phase']='27-selected-indirect-words'
            for selection in selected['selected_stub_rows']:
                tag=selection['stub_address'][2:];offset=selection['indirect_word_file_offset']
                raw=take(reader,offset,4,state,'indirect')
                row=dict(selection=selection,indirect_raw=raw_receipt(tag,'indirect',offset,raw))
                rows.append(row);row['indirect']=indirect(raw)
            need(len(rows)==27 and state['stage_bytes']['indirect']==108,'exact selected indirect stage')
            state['phase']='selected-nlist-records'
            for row in rows:
                index=row['indirect']['nlist_index']
                if index is None:continue
                offset=nlist_offset(index);tag=row['selection']['stub_address'][2:]
                raw=take(reader,offset,16,state,'nlist')
                row['nlist_raw']=raw_receipt(tag,'nlist',offset,raw);row['nlist']=nlist_fields(raw)
            state['phase']='selected-bounded-names'
            for row in rows:
                if 'nlist' not in row:continue
                tag=row['selection']['stub_address'][2:];strx=row['nlist']['n_strx'];buffer=bytearray()
                try:
                    raw=name_bytes(lambda offset:take(reader,offset,1,state,'names'),strx,buffer)
                    row['name']=display_name(raw)
                finally:
                    row['name_raw']=raw_receipt(tag,'name',STRINGS['file_offset']+strx,bytes(buffer))
            save('selected-joins.json',dict(rows=rows,provider_binding='unknown',required_unsupported='U',coverage='OPEN',n_value_followed=False,n_desc_high8_is_universal_ordinal=False,duplicate_policy='No cache; each of27selectedstub rows retains its own bounded record/name reads, even when indices/strx repeat.'))
        need(state['content_bytes_read']==sum(state['stage_bytes'].values())<=CONTENT_CAP,'exact aggregate content accounting')
        state['phase']='captured-selected-raw-declarations-only'
    except BaseException as failure:
        state['error']=type(failure).__name__+': '+str(failure)
        save('failure.json',dict(ended_utc=utc(),phase=state['phase'],error=state['error'],partial_artifacts_retained=True,automatic_retry=False))
        save('partial-joins.json',dict(rows=rows,provider_binding='unknown',coverage='OPEN'))
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
    selected,metadata,geometry,boundary=plan();negative=[]
    def rejected(name,action):
        try:action()
        except (ValueError,KeyError,struct.error):negative.append(name)
        else:raise ValueError('negative accepted: '+name)
    need(indirect(struct.pack('<I',50510))['nlist_index']==50510,'last valid ordinary index')
    for value in [0x80000000,0x40000000,0xc0000011]:need(indirect(struct.pack('<I',value))['nlist_index'] is None,'special flags stop unresolved')
    rejected('truncated indirect word',lambda:indirect(b'\0'*3))
    rejected('ordinary index outside nlist',lambda:indirect(struct.pack('<I',50511)))
    rejected('large ordinary nonflag index',lambda:indirect(struct.pack('<I',0x20000000)))
    rejected('negative nlist index',lambda:nlist_offset(-1))
    rejected('out-of-bounds nlist record',lambda:nlist_offset(50511))
    need(nlist_offset(50510)+16==NLIST['file_offset']+NLIST['bytes'],'last exact nlist extent')
    raw=struct.pack('<IBBHQ',0,1,0,0xff01,U64)
    fields=nlist_fields(raw);need(fields['n_desc_high8_raw']==255 and fields['n_value']==U64,'raw nlist bits/value preserved without follow')
    unsupported=nlist_fields(struct.pack('<IBBHQ',0,255,255,0xffff,U64))
    need(unsupported['n_type']==255 and 'unresolved' in unsupported['status'],'unsupported nlist type remains raw unknown')
    rejected('truncated nlist',lambda:nlist_fields(raw[:-1]))
    rejected('n_strx outside string table',lambda:nlist_fields(struct.pack('<IBBHQ',STRINGS['bytes'],1,0,0,0)))
    seen=[]
    def fake(data):
        def byte(offset):
            seen.append(offset);index=offset-STRINGS['file_offset'];return data[index:index+1]
        return byte
    seen.clear();rawname=name_bytes(fake(b'ab\0UNREAD'),0,bytearray())
    need(rawname==b'ab\0' and len(seen)==3,'stop at first NUL without overread')
    need(display_name(name_bytes(fake(b'\0'),0,bytearray()))['empty_name'],'empty name raw unknown accepted')
    need(display_name(name_bytes(fake(b'\xff\0'),0,bytearray()))['text']=='\\xff','invalid UTF8 escaped with raw bytes retained')
    seen.clear();rejected('EOF before name NUL',lambda:name_bytes(fake(b'ab'),0,bytearray()));need(len(seen)==3,'EOF stops immediately')
    seen.clear();rejected('unterminated4096-byte name',lambda:name_bytes(fake(b'a'*4096),0,bytearray()));need(len(seen)==4096,'exact4096name cap')
    seen.clear();need(len(name_bytes(fake(b'a'*4095+b'\0'),0,bytearray()))==4096 and len(seen)==4096,'4096inclusive-NUL boundary accepted')
    seen.clear();rejected('NUL at byte4097 excluded',lambda:name_bytes(fake(b'a'*4096+b'\0'),0,bytearray()));need(len(seen)==4096,'no overread to4097')
    seen.clear();last=STRINGS['bytes']-1
    need(name_bytes(lambda off:b'\0',last,bytearray())==b'\0','last string-table byte NUL accepted')
    calls=[]
    def last_nonzero(off):calls.append(off);return b'x'
    rejected('unterminated at string-table end',lambda:name_bytes(last_nonzero,last,bytearray()));need(len(calls)==1,'no byte outside string table')
    rejected('string index OOB',lambda:name_bytes(fake(b'\0'),STRINGS['bytes'],bytearray()))
    rejected('negative string index',lambda:name_bytes(fake(b'\0'),-1,bytearray()))
    need([indirect(struct.pack('<I',7))['nlist_index'] for _ in range(2)]==[7,7],'duplicate ordinary indices permitted')
    dup=state_new()
    for _ in range(2):
        r=take(lambda off,size:struct.pack('<IBBHQ',0,1,0,0,0),nlist_offset(7),16,dup,'nlist')
        need(nlist_fields(r)['n_strx']==0,'duplicate records separately bounded')
        need(name_bytes(lambda off:take(lambda *_:b'\0',off,1,dup,'names'),0,bytearray())==b'\0','duplicate names separately bounded')
    need(dup['stage_bytes']['nlist']==32 and dup['stage_bytes']['names']==2,'duplicate read accounting')
    exhausted=state_new();exhausted['content_bytes_read']=CONTENT_CAP
    rejected('aggregate cap before read',lambda:take(lambda *_:b'x',STRINGS['file_offset'],1,exhausted,'names'))
    exhausted=state_new();exhausted['stage_bytes']['names']=STAGE_CAPS['names']
    rejected('name stage cap before read',lambda:take(lambda *_:b'x',STRINGS['file_offset'],1,exhausted,'names'))
    rejected('range overflow',lambda:span(U64,1,0,U64))
    rejected('range outside table',lambda:span(NLIST['file_offset']-1,16,NLIST['file_offset'],NLIST['bytes']))
    for name,key,value in [('wrong aggregate cap','maximum_content_bytes',111133),('extra selected row','maximum_stubs',28)]:
        changed=copy.deepcopy(selected);changed[key]=value
        rejected(name,lambda changed=changed:validate_selection(changed,metadata,geometry,boundary))
    changed=copy.deepcopy(selected);changed['selected_stub_rows'][0]['indirect_word_file_offset']+=4
    rejected('changed selected word offset',lambda:validate_selection(changed,metadata,geometry,boundary))
    changed=copy.deepcopy(selected);changed['nlist_table']['bytes']+=16
    rejected('changed nlist table bounds',lambda:validate_selection(changed,metadata,geometry,boundary))
    badpin=copy.deepcopy(selected['prerequisites'][0]);badpin['sha256']='0'*64
    rejected('immutable document pin corruption',lambda:verify(badpin))
    need(not DEST.exists(),'no actual capture destination during preparation')
    print(json.dumps(dict(status='PASS-preparation-documents-and-synthetics-only',root_selection_sha256=SELECTION_SHA,prerequisite_documents=5,selected_stub_rows=27,selected_occurrences=37,synthetic_negative_controls=negative,positive_controls=['ordinary lastindex','LOCAL/ABS flag combinations stop','raw nlist/type/high8/value','unsupported type remains unknown','4096inclusive-NUL boundary','NUL exact stop','empty name','invalidUTF8 escaped','last string byte','duplicate index/record accounting'],maximum_content_bytes=CONTENT_CAP,image_or_binary_opened=False,children=0,original_calls=0,provider_binding='unknown',required_unsupported='U',coverage='OPEN',limits='No actual selected table/name/header/image/hash/provider reads; external Root source/readiness/separate actual gates remain.'),indent=2))
    return 0


if __name__=='__main__':
    if sys.argv[1:]==['--check']:raise SystemExit(check())
    need(sys.argv[1:]==['--capture-once',SELECTION_SHA],'use --check or separately selected exact --capture-once digest; no retry/overrides')
    raise SystemExit(capture(plan()[0]))
