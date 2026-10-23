#!/usr/bin/env python3
"""Finite source/operand checks. Never execute imported/original code or write reports."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
P = Path(__file__).resolve().parent
R = P.parents[3]

def path(n):
    n = Path(n)
    return n if n.is_absolute() else R / n

def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def operands(data, trace):
    # Only retained exact aligned words; this is not a general decoder or interpreter.
    ws = {}
    for r in data['raw_reads']:
        b = bytes.fromhex(r['raw']); a = int(r['vmaddr'], 16)
        assert len(b) == r['bytes'] and len(b) % 4 == 0
        assert hashlib.sha256(b).hexdigest() == r['sha256']
        for i in range(0, len(b), 4):
            assert a + i not in ws
            ws[a+i] = struct.unpack_from('<I', b, i)[0]
    def branch(a, link=True):
        w = ws[a]; assert w >> 26 == (0b100101 if link else 0b000101)
        n = w & 0x3ffffff; n -= (1 << 26) if n & (1 << 25) else 0
        return a + 4*n
    def move(a, d, s): assert ws[a] == 0x1e204000 | (s << 5) | d
    def pair(a, d, e, n, offset, load=False):
        w = ws[a]
        assert w & 0xffc00000 == (0x2d400000 if load else 0x2d000000)
        imm = (w >> 15) & 127; imm -= 128 if imm & 64 else 0
        assert (w & 31, (w >> 10) & 31, (w >> 5) & 31, imm*4) == (d,e,n,offset)
    def adr(a, rd):
        w = ws[a]; assert w & 0x9f00001f == 0x90000000 | rd
        n = (((w >> 5) & 0x7ffff) << 2) | ((w >> 29) & 3)
        n -= 1 << 21 if n & (1 << 20) else 0
        add = ws[a+4]; assert add & 0xffc003ff == 0x91000000 | (rd << 5) | rd
        return (a & ~4095) + (n << 12) + ((add >> 10) & 4095)
    assert len(data['raw_reads']) == 17 and sum(r['bytes'] for r in data['raw_reads']) == 1872
    assert [branch(a) for a in [0x10319278c,0x1031978e8,0x1026f0b84,0x1026f0c2c]] == [0x103197830,0x1026f0b58,0x1026f0bcc,0x10157432c]
    for a,d,s in [(0x103192748,8,0),(0x10319277c,0,8),(0x103197864,8,0),(0x1031978e0,2,8),
                   (0x1026f0c00,8,2),(0x1026f0c04,9,1),(0x1026f0c08,10,0),(0x101574344,8,2),(0x101574394,0,8)]: move(a,d,s)
    assert ws[0x1031978cc] == 0x2f00e400  # MOVI D0,#0, no arithmetic conversion
    w = ws[0x1031978d0]; assert w & 0xffe01fe0 == 0x1e201000 and w & 31 == 1
    imm = (w >> 13) & 255; b6 = (imm >> 6) & 1
    exp = ((1-b6) << 7) | ((31 if b6 else 0) << 2) | ((imm >> 4) & 3)
    assert ((imm >> 7) << 31) | (exp << 23) | ((imm & 15) << 19) == 0x3f800000
    assert ws[0x10319786c] == 0xaa0103f4 and ws[0x1031978d8] == 0xaa1403e0
    assert ws[0x1026f0c14] == 0xf9411800  # LDR X0,[model X0,+230]
    pair(0x101574348,0,1,0,0x80)
    assert ws[0x10157434c] == 0xbd008802  # STR S2,[X0,+88]
    assert branch(0x1015743ac,False) == 0x101568960
    assert ws[0x101568974] == 0xbd005800 and ws[0x10156887c] == 0xbd405800  # same+58, not+88
    assert ws[0x101568880] == 0xd65f03c0
    # Constructed subordinate vptr, exact slots and thunk, not recovered C return types.
    assert adr(0x1026f1b60,8) == 0x1067fb6f8 and ws[0x1026f1b68] == 0xf9000008
    assert struct.pack('<II',ws[0x1067fb908],ws[0x1067fb90c]) == struct.pack('<Q',0x101574608)
    assert struct.pack('<II',ws[0x1067fb900],ws[0x1067fb904]) == struct.pack('<Q',0x10157459c)
    assert branch(0x101574608,False) == 0x10156887c
    assert ws[0x1015745b0] == 0xf9410908 and ws[0x1015745b4] == 0xd63f0100  # getter virtual210 supplies S0
    assert ws[0x1015745b8] == 0xf9403e60  # converter X0=[sub X19,+78]
    pair(0x1015745bc,1,2,19,0x80,True)
    assert ws[0x1015745c4] == 0xf9401501 and ws[0x1015745d0] == 0xd61f0020
    assert struct.pack('<II',ws[0x106680808],ws[0x10668080c]) == struct.pack('<Q',0x1015758bc)
    # Guarded constructor argument lanes and stores; object/global identity stays a predicate.
    assert ws[0x103192788] == 0xd2800006 and ws[0x103197854] == 0xaa0603f9
    assert ws[0x1031978a0] == 0xf100033f and ws[0x1031978a4] == 0x9a990102
    assert ws[0x103197974] == 0x2f00e400 and ws[0x103197978] == 0x1e2e1001
    assert branch(0x10319797c) == 0x101575868
    for a,d,s in [(0x101575884,11,0),(0x101575880,10,1)]: move(a,d,s)
    pair(0x1015758a4,11,10,0,0x28)
    assert adr(0x101575898,8) == 0x1066807e0 and ws[0x1015758a0] == 0xf9000008
    assert ws[0x1026f0bfc] == 0xaa0203e8 and ws[0x1026f0c28] == 0xaa0803e1
    assert ws[0x101574390] == 0xf9003c01  # converter pointer to subordinate+78
    # Three selected caller windows: constant formation and model pointer loads.
    for a,off in [(0x1030e2e6c,0x448),(0x1030e2e90,0x460),(0x1030e2ebc,0x478)]:
        w = ws[a]; assert w & 0xffc003ff == 0xf9400000 | (19 << 5) | 1
        assert ((w >> 10) & 4095)*8 == off
    assert ws[0x1030e2e78] == 0x1e2c1000
    for a,low,high in [(0x1030e2e9c,0xcccd,0x3dcc),(0x1030e2ec8,0x6666,0x3f66)]:
        w,v = ws[a],ws[a+4]; assert w & 0xffe0001f == 0x52800008 and v & 0xffe0001f == 0x72a00008
        assert ((w >> 5) & 65535, (v >> 5) & 65535) == (low,high)
        assert ws[a+8] == 0x1e270100
    assert all(branch(a)==0x103192720 for a in [0x1030e2e8c,0x1030e2eb8,0x1030e2ee4])
    # Finite matching interval branch bypasses ALL interpolation; no formula is executed here.
    pair(0x1015758bc,3,4,0,0x28,True)
    assert ws[0x1015758c0] == 0x1e212060 and ws[0x1015758c4] == 0x1e220480  # FCMP; FCCMP EQ fallback NZCV0
    w = ws[0x1015758c8]; assert w & 0xff00001f == 0x54000000
    imm = (w >> 5) & 0x7ffff; imm -= (1 << 19) if imm & (1 << 18) else 0
    assert 0x1015758c8 + 4*imm == 0x1015758f8
    assert [ws[a] for a in [0x1015758f8,0x1015758fc,0x101575900,0x101575904]] == [0x1e222000,0x1e20cc42,0x1e212000,0x1e224c20]
    assert [((ws[a]>>5)&31,(ws[a]>>16)&31,(ws[a]>>12)&15,ws[a]&31) for a in [0x1015758fc,0x101575904]] == [(2,0,12,2),(1,2,4,0)]
    assert len(trace['claims']) == 6 and all(c['target_grade']=='U' and c['executed'] is False and c['application_expected'] is None and c['application_comparison'] is None for c in trace['claims'])
    assert trace['limits'] == {'application_expected':None,'application_comparison':None,'application_grade':'U','application_executed':False,'requirements_added':0,'cases_added':0,'coverage_credit':0,'emission_join_closed':False,'all_IEEE_identity_claimed':False}
    assert trace['predicates'] == dict.fromkeys(['actual_selected_path_reached','valid_model_subordinate_converter_objects','constructed_vptrs_and_associated_pointer_identity_stable','lower_D8_callee_save_contract_holds','initial_guard_allocation_base_constructor_identity_or_independent_matching_converter_fields','no_intervening_relevant_writes_including_callbacks','finite_ordered_matching_interval_0_1','finite_current_value_in_0_1'], True)
    for c in trace['claims']:
        s=c['source']; f=data['source_records'][s['source_record_index']]
        assert f['entry']==s['entry'] and f['record']['code'][s['code_start']:s['code_end']]==s['text'] and s['text']
        assert all(int(a,16) in ws for a in c['instruction_addresses'])
    return len(ws)

def main():
    if sys.argv[1:] != ['--check']:
        print('Only --check is supported; writes/sealing are refused.',file=sys.stderr); return 1
    manifest=json.loads((P/'manifest.json').read_text()); inputs=json.loads((P/'inputs.json').read_text())
    assert set(manifest['payloads'])=={'README.md','check.py','records.json','trace.json','inputs.json'}
    assert {p.name for p in P.iterdir()}==set(manifest['payloads'])|{'manifest.json'}
    watch=[P/n for n in list(manifest['payloads'])+['manifest.json']]+[path(n) for n in inputs['files']]
    before={str(p):pin(p) for p in watch}
    for n,v in manifest['payloads'].items(): assert pin(P/n)==v,n
    for n,v in inputs['files'].items(): assert pin(path(n))==v,n
    data=json.loads((P/'records.json').read_text()); trace=json.loads((P/'trace.json').read_text())
    assert len(data['source_records'])==10 and len(data['reused_A1_providers'])==5
    # All source text is JSON data; no original module/function/code is imported or called.
    source_cache={n:path(n).read_bytes().splitlines() for n in {r['path'] for r in data['source_records']}}
    for x in data['source_records']:
        b=source_cache[x['path']][x['line']-1]
        assert hashlib.sha256(b).hexdigest()==x['raw_sha256'] and json.loads(b)==x['record']
        assert len(b)==x['raw_line_bytes_excluding_terminator']
        c=x['record']['code'].encode(); assert len(c)==x['record']['code_bytes'] and hashlib.sha256(c).hexdigest()==x['record']['code_sha256']
    function_metadata={x['entry']:x['record'] for x in data['source_records']}
    for ref,index,entry in zip(data['reused_A1_providers'],[29,30,31,35,44],['0x1026f070c','0x1026f0b58','0x1026f0bcc','0x103197830','0x10150b1cc']):
        assert ref['pointer']==f'/functions/{index}' and ref['entry']==entry
        row=json.loads(path(ref['path']).read_text())['functions'][index]; f=row['record']
        assert f['entry']==entry and f['code_sha256']==ref['code_sha256']
        function_metadata[entry]=f
        b=path(row['path']).read_bytes().splitlines()[row['line']-1]
        assert hashlib.sha256(b).hexdigest()==row['raw_line_sha256'] and json.loads(b)==f
    full_bodies=[r for r in data['raw_reads'] if r.get('entry')==r['vmaddr']]
    assert len(full_bodies)==13
    for r in full_bodies:
        f=function_metadata[r['entry']];a=int(r['vmaddr'],16)
        assert f['body_bytes']==r['bytes'] and f['body_ranges']==[[hex(a),hex(a+r['bytes']-1)]]
    assert data['source_records'][7]['record']['warnings']  # pull tail/jumptable export warning retained
    # Fixed file-backed Mach-O mapping and exact selected ranges; never executable mapping.
    image=path(data['image']['path']); assert pin(image)=={k:data['image'][k] for k in ['bytes','sha256']}
    with image.open('rb') as f:
        h=f.read(32); assert h.hex()==data['image']['header']
        magic,cpu,_,_,n,size,_,_=struct.unpack('<8I',h); assert magic==0xfeedfacf and cpu==0x100000c
        b=f.read(size); o=0; segments=[]
        for _ in range(n):
            cmd,sz=struct.unpack_from('<II',b,o); assert sz>=8 and o+sz<=len(b)
            if cmd==0x19:
                name=b[o+8:o+24].split(b'\0')[0].decode();va,vs,fo,fs=struct.unpack_from('<4Q',b,o+24)
                segments.append(dict(name=name,vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs))
            o+=sz
        assert o==len(b) and segments==data['segments']
        for row in data['raw_reads']:
            a=int(row['vmaddr'],16);sg=[s for s in segments if s['vmaddr']<=a and a+row['bytes']<=s['vmaddr']+s['filesize']]; assert len(sg)==1;s=sg[0]
            assert row['fileoff']==s['fileoff']+a-s['vmaddr']; f.seek(row['fileoff']); assert f.read(row['bytes']).hex()==row['raw']
    assert len(data['retained_instruction_rows'])==190
    wordbytes={hex(int(r['vmaddr'],16)+i):r['raw'][i*2:i*2+8] for r in data['raw_reads'] for i in range(0,r['bytes'],4)}
    for x in data['retained_instruction_rows']:
        index=int(x['pointer'].removeprefix('/disassembly/')); assert x['pointer']==f'/disassembly/{index}'
        row=json.loads(path(x['path']).read_text())['disassembly'][index]
        assert row==x['row'] and wordbytes[row['address']]==row['bytes']
    count=operands(data,trace)
    variants=[]
    # Mutate exact native operand words while repairing range hash, so failures test associations.
    for addr,newword in [(0x101568974,0xbd008800),(0x10157434c,0xbd008801),(0x1031978e0,0x1e204122),
                         (0x1015745bc,0x2d510a61),(0x1015758c8,0x54000000),(0x1015758fc,0x1e20dc42),
                         (0x1067fb908,0x0157459c)]:
        q=copy.deepcopy(data)
        row=next(r for r in q['raw_reads'] if int(r['vmaddr'],16)<=addr<int(r['vmaddr'],16)+r['bytes'])
        b=bytearray.fromhex(row['raw']);struct.pack_into('<I',b,addr-int(row['vmaddr'],16),newword);row['raw']=b.hex();row['sha256']=hashlib.sha256(b).hexdigest();variants.append((q,trace))
    for key,value in [('emission_join_closed',True),('all_IEEE_identity_claimed',True),('application_grade','D'),('application_expected',0.5),('coverage_credit',1)]:
        q=copy.deepcopy(trace);q['limits'][key]=value;variants.append((data,q))
    q=copy.deepcopy(trace);q['predicates']['no_intervening_relevant_writes_including_callbacks']=False;variants.append((data,q))
    q=copy.deepcopy(trace);q['claims'][0]['source']['source_record_index']=0;variants.append((data,q))
    for d,t in variants:
        try:operands(d,t)
        except (AssertionError,KeyError,IndexError):pass
        else:raise AssertionError('unsafe mutation accepted')
    assert before=={str(p):pin(p) for p in watch},'watched inputs changed'
    print(json.dumps({'status':'PASS','scope':'conditional source-local value only; no application/emission grade','new_source_records':10,'reused_records':5,'raw_ranges':17,'raw_bytes':1872,'operand_words':count,'dossier_rows':190,'unsafe_variants_rejected':len(variants),'watched_unchanged':len(before)}))
    return 0
if __name__=='__main__':sys.exit(main())
