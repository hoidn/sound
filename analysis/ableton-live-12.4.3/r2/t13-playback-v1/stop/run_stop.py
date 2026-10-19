"""T1.3 stop timing: run original x86_64 Live 12.4.3 functions on the stop cases (ADR 0003, evidence label X).

usage: python3 -I -B run_stop.py        (from any directory; writes results/stop.json and raw/runs.jsonl here)

Functions (matching in matching.tsv; all pure arithmetic on registers and hand-built buffers, no pointers inside
buffers, so the unmodified tools/xexec loader is used, built to XEXEC_BIN below):
  GRID     0x101ad2ef0  ({int n, int d}*, int q) -> grid length in beats (X2 match; Engine
                        NQuantizationTypes::SQuantizationTime). The stop path calls it from 0x101af9d50
                        with the track fire manager's global quantization (static, matching.tsv).
  LATTICE  0x1011999d0  (int mode, double x, ...) mode 3 = the press-time rounding to 1/3,843,840 (X2).
  BOUNDARY 0x101ae8280  (entry*, double t, double g, int mode=1): anchor max([entry+8], 0), ceiling, lattice (X2).
  PASTEND  0x101b17510  (double now, double start, clip*, loop*) -> unlooped clip past its end
                        (Engine OClipTimeable::SIsPastEndOfUnloopedSlotClip).
  UNWEND   0x101b6c540  (TStatus*, double start, double secs) -> song beat of an unwarped clip's end
                        (Engine OUnwarpedClipTimeEvent::SBeatTimeForClipTime); calls 0x101ad8a60
                        (Engine OScheduler::TStatus::SecondsToBeats).
  FADEINIT 0x10227c780  default clip fade duration init (Engine OAudioClipFadeTime::SInitInstance).
  XFADE    0x102278eb0  (double tempo, OAudioClip* old, OAudioClip* new) -> crossfade/predelay in beats
                        (Engine OAudioClip::SCrossfadeDurBeat).
Models in this file are harness arithmetic used only for comparison. Depends on gcc, python3 and the slice.
"""
import json
import math
import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
os.environ.setdefault('XEXEC_BIN', '/var/tmp/sound-analysis/xexec-t13-stop/xexec')
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
import xexec  # noqa: E402
from xexec import as_f64, dbl  # noqa: E402

GRID, LATTICE, BOUNDARY = 0x101ad2ef0, 0x1011999d0, 0x101ae8280
PASTEND, UNWEND, FADEINIT, XFADE = 0x101b17510, 0x101b6c540, 0x10227c780, 0x102278eb0
NOOP = 0x1002c4280       # used by X2 only to allocate a buffer
DBL_MAX = sys.float_info.max
N = 3843840
R = xexec.Runner()
RUNS = []


def run(toks):
    res = R.run(toks)
    RUNS.append({'argv': [str(t) for t in toks], 'rc': res.rc, 'stdout': res.stdout, 'stderr': res.stderr})
    if not res.ok:
        raise RuntimeError(f'run failed: trap={res.trap} fault={res.fault}\n{res.stderr[-1500:]}')
    return res


def bits(x):
    return f'{struct.unpack("<Q", struct.pack("<d", x))[0]:#018x}'


def lattice_model(x):
    """REQ-CLIP-LAUNCH-013 formula (binary64 operations)."""
    s = 1.0 if x >= 0 else -1.0
    return s * (math.floor(abs(x + s * (1.0 / N) / 2) * N) / N)


# ---- a: stop boundary (grid, press rounding, boundary) ---------------------------------------
STOPS = [  # label, signature, global q, press beat, anchor
    ('STP-quantized 4/4 1 Bar t=5.3', (4, 4), 4, 5.3, 0.0),
    ('STP-quantized 4/4 1 Bar t=7.99', (4, 4), 4, 7.99, 0.0),
    ('STP-quantized 4/4 1 Bar t=7.996 (inside 0.006 of 8)', (4, 4), 4, 7.996, 0.0),
    ('STP-quantized 4/4 1 Bar t=8 exactly', (4, 4), 4, 8.0, 0.0),
    ('STP-quantized 4/4 2 Bars t=9', (4, 4), 3, 9.0, 0.0),
    ('STP-quantized 4/4 1/4 t=2.1', (4, 4), 7, 2.1, 0.0),
    ('STP-quantized 4/4 1/4T t=10/3', (4, 4), 8, 10 / 3, 0.0),
    ('STP-quantized 3/4 1 Bar t=4', (3, 4), 4, 4.0, 0.0),
    ('STP-quantized 4/4 1/16 t=1.3', (4, 4), 11, 1.3, 0.0),
    ('STP-quantized 4/4 None t=5.3', (4, 4), 0, 5.3, 0.0),
]


def stops():
    toks = ['call', hex(NOOP), 'buf:16']
    idx = []
    k = 1
    for _, (n, d), q, t, a in STOPS:
        toks += ['call', hex(GRID), 'hex:' + struct.pack('<ii', n, d).hex(), f'i:{q & 0xffffffff}']
        toks += ['call', hex(LATTICE), 'i:3', dbl(t), dbl(1.0), dbl(0.0)]
        idx.append((k, k + 1))
        k += 2
    res = run(toks)
    grids = [(as_f64(res.calls[g]['xmm0']), as_f64(res.calls[l]['xmm0'])) for g, l in idx]
    toks = ['call', hex(NOOP), 'buf:16']
    bidx = []
    k = 1
    for (lbl, sig, q, t, a), (g, tl) in zip(STOPS, grids):
        if g > 0:
            toks += ['call', hex(BOUNDARY), 'hex:' + struct.pack('<dd', 0.0, a).hex(), dbl(tl), dbl(g), 'i:1']
            bidx.append(k)
            k += 1
        else:
            bidx.append(None)
    res = run(toks)
    out = []
    for (lbl, sig, q, t, a), (g, tl), bi in zip(STOPS, grids, bidx):
        B = as_f64(res.calls[bi]['xmm0']) if bi is not None else tl
        mB = lattice_model(max(a, 0) + math.ceil((tl - max(a, 0)) / g) * g) if g > 0 else lattice_model(t)
        out.append({'label': lbl, 'sig': sig, 'q': q, 't': t, 'grid': g, 'grid_bits': bits(g),
                    't_lattice': tl, 't_lattice_model_equal': tl == lattice_model(t),
                    'B': B, 'B_bits': bits(B), 'B_model': mB, 'model_equal': B == mB,
                    'note': 'no grid: the stop is not moved to a grid line (B = t)' if g <= 0 else ''})
    return out


# ---- b: unlooped clip end (warped) ----------------------------------------------------------
def clip_buf(slot, start, loop_start, loop_end, looped, warped=1, fade=1, xin=0, fade_in=0.0, fade_out=0.0):
    """OClip/OAudioClip fields the stop path reads (Engine OClip::OClip / OAudioClip::OAudioClip message order):
    +0x2c SlotIndex, +0x38 Start, +0x40 LoopStart, +0x48 LoopEnd, +0x50 IsLooped, +0x58 IsWarped, +0xe0 Fade,
    +0xe1 IsCrossfadingIn, +0x100 FadeIn, +0x108 FadeOut."""
    b = bytearray(0x120)
    struct.pack_into('<i', b, 0x2c, slot)
    struct.pack_into('<ddd', b, 0x38, start, loop_start, loop_end)
    b[0x50], b[0x58], b[0xe0], b[0xe1] = looped, warped, fade, xin
    struct.pack_into('<dd', b, 0x100, fade_in, fade_out)
    return 'hex:' + bytes(b).hex()


NO_LOOP = 'hex:' + struct.pack('<dddQ', DBL_MAX, DBL_MAX, DBL_MAX, 0).hex()   # KNone override loop
PAST = [  # label, clip (start, loop_start, loop_end, looped), launch offset (song beat), now
    ('unlooped 1-bar clip launched at 8: now 11.999', (0.0, 0.0, 4.0, 0), 8.0, 11.999),
    ('unlooped 1-bar clip launched at 8: now 12', (0.0, 0.0, 4.0, 0), 8.0, 12.0),
    ('unlooped 1-bar clip launched at 8: now 12.001', (0.0, 0.0, 4.0, 0), 8.0, 12.001),
    ('unlooped clip region 1..3 launched at 8: now 10', (1.0, 1.0, 3.0, 0), 8.0, 10.0),
    ('looped 1-bar clip launched at 8: now 100', (0.0, 0.0, 4.0, 1), 8.0, 100.0),
    ('arrangement clip (slot -1), unlooped: now 100', (0.0, 0.0, 4.0, 0), 8.0, 100.0),
]


def past_end():
    toks, idx, k = ['call', hex(NOOP), 'buf:16'], [], 1
    for lbl, (s, ls, le, lp), off, now in PAST:
        slot = -1 if 'slot -1' in lbl else 0
        toks += ['call', hex(PASTEND), dbl(now), dbl(off), clip_buf(slot, s, ls, le, lp), NO_LOOP]
        idx.append(k)
        k += 1
    res = run(toks)
    return [{'label': lbl, 'clip': {'start': s, 'loop_start': ls, 'loop_end': le, 'looped': lp},
             'offset': off, 'now': now, 'past_end': res.calls[i]['rax'] & 0xff,
             'model': int(((le - ls) + off <= now) and not lp and 'slot -1' not in lbl)}
            for (lbl, (s, ls, le, lp), off, now), i in zip(PAST, idx)]


# ---- c: unwarped clip end -------------------------------------------------------------------
def status_buf(sr, tempo, anchor):
    """TStatus fields read by the unwarped end (Engine OScheduler::TStatus): +0 sample rate (int),
    +0x28 samples per beat, +0x30 beats per sample (as OScheduler::DoSetTempo computes them), +0x80 anchor."""
    spb = (sr / tempo) * 60.0
    b = bytearray(0xb8)
    struct.pack_into('<i', b, 0, sr)
    struct.pack_into('<dd', b, 0x28, spb, 1.0 / spb)
    struct.pack_into('<d', b, 0x80, anchor)
    return 'hex:' + bytes(b).hex(), spb


UNW = [  # sample rate, tempo (binary32 value), launch song beat, clip length in seconds, anchor
    (48000, 90.0, 8.0, 2.0, 0.0), (48000, 90.0, 8.0, 2.0 + 1 / 96000, 0.0), (44100, 90.0, 8.0, 2.0, 0.0),
    (48000, 120.0, 4.0, 1.0, 0.0), (48000, 120.0, 4.0, 0.123456, 0.0), (48000, 90.0, 8.0, 2.0, 0.37),
]


def unwarped_end():
    toks, idx, k, sp = ['call', hex(NOOP), 'buf:16'], [], 1, []
    for sr, tempo, start, secs, anchor in UNW:
        sb, spb = status_buf(sr, tempo, anchor)
        toks += ['call', hex(UNWEND), sb, dbl(start), dbl(secs)]
        idx.append(k)
        sp.append(spb)
        k += 1
    res = run(toks)
    out = []
    for (sr, tempo, start, secs, anchor), i, spb in zip(UNW, idx, sp):
        e = as_f64(res.calls[i]['xmm0'])
        bps = 1.0 / spb
        x = (secs * sr * bps + start) - anchor
        model = (math.ceil(x / bps) * bps) + anchor + (-1.3007825507825508e-07)
        out.append({'sr': sr, 'tempo': tempo, 'start': start, 'secs': secs, 'anchor': anchor,
                    'end_beat': e, 'end_bits': bits(e), 'model': model, 'model_equal': e == model,
                    'end_lattice_model': lattice_model(e)})
    return out


# ---- d: predelay (crossfade) of a stop and of a clip change on an audio track ----------------------
XF = [  # label, tempo, old clip kwargs or None, new clip kwargs or None
    ('stop: warped 1-bar session clip, Fade on, 90 BPM', 90.0, dict(slot=0, start=0, loop_start=0, loop_end=4, looped=1), None),
    ('stop: warped 1-bar session clip, Fade off, 90 BPM', 90.0, dict(slot=0, start=0, loop_start=0, loop_end=4, looped=1, fade=0), None),
    ('stop: unwarped session clip 2.6667 s, Fade on, 90 BPM', 90.0, dict(slot=0, start=0, loop_start=0, loop_end=8 / 3, looped=0, warped=0), None),
    ('stop: warped clip 0.01 beat long, Fade on, 90 BPM', 90.0, dict(slot=0, start=0, loop_start=0, loop_end=0.01, looped=1), None),
    ('stop: warped 1-bar session clip, Fade on, 120 BPM', 120.0, dict(slot=0, start=0, loop_start=0, loop_end=4, looped=1), None),
    ('stop: nothing playing', 90.0, None, None),
    ('change: 1-bar to 1-bar, both Fade on, 90 BPM', 90.0, dict(slot=0, start=0, loop_start=0, loop_end=4, looped=1),
     dict(slot=1, start=0, loop_start=0, loop_end=4, looped=1)),
    ('change: from nothing to 1-bar, Fade on, 90 BPM', 90.0, None, dict(slot=1, start=0, loop_start=0, loop_end=4, looped=1)),
]


def xfade():
    toks, idx, k = ['call', hex(NOOP), 'buf:16'], [], 1
    toks += ['call', hex(FADEINIT)]
    k += 1
    for lbl, tempo, old, new in XF:
        args = [dbl(tempo), clip_buf(**old) if old else 'i:0', clip_buf(**new) if new else 'i:0']
        toks += ['call', hex(XFADE), *args]
        idx.append(k)
        k += 1
    res = run(toks)
    out = []
    for (lbl, tempo, old, new), i in zip(XF, idx):
        o = as_f64(res.calls[i]['xmm0'])
        fade = 4.0 * 0.001 * tempo / 60.0

        def half(c):
            h = (c['loop_end'] - c['loop_start']) * 0.5
            return h if c.get('warped', 1) else h * tempo / 60.0
        if new is None:
            m = min(half(old), fade) if old and old.get('fade', 1) else 0.0
        elif old is None:
            m = 0.0
        else:
            m = min(min(half(new), fade), min(half(old), fade))
        out.append({'label': lbl, 'tempo': tempo, 'old': old, 'new': new, 'predelay_beats': o,
                    'predelay_bits': bits(o), 'model': m, 'model_equal': o == m,
                    'imports_used': dict(res.used)})
    return out


def main():
    out = {'slice_sha256': '1bae9a97...be999b0 (X1 slice)', 'loader': os.environ['XEXEC_BIN'],
           'stop_boundary': stops(), 'unlooped_end': past_end(), 'unwarped_end': unwarped_end(),
           'predelay': xfade()}
    (HERE / 'results' / 'stop.json').write_text(json.dumps(out, indent=1) + '\n')
    with open(HERE / 'raw' / 'runs.jsonl', 'w') as f:
        for r in RUNS:
            f.write(json.dumps(r) + '\n')
    for sect in ('stop_boundary', 'unlooped_end', 'unwarped_end', 'predelay'):
        print('==', sect)
        for r in out[sect]:
            print(json.dumps(r))


if __name__ == '__main__':
    main()
