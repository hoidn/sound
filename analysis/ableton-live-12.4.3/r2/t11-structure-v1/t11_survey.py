"""T1.1 static survey: Live Set structure in the 12.4.3 bundle's schema and shipped documents.

Usage: python3 -I t11_survey.py <bundle Contents dir> <out dir>
Read-only on inputs; writes <out>/schema.json, <out>/documents.json, <out>/inputs-documents.tsv.
Documents: every non-AppleDouble .als and .alc under Contents/App-Resources (gzip XML).
Shipped documents are evidence only: nothing from them is copied into a fixture.
Measures, per document kind (.als set, .alc clip file):
  LiveSet child order and presence; track lists (types, order, Ids, names, colours);
  scenes and clip slots (counts, Ids, empty-slot forms, scene fields); clip children order;
  sample references (FileRef / SampleRef values); SendsPre and send holders versus returns;
  routing targets; device-chain placement of the seven bundled devices; every element with
  an Id attribute (pointee tags versus list items, uniqueness, relation to NextPointeeId);
  envelope target resolution by track type.
"""
import collections, gzip, hashlib, json, os, re, sys
import xml.etree.ElementTree as ET

TRACKS = ("AudioTrack", "MidiTrack", "GroupTrack", "ReturnTrack")
SEVEN = ("Amp", "Cabinet", "UltraAnalog", "StringStudio", "Collision", "LoungeLizard", "Corpus")
C = collections.Counter


def sha(b):
    return hashlib.sha256(b).hexdigest()


def schema_part(sdir):
    root = ET.parse(os.path.join(sdir, "12.0_12402.txt")).getroot()
    want = ("LiveSet", "AudioTrack", "MidiTrack", "GroupTrack", "ReturnTrack", "MainTrack", "PreHearTrack",
            "AudioTrackDeviceChain", "MidiTrackDeviceChain", "GroupTrackDeviceChain", "SendTrackDeviceChain",
            "MainTrackDeviceChain", "PreHearTrackDeviceChain", "AudioToAudioDeviceChain", "MidiToAudioDeviceChain",
            "MidiToMidiDeviceChain", "AudioSequencer", "MidiSequencer", "ClipSlot", "GroupTrackSlot", "Scene",
            "FileRef", "SampleRef", "AudioClip", "MidiClip", "DeviceChainContainerName", "RemoteableDocumentColor",
            "TrackSendHolder", "Routable", "Pointee", "AutomationTarget", "TimeableAutomationTarget",
            "TimeableModulationTarget", "UserFloatModulationTarget", "Loop")
    out = {"attrs": dict(root.attrib), "classes": {}}
    for c in want:
        e = root.find(c)
        if e is not None:
            out["classes"][c] = {"attrib": dict(e.attrib),
                                 "fields": [[f.tag, f.get("Class"), f.get("Type")] + ([f.get("InternalName")] if f.get("InternalName") else []) for f in e]}
    # classes that declare a Pointee member or are pointee-like by name
    out["classes_with_pointee_member"] = sorted(e.tag for e in root if any(f.get("Class") == "Pointee" for f in e))
    return out


def text(e, p):
    x = e.find(p)
    return None if x is None else x.get("Value")


def doc_part(path, kind, acc):
    raw = open(path, "rb").read()
    xml = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
    root = ET.fromstring(xml)
    ls = root.find("LiveSet")
    acc["n"] += 1
    acc["minor"][root.get("MinorVersion")] += 1
    acc["children_seq"][tuple(c.tag for c in ls)] += 1
    for c in ls:
        acc["child_presence"][c.tag] += 1
    tracks = list(ls.find("Tracks"))
    types = [t.tag for t in tracks]
    acc["track_counts"][tuple(C(types).get(k, 0) for k in TRACKS)] += 1
    for t in types:
        acc["track_tag"][t] += 1
    seen_ret = False
    order_ok = True
    for t in types:
        if t == "ReturnTrack":
            seen_ret = True
        elif seen_ret:
            order_ok = False
    acc["returns_last"][order_ok] += 1
    ids = [t.get("Id") for t in tracks]
    acc["track_ids_unique"][len(ids) == len(set(ids))] += 1
    acc["track_id_none"][sum(i is None for i in ids)] += 1
    for k in ("MainTrack", "PreHearTrack"):
        e = ls.find(k)
        acc["special_present"][(k, e is not None, None if e is None else e.get("Id"))] += 1
        if e is not None:
            acc["special_names"][(k, text(e, "Name/EffectiveName"), text(e, "Name/UserName"))] += 1
            acc["special_color"][(k, text(e, "Color"))] += 1
            acc["special_children"][(k, tuple(c.tag for c in e))] += 1
    nret = types.count("ReturnTrack")
    scenes = list(ls.find("Scenes")) if ls.find("Scenes") is not None else []
    acc["scene_count"][len(scenes)] += 1
    acc["scene_ids_seq"][tuple(s.get("Id") for s in scenes) == tuple(str(i) for i in range(len(scenes)))] += 1
    for s in scenes:
        acc["scene_children"][tuple(c.tag for c in s)] += 1
        acc["scene_name_empty"][text(s, "Name") == ""] += 1
        acc["scene_tempo"][(text(s, "Tempo"), text(s, "IsTempoEnabled"))] += 1
        acc["scene_tsig"][(text(s, "TimeSignatureId"), text(s, "IsTimeSignatureEnabled"))] += 1
        acc["scene_color"][text(s, "Color")] += 1
    sp = ls.find("SendsPre")
    spn = [] if sp is None else list(sp)
    acc["sendspre_vs_returns"][(len(spn) == nret, tuple(sorted(C(x.tag for x in spn).items())))] += 1
    acc["sendspre_ids_seq"][tuple(x.get("Id") for x in spn) == tuple(str(i) for i in range(len(spn)))] += 1
    for x in spn:
        acc["sendspre_values"][x.get("Value")] += 1
    for t in tracks + [e for e in (ls.find("MainTrack"), ls.find("PreHearTrack")) if e is not None]:
        tag = t.tag
        acc["name_form"][(tag, text(t, "Name/UserName") == "", bool(text(t, "Name/EffectiveName")))] += 1
        col = text(t, "Color")
        acc["color_values"][(tag, None if col is None else int(col) if col.lstrip("-").isdigit() else col)] += 1
        dc = t.find("DeviceChain")
        acc["chain_children"][(tag, tuple(c.tag for c in dc))] += 1
        for r in ("AudioInputRouting", "AudioOutputRouting", "MidiInputRouting", "MidiOutputRouting"):
            v = text(dc, f"{r}/Target")
            v = re.sub(r"\d+", "N", v) if v else v
            acc["routing"][(tag, r, v)] += 1
        holders = dc.findall("Mixer/Sends/TrackSendHolder")
        acc["holders_vs_returns"][(tag, len(holders) - nret)] += 1
        ms = dc.find("MainSequencer")
        if ms is not None and ms.find("ClipSlotList") is not None:
            slots = list(ms.find("ClipSlotList"))
            acc["slots_minus_scenes"][(tag, len(slots) - len(scenes))] += 1
            acc["slot_ids_seq"][tuple(s.get("Id") for s in slots) == tuple(str(i) for i in range(len(slots)))] += 1
            for s in slots:
                acc["slot_tag"][s.tag] += 1
                acc["slot_children"][tuple(c.tag for c in s)] += 1
                v = s.find("ClipSlot/Value")
                content = tuple(c.tag for c in v) if v is not None else ("<no Value>",)
                acc["slot_content"][(tag, content)] += 1
                for clip in (v if v is not None else []):
                    acc["clip_attrs"][(clip.tag, tuple(sorted(clip.attrib)))] += 1
                    acc["clip_children"][(clip.tag, tuple(c.tag for c in clip))] += 1
                    if clip.tag == "AudioClip":
                        sample_ref(clip, acc, kind)
        elif tag in ("AudioTrack", "MidiTrack"):
            acc["slots_minus_scenes"][(tag, "no ClipSlotList")] += 1
        if tag == "GroupTrack":
            gs = t.find("Slots")
            acc["group_slots_minus_scenes"][None if gs is None else len(list(gs)) - len(scenes)] += 1
        inner = dc.find("DeviceChain/Devices")
        if inner is not None:
            acc["chain_devices"][(tag, tuple(d.tag for d in inner))] += 1
        acc["envelopes"][(tag, len(t.findall("AutomationEnvelopes/Envelopes/AutomationEnvelope")))] += 1
    for t in [t for t in tracks if t.tag == "GroupTrack" or t.find("TrackGroupId") is not None]:
        acc["track_group_id"][(t.tag, text(t, "TrackGroupId") == "-1")] += 1
    # device placement: path of each of the seven devices
    parent = {c: p for p in root.iter() for c in p}
    for e in root.iter():
        if e.tag in SEVEN:
            p, chain = e, []
            while p in parent:
                p = parent[p]
                chain.append(p.tag)
            acc["seven_paths"][(kind, e.tag, "/".join(reversed(chain[:8])))] += 1
            acc["seven_attrs"][(e.tag, tuple(sorted(e.attrib)))] += 1
    # Ids
    npid = int(ls.find("NextPointeeId").get("Value")) if ls.find("NextPointeeId") is not None else None
    by_tag = collections.defaultdict(list)
    for e in root.iter():
        if "Id" in e.attrib:
            by_tag[e.tag].append(int(e.get("Id")))
    pointee_tags = [t for t in by_tag if t in ("Pointee", "AutomationTarget", "ModulationTarget") or t.endswith("ModulationTarget") or t.startswith("ControllerTargets.")]
    allp = [i for t in pointee_tags for i in by_tag[t]]
    nz = [i for i in allp if i != 0]
    acc["pointee_tags"].update({t: len(by_tag[t]) for t in pointee_tags})
    acc["pointee_unique_nonzero"][len(nz) == len(set(nz))] += 1
    acc["pointee_zero_count"][sum(1 for i in allp if i == 0)] += 1
    acc["pointee_below_next"][(npid is not None) and all(i < npid for i in allp)] += 1
    if npid is not None and allp:
        acc["next_minus_max"].append(npid - max(allp))
        acc["pointee_min"].append(min(allp))
    # are any list-item Ids (other tags) equal to pointee Ids? (informational)
    other = {t: v for t, v in by_tag.items() if t not in pointee_tags}
    acc["id_tags_other"].update({t: len(v) for t, v in other.items()})
    # list items: unique within their parent list
    for p in root.iter():
        kids = [c for c in p if "Id" in c.attrib and c.tag not in pointee_tags]
        if len(kids) > 1:
            v = [c.get("Id") for c in kids]
            acc["list_ids_unique"][(len(v) == len(set(v)))] += 1
            if len(v) != len(set(v)):
                acc["list_ids_dup_parents"][p.tag] += 1
    # envelope target resolution
    tgt = {}
    for e in root.iter():
        if e.tag in pointee_tags:
            tgt[e.get("Id")] = e.tag
    for env in root.iter("AutomationEnvelope"):
        pid = env.find("EnvelopeTarget/PointeeId").get("Value")
        acc["env_target_tag"][tgt.get(pid, "<unresolved>")] += 1


def sample_ref(clip, acc, kind):
    sr = clip.find("SampleRef")
    if sr is None:
        acc["sampleref"][("absent",)] += 1
        return
    acc["sampleref_children"][tuple(c.tag for c in sr)] += 1
    fr = sr.find("FileRef")
    acc["fileref_children"][tuple(c.tag for c in fr)] += 1
    rpt, rp, p, ty = text(fr, "RelativePathType"), text(fr, "RelativePath"), text(fr, "Path"), text(fr, "Type")
    acc["fileref_kind"][(kind, rpt, ty, bool(rp), (p or "")[:1], text(fr, "LivePackName") != "")] += 1
    acc["fileref_rp_prefix"][(rpt, "/".join((rp or "").split("/")[:2]) if rpt != "3" else (rp or "").split("/")[0])] += 1
    acc["fileref_path_prefix"][(rpt, "/".join((p or "").split("/")[:4]))] += 1
    acc["fileref_ext"][os.path.splitext(p or rp or "")[1].lower()] += 1
    acc["fileref_size_crc"][(text(fr, "OriginalFileSize") not in (None, "0"), text(fr, "OriginalCrc") not in (None, "0"))] += 1
    acc["fileref_sourcehint"][bool(text(fr, "SourceHint"))] += 1
    acc["sampleref_rate"][text(sr, "DefaultSampleRate")] += 1
    acc["sampleref_duration_zero"][text(sr, "DefaultDuration") in ("0", None)] += 1
    acc["sampleref_lastmod_zero"][text(sr, "LastModDate") in ("0", None)] += 1


def keyed(c):
    return [[list(k) if isinstance(k, tuple) else k, v] for k, v in sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0])))]


def main():
    contents, out = sys.argv[1], sys.argv[2]
    res = os.path.join(contents, "App-Resources")
    os.makedirs(out, exist_ok=True)
    json.dump(schema_part(os.path.join(res, "Schema")), open(os.path.join(out, "schema.json"), "w"), indent=1)
    files = sorted(os.path.join(d, f) for d, _, fs in os.walk(res) for f in fs
                   if f.endswith((".als", ".alc")) and not f.startswith("._"))
    result = {}
    rows = []
    for kind in (".als", ".alc"):
        acc = collections.defaultdict(C)
        acc["n"] = 0
        acc["next_minus_max"], acc["pointee_min"] = [], []
        for f in (x for x in files if x.endswith(kind)):
            b = open(f, "rb").read()
            rows.append(f"{sha(b)}\t{len(b)}\t{os.path.relpath(f, contents)}")
            doc_part(f, kind, acc)
        r = {}
        for k, v in acc.items():
            if isinstance(v, C):
                r[k] = keyed(v)
            elif isinstance(v, list):
                r[k] = {"min": min(v), "max": max(v), "n": len(v)} if v else {}
            else:
                r[k] = v
        result[kind] = r
    json.dump(result, open(os.path.join(out, "documents.json"), "w"), indent=1)
    open(os.path.join(out, "inputs-documents.tsv"), "w").write("\n".join(rows) + "\n")


if __name__ == "__main__":
    main()
