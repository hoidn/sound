"""Data-only description of two retained captures; no fit, threshold or grade."""
from pathlib import Path
import hashlib
import json
import math
import struct

BASE = Path(__file__).resolve().parent


def energy(values):
    return math.fsum(float(v) * float(v) for v in values)


def compare(a, b):
    assert len(a) == len(b)
    changed = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return {'different_numeric_samples': len(changed),
            'first_different_local_frame': changed[0] if changed else None,
            'last_different_local_frame': changed[-1] if changed else None,
            'squared_difference_sum': energy([float(y) - float(x) for x, y in zip(a, b)])}


assert energy([0., 1., -2.]) == 5.
assert compare([0., 1.], [0., 2.]) == {
    'different_numeric_samples': 1, 'first_different_local_frame': 1,
    'last_different_local_frame': 1, 'squared_difference_sum': 1.}
assert compare([1.], [1.])['first_different_local_frame'] is None

raw = {}
channels = {}
for name in ['control', 'left-step']:
    data = (BASE / 'raw' / (name + '.f32')).read_bytes()
    assert len(data) == 131072
    frames = list(struct.iter_unpack('<ff', data))
    assert all(math.isfinite(v) for frame in frames for v in frame)
    raw[name] = data
    channels[name] = [[frame[c] for frame in frames] for c in range(2)]

windows = [(0, 4096), (4096, 8192), (8192, 16384)]
windows += [(start, start + 512) for start in range(8192, 16384, 512)]
rows = []
for start, end in windows:
    for c, label in enumerate(['L', 'R']):
        a = channels['control'][c][start:end]
        b = channels['left-step'][c][start:end]
        row = {'start_frame_inclusive': start, 'end_frame_exclusive': end,
               'channel': label, 'control_energy': energy(a), 'step_energy': energy(b),
               **compare(a, b)}
        row['all_channel_sample_bits_equal'] = all(
            raw['control'][8 * i + 4 * c:8 * i + 4 * c + 4] ==
            raw['left-step'][8 * i + 4 * c:8 * i + 4 * c + 4]
            for i in range(start, end))
        rows.append(row)

result = {'format': 'little-endian binary32 stereo; f32 decoded to Python binary64',
          'method': 'Fixed windows; fsum of binary64 squares/differences. No FFT/model/fit/epsilon.',
          'inputs': {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                     for name, data in raw.items()},
          'rows': rows, 'criterion': None, 'grade': None,
          'limits': 'Finite capture observations only. No smoothing duration, right-invariance law, A1, Live or candidate claim.'}
with (BASE / 'fixed-window-description.json').open('x') as f:
    f.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
print(json.dumps({'rows': len(rows), 'main_windows': rows[:6]}, indent=2))
