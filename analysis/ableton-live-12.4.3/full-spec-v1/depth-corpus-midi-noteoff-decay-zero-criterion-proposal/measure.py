"""Proposed finite B waveform measurement. Stdlib/data only; never invokes device code."""
from pathlib import Path
import hashlib
import json
import math
import struct
import sys

HERE = Path(__file__).resolve().parent
FRAMES = 16384
START = 4096
LIMIT = 0.01
B_SHA256 = 'a378ac6de6c04041a21aee501094be643fdb6615d3fc212ebbcc32afdf76d829'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    if len(data) != FRAMES * 8:
        raise ValueError('Exactly 16384 stereo interleaved little-endian binary32 frames required')
    values = struct.unpack('<32768f', data)
    if not all(math.isfinite(v) for v in values):
        raise ValueError('Nonfinite sample anywhere in full file')
    return values


def trusted_reference(data):
    if sha(data) != B_SHA256:
        raise ValueError('Reference is not the pinned host34-zero B capture')


def compare_bytes(reference, candidate):
    """Pure arithmetic for synthetic controls; caller must separately bind reference identity."""
    ref, trial = decode(reference), decode(candidate)
    rows = []
    for channel in (0, 1):
        r, y = ref[2 * START + channel::2], trial[2 * START + channel::2]
        ref_energy = math.fsum(v * v for v in r)
        candidate_energy = math.fsum(v * v for v in y)
        if ref_energy <= 0 or candidate_energy <= 0:
            raise ValueError('Positive post4096 reference and candidate energy required in each channel')
        error_energy = math.fsum((a - b) * (a - b) for a, b in zip(y, r))
        error = math.sqrt(error_energy / ref_energy)
        rows.append(dict(channel=channel, reference_energy=ref_energy,
                         candidate_energy=candidate_energy, error_energy=error_energy,
                         relative_rms=error, proposed_acceptance=error <= LIMIT))
    return dict(proposed_acceptance=all(r['proposed_acceptance'] for r in rows),
                threshold=LIMIT, scored_frames_inclusive=[START, FRAMES - 1], channels=rows)


def self_tests():
    values = [0.0] * (FRAMES * 2)
    values[START * 2:START * 2 + 2] = [100.0, 100.0]
    reference = struct.pack('<32768f', *values)
    passed = []

    def packed(left=100.0, right=100.0, at=None, value=0.0):
        trial = values.copy()
        trial[START * 2:START * 2 + 2] = [left, right]
        if at is not None:
            trial[at] = value
        return struct.pack('<32768f', *trial)

    def outcome(name, data, expected, ref=reference):
        result = compare_bytes(ref, data)
        assert result['proposed_acceptance'] is expected, name
        passed.append(name)
        return result

    def invalid(name, ref, data):
        try:
            compare_bytes(ref, data)
        except ValueError:
            passed.append(name)
        else:
            raise AssertionError(name)

    outcome('identical', reference, True)
    boundary = outcome('inclusive-1pct', packed(101.0, 101.0), True)
    assert all(r['relative_rms'] == LIMIT for r in boundary['channels'])
    bits = struct.unpack('<I', struct.pack('<f', 101.0))[0]
    low, high = [struct.unpack('<f', struct.pack('<I', bits + step))[0] for step in (-1, 1)]
    outcome('adjacent-below', packed(low, low), True)
    outcome('adjacent-above', packed(high, high), False)
    outcome('left-only-fails', packed(high, 100.0), False)
    outcome('right-only-fails', packed(100.0, high), False)
    assert all(r['relative_rms'] == 0.5 for r in outcome('half-gain', packed(50.0, 50.0), False)['channels'])
    assert all(r['relative_rms'] == 2.0 for r in outcome('polarity', packed(-100.0, -100.0), False)['channels'])
    outcome('last-prefix-frame-finite-only', packed(at=START * 2 - 1, value=123.0), True)
    outcome('last-scored-frame-included', packed(at=FRAMES * 2 - 1, value=2.0), False)
    for name, data in [('short', reference[:-4]), ('extra', reference + bytes(8)),
                       ('odd', reference[:-1]),
                       ('prefix-NaN', packed(at=0, value=math.nan)),
                       ('scored-Inf', packed(math.inf)),
                       ('left-zero', packed(0.0, 100.0)), ('right-zero', packed(100.0, 0.0)),
                       ('both-zero', bytes(len(reference)))]:
        invalid(name, reference, data)
    invalid('reference-zero', bytes(len(reference)), reference)
    invalid('reference-nonfinite', packed(at=0, value=math.nan), reference)
    try:
        trusted_reference(reference)
    except ValueError:
        passed.append('wrong-reference-identity')
    else:
        raise AssertionError('Synthetic reference passed actual B identity gate')
    return passed


def check():
    inputs = json.loads((HERE / 'inputs.json').read_text())
    frozen = HERE / 'manifest.json'
    if frozen.exists():
        manifest = json.loads(frozen.read_text())
        assert {r['path'] for r in manifest['files']} == {p.name for p in HERE.iterdir() if p.is_file() and p != frozen}
        for r in manifest['files']:
            raw = (HERE / r['path']).read_bytes()
            assert len(raw) == r['bytes'] and sha(raw) == r['sha256']
    watched = {p: p.read_bytes() for p in HERE.iterdir() if p.is_file()}
    providers = {}
    for pin in inputs['pins']:
        p = Path(pin['path']); raw = p.read_bytes()
        assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256']
        watched[p] = raw
        providers[pin['role']] = raw
    for role in ('new_capture_manifest', 'old_capture_manifest'):
        seal_pin = next(p for p in inputs['pins'] if p['role'] == role)
        parent = Path(seal_pin['path']).parent
        for pin in json.loads(providers[role])['files']:
            p = parent / pin['path']; raw = p.read_bytes()
            assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256']
            watched[p] = raw
    ref = providers['B_reference']
    trusted_reference(ref)
    new_script, old_script = providers['B_script'].decode(), providers['old_B_script'].decode()
    assert new_script.replace('param 34 0.0\n', 'param 34 1.0\n') == old_script
    criteria = json.loads((HERE / 'criterion.json').read_text())
    assert criteria['metric_kind_proposed'] == 'noteoff_decay_zero_waveform'
    assert criteria['threshold'] == LIMIT and criteria['reference_sha256'] == B_SHA256
    comparisons = {name: compare_bytes(ref, providers[role]) for name, role in [
        ('B-self', 'B_reference'), ('wrong-fresh-A-held', 'A_control'),
        ('wrong-fresh-C-gate0-off', 'C_control'), ('wrong-old-host34-one-B', 'old_B_control')]}
    tail_zero = list(decode(ref))
    tail_zero[8192 * 2:] = [0.0] * (8192 * 2)
    scope_control = compare_bytes(ref, struct.pack('<32768f', *tail_zero))
    raw_controls = {r: providers[r] for r in ('A_control', 'C_control', 'old_B_control')}
    pair_equalities = []
    roles = list(raw_controls)
    for i, left in enumerate(roles):
        for right in roles[i + 1:]:
            a, b = raw_controls[left], raw_controls[right]
            pair_equalities.append(dict(left=left, right=right, full_file_equal=a == b,
                                        scored_bytes_equal=a[START * 8:] == b[START * 8:]))
    assert comparisons['B-self']['proposed_acceptance']
    checks = self_tests()
    result = dict(status='PROPOSAL measurement only; no criterion/capture adoption',
                  metric_kind_proposed=criteria['metric_kind_proposed'], comparisons=comparisons,
                  deliberately_zeroed_last8192_scope_control=scope_control,
                  controls_pair_identity=pair_equalities, mathematical_self_tests=checks,
                  control_count_not_independence_claim=True, fitting=False,
                  prefix_finite_only=True, new_native_calls=0, new_normative_cases=0, grade=None)
    if (HERE / 'results.json').exists():
        assert json.loads((HERE / 'results.json').read_text()) == result
    for p, raw in watched.items():
        assert p.read_bytes() == raw
    return result


def main():
    if sys.argv[1:] == ['--self-test']:
        print(json.dumps(dict(tests=self_tests(), writes=False), indent=2))
        return 0
    if sys.argv[1:] != ['--check']:
        print('Read-only --check or --self-test only; no old tool or device invocation.', file=sys.stderr)
        return 2
    print(json.dumps(check(), indent=2, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
