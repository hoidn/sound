"""Direct-call reachability over a corpus calls index (analyst tool; output is data).
usage: python3 -I reach.py <corpus dir> <depth> <root> <target>... [--grep REGEX]
Prints each target reached from root within depth direct calls (with one path), and, with --grep,
every reached function whose pseudocode matches REGEX. Indirect (vtable) calls are not followed."""
import collections, glob, json, re, sys
C, depth, root = sys.argv[1], int(sys.argv[2]), sys.argv[3].lower()
args = sys.argv[4:]
rx = None
if '--grep' in args:
    i = args.index('--grep'); rx = re.compile(args[i + 1]); args = args[:i]
targets = {a.lower() for a in args}
out = collections.defaultdict(set)
for line in open(C + '/indexes/calls.jsonl'):
    r = json.loads(line)
    callee = r.get('callee_resolved') or r.get('callee')
    if r.get('caller') and callee:
        out[r['caller']].add(callee)
prev, frontier, seen = {root: None}, [root], {root}
for _ in range(depth):
    nxt = []
    for f in frontier:
        for g in out.get(f, ()):
            if g not in seen:
                seen.add(g); prev[g] = f; nxt.append(g)
    frontier = nxt
for t in sorted(targets):
    if t in seen:
        p, path = t, []
        while p: path.append(p); p = prev[p]
        print('REACHED', t, ' <- '.join(path))
    else:
        print('not reached', t)
print('functions reached:', len(seen))
if rx:
    for f in sorted(glob.glob(C + '/decomp/chunks/*.jsonl')):
        for line in open(f):
            j = line.find('"entry":"'); e = line[j + 9:line.index('"', j + 9)]
            if e in seen:
                r = json.loads(line)
                if r['code'] and rx.search(r['code']):
                    print('GREP', e, r['name'])
