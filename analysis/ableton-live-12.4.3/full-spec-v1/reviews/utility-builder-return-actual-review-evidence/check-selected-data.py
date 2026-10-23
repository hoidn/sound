"""Independent selected-data checks only. No decoder or source functions execute."""
from pathlib import Path
import hashlib, json, struct

BASE = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
DATA = BASE / 'depth-utility-builder-return-instruction-data'
ROOT = BASE / 'reviews/utility-builder-return-root-execution'
START = 0x101aa80cc

def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text())
def identity(p):
    h = hashlib.sha256(); size = 0
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b); size += len(b)
    return dict(path=str(p), bytes=size, sha256=h.hexdigest())
def signed(n, bits): return n - (1 << bits) if n & (1 << (bits-1)) else n

def operands(w, pc):
    rd, rn, rm = w & 31, (w >> 5) & 31, (w >> 16) & 31
    if w & 0xfc000000 == 0x94000000:
        return dict(kind='BL', target=hex(pc + signed(w & 0x3ffffff, 26)*4), xdefs=[30])
    if w & 0xff800000 == 0x52800000:
        return dict(kind='MOVZ_W', rd=rd, immediate=((w >> 5)&65535) << (16*((w>>21)&3)), xdefs=[rd])
    if w & 0xffe0ffe0 == 0xaa0003e0:
        return dict(kind='MOV_X', rd=rd, source=rm, xdefs=[rd])
    if w & 0xffc00000 == 0x39c00000:
        return dict(kind='LDRSB_W', rd=rd, base=rn, displacement=(w>>10)&4095, xdefs=[rd])
    if w & 0xffc00000 == 0xf9400000:
        return dict(kind='LDR_X', rd=rd, base=rn, displacement=((w>>10)&4095)*8, xdefs=[rd])
    if w & 0xff00001f == 0x7100001f:
        return dict(kind='CMP_W_IMM', source=rn, immediate=((w>>10)&4095) << (12*((w>>22)&1)), xdefs=[])
    if w & 0xffe00c00 == 0x9a800000:
        return dict(kind='CSEL_X', rd=rd, first=rn, second=rm, condition=(w>>12)&15, xdefs=[rd])
    if w & 0xffe00c00 in (0xb8000000, 0xfc000000):
        return dict(kind='STUR_W' if w & 0xffe00c00 == 0xb8000000 else 'STUR_D',
                    source=rd, base=rn, displacement=signed((w>>12)&511,9), xdefs=[])
    if w & 0x9ff80c00 == 0x0f000400:
        q, op, cmode = (w>>30)&1, (w>>29)&1, (w>>12)&15
        imm = (((w>>16)&7)<<5) | ((w>>5)&31)
        assert (q,op,cmode,(w>>11)&1,imm) == (1,1,14,0,255)
        return dict(kind='MOVI_V_2D_ALLONES', vd=rd, xdefs=[])
    if w & 0xffc00000 in (0xa9400000, 0xa8c00000):
        post = w & 0xffc00000 == 0xa8c00000
        rt2 = (w>>10)&31
        return dict(kind='LDP_X_POST' if post else 'LDP_X_OFFSET', first=rd, second=rt2,
                    base=rn, displacement=signed((w>>15)&127,7)*8,
                    xdefs=[rd,rt2] + ([rn] if post else []))
    if w & 0xfffffc1f == 0xd65f0000:
        return dict(kind='RET', target_register=rn, xdefs=[])
    raise AssertionError('Unselected encoding class: '+hex(w))

def main():
    # No destination writes: stdout is retained separately by the reviewer.
    manifest = load(DATA/'manifest.json')
    assert sha((DATA/'manifest.json').read_bytes()) == '1b6ceaf4e295dce15a623ad50acd835074a2bb4f085732c447cc972c79e44a2b'
    assert {r['path'] for r in manifest['files']} == {p.name for p in DATA.iterdir() if p.name != 'manifest.json'}
    for r in manifest['files']:
        v=identity(DATA/r['path']); assert (v['bytes'],v['sha256']) == (r['bytes'],r['sha256'])
    ex=load(DATA/'extraction.json'); raw=(DATA/'helper-tail-96.bin').read_bytes()
    assert len(raw)==96 and sha(raw)==ex['raw_sha256']
    rows=load(DATA/'decoder.stdout.json'); assert len(rows)==24
    assert b''.join(bytes.fromhex(r['bytes']) for r in rows)==raw
    image=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64')
    im_before=identity(image)
    assert (im_before['bytes'],im_before['sha256'])==(149711904,'3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad')
    with image.open('rb') as f:
        header=f.read(32); assert header.hex()==ex['image_header_hex']
        magic,cpu,sub,typ,ncmds,size,flags,res=struct.unpack('<8I',header)
        assert (magic,cpu,typ,ncmds,size,res)==(0xfeedfacf,0x100000c,2,53,6944,0)
        commands=f.read(size); assert sha(commands)==ex['load_commands_sha256']
        off=0; maps=[]
        for _ in range(ncmds):
            cmd,n=struct.unpack_from('<II',commands,off)
            assert n>=8 and n%8==0 and off+n<=size
            if cmd==0x19:
                name,va,vs,fo,fs,mp,ip,ns,sf=struct.unpack_from('<16sQQQQiiII',commands,off+8)
                assert n==72+ns*80 and fo+fs<=im_before['bytes']
                if va<=START and START+96<=va+min(vs,fs):
                    maps.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip))
            off+=n
        assert off==size and maps==[ex['selected_mapping']]
        offset=maps[0]['fileoff']+START-maps[0]['vmaddr']
        assert offset==ex['file_offset']==27951308
        f.seek(offset); assert f.read(96)==raw
    decoded=[]
    for i,row in enumerate(rows):
        pc=START+4*i; w=struct.unpack_from('<I',raw,4*i)[0]
        assert row['offset']==pc and row['size']==4
        assert ex['words'][i]==dict(va=hex(pc),bytes=raw[4*i:4*i+4].hex(),word=hex(w))
        v=operands(w,pc); decoded.append(dict(va=hex(pc),word=hex(w),**v))
        if v['kind']=='BL': assert row['jump']==int(v['target'],16)
    assert decoded[10]==dict(va='0x101aa80f4',word='0xaa1503e0',kind='MOV_X',rd=0,source=21,xdefs=[0])
    assert decoded[12]['target']=='0x1054d70a0'
    assert len(decoded[13:21])==8 and all(0 not in r['xdefs'] for r in decoded[13:21])
    assert decoded[21]['kind']=='RET' and decoded[21]['target_register']==30
    assert [x['kind'] for x in decoded[13:21]]==['STUR_W','MOVI_V_2D_ALLONES','STUR_D']+['LDP_X_OFFSET']*4+['LDP_X_POST']
    assert decoded[13]['source']==19 and decoded[13]['base']==25 and decoded[13]['displacement']==-32
    assert decoded[15]['source']==0 and decoded[15]['base']==25 and decoded[15]['displacement']==-28
    assert operands(0x97ffffff,0x1000)['target']=='0xffc'
    try: operands(0,0)
    except AssertionError: pass
    else: raise AssertionError('unknown encoding accepted')
    inner=load(DATA/'before-map.json'); inner_after=load(DATA/'after-map.json')
    assert len(inner)==12 and inner==inner_after['files'] and inner_after['unchanged']
    assert [json.loads(s) for s in (DATA/'before-identities.jsonl').read_text().splitlines()]==inner
    outer=load(ROOT/'watch-before.json'); assert len(outer)==2182 and outer==load(ROOT/'watch-after.json')
    assert len({r['path'] for r in inner})==12 and len({r['path'] for r in outer})==2182
    status=load(DATA/'status.json'); receipt=load(ROOT/'receipt.json')
    assert receipt['collector_status']==status and status['tool_attempts']==1 and status['tool_returned_pid']==339764 and status['tool_exit']==0 and status['exception'] is None
    assert (DATA/'decoder.stderr').read_bytes()==b'' and receipt['process_exit']==0
    assert im_before==identity(image)
    watch=load(Path('/tmp/utility-builder-return-actual-review-watch.json'))
    assert all(identity(Path(r['path']))==r for r in watch)
    print(json.dumps(dict(status='PASS_SELECTED_DATA_ONLY',rows=decoded,raw_sha256=sha(raw),image_before=im_before,image_after=identity(image),inner_paired=12,outer_paired=2182,reviewer_watch_unchanged=len(watch),synthetic_checks=2,reviewer_watch=watch,original_or_decoder_execution=False),indent=2))

if __name__=='__main__': main()
