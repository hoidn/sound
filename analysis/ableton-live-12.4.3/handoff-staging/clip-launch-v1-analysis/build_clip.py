"""Stage the clip-launch-v1 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3 and -I from anywhere:
  python3 -I build_clip.py build          # fixtures/, cases.json, draft manifest.json in ../clip-launch-v1/
  python3 -I build_clip.py seal           # manifest files[], author-validation.json, traceability.json
  python3 -I build_clip.py verify <dir>   # same checks against an exported copy (no rewrite)

spec.md, README.md and AGENTS.md are hand-written. Fixtures are authored here from a template
written for this release; no shipped file is read. Expected results are the hand-derived static
expectations in CASES (SPEC-CLIP-LAUNCH r1, narrowed; see wiki/specs/clip-launch-handoff-plan.md).
model() is an independent restatement of the released clauses used only to cross-check them. It
shares the static evidence and is not an oracle.
"""
import copy, hashlib, json, math, re, shutil, struct, sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent / "clip-launch-v1"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"
PROV = "static-derived; not observed reference output"
R = "REQ-CLIP-LAUNCH-"
LATTICE = 3843840.0

# ---- named locations (paths relative to /Ableton/LiveSet) ----
SC = "Tracks/MidiTrack[1]/DeviceChain/MainSequencer/ClipSlotList/ClipSlot[1]/ClipSlot/Value/MidiClip"
SA = "Tracks/AudioTrack[1]/DeviceChain/MainSequencer/ClipSlotList/ClipSlot[1]/ClipSlot/Value/AudioClip"
AR = "Tracks/MidiTrack[1]/DeviceChain/MainSequencer/ClipTimeable/ArrangerAutomation/Events/MidiClip[1]"
SN = "Scenes/Scene[1]"
GQ, AQ = "GlobalQuantisation", "AutoQuantisation"

LAUNCH = ["LaunchMode", "LaunchQuantisation", "Legato", "VelocityAmount", "FollowAction"]
FA_NAMES = ["FollowTime", "IsLinked", "LoopIterations", "FollowActionA", "FollowActionB", "FollowChanceA",
            "FollowChanceB", "JumpIndexA", "JumpIndexB", "FollowActionEnabled"]
OLD = ["FollowTime", "FollowActionA", "FollowActionB", "FollowChanceA", "FollowChanceB"]  # clip children before 406
TYPE = {"Legato": "bool", "IsLinked": "bool", "FollowActionEnabled": "bool",
        "LaunchMode": "int", "LaunchQuantisation": "int", "LoopIterations": "int", "FollowActionA": "int",
        "FollowActionB": "int", GQ: "int", AQ: "int",
        "VelocityAmount": "f32", "FollowChanceA": "f32", "FollowChanceB": "f32", "JumpIndexA": "f32",
        "JumpIndexB": "f32", "FollowTime": "f64"}
FA_INIT = {"FollowTime": 4.0, "IsLinked": True, "LoopIterations": 1, "FollowActionA": 4, "FollowActionB": 0,
           "FollowChanceA": 100.0, "FollowChanceB": 0.0, "JumpIndexA": 1.0, "JumpIndexB": 1.0,
           "FollowActionEnabled": False}
CLIP_INIT = {"Legato": False, "VelocityAmount": 0.0}
RANGE = {"LaunchMode": (0, 3), "LaunchQuantisation": (0, 14), "FollowActionA": (0, 9), "FollowActionB": (0, 9),
         GQ: (0, 13), AQ: (0, 8), "LoopIterations": (1, 1073741823), "VelocityAmount": (0.0, 1.0),
         "FollowChanceA": (0.0, 100.0), "FollowChanceB": (0.0, 100.0), "JumpIndexA": (-1.0, 8388608.0),
         "JumpIndexB": (-1.0, 8388608.0), "FollowTime": (0.0, 999999.999999)}
ENUMS = ("LaunchMode", "LaunchQuantisation", "FollowActionA", "FollowActionB")

# ---- fixture authoring ----
FA_T = [("FollowTime", "4"), ("IsLinked", "true"), ("LoopIterations", "1"), ("FollowActionA", "4"),
        ("FollowActionB", "0"), ("FollowChanceA", "100"), ("FollowChanceB", "0"), ("JumpIndexA", "1"),
        ("JumpIndexB", "1"), ("FollowActionEnabled", "false")]
CLIP_T = [("LaunchMode", "0"), ("LaunchQuantisation", "0"), ("Legato", "false"), ("VelocityAmount", "0")]
OLD_T = [("FollowTime", "4"), ("FollowActionA", "0"), ("FollowActionB", "0"), ("FollowChanceA", "1"),
         ("FollowChanceB", "0")]


def edit(pairs, set_=None, drop=(), dup=None):
    """pairs: [(name, text)]; set_ {name: text}; drop names; dup (name, text) appended after name."""
    out = []
    for n, v in pairs:
        if n in drop:
            continue
        out.append((n, (set_ or {}).get(n, v)))
        if dup and dup[0] == n:
            out.append(dup)
    return out


def leaves(pairs, ind):
    return [f'{" " * ind}<{n} Value="{v}" />' for n, v in pairs]


def fa_xml(pairs, ind):
    return [f'{" " * ind}<FollowAction>', *leaves(pairs, ind + 2), f'{" " * ind}</FollowAction>']


def clip_xml(tag, ind, clip=CLIP_T, fa=FA_T, old=None, dup_launch=None):
    body = leaves(clip, ind + 2)
    if dup_launch:
        i = [n for n, _ in clip].index(dup_launch[0])
        body.insert(i + 1, f'{" " * (ind + 2)}<{dup_launch[0]} Value="{dup_launch[1]}" />')
    if old is not None:
        body += leaves(old, ind + 2)
    if fa is not None:
        body += fa_xml(fa, ind + 2)
    return [f'{" " * ind}<{tag} Id="0" Time="0">', *body, f'{" " * ind}</{tag}>']


def wrap(lines, tags, ind):
    """Nest lines inside the given element start tags (outermost first) at indentation ind."""
    out = list(lines)
    for depth in range(len(tags) - 1, -1, -1):
        name = tags[depth].split()[0]
        out = [f'{" " * (ind + 2 * depth)}<{tags[depth]}>', *out, f'{" " * (ind + 2 * depth)}</{name}>']
    return out


def track(kind="MidiTrack", where="session", **clip_kw):
    tag = "MidiClip" if kind == "MidiTrack" else "AudioClip"
    if where == "session":
        inner = ["DeviceChain", "MainSequencer", "ClipSlotList", 'ClipSlot Id="0"', "ClipSlot", "Value"]
    else:
        inner = ["DeviceChain", "MainSequencer", "ClipTimeable", "ArrangerAutomation", "Events"]
    c = clip_xml(tag, 6 + 2 * (len(inner) + 1), **clip_kw)
    return wrap(c, [f'{kind} Id="1"', *inner], 6)


def scene_xml(fa):
    if fa is None:
        return ['    <Scenes>', '      <Scene Id="0" />', '    </Scenes>']
    return ['    <Scenes>', '      <Scene Id="0">', *fa_xml(fa, 8), '      </Scene>', '    </Scenes>']


def doc(minor="12.0_12402", tracks=None, scenes=None, gq="4", aq="0"):
    tracks = track() if tracks is None else tracks
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             f'<Ableton MajorVersion="5" MinorVersion="{minor}" SchemaChangeCount="1">', '  <LiveSet>',
             '    <Tracks>', *tracks, '    </Tracks>',
             *([] if scenes is None else scene_xml(None if scenes == "bare" else scenes)),
             f'    <GlobalQuantisation Value="{gq}" />', f'    <AutoQuantisation Value="{aq}" />',
             '  </LiveSet>', '</Ableton>']
    return "\n".join(lines) + "\n"


def fav(prefix, vals):
    return {f"{prefix}/FollowAction/{k}": v for k, v in vals.items()}


def fa_all(prefix, **chg):
    v = dict(FA_INIT)
    v.update(chg)
    return fav(prefix, v)


def clip_all(prefix, lm=0, lq=0, **chg):
    v = {f"{prefix}/LaunchMode": lm, f"{prefix}/LaunchQuantisation": lq, f"{prefix}/Legato": False,
         f"{prefix}/VelocityAmount": 0.0}
    v.update(fa_all(prefix, **chg))
    return v


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


FT3 = 11531521 / LATTICE  # nearest binary64 to 11531521/3843840
OLD405 = "11.0_405"
SCN = "12.0_12117"
LINKED_SCENE = edit(FA_T, {"IsLinked": "false"})

# id, kind, requirement suffixes, purpose, fixture text, action, expected
CASES = [
    (1, "save", ["001", "002", "003"], "Template: launch values held, written back unchanged and in order",
     doc(), "open-save",
     {"outcome": "opens", "values": {**clip_all(SC), GQ: 4, AQ: 0},
      "saved": {"values": clip_all(SC), "clip_order": SC}}),
    (2, "positive", ["001", "004", "005"], "Launch mode 2 (Toggle) and launch quantization 5 (1 Bar)",
     doc(tracks=track(clip=edit(CLIP_T, {"LaunchMode": "2", "LaunchQuantisation": "5"}))), "open-save",
     {"outcome": "opens", "values": {SC + "/LaunchMode": 2, SC + "/LaunchQuantisation": 5},
      "saved": {"values": {SC + "/LaunchMode": 2, SC + "/LaunchQuantisation": 5}}}),
    (3, "boundary", ["004", "005"], "Largest values: launch mode 3 (Repeat), launch quantization 14 (1/32)",
     doc(tracks=track(clip=edit(CLIP_T, {"LaunchMode": "3", "LaunchQuantisation": "14"}))), "open",
     {"outcome": "opens", "values": {SC + "/LaunchMode": 3, SC + "/LaunchQuantisation": 14}}),
    (4, "positive", ["001", "004", "005"], "Session audio clip: launch mode 1 (Gate), quantization 1 (None)",
     doc(tracks=track("AudioTrack", clip=edit(CLIP_T, {"LaunchMode": "1", "LaunchQuantisation": "1"}))),
     "open-save",
     {"outcome": "opens", "values": {SA + "/LaunchMode": 1, SA + "/LaunchQuantisation": 1},
      "saved": {"values": {SA + "/LaunchMode": 1, SA + "/LaunchQuantisation": 1}, "clip_order": SA}}),
    (5, "save", ["001", "005"], "Arrangement MIDI clip keeps launch quantization 1 (None) on save",
     doc(tracks=track(where="arrangement", clip=edit(CLIP_T, {"LaunchQuantisation": "1"}))), "open-save",
     {"outcome": "opens", "values": {AR + "/LaunchQuantisation": 1},
      "saved": {"values": {AR + "/LaunchQuantisation": 1}, "clip_order": AR}}),
    (6, "positive", ["003", "005"], "Global quantization 7 (1/4)", doc(gq="7"), "open",
     {"outcome": "opens", "values": {GQ: 7}}),
    (7, "boundary", ["003", "005"], "Global quantization 0 (None)", doc(gq="0"), "open",
     {"outcome": "opens", "values": {GQ: 0}}),
    (8, "boundary", ["003", "005"], "Global quantization 13 (1/32), the largest value", doc(gq="13"), "open",
     {"outcome": "opens", "values": {GQ: 13}}),
    (9, "positive", ["003", "006"], "Record quantization 5 (1/16)", doc(aq="5"), "open",
     {"outcome": "opens", "values": {AQ: 5}}),
    (10, "boundary", ["003", "006"], "Record quantization 8 (1/32), the largest value", doc(aq="8"), "open",
     {"outcome": "opens", "values": {AQ: 8}}),
    (11, "positive", ["002", "007"], "Follow action A 9 (Jump) and B 2 (Play Again)",
     doc(tracks=track(fa=edit(FA_T, {"FollowActionA": "9", "FollowActionB": "2"}))), "open-save",
     {"outcome": "opens", "values": fav(SC, {"FollowActionA": 9, "FollowActionB": 2}),
      "saved": {"values": fav(SC, {"FollowActionA": 9, "FollowActionB": 2})}}),
    (12, "positive", ["001"], "Legato on and velocity amount 0.5",
     doc(tracks=track(clip=edit(CLIP_T, {"Legato": "true", "VelocityAmount": "0.5"}))), "open-save",
     {"outcome": "opens", "values": {SC + "/Legato": True, SC + "/VelocityAmount": 0.5},
      "saved": {"values": {SC + "/Legato": True, SC + "/VelocityAmount": 0.5}}}),
    (13, "positive", ["001"], "Legato text 1 reads as on",
     doc(tracks=track(clip=edit(CLIP_T, {"Legato": "1"}))), "open",
     {"outcome": "opens", "values": {SC + "/Legato": True}}),
    (14, "boundary", ["001"], "Velocity amount 0.3 is held as the nearest binary32 value",
     doc(tracks=track(clip=edit(CLIP_T, {"VelocityAmount": "0.3"}))), "open",
     {"outcome": "opens", "values": {SC + "/VelocityAmount": f32(0.3)}}),
    (15, "boundary", ["001"], "Integer text +2 and leading-space 5 are accepted",
     doc(tracks=track(clip=edit(CLIP_T, {"LaunchMode": "+2", "LaunchQuantisation": " 5"}))), "open",
     {"outcome": "opens", "values": {SC + "/LaunchMode": 2, SC + "/LaunchQuantisation": 5}}),
    (16, "boundary", ["002", "013"], "Follow time text 4.5abc reads as 4.5",
     doc(tracks=track(fa=edit(FA_T, {"FollowTime": "4.5abc"}))), "open",
     {"outcome": "opens", "values": fav(SC, {"FollowTime": 4.5})}),
    (17, "negative", ["001"], "Legato text TRUE is refused (case-sensitive)",
     doc(tracks=track(clip=edit(CLIP_T, {"Legato": "TRUE"}))), "open", {"outcome": "refused"}),
    (18, "negative", ["001"], "Launch mode text 2.0 is refused",
     doc(tracks=track(clip=edit(CLIP_T, {"LaunchMode": "2.0"}))), "open", {"outcome": "refused"}),
    (19, "negative", ["001"], "Two LaunchMode elements in one clip are refused",
     doc(tracks=track(dup_launch=("LaunchMode", "2"))), "open", {"outcome": "refused"}),
    (20, "negative", ["001"], "Velocity amount text abc is refused",
     doc(tracks=track(clip=edit(CLIP_T, {"VelocityAmount": "abc"}))), "open", {"outcome": "refused"}),
    (21, "negative", ["003"], "Global quantization text 4.0 is refused", doc(gq="4.0"), "open",
     {"outcome": "refused"}),
    (22, "negative", ["002"], "Follow-action enabled text yes is refused",
     doc(tracks=track(fa=edit(FA_T, {"FollowActionEnabled": "yes"}))), "open", {"outcome": "refused"}),
    (23, "missing", ["009"], "Clip without Legato, VelocityAmount and FollowAction opens with initial values",
     doc(tracks=track(clip=edit(CLIP_T, drop=("Legato", "VelocityAmount")), fa=None)), "open-save",
     {"outcome": "opens", "values": clip_all(SC), "saved": {"values": clip_all(SC), "clip_order": SC}}),
    (24, "missing", ["009"], "Follow action without JumpIndexA opens with jump index A 1",
     doc(tracks=track(fa=edit(FA_T, {"JumpIndexB": "3"}, drop=("JumpIndexA",)))), "open-save",
     {"outcome": "opens", "values": fav(SC, {"JumpIndexA": 1.0, "JumpIndexB": 3.0}),
      "saved": {"values": fav(SC, {"JumpIndexA": 1.0, "JumpIndexB": 3.0})}}),
    (25, "missing", ["009"], "Follow action without IsLinked, LoopIterations and FollowActionEnabled",
     doc(tracks=track(fa=edit(FA_T, {"FollowTime": "8"}, drop=("IsLinked", "LoopIterations", "FollowActionEnabled")))),
     "open-save",
     {"outcome": "opens", "values": fa_all(SC, FollowTime=8.0), "saved": {"values": fa_all(SC, FollowTime=8.0)}}),
    (26, "negative", ["011"], "Launch quantization 15, outside the defined values, does not refuse the document",
     doc(tracks=track(clip=edit(CLIP_T, {"LaunchQuantisation": "15"}))), "open", {"outcome": "opens"}),
    (27, "negative", ["011"], "Launch mode 4, outside the defined values, does not refuse the document",
     doc(tracks=track(clip=edit(CLIP_T, {"LaunchMode": "4"}))), "open", {"outcome": "opens"}),
    (28, "negative", ["011"], "Follow action A 10, outside the defined values, does not refuse the document",
     doc(tracks=track(fa=edit(FA_T, {"FollowActionA": "10"}))), "open", {"outcome": "opens"}),
    (29, "positive", ["012"], "Chances 30 and 30 become 50 and 50",
     doc(tracks=track(fa=edit(FA_T, {"FollowChanceA": "30", "FollowChanceB": "30"}))), "open-save",
     {"outcome": "opens", "values": fav(SC, {"FollowChanceA": 50.0, "FollowChanceB": 50.0}),
      "saved": {"values": fav(SC, {"FollowChanceA": 50.0, "FollowChanceB": 50.0})}}),
    (30, "boundary", ["012"], "Chances 0 and 0 with follow actions enabled become 100 and 0, disabled",
     doc(tracks=track(fa=edit(FA_T, {"FollowChanceA": "0", "FollowActionEnabled": "true"}))), "open-save",
     {"outcome": "opens",
      "values": fav(SC, {"FollowChanceA": 100.0, "FollowChanceB": 0.0, "FollowActionEnabled": False}),
      "saved": {"values": fav(SC, {"FollowChanceA": 100.0, "FollowChanceB": 0.0, "FollowActionEnabled": False})}}),
    (31, "boundary", ["012"], "Chances 1 and 7 become 13 and 87 (an exact half rounds away from zero)",
     doc(tracks=track(fa=edit(FA_T, {"FollowChanceA": "1", "FollowChanceB": "7"}))), "open-save",
     {"outcome": "opens", "values": fav(SC, {"FollowChanceA": 13.0, "FollowChanceB": 87.0}),
      "saved": {"values": fav(SC, {"FollowChanceA": 13.0, "FollowChanceB": 87.0})}}),
    (32, "positive", ["012"], "Chances 1 and 2 become 33 and 67",
     doc(tracks=track(fa=edit(FA_T, {"FollowChanceA": "1", "FollowChanceB": "2"}))), "open-save",
     {"outcome": "opens", "values": fav(SC, {"FollowChanceA": 33.0, "FollowChanceB": 67.0}),
      "saved": {"values": fav(SC, {"FollowChanceA": 33.0, "FollowChanceB": 67.0})}}),
    (33, "boundary", ["012"], "Chances 0 and 50 become 0 and 100; follow actions stay disabled",
     doc(tracks=track(fa=edit(FA_T, {"FollowChanceA": "0", "FollowChanceB": "50"}))), "open-save",
     {"outcome": "opens",
      "values": fav(SC, {"FollowChanceA": 0.0, "FollowChanceB": 100.0, "FollowActionEnabled": False}),
      "saved": {"values": fav(SC, {"FollowChanceA": 0.0, "FollowChanceB": 100.0})}}),
    (34, "positive", ["012"], "Fractional chances 0.25 and 0.75 become 25 and 75",
     doc(tracks=track(fa=edit(FA_T, {"FollowChanceA": "0.25", "FollowChanceB": "0.75"}))), "open-save",
     {"outcome": "opens", "values": fav(SC, {"FollowChanceA": 25.0, "FollowChanceB": 75.0}),
      "saved": {"values": fav(SC, {"FollowChanceA": 25.0, "FollowChanceB": 75.0})}}),
    (35, "boundary", ["012"], "Chances 100 and 0 with follow actions enabled are unchanged and stay enabled",
     doc(tracks=track(fa=edit(FA_T, {"FollowActionEnabled": "true"}))), "open-save",
     {"outcome": "opens",
      "values": fav(SC, {"FollowChanceA": 100.0, "FollowChanceB": 0.0, "FollowActionEnabled": True}),
      "saved": {"values": fav(SC, {"FollowChanceA": 100.0, "FollowChanceB": 0.0, "FollowActionEnabled": True})}}),
    (36, "missing", ["009", "012"], "Chance A 30 without FollowChanceB becomes 100 and 0",
     doc(tracks=track(fa=edit(FA_T, {"FollowChanceA": "30"}, drop=("FollowChanceB",)))), "open-save",
     {"outcome": "opens", "values": fav(SC, {"FollowChanceA": 100.0, "FollowChanceB": 0.0}),
      "saved": {"values": fav(SC, {"FollowChanceA": 100.0, "FollowChanceB": 0.0})}}),
    (37, "boundary", ["013"], "Follow time 2.0000001 becomes exactly 2",
     doc(tracks=track(fa=edit(FA_T, {"FollowTime": "2.0000001"}))), "open-save",
     {"outcome": "opens", "values": fav(SC, {"FollowTime": 2.0}),
      "saved": {"values": fav(SC, {"FollowTime": 2.0})}}),
    (38, "boundary", ["013"], "Follow time 3.0000002 becomes 11531521/3843840",
     doc(tracks=track(fa=edit(FA_T, {"FollowTime": "3.0000002"}))), "open",
     {"outcome": "opens", "values": fav(SC, {"FollowTime": FT3})}),
    (39, "boundary", ["013"], "Follow time 1e-8 becomes 0",
     doc(tracks=track(fa=edit(FA_T, {"FollowTime": "1e-8"}))), "open-save",
     {"outcome": "opens", "values": fav(SC, {"FollowTime": 0.0}), "saved": {"values": fav(SC, {"FollowTime": 0.0})}}),
    (40, "positive", ["013"], "Follow time 1.3333333 becomes 4/3",
     doc(tracks=track(fa=edit(FA_T, {"FollowTime": "1.3333333"}))), "open",
     {"outcome": "opens", "values": fav(SC, {"FollowTime": 4 / 3})}),
    (41, "positive", ["009", "012", "014"], "11.0_405 clip, follow time 4, actions 0 and 0: linked, A becomes Next",
     doc(OLD405, tracks=track(fa=None, old=OLD_T)), "open-save",
     {"outcome": "opens", "values": fa_all(SC),
      "saved": {"values": fa_all(SC), "absent": [f"{SC}/{n}" for n in OLD], "clip_order": SC}}),
    (42, "positive", ["009", "012", "014"], "11.0_405 clip with A 3 at 0.5 and B 1 at 0.5: enabled, unlinked, 50/50",
     doc(OLD405, tracks=track(fa=None, old=edit(OLD_T, {"FollowTime": "8", "FollowActionA": "3", "FollowActionB": "1",
                                                        "FollowChanceA": "0.5", "FollowChanceB": "0.5"}))),
     "open-save",
     {"outcome": "opens",
      "values": fa_all(SC, FollowTime=8.0, IsLinked=False, FollowActionA=3, FollowActionB=1, FollowChanceA=50.0,
                       FollowChanceB=50.0, FollowActionEnabled=True),
      "saved": {"values": fa_all(SC, FollowTime=8.0, IsLinked=False, FollowActionA=3, FollowActionB=1,
                                 FollowChanceA=50.0, FollowChanceB=50.0, FollowActionEnabled=True),
                "absent": [f"{SC}/{n}" for n in OLD], "clip_order": SC}}),
    (43, "positive", ["012", "014"], "11.0_405 clip with A 2 at 0.25 and B 4 at 0.75, follow time 4: enabled, unlinked",
     doc(OLD405, tracks=track(fa=None, old=edit(OLD_T, {"FollowActionA": "2", "FollowActionB": "4",
                                                        "FollowChanceA": "0.25", "FollowChanceB": "0.75"}))),
     "open-save",
     {"outcome": "opens",
      "values": fa_all(SC, IsLinked=False, FollowActionA=2, FollowActionB=4, FollowChanceA=25.0, FollowChanceB=75.0,
                       FollowActionEnabled=True),
      "saved": {"values": fav(SC, {"IsLinked": False, "FollowActionA": 2, "FollowChanceA": 25.0,
                                   "FollowActionEnabled": True})}}),
    (44, "boundary", ["014"], "11.0_405 clip, follow time 8, actions 0 and 0: unlinked, A stays No Action",
     doc(OLD405, tracks=track(fa=None, old=edit(OLD_T, {"FollowTime": "8"}))), "open",
     {"outcome": "opens", "values": fa_all(SC, FollowTime=8.0, IsLinked=False, FollowActionA=0)}),
    (45, "missing", ["014"], "11.0_405 clip without FollowTime: follow time 1, unlinked",
     doc(OLD405, tracks=track(fa=None, old=edit(OLD_T, drop=("FollowTime",)))), "open",
     {"outcome": "opens", "values": fa_all(SC, FollowTime=1.0, IsLinked=False, FollowActionA=0)}),
    (46, "positive", ["014"], "12.0_12117 scene meeting the linked condition gets IsLinked true",
     doc(SCN, scenes=LINKED_SCENE), "open", {"outcome": "opens", "values": fav(SN, {"IsLinked": True})}),
    (47, "positive", ["014"], "12.0_12117 scene with follow time 8 gets IsLinked false",
     doc(SCN, scenes=edit(FA_T, {"FollowTime": "8"})), "open",
     {"outcome": "opens", "values": fav(SN, {"IsLinked": False, "FollowTime": 8.0})}),
    (48, "missing", ["014"], "12.0_12117 scene without FollowAction gets the conversion's follow action",
     doc(SCN, scenes="bare"), "open",
     {"outcome": "opens", "values": fa_all(SN, FollowActionA=0)}),
    (49, "negative", ["014"], "12.0_12117 scene with follow actions enabled gets IsLinked false",
     doc(SCN, scenes=edit(FA_T, {"FollowActionEnabled": "true"})), "open",
     {"outcome": "opens", "values": fav(SN, {"IsLinked": False, "FollowActionEnabled": True})}),
    (50, "negative", ["014"], "12.0_12402 scene is not converted: IsLinked false stays false",
     doc(scenes=LINKED_SCENE), "open", {"outcome": "opens", "values": fav(SN, {"IsLinked": False})}),
]
# scenes="bare": a Scenes element whose first scene has no FollowAction
COMPARATOR = {
    "open": "outcome exact; listed values exact (binary32 compared after exact widening)",
    "open-save": "outcome exact; listed values exact; saved document compared as parsed XML for listed values "
                 "(single element, only attribute Value, text read back with the release's rules), absent paths "
                 "and clip_order only",
}


# ---- independent cross-check model of the released clauses (not an oracle) ----
class Refused(Exception):
    pass


class NoExpectation(Exception):
    pass


def read_bool(t):
    if t in ("true", "1"):
        return True
    if t in ("false", "0"):
        return False
    raise Refused(t)


def read_int(t):
    if re.fullmatch(r" +\+?\d+ +|\+\d+ +", t) or "-" in t:
        raise NoExpectation(f"integer form {t!r}")
    if not t.isascii() or not t.strip(" "):
        raise Refused(t)
    body = t.strip(" ")
    body = body[1:] if body.startswith("+") else body
    if not re.fullmatch(r"\d{1,63}", body):
        raise Refused(t)
    if len(body) > 9:
        raise NoExpectation(f"ten or more digits {t!r}")
    return int(body)


def read_f64(t):
    rest = t.lstrip(" ").lstrip("+-").lower()
    if t == "Invalid" or t.startswith("#") or rest.startswith(("0x", "inf", "nan")) or re.match(r"^ *[^\S ]", t):
        raise NoExpectation(f"number form {t!r}")
    m = re.match(r"^ *([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)", t)
    if not m:
        raise Refused(t)
    return float(m.group(1))


def read(name, t):
    kind = TYPE[name]
    return {"bool": read_bool, "int": read_int, "f64": read_f64, "f32": lambda s: f32(read_f64(s))}[kind](t)


def write(name, v):
    return ("true" if v else "false") if TYPE[name] == "bool" else str(v) if TYPE[name] == "int" else repr(v)


def kids(el, name):
    return [c for c in el if c.tag == name]


def leaf_value(el, name, required=True):
    found = kids(el, name)
    if not found:
        if required:
            raise NoExpectation(f"missing {name}")
        return None
    if len(found) > 1 or found[0].get("Value") is None or list(found[0]) or set(found[0].attrib) != {"Value"}:
        raise NoExpectation(f"shape of {name}")
    return found[0].get("Value")


def num(el, name, default):
    t = leaf_value(el, name, required=False)
    return default if t is None else read(name, t)


def add_leaf(parent, name, value):
    ET.SubElement(parent, name, Value=write(name, value))


# conversion steps on the document tree (before values are read)
def step406(clip):
    if kids(clip, "FollowAction"):
        raise NoExpectation("old clip with FollowAction")
    texts = {n: leaf_value(clip, n, required=(n != "FollowTime")) for n in OLD}
    for n in OLD:
        for c in kids(clip, n):
            clip.remove(c)
    fa = ET.SubElement(clip, "FollowAction")
    ft = 1.0 if texts["FollowTime"] is None else read("FollowTime", texts["FollowTime"])
    add_leaf(fa, "FollowTime", ft)
    for n in OLD[1:]:
        ET.SubElement(fa, n, Value=texts[n])


def step417(fa):
    if kids(fa, "FollowActionEnabled"):
        return
    a, b = num(fa, "FollowActionA", 0), num(fa, "FollowActionB", 0)
    ca, cb = num(fa, "FollowChanceA", 0.0), num(fa, "FollowChanceB", 0.0)
    add_leaf(fa, "FollowActionEnabled", (a != 0 and ca != 0) or (b != 0 and cb != 0))


def step421(fa):
    if kids(fa, "IsLinked"):
        raise NoExpectation("IsLinked before 421")
    linked = (not read("FollowActionEnabled", leaf_value(fa, "FollowActionEnabled"))
              and read("FollowActionA", leaf_value(fa, "FollowActionA")) == 0
              and read("FollowActionB", leaf_value(fa, "FollowActionB")) == 0
              and read("FollowTime", leaf_value(fa, "FollowTime")) == 4.0)
    if linked:
        kids(fa, "FollowActionA")[0].set("Value", "4")
    add_leaf(fa, "IsLinked", linked)


def step12203(scene):
    found = kids(scene, "FollowAction")
    if not found:
        fa = ET.SubElement(scene, "FollowAction")
        for n, v in {**FA_INIT, "FollowActionA": 0}.items():
            add_leaf(fa, n, v)
        return
    fa = found[0]
    g = {n: read(n, leaf_value(fa, n)) for n in FA_NAMES if n != "IsLinked"}
    linked = (not g["FollowActionEnabled"] and g["FollowTime"] == 4.0 and g["FollowActionA"] == 4
              and g["FollowActionB"] == 0 and g["FollowChanceA"] == 100.0 and g["FollowChanceB"] == 0.0)
    for c in kids(fa, "IsLinked"):
        fa.remove(c)
    add_leaf(fa, "IsLinked", linked)


def frinta(x):
    return math.floor(x) + (1.0 if x - math.floor(x) >= 0.5 else 0.0) if x >= 0 else -frinta(-x)


def round_lattice(x):
    lo, hi = math.floor(x * LATTICE), math.floor(x * LATTICE) + 1
    if abs(x * LATTICE - (lo + 0.5)) < 1e-9 * LATTICE:
        raise NoExpectation("follow time near a half-multiple")
    return (hi if x * LATTICE - lo > 0.5 else lo) / LATTICE


def load_fa(fa_el):
    """Read a follow action (absent items keep initial values), then apply the opening corrections."""
    v = dict(FA_INIT)
    if fa_el is not None:
        for c in fa_el:
            if c.tag not in FA_NAMES:
                raise NoExpectation(f"unknown follow-action child {c.tag}")
        for n in FA_NAMES:
            t = leaf_value(fa_el, n, required=False)
            if t is not None:
                v[n] = read(n, t)
    for n in FA_NAMES:
        if n in RANGE and n not in ENUMS and not RANGE[n][0] <= v[n] <= RANGE[n][1]:
            raise NoExpectation(f"{n} out of range")
    a, b = v["FollowChanceA"], v["FollowChanceB"]
    if a == 0 and b == 0:
        v["FollowChanceA"], v["FollowActionEnabled"] = 100.0, False
    else:
        v["FollowChanceA"] = frinta(f32(a / f32(f32(a + b) / 100.0)))
        v["FollowChanceB"] = f32(100.0 - v["FollowChanceA"])
    v["FollowTime"] = round_lattice(v["FollowTime"])
    return v


def load_clip(clip):
    for n in LAUNCH:
        if len(kids(clip, n)) > 1:
            raise Refused("duplicate " + n)
    v = {"LaunchMode": read("LaunchMode", leaf_value(clip, "LaunchMode")),
         "LaunchQuantisation": read("LaunchQuantisation", leaf_value(clip, "LaunchQuantisation"))}
    for n, d in CLIP_INIT.items():
        v[n] = num(clip, n, d)
    if not 0.0 <= v["VelocityAmount"] <= 1.0:
        raise NoExpectation("velocity amount out of range")
    fa = kids(clip, "FollowAction")
    return v, load_fa(fa[0] if fa else None)


def model(text):
    """Return (outcome, values {path: value}, out_of_range paths, saved LiveSet element or None)."""
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return "refused", None, None, None
    minor = root.get("MinorVersion")
    assert root.tag == "Ableton" and root.get("MajorVersion") == "5" and root.get("SchemaChangeCount") == "1"
    c = {"12.0_12402": 12402, "12.0_12117": 12117, "11.0_405": 405}[minor]
    live = copy.deepcopy(root.find("LiveSet"))
    clips = {p: live.find(p) for p in (SC, SA, AR) if live.find(p) is not None}
    scene = live.find(SN)
    try:
        for clip in clips.values():  # conversion steps, increasing order, numbers above c
            if c < 406:
                step406(clip)
            fa = kids(clip, "FollowAction")
            if c < 417 and fa:
                step417(fa[0])
            if c < 421 and fa:
                step421(fa[0])
        if scene is not None and c < 12203:
            step12203(scene)
        values, wide = {}, []
        for name in (GQ, AQ):
            values[name] = read(name, leaf_value(live, name))
            if not RANGE[name][0] <= values[name] <= RANGE[name][1]:
                raise NoExpectation(f"{name} out of range")
        loaded = {}
        for p, clip in clips.items():
            cv, fv = load_clip(clip)
            loaded[p] = (cv, fv)
            values.update({f"{p}/{k}": x for k, x in cv.items()})
            values.update({f"{p}/FollowAction/{k}": x for k, x in fv.items()})
            for k in ENUMS:
                x = cv.get(k, fv.get(k))
                if not RANGE[k][0] <= x <= RANGE[k][1]:
                    wide.append(k)
        if scene is not None:
            fv = load_fa(scene.find("FollowAction"))
            values.update({f"{SN}/FollowAction/{k}": x for k, x in fv.items()})
    except Refused:
        return "refused", None, None, None
    saved = ET.Element("LiveSet")
    for p, (cv, fv) in loaded.items():  # save: launch elements in order, follow action with its ten children
        parts = p.split("/")
        parent = saved
        for part in parts:
            parent = ET.SubElement(parent, part.split("[")[0])
        for n in LAUNCH[:4]:
            add_leaf(parent, n, cv[n])
        fa = ET.SubElement(parent, "FollowAction")
        for n in FA_NAMES:
            add_leaf(fa, n, fv[n])
    return "opens", values, wide, saved


def judge(expected, outcome, values, wide, saved):
    if outcome != expected["outcome"]:
        return [f"outcome {outcome}"]
    errs = []
    if outcome == "opens" and wide and "values" in expected:
        if any(k.split("/")[-1] in wide for k in expected["values"]):
            errs.append("judged value is out of range")
    for k, v in expected.get("values", {}).items():
        if k not in values or values[k] != v or type(values[k]) is not type(v):
            errs.append(f"value {k}={values.get(k)!r}")
    sv = expected.get("saved", {})
    for path, v in sv.get("values", {}).items():
        els = saved.findall(path)
        if len(els) != 1 or list(els[0]) or set(els[0].attrib) != {"Value"} \
                or read(path.split("/")[-1], els[0].get("Value")) != v:
            errs.append(f"saved {path}")
    for path in sv.get("absent", []):
        if saved.findall(path):
            errs.append(f"present {path}")
    if sv.get("clip_order"):
        clip = saved.find(sv["clip_order"])
        names = [c.tag for c in clip if c.tag in LAUNCH]
        fa = clip.find("FollowAction")
        if names != LAUNCH or [c.tag for c in fa] != FA_NAMES:
            errs.append("clip order")
    return errs


def mutate(expected):
    """Return a copy with the first judged value changed, for the mutation self-test."""
    e = copy.deepcopy(expected)
    for part in (e.get("values"), e.get("saved", {}).get("values")):
        if part:
            k = next(iter(part))
            v = part[k]
            part[k] = (not v) if isinstance(v, bool) else v + 1 if isinstance(v, int) else v * 2 + 1
            return e
    e["outcome"] = "refused" if e["outcome"] == "opens" else "opens"
    return e


# ---- packaging ----
def cid(n):
    return f"CLIP-LAUNCH-{n:03d}"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def manifest_skeleton():
    return {
        "schema": "handoff-manifest-v1", "release_id": "clip-launch-v1",
        "release_status": "candidate-unreviewed", "release_date": None, "target": TARGET,
        "specification": {"id": "SPEC-CLIP-LAUNCH", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-SESSION", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": {
            R + "001": "Launch elements of session MIDI and audio clips and arrangement MIDI clips: location, types, reading rules, refusal of refused text and of a repeated launch element, saved form, relative order and read-back value. Saved text not released",
            R + "002": "Follow-action compound: ten children, types, reading rules; saved with exactly these children in order. Scene compound only as converted by REQ-014",
            R + "003": "GlobalQuantisation and AutoQuantisation location, integer type and reading rule. Saved form not released",
            R + "004": "Launch mode values 0-3 and their labels",
            R + "005": "Clip launch quantization 0-14 and global quantization 0-13 with labels; clip value k>=1 denotes global value k-1, clip value 0 denotes the global setting",
            R + "006": "Record quantization values 0-8 and their labels; effect on recording excluded",
            R + "007": "Follow-action values 0-9 and their labels",
            R + "009": "Initial clip and follow-action values for absent Legato, VelocityAmount, FollowAction or follow-action children; written on save",
            R + "011": "Out-of-range launch mode, launch quantization or follow-action values of at most nine digits do not refuse the document; nothing else",
            R + "012": "Follow-chance rescaling on opening for chances 0-100 in binary32 arithmetic with halves away from zero",
            R + "013": "Follow-time rounding on opening to the nearest multiple of 1/3,843,840, halves away from zero, for values 0 to below 1,000,000 not near a half-multiple",
            R + "014": "Conversion steps 406, 417 and 421 for clips of 11.0_405 documents and 12203 for scenes of 12.0_12117 documents, applied before reading; no conversion at 12.0_12402",
            R + "015": "Grid length denoted by each global quantization value for a given time signature; definitional, no case",
        },
        "unreleased_requirements": [R + "008", R + "010", R + "016", R + "017", R + "018", R + "019", R + "020",
                                    R + "021", R + "022", R + "023"],
        "compatibility_dimensions": {
            "project-files": "static-derived expectations for the listed document values; reference execution not-run",
            "behavior": "launching excluded: timing, grid placement, launch modes, legato, velocity, follow actions",
            "ui": "excluded (labels define meaning; displayed text not graded)",
            "audio": "excluded", "timing": "excluded",
        },
        "exclusions": {
            "inputs_without_expectation": [
                "a clip without LaunchMode or LaunchQuantisation; a LiveSet without GlobalQuantisation or AutoQuantisation",
                "a launch element or follow-action child without a Value attribute, with other attributes or with child elements",
                "GlobalQuantisation outside 0-13 and AutoQuantisation outside 0-8",
                "VelocityAmount outside 0-1; chances negative or above 100; jump indices outside -1 to 8,388,608; LoopIterations outside 1 to 1,073,741,823; FollowTime negative, 1,000,000 or more, or within 1e-9 of a half-multiple of 1/3,843,840",
                "number text starting (after spaces and sign) with 0x, inf or nan; Invalid; text starting with #; leading whitespace other than U+0020",
                "integer text with spaces both before and after the digits, a plus sign with trailing spaces, any minus sign, or ten or more digits within 63 characters",
                "repeated or unknown children of FollowAction; unknown children or attributes of a clip element",
                "clips other than at the named locations, including take lanes and the groove pool",
                "in 11.0_405 documents: a clip that already has FollowAction, a clip without FollowActionA, FollowActionB, FollowChanceA or FollowChanceB, or with FollowActionEnabled or IsLinked; scenes",
                "in 12.0_12117 documents: a scene FollowAction without all ten children",
                "other envelopes, format versions, compressed containers and document kinds",
                "documents that break more than one refusal rule",
            ],
            "behavior": [
                "launching: start time, grid placement, the time signature a launch uses, launches without a grid or with the transport stopped, Gate, Toggle and Repeat, Legato, velocity scaling, follow-action timing and chance selection",
                "displayed text, including where each follow-action label set is shown",
                "value held, displayed or saved for an out-of-range launch mode, launch quantization or follow-action value",
                "text written for numbers and Booleans; layout; save container and envelope; saved form of set-level values and of scenes",
                "initial launch mode and quantization of a new clip and the related preferences; set initial values; File > New; clip creation paths",
                "conversion steps other than 406, 417, 421 and 12203; the conversion error for a clip that has both forms",
                "scripting interface names, properties and value assignment",
                "effect of record quantization; scene follow actions other than their conversion",
                "editing after opening, undo, refusal text and presentation",
            ],
        },
        "fixture_origin": "independently authored minimal XML documents from a template written for this release; no shipped file content",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None,
                   "record": None},
        "supersedes": None, "entrypoint": "README.md", "case_count": len(CASES),
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def build():
    shutil.rmtree(STAGE / "fixtures", ignore_errors=True)
    (STAGE / "fixtures").mkdir(parents=True)
    cases = []
    for n, kind, reqs, purpose, text, action, expected in CASES:
        rel = f"fixtures/{cid(n)}.xml"
        (STAGE / rel).write_text(text)
        cases.append({"id": cid(n), "kind": kind, "purpose": purpose, "requirements": [R + r for r in reqs],
                      "input": rel, "action": action, "expected": expected, "expectation_provenance": PROV,
                      "reference_execution": "not-run", "candidate_execution": "not-run",
                      "comparator": COMPARATOR[action]})
    (STAGE / "cases.json").write_text(json.dumps({
        "schema": "clip-launch-cases-v1", "target": TARGET,
        "scope": "clip-launch-v1 partial requirement clauses only (see spec.md)",
        "status": "candidate-unreviewed",
        "fixture_origin": "Independently authored minimal XML documents; no shipped file copied or excerpted",
        "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
        "representation": {
            "paths": "relative to /Ableton/LiveSet; X[1] is the first child element named X",
            "values": "value held after opening; type by element name (see spec.md); binary32 compared after exact widening",
            "saved": "values: path -> value read back from the saved Value text; absent: paths; clip_order: clip path whose launch elements and follow-action children are checked for order",
            "note": "project comparison representation, not an API of the original application or a required design"},
        "cases": cases}, indent=1) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_skeleton(), indent=1) + "\n")
    print(len(cases), "cases staged")


# ---- analyst-only traceability ----
S5 = "analysis/ableton-live-12.4.3/r2/s5-clip-launch-v1/"
N1 = "analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/"
E = {
    "fields": S5 + "static-survey.json schema.field_order_latest, homonyms_latest, evolution; clip-records.tsv (4,130 clips); "
                   "registry-order-check.txt (28 AClip and 10 AFollowAction registrations = 12.0_12402 order)",
    "io": S5 + "notes.md 'Static checks run': AClip vtable 0x1067b6cc0 and AFollowAction 0x1067c8830 hold loader 0x101487310 "
               "(+0x140) and writer 0x101486cdc (+0x138) (read_ptrs.py)",
    "text": "handoff/transport-state-v1 REQ-003/004/005/006 (released rules); " + N1 + "0x10152bfb8 Bool/Int/Float/Double branches; "
            "0x1002fd908 integer acceptance (n1-0006)",
    "dup": N1 + "add-member 0x101472624 'already has member' (n1-0007)",
    "enums": S5 + "corpus 0x102438b44 (launch mode); results/s5-0002 0x102438d00 (15 clip values); results/s5-0001 0x10266f738 "
                  "(14 global, 9 record labels by string-reference order); 0x102503ea0 and s5-0001 0x102505724 (follow actions, short 'Again')",
    "clipgrid": S5 + "results/s5-0001 0x102442998 (non-zero k -> grid(k - 1) with clip signature; 0 -> song grid)",
    "init": S5 + "results/s5-0001 0x102436fc4 (Legato false, VelocityAmount UserFloat 0..1 value 0), 0x102505030 (FollowTime 4.0, "
                 "IsLinked true, LoopIterations 1, Enabled false), 0x102505724 (A 4 at 100, B 0 at 0, jump 1.0); s5-0004 0x1015743b0",
    "absent": "wiki/research/transport-state-native.md 'How a set reaches the transport objects' (generic loader leaves absent "
              "members at constructor values; inferred for AClip/AFollowAction from the shared loader)",
    "enumload": S5 + "notes.md / spec appendix CL-15: loader stores the enum index directly, setter 0x10156675c not called (N1)",
    "postload": S5 + "notes.md: post-load slot +0xd0 AClip 0x102441a30, AFollowAction 0x1025044b4",
    "chance": S5 + "results/s5-0003 0x1025044b4 disassembly 0x1025044f0-0x102504584: fcmp A,B with 0; fadd; fdiv by 100.0f; "
                   "fdiv A by it; frinta; setter +0x280; 100 - A; Enabled via 0x101564698(...,0) in the zero branch",
    "ftround": S5 + "s5-0001 0x102505030 calls 0x101565624(...,1,1) (sets +0x70); " + N1 + "corpus 0x10156580c; bytes "
               "0x101565860-0x1015658ac re-read from Live.arm64 on 2026-10-18 with fp_opcodes.py: fcmp/fcsel sign, fmadd "
               "x + s*(1/3843840)*0.5, fabs, fmul 3843840.0, frintm, fdiv, fmul sign (same sequence as the grid rounding in 0x101aaae44)",
    "registry": S5 + "notes.md pre-round: translators registered in 0x10148ec98 (0x196, 0x1a1, 0x1a5, 0x2ee8, 0x2fab)",
    "m406": S5 + "results/s5-0003 0x1014b6d14.c: FollowTime default 1.0 when absent; FollowChanceA default 1.0, B 0; "
                 "'Unexpected member FollowAction' when present (excluded)",
    "m417": S5 + "results/s5-0003 0x1014b82d8.c: only when FollowActionEnabled absent; (A!=0 && chA!=0) || (B!=0 && chB!=0)",
    "m421": S5 + "results/s5-0002 0x1014b8b00 (disassembly mov w1,#0x4 at 0x1014b8be4): IsLinked := !Enabled && A==0 && B==0 && FT==4.0, then A := 4",
    "m12203": S5 + "results/s5-0004 0x1014c04d0.c (pseudocode; disassembly retained): default scene FollowAction "
                   "(4.0, 1, 0, 0, 100, 0, false, 1, 1, IsLinked true); else IsLinked := !Enabled && FT==4 && A==4 && B==0 && chA==100 && chB==0",
    "schemas": "analysis/ableton-live-12.4.3/r2/s2-static-v1/out/schemas.json: 11.0_405, 12.0_12117, 12.0_12402 in S; "
               "11.0_405 MidiClip holds FollowTime..FollowChanceB after VelocityAmount; 11.0_405 LiveSet has no Scenes",
    "grid": S5 + "results/s5-0001 0x101aaae44: sub w8,w1,#1; cmp w8,#0xc; b.hi default 0; jump table 0x105846ef8; constants "
                 "8*bar, 2*bar (fadd), 2.0, 1/3, 1/6, 0.125 spot-checked in the dossier on 2026-10-18",
}
A = {
    "A2": "A clip and its follow action read from a document start with the initial values and receive only the members "
          "present, stored as read without range checks (spec r1 A2). Payload: first bullet of 'What the contract means'.",
    "A3": "The opening corrections run for every clip read from a Live Set (spec r1 A3). Payload: second bullet.",
    "A5": "Conversion applies every step numbered above the suffix number, in increasing order, before values are read "
          "(spec r1 A5). Payload: fourth bullet.",
    "A7": "The chance setter (+0x280) stores the computed values unchanged for integral results in 0..100; the chance "
          "controller 0x10652b4d8 was not read (spec r1 REQ-012 U clause). Payload: third bullet.",
}
SRC = {1: "CLC-002", 2: "CLC-001", 3: "REQ-004/005 largest values (new; CLC-018 reached them through the scripting interface)", 4: "REQ-001 audio clip (new)",
       5: "CLC-009 (authored arrangement clip)", 6: "CLC-006", 7: "CLC-007", 8: "REQ-005 boundary (new)", 9: "CLC-008",
       10: "REQ-006 boundary (new)", 11: "CLC-010", 12: "REQ-001 Boolean and binary32 (new)", 13: "REQ-001 Boolean '1' (new)",
       14: "REQ-001 binary32 rounding (new)", 15: "REQ-001 integer spellings (new)", 16: "REQ-002 decimal prefix (new)",
       17: "CLC-003", 18: "CLC-004", 19: "CLC-005", 20: "REQ-001 binary32 refusal (new)", 21: "REQ-003 integer refusal (new)",
       22: "REQ-002 Boolean refusal (new)", 23: "CLC-011", 24: "CLC-012", 25: "REQ-009 follow-action children (new)",
       26: "CLC-014 narrowed to outcome", 27: "CLC-015 narrowed to outcome", 28: "REQ-011 follow action (new)",
       29: "CLC-019", 30: "CLC-020", 31: "CLC-021", 32: "CLC-022", 33: "REQ-012 zero A (new)",
       34: "REQ-012/014 fraction example (new, at 12.0_12402)", 35: "REQ-012 enabled unchanged (new)",
       36: "REQ-009 + REQ-012 (new)", 37: "CLC-024", 38: "CLC-025 (values instead of saved text)", 39: "REQ-013 example 1e-8 (new)",
       40: "REQ-013 triplet lattice (new)", 41: "CLC-028 (authored 11.0_405 fixture)", 42: "CLC-029 (authored 11.0_405 fixture)",
       43: "REQ-014 step 417 then 421 (new)", 44: "REQ-014 step 421 FT != 4 (new)", 45: "REQ-014 step 406 default (new)",
       46: "CLC-026 (authored 12.0_12117 fixture; values instead of saved)", 47: "CLC-027 (values instead of saved)",
       48: "REQ-014 step 12203 default (new)", 49: "REQ-014 step 12203 enabled (new)", 50: "REQ-014 no conversion at 12402 (new)"}
EV = {"001": ["fields", "io", "text"], "002": ["fields", "io", "text"], "003": ["fields", "text"], "004": ["enums"],
      "005": ["enums", "clipgrid"], "006": ["enums"], "007": ["enums"], "009": ["init", "absent", "io"],
      "011": ["enumload", "text"], "012": ["chance", "postload"], "013": ["ftround", "postload"],
      "014": ["registry", "m406", "m417", "m421", "m12203", "schemas"]}
AS = {"001": [], "002": [], "003": [], "004": [], "005": [], "006": [], "007": [], "009": ["A2"], "011": ["A2"],
      "012": ["A2", "A3", "A7"], "013": ["A2", "A3"], "014": ["A2", "A3", "A5"]}
REMOVED = {"CLC-013": "REQ-010 unreleased (preference defaults, Q-017)", "CLC-016, CLC-017": "scripting interface excluded",
           "CLC-018": "API part excluded; values covered by case 003", "CLC-023": "chance above the 0-100 bound (A2 for floats unestablished)",
           "CLC-030": "REQ-008 unreleased (Q-017)", "CLC-031 to CLC-056": "launch timing, REQ-016 to 019 unreleased (A1, A4, Q-017)"}

DENY = [r"0x1[0-9a-f]{5,}", r"FUN_", r"\bA(Clip|FollowAction|Song|Scene)\w*", r"\bL(Song|Clip)\w*", r"Remoteable",
        r"UserFloat", r"RangedRemote", r"[Tt]ranslator", r"\bChangeCount\b", r"registr", r"vtable", r"constructor",
        r"post-load", r"loader", r"setter", r"\bslot \+", r"frint", r"fcsel", r"fmadd", r"Ghidra", r"decompil",
        r"pseudocode", r"disassembl", r"dossier", r"corpus", r"\bs5-0", r"\bn1-0", r"PRB-", r"\bQ-0\d", r"CLC-",
        r"\bA[1-7]\b", r"\bCL-\d", r"analysis/", r"wiki/", r"\.\./", r"/home/", r"/var/", r"/tmp/", r"derivation",
        r"traceab", r"Python", r"\bq_\w+", r"launch_mode", r"launch_quantization", r"clip_trigger", r"rec_q",
        r"Invalid launch", r"out of range'", r"Unexpected member", r"Enum value", r"Drums Lesson", r"Core Library",
        r"DefaultLiveSet", r"Vocal Recording", r"Chuck Sutton", r"Driver Error", r"Chord C", r"UpdateEngine",
        r"Quantisation(Time|KeyMidi)", r"OSlot", r"build_clip", r"\bev_[0-9a-f]", r"\bS5\b", r"\bN1\b", r"Live\.arm64",
        r"strtod", r"printf", r"from_chars"]
ALLOWED_HITS = {"AGENTS.md": {"decompil"}}  # forbidden-inputs list, same wording as released packages


def links(pkg, md):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
        path, _, anchor = target.partition("#")
        dest = (md.parent / path).resolve() if path else md
        ok = not re.match(r"[a-z]+:", target) and dest.is_file() and pkg in dest.parents
        if ok and anchor:
            ok = anchor in {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                            for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
        out.append((target, ok))
    return out


def check(pkg, rewrite):
    pkg = pkg.resolve()
    doc_ = json.loads((pkg / "cases.json").read_text())
    problems, mutants, inputs = {}, 0, set()
    for c in doc_["cases"]:
        raw = (pkg / c["input"]).read_bytes()
        inputs.add(raw)
        errs = [] if raw.isascii() and b"\r" not in raw and b"\t" not in raw and raw.endswith(b"\n") else ["format"]
        try:
            outcome, values, wide, saved = model(raw.decode("ascii"))
            errs += judge(c["expected"], outcome, values, wide, saved)
            mutants += bool(judge(mutate(c["expected"]), outcome, values, wide, saved))
            if c["action"] == "open" and c["expected"].get("saved"):
                errs.append("saved part on an open case")
        except NoExpectation as e:
            errs.append(f"fixture hits an exclusion: {e}")
        ET.fromstring(raw)  # every fixture is well-formed; refusals come from value text, not XML
        if errs:
            problems[c["id"]] = errs
    files = sorted(p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.json")
    manifest = json.loads((pkg / "manifest.json").read_text())
    if rewrite:
        manifest["files"] = [{"path": str(p.relative_to(pkg)), "sha256": sha(p.read_bytes()),
                              "bytes": p.stat().st_size} for p in files]
        (pkg / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    listed = {f["path"]: f for f in manifest["files"]}
    deny = {}
    for p in [*files, pkg / "manifest.json"]:
        hits = sorted({m for pat in DENY for m in re.findall(pat, p.read_text())})
        hits = [h for h in hits if not any(h.startswith(a) for a in ALLOWED_HITS.get(p.name, ()))]
        if hits:
            deny[str(p.relative_to(pkg))] = hits
    return {
        "cases": len(doc_["cases"]), "manifest_case_count": manifest["case_count"], "case_problems": problems,
        "mutations_detected": f"{mutants}/{len(doc_['cases'])}", "distinct_inputs": len(inputs),
        "payload_files": len(files), "files_including_manifest": len(files) + 1,
        "manifest_sha256": sha((pkg / "manifest.json").read_bytes()),
        "hash_or_size_mismatches": [k for k, f in listed.items() if not (pkg / k).is_file()
                                    or sha((pkg / k).read_bytes()) != f["sha256"] or (pkg / k).stat().st_size != f["bytes"]],
        "inventory_differences": sorted({str(p.relative_to(pkg)) for p in files} ^ set(listed)),
        "symlinks": [str(p) for p in pkg.rglob("*") if p.is_symlink()],
        "markdown_links": {md.name: len(links(pkg, md)) for md in pkg.glob("*.md")},
        "unresolved_links": {md.name: [t for t, ok in links(pkg, md) if not ok] for md in pkg.glob("*.md")
                             if not all(ok for _, ok in links(pkg, md))},
        "missing_case_inputs": [c["input"] for c in doc_["cases"] if not (pkg / c["input"]).is_file()],
        "deny_list_hits": deny, "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()},
        "limits": "Checks authored consistency only: no reference or candidate executed; the cross-check model is an "
                  "independent restatement of the same static evidence, not an oracle.",
    }


def seal():
    rep = check(STAGE, rewrite=True)
    rep = {"schema": "author-validation-v1", "package": "clip-launch-v1 (staged candidate)",
           "python": sys.version.split()[0], **rep}
    (HERE / "author-validation.json").write_text(json.dumps(rep, indent=1) + "\n")
    cases = {}
    for n, kind, reqs, *_ in CASES:
        cases[cid(n)] = {"source": SRC[n], "evidence": sorted({k for r in reqs for k in EV[r]}),
                         "assumptions": sorted({a for r in reqs for a in AS[r]})}
    trace = {"schema": "clip-launch-traceability-v1", "spec": "SPEC-CLIP-LAUNCH r1", "evidence": E, "assumptions": A,
             "cases": cases, "parent_cases_not_released": REMOVED}
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1) + "\n")
    print(json.dumps({k: rep[k] for k in ("cases", "case_problems", "mutations_detected", "distinct_inputs",
                                          "payload_files", "hash_or_size_mismatches", "inventory_differences",
                                          "unresolved_links", "missing_case_inputs", "deny_list_hits",
                                          "manifest_sha256")}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "seal":
        seal()
    else:
        print(json.dumps(check(Path(sys.argv[2]), rewrite=False), indent=1))
