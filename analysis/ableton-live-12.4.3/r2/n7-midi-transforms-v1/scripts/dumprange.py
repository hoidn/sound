"""dumprange.py LO HI OUT: write all corpus functions with entry in [LO,HI) to OUT (one file, separated)."""
import sys, json, glob
lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
out = open(sys.argv[3], 'w'); n = 0
for p in sorted(glob.glob('/var/tmp/sound-analysis/corpus/decomp/chunks/chunk-*.jsonl')):
    with open(p) as f:
        first = f.readline()
        if not first: continue
        e0 = int(json.loads(first)['entry'].split(':')[-1], 16)
        if e0 >= hi: break
        f.seek(0)
        for line in f:
            r = json.loads(line); e = r['entry']
            if ':' in e: continue
            a = int(e, 16)
            if lo <= a < hi:
                out.write('\n/////// %s %s %s\n' % (e, r['name'], r['state'])); out.write(r.get('code') or r.get('partial_code') or ''); n += 1
print(n)
