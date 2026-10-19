"""T1.3 MIDI: run Live x86_64's per-key note-event builder 0x102a13f20 on hand-built notes (ADR 0003, label X).

usage: python3 -I -B midi/run_builder.py     (writes midi/results/note-events.json, midi/raw/builder-runs.jsonl)

0x102a13f20(out*, key, notes*, count, perNoteStore*, groups*) fills out = {int count, double* times,
TMidiNoteEventDescription* events (28 bytes: type, key, value, deviation, probability, group, flags)}; arm64
counterpart 0x1028cf5c0; caller 0x102a13a10 sends the arrays as OMidiNoteAutomation.Create members
NumEvents, EventTimesPtr, MidiNotes. Note record (48 bytes, the in-memory note at AMidiNoteEvent + 0x28):
+0 time, +8 duration, +0x10 velocity, +0x14 velocity deviation, +0x18 off velocity, +0x1c probability,
+0x20 enabled, +0x28 per-note-event key.
Harness setup (all recorded in each run's gdb script):
  * the shared-memory pool allocator 0x101ac2ea0 (size) is replaced under gdb by glibc malloc(size);
  * the application flag object read by 0x1014f9cc0 is supplied by poking the cached singleton pointer
    0x1073e1d60 -> buffer A, A+0x60 -> buffer B, byte B+0x39 = FLAG (0 or 1);
  * the probability-group lookup (groups+0x20 -> object, vtable slot +0x30) points at 0x1014b4330, which is
    replaced under gdb by "return 0x80000000" (no group);
  * the per-note event store is a zeroed 0x60-byte buffer (bucket count +0x48 = 0: no per-note events).
Loader: midi/xexec_t13m.c built to /var/tmp/sound-analysis/xexec-t13-midi/xexec (run_x.py builds it).
"""
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
import xexec  # noqa: E402

LOADER = '/var/tmp/sound-analysis/xexec-t13-midi/xexec'
BUILDER, POOL_ALLOC, SINGLETON, GROUP_FN = 0x102a13f20, 0x101ac2ea0, 0x1073e1d60, 0x1014b4330
NOP_GETTER = 0x102a1e960   # returns qword at rdi; used only as a call that creates buffers
H = 2.6015651015651016e-07


def note(t, dur, vel=100.0, dev=0.0, off=64.0, prob=1.0, enabled=1, key=0):
    return struct.pack('<ddffffB7xQ', t, dur, vel, dev, off, prob, enabled, key)


CASES = [  # (label, flag, notes)
    ('single note', 0, [note(0.0, 1.0)]),
    ('adjacent notes, off velocities 0 and 127', 0, [note(0.0, 1.0, 100.0, off=0.0), note(1.0, 1.0, 90.0, off=127.0)]),
    ('zero-length note then a later note', 0, [note(1.0, 0.0), note(2.0, 0.5)]),
    ('zero-length note sharing its start with the next note', 0, [note(1.0, 0.0, 80.0), note(1.0, 0.5, 70.0)]),
    ('two notes with the same start', 0, [note(1.0, 1.0, 80.0), note(1.0, 0.5, 70.0)]),
    ('disabled middle note', 0, [note(0.0, 0.5), note(1.0, 0.5, enabled=0), note(2.0, 0.5)]),
    ('non-lattice start and duration', 0, [note(0.1, 1.0 / 3.0), note(1.0000001, 0.2499999)]),
    ('deviation and probability, flag 0', 0, [note(0.0, 1.0, 100.0, dev=-20.0, prob=0.5), note(1.0, 1.0, 100.0, dev=50.0, prob=0.0)]),
    ('deviation and probability, flag 1', 1, [note(0.0, 1.0, 100.0, dev=-20.0, prob=0.5), note(1.0, 1.0, 100.0, dev=50.0, prob=0.0)]),
    ('fractional velocity 63.5', 0, [note(0.0, 1.0, 63.5, off=0.25)]),
    ('overlapping notes on one key', 0, [note(0.0, 2.0, 100.0), note(1.0, 2.0, 90.0)]),
    ('note longer than any loop', 0, [note(3.5, 9.0)]),
]


def run_case(label, flag, notes, key=60):
    toks = ['call', hex(NOP_GETTER), 'buf:24', 'buf:4096', 'buf:4096', 'buf:256', 'buf:64', 'buf:96']
    # b0 out, b1 A (singleton), b2 B (flag object), b3 G groups, b4 O group object, b5 V vtable
    toks += ['poke', hex(SINGLETON), 'b1', 'poke', 'b1+96', 'b2', 'poke', 'b2+56', hex(flag << 8),
             'poke', 'b3+32', 'b4', 'poke', 'b4', 'b5', 'poke', 'b5+48', hex(GROUP_FN)]
    toks += ['call', hex(BUILDER), 'ref:b0', f'i:{key}', 'hex:' + b''.join(notes).hex(), f'i:{len(notes)}',
             'buf:96', 'ref:b3']
    toks += ['dump', 'b0', '24', 'dump', 'b0+8*', '256', 'dump', 'b0+16*', '896']
    script = ['set pagination off', 'set confirm off', 'break xcall', 'run', 'delete 1',
              f'break *{POOL_ALLOC:#x}', 'commands', 'silent', 'set $sz = $rdi', 'return',
              'set $rax = (unsigned long) malloc($sz)', 'continue', 'end',
              f'break *{GROUP_FN:#x}', 'commands', 'silent', 'return', 'set $rax = 0x80000000', 'continue', 'end',
              'continue']
    g = tempfile.NamedTemporaryFile('w', suffix='.gdb', delete=False)
    g.write('\n'.join(script) + '\n')
    g.close()
    argv = [LOADER, xexec.SLICE, *toks]
    p = subprocess.run(['gdb', '-q', '-batch', '-nx', '-x', g.name, '--args', *argv],
                       capture_output=True, text=True, timeout=60)
    res = xexec.parse(p.returncode, p.stdout, p.stderr)
    raw = {'label': label, 'argv': argv, 'gdb_script': script, 'rc': p.returncode, 'stdout': p.stdout,
           'stderr': p.stderr}
    assert not res.trap and not res.fault, (label, res.trap, res.fault, p.stderr[-800:])
    d = {e: b for e, _, b in res.dumps}
    n = struct.unpack_from('<i', d['b0'], 0)[0]
    times = struct.unpack_from(f'<{n}d', d['b0+8*'], 0)
    events = []
    for i in range(n):
        ty, k, v, dev, prob, grp, f0, f1 = struct.unpack_from('<iifffiBB', d['b0+16*'], 28 * i)
        events.append({'time': times[i], 'type': {0: 'expression', 1: 'note-off', 2: 'note-on'}.get(ty, ty),
                       'key': k, 'value': v, 'deviation': dev, 'probability': prob, 'group': grp,
                       'flag18': f0, 'flag19': f1})
    return {'label': label, 'flag': flag, 'notes': [list(struct.unpack('<ddffffB7xQ', x)) for x in notes],
            'count': n, 'events': events, 'imports': res.used}, raw


def main():
    out, raws = [], []
    for c in CASES:
        r, raw = run_case(*c)
        out.append(r)
        raws.append(raw)
        print(f"{r['label']} (flag {r['flag']}): " + '; '.join(
            f"{e['type']}@{e['time']!r} v={e['value']!r}" + (f" dev={e['deviation']!r} p={e['probability']!r}"
            if e['type'] == 'note-on' else '') for e in r['events']))
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'raw').mkdir(exist_ok=True)
    json.dump(out, open(HERE / 'results' / 'note-events.json', 'w'), indent=1)
    with open(HERE / 'raw' / 'builder-runs.jsonl', 'w') as f:
        for r in raws:
            f.write(json.dumps(r) + '\n')


if __name__ == '__main__':
    main()
