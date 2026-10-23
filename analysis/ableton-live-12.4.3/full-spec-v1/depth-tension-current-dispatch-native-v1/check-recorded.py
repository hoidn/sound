"""Fixed retained-packet data check only; no external pin opens, imports or children."""
import copy
import hashlib
import json
from pathlib import Path
import sys
P=Path(__file__).resolve().parent
PRE='14a8e9d85ca6bf18296ab08647db1a82a6531b3710c4ef94f776d4cfc1d3f94c'
RANGES=[(0x16110,24),(0x15ae4,1480),(0x15998,76)]
DATA=[(0x5d610,0x159e4),(0x5d618,0x15a64)]
LOADS={0x16110:(0,0,8),0x16118:(8,0,0),0x1611c:(2,8,0x38),0x15ee0:(0,21,8),0x15ee8:(5,21,0x18),0x15eec:(8,0,0),0x15ef0:(8,8,0x60),0x15ef4:(20,31,0x10),0x15f04:(1,31,0x30),0x1599c:(0,0,8),0x159ac:(8,8,0x4060),0x159c0:(8,0,0),0x159c4:(4,8,0x68),0x159d4:(8,0,0),0x159d8:(4,8,0x68)}
INDIRECT={0x16120:('BR',2),0x15f14:('BLR',8),0x159c8:('BR',4),0x159e0:('BR',4)}

def need(x,m):
    if not x:raise ValueError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def J(n):return json.loads((P/n).read_bytes())
def sx(n,b):return n-(1<<b) if n&(1<<(b-1)) else n

def flow(pc,w):
    if w&0x7c000000==0x14000000:return {'pc':hex(pc),'kind':'BL' if w>>31 else 'B','target':hex(pc+sx(w&0x3ffffff,26)*4)}
    if w&0xff000010==0x54000000:return {'pc':hex(pc),'kind':'B.cond','condition':w&15,'target':hex(pc+sx(w>>5&0x7ffff,19)*4)}
    if w&0x7e000000==0x34000000:return {'pc':hex(pc),'kind':'CBNZ' if w>>24&1 else 'CBZ','Rt':w&31,'target':hex(pc+sx(w>>5&0x7ffff,19)*4)}
    if w&0x7e000000==0x36000000:return {'pc':hex(pc),'kind':'TBNZ' if w>>24&1 else 'TBZ','Rt':w&31,'bit':(w>>31<<5)|(w>>19&31),'target':hex(pc+sx(w>>5&0x3fff,14)*4)}
    t=w&0xfffffc1f
    if t in [0xd61f0000,0xd63f0000,0xd65f0000]:return {'pc':hex(pc),'kind':{0xd61f0000:'BR',0xd63f0000:'BLR',0xd65f0000:'RET'}[t],'Rn':w>>5&31}
    return None

def ldr(w,t):need(w&0xffc00000==0xf9400000 and (w&31,w>>5&31,(w>>10&4095)*8)==t,'rawLDR64')
def fields(words):
    for pc,t in LOADS.items():ldr(words[pc],t)
    need(words[0x15b20]==0xaa0003f5,'entryX0savedX21')
    need([words[0x16110+4*i] for i in range(6)]==[0xf9400400,0xb4000080,0xf9400008,0xf9401d02,0xd61f0040,0xd65f03c0],'complete6wordtail/unchangedX1S0')
    need(words[0x159a0]==0x7100503f and words[0x159dc]==0x52800281,'query14separate')
    need(words[0x15f0c]==0xaa1603e6 and words[0x15f10]==0xaa1703e7,'processingGPRarguments')
    need(words[0x160a0]==0xa8c66ffc and words[0x160a4]==0xd65f03c0,'postindexedepilogue')

def plan_scope(p):
    need(p['ranges']==[{'start':hex(a),'end_exclusive':hex(a+n),'file_offset':a,'bytes':n,'words':n//4} for a,n in RANGES],'fixed3ranges')
    need(p['data_words']==[{'start':hex(a),'file_offset':a,'bytes':8} for a,v in DATA],'fixed2words/noPword')

def claims(a):
    need(a['scope']=={'whole_C_records':3,'C_bytes':9543,'C_lines':318,'raw_C1_bytes':11527,'native_bodies':3,'native_bytes':1580,'native_rows':395,'literal_words':2,'literal_bytes':16,'total_new_native_data_bytes':1596,'old_actual_raw_replayed':0},'fixedscope')
    c=a['carrier_status']
    for k in ['P_equals_or_distinct_from_O','Q_D_I_binding','current_O_table_at_public_dispatch','current_P_table_continuity','runtime_pointer_encoding_targets_class_ABI_public','index63_internal_Damper']:need(c[k]=='unknown','unknownjoins')
    need(c['current_O_plus8_equals_P']=='conditional-premise-only','currentmemberpremise')
    need(a['claims'][5]['runtime_targets_proved'] is False,'rawwordnotruntime')
    need(a['inner_operand_frontier']['P_table_word_content_acquired'] is False,'noPwords')
    need(a['counts']['new_resolved_runtime_sites']==0 and a['counts']['main_Live_inventory']=='25095 of268015 unchanged','no runtimecredit')
    need(a['no_successor_selected'] and a['required_status']=='U/OPEN unchanged' and len(a['claims'])==8 and len(a['claims'][4]['premises'])>=6,'qualifiedclaims')

def check():
    pb=(P/'pre-call-manifest.json').read_bytes();need(H(pb)==PRE,'precall');p=json.loads(pb);plan_scope(p);bf=J('capture/before-identities.json');af=J('capture/after-identities.json');expected=[p['image'],p['tool'],*p['pins'],{'path':str(P/'pre-call-manifest.json'),'bytes':len(pb),'sha256':PRE}];need(len(bf)==20 and bf==expected==af['files'] and af['unchanged'],'20recordedcustodypairs')
    for pin in p['pins']:
        q=Path(pin['path'])
        if q.parent==P:
            b=q.read_bytes();need(len(b)==pin['bytes'] and H(b)==pin['sha256'],'ownedprecallpin')
    st=J('capture/status.json');need(st['error'] is None and st['watch_unchanged'] and st['attempts']==st['children_started']==3 and not st['automatic_retry'],'capture3success');need(st['selected_bytes_read']==st['validated_bytes']==1580 and st['validated_words']==395 and st['selected_table_bytes_read']==16 and st['native_original_instruction_execution']==0,'1596staticbounds')
    src=(P/'source-context.jsonl').read_bytes().splitlines(keepends=True);meta=J('selected-metadata.json')['records'];need(len(src)==len(meta)==3,'3completeC');words={};branches=[];pairs=[];rec=[];cb=cl=warnings=0
    for i,((start,n),line,sm) in enumerate(zip(RANGES,src,meta)):
        r=sm['C1_metadata'];need(len(line)==r['raw_bytes'] and H(line)==r['raw_sha256'],'rawC1');d=json.loads(line);c=d.pop('code');need(d==r['metadata'] and d['body_ranges']==[[hex(start),hex(start+n-1)]] and d['body_bytes']==n,'allmetadata');need(d['error'] is None and not d['thunk'] and not d['timed_out'] and not d['partial_code'],'Cstatus');need(len(c.encode())==d['code_bytes'] and H(c.encode())==d['code_sha256'],'fullC');cb+=len(c.encode());cl+=len(c.splitlines());warnings+=len(d['warnings']);name=hex(start)[2:];raw=(P/('capture/'+name+'.bin')).read_bytes();rows=J('capture/'+name+'.stdout.json');need(len(raw)==n and len(rows)==n//4,'wholeextent');need(J('capture/extraction.json')['ranges'][i]=={**p['ranges'][i],'sha256':H(raw)},'extraction')
        for j,row in enumerate(rows):
            pc=start+4*j;bb=raw[4*j:4*j+4];need(type(row['offset']) is int and row['offset']==pc and type(row['size']) is int and row['size']==4 and row['bytes']==bb.hex(),'all395associations');w=int.from_bytes(bb,'little');words[pc]=w;z=flow(pc,w)
            if z:
                if 'target' in z:need(row.get('jump')==int(z['target'],16),'rawflowtarget')
                branches.append(z)
            if w&0x3e000000==0x28000000:
                v=w>>26&1;opc=w>>30&3
                if (not v and opc==2) or(v and opc in [0,1,2]):
                    scale=(4<<opc) if v else 8;pairs.append({'pc':hex(pc),'bank':'SIMD/FP' if v else 'GPR','element_bytes':scale,'load':bool(w>>22&1),'mode':w>>23&3,'Rt':w&31,'Rn':w>>5&31,'Rt2':w>>10&31,'offset':sx(w>>15&127,7)*scale})
        a=J('capture/'+name+'.invocation-after.json');b=J('capture/'+name+'.invocation-before.json');pid=J('capture/'+name+'.pid.json');argv=[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(start),'-s',hex(start),'-q','-c','pdj '+str(n//4),str(P/('capture/'+name+'.bin'))];need(a['argv']==b['argv']==pid['argv']==argv and a['pid']==pid['pid']==pid['pgid'],'argvpid');need(a['exit_code']==0 and a['error'] is None and not a['timed_out'] and (P/('capture/'+name+'.stderr')).read_bytes()==b'','status');need(a['timeout_seconds']==30 and a['stdin']=='DEVNULL' and a['core_limit_bytes']==0 and a['new_process_session'] and a['cleanup']=='process-group-already-gone','policy');need(a['started_utc']<=pid['spawned_utc']<=a['finished_utc'],'time');rec.append({'entry':hex(start),'pid':a['pid'],'UTC':[a['started_utc'],a['finished_utc']]})
    need(cb==9543 and cl==318 and warnings==9 and len(words)==395,'3totals')
    for x,y in zip(rec,rec[1:]):need(x['UTC'][1]<=y['UTC'][0],'sequential')
    receipt=J('source-read-receipt.json');need(receipt['approval_identity_verified_before_C_read_utc']<=receipt['selected_C_record_acquisition_finished_utc']<st['started_utc'],'approvalCbeforecapture')
    t=J('capture/table-words.json');need(t['total_bytes']==16 and len(t['words'])==2,'2words');values=[]
    for row,(a,v) in zip(t['words'],DATA):
        b=(P/('capture/word-'+hex(a)[2:]+'.bin')).read_bytes();need(row=={'start':hex(a),'file_offset':a,'bytes':8,'raw_hex':b.hex(),'sha256':H(b)} and len(b)==8 and int.from_bytes(b,'little')==v,'rawintegerbytes');values.append({'position':hex(a),'raw_hex':b.hex(),'stored_integer':hex(v)})
    fields(words);need({int(b['pc'],16):(b['kind'],b['Rn']) for b in branches if b['kind'] in ['BR','BLR']}==INDIRECT,'complete4indirectoperands');a=J('assessment.json');claims(a);controls=[]
    def reject(label,fn):
        try:fn()
        except(ValueError,KeyError,TypeError):controls.append(label);return
        raise ValueError('acceptednegative:'+label)
    for label,pc,v in [('setterwrongmember',0x16110,words[0x16110]^(1<<10)),('setterwrongslot',0x1611c,words[0x1611c]^(1<<10)),('tailchangedtolink',0x16120,words[0x16120]^(1<<21)),('processreceiverwrong',0x15b20,0xaa0103f5),('processinnerwrongmember',0x15ee0,words[0x15ee0]^(1<<10)),('processwrongslot',0x15ef0,words[0x15ef0]^(1<<10)),('querycommandconflation',0x159a0,words[0x159a0]^(1<<10)),('queryouterstatewrongoffset',0x159ac,words[0x159ac]^(1<<10)),('postindexframecorrupted',0x160a0,words[0x160a0]^(1<<15))]:
        bad=words.copy();bad[pc]=v;reject(label,lambda bad=bad:fields(bad))
    z=copy.deepcopy(p);z['data_words'].append({'start':'0x5c0f8','file_offset':0x5c0f8,'bytes':8});reject('forbiddenPword',lambda:plan_scope(z))
    for label,key,v in [('P=Oinvented','P_equals_or_distinct_from_O','equal'),('OmemberPproved','current_O_plus8_equals_P','proved'),('stablePtable','current_P_table_continuity','proved'),('callbackjoininvented','Q_D_I_binding','proved'),('Damperlaw','index63_internal_Damper','noeffect')]:
        z=copy.deepcopy(a);z['carrier_status'][key]=v;reject(label,lambda z=z:claims(z))
    z=copy.deepcopy(a);z['claims'][5]['runtime_targets_proved']=True;reject('rawwordruntimepromotion',lambda:claims(z))
    z=copy.deepcopy(a);z['counts']['new_resolved_runtime_sites']=4;reject('sitecredit',lambda:claims(z))
    z=copy.deepcopy(a);z['no_successor_selected']=False;reject('automatic targetfollow',lambda:claims(z))
    if(P/'manifest.json').exists():
        m=J('manifest.json');need({str(q.relative_to(P)) for q in P.rglob('*') if q.is_file() and q.name!='manifest.json'}=={x['path'] for x in m['files']},'exacttree')
        for x in m['files']:
            b=(P/x['path']).read_bytes();need(len(b)==x['bytes'] and H(b)==x['sha256'],'sealedhash')
    return {'status':'PASS-packet-only','C_records':3,'C_bytes':cb,'C_lines':cl,'warning_occurrences':warnings,'native_bytes':1580,'native_rows':395,'literal_bytes':16,'recorded_custody_pairs':20,'receipts':rec,'all_raw_flow_forms':branches,'all_raw_pair_fields':pairs,'critical_u64_load_fields':[{ 'pc':hex(pc),'Rt':t[0],'Rn':t[1],'offset':t[2]} for pc,t in LOADS.items()],'raw_integer_observations':values,'negative_controls':controls,'external_paths_reopened':0,'new_decoder_original_model_calls':0,'limit':'Narrowrawfield/staticchecks,notcompleteISAdecoder/translatedmodel/formalABI/runtimebinding/mathoracle.'}

if __name__=='__main__':
    need(sys.argv[1:]==['--check'],'only --check')
    print(json.dumps(check(),indent=2))
