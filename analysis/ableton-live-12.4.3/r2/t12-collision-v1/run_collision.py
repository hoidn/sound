"""Render the Collision cases through the bundle's x86_64 slice and measure them.

    python3 -I run_collision.py      # writes raw/*.wav (reference renders), raw/*.script, results/collision.json

Every render: CreateInstanceU, SetSampleRateU(fs), SetParameterA for all 139 host indices (col.py:
PRESET, the shipped Defaults preset as Live sends it, with the case's host-value overrides), a warm-up
without events (11,264 frames at 44.1 kHz, 12,288 at 48 kHz, output discarded, as SPEC-DEVICE-ELECTRIC),
then note events at frames counted from render frame 0 and CalcA in host blocks of 512 frames, input
flag 0, silent input, transport {0, 0.0, 120.0}.
The clock that seeds rand is fixed at 0 unless a case says otherwise. "Q" cases set Mallet/NoiseAmount
to host 0, which leaves a mallet-noise share of 4.7e-4 (see the research page). Measurements use
fit.py (demodulation) and model.py (static model); renders kept for grading are written as 32-bit
float stereo WAV. Scratch renders go to /var/tmp/sound-analysis/t12-collision/.
Dependencies: numpy, scipy, gcc (xdevpy.build), the app bundle.
"""
import concurrent.futures as cf
import json
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402
from scipy.io import wavfile  # noqa: E402

import fit  # noqa: E402
import model  # noqa: E402
import xdevpy  # noqa: E402
from col import CTOR, FS, P, PRESET, idx, note, onset, peak_hz, render, script  # noqa: E402

RAW, RES = HERE / 'raw', HERE / 'results'
SCR = Path('/var/tmp/sound-analysis/t12-collision/run')
Q = dict(Mallet__NoiseAmount=0)
OUT = {}


WARM = {44100: 11264, 48000: 12288}           # warm-up: 256 control periods, whole 512-frame blocks (as Electric)


def run(tag, params, events, frames, fs=FS, block=512, pre=(), env=None, keep=False, mxcsr=None, warm=True):
    """Render after the warm-up (no events, output discarded); with keep=True also write raw/<tag>.wav and
    raw/<tag>.script. Event frames count from render frame 0, the first frame after the warm-up.
    Returns float64 frames x 2."""
    w = WARM[fs] if warm else 0
    lines = script(params, events, fs=fs, frames=frames, block=block,
                   pre=(['inflag 0', 'input zero', f'process {w} 512'] if w else []) + list(pre), mxcsr=mxcsr)
    p = SCR / f'{tag}.f32'
    y, log = render(lines, p, env=env)
    LOG[tag] = log
    y = y[w:]
    if keep:
        (RAW / f'{tag}.script').write_text('\n'.join(lines) + '\n')
        wavfile.write(RAW / f'{tag}.wav', fs, y)
        KEPT[tag] = dict(sha256=xdevpy.sha256(RAW / f'{tag}.wav'), frames=int(len(y)), fs=fs, warm_up_frames=w,
                         imports=xdevpy.used_imports(log), process=[l for l in log.splitlines() if l.startswith('process')])
    return y.astype(float)


KEPT = {}
LOG = {}


def fitg(a, b):
    """Least-squares gain of a on b and the relative residual."""
    g = float(a @ b / (b @ b)) if b @ b > 0 else 0.0
    return g, float(math.sqrt(((a - g * b) ** 2).mean() / max((a ** 2).mean(), 1e-300)))


def db(x):
    return 20 * math.log10(abs(x)) if x else -math.inf


def par(fn, items, workers=8):
    with cf.ThreadPoolExecutor(workers) as ex:
        return list(ex.map(fn, items))


# ---------------------------------------------------------------- root cause and topology
def root_cause():
    ev = note(60, 100)
    out = {}
    y = run('ctor_c4', CTOR, ev, 22050, keep=True)
    out['ctor'] = dict(peak=float(np.abs(y).max()), note='constructor defaults: Resonator1/OnOff and Resonator2/OnOff both 0')
    y = run('preset_c4', PRESET, ev, 44100, keep=True)
    out['preset'] = dict(peak=float(np.abs(y).max()), first_change=int(onset(y, 1e-12)))
    rows = []
    q1 = P(**Q)
    r1 = run('topo_r1', q1, note(60, 100, dur=None), 16384)
    for order in (0, 1):
        for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
            y = run(f'topo_{order}{a}{b}', P(**Q, Resonator1__OnOff=a, Resonator2__OnOff=b, ResonatorOrder=order), note(60, 100, dur=None), 16384)
            rows.append(dict(order=order, res1=a, res2=b, peak=float(np.abs(y).max()),
                             equals_res1_only=bool(np.array_equal(y, r1)), minus_twice_res1=float(np.abs(y - 2 * r1).max())))
    out['topology'] = rows
    return out


# ---------------------------------------------------------------- protocol invariances
def protocol():
    ev = note(60, 100)
    base = run('proto_base', PRESET, ev, 44100)
    rows = []
    variants = [('rerun', {}), ('block64', dict(block=64)), ('block256', dict(block=256)), ('block2048', dict(block=2048)),
                ('block333', dict(block=333)), ('ftz_daz', dict(mxcsr=0x9fc0)),
                ('reset_sequence', dict(pre=['reset', f'param 0 {PRESET[0]!r}'])),
                ('no_warm_up', dict(warm=False)),
                ('clock_1760000000', dict(env={'XDEV_TIME': '1760000000'}))]
    for name, kw in variants:
        y = run(f'proto_{name}', PRESET, ev, 44100, **kw)
        d = np.abs(y - base)
        rows.append(dict(variant=name, bit_identical=bool(np.array_equal(y, base)), max_abs_diff=float(d.max()),
                         rel_rms=float(np.sqrt((d ** 2).mean() / (base ** 2).mean()))))
        if name == 'block333':                            # the note takes effect at 4092 instead of 4136 (grid rule)
            rows.append(dict(variant='block333, shifted by 44 frames', bit_identical=bool(np.array_equal(y[:-44], base[44:])),
                             max_abs_diff=float(np.abs(y[:-44] - base[44:]).max())))
    q = P(**Q)
    b2 = run('proto_q', q, ev, 44100)
    y = run('proto_q_clock', q, ev, 44100, env={'XDEV_TIME': '1760000000'})
    rows.append(dict(variant='Q, clock 1760000000', max_abs_diff=float(np.abs(y - b2).max()),
                     rel_rms=float(np.sqrt(((y - b2) ** 2).mean() / (b2 ** 2).mean()))))
    d48 = run('proto_48', q, ev, 48000, fs=48000)
    y = run('proto_44_then_48', q, ev, 48000, fs=48000, pre=['rate 44100', 'rate 48000'])
    rel = lambda a, b: float(np.sqrt(((a - b) ** 2).mean() / (b ** 2).mean()))  # noqa: E731
    rows.append(dict(variant='rate 44100 then 48000 (Q)', bit_identical=bool(np.array_equal(y, d48)), max_abs_diff=float(np.abs(y - d48).max()),
                     rel_rms=rel(y, d48)))
    y = run('proto_params_then_rate', q, ev, 48000, fs=44100, pre=['rate 48000'])
    rows.append(dict(variant='parameters at 44100, then rate 48000 (Q)', bit_identical=bool(np.array_equal(y, d48)),
                     max_abs_diff=float(np.abs(y - d48).max()), rel_rms=rel(y, d48)))
    info = [l for l in xdevpy.render('Collision', ['info', 'create', 'rate 44100', 'destroy'], SCR / 'info.f32')[1].splitlines() if l.startswith('info')]
    return dict(variants=rows, plug_info=info)


# ---------------------------------------------------------------- event timing
def grid_rule(f, block, period):
    """First output frame an event at frame f changes: the start g of the 1 ms grid period that contains f
    (period = fs // 1000 frames, counted from the first processed frame), or g + period when g lies in an
    earlier host block."""
    g = period * (f // period)
    return g if g >= block * (f // block) else g + period


def timing():
    q = P(**Q)
    out = {}
    for label, fs, block in (('on_44_b512', 44100, 512), ('on_44_b64', 44100, 64), ('on_44_b333', 44100, 333), ('on_48_b512', 48000, 512)):
        base = run(f'tm0_{label}', q, [], 4096, fs=fs, block=block)
        frames = list(range(0, 120, 3)) + list(range(1000, 1130, 3))

        def one(f):
            y = run(f'tm_{label}_{f}', q, [(f, 0x90, 60, 100)], 4096, fs=fs, block=block)
            k = np.nonzero(np.abs(y - base).max(1) > 0)[0]
            return dict(event=f, first_change=int(k[0]), rule=grid_rule(f, block, fs // 1000))
        rows = par(one, frames)
        out[label] = dict(fs=fs, block=block, n=len(rows), rule_holds=all(r['first_change'] == r['rule'] for r in rows), rows=rows)
    q0 = P(**Q, Resonator1__DecayOnNoteOff=0.5)
    held = run('tm_held', q0, [(1024, 0x90, 60, 100)], 8192)

    def off(f):
        y = run(f'tm_off_{f}', q0, [(1024, 0x90, 60, 100), (f, 0x80, 60, 0)], 8192)
        k = np.nonzero(np.abs(y - held).max(1) > 0)[0]
        return dict(event=f, first_change=int(k[0]) if len(k) else None, rule=grid_rule(f, 512, 44))
    rows = par(off, list(range(4000, 4130, 3)))
    out['off_44_b512_offdecay_host0.5'] = dict(rows=rows, rule_holds=all(r['first_change'] == r['rule'] for r in rows))
    return out


# ---------------------------------------------------------------- pitch
def pitch():
    rows = []
    s = dict(Mallet__NoiseAmount=0, Resonator1__Type=2, Resonator1__Quality=0, Resonator1__Decay=1)

    def f0(args):
        tag, kw, n, fs = args
        low = n < 48 or kw.get('Resonator1__Transpose', 0) < -12
        y = run(tag, P(**s, **kw), note(n, 100, on=0, dur=None), 131072 if low else 32768, fs=fs)
        nom = 261.62 * model.A(kw.get('Resonator1__KeyToTranspose', 1) * (n - 60) / 12 + kw.get('Resonator1__Transpose', 0) / 12
                               + kw.get('Resonator1__FineTranspose', 0) / 1200)
        est = peak_hz(y[1024:1024 + (65536 if low else 16384), 0], fs, lo_hz=10.0)
        hz = fit.track(y[:, 0], est, fs, 1024, min(20.0, 0.3 * est), max_taps=32001)['hz']
        return dict(case=tag, note=n, fs=fs, **{k.split('__')[1]: v for k, v in kw.items()}, hz=hz, model_hz=nom,
                    rel=(hz - nom) / nom, ulp_bounds=(hz - nom) / nom / freq_bound(nom, fs), cents_from_12tet=1200 * math.log2(hz / (440 * 2 ** ((n - 69) / 12))))
    items = [(f'pitch_n{n}_{fs}', {}, n, fs) for n in (24, 36, 48, 60, 69, 72, 84, 96, 108) for fs in (44100, 48000)]
    items += [(f'pitch_tr{t}', dict(Resonator1__Transpose=t), 60, FS) for t in (-48, -24, -12, 1, 7, 12, 24, 48)]
    items += [(f'pitch_fine{t}', dict(Resonator1__FineTranspose=t), 60, FS) for t in (-50, -25, 10, 50)]
    items += [(f'pitch_key{k}', dict(Resonator1__KeyToTranspose=k), 72, FS) for k in (-1, 0, 0.5, 2)]
    rows = par(f0, items)
    return rows


# ---------------------------------------------------------------- resonator against the static model
def freq_bound(hz, fs):
    th = 2 * math.pi * hz / fs
    return 3 * 2 ** -25 / th ** 2 + 2 ** -23


def modal(tag, kw, n=60, fs=FS, res=1, keep=False, frames=32768, vel=100):
    q = P(**Q, **kw)
    y = run(tag, q, note(n, vel, on=0, dur=None), frames, fs=fs, keep=keep)
    m = model.CollisionModel(q, n, res=res, fs=fs)
    ps = m.poles()
    M = model.mallet_response(q, [p['pole_hz'] for p in ps], fs)
    out = []
    for ci, ch in enumerate('LR'):
        w = [p['gain'] * p['exc'] * p['pick'][ch] * M[i] for i, p in enumerate(ps)]
        big = max(abs(v) for v in w)
        rows = []
        for i, p in enumerate(ps):
            if abs(w[i]) < 1e-3 * big:
                continue
            gap = min([abs(p['pole_hz'] - o['pole_hz']) for o in ps if o is not p] + [1e9])
            cut = min(100.0, 0.4 * gap)
            if cut < 10:
                continue                                        # closely spaced: not resolved by the estimator
            end = min(len(y), 64 + int(6.9 / abs(p['log_radius'])) + 1500)    # until about -60 dB (control-rate residual below)
            t = fit.track(y[:end, ci], p['pole_hz'], fs, 0, cut)          # amplitude at render frame 0, the note-on
            if abs(t['hz'] - p['pole_hz']) / p['pole_hz'] > 1e-4:
                continue
            rows.append(dict(k=p['k'], model_hz=p['pole_hz'], weight=abs(w[i]) / big, hz=t['hz'],
                             f_ulp=((t['hz'] - p['pole_hz']) / p['pole_hz']) / freq_bound(p['pole_hz'], fs),
                             rho_rel=t['log_radius'] / p['log_radius'] - 1, rho_ulp=(t['log_radius'] - p['log_radius']) / 2 ** -25,
                             amp=t['amp'], model=w[i]))
        G = np.median([r['amp'] / r['model'] for r in rows if r['weight'] >= 1e-2]) if rows else 0
        for r in rows:
            r['amp_rel_err'] = abs(r['amp'] / r['model'] / G - 1)
            r['amp'] = [r['amp'].real, r['amp'].imag]
            r['model'] = [r['model'].real, r['model'].imag]
        strong = [r for r in rows if r['weight'] >= 1e-2]
        out.append(dict(channel=ch, modes=len(ps), measured=len(rows), graded=len(strong),
                        gain=[float(np.real(G)), float(np.imag(G))], gain_per_pitch=float(np.real(G)) / model.A(m.pitch),
                        max_f_ulp=max((abs(r['f_ulp']) for r in strong), default=None),
                        max_rho_ulp=max((abs(r['rho_ulp']) for r in strong), default=None),
                        max_f_ulp_weak=max((abs(r['f_ulp']) for r in rows), default=None),
                        max_amp_rel_err=max((r['amp_rel_err'] for r in strong), default=None), rows=rows))
    return dict(case=tag, params=kw, note=n, fs=fs, channels=out)


MODAL = [('mode_beam_high', dict(Resonator1__Type=0, Resonator1__Quality=3, Resonator1__Decay=0.75), {}, True),
         ('mode_marimba_high', dict(Resonator1__Type=1, Resonator1__Quality=3, Resonator1__Decay=0.75), {}, True),
         ('mode_string_high', dict(Resonator1__Type=2, Resonator1__Quality=3, Resonator1__Decay=0.75), {}, True),
         ('mode_membrane_high', dict(Resonator1__Type=3, Resonator1__Quality=3, Resonator1__Decay=0.75), {}, True),
         ('mode_plate_high', dict(Resonator1__Type=4, Resonator1__Quality=3, Resonator1__Decay=0.75), {}, True),
         ('mode_beam_48', dict(Resonator1__Type=0, Resonator1__Quality=3, Resonator1__Decay=0.75), dict(fs=48000), True),
         ('mode_string_48', dict(Resonator1__Type=2, Resonator1__Quality=3, Resonator1__Decay=0.75), dict(fs=48000), False),
         ('quality_eco', dict(Resonator1__Type=2, Resonator1__Quality=0, Resonator1__Decay=0.75), {}, False),
         ('quality_low', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.75), {}, False),
         ('decay_0.25', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.25), {}, True),
         ('decay_0.5', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.5), {}, False),
         ('decay_1', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=1), {}, False)]
MODAL += [(f'material_{v}', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.75, Resonator1__Damp=v), {}, v in (-1, 1))
          for v in (-1, -0.5, 0.5, 1)]
MODAL += [(f'inharm_{v}', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.75, Resonator1__Inharmonics=v), {}, v == 0.5)
          for v in (-0.5, 0.5)]
MODAL += [(f'bright_{v}', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.75, Resonator1__AmpFreq=v), {}, v == 1)
          for v in (-1, 1)]
MODAL += [(f'ratio_{t}_{v}', dict(Resonator1__Type=t, Resonator1__Quality=1, Resonator1__Decay=0.75, Resonator1__Ratio=v), {}, v == 0.75)
          for t in (3, 4) for v in (0.25, 0.75)]
MODAL += [(f'hit_{v}', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.75, Resonator1__HitX=v), {}, True)
          for v in (0, 0.25, 1)]
MODAL += [('listen_L0_R0.5', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.75, Resonator1__ListeningXL=0,
                                  Resonator1__ListeningXR=0.5), {}, True),
          ('listen_L1_R0', dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.75, Resonator1__ListeningXL=1,
                                Resonator1__ListeningXR=0), {}, False),
          ('bleed_1', dict(Resonator1__Type=2, Resonator1__Quality=0, Resonator1__Decay=0.75, Resonator1__Bleed=1), {}, False),
          ('note_36', dict(Resonator1__Type=0, Resonator1__Quality=2, Resonator1__Decay=0.75), dict(n=36), False),
          ('note_84', dict(Resonator1__Type=0, Resonator1__Quality=2, Resonator1__Decay=0.75), dict(n=84), False),
          ('res2_marimba_tr7', dict(Resonator1__OnOff=0, Resonator2__OnOff=1, ResonatorOrder=1, Resonator2__Type=1, Resonator2__Quality=2,
                                    Resonator2__Decay=0.75, Resonator2__Transpose=7), dict(res=2), True)]
MODAL += [(f'stiff_{v}', dict(Resonator1__Type=2, Resonator1__Quality=2, Resonator1__Decay=0.75, Mallet__Stiffness=v), dict(n=48), v in (0.15, 1))
          for v in (0.15, 0.3, 0.7, 1)]


def resonator():
    return par(lambda c: modal(c[0], c[1], keep=c[3], **c[2]), MODAL)


# ---------------------------------------------------------------- mallet
def mallet():
    out = {}
    ev = note(60, 100, on=0, dur=None)
    base = run('mv_base', P(**Q), ev, 16384)[:, 0]
    rows = []
    for v in (0, 0.1, 0.25, 0.4, 0.6, 0.75, 1):
        g, res = fitg(run(f'mv_{v}', P(**Q, Mallet__Volume=v), ev, 16384)[:, 0], base)
        pred = {m: model.expo(c, 0.001, 1) / model.expo(64, 0.001, 1)
                for m, c in (('floor', math.floor(model.U(v))), ('floor+0.4', math.floor(model.U(v) + 0.4)), ('none', model.U(v)))}
        rows.append(dict(volume=v, gain=g, residual=res, **{f'pred_{k}': p for k, p in pred.items()}))
    out['volume'] = rows
    # mallet noise mix: y(n) = (1 - n) D + n N for one seed; solve D, N from two settings, predict the others
    amts = {v: run(f'mn_{v}', P(Mallet__NoiseAmount=v), ev, 16384) for v in (0, 0.25, 0.5, 0.75, 1)}

    def nmix(v, rule):
        c = model.U(v)
        c = model.TR(c) if rule == 'TR' else c
        a = model.lin(c, -4, 4)
        return (math.atan(a) / math.pi + 0.5) ** 3
    res = {}
    for rule in ('TR', 'none'):
        n1, n2 = nmix(0.5, rule), nmix(1, rule)
        Dm = (n2 * amts[0.5] - n1 * amts[1]) / (n2 - n1)
        Nm = (amts[1] - (1 - n2) * Dm) / n2
        res[rule] = {str(v): float(np.sqrt((((1 - nmix(v, rule)) * Dm + nmix(v, rule) * Nm - amts[v]) ** 2).mean() / (amts[v] ** 2).mean()))
                     for v in (0, 0.25, 0.75)}
        res[rule + '_n'] = {str(v): nmix(v, rule) for v in amts}
    out['noise_mix'] = res
    return out


# ---------------------------------------------------------------- velocity and key
def velocity():
    out = {}
    ev = lambda n, v: note(n, v, on=0, dur=None)  # noqa: E731
    rows = []
    b0 = run('vel_base', P(**Q), ev(60, 100), 16384)[:, 0]
    for v in (1, 64, 127):
        y = run(f'vel_none_{v}', P(**Q), ev(60, v), 16384)[:, 0]
        rows.append(dict(amount=0, velocity=v, bit_identical_to_v100=bool(np.array_equal(y, b0))))
    for amt in (1, 2.5, 5, -2.5):
        for v in (1, 32, 64, 100, 127):
            g, r = fitg(run(f'vel_{amt}_{v}', P(**Q, Mallet__VelToVolume=amt), ev(60, v), 16384, keep=(amt == 2.5 and v in (1, 127)))[:, 0], b0)
            rows.append(dict(amount=amt, velocity=v, gain_db=db(g), residual=r, source=(v - 64) / 63))
    k = [r for r in rows if r.get('amount') and r['velocity'] != 64]
    F = float(np.median([r['gain_db'] / (20 * math.log10(2) * r['amount'] * r['source']) for r in k]))
    out['vel_to_volume'] = dict(rows=rows, factor_octaves_per_amount=F,
                                max_dev_db=max(abs(r['gain_db'] - 20 * math.log10(2) * F * r['amount'] * r['source']) for r in k))
    rows = []
    for n in (36, 48, 72, 84):
        b = run(f'key_base_{n}', P(**Q), ev(n, 100), 16384)[:, 0]
        for amt in (1, -1):
            g, r = fitg(run(f'key_{amt}_{n}', P(**Q, Mallet__KeyToVolume=amt), ev(n, 100), 16384)[:, 0], b)
            rows.append(dict(amount=amt, note=n, gain_db=db(g), residual=r, source=(n - 60) / 12,
                             pred_db=20 * math.log10(2) * F * amt * (n - 60) / 12))
    out['key_to_volume'] = rows
    # VelToStiffness: effective mallet corner from the graded mode amplitudes (String, note 48)
    rows = []
    for amt, v in ((0, 100), (1, 127), (1, 100), (1, 1), (2.5, 127), (2.5, 1), (-1, 127)):
        kw = dict(Resonator1__Type=2, Resonator1__Quality=2, Resonator1__Decay=0.75, Mallet__VelToStiffness=amt)
        res = modal(f'vstiff_{amt}_{v}', kw, n=48, vel=v, keep=(amt, v) == (2.5, 127))
        f = np.array([r['model_hz'] for ch in res['channels'] for r in ch['rows'] if r['weight'] >= 1e-2])
        ratio = np.array([abs(complex(*r['amp']) / complex(*r['model'])) for ch in res['channels'] for r in ch['rows'] if r['weight'] >= 1e-2])

        def lp(fc):
            w = min(2 * math.pi * fc / FS, 2.9919932)
            s_, c = math.sin(w), math.cos(w)
            z = np.exp(-2j * np.pi * f / FS)
            return np.abs((0.5 + z + 0.5 * z * z) / (1 - 2 * c / (1 + s_) * z + (1 - s_) / (1 + s_) * z * z))
        f0 = model.expo(64, 2, 5000)
        grid = np.exp(np.linspace(np.log(20), np.log(8000), 6000))
        err = [np.std(np.log(ratio * lp(f0) / lp(fc))) for fc in grid]
        fc = float(grid[int(np.argmin(err))])
        rows.append(dict(amount=amt, velocity=v, modes=int(len(f)), corner_hz=fc, fit_log_sd=float(min(err)),
                         octaves_vs_default=math.log2(fc / f0), pred_octaves=F * amt * (v - 64) / 63))
    out['vel_to_stiffness'] = rows
    return out


# ---------------------------------------------------------------- levels and coupling
def levels():
    out = {}
    ev = note(60, 100, on=0, dur=None)
    b = run('lv_base', P(**Q), ev, 16384)

    def table(name, vals, key, on=0):
        ref = b if on == 0 else run(f'lv_base_{on}', P(**Q), note(60, 100, on=on, dur=None), on + 16384)[on:]
        rows = []
        for v in vals:
            y = run(f'lv_{name}_{v}', P(**Q, **{key: v}), note(60, 100, on=on, dur=None), on + 16384)[on:]
            gl, rl = fitg(y[:, 0], ref[:, 0])
            gr, rr = fitg(y[:, 1], ref[:, 1])
            rows.append(dict(value=v, controller=model.U(v) if name != 'pan' else model.K1(v, -1, 1),
                             left_db=db(gl), right_db=db(gr), residual=max(rl, rr) if gl and gr else None))
        return rows
    out['volume'] = table('volume', (0, 0.1, 0.25, 0.4, 0.5, 0.6, 0.7047892213, 0.9, 1), 'Volume', on=4096)
    y0 = run('lv_start_0.25', P(**Q, Volume=0.25), ev, 16384, warm=False)   # note at the instance's first frame
    b0 = run('lv_start_base', P(**Q), ev, 16384, warm=False)
    g_late = fitg(y0[4096:, 0], b0[4096:, 0])[0]
    k = np.nonzero(np.abs(y0[:, 0] - g_late * b0[:, 0]) > 1e-3 * np.abs(y0[:, 0]).max())[0]
    out['volume_start'] = dict(volume=0.25, settled_gain_db=db(g_late), last_frame_off_settled=int(k[-1]) if len(k) else None,
                               first_frame_gain=float(y0[np.argmax(np.abs(b0[:, 0]) > 0), 0] / b0[np.argmax(np.abs(b0[:, 0]) > 0), 0]))
    out['res_volume'] = table('resvol', (0, 0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9, 1), 'Resonator1__Volume')
    out['pan'] = table('pan', (-1, -0.75, -0.5, -0.25, -0.1, 0, 0.1, 0.25, 0.5, 0.75, 1), 'Resonator1__Pan')
    # coupling
    r1 = run('cp_r1', P(**Q), ev, 16384)
    two = dict(Resonator2__OnOff=1, Resonator2__Type=1, Resonator2__Transpose=7)
    r2 = run('cp_r2', P(**Q, Resonator1__OnOff=0, ResonatorOrder=1, **two), ev, 16384)
    pp = run('coupling_parallel', P(**Q, ResonatorOrder=1, **two), ev, 32768, keep=True)
    s = run('coupling_serial', P(**Q, ResonatorOrder=0, **two), ev, 32768, keep=True)
    s_v2 = run('cp_s_v2', P(**Q, ResonatorOrder=0, **two, Resonator2__Volume=0), ev, 16384)
    s_v1 = run('cp_s_v1', P(**Q, ResonatorOrder=0, **two, Resonator1__Volume=0), ev, 16384)
    s_p = run('cp_s_p', P(**Q, ResonatorOrder=0, **two, Resonator1__Volume=0, Resonator1__Pan=-1), ev, 16384)
    s_x = run('cp_s_x', P(**Q, ResonatorOrder=0, **two, Resonator1__Volume=0, Resonator1__ListeningXL=0.9, Resonator1__ListeningXR=0.1), ev, 16384)
    s_r2only = run('cp_s_r2only', P(**Q, ResonatorOrder=0, Resonator1__OnOff=0, **two), ev, 16384)
    same1 = run('cp_same1', P(**Q), ev, 16384)
    same2 = run('cp_same2', P(**Q, Resonator1__OnOff=0, Resonator2__OnOff=1, ResonatorOrder=1), ev, 16384)
    out['coupling'] = dict(
        parallel_minus_sum=float(np.abs(pp[:16384] - (r1 + r2)).max()), parallel_peak=float(np.abs(pp).max()),
        res2_alone_equals_res1_alone_same_settings=bool(np.array_equal(same1, same2)),
        serial_peak=float(np.abs(s).max()),
        serial_res2_volume0_vs_res1=fitg(s_v2[:, 0], r1[:, 0]),
        serial_res1_volume0_peak=float(np.abs(s_v1).max()),
        serial_res1_volume0_res1_pan_change_max_diff=float(np.abs(s_v1 - s_p).max()),
        serial_res1_pickups_swapped_max_diff=float(np.abs(s_v1 - s_x).max()),
        serial_res2_only_peak=float(np.abs(s_r2only).max()),
        serial_equals_res1_part_plus_res2_part=float(np.abs(s[:16384] - (s_v2 + s_v1)).max()))
    return out


# ---------------------------------------------------------------- note-off, voices, pitch envelope, waveguides
def noteoff():
    out = {}
    q = P(**Q)
    held = run('no_held', q, note(60, 100, on=0, dur=None), 44100)
    rel = run('no_rel', q, note(60, 100, on=0, dur=11025), 44100)
    out['default_offdecay_host1_max_diff'] = float(np.abs(rel - held).max())
    rows = []
    for hv in (0, 0.1, 0.25, 0.5, 0.75, 0.9, 1):
        qq = P(**Q, Resonator1__Type=2, Resonator1__Quality=0, Resonator1__Decay=0.75, Resonator1__DecayOnNoteOff=hv)
        y = run(f'no_{hv}', qq, note(60, 100, on=0, dur=11025), 11025 + 32768, keep=(hv == 0.5))
        a = fit.track(y[:11025, 0], 261.62, FS, 512, 20)
        tail = y[:11025 + 8192, 0]
        b = fit.track(tail, 261.62, FS, 11025 + 64, 20) if np.abs(y[11025 + 400:11025 + 8192]).max() > 1e-9 else None
        T = lambda t: -math.log(1000) / (t['log_radius'] * FS)  # noqa: E731
        rows.append(dict(host=hv, stored=1 - hv, t60_held_s=T(a), t60_after_off_s=T(b) if b else None))
    out['offdecay'] = rows
    return out


def voices():
    notes = [48 + 2 * k for k in range(24)]
    rows = []
    for poly in range(9):
        q = P(**Q, Resonator1__Type=2, Resonator1__Quality=0, Resonator1__Decay=0.75, Polyphony=poly)
        ev = [(2000 * k, 0x90, n, 100) for k, n in enumerate(notes)]
        end = 2000 * len(notes) + 1000
        y = run(f'poly_{poly}', q, ev, end + 8192)
        seg = y[end:end + 8192, 0] * np.hanning(8192)
        t = np.arange(8192)
        lv = np.array([abs((seg * np.exp(-2j * np.pi * 261.62 * model.A((n - 60) / 12) * t / FS)).sum()) for n in notes])
        alive = [n for n, l in zip(notes, lv) if l > 1e-3 * lv.max()]
        rows.append(dict(index=poly, voices=len(alive), sounding=alive))
    # stealing: one voice; the second note takes it over
    q = P(**Q, Resonator1__Type=2, Resonator1__Quality=0, Resonator1__Decay=0.75, Polyphony=0)
    both = run('steal_both', q, [(0, 0x90, 60, 100), (11025, 0x90, 67, 100)], 22050, keep=True)
    alone = run('steal_alone', q, [(11025, 0x90, 67, 100)], 22050)
    first = run('steal_first', q, [(0, 0x90, 60, 100)], 22050)
    d = both - alone                                   # what is left of the first note
    g = grid_rule(11025, 512, 44)
    return dict(polyphony=rows, steal=dict(takeover_frame=g, first_note_before=float(np.abs(d[g - 64:g, 0]).max()),
                                          first_note_after=float(np.abs(d[g:g + 4096, 0]).max()),
                                          untouched_first_after=float(np.abs(first[g:g + 64, 0]).max())))


def pitch_env():
    rows = []
    for st, tm in ((1, 0.5), (0.5, 0.5), (-1, 0.5), (1, 0.25), (1, 0.75)):
        q = P(**Q, Resonator1__Type=2, Resonator1__Quality=0, Resonator1__Decay=1, Resonator1__StartTranspose=st, Resonator1__StartTime=tm)
        y = run(f'penv_{st}_{tm}', q, note(60, 100, on=0, dur=None), 32768, keep=(st, tm) == (1, 0.5))
        traj = {}
        for ms in (10, 20, 50, 100, 200, 400):
            a = int(ms * FS / 1000)
            seg = y[a:a + 882, 0]                     # 20 ms around each time
            traj[ms] = 12 * math.log2(peak_hz(seg, lo_hz=60.0) / 261.62)
        rows.append(dict(start=st, time=tm, semitones_at_ms=traj))
    return rows


def waveguides():
    rows = []
    for tag, kw, fs, keep in (('wg_pipe', dict(Resonator1__Type=5), FS, True), ('wg_tube', dict(Resonator1__Type=6), FS, True),
                              ('wg_pipe_48', dict(Resonator1__Type=5), 48000, False), ('wg_tube_48', dict(Resonator1__Type=6), 48000, False),
                              ('wg_pipe_r1', dict(Resonator1__Type=5, Resonator1__Radius=1), FS, False),
                              ('wg_pipe_op0.3', dict(Resonator1__Type=5, Resonator1__TubeOpening=0.3), FS, False),
                              ('wg_tube_r0', dict(Resonator1__Type=6, Resonator1__Radius=0), FS, False)):
        y = run(tag, P(**Q, Resonator1__Decay=1, **kw), note(60, 100, on=0, dur=None), 32768, fs=fs, keep=keep)
        live = np.nonzero(np.abs(y[:, 0]) > 1e-4 * np.abs(y[:, 0]).max())[0][-1]
        a0 = 64 if live < 8192 else 2048
        est = peak_hz(y[a0:min(live, a0 + 16384), 0], fs, lo_hz=60.0)
        hz = fit.track(y[:live, 0], est, fs, a0, 20)['hz'] if live >= 8192 else est   # heavily damped: spectral peak only
        rows.append(dict(case=tag, fs=fs, fundamental_hz=hz, channels_identical=bool(np.array_equal(y[:, 0], y[:, 1]))))
    return rows


# ---------------------------------------------------------------- range mismatches, flags, residual, random draws
def extras():
    out = {}
    ev = note(60, 100, on=0, dur=None)
    base = dict(Mallet__NoiseAmount=0, Resonator1__OnOff=0, Resonator2__OnOff=1, ResonatorOrder=1)
    y = {t: run(f'mm_res2_type{t}', P(**base, Resonator2__Type=t), ev, 16384) for t in (4, 5, 6)}
    r1 = {t: run(f'mm_res1_type{t}', P(**Q, Resonator1__Type=t), ev, 16384) for t in (5, 6)}
    out['res2_type6_equals_type5'] = bool(np.array_equal(y[6], y[5]))
    out['res2_type6_equals_type4'] = bool(np.array_equal(y[6], y[4]))
    out['res1_type6_equals_type5'] = bool(np.array_equal(r1[6], r1[5]))
    b1 = dict(Resonator1__Type=2, Resonator1__Quality=0, Resonator1__Decay=1, Resonator1__StartTranspose=0.5)
    rows = []
    for v in (1, 64, 100, 127):
        a0 = run('mm_vst_0', P(**Q, **b1), note(60, v, on=0, dur=None), 16384)
        for amt in (-1, 1, 3):
            a = run('mm_vst', P(**Q, **b1, Resonator1__VelToStartTranspose=amt), note(60, v, on=0, dur=None), 16384)
            rows.append(dict(velocity=v, amount=amt, bit_identical_to_amount0=bool(np.array_equal(a, a0))))
    out['vel_to_start_transpose'] = rows
    # activity flag and the residual of a held, decayed voice
    for tag, kw, frames in (('flag_decay0', dict(Resonator1__Decay=0), 132300), ('resid_string_low_d0.25',
                            dict(Resonator1__Type=2, Resonator1__Quality=1, Resonator1__Decay=0.25), 66150)):
        yy = run(tag, P(**Q, **kw), ev, frames)
        tail = yy[frames // 2:]
        out[tag] = dict(process=[l for l in LOG[tag].splitlines() if l.startswith('process')][-1],
                        peak=float(np.abs(yy).max()), tail_peak=float(np.abs(tail).max()),
                        tail_unique_values=int(len(np.unique(tail[:, 0]))))
    # random draws per voice and frame
    for tag, events in (('rand_none', []), ('rand_one', note(60, 100, on=0, dur=None)),
                        ('rand_two', note(60, 100, on=0, dur=None) + note(67, 100, on=0, dur=None))):
        run(tag, P(**Q), events, 44100)
        out[tag] = {k: v for k, v in xdevpy.used_imports(LOG[tag]).items() if k in ('_rand', '_srand', '_time')}
    # CalcA return value in a loud serial render
    run('ret_serial', P(**Q, Resonator2__OnOff=1, ResonatorOrder=0, Volume=1), ev, 20480)
    out['ret_serial_volume1'] = [l for l in LOG['ret_serial'].splitlines() if l.startswith('process')][-1]
    return out


def main():
    xdevpy.build()
    RAW.mkdir(exist_ok=True)
    RES.mkdir(exist_ok=True)
    SCR.mkdir(parents=True, exist_ok=True)
    for name, fn in (('root_cause', root_cause), ('protocol', protocol), ('timing', timing), ('pitch', pitch),
                     ('resonator', resonator), ('mallet', mallet), ('velocity', velocity), ('levels', levels),
                     ('noteoff', noteoff), ('voices', voices), ('pitch_env', pitch_env), ('waveguides', waveguides),
                     ('extras', extras)):
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        OUT[name] = fn()
        print(name, 'done', flush=True)
    path = RES / 'collision.json'
    old = json.loads(path.read_text()) if path.exists() and len(sys.argv) > 1 else {}
    old.update(OUT)
    kept = old.get('reference_renders', {})
    kept.update(KEPT)
    old['reference_renders'] = kept
    old['slice'] = dict(bundle=str(xdevpy.BUNDLES['Collision']), loader=str(xdevpy.BIN))
    path.write_text(json.dumps(old, indent=1, default=lambda o: [o.real, o.imag] if isinstance(o, complex) else str(o)) + '\n')


if __name__ == '__main__':
    os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
    main()
