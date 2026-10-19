"""T1.3 transport: sweep of the beat -> sample placement rule (analyst tool; output is data).

Model (x86_64 operation order of OScheduler::ProcessNextEvents / TStatus::PredictedLongSampleTime, confirmed by X
on 1,216 rows in results/fire.json): offset = ceil(fl(fl(fl(b - b0) * spb) + N)) - N, spb = fl(fl(SR / T) * 60).
arm64 order (fmadd + fcvtps): ceil(fma(fl(b - b0), spb, N)) - N.
Ideal: the least integer >= (b - b0) * SR * 60 / T in exact rational arithmetic, with b and b0 the lattice points
k/3,843,840 their binary64 values stand for and T the binary32 tempo.
Part 1 compares the three over random inputs. Part 2 runs PredictedLongSampleTime of the Live x86_64 slice on a
subset (hand-built TStatus: +0x28 spb, +0xa8 N, +0xb0 b0) and checks it equals the x86 model.
usage: python3 -I -B sweep.py      (writes results/sweep.json; prints a summary)
"""
import json, math, random, struct, sys
from collections import Counter
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from xexec import Runner  # noqa: E402
from run_transport import lattice, f32, PRED_SAMPLE, NOP  # noqa: E402

HERE = Path(__file__).resolve().parent
RATES = [44100, 48000, 88200, 96000]
COMMON = [60.0, 90.0, 100.0, 110.0, 120.0, 125.0, 128.0, 130.0, 135.0, 140.0, 150.0, 160.0, 170.0, 174.0, 175.0, 180.0]
NS = [0, 1 << 10, 1 << 20, 1 << 25, 1 << 30, (1 << 32) + 777]


def x86(d, spb, n):
    return math.ceil((d * spb) + float(n)) - n


def arm(d, spb, n):
    return math.ceil(math.fma(d, spb, float(n))) - n


def lat_fr(x):
    """The lattice point k/3,843,840 that the binary64 value x stands for."""
    return Fr(round(Fr(x) * 3843840), 3843840)


def ideal(b, b0, sr, t):
    return math.ceil((lat_fr(b) - lat_fr(b0)) * sr * 60 / Fr(t))


def main():
    rnd = random.Random(20261018)
    cases = []
    for _ in range(40000):
        sr = rnd.choice(RATES)
        t = rnd.choice(COMMON) if rnd.random() < 0.5 else f32(rnd.uniform(20, 999))
        b0 = lattice(rnd.choice([0.0, 0.0, rnd.randrange(0, 64) / 4, rnd.randrange(0, 3843840 * 8) / 3843840]))
        k = rnd.choice([1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 3843840])
        b = lattice(b0 + rnd.randrange(1, 4000) / k)
        cases.append((sr, t, b0, b))
    tally = Counter()
    examples = []
    for sr, t, b0, b in cases:
        spb = (sr / t) * 60.0
        d = b - b0
        idl = ideal(b, b0, sr, t)
        for n in NS:
            xv, av = x86(d, spb, n), arm(d, spb, n)
            tally[('x86-ideal', n, xv - idl)] += 1
            tally[('arm-x86', n, av - xv)] += 1
            if (xv != idl or av != xv) and len(examples) < 60:
                examples.append({'sr': sr, 'tempo': t, 'b0': b0, 'beat': b, 'N': n, 'x86': xv, 'arm64': av, 'ideal': idl})
    # common tempos: is spb exact (an integer or exactly representable rational)?
    spb_exact = {f'{sr}/{t}': Fr((sr / t) * 60.0) == Fr(sr) * 60 / Fr(t) for sr in RATES for t in COMMON}
    # part 2: X check of PredictedLongSampleTime on a subset
    r = Runner()
    sub = cases[:4000]
    xok = xbad = 0
    for i in range(0, len(sub), 200):
        chunk = sub[i:i + 200]
        toks = []
        for sr, t, b0, b in chunk:
            st = bytearray(0xb8)
            struct.pack_into('<i', st, 0, sr)
            struct.pack_into('<d', st, 0x28, (sr / t) * 60.0)
            struct.pack_into('<q', st, 0xa8, NS[i // 200 % len(NS)])
            struct.pack_into('<d', st, 0xb0, b0)
            toks += ['call', hex(PRED_SAMPLE), 'hex:' + st.hex(), f'd:{b!r}']
        res = r.run(toks)
        assert res.ok, res.stderr
        n = NS[i // 200 % len(NS)]
        for (sr, t, b0, b), c in zip(chunk, res.calls):
            v = c['rax'] - (1 << 64) if c['rax'] >> 63 else c['rax']
            if v - n == x86(b - b0, (sr / t) * 60.0, n):
                xok += 1
            else:
                xbad += 1
    out = {'cases': len(cases), 'anchors': NS,
           'tally': [{'kind': k[0], 'N': k[1], 'difference': k[2], 'count': v} for k, v in sorted(tally.items())],
           'spb_exact_common': spb_exact, 'examples': examples,
           'x_check': {'PredictedLongSampleTime_calls': xok + xbad, 'equal_x86_model': xok, 'differ': xbad}}
    json.dump(out, open(HERE / 'results/sweep.json', 'w'), indent=1)
    for row in out['tally']:
        print(row)
    print('X check', out['x_check'])
    print('spb exact for common tempos:', sum(spb_exact.values()), 'of', len(spb_exact),
          'inexact:', [k for k, v in spb_exact.items() if not v])


if __name__ == '__main__':
    main()
