"""Measures of an Electric render and the SPEC-DEVICE-ELECTRIC comparison metric.

    m = measure(x, fs, case)                 # x: mono render after the warm-up
    d = element_deviations(m_ref, m_other, fs)
    masks, tol, summary = grade([d1, d2, ...], m_ref)   # graded elements and tolerances from variants
    fails = check(m_ref, m_cand, masks, tol, fs)

Measures (frame 0 = first frame after the warm-up):
  onset      first frame whose sample is not exactly 0; onset_1e6: first frame with |x| > 1e-6 * peak
  env        level in dB of consecutive 10 ms frames (fs/100 samples): 20 log10(RMS)
  bands      third-octave band levels (centres 1 kHz * 2^(k/3), 50 Hz..16 kHz) of 4096-frame Hann
             windows starting at the case's band_starts; power summed over the FFT bins of each band
  partials   single-note cases: harmonic k = 1..8 (below fs/2 - 200 Hz) by fit.track at k * f0 over
             [onset + 30 ms, note-off), cutoff min(20 Hz, f0/4): frequency, amplitude (dB) at the window
             start, decay (dB/s); f0 is the case's reference fundamental
  noise      level of the random component: 20 log10 RMS((x_a - x_b)/sqrt 2) / RMS(x_a) over
             [onset, note-off) for two renders that differ only in the noise seed
Grading: an element is graded when it is loud enough (env within 40 dB of the loudest frame; bands
within 30 dB of the window's strongest band; partials within 30 dB of the strongest harmonic) and no
variant render moves it by more than CAP. Tolerance per measure: twice the largest deviation of any
variant over the graded elements, at least FLOOR. Partial frequencies: within FREQ_TOL ulp bounds of
the fundamental (all harmonics move with the fundamental).
Dependencies: numpy, fit.py.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fit  # noqa: E402

FLOOR = dict(env=0.05, bands=0.1, amp=0.1, decay=0.1)
CAP = dict(env=1.5, bands=1.5, amp=1.5, decay=2.0)
FREQ_TOL = 4.0
NOISE_TOL_DB = 6.0


def onset(x, rel=0.0):
    k = np.nonzero(np.abs(x) > rel * np.abs(x).max())[0] if rel else np.nonzero(x)[0]
    return int(k[0]) if len(k) else None


def env_db(x, fs):
    hop = fs // 100
    n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-30)


def band_centres():
    return [1000 * 2 ** (k / 3) for k in range(-13, 13) if 50 <= 1000 * 2 ** (k / 3) <= 16000]


def bands_db(x, fs):
    sp = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    hz = np.fft.rfftfreq(len(x), 1 / fs)
    return np.array([10 * np.log10(sp[(hz >= c * 2 ** (-1 / 6)) & (hz < c * 2 ** (1 / 6))].sum() + 1e-30) for c in band_centres()])


def partials(x, fs, on, off, f0):
    start = on + int(0.03 * fs)
    out = []
    for k in range(1, 9):
        if k * f0 > fs / 2 - 200:
            break
        t = fit.track(x[:off], k * f0, fs, start, min(20.0, f0 / 4))
        out.append(dict(k=k, hz=float(t['hz']), amp_db=float(20 * np.log10(abs(t['amp']) + 1e-30)),
                        decay_db_s=float(t['log_radius'] * fs * 20 / np.log(10))))
    return out


def measure(x, fs, case):
    m = dict(onset=onset(x), onset_1e6=onset(x, 1e-6), peak=float(np.abs(x).max()), env=env_db(x, fs).tolist(),
             bands=[bands_db(x[s:s + 4096], fs).tolist() for s in case['band_starts']])
    if case.get('f0') and m['onset'] is not None:
        m['partials'] = partials(x, fs, m['onset'], case['off'], case['f0'])
    return m


def ulp_bound(hz, fs):
    """Relative frequency change from one binary32 ulp in each coefficient of a two-pole resonator at
    hz (the Corpus definition): 3 * 2^-25 / theta^2 + 2^-23, theta = 2 pi hz / fs."""
    th = 2 * np.pi * hz / fs
    return 3 * 2 ** -25 / th ** 2 + 2 ** -23


def element_deviations(ref, other, fs):
    d = dict(onset=other['onset'] == ref['onset'], env=np.abs(np.subtract(other['env'], ref['env'])),
             bands=np.abs(np.subtract(other['bands'], ref['bands'])))
    if 'partials' in ref:
        b = ulp_bound(ref['partials'][0]['hz'], fs)
        p, q = ref['partials'], other['partials']
        d['freq'] = np.array([abs(v['hz'] / u['hz'] - 1) / b for u, v in zip(p, q)])
        d['amp'] = np.array([abs(v['amp_db'] - u['amp_db']) for u, v in zip(p, q)])
        d['decay'] = np.array([abs(v['decay_db_s'] - u['decay_db_s']) for u, v in zip(p, q)])
    return d


def loud(ref):
    e = np.array(ref['env'])
    b = np.array(ref['bands'])
    out = dict(env=e > e.max() - 40, bands=b > b.max(1, keepdims=True) - 30)
    if 'partials' in ref:
        a = np.array([p['amp_db'] for p in ref['partials']])
        out['amp'] = out['decay'] = out['freq'] = a > a.max() - 30
    return out


def grade(devs, ref):
    """devs: element_deviations of each variant. Returns (graded masks, tolerances, summary)."""
    masks, tol, summary = {}, {}, {}
    for k, base in loud(ref).items():
        stack = np.array([d[k] for d in devs])
        if k == 'freq':
            masks[k] = base
            tol['freq_ulp_bounds'] = FREQ_TOL
            summary['freq_variants_max'] = float(stack[:, base].max()) if base.any() else 0.0
            continue
        g = base & (stack.max(0) <= CAP[k])
        masks[k] = g
        worst = float(stack[:, g].max()) if g.any() else 0.0
        tol[k] = max(FLOOR[k], 2 * worst)
        summary[f'{k}_graded'] = int(g.sum())
        summary[f'{k}_loud_not_graded'] = int((base & ~g).sum())
    return masks, tol, summary


def check(ref, cand, masks, tol, fs):
    """Names of the measures on which a candidate measure set fails the reference's tolerances."""
    d = element_deviations(ref, cand, fs)
    fails = [k for k in ('env', 'bands', 'amp', 'decay') if k in masks and np.any(d[k][masks[k]] > tol[k])]
    if 'freq' in masks and np.any(d['freq'][masks['freq']] > tol['freq_ulp_bounds']):
        fails.append('freq')
    return fails


def noise_level_db(xa, xb, on, off):
    r = (xa[on:off] - xb[on:off]) / np.sqrt(2)
    return float(20 * np.log10(np.sqrt((r ** 2).mean()) / np.sqrt((xa[on:off] ** 2).mean())))


if __name__ == '__main__':
    fs = 44100
    n = np.arange(fs)
    x = np.where(n >= 100, 0.3 * np.exp(-n / fs) * np.sin(2 * np.pi * 261.6 * n / fs), 0.0)
    case = dict(band_starts=[1000], f0=261.6, off=fs)
    m = measure(x, fs, case)
    assert m['onset'] == 100, m['onset']
    p = m['partials'][0]
    assert abs(p['hz'] - 261.6) < 1e-3 and abs(p['decay_db_s'] + 20 / np.log(10)) < 0.01, p
    masks, tol, _ = grade([element_deviations(m, m, fs)], m)
    assert check(m, m, masks, tol, fs) == [] and tol['env'] == FLOOR['env']
    assert 'env' in check(m, measure(x * 1.1, fs, case), masks, tol, fs)
    print('measure.py self-check ok')
