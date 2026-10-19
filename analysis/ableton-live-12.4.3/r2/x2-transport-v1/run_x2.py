"""X2 transport state: run original x86_64 Live 12.4.3 functions on discriminating inputs (ADR 0003, label X).

usage: python3 -I -B run_x2.py            (from any directory; writes next to this file)

Targets (SPEC-TRANSPORT-STATE r2): (a) REQ-011 k near powers of ten, (b) negative zero on save,
(c) REQ-006 integer text and the REQ-004/005 number text, (d) REQ-010 meter codes and list texts.
Inputs are defined in this file. Outputs: results/{writer,parse,meter}.json, raw/runs.jsonl (every
subprocess), addresses.json, imports.txt, x86-disasm.txt, summary.txt.
Loader: the X2 copy xexec.c / xexec.py in this directory (tools/xexec plus _strtod, mk and ptrs:).
Each process loads the slice afresh; several calls may share one process (batched pure calls).
"""
import bisect
import json
import math
import struct
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal, getcontext
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from xexec import Runner, SLICE, dbl, f32, flt  # noqa: E402  (X2 copy)
import lookup  # noqa: E402  (corpus locators for addresses.json; read-only)

# ---- x86_64 addresses (image VAs); matching evidence in MATCHES / addresses.json --------------------
INIT_EMPTY_STRING = 0x1014206e0   # shared empty Live string (X1)
FMT9, FMT17 = 0x10142b6c0, 0x10142b980          # (sret, double x): number text, P = 9 / 17 (X1)
WRITE_F32, WRITE_F64 = 0x10150f6a0, 0x10150f7a0  # (float|double x, stream*): attribute value writers
CONVERT = 0x10151b630             # (node*, {char *p; int n}*): attribute text -> typed value
INT_PARSE = 0x100375650           # (const char*, size_t) -> bit 32 accepted, low 32 bits the value (X1)
TS_ENCODE = 0x101ae7a40           # ({int n; int d}*) -> code or INT_MIN
TS_DECODE = 0x101ae7a00           # (int code) -> n | d << 32, or INT_MIN | INT_MIN << 32
TS_LIST = 0x102812bf0             # () -> &vector of 495 Live strings (globals below)
TS_LIST_BEGIN = 0x10749eb10       # vector begin / end / capacity
# Converter setup. The node's vtable slot +0x28 must return a pointer to the base-type id (the converter
# reads it with 0x1011ec760 = `return *p`). VT is an address in __DATA_CONST whose qword at +0x28 is
# 0x103c2c670 = `push rbp; mov rbp,rsp; mov rax,[rdi+8]; pop rbp; ret`, so a node {VT, &id} works with
# no code stubbed. SetValue<T> is reached through these __stubs (tail jumps); gdb stops there, prints
# the value register and returns, so the node's value holder is never needed.
VT = 0x106a4b178
SET_BOOL, SET_DOUBLE, SET_FLOAT, SET_INT = 0x105a4d446, 0x105a4d44c, 0x105a4d452, 0x105a4d458
TYPE_IDS = {'bool': 0x10, 'int': 0x11, 'float': 0x12, 'double': 0x17}
# Writer setup: a stream object {&fake_vtable}; slot +0x30 receives a Live string, +0x38 a C string.
# The two slot targets are unrelated function entries; gdb stops at them before they run.
SLOT30, SLOT38 = 0x103c3e940, 0x103caf380

MATCHES = [
    {'x86': INIT_EMPTY_STRING, 'arm64': None, 'role': 'shared empty Live string (setup only)', 'how': 'X1'},
    {'x86': FMT9, 'arm64': 0x101431584, 'role': 'number text P = 9', 'how': 'X1: one of the two references to "%.*lf"'},
    {'x86': FMT17, 'arm64': 0x101431788, 'role': 'number text P = 17', 'how': 'X1: the other "%.*lf" reference'},
    {'x86': 0x10142b6a0, 'arm64': 0x10143157c, 'role': 'widen float, call P = 9 text', 'how': 'called by the float writer; cvtss2sd / fcvt then the P = 9 function'},
    {'x86': WRITE_F32, 'arm64': 0x101520c70, 'role': 'float attribute value writer',
     'how': 'sole x86 reference to "#%8.8X" (0x106100f1c); arm64 sole reference 0x105b9b2d9; same branches (finite, == FLT_MAX -> "Invalid", else number text)'},
    {'x86': WRITE_F64, 'arm64': 0x101520dbc, 'role': 'double attribute value writer',
     'how': 'sole x86 reference to "#%16.16llX" (0x106100f23); arm64 0x105b9b2e0'},
    {'x86': CONVERT, 'arm64': 0x10152bfb8, 'role': 'attribute text to typed value (bool, int, float, double ...)',
     'how': '5th of the 10 x86 call sites of the int parser 0x100375650 (by address), as 0x10152bfb8 is the 5th arm64 site of 0x1002fd908; same switch on type ids 0x10-0x19, same "true"/"false"/"0", "Invalid", #hex8/#hex16 and strtod structure'},
    {'x86': 0x1011ec760, 'arm64': 0x10120e264, 'role': 'base-type id read (return *p)', 'how': 'callee of the converter right after vtable slot +0x28 in both slices'},
    {'x86': INT_PARSE, 'arm64': 0x1002fd908, 'role': 'Int attribute text parse', 'how': 'X1'},
    {'x86': 0x100375790, 'arm64': 0x1002fda78, 'role': 'from_chars<int>', 'how': 'X1; callee of the parser'},
    {'x86': TS_ENCODE, 'arm64': 0x101abea70, 'role': 'meter (n, d) -> code',
     'how': 'same test n > 0, d - 1 < 16, popcount(d) == 1, result 99 * log2(d) + n - 1, else INT_MIN; called by the time-signature init 0x102829920 (arm64 0x1026f7420) right after the list builder'},
    {'x86': TS_DECODE, 'arm64': 0x101abea38, 'role': 'meter code -> (n, d)',
     'how': 'the x86 and arm64 functions with both "code % 99" and "code / 99" next to the encoder (x86 0x101ae79a0 / 0x101ae79d0 / 0x101ae7a00, arm64 0x101abe9e4 / 0x101abea10 / 0x101abea38); (code % 99 + 1, 1 << (code / 99 & 31)) for code >= 0, else INT_MIN pair'},
    {'x86': TS_LIST, 'arm64': 0x1026e10a8, 'role': '495-entry meter text list (guarded static vector)',
     'how': 'callee of the time-signature init 0x102829920; loops exponent 0..4 by numerator 1..99, entry text from 0x1028127e0 (arm64 0x1026e0c6c): int text, "/", int text'},
    {'x86': 0x1028127e0, 'arm64': 0x1026e0c6c, 'role': 'meter entry text n/d', 'how': 'callee of the list builder; "%d"-based int text joined with "/"'},
]
LIBS = {'log10': 'glibc 2.39 log10 (Apple libm not available)', 'vsnprintf_l': 'glibc vsnprintf under uselocale(C)',
        'strtod': 'glibc 2.39 strtod, process locale C', 'newlocale': 'C locale only'}

R = Runner()
P = {'float': 9, 'double': 17}
I32 = lambda v: struct.unpack('<i', struct.pack('<I', v & 0xffffffff))[0]  # noqa: E731


def bits64(x):
    return struct.unpack('<Q', struct.pack('<d', x))[0]


def from_bits64(b):
    return struct.unpack('<d', struct.pack('<Q', b))[0]


def f32_next(x, j):
    """binary32 value j steps from binary32 x (monotone integer key; finite results only)."""
    i = struct.unpack('<i', struct.pack('<f', x))[0]
    k = i if i >= 0 else -(i & 0x7fffffff)
    k += j
    return struct.unpack('<f', struct.pack('<i', k if k >= 0 else (-k) | -0x80000000))[0]


def live_text(data):
    return data.decode('utf-16-le').rstrip('\0')


def pmap(fn, items, workers=8):
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(fn, items))


# ---- (a) number text: the P = 9 / P = 17 functions, batched --------------------------------------
def formatter_batch(items):
    """items: [(kind, x)]; one process, one call per value; returns the texts in order."""
    toks = ['call', hex(INIT_EMPTY_STRING)]
    for kind, x in items:
        toks += ['call', hex(FMT9 if kind == 'float' else FMT17), 'buf:8', dbl(f32(x) if kind == 'float' else x)]
    for k in range(len(items)):
        toks += ['dump', f'b{k}*+16', f'b{k}*+4@']
    res = R.run(toks)
    if not res.ok:
        raise RuntimeError(f'formatter batch failed: trap={res.trap} fault={res.fault}\n{res.stderr[-500:]}')
    return [live_text(d) for _, _, d in res.dumps]


def chunks(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]


# Models of REQ-011 step 1, compared with X. "exact": k from the exact logarithm (r2 text read literally);
# "cr": k from log10|x| rounded to nearest binary64; "glibc": k from the substituted library's log10.
getcontext().prec = 80


def rule_text(kind, x, how):
    x = f32(x) if kind == 'float' else x
    if x == 0:
        return '-0' if math.copysign(1, x) < 0 else '0'
    a = abs(x)
    if how == 'glibc':
        lg = math.log10(a)
    else:
        lg = Decimal(a).log10()
        if how == 'cr':
            lg = float(lg)
    k = math.ceil(lg) if lg >= 0 else math.floor(lg)
    t = '%.*f' % (max(0, P[kind] - k), x)
    return t.rstrip('0').rstrip('.') if '.' in t else t


def log_offset(x):
    """(n, offset of the exact log10|x| from the nearest integer n in units of the binary64 spacing on
    that side of n, whether glibc log10 is correctly rounded at x)."""
    a = abs(x)
    lg = Decimal(a).log10()
    n = int(lg.to_integral_value())
    if n == 0:
        return 0, None, float(lg) == math.log10(a)
    side = math.ulp(float(abs(n))) if abs(lg) > abs(n) else float(abs(n)) - math.nextafter(float(abs(n)), 0)
    return n, float(abs(lg - n) / Decimal(side)), float(lg) == math.log10(a)


def sweep_inputs():
    vals = []
    for n in list(range(-30, 23)) + [-307, -300, -200, -100, -50, 50, 100, 200, 300, 308]:
        x0 = float(f'1e{n}')
        for j in range(-40, 41):
            x = x0
            for _ in range(abs(j)):
                x = math.nextafter(x, math.inf if j > 0 else 0.0)
            vals.append(('double', x))
    for n in range(-3, 4):                   # sign symmetry
        x = math.nextafter(float(f'1e{n}'), math.inf)
        vals += [('double', -x), ('double', -math.nextafter(float(f'1e{n}'), 0.0))]
    for n in range(-45, 39):                 # binary32 neighbours of every power of ten in range
        x0 = f32(float(f'1e{n}'))
        if x0 == 0 or math.isinf(x0):
            continue
        vals += [('float', f32_next(x0, j)) for j in range(-8, 9)]
    # exact decimal ties at the printed precision (x86: glibc vsnprintf decides them)
    vals += [('double', 1 + 2 ** -17), ('double', 1e15 + 0.125), ('float', 120.0078125), ('float', 1.001953125),
             ('double', 2.5), ('double', 5e-324), ('float', 1.401298464324817e-45), ('double', 2.2250738585072014e-308)]
    seen, out = set(), []
    for kind, x in vals:
        key = (kind, bits64(x))
        if key not in seen and x != 0 and math.isfinite(x):
            seen.add(key)
            out.append((kind, x))
    return out


def writer_sweep():
    items = sweep_inputs()
    texts = sum(pmap(formatter_batch, chunks(items, 100)), [])
    rows = []
    for (kind, x), t in zip(items, texts):
        n, off, cr = log_offset(f32(x) if kind == 'float' else x)
        rows.append({'kind': kind, 'value': x, 'value_hex': float(x).hex(), 'X': t,
                     'exact': rule_text(kind, x, 'exact'), 'cr': rule_text(kind, x, 'cr'),
                     'glibc': rule_text(kind, x, 'glibc'), 'n': n, 'offset_ulps': off, 'glibc_log10_is_cr': cr})
    return rows


# ---- (a, b) the attribute value writers with a fake stream (gdb stops at the stream's slots) ---------
NQ = 100
WRITER_SKIP = {SLOT30: ['*(unsigned int*)(*(long*)$rsi+4)'] + [f'*(unsigned long*)(*(long*)$rsi+{16 + 8 * i})' for i in range(NQ)],
               SLOT38: [f'*(unsigned long*)($rsi+{8 * i})' for i in range(4)]}


def attr_write(kind, x):
    fn, arg = (WRITE_F64, dbl(x)) if kind == 'double' else (WRITE_F32, flt(x))
    if math.isnan(x):                 # dbl()/flt() drop a NaN's sign; strtod('-nan') keeps it
        arg = arg[:2] + ('-nan' if math.copysign(1, x) < 0 else 'nan')
    res = R.run(['call', hex(INIT_EMPTY_STRING), 'mk', f'ptrs:0,0,0,0,0,0,{SLOT30:#x},{SLOT38:#x}',
                 'call', hex(fn), arg, 'ptrs:b0'], skip=WRITER_SKIP)
    out = []
    for _, addr, vals in res.hits:
        if addr == SLOT30:
            raw = b''.join(struct.pack('<Q', v) for v in vals[1:])
            out.append({'slot': '+0x30 (Live string)', 'text': raw[:vals[0]].decode('utf-16-le').rstrip('\0')})
        else:
            raw = b''.join(struct.pack('<Q', v) for v in vals)
            out.append({'slot': '+0x38 (C string)', 'text': raw.split(b'\0')[0].decode('ascii')})
    return {'kind': kind, 'x': repr(x), 'x_bits': '%016x' % bits64(x) if kind == 'double'
            else '%08x' % struct.unpack('<I', struct.pack('<f', f32(x)))[0],
            'writes': out, 'trap': res.trap, 'fault': res.fault}


FLT_MAX, DBL_MAX = 3.4028234663852886e38, 1.7976931348623157e308
WRITER_SPECIALS = [(k, v) for k in ('double', 'float') for v in (
    0.0, -0.0, DBL_MAX if k == 'double' else FLT_MAX, -(DBL_MAX if k == 'double' else FLT_MAX),
    math.inf, -math.inf, math.nan, -math.nan)]
# Values of the released and proposed save cases, through the whole writer.
WRITER_CASE_VALUES = [('double', 4.5), ('double', 0.3), ('double', 8.0), ('double', 16.0), ('double', 0.0),
                      ('float', 120.0), ('float', 121.2), ('float', 93.3333333),
                      ('double', 100.00000000000001), ('double', 1000.0000000000001),
                      ('double', 0.09999999999999999), ('double', 10.000000000000002), ('double', 3.3),
                      ('double', 0.000001), ('double', -1000.0000000000001), ('double', 1e-14)]


# ---- (b, c) the attribute text converter with a fake node --------------------------------------
CONVERT_SKIP = {SET_BOOL: ['$rsi'], SET_DOUBLE: ['$xmm0.v2_int64[0]'], SET_FLOAT: ['$xmm0.v4_int32[0]'],
                SET_INT: ['$rsi']}


def convert(kind, raw):
    """Run the converter on bytes raw for base type kind. -> ('value', python value, bits) | ('refused', trap)."""
    tid = TYPE_IDS[kind]
    res = R.run(['call', hex(INIT_EMPTY_STRING), 'mk', 'hex:' + struct.pack('<I', tid).hex(),
                 'mk', f'ptrs:{VT:#x},b0', 'mk', 'hex:' + raw.hex() + '00',
                 'call', hex(CONVERT), 'ref:b1', f'ptrs:b2,{len(raw)}'], skip=CONVERT_SKIP)
    rec = {'kind': kind, 'text': raw.decode('latin-1'), 'bytes': raw.hex(), 'used': res.used}
    if res.hits:
        _, addr, (v,) = res.hits[0]
        if addr == SET_INT:
            rec.update(result='value', value=I32(v), via='SetValue<int>')
        elif addr == SET_BOOL:
            rec.update(result='value', value=bool(v & 0xff), via='SetValue<bool>')
        elif addr == SET_FLOAT:
            fv = struct.unpack('<f', struct.pack('<I', v & 0xffffffff))[0]
            rec.update(result='value', value=repr(fv), bits='%08x' % (v & 0xffffffff), via='SetValue<float>')
        else:
            rec.update(result='value', value=repr(from_bits64(v)), bits='%016x' % v, via='SetValue<double>')
    elif res.trap:
        rec.update(result='refused', via=f'TRAP {res.trap}')
    else:
        rec.update(result='error', via=f'rc={res.rc} fault={res.fault} {res.stderr[-300:]}')
    return rec


def int_parse(raw):
    res = R.run(['call', hex(INT_PARSE), 'hex:' + raw.hex() if raw else 'buf:1', f'i:{len(raw)}'])
    rax = res.calls[-1]['rax']
    return I32(rax) if rax >> 32 & 1 else None


D = '0' * 60 + '201'                          # 63 characters
INT_TEXTS = [
    # r2 accepted / refused examples and X1 probes
    '201', ' 201', '+201', ' +201', '  +201', '201 ', '', '   ', '201é', '+-201', '201.0', '2e2', '0x10', 'abc',
    ' 201 ', '+201 ', '-201', '- 201', '+', '-', '2147483648', '4294967497',
    # spaces on both sides, + with trailing spaces (TS-010), several trailing spaces
    ' +201 ', '  201  ', '   201 ', ' 201   ', '+201  ', '201  ', '201' + ' ' * 70, ' ' * 70 + '201',
    # minus sign
    '-0', '-000', '-1', '-495', ' -201', '  -201', '-201 ', '-201  ', ' -201 ', '+-0', '-+201', '--201', '-2147483648',
    '-2147483649', '2147483647', '00201', '+0', '0', '495', '-01',
    # other whitespace (after XML decoding) and inner characters
    '\t201', '201\t', '\n201', '201\n', '\r201', '2 01', '201x', ' 201',
    # length limit with and without sign, leading and trailing spaces
    D, '0' + D, D + ' ', '0' + D + ' ', ' ' + D, ' 0' + D, '+' + D, '+0' + D, '-' + D[1:], '-' + D,
    ' ' * 3 + D, D + '  ', '-' + '0' * 62, '-' + '0' * 63,
]
NUM_TEXTS = [
    '4.5', ' 4.5', ' 4.5 ', '4.5 ', '+4.5', '+4.5 ', ' +4.5 ', '-4.5', ' -4.5', '- 4.5', '+ 4.5', '+-4.5', '--4.5', '+', '-',
    '', ' ', '.', '-0', '-0.0', '+0', '0', '4.5abc', 'abc', '1e', '1e+', '\t4.5', '\n4.5', ' 4.5',
    'Invalid', 'Invalid ', ' Invalid', 'invalid', 'INVALID', 'inf', '-inf', 'INF', 'infinity', 'nan', '-nan', 'NaN',
    '0x10', '0x1p3', '1e400', '-1e400', '1e-400', '-1e-400', '3.4028235e38', '3.4028236e38', '1e39',
    '100.00000000000001', '1000.0000000000001', '0.09999999999999999', '0.000001', '93.3333333', '121.2', '0.3',
]
HEX_TEXTS = {'double': ['#3FF0000000000000', '#3ff0000000000000', '#3FF000000000000', '#3FF00000000000000', '#7FF0000000000000',
                        '#FFF8000000000000', '#8000000000000000', '#3FF000000000000G', '# 3FF00000000000', '#4012000000000000'],
             'float': ['#3F800000', '#3f800000', '#3F80000', '#3F8000000', '#7F800000', '#80000000', '#3F80000G', '#42f00000',
                       '#42F00000']}
BOOL_TEXTS = ['true', '1', 'false', '0', 'TRUE', 'True', '', ' true', 'true ', 'yes', '01', '00', 'false ']


def parse_target():
    ints = pmap(lambda t: {'parser': int_parse(t.encode('utf-8')), **convert('int', t.encode('utf-8'))}, INT_TEXTS)
    jobs = [(k, t) for k in ('double', 'float') for t in NUM_TEXTS + HEX_TEXTS[k]] + [('bool', t) for t in BOOL_TEXTS]
    nums = pmap(lambda kt: convert(kt[0], kt[1].encode('utf-8')), jobs)
    return {'int': ints, 'number_and_bool': nums}


# ---- (d) meter codes and list texts --------------------------------------------------------------------
def meter_target():
    pairs = [(n, d) for d in (1, 2, 4, 8, 16) for n in range(1, 100)]
    pairs += [(n, d) for n in (-2147483648, -1, 0, 1, 4, 99, 100, 101, 1000, 2147483647)
              for d in (-2147483648, -1, 0, 1, 2, 3, 4, 5, 6, 8, 12, 16, 17, 32, 64, 1 << 30)]
    def enc(batch):
        toks = sum((['call', hex(TS_ENCODE), 'hex:' + struct.pack('<ii', n, d).hex()] for n, d in batch), [])
        res = R.run(toks)
        assert res.ok and len(res.calls) == len(batch), res.stderr
        return [I32(c['rax']) for c in res.calls]
    enc_out = sum(pmap(enc, chunks(pairs, 150)), [])
    codes = [-2147483648, -100, -2, -1] + list(range(0, 3400)) + [2147483647]
    def dec(batch):
        res = R.run(sum((['call', hex(TS_DECODE), f'i:{c & 0xffffffff}'] for c in batch), []))
        assert res.ok and len(res.calls) == len(batch), res.stderr
        return [(I32(c['rax']), I32(c['rax'] >> 32)) for c in res.calls]
    dec_out = sum(pmap(dec, chunks(codes, 200)), [])  # at most 256 calls per process (loader rets[256])
    toks = ['call', hex(INIT_EMPTY_STRING), 'call', hex(TS_LIST), 'dump', hex(TS_LIST_BEGIN), '24']
    for i in range(495):
        toks += ['dump', f'{TS_LIST_BEGIN:#x}*+{8 * i}*+16', f'{TS_LIST_BEGIN:#x}*+{8 * i}*+4@']
    res = R.run(toks)
    assert res.ok, res.stderr
    begin, end, cap = struct.unpack('<QQQ', res.dumps[0][2])
    texts = [live_text(d) for _, _, d in res.dumps[1:]]
    return {'encode': [{'n': n, 'd': d, 'code': c} for (n, d), c in zip(pairs, enc_out)],
            'decode': [{'code': c, 'n': n, 'd': d} for c, (n, d) in zip(codes, dec_out)],
            'list': {'returned': hex(res.calls[1]['rax']), 'entries': (end - begin) // 8, 'capacity': (cap - begin) // 8,
                     'texts': texts}}


# ---- evidence files ---------------------------------------------------------------------------------
def function_starts(path):
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
                    b = data[p]; p += 1; v |= (b & 0x7f) << sh; sh += 7  # noqa: E702
                    if not b & 0x80:
                        break
                addr += v
                starts.append(addr)
            return starts
        off += size


def disassemble(path, addrs):
    starts, out = function_starts(path), []
    for a in addrs:
        end = starts[bisect.bisect_right(starts, a)]
        out.append(f'### {a:#x} .. {end:#x}\n')
        p = subprocess.run(['objdump', '-D', '-b', 'binary', '-m', 'i386:x86-64', '--adjust-vma=0x100000000',
                            f'--start-address={a:#x}', f'--stop-address={end:#x}', path],
                           capture_output=True, text=True, check=True)
        out.append(p.stdout.split('<.data+', 1)[-1].split('\n', 1)[-1])
    return ''.join(out)


def corpus_locator(tag, addr):
    """Chunk file and code SHA-256 of the decompiled record for addr (corpus pseudocode, static evidence)."""
    f, off = lookup.entry_map(lookup.ROOTS[tag], tag)[hex(addr)]
    with open(f, 'rb') as fh:
        fh.seek(off)
        r = json.loads(fh.readline())
    return {'chunk': f, 'byte_offset': off, 'code_sha256': r['code_sha256'], 'state': r['state']}


def summarize(w, sp, cases, pr, m):
    lines = []
    sweep = w['sweep']
    for model in ('glibc', 'cr', 'exact'):
        bad = [r for r in sweep if r['X'] != r[model]]
        lines.append(f"writer sweep: X = {model} model for {len(sweep) - len(bad)}/{len(sweep)}")
    ex = [r for r in sweep if r['X'] != r['exact']]
    lines.append(f"  X != exact-log model: {len(ex)} values; kinds {sorted({r['kind'] for r in ex})}; "
                 f"offsets {min((r['offset_ulps'] for r in ex), default=None)}..{max((r['offset_ulps'] for r in ex), default=None)} ulps; "
                 f"n {sorted({r['n'] for r in ex})}")
    nc = [r for r in sweep if not r['glibc_log10_is_cr']]
    lines.append(f"  glibc log10 not correctly rounded at {len(nc)}/{len(sweep)} inputs; text differs from cr model at "
                 f"{sum(r['X'] != r['cr'] for r in sweep)}")
    for r in sp + cases:
        lines.append(f"attr writer {r['kind']} {r['x']} -> {[x['text'] for x in r['writes']]}")
    for r in pr['int']:
        lines.append(f"int {r['text']!r}: parser {r['parser']!r}; converter {r['result']} {r.get('value', '')}")
    for r in pr['number_and_bool']:
        lines.append(f"{r['kind']} {r['text']!r}: {r['result']} {r.get('value', '')} {r.get('bits', '')}")
    enc_ok = all(e['code'] == (e['n'] - 1 + 99 * int(math.log2(e['d']))) for e in m['encode']
                 if 1 <= e['n'] <= 99 and e['d'] in (1, 2, 4, 8, 16))
    lines.append(f"meter encode: formula holds for all valid (n, d): {enc_ok}; list entries {m['list']['entries']}")
    lines.append(f"meter list == decoded n/d for 0..494: "
                 f"{all(t == f'{d[0]}/{d[1]}' for t, d in zip(m['list']['texts'], [(x['n'], x['d']) for x in m['decode'] if 0 <= x['code'] <= 494]))}")
    return '\n'.join(lines) + '\n'


def main():
    blocks = {}
    first = len(R.log)
    sweep = writer_sweep()
    specials = pmap(lambda kv: attr_write(*kv), WRITER_SPECIALS)
    cases = pmap(lambda kv: attr_write(*kv), WRITER_CASE_VALUES)
    blocks['writer'] = (first, len(R.log))
    first = len(R.log)
    pr = parse_target()
    blocks['parse'] = (first, len(R.log))
    first = len(R.log)
    m = meter_target()
    blocks['meter'] = (first, len(R.log))

    def used(a, b):
        u = {}
        for _, res in R.log[a:b]:
            for s, n in res.used.items():
                u[s] = u.get(s, 0) + n
        return dict(sorted(u.items()))

    out = {'writer': {'sweep': sweep, 'attribute_writer_specials': specials, 'attribute_writer_case_values': cases},
           'parse': pr, 'meter': m}
    (HERE / 'results').mkdir(exist_ok=True)
    for k, v in out.items():
        a, b = blocks[k]
        v['replaced_imports_called'] = used(a, b)
        v['runs'] = {'count': b - a, 'not_ok_or_trapped': sum(not r.ok for _, r in R.log[a:b])}
        (HERE / 'results' / f'{k}.json').write_text(json.dumps(v, indent=1) + '\n')
    (HERE / 'raw').mkdir(exist_ok=True)
    with open(HERE / 'raw' / 'runs.jsonl', 'w') as f:
        for argv, res in sorted(R.log, key=lambda e: json.dumps(e[0])):
            f.write(json.dumps({'argv': argv, 'rc': res.rc, 'stdout': res.stdout, 'stderr': res.stderr,
                                'timeout': res.timeout, 'gdb_script': res.gdb_script}) + '\n')
    (HERE / 'addresses.json').write_text(json.dumps(
        {'slice': SLICE, 'image_base': '0x100000000', 'libraries_substituted': LIBS,
         'setup': {'node_vtable': hex(VT), 'node_slot_0x28_target': '0x103c2c670', 'stream_slots': [hex(SLOT30), hex(SLOT38)],
                   'setvalue_stubs': {'bool': hex(SET_BOOL), 'double': hex(SET_DOUBLE), 'float': hex(SET_FLOAT), 'int': hex(SET_INT)},
                   'type_ids': TYPE_IDS},
         'functions': [{**x, 'x86': hex(x['x86']), 'arm64': x['arm64'] and hex(x['arm64']),
                        'corpus': {t: corpus_locator(t, a) for t, a in (('x86', x['x86']), ('arm', x['arm64'])) if a}}
                       for x in MATCHES]},
        indent=1) + '\n')
    (HERE / 'x86-disasm.txt').write_text(disassemble(SLICE, [x['x86'] for x in MATCHES] + [0x103c2c670]))
    (HERE / 'imports.txt').write_text(R.run(['--imports']).stdout)
    s = summarize(out['writer'], specials, cases, pr, m)
    (HERE / 'summary.txt').write_text(s)
    print(s, end='')


if __name__ == '__main__':
    assert f32_next(1.0, 1) == 1.0000001192092896 and f32_next(1.0, -1) == 0.9999999403953552
    assert rule_text('double', 0.3, 'exact') == '0.299999999999999989' and rule_text('float', 121.2, 'cr') == '121.199997'
    main()
