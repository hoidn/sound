#!/usr/bin/env python3
"""Image-free v2 method controls and writable-TEMP owned-data verification."""
import copy
import json
from pathlib import Path
import runpy
import shutil
import sys
import tempfile

HERE=Path(__file__).resolve().parent
m=runpy.run_path(str(HERE/'extract-sites.py'),run_name='inert_owned_v2')
decode,associate,leb=m['decode'],m['associate'],m['leb']
CONTEXT={'segments':[{'index':0,'name':'test','vmaddr':0,'vmsize':256,'fileoff':0,'filesize':256,'initprot':3,'maxprot':3},{'index':1,'name':'__LINKEDIT','vmaddr':256,'vmsize':256,'fileoff':256,'filesize':256,'initprot':1,'maxprot':1}],'linkedit_index':1,'dylib_count':2}

def synthetic():
    controls=[]
    def run(name,raw,mode='bind',expected=None,unknown=False,context=CONTEXT):
        r=decode(bytes.fromhex(raw),mode,context)
        if unknown:
            assert not r['classic_pointer_site_decode_complete'] and not r['absence_claim_allowed'],(name,r)
        else:
            assert r['classic_pointer_site_decode_complete'],(name,r['failure'])
        if expected is not None:
            sites=[x['segment_offset']+j*x['stride'] for x in r['runs'] for j in range(x['count'])]
            assert sites==expected,(name,sites)
        controls.append(name)
        return r
    run('classic rebase arithmetic','11 20 00 30 08 41 51 60 02 70 08 80 02 08 00','rebase',[16,24,32,40,56,72])
    run('classic ordinary bind arithmetic','11 40 78 00 51 70 00 80 08 90 a0 08 b1 c0 02 08 00',expected=[8,16,32,48,64])
    prefix='11 40 78 00 51 70 08 '
    wrapped=run('ADD_ADDR modulo64 returns valid site',prefix+'80 '+'f8 '+'ff '*8+'01 90 00',expected=[0])
    assert wrapped['trace'][-3]['modular_advance']['wrapped']
    zero=run('DO_BIND_ADD zero modular advance keeps distinct events',prefix+'a0 '+'f8 '+'ff '*8+'01 90 00',expected=[8,8])
    assert zero['runs'][0]['stride']==8 and zero['trace'][-3]['modular_advance']['delta_mod64']==0
    assert len(associate(zero['runs'],CONTEXT['segments'],[8])['0x8'])==2
    run('current emission retained before malformed next operand',prefix+'a0 80',expected=[8],unknown=True)
    run('wrapped destination outside segment stays unknown',prefix+'80 '+'f0 '+'ff '*8+'01 90 00',expected=[],unknown=True)
    run('ordinary requires explicit POINTER','11 40 78 00 70 00 90 00',unknown=True)
    run('ordinary requires ordinal','40 78 00 51 70 00 90 00',unknown=True)
    run('missing segment','11 40 78 00 51 90 00',unknown=True)
    run('missing symbol','11 51 70 00 90 00',unknown=True)
    run('ordinary ordinal exceeds dylibcount','13 40 78 00 51 70 00 90 00',unknown=True)
    run('special ordinal lower bound','3c 40 78 00 51 70 00 90 00',unknown=True)
    sp=run('known special WEAK_LOOKUP sign extension','3d 40 78 00 51 70 00 90 00',expected=[0])
    assert sp['runs'][0]['encoded_binding']['ordinal']['value']==-3
    run('weak POINTER and WEAK_LOOKUP defaults','40 78 00 70 00 90 00','weak_bind',[0])
    run('weak ordinal opcode forbidden','11 00','weak_bind',unknown=True)
    strong=run('weak strong marker is metadata not write','48 78 00 00','weak_bind',[])
    assert strong['trace'][0]['strong_definition_marker'] and not strong['runs']
    lazy=run('whole-lazy DONE persists established state','11 40 78 00 70 00 60 7f 90 00 90 00','lazy_bind',[0,8])
    assert all(x['encoded_binding']['addend']==-1 for x in lazy['runs'])
    run('whole-lazy pointer default but missing ordinal unknown','40 78 00 70 00 90 00','lazy_bind',unknown=True)
    run('lazy excludes analyzer type-setting','51 00','lazy_bind',unknown=True)
    run('lazy excludes ordinary modular ADD_ADDR','80 00 00','lazy_bind',unknown=True)
    run('lazy excludes ordinary DO_BIND_ADD','a0 00 00','lazy_bind',unknown=True)
    run('unknown symbol flags','42 78 00 00',unknown=True)
    run('nonpointer type','12 00','rebase',unknown=True)
    run('threaded opcode','d0 00',unknown=True)
    run('unknown opcode','f0 00',unknown=True)
    run('nonzero reserved immediate','11 20 00 31 00 00','rebase',unknown=True)
    run('missing DONE','11 20 00 51','rebase',[0],unknown=True)
    run('nonzero terminal suffix','00 11','rebase',unknown=True)
    run('empty stream','', 'weak_bind',[])
    run('DONE padding','11 20 00 51 00 00','rebase',[0])
    run('last 8B interval valid','11 20 f8 01 51 00','rebase',[248])
    run('8B interval crossing','11 20 f9 01 51 00','rebase',unknown=True)
    for name,changes in [('tiny vmsize',{'vmsize':7}),('virtual-only mapping',{'filesize':0}),('readonly protection',{'initprot':1}),('executable data',{'initprot':7})]:
        ctx=copy.deepcopy(CONTEXT);ctx['segments'][0].update(changes)
        run(name,'11 20 00 51 00','rebase',unknown=True,context=ctx)
    run('LINKEDIT emission forbidden','11 21 00 51 00','rebase',unknown=True)
    run('zero repeat does not emit','11 20 00 60 00 00','rebase',[])
    run('repeat remains strict and bounded','11 20 00 80 '+'ff '*9+'01 01 00','rebase',unknown=True)
    run('rebase ADD remains strict','11 20 08 30 '+'ff '*9+'01 00','rebase',unknown=True)
    for name,raw,mode in [('truncated ULEB','11 20 80','rebase'),('too long ULEB','11 20 '+'80 '*10+'00','rebase'),('unsigned overflow','11 20 '+'ff '*9+'02','rebase'),('signed overflow','60 '+'ff '*9+'01','bind'),('truncated SLEB','60 80','bind'),('unterminated symbol','40 78','bind')]:
        run(name,raw,mode,unknown=True)
    for raw,signed,value in [('ff '*9+'01',False,(1<<64)-1),('ff '*9+'00',True,(1<<63)-1),('80 '*9+'7f',True,-(1<<63)),('7f',True,-1)]:
        data=bytes.fromhex(raw);v,pos,hx=leb(data,0,signed);assert v==value and pos==len(data)
    controls.append('signed unsigned64 LEB endpoints')
    two=decode(bytes.fromhex('11 20 00 52 00'),'rebase',CONTEXT)
    matches=associate(two['runs'],CONTEXT['segments'],[0,4,8,16])
    assert [len(matches[hex(t)])for t in [0,4,8,16]]==[1,2,1,0]
    assert all(x['overlap']=='partial'for x in matches['0x4'])
    controls.append('analytical interval overlap both neighbors and exact absence')
    return {'status':'PASS','controls':controls,'count':len(controls),'image_or_original_access':False,'only_in_memory_test_inputs':True}

def retained():
    assert m['analyze'](HERE)==json.loads((HERE/'result.json').read_text())
    rejected=[]
    for kind in ['stream_byte','word_byte','LC_permissions','LC_dylibcount','result_promotion','result_site','missing_stream']:
        with tempfile.TemporaryDirectory(prefix='electric-sites-v2-')as directory:
            p=Path(directory);shutil.copytree(HERE/'inputs',p/'inputs');shutil.copyfile(HERE/'result.json',p/'result.json')
            for f in p.rglob('*'):
                if f.is_file():f.chmod(0o644)
            if kind in ['stream_byte','word_byte','LC_permissions','LC_dylibcount']:
                name={'stream_byte':'bind.bin','word_byte':'word-300c0.bin','LC_permissions':'load-commands.bin','LC_dylibcount':'load-commands.bin'}[kind]
                f=p/'inputs'/name;b=bytearray(f.read_bytes());offset={'stream_byte':0,'word_byte':0,'LC_permissions':664-32+60,'LC_dylibcount':1584-32}[kind];b[offset]^=1 if kind!='LC_permissions'else 2;f.write_bytes(b)
            elif kind=='missing_stream':(p/'inputs/lazy_bind.bin').unlink()
            else:
                f=p/'result.json';j=json.loads(f.read_text())
                if kind=='result_promotion':j['runtime_targets_or_provider_resolution']=True
                else:j['six_words'][0]['accepted_hit_count']+=1
                f.write_text(json.dumps(j))
            try:assert m['analyze'](p)==json.loads((p/'result.json').read_text())
            except (AssertionError,ValueError,FileNotFoundError):rejected.append(kind)
            else:raise AssertionError('accepted owned tamper '+kind)
    return {'status':'PASS','owned_data_only':True,'writable_TEMP_files_only':True,'rejected':rejected,'count':len(rejected)}

if __name__=='__main__':
    assert len(sys.argv)==2
    if sys.argv[1]=='--synthetic':print(json.dumps(synthetic(),indent=2))
    elif sys.argv[1]=='--check':print(json.dumps(retained(),indent=2))
    else:raise ValueError('unknown mode')
