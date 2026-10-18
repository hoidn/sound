"""Reviewer check (analyst-side): corpus-wide list of functions that call the shared object base
constructor FUN_10128ed98 and store a byte at offset +0x2c, with the stored values. Used to look
for any load-context constructor that leaves the post-load flag clear.
usage: python3 -I ctor_scan.py <chunks dir>"""
import glob, json, os, re, sys
st = re.compile(r"\*\(undefined1 \*\)\((?:\(long\))?[^)]*\+ 0x2c\) = ([^;]+);")
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'chunk-*.jsonl'))):
    for line in open(f):
        if 'FUN_10128ed98' not in line or '0x2c) = ' not in line:
            continue
        r = json.loads(line); c = r['code'] or ''
        ws = st.findall(c)
        if ws and 'FUN_10128ed98()' in c:
            print(r['entry'], r['name'], ws, '+0x28=-1' if '0xffffffff' in c else '')
