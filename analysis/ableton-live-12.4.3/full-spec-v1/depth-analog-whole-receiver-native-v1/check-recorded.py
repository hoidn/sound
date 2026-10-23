"""Retained packet only. No external pin/image/tool/source/index reads or children."""
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
CAP=HERE/'capture'
SITES=[0x17074,0x17624,0x17404,0x17424,0x176bc,0x1a244,0x18768,0x18890,0x188cc]

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

def field_checks(w):
    for pc,target in {0x3a28:0x509f4,0x3a30:0x1760,0x3a3c:0x509f4,0x3a44:0x198dc,
                      0x3a5c:0x199cc,0x3a70:0x1a23c,0x17050:0x3a10}.items():
        need(direct(pc,w[pc])=={'link':True,'target':target},'factory direct '+hex(pc))
    for pc,rd,rm in [(0x3a2c,19,0),(0x3a40,20,0),(0x3a74,0,20),(0x17054,19,0),
                     (0x198e8,19,0),(0x19930,0,19),(0x17328,23,0),(0x173f4,0,23),
                     (0x17414,0,23),(0x1875c,0,20)]:
        need(mov(w[pc])==(rd,rm),'carrier '+hex(pc))
    need(mem(w[0x3a48])=={'load':False,'rt':19,'rn':20,'offset':8},'P stored at O+8')
    need(adr(0x198ec,w[0x198ec])==(8,0x595f8),'O addresspoint595f8')
    # First64-bit lane of STP X8,XZR,[X0] stores595f8 through incoming O.
    need(w[0x198f4]==0xa9007c08,'outer addresspoint pair store')
    patterns=[(0x1705c,8,19,0),(0x17060,8,8,0x68),
              (0x1761c,8,0,0),(0x17620,8,8,0x38),
              (0x173d8,8,23,0),(0x173dc,8,8,0x60),
              (0x1740c,8,23,0),(0x17410,8,8,0x68),
              (0x176b4,8,0,0),(0x176b8,8,8,0x58),
              (0x1a23c,8,0,0),(0x1a240,1,8,0x10),
              (0x18754,8,20,0),(0x18758,8,8,0x90),
              (0x187dc,0,20,8),(0x18830,0,20,8),(0x18858,0,20,8),(0x18894,0,20,8),
              (0x1884c,8,0,0),(0x18850,3,8,0xc8),
              (0x1886c,8,0,0),(0x18870,3,8,0xd8),
              (0x188ac,8,0,0),(0x188b0,4,8,0xd0)]
    for pc,rt,rn,off in patterns:
        need(mem(w[pc])=={'load':True,'rt':rt,'rn':rn,'offset':off},'receiver/slot '+hex(pc))
    for pc,rn,link in [(0x17074,8,True),(0x17624,8,True),(0x17404,8,True),
                       (0x17424,8,True),(0x176bc,8,True),(0x1a244,1,False),
                       (0x18768,8,True),(0x18890,3,False),(0x188cc,4,False),
                       (0x1717c,8,True),(0x172ec,16,True),(0x187d8,10,False)]:
        need(indirect(w[pc])=={'link':link,'rn':rn},'indirect register '+hex(pc))
    need(adr(0x187c4,w[0x187c4])==(9,0x53276),'unread local jump-byte table address')
    need(adr(0x187cc,w[0x187cc])==(10,0x187dc),'local jump base')
    need(w[0x187d0]==0x3868692b and w[0x187d4]==0x8b0b094a,'local byte-index branch expressions')

def assessment_checks(a,addresses):
    c=a['conclusions']
    for key in ['A_equals_prior_P','O_equals_A_or_distinct_allocations','table_runtime_pointer_encoding','actual_Live_public_binding']:
        need(c[key].startswith('unknown'),'no promotion '+key)
    need(c['new_Analog_local_runtime_resolved_sites']==0 and c['main_Live_resolved_sites']==25095
         and c['main_Live_site_universe']==268015 and c['main_Live_baseline']==25071
         and c['main_Live_conditional']==24,'separate images/counts')
    need(a['no_successor_selected'] is True and a['shared_files_changed'] is False,'scope limits')
    read=[]
    for g in a['whole509_read_map']:
        values=list(range(int(g['start'],16),int(g['last'],16)+1,4))
        need(len(values)==g['words'],'read-map word count');read.extend(values)
    need(read==addresses,'complete509 read map without omission/overlap')
    need({int(x['site'],16) for x in a['nine_site_scope']}==set(SITES),'exact nine-site scope')
    need(all(x['target'].startswith('unknown') for x in a['nine_site_scope']),'no runtime target promotion')

def main():
    planraw=(HERE/'pre-call-manifest.json').read_bytes();plan=json.loads(planraw)
    status=json.loads((CAP/'status.json').read_bytes());before=json.loads((CAP/'before-identities.json').read_bytes())
    after=json.loads((CAP/'after-identities.json').read_bytes())
    need(hashlib.sha256(planraw).hexdigest()==status['pre_call_manifest_sha256'],'precall identity')
    need(before==after['files'] and after['unchanged'] and len(before)==21,'recorded21 matching custody identities')
    need(before[:2]==[plan['image'],plan['tool']] and before[2:-1]==plan['pins'],'recorded custody matches declared inputs')
    need(status['error'] is None and status['attempts']==status['children_started']==10,'ten successful attempts')
    need(status['selected_bytes_read']==status['validated_bytes']==2036 and status['selected_table_bytes_read']==40
         and status['validated_words']==509 and status['native_original_instruction_execution']==0,'exact aggregate')
    meta=json.loads((HERE/'selected-metadata.json').read_bytes())
    ranges=[]
    for rec in meta['records']:
        m=rec['metadata'];need(m['error'] is None and not m['timed_out'] and not m['partial_code'] and not m['thunk'],'full metadata status')
        need(sum(int(e,16)+1-int(s,16) for s,e in m['body_ranges'])==m['body_bytes'],'declared range sum')
        for s,e in m['body_ranges']:
            need(int(s,16)%4==0 and (int(e,16)+1)%4==0,'aligned explicit range')
            ranges.append((int(s,16),int(e,16)+1))
    ranges.sort();need(all(a[1]<=b[0] for a,b in zip(ranges,ranges[1:])) and sum(b-a for a,b in ranges)==2036,'whole disjoint2036B')
    w={};rowsout=[];receipts=[]
    for win in plan['ranges']:
        name=win['start'][2:];raw=(CAP/(name+'.bin')).read_bytes();rows=json.loads((CAP/(name+'.stdout.json')).read_bytes())
        rec=json.loads((CAP/(name+'.invocation-after.json')).read_bytes())
        need(rec['exit_code']==0 and not rec['timed_out'] and rec['error'] is None and not (CAP/(name+'.stderr')).read_bytes(),'child status')
        need(len(raw)==win['bytes'] and len(rows)==win['words'],'body bounds')
        for i,row in enumerate(rows):
            pc=int(win['start'],16)+4*i;enc=raw[4*i:4*i+4]
            need(type(row['offset']) is int and row['offset']==pc and type(row['size']) is int and row['size']==4 and row['bytes'].lower()==enc.hex(),'all row encodings')
            w[pc]=int.from_bytes(enc,'little');rowsout.append({'pc':hex(pc),'raw':enc.hex(),'opcode_unchanged':row['opcode']})
        receipts.append({'entry':win['start'],'pid':rec['pid'],'exit':rec['exit_code'],'timeout':rec['timed_out'],'stderr_bytes':0,'cleanup':rec['cleanup']})
    table=json.loads((CAP/'table-words.json').read_bytes());need(len(table['words'])==5,'five words')
    for a,b in zip(table['words'],plan['data_words'],strict=True):
        raw=(CAP/('word-'+b['start'][2:]+'.bin')).read_bytes()
        need(len(raw)==8 and raw.hex()==a['raw_hex'] and hashlib.sha256(raw).hexdigest()==a['sha256'],'raw word association')
        need(all(a[k]==b[k] for k in ('start','file_offset','bytes')),'word scope')
    field_checks(w)
    assessment=json.loads((HERE/'assessment.json').read_bytes())
    assessment_checks(assessment,list(w))
    neg=[]
    for label,pc,value in [('conflate P/O store',0x3a48,0xf9000280),('wrong O addresspoint',0x198ec,w[0x198ec]^(1<<5)),
                           ('wrong wrapper slot',0x17620,w[0x17620]^(1<<10)),('wrong callback receiver level',0x18830,0xf9400280),
                           ('wrong callback slot',0x18850,w[0x18850]^(1<<10)),('wrong tail carrier',0x18890,0xd61f0080),
                           ('wrong factory branch',0x17050,w[0x17050]+1),('wrong jump base',0x187cc,w[0x187cc]^(1<<5))]:
        bad=copy.copy(w);bad[pc]=value
        try:field_checks(bad)
        except ValueError:neg.append(label)
        else:raise ValueError('negative accepted '+label)
    for label,change in [('invent A=priorP',lambda a:a['conclusions'].__setitem__('A_equals_prior_P','proved')),
                         ('invent pointer encoding',lambda a:a['conclusions'].__setitem__('table_runtime_pointer_encoding','proved absolute')),
                         ('mix Analog into main count',lambda a:a['conclusions'].__setitem__('main_Live_resolved_sites',25104)),
                         ('omit complete-read group',lambda a:a['whole509_read_map'].pop())]:
        bad=copy.deepcopy(assessment);change(bad)
        try:assessment_checks(bad,list(w))
        except ValueError:neg.append(label)
        else:raise ValueError('negative accepted '+label)
    print(json.dumps({'status':'PASS-packet-only','rows':len(rowsout),'code_bytes':2036,'raw_data_bytes':40,'custody_pairs':21,
          'child_receipts':receipts,'raw_associations':rowsout,
          'direct_transfers':[{'pc':hex(pc),'link':bool(word>>31),'target':hex(direct(pc,word)['target'])} for pc,word in w.items() if word&0x7c000000==0x14000000],
          'indirect_sites':[{'pc':hex(pc),'selected_nine_scope':pc in SITES,**indirect(word)} for pc,word in w.items() if word&0xfffffc1f in (0xd61f0000,0xd63f0000)],
          'negative_controls_rejected':neg,'external_image_tool_provider_source_index_reopened':False,
          'proof_limit':'Narrow raw fields only; no complete independent disassembler, runtime pointer encoding, formalABI, actual receiver or public outcome proof.'},indent=2))

if __name__=='__main__':main()
