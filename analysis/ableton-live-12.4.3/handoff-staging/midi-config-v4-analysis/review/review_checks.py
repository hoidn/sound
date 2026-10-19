"""Reviewer checks for the midi-config-v4 candidate (analyst side; never shipped).

  python3 -I -B review_checks.py behavior > review-checks.txt   # supersession, restatement, two-build model, precision
  python3 -I -B review_checks.py export <dir> > review-checks-export.json   # package checks of an exported copy

Written by the reviewer from spec.md, not from the author's model4() or run_x2.r5_model():
- exact(): an exact-rational restatement of the value clauses of spec.md, which also records every takeover test it
  reaches with the distance between the test's two sides, and every Value Scaling move.
- b32(): a binary32 model of the original's operation order for absolute values. Takeover, Pick-Up, the pair
  previous value and the final clamp are transliterated from the reviewer's reading of the arm64 dossier n7-0001
  (takeover 0x101b7c508, Pick-Up 0x101b7c344) and the x86 listing r2/x2-midi-v1/x86-disasm.txt. The two builds
  differ only in the target: x86 rounds hi*t and the sum separately; arm64 fuses them (glibc fmaf stands in).
- precision sweeps for findings F1 and F2 of the plan page and for stepped rounding.
"""
import ctypes
import difflib
import hashlib
import json
import re
import struct
import sys
from fractions import Fraction as F
from math import floor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
STAGE = HERE.parents[1] / 'midi-config-v4'
V3 = ROOT / 'handoff/midi-config-v3'
NEAR = 8
NEAR_CASES = {149} | set(range(152, 162))
MOVE_CASES = {129, 133, 137, 138, 143, 144, 145, 153, 155, 161}
libm = ctypes.CDLL('libm.so.6')
libm.fmaf.restype, libm.fmaf.argtypes = ctypes.c_float, [ctypes.c_float] * 3


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tau(mn, mx):
    return max(F(1, 10 ** 6), F(1, 2 ** 22) * max(abs(F(mn)), abs(F(mx))))


def rha(x):
    return F(floor(x + F(1, 2))) if x >= 0 else -F(floor(-x + F(1, 2)))


# ---- exact restatement of spec.md ------------------------------------------------------------------------------
A = [20, 1, 2, 3, 4, 5, 8, 10, 20, 50]
B = [50, 1, 2, 3, 4, 5, 8, 20, 50]


def a_(k):
    return A[k] if 1 <= k <= 9 else 20


def b_(k):
    return B[k] if 1 <= k <= 8 else 50


DECODE = {
    'LinearSignedBit': lambda v: v if v <= 64 else -(v - 64),
    'LinearSignedBit2': lambda v: -v if v <= 64 else v - 64,
    'LinearTwoCompliment': lambda v: v if v <= 64 else v - 128,
    'LinearBinaryOffset': lambda v: v - 64,
    'AccelSignedBit': lambda v: a_(v) if v <= 64 else -a_(v - 64),
    'AccelSignedBit2': lambda v: -b_(v) if v <= 64 else b_(v - 64),
    'AccelTwoCompliment': lambda v: b_(v) if v <= 65 else -b_(128 - v),
    'AccelBinaryOffset': lambda v: b_(v - 64) if v >= 64 else -b_(64 - v),
}


def pair_prev(m, l):
    if m is not None and l is not None:
        return F(128 * m + l, 129)
    if m is None and l is None:
        return F(-1, 129)
    if m is None:
        return -128 + F(l, 129)
    return F(-1, 129) if m % 2 else F(-1)


def exact(case, choice):
    """Values after each message, the takeover tests reached as (name, |side1 - side2|), and the move count."""
    s, p = case['stimulus'], case['stimulus']['parameter']
    a = case['expected']['assignments'][0]
    mode, cross = a['map_mode'], a['control'] == 'CrossfaderSlider'
    mn, mx, stepped, kind = F(p['min']), F(p['max']), p['stepped'], p['kind']
    lo, hi = min(mn, mx), max(mn, mx)
    cur, rec, held, out, tests, moves = F(p['initial_value']), {}, {}, [], [], 0

    def tgt(x):
        t = mn + (mx - mn) * x / 127
        if stepped:
            tests.append(('stepped rounding', abs(t - floor(t) - F(1, 2))))
            return rha(t)
        return t

    def takeover(n, xdata, pdata, has_prev):
        nonlocal moves
        c = cur
        if not has_prev:
            return c
        pv = tgt(pdata)
        tests.append(('p and -129', abs(pv + 129)))
        if pv == -129:
            return c
        w0, w = (hi - lo) / 256, (hi - lo) / 64
        tests.append(('c - (hi-lo)/256 and p', abs(pv - (c - w0))))
        if pv >= c - w0:
            tests.append(('c + (hi-lo)/256 and p', abs(c + w0 - pv)))
            if pv <= c + w0:
                return n
        if choice == 'pick-up':
            tests.append(('c and min(n, p) - w', abs(c - (min(n, pv) - w))))
            if c < min(n, pv) - w:
                return c
            tests.append(('c and max(n, p) + w', abs(max(n, pv) + w - c)))
            return n if c <= max(n, pv) + w else c
        tests.append(('c - w and n', abs(n - (c - w))))
        if n >= c - w:
            tests.append(('c + w and n', abs(c + w - n)))
            if n <= c + w:
                return n
        if xdata != pdata:
            tests.append(('p and n', abs(pv - n)))
        if pv == n:
            return c
        moves += 1
        return c + (hi - c) * (n - pv) / (hi - pv) if n > pv else c - (c - lo) * (pv - n) / (pv - lo)

    for m in s['messages']:
        _, num, v = (int(t, 16) for t in m.split())
        prev = rec.get(num)
        rec[num] = v
        if mode in DECODE:
            d = DECODE[mode](v)
            if stepped:
                step = 1 if (d > 0) == (mx > mn) else -1
                cur = min(max(cur + step, lo), hi)
            else:
                cur = min(max(cur + (mx - mn) * d / 256, lo), hi)
        elif mode == 'Absolute':
            n = tgt(F(v))
            direct = choice == 'none' or kind != 'continuous' or cross
            cur = n if direct else min(max(takeover(n, F(v), None if prev is None else F(prev), prev is not None), lo), hi)
        else:
            held[num] = (v, prev)
            if 20 in held and 52 in held:
                (msb, pm), (lsb, pl) = held.pop(20), held.pop(52)
                x = F(128 * msb + lsb, 129)
                n = tgt(x)
                if choice == 'none' or kind != 'continuous':
                    cur = n
                else:
                    cur = min(max(takeover(n, x, pair_prev(pm, pl), True), lo), hi)
        out.append(cur)
    return out, tests, moves


# ---- binary32 model of both builds (absolute modes) -------------------------------------------------------------
def f32(x):
    return struct.unpack('<f', struct.pack('<f', x))[0]


def roundf(x):
    return float(rha(F(x)))


def tgt32(xd, mn, mx, stepped, arm):
    lo, hi = f32(min(mn, mx)), f32(max(mn, mx))
    vv = f32(127.0 - xd) if mx < mn else xd
    t = f32(vv / 127.0)
    s1 = f32(lo * f32(1.0 - t))
    r = float(libm.fmaf(hi, t, s1)) if arm else f32(f32(hi * t) + s1)
    return roundf(r) if stepped else r


def take32(choice, n, prior_raw, pdata, c, mn, mx, stepped, arm):
    lo, hi = f32(min(mn, mx)), f32(max(mn, mx))
    c = lo if c < lo else hi if c > hi else c
    if prior_raw == -129.0:
        r = c
    else:
        p = tgt32(pdata, mn, mx, stepped, arm)
        w0 = f32(f32(f32(hi - lo) * 0.5) / 128.0)
        w = f32(f32(f32(hi - lo) + f32(hi - lo)) / 128.0)
        if p == -129.0:
            r = c
        elif f32(c - w0) <= p and f32(c + w0) >= p:
            r = n
        elif choice == 'pick-up':
            low, high = f32((n if n < p else p) - w), f32((n if n >= p else p) + w)
            r = c if low > c or high < c else n
        elif f32(c - w) <= n and f32(c + w) >= n:
            r = n
        elif p == n:
            r = c
        elif p <= n:
            s0 = f32(f32(hi - c) * f32(f32(n - p) / f32(hi - p)))
            r = f32(c + s0 * (-1.0 if s0 < 0 else 1.0))
        else:
            s0 = f32(f32(c - lo) * f32(f32(p - n) / f32(p - lo)))
            r = f32(c + s0 * (-1.0 if s0 > 0 else 1.0))
    return hi if r > hi else lo if r < lo else r


def b32(case, arm):
    s, p = case['stimulus'], case['stimulus']['parameter']
    a = case['expected']['assignments'][0]
    mode, cross, choice = a['map_mode'], a['control'] == 'CrossfaderSlider', s['takeover']
    mn, mx, stepped, kind = float(p['min']), float(p['max']), p['stepped'], p['kind']
    cur, rec, held, out = f32(p['initial_value']), {}, {}, []
    for m in s['messages']:
        _, num, v = (int(t, 16) for t in m.split())
        prev = rec.get(num, -129)
        rec[num] = v
        if mode == 'Absolute':
            n = tgt32(float(v), mn, mx, stepped, arm)
            direct = choice == 'none' or kind != 'continuous' or cross
            cur = n if direct else take32(choice, n, float(prev), float(prev), cur, mn, mx, stepped, arm)
        else:
            held[num] = (v, prev)
            if 20 in held and 52 in held:
                (msb, pm), (lsb, pl) = held.pop(20), held.pop(52)
                x = f32(f32(float(msb << 7 | lsb)) / 129.0)
                px = f32(f32(float(pm << 7 | pl)) / 129.0)     # -129 for a missing half, as both builds combine it
                n = tgt32(x, mn, mx, stepped, arm)
                cur = n if choice == 'none' or kind != 'continuous' else take32(choice, n, px, px, cur, mn, mx, stepped, arm)
        out.append(cur)
    return out


# ---- checks ------------------------------------------------------------------------------------------------------
def supersession():
    v3, v4 = (json.loads((d / 'cases.json').read_text()) for d in (V3, STAGE))
    recs = all(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True) for a, b in zip(v3['cases'], v4['cases']))
    fix = all((V3 / c['input']).read_bytes() == (STAGE / c['input']).read_bytes() for c in v3['cases'])
    v3man = json.loads((V3 / 'manifest.json').read_text())
    v3bad = [f['path'] for f in v3man['files'] if sha((V3 / f['path']).read_bytes()) != f['sha256']]
    rep = {k: (v3['representation'].get(k), v4['representation'].get(k)) for k in v4['representation']
           if v3['representation'].get(k) != v4['representation'].get(k)}
    print('== supersession')
    print(f"v3 cases {len(v3['cases'])}; v4 cases {len(v4['cases'])}; first 127 records equal: {recs}; "
          f"fixture bytes equal: {fix}; ids: {[c['id'] for c in v4['cases']] == [f'MIDI-CONFIG-{i:03d}' for i in range(1, 162)]}")
    print(f"v3 manifest sha256 {sha((V3 / 'manifest.json').read_bytes())}; v3 files listed {len(v3man['files'])}, "
          f"mismatches {v3bad}")
    print('representation fields changed:', sorted(rep))
    ok = all(pair_prev(m, l) == F(((-129 if m is None else m) << 7) | (-129 if l is None else l), 129)
             for m in [None, *range(128)] for l in [None, *range(128)])
    print(f'pair previous value: four-case rule equals the two-build combination ((m << 7) | l)/129 with -129 for a '
          f'missing half, all 16,641 combinations: {ok}')
    for name in ('README.md', 'AGENTS.md', 'spec.md'):
        a, b = (V3 / name).read_text().splitlines(), (STAGE / name).read_text().splitlines()
        rem = sum(1 for x in difflib.ndiff(a, b) if x.startswith('- '))
        print(f'{name}: v3 lines changed or removed {rem}')


def values():
    cases = [c for c in json.loads((STAGE / 'cases.json').read_text())['cases'] if 'stimulus' in c]
    print('\n== value cases: exact restatement (R), binary32 x86 model (X86), binary32 arm64 model (ARM)')
    near_found, move_found, far = set(), set(), []
    bad = 0
    for c in cases:
        k = int(c['id'][-3:])
        p, exp = c['stimulus']['parameter'], [F(v) for v in c['expected']['values']]
        t = tau(p['min'], p['max']) if k >= 128 else F(1, 10 ** 6)
        choices = ['none', 'pick-up', 'value-scaling'] if c['stimulus']['takeover'] == 'any' else [c['stimulus']['takeover']]
        rs = [exact(c, ch) for ch in choices]
        r_ok = all(len(v) == len(exp) and all(abs(a - b) <= t for a, b in zip(v, exp)) for v, _, _ in rs)
        r_err = max(abs(a - b) / t for v, _, _ in rs for a, b in zip(v, exp))
        tests = [m for _, ts, _ in rs for m in ts if m[0] != 'stepped rounding']
        stepped = [m for _, ts, _ in rs for m in ts if m[0] == 'stepped rounding']
        moves = sum(mv for _, _, mv in rs)
        mint = min((d / t for _, d in tests), default=None)
        if mint is not None and mint < NEAR:
            near_found.add(k)
        if moves:
            move_found.add(k)
        line = f"{c['id']} {c['stimulus']['takeover']:13} R within tau: {r_ok} (largest {float(r_err):.3f} tau)"
        if mint is not None:
            line += f"; nearest test {float(mint):.3g} tau"
        if stepped:
            line += f"; nearest half-integer {float(min(d for _, d in stepped) / t):.3g} tau"
        if moves:
            line += f'; moves {moves}'
        if k >= 128 or c['expected']['assignments'][0]['map_mode'].startswith('Absolute'):
            if k >= 128 and mint is not None and mint >= NEAR:
                far.append(mint)
            if c['stimulus']['takeover'] != 'any':
                x86, arm = b32(c, False), b32(c, True)
                x_ok = all(abs(F(a) - b) <= (F(5, 10 ** 10) if k >= 128 else t) for a, b in zip(x86, exp))
                a_ok = all(abs(F(a) - b) <= t for a, b in zip(arm, exp))
                a_d = max(abs(F(a) - F(b)) for a, b in zip(arm, x86)) / t
                line += (f"; X86 {'= expected' if k >= 128 else 'within tau'}: {x_ok}; ARM within tau: {a_ok} "
                         f"(ARM - X86 up to {float(a_d):.3f} tau)")
                bad += not (x_ok and a_ok)
        bad += not r_ok
        print(line)
    print(f'near-bound set found {sorted(near_found & set(range(128, 162)))}; listed {sorted(NEAR_CASES)}; '
          f'equal {near_found & set(range(128, 162)) == NEAR_CASES}; no carried case near a bound: {not near_found - set(range(128, 162))}')
    print(f'move set found {sorted(move_found)}; listed {sorted(MOVE_CASES)}; equal {move_found == MOVE_CASES}')
    print(f'smallest test distance in other new cases: {float(min(far)):.0f} tau; problems {bad}')


def sweep_ranges():
    return [(0., 1.), (0., 3.), (1., 0.), (3., -1.), (-1., 1.), (0., 4.25), (0., 8.), (-8., 8.), (0., 127.), (0., 128.),
            (-129., 0.), (20., 999.), (999., 20.), (-999., 999.), (-70., 6.), (0.25, 0.75), (1000., 1001.),
            (4096., 4100.), (-128., 127.), (16., -16.), (0.001, 2.)]


def data_values():
    xs7 = [(float(v), F(v)) for v in range(128)]
    xs14 = [(f32(f32(float(q)) / 129.0), F(q, 129)) for q in range(16384)]
    priors = [(f32(f32(float(-129 << 7 | l)) / 129.0), pair_prev(None, l)) for l in range(128)]
    priors += [(f32(f32(float(m << 7 | -129)) / 129.0), pair_prev(m, None)) for m in range(128)]
    return xs7, xs14 + priors


def precision():
    print('\n== precision: target error |binary32 - exact| over all 7-bit values, all 16,384 pairs and the 256 '
          'one-half pair previous values, both builds')
    xs7, xs14 = data_values()
    worst = (0, None)
    worst_p = (0, None)
    for mn, mx in sweep_ranges():
        t = tau(mn, mx)
        err = [max(abs(F(tgt32(xd, mn, mx, False, arm)) - (F(mn) + (F(mx) - F(mn)) * xx / 127)) / t
                   for xd, xx in xs for arm in (False, True)) for xs in (xs7 + xs14[:16384], xs14[16384:])]
        worst, worst_p = max(worst, (err[0], (mn, mx))), max(worst_p, (err[1], (mn, mx)))
        print(f'range {mn}..{mx}: largest error of a value {float(err[0]):.3f} tau; of a one-half pair previous '
              f'target {float(err[1]):.3f} tau')
    print(f'largest over the ranges: value {float(worst[0]):.3f} tau at {worst[1]}; one-half pair previous target '
          f'{float(worst_p[0]):.3f} tau at {worst_p[1]} (random ranges: tau_sweep.py)')
    flips()
    stepped_flips()
    move_error()


def flips():
    """Current values placed k*tau from each takeover bound; binary32 decision (both builds) against exact."""
    print('\n== precision: takeover tests with c placed near each bound (k*tau, k = -8..8 step 0.125)')
    ks = [F(i, 8) for i in range(-64, 65)]
    for mn, mx in [(0., 1.), (0., 3.), (3., -1.), (0., 8.), (-8., 8.), (20., 999.), (-999., 999.), (0., 128.), (1000., 1001.)]:
        lo, hi, t = min(mn, mx), max(mn, mx), tau(mn, mx)
        W0, W = (F(hi) - F(lo)) / 256, (F(hi) - F(lo)) / 64
        far_flip, tried = F(0), 0
        for v in range(0, 128, 3):
            xx = F(v)
            for arm in (False, True):
                p32 = tgt32(float(v), mn, mx, False, arm)
                px = F(mn) + (F(mx) - F(mn)) * xx / 127
                for b in (px - W0, px + W0, px - W, px + W):
                    for k in ks:
                        c = f32(float(b + k * t))
                        if not lo <= c <= hi:
                            continue
                        tried += 1
                        cc = F(c)
                        w0, w = f32(f32(f32(hi - lo) * 0.5) / 128.0), f32(f32(f32(hi - lo) + f32(hi - lo)) / 128.0)
                        sync32 = f32(c - w0) <= p32 <= f32(c + w0)
                        syncx = abs(px - cc) <= W0
                        near32 = f32(c - w) <= p32 <= f32(c + w)      # Value Scaling near-target form (target for n)
                        win32 = f32(p32 - w) <= c <= f32(p32 + w)     # Pick-Up window form (target for min/max(n, p))
                        nearx = abs(px - cc) <= W
                        for got, want, bound in ((sync32, syncx, W0), (near32, nearx, W), (win32, nearx, W)):
                            if got != want:
                                far_flip = max(far_flip, abs(abs(px - cc) - bound) / t)
        print(f'range {mn}..{mx}: {tried} placements; largest distance of a decision that differs: {float(far_flip):.3f} tau')


def stepped_flips():
    print('\n== precision: stepped rounding, binary32 (both builds) against exact, all 7-bit values and pairs')
    xs7, xs14 = data_values()
    for mn, mx in [(0., 3.), (-48., 48.), (0., 1000.), (0., 5000.), (0., 20000.), (0., 100000.), (20000., 0.)]:
        t = tau(mn, mx)
        n, far = [0, 0], F(0)
        for i, xs in enumerate((xs7, xs14)):
            for xd, xx in xs:
                ex = F(mn) + (F(mx) - F(mn)) * xx / 127
                for arm in (False, True):
                    if F(tgt32(xd, mn, mx, True, arm)) != rha(ex):
                        n[i] += 1
                        far = max(far, abs(ex - floor(ex) - F(1, 2)) / t)
        print(f'stepped range {mn}..{mx}: results that differ from the exact rule: 7-bit {n[0]}, pairs and pair '
              f'previous values {n[1]}; largest distance from a half-integer among them {float(far):.4f} tau')


def move_error():
    print('\n== precision: Value Scaling move |binary32 - exact| (finding F1), pairs near the top of the range, c = lo')
    for mn, mx in [(0., 1.), (0., 3.), (0., 127.)]:
        lo, hi, t = mn, mx, tau(mn, mx)
        qs = range(16383 - 200, 16384)
        x32 = {q: f32(f32(float(q)) / 129.0) for q in qs}
        worst = (F(0), None)
        for pq in qs:
            for nq in range(pq + 1, min(pq + 12, 16384)):
                n32, p32 = tgt32(x32[nq], mn, mx, False, False), tgt32(x32[pq], mn, mx, False, False)
                nx, px = F(lo) + (F(hi) - F(lo)) * F(nq, 16383), F(lo) + (F(hi) - F(lo)) * F(pq, 16383)
                if abs(px - lo) <= (F(hi) - F(lo)) / 256 or abs(nx - lo) <= (F(hi) - F(lo)) / 64:
                    continue
                c = f32(lo)
                got = f32(c + f32(f32(hi - c) * f32(f32(n32 - p32) / f32(hi - p32))))
                want = F(c) + (F(hi) - F(c)) * (nx - px) / (F(hi) - px)
                e = abs(F(got) - want) / t
                if e > worst[0]:
                    worst = (e, (pq, nq, got, float(want)))
        print(f'range {mn}..{mx}: largest move error {float(worst[0]):.1f} tau at (previous pair, pair, binary32, exact) {worst[1]}')


# ---- package checks of an exported copy -----------------------------------------------------------------------------
DENY = [r'0x[0-9a-fA-F]{4,}', r'\+0x', r'FUN_', r'DAT_', r'analysis/', r'raw/', r'wiki/', r'\.\./', r'/home/', r'/var/',
        r'/tmp/', r'decompil', r'disassembl', r'pseudocode', r'Ghidra', r'dossier', r'corpus', r'\bgdb\b', r'xexec',
        r'\bstub', r'harness', r'run_x2', r'fmaf?\b', r'fmadd', r'frinta', r'roundss', r'libm', r'cxa', r'pthread',
        r'operator new', r'\bApply\b', r'value function', r'combiner', r'setter', r'dispatch', r'receiver', r'registry',
        r'handler', r'PickUp', r'TakeOver', r'LMidi', r'sControl', r'OSet', r'OChange', r'TTimeable', r'Timeable',
        r'MidiInput', r'InputHistory', r'input_history', r'Launch_Control', r'FLT_MAX', r'3\.40282', r'sentinel',
        r'marker', r'\bprior', r'quantiz', r'[Zz]oom', r'sensitivity', r'accumulator', r'\bthread', r'vtable',
        r'offset', r'\bMT-\d', r'\bT[KB]-\d', r'\bE1\d\b', r'\bI\d\b', r'PRB-', r'\bQ-0', r'S-cond', r'\bF[1-4]\b',
        r'\bX[12]\b', r'\bRV[1-3]-', r'\bN7', r'Languages', r'\.alp', r'\.pyc', r'Python', r'configparser', r'_Framework',
        r'UserScript', r'GenericScript', r'Remote Script', r'precision-model', r'author-validation', r'traceability']
ALLOWED = {'AGENTS.md': {'decompil'}, 'spec.md': {'harness'}}  # forbidden-inputs list; carried 'not an executable harness' sentence


def slugs(text):
    return {re.sub(r'[^\w\- ]', '', h.strip().lower()).replace(' ', '-') for h in re.findall(r'^#+ (.+)$', text, re.M)}


def export(d):
    d = Path(d)
    man = json.loads((d / 'manifest.json').read_text())
    files = sorted(p for p in d.rglob('*') if p.is_file() and p.name != 'manifest.json')
    bad = [f['path'] for f in man['files'] if not (d / f['path']).is_file()
           or sha((d / f['path']).read_bytes()) != f['sha256'] or (d / f['path']).stat().st_size != f['bytes']]
    inv = sorted({str(p.relative_to(d)) for p in files} ^ {f['path'] for f in man['files']})
    links, unresolved = 0, []
    for md in d.glob('*.md'):
        for target in re.findall(r'\]\(([^)\s]+)\)', md.read_text()):
            links += 1
            path, _, anchor = target.partition('#')
            dest = (md.parent / path).resolve() if path else md
            ok = not re.match(r'[a-z]+:', target) and dest.is_file() and d.resolve() in dest.parents
            if ok and anchor:
                ok = anchor in slugs(dest.read_text())
            if not ok:
                unresolved.append(f'{md.name}: {target}')
    cases = json.loads((d / 'cases.json').read_text())['cases']
    deny = {}
    for p in [*files, d / 'manifest.json']:
        hits = sorted({m for pat in DENY for m in re.findall(pat, p.read_text())} - ALLOWED.get(p.name, set()))
        if hits:
            deny[str(p.relative_to(d))] = hits
    fx = [c['input'] for c in cases]
    raw = [(d / f).read_bytes() for f in fx]
    fixtures = {'count': len(fx), 'missing': [f for f in fx if not (d / f).is_file()],
                'not_ascii_lf': [f for f, b in zip(fx, raw) if not b.isascii() or b'\r' in b or not b.endswith(b'\n')
                                 or re.search(rb'[\x00-\x09\x0b-\x1f\x7f]', b)]}
    statuses = {'manifest': man['release_status'], 'review': man['review']['status'],
                'cases': json.loads((d / 'cases.json').read_text())['status']}
    return {'dir': str(d), 'payload_files': len(files), 'listed': len(man['files']), 'hash_or_size_mismatches': bad,
            'inventory_differences': inv, 'symlinks': [str(p) for p in d.rglob('*') if p.is_symlink()],
            'markdown_links': links, 'unresolved_links': unresolved, 'deny_list_hits': deny, 'fixtures': fixtures,
            'case_count': len(cases), 'manifest_case_count': man['case_count'], 'statuses': statuses,
            'manifest_sha256': sha((d / 'manifest.json').read_bytes())}


if __name__ == '__main__':
    if sys.argv[1] == 'export':
        print(json.dumps(export(sys.argv[2]), indent=1))
    else:
        assert sys.argv[1:] == ['behavior']
        supersession()
        values()
        precision()
