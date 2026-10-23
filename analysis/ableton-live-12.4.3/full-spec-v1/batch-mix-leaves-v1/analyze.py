"""Extract finite results; compare only declared return fields and exact dumps."""
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools/xexec'))
from xexec import parse

XFADE = {0x101b1a470, 0x101b1a550, 0x101b1a630, 0x101b1a6f0,
         0x101b1a7b0, 0x101b1a880, 0x101b1a8e0}


def fields(call):
    address = call['addr']
    if address in XFADE or address == 0x101b2ba80:
        return {'xmm0_low32': call['xmm0'] & 0xffffffff}
    if address == 0x101b2ba30:
        return {'rax_packed_target_length': call['rax']}
    if address == 0x101b0ee70:
        return {'eax_samples': call['rax'] & 0xffffffff}
    if address == 0x1011f1610:
        return {k: call[k] for k in ['xmm0', 'xmm1']}
    return {}


def main():
    # Floating scalar high lanes and unrelated volatile registers are not returns.
    a = {'addr': 0x101b1a470, 'xmm0': 0x3f800000, 'rax': 1}
    assert fields(a) == fields(a | {'xmm0': 0x123456783f800000, 'rax': 999})
    assert fields(a) != fields(a | {'xmm0': 0x3f800001})
    assert fields({'addr': 0}) == {}
    inputs = json.loads((HERE / 'inputs.json').read_text())
    rows = [json.loads(line) for line in (HERE / 'results.jsonl').read_text().splitlines()]
    assert len(rows) == len(inputs) == 144
    used, calls, dumps, returns, overlap = collections.Counter(), 0, 0, 0, 0
    levels, prior, mismatches = [], {}, []
    for source, row in zip(inputs, rows):
        assert source['id'] == row['id']
        got = parse(row['rc'], row['stdout'], row['stderr'])
        assert got.ok and not row['timeout']
        assert len(got.calls) == source['tokens'].count('call')
        calls += len(got.calls)
        used.update(got.used)
        if 'historical_stdout' in source:
            old = parse(0, source['historical_stdout'], '')
            assert [c['addr'] for c in got.calls] == [c['addr'] for c in old.calls]
            assert len(got.dumps) == len(old.dumps)
            for fresh, previous in zip(got.dumps, old.dumps):
                dumps += 1
                if (fresh[0], fresh[2]) != (previous[0], previous[2]):
                    mismatches.append({'id': source['id'], 'kind': 'exact-dump', 'expr': fresh[0]})
            for fresh, previous in zip(got.calls, old.calls):
                returns += len(fields(fresh))
                if fields(fresh) != fields(previous):
                    mismatches.append({'id': source['id'], 'kind': 'declared-return'})
            if len(got.calls) == 1 and got.calls[0]['addr'] in XFADE:
                position = source['tokens'][2].split(':', 1)[1]
                prior[(got.calls[0]['addr'], float.fromhex(position))] = fields(got.calls[0])['xmm0_low32']
        else:
            for position, call in zip(source['positions_hex'], got.calls):
                bits = call['xmm0'] & 0xffffffff
                key = (call['addr'], float.fromhex(position))
                if key in prior:
                    overlap += 1
                    if prior[key] != bits:
                        mismatches.append({'id': source['id'], 'kind': 'overlap', 'position': position})
                levels.append({'row': row['id'], 'function': hex(call['addr']), 'position_hex': position,
                               'level_binary32_hex': f'{bits:08x}',
                               'level': struct.unpack('<f', struct.pack('<I', bits))[0],
                               'historical_overlap': key in prior, 'grade': 'ungraded-discovery'})
    assert calls == 517 and len(levels) == 301 and overlap == 49
    summary = {'status': 'PASS-finite-replay-agreement' if not mismatches else 'MISMATCH-REVIEW-REQUIRED',
               'processes': len(rows), 'returned_direct_calls': calls, 'exact_dump_comparisons': dumps,
               'declared_scalar_return_field_comparisons': returns, 'historical_mismatches': mismatches,
               'boundary_evaluations': len(levels), 'historical_boundary_overlaps': overlap,
               'new_distinct_boundary_evaluations': len(levels) - overlap,
               'substituted_import_calls': dict(used),
               'negative_finite_boundary_levels': [x for x in levels if x['level'] < 0],
               'tool_source_sha256': hashlib.sha256((ROOT / 'tools/xexec/xexec.py').read_bytes()).hexdigest(),
               'new_behavior_grades': 0,
               'limits': 'Finite original x86 calls with recorded setup/stubs and glibc cos/cosf. No public mix/audio binding, native arm64 execution or unbounded curve law. Unspecified volatile registers are not compared; dumps use exact bytes without address normalization.'}
    for name, value in [('boundary-levels.json', levels), ('analysis.json', summary)]:
        with (HERE / name).open('x') as stream:
            stream.write(json.dumps(value, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
