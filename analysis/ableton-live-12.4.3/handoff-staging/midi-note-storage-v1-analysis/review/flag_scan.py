"""Reviewer check (analyst-side): byte stores at offset +0x2c in a code address range, and in
any corpus function that calls the load-context accessors (flag getter 0x1015192c0, payload
getter 0x1015183fc) or passes through the XML reader setup 0x10146b258.
usage: python3 -I flag_scan.py <chunks dir> <lo hex> <hi hex>"""
import glob, json, os, re, sys
lo, hi = int(sys.argv[2], 16), int(sys.argv[3], 16)
st = re.compile(r"\*\(undefined1 \*\)\((?:\(long\))?[^)]*\+ 0x2c\) = ([^;]+);")
tags = ('FUN_1015192c0', 'FUN_1015183fc', 'FUN_10146b258')
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'chunk-*.jsonl'))):
    for line in open(f):
        r = json.loads(line); c = r['code'] or ''
        e = int(r['entry'], 16)
        ws = st.findall(c)
        if ws and (lo <= e < hi or any(t in c for t in tags)):
            print(r['entry'], r['name'], 'in-range' if lo <= e < hi else 'calls-accessor', ws)
