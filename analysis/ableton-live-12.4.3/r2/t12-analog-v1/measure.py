"""Measurements of Analog's signal behavior from renders of the bundle's x86_64 slice.

    python3 -I measure.py AREA [AREA ...]      # writes results/<area>.json

Each area renders single-parameter variations of a probe set (stored values, an.stored) and reduces
every render to the quantity the spec states (a frequency, a level, a time ...). Renders are not
kept; cases.py writes the retained reference renders. The probe set is the table defaults with
both envelopes of chain 1 held at sustain 1 (so the voice sounds steadily while the key is held)
and, unless an area says otherwise, the sine shape. Dependencies: numpy, scipy, an, model, fit.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import an  # noqa: E402
import model  # noqa: E402

C1, C2 = 'SignalChain1/', 'SignalChain2/'
FE, AE = C1 + 'Envelope.0/', C1 + 'Envelope.1/'
PROBE = {FE + 'SustainLevel': 1, AE + 'SustainLevel': 1, C1 + 'OscillatorWaveShape': 0}
RESULTS = HERE / 'results'


def probe(**ch):
    return an.stored('table', **{**PROBE, **ch})


def save(area, data):
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f'{area}.json').write_text(json.dumps(data, indent=1, default=float) + '\n')
    print(area, 'written')


def held(st, key=60, fs=44100, secs=1.0, vel=100):
    """Render a key held for secs from frame on = 100 control periods; returns (left channel, on, off)."""
    on = (fs // 1000) * 100
    off = on + int(secs * fs)
    y, _ = an.render(st, an.note(key, vel, on, off), fs=fs, frames=off + fs // 5)
    return y, on, off


def cents(a, b):
    return 1200 * np.log2(a / b)


# ---- pitch -------------------------------------------------------------------------------------

def area_pitch():
    items = [dict(key=k, fs=fs) for fs in (44100, 48000) for k in range(24, 109)]
    items += [dict(key=60, fs=fs, osc_oct=o) for fs in (44100, 48000) for o in (-3, -2, -1, 1, 2, 3)]
    items += [dict(key=60, fs=fs, osc_semi=s) for fs in (44100, 48000) for s in range(-12, 13) if s]
    items += [dict(key=k, fs=44100, octave=o) for k in (48, 72) for o in (-3, -1, 1, 2)]
    items += [dict(key=k, fs=44100, transpose=t) for k in (48, 72) for t in (-12, -7, -1, 1, 5, 12)]
    grid = [i / 16 for i in range(17)] + [0.3, 0.503, 0.7]
    items += [dict(key=60, fs=fs, detune=v) for fs in (44100, 48000) for v in grid if v != 0.5]
    items += [dict(key=60, fs=44100, fine=v) for v in grid if v != 0.5]
    items += [dict(key=k, fs=44100, stretch=v) for k in (24, 48, 69, 96, 108) for v in (0, 0.25, 0.75, 1)]
    items += [dict(key=k, fs=44100, stretch=s, transpose=t, octave=o, fine=f) for k in (36, 84)
              for s, t, o, f in ((0, 5, 0, 0.5), (1, 0, 1, 0.5), (0, 0, 0, 0), (1, -7, -1, 1))]
    names = dict(osc_oct=C1 + 'OscillatorOct', osc_semi=C1 + 'OscillatorSemi', detune=C1 + 'OscillatorDetune',
                 octave='Octave', transpose='Transpose', fine='KeyboardFineTune', stretch='KeyboardStretch')

    def run(it):
        ch = {names[k]: v for k, v in it.items() if k in names}
        m = model.osc_freq(**it)
        y, on, off = held(probe(**ch), it['key'], it['fs'], secs=1.0 if m > 200 else 4.0)
        f = an.fund(y[on + it['fs'] // 10:off, 0], it['fs'])
        return dict(it, hz=f, model_hz=m, err_cents=cents(f, m), et_cents=cents(f, 440 * 2 ** ((it['key'] - 69) / 12)))

    rows = an.pmap(run, items)
    worst = max(abs(r['err_cents']) for r in rows)
    save('pitch', dict(rows=rows, n=len(rows), max_abs_err_cents=worst,
                       max_rel_err=max(abs(r['hz'] / r['model_hz'] - 1) for r in rows)))
    print('pitch: worst |render - model|', worst, 'cents over', len(rows))


# ---- oscillator shapes and pulse width -----------------------------------------------------------

def duty_fit(amps):
    """Duty d of a pulse train from harmonic amplitudes |sin(pi k d)| / k (least squares over d)."""
    k = np.arange(1, len(amps) + 1)
    ds = np.linspace(0.001, 0.5, 49901)
    shape = np.abs(np.sin(np.pi * np.outer(ds, k))) / k
    scale = (shape @ amps) / (shape ** 2).sum(1)
    err = ((shape * scale[:, None] - amps) ** 2).sum(1)
    i = int(np.argmin(err))
    return float(ds[i]), float(scale[i]), float(np.sqrt(err[i] / len(amps)))


def area_osc():
    rows = []
    def run(it):
        ch = {C1 + 'OscillatorWaveShape': it['shape']}
        if 'pw' in it:
            ch[C1 + 'OscillatorPulseWidth'] = it['pw']
        y, on, off = held(probe(**ch), it['key'], 44100, secs=1.0)
        f = model.osc_freq(it['key'], 44100)
        x = y[on + 4410:off, 0].astype(float)
        nh = int(22050 // f)
        a, ph, res, dc = an.harmonics(x, 44100, f, min(nh, 60))
        r = dict(it, hz=f, harmonics=a.tolist(), phases=ph.tolist(), residual_rms=res, dc=dc,
                 rms=float(np.sqrt((x ** 2).mean())), peak=float(np.abs(x).max()), max=float(x.max()), min=float(x.min()),
                 onset=y[on:on + 8, 0].tolist(), channels_identical=bool(np.array_equal(y[:, 0], y[:, 1])))
        if it['shape'] == 2:
            r['duty'], r['duty_scale'], r['duty_fit_rms'] = duty_fit(a[:min(nh, 40)])
        return r
    items = [dict(shape=s, key=k) for s in (0, 1, 2) for k in (36, 60, 84, 96)]
    items += [dict(shape=2, key=60, pw=v) for v in (0, 0.1, 0.25, 0.4, 0.49, 0.503, 0.6, 0.75, 0.9, 1)]
    items += [dict(shape=s, key=60, pw=v) for s in (0, 1) for v in (0, 1)]
    rows = an.pmap(run, items)
    save('osc', dict(rows=rows))
    for r in rows:
        print(r['shape'], r['key'], r.get('pw'), 'rms %.5f peak %.5f dc %.2e res %.2e' % (r['rms'], r['peak'], r['dc'], r['residual_rms']),
              'h1..4', ' '.join('%.5f' % v for v in r['harmonics'][:4]), 'duty %s' % r.get('duty'))


# ---- levels ------------------------------------------------------------------------------------

def steady_rms(st, key=60, secs=0.5):
    y, on, off = held(st, key, 44100, secs=secs)
    x = y[on + 4410:off].astype(float)
    return float(np.sqrt((x[:, 0] ** 2).mean())), float(np.sqrt((x[:, 1] ** 2).mean()))


def area_levels():
    grid = (0, 0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8062000275, 0.869, 0.9, 1)
    params = {C1 + 'OscillatorLevel': ('exp', 0.01, 3.0), C1 + 'AmplifierLevel': ('exp', 0.01, 2.0),
              'Volume': ('square', 0, 2.0)}
    items = [(p, v) for p in params for v in grid]
    items += [(C1 + 'OscillatorBalance', v) for v in (0, 0.25, 0.5, 0.75, 1)]
    ref = steady_rms(probe())

    def run(it):
        p, v = it
        return dict(param=p, value=v, rms=steady_rms(probe(**{p: v})))
    rows = an.pmap(run, items)
    for r in rows:
        r['gain_db'] = 20 * np.log10(max(r['rms'][0], 1e-30) / ref[0])
        if r['param'] in params:
            kind, lo, hi = params[r['param']]
            d = an.stored('table')[r['param']]
            g = (lambda v: model.expo_smooth(model.ctl(v), lo, hi)) if kind == 'exp' else (lambda v: float(model.square(model.ctl(v), lo, hi)))
            r['model_db'] = 20 * np.log10(max(g(r['value']), 1e-30) / g(d))
    save('levels', dict(reference_rms=ref, rows=rows))
    for r in rows:
        print(r['param'], r['value'], '%.4f dB' % r['gain_db'], 'model %.4f' % r['model_db'] if 'model_db' in r else '', r['rms'])


# ---- noise -------------------------------------------------------------------------------------

NOISE = {C1 + 'OscillatorToggle': 0, 'NoiseToggle': 1, 'NoiseBalance': 1}


def psd(x, fs=44100, nper=8192):
    from scipy.signal import welch
    return welch(np.asarray(x, float), fs, nperseg=nper)


def noise_color_h(f, v, fs=44100):
    """Model color filter: one-pole low-pass y += a (x - y), a = min(1, 2 pi fc / fs), fc = 20 * 1100^(c / 127)."""
    a = min(1.0, 2 * np.pi * model.expo_smooth(model.ctl(v), 20, 22000) / fs)
    return a / (1 - (1 - a) * np.exp(-2j * np.pi * f / fs))


def area_noise():
    """Noise source alone into filter 1 (filter off). The same seed gives the same noise sequence, so the
    color filter's transfer function is the cross-spectrum against Color 1 (no filtering)."""
    from scipy.signal import csd, welch
    items = [('NoiseColor', v) for v in (0, 0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8, 0.9, 1)]
    items += [('NoiseLevel', v) for v in (0.25, 0.5, 1)] + [('NoiseBalance', v) for v in (0, 0.25, 0.5, 0.75)]
    items += [('seed', t) for t in ('1', '1760000000')] + [('key', k) for k in (36, 96)]
    on, off = 4400, 4400 + 3 * 44100

    def run(it):
        p, v = it
        st = probe(**{**NOISE, **({p: v} if p in ('NoiseColor', 'NoiseLevel', 'NoiseBalance') else {})})
        y, _ = an.render(st, an.note(v if p == 'key' else 60, 100, on, off), frames=off + 4410,
                         env={'XDEV_TIME': v} if p == 'seed' else None)
        return it, y[on + 4410:off, 0].astype(float)
    got = an.pmap(run, items)
    raw = dict(got)[('NoiseColor', 1)]
    f, Pxx = welch(raw, 44100, nperseg=4096)
    grid = [50, 100, 200, 400, 800, 1600, 3200, 6400, 10000, 15000, 20000]
    idx = [int(np.argmin(abs(f - g))) for g in grid]
    rows = []
    for (p, v), x in got:
        r = dict(param=p, value=v, rms=float(x.std()), mean=float(x.mean()), peak=float(np.abs(x).max()))
        if r['rms'] > 0:
            r['rms_ratio_db'] = float(20 * np.log10(r['rms'] / raw.std()))
            r['kurtosis'] = float(((x - x.mean()) ** 4).mean() / x.var() ** 2)
        if p == 'NoiseColor':
            _, Pxy = csd(raw, x, 44100, nperseg=4096)
            H = Pxy / Pxx
            Hm = noise_color_h(f, v)
            r['h_db'] = {str(grid[j]): float(20 * np.log10(abs(H[i]))) for j, i in enumerate(idx)}
            band = (f > 30) & (f < 20000)
            r['max_abs_db_vs_model'] = float(np.max(np.abs(20 * np.log10(abs(H[band]) / abs(Hm[band])))))
            r['max_abs_deg_vs_model'] = float(np.max(np.abs(np.degrees(np.angle(H[band] / Hm[band])))))
        rows.append(r)
    save('noise', dict(raw_psd_db={str(grid[j]): float(10 * np.log10(Pxx[i])) for j, i in enumerate(idx)}, rows=rows))
    for r in rows:
        print(r['param'], r['value'], 'rms %.5f mean %.1e peak %.4f' % (r['rms'], r['mean'], r['peak']), r.get('rms_ratio_db'),
              r.get('kurtosis'), r.get('max_abs_db_vs_model'), r.get('max_abs_deg_vs_model'))

# ---- filters -----------------------------------------------------------------------------------

FNOISE = {**NOISE, 'NoiseColor': 1, 'NoiseLevel': 0.25}


def arx(x, y, nb, na, n0=2000, N=40000):
    """Least-squares IIR fit y[n] = sum b_k x[n-k] - sum a_k y[n-k]; returns b, a (a[0] = 1), relative residual."""
    X = np.array([x[n0 - k:n0 - k + N] for k in range(nb)] + [-y[n0 - k:n0 - k + N] for k in range(1, na + 1)]).T
    t = y[n0:n0 + N]
    c, *_ = np.linalg.lstsq(X, t, rcond=None)
    res = t - X @ c
    return c[:nb], np.concatenate([[1], c[nb:]]), float(np.sqrt((res ** 2).mean() / (t ** 2).mean()))


def biquad_params(a, fs):
    """Bilinear (prewarped) two-pole denominator 1 + a1 z^-1 + a2 z^-2 -> (fc Hz, Q, 1/D)."""
    a1, a2 = a[1], a[2]
    K = (1 - a1 + a2) / 4
    g = np.sqrt((1 + a1 + a2) / (1 - a1 + a2))
    q = 2 * g * K / (1 - a2)
    return float(np.arctan(g) * fs / np.pi), float(q), float(K)


def area_filter():
    on = 4400
    def run(it):
        fs = it.get('fs', 44100)
        ch = {**FNOISE, **{C1 + k: v for k, v in it['set'].items()}}
        key = it.get('key', 60)
        y0, _ = an.render(probe(**{**FNOISE, **({C1 + 'FilterKbdCutoffMod': 0} if 0 else {})}), an.note(key, 100, on, on + fs * 2), fs=fs, frames=on + fs * 2)
        y1, _ = an.render(probe(**ch), an.note(key, 100, on, on + fs * 2), fs=fs, frames=on + fs * 2)
        x, y = y0[on + 4400:, 0].astype(float), y1[on + 4400:, 0].astype(float)
        t = int(it['set'].get('FilterType', 0))
        order = 4 if t in (1, 3, 5, 7) else 2
        b, a, rel = arx(x, y, order + 1, order)
        r = dict(it, order=order, b=b.tolist(), a=a.tolist(), rel_residual=rel)
        if order == 2:
            r['fc_hz'], r['Q'], _ = biquad_params(a, fs)
        else:
            r['section_a'] = [1.0, a[1] / 2, float(np.sqrt(abs(a[4])))]
            r['square_check'] = float(abs(a[2] - (a[1] ** 2 / 4 + 2 * np.sqrt(abs(a[4])))) + abs(a[3] - a[1] * np.sqrt(abs(a[4]))))
            r['fc_hz'], r['Q'], _ = biquad_params(r['section_a'], fs)
        c = model.ctl(it['set'].get('FilterCutoffFrequency', 1))
        r['model_fc_hz'] = model.expo_smooth(c, 30, 22000)
        return r
    F = dict(FilterToggle=1)
    items = []
    for fs in (44100, 48000):
        for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.503, 0.6, 0.7, 0.8, 0.9, 0.95):
            items.append(dict(fs=fs, set=dict(F, FilterType=0, FilterCutoffFrequency=v, FilterQFactor=0.3)))
    for q in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.503, 0.6, 0.7, 0.8, 0.9, 1):
        for t in (0, 1):
            items.append(dict(set=dict(F, FilterType=t, FilterCutoffFrequency=0.5, FilterQFactor=q)))
    for t in range(8):
        for q in (0, 0.6):
            items.append(dict(set=dict(F, FilterType=t, FilterCutoffFrequency=0.4, FilterQFactor=q)))
    for k in (36, 84):
        for m in (-1, -0.5, 0.5, 1):
            items.append(dict(key=k, set=dict(F, FilterType=0, FilterCutoffFrequency=0.5, FilterQFactor=0.3, FilterKbdCutoffMod=m)))
    rows = an.pmap(run, items)
    save('filter', dict(rows=rows))
    for r in rows:
        print(r.get('fs', 44100), r.get('key', 60), r['set'], 'rel %.1e' % r['rel_residual'], 'fc %.3f model %.3f Q %.4f' % (r['fc_hz'], r['model_fc_hz'], r['Q']),
              'b', np.round(r['b'], 6), r.get('square_check'))


# ---- envelopes ---------------------------------------------------------------------------------

EPROBE = {C1 + 'OscillatorWaveShape': 2, C1 + 'OscillatorPulseWidth': 1}     # 50 % pulse: |x| >= 0.12 between edges


def env_curve(st, events, frames, env_index=99, fs=44100, ref_off=None):
    """Per-frame gain of the amplitude envelope: the render divided by a reference render with the
    envelope's unstored ToggleDummy (host index 99 for chain 1's amplitude envelope) set to 0, which
    removes the envelope (a measurement device; Live always sends 1). The reference keeps its key
    held to the end, so that it still sounds during the release. NaN where |reference| < 1e-4."""
    hv = an.host(st)
    y, _ = an.render(None, events, fs=fs, frames=frames, hv=hv)
    hv0 = dict(hv)
    hv0[env_index] = 0.0
    r, _ = an.render(None, [e for e in events if e[1] == 0x90], fs=fs, frames=frames, hv=hv0)
    y, r = y[:, 0].astype(float), r[:, 0].astype(float)
    ok = np.abs(r) > 1e-4
    return np.where(ok, y / np.where(ok, r, 1), np.nan), y, r


def area_env():
    """Chain 1 amplitude envelope. Each segment is compared with the segment model (model.segment)
    started at the first frame after the event's control-grid point."""
    on, fs = 4400, 44100
    def run(it):
        s = it['set']
        ch = {**EPROBE, **{AE + k: v for k, v in s.items()}}
        hold = int(it.get('hold', 1.0) * fs)
        off = on + hold
        frames = off + int(it.get('tail', 0.5) * fs)
        e, y, r = env_curve(probe(**ch), an.note(60, 100, on, off), frames)
        exp_ = bool(s.get('ExponentialSlope', 1))
        S = float(model.lin(model.ctl(s.get('SustainLevel', 1)), 0, 1))
        A, D, R = s.get('AttackTime', 0), s.get('DecayTime', 0.6000000238), s.get('ReleaseTime', 0.6000000238)
        Lr = model.env_time(R) * fs
        m = np.full(frames, np.nan)
        m[on + 1:off] = model.adsr(fs, off - on - 1, A, D, S, exp_, s.get('SustainTime', 1))
        res = dict(it, La=model.env_time(A) * fs, Ld=model.env_time(D) * fs, Lr=Lr, S=S)
        seg = slice(on + 1, off - 50)
        d = np.abs(e[seg] - m[seg])
        res['max_abs_err_hold'] = float(np.nanmax(d))
        res['worst_frame_hold'] = int(1 + np.nanargmax(d))
        g = 44 * (off // 44)                        # note-off control-grid point
        lvl = e[g]
        res['level_at_release'] = float(lvl)
        d = np.abs(e[g + 1:] - model.segment(lvl, 0, Lr, frames - g - 1, exp_))
        res['max_abs_err_release'] = float(np.nanmax(d)) if np.any(~np.isnan(d)) else None
        nz = np.nonzero(np.abs(y) > 0)[0]
        res['last_nonzero_after_grid'] = int(nz[-1]) - g
        res['curve'] = {str(k): float(e[on + k]) for k in (1, 2, 10, 100, 1000, 5000, 20000) if on + k < frames}
        return res
    items = []
    for slope in (1, 0):
        for v in (0, 0.1, 0.25, 0.4, 0.5, 0.6):
            items.append(dict(set=dict(ExponentialSlope=slope, AttackTime=v, SustainLevel=1), hold=1.5))
        for v in (0, 0.1, 0.4, 0.6):
            items.append(dict(set=dict(ExponentialSlope=slope, DecayTime=v, SustainLevel=0.5, SustainTime=1), hold=1.5))
        for v in (0, 0.1, 0.4, 0.6):
            items.append(dict(set=dict(ExponentialSlope=slope, ReleaseTime=v, SustainLevel=1), hold=0.3, tail=1.5))
        for sv in (0, 0.25, 0.5, 0.75):
            items.append(dict(set=dict(ExponentialSlope=slope, DecayTime=0.3, SustainLevel=sv), hold=1.0))
        for st in (0, 0.25, 0.5, 0.75, 0.9):
            items.append(dict(set=dict(ExponentialSlope=slope, DecayTime=0.2, SustainLevel=0.75, SustainTime=st), hold=2.5))
    rows = an.pmap(run, items)
    save('env', dict(rows=rows))
    for r in rows:
        print(r['set'], 'L %.1f %.1f %.1f' % (r['La'], r['Ld'], r['Lr']), 'err hold %.2e @%d' % (r['max_abs_err_hold'], r['worst_frame_hold']),
              'rel %s' % r['max_abs_err_release'], 'lvl %.5f' % r['level_at_release'], 'last nz +%d' % r['last_nonzero_after_grid'])

# ---- velocity ------------------------------------------------------------------------------------

def area_velocity():
    """Amplitude envelope gain while sustaining (AmpMod) and attack length (AttackMod) against note
    velocity; ratio method of env_curve."""
    on, fs = 4400, 44100
    def run(it):
        am, atm, vel = it
        ch = {**EPROBE, AE + 'AmpMod': am, AE + 'AttackMod': atm, AE + 'AttackTime': 0.4 if atm else 0}
        e, y, r = env_curve(probe(**ch), an.note(60, vel, on, on + fs), on + fs)
        k = np.nonzero(e[on:] >= 0.999999)[0]
        return dict(amp_mod=am, attack_mod=atm, velocity=vel, sustain_gain=float(np.nanmedian(e[on + 2000:on + 40000])),
                    attack_end=int(k[0]) if len(k) and atm else None,
                    model_gain=2 ** (float(model.lin(model.ctl(am), 0, 8)) / 2 * (vel - 64) / 63),
                    model_attack_frames=int(model.env_time(0.4) * fs * 2 ** (-float(model.lin(model.ctl(atm), 0, 8)) / 2 * (vel - 64) / 63)) + 1)
    items = [(am, 0, v) for am in (0, 0.25, 0.5, 0.75, 1) for v in (1, 32, 64, 100, 127)]
    items += [(0, atm, v) for atm in (0.25, 0.5, 1) for v in (1, 32, 64, 100, 127)]
    rows = an.pmap(run, items)
    save('velocity', dict(rows=rows))
    for r in rows:
        print(r)


# ---- voices --------------------------------------------------------------------------------------

def tone_amps(x, keys, fs=44100):
    t = np.arange(len(x)) / fs
    w = np.hanning(len(x))
    return [float(2 * abs(np.mean(x * np.exp(-2j * np.pi * model.osc_freq(k, fs) * t) * w)) / 0.5) for k in keys]


def area_voices():
    fs = 44100
    keys = list(range(36, 72))
    def count(p):
        ev = [(4400 + 2200 * i, 0x90, k, 100) for i, k in enumerate(keys)]
        end = 4400 + 2200 * len(keys) + 22050
        y, _ = an.render(probe(Polyphony=p), ev, frames=end)
        a = tone_amps(y[end - 16384:end, 0].astype(float), keys)
        return dict(polyphony=p, sounding=[k for k, v in zip(keys, a) if v > 0.2], amps=a)
    poly = an.pmap(count, range(10))
    ev = [(4400, 0x90, 60, 100), (13200, 0x90, 67, 100), (22000, 0x90, 64, 100), (30800, 0x80, 67, 64), (39600, 0x80, 64, 64), (48400, 0x80, 60, 64)]
    def mono(pr):
        y, _ = an.render(probe(Polyphony=0, KeyboardPriority=pr), ev, frames=fs * 3 // 2)
        t, f = an.zc_freq(y[:, 0], fs)
        return dict(priority=pr, hz_at={str(T): float(np.median(f[(t > T - 0.01) & (t < T + 0.01)])) for T in (0.2, 0.4, 0.6, 0.8, 1.0)})
    pri = an.pmap(mono, (0, 1, 2))
    save('voices', dict(events_mono=ev, polyphony=poly, priority=pri, key_hz={k: model.osc_freq(k, fs) for k in (60, 64, 67)}))
    for r in poly:
        print(r['polyphony'], len(r['sounding']), r['sounding'][:2], r['sounding'][-2:])
    for r in pri:
        print(r)


# ---- routing, filter 2 follow, drive, output saturator ---------------------------------------------

def area_routing():
    fs, on = 44100, 4400
    base2 = {C2 + 'Envelope.0/SustainLevel': 1, C2 + 'Envelope.1/SustainLevel': 1}
    def rend(ch):
        y, _ = an.render(an.stored('table', **{**PROBE, **base2, **ch}), an.note(60, 100, on, on + fs), frames=on + fs)
        return y[on + 4400:, 0].astype(float)
    N = dict(FNOISE)
    lp = {C1 + 'FilterToggle': 1, C1 + 'FilterCutoffFrequency': 0.5}
    cases = {'f1': {**N, 'NoiseBalance': 1}, 'f2': {**N, 'NoiseBalance': 0, C2 + 'AmplifierToggle': 1},
             'f2_amp2_off': {**N, 'NoiseBalance': 0}, 'f1lp': {**N, 'NoiseBalance': 1, **lp}}
    for v in (0.25, 0.5, 1):
        cases[f'ser{v}'] = {**N, 'NoiseBalance': 1, **lp, C1 + 'FilterToFilter2': v, C2 + 'AmplifierToggle': 1, C1 + 'AmplifierToggle': 0}
    R = dict(an.pmap(lambda kv: (kv[0], rend(kv[1])), cases.items()))
    out = dict(chain2_equals_chain1=bool(np.array_equal(R['f1'], R['f2'])), amp2_off_rms=float(R['f2_amp2_off'].std()),
               filter_to_filter2={})
    for v in (0.25, 0.5, 1):
        y = R[f'ser{v}']
        out['filter_to_filter2'][str(v)] = dict(gain=float(y @ R['f1lp'] / (R['f1lp'] @ R['f1lp'])),
                                                residual=float(np.abs(y - R['f1lp'] * (y @ R['f1lp'] / (R['f1lp'] @ R['f1lp']))).max()),
                                                model=2 * (float(model.ctl(v)) / 127) ** 2)
    x = rend({**N, 'NoiseBalance': 0, C2 + 'AmplifierToggle': 1})
    def follow(it):
        f1c, f2c, f1on = it
        y = rend({**N, 'NoiseBalance': 0, C2 + 'AmplifierToggle': 1, C1 + 'FilterToggle': f1on, C1 + 'FilterCutoffFrequency': f1c,
                  C2 + 'FilterToggle': 1, C2 + 'FilterCutoffFrequency': f2c, C2 + 'FilterQFactor': 0.3, C2 + 'FilterControllee': 1})
        b, a, rel = arx(x, y, 3, 2, N=30000)
        fc, Q, _ = biquad_params(a, fs)
        f1 = model.expo_smooth(model.ctl(f1c), 30, 22000)
        c2 = float(model.ctl(f2c))
        return dict(f1_cutoff=f1c, f2_cutoff=f2c, f1_on=f1on, f2_hz=fc, ratio_to_f1=fc / f1, rel=rel,
                    model_ratio=model.A((c2 - 64) / 32) if c2 < 127 else 4.0)
    out['follow'] = an.pmap(follow, [(0.5, v, 1) for v in (0, 0.1, 0.25, 0.4, 0.45, 0.49, 0.503, 0.55, 0.6, 0.75, 0.9, 1)] + [(0.3, 0.5, 1), (0.6, 0.4, 1), (0.5, 0.4, 0)])
    save('routing', out)
    print({k: v for k, v in out.items() if k != 'follow'})
    for r in out['follow']:
        print(r)


def sat(u, L, K=1.0):
    """Saturator family: |u| <= K unchanged; above, sign(u) * (L - (L - K) / (1 + (|u| - K) / (3 (L - K)))^3)."""
    a = np.abs(u)
    o = a.copy()
    k = a > K
    o[k] = L - (L - K) / (1 + (a[k] - K) / (3 * (L - K))) ** 3
    return np.sign(u) * o


def area_drive():
    """Filter Drive on a 32.7 Hz sine, filter LP12 at maximum cutoff and Q 0, amplifier low enough to stay below
    the output saturator. Fit: out = f(alpha * g * x) / alpha with x the drive-0 render scaled to the same
    oscillator gain, g the drive's input gain, f = sat with ceilings L+ and L-."""
    from scipy.optimize import least_squares
    fs = 44100
    def run(it):
        d, lvl = it
        st = probe(**{C1 + 'FilterToggle': 1, C1 + 'FilterType': 0, C1 + 'FilterCutoffFrequency': 1, C1 + 'FilterQFactor': 0,
                      C1 + 'FilterDrive': d, C1 + 'OscillatorLevel': lvl, C1 + 'AmplifierLevel': 0.4})
        y, _ = an.render(st, an.note(24, 100, 4400, 4400 + fs), frames=4400 + fs)
        return it, y[4400 + 8820:, 0].astype(float)
    R = dict(an.pmap(run, [(d, l) for d in range(7) for l in (0.5, 1.0)]))
    g = lambda v: model.expo_smooth(model.ctl(v), 0.01, 3)
    lin = R[(0, 0.5)] * g(1.0) / g(0.5)
    gains = [1, 1, 2 ** 0.5, 2, 1, 2 ** 0.5, 2]
    rows = []
    for d in range(1, 7):
        lo = R[(d, 0.5)]
        gain_low = float(lo @ R[(0, 0.5)] / (R[(0, 0.5)] @ R[(0, 0.5)]))
        xl = lin * gains[d]
        hot = R[(d, 1.0)]
        def res(p):
            a, Lp, Ln = p
            u = a * xl
            return np.where(u >= 0, sat(u, Lp), sat(u, Ln)) / a - hot
        best = min((least_squares(res, [a0, 2, 2], bounds=([0.1, 1.01, 1.01], [1000, 50, 50])) for a0 in (5, 10, 15, 20)), key=lambda s: s.cost)
        rows.append(dict(drive=d, small_signal_gain=gain_low, alpha=best.x[0], ceiling_pos=best.x[1], ceiling_neg=best.x[2],
                         max_abs_err=float(np.abs(res(best.x)).max()), peak_out=float(np.abs(hot).max())))
    save('drive', dict(rows=rows, drive0_linear_peak=float(np.abs(R[(0, 1.0)]).max())))
    for r in rows:
        print(r)


def area_output():
    """Output saturator: a saw whose linear output would exceed 2.8, against the drive-free render at a lower
    oscillator level scaled up (the gain curve of OscillatorLevel is exact)."""
    fs, on = 44100, 4400
    def run(lv):
        y, _ = an.render(probe(**{C1 + 'OscillatorLevel': lv, C1 + 'AmplifierLevel': 1, 'Volume': 1, C1 + 'OscillatorWaveShape': 1}),
                         an.note(48, 100, on, on + fs), frames=on + fs)
        return lv, y[on + 4410:, 0].astype(float)
    R = dict(an.pmap(run, [0.5, 1.0]))
    g = lambda v: model.expo_smooth(model.ctl(v), 0.01, 3)
    lin = R[0.5] * g(1.0) / g(0.5)
    m = 4 * sat(lin / 4, 1.0, 0.7)
    err = np.abs(R[1.0] - m)
    save('output', dict(max_linear=float(lin.max()), max_out=float(R[1.0].max()), max_abs_err_vs_saturator=float(err.max()),
                        rms_err=float(np.sqrt((err ** 2).mean())), samples_above_knee=int((np.abs(lin) > 2.8).sum())))
    print('output saturator max err', err.max(), 'linear max', lin.max(), 'out max', R[1.0].max())


# ---- modulation depths: filter envelope, keyboard, LFO; pitch envelope; vibrato; sub and sync -------

def area_mod():
    """Static filter-cutoff and Q modulation (filter envelope held at its sustain, keyboard tracking)
    measured as the filter's two-pole coefficients by system identification on noise."""
    fs, on = 44100, 4400
    def rend(ch, key=60):
        y, _ = an.render(probe(**{**FNOISE, **ch}), an.note(key, 100, on, on + fs), frames=on + fs)
        return y[on + 4400:, 0].astype(float)
    x = rend({})
    base = {C1 + 'FilterToggle': 1, C1 + 'FilterCutoffFrequency': 0.4, C1 + 'FilterQFactor': 0.3, FE + 'AttackTime': 0, FE + 'DecayTime': 0}
    def run(it):
        kind, m, S, key = it
        ch = {**base, FE + 'SustainLevel': S}
        ch[C1 + {'env': 'FilterEnvCutoffMod', 'envq': 'FilterEnvQMod', 'kbd': 'FilterKbdCutoffMod', 'kbdq': 'FilterKbdQMod'}[kind]] = m
        y = rend(ch, key)
        b, a, rel = arx(x, y, 3, 2, N=20000)
        fc, Q, _ = biquad_params(a, fs)
        return dict(kind=kind, amount=m, sustain=S, key=key, fc_hz=fc, Q=Q, rel=rel,
                    octaves=float(np.log2(fc / model.expo_smooth(model.ctl(0.4), 30, 22000))),
                    q_octaves=float(np.log2(Q / model.expo_smooth(model.ctl(0.3), 0.1, 120))))
    items = [('env', m, S, 60) for m in (0.25, 0.5, 0.75, -0.5) for S in (0.5, 1)]
    items += [('envq', m, 1, 60) for m in (0.25, 0.5, 1, -0.5)]
    items += [('kbd', m, 1, k) for m in (0.25, 0.5, 0.75, -0.5) for k in (48, 72)]
    items += [('kbdq', m, 1, k) for m in (0.5, 1) for k in (48, 72)]
    rows = an.pmap(run, items)
    save('mod', dict(rows=rows))
    for r in rows:
        print(r['kind'], r['amount'], r['sustain'], r['key'], 'oct %.5f qoct %.5f rel %.1e' % (r['octaves'], r['q_octaves'], r['rel']))


def pitch_track(ch, key=81, secs=2.0, on=4400, fs=44100):
    y, _ = an.render(probe(**ch), an.note(key, 100, on, on + int(secs * fs)), frames=on + int(secs * fs))
    t, f = an.zc_freq(y[on:, 0], fs)
    return t, np.log2(f / model.osc_freq(key, fs))


def area_lfo():
    """Chain 1 LFO on oscillator pitch: depth, rate, shape profile against the LFO phase counted from the
    first processed frame (free-running) and the note-on (gate reset)."""
    fs, on = 44100, 4400
    def run(it):
        shape, speed, m, pw, phase, reset = it
        t, o = pitch_track({C1 + 'LFOToggle': 1, C1 + 'LFOWaveShape': shape, C1 + 'LFOSpeed': speed, C1 + 'OscillatorLFOModPitch': m,
                            C1 + 'LFOPulseWidth': pw, C1 + 'LFOPhase': phase, C1 + 'LFOGateReset': reset}, secs=3.0)
        rate = model.expo_smooth(model.ctl(speed), 3, 1000) / 60
        T = t + (0 if reset else on / fs)
        ph = (T * rate) % 1
        prof = []
        for i in range(20):
            sel = (ph >= i / 20) & (ph < (i + 1) / 20) & (t > 0.02)
            prof.append(float(np.median(o[sel])) if sel.any() else None)
        late = o[t > 0.05]
        return dict(shape=shape, speed=speed, amount=m, pw=pw, phase=phase, reset=reset, model_rate_hz=rate,
                    model_depth_oct=4 * float(model.lin(model.ctl(abs(m)), 0, 1)) ** 2 if abs(float(model.ctl(abs(m))) - 64) > 1e-4 else 1.0,
                    min=float(late.min()), max=float(late.max()), profile=prof)
    items = [(0, 0.75, m, 0.5, 0, 0) for m in (0.1, 0.25, 0.5, 0.75)] + [(0, v, 0.25, 0.5, 0, 0) for v in (0.6, 0.9, 1)]
    items += [(s, 0.75, 0.25, 0.5, 0, 0) for s in (1, 2, 3, 4)] + [(1, 0.75, 0.25, 0.25, 0, 0), (2, 0.75, 0.25, 0.25, 0, 0), (2, 0.75, 0.25, 0.9, 0, 0)]
    items += [(0, 0.75, 0.25, 0.5, 0, 1), (0, 0.75, 0.25, 0.5, 0.25, 1), (0, 0.75, 0.25, 0.5, 0.5, 1), (0, 0.75, 0.25, 0.5, 0.5, 0)]
    rows = an.pmap(run, items)
    save('lfo', dict(rows=rows))
    for r in rows:
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != 'profile'}, np.round([p if p is not None else np.nan for p in r['profile']], 3)[::2])


def area_peg():
    fs = 44100
    def run(it):
        amt, tm = it
        t, o = pitch_track({C1 + 'OscillatorEnvAmount': amt, C1 + 'OscillatorEnvTime': tm})
        T = model.env_time(tm, 0.01, 10)
        A = model.env_time(abs(amt), 0.01, 6) * np.sign(amt)
        pts = {}
        for f in (0.05, 0.25, 0.5, 0.75, 0.95, 1.2):
            sel = np.abs(t - f * T) < 0.001
            pts[str(f)] = float(np.median(o[sel])) if sel.any() else None
        return dict(amount=amt, time=tm, model_time_s=T, model_amount_oct=A, offset_at_fraction_of_time=pts,
                    model_linear={str(f): A * max(0.0, 1 - f) for f in (0.05, 0.25, 0.5, 0.75, 0.95, 1.2)})
    rows = an.pmap(run, [(0.5, 0.5), (-0.5, 0.5), (0.25, 0.5), (0.5, 0.25), (0.5, 0.75), (0.6, 0.6)])
    save('peg', dict(rows=rows))
    for r in rows:
        print(r['amount'], r['time'], r['model_amount_oct'], {k: round(v, 4) if v is not None else None for k, v in r['offset_at_fraction_of_time'].items()})


def area_vibrato():
    def run(it):
        va, vs, vd, vf = it
        t, o = pitch_track({'VibratoToggle': 1, 'VibratoAmount': va, 'VibratoSpeed': vs, 'VibratoDelay': vd, 'VibratoFadeIn': vf}, secs=4.0)
        late = o[t > 2.0]
        s = late - np.median(late)
        tt = t[t > 2.0]
        zc = np.nonzero((s[:-1] < 0) & (s[1:] >= 0))[0]
        env = [float(np.max(np.abs(o[(t > a) & (t < a + 0.25)]))) for a in np.arange(0, 2.0, 0.25)]
        return dict(amount=va, speed=vs, delay=vd, fade=vf, depth_oct=float((late.max() - late.min()) / 2),
                    rate_hz=float((len(zc) - 1) / (tt[zc[-1]] - tt[zc[0]])) if len(zc) > 2 else None,
                    model_depth_oct=float(model.expo(model.ctl(va), 0.0002, 1 / 6)), model_rate_hz=float(model.lin(model.ctl(vs), 0.25, 10)),
                    peak_per_quarter_second=env)
    rows = an.pmap(run, [(0.5, 0.5, 0, 0), (1, 0.5, 0, 0), (0.25, 0.5, 0, 0), (0.75, 1, 0, 0), (0.75, 0.25, 0, 0), (0.75, 0.5, 0.5, 0), (0.75, 0.5, 0, 0.5), (0.75, 0.5, 0.5, 0.5)])
    save('vibrato', dict(rows=rows))
    for r in rows:
        print({k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items() if k != 'peak_per_quarter_second'}, np.round(r['peak_per_quarter_second'], 4))


def area_subsync():
    fs, on = 44100, 4400
    def run(it):
        mode, amt, shape = it
        y, _ = an.render(probe(**{C1 + 'OscillatorWaveShape': shape, C1 + 'OscillatorMode': mode, C1 + 'OscillatorSubAmount': amt}),
                         an.note(60, 100, on, on + fs), frames=on + fs)
        x = y[on + 4410:, 0].astype(float)
        f = model.osc_freq(60, fs)
        a, ph, res, dc = an.harmonics(x, fs, f / 2, 60)
        return dict(mode=mode, amount=amt, shape=shape, half_harmonics=a.tolist(), residual=res, dc=dc,
                    model_sub_level=float(model.expo(model.ctl(amt), 0.01, 1.0)) if amt > 0 else 0.0,
                    model_sync_ratio=float(model.expo(model.ctl(amt), 1, 20)))
    rows = an.pmap(run, [(m, a, s) for m in (0, 1) for a in (0, 0.25, 0.5, 0.75, 1) for s in (0, 1, 2)])
    save('subsync', dict(rows=rows))
    for r in rows:
        a = np.array(r['half_harmonics'])
        print(r['mode'], r['amount'], r['shape'], 'sub (f/2) %.4f' % a[0], 'odd sub h3 %.4f' % a[2], 'main h1 %.4f' % a[1],
              'strongest k/2: %d' % (int(np.argmax(a)) + 1), 'model sub %.4f sync %.3f' % (r['model_sub_level'], r['model_sync_ratio']))


# ---- timing, determinism, libm sensitivity --------------------------------------------------------

def grid_rule(f, block, period):
    """First output frame an event at frame f can change (t12-device-dsp-v1 run_analog.grid_rule)."""
    g = period * (f // period)
    return (g if g >= block * (f // block) else g + period) + 1


def area_timing():
    st = probe()
    rows = []
    def on_run(it):
        fs, block, f = it
        y, _ = an.render(st, [(f, 0x90, 60, 100)], fs=fs, frames=4096, block=block)
        return dict(kind='on', fs=fs, block=block, event=f, first_nonzero=an.first_above(y, 0), expected=grid_rule(f, block, fs // 1000))
    items = [(fs, b, f) for fs in (44100, 48000) for b in (512, 64, 333) for f in range(1000, 1200, 7)]
    rows += an.pmap(on_run, items)
    held = {fs: an.render(st, [(1024, 0x90, 60, 100)], fs=fs, frames=8192)[0] for fs in (44100, 48000)}
    def off_run(it):
        fs, f = it
        y, _ = an.render(st, [(1024, 0x90, 60, 100), (f, 0x80, 60, 64)], fs=fs, frames=8192)
        d = np.nonzero(np.abs(y.astype(float) - held[fs].astype(float)).max(1) > 0)[0]
        return dict(kind='off', fs=fs, block=512, event=f, first_diff=int(d[0]) if len(d) else None, expected=grid_rule(f, 512, fs // 1000))
    rows += an.pmap(off_run, [(fs, f) for fs in (44100, 48000) for f in range(4000, 4200, 9)])
    ok = all((r.get('first_nonzero', r.get('first_diff')) == r['expected']) for r in rows)
    save('timing', dict(rows=rows, n=len(rows), rule_holds=ok))
    print('timing rule holds for', len(rows), ok)


def area_determinism():
    """Re-run, host block sizes, MXCSR flush-to-zero/denormals-are-zero, the clock seed, and 48 kHz, on the
    Defaults-preset set with a three-note chord (oscillators, filters with drive, envelopes)."""
    st = an.stored('preset')
    ev = an.note(48, 100, 4400, 30000) + an.note(55, 90, 8800, 30000) + an.note(64, 110, 13200, 30000)
    base, _ = an.render(st, ev, frames=65536)
    rows = []
    for name, kw, env, extra in [('rerun', {}, None, ()), ('block64', dict(block=64), None, ()), ('block256', dict(block=256), None, ()),
                                 ('block333', dict(block=333), None, ()), ('block2048', dict(block=2048), None, ()),
                                 ('ftz_daz', {}, None, ('mxcsr 0x9fc0',)), ('seed', {}, {'XDEV_TIME': '1760000000'}, ())]:
        y, _ = an.render(st, ev, frames=65536, env=env, extra=extra, **kw)
        d = np.abs(y.astype(float) - base.astype(float))
        rows.append(dict(variant=name, bit_identical=bool(np.array_equal(y.view(np.uint32), base.view(np.uint32))),
                         max_abs_diff=float(d.max()), first_diff_frame=int(np.argmax(d.max(1) > 0)) if d.max() > 0 else None))
    save('determinism', dict(rows=rows))
    for r in rows:
        print(r)


def area_libm():
    """Every inexact libm result moved one ulp up, then down (harness XDEV_LIBM_ULP), on three sets."""
    sets = {'preset_chord': (an.stored('preset'), an.note(48, 100, 4400, 30000) + an.note(64, 110, 13200, 30000)),
            'probe_saw_c4': (probe(**{C1 + 'OscillatorWaveShape': 1}), an.note(60, 100, 4400, 48500)),
            'lp24_res_noise': (probe(**{**FNOISE, C1 + 'FilterToggle': 1, C1 + 'FilterType': 1, C1 + 'FilterQFactor': 0.8, C1 + 'FilterCutoffFrequency': 0.5}),
                               an.note(60, 100, 4400, 48500))}
    rows = []
    for name, (st, ev) in sets.items():
        base, _ = an.render(st, ev, frames=65536)
        for u in ('+1', '-1'):
            y, log = an.render(st, ev, frames=65536, env={'XDEV_LIBM_ULP': u})
            d = y.astype(float) - base.astype(float)
            x = base.astype(float)
            f0 = None
            if name == 'probe_saw_c4':
                f0 = [an.fund(z[8800:48000, 0], 44100) for z in (base, y)]
            rows.append(dict(set=name, ulp=u, max_abs_diff=float(np.abs(d).max()), rel_rms=float(np.sqrt((d ** 2).mean() / (x ** 2).mean())),
                             f0_rel_change=(f0[1] / f0[0] - 1) if f0 else None))
    save('libm', dict(rows=rows))
    for r in rows:
        print(r)


# ---- protocol details: warm-up, channel, velocity 0, release velocity, parameter changes -----------

def area_protocol():
    fs = 44100
    st = an.stored('preset')
    out = {}
    ev = an.note(60, 100, 4400, 26450)
    base, _ = an.render(st, ev, frames=44100)
    W = 11264                                    # 256 control periods, 22 blocks of 512
    warm, _ = an.render(st, [(f + W, s, a, b) for f, s, a, b in ev], frames=44100 + W)
    out['warmup_11264_bit_identical'] = bool(np.array_equal(warm[W:].view(np.uint32), base.view(np.uint32)))
    out['warmup_output_all_zero'] = bool(np.all(warm[:W] == 0))
    ch2, _ = an.render(st, [(4400, 0x91, 60, 100), (26450, 0x81, 60, 64)], frames=44100)
    out['channel_2_bit_identical'] = bool(np.array_equal(ch2, base))
    v0, _ = an.render(st, [(4400, 0x90, 60, 100), (26450, 0x90, 60, 0)], frames=44100)
    out['note_on_velocity_0_is_note_off'] = bool(np.array_equal(v0, base))
    r127, _ = an.render(st, [(4400, 0x90, 60, 100), (26450, 0x80, 60, 127)], frames=44100)
    out['release_velocity_127_bit_identical'] = bool(np.array_equal(r127, base))
    stray, _ = an.render(st, ev + [(15000, 0x80, 62, 64)], frames=44100)
    out['note_off_unsounding_key_no_change'] = bool(np.array_equal(stray, base))
    flag = [l for l in an.render(st, ev, frames=44100)[1].splitlines() if l.startswith('process')]
    out['activity_flag_runs'] = flag[0]
    # parameter changes between blocks while a note sounds: process 13,312 frames, set the value, process the rest
    pr = probe(**{C1 + 'OscillatorWaveShape': 1, C1 + 'FilterToggle': 1, C1 + 'FilterCutoffFrequency': 0.5})
    hv = an.host(pr)
    rows = []
    for name, idx, val in (('cutoff', 52, 0.6), ('osc level', 45, 0.6), ('amp level', 68, 0.6), ('volume', 2, 0.5), ('pan', 71, 0.0),
                           ('osc semi', 31, 19.0), ('detune', 34, 0.6), ('attack time (held note)', 105, 0.9)):
        lines0 = an.script(hv, [(4400, 0x90, 60, 100)], fs, 26624, 512)
        lines = lines0[:-3] + ['process 13312 512', f'param {idx} {val!r}', 'process 13312 512', 'destroy']
        lines0 = lines0[:-3] + ['process 13312 512', 'process 13312 512', 'destroy']
        y1, _ = xr(lines)
        y0, _ = xr(lines0)
        d = np.nonzero(np.abs(y1.astype(float) - y0.astype(float)).max(1) > 0)[0]
        rows.append(dict(parameter=name, index=idx, value=val, change_frame=13312, first_changed_frame=int(d[0]) if len(d) else None))
    out['parameter_changes'] = rows
    save('protocol', out)
    print(json.dumps(out, indent=1))


def xr(lines):
    import tempfile
    an.SCRATCH.mkdir(parents=True, exist_ok=True)
    fd, p = tempfile.mkstemp(suffix='.f32', dir=an.SCRATCH)
    import os
    os.close(fd)
    y, log = an.xdevpy.render('Analog', lines, p)
    Path(p).unlink()
    Path(p).with_suffix('.script').unlink()
    return y, log


# ---- LFO destinations, voice stealing, mono key change and glide (the last two left open) ---------

def area_lfodest():
    """Square LFO 1 (speed 0.6, 1.66 Hz) on amplitude, pan, cutoff and pulse width: the two states of
    each half cycle, measured away from the edges."""
    fs, on = 44100, 4400
    rate = model.expo_smooth(model.ctl(0.6), 3, 1000) / 60
    def run(it):
        dest, m = it
        ch = {C1 + 'LFOToggle': 1, C1 + 'LFOWaveShape': 2, C1 + 'LFOSpeed': 0.6, **EPROBE}
        ch[C1 + {'amp': 'AmplifierLFOAmpMod', 'pan': 'AmplifierLFOPanMod', 'cut': 'FilterLFOCutoffMod', 'pw': 'OscillatorLFOModPW'}[dest]] = m
        if dest == 'cut':
            ch.update({**FNOISE, C1 + 'FilterToggle': 1, C1 + 'FilterCutoffFrequency': 0.4, C1 + 'FilterQFactor': 0.3})
        if dest == 'pw':
            ch[C1 + 'OscillatorPulseWidth'] = 0.5
        y, _ = an.render(probe(**ch), an.note(60, 100, on, on + fs * 2), frames=on + fs * 2)
        T = np.arange(len(y)) / fs
        ph = (T * rate) % 1
        sel = {'hi': (ph > 0.05) & (ph < 0.45) & (T > 0.15), 'lo': (ph > 0.55) & (ph < 0.95) & (T > 0.15)}
        out = dict(dest=dest, amount=m)
        for nm, k in sel.items():
            idx = np.nonzero(k)[0]
            first = idx[:np.argmax(np.diff(idx) > 1)] if np.any(np.diff(idx) > 1) else idx
            if dest in ('amp', 'pan'):
                out[nm] = [float(np.sqrt((y[k, c].astype(float) ** 2).mean())) for c in (0, 1)]
            elif dest == 'cut':
                y0, _ = an.render(probe(**{**EPROBE, **FNOISE}), an.note(60, 100, on, on + fs * 2), frames=on + fs * 2)
                b, a, rel = arx(y0[:, 0].astype(float), y[:, 0].astype(float), 3, 2, n0=int(first[0]) + 200, N=min(8000, len(first) - 210))
                out[nm] = dict(fc_hz=biquad_params(a, fs)[0], rel=rel)
            else:
                x = y[first[:8000], 0].astype(float)
                a, phs, res, dc = an.harmonics(x, fs, model.osc_freq(60, fs), 20)
                out[nm] = duty_fit(a)[0]
        return out
    rows = an.pmap(run, [('amp', m) for m in (0.25, 0.5, 1)] + [('pan', m) for m in (0.25, 0.5, 1)] + [('cut', m) for m in (0.25, 0.5)] +
                   [('pw', m) for m in (0.25, 0.5, 1)])
    save('lfodest', dict(rows=rows, base_cutoff_hz=model.expo_smooth(model.ctl(0.4), 30, 22000)))
    for r in rows:
        print(r)


def area_steal():
    """Two voices (Polyphony 1); a third note at frame 22,000 steals the oldest (key 48). The key-48
    tone's amplitude (demodulated, 40 Hz low-pass) with the steal, relative to the same render
    without the third note."""
    fs = 44100
    ev = [(4400, 0x90, 48, 100), (8800, 0x90, 72, 100), (22000, 0x90, 96, 100)]
    rows = []
    for rel in (0.6000000238, 0.2):
        st = probe(Polyphony=1, **{AE + 'ReleaseTime': rel})
        y, _ = an.render(st, ev, frames=44100)
        y1, _ = an.render(st, ev[:2], frames=44100)
        f = model.osc_freq(48, fs)
        e3, e2 = an.envelope(y[:, 0], fs, f, 40), an.envelope(y1[:, 0], fs, f, 40)
        rows.append(dict(release=rel, first_changed_frame=int(np.argmax(np.abs(y[:, 0] - y1[:, 0]) > 0)),
                         key48_ratio={str(k): float(e3[k] / e2[k]) for k in (21500, 22100, 22300, 22500, 23000, 23500, 24000, 26000)}))
    save('steal', dict(events=ev, rows=rows))
    for r in rows:
        print(r)


def area_glide():
    """Mono legato key changes with glide (left open in the spec): pitch fraction of the interval from
    zero crossings, and the output peak around the change."""
    fs = 44100
    def run(it):
        pt, mode, iv = it
        ev = [(4400, 0x90, 84, 100), (26400, 0x90, 84 + iv, 100)]
        st = probe(Polyphony=0, PortamentoToggle=1, PortamentoTime=pt, PortamentoMode=mode)
        y, _ = an.render(st, ev, frames=fs * 2)
        t, f = an.zc_freq(y[:, 0], fs)
        f0, f1 = model.osc_freq(84, fs), model.osc_freq(84 + iv, fs)
        o = np.log2(f / f0) / np.log2(f1 / f0)
        tt = t * fs - 26400
        frac = {}
        for T in (22, 66, 110, 220, 441, 882, 1433, 2205, 4410, 7950, 15000, 30000):
            sel = np.abs(tt - T) < 25
            frac[str(T)] = float(np.median(o[sel])) if sel.any() else None
        return dict(time=pt, mode=mode, interval=iv, fraction_after_frames=frac,
                    peak_per_50_frames_from_26300=np.abs(y[26300:26800, 0]).reshape(-1, 50).max(1).tolist())
    rows = an.pmap(run, [(pt, 0, 12) for pt in (0.5, 0.75, 1)] + [(0.75, 1, iv) for iv in (6, 12, 24)])
    save('glide', dict(rows=rows))
    for r in rows:
        print(r['time'], r['mode'], r['interval'], {k: (round(v, 3) if v is not None else None) for k, v in r['fraction_after_frames'].items()})


AREAS = {k[5:]: v for k, v in dict(globals()).items() if k.startswith('area_')}

if __name__ == '__main__':
    for a in sys.argv[1:] or AREAS:
        AREAS[a]()
