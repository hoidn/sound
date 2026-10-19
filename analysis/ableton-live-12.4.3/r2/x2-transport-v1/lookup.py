"""Read-only lookups over the decompiled corpora (analyst tool; output is data).

usage: python3 -I lookup.py {arm|x86} code <entry>...    decompiled code of functions
       python3 -I lookup.py {arm|x86} str <regex>        strings matching, with referencing functions
       python3 -I lookup.py {arm|x86} callers <entry>    direct call edges into <entry>
       python3 -I lookup.py {arm|x86} callees <entry>    direct call edges out of <entry>
Corpora: /var/tmp/sound-analysis/corpus (arm64) and corpus-x86. The entry -> chunk map is cached
under LOOKUP_CACHE (default: /var/tmp/sound-analysis/scratch/x2-transport-v1), never next to this file.
"""
import glob, json, os, pickle, re, sys
ROOTS = {'arm': '/var/tmp/sound-analysis/corpus', 'x86': '/var/tmp/sound-analysis/corpus-x86'}


def entry_map(c, tag):
    d = os.environ.get('LOOKUP_CACHE', '/var/tmp/sound-analysis/scratch/x2-transport-v1')
    os.makedirs(d, exist_ok=True)
    cache = os.path.join(d, f'x2-entry-map-{tag}.pickle')
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


def main(tag, cmd, *args):
    c = ROOTS[tag]
    if cmd == 'code':
        m = entry_map(c, tag)
        for e in args:
            f, off = m[e.lower()]
            with open(f, 'rb') as fh:
                fh.seek(off)
                r = json.loads(fh.readline())
            print(f"// {r['entry']} {r['name']} state={r['state']} warnings={r['warnings']}")
            print(r['code'])
    elif cmd == 'str':
        p = re.compile(args[0])
        for line in open(c + '/indexes/strings.jsonl'):
            r = json.loads(line)
            if p.search(r['value'] or ''):
                fns = sorted({x.get('function') for x in r['refs'] if x.get('function')}, key=str)
                print(r['address'], json.dumps(r['value']), fns)
    elif cmd in ('callers', 'callees'):
        a, key = args[0].lower(), 'callee' if cmd == 'callers' else 'caller'
        for line in open(c + '/indexes/calls.jsonl'):
            if a in line:
                r = json.loads(line)
                if r[key] == a or (key == 'callee' and r.get('callee_resolved') == a):
                    print(r['caller'], r['site'], r['kind'], '->', r['callee'], r['callee_name'])


if __name__ == '__main__':
    main(*sys.argv[1:])
