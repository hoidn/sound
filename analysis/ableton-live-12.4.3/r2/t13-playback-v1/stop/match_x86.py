"""Match named Engine x86_64 functions to Live x86_64 functions (analyst tool; output is data).

The Engine bundle and Live x86_64 are separate compiles of the same engine sources. Candidates are Live functions
whose body size in bytes is identical to the Engine function's. Each candidate is scored by the overlap (multiset
Jaccard) of the body sizes of its direct callees with the Engine function's (calls index). The best two are printed
with their scores; 'unique' means exactly one candidate scores 1.0, 'best' means the top score is strictly highest.
usage: python3 -I match_x86.py <engine-entry>...
Depends on the corpora's decomp chunks (via the cached entry maps in $T13_CACHE) and indexes/calls.jsonl.
"""
import collections, json, os, pickle, sys

C = os.environ['T13_CACHE']
ROOT = {'eng': '/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/corpus',
        'x86': '/var/tmp/sound-analysis/corpus-x86'}


def load(which):
    m = pickle.load(open(f'{C}/t13-entry-map-{which}.pickle', 'rb'))
    size = {int(e, 16): s for e, (_, _, _, s) in m.items()}
    name = {int(e, 16): n for e, (_, _, n, _) in m.items()}
    callees = collections.defaultdict(list)
    for line in open(ROOT[which] + '/indexes/calls.jsonl'):
        r = json.loads(line)
        if r['kind'] == 'call' and r['callee']:
            callees[int(r['caller'], 16)].append(int(r['callee'], 16))
    return size, name, callees


def sig(size, callees, f):
    return size.get(f), tuple(sorted(size.get(c, -1) for c in callees.get(f, [])))


def main():
    es, en, ec = load('eng')
    xs, xn, xc = load('x86')
    by_size = collections.defaultdict(list)
    for f, s in xs.items():
        by_size[s].append(f)
    for a in sys.argv[1:]:
        f = int(a, 16)
        want = sig(es, ec, f)
        wc = collections.Counter(want[1])
        scored = []
        for g in by_size[want[0]]:
            gc = collections.Counter(sig(xs, xc, g)[1])
            union = sum((wc | gc).values())
            scored.append(((sum((wc & gc).values()) / union) if union else 1.0, g))
        scored.sort(reverse=True)
        top = ' '.join(f'{hex(g)}:{sc:.2f}' for sc, g in scored[:2]) or 'none'
        tag = ('unique' if scored and scored[0][0] == 1.0 and (len(scored) == 1 or scored[1][0] < 1.0) else
               'best' if scored and (len(scored) == 1 or scored[0][0] > scored[1][0]) else 'ambiguous')
        print(f'{a} {en.get(f)} size={want[0]} ncallees={len(want[1])} -> {top} ({tag}, {len(scored)} same-size)')


if __name__ == '__main__':
    main()
