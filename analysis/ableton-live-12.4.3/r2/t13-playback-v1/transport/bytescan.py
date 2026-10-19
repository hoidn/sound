"""Find byte patterns (hex, '..' = any byte) in a Mach-O slice's __TEXT and print image VAs (analyst tool; output is data).
usage: python3 -I bytescan.py <slice> <base> <hexpattern>...   base: 0x100000000 for Live x86_64, 0 for the Engine
"""
import re, sys
path, base = sys.argv[1], int(sys.argv[2], 16)
b = open(path, 'rb').read()
for pat in sys.argv[3:]:
    rx = re.compile(b''.join(b'.' if t == '..' else re.escape(bytes.fromhex(t)) for t in pat.split()), re.S)
    hits = [hex(m.start() + base) for m in rx.finditer(b)]
    print(pat, len(hits), ' '.join(hits[:40]))
