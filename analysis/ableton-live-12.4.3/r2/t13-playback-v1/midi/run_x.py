"""T1.3 MIDI clip playback: run original x86_64 Live 12.4.3 clip-position arithmetic (ADR 0003, label X).

usage: python3 -I -B midi/run_x.py      (writes midi/results/clip-position.json, midi/raw/clip-position-runs.jsonl)

Targets (Live x86_64 slice; Engine names by address/size neighbourhood match, see midi/match-eng-x86.tsv):
  0x101b12870  OClip::SCalcCurrentPos(start, loopStart, loopEnd, looped, d) -> clip time (DBL_MAX = ended)
  0x101b14fd0  clip position core (d, OClipLoop*, flag)                       (Engine FUN_00145c80)
  0x101b12950  OClip::SCalcAutomationOffset(OClipLoop*, d, flag) -> d - clip time
OClipLoop = {double Start, double LoopStart, double LoopEnd, bool IsLooped} (Engine OClip ctor +0x38..+0x50).
Each result is compared with a binary64 model written from the disassembly (lattice rounding L, fmod fold).
Loader: midi/xexec_t13m.c (copy of the X2 loader), built to /var/tmp/sound-analysis/xexec-t13-midi/xexec.
"""
import json
import math
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
import xexec  # noqa: E402
from xexec import as_f64, dbl  # noqa: E402

LOADER = Path('/var/tmp/sound-analysis/xexec-t13-midi/xexec')


def build_loader():
    src = HERE / 'xexec_t13m.c'
    if not LOADER.exists() or LOADER.stat().st_mtime < src.stat().st_mtime:
        LOADER.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['gcc', *xexec.CFLAGS, '-o', str(LOADER), str(src), '-ldl', '-lm'], check=True)
    return LOADER


xexec.build = build_loader
R = xexec.Runner()
CURPOS, CORE, AUTOOFF = 0x101b12870, 0x101b14fd0, 0x101b12950
DBL_MAX = sys.float_info.max
SENT = {-1.7976931348623155e308, 1.7976931348623155e308, DBL_MAX, math.inf}
H = 2.6015651015651016e-07


def L(x):
    """Lattice rounding as the code does it (sentinels pass): s * floor(|x + s*h*0.5| * 3843840) / 3843840."""
    if x in SENT:
        return x
    s = 1.0 if x >= 0.0 else -1.0
    return (math.floor(abs(H * s * 0.5 + x) * 3843840.0) / 3843840.0) * s


def fold(x, a, b):
    w = b - a
    r = math.fmod(x - a, w)
    sg = 0.0 if w == 0.0 else (1.0 if w > 0.0 else -1.0)
    return (w + r if sg * r < 0.0 else r) + a


def core(d, S, Ls, Le, looped, flag):
    p = L(d + S)
    if looped and Le <= p:
        p = L(fold(L(p), Ls, Le))
        if p == Le:
            p = Ls
        p = L(p)
        if flag and p == Ls:
            return Le
    return p


def curpos(S, Ls, Le, looped, d):
    p = core(d, S, Ls, Le, looped, 0)
    return p if looped or p < Le else DBL_MAX


def autooff(S, Ls, Le, looped, d, flag):
    if Le <= S + d:
        if not looped:
            return d - Le
    elif not (flag and d < 0.0 and looped and S >= Ls):
        return 0.0 - S
    q = L(fold(L(S + d), Ls, Le))
    q = Ls if Le == q else q
    return L(d - q)


def loopbuf(S, Ls, Le, looped):
    return 'hex:' + struct.pack('<dddB7x', S, Ls, Le, looped).hex()


LOOPS = [  # (label, Start, LoopStart, LoopEnd, looped)
    ('loop0-4', 0.0, 0.0, 4.0, 1), ('start1-loop0-4', 1.0, 0.0, 4.0, 1), ('start-32-loop0-16', -32.0, 0.0, 16.0, 1),
    ('start2-loop1-3', 2.0, 1.0, 3.0, 1), ('start0.5-loop0.25-2.75', 0.5, 0.25, 2.75, 1),
    ('start3.5-loop1-3 (start after loop end)', 3.5, 1.0, 3.0, 1), ('triplet loop 0-4/3', 0.0, 0.0, 4.0 / 3.0, 1),
    ('unlooped 0-4', 0.0, 0.0, 4.0, 0), ('unlooped 1-4', 1.0, 1.0, 4.0, 0)]
DS = [0.0, 0.1, 1.0 / 3.0, 1.5, 2.0, 2.5, 2.9999999, 3.0, 3.5, 3.9999999, 4.0, 4.0 + H, 4.0 - H, 5.75, 7.0, 8.0,
      12.5, 15.999999, 16.0, 31.0, 32.0, 47.75, 48.0, 100.0, 1000003.3, -0.5]


def main():
    out, raw = [], []
    cases = [(lab, S, Ls, Le, lp, d) for (lab, S, Ls, Le, lp) in LOOPS for d in DS]
    for i in range(0, len(cases), 80):
        chunk = cases[i:i + 80]
        toks = []
        for (_, S, Ls, Le, lp, d) in chunk:
            toks += ['call', hex(CURPOS), dbl(S), dbl(Ls), dbl(Le), f'i:{lp}', dbl(d)]
            toks += ['call', hex(AUTOOFF), dbl(d), loopbuf(S, Ls, Le, lp), 'i:0']
            toks += ['call', hex(CORE), dbl(d), loopbuf(S, Ls, Le, lp), 'i:1']
        res = R.run(toks)
        raw.append({'argv': R.log[-1][0], 'rc': res.rc, 'stdout': res.stdout, 'stderr': res.stderr})
        assert res.ok, (res.trap, res.fault, res.stderr[-500:])
        for k, (lab, S, Ls, Le, lp, d) in enumerate(chunk):
            cp, ao, co = (as_f64(res.calls[3 * k + j]['xmm0']) for j in range(3))
            m = (curpos(S, Ls, Le, lp, d), autooff(S, Ls, Le, lp, d, 0), core(d, S, Ls, Le, lp, 1))
            out.append({'loop': lab, 'Start': S, 'LoopStart': Ls, 'LoopEnd': Le, 'IsLooped': lp, 'd': d,
                        'clip_time_x': cp, 'auto_offset_x': ao, 'core_flag1_x': co,
                        'model': list(m), 'agree': [cp == m[0], ao == m[1], co == m[2]],
                        'imports': res.used})
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'raw').mkdir(exist_ok=True)
    json.dump(out, open(HERE / 'results' / 'clip-position.json', 'w'), indent=1)
    with open(HERE / 'raw' / 'clip-position-runs.jsonl', 'w') as f:
        for r in raw:
            f.write(json.dumps(r) + '\n')
    n = len(out)
    print(f'clip position: {n} inputs x 3 functions; agree with model: '
          f'{sum(o["agree"][0] for o in out)}/{n} SCalcCurrentPos, {sum(o["agree"][1] for o in out)}/{n} '
          f'SCalcAutomationOffset, {sum(o["agree"][2] for o in out)}/{n} core(flag 1)')
    for o in out:
        if not all(o['agree']):
            print('DIFF', o['loop'], o['d'], o['clip_time_x'], o['auto_offset_x'], o['core_flag1_x'], o['model'])


if __name__ == '__main__':
    main()
