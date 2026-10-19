"""T1.3 transport and clock: extracted execution of the Live x86_64 scheduler (ADR 0003, label X).

Runs the original OScheduler functions of the Live x86_64 slice on a hand-built scheduler object and
records (1) where the scheduler places a beat event in samples after a Play anchor, (2) the song-loop
jump, (3) stop and resume, (4) a tempo change mid-play. Addresses were matched to the named Live Engine
corpus (matching.tsv: identical instruction streams, constant address delta). Output is data.

usage: python3 -I -B run_transport.py        (writes raw/runs.jsonl, results/*.json; prints a summary)
Depends on xexec.py / xexec_t13.c in this directory (built to /var/tmp/sound-analysis/xexec-t13-transport/xexec),
gcc, and the Live x86_64 slice at XEXEC_SLICE.
"""
import json, math, struct, sys
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from xexec import Runner  # noqa: E402

HERE = Path(__file__).resolve().parent
# Live x86_64 functions (Engine name -> Live x86_64 VA; see matching.tsv)
DO_SET_TEMPO = 0x101adb640      # OScheduler::DoSetTempo(float, float, bool)
SET_BEAT_TIME = 0x101adc9a0     # OScheduler::SetBeatTime(double)
SET_PLAYING = 0x101adc350       # OScheduler::SetPlaying(bool)
SET_LOOP = 0x101adbe80          # OScheduler::SetLoop(bool, double, double)
SCHED_ABS = 0x101ad9760         # OScheduler::ScheduleAbsoluteBeatEvent(OBeatEvent*)
UNSCHED = 0x101ad9ac0           # OScheduler::UnscheduleBeatEvent(OBeatEvent*)
PROCESS_NEXT = 0x101ade8a0      # OScheduler::ProcessNextEvents()
PRED_SAMPLE = 0x101ad8a30       # OScheduler::TStatus::PredictedLongSampleTime(double)
PRED_BEAT = 0x101ad8a10         # OScheduler::TStatus::PredictedBeatTime(long long)
CALL_PROCESS = 0x101ab6900      # OEvent::CallProcess (vtable slot +0x10 -> slot +0x18)
NOP = 0x101b32800               # OSequencer::Exit (push rbp; mov rbp,rsp; pop rbp; ret)
LOOP_BRACE_VTBL = 0x106c98e80   # OLoopBraceEvent vtable as stored by OScheduler::Init (0x101add9b0)
SAMPLE_LIMIT_GUARD, SAMPLE_LIMIT = 0x1073e8040, 0x1073e8038   # lazily initialised limit read by ProcessNextEvents
FLT_MAX = 0x7f7fffff

f32 = lambda x: struct.unpack('<f', struct.pack('<f', x))[0]
bits = lambda d: struct.unpack('<Q', struct.pack('<d', d))[0]
unbits = lambda q: struct.unpack('<d', struct.pack('<Q', q))[0]


def sched_bytes(sr, n0):
    s = bytearray(0x460)
    struct.pack_into('<i', s, 0xe8, sr)                 # status: sample rate (TStatus +0x00)
    struct.pack_into('<d', s, 0x140, 1e12)              # loop start (status +0x58): far away, loop off
    struct.pack_into('<d', s, 0x148, 1.0)               # loop length (status +0x60)
    struct.pack_into('<q', s, 0x180, n0)                # long sample time (status +0x98)
    struct.pack_into('<I', s, 0x1b8, 1)
    struct.pack_into('<I', s, 0x1e8, FLT_MAX)           # no deferred tempo
    struct.pack_into('<I', s, 0x1f0, FLT_MAX)           # no deferred groove
    struct.pack_into('<Q', s, 0x1f8, 0x8000000080000000)  # no pending time signature (invalid)
    struct.pack_into('<I', s, 0x420, FLT_MAX)
    struct.pack_into('<H', s, 0x428, 0x100)             # +0x428 = 0, +0x429 = 1 (own status, as OScheduler::Init(false, sr))
    struct.pack_into('<f', s, 0x438, 1.0)               # tempo modulation
    struct.pack_into('<I', s, 0x43c, FLT_MAX)
    return s


def brace_bytes(start):
    e = bytearray(0x48)
    struct.pack_into('<Q', e, 0, LOOP_BRACE_VTBL)
    struct.pack_into('<i', e, 0x20, 13 if start else 5)  # priorities set by OScheduler::Init
    e[0x30] = 1 if start else 0
    return e


def setup(sr, tempo, n0, t0, loop=None):
    """b0 scheduler, b1 domain stub (flag +0x18, countdown +0x4c), b2/b3 loop braces, b4 probe vtable, b5 probe event."""
    vt = b''.join(struct.pack('<Q', a) for a in (NOP, NOP, CALL_PROCESS, NOP, NOP, NOP))
    probe = bytearray(0x48)
    t = ['call', hex(NOP), 'hex:' + sched_bytes(sr, n0).hex(), 'hex:' + ('00' * 0x60), 'hex:' + brace_bytes(1).hex(),
         'hex:' + brace_bytes(0).hex(), 'hex:' + vt.hex(), 'hex:' + probe.hex()]
    t += ['poke', 'b1+0x18', '1', 'poke', 'b1+0x10', 'b0',
          'poke', 'b0+0x20', 'b1+0x4c', 'poke', 'b0+0x1b0', 'b1+0x18',
          'poke', 'b0+0x1a0', 'b0+0xe8', 'poke', 'b0+0x1a8', 'b0+0x30',
          'poke', 'b0+0x408', 'b2', 'poke', 'b0+0x410', 'b3', 'poke', 'b2+0x38', 'b0', 'poke', 'b3+0x38', 'b0',
          'poke', 'b5', 'b4', 'poke', hex(SAMPLE_LIMIT), '400000000', 'poke', hex(SAMPLE_LIMIT_GUARD), '1']
    if loop:
        t += ['call', hex(SET_LOOP), 'ref:b0', 'i:1', f'd:{loop[0]!r}', f'd:{loop[1]!r}']
    t += ['call', hex(DO_SET_TEMPO), 'ref:b0', 'i:0', f'f:{tempo!r}', f'f:{tempo!r}',
          'call', hex(SET_BEAT_TIME), 'ref:b0', f'd:{t0!r}',
          'call', hex(SET_PLAYING), 'ref:b0', 'i:1']
    return t


STATUS_DUMPS = ['dump', 'b0+0x180', '8', 'dump', 'b0+0x190', '8', 'dump', 'b0+0x198', '8', 'dump', 'b0+0x158', '8',
                'dump', 'b0+0x110', '8', 'dump', 'b0+0x118', '8', 'dump', 'b1+0x4c', '4', 'dump', 'b0+0x150', '1']


def parse_status(dumps):
    d = {e: b for e, _, b in dumps}
    return {'long_sample': struct.unpack('<q', d['b0+0x180'])[0], 'ref_sample': struct.unpack('<q', d['b0+0x190'])[0],
            'ref_beat': struct.unpack('<d', d['b0+0x198'])[0], 'song_beat': struct.unpack('<d', d['b0+0x158'])[0],
            'spb': struct.unpack('<d', d['b0+0x110'])[0], 'bps': struct.unpack('<d', d['b0+0x118'])[0],
            'countdown': struct.unpack('<i', d['b1+0x4c'])[0], 'playing': d['b0+0x150'][0]}


# ---- models ---------------------------------------------------------------------------------------
def lattice(x):
    """Beat-event time rounding of ScheduleAbsoluteBeatEvent (REQ-CLIP-LAUNCH-013 formula)."""
    if x in (1.7976931348623155e308, -1.7976931348623155e308, 1.7976931348623157e308, math.inf):
        return x
    h = 1 / 3843840
    s = 1.0 if x >= 0 else -1.0
    return s * (math.floor(abs(x + s * h * 0.5) * 3843840.0) / 3843840.0)


def model(sr, tempo, n0, t0, b):
    spb = (sr / tempo) * 60.0
    d = lattice(b) - lattice(t0)
    x86 = math.ceil((d * spb) + float(n0)) - n0
    arm = math.ceil(math.fma(d, spb, float(n0))) - n0
    exact = Fr(lattice(b)) - Fr(lattice(t0))
    ex = math.ceil(exact * Fr(sr) * 60 / Fr(tempo))
    return {'x86_model': x86, 'arm64_fma_model': arm, 'exact_rational': ex}


# ---- experiments -----------------------------------------------------------------------------------
BEATS = [0.25, 1.0, 4.0, 8.0, 16.0, 64.0, 1000.0, 4 / 3, 10 / 3, 2 / 3, 1 / 3, 1 / 3843840, 1 + 1 / 3843840, 0.5, 3.75, 7.0]
TEMPOS = [90.0, 120.0, 128.0, 140.0, f32(280 / 3), f32(121.2), 20.0, 999.0]
RATES = [44100, 48000, 96000]
ANCHORS = [0, 1 << 20, (1 << 31) + 12345]


def fire_run(r, sr, tempo, n0, t0):
    beats = [t0 + o for o in BEATS]          # every probe lies after the anchor beat, so none fires at once
    t = setup(sr, tempo, n0, t0) + STATUS_DUMPS
    for b in beats:
        t += ['poke', 'b5+0x28', hex(bits(b)), 'poke', 'b5+0x10', '0', 'poke', 'b5+0x18', '0',
              'call', hex(SCHED_ABS), 'ref:b0', 'ref:b5', 'dump', 'b5+0x28', '8',
              'call', hex(PROCESS_NEXT), 'ref:b0', 'dump', 'b1+0x4c', '4', 'dump', 'b0+0x1d0', '8',
              'call', hex(PRED_SAMPLE), 'ref:b0+0xe8', 'd:' + repr(lattice(b)),
              'call', hex(UNSCHED), 'ref:b0', 'ref:b5']
    res = r.run(t)
    out = {'sr': sr, 'tempo': tempo, 'n0': n0, 't0': t0, 'ok': res.ok, 'trap': res.trap, 'fault': res.fault,
           'used': res.used}
    dumps = res.dumps
    out['status'] = parse_status(dumps[:8]) if len(dumps) >= 8 else None
    rows, k = [], 8
    pred_calls = [c for c in res.calls if c['addr'] == PRED_SAMPLE]
    for i, b in enumerate(beats):
        if k + 3 > len(dumps):
            break
        sched_time = struct.unpack('<d', dumps[k][2])[0]
        cd = struct.unpack('<i', dumps[k + 1][2])[0]
        head = struct.unpack('<Q', dumps[k + 2][2])[0]
        k += 3
        pred = pred_calls[i]['rax'] - (1 << 64) if pred_calls[i]['rax'] >> 63 else pred_calls[i]['rax']
        m = model(sr, tempo, n0, t0, b)
        rows.append({'beat': b, 'scheduled_time': sched_time, 'lattice_model': lattice(b), 'countdown': cd,
                     'predicted_sample_minus_n0': pred - n0, **m, 'head_is_probe': head != 0})
    out['rows'] = rows
    return out, res


def loop_run(r, sr, tempo, n0, t0, loop, passes, extra=None):
    """Advance the scheduler to each next event as the engine's domain does (countdown to 0, status flag cleared),
    then let ProcessNextEvents run the event; dump the status after each step."""
    t = setup(sr, tempo, n0, t0, loop) + ['call', hex(PROCESS_NEXT), 'ref:b0'] + STATUS_DUMPS
    for _ in range(passes):
        # the domain consumed `countdown` samples: countdown -> 0 and the status-valid flag cleared
        t += ['poke', 'b1+0x4c', '0', 'poke', 'b1+0x18', '0', 'call', hex(PROCESS_NEXT), 'ref:b0'] + STATUS_DUMPS
    if extra:
        t += extra
    res = r.run(t)
    steps = [parse_status(res.dumps[i:i + 8]) for i in range(0, len(res.dumps) - 7, 8)]
    return {'sr': sr, 'tempo': tempo, 'n0': n0, 't0': t0, 'loop': loop, 'ok': res.ok, 'trap': res.trap,
            'fault': res.fault, 'steps': steps}, res


def stop_resume_run(r, sr, tempo, n0, t0, run1, gap):
    """Play from t0, let run1 samples elapse, stop; let gap samples elapse, play again (no beat-time jump)."""
    # elapsed samples are (+0x18) - countdown, so set +0x18 to n and the countdown to 0 to model n elapsed samples
    adv = lambda n: ['poke', 'b0+0x18', str(n), 'poke', 'b1+0x4c', '0', 'poke', 'b1+0x18', '0']
    t = setup(sr, tempo, n0, t0) + STATUS_DUMPS
    t += adv(run1) + ['call', hex(SET_PLAYING), 'ref:b0', 'i:0'] + STATUS_DUMPS
    t += adv(gap) + ['call', hex(PROCESS_NEXT), 'ref:b0'] + STATUS_DUMPS
    t += ['call', hex(SET_PLAYING), 'ref:b0', 'i:1'] + STATUS_DUMPS
    t += adv(run1) + ['call', hex(PROCESS_NEXT), 'ref:b0'] + STATUS_DUMPS
    res = r.run(t)
    steps = [parse_status(res.dumps[i:i + 8]) for i in range(0, len(res.dumps) - 7, 8)]
    return {'sr': sr, 'tempo': tempo, 'n0': n0, 't0': t0, 'run1': run1, 'gap': gap, 'ok': res.ok, 'trap': res.trap,
            'fault': res.fault, 'steps': steps}, res


def tempo_change_run(r, sr, t1, t2, n0, run1, probe):
    """Play from 0 at tempo t1, let run1 samples elapse, call DoSetTempo(t2) (as the scheduler does when the
    nudged tempo arrives), then measure where a probe beat event fires."""
    adv = ['poke', 'b0+0x18', str(run1), 'poke', 'b1+0x4c', '0', 'poke', 'b1+0x18', '0']
    t = setup(sr, t1, n0, 0.0) + STATUS_DUMPS + adv + ['call', hex(PROCESS_NEXT), 'ref:b0'] + STATUS_DUMPS
    t += ['call', hex(DO_SET_TEMPO), 'ref:b0', 'i:0', f'f:{t2!r}', f'f:{t2!r}'] + STATUS_DUMPS
    t += ['poke', 'b5+0x28', hex(bits(probe)), 'call', hex(SCHED_ABS), 'ref:b0', 'ref:b5',
          'call', hex(PROCESS_NEXT), 'ref:b0'] + STATUS_DUMPS
    res = r.run(t)
    steps = [parse_status(res.dumps[i:i + 8]) for i in range(0, len(res.dumps) - 7, 8)]
    return {'sr': sr, 'tempo_before': t1, 'tempo_after': t2, 'n0': n0, 'run1': run1, 'probe': probe, 'ok': res.ok,
            'trap': res.trap, 'fault': res.fault, 'steps': steps}, res


class RecordingRunner(Runner):
    """Runner that keeps the token list of each run on its Result (for raw/runs.jsonl)."""
    def run(self, tokens, skip=None):
        res = super().run(tokens, skip)
        res.tokens = [str(t) for t in tokens]
        return res


def main():
    r = RecordingRunner()
    raw = open(HERE / 'raw/runs.jsonl', 'w')

    def keep(kind, out, res):
        raw.write(json.dumps({'kind': kind, 'argv_tail': res.tokens, 'rc': res.rc, 'stdout': res.stdout,
                              'stderr': res.stderr}) + '\n')
        return out

    jobs = [(sr, tp, n0, 0.0) for sr in RATES for tp in TEMPOS for n0 in ANCHORS]
    jobs += [(48000, tp, n0, 3.5) for tp in (90.0, 140.0) for n0 in (0, 1 << 20)]
    with ThreadPoolExecutor(4) as ex:
        fire = [keep('fire', *x) for x in ex.map(lambda j: fire_run(r, *j), jobs)]
    json.dump(fire, open(HERE / 'results/fire.json', 'w'), indent=1)

    loops = []
    for sr, tp, n0, t0, lp in [(48000, 120.0, 0, 4.0, (4.0, 4.0)), (48000, 140.0, 0, 4.0, (4.0, 4.0)),
                               (48000, 90.0, 0, 4.0, (4.0, 4.0)), (48000, 90.0, 1 << 20, 4.0, (4.0, 4.0)),
                               (44100, 140.0, 1 << 20, 0.0, (4.0, 4.0)), (48000, 120.0, 0, 0.0, (2.0, 10 / 3)),
                               (48000, 120.0, 0, 10.0, (4.0, 4.0))]:
        loops.append(keep('loop', *loop_run(r, sr, tp, n0, t0, lp, 4)))
    json.dump(loops, open(HERE / 'results/loop.json', 'w'), indent=1)

    stops = [keep('stop', *stop_resume_run(r, 48000, 140.0, 0, 0.0, 30000, 5000)),
             keep('stop', *stop_resume_run(r, 48000, 120.0, 1 << 20, 2.0, 12345, 999))]
    json.dump(stops, open(HERE / 'results/stop_resume.json', 'w'), indent=1)

    tempos = [keep('tempo', *tempo_change_run(r, 48000, 120.0, 90.0, 0, 24000, 2.0)),
              keep('tempo', *tempo_change_run(r, 48000, 120.0, 140.0, 0, 12000, 1.0)),
              keep('tempo', *tempo_change_run(r, 44100, 128.0, 93.33333587646484, 1 << 20, 20671, 2.0))]
    json.dump(tempos, open(HERE / 'results/tempo_change.json', 'w'), indent=1)
    raw.close()

    # summary
    bad = [x for x in fire + loops + stops + tempos if not x['ok']]
    print('runs', len(fire) + len(loops) + len(stops) + len(tempos), 'not ok', len(bad))
    n = agree = 0
    diffs = []
    for f in fire:
        for row in f['rows']:
            n += 1
            ok = row['countdown'] == row['x86_model'] == row['predicted_sample_minus_n0'] and \
                row['scheduled_time'] == row['lattice_model']
            agree += ok
            if row['x86_model'] != row['exact_rational'] or row['x86_model'] != row['arm64_fma_model']:
                diffs.append((f['sr'], f['tempo'], f['n0'], f['t0'], row['beat'], row['countdown'], row['x86_model'],
                              row['arm64_fma_model'], row['exact_rational']))
    print('fire rows', n, 'X == x86 model == PredictedLongSampleTime', agree)
    print('rows where x86 model differs from exact rational ceiling or arm64 fma model:', len(diffs))
    for d in diffs:
        print('  sr=%d tempo=%r n0=%d t0=%r beat=%r X=%d x86=%d arm64=%d exact=%d' % d)


if __name__ == '__main__':
    main()
