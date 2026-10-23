"""Fixed packet-only data checks; no external pins, children, original calls or collector imports."""
import copy
import hashlib
import json
from pathlib import Path
import sys
P=Path(__file__).resolve().parent
PRE='93395a920454a3df50545b05eb15a1b62f85b291b612a60ae375e9a5cbcde896'
RANGES=[(0x159e4,128),(0x15a64,128)]
# (fixed unsigned-immediate load/store form, Rt, Rn, byte offset, scale)
MEM={0x159e4:(0xbd000000,0,0,0x10,4),0x159e8:(0xbd400000,1,0,0x20,4),0x15a18:(0xf9000000,8,0,0x18,8),0x15a20:(0xf9000000,8,0,0x2028,8),0x15a28:(0x3d800000,2,0,0x4030,16),0x15a2c:(0xbd000000,1,0,0x20,4),0x15a30:(0xf9400000,0,0,8,8),0x15a38:(0xf9400000,8,0,0,8),0x15a3c:(0xf9400000,1,8,0x50,8),0x15a44:(0xb9000000,31,0,0x20,4),0x15a4c:(0xf9000000,8,0,0x2028,8),0x15a54:(0x3d800000,1,0,0x4030,16),0x15a58:(0xf9400000,0,0,8,8),0x15a64:(0xbd400000,0,0,0x20,4),0x15a80:(0xbd400000,1,0,0x10,4),0x15a98:(0xf9000000,8,0,0x18,8),0x15aa0:(0xf9000000,8,0,0x2028,8),0x15aa8:(0x3d800000,1,0,0x4030,16),0x15aac:(0xbd000000,0,0,0x20,4),0x15ab0:(0xf9400000,0,0,8,8),0x15ab8:(0xf9400000,8,0,0,8),0x15abc:(0xf9400000,1,8,0x58,8),0x15ac4:(0xb9000000,31,0,0x20,4),0x15acc:(0xf9000000,8,0,0x2028,8),0x15ad4:(0x3d800000,0,0,0x4030,16),0x15ad8:(0xf9400000,0,0,8,8)}
FIX={0x159ec:0x1e202028,0x159f4:0x52824de8,0x159f8:0x72a75068,0x159fc:0x1e270102,0x15a00:0x1e22cc21,0x15a04:0x1e2c1002,0x15a08:0x1f000822,0x15a0c:0x9e390048,0x15a10:0xf100011f,0x15a14:0x9a9f1508,0x15a1c:0x52808028,0x15a24:0x6f00e402,0x15a40:0xd61f0020,0x15a48:0x52808028,0x15a50:0x6f00e401,0x15a60:0xd65f03c0,0x15a68:0x1e202008,0x15a70:0x52824de8,0x15a74:0x72a75068,0x15a78:0x1e270101,0x15a7c:0x1e21cc00,0x15a84:0x1e2c1002,0x15a88:0x1f000821,0x15a8c:0x9e390028,0x15a90:0xf100011f,0x15a94:0x9a9f1508,0x15a9c:0x52808028,0x15aa4:0x6f00e401,0x15ac0:0xd61f0020,0x15ac8:0x52808028,0x15ad0:0x6f00e400,0x15ae0:0xd65f03c0}

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

def fields(words):
    for pc,(op,rt,rn,off,scale) in MEM.items():
        w=words[pc];need(w&0xffc00000==op and (w&31,w>>5&31,(w>>10&4095)*scale)==(rt,rn,off),'rawMEM:'+hex(pc))
    for pc,w in FIX.items():need(words[pc]==w,'rawfixed:'+hex(pc))
    need(words[0x159f0]&15==13 and words[0x15a6c]&15==13,'LEconditions')

def scope(p):
    need(p['ranges']==[{'start':hex(a),'end_exclusive':hex(a+n),'file_offset':a,'bytes':n,'words':n//4} for a,n in RANGES],'exactranges')
    need(p['data_words']==[] and p['selected_bytes']==256 and p['selected_words']==64 and p['selected_data_bytes']==0,'noadditionaldata')

def claims(a):
    need(a['scope']=={'whole_C_records':2,'C_bytes':2115,'C_lines':81,'warning_occurrences':4,'raw_C1_bytes':3178,'native_bodies':2,'native_bytes':256,'native_rows':64,'data_words':0,'data_bytes':0,'old_actual_raw_or_source_replayed':0},'scope')
    for k,v in a['carrier_status'].items():need(v==('conditional-premise-only' if k=='current_O_plus8_equals_P' else 'unknown'),'carrier:'+k)
    f=a['conditional_inner_operand_frontier'];need(not f['P_word_content_acquired'] and not f['complete_P_table_set_proved'] and not f['offset10_operand_proved'],'noPtablepromotion')
    need(f['new_offsets']==['0x50','0x58'] and f['inherited_offsets']==['0x38','0x60','0x68'],'offsetscope')
    need(a['claims'][1]['runtime_target_proved'] is False and a['claims'][3]['runtime_target_proved'] is False and a['claims'][4]['native_operation_order_numeric_behavior_or_FP_state_executed'] is False,'noruntimeorFPproof')
    need(a['claims'][6]['automatic_composition_proved'] is False and len(a['claims'][6]['premises'])>=7,'conditionalcomposition')
    need(a['counts']['new_resolved_runtime_sites']==0 and a['counts']['main_Live_inventory']=='25095 of268015 unchanged','siteuniverse')
    need(a['required_status']=='U/OPEN unchanged' and a['no_successor_selected'] and len(a['claims'])==8,'noclosure')

def check():
    pb=(P/'pre-call-manifest.json').read_bytes();need(H(pb)==PRE,'precall');p=json.loads(pb);scope(p)
    before=J('capture/before-identities.json');after=J('capture/after-identities.json');expected=[p['image'],p['tool'],*p['pins'],{'path':str(P/'pre-call-manifest.json'),'bytes':len(pb),'sha256':PRE}]
    need(len(before)==16 and before==expected==after['files'] and after['unchanged'],'16recordedcustody')
    for pin in p['pins']:
        q=Path(pin['path'])
        if q.parent==P:
            b=q.read_bytes();need(len(b)==pin['bytes'] and H(b)==pin['sha256'],'ownedpin')
    st=J('capture/status.json');need(st['error'] is None and st['watch_unchanged'] and st['attempts']==st['children_started']==2 and not st['automatic_retry'],'capturestatus')
    need(st['selected_bytes_read']==st['validated_bytes']==256 and st['validated_words']==64 and st['selected_table_bytes_read']==st['native_original_instruction_execution']==0,'exactstaticbounds')
    need(J('capture/table-words.json')['words']==[] and J('capture/table-words.json')['total_bytes']==0,'zeroactualwordcontent')
    src=(P/'source-context.jsonl').read_bytes().splitlines(keepends=True);meta=J('selected-metadata.json')['records'];need(len(src)==len(meta)==2 and sum(map(len,src))==3178,'tworawrecords');words={};flows=[];receipts=[];cb=cl=warn=0
    for i,((a,n),rawline,m) in enumerate(zip(RANGES,src,meta)):
        r=m['C1_metadata'];need(len(rawline)==r['raw_bytes'] and H(rawline)==r['raw_sha256'],'Craw');d=json.loads(rawline);c=d.pop('code');need(d==m['complete_metadata'] and d['body_ranges']==[[hex(a),hex(a+n-1)]] and d['body_bytes']==n,'completegeometry');need(d['error'] is None and not d['thunk'] and not d['partial_code'] and not d['timed_out'] and d['state']=='exported-with-warnings','Cstatus');need(len(c.encode())==r['code_bytes'] and len(c.splitlines())==r['code_lines'] and H(c.encode())==r['code_sha256'],'Cfull');cb+=len(c.encode());cl+=len(c.splitlines());warn+=len(d['warnings'])
        name=hex(a)[2:];raw=(P/('capture/'+name+'.bin')).read_bytes();rows=J('capture/'+name+'.stdout.json');need(len(raw)==n and len(rows)==n//4,'extent');need(J('capture/extraction.json')['ranges'][i]=={**p['ranges'][i],'sha256':H(raw)},'extracthash')
        for j,row in enumerate(rows):
            pc=a+4*j;bb=raw[4*j:4*j+4];need(type(row['offset']) is int and row['offset']==pc and type(row['size']) is int and row['size']==4 and row['bytes']==bb.hex(),'all64associations');w=int.from_bytes(bb,'little');words[pc]=w;f=flow(pc,w)
            if f:
                if 'target' in f:need(row.get('jump')==int(f['target'],16),'rawflowtarget')
                flows.append(f)
        b=J('capture/'+name+'.invocation-before.json');r=J('capture/'+name+'.invocation-after.json');pid=J('capture/'+name+'.pid.json');argv=[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(a),'-s',hex(a),'-q','-c','pdj 32',str(P/('capture/'+name+'.bin'))]
        need(r['argv']==b['argv']==pid['argv']==argv and r['pid']==pid['pid']==pid['pgid'],'argvpid');need(r['exit_code']==0 and r['error'] is None and not r['timed_out'] and (P/('capture/'+name+'.stderr')).read_bytes()==b'','receiptstatus');need(r['timeout_seconds']==30 and r['stdin']=='DEVNULL' and r['core_limit_bytes']==0 and r['new_process_session'] and r['cleanup']=='process-group-already-gone','processpolicy');need(r['started_utc']<=pid['spawned_utc']<=r['finished_utc'],'times');receipts.append({'entry':hex(a),'pid':r['pid'],'started_utc':r['started_utc'],'finished_utc':r['finished_utc']})
    need(cb==2115 and cl==81 and warn==4 and len(words)==64,'totals');need(receipts[0]['finished_utc']<=receipts[1]['started_utc'],'sequential')
    receipt=J('source-read-receipt.json');need(receipt['prerequisite_approval']['sha256']=='53a6956a7cfeff8d56ca8e302b04898bd7cc5f032f797c40db514a5e432d4197' and receipt['approval_identity_verified_before_C_read_utc']<=receipt['selected_C_record_acquisition_finished_utc']<st['started_utc'],'approvalbeforeCbeforecapture')
    fields(words);need(len(flows)==10 and {int(f['pc'],16):(f['kind'],f.get('Rn')) for f in flows if f['kind'] in ['BR','BLR','BL']}=={0x15a40:('BR',1),0x15ac0:('BR',1)},'localtailsnoothercalls')
    a=J('assessment.json');claims(a);neg=[]
    def reject(name,fn):
        try:fn()
        except(ValueError,KeyError,TypeError):neg.append(name);return
        raise ValueError('negativeaccepted:'+name)
    for name,pc,delta in [('wrongentryFPstore',0x159e4,1<<10),('wrongmember50',0x15a30,1<<10),('wrongslot50',0x15a3c,1<<10),('tailmadecall',0x15a40,1<<21),('signedconversionrepaired',0x15a0c,1<<16),('FMADDchanged',0x15a08,1<<15),('Qstorewidthchanged',0x15a28,1<<30),('wrongstate2028',0x15a20,1<<10),('wrongslot58',0x15abc,1<<10),('wrongmember58',0x15ab0,1<<10)]:
        z=words.copy();z[pc]^=delta;reject(name,lambda z=z:fields(z))
    z=copy.deepcopy(p);z['data_words']=[{'start':'0x5c110','file_offset':0x5c110,'bytes':8}];reject('forbiddenPword',lambda:scope(z))
    for name,k,v in [('entryOassumed','incoming_candidate_receiver_equals_public_O','proved'),('Pmemberassumed','current_O_plus8_equals_P','proved'),('stablePtable','current_P_table_continuity','proved'),('publicABIassumed','runtime_encoding_class_ABI_target_public','proved')]:
        z=copy.deepcopy(a);z['carrier_status'][k]=v;reject(name,lambda z=z:claims(z))
    z=copy.deepcopy(a);z['claims'][1]['runtime_target_proved']=True;reject('tailtargetpromoted',lambda:claims(z))
    z=copy.deepcopy(a);z['claims'][4]['native_operation_order_numeric_behavior_or_FP_state_executed']=True;reject('FPexperimentinvented',lambda:claims(z))
    z=copy.deepcopy(a);z['conditional_inner_operand_frontier']['complete_P_table_set_proved']=True;reject('completePtableinvented',lambda:claims(z))
    z=copy.deepcopy(a);z['counts']['new_resolved_runtime_sites']=2;reject('mainsitecredit',lambda:claims(z))
    if(P/'manifest.json').exists():
        m=J('manifest.json');need({str(q.relative_to(P)) for q in P.rglob('*') if q.is_file() and q.name!='manifest.json'}=={r['path'] for r in m['files']},'sealedtree')
        for r in m['files']:
            b=(P/r['path']).read_bytes();need(len(b)==r['bytes'] and H(b)==r['sha256'],'sealedhash')
    return {'status':'PASS-packet-only','C_records':2,'C_bytes':cb,'C_lines':cl,'warning_occurrences':warn,'native_rows':len(words),'native_bytes':256,'data_bytes':0,'recorded_custody_pairs':16,'receipts':receipts,'all_raw_flow_forms':flows,'checked_memory_fields':[{'pc':hex(pc),'form':hex(v[0]),'Rt':v[1],'Rn':v[2],'byte_offset':v[3],'scale':v[4]} for pc,v in MEM.items()],'fixed_raw_FP_literal_tail_forms':len(FIX),'negative_controls':neg,'external_paths_reopened':0,'new_decoder_original_model_calls':0,'limit':'Narrow static raw-field checks; not a full ISA decoder, runtime ABI/encoding proof, FP execution or numeric oracle.'}

if __name__=='__main__':
    need(sys.argv[1:]==['--check'],'only --check')
    print(json.dumps(check(),indent=2))
