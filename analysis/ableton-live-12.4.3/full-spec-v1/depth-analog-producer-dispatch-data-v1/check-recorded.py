#!/usr/bin/env python3
"""Current packet data only. No external hashes, code decode, runtime or target follow."""
import argparse
import hashlib
import json
from pathlib import Path
P=Path(__file__).resolve().parent
PLAN='90b34f4fd24ba70197b21569ea43b4ddce68c83308e29dab4de5bab472d53cc6'
def load(n):return json.loads((P/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,n):
    if not ok:raise ValueError(n)
def project(raw):
    need(len(raw)==126,'whole126-byte-window')
    rows=[]
    for i,b in enumerate(raw):
        short=i<11;index=i if short else i-11
        base=0x2d34 if short else 0x2c9c
        rows.append({'table':'0x52ec0' if short else '0x52ecb','table_index':index,
                     'incoming_X1':index if short else index+0x58,'byte_VA':hex(0x52ec0+i),
                     'raw_byte':b,'branch_base':hex(base),'branch_address_nomination':hex(base+4*b),
                     'runtime_target':None,'destination_content_read':False})
    return rows
def validate_projection(rows,raw):
    need(rows==project(raw),'exact-whole-projection')
def check():
    rawplan=(P/'input-plan.json').read_bytes();need(sha(rawplan)==PLAN,'input-plan-pin')
    plan=json.loads(rawplan)
    before,after=load('capture/before-identities.json'),load('capture/after-identities.json')
    need(before==plan['pins']==after['files'] and after['unchanged'] and len(before)==12,'recorded-custody')
    for pin in plan['pins']:
        path=Path(pin['path'])
        if path.parent==P:
            b=path.read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'local-pin')
    extraction=load('capture/extraction.json')
    need(extraction['content_bytes']==134 and extraction['code_bytes']==0 and extraction['reads_per_range']==1,'content-count')
    tables=(P/'capture/dispatch-bytes.bin').read_bytes();word=(P/'capture/producer-word.bin').read_bytes()
    for row,raw in zip(extraction['ranges'],[tables,word]):
        need(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'raw-window-custody')
    need(len(tables)==126 and len(word)==8,'raw-widths')
    need(word.hex()=='8818000000000000' and int.from_bytes(word,'little')==0x1888,'raw-little-endian-integer')
    # All geometry is retained input metadata, not a new load-command/header read.
    for addr,count,sec in [(0x52ec0,126,plan['H4']['tables_geometry']), (0x58130,8,plan['H4']['word_geometry'])]:
        a=int(sec['VA'],16)
        need(a<=addr and addr+count<=a+sec['size'],'retained-section-range')
        need(sec['file_offset']+addr-a==addr,'retained-section-file-mapping')
    status=load('capture/status.json');outer=load('outer-invocation.json')
    need(status['error'] is None and status['watch_unchanged'] and status['selected_content_bytes_read']==134,'actual-success')
    need(status['attempts']==1 and not status['automatic_retry'] and status['children']==0 and status['original_instruction_execution']==0,'no-retry-child-runtime')
    need(outer['pid']==status['pid'] and outer['exit_code']==0 and not outer['timed_out'],'outer-status')
    need(outer['env']==status['environment']=={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'},'actual-environment')
    need(outer['started_utc']<=status['started_utc']<=status['finished_utc']<=outer['finished_utc'],'time-order')
    need((P/'outer.stderr').stat().st_size==0,'stderr-zero')
    rows=project(tables);validate_projection(rows,tables)
    need(len(rows)==126 and len({x['byte_VA'] for x in rows})==126,'whole-byte-coverage')
    need({x['incoming_X1'] for x in rows[:11]}==set(range(11)),'whole-short-guard')
    need({x['incoming_X1'] for x in rows[11:]}==set(range(0x58,0xcb)),'whole-long-guard')
    need({x['incoming_X1'] for x in rows[11:] if x['branch_address_nomination']=='0x2c9c'}=={0x58,0x64,0xab,0xb7},'all-four-special-long-entries')
    controls=[]
    def reject(n,fn):
        try:fn()
        except ValueError:controls.append(n)
        else:raise AssertionError('accepted:'+n)
    reject('truncate-long-guard',lambda:project(tables[:-1]))
    reject('add-unselected-byte',lambda:project(tables+b'\0'))
    bad=json.loads(json.dumps(rows));bad[0]['branch_base']='0x2c9c'
    reject('wrong-branch-base',lambda:validate_projection(bad,tables))
    bad=json.loads(json.dumps(rows));bad[11]['raw_byte']=128
    reject('wrong-raw-entry',lambda:validate_projection(bad,tables))
    bad=json.loads(json.dumps(rows));bad[-1]['incoming_X1']=0xcb
    reject('include-guard-excluded-selector',lambda:validate_projection(bad,tables))
    bad=json.loads(json.dumps(rows));bad[1]['branch_address_nomination']=hex(0x2d34+tables[1])
    reject('omit-times-four',lambda:validate_projection(bad,tables))
    bad=json.loads(json.dumps(rows));bad[0]['runtime_target']=bad[0]['branch_address_nomination']
    reject('runtime-target-promotion',lambda:validate_projection(bad,tables))
    bad=json.loads(json.dumps(rows));bad[0]['destination_content_read']=True
    reject('destination-read-promotion',lambda:validate_projection(bad,tables))
    reject('omit-multiple-equivalent-selector',lambda:validate_projection(rows[:-1],tables))
    reject('wrong-word-endianness',lambda:need(int.from_bytes(word,'big')==0x1888,'word-endian'))
    need(len(controls)==10,'control-count')
    groups={}
    for row in rows:groups.setdefault(row['branch_address_nomination'],[]).append(row['incoming_X1'])
    return {'status':'PASS','scope':'CURRENT_PACKET_ONLY; external identities compared only as recorded custody',
            'plan_sha256':PLAN,'raw_data_bytes':134,'projected_entries':126,'recorded_custody_pairs':12,
            'word':{'VA':'0x58130','bytes_hex':word.hex(),'little_endian_raw_integer':'0x1888','runtime_pointer_or_target':None},
            'entries':rows,'nomination_groups':groups,'unique_address_nominations':len(groups),
            'negative_controls':controls,'negative_control_count':len(controls),'native_or_original_execution':0,
            'main_site_resolution_credit':0,'new_ready_X':0,
            'limits':'Guard-backed byte windows, not maximal linker tables; branch andword integers are conditional nominations. No destination content, pointerencoding/fixup, class/ABI/public behavior or effective runtime permission proof.'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true',required=True);ap.parse_args()
    print(json.dumps(check(),indent=2))
