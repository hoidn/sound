"""T1.3 launch: run the original x86_64 Live 12.4.3 launch pre-delay (crossfade) arithmetic (ADR 0003, label X).

usage: python3 -I -B run_launch.py      (from any directory; writes next to this file)

Target: x86_64 0x102278eb0, the clip crossfade length in beats (Engine name OAudioClip::SCrossfadeDurBeat,
Engine 0x9a45d0; arm64 counterpart named in matching.tsv). Arguments: xmm0 = tempo (binary64 of the scheduler's
binary32 tempo), rdi = previously playing clip (or null), rsi = new clip (or null). Its fade-time static is set
by its initializer 0x10227c780 (Engine OAudioClipFadeTime::SInitInstance), which is called first in each run.
Clip objects are hand-built buffers holding only the fields the function reads (Engine OAudioClip.Create member
order, ctor 0x9a3740): +0x2c SlotIndex (int), +0x40 LoopStart, +0x48 LoopEnd (binary64), +0x58 IsWarped,
+0xe0 Fade, +0xe1 IsCrossfadingIn (bytes), +0x100 FadeIn, +0x108 FadeOut (binary64).
Loader: xexec_t13.c (the X2 copy with its poke command), built to LOADER; driver tools/xexec/xexec.py.
Outputs: results.json (one record per case, with the static-reading model value), raw-runs.jsonl.
"""
import json
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
import xexec  # noqa: E402
from xexec import as_f64, dbl  # noqa: E402

LOADER = Path('/var/tmp/sound-analysis/xexec-t13-launch/xexec')
XFADE = 0x102278eb0
FADE_INIT = 0x10227c780
FADE_MS = 0x10744f7e8      # static written by FADE_INIT
FADE_GUARD = 0x10744f7f0


def build_loader():
    src = HERE / 'xexec_t13.c'
    if not LOADER.exists() or LOADER.stat().st_mtime < src.stat().st_mtime:
        LOADER.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['gcc', *xexec.CFLAGS, '-o', str(LOADER), str(src), '-ldl', '-lm'], check=True)
    return LOADER


xexec.build = build_loader
R = xexec.Runner()


def clip(slot=0, loop=(0.0, 4.0), warped=True, fade=True, xfin=False, fadein=0.0, fadeout=0.0):
    b = bytearray(0x120)
    struct.pack_into('<i', b, 0x2c, slot)
    struct.pack_into('<dd', b, 0x40, *loop)
    b[0x58], b[0xe0], b[0xe1] = int(warped), int(fade), int(xfin)
    struct.pack_into('<dd', b, 0x100, fadein, fadeout)
    return 'hex:' + b.hex()


def model(tempo, old, new):
    """Static reading of the disassembly (x86 0x102278eb0, Engine 0x9a45d0); fade time 4 ms."""
    def fade(c, t):
        if c['slot'] < 0:
            return None
        if not c['fade']:
            return 0.0
        half = (c['loop'][1] - c['loop'][0]) * 0.5
        if not c['warped']:
            half = (half * t) / 60.0
        return min(half, (4.0 * 0.001 * t) / 60.0)
    big = 1.7976931348623157e308
    if new is None:
        if old is None or old['slot'] < 0 or not old['fade']:
            return 0.0
        return fade(old, tempo)
    if new['xfin']:
        if new['slot'] < 0:
            return new['fadein']
        if not new['fade']:
            return 0.0
        half = (new['loop'][1] - new['loop'][0]) * 0.5
        if not new['warped']:
            half = (half * big) / 60.0
        return min(half, (4.0 * 0.001 * big) / 60.0)
    if old is None or new['slot'] < 0:
        return 0.0
    f_new = fade(new, tempo)
    if old['slot'] < 0:
        return min(old['fadeout'], f_new)
    return min(fade(old, tempo), f_new)


C = dict  # case parameters, mirrored into clip()
CASES = [
    ('no previous clip', 90.0, None, C(slot=0, loop=(0.0, 4.0), warped=True, fade=True)),
    ('both Fade on, warped 1-bar loops', 90.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=True),
     C(slot=0, loop=(0.0, 4.0), warped=True, fade=True)),
    ('both Fade on, 120 BPM', 120.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=True),
     C(slot=0, loop=(0.0, 4.0), warped=True, fade=True)),
    ('both Fade on, 20 BPM', 20.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=True),
     C(slot=0, loop=(0.0, 4.0), warped=True, fade=True)),
    ('both Fade on, 999 BPM', 999.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=True),
     C(slot=0, loop=(0.0, 4.0), warped=True, fade=True)),
    ('both unwarped, loops in seconds (2 s)', 90.0, C(slot=1, loop=(0.0, 2.0), warped=False, fade=True),
     C(slot=0, loop=(0.0, 2.0), warped=False, fade=True)),
    ('new unwarped 5 ms loop (half loop shorter than 4 ms)', 90.0,
     C(slot=1, loop=(0.0, 2.0), warped=False, fade=True), C(slot=0, loop=(1.0, 1.005), warped=False, fade=True)),
    ('old warped 0.004-beat loop', 90.0, C(slot=1, loop=(0.0, 0.004), warped=True, fade=True),
     C(slot=0, loop=(0.0, 4.0), warped=True, fade=True)),
    ('new Fade off', 90.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=True),
     C(slot=0, loop=(0.0, 4.0), warped=True, fade=False)),
    ('old Fade off', 90.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=False),
     C(slot=0, loop=(0.0, 4.0), warped=True, fade=True)),
    ('stop (no new clip), old Fade on', 90.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=True), None),
    ('stop (no new clip), old Fade off', 90.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=False), None),
    ('new IsCrossfadingIn, session, warped', 90.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=True),
     C(slot=0, loop=(0.0, 4.0), warped=True, fade=True, xfin=True)),
    ('new IsCrossfadingIn, session, unwarped', 90.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=True),
     C(slot=0, loop=(0.0, 4.0), warped=False, fade=True, xfin=True)),
    ('new IsCrossfadingIn, arrangement (slot -1)', 90.0, C(slot=1, loop=(0.0, 4.0), warped=True, fade=True),
     C(slot=-1, loop=(0.0, 4.0), warped=True, fade=True, xfin=True, fadein=0.25)),
    ('old arrangement clip (slot -1) FadeOut 0.003', 90.0,
     C(slot=-1, loop=(0.0, 4.0), warped=True, fade=True, fadeout=0.003),
     C(slot=0, loop=(0.0, 4.0), warped=True, fade=True)),
]


def full(c):
    if c is None:
        return None
    d = dict(slot=0, loop=(0.0, 4.0), warped=True, fade=True, xfin=False, fadein=0.0, fadeout=0.0)
    d.update(c)
    return d


def main():
    out, raw = [], open(HERE / 'raw-runs.jsonl', 'w')
    for label, tempo, old, new in CASES:
        old, new = full(old), full(new)
        t = float(struct.unpack('<f', struct.pack('<f', tempo))[0])   # the scheduler holds a binary32 tempo
        toks = ['call', hex(FADE_INIT), 'dump', hex(FADE_MS), '8', 'dump', hex(FADE_GUARD), '1',
                'call', hex(XFADE), dbl(t), clip(**old) if old else 'i:0', clip(**new) if new else 'i:0']
        r = R.run(toks)
        raw.write(json.dumps({'label': label, 'argv': toks, 'rc': r.rc, 'stdout': r.stdout, 'stderr': r.stderr}) + '\n')
        x = as_f64(r.calls[1]['xmm0']) if r.ok and len(r.calls) > 1 else None
        m = model(t, old, new)
        fade_ms = struct.unpack('<d', r.dumps[0][2])[0] if r.ok else None
        out.append({'label': label, 'tempo': t, 'old': old, 'new': new, 'x': x, 'x_hex': x.hex() if x is not None else None,
                    'model': m, 'equal': x == m, 'fade_ms_static': fade_ms, 'ok': r.ok, 'trap': r.trap,
                    'fault': r.fault, 'replaced_imports_called': r.used})
        print(f"{label}: x={x!r} model={m!r} equal={x == m} fade_ms={fade_ms} used={r.used} trap={r.trap}")
    raw.close()
    json.dump(out, open(HERE / 'results.json', 'w'), indent=1)
    print(f"{sum(o['equal'] for o in out)}/{len(out)} equal")


if __name__ == '__main__':
    main()
