"""Read-only lookups over the arm64 (C1) and x86_64 (C1-x86) Live corpora (analyst tool; output is data).

usage: python3 -I lookup.py {arm|x86} code <entry>...    decompiled code of functions
       python3 -I lookup.py {arm|x86} str <regex>        strings whose value matches, with referencing functions
       python3 -I lookup.py {arm|x86} callers <entry>    direct call edges into <entry>
       python3 -I lookup.py {arm|x86} callees <entry>    direct call edges out of <entry>
       python3 -I lookup.py {arm|x86} grep <regex>       functions whose code matches (scans all chunks)
       python3 -I lookup.py {arm|x86} excerpt <out.jsonl> <entry>...  retain records with chunk, offset, line SHA-256
Copied from n1-transport-state-v1/corpus_lookup.py with a corpus switch. Depends on
/var/tmp/sound-analysis/{corpus,corpus-x86}/{decomp/chunks,indexes}; caches an entry->chunk map in
$X2_CACHE (default: the system temp directory).
"""
import glob, hashlib, json, os, pickle, re, sys, tempfile

CORPUS = {'arm': '/var/tmp/sound-analysis/corpus', 'x86': '/var/tmp/sound-analysis/corpus-x86'}


def entry_map(c, which):
    cache = os.path.join(os.environ.get('X2_CACHE', tempfile.gettempdir()), f'x2-entry-map-{which}.pickle')
    if os.path.exists(cache):
        return pickle.load(open(cache, 'rb'))
    m = {}
    for f in sorted(glob.glob(c + '/decomp/chunks/*.jsonl')):
        with open(f, 'rb') as fh:
            off = 0
            for line in fh:
                j = line.find(b'"entry":"')
                m[line[j + 9:line.index(b'"', j + 9)].decode()] = (f, off)
                off += len(line)
    pickle.dump(m, open(cache, 'wb'))
    return m


def record(c, which, e):
    f, off = entry_map(c, which)[e.lower()]
    with open(f, 'rb') as fh:
        fh.seek(off)
        line = fh.readline()
    return f, off, line


def main():
    which, cmd, args = sys.argv[1], sys.argv[2], sys.argv[3:]
    c = CORPUS[which]
    if cmd == 'code':
        for e in args:
            r = json.loads(record(c, which, e)[2])
            print(f"// {r['entry']} {r['name']} state={r['state']} body={r['body_ranges']}")
            print(r['code'])
    elif cmd == 'str':
        p = re.compile(args[0])
        for line in open(c + '/indexes/strings.jsonl'):
            r = json.loads(line)
            if p.search(r['value'] or ''):
                fns = sorted({x.get('function') for x in r['refs'] if x.get('function')}
                             | {v.get('function') for x in r['refs'] for v in (x.get('via') or [])}, key=str)
                print(r['address'], json.dumps(r['value']), r['type'], fns)
    elif cmd in ('callers', 'callees'):
        a, key = args[0].lower(), 'callee' if cmd == 'callers' else 'caller'
        for line in open(c + '/indexes/calls.jsonl'):
            if a in line:
                r = json.loads(line)
                if r[key] == a or (key == 'callee' and r.get('callee_resolved') == a):
                    print(r['caller'], r['site'], r['kind'], '->', r['callee'], r['callee_name'])
    elif cmd == 'grep':
        p = re.compile(args[0])
        for f in sorted(glob.glob(c + '/decomp/chunks/*.jsonl')):
            for line in open(f):
                r = json.loads(line)
                if r['code'] and p.search(r['code']):
                    print(r['entry'], r['name'])
    elif cmd == 'excerpt':
        with open(args[0], 'a') as o:
            for e in args[1:]:
                f, off, line = record(c, which, e)
                o.write(json.dumps({'corpus': which, 'chunk': os.path.basename(f), 'offset': off,
                                    'line_sha256': hashlib.sha256(line.rstrip(b'\n')).hexdigest(),
                                    'record': json.loads(line)}) + '\n')


if __name__ == '__main__':
    main()
