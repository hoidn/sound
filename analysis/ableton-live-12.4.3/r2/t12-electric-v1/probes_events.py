"""Electric probes on the event side: event timing, note messages, voices, tuning, other MIDI.

    python3 -I probes_events.py      # writes results/probes_events.json (renders not retained)

All renders use el.py's protocol (constructor values, clock value 0) unless a probe says otherwise.
Timing probes use no warm-up, so frames count from the instance's first processed frame.
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import el  # noqa: E402
import fit  # noqa: E402
import xdevpy  # noqa: E402

H = el.host_values(el.CONSTRUCTOR)


def grid(f, block, period):
    """Start of the control period containing frame f; the next one if that start lies in an earlier block."""
    g = period * (f // period)
    return g if g >= block * (f // block) else g + period


def _on(a):
    f, fs, block = a
    x, _ = el.render(H, [(f, 0x90, 60, 100)], fs, f'ton_{fs}_{block}_{f}', f + 2048, block=block, warm=0)
    nz = np.nonzero(x)[0]
    return dict(event=f, first_nonzero=int(nz[0]), predicted=grid(f, block, fs // 1000) + fs // 1000,
                silent_before=bool(not np.any(x[:nz[0]])))


def _off(a):
    f, fs, block, held = a
    x, _ = el.render(H, [(1024, 0x90, 60, 100), (f, 0x80, 60, 0)], fs, f'toff_{fs}_{block}_{f}', 8192, block=block, warm=0)
    d = np.nonzero(x != held)[0]
    return dict(event=f, first_changed=int(d[0]), predicted=grid(f, block, fs // 1000))


def timing(pool):
    out = {}
    for fs, block, frames in ((44100, 512, list(range(0, 200, 4)) + list(range(1000, 1200, 3))), (44100, 64, list(range(1000, 1200, 3))),
                              (44100, 333, list(range(1000, 1200, 3))), (48000, 512, list(range(1000, 1200, 3)))):
        rows = pool.map(_on, [(f, fs, block) for f in frames])
        out[f'note_on_{fs}_b{block}'] = dict(rows=rows, rule_holds=all(r['first_nonzero'] == r['predicted'] and r['silent_before'] for r in rows))
    for fs, block in ((44100, 512), (44100, 333), (48000, 512)):
        held, _ = el.render(H, [(1024, 0x90, 60, 100)], fs, f'theld_{fs}_{block}', 8192, block=block, warm=0)
        rows = pool.map(_off, [(f, fs, block, held) for f in range(4000, 4200, 3)])
        out[f'note_off_{fs}_b{block}'] = dict(rows=rows, rule_holds=all(r['first_changed'] == r['predicted'] for r in rows))
    return out


def same(a, b):
    return bool(np.array_equal(a, b))


def messages():
    ev = el.note(60, 100, 0, 13230)
    base, _ = el.render(H, ev, 44100, 'm_base', 22050)
    r = {}
    r['note_on_velocity_0_is_note_off'] = same(el.render(H, [ev[0], (13230, 0x90, 60, 0)], 44100, 'm_v0', 22050)[0], base)
    r['release_velocity_127_same_as_0'] = same(el.render(H, [ev[0], (13230, 0x80, 60, 127)], 44100, 'm_rv', 22050)[0], base)
    r['channel_2_same_as_channel_1'] = same(el.render(H, [(0, 0x91, 60, 100), (13230, 0x81, 60, 0)], 44100, 'm_ch', 22050)[0], base)
    r['channel_16_same_as_channel_1'] = same(el.render(H, [(0, 0x9f, 60, 100), (13230, 0x8f, 60, 0)], 44100, 'm_ch16', 22050)[0], base)
    held, _ = el.render(H, [ev[0]], 44100, 'm_held', 22050)
    r['note_off_other_key_ignored'] = same(el.render(H, [ev[0], (13230, 0x80, 61, 0)], 44100, 'm_ok', 22050)[0], held)
    for n in (0, 127):
        x, _ = el.render(H, el.note(n, 100, 0, 13230), 44100, f'm_n{n}', 22050)
        r[f'note_{n}_peak'] = float(np.abs(x).max())
    sus, _ = el.render(H, [(0, 0xB0, 64, 127)] + ev + [(30870, 0xB0, 64, 0)], 44100, 'm_sus', 52920)
    lv = lambda x, a, b: float(20 * np.log10(np.sqrt((x[a:b] ** 2).mean()) + 1e-30))  # noqa: E731
    r['cc64'] = dict(level_0_2s_after_note_off_db=lv(sus, 22050, 24255), without_pedal_db=lv(base, 17640, 19845),
                     level_0_3s_after_pedal_up_db=lv(sus, 44100, 46305))
    pb = {}
    for rng in (0.0, 0.25, 0.5, 1.0):
        h = {**H, 1: rng}
        for val, name in ((0x3fff, 'up'), (0, 'down')):
            x, _ = el.render(h, [(0, 0x90, 69, 100), (0, 0xE0, val & 127, val >> 7), (13230, 0x80, 69, 0)], 44100, 'm_pb', 22050)
            pb[f'range_{rng}_{name}'] = f0_of(x, 440 * 2 ** ((12 * rng if name == 'up' else -12 * rng) / 12), 44100, 13230)
    x, _ = el.render(H, el.note(69, 100, 0, 13230), 44100, 'm_a4', 22050)
    pb['no_bend'] = f0_of(x, 440, 44100, 13230)
    r['pitch_bend_f0_hz'] = pb
    return r


def f0_of(x, guess, fs, off, start=None):
    """Fundamental near guess (+/- 4 %, the strongest of harmonics 1..3), by FFT peak and fit.track."""
    start = start or int(0.03 * fs) + 44
    seg = x[start:off]
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 19))
    hz = np.fft.rfftfreq(1 << 19, 1 / fs)
    best = None
    for k in (1, 2, 3):
        if k * guess > fs / 2 - 200:
            break
        lo, hi = np.searchsorted(hz, k * guess * 0.96), np.searchsorted(hz, k * guess * 1.04)
        j = lo + int(np.argmax(sp[lo:hi]))
        if best is None or sp[j] > best[0]:
            best = (sp[j], k, hz[j])
    _, k, g = best
    return float(fit.track(x[:off], g, fs, start, min(20.0, g / 4))['hz'] / k)


def _tune(a):
    n, changes, fs = a
    h = {**H, **changes}
    x, _ = el.render(h, el.note(n, 100, 0, 17640), fs, f'tu_{n}_{sorted(changes.items())}_{fs}', 17640)
    t = h[30] - 12 + (h[3] - 0.5)
    return n, f0_of(x, 440 * 2 ** ((n - 69 + t) / 12), fs, 17640)


def tuning(pool):
    out = {}
    for label, ch, fs, notes in (('defaults_44', {}, 44100, range(0, 128)), ('defaults_48', {}, 48000, range(21, 109, 12)),
                                 ('stretch_0', {31: 0.0}, 44100, range(21, 109, 3)), ('stretch_1', {31: 1.0}, 44100, range(21, 109, 3)),
                                 ('stretch_0.25', {31: 0.25}, 44100, range(21, 109, 12)), ('stretch_0.75', {31: 0.75}, 44100, range(21, 109, 12)),
                                 ('finetune_0', {3: 0.0}, 44100, (36, 60, 84)), ('finetune_0.25', {3: 0.25}, 44100, (36, 60, 84)),
                                 ('finetune_0.75', {3: 0.75}, 44100, (36, 60, 84)), ('finetune_1', {3: 1.0}, 44100, (36, 60, 84)),
                                 ('transpose_0', {30: 0.0}, 44100, (48, 60, 72)), ('transpose_11', {30: 11.0}, 44100, (60,)),
                                 ('transpose_13', {30: 13.0}, 44100, (60,)), ('transpose_24', {30: 24.0}, 44100, (48, 60, 72))):
        out[label] = dict(pool.map(_tune, [(n, ch, fs) for n in notes]))
    d = out['defaults_44']
    out['defaults_44_cents_re_equal_temperament_a440'] = {n: 1200 * np.log2(f / (440 * 2 ** ((n - 69) / 12))) for n, f in d.items()}
    out['cents_re_defaults'] = {k: {n: 1200 * np.log2(f / d[n]) for n, f in v.items()} for k, v in out.items()
                                if k.startswith(('stretch', 'finetune'))}
    return out


def resid_db(full, part, a, b):
    d = full[a:b] - part[a:b]
    return float(20 * np.log10(np.sqrt((d ** 2).mean()) / np.sqrt((full[a:b] ** 2).mean())))


def _limit(p):
    """Voice limit test for Polyphony index p: n = p + 2 and p + 3 staggered held notes; residual of
    the full render against the render without the first note, 0.1 s after the last note-on."""
    h = {**H, 0: float(p), 28: 0.0}
    out = {}
    for n in (p + 2, p + 3):
        ev = [(1024 * k, 0x90, 40 + k, 100) for k in range(n)]
        end = 1024 * n + 8820
        full, _ = el.render(h, ev, 44100, f'pl_{p}_{n}', end)
        part, _ = el.render(h, ev[1:], 44100, f'plp_{p}_{n}', end)
        out[n] = resid_db(full, part, 1024 * (n - 1) + 4410, end)
    return p, dict(residual_without_first_db=out, voice_limit_is_p_plus_2=out[p + 2] > -20 and out[p + 3] < -35)


def voices(pool):
    out = dict(limit=dict(pool.map(_limit, range(31))))
    h2 = {**H, 0: 0.0, 28: 0.0}
    G, end = 2205, 2205 * 4 + 8820

    def ev(lst):
        return [(G * k, s, m, v) for k, s, m, v in lst]
    h3 = {**H, 0: 1.0, 28: 0.0}
    seq = [(k, 0x90, m, 100) for k, m in enumerate((72, 67, 64, 60))]
    full, _ = el.render(h3, ev(seq), 44100, 'vo_desc', end)
    out['three_voices_descending_drop_db'] = {seq[d][2]: resid_db(full, el.render(h3, ev(seq[:d] + seq[d + 1:]), 44100, 'vo_d', end)[0],
                                                                  G * 3 + 4410, end) for d in range(4)}
    seq = [(0, 0x90, 60, 100), (1, 0x90, 64, 100), (2, 0x80, 64, 0), (3, 0x90, 67, 100)]
    full, _ = el.render(h2, ev(seq), 44100, 'vo_rel', end)
    out['two_voices_released_vs_held_drop_db'] = {
        'held_60': resid_db(full, el.render(h2, ev([e for e in seq if e[2] != 60]), 44100, 'vo_r1', end)[0], G * 3 + 2205, end),
        'released_64': resid_db(full, el.render(h2, ev([e for e in seq if e[2] != 64]), 44100, 'vo_r2', end)[0], G * 3 + 2205, end)}
    for lim, hh in (('2', h2), ('32', {**H, 28: 0.0})):
        full, _ = el.render(hh, ev([(0, 0x90, 60, 100), (1, 0x90, 60, 100)]), 44100, 'vo_rep', end)
        a, _ = el.render(hh, ev([(0, 0x90, 60, 100)]), 44100, 'vo_rep_a', end)
        b, _ = el.render(hh, ev([(1, 0x90, 60, 100)]), 44100, 'vo_rep_b', end)
        out[f'repeat_key_{lim}_voices_vs_sum_of_two_single_strikes_db'] = resid_db(full, a + b, G + 4410, end)
    full, _ = el.render({**H, 28: 0.0}, ev([(0, 0x90, 60, 100), (1, 0x90, 60, 100), (2, 0x80, 60, 0)]), 44100, 'vo_off', end)
    out['repeat_key_one_note_off_level_db_0_2s_later'] = float(20 * np.log10(np.sqrt((full[G * 2 + 8820:G * 2 + 11025] ** 2).mean()) + 1e-30))
    seq = [(0, 0x90, 60, 100), (1, 0x90, 64, 100), (2, 0x90, 67, 100)]
    full, _ = el.render(h2, ev(seq), 44100, 'vo_f1', end)
    part, _ = el.render(h2, ev(seq[1:]), 44100, 'vo_f2', end)
    alone, _ = el.render(h2, ev(seq[:1]), 44100, 'vo_f3', end)
    g = grid(2 * G, 512, 44)
    ratio = [(full[g + k] - part[g + k]) / alone[g + k] if abs(alone[g + k]) > 1e-3 else None for k in range(-2, 50)]
    out['steal_fade'] = dict(grid_frame=g, frames_from_grid=list(range(-2, 50)), stolen_voice_ratio=ratio,
                             residual_after_db=resid_db(full, part, g + 44, g + 44 + 4410))
    return out


def _vel(a):
    fv, sv, v = a
    x, _ = el.render({**H, 9: fv, 6: sv}, el.note(60, v, 0, 13230), 44100, f've_{fv}_{sv}_{v}', 22050)
    e = 20 * np.log10(np.sqrt((x[2205:13230] ** 2).mean()) + 1e-30)
    return f'forcevel_{fv}_stiffvel_{sv}_vel_{v}', dict(peak=float(np.abs(x).max()), sustain_db=float(e))


def velocity(pool):
    """Peak and sustain level (50 ms to the note-off) of C4 by velocity, for velocity sensitivities."""
    return dict(pool.map(_vel, [(fv, sv, v) for fv in (0.0, 0.5, 1.0) for sv in (0.0, 0.5, 1.0) for v in (1, 16, 32, 64, 96, 100, 127)]))


def main():
    xdevpy.build()
    with Pool(8) as pool:
        out = dict(timing=timing(pool), messages=messages(), tuning=tuning(pool), voices=voices(pool), velocity=velocity(pool))
    (HERE / 'results' / 'probes_events.json').write_text(json.dumps(out, indent=1))
    print({k: v['rule_holds'] for k, v in out['timing'].items()})
    print(json.dumps(out['messages'], indent=1))
    print('limit p+2 for all p:', all(v['voice_limit_is_p_plus_2'] for v in out['voices']['limit'].values()))
    print({k: v for k, v in out['voices'].items() if k not in ('limit', 'steal_fade')})


if __name__ == '__main__':
    main()
