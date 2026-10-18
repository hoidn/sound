"""Cross-check model for midi-note-storage-v1 (analyst side; never shipped).

An independent restatement of the released clauses (spec.md of the staged package). model(raw)
returns ("refused", None), ("loads", saved_notes) or ("loads", None) when the release judges only
the outcome (unsorted or overlapping notes), and ("no-expectation", reason) for excluded inputs.
judge(case, got) lists disagreements with a case. It restates the same static evidence as the
hand-authored expectations and is not an oracle.
"""
import math, re, struct, zlib
import xml.etree.ElementTree as ET
from fractions import Fraction

GZ_HEADER = bytes.fromhex("1f8b0800000000000213")
CLIP = "LiveSet/Tracks/MidiTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/MidiClip"
CHILDREN = ["KeyTracks", "PerNoteEventStore", "NoteProbabilityGroups", "ProbabilityGroupIdGenerator", "NoteIdGenerator"]
NOTE_ATTRS = {"Time", "Duration", "Velocity", "VelocityDeviation", "OffVelocity", "Probability", "IsEnabled", "NoteId"}
CURVES = ["CurveControl1X", "CurveControl1Y", "CurveControl2X", "CurveControl2Y"]
ENVELOPE = {"MajorVersion": "5", "MinorVersion": "12.0_12402", "SchemaChangeCount": "1",
            "Creator": "Ableton Live 12.4.3", "Revision": "0123456789abcdef0123456789abcdef01234567"}
DMAX = 1.7976931348623157e308
H = 1 / 3843840


class Refused(Exception):
    pass


class Excluded(Exception):
    pass


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def number(text, single=False, invalid_ok=False):
    """REQ-002 clause 3: decimal prefix, nearest binary64 (then binary32); Invalid only where allowed."""
    if text == "Invalid":
        if invalid_ok:
            return DMAX
        raise Excluded("Invalid outside Duration and TimeOffset")
    rest = text.lstrip(" ").lstrip("+-").lower()
    if text.startswith("#") or rest.startswith(("0x", "inf", "nan")) or re.match(r" *[^\S ]", text):
        raise Excluded(f"number form {text!r}")
    m = re.match(r" *([+-]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)", text)
    if not m:
        raise Refused(f"no numeric prefix {text!r}")
    v = f32(float(m.group(1))) if single else float(m.group(1))
    if (v == 0 and math.copysign(1, v) < 0) or not abs(v) < 1e6:
        raise Excluded(f"value {text!r} out of scope")
    return v


def boolean(text):
    if text in ("true", "1", "false", "0"):
        return text in ("true", "1")
    raise Refused(f"Boolean {text!r}")


def integer(text):
    """REQ-002 clause 5 (NoteId and next id)."""
    if re.fullmatch(r" +\+?[0-9]+ +|\+[0-9]+ +", text) or "-" in text.replace("+-", ""):
        raise Excluded(f"integer form {text!r}")
    m = re.fullmatch(r" *\+?([0-9]+)|([0-9]+) +", text) if text.isascii() else None
    if not m:
        raise Refused(f"integer {text!r}")
    digits = m.group(1) or m.group(2)
    if len(digits) > 63 or int(digits) > 2 ** 63 - 1:
        raise Refused(f"integer length or range {text!r}")
    if int(digits) > 1_000_000:
        raise Excluded("integer above 1,000,000")
    return int(digits)


def plain(text, neg=False):
    if not re.fullmatch(r"-?(?:0|[1-9][0-9]*)" if neg else r"0|[1-9][0-9]*", text or ""):
        raise Excluded(f"plain integer {text!r}")
    return int(text)


def grid(x):
    """REQ-006 rounding; the largest finite value is left unchanged."""
    if x == DMAX:
        return x
    s = 1.0 if x >= 0 else -1.0
    r = s * (math.floor(abs(x + s * H * 0.5) * 3843840.0) / 3843840.0)
    if r == 0 and math.copysign(1, r) < 0:
        raise Excluded("rounds to negative zero")
    return r


def fmt(x, p):
    """REQ-016 number text."""
    if x == 0:
        return "0"
    lg = math.log10(abs(x))
    if abs(lg - round(lg)) < 1e-12 and Fraction(abs(x)) != Fraction(10) ** round(lg):
        raise Excluded("saved value near a power of ten")
    k = math.ceil(lg) if abs(x) >= 1 else math.floor(lg)
    s = "%.*f" % (max(0, p - k), x)
    return s.rstrip("0").rstrip(".") if "." in s else s


def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


def read_note(el):
    a = el.attrib
    if set(a) - NOTE_ATTRS or not {"Time", "Duration", "Velocity", "OffVelocity"} <= set(a):
        raise Excluded("note attributes")
    nt = {"Time": number(a["Time"]), "Duration": number(a["Duration"], invalid_ok=True),
          "Velocity": number(a["Velocity"], True), "VelocityDeviation": number(a.get("VelocityDeviation", "0"), True),
          "OffVelocity": number(a["OffVelocity"], True), "Probability": number(a.get("Probability", "1"), True),
          "IsEnabled": boolean(a.get("IsEnabled", "true")),
          "NoteId": integer(a["NoteId"]) if "NoteId" in a else None}
    nt["Velocity"] = clamp(nt["Velocity"], 1.0, 127.0)
    nt["OffVelocity"] = clamp(nt["OffVelocity"], 0.0, 127.0)
    nt["Probability"] = clamp(nt["Probability"], 0.0, 1.0)
    if nt["Duration"] < 0 or nt["Duration"] == DMAX:
        nt["Duration"] = 0.0
    nt["Time"], nt["Duration"] = grid(nt["Time"]), grid(nt["Duration"])
    return nt


def read_tracks(el):
    tracks, ids = [], []
    for kt in el:
        if kt.tag != "KeyTrack" or set(kt.attrib) != {"Id"} or [c.tag for c in kt] != ["Notes", "MidiKey"]:
            raise Excluded("key track shape")
        ids.append(plain(kt.get("Id")))
        notes = []
        for x in kt[0]:
            if x.tag != "MidiNoteEvent":
                raise Refused(f"element {x.tag} among notes")
            notes.append(read_note(x))
        if set(kt[1].attrib) != {"Value"} or len(kt[1]):
            raise Excluded("MidiKey shape")
        key = plain(kt[1].get("Value"), neg=True)
        if not 0 <= key <= 127 or not notes:
            raise Excluded("key range or empty key track")
        tracks.append((key, notes))
    keys = [k for k, _ in tracks]
    if any(a >= b for a, b in zip(keys, keys[1:])) or len(set(ids)) != len(ids):
        raise Excluded("key order, repeated key or repeated key track Id")
    return tracks


def read_event(x):
    b = x.attrib
    if x.tag != "PerNoteEvent" or set(b) - {"TimeOffset", "Value", *CURVES} or not {"TimeOffset", "Value"} <= set(b):
        raise Excluded("event shape")
    return {"TimeOffset": grid(number(b["TimeOffset"], invalid_ok=True)), "Value": number(b["Value"], True),
            **{c: number(b.get(c, "0.5")) for c in CURVES}}


def read_lists(store):
    if [c.tag for c in store] != ["EventLists"]:
        raise Excluded("store shape")
    lists = []
    for el in store[0]:
        if el.tag != "PerNoteEventList" or set(el.attrib) != {"Id", "NoteId", "CC"} or \
                [c.tag for c in el] != ["Events"]:
            raise Excluded("list shape")
        lists.append({"Id": plain(el.get("Id")), "NoteId": plain(el.get("NoteId")), "CC": plain(el.get("CC"), True),
                      "events": [read_event(x) for x in el[0]]})
    if len({lst["Id"] for lst in lists}) != len(lists):
        raise Excluded("repeated list Id")
    return lists


def generator(el):
    if [c.tag for c in el] != ["NextId"] or set(el[0].attrib) != {"Value"}:
        raise Excluded("generator shape")
    return integer(el[0].get("Value"))


def valid_cc(cc):
    return -2 <= cc <= 128 and cc not in (0, 32) and not 120 <= cc <= 128


def process_lists(lists):
    """REQ-014 clauses 1 (NoteId 0, CC), 2 and 3, in the released order."""
    for lst in lists:
        if valid_cc(lst["CC"]):
            lo, hi = (-8192.0, 8191.0) if lst["CC"] == -2 else (0.0, 127.0)
            lst["events"] = [dict(x, Value=clamp(x["Value"], lo, hi)) for x in lst["events"] if x["TimeOffset"] != DMAX]
            lst["events"].sort(key=lambda x: x["TimeOffset"])
    kept = [lst for lst in lists if lst["NoteId"] != 0 and valid_cc(lst["CC"])]
    pairs = [(lst["NoteId"], lst["CC"]) for lst in kept]
    if len(set(pairs)) != len(pairs):
        raise Refused("repeated NoteId and CC")
    return kept


def ordered(tracks):
    for _, notes in tracks:
        for a, b in zip(notes, notes[1:]):
            if b["Time"] <= a["Time"] or b["Time"] < a["Time"] + a["Duration"]:
                return False
    return True


def note_text(nt):
    out = {"Time": fmt(nt["Time"], 17), "Duration": fmt(nt["Duration"], 17), "Velocity": fmt(nt["Velocity"], 9)}
    if nt["VelocityDeviation"] != 0:
        out["VelocityDeviation"] = fmt(nt["VelocityDeviation"], 9)
    out["OffVelocity"] = fmt(nt["OffVelocity"], 9)
    if nt["Probability"] != 1:
        out["Probability"] = fmt(nt["Probability"], 9)
    if not nt["IsEnabled"]:
        out["IsEnabled"] = "false"
    out["NoteId"] = str(nt["NoteId"])
    return out


def event_text(x):
    return {"TimeOffset": fmt(x["TimeOffset"], 17), "Value": fmt(x["Value"], 9),
            **{c: fmt(x[c], 17) for c in CURVES if x[c] != 0.5}}


def process(raw):
    if raw[:10] != GZ_HEADER:
        raise Excluded("container")
    try:
        root = ET.fromstring(zlib.decompress(raw, 31))
    except ET.ParseError:
        raise Refused("not well-formed XML")
    clips = root.findall(CLIP)
    if root.tag != "Ableton" or root.attrib != ENVELOPE or len(clips) != 1 or clips[0].find("Notes") is None:
        raise Excluded("carrier")
    el = clips[0].find("Notes")
    if [c.tag for c in el] != CHILDREN or len(el[2]):
        raise Excluded("notes element shape or probability groups")
    tracks, lists = read_tracks(el[0]), read_lists(el[1])
    generator(el[3])
    stored_next = generator(el[4])
    notes = [nt for _, ns in tracks for nt in ns]
    absent = [nt["NoteId"] is None for nt in notes]
    if any(absent) and not all(absent):
        raise Excluded("NoteId absent from some notes")
    for nt in notes:
        nt["NoteId"] = nt["NoteId"] or 0
    lists = process_lists(lists)
    stored = [nt["NoteId"] for nt in notes if nt["NoteId"]]
    if len(set(stored)) != len(stored):
        raise Refused("repeated NoteId")
    nxt = max(stored_next, max(stored) + 1 if stored else 1)
    lists = [lst for lst in lists if lst["NoteId"] in stored and lst["events"]]
    duration = {nt["NoteId"]: nt["Duration"] for nt in notes if nt["NoteId"]}
    for lst in lists:
        if not all(0 < x["TimeOffset"] < duration[lst["NoteId"]] for x in lst["events"]):
            raise Excluded("event at or outside its note's span")
    for nt in notes:
        if nt["NoteId"] == 0:
            nt["NoteId"], nxt = nxt, nxt + 1
    if not ordered(tracks):
        return ("loads", None)
    return ("loads", {"key_tracks": [{"midi_key": str(k), "notes": [note_text(nt) for nt in ns]} for k, ns in tracks],
                      "event_lists": [{"NoteId": str(lst["NoteId"]), "CC": str(lst["CC"]),
                                       "events": [event_text(x) for x in lst["events"]]} for lst in lists],
                      "note_id_next": str(nxt)})


def model(raw):
    try:
        return process(raw)
    except Refused:
        return ("refused", None)
    except Excluded as x:
        return ("no-expectation", str(x))


def judge(case, got):
    exp = case["expected"]
    if got[0] == "no-expectation":
        return [f"model gives no expectation: {got[1]}"]
    if got[0] != exp["outcome"]:
        return [f"model outcome {got[0]}"]
    if case["action"] != "open-save":
        return [] if "saved_notes" not in exp else ["saved notes listed for an open case"]
    if got[1] is None:
        return ["saved notes undetermined (order or overlap)"]

    def kts(v):  # note attribute order is part of the comparison (REQ-004)
        return [(t["midi_key"], [list(nt.items()) for nt in t["notes"]]) for t in v["key_tracks"]]

    def lsts(v):  # lists matched by NoteId and CC; event attribute order not compared
        return sorted((x["NoteId"], x["CC"], [sorted(ev.items()) for ev in x["events"]]) for x in v["event_lists"])

    s, x = got[1], exp["saved_notes"]
    return [k for k, ok in (("key tracks", kts(s) == kts(x)), ("event lists", lsts(s) == lsts(x)),
                            ("next id", s["note_id_next"] == x["note_id_next"])) if not ok]
