"""X2 MIDI: run the original x86_64 MIDI-mapping chain (receiver -> Apply -> value function -> takeover)
of Live 12.4.3 on chosen inputs (ADR 0003, label X).

usage: python3 -I -B run_x2.py            (from any directory; writes next to this file)

Inputs: the x86_64 slice (tools/xexec/xexec.py SLICE), the N7 case file
analysis/.../n7-midi-transforms-v1/out/acceptance-cases.json (MT-01..MT-23) and the inputs defined below.
Outputs: results/*.json, raw/runs.jsonl (argv, gdb script, stdout, stderr of every run), addresses.json,
x86-disasm.txt, imports.txt, summary.txt (stdout of this script).

Harness (one gdb process per message sequence; tools/xexec is used unchanged):
- The original receivers run: CC receiver 0x101bbc3b0 (registry type 3), 14-bit MSB/LSB setters 0x101bbced0 /
  0x101bbcf10 (types 5/6) and the combiner 0x101bbc870. The receivers call Apply 0x101bbc9c0 (through the
  original callback 0x101bc09b0 for type 3), which calls the value function 0x101bb27b0 and takeover 0x101bb8b70.
- The takeover preference is set by the original command handler 0x101bc0770 (OSetMidiTakeOverMode) from a
  message buffer {u16 0, u16 read offset 0, i32 index}.
- Stubbed under gdb (body not run; see STUBS): Apply's three accessors of the owner/parameter object and the
  parameter setter. The parameter is simulated by them: "get value" returns the last value "set" (initially the
  case's current value). The PickUpNotification post inside Pick-Up (0x101bb8a0d..0x101bb8a7f) is jumped over
  after the result is stored; the result is reloaded by the original epilogue.
- Not run: the per-input previous-value table and dispatcher (arm64 0x101b65b68 / 0x101b7842c). The harness
  supplies the prior as that static reading says: the last data value on the same controller, -129 before any.
"""
import bisect
import ctypes
import json
import os
import struct
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
from xexec import Runner, SLICE, as_f32, as_f64, dbl, f32, flt, parse  # noqa: E402

# ---- x86_64 addresses (image VAs) ---------------------------------------------------------------
MIDI_TU_INIT = 0x101bc1360   # static initializer of the MIDI-mapping unit (accel tables, notification types)
SET_TAKEOVER = 0x101bc0770   # OSetMidiTakeOverMode handler: reads i32 from the message, stores 0x107443e78
TAKEOVER_MODE = 0x107443e78  # the global the takeover function reads
CC_RECEIVER = 0x101bbc3b0    # (rdi receiver, esi mode; xmm0 value, xmm1 prior)
MSB_SET = 0x101bbced0        # (rdi receiver; xmm0 value, xmm1 prior); registry type 5
LSB_SET = 0x101bbcf10        # registry type 6
COMBINER = 0x101bbc870
APPLY_CB = 0x101bc09b0       # callback the CC receiver installs: tail-calls Apply
APPLY = 0x101bbc9c0          # (rdi owner, rsi details*, rdx data*, rcx extra*)
VALUE_FN = 0x101bb27b0       # (xmm0 cur, xmm1 {lo,hi}, rdi data*, esi quantized, edx reversed) -> xmm0
TAKEOVER = 0x101bb8b70       # (edi id, esi mode, edx reversed, ecx quantized; xmm0 cur, xmm1 new, xmm2 prior, xmm3 {lo,hi})
PICKUP = 0x101bb8990         # Pick-Up decision + notification
THREAD_CHECK = 0x10119c480   # runs natively; false selects Apply's direct path
OWNER_DEREF = 0x101abb210    # stub: returns rdi
PARAM_AT = 0x101b3d680       # stub: returns a dummy parameter pointer
GET_VALUE = 0x101b6f830      # stub: returns the simulated current value
SET_VALUE = 0x101b3d360      # stub: records *(float*)rcx and makes it the simulated current value
NOTIFY_FROM, NOTIFY_TO = 0x101bb8a0d, 0x101bb8a80

MATCHES = [
    {'x86': SET_TAKEOVER, 'arm64': 0x101b83750, 'role': 'OSetMidiTakeOverMode handler', 'how': 'registered with '
     'the string "OSetMidiTakeOverMode" and field "TakeOverModeIndex" in 0x101bb8da0; only writer of 0x107443e78; '
     'arm64 0x101b83750 stores 0x106fb2110 the same way (n7-0003)'},
    {'x86': TAKEOVER, 'arm64': 0x101b7c508, 'role': 'takeover', 'how': 'Apply 0x101bbc9c0 calls it right after '
     'the value function, as arm64 Apply 0x101b801c4; reads 0x107443e78; constants -129, 0.5, {128, 16384}, -1, 1'},
    {'x86': PICKUP, 'arm64': 0x101b7c344, 'role': 'Pick-Up', 'how': 'only callee of the takeover besides the '
     'value function; 2(hi-lo)/{128,16384} window; posts the notification type 0x107443e48'},
    {'x86': CC_RECEIVER, 'arm64': 0x101b7f894, 'role': 'CC receiver (registry type 3)', 'how': 'registered for '
     'type 3 by 0x101bc1950 (arm64 registry 0x101b84798 type 3); avoid +0x44, Zoom +0x3c, sensitivity +0x48, '
     'accumulator +0x4c'},
    {'x86': MSB_SET, 'arm64': 0x101b8028c, 'role': '14-bit MSB setter (registry type 5)', 'how': 'registered for '
     'type 5 by 0x101bc1950; same body as X1 0x101bbc830'},
    {'x86': LSB_SET, 'arm64': 0x101b802bc, 'role': '14-bit LSB setter (registry type 6)', 'how': 'registered for '
     'type 6; same body as X1 0x101bbc980'},
    {'x86': COMBINER, 'arm64': 0x101b7fcc0, 'role': '14-bit combiner', 'how': 'X1; prior FLT_MAX when avoid '
     '+0x44 is set or either half prior is FLT_MAX'},
    {'x86': APPLY_CB, 'arm64': 0x101b83974, 'role': 'apply callback', 'how': 'installed by the CC receiver; '
     'shifts arguments and jumps to Apply'},
    {'x86': APPLY, 'arm64': 0x101b7fde4, 'role': 'Apply', 'how': 'X1; Type 2 threshold test, value function, '
     'takeover gate (mode 0/5, Type 1, prior != FLT_MAX), setter'},
    {'x86': VALUE_FN, 'arm64': 0x101b76bf0, 'role': 'value function', 'how': 'X1'},
    {'x86': 0x101bb7ff0, 'arm64': 0x101b7b96c, 'role': 'relative decoder', 'how': 'X1'},
    {'x86': MIDI_TU_INIT, 'arm64': None, 'role': 'static initializer of the unit', 'how': 'X1'},
    {'x86': 0x1023e2a60, 'arm64': 0x1022cec38, 'role': 'LMidiPreferences::OnTakeOverModeChanged (static only)',
     'how': 'arm64 named by PTR_CallMemberFunc<&LMidiPreferences::OnTakeOverModeChanged>; both post '
     'OSetMidiTakeOverMode with the chooser index (+0xd8, -99 -> 0)'},
    {'x86': 0x1023e0050, 'arm64': 0x1022cc18c, 'role': 'LMidiPreferences constructor (static only)',
     'how': 'builds the chooser entry list [sControlNoTakeOverEntry, sControlPickUpTakeOverEntry, '
     'sControlValueScalingTakeOverEntry]'},
]
STUBS = {
    OWNER_DEREF: 'owner -> object (*(owner)); stub returns rdi, the object is only passed to the next two stubs',
    PARAM_AT: 'object, timeable index -> parameter pointer; stub returns 0x5a5a0000',
    GET_VALUE: "parameter -> current value (virtual); stub returns the simulated value",
    SET_VALUE: 'parameter setter (object, timeable index, id, {value, extra}); stub records the value',
    NOTIFY_FROM: 'PickUpNotification post (0x101bb8a0d..0x101bb8a7f) jumped over after the result is stored',
}
FLT_MAX = 3.4028234663852886e38
NO_PRIOR = -129.0
MODES = {'Absolute': 0, 'AccelSignedBit': 1, 'AccelBinaryOffset': 2, 'AccelTwoCompliment': 3,
         'AccelSignedBit2': 4, 'Absolute14Bit': 5, 'LinearSignedBit': 6, 'LinearBinaryOffset': 7,
         'LinearTwoCompliment': 8, 'LinearSignedBit2': 9}
TAKEOVER_INDEX = {'none': 0, 'pickup': 1, 'scaling': 2}
TYPES = {'other': 0, 'continuous': 1, 'onoff': 2, 'enum': 3}

R = Runner()
LOG = []                     # (argv, gdb script, Result) of every run
libm = ctypes.CDLL('libm.so.6')
libm.fmaf.restype, libm.fmaf.argtypes = ctypes.c_float, [ctypes.c_float] * 3


def bits(x):
    return struct.unpack('<I', struct.pack('<f', x))[0]


def gdb_script(cur0):
    """Breakpoint commands that stand in for the parameter object and skip the notification post."""
    s = ['set pagination off', 'set confirm off', 'break xcall', 'run', 'delete 1', f'set $cur = {bits(cur0):#x}']

    def bp(addr, body):
        s.extend([f'break *{addr:#x}', 'commands', 'silent', *body, 'continue', 'end'])
    bp(OWNER_DEREF, ['set $rax = $rdi', 'return'])
    bp(PARAM_AT, ['set $rax = 0x5a5a0000', 'return'])
    bp(GET_VALUE, [f'printf "HIT {GET_VALUE:#x} %x\\n", $cur', 'set $xmm0.v4_int32[0] = $cur', 'return'])
    bp(SET_VALUE, [f'printf "HIT {SET_VALUE:#x} %x %x %x\\n", *(unsigned int*)$rcx, $esi, $edx',
                   'set $cur = *(int*)$rcx', 'return'])
    bp(NOTIFY_FROM, [f'printf "HIT {NOTIFY_FROM:#x} %x %x\\n", $xmm0.v4_int32[0], $ebx', f'set $pc = {NOTIFY_TO:#x}'])
    # observation only (the body runs): Apply's data record and the takeover's arguments
    bp(APPLY, [f'printf "HIT {APPLY:#x} %x %x %x %x\\n", *(unsigned int*)$rdx, *((unsigned int*)$rdx+1), '
               '*((unsigned int*)$rdx+2), *((unsigned int*)$rdx+3)'])
    bp(TAKEOVER, [f'printf "HIT {TAKEOVER:#x} %x %x %x %x %x %x %x %x %x\\n", $xmm0.v4_int32[0], $xmm1.v4_int32[0], '
                  '$xmm2.v4_int32[0], $xmm3.v4_int32[0], $xmm3.v4_int32[1], $edi, $esi, $edx, $ecx'])
    bp(THREAD_CHECK + 0x20, [f'printf "HIT {THREAD_CHECK:#x} %x\\n", $eax'])   # at its ret: al = posting path
    s.append('continue')
    return '\n'.join(s) + '\n'


def gdb_run(tokens, cur0):
    argv = [str(R.bin), R.slice, *map(str, tokens)]
    script = gdb_script(cur0)
    f = tempfile.NamedTemporaryFile('w', suffix='.gdb', delete=False)
    f.write(script)
    f.close()
    try:
        p = subprocess.run(['gdb', '-q', '-batch', '-nx', '-x', f.name, '--args', *argv],
                           capture_output=True, text=True, timeout=120)
        res = parse(p.returncode, p.stdout, p.stderr)
    finally:
        os.unlink(f.name)
    LOG.append((argv[1:], script, res))
    if res.trap or res.fault or res.rc:
        raise RuntimeError(f'run failed: trap={res.trap} fault={res.fault} rc={res.rc}\n{res.stderr[-800:]}')
    return res


def details(kind, lo, hi, quantized, zoom=1.0, uid=7):
    """TTimeableDetails, 0x24 bytes: Type, Min, Max, Quantized, InterpretReverse, TrackIndex, TimeableIndex,
    UniqueAObjectId, Zoom, HasBeenPickedUp (field names from the OChangeControllerDataCommand registration)."""
    return struct.pack('<iffBBxxiiifB3x', TYPES[kind], lo, hi, int(quantized), 0, 0, 1, uid, zoom, 0)


def chain(messages, param, takeover='none', avoid=False, mode_name='Absolute', priors=None):
    """Run one message sequence. messages: list of (cc, data byte). param: kind, min, max, quantized, value.
    Returns the simulated parameter value after each message plus the observed calls."""
    mode = MODES[mode_name]
    d = details(param['kind'], param['min'], param['max'], param['quantized'])
    if mode == 5:
        rec = bytearray(0x48)
        struct.pack_into('<Q', rec, 8, 0x100000000)      # object whose +0xa0 is the owner (nonzero)
        rec[0x10:0x34] = d
        struct.pack_into('<ffff', rec, 0x34, FLT_MAX, FLT_MAX, FLT_MAX, FLT_MAX)
        rec[0x44] = int(avoid)
    else:
        rec = bytearray(0x50)
        struct.pack_into('<QQQ', rec, 8, APPLY_CB, 0, 0x100000000)
        rec[0x20:0x44] = d
        rec[0x44] = int(avoid)
        struct.pack_into('<ff', rec, 0x48, 1.0, 0.0)     # sensitivity 1, accumulator 0
    toks = ['call', hex(MIDI_TU_INIT), 'call', hex(SET_TAKEOVER), 'hex:' + struct.pack('<HHi', 0, 0, TAKEOVER_INDEX[takeover]).hex()]
    last = dict(priors or {})
    for i, (cc, v) in enumerate(messages):
        r = 'hex:' + rec.hex() if i == 0 else 'ref:b1'
        prior = last.get(cc, NO_PRIOR)
        if mode == 5:
            toks += ['call', hex(MSB_SET if cc == 20 else LSB_SET), r, flt(v), flt(prior)]
        else:
            toks += ['call', hex(CC_RECEIVER), r, f'i:{mode}', flt(v), flt(prior)]
        last[cc] = v
    toks += ['dump', hex(TAKEOVER_MODE), '4']
    res = gdb_run(toks, param['value'])
    stored = struct.unpack('<i', res.dumps[0][2])[0]
    values, cur, calls = [], f32(param['value']), []
    for k in range(len(messages)):
        hits = [(a, vals) for c, a, vals in res.hits if c == k + 2]
        sets = [as_f32(vals[0]) for a, vals in hits if a == SET_VALUE]
        cur = sets[-1] if sets else cur
        values.append(cur)
        calls.append(describe(hits))
    return {'values': values, 'calls': calls, 'takeover_index_stored': stored,
            'posting_path': any(a == THREAD_CHECK and vals[0] & 0xff for c, a, vals in res.hits)}


def describe(hits):
    out = []
    for a, v in hits:
        if a == APPLY:
            out.append({'apply': {'v': as_f32(v[0]), 'prior': as_f32(v[1]), 'mode': v[2], 'sens': as_f32(v[3])}})
        elif a == TAKEOVER:
            out.append({'takeover': {'cur': as_f32(v[0]), 'new': as_f32(v[1]), 'prior': as_f32(v[2]),
                                     'lo': as_f32(v[3]), 'hi': as_f32(v[4]), 'id': v[5], 'mode': v[6],
                                     'reversed': v[7] & 0xff, 'quantized': v[8] & 0xff}})
        elif a == NOTIFY_FROM:
            out.append({'pickup_result': as_f32(v[0])})
        elif a == SET_VALUE:
            out.append({'set': as_f32(v[0])})
    return out


def msgs(lines):
    return [(int(x.split()[1], 16), int(x.split()[2], 16)) for x in lines]


# ---- target A: MT-01..MT-23 through the whole chain --------------------------------------------------
UNIT = {'kind': 'continuous', 'min': 0.0, 'max': 1.0, 'quantized': False, 'value': 0.5}
STEP3 = {'kind': 'continuous', 'min': 0.0, 'max': 3.0, 'quantized': True, 'value': 1.0}
ONOFF = {'kind': 'onoff', 'min': 64.0, 'max': 127.0, 'quantized': False, 'value': 0.0}
ANY = ('none', 'pickup', 'scaling')
MT_SETUP = {   # case -> (parameter, takeover settings to run, avoid flag); every one must give the same values
    **{f'MT-{i:02d}': (UNIT, ('none',), False) for i in range(1, 6)},
    **{f'MT-{i:02d}': (UNIT, ANY, False) for i in range(6, 15)},
    'MT-15': (STEP3, ('none',), False), 'MT-16': (STEP3, ANY, False),
    'MT-17': (ONOFF, ANY, False), 'MT-18': (ONOFF, ANY, False),
    'MT-19': (UNIT, ('pickup',), False), 'MT-20': (UNIT, ('scaling',), False), 'MT-21': (UNIT, ('pickup',), False),
    'MT-22': (UNIT, ANY, True), 'MT-23': (UNIT, ANY, False),
}


def mt_cases():
    src = ROOT / 'analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/out/acceptance-cases.json'
    out = []
    for c in json.load(open(src))['cases']:
        param, settings, avoid = MT_SETUP[c['id']]
        runs = {t: chain(msgs(c['input']), param, t, avoid, c['map_mode']) for t in settings}
        vals = [r['values'] for r in runs.values()]
        exp = c['expected_after_each_message']
        x = vals[0]
        out.append({'case': c['id'], 'map_mode': c['map_mode'], 'input': c['input'], 'parameter': param,
                    'avoid_takeover': avoid, 'takeover_settings_run': list(settings),
                    'same_under_all_settings_run': all(v == x for v in vals),
                    'expected_r4': exp, 'x': x, 'agree_1e-6': [abs(a - b) <= 1e-6 for a, b in zip(x, exp)],
                    'agree': all(abs(a - b) <= 1e-6 for a, b in zip(x, exp)) and len(x) == len(exp),
                    **({'r5_model': (m := r5_model(msgs(c['input']), param, settings[0], c['map_mode'], avoid)),
                        'r5_model_agrees': all(abs(a - b) <= 1e-6 for a, b in zip(x, m))}
                       if c['map_mode'].startswith('Absolute') else {}),
                    'calls': {t: r['calls'] for t, r in runs.items()},
                    'posting_path_taken': any(r['posting_path'] for r in runs.values()),
                    'takeover_index_stored': {t: r['takeover_index_stored'] for t, r in runs.items()}})
    return out


# ---- target A: new takeover cases (every sequence starts from an input just opened) ----------------------
def rha(x):
    """Round half away from zero (frinta / roundss + copysign), exact."""
    x = F(x)
    return F(int(x + F(1, 2)) if x >= 0 else -int(-x + F(1, 2)))


def r5_model(seq, param, setting, mode_name, avoid=False):
    """REQ-MIDI-USER-005 as revision 5 states it, in exact arithmetic (absolute modes only).
    seq: (cc, data byte) from an input just opened. Returns the value after each message."""
    mn, mx, q = F(param['min']), F(param['max']), param['quantized']
    lo, hi = min(mn, mx), max(mn, mx)
    cur, out, last, held = F(param['value']), [], {}, {}

    def tgt(v):                      # Absolute target, reported min and max, either order
        t = mn + (mx - mn) * F(v) / 127
        return rha(t) if q else t

    for cc, v in seq:
        prev = last.get(cc)
        last[cc] = v
        if mode_name == 'Absolute14Bit':
            held[cc] = (v, prev)
            if not (20 in held and 52 in held):
                out.append(float(cur))
                continue
            (m, pm), (l, pl) = held.pop(20), held.pop(52)
            data = F(m * 128 + l, 129)
            pm, pl = -129 if pm is None else pm, -129 if pl is None else pl
            prior = F(((pm << 7) | pl), 129)          # 32-bit two's complement OR, as the combiner computes it
            has_prior = True
        else:
            data, prior, has_prior = F(v), (None if prev is None else F(prev)), prev is not None
        if param['kind'] == 'onoff':
            on = lo <= data <= hi
            cur = F(int(on != (mn > mx)))
            out.append(float(cur))
            continue
        n = tgt(data)
        if param['kind'] != 'continuous' or setting == 'none' or (avoid and mode_name == 'Absolute'):
            cur = n
            out.append(float(cur))
            continue
        c = min(max(cur, lo), hi)
        if not has_prior:
            r = c
        else:
            p = tgt(prior)
            w0, w = (hi - lo) / 256, (hi - lo) / 64
            if p == -129:
                r = c
            elif abs(p - c) <= w0:
                r = n
            elif setting == 'pickup':
                r = n if min(n, p) - w <= c <= max(n, p) + w else c
            elif abs(n - c) <= w:
                r = n
            elif p == n:
                r = c
            elif n > p:
                r = c + (hi - c) * (n - p) / (hi - p)
            else:
                r = c - (c - lo) * (p - n) / (p - lo)
        cur = min(max(r, lo), hi)
        out.append(float(cur))
    return out


def nextf(x, up):
    """Adjacent binary32 value of positive binary32 x."""
    return struct.unpack('<f', struct.pack('<I', bits(x) + (1 if up else -1)))[0]


REV = {**UNIT, 'min': 1.0, 'max': 0.0}
R127 = {'kind': 'continuous', 'min': 0.0, 'max': 127.0, 'quantized': False}
TK = [  # id, purpose, takeover, parameter, mode, messages from input open
    ('TK-01', 'Pick-Up: knob below, value stays until it passes', 'pickup', UNIT, 'Absolute',
     [(20, 10), (20, 11), (20, 63), (20, 70)]),
    ('TK-02', 'Pick-Up: knob above, crossing downward picks up', 'pickup', UNIT, 'Absolute',
     [(20, 120), (20, 100), (20, 60), (20, 50)]),
    ('TK-03', 'Pick-Up: jump past the value in one message picks up', 'pickup', UNIT, 'Absolute',
     [(20, 10), (20, 100)]),
    ('TK-04', 'Value Scaling: upward travel', 'scaling', UNIT, 'Absolute', [(20, 10), (20, 20), (20, 127)]),
    ('TK-05', 'Value Scaling: downward travel', 'scaling', UNIT, 'Absolute', [(20, 120), (20, 110), (20, 0)]),
    ('TK-06', 'Value Scaling: same data value twice keeps the value', 'scaling', UNIT, 'Absolute',
     [(20, 10), (20, 10)]),
    ('TK-07', 'Value Scaling: first message after open keeps the value', 'scaling', UNIT, 'Absolute', [(20, 100)]),
    ('TK-08', 'Pick-Up, reversed range (reported min 1, max 0)', 'pickup', REV, 'Absolute',
     [(20, 10), (20, 63), (20, 64), (20, 70)]),
    ('TK-09', 'Value Scaling, reversed range, target moving down', 'scaling', REV, 'Absolute',
     [(20, 10), (20, 20), (20, 30)]),
    ('TK-10', 'Value Scaling, reversed range, target moving up', 'scaling', REV, 'Absolute', [(20, 100), (20, 90)]),
    ('TK-11', 'Pick-Up, reversed range: previous target within (max-min)/256 of the value', 'pickup',
     {**REV, 'value': 0.25}, 'Absolute', [(20, 95), (20, 100)]),
    ('TK-12', 'Pick-Up, reversed range (min 3, max -1): just inside the window', 'pickup',
     {**UNIT, 'min': 3.0, 'max': -1.0, 'value': 1.06}, 'Absolute', [(20, 40), (20, 60)]),
    ('TK-13', '14-bit, Pick-Up: first pair after open, target above the value', 'pickup', UNIT, 'Absolute14Bit',
     [(20, 0x50), (52, 0)]),
    ('TK-14', '14-bit, Pick-Up: first pair after open, target below the value', 'pickup', UNIT, 'Absolute14Bit',
     [(20, 0x10), (52, 0)]),
    ('TK-15', '14-bit, Value Scaling: first pair after open, target below the value', 'scaling', UNIT,
     'Absolute14Bit', [(20, 0x10), (52, 0)]),
    ('TK-16', '14-bit, Value Scaling: first pair after open, target above', 'scaling', UNIT, 'Absolute14Bit',
     [(20, 0x60), (52, 0)]),
    ('TK-17', '14-bit, Value Scaling: MSB has a previous value, LSB none', 'scaling', UNIT, 'Absolute14Bit',
     [(20, 0x10), (20, 0x60), (52, 0)]),
    ('TK-18', '14-bit, Value Scaling: LSB has a previous value, MSB none', 'scaling', UNIT, 'Absolute14Bit',
     [(52, 0x20), (52, 0), (20, 0x60)]),
    ('TK-19', '14-bit, Pick-Up: later pairs use the previous pair', 'pickup', UNIT, 'Absolute14Bit',
     [(20, 0x30), (52, 0), (20, 0x41), (52, 0), (20, 0x50), (52, 0)]),
    ('TK-20', '14-bit, Value Scaling: second pair scales from the first', 'scaling', UNIT, 'Absolute14Bit',
     [(20, 0x10), (52, 0), (20, 0x20), (52, 0)]),
    ('TK-21', 'Stepped continuous parameter, Value Scaling: result is not rounded', 'scaling', STEP3, 'Absolute',
     [(20, 0), (20, 64)]),
    ('TK-22', 'Stepped continuous parameter, Pick-Up: the previous target is rounded', 'pickup', STEP3,
     'Absolute', [(20, 50), (20, 127)]),
    ('TK-23', 'Enumerated parameter: never subject to takeover', 'pickup', {**STEP3, 'kind': 'enum'}, 'Absolute',
     [(20, 127)]),
    ('TK-24', 'Other parameter kind: never subject to takeover', 'scaling', {**UNIT, 'kind': 'other'}, 'Absolute',
     [(20, 10)]),
    ('TK-25', 'A previous target of exactly -129 counts as no previous value', 'pickup',
     {**UNIT, 'min': -129.0, 'max': 0.0, 'value': -10.0}, 'Absolute', [(20, 0), (20, 127)]),
    ('TK-26', 'Harness check: avoid flag on a 14-bit receiver gives the combiner a FLT_MAX prior', 'pickup', UNIT,
     'Absolute14Bit', [(20, 0x10), (52, 0)]),
    ('TK-27', '14-bit on/off: pair/129 compared with thresholds 64..127', 'none', ONOFF, 'Absolute14Bit',
     [(20, 0x40), (52, 0x00), (20, 0x40), (52, 0x7F), (20, 0x7F), (52, 0x7F)]),
    ('TK-28', 'On/off with reversed thresholds (min 127, max 64): result inverted', 'none',
     {**ONOFF, 'min': 127.0, 'max': 64.0}, 'Absolute', [(20, 63), (20, 64), (20, 127)]),
    ('TK-29', 'Crossfader Absolute14Bit pair (pair receiver has no avoid flag), Pick-Up', 'pickup', UNIT,
     'Absolute14Bit', [(20, 0x10), (52, 0)]),
    ('TK-30', 'Wide range 20..999, Absolute, None (slice tolerance)', 'none',
     {**UNIT, 'min': 20.0, 'max': 999.0, 'value': 500.0}, 'Absolute', [(20, 4), (20, 5), (20, 8), (20, 127)]),
    # boundaries: range 0..127 (min 0), targets exact integers; first message gives the previous value
    ('TB-01', 'In sync: c - p = (max-min)/256 exactly', 'scaling', {**R127, 'value': 30 + 127 / 256}, 'Absolute',
     [(20, 30), (20, 10)]),
    ('TB-02', 'In sync: c - p one binary32 step beyond (max-min)/256', 'scaling',
     {**R127, 'value': nextf(30 + 127 / 256, True)}, 'Absolute', [(20, 30), (20, 10)]),
    ('TB-03', 'In sync: p - c = (max-min)/256 exactly', 'scaling', {**R127, 'value': 30 - 127 / 256}, 'Absolute',
     [(20, 30), (20, 50)]),
    ('TB-04', 'In sync: p - c one binary32 step beyond (max-min)/256', 'scaling',
     {**R127, 'value': nextf(30 - 127 / 256, False)}, 'Absolute', [(20, 30), (20, 50)]),
    ('TB-05', 'Pick-Up window: c = max(n, p) + (max-min)/64 exactly', 'pickup', {**R127, 'value': 30 + 127 / 64},
     'Absolute', [(20, 10), (20, 30)]),
    ('TB-06', 'Pick-Up window: c one binary32 step above it', 'pickup',
     {**R127, 'value': nextf(30 + 127 / 64, True)}, 'Absolute', [(20, 10), (20, 30)]),
    ('TB-07', 'Pick-Up window: c = min(n, p) - (max-min)/64 exactly', 'pickup', {**R127, 'value': 30 - 127 / 64},
     'Absolute', [(20, 50), (20, 30)]),
    ('TB-08', 'Pick-Up window: c one binary32 step below it', 'pickup',
     {**R127, 'value': nextf(30 - 127 / 64, False)}, 'Absolute', [(20, 50), (20, 30)]),
    ('TB-09', 'Value Scaling: |n - c| = (max-min)/64 exactly', 'scaling', {**R127, 'value': 60 + 127 / 64},
     'Absolute', [(20, 10), (20, 60)]),
    ('TB-10', 'Value Scaling: |n - c| one binary32 step beyond', 'scaling',
     {**R127, 'value': nextf(60 + 127 / 64, True)}, 'Absolute', [(20, 10), (20, 60)]),
]
HARNESS_ONLY = {'TK-26'}
# New acceptance cases (revision 5): case id -> exploration id. Labels: X, or S-cond (on/off threshold source).
NEW_CASES = {'MT-24': 'TK-02', 'MT-25': 'TK-03', 'MT-26': 'TK-05', 'MT-27': 'TK-06', 'MT-28': 'TK-07',
             'MT-29': 'TK-08', 'MT-30': 'TK-09', 'MT-31': 'TK-10', 'MT-32': 'TK-11', 'MT-33': 'TK-12',
             'MT-34': 'TK-13', 'MT-35': 'TK-14', 'MT-36': 'TK-15', 'MT-37': 'TK-17', 'MT-38': 'TK-18',
             'MT-39': 'TK-19', 'MT-40': 'TK-22', 'MT-41': 'TK-23', 'MT-42': 'TK-25', 'MT-43': 'TK-27',
             'MT-44': 'TK-28', 'MT-45': 'TK-29', 'MT-46': 'TK-30',
             **{f'MT-{47 + i}': f'TB-{i + 1:02d}' for i in range(10)}}
SCOND = {'MT-43', 'MT-44'}


def tau(param):
    return max(1e-6, 2.0 ** -22 * max(abs(param['min']), abs(param['max'])))


def tk_cases():
    out = []
    for cid, purpose, setting, param, mode, ms in TK:
        res = chain(ms, param, setting, avoid=(cid == 'TK-26'), mode_name=mode)
        row = {'case': cid, 'purpose': purpose, 'takeover': setting, 'map_mode': mode, 'parameter': param,
               'messages': [f'B0 {cc:02X} {v:02X}' for cc, v in ms], 'avoid_takeover': cid == 'TK-26',
               'x': res['values'], 'calls': res['calls']}
        if cid not in HARNESS_ONLY:
            m = r5_model(ms, param, setting, mode)
            row['r5_model'] = m
            row['tolerance'] = tau(param)
            row['agrees_with_r5_model'] = all(abs(a - b) <= tau(param) for a, b in zip(res['values'], m))
        if mode == 'Absolute' and param['kind'] == 'continuous' and not param['quantized']:
            row['r4_literal_reading'] = r4_literal(ms, param, setting)
            row['agrees_with_r4_literal'] = all(abs(a - b) <= tau(param)
                                                for a, b in zip(res['values'], row['r4_literal_reading']))
        out.append(row)
    return out


def r4_literal(ms, param, setting):
    """Revision 4 Pick-Up / Value Scaling read literally: w, the sync tolerance and the scaling use the reported
    min and max even when max < min."""
    mn, mx = F(param['min']), F(param['max'])
    lo, hi = min(mn, mx), max(mn, mx)
    cur, last, out = F(param['value']), {}, []
    for cc, v in ms:
        n = mn + (mx - mn) * F(v) / 127
        c = min(max(cur, lo), hi)
        if setting == 'none':
            r = n
        elif cc not in last:
            r = c
        else:
            p = mn + (mx - mn) * F(last[cc]) / 127
            w = (mx - mn) / 64
            if abs(p - c) <= (mx - mn) / 256:
                r = n
            elif setting == 'pickup':
                r = n if min(n, p) - w <= c <= max(n, p) + w else c
            elif abs(n - c) <= w:
                r = n
            elif p == n:
                r = c
            elif n > p:
                r = c + (mx - c) * (n - p) / (mx - p)
            else:
                r = c - (c - mn) * (p - n) / (p - mn)
        cur = min(max(r, lo), hi)
        last[cc] = v
        out.append(float(cur))
    return out


def new_cases(tk):
    by = {c['case']: c for c in tk}
    out = []
    for mid, src in NEW_CASES.items():
        c = by[src]
        out.append({'id': mid, 'source_run': src, 'label': 'S-cond' if mid in SCOND else 'X',
                    'title': c['purpose'], 'map_mode': c['map_mode'], 'takeover': c['takeover'],
                    'parameter': c['parameter'], 'input': c['messages'],
                    'expected_after_each_message': c['x'], 'tolerance': c['tolerance'],
                    'r5_model_agrees': c['agrees_with_r5_model'],
                    'provenance': 'X: x86_64 receiver, Apply, value function and takeover run under '
                                  'run_x2.py (stubs in addresses.json); arm64 equivalence static'})
    return out


# ---- target C: value tolerance across slices -------------------------------------------------------------
RANGES = [(0.0, 1.0), (-1.0, 1.0), (20.0, 999.0), (-999.0, 999.0), (-70.0, 6.0), (0.25, 0.75),
          (1.0, 0.0), (999.0, 20.0), (-100.0, -1.0), (1e-3, 2.0)]


BATCH = 200   # value-function calls per process; xexec allows at most 256 calls per process


def value_batch(v_list, lo, hi, reversed_):
    """X: the value function alone, up to BATCH calls per process after the initializer (no gdb)."""
    rng = dbl(as_f64(struct.unpack('<Q', struct.pack('<ff', min(lo, hi), max(lo, hi)))[0]))
    out = []
    for k in range(0, len(v_list), BATCH):
        toks = ['call', hex(MIDI_TU_INIT)]
        for v in v_list[k:k + BATCH]:
            toks += ['call', hex(VALUE_FN), flt(0.5), rng, 'hex:' + struct.pack('<ffif', v, FLT_MAX, 0, 1.0).hex(),
                     'i:0', f'i:{int(reversed_)}']
        res = R.run(toks)
        LOG.append((['<Runner>'] + [str(t) for t in toks[:12]] + ['...'], None, res))
        if not res.ok or len(res.calls) != len(v_list[k:k + BATCH]) + 1:
            raise RuntimeError(f'value batch failed {res.trap} {res.fault} {res.stderr[-300:]}')
        out += [as_f32(c['xmm0']) for c in res.calls[1:]]
    return out


def ulp32(x):
    x = abs(f32(x))
    return struct.unpack('<f', struct.pack('<I', bits(x) + 1))[0] - x if x else 1.401298464324817e-45


def models(v, lo, hi, reversed_):
    """x86 (two roundings) and arm64 (fmadd at 0x101b76c60) Absolute sequences in binary32."""
    a, b = f32(min(lo, hi)), f32(max(lo, hi))
    vv = f32(f32(127.0) - f32(v)) if reversed_ else f32(v)
    t = f32(vv / 127.0)
    s1 = f32(a * f32(1.0 - t))
    x86 = f32(f32(b * t) + s1)
    arm = float(libm.fmaf(b, t, s1))
    return x86, arm


def tolerance():
    out = []
    pairs = [m << 7 | l for m in range(128) for l in range(128)]
    for lo, hi in RANGES:
        rev = hi < lo
        v7 = [float(v) for v in range(128)]
        v14 = [f32(f32(float(p)) / f32(129.0)) for p in pairs]
        x7 = value_batch(v7, lo, hi, rev)
        x14 = value_batch(v14[::41] + [v14[-1]], lo, hi, rev)   # every 41st pair plus full scale (X sample)
        m7 = [models(v, lo, hi, rev) for v in v7]
        m14 = [models(v, lo, hi, rev) for v in v14]
        m14s = m14[::41] + [m14[-1]]
        M = max(abs(lo), abs(hi))
        d7 = [abs(x - arm) for (_, arm), x in zip(m7, x7)]
        d14 = [abs(x86 - arm) for x86, arm in m14]
        dmax = max(d7 + d14)
        out.append({'min': lo, 'max': hi, 'reversed': rev,
                    'x86_model_equals_x_7bit': sum(m[0] == x for m, x in zip(m7, x7)), 'n7': 128,
                    'x86_model_equals_x_14bit_sample': sum(m[0] == x for m, x in zip(m14s, x14)), 'n14_sample': len(x14),
                    'arm64_differs_7bit': sum(d > 0 for d in d7), 'arm64_differs_14bit_model': sum(d > 0 for d in d14),
                    'n14': len(d14), 'max_abs_difference': dmax, 'M': M, 'ulp32_M': ulp32(M),
                    'max_difference_in_ulp32_M': dmax / ulp32(M), 'max_difference_over_M': dmax / M,
                    'bound_2^-22_M': M * 2.0 ** -22, 'within_bound': dmax <= M * 2.0 ** -22})
    return out


def vs32(c, n, p, lo, hi):
    """Value Scaling in binary32 in the operation order both slices use (x86 0x101bb8b70, arm64 0x101b7c508)."""
    c = min(max(c, lo), hi)
    w0, w = f32(f32(0.5 * f32(hi - lo)) / 128), f32(f32(f32(hi - lo) + f32(hi - lo)) / 128)
    if f32(c - w0) <= p <= f32(c + w0) or f32(c - w) <= n <= f32(c + w):
        return n
    if p == n:
        return c
    if n > p:
        return f32(c + f32(f32(hi - c) * f32(f32(n - p) / f32(hi - p))))
    return f32(c - f32(f32(c - lo) * f32(f32(p - n) / f32(p - lo))))


def value_scaling_amplification():
    """Model only (not X): Value Scaling fed with the x86 and with the arm64 Absolute targets, every previous and
    new data value, 33 current values per range. Shows how far the slices can drift apart after scaling."""
    out = []
    for lo, hi in [(0.0, 1.0), (20.0, 999.0), (-999.0, 999.0), (-70.0, 6.0), (0.25, 0.75)]:
        tg = [models(v, lo, hi, False) for v in range(128)]
        worst = (0.0, None)
        for k in range(33):
            c = f32(lo + (hi - lo) * k / 32)
            for P in range(128):
                for V in range(128):
                    a = vs32(c, tg[V][0], tg[P][0], lo, hi)
                    b = vs32(c, tg[V][1], tg[P][1], lo, hi)
                    if abs(a - b) > worst[0]:
                        worst = (abs(a - b), {'c': c, 'prior': P, 'new': V, 'x86': a, 'arm64': b})
        M = max(abs(lo), abs(hi))
        out.append({'min': lo, 'max': hi, 'max_cross_slice_difference': worst[0],
                    'in_units_of_2^-22_M': worst[0] / (M * 2.0 ** -22), 'worst': worst[1]})
    return out


# ---- evidence files ------------------------------------------------------------------------------------------
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
                    b = data[p]
                    p += 1
                    v |= (b & 0x7f) << sh
                    sh += 7
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
    results = {'mt': mt_cases(), 'takeover': tk_cases(), 'tolerance': tolerance(),
               'value_scaling_model': value_scaling_amplification()}
    cases = new_cases(results['takeover'])
    used = {}
    for _, _, res in LOG:
        for sym, n in res.used.items():
            used[sym] = used.get(sym, 0) + n
    meta = {'replaced_imports_called': dict(sorted(used.items())), 'runs': len(LOG),
            'stubs_under_gdb': {hex(k): v for k, v in STUBS.items()}}
    (HERE / 'results').mkdir(exist_ok=True)
    for k, v in results.items():
        key = 'ranges' if k in ('tolerance', 'value_scaling_model') else 'cases'
        (HERE / 'results' / f'{k}.json').write_text(json.dumps({key: v, **meta}, indent=1) + '\n')
    (HERE / 'acceptance-cases-x2.json').write_text(json.dumps(
        {'schema': 'n7-acceptance-cases (MT ids continue MT-01..MT-23)', 'target': 'Ableton Live 12 Suite 12.4.3',
         'note': 'Every sequence starts from an input just opened, channel 0, CC 20 (MSB) and CC 52 (LSB). '
                 'Expected values are X results; tolerance = max(1e-6, 2^-22 * max(|min|, |max|)).',
         'cases': cases}, indent=1) + '\n')
    (HERE / 'raw').mkdir(exist_ok=True)
    with open(HERE / 'raw' / 'runs.jsonl', 'w') as f:
        for argv, script, res in LOG:
            f.write(json.dumps({'argv': argv, 'gdb_script': script, 'rc': res.rc, 'stdout': res.stdout,
                                'stderr': res.stderr}) + '\n')
    (HERE / 'addresses.json').write_text(json.dumps(
        {'slice': SLICE, 'image_base': '0x100000000',
         'functions': [{**m, 'x86': hex(m['x86']), 'arm64': m['arm64'] and hex(m['arm64'])} for m in MATCHES],
         'stubs_under_gdb': {hex(k): v for k, v in STUBS.items()}}, indent=1) + '\n')
    (HERE / 'x86-disasm.txt').write_text(disassemble(SLICE, [m['x86'] for m in MATCHES] + [THREAD_CHECK]))
    (HERE / 'imports.txt').write_text(R.run(['--imports']).stdout)
    report(results, cases, meta)


def report(results, cases, meta):
    mt = results['mt']
    print(f"MT-01..23: {sum(c['agree'] for c in mt)}/{len(mt)} agree with r4 within 1e-6; "
          f"same under every takeover setting run: {sum(c['same_under_all_settings_run'] for c in mt)}/{len(mt)}; "
          f"r5 model agrees (absolute cases): {sum(c['r5_model_agrees'] for c in mt if 'r5_model_agrees' in c)}/"
          f"{sum('r5_model_agrees' in c for c in mt)}; posting path taken: {sum(c['posting_path_taken'] for c in mt)}")
    for c in mt:
        if not c['agree']:
            print('  differs', c['case'], c['x'], c['expected_r4'])
    for c in results['takeover']:
        r5 = '' if 'agrees_with_r5_model' not in c else ('r5=X' if c['agrees_with_r5_model'] else f"r5 {c['r5_model']}")
        r4 = '' if 'agrees_with_r4_literal' not in c else ('r4=X' if c['agrees_with_r4_literal']
                                                          else f"r4 literal {[round(x, 7) for x in c['r4_literal_reading']]}")
        print(f"{c['case']} {c['takeover']:8} {c['map_mode']:13} c0={c['parameter']['value']!r} "
              f"{[round(x, 7) for x in c['x']]}  {r5}  {r4}")
    print(f"new acceptance cases: {len(cases)} ({sum(c['label'] == 'X' for c in cases)} X, "
          f"{sum(c['label'] == 'S-cond' for c in cases)} S-cond); r5 model agrees {sum(c['r5_model_agrees'] for c in cases)}")
    for t in results['tolerance']:
        print(f"tolerance ({t['min']}, {t['max']}): x86 model = X {t['x86_model_equals_x_7bit']}/128 and "
              f"{t['x86_model_equals_x_14bit_sample']}/{t['n14_sample']}; arm64 differs 7-bit {t['arm64_differs_7bit']}, "
              f"14-bit {t['arm64_differs_14bit_model']}/{t['n14']}; max {t['max_abs_difference']:.3g} = "
              f"{t['max_difference_in_ulp32_M']:.3g} ulp(M) = {t['max_difference_over_M']:.3g} M; "
              f"within 2^-22 M: {t['within_bound']}")
    for t in results['value_scaling_model']:
        print(f"value scaling model ({t['min']}, {t['max']}): max cross-slice difference {t['max_cross_slice_difference']:.3g}"
              f" = {t['in_units_of_2^-22_M']:.3g} x 2^-22 M; worst {t['worst']}")
    print(f"runs {meta['runs']}; replaced imports called: {', '.join(meta['replaced_imports_called'])}")


if __name__ == '__main__':
    assert struct.calcsize('<iffBBxxiiifB3x') == 0x24
    assert models(64, 0.0, 1.0, False) == (f32(64 / 127), f32(64 / 127))
    main()
