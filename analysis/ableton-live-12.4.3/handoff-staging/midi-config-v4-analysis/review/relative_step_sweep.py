"""Reviewer model sweep (analyst side; not X): rounding of one continuous relative step in binary32, in the
operation order of the x86 listing (f32(f32(f32(hi - lo) / 256) * d) added to the current value, then clamped;
negated for a reversed range), against the exact rule from the same current value. Units of tau."""
import random
import struct
from fractions import Fraction as F


def f32(v):
    return struct.unpack('<f', struct.pack('<f', v))[0]


random.seed(18)
worst = (F(0), None)
for _ in range(3000):
    M = 10 ** random.uniform(-3, 6)
    mn, mx = f32(random.uniform(-M, M)), f32(random.uniform(-M, M))
    if mn == mx:
        continue
    lo, hi, rev = min(mn, mx), max(mn, mx), mx < mn
    tau = max(F(1, 10 ** 6), F(1, 2 ** 22) * max(abs(F(mn)), abs(F(mx))))
    for _ in range(20):
        cur = f32(random.uniform(lo, hi))
        d = random.choice([1, 2, 3, 5, 8, 20, 50, 63, 64, -1, -7, -50, -64])
        step = f32(f32(f32(hi - lo) * 0.00390625) * d)
        step = -step if rev else step
        got = min(max(f32(step + cur), lo), hi)
        want = min(max(F(cur) + (F(mx) - F(mn)) * d / 256, F(lo)), F(hi))
        e = abs(F(got) - want) / tau
        if e > worst[0]:
            worst = (e, (mn, mx, cur, d))
print(f'largest rounding of one continuous relative step: {float(worst[0]):.3f} tau at (min, max, current, d) {worst[1]}')
