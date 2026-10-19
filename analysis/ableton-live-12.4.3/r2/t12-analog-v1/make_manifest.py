"""Write manifest.json: SHA-256 and size of every file in this evidence directory, the external inputs
(the Analog bundle executable with its x86_64 slice, the N6 tables, the helper corpus) and the tools.

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


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def slice_identity(path):
    b = Path(path).read_bytes()
    out = {'file_sha256': hashlib.sha256(b).hexdigest()}
    for i in range(struct.unpack_from('>I', b, 4)[0]):
        cpu, _, off, size, _ = struct.unpack_from('>IIIII', b, 8 + 20 * i)
        if cpu == 0x01000007:
            out.update(x86_64_offset=off, x86_64_size=size, x86_64_sha256=hashlib.sha256(b[off:off + size]).hexdigest())
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
    ext = {'bundle:Analog': dict(path=str(xdevpy.BUNDLES['Analog']), **slice_identity(xdevpy.BUNDLES['Analog']))}
    for rel in ('n6-device-tables-v1/out/conversions.tsv', 'n6-device-tables-v1/out/spec_defaults.tsv'):
        p = HERE.parent / rel
        ext[rel] = dict(path=str(p.resolve()), sha256=sha(p))
    h = Path('/var/tmp/sound-analysis/helpers/Analog')
    ext['helper-corpus:Analog'] = dict(path=str(h), slice=json.loads((h / 'slice.json').read_text()),
                                      corpus_manifest_sha256=sha(h / 'corpus' / 'indexes' / 'manifest.json'))
    tools = dict(host=platform.platform(), python=sys.version.split()[0], numpy=numpy.__version__, scipy=scipy.__version__,
                 gcc=first_line(['gcc', '--version']), glibc=first_line(['ldd', '--version']), objdump=first_line(['objdump', '--version']),
                 loader_binary=str(xdevpy.BIN), loader_sha256=sha(xdevpy.BIN) if xdevpy.BIN.exists() else None)
    m = dict(id='t12-analog-v1', created='2026-10-18', packet='T1.2 device audio: Analog by extracted execution',
             regenerate='sh run.sh', tools=tools, external_inputs=ext, files=files,
             harness='harness/ is a byte-identical copy of t12-device-dsp-v1/harness (SHA-256 per file below); built to /var/tmp/sound-analysis/t12-analog/xdev',
             not_retained='Measurement renders (measure.py) are reduced to results/*.json and not kept; variants are written under '
                          '/var/tmp/sound-analysis/t12-analog/tmp and deleted.')
    (HERE / 'manifest.json').write_text(json.dumps(m, indent=1) + '\n')
    print(f'{len(files)} files')


if __name__ == '__main__':
    main()
