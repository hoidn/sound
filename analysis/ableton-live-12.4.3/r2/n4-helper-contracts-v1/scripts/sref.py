# usage: sref.py <hexaddr|=exact|~substr>...  -> referencing functions from strings.jsonl
import sys, json
want=sys.argv[1:]
addrs={hex(int(w,16)) for w in want if w.startswith('0x')}
ex={w[1:] for w in want if w.startswith('=')}
sub=[w[1:] for w in want if w.startswith('~')]
for line in open('/var/tmp/sound-analysis/corpus/indexes/strings.jsonl'):
    r=json.loads(line); v=r.get('value') or ''
    if r['address'] in addrs or v in ex or any(s in v for s in sub):
        fs=sorted({(x.get('function'),x.get('function_name')) for x in r['refs']},key=str)
        print(r['address'],repr(v[:90]),'->',' '.join(f'{f}' for f,n in fs) or 'NOREFS')
