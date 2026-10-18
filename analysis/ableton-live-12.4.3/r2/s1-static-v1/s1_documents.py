"""S1 static half: transport-state values in shipped Live documents.

Usage: python3 -I s1_documents.py <bundle Contents dir> <Schema dir> <out.json> <inputs.tsv>
Walks Contents for *.als/.alc/.adv/.adg/.agr/.alp, skips AppleDouble '._*'
files (checking their 00051607 magic), gunzips (or reads plain XML) and parses
the rest,
censuses every element path ending in a transport-related tag, and extracts
transport, main-track tempo/time-signature, tempo automation and scene values
from documents whose root holds a LiveSet. Read-only on inputs.
inputs.tsv lists sha256, size, gzip flag, parsed-as-XML flag and relative path of
every non-AppleDouble file read.
"""
import collections, gzip, hashlib, json, math, multiprocessing, os, re, struct, sys
import xml.etree.ElementTree as ET

EXTS = {".als", ".alc", ".adv", ".adg", ".agr", ".alp"}
TAGS = {"Transport", "Tempo", "TimeSignature", "LoopOn", "LoopStart", "LoopLength",
        "CurrentTime", "PhaseNudgeTempo", "TimeSignatureId", "IsTempoEnabled",
        "IsTimeSignatureEnabled", "SavedTempo", "TempoControl", "MainTrack", "MasterTrack"}
APPLEDOUBLE = bytes.fromhex("00051607")


def census(el, path, out):
    for c in el:
        p = f"{path}/{c.tag}"
        if c.tag in TAGS:
            out[p] += 1
        census(c, p, out)


def val(el, sub, attr="Value"):
    x = el.find(sub) if el is not None else None
    return None if x is None else x.get(attr)


def liveset(ls):
    """Extract S1 fields from an /Ableton/LiveSet element."""
    rec = {}
    tr = ls.find("Transport")
    rec["transport"] = None if tr is None else [
        [c.tag, dict(c.attrib), [g.tag for g in c]] for c in tr]
    track = next((t for t in (ls.find("MainTrack"), ls.find("MasterTrack")) if t is not None), None)
    rec["track_tag"] = None if track is None else track.tag
    rec["main_mixer_children"] = None
    mixer = None
    if track is not None:
        mixer = next((m for m in (track.find("DeviceChain/Mixer"), track.find("MasterChain/Mixer"))
                      if m is not None), None)
    if mixer is not None:
        rec["main_mixer_children"] = [c.tag for c in mixer]
    for key in ("Tempo", "TimeSignature"):
        el = None if mixer is None else mixer.find(key)
        rec[key] = None if el is None else {
            "children": [c.tag for c in el], "manual": val(el, "Manual"),
            "range": [val(el, "MidiControllerRange/Min"), val(el, "MidiControllerRange/Max")],
            "automation_id": val(el, "AutomationTarget", "Id"),
            "modulation_id": val(el, "ModulationTarget", "Id")}
    ids = {(rec[k] or {}).get("automation_id"): k for k in ("Tempo", "TimeSignature")}
    envs = {}  # only envelopes targeting tempo or time signature
    for env in ([] if track is None else track.findall("AutomationEnvelopes/Envelopes/AutomationEnvelope")):
        key = ids.get(val(env, "EnvelopeTarget/PointeeId"))
        if key:
            envs[key] = [[e.tag, e.get("Time"), e.get("Value")] for e in env.findall("Automation/Events/*")]
    rec["envelopes"] = envs
    rec["scenes"] = [[val(s, "Tempo"), val(s, "IsTempoEnabled"), val(s, "TimeSignatureId"),
                      val(s, "IsTimeSignatureEnabled")] for s in ls.findall("Scenes/Scene")]
    scenes = ls.findall("Scenes/Scene")
    tracks = ls.find("Tracks")
    slot_sigs = {}  # scenes with an enabled time signature -> clip signatures in that slot row
    for i, sc in enumerate(scenes):
        if val(sc, "IsTimeSignatureEnabled") != "true":
            continue
        c = collections.Counter()
        for tr in ([] if tracks is None else tracks):
            slots = tr.findall("DeviceChain/MainSequencer/ClipSlotList/ClipSlot")
            for r in (slots[i].iter("RemoteableTimeSignature") if i < len(slots) else []):
                c[f"{val(r, 'Numerator')}/{val(r, 'Denominator')}"] += 1
        slot_sigs[i] = [val(sc, "TimeSignatureId"), dict(c)]
    rec["scene_slot_signatures"] = slot_sigs
    sigs = collections.Counter()
    for r in ls.iter("RemoteableTimeSignature"):
        sigs[f"{val(r, 'Numerator')}/{val(r, 'Denominator')}@{val(r, 'Time')}"] += 1
    rec["clip_time_signatures"] = dict(sigs)
    starts, ends = [], []
    for aa in ls.iter("ArrangerAutomation"):
        for clip in aa.findall("Events/*"):
            if clip.find("CurrentStart") is not None:
                starts.append(float(val(clip, "CurrentStart")))
                ends.append(float(val(clip, "CurrentEnd")))
    rec["arrangement_clips"] = [len(starts), min(starts, default=None), max(ends, default=None)]
    return rec


def work(args):
    root_dir, rel = args
    data = open(os.path.join(root_dir, rel), "rb").read()
    out = {"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
           "gzip": data[:2] == b"\x1f\x8b", "magic": data[:4].hex()}
    if not out["gzip"] and not data.startswith(b"<?xml"):
        return out  # opaque/binary: counted, not parsed
    xml = gzip.decompress(data) if out["gzip"] else data
    out["decoded_sha256"] = hashlib.sha256(xml).hexdigest()
    root = ET.fromstring(xml)
    out["root"] = [root.tag, dict(root.attrib), [c.tag for c in root]]
    cen = collections.Counter()
    census(root, f"/{root.tag}", cen)
    out["census"] = dict(cen)
    ls = root.find("LiveSet")
    if ls is not None:
        out["liveset"] = liveset(ls)
    return out


def walk(contents):
    files, skipped = [], collections.Counter()
    for d, _, names in os.walk(contents):
        for n in names:
            ext = os.path.splitext(n)[1].lower()
            if ext not in EXTS:
                continue
            p = os.path.join(d, n)
            if n.startswith("._"):
                with open(p, "rb") as fh:
                    skipped[(ext, fh.read(4) == APPLEDOUBLE)] += 1
                continue
            files.append(os.path.relpath(p, contents))
    return sorted(files), skipped


def numfmt(s):
    if s in ("true", "false"):
        return "bool-token"
    if re.fullmatch(r"-?\d+", s):
        return "integer"
    if re.fullmatch(r"-?\d+\.\d+", s):
        return "decimal"
    if re.fullmatch(r"-?\d+(\.\d+)?[eE][-+]?\d+", s):
        return "exponent"
    return "other"


# Leaf value classes declared by schema 12.0_12402 (see schema-survey.json path_resolution).
FIELD_CLASS = {"Tempo/Manual": "Float", "Tempo/MidiControllerRange/Min": "Float",
               "Tempo/MidiControllerRange/Max": "Float", "Transport/PhaseNudgeTempo": "Float",
               "Transport/MetronomeTickDuration": "Float", "Transport/LoopStart": "Double",
               "Transport/LoopLength": "Double", "Transport/CurrentTime": "Double"}


def f32(x):
    return struct.unpack("<f", struct.pack("<f", float(x)))[0]


def shortest(x, double):
    """Shortest %.Ng text (N >= integer digits, so no exponent) that round-trips to x."""
    for p in range(max(1, len(str(int(abs(x))))), 18):
        s = "%.*g" % (p, x)
        if (float(s) if double else f32(s)) == x:
            return s


def format_check(field, v):
    """Compare a stored lexical value with %.9g (Float) / %.17g (Double) and shortest forms."""
    double = FIELD_CLASS[field] == "Double"
    x = float(v) if double else f32(v)
    fixed = "%.17g" % x if double else "%.9g" % x
    return f"{FIELD_CLASS[field]} equals_{'%.17g' if double else '%.9g'}={fixed == v} equals_shortest={shortest(x, double) == v}"


def decode_timesig(v):
    """Hypothesis H-TS: v = (numerator - 1) + 99 * log2(denominator)."""
    v = int(v)
    return v % 99 + 1, 2 ** (v // 99)


def schema_transport(schema_dir, minor, cache={}):
    """(Transport field names, MainTrackDevice field names, root ChangeCount) or None."""
    if minor not in cache:
        p = os.path.join(schema_dir, f"{minor}.txt")
        cache[minor] = None
        if os.path.exists(p):
            r = ET.parse(p).getroot()
            cache[minor] = ([f.tag for f in r.find("Transport")],
                            [f.tag for f in r.find("MainTrackDevice")], r.get("ChangeCount"))
    return cache[minor]


def is_subsequence(sub, seq):
    it = iter(seq)
    return all(x in it for x in sub)


def summarize(results, schema_dir):
    agg = {"by_ext": collections.defaultdict(collections.Counter),
           "census": collections.defaultdict(collections.Counter)}
    ls_docs = []
    for r in results:
        ext = os.path.splitext(r["path"])[1].lower()
        agg["by_ext"][ext]["files"] += 1
        agg["by_ext"][ext]["gzip" if r["gzip"] else f"not-gzip:{r['magic']}"] += 1
        if "root" in r:
            agg["by_ext"][ext][f"root-child:{','.join(r['root'][2])}"] += 1
            for p, n in r["census"].items():
                agg["census"][ext][p] += n
        if "liveset" in r:
            ls_docs.append(r)
    fields = collections.defaultdict(lambda: {"values": collections.Counter(),
                                              "formats": collections.Counter(),
                                              "by_minor": collections.defaultdict(collections.Counter),
                                              "by_creator": collections.defaultdict(collections.Counter),
                                              "present": 0})
    checks = collections.defaultdict(collections.Counter)
    notable = collections.defaultdict(list)
    roots = collections.Counter()
    for r in ls_docs:
        ext = os.path.splitext(r["path"])[1].lower()
        a = r["root"][1]
        minor, creator = a.get("MinorVersion"), a.get("Creator")
        roots[(ext, a.get("MajorVersion"), minor, a.get("SchemaChangeCount"), creator)] += 1
        L = r["liveset"]
        flat = {}
        for tag, attrs, kids in L["transport"] or []:
            flat[f"Transport/{tag}"] = attrs.get("Value")
            checks["transport_child_attr_sets"][",".join(sorted(attrs))] += 1
            if kids:
                checks["transport_children_with_subelements"][tag] += 1
        for key in ("Tempo", "TimeSignature"):
            t = L[key]
            if t:
                flat[f"{key}/Manual"] = t["manual"]
                flat[f"{key}/MidiControllerRange/Min"], flat[f"{key}/MidiControllerRange/Max"] = t["range"]
                flat[f"{key}/AutomationTarget@Id"] = t["automation_id"]
                checks[f"{key}_children"][",".join(t["children"])] += 1
        for k, v in flat.items():
            if v is None:
                continue
            if k in FIELD_CLASS:
                checks["lexical_format_vs_width"][f"{k}: {format_check(k, v)}"] += 1
            f = fields[k]
            f["present"] += 1
            f["values"][v] += 1
            f["formats"][numfmt(v)] += 1
            f["by_minor"][minor][v] += 1
            f["by_creator"][creator][v] += 1
        # schema conformance of Transport children
        sch = schema_transport(schema_dir, minor)
        if sch is None:
            checks["transport_vs_schema"]["no schema file for MinorVersion"] += 1
        else:
            got = [t for t, _, _ in L["transport"] or []]
            extra = [t for t in got if t not in sch[0]]
            missing = [t for t in sch[0] if t not in got]
            checks["transport_vs_schema"][f"extra={extra}"] += 1
            checks["transport_missing_schema_fields"][",".join(missing)] += 1
            checks["transport_in_schema_order"][is_subsequence(got, sch[0])] += 1
            checks["schemachangecount_vs_schema_changecount"][
                f"doc={a.get('SchemaChangeCount')} schema={sch[2]}"] += 1
            mix = L["main_mixer_children"] or []
            checks["main_mixer_missing_schema_fields"][",".join(f for f in sch[1] if f not in mix)] += 1
            checks["main_mixer_extra_vs_schema"][",".join(f for f in mix if f not in sch[1])] += 1
        # tempo / time-signature automation
        for key, events in L["envelopes"].items():
            manual = L[key]["manual"]
            checks[f"{key}_envelope_event_tags"][",".join(sorted({e[0] for e in events}))] += 1
            checks[f"{key}_envelope_event_count"][len(events)] += 1
            if events:
                checks[f"{key}_envelope_first_event"][
                    f"time={events[0][1]} value_eq_manual={events[0][2] == manual}"] += 1
            notable[f"{key}_envelopes"].append([r["path"], manual, len(events), events[:4]])
        # filename tempo cross-check
        m = re.search(r"(\d+(?:\.\d+)?)\s*bpm", os.path.basename(r["path"]), re.I)
        if m and L["Tempo"]:
            same = float(m.group(1)) == float(L["Tempo"]["manual"])
            checks["filename_bpm_equals_tempo_manual"][same] += 1
            if not same:
                notable["filename_bpm_mismatch"].append([r["path"], L["Tempo"]["manual"]])
        # time-signature encoding hypothesis
        if L["TimeSignature"]:
            n, d = decode_timesig(L["TimeSignature"]["manual"])
            clip_sigs = {k.split("@")[0] for k in L["clip_time_signatures"]}
            checks["timesig_decoded"][f"{n}/{d}"] += 1
            if clip_sigs:
                checks["timesig_decoded_in_clip_signatures"][f"{n}/{d}" in clip_sigs] += 1
            for s in L["scenes"]:
                if s[2] is not None:
                    checks["scene_timesig_id_decoded"][f"{'%d/%d' % decode_timesig(s[2])} enabled={s[3]}"] += 1
            if (n, d) != (4, 4):
                notable["non_4_4"].append([r["path"], L["TimeSignature"]["manual"], f"{n}/{d}",
                                           sorted(clip_sigs), flat.get("Transport/LoopStart"),
                                           flat.get("Transport/LoopLength")])
            bar = n * 4 / d
            for k in ("LoopStart", "LoopLength", "CurrentTime"):
                v = flat.get(f"Transport/{k}")
                if v is not None:
                    x = float(v)
                    checks[f"{k}_multiple_of_bar_in_quarter_notes"][math.isclose(x / bar, round(x / bar))] += 1
        for i, (sid, slot) in L["scene_slot_signatures"].items():
            dec = "%d/%d" % decode_timesig(sid)
            checks["scene_timesig_decoded_in_slot_clip_signatures"][f"{dec} in {sorted(slot)}: {dec in slot}"] += 1
        for s in L["scenes"]:
            checks["scene_tempo_enabled"][f"tempo={s[0]} enabled={s[1]}"] += 1
        # loop region vs arrangement clip extent (timeline units)
        nclips, lo, hi = L["arrangement_clips"]
        if nclips and flat.get("Transport/LoopStart") is not None:
            ls0, ll = float(flat["Transport/LoopStart"]), float(flat["Transport/LoopLength"])
            checks["loop_vs_arrangement_extent"][
                "equal" if (ls0, ls0 + ll) == (lo, hi) else
                "inside" if lo <= ls0 and ls0 + ll <= hi else "other"] += 1
            notable["loop_vs_arrangement"].append([r["path"], ls0, ll, lo, hi, nclips])
    return {
        "by_ext": {k: dict(v) for k, v in agg["by_ext"].items()},
        "census": {k: dict(sorted(v.items())) for k, v in agg["census"].items()},
        "liveset_docs": len(ls_docs),
        "liveset_roots": [[list(k), n] for k, n in sorted(roots.items(), key=str)],
        "fields": {k: {"present": f["present"], "distinct": len(f["values"]),
                       "values": dict(f["values"].most_common()),
                       "formats": dict(f["formats"]),
                       "by_minor": {m: dict(c) for m, c in sorted(f["by_minor"].items())},
                       "by_creator": {m: dict(c) for m, c in sorted(f["by_creator"].items())}}
                   for k, f in sorted(fields.items())},
        "checks": {k: {str(x): n for x, n in v.most_common()} for k, v in checks.items()},
        "notable": notable,
    }


def selftest():
    assert [numfmt(x) for x in ("true", "120", "121.199997", "1e3", "x")] == \
        ["bool-token", "integer", "decimal", "exponent", "other"]
    assert decode_timesig("201") == (4, 4) and decode_timesig("302") == (6, 8)
    assert format_check("Tempo/Manual", "121.199997") == "Float equals_%.9g=True equals_shortest=False"
    assert format_check("Transport/LoopStart", "8") == "Double equals_%.17g=True equals_shortest=True"
    assert format_check("Transport/PhaseNudgeTempo", "10") == "Float equals_%.9g=True equals_shortest=True"
    assert decode_timesig("0") == (1, 1) and decode_timesig("494") == (99, 16)
    assert is_subsequence(["a", "c"], ["a", "b", "c"]) and not is_subsequence(["c", "a"], ["a", "c"])


def main(contents, schema_dir, out_path, inputs_path):
    selftest()
    files, skipped = walk(contents)
    with multiprocessing.Pool(min(32, os.cpu_count())) as pool:
        results = pool.map(work, [(contents, f) for f in files], chunksize=8)
    with open(inputs_path, "w") as fh:
        for r in results:
            fh.write(f"{r['sha256']}\t{r['bytes']}\t{int(r['gzip'])}\t{int('root' in r)}\t{r['path']}\n")
    out = {"contents": contents, "files": len(files),
           "appledouble_skipped": {f"{e} magic_ok={ok}": n for (e, ok), n in sorted(skipped.items())},
           **summarize(results, schema_dir),
           "liveset_records": [{k: r[k] for k in ("path", "sha256", "decoded_sha256", "root", "liveset")}
                               for r in results if "liveset" in r]}
    for rec in out["liveset_records"]:
        rec["root"] = rec["root"][1]
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1, default=list)


if __name__ == "__main__":
    main(*sys.argv[1:5])
