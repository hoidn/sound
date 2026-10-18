"""X1 pilot: run original x86_64 Live 12.4.3 functions on released expectations (ADR 0003, label X).

usage: python3 -I -B run_pilot.py            (from any directory; writes next to this file)

Inputs: the x86_64 slice (tools/xexec/xexec.py SLICE), handoff/{mixer-values-v1,midi-config-v3,
transport-state-v1}/cases.json and the spec examples quoted in EXAMPLES below.
Outputs: results/*.json (per case), raw/runs.jsonl (every subprocess), imports.txt, addresses.json.
Every call runs in its own xexec process; see tools/xexec/xexec.c for the bound imports.
"""
import bisect
import ctypes
import json
import math
import re
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
from xexec import Runner, SLICE, as_f32, as_f64, dbl, f32, flt, ustr  # noqa: E402

# ---- x86_64 addresses (image VAs; matching evidence in addresses.json) --------------------
INIT_EMPTY_STRING = 0x1014206e0   # nifty-counter init of the shared empty Live string
MAKE_DB_HOLDER = 0x1024fb0b0      # (slot*, int*, u8*, u8*, int*) as ATrackDevice ctor 0x10284e830 calls it
GAIN_TEXT = 0x1022736b0           # (sret, holder, double gain): log10f*20 then formatter slot +0x28
DB_TEXT = 0x101431530             # formatter slot +0x28: (sret, formatter, double dB)
PAN_TEXT = 0x101433f60            # (sret, double pan)
MIDI_TU_INIT = 0x101bc1360        # static initializer of the MIDI-mapping unit (accel tables)
MIDI_VALUE = 0x101bb27b0          # (float cur, {float min,max}, data*, bool quantized, bool reversed) -> float
PAIR_MSB = 0x101bbc830            # 14-bit receiver: (this, float msb, float prior)
PAIR_LSB = 0x101bbc980            # 14-bit receiver: (this, float lsb, float prior)
PAIR_APPLY = 0x101bbc9c0          # Apply(owner+0xa0, mapping, data*, flags*): skipped under gdb, data printed
FLOAT_WRITER = 0x10142b6c0        # (sret, double x): writer text, P = 9
DOUBLE_WRITER = 0x10142b980       # (sret, double x): writer text, P = 17
INT_PARSE = 0x100375650           # (const char*, size_t) -> bit 32 accepted, low 32 bits the value

# How each x86_64 function was matched to its arm64 counterpart (arm64 addresses from the cited research pages).
MATCHES = [
    {'x86': INIT_EMPTY_STRING, 'role': 'shared empty Live string (nifty counter: count, allocate 8, make empty)',
     'arm64': None, 'how': 'writer of the global read by the string-assign helper 0x1011a7c70 (decompiled corpus); setup only'},
    {'x86': 0x10142c000, 'arm64': 0x101431c6c, 'role': 'number to Live string with %*.*f, zero test, trailing-zero trim',
     'how': 'only x86 reference to the string "%*.*f" (0x1060f506b); arm64 sole reference 0x105b8f310'},
    {'x86': PAN_TEXT, 'arm64': 0x10143a290, 'role': 'pan text', 'how': 'same position (25th) among callers of the '
     'int-format wrapper 0x10142bfd0 (arm64 0x101431c60) in the formatter cluster; constants -0.01, 0.01, -50, 50; '
     'strings "C", "L", "R"'},
    {'x86': DB_TEXT, 'arm64': 0x101437334, 'role': 'dB formatter slot +0x28', 'how': 'calls 0x10142c000; "-inf", " dB"; '
     'constant 0.3, fields +0x18..+0x2a as the arm64 ctor 0x1014371e0 stores them; vtable 0x106bb33b8 slot +0x28'},
    {'x86': 0x101431380, 'arm64': 0x1014371e0, 'role': 'dB formatter ctor (twin 0x1014313f0)',
     'how': 'stores vtable 0x106bb33b8 and the same fields'},
    {'x86': 0x1022735b0, 'arm64': 0x102183abc, 'role': 'gain-text holder ctor', 'how': 'only caller pattern '
     '(-70.0 at 0x105ddca88, formatter ctor 0x1014313f0); holder vtable 0x106cb8ce8'},
    {'x86': MAKE_DB_HOLDER, 'arm64': 0x1023e06fc, 'role': 'make holder (allocate 0x20, ctor via 0x1022736a0)',
     'how': 'ATrackDevice ctor 0x10284e830 (arm64 0x10271b660) calls it under a guard with (3, 1, 1, 1) right '
     'before "Track Volume"'},
    {'x86': GAIN_TEXT, 'arm64': 0x102183bf4, 'role': 'gain to text', 'how': 'holder vtable slot +0x28; log10f, x 20.0f, '
     'slot +0x28 of the formatter; -140.0 for gain <= 0'},
    {'x86': MIDI_VALUE, 'arm64': 0x101b76bf0, 'role': 'map-mode value function', 'how': 'mode test 0 or 5 '
     '(7.00649e-45), guarded 127 from 0x1011899c0 (arm64 0x1011afc2c), calls the decoder, 1/256 step'},
    {'x86': 0x101bb7ff0, 'arm64': 0x101b7b96c, 'role': 'relative delta decoder', 'how': 'same switch over modes 1-9, '
     'vector tables, defaults 20 and 50'},
    {'x86': MIDI_TU_INIT, 'arm64': None, 'role': 'static initializer (mod_init_func index 728) filling accel tables '
     'B (8) and A (9) at 0x107443db8 / 0x107443dd0', 'how': 'only writer of the tables the decoder reads; values equal '
     'arm64 tables 0x10584a580 / 0x10584a5a0 + 50 (n7 native-constants.json)'},
    {'x86': PAIR_MSB, 'arm64': 0x101b8028c, 'role': '14-bit MSB setter', 'how': 'stores +0x34/+0x3c, FLT_MAX tests, '
     'jumps to the combiner'},
    {'x86': PAIR_LSB, 'arm64': 0x101b802bc, 'role': '14-bit LSB setter', 'how': 'stores +0x38/+0x40, as above'},
    {'x86': 0x101bbc870, 'arm64': 0x101b7fcc0, 'role': '14-bit combiner', 'how': '(MSB<<7|LSB)/129.0f, data '
     '{v, prior, mode 0, 1.0f}, calls Apply, resets halves to FLT_MAX'},
    {'x86': PAIR_APPLY, 'arm64': 0x101b7fde4, 'role': 'Apply (skipped under gdb)', 'how': 'called by the combiner; '
     'calls the value function'},
    {'x86': FLOAT_WRITER, 'arm64': 0x101431584, 'role': 'writer text, P = 9', 'how': 'x86 references to "%.*lf" '
     '(0x1060f5424) are exactly these two; constants 9/8 here, 17/16 in the other'},
    {'x86': DOUBLE_WRITER, 'arm64': 0x101431788, 'role': 'writer text, P = 17', 'how': 'as above'},
    {'x86': INT_PARSE, 'arm64': 0x1002fd908, 'role': 'Int attribute text parse', 'how': 'decompiled shape (space '
     'trim, "+", < 0x40, "+-", ASCII test, from_chars 0x100375790 = arm64 0x1002fda78) and "string_view::substr"; '
     '7 callers in both slices'},
]

MODES = {'Absolute': 0, 'AccelSignedBit': 1, 'AccelBinaryOffset': 2, 'AccelTwoCompliment': 3,
         'AccelSignedBit2': 4, 'Absolute14Bit': 5, 'LinearSignedBit': 6, 'LinearBinaryOffset': 7,
         'LinearTwoCompliment': 8, 'LinearSignedBit2': 9}
FLT_MAX = 3.4028234663852886e38

# Spec examples quoted from the released spec texts (REQ-MIXER-VALUES-006/007, REQ-TRANSPORT-STATE-011).
EXAMPLES = {
    'db': [(1, '0.0 dB'), (0.5011872053, '-6.0 dB'), (0.5, '-6.021 dB'), (0.25, '-12.041 dB'),
           (0.30725, '-10.25 dB'), (0.7367056608, '-2.654 dB'), (1.5, '3.522 dB'), (1.99526238, '6.0 dB'),
           (0.99999, '0.0 dB'), (0.0003311311302, '-69.6 dB'), (0.0003235936455, '-inf dB'),
           (0.0003162277571, '-inf dB')],
    'pan': [(-1, '50L'), (-0.6, '30L'), (-0.5, '25L'), (0.2, '10R'), (0.5, '25R'), (1, '50R'),
            (0.004999999888, 'C'), (0.01, 'C'), (0.0101, '1R'), (-0.0101, '1L'), (0.33, '17R')],
    'writer': [('float', 120.0, '120'), ('double', 8.0, '8'), ('double', 4.5, '4.5'),
               ('float', 121.2, '121.199997'), ('float', 93.3333333, '93.3333359'),
               ('double', 0.3, '0.299999999999999989'), ('double', 3.3, '3.2999999999999998'),
               ('double', 0.0, '0')],
    # REQ-TRANSPORT-STATE-006: accepted texts with their code, refused texts with None
    'int': [('201', 201), (' 201', 201), ('+201', 201), (' +201', 201), ('201 ', 201),
            ('', None), ('   ', None), ('201\u00e9', None), ('+-201', None), ('201.0', None), ('2e2', None),
            ('0x10', None), ('abc', None), ('0' * 61 + '201', None)],
}
# Inputs the released specs exclude or leave open; X reports what the original code gives.
PROBES = {
    'pan': [-0.75, -0.25, 0.25, 0.75],
    'db_text': [-69.69999694824219, -69.70000457763672],   # binary32 neighbours of -69.7 (formatter alone)
    # binary64 values next to powers of ten: REQ-TRANSPORT-STATE-011 with exact log10 versus X
    'writer': [('double', 10.000000000000002), ('double', 1000.0000000000001), ('double', 1000000.0000000001),
               ('double', 0.09999999999999999), ('double', 0.009999999999999998), ('double', 0.9999999999999999),
               ('float', 100.00000762939453), ('float', 0.09999999403953552), ('double', -0.0), ('float', -0.0)],
    'int': ['0' * 60 + '201', ' 201 ', '+201 ', '-201', '- 201', '+', '-', '2147483648', '4294967497'],
}

R = Runner()
libm = ctypes.CDLL('libm.so.6')
libm.log10f.restype, libm.log10f.argtypes = ctypes.c_float, [ctypes.c_float]


def live_string(res, k):
    """Text of the Live string whose block pointer is in buffer k (the run must dump b{k}*+16)."""
    for expr, _, data in res.dumps:
        if expr == f'b{k}*+16':
            return ustr(data)
    raise RuntimeError(f'no dump of b{k}: trap={res.trap} fault={res.fault} rc={res.rc}\n{res.stderr}')


def run_text(tokens, k):
    res = R.run(tokens + ['dump', f'b{k}*+16', f'b{k}*+4@'])
    if not res.ok:
        return None, res
    return live_string(res, k), res


DB_SETUP = ['call', hex(INIT_EMPTY_STRING),
            'call', hex(MAKE_DB_HOLDER), 'buf:8', 'hex:03000000', 'hex:01', 'hex:01', 'hex:01000000']


def gain_text(g):
    return run_text(DB_SETUP + ['call', hex(GAIN_TEXT), 'buf:8', 'ref:b0*', dbl(f32(g))], 5)[0]


def db_text(db):
    """Formatter slot alone, for the log10f sensitivity check (formatter = holder +0x18)."""
    return run_text(DB_SETUP + ['call', hex(DB_TEXT), 'buf:8', 'ref:b0*+24*', dbl(db)], 5)[0]


def pan_text(p):
    return run_text(['call', hex(INIT_EMPTY_STRING), 'call', hex(PAN_TEXT), 'buf:8', dbl(f32(p))], 0)[0]


def writer_text(kind, x):
    v = f32(x) if kind == 'float' else float(x)
    fn = FLOAT_WRITER if kind == 'float' else DOUBLE_WRITER
    return run_text(['call', hex(INIT_EMPTY_STRING), 'call', hex(fn), 'buf:8', dbl(v)], 0)[0]


def cr_log10f(g):
    """Correctly rounded binary32 log10 of binary32 g (Decimal, 60 digits)."""
    getcontext().prec = 60
    exact = Decimal(g).log10()
    c = f32(float(exact))
    return min([c] + ulp_neighbours(c), key=lambda y: abs(Decimal(y) - exact))


def ulp_neighbours(x):
    """The binary32 numbers just below and just above binary32 x (finite x)."""
    def key(y):                       # monotone integer key of a binary32 value
        i = struct.unpack('<i', struct.pack('<f', y))[0]
        return i if i >= 0 else -(i & 0x7fffffff)
    def unkey(k):
        return struct.unpack('<f', struct.pack('<i', k if k >= 0 else (-k) | -0x80000000))[0]
    return [unkey(key(x) - 1), unkey(key(x) + 1)]


# ---- target 1: mixer value text -------------------------------------------------------------
def mixer():
    cases = json.load(open(ROOT / 'handoff/mixer-values-v1/cases.json'))['cases']
    memo, out = {}, []
    for c in cases:
        checks = []
        for key, exp in c['expected'].get('values', {}).items():
            elem = key.split('/')[1]
            if 'text' not in exp or elem == 'Speaker':
                continue
            kind = 'db' if elem in ('Volume', 'Send') else 'pan'
            if (kind, exp['value']) not in memo:
                memo[kind, exp['value']] = gain_text(exp['value']) if kind == 'db' else pan_text(exp['value'])
            got = memo[kind, exp['value']]
            checks.append({'key': key, 'value': exp['value'], 'expected': exp['text'], 'x': got,
                           'agree': got == exp['text']})
        out.append({'case': c['id'], 'checks': checks, 'agree': sum(x['agree'] for x in checks), 'n': len(checks)})
    examples = []
    for g, t in EXAMPLES['db']:
        examples.append({'kind': 'db', 'input': g, 'expected': t, 'x': gain_text(g)})
    for p, t in EXAMPLES['pan']:
        examples.append({'kind': 'pan', 'input': p, 'expected': t, 'x': pan_text(p)})
    for e in examples:
        e['agree'] = e['x'] == e['expected']
    # log10f substitution: glibc vs correctly rounded, and the text at L - 1 ulp and L + 1 ulp
    sens = []
    for kind, v in sorted(k for k in memo if k[0] == 'db'):
        if v <= 0:
            continue
        L = libm.log10f(v)
        texts = {str(l): db_text(float(f32(l * 20.0))) for l in [L] + ulp_neighbours(L)}
        sens.append({'gain': v, 'glibc_log10f': L, 'correctly_rounded': cr_log10f(v),
                     'glibc_is_cr': L == cr_log10f(v), 'texts_by_L': texts,
                     'stable_within_1ulp': len(set(texts.values())) == 1})
    probes = [{'kind': 'pan', 'input': p, 'x': pan_text(p)} for p in PROBES['pan']]
    probes += [{'kind': 'db_text', 'input': d, 'x': db_text(d)} for d in PROBES['db_text']]
    return {'cases': out, 'examples': examples, 'log10f_sensitivity': sens, 'probes': probes}


# ---- target 2: MIDI map-mode value function -------------------------------------------------
def midi_value(cur, lo, hi, v, mode, quantized):
    data = struct.pack('<ffif', v, FLT_MAX, mode, 1.0).hex()
    rng = as_f64(struct.unpack('<Q', struct.pack('<ff', lo, hi))[0])
    res = R.run(['call', hex(MIDI_TU_INIT), 'call', hex(MIDI_VALUE), flt(cur), dbl(rng),
                 'hex:' + data, f'i:{int(quantized)}', 'i:0'])
    return as_f32(res.calls[-1]['xmm0']) if res.ok else None


def pair_harness(messages):
    """Absolute14Bit pairing as the released spec states it (harness logic, not X): yields the data
    value pair/129 (binary32, as the x86 combiner 0x101bbc870 divides) or None for no new value."""
    msb = lsb = None
    for m in messages:
        _, n, v = (int(x, 16) for x in m.split())
        if n == 20:
            msb = v
        else:
            lsb = v
        if msb is not None and lsb is not None:
            yield f32(f32(float(msb << 7 | lsb)) / f32(129.0))
            msb = lsb = None
        else:
            yield None


def pair_x(messages):
    """Absolute14Bit pairing executed by the original receiver setters and combiner (X). Apply is
    skipped under gdb; the data it receives is recorded. Receiver state: no half held (FLT_MAX
    sentinels at +0x34..+0x40), owner pointer = image base (only read, then passed to the skipped Apply).
    Prior = the input's last value for that controller, -129 before any (per 0x101b65b68)."""
    rec = bytearray(0x48)
    struct.pack_into('<Q', rec, 8, 0x100000000)
    struct.pack_into('<ffff', rec, 0x34, FLT_MAX, FLT_MAX, FLT_MAX, FLT_MAX)
    toks, last = ['call', hex(MIDI_TU_INIT)], {}
    for i, m in enumerate(messages):
        _, n, v = (int(x, 16) for x in m.split())
        toks += ['call', hex(PAIR_MSB if n == 20 else PAIR_LSB), 'hex:' + rec.hex() if i == 0 else 'ref:b0',
                 flt(v), flt(last.get(n, -129))]
        last[n] = v
    rdx = '(unsigned int*)$rdx'
    res = R.run(toks, skip={PAIR_APPLY: [f'*{rdx}', f'*({rdx}+1)', f'*({rdx}+2)', f'*({rdx}+3)']})
    if not res.ok:
        raise RuntimeError(f'14-bit run failed: {res.trap} {res.fault} {res.stderr[-500:]}')
    applied = {k - 1: vals for k, _, vals in res.hits}       # call index k-1 = message index (call 0 is init)
    return [None if i not in applied else
            {'v': as_f32(applied[i][0]), 'prior': as_f32(applied[i][1]), 'mode': applied[i][2],
             'sensitivity': as_f32(applied[i][3])} for i in range(len(messages))]


def midi():
    cases = json.load(open(ROOT / 'handoff/midi-config-v3/cases.json'))['cases']
    out = []
    for c in cases:
        if 'stimulus' not in c:
            continue
        st, prm = c['stimulus'], c['stimulus']['parameter']
        mode_name = next(a['map_mode'] for a in c['expected']['assignments'] if a['number'] == 20)
        mode = MODES[mode_name]
        cur, lo, hi, q = f32(prm['initial_value']), f32(prm['min']), f32(prm['max']), prm['stepped']
        pairing = None
        if mode == 5:
            px = pair_x(st['messages'])
            spec = list(pair_harness(st['messages']))
            pairing = {'x_applied': px, 'spec_rule_v': spec,
                       'agree': [(a is None and b is None) or (a is not None and a['v'] == b) for a, b in zip(px, spec)]}
            inputs = [None if a is None else a['v'] for a in px]
            mode = px[[a is not None for a in px].index(True)]['mode']   # the combiner's own mode (0)
        else:
            inputs = [float(int(m.split()[2], 16)) for m in st['messages']]
        got = []
        for v in inputs:
            if v is not None:
                cur = midi_value(cur, lo, hi, v, mode, q)
            got.append(cur)
        exp = c['expected']['values']
        agree = [g is not None and abs(g - e) <= 1e-6 for g, e in zip(got, exp)]
        out.append({'case': c['id'], 'mode': mode_name, 'stepped': q, 'messages': st['messages'],
                    'expected': exp, 'x': got, 'agree_each': agree, 'n': 1,
                    'agree': int(all(agree) and len(got) == len(exp)),
                    'pairing': pairing,
                    'x_scope': 'value function' if mode_name != 'Absolute14Bit'
                    else 'receiver setters + combiner (Apply skipped under gdb), then value function'})
    # control: without the unit's static initializer the accel tables are empty (default 20 / 50)
    control = {'what': 'AccelSignedBit v=1 from 0.5 without 0x101bc1360',
               'with_init': midi_value(0.5, 0.0, 1.0, 1.0, 1, False)}
    res = R.run(['call', hex(MIDI_VALUE), flt(0.5), dbl(as_f64(struct.unpack('<Q', struct.pack('<ff', 0, 1))[0])),
                 'hex:' + struct.pack('<ffif', 1.0, FLT_MAX, 1, 1.0).hex(), 'i:0', 'i:0'])
    control['without_init'] = as_f32(res.calls[-1]['xmm0']) if res.ok else (res.trap or res.fault)
    return {'cases': out, 'control': control, 'fma_check': [fma_check(-1.0, 1.0), fma_check(20.0, 999.0)]}


def r32(q):
    """Binary32 nearest to the rational q, ties to even."""
    c = f32(float(q))
    cands = sorted(set([c] + ulp_neighbours(c)), key=lambda y: (abs(Fraction(y) - q),
                   struct.unpack('<I', struct.pack('<f', y))[0] & 1))
    return cands[0]


def fma_check(lo, hi):
    """Absolute mode with min != 0: the x86 code rounds max*t and min*(1-t) separately; arm64 0x101b76c60
    fuses max*t + s1 (fmadd). Models in exact rationals; the x86 model is checked against X for all 128 v."""
    F = Fraction
    rows = []
    for v in range(128):
        t = r32(F(v) / 127)
        s1 = r32(F(lo) * r32(1 - F(t)))
        x86 = r32(F(r32(F(hi) * F(t))) + F(s1))
        arm = r32(F(hi) * F(t) + F(s1))
        rows.append((v, x86, arm, midi_value(lo, lo, hi, float(v), 0, False)))
    diff = [{'v': r[0], 'x': r[3], 'arm64_model': r[2]} for r in rows if r[2] != r[3]]
    return {'min': lo, 'max': hi, 'x86_model_equals_x': sum(r[1] == r[3] for r in rows), 'n': len(rows),
            'arm64_fma_model_differs_from_x': diff,
            'max_abs_difference': max([abs(d['x'] - d['arm64_model']) for d in diff], default=0.0)}


# ---- target 3: transport-state number text on save ------------------------------------------
TS_PATHS = {'Transport/LoopStart': 'double', 'Transport/LoopLength': 'double', 'Transport/CurrentTime': 'double',
            'MainTrack/DeviceChain/Mixer/Tempo/Manual': 'float'}


def transport():
    cases = json.load(open(ROOT / 'handoff/transport-state-v1/cases.json'))['cases']
    out = []
    # value written = value read; the state comes from the case or, for save-only cases, from the fixture text
    for c in cases:
        saved = c['expected'].get('saved', {}).get('values', {})
        checks = []
        for path, text in saved.items():
            if path not in TS_PATHS:
                continue
            kind = TS_PATHS[path]
            src = fixture_value(c, path)
            got = writer_text(kind, src)
            checks.append({'path': path, 'kind': kind, 'value_read': f32(src) if kind == 'float' else src,
                           'expected': text, 'x': got, 'agree': got == text})
        if checks:
            out.append({'case': c['id'], 'checks': checks, 'agree': sum(x['agree'] for x in checks), 'n': len(checks)})
    examples = [{'kind': k, 'input': x, 'expected': t, 'x': writer_text(k, x)} for k, x, t in EXAMPLES['writer']]
    for e in examples:
        e['agree'] = e['x'] == e['expected']
    icase, iex = transport_int()
    out.append(icase)
    probes = [{'kind': 'int', 'input': t, 'x': int_parse(t)} for t in PROBES['int']]
    probes += [{'kind': f'writer-{k}', 'input': x, 'x': writer_text(k, x), 'spec_rule_exact_log10': writer_rule_exact(k, x)}
               for k, x in PROBES['writer']]
    for e in examples:
        if e['kind'] in ('float', 'double'):
            e['spec_rule_exact_log10'] = writer_rule_exact(e['kind'], e['input'])
    return {'cases': out, 'examples': examples + iex, 'probes': probes}


def writer_rule_exact(kind, x):
    """REQ-TRANSPORT-STATE-011 read literally: k from the exact log10 (Decimal, 80 digits)."""
    getcontext().prec = 80
    x = f32(x) if kind == 'float' else x
    if x == 0:
        return '0' if math.copysign(1, x) > 0 else 'undefined (log10 of 0)'
    d = Decimal(x)
    lg = abs(d).log10()
    k = math.ceil(lg) if abs(d) >= 1 else math.floor(lg)
    t = format(d, f'.{max(0, (9 if kind == "float" else 17) - k)}f')
    return t.rstrip('0').rstrip('.') if '.' in t else t


def int_parse(text):
    raw = text.encode('utf-8')
    res = R.run(['call', hex(INT_PARSE), 'hex:' + raw.hex() if raw else 'buf:1', f'i:{len(raw)}'])
    rax = res.calls[-1]['rax']
    return (struct.unpack('<i', struct.pack('<I', rax & 0xffffffff))[0]) if rax >> 32 & 1 else None


def transport_int():
    cases = json.load(open(ROOT / 'handoff/transport-state-v1/cases.json'))['cases']
    c = next(c for c in cases if c['id'] == 'TS-009')
    text = ET.parse(ROOT / 'handoff/transport-state-v1' / c['input']).getroot().find(
        'LiveSet/MainTrack/DeviceChain/Mixer/TimeSignature/Manual').get('Value')
    got = int_parse(text)
    case = {'case': 'TS-009', 'checks': [{'path': 'TimeSignature/Manual', 'text': text, 'expected': 'refused',
                                          'x': 'refused' if got is None else got, 'agree': got is None}],
            'n': 1, 'agree': int(got is None)}
    ex = [{'kind': 'int', 'input': t, 'expected': e, 'x': int_parse(t)} for t, e in EXAMPLES['int']]
    for e in ex:
        e['agree'] = e['x'] == e['expected']
    return case, ex


def fixture_value(case, path):
    """Value the case's fixture stores at path, read with Python float() (REQ-004 prefix rule for the
    texts involved: they are plain decimals except TS-006, whose prefix is taken as the spec says)."""
    root = ET.parse(ROOT / 'handoff/transport-state-v1' / case['input']).getroot()
    el = root.find('LiveSet/' + path) if root.tag != 'LiveSet' else root.find(path)
    text = el.get('Value')
    return float(re.match(r' *[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?', text).group(0))


def function_starts(path):
    """Function start VAs from LC_FUNCTION_STARTS (ULEB deltas from the image base)."""
    data = open(path, 'rb').read()
    ncmds, off = struct.unpack_from('<I', data, 16)[0], 32
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', data, off)
        if cmd == 0x26:
            fo, fs = struct.unpack_from('<II', data, off + 8)
            starts, addr, p, end = [], 0x100000000, fo, fo + fs
            while p < end and data[p]:
                v = sh = 0
                while True:
                    b = data[p]; p += 1; v |= (b & 0x7f) << sh; sh += 7
                    if not b & 0x80:
                        break
                addr += v
                starts.append(addr)
            return starts
        off += size


def disassemble(path, addrs):
    starts = function_starts(path)
    out = []
    for a in addrs:
        end = starts[bisect.bisect_right(starts, a)]
        out.append(f'### {a:#x} .. {end:#x}\n')
        p = subprocess.run(['objdump', '-D', '-b', 'binary', '-m', 'i386:x86-64', '--adjust-vma=0x100000000',
                            f'--start-address={a:#x}', f'--stop-address={end:#x}', path],
                           capture_output=True, text=True, check=True)
        out.append(p.stdout.split('<.data+', 1)[-1].split('\n', 1)[-1])
    return ''.join(out)


def main():
    results = {}
    for name, fn in (('mixer', mixer), ('midi', midi), ('transport', transport)):
        first = len(R.log)
        results[name] = fn()
        used = {}
        for _, res in R.log[first:]:
            for sym, n in res.used.items():
                used[sym] = used.get(sym, 0) + n
        results[name]['replaced_imports_called'] = dict(sorted(used.items()))
        results[name]['runs'] = {'count': len(R.log) - first,
                                 'not_ok': sum(not r.ok for _, r in R.log[first:])}
    (HERE / 'results').mkdir(exist_ok=True)
    for k, v in results.items():
        (HERE / 'results' / f'{k}.json').write_text(json.dumps(v, indent=1) + '\n')
    (HERE / 'raw').mkdir(exist_ok=True)
    with open(HERE / 'raw' / 'runs.jsonl', 'w') as f:
        for argv, res in R.log:
            f.write(json.dumps({'argv': argv, 'rc': res.rc, 'stdout': res.stdout, 'stderr': res.stderr,
                                'timeout': res.timeout}) + '\n')
    (HERE / 'addresses.json').write_text(json.dumps(
        {'slice': SLICE, 'image_base': '0x100000000',
         'functions': [{**m, 'x86': hex(m['x86']), 'arm64': m['arm64'] and hex(m['arm64'])} for m in MATCHES]},
        indent=1) + '\n')
    (HERE / 'x86-disasm.txt').write_text(disassemble(SLICE, [m['x86'] for m in MATCHES]))
    imp = R.run(['--imports'])
    (HERE / 'imports.txt').write_text(imp.stdout)
    for k, v in results.items():
        cs = v['cases']
        n, a = sum(c['n'] for c in cs), sum(c['agree'] for c in cs)
        ex = v.get('examples', [])
        print(f"{k}: {len(cs)} cases, {a}/{n} checks agree; spec examples {sum(e['agree'] for e in ex)}/{len(ex)}")
    for k, v in results.items():
        for p in v.get('probes', []):
            extra = f"  (spec rule, exact log10: {p['spec_rule_exact_log10']!r})" if 'spec_rule_exact_log10' in p else ''
            print(f"probe {p['kind']} {p['input']!r} -> {p['x']!r}{extra}")
    print('control', results['midi']['control'])
    for fc in results['midi']['fma_check']:
        print(f"fma: x86 model = X for {fc['x86_model_equals_x']}/{fc['n']}; arm64 fmadd model differs for "
              f"{len(fc['arm64_fma_model_differs_from_x'])} data values (min {fc['min']}, max {fc['max']}, "
              f"max |diff| {fc['max_abs_difference']})")
    for k, v in results.items():
        print(f"{k}: runs {v['runs']}; replaced imports called: {', '.join(v['replaced_imports_called'])}")
    s = results['mixer']['log10f_sensitivity']
    print(f"log10f: glibc correctly rounded for {sum(x['glibc_is_cr'] for x in s)}/{len(s)} gains; "
          f"text stable within 1 ulp for {sum(x['stable_within_1ulp'] for x in s)}/{len(s)}")


if __name__ == '__main__':
    assert ulp_neighbours(1.0) == [0.9999999403953552, 1.0000001192092896]
    assert ulp_neighbours(0.0)[1] == 1.401298464324817e-45 and ulp_neighbours(-1.0)[1] == -0.9999999403953552
    main()
