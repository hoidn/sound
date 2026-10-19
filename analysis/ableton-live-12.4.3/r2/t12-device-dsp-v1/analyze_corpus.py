"""Compare the Corpus renders (run_corpus.py) with the static model (model.py) and with the port.

    python3 -I analyze_corpus.py     # writes results/corpus_model.json, results/corpus_port.json

Per mode, fit.track measures frequency, decay and complex amplitude in the render and, with the
same filter, in the model's own output for the same input; render minus model is reported. Each
frequency and decay difference is set against the change that one binary32 ulp in the mode's
filter coefficients a1 and a2 would cause (the engine computes and stores them in binary32; the
model rounds float64 values). Time-domain checks run the model's filters in float64. Port renders
come from port_render.js (node). Model: binary32-rounded coefficients (CorpusModel coef32=True).
"""
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402
from scipy.signal import lfilter  # noqa: E402

import fit  # noqa: E402
import model  # noqa: E402

RUNS = json.loads((HERE / 'results' / 'corpus_runs.json').read_text())
N0, FRAMES = RUNS['impulse_at'], RUNS['frames']
CH = {'L': 0, 'R': 1}
MODAL = ('defaults_', 'mode_', 'pitch_', 'detune', 'decay_', 'tone_', 'hit_', 'listen', 'width', 'inharm_', 'bright_', 'ratio_', 'bleed_')


def load(name, d=HERE / 'raw' / 'corpus'):
    return np.fromfile(d / f'{name}.f32', np.float32).reshape(-1, 2).astype(float)


def mdl(name):
    c = RUNS['runs'][name]['case']
    return model.CorpusModel({int(k): v for k, v in c['params'].items()}, c['fs'], coef32=True)


def impulse():
    x = np.zeros(FRAMES)
    x[N0] = 1.0
    return x


def model_output(m, x):
    """Model output (frames x 2) for a stereo input whose channels are equal (x is mono)."""
    res = {}
    for ch in ('L', 'R'):
        modes, bl = m.coefs(ch)
        h = np.zeros_like(x)
        for c in modes:
            b = 3000 * c['g'] * c['exc'] * c['pick']
            h += lfilter([b, 0, -b], [1, c['a1'], c['a2']], x)
        if bl:
            h += lfilter(3000 * bl['b0'] * m.amp_hp * np.array([1, -2, 1]), [1, bl['a1'], bl['a2']], x)
        res[ch] = h
    A, B = m.width
    return np.stack([m.drive * m.wet * (A * res['L'] + B * res['R']) + m.dry * x,
                     m.drive * m.wet * (A * res['R'] + B * res['L']) + m.dry * x], 1)


def err(y, ref):
    d = y - ref
    return dict(rel_rms=float(np.sqrt((d ** 2).mean() / (ref ** 2).mean())), max_abs=float(np.abs(d).max()),
                peak=float(np.abs(ref).max()))


def ulp32(x):
    return float(np.spacing(np.float32(abs(x))))


def bounds(c):
    """Relative change of the pole angle for one binary32 ulp in a1 and one in a2, plus two ulps
    of the angle itself (2^-23, the rounding of w and w/fs); and relative change of the per-sample
    log radius for one ulp in a2."""
    a1, a2 = c['a1'], c['a2']
    th = math.acos(-a1 / (2 * math.sqrt(a2)))
    dth = ulp32(a1) / (2 * math.sqrt(a2) * math.sin(th)) + abs(math.cos(th)) * ulp32(a2) / (2 * a2 * math.sin(th))
    return dth / th + 2 ** -23, ulp32(a2) / (1 - a2)


def mode_rows(name, ch, thr=1e-3):
    m = mdl(name)
    pred = m.poles(ch)
    wmax = max(abs(p['g'] * p['exc'] * p['pick']) for p in pred)
    sig = [p for p in pred if abs(p['g'] * p['exc'] * p['pick']) >= thr * wmax]
    y, ym = load(name)[:, CH[ch]], model_output(m, impulse())[:, CH[ch]]
    rows = []
    for p in sig:
        gap = min([abs(p['pole_hz'] - q['pole_hz']) for q in sig if q is not p] or [200])
        row = dict(k=p['k'], ratio=p['r'], nominal_hz=p['nominal_hz'], pole_hz=p['pole_hz'],
                   weight=abs(p['g'] * p['exc'] * p['pick']) / wmax, gap_hz=gap)
        cutoff = min(100, 0.4 * gap)
        taps = int(3.3 * m.fs / cutoff) | 1
        if -math.log(p['radius']) * (taps + 2000) > 12:     # below -104 dB before the estimator has data
            rows.append({**row, 'resolved': False, 'why': 'decays before the estimator settles'})
            continue
        try:
            tr, tm = (fit.track(s, p['pole_hz'], m.fs, N0, cutoff) for s in (y, ym))
        except ValueError:
            rows.append({**row, 'resolved': False, 'why': 'window shorter than the filter'})
            continue
        fb, rb = bounds(p)
        ratio = tr['amp'] / tm['amp']
        rows.append({**row, 'resolved': True, 'render_hz': tr['hz'], 'model_est_hz': tm['hz'],
                     'rel_freq_err': (tr['hz'] - tm['hz']) / p['pole_hz'], 'freq_ulp_bound': fb,
                     'estimator_bias': tm['hz'] / p['pole_hz'] - 1, 'pred_log_radius': math.log(p['radius']),
                     'render_log_radius': tr['log_radius'], 'decay_rate_rel_err': tr['log_radius'] / tm['log_radius'] - 1,
                     'decay_ulp_bound': rb, 'amp_ratio': [ratio.real, ratio.imag], 'amp_err': abs(ratio - 1)})
    return m, rows


def summary(rows):
    """Errors over the clean modes: resolved, and the estimator recovers the model's own pole frequency
    to 1e-4 (closely spaced 2-D modes and heavily damped modes are not clean)."""
    r = [x for x in rows if x['resolved']]
    c = [x for x in r if abs(x['estimator_bias']) < 1e-4]
    return dict(significant=len(rows), resolved=len(r), clean=len(c),
                max_abs_rel_freq_err=max(abs(x['rel_freq_err']) for x in c),
                max_freq_err_in_ulp_bounds=max(abs(x['rel_freq_err']) / x['freq_ulp_bound'] for x in c),
                max_abs_decay_rate_rel_err=max(abs(x['decay_rate_rel_err']) for x in c),
                max_decay_err_in_ulp_bounds=max(abs(x['decay_rate_rel_err']) / x['decay_ulp_bound'] for x in c),
                max_amp_err=max(x['amp_err'] for x in c), max_abs_estimator_bias=max(abs(x['estimator_bias']) for x in r))


def modes_section():
    out = {}
    for name in [n for n in RUNS['runs'] if n.startswith(MODAL)]:
        out[name] = {}
        for ch in ('L', 'R'):
            m, rows = mode_rows(name, ch)
            out[name][ch] = dict(type=m.itype, N=m.N, active=len(m.poles(ch)), fs=m.fs, **summary(rows), modes=rows)
            if name.startswith(('pitch_', 'detune', 'mode_string')):
                f0 = next(x for x in rows if x['k'] == 0)
                p = m.pitch[ch]
                out[name][ch]['f0'] = dict(pitch_oct=p, render_hz=f0['render_hz'], model_pole_hz=f0['pole_hz'],
                                           with_engine_pow2_hz=261.62 * model.pow2(p), with_exact_2p_hz=261.62 * 2 ** p)
    return out


def null_section():
    """hit_0 (strike at the centre): even harmonics of the String are predicted absent. Levels at
    harmonics 1-8 from a Blackman-Harris spectrum of 8192 samples after the impulse, render and model."""
    from scipy.signal.windows import blackmanharris
    m = mdl('hit_0')
    pred = {p['k']: p for p in m.poles('L')}
    out = dict(strike_position=m.exci, predicted_exc={k + 1: pred[k]['exc'] for k in range(8)})
    for label, s in (('render', load('hit_0')[:, 0]), ('model', model_output(m, impulse())[:, 0])):
        seg = s[N0:N0 + 8192] * blackmanharris(8192)
        spec, hz = np.abs(np.fft.rfft(seg, 1 << 16)), np.fft.rfftfreq(1 << 16, 1 / m.fs)
        lvl = [spec[np.abs(hz - pred[k]['pole_hz']) <= 3].max() for k in range(8)]
        out[label + '_db_re_fundamental'] = {k + 1: 20 * math.log10(v / lvl[0]) for k, v in enumerate(lvl)}
    return out


def lfo_section():
    """lfo_sine: the String's fundamental follows the LFO. Instantaneous frequency (averaged over 200
    samples) of render and port, against 261.62 * 2^(amount * S(phase)) with the engine's sine
    polynomial S, rate and amount from the drivers, phase 0 at the first processed sample and the
    right channel half a cycle later (Phase mode, LfoPhase 180)."""
    from scipy.signal import firwin
    c = RUNS['runs']['lfo_sine']['case']['params']
    rate = model.expo(model.D(c['20']), 0.01, 10)
    amount = model.lin(model.D(c['26']), 0, 1)
    rel = model.lin(model.f32(0.35 * c['24'] + 1) if c['24'] >= 180 else c['24'] * 127 / 360, 0, 1)
    S = lambda p: 6.094263 * p + 6.094263 * p ** 2 - 85.31969 * p ** 3 + 121.88526 * p ** 4 - 48.754105 * p ** 5  # noqa: E731
    h = firwin(801, 80, fs=44100)
    n = np.arange(FRAMES)
    out = dict(rate_hz=rate, amount_oct=amount, right_phase_offset=rel, at={})
    sigs = dict(render=load('lfo_sine'), port=load('lfo_sine', Path('/var/tmp/sound-analysis/t12-xdev/port')))
    for t in range(N0 + 1200, FRAMES - 600, 1000):
        row = {}
        for ch, off in (('L', 0.0), ('R', rel)):
            ph = (rate * t / 44100 + off) % 1
            ticks = 200 * np.floor(np.arange(t - 100, t + 101) / 200)       # pitch read every 200 samples
            row[ch] = dict(predicted_continuous=261.62 * model.pow2(amount * S(ph)),
                           predicted=float(np.mean([261.62 * model.pow2(amount * S((rate * k / 44100 + off) % 1)) for k in ticks])))
            for lab, y in sigs.items():
                z = lfilter(h, 1, y[:, CH[ch]] * np.exp(-2j * np.pi * 261.62 * n / 44100))
                k = t + 400                                        # filter delay 400 samples
                inst = np.diff(np.unwrap(np.angle(z[k - 100:k + 101]))).mean() * 44100 / (2 * np.pi) + 261.62
                row[ch][lab] = float(inst)
        out['at'][t] = row
    out['max_abs_render_minus_continuous_hz'] = max(abs(r[ch]['render'] - r[ch]['predicted_continuous']) for r in out['at'].values() for ch in r)
    out['max_abs_render_minus_predicted_hz'] = max(abs(r[ch]['render'] - r[ch]['predicted']) for r in out['at'].values() for ch in r)
    out['max_abs_render_minus_port_hz'] = max(abs(r[ch]['render'] - r[ch]['port']) for r in out['at'].values() for ch in r)
    return out


def ir_section():
    out = {}
    for name in [n for n in RUNS['runs'] if n.startswith(MODAL)]:
        y, ym = load(name), model_output(mdl(name), impulse())
        out[name] = {ch: dict(first_256=err(y[N0:N0 + 256, i], ym[N0:N0 + 256, i]), first_8192=err(y[N0:N0 + 8192, i], ym[N0:N0 + 8192, i]))
                     for ch, i in CH.items()}
    y, yd = load('left_only'), load('defaults_44')
    out['left_only'] = dict(right_max_abs=float(np.abs(y[:, 1]).max()), left_bit_identical_to_defaults=bool(np.array_equal(y[:, 0], yd[:, 0])))
    for g in ('listenL', 'listenR'):
        other = 1 if g == 'listenL' else 0
        ys = [load(n)[:, other] for n in RUNS['runs'] if n.startswith(g + '_')]
        out[f'{g}_other_channel_max_abs_diff'] = max(float(np.abs(v - ys[0]).max()) for v in ys[1:])
    return out


def sine_section():
    out = {}
    for name in [n for n in RUNS['runs'] if n.startswith(('sine_', 'drive_', 'drywet_'))]:
        c = RUNS['runs'][name]['case']
        f = 261.62 if c['input'].startswith('sine261') else float(c['input'].split('_')[0][4:])
        m, y = mdl(name), load(name)
        n = np.arange(FRAMES)[-8192:]
        X = np.stack([np.sin(2 * np.pi * f * n / m.fs), np.cos(2 * np.pi * f * n / m.fs)], 1)
        row = {}
        for ch, i in CH.items():
            s, co = np.linalg.lstsq(X, y[-8192:, i], rcond=None)[0]
            H, Hm = complex(s, co) / 0.25, complex(m.response([f], ch)[0])
            res = y[-8192:, i] - X @ np.array([s, co])
            row[ch] = dict(freq=f, measured=[H.real, H.imag], model=[Hm.real, Hm.imag], mag_db_err=20 * math.log10(abs(H) / abs(Hm)),
                           phase_err_deg=math.degrees(np.angle(H / Hm)), fit_rel_residual=float(np.sqrt((res ** 2).mean() / (y[-8192:, i] ** 2).mean())))
        out[name] = row
    return out


def third_octave(y, ref, fs):
    w = np.hanning(len(y))
    Y, R = np.fft.rfft(y * w), np.fft.rfft(ref * w)
    hz = np.fft.rfftfreq(len(y), 1 / fs)
    out = []
    for e in 1000 * 2.0 ** (np.arange(-14, 13) / 3):
        k = (hz >= e) & (hz < e * 2 ** (1 / 3))
        if k.sum() >= 4:
            out.append(dict(lo=float(e), db_diff=10 * math.log10((np.abs(Y[k]) ** 2).sum() / (np.abs(R[k]) ** 2).sum())))
    return out


def noise_section():
    x = np.fromfile(HERE / 'inputs' / 'noise44.f32', np.float32).reshape(-1, 2)[:, 0].astype(float)
    m, y = mdl('noise_44'), load('noise_44')
    ym = model_output(m, x)
    bands = third_octave(y[8192:, 0], ym[8192:, 0], 44100)
    return dict(time_domain_from_8192={ch: err(y[8192:, i], ym[8192:, i]) for ch, i in CH.items()},
                third_octave_max_abs_db=max(abs(b['db_diff']) for b in bands), third_octave_bands=bands)


def f0_track(y, fs, lo=100, hi=2000):
    """Strongest spectral peak in lo..hi Hz after the impulse, refined by fit.track (cutoff 10 Hz)."""
    seg = y[N0:]
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 18))
    hz = np.fft.rfftfreq(1 << 18, 1 / fs)
    k = (hz >= lo) & (hz <= hi)
    return fit.track(y, float(hz[k][np.argmax(spec[k])]), fs, N0, 10)['hz']


def port_section():
    tmp = Path('/var/tmp/sound-analysis/t12-xdev/port')
    tmp.mkdir(parents=True, exist_ok=True)
    cases = [dict(name=n, fs=r['case']['fs'], block=r['case']['block'], frames=FRAMES,
                  input=str(HERE / 'inputs' / f"{r['case']['input']}.f32"), params=r['case']['params'])
             for n, r in RUNS['runs'].items()]
    (tmp / 'cases.json').write_text(json.dumps(cases))
    subprocess.run(['node', str(HERE / 'port_render.js'), str(tmp / 'cases.json'), str(tmp)], check=True)
    out = {}
    for n, r in RUNS['runs'].items():
        y, yp = load(n), load(n, tmp)
        impulse_case = r['case']['input'].startswith('impulse')
        e = dict(port_sha256=hashlib.sha256((tmp / f'{n}.f32').read_bytes()).hexdigest())
        for label, a in (('from_impulse', N0) if impulse_case else ('from_0', 0), ('from_8192', 8192)):
            e[label] = {ch: err(yp[a:, i], y[a:, i]) for ch, i in CH.items()}
        if r['case']['input'].startswith('noise'):
            e['third_octave_max_abs_db_from_8192'] = max(abs(b['db_diff']) for b in third_octave(yp[8192:, 0], y[8192:, 0], r['case']['fs']))
        if n.startswith('wg_'):
            fs = r['case']['fs']
            f0 = f0_track(y[:, 0], fs)
            e['f0_hz'] = dict(render=f0, port=f0_track(yp[:, 0], fs))
            lv = [abs(fit.track(y[:, 0], k * f0, fs, N0, 10)['amp']) for k in (1, 2, 3, 4)]
            e['harmonic_levels_db_re_f0'] = [20 * math.log10(v / lv[0]) for v in lv]
            e['channels_identical'] = bool(np.array_equal(y[:, 0], y[:, 1]))
        out[n] = e
    return out


def startup_section():
    """startup_dry: DryWet 0, constant input 0.5 from the first frame. Output / input = dry gain."""
    out = {}
    for label, d in (('render', HERE / 'raw' / 'corpus'), ('port', Path('/var/tmp/sound-analysis/t12-xdev/port'))):
        g = load('startup_dry', d)[:, 0] / 0.5
        on = np.nonzero(g > 1e-9)[0]
        final = float(g[-1])
        full = np.nonzero(np.abs(g - final) <= 1e-7 * final)[0]
        out[label] = dict(first_frame_with_gain=int(on[0]), first_frame_at_final=int(full[0]), final_gain=final,
                          gain_at={int(k): float(g[k]) for k in (0, 99, 100, 101, 150, 199, 200)})
    out['model_final_gain'] = model.P(0.25)
    return out


def main():
    res = dict(modes=modes_section(), even_mode_null=null_section(), impulse_response=ir_section(),
               sine=sine_section(), noise=noise_section())
    port = port_section()
    res['lfo'] = lfo_section()
    res['startup'] = startup_section()
    (HERE / 'results' / 'corpus_model.json').write_text(json.dumps(res, indent=1))
    (HERE / 'results' / 'corpus_port.json').write_text(json.dumps(port, indent=1))
    for k, v in res['modes'].items():
        s = v['L']
        print(f"{k:16s} sig {s['significant']:2d} res {s['resolved']:2d} f {s['max_abs_rel_freq_err']:.1e} ({s['max_freq_err_in_ulp_bounds']:.2f} ulp-b) "
              f"clean {s['clean']:2d} d {s['max_abs_decay_rate_rel_err']:.1e} ({s['max_decay_err_in_ulp_bounds']:.2f}) amp {s['max_amp_err']:.1e} bias {s['max_abs_estimator_bias']:.0e}")
    print('startup', res['startup'])
    print('null', {k: v for k, v in res['even_mode_null'].items() if k.endswith('fundamental')})
    print('lfo', {k: v for k, v in res['lfo'].items() if k != 'at'})
    print('ir', {k: '%.0e/%.0e' % (v['L']['first_256']['rel_rms'], v['L']['first_8192']['rel_rms']) for k, v in res['impulse_response'].items() if isinstance(v, dict) and 'L' in v})
    print('left_only', res['impulse_response']['left_only'])
    print('sine', {k: (round(v['L']['mag_db_err'], 5), round(v['L']['phase_err_deg'], 4)) for k, v in res['sine'].items()})
    print('noise', res['noise']['time_domain_from_8192']['L'], res['noise']['third_octave_max_abs_db'])
    for k, v in port.items():
        a = v.get('from_impulse', v.get('from_0'))
        print(f"port {k:16s} {a['L']['rel_rms']:.1e} steady {v['from_8192']['L']['rel_rms']:.1e}", v.get('f0_hz', ''), v.get('third_octave_max_abs_db_from_8192', ''))


if __name__ == '__main__':
    main()
