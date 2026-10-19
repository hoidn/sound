"""Reviewer check of two stated numbers (analyst side): the round-trip curve points' distance from a binary32 rounding
midpoint (spec.md: at least 0.16 of a step) and the shift of MIXER-VALUES-051 for a one-step change of a bottom point.
Uses x_sample.py's own restatement of REQ-005.   python3 -I -B margins.py > margins.out"""
import sys
from pathlib import Path
from decimal import Decimal
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fractions import Fraction
import x_sample as r

def exact_and_margin(top):
    import struct
    G = r.curve(top)
    # rebuild D as curve() does
    e = [r.f32(top)]
    snap = lambda z: 0.0 if abs(z) < 0.0001 else z
    for _ in range(60):
        e.append(snap(r.f32(e[-1] - r.f32(0.4))))
    s = r.f32(0.4)
    for _ in range(36):
        s = r.f32(s + r.f32(0.04)); e.append(snap(r.f32(e[-1] - s)))
    a = r.f32(s + r.f32(0.04)); e97 = r.f32(e[-1] - a)
    b = r.f32(r.f32(r.f32(3 * a) + r.f32(-70.0 - e97)) / 6)
    e.append(snap(e97)); e.append(snap(r.f32(e[-1] - r.f32(a - b)))); e.append(snap(r.f32(e[-1] + r.f32(b - r.f32(a - b))))); e.append(-70.0)
    D = e[::-1]
    out = {}
    for k in range(101):
        q = Fraction((Decimal(r.f32(D[k] * r.f32(0.05))) * r.LN10).exp())
        g = G[k]
        side = r.step(g, 1 if q > Fraction(g) else -1)
        out[k] = float(Fraction(1, 2) - abs(q - Fraction(g)) / abs(Fraction(side) - Fraction(g)))
    return G, out

for name, top, ks in (("volume", 6.0, (0, 70, 85, 100)), ("send", 0.0, (0, 85, 100))):
    G, m = exact_and_margin(top)
    print(name, "midpoint margins (steps):", {k: round(m[k], 3) for k in ks})
G = r.curve(6.0)
g = r.f32(0.001)
k = r.bisect_right(G, g) - 1
for j in (k, k + 1):
    for d in (-1, 1):
        G2 = list(G); G2[j] = r.step(G[j], d)
        print(f"051: gain 0.001 lies between G[{k}] and G[{k+1}]; one step {d:+d} at G[{j}] moves the position by",
              abs(r.g2p(g, G2) - r.g2p(g, G)))
