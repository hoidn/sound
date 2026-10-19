"""Electric probes on the parameter and protocol side: when parameter changes take effect, ramps,
gain laws, output limit, rate change, reset, transport, activity flag, determinism, start-up,
and 0.25/0.75 sweeps of every continuous parameter.

    python3 -I probes_params.py      # writes results/probes_params.json (renders not retained)
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import el  # noqa: E402
import fit  # noqa: E402
import measure as M  # noqa: E402
import xdevpy  # noqa: E402
from probes_events import f0_of  # noqa: E402

H = el.host_values(el.CONSTRUCTOR)
NOTE = el.note(60, 100, 0, 13230)


def lvl(x):
    return float(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-30))


def first_diff(a, b):
    d = np.nonzero(a != b)[0]
    return int(d[0]) if len(d) else None


def _latch(i):
    """Index i changed at render frame 8192 while C4 (on at 0, off at 12288) sounds."""
    new = {0: 0.0, 23: 1.0, 30: 0.0, 32: 0.0, 2: 0.35}.get(i, 0.0 if H[i] >= 0.5 else 1.0)
    ev = [(0, 0x90, 60, 100), (12288, 0x80, 60, 0)]
    base, _ = el.render(H, ev, 44100, f'la_b_{i}', 20480)
    held, _ = el.render(H, ev, 44100, f'la_h_{i}', 20480, extra=[(8192, f'param {i} {new!r}')])
    f = first_diff(base, held)
    when = 'never' if f is None else 'held note' if f < 12288 else 'from the note-off'
    return i, dict(new_value=new, first_changed_frame=f, effect=when)


def _next_note(i):
    """Index i changed at render frame 0; a note at 512 (just after) against a note at 44032 (settled)."""
    new = {0: 0.0, 23: 1.0, 30: 0.0, 32: 0.0, 2: 0.35}.get(i, 0.0 if H[i] >= 0.5 else 1.0)
    out = {}
    for dt in (512, 2048, 3584, 4096, 4608, 44032):
        x, _ = el.render(H, el.note(60, 100, dt, 13230), 44100, f'nn_{i}_{dt}', dt + 13230, extra=[(0, f'param {i} {new!r}')])
        out[dt] = lvl(x[dt:dt + 13230])
    return i, dict(new_value=new, note_level_db_by_onset=out, settled_by_512=abs(out[512] - out[44032]) < 0.05)


def ramps():
    out = {}
    base, _ = el.render(H, [NOTE[0]], 44100, 'rv_base', 30000)
    for fs in (44100, 48000):
        b, _ = el.render(H, [NOTE[0]], fs, f'rv_base{fs}', 30000)
        for nv in (0.0, 0.35, 1.0):
            x, _ = el.render(H, [NOTE[0]], fs, f'rv_{fs}_{nv}', 30000, extra=[(8192, f'param 2 {nv!r}')])
            f = first_diff(b, x)
            target = (nv / H[2]) ** 2
            ok = np.abs(b) > 1e-3
            r = np.where(ok, x / np.where(ok, b, 1), np.nan)
            seg = r[f:f + 6000]
            done = np.nonzero(np.abs(np.nan_to_num(seg, nan=target) - target) > 1e-4 * max(target, 1))[0]
            lin = 1 + (target - 1) * np.minimum(np.arange(1, 6001) / 4000, 1)
            dev = np.nanmax(np.abs(seg - lin))
            out[f'volume_{fs}_{nv}'] = dict(first_changed_frame=f, target_ratio=target, ramp_frames=int(done[-1]) + 1 if len(done) else 0,
                                            ratio_at=[None if np.isnan(seg[k]) else float(seg[k]) for k in (0, 1, 999, 1999, 2999, 3998, 3999, 4000)],
                                            max_dev_from_linear_4000=float(dev))
    h = {**H, 21: 1.0}
    x, _ = el.render(h, [NOTE[0]], 44100, 'rf', 30000, extra=[(8192, 'param 3 1.0')])
    t = [fit.track(x[:a + 2205], 261.6 * (2 ** (0.5 / 12) if a > 8192 else 1), 44100, a, 200)['hz'] for a in (6000, 8300, 8500, 8800, 9200, 10000, 14000)]
    out['finetune_glide_hz_at'] = dict(frames=[6000, 8300, 8500, 8800, 9200, 10000, 14000], hz=t)
    lv = {}
    for dt in (0, 1024, 2048, 3072, 3584, 3840, 4032, 4096, 4224, 4608, 8192):
        y, _ = el.render(H, el.note(60, 100, dt, 13230), 44100, f'rmfv_{dt}', dt + 13230, extra=[(0, 'param 9 1.0')])
        lv[dt] = lvl(y[dt:dt + 13230])
    out['forcevel_0.5_to_1_note_level_db_by_onset'] = lv
    return out


def gains():
    out = {}
    ev = [NOTE[0]]
    ref, _ = el.render(H, ev, 44100, 'g_ref', 22050)
    m = np.abs(ref) > 1e-3
    for v in (0.1, 0.25, 0.5, 0.75, 1.0):
        x, _ = el.render({**H, 2: v}, ev, 44100, f'g_v{v}', 22050)
        r = x[m] / ref[m]
        out[f'volume_{v}'] = dict(ratio_mean=float(r.mean()), ratio_spread=float(r.max() - r.min()), v2_ratio=(v / H[2]) ** 2)
    for v in (0.1, 0.25, 0.75, 1.0):
        x, _ = el.render({**H, 25: v}, ev, 44100, f'g_o{v}', 22050)
        r = x[m] / ref[m]
        out[f'pickup_amp_out_{v}'] = dict(ratio_mean=float(r.mean()), ratio_spread=float(r.max() - r.min()), db=float(20 * np.log10(r.mean())))
    for v in (0.0, 0.25, 0.75, 1.0):
        row = {}
        for n in (36, 48, 72, 84, 96):
            a, _ = el.render(H, el.note(n, 100, 0, 13230), 44100, f'g_k{n}', 22050)
            b, _ = el.render({**H, 26: v}, el.note(n, 100, 0, 13230), 44100, f'g_k{n}_{v}', 22050)
            mm = np.abs(a) > 1e-3 * np.abs(a).max()
            r = b[mm] / a[mm]
            row[n] = dict(db=float(20 * np.log10(np.median(r))), spread=float(r.max() - r.min()))
        out[f'pickup_amp_keyboard_{v}'] = row
    hot = {**H, 9: 1.0, 24: 1.0, 25: 1.0, 2: 1.0, 20: 1.0}
    x, _ = el.render(hot, el.note(60, 127, 0, 13230), 44100, 'g_hot', 22050)
    out['clip'] = dict(max=float(x.max()), min=float(x.min()), frames_at_plus_4=int((x == 4.0).sum()), frames_at_minus_4=int((x == -4.0).sum()))
    return out


def protocol():
    out = {}
    case = dict(band_starts=[0, 4410, 13230], f0=261.62, off=13230)
    ref, log = el.render(H, NOTE, 44100, 'pr_ref', 22050)
    mref = M.measure(ref, 44100, case)
    lines = ['create', 'rate 44100'] + [f'param {i} {v!r}' for i, v in sorted(H.items())] + ['inflag 0', 'input zero', 'process 11264 512',
             'rate 48000', f'event {11264 + 12288} 0x90 60 100', f'event {11264 + 12288 + 14400} 0x80 60 0', 'process 36288 512', 'destroy']
    y, _ = xdevpy.render('Electric', lines, el.SCRATCH / 'pr_rate.f32', script_path=el.SCRATCH / 'pr_rate.script')
    y = y[11264 + 12288:, 0].astype(float)
    d48, _ = el.render(H, el.note(60, 100, 0, 14400), 48000, 'pr_48', 24000)
    case48 = dict(band_starts=[0, 4800, 14400], f0=261.61, off=14400)
    dv = M.element_deviations(M.measure(d48, 48000, case48), M.measure(y, 48000, case48), 48000)
    out['rate_44100_then_48000_vs_48000'] = dict(bit_identical=bool(np.array_equal(y, d48)), env_max_db=float(dv['env'].max()),
                                                 amp_max_db=float(dv['amp'].max()), freq_max_ulp_bounds=float(dv['freq'].max()))
    for tag, extra in (('reset_sequence', [(0, 'reset'), (0, 'param 0 30.0')]), ('reset_only', [(0, 'reset')]),
                       ('transport_playing_90bpm', [(0, 'transport 1 16.0 90.0')])):
        x, _ = el.render(H, NOTE, 44100, f'pr_{tag}', 22050, extra=extra)
        dv = M.element_deviations(mref, M.measure(x, 44100, case), 44100)
        out[tag] = dict(bit_identical=bool(np.array_equal(x, ref)), env_max_db=float(dv['env'].max()), amp_max_db=float(dv['amp'].max()))
    for tag, kw in (('rerun', {}), ('block_64', dict(block=64)), ('block_256', dict(block=256)), ('block_2048', dict(block=2048)),
                    ('block_333', dict(block=333))):
        x, _ = el.render(H, NOTE, 44100, f'pr_{tag}', 22050, **kw)
        dv = M.element_deviations(mref, M.measure(x, 44100, case), 44100)
        out[tag] = dict(bit_identical=bool(np.array_equal(x, ref)), onset=M.onset(x), env_max_db=float(dv['env'].max()),
                        amp_max_db=float(dv['amp'].max()))
    sig = np.repeat(0.5 * np.sin(2 * np.pi * 440 * np.arange(11264 + 22050) / 44100), 2).astype('<f4')
    sig.tofile(el.SCRATCH / 'pr_sine.f32')
    for flag in (0, 1):
        lines = [f'input {el.SCRATCH / "pr_sine.f32"}' if l == 'input zero' else f'inflag {flag}' if l == 'inflag 0' else l
                 for l in el.script(H, NOTE, 44100, 22050)]
        y, _ = xdevpy.render('Electric', lines, el.SCRATCH / f'pr_in{flag}.f32', script_path=el.SCRATCH / f'pr_in{flag}.script')
        out[f'input_sine_inflag_{flag}'] = dict(bit_identical=bool(np.array_equal(y[11264:, 0].astype(float), ref)))
    lines = el.script(H, NOTE, 44100, 22050)
    lines.insert(lines.index('inflag 0'), 'mxcsr 0x9fc0')
    y, _ = xdevpy.render('Electric', lines, el.SCRATCH / 'pr_ftz.f32', script_path=el.SCRATCH / 'pr_ftz.script')
    out['ftz_daz'] = dict(bit_identical=bool(np.array_equal(y[11264:, 0].astype(float), ref)))
    _, lg = el.render(H, [(0, 0x90, 60, 100), (4096, 0x80, 60, 0)], 44100, 'pr_flag', 441000, warm=0)
    _, lg2 = el.render(H, [], 44100, 'pr_flag0', 441000, warm=0)
    out['activity_flag'] = dict(note_then_silence=[l for l in lg.splitlines() if l.startswith('process')],
                                no_note=[l for l in lg2.splitlines() if l.startswith('process')])
    st = {}
    for on in (0, 1024, 2048, 3072, 4096, 4224, 4352, 4400, 4480, 5000, 11264):
        x, _ = el.render(H, el.note(60, 100, on, 13230), 44100, f'pr_st_{on}', on + 13230, warm=0)
        st[on] = lvl(x[on:on + 13230])
    out['start_up_note_level_db_by_onset_from_creation'] = st
    x, _ = el.render(H, [NOTE[0]], 44100, 'pr_poly_b', 20480)
    for pv in (0.0, 29.0):
        y, _ = el.render(H, [NOTE[0]], 44100, f'pr_poly_{pv}', 20480, extra=[(8192, f'param 0 {pv!r}')])
        out[f'polyphony_to_{pv}_during_note'] = dict(first_changed=first_diff(x, y), level_before_db=lvl(y[4410:8192]),
                                                    level_after_db=lvl(y[9000:20480]), unchanged_level_db=lvl(x[9000:20480]))
    return out


def _release(a):
    """Time from the note-off until the 10 ms level is 60 dB below the last 10 ms before it."""
    n, v = a
    x, _ = el.render({**H, 14: v}, el.note(n, 100, 0, 13230), 44100, f'rl_{n}_{v}', 13230 + 132300)
    e = M.env_db(x, 44100)
    rel = np.nonzero(e[30:] < e[29] - 60)[0]
    return f'{n}_{v}', float(rel[0] * 0.01) if len(rel) else None


def n_of(v):
    c = 128 * v if v <= 0.5 else 126 * v + 1
    return 0.5 if c == 64 else c / 127


def _law(a):
    i, v, ref_v = a
    ref, _ = el.render({**H, i: ref_v}, [(0, 0x90, 60, 100)], 44100, f'law_{i}_ref', 8820)
    x, _ = el.render({**H, i: v}, [(0, 0x90, 60, 100)], 44100, f'law_{i}_{v}', 8820)
    m = np.abs(ref) > 1e-3
    r = x[m] / ref[m]
    return i, v, dict(ratio=float(np.median(r)), spread=float(r.max() - r.min()))


def _quant(i):
    a, _ = el.render({**H, i: 0.25}, el.note(60, 100, 0, 8820), 44100, f'qa_{i}', 13230)
    b, _ = el.render({**H, i: 0.2525}, el.note(60, 100, 0, 8820), 44100, f'qb_{i}', 13230)
    return i, bool(np.array_equal(a, b))


def _mfv(a):
    fs, dt = a
    x, _ = el.render(H, el.note(60, 100, dt, 8000), fs, f'mfv_{fs}_{dt}', dt + 8000, extra=[(0, 'param 9 1.0')])
    return f'{fs}_{dt}', float(np.sqrt((x[dt:] ** 2).mean()))


def laws(pool):
    """Gain laws (sample ratio against a reference value), controller quantization, the
    MalletForceVelocity settling time and the start-up with index 9 left unsent."""
    vol = [round(0.05 * k, 2) for k in range(1, 21)] + [0.01, 0.02, H[2]]
    out = dict(volume_re_1={}, pickup_amp_out_re_0_5={})
    for i, v, r in pool.map(_law, [(2, v, 1.0) for v in vol] + [(25, v, 0.5) for v in
                                   (0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.45, 0.49, 0.51, 0.55, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0)]):
        if i == 2:
            out['volume_re_1'][str(v)] = dict(r, n_squared=n_of(v) ** 2)
        else:
            c = 128 * v if v <= 0.5 else 126 * v + 1
            out['pickup_amp_out_re_0_5'][str(v)] = dict(r, db=float(20 * np.log10(r['ratio'])), law_db=15 * (c - 64) / 64)
    out['volume_max_rel_dev_from_n_squared'] = max(abs(r['ratio'] / r['n_squared'] - 1) for r in out['volume_re_1'].values())
    out['amp_out_max_abs_dev_db'] = max(abs(r['db'] - r['law_db']) for r in out['pickup_amp_out_re_0_5'].values())
    out['quantized_0.25_vs_0.2525_identical'] = dict(pool.map(_quant, (3, 4, 7, 9, 14, 19, 20, 21, 22, 24, 27, 28, 31)))
    r = dict(pool.map(_mfv, [(44100, d) for d in range(4180, 4600, 44)] + [(48000, d) for d in range(4320, 5100, 48)]
                      + [(44100, 40000), (48000, 40000)]))
    out['forcevel_note_rms_re_settled'] = {k: v / r[f"{k.split('_')[0]}_40000"] for k, v in r.items() if not k.endswith('_40000')}
    p = {k: v for k, v in H.items() if k != 9}
    early, _ = el.render(p, el.note(60, 100, 0, 13230), 44100, 'su_early', 13230, warm=0)
    late, _ = el.render(p, el.note(60, 100, 44100, 13230), 44100, 'su_late', 44100 + 13230, warm=0)
    out['start_up_index9_unsent_early_vs_late_db'] = lvl(early) - lvl(late[44100:])
    return out


def _sweep(a):
    i, v = a
    x, _ = el.render({**H, i: v}, NOTE, 44100, f'sw_{i}_{v}', 22050)
    on = M.onset(x)
    if on is None:
        return i, v, None
    f0 = f0_of(x, 261.62 * 2 ** ((H[3] - 0.5) / 12 if i != 3 else (v - 0.5) / 12), 44100, 13230)
    p = M.partials(x, 44100, on, 13230, f0)
    e = M.env_db(x, 44100)
    rel = np.nonzero(e[30:] < e[29] - 60)[0]          # 10 ms frames from the note-off (frame 30 = 13230)
    a20 = x[on:on + 882]
    sp = np.abs(np.fft.rfft(a20 * np.hanning(len(a20)), 8192)) ** 2
    hz = np.fft.rfftfreq(8192, 1 / 44100)
    return i, v, dict(peak=float(np.abs(x).max()), sustain_db=lvl(x[2205:13230]), f0=f0,
                      harmonics_db=[q['amp_db'] for q in p[:5]], decay_db_s=[q['decay_db_s'] for q in p[:3]],
                      release_60db_s=float(rel[0] * 0.01) if len(rel) else None,
                      attack_centroid_hz=float((sp * hz).sum() / sp.sum()))


def main():
    xdevpy.build()
    with Pool(8) as pool:
        latch = dict(pool.map(_latch, range(33)))
        nxt = dict(pool.map(_next_note, range(33)))
        sw = pool.map(_sweep, [(i, v) for i in range(1, 32) if i not in (23, 30) for v in (0.0, 0.25, 0.5, 0.75, 1.0)])
        rel = dict(pool.map(_release, [(n, v) for n in (36, 60, 84) for v in (0.0, 0.25, 0.5, 0.75, 1.0)]))
        lw = laws(pool)
    out = dict(latch_during_note=latch, change_before_next_note=nxt, ramps=ramps(), gains=gains(), protocol=protocol(),
               release_60db_s_by_note_and_fork_release_time=rel, laws=lw,
               sweeps={f'{i}_{el.NAMES[i]}': {str(v): r for j, v, r in sw if j == i} for i in sorted({s[0] for s in sw})})
    (HERE / 'results' / 'probes_params.json').write_text(json.dumps(out, indent=1))
    print({i: (v['effect'], v['first_changed_frame']) for i, v in latch.items()})
    print({i: v['settled_by_512'] for i, v in nxt.items()})
    print(rel)
    print({k: v for k, v in lw.items() if not isinstance(v, dict) or k.startswith('quant')})
    print(json.dumps(out['ramps'], indent=0)[:3000])
    print(json.dumps(out['gains'], indent=0)[:3000])
    print(json.dumps(out['protocol'], indent=0)[:4000])


if __name__ == '__main__':
    main()
