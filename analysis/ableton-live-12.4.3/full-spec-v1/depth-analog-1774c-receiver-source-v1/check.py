#!/usr/bin/env python3
"""Data-only checks; no imports or executions of retained helper tooling."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def sha(b):
    return hashlib.sha256(b).hexdigest()

def validate(raw, code, locator, assessment):
    record = json.loads(raw)
    assert len(raw.splitlines()) == 1 and raw.endswith(b'\n')
    assert record['entry'] == '0x1774c' and record['name'] == 'FUN_0001774c'
    assert len(raw) == locator['raw_bytes'] == 1007
    assert sha(raw) == locator['raw_sha256']
    assert code == record['code'].encode('utf-8')
    assert len(code) == record['code_bytes'] == locator['C_bytes'] == 630
    assert sha(code) == record['code_sha256'] == locator['C_sha256']
    assert len(code.splitlines()) == locator['C_lines'] == 27
    assert len(raw) <= 32768 and len(code) <= 32768 and len(code.splitlines()) <= 1000
    assert {k:v for k,v in record.items() if k != 'code'} == locator['record_metadata']
    assert record['thunk'] is False and record['state'] == 'exported'
    assert record['warnings'] == [] and record['error'] is None
    assert record['partial_code'] is False and record['timed_out'] is False
    assert record['signature'] == 'undefined FUN_0001774c()'
    assert record['body_ranges'] == [['0x1774c', '0x17837']]
    assert int('17837',16)-int('1774c',16)+1 == record['body_bytes'] == 236
    assert assessment['result']['callee_Q_returned_as_B'] == 'literal-C-only-under-stated-premises'
    for key in ('caller_P_equals_callee_Q', 'caller_P_equals_returned_B',
                'public_binding', 'actual_ABI_carriers', 'construction_success'):
        assert assessment['result'][key] == 'unknown'
    assert assessment['selected_entries'] == ['0x1774c']
    assert assessment['unread_direct_callees'] == ['0x1b138','0x1ac0c','0x1b058','0x1b0fc']
    assert assessment['unread_named_data'] == ['0x59338','0x59400','0x59460','0x59690']
    assert assessment['signature_mismatch_preserved'] is True
    assert assessment['new_original_calls'] == assessment['new_native_bytes'] == 0
    assert assessment['new_resolved_indirect_sites'] == assessment['new_case_or_grade_changes'] == 0
    assert assessment['coverage'] == 'OPEN-required-unsupported-remains-U'
    assert 'return param_1;' in code.decode() and 'FUN_0001774c(undefined8 *param_1)' in code.decode()
    anchors={'AC01':[2,2],'AC02':[7,12],'AC03':[13,20],'AC04':[21,24],'AC05':[25,25]}
    for claim in assessment['claims']:
        if claim['id'] in anchors:
            assert claim['C_lines'] == anchors[claim['id']]
    assert assessment['residual_frontier']['wrapper_targets_resolved'] == []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    raw=(HERE/'source-record.jsonl').read_bytes()
    code=(HERE/'source.c').read_bytes()
    loc=json.loads((HERE/'source-locator.json').read_bytes())
    ass=json.loads((HERE/'assessment.json').read_bytes())
    validate(raw,code,loc,ass)
    pin_data=json.loads((HERE/'pins.json').read_bytes())
    pins=pin_data['pins']
    for p in pins:
        data=(ROOT/p['path']).read_bytes() if not Path(p['path']).is_absolute() else Path(p['path']).read_bytes()
        assert len(data)==p['bytes'] and sha(data)==p['sha256'], p['path']
        if p['path'] == loc['alias_locator']['path']:
            rows=data.splitlines(keepends=True); a=loc['alias_locator']
            selected=rows[a['row']-1]
            assert sum(map(len,rows[:a['row']-1])) == a['byte_offset']
            assert len(selected)==a['raw_bytes'] and sha(selected)==a['raw_sha256']
            assert json.loads(selected)==a['record'] and a['record']['entry']=='0x1774c'
    c=pin_data['context_record']
    with (ROOT/c['path']).open('rb') as f:
        context=f.read(c['raw_bytes'])
    assert sha(context)==c['raw_sha256'] and json.loads(context)['entry']=='0x15e0'
    controls=[]
    def reject(name, change):
        args=[raw,code,copy.deepcopy(loc),copy.deepcopy(ass)]
        change(args)
        try:
            validate(*args)
        except (AssertionError, ValueError, KeyError):
            controls.append(name)
        else:
            raise AssertionError('negative control accepted: '+name)
    reject('raw byte corruption',lambda a:a.__setitem__(0,raw.replace(b'0x1774c',b'0x1774d',1)))
    reject('C projection truncated',lambda a:a.__setitem__(1,code[:-1]))
    reject('fabricated B=P',lambda a:a[3]['result'].__setitem__('caller_P_equals_returned_B','proved'))
    reject('fabricated Q=P',lambda a:a[3]['result'].__setitem__('caller_P_equals_callee_Q','proved'))
    reject('public binding promotion',lambda a:a[3]['result'].__setitem__('public_binding','proved'))
    reject('ABI by C signature',lambda a:a[3]['result'].__setitem__('actual_ABI_carriers','proved'))
    reject('construction success by return',lambda a:a[3]['result'].__setitem__('construction_success','proved'))
    reject('lost signature mismatch',lambda a:a[3].__setitem__('signature_mismatch_preserved',False))
    reject('omitted unread helper',lambda a:a[3]['unread_direct_callees'].pop())
    reject('invented indirect resolution',lambda a:a[3].__setitem__('new_resolved_indirect_sites',1))
    reject('out-of-scope second entry',lambda a:a[3]['selected_entries'].append('0x1b138'))
    reject('false C anchor',lambda a:a[3]['claims'][4].__setitem__('C_lines',[24,24]))
    reject('invented wrapper target',lambda a:a[3]['residual_frontier']['wrapper_targets_resolved'].append('0x17404'))
    print(json.dumps({'status':'PASS','record_count':1,'raw_bytes':len(raw),'C_bytes':len(code),
                      'C_lines':len(code.splitlines()),'pins_checked':len(pins),
                      'negative_controls_rejected':controls},indent=2))

if __name__ == '__main__':
    main()
