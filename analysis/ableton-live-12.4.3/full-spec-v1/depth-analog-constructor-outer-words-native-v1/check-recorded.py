"""Packet-only checks; never opens external pin paths or launches a child."""
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
STARTS = [0x59608,0x59630,0x59648,0x59650,0x59658,0x59660]
VALUES = [0x1a128,0x1a18c,0x19a60,0x19ae0,0x19b60,0x19a14]
PRE_SHA = '7dff1087897f5ea266172bc0fb7bb2ca79fdfd6e5f20c98c36deaa364b2cdfb6'

def require(test, message):
    if not test:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(name):
    return json.loads((HERE/name).read_bytes())

def branch(raw):
    require(len(raw)==4,'one native word')
    word=int.from_bytes(raw,'little')
    require(word & 0xfc000000 == 0x14000000,'unconditional B, not BL/other')
    imm=word & 0x03ffffff
    signed=imm-(1<<26) if imm & (1<<25) else imm
    target=0x1760+signed*4
    require(target==0x15e0,'exact prior entry, not another callee')
    return {'word_hex':hex(word),'signed_imm26':signed,'displacement_bytes':signed*4,'target':hex(target),
            'writes_general_registers':False,'writes_link_register':False}

def rowcheck(row,raw):
    require(type(row['offset']) is int and row['offset']==0x1760,'row PC')
    require(type(row['size']) is int and row['size']==4,'row size')
    require(row['bytes']==raw.hex(),'retained raw association')
    require(row['jump']==0x15e0 and row['type']=='jmp','decoder projection')
    require(row['opcode']=='b 0x15e0','decoder spelling')
    branch(raw)

def wordcheck(rows,raws,mapping):
    require(len(rows)==len(raws)==6,'six words only')
    section=mapping['const_section']; base=int(section['addr'],16)
    require(base==0x580b0 and section['offset']==360624 and section['size']==9672,'retained section')
    for start,value,row,raw in zip(STARTS,VALUES,rows,raws):
        require(row['start']==hex(start) and row['file_offset']==start and row['bytes']==8,'selected word geometry')
        require(base<=start and start+8<=base+section['size'],'word within retained section')
        require(section['offset']+start-base==start,'mapped file position')
        require(len(raw)==8 and row['raw_hex']==raw.hex() and row['sha256']==sha(raw),'word bytes/hash')
        require(int.from_bytes(raw,'little')==value,'stored integer observation')

def claimcheck(a):
    require(a['scope']=={'code_bytes':4,'decoded_rows':1,'literal_bytes':48,'literal_words':6,'total_content_bytes':52},'fixed scope')
    require(a['native_fact']['kind']=='unconditional-local-B-preserving-X0-and-X30','branch role')
    c=a['conditional_composition']
    require(c['A_equals_prior_P_Q_B']=='conditional-normal-path-only' and len(c['premises'])>=6,'carrier qualifications')
    require(c['A_equals_O']=='unknown' and c['R_binding']=='unknown' and c['C_binding']=='unknown','unproved carrier joins')
    require(a['literal_interpretation']['runtime_pointer_or_target_proved'] is False,'no raw-word promotion')
    require(a['literal_interpretation']['current_O_table_continuity']=='unknown','no stable-vptr assumption')
    require(a['claims_not_established']['actual_Live_binding'] is False,'no public promotion')
    require(a['counts']['main_inventory']=='25095 of268015 unchanged' and a['counts']['new_resolved_bundle_runtime_sites']==0,'separate image count')
    require(a['counts']['original_instructions_executed']==0 and a['required_status']=='U/OPEN unchanged','no execution/grade')

def check():
    pre=(HERE/'pre-call-manifest.json').read_bytes(); require(sha(pre)==PRE_SHA,'pre-call identity')
    p=json.loads(pre); status=read('capture/status.json'); before=read('capture/before-identities.json'); after=read('capture/after-identities.json')
    expected=[p['image'],p['tool'],*p['pins'],{'path':str(HERE/'pre-call-manifest.json'),'bytes':len(pre),'sha256':PRE_SHA}]
    require(len(before)==17 and before==expected==after['files'] and after['unchanged'] is True,'17 recorded custody pairs')
    # External identities are receipt comparisons only, never reopened here.
    for pin in p['pins']:
        q=Path(pin['path'])
        if q.parent==HERE:
            raw=q.read_bytes(); require(len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],'packet source pin')
    require(status['error'] is None and status['watch_unchanged'] is True,'capture success')
    require(status['attempts']==status['children_started']==1 and status['validated_words']==1 and status['validated_bytes']==4,'single complete decoder')
    require(status['selected_bytes_read']==4 and status['selected_table_bytes_read']==48 and status['native_original_instruction_execution']==0,'exact static content')
    raw=(HERE/'capture/1760.bin').read_bytes(); rows=read('capture/1760.stdout.json'); require(len(rows)==1,'one decoder row'); rowcheck(rows[0],raw)
    receipt=read('capture/1760.invocation-after.json'); pid=read('capture/1760.pid.json')
    require(receipt['pid']==pid['pid'] and receipt['pid']>0 and receipt['exit_code']==0 and receipt['timed_out'] is False and receipt['error'] is None,'child status')
    require(receipt['timeout_seconds']==30 and receipt['stdin']=='DEVNULL' and receipt['core_limit_bytes']==0 and receipt['new_process_session'] is True,'fixed child policy')
    require(receipt['cleanup']=='process-group-already-gone' and (HERE/'capture/1760.stderr').read_bytes()==b'','cleanup/stderr')
    require(receipt['argv']==[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m','0x1760','-s','0x1760','-q','-c','pdj 1',str(HERE/'capture/1760.bin')],'exact argv')
    words=read('capture/table-words.json')['words']; raws=[(HERE/('capture/word-'+hex(s)[2:]+'.bin')).read_bytes() for s in STARTS]
    mapping=read('retained-map.json'); wordcheck(words,raws,mapping)
    ex=read('capture/extraction.json'); require(ex['ranges'][0]['sha256']==sha(raw) and ex['total_code_bytes']==4 and ex['total_table_bytes']==48,'extraction')
    a=read('assessment.json'); claimcheck(a)
    rejected=[]
    def reject(name, action):
        try: action()
        except (ValueError,KeyError,TypeError): rejected.append(name); return
        raise ValueError('accepted negative: '+name)
    reject('BL changes link register',lambda:branch((int.from_bytes(raw,'little')|0x80000000).to_bytes(4,'little')))
    reject('wrong branch destination',lambda:branch((int.from_bytes(raw,'little')+1).to_bytes(4,'little')))
    reject('truncated native word',lambda:branch(raw[:-1]))
    bad=copy.deepcopy(rows[0]); bad['bytes']='00000000'; reject('decoder/raw mismatch',lambda:rowcheck(bad,raw))
    badw=copy.deepcopy(words); badw[0]['start']='0x58150'; reject('forbidden presumed R word',lambda:wordcheck(badw,raws,mapping))
    badraw=copy.deepcopy(raws); badraw[0]=badraw[0][::-1]; reject('wrong literal endian/bytes',lambda:wordcheck(words,badraw,mapping))
    for name,group,key,value in [('raw word becomes runtime target','literal_interpretation','runtime_pointer_or_target_proved',True),
                               ('stable O vptr assumed','literal_interpretation','current_O_table_continuity','proved'),
                               ('A equated O','conditional_composition','A_equals_O','proved'),
                               ('R equated A','conditional_composition','R_binding','A'),
                               ('C assigned known addresspoint','conditional_composition','C_binding','0x580c0'),
                               ('public binding promoted','claims_not_established','actual_Live_binding',True),
                               ('bundle added main sites','counts','main_inventory','25096 of268015'),
                               ('runtime-site closure','counts','new_resolved_bundle_runtime_sites',1)]:
        bad=copy.deepcopy(a); bad[group][key]=value; reject(name,lambda bad=bad:claimcheck(bad))
    if (HERE/'manifest.json').exists():
        m=read('manifest.json'); actual={str(q.relative_to(HERE)) for q in HERE.rglob('*') if q.is_file() and q.name!='manifest.json'}
        require(actual=={x['path'] for x in m['files']},'exact sealed tree')
        for x in m['files']:
            b=(HERE/x['path']).read_bytes(); require(len(b)==x['bytes'] and sha(b)==x['sha256'],'sealed payload hash')
    return {'status':'PASS-packet-data-only','code_bytes':4,'decoded_rows':1,'literal_bytes':48,'custody_pairs':17,'child_receipts':1,
            'raw_branch_fields':branch(raw),'literal_values_little_endian':[hex(v) for v in VALUES],
            'negative_controls':rejected,'external_paths_reopened':0,'decoder_children_launched':0,'original_instructions_executed':0}

if __name__=='__main__':
    require(sys.argv[1:]==['--check'],'only --check')
    print(json.dumps(check(),indent=2))
