#!/usr/bin/env python3
"""Structural input-union/result checks, synthetic DATA controls; no original/provider/model execution."""
import collections
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def bits(x):
    return struct.pack('>d', x).hex()

def union(historical):
    values = set()
    def triple(x):
        values.update(bits(v) for v in (math.nextafter(x, -math.inf), x, math.nextafter(x, math.inf)))
    for r in historical:
        values.add(bits(float(r['x'])))
    indices = {math.floor(abs(float(r['x'])) * 2**24) for r in historical}
    for k in indices:
        for sign in (-1, 1):
            triple(sign * math.ldexp(k + 0.5, -24))
            triple(sign * math.ldexp(float(k), -24))
    for x in (0.0, -0.0, 2**-24, 2**-1022, 2.0**28, 2.0**29, math.ldexp(sys.float_info.max, -24), sys.float_info.max):
        for sign in (-1, 1):
            triple(math.copysign(x, sign))
    values.update(('7ff0000000000000', 'fff0000000000000', '7ff8000000000000', 'fff8000000000000'))
    return values

def validate(inputs, result, historical):
    rows, children = inputs['rows'], result['children']
    assert len(rows) == 117 and len({r['id'] for r in rows}) == 117
    assert {r['input_binary64_hex'] for r in rows} == union(historical)
    assert len({r['input_binary64_hex'] for r in rows}) == 117
    assert sum(r['expected_output_binary64_hex'] is not None for r in rows) == 8
    for i, r in enumerate(rows[:8]):
        assert r['input_binary64_hex'] == bits(float(historical[i]['x']))
        assert r['expected_output_binary64_hex'] == bits(float(historical[i]['y']))
        assert r['historical_source']['pointer'] == f'/{i}'
    assert all(r['expected_output_binary64_hex'] is None for r in rows[8:])
    assert result['status'] == 'COMPLETE-117-ONE-ATTEMPT-EACH' and result['error'] is None
    assert result['custody_before'] == result['custody_after'] and len(result['custody_before']) == 22
    assert len(children) == 117 and len({c['pid'] for c in children}) == 117
    assert [r['id'] for r in rows] == [c['id'] for c in children]
    assert len(result['strtod_argument_bits']) == 117
    for row, parser, child in zip(rows, result['strtod_argument_bits'], children):
        assert parser['parsed_binary64_hex'] == row['input_binary64_hex'] and parser['token'] == row['token']
        assert child['exit'] == 0 and child['timeout'] is False and child['stderr']['bytes'] == 0
        assert child['argv'][-4:] == ['--imports', 'call', '0x10235b910', row['token']]
        assert len(child['argv']) == 6
        assert child['control_match'] == (None if row['expected_output_binary64_hex'] is None else child['projected_binary64_hex'] == row['expected_output_binary64_hex'])
        assert child['control_match'] is not False
        assert child['projected_binary64_hex'] == child['return_registers_hex']['xmm0']
        assert bytes.fromhex(row['input_binary64_hex'])[::-1].hex() == row['input_bytes_le_hex']
    return True

def main():
    inputs = json.loads((HERE / 'inputs.json').read_text())
    result = json.loads((HERE / 'results.json').read_text())
    historical = json.loads((ROOT / 'analysis/ableton-live-12.4.3/r2/t13-playback-v1/audio/results/quant.json').read_text())
    validate(inputs, result, historical)
    changes = [
        ('one new input omitted', lambda a, b: a['rows'].pop()),
        ('boundary replaced while count117', lambda a, b: a['rows'][8].update(input_binary64_hex='3fd0000000000000')),
        ('oldcontrol expectation changed', lambda a, b: a['rows'][0].update(expected_output_binary64_hex='8000000000000000')),
        ('newNULL filled after observation', lambda a, b: a['rows'][8].update(expected_output_binary64_hex=b['children'][8]['projected_binary64_hex'])),
        ('one child omitted', lambda a, b: b['children'].pop()),
        ('nonzero exit', lambda a, b: b['children'][0].update(exit=87)),
        ('timeout', lambda a, b: b['children'][0].update(timeout=True)),
        ('parser negativezero sign lost', lambda a, b: next(x for x in b['strtod_argument_bits'] if x['parsed_binary64_hex'] == '8000000000000000').update(parsed_binary64_hex='0000000000000000')),
        ('unexpected thirdparty target', lambda a, b: b['children'][0]['argv'].__setitem__(-2, '0x0')),
        ('custody change', lambda a, b: b['custody_after'][0].update(sha256='0' * 64)),
        ('declared endian reversal lost', lambda a, b: a['rows'][1].update(input_bytes_le_hex=a['rows'][1]['input_binary64_hex']))]
    rejected = []
    for name, mutate in changes:
        a, b = copy.deepcopy((inputs, result))
        mutate(a, b)
        try:
            validate(a, b, historical)
        except (AssertionError, StopIteration):
            rejected.append(name)
        else:
            raise AssertionError('False promotion accepted: ' + name)
    print(json.dumps({'status': 'PASS', 'complete_union': 117, 'controls': 8, 'new_prior_NULL': 109, 'source_input_census_all': 8, 'negative_controls': rejected, 'original_calls': 0, 'binary_reads': 0, 'model_comparator_runs': 0}))

if __name__ == '__main__':
    main()
