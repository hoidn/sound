"""Reviewer check (analyst-side): list every corpus function that names a load-context
vtable (0x106675000-0x106677000) and every assignment it makes at offset +0x2c.
usage: python3 -I ctx_scan.py /var/tmp/sound-analysis/corpus/decomp/chunks"""
import glob, json, os, re, sys
vt = re.compile(r'_10667([0-9a-f]{4})\b')
w = re.compile(r'0x2c\) = ([^;]+);')
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'chunk-*.jsonl'))):
    for line in open(f):
        if '_10667' not in line:
            continue
        r = json.loads(line); c = r['code'] or ''
        vs = sorted({'0x10667' + m for m in vt.findall(c) if 0x5000 <= int(m, 16) < 0x7000})
        if vs:
            print(r['entry'], r['name'], ' '.join(vs), w.findall(c))
