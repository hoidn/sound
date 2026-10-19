"""Write manifest.json for t13-playback-v1: SHA-256 of every retained file, the slices, the harness sources and the
loaders built for this packet; tool versions; commands. Analyst tool; output is data."""
import hashlib
import json
import platform
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLICES = {'live_x86_64': ('/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64', '0x100000000'),
          'live_arm64': (str(ROOT / 'analysis/ableton-live-12.4.3/derived/Live.arm64'), '0x100000000'),
          'live_engine_x86_64': ('/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/'
                                 'Ableton_Live_Engine_x86_64.x86_64', '0x0')}
LOADERS = {a: f'/var/tmp/sound-analysis/xexec-t13-{a}/xexec' for a in ('transport', 'launch', 'midi', 'audio', 'stop', 'end')}
LOADER_SOURCE = {'transport': 'transport/xexec_t13.c (tools/xexec/xexec.c plus "poke")',
                 'launch': 'launch/xexec_t13.c (tools/xexec/xexec.c plus "poke")',
                 'midi': 'midi/xexec_t13m.c (copy of the X2 loader: tools/xexec/xexec.c plus "poke")',
                 'audio': 'audio/xexec_t13.c (tools/xexec/xexec.c plus "poke")',
                 'stop': 'tools/xexec/xexec.c (unchanged)', 'end': 'tools/xexec/xexec.c (unchanged)'}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def first_line(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[0]


files = {str(p.relative_to(HERE)): sha(p) for p in sorted(HERE.rglob('*'))
         if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
manifest = {
    'id': 'T13-PLAYBACK-V1',
    'packet': 'T1.3 playback core: clock, transport, launch timing, MIDI and unwarped audio clip playback, stopping '
              '(static analysis of the Live Engine and both Live corpora; extracted execution, ADR 0003 label X)',
    'target': 'Ableton Live 12 Suite 12.4.3',
    'pages': ['wiki/research/playback-core.md', 'wiki/specs/playback-core.md'],
    'slices': {k: {'path': p, 'sha256': sha(p), 'image_base': b} for k, (p, b) in SLICES.items()},
    'harness': {'tools/xexec/xexec.py (driver; copied unchanged into transport/ and audio/)': sha(ROOT / 'tools/xexec/xexec.py'),
                'tools/xexec/xexec.c (base of every loader)': sha(ROOT / 'tools/xexec/xexec.c'),
                'loaders': {a: {'source': LOADER_SOURCE[a], 'path': p, 'sha256': sha(p) if Path(p).exists() else None}
                            for a, p in LOADERS.items()}},
    'tools': {'gcc': first_line(['gcc', '--version']), 'gdb': first_line(['gdb', '--version']),
              'objdump': first_line(['objdump', '--version']), 'python': platform.python_version(),
              'glibc': platform.libc_ver()[1], 'kernel': platform.release()},
    'commands': ['sh run.sh'],
    'executed_live_application': False,
    'executed_original_code': 'Live x86_64 functions named in each area\'s scripts and matching tables, in the xexec '
                              'harness on Linux x86_64, with hand-built inputs; imports bound to glibc (called: memcpy, bzero, fmod, '
                              'powf, exp, sinf, exp10f, malloc, operator new, C++ guards; see raw outputs)',
    'static_tools': ['lookup.py (decompiled corpora: arm, x86, eng)', 'peek.py (slice words)', 'objdump',
                     'per-area matching scripts'],
    'files': files,
}
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
print(f'manifest.json: {len(files)} files')
