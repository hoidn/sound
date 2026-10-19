"""Write disassembly of the cited Live x86_64 and Engine functions (objdump, from each function's body range in
excerpts.jsonl) and FP-opcode classes of cited arm64 functions (fp_opcodes.py) to disasm-x86.txt, disasm-eng.txt
and arm64-fp.txt (analyst tool; output is data). usage: python3 -I disasm.py"""
import json, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
X86 = ['0x101af9d50', '0x101af9eb0', '0x101afb500', '0x101af9bb0', '0x102278eb0', '0x10227c780', '0x10227c4d0',
       '0x101b119a0', '0x101b179a0', '0x101b17510', '0x101b6c540', '0x101b6caa0', '0x101b06ad0', '0x101b05a60',
       '0x102842c50', '0x10269d2d0', '0x10285cce0', '0x10288c480', '0x1027e8480', '0x101b1d820', '0x101b3dcc0']
ENG = ['0x12a9f0', '0x12c1a0', '0x9a45d0', '0x1481c0', '0x14e4d0', '0x14dca0', '0x137770', '0x19d230']
ARM = [('0x101b37194', 66), ('0x102188f34', 166), ('0x101ae6134', 2), ('0x101aebbec', 2), ('0x101aeb668', 24)]
SL = {'x86': ('/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64', '0x100000000'),
      'eng': ('/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64', '0')}
rec = {}
for line in open(HERE / 'excerpts.jsonl'):
    r = json.loads(line)
    rec[(r['corpus'], r['record']['entry'])] = r['record']
for which, entries, out in (('x86', X86, 'disasm-x86.txt'), ('eng', ENG, 'disasm-eng.txt')):
    path, vma = SL[which]
    with open(HERE / out, 'w') as f:
        for e in entries:
            r = rec[(which, e)]
            for lo, hi in r['body_ranges']:
                p = subprocess.run(['objdump', '-D', '-b', 'binary', '-m', 'i386:x86-64', f'--adjust-vma={vma}',
                                    '--no-show-raw-insn', f'--start-address={lo}', f'--stop-address={int(hi, 16) + 1:#x}', path],
                                   capture_output=True, text=True, check=True)
                f.write(f'### {which} {e} {r["name"]} [{lo}, {hi}]\n')
                f.write('\n'.join(l for l in p.stdout.splitlines() if l[:1] == ' ' and ':' in l) + '\n')
with open(HERE / 'arm64-fp.txt', 'w') as f:
    for va, n in ARM:
        p = subprocess.run(['python3', '-I', str(HERE / 'fp_opcodes.py'), str(HERE.parents[2] / 'derived' / 'Live.arm64'), va, str(n)],
                           capture_output=True, text=True, check=True)
        f.write(f'### arm64 {va} ({n} words)\n' + p.stdout)
