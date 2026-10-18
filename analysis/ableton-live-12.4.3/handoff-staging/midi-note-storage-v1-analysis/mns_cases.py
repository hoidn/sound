"""Fixtures, cases and probes of the midi-note-storage-v1 candidate (analyst side; never shipped).

The base notes are fragments F0 and F1 of SPEC-MIDI-NOTE-STORAGE r1, held in a carrier Live Set
written for this release; each case applies one edit. Expected saved notes are hand-authored as
edits of the base expectations (s0, s1). Used by build_mns.py.
"""
import copy, struct, zlib

PROV = "static-derived; not observed reference output"
# Unused since review RVN-01 established that the open-time steps run when a Live Set is opened.
PROV_LIMITS = ("static-derived; rests on the stated assumption that the note value limits apply when a Live Set "
               "is opened; not observed reference output")
GZ_HEADER = bytes.fromhex("1f8b0800000000000213")  # FLG 0, MTIME 0, XFL 2, OS 19 (als-container-v1 form)
ROOT_ATTRS = ('MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1" Creator="Ableton Live 12.4.3" '
              'Revision="0123456789abcdef0123456789abcdef01234567"')
PATH = ["LiveSet", "Tracks", 'MidiTrack Id="1"', "DeviceChain", "MainSequencer", "ClipSlotList", 'ClipSlot Id="0"',
        "ClipSlot", "Value", 'MidiClip Id="0" Time="0"']
ORDER = ["Time", "Duration", "Velocity", "VelocityDeviation", "OffVelocity", "Probability", "IsEnabled", "NoteId",
         "TimeOffset", "Value", "CurveControl1X", "CurveControl1Y", "CurveControl2X", "CurveControl2Y"]
R = "REQ-MIDI-NOTE-STORAGE-"
O, OS, REF, LOADS = "open", "open-save", "refused", "loads"


# ---- fixture model: base fragments F0 and F1 of the parent spec ----
def note(t, d, v, i, o="64"):
    return [["Time", t], ["Duration", d], ["Velocity", v], ["OffVelocity", o], ["NoteId", i]]


def ev(t, v):
    return [["TimeOffset", t], ["Value", v]]


def plist(i, nid, cc, events):
    return {"attrs": [["Id", i], ["NoteId", nid], ["CC", cc]], "events": events}


def f0():
    return {"tracks": [["0", "36", [note("0", "0.25", "85", "1"), note("1", "0.25", "85", "2")]],
                       ["1", "38", [note("0.5", "0.25", "100", "3")]]], "lists": [], "gnext": "1", "next": "4"}


def f1():
    f = f0()
    f["lists"] = [plist("0", "1", "-2", [ev("0.0625", "100"), ev("0.125", "-200")])]
    return f


def nref(f, k):
    return {1: f["tracks"][0][2][0], 2: f["tracks"][0][2][1], 3: f["tracks"][1][2][0]}[k]


def put(attrs, kv):
    for k, v in kv.items():
        hit = [a for a in attrs if a[0] == k]
        if v is None:
            attrs[:] = [a for a in attrs if a[0] != k]
        elif hit:
            hit[0][1] = v
        else:
            attrs.append([k, v])
    attrs.sort(key=lambda a: ORDER.index(a[0]))


def n(k, **kv):  # edit note n1, n2 or n3
    return lambda f: put(nref(f, k), kv)


def e(k, **kv):  # edit event e1 or e2 of list L1
    return lambda f: put(f["lists"][0]["events"][k - 1], kv)


def l1(**kv):  # edit an attribute of list L1
    return lambda f: [a.__setitem__(1, kv[a[0]]) for a in f["lists"][0]["attrs"] if a[0] in kv]


def add_list(nid, cc, events):
    return lambda f: f["lists"].append(plist(str(len(f["lists"])), nid, cc, events))


def F(base, *edits):
    f = base()
    for ed in edits:
        ed(f)
    return f


def attrs_text(attrs):
    return " ".join(f'{k}="{v}"' for k, v in attrs)


def notes_lines(f):
    out = ["<Notes>", "\t<KeyTracks>"]
    for kid, key, notes in f["tracks"]:
        out += [f'\t\t<KeyTrack Id="{kid}">', "\t\t\t<Notes>"]
        out += ["\t\t\t\t" + (x if isinstance(x, str) else f"<MidiNoteEvent {attrs_text(x)} />") for x in notes]
        out += ["\t\t\t</Notes>", f'\t\t\t<MidiKey Value="{key}" />', "\t\t</KeyTrack>"]
    out += ["\t</KeyTracks>", "\t<PerNoteEventStore>"]
    if not f["lists"]:
        out.append("\t\t<EventLists />")
    else:
        out.append("\t\t<EventLists>")
        for lst in f["lists"]:
            out.append(f"\t\t\t<PerNoteEventList {attrs_text(lst['attrs'])}>")
            if lst["events"]:
                out += ["\t\t\t\t<Events>"] + [f"\t\t\t\t\t<PerNoteEvent {attrs_text(x)} />" for x in lst["events"]]
                out.append("\t\t\t\t</Events>")
            else:
                out.append("\t\t\t\t<Events />")
            out.append("\t\t\t</PerNoteEventList>")
        out.append("\t\t</EventLists>")
    out += ["\t</PerNoteEventStore>", "\t<NoteProbabilityGroups />", "\t<ProbabilityGroupIdGenerator>",
            f'\t\t<NextId Value="{f["gnext"]}" />', "\t</ProbabilityGroupIdGenerator>", "\t<NoteIdGenerator>",
            f'\t\t<NextId Value="{f["next"]}" />', "\t</NoteIdGenerator>", "</Notes>"]
    return out


def document(f):
    out = ['<?xml version="1.0" encoding="UTF-8"?>', f"<Ableton {ROOT_ATTRS}>"]
    out += ["\t" * (d + 1) + f"<{el}>" for d, el in enumerate(PATH)]
    ind = "\t" * (len(PATH) + 1)
    out += [ind + x for x in ["<Loop>", '\t<LoopStart Value="0" />', '\t<LoopEnd Value="8" />',
                              '\t<LoopOn Value="true" />', "</Loop>"] + notes_lines(f)]
    out += ["\t" * (d + 1) + f"</{PATH[d].split()[0]}>" for d in reversed(range(len(PATH)))]
    out.append("</Ableton>")
    return ("\n".join(out) + "\n").encode("utf-8")


def gz(data):
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    return GZ_HEADER + c.compress(data) + c.flush() + struct.pack("<II", zlib.crc32(data), len(data))


# ---- hand-authored expected saved notes (edits of the base expectations) ----
def sn(t, d, v, i, o="64"):
    return {"Time": t, "Duration": d, "Velocity": v, "OffVelocity": o, "NoteId": i}


L1S = {"NoteId": "1", "CC": "-2", "events": [{"TimeOffset": "0.0625", "Value": "100"},
                                             {"TimeOffset": "0.125", "Value": "-200"}]}


def s0():
    return {"key_tracks": [{"midi_key": "36", "notes": [sn("0", "0.25", "85", "1"), sn("1", "0.25", "85", "2")]},
                           {"midi_key": "38", "notes": [sn("0.5", "0.25", "100", "3")]}],
            "event_lists": [], "note_id_next": "4"}


def s1():
    s = s0()
    s["event_lists"] = [copy.deepcopy(L1S)]
    return s


def X(base, notes=None, nxt=None, lists=None):
    s = base()
    where = {1: s["key_tracks"][0]["notes"][0], 2: s["key_tracks"][0]["notes"][1], 3: s["key_tracks"][1]["notes"][0]}
    for k, kv in (notes or {}).items():
        d = where[k]
        for a, v in kv.items():
            d.pop(a) if v is None else d.__setitem__(a, v)
        ordered = {a: d[a] for a in ORDER if a in d}
        d.clear()
        d.update(ordered)
    if nxt:
        s["note_id_next"] = nxt
    if lists is not None:
        s["event_lists"] = lists
    return s


def L1(cc="-2", events=None):
    return {"NoteId": "1", "CC": cc, "events": events or copy.deepcopy(L1S["events"])}


def nid(f, v):
    for k in (1, 2, 3):
        put(nref(f, k), {"NoteId": v})


ALPHA = [["Duration", "0.25"], ["IsEnabled", "false"], ["NoteId", "1"], ["OffVelocity", "64"],
         ["Probability", "0.5"], ["Time", "0"], ["Velocity", "85"], ["VelocityDeviation", "3"]]
OPT3 = {1: {"VelocityDeviation": "3", "Probability": "0.5", "IsEnabled": "false"}}
H = "0.000000260156510156510156"
EV1 = [ev("0.0625", "1")]
CC_DROP = {"a": "0", "b": "32", "c": "120", "d": "128", "e": "129", "f": "-3"}
CC_KEEP = {"a": "1", "b": "119", "c": "-1"}
KEEP_E = [{"TimeOffset": "0.0625", "Value": "100"}, {"TimeOffset": "0.125", "Value": "0"}]

# id, kind, requirement suffixes, purpose, fixture notes, action, expected (REF, LOADS or saved notes), limits flag
CASES = [
    ("MNS-001", "save", ["001", "004", "010", "016"], "Base notes unchanged: the saved key tracks, notes and next id equal the input",
     F(f0), OS, s0(), False),
    ("MNS-002", "positive", ["003", "004"], "n1 states VelocityDeviation 0, Probability 1 and IsEnabled true; "
     "none of them is written", F(f0, n(1, VelocityDeviation="0", Probability="1", IsEnabled="true")), OS, s0(), False),
    ("MNS-003", "save", ["003", "004", "016"], "n1 states VelocityDeviation 3, Probability 0.5 and IsEnabled false; "
     "they are written in order and n2 keeps its defaults",
     F(f0, n(1, VelocityDeviation="3", Probability="0.5", IsEnabled="false")), OS, X(s0, OPT3), False),
    ("MNS-004", "boundary", ["002", "003", "004"], "n1 lists all eight attributes in alphabetical order",
     F(f0, lambda f: nref(f, 1).__setitem__(slice(None), copy.deepcopy(ALPHA))), OS, X(s0, OPT3), False),
    ("MNS-005", "positive", ["002", "004"], "IsEnabled text 0 on n1 and 1 on n2",
     F(f0, n(1, IsEnabled="0"), n(2, IsEnabled="1")), OS, X(s0, {1: {"IsEnabled": "false"}}), False),
    ("MNS-006", "negative", ["002"], "IsEnabled text TRUE on n1 is refused", F(f0, n(1, IsEnabled="TRUE")), O, REF, False),
    ("MNS-007", "negative", ["002"], "NoteId text 3.0 on n3 is refused", F(f0, n(3, NoteId="3.0")), O, REF, False),
    ("MNS-008", "negative", ["002"], "NoteId text 0x3 on n3 is refused", F(f0, n(3, NoteId="0x3")), O, REF, False),
    ("MNS-009", "negative", ["002"], "Empty NoteId text on n3 is refused", F(f0, n(3, NoteId="")), O, REF, False),
    ("MNS-010", "boundary", ["002", "009"], "NoteId text ' +7' on n3 reads as 7 and raises the next id to 8",
     F(f0, n(3, NoteId=" +7")), OS, X(s0, {3: {"NoteId": "7"}}, nxt="8"), False),
    ("MNS-012", "negative", ["002"], "n1 carries the Velocity attribute twice (not well-formed XML)",
     F(f0, lambda f: nref(f, 1).insert(3, ["Velocity", "85"])), O, REF, False),
    ("MNS-013", "negative", ["001"], "An element Foo after n2 among the notes of key 36 is refused",
     F(f0, lambda f: f["tracks"][0][2].append("<Foo />")), O, REF, False),
    ("MNS-014", "boundary", ["005", "016"], "Velocity 0, 300 and 0.5 are limited to 1, 127 and 1",
     F(f0, n(1, Velocity="0"), n(2, Velocity="300"), n(3, Velocity="0.5")), OS,
     X(s0, {1: {"Velocity": "1"}, 2: {"Velocity": "127"}, 3: {"Velocity": "1"}}), False),
    ("MNS-015", "boundary", ["005"], "OffVelocity -5 and 200 are limited to 0 and 127",
     F(f0, n(1, OffVelocity="-5"), n(2, OffVelocity="200")), OS,
     X(s0, {1: {"OffVelocity": "0"}, 2: {"OffVelocity": "127"}}), False),
    ("MNS-016", "boundary", ["004", "005"], "Probability 1.5 is limited to 1 and omitted; -1 is limited to 0",
     F(f0, n(1, Probability="1.5"), n(2, Probability="-1")), OS, X(s0, {2: {"Probability": "0"}}), False),
    ("MNS-017", "boundary", ["002", "005"], "Duration -2 and Duration Invalid both become 0",
     F(f0, n(1, Duration="-2"), n(2, Duration="Invalid")), OS,
     X(s0, {1: {"Duration": "0"}, 2: {"Duration": "0"}}), False),
    ("MNS-018", "boundary", ["005", "007"], "Time -3 and VelocityDeviation -500 on n1 are not limited",
     F(f0, n(1, Time="-3", VelocityDeviation="-500")), OS,
     X(s0, {1: {"Time": "-3", "VelocityDeviation": "-500"}}), False),
    ("MNS-019", "positive", ["002", "005", "016"], "Fractional Velocity 80.578949 and 33.3 are kept as binary32",
     F(f0, n(1, Velocity="80.578949"), n(2, Velocity="33.3")), OS,
     X(s0, {1: {"Velocity": "80.578949"}, 2: {"Velocity": "33.2999992"}}), False),
    ("MNS-020", "boundary", ["006", "016"], "Off-grid Time 0.123456789 and Duration 0.3333333333 on n1 are rounded",
     F(f0, n(1, Time="0.123456789", Duration="0.3333333333")), OS,
     X(s0, {1: {"Time": "0.123456751581751581", "Duration": "0.333333333333333315"}}), False),
    ("MNS-021", "boundary", ["006", "016"], "Time -0.0000002 on n1 rounds to minus one grid unit",
     F(f0, n(1, Time="-0.0000002")), OS, X(s0, {1: {"Time": "-" + H}}), False),
    ("MNS-022", "boundary", ["006", "016"], "Time 0.00000013 on n1 rounds to 0; Duration 0.000000131 on n3 rounds "
     "to one grid unit", F(f0, n(1, Time="0.00000013"), n(3, Duration="0.000000131")), OS,
     X(s0, {3: {"Duration": H}}), False),
    ("MNS-025", "positive", ["007"], "n2 at Time 20, outside the clip loop from 0 to 8, and n3 with Duration 0 "
     "are kept", F(f0, n(2, Time="20"), n(3, Duration="0")), OS,
     X(s0, {2: {"Time": "20"}, 3: {"Duration": "0"}}), False),
    ("MNS-026", "negative", ["008"], "n3 repeats NoteId 2 of n2 in another key", F(f0, n(3, NoteId="2")), O, REF, False),
    ("MNS-027", "negative", ["008"], "n2 repeats NoteId 1 of n1 in the same key", F(f0, n(2, NoteId="1")), O, REF, False),
    ("MNS-028", "positive", ["009"], "n2 with NoteId 0 receives 4; the next id becomes 5",
     F(f0, n(2, NoteId="0")), OS, X(s0, {2: {"NoteId": "4"}}, nxt="5"), False),
    ("MNS-029", "positive", ["009"], "All three notes with NoteId 0 receive 4, 5 and 6 in key order",
     F(f0, lambda f: nid(f, "0")), OS,
     X(s0, {1: {"NoteId": "4"}, 2: {"NoteId": "5"}, 3: {"NoteId": "6"}}, nxt="7"), False),
    ("MNS-030", "missing", ["009"], "NoteId absent from every note: numbered as in MNS-029",
     F(f0, lambda f: nid(f, None)), OS,
     X(s0, {1: {"NoteId": "4"}, 2: {"NoteId": "5"}, 3: {"NoteId": "6"}}, nxt="7"), False),
    ("MNS-031", "boundary", ["009"], "Stored next id 1 is raised to 4",
     F(f0, lambda f: f.__setitem__("next", "1")), OS, s0(), False),
    ("MNS-032", "boundary", ["009"], "Stored next id 100 is kept",
     F(f0, lambda f: f.__setitem__("next", "100")), OS, X(s0, nxt="100"), False),
    ("MNS-033", "boundary", ["009"], "All NoteIds 0 with stored next id 100: 100, 101 and 102",
     F(f0, lambda f: (nid(f, "0"), f.__setitem__("next", "100"))), OS,
     X(s0, {1: {"NoteId": "100"}, 2: {"NoteId": "101"}, 3: {"NoteId": "102"}}, nxt="103"), False),
    ("MNS-036", "boundary", ["010"], "n1 Duration 2 overlaps n2 on the same key; the set loads",
     F(f0, n(1, Duration="2")), O, LOADS, False),
    ("MNS-039", "save", ["013", "014", "016"], "Base list L1 unchanged", F(f1), OS, s1(), False),
    ("MNS-040", "save", ["013", "016"], "e1 adds CurveControl1X 0.5 (omitted on save) and CurveControl1Y 0.2",
     F(f1, e(1, CurveControl1X="0.5", CurveControl1Y="0.2")), OS,
     X(s1, lists=[L1(events=[{"TimeOffset": "0.0625", "Value": "100", "CurveControl1Y": "0.200000000000000011"},
                             {"TimeOffset": "0.125", "Value": "-200"}])]), False),
    ("MNS-041", "negative", ["014"], "A second list with NoteId 1 and CC -2 is refused",
     F(f1, add_list("1", "-2", EV1)), O, REF, False),
    ("MNS-042", "positive", ["014"], "A second list for n1 with CC 74 is kept beside L1",
     F(f1, add_list("1", "74", [ev("0.0625", "64")])), OS,
     X(s1, lists=[L1(), {"NoteId": "1", "CC": "74", "events": [{"TimeOffset": "0.0625", "Value": "64"}]}]), False),
    *[(f"MNS-043{v}", "boundary", ["014"], f"L1 with CC {cc} is removed", F(f1, l1(CC=cc)), OS, X(s1, lists=[]), False)
      for v, cc in CC_DROP.items()],
    *[(f"MNS-044{v}", "boundary", ["014"], f"L1 with CC {cc} is kept and its values limited to 0..127",
       F(f1, l1(CC=cc)), OS, X(s1, lists=[L1(cc, copy.deepcopy(KEEP_E))]), False) for v, cc in CC_KEEP.items()],
    ("MNS-045a", "boundary", ["014"], "L1 with NoteId 0 is removed", F(f1, l1(NoteId="0")), OS, X(s1, lists=[]), False),
    ("MNS-045b", "boundary", ["014"], "L1 naming NoteId 99, which no note has, is removed",
     F(f1, l1(NoteId="99")), OS, X(s1, lists=[]), False),
    ("MNS-046", "boundary", ["014"], "Two lists with NoteId 99 and CC -2 are refused although no note has NoteId 99",
     F(f1, l1(NoteId="99"), add_list("99", "-2", EV1)), O, REF, False),
    ("MNS-047", "boundary", ["014", "016"], "Values 9000 and -9000 for CC -2 are limited to 8191 and -8192",
     F(f1, e(1, Value="9000"), e(2, Value="-9000")), OS,
     X(s1, lists=[L1(events=[{"TimeOffset": "0.0625", "Value": "8191"}, {"TimeOffset": "0.125", "Value": "-8192"}])]),
     False),
    ("MNS-048", "boundary", ["014"], "Values 200 and -1 for CC 74 are limited to 127 and 0",
     F(f1, l1(CC="74"), e(1, Value="200"), e(2, Value="-1")), OS,
     X(s1, lists=[L1("74", [{"TimeOffset": "0.0625", "Value": "127"}, {"TimeOffset": "0.125", "Value": "0"}])]),
     False),
    ("MNS-049a", "boundary", ["014"], "e2 listed before e1: events are sorted by TimeOffset",
     F(f1, lambda f: f["lists"][0]["events"].reverse()), OS, s1(), False),
    ("MNS-049b", "boundary", ["014"], "A third event at TimeOffset 0.0625 after e2 keeps its place after e1",
     F(f1, lambda f: f["lists"][0]["events"].append(ev("0.0625", "5"))), OS,
     X(s1, lists=[L1(events=[{"TimeOffset": "0.0625", "Value": "100"}, {"TimeOffset": "0.0625", "Value": "5"},
                             {"TimeOffset": "0.125", "Value": "-200"}])]), False),
    ("MNS-050", "boundary", ["014"], "L1 stored with an empty Events element is removed",
     F(f1, lambda f: f["lists"][0].__setitem__("events", [])), OS, X(s1, lists=[]), False),
    ("MNS-051a", "boundary", ["002", "014"], "e2 with TimeOffset Invalid is dropped",
     F(f1, e(2, TimeOffset="Invalid")), OS, X(s1, lists=[L1(events=[{"TimeOffset": "0.0625", "Value": "100"}])]),
     False),
    ("MNS-051b", "boundary", ["002", "014"], "e1 and e2 with TimeOffset Invalid: L1 is left empty and removed",
     F(f1, e(1, TimeOffset="Invalid"), e(2, TimeOffset="Invalid")), OS, X(s1, lists=[]), False),
    ("MNS-052", "boundary", ["009", "014"], "n2 with NoteId 0 receives 4; a list naming 4 is removed",
     F(f1, n(2, NoteId="0"), add_list("4", "-2", EV1)), OS, X(s1, {2: {"NoteId": "4"}}, nxt="5"), False),
    ("MNS-061", "positive", ["002"], "NoteId text ' 1', '+2' and '3 ' read as 1, 2 and 3",
     F(f0, n(1, NoteId=" 1"), n(2, NoteId="+2"), n(3, NoteId="3 ")), OS, s0(), False),
    ("MNS-062", "negative", ["002"], "NoteId text +-3 on n3 is refused", F(f0, n(3, NoteId="+-3")), O, REF, False),
    ("MNS-063", "negative", ["002"], "NoteId text of three spaces on n3 is refused",
     F(f0, n(3, NoteId="   ")), O, REF, False),
    ("MNS-064", "negative", ["002"], "NoteId text U+FF13 (fullwidth digit three) on n3 is refused",
     F(f0, n(3, NoteId="３")), O, REF, False),
    ("MNS-065", "negative", ["002"], "NoteId text of 64 digits (63 zeros, then 3) on n3 is refused",
     F(f0, n(3, NoteId="0" * 63 + "3")), O, REF, False),
    ("MNS-066", "negative", ["002"], "NoteId 9223372036854775808 on n3 exceeds the 64-bit range and is refused",
     F(f0, n(3, NoteId="9223372036854775808")), O, REF, False),
    ("MNS-067", "boundary", ["002", "016"], "Time text ' 0.5abc' on n3 reads as 0.5",
     F(f0, n(3, Time=" 0.5abc")), OS, s0(), False),
    ("MNS-068", "negative", ["002"], "Velocity text abc on n1 is refused", F(f0, n(1, Velocity="abc")), O, REF, False),
    ("MNS-069", "boundary", ["006", "013", "016"], "Off-grid TimeOffset 0.123456789 on e1 is rounded",
     F(f1, e(1, TimeOffset="0.123456789")), OS,
     X(s1, lists=[L1(events=[{"TimeOffset": "0.123456751581751581", "Value": "100"},
                             {"TimeOffset": "0.125", "Value": "-200"}])]), False),
    ("MNS-070", "boundary", ["010"], "n2 at Time 0, the same Time as n1 on the same key; the set loads",
     F(f0, n(2, Time="0")), O, LOADS, False),
    *[(f"MNS-071{v}", "boundary", ["014"], f"L1 with CC {cc} is kept and its values limited to 0..127",
       F(f1, l1(CC=cc)), OS, X(s1, lists=[L1(cc, copy.deepcopy(KEEP_E))]), False)
      for v, cc in {"a": "31", "b": "33"}.items()],
]
COMPARATOR = {
    O: "outcome exact",
    OS: "outcome exact; saved notes element compared as parsed XML: children and order, key tracks and notes in "
        "order with exact attribute sets and text in save order, lists matched by NoteId and CC with events in order, "
        "next id exact; key track and list Ids, NoteProbabilityGroups content and the ProbabilityGroupIdGenerator "
        "NextId not compared",
}


def swap_tracks(f):
    f["tracks"].reverse()


# Excluded or unresolved inputs (several from MNS-011 to MNS-053): the model must give no saved expectation.
PROBES = {
    "MidiKey 128": F(f0, lambda f: f["tracks"][1].__setitem__(1, "128")),
    "MidiKey -1": F(f0, lambda f: f["tracks"][1].__setitem__(1, "-1")),
    "two key tracks with key 36": F(f0, lambda f: f["tracks"][1].__setitem__(1, "36")),
    "key tracks in descending key order": F(f0, swap_tracks),
    "empty key track": F(f0, lambda f: f["tracks"][1].__setitem__(2, [])),
    "repeated key track Id": F(f0, lambda f: f["tracks"][1].__setitem__(0, "0")),
    "notes of key 36 out of order": F(f0, lambda f: f["tracks"][0][2].reverse()),
    "NoteId ' 7 '": F(f0, n(3, NoteId=" 7 ")),
    "NoteId -5": F(f0, n(3, NoteId="-5")),
    "next id -5": F(f0, lambda f: f.__setitem__("next", "-5")),
    "NoteId absent from n1 only": F(f0, n(1, NoteId=None)),
    "Time absent from n1": F(f0, n(1, Time=None)),
    "Time -0.0000001 (negative zero)": F(f0, n(1, Time="-0.0000001")),
    "Time Invalid": F(f0, n(2, Time="Invalid")),
    "Velocity inf": F(f0, n(1, Velocity="inf")),
    "event at offset 0": F(f1, e(1, TimeOffset="0")),
    "event at the note's Duration": F(f1, e(2, TimeOffset="0.25")),
    "event before offset 0": F(f1, e(1, TimeOffset="-0.1")),
}
