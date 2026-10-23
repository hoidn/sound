"""Retained packet only. No external pin/image/tool/source/index reads or children."""
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
CAP=HERE/'capture'
SITES=[0x3e10,0x3e38,0xbd20,0xc0b0,0xc0d0,0xc2d0,0xc368,0xede4]

def need(v,msg):
    if not v: raise ValueError(msg)

def sx(v,n): return v-(1<<n) if v&(1<<(n-1)) else v

def mem(w):
    need(w&0xff800000==0xf9000000,'64-bit unsigned memory')
    return {'load':bool((w>>22)&1),'rt':w&31,'rn':(w>>5)&31,'offset':8*((w>>10)&4095)}

def mov(w):
    need(w&0xffe0ffe0==0xaa0003e0,'unshifted64-bit MOV alias')
    return (w&31,(w>>16)&31)

def adr(pc,w):
    need(w&0x9f000000==0x10000000,'ADR')
    return (w&31,pc+sx((((w>>5)&0x7ffff)<<2)|((w>>29)&3),21))

def direct(pc,w):
    need(w&0x7c000000==0x14000000,'B/BL immediate')
    return {'link':bool(w>>31),'target':pc+4*sx(w&0x3ffffff,26)}

def indirect(w):
    form=w&0xfffffc1f
    need(form in (0xd61f0000,0xd63f0000),'BR/BLR')
    return {'link':form==0xd63f0000,'rn':(w>>5)&31}

def pair(w):
    need(w&0x3e000000==0x28000000 and w>>30==2,'GPR64 pair')
    return {'load':bool((w>>22)&1),'mode':(w>>23)&3,'offset':8*sx((w>>15)&127,7),
            'rt':w&31,'rt2':(w>>10)&31,'rn':(w>>5)&31}

def addimm(w):
    need(w&0xffc00000==0x91000000,'ADD64 unshifted immediate')
    return (w&31,(w>>5)&31,(w>>10)&4095)

def wide(w):
    need(w&0x7f800000 in (0x52800000,0x72800000),'MOVZ/MOVK immediate')
    return {'rd':w&31,'keep':bool((w>>29)&1),'shift':16*((w>>21)&3),'imm':(w>>5)&65535}

def registrations(w):
    result=[];rp=None;idx=None;ip=None
    for pc in range(0x3ddc,0x4124,4):
        word=w[pc]
        if word&0xffe0ffe0==0xaa0003e0 and mov(word)==(0,19):rp=pc
        if word&0x7f800000==0x52800000 and word&31==1:
            val=wide(word);need(val['shift']==0,'unshifted index');idx=val['imm'];ip=pc
        if word&0x7c000000==0x14000000:
            target=direct(pc,word)['target']
            if target in (0xc650,0xc754,0xc8a4,0xc9f8):
                need(rp is not None and idx is not None,'registration R/index arguments')
                result.append({'pc':hex(pc),'index':idx,'helper':hex(target),'receiver_MOV_X0_X19':hex(rp),'index_MOV':hex(ip),'tail':not bool(word>>31)})
            if word>>31:rp=None;idx=None;ip=None
        elif word&0xfffffc1f==0xd63f0000:rp=None;idx=None;ip=None
    need([x['index'] for x in result]==list(range(33)),'whole33 registration indices')
    return result

def field_checks(w):
    calls={0xbbf0:0x293d8,0xbbf8:0xc3f8,0xbc14:0x293d8,0xbc1c:0xe47c,0xbc34:0xe56c,
           0xbc48:0xeddc,0xbcfc:0xbbd8,0x3d9c:0x293d8,0x3da4:0x4db0,0x4514:0x1b124,
           0x3df4:0x4124,0x4158:0x2942c}
    for pc,target in calls.items():need(direct(pc,w[pc])=={'link':True,'target':target},'direct '+hex(pc))
    for pc,rd,rm in [(0xbbf4,19,0),(0xbc18,20,0),(0xbc4c,0,20),(0xc40c,19,0),(0xc4cc,0,19),
                     (0xe488,19,0),(0xe4d0,0,19),(0x3da0,19,0),(0x3da8,0,19),
                     (0x4510,19,0),(0x4d84,0,19),(0x3df0,19,0),(0x3df8,20,0),(0xbfd4,23,0)]:
        need(mov(w[pc])==(rd,rm),'carrier '+hex(pc))
    need(adr(0xbbfc,w[0xbbfc])==(8,0x300a0) and addimm(w[0xbc04])==(8,8,16),'300b0 address')
    need(mem(w[0xbc08])=={'load':False,'rt':8,'rn':19,'offset':0},'address through saved A')
    need(mem(w[0xbc20])=={'load':False,'rt':19,'rn':20,'offset':8},'A at O+8')
    need(adr(0xe48c,w[0xe48c])==(8,0x30d10) and w[0xe494]==0xa9007c08,'outer addresspoint')
    need(adr(0xc410,w[0xc410])==(8,0x30a50) and w[0xc418]==0xa9007c08,'initial A addresspoint')
    need(adr(0x4518,w[0x4518])==(8,0x30178),'core address constant')
    need(mem(w[0x4520])=={'load':False,'rt':8,'rn':0,'offset':0},'store through unread helper return')
    need(addimm(w[0x4524])==(8,8,0x118) and mem(w[0x4528])=={'load':False,'rt':8,'rn':0,'offset':0xe0},'core secondary address')
    need(mem(w[0x4138])=={'load':True,'rt':0,'rn':0,'offset':8},'type-helper child receiver')
    for pc,rt,rn,off in [(0x3e00,8,0,0),(0x3e04,8,8,0xd8),(0x3e18,8,20,0),(0x3e1c,8,8,0xd8),
                          (0xbd08,8,19,0),(0xbd0c,8,8,0x68),(0xbe20,8,0,0),(0xbe24,8,8,0x50),
                          (0xc084,8,23,0),(0xc088,8,8,0x60),(0xc0b8,8,23,0),(0xc0bc,8,8,0x68),
                          (0xc2c8,8,0,0),(0xc2cc,8,8,0x38),(0xc360,8,0,0),(0xc364,8,8,0x58),
                          (0xeddc,8,0,0),(0xede0,1,8,0x10),(0xc4b4,0,23,0),(0xc4c0,0,23,0)]:
        need(mem(w[pc])=={'load':pc!=0xc4b4,'rt':rt,'rn':rn,'offset':off},'memory '+hex(pc))
    for pc in SITES:
        need(indirect(w[pc])=={'link':pc!=0xede4,'rn':1 if pc==0xede4 else 8},'selected indirect '+hex(pc))
    need(indirect(w[0xbe28])=={'link':True,'rn':8} and indirect(w[0xbf98])=={'link':True,'rn':16},'extra context')
    for lo,hi,add,dest in [(0xc674,0xc678,0xc67c,22),(0xc788,0xc78c,0xc790,22),
                            (0xc8d8,0xc8dc,0xc8e0,22),(0xca24,0xca28,0xca2c,23)]:
        need(wide(w[lo])=={'rd':8,'keep':False,'shift':0,'imm':0x60}
             and wide(w[hi])=={'rd':8,'keep':True,'shift':16,'imm':0xe},'container offset fragments')
        word=w[add]
        need(word&0xff200000==0x8b000000 and word&31==dest and (word>>5)&31==0
             and (word>>16)&31==8 and (word>>10)&63==0,'container R+e0060')
    for pc,rt,rn in [(0xc6bc,23,22),(0xc7d0,23,22),(0xc920,23,22),(0xca6c,24,23)]:
        need(mem(w[pc])=={'load':True,'rt':rt,'rn':rn,'offset':0},'post-growth buffer reload')
    for pc,load in [(0xc404,False),(0xc4d0,True),(0x3de8,False),(0x4110,True)]:
        need(pair(w[pc])=={'load':load,'mode':2,'offset':48,'rt':29,'rt2':30,'rn':31},'malformed printed FP/LR pair')
    return registrations(w)

def assessment_checks(a,addresses):
    c=a['conclusions']
    for key in ['A_equals_O_or_distinct_allocations','core_factory_S_equals_4500_incoming_T','4500_helper_return_K_equals_T','registration_R_equals_A_or_O','dynamic_cast_D_equals_child_S','runtime_table_targets','actual_Live_public_binding']:
        need(c[key].startswith('unknown'),'no unsupported composition '+key)
    need(c['main_Live_resolved_sites']==25095 and c['main_Live_site_universe']==268015 and c['Electric_local_runtime_resolved_sites']==0,'separate image counts')
    read=[]
    for g in a['whole1563_read_map']:
        x=list(range(int(g['start'],16),int(g['last'],16)+1,4));need(len(x)==g['words'],'read-map count');read+=x
    need(read==addresses,'whole1563 read map')
    need(a['table_bytes_acquired']==0 and a['no_successor_selected'],'no table/successor')

def main():
    planraw=(HERE/'pre-call-manifest.json').read_bytes();plan=json.loads(planraw)
    status=json.loads((CAP/'status.json').read_bytes());before=json.loads((CAP/'before-identities.json').read_bytes());after=json.loads((CAP/'after-identities.json').read_bytes())
    need(hashlib.sha256(planraw).hexdigest()==status['pre_call_manifest_sha256'],'precall identity')
    need(before==after['files'] and after['unchanged'] and len(before)==22,'recorded22 custody pairs')
    need(before[:2]==[plan['image'],plan['tool']] and before[2:-1]==plan['pins'],'declared custody inputs')
    need(status['error'] is None and status['attempts']==status['children_started']==18 and status['validated_words']==1563
         and status['validated_bytes']==status['selected_bytes_read']==6252 and status['native_original_instruction_execution']==0,'fixed actual totals')
    need(plan['table_word_reads']==0 and not list(CAP.glob('word-*')),'no table acquisition')
    meta=json.loads((HERE/'selected-metadata.json').read_bytes());ranges=[]
    for x in meta['records']:
        m=x['metadata'];need(m['error'] is None and not m['thunk'] and not m['partial_code'] and not m['timed_out'],'full metadata')
        need(sum(int(e,16)+1-int(s,16) for s,e in m['body_ranges'])==m['body_bytes'],'explicit extent sum')
        for s,e in m['body_ranges']:
            need(int(s,16)%4==0 and (int(e,16)+1)%4==0,'aligned range');ranges.append((int(s,16),int(e,16)+1))
    ranges.sort();need(len(ranges)==18 and sum(e-s for s,e in ranges)==6252 and all(a[1]<=b[0] for a,b in zip(ranges,ranges[1:])),'whole metadata bound')
    context=(HERE/'source-context.jsonl').read_bytes().splitlines(keepends=True);cm=json.loads((HERE/'context-read-map.json').read_bytes())
    need(len(context)==len(cm['records'])==18 and cm['total_C_lines']==1180 and cm['total_C_bytes']==35587,'whole C context')
    for raw,m in zip(context,cm['records'],strict=True):
        r=json.loads(raw);code=r['code'].encode();need(hashlib.sha256(raw).hexdigest()==m['raw_sha256'] and len(raw)==m['raw_bytes'],'unchanged source context')
        need(len(code)==m['C_bytes'] and hashlib.sha256(code).hexdigest()==m['C_sha256'] and m['full_C_read_ranges']==[[1,len(code.splitlines())]],'full C read span/hash')
    w={};out=[];receipts=[]
    for win in plan['ranges']:
        tag=win['start'][2:];raw=(CAP/(tag+'.bin')).read_bytes();rows=json.loads((CAP/(tag+'.stdout.json')).read_bytes());r=json.loads((CAP/(tag+'.invocation-after.json')).read_bytes())
        need(r['exit_code']==0 and not r['timed_out'] and r['error'] is None and not (CAP/(tag+'.stderr')).read_bytes(),'child status')
        need(len(rows)==win['words'] and len(raw)==win['bytes'],'body bounds')
        for i,row in enumerate(rows):
            pc=int(win['start'],16)+i*4;b=raw[4*i:4*i+4];need(type(row['offset']) is int and row['offset']==pc and type(row['size']) is int and row['size']==4 and row['bytes'].lower()==b.hex(),'row association')
            w[pc]=int.from_bytes(b,'little');out.append({'pc':hex(pc),'raw':b.hex(),'opcode_unchanged':row['opcode']})
        receipts.append({'entry':win['start'],'pid':r['pid'],'exit':0,'stderr_bytes':0,'timeout':False,'cleanup':r['cleanup']})
    regs=field_checks(w);a=json.loads((HERE/'assessment.json').read_bytes());assessment_checks(a,list(w));neg=[]
    for label,pc,value in [('wrong A argument',0xc40c,0xaa0103f3),('wrong outer store',0xbc20,0xf9000280),
                           ('wrong core-return store base',0x4520,0xf9000268),('wrong cast child offset',0x4138,0xf9400000),
                           ('wrong registration receiver',0x3e48,0xaa1403e0),('omit last registration index',0x4108,0x528003e1),
                           ('wrong receiver-container offset',0xc674,w[0xc674]^(1<<5)),
                           ('wrong wrapper slot',0xc2cc,w[0xc2cc]^(1<<10)),('lost field reload',0xc4c0,0xf90002e0),
                           ('malformed printed offset taken literally',0xc404,w[0xc404]^(1<<15))]:
        bad=copy.copy(w);bad[pc]=value
        try:field_checks(bad)
        except ValueError:neg.append(label)
        else:raise ValueError('negative accepted '+label)
    for label,change in [('invent core composition',lambda a:a['conclusions'].__setitem__('core_factory_S_equals_4500_incoming_T','proved')),
                         ('invent registration identity',lambda a:a['conclusions'].__setitem__('registration_R_equals_A_or_O','proved')),
                         ('main-image count contamination',lambda a:a['conclusions'].__setitem__('main_Live_resolved_sites',25103)),
                         ('omit native read group',lambda a:a['whole1563_read_map'].pop())]:
        bad=copy.deepcopy(a);change(bad)
        try:assessment_checks(bad,list(w))
        except ValueError:neg.append(label)
        else:raise ValueError('negative accepted '+label)
    print(json.dumps({'status':'PASS-packet-only','rows':len(out),'code_bytes':6252,'table_bytes':0,'custody_pairs':22,
          'child_receipts':receipts,'all33_registrations':regs,'raw_associations':out,
          'indirect_sites':[{'pc':hex(pc),'selected_eight_scope':pc in SITES,**indirect(word)} for pc,word in w.items() if word&0xfffffc1f in (0xd61f0000,0xd63f0000)],
          'negative_controls_rejected':neg,'external_image_tool_provider_source_index_reopened':False,
          'proof_limit':'Narrow raw fields, not a second complete disassembler, native execution, formal ABI or public binding.'},indent=2))

if __name__=='__main__':main()

