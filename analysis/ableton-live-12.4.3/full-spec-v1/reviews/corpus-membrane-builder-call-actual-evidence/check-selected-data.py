"""Review only the selected Corpus 12-byte data, never run a decoder/source function."""
from pathlib import Path
import hashlib, json, struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
D=B/'depth-corpus-membrane-builder-call-instructions-r2'
R=B/'reviews/corpus-membrane-builder-call-root-execution'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def ident(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b))
def signed(x,bits):return x-(1<<bits) if x&(1<<(bits-1)) else x
def field(w,pc):
    if w&0xfc000000 in (0x14000000,0x94000000):
        return dict(kind='B' if w&0xfc000000==0x14000000 else 'BL',target=hex(pc+signed(w&0x3ffffff,26)*4))
    if w&0xffe0ffe0==0xaa0003e0:
        return dict(kind='MOV_X',destination=w&31,source=(w>>16)&31)
    raise AssertionError('unselected word '+hex(w))
def main():
    m=load(D/'manifest.json')
    assert sha((D/'manifest.json').read_bytes())=='ece8b0417bc77f406955a3f99618616fdaf5a19d56fb8522f08e7db480551670'
    assert {r['path'] for r in m['files']}=={p.name for p in D.iterdir() if p.name!='manifest.json'}
    for r in m['files']:
        v=ident(D/r['path']);assert (v['bytes'],v['sha256'])==(r['bytes'],r['sha256'])
    ex=load(D/'extraction.json');image=Path(ex['image']['path']);before=ident(image);assert before==ex['image']
    hp=Path(ex['header_map']['path']);hm=ident(hp);assert hm==ex['header_map'];meta=load(hp)
    raw=(D/'call-12.bin').read_bytes();assert len(raw)==12 and sha(raw)==ex['raw_sha256']
    with image.open('rb') as f:
        h=f.read(32);assert h.hex()==meta['header_hex']
        values=struct.unpack('<8I',h);assert list(values)==meta['header_values']
        assert values[0]==0xfeedfacf and values[1]==0x100000c and values[3:6]==(8,15,1704)
        commands=f.read(values[5]);assert commands.hex()==meta['load_commands_hex'] and sha(commands)==meta['load_commands_sha256']
        off=0;segments=[]
        for _ in range(values[4]):
            cmd,n=struct.unpack_from('<II',commands,off);assert n>=8 and n%8==0 and off+n<=len(commands)
            if cmd==0x19:
                name,va,vs,fo,fs,mp,ip,ns,flags=struct.unpack_from('<16sQQQQiiII',commands,off+8)
                assert n==72+ns*80 and fo+fs<=before['bytes']
                segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=flags))
            off+=n
        assert off==len(commands) and segments==meta['segments']
        matches=[s for s in segments if s['vmaddr']<=0x24884 and 0x24890<=s['vmaddr']+min(s['vmsize'],s['filesize'])]
        assert matches==[meta['selected_segment']]
        offset=matches[0]['fileoff']+0x24884-matches[0]['vmaddr'];assert offset==149636==ex['file_offset']
        f.seek(offset);assert f.read(12)==raw
    rows=load(D/'call-12.stdout.json');assert len(rows)==3
    expected=[dict(kind='B',target='0x24ad4'),dict(kind='MOV_X',destination=0,source=20),dict(kind='BL',target='0x25210')]
    fields=[]
    for i,r in enumerate(rows):
        pc=0x24884+4*i;w=struct.unpack_from('<I',raw,4*i)[0]
        assert r['offset']==pc and r['size']==4 and bytes.fromhex(r['bytes'])==raw[4*i:4*i+4]
        v=field(w,pc);assert v==expected[i]
        if 'target' in v:assert r['jump']==int(v['target'],16)
        fields.append(dict(va=hex(pc),word=hex(w),**v))
    assert field(0x17ffffff,0x1000)==dict(kind='B',target='0xffc')
    try:field(0,0)
    except AssertionError:pass
    else:raise AssertionError('unknown word accepted')
    initial=load(D/'before-map.json')['files'];after=load(D/'after-map.json')
    assert len(initial)==24 and initial==after['files'] and after['unchanged']
    outer=load(R/'watch-before.json');assert len(outer)==2290 and outer==load(R/'watch-after.json')
    assert len({r['path'] for r in initial})==24 and len({r['path'] for r in outer})==2290
    status=load(D/'status.json');receipt=load(R/'receipt.json')
    assert status==receipt['collector_status'] and receipt['process_exit']==0 and status['exit']==0 and status['exception'] is None
    assert status['attempted_decoder_children']==1 and status['returned_pid_children']==1
    assert load(D/'returned-pid.json')['pid']==344979 and (D/'call-12.stderr').read_bytes()==b''
    watch=load(Path('/tmp/corpus-membrane-builder-call-actual-watch.json'))
    assert all(ident(Path(r['path']))==r for r in watch)
    assert ident(image)==before and ident(hp)==hm
    print(json.dumps(dict(status='PASS_SELECTED_DATA_ONLY',fields=fields,image_before=before,image_after=ident(image),header_map=hm,raw_sha256=sha(raw),inner_paired=24,outer_paired=2290,reviewer_unchanged=len(watch),reviewer_watch=watch,synthetic_controls=2,no_original_or_decoder_execution=True),indent=2))
if __name__=='__main__':main()
