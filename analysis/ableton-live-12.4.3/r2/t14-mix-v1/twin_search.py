"""Locate Live x86_64 twins of Engine functions by byte comparison with RIP-relative displacements masked.

usage: python3 -I twin_search.py START:END...   (engine VAs; image base 0, VA == file offset)
For each engine function body [START, END) it masks the 4-byte displacement of every
RIP-relative operand and of rel32 calls/jumps (found with objdump), then searches the
Live x86_64 slice for the masked pattern. Prints Live VAs (file offset + 0x100000000).
Read-only; output is data.
"""
import re, subprocess, sys
ENGINE = '/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64'
LIVE = '/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64'

def masked(start, end):
    out = subprocess.run(['objdump', '-D', '-b', 'binary', '-m', 'i386:x86-64', f'--start-address={start:#x}',
                          f'--stop-address={end:#x}', ENGINE], capture_output=True, text=True, check=True).stdout
    eng = open(ENGINE, 'rb').read()
    rx = []
    for line in out.splitlines():
        m = re.match(r'\s*([0-9a-f]+):\s+((?:[0-9a-f]{2} )+)\s*(.*)', line)
        if not m:
            continue
        addr, raw, ins = int(m.group(1), 16), bytes.fromhex(m.group(2).replace(' ', '')), m.group(3)
        if not ins:   # continuation line of a long instruction
            rx.append(re.escape(raw)); continue
        if '(%rip)' in ins or re.match(r'(call|jmp|j[a-z]+)\s+[0-9a-f]+', ins) and len(raw) >= 5:
            # displacement position: last 4 bytes before any trailing immediate
            imm = 0
            if '(%rip)' in ins and ins.startswith(('cmp', 'mov', 'test', 'add', 'sub', 'and', 'or')) and '$' in ins:
                imm = len(raw) - raw.rfind(b'\x00') if False else 0
            d = len(raw) - 4 - imm
            rx.append(re.escape(raw[:d]) + b'....' + re.escape(raw[d + 4:]))
        else:
            rx.append(re.escape(raw))
    return re.compile(b''.join(rx), re.S)

if __name__ == '__main__':
    live = open(LIVE, 'rb').read()
    for spec in sys.argv[1:]:
        s, e = (int(x, 16) for x in spec.split(':'))
        hits = [hex(m.start() + 0x100000000) for m in masked(s, e).finditer(live)]
        print(spec, hits[:10], len(hits))
