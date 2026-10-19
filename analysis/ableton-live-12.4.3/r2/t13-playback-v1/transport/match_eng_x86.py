"""Match Live Engine (x86_64, named) functions to Live x86_64 functions by function order and body size
(analyst tool; output is data). A match needs the engine function and its K neighbours on each side to have
a Live counterpart at one constant address delta with identical body sizes.

usage: python3 -I match_eng_x86.py <engine entry or name regex>...
Depends on the entry-map caches built by ../lookup.py in $T13_CACHE.
"""
import bisect, os, pickle, re, sys

C = os.environ['T13_CACHE']
K = 4


def load(which):
    m = pickle.load(open(os.path.join(C, f't13-entry-map-{which}.pickle'), 'rb'))
    return sorted((int(k, 16), v[3], v[2]) for k, v in m.items())


eng, x86 = load('eng'), load('x86')
xsize = {a: s for a, s, _ in x86}
xaddr = [a for a, _, _ in x86]
xsizes = [s for _, s, _ in x86]


def match(i):
    a, s, _ = eng[i]
    win = eng[max(0, i - K):i + K + 1]
    # candidate deltas: every Live function with the same size
    for j, xs in enumerate(xsizes):
        if xs != s:
            continue
        d = xaddr[j] - a
        if all(xsize.get(b + d) == t for b, t, _ in win):
            yield xaddr[j], d


def main():
    for arg in sys.argv[1:]:
        if arg.startswith('0x'):
            idx = [bisect.bisect_left(eng, (int(arg, 16),))]
        else:
            p = re.compile(arg)
            idx = [i for i, (_, _, n) in enumerate(eng) if p.search(n or '')]
        for i in idx:
            a, s, n = eng[i]
            ms = list(match(i))
            print(f'{a:#x}\t{s}\t{n}\t' + (' '.join(f'{x:#x}(d={d:#x})' for x, d in ms) or 'NO-MATCH'))


if __name__ == '__main__':
    main()
