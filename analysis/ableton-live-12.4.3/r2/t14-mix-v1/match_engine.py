"""Locate the Live x86_64 twin of an Ableton Live Engine x86_64 function by byte similarity.

usage: python3 -I match_engine.py ENGINE_ADDR LENGTH [ENGINE_ADDR LENGTH ...]
For each engine function [ADDR, ADDR+LENGTH) it takes every 12-byte window, finds exact occurrences
in the Live x86_64 slice, votes on the implied function start, and reports the best start with the
fraction of identical bytes over LENGTH (RIP-relative displacements and call targets differ between
the two images, so 100% is not expected). Read-only; output is data.
"""
import collections, sys
ENGINE = '/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64'
LIVE = '/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64'
LIVE_BASE = 0x100000000

def best(e, l, a, n, w=12):
    votes = collections.Counter()
    for i in range(0, n - w + 1):
        pat = e[a + i:a + i + w]
        if len(set(pat)) < 4:
            continue
        p, hits = l.find(pat), 0
        while p != -1 and hits < 8:
            votes[p - i] += 1; hits += 1
            p = l.find(pat, p + 1)
    out = []
    for start, v in votes.most_common(3):
        same = sum(x == y for x, y in zip(e[a:a + n], l[start:start + n]))
        out.append((start + LIVE_BASE, v, same))
    return out

if __name__ == '__main__':
    e, l = open(ENGINE, 'rb').read(), open(LIVE, 'rb').read()
    args = sys.argv[1:]
    for k in range(0, len(args), 2):
        a, n = int(args[k], 16), int(args[k + 1], 0)
        cands = best(e, l, a, n)
        print(f'engine {a:#x} len {n}: ' + '; '.join(f'live {s:#x} votes {v} same {m}/{n}' for s, v, m in cands))
