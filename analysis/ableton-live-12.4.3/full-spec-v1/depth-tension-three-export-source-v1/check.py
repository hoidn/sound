#!/usr/bin/env python3
"""Fixed packet-only source projection/scope checks; no external reads or runtime."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
EXPECTED=[
 ('0x12fc8',810,'a076561f271be8747b4c5e462360b2fc27dc4aed65dc76de400905de49f5e5b0',431,18,'2de2e82908e86d72be57188d16e845f97e8d771010ab7867df696769a7c24d9e',132,'0x1304b'),
 ('0x13248',3788,'98f59ad608fd55cdd2a1bb369aa3241246d07b661a4ec9b6a8b14c590d5d4b7f',3254,131,'1999e40c9a73916ff0759507cf5d7ea396fdffd3698c2277db654218e2da34bc',664,'0x134df'),
 ('0x13590',688,'d8a7088ed020b473bdc766dabd6dc0a3b9f803c7bebe84a716e2773f089b8b4f',314,17,'4c9915c93b7ec2aac996f62956901615656ec8065a03fa0af3ccc643101f13cb',104,'0x135f7')]

def sha(b):return hashlib.sha256(b).hexdigest()

def validate(raw,projections,a):
    lines=raw.splitlines(keepends=True)
    assert len(lines)==3 and len(raw)==5286
    assert a['selected_entries']==[e[0] for e in EXPECTED]
    assert a['totals']=={'records':3,'raw_bytes':5286,'C_bytes':3999,'C_lines':166,'metadata_native_extent_bytes':900}
    assert len(a['records'])==3
    for b,e,selected in zip(lines,EXPECTED,a['records']):
        entry,n,rh,cn,cl,ch,bn,end=e
        assert len(b)==n and sha(b)==rh and b.endswith(b'\n')
        r=json.loads(b);code=projections[entry]
        assert r['entry']==entry and selected['entry']==entry
        assert r['code'].encode()==code and len(code)==cn==r['code_bytes']
        assert len(code.splitlines())==cl==selected['C_lines']
        assert sha(code)==ch==r['code_sha256']
        assert {k:v for k,v in r.items() if k!='code'}==selected['metadata']
        assert r['body_ranges']==[[entry,end]] and r['body_bytes']==bn==int(end,16)-int(entry,16)+1
        assert r['thunk'] is False and r['error'] is None and r['partial_code'] is False and r['timed_out'] is False
        assert r['signature']=='undefined '+r['name']+'()'
        assert selected['source_locator']['raw_bytes']==n and selected['source_locator']['raw_sha256']==rh
        if entry=='0x13248':
            assert r['state']=='exported-with-warnings' and r['warnings']==['/* WARNING: Subroutine does not return */']
        else:assert r['state']=='exported' and r['warnings']==[]
    assert a['metadata_signature_mismatches_preserved'] is True
    assert [(r['site'],r['byte_slot'],r['target']) for r in a['slot_frontier']]==[
        ('0x12ff8','0x68','unresolved'),('0x13388','0x60','unresolved'),('0x133a8','0x68','unresolved'),('0x135a8','0x38','unresolved')]
    assert a['slot_frontier'][-1]['argument_projection']=='()'
    assert a['unread_direct_callees']==['0x1b7c','0x1c18','0x162ec','0x1577c','0x163a0']
    assert {c['id'] for c in a['claims']}=={'TEN-E'+str(i).zfill(2) for i in range(1,11)} and len(a['claims'])==10
    anchors={'TEN-E01':('12fc8.c',[2,8]),'TEN-E02':('12fc8.c',[9,16]),'TEN-E03':('13590.c',[2,15]),'TEN-E04':('13248.c',[2,33]),'TEN-E05':('13248.c',[34,47]),'TEN-E06':('13248.c',[48,70]),'TEN-E07':('13248.c',[71,74]),'TEN-E08':('13248.c',[75,124]),'TEN-E09':('13248.c',[125,131])}
    for c in a['claims']:
        if c['id'] in anchors:assert (c['source'],c['C_lines'])==anchors[c['id']]
    for key,v in a['result'].items():
        if key.startswith('new_'):assert type(v) is int and v==0
        elif key=='coverage':assert v=='OPEN-required-unsupported-remains-U'
        else:assert v=='unknown'
    assert a['no_successor_selected'] is True
    assert len(a['selected_indirect_metadata'])==5
    for x in a['selected_indirect_metadata']:
        r=x['record']
        if r['site']=='0x13270':assert r['resolved_targets'][0]['function']=='0x72500'
        else:assert r['resolved_targets']==[]
    # Entire projections are pinned; these anchors expose material recovery gaps explicitly.
    create=projections['0x12fc8'].decode().splitlines()
    calc=projections['0x13248'].decode().splitlines()
    setter=projections['0x13590'].decode().splitlines()
    assert '(*plVar2 + 0x68)' in create[9]
    assert 'auVar12 = (*(code *)PTR____chkstk_darwin_0005c080)();' in calc[29]
    assert 'lVar9 = auVar12._8_8_;' in calc[30] and 'plVar7 = auVar12._0_8_;' in calc[31]
    assert setter[12]=='    (**(code **)(*param_1 + 0x38))();'
    assert 'WARNING: Subroutine does not return' in calc[127]

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);p.parse_args()
    raw=(HERE/'records.jsonl').read_bytes()
    projections={e[0]:(HERE/(e[0][2:]+'.c')).read_bytes() for e in EXPECTED}
    a=json.loads((HERE/'assessment.json').read_bytes())
    validate(raw,projections,a)
    rejected=[]
    def reject(name,change):
        x=[raw,copy.deepcopy(projections),copy.deepcopy(a)];change(x)
        try:validate(*x)
        except (AssertionError,KeyError,ValueError):rejected.append(name)
        else:raise AssertionError('accepted negative control '+name)
    reject('lost whole record',lambda x:x.__setitem__(0,b''.join(raw.splitlines(keepends=True)[:2])))
    reject('truncated C projection',lambda x:x[1].__setitem__('0x13248',x[1]['0x13248'][:-1]))
    reject('metadata warning concealed',lambda x:x[2]['records'][1]['metadata'].__setitem__('warnings',[]))
    reject('metadata signature mismatch concealed',lambda x:x[2].__setitem__('metadata_signature_mismatches_preserved',False))
    reject('invented recovered setter arguments',lambda x:x[2]['slot_frontier'][-1].__setitem__('argument_projection','(receiver,63,value)'))
    reject('invented indirect target',lambda x:x[2]['slot_frontier'][0].__setitem__('target','0x1b7c'))
    reject('stack-probe receiver repaired by guess',lambda x:x[2]['result'].__setitem__('Calc_plVar7_equals_param1','proved'))
    reject('ungated law promoted',lambda x:x[2]['result'].__setitem__('internal_Damper_state_gating_and_named_predicate','no-effect'))
    reject('new site credit',lambda x:x[2]['result'].__setitem__('new_resolved_indirect_sites',1))
    reject('missing complete source claim',lambda x:x[2]['claims'].pop())
    reject('false source anchor',lambda x:x[2]['claims'][2].__setitem__('C_lines',[2,14]))
    reject('automatic successor selected',lambda x:x[2].__setitem__('no_successor_selected',False))
    print(json.dumps({'status':'PASS-packet-only','records':3,'raw_bytes':5286,'C_bytes':3999,'C_lines':166,'warnings':1,'unresolved_receiver_sites':4,'negative_controls_rejected':rejected,'external_source_native_provider_reads':0,'original_model_harness_calls':0,'new_site_case_grade_credit':0},indent=2))

if __name__=='__main__':main()
