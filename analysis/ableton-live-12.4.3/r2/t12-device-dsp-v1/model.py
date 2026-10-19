"""The static Corpus model of wiki/research/corpus-dsp-static.md (and the corpus-dsp-v1 reports),
written out as formulas, for comparison with extracted-execution renders. Analyst material only:
it restates decompiled behaviour and must never seed the independent reimplementation.

Scope: steady state of the modal resonator types (Beam, Marimba, String, Membrane, Plate) with the
LFO off, the band filter off and MIDI pitch off, after every ramp has finished. Waveguide types are
not modelled here (the port covers them).

    m = CorpusModel(host_values, fs)          # host_values: {SetParameterA index: value}
    m.poles('L')                              # per mode: frequency (Hz), per-sample radius, ...
    m.response(freqs_hz, 'L')                 # complex steady-state gain, input L+R equal

`coef32=True` rounds the per-mode filter coefficients to binary32, as the engine stores them.
Dependencies: numpy and corpus-dsp-v1/tables.py (the mode-ratio rebuild script).
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'corpus-dsp-v1'))
import tables  # noqa: E402  (beam, marimba, string, grid2d)

LN2 = math.log(2)
W0 = 1643.807                      # 2*pi*261.62 rad/s
MODES = [4, 16, 30, 70]
TYPE_REMAP = [1, 2, 3, 4, 5, 7, 6]  # Live ResonanceType -> internal type


def f32(x):
    return float(np.float32(x))


def pow2(x):                       # engine's 2^x: cubic in the fractional part
    n = math.floor(x)
    t = (x - n) * LN2
    return math.ldexp(1 + t + t * t * (0.5 + 0.200064 * t), n)


# host value -> controller (wrapper), all in binary32 as the wrapper computes them
def D(v):
    v = min(f32(v), 1.0)
    return f32(128 * v) if v <= 0.5 else f32(f32(126 * v) + 1)


def B(v):
    v = f32(v)
    return f32(f32(63.5 * v) + 63.5) if v < 0 else f32(f32(63 * v) + 64)


def POS(v):
    return f32(f32(31.5 * f32(v)) + 64)


# controller -> value (module drivers); the resonator truncates its controllers first
def lin(c, lo, hi):
    n = 0.5 if 63.9999 < c < 64.0001 else c / 127
    return lo + n * (hi - lo)


def expo(c, lo, hi):
    return lo * (hi / lo) ** (c / 127)


def P(t):                          # panpot curve
    return t * (10.392633 - 31.177902 * t + 20.785267 * t * t)


def ratios(itype, N, R):
    """Mode ratios and 2-D indices of internal type itype with N modes (tables.py)."""
    if itype == 1:
        return [(r, None) for r in tables.beam(N)]
    if itype == 2:
        return [(r, None) for r in tables.marimba(N)]
    if itype in (0, 3):
        return [(r, None) for r in tables.string(N)]
    return [(r, (m, n)) for r, m, n in tables.grid2d(N, R, itype == 5)]


def shape1(k, N, x):
    G = N + 2
    q = x * (G - 1)
    i = min(G - 2, math.floor(q))
    f = q - i
    T = [math.sin(math.pi * (k + 1) * j / (N + 1)) for j in (i, i + 1)]
    return 0.5 * (T[0] + f * (T[1] - T[0]))


def shape2(mn, N, x, y=0.44375):
    G = math.floor(math.sqrt(N)) + 3
    m, n = mn
    s = lambda a, u: math.sin(math.pi * a * u / (G - 1))  # noqa: E731
    qx, qy = x * (G - 1), y * (G - 1)
    i, j = min(G - 2, math.floor(qx)), min(G - 2, math.floor(qy))
    fx, fy = qx - i, qy - j
    v = lambda a, b: s(m, a) * s(n, b)  # noqa: E731
    return 0.5 * ((1 - fy) * ((1 - fx) * v(i, j) + fx * v(i + 1, j)) + fy * ((1 - fx) * v(i, j + 1) + fx * v(i + 1, j + 1)))


class CorpusModel:
    def __init__(self, host, fs, coef32=False):
        self.h, self.fs, self.coef32 = host, fs, coef32
        g = lambda i: host[i]  # noqa: E731
        self.itype = TYPE_REMAP[int(g(0))] if int(g(0)) < 7 else 0
        if self.itype in (6, 7):
            raise ValueError('waveguide types are not modelled')
        self.N = MODES[min(int(g(33)), 3)]
        self.decay = expo(int(D(g(1))), 0.05, 35)
        self.tone = lin(int(B(g(2))), -1, 1)
        self.inharm = lin(int(B(g(3))), -1, 1)
        self.R = expo(int(D(g(4))), 1, 20)
        self.amp_freq = lin(int(B(g(11))), -1, 1)
        self.exci = lin(int(POS(g(14))), 0.05, 0.95)
        self.listen = {'L': lin(int(POS(g(15))), 0.01, 0.99), 'R': lin(int(POS(g(16))), 0.01, 0.99)}
        self.amp = expo(64, 0.25, 4)
        self.amp_hp = expo(int(D(g(36))), 0.01, 1)
        det = lin(B(g(9)), -1 / 12, 1 / 12)
        p = lin(D(g(6)), -4, 4)
        self.pitch = {'L': min(max(p + det, -5), 67 / 12), 'R': min(max(p - det, -5), 67 / 12)}
        a = D(g(32)) / 127
        self.wet, self.dry = P(a / 4), P(0.25 - a / 4)
        self.drive = expo(D(g(30)), 0.17783, 5.6234)
        w = lin(D(g(31)), 0, 1)
        self.width = (0.5 + 0.5 * w, 0.5 - 0.5 * w)
        self.modes = ratios(self.itype, self.N, self.R)

    def shape(self, k, x):
        r, mn = self.modes[k]
        return shape1(k, self.N, x) if mn is None else shape2(mn, self.N, x)

    def coefs(self, ch):
        """Per-mode filter coefficients for channel ch ('L' or 'R'); bleed section or None."""
        fs, p, out = self.fs, self.pitch[ch], []
        inh = min(max(self.inharm ** 3, -1), 1)
        x = min(max(min(max(self.exci, 0), 1), 0.02), 0.98)
        last, bleed = None, True
        for k, (r, mn) in enumerate(self.modes):
            L = math.log2(r)
            w = pow2(p) * W0 * r * pow2(inh * L)
            if w >= fs * 2.6179938:
                bleed = False
                break
            t = self.tone
            e = (5 - L) * min(t, 1) if t >= 0 else -max(t, -1) * L
            d = 8 * pow2(e) / self.decay
            th = w / fs
            alpha = (math.pi / (math.pi - th)) * math.sin(th) * d / w
            tilt = pow2((L - 2) * self.amp_freq)
            c = dict(k=k, r=r, mn=mn, w=w, th=th, d=d, alpha=alpha,
                     g=alpha * self.amp * tilt / (2 * d * (1 + alpha)),
                     a1=-2 * math.cos(th) / (1 + alpha), a2=(1 - alpha) / (1 + alpha),
                     exc=self.shape(k, x), pick=self.shape(k, self.listen[ch]))
            if self.coef32:
                for key in ('g', 'a1', 'a2', 'exc', 'pick'):
                    c[key] = f32(c[key])
            out.append(c)
            last = (w, th, d, tilt)
        bl = None
        if bleed and last:
            w, th, d, tilt = last
            aH = 32 * (math.pi / (math.pi - th)) * math.sin(th) * d / w
            bl = dict(b0=((1 + math.cos(th)) / 2) * self.amp * tilt / ((1 + aH) * w),
                      a1=-2 * math.cos(th) / (1 + aH), a2=(1 - aH) / (1 + aH))
        return out, bl

    def poles(self, ch):
        """Per mode: pole frequency (Hz) and radius from its (a1, a2), and its residue weight."""
        res, _ = self.coefs(ch)
        for c in res:
            rad = math.sqrt(c['a2'])
            c['pole_hz'] = math.acos(min(1.0, -c['a1'] / (2 * rad))) * self.fs / (2 * math.pi)
            c['radius'] = rad
            c['nominal_hz'] = c['w'] / (2 * math.pi)
        return res

    def resonator_response(self, f, ch):
        z1 = np.exp(-2j * np.pi * np.asarray(f, float) / self.fs)
        res, bl = self.coefs(ch)
        H = np.zeros_like(z1)
        for c in res:
            H += c['g'] * c['exc'] * c['pick'] * (1 - z1 ** 2) / (1 + c['a1'] * z1 + c['a2'] * z1 ** 2)
        if bl:
            H += bl['b0'] * self.amp_hp * (1 - 2 * z1 + z1 ** 2) / (1 + bl['a1'] * z1 + bl['a2'] * z1 ** 2)
        return 3000 * H

    def response(self, f, ch):
        """Output channel ch for the same input on both channels (filter off, after all ramps)."""
        A, Bw = self.width
        other = 'R' if ch == 'L' else 'L'
        Hres = A * self.resonator_response(f, ch) + Bw * self.resonator_response(f, other)
        return self.drive * self.wet * Hres + self.dry


if __name__ == '__main__':
    assert pow2(0) == 1.0 and abs(pow2(0.5) - 1.4149585) < 1e-6
    assert D(0.5) == 64.0 and B(0.0) == 64.0 and POS(1.0) == 95.5
    host = {i: 0.0 for i in range(38)}
    host.update({1: 0.5, 4: 0.5, 5: 0.5, 6: 0.5, 14: 0.5, 15: 0.1, 16: 0.9, 30: 0.5, 31: 1, 32: 0.5, 33: 2, 34: 1, 35: 1})
    m = CorpusModel(host, 44100)
    assert m.itype == 1 and abs(m.poles('L')[0]['nominal_hz'] - 261.62) < 0.01
    print('model.py self-check ok')
