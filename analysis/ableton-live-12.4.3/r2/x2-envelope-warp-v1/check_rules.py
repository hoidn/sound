"""Re-derive the X2 warp results from the binary64 operation sequences stated in SPEC-WARP-MARKERS r3.

usage: python3 -I check_rules.py      (reads results/envelope-warp.json; exits non-zero on a mismatch)
Rules (each operation rounds to binary64; fma is fused, math.fma, Python >= 3.13):
  q(b):      b unchanged if b is one of +-1.7976931348623155e308, 1.7976931348623157e308, +inf;
             else s = +1 if b >= 0 else -1 (NaN gives -1), y = |b + s * (2.6015651015651016e-07 * 0.5)| * 3843840,
             q = s * floor(y) / 3843840  (floor of NaN or inf is itself).
  bounds:    for neighbour (sn, bn) and new SecTime p: d = p - sn, a = bn + d * (5 / 60), c = bn + d * (999 / 60),
             returned as (min(a, c), max(a, c)).
  convert:   k from an upper-bound search over the first n-1 coordinates, k = max(j - 1, 0);
             u = (x - xk) / (xk1 - xk); result = fma(u, yk1, fma(-u, yk, yk)).
"""
import bisect, json, math, sys
from pathlib import Path

SENT = {1.7976931348623155e308, -1.7976931348623155e308, 1.7976931348623157e308, math.inf}


def q(b):
    if b in SENT:
        return b
    s = 1.0 if b >= 0 else -1.0
    y = abs(b + s * (2.6015651015651016e-07 * 0.5)) * 3843840.0
    f = y if (math.isnan(y) or math.isinf(y)) else float(math.floor(y))
    return s * f / 3843840.0


def bounds(sn, bn, p):
    d = p - sn
    a, c = bn + d * (5.0 / 60.0), bn + d * (999.0 / 60.0)
    return [min(a, c), max(a, c)]


def convert(xs, ys, x):
    j = bisect.bisect_right(xs[:-1], x)
    k = max(j - 1, 0)
    u = (x - xs[k]) / (xs[k + 1] - xs[k])
    return math.fma(u, ys[k + 1], math.fma(-u, ys[k], ys[k]))


def same(a, b):
    return (isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b)) or a == b


def main():
    d = json.loads((Path(__file__).resolve().parent / 'results' / 'envelope-warp.json').read_text(),
                   parse_constant=lambda c: {'NaN': math.nan, 'Infinity': math.inf, '-Infinity': -math.inf}[c])
    bad = []
    for k, v in d['warp_edges_REQ015_016']['beat_grid_round'].items():
        if not same(q(float(k)), v):
            bad.append(('q', k, v, q(float(k))))
    cases = {'p1.5_nb(1,2)': (1.0, 2.0, 1.5), 'p1_nb(1,2)_ds0': (1.0, 2.0, 1.0),
             'p1.0004_nb(1,2)': (1.0, 2.0, 1.0004), 'p1.5_right_nb(2,3)': (2.0, 3.0, 1.5)}
    for k, v in d['warp_edges_REQ015_016']['add_bounds_lo_hi'].items():
        if bounds(*cases[k]) != v:
            bad.append(('bounds', k, v, bounds(*cases[k])))
    tables = {'warp_WMK016_M1': [(0.0, 0.0), (1.0, 2.0), (2.0, 3.0), (2.015625, 3.03125)],
              'warp_WMK017_M2': [(0.5, 1.0), (1.0, 2.0), (2.0, 3.0), (2.015625, 3.03125)]}
    for name, m in tables.items():
        secs, beats = [a for a, _ in m], [b for _, b in m]
        for t, v in d[name]['sample_to_beat'].items():
            if convert(secs, beats, float(t) / 48000.0) != v:
                bad.append((name, 's2b', t, v))
        for b, v in d[name]['beat_to_sample'].items():
            if convert(beats, secs, float(b)) * 48000.0 != v:
                bad.append((name, 'b2s', b, v))
    print('mismatches:', bad if bad else 'none')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
