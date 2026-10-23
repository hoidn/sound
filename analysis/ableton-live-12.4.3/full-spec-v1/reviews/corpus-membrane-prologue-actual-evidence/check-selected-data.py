"""Independent selected-data/register checks; no source/decoder/native execution."""
from pathlib import Path
import hashlib, json, struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
D=B/'depth-corpus-membrane-builder-prologue-instructions'
R=B/'reviews/corpus-membrane-builder-prologue-root-execution'
START=0x243e8
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def ident(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b))
def signed(v,n):return v-(1<<n) if v&(1<<(n-1)) else v
def fields(w,pc):
    rd,rn,rm=w&31,(w>>5)&31,(w>>16)&31
    if w&0xffc00000 in (0xa9000000,0xa9800000):
        pre=w&0xffc00000==0xa9800000
        return dict(kind='STP_PRE' if pre else 'STP',first=rd,second=(w>>10)&31,base=rn,offset=signed((w>>15)&127,7)*8,defs=[rn] if pre else [])
    if w&0xff000000 in (0x91000000,0xd1000000):
        return dict(kind='ADD_IMM' if w&0xff000000==0x91000000 else 'SUB_IMM',rd=rd,rn=rn,immediate=((w>>10)&4095)<<(12*((w>>22)&1)),defs=[rd])
    if w&0xffe0ffe0 in (0xaa0003e0,0x2a0003e0):
        return dict(kind='MOV_X' if w&0x80000000 else 'MOV_W',rd=rd,source=rm,defs=[rd])
    if w==0xd503201f:return dict(kind='NOP',defs=[])
    if w&0xff000000==0x58000000:
        return dict(kind='LDR_X_LITERAL',rd=rd,address=hex(pc+signed((w>>5)&0x7ffff,19)*4),defs=[rd])
    if w&0xffc00000 in (0xf9400000,0xb9800000):
        isx=w&0xffc00000==0xf9400000
        return dict(kind='LDR_X' if isx else 'LDRSW_X',rd=rd,base=rn,offset=((w>>10)&4095)*(8 if isx else 4),defs=[rd])
    if w&0xffe00c00==0xf8000000:
        return dict(kind='STUR_X',source=rd,base=rn,offset=signed((w>>12)&511,9),defs=[])
    if w&0xff00001f==0x7100001f:
        return dict(kind='CMP_W',source=rn,immediate=((w>>10)&4095)<<(12*((w>>22)&1)),defs=[])
    if w&0xff000010==0x54000000:
        return dict(kind='B_COND',condition=w&15,target=hex(pc+signed((w>>5)&0x7ffff,19)*4),defs=[])
    if w&0x9f000000==0x10000000:
        imm=(((w>>5)&0x7ffff)<<2)|((w>>29)&3)
        return dict(kind='ADR',rd=rd,address=hex(pc+signed(imm,21)),defs=[rd])
    if w&0xffe00c00 in (0xb8600800,0xbc600800,0x78600800):
        tag={0xb8600800:'LDR_W_REG',0xbc600800:'LDR_S_REG',0x78600800:'LDR_H_REG'}[w&0xffe00c00]
        return dict(kind=tag,rd=rd,base=rn,index=rm,option=(w>>13)&7,scale_bit=(w>>12)&1,defs=[] if tag=='LDR_S_REG' else [rd])
    if w&0xfc000000==0x14000000:
        return dict(kind='B',target=hex(pc+signed(w&0x3ffffff,26)*4),defs=[])
    if w&0xff800000 in (0x52800000,0x72800000):
        return dict(kind='MOVZ_W' if w&0xff800000==0x52800000 else 'MOVK_W',rd=rd,imm16=(w>>5)&65535,shift=16*((w>>21)&3),defs=[rd])
    if w&0xfffffc00==0x5e21d800:
        return dict(kind='SCVTF_SIMD_S',sd=rd,sn=rn,defs=[])
    if w&0xfffffc00==0x1e380000:
        return dict(kind='FCVTZS_W_S',rd=rd,sn=rn,defs=[rd])
    if w&0xff200000==0x8b000000:
        return dict(kind='ADD_SHIFT_X',rd=rd,rn=rn,rm=rm,shift=(w>>22)&3,amount=(w>>10)&63,defs=[rd])
    if w&0xfffffc1f==0xd61f0000:
        return dict(kind='BR',target_register=rn,defs=[])
    raise AssertionError('unselected encoding '+hex(w))
def main():
    m=load(D/'manifest.json')
    assert sha((D/'manifest.json').read_bytes())=='cb9c02ab4d64f3356f3bfa998c0ba76b51fc9a31b54bcc94300c470f086d5008'
    assert {r['path'] for r in m['files']}=={p.name for p in D.iterdir() if p.name!='manifest.json'}
    for r in m['files']:
        v=ident(D/r['path']);assert (v['bytes'],v['sha256'])==(r['bytes'],r['sha256'])
    ex=load(D/'extraction.json');im=Path(ex['image']['path']);initial=ident(im);assert initial==ex['image']
    hp=Path(ex['header_map']['path']);hm=ident(hp);assert hm==ex['header_map'];meta=load(hp)
    raw=(D/'prologue-148.bin').read_bytes();assert len(raw)==148 and sha(raw)==ex['raw_sha256']
    with im.open('rb') as f:
        h=f.read(32);assert h.hex()==meta['header_hex']
        v=struct.unpack('<8I',h);assert list(v)==meta['header_values'] and v[0]==0xfeedfacf and v[1]==0x100000c and v[3:6]==(8,15,1704)
        commands=f.read(v[5]);assert commands.hex()==meta['load_commands_hex'] and sha(commands)==meta['load_commands_sha256']
        off=0;segments=[]
        for _ in range(v[4]):
            cmd,n=struct.unpack_from('<II',commands,off);assert n>=8 and n%8==0 and off+n<=len(commands)
            if cmd==0x19:
                name,va,vs,fo,fs,mp,ip,ns,flags=struct.unpack_from('<16sQQQQiiII',commands,off+8)
                assert n==72+80*ns and fo+fs<=initial['bytes']
                segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=flags))
            off+=n
        assert off==len(commands) and segments==meta['segments']
        maps=[s for s in segments if s['vmaddr']<=START and START+148<=s['vmaddr']+min(s['vmsize'],s['filesize'])]
        assert maps==[meta['selected_segment']]
        offset=maps[0]['fileoff']+START-maps[0]['vmaddr'];assert offset==148456==ex['file_offset']
        f.seek(offset);assert f.read(148)==raw
    rows=load(D/'prologue-148.stdout.json');assert len(rows)==37
    decoded=[]
    for i,r in enumerate(rows):
        pc=START+i*4;w=struct.unpack_from('<I',raw,i*4)[0]
        assert r['offset']==pc and r['size']==4 and bytes.fromhex(r['bytes'])==raw[i*4:i*4+4]
        x=fields(w,pc)
        if 'target' in x:assert r['jump']==int(x['target'],16)
        decoded.append(dict(va=hex(pc),word=hex(w),**x))
    z={int(x['va'],16):x for x in decoded}
    assert (z[0x2440c]['rd'],z[0x2440c]['source'])==(19,0)
    assert (z[0x24420]['rd'],z[0x24420]['rn'],z[0x24420]['immediate'])==(20,0,0x148)
    assert all(0 not in x['defs'] for x in decoded)
    assert (z[0x24424]['kind'],z[0x24424]['rd'],z[0x24424]['base'],z[0x24424]['offset'])==('LDRSW_X',8,0,0x160)
    assert (z[0x24428]['source'],z[0x24428]['immediate'])==(8,3)
    assert (z[0x2442c]['condition'],z[0x2442c]['target'])==(8,'0x24440')
    assert (z[0x24430]['rd'],z[0x24430]['address'])==(9,'0x2ab90')
    assert (z[0x24438]['rd'],z[0x24438]['base'],z[0x24438]['index'],z[0x24438]['option'],z[0x24438]['scale_bit'])==(1,9,8,3,1)
    assert z[0x2443c]['target']=='0x24444'
    assert (z[0x24440]['rd'],z[0x24440]['imm16'],z[0x24440]['shift'])==(1,30,0)
    assert (z[0x24444]['rd'],z[0x24444]['source'])==(23,1)
    assert all(1 not in x['defs'] and 20 not in x['defs'] for x in decoded[23:])
    assert not any((struct.unpack_from('<I',raw,i)[0]&0xfc000000)==0x94000000 for i in range(0,148,4))
    assert z[0x24478]['kind']=='BR' and z[0x24478]['target_register']==10
    inner=load(D/'before-map.json')['files'];a=load(D/'after-map.json');assert len(inner)==27 and inner==a['files'] and a['unchanged']
    outer=load(R/'before-map.json')['files'];a=load(R/'after-map.json');assert len(outer)==2209 and outer==a['files'] and a['unchanged']
    assert len({r['path'] for r in inner})==27 and len({r['path'] for r in outer})==2209
    status=load(D/'status.json');receipt=load(R/'receipt.json');assert status['exit']==0 and status['exception'] is None and receipt['exit']==0 and receipt['unchanged']
    assert status['attempted_decoder_children']==status['returned_pid_children']==1 and (D/'prologue-148.stderr').read_bytes()==b''
    watch=load(Path('/tmp/corpus-membrane-prologue-actual-watch.json'));assert all(ident(Path(r['path']))==r for r in watch)
    assert ident(im)==initial and ident(hp)==hm
    print(json.dumps(dict(status='PASS_SELECTED_DATA_ONLY',decoded=decoded,image_before=initial,image_after=ident(im),header_map=hm,raw_sha256=sha(raw),inner_paired=27,outer_paired=2209,reviewer_unchanged=len(watch),reviewer_watch=watch,no_decoder_or_original_execution=True),indent=2))
if __name__=='__main__':main()
