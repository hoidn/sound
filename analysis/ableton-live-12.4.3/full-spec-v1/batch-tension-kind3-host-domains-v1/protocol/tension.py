"""Tension (StringStudio) host values, stored-value conversion and render scripts for the xdev loader.

    from tension import live_defaults, host_values, script, render
    host = host_values({'ExcitatorType': 1})          # stored values -> {index: host value}
    y, log = render(script(host, [(4096, 0x90, 60, 100)]), 'raw/x.f32')

Stored -> host follows SPEC-BUNDLED-DEVICE-PARAMETERS r2 and the N6 table
(n6-device-tables-v1/out/conversions.tsv, rows 'StringStudio'): each stored value is clamped to its
domain, integer-stepped Floats are quantized (nearest 1/32768, then toward zero), then the row's
mapping mode is applied (0 identity, 1 |v| plus sign flag on the next index, 2 v + 1 if the toggle is
on else 0, 3 int(v) >> 1 plus int(v) & 1 on the next index, 4 1 if v <= 0.5 else 0, 5 max(v - 1, 0)
plus v > 0.5 on index 7, 6 offset + mult * v). Index 2 is never sent. Dependencies: numpy, xdevpy.
"""
import csv
import gzip
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import xdevpy  # noqa: E402

N6 = HERE.parent / 'n6-device-tables-v1' / 'out' / 'conversions.tsv'
PRESETS = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Core Library')
ROWS = [r for r in csv.DictReader(N6.open(), delimiter='\t') if r['device'] == 'StringStudio']
PARAMS = {r['stored_name']: r for r in ROWS if not r['stored_name'].startswith('(')}
TOGGLES = {'KeyboardUnison': 'KeyboardUnisonToggle', 'LFOSync': 'LFOSyncToggle', 'BodyType': 'BodyToggle'}
TOGGLE_DEFAULTS = {'KeyboardUnisonToggle': 0.0, 'LFOSyncToggle': 0.0, 'BodyToggle': 0.0}   # spec table: false / 0


def stored_defaults():
    """Stored name -> constructor default ('Default when absent'), toggles included."""
    d = {n: float(r['default']) for n, r in PARAMS.items() if r['index'] and r['default']}
    d.update(TOGGLE_DEFAULTS)
    return d


def _domain(r):
    lo, hi = r['stored_domain'].split(' ')[0].split('..')
    return float(lo), float(hi)


def _quant(v):
    """ConvertQuantingInt: nearest 1/32768 (half away from zero), then toward zero."""
    q = math.copysign(math.floor(abs(v) * 32768 + 0.5), v) / 32768
    return float(math.trunc(q))


def host_values(changes=None, base=None):
    """Stored values (constructor defaults, overlaid by base, e.g. a preset, then by changes) -> {host index: float value}."""
    s = stored_defaults()
    s.update(base or {})
    s.update(changes or {})
    out = {}
    for name, r in PARAMS.items():
        if not r['index']:
            continue                                   # PerNotePitchBendRange: not passed
        i = int(r['index'])
        v = s[name]
        if r['class'] == 'TimeableBool':
            v = 1.0 if v > 0.5 else 0.0
        else:
            lo, hi = _domain(r)
            v = min(max(v, lo), hi)
        if r['user_converter'].startswith('legacyint'):
            v = _quant(v)
        if r['class'] == 'TimeableEnum':
            v = float(int(v))
        m = r['mode']
        if m.startswith('IndexedFloat'):
            out[i] = v
        elif m.startswith('ModulationPolarizer'):
            out[i], out[i + 1] = abs(v), float(v < 0)
        elif m.startswith('ToggleMapping'):
            out[i] = v + 1 if s[TOGGLES[name]] > 0.5 else 0.0
        elif m == 'FilterType':
            out[i], out[i + 1] = float(int(v) >> 1), float(int(v) & 1)
        elif m == 'BoolInverter':
            out[i] = 1.0 if v <= 0.5 else 0.0
        elif m.startswith('ToToggleMapping'):
            out[i], out[7] = max(v - 1, 0.0), float(v > 0.5)
        elif m.startswith('MultiplyOffset'):
            mult, off = (float(t.split('=')[1]) for t in m.split()[1:])
            if name == 'PitchBendRange':
                mult = 1 / 12                           # table prints 0.0833333; the constructor's v / 12
            out[i] = off + mult * v
        else:
            raise ValueError(f'mode {m} for {name}')
    assert sorted(out) == [i for i in range(130) if i != 2], sorted(set(range(130)) - set(out))
    return out


def preset_values(rel):
    """Stored StringStudio values of a shipped preset (path relative to Core Library)."""
    root = ET.fromstring(gzip.decompress((PRESETS / rel).read_bytes()))
    dev = root.find('.//StringStudio')
    out = {}
    for name in list(PARAMS) + list(TOGGLE_DEFAULTS):
        e = dev.find(name)
        if e is None:
            continue
        man = e.find('Manual')
        t = man.get('Value')
        out[name] = 1.0 if t == 'true' else 0.0 if t == 'false' else float(t)
    return out


def script(host, events, fs=44100, block=512, frames=88200, mxcsr=None, pre=(), post=()):
    lines = ['create', f'rate {fs}'] + list(pre) + [f'param {i} {v!r}' for i, v in sorted(host.items())] + list(post)
    lines += [f'event {f} {s:#x} {a} {b}' for f, s, a, b in events]
    if mxcsr:
        lines.append(f'mxcsr {mxcsr:#x}')
    return lines + ['inflag 0', 'input zero', f'process {frames} {block}', 'destroy']


def render(lines, out_path, env=None):
    return xdevpy.render('Tension', lines, out_path, env=env)


def note(n=60, vel=100, on=4096, dur=22050):
    return [(on, 0x90, n, vel), (on + dur, 0x80, n, 0)] if dur else [(on, 0x90, n, vel)]


if __name__ == '__main__':
    h = host_values()
    n6 = {int(r['index']): float(r['sent_for_default']) for r in ROWS if r['index'] and r['sent_for_default']}
    assert all(abs(h[i] - v) < 1e-6 for i, v in n6.items()), [(i, h[i], v) for i, v in n6.items() if abs(h[i] - v) >= 1e-6]
    print('tension.py self-check ok:', len(h), 'host values;', len(n6), 'equal N6 sent_for_default')
