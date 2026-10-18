# usage: python3 -I sref.py <strings.jsonl> <0xaddr|=exact|~substr>...  -> referencing functions
import sys, json
want = sys.argv[2:]
addrs = {hex(int(w, 16)) for w in want if w.startswith('0x')}
ex = {w[1:] for w in want if w.startswith('=')}
sub = [w[1:] for w in want if w.startswith('~')]
for line in open(sys.argv[1]):
    r = json.loads(line); v = r.get('value') or ''
    if r['address'] in addrs or v in ex or any(s in v for s in sub):
        fs = sorted({x.get('function') or ('via:' + ','.join(y['function'] or '?' for y in x.get('via', []))) for x in r['refs']}, key=str)
        print(r['address'], repr(v[:100]), '->', ' '.join(fs) or 'NOREFS')
