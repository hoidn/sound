"""Reviewer's independent restatement of the automation-envelopes-v1 contract (spec.md), plus fixture checks.

Written by the handoff reviewer from the contract text alone; it does not import the author's model.
Run: python3 -I reviewer_model.py <package dir>   (prints JSON; exit 1 on any disagreement)

Checks per case: outcome and saved text from the restated clauses; per fixture: the template skeleton,
target resolution, time order, required attributes, unique event Ids, ranges and kind (no Q-020-class input),
ASCII/LF, and no shipped content markers.
"""
import json, re, struct, sys
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

L = -63072000.0
KIND = {"21": ("Speaker", "BoolEvent"), "22": ("Pan", "FloatEvent"), "23": ("CrossFadeState", "EnumEvent"),
        "31": ("ControllerTargets.6", "FloatEvent")}
RANGE = {"Pan": (-1, 1), "ControllerTargets.6": (0, 127), "CrossFadeState": (0, 2)}
CC = ["CurveControl1X", "CurveControl1Y", "CurveControl2X", "CurveControl2Y"]


class NoExpectation(Exception):
    pass


class Refused(Exception):
    pass


def read_double(text):  # REQ-012 rule 1
    t = text.lstrip(" ")
    if re.match(r"[+-]?(0[xX]|inf|nan)", t, re.I) or t.startswith("#") or t == "Invalid" or text[:1] in "\t\n\r":
        raise NoExpectation(f"excluded text form {text!r}")
    m = re.match(r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?", t)
    if not m:
        raise Refused(f"no decimal prefix in {text!r}")
    return float(m.group(0))


def to32(x):
    return struct.unpack("f", struct.pack("f", x))[0]


def read_bool(text):  # rule 3
    if text in ("true", "1"):
        return True
    if text in ("false", "0"):
        return False
    raise Refused(f"bool text {text!r}")


def read_int(text):  # rule 4, accepted forms and the refusals the cases use
    if re.fullmatch(r" *\+?[0-9]+", text) or re.fullmatch(r"[0-9]+ +", text):
        return int(text.strip())
    if re.fullmatch(r" *[+-]?[0-9]+ *", text):
        raise NoExpectation(f"excluded integer form {text!r}")
    raise Refused(f"integer text {text!r}")


def fmt(x, p):  # rule 7
    if x == 0 and str(x) == "0.0":
        return "0"
    if x == 0:
        raise NoExpectation("saved negative zero")
    d = Decimal(x)
    a = abs(d)
    e = a.adjusted()
    k = (e if a == Decimal(10) ** e else e + 1) if a >= 1 else e
    s = format(d.quantize(Decimal(1).scaleb(-max(0, p - k)), rounding=ROUND_HALF_EVEN), "f")
    return s.rstrip("0").rstrip(".") if "." in s else s


def K(c1, c2):  # REQ-009 sufficient condition
    return 0 <= c1 <= 1 and 0 <= c2 <= 1 and (c1 <= c2 or c1 * c1 + c2 * c2 - c1 * c2 - c1 <= -1e-6)


def envelopes(root):
    ls = root.find("LiveSet")
    track = ls.find("Tracks/AudioTrack/AutomationEnvelopes/Envelopes")
    clip = ls.find("Tracks/MidiTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/MidiClip/Envelopes/Envelopes")
    return [("track", e) for e in track] + [("clip", e) for e in clip]


def read_events(env):
    """Returns parsed events; raises Refused for one broken rule, NoExpectation for excluded input."""
    out = []
    for ev in env.find("Automation/Events"):
        a = ev.attrib
        cls = ev.tag
        t = read_double(a["Time"])
        if cls == "FloatEvent":
            v = to32(read_double(a["Value"]))
            ctl = {c: read_double(a[c]) if c in a else 0.5 for c in CC}
        elif cls == "BoolEvent":
            v, ctl = read_bool(a["Value"]), None
        else:
            v, ctl = read_int(a["Value"]), None
        out.append((cls, t, v, ctl))
    return out


def model(raw, action):
    root = ET.fromstring(raw)
    refusals, saved = [], {}
    for where, env in envelopes(root):
        target, _ = KIND[env.find("EnvelopeTarget/PointeeId").get("Value")]
        try:
            evs = read_events(env)
        except Refused as r:
            refusals.append(str(r))
            continue
        if not evs:
            refusals.append("empty list")
            continue
        if evs[0][1] not in (L, 0.0):
            refusals.append("first time")
            continue
        rows = []
        for i, (cls, t, v, ctl) in enumerate(evs if action == "open-save" else []):
            row = {"Time": fmt(t, 17)}
            if cls == "FloatEvent":
                row["Value"] = fmt(float(v), 9)
                curved = any(ctl[c] != 0.5 for c in CC)
                if curved:
                    ok_pos = 0 < i < len(evs) - 1 and evs[i + 1][1] > t and evs[i + 1][2] != v
                    if not ok_pos or not (K(ctl["CurveControl1X"], ctl["CurveControl2X"]) and
                                          K(ctl["CurveControl1Y"], ctl["CurveControl2Y"])):
                        raise NoExpectation("controls outside the released conditions")
                    row.update({c: fmt(ctl[c], 17) for c in CC if ctl[c] != 0.5})
            elif cls == "BoolEvent":
                row["Value"] = "true" if v else "false"
            else:
                row["Value"] = str(v)
            rows.append({"element": cls, "attributes": row})
        if where == "track":
            saved[target] = rows
    if len(refusals) > 1:
        raise NoExpectation("more than one broken rule")
    if refusals:
        return {"outcome": "refused"}
    if action == "open":
        return {"outcome": "opens"}
    if action == "open-save":
        return {"outcome": "opens", "saved": {"envelopes": [{"target": k, "events": v} for k, v in saved.items()]}}
    raise NoExpectation(f"action {action} has no released expectation")


def same_saved(got, exp):
    g = {e["target"]: e["events"] for e in got["saved"]["envelopes"]}
    x = {e["target"]: e["events"] for e in exp["saved"]["envelopes"]}
    return g == x


def fixture_checks(raw):
    """Flags any Q-020-class or otherwise excluded input, and shipped-content markers."""
    issues = []
    if not raw.isascii() or b"\r" in raw or not raw.endswith(b"\n"):
        issues.append("not ASCII/LF/final newline")
    root = ET.fromstring(raw)
    if root.tag != "Ableton" or root.attrib != {"MajorVersion": "5", "MinorVersion": "12.0_12402", "SchemaChangeCount": "1"}:
        issues.append("root attributes")
    ids = {}
    for el in root.iter():
        if "Id" in el.attrib and el.tag in ("AutomationTarget", "ControllerTargets.6"):
            ids.setdefault(el.get("Id"), []).append(el.tag)
    if sorted(ids) != ["21", "22", "23", "31"] or any(len(v) != 1 for v in ids.values()):
        issues.append(f"target Ids {ids}")
    nxt = int(root.find("LiveSet/NextPointeeId").get("Value"))
    if max(int(i) for i in ids) >= nxt:
        issues.append("target Id not below NextPointeeId")
    if any(lk.get("Value") != "0" for lk in root.iter("LockEnvelope")):
        issues.append("LockEnvelope")
    named = []
    for where, env in envelopes(root):
        pid = env.find("EnvelopeTarget/PointeeId").get("Value")
        named.append(pid)
        if pid not in KIND or (where == "clip") != (pid == "31"):
            issues.append(f"dangling or out-of-relation PointeeId {pid}")
            continue
        target, cls = KIND[pid]
        st = env.find("Automation/AutomationTransformViewState")
        if st.find("IsTransformPending").get("Value") != "false" or len(st.find("TimeAndValueTransforms")):
            issues.append("stored transform")
        evs = list(env.find("Automation/Events"))
        eids = [e.get("Id") for e in evs]
        if None in eids or len(set(eids)) != len(eids):
            issues.append("missing or repeated event Id")
        times = []
        for e in evs:
            if e.tag != cls:
                issues.append("event class does not match target kind")
            if "Time" not in e.attrib or "Value" not in e.attrib:
                issues.append("event without Time or Value")
                continue
            try:
                times.append(read_double(e.get("Time")))
                if target in RANGE:
                    v = read_double(e.get("Value")) if cls == "FloatEvent" else read_int(e.get("Value"))
                    lo, hi = RANGE[target]
                    if not lo <= v <= hi:
                        issues.append("value out of range")
            except (Refused, NoExpectation):
                pass  # the case's single refused text; judged by the model
        if times != sorted(times):
            issues.append("events in time disorder")
        if any(times.count(t) > 2 for t in times):
            issues.append("three or more events at one time")
        if any(t < L or t >= 1_000_000 for t in times):
            issues.append("time outside the released range")
    if len(named) != len(set(named)):
        issues.append("two envelopes name one target")
    text = raw.decode("ascii", "replace")
    for marker in ("Creator", "Revision", "Sample", "FileRef", "Path", "Ableton Live 1", ".als", ".wav", "Core Library"):
        if marker in text:
            issues.append(f"marker {marker}")
    return issues


def skeleton(raw):
    """The fixture with every envelope list emptied; must equal the template's skeleton for all fixtures."""
    root = ET.fromstring(raw)
    ls = root.find("LiveSet")
    for path in ("Tracks/AudioTrack/AutomationEnvelopes/Envelopes",
                 "Tracks/MidiTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/MidiClip/Envelopes/Envelopes"):
        el = ls.find(path)
        for c in list(el):
            el.remove(c)
        el.text = None
    for el in root.iter():
        el.tail = None
        if not len(el):
            el.text = None
    return ET.tostring(root)


def main(d):
    d = Path(d)
    cases = json.loads((d / "cases.json").read_text())["cases"]
    report, bad = {}, False
    skel = None
    for c in cases:
        raw = (d / c["input"]).read_bytes()
        row = {"fixture_issues": fixture_checks(raw)}
        sk = skeleton(raw)
        skel = skel or sk
        row["skeleton_equals_first"] = sk == skel
        try:
            got = model(raw, c["action"])
            exp = c["expected"]
            ok = got["outcome"] == exp["outcome"] and set(got) == set(exp) and ("saved" not in exp or same_saved(got, exp))
            row["model"] = "agrees" if ok else f"DISAGREES: {got}"
        except NoExpectation as e:
            row["model"] = f"NO EXPECTATION: {e}"
        bad |= row["model"] != "agrees" or bool(row["fixture_issues"]) or not row["skeleton_equals_first"]
        report[c["id"]] = row
    hashes = {}
    for c in cases:
        hashes.setdefault((d / c["input"]).read_bytes(), []).append(c["id"])
    report["_identical_inputs"] = [v for v in hashes.values() if len(v) > 1]
    report["_fmt_examples"] = {"L": fmt(L, 17), "4": fmt(4.0, 17), "Value 0.3": fmt(float(to32(0.3)), 9),
                               "Time 0.3": fmt(0.3, 17), "0.8": fmt(0.8, 17), "0.2": fmt(0.2, 17), "1 (P=9)": fmt(1.0, 9)}
    print(json.dumps(report, indent=1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
