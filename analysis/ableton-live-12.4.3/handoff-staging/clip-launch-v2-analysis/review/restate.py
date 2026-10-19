"""Reviewer's own executable restatement of the clip-launch-v2 contract (analyst side; never shipped).

Written from the staged spec.md text, not from the author's model_v2.py or build_clip.py.
usage: python3 -I -B restate.py <package dir> [--mutate]
Document cases: conversion (REQ-014), reading rules, duplicate refusal, initial values (REQ-009),
chance rescaling with the 0-100 limit (REQ-012), follow-time formula (REQ-013); saved values are the
held values, saved.absent and clip_order are checked on a modelled save. Value cases: G, clip grid,
L and B in binary64. --mutate perturbs every expected value once and counts detections.
"""
import copy, json, math, re, struct, sys
import xml.etree.ElementTree as ET
from pathlib import Path

N = 3843840
H = 1 / N
SC = "Tracks/MidiTrack[1]/DeviceChain/MainSequencer/ClipSlotList/ClipSlot[1]/ClipSlot/Value/MidiClip"
SA = "Tracks/AudioTrack[1]/DeviceChain/MainSequencer/ClipSlotList/ClipSlot[1]/ClipSlot/Value/AudioClip"
AR = "Tracks/MidiTrack[1]/DeviceChain/MainSequencer/ClipTimeable/ArrangerAutomation/Events/MidiClip[1]"
SN = "Scenes/Scene[1]"
LAUNCH = ["LaunchMode", "LaunchQuantisation", "Legato", "VelocityAmount", "FollowAction"]
FA = ["FollowTime", "IsLinked", "LoopIterations", "FollowActionA", "FollowActionB", "FollowChanceA",
      "FollowChanceB", "JumpIndexA", "JumpIndexB", "FollowActionEnabled"]
OLD = ["FollowTime", "FollowActionA", "FollowActionB", "FollowChanceA", "FollowChanceB"]
TYPE = {"LaunchMode": "i", "LaunchQuantisation": "i", "Legato": "b", "VelocityAmount": "f", "FollowTime": "d",
        "IsLinked": "b", "LoopIterations": "i", "FollowActionA": "i", "FollowActionB": "i", "FollowChanceA": "f",
        "FollowChanceB": "f", "JumpIndexA": "f", "JumpIndexB": "f", "FollowActionEnabled": "b",
        "GlobalQuantisation": "i", "AutoQuantisation": "i"}
INIT_CLIP = {"Legato": False, "VelocityAmount": 0.0}
INIT_FA = {"FollowTime": 4.0, "IsLinked": True, "LoopIterations": 1, "FollowActionA": 4, "FollowActionB": 0,
           "FollowChanceA": 100.0, "FollowChanceB": 0.0, "JumpIndexA": 1.0, "JumpIndexB": 1.0,
           "FollowActionEnabled": False}


class Refused(Exception):
    pass


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def bits(x):
    return struct.unpack("<Q", struct.pack("<d", float(x)))[0]


def read(kind, t):
    """Reading rules of spec.md 'Reading rules for value text' (inputs in the release's ranges)."""
    if kind == "b":
        if t in ("true", "1"):
            return True
        if t in ("false", "0"):
            return False
        raise Refused(f"Boolean {t!r}")
    if kind == "i":
        m = re.fullmatch(r" *\+?([0-9]{1,9})", t) or re.fullmatch(r"([0-9]+) +", t)
        if not m or len(t) > 63 and not t.endswith(" "):
            raise Refused(f"integer {t!r}")
        return int(m.group(1))
    m = re.match(r" *([+-]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)", t)
    if not m:
        raise Refused(f"number {t!r}")
    v = float(m.group(1))                       # correctly rounded, ties to even
    return f32(v) if kind == "f" else v


def kids(el, name):
    return [c for c in el if c.tag == name]


def value(el, name):
    k = kids(el, name)
    return None if not k else read(TYPE[name], k[0].get("Value"))


def add(parent, name, text):
    ET.SubElement(parent, name, Value=text)


def convert_clip(clip, c):
    """REQ-014 steps 406, 417, 421 (applied when the step number is above c)."""
    if c < 406:
        fa = ET.SubElement(clip, "FollowAction")
        for n in OLD:
            k = kids(clip, n)
            add(fa, n, k[0].get("Value") if k else "1")   # absent FollowTime becomes 1; others excluded
            for e in k:
                clip.remove(e)
    fa = kids(clip, "FollowAction")[0] if kids(clip, "FollowAction") else None
    if fa is None:
        return
    if c < 417 and not kids(fa, "FollowActionEnabled"):
        A, B = value(fa, "FollowActionA"), value(fa, "FollowActionB")
        ca, cb = value(fa, "FollowChanceA"), value(fa, "FollowChanceB")
        add(fa, "FollowActionEnabled", "true" if (A != 0 and ca != 0) or (B != 0 and cb != 0) else "false")
    if c < 421:
        on = (value(fa, "FollowActionEnabled") is False and value(fa, "FollowActionA") == 0
              and value(fa, "FollowActionB") == 0 and value(fa, "FollowTime") == 4.0)
        if on:
            kids(fa, "FollowActionA")[0].set("Value", "4")
        add(fa, "IsLinked", "true" if on else "false")


def convert_scene(scene, c):
    if c >= 12203:
        return
    fa = kids(scene, "FollowAction")
    if not fa:
        f = ET.SubElement(scene, "FollowAction")
        for n, t in (("FollowTime", "4"), ("LoopIterations", "1"), ("FollowActionA", "0"), ("FollowActionB", "0"),
                     ("FollowChanceA", "100"), ("FollowChanceB", "0"), ("FollowActionEnabled", "false"),
                     ("JumpIndexA", "1"), ("JumpIndexB", "1"), ("IsLinked", "true")):
            add(f, n, t)
        return
    f = fa[0]
    on = (value(f, "FollowActionEnabled") is False and value(f, "FollowTime") == 4.0 and value(f, "FollowActionA") == 4
          and value(f, "FollowActionB") == 0 and value(f, "FollowChanceA") == 100.0 and value(f, "FollowChanceB") == 0.0)
    for e in kids(f, "IsLinked"):
        f.remove(e)
    add(f, "IsLinked", "true" if on else "false")


def round_half_away(q):
    return math.floor(abs(q) + 0.5) * (1 if q >= 0 else -1)   # q is binary32; |q| + 0.5 exact in binary64


def L(x):
    """REQ-013 formula, binary64, round to nearest even."""
    t1 = x + H * 0.5
    t2 = t1 * N
    return math.floor(t2) / N


def read_follow(fa, corrections=True):
    v = dict(INIT_FA)
    if fa is not None:
        for n in FA:
            x = value(fa, n)
            if x is not None:
                v[n] = x
    if not corrections:
        return v
    a, b = v["FollowChanceA"], v["FollowChanceB"]
    if a == 0 and b == 0:                                  # -0 == 0
        v["FollowChanceA"], v["FollowActionEnabled"] = 100.0, False
    else:
        s = f32(f32(a + b) / 100.0)
        q = f32(a / s)
        ra = float(round_half_away(q))
        rb = f32(100.0 - ra)
        v["FollowChanceA"], v["FollowChanceB"] = min(max(ra, 0.0), 100.0), min(max(rb, 0.0), 100.0)
    v["FollowTime"] = L(v["FollowTime"])
    return v


def open_doc(text):
    root = ET.fromstring(text)
    c = int(root.get("MinorVersion").split("_")[1])
    ls = root.find("LiveSet")
    held, saved = {}, {}
    try:
        for p in (SC, SA, AR):
            clip = ls.find(p)
            if clip is None:
                continue
            for n in LAUNCH:
                if len(kids(clip, n)) > 1:
                    raise Refused("repeated " + n)
            convert_clip(clip, c)
            for n in ("LaunchMode", "LaunchQuantisation"):
                held[f"{p}/{n}"] = value(clip, n)
            for n, d in INIT_CLIP.items():
                x = value(clip, n)
                held[f"{p}/{n}"] = d if x is None else x
            fa = kids(clip, "FollowAction")
            for n, x in read_follow(fa[0] if fa else None).items():
                held[f"{p}/FollowAction/{n}"] = x
            saved[p] = [n for n in [c2.tag for c2 in clip] if n in LAUNCH or n in OLD]
        scene = ls.find(SN)
        if scene is not None:
            convert_scene(scene, c)
            for n, x in read_follow(kids(scene, "FollowAction")[0], corrections=False).items():
                held[f"{SN}/FollowAction/{n}"] = x
        for n in ("GlobalQuantisation", "AutoQuantisation"):
            held[n] = value(ls, n)
    except Refused:
        return "refused", {}, {}
    return "opens", held, saved


def saved_doc_paths(held):
    """Modelled save: each clip's five launch elements once, FollowAction with exactly its ten children."""
    paths = set()
    for k in held:
        for p in (SC, SA, AR):
            if k.startswith(p + "/"):
                paths.update({f"{p}/{n}" for n in LAUNCH} | {f"{p}/FollowAction/{n}" for n in FA})
    return paths


def eq(a, b):
    if isinstance(b, bool) or isinstance(a, bool):
        return a is b
    return a is not None and float(a) == float(b)      # equality does not distinguish -0


def G(q, n, d):
    bar = 4 * n / d
    return {1: 8 * bar, 2: 4 * bar, 3: 2 * bar, 4: bar, 5: 2.0, 6: 4 / 3, 7: 1.0, 8: 2 / 3, 9: 0.5, 10: 1 / 3,
            11: 0.25, 12: 1 / 6, 13: 0.125}.get(q, 0.0)


def compute(fn, a):
    if fn == "grid-length":
        return {"grid": G(a["q"], *a["time_signature"])}
    if fn == "clip-grid":
        k = 0 if a["clip_value"] == -99 else a["clip_value"]
        return {"grid": G(a["global_value"], *a["song_time_signature"]) if k == 0
                else G(k - 1, *a["clip_time_signature"])}
    p, g = L(a["beat"]), a["grid"]
    if g == 0:
        return {"rounded_beat": p, "boundary": p}
    a2 = max(0.0, a["anchor"])
    return {"rounded_beat": p, "boundary": L(a2 + math.ceil((p - a2) / g) * g)}


def judge(case, pkg):
    e = case["expected"]
    errs = []
    if case["action"] == "compute":
        for comp in e["computations"]:
            m = compute(comp["function"], comp["arguments"])
            if set(m) != set(comp["result"]) or any(bits(m[k]) != bits(comp["result"][k]) for k in m):
                errs.append(f"{comp['function']} {comp['arguments']} model {m} case {comp['result']}")
        return errs
    outcome, held, saved = open_doc((pkg / case["input"]).read_text())
    if outcome != e["outcome"]:
        return [f"outcome {outcome}"]
    for part in (e.get("values", {}), e.get("saved", {}).get("values", {})):
        for k, v in part.items():
            if not eq(held.get(k), v):
                errs.append(f"{k.rsplit('/', 2)[-2:]} model {held.get(k)!r} case {v!r}")
    sp = saved_doc_paths(held)
    for k in e.get("saved", {}).get("absent", []):
        if k in sp:
            errs.append(f"absent {k} would be written")
    co = e.get("saved", {}).get("clip_order")
    if co and co not in saved:
        errs.append(f"clip_order {co} not a clip")
    return errs


def mutate(case):
    """Perturb each judged value once; yield mutated copies."""
    e = case["expected"]
    if case["action"] == "compute":
        for i, comp in enumerate(e["computations"]):
            for k, v in comp["result"].items():
                m = copy.deepcopy(case)
                m["expected"]["computations"][i]["result"][k] = math.nextafter(v, math.inf) if v else 1.0
                yield m
        return
    if e["outcome"] == "refused":
        m = copy.deepcopy(case)
        m["expected"]["outcome"] = "opens"
        yield m
        return
    for part in ("values", "saved"):
        d = e.get("values", {}) if part == "values" else e.get("saved", {}).get("values", {})
        for k, v in d.items():
            m = copy.deepcopy(case)
            t = m["expected"]["values"] if part == "values" else m["expected"]["saved"]["values"]
            t[k] = (not v) if isinstance(v, bool) else v + 1
            yield m


def main(pkg, mut):
    cases = json.loads((pkg / "cases.json").read_text())["cases"]
    bad = 0
    for c in cases:
        errs = judge(c, pkg)
        bad += bool(errs)
        print(c["id"], "agree" if not errs else "DISAGREE " + "; ".join(errs))
    print(f"{len(cases) - bad}/{len(cases)} cases agree with the reviewer restatement")
    if mut:
        total = det = 0
        for c in cases:
            for m in mutate(c):
                total += 1
                det += bool(judge(m, pkg))
        print(f"mutations detected: {det}/{total}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), "--mutate" in sys.argv)
