#!/usr/bin/env python3
"""Owned recorded44-byte packet checker; no external reads/imports/decoder/ESIL."""
import argparse,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent
PLAN='fdfc5d6013b288128623a447734d511f21915b3376f68e196f4226b1d6cf54c1'
WORDS=['f44fbea9','fd7b01a9','fd430091','008e8452','573c0194','f30300aa','ea0a0094','e00313aa','fd7b41a9','f44fc2a8','c0035fd6']
def load(n):return json.loads((P/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,n):
    if not ok:raise ValueError(n)
def sx(v,n):return v-(1<<n) if v&(1<<(n-1)) else v
def bl(w,pc):
    need(w&0xfc000000==0x94000000,'BL-family');return pc+(sx(w&0x3ffffff,26)<<2)
def pair(w):
    need(w&0x3a000000==0x28000000 and not w&(1<<26) and w>>30==2,'GPR64-pair')
    return {'rt':w&31,'rt2':(w>>10)&31,'rn':(w>>5)&31,'offset':sx((w>>15)&127,7)*8,'load':bool(w&(1<<22)),'mode':(w>>23)&3}
def equal(a,b,n):need(a==b,n)
def check():
    pr=(P/'input-plan.json').read_bytes();need(sha(pr)==PLAN,'frozen-plan');plan=json.loads(pr)
    before,after=load('capture/before-identities.json'),load('capture/after-identities.json')
    need(before==plan['pins']==after['files'] and after['unchanged'] and len(before)==12,'recorded-custody')
    for pin in plan['pins']:
        f=Path(pin['path'])
        if f.parent==P:
            b=f.read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'local-pin')
    raw=(P/'capture/1888.bin').read_bytes();rows=load('capture/1888.stdout.json');need(len(raw)==44 and len(rows)==11,'whole-extent')
    need(raw==bytes.fromhex(''.join(WORDS)),'complete-raw-word-set')
    for i,r in enumerate(rows):need((r['offset'],r['size'],r['bytes'])==(0x1888+4*i,4,WORDS[i]),'raw-association')
    words=[int.from_bytes(raw[i:i+4],'little') for i in range(0,44,4)]
    need(bl(words[4],0x1898)==rows[4]['jump']==0x509f4,'first-raw-BL')
    need(bl(words[6],0x18a0)==rows[6]['jump']==0x4448,'second-raw-BL')
    need(words[3]&0xff80001f==0x52800000 and ((words[3]>>5)&65535)==0x2470,'W0-constant')
    need(words[5]==0xaa0003f3 and words[7]==0xaa1303e0,'save-first-return-and-restore-X0')
    need(words[10]==0xd65f03c0,'RET-X30')
    ps=[pair(words[i]) for i in [0,1,8,9]]
    equal(ps,[{'rt':20,'rt2':19,'rn':31,'offset':-32,'load':False,'mode':3},
              {'rt':29,'rt2':30,'rn':31,'offset':16,'load':False,'mode':2},
              {'rt':29,'rt2':30,'rn':31,'offset':16,'load':True,'mode':2},
              {'rt':20,'rt2':19,'rn':31,'offset':32,'load':True,'mode':1}],'four-stack-pair-fields')
    sr=(P/'source-context.jsonl').read_bytes();source=json.loads(sr);meta=load('selected-metadata.json')
    need(len(sr)==483 and sha(sr)==meta['raw_sha256'],'source-record')
    cb=source['code'].encode();need(len(cb)==126 and sha(cb)==source['code_sha256'] and len(source['code'].splitlines())==11,'source-C')
    need(source['entry']=='0x1888' and source['body_bytes']==44 and source['state']=='exported' and not source['thunk'] and not source['warnings'] and source['error'] is None and not source['partial_code'] and not source['timed_out'],'source-status')
    s=load('capture/status.json');inv=load('capture/invocation-after.json');pid=load('capture/pid.json');outer=load('outer-invocation.json')
    need(s['error'] is None and s['watch_unchanged'] and s['attempts']==1 and s['children_started']==1 and s['validated_rows']==11 and s['native_original_execution']==0 and not s['automatic_retry'],'capture-status')
    need(inv['exit_code']==0 and not inv['timed_out'] and inv['pid']==pid['pid']==pid['pgid'] and inv['argv']==pid['argv'],'decoder-status')
    need(inv['timeout_seconds']==30 and inv['stdin']=='DEVNULL' and inv['core_bytes']==0 and inv['new_session'],'decoder-limits')
    need(outer['pid']==s['pid'] and outer['exit_code']==0 and not outer['timed_out'],'outer-status')
    need((P/'capture/1888.stderr').stat().st_size==(P/'outer.stderr').stat().st_size==0,'stderr')
    controls=[]
    def reject(n,fn):
        try:fn()
        except ValueError:controls.append(n)
        else:raise AssertionError(n)
    reject('first-target-not-C-name',lambda:equal(bl(words[4],0x1898),0x3b18,'first-target'))
    reject('second-target-not-C-thunk-name',lambda:equal(bl(words[6],0x18a0),0x3b18,'second-target'))
    reject('wrong-first-call-PC',lambda:equal(bl(words[4],0x189c),0x509f4,'PC'))
    reject('second-call-return-not-preserved-return',lambda:equal(words[7],0xaa0003e0,'X0-return-source'))
    reject('incoming-X0-not-preserved-receiver',lambda:equal(words[3],0xaa0003f3,'X0-overwrite'))
    reject('postindex-not-offset-mode',lambda:equal(ps[-1]['mode'],2,'pair-mode'))
    reject('stackpair-not-objectstore',lambda:equal(ps[0]['rn'],0,'pair-base'))
    reject('stackdelta-not16',lambda:equal(ps[0]['offset'],-16,'stack-delta'))
    reject('no-extra-tableword',lambda:equal(plan['data_bytes'],8,'data-expansion'))
    reject('no-truncated-body',lambda:equal(len(rows),10,'wholebody'))
    need(len(controls)==10,'controls')
    return {'status':'PASS','scope':'currentpacketonly;externalcustodyrecordcomparisonnotfreshrehash','rows':11,'native_bytes':44,'C_bytes':126,'C_lines':11,'raw_associations':[{'pc':hex(r['offset']),'bytes':r['bytes']} for r in rows],'raw_BL_targets':[{'pc':'0x1898','nomination':'0x509f4'},{'pc':'0x18a0','nomination':'0x4448'}],'stack_pair_fields':ps,'negative_controls':controls,'negative_control_count':10,'recorded_custody_pairs':12,'child_pid':inv['pid'],'ESIL_used':False,'source_C_name_native_target_join':'UNPROVED;sourceoperator_new/thunk_FUN_00003b18vsnative509f4/4448','runtimebinding_site_grade_credit':0}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true',required=True);ap.parse_args();print(json.dumps(check(),indent=2))
