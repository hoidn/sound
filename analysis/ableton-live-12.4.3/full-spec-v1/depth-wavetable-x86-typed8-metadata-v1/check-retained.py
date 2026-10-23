"""Read only this retained metadata packet and its three immutable document pins."""
from pathlib import Path
import copy
import hashlib
import json
import struct

BASE=Path(__file__).resolve().parent
SHA='69a810c15eabcbfff67bb813cd9e63d199cf29cdc58191d1cd768334bcb7b1a0'


def need(value,message):
    if not value:raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def verify(meta,plan,receipt,attempt,header):
    need(meta['selection_sha256']==SHA and receipt['selection_sha256']==attempt['selection_sha256']==SHA,'selection joins')
    need(receipt['acquisition_attempts']==attempt['acquisition_attempts']==receipt['image_opens']==1,'one acquisition')
    need(receipt['original_model_harness_decoder_calls']==0 and receipt['automatic_retry'] is False and receipt['error'] is None,'no execution/retry')
    need(all(receipt['image_identity'][k]==v for k,v in plan['image'].items()) and receipt['image_identity']['descriptor_before_after_equal'] is True,'recorded image custody only')
    need(meta['no_instruction_decoder_or_original_execution'] is True and meta['complete_table_or_ABI_proof'] is False,'metadata scope')
    r=meta['result'];need(r['status']=='REFUSED-U' and receipt['result_status']==r['status'] and r['full_prefix_materialization'] is False,'whole-set refusal')
    need(r['required_unsupported']=='U' and r['coverage_gate']=='OPEN' and 'function_starts' not in r,'no promotion or starts follow after refusal')
    need(len(r['types'])==8 and [(t['type_encoding'],t['ARM_slot3_entry'],t['ARM_address_point']) for t in r['types']]==
         [(t['type_encoding'],t['ARM_slot3_entry'],t['ARM_address_point']) for t in plan['whole_typed_set']],'whole ordered8')
    need(any(len(t['name_matches'])!=1 or len(t['typeinfo_candidates'])!=1 or len(t['primary_tables'])!=1 for t in r['types']),'genuine missing/ambiguous join')
    info=meta['macho'];raws=r['selected_ranges'];need(len(raws)==21,'all retained21metadata ranges')
    def mapping(va,size,allowed):
        segs=[s for s in info['segments'] if s['name'] in allowed and s['vmaddr']<=va and va+size<=s['vmaddr']+s['filesize']]
        need(len(segs)==1,'unique retained segment mapping');s=segs[0];return s['fileoff']+va-s['vmaddr']
    def raw(kind,va,size,allowed):
        matches=[x for x in raws if x['kind']==kind and int(x['va'],16)==va and x['bytes']==size]
        need(len(matches)==1,'one exact retained selected span');x=matches[0];b=bytes.fromhex(x['hex'])
        need(len(b)==size and digest(b)==x['sha256'] and x['file_offset']==mapping(va,size,allowed),'retained raw/hash/geometry');return b
    for t in r['types']:
        need(t['status']=='U' and 'slots' not in t and t['name_match_count']==len(t['name_matches']),'no first7 prefix or name promotion')
        for n in t['name_matches']:
            b=raw('exact-NUL-bounded-type-name',n['va']-1,len(t['type_encoding'])+2,['__TEXT'])
            need(b==b'\0'+t['type_encoding'].encode()+b'\0' and n['file_offset']==mapping(n['va'],1,['__TEXT']),'exact bounded literal')
        for ti in t['typeinfo_candidates']:
            b=raw('candidate-typeinfo-two-qword-head',ti['va'],16,['__DATA','__DATA_CONST'])
            vp,name=struct.unpack('<QQ',b)
            need(name==ti['name_va'] and any(n['va']==name for n in t['name_matches']) and ti['name_pointer_field_va']==ti['va']+8,'name-pointer/typeinfo join')
            need(ti['header_hex']==b.hex() and ti['vptr_unresolved']==hex(vp),'raw unresolved vptr')
        for h in t['table_headers']:
            b=raw('offset-to-top-and-typeinfo-header',h['header_va'],16,['__DATA','__DATA_CONST']);top,ti=struct.unpack('<qQ',b)
            need(top==h['offset_to_top'] and ti==h['typeinfo_va'] and any(x['va']==ti for x in t['typeinfo_candidates']),'header identity join')
            need(h['address_point']==h['header_va']+16 and h['raw_header_hex']==b.hex(),'address point/raw header')
        need(t['primary_tables']==[h for h in t['table_headers'] if h['offset_to_top']==0],'all primary candidates')
    counts=dict(name_matches=sum(len(t['name_matches']) for t in r['types']),
        aligned_name_pointer_refs=sum(len(t['typeinfo_candidates'])+len(t['unjoined_name_pointer_refs']) for t in r['types']),
        typeinfo_candidates=sum(len(t['typeinfo_candidates']) for t in r['types']),
        aligned_typeinfo_pointer_refs=sum(len(t['table_headers'])+len(t['unjoined_typeinfo_pointer_refs']) for t in r['types']),
        table_headers=sum(len(t['table_headers']) for t in r['types']),primary_tables=sum(len(t['primary_tables']) for t in r['types']))
    need(r['counts']==receipt['counts']==counts==dict.fromkeys(counts,7),'complete seven candidate census')
    need({x['kind'] for x in raws}=={'exact-NUL-bounded-type-name','candidate-typeinfo-two-qword-head','offset-to-top-and-typeinfo-header'},'no target/slot/native raw retention')
    need(len(header)==32+info['header']['sizeofcmds'] and len(header)+len(json.dumps(meta,indent=2,allow_nan=False).encode())+1==receipt['retained_selected_metadata_bytes']<=1048576,'retention cap')
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
        except ValueError:neg.append(name);return
        raise ValueError('accepted false promotion '+name)
    rejected('drop missing type from whole8',lambda q,r:q['result']['types'].pop(0))
    rejected('promote refused7 to complete8',lambda q,r:q['result'].update(status='COMPLETE-BOUNDED-METADATA'))
    rejected('first7 slot materialization invented',lambda q,r:q['result']['types'][1].update(slots=[]))
    rejected('missing literal count promoted',lambda q,r:q['result']['types'][0].update(name_match_count=1))
    rejected('wrong image identity receipt',lambda q,r:r['image_identity'].update(sha256='0'*64))
    rejected('second image acquisition invented',lambda q,r:r.update(image_opens=2))
    rejected('decoder call invented',lambda q,r:r.update(original_model_harness_decoder_calls=1))
    rejected('unknown coverage closed',lambda q,r:q['result'].update(coverage_gate='CLOSED'))
    rejected('LC starts parse invented after refusal',lambda q,r:q['result'].update(function_starts={'body_proof':True}))
    rejected('name pointer changed',lambda q,r:q['result']['types'][1]['typeinfo_candidates'][0].update(name_va=0))
    rejected('primary top changed',lambda q,r:q['result']['types'][1]['table_headers'][0].update(offset_to_top=1))
    rejected('address point changed',lambda q,r:q['result']['types'][1]['table_headers'][0].update(address_point=0))
    rejected('raw name boundary changed',lambda q,r:q['result']['selected_ranges'][0].update(hex='ff'+q['result']['selected_ranges'][0]['hex'][2:]))
    print(json.dumps(dict(status='PASS-retained-data-only',types=8,missing_exact_names=1,candidate_typeinfos=7,
        candidate_primary_headers=7,slot_prefixes=0,selected_ranges=21,negative_count=len(neg),negatives=neg,
        new_image_or_decoder_original_model_harness_reads_calls=0,required_unsupported='U',coverage_gate='OPEN'),indent=2))


if __name__=='__main__':
    main()
