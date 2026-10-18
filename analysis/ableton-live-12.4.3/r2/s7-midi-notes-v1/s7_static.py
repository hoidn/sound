"""S7 static half: MIDI note storage in Live's shipped schemas and documents (analyst tool; output is data).

Usage: python3 -I s7_static.py <bundle Contents dir> <out.json> <inputs.tsv>
Read-only on inputs. Schema part: every non-AppleDouble App-Resources/Schema/*.txt, ordered by
(major, minor, number) from the file name (presentation order, not proven migration order); field
lists of the note classes as contiguous evolution segments. Document part: every non-AppleDouble
*.als, *.alc and *.agr below Contents (gzip or plain XML; AB1E binary files are counted, not parsed);
every MidiClip with notes: MidiNoteEvent attribute shapes, value domains, ordering, overlaps, NoteId
and NextId relations, KeyTrack ids and keys, per-note expression lists, probability groups, the
1/3,843,840 time grid, and the save number-format rule derived in n1-transport-state-v1.
inputs.tsv: sha256, bytes, kind (gzip/xml/ab1e), relative path of each document read.
"""
import collections, gzip, hashlib, json, math, os, re, struct, sys
import xml.etree.ElementTree as ET

CLASSES = ["MidiNotes", "KeyTrack", "MidiNoteEvent", "NoteIdGenerator", "NoteProbabilityGroup", "NoteId",
           "PerNoteEventStore", "PerNoteEventList", "PerNoteEvent"]
NOTE_ATTRS = ["Time", "Duration", "Velocity", "VelocityDeviation", "OffVelocity", "Probability", "IsEnabled", "NoteId"]
PNE_ATTRS = ["TimeOffset", "Value", "CurveControl1X", "CurveControl1Y", "CurveControl2X", "CurveControl2Y"]
DOUBLE = {"Time", "Duration", "TimeOffset", "CurveControl1X", "CurveControl1Y", "CurveControl2X", "CurveControl2Y"}
FLOAT = {"Velocity", "VelocityDeviation", "OffVelocity", "Probability", "Value"}
GRID = 3843840.0
HALF = 2.6015651015651016e-07 * 0.5  # constant 0x3e9175746e8cba40 times 0.5, as in FUN_1028e2e24


def vkey(name):
    m = re.fullmatch(r"(\d+)\.(\d+)_(\d+)\.txt", name)
    if not m:
        raise ValueError(f"unexpected schema file name {name!r}")
    return tuple(int(x) for x in m.groups())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def fmt(x, p, pzero):
    """Writer text rule from n1-transport-state-v1 (FUN_101431584 / FUN_101431788)."""
    if x == 0:
        prec = pzero
    else:
        e = math.log10(abs(x))
        prec = max(0, p - (math.floor(e) if e < 0 else math.ceil(e)))
    s = "%.*f" % (prec, x)
    return s.rstrip("0").rstrip(".") if "." in s else s


def f32(t):
    return struct.unpack("<f", struct.pack("<f", float(t)))[0]


def quantize(t):
    """Load-time time quantization of FUN_1028e2e24 / FUN_1025c7a0c (special sentinels not handled here)."""
    s = 1.0 if t >= 0 else -1.0
    return s * (math.floor(abs(t + s * HALF) * GRID) / GRID)


def schema_part(sdir):
    files = sorted((f for f in os.listdir(sdir) if f.endswith(".txt") and not f.startswith("._")), key=vkey)
    segs, versions = {c: [] for c in CLASSES + ["MidiClip.Notes"]}, []
    for f in files:
        raw = open(os.path.join(sdir, f), "rb").read()
        root, v = ET.fromstring(raw), f[:-4]
        versions.append({"version": v, "sha256": sha(raw)})
        for c in CLASSES + ["MidiClip.Notes"]:
            cls, _, fld = c.partition(".")
            el = root.find(cls)
            sig = None if el is None else [
                {k: x.get(k) for k in ("Class", "Type", "ArrayTranslator") if x.get(k) is not None} | {"field": x.tag}
                for x in el if not fld or x.tag == fld]
            if segs[c] and segs[c][-1]["fields"] == sig:
                segs[c][-1].update(last=v, count=segs[c][-1]["count"] + 1)
            else:
                segs[c].append({"first": v, "last": v, "count": 1, "fields": sig})
    latest = ET.fromstring(open(os.path.join(sdir, files[-1]), "rb").read())
    translators = sorted(f"{c.tag}.{x.tag}={x.get('ArrayTranslator')}" for c in latest for x in c if x.get("ArrayTranslator"))
    return {"files": len(files), "versions": versions, "segments": segs, "array_translators_latest": translators}


class Stats:
    def __init__(self):
        self.n, self.vals = 0, collections.Counter()

    def add(self, text):
        self.n += 1
        self.vals[text] += 1

    def out(self):
        nums = [float(v) for v in self.vals if re.fullmatch(r"-?[0-9.eE+-]+", v)]
        ints = sum(c for v, c in self.vals.items() if re.fullmatch(r"-?\d+", v))
        return {"count": self.n, "distinct": len(self.vals), "integer_text": ints,
                "min": min(nums) if nums else None, "max": max(nums) if nums else None,
                "top": self.vals.most_common(12)}


def read_doc(path):
    raw = open(path, "rb").read()
    if raw[:2] == b"\x1f\x8b":
        return raw, "gzip", gzip.decompress(raw)
    if raw[:4] == b"AB1E" or raw.lstrip()[:1] != b"<":
        return raw, "ab1e", None
    return raw, "xml", raw


def clip_records(root, rel, kind):
    """Yield (context, MidiClip element, Notes element) for every MidiClip with a MidiNotes child."""
    ab = root if root.tag == "Ableton" else None
    meta = (ab.get("MinorVersion"), ab.get("Creator")) if ab is not None else (None, None)
    for clip in root.iter("MidiClip"):
        notes = clip.find("Notes")
        if notes is not None and notes.find("KeyTracks") is not None:
            yield {"doc": rel, "type": kind, "minor": meta[0], "creator": meta[1]}, clip, notes


def survey_clip(ctx, clip, notes, acc):
    c = acc["checks"]
    g = f'{ctx["type"]}|{ctx["minor"]}|{ctx["creator"]}'
    ex = lambda k, *v: acc["examples"].setdefault(k, []).append([ctx["doc"], *v]) if len(acc["examples"].get(k, [])) < 5 else None
    acc["midinotes_child_orders"][(g,) + tuple(x.tag for x in notes)] += 1
    nextid = notes.find("NoteIdGenerator/NextId")
    pnext = notes.find("ProbabilityGroupIdGenerator/NextId")
    loop = clip.find("Loop")
    lstart = float(loop.find("LoopStart").get("Value")) if loop is not None else None
    lend = float(loop.find("LoopEnd").get("Value")) if loop is not None else None
    ids, keys, kt_ids, note_dur = [], [], [], {}
    for kt in notes.find("KeyTracks"):
        if kt.tag != "KeyTrack":
            acc["unexpected"].append([ctx["doc"], "KeyTracks child", kt.tag])
            continue
        acc["keytrack_attr_sets"][tuple(kt.keys())] += 1
        acc["keytrack_child_orders"][tuple(x.tag for x in kt)] += 1
        key = int(kt.find("MidiKey").get("Value"))
        keys.append(key)
        kt_ids.append(int(kt.get("Id")))
        acc["midikey"].add(str(key))
        evs = list(kt.find("Notes"))
        c["keytracks"] += 1
        c["keytracks_empty"] += not evs
        prev = None
        for ev in evs:
            if ev.tag != "MidiNoteEvent":
                acc["unexpected"].append([ctx["doc"], "Notes child", ev.tag])
                continue
            c["notes"] += 1
            a = ev.attrib
            acc["note_attr_orders"][(g,) + tuple(a)] += 1
            if list(a) != [k for k in NOTE_ATTRS if k in a]:
                ex("note_attr_order_not_schema", key, list(a))
            for k in ("VelocityDeviation", "Probability", "IsEnabled"):
                if k in a:
                    acc["optional_attr_values"][(g, k, a[k])] += 1
            for k, v in a.items():
                acc["note_values"].setdefault(k, Stats()).add(v)
                if k in DOUBLE:
                    c["fmt_ok" if fmt(float(v), 17, 16) == v else "fmt_bad"] += 1
                    c["fmt_17g_differs"] += fmt(float(v), 17, 16) == v and "%.17g" % float(v) != v
                elif k in FLOAT:
                    c["fmt_ok" if fmt(f32(v), 9, 8) == v else "fmt_bad"] += 1
            t, d = float(a["Time"]), float(a["Duration"])
            c["time_on_grid"] += quantize(t) == t
            c["duration_on_grid"] += quantize(d) == d
            c["time_negative"] += t < 0
            c["duration_nonpositive"] += d <= 0
            if t < 0:
                ex("time_negative", key, a["Time"])
            if d <= 0:
                ex("duration_nonpositive", key, a["Time"], a["Duration"])
            if lstart is not None:
                c["time_before_loopstart"] += t < lstart
                c["time_at_or_after_loopend"] += t >= lend
            vel = float(a["Velocity"])
            c["velocity_outside_1_127"] += not 1 <= vel <= 127
            c["velocity_fractional"] += vel != int(vel)
            if "OffVelocity" in a:
                c["offvelocity_outside_0_127"] += not 0 <= float(a["OffVelocity"]) <= 127
            if "Probability" in a:
                c["probability_outside_0_1"] += not 0 <= float(a["Probability"]) <= 1
                c["probability_present_equal_1"] += float(a["Probability"]) == 1
            if "VelocityDeviation" in a:
                c["veldev_present_equal_0"] += float(a["VelocityDeviation"]) == 0
            if "IsEnabled" in a:
                c["isenabled_present_true"] += a["IsEnabled"] == "true"
            if "NoteId" in a:
                ids.append(int(a["NoteId"]))
                note_dur[int(a["NoteId"])] = d
            if prev is not None:
                pt, pd = prev
                c["order_time_decreasing"] += t < pt
                c["order_time_equal"] += t == pt
                c["overlap_same_key"] += t < pt + pd and t >= pt
                if t < pt + pd and t >= pt:
                    ex("overlap_same_key", key, pt, pd, t)
                    acc["overlap_by_group"][g] += 1
            prev = (t, d)
    c["clips"] += 1
    c["clips_without_noteids"] += not ids
    c["keytrack_ids_not_unique"] += len(set(kt_ids)) != len(kt_ids)
    c["midikeys_not_unique"] += len(set(keys)) != len(keys)
    c["keytracks_sorted_by_key"] += keys == sorted(keys)
    c["keytracks_sorted_by_id"] += kt_ids == sorted(kt_ids)
    c["noteids_not_unique"] += len(set(ids)) != len(ids)
    c["noteid_zero"] += ids.count(0)
    if nextid is not None and ids:
        n = int(nextid.get("Value"))
        rel = "nextid_eq_max_plus_1" if n == max(ids) + 1 else "nextid_gt_max_plus_1" if n > max(ids) + 1 else "nextid_le_max"
        c[rel] += 1
        acc["nextid_gap"][n - max(ids) - 1] += 1
    elif nextid is not None:
        acc["nextid_without_notes"][nextid.get("Value")] += 1
    if pnext is not None:
        acc["probability_group_nextid"][pnext.get("Value")] += 1
    pg = notes.find("NoteProbabilityGroups")
    acc["probability_groups"][0 if pg is None else len(pg)] += 1
    store = notes.find("PerNoteEventStore/EventLists")
    seen = set()
    for pl in (store if store is not None else []):
        c["pne_lists"] += 1
        acc["pne_list_attr_orders"][tuple(pl.attrib)] += 1
        nid, cc = int(pl.get("NoteId")), int(pl.get("CC"))
        acc["pne_cc"][cc] += 1
        c["pne_list_orphan"] += nid not in note_dur
        c["pne_list_dup_noteid_cc"] += (nid, cc) in seen
        seen.add((nid, cc))
        prev = None
        for pe in pl.find("Events"):
            c["pne_events"] += 1
            a = pe.attrib
            acc["pne_attr_orders"][tuple(a)] += 1
            for k, v in a.items():
                acc["pne_values"].setdefault(f"{k}@CC{cc}" if k == "Value" else k, Stats()).add(v)
                ok = fmt(float(v), 17, 16) == v if k in DOUBLE else fmt(f32(v), 9, 8) == v
                c["fmt_ok" if ok else "fmt_bad"] += 1
                if k.startswith("Curve"):
                    c["pne_curve_present_equal_half"] += float(v) == 0.5
            to = float(a["TimeOffset"])
            c["pne_timeoffset_on_grid"] += quantize(to) == to
            c["pne_timeoffset_negative"] += to < 0
            c["pne_timeoffset_beyond_note_duration"] += nid in note_dur and to > note_dur[nid]
            if prev is not None:
                c["pne_order_decreasing"] += to < prev
                c["pne_order_equal"] += to == prev
                if to == prev:
                    ex("pne_order_equal", nid, cc, to)
            prev = to
    return ids


def documents_part(contents):
    acc = {"checks": collections.Counter(), "unexpected": [], "midinotes_child_orders": collections.Counter(),
           "keytrack_attr_sets": collections.Counter(), "keytrack_child_orders": collections.Counter(),
           "note_attr_orders": collections.Counter(), "note_values": {}, "midikey": Stats(),
           "nextid_gap": collections.Counter(), "nextid_without_notes": collections.Counter(),
           "probability_group_nextid": collections.Counter(), "probability_groups": collections.Counter(),
           "pne_list_attr_orders": collections.Counter(), "pne_cc": collections.Counter(),
           "pne_attr_orders": collections.Counter(), "pne_values": {}, "examples": {},
           "optional_attr_values": collections.Counter(), "overlap_by_group": collections.Counter()}
    inputs, kinds, groups, per_doc = [], collections.Counter(), collections.Counter(), []
    for d, dirs, files in os.walk(contents):
        dirs.sort()
        for f in sorted(files):
            if f.startswith("._") or not f.endswith((".als", ".alc", ".agr")):
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, contents)
            raw, kind, xml = read_doc(p)
            inputs.append((sha(raw), len(raw), kind, rel))
            kinds[(f.rsplit(".", 1)[1], kind)] += 1
            if xml is None:
                continue
            root = ET.fromstring(xml)
            for ctx, clip, notes in clip_records(root, rel, f.rsplit(".", 1)[1]):
                groups[(ctx["type"], ctx["minor"], ctx["creator"])] += 1
                ids = survey_clip(ctx, clip, notes, acc)
                per_doc.append([rel, len(ids)])
    out = {k: (v.out() if isinstance(v, Stats) else v) for k, v in acc.items()}
    out["note_values"] = {k: v.out() for k, v in sorted(acc["note_values"].items())}
    out["pne_values"] = {k: v.out() for k, v in sorted(acc["pne_values"].items())}
    for k in ("midinotes_child_orders", "keytrack_attr_sets", "keytrack_child_orders", "note_attr_orders",
              "pne_list_attr_orders", "pne_attr_orders"):
        out[k] = sorted([list(t), n] for t, n in acc[k].items())
    for k in ("nextid_gap", "nextid_without_notes", "probability_group_nextid", "probability_groups", "pne_cc",
              "optional_attr_values", "overlap_by_group"):
        out[k] = sorted([str(t), n] for t, n in acc[k].items())
    out["checks"] = dict(sorted(acc["checks"].items()))
    order_ok = sum(n for t, n in acc["note_attr_orders"].items()
                   if list(t[1:]) == [a for a in NOTE_ATTRS if a in t])
    out["checks"]["note_attr_order_is_schema_subsequence"] = order_ok
    out["document_kinds"] = sorted([list(k), n] for k, n in kinds.items())
    out["clip_groups"] = sorted([list(k), n] for k, n in groups.items())
    out["clips_by_document"] = per_doc
    return out, inputs


def main(contents, out_json, out_tsv):
    sdir = os.path.join(contents, "App-Resources", "Schema")
    docs, inputs = documents_part(contents)
    result = {"schema": schema_part(sdir), "documents": docs,
              "rules": {"grid": GRID, "half_step": HALF, "number_format": "n1-transport-state-v1 fmt(P=17|9)"}}
    with open(out_json, "w") as o:
        json.dump(result, o, indent=1, sort_keys=True)
        o.write("\n")
    with open(out_tsv, "w") as o:
        for row in sorted(inputs, key=lambda r: r[3]):
            o.write("\t".join(map(str, row)) + "\n")


if __name__ == "__main__":
    assert fmt(0.359923670079920099, 17, 16) == "0.359923670079920099" and quantize(0.25) == 0.25
    main(*sys.argv[1:4])
