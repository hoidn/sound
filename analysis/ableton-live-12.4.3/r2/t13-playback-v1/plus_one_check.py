"""T1.3: where does the x86_64 placement model give one sample more than the exact ceiling? (analyst tool; output is data)

Regenerates the 40,000 cases of transport/sweep.py (same seed and generator, without the X part) and, for every case and
anchor counter N, classifies x86 - ideal by whether the exact rational position (b - b0) * SR * 60 / T is an integer, whether
binary64 spb equals SR * 60 / T exactly, and N; and, for both the x86 model and the arm64 fused model, by whether
the exact product q of the binary64 operands fl(b - b0) and spb, and q rounded to binary64, lie above the ideal P.
The x86 model itself is X-confirmed in transport/results/fire.json and sweep.json.
usage: python3 -I -B plus_one_check.py     (prints a tally; writes plus_one_check.json)
"""
import json, math, random, struct, sys
from collections import Counter
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
RATES = [44100, 48000, 88200, 96000]
COMMON = [60.0, 90.0, 100.0, 110.0, 120.0, 125.0, 128.0, 130.0, 135.0, 140.0, 150.0, 160.0, 170.0, 174.0, 175.0, 180.0]
NS = [0, 1 << 10, 1 << 20, 1 << 25, 1 << 30, (1 << 32) + 777]


def f32(x):
    return struct.unpack('<f', struct.pack('<f', x))[0]


def lattice(x):
    """Binary64 lattice rounding of REQ-CLIP-LAUNCH-013 (halves away from zero), as transport/run_transport.py."""
    h = 1.0 / 3843840
    s = 1.0 if x >= 0 else -1.0
    return s * (math.floor(abs(x + s * h * 0.5) * 3843840) / 3843840)


def lat_fr(x):
    return Fr(round(Fr(x) * 3843840), 3843840)


def main():
    sys.path.insert(0, str(HERE / 'transport'))
    from run_transport import lattice as lat_ref  # same rounding as the sweep
    rnd = random.Random(20261018)
    cases = []
    for _ in range(40000):
        sr = rnd.choice(RATES)
        t = rnd.choice(COMMON) if rnd.random() < 0.5 else f32(rnd.uniform(20, 999))
        b0 = lat_ref(rnd.choice([0.0, 0.0, rnd.randrange(0, 64) / 4, rnd.randrange(0, 3843840 * 8) / 3843840]))
        k = rnd.choice([1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 3843840])
        b = lat_ref(b0 + rnd.randrange(1, 4000) / k)
        cases.append((sr, t, b0, b))
    tally = Counter()
    tally2 = Counter()
    tally3 = Counter()
    for sr, t, b0, b in cases:
        spb = (sr / t) * 60.0
        exact = (lat_fr(b) - lat_fr(b0)) * sr * 60 / Fr(t)
        idl = math.ceil(exact)
        for n in NS:
            xv = math.ceil((b - b0) * spb + float(n)) - n
            av = math.ceil(math.fma(b - b0, spb, float(n))) - n
            spb_exact = Fr(spb) == Fr(sr) * 60 / Fr(t)
            q_above = Fr(b - b0) * Fr(spb) > idl  # exact product of the binary64 operands above P
            fq_above = (b - b0) * spb > idl          # that product rounded to binary64 above P
            tally[(xv - idl, exact.denominator == 1, spb_exact, n)] += 1
            tally2[(exact.denominator == 1, q_above, xv - idl, av - idl)] += 1
            tally3[(exact.denominator == 1, fq_above, xv - idl, av - idl)] += 1
    out = [{'x86_minus_ideal': k[0], 'exact_is_integer': k[1], 'spb_exact': k[2], 'N': k[3], 'count': v}
           for k, v in sorted(tally.items())]
    out2 = [{'exact_is_integer': k[0], 'binary64_product_above_P': k[1], 'x86_minus_ideal': k[2],
             'arm64_minus_ideal': k[3], 'count': v} for k, v in sorted(tally2.items())]
    out3 = [{'exact_is_integer': k[0], 'rounded_product_above_P': k[1], 'x86_minus_ideal': k[2],
             'arm64_minus_ideal': k[3], 'count': v} for k, v in sorted(tally3.items())]
    (HERE / 'plus_one_check.json').write_text(json.dumps({'by_class': out, 'by_product': out2,
                                                         'by_rounded_product': out3}, indent=1) + '\n')
    for row in out:
        print(row)
    for row in out2:
        print(row)
    for row in out3:
        print(row)


if __name__ == '__main__':
    main()
