"""Expected note-on/off song beats and sample indices for the proposed MIDI playback cases (analysis aid; data).

usage: python3 -I -B midi/cases.py > midi/results/cases.json
Rules used (see the fork report): note events at song beat B + (t - S) in the first pass and W_k + (t - Ls) in
pass k >= 1, W_1 = B + (Le - S), W_k+1 = W_k + (Le - Ls), all on the 1/3,843,840 lattice; note-off at
L(t + duration), or L(t + h) for a zero-length note. Sample rule (fork A dependency, not settled here): an event
at song beat b fires at sample ceil(b * spb) with spb = (SR / T) * 60 in binary64, T binary32, the transport
started at song beat 0 at sample 0 with constant tempo. The launch beat B comes from REQ-CLIP-LAUNCH-017 (fork B).
"""
import json
import math
import struct

H = 2.6015651015651016e-07


def f32(x):
    return struct.unpack('<f', struct.pack('<f', x))[0]


def L(x):
    s = 1.0 if x >= 0.0 else -1.0
    return (math.floor(abs(H * s * 0.5 + x) * 3843840.0) / 3843840.0) * s


def spb(sr, t):
    return (float(sr) / f32(t)) * 60.0


def smp(b, sr, t):
    return math.ceil(b * spb(sr, t))


SLIDE = [(0.5 * k, 0.25) for k in range(8)]   # B1 "Slide", key 51, velocity 100, off velocity 64


def events(notes, B, S, Ls, Le, looped, passes, end=None):
    """List (beat, kind, note index, velocity tag) for a clip with the given loop; end = unlooped clip end."""
    out = []
    bases = [L(B - S)]
    if looped:
        W = L(B + (Le - S))
        for _ in range(passes - 1):
            bases.append(L(W - Ls))
            W = L(W + (Le - Ls))
    for k, base in enumerate(bases):
        lo = S if k == 0 else Ls
        hi = Le if looped else end
        pass_end = L(base + hi)
        for i, (t, d) in enumerate(notes):
            if t < lo or t >= hi:
                continue            # before the pass start (not chased) or at/after its end
            on = L(base + t)
            off = L(base + (L(t + d) if d > 0 else L(t + H)))
            out.append((on, 'on', i, 'velocity'))
            if off <= pass_end:          # an off exactly at the pass end fires before the wrap (priority 1 < 7)
                out.append((off, 'off', i, 'off velocity'))
            else:
                out.append((pass_end, 'off', i, '64 (cut at loop end or clip end)'))
    return sorted(out, key=lambda e: (e[0], e[1] == 'on'))


def table(evs, rates):
    return [{'beat': b, 'kind': k, 'note': i, 'velocity': v,
             **{f'{sr}Hz@{t}': smp(b, sr, t) for sr, t in rates}} for b, k, i, v in evs]


RATES = [(48000, 120.0), (48000, 90.0), (44100, 110.0)]
CASES = {
    'MC-01 Slide, launch B=4, two passes': events(SLIDE, 4.0, 0.0, 0.0, 4.0, True, 2),
    'MC-02 Slide, start 0.125 (inside note 0), B=4': events(SLIDE, 4.0, 0.125, 0.0, 4.0, True, 2),
    'MC-03 Slide, last note 1 beat long (crosses loop end), B=4': events(SLIDE[:7] + [(3.5, 1.0)], 4.0, 0.0, 0.0, 4.0, True, 2),
    'MC-04 Slide, note 1 zero length, B=4': events([SLIDE[0], (0.5, 0.0)] + SLIDE[2:], 4.0, 0.0, 0.0, 4.0, True, 1),
    'MC-05 Slide, loop off, end 4, B=4': events(SLIDE, 4.0, 0.0, 0.0, 4.0, False, 1, end=4.0),
    'MC-06 Slide, loop off, last note 1 beat long, B=4': events(SLIDE[:7] + [(3.5, 1.0)], 4.0, 0.0, 0.0, 4.0, False, 1, end=4.0),
}
print(json.dumps({'spb': {f'{sr}Hz@{t}': spb(sr, t) for sr, t in RATES},
                  'cases': {k: table(v, RATES) for k, v in CASES.items()}}, indent=1))
