"""New stdlib checks of the selected 32 bytes only. No decoder/native execution."""
from pathlib import Path
import hashlib, json, struct
BASE=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
DATA=BASE/'depth-utility-builder-entry-origin-instruction-data'
ROOT=BASE/'reviews/utility-builder-entry-origin-root-execution'
START=0x101aa80ac
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text())
def ident(p):
    h=hashlib.sha256(); n=0
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b); n+=len(b)
    return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def signed(v,n): return v-(1<<n) if v&(1<<(n-1)) else v
def operands(w,pc):
    rd,rn,rm=w&31,(w>>5)&31,(w>>16)&31
    if w&0xffc00000==0xf9000000:
        return dict(kind='STR_X',source=rd,base=rn,displacement=((w>>10)&4095)*8)
    if w&0xff000000==0xb4000000:
        return dict(kind='CBZ_X',source=rd,target=hex(pc+signed((w>>5)&0x7ffff,19)*4))
    if w&0xffe0ffe0==0xaa0003e0:
        return dict(kind='MOV_X',destination=rd,source=rm)
    if w&0xfc000000==0x94000000:
        return dict(kind='BL',target=hex(pc+signed(w&0x3ffffff,26)*4))
    if w&0xff000000==0xd1000000:
        return dict(kind='SUB_X_IMM',destination=rd,source=rn,immediate=((w>>10)&4095)<<(12*((w>>22)&1)))
    if w&0xff800000==0x52800000:
        return dict(kind='MOVZ_W',destination=rd,immediate=((w>>5)&65535)<<(16*((w>>21)&3)))
    raise AssertionError('unselected encoding '+hex(w))
def main():
    manifest=load(DATA/'manifest.json')
    assert sha((DATA/'manifest.json').read_bytes())=='9fc13ddbf26fb4ffc919d8e1ca25ebfdd1af1d1b12d42c0d0c551380cd81eb26'
    assert {r['path'] for r in manifest['files']}=={p.name for p in DATA.iterdir() if p.name!='manifest.json'}
    for r in manifest['files']:
        v=ident(DATA/r['path']);assert (v['bytes'],v['sha256'])==(r['bytes'],r['sha256'])
    ex=load(DATA/'extraction.json'); raw=(DATA/'helper-preceding-32.bin').read_bytes()
    rows=load(DATA/'decoder.stdout.json')
    assert len(raw)==32 and sha(raw)==ex['raw_sha256'] and len(rows)==8
    image=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64')
    initial=ident(image); assert (initial['bytes'],initial['sha256'])==(149711904,'3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad')
    with image.open('rb') as f:
        header=f.read(32);assert header.hex()==ex['image_header_hex']
        magic,cpu,sub,typ,ncmds,size,flags,res=struct.unpack('<8I',header)
        assert (magic,cpu,typ,ncmds,size,res)==(0xfeedfacf,0x100000c,2,53,6944,0)
        commands=f.read(size);assert sha(commands)==ex['load_commands_sha256']
        off=0;maps=[]
        for _ in range(ncmds):
            cmd,n=struct.unpack_from('<II',commands,off);assert n>=8 and n%8==0 and off+n<=size
            if cmd==0x19:
                name,va,vs,fo,fs,mp,ip,ns,sf=struct.unpack_from('<16sQQQQiiII',commands,off+8)
                assert n==72+80*ns and fo+fs<=initial['bytes']
                if va<=START and START+32<=va+min(vs,fs):
                    maps.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip))
            off+=n
        assert off==size and maps==[ex['selected_mapping']]
        offset=maps[0]['fileoff']+START-maps[0]['vmaddr'];assert offset==ex['file_offset']==27951276
        f.seek(offset);assert f.read(32)==raw
    expected=[dict(kind='STR_X',source=26,base=21,displacement=0x2b8),dict(kind='CBZ_X',source=22,target='0x101aa80bc'),dict(kind='MOV_X',destination=0,source=22),dict(kind='BL',target='0x1054d5510'),dict(kind='STR_X',source=25,base=21,displacement=0x2b0),dict(kind='SUB_X_IMM',destination=21,source=25,immediate=0x120),dict(kind='MOV_X',destination=0,source=21),dict(kind='MOVZ_W',destination=1,immediate=0xff)]
    fields=[]
    for i,row in enumerate(rows):
        pc=START+i*4;word=struct.unpack_from('<I',raw,i*4)[0]
        assert row['offset']==pc and row['size']==4 and bytes.fromhex(row['bytes'])==raw[i*4:i*4+4]
        assert ex['words'][i]==dict(va=hex(pc),bytes=raw[i*4:i*4+4].hex(),word=hex(word))
        d=operands(word,pc);assert d==expected[i]
        if 'target' in d:assert row['jump']==int(d['target'],16)
        fields.append(dict(va=hex(pc),word=hex(word),**d))
    assert operands(0x97ffffff,0x1000)['target']=='0xffc'
    try:operands(0,0)
    except AssertionError:pass
    else:raise AssertionError('unknown encoding accepted')
    inner=load(DATA/'before-map.json');inner_after=load(DATA/'after-map.json')
    outer=load(ROOT/'watch-before.json')
    assert len(inner)==12 and inner==inner_after['files'] and inner_after['unchanged']
    assert [json.loads(s) for s in (DATA/'before-identities.jsonl').read_text().splitlines()]==inner
    assert len(outer)==2193 and outer==load(ROOT/'watch-after.json')
    assert len({x['path'] for x in inner})==12 and len({x['path'] for x in outer})==2193
    status=load(DATA/'status.json');receipt=load(ROOT/'receipt.json')
    assert receipt['collector_status']==status and receipt['process_exit']==0
    assert status['tool_attempts']==1 and status['tool_returned_pid']==341290 and status['tool_exit']==0 and status['exception'] is None
    assert (DATA/'decoder.stderr').read_bytes()==b''
    watch=load(Path('/tmp/utility-builder-entry-origin-actual-watch.json'))
    assert all(ident(Path(x['path']))==x for x in watch) and ident(image)==initial
    print(json.dumps(dict(status='PASS_SELECTED_DATA_ONLY',fields=fields,image_before=initial,image_after=ident(image),raw_sha256=sha(raw),inner_paired=12,outer_paired=2193,synthetic_controls=2,reviewer_unchanged=len(watch),reviewer_watch=watch,decoder_or_original_executed=False),indent=2))
if __name__=='__main__':main()
