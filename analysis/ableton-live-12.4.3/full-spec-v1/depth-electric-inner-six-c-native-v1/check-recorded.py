"""Only sealed owned source/native/receipts; no external image/tool/corpus opens or children."""
import copy
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
PRE='e20f416c9692b29139cd16461b92954daf998ce6947cde81d421c3f3d0b318ec'
EXPECTED=[(0xcb0c,800),(0xd2e0,656),(0xd688,700),(0xd9b8,16),(0xd9c8,540),(0xdbe4,108)]
LOADS={0xcb4c:(8,0,0),0xcb50:(8,8,0x70),0xcb8c:(8,20,0),0xcb90:(8,8,0x80),0xccc0:(8,20,0),0xccc4:(8,8,0x78),0xcce8:(8,23,0),0xccec:(8,8,0x10),0xcd0c:(0,20,8),0xcd10:(8,0,0),0xcd14:(8,8,0x58),0xcd28:(8,20,8),0xcd30:(8,20,0),0xcd34:(8,8,0x20),0xcd94:(8,20,0),0xcd98:(8,8,0x88),0xd3f4:(8,20,0),0xd3f8:(8,8,0x90),0xd47c:(0,20,8),0xd4d0:(0,20,8),0xd4ec:(8,0,0),0xd4f0:(3,8,0xc8),0xd4f8:(0,20,8),0xd50c:(8,0,0),0xd510:(3,8,0xd8),0xd534:(0,20,8),0xd54c:(8,0,0),0xd550:(4,8,0xd0),0xd6ac:(8,0,8),0xd6d4:(8,21,0),0xd6d8:(1,8,0x58),0xd790:(0,21,8),0xd79c:(8,0,0),0xd7a0:(8,8,0x60),0xd7ac:(0,21,8),0xd7b0:(8,0,0),0xd7b4:(8,8,0x18),0xd7bc:(0,21,8),0xd7c4:(8,0,0),0xd7c8:(8,8,8),0xd7d0:(8,21,0),0xd7d4:(8,8,0x70),0xd7f8:(8,21,0),0xd7fc:(8,8,0x78),0xd820:(8,22,0),0xd824:(8,8,0x10),0xd844:(0,21,8),0xd848:(8,0,0),0xd84c:(8,8,0x58),0xd928:(8,21,0),0xd92c:(8,8,0x38),0xd9b8:(0,0,8),0xd9bc:(8,0,0),0xd9c0:(1,8,0x78),0xda04:(28,29,0x10),0xdaa0:(8,22,8),0xdb2c:(0,22,8),0xdb34:(1,27,0),0xdb38:(8,0,0),0xdb3c:(8,8,0x20),0xdc10:(0,0,8),0xdc34:(8,0,0),0xdc38:(8,8,0)}
INDIRECT={0xcb54:('BLR',8),0xcb98:('BLR',8),0xcccc:('BLR',8),0xcd08:('BLR',8),0xcd24:('BLR',8),0xcd3c:('BLR',8),0xcda0:('BLR',8),0xd408:('BLR',8),0xd478:('BR',10),0xd530:('BR',3),0xd56c:('BR',4),0xd700:('BR',1),0xd7a8:('BLR',8),0xd7b8:('BLR',8),0xd7cc:('BLR',8),0xd7e0:('BLR',8),0xd804:('BLR',8),0xd840:('BLR',8),0xd85c:('BLR',8),0xd938:('BLR',8),0xd9c4:('BR',1),0xdb50:('BLR',8),0xdc3c:('BLR',8)}
def require(x,msg):
    if not x: raise ValueError(msg)

def sha(b): return hashlib.sha256(b).hexdigest()
def read(n): return json.loads((HERE/n).read_bytes())
def signed(n,b): return n-(1<<b) if n&(1<<(b-1)) else n

def branch(pc,w):
    if w & 0x7c000000 == 0x14000000:
        return {'pc':hex(pc),'kind':'BL' if w>>31 else 'B','target':hex(pc+signed(w&0x3ffffff,26)*4)}
    if w & 0xff000010 == 0x54000000:
        return {'pc':hex(pc),'kind':'B.cond','condition':w&15,'target':hex(pc+signed((w>>5)&0x7ffff,19)*4)}
    if w & 0x7e000000 == 0x34000000:
        return {'pc':hex(pc),'kind':'CBNZ' if w&(1<<24) else 'CBZ','register':w&31,'width':64 if w>>31 else 32,'target':hex(pc+signed((w>>5)&0x7ffff,19)*4)}
    if w & 0x7e000000 == 0x36000000:
        return {'pc':hex(pc),'kind':'TBNZ' if w&(1<<24) else 'TBZ','register':w&31,'bit':((w>>31)<<5)|((w>>19)&31),'target':hex(pc+signed((w>>5)&0x3fff,14)*4)}
    mask=w&0xfffffc1f
    if mask in (0xd61f0000,0xd63f0000,0xd65f0000):
        return {'pc':hex(pc),'kind':{0xd61f0000:'BR',0xd63f0000:'BLR',0xd65f0000:'RET'}[mask],'register':(w>>5)&31}
    return None

def load(w,expected):
    require(w&0xffc00000==0xf9400000,'unsigned64 LDR form')
    found=(w&31,(w>>5)&31,((w>>10)&0xfff)*8)
    require(found==expected,'exact LDR register/base/offset')
    return {'Rt':found[0],'Rn':found[1],'offset':hex(found[2])}

def mov(w,rd,rm):
    require(w&0xffe0ffe0==0xaa0003e0 and w&31==rd and (w>>16)&31==rm,'64bit MOV alias carrier')

def vector_mov(w,rd,rm):
    require(w&0xffe0fc00==0x4ea01c00 and w&31==rd and (w>>5)&31==rm and (w>>16)&31==rm,'raw vector MOV alias carrier')

def store(w,rt,rn,offset):
    require(w&0xffc00000==0xf9000000 and (w&31,(w>>5)&31,((w>>10)&4095)*8)==(rt,rn,offset),'raw STR X register/base/offset')

def wide_pair(a,b,value):
    require(a&0xff80001f==0x52800008 and b&0xff80001f==0x72800008,'MOVZ/MOVK W8 form')
    require((a>>21)&3==0 and (b>>21)&3==1,'W8 halfword selectors')
    require(((a>>5)&65535)|(((b>>5)&65535)<<16)==value,'W8 exact full immediate')

def claims(a):
    require(a['scope']=={'C_records':6,'C_bytes':14556,'C_lines':500,'warnings':9,'native_intervals':6,'native_bytes':2820,'native_rows':705,'new_table_header_LC_fixup_bytes':0},'whole six scope')
    require(a['required_status']=='U/OPEN' and a['new_cases_grades_releases_main_sites']==0 and a['successor_selected']is False,'no behavioral promotion')
    for key in ['incoming_I_equals_prior_A','current_I_vptr_literal300b0','current_child_continuity','cast_D_equals_stored_P','runtime_encoding_application','formal_ABI','public_parameter_index_binding','construction_class_success']:
        require(a['carrier_limits'][key]=='unknown/conditional','no unsupported carrier/ABI/public inference')
    require(len(a['claims'])==9 and a['prerequisites']['Root_v2_approval_before_C_and_native']is True,'bounded claims and selected chronology')

def check():
    rawpre=(HERE/'pre-call-manifest.json').read_bytes();require(sha(rawpre)==PRE,'fixed precall identity');p=json.loads(rawpre)
    expected=[p['image'],p['tool'],*p['pins'],{'path':str(HERE/'pre-call-manifest.json'),'bytes':len(rawpre),'sha256':PRE}]
    before=read('capture/before-identities.json');after=read('capture/after-identities.json')
    require(len(before)==19 and before==expected==after['files'] and after['unchanged']is True,'recorded19custodypairs')
    for pin in p['pins']:
        f=Path(pin['path'])
        if f.parent==HERE:
            b=f.read_bytes();require(len(b)==pin['bytes']and sha(b)==pin['sha256'],'owned source pin')
    status=read('capture/status.json');require(status['error']is None and status['watch_unchanged']is True,'capture status')
    require(status['attempts']==status['children_started']==6 and status['selected_bytes_read']==status['validated_bytes']==2820 and status['validated_words']==705,'whole native totals')
    require(status['selected_table_bytes_read']==0 and status['native_original_instruction_execution']==0 and not status['automatic_retry'],'no other content/original/retry')
    require(read('capture/table-words.json')['words']==[],'no table words')
    meta=read('selected-metadata.json')['records'];source=(HERE/'source-context.jsonl').read_bytes().splitlines(keepends=True)
    require(len(meta)==len(source)==6,'whole C set')
    Cbytes=Clines=warnings=0;allrows={};branches=[];pairs=[];literals=[];receipts=[];projection=[]
    extracted=read('capture/extraction.json')['ranges']
    for (start,n),record,line,window,ex in zip(EXPECTED,meta,source,p['ranges'],extracted):
        require(window=={'start':hex(start),'end_exclusive':hex(start+n),'file_offset':start,'bytes':n,'words':n//4},'exact whole selected native range')
        md=record['C1_metadata'];require(len(line)==md['raw_bytes']and sha(line)==md['raw_sha256'],'raw selected C1 pin')
        d=json.loads(line);code=d.pop('code');require(d==md['metadata'],'all source metadata preserved')
        require(d['body_ranges']==[[hex(start),hex(start+n-1)]] and d['body_bytes']==n,'source extent')
        require(d['signature']=='undefined FUN_'+format(start,'08x')+'()','unrecovered metadata signature preserved')
        require(d['error']is None and not d['timed_out']and not d['partial_code']and not d['thunk'],'source status/thunk')
        require(len(code.encode())==d['code_bytes']and sha(code.encode())==d['code_sha256']and len(code.splitlines())==record['measured_C_lines'],'whole C projection size/hash')
        Cbytes+=len(code.encode());Clines+=len(code.splitlines());warnings+=len(d['warnings'])
        projection.append(('\n/* WHOLE SELECTED '+format(start,'x')+'; original C follows unchanged */\n'+code).encode())
        name=format(start,'x');raw=(HERE/('capture/'+name+'.bin')).read_bytes();rows=read('capture/'+name+'.stdout.json')
        require(len(raw)==n and len(rows)==n//4 and ex=={**window,'sha256':sha(raw)},'whole raw/extraction extent')
        for i,row in enumerate(rows):
            pc=start+4*i;word=int.from_bytes(raw[4*i:4*i+4],'little');allrows[pc]=(row,word)
            require(type(row['offset'])is int and row['offset']==pc and type(row['size'])is int and row['size']==4,'row address/size')
            require(row['bytes']==raw[4*i:4*i+4].hex()and row['opcode']and row['type']not in ['invalid','ill'],'raw association')
            b=branch(pc,word)
            if b:
                if'target'in b:require(row.get('jump')==int(b['target'],16),'raw branch target')
                branches.append(b)
            if word&0x3e000000 in [0x28000000,0x2c000000]:
                vector=bool(word&(1<<26));opc=(word>>30)&3
                scale=(4<<opc)if vector else(8 if opc==2 else 4)
                pairs.append({'pc':hex(pc),'load':bool(word&(1<<22)),'vector':vector,'opc':opc,'mode':(word>>23)&3,'Rn':(word>>5)&31,'Rt':word&31,'Rt2':(word>>10)&31,'offset':signed((word>>15)&127,7)*scale})
            if word&0x9f000000==0x10000000:
                target=pc+signed((((word>>5)&0x7ffff)<<2)|((word>>29)&3),21)
                literals.append({'pc':hex(pc),'kind':'ADR','Rd':word&31,'target':hex(target)})
            if word&0xff000000==0x58000000:
                literals.append({'pc':hex(pc),'kind':'LDRliteralX','Rt':word&31,'target':hex(pc+signed((word>>5)&0x7ffff,19)*4)})
        rc=read('capture/'+name+'.invocation-after.json');pid=read('capture/'+name+'.pid.json')
        require(rc['pid']==pid['pid']and rc['exit_code']==0 and rc['error']is None and not rc['timed_out']and rc['timeout_seconds']==30,'decoder receipt status')
        require(rc['stdin']=='DEVNULL'and rc['new_process_session']and rc['core_limit_bytes']==0 and rc['cleanup']=='process-group-already-gone','child bounds/cleanup')
        require((HERE/('capture/'+name+'.stderr')).read_bytes()==b'','empty stderr')
        require(rc['argv']==[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(start),'-s',hex(start),'-q','-c','pdj '+str(n//4),str(HERE/('capture/'+name+'.bin'))],'exact bounded argv')
        receipts.append({'entry':hex(start),'pid':rc['pid'],'start':rc['started_utc'],'end':rc['finished_utc']})
    require(Cbytes==14556 and Clines==500 and warnings==9 and len(allrows)==705,'entire source/native totals')
    require(b''.join(projection)==(HERE/'whole-selected-C.txt').read_bytes(),'lossless complete C text projection')
    require(len({r['pid']for r in receipts})==6,'unique children')
    for a,b in zip(receipts,receipts[1:]):require(a['end']<=b['start'],'sequential child order')
    sr=read('source-read-receipt.json');require(sr['approval']['sha256']=='653ce9bdd71c91a817a3c6166677f8f7065ea51ccd706c865e11b667ed9b375c'and sr['approval_verified_before_C_read_utc']<=sr['finished_utc']<status['started_utc'],'source/native selection chronology')
    require(sr['chunk_before']==sr['chunk_after']and not sr['alias_census_replayed']and not sr['automatic_retry'],'exact source custody/no census')
    loads=[{'pc':hex(pc),**load(allrows[pc][1],value)}for pc,value in LOADS.items()]
    transfers={int(b['pc'],16):(b['kind'],b['register'])for b in branches if b['kind']in ['BR','BLR']}
    require(transfers==INDIRECT,'all23 indirect transfers')
    for pc,rd,rm in [(0xcb30,20,0),(0xd2fc,19,1),(0xd344,20,0),(0xd6b8,21,0),(0xd7e4,22,0),(0xd9e8,19,7),(0xd9ec,23,6),(0xd9f0,21,5),(0xd9f4,20,4),(0xd9f8,24,3),(0xd9fc,25,1),(0xda00,22,0)]:mov(allrows[pc][1],rd,rm)
    vector_mov(allrows[0xd6b4][1],8,0);vector_mov(allrows[0xd7dc][1],0,8);vector_mov(allrows[0xd404][1],0,8)
    store(allrows[0xcb58][1],0,20,8);store(allrows[0xd7e8][1],0,21,8);store(allrows[0xda90][1],8,27,0x30)
    for lo,hi,value in [(0xcb34,0xcb38,0xe0028),(0xcb40,0xcb44,0xe007c),(0xccd0,0xccd4,0xe0030),(0xd300,0xd304,0xe0060),(0xd6bc,0xd6c0,0xe0028),(0xd808,0xd80c,0xe0030),(0xda08,0xda0c,0xe0028),(0xda94,0xda98,0xe0030),(0xdbfc,0xdc00,0xe0078)]:wide_pair(allrows[lo][1],allrows[hi][1],value)
    require(allrows[0xcb48][1]==0xbc286800,'incoming S0 register-offset store')
    require(allrows[0xccf4][1]==allrows[0xd82c][1]==0x290027e0,'packed W0/W9 stack words')
    require(branch(0xd40c,allrows[0xd40c][1])=={'pc':'0xd40c','kind':'TBNZ','register':0,'bit':0,'target':'0xd43c'},'hook low-bit branch')
    require(allrows[0xdb74][1]==0x52800020 and branch(0xdc4c,allrows[0xdc4c][1])['target']=='0xedf4','literal return1 and fallback tail target')
    a=read('assessment.json');claims(a)
    rejected=[]
    def reject(name,fn):
        try:fn()
        except(ValueError,KeyError,TypeError):rejected.append(name);return
        raise ValueError('accepted negative '+name)
    reject('wrong current child offset',lambda:load(allrows[0xd9b8][1]^(1<<10),(0,0,8)))
    reject('wrong child slot',lambda:load(allrows[0xd9c0][1]^(1<<10),(1,8,0x78)))
    reject('wrong incoming receiver',lambda:mov(allrows[0xcb30][1]^(1<<16),20,0))
    reject('wrong FP carrier',lambda:vector_mov(allrows[0xd6b4][1]^(1<<16),8,0))
    reject('wrong replacement member',lambda:store(allrows[0xd7e8][1]^(1<<10),0,21,8))
    reject('tail promoted call',lambda:require(branch(0xd9c4,allrows[0xd9c4][1])['kind']=='BLR','BR retains caller link'))
    for key in a['carrier_limits']:
        bad=copy.deepcopy(a);bad['carrier_limits'][key]='proved';reject('promoted '+key,lambda bad=bad:claims(bad))
    for name,key,value in [('public completion','required_status','complete'),('new site grade','new_cases_grades_releases_main_sites',23),('automatic successor','successor_selected',True)]:
        bad=copy.deepcopy(a);bad[key]=value;reject(name,lambda bad=bad:claims(bad))
    if(HERE/'manifest.json').exists():
        manifest=read('manifest.json');actual={str(f.relative_to(HERE))for f in HERE.rglob('*')if f.is_file()and f.name!='manifest.json'}
        require(actual=={x['path']for x in manifest['files']},'exact frozen tree')
        for x in manifest['files']:
            b=(HERE/x['path']).read_bytes();require(len(b)==x['bytes']and sha(b)==x['sha256'],'frozen payload pin')
    return {'status':'PASS-packet-only','C_records':6,'C_bytes':Cbytes,'C_lines':Clines,'warning_occurrences':warnings,'native_bytes':2820,'native_rows':705,'new_table_header_LC_fixup_bytes':0,'recorded_custody_pairs':19,'receipts':receipts,'critical_u64_loads':loads,'branch_fields':branches,'all_general_and_FP_pairs':pairs,'literal_address_nominations_only':literals,'negative_controls':rejected,'external_paths_reopened':0,'decoder_or_original_calls':0,'ESIL_used_for_semantics':False}

if __name__=='__main__':
    require(sys.argv[1:]==['--check'],'only packet check mode')
    print(json.dumps(check(),indent=2))
