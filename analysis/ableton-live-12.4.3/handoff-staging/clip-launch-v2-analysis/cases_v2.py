"""Case definitions for the clip-launch-v2 candidate (analyst side; never shipped).

CARRIED: the 50 clip-launch-v1 cases. Records are copied verbatim from handoff/clip-launch-v1/cases.json;
only the fixture is rebuilt, from fixtures_v2.base(version) with the edit listed here (the v1 edit,
restated on the minimal set). NEW_DOC: document cases for REQ-012/013 settled by extracted execution
(SPEC-CLIP-LAUNCH r3/r4). NEW_VAL: value cases for REQ-015 to 018 (grid and boundary arithmetic, released
as a value contract only). Expected values are hand-written literals; seal checks each against the X2
results named in its xref and against the cross-check model.
xref forms (joined by |): grid:n/d/q  getter:k  boundary:<X2 label>  sweep:q/k/step  chance:<X2 label>  ft:<input repr>
"""
from fixtures_v2 import AR, SA, SC, SN, V12117, V12402, V405

R = "REQ-CLIP-LAUNCH-"
PROV_S = "static-derived; not observed reference output"
PROV_X = "extracted execution (x86_64 slice); arm64 equivalence inferred"
B_X = "extracted execution"
B_SEL = "selection static-derived; grid length extracted execution"
B_SEL_X = "selection static-derived; reading of -99 and grid length extracted execution"
B_NOGRID = "rounded beat extracted execution; boundary with no grid static-derived"
GQ, AQ = "GlobalQuantisation", "AutoQuantisation"
FA = SC + "/FollowAction"
FA_INIT = {"FollowTime": 4.0, "IsLinked": True, "LoopIterations": 1, "FollowActionA": 4, "FollowActionB": 0,
           "FollowChanceA": 100.0, "FollowChanceB": 0.0, "JumpIndexA": 1.0, "JumpIndexB": 1.0,
           "FollowActionEnabled": False}


def fav(prefix, vals):
    return {f"{prefix}/FollowAction/{k}": v for k, v in vals.items()}


def clip(**kv):
    return [("set", SC, kv)]


def fa(**kv):
    return [("set", FA, kv)]


def chances(a, b, **more):
    return fa(FollowChanceA=a, FollowChanceB=b, **more)


# ---- carried v1 cases: version and edit on the base ----
CARRIED = {
    1: (V12402, []), 2: (V12402, clip(LaunchMode="2", LaunchQuantisation="5")),
    3: (V12402, clip(LaunchMode="3", LaunchQuantisation="14")),
    4: (V12402, [("set", SA, {"LaunchMode": "1", "LaunchQuantisation": "1"})]),
    5: (V12402, [("arr", None, {"LaunchQuantisation": "1"})]),
    6: (V12402, [("set", "", {GQ: "7"})]), 7: (V12402, [("set", "", {GQ: "0"})]),
    8: (V12402, [("set", "", {GQ: "13"})]), 9: (V12402, [("set", "", {AQ: "5"})]),
    10: (V12402, [("set", "", {AQ: "8"})]), 11: (V12402, fa(FollowActionA="9", FollowActionB="2")),
    12: (V12402, clip(Legato="true", VelocityAmount="0.5")), 13: (V12402, clip(Legato="1")),
    14: (V12402, clip(VelocityAmount="0.3")), 15: (V12402, clip(LaunchMode="+2", LaunchQuantisation=" 5")),
    16: (V12402, fa(FollowTime="4.5abc")), 17: (V12402, clip(Legato="TRUE")),
    18: (V12402, clip(LaunchMode="2.0")), 19: (V12402, [("dup", SC, ("LaunchMode", "2"))]),
    20: (V12402, clip(VelocityAmount="abc")), 21: (V12402, [("set", "", {GQ: "4.0"})]),
    22: (V12402, fa(FollowActionEnabled="yes")),
    23: (V12402, [("drop", SC, ["Legato", "VelocityAmount", "FollowAction"])]),
    24: (V12402, fa(JumpIndexB="3") + [("drop", FA, ["JumpIndexA"])]),
    25: (V12402, fa(FollowTime="8") + [("drop", FA, ["IsLinked", "LoopIterations", "FollowActionEnabled"])]),
    26: (V12402, clip(LaunchQuantisation="15")), 27: (V12402, clip(LaunchMode="4")),
    28: (V12402, fa(FollowActionA="10")), 29: (V12402, chances("30", "30")),
    30: (V12402, fa(FollowChanceA="0", FollowActionEnabled="true")), 31: (V12402, chances("1", "7")),
    32: (V12402, chances("1", "2")), 33: (V12402, chances("0", "50")), 34: (V12402, chances("0.25", "0.75")),
    35: (V12402, fa(FollowActionEnabled="true")),
    36: (V12402, fa(FollowChanceA="30") + [("drop", FA, ["FollowChanceB"])]),
    37: (V12402, fa(FollowTime="2.0000001")), 38: (V12402, fa(FollowTime="3.0000002")),
    39: (V12402, fa(FollowTime="1e-8")), 40: (V12402, fa(FollowTime="1.3333333")),
    41: (V405, []),
    42: (V405, clip(FollowTime="8", FollowActionA="3", FollowActionB="1", FollowChanceA="0.5", FollowChanceB="0.5")),
    43: (V405, clip(FollowActionA="2", FollowActionB="4", FollowChanceA="0.25", FollowChanceB="0.75")),
    44: (V405, clip(FollowTime="8")), 45: (V405, [("drop", SC, ["FollowTime"])]),
    46: (V12117, [("set", SN + "/FollowAction", {"IsLinked": "false"})]),
    47: (V12117, [("set", SN + "/FollowAction", {"FollowTime": "8"})]),
    48: (V12117, [("remove", SN + "/FollowAction", None)]),
    49: (V12117, [("set", SN + "/FollowAction", {"FollowActionEnabled": "true"})]),
    50: (V12402, [("set", SN + "/FollowAction", {"IsLinked": "false"})]),
}


def ch_case(a, b, va, vb, enabled=None):
    v = {"FollowChanceA": va, "FollowChanceB": vb}
    if enabled is not None:
        v["FollowActionEnabled"] = enabled
    return {"outcome": "opens", "values": fav(SC, v), "saved": {"values": fav(SC, v)}}


def ft_case(x):
    return {"outcome": "opens", "values": fav(SC, {"FollowTime": x})}


# ---- new document cases: n, kind, reqs, purpose, version, edits, action, expected, xref ----
NEW_DOC = [
    (51, "boundary", ["012"], "Chances 3 and 5 become 38 and 62 (37.5 rounds away from zero)", V12402,
     chances("3", "5"), "open-save", ch_case(3, 5, 38.0, 62.0), "chance:3/5 (37.5)"),
    (52, "boundary", ["012"], "Chances 5 and 3 become 63 and 37 (62.5 rounds away from zero)", V12402,
     chances("5", "3"), "open-save", ch_case(5, 3, 63.0, 37.0), "chance:5/3 (62.5)"),
    (53, "boundary", ["012"], "Chances 1 and 199 become 1 and 99 (0.5 rounds away from zero)", V12402,
     chances("1", "199"), "open-save", ch_case(1, 199, 1.0, 99.0), "chance:1/199 (0.5)"),
    (54, "boundary", ["012"], "Chances 99.5 and 0.5 become 100 and 0", V12402, chances("99.5", "0.5"),
     "open-save", ch_case(99.5, 0.5, 100.0, 0.0), "chance:99.5/0.5"),
    (55, "boundary", ["012"], "Chance A negative zero and chance B 0 count as both zero: 100 and 0, disabled",
     V12402, chances("-0", "0", FollowActionEnabled="true"), "open-save",
     ch_case(-0.0, 0, 100.0, 0.0, enabled=False), "chance:-0/0"),
    (56, "boundary", ["011", "012"], "Chances 150 and 50, outside 0 to 100, become 75 and 25", V12402,
     chances("150", "50"), "open-save", ch_case(150, 50, 75.0, 25.0), "chance:CLC-023 150/50"),
    (57, "boundary", ["011", "012"], "Chances -10 and 50 become 0 and 100 (rescaled -25 and 125, then limited)",
     V12402, chances("-10", "50"), "open-save", ch_case(-10, 50, 0.0, 100.0), "chance:-10/50"),
    (58, "boundary", ["011", "012"], "Chances 150 and -50 become 100 and 0 (limited)", V12402,
     chances("150", "-50"), "open-save", ch_case(150, -50, 100.0, 0.0), "chance:150/-50"),
    (59, "boundary", ["011", "012"], "Chances -10 and -10 become 50 and 50", V12402, chances("-10", "-10"),
     "open-save", ch_case(-10, -10, 50.0, 50.0), "chance:-10/-10"),
    (60, "boundary", ["013"], "Follow time one step below the nearest value to half a lattice step is held as "
     "one lattice step, not 0", V12402, fa(FollowTime="1.3007825507825505e-07"), "open",
     ft_case(2.6015651015651016e-07), "ft:1.3007825507825505e-07"),
    (61, "boundary", ["013"], "Follow time just below 1.5 lattice steps is held as two steps", V12402,
     fa(FollowTime="3.902347652347652e-07"), "open", ft_case(5.203130203130203e-07), "ft:3.902347652347652e-07"),
    (62, "boundary", ["013"], "Follow time next to a halfway point above 100,000 rounds up by the formula", V12402,
     fa(FollowTime="100000.00000143086"), "open", ft_case(100000.00000156094), "ft:100000.00000143086"),
]


# ---- value cases ----
def gl(q, n, d, g, xref=True):
    return {"function": "grid-length", "arguments": {"q": q, "time_signature": [n, d]}, "result": {"grid": g},
            "basis": B_X, "xref": f"grid:{n}/{d}/{q}" if xref else None}


def cg(k, gq, clip_sig, song_sig, g, xq=None):
    """clip-grid; xq: (n, d, q) of the grid-length run that backs the result."""
    k0 = 0 if k == -99 else k
    if xq is None:
        xq = (*song_sig, gq) if k0 == 0 else (*clip_sig, k0 - 1)
    return {"function": "clip-grid", "arguments": {"clip_value": k, "global_value": gq,
            "clip_time_signature": list(clip_sig), "song_time_signature": list(song_sig)}, "result": {"grid": g},
            "basis": B_SEL_X if k < 0 or k == -99 else B_SEL,
            "xref": "grid:%d/%d/%d" % xq + (f"|getter:{k}" if k < 0 or k >= 14 else "")}


def bd(t, g, p, b, xref, a=0.0):
    basis = B_NOGRID if g == 0 else B_X
    return {"function": "grid-boundary", "arguments": {"beat": t, "grid": g, "anchor": a},
            "result": {"rounded_beat": p, "boundary": b}, "basis": basis, "xref": xref}


S44, S34, S68, S78, S54 = (4, 4), (3, 4), (6, 8), (7, 8), (5, 4)


def launch(gq, t, g, p, b, xref, k=0, clip_sig=S44, song_sig=S44):
    return [cg(k, gq, clip_sig, song_sig, g), bd(t, g, p, b, xref)]


NEW_VAL = [
    (63, ["015"], "Grid lengths of the 13 settings in 4/4",
     [gl(q, 4, 4, g) for q, g in zip(range(1, 14), (32.0, 16.0, 8.0, 4.0, 2.0, 4 / 3, 1.0, 2 / 3, 0.5, 1 / 3, 0.25,
                                                         1 / 6, 0.125))]),
    (64, ["015"], "Bar settings follow the time signature: 3/4, 6/8, 7/8 and 5/4",
     [gl(q, n, d, g) for (n, d), gs in ((S34, (24.0, 12.0, 6.0, 3.0)), (S68, (24.0, 12.0, 6.0, 3.0)),
                                         (S78, (28.0, 14.0, 7.0, 3.5)), (S54, (40.0, 20.0, 10.0, 5.0)))
      for q, g in zip(range(1, 5), gs)]),
    (65, ["015"], "Note settings do not depend on the time signature",
     [gl(5, 6, 8, 2.0), gl(6, 7, 8, 4 / 3), gl(7, 5, 4, 1.0), gl(8, 3, 4, 2 / 3), gl(9, 5, 4, 0.5),
      gl(10, 6, 8, 1 / 3), gl(11, 7, 8, 0.25), gl(12, 3, 4, 1 / 6), gl(13, 5, 4, 0.125)]),
    (66, ["015"], "Bar settings at the extreme time signatures 1/1, 1/16, 99/1 and 99/16",
     [gl(1, 1, 1, 32.0), gl(4, 1, 1, 4.0), gl(4, 1, 16, 0.25), gl(1, 1, 16, 2.0), gl(4, 99, 1, 396.0),
      gl(1, 99, 16, 198.0), gl(3, 13, 16, 6.5), gl(2, 17, 8, 34.0)]),
    (67, ["015"], "Values other than 1 to 13 denote no grid (0)",
     [gl(q, 4, 4, 0.0) for q in (0, -1, -2, -99, 14, 15, 100)] + [gl(0, 7, 8, 0.0), gl(14, 3, 4, 0.0)]),
    (68, ["011", "016"], "Grid a clip's setting denotes: own time signature, -99 as Global, values without a grid",
     [cg(2, 4, S78, S44, 28.0), cg(14, 4, S44, S44, 0.125), cg(-99, 7, S68, S34, 1.0),
      cg(0, 13, S68, S34, 0.125), cg(-98, 4, S44, S44, 0.0), cg(15, 4, S44, S44, 0.0)]),
    (69, ["015", "016", "017"], "Global 1 Bar in 4/4: beat 5.3 gives the boundary 8",
     launch(4, 5.3, 4.0, 5.3, 8.0, "boundary:CLC-031")),
    (70, ["015", "016", "017"], "Global 2 Bars: beat 9 gives 16", launch(3, 9.0, 8.0, 9.0, 16.0, "boundary:CLC-032")),
    (71, ["015", "016", "017"], "Global 4 Bars: beat 17 gives 32",
     launch(2, 17.0, 16.0, 17.0, 32.0, "boundary:CLC-033")),
    (72, ["015", "016", "017"], "Global 8 Bars: beat 1 gives 32", launch(1, 1.0, 32.0, 1.0, 32.0, "boundary:CLC-034")),
    (73, ["015", "016", "017"], "Song in 3/4, Global 1 Bar: beat 4 gives 6",
     launch(4, 4.0, 3.0, 4.0, 6.0, "boundary:CLC-035", song_sig=S34)),
    (74, ["015", "016", "017"], "Song in 3/4, Global 8 Bars: beat 1 gives 24",
     launch(1, 1.0, 24.0, 1.0, 24.0, "boundary:CLC-036", song_sig=S34)),
    (75, ["015", "016", "017"], "Song in 6/8, Global 1 Bar: beat 1 gives 3",
     launch(4, 1.0, 3.0, 1.0, 3.0, "boundary:CLC-037", song_sig=S68)),
    (76, ["015", "016", "017"], "Song in 7/8, Global 1 Bar: beat 4 gives 7",
     launch(4, 4.0, 3.5, 4.0, 7.0, "boundary:CLC-038", song_sig=S78)),
    (77, ["015", "016", "017"], "Song in 5/4, Global 2 Bars: beat 1 gives 10",
     launch(3, 1.0, 10.0, 1.0, 10.0, "boundary:CLC-039", song_sig=S54)),
    (78, ["015", "016", "017"], "Global 1/2: beat 2.25 gives 4", launch(5, 2.25, 2.0, 2.25, 4.0, "boundary:CLC-040")),
    (79, ["015", "016", "017"], "Global 1/2T: beat 1.5 gives 8/3",
     launch(6, 1.5, 4 / 3, 1.5, 8 / 3, "boundary:CLC-041")),
    (80, ["015", "016", "017"], "Global 1/4: beat 2.1 gives 3", launch(7, 2.1, 1.0, 2.1, 3.0, "boundary:CLC-042")),
    (81, ["015", "016", "017"], "Global 1/4T: beat 1 gives 4/3",
     launch(8, 1.0, 2 / 3, 1.0, 4 / 3, "boundary:CLC-043")),
    (82, ["015", "016", "017"], "Global 1/8: beat 3.1 gives 3.5", launch(9, 3.1, 0.5, 3.1, 3.5, "boundary:CLC-044")),
    (83, ["015", "016", "017"], "Global 1/8T: beat 0.4 gives 2/3",
     launch(10, 0.4, 1 / 3, 0.4, 2 / 3, "boundary:CLC-045")),
    (84, ["015", "016", "017"], "Global 1/16: beat 1.3 gives 1.5",
     launch(11, 1.3, 0.25, 1.3, 1.5, "boundary:CLC-046")),
    (85, ["015", "016", "017"], "Global 1/16T: beat 0.2 gives 1/3",
     launch(12, 0.2, 1 / 6, 0.2, 1 / 3, "boundary:CLC-047")),
    (86, ["015", "016", "017"], "Global 1/32: beat 0.13 is first rounded to the lattice, then gives 1/4",
     launch(13, 0.13, 0.125, 0.12999994796869796, 0.25, "boundary:CLC-048")),
    (87, ["015", "016", "017"], "Clip set to 1/4 while Global is 1 Bar: beat 2.1 gives 3, not 4",
     launch(4, 2.1, 1.0, 2.1, 3.0, "boundary:CLC-049", k=8)),
    (88, ["015", "016", "017"], "Clip in 6/8 set to 1 Bar in a 4/4 song: beats 1.2 and 4.2 give 3 and 6",
     launch(4, 1.2, 3.0, 1.2, 3.0, "boundary:CLC-050a", k=5, clip_sig=S68)
     + [bd(4.2, 3.0, 4.2, 6.0, "boundary:CLC-050b")]),
    (89, ["015", "016", "017"], "Clip in 6/8 set to Global denotes the global value in the song's 4/4: beat 1.2 gives 4",
     launch(4, 1.2, 4.0, 1.2, 4.0, "boundary:CLC-051", k=0, clip_sig=S68)),
    (90, ["016", "018"], "Clip set to None: no grid, the boundary is the rounded beat 5.3",
     launch(4, 5.3, 0.0, 5.3, 5.3, "boundary:CLC-031", k=1)),
    (91, ["016", "018"], "Global None with a clip set to Global: no grid, boundary 5.3",
     launch(0, 5.3, 0.0, 5.3, 5.3, "boundary:CLC-031")),
    (92, ["015", "016", "017"], "Beats 3.99 and 4 with 1 Bar in 4/4 both give 4",
     launch(4, 3.99, 4.0, 3.990000104062604, 4.0, "boundary:PRB-S5-01 4/4 1 Bar t=3.99")
     + [bd(4.0, 4.0, 4.0, 4.0, "boundary:PRB-S5-01 4/4 1 Bar t=4.0")]),
    (93, ["011", "015", "016", "017"], "Clip value -99 counts as Global: beat 5.3 gives 8",
     launch(4, 5.3, 4.0, 5.3, 8.0, "boundary:CLC-031", k=-99)),
    (94, ["016", "018"], "Clip value -1: no grid, boundary 5.3", launch(4, 5.3, 0.0, 5.3, 5.3, "boundary:CLC-031", k=-1)),
    (95, ["015", "016", "017"], "Global 1/4T: the beat nearest 10/3, on a grid line, gives 4, not 10/3",
     launch(8, 10 / 3, 2 / 3, 10 / 3, 4.0, "sweep:8/5/0")),
    (96, ["017"], "Beat rounding next to the grid line at beat 4 (1 Bar in 4/4)",
     [bd(t, 4.0, p, b, f"boundary:PRB-S5-01 4/4 1 Bar t={t!r}") for t, p, b in (
         (1.5, 1.5, 4.0), (3.9, 3.9, 4.0), (3.99999973984349, 3.99999973984349, 4.0),
         (3.9999998699217447, 4.0, 4.0), (4.000000130078255, 4.0, 4.0), (4.00000012747669, 4.0, 4.0),
         (4.000000260156511, 4.000000260156511, 8.0), (3.999999999, 4.0, 4.0), (4.000000001, 4.0, 4.0))]),
    (97, ["017"], "Beats exactly on triplet grid lines: some give the next line",
     [bd(20 / 3, 4 / 3, 20 / 3, 8.0, "sweep:6/5/0"), bd(5 / 3, 1 / 3, 5 / 3, 2.0, "sweep:10/5/0"),
      bd(371 / 6, 1 / 6, 371 / 6, 62.0, "sweep:12/371/0"), bd(2 / 3, 2 / 3, 2 / 3, 2 / 3, "sweep:8/1/0"),
      bd(4 / 3, 2 / 3, 4 / 3, 4 / 3, "sweep:8/2/0"), bd(8 / 3, 2 / 3, 8 / 3, 8 / 3, "sweep:8/4/0"),
      bd(4 / 3, 4 / 3, 4 / 3, 4 / 3, "sweep:6/1/0"), bd(1 / 6, 1 / 6, 1 / 6, 1 / 6, "sweep:12/1/0")]),
    (98, ["017"], "One lattice step before or after a triplet line gives the first line at or after the beat",
     [bd(3.3333330731768234, 2 / 3, 3.3333330731768234, 10 / 3, "sweep:8/5/-1"),
      bd(3.3333335934898436, 2 / 3, 3.3333335934898436, 4.0, "sweep:8/5/1"),
      bd(6.666666406510156, 4 / 3, 6.666666406510156, 20 / 3, "sweep:6/5/-1"),
      bd(6.666666926823177, 4 / 3, 6.666666926823177, 8.0, "sweep:6/5/1"),
      bd(61.833333073176824, 1 / 6, 61.833333073176824, 371 / 6, "sweep:12/371/-1"),
      bd(61.83333359348984, 1 / 6, 61.83333359348984, 62.0, "sweep:12/371/1")]),
    (99, ["017"], "The anchor: 8 with grid 3 and beat 9 gives 11; a negative anchor counts as 0",
     [bd(9.0, 3.0, 9.0, 11.0, "boundary:CLC-055 anchor 8, 3/4 1 Bar, t=9", a=8.0),
      bd(5.3, 4.0, 5.3, 8.0, "boundary:anchor -5 (clamped to 0), 1 Bar, t=5.3", a=-5.0),
      bd(9.0, 3.0, 9.0, 11.0, "boundary:anchor 8.0000001 (off lattice), 3/4 1 Bar, t=9", a=8.0000001)]),
    (100, ["018"], "With no grid the boundary is the beat rounded to the lattice",
     [bd(3.99, 0.0, 3.990000104062604, 3.990000104062604, "boundary:PRB-S5-01 4/4 1 Bar t=3.99"),
      bd(0.13, 0.0, 0.12999994796869796, 0.12999994796869796, "boundary:CLC-048"),
      bd(4.000000001, 0.0, 4.0, 4.0, "boundary:PRB-S5-01 4/4 1 Bar t=4.000000001")]),
]

# spec cases each new case restates (traceability only)
SPEC_CASE = {51: "CLC-057", 52: "REQ-012 example 5/3", 53: "REQ-012 example 1/199", 54: "REQ-012 example 99.5/0.5",
             55: "REQ-012 (-0 counts as 0)", 56: "CLC-023", 57: "CLC-058", 58: "CLC-059",
             59: "REQ-011 example -10/-10", 60: "CLC-060", 61: "REQ-013 near-tie (X2 k=1)",
             62: "REQ-013 near-tie (X2 k=N*100000+5)", 63: "REQ-015 table", 64: "REQ-015 table",
             65: "REQ-015 note values", 66: "REQ-015 (495 signatures)", 67: "REQ-015 no grid",
             68: "REQ-016 clauses, REQ-011 -99", 69: "CLC-031", 70: "CLC-032", 71: "CLC-033", 72: "CLC-034",
             73: "CLC-035", 74: "CLC-036", 75: "CLC-037", 76: "CLC-038", 77: "CLC-039", 78: "CLC-040",
             79: "CLC-041", 80: "CLC-042", 81: "CLC-043", 82: "CLC-044", 83: "CLC-045", 84: "CLC-046",
             85: "CLC-047", 86: "CLC-048", 87: "CLC-049", 88: "CLC-050", 89: "CLC-051", 90: "CLC-052",
             91: "CLC-053", 92: "CLC-054 (beats only)", 93: "CLC-062", 94: "CLC-063", 95: "CLC-064 (beats only)",
             96: "REQ-017 press rounding (PRB-S5-01 presses)", 97: "REQ-017 triplet correction",
             98: "REQ-017 one-step presses", 99: "REQ-017 anchor arithmetic (CLC-055 arithmetic)",
             100: "REQ-018 no grid"}
