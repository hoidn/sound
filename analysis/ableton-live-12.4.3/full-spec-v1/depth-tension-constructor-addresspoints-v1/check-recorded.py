"""Fixed source/native packet checks only; no external paths, decoder or original calls."""
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
def branch(pc,w,link):
    need(w&0xfc000000==(0x94000000 if link else 0x14000000),'B/BLkind');return pc+4*sx(w&0x3ffffff,26)
def mov(w):
    need(w&0xffe0ffe0==0xaa0003e0,'MOV64');return w&31,(w>>16)&31
def adr(pc,w):
    need(w&0x9f000000==0x10000000,'ADR');return w&31,pc+sx(((w>>5)&0x7ffff)*4+((w>>29)&3),21)
def store(w):
    need(w&0xffc00000==0xf9000000,'STR64');return w&31,(w>>5)&31,8*((w>>10)&4095)
def pair(w):
    need(w&0x3e000000==0x28000000 and w>>30==2,'pair64');return bool(w&(1<<22)),(w>>23)&3,8*sx((w>>15)&127,7),(w>>5)&31,w&31,(w>>10)&31
BLS={0x1ca8:0x136d0,0x1d14:0x19db8,0x1d50:0x19db8,0x158b0:0x162ec}
ADRS={0x1cac:(8,0x5c0c0),0x1cb8:(22,0x5c188),0x1ce4:(2,0x59144),0x1d18:(2,0x59144),0x15870:(8,0x5d5c0)}
def fields(w):
    need(branch(0x1e04,w[0x1e04],False)==0x1c84 and w[0x1e04]==0x17ffffa0,'physicalthunkB')
    for pc,t in BLS.items():need(branch(pc,w[pc],True)==t,'BLtarget')
    for pc,t in ADRS.items():need(adr(pc,w[pc])==t,'ADRconstant')
    for pc,t in [(0x1c98,(19,0)),(0x1d54,(0,19)),(0x1586c,(19,0)),(0x158b4,(0,19))]:need(mov(w[pc])==t,'ownincomingreturncarrier')
    need(store(w[0x1cb4])==(8,0,0),'BstoreNOTincomingP')
    need(w[0x1cb0]==0xd503201f,'BstoreNOP')
    need(pair(w[0x15878])==(False,2,0,0,8,31),'Oaddressandfield8zero')
    saves=[(False,3,-64,31,24,23),(False,2,16,31,22,21),(False,2,32,31,20,19),(False,2,48,31,29,30)]
    restores=[(True,2,48,31,29,30),(True,2,32,31,20,19),(True,2,16,31,22,21),(True,1,64,31,24,23)]
    need([pair(w[0x1c84+4*i]) for i in range(4)]==saves,'firstframe')
    need([pair(w[0x1d58+4*i]) for i in range(4)]==restores,'firstrestore')
    need([pair(w[0x15860+4*i]) for i in range(2)]==[(False,3,-32,31,20,19),(False,2,16,31,29,30)],'outerframe')
    need([pair(w[0x158b8+4*i]) for i in range(2)]==[(True,2,16,31,29,30),(True,1,32,31,20,19)],'outerrestore')
    need(w[0x1d68]==w[0x158c0]==0xd65f03c0,'RETX30')
    # Complete first entry-through-call prefix leaves incomingX0 unchanged before unread136d0.
    need([w[0x1c84+4*i] for i in range(10)]==[0xa9bc5ff8,0xa90157f6,0xa9024ff4,0xa9037bfd,0x9100c3fd,0xaa0003f3,0x52801008,0x72a001c8,0x8b080014,0x9400468a],'wholePforwardprefix')
    # Literal helper setup and zero stores, without assigning observable numeric meaning.
    for pc,v in {0x1589c:0x52880808,0x158a0:0x8b080000,0x158a4:0x6f00e400,0x158a8:0x3d900e60,0x158ac:0x52808001}.items():need(w[pc]==v,'outerinteriorhelperword')

def source_scope(raw,codes,plan,a,tm):
    lines=raw.splitlines(keepends=True);need(len(lines)==2 and len(raw)==1760,'whole2source')
    for b,pin in zip(lines,plan['selected_retained_source_records']):
        need(len(b)==pin['raw_bytes'] and sha(b)==pin['raw_sha256'],'rawsourceidentity')
        r=json.loads(b);code=codes[r['entry']]
        need(r['code'].encode()==code and len(code)==r['code_bytes'] and sha(code)==r['code_sha256'] and len(code.splitlines())==pin['C_lines'],'exactC')
        need({k:v for k,v in r.items() if k!='code'}==pin['metadata'],'allmetadata')
        need(r['thunk'] is False and r['error'] is None and r['warnings']==[] and not r['partial_code'] and not r['timed_out'],'metadatastatus')
    need(a['selected_source_records']==plan['selected_retained_source_records'] and a['metadata_signature_mismatches_preserved'] is True,'signature/sourcepreservation')
    need(tm['metadata']['thunk'] is True and tm['metadata']['body_bytes']==4 and tm['metadata']['body_ranges']==[['0x1e04','0x1e07']] and tm['metadata']['code_bytes']==698,'thunkmetadata')
    need(tm['alias']['thunk_target']=='0x1c84' and tm['expanded_C_read_or_retained'] is False and a['expanded_thunk_C_read_or_retained'] is False,'noexpandedthunkC')
    need(a['result']['B_equals_P']=='unknown' and a['result']['literal5c0c0_stored_through']=='returnedB only','P/Bgap')
    need(a['result']['O_current_table_continuity']=='unknown' and a['result']['P_equals_or_distinct_from_O']=='unknown','O/Pgap')
    need(a['result']['actual_runtime_targets_class_ABI_public_binding']=='unknown' and a['result']['index63_internal_Damper_ungated_predicate']=='unknown','named/publicgaps')
    need(a['newly_resolved_runtime_targets']==[] and a['new_site_case_grade_release_inventory_credit']==a['new_original_model_harness_calls']==0,'nocredit')
    need(a['no_successor_selected'] is True and len(a['claims'])==7,'wholescope')
    need(a['unread_direct_targets']==['0x136d0','0x19db8','0x162ec'],'unreadcallees')

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);p.parse_args()
    pre=(HERE/'pre-call-manifest.json').read_bytes();plan=json.loads(pre);status=json.loads((CAP/'status.json').read_bytes());before=json.loads((CAP/'before-identities.json').read_bytes());after=json.loads((CAP/'after-identities.json').read_bytes())
    need(sha(pre)==status['pre_call_manifest_sha256'],'precallidentity')
    need(len(before)==16 and before==after['files'] and after['unchanged'] is True,'16custodypairs')
    need(before==[plan['image'],plan['tool'],*plan['pins'],{'path':str(HERE/'pre-call-manifest.json'),'bytes':len(pre),'sha256':sha(pre)}],'pinjoins')
    for pin in plan['pins']:
        path=Path(pin['path'])
        if path.parent==HERE:
            b=path.read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'ownfrozenpin')
    need(status['error'] is None and status['watch_unchanged'] and status['attempts']==status['children_started']==3 and not status['automatic_retry'],'threenormalchildren')
    need(status['selected_bytes_read']==status['validated_bytes']==336 and status['validated_words']==84 and status['native_original_instruction_execution']==0,'exactstaticbounds')
    words={};receipts=[];malformed=[]
    for win in plan['ranges']:
        tag=win['start'][2:];raw=(CAP/(tag+'.bin')).read_bytes();rows=json.loads((CAP/(tag+'.stdout.json')).read_bytes());rec=json.loads((CAP/(tag+'.invocation-after.json')).read_bytes());beg=json.loads((CAP/(tag+'.invocation-before.json')).read_bytes());pid=json.loads((CAP/(tag+'.pid.json')).read_bytes())
        argv=[plan['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',win['start'],'-s',win['start'],'-q','-c','pdj '+str(win['words']),str(CAP/(tag+'.bin'))]
        need(rec['argv']==beg['argv']==pid['argv']==argv and rec['pid']==pid['pid']==pid['pgid'],'argvpid')
        need(rec['exit_code']==0 and not rec['timed_out'] and rec['error'] is None and (CAP/(tag+'.stderr')).read_bytes()==b'','childstatus')
        need(len(raw)==win['bytes'] and len(rows)==win['words'],'wholewindow')
        for i,r in enumerate(rows):
            pc=int(win['start'],16)+4*i;bb=raw[4*i:4*i+4]
            need(type(r['offset']) is int and r['offset']==pc and type(r['size']) is int and r['size']==4 and bytes.fromhex(r['bytes'])==bb,'allrowassociations');words[pc]=int.from_bytes(bb,'little')
            if '0lr' in r['opcode']:malformed.append(hex(pc))
        receipts.append({'pid':rec['pid'],'exit':rec['exit_code'],'timeout':rec['timed_out'],'stderr_bytes':0,'cleanup':rec['cleanup']})
    fields(words);raw=(HERE/'records.jsonl').read_bytes();codes={e:(HERE/(e[2:]+'.c')).read_bytes() for e in ['0x1c84','0x15860']};a=json.loads((HERE/'assessment.json').read_bytes());tm=json.loads((HERE/'thunk-metadata.json').read_bytes());source_scope(raw,codes,plan,a,tm)
    pcs=[]
    for g in a['whole84_read_map']:
        r=list(range(int(g['start'],16),int(g['last'],16)+1,4));need(len(r)==g['words'],'groupsize');pcs+=r
    need(pcs==list(words),'whole84readmap')
    negatives=[]
    for name,pc,v in [('thunkchangedtoBL',0x1e04,0x97ffffa0),('wrongthunktarget',0x1e04,words[0x1e04]^1),('BstoremisboundtoP',0x1cb4,0xf9000268),('outerfield8notzero',0x15878,words[0x15878]^(1<<10)),('wrong5d5c0constant',0x15870,words[0x15870]^(1<<5)),('wrongPreturncarrier',0x1d54,0xaa1403e0),('malformedFPoffsetmisread',0x1c90,words[0x1c90]^(1<<15)),('interiorhelperwrongbase',0x158a0,words[0x158a0]^(1<<5))]:
        bad=words.copy();bad[pc]=v
        try:fields(bad)
        except ValueError:negatives.append(name)
        else:raise ValueError('acceptedrawnegative '+name)
    for name,mut in [('B=Pinvented',lambda z:z['result'].__setitem__('B_equals_P','proved')),('currentOtableinvented',lambda z:z['result'].__setitem__('O_current_table_continuity','proved')),('Damperlawinvented',lambda z:z['result'].__setitem__('index63_internal_Damper_ungated_predicate','no-effect')),('expandedthunkCretained',lambda z:z.__setitem__('expanded_thunk_C_read_or_retained',True)),('missingcalleequalification',lambda z:z['unread_direct_targets'].pop())]:
        bad=copy.deepcopy(a);mut(bad)
        try:source_scope(raw,codes,plan,bad,tm)
        except ValueError:negatives.append(name)
        else:raise ValueError('acceptedscopecontrol '+name)
    print(json.dumps({'status':'PASS-combined-packet-only','C_records':2,'raw_source_bytes':1760,'C_bytes':1021,'C_lines':37,'native_bytes':336,'native_rows':84,'recorded_custody_pairs':16,'child_receipts':receipts,'raw_thunk':{'pc':'0x1e04','target':hex(branch(0x1e04,words[0x1e04],False)),'word':hex(words[0x1e04]),'writes_LR_or_argument_registers':False},'rawBLtargets':[{'pc':hex(pc),'target':hex(branch(pc,words[pc],True))} for pc in BLS],'rawADRconstants':[{'pc':hex(pc),'rd':adr(pc,words[pc])[0],'target':hex(adr(pc,words[pc])[1])} for pc in ADRS],'frame_pair_instructions':12,'outer_data_pair_checked':True,'malformed0lr_sites_retained':malformed,'negative_controls_rejected':negatives,'external_image_tool_source_provider_reads':0,'new_original_model_decoder_calls':0,'limit':'Narrowfields are not fullindependentdisassembly or unreadcallee/class/ABI/public/namedDamperproof.'},indent=2))

if __name__=='__main__':main()
