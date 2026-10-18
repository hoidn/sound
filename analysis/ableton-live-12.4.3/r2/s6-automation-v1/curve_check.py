"""S6 static derivation: apply the traced FloatEvent curve rules to the shipped documents.

Usage: python3 -I curve_check.py <bundle Contents dir> <documents-survey.json>
Re-implements, from the disassembly kept in results/s6-0001 and s6-0002:
  monotone(p0,p1,p2,p3)   0x1012132d8  1-D cubic Bezier monotonicity test
  load reset              0x102778870  X=(0,x1,x2,1) and Y=(0,y1,y2,1) must both be monotone,
                                       otherwise all four controls become 0.5
  segment value           0x102403c88 / 0x101212e30 / 0x102404218: absolute Bezier through
                                       (t0,v0),(t0+x1*dt, v0+y1*dv),(t0+x2*dt, v0+y2*dv),(t1,v1);
                                       bisection on the curve parameter until |x(s)-t| <= 1e-8
and counts, over every FloatEvent carrying CurveControl attributes in the shipped LiveSet
documents, how many would be reset on load. A self-check (assert) pins the rules on fixed
inputs. Static derivation only: nothing here was executed by Live. Output is data.
"""
import collections, gzip, json, math, os, sys
import xml.etree.ElementTree as ET

LOW = -63072000.0


def monotone(p0, p1, p2, p3):
    if not all(math.isfinite(v) for v in (p0, p1, p2, p3)):
        return False
    if (p0 <= p1 <= p2 <= p3) or (p0 >= p1 >= p2 >= p3):
        return True
    d = p1 * p1 + p2 * p2 + p0 * p3 - p0 * p2 - p1 * p2 - p1 * p3   # compensated sum in Live
    if not all(math.isfinite(v) for v in (p1 * p1, p2 * p2, p0 * p3, p0 * p2, p1 * p2, p1 * p3)):
        return False
    if d <= 2.220446049250313e-16:
        return True
    a = p0 - 2 * p1 + p2
    den = 2 * (-p0 + 3 * p1 - 3 * p2 + p3)
    r = math.sqrt(d)
    r1 = ieee_div(2 * r - 2 * a, den)
    if 0.0 < r1 < 1.0:
        return False
    r2 = ieee_div(-2 * r - 2 * a, den)
    return r2 <= 0.0 or r2 >= 1.0      # NaN -> False, as fcmp/csinc in the disassembly


def ieee_div(n, d):
    if d:
        return n / d
    return math.nan if n == 0 else math.copysign(math.inf, n) * math.copysign(1.0, d)


def load_controls(c):
    x1, y1, x2, y2 = c
    return c if monotone(0.0, x1, x2, 1.0) and monotone(0.0, y1, y2, 1.0) else (0.5, 0.5, 0.5, 0.5)


def bez(p, s):
    u = 1 - s
    return u * u * u * p[0] + 3 * u * u * s * p[1] + 3 * u * s * s * p[2] + s * s * s * p[3]


def segment_value(t, t0, v0, t1, v1, c):
    """Value at t inside [t0, t1] for a curved segment (increasing time)."""
    x1, y1, x2, y2 = c
    xs = (t0, t0 + (t1 - t0) * x1, t0 + (t1 - t0) * x2, t1)
    ys = (v0, v0 + (v1 - v0) * y1, v0 + (v1 - v0) * y2, v1)
    if t <= t0:
        return v0
    if t >= t1:
        return v1
    lo, hi, s = 0.0, 1.0, 0.5
    x = bez(xs, s)
    while abs(t - x) > 1e-8:
        if x < t:
            lo = s
        else:
            hi = s
        s = (lo + hi) * 0.5
        x = bez(xs, s)
    return bez(ys, s)


def selfcheck():
    assert monotone(0, 0.5, 0.5, 1) and monotone(0, 0, 1, 1)
    assert monotone(0.0, 0.25, 0.75, 1.0)
    assert not monotone(0.0, 1.5, -0.5, 1.0)          # overshoots both ways
    assert load_controls((0.2, 1.4, 0.8, 1.4)) == (0.5, 0.5, 0.5, 0.5)
    assert load_controls((0.1, 0.0, 0.7, 1.0)) == (0.1, 0.0, 0.7, 1.0)
    # default controls give the straight line
    for t in (1.0, 1.25, 1.5, 1.9):
        assert abs(segment_value(t, 1.0, 10.0, 2.0, 20.0, (0.5, 0.5, 0.5, 0.5)) - (10 + 10 * (t - 1))) < 1e-6


def main():
    selfcheck()
    contents, survey = sys.argv[1:3]
    docs = [d[0] for d in json.load(open(survey))["per_document"]]
    out = collections.Counter()
    examples = []
    for rel in docs:
        root = ET.fromstring(gzip.open(os.path.join(contents, rel)).read())
        for ev in root.iter("FloatEvent"):
            if ev.get("CurveControl1X") is None:
                continue
            c = tuple(float(ev.get(k)) for k in ("CurveControl1X", "CurveControl1Y", "CurveControl2X", "CurveControl2Y"))
            kept = load_controls(c) == c
            out[f"kept={kept}"] += 1
            out[f"x_monotone={monotone(0.0, c[0], c[2], 1.0)}"] += 1
            out[f"y_monotone={monotone(0.0, c[1], c[3], 1.0)}"] += 1
            out[f"y_in_unit={0 <= c[1] <= 1 and 0 <= c[3] <= 1}"] += 1
            if not kept and len(examples) < 12:
                examples.append([rel, ev.get("Id"), ev.get("Time"), c])
    print(json.dumps({"curve_events": dict(sorted(out.items())), "reset_examples": examples}, indent=1))


if __name__ == "__main__":
    main()
