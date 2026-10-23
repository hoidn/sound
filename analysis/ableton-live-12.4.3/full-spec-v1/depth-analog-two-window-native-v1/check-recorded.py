"""Packet-only integrity and narrow raw ARM field checks; never starts children."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
CAP=HERE/'capture'

def need(v,msg):
    if not v: raise ValueError(msg)

def sx(n,bits):
    return n-(1<<bits) if n&(1<<(bits-1)) else n

def branch(pc,w):
    need(w&0xfc000000==0x94000000,'BL encoding')
    return pc+4*sx(w&0x3ffffff,26)

def adr(pc,w):
    need(w&0x9f000000==0x10000000,'ADR encoding')
    return {'rd':w&31,'target':pc+sx(((w>>5)&0x7ffff)*4+((w>>29)&3),21)}

def mov(w):
    need(w&0xffe0ffe0==0xaa0003e0,'64-bit unshifted ORR/MOV encoding')
    return {'rd':w&31,'rm':(w>>16)&31}

def pair(w):
    need(w&0x3e000000==0x28000000 and w>>30==2,'64-bit GPR pair encoding')
    return {'load':bool((w>>22)&1),'mode':(w>>23)&3,'offset_bytes':8*sx((w>>15)&127,7),
            'rn':(w>>5)&31,'rt':w&31,'rt2':(w>>10)&31}

def memory64(w):
    need(w&0xff800000==0xf9000000,'64-bit unsigned-immediate memory encoding')
    return {'load':bool((w>>22)&1),'offset_bytes':8*((w>>10)&4095),'rn':(w>>5)&31,'rt':w&31}

CALLS={0x1604:0x1774c,0x1670:0x1de3c,0x16ac:0x1de3c,
       0x177b0:0x1b138,0x17804:0x1ac0c,0x17810:0x1b058,0x1781c:0x1b0fc}
ADRS={0x1608:(8,0x580c0),0x1614:(22,0x58188),0x1640:(2,0x5579c),0x1674:(2,0x5579c),
      0x17764:(8,0x59338),0x17770:(8,0x59400),0x17780:(8,0x59460),0x177c0:(8,0x59680)}

def check_fields(words):
    for pc,target in CALLS.items(): need(branch(pc,words[pc])==target,'BL target '+hex(pc))
    for pc,(rd,target) in ADRS.items(): need(adr(pc,words[pc])=={'rd':rd,'target':target},'ADR target '+hex(pc))
    for pc,rd,rm in [(0x15f4,19,0),(0x17760,19,0),(0x17820,0,19),(0x16b0,0,19)]:
        need(mov(words[pc])=={'rd':rd,'rm':rm},'carrier '+hex(pc))
    for start,epilogue in [(0x15e0,0x16b4),(0x1774c,0x17824)]:
        saves=[pair(words[start+4*i]) for i in range(4)]
        loads=[pair(words[epilogue+4*i]) for i in range(4)]
        need(saves==[{'load':False,'mode':3,'offset_bytes':-64,'rn':31,'rt':24,'rt2':23},
                     {'load':False,'mode':2,'offset_bytes':16,'rn':31,'rt':22,'rt2':21},
                     {'load':False,'mode':2,'offset_bytes':32,'rn':31,'rt':20,'rt2':19},
                     {'load':False,'mode':2,'offset_bytes':48,'rn':31,'rt':29,'rt2':30}],'saved pairs')
        need(loads==[{'load':True,'mode':2,'offset_bytes':48,'rn':31,'rt':29,'rt2':30},
                     {'load':True,'mode':2,'offset_bytes':32,'rn':31,'rt':20,'rt2':19},
                     {'load':True,'mode':2,'offset_bytes':16,'rn':31,'rt':22,'rt2':21},
                     {'load':True,'mode':1,'offset_bytes':64,'rn':31,'rt':24,'rt2':23}],'restored pairs')
    need(memory64(words[0x1610])=={'load':False,'offset_bytes':0,'rn':0,'rt':8},'580c0 store through B')
    need(memory64(words[0x17808])=={'load':False,'offset_bytes':0,'rn':23,'rt':0},'helper return store')
    need(memory64(words[0x17814])=={'load':True,'offset_bytes':0,'rn':23,'rt':0},'post-helper reload')
    need(words[0x17834]==words[0x16c4]==0xd65f03c0,'RET X30')
    need(words[0x160c]==0xd503201f,'NOP between ADR and store')
    # Complete prefix to the call: stores/save-frame, FP/X19 setup, W8 constants,
    # X20 derived from incoming X0. None of these words writes X0.
    need([words[0x15e0+4*i] for i in range(10)]==[
        0xa9bc5ff8,0xa90157f6,0xa9024ff4,0xa9037bfd,0x9100c3fd,
        0xaa0003f3,0x52801008,0x72a001c8,0x8b080014,0x94005852], 'whole incoming-X0 prefix')

def main():
    argparse.ArgumentParser().parse_args()
    planraw=(HERE/'pre-call-manifest.json').read_bytes(); plan=json.loads(planraw)
    status=json.loads((CAP/'status.json').read_bytes())
    need(hashlib.sha256(planraw).hexdigest()==status['pre_call_manifest_sha256'],'pre-call identity')
    need(status['error'] is None and status['watch_unchanged'],'successful custody')
    need(status['attempts']==status['children_started']==2,'two children')
    need(status['selected_bytes_read']==status['validated_bytes']==468 and status['validated_words']==117,'whole bounds')
    need(status['native_original_instruction_execution']==0 and status['automatic_retry'] is False,'static no retry')
    before=json.loads((CAP/'before-identities.json').read_bytes())
    after=json.loads((CAP/'after-identities.json').read_bytes())
    need(before==after['files'] and after['unchanged'] is True and len(before)==23,'23 equal custody identities')
    for pin in plan['pins']:
        current=Path(pin['path']).read_bytes()
        need(len(current)==pin['bytes'] and hashlib.sha256(current).hexdigest()==pin['sha256'],'retained doc pin '+pin['path'])
    words={}; associations=[]; receipts=[]
    for win in plan['ranges']:
        tag=win['start'][2:]; raw=(CAP/(tag+'.bin')).read_bytes()
        rows=json.loads((CAP/(tag+'.stdout.json')).read_bytes())
        receipt=json.loads((CAP/(tag+'.invocation-after.json')).read_bytes())
        need(receipt['exit_code']==0 and receipt['timed_out'] is False and receipt['error'] is None,'child status')
        need((CAP/(tag+'.stderr')).read_bytes()==b'','empty stderr')
        need(len(raw)==win['bytes'] and len(rows)==win['words'],'row/raw bounds')
        need(receipt['argv'][-2]=='pdj '+str(win['words']),'fixed word request')
        for i,row in enumerate(rows):
            pc=int(win['start'],16)+4*i; value=raw[i*4:i*4+4]
            need(type(row['offset']) is int and row['offset']==pc and type(row['size']) is int and row['size']==4,'row geometry')
            need(row['bytes'].lower()==value.hex(),'raw row encoding')
            words[pc]=int.from_bytes(value,'little')
            associations.append({'pc':hex(pc),'raw_bytes':value.hex(),'word_little_endian':hex(words[pc]),
                                 'opcode_unchanged':row['opcode'],'type_unchanged':row['type']})
        receipts.append({'pid':receipt['pid'],'exit':receipt['exit_code'],'timeout':receipt['timed_out'],
                         'stderr_bytes':0,'cleanup':receipt['cleanup']})
    check_fields(words)
    assessment=json.loads((HERE/'assessment.json').read_bytes())
    need(assessment['conclusion']['formal_ABI_or_class_identity']=='unknown','no formal ABI/class promotion')
    need(assessment['conclusion']['factory_object_or_actual_Live_instance_identity']=='unknown','no factory/public promotion')
    need(assessment['conclusion']['new_resolved_indirect_sites']==0,'no indirect-site credit')
    need(assessment['conclusion']['P_equals_B'].startswith('conditional'),'conditional relation only')
    need(assessment['no_successor_selected'] is True,'no successor selection')
    read_addresses=[]
    for group in assessment['whole117_read_map']:
        addresses=list(range(int(group['start'],16),int(group['last'],16)+1,4))
        need(len(addresses)==group['words'],'read-map group size')
        read_addresses.extend(addresses)
    need(read_addresses==list(words),'complete117 read map without gap/overlap')
    negatives=[]
    for name,pc,mutated in [('wrong direct target',0x1604,words[0x1604]+1),
                           ('wrong580c0 address',0x1608,words[0x1608]^(1<<5)),
                           ('wrong incoming register',0x15f4,0xaa0103f3),
                           ('wrong returned register',0x17820,0xaa1403e0),
                           ('wrong store base',0x1610,0xf9000028),
                           ('lost post-helper reload',0x17814,0xf90002e0),
                           ('wrong FP/LR offset',0x17758,words[0x17758]^(1<<15)),
                           ('wrong final SP restore',0x17830,words[0x17830]^(1<<15))]:
        bad=copy.copy(words); bad[pc]=mutated
        try: check_fields(bad)
        except ValueError: negatives.append(name)
        else: raise ValueError('accepted control '+name)
    print(json.dumps({'status':'PASS-packet-data-only','rows':117,'raw_bytes':468,'equal_custody_identities':23,
                      'all_row_associations':associations,'child_receipts':receipts,
                      'BL_fields':[{'pc':hex(pc),'target':hex(branch(pc,words[pc]))} for pc in CALLS],
                      'ADR_fields':[{'pc':hex(pc),**{k:(hex(v) if k=='target' else v) for k,v in adr(pc,words[pc]).items()}} for pc in ADRS],
                      'FP_LR_raw_pairs':[{'pc':hex(pc),**pair(words[pc])} for pc in [0x15ec,0x16b4,0x17758,0x17824]],
                      'negative_controls_rejected':negatives,'image_tool_chunk_or_callee_reopened':False,
                      'no_claim':'Field checks are not a complete independent disassembler, ABI/callee conformance proof, native execution or public binding.'},indent=2))

if __name__=='__main__': main()
