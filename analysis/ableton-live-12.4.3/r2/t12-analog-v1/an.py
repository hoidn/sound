"""Analog (UltraAnalog) through the bundle's x86_64 slice: stored values -> host values -> renders.

    import an
    st = an.stored('table', **{'SignalChain1/OscillatorWaveShape': 0})
    y = an.render(st, an.note(60, 100, on=4400, off=48400), frames=65536)

Stored values are SPEC-BUNDLED-DEVICE-PARAMETERS r2 values (the 'table' set is the "Default when absent"
column, the 'preset' set the Defaults-preset column; both from n6-device-tables-v1/out/spec_defaults.tsv).
host() turns them into the 203 SetParameterA values with N6's conversions (n6 out/conversions.tsv,
column mode): identity, polarizer (|v| and a sign flag 1 for v < 0 on the next index), filter type
(v >> 1 and v & 1), multiply-offset, toggle mapping (v + 1 when the toggle is on, else 0), Polyphony
(max(v - 1, 0) and v > 0.5 on index 7), legacy-int quantization (nearest 1/32768, then toward zero),
and the unstored constants (ToggleDummy 1, DummyPerNotePitchBendRange 48).
Renders: a fresh process per render (xdevpy), create, rate, all 203 values in index order, events,
input flag 0, silent input, host blocks of 512 frames. Output frames x 2 binary32.
Dependencies: numpy, xdevpy (the loader in harness/, built to /var/tmp/sound-analysis/t12-analog/xdev).
"""
import csv
import math
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

import xdevpy

HERE = Path(__file__).resolve().parent
N6 = HERE.parent / 'n6-device-tables-v1' / 'out'
SCRATCH = Path(os.environ.get('AN_SCRATCH', '/var/tmp/sound-analysis/t12-analog/tmp'))
WORKERS = int(os.environ.get('AN_WORKERS', '8'))


def _rows(name):
    return [r for r in csv.DictReader((N6 / name).open(), delimiter='\t') if r['device'] == 'UltraAnalog']


SPEC_ROWS = _rows('spec_defaults.tsv')
CONV_ROWS = [r for r in _rows('conversions.tsv') if r['index']]


def _num(text):
    return {'true': 1.0, 'false': 0.0}.get(text, None) if text in ('true', 'false') else float(text)


def stored(which='table', **changes):
    """Stored values by path: the table defaults or the Defaults preset, with changes applied."""
    col = 'default' if which == 'table' else 'preset'
    st = {r['path']: _num(r[col] or r['default']) for r in SPEC_ROWS if r['class'] in ('Float', 'Enum', 'Bool')}
    for k, v in changes.items():
        if k not in st:
            raise KeyError(k)
        st[k] = float(v)
    return st


def legacy_int(v):
    q = math.floor(v * 32768 + 0.5) if v >= 0 else -math.floor(-v * 32768 + 0.5)
    return float(math.trunc(q / 32768))


def host(st):
    """203 host values {index: float} for stored values st (N6 conversions)."""
    out = {}
    for r in CONV_ROWS:
        i, name, mode = int(r['index']), r['stored_name'], r['mode']
        if name.startswith('(second output'):
            continue
        if name.endswith('ToggleDummy'):
            out[i] = 1.0
            continue
        if name == 'DummyPerNotePitchBendRange':
            out[i] = 48.0
            continue
        v = st[name]
        if r['user_converter'].startswith('legacyint'):
            v = legacy_int(v)
        if mode.startswith('ToToggleMapping'):
            out[i], out[7] = max(v - 1, 0.0), float(v > 0.5)
        elif mode.startswith('IndexedFloat'):
            out[i] = v
        elif mode.startswith('MultiplyOffset'):
            m, o = (float(t.split('=')[1]) for t in mode.split()[1:3])
            out[i] = o + m * v
        elif mode.startswith('ToggleMapping'):
            tog = mode.split('toggle=')[1]
            out[i] = v + 1 if st[tog] > 0.5 else 0.0
        elif mode == 'FilterType':
            out[i], out[i + 1] = float(int(v) >> 1), float(int(v) & 1)
        elif mode.startswith('ModulationPolarizer'):
            out[i], out[i + 1] = abs(v), float(v < 0)
        else:
            raise ValueError(mode)
    assert sorted(out) == list(range(203)), sorted(set(range(203)) - set(out))
    return out


def note(key=60, vel=100, on=4400, off=None, offvel=64):
    ev = [(on, 0x90, key, vel)]
    if off is not None:
        ev.append((off, 0x80, key, offvel))
    return ev


def script(hv, events, fs=44100, frames=65536, block=512, extra=()):
    lines = ['create', f'rate {fs}'] + [f'param {i} {v!r}' for i, v in sorted(hv.items())]
    lines += list(extra)
    lines += [f'event {f} {s:#x} {a} {b}' for f, s, a, b in sorted(events, key=lambda e: e[0])]
    return lines + ['inflag 0', 'input zero', f'process {frames} {block}', 'destroy']


def render(st, events, fs=44100, frames=65536, block=512, out=None, env=None, extra=(), hv=None):
    """Render stored values st (or host values hv) with events; returns frames x 2 float32."""
    SCRATCH.mkdir(parents=True, exist_ok=True)
    if out is None:
        fd, p = tempfile.mkstemp(suffix='.f32', dir=SCRATCH)
        os.close(fd)
        out = Path(p)
    y, log = xdevpy.render('Analog', script(hv if hv is not None else host(st), events, fs, frames, block, extra), out, env=env)
    if out.parent == SCRATCH:
        out.unlink()
        out.with_suffix('.script').unlink()
    return y, log


def pmap(fn, items):
    with ThreadPoolExecutor(WORKERS) as ex:
        return list(ex.map(fn, items))


# ---- measurements ------------------------------------------------------------------------------

def f0(y, fs, start, stop, guess):
    """Fundamental by demodulation around the guess (fit.track on a steady segment)."""
    import fit
    seg = np.asarray(y[:stop], float)
    return fit.track(seg, guess, fs, start, 20)['hz']


def harmonics(x, fs, f, n=10):
    """Amplitudes of harmonics 1..n of frequency f (least squares on cos/sin at k f), and the residual."""
    t = np.arange(len(x)) / fs
    cols = []
    for k in range(1, n + 1):
        cols += [np.cos(2 * np.pi * k * f * t), np.sin(2 * np.pi * k * f * t)]
    cols.append(np.ones_like(t))
    A = np.array(cols).T
    c, *_ = np.linalg.lstsq(A, x, rcond=None)
    amps = np.hypot(c[0:-1:2], c[1:-1:2])
    phases = np.arctan2(-c[1:-1:2], c[0:-1:2])
    res = x - A @ c
    return amps, phases, float(np.sqrt((res ** 2).mean())), float(c[-1])


def env_rms(x, win):
    """RMS in consecutive windows of win frames."""
    n = len(x) // win
    return np.sqrt((np.asarray(x[:n * win], float).reshape(n, win) ** 2).mean(1))


def first_above(y, thr=0.0):
    k = np.nonzero(np.abs(y).max(1) > thr)[0]
    return int(k[0]) if len(k) else None


def fund(x, fs, fmin=15.0):
    """Fundamental of a periodic segment: the strongest spectral peak, moved down to the lowest
    sub-multiple f/d (d <= 8) that carries at least 1e-3 of the peak amplitude, then refined by
    demodulation (fit.track) over the segment."""
    import fit
    x = np.asarray(x, float)
    n = 1 << int(np.ceil(np.log2(len(x) * 4)))
    sp = np.abs(np.fft.rfft(x * np.hanning(len(x)), n))
    hz = np.fft.rfftfreq(n, 1 / fs)
    sp[hz < fmin] = 0
    k = int(np.argmax(sp))
    f = hz[k]
    for d in range(8, 1, -1):
        j = int(round(k / d))
        lo, hi = max(j - 3, 1), j + 4
        if f / d >= fmin and sp[lo:hi].max() >= 1e-3 * sp[k]:
            f = hz[lo + int(np.argmax(sp[lo:hi]))]
            break
    return fit.track(x, f, fs, 0, min(20.0, f / 4))['hz']


def envelope(x, fs, hz, cutoff=None):
    """Amplitude envelope of a tone at hz: |2 * lowpass(x * exp(-i 2 pi hz n / fs))|, linear-phase FIR
    (cutoff default hz / 2), delay compensated; the first and last half filter lengths are NaN."""
    from scipy.signal import firwin, lfilter
    cutoff = cutoff or hz / 2
    taps = min(4001, int(3.3 * fs / cutoff) | 1)
    h = firwin(taps, cutoff, fs=fs)
    n = np.arange(len(x))
    z = lfilter(h, 1, np.asarray(x, float) * np.exp(-2j * np.pi * hz * n / fs))
    a = np.full(len(x), np.nan)
    d = (taps - 1) // 2
    a[:len(x) - d] = 2 * np.abs(z[d:])
    a[:taps] = np.nan
    return a


def zc_freq(x, fs):
    """Instantaneous frequency from upward zero crossings (linear interpolation): (times s, Hz)."""
    x = np.asarray(x, float)
    k = np.nonzero((x[:-1] < 0) & (x[1:] >= 0))[0]
    t = k + x[k] / (x[k] - x[k + 1])
    return (t[1:] + t[:-1]) / 2 / fs, fs / np.diff(t)


def inst_freq(x, fs):
    """Instantaneous frequency (Hz) of a single tone from the analytic signal's phase derivative."""
    from scipy.signal import hilbert
    ph = np.unwrap(np.angle(hilbert(np.asarray(x, float))))
    return np.gradient(ph) * fs / (2 * np.pi)
