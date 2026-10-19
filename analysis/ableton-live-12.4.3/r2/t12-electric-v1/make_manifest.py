"""Write manifest.json: SHA-256 and size of every file in this evidence directory, the external
inputs (the Electric bundle executable and its x86_64 slice, the N5 table, the shipped presets)
and the tools.

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
import el  # noqa: E402
import xdevpy  # noqa: E402


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def first_line(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        return (r.stdout or r.stderr).splitlines()[0]
    except (OSError, IndexError):
        return 'unavailable'


def slice_identity(path):
    b = Path(path).read_bytes()
    out = {'file_sha256': hashlib.sha256(b).hexdigest()}
    for i in range(struct.unpack_from('>I', b, 4)[0]):
        cpu, _, off, size, _ = struct.unpack_from('>IIIII', b, 8 + 20 * i)
        name = {0x01000007: 'x86_64', 0x0100000c: 'arm64'}[cpu]
        out[f'{name}_offset'], out[f'{name}_size'] = off, size
        out[f'{name}_sha256'] = hashlib.sha256(b[off:off + size]).hexdigest()
    return out


def main():
    import numpy
    import scipy
    files = {str(p.relative_to(HERE)): dict(sha256=sha(p), bytes=p.stat().st_size)
             for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name != 'manifest.json'}
    ext = {'bundle:Electric': dict(path=str(xdevpy.BUNDLES['Electric']), **slice_identity(xdevpy.BUNDLES['Electric'])),
           'n5-device-mapping-v1/out/conversions.tsv': dict(path=str(el.N5.resolve()), sha256=sha(el.N5)),
           'Defaults/Instruments/Electric.adv': dict(path=str(el.DEFAULTS_PRESET), sha256=sha(el.DEFAULTS_PRESET))}
    for p in sorted(el.PRESETS.rglob('*.adv')):
        if not p.name.startswith('._'):
            ext[f'preset:{p.stem}'] = dict(path=str(p), sha256=sha(p))
    tools = dict(host=platform.platform(), python=sys.version.split()[0], numpy=numpy.__version__, scipy=scipy.__version__,
                 gcc=first_line(['gcc', '--version']), glibc=first_line(['ldd', '--version']),
                 objdump=first_line(['objdump', '--version']), loader_binary=str(xdevpy.BIN),
                 loader_sha256=sha(xdevpy.BIN) if xdevpy.BIN.exists() else None)
    m = dict(id='t12-electric-v1', created='2026-10-18', packet='T1.2 Electric audio by extracted execution (SPEC-DEVICE-ELECTRIC r1)',
             regenerate='sh run.sh', tools=tools, external_inputs=ext, files=files,
             harness_change='harness/ is the t12-device-dsp-v1 loader with one change in xdev.c: event frames count over all '
                            'process commands, so parameters can change between process commands without events being delivered twice',
             not_retained='Variant renders (reseeded, libm-perturbed), probe renders and the stereo binary32 originals of the '
                          'retained WAV files are written under /var/tmp/sound-analysis/t12-electric/; their measures are in results/.')
    (HERE / 'manifest.json').write_text(json.dumps(m, indent=1) + '\n')
    print(f'{len(files)} files')


if __name__ == '__main__':
    main()
