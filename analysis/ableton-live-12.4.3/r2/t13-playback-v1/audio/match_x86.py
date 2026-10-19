"""Match Engine x86_64 functions to Live x86_64 functions by body size and byte similarity (read-only; output is data).

usage: python3 -I match_x86.py <engine-entry-hex>...
For each Engine function (entry and body size from the Engine corpus), every Live x86_64 corpus function of
the same body size is compared byte by byte; candidates with >= 70% identical bytes are printed best first.
Differences are expected only in rip-relative displacements and call targets, so an exact compile scores
high but rarely 100%. A match is then confirmed by reading both disassemblies (see notes in the reply).
Depends on the T13 entry-map caches built by ../lookup.py (T13_CACHE) and on the two slices.
"""
import os, pickle, struct, sys
from collections import defaultdict

CACHE = os.environ['T13_CACHE']
ENG = '/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64'
LIVE = '/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64'


def segs(b):
    ncmds, off, out = struct.unpack_from('<I', b, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            vm, vs, fo, fs = struct.unpack_from('<QQQQ', b, off + 24)
            out.append((vm, fo, fs))
        off += size
    return out


def read(b, sg, va, n):
    fo = next(fo + va - vm for vm, fo, fs in sg if vm <= va < vm + fs)
    return b[fo:fo + n]


def main():
    eng = pickle.load(open(os.path.join(CACHE, 't13-entry-map-eng.pickle'), 'rb'))
    live = pickle.load(open(os.path.join(CACHE, 't13-entry-map-x86.pickle'), 'rb'))
    by_size = defaultdict(list)
    for e, (_, _, n, s) in live.items():
        by_size[s].append(e)
    eb, lb = open(ENG, 'rb').read(), open(LIVE, 'rb').read()
    es, ls = segs(eb), segs(lb)
    for e in sys.argv[1:]:
        _, _, name, size = eng[e]
        a = read(eb, es, int(e, 16), size)
        scored = []
        for c in by_size.get(size, []):
            bb = read(lb, ls, int(c, 16), size)
            same = sum(x == y for x, y in zip(a, bb)) / size
            if same >= 0.7:
                scored.append((same, c))
        scored.sort(reverse=True)
        print(e, size, name, '->', ' '.join(f'{c}:{s:.3f}' for s, c in scored[:4]) or 'none')


if __name__ == '__main__':
    main()
