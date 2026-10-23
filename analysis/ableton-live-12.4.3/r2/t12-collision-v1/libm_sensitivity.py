"""Sensitivity of the Collision renders to the substituted libm: every inexact libm result one ulp up
(XDEV_LIBM_ULP=+1) and one ulp down (-1); floor, modf, ldexp, fabs and sqrt stay exact.

    python3 -I libm_sensitivity.py   # writes results/libm_sensitivity.json (renders in /var/tmp)

Per case: waveform rel RMS over the first 256 frames and over the whole render against the
unperturbed render, and the largest shift of a graded mode's frequency, in the spec's ulp bounds.
Dependencies: numpy, scipy, run_collision.py.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402

import fit  # noqa: E402
import run_collision as rc  # noqa: E402
from col import FS, P, PRESET, note  # noqa: E402

CASES = [('beam_high', dict(Resonator1__Type=0, Resonator1__Quality=3, Resonator1__Decay=0.75), 60),
         ('string_med', dict(Resonator1__Type=2, Resonator1__Quality=2, Resonator1__Decay=0.75), 60),
         ('string_note36', dict(Resonator1__Type=2, Resonator1__Quality=2, Resonator1__Decay=0.75), 36),
         ('stiff_1', dict(Resonator1__Type=2, Resonator1__Quality=2, Resonator1__Decay=0.75, Mallet__Stiffness=1), 48),
         ('decay_0.5', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.5), 60),
         ('pipe', dict(Resonator1__Type=5, Resonator1__Decay=1), 60)]


def rel(a, b, n=None):
    a, b = (a[:n], b[:n]) if n else (a, b)
    return float(np.sqrt(((a - b) ** 2).mean() / (b ** 2).mean()))


def main():
    rc.xdevpy.build()
    rc.SCR.mkdir(parents=True, exist_ok=True)
    out = []
    for tag, kw, n in CASES:
        ref = rc.modal(f'lm_{tag}', kw, n=n)
        base = rc.run(f'lm_{tag}', P(**rc.Q, **kw), note(n, 100, on=0, dur=None), 32768)
        row = dict(case=tag)
        for d in ('+1', '-1'):
            y = rc.run(f'lm_{tag}_{d}', P(**rc.Q, **kw), note(n, 100, on=0, dur=None), 32768, env={'XDEV_LIBM_ULP': d})
            shift = 0.0
            for ch, c in zip((0, 1), ref['channels']):
                for r in c['rows']:
                    if r['weight'] < 1e-2:
                        continue
                    t = fit.track(y[:, ch], r['model_hz'], FS, 64, 20)
                    t0 = fit.track(base[:, ch], r['model_hz'], FS, 64, 20)
                    shift = max(shift, abs(t['hz'] - t0['hz']) / t0['hz'] / rc.freq_bound(t0['hz'], FS))
            row[d] = dict(rel_rms_256=rel(y, base, 256), rel_rms_all=rel(y, base), max_mode_shift_ulp_bounds=shift)
        out.append(row)
        print(row, flush=True)
    for tag, params, ev in (('preset', PRESET, note(60, 100, on=0, dur=None)),
                            ('noise_exc', P(Mallet__OnOff=0, Noise__OnOff=1), note(60, 100, on=0, dur=13230))):
        base = rc.run(f'lm_{tag}', params, ev, 32768)
        row = dict(case=tag)
        for d in ('+1', '-1'):
            y = rc.run(f'lm_{tag}_{d}', params, ev, 32768, env={'XDEV_LIBM_ULP': d})
            row[d] = dict(rel_rms_256=rel(y, base, 256), rel_rms_all=rel(y, base))
        out.append(row)
        print(row, flush=True)
    (HERE / 'results' / 'libm_sensitivity.json').write_text(json.dumps(out, indent=1) + '\n')


if __name__ == '__main__':
    main()
