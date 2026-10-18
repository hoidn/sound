"""S8 static half: warp markers and warp settings in Live's shipped schemas and documents.

Usage: python3 -I s8_static.py <bundle Contents dir> <out.json> <inputs.tsv> <records.jsonl>
Read-only on inputs. Analyst tool; recovered text is data.
Schema part: every non-AppleDouble App-Resources/Schema/*.txt ordered by (major, minor, number) from the
file name (presentation order, not proven migration order); per-version field class/type of the warp-related
classes, evolution segments, latest field order, classes holding warp-named fields, tag-name census.
Document part: every non-AppleDouble *.als/.alc/.adv/.adg below Contents (gzip or plain XML). Each
WarpMarkers element with its holder (AudioClip or SampleWarpProperties) yields one record; `checks`
counts the static hypotheses named in the wiki page (ordering, shadow marker, extrapolation, units,
number text, quantisation, file-name tempo).
inputs.tsv: sha256, bytes, gzip flag, relative path of each document read.
records.jsonl: one line per AudioClip holder (document order); SampleWarpProperties holders enter `checks`,
`distributions` and `notable` only (11,616 lines would add about 8 MB).
"""
import collections, gzip, hashlib, json, math, os, re, sys
import xml.etree.ElementTree as ET

CLASSES = {  # class -> fields of interest (None = all fields)
    "AudioClip": ["IsWarped", "SampleRef", "Onsets", "WarpMode", "GranularityTones", "GranularityTexture",
                  "FluctuationTexture", "FluxTexture", "TransientResolution", "TransientLoopMode",
                  "TransientEnvelope", "ComplexProFormants", "ComplexProEnvelope", "Sync", "HiQ", "Fade",
                  "PitchCoarse", "PitchFine", "SampleVolume", "WarpMarkers", "SavedWarpMarkersForStretched",
                  "MarkersGenerated", "IsSongTempoLeader", "Loop", "CurrentStart", "CurrentEnd"],
    "WarpMarker": None, "SampleWarpProperties": None, "SampleRef": None, "Loop": None, "OnsetArray": None,
    "MultiSamplePart": ["SampleStart", "SampleEnd", "SampleRef", "SampleWarpProperties", "IsWarped"],
}
SETTINGS = ["IsWarped", "WarpMode", "GranularityTones", "GranularityTexture", "FluctuationTexture",
            "TransientResolution", "TransientLoopMode", "TransientEnvelope", "ComplexProFormants",
            "ComplexProEnvelope"]
LOOP = ["LoopStart", "LoopEnd", "StartRelative", "LoopOn", "OutMarker", "HiddenLoopStart", "HiddenLoopEnd"]
SHADOW = 0.03125
Q = 3843840.0  # beat quantum seen in the native setters (1/3,843,840 beat)
BPM_RX = re.compile(r"(\d+(?:\.\d+)?) ?bpm", re.I)


def vkey(name):
    m = re.fullmatch(r"(\d+)\.(\d+)_(\d+)\.txt", name)
    if not m:
        raise ValueError(f"unexpected schema file name {name!r}")
    return tuple(int(x) for x in m.groups())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def schema_part(sdir):
    files = sorted((f for f in os.listdir(sdir) if f.endswith(".txt") and not f.startswith("._")), key=vkey)
    versions, segs, prev, latest, tags = [], collections.OrderedDict(), None, None, collections.Counter()
    for f in files:
        raw = open(os.path.join(sdir, f), "rb").read()
        root = ET.fromstring(raw)
        v = "%d.%d_%d" % vkey(f)
        versions.append({"version": v, "sha256": sha(raw)})
        for t in ("FluxTexture", "FluctuationTexture", "WarpMarker", "SampleWarpProperties"):
            tags[t] += any(fl.tag == t or cl.tag == t for cl in root for fl in [cl, *cl])
        cur = {}
        for cls, want in CLASSES.items():
            el = root.find(cls)
            for fl in ([] if el is None else el):
                if want is None or fl.tag in want:
                    cur[f"{cls}.{fl.tag}"] = f"{fl.get('Class')}:{fl.get('Type')}"
        for key in set(cur) | set(segs):
            s = segs.setdefault(key, [])
            val = cur.get(key)
            if s and s[-1]["value"] == val and s[-1]["last"] == prev:
                s[-1]["last"] = v
            else:
                s.append({"value": val, "first": v, "last": v})
        prev, latest = v, root
    order = {c: [fl.tag for fl in latest.find(c)] for c in ("AudioClip", "SampleWarpProperties", "WarpMarker", "SampleRef", "Loop")}
    holders = {t: sorted(c.tag for c in latest if c.find(t) is not None)
               for t in ("WarpMarkers", "WarpMode", "IsWarped", "SampleWarpProperties", "SecTime", "TransientLoopMode")}
    evolution = {k: [x for x in s if x["value"] is not None] for k, s in sorted(segs.items())}
    return {"files_parsed": len(files), "versions": versions, "evolution": evolution,
            "field_order_latest": order, "holders_latest": holders,
            "files_with_tag": dict(tags)}


def num_text(x):
    """Static Double writer rule from n1-transport-state-v1 (precision max(0, 17 - k), trailing zeros cut)."""
    if x == 0:
        prec = 16
    else:
        e = math.log10(abs(x))
        prec = max(0, 17 - (math.floor(e) if e < 0 else math.ceil(e)))
    s = "%.*f" % (prec, x)
    return s.rstrip("0").rstrip(".") if "." in s else s


def val(el, sub, attr="Value"):
    x = el.find(sub) if el is not None else None
    return None if x is None else x.get(attr)


def fnum(t):
    return None if t is None else float(t)


def tempo(a, b):
    ds = b[0] - a[0]
    return (b[1] - a[1]) / ds * 60.0 if ds > 0 else None


def record(doc, path, holder, parent):
    ms = [(m.get("Id"), m.get("SecTime"), m.get("BeatTime")) for m in holder.find("WarpMarkers")]
    sref = holder.find("SampleRef") if holder.tag == "AudioClip" else parent.find("SampleRef")
    file_name = val(sref, "FileRef/RelativePath") or val(sref, "FileRef/Path") or ""
    rec = {"doc": doc, "holder": holder.tag, "path": "/".join(path.split("/")[-5:]),
           **{k: val(holder, k) for k in SETTINGS},
           "markers": ms, "saved_markers": None if (sv := holder.find("SavedWarpMarkersForStretched")) is None else len(sv),
           "markers_generated": val(holder, "MarkersGenerated"),
           "default_duration": val(sref, "DefaultDuration"), "default_sample_rate": val(sref, "DefaultSampleRate"),
           "samples_to_auto_warp": val(sref, "SamplesToAutoWarp"),
           "sample_ext": os.path.splitext(file_name)[1].lower()}
    if holder.tag == "AudioClip":
        rec["loop"] = {k: val(holder, f"Loop/{k}") for k in LOOP}
        rec["current"] = [val(holder, "CurrentStart"), val(holder, "CurrentEnd")]
    else:
        rec["part"] = {"tag": parent.tag, "SampleStart": val(parent, "SampleStart"), "SampleEnd": val(parent, "SampleEnd")}
    return rec


def holders(root):
    stack = [(root, root.tag, None)]
    while stack:
        el, path, parent = stack.pop()
        for c in el:
            p = f"{path}/{c.tag}"
            if c.tag in ("AudioClip", "SampleWarpProperties") and c.find("WarpMarkers") is not None:
                yield p, c, el
            stack.append((c, p, el))


def checks_for(rec, chk, notable, song_tempo):
    h, w = rec["holder"], rec["IsWarped"]
    pts = [(float(s), float(b)) for _, s, b in rec["markers"]]
    n = len(pts)
    chk[f"{h}|count={n if n < 4 else '4+'}|IsWarped={w}"] += 1
    for i, s, b in rec["markers"]:
        for t in (s, b):
            ok = num_text(float(t)) == t
            chk[f"number_text_rule|{'match' if ok else 'mismatch'}"] += 1
            if not ok and len(notable["number_text_mismatch"]) < 20:
                notable["number_text_mismatch"].append([rec["doc"], t, num_text(float(t))])
        q = float(b) * Q
        chk[f"beat_on_1/3843840_grid|{abs(q - round(q)) < 1e-6}"] += 1
    ids = [i for i, _, _ in rec["markers"]]
    if n:
        chk[f"{h}|ids_unique={len(set(ids)) == n}|ids_ascending={ids == sorted(ids, key=int)}"] += 1
        chk[f"{h}|first_marker={'(0,0)' if pts[0] == (0.0, 0.0) else 'other'}"] += 1
        if pts[0] != (0.0, 0.0) and len(notable["first_marker_not_origin"]) < 20:
            notable["first_marker_not_origin"].append([rec["doc"], h, rec["markers"][0]])
        chk[f"{h}|any_negative={any(s < 0 or b < 0 for s, b in pts)}"] += 1
    if n < 2:
        return
    chk[f"{h}|sec_strictly_increasing={all(b[0] > a[0] for a, b in zip(pts, pts[1:]))}"] += 1
    chk[f"{h}|beat_strictly_increasing={all(b[1] > a[1] for a, b in zip(pts, pts[1:]))}"] += 1
    shadow = pts[-1][1] - pts[-2][1] == SHADOW
    chk[f"{h}|last_beat_step_is_1/32={shadow}"] += 1
    if not shadow and len(notable["last_step_not_1/32"]) < 40:
        notable["last_step_not_1/32"].append([rec["doc"], h, rec["path"], w, rec["markers"][-3:]])
    t_shadow = tempo(pts[-2], pts[-1])
    segs = [tempo(a, b) for a, b in zip(pts, pts[1:])]
    if n >= 3:
        same = abs(t_shadow - segs[-2]) <= 1e-6 * abs(segs[-2])
        chk[f"{h}|n>=3|shadow_tempo==previous_segment_tempo={same}"] += 1
    lo, hi = min(segs), max(segs)
    chk[f"{h}|all_segment_tempi_in_[5,999]={5.0 <= lo and hi <= 999.0}"] += 1
    m = BPM_RX.search(os.path.basename(rec["doc"]))
    if m and h == "AudioClip" and w == "true":
        chk[f"filename_bpm|shadow_tempo_within_0.01={abs(t_shadow - float(m.group(1))) < 0.01}"] += 1
        if abs(t_shadow - float(m.group(1))) >= 0.01 and len(notable["filename_bpm_differs"]) < 20:
            notable["filename_bpm_differs"].append([rec["doc"], m.group(1), t_shadow, song_tempo])
    dur, sr = fnum(rec["default_duration"]), fnum(rec["default_sample_rate"])
    if h != "AudioClip" or not dur or not sr:
        return
    secs = dur / sr
    lp = {k: fnum(v) for k, v in rec["loop"].items() if k != "LoopOn"}
    if w == "true":
        # beat position of the sample end, extrapolated with the shadow segment's slope (hypothesis H-EXT)
        end_beat = pts[-1][1] + (secs - pts[-1][0]) * (pts[-1][1] - pts[-2][1]) / (pts[-1][0] - pts[-2][0])
        start_beat = pts[0][1] - pts[0][0] * (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0])
        for k in ("OutMarker", "HiddenLoopEnd", "LoopEnd"):
            chk[f"warped|{k}==extrapolated_sample_end_beat={abs(lp[k] - end_beat) < 1e-6}"] += 1
        chk[f"warped|HiddenLoopStart==extrapolated_sample_start_beat={abs(lp['HiddenLoopStart'] - start_beat) < 1e-6}"] += 1
        if abs(lp["OutMarker"] - end_beat) >= 1e-6 and len(notable["warped_outmarker_differs"]) < 20:
            notable["warped_outmarker_differs"].append([rec["doc"], lp["OutMarker"], end_beat, lp["HiddenLoopEnd"]])
    else:
        for k in ("OutMarker", "HiddenLoopEnd", "LoopEnd"):
            chk[f"unwarped|{k}==sample_length_seconds={abs(lp[k] - secs) < 1e-6}"] += 1
        chk[f"unwarped|LoopEnd<=sample_length_seconds={lp['LoopEnd'] <= secs + 1e-6}"] += 1
        if abs(lp["OutMarker"] - secs) >= 1e-6 and song_tempo:
            beats = secs * float(song_tempo) / 60.0
            chk[f"unwarped|OutMarker!=seconds|OutMarker==seconds*set_tempo/60={abs(lp['OutMarker'] - beats) < 1e-4}"] += 1
        if abs(lp["OutMarker"] - secs) >= 1e-6 and len(notable["unwarped_outmarker_differs"]) < 20:
            notable["unwarped_outmarker_differs"].append([rec["doc"], lp, secs])


def doc_part(contents):
    exts = (".als", ".alc", ".adv", ".adg")
    paths = sorted(os.path.join(d, f) for d, _, fs in os.walk(contents) for f in fs
                   if f.endswith(exts) and not f.startswith("._"))
    skipped = sum(1 for d, _, fs in os.walk(contents) for f in fs if f.endswith(exts) and f.startswith("._"))
    inputs, records, unparsed = [], [], []
    dist = collections.defaultdict(collections.Counter)
    chk, notable = collections.Counter(), collections.defaultdict(list)
    for p in paths:
        raw = open(p, "rb").read()
        rel = os.path.relpath(p, contents)
        gz = raw[:2] == b"\x1f\x8b"
        inputs.append(f"{sha(raw)}\t{len(raw)}\t{int(gz)}\t{rel}")
        try:
            root = ET.fromstring(gzip.decompress(raw) if gz else raw)
        except (ET.ParseError, OSError, EOFError) as e:
            unparsed.append([rel, type(e).__name__])
            continue
        song_tempo = val(root, "LiveSet/MainTrack/DeviceChain/Mixer/Tempo/Manual")
        for path, h, parent in holders(root):
            rec = record(rel, path, h, parent)
            records.append(rec)
            dist[f"{h.tag}|doc_ext"][os.path.splitext(rel)[1]] += 1
            dist[f"{h.tag}|doc"][rel] += 1
            for k in SETTINGS:
                dist[f"{h.tag}|{k}"][rec[k]] += 1
            dist[f"{h.tag}|IsWarped|WarpMode"][f"{rec['IsWarped']}|{rec['WarpMode']}"] += 1
            dist[f"{h.tag}|WarpMode|sample_ext"][f"{rec['WarpMode']}|{rec['sample_ext']}"] += 1
            dist[f"{h.tag}|MarkersGenerated"][rec["markers_generated"]] += 1
            dist[f"{h.tag}|SavedWarpMarkersForStretched_count"][rec["saved_markers"]] += 1
            dist[f"{h.tag}|SamplesToAutoWarp"][rec["samples_to_auto_warp"]] += 1
            dist[f"{h.tag}|DefaultSampleRate"][rec["default_sample_rate"]] += 1
            checks_for(rec, chk, notable, song_tempo)
    ranges = {}
    for r in records:
        for k in SETTINGS[2:]:
            if r[k] is not None and k not in ("TransientResolution", "TransientLoopMode"):
                lo, hi = ranges.get(f"{r['holder']}|{k}", (math.inf, -math.inf))
                ranges[f"{r['holder']}|{k}"] = (min(lo, float(r[k])), max(hi, float(r[k])))
    return {"files": len(paths), "appledouble_skipped": skipped, "unparsed": unparsed,
            "records": len(records),
            "distributions": {k: dict(sorted(v.items(), key=lambda kv: (-kv[1], str(kv[0])))) for k, v in sorted(dist.items())},
            "setting_ranges": dict(sorted(ranges.items())),
            "checks": dict(sorted(chk.items())), "notable": dict(notable)}, inputs, records


def main():
    contents, out, tsv, jsonl = sys.argv[1:5]
    res = {"schema": schema_part(os.path.join(contents, "App-Resources", "Schema"))}
    res["documents"], inputs, records = doc_part(contents)
    json.dump(res, open(out, "w"), indent=1)
    open(tsv, "w").write("sha256\tbytes\tgzip\tpath\n" + "\n".join(inputs) + "\n")
    open(jsonl, "w").write("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in records if r["holder"] == "AudioClip"))


if __name__ == "__main__":
    main()
