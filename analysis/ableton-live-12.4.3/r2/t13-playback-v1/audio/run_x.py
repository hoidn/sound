"""T1.3 audio: extracted execution of Live x86_64 functions for unwarped audio-clip playback.

Runs (each a fresh process of the loader copy xexec_t13.c, see xexec.py):
  inc     SSemitonesToInc (x86 0x10236f1f0; Engine OWarperProcessor::SSemitonesToInc 0xaa7290)
  quant   SQuantizePosFileSmpl (x86 0x10235b910; Engine OWarperBase::SQuantizePosFileSmpl 0xa92b50)
  gain    clip-gain value->control (mapping slot +0x28, x86 0x102683d70 -> SControlLevel 0x101aed490)
          and control->gain on the engine side (SAudioLevel 0x101aed3a0), range 3 table built by the
          original SInitA 0x101aed1e0; the pool allocator 0x101ac2ec0 is replaced by malloc under gdb
  kernel  per-output-sample interpolators of OFadingPlayer on a player record built by the original OPlayer
          ctor 0x10234d260 at record+0x10, then position, increment, amp 1 and ramp 1 (delta 0) poked in:
          Non 0x1022979f0, Lin 0x1022978c0, Cubic 0x102297930, FIR 0x102297a30, FIR2X 0x102297b10
          (float mono), T16 Non 0x1022984d0, T16 Lin 0x102298370 (16-bit mono); FIR tables from the
          original SInitO 0x101e95890 (glibc exp, sinf)
Writes results/*.json, raw/runs.jsonl. Usage: python3 -I -B run_x.py
Dependencies: gcc, gdb, numpy; the Live x86_64 slice (XEXEC_SLICE or the default in xexec.py).
"""
import json, os, struct, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np
import xexec
from xexec import as_f32, as_f64, f32

R = xexec.Runner()
OUT, RAW = HERE / 'results', HERE / 'raw'
OUT.mkdir(exist_ok=True); RAW.mkdir(exist_ok=True)
INIT = ['call', '0x1014206e0']           # shared empty Live string (harness convention, X1)
MALLOC = {0x101ac2ec0: ['$rax = (long)malloc($rsi + 0x40)']}


def hexf(x):
    return 'f:' + f32(x).hex()


def check(res, what):
    if not res.ok:
        raise SystemExit(f'{what}: rc={res.rc} trap={res.trap} fault={res.fault}\n{res.stderr[-800:]}')


# ---- 1. increment from semitones and rates ---------------------------------------------
def run_inc():
    rows, toks, keys = [], [], []
    semis = [0, 1, -1, 12, -12, 0.5, -0.25, 7, 24, 48, -48, 0.01, 3.3]
    rates = [(48000, 48000), (44100, 48000), (48000, 44100), (96000, 48000), (22050, 44100), (44100, 44100)]
    for s in semis:
        for fr, er in rates:
            toks += ['call', '0x10236f1f0', xexec.dbl(s), xexec.dbl(fr), xexec.dbl(er)]
            keys.append((s, fr, er))
    res = R.run(toks)
    check(res, 'inc')
    for (s, fr, er), c in zip(keys, res.calls):
        inc = as_f64(c['xmm0'])
        p = float(np.power(np.float32(2 ** (1 / 12)), np.float32(s), dtype=np.float32))
        model = float(np.float64(np.float32(p))) * (fr / er)
        fixed = int(np.floor(abs(inc) * 2 ** 32 + 0.5)) * (1 if inc >= 0 else -1)   # llround(2^32 * inc)
        rows.append({'semitones': s, 'file_rate': fr, 'engine_rate': er, 'inc': inc.hex(), 'inc_dec': repr(inc),
                     'model_powf_numpy': repr(model), 'equal_model': bool(inc == model), 'fixed_32_32': fixed})
    return rows


# ---- 2. file-position quantization -------------------------------------------------------
def run_quant():
    xs = [0.0, 1.0, 12345.678, 0.5 / 2 ** 24, 1.5 / 2 ** 24, -2.5 / 2 ** 24, 44100 * 0.123456789, 1e7 + 1 / 3]
    toks = []
    for x in xs:
        toks += ['call', '0x10235b910', xexec.dbl(x)]
    res = R.run(toks)
    check(res, 'quant')
    rows = []
    for x, c in zip(xs, res.calls):
        y = as_f64(c['xmm0'])
        t = x * 2 ** 24
        model = (np.trunc(t + np.copysign(0.49999999999999994, t))) / 2 ** 24
        rows.append({'x': repr(x), 'y': repr(y), 'model_round_half_away_2^-24': repr(float(model)), 'equal': bool(y == model)})
    return rows


# ---- 3. clip gain ------------------------------------------------------------------------
GAINS = [1.0, 0.5011872336272722, 0.3162277639, 0.8666422963, 0.630957365, 0.942270577, 0.7542234063,
         1.99526238, 0.9652072787, 1.41253757, 0.4837246537, 8.5381422, 7.07945824, 5.01187229, 3.98107195,
         2.51188636, 1.58489323, 1.25892544, 10.0, 0.7943282127, 15.848932, 15.848933219909668, 20.0,
         0.000316227766, 0.0003162277571391314, 1e-5, 0.0, 0.1, 0.01, 0.001, 0.0316227766, 1.12201845]


def gain_prefix():
    # shared-memory static-pointer block for SStaticPointer(10), tables by the original SInitA, then the
    # range-3 mapping object by its original constructor 0x102683d10 (b1)
    return INIT + ['buf:4096', 'poke', '0x1074004c0', 'b0', 'call', '0x101aed1e0',
                   'call', '0x102683d10', 'buf:64', 'i:3']


def run_gain():
    toks = gain_prefix()
    for g in GAINS:
        toks += ['call', '0x102683d70', 'ref:b1', hexf(g)]
    res = R.run(toks, skip=MALLOC)
    check(res, 'gain value->control')
    ctl = [as_f32(c['xmm0']) for c in res.calls[3:]]
    toks = gain_prefix()
    for c in ctl:
        toks += ['call', '0x101aed3a0', hexf(c), 'i:3']
    toks += ['dump', '0x1074004c0*+0x460*+0x20*+0x30*', '404', 'dump', '0x1074004c0*+0x460*+0x20*+0x20*', '404']
    res2 = R.run(toks, skip=MALLOC)
    check(res2, 'gain control->gain')
    back = [as_f32(c['xmm0']) for c in res2.calls[3:]]
    audio = struct.unpack('<101f', res2.dumps[0][2])
    db = struct.unpack('<101f', res2.dumps[1][2])
    rows = []
    for g, c, b in zip(GAINS, ctl, back):
        g32 = f32(g)
        rows.append({'sample_volume': repr(g), 'binary32': repr(g32), 'control': repr(c), 'engine_gain': repr(b),
                     'engine_gain_hex': b.hex(), 'rel_err': (b - g32) / g32 if g32 else None,
                     'equal_binary32': bool(b == g32)})
    return {'rows': rows, 'range3_audio_table': list(audio), 'range3_db_table': list(db)}


# ---- 4. interpolation kernels --------------------------------------------------------------
KER = {'Non': 0x1022979f0, 'Lin': 0x1022978c0, 'Cubic': 0x102297930, 'FIR': 0x102297a30, 'FIR2X': 0x102297b10,
       'T16Non': 0x1022984d0, 'T16Lin': 0x102298370, 'T16FIR': 0x102298520, 'T16FIR2X': 0x102298600}
CL = '/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Core Library/'
SHIPPED = {'rim3k48': 'Samples/One Shots/Drums/Rim/Rim 3k Sharp.wav', 'rimdmx44': 'Samples/One Shots/Drums/Rim/Rim DMX Vinyl.wav'}


def wav16(rel):
    """(rate, int16 mono frames, sha256) of a 16-bit PCM mono WAV (RIFF chunks walked, 'data' read)."""
    import hashlib
    b = open(CL + rel, 'rb').read()
    i, fmt, data = 12, None, None
    while i + 8 <= len(b):
        cid, n = b[i:i + 4], struct.unpack('<I', b[i + 4:i + 8])[0]
        if cid == b'fmt ':
            fmt = struct.unpack('<HHIIHH', b[i + 8:i + 24])
        elif cid == b'data':
            data = b[i + 8:i + 8 + n]
        i += 8 + n + (n & 1)
    assert fmt[0] == 1 and fmt[1] == 1 and fmt[5] == 16, fmt
    return fmt[2], np.frombuffer(data, '<i2'), hashlib.sha256(b).hexdigest()
PAD = 64                                   # samples of zeros before index 0 (taps reach back 7, FIR2X 15)


def run_kernel(name, sig, frac, idx, inc_fixed, n, t16=False, fir=False):
    data = (np.concatenate([np.zeros(PAD), sig, np.zeros(PAD)]))
    raw = (data.astype('<i2').tobytes() if t16 else data.astype('<f4').tobytes())
    w = 2 if t16 else 4
    toks = INIT[:]
    if fir:
        toks += ['call', '0x101e95890']
    amp = struct.unpack('<I', struct.pack('<f', 1.0 / 32768 if t16 else 1.0))[0]
    toks += ['call', '0x1014206e0', 'buf:0x250', 'hex:' + raw.hex(), f'buf:{4 * n}', f'buf:{4 * n}',
             'call', '0x10234d260', 'ref:b0+16',        # original OPlayer ctor (Engine OPlayer::OPlayer 0xa84360)
             'poke', 'b0+16', f'b1+{PAD * w}', 'poke', 'b0+24', f'b1+{PAD * w}',
             'poke', 'b0+32', hex((idx << 32) + frac), 'poke', 'b0+40', hex(inc_fixed),
             'poke', 'b0+56', hex(amp), 'poke', 'b0+64', hex(0x3f800000)]
    for k in range(n):
        toks += ['call', hex(KER[name]), 'ref:b0', f'ref:b2+{4 * k}', f'ref:b3+{4 * k}']
    toks += ['dump', 'b2', str(4 * n), 'dump', 'b3', str(4 * n), 'dump', 'b0+32', '8']
    if fir:
        toks += ['dump', '0x10750ed80', str(257 * 64), 'dump', '0x107512dc0', str(256 * 64)]
    res = R.run(toks)
    check(res, name)
    L = np.frombuffer(res.dumps[0][2], '<f4')
    Rr = np.frombuffer(res.dumps[1][2], '<f4')
    end = struct.unpack('<Q', res.dumps[2][2])[0]
    tabs = (np.frombuffer(res.dumps[3][2], '<f4').reshape(257, 16), np.frombuffer(res.dumps[4][2], '<f4').reshape(256, 16)) if fir else None
    return L, Rr, end, tabs, data


def f32a(x):
    return np.float32(x)


def model(name, data, frac, idx, inc_fixed, n, tabs=None):
    """Python models of the decompiled kernels, in binary32 with the decompiled operation order."""
    out = []
    pos = (idx << 32) + frac
    x = data.astype(np.float32)
    for _ in range(n):
        i, fr = (pos >> 32) + PAD, pos & 0xffffffff
        f = np.float32(np.float64(fr) * 2.3283064365386963e-10)
        if name in ('Non', 'T16Non'):
            v = x[i]
        elif name in ('Lin', 'T16Lin'):
            v = (np.float32(1) - f) * x[i] + f * x[i + 1]
        elif name == 'Cubic':
            x0, x1, x2, x3 = x[i], x[i + 1], x[i + 2], x[i + 3]
            a = ((x1 - x2) * np.float32(3) + (x3 - x0)) * np.float32(0.5)
            c = (x2 - x0) * np.float32(0.5)
            b = (x0 - x1) + (c - a)                      # order from x86-disasm-cubic.txt
            v = ((a * f + b) * f + c) * f + x1
        elif name == 'FIR':
            t, d = tabs
            ph, fine = fr >> 24, np.float32((fr >> 9) & 0x7fff)
            coef = (fine * d[ph] + t[ph]).astype(np.float64)
            v = np.float32(np.dot(coef, x[i - 7:i + 9].astype(np.float64)))
        else:
            v = np.float32('nan')
        out.append(np.float32(v))
        pos += inc_fixed if name not in ('Non', 'T16Non') else (inc_fixed >> 32) << 32
    return np.array(out, np.float32)


def fir_formula():
    """Kaiser-windowed sinc as read from SInitO (Engine NFirInterpolation::SInitO 0x520260): 257 phases x 16 taps,
    tap j at phase k: x = 7 - j + k/256; w = I0(5*pi*sqrt(1 - u^2)) / I0(5*pi) with u = clamp(x + 8, 0, 16)/8 - 1;
    h = 0.95 * sinc(0.95 x) * w (sinc in binary32 via sinf).  Returns float64 values (I0 exact, not the polynomial)."""
    k = np.arange(257)[:, None] / 256.0
    j = np.arange(16)[None, :]
    x = 7 - j + k
    t = np.clip(x + 8, 0, 16)
    u = t / 8 - 1
    w = np.i0(5 * np.pi * np.sqrt(np.maximum(0, 1 - u * u))) / np.i0(5 * np.pi)
    fx = 0.95 * x
    sinc = np.where(fx == 0, 1.0, np.sin(np.pi * fx) / np.where(fx == 0, 1, np.pi * fx))
    return 0.95 * sinc * w


def fixed(inc):
    return int(np.floor(inc * 2 ** 32 + 0.5))


def run_kernels():
    n = 96
    sine = 0.5 * np.sin(2 * np.pi * np.arange(256) / 32.0)
    ramp = np.arange(256, dtype=float)
    imp = np.zeros(256); imp[16] = 1.0
    t16 = np.round(sine * 32767)
    incs = {'1': fixed(1.0), '44100/48000': fixed(44100 / 48000), '48000/44100': fixed(48000 / 44100),
            '+1 semitone': fixed(float(np.float32(2 ** (1 / 12)))), '-12 semitones': fixed(0.5), '1.5': fixed(1.5)}
    rows = []
    for name in ('Non', 'Lin', 'Cubic', 'FIR', 'FIR2X'):
        for sname, sig in (('sine', sine), ('ramp', ramp), ('impulse16', imp)):
            for iname, inc in incs.items():
                for frac in (0, 0x40000000):
                    if name == 'Non' and (frac or iname != '1'):
                        continue
                    L, Rr, end, tabs, data = run_kernel(name, sig, frac, 0, inc, n, fir=name.startswith('FIR'))
                    m = model(name, data, frac, 0, inc, n, tabs)
                    row = {'kernel': name, 'signal': sname, 'inc': iname, 'inc_fixed': inc, 'start_frac': frac,
                           'out_L': [float(v) for v in L], 'R_equals_L': bool(np.array_equal(L, Rr)),
                           'end_pos_fixed': end, 'model_max_abs_diff': float(np.nanmax(np.abs(m - L))) if name != 'FIR2X' else None,
                           'model_bit_equal': bool(np.array_equal(m, L)) if name != 'FIR2X' else None}
                    if tabs is not None and sname == 'impulse16' and iname == '1' and not frac:
                        np.save(OUT / 'fir_table.npy', tabs[0]); np.save(OUT / 'fir_diff_table.npy', tabs[1])
                    rows.append(row)
    for name in ('T16Non', 'T16Lin'):
        for iname in ('1', '44100/48000'):
            if name == 'T16Non' and iname != '1':
                continue
            L, Rr, end, _, data = run_kernel(name, t16, 0, 0, incs[iname], n, t16=True)
            m = model(name, data, 0, 0, incs[iname], n) * np.float32(1 / 32768)
            rows.append({'kernel': name, 'signal': 'sine int16', 'inc': iname, 'inc_fixed': incs[iname], 'start_frac': 0,
                         'out_L': [float(v) for v in L], 'R_equals_L': bool(np.array_equal(L, Rr)), 'end_pos_fixed': end,
                         'model_max_abs_diff': float(np.max(np.abs(m - L))), 'model_bit_equal': bool(np.array_equal(m, L))})
    return rows


def run_shipped():
    """Reference renders of the first 96 output samples of two shipped 16-bit mono files (kernel only: start at
    frame 0, fraction 0, gain 1, ramp 1).  Float kernels get x/32768, 16-bit kernels the int16 frames with amp 1/32768."""
    n, rows = 96, []
    cases = [('rim3k48', 'Non', '48k file at 48k, transposition 0', fixed(1.0)),
             ('rimdmx44', 'Lin', '44.1k file at 48k, HiQ off', fixed(44100 / 48000)),
             ('rimdmx44', 'FIR', '44.1k file at 48k, HiQ on, float chunks', fixed(44100 / 48000)),
             ('rim3k48', 'Lin', '48k file at 48k, +12 semitones, HiQ off', 8589939712),
             ('rim3k48', 'FIR2X', '48k file at 48k, +12 semitones, HiQ on, float chunks', 8589939712)]
    for key, ker, what, inc in cases:
        rate, x, sha = wav16(SHIPPED[key])
        sig = x[:256].astype(float)
        for t16 in (False, True):
            name = ('T16' + ker) if t16 else ker
            L, Rr, end, tabs, data = run_kernel(name, sig if t16 else sig / 32768, 0, 0, inc, n, t16=t16,
                                                fir=ker.startswith('FIR'))
            rows.append({'file': SHIPPED[key], 'file_sha256': sha, 'file_rate': rate, 'frames': int(len(x)),
                         'case': what, 'kernel': name, 'inc_fixed': inc, 'out': [float(v) for v in L],
                         'out_hex': [struct.pack('<f', v).hex() for v in L], 'R_equals_L': bool(np.array_equal(L, Rr)),
                         'first_frames_int16': [int(v) for v in x[:12]]})
    return rows


def main():
    results = {'inc': run_inc(), 'quant': run_quant(), 'gain': run_gain(), 'kernels': run_kernels(),
               'shipped': run_shipped()}
    tab = np.load(OUT / 'fir_table.npy').astype(np.float64)
    ref = fir_formula()
    results['fir_formula'] = {'max_abs_diff_table_vs_formula': float(np.max(np.abs(tab - ref))),
                              'phase0_taps': [float(v) for v in tab[0]], 'phase128_taps': [float(v) for v in tab[128]],
                              'dc_gain_phase0': float(tab[0].sum()), 'dc_gain_phase128': float(tab[128].sum())}
    for k, v in results.items():
        (OUT / f'{k}.json').write_text(json.dumps(v, indent=1) + '\n')
    with open(RAW / 'runs.jsonl', 'w') as f:
        for argv, res in R.log:
            f.write(json.dumps({'argv': argv, 'rc': res.rc, 'stdout': res.stdout, 'stderr': res.stderr,
                                'gdb_script': res.gdb_script}) + '\n')
    s = results
    print('inc: %d/%d equal powf model' % (sum(r['equal_model'] for r in s['inc']), len(s['inc'])))
    print('quant: %d/%d equal model' % (sum(r['equal'] for r in s['quant']), len(s['quant'])))
    print('gain: %d/%d round trip equal binary32; max |rel err| %.3g' % (
        sum(r['equal_binary32'] for r in s['gain']['rows']), len(s['gain']['rows']),
        max(abs(r['rel_err']) for r in s['gain']['rows'] if r['rel_err'] is not None)))
    for r in s['kernels']:
        print('kernel %-6s %-10s inc %-12s frac %#010x  model bit-equal %s  max diff %s  R=L %s' % (
            r['kernel'], r['signal'], r['inc'], r['start_frac'], r['model_bit_equal'], r['model_max_abs_diff'], r['R_equals_L']))
    print('fir table vs formula: max abs diff %.3g' % s['fir_formula']['max_abs_diff_table_vs_formula'])
    sh = s['shipped']
    for a, b in zip(sh[0::2], sh[1::2]):
        print('shipped %-55s float %-6s vs 16-bit %-8s bit-equal %s max diff %.3g' % (
            a['case'], a['kernel'], b['kernel'], a['out'] == b['out'], max(abs(u - v) for u, v in zip(a['out'], b['out']))))
    print('processes:', len(R.log))


if __name__ == '__main__':
    main()
