"""Fixed combined-source/retained-native checks only; never opens external paths."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CAP=HERE/'capture'

def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def sx(n,b):return n-(1<<b) if n&(1<<(b-1)) else n
def bl(pc,w):
    need(w&0xfc000000==0x94000000,'BLencoding');return pc+4*sx(w&0x3ffffff,26)
def regbranch(w,link):
    need(w&0xfffffc1f==(0xd63f0000 if link else 0xd61f0000),'BR/BLRkind');return (w>>5)&31
def mov(w):
    need(w&0xffe0ffe0==0xaa0003e0,'MOV64');return w&31,(w>>16)&31
def memory(w,load):
    need(w&0xffc00000==(0xf9400000 if load else 0xf9000000),'memory64');return w&31,(w>>5)&31,8*((w>>10)&4095)
def adr(pc,w):
    need(w&0x9f000000==0x10000000,'ADR');return w&31,pc+sx(((w>>5)&0x7ffff)*4+((w>>29)&3),21)
def cbz(pc,w):
    need(w&0xff000000==0xb4000000,'CBZX');return w&31,pc+4*sx((w>>5)&0x7ffff,19)
def pair(w):
    need(w&0x3e000000==0x28000000 and w>>30==2,'pair64');return bool(w&(1<<22)),(w>>23)&3,8*sx((w>>15)&127,7),(w>>5)&31,w&31,(w>>10)&31
def wide(w,kind,shift):
    need(w&0xff800000==(0x52800000 if kind=='z' else 0x72800000),'wide32kind')
    need(((w>>21)&3)*16==shift,'wide32shift');return w&31,(w>>5)&65535
BLS={0x1b94:0x51e48,0x1b9c:0x1e04,0x1ba8:0x51e48,0x1bb0:0x15860,0x1bc8:0x15950,0x1bdc:0x161c0,0x1c3c:0x51ea8,0x1c48:0x161cc}
MOVS={0x1b98:(19,0),0x1bac:(20,0),0x1bc4:(0,20),0x1bd8:(0,20),0x1be0:(0,20),0x1c44:(19,0),0x1c68:(0,19)}
LOADS={0x1c4c:(0,19,8),0x1c54:(8,0,0),0x1c58:(8,8,8),0x1c60:(8,19,0),0x1c64:(1,8,8)}
def fields(w):
    for pc,t in BLS.items():need(bl(pc,w[pc])==t,'BLtarget '+hex(pc))
    for pc,t in MOVS.items():need(mov(w[pc])==t,'carrier '+hex(pc))
    for pc,t in LOADS.items():need(memory(w[pc],True)==t,'reload/slot '+hex(pc))
    need(memory(w[0x1bb4],False)==(19,20,8),'PstoreOplus8')
    need(regbranch(w[0x1c5c],True)==8,'innerBLRX8')
    need(regbranch(w[0x1c74],False)==1,'outertailBRX1')
    need(adr(0x1c28,w[0x1c28])==(1,0x5d6b8) and adr(0x1c30,w[0x1c30])==(2,0x5d630),'castaddressconstants')
    for pc,t in [(0x1c24,(0,0x1c78)),(0x1c40,(0,0x1c78)),(0x1c50,(0,0x1c60))]:need(cbz(pc,w[pc])==t,'nullguard '+hex(pc))
    for low,high,rd,value in [(0x1b8c,0x1b90,0,0xe0130),(0x1ba0,0x1ba4,0,0x48070),(0x1bb8,0x1bbc,8,0x3a83126f),(0x1bcc,0x1bd0,8,0x472c4400)]:
        a,b=wide(w[low],'z',0),wide(w[high],'k',16);need(a[0]==b[0]==rd and (a[1]|b[1]<<16)==value,'literalbits')
    need(w[0x1bc0]==w[0x1bd4]==0x1e270100,'S0bitmoveW8')
    need(w[0x1c38]==0xd2800003,'castX3zero')
    need(w[0x1bf0]==w[0x1c80]==0xd65f03c0,'RET')
    need([pair(w[0x1b7c+4*i]) for i in range(3)]==[(False,3,-48,31,22,21),(False,2,16,31,20,19),(False,2,32,31,29,30)],'constructorframe')
    need([pair(w[0x1be4+4*i]) for i in range(3)]==[(True,2,32,31,29,30),(True,2,16,31,20,19),(True,1,48,31,22,21)],'constructorrestore')
    need([pair(w[0x1c18+4*i]) for i in range(2)]==[(False,3,-32,31,20,19),(False,2,16,31,29,30)],'cleanupframe')
    for s in [0x1c6c,0x1c78]:need([pair(w[s+4*i]) for i in range(2)]==[(True,2,16,31,29,30),(True,1,32,31,20,19)],'cleanuprestore')
    # Calls1e04/15860 have no intervening X0 modification after the saved result.
    need(w[0x1b98]==0xaa0003f3 and w[0x1bac]==0xaa0003f4,'emptyCargsresolvedlocally')

def source(raw,codes,plan,a):
    lines=raw.splitlines(keepends=True);need(len(lines)==2 and len(raw)==1730,'whole2raw')
    for b,rpin in zip(lines,plan['selected_retained_source_records']):
        need(len(b)==rpin['raw_bytes'] and sha(b)==rpin['raw_sha256'],'sourceidentity')
        r=json.loads(b);code=codes[r['entry']]
        need(r['code'].encode()==code and len(code)==r['code_bytes'] and sha(code)==r['code_sha256'],'Cprojection')
        need({k:v for k,v in r.items() if k!='code'}==rpin['metadata'],'allmetadata')
        need(len(code.splitlines())==rpin['C_lines'],'fullClines')
    need(a['selected_source_records']==plan['selected_retained_source_records'],'preserveselectedmetadata')
    need(a['source_signature_mismatches_preserved'] is True,'signaturegaps')
    need(a['source_warnings_preserved']==['/* WARNING: Could not recover jumptable at 0x00001c74. Too many branches */','/* WARNING: Treating indirect jump as call */'],'warnings')
    need(a['constructor_relation']['P_equals_or_distinct_from_O']=='unknown' and a['constructor_relation']['O_current_field8_equals_P']=='unknown' and a['constructor_relation']['actual_allocator_class_success']=='unknown','constructorlimits')
    need(a['cleanup_relation']['D_equals_Q_or_O']=='unknown' and a['cleanup_relation']['I_equals_P']=='unknown' and a['cleanup_relation']['destructor_or_lifetime_semantics']=='unknown','cleanupjoins')
    need(a['newly_resolved_targets']==[] and a['new_indirect_site_case_grade_release_inventory_credit']==0 and a['no_successor_selected'] is True,'noscopepromotion')
    need(a['coverage']=='OPEN-required-unsupported-remains-U' and len(a['claims'])==6,'allclaimsandU')

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);p.parse_args()
    pre=(HERE/'pre-call-manifest.json').read_bytes();plan=json.loads(pre);status=json.loads((CAP/'status.json').read_bytes());before=json.loads((CAP/'before-identities.json').read_bytes());after=json.loads((CAP/'after-identities.json').read_bytes())
    need(sha(pre)==status['pre_call_manifest_sha256'],'precallidentity')
    need(len(before)==14 and before==after['files'] and after['unchanged'] is True,'recordedcustody')
    need(before==[plan['image'],plan['tool'],*plan['pins'],{'path':str(HERE/'pre-call-manifest.json'),'bytes':len(pre),'sha256':sha(pre)}],'declarations')
    for pin in plan['pins']:
        path=Path(pin['path'])
        if path.parent==HERE:
            b=path.read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'ownprecallpin')
    need(status['error'] is None and status['watch_unchanged'] and status['attempts']==status['children_started']==2,'twonormalchildren')
    need(status['selected_bytes_read']==status['validated_bytes']==228 and status['validated_words']==57 and not status['automatic_retry'] and status['native_original_instruction_execution']==0,'exactstaticcapture')
    words={};receipts=[];malformed=[]
    for win in plan['ranges']:
        tag=win['start'][2:];raw=(CAP/(tag+'.bin')).read_bytes();rows=json.loads((CAP/(tag+'.stdout.json')).read_bytes());rec=json.loads((CAP/(tag+'.invocation-after.json')).read_bytes());beg=json.loads((CAP/(tag+'.invocation-before.json')).read_bytes());pid=json.loads((CAP/(tag+'.pid.json')).read_bytes())
        argv=[plan['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',win['start'],'-s',win['start'],'-q','-c','pdj '+str(win['words']),str(CAP/(tag+'.bin'))]
        need(rec['argv']==beg['argv']==pid['argv']==argv and rec['pid']==pid['pid']==pid['pgid'],'argvPID')
        need(rec['exit_code']==0 and not rec['timed_out'] and rec['error'] is None and (CAP/(tag+'.stderr')).read_bytes()==b'','statusstderr')
        need(len(raw)==win['bytes'] and len(rows)==win['words'],'wholewindow')
        for i,r in enumerate(rows):
            pc=int(win['start'],16)+4*i;bb=raw[4*i:4*i+4]
            need(type(r['offset']) is int and r['offset']==pc and type(r['size']) is int and r['size']==4 and bytes.fromhex(r['bytes'])==bb,'everyrowassociation');words[pc]=int.from_bytes(bb,'little')
            if '0lr' in r['opcode']:malformed.append(hex(pc))
        receipts.append({'pid':rec['pid'],'exit':rec['exit_code'],'timeout':rec['timed_out'],'stderr_bytes':0,'cleanup':rec['cleanup']})
    fields(words);a=json.loads((HERE/'assessment.json').read_bytes());raw=(HERE/'records.jsonl').read_bytes();codes={e:(HERE/(e[2:]+'.c')).read_bytes() for e in ['0x1b7c','0x1c18']};source(raw,codes,plan,a)
    pcs=[]
    for g in a['whole57_read_map']:
        rr=list(range(int(g['start'],16),int(g['last'],16)+1,4));need(len(rr)==g['words'],'groupwordcount');pcs+=rr
    need(pcs==list(words),'complete57readmap')
    negatives=[]
    for name,pc,val in [('Pstorewrongbase',0x1bb4,words[0x1bb4]^(1<<5)),('returnedOcarrier',0x1be0,0xaa1303e0),('posthelperinnerreloadlost',0x1c4c,0xf9400260),('inneroffsetwrong',0x1c58,words[0x1c58]^(1<<10)),('tailBRchangedtoBLR',0x1c74,0xd63f0020),('castconstantwrong',0x1c28,words[0x1c28]^(1<<5)),('nullcastbranchwrong',0x1c40,words[0x1c40]^(1<<5)),('frameoffsetwrong',0x1c6c,words[0x1c6c]^(1<<15)),('FPbitmovewrong',0x1bc0,0x1e270120)]:
        bad=words.copy();bad[pc]=val
        try:fields(bad)
        except ValueError:negatives.append(name)
        else:raise ValueError('accepted rawcontrol '+name)
    for name,mut in [('P/Oequalityinvented',lambda z:z['constructor_relation'].__setitem__('P_equals_or_distinct_from_O','distinct')),('staleinnerPjoin',lambda z:z['cleanup_relation'].__setitem__('I_equals_P','proved')),('warningconcealed',lambda z:z['source_warnings_preserved'].pop()),('runtime-targetresolved',lambda z:z['newly_resolved_targets'].append('0x1c74'))]:
        bad=copy.deepcopy(a);mut(bad)
        try:source(raw,codes,plan,bad)
        except ValueError:negatives.append(name)
        else:raise ValueError('accepted scopecontrol '+name)
    print(json.dumps({'status':'PASS-combined-packet-only','source_records':2,'raw_source_bytes':1730,'C_bytes':857,'C_lines':38,'native_bytes':228,'native_rows':57,'recorded_custody_pairs':14,'child_receipts':receipts,'rawBLtargets':[{'pc':hex(pc),'target':hex(bl(pc,words[pc]))} for pc in BLS],'rawBR_BLRevidence':[{'pc':'0x1c5c','kind':'BLR','register':regbranch(words[0x1c5c],True)},{'pc':'0x1c74','kind':'BR','register':regbranch(words[0x1c74],False)}],'rawADRconstants':[{'pc':hex(pc),'rd':adr(pc,words[pc])[0],'target':hex(adr(pc,words[pc])[1])} for pc in [0x1c28,0x1c30]],'pair_instructions_checked':12,'malformed0lr_sites':malformed,'negative_controls_rejected':negatives,'external_source_image_tool_provider_reads':0,'new_original_model_decoder_calls':0,'limit':'Fixedrawfield/sourcechecksare notfullindependentdisassembly,unreadcallee/probeconformance,class/allocator/target/lifetime/publicorDamperlaw.'},indent=2))

if __name__=='__main__':main()
