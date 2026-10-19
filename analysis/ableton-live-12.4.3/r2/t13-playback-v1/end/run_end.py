"""T1.3: end sample of the two shipped unwarped one-shot clips used by the audio cases (ADR 0003, evidence label X).

Runs the Live x86_64 function 0x101b6c540 (Engine OUnwarpedClipTimeEvent::SBeatTimeForClipTime; matching in
../stop/matching.tsv) on a hand-built scheduler status, exactly as ../stop/run_stop.py does for its STP-15 rows,
with the clip lengths of the shipped clips (LoopEnd - LoopStart, seconds, transposition 0) read from
../audio/shipped-unwarped-clips.jsonl. Then places the lattice-rounded end beat and the launch beat on samples by
the X-confirmed clock rule of ../transport (anchor beat 0 at sample 0, counter 0).
The loader is the unmodified tools/xexec, built to XEXEC_BIN below.
usage: python3 -I -B run_end.py      (writes results.json and raw-runs.jsonl here)
"""
import json, math, os, struct, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
os.environ.setdefault('XEXEC_BIN', '/var/tmp/sound-analysis/xexec-t13-end/xexec')
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
import xexec  # noqa: E402
from xexec import as_f64, dbl  # noqa: E402

UNWEND, NOOP, N = 0x101b6c540, 0x1002c4280, 3843840
CLIPS = {'Rim 3k Sharp (48 kHz file)': 0.41485416666666669 - 0.0, 'Rim DMX Vinyl (44.1 kHz file)': 0.0767800453514739245 - 0.0}
SETUPS = [(48000, 120.0, 4.0), (48000, 90.0, 8.0), (44100, 90.0, 8.0), (44100, 120.0, 4.0)]


def lattice(x):
    s = 1.0 if x >= 0 else -1.0
    return s * (math.floor(abs(x + s * (1.0 / N) / 2) * N) / N)


def place(b, sr, tempo):
    return math.ceil(b * ((sr / tempo) * 60.0) + 0.0)


def status(sr, tempo):
    spb = (sr / tempo) * 60.0
    b = bytearray(0xb8)
    struct.pack_into('<i', b, 0, sr)
    struct.pack_into('<dd', b, 0x28, spb, 1.0 / spb)
    struct.pack_into('<d', b, 0x80, 0.0)
    return 'hex:' + bytes(b).hex()


def main():
    rows = [(name, secs, sr, t, start) for name, secs in CLIPS.items() for sr, t, start in SETUPS]
    toks = ['call', hex(NOOP), 'buf:16']
    for _, secs, sr, t, start in rows:
        toks += ['call', hex(UNWEND), status(sr, t), dbl(start), dbl(secs)]
    r = xexec.Runner().run(toks)
    (HERE / 'raw-runs.jsonl').write_text(json.dumps({'argv': toks, 'rc': r.rc, 'stdout': r.stdout, 'stderr': r.stderr}) + '\n')
    assert r.ok, r.stderr
    out = []
    for (name, secs, sr, t, start), c in zip(rows, r.calls[1:]):
        e = as_f64(c['xmm0'])
        n0, n1 = place(start, sr, t), place(lattice(e), sr, t)
        out.append({'clip': name, 'secs': secs, 'rate': sr, 'tempo': t, 'launch_beat': start, 'end_beat_x': e,
                    'end_beat_lattice': lattice(e), 'launch_sample': n0, 'end_sample': n1, 'length_samples': n1 - n0,
                    'exact_length': secs * sr})
    (HERE / 'results.json').write_text(json.dumps(out, indent=1) + '\n')
    for o in out:
        print(o)


if __name__ == '__main__':
    main()
