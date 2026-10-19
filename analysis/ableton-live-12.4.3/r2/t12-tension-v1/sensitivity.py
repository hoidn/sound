"""How much do the reference renders depend on floating-point details? Re-render selected cases with
(1) every inexact libm result moved one ulp up, then down (XDEV_LIBM_ULP=+1/-1; integer-valued results
such as expf(0) = 1 are left exact, see harness/xdev_bind.c), and (2) MXCSR rounding toward -inf,
+inf and zero for every SSE operation of the bundle (0x3f80, 0x5f80, 0x7f80), a stand-in for per-
operation rounding differences such as the arm64 slice's fused multiply-adds. Compare each with the
retained reference render.

    python3 -I sensitivity.py > results/sensitivity.txt     # writes results/sensitivity.json

Measures per perturbation: waveform rel RMS from the first non-zero frame (whole render, held part,
release part, first 2,048 frames); the held RMS level change in dB; the shifts of the first and last
non-zero frames; measure.modal_compare on the held partials; the largest
third-octave level difference over the held window, in the bands within 40 dB of the reference's
strongest; the largest 50 ms envelope difference where the
reference is within 60 dB of its loudest 50 ms. Dependencies: numpy, scipy, analyze_tension.py output.
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402

import cases  # noqa: E402
import measure as M  # noqa: E402
import tension as T  # noqa: E402
import xdevpy  # noqa: E402
from run_tension import load  # noqa: E402

TMP = Path('/var/tmp/sound-analysis/t12-tension/sens')
CASES = ['defaults_44', 'defaults_48', 'note_36', 'note_84', 'vel_127', 'velmod_127', 'exc_hammer', 'plk_x1', 'ham_x1', 'pos_1',
         'str_decay_1', 'str_inharm_1', 'str_ratio_1', 'damper_on', 'damper_gated', 'damper_mass_0', 'term_on', 'pickup_on',
         'body_type_1', 'body_type_2', 'body_decay_1', 'filt_t1_q1', 'filt_t8', 'preset_defaults', 'preset_steel_guitar',
         'preset_clav_clicky', 'preset_nice_harp',
         'exc_bounce', 'exc_bow', 'bow_x1', 'preset_cello']
CHAOTIC = {'exc_bounce', 'exc_bow', 'bow_x1', 'preset_cello', 'damper_mass_0'}
PERT = {'libm+1': ({'XDEV_LIBM_ULP': '+1'}, None), 'libm-1': ({'XDEV_LIBM_ULP': '-1'}, None),
        'round_down': (None, 0x3f80), 'round_up': (None, 0x5f80), 'round_zero': (None, 0x7f80)}


def one(job):
    name, tag = job
    env, mx = PERT[tag]
    c = cases.CASES[name]
    y, _ = T.render(cases.script(c, mxcsr=mx), TMP / f'{name}_{tag}.f32', env=env)
    return job, y[:, 0].astype(float)


def compare(name, x, r, meas):
    c = cases.CASES[name]
    on, off, fs = M.onset(r), c['off'], c['fs']
    d = dict(whole=M.rel_rms(x[on:], r[on:]), held=M.rel_rms(x[on:off], r[on:off]), release=M.rel_rms(x[off:], r[off:]),
             first_2048=M.rel_rms(x[on:on + 2048], r[on:on + 2048]))
    d['modal'] = M.modal_compare(x, r, meas['held'], fs) if meas.get('held') else None
    a = on + 2048
    tx, tr = np.array(M.third_octave(x, a, off, fs)), np.array(M.third_octave(r, a, off, fs))
    sel = tr >= tr.max() - 40                                      # bands within 40 dB of the strongest
    d['third_octave_max_db'] = float(np.max(np.abs(tx[sel] - tr[sel])))
    er, ex = M.env_db(r, fs // 20), M.env_db(x, fs // 20)
    sel = er > er.max() - 60
    d['env_50ms_max_db'] = float(np.max(np.abs(ex[sel] - er[sel])))
    d['held_rms_db'] = float(20 * np.log10(np.sqrt(np.mean(x[a:off] ** 2)) / np.sqrt(np.mean(r[a:off] ** 2))))
    d['onset_shift_frames'] = M.onset(x) - on
    d['last_nonzero_shift_frames'] = (M.last(x) or 0) - (M.last(r) or 0)
    return d


def main():
    xdevpy.build()
    TMP.mkdir(parents=True, exist_ok=True)
    meas = json.loads((HERE / 'results' / 'measure.json').read_text())
    with ThreadPoolExecutor(8) as ex:
        ys = dict(ex.map(one, [(n, t) for n in CASES for t in PERT]))
    out = {}
    for n in CASES:
        r = load(n)[:, 0]
        out[n] = {t: compare(n, ys[(n, t)], r, meas[n]) for t in PERT}
        w = {k: max(out[n][t][k] for t in PERT) for k in ('whole', 'held', 'release', 'first_2048', 'third_octave_max_db', 'env_50ms_max_db')}
        mods = [out[n][t]['modal'] for t in PERT if out[n][t]['modal']]
        mw = {k: max(m[k] for m in mods) for k in ('freq_rel', 'log_radius_rel', 'amp_rel')} if mods else {}
        print(f'{n:20s}', ' '.join(f'{k} {v:.1e}' for k, v in w.items()), '| modal', ' '.join(f'{k} {v:.1e}' for k, v in mw.items()),
              f"(n={mods[0]['n']})" if mods else '')
    summary = {}
    for group, names in (('stable', [n for n in CASES if n not in CHAOTIC]), ('bounce', ['exc_bounce']),
                         ('chaotic', [n for n in CASES if n in CHAOTIC and n != 'exc_bounce'])):
        g = {}
        for k in ('whole', 'held', 'release', 'first_2048', 'third_octave_max_db', 'env_50ms_max_db'):
            g[k] = max(out[n][t][k] for n in names for t in PERT)
        for k in ('held_rms_db', 'onset_shift_frames', 'last_nonzero_shift_frames'):
            g[k + '_max_abs'] = max(abs(out[n][t][k]) for n in names for t in PERT)
        for k in ('freq_rel', 'log_radius_rel', 'amp_rel'):
            v = [out[n][t]['modal'][k] for n in names for t in PERT if out[n][t]['modal']]
            g['modal_' + k] = max(v) if v else None
        summary[group] = g
    out['_summary'] = summary
    print(json.dumps(summary, indent=1))
    (HERE / 'results' / 'sensitivity.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
