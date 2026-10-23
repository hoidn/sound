"""Read only this packet. No external pins reopened, child or source helper imported."""
import copy
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
PRE='c01827179ad477bd8daeddbcb2a90b1a5ccd110c2c7249fe3bbd0b3e181bd136'
EXPECTED=[(0xe5b4,76),(0xe600,128),(0xe680,128),(0xe700,1480),(0xecc8,24),(0xed2c,24)]
LOADS={0xe5b8:(0,0,8),0xe5c8:(8,8,0x4060),0xe5dc:(8,0,0),0xe5e0:(4,8,0x68),0xe5f0:(8,0,0),0xe5f4:(4,8,0x68),0xe64c:(0,0,8),0xe654:(8,0,0),0xe658:(1,8,0x50),0xe674:(0,0,8),0xe6cc:(0,0,8),0xe6d4:(8,0,0),0xe6d8:(1,8,0x58),0xe6f4:(0,0,8),0xeafc:(0,21,8),0xeb04:(5,21,0x18),0xeb08:(8,0,0),0xeb0c:(8,8,0x60),0xeb10:(20,31,0x10),0xeb20:(1,31,0x30),0xecc8:(0,0,8),0xecd0:(8,0,0),0xecd4:(1,8,0x10),0xed2c:(0,0,8),0xed34:(8,0,0),0xed38:(2,8,0x38)}
INDIRECT={0xe5e4:('BR',4),0xe5fc:('BR',4),0xe65c:('BR',1),0xe6dc:('BR',1),0xeb30:('BLR',8),0xecd8:('BR',1),0xed3c:('BR',2)}

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

def claims(a):
    require(a['scope']=={'whole_C_records':6,'C_lines':414,'C_bytes':12149,'native_intervals':6,'native_rows':465,'native_bytes':1860,'new_table_bytes':0,'prior_actual_raw_replayed':0},'scope')
    require(a['prerequisite']['verified_before_any_C_or_native_acquisition'] is True,'approval chronology')
    c=a['carrier_status']
    for k in ['A_equals_O','R_equals_A_O','child_equals_A','D_equals_child','D_addresspoint','current_O_vptr_continuity','runtime_encoding_or_relocation_PAC']:
        require(c[k]=='unknown','no carrier/pointer promotion')
    require(c['current_O_plus8_equals_A']=='conditional-premise-only','no currentmember continuity assumed')
    require(a['counts']['new_resolved_runtime_sites']==0 and a['counts']['main_Live_inventory']=='25095 of268015 unchanged','no site credit')
    require(a['required_status']=='U/OPEN unchanged' and a['successor_selected'] is False,'no public closure or successor')
    require(len(a['claims'])==8 and len(a['claims'][2]['premises'])>=6,'bounded claims/premises')

def check():
    rawpre=(HERE/'pre-call-manifest.json').read_bytes(); require(sha(rawpre)==PRE,'precall identity'); p=json.loads(rawpre)
    expected=[p['image'],p['tool'],*p['pins'],{'path':str(HERE/'pre-call-manifest.json'),'bytes':len(rawpre),'sha256':PRE}]
    before=read('capture/before-identities.json'); after=read('capture/after-identities.json')
    require(len(before)==18 and before==expected==after['files'] and after['unchanged'] is True,'recorded18custodypairs')
    for pin in p['pins']:
        q=Path(pin['path'])
        if q.parent==HERE:
            b=q.read_bytes(); require(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'owned precall source pin')
    status=read('capture/status.json'); require(status['error'] is None and status['watch_unchanged'] is True,'success')
    require(status['attempts']==status['children_started']==6 and status['validated_words']==465 and status['validated_bytes']==1860,'six complete decodes')
    require(status['selected_table_bytes_read']==0 and status['native_original_instruction_execution']==0,'no tables/native execution')
    require(read('capture/table-words.json')['words']==[],'no selected datawords')
    meta=read('selected-metadata.json')['records']; source=(HERE/'source-context.jsonl').read_bytes().splitlines(keepends=True)
    require(len(source)==len(meta)==6,'complete source set'); Cbytes=Clines=warnings=0
    allrows={}; branches=[]; pairs=[]; receipts=[]
    extracted=read('capture/extraction.json')['ranges']
    for i,((start,n),record,line,r) in enumerate(zip(EXPECTED,meta,source,p['ranges'])):
        require(r=={'start':hex(start),'end_exclusive':hex(start+n),'file_offset':start,'bytes':n,'words':n//4},'exact explicit range')
        m=record['C1_metadata']; require(len(line)==m['raw_bytes'] and sha(line)==m['raw_sha256'],'exact retained C1 line')
        d=json.loads(line); c=d.pop('code'); require(d==m['metadata'],'full metadata preservation')
        require(d['body_ranges']==[[hex(start),hex(start+n-1)]] and d['body_bytes']==n,'explicit C1 range')
        require(d['error'] is None and not d['timed_out'] and not d['partial_code'] and not d['thunk'],'source statuses')
        require(len(c.encode())==d['code_bytes'] and sha(c.encode())==d['code_sha256'],'complete C code hash')
        Cbytes+=len(c.encode()); Clines+=len(c.splitlines()); warnings+=len(d['warnings'])
        raw=(HERE/('capture/'+hex(start)[2:]+'.bin')).read_bytes(); rows=read('capture/'+hex(start)[2:]+'.stdout.json')
        require(len(raw)==n and len(rows)==n//4,'whole raw/row extent')
        require(extracted[i]=={**r,'sha256':sha(raw)},'extraction bytes')
        for j,row in enumerate(rows):
            pc=start+4*j; require(type(row['offset']) is int and row['offset']==pc and type(row['size']) is int and row['size']==4,'row geometry')
            require(row['bytes']==raw[j*4:j*4+4].hex() and row['opcode'] and row['type'] not in ('invalid','ill'),'raw association')
            w=int.from_bytes(raw[j*4:j*4+4],'little'); allrows[pc]=(row,w)
            b=branch(pc,w)
            if b:
                if 'target' in b: require(row.get('jump')==int(b['target'],16),'raw branch destination')
                branches.append(b)
            if w&0x3e000000==0x28000000 and (w>>30)&3==2 and (w>>26)&1==0:
                pairs.append({'pc':hex(pc),'load':bool(w&(1<<22)),'mode':(w>>23)&3,'Rn':(w>>5)&31,'Rt':w&31,'Rt2':(w>>10)&31,'offset':signed((w>>15)&127,7)*8})
        name=hex(start)[2:]; rc=read('capture/'+name+'.invocation-after.json'); pid=read('capture/'+name+'.pid.json')
        require(rc['pid']==pid['pid'] and rc['exit_code']==0 and rc['error'] is None and rc['timed_out'] is False and rc['timeout_seconds']==30,'child status')
        require(rc['stdin']=='DEVNULL' and rc['core_limit_bytes']==0 and rc['new_process_session'] and rc['cleanup']=='process-group-already-gone','child limits/cleanup')
        require((HERE/('capture/'+name+'.stderr')).read_bytes()==b'','empty stderr')
        require(rc['argv']==[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(start),'-s',hex(start),'-q','-c','pdj '+str(n//4),str(HERE/('capture/'+name+'.bin'))],'exact bounded argv')
        receipts.append({'entry':hex(start),'pid':rc['pid'],'start':rc['started_utc'],'end':rc['finished_utc']})
    require(Cbytes==12149 and Clines==414 and warnings==15 and len(allrows)==465,'whole set totals')
    require(len({x['pid'] for x in receipts})==6,'six unique child PIDs')
    for a,b in zip(receipts,receipts[1:]): require(a['end']<=b['start'],'sequential children')
    require(p['prerequisite_approval']['sha256']=='66b782de127d886531527e2b1b57358a3b337decf1cdd1fc8e40959c9b78cbbb','prior approval')
    source_receipt=read('source-read-receipt.json'); require(source_receipt['approval_identity_verified_before_C_read_utc']<=source_receipt['selected_C_record_acquisition_finished_utc']<status['started_utc'],'C afterapproval beforecapture')
    loads=[]
    for pc,expectedload in LOADS.items(): loads.append({'pc':hex(pc),**load(allrows[pc][1],expectedload)})
    mov(allrows[0xe73c][1],21,0); mov(allrows[0xeb28][1],6,22); mov(allrows[0xeb2c][1],7,23)
    indirect=[b for b in branches if b['kind'] in ('BR','BLR')]
    require({int(b['pc'],16):(b['kind'],b['register']) for b in indirect}==INDIRECT,'seven operand transfers')
    require(next(x for x in pairs if x['pc']=='0xecbc')=={'pc':'0xecbc','load':True,'mode':1,'Rn':31,'Rt':28,'Rt2':27,'offset':96},'final post-index register restoration')
    a=read('assessment.json'); claims(a)
    require(read('read-map.json')['native_rows']==465 and read('read-map.json')['C_lines']==414,'readmap scope')
    rejected=[]
    def reject(name,fn):
        try: fn()
        except (ValueError,KeyError,TypeError): rejected.append(name); return
        raise ValueError('accepted negative:'+name)
    reject('child pointer wrong member offset',lambda:load(allrows[0xe5b8][1]^(1<<10),(0,0,8)))
    reject('wrong slot register',lambda:load(allrows[0xeb0c][1]^1,(8,8,0x60)))
    reject('32bit load substituted',lambda:load(allrows[0xe5b8][1]^(1<<30),(0,0,8)))
    reject('entry receiver saved from wrong register',lambda:mov(allrows[0xe73c][1]^(1<<16),21,0))
    reject('BR treated as BLR',lambda:require(branch(0xecd8,allrows[0xecd8][1])['kind']=='BLR','tail preserves link'))
    require(branch(0xeb30,allrows[0xeb30][1])['kind']=='BLR','processing call writes link')
    for name,key,value in [('R equated A','R_equals_A_O','A'),('D assigned vptr','D_addresspoint','300b0'),('registration child equated A','child_equals_A','proved'),('cast D equated child','D_equals_child','proved'),('A equated O','A_equals_O','proved'),('stable currentOtable','current_O_vptr_continuity','proved'),('runtime encoding guessed','runtime_encoding_or_relocation_PAC','proved')]:
        bad=copy.deepcopy(a); bad['carrier_status'][key]=value; reject(name,lambda bad=bad:claims(bad))
    for name,key,value in [('site credit','new_resolved_runtime_sites',7),('main image count changed','main_Live_inventory','25102 of268015')]:
        bad=copy.deepcopy(a); bad['counts'][key]=value; reject(name,lambda bad=bad:claims(bad))
    bad=copy.deepcopy(a); bad['required_status']='complete'; reject('public completion',lambda:claims(bad))
    bad=copy.deepcopy(a); bad['successor_selected']=True; reject('automatic callee follow',lambda:claims(bad))
    if (HERE/'manifest.json').exists():
        m=read('manifest.json'); actual={str(f.relative_to(HERE)) for f in HERE.rglob('*') if f.is_file() and f.name!='manifest.json'}
        require(actual=={f['path'] for f in m['files']},'exact sealed tree')
        for f in m['files']:
            b=(HERE/f['path']).read_bytes(); require(len(b)==f['bytes'] and sha(b)==f['sha256'],'sealed payload hash')
    return {'status':'PASS-packet-only','C_records':6,'C_bytes':Cbytes,'C_lines':Clines,'warning_occurrences':warnings,'native_bytes':1860,'native_rows':465,'new_table_bytes':0,'custody_pairs':18,'receipts':receipts,'raw_unsigned64_loads':loads,'raw_branch_forms':branches,'raw_general_register_pairs':pairs,'negative_controls':rejected,'external_paths_reopened':0,'decoder_or_original_calls':0}

if __name__=='__main__':
    require(sys.argv[1:]==['--check'],'only --check')
    print(json.dumps(check(),indent=2))
