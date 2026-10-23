"""Fixed packet-only integrity and narrow raw ARM fields; never starts children."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
CAP=HERE/'capture'

def need(v,m):
    if not v:raise ValueError(m)
def sx(v,n):return v-(1<<n) if v&(1<<(n-1)) else v
def bl(pc,w):
    need(w&0xfc000000==0x94000000,'BL encoding')
    return pc+4*sx(w&0x3ffffff,26)
def blr(w):
    need(w&0xfffffc1f==0xd63f0000,'BLR encoding')
    return (w>>5)&31
def ldr(w):
    need(w&0xffc00000==0xf9400000,'LDR64unsigned')
    return w&31,(w>>5)&31,8*((w>>10)&4095)
def literal(pc,w):
    need(w&0xff000000==0x58000000,'LDR64literal')
    return w&31,pc+4*sx((w>>5)&0x7ffff,19)
def mov(w):
    need(w&0xffe0ffe0==0xaa0003e0,'MOV64unshifted')
    return w&31,(w>>16)&31
def movz(w,bits):
    need(w&0xffe00000==(0xd2800000 if bits==64 else 0x52800000),'MOVZimmediate')
    return w&31,(w>>5)&65535
def cbz(pc,w):
    need(w&0x7f000000==0x34000000,'CBZencoding')
    return 64 if w>>31 else 32,w&31,pc+4*sx((w>>5)&0x7ffff,19)
def pair(w):
    need(w&0x3e000000==0x28000000 and w>>30==2,'pair64GPR')
    return bool(w&(1<<22)),(w>>23)&3,8*sx((w>>15)&127,7),(w>>5)&31,w&31,(w>>10)&31

BLS={0x12fd4:0x1b7c,0x1302c:0x51fa4,0x13034:0x1c18,0x132b8:0x162ec,0x132d0:0x1577c,0x1347c:0x51fa4,0x13498:0x163a0,0x134dc:0x51ef0,0x135e4:0x51fa4}
BLRS={0x12ff8:8,0x13270:16,0x13388:8,0x133a8:8,0x135a8:8}
LOADS={0x12fe0:(8,19,0),0x12fe4:(8,8,0x68),0x1335c:(8,23,0),0x13360:(8,8,0x60),0x13390:(8,23,0),0x13394:(8,8,0x68),0x135a0:(8,0,0),0x135a4:(8,8,0x38)}
MOVS={0x12fd8:(19,0),0x12fe8:(0,19),0x13000:(0,19),0x13030:(0,19),0x1303c:(0,19),0x13290:(22,7),0x13294:(24,6),0x13298:(25,5),0x1329c:(26,4),0x132a0:(19,3),0x132a4:(20,2),0x132a8:(21,1),0x132ac:(23,0),0x13378:(0,23),0x13380:(5,21),0x13398:(0,23),0x134b4:(0,19)}

def fields(w):
    for pc,t in BLS.items():need(bl(pc,w[pc])==t,'BLtarget '+hex(pc))
    for pc,r in BLRS.items():need(blr(w[pc])==r,'BLRregister '+hex(pc))
    for pc,t in LOADS.items():need(ldr(w[pc])==t,'receiver/slotload '+hex(pc))
    for pc,t in MOVS.items():need(mov(w[pc])==t,'carrierMOV '+hex(pc))
    need(literal(0x1326c,w[0x1326c])==(16,0x5c080),'probe pointer-location only')
    for pc,bits,t in [(0x12fec,32,(1,0x15)),(0x1339c,32,(1,0x14)),(0x12ff0,64,(2,0)),(0x12ff4,64,(3,0)),(0x133a0,64,(2,0)),(0x133a4,64,(3,0)),(0x1337c,64,(2,0)),(0x13384,32,(7,2)),(0x13264,32,(9,0x4080))]:need(movz(w[pc],bits)==t,'immediate '+hex(pc))
    for pc,t in [(0x12fdc,(64,0,0x13000)),(0x12ffc,(32,0,0x13010)),(0x1328c,(64,0,0x13304)),(0x1338c,(64,22,0x133b8)),(0x1359c,(64,0,0x135b8))]:need(cbz(pc,w[pc])==t,'CBZ '+hex(pc))
    # Exact complete setter prefix: no instruction writes X0/X1/S0 before BLR.
    need([w[0x13590+4*i] for i in range(7)]==[0xa9be4ff4,0xa9017bfd,0x910043fd,0xb40000e0,0xf9400008,0xf9401d08,0xd63f0100],'whole nonnullsetterprefix')
    expected_small=[(False,3,-32,31,20,19),(False,2,16,31,29,30)]
    restored_small=[(True,2,16,31,29,30),(True,1,32,31,20,19)]
    for s in [0x12fc8,0x13590]:need([pair(w[s+4*i]) for i in range(2)]==expected_small,'smallframe saves')
    for s in [0x13004,0x13040,0x135ac,0x135ec]:need([pair(w[s+4*i]) for i in range(2)]==restored_small,'smallframe restores')
    saves=[(False,3,-96,31,28,27)]+[(False,2,o,31,a,b) for o,a,b in [(16,26,25),(32,24,23),(48,22,21),(64,20,19),(80,29,30)]]
    restores=[(True,2,o,31,a,b) for o,a,b in [(80,29,30),(64,20,19),(48,22,21),(32,24,23),(16,26,25)]]+[(True,1,96,31,28,27)]
    need([pair(w[0x13248+4*i]) for i in range(6)]==saves,'Calc saves')
    need([pair(w[0x134c0+4*i]) for i in range(6)]==restores,'Calc restores')
    for pc in [0x1300c,0x13048,0x134d8,0x135b4,0x135f4]:need(w[pc]==0xd65f03c0,'RET X30')
    exact={0x13274:0xd14013ff,0x13278:0xd10203ff,0x134b8:0x914013ff,0x134bc:0x910203ff,0x13364:0x910023e9,0x13368:0xf90003e9,0x1336c:0x9100a3e1,0x13370:0xd101a3a3,0x13374:0xd101e3a4,0x13344:0xb9400308,0x13354:0x3cc08300,0x13358:0x3c8103e0,0x133b4:0xb90002c8}
    for pc,v in exact.items():need(w[pc]==v,'critical local/stack/field word '+hex(pc))

def scope(a):
    r=a['result']
    need(r['setter_local_X0_X1_S0_preservation'].startswith('conditional-'),'conditional setter')
    need(r['Calc_entry_to_postprobe_relation']=='conditional-only-if-unread-probe-preserves-X0..X7','probe premise')
    for k in ['named_index63_FP_semantics','formal_ABI_transport_or_public_Live_binding','factory_receiver_class_or_internal_Damper_gating','ungated_DamperVelocity_predicate']:need(r[k]=='unknown','no promotion '+k)
    need(r['new_resolved_indirect_sites']==r['new_cases_grades_releases_inventory']==0,'no credit')
    need(a['no_successor_selected'] is True,'no successor')
    need([(x['site'],x['slot'],x['target']) for x in a['four_receiver_sites']]==[('0x12ff8','0x68','unresolved'),('0x13388','0x60','unresolved'),('0x133a8','0x68','unresolved'),('0x135a8','0x38','unresolved')],'wholefourfrontier')
    need(len(a['claims'])==8,'all8claims')

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);p.parse_args()
    planraw=(HERE/'pre-call-manifest.json').read_bytes();plan=json.loads(planraw)
    status=json.loads((CAP/'status.json').read_bytes());before=json.loads((CAP/'before-identities.json').read_bytes());after=json.loads((CAP/'after-identities.json').read_bytes())
    need(hashlib.sha256(planraw).hexdigest()==status['pre_call_manifest_sha256'],'precall identity')
    need(status['error'] is None and status['watch_unchanged'] and before==after['files'] and after['unchanged'] and len(before)==11,'custody')
    need(before==[plan['image'],plan['tool'],*plan['pins'],{'path':str(HERE/'pre-call-manifest.json'),'bytes':len(planraw),'sha256':hashlib.sha256(planraw).hexdigest()}],'declared custody pins')
    need(status['attempts']==status['children_started']==3 and status['selected_bytes_read']==status['validated_bytes']==900 and status['validated_words']==225,'wholecapture')
    need(status['native_original_instruction_execution']==0 and not status['automatic_retry'],'static/no retry')
    words={};receipts=[];malformed=[]
    for win in plan['ranges']:
        tag=win['start'][2:];raw=(CAP/(tag+'.bin')).read_bytes();rows=json.loads((CAP/(tag+'.stdout.json')).read_bytes())
        pre=json.loads((CAP/(tag+'.invocation-before.json')).read_bytes());rec=json.loads((CAP/(tag+'.invocation-after.json')).read_bytes());pid=json.loads((CAP/(tag+'.pid.json')).read_bytes())
        expected=[plan['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',win['start'],'-s',win['start'],'-q','-c','pdj '+str(win['words']),str(CAP/(tag+'.bin'))]
        need(rec['argv']==pre['argv']==pid['argv']==expected and rec['pid']==pid['pid']==pid['pgid'],'all argv/pid')
        need(rec['exit_code']==0 and not rec['timed_out'] and rec['error'] is None and (CAP/(tag+'.stderr')).read_bytes()==b'','child status')
        need(len(rows)==win['words'] and len(raw)==win['bytes'],'row lengths')
        for i,row in enumerate(rows):
            pc=int(win['start'],16)+4*i;bb=raw[4*i:4*i+4]
            need(type(row['offset']) is int and row['offset']==pc and type(row['size']) is int and row['size']==4 and bytes.fromhex(row['bytes'])==bb,'allrowrawgeometry')
            words[pc]=int.from_bytes(bb,'little')
            if '0lr' in row['opcode']:malformed.append(hex(pc))
        receipts.append({'pid':rec['pid'],'exit':rec['exit_code'],'timeout':rec['timed_out'],'stderr_bytes':0,'cleanup':rec['cleanup']})
    need(len(set(r['pid'] for r in receipts))==3,'threechildren')
    fields(words);a=json.loads((HERE/'assessment.json').read_bytes());scope(a)
    addresses=[]
    for g in a['whole225_read_map']:
        pcs=list(range(int(g['start'],16),int(g['last'],16)+1,4));need(len(pcs)==g['words'],'group words');addresses+=pcs
    need(addresses==list(words),'full225readmap')
    negatives=[]
    for name,pc,val in [('setter slot offset',0x135a4,words[0x135a4]^(1<<10)),('setter incomingX1changed',0x13598,0x52800001),('Calc saved receiver',0x132ac,0xaa0103f7),('query command conflated',0x1339c,0x528002a1),('processing count carrier',0x13380,0xaa1403e5),('stackprobe register',0x13270,0xd63f0100),('FP/LR pair offset',0x1325c,words[0x1325c]^(1<<15)),('stack restore',0x134bc,words[0x134bc]^(1<<10)),('postprobe field source',0x13354,words[0x13354]^(1<<5)),('direct target',0x12fd4,words[0x12fd4]^1)]:
        bad=words.copy();bad[pc]=val
        try:fields(bad)
        except ValueError:negatives.append(name)
        else:raise ValueError('accepted rawnegative '+name)
    for name,mutate in [('probe preservation invented',lambda b:b['result'].__setitem__('Calc_entry_to_postprobe_relation','proved')),('Damper law invented',lambda b:b['result'].__setitem__('ungated_DamperVelocity_predicate','no-effect'))]:
        bad=copy.deepcopy(a);mutate(bad)
        try:scope(bad)
        except ValueError:negatives.append(name)
        else:raise ValueError('accepted scopenegative '+name)
    print(json.dumps({'status':'PASS-packet-only','rows':225,'raw_bytes':900,'equal_recorded_custody_identities':11,'child_receipts':receipts,'raw_BL_fields':[{'pc':hex(pc),'target':hex(bl(pc,words[pc]))} for pc in BLS],'raw_BLR_fields':[{'pc':hex(pc),'register':blr(words[pc])} for pc in BLRS],'raw_receiver_slot_loads':[{'pc':hex(pc),'rd':ldr(words[pc])[0],'rn':ldr(words[pc])[1],'offset_bytes':ldr(words[pc])[2]} for pc in LOADS],'pair_instructions_checked':24,'malformed0lr_sites':malformed,'negative_controls_rejected':negatives,'external_source_image_tool_provider_reads':0,'new_original_model_decoder_calls':0,'limit':'Narrow rawfields not full independentdisassembler/probe-callee-conformance/actualABI/publicorDamperlaw.'},indent=2))

if __name__=='__main__':main()
