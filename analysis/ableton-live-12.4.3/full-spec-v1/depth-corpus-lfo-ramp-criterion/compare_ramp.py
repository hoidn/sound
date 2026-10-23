"""Proposed finite Ramp audio criterion; data only, no original-code execution."""
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

FRAMES = 16384
START = 4096
THRESHOLD = 0.01
REFERENCE_SHA256 = '40b77412adfc4768bd18e76e5df330ecd536544c50553212ba3125a8de7982ec'


def decode(data):
    if len(data) != FRAMES * 2 * 4:
        raise ValueError('exactly 16384 interleaved stereo binary32 frames required')
    values = struct.unpack('<32768f', data)
    if not all(math.isfinite(value) for value in values):
        raise ValueError('all samples, including pre-impulse samples, must be finite')
    return values


def compare_bytes(reference, candidate):
    ref, trial = decode(reference), decode(candidate)
    channels = []
    for channel in (0, 1):
        r = ref[START * 2 + channel::2]
        y = trial[START * 2 + channel::2]
        ref_energy = math.fsum(value * value for value in r)
        trial_energy = math.fsum(value * value for value in y)
        if ref_energy <= 0 or trial_energy <= 0:
            raise ValueError('positive post-impulse energy required in each channel')
        error_energy = math.fsum((a - b) * (a - b) for a, b in zip(y, r))
        error = math.sqrt(error_energy / ref_energy)
        channels.append({'channel': channel, 'reference_energy': ref_energy,
                         'candidate_energy': trial_energy, 'error_energy': error_energy,
                         'relative_rms_error': error, 'accepted': error <= THRESHOLD})
    return {'accepted': all(row['accepted'] for row in channels),
            'threshold': THRESHOLD, 'frame_interval_inclusive': [START, FRAMES - 1],
            'channels': channels}


def self_test():
    values = [0.0] * (FRAMES * 2)
    values[START * 2:START * 2 + 2] = [100.0, 100.0]
    ref = struct.pack('<32768f', *values)
    passed = []

    def packed(left=100.0, right=100.0, prefix=None):
        trial = values.copy()
        trial[START * 2:START * 2 + 2] = [left, right]
        if prefix is not None:
            trial[0] = prefix
        return struct.pack('<32768f', *trial)

    def outcome(name, data, expected):
        result = compare_bytes(ref, data)
        assert result['accepted'] is expected, name
        passed.append(name)
        return result

    outcome('identical-reference', ref, True)
    boundary = outcome('inclusive-one-percent-boundary', packed(101.0, 101.0), True)
    assert all(row['relative_rms_error'] == THRESHOLD for row in boundary['channels'])
    bits = struct.unpack('<I', struct.pack('<f', 101.0))[0]
    below = struct.unpack('<f', struct.pack('<I', bits - 1))[0]
    above = struct.unpack('<f', struct.pack('<I', bits + 1))[0]
    outcome('adjacent-below-boundary', packed(below, below), True)
    outcome('adjacent-above-boundary', packed(above, above), False)
    outcome('left-fails-right-passes', packed(above, 100.0), False)
    outcome('right-fails-left-passes', packed(100.0, above), False)
    half_gain = outcome('half-gain', packed(50.0, 50.0), False)
    assert all(row['relative_rms_error'] == 0.5 for row in half_gain['channels'])
    polarity = outcome('polarity-inversion', packed(-100.0, -100.0), False)
    assert all(row['relative_rms_error'] == 2.0 for row in polarity['channels'])
    outcome('finite-prefix-outside-metric', packed(prefix=123.0), True)
    for name, data in [('short', ref[:-4]), ('extra-frame', ref + bytes(8)),
                       ('odd-length', ref[:-1]), ('nonfinite-prefix', packed(prefix=float('nan'))),
                       ('nonfinite-active', packed(float('inf'), 100.0)),
                       ('zero-left-energy', packed(0.0, 100.0)),
                       ('zero-right-energy', packed(100.0, 0.0)),
                       ('both-silent', bytes(len(ref)))]:
        try:
            compare_bytes(ref, data)
        except ValueError:
            passed.append(name)
        else:
            raise AssertionError('invalid candidate admitted: ' + name)
    for name, bad_ref in [('zero-reference', bytes(len(ref))),
                          ('nonfinite-reference', packed(prefix=float('nan')))]:
        try:
            compare_bytes(bad_ref, ref)
        except ValueError:
            passed.append(name)
        else:
            raise AssertionError('invalid reference admitted: ' + name)
    return passed


def main():
    if sys.argv[1:] == ['--self-test']:
        checks = self_test()
        print(json.dumps({'status': 'pass', 'checks': checks, 'writes': False}))
        return 0
    if len(sys.argv) != 3 or any(arg.startswith('--') for arg in sys.argv[1:]):
        print('usage: compare_ramp.py REFERENCE.f32 CANDIDATE.f32 | --self-test', file=sys.stderr)
        return 2
    try:
        reference = Path(sys.argv[1]).read_bytes()
        if hashlib.sha256(reference).hexdigest() != REFERENCE_SHA256:
            raise ValueError('reference must be the pinned finite Ramp capture')
        result = compare_bytes(reference, Path(sys.argv[2]).read_bytes())
    except (OSError, ValueError) as error:
        print(json.dumps({'status': 'invalid', 'error': str(error)}))
        return 2
    print(json.dumps(result, allow_nan=False))
    return 0 if result['accepted'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
