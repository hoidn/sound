"""Reviewer's checks of the live-set-structure-v1 candidate (analyst side; never shipped; output is data).

usage: python3 -I -B review_checks.py [PACKAGE_DIR]   (default: the staging copy)
Independent of build_lss.py and lss_cases.py: an own restatement of the released clauses (judge), refusal
isolation against T11-MIN, exclusion hits, cross-release spot checks of T11-MIN's field text, the sample identity,
package inventory, hashes, links, fixture container form and a sanitization scan. The T11 checker itself
(schema_check.py, fixture_audit.py) is run unchanged and separately (see review-checks.txt).
"""
import gzip, hashlib, json, math, re, struct, sys, wave, zlib
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parents[1] / "live-set-structure-v1"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
T11 = HERE.parents[2] / "r2/t11-structure-v1"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_schema():
    r = ET.parse(SCHEMA).getroot()
    return {c.tag: {f.tag: (f.get("Class"), f.get("Type")) for f in c} for c in r}


SCH = load_schema()
PLAYER = ("MidiTrack", "AudioTrack", "GroupTrack")
TRACK_KINDS = PLAYER + ("ReturnTrack",)
TARGETS = {"AutomationTarget", "ModulationTarget", "Pointee", "VolumeModulationTarget", "TranspositionModulationTarget",
           "TransientEnvelopeModulationTarget", "GrainSizeModulationTarget", "FluxModulationTarget",
           "SampleOffsetModulationTarget", "ComplexProFormantsModulationTarget", "ComplexProEnvelopeModulationTarget"} | \
          {f"ControllerTargets.{i}" for i in range(131)}
KIND = {"MidiTrack": "midi", "AudioTrack": "audio", "ReturnTrack": "return"}


def send_text(g):  # mixer text rule as far as these fixtures need it (-inf dB at or below -69.7 dB)
    db = 20 * math.log10(g)
    if db <= -69.7:
        return "-inf dB"
    return f"{db:.1f} dB"  # ponytail: no fixture reaches this branch; the full rule lives in mixer-values-v1


def shapes(ls):
    """Reading-time shapes, by the document's element classes: (violations, exclusions)."""
    viol, excl = [], []

    def walk(e, cls):
        fields = SCH.get(cls)
        if fields is None:
            return
        for tag, k in Counter(c.tag for c in e if c.tag in fields).items():
            if k > 1:
                (excl if tag.endswith("KeyMidi") else viol).append(f"001 repeated member {cls}/{tag}")
        for c in e:
            f = fields.get(c.tag)
            if f is None:
                continue  # unknown child: skipped (001 clause 4)
            fcls, ftype = f
            if ftype == "-4":
                if "Value" not in c.attrib:
                    (viol if c.tag == "NextPointeeId" else excl).append(f"001 value element without Value {c.tag}")
            elif ftype == "0":
                walk(c, fcls)
            elif ftype == "-1":
                ids = []
                for item in c:
                    i = item.get("Id")
                    if i is None:
                        excl.append(f"016 list item without Id {c.tag}/{item.tag}")
                    elif i == "-1":
                        viol.append(f"016 negative list-item Id {c.tag}/{item.tag}")
                    elif i == "a":
                        viol.append(f"016 lettered list-item Id {c.tag}/{item.tag}")
                    elif not re.fullmatch(r"0|[1-9][0-9]*", i):
                        excl.append(f"016 other Id text {i!r}")
                    ids.append(i)
                    if c.tag == "Tracks" and item.tag not in TRACK_KINDS:
                        (viol if item.tag not in SCH else excl).append(f"001 Tracks item {item.tag}")
                    walk(item, item.tag)
                for i, k in Counter(x for x in ids if x is not None).items():
                    if k > 1:
                        viol.append(f"016 repeated list-item Id {c.tag} {i}")
            # type -3 arrays: items of one name; no member rule applies
    walk(ls, "LiveSet")
    return viol, excl


def judge(raw, setup="with-samples"):
    """Return (outcome, state, violations, exclusions, repairs) under the released clauses."""
    root = ET.fromstring(gzip.decompress(raw))
    excl, rep = [], []
    if root.tag != "Ableton" or root.attrib != {"MajorVersion": "5", "MinorVersion": "12.0_12402",
                                                "SchemaChangeCount": "1"} or [c.tag for c in root] != ["LiveSet"]:
        excl.append("envelope")
    ls = root.find("LiveSet")
    viol, x = shapes(ls)
    excl += x
    tracks_el = ls.find("Tracks")
    tracks = list(tracks_el) if tracks_el is not None else []
    # targets (015)
    tids = []
    for e in ls.iter():
        if e.tag in TARGETS:
            i = e.get("Id")
            if i in (None, "0"):
                viol.append(f"015 target Id 0 or none ({e.tag})")
            else:
                tids.append(int(i))
    if len(tids) != len(set(tids)) or any(i < 0 for i in tids):
        excl.append("015 repeated or negative target Ids")
    npi = ls.find("NextPointeeId")
    if npi is None or "Value" in npi.attrib:
        nxt = 1 if npi is None else int(npi.get("Value"))
        if nxt <= max(tids, default=0):
            viol.append("015 NextPointeeId not above the largest target Id")
    # sends (013)
    R = 0
    for t in reversed(tracks):
        if t.tag != "ReturnTrack":
            break
        R += 1
    counts, texts = [], {}
    for k, t in enumerate(tracks, 1):
        hs = t.findall("DeviceChain/Mixer/Sends/TrackSendHolder")
        if len(hs) > R:
            viol.append(f"013 more send holders than R (track {k})")
        if len(hs) < R:
            rep.append(f"013 {R - len(hs)} holder(s) added (track {k})")
        counts.append(max(len(hs), R))
        texts[str(k)] = [send_text(float(h.find("Send/Manual").get("Value"))) for h in hs] + ["-inf dB"] * (R - len(hs))
    sp = ls.find("SendsPre")
    if (len(list(sp)) if sp is not None else 0) != sum(t.tag == "ReturnTrack" for t in tracks):
        excl.append("013 SendsPre length differs from the number of return tracks")
    # envelopes (014)
    autom = {}
    for k, t in enumerate(tracks, 1):
        kept = set()
        for env in t.findall("AutomationEnvelopes/Envelopes/AutomationEnvelope"):
            p = env.find("EnvelopeTarget/PointeeId").get("Value")
            if p == "0" or int(p) not in tids:
                rep.append(f"014 envelope removed (track {k}, PointeeId {p})")
            else:
                kept.add(p)
        autom[str(k)] = len(kept)
    # walk (002, 006)
    if not any(t.tag in PLAYER for t in tracks):
        viol.append("002 no audio, MIDI or group track")
    seen_ret = False
    for t in tracks:
        if t.tag == "ReturnTrack":
            seen_ret = True
        elif t.tag in PLAYER and seen_ret:
            viol.append("002 player track after a return track")
            break
    if any(t.tag == "GroupTrack" for t in tracks):
        excl.append("group tracks")
    elif any((t.find("TrackGroupId") is not None and t.find("TrackGroupId").get("Value") != "-1") for t in tracks):
        viol.append("002 TrackGroupId other than -1 without group tracks")
    scenes = ls.find("Scenes")
    nsc = len(list(scenes)) if scenes is not None else None
    clips = []
    for t in tracks:
        if t.tag not in ("MidiTrack", "AudioTrack"):
            if t.find("DeviceChain/MainSequencer") is not None:
                excl.append("slots on a return track")
            continue
        main = t.findall("DeviceChain/MainSequencer/ClipSlotList/ClipSlot")
        frz = t.findall("DeviceChain/FreezeSequencer/ClipSlotList/ClipSlot")
        if len(main) != len(frz):
            viol.append(f"006 freeze slots {len(frz)} != session slots {len(main)} ({t.tag})")
        if nsc is None and main or nsc is not None and len(main) != nsc:
            excl.append("006 session slots differ from scenes")
        row = []
        for s in main:
            v = list(s.find("ClipSlot/Value"))
            want = "MidiClip" if t.tag == "MidiTrack" else "AudioClip"
            if len(v) > 1 or (v and v[0].tag != want):
                excl.append("006 two clips or wrong clip kind")
            row.append(v[0].find("Name").get("Value") if v else None)
        clips.append(row)
    # other exclusions
    for t in tracks:
        if t.tag in TRACK_KINDS and len(t.findall("DeviceChain/DeviceChain/Devices/*")):
            excl.append(f"device in {t.tag}")
        tg = t.find("DeviceChain/AudioOutputRouting/Target")
        if t.tag in KIND and (tg is None or tg.get("Value") != "AudioOut/Main"):
            excl.append("output routing")
    # sample resolution (009) for track 2 slot 1
    fr = tracks[1].find("DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/AudioClip/SampleRef/FileRef") \
        if len(tracks) > 1 and tracks[1].tag == "AudioTrack" else None
    afile = None
    if fr is not None:
        files = set() if setup == "without-samples" else {"Samples/T11-tone.wav"}
        rpt, rp, path = (fr.find(n).get("Value") for n in ("RelativePathType", "RelativePath", "Path"))
        if setup == "with-samples-absolute-path":
            assert path == "/T11/Samples/T11-tone.wav"
            path = "<folder>/Samples/T11-tone.wav"
        if rpt not in ("0", "1"):
            excl.append("RelativePathType 2 to 7")
        elif rp and rp in files:
            afile = rp
        elif path and path.startswith("<folder>/") and path[9:] in files:
            afile = path[9:]
    main = ls.find("MainTrack")
    tempo = 120.0 if main is None else float(main.find("DeviceChain/Mixer/Tempo/Manual").get("Value"))
    state = {"track_kinds": [KIND.get(t.tag, t.tag) for t in tracks],
             "scene_names": [s.find("Name").get("Value") for s in scenes] if scenes is not None else None,
             "session_clips": clips, "send_counts": counts, "send_texts": texts, "automated_parameters": autom,
             "tempo": tempo, "audio_clip_file": afile}
    return ("refused" if viol else "opens"), (None if viol else state), viol, sorted(set(excl)), rep


# ---- T11-MIN field text against the other released contracts (refusal-relevant parts only) ----
NUM = re.compile(r" *[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def cross_release(raw):
    root = ET.fromstring(gzip.decompress(raw))
    bad = []
    for env in list(root.iter("AutomationEnvelope")) + list(root.iter("ClipEnvelope")):
        ev = list(env.find("Automation/Events"))
        if not ev:
            bad.append("automation-envelopes 007: empty Events")
        elif float(ev[0].get("Time")) not in (-63072000.0, 0.0):
            bad.append("automation-envelopes 007: first event time")
        for e in ev:
            for a in ("Time", "Value"):
                if not NUM.match(e.get(a, "")):
                    bad.append(f"automation event {a} text")
    for clip in root.iter("MidiClip"):
        ids = []
        for kt in clip.iter("KeyTrack"):
            for n in kt.find("Notes"):
                if n.tag != "MidiNoteEvent":
                    bad.append("midi-note-storage 001: non-note in KeyTrack/Notes")
                for a in ("Time", "Duration", "Velocity", "OffVelocity"):
                    if not NUM.match(n.get(a, "")):
                        bad.append(f"note {a} text")
                if not re.fullmatch(r"[0-9]+", n.get("NoteId", "x")):
                    bad.append("note NoteId text")
                ids.append(n.get("NoteId"))
        nz = [i for i in ids if i != "0"]
        if len(nz) != len(set(nz)):
            bad.append("midi-note-storage 008: repeated NoteId")
        if [c.tag for c in clip.find("Notes")] != ["KeyTracks", "PerNoteEventStore", "NoteProbabilityGroups",
                                                    "ProbabilityGroupIdGenerator", "NoteIdGenerator"]:
            bad.append("midi-note-storage 001: notes children")
    for clip in list(root.iter("MidiClip")) + list(root.iter("AudioClip")):
        for n in ("LaunchMode", "LaunchQuantisation", "VelocityAmount"):
            if not re.fullmatch(r"-?[0-9]+", clip.find(n).get("Value")):
                bad.append(f"clip-launch: {n} text")
        if clip.find("Legato").get("Value") not in ("true", "false"):
            bad.append("clip-launch: Legato text")
        tags = [c.tag for c in clip]
        if len(tags) != len(set(tags)):
            bad.append("clip-launch 001: repeated clip child")
    for wm in root.iter("WarpMarker"):
        for a in ("SecTime", "BeatTime"):
            if not NUM.match(wm.get(a, "")):
                bad.append("warp-markers: marker text")
    for wl in root.iter("WarpMarkers"):
        if len(wl) < 2:
            bad.append("warp-markers: fewer than two markers")
    tp = root.find("LiveSet/Transport")
    if tp.find("LoopOn").get("Value") not in ("true", "false", "0", "1"):
        bad.append("transport-state 003: loop switch text")
    for n in ("LoopStart", "LoopLength", "CurrentTime"):
        if not NUM.match(tp.find(n).get("Value")):
            bad.append(f"transport-state: {n} text")
    return bad


def crc16(b):
    c = 0
    for x in b:
        c ^= x << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x8005) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
    return c


def container(raw):
    """Header, one member, valid trailer, nothing after; returns problems."""
    p = []
    if raw[:10] != bytes.fromhex("1f8b0800000000000213"):
        p.append("header")
    d = zlib.decompressobj(-15)
    data = d.decompress(raw[10:])
    rest = d.unused_data
    if len(rest) != 8 or struct.unpack("<II", rest) != (zlib.crc32(data), len(data)):
        p.append("trailer or trailing bytes")
    if b"\r" in data or not data.endswith(b"\n") or not data.startswith(b'<?xml version="1.0" encoding="UTF-8"?>\n'):
        p.append("text form")
    data.decode("utf-8")
    return p


def md_links(d):
    out = {}
    for md in sorted(d.glob("*.md")):
        rows = []
        for tgt in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
            path, _, anchor = tgt.partition("#")
            dest = (md.parent / path).resolve() if path else md
            ok = not re.match(r"[a-z]+:", tgt) and dest.is_file() and d.resolve() in dest.parents
            if ok and anchor:
                slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                         for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
                ok = anchor in slugs
            rows.append((tgt, ok))
        out[md.name] = rows
    return out


DENY = [r"0x[0-9a-fA-F]{5,}", r"FUN_", r"(?i)decompil", r"(?i)disassembl", r"(?i)pseudocode", r"Ghidra", r"(?i)corpus",
        r"(?i)vtable", r"analysis/", r"wiki/", r"raw/", r"/home/", r"/var/", r"/tmp/", r"\bLSS-", r"\bQ-0\d", r"\bA[1-7]\b",
        r"S-cond", r"\bT1\.\d", r"\bADR\b", r"\bA[A-Z][a-z]+[A-Z]\w*", r"(?i)post-load", r"(?i)validation walk",
        r"(?i)\bloader\b", r"(?i)constructor", r"(?i)pointee", r"Slot count mismatch", r"no player tracks",
        r"out of order", r"grouping corrupt", r"Non-unique", r"Illegal value", r"Invalid Pointee", r"send knobs",
        r"(?i)\bschema\b", r"Python", r"zlib", r"(?i)x86", r"\+0x", r"traceab", r"(?i)\bprobe\b", r"REQ-[A-Z-]+-\d+"]


def scan(d):
    hits = {}
    for p in sorted(d.rglob("*")):
        if not p.is_file() or p.suffix == ".wav":
            continue
        raw = p.read_bytes()
        t = gzip.decompress(raw).decode() if raw[:2] == b"\x1f\x8b" else raw.decode()
        t = re.sub(r"\b(?:Next)?PointeeId\b|\"schema\": \"[\w-]+\"", "", t)  # public element names; cases-file key
        h = sorted({m for pat in DENY for m in re.findall(pat, t)})
        if p.suffix != ".md" and p.name != "manifest.json" and p.name != "cases.json":
            h = [x for x in h if not x.startswith("REQ-")]
        h = [x for x in h if not re.fullmatch(r"REQ-LIVE-SET-STRUCTURE-\d{3}", x)]
        if h:
            hits[str(p.relative_to(d))] = h
    return hits


def pick(got, want):  # keyed state values: only the listed track numbers are judged (spec comparison rules)
    return {k: got.get(k) for k in want} if isinstance(want, dict) else got


def judged(got, want):
    return pick(got, want) == want


def main():
    d = PKG
    out = {"package": str(d)}
    man = json.loads((d / "manifest.json").read_text())
    files = sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file() and p.name != "manifest.json")
    out["hash_mismatches"] = [f["path"] for f in man["files"] if sha((d / f["path"]).read_bytes()) != f["sha256"]
                              or (d / f["path"]).stat().st_size != f["bytes"]]
    out["inventory_differences"] = sorted(set(files) ^ {f["path"] for f in man["files"]})
    out["manifest_sha256"] = sha((d / "manifest.json").read_bytes())
    links = md_links(d)
    out["links"] = {k: len(v) for k, v in links.items()}
    out["unresolved_links"] = {k: [t for t, ok in v if not ok] for k, v in links.items() if not all(ok for _, ok in v)}
    cases = json.loads((d / "cases.json").read_text())["cases"]
    out["missing_inputs"] = [c["input"] for c in cases if not (d / c["input"]).is_file()]
    als = sorted(d.glob("fixtures/*.als"))
    out["container_problems"] = {p.name: container(p.read_bytes()) for p in als if container(p.read_bytes())}
    decoded = {p.name: gzip.decompress(p.read_bytes()) for p in als}
    out["distinct_fixtures"] = len(set(decoded.values())) == len(decoded)
    out["reading_copy_equal"] = (d / "fixtures/T11-MIN.xml").read_bytes() == decoded["T11-MIN.als"]
    out["fixture_only_ascii"] = all(all(b < 128 for b in v) for v in decoded.values())
    base = (d / "fixtures/T11-MIN.als").read_bytes()
    _, _, v0, x0, r0 = judge(base)
    out["T11-MIN"] = {"violations": v0, "exclusions": x0, "repairs": r0, "cross_release": cross_release(base)}
    results, problems = {}, {}
    for c in cases:
        if c["action"] == "compute-identity":
            s = (d / c["input"]).read_bytes()
            with wave.open(str(d / c["input"])) as w:
                ident = {"OriginalFileSize": len(s), "OriginalCrc": crc16(s[:16384]), "DefaultDuration": w.getnframes(),
                         "DefaultSampleRate": w.getframerate()}
                form = (w.getnchannels(), w.getsampwidth(), w.getcomptype())
            x = json.loads((T11 / "out/x-crc.json").read_text())
            xr = next(r for r in x["runs"] if r["input"].startswith("fixture T11-tone.wav"))
            ok = ident == c["expected"]["identity"] and crc16(b"123456789") == 65256 and xr["x86_result"] == ident[
                "OriginalCrc"] and xr["sha256"] == sha(s[:16384]) and form == (2, 2, "NONE")
            results[c["id"]] = {"identity": ident, "x86_on_prefix": xr["x86_result"], "wav_form": form, "agrees": ok}
            if not ok:
                problems[c["id"]] = results[c["id"]]
            continue
        raw = (d / c["input"]).read_bytes()
        outcome, state, viol, excl, rep = judge(raw, c["setup"])
        exp = c["expected"]
        agree = outcome == exp["outcome"] and all(state is not None and judged(state[k], v) for k, v in exp.get("state", {}).items())
        iso = (len(viol) == 1) if exp["outcome"] == "refused" else (not viol)
        results[c["id"]] = {"outcome": outcome, "violations": viol, "exclusions": excl, "repairs": rep,
                            "agrees": agree, "isolated": iso,
                            "judged": {k: pick(state[k], v) for k, v in exp.get("state", {}).items()} if state else None}
        if not agree or not iso or excl:
            problems[c["id"]] = results[c["id"]]
    out["cases"] = results
    out["problems"] = problems
    out["sanitization_hits"] = scan(d)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
