"""Write manifest.json: SHA-256 of the evidence files, harness sources, built loader and slice; tool versions."""
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
from xexec import SLICE  # noqa: E402

LOADER = Path('/var/tmp/sound-analysis/xexec-x2-notes-launch/xexec')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def first_line(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[0]


files = {str(p.relative_to(HERE)): sha(p) for p in sorted(HERE.rglob('*'))
         if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
manifest = {
    'id': 'X2-NOTES-LAUNCH-V1',
    'packet': 'X2 extracted execution: MIDI note storage and clip launch (ADR 0003, evidence label X)',
    'target': 'Ableton Live 12 Suite 12.4.3, Live x86_64 slice',
    'slice': {'path': SLICE, 'sha256': sha(SLICE), 'image_base': '0x100000000'},
    'harness': {'tools/xexec/xexec.py (driver, unchanged)': sha(ROOT / 'tools/xexec/xexec.py'),
                'tools/xexec/xexec.c (copied from)': sha(ROOT / 'tools/xexec/xexec.c'),
                'xexec_x2.c (loader copy: adds "poke")': sha(HERE / 'xexec_x2.c'),
                'built_loader': {'path': str(LOADER), 'sha256': sha(LOADER)}},
    'tools': {'gcc': first_line(['gcc', '--version']), 'gdb': first_line(['gdb', '--version']),
              'objdump': first_line(['objdump', '--version']), 'python': platform.python_version(),
              'glibc': platform.libc_ver()[1], 'kernel': platform.release()},
    'commands': ['sh run.sh'],
    'executed_live_application': False,
    'executed_original_code': 'x86_64 functions listed in addresses.json (those without "static" in their role), '
                              'in the xexec_x2 harness on Linux x86_64',
    'static_tools': ['xtool.py (x86 pointer/constant reads, objdump)', 'corpus_lookup.py (decompiled corpora)'],
    'files': files,
}
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
print(f'manifest.json: {len(files)} files')
