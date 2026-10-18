"""Reviewer check of REQ-WARP-MARKERS-015/016 edge bands (analyst side; not payload). python3 -I edges.py
Compares the contract's exact rules with the add's own floating-point procedure as the evidence shows it:
beat bounds nb.beat + (bpm/60)*ds, min/max, inclusive; grid rounding sign*floor(|b + sign*step/2|*3843840)/3843840.
Inputs stay inside the released scope (magnitudes below 1,000,000; neighbour beats need not be on the grid,
because opening does not round). Seeds are fixed."""
import math, random
from fractions import Fraction as F

N, STEP = 3843840, 2.6015651015651016e-07


def q_fp(b):
    s = 1.0 if b >= 0 else -1.0
    return s * (math.floor(abs(b + s * STEP * 0.5) * 3843840.0) / 3843840.0)


def q_exact(b):
    n = math.floor(abs(F(b)) * N + F(1, 2))
    return F(n if b >= 0 else -n, N)


def fp_ok(p, qr, s, b):
    ds = p - s
    a, c = (999.0 / 60.0) * ds + b, (5.0 / 60.0) * ds + b
    lo, hi = (c, a) if c < a else (a, c)
    return not (lo > qr or hi < qr)


def tempo_run(seed, min_gap, samples):
    random.seed(seed)
    worst, n = F(0), 0
    for _ in range(samples):
        b = random.uniform(-1e6, 1e6)
        s = random.choice([random.uniform(-1e6, 1e6), random.uniform(999000, 999999), random.uniform(0, 3)])
        p = s + 10 ** random.uniform(math.log10(min_gap), -1.5) * random.choice([1, -1])
        if abs(F(p) - F(s)) < F(min_gap) or abs(p) >= 1e6:
            continue
        lim = random.choice([5.0, 999.0])
        qr = q_fp(b + lim / 60 * (p - s) + random.uniform(-1e-6, 1e-6))
        t = (F(qr) - F(b)) / (F(p) - F(s)) * 60
        n += 1
        if (5 <= t <= 999) != fp_ok(p, qr, s, b):
            worst = max(worst, abs(t - F(lim)))
    return n, float(worst)


print("tempo: largest distance from 5 or 999 BPM at which the exact rule and the bounds disagree")
print("  gaps >= 0.001 s (author's band 0.000001 BPM):", tempo_run(1, 1e-3, 600000))
print("  gaps >= 0.0005 s (review band 0.001 BPM):   ", tempo_run(2, 5e-4, 600000))
# grid rounding: worst disagreement distance from a tie, in grid steps, for |b| < 1e6
random.seed(3)
worst, n = 0.0, 0
for _ in range(600000):
    k = random.randrange(-N * 10**6 + 1, N * 10**6 - 1)
    off = random.uniform(-2e-3, 2e-3)
    b = float((F(k) + F(1, 2) + F(off)) / N)
    if abs(b) >= 1e6:
        continue
    x = abs(F(b)) * N
    dist = float(abs(x - math.floor(x) - F(1, 2)))
    n += 1
    if q_fp(b) != float(q_exact(b)):
        worst = max(worst, dist)
print("rounding: samples", n, "largest tie distance (grid steps) with a disagreement:", worst,
      "(author's band 0.000001, review band 0.001)")
