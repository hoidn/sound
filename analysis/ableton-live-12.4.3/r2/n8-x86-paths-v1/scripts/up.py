# usage: python3 -I up.py <idx.pkl> <depth> <entry>...  -> transitive direct callers (BFS), one line per edge
import sys, pickle
C, off, callers, callees, names = pickle.load(open(sys.argv[1], 'rb'))
depth = int(sys.argv[2]); seen = set(); frontier = [hex(int(a, 16)) for a in sys.argv[3:]]
for d in range(depth):
    nxt = []
    for a in frontier:
        if a in seen: continue
        seen.add(a); cs = callers.get(a, [])
        if not cs: print(d, a, names.get(a), '<- (no direct callers)')
        for s, c, k in cs:
            print(d, a, '<-', c, names.get(c), s, k); nxt.append(c)
    frontier = nxt
