"""Print dossier disassembly (analyst tool; output is data).
usage: python3 -I disasm.py <functions/0x....json> [start_hex end_hex]"""
import json, sys
d = json.load(open(sys.argv[1]))
lo, hi = (int(sys.argv[2], 16), int(sys.argv[3], 16)) if len(sys.argv) > 3 else (0, 1 << 64)
for i in d['disassembly']:
    if lo <= int(i['address'], 16) <= hi:
        print(i['address'], i['text'])
