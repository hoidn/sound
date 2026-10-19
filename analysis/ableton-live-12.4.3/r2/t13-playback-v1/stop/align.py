"""Print the direct callees of a matched Live x86_64 / arm64 function pair side by side, in call-site order, with
each callee's body size, to align counterparts by position (analyst tool; output is data).
usage: python3 -I align.py <x86-entry> <arm64-entry>    (uses the calls indexes and $T13_CACHE entry maps)"""
import json, os, pickle, sys
C = os.environ['T13_CACHE']
ROOT = {'x86': '/var/tmp/sound-analysis/corpus-x86', 'arm': '/var/tmp/sound-analysis/corpus'}


def callees(which, f):
    m = pickle.load(open(f'{C}/t13-entry-map-{which}.pickle', 'rb'))
    out = []
    for line in open(ROOT[which] + '/indexes/calls.jsonl'):
        if f in line:
            r = json.loads(line)
            if r['caller'] == f and r['callee']:
                out.append((int(r['site'], 16), r['callee'], m.get(r['callee'], (0, 0, '', 0))[3]))
    return sorted(out)


x, a = callees('x86', sys.argv[1].lower()), callees('arm', sys.argv[2].lower())
for i in range(max(len(x), len(a))):
    l = f'{x[i][1]} ({x[i][2]})' if i < len(x) else ''
    r = f'{a[i][1]} ({a[i][2]})' if i < len(a) else ''
    print(f'{i:3d} {l:28s} {r}')
