"""Reviewer's own restatement of clip-launch-v1 (written from the evidence, not from build_clip.py).

usage: python3 -I reviewer_model.py <package dir>
Prints one line per case (agree/DISAGREE) and a summary. Also checks that every graded saved
number has at most six significant decimal digits (narrowed REQ-001 clause 6).
"""
import json, re, struct, sys, xml.etree.ElementTree as ET
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

N = 3843840
SC = "Tracks/MidiTrack[1]/DeviceChain/MainSequencer/ClipSlotList/ClipSlot[1]/ClipSlot/Value/MidiClip"
SA = "Tracks/AudioTrack[1]/DeviceChain/MainSequencer/ClipSlotList/ClipSlot[1]/ClipSlot/Value/AudioClip"
AR = "Tracks/MidiTrack[1]/DeviceChain/MainSequencer/ClipTimeable/ArrangerAutomation/Events/MidiClip[1]"
SN = "Scenes/Scene[1]"
FA = ["FollowTime", "IsLinked", "LoopIterations", "FollowActionA", "FollowActionB",
      "FollowChanceA", "FollowChanceB", "JumpIndexA", "JumpIndexB", "FollowActionEnabled"]
KIND = {"Legato": "b", "IsLinked": "b", "FollowActionEnabled": "b", "VelocityAmount": "f",
        "FollowChanceA": "f", "FollowChanceB": "f", "JumpIndexA": "f", "JumpIndexB": "f", "FollowTime": "d",
        "LaunchMode": "i", "LaunchQuantisation": "i", "LoopIterations": "i", "FollowActionA": "i",
        "FollowActionB": "i", "GlobalQuantisation": "i", "AutoQuantisation": "i"}
NEW_FA = dict(FollowTime=4.0, IsLinked=True, LoopIterations=1, FollowActionA=4, FollowActionB=0,
              FollowChanceA=100.0, FollowChanceB=0.0, JumpIndexA=1.0, JumpIndexB=1.0, FollowActionEnabled=False)


class Refused(Exception):
    pass


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def text_value(kind, t):
    if kind == "b":
        if t in ("true", "1"):
            return True
        if t in ("false", "0"):
            return False
        raise Refused(t)
    if kind == "i":
        m = re.fullmatch(r" *\+?([0-9]{1,9})|([0-9]{1,9}) +", t)
        if not m:
            raise Refused(t)
        return int(m.group(1) or m.group(2))
    m = re.match(r" *([+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][+-]?[0-9]+)?)", t)
    if not m:
        raise Refused(t)
    v = float(m.group(1))  # Python float() is correctly rounded, ties to even
    return f32(v) if kind == "f" else v


def child(el, name):
    found = [c for c in el if c.tag == name]
    return found


def val(el, name):
    c = child(el, name)
    return None if not c else text_value(KIND[name], c[0].get("Value"))


def leaf(parent, name, text):
    ET.SubElement(parent, name, Value=text)


def convert_clip(clip, c):
    if c < 406:  # move the five old clip children into a new FollowAction; FollowTime 1 when absent
        moved = {n: child(clip, n) for n in ("FollowTime", "FollowActionA", "FollowActionB", "FollowChanceA", "FollowChanceB")}
        fa = ET.SubElement(clip, "FollowAction")
        for n, els in moved.items():
            for e in els:
                clip.remove(e)
            leaf(fa, n, els[0].get("Value") if els else "1")
    for fa in child(clip, "FollowAction"):
        if c < 417 and not child(fa, "FollowActionEnabled"):
            on = (val(fa, "FollowActionA") or 0) != 0 and (val(fa, "FollowChanceA") or 0) != 0 \
                or (val(fa, "FollowActionB") or 0) != 0 and (val(fa, "FollowChanceB") or 0) != 0
            leaf(fa, "FollowActionEnabled", "true" if on else "false")
        if c < 421:
            linked = (not val(fa, "FollowActionEnabled") and val(fa, "FollowActionA") == 0
                      and val(fa, "FollowActionB") == 0 and val(fa, "FollowTime") == 4.0)
            if linked:
                child(fa, "FollowActionA")[0].set("Value", "4")
            leaf(fa, "IsLinked", "true" if linked else "false")


def convert_scene(scene, c):
    if c >= 12203:
        return
    fas = child(scene, "FollowAction")
    if not fas:
        fa = ET.SubElement(scene, "FollowAction")
        for n, t in [("FollowTime", "4"), ("LoopIterations", "1"), ("FollowActionA", "0"), ("FollowActionB", "0"),
                     ("FollowChanceA", "100"), ("FollowChanceB", "0"), ("FollowActionEnabled", "false"),
                     ("JumpIndexA", "1"), ("JumpIndexB", "1"), ("IsLinked", "true")]:
            leaf(fa, n, t)
        return
    fa = fas[0]
    linked = (not val(fa, "FollowActionEnabled") and val(fa, "FollowTime") == 4.0 and val(fa, "FollowActionA") == 4
              and val(fa, "FollowActionB") == 0 and val(fa, "FollowChanceA") == 100.0 and val(fa, "FollowChanceB") == 0.0)
    for e in child(fa, "IsLinked"):
        fa.remove(e)
    leaf(fa, "IsLinked", "true" if linked else "false")


def half_away(x):
    q = Fraction(x)
    m = int(abs(q) + Fraction(1, 2))  # floor(|q| + 1/2)
    return m if q >= 0 else -m


def read_fa(el):
    v = dict(NEW_FA)
    for n in FA:
        x = None if el is None else val(el, n)
        if x is not None:
            v[n] = x
    a, b = v["FollowChanceA"], v["FollowChanceB"]
    if a == 0 and b == 0:
        v["FollowChanceA"], v["FollowActionEnabled"] = 100.0, False
    else:
        s = f32(f32(a + b) / 100.0)
        q = f32(a / s)
        v["FollowChanceA"] = float(half_away(q))
        v["FollowChanceB"] = f32(100.0 - v["FollowChanceA"])
    m = half_away(Fraction(v["FollowTime"]) * N)
    v["FollowTime"] = float(Fraction(m, N))  # Fraction -> float is correctly rounded
    return v


def open_doc(text):
    root = ET.fromstring(text)
    c = int(root.get("MinorVersion").split("_")[1])
    live = root.find("LiveSet")
    held = {}
    try:
        for p in (SC, SA, AR):
            clip = live.find(p)
            if clip is None:
                continue
            for n in ("LaunchMode", "LaunchQuantisation", "Legato", "VelocityAmount", "FollowAction"):
                if len(child(clip, n)) > 1:
                    raise Refused("duplicate " + n)
            convert_clip(clip, c)
            held[f"{p}/LaunchMode"] = val(clip, "LaunchMode")
            held[f"{p}/LaunchQuantisation"] = val(clip, "LaunchQuantisation")
            lg, va = val(clip, "Legato"), val(clip, "VelocityAmount")
            held[f"{p}/Legato"] = False if lg is None else lg
            held[f"{p}/VelocityAmount"] = 0.0 if va is None else va
            fa = child(clip, "FollowAction")
            held.update({f"{p}/FollowAction/{k}": x for k, x in read_fa(fa[0] if fa else None).items()})
        scene = live.find(SN)
        if scene is not None:
            convert_scene(scene, c)
            held.update({f"{SN}/FollowAction/{k}": x for k, x in read_fa(child(scene, "FollowAction")[0]).items()})
        for n in ("GlobalQuantisation", "AutoQuantisation"):
            held[n] = val(live, n)
    except Refused:
        return "refused", {}
    return "opens", held


def same(a, b):
    return type(a) is type(b) and a == b


def short(v):
    return isinstance(v, bool) or len(Decimal(v).normalize().as_tuple().digits) <= 6


def main(pkg):
    cases = json.loads((pkg / "cases.json").read_text())["cases"]
    bad = 0
    for cs in cases:
        e = cs["expected"]
        outcome, held = open_doc((pkg / cs["input"]).read_text())
        errs = [] if outcome == e["outcome"] else [f"outcome {outcome}"]
        for k, v in {**e.get("values", {}), **e.get("saved", {}).get("values", {})}.items():
            if not same(held.get(k), v):
                errs.append(f"{k.split('/')[-1]} model={held.get(k)!r} case={v!r}")
        for k, v in e.get("saved", {}).get("values", {}).items():
            if not short(v):
                errs.append(f"saved {k.split('/')[-1]}={v!r} needs more than six digits")
        bad += bool(errs)
        print(cs["id"], "agree" if not errs else "DISAGREE " + "; ".join(errs))
    print(f"{len(cases) - bad}/{len(cases)} cases agree with the reviewer model")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
