"""Print disassembly from a kept dossier JSON, optionally between two addresses (analyst helper; output is data).
usage: python3 -I dis.py <functions/0x....json> [from_hex [to_hex]]"""
import json, sys
j = json.load(open(sys.argv[1]))
lo = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0
hi = int(sys.argv[3], 16) if len(sys.argv) > 3 else 1 << 64
for i in j['disassembly']:
    a = int(i['address'], 16)
    if lo <= a <= hi:
        print(i['address'], i['text'])
