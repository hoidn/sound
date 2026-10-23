#!/usr/bin/env python3
"""Owned packet data only. Never executes an original child or reopens runtime images."""
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('owned_relative_recording',HERE/'run_batch.py')
R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)

def load(name):return json.loads((HERE/name).read_text())
def h(b):return hashlib.sha256(b).hexdigest()
def canonical(d):return json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def historical(data,controls,raw):
    assert len(controls)==18 and len(raw.splitlines())==18
    assert {(c['mode'],c['byte']) for c in controls}=={(m,v) for m in R.MODES for v in R.OLD[m]}
    out={}
    for c in controls:
        b=raw[c['selected_offset']:c['selected_offset']+c['raw_bytes']]
        assert h(b)==c['raw_sha256']
        record=json.loads(b)
        row=next(r for r in data['rows'] if (r['mode'],r['byte'])==(c['mode'],c['byte']))
        assert row['historical']==c['result_locator']
        assert record['argv'][1:]==['call',R.INIT]+R.tokens(row)
        assert record['rc']==0 and record['stderr']=='' and record['timeout'] is False
        calls=[line for line in record['stdout'].splitlines() if line.startswith('call ')]
        assert len(calls)==2 and calls[1].startswith('call 1 '+R.TARGET+' ')
        bits=f'{int(calls[1].split("xmm0=")[1].split()[0],16)&0xffffffff:08x}'
        assert bits==c['bits32']==row['expected_low_xmm0_bits32']
        assert c['original_offset']>=0 and c['original_row']>0
        assert c['historical_pid'] is None and c['historical_utc'] is None
        out[row['id']]={'id':row['id'],'provenance':'inherited-X1','low_xmm0_bits32':bits,
                        'historical_locator':c['result_locator'],'old_raw_original_row':c['original_row'],
                        'old_raw_selected_offset':c['selected_offset'],'raw_sha256':c['raw_sha256'],
                        'actual_child_this_batch':None}
    return out

def check(data,result,controls,oldraw,raw_by_mode):
    R.validate(data)
    assert result['status']=='COMPLETE-ONE-ATTEMPT-PER-MODE' and result['error'] is None
    assert result['phases']==dict.fromkeys(('inputs_validated','custody_before','calls_started','all_children_completed','custody_after'),True)
    assert result['custody_before']==result['custody_after']
    assert len(result['children'])==8 and len({c['pid'] for c in result['children']})==8
    obs=historical(data,controls,oldraw);byid={r['id']:r for r in data['rows']}
    totalcalls=0;totalbuffers=0;uses={}
    for c,p in zip(result['children'],data['plans']):
        assert c['mode']==p['mode'] and c['exit']==0 and c['timeout'] is False and c['status']=='RECORDED'
        assert c['pid']>0 and c['elapsed_seconds']>=0
        assert c['custody_after']==result['custody_before']
        assert c['argv'][2:]==['--imports']+p['tokens']
        out,err=raw_by_mode[p['mode']]
        for key,b in [('stdout',out),('stderr',err)]:
            assert len(b)==c[key]['bytes'] and h(b)==c[key]['sha256']
        parsed=R.parse_output(out.decode(),err.decode(),c['exit'],p,byid)
        assert parsed==c['parsed'] and parsed['oracle_mismatches']==[]
        for k,n in parsed['used'].items():uses[k]=uses.get(k,0)+n
        totalcalls+=len(parsed['calls']);totalbuffers+=len(parsed['buffers'])
        for call,buf in zip(parsed['calls'][1:],parsed['buffers']):
            rid=call['row_id'];assert rid not in obs and byid[rid]['provenance']=='fresh-selected'
            bits=call['low_xmm0_bits32'];value=struct.unpack('<f',bytes.fromhex(bits)[::-1])[0]
            assert math.isfinite(value) and call['oracle_agrees']
            obs[rid]={'id':rid,'provenance':'fresh-selected','mode':c['mode'],'child_pid':c['pid'],
                      'call_index':call['index'],'low_xmm0_bits32':bits,'value':value,
                      'registers_hex':{k:call[k] for k in ('rax','rdx','xmm0','xmm1')},
                      'buffer_after':buf,'oracle_agrees':True}
    assert len(obs)==1024 and totalcalls==1014 and totalbuffers==1006
    assert uses=={k:v*8 for k,v in R.USES.items()}
    return {'logical':1024,'inherited':18,'fresh_targets':1006,'initializers':8,'original_calls':1014,
            'children':8,'fresh_all_finite':True,'fresh_exact_oracle_agreements':1006,
            'inherited_exact_oracle_agreements':18,'used_import_totals':uses,
            'observations':[obs[r['id']] for r in data['rows']]}

def negatives(data,result,controls,oldraw,raw):
    passed=[]
    def test(label,mutate):
        d=copy.deepcopy(data);r=copy.deepcopy(result);c=copy.deepcopy(controls);rr=copy.deepcopy(raw)
        mutate(d,r,c,rr)
        try:check(d,r,c,oldraw,rr)
        except (AssertionError,ValueError,IndexError,KeyError):passed.append(label)
        else:raise AssertionError('negative accepted '+label)
    test('missing-child',lambda d,r,c,b:r['children'].pop())
    test('duplicate-child-pid',lambda d,r,c,b:r['children'][1].update(pid=r['children'][0]['pid']))
    test('timeout',lambda d,r,c,b:r['children'][0].update(timeout=True))
    test('nonzero-exit',lambda d,r,c,b:r['children'][0].update(exit=87))
    test('custody-mismatch',lambda d,r,c,b:r['custody_after'].pop())
    test('wrong-fresh-result',lambda d,r,c,b:r['children'][0]['parsed']['calls'][1].update(low_xmm0_bits32='00000000'))
    test('missing-buffer',lambda d,r,c,b:r['children'][0]['parsed']['buffers'].pop())
    test('wrong-import-count',lambda d,r,c,b:r['children'][0]['parsed']['used'].update(__Znwm=3))
    test('wrong-call-address',lambda d,r,c,b:r['children'][0]['parsed']['calls'][1].update(address='0x0'))
    test('old-control-bit-corruption',lambda d,r,c,b:c[0].update(bits32='00000000'))
    test('invented-historical-pid',lambda d,r,c,b:c[0].update(historical_pid=1))
    test('old-source-offset-corruption',lambda d,r,c,b:c[0].update(selected_offset=1))
    test('raw-stdout-corruption',lambda d,r,c,b:b.__setitem__(1,(b[1][0]+b'\n',b[1][1])))
    test('raw-stderr-not-empty',lambda d,r,c,b:b.__setitem__(1,(b[1][0],b'FAULT\n')))
    # Test parser faults directly, independently of the recorded hash comparisons.
    p=data['plans'][0];byid={r['id']:r for r in data['rows']};text=raw[1][0].decode()
    for label,s in [
        ('parser-missing-final-call','\n'.join(l for l in text.splitlines() if not l.startswith('call 127 '))+'\n'),
        ('parser-extra-import-use',text+'used _malloc 1\n'),
        ('parser-buffer-endian',text.replace('0000a041ffff7f7f010000000000803f','ffffffffffffffffffffffffffffffff')),
        ('parser-unrecognized-event',text+'HIT 0x0\n')]:
        # The selected buffer-pattern mutation must actually change a retained byte string.
        if label=='parser-buffer-endian':
            original=byid[p['row_ids'][0]]['buffer_le'];s=text.replace(original,'f'*32)
        assert s!=text
        try:R.parse_output(s,'',0,p,byid)
        except AssertionError:passed.append(label)
        else:raise AssertionError('parser negative accepted '+label)
    return passed

def main():
    assert sys.argv[1:] in (['--check'],['--write-analysis'])
    data=load('inputs.json');result=load('results.json');controls=load('inherited-controls.json')
    oldraw=(HERE/'historical-controls.jsonl').read_bytes()
    raw={}
    for mode in R.MODES:
        directory=HERE/'attempts'/f'mode-{mode}'
        raw[mode]=((directory/'stdout.txt').read_bytes(),(directory/'stderr.txt').read_bytes())
    output=check(data,result,controls,oldraw,raw)
    negative=negatives(data,result,controls,oldraw,raw)
    freeze=load('manifest-before.json')
    for pin in freeze['frozen_files']:
        p=Path(pin['path']);assert p.is_relative_to(HERE)
        b=p.read_bytes();assert len(b)==pin['bytes'] and h(b)==pin['sha256']
    report={'status':'PASS','counts':{k:v for k,v in output.items() if k!='observations'},
            'input_negative_controls':R.input_controls(data),'recorded_negative_controls':negative,
            'new_original_calls':0,'runtime_image_reads':0,'old_helper_imports':0,
            'observation_canonical_sha256':h(canonical(output['observations']))}
    if sys.argv[1:]==['--write-analysis']:
        R.save(HERE/'observations.json',output['observations']);R.save(HERE/'analysis.json',report)
    else:
        assert load('observations.json')==output['observations'] and load('analysis.json')==report
    print(json.dumps(report))

if __name__=='__main__':main()
