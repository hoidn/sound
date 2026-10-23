"""Read this fixed packet only. No external pin opens, children, original or helper imports."""
import copy
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
PRE='d70ca564f407972804630c9e2728be7993981751c59f0545abc2226fcc7cd2dc'
EXPECTED=[(0x136d0,236),(0x19db8,228),(0x162ec,180),(0x1306c,72),(0x130e4,96),(0x13628,80)]
DATA=[(0x5d5f8,0x16110),(0x5d620,0x15ae4),(0x5d628,0x15998)]

def need(x,msg):
    if not x: raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((HERE/n).read_bytes())
def sx(n,b):return n-(1<<b) if n&(1<<(b-1)) else n

def branch(pc,w):
    if w&0x7c000000==0x14000000:return {'pc':hex(pc),'kind':'BL' if w>>31 else 'B','target':hex(pc+sx(w&0x3ffffff,26)*4)}
    if w&0xff000010==0x54000000:return {'pc':hex(pc),'kind':'B.cond','condition':w&15,'target':hex(pc+sx((w>>5)&0x7ffff,19)*4)}
    if w&0x7e000000==0x34000000:return {'pc':hex(pc),'kind':'CBNZ' if w&(1<<24) else 'CBZ','Rn':w&31,'target':hex(pc+sx((w>>5)&0x7ffff,19)*4)}
    tag=w&0xfffffc1f
    if tag in [0xd61f0000,0xd63f0000,0xd65f0000]:return {'pc':hex(pc),'kind':{0xd61f0000:'BR',0xd63f0000:'BLR',0xd65f0000:'RET'}[tag],'Rn':w>>5&31}
    return None

def mov(w,rd,rn):need(w&0xffe0ffe0==0xaa0003e0 and w&31==rd and w>>16&31==rn,'MOV carrier')
def ldr(w,rt,rn,off):need(w&0xffc00000==0xf9400000 and (w&31,w>>5&31,(w>>10&4095)*8)==(rt,rn,off),'LDR64 fields')
def adr(pc,w,rd,t):
    need(w&0x9f000000==0x10000000,'ADR type');need((w&31,pc+sx(((w>>5)&0x7ffff)*4+(w>>29&3),21))==(rd,t),'ADR fields')
def storeS(w,rt,rn,off):need(w&0xffc00000==0xbd000000 and (w&31,w>>5&31,(w>>10&4095)*4)==(rt,rn,off),'STR S fields')

def raw_fields(words):
    for pc,rd,rn in [(0x136e4,19,0),(0x137a4,0,19),(0x162f8,19,0),(0x1634c,0,19),(0x16390,0,19)]:mov(words[pc],rd,rn)
    need(words[0x137b8]==words[0x16358]==words[0x1639c]==0xd65f03c0,'returnX30')
    adr(0x13744,words[0x13744],8,0x5d648)
    need(words[0x1374c]==0x91004108 and words[0x13750]==0xf90006e8,'derived5d658 store')
    for pc,rt,rn,off in [(0x130f8,8,0,0),(0x130fc,8,8,0x50),(0x13638,8,0,0),(0x1363c,8,8,0x58)]:ldr(words[pc],rt,rn,off)
    need(words[0x130f4]==0x9e220020,'signedX1 toS0 instruction')
    need(branch(0x13100,words[0x13100])=={'pc':'0x13100','kind':'BLR','Rn':8} and branch(0x13640,words[0x13640])=={'pc':'0x13640','kind':'BLR','Rn':8},'two exportcall operands')
    need(words[0x16338]==0xf110003f,'CMP unsignedX1 bound400')
    need(branch(0x1633c,words[0x1633c])=={'pc':'0x1633c','kind':'B.cond','condition':8,'target':'0x1635c'},'small branch bound/direction')
    need(branch(0x1632c,words[0x1632c])['target']=='0x16314' and words[0x16328]==0xf140113f,'clearloop bound')
    need(words[0x19e6c]==0x1e25c000,'FRINTZ S0 notintegerconversion')
    storeS(words[0x19e70],0,20,0x30)

def scope(a):
    need(a['scope']=={'whole_C_records':6,'C_bytes':3486,'C_lines':145,'raw_C1_bytes':5746,'native_bodies':6,'native_bytes':892,'native_rows':223,'literal_words':3,'literal_bytes':24,'total_new_native_data_bytes':916,'old_actual_raw_replayed':0},'wholefixedscope')
    c=a['carrier_status'];need(c['B_equals_P']=='conditional-normalreturn-selected-path-only','conditionalP=B')
    for key in ['P_equals_or_distinct_from_O','Q_D_I_binding','O_current_table_at_public_dispatch','actual_runtime_pointer_encoding_targets_class_ABI_public','index63_internal_Damper']:need(c[key]=='unknown','unknowncarrier/public')
    need(c['O_firstword_after_selected162ec_smallpath']=='conditional-local-nonwrap-nonalias-only','boundedlocalpreservation')
    need(a['claims'][5]['runtime_targets_proved'] is False,'rawnotruntime')
    need(a['extra_operand_frontier']['no_new_words_read'] is True and a['extra_operand_frontier']['proved_new_offsets']==['0x50','0x58'],'onlynewoperandproof')
    need(a['counts']['new_resolved_runtime_sites']==0 and a['counts']['main_Live_inventory']=='25095 of268015 unchanged','no runtime/maincredit')
    need(a['required_status']=='U/OPEN unchanged' and a['no_successor_selected'] is True and len(a['claims'])==8,'no publicclosure/successor')

def check():
    pb=(HERE/'pre-call-manifest.json').read_bytes();need(sha(pb)==PRE,'precall');p=json.loads(pb);st=read('capture/status.json');bf=read('capture/before-identities.json');af=read('capture/after-identities.json')
    expected=[p['image'],p['tool'],*p['pins'],{'path':str(HERE/'pre-call-manifest.json'),'bytes':len(pb),'sha256':PRE}]
    need(len(bf)==19 and bf==expected==af['files'] and af['unchanged'] is True,'19recordedcustodypairs')
    for pin in p['pins']:
        q=Path(pin['path'])
        if q.parent==HERE:
            b=q.read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'ownedprecallpin')
    need(st['error'] is None and st['watch_unchanged'] is True and st['attempts']==st['children_started']==6,'single6success')
    need(st['selected_bytes_read']==st['validated_bytes']==892 and st['validated_words']==223 and st['selected_table_bytes_read']==24 and st['native_original_instruction_execution']==0,'916staticbytes')
    source=(HERE/'source-context.jsonl').read_bytes().splitlines(keepends=True);meta=read('selected-metadata.json')['records'];need(len(source)==len(meta)==6,'6wholeC');cb=cl=0;words={};branches=[];pairs=[];receipts=[];malformed=[]
    for i,((start,n),r,line,record) in enumerate(zip(EXPECTED,p['ranges'],source,meta)):
        need(r=={'start':hex(start),'end_exclusive':hex(start+n),'file_offset':start,'bytes':n,'words':n//4},'exactexplicitrange');s=record['C1_metadata'];need(len(line)==s['raw_bytes'] and sha(line)==s['raw_sha256'],'rawC1');d=json.loads(line);c=d.pop('code');need(d==s['metadata'] and d['body_ranges']==[[hex(start),hex(start+n-1)]] and d['body_bytes']==n,'metadata');need(d['warnings']==[] and d['error'] is None and not d['thunk'] and not d['partial_code'] and not d['timed_out'],'status');need(len(c.encode())==d['code_bytes'] and sha(c.encode())==d['code_sha256'],'Cbytes');cb+=len(c.encode());cl+=len(c.splitlines())
        name=hex(start)[2:];raw=(HERE/('capture/'+name+'.bin')).read_bytes();rows=read('capture/'+name+'.stdout.json');need(len(raw)==n and len(rows)==n//4,'rawbounds');need(read('capture/extraction.json')['ranges'][i]=={**r,'sha256':sha(raw)},'extraction')
        for j,row in enumerate(rows):
            pc=start+4*j;b=raw[4*j:4*j+4];need(type(row['offset']) is int and row['offset']==pc and type(row['size']) is int and row['size']==4 and row['bytes']==b.hex(),'all223associations');w=int.from_bytes(b,'little');words[pc]=w;z=branch(pc,w)
            if z:
                if 'target' in z:need(row.get('jump')==int(z['target'],16),'rawbranchtarget')
                branches.append(z)
            if '0lr' in row['opcode']:malformed.append(hex(pc))
            if w&0x3e000000==0x28000000:
                V=w>>26&1;opc=w>>30&3
                if (not V and opc==2) or (V and opc in [0,1,2]):
                    scale=(4<<opc) if V else 8;pairs.append({'pc':hex(pc),'bank':'SIMD/FP' if V else 'GPR','element_bytes':scale,'load':bool(w>>22&1),'mode':w>>23&3,'Rt':w&31,'Rn':w>>5&31,'Rt2':w>>10&31,'offset':sx(w>>15&127,7)*scale})
        rec=read('capture/'+name+'.invocation-after.json');beg=read('capture/'+name+'.invocation-before.json');pid=read('capture/'+name+'.pid.json');argv=[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(start),'-s',hex(start),'-q','-c','pdj '+str(n//4),str(HERE/('capture/'+name+'.bin'))]
        need(rec['argv']==beg['argv']==pid['argv']==argv and rec['pid']==pid['pid']==pid['pgid'],'argvpid');need(rec['exit_code']==0 and rec['error'] is None and rec['timed_out'] is False and (HERE/('capture/'+name+'.stderr')).read_bytes()==b'','childstatus');need(rec['timeout_seconds']==30 and rec['stdin']=='DEVNULL' and rec['core_limit_bytes']==0 and rec['new_process_session'] and rec['cleanup']=='process-group-already-gone','limits');need(rec['started_utc']<=pid['spawned_utc']<=rec['finished_utc'],'times');receipts.append({'entry':hex(start),'pid':rec['pid'],'UTC':[rec['started_utc'],rec['finished_utc']]})
    need(cb==3486 and cl==145 and len(words)==223,'wholesettotals')
    for a,b in zip(receipts,receipts[1:]):need(a['UTC'][1]<=b['UTC'][0],'sequential')
    s=read('source-read-receipt.json');need(s['approval_identity_verified_before_C_read_utc']<=s['selected_C_record_acquisition_finished_utc']<st['started_utc'],'approval/Cbeforecapture')
    t=read('capture/table-words.json');need(t['total_bytes']==24 and len(t['words'])==3,'3words')
    vals=[]
    for row,(addr,val) in zip(t['words'],DATA):
        b=(HERE/('capture/word-'+hex(addr)[2:]+'.bin')).read_bytes();need(row=={'start':hex(addr),'file_offset':addr,'bytes':8,'raw_hex':b.hex(),'sha256':sha(b)} and len(b)==8 and int.from_bytes(b,'little')==val,'wordbytes');vals.append({'position':hex(addr),'stored_integer':hex(val),'raw_hex':b.hex()})
    need([x['start'] for x in p['data_words']]==[hex(x[0]) for x in DATA],'no extra words')
    raw_fields(words);a=read('assessment.json');scope(a);rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,TypeError):rejected.append(name);return
        raise ValueError('acceptednegative:'+name)
    for name,pc,v in [('helperreturnswrongcarrier',0x137a4,0xaa1403e0),('initialhelperwrongincoming',0x136e4,0xaa0103f3),('ratewrongslot',0x130fc,words[0x130fc]^(1<<10)),('resetwrongregister',0x1363c,words[0x1363c]^1),('rateunsignednot signed',0x130f4,words[0x130f4]^(1<<16)),('smallbranchwrongcondition',0x1633c,words[0x1633c]^1),('smallbranchwrongbound',0x16338,words[0x16338]^(1<<10)),('FPstoreintegerreplacement',0x19e70,0xb9003280),('FRINTZreplaced',0x19e6c,words[0x19e6c]^(1<<16)),('derivedaddresswrongoffset',0x1374c,words[0x1374c]^(1<<10))]:
        bad=words.copy();bad[pc]=v;reject(name,lambda bad=bad:raw_fields(bad))
    for name,key,val in [('unconditionalB=P','B_equals_P','proved'),('Otablecurrentinvented','O_current_table_at_public_dispatch','proved'),('P=Oinvented','P_equals_or_distinct_from_O','equal'),('cleanupbindinginvented','Q_D_I_binding','proved'),('namedDamperlaw','index63_internal_Damper','noeffect')]:
        z=copy.deepcopy(a);z['carrier_status'][key]=val;reject(name,lambda z=z:scope(z))
    z=copy.deepcopy(a);z['claims'][5]['runtime_targets_proved']=True;reject('rawwordruntimepromotion',lambda:scope(z))
    z=copy.deepcopy(a);z['counts']['new_resolved_runtime_sites']=3;reject('siteclosure',lambda:scope(z))
    z=copy.deepcopy(a);z['no_successor_selected']=False;reject('automatic target follow',lambda:scope(z))
    if (HERE/'manifest.json').exists():
        m=read('manifest.json');actual={str(f.relative_to(HERE)) for f in HERE.rglob('*') if f.is_file() and f.name!='manifest.json'};need(actual=={x['path'] for x in m['files']},'exacttree')
        for x in m['files']:
            b=(HERE/x['path']).read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'sealedhash')
    return {'status':'PASS-packet-only','C_records':6,'C_bytes':cb,'C_lines':cl,'native_bytes':892,'native_rows':223,'raw_literal_bytes':24,'recorded_custody_pairs':19,'receipts':receipts,'raw_branch_RET_forms':branches,'all_raw_pair_fields':pairs,'malformed0lr_sites_retained':malformed,'literal_integer_observations':vals,'negative_controls':rejected,'external_paths_reopened':0,'new_decoder_or_original_calls':0,'limit':'Narrowrawfields/staticpredicates only,notfullindependentdisassembler/translatedexecution/ABI/provider/object/FPnumericmodel.'}

if __name__=='__main__':
    need(sys.argv[1:]==['--check'],'only --check')
    print(json.dumps(check(),indent=2))
