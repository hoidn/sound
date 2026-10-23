#!/usr/bin/env python3
"""Retained packet checks; no runtime/image/provider/original execution or reads."""
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def selected_bits(raw_hex, width):
    assert width in (32, 64)
    return format(int(raw_hex, 16) & ((1 << width) - 1), '0' + str(width // 4) + 'x')


def check():
    config = json.loads((HERE / 'inputs.json').read_text())
    result = json.loads((HERE / 'results.json').read_text())
    assert result['status'] == 'COMPLETE-WHOLE-316-ONE-ATTEMPT-PER-GROUP' and result['error'] is None
    assert result['custody_before'] == result['custody_after'] and len(result['custody_before']) == 31
    for name in ('inputs.json', 'run_batch.py'):
        actual = (HERE / name).read_bytes()
        recorded = next(p for p in result['custody_before'] if p['path'] == str(HERE / name))
        assert len(actual) == recorded['bytes'] and sha(actual) == recorded['sha256']
    assert [r['id'] for r in result['groups']] == [g['id'] for g in config['groups']]
    assert len(result['groups']) == 8
    all_rows, debug_pids, inferior_pids = [], [], []
    warning = b"/usr/bin/gdb: warning: Couldn't determine a path for the index cache directory.\n"
    for g, r in zip(config['groups'], result['groups']):
        assert not r['timeout'] and r['debugger_exit'] == 0
        d = HERE / 'attempts' / r['id']
        assert {f.name for f in d.iterdir()} == {'stdout.txt', 'stderr.txt'}
        for key in ('stdout', 'stderr'):
            raw = (d / (key + '.txt')).read_bytes()
            assert len(raw) == r[key]['bytes'] and sha(raw) == r[key]['sha256']
        assert (d / 'stderr.txt').read_bytes() == warning
        log = (d / 'stdout.txt').read_text()
        normal = re.findall(r'\[Inferior (\d+) \(process (\d+)\) exited normally\]', log)
        assert len(normal) == 1 and int(normal[0][1]) == r['projection']['inferior_pid']
        debug_pids.append(r['debugger_pid'])
        inferior_pids.append(int(normal[0][1]))
        calls = re.findall(r'^call (\d+) (0x[0-9a-f]+) ', log, re.M)
        assert len(calls) == len(g['conversions']) + 1 == g['direct_calls']
        assert [int(i) for i, _ in calls] == list(range(len(calls)))
        assert [a for _, a in calls] == ['0x1014206e0'] + ['0x10151b630'] * len(g['conversions'])
        hits = re.findall(r'^HIT (0x[0-9a-f]+) ([0-9a-f]+)$', log, re.M)
        assert len(hits) == len(g['conversions']) == len(r['projection']['observations'])
        for request, observed, (address, raw) in zip(g['conversions'], r['projection']['observations'], hits):
            assert observed['id'] == request['id'] and observed['type_id'] == request['type_id']
            assert observed['input_bytes_hex'] == request['input_bytes_hex']
            assert address == request['expected_SetValue_stub'] == observed['setter_stub']
            assert raw == observed['raw_unsigned_HIT']
            assert selected_bits(raw, request['width']) == observed['selected_typed_bits_hex']
            selected = int(raw, 16) & ((1 << request['width']) - 1)
            assert bytes.fromhex(observed['selected_typed_bytes_le']) == selected.to_bytes(request['width'] // 8, 'little')
            assert observed['owner_bit_oracle_agreement'] == (observed['selected_typed_bits_hex'] == request['word_hex'])
            assert observed['candidate_grade'] is None
            all_rows.append(observed)
        assert g['owned_buffers'] < 256 and g['direct_calls'] < 256
        used = dict((n, int(v)) for n, v in re.findall(r'^used (\S+) (\d+)$', log, re.M))
        assert used == r['projection']['used_imports']
    assert len(set(debug_pids)) == len(set(inferior_pids)) == 8
    assert len(all_rows) == 316 and len({(r['kind'], r['input_bytes_hex']) for r in all_rows}) == 316
    assert all(r['owner_bit_oracle_agreement'] for r in all_rows)
    # Bit-level controls never cast input or output to host float/NaN.
    assert selected_bits('ffffffffffffffff', 32) == 'ffffffff'
    assert selected_bits('ffffffff', 64) == '00000000ffffffff'
    assert selected_bits('7f800001', 32) != selected_bits('7fc00000', 32)
    assert bytes.fromhex('0100807f') != bytes.fromhex('7f800001')
    assert selected_bits('fff0000000000001', 64) != selected_bits('7ff0000000000001', 64)
    for bad in (0, 16, 128):
        try:
            selected_bits('7f800001', bad)
        except AssertionError:
            pass
        else:
            raise AssertionError('Unknown width accepted')
    return {'status': 'PASS', 'strings': 316, 'words': 158, 'new_strings': 313, 'historical_controls': 3,
            'debugger_invocations': 8, 'normal_inferior_exit_records': 8,
            'original_converter_calls': 316, 'mandatory_recorded_init_calls': 8, 'direct_entry_calls': 324,
            'owner_raw_bit_oracle_agreements': 316, 'mismatches': 0,
            'stderr': '8identical80B GDB index-cache warnings retained; not empty',
            'custody_equal_records': 31, 'author_bit_controls': ['width masking/sign extension', '64bit zero-padding',
                'sNaN payload vs canonical qNaN distinct', 'endian byte order', 'NaN sign distinct', 'unknown widths rejected'],
            'unknowns': 'FP trap/state not observed; SetValue bodies skipped; public node/load/save and ARM/Apple binding not established',
            'new_original_invocations': 0}


if __name__ == '__main__':
    print(json.dumps(check()))
