"""Expectation model for the playback-core-v1 candidate (analyst side; never shipped).

Restates the SPEC-PLAYBACK-CORE r1 rules that the candidate releases, so that build_playback.py can compute
each case's expected events and samples for its own generated fixtures:
  clock and placement   REQ-001/002 (X-confirmed: transport/results/fire.json, sweep.json, plus_one_check.json)
  Play, Stop, Continue  REQ-004/005 (X: stop_resume.json)       song loop  REQ-006 (X: loop.json)
  launch grid, boundary REQ-007/008/010 with the REQ-CLIP-LAUNCH-015/017 arithmetic (X: x2 launch.json)
  MIDI clip passes and note events  REQ-011 to 014 (X: midi/results/*.json; the pass rule as midi/cases.py)
  unwarped audio read positions, linear kernel, gain  REQ-017 to 020 (X: audio/results/*.json, model of run_x.py)
Dependencies: stdlib and numpy (binary32 arithmetic). Pure functions; no file access.
"""
import math
import struct
from fractions import Fraction as Fr

import numpy as np

N = 3843840
H = 1.0 / N
# Absolute engine sample counters tried for render sample 0 (the counter is not set by the set or the script).
COUNTERS = (0, 1 << 10, 1 << 20, 1 << 25, (1 << 31) + 12345, (1 << 32) + 777)


def f32(x):
    return struct.unpack('<f', struct.pack('<f', x))[0]


def L(x):
    """Lattice rounding, binary64 formula (REQ-CLIP-LAUNCH-013 / REQ-MIDI-NOTE-STORAGE-006)."""
    s = 1.0 if x >= 0 else -1.0
    return s * (math.floor(abs(x + s * H * 0.5) * N) / N)


def lat(x):
    """The exact rational multiple of 1/N that a lattice value stands for."""
    m = Fr(x) * N
    assert abs(m - round(m)) < Fr(1, 1000), x
    return Fr(round(m), N)


class Clock:
    """Song clock of one render: anchors (render sample, beat), Stop/Continue and song-loop jumps."""

    def __init__(self, sr, tempo, start_beat=0.0, stop=None, cont=None, loop=None, horizon=10 ** 8):
        self.sr, self.T = sr, f32(tempo)
        self.spb = (sr / self.T) * 60.0
        self.bps = 1.0 / self.spb
        self.loop = None
        b0 = max(0.0, L(start_beat))
        self.segs = []  # dicts: n (anchor sample), b (anchor beat), until (exclusive sample or None), end (jump beat)
        if stop is not None:
            held = b0 + (stop - 0) * self.bps
            self.segs.append({'n': 0, 'b': b0, 'until': stop, 'end': None})
            self.segs.append({'n': cont, 'b': held, 'until': None, 'end': None})
            self.held = held
            return
        if loop is None:
            self.segs.append({'n': 0, 'b': b0, 'until': None, 'end': None})
            return
        start, length = max(0.0, loop[0]), max(1.0, loop[1])
        end = L(start + length)
        self.loop = (start, end)
        n, b = 0, b0
        while True:
            if b >= end:  # Play at or after the loop end never loops
                self.segs.append({'n': n, 'b': b, 'until': None, 'end': None})
                return
            j = self.place(end, n, b)
            assert len(j) == 1, ('jump sample must be unambiguous', j)
            j = j[0]
            self.segs.append({'n': n, 'b': b, 'until': j, 'end': end})
            if j > horizon:
                self.segs.append({'n': j, 'b': start, 'until': None, 'end': None})
                return
            n, b = j, start

    def jumps(self):
        return [s['until'] for s in self.segs if s['end'] is not None]

    def place(self, b, n_a, b_a):
        """Render samples allowed for an event at lattice beat b, relative to anchor (n_a, b_a): REQ-002."""
        exact = (lat(b) - Fr(b_a)) * self.sr * 60 / Fr(self.T)
        P = n_a + math.ceil(exact)
        q = (b - b_a) * self.spb
        allowed = [P] if (exact.denominator != 1 or q <= exact) else [P, P + 1]
        xs = {math.ceil((b - b_a) * self.spb + float(n_a + c)) - c for c in COUNTERS}
        assert xs <= set(allowed), (b, n_a, b_a, xs, allowed)
        return allowed

    def seg_at(self, r):
        for i, s in enumerate(self.segs):
            if s['n'] <= r and (s['until'] is None or r < s['until']):
                return i
        raise AssertionError(('transport stopped at request sample', r))

    def beat_at(self, r):
        s = self.segs[self.seg_at(r)]
        return s['b'] + (r - s['n']) * self.bps

    def place_clip_beat(self, b, i):
        """An event of a clip launched in segment i, at beat b of that segment's timeline. A song-loop jump shifts
        the clip by the jump (REQ-006: the clip is not moved); cross-check against placing it unshifted."""
        unshifted = self.place(b, self.segs[i]['n'], self.segs[i]['b'])
        shifted_b = b
        while self.segs[i]['end'] is not None and lat(shifted_b) >= lat(self.segs[i]['end']):
            assert lat(shifted_b) != lat(self.segs[i]['end']), ('event on a jump beat', b)
            shifted_b = L(shifted_b - (self.segs[i]['end'] - self.loop[0]))
            i += 1
        s = self.segs[i]
        out = self.place(shifted_b, s['n'], s['b'])
        assert out == unshifted, ('shifted and unshifted placements differ', b, out, unshifted)
        return out


def bar(n, d):
    return L(4.0 * n / d)


def grid(global_q, song_sig, clip_q, clip_sig):
    """Grid length in beats of a launch-button press (REQ-007, REQ-CLIP-LAUNCH-015/016); 0 means no grid."""
    if clip_q == 1:
        return 0.0
    q, sig = (global_q, song_sig) if clip_q == 0 else (clip_q - 1, clip_sig)
    b = bar(*sig)
    table = {1: 8 * b, 2: 4 * b, 3: 2 * b, 4: b, 5: 2.0, 6: 4 / 3, 7: 1.0, 8: 2 / 3, 9: 0.5, 10: 1 / 3, 11: 0.25,
             12: 1 / 6, 13: 0.125}
    return table.get(q, 0.0)


def boundary(t, g):
    """Launch boundary B for lattice press beat t and grid g (REQ-CLIP-LAUNCH-017 arithmetic, anchor 0)."""
    return L(math.ceil(t / g) * g) if g > 0 else L(t)


def note_events(notes, B, loop_start, loop_end, start_rel, looped, until_beat):
    """Clip-frame note events of a warped session MIDI clip whose start plays at song beat B (REQ-011 to 014).
    notes: dicts with t, d (lattice values), vel, off, on (enabled), key. Returns (beat, prio, kind, key, vel)."""
    S, Ls, Le = L(loop_start + start_rel), loop_start, loop_end
    out, k = [], 0
    base, lo, W = L(B - S), S, L(B + (Le - S))
    while True:
        hi_beat = L(base + Le)
        for n in notes:
            if not n['on'] or n['t'] < lo or n['t'] >= Le:
                continue  # disabled; under way at the pass start (not chased); at or after the loop end
            on = L(base + n['t'])
            if on >= until_beat:
                continue
            assert on == L(B - S + n['t']) or k > 0
            off_t = L(n['t'] + n['d']) if n['d'] > 0 else L(n['t'] + H)
            out.append((on, 14, 'note-on', n['key'], n['vel']))
            if off_t <= Le:  # an off exactly at the loop end is sent with its own velocity before the wrap
                out.append((L(base + off_t), 1, 'note-off', n['key'], n['off']))
            else:  # cut at the wrap (state at Ls = 0 is the clip start) or at the unlooped clip's end
                assert Ls == 0.0
                out.append((hi_beat, 1, 'note-off', n['key'], 64.0))
        if not looped or W >= until_beat:
            break
        base, lo, W, k = L(W - Ls), Ls, L(W + (Le - Ls)), k + 1
    return sorted(out, key=lambda e: (lat(e[0]), e[1]))


# ---- unwarped audio (REQ-017 to 020) ----
def read_step_fixed(file_rate, sr, coarse=0.0, fine=0.0):
    """32.32 fixed-point read step. For transposition 0 the power is exactly 1 in any C library; otherwise the
    binary32 power of the X runs is used (glibc powf; numpy's float32 power gives the same value for +12)."""
    t = np.float32(np.float32(coarse) + np.float32(0.01) * np.float32(fine))
    t = min(max(float(t), -48.0), 48.0)
    p = 1.0 if t == 0 else float(np.power(np.float32(2 ** (1 / 12)), np.float32(t), dtype=np.float32))
    inc = p * (file_rate / sr)
    return int(math.floor(abs(inc) * 2 ** 32 + 0.5))


def first_frame(file_rate, loop_start):
    return int(math.trunc(file_rate * loop_start))


def render_clip(frames, f0, inc, count, gain=1.0):
    """Output values (binary32) of k = 0 .. count-1, and the last k whose read uses only frames inside the file.
    Direct copy for a step of exactly 1, else linear interpolation in binary32 (X-confirmed kernel model)."""
    x = np.asarray(frames, dtype=np.float32) / np.float32(32768)
    g = np.float32(gain)
    out, graded = [], 0
    pos = f0 << 32
    for _ in range(count):
        i, fr = pos >> 32, pos & 0xffffffff
        if inc == 1 << 32:
            if i >= len(x):
                break
            v = x[i]
        else:
            if i + 1 >= len(x):
                break
            f = np.float32(float(fr) * 2.3283064365386963e-10)
            v = np.float32(np.float32(np.float32(1) - f) * x[i]) + np.float32(f * x[i + 1])
        out.append(float(np.float32(np.float32(v) * g)))
        graded += 1
        pos += inc
    return out
