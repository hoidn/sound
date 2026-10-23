"""Read fixed captured bytes only; descriptive differences, no acceptance decision."""
from pathlib import Path
import hashlib, json, math, struct

HERE = Path(__file__).resolve().parent

def read(path):
    raw = path.read_bytes()
    assert len(raw) == 131072
    values = list(struct.iter_unpack('<ff', raw))
    assert all(math.isfinite(v) for frame in values for v in frame)
    return raw, values

def stats(a, b):
    energy = math.fsum(v*v for v in a)
    difference = math.fsum((v-w)**2 for v, w in zip(a, b))
    return {'differing_samples': sum(v != w for v, w in zip(a, b)),
            'max_abs_difference': max(abs(v-w) for v, w in zip(a, b)),
            'relative_rms_to_first': math.sqrt(difference/energy) if energy else None}

assert stats([1., 0.], [0., 0.]) == {'differing_samples': 1, 'max_abs_difference': 1., 'relative_rms_to_first': 1.}
assert stats([0.], [0.])['relative_rms_to_first'] is None
paths = {'A': HERE/'raw/gate1-held.f32', 'B': HERE/'raw/gate1-off.f32',
         'C': HERE/'raw/gate0-off.f32',
         'old_A': HERE.parent/'depth-corpus-midi-gate-release/raw/gate1-held.f32',
         'old_held0': HERE.parent/'depth-corpus-midi-pitch/raw/note60.f32'}
data = {name: read(path) for name, path in paths.items()}
rows = []
for first, second in [('A', 'B'), ('A', 'old_A'), ('C', 'old_held0')]:
    for channel in (0, 1):
        for start, end in [(0, 3072), (3072, 4096), (4096, 8192), (8192, 16384)]:
            a = [v[channel] for v in data[first][1][start:end]]
            b = [v[channel] for v in data[second][1][start:end]]
            rows.append({'first': first, 'second': second, 'channel': channel,
                         'start': start, 'end_exclusive': end, **stats(a, b)})
print(json.dumps({'scope': 'Fixed-window descriptive data only; host command block boundary3072 is not proven internal onset. No normalization, fit, FFT, criterion, grade or native call.',
    'inputs': {name: {'path': str(paths[name]), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()} for name, (raw, _) in data.items()},
    'full_byte_equal': {a+'__'+b: data[a][0] == data[b][0] for a, b in [('A', 'B'), ('A', 'old_A'), ('C', 'old_held0')]},
    'all_post4096_equal_old_held0': all(data[name][0][4096*8:] == data['old_held0'][0][4096*8:] for name in ['A', 'B', 'C']),
    'rows': rows}, indent=2, allow_nan=False))
