import json, glob, re, sys
lo, hi = int(sys.argv[1],16), int(sys.argv[2],16)
for f in sorted(glob.glob('/var/tmp/sound-analysis/corpus/decomp/chunks/*.jsonl')):
    for line in open(f):
        i=line.find('"entry":"')+9; e=int(line[i:line.index('"',i)],16)
        if not lo<=e<hi: continue
        r=json.loads(line); c=r['code'] or ''
        m=re.fullmatch(r'\s*\n?\S+ \S+\((void|undefined8 param_1|long param_1)\)\s*\{\s*return (0x[0-9a-f]+|\d+);\s*\}\s*', c.strip(), re.S)
        if m and m.group(2) in ('4','0x20','8','0x10'): print(hex(e), m.group(2))
