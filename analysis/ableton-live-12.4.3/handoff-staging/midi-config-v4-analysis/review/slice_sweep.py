"""Reviewer model sweep (analyst side; not X): largest |arm64 - x86_64| target difference over random ranges, every
7-bit value and every 14-bit pair, in binary32 units in the last place of R = max(|min|, |max|) and in tau."""
import random
import struct
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from review_checks import f32, tgt32  # noqa: E402

random.seed(7)


def ulp(x):
    x = abs(f32(x))
    return struct.unpack('<f', struct.pack('<I', struct.unpack('<I', struct.pack('<f', x))[0] + 1))[0] - x


xs = [float(v) for v in range(128)] + [f32(f32(float(q)) / 129.0) for q in range(0, 16384, 7)]
worst_u, worst_t = (0.0, None), (0.0, None)
for _ in range(600):
    M = 10 ** random.uniform(-2, 6)
    mn, mx = f32(random.uniform(-M, M)), f32(random.choice((1, -1)) * M)
    if mn == mx:
        continue
    R = max(abs(mn), abs(mx))
    tau = max(1e-6, 2.0 ** -22 * R)
    for xd in xs:
        dlt = abs(tgt32(xd, mn, mx, False, True) - tgt32(xd, mn, mx, False, False))
        if dlt / ulp(R) > worst_u[0]:
            worst_u = (dlt / ulp(R), (mn, mx, xd))
        if dlt / tau > worst_t[0]:
            worst_t = (dlt / tau, (mn, mx, xd))
print(f'largest arm64 - x86_64 target difference: {worst_u[0]:.3f} ulp(R) at {worst_u[1]}; {worst_t[0]:.3f} tau at {worst_t[1]}')
