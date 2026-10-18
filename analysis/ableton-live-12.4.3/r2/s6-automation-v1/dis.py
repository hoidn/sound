"""Print a retained dossier's disassembly (analyst helper; output is data).
usage: python3 -I dis.py <results/<id>/functions/<entry>.json> [from_addr to_addr]"""
import json, sys
d = json.load(open(sys.argv[1]))
lo, hi = (int(sys.argv[2], 16), int(sys.argv[3], 16)) if len(sys.argv) > 3 else (0, 1 << 64)
for i in d['disassembly']:
    if lo <= int(i['address'], 16) <= hi:
        print(i['address'], i['text'])
