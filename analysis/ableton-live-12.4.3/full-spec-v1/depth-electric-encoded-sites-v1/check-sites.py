#!/usr/bin/env python3
"""Image-free synthetic controls; owned result checks use writable temp only."""
import json
from pathlib import Path
import runpy
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
m = runpy.run_path(str(HERE/'extract-sites.py'), run_name='inert_owned_extractor')
decode, associate, leb = m['decode'], m['associate'], m['leb']
segs = [{'index':0,'name':'test','vmaddr':0,'vmsize':256,'fileoff':0,'filesize':256}]

def synthetic():
    passed = []
    def complete(name, raw, mode, expected):
        r = decode(bytes.fromhex(raw),mode,segs)
        assert r['classic_pointer_site_decode_complete'], (name,r['failure'])
        sites = [run['segment_offset']+i*run['stride'] for run in r['runs'] for i in range(run['count'])]
        assert sites == expected, (name,sites)
        passed.append(name)
        return r
    def unknown(name, raw, mode='rebase'):
        r = decode(bytes.fromhex(raw),mode,segs)
        assert not r['classic_pointer_site_decode_complete'] and not r['absence_claim_allowed'], name
        assert r['failure']['opcode_offset'] >= 0
        passed.append(name)
    complete('all rebase classic transitions','11 20 00 30 08 41 51 60 02 70 08 80 02 08 00','rebase',[16,24,32,40,56,72])
    b = complete('all bind classic transitions and encoded operands','11 20 81 01 3f 40 78 00 51 60 7f 70 00 80 08 90 a0 08 b1 c0 02 08 00','bind',[8,16,32,48,64])
    assert b['runs'][0]['encoded_binding']['addend'] == -1
    assert b['runs'][0]['encoded_binding']['ordinal']['raw_immediate'] == 15
    complete('weak known flags','48 78 00 70 00 90 00','weak_bind',[0])
    complete('lazy explicit records and implicit local pointer default','70 00 40 61 00 90 00 70 08 40 62 00 90 00','lazy_bind',[0,8])
    complete('last valid 8B write','11 20 f8 01 51 00','rebase',[248])
    complete('zero repeat no write','11 20 00 60 00 00','rebase',[])
    complete('terminal zero padding','11 20 00 51 00 00 00','rebase',[0])
    complete('empty stream','', 'weak_bind',[])
    unknown('missing rebase type','20 00 51 00')
    unknown('missing segment','11 51 00')
    unknown('bad segment index','11 24 00 51 00')
    unknown('write crosses vmsize','11 20 f9 01 51 00')
    unknown('nonpointer rebase type','12 00')
    unknown('nonpointer bind type','52 00','bind')
    unknown('threaded opcode','d0 00','bind')
    unknown('unknown opcode','f0 00','bind')
    unknown('reserved immediate','11 20 00 31 00 00')
    unknown('missing terminal DONE','11 20 00 51')
    unknown('nonzero after DONE','00 11')
    unknown('nonzero DONE immediate','01')
    unknown('truncated ULEB','11 20 80')
    unknown('too long ULEB','11 20 '+'80 '*10+'00')
    unknown('unsigned overflow','11 20 '+'ff '*9+'02 00')
    unknown('signed overflow','60 '+'ff '*9+'01 00','bind')
    unknown('truncated SLEB','60 80','bind')
    unknown('missing symbol','70 00 90 00','bind')
    unknown('unterminated symbol','40 78','bind')
    unknown('unknown symbol flags','42 78 00 00','bind')
    unknown('repeat multiplication overflow','11 20 00 80 '+'ff '*9+'01 01 00')
    unknown('lazy inherited segment ambiguous','70 00 40 61 00 90 00 40 62 00 90 00','lazy_bind')
    unknown('lazy inherited addend ambiguous','60 7f 70 00 40 61 00 90 00 70 08 40 62 00 90 00','lazy_bind')
    complete('lazy addend reestablished','60 7f 70 00 40 61 00 90 00 60 00 70 08 40 62 00 90 00','lazy_bind',[0,8])
    vals = [('ff '*9+'01',False,(1<<64)-1),('ff '*9+'00',True,(1<<63)-1),('80 '*9+'7f',True,-(1<<63)),('7f',True,-1)]
    for raw,signed,value in vals:
        v,pos,hx = leb(bytes.fromhex(raw),0,signed)
        assert v==value and pos==len(bytes.fromhex(raw))
    passed.append('64-bit LEB signed unsigned endpoints')
    raw = decode(bytes.fromhex('11 20 00 52 00'),'rebase',segs)
    matches = associate(raw['runs'],segs,[0,4,8,16])
    assert [len(matches[hex(x)]) for x in [0,4,8,16]] == [1,2,1,0]
    assert all(x['overlap']=='partial' for x in matches['0x4'])
    passed.append('analytic exact partial two-sided and absent intervals')
    assert len(associate(raw['runs']*2,segs,[0])['0x0'])==2
    passed.append('duplicate site retained')
    vs = [dict(segs[0],filesize=0)]
    virtual = decode(bytes.fromhex('11 20 00 51 00'),'rebase',vs)
    assert virtual['classic_pointer_site_decode_complete'] and virtual['runs'][0]['file_mapping']=='all_virtual_only'
    assert associate(virtual['runs'],vs,[0])['0x0'][0]['site_file_offset'] is None
    passed.append('virtual-only write cannot fabricate file mapping')
    return {'status':'PASS','count':len(passed),'controls':passed,'image_or_original_access':False}

def retained():
    expected = json.loads((HERE/'result.json').read_text())
    assert m['analyze'](HERE)==expected
    rejected = []
    for kind in ['raw_byte','word_byte','result_promotion','result_site','missing_stream']:
        with tempfile.TemporaryDirectory(prefix='electric-sites-owned-') as d:
            p=Path(d)
            shutil.copytree(HERE/'inputs',p/'inputs')
            shutil.copyfile(HERE/'result.json',p/'result.json')
            for f in p.rglob('*'):
                if f.is_file(): f.chmod(0o644)
            if kind in ['raw_byte','word_byte']:
                f=p/'inputs'/('rebase.bin' if kind=='raw_byte' else 'word-300c0.bin')
                b=bytearray(f.read_bytes()); b[0]^=1; f.write_bytes(b)
            elif kind=='missing_stream':
                (p/'inputs'/'lazy_bind.bin').unlink()
            else:
                f=p/'result.json'; j=json.loads(f.read_text())
                if kind=='result_promotion': j['runtime_targets_or_provider_resolution']=True
                else: j['six_words'][0]['hit_count']+=1
                f.write_text(json.dumps(j))
            try:
                assert m['analyze'](p)==json.loads((p/'result.json').read_text())
            except (AssertionError,ValueError,FileNotFoundError): rejected.append(kind)
            else: raise AssertionError('accepted owned tamper '+kind)
    return {'status':'PASS','owned_data_only':True,'writable_TEMP_files_only':True,'rejected_tampers':rejected,'count':len(rejected)}

if __name__=='__main__':
    assert len(sys.argv)==2
    if sys.argv[1]=='--synthetic': print(json.dumps(synthetic(),indent=2))
    elif sys.argv[1]=='--check': print(json.dumps(retained(),indent=2))
    else: raise ValueError('unknown mode')
