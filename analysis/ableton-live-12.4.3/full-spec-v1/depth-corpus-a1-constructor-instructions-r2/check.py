"""Finite data-only checks. No subprocess, decoder, image read or source execution."""
from pathlib import Path
import copy,hashlib,json,struct,sys
if sys.argv[1:]!=['--check']:
    raise SystemExit('Only --check; decode, capture, extraction and writes refused.')
root=Path(__file__).resolve().parent

def validate(raw,rows,findings):
    assert len(raw)==288 and len(rows)==72
    assert hashlib.sha256(raw).hexdigest()=='3c36b423c1a6cd8f194ec973135ba170c4e764194419e27642161f0475123885'
    for i,row in enumerate(rows):
        assert row['offset']==0x1026e8e50+4*i and row['size']==4
        assert bytes.fromhex(row['bytes'])==raw[4*i:4*i+4]
    words=struct.unpack('<72I',raw)
    assert words[5]==0xaa0003f3  # Entry X0 -> X19.
    assert words[64]==words[66]==0xaa1303e0  # Saved entry -> final X0.
    assert words[71]==0xd65f03c0
    def displacement(w,bits,shift):
        imm=(w>>shift)&((1<<bits)-1)
        if imm&(1<<(bits-1)):imm-=1<<bits
        return 4*imm
    for i,target in [(17,23),(30,36)]:
        assert words[i]&0xff00001f==0xb4000000
        assert 4*i+displacement(words[i],19,5)==4*target
    for i,target in [(21,23),(34,36)]:
        assert words[i]&0xff00001f==0x54000001
        assert 4*i+displacement(words[i],19,5)==4*target
    for i in [3,67]:
        w=words[i];imm=(w>>15)&127
        if imm&64:imm-=128
        assert (w&31,(w>>10)&31,(w>>5)&31,imm*8)==(29,30,31,48)
    assert findings['normal_return_proof']['entry_save']['index']==5
    assert findings['normal_return_proof']['last_result_assignment']['index']==66
    assert 'callee-save' in ' '.join(findings['premises'])
    assert findings['premises'] and findings['unknowns']
    assert findings['A1']=='unknown' and findings['grade'] is None
    assert findings['application_expected'] is None and findings['application_comparison'] is None
    assert findings['new_requirements']==findings['new_cases']==findings['coverage_credit']==0

manifest=json.loads((root/'manifest.json').read_bytes())
watch={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir()}
assert set(watch)==set(manifest['files'])|{'manifest.json'}
for name,pin in manifest['files'].items():
    b=(root/name).read_bytes()
    assert {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}==pin
raw=(root/'constructor-288.bin').read_bytes()
rows=json.loads((root/'constructor-288.stdout.json').read_bytes())
f=json.loads((root/'findings.json').read_bytes());validate(raw,rows,f)
before=json.loads((root/'before-map.json').read_bytes())['providers']
after=json.loads((root/'after-map.json').read_bytes())
assert before==after['providers'] and after['unchanged']
for pin in before:
    b=Path(pin['path']).read_bytes()
    assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256']
argv=json.loads((root/'invocation-before.json').read_bytes())['argv']
assert argv[1:5]==['-NN','-n','-x','-f']
assert argv[5:11]==['-a','arm','-b','64','-E','little']
assert argv[11:18]==['-m','0x1026e8e50','-s','0x1026e8e50','-q','-c','pdj 72']
status=json.loads((root/'status.json').read_bytes())
assert status['exit']==0 and status['exception'] is None
assert (root/'constructor-288.stderr').read_bytes()==b''
negative=0
for mutation in ['short raw','changed final move','wrong offset','incomplete decoder row','missing ABI premise','invented A1 grade']:
    r=bytearray(raw);d=copy.deepcopy(rows);g=copy.deepcopy(f)
    if mutation=='short raw':r=r[:-4]
    elif mutation=='changed final move':r[66*4]^=1;d[66]['bytes']=bytes(r[66*4:67*4]).hex()
    elif mutation=='wrong offset':d[71]['offset']+=4
    elif mutation=='incomplete decoder row':d[64]['size']=0
    elif mutation=='missing ABI premise':g['premises']=[]
    else:g['grade']='pass'
    try:validate(bytes(r),d,g)
    except AssertionError:negative+=1
    else:raise AssertionError('Mutation accepted: '+mutation)
assert negative==6
assert watch=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir()}
print(json.dumps({'status':'PASS','raw_bytes':288,'words':72,'negative_fixtures':negative,'packet_files_unchanged':len(watch),'external_pins_unchanged':len(before),'original_calls':0,'tool_replays':0}))
