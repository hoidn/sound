# usage: python3 -I ddis.py <results-dir> <entry> [from_addr to_addr]  -> dossier disassembly lines
import json, sys
d = json.load(open(f'{sys.argv[1]}/functions/{sys.argv[2]}.json'))
lo = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0; hi = int(sys.argv[4], 16) if len(sys.argv) > 4 else 1 << 64
for i in d['disassembly']:
    a = int(i['address'], 16)
    if lo <= a <= hi: print(i['address'], i.get('text') or i)
