"""Reviewer sweep (analyst side): largest |binary32 target - exact target| / tau over random ranges, both builds,
every 7-bit value and every 14-bit pair. Exact targets in binary64 (error ~1e-16 M, negligible against tau)."""
import random
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from review_checks import f32, libm  # noqa: E402

random.seed(20261018)


def tgt(xd, a, b, rev, arm):
    vv = f32(127.0 - xd) if rev else xd
    t = f32(vv / 127.0)
    s1 = f32(a * f32(1.0 - t))
    return float(libm.fmaf(b, t, s1)) if arm else f32(f32(b * t) + s1)


ranges = []
for _ in range(400):
    M = 10 ** random.uniform(-3, 6)
    k = random.random()
    mn, mx = f32(-M * k if random.random() < 0.5 else M * k * random.random()), f32(M * random.choice((1, -1)))
    if mn != mx:
        ranges.append((mn, mx))
ranges += [(f32(-2.0 ** e), f32(2.0 ** e - 1)) for e in range(3, 20)] + [(-128.0, 127.0), (-999.0, 999.0)]
xs = [(float(v), v / 127.0) for v in range(128)] + [(f32(f32(float(q)) / 129.0), q / 16383.0) for q in range(16384)]
worst = (0.0, None)
for mn, mx in ranges:
    a, b, rev = min(mn, mx), max(mn, mx), mx < mn
    tau = max(1e-6, 2.0 ** -22 * max(abs(mn), abs(mx)))
    for xd, frac in xs:
        ex = mn + (mx - mn) * frac
        for arm in (False, True):
            e = abs(tgt(xd, a, b, rev, arm) - ex) / tau
            if e > worst[0]:
                worst = (e, (mn, mx, xd, arm))
print(f'{len(ranges)} ranges; largest |binary32 - exact| over 7-bit values and pairs: {worst[0]:.3f} tau at '
      f'(min, max, data value, arm64) {worst[1]}')
