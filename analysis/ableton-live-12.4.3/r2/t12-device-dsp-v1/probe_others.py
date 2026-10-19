"""Feasibility probe for the other five bundled devices: does the bundle loader load each x86_64
slice, create an instance and render a note (instruments) or silence (effects)?

    python3 -I probe_others.py      # writes results/other_devices.json (renders not retained)

Instruments get a C4 note (velocity 100) at frame 4096 and its note-off 0.5 s later, once with the
engine's built-in patch (no SetParameterA) and once with Live's constructor defaults from the N6
table. Amp and Cabinet (MH_DYLIB) get create and 1 s of silence. A trap names the first import
that the loader leaves unbound.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402

import run_analog  # noqa: E402
import xdevpy  # noqa: E402

DOC = {'Tension': 'StringStudio', 'Collision': 'Collision', 'Electric': 'LoungeLizard'}


def slice_identity(path):
    import struct
    import hashlib
    b = Path(path).read_bytes()
    out = {'file_sha256': hashlib.sha256(b).hexdigest()}
    for i in range(struct.unpack_from('>I', b, 4)[0]):
        cpu, _, off, size, _ = struct.unpack_from('>IIIII', b, 8 + 20 * i)
        if cpu == 0x01000007:
            out.update(x86_64_offset=off, x86_64_size=size, x86_64_sha256=hashlib.sha256(b[off:off + size]).hexdigest(),
                       filetype={6: 'MH_DYLIB', 8: 'MH_BUNDLE'}[struct.unpack_from('<I', b, off + 12)[0]])
    return out


def run(dev, lines, tag):
    d = Path('/var/tmp/sound-analysis/t12-xdev/rerun')
    try:
        y, log = xdevpy.render(dev, lines, d / f'probe_{dev}_{tag}.f32')
    except xdevpy.RunError as e:
        msg = str(e)
        return dict(ok=False, trap=next((l for l in msg.splitlines() if l.startswith(('TRAP', 'FAULT'))), msg[:200]),
                    initializers=[l for l in msg.splitlines() if l.startswith('init ')])
    nz = np.nonzero(np.abs(y).max(1) > 0)[0]
    loud = np.nonzero(np.abs(y).max(1) > 1e-6)[0]
    return dict(ok=True, first_nonzero_frame=int(nz[0]) if len(nz) else None, first_frame_above_1e6=int(loud[0]) if len(loud) else None,
                peak=float(np.abs(y).max()), process=next(l for l in log.splitlines() if l.startswith('process')),
                used_imports=len(xdevpy.used_imports(log)))


def main():
    xdevpy.build()
    note = ['inflag 0', 'input zero', 'event 4096 0x90 60 100', 'event 26146 0x80 60 0', 'process 44100 512', 'destroy']
    out = {}
    for dev in ('Tension', 'Collision', 'Electric'):
        live = run_analog.live_defaults(DOC[dev])
        out[dev] = dict(identity=slice_identity(xdevpy.BUNDLES[dev]), params_sent=len(live),
                        builtin=run(dev, ['create', 'rate 44100'] + note, 'builtin'),
                        live_defaults=run(dev, ['create', 'rate 44100'] + [f'param {i} {v!r}' for i, v in sorted(live.items())] + note, 'live'))
    for dev in ('Amp', 'Cabinet'):
        out[dev] = dict(identity=slice_identity(xdevpy.BUNDLES[dev]),
                        silence=run(dev, ['info', 'create', 'rate 44100', 'inflag 1', 'input zero', 'process 44100 512', 'destroy'], 'fx'))
    (HERE / 'results' / 'other_devices.json').write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
