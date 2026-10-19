"""Read-only lookups over the C1/C2 Live corpus (analyst tool; output is data).

usage: python3 -I corpus_lookup.py code <entry>...      decompiled code of functions
       python3 -I corpus_lookup.py str <regex>          strings whose value matches, with referencing functions
       python3 -I corpus_lookup.py callers <entry>      direct call edges into <entry>
       python3 -I corpus_lookup.py callees <entry>      direct call edges out of <entry>
       python3 -I corpus_lookup.py grep <regex>         functions whose code matches (slow: scans all chunks)
       python3 -I corpus_lookup.py excerpt <out.jsonl> <entry>...  retain records with chunk file, byte offset, line SHA-256
Depends on /var/tmp/sound-analysis/corpus/{decomp/chunks,indexes}; builds a cached entry->chunk map.
"""
import json, os, re, sys, glob, pickle
C = '/var/tmp/sound-analysis/corpus-x86'
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.entry-map.pickle')
if os.environ.get('N1_CACHE'): CACHE = os.environ['N1_CACHE']

def entry_map():
    if os.path.exists(CACHE):
        return pickle.load(open(CACHE, 'rb'))
    m = {}
    for f in sorted(glob.glob(C + '/decomp/chunks/*.jsonl')):
        with open(f, 'rb') as fh:
            off = 0
            for line in fh:
                j = line.find(b'"entry":"')
                m[line[j + 9:line.index(b'"', j + 9)].decode()] = (f, off)
                off += len(line)
    pickle.dump(m, open(CACHE, 'wb'))
    return m

def code(entries):
    m = entry_map()
    for e in entries:
        f, off = m[e.lower()]
        with open(f, 'rb') as fh:
            fh.seek(off); r = json.loads(fh.readline())
        print(f"// {r['entry']} {r['name']} state={r['state']} warnings={r['warnings']}")
        print(r['code'])

def strings(rx):
    p = re.compile(rx)
    for line in open(C + '/indexes/strings.jsonl'):
        r = json.loads(line)
        if p.search(r['value'] or ''):
            fns = sorted({(x.get('function'), x.get('function_name')) for x in r['refs'] if x.get('function')} | {(v.get('function'), v.get('function_name')) for x in r['refs'] for v in (x.get('via') or [])}, key=str)
            print(r['address'], json.dumps(r['value']), r['type'], fns)

def edges(addr, key):
    a = addr.lower()
    for line in open(C + '/indexes/calls.jsonl'):
        if a in line:
            r = json.loads(line)
            if r[key] == a or (key == 'callee' and r.get('callee_resolved') == a):
                print(r['caller'], r['caller_name'], r['site'], r['kind'], '->', r['callee'], r['callee_name'])

def grep(rx):
    p = re.compile(rx)
    for f in sorted(glob.glob(C + '/decomp/chunks/*.jsonl')):
        for line in open(f):
            r = json.loads(line)
            if r['code'] and p.search(r['code']):
                print(r['entry'], r['name'])

def excerpt(out, entries):
    import hashlib
    m = entry_map()
    with open(out, 'w') as o:
        for e in entries:
            f, off = m[e.lower()]
            with open(f, 'rb') as fh:
                fh.seek(off); line = fh.readline()
            r = json.loads(line)
            o.write(json.dumps({'chunk': os.path.basename(f), 'offset': off,
                                'line_sha256': hashlib.sha256(line.rstrip(b'\n')).hexdigest(), 'record': r}) + '\n')

if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    {'code': lambda: code(args), 'str': lambda: strings(args[0]), 'callers': lambda: edges(args[0], 'callee'),
     'callees': lambda: edges(args[0], 'caller'), 'grep': lambda: grep(args[0]), 'excerpt': lambda: excerpt(args[0], args[1:])}[cmd]()
