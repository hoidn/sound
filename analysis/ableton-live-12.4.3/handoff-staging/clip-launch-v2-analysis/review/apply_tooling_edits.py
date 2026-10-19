"""Reviewer's edits to the author's generators (run once; fails on any miss), before `build_v2.py build`.

usage: python3 -I -B apply_tooling_edits.py
RVC2-01: value function launch-boundary -> grid-boundary, result press_beat -> rounded_beat, prose
"press beat" -> "rounded beat", case purposes without launch wording. RVC2-02, RVC2-03: manifest scope and
exclusion texts in meta_v2.py. build_v2.py: cases.json status for a reviewed release.
"""
from pathlib import Path

T = Path(__file__).resolve().parents[1]

EDITS = {
    "model_v2.py": [
        ('    if function == "launch-boundary":\n', '    if function == "grid-boundary":\n'),
        ('        return {"press_beat": p, "boundary": b}\n', '        return {"rounded_beat": p, "boundary": b}\n'),
    ],
    "build_v2.py": [
        ('same(v("t_lattice"), res["press_beat"])', 'same(v("t_lattice"), res["rounded_beat"])'),
        ('"status": "candidate-unreviewed",\n        "fixture_origin"', '"status": "released-reviewed",\n        "fixture_origin"'),
    ],
    "cases_v2.py": [
        ('B_NOGRID = "press beat extracted execution; boundary with no grid static-derived"',
         'B_NOGRID = "rounded beat extracted execution; boundary with no grid static-derived"'),
        ('    return {"function": "launch-boundary", "arguments": {"beat": t, "grid": g, "anchor": a},\n'
         '            "result": {"press_beat": p, "boundary": b}, "basis": basis, "xref": xref}',
         '    return {"function": "grid-boundary", "arguments": {"beat": t, "grid": g, "anchor": a},\n'
         '            "result": {"rounded_beat": p, "boundary": b}, "basis": basis, "xref": xref}'),
        ('"Clip in 6/8 set to Global uses the song\'s 4/4: beat 1.2 gives 4"',
         '"Clip in 6/8 set to Global denotes the global value in the song\'s 4/4: beat 1.2 gives 4"'),
        ('"Clip set to None: no grid, the boundary is the press beat 5.3"',
         '"Clip set to None: no grid, the boundary is the rounded beat 5.3"'),
        ('"Press beat rounding next to the bar line at beat 4 (1 Bar in 4/4)"',
         '"Beat rounding next to the grid line at beat 4 (1 Bar in 4/4)"'),
        ('"With no grid the boundary is the press beat, rounded to the lattice"',
         '"With no grid the boundary is the beat rounded to the lattice"'),
    ],
    "meta_v2.py": [
        ('the clip\'s and the song\'s time signatures given as inputs; its use at launch excluded",',
         'the clip\'s and the song\'s time signatures given as inputs; which global value, time signatures and grid '
         'a launch uses, and its use at launch, excluded",'),
        ('"017": "Value contract: press beat (lattice rounding) and boundary arithmetic for a beat, a grid length and an '
         'anchor given as inputs; which beat and anchor a launch uses, the pre-delay, the move to the next line and all '
         'sample timing excluded",',
         '"017": "Value contract: rounded beat (lattice rounding) and boundary arithmetic for a beat, a grid length and '
         'an anchor given as inputs; which beat and anchor a launch uses, whether a launch starts at the boundary, the '
         'pre-delay, the move to the next line and all sample timing excluded",'),
        ('"018": "Value contract: with no grid the boundary is the press beat; launch timing excluded",',
         '"018": "Value contract: with no grid the boundary is the rounded beat; launch timing excluded",'),
        ('"launch timing: when a launched clip starts, the sample at which a launch takes effect, which beat and anchor '
         'a launch uses, the pre-delay and the move to the next grid line, launching with the transport stopped, how a '
         'launch picks its grid at run time; these belong to a separate playback release",',
         '"launch timing: when a launched clip starts, the sample at which a launch takes effect, which beat, anchor, '
         'global value, time signatures and grid a launch uses at run time, whether a launch starts at the boundary of '
         'REQ-CLIP-LAUNCH-017, the pre-delay and the move to the next grid line, launching with the transport stopped; '
         'these belong to a separate playback release; the value functions of REQ-CLIP-LAUNCH-015 to 018 are not launch '
         'timing",'),
        ('"value held, displayed or saved for an out-of-range launch mode, launch quantization or follow-action value; '
         'the held value of a follow time outside 0 to below 1,000,000",',
         '"value held, displayed or saved for an out-of-range launch mode, launch quantization or follow-action value; '
         'for a follow time outside 0 to below 1,000,000, whether the document opens and the value then held",'),
        ('"behavior": "launch grid values as a value contract (extracted execution and static-derived); launching '
         'excluded",',
         '"behavior": "quantization grid values as a value contract of explicit inputs (extracted execution and '
         'static-derived); not launch timing; launching excluded",'),
        ('press beat and boundary including the triplet next-line case, no grid); cases 063-100",',
         'rounded beat and boundary including the triplet next-line case, no grid); not launch timing; cases 063-100",'),
    ],
}

for name, pairs in EDITS.items():
    p = T / name
    s = p.read_text()
    for old, new in pairs:
        assert s.count(old) == 1, (name, old[:80], s.count(old))
        s = s.replace(old, new)
    p.write_text(s)
    print(name, len(pairs), "edits")
