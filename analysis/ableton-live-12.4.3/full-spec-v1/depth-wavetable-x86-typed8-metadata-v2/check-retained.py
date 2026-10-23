"""Read only this retained metadata packet and its five immutable document pins."""
from pathlib import Path
import copy
import hashlib
import json
import struct

BASE=Path(__file__).resolve().parent
SHA='01a8c9aba288b4082c86782d1edc23331d78cb6731485e68fc93a56493dc14e1'


def need(value,message):
    if not value:raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def leb(raw):
    b=bytes.fromhex(raw);need(0<len(b)<=10,'selected ULEB length');value=0
    for i,x in enumerate(b):
        need((x<128)==(i==len(b)-1),'selected ULEB terminator')
        need(i!=9 or x<=1,'selected ULEB overflow');value|=(x&127)<<(7*i)
    need(len(b)==1 or b[-1]!=0,'selected ULEB canonical');return value


def verify(meta,plan,receipt,attempt,header):
    need(meta['selection_sha256']==receipt['selection_sha256']==attempt['selection_sha256']==SHA,'selection joins')
    need(receipt['acquisition_attempts']==attempt['acquisition_attempts']==receipt['image_opens']==1,'one acquisition')
    need(receipt['original_model_harness_decoder_calls']==0 and receipt['automatic_retry'] is False and receipt['error'] is None,'no execution/retry')
    need(all(receipt['image_identity'][k]==v for k,v in plan['image'].items()) and receipt['image_identity']['descriptor_before_after_equal'] is True,'recorded image custody only')
    need(meta['no_instruction_decoder_or_original_execution'] is True and meta['complete_table_or_ABI_proof'] is False,'metadata scope')
    info=meta['macho'];r=meta['result'];types=r['types'];raws=r['selected_ranges']
    need(r['status']==receipt['result_status']=='COMPLETE-BOUNDED-METADATA' and r['full_prefix_materialization'] is True,'whole metadata result')
    need(r['required_unsupported']=='U' and r['coverage_gate']=='OPEN','no behavior promotion')
    need(len(types)==8 and [(t['type_encoding'],t['ARM_slot3_entry'],t['ARM_address_point']) for t in types]==[(t['type_encoding'],t['ARM_slot3_entry'],t['ARM_address_point']) for t in plan['whole_typed_set']],'whole ordered8')
    need(len(raws)==40 and len({(x['kind'],x['va'],x['bytes']) for x in raws})==40,'all retained40metadata ranges')
    def mapping(va,size,allowed):
        segs=[s for s in info['segments'] if s['name'] in allowed and s['vmaddr']<=va and va+size<=s['vmaddr']+s['filesize']]
        need(len(segs)==1,'unique retained segment mapping');s=segs[0];return s['fileoff']+va-s['vmaddr']
    def raw(kind,va,size,allowed):
        matches=[x for x in raws if x['kind']==kind and int(x['va'],16)==va and x['bytes']==size]
        need(len(matches)==1,'one exact retained selected span');x=matches[0];b=bytes.fromhex(x['hex'])
        need(len(b)==size and digest(b)==x['sha256'] and x['file_offset']==mapping(va,size,allowed),'retained raw/hash/geometry');return b
    targets=[];preceding=[]
    for t in types:
        need(t['status']=='exact-typed-primary-six-slot-metadata-only' and t['name_match_count']==len(t['name_matches'])==len(t['typeinfo_candidates'])==len(t['table_headers'])==len(t['primary_tables'])==1,'complete unique joins per type')
        need(not t['unjoined_name_pointer_refs'] and not t['unjoined_typeinfo_pointer_refs'],'no hidden unjoined pointers')
        n=t['name_matches'][0];ti=t['typeinfo_candidates'][0];h=t['table_headers'][0]
        b=raw('exact-trailing-NUL-type-name',n['va'],len(t['type_encoding'])+1,['__TEXT'])
        need(b==t['type_encoding'].encode()+b'\0' and n['file_offset']==mapping(n['va'],1,['__TEXT']),'exact trailingNUL literal')
        p=raw('selected-name-preceding-byte',n['va']-1,1,['__TEXT'])
        need(p.hex()==n['preceding_byte_hex'] and n['preceding_file_offset']==n['file_offset']-1,'preceding byte locator');preceding.append(p.hex())
        b=raw('candidate-typeinfo-two-qword-head',ti['va'],16,['__DATA','__DATA_CONST']);vp,name=struct.unpack('<QQ',b)
        need(name==ti['name_va']==n['va'] and ti['name_pointer_field_va']==ti['va']+8 and ti['file_offset']==mapping(ti['va'],16,['__DATA','__DATA_CONST']),'exact name pointer join')
        need(vp==16 and ti['header_hex']==b.hex() and ti['vptr_unresolved']=='0x10','raw unresolved vptr')
        b=raw('offset-to-top-and-typeinfo-header',h['header_va'],16,['__DATA','__DATA_CONST']);top,tiva=struct.unpack('<qQ',b)
        need(top==h['offset_to_top']==0 and tiva==h['typeinfo_va']==ti['va'] and h['file_offset']==mapping(h['header_va'],16,['__DATA','__DATA_CONST']),'primary header identity join')
        need(h['address_point']==h['header_va']+16 and h['raw_header_hex']==b.hex() and t['primary_tables']==[h],'address point/raw header')
        b=raw('whole-six-qword-primary-prefix',h['address_point'],48,['__DATA','__DATA_CONST']);words=struct.unpack('<6Q',b)
        need(len(t['slots'])==6,'whole six slots')
        for i,(s,address) in enumerate(zip(t['slots'],words)):
            need(s['index']==i and int(s['field_va'],16)==h['address_point']+8*i and int(s['target'],16)==address and s['selected_instruction_bytes']==0,'raw slot word joins')
            sections=[x for x in info['sections'] if x['segment']=='__TEXT' and x['executable'] and x['file_backed'] and x['addr']<=address<x['addr']+x['size']]
            need(len(sections)==1,'unique executable section metadata');section=sections[0]
            need(s['mapping']==dict(status='unique-executable-TEXT-section-metadata',section=section['name'],file_offset=section['fileoff']+address-section['addr'],instruction_bytes_read=False),'target metadata only')
            targets.append(address)
    need(preceding==['3e']+['00']*7,'observed preceding bytes, not P suffix mechanism')
    counts=dict.fromkeys(['name_matches','aligned_name_pointer_refs','typeinfo_candidates','aligned_typeinfo_pointer_refs','table_headers','primary_tables'],8);counts['primary_slots']=48
    need(r['counts']==receipt['counts']==counts and len(targets)==len(set(targets))==48,'whole8 and48target counts')
    need({x['kind'] for x in raws}=={'exact-trailing-NUL-type-name','selected-name-preceding-byte','candidate-typeinfo-two-qword-head','offset-to-top-and-typeinfo-header','whole-six-qword-primary-prefix'},'selected metadata spans only')
    need(len(header)==32+info['header']['sizeofcmds'] and len(header)+len((json.dumps(meta,indent=2,allow_nan=False)+'\n').encode())==receipt['retained_selected_metadata_bytes']<=1048576,'retention cap')
    fs=r['function_starts'];command=info['starts_command'];end=command['dataoff']+command['datasize']
    need(fs['status']=='strict-linker-metadata-only' and fs['command']==command and 0<command['datasize']<=4194304 and 0<fs['count']<=1000000 and fs['body_proof'] is False and fs['full_payload_retained'] is False,'strict bounded linker metadata')
    need(fs['sentinel_file_offset']+1+fs['trailing_zero_bytes']==end and fs['trailing_zero_bytes']>=0,'recorded sentinel extent')
    need(int(fs['first']['address'],16)==info['text']['vmaddr']+leb(fs['first']['uleb_hex']),'first selected ULEB')
    need(len(fs['payload_sha256'])==64 and len(fs['targets'])==48 and [int(x['target'],16) for x in fs['targets']]==sorted(targets),'all target starts rows')
    for x in fs['targets']:
        target=int(x['target'],16);prev=x['previous_or_equal_start'];nxt=x['next_start']
        need(x['exact_declared_start'] is True and x['body_range_proven'] is False and int(prev['address'],16)==target and target<int(nxt['address'],16),'conditional target next-start relation')
        need(int(nxt['address'],16)-target==leb(nxt['uleb_hex']),'retained next ULEB delta')
        for row in [prev,nxt]:
            need(command['dataoff']<=row['uleb_file_offset'] and row['uleb_file_offset']+len(bytes.fromhex(row['uleb_hex']))<=fs['sentinel_file_offset'],'selected ULEB payload coordinates')
            need(row['file_offset']==mapping(int(row['address'],16),1,['__TEXT']),'starts target file mapping');leb(row['uleb_hex'])
    magic,cpu,subtype,kind,count,size,flags,reserved=struct.unpack_from('<8I',header)
    need((hex(magic),hex(cpu),hex(subtype),kind,count,size,hex(flags),reserved)==tuple(info['header'][k] for k in ['magic','cpu','subtype','filetype','ncmds','sizeofcmds','flags','reserved']),'retained header fields')
    cursor=32;segs=[];sects=[];starts=[]
    for i in range(count):
        cmd,n=struct.unpack_from('<II',header,cursor);need(n>=8 and n%8==0 and cursor+n<=len(header),'command bounds')
        if cmd==0x19:
            _,_,name,va,vs,fo,fs,mp,ip,ns,fl=struct.unpack_from('<II16sQQQQiiII',header,cursor)
            need(n==72+80*ns,'segment section extent');sg=name.rstrip(b'\0').decode()
            segs.append((sg,va,vs,fo,fs,mp,ip,i,cursor,ns,fl))
            for j in range(ns):
                x=struct.unpack_from('<16s16sQQ8I',header,cursor+72+80*j)
                sects.append((x[0].rstrip(b'\0').decode(),x[1].rstrip(b'\0').decode(),*x[2:]))
        elif cmd==0x26:
            _,_,off,length=struct.unpack_from('<4I',header,cursor);starts.append(dict(command_index=i,command_file_offset=cursor,dataoff=off,datasize=length))
        cursor+=n
    need(cursor==len(header),'full command extent')
    need(segs==[tuple(s[k] for k in ['name','vmaddr','vmsize','fileoff','filesize','maxprot','initprot','command_index','command_file_offset','section_count','flags']) for s in info['segments']],'all segment records')
    need(sects==[tuple(s[k] for k in ['name','segment','addr','size','fileoff','align','relocation_fileoff','relocation_count','flags','reserved1','reserved2','reserved3']) for s in info['sections']],'all section records')
    need(starts==[info['starts_command']],'LC starts command metadata only')


def main():
    selection=(BASE/'selection-root.json').read_bytes();need(digest(selection)==SHA,'root selection seal');p=json.loads(selection)
    m=json.loads((BASE/'metadata.json').read_bytes());r=json.loads((BASE/'acquisition-receipt.json').read_bytes());a=json.loads((BASE/'acquisition-attempt.json').read_bytes());h=(BASE/'header-loadcommands.bin').read_bytes()
    for pin in p['inputs']:
        b=Path(pin['path']).read_bytes();need(len(b)==pin['bytes'] and digest(b)==pin['sha256'],'immutable document pin')
    code=(BASE/'collect-metadata-once.py').read_bytes();check=json.loads((BASE/'author-check.json').read_bytes())
    need(digest(code)==a['collector_sha256']==r['collector_sha256']==check['collector']['sha256'],'exact acquired collector source')
    verify(m,p,r,a,h);neg=[]
    def rejected(name,mutate):
        q=copy.deepcopy(m);rr=copy.deepcopy(r);mutate(q,rr)
        try:verify(q,p,rr,a,h)
        except (ValueError,KeyError,IndexError,struct.error):neg.append(name);return
        raise ValueError('accepted false promotion '+name)
    rejected('drop whole eighth type',lambda q,r:q['result']['types'].pop())
    rejected('substitute exact type spelling',lambda q,r:q['result']['types'][0].update(type_encoding='P'+q['result']['types'][0]['type_encoding']))
    rejected('hide nonNUL prior byte',lambda q,r:q['result']['types'][0]['name_matches'][0].update(preceding_byte_hex='00'))
    rejected('invent P prefix mechanism',lambda q,r:q['result']['types'][0]['name_matches'][0].update(preceding_byte_hex='50'))
    rejected('name pointer changed',lambda q,r:q['result']['types'][1]['typeinfo_candidates'][0].update(name_va=0))
    rejected('loaded vptr invented',lambda q,r:q['result']['types'][2]['typeinfo_candidates'][0].update(vptr_unresolved='0x100000010'))
    rejected('drop sixth slot',lambda q,r:q['result']['types'][3]['slots'].pop())
    rejected('slot target changed',lambda q,r:q['result']['types'][4]['slots'][3].update(target='0x100000000'))
    rejected('target instructions acquired',lambda q,r:q['result']['types'][5]['slots'][3].update(selected_instruction_bytes=1))
    rejected('function body inferred',lambda q,r:q['result']['function_starts'].update(body_proof=True))
    rejected('LC next-start delta changed',lambda q,r:q['result']['function_starts']['targets'][0]['next_start'].update(uleb_hex='11'))
    rejected('starts count exceeds cap',lambda q,r:q['result']['function_starts'].update(count=1000001))
    rejected('wrong image identity receipt',lambda q,r:r['image_identity'].update(sha256='0'*64))
    rejected('second acquisition invented',lambda q,r:r.update(image_opens=2))
    rejected('decoder call invented',lambda q,r:r.update(original_model_harness_decoder_calls=1))
    rejected('unknown coverage closed',lambda q,r:q['result'].update(coverage_gate='CLOSED'))
    print(json.dumps(dict(status='PASS-retained-data-only',types=8,candidate_typeinfos=8,primary_headers=8,prefixes=8,slots=48,selected_ranges=40,negative_count=len(neg),negatives=neg,new_image_or_decoder_original_model_harness_reads_calls=0,required_unsupported='U',coverage_gate='OPEN'),indent=2))


if __name__=='__main__':
    main()
