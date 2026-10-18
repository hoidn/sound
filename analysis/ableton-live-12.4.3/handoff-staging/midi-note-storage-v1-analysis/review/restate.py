"""Reviewer's executable restatement of the midi-note-storage-v1 clauses (analyst-side; not payload).

Written by the reviewer from the release contract (spec.md), not from the author's mns_model.py.
It reads each fixture, applies the released clauses and compares outcome and saved notes with
cases.json. Inputs the contract gives no expectation raise NoExpectation. It also checks that each
fixture is the carrier (root, path, Loop) holding the base notes with keys 36 and 38 only.
usage: python3 -I restate.py <package dir>
"""
import json, math, re, struct, sys, zlib
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

DMAX = sys.float_info.max
G = 3843840.0
H = 1 / G  # binary64 nearest to 1/3,843,840
ROOT = {"MajorVersion": "5", "MinorVersion": "12.0_12402", "SchemaChangeCount": "1",
        "Creator": "Ableton Live 12.4.3"}
PATH = "LiveSet/Tracks/MidiTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/MidiClip"
NOTE_ORDER = ["Time", "Duration", "Velocity", "VelocityDeviation", "OffVelocity", "Probability", "IsEnabled",
              "NoteId"]
EVENT_ATTRS = {"TimeOffset", "Value", "CurveControl1X", "CurveControl1Y", "CurveControl2X", "CurveControl2Y"}
CHILDREN = ["KeyTracks", "PerNoteEventStore", "NoteProbabilityGroups", "ProbabilityGroupIdGenerator",
            "NoteIdGenerator"]


class Refused(Exception):
    pass


class NoExpectation(Exception):
    pass


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


# REQ-002 clause 3: decimal prefix after leading U+0020; Invalid only where expectations exist.
NUM = re.compile(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?")


def num(text, invalid_ok):
    if text == "Invalid":
        if not invalid_ok:
            raise NoExpectation("Invalid outside Duration/TimeOffset")
        return DMAX
    s = text.lstrip(" ")
    if s[:1] in "\t\n\r\f\v" and s:
        raise NoExpectation("non-space leading whitespace")
    body = s.lstrip("+-")
    if s.startswith("#") or body[:2].lower() == "0x" or body[:3].lower() in ("inf", "nan"):
        raise NoExpectation("excluded number form")
    m = NUM.match(s)
    if not m:
        raise Refused("no numeric prefix")
    x = float(m.group(0))
    if x == 0 and math.copysign(1, x) < 0:
        raise NoExpectation("negative zero read")
    if abs(x) >= 1e6:
        raise NoExpectation("magnitude >= 1e6")
    return x


def boolean(text):
    if text in ("true", "1"):
        return True
    if text in ("false", "0"):
        return False
    raise Refused("bool text")


def int64(text):  # REQ-002 clause 6
    if re.fullmatch(r" *\+?[0-9]+", text) or re.fullmatch(r"[0-9]+ *", text):
        digits = text.strip(" ").lstrip("+")
        if len(digits) > 63 or int(digits) > 2 ** 63 - 1:
            raise Refused("integer length or range")
        v = int(digits)
        if v > 1_000_000:
            raise NoExpectation("integer above 1,000,000")
        return v
    if re.fullmatch(r" *\+?[0-9]+ +", text) and (text[0] == " " or text.lstrip(" ")[0] == "+"):
        raise NoExpectation("spaces on both sides or + with trailing spaces")
    i = text.find("-")
    if i >= 0 and not text[:i].rstrip(" ").endswith("+"):
        raise NoExpectation("minus sign")
    raise Refused("integer text")


def plain(text, minus=False):  # REQ-002 clause 7
    if not re.fullmatch((r"-?" if minus else "") + r"(0|[1-9][0-9]*)", text):
        raise NoExpectation("not plain decimal")
    return int(text)


def grid(x):  # REQ-006
    if x == DMAX:
        return x
    s = 1.0 if x >= 0 else -1.0
    r = s * (math.floor(abs(x + s * H / 2) * G) / G)
    if r == 0 and math.copysign(1, r) < 0:
        raise NoExpectation("negative zero produced")
    return r


def text_num(x, p):  # REQ-016 clause 3
    if x == 0:
        if math.copysign(1, x) < 0:
            raise NoExpectation("negative zero")
        return "0"
    d = Decimal(x).copy_abs()
    lg = math.log10(abs(x))
    if abs(lg - round(lg)) < 1e-12 and d != Decimal(10) ** round(lg):
        raise NoExpectation("log10 near integer")
    if d >= 1:
        k = len(str(int(d))) - (1 if d == Decimal(10) ** (len(str(int(d))) - 1) else 0)
    else:
        k = math.floor(lg) if d != Decimal(10) ** round(lg) else round(lg)
    q = Decimal(x).quantize(Decimal(1).scaleb(-max(0, p - k)), rounding=ROUND_HALF_EVEN)
    t = format(q, "f")
    return t.rstrip("0").rstrip(".") if "." in t else t


def read_note(el):
    a = dict(el.attrib)
    unknown = set(a) - set(NOTE_ORDER)
    if unknown:
        raise NoExpectation("unknown note attribute")
    n = {"VelocityDeviation": 0.0, "Probability": 1.0, "IsEnabled": True}  # REQ-003
    for k in ("Time", "Duration", "Velocity", "OffVelocity"):
        if k not in a:
            raise NoExpectation("missing note attribute " + k)
    n["Time"] = num(a["Time"], False)
    n["Duration"] = num(a["Duration"], True)
    for k in ("Velocity", "OffVelocity", "VelocityDeviation", "Probability"):
        if k in a:
            n[k] = f32(num(a[k], False))
    if "IsEnabled" in a:
        n["IsEnabled"] = boolean(a["IsEnabled"])
    n["NoteId"] = int64(a["NoteId"]) if "NoteId" in a else None
    # REQ-005 limits, then REQ-006 grid
    v = n["Velocity"]; n["Velocity"] = 1.0 if v < 1 else 127.0 if v > 127 else v
    for k, hi in (("OffVelocity", 127.0), ("Probability", 1.0)):
        v = n[k]; n[k] = 0.0 if v < 0 else hi if v > hi else v
    if n["Duration"] < 0 or n["Duration"] == DMAX:
        n["Duration"] = 0.0
    n["Time"], n["Duration"] = grid(n["Time"]), grid(n["Duration"])
    return n


def saved_note(n):
    out = {"Time": text_num(n["Time"], 17), "Duration": text_num(n["Duration"], 17),
           "Velocity": text_num(n["Velocity"], 9)}
    if n["VelocityDeviation"] != 0:
        out["VelocityDeviation"] = text_num(n["VelocityDeviation"], 9)
    out["OffVelocity"] = text_num(n["OffVelocity"], 9)
    if n["Probability"] != 1:
        out["Probability"] = text_num(n["Probability"], 9)
    if not n["IsEnabled"]:
        out["IsEnabled"] = "false"
    out["NoteId"] = str(n["NoteId"])
    return out


def cc_kept(cc):
    return cc in (-2, -1) or 1 <= cc <= 31 or 33 <= cc <= 119


def evaluate(raw):
    doc = zlib.decompress(raw, 31)
    try:
        root = ET.fromstring(doc)
    except ET.ParseError:
        raise Refused("not well-formed XML")
    if root.tag != "Ableton" or any(root.get(k) != v for k, v in ROOT.items()):
        raise NoExpectation("root differs from the carrier")
    clip = root.find(PATH)
    loop = clip.find("Loop")
    assert [c.tag for c in clip] == ["Loop", "Notes"], "clip children"
    assert [(c.tag, c.get("Value")) for c in loop] == [("LoopStart", "0"), ("LoopEnd", "8"), ("LoopOn", "true")]
    notes = clip.find("Notes")
    if [c.tag for c in notes] != CHILDREN:
        raise NoExpectation("structure")
    if len(notes.find("NoteProbabilityGroups")) or notes.find("NoteProbabilityGroups").attrib:
        raise NoExpectation("group content")
    tracks = []
    for kt in notes.find("KeyTracks"):
        if kt.tag != "KeyTrack" or [c.tag for c in kt] != ["Notes", "MidiKey"]:
            raise NoExpectation("key track structure")
        evs = list(kt.find("Notes"))
        if any(e.tag != "MidiNoteEvent" for e in evs):
            raise Refused("non-note element among notes")  # REQ-001 clause 3
        key = plain(kt.find("MidiKey").get("Value"))
        assert key in (36, 38), "only keys 36 and 38 may appear"
        if not evs:
            raise NoExpectation("empty key track")
        tracks.append([key, [read_note(e) for e in evs], kt.get("Id")])
    if [t[0] for t in tracks] != sorted({t[0] for t in tracks}):
        raise NoExpectation("key order or repeated key")
    if len({t[2] for t in tracks}) != len(tracks):
        raise NoExpectation("repeated key track Id")
    allnotes = [n for t in tracks for n in t[1]]
    absent = [n["NoteId"] is None for n in allnotes]
    if any(absent) and not all(absent):
        raise NoExpectation("NoteId absent from some notes")
    for n in allnotes:
        n["NoteId"] = 0 if n["NoteId"] is None else n["NoteId"]
    order_ok = all(a["Time"] < b["Time"] and a["Time"] + a["Duration"] <= b["Time"]
                   for t in tracks for a, b in zip(t[1], t[1][1:]))
    # per-note lists: REQ-013, REQ-014 clauses 1 to 3
    store = list(notes.find("PerNoteEventStore"))
    if [c.tag for c in store] != ["EventLists"]:
        raise NoExpectation("store structure")
    lists, ids = [], []
    for pl in store[0]:
        if set(pl.attrib) != {"Id", "NoteId", "CC"} or [c.tag for c in pl] != ["Events"]:
            raise NoExpectation("list structure")
        ids.append(plain(pl.get("Id")))
        lst = {"NoteId": plain(pl.get("NoteId")), "CC": plain(pl.get("CC"), True), "events": []}
        for ev in pl[0]:
            if ev.tag != "PerNoteEvent" or set(ev.attrib) - EVENT_ATTRS or not {"TimeOffset", "Value"} <= set(ev.attrib):
                raise NoExpectation("event structure")
            e = {"TimeOffset": grid(num(ev.get("TimeOffset"), True)), "Value": f32(num(ev.get("Value"), False))}
            for k in sorted(EVENT_ATTRS - {"TimeOffset", "Value"}):
                e[k] = num(ev.get(k), False) if k in ev.attrib else 0.5
            lst["events"].append(e)
        lists.append(lst)
    if len(set(ids)) != len(ids):
        raise NoExpectation("repeated list Id")
    for lst in lists:
        if cc_kept(lst["CC"]):
            lo, hi = (-8192.0, 8191.0) if lst["CC"] == -2 else (0.0, 127.0)
            kept = [e for e in lst["events"] if e["TimeOffset"] != DMAX]
            for e in kept:
                e["Value"] = lo if e["Value"] < lo else hi if e["Value"] > hi else e["Value"]
            lst["events"] = sorted(kept, key=lambda e: e["TimeOffset"])  # stable
    lists = [l for l in lists if l["NoteId"] != 0 and cc_kept(l["CC"])]
    pairs = [(l["NoteId"], l["CC"]) for l in lists]
    if len(set(pairs)) != len(pairs):
        raise Refused("duplicate NoteId and CC")  # REQ-014 clause 2
    stored = [n["NoteId"] for n in allnotes if n["NoteId"] != 0]
    if len(set(stored)) != len(stored):
        raise Refused("NoteId repeated")  # REQ-008
    nxt = int64(notes.find("NoteIdGenerator").find("NextId").get("Value"))
    nxt = max(nxt, max(stored) + 1 if stored else 1)  # REQ-009 clause 1
    lists = [l for l in lists if l["NoteId"] in stored]  # orphans
    lists = [l for l in lists if l["events"]]  # REQ-014 clause 4
    dur = {n["NoteId"]: n["Duration"] for n in allnotes if n["NoteId"]}
    for l in lists:  # clause 5 applies only strictly inside the note
        if not (l["events"][0]["TimeOffset"] > 0 and l["events"][-1]["TimeOffset"] < dur[l["NoteId"]]):
            raise NoExpectation("list reaches its note's edges")
    for t in tracks:  # REQ-009 clause 2 (stored key order is ascending here)
        for n in t[1]:
            if n["NoteId"] == 0:
                n["NoteId"], nxt = nxt, nxt + 1
    saved = {"key_tracks": [{"midi_key": str(k), "notes": [saved_note(n) for n in ns]} for k, ns, _ in tracks],
             "event_lists": [{"NoteId": str(l["NoteId"]), "CC": str(l["CC"]),
                              "events": [{**{"TimeOffset": text_num(e["TimeOffset"], 17),
                                             "Value": text_num(e["Value"], 9)},
                                          **{k: text_num(e[k], 17) for k in sorted(EVENT_ATTRS - {"TimeOffset", "Value"})
                                             if e[k] != 0.5}} for e in l["events"]]} for l in lists],
             "note_id_next": str(nxt)}
    return saved, order_ok


def judge(case, raw):
    try:
        saved, order_ok = evaluate(raw)
    except Refused as r:
        return ("refused", str(r))
    except NoExpectation as x:
        return ("no-expectation", str(x))
    exp = case["expected"]
    if exp["outcome"] != "loads":
        return ("loads", "expected refused")
    if case["action"] == "open-save":
        if not order_ok:
            return ("no-expectation", "unsorted or overlapping notes saved")
        e = exp["saved_notes"]
        norm = lambda s: {**s, "event_lists": sorted(s["event_lists"], key=lambda l: (l["NoteId"], l["CC"]))}
        if norm(e) != norm(saved) or any(list(n) != [k for k in NOTE_ORDER if k in n]
                                         for t in e["key_tracks"] for n in t["notes"]):
            return ("loads", "saved notes differ: " + json.dumps(saved))
    return ("loads", "")


def main(pkg):
    pkg = Path(pkg)
    cases = json.loads((pkg / "cases.json").read_text())["cases"]
    bad = 0
    for c in cases:
        got, why = judge(c, (pkg / c["input"]).read_bytes())
        ok = got == c["expected"]["outcome"] and (got == "refused" or not why)
        bad += not ok
        print(("ok  " if ok else "BAD ") + c["id"], got, why)
    print(f"{len(cases)} cases, {bad} disagreements")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)
