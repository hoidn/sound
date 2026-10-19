"""Match Engine x86_64 functions (base 0) to Live x86_64 functions (base 0x100000000) by body size and
neighbourhood: a candidate Live entry must have the same body size as the Engine function, and the score is
the number of the 6 preceding and 6 following Engine functions whose entry + the same delta is a Live entry of
the same body size. Searches deltas within +-RANGE of BASE. Read-only; output is data (TSV:
engine entry, size, name, live entry, delta, score/12).
usage: T13_CACHE=... python3 -I midi/match_eng_x86.py <engine-name-regex>"""
import bisect, os, pickle, re, sys
C = os.environ['T13_CACHE']
eng = pickle.load(open(os.path.join(C, 't13-entry-map-eng.pickle'), 'rb'))
x86 = pickle.load(open(os.path.join(C, 't13-entry-map-x86.pickle'), 'rb'))
BASE, RANGE = int(os.environ.get('BASE', '0x1019cf350'), 16), int(os.environ.get('RANGE', '0x80000'), 16)
E = sorted((int(e, 16), v[3], v[2]) for e, v in eng.items())
X = {int(e, 16): v[3] for e, v in x86.items()}
XS = sorted(X)
pos = {a: i for i, (a, _, _) in enumerate(E)}
pat = re.compile(sys.argv[1])
for a, s, n in E:
    if not pat.search(n or ''):
        continue
    i = pos[a]
    lo, hi = bisect.bisect_left(XS, a + BASE - RANGE), bisect.bisect_right(XS, a + BASE + RANGE)
    best = None
    for x in XS[lo:hi]:
        if X[x] != s:
            continue
        d = x - a
        sc = sum(1 for j in range(max(0, i - 6), min(len(E), i + 7)) if j != i and X.get(E[j][0] + d) == E[j][1])
        if best is None or sc > best[2]:
            best = (x, d, sc)
    print(f"{a:#x}\t{s}\t{n}\t" + (f"{best[0]:#x}\t{best[1]:#x}\t{best[2]}/12" if best else "-\t-\t-"))
