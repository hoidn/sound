"""Static derivation of Live's mixer gain curves and dB/pan display text (analysis aid, not application code).

Re-implements, in float32 arithmetic, the functions read in notes.md (all addresses in Live.arm64, SHA-256 3a99ceea...):
  0x101ac2bf8  per-curve 101-point dB table (step/increment per mode, landing at the minimum)
  0x101ac2ad8  dB table -> gain table, gain[100 - i] = exp10f(dB[i] * 0.05)
  0x101ac3498  normalized position (0..1) -> gain, linear interpolation between table points
  0x101ac353c  gain -> normalized position (binary search, linear interpolation)
  0x101437334  dB text: "-inf" when dB <= floor + 0.3, else up to 3 decimals, at least 1 (track volume/send formatter)
  0x101431c6c  "%.*f" formatting, trailing-zero strip down to the minimum decimals, zero when it rounds to 0
  0x10143a290  pan text: "C" for |p| <= 0.01, else round(|p| * 50) with "L"/"R"
  0x101b3b95c  per-track 2x2 output gain matrix from (split weight, pan, split L, split R, volume)
Mode ranges come from the int tables at 0x1058486a8 (max dB) / 0x1058486c4 (min dB), read by read_mem.py.
exp10f/log10f are emulated by double evaluation rounded to float32; Apple libm results may differ in the last ulp.
usage: python3 -I derive_curves.py > curves.txt ; a self-check runs first and exits non-zero on failure.
"""
import math, struct
from fractions import Fraction

MAXDB = [0, 6, 3, 24, 6, 0, 6]          # 0x1058486a8
MINDB = [-70, -70, -40, -70, -66, -42, -70]  # 0x1058486c4
NAMES = ["-70 to 0 dB", "-70 to +6 dB", "-40 to +3 dB", "-70 to +24 dB",
         "-66 to +6 dB Logarithmic", "-42 to 0 dB Logarithmic", "-70 to 6 dB RMS"]  # 0x1067568f8 list


def f(x):  # round to float32
    return struct.unpack('<f', struct.pack('<f', x))[0]


def bits(x):
    return struct.pack('>f', x).hex()


EPS = f(1e-4)  # 0x38d1b717


def snap(prev, d):  # fabd/fcmp/fcsel: 0 when |prev - d| < 1e-4, else prev - d
    return 0.0 if abs(f(prev - d)) < EPS else f(prev - d)


def db_table(mode):
    mx, mn = MAXDB[mode], MINDB[mode]
    if mode in (4, 5):
        step, inc = f(f(mx - mn) / f(101.0)), 0.0
    else:
        step, inc = {0: (0.4, 0.04), 1: (0.4, 0.04), 2: (0.4, 0.0), 3: (0.4, 0.04), 6: (0.6, 0.015)}[mode]
        step, inc = f(step), f(inc)
    t, v = [], f(mx)
    for _ in range(60):  # i = 0..59
        v = 0.0 if abs(v) < EPS else v
        t.append(v)
        v = f(v - step)
    t.append(0.0 if abs(v) < EPS else v)  # i = 60
    s3 = step
    for _ in range(36):  # i = 61..96
        s3 = f(inc + s3)
        t.append(snap(t[-1], s3))
    d97 = f(inc + s3)
    s3 = f(t[-1] - d97)
    s6 = f(f(mn) - s3)
    s6 = f(float(Fraction(d97) * 3 + Fraction(s6)))  # fmadd: single rounding
    s6 = f(s6 / f(6.0))
    t.append(0.0 if abs(f(t[-1] - d97)) < EPS else s3)  # i = 97
    s0 = f(d97 - s6)
    t.append(snap(t[-1], s0))  # i = 98
    s0 = f(s6 - s0)
    v = f(t[-1] + s0)
    t.append(0.0 if abs(v) < EPS else v)  # i = 99
    t.append(f(mn))  # i = 100
    return t


def gain_table(mode):
    db = db_table(mode)
    return [f(10 ** (f(db[100 - j] * f(0.05)))) for j in range(101)]  # index j = normalized * 100


def norm_to_gain(p, g):
    if p <= 0.0:
        return g[0]
    if p >= 1.0:
        return g[100]
    i = int(p * 100.0)
    fr = p * 100.0 - i
    fr = 0.0 if fr <= 7.62939453125e-06 else (1.0 if fr >= 0.9999923706054688 else fr)
    return f(fr * g[i + 1] + (1.0 - fr) * g[i])


def gain_to_norm(x, g):
    import bisect
    k = bisect.bisect_right(g, x)  # first index with g[k] > x
    if k == 0:
        return 0.0
    if k == 101:
        return 1.0
    return f(f(f(f(x - g[k - 1]) / f(g[k] - g[k - 1])) + f(k - 1)) * f(0.01))


def fmt_num(v, mx, mn):  # 0x101431c6c with width 0
    if round_away(10 ** mx * v) == 0:
        v = 0.0
    s = '%.*f' % (mx, v)
    if mx > mn and '.' in s:
        dot = s.index('.')
        while len(s) - 1 > dot + mn and s[-1] == '0':
            s = s[:-1]
        if s.endswith('.'):
            s = s[:-1]
    return s


def round_away(x):
    return math.floor(abs(x) + 0.5) * (1 if x >= 0 else -1)


def db_text(gain, floor=-70.0, n=3, n_min=1):  # 0x102183bf4 then 0x101437334 with flags 0x28 = 0x29 = 0x2a = 1
    db = f(f(math.log10(gain)) * f(20.0)) if gain > 0 else -140.0
    if floor + 0.3 >= db:
        return '-inf dB'
    d = round_away(abs(db) * 10 ** n) / 10 ** n
    if d >= 100:
        mx = mn = 0
    elif d >= 10:
        mx, mn = n, n_min
    else:
        mx, mn = n, n_min
    return fmt_num(db, mx, mn) + ' dB'


def pan_text(p):
    if -0.01 <= p <= 0.01:
        return 'C'
    return ('%.0f' % (abs(p) * 50.0)) + ('R' if p > 0 else 'L')


def matrix(w, pan, sl, sr, vol):  # 0x101b3b95c; returns (L->L, L->R, R->L, R->R)
    if vol == 0.0:
        return (0.0, 0.0, 0.0, 0.0)
    q = math.pi / 4
    tl, tr, tp = sl * q + q, sr * q + q, pan * q + q
    a, b = max(1e-05, math.cos(tp) * math.sqrt(2)), max(1e-05, math.cos(math.pi / 2 - tp) * math.sqrt(2))
    return tuple(f(x) for x in (vol * (w * f(math.cos(tl)) + (1 - w) * f(a)), vol * (w * f(math.cos(math.pi / 2 - tl))),
                                vol * (w * f(math.cos(tr))), vol * (w * f(math.cos(math.pi / 2 - tr)) + (1 - w) * f(b))))


def selfcheck():
    g1, g0 = gain_table(1), gain_table(0)
    # shipped MidiControllerRange text (N1 writer rule) equals the curve endpoints
    assert '%.13f' % g1[0] == '0.0003162277571', g1[0]
    assert bits(g1[100]) == '3fff64c2' and bits(g1[0]) == '39a5cb5f'
    assert g0[100] == 1.0 and g0[0] == g1[0]
    assert db_table(1)[15] == 0.0 and g1[85] == 1.0  # 0 dB sits at normalized 0.85 on the track volume curve
    assert db_text(g1[0]) == '-inf dB' and db_text(1.0) == '0.0 dB' and db_text(g1[100]) == '6.0 dB'
    assert pan_text(0.0049999999) == 'C' and pan_text(-1.0) == '50L' and pan_text(0.6) == '30R'
    assert matrix(0, 0, -1, 1, 1.0)[0] == f(1.0) and matrix(1, 0, -1, 1, 1.0)[2] < 1e-7


def main():
    selfcheck()
    for m in range(7):
        db, g = db_table(m), gain_table(m)
        print(f'== mode {m} "{NAMES[m]}" dB {MINDB[m]}..{MAXDB[m]}')
        print(' dB table (index i = (1 - normalized) * 100):', ' '.join('%g' % x for x in db))
        print(' gain at normalized 0, 0.5, 0.85, 1:', [g[0], norm_to_gain(0.5, g), norm_to_gain(0.85, g), g[100]],
              ' bits', bits(g[0]), bits(g[100]))
    g1, g0 = gain_table(1), gain_table(0)
    print('== track volume (mode 1) and send (mode 0) points')
    for db in (6, 0, -3, -6, -12, -18, -24, -36, -48, -60, -69.7, -69.8, -70):
        x = f(10 ** (db / 20))
        print(f' {db:>6} dB gain {x!r:<24} vol-norm {gain_to_norm(x, g1):.6f} send-norm {gain_to_norm(x, g0):.6f} text {db_text(x)!r}')
    print('== pan text', [(p, pan_text(p)) for p in (-1, -0.6, -0.2, -0.0101, -0.01, 0, 0.005, 0.01, 0.0101, 0.2, 0.33, 1)])
    print('== stereo-mode matrix (w=0) L->L, L->R, R->L, R->R at volume 1')
    for p in (-1, -0.5, 0, 0.5, 1):
        print(f' pan {p:>5}', ['%.7g' % v for v in matrix(0, p, -1, 1, 1.0)],
              ' dB', ['%.3f' % (20 * math.log10(v)) if v > 0 else '-inf' for v in matrix(0, p, -1, 1, 1.0)])
    print('== split-mode matrix (w=1) at volume 1')
    for sl, sr in ((-1, 1), (0, 0), (-1, -1), (1, 1)):
        print(f' L {sl:>3} R {sr:>3}', ['%.7g' % v for v in matrix(1, 0, sl, sr, 1.0)])


if __name__ == '__main__':
    main()
