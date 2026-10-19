"""Measure every retained Tension render (raw/*.wav): timing, level, partials, filter and body responses.

    python3 -I analyze_tension.py > results/analyze.txt     # also writes results/measure.json

Windows: "held" is from the first non-zero frame + 2,048 to the note-off frame; "release" is from the
note-off frame + 882 (20 ms) to the end. Partials come from measure.modes. Filter cases are compared
with filt_base (the same note with the filter off) by measure.transfer; body cases with defaults_44
by third-octave levels. Dependencies: numpy, scipy, the retained renders.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402

import cases  # noqa: E402
import measure as M  # noqa: E402
from run_tension import load  # noqa: E402

STD_HZ = [65.4, 130.8, 261.6, 523.3, 1046.5, 2093.0, 4186.0, 8372.0, 12000.0]


def f0_expected(c):
    h = cases.host(c)
    semis = c['note'] + 12 * (h[3] - 3) + (h[4] - 12) + 100 * (h[5] - 0.5) / 100
    return 440 * 2 ** ((semis - 69) / 12)


def basic(c, x):
    fs = c['fs']
    on = M.onset(x)
    d = dict(first_nonzero=on, first_above_1e6=M.onset(x, 1e-6), last_nonzero=M.last(x), peak=float(np.abs(x).max()),
             clipped_at_4=bool(np.abs(x).max() >= 3.999), f0_expected_hz=f0_expected(c))
    end = d['last_nonzero']
    if end is not None and end < len(x) - 1:
        d['max_abs_10ms_before_end'] = float(np.abs(x[max(0, end - fs // 100):end + 1]).max())
    if on is None:
        return d
    a, b = on + 2048, c['off']
    d['rms_held'] = float(np.sqrt((x[a:b] ** 2).mean()))
    d['env_db_50ms'] = [round(float(20 * np.log10(np.sqrt((x[k:k + fs // 20] ** 2).mean()) + 1e-30)), 2) for k in range(0, len(x), fs // 20)]
    d['held'] = M.modes(x, d['f0_expected_hz'], a, b, fs)
    d['release'] = M.modes(x, d['f0_expected_hz'], c['off'] + 882, len(x), fs)
    d['third_octave_held_db'] = M.third_octave(x, a, b, fs)
    return d


def filter_response(x, base, c):
    on = M.onset(base)
    f, h = M.transfer(x, base, on + 2048, c['off'], c['fs'])
    db = 20 * np.log10(np.abs(h))
    std = {f'{q:g}': round(float(db[np.argmin(abs(f - q))]), 2) for q in STD_HZ}
    below3 = np.nonzero(db < -3)[0]
    return dict(n_partials=len(f), max_hz=float(f.max()), at_std_hz_db=std, peak_db=float(db.max()), peak_hz=float(f[np.argmax(db)]),
                first_below_minus3db_hz=float(f[below3[0]]) if len(below3) else None,
                partials_hz=[round(float(v), 3) for v in f], gain_db=[round(float(v), 3) for v in db],
                phase_rad=[round(float(v), 4) for v in np.angle(h)])


def show(name, d):
    held = d.get('held', {}).get('partials', [])
    rel = d.get('release', {}).get('partials', [])
    p = ' '.join(f"{m['k']}:{m['hz']:.3f}/{(m['t60_s'] or 0):.3f}s/{m['level_db']:.1f}" for m in held[:6])
    r = ' '.join(f"{m['k']}:{(m['t60_s'] or 0):.3f}" for m in rel[:4])
    B = d.get('held', {}).get('B')
    print(f"{name:20s} on {d['first_nonzero']} pk {d['peak']:.4f} last {d['last_nonzero']} rms {d.get('rms_held', 0):.4e} "
          f"B {B if B is None else round(B, 6)} | {p} | rel {r}")


def main():
    out = {}
    ref = {n: load(n)[:, 0] for n in cases.CASES}
    for name, c in cases.CASES.items():
        x = ref[name]
        d = basic(c, x)
        if c['group'] == 'F' and name != 'filt_base':
            d['filter'] = filter_response(x, ref['filt_base'], c)
        if c['group'] == 'B':
            on = M.onset(x)
            d['body_minus_dry_third_octave_db'] = [round(a - b, 2) for a, b in zip(M.third_octave(x, on + 2048, c['off'], c['fs']),
                                                                               M.third_octave(ref['defaults_44'], on + 2048, c['off'], c['fs']))]
        out[name] = d
        show(name, d)
        if 'filter' in d:
            fr = d['filter']
            print('   filter', fr['at_std_hz_db'], 'peak', round(fr['peak_db'], 2), '@', round(fr['peak_hz'], 1), '-3dB@', fr['first_below_minus3db_hz'])
        if 'body_minus_dry_third_octave_db' in d:
            print('   body-dry 1/3 oct (50 Hz..16 kHz)', d['body_minus_dry_third_octave_db'])
    (HERE / 'results' / 'measure.json').write_text(json.dumps(out, indent=1, default=lambda v: None))


if __name__ == '__main__':
    main()
