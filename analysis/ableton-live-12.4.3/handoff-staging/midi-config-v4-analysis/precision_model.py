"""Precision scoping for the midi-config-v4 exclusions (analyst side; a model, not extracted execution).

  python3 -I precision_model.py > precision-model.txt     # a few minutes

Compares the exact rules of spec.md with a binary32 model of the original's operation order, for ranges whose
smaller bound is 0 (where the two builds agree exactly). The binary32 target model and the Value Scaling operation
order are those of r2/x2-midi-v1/run_x2.py (models() x86 branch and vs32()); the target model equals the X results
on every value run there. Two questions:
  1. How far can a Value Scaling move lie from the exact formula, in units of tau?
  2. Do takeover bound tests decide differently from exact arithmetic when the current value lies a few binary32
     steps from the exact bound?
"""
import struct
from fractions import Fraction as F


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def step32(x, k):
    """The binary32 value k steps from positive binary32 x."""
    return struct.unpack("<f", struct.pack("<I", struct.unpack("<I", struct.pack("<f", x))[0] + k))[0]


def target32(x, lo, hi, rev):
    a, b = f32(min(lo, hi)), f32(max(lo, hi))
    vv = f32(f32(127.0) - f32(x)) if rev else f32(x)
    t = f32(vv / 127.0)
    return f32(f32(b * t) + f32(a * f32(1.0 - t)))


def vs32(c, n, p, lo, hi):
    w0, w = f32(f32(0.5 * f32(hi - lo)) / 128), f32(f32(f32(hi - lo) + f32(hi - lo)) / 128)
    if f32(c - w0) <= p <= f32(c + w0) or f32(c - w) <= n <= f32(c + w):
        return n, "n"
    if p == n:
        return c, "c"
    if n > p:
        return f32(c + f32(f32(hi - c) * f32(f32(n - p) / f32(hi - p)))), "move"
    return f32(c - f32(f32(c - lo) * f32(f32(p - n) / f32(p - lo)))), "move"


def vs_exact(c, n, p, lo, hi):
    if abs(p - c) <= (hi - lo) / 256 or abs(n - c) <= (hi - lo) / 64:
        return n, "n"
    if p == n:
        return c, "c"
    if n > p:
        return c + (hi - c) * (n - p) / (hi - p), "move"
    return c - (c - lo) * (p - n) / (p - lo), "move"


def data_values(pairs):
    return [F(m << 7 | l, 129) for m in range(0, 128, 3) for l in range(0, 128, 9)] if pairs else [F(v) for v in range(128)]


def moves(mn, mx, pairs):
    lo, hi, rev = min(mn, mx), max(mn, mx), mx < mn
    tau = max(1e-6, 2 ** -22 * max(abs(mn), abs(mx)))
    xs = data_values(pairs)
    t32 = [target32(f32(float(x)), lo, hi, rev) for x in xs]
    tx = [F(mn) + (F(mx) - F(mn)) * x / 127 for x in xs]
    worst, branch = (0.0, None), 0
    for k in range(33):
        c = f32(lo + (hi - lo) * k / 32)
        for i in range(len(xs)):
            for j in range(len(xs)):
                a, ba = vs32(c, t32[j], t32[i], lo, hi)
                b, bb = vs_exact(F(c), tx[j], tx[i], F(lo), F(hi))
                if ba != bb:
                    branch += 1
                elif ba == "move" and abs(F(a) - b) / F(tau) > worst[0]:
                    worst = (float(abs(F(a) - b) / F(tau)), (c, float(xs[i]), float(xs[j])))
    return worst, branch


def bound_flips(mn, mx, steps=4):
    """In-sync test |p - c| <= (hi - lo)/256 with c a few binary32 steps from p + (hi - lo)/256."""
    lo, hi = min(mn, mx), max(mn, mx)
    flips, tried = [], 0
    for v in range(128):
        p32, px = target32(float(v), lo, hi, mx < mn), F(mn) + (F(mx) - F(mn)) * v / 127
        b = f32(float(px + F(hi - lo) / 256))
        if not 0 < b < hi:
            continue
        for k in range(-steps, steps + 1):
            c = step32(b, k)
            tried += 1
            w0 = f32(f32(0.5 * f32(hi - lo)) / 128)
            got32, gotx = f32(c - w0) <= p32 <= f32(c + w0), abs(px - F(c)) <= F(hi - lo) / 256
            if got32 != gotx:
                flips.append((v, k, c, got32, gotx))
    return tried, flips


if __name__ == "__main__":
    for mn, mx, pairs in [(0., 1., False), (0., 127., False), (1., 0., False), (0., 1., True), (0., 3., False)]:
        worst, branch = moves(mn, mx, pairs)
        print(f"moves range {mn}..{mx} {'14-bit sample' if pairs else '7-bit'}: largest |binary32 - exact| = "
              f"{worst[0]:.3f} tau at (c, previous x, x) = {worst[1]}; branch differences {branch}")
    for mn, mx in [(0., 1.), (0., 127.), (0., 3.)]:
        tried, flips = bound_flips(mn, mx)
        print(f"in-sync bound range {mn}..{mx}: {tried} current values within 4 binary32 steps of the exact bound, "
              f"{len(flips)} decided differently; first {flips[:3]}")
