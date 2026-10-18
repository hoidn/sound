"""List string references from a dossier body in address order (analyst tool; output is data).
usage: python3 -I strrefs.py <functions/0x....json> [start_hex end_hex]"""
import json, sys
d = json.load(open(sys.argv[1]))
lo, hi = (int(sys.argv[2], 16), int(sys.argv[3], 16)) if len(sys.argv) > 3 else (0, 1 << 64)
for r in sorted(d['references_from_body'], key=lambda r: int(r['from'], 16)):
    s = r['target'].get('string')
    if s is not None and lo <= int(r['from'], 16) <= hi:
        print(r['from'], r['to'], repr(s))
