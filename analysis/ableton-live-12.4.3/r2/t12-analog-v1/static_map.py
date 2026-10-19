"""Static reading: Analog's host index -> engine module parameter, and the module parameters' curves.

    python3 -I static_map.py      # writes results/static_map.json

Source: the arm64 helper corpus of Analog.bundle (/var/tmp/sound-analysis/helpers/Analog/corpus,
decompiled functions, read-only). The parameter builder FUN_000018d8 registers each host index with one
of four setters: FUN_000179a4 (kind 0: host 0..1 sent as a controller value), FUN_00017aa8 (kind 2: float
range), FUN_00017c44 (kind 3: integer 0..max), FUN_00017d58 (virtual, handled by the wrapper itself).
Each registration names a module handle (an offset in the engine object) and the module's parameter id.
Module names per handle are inferred from the order of the module list in the patch text and from the
parameters each handle receives (labelled 'inferred'). Module constructors declare their parameters with
curve helpers (exponential FUN_0001cf3c, zero-capable exponential FUN_0001de3c, linear FUN_0001c0a0,
integer FUN_0001bdd0, square FUN_0001ed6c, smoothed exponential FUN_00024cf0, smoothed linear
FUN_00024888); the float arguments are decoded from their hex words. Dependencies: Python only.
"""
import glob
import json
import re
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = Path('/var/tmp/sound-analysis/helpers/Analog/corpus/decomp/chunks')
SETTERS = {'FUN_000179a4': 'kind0', 'FUN_00017aa8': 'kind2', 'FUN_00017c44': 'kind3', 'FUN_00017d58': 'virtual', 'FUN_00017bfc': 'kind2-signed'}
CURVES = {'FUN_0001cf3c': 'exp', 'FUN_0001de3c': 'exp-zero', 'FUN_0001c0a0': 'linear', 'FUN_0001bdd0': 'int', 'FUN_0001ed6c': 'square',
          'FUN_00024cf0': 'exp-smoothed', 'FUN_00024888': 'linear-smoothed', 'FUN_0001b9c8': 'bool'}
MODULES = {  # handle offset -> module (inferred from the patch module order and the parameters received)
    0x2168: 'unison detune', 0x216c: 'polyphony manager', 0x2170: 'MPE to CV (pitch bend ranges)', 0x2174: 'keyboard features',
    0x217c: 'Vibrato', 0x2180: 'Portamento', 0x2184: 'Noise', 0x2188: 'Noise_Routing', 0x218c: 'Oscillator_1', 0x2190: 'Oscillator_1_Routing',
    0x2198: 'Filter_1', 0x219c: 'Filter_1_To_Filter_2', 0x21a0: 'Amp_1', 0x21a4: 'Lfo_1', 0x21a8: 'Filter_Env_1', 0x21ac: 'Amp_Env_1',
    0x21b0: 'Oscillator_2', 0x21b4: 'Oscillator_2_Routing', 0x21bc: 'Filter_2', 0x21c0: 'Amp_2', 0x21c4: 'Lfo_2', 0x21c8: 'Filter_Env_2',
    0x21cc: 'Amp_Env_2', 0x21e8: 'Volume', 0x21f4: 'Lfo_Router'}


def code():
    out = {}
    for f in sorted(glob.glob(str(CORPUS / '*.jsonl'))):
        for line in open(f):
            d = json.loads(line)
            out[d['entry']] = d['code'] or ''
    return out


def word(s):
    s = s.strip()
    if s.startswith('0x'):
        v = int(s, 16)
        return struct.unpack('<f', struct.pack('<I', v))[0] if v > 0xffff else v
    try:
        return float(s)
    except ValueError:
        return s


def main():
    C = code()
    rows = []
    for m in re.finditer(r'(FUN_000179a4|FUN_00017aa8|FUN_00017c44|FUN_00017d58|FUN_00017bfc)\(([^;]*)\);', C['0x18d8']):
        a = [x.strip() for x in m.group(2).split(',')]
        kind = SETTERS[m.group(1)]
        if kind == 'kind0':
            idx, mod, pid, extra = a[1], a[2], a[3], None
        elif kind == 'kind2':
            idx, mod, pid, extra = a[3], a[4], a[5], [word(a[0]), word(a[1])]
        elif kind == 'kind3':
            idx, mod, pid, extra = a[1], a[2], a[3], word(a[4])
        elif kind == 'virtual':
            idx, mod, pid, extra = a[1], None, None, word(a[2])
        else:
            idx, mod, pid, extra = a[3], None, None, [word(a[0]), word(a[1])]
        off = int(re.search(r'0x[0-9a-f]+', mod).group(0), 16) if mod else None
        rows.append(dict(index=int(word(idx)), kind=kind, module_offset=hex(off) if off else None,
                         module_inferred=MODULES.get(off), param_id=int(word(pid)) if pid else None, range_or_max=extra))
    rows.sort(key=lambda r: r['index'])
    decls = []
    for entry, src in sorted(C.items()):
        for m in re.finditer(r'(FUN_000(?:1cf3c|1de3c|1c0a0|1bdd0|1ed6c|24cf0|24888))\(([^;]*)\);', src):
            a = [x.strip() for x in m.group(2).split(',')]
            name = next((x.strip('"') for x in a if x.startswith('"')), '')
            decls.append(dict(function=entry, curve=CURVES[m.group(1)], name=name, args=[word(x) for x in a if not x.startswith('"')]))
    out = dict(source=str(CORPUS), builder='0x18d8', index_map=rows, declarations=decls)
    (HERE / 'results' / 'static_map.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
    print(len(rows), 'indices,', len(decls), 'declarations')


if __name__ == '__main__':
    main()
