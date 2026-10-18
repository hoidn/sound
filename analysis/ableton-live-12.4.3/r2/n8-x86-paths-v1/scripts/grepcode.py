# usage: python3 -I grepcode.py <corpus-root> <lo-hex> <hi-hex> <regex>...  -> entries in [lo,hi) whose pseudocode matches all regexes
import sys, json, glob, re
C, lo, hi = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16); pats = [re.compile(p) for p in sys.argv[4:]]
for f in sorted(glob.glob(C + '/decomp/chunks/*.jsonl')):
    for line in open(f):
        r = json.loads(line); e = int(r['entry'], 16)
        if lo <= e < hi and r.get('code') and all(p.search(r['code']) for p in pats): print(r['entry'], r['name'])
