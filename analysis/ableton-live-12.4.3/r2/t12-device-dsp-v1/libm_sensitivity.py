"""How much do the renders depend on the libm results? Re-render selected cases with every inexact
libm result moved one ulp up (XDEV_LIBM_ULP=+1) and down (-1), and compare with the reference renders.

    python3 -I libm_sensitivity.py    # after run_corpus.py and run_analog.py; writes results/libm_sensitivity.json

Apple's libm is not available; glibc 2.39's is bound instead. If each Apple result is within one ulp
of glibc's, these two runs bracket the effect of the substitution per call site (an inference: a
real substitution can move different calls in different directions).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402

import analyze_corpus as ac  # noqa: E402
import fit  # noqa: E402
import run_analog  # noqa: E402
import run_corpus  # noqa: E402
import xdevpy  # noqa: E402

CORPUS = ['defaults_44', 'mode_string_44', 'mode_membrane_44', 'pitch_0.25', 'pitch_0.5625', 'wg_tube_48', 'noise_44', 'lfo_sine', 'sine_1000']


def main():
    tmp = Path('/var/tmp/sound-analysis/t12-xdev/libm')
    tmp.mkdir(parents=True, exist_ok=True)
    inputs = {k: str(HERE / 'inputs' / f'{k}.f32') for k in ac.RUNS['inputs']}
    out = {}
    for name in CORPUS:
        c = ac.RUNS['runs'][name]['case']
        ref = ac.load(name)
        start = ac.N0 if c['input'].startswith('impulse') else 8192
        row = {}
        for d in ('+1', '-1'):
            y, _ = xdevpy.render('Corpus', run_corpus.script(c, inputs), tmp / f'{name}{d}.f32', env={'XDEV_LIBM_ULP': d})
            y = y.astype(float)
            r = dict(bit_identical=bool(np.array_equal(y, ref)), max_abs_diff_re_peak=float(np.abs(y - ref).max() / np.abs(ref).max()),
                     first_256=ac.err(y[start:start + 256], ref[start:start + 256])['rel_rms'],
                     window=ac.err(y[start:], ref[start:])['rel_rms'])
            if name.startswith(('mode_', 'pitch_', 'defaults')):
                m = ac.mdl(name)
                shifts = []
                for p in m.poles('L')[:12]:
                    a, b = (fit.track(s[:, 0], p['pole_hz'], m.fs, ac.N0, 30)['hz'] for s in (y, ref))
                    shifts.append(abs(a / b - 1))
                r['max_mode_freq_shift_rel'] = max(shifts)
            row[d] = r
        out[name] = row
    live = run_analog.live_defaults()
    ref = np.fromfile(HERE / 'raw' / 'analog' / 'note_live_44.f32', np.float32).reshape(-1, 2).astype(float)
    on, off = 4096, 4096 + 22050
    row = {}
    for d in ('+1', '-1'):
        y, _ = xdevpy.render('Analog', run_analog.script(live, [(on, 0x90, 60, 100), (off, 0x80, 60, 0)]), tmp / f'analog{d}.f32',
                             env={'XDEV_LIBM_ULP': d})
        y = y.astype(float)
        f = [fit.track(s[:off, 0], 261.537, 44100, on + 2048, 20)['hz'] for s in (y, ref)]
        row[d] = dict(bit_identical=bool(np.array_equal(y, ref)), max_abs_diff_re_peak=float(np.abs(y - ref).max() / np.abs(ref).max()),
                      window=ac.err(y[on:], ref[on:])['rel_rms'], fundamental_shift_rel=f[0] / f[1] - 1)
    out['analog_note_live_44'] = row
    (HERE / 'results' / 'libm_sensitivity.json').write_text(json.dumps(out, indent=1))
    for k, v in out.items():
        print(k, {d: {kk: (f'{vv:.1e}' if isinstance(vv, float) else vv) for kk, vv in r.items()} for d, r in v.items()})


if __name__ == '__main__':
    main()
