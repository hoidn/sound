"""Read-only packet checks; never invokes an external tool or reads the image."""
from pathlib import Path
import copy,hashlib,json,struct,sys
if sys.argv[1:] != ['--check']:
    raise SystemExit('Only --check is supported; extraction, replay and writes are refused.')
root=Path(__file__).resolve().parent

def validate(raw,decoded,findings):
    assert len(raw)==100 and len(decoded)==25
    for i,row in enumerate(decoded):
        assert row['offset']==0x1024f415c+4*i and row['size']==4
        assert bytes.fromhex(row['bytes'])==raw[4*i:4*i+4]
    words=struct.unpack('<25I',raw)
    # These exact instruction words anchor register arguments and store bases.
    expected={4:0xaa0803f3,5:0x52801500,7:0xaa0003f4,11:0xf9000008,
              13:0xf9001408,15:0xf9000274,19:0xaa1403e0,24:0xd65f03c0}
    for i,word in expected.items(): assert words[i]==word
    def branch(i):
        w=words[i];assert w>>26==0b100101
        imm=w&0x3ffffff
        if imm&(1<<25):imm-=1<<26
        return 0x1024f415c+4*i+4*imm
    assert [branch(i) for i in (6,8,14,20)]==[0x1012d9734,0x1026e8e50,0x101486414,0x101482718]
    # ADRP's signed immediate is relative to the current instruction page.
    w=words[9];assert w&0x9f00001f==0x90000008
    imm=((w>>5)&0x7ffff)<<2 | ((w>>29)&3)
    if imm&(1<<20):imm-=1<<21
    page=((0x1024f415c+4*9)&~0xfff)+(imm<<12)
    assert page==0x1067c6000
    for i,immediate in [(10,0xb90),(12,0x308)]:
        w=words[i];assert w&0xffc003ff==0x91000108
        assert (w>>10)&0xfff==immediate
    assert page+0xb90==0x1067c6b90 and page+0xb90+0x308==0x1067c6e98
    assert findings['A1']=='unknown' and findings['grade'] is None
    assert findings['application_expected'] is None and findings['application_comparison'] is None
    assert findings['conditional_join']['remaining_source_premise']
    assert findings['scope']['original_instructions_executed'] is False
    assert findings['new_requirements']==findings['new_cases']==findings['coverage_credit']==0

manifest=json.loads((root/'manifest.json').read_bytes())
watched={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.is_file()}
assert set(watched)==set(manifest['files'])|{'manifest.json'}
for name,pin in manifest['files'].items():
    b=(root/name).read_bytes()
    assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256']
raw=(root/'factory-100.bin').read_bytes()
decoded=json.loads((root/'factory-100.stdout.json').read_bytes())
findings=json.loads((root/'findings.json').read_bytes())
validate(raw,decoded,findings)
control=json.loads((root/'synthetic-ret.stdout.json').read_bytes())
assert len(control)==1 and control[0]['offset']==0x1024f415c
assert control[0]['opcode']=='ret' and control[0]['bytes']=='c0035fd6'
assert (root/'synthetic-ret.bin').read_bytes()==bytes.fromhex('c0035fd6')
for label,count in [('synthetic-ret',1),('factory-100',25)]:
    record=json.loads((root/(label+'.invocation.json')).read_bytes())
    argv=record['argv']
    assert record['exit']==0 and argv[1:4]==['-NN','-n','-x']
    assert argv[4:10]==['-a','arm','-b','64','-E','little']
    assert argv[10:15]==['-m','0x1024f415c','-s','0x1024f415c','-q']
    assert argv[15:17]==['-c','pdj '+str(count)]
    assert (root/(label+'.stderr')).read_bytes()==b''
extraction=json.loads((root/'extraction.json').read_bytes())
assert extraction['providers_before']==extraction['providers_after']
assert extraction['length']==100 and extraction['selected_mapping']['name']=='__TEXT'
assert extraction['raw_sha256']==hashlib.sha256(raw).hexdigest()
negative=0
for mode in ['changed argument word','changed mapped offset','constructor result promoted to instruction identity','invented grade']:
    r=bytearray(raw); d=copy.deepcopy(decoded); f=copy.deepcopy(findings)
    if mode=='changed argument word':r[16]^=1;d[4]['bytes']=bytes(r[16:20]).hex()
    elif mode=='changed mapped offset':d[0]['offset']+=4
    elif mode=='constructor result promoted to instruction identity':f['conditional_join']['remaining_source_premise']=''
    else:f['grade']='pass'
    try:validate(bytes(r),d,f)
    except AssertionError:negative+=1
    else:raise AssertionError('Mutation accepted: '+mode)
assert negative==4
assert watched=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.is_file()}
print(json.dumps({'status':'PASS','original_bytes':100,'original_words':25,'synthetic_controls':1,'negative_fixtures':negative,'packet_files_unchanged':len(watched),'original_calls':0,'tool_replays':0}))
