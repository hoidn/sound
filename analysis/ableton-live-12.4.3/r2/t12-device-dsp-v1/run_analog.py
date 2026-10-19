"""Drive Analog's instrument path through the bundle's x86_64 slice: note events in, audio out.

    python3 -I run_analog.py         # writes raw/analog/, results/analog.json

Parameter sets: "bundle" sends nothing (the engine's built-in patch); "live" sends all 203 host
indices with the values Live sends for a fresh Analog, from the N6 table
(n6-device-tables-v1/out/conversions.tsv, column sent_for_default). Second outputs are derived as
that page states: a mode-1 sign flag is 1 for a negative default, a mode-3 low bit is
FilterType & 1, the mode-5 flag (index 7) is Polyphony > 0.5, and a mode-2 entry whose toggle
defaults off sends 0. Events are {frame, status, d1, d2} at absolute output frames. Inputs are silent;
the input flag is 0. The onset is the first frame whose |sample| exceeds 1e-6 on either channel.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402

import fit  # noqa: E402
import xdevpy  # noqa: E402

N6 = HERE.parent / 'n6-device-tables-v1' / 'out' / 'conversions.tsv'
N5 = HERE.parent / 'n5-device-mapping-v1' / 'out' / 'conversions.tsv'     # Amp, Cabinet, Electric, Corpus
FRAMES = 65536


def live_defaults(device='UltraAnalog'):
    """Host index -> value Live sends for a fresh instance (N6 or N5 table; device = its document element)."""
    table = N5 if device in ('Amp', 'Cabinet', 'LoungeLizard', 'Corpus') else N6
    rows = [r for r in csv.DictReader(table.open(), delimiter='\t') if r['device'] == device and r['index']]
    by = {int(r['index']): r for r in rows}
    vals = {}
    for i, r in sorted(by.items()):
        if r['sent_for_default']:
            vals[i] = float(r['sent_for_default'])
        elif r['stored_name'].startswith('(second output of index'):
            src = by[int(r['stored_name'].split()[4].rstrip(':'))]
            d = float(src['default'])
            vals[i] = 1.0 if 'mode 5' in r['stored_name'] else float(int(d) & 1) if 'mode 3' in r['stored_name'] else float(d < 0)
        elif r['mode'].startswith('ToggleMapping'):
            vals[i] = 0.0                       # its toggle (KeyboardUnisonToggle, LFOSyncToggle) defaults off
        elif r['stored_name'].startswith('(unused index'):
            continue                            # Tension index 2: nothing writes it
        else:
            raise ValueError(f'no default for index {i}')
    assert device != 'UltraAnalog' or (len(vals) == 203 and vals[7] == 1.0)
    return vals


def script(params, events, fs=44100, block=512, mxcsr=None, frames=FRAMES):
    lines = ['create', f'rate {fs}'] + [f'param {i} {v!r}' for i, v in sorted(params.items())]
    lines += [f'event {f} {s:#x} {a} {b}' for f, s, a, b in events]
    if mxcsr:
        lines.append(f'mxcsr {mxcsr:#x}')
    return lines + ['inflag 0', 'input zero', f'process {frames} {block}', 'destroy']


def first(y, thr):
    k = np.nonzero(np.abs(y).max(1) > thr)[0]
    return int(k[0]) if len(k) else None


def describe(y, fs, on, off):
    loud = np.nonzero(np.abs(y).max(1) > 1e-6)[0]
    seg = y[on + 2048:off, 0].astype(float)
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 18))
    hz = np.fft.rfftfreq(1 << 18, 1 / fs)
    f0 = fit.track(y[:off, 0].astype(float), float(hz[np.argmax(spec)]), fs, on + 2048, 20)['hz']
    return dict(first_nonzero_frame=first(y, 0), first_frame_above_1e6=first(y, 1e-6),
                last_frame_above_1e6=int(loud[-1]) if len(loud) else None,
                peak=float(np.abs(y).max()), rms_sustain=float(np.sqrt((y[on + 4096:off] ** 2).mean())),
                fundamental_hz=f0, channels_identical=bool(np.array_equal(y[:, 0], y[:, 1])))


def grid_rule(f, block, period):
    """First output frame an event at frame f can change: the frame after the start of the control
    period (period = fs // 1000 frames, counted from the first processed frame) that contains f; if
    that period began in an earlier host block, the frame after the start of the next period."""
    g = period * (f // period)
    return (g if g >= block * (f // block) else g + period) + 1


def sweeps(live, d):
    """Note-on frame -> first non-zero output frame, and note-off frame -> first frame that differs
    from the same note held, for several block sizes and both rates (renders not retained)."""
    out = {}
    for label, fs, block, frames in (('on_44_b512', 44100, 512, list(range(0, 200, 4)) + list(range(1000, 1200, 4))),
                                     ('on_44_b64', 44100, 64, list(range(1000, 1200, 4))),
                                     ('on_44_b333', 44100, 333, list(range(1000, 1200, 4))),
                                     ('on_48_b512', 48000, 512, list(range(1000, 1200, 4)))):
        rows = []
        for f in frames:
            y, _ = xdevpy.render('Analog', script(live, [(f, 0x90, 60, 100)], fs, block, frames=4096), d / 'sweep.f32')
            rows.append(dict(event=f, first_nonzero=first(y, 0), expected=grid_rule(f, block, fs // 1000)))
        out[label] = dict(fs=fs, block=block, period=fs // 1000, rows=rows,
                          rule_holds=all(r['first_nonzero'] == r['expected'] for r in rows))
    held, _ = xdevpy.render('Analog', script(live, [(1024, 0x90, 60, 100)], 44100, 512, frames=8192), d / 'held.f32')
    rows = []
    for f in range(4000, 4200, 4):
        y, _ = xdevpy.render('Analog', script(live, [(1024, 0x90, 60, 100), (f, 0x80, 60, 0)], 44100, 512, frames=8192), d / 'off.f32')
        diff = np.nonzero(np.abs(y.astype(float) - held.astype(float)).max(1) > 0)[0]
        rows.append(dict(event=f, first_diff=int(diff[0]) if len(diff) else None, expected=grid_rule(f, 512, 44)))
    out['off_44_b512'] = dict(fs=44100, block=512, period=44, rows=rows,
                              rule_holds=all(r['first_diff'] == r['expected'] for r in rows))
    return out


def main():
    xdevpy.build()
    raw = HERE / 'raw' / 'analog'
    raw.mkdir(parents=True, exist_ok=True)
    live = live_defaults()
    on, off = 4096, 4096 + 22050
    note = [(on, 0x90, 60, 100), (off, 0x80, 60, 0)]
    cases = {'note_bundle_44': dict(params={}, events=note), 'note_live_44': dict(params=live, events=note),
             'note_live_48': dict(params=live, events=note, fs=48000),
             'note_live_a4_44': dict(params=live, events=[(on, 0x90, 69, 100), (off, 0x80, 69, 0)])}
    out, runs = {}, {}
    for name, c in cases.items():
        y, log = xdevpy.render('Analog', script(c['params'], c['events'], c.get('fs', 44100), frames=c.get('frames', FRAMES)),
                               raw / f'{name}.f32')
        (raw / f'{name}.log').write_text(log)
        runs[name] = dict(sha256=xdevpy.sha256(raw / f'{name}.f32'), events=c['events'], fs=c.get('fs', 44100),
                          params='none' if not c['params'] else 'live-defaults', imports=xdevpy.used_imports(log),
                          process=next(l for l in log.splitlines() if l.startswith('process')))
        out[name] = describe(y, c.get('fs', 44100), on, off)
    scratch = Path('/var/tmp/sound-analysis/t12-xdev/rerun')
    scratch.mkdir(parents=True, exist_ok=True)
    sweep = sweeps(live, scratch)
    det = []
    base = raw / 'note_live_44.f32'
    for vname, kw in [('rerun', {}), ('block64', dict(block=64)), ('block256', dict(block=256)), ('block333', dict(block=333)),
                      ('ftz_daz', dict(mxcsr=0x9fc0))]:
        y, _ = xdevpy.render('Analog', script(live, note, **kw), scratch / f'analog_{vname}.f32')
        yb = np.fromfile(base, np.float32).reshape(-1, 2)
        d = np.abs(y.astype(float) - yb.astype(float))
        det.append(dict(variant=vname, equal=bool(np.array_equal(y.view(np.uint32), yb.view(np.uint32))),
                        max_abs_diff=float(d.max()), first_diff_frame=int(np.argmax(d.max(1) > 0)) if d.max() > 0 else None))
    (HERE / 'results' / 'analog.json').write_text(json.dumps(dict(
        bundle=str(xdevpy.BUNDLES['Analog']), bundle_sha256=xdevpy.sha256(xdevpy.BUNDLES['Analog']),
        n6_conversions_sha256=xdevpy.sha256(N6), live_defaults=live, runs=runs, measurements=out, determinism=det,
        timing=sweep), indent=1))
    print(json.dumps(out, indent=1))
    print(json.dumps(det, indent=1))
    print({k: v['rule_holds'] for k, v in sweep.items()})


if __name__ == '__main__':
    main()
