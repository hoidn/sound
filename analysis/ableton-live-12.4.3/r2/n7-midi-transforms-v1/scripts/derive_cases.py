"""derive_cases.py OUT.json -- static derivation of N7 acceptance cases (analysis tool, not an implementation).

Models the native path traced in ../notes.md: decoder 0x101b7b96c, value function 0x101b76bf0, apply 0x101b7fde4,
takeover 0x101b7c508/0x101b7c344, CC receiver 0x101b7f894, 14-bit pairing 0x101b8028c/0x101b802bc/0x101b7fcc0,
prior table 0x101b65b68. Arithmetic is float32 per instruction (fmadd fused); expected values are reported to 1e-6.
Expected outputs are static derivations, never observed runs.
"""
import sys, json, struct
from fractions import Fraction

def f(x): return struct.unpack('<f', struct.pack('<f', float(x)))[0]          # round to float32
def fma(a, b, c): return f(float(Fraction(a) * Fraction(b) + Fraction(c)))    # fused multiply-add
A = [1, 2, 3, 4, 5, 8, 10, 20, 50]; B = [1, 2, 3, 4, 5, 8, 20, 50]
MODE = {'Absolute': 0, 'AccelSignedBit': 1, 'AccelBinaryOffset': 2, 'AccelTwoCompliment': 3, 'AccelSignedBit2': 4,
        'Absolute14Bit': 5, 'LinearSignedBit': 6, 'LinearBinaryOffset': 7, 'LinearTwoCompliment': 8, 'LinearSignedBit2': 9}
NONE, PICKUP, SCALING = 0, 1, 2
UNKNOWN_PRIOR, NO_PRIOR = -129.0, f(3.4028235e38)

def decode(v, m):  # 0x101b7b96c
    i = int(v)
    def look(t, idx, fb, pos): return (t[idx] if 0 <= idx < len(t) else fb) * (1 if pos else -1)
    if m == 1: return look(A, i - 65 if i >= 65 else i - 1, 20.0, i < 65)
    if m == 2: return look(B, i - 65 if i > 63 else 63 - i, 50.0, i > 63)
    if m == 3: return look(B, 127 - i if i >= 66 else i - 1, 50.0, i < 66)
    if m == 4: return look(B, i - 65 if i > 64 else i - 1, 50.0, i > 64)
    if m == 6: return v if i < 65 else f(64.0 - v)
    if m == 7: return f(v - 64.0)
    if m == 8: return v if i < 65 else f(v - 128.0)
    if m == 9: return -v if i < 65 else f(v - 64.0)
    return 0.0

def value_fn(cur, lo, hi, v, m, sens, quant, inv):  # 0x101b76bf0
    if m in (0, 5):
        x = f(f(127.0 - v) if inv else v); t = f(x / 127.0)
        r = fma(hi, t, f(lo * f(1.0 - t)))
    else:
        d = f(decode(v, m) * sens)
        step = (1.0 if d > 0 else -1.0) if quant else f(f(f(hi - lo) * f(1 / 256)) * d)
        r = f(cur + (-step if inv else step)); r = hi if r > hi else r; r = lo if r < lo else r
    return float(round(r)) if quant else r  # frinta: ties away from zero (Python round differs only at exact .5)

def takeover(cur, new, prior, lo, hi, m, tm, quant, inv):  # 0x101b7c508 / 0x101b7c344
    c = lo if cur < lo else (hi if cur > hi else cur); r = new
    if tm != NONE:
        r = c
        if prior != UNKNOWN_PRIOR:
            pp = value_fn(c, lo, hi, prior, m, 1.0, quant, inv)
            steps = 16384.0 if m == 5 else 128.0; tol = f(f(f(hi - lo) * 0.5) / steps)
            if f(c - tol) <= pp <= f(c + tol): r = new
            elif tm == SCALING:
                t2 = f(f(f(hi - lo) * 2) / steps)
                if f(c - t2) <= new <= f(c + t2): r = new
                elif pp == new: r = c
                elif pp <= new: r = f(c + f(f(hi - c) * f(f(new - pp) / f(hi - pp))))
                else: r = f(c - f(f(c - lo) * f(f(pp - new) / f(pp - lo))))
            elif tm == PICKUP:
                t2 = f(f(f(hi - lo) * 2) / (16384.0 if m == 5 else 128.0))
                r = new if f(min(new, pp) - t2) <= c <= f(max(new, pp) + t2) else c
            else: r = new
    return hi if r > hi else (lo if r < lo else r)

class Mapping:
    """One script mapping of CC `cc` (14-bit: MSB cc, LSB cc+32) on channel 0 to a parameter."""
    def __init__(s, mode, kind='float', lo=0.0, hi=1.0, quant=False, value=0.5, avoid=False, thr=(64, 127), tm=NONE):
        s.m, s.kind, s.lo, s.hi, s.q, s.val, s.avoid, s.thr, s.tm = MODE[mode], kind, f(lo), f(hi), quant, f(value), avoid, thr, tm
        s.acc = 0.0; s.msb = s.lsb = s.pmsb = s.plsb = NO_PRIOR
    def apply(s, v, prior):  # 0x101b7fde4, Zoom = 1.0 branch
        lo, hi = min(s.lo, s.hi), max(s.lo, s.hi); inv = s.hi < s.lo
        if s.kind == 'bool':
            if s.m in (0, 5):
                a, b = min(s.thr), max(s.thr); s.val = 1.0 if ((a <= v <= b) != (s.thr[0] > s.thr[1])) else 0.0
            else: s.val = 1.0 if decode(v, s.m) > 0 else 0.0
            return
        new = value_fn(s.val, lo, hi, v, s.m, 1.0, s.q, inv)
        if s.m in (0, 5) and s.kind == 'float' and prior != NO_PRIOR:
            new = takeover(s.val, new, prior, lo, hi, s.m, s.tm, s.q, inv)
        s.val = new
    def cc(s, v, prior):  # 0x101b7f894 (mode != 5)
        if s.avoid: prior = NO_PRIOR
        if s.m not in (0, 5) and s.q:
            s.acc += 1.0 if decode(v, s.m) > 0 else -1.0
            if abs(s.acc) < 1: return
            s.acc -= 1.0 if s.acc >= 0 else -1.0
        s.apply(float(v), prior)
    def pair(s):  # 0x101b7fcc0; avoid flag is fixed false for 14-bit
        p = NO_PRIOR if NO_PRIOR in (s.pmsb, s.plsb) else f((int(s.plsb) | (int(s.pmsb) << 7)) / 129.0)
        s.apply(f((int(s.lsb) | (int(s.msb) << 7)) / 129.0), p); s.msb = s.lsb = s.pmsb = s.plsb = NO_PRIOR

def run(mapping, cc, msgs, priors=None):
    """msgs: list of (controller, value). Prior table per controller starts at -129 unless `priors` given."""
    table = dict(priors or {}); out = []
    for ctl, v in msgs:
        prior = table.get(ctl, UNKNOWN_PRIOR); table[ctl] = float(v)
        if mapping.m == 5:
            if ctl == cc: mapping.msb, mapping.pmsb = float(v), prior
            elif ctl == cc + 32: mapping.lsb, mapping.plsb = float(v), prior
            if NO_PRIOR not in (mapping.msb, mapping.lsb): mapping.pair()
        elif ctl == cc: mapping.cc(v, prior)
        out.append(round(mapping.val, 6))
    return out

def case(cid, title, mode, msgs, prec, cc=20, priors=None, **kw):
    m = Mapping(mode, **kw); exp = run(m, cc, msgs, priors)
    return {'id': cid, 'title': title, 'map_mode': mode, 'controller': cc, 'channel': 0,
            'preconditions': prec, 'input': [('B0 %02X %02X' % (c, v)) for c, v in msgs],
            'expected_after_each_message': exp, 'tolerance': 1e-6, 'provenance': 'static derivation (N7); unexecuted'}

P = 'continuous parameter, is_quantized false, min 0.0, max 1.0, value 0.5; no CC 20/52 received on this input since it was opened'
def build():
    C = []
    C.append(case('MT-01', 'Absolute: v/127 of the range, jump (Takeover None)', 'Absolute', [(20, 0), (20, 64), (20, 127)], P + '; Takeover Mode None'))
    C.append(case('MT-02', 'Absolute14Bit: MSB then LSB', 'Absolute14Bit', [(20, 100), (52, 50)], P + '; Takeover Mode None'))
    C.append(case('MT-03', 'Absolute14Bit: LSB then MSB', 'Absolute14Bit', [(52, 50), (20, 100)], P + '; Takeover Mode None'))
    C.append(case('MT-04', 'Absolute14Bit: latest MSB wins; a pair is consumed', 'Absolute14Bit', [(20, 16), (20, 100), (52, 50), (52, 0)], P + '; Takeover Mode None'))
    C.append(case('MT-05', 'Absolute14Bit: full scale', 'Absolute14Bit', [(20, 127), (52, 127), (20, 0), (52, 0)], P + '; Takeover Mode None'))
    rel = {'LinearSignedBit': [1, 65, 64, 127], 'LinearSignedBit2': [1, 65, 64], 'LinearTwoCompliment': [1, 127, 65, 64],
           'LinearBinaryOffset': [65, 63, 64, 0], 'AccelSignedBit': [1, 7, 9, 10, 65, 73, 0],
           'AccelSignedBit2': [1, 65, 7, 71, 0], 'AccelTwoCompliment': [1, 127, 8, 65, 66, 0],
           'AccelBinaryOffset': [65, 63, 70, 57, 64]}
    for n, (mode, vals) in enumerate(rel.items(), 6):
        C.append(case('MT-%02d' % n, '%s: per-message steps of (max-min)/256 x decoded delta' % mode, mode,
                      [(20, v) for v in vals], P + '; any Takeover Mode'))
    C.append(case('MT-14', 'Relative clamp at max and min', 'LinearBinaryOffset', [(20, 127), (20, 127), (20, 127), (20, 0), (20, 0), (20, 0), (20, 0), (20, 0)], P + '; any Takeover Mode'))
    Q = 'quantized parameter (is_quantized true), min 0, max 3, value 1; Takeover Mode None; no prior CC 20'
    C.append(case('MT-15', 'Quantized absolute: round half away from zero', 'Absolute', [(20, 21), (20, 22), (20, 63), (20, 64), (20, 127)], Q, lo=0, hi=3, quant=True, value=1))
    C.append(case('MT-16', 'Quantized relative: one step per message, sign only', 'LinearSignedBit', [(20, 5), (20, 1), (20, 65), (20, 70), (20, 70), (20, 70)], Q, lo=0, hi=3, quant=True, value=1))
    Bp = 'on/off parameter with MidiCCOnOffThresholds Min 64 Max 127, value off (0)'
    C.append(case('MT-17', 'On/off absolute: on inside the threshold interval', 'Absolute', [(20, 63), (20, 64), (20, 127), (20, 0)], Bp, kind='bool', lo=0, hi=1, value=0))
    C.append(case('MT-18', 'On/off relative: on for a positive delta, off otherwise', 'LinearSignedBit', [(20, 1), (20, 65), (20, 3)], Bp, kind='bool', lo=0, hi=1, value=0))
    C.append(case('MT-19', 'Takeover Pick-Up: no move until the controller passes the value', 'Absolute', [(20, 10), (20, 11), (20, 12), (20, 63), (20, 70)], P + '; Takeover Mode Pick-Up', tm=PICKUP))
    C.append(case('MT-20', 'Takeover Value Scaling: proportional approach', 'Absolute', [(20, 10), (20, 20), (20, 30)], P + '; Takeover Mode Value Scaling', tm=SCALING))
    C.append(case('MT-21', 'Takeover enabled: first message with unknown prior leaves the value', 'Absolute', [(20, 100)], P + '; Takeover Mode Pick-Up', tm=PICKUP))
    C.append(case('MT-22', 'Avoid-takeover control (crossfader): jumps despite Pick-Up', 'Absolute', [(20, 10), (20, 100)], 'crossfader-like mapping with takeover disabled by the script; continuous parameter min 0.0 max 1.0 value 0.5; Takeover Mode Pick-Up', avoid=True, tm=PICKUP))
    C.append(case('MT-23', 'Relative modes ignore takeover', 'LinearSignedBit', [(20, 1)], P + '; Takeover Mode Pick-Up', tm=PICKUP))
    return C

def selfcheck(C):
    by = {c['id']: c['expected_after_each_message'] for c in C}
    assert by['MT-01'] == [0.0, round(64 / 127, 6), 1.0]
    assert by['MT-02'] == [0.5, round(12850 / 16383, 6)] and by['MT-03'] == by['MT-02']
    assert by['MT-04'][-1] == by['MT-04'][-2] == round(12850 / 16383, 6)
    assert by['MT-06'] == [round(0.5 + 1 / 256, 6), 0.5, 0.75, round(0.75 - 63 / 256, 6)]
    assert by['MT-15'] == [0.0, 1.0, 1.0, 2.0, 3.0] and by['MT-16'] == [2.0, 3.0, 2.0, 1.0, 0.0, 0.0]
    assert by['MT-17'] == [0.0, 1.0, 1.0, 0.0] and by['MT-21'] == [0.5]
    assert by['MT-19'][:3] == [0.5] * 3 and by['MT-19'][3] == round(63 / 127, 6) and by['MT-19'][4] == round(70 / 127, 6)
    assert abs(by['MT-20'][1] - (0.5 + 0.5 * (10 / 127) / (1 - 10 / 127))) < 1e-6
    assert by['MT-22'] == [round(10 / 127, 6), round(100 / 127, 6)]

if __name__ == '__main__':
    C = build(); selfcheck(C)
    json.dump({'schema': 'n7-acceptance-cases-v1', 'target': 'Ableton Live 12 Suite 12.4.3 arm64',
               'note': 'static derivations from native disassembly; no reference or candidate run', 'cases': C},
              open(sys.argv[1], 'w'), indent=1)
    print(len(C), 'cases')
