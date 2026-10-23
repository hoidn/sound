"""Optional stdout-only descriptive comparison, never a collector or acceptance test."""
from pathlib import Path
import hashlib, json, math, struct, sys

def audio(path, pin=None):
    b = path.read_bytes()
    if pin is not None:
        assert len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256']
    assert len(b) == 131072
    x = list(struct.iter_unpack('<ff', b))
    assert all(math.isfinite(v) for f in x for v in f)
    return b, x

def main():
    if len(sys.argv) != 3 or sys.argv[1] != '--describe':
        raise SystemExit('Read-only --describe EXACT_FINAL_CAPTURE_DIRECTORY only; no capture or fit.')
    dest = Path(sys.argv[2]).resolve()
    proposal = json.loads((Path(__file__).resolve().parent / 'proposal.json').read_text())
    assert dest == Path(proposal['final_directory'])
    results = json.loads((dest / 'results.json').read_text())
    assert results['all3_structurally_valid'] and [r['name'] for r in results['runs']] == proposal['run_order']
    channels, data = {}, {}
    for r in results['runs']:
        name = r['name']
        b, data[name] = audio(dest / 'raw' / (name + '.f32'), r['output'])
        channels[name] = {'sha256': hashlib.sha256(b).hexdigest(), 'historical': False}
    pin = proposal['source_pins']['historical_reference']
    b, data['historical-gate0-held'] = audio(Path(pin['path']), pin)
    channels['historical-gate0-held'] = {'sha256': hashlib.sha256(b).hexdigest(), 'historical': True}
    windows = [('prefix', 0, 4096), ('pre_off_command_block', 4096, 8192), ('later_command_block_onward', 8192, 16384)]
    energies = []
    for name, x in data.items():
        for label, a, z in windows:
            for c in (0, 1):
                v = [f[c] for f in x[a:z]]
                energies.append({'name': name, 'window': label, 'frames_half_open': [a, z], 'channel': c,
                                 'mean_square': math.fsum(t*t for t in v)/len(v),
                                 'peak': max(map(abs, v)), 'nonzero': sum(t != 0 for t in v)})
    pairs = [('gate1-held', 'historical-gate0-held'), ('gate1-off', 'gate1-held'),
             ('gate0-off', 'historical-gate0-held'), ('gate1-off', 'gate0-off')]
    differences = []
    for left, right in pairs:
        for label, a, z in windows:
            for c in (0, 1):
                d = [data[left][i][c] - data[right][i][c] for i in range(a, z)]
                differences.append({'left': left, 'right': right, 'window': label, 'channel': c,
                                    'different_samples': sum(t != 0 for t in d), 'max_abs_difference': max(map(abs, d)),
                                    'rms_difference': math.sqrt(math.fsum(t*t for t in d)/len(d))})
    print(json.dumps({'status': 'Descriptive only; no tolerance, pass/fail, silence/release curve or MIDI law inferred.',
          'window_caveat': '8192 is the host command block start, NOT a proved device release onset. Event is host8193/local1; admission/update latency unknown.',
          'historical_control_caveat': 'Separate older process/time, not a new matched recapture.',
          'sources': channels, 'energies': energies, 'differences': differences,
          'criterion': None, 'application_grade': None}, indent=2, allow_nan=False))

if __name__ == '__main__': main()
