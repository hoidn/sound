"""Signal measurements used by the Tension analysis, checks and metric (no device code).

    modes(x, f0, start, end)       partials of a ringing string, by the fit.py demodulation estimator
    third_octave(x, a, b, fs)      band levels in dB, 50 Hz to 16 kHz
    transfer(x_on, x_off, a, b)    complex ratio of two renders at the spectral peaks of x_off
    rel_rms(a, b)                  ||a - b|| / ||b||

modes(): partial k is predicted from the measured first partial f1 and a running inharmonicity fit
(f_k = k f1 sqrt((1 + B k^2) / (1 + B))), refined to the largest spectral peak within +-0.25 f1 of the
prediction, and measured with fit.track (cutoff min(150 Hz, 0.3 f1)) over [start, end). The window
ends early where the signal stays below 1e-4 of its peak (a voice that has ended). Partials more
than 60 dB below the strongest peak are skipped, as are estimates that land more than 0.1 f1 from
their peak. Dependencies: numpy, scipy, fit.py.
"""
import numpy as np

import fit


def onset(x, thr=0.0):
    k = np.nonzero(np.abs(x) > thr)[0]
    return int(k[0]) if len(k) else None


def last(x, thr=0.0):
    k = np.nonzero(np.abs(x) > thr)[0]
    return int(k[-1]) if len(k) else None


def rel_rms(a, b):
    d = float(np.sum(b ** 2))
    return float(np.sqrt(np.sum((a - b) ** 2) / d)) if d > 0 else (0.0 if not np.any(a) else float('inf'))


def spectrum(x, fs, n=1 << 20):
    sp = np.abs(np.fft.rfft(x * np.hanning(len(x)), n))
    return sp, np.fft.rfftfreq(n, 1 / fs)


def modes(x, f0, start, end, fs, K=16, floor_db=-60.0):
    peak = np.abs(x).max()
    if peak == 0:
        return dict(partials=[], B=None, window=None)
    loud = np.nonzero(np.abs(x[:end]) > 1e-4 * peak)[0]
    end = min(end, int(loud[-1]) + 1) if len(loud) else end
    start = max(0, min(start, end - 4096))
    sp, hz = spectrum(x[start:end], fs)
    out, B, f1, ref = [], 0.0, f0, None
    for k in range(1, K + 1):
        pred = k * f1 * np.sqrt((1 + B * k * k) / (1 + B))
        if pred > 0.45 * fs:
            break
        lo, hi = np.searchsorted(hz, [pred - 0.25 * f1, pred + 0.25 * f1])
        if hi <= lo:
            break
        j = lo + int(np.argmax(sp[lo:hi]))
        ref = sp[j] if ref is None else max(ref, sp[j])
        if 20 * np.log10(sp[j] / ref) < floor_db:
            continue
        try:
            t = fit.track(x[:end], hz[j], fs, start, min(150.0, 0.3 * f1))
        except ValueError:
            continue
        if abs(t['hz'] - hz[j]) > 0.1 * f1 or not np.isfinite(t['log_radius']):
            continue
        if not out and k == 1:
            f1 = t['hz']
        out.append(dict(k=k, hz=float(t['hz']), log_radius=float(t['log_radius']),
                        t60_s=float(-3 * np.log(10) / (t['log_radius'] * fs)) if t['log_radius'] < 0 else None,
                        amp=abs(t['amp']), phase=float(np.angle(t['amp']))))
        if len(out) >= 3:
            ks = np.array([m['k'] for m in out], float)
            r2 = (np.array([m['hz'] for m in out]) / (ks * f1)) ** 2
            B = float(np.sum((r2 - 1) * (ks ** 2 - 1)) / np.sum((ks ** 2 - 1) ** 2))
    top = max((m['amp'] for m in out), default=1.0)
    for m in out:
        m['ratio'] = m['hz'] / (m['k'] * f1)
        m['level_db'] = float(20 * np.log10(m['amp'] / top))
    return dict(partials=out, B=B, window=[int(start), int(end)])


BANDS = 1000 * 2.0 ** (np.arange(-13, 13) / 3)          # 50 Hz .. 16 kHz


def third_octave(x, a, b, fs):
    seg = x[a:b]
    p = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
    hz = np.fft.rfftfreq(len(seg), 1 / fs)
    return [float(10 * np.log10(p[(hz >= c * 2 ** (-1 / 6)) & (hz < c * 2 ** (1 / 6))].sum() + 1e-30)) for c in BANDS]


def transfer(x_on, x_off, a, b, fs, floor_db=-90.0, min_spacing_hz=30.0):
    """Complex ratio X_on / X_off at the spectral peaks of x_off over [a, b) (Hann window)."""
    from scipy.signal import find_peaks
    w = np.hanning(b - a)
    X0, X1 = np.fft.rfft(x_off[a:b] * w), np.fft.rfft(x_on[a:b] * w)
    hz = np.fft.rfftfreq(b - a, 1 / fs)
    P = 20 * np.log10(np.abs(X0) / np.abs(X0).max() + 1e-30)
    pk, _ = find_peaks(P, height=floor_db, distance=max(1, int(min_spacing_hz / (fs / (b - a)))))
    return hz[pk], X1[pk] / X0[pk]


def modal_compare(x, ref_x, ref_modes, fs, floor_db=-60.0):
    """Measure x and ref_x with the same estimator at the partials of ref_modes (the reference's modes()
    result): worst relative frequency difference, worst relative log-radius difference and worst complex
    amplitude difference relative to the strongest partial, over partials at or above floor_db."""
    if not ref_modes['partials']:
        return None
    a, b = ref_modes['window']
    f1 = ref_modes['partials'][0]['hz'] / ref_modes['partials'][0]['k']
    c = min(150.0, 0.3 * f1)
    top = max(m['amp'] for m in ref_modes['partials'])
    worst = dict(freq_rel=0.0, log_radius_rel=0.0, amp_rel=0.0, n=0)
    for m in ref_modes['partials']:
        if m['level_db'] < floor_db:
            continue
        tr, tx = (fit.track(s[:b], m['hz'], fs, a, c) for s in (ref_x, x))
        worst['freq_rel'] = max(worst['freq_rel'], abs(tx['hz'] / tr['hz'] - 1))
        worst['log_radius_rel'] = max(worst['log_radius_rel'], abs(tx['log_radius'] / tr['log_radius'] - 1))
        worst['amp_rel'] = max(worst['amp_rel'], abs(tx['amp'] - tr['amp']) / top)
        worst['n'] += 1
    return worst


def env_db(x, hop):
    return np.array([20 * np.log10(np.sqrt((x[k:k + hop] ** 2).mean()) + 1e-30) for k in range(0, len(x) - hop + 1, hop)])
