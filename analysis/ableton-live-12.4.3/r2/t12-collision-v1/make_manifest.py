"""Write manifest.json: SHA-256 and size of every file in this evidence directory, the external inputs
(the Collision executable with its x86_64 slice, the N6 table, the Corpus mode tables, the Defaults
preset, the preset and preview files used) and the tools.

    python3 -I make_manifest.py
"""
import hashlib
import json
import platform
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import xdevpy  # noqa: E402
from col import DEFAULTS_ADV, N6  # noqa: E402


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def slice_identity(path):
    b = Path(path).read_bytes()
    out = dict(path=str(path), file_sha256=hashlib.sha256(b).hexdigest())
    for i in range(struct.unpack_from('>I', b, 4)[0]):
        cpu, _, off, size, _ = struct.unpack_from('>IIIII', b, 8 + 20 * i)
        name = {0x01000007: 'x86_64', 0x0100000c: 'arm64'}[cpu]
        out[name] = dict(offset=off, size=size, sha256=hashlib.sha256(b[off:off + size]).hexdigest())
    return out


def first_line(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        return (r.stdout or r.stderr).splitlines()[0]
    except (OSError, IndexError):
        return 'unavailable'


def main():
    import numpy
    import scipy
    files = {str(p.relative_to(HERE)): dict(sha256=sha(p), bytes=p.stat().st_size)
             for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name != 'manifest.json'}
    ext = {'bundle:Collision': slice_identity(xdevpy.BUNDLES['Collision'])}
    for p in (N6, HERE.parent / 'corpus-dsp-v1' / 'tables.py', DEFAULTS_ADV):
        ext[str(p)] = dict(sha256=sha(p))
    prev = json.loads((HERE / 'results' / 'previews.json').read_text())
    ext['previews'] = {r['preset']: dict(adv_sha256=r.get('adv_sha256'), ogg_sha256=r.get('ogg_sha256')) for r in prev['presets']}
    tools = dict(host=platform.platform(), python=sys.version.split()[0], numpy=numpy.__version__, scipy=scipy.__version__,
                 gcc=first_line(['gcc', '--version']), glibc=first_line(['ldd', '--version']),
                 objdump=first_line(['objdump', '--version']), gstreamer=first_line(['gst-launch-1.0', '--version']),
                 loader_binary=str(xdevpy.BIN), loader_sha256=sha(xdevpy.BIN) if xdevpy.BIN.exists() else None)
    m = dict(id='t12-collision-v1', created='2026-10-18', packet='T1.2 Collision audio by extracted execution',
             regenerate='sh run.sh', loader='harness/ is an unmodified copy of t12-device-dsp-v1/harness',
             tools=tools, external_inputs=ext, files=files,
             not_retained='Sweeps, ensembles (members 1-7), perturbed renders, decoded previews and preview renders are written '
                          'under /var/tmp/sound-analysis/t12-collision/; their measurements are in results/.')
    (HERE / 'manifest.json').write_text(json.dumps(m, indent=1) + '\n')
    print(f'{len(files)} files')


if __name__ == '__main__':
    main()
