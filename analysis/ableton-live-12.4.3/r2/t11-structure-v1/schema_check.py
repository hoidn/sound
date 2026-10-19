"""Check Live Set XML against the shipped class schema (12.0_12402) and the T1.1 structure rules.

Usage: python3 -I schema_check.py <schema.txt> <doc.als|doc.xml>...   (gzip or plain XML)
Output: one JSON line per document: schema deviations (element or attribute names the schema
does not declare for the parent's class, and children out of the class's field order) and
structure-rule results. Analyst tool; output is data.

Schema model (from the schema file's own form): each class element lists fields with Class and
Type. Type 0 is a compound of class Class; Type -4 a base value (written either as an attribute of
the parent or as a child element with a Value attribute); Type -1 a list or slot whose children
are elements named by their class; Type -3 an array whose items are named by ArrayTranslator.
List items additionally carry an Id attribute. A field Class of the form Slot<X> is a slot (Type -1).
"""
import gzip, json, sys
import xml.etree.ElementTree as ET


def load_schema(p):
    r = ET.parse(p).getroot()
    return {c.tag: {f.tag: (f.get("Class"), f.get("Type"), f.get("ArrayTranslator")) for f in c} for c in r}


POINTEE_CLASSES = {"Pointee", "FloatAutomationTarget", "EnumAutomationTarget", "BoolAutomationTarget",
                   "TimeableModulationTarget", "UserFloatModulationTarget"}


def check(schema, root):
    """Return (deviations, pointee elements). A pointee is an element whose schema class is one of
    POINTEE_CLASSES (the schema's classes with an Id field that the reader treats as pointees)."""
    dev = {}
    pointees = []

    def note(kind, path, name):
        dev.setdefault(f"{kind} {path} {name}", 0)
        dev[f"{kind} {path} {name}"] += 1

    def walk(e, cls, path, is_item):
        fields = schema.get(cls)
        if fields is None:
            note("unknown-class", path, cls)
            return
        for a in e.attrib:
            if a == "Id" and (is_item or "Id" in fields):
                continue
            f = fields.get(a)
            if f is None or f[1] != "-4":
                note("unknown-attribute", f"{cls}", a)
        order = list(fields)
        last = -1
        for c in e:
            if c.tag in fields:
                i = order.index(c.tag)
                if i < last:
                    note("order", cls, c.tag)
                last = max(last, i)
        for c in e:
            f = fields.get(c.tag)
            if f is None:
                note("unknown-element", cls, c.tag)
                continue
            fcls, ftype, arr = f
            if ftype == "-4":
                if set(c.attrib) - {"Value"} or len(c):
                    note("base-shape", cls, c.tag)
            elif ftype == "0":
                if fcls in POINTEE_CLASSES:
                    pointees.append(c)
                walk(c, fcls, f"{cls}/{c.tag}", False)
            elif ftype == "-1":
                for item in c:
                    if "Id" not in item.attrib and fcls == "RemoteableList":
                        note("list-item-without-id", f"{cls}/{c.tag}", item.tag)
                    walk(item, item.tag, f"{cls}/{c.tag}/*", True)
            elif ftype == "-3":
                for item in c:
                    if item.tag != arr:
                        note("array-item", f"{cls}/{c.tag}", item.tag)

    ls = root.find("LiveSet")
    walk(ls, "LiveSet", "LiveSet", False)
    return dev, pointees


def rules(root, pels):
    """Structure measurements named after SPEC-LIVE-SET-STRUCTURE's rules (facts, not verdicts)."""
    ls = root.find("LiveSet")
    out = {}
    tracks = list(ls.find("Tracks")) if ls.find("Tracks") is not None else []
    types = [t.tag for t in tracks]
    out["player_tracks"] = sum(t in ("AudioTrack", "MidiTrack", "GroupTrack") for t in types)
    first_ret = types.index("ReturnTrack") if "ReturnTrack" in types else len(types)
    out["returns_after_others"] = all(t == "ReturnTrack" for t in types[first_ret:])
    trailing = 0
    for t in reversed(types):
        if t != "ReturnTrack":
            break
        trailing += 1
    out["trailing_returns"] = trailing
    out["grouped_tracks"] = sum(1 for t in tracks if t.find("TrackGroupId") is not None and t.find("TrackGroupId").get("Value") != "-1")
    scenes = list(ls.find("Scenes")) if ls.find("Scenes") is not None else []
    out["scenes"] = len(scenes)
    out["scenes_present"] = ls.find("Scenes") is not None
    main_eq_freeze, main_eq_scenes = True, True
    for t in tracks:
        if t.tag not in ("AudioTrack", "MidiTrack"):
            continue
        n_main = len(t.findall("DeviceChain/MainSequencer/ClipSlotList/ClipSlot"))
        n_freeze = len(t.findall("DeviceChain/FreezeSequencer/ClipSlotList/ClipSlot"))
        main_eq_freeze &= n_main == n_freeze
        main_eq_scenes &= n_main == len(scenes)
    out["freeze_slots_equal_main"] = main_eq_freeze
    out["main_slots_equal_scenes"] = main_eq_scenes
    holders = [len(t.findall("DeviceChain/Mixer/Sends/TrackSendHolder")) for t in tracks]
    out["holders_more_than_returns"] = any(n > trailing for n in holders)
    out["holders_fewer_than_returns"] = any(n < trailing for n in holders)
    special = [ls.find(k) for k in ("MainTrack", "PreHearTrack")]
    out["main_prehear_no_sends"] = all(s is None or not s.findall("DeviceChain/Mixer/Sends/TrackSendHolder") for s in special)
    sp = ls.find("SendsPre")
    out["sendspre_present"] = sp is not None
    out["sendspre_equal_returns"] = (0 if sp is None else len(list(sp))) == trailing
    pset = set(map(id, pels))
    pids = [int(e.get("Id")) for e in pels if "Id" in e.attrib]
    out["pointees"] = len(pels)
    out["pointee_without_id_or_zero"] = sum(1 for e in pels if e.get("Id") in (None, "0"))
    nz = [i for i in pids if i != 0]
    out["pointee_ids_unique"] = len(nz) == len(set(nz))
    npid = ls.find("NextPointeeId")
    out["next_pointee_id"] = None if npid is None else int(npid.get("Value"))
    out["max_pointee_id"] = max(pids) if pids else None
    effective_next = 1 if npid is None else int(npid.get("Value"))
    out["next_pointee_id_above_max"] = effective_next > max([0] + pids)
    by_id = {e.get("Id") for e in pels}
    out["dangling_envelopes"] = sum(1 for env in list(root.iter("AutomationEnvelope")) + list(root.iter("ClipEnvelope"))
                                    if env.find("EnvelopeTarget/PointeeId").get("Value") not in by_id)
    lists_ok = True
    for p in root.iter():
        kids = [c.get("Id") for c in p if "Id" in c.attrib and id(c) not in pset]
        if len(kids) != len(set(kids)):
            lists_ok = False
    out["list_item_ids_unique"] = lists_ok
    return out


def main():
    schema = load_schema(sys.argv[1])
    for p in sys.argv[2:]:
        b = open(p, "rb").read()
        try:  # deliberately malformed inputs (container cases) are reported, not checked
            root = ET.fromstring(gzip.decompress(b) if b[:2] == b"\x1f\x8b" else b)
            if root.find("LiveSet") is None:
                raise ValueError("no LiveSet element")
        except (ET.ParseError, OSError, EOFError, ValueError) as e:
            print(json.dumps({"doc": p, "error": f"{type(e).__name__}: {e}"}))
            continue
        dev, pels = check(schema, root)
        print(json.dumps({"doc": p.rsplit("/App-Resources/", 1)[-1], "minor": root.get("MinorVersion"),
                          "deviations": dev, "rules": rules(root, pels)}, sort_keys=True))


if __name__ == "__main__":
    main()
