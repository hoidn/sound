#!/usr/bin/env python3
"""Retained binary64 return DATA only. No originals, provider, old helper/model or native-source imports."""
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

HERE = Path(__file__).resolve().parent
TARGET = '0x10235b910'

def classify(bits):
    assert len(bits) == 16
    n = int(bits, 16)
    sign, exponent, fraction = n >> 63, (n >> 52) & 2047, n & ((1 << 52) - 1)
    category = ('negative-' if sign else 'positive-')
    if exponent == 2047:
        category += 'qNaN' if fraction and (fraction >> 51) else 'sNaN' if fraction else 'infinity'
        numeric_hex = None
    else:
        category += 'zero' if exponent == 0 and fraction == 0 else 'subnormal' if exponent == 0 else 'normal'
        numeric_hex = struct.unpack('>d', bytes.fromhex(bits))[0].hex()
    return {'binary64_hex': bits, 'bytes_le_hex': bytes.fromhex(bits)[::-1].hex(), 'classification': category, 'finite_value_hex': numeric_hex}

def parse(out, err, rc):
    assert rc == 0 and err == ''
    assert not re.search(r'(?m)^(TRAP|FAULT|HIT|xexec:|used|out|dump|poke) ', out + err)
    calls = re.findall(r'^call (\d+) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)$', out, re.M)
    assert len(calls) == 1 and calls[0][:2] == ('0', TARGET)
    registers = {k: f'{int(v, 16):016x}' for k, v in zip(('rax', 'rdx', 'xmm0', 'xmm1'), calls[0][2:])}
    imports = re.findall(r'^import (\S+) (\S+) slots=(\d+)$', out, re.M)
    assert len(imports) == 1882 and len({name for kind, name, slots in imports}) == 1882
    return registers, {kind: sum(k == kind for k, name, slots in imports) for kind in {x[0] for x in imports}}

def controls():
    results = []
    assert classify('0000000000000000')['classification'] == 'positive-zero'
    assert classify('8000000000000000')['classification'] == 'negative-zero'
    assert classify('0000000000000001')['classification'] == 'positive-subnormal'
    assert classify('7ff0000000000000')['classification'] == 'positive-infinity'
    assert classify('7ff8000000000000')['classification'] == 'positive-qNaN'
    assert classify('fff8000000000000')['classification'] == 'negative-qNaN'
    results += ['signed-zero identity', 'subnormal retained', 'infinity distinct from NaN', 'exact qNaN signs/payload identities']
    for bad in ('', '0', 'not-binary64'):
        try:
            classify(bad)
        except (AssertionError, ValueError):
            results.append('reject invalid bitwidth/encoding ' + repr(bad))
        else:
            raise AssertionError('bad bits accepted')
    return results

def derive():
    inputs = json.loads((HERE / 'inputs.json').read_text())
    result = json.loads((HERE / 'results.json').read_text())
    assert result['status'] == 'COMPLETE-117-ONE-ATTEMPT-EACH' and result['error'] is None
    assert len(result['children']) == len(inputs['rows']) == 117
    assert [r['id'] for r in result['children']] == [r['id'] for r in inputs['rows']]
    assert result['custody_before'] == result['custody_after']
    rows = []
    for selected, child in zip(inputs['rows'], result['children']):
        assert child['exit'] == 0 and not child['timeout']
        directory = HERE / 'attempts' / child['id']
        assert {p.name for p in directory.iterdir()} == {'stdout.txt', 'stderr.txt'}
        for key, name in [('stdout', 'stdout.txt'), ('stderr', 'stderr.txt')]:
            data = (directory / name).read_bytes()
            assert len(data) == child[key]['bytes'] and hashlib.sha256(data).hexdigest() == child[key]['sha256']
        registers, bindings = parse((directory / 'stdout.txt').read_text(), (directory / 'stderr.txt').read_text(), child['exit'])
        assert registers == child['return_registers_hex']
        projected = registers['xmm0']
        expected = selected['expected_output_binary64_hex']
        assert child['projected_binary64_hex'] == projected
        match = None if expected is None else projected == expected
        assert match == child['control_match'] and match is not False
        rows.append({'id': selected['id'], 'input': classify(selected['input_binary64_hex']), 'classes': selected['classes'], 'actual_return': classify(projected), 'historical_expected_output_binary64_hex': expected, 'historical_control_match': match, 'new_input_expected_value': None, 'new_behavior_grade': None, 'import_binding_classes': bindings, 'called_imports': {}, 'source_result': 'results.json#/children/' + str(len(rows))})
    return {'schema': 'playback-quantization-finite-observations-v1', 'status': 'PENDING-ONE-INDEPENDENT-BATCH-REVIEW', 'scope': 'Supplied one-double x86 helper only; no receiver, initializer, patches or public input/file-position/audio/clock/ARM/Apple equivalence. New109 inputs are discovery with NULL prior expectations; exact117 returns retained for later finite owner adoption, not a general quantizer or input-admission law.', 'summary': {'children': 117, 'calls': 117, 'historical_controls_agree': 8, 'new_discovery_pairs': 109, 'new_expected_values_predeclared': 0, 'input_unique_bitpatterns': 117, 'output_finite': sum('NaN' not in r['actual_return']['classification'] and 'infinity' not in r['actual_return']['classification'] for r in rows), 'output_nonfinite': sum('NaN' in r['actual_return']['classification'] or 'infinity' in r['actual_return']['classification'] for r in rows), 'timeouts': 0, 'nonzero_exits': 0, 'called_imports': 0}, 'controls': controls(), 'rows': rows, 'FP_and_parser_limit': 'Allstrtod argument tokens checked in host libc against exactdeclaredbits, but no childprocess input-register/FPflags trace. Existing loader temporaryfloatcast may affect FPflags; nonfinite/overflow probes are localFPdiscovery, not publicadmission or ARMexpectations. No model/oracle repaired/fit to outputs.'}

if __name__ == '__main__':
    assert sys.argv[1:] in (['--write'], ['--check'])
    d = derive()
    if sys.argv[1] == '--write':
        assert not (HERE / 'observations.json').exists()
        (HERE / 'observations.json').write_text(json.dumps(d, indent=2, allow_nan=False) + '\n')
    else:
        assert json.loads((HERE / 'observations.json').read_text()) == d
    print(json.dumps({'status': 'PASS', 'summary': d['summary'], 'controls': d['controls'], 'new_original_calls': 0}))
