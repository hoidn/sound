"""X2 notes and launch: run original x86_64 Live 12.4.3 functions (ADR 0003, evidence label X).

usage: python3 -I -B run_x2.py          (from any directory; writes next to this file)

Targets (addresses and matching evidence in addresses.json):
  a  note value limits 0x102a2a7f0, note and event time grid 0x102a2a9b0 / 0x1026ede60, the writer
     text of the held values (0x10142b980 P=17, 0x10142b6c0 P=9), the MidiKey getter 0x1029ed3b0;
  b  launch grid length 0x101ad2ef0, lattice helper 0x1011999d0, anchor/boundary helper 0x101ae8280,
     enum getter 0x101556330;
  c  follow-action chance rescaling 0x10262a930 on UserFloat chance objects (setter 0x101565360),
     ARemoteableDouble post-load rounding 0x101555850 (follow time).
Loader: xexec_x2.c (tools/xexec/xexec.c plus a "poke" command), built to LOADER below; the driver is
tools/xexec/xexec.py with its build step pointed at that loader. Each process makes at most 250 calls
and 250 buffers (the loader's fixed tables hold 256).
Outputs: results/{notes,launch,follow}.json, raw/runs.jsonl, addresses.json, imports.txt,
x86-disasm.txt, summary.txt (stdout).
"""
import bisect
import json
import math
import struct
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
import xexec  # noqa: E402
from xexec import SLICE, as_f32, as_f64, dbl, f32, flt, ustr  # noqa: E402

LOADER = Path('/var/tmp/sound-analysis/xexec-x2-notes-launch/xexec')


def build_loader():
    src = HERE / 'xexec_x2.c'
    if not LOADER.exists() or LOADER.stat().st_mtime < src.stat().st_mtime:
        LOADER.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['gcc', *xexec.CFLAGS, '-o', str(LOADER), str(src), '-ldl', '-lm'], check=True)
    return LOADER


xexec.build = build_loader
R = xexec.Runner()

# ---- x86_64 addresses ----------------------------------------------------------------------------
INIT_EMPTY_STRING = 0x1014206e0   # shared empty Live string (X1)
NOTE_LIMITS = 0x102a2a7f0         # AMidiNoteEvent vtable 0x106d6ab58 slot +0xd0 (post-load)
NOTE_GRID = 0x102a2a9b0           # AMidiNoteEvent translator vtable 0x106d6ad10 slot +0 (this = note + 0x28)
EVENT_GRID = 0x1026ede60          # APerNoteEvent translator vtable 0x106d24b48 slot +0 (this = event + 0x28)
DOUBLE_WRITER = 0x10142b980       # (sret, double): writer text P = 17 (X1)
FLOAT_WRITER = 0x10142b6c0        # (sret, double): writer text P = 9 (X1)
MIDIKEY_GET = 0x1029ed3b0         # KeyTrack -> int at +0x40
GRID = 0x101ad2ef0                # ({int n, int d}*, int q) -> grid length in beats
LATTICE = 0x1011999d0             # (int mode, double x, double g, double a)
BOUNDARY = 0x101ae8280            # (entry*, double t, double g, int mode): a = max([entry+8], 0), then LATTICE
ENUM_GET = 0x101556330            # ARemoteableEnum value getter: [+0xd8], -99 read as 0
FA_POSTLOAD = 0x10262a930         # AFollowAction vtable 0x106d0dc08 slot +0xd0 (chance rescaling)
FA_NOTIFY = 0x102630ef0           # CallMemberFunc<&AFollowAction::NotifyListeners> (skipped under gdb)
BOOL_SET = 0x101554600            # ARemoteableBool setter (skipped under gdb; FollowActionEnabled)
UF_VTABLE = 0x106bc35b0           # UserFloat (ARemoteableFloat subclass) vtable, factory 0x101564c00
UF_VTABLE2 = 0x106bc3848          # its secondary vtable at +0x70
UF_INIT = 0x101564e20             # (float min, float max, float default, obj*, mapping*, callback*)
UF_SETTER = 0x101565360           # UserFloat vtable +0x280: clamp to the mapped bounds, then store and notify
RAW_FLOAT_STORE = 0x101558d40     # movss %xmm0,0x58(%rdi): the field the generic loader stores into
MAPPING_CTOR = 0x101566480        # (float a, float b, float c, float d, obj*): value mapping, vtable 0x106bc3958
RD_VTABLE = 0x106bc07b0           # ARemoteableDouble vtable, factory 0x101555070
RD_POSTLOAD = 0x101555850         # ARemoteableDouble slot +0xd0: generic post-load, then round when flag +0x70
GENERIC_POSTLOAD = 0x10147e120    # generic compound post-load (skipped under gdb for a leaf double)

MATCHES = [
    {'x86': NOTE_LIMITS, 'arm64': 0x1028e2c80, 'role': 'AMidiNoteEvent post-load value limits',
     'how': 'slot +0xd0 of the AMidiNoteEvent vtable in both slices (x86 0x106d6ab58 stored by the ctor 0x102a2a660; '
            'arm64 0x1068256e0); same fields +0x38/+0x40/+0x48/+0x4c and constants 127, 1, DBL_MAX, (127, 1)'},
    {'x86': NOTE_GRID, 'arm64': 0x1028e2e24, 'role': 'note copy into the in-memory note with Time/Duration grid rounding',
     'how': 'slot +0 of the translator vtable (x86 0x106d6ad10, arm64 0x106825898); same sentinel table, h, 0.5, '
            '3843840 (x86 0x105b3eb00/0x105b3eac0/0x105a57808/0x105b3eac8 = arm64 0x1055d9680 and immediates)'},
    {'x86': 0x102a2a250, 'arm64': 0x1028e26c0, 'role': 'AMidiNoteEvent member registration (setup reference only)',
     'how': 'registers mTime +0x30, mDuration +0x38, mVelocity +0x40, mVelocityDeviation +0x44, mOffVelocity +0x48, '
            'mProbability +0x4c, mIsEnabled +0x50, mNoteId +0x58 (x86 pseudocode); only x86 function naming "OffVelocity" '
            'next to the note vtables'},
    {'x86': EVENT_GRID, 'arm64': 0x1025c7a0c, 'role': 'per-note event copy with TimeOffset grid rounding',
     'how': 'slot +0 of the APerNoteEvent translator vtable 0x106d24b48 (ctor 0x1026edc20; registration 0x1026ed900 '
            'names mTimeOffset +0x30 ... mCurveControl2Y +0x58); same rounding sequence and constants'},
    {'x86': 0x10150f7a0, 'arm64': 0x101520dbc, 'role': 'Double member text writer (static reference only)',
     'how': 'sole x86 reference to "#%16.16llX"; DBL_MAX -> "Invalid"; finite -> 0x10142b960 -> 0x10142b980'},
    {'x86': 0x10150f6a0, 'arm64': 0x101520c70, 'role': 'Float member text writer (static reference only)',
     'how': 'sole x86 reference to "#%8.8X"; finite -> 0x10142b6a0 -> P = 9 writer'},
    {'x86': DOUBLE_WRITER, 'arm64': 0x101431788, 'role': 'writer text P = 17', 'how': 'X1 match'},
    {'x86': FLOAT_WRITER, 'arm64': 0x101431584, 'role': 'writer text P = 9', 'how': 'X1 match'},
    {'x86': MIDIKEY_GET, 'arm64': 0x1028aca40, 'role': 'KeyTrack MidiKey getter (returns int +0x40)',
     'how': 'called by the key-map rebuild x86 0x102a40980 = arm64 0x1028f5f74 (first call of the AMidiNotes post-load '
            'x86 0x102a40180 = arm64 0x1028f5864, sole x86 reference to "Note IDs are not unique")'},
    {'x86': 0x102a40980, 'arm64': 0x1028f5f74, 'role': 'key-map rebuild (static only)',
     'how': 'cltq; mov %r13,(%rbx,%rax,8) with rbx = this+0x28 = arm64 str x23,[x19,w0,SXTW #3]; no bound check'},
    {'x86': 0x102a3fce0, 'arm64': 0x1028f5420, 'role': 'key-map store/clear (static only)',
     'how': 'two getter calls each, stores at this+0x28+8*key without bound check in both'},
    {'x86': GRID, 'arm64': 0x101aaae44, 'role': 'grid length (signature, global value q)',
     'how': 'switch on q-1 <= 12 with the same cases (8/4/2/1 bar, 2, 4/3, 1, 2/3, 1/2, 1/3, 1/4, 1/6, 1/8) and the '
            'same lattice rounding of the bar; callers include the clip grid x86 0x1025612b0 = arm64 0x102442998'},
    {'x86': 0x1025612b0, 'arm64': 0x102442998, 'role': 'clip grid (static only)',
     'how': 'enum at [clip+0x258] via the enum getter, signature [clip+0x1d8] via 0x102815210 (= arm64 0x1026e3698, '
            'cvttss2si = fcvtzs), grid(sig, k-1); else song grid or -1.0 (0x105b35858)'},
    {'x86': 0x101af9eb0, 'arm64': 0x101ad0130, 'role': 'fire/boundary computation (static only)',
     'how': 'sole caller of the grid-choice function x86 0x101af9d50 = arm64 0x101acffa4 (sole caller 0x101ad0130); '
            'same inline lattice rounding of the current time [+0x70] and call of the boundary helper with mode 1'},
    {'x86': BOUNDARY, 'arm64': 0x101abf294, 'role': 'boundary helper: anchor max([entry+8], 0), then lattice helper',
     'how': 'called from 0x101afa59b with rdi = obj+0x38, esi = 1 exactly where arm64 0x101ad07c8 calls 0x101abf294; '
            'maxsd with 0 (arm64 fmaxnm), tail jump to the lattice helper'},
    {'x86': LATTICE, 'arm64': 0x1011be6c8, 'role': 'lattice helper (mode 0 round, 1 ceil, 2 floor, other none)',
     'how': 'tail target of the boundary helper; same mode tests, g == 0 skip, then the grid rounding'},
    {'x86': ENUM_GET, 'arm64': 0x1015661b8, 'role': 'ARemoteableEnum value getter',
     'how': 'called by both clip grid functions on [clip+0x258]; both return 0 for a stored -99'},
    {'x86': FA_POSTLOAD, 'arm64': 0x1025044b4, 'role': 'AFollowAction post-load (chance rescaling)',
     'how': 'slot +0xd0 of the AFollowAction vtable (x86 0x106d0dc08 stored by the ctor 0x10262b4b0, found through the '
            'symbolized CallMemberFunc<&AFollowAction::...> pointers; arm64 0x1067c8830); same members +0xf0, +0x108, +0x120'},
    {'x86': 0x10262b4b0, 'arm64': 0x102505030, 'role': 'AFollowAction ctor (static reference; not run: needs the '
     'class registries)', 'how': 'stores vtable 0x106d0dc08, builds FollowTime/IsLinked/LoopIterations/A/B/chances/'
     'jump indices with the same values as arm64'},
    {'x86': 0x10262bc20, 'arm64': 0x102505724, 'role': 'follow-action member builder (static reference)',
     'how': 'label list No Action ... Jump; UserFloat init (0, 100, default) and (-1, 8388608, 1)'},
    {'x86': 0x102630f80, 'arm64': None, 'role': 'CallMemberFunc<&AFollowAction::FollowChanceController> (static only)',
     'how': 'symbol name in the x86 corpus; rounds the value (roundf) and sets the other chance to 100 - it'},
    {'x86': 0x102630f60, 'arm64': None, 'role': 'CallMemberFunc<&AFollowAction::FollowTimeController> (static only)',
     'how': 'symbol name in the x86 corpus; max(0.25, v), then the double setter'},
    {'x86': UF_INIT, 'arm64': 0x10157432c, 'role': 'UserFloat init (bounds, mapping, default, callback)',
     'how': 'called by the member builder with (0, 100, default) as arm64 0x102505724 calls 0x10157432c'},
    {'x86': UF_SETTER, 'arm64': 0x10157478c, 'role': 'UserFloat vtable +0x280 setter',
     'how': 'slot +0x280 of the UserFloat vtable (x86 0x106bc35b0 from factory 0x101564c00; arm64 0x106680438 from '
            '0x1015740f0); both map min and max through [+0x78] slot +0x30 and clamp'},
    {'x86': MAPPING_CTOR, 'arm64': None, 'role': 'value-mapping ctor used by the AFollowAction ctor for the chances',
     'how': 'called by 0x10262b4b0 as (0, 100, 1, 1, obj); slot +0x30 0x1015665a0 returns x unchanged when its '
            '(+0x28, +0x2c) equal the bounds passed'},
    {'x86': RD_POSTLOAD, 'arm64': 0x10156580c, 'role': 'ARemoteableDouble post-load: grid rounding when flag +0x70',
     'how': 'slot +0xd0 of the ARemoteableDouble vtable (x86 0x106bc07b0 from 0x101555070; arm64 0x10667d7e8)'},
    {'x86': 0x101555660, 'arm64': 0x101565624, 'role': 'ARemoteableDouble set-quantize flag (static reference)',
     'how': 'AFollowAction ctor calls it with (FollowTime, 1, 1) in both slices'},
]

FLT_MAX = 3.4028234663852886e38
DBL_MAX = sys.float_info.max
N = 3843840
H = 1 / N
SENT = (-1.7976931348623155e308, 1.7976931348623155e308, DBL_MAX, math.inf)


# ---- batching ------------------------------------------------------------------------------------
class Batch:
    """One loader process: call tokens with buffer numbering tracked. At most 250 calls and buffers."""

    def __init__(self, setup=()):
        self.toks, self.nbuf, self.ncall = [], 0, 0
        for addr, args in setup:
            self.call(addr, args)

    def call(self, addr, args=()):
        bufs = []
        for a in args:
            if a.split(':')[0] in ('buf', 'hex', 'str'):
                bufs.append(self.nbuf)
                self.nbuf += 1
        self.toks += ['call', hex(addr), *args]
        self.ncall += 1
        assert self.ncall <= 250 and self.nbuf <= 250
        return self.ncall - 1, bufs

    def poke(self, where, value):
        self.toks += ['poke', where, value]

    def dump(self, expr, n):
        self.toks += ['dump', expr, str(n)]

    def run(self, skip=None):
        res = R.run(self.toks, skip=skip)
        if not res.ok:
            raise RuntimeError(f'run failed: trap={res.trap} fault={res.fault} rc={res.rc}\n{res.stderr[-2000:]}')
        return res


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def bits64(x):
    return struct.unpack('<Q', struct.pack('<d', x))[0]


def bits32(x):
    return struct.unpack('<I', struct.pack('<f', x))[0]


def jnum(x):
    """JSON-safe number with its exact bits."""
    if isinstance(x, float):
        return {'v': x if math.isfinite(x) else str(x), 'hex': x.hex() if math.isfinite(x) else str(x),
                'bits': f'{bits64(x):#018x}'}
    return x


def jf32(x):
    return {'v': x if math.isfinite(x) else str(x), 'bits32': f'{bits32(x):#010x}'}


# ---- models (harness arithmetic, used only to compare) -------------------------------------------
def grid_round(x):
    """REQ-MIDI-NOTE-STORAGE-006 read as binary64 operations (the spec formula)."""
    if x in SENT:
        return x
    s = 1.0 if x >= 0 else -1.0
    y = abs(x + (H * s) * 0.5) * N
    if not math.isfinite(y):
        return (y / N) * s if not math.isnan(y) else y
    return (float(math.floor(y)) / N) * s


def grid_round_exact(x):
    """Nearest multiple of 1/N, halves away from zero, exact; then the nearest binary64."""
    if not math.isfinite(x) or x in SENT:
        return x
    q = Fraction(x) * N
    k = math.floor(abs(q) + Fraction(1, 2))
    return float(Fraction(k if q >= 0 else -k, N)) if k else (0.0 if q >= 0 else -0.0)


# ---- target a: notes -----------------------------------------------------------------------------
NOTE_BASE = {'time': 0.0, 'dur': 0.25, 'vel': 85.0, 'veldev': 0.0, 'offvel': 64.0, 'prob': 1.0}
F32_ABOVE_127 = struct.unpack('<f', struct.pack('<I', bits32(127.0) + 1))[0]
F32_BELOW_1 = struct.unpack('<f', struct.pack('<I', bits32(1.0) - 1))[0]
F32_ABOVE_1 = struct.unpack('<f', struct.pack('<I', bits32(1.0) + 1))[0]
NAN = float('nan')

NOTE_VECTORS = [
    ('MNS-001 n1', {}),
    ('MNS-014 n1', {'vel': 0.0}), ('MNS-014 n2', {'vel': 300.0}), ('MNS-014 n3', {'vel': 0.5}),
    ('MNS-015 n1', {'offvel': -5.0}), ('MNS-015 n2', {'offvel': 200.0}),
    ('MNS-016 n1', {'prob': 1.5}), ('MNS-016 n2', {'prob': -1.0}),
    ('MNS-017 n1', {'dur': -2.0}), ('MNS-017 n2', {'dur': DBL_MAX}),
    ('MNS-018 n1', {'time': -3.0, 'veldev': -500.0}),
    ('MNS-019 n1', {'vel': 80.578949}), ('MNS-019 n2', {'vel': 33.3}),
    ('MNS-020 n1', {'time': 0.123456789, 'dur': 0.3333333333}),
    ('MNS-021 n1', {'time': -0.0000002}),
    ('MNS-022 n1', {'time': 0.00000013}), ('MNS-022 n3', {'dur': 0.000000131}),
    ('MNS-023 n1', {'time': -0.0000001}),
    ('MNS-024 n2', {'time': DBL_MAX}),
    ('MNS-025', {'time': 20.0, 'dur': 0.0}),
    ('MNS-067 n3', {'time': 0.5}),
    # boundaries and specials beyond the cases
    ('vel 1', {'vel': 1.0}), ('vel 127', {'vel': 127.0}), ('vel below 1', {'vel': F32_BELOW_1}),
    ('vel above 127', {'vel': F32_ABOVE_127}), ('vel -0', {'vel': -0.0}), ('vel +inf', {'vel': math.inf}),
    ('vel -inf', {'vel': -math.inf}), ('vel nan', {'vel': NAN}), ('vel denormal', {'vel': 1e-45}),
    ('offvel 0', {'offvel': 0.0}), ('offvel -0', {'offvel': -0.0}), ('offvel 127', {'offvel': 127.0}),
    ('offvel above 127', {'offvel': F32_ABOVE_127}), ('offvel -denormal', {'offvel': -1e-45}),
    ('offvel +inf', {'offvel': math.inf}), ('offvel nan', {'offvel': NAN}),
    ('prob 0', {'prob': 0.0}), ('prob above 1', {'prob': F32_ABOVE_1}), ('prob -0', {'prob': -0.0}),
    ('prob nan', {'prob': NAN}),
    ('dur 0', {'dur': 0.0}), ('dur -0', {'dur': -0.0}), ('dur -denormal', {'dur': -5e-324}),
    ('dur 1.7976931348623155e308', {'dur': 1.7976931348623155e308}), ('dur +inf', {'dur': math.inf}),
    ('dur -inf', {'dur': -math.inf}), ('dur nan', {'dur': NAN}),
    ('time -1.7976931348623155e308', {'time': -1.7976931348623155e308}),
    ('time 1.7976931348623155e308', {'time': 1.7976931348623155e308}), ('time +inf', {'time': math.inf}),
    ('time -inf', {'time': -math.inf}), ('time nan', {'time': NAN}), ('time -0', {'time': -0.0}),
    ('time -1/N', {'time': -H}), ('time 352', {'time': 352.0}), ('time 1e9+0.3', {'time': 1e9 + 0.3}),
    ('time 2^40+0.3', {'time': 2.0 ** 40 + 0.3}),
]


def near_tie_times():
    """Binary64 values at and next to the exact halfway points (k + 1/2)/N, for several k."""
    out = []
    for k in (0, 1, 7, 1000, N * 4 + 1, N * 100 + 5, N * 1000 + 5):
        mid = float(Fraction(2 * k + 1, 2 * N))
        for d in (-3, -1, 0, 1, 3):
            x = mid
            for _ in range(abs(d)):
                x = math.nextafter(x, math.inf if d > 0 else -math.inf)
            out.append((f'tie k={k} {d:+d}ulp', {'time': x}))
            out.append((f'tie k={k} {d:+d}ulp neg', {'time': -x}))
    return out


def note_bytes(v):
    b = bytearray(0x60)
    struct.pack_into('<d', b, 0x30, v['time'])
    struct.pack_into('<d', b, 0x38, v['dur'])
    struct.pack_into('<ffff', b, 0x40, v['vel'], v['veldev'], v['offvel'], v['prob'])
    b[0x50] = 1
    struct.pack_into('<q', b, 0x58, 7)
    return bytes(b)


def note_fields(b):
    t, d = struct.unpack_from('<dd', b, 0x30)
    vel, vd, ov, pr = struct.unpack_from('<ffff', b, 0x40)
    return {'time': t, 'dur': d, 'vel': vel, 'veldev': vd, 'offvel': ov, 'prob': pr}


def notes():
    vecs = [(lbl, {**NOTE_BASE, **ch}) for lbl, ch in NOTE_VECTORS + near_tie_times()]
    rows = []
    for part in chunks(vecs, 120):
        b = Batch()
        idx = []
        for lbl, v in part:
            _, (nb,) = b.call(NOTE_LIMITS, ['hex:' + note_bytes(v).hex()])
            _, (ob,) = b.call(NOTE_GRID, [f'ref:b{nb}+0x28', 'buf:48'])
            idx.append((lbl, v, nb, ob))
        res = b.run()
        for lbl, v, nb, ob in idx:
            lim = note_fields(res.outs[nb])
            t_q, d_q = struct.unpack_from('<dd', res.outs[ob], 0)
            rest = struct.unpack_from('<ffff', res.outs[ob], 0x10)
            rows.append({'label': lbl, 'input': {k: (jnum(x) if k in ('time', 'dur') else jf32(f32(x)))
                                                 for k, x in v.items()},
                         'after_limits': {k: (jnum(x) if k in ('time', 'dur') else jf32(x)) for k, x in lim.items()},
                         'held_time': jnum(t_q), 'held_duration': jnum(d_q),
                         'copied_vel_veldev_offvel_prob': [jf32(x) for x in rest],
                         'spec_formula_time': jnum(grid_round(lim['time'])),
                         'spec_formula_duration': jnum(grid_round(lim['dur'])),
                         'exact_half_away_time': jnum(grid_round_exact(lim['time'])),
                         'formula_equals_x': bits64(grid_round(lim['time'])) == bits64(t_q)
                         and bits64(grid_round(lim['dur'])) == bits64(d_q),
                         'exact_equals_x_time': bits64(grid_round_exact(lim['time'])) == bits64(t_q)})
    # per-note event TimeOffset (MNS-069 and neighbours)
    ev_in = [0.123456789, 0.0625, 0.125, DBL_MAX, -0.1, 0.0, -0.0000001, 0.25, 66.66]
    # the function's this is the translator subobject at event + 0x28 (it reads this+8 = TimeOffset)
    b = Batch()
    idx = []
    for x in ev_in:
        e = bytearray(0x60)
        struct.pack_into('<df', e, 0x30, x, 100.0)
        struct.pack_into('<dddd', e, 0x40, 0.5, 0.2, 0.5, 0.5)
        _, (eb,) = b.call(0x1002c4280, ['hex:' + bytes(e).hex()])          # no-op: only allocates the buffer
        _, (ob,) = b.call(EVENT_GRID, [f'ref:b{eb}+0x28', 'buf:64'])
        idx.append((x, eb, ob))
    res = b.run()
    events = []
    for x, eb, ob in idx:
        t_q, = struct.unpack_from('<d', res.outs[ob], 0)
        val, = struct.unpack_from('<f', res.outs[ob], 8)
        curves = struct.unpack_from('<dddd', res.outs[ob], 0x10)
        events.append({'input_time_offset': jnum(x), 'held_time_offset': jnum(t_q), 'value': val,
                       'curves': list(curves), 'spec_formula': jnum(grid_round(x)),
                       'formula_equals_x': bits64(grid_round(x)) == bits64(t_q)})
    # writer text of held values (finite, not DBL_MAX: the member writers 0x10150f7a0 / 0x10150f6a0 route those
    # to "#..." and "Invalid" without the formatter)
    dvals, fvals = [], []
    for r in rows:
        if not r['label'].startswith(('MNS', 'time -0', 'dur -0')):
            continue
        for key in ('held_time', 'held_duration'):
            x = float.fromhex(r[key]['hex']) if r[key]['hex'] not in ('inf', '-inf', 'nan') else None
            if x is not None and x != DBL_MAX and x not in dvals:
                dvals.append(x)
        for k in ('vel', 'offvel', 'prob', 'veldev'):
            x = r['after_limits'][k]['v']
            if isinstance(x, float) and x not in fvals:
                fvals.append(x)
    dvals += [x for x in (0.1, 0.2) if x not in dvals] + [0.0, -0.0]
    texts = writer_texts([('double', x) for x in dvals] + [('float', x) for x in fvals + [-0.0]])
    # MidiKey getter: the value stored at +0x40 reaches the key-map store unchanged
    b = Batch()
    idx = []
    for key in (36, 0, 127, 128, 129, -1, -5, 2 ** 31 - 1):
        kt = bytearray(0x48)
        struct.pack_into('<i', kt, 0x40, key)
        c, _ = b.call(MIDIKEY_GET, ['hex:' + bytes(kt).hex()])
        idx.append((key, c))
    res = b.run()
    keys = [{'stored': k, 'getter': struct.unpack('<i', struct.pack('<I', res.calls[c]['rax'] & 0xffffffff))[0],
             'map_slot_offset_from_object': hex(0x28 + 8 * k)} for k, c in idx]
    return {'notes': rows, 'events': events, 'writer_texts': texts, 'midikey_getter': keys}


def writer_texts(items):
    out = []
    for part in chunks(items, 120):
        b = Batch([(INIT_EMPTY_STRING, [])])
        idx = []
        for kind, x in part:
            _, (sb,) = b.call(DOUBLE_WRITER if kind == 'double' else FLOAT_WRITER, ['buf:8', dbl(x)])
            b.dump(f'b{sb}*+16', f'b{sb}*+4@')
            idx.append((kind, x, sb))
        res = b.run()
        dumps = {e: d for e, _, d in res.dumps}
        for kind, x, sb in idx:
            out.append({'kind': kind, 'value': jnum(x), 'text': ustr(dumps[f'b{sb}*+16'])})
    return out


# ---- target b: launch grid -----------------------------------------------------------------------
SIGS = [(n, d) for d in (1, 2, 4, 8, 16) for n in range(1, 100)]
GRID_NOTE = {5: Fraction(2), 6: Fraction(4, 3), 7: Fraction(1), 8: Fraction(2, 3), 9: Fraction(1, 2),
             10: Fraction(1, 3), 11: Fraction(1, 4), 12: Fraction(1, 6), 13: Fraction(1, 8)}
SPEC_GRID_LITERAL = {6: 4 / 3, 8: 2 / 3, 10: 1 / 3, 12: 1 / 6}


def spec_grid(q, n, d):
    """REQ-CLIP-LAUNCH-015: bar = 4n/d rounded to the lattice; 8, 4, 2, 1 bars; note values; else 0."""
    if 1 <= q <= 4:
        bar = grid_round((n / d) * 4.0)
        return {1: bar * 8.0, 2: bar * 4.0, 3: bar + bar, 4: bar}[q]
    if q in GRID_NOTE:
        return float(GRID_NOTE[q])
    return 0.0


def launch():
    # grid lengths: every valid signature x q 1..13, plus out-of-range q on four signatures
    jobs = [(n, d, q) for (n, d) in SIGS for q in range(1, 14)]
    jobs += [(n, d, q) for (n, d) in ((4, 4), (3, 4), (6, 8), (7, 8)) for q in (-99, -2, -1, 0, 14, 15, 100)]
    grid = []
    for part in chunks(jobs, 240):
        b = Batch()
        b.call(0x1002c4280, ['buf:8'])
        idx = []
        for n, d, q in part:
            b.poke('b0', f'{(d << 32) | n:#x}')
            c, _ = b.call(GRID, ['ref:b0', f'i:{q & 0xffffffff}'])
            idx.append((n, d, q, c))
        res = b.run()
        for n, d, q, c in idx:
            g = as_f64(res.calls[c]['xmm0'])
            sg = spec_grid(q, n, d)
            grid.append({'n': n, 'd': d, 'q': q, 'x': g.hex(), 'spec': sg.hex(), 'equal': bits64(g) == bits64(sg)})
    g_of = {(r['n'], r['d'], r['q']): float.fromhex(r['x']) for r in grid}

    # lattice rounding of a press time, then the boundary with anchor a and grid g (mode 1 = ceiling)
    cases = []

    def case(label, t, g, a=0.0, explicit=False):
        cases.append({'label': label, 't': t, 'g': g, 'a': a, 'explicit': explicit})

    for t in (1.5, 3.9, 3.99, 4.0, 4 - H, 4 - H / 2, 4 + H / 2, 4 + 0.49 * H, 4 + H, 4 - 1e-9, 4 + 1e-9):
        case(f'PRB-S5-01 4/4 1 Bar t={t!r}', t, g_of[4, 4, 4])
    grid_cases = [('CLC-031', 5.3, (4, 4, 4)), ('CLC-032', 9, (4, 4, 3)), ('CLC-033', 17, (4, 4, 2)),
                  ('CLC-034', 1, (4, 4, 1)), ('CLC-035', 4, (3, 4, 4)), ('CLC-036', 1, (3, 4, 1)),
                  ('CLC-037', 1, (6, 8, 4)), ('CLC-038', 4, (7, 8, 4)), ('CLC-039', 1, (5, 4, 3)),
                  ('CLC-040', 2.25, (4, 4, 5)), ('CLC-041', 1.5, (4, 4, 6)), ('CLC-042', 2.1, (4, 4, 7)),
                  ('CLC-043', 1, (4, 4, 8)), ('CLC-044', 3.1, (4, 4, 9)), ('CLC-045', 0.4, (4, 4, 10)),
                  ('CLC-046', 1.3, (4, 4, 11)), ('CLC-047', 0.2, (4, 4, 12)), ('CLC-048', 0.13, (4, 4, 13)),
                  ('CLC-049', 2.1, (4, 4, 7)), ('CLC-050a', 1.2, (6, 8, 4)), ('CLC-050b', 4.2, (6, 8, 4)),
                  ('CLC-051', 1.2, (4, 4, 4))]
    for lbl, t, key in grid_cases:
        case(lbl, float(t), g_of[key])
    case('CLC-055 anchor 8, 3/4 1 Bar, t=9', 9.0, g_of[3, 4, 4], a=8.0)
    case('anchor -5 (clamped to 0), 1 Bar, t=5.3', 5.3, g_of[4, 4, 4], a=-5.0)
    case('anchor 8.0000001 (off lattice), 3/4 1 Bar, t=9', 9.0, g_of[3, 4, 4], a=8.0000001)
    case('1/8T, explicit time 1.0000001 (not lattice-rounded)', 1.0000001, g_of[4, 4, 10], explicit=True)
    # every grid line of the triplet and note grids up to beat 64, on the lattice, and one lattice step either side
    sweep = []
    for q in (5, 6, 7, 8, 9, 10, 11, 12, 13):
        gx = g_of[4, 4, q]
        k = 1
        while GRID_NOTE[q] * k <= 64:
            line = Fraction(GRID_NOTE[q] * k)
            for step in (-1, 0, 1):
                t = float(line + Fraction(step, N))
                sweep.append({'q': q, 'k': k, 'step': step, 't': t, 'g': gx, 'a': 0.0, 'explicit': False,
                              'exact_first_line': float(line if step <= 0 else line + GRID_NOTE[q])})
            k += 1
    allc = cases + sweep
    for part in chunks(allc, 120):
        b = Batch()
        b.call(0x1002c4280, ['buf:16'])
        idx = []
        for c in part:
            c1, _ = b.call(LATTICE, ['i:3', dbl(c['t']), dbl(1.0), dbl(0.0)])
            idx.append(c1)
        res1 = b.run()
        tl = [as_f64(res1.calls[i]['xmm0']) for i in idx]
        b = Batch()
        b.call(0x1002c4280, ['buf:16'])
        idx = []
        for c, t_l in zip(part, tl):
            c['t_lattice'] = t_l
            tt = c['t'] if c['explicit'] else t_l
            b.poke('b0+8', f'{bits64(c["a"]):#x}')
            c2, _ = b.call(BOUNDARY, ['ref:b0', dbl(tt), dbl(c['g']), 'i:1'])
            idx.append(c2)
        res2 = b.run()
        for c, i in zip(part, idx):
            c['B'] = as_f64(res2.calls[i]['xmm0'])
            tt = c['t'] if c['explicit'] else c['t_lattice']
            a = max(c['a'], 0.0)
            c['model_B'] = grid_round(a + math.ceil((tt - a) / c['g']) * c['g'])
    out_cases = [{**{k: (jnum(v) if isinstance(v, float) else v) for k, v in c.items()},
                  'model_equals_x': bits64(c['B']) == bits64(c['model_B'])} for c in cases]
    sweep_out = []
    for c in sweep:
        sweep_out.append({'q': c['q'], 'k': c['k'], 'step': c['step'], 't': c['t'].hex(),
                          't_lattice': c['t_lattice'].hex(), 'B': c['B'].hex(),
                          'exact_first_line': c['exact_first_line'].hex(),
                          'equals_exact': bits64(c['B']) == bits64(c['exact_first_line']),
                          'model_equals_x': bits64(c['B']) == bits64(c['model_B'])})
    # enum getter: the value a clip-grid or song-grid caller receives for a stored enum index
    b = Batch()
    b.call(0x1002c4280, ['buf:232'])
    idx = []
    for v in (-99, -100, -98, -1, 0, 1, 14, 15, 2 ** 31 - 1, -2 ** 31):
        b.poke('b0+216', f'{v & 0xffffffff:#x}')
        c, _ = b.call(ENUM_GET, ['ref:b0'])
        idx.append((v, c))
    res = b.run()
    enum = [{'stored': v, 'getter': struct.unpack('<i', struct.pack('<I', res.calls[c]['rax'] & 0xffffffff))[0]}
            for v, c in idx]
    return {'grid': grid, 'boundary_cases': out_cases, 'gridline_sweep': sweep_out, 'enum_getter': enum}


# ---- target c: follow action ---------------------------------------------------------------------
def userfloat(b, lo, hi, default, value, mapbuf, cbbuf):
    """A UserFloat object as the AFollowAction ctor builds a chance: vtables, refcount, the real init with the
    ctor's mapping and callback, then the loaded value stored into +0x58 as the generic loader does."""
    o = bytearray(0x90)
    struct.pack_into('<QI', o, 0, UF_VTABLE, 1)
    struct.pack_into('<Q', o, 0x70, UF_VTABLE2)
    _, (ob,) = b.call(0x1002c4280, ['hex:' + bytes(o).hex()])
    b.call(UF_INIT, [flt(lo), flt(hi), flt(default), f'ref:b{ob}', f'ref:b{mapbuf}', f'ref:b{cbbuf}'])
    b.call(RAW_FLOAT_STORE, [f'ref:b{ob}', flt(value)])
    return ob


FA_CASES = [('CLC-019', 30, 30, False), ('CLC-020', 0, 0, True), ('CLC-021', 1, 7, False),
            ('CLC-022', 1, 2, False), ('REQ-012 example 1/0', 1, 0, False), ('0/1', 0, 1, False),
            ('100/0 (shipped)', 100, 0, False), ('0/100', 0, 100, False), ('50/50', 50, 50, False),
            ('33/67', 33, 67, False), ('3/5 (37.5)', 3, 5, False), ('5/3 (62.5)', 5, 3, False),
            ('7/1 (87.5)', 7, 1, False), ('1/199 (0.5)', 1, 199, False), ('1/3', 1, 3, False),
            ('2/1', 2, 1, False), ('old fractions 1/0', 1.0, 0.0, False), ('old fractions 0.25/0.75', 0.25, 0.75, False),
            ('old fractions 0.5/0.5', 0.5, 0.5, False), ('-0/0', -0.0, 0.0, True),
            ('CLC-023 150/50', 150, 50, False), ('-10/50', -10, 50, False), ('150/-50', 150, -50, False),
            ('-10/-10', -10, -10, False), ('200/200', 200, 200, False), ('100/100', 100, 100, False),
            ('1e-3/0', 1e-3, 0, False), ('99.5/0.5', 99.5, 0.5, False)]


def rescale_model(a, b):
    """REQ-CLIP-LAUNCH-012 in binary32: A' = round(A / ((A + B) / 100)), B' = 100 - A' (before the setter clamp)."""
    a, b = f32(a), f32(b)
    if a == 0 and b == 0:
        return 100.0, None
    s = f32(f32(a + b) / 100.0)
    q = f32(a / s)
    r = math.floor(abs(q) + 0.5) * (1 if q >= 0 else -1) if math.isfinite(q) else q
    return float(r), f32(100.0 - r)


def follow():
    rows = []
    for lbl, a, bb, enabled in FA_CASES:
        b = Batch()
        _, (mb,) = b.call(0x1002c4280, ['buf:56'])
        b.call(MAPPING_CTOR, [flt(0), flt(100), flt(1), flt(1), f'ref:b{mb}'])
        _, (cb,) = b.call(0x1002c4280, ['hex:' + struct.pack('<QQ', FA_NOTIFY, 0).hex()])
        ab = userfloat(b, 0, 100, 100, a, mb, cb)
        bbuf = userfloat(b, 0, 100, 0, bb, mb, cb)
        _, (eb,) = b.call(0x1002c4280, ['buf:104'])
        _, (fa,) = b.call(0x1002c4280, ['buf:320'])
        b.poke(f'b{fa}+0xf0', f'b{ab}')
        b.poke(f'b{fa}+0x108', f'b{bbuf}')
        b.poke(f'b{fa}+0x120', f'b{eb}')
        first = b.ncall
        b.call(FA_POSTLOAD, [f'ref:b{fa}'])
        b.dump(f'b{ab}+0x58', 4)
        b.dump(f'b{bbuf}+0x58', 4)
        res = b.run(skip={BOOL_SET: ['$rdi', '$esi'], FA_NOTIFY: ['$rdi', '$rsi', '$edx']})
        d = [struct.unpack('<f', x)[0] for _, _, x in res.dumps]
        hits = [(k, addr, vals) for k, addr, vals in res.hits if k >= first]
        names = {BOOL_SET: 'FollowActionEnabled setter', FA_NOTIFY: 'NotifyListeners callback'}
        events = [{'call': names[addr], 'int_arg': hex(vals[-1]),     # BOOL_SET: esi; FA_NOTIFY: edx
                   'object': 'A' if addr == FA_NOTIFY and vals[1] == res_buf_addr(res, ab) else
                   'B' if addr == FA_NOTIFY and vals[1] == res_buf_addr(res, bbuf) else
                   'enabled' if addr == BOOL_SET else '?'} for _, addr, vals in hits]
        ma, mbv = rescale_model(a, bb)
        rows.append({'label': lbl, 'loaded': [jf32(f32(a)), jf32(f32(bb))], 'held_after_postload': [d[0], d[1]],
                     'rescaled_before_setter_model': [ma, mbv], 'events': events,
                     'enabled_set_false': any(e['call'] == names[BOOL_SET] and e['int_arg'] == '0x0'
                                              for e in events)})
    # follow time: ARemoteableDouble post-load with the quantize flag set (as the AFollowAction ctor sets it)
    vals = [4.0, 2.0000001, 3.0000002, 1e-8, 0.0, -0.0, -0.3, -5.0, 999999.9999999, 1e6, 2e6, 1e15 + 0.3,
            DBL_MAX, math.inf, 0.1]
    for k in (0, 1, 7, N * 4 + 1, N * 1000 + 5, N * 100000 + 5):
        mid = float(Fraction(2 * k + 1, 2 * N))
        vals += [math.nextafter(mid, -math.inf), mid, math.nextafter(mid, math.inf)]
    ft = []
    for flag in (1, 0):
        for part in chunks(vals, 100):
            b = Batch()
            o = bytearray(0x78)
            struct.pack_into('<QI', o, 0, RD_VTABLE, 1)
            o[0x70] = flag
            _, (ob,) = b.call(0x1002c4280, ['hex:' + bytes(o).hex()])
            for x in part:
                b.poke(f'b{ob}+0x58', f'{bits64(x):#x}')
                b.call(RD_POSTLOAD, [f'ref:b{ob}'])
                b.dump(f'b{ob}+0x58', 8)
            res = b.run(skip={GENERIC_POSTLOAD: ['$rdi']})
            for x, (_, _, raw) in zip(part, res.dumps):
                y = struct.unpack('<d', raw)[0]
                ft.append({'flag': flag, 'input': jnum(x), 'held': jnum(y),
                           'spec_formula': jnum(grid_round(x) if flag else x),
                           'exact_half_away': jnum(grid_round_exact(x) if flag else x),
                           'formula_equals_x': bits64(grid_round(x) if flag else x) == bits64(y),
                           'exact_equals_x': bits64(grid_round_exact(x) if flag else x) == bits64(y)})
            assert len([h for h in res.hits if h[1] == GENERIC_POSTLOAD]) == len(part)
    return {'chances': rows, 'follow_time': ft}


def res_buf_addr(res, k):
    """Address of buffer k in a run (from the 'out bK ADDR' lines)."""
    for line in res.stdout.splitlines():
        f = line.split()
        if len(f) > 2 and f[0] == 'out' and f[1] == f'b{k}':
            return int(f[2], 16)
    return None


# ---- evidence files ------------------------------------------------------------------------------
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
                    c = data[p]; p += 1; v |= (c & 0x7f) << sh; sh += 7
                    if not c & 0x80:
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


EXTRA_DISASM = [0x102a2aaf0, 0x102a2ab70, 0x102a2ab90, 0x10142b960, 0x101565160, 0x101558b90, 0x101558c60,
                0x1015665a0, 0x10154dfb0, 0x10154e240, 0x10147a210, 0x101559950, 0x101555660, 0x10155ef70,
                0x101558d20, 0x101558be0]


def rows_json(d):
    """JSON object with one list row per line (the files hold thousands of rows)."""
    parts = []
    for k, v in d.items():
        if isinstance(v, list):
            body = ',\n  '.join(json.dumps(x) for x in v)
            parts.append(f' {json.dumps(k)}: [\n  {body}\n ]')
        else:
            parts.append(f' {json.dumps(k)}: {json.dumps(v)}')
    return '{\n' + ',\n'.join(parts) + '\n}\n'


def main():
    results = {}
    for name, fn in (('notes', notes), ('launch', launch), ('follow', follow)):
        first = len(R.log)
        results[name] = fn()
        used = {}
        for _, res in R.log[first:]:
            for sym, n in res.used.items():
                used[sym] = used.get(sym, 0) + n
        results[name]['replaced_imports_called'] = dict(sorted(used.items()))
        results[name]['runs'] = {'count': len(R.log) - first, 'not_ok': sum(not r.ok for _, r in R.log[first:])}
    (HERE / 'results').mkdir(exist_ok=True)
    for k, v in results.items():
        (HERE / 'results' / f'{k}.json').write_text(rows_json(v))
    (HERE / 'raw').mkdir(exist_ok=True)
    with open(HERE / 'raw' / 'runs.jsonl', 'w') as f:
        for argv, res in R.log:
            f.write(json.dumps({'argv': argv, 'rc': res.rc, 'stdout': res.stdout, 'stderr': res.stderr,
                                'timeout': res.timeout, 'gdb_script': res.gdb_script}) + '\n')
    (HERE / 'addresses.json').write_text(json.dumps(
        {'slice': SLICE, 'image_base': '0x100000000',
         'functions': [{**m, 'x86': hex(m['x86']), 'arm64': m['arm64'] and hex(m['arm64'])} for m in MATCHES]},
        indent=1) + '\n')
    (HERE / 'x86-disasm.txt').write_text(disassemble(SLICE, [m['x86'] for m in MATCHES] + EXTRA_DISASM))
    inputs = {'note_vectors': [{'label': l, **{k: jnum(float(x)) for k, x in {**NOTE_BASE, **v}.items()}}
                               for l, v in NOTE_VECTORS + near_tie_times()],
              'follow_action_chances': [{'label': l, 'A': a, 'B': b, 'enabled_initially': e} for l, a, b, e in FA_CASES],
              'grid': 'every (n, d) with n 1..99, d in 1, 2, 4, 8, 16 and q 1..13; q -99, -2, -1, 0, 14, 15, 100 '
                      'on 4/4, 3/4, 6/8, 7/8',
              'boundary': 'the boundary_cases and gridline_sweep inputs in results/launch.json (t, g, a)',
              'follow_time': 'results/follow.json follow_time inputs, flag 1 and 0'}
    (HERE / 'inputs.json').write_text(rows_json(inputs))
    imp = R.run(['--imports'])
    (HERE / 'imports.txt').write_text(imp.stdout)
    summarize(results)


def summarize(r):
    n = r['notes']['notes']
    print(f"notes: {len(n)} vectors; spec formula = X for {sum(x['formula_equals_x'] for x in n)}/{len(n)}; "
          f"exact half-away = X (time) for {sum(x['exact_equals_x_time'] for x in n)}/{len(n)}")
    for x in n:
        if x['label'].startswith('MNS') or not x['formula_equals_x']:
            al = x['after_limits']
            print(f"  {x['label']}: limits vel {al['vel']['v']} offvel {al['offvel']['v']} prob {al['prob']['v']} "
                  f"dur {al['dur']['v']}; held time {x['held_time']['v']} dur {x['held_duration']['v']}")
    for x in n:
        if not x['label'].startswith(('MNS', 'tie')):
            al = x['after_limits']
            print(f"  {x['label']}: -> vel {al['vel']['bits32']} offvel {al['offvel']['bits32']} prob "
                  f"{al['prob']['bits32']} dur {al['dur']['hex']} time held {x['held_time']['hex']}")
    ties = [x for x in n if x['label'].startswith('tie')]
    print(f"  near-tie times: formula = X {sum(x['formula_equals_x'] for x in ties)}/{len(ties)}; "
          f"exact = X {sum(x['exact_equals_x_time'] for x in ties)}/{len(ties)}")
    for x in ties:
        if not x['exact_equals_x_time']:
            print(f"    {x['label']}: X {x['held_time']['hex']} exact {x['exact_half_away_time']['hex']}")
    for e in r['notes']['events']:
        print(f"  event {e['input_time_offset']['v']} -> {e['held_time_offset']['v']} (formula = X {e['formula_equals_x']})")
    for t in r['notes']['writer_texts']:
        print(f"  text {t['kind']} {t['value']['v']!r} -> {t['text']!r}")
    print('  midikey getter:', [(k['stored'], k['getter']) for k in r['notes']['midikey_getter']])
    g = r['launch']['grid']
    print(f"launch grid: {len(g)} (n, d, q); spec table = X for {sum(x['equal'] for x in g)}/{len(g)}")
    for x in g:
        if not x['equal'] or (x['n'], x['d']) == (4, 4):
            print(f"  ({x['n']}/{x['d']}, q={x['q']}) X {float.fromhex(x['x'])} spec {float.fromhex(x['spec'])}")
    for c in r['launch']['boundary_cases']:
        print(f"  {c['label']}: t {c['t']['v']} -> lattice {c['t_lattice']['v']}; g {c['g']['v']}; B {c['B']['v']} "
              f"(model = X {c['model_equals_x']})")
    s = r['launch']['gridline_sweep']
    print(f"  grid-line sweep: {len(s)} presses; B = exact first line for {sum(x['equals_exact'] for x in s)}; "
          f"model = X for {sum(x['model_equals_x'] for x in s)}")
    for x in s:
        if not x['equals_exact']:
            print(f"    q={x['q']} k={x['k']} step={x['step']}: B {float.fromhex(x['B'])} "
                  f"exact {float.fromhex(x['exact_first_line'])}")
    print('  enum getter:', [(e['stored'], e['getter']) for e in r['launch']['enum_getter']])
    for c in r['follow']['chances']:
        print(f"follow {c['label']}: loaded {c['loaded'][0]['v']}/{c['loaded'][1]['v']} -> held "
              f"{c['held_after_postload'][0]}/{c['held_after_postload'][1]} (model before clamp "
              f"{c['rescaled_before_setter_model']}); enabled:=false {c['enabled_set_false']}; "
              f"notifications {[e['object'] for e in c['events'] if e['call'].startswith('Notify')]}")
    ft = r['follow']['follow_time']
    print(f"follow time: {len(ft)} runs; formula = X {sum(x['formula_equals_x'] for x in ft)}; "
          f"exact = X {sum(x['exact_equals_x'] for x in ft)}")
    for x in ft:
        if x['flag'] and (not x['exact_equals_x'] or x['input']['v'] in (2.0000001, 3.0000002, 1e-8, -0.3, -5.0, 2e6)):
            print(f"  {x['input']['v']!r} -> {x['held']['v']!r} (exact {x['exact_half_away']['v']!r})")
    for k, v in r.items():
        print(f"{k}: runs {v['runs']}; replaced imports called: {', '.join(v['replaced_imports_called']) or 'none'}")


if __name__ == '__main__':
    assert grid_round(0.123456789) == 0.12345675158175158
    assert grid_round_exact(-0.0000001) == -0.0 and math.copysign(1, grid_round(-0.0000001)) < 0
    assert rescale_model(1, 7) == (13.0, 87.0) and rescale_model(30, 30) == (50.0, 50.0)
    main()
