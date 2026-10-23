"""Current owned source/native/receipt data only, no external opens or child execution."""
import copy
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
PRE='97ce9a70368d817fe13e6b17a7004ea3a7a9a6cc428961bc6e9f392811966222'
EXPECTED=[(0x145c4,656),(0x14a6c,700),(0x14d9c,16),(0x14dac,540),(0x14fc8,108)]
LOADS={83672: (8, 20, 0), 83676: (8, 8, 144), 83808: (0, 20, 8), 83892: (0, 20, 8), 83920: (8, 0, 0), 83924: (3, 8, 200), 83932: (0, 20, 8), 83952: (8, 0, 0), 83956: (3, 8, 216), 83992: (0, 20, 8), 84016: (8, 0, 0), 84020: (4, 8, 208), 84624: (8, 0, 8), 84664: (8, 21, 0), 84668: (1, 8, 88), 84852: (0, 21, 8), 84864: (8, 0, 0), 84868: (8, 8, 96), 84880: (0, 21, 8), 84884: (8, 0, 0), 84888: (8, 8, 24), 84896: (0, 21, 8), 84904: (8, 0, 0), 84908: (8, 8, 8), 84916: (8, 21, 0), 84920: (8, 8, 112), 84956: (8, 21, 0), 84960: (8, 8, 120), 84996: (8, 22, 0), 85000: (8, 8, 16), 85032: (0, 21, 8), 85036: (8, 0, 0), 85040: (8, 8, 88), 85260: (8, 21, 0), 85264: (8, 8, 56), 85404: (0, 0, 8), 85408: (8, 0, 0), 85412: (1, 8, 120), 85480: (28, 29, 16), 85636: (8, 22, 8), 85776: (0, 22, 8), 85784: (1, 27, 0), 85788: (8, 0, 0), 85792: (8, 8, 32), 86004: (0, 0, 8), 86040: (8, 0, 0), 86044: (8, 8, 0)}
INDIRECT={83692: ('BLR', 8), 83804: ('BR', 10), 83988: ('BR', 3), 84048: ('BR', 4), 84708: ('BR', 1), 84876: ('BLR', 8), 84892: ('BLR', 8), 84912: ('BLR', 8), 84932: ('BLR', 8), 84968: ('BLR', 8), 85028: ('BLR', 8), 85056: ('BLR', 8), 85276: ('BLR', 8), 85416: ('BR', 1), 85812: ('BLR', 8), 86048: ('BLR', 8)}
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
    require(a['scope']=={'C_records':5,'C_bytes':10767,'C_lines':365,'warnings':8,'native_intervals':5,'native_bytes':2020,'native_rows':505,'new_table_header_LC_fixup_bytes':0},'whole five scope')
    require(a['required_status']=='U/OPEN'and a['new_cases_grades_releases_main_sites']==0 and a['successor_selected']is False,'no behavioral promotion')
    require(len(a['claims'])==8,'eight bounded claims')
    for key in ['incoming_I_equals_prior_P','current_I_vptr_literal5c0c0','current_child_continuity','saved_N_equals_current_child_after_calls','cast_D_equals_child','runtime_encoding_application','formal_ABI','public_parameter_index63_binding','Damper_internal_law','construction_class_success']:
        require(a['carrier_limits'][key]=='unknown/conditional','preserve runtime/current/ABI/named gaps')


def check():
    rawpre=(HERE/'pre-call-manifest.json').read_bytes();require(sha(rawpre)==PRE,'fixed precall identity');p=json.loads(rawpre)
    require(p['sole_independent_reviewer']=='arrangement_map_review','selected solepeer before capture')
    expected=[p['image'],p['tool'],*p['pins'],{'path':str(HERE/'pre-call-manifest.json'),'bytes':len(rawpre),'sha256':PRE}]
    before=read('capture/before-identities.json');after=read('capture/after-identities.json')
    require(len(before)==15 and before==expected==after['files']and after['unchanged']is True,'15recorded custody pairs')
    for pin in p['pins']:
        path=Path(pin['path'])
        if path.parent==HERE:
            data=path.read_bytes();require(len(data)==pin['bytes']and sha(data)==pin['sha256'],'owned frozen input')
    status=read('capture/status.json');require(status['error']is None and status['watch_unchanged']is True,'capture status')
    require(status['attempts']==status['children_started']==5 and status['selected_bytes_read']==status['validated_bytes']==2020 and status['validated_words']==505,'whole native totals')
    require(status['selected_table_bytes_read']==0 and status['native_original_instruction_execution']==0 and status['automatic_retry']is False,'no other content/execution/retry')
    require(read('capture/table-words.json')['words']==[],'zero data words')
    metadata=read('selected-metadata.json')['records'];source=(HERE/'source-context.jsonl').read_bytes().splitlines(keepends=True)
    require(len(metadata)==len(source)==5,'all five whole records')
    extracted=read('capture/extraction.json')['ranges'];allrows={};branches=[];pairs=[];literals=[];receipts=[];projection=[];Cbytes=Clines=warnings=0
    for (start,size),record,line,window,ex in zip(EXPECTED,metadata,source,p['ranges'],extracted):
        require(window=={'start':hex(start),'end_exclusive':hex(start+size),'file_offset':start,'bytes':size,'words':size//4},'whole explicit native interval')
        md=record['C1_metadata'];require(len(line)==md['raw_bytes']and sha(line)==md['raw_sha256'],'raw C1 exact pin')
        decoded=json.loads(line);code=decoded.pop('code');require(decoded==md['metadata'],'all original source metadata preserved')
        require(decoded['body_ranges']==[[hex(start),hex(start+size-1)]]and decoded['body_bytes']==size,'whole source/native extent')
        require(decoded['signature']=='undefined FUN_'+format(start,'08x')+'()'and decoded['error']is None and not decoded['timed_out']and not decoded['partial_code']and not decoded['thunk'],'unrecovered signature/status')
        require(len(code.encode())==decoded['code_bytes']and sha(code.encode())==decoded['code_sha256']and len(code.splitlines())==record['measured_C_lines'],'whole C identity/linecount')
        Cbytes+=len(code.encode());Clines+=len(code.splitlines());warnings+=len(decoded['warnings'])
        projection.append(('\n/* WHOLE SELECTED '+format(start,'x')+'; original C follows unchanged */\n'+code).encode())
        name=format(start,'x');raw=(HERE/('capture/'+name+'.bin')).read_bytes();rows=read('capture/'+name+'.stdout.json')
        require(len(raw)==size and len(rows)==size//4 and ex=={**window,'sha256':sha(raw)},'whole raw range projection')
        for i,row in enumerate(rows):
            pc=start+4*i;word=int.from_bytes(raw[4*i:4*i+4],'little');allrows[pc]=(row,word)
            require(type(row['offset'])is int and row['offset']==pc and type(row['size'])is int and row['size']==4,'whole row address/length')
            require(row['bytes']==raw[4*i:4*i+4].hex()and row['opcode']and row['type']not in ['invalid','ill'],'all raw/row associations')
            b=branch(pc,word)
            if b:
                if 'target'in b:require(row.get('jump')==int(b['target'],16),'independent raw branch target')
                branches.append(b)
            if word&0x3e000000 in [0x28000000,0x2c000000]:
                vector=bool(word&(1<<26));opc=(word>>30)&3;scale=(4<<opc)if vector else(8 if opc==2 else 4)
                pairs.append({'pc':hex(pc),'load':bool(word&(1<<22)),'vector':vector,'opc':opc,'mode':(word>>23)&3,'Rn':(word>>5)&31,'Rt':word&31,'Rt2':(word>>10)&31,'offset':signed((word>>15)&127,7)*scale})
            if word&0x9f000000==0x10000000:
                target=pc+signed((((word>>5)&0x7ffff)<<2)|((word>>29)&3),21)
                literals.append({'pc':hex(pc),'kind':'ADR','Rd':word&31,'target':hex(target)})
            if word&0xff000000==0x58000000:literals.append({'pc':hex(pc),'kind':'LDRliteralX','Rt':word&31,'target':hex(pc+signed((word>>5)&0x7ffff,19)*4)})
        rc=read('capture/'+name+'.invocation-after.json');pid=read('capture/'+name+'.pid.json');initial=read('capture/'+name+'.invocation-before.json')
        require(rc['pid']==pid['pid']and rc['exit_code']==0 and rc['error']is None and not rc['timed_out']and rc['timeout_seconds']==30,'decoder receipt success')
        require(rc['stdin']=='DEVNULL'and rc['new_process_session']and rc['core_limit_bytes']==0 and rc['cleanup']=='process-group-already-gone','process bounds/cleanup')
        require(rc['environment']=={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'},'fixed environment')
        require((HERE/('capture/'+name+'.stderr')).read_bytes()==b'','empty retained stderr')
        require(rc['argv']==[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(start),'-s',hex(start),'-q','-c','pdj '+str(size//4),str(HERE/('capture/'+name+'.bin'))],'exact fixed decoder argv')
        require(initial['pid']is None and initial['exit_code']is None and initial['argv']==rc['argv']==pid['argv']and initial['started_utc']==rc['started_utc'],'one initial receipt per child')
        receipts.append({'entry':hex(start),'pid':rc['pid'],'start':rc['started_utc'],'end':rc['finished_utc']})
    require(Cbytes==10767 and Clines==365 and warnings==8 and len(allrows)==505,'entire source/native totals')
    require(b''.join(projection)==(HERE/'whole-selected-C.txt').read_bytes(),'lossless all C projection')
    require(len({r['pid']for r in receipts})==5,'unique child processes')
    for a,b in zip(receipts,receipts[1:]):require(a['end']<=b['start'],'sequential order')
    sr=read('source-read-receipt.json')
    require(sr['approval']['sha256']=='982ec730731c3ffffb2063eaa876a7e432b043a5343554ca7573491ff468710e'and sr['approval_verified_before_C_read_utc']<=sr['finished_utc']<status['started_utc'],'source approval/capture chronology')
    require(sr['chunk_before']==sr['chunk_after']and not sr['alias_census_replayed']and not sr['automatic_retry'],'source custody/no replay')
    loads=[{'pc':hex(pc),**load(allrows[pc][1],value)}for pc,value in LOADS.items()]
    transfers={int(b['pc'],16):(b['kind'],b['register'])for b in branches if b['kind']in ['BR','BLR']};require(transfers==INDIRECT,'all16indirect carriers')
    for pc,rd,rm in [(0x145e0,19,1),(0x14628,20,0),(0x14a9c,21,0),(0x14bc8,22,0),(0x14dcc,19,7),(0x14dd0,23,6),(0x14dd4,21,5),(0x14dd8,20,4),(0x14ddc,24,3),(0x14de0,25,1),(0x14de4,22,0)]:mov(allrows[pc][1],rd,rm)
    for pc,rd,rm in [(0x14a98,8,0),(0x14bc0,0,8),(0x146e8,0,8)]:vector_mov(allrows[pc][1],rd,rm)
    store(allrows[0x14bcc][1],0,21,8);store(allrows[0x14e74][1],8,27,0x30)
    for lo,hi,value in [(0x145e4,0x145e8,0xe0060),(0x14aa0,0x14aa4,0xe0028),(0x14bec,0x14bf0,0xe0030),(0x14dec,0x14df0,0xe0028),(0x14e78,0x14e7c,0xe0030),(0x14fe0,0x14fe4,0xe0078)]:wide_pair(allrows[lo][1],allrows[hi][1],value)
    require(allrows[0x14c10][1]==0x290027e0,'packed W0/W9 payload, not formal stack arglist')
    require(branch(0x146f0,allrows[0x146f0][1])=={'pc':'0x146f0','kind':'TBNZ','register':0,'bit':0,'target':'0x14720'},'hook low-bit branch')
    require(allrows[0x14f58][1]==0x52800020 and branch(0x15030,allrows[0x15030][1])['target']=='0x161d8','literal normal return1/fallback tail')
    require(allrows[0x1473c][1]==0xb94002e8 and allrows[0x14740][1]==0x71000d1f and branch(0x14744,allrows[0x14744][1])=={'pc':'0x14744','kind':'B.cond','condition':8,'target':'0x14720'},'computed table unsigned guard')
    require(allrows[0x14754][1]==0x3868692b and allrows[0x14758][1]==0x8b0b094a,'byte-indexed native dispatch expression; no table bytes')
    require(allrows[0x14e88][1]==0xbd401500 and allrows[0x14e8c][1]==0x5e21d800,'raw child+14 low32load/SCVTF carrier, no numerical law')
    a=read('assessment.json');claims(a);rejected=[]
    def reject(name,fn):
        try:fn()
        except(ValueError,KeyError,TypeError):rejected.append(name);return
        raise ValueError('accepted negative '+name)
    reject('wrong current child offset',lambda:load(allrows[0x14d9c][1]^(1<<10),(0,0,8)))
    reject('wrong child slot',lambda:load(allrows[0x14da4][1]^(1<<10),(1,8,0x78)))
    reject('wrong incoming receiver',lambda:mov(allrows[0x14a9c][1]^(1<<16),21,0))
    reject('wrong FP carrier',lambda:vector_mov(allrows[0x14a98][1]^(1<<16),8,0))
    reject('wrong replacement field',lambda:store(allrows[0x14bcc][1]^(1<<10),0,21,8))
    reject('tail promoted call',lambda:require(branch(0x14da8,allrows[0x14da8][1])['kind']=='BLR','tail BR, not BLR'))
    for key in a['carrier_limits']:
        bad=copy.deepcopy(a);bad['carrier_limits'][key]='proved';reject('promoted '+key,lambda bad=bad:claims(bad))
    for name,key,value in [('required closure','required_status','complete'),('new site grade','new_cases_grades_releases_main_sites',16),('automatic successor','successor_selected',True)]:
        bad=copy.deepcopy(a);bad[key]=value;reject(name,lambda bad=bad:claims(bad))
    if(HERE/'manifest.json').exists():
        manifest=read('manifest.json');actual={str(f.relative_to(HERE))for f in HERE.rglob('*')if f.is_file()and f.name!='manifest.json'}
        require(actual=={x['path']for x in manifest['files']},'exact final tree')
        for x in manifest['files']:
            data=(HERE/x['path']).read_bytes();require(len(data)==x['bytes']and sha(data)==x['sha256'],'frozen payload pin')
    return {'status':'PASS-owned-data-only','C_records':5,'C_bytes':Cbytes,'C_lines':Clines,'warning_occurrences':warnings,'native_bytes':2020,'native_rows':505,'recorded_custody_pairs':15,'receipts':receipts,'critical_u64_loads':loads,'branch_fields':branches,'all_general_and_FP_pairs':pairs,'literal_address_nominations_only':literals,'negative_controls':rejected,'external_paths_opened':0,'decoder_original_calls':0,'ESIL_used_for_semantics':False}

if __name__=='__main__':
    require(sys.argv[1:]==['--check'],'only owned packet check')
    print(json.dumps(check(),indent=2))
