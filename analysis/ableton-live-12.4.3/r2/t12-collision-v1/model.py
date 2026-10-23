"""Static model of Collision's mallet and modal resonator, for comparison with the X renders.
Analyst material only: it restates decompiled behaviour (Collision arm64 helper corpus, and the
Corpus model of ../t12-device-dsp-v1/model.py, whose modal resonator Collision shares) and must
never seed the independent reimplementation.

    m = CollisionModel(host, note=60, res=1, fs=44100)
    m.poles()                      # per mode: pole frequency (Hz), per-sample log radius, weights
    m.mallet_response(f_hz)        # complex response of the mallet pulse (deterministic part)

Host values are SetParameterA values (col.py). Controllers: kind 0 -> U rule (128v, or 126v + 1
above 0.5); kind 1 -> (v - min) * 127 / (max - min). Exponential module parameters take floor(c);
material, inharmonicity and brightness FL(c), positions and
the mallet noise amount TR(c) (all established by the renders, see results/collision.json).
Dependencies: numpy, ../corpus-dsp-v1/tables.py (mode-ratio tables).
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'corpus-dsp-v1'))
import tables  # noqa: E402

from col import idx  # noqa: E402

LN2 = math.log(2)
W0 = 2 * math.pi * 261.62
MODES = [4, 16, 30, 70]
TYPE_REMAP = [1, 2, 3, 4, 5, 7, 6]          # Live type -> internal type, as Corpus


def f32(x):
    return float(np.float32(x))


def A(x):                                   # the engine's 2^x
    n = math.floor(x)
    t = (x - n) * LN2
    return math.ldexp(1 + t + t * t * (0.5 + 0.200064 * t), n)


def U(v):
    v = min(max(f32(v), 0.0), 1.0)
    return f32(128 * v) if v <= 0.5 else f32(f32(126 * v) + 1)


def K1(v, lo, hi):
    v = min(max(f32(v), lo), hi)
    return f32(f32((v - lo) * 127) / (hi - lo))


def lin(c, lo, hi):
    n = 0.5 if 63.9999 < c < 64.0001 else c / 127
    return lo + n * (hi - lo)


def expo(c, lo, hi):
    return lo * (hi / lo) ** (c / 127)


def ratios(itype, N, R):
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


def TR(c):
    """Controller as a linear module parameter takes it: 64 when c/127 is within 1e-5 of one half,
    else floor(c + 0.4). (Exponential parameters take floor(c); see int(...) below.)"""
    return 64.0 if 0.49999 < c / 127 < 0.50001 else float(math.floor(c + 0.4))


def FL(c):
    """Controller as the resonator's material, inharmonicity and brightness take it: 64 when c/127 is
    within 1e-5 of one half, else floor(c)."""
    return 64.0 if 0.49999 < c / 127 < 0.50001 else float(math.floor(c))


class CollisionModel:
    """One resonator (res = 1 or 2) of one voice playing `note`, all Vel/Key amounts 0 except KeyToTranspose."""

    def __init__(self, host, note=60, res=1, fs=44100):
        g = lambda name: host[idx(f'Resonator{res}/{name}')]  # noqa: E731
        self.fs = fs
        t = int(g('Type'))
        self.itype = TYPE_REMAP[t] if t < 7 else 0
        self.N = MODES[min(int(g('Quality')), 3)]
        self.decay = expo(int(U(g('Decay'))), 0.05, 35)
        self.tone = lin(FL(K1(g('Damp'), -1, 1)), -1, 1)
        self.inharm = lin(FL(K1(g('Inharmonics'), -1, 1)), -1, 1)
        self.R = expo(int(U(g('Ratio'))), 1, 20)
        self.amp_freq = lin(FL(K1(g('AmpFreq'), -1, 1)), -1, 1)
        self.exci = lin(TR(K1(g('HitX'), -2, 2)), 0.05, 0.95)
        self.listen = {'L': lin(TR(K1(g('ListeningXL'), -2, 2)), 0.01, 0.99),
                       'R': lin(TR(K1(g('ListeningXR'), -2, 2)), 0.01, 0.99)}
        self.bleed = expo(int(U(g('Bleed'))), 0.01, 1)
        p = g('KeyToTranspose') * (note - 60) / 12 + g('Transpose') / 12 + g('FineTranspose') / 1200
        self.pitch = min(max(p, -5), 67 / 12)
        self.modes = ratios(self.itype, self.N, self.R)

    def shape(self, k, x):
        r, mn = self.modes[k]
        return shape1(k, self.N, x) if mn is None else shape2(mn, self.N, x)

    def poles(self):
        fs, out = self.fs, []
        inh = min(max(self.inharm ** 3, -1), 1)
        x = min(max(self.exci, 0.02), 0.98)
        for k, (r, mn) in enumerate(self.modes):
            L = math.log2(r)
            w = A(self.pitch) * W0 * r * A(inh * L)
            if w >= fs * 2.6179938:
                break
            t = self.tone
            e = (5 - L) * min(t, 1) if t >= 0 else -max(t, -1) * L
            d = 8 * A(e) / self.decay
            th = w / fs
            alpha = (math.pi / (math.pi - th)) * math.sin(th) * d / w
            a1, a2 = f32(-2 * math.cos(th) / (1 + alpha)), f32((1 - alpha) / (1 + alpha))
            rad = math.sqrt(a2)
            out.append(dict(k=k, r=r, mn=mn, nominal_hz=w / (2 * math.pi),
                            pole_hz=math.acos(min(1.0, -a1 / (2 * rad))) * fs / (2 * math.pi), log_radius=math.log(rad),
                            gain=alpha * A((L - 2) * self.amp_freq) / (2 * d * (1 + alpha)),
                            exc=self.shape(k, x), pick={c: self.shape(k, self.listen[c]) for c in 'LR'}))
        return out


def mallet_response(host, f_hz, fs=44100):
    """Deterministic part of the mallet pulse: an impulse of the Volume strength through a second-order
    low-pass at the Stiffness frequency (RBJ form, alpha = sin w, gain fs/(4000 w)), times (1 - n) of the
    noise mix. Returns complex response at f_hz (relative units)."""
    strength = expo(int(U(host[idx('Mallet/Volume')])), 0.001, 1)
    fc = min(max(expo(int(U(host[idx('Mallet/Stiffness')])), 2, 5000), 10), 20000)
    amt = lin(TR(U(host[idx('Mallet/NoiseAmount')])), -4, 4)
    n = (math.atan(amt) / math.pi + 0.5) ** 3
    w = min(2 * math.pi * fc / fs, 2.9919932)
    s, c = math.sin(w), math.cos(w)
    k = fs * 0.0025 * (1 - c) / (10 * w * (1 + s))
    b = np.array([k / 2, k, k / 2])
    a = np.array([1, -2 * c / (1 + s), (1 - s) / (1 + s)])
    z = np.exp(-2j * np.pi * np.asarray(f_hz, float) / fs)
    H = (b[0] + b[1] * z + b[2] * z * z) / (a[0] + a[1] * z + a[2] * z * z)
    return strength * (1 - n) * H
