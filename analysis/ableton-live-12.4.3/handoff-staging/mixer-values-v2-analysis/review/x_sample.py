"""Reviewer re-run of the mixer-values-v2 computed cases through the X2 harness (analyst side; never shipped).

  python3 -I -B x_sample.py > x_sample.out

Uses r2/x2-mixer-v1/harness/xexec.py and the target constants of r2/x2-mixer-v1/run_mixer.py, both imported unchanged.
At most 256 calls per process (loader limit): one curve build plus at most 200 conversions.
  1. every compute case of the payload (038 to 080), compared exactly and under its comparator;
  2. all 101 points G[k] of both curves, read back through position -> gain at binary32(k/100), compared with the
     reviewer's own restatement of spec.md REQ-005 (forward snap) and with the alternative end-only snap;
  3. a random sample of binary32 gains on both curves through gain -> position, then position -> gain, to test the
     round trip between curve points (finding F1), plus volume 0.3.
The reviewer's model is written from spec.md's text only (decimal exponential, correctly rounded to binary32).
"""
import json
import math
import random
import struct
import sys
from bisect import bisect_right
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
X2 = ROOT / 'analysis/ableton-live-12.4.3/r2/x2-mixer-v1'
STAGE = HERE.parents[1] / 'mixer-values-v2'
sys.dont_write_bytecode = True
sys.path.insert(0, str(X2))
import run_mixer as x  # noqa: E402  (constants and Runner; main() not run)

R, flt, as_f32 = x.R, x.flt, x.as_f32
MODE = {'volume': x.MODE_VOLUME, 'send': x.MODE_SEND}
MAX_CALLS = 0
getcontext().prec = 60
LN10 = Decimal(10).ln()


def f32(v):
    return struct.unpack('<f', struct.pack('<f', v))[0]


def bits(v):
    b = struct.unpack('<i', struct.pack('<f', v))[0]
    return b if b >= 0 else -(b & 0x7FFFFFFF)


def step(v, d):
    b = bits(v) + d
    return struct.unpack('<f', struct.pack('<i', b if b >= 0 else (-b) | -0x80000000))[0]


# ---- harness batches ----
def batch(fn, curve, args):
    """Run fn (POS_TO_GAIN or GAIN_TO_POS) on each binary32 arg against the built curve; one process per 200."""
    global MAX_CALLS
    out = []
    for i in range(0, len(args), 200):
        chunk = args[i:i + 200]
        toks = [*x.PATCH, 'call', hex(x.BUILD_CURVES), 'buf:64']
        for a in chunk:
            toks += ['call', hex(fn), flt(a), 'ref:' + x.curve_obj(MODE[curve])]
        res = R.run(toks)
        assert res.ok and len(res.calls) == len(chunk) + 1, (res.rc, res.stderr[-400:])
        MAX_CALLS = max(MAX_CALLS, len(res.calls))
        out += [as_f32(c['xmm0']) for c in res.calls[1:]]
    return out


def pan_x(w, p, sl, sr, v):
    g, res = x.pan_matrix(w, p, sl, sr, v)
    assert res.ok
    return dict(zip(('L->L', 'L->R', 'R->L', 'R->R'), g))


def xfade_x(code, positions):
    _, addr = x.XFADE[code]
    toks = []
    for p in positions:
        toks += ['call', hex(addr), flt(p)]
    res = R.run(toks)
    assert res.ok and len(res.calls) == len(positions)
    return [as_f32(c['xmm0']) for c in res.calls]


# ---- reviewer's restatement of spec.md REQ-005 ----
def nearest32(q):
    n = f32(float(q))
    return min((n, step(n, -1), step(n, 1)), key=lambda c: (abs(Fraction(c) - q), bits(c) & 1))


def curve(top, forward=True):
    snap = lambda z: 0.0 if abs(z) < 0.0001 else z
    keep = snap if forward else (lambda z: z)
    e = [f32(top)]
    for _ in range(60):
        e.append(keep(f32(e[-1] - f32(0.4))))
    s = f32(0.4)
    for _ in range(36):
        s = f32(s + f32(0.04))
        e.append(keep(f32(e[-1] - s)))
    a = f32(s + f32(0.04))
    e97 = f32(e[-1] - a)
    b = f32(f32(f32(3 * a) + f32(-70.0 - e97)) / 6)
    e.append(keep(e97))
    e.append(keep(f32(e[-1] - f32(a - b))))
    e.append(keep(f32(e[-1] + f32(b - f32(a - b)))))
    e.append(-70.0)
    D = [d if forward else snap(d) for d in e[::-1]]
    return [nearest32(Fraction((Decimal(f32(d * f32(0.05))) * LN10).exp())) for d in D]


def p2g(p, G):
    if p <= 0:
        return G[0]
    if p >= 1:
        return G[100]
    xx = 100.0 * p
    k = math.floor(xx)
    f = xx - k
    f = 0.0 if f <= 2.0 ** -17 else 1.0 if f >= 1 - 2.0 ** -17 else f
    return f32((1 - f) * G[k] + f * G[k + 1])


def g2p(g, G):
    if g < G[0]:
        return 0.0
    if g >= G[100]:
        return 1.0
    k = bisect_right(G, g) - 1
    return f32((k + (g - G[k]) / (G[k + 1] - G[k])) / 100)


def close32(got, exp, tol=None):
    return got == exp or (tol is not None and abs(got - exp) <= tol) or (f32(got) == got and abs(bits(got) - bits(exp)) == 1)


def main():
    cases = [c for c in json.loads((STAGE / 'cases.json').read_text())['cases'] if c['action'] == 'compute']
    G = {'volume': curve(6.0), 'send': curve(0.0)}
    Gend = {'volume': curve(6.0, False), 'send': curve(0.0, False)}

    print('== 1. every compute case re-run through the harness ==')
    exact = agree = 0
    for c in cases:
        cp, exp = c['compute'], c['expected']
        fn = cp['function']
        if fn == 'position-to-gain':
            got = {'gain': batch(x.POS_TO_GAIN, cp['curve'], [cp['position']])[0]}
            ok = close32(got['gain'], exp['gain'])
        elif fn == 'gain-to-position':
            got = {'position': batch(x.GAIN_TO_POS, cp['curve'], [cp['gain']])[0]}
            ok = abs(got['position'] - exp['position']) <= 1e-6
        elif fn == 'round-trip':
            pos = batch(x.GAIN_TO_POS, cp['curve'], [cp['gain']])[0]
            got = {'gain': batch(x.POS_TO_GAIN, cp['curve'], [pos])[0]}
            ok = got['gain'] == exp['gain'] == cp['gain']
        elif fn == 'pan-law':
            got = {'gains': pan_x(cp['w'], cp['pan'], cp['split_left'], cp['split_right'], cp['v'])}
            ok = all(close32(got['gains'][k], v, 1e-12) for k, v in exp['gains'].items())
        else:
            lv = xfade_x(cp['curve'], cp['positions'])
            got = {'levels': [{'position': p, 'level': l} for p, l in zip(cp['positions'], lv)]}
            ok = all(close32(g['level'], e['level'], 1e-12) for g, e in zip(got['levels'], exp['levels']))
        exact += got == exp
        agree += ok
        print(c['id'], fn, 'exact' if got == exp else 'DIFFERS ' + json.dumps(got), 'comparator', 'pass' if ok else 'FAIL')
    print(f'{exact}/{len(cases)} equal the payload exactly; {agree}/{len(cases)} pass their comparator')

    print('== 2. curve points G[k] through position -> gain at binary32(k/100) ==')
    for name in ('volume', 'send'):
        gx = batch(x.POS_TO_GAIN, name, [f32(k / 100) for k in range(101)])
        fwd = [k for k in range(101) if gx[k] != G[name][k]]
        end = [k for k in range(101) if gx[k] != Gend[name][k]]
        endsteps = sorted({abs(bits(gx[k]) - bits(Gend[name][k])) for k in end})
        print(f'{name}: X points differing from the forward-snap restatement: {len(fwd)} {fwd}')
        print(f'{name}: X points differing from an end-only snap: {len(end)} {end} (steps {endsteps})')
        if name == 'volume':
            print('  G[50], G[70] X:', gx[50], gx[70], ' end-only snap:', Gend[name][50], Gend[name][70])

    print('== 3. round trip of random binary32 gains (gain -> position -> gain), both through the harness ==')
    rng = random.Random(20261018 + 1)
    for name, n in (('volume', 800), ('send', 800)):
        Gc = G[name]
        gains = [f32(math.exp(rng.uniform(math.log(Gc[0]), math.log(Gc[100])))) for _ in range(n)]
        if name == 'volume':
            gains.append(f32(0.3))
        pos = batch(x.GAIN_TO_POS, name, gains)
        back = batch(x.POS_TO_GAIN, name, pos)
        st = [abs(bits(b) - bits(g)) for g, b in zip(gains, back)]
        on_point = sum(g in Gc for g in gains)
        mpos = sum(p == g2p(g, Gc) for g, p in zip(gains, pos))
        mback = sum(b == p2g(p, Gc) for p, b in zip(pos, back))
        hist = {s: st.count(s) for s in sorted(set(st))}
        print(f'{name}: {len(gains)} gains ({on_point} on a curve point); not returned exactly {sum(s > 0 for s in st)}; '
              f'worst {max(st)} binary32 steps; steps histogram {hist}')
        print(f'  restatement agrees with X: gain -> position {mpos}/{len(gains)}, position -> gain {mback}/{len(gains)}')
        inr = [s for g, s in zip(gains, st) if Gc[70] <= g < Gc[85]] if name == 'volume' else []
        if inr:
            print(f'  of these, {len(inr)} lie from G[70] (-6 dB) to below G[85] (0 dB); not returned exactly '
                  f'{sum(s > 0 for s in inr)}')
        if name == 'volume':
            print('  volume 0.3:', gains[-1], '-> position', pos[-1], '-> gain', back[-1])
    print(f'processes {len(R.log)}; largest call count per process {MAX_CALLS} (limit 256)')


if __name__ == '__main__':
    main()
