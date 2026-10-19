"""Audit every released fixture against the structural load rules of SPEC-LIVE-SET-STRUCTURE r1.

Usage: python3 -I fixture_audit.py <schema.txt> <handoff dir> <out.json>
Read-only on handoff/. For each release, each fixture file is classified (Live Set, device preset,
deliberately unparseable, or not a Live Set document) and linked to the cases that use it with their
expectations. For a Live Set, the traced refusals are evaluated:
  REQ-002  no audio, MIDI or group track; a player track after a return track     (validation walk)
  REQ-006  an audio or MIDI track whose freeze slot count differs from its session slot count (walk)
  REQ-013  a mixer with more send holders than trailing return tracks              (root post-load)
  REQ-015  a pointee present with Id 0 or without Id; NextPointeeId not above the largest pointee Id
  REQ-016  a negative or duplicate list-item Id (S-cond A5)
and two shapes with no load check (REQ-006 slots != scenes, REQ-013 SendsPre != returns) are noted.
For a fixture that would be refused, the minimal addition taken from T11-MIN's skeleton is recorded
as XML text with its insertion point, applied to a copy, and the copy is re-checked. The addition
only adds elements; no existing element or value changes, so what the case tests is kept.
Envelope, value-text and field-level refusals belong to the other specs and are not evaluated.
"""
import copy, gzip, json, os, sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schema_check import check, load_schema, rules  # noqa: E402

OPENS = {"opens", "loads", "accepted"}  # outcomes that require the set to open
FREEZE_SLOT = '<ClipSlot Id="{i}"><ClipSlot><Value /></ClipSlot><HasStop Value="true" /></ClipSlot>'
MIDI_TRACK = ('<Tracks><MidiTrack Id="1"><Name><EffectiveName Value="1-MIDI" /><UserName Value="" /></Name>'
              '<Color Value="15" /><TrackGroupId Value="-1" /><DeviceChain><AudioOutputRouting>'
              '<Target Value="AudioOut/Main" /></AudioOutputRouting><MainSequencer><ClipSlotList /></MainSequencer>'
              '<FreezeSequencer><ClipSlotList /></FreezeSequencer></DeviceChain></MidiTrack></Tracks>')
SCENE = ('<Scene Id="{i}"><Name Value="" /><Color Value="-1" /><Tempo Value="120" /><IsTempoEnabled Value="false" />'
         '<TimeSignatureId Value="201" /><IsTimeSignatureEnabled Value="false" /></Scene>')
LIVESET_ORDER = []  # the schema's LiveSet field order, set in main()


def read(path):
    b = open(path, "rb").read()
    try:
        root = ET.fromstring(gzip.decompress(b) if b[:2] == b"\x1f\x8b" else b)
    except (ET.ParseError, OSError, EOFError, UnicodeDecodeError) as e:
        return None, f"unparseable: {type(e).__name__}: {e}"
    if root.tag != "Ableton":
        return None, f"not a Live Set document (root {root.tag})"
    if root.find("LiveSet") is None:
        kids = [c.tag for c in root]
        return None, f"not a Live Set document (Ableton root holding {kids[:1]})"
    return root, "live-set"


def insert_ordered(ls, el):
    """Insert a LiveSet child at its schema position among the T1 fields."""
    rank = LIVESET_ORDER.index(el.tag)
    for i, c in enumerate(list(ls)):
        if c.tag in LIVESET_ORDER and LIVESET_ORDER.index(c.tag) > rank:
            ls.insert(i, el)
            return
    ls.append(el)


def refusals(r, dev):
    out = []
    if r["player_tracks"] == 0:
        out.append("REQ-002: no audio, MIDI or group track")
    if not r["returns_after_others"]:
        out.append("REQ-002: player track after a return track")
    if not r["freeze_slots_equal_main"]:
        out.append("REQ-006: freeze slot count differs from session slot count")
    if r["holders_more_than_returns"]:
        out.append("REQ-013: more send holders than return tracks")
    if r["pointee_without_id_or_zero"]:
        out.append("REQ-015: pointee with Id 0 or without Id")
    if not r["next_pointee_id_above_max"]:
        out.append("REQ-015: NextPointeeId not above the largest pointee Id")
    if not r["list_item_ids_unique"]:
        out.append("REQ-016: duplicate list-item Id (S-cond A5)")
    if r.get("negative_list_ids"):
        out.append("REQ-016: negative list-item Id (S-cond A5)")
    return out


def unknowns(r):
    out = []
    if not r["main_slots_equal_scenes"]:
        out.append("REQ-006 U: session slot count differs from scene count (no load check found)")
    if not r["sendspre_equal_returns"]:
        out.append("REQ-013 U: SendsPre length differs from the number of return tracks (no load check found)")
    return out


def measure(schema, root):
    dev, pels = check(schema, root)
    r = rules(root, pels)
    pset = set(map(id, pels))
    r["negative_list_ids"] = sum(1 for p in root.iter() for c in p
                                 if "Id" in c.attrib and id(c) not in pset and c.get("Id").lstrip().startswith("-"))
    return dev, r


def repairs(root):
    """Return (additions, recommended, repaired copy): the T11-MIN elements the fixture lacks."""
    fixed = copy.deepcopy(root)
    ls = fixed.find("LiveSet")
    adds, recs = [], []
    tracks = ls.find("Tracks")
    players = [t for t in (list(tracks) if tracks is not None else []) if t.tag in ("AudioTrack", "MidiTrack", "GroupTrack")]
    if not players:
        el = ET.fromstring(MIDI_TRACK)
        if tracks is None:
            insert_ordered(ls, el)
            adds.append({"what": "a MIDI track with empty session and freeze slot lists (T11-MIN MidiTrack skeleton)",
                         "insert": "/Ableton/LiveSet, before MainTrack", "xml": MIDI_TRACK})
        else:
            track = el[0]
            tracks.insert(0, track)
            adds.append({"what": "a MIDI track with empty session and freeze slot lists (T11-MIN MidiTrack skeleton)",
                         "insert": "/Ableton/LiveSet/Tracks, first item",
                         "xml": ET.tostring(track, encoding="unicode")})
        tracks = ls.find("Tracks")
    nslots = 0
    for t in list(tracks):
        if t.tag not in ("AudioTrack", "MidiTrack"):
            continue
        dc = t.find("DeviceChain")
        main = dc.findall("MainSequencer/ClipSlotList/ClipSlot") if dc is not None else []
        nslots = max(nslots, len(main))
        fs = dc.find("FreezeSequencer") if dc is not None else None
        have = len(fs.findall("ClipSlotList/ClipSlot")) if fs is not None else 0
        if have == len(main):
            continue
        missing = range(have, len(main))
        xml = "".join(FREEZE_SLOT.format(i=i) for i in missing)
        if fs is None:
            xml_full = f"<FreezeSequencer><ClipSlotList>{xml}</ClipSlotList></FreezeSequencer>"
            pos = list(dc).index(dc.find("MainSequencer")) + 1
            dc.insert(pos, ET.fromstring(xml_full))
            adds.append({"what": f"{len(main)} empty freeze slots (T11-MIN FreezeSequencer form)",
                         "insert": f"{t.tag}[@Id='{t.get('Id')}']/DeviceChain, after MainSequencer", "xml": xml_full})
        else:
            lst = fs.find("ClipSlotList")
            for s in ET.fromstring(f"<x>{xml}</x>"):
                lst.append(s)
            adds.append({"what": f"{len(missing)} more empty freeze slots",
                         "insert": f"{t.tag}[@Id='{t.get('Id')}']/DeviceChain/FreezeSequencer/ClipSlotList, at the end",
                         "xml": xml})
    nret = sum(1 for t in tracks if t.tag == "ReturnTrack") if tracks is not None else 0
    sp = ls.find("SendsPre")
    if sp is None and nret:
        xml = "<SendsPre>" + "".join(f'<SendPreBool Id="{i}" Value="false" />' for i in range(nret)) + "</SendsPre>"
        insert_ordered(ls, ET.fromstring(xml))
        recs.append({"what": f"SendsPre with {nret} item(s), as T11-MIN (removes REQ-013's unknown)",
                     "insert": "/Ableton/LiveSet, after PreHearTrack", "xml": xml})
    if nslots:  # recommended: every audio and MIDI track gets one session and one freeze slot per scene
        for t in list(tracks):
            if t.tag not in ("AudioTrack", "MidiTrack"):
                continue
            dc = t.find("DeviceChain")
            if dc is None:
                dc = ET.SubElement(t, "DeviceChain")
            for seq in ("MainSequencer", "FreezeSequencer"):
                el = dc.find(seq)
                have = len(el.findall("ClipSlotList/ClipSlot")) if el is not None else 0
                if have >= nslots:
                    continue
                xml = "".join(FREEZE_SLOT.format(i=i) for i in range(have, nslots))
                if el is None:
                    el = ET.fromstring(f"<{seq}><ClipSlotList /></{seq}>")
                    later = [i for i, c in enumerate(dc) if c.tag in ("FreezeSequencer", "DeviceChain")
                             and not (seq == "FreezeSequencer" and c.tag == "FreezeSequencer")]
                    dc.insert(later[0] if later else len(dc), el)
                lst = el.find("ClipSlotList")
                if lst is None:
                    lst = ET.SubElement(el, "ClipSlotList")
                for x in ET.fromstring(f"<x>{xml}</x>"):
                    lst.append(x)
                recs.append({"what": f"{nslots - have} empty slot(s) so that the track has one per scene",
                             "insert": f"{t.tag}[@Id='{t.get('Id')}']/DeviceChain/{seq}/ClipSlotList",
                             "xml": xml})
    sc = ls.find("Scenes")
    if nslots and sc is None:
        xml = "<Scenes>" + "".join(SCENE.format(i=i) for i in range(nslots)) + "</Scenes>"
        insert_ordered(ls, ET.fromstring(xml))
        recs.append({"what": f"{nslots} scene(s), one per slot, as T11-MIN (removes REQ-006's unknown)",
                     "insert": "/Ableton/LiveSet, after SendsPre or PreHearTrack", "xml": xml})
    return adds, recs, fixed


def case_effect(expected_outcome, action, refused):
    if not refused:
        return "consistent"
    if expected_outcome == "envelope-accepted":
        return "consistent: the case grades envelope acceptance only, which comes before these checks"
    if expected_outcome in OPENS or action == "open-call":  # open-call: the set must open before the call
        return "contradicted: the case expects the set to open; the traced rules refuse it"
    if expected_outcome == "refused":
        return ("outcome unchanged (refused), but the fixture does not isolate the rule under test: "
                "a candidate that missed that rule would still be refused")
    return f"unclassified outcome {expected_outcome!r}"


def main():
    schema = load_schema(sys.argv[1])
    LIVESET_ORDER.extend(schema["LiveSet"])
    hroot, out_path = sys.argv[2], sys.argv[3]
    releases = []
    totals = {"fixtures": 0, "live_sets": 0, "refused": 0, "cases_contradicted": 0, "cases_not_isolating": 0}
    for rel in sorted(d for d in os.listdir(hroot) if os.path.isdir(os.path.join(hroot, d))):
        rdir = os.path.join(hroot, rel)
        fdir = os.path.join(rdir, "fixtures")
        cases_path = os.path.join(rdir, "cases.json")
        if not os.path.isdir(fdir):
            continue
        cases = json.load(open(cases_path)) if os.path.exists(cases_path) else []
        cases = cases["cases"] if isinstance(cases, dict) else cases
        by_input = {}
        for c in cases:
            inp = c.get("input")
            if isinstance(inp, str):
                by_input.setdefault(os.path.normpath(inp), []).append(c)
        entries = []
        for dpath, _, files in sorted(os.walk(fdir)):
            for f in sorted(files):
                p = os.path.join(dpath, f)
                relp = os.path.relpath(p, rdir)
                root, kind = read(p)
                used = by_input.get(os.path.normpath(relp), [])
                e = {"fixture": relp, "kind": kind,
                     "cases": [{"id": c["id"], "action": c.get("action"), "expected": c.get("expected")} for c in used]}
                totals["fixtures"] += 1
                if root is not None:
                    totals["live_sets"] += 1
                    dev, r = measure(schema, root)
                    ref, unk = refusals(r, dev), unknowns(r)
                    e["refused_by_traced_rules"] = bool(ref)
                    e["refusals"] = ref
                    e["unknown_shapes"] = unk
                    adds, recs, fixed = repairs(root) if (ref or unk) else ([], [], None)
                    if ref:
                        totals["refused"] += 1
                        e["minimal_addition"] = adds
                    if recs:
                        e["recommended_addition"] = recs
                    if fixed is not None:
                        dev2, r2 = measure(schema, fixed)
                        e["after_additions"] = {"refusals": refusals(r2, dev2), "unknown_shapes": unknowns(r2),
                                                "new_schema_deviations": sorted(set(dev2) - set(dev))}
                    for c in e["cases"]:
                        out = (c["expected"] or {}).get("outcome")
                        c["effect"] = case_effect(out, c.get("action"), bool(ref))
                        totals["cases_contradicted"] += c["effect"].startswith("contradicted")
                        totals["cases_not_isolating"] += c["effect"].startswith("outcome unchanged")
                elif kind.startswith("unparseable"):
                    for c in e["cases"]:
                        c["effect"] = "not evaluated: the file is deliberately not well-formed"
                else:
                    for c in e["cases"]:
                        c["effect"] = "not evaluated: not a Live Set document"
                entries.append(e)
        summary = {"fixtures": len(entries),
                   "live_sets": sum(1 for x in entries if x["kind"] == "live-set"),
                   "refused": sum(1 for x in entries if x.get("refused_by_traced_rules")),
                   "cases_contradicted": sorted(c["id"] for x in entries for c in x["cases"]
                                                if c.get("effect", "").startswith("contradicted")),
                   "cases_not_isolating": sorted(c["id"] for x in entries for c in x["cases"]
                                                 if c.get("effect", "").startswith("outcome unchanged")),
                   "with_unknown_shapes": sum(1 for x in entries if x.get("unknown_shapes"))}
        releases.append({"release": rel, "summary": summary, "fixtures": entries})
    doc = {
        "id": "T11-RELEASED-FIXTURE-AUDIT",
        "spec": "SPEC-LIVE-SET-STRUCTURE revision 1 (A1, A2, A3 settled statically; A5 still an assumption)",
        "method": __doc__.strip(),
        "basis": {"REQ-002, REQ-006": "validation walk, run by the XML reader's load step on every open (A1 settled)",
                  "REQ-006 freeze count": "the freeze sequencer is constructed with an empty slot list and no load step adds slots (A2 settled)",
                  "REQ-013, REQ-015 NextPointeeId": "root post-load step, enabled by the reading context's flag, which the XML reader's context sets (A1 settled)",
                  "REQ-015 Id 0": "member post-load step; preset exemption not set on the set-open path (A3 settled)",
                  "REQ-016": "generic list loader (S-cond A5)"},
        "totals": totals,
        "releases": releases,
    }
    json.dump(doc, open(out_path, "w"), indent=1)
    open(out_path, "a").write("\n")
    print(json.dumps(totals))
    for r in releases:
        s = r["summary"]
        print(r["release"], s["fixtures"], s["live_sets"], s["refused"], len(s["cases_contradicted"]),
              len(s["cases_not_isolating"]), s["with_unknown_shapes"])


if __name__ == "__main__":
    main()
