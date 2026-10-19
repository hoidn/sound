"""Write manifest.json: SHA-256 of evidence files, the X2 loader source/binary, the slice, and tool versions."""
import hashlib, json, platform, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
from xexec import SLICE                                            # noqa: E402
import os
BIN = Path(os.environ.get('X2_BIN', '/var/tmp/sound-analysis/xexec/x2-envelope-warp/xexec2'))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def first_line(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[0]


files = {str(p.relative_to(HERE)): sha(p) for p in sorted(HERE.rglob('*'))
         if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts and p.suffix != '.pickle'}
manifest = {
    'id': 'X2-ENVELOPE-WARP-V1',
    'packet': 'X2 extracted execution: automation-envelope evaluation and warp-marker mapping (ADR 0003, label X)',
    'target': 'Ableton Live 12 Suite 12.4.3, Live x86_64 slice',
    'slice': {'path': SLICE, 'sha256': sha(SLICE), 'image_base': '0x100000000'},
    'loader': {'source': 'analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/xexec2.c (copy of tools/xexec/xexec.c; X2 additions marked)',
               'xexec2.c_sha256': sha(HERE / 'xexec2.c'),
               'built_binary': {'path': str(BIN), 'sha256': sha(BIN) if BIN.exists() else None},
               'base_loader': 'tools/xexec/xexec.c', 'base_loader_sha256': sha(ROOT / 'tools/xexec/xexec.c')},
    'tools': {'gcc': first_line(['gcc', '--version']), 'gdb': first_line(['gdb', '--version']),
              'objdump': first_line(['objdump', '--version']), 'python': platform.python_version(),
              'glibc': platform.libc_ver()[1], 'libstdcxx': 'libstdc++.so.6 (Itanium demangler, std::string::append)',
              'kernel': platform.release()},
    'commands': ['sh run.sh'],
    'executed_live_application': False,
    'executed_original_code': 'x86_64 functions in addresses.json, run in the X2 harness on Linux x86_64',
    'added_import_bindings_over_x1': ['__ZNSt3__112__next_primeEm', '_getenv', '_mach_timebase_info',
        '_CFPreferencesCopyValue', 'expl', '___cxa_demangle', '_strstr/_strrchr/_strcpy/_strncpy/_memchr/_strnlen',
        'std::string::append(char*,size_t)', '____chkstk_darwin', 'stack-argument passing (ARG s:E), mkbuf, init, poke'],
    'note': 'Static initialisers are run via the init command; 295 of 3322 reach a trap/fault and are '
            'abandoned (none in the automation/warp class graph). The automation and warp classes are '
            'registered from a minimal registry subset before use. Heap addresses in raw/runs.jsonl vary '
            'with ASLR; the results file is stable.',
    'files': files,
}
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
print(f'manifest.json: {len(files)} files')
