"""Per-mode measurement of a decaying resonance by demodulation.

    t = track(signal, hz, fs, start, cutoff_hz)

The signal is mixed down by exp(-i*2*pi*hz*n/fs) and low-passed (linear-phase FIR, cutoff_hz).
After the filter has settled, straight lines are fitted to the unwrapped phase and to the log
magnitude. The result gives the mode's frequency (hz + phase slope), its per-sample log radius
(log-magnitude slope) and its complex amplitude extrapolated back to sample `start`. Applied
identically to a render and to a model output, the estimator's own bias (filter gain on a
decaying tone, leakage of neighbours) is the same in both and cancels in their difference.
Dependencies: numpy, scipy.
"""
import numpy as np
from scipy.signal import firwin, lfilter


def track(s, hz, fs, start, cutoff_hz):
    taps = min(4001, int(3.3 * fs / cutoff_hz) | 1)
    h = firwin(taps, cutoff_hz, fs=fs)
    n = np.arange(len(s))
    z = lfilter(h, 1, np.asarray(s, float) * np.exp(-2j * np.pi * hz * n / fs))
    seg = slice(start + taps, len(s))
    t = n[seg] - (taps - 1) // 2                      # time of the input each output sample represents
    if len(t) < taps:
        raise ValueError('window shorter than the filter')
    ph = np.polyfit(t, np.unwrap(np.angle(z[seg])), 1)
    la = np.polyfit(t, np.log(np.abs(z[seg])), 1)
    amp = 2 * np.exp(la[0] * start + la[1] + 1j * (ph[0] * start + ph[1]))
    return dict(hz=hz + ph[0] * fs / (2 * np.pi), log_radius=float(la[0]), amp=complex(amp), taps=taps)


if __name__ == '__main__':
    fs, n = 44100, np.arange(20000)
    y = 0.7 * 0.9999 ** n * np.cos(2 * np.pi * 440.01 * n / fs + 0.3) + 0.2 * np.cos(2 * np.pi * 600 * n / fs)
    t = track(y, 440, fs, 0, 40)
    assert abs(t['hz'] - 440.01) < 1e-4 and abs(t['log_radius'] - np.log(0.9999)) < 1e-8, t
    assert abs(abs(t['amp']) - 0.7) < 1e-3 and abs(np.angle(t['amp']) - 0.3) < 1e-3, t
    print('fit.py self-check ok')
