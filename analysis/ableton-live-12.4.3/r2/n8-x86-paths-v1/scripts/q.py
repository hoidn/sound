# usage: python3 -I q.py <idx.pkl> code|callers|callees|name <entry>...
import sys, pickle, json
C, off, callers, callees, names = pickle.load(open(sys.argv[1], 'rb'))
cmd = sys.argv[2]
for a in sys.argv[3:]:
    a = hex(int(a, 16))
    if cmd == 'code':
        f, p = off[a]; fh = open(C + '/decomp/chunks/' + f, 'rb'); fh.seek(p); r = json.loads(fh.readline())
        print('//', a, r['name'], r['state'], r.get('error') or '', 'sig:', r['signature']); print(r['code'])
    elif cmd == 'callers':
        for s, c, k in callers.get(a, []): print(a, '<-', c, names.get(c), s, k)
    elif cmd == 'callees':
        for s, t, n, k in callees.get(a, []): print(a, '->', t, n, s, k)
    elif cmd == 'name': print(a, names.get(a))
