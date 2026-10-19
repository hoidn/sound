"""Behavioral model of Analog's control mappings, written from the spec's formulas (SPEC-DEVICE-ANALOG),
used by measure.py to check them against renders. Analysis tooling, not a port.

Conventions: host value v (what SetParameterA receives); controller c = 128 v for v <= 0.5, else
126 v + 1 (both binary32); A(x) is the 2^x approximation of REQ-DEVICE-ANALOG-005.
Dependencies: numpy.
"""
import numpy as np

f32 = np.float32
LN2 = np.float64(np.log(2))


def ctl(v):
    v = f32(min(max(v, 0.0), 1.0))
    return f32(v * f32(126) + f32(1)) if v > 0.5 else f32(v * f32(128))


def lin(c, lo, hi):
    n = f32(0.5) if abs(float(c) - 64) < 1e-4 else f32(c) * f32(1 / 127)
    return f32(lo + n * f32(hi - lo))


def expo(c, lo, hi):
    r = f32(hi) / f32(lo)
    n = (f32(np.exp(f32(c) * f32(1 / 127) * f32(np.log(r)))) - 1) / (r - 1)
    return f32(lo + n * f32(hi - lo))


def square(c, lo, hi):
    n = f32(0.25) if int(c) == 64 else f32(c * f32(1 / 127)) ** 2
    return f32(lo + n * f32(hi - lo))


def A(x):
    """2^x: whole octaves exact, the fraction by 1 + t + t^2 (0.5 + 0.200064 t), t = frac * ln 2 (binary32)."""
    x = f32(x)
    i = np.floor(x)
    t = f32((x - i) * LN2)
    return float(np.ldexp(f32(t + f32(1) + f32(f32(t * f32(0.200064) + f32(0.5)) * t * t)), int(i)))


def log2fs(fs):
    return f32(np.float64(np.log(f32(fs))) * (1 / LN2))


def detune_oct(v):
    """Oscillator Detune host value -> octaves: -(1 - c/64)^2 / 4 below c = 64, (c/64 - 1)^2 / 4 from 64."""
    c = ctl(v)
    return float(f32(0.25) * f32(c * f32(0.015625) - 1) ** 2) if c >= 64 else -float(f32(0.25) * f32(1 - c * f32(0.015625)) ** 2)


def osc_freq(key, fs, octave=0, transpose=0, fine=0.5, stretch=0.5, osc_oct=0, osc_semi=0, detune=0.5):
    """Oscillator frequency in Hz for a held key (no modulation, no glide, no error)."""
    s = float(lin(ctl(stretch), 0.992, 1.008))
    p = ((key - 69) * s + 9 + transpose + 12 * octave) / 12 + float(lin(ctl(fine), -1 / 24, 1 / 24))
    q = log2fs(fs) - f32(8.03136) - osc_oct - osc_semi / 12 - detune_oct(detune)
    return fs * A(p) / A(q)


def expo_smooth(c, lo, hi):
    """The level and cutoff curves: lo * (hi / lo)^(c / 127)."""
    return float(lo * (hi / lo) ** (float(c) / 127))


def S(phi):
    """The polynomial sine of the balance law: approximately sin(2 pi phi) for 0 <= phi <= 1/4."""
    p = f32(phi)
    p2 = p * p
    return float(p * f32(6.094263) + p * p * f32(6.094263) + p2 * (p2 * f32(121.88526) + p * (p2 * f32(-48.754105) + f32(-85.31969))))


def balance_gains(v):
    """(gain into filter 1, gain into filter 2) for a Balance host value v (1 - stored value)."""
    n = float(lin(ctl(v), 0, 1))
    return S((1 - n) / 4), S(n / 4)


def env_time(v, lo=0.005, hi=15.0):
    """Envelope segment time in seconds for a host value (exponential curve, binary32)."""
    return float(expo(ctl(v), lo, hi))


def segment(y0, y1, L, nsteps, exponential=True):
    """Envelope gains for steps 1 .. nsteps of a segment from y0 to y1 lasting L = T * fs frames (real),
    in binary32. N = int(L). Linear: y <- y + (y1 - y0) / N. Exponential: k = 3.4906588 / L,
    t = y0 + (y1 - y0) * 1.0313935, y <- y * (1 - k) + t * k. Steps beyond N hold exactly y1
    (step N + 1 is the segment's last frame; the next segment's step 1 follows it)."""
    N = int(L)
    out = np.empty(nsteps)
    y = f32(y0)
    if N < 1:
        out[:] = f32(y1)
        return out
    if exponential:
        k = f32(f32(3.4906588) / f32(L))
        a = f32(-(k - f32(1)))
        t = f32(f32(y0) + f32(f32(y1) - f32(y0)) * f32(1.0313935))
        tk = f32(t * k)
        for i in range(min(nsteps, N)):
            y = f32(f32(y * a) + tk)
            out[i] = y
    else:
        d = f32(f32(f32(y1) - f32(y0)) / f32(N))
        for i in range(min(nsteps, N)):
            y = f32(y + d)
            out[i] = y
    out[N:] = f32(y1)
    return out


def adsr(fs, nframes, A, D, S, exponential=True, ST=1.0):
    """Gain for frames 1 .. nframes after a note-on point while the key is held: attack 0 -> 1,
    decay 1 -> S, then the sustain segment S -> 0 over the sustain time. A, D, ST are host values,
    S the sustain gain."""
    parts, left = [], nframes
    for y0, y1, L in ((0, 1, env_time(A) * fs), (1, S, env_time(D) * fs), (S, 0, env_time(ST, 0.1, 1000) * fs)):
        n = min(left, int(L) + 1)
        parts.append(segment(y0, y1, L, n, exponential))
        left -= n
        if left <= 0:
            break
    out = np.concatenate(parts)
    if left > 0:
        out = np.concatenate([out, np.zeros(left)])
    return out[:nframes]
