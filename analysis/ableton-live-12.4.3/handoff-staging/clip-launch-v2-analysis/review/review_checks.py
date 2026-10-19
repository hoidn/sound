"""Reviewer's mechanical checks of the clip-launch-v2 package (analyst side; never shipped).

usage: python3 -I -B review_checks.py <package dir> > <out.json>
Checks: supersession (v1 digest, v1 files, carried records, carried launch content), fixture form,
per-fixture differences from the version's reference fixture, Live Set structure rules read from
SPEC-LIVE-SET-STRUCTURE r1 (own implementation; older versions after the renames their conversion
steps make), the sample, contract examples, links, inventory and hashes, and a hygiene scan.
"""
import hashlib, json, math, re, struct, sys, wave
import xml.etree.ElementTree as ET
from pathlib import Path

PKG = Path(sys.argv[1]).resolve()
REPO = Path(__file__).resolve().parents[5]
V1 = REPO / "handoff/clip-launch-v1"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import restate as R  # noqa: E402  (reviewer restatement: L, G, compute)

SC, SA, AR, SN = R.SC, R.SA, R.AR, R.SN
OLD = R.OLD
out = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def schema(v):
    r = ET.parse(SCHEMA / f"{v}.txt").getroot()
    return {c.tag: {f.tag: (f.get("Class"), f.get("Type")) for f in c} for c in r}


SCH = {v: schema(v) for v in ("12.0_12402", "12.0_12117", "11.0_405")}

# ---- supersession ----
idx = (REPO / "handoff/index.md").read_text()
row = next(l for l in idx.splitlines() if l.startswith("| [clip-launch-v1]"))
v1m = json.loads((V1 / "manifest.json").read_text())
mm = json.loads((PKG / "manifest.json").read_text())
out["v1_digest"] = {"file": sha((V1 / "manifest.json").read_bytes()),
                    "catalog": re.search(r"`([0-9a-f]{64})`", row).group(1),
                    "claimed": mm["supersession"]["superseded_manifest_sha256"]}
out["v1_digest"]["all_equal"] = len(set(out["v1_digest"].values()) - {True}) == 1
out["v1_files_mismatch"] = [f["path"] for f in v1m["files"] if sha((V1 / f["path"]).read_bytes()) != f["sha256"]]
v1c = {c["id"]: c for c in json.loads((V1 / "cases.json").read_text())["cases"]}
cases = json.loads((PKG / "cases.json").read_text())["cases"]
by = {c["id"]: c for c in cases}
out["carried_records"] = {"identical_content": sum(by[k] == v for k, v in v1c.items()),
                          "identical_serialization": sum(json.dumps(by[k], indent=1) == json.dumps(v, indent=1)
                                                         for k, v in v1c.items()),
                          "v1_cases": len(v1c)}


def launch_content(root):
    ls = root.find("LiveSet")
    lc = {"root": sorted(root.attrib.items()),
          "set": [(c.tag, sorted(c.attrib.items())) for c in ls if c.tag in ("GlobalQuantisation", "AutoQuantisation")]}
    for p in (SC, SA, AR):
        clip = ls.find(p)
        if clip is not None:
            lc[p] = [ET.tostring(c, encoding="unicode").strip().replace("\t", "").replace("\n", "").replace("  ", "")
                     for c in clip if c.tag in R.LAUNCH or c.tag in OLD]
    s = ls.find(SN)
    if s is not None:
        fa = s.find("FollowAction")
        lc["scene_fa"] = None if fa is None else [(g.tag, g.get("Value")) for g in fa]
    return lc


def norm(xs):
    return [re.sub(r"\s+", "", x) for x in xs] if isinstance(xs, list) and xs and isinstance(xs[0], str) else xs


carry = {}
for k in v1c:
    a = launch_content(ET.parse(V1 / v1c[k]["input"]).getroot())
    b = launch_content(ET.parse(PKG / by[k]["input"]).getroot())
    carry[k] = {"v1_locations": list(a), "changed": [x for x in a if norm(a[x]) != norm(b.get(x))],
                "added_locations": [x for x in b if x not in a]}
out["carried_launch_content_changed"] = {k: v["changed"] for k, v in carry.items() if v["changed"]}
out["carried_added_locations"] = sorted({tuple(v["added_locations"]) for v in carry.values()})

# ---- fixture form and differences ----
fx = sorted((PKG / "fixtures").glob("*.xml"))
raws = {p.name: p.read_bytes() for p in fx}
out["fixture_form"] = {"count": len(fx), "distinct": len(set(raws.values())),
                       "not_ascii_lf_final_newline": [n for n, b in raws.items()
                                                      if not (b.isascii() and b"\r" not in b and b.endswith(b"\n"))],
                       "space_indented_lines": [n for n, b in raws.items() if re.search(rb"\n +<", b)]}
REF = {"12.0_12402": "CLIP-LAUNCH-001.xml", "11.0_405": "CLIP-LAUNCH-041.xml", "12.0_12117": "CLIP-LAUNCH-047.xml"}


def flat(e, path=""):
    d = {}
    seen = {}
    for c in e:
        seen[c.tag] = seen.get(c.tag, 0) + 1
        p = f"{path}/{c.tag}[{seen[c.tag]}]"
        d[p] = tuple(sorted(c.attrib.items()))
        d.update(flat(c, p))
    return d


diffs = {}
for p in fx:
    root = ET.fromstring(raws[p.name])
    v = root.get("MinorVersion")
    ref = flat(ET.fromstring(raws[REF[v]]).find("LiveSet"))
    cur = flat(root.find("LiveSet"))
    d = sorted({k for k in ref.keys() | cur.keys() if ref.get(k) != cur.get(k)})
    # collapse to the shortest prefixes
    short = [k for k in d if not any(k != j and k.startswith(j + "/") for j in d)]
    diffs[p.name] = {"version": v, "vs": REF[v], "changed": [re.sub(r"\[1\]", "", k) for k in short]}
out["fixture_differences"] = diffs


# ---- structure rules (own reading of SPEC-LIVE-SET-STRUCTURE r1) ----
def converted(root):
    """Renames made by conversion steps above 405 that the rules depend on: 407 (scene Value -> Name),
    411 (ColorIndex -> Color), 414 (SceneNames -> Scenes), 12020 (MasterTrack -> MainTrack)."""
    root = ET.fromstring(ET.tostring(root))
    ls = root.find("LiveSet")
    if root.get("MinorVersion") == "11.0_405":
        sn = ls.find("SceneNames")
        for s in sn:
            assert s.find("Name") is None          # step 407 reports an error for an existing Name
            name = s.attrib.pop("Value", "")
            ET.SubElement(s, "Name", Value=name)
        sn.tag = "Scenes"
        ls.find("MasterTrack").tag = "MainTrack"
    return root


def structure(root, sch):
    """Returns the list of refusal reasons and unknown shapes under the traced rules."""
    ref, unk = [], []
    ls = root.find("LiveSet")

    def walk(e, cls):
        fields = sch.get(cls, {})
        names = [c.tag for c in e]
        for n in set(names):
            if names.count(n) > 1 and fields.get(n, (None, None))[1] in ("0", "-4"):
                ref.append(f"REQ-001 repeated {cls}/{n}")
        for c in e:
            f = fields.get(c.tag)
            if f is None:
                continue                                  # undeclared: skipped by the reader
            if f[1] == "-4" and "Value" not in c.attrib:
                ref.append(f"REQ-001 base value without Value {cls}/{c.tag}")
            elif f[1] == "0":
                walk(c, f[0])
            elif f[1] == "-1":
                ids = [i.get("Id") for i in c]
                if len(ids) != len(set(ids)) or any(i is not None and int(i) < 0 for i in ids):
                    ref.append(f"REQ-016 list Ids {cls}/{c.tag}")
                for i in c:
                    if i.tag not in sch:
                        ref.append(f"REQ-001 unknown list class {i.tag}")
                    else:
                        walk(i, i.tag)
    walk(ls, "LiveSet")
    tracks = list(ls.find("Tracks")) if ls.find("Tracks") is not None else []
    kinds = [t.tag for t in tracks]
    if not any(k in ("AudioTrack", "MidiTrack", "GroupTrack") for k in kinds):
        ref.append("REQ-002 no player track")
    if "ReturnTrack" in kinds and any(k != "ReturnTrack" for k in kinds[kinds.index("ReturnTrack"):]):
        ref.append("REQ-002 player track after a return track")
    if any(t.find("TrackGroupId") is not None and t.find("TrackGroupId").get("Value") != "-1" for t in tracks):
        ref.append("REQ-002 grouped track (outside T1)")
    scenes = ls.find("Scenes")
    nsc = 0 if scenes is None else len(scenes)
    returns = len([k for k in kinds if k == "ReturnTrack"])
    for t in tracks:
        if t.tag in ("AudioTrack", "MidiTrack"):
            m = len(t.findall("DeviceChain/MainSequencer/ClipSlotList/ClipSlot"))
            fz = t.find("DeviceChain/FreezeSequencer")
            f = 0 if fz is None else len(fz.findall("ClipSlotList/ClipSlot"))
            if m != f:
                ref.append(f"REQ-006 freeze slots {f} != session slots {m} ({t.tag})")
            if m != nsc:
                unk.append(f"REQ-006 U session slots {m} != scenes {nsc}")
        if len(t.findall("DeviceChain/Mixer/Sends/TrackSendHolder")) > returns:
            ref.append("REQ-013 more send holders than returns")
        if t.find("DeviceChain/AudioOutputRouting/Target") is None or \
                t.find("DeviceChain/AudioOutputRouting/Target").get("Value") != "AudioOut/Main":
            unk.append("REQ-005 output not the main track")
    for k in ("MainTrack", "PreHearTrack"):
        e = ls.find(k)
        if e is not None and e.findall("DeviceChain/Mixer/Sends/TrackSendHolder"):
            ref.append(f"REQ-013 {k} has sends")
    sp = ls.find("SendsPre")
    if (0 if sp is None else len(sp)) != returns:
        unk.append("REQ-013 SendsPre count != returns")
    # pointees: AutomationTarget / ModulationTarget elements (the classes the reader registers)
    pts = [e for e in ls.iter() if e.tag in ("AutomationTarget", "ModulationTarget")]
    pid = [e.get("Id") for e in pts]
    if any(i in (None, "0") for i in pid):
        ref.append("REQ-015 pointee without Id or with Id 0")
    nums = [int(i) for i in pid if i not in (None, "0")]
    npi = ls.find("NextPointeeId")
    if (1 if npi is None else int(npi.get("Value"))) <= max([0] + nums):
        ref.append("REQ-015 NextPointeeId not above the largest pointee Id")
    if len(nums) != len(set(nums)):
        unk.append("REQ-015 duplicate pointee Id")
    envs = {e.find("EnvelopeTarget/PointeeId").get("Value") for e in ls.iter("AutomationEnvelope")}
    if not envs <= set(pid):
        unk.append("REQ-014 envelope target without pointee")
    devs = [d for d in ls.iter("Devices") if len(d)]
    if devs:
        unk.append("REQ-012 devices present")
    return sorted(set(ref)), sorted(set(unk)), {"tracks": kinds, "scenes": nsc, "pointees": len(pts),
                                                 "max_pointee": max(nums), "next_pointee": None if npi is None else
                                                 int(npi.get("Value"))}


st = {}
for p in fx:
    root = ET.fromstring(raws[p.name])
    v = root.get("MinorVersion")
    conv = converted(root)
    # rules are read against the class names a 12402 reader sees after conversion
    r, u, facts = structure(conv, SCH["12.0_12402"] if v != "11.0_405" else {**SCH["11.0_405"], **{
        "LiveSet": {**SCH["11.0_405"]["LiveSet"], "Scenes": ("RemoteableList", "-1"),
                    "MainTrack": ("MasterTrack", "0")}}})
    st[p.name] = {"version": v, "refusals": r, "unknown": u, **facts}
expect = {c["input"].split("/")[-1]: c["expected"]["outcome"] for c in cases if c["input"]}
out["structure"] = {"refused_by_structure": {k: v["refusals"] for k, v in st.items() if v["refusals"]},
                    "unknown_shapes": {k: v["unknown"] for k, v in st.items() if v["unknown"]},
                    "facts_by_version": {v: next(x for x in st.values() if x["version"] == v) for v in REF},
                    "fixtures_expected_refused": sorted(k for k, o in expect.items() if o == "refused")}
# a 405 document with the audit tool's recommended 12402 scene form would hold Scene/Name before step 407
out["structure"]["audit_advice_405"] = ("the 11.0_405 schema declares LiveSet/SceneNames and a Scene with a Value "
                                        "field; it declares no LiveSet/Scenes: " +
                                        str(("SceneNames" in SCH["11.0_405"]["LiveSet"],
                                             "Scenes" in SCH["11.0_405"]["LiveSet"],
                                             "Value" in SCH["11.0_405"]["Scene"],
                                             "Name" in SCH["11.0_405"]["Scene"])))

# ---- sample ----
w = PKG / "fixtures/Samples/T11-tone.wav"
with wave.open(str(w)) as f:
    params = (f.getnchannels(), f.getsampwidth(), f.getframerate(), f.getnframes())
    frames = f.readframes(f.getnframes())
gen = b"".join(struct.pack("<hh", v, v) for v in (int(round(8192 * math.sin(2 * math.pi * 441 * i / 44100)))
                                                   for i in range(44100)))
out["sample"] = {"bytes": w.stat().st_size, "channels_width_rate_frames": params, "equals_generated_sine": frames == gen,
                 "max_abs_diff": max(abs(a - b) for a, b in zip(struct.unpack(f"<{len(frames)//2}h", frames),
                                                                struct.unpack(f"<{len(gen)//2}h", gen)))}

# ---- contract examples (REQ-012, 013, 015 to 017) ----
ex = {}


def chances(a, b):
    v = R.read_follow(None)
    fa = ET.Element("FollowAction")
    R.add(fa, "FollowChanceA", a)
    R.add(fa, "FollowChanceB", b)
    v = R.read_follow(fa)
    return v["FollowChanceA"], v["FollowChanceB"]


for a, b, ra, rb in [("30", "30", 50, 50), ("1", "2", 33, 67), ("1", "7", 13, 87), ("3", "5", 38, 62),
                     ("5", "3", 63, 37), ("1", "199", 1, 99), ("0", "50", 0, 100), ("0.25", "0.75", 25, 75),
                     ("99.5", "0.5", 100, 0), ("100", "0", 100, 0), ("150", "50", 75, 25), ("-10", "50", 0, 100),
                     ("150", "-50", 100, 0), ("-10", "-10", 50, 50)]:
    ex[f"REQ-012 {a}/{b}"] = chances(a, b) == (ra, rb)
ex["REQ-012 q of 30/30 is 49.999996"] = abs(R.f32(30.0 / R.f32(60.0 / 100.0)) - 49.999996) < 1e-6
for x, y in [(2.0000001, 2.0), (3.0000002, 11531521 / 3843840), (1e-8, 0.0), (1.3333333, 4 / 3),
             (3.902347652347652e-07, 5.203130203130203e-07), (100000.00000143086, 100000.00000156094),
             (1.3007825507825505e-07, 2.6015651015651016e-07)]:
    ex[f"REQ-013 {x!r}"] = R.L(x) == y
hh = 1 / 3843840
ex["REQ-013 one step below nearest h/2"] = math.nextafter(hh / 2, 0) == 1.3007825507825505e-07 and hh == 2.6015651015651016e-07
for q, n, d, g in [(4, 3, 4, 3), (4, 6, 8, 3), (4, 7, 8, 3.5), (1, 99, 16, 198), (5, 6, 8, 2)]:
    ex[f"REQ-015 G({q},{n}/{d})"] = R.G(q, n, d) == g
ex["REQ-016 examples"] = (R.compute("clip-grid", {"clip_value": 5, "global_value": 4, "clip_time_signature": [6, 8],
                                                  "song_time_signature": [3, 4]})["grid"] == 3 and
                          R.compute("clip-grid", {"clip_value": 0, "global_value": 4, "clip_time_signature": [6, 8],
                                                  "song_time_signature": [4, 4]})["grid"] == 4 and
                          all(R.compute("clip-grid", {"clip_value": 8, "global_value": q, "clip_time_signature": [4, 4],
                                                      "song_time_signature": [4, 4]})["grid"] == 1 for q in range(14)))
for t, p in [(3.99, 3.990000104062604), (4 - 1e-9, 4.0), (4 + 1e-9, 4.0), (0.13, 0.12999994796869796),
             (4.000000260156511, 4.000000260156511)]:
    ex[f"REQ-017 p({t!r})"] = R.L(t) == p
B = lambda t, g, a=0.0: R.compute("grid-boundary", {"beat": t, "grid": g, "anchor": a})["boundary"]  # noqa: E731
ex["REQ-017 B examples"] = (B(5.3, 4.0) == 8 and B(4.0, 4.0) == 4 and B(3.99, 4.0) == 4 and
                            B(4.000000260156511, 4.0) == 8 and B(0.4, 1 / 3) == 2 / 3 and B(9.0, 3.0, 8.0) == 11 and
                            B(10 / 3, 2 / 3) == 4 and B(4 / 3, 2 / 3) == 4 / 3)
from fractions import Fraction  # noqa: E402
NOTE = {5: Fraction(2), 6: Fraction(4, 3), 7: Fraction(1), 8: Fraction(2, 3), 9: Fraction(1, 2), 10: Fraction(1, 3),
        11: Fraction(1, 4), 12: Fraction(1, 6), 13: Fraction(1, 8)}
sweep_ok, sweep_n = True, 0
for qq, gl in NOTE.items():
    k = 1
    while gl * k <= 64:
        for s in (-1, 1):
            t = float(gl * k + Fraction(s, 3843840))
            sweep_ok &= B(t, R.G(qq, 4, 4)) == float(gl * k if s < 0 else gl * (k + 1))
            sweep_n += 1
        k += 1
ex[f"REQ-017 one lattice step either side of every note-grid line to 64, anchor 0 ({sweep_n} beats)"] = sweep_ok
out["contract_examples"] = ex

# ---- links, inventory, hashes ----
links = {}
for md in sorted(PKG.glob("*.md")):
    for t in re.findall(r"\]\(([^)]+)\)", md.read_text()):
        path, _, anchor = t.partition("#")
        tgt = (PKG / path) if path else md
        ok = not t.startswith(("http", "/")) and ".." not in path and tgt.is_file()
        if ok and anchor and tgt.suffix == ".md":
            heads = [re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", tgt.read_text(), re.M)]
            ok = anchor in heads
        links.setdefault(md.name, []).append((t, ok))
out["links"] = {k: {"count": len(v), "unresolved": [t for t, ok in v if not ok]} for k, v in links.items()}
files = sorted(p for p in PKG.rglob("*") if p.is_file() and p.name != "manifest.json")
listed = {f["path"]: f for f in mm["files"]}
out["inventory"] = {"files": len(files), "listed": len(listed),
                    "differences": sorted({str(p.relative_to(PKG)) for p in files} ^ set(listed)),
                    "hash_or_size_mismatch": [k for k, f in listed.items() if not (PKG / k).is_file() or
                                              sha((PKG / k).read_bytes()) != f["sha256"] or
                                              (PKG / k).stat().st_size != f["bytes"]],
                    "symlinks": [str(p) for p in PKG.rglob("*") if p.is_symlink()],
                    "case_count": (mm["case_count"], len(cases)),
                    "manifest_sha256": sha((PKG / "manifest.json").read_bytes())}

# ---- hygiene ----
DENY = [r"0x[0-9a-fA-F]{5,}", r"FUN_", r"\bA[A-Z][a-z]+[A-Z]\w*::", r"::", r"\bO[A-Z][a-z]+(?:Clip|Fire|Audio)\w*",
        r"\bL[A-Z][a-z]+Song\w*", r"\bASong\b", r"\bAClip\b", r"AFollowAction", r"UserFloat", r"vtable", r"decompil",
        r"pseudocode", r"disassembl", r"Ghidra", r"\bgdb\b", r"xexec", r"harness", r"getter", r"helper",
        r"analysis/", r"raw/", r"wiki/", r"\.\./", r"T11", r"t11", r"\bX2\b", r"\bS5\b", r"s5-", r"PRB-", r"CLC-",
        r"\bQ-0\d\d", r"\bA[1-7]\b", r"\bF[1-9]\b", r"RVC-", r"\bPBC-", r"REQ-PLAYBACK", r"REQ-LIVE-SET", r"ADR",
        r"probe", r"packet", r"translator", r"registry", r"offset", r"frint", r"fmadd", r"maxsd", r"fmaxnm",
        r"cvtt", r"fcvtzs", r"jump table", r"sentinel", r"Remoteable\w*", r"Engine", r"slice", r"x86", r"arm64",
        r"glibc", r"Linux"]
hy = {}
for p in [*files, PKG / "manifest.json"]:
    if p.suffix not in (".md", ".json", ".xml"):
        continue
    text = p.read_text()
    hits = {}
    for pat in DENY:
        for m in re.finditer(pat, text):
            hits.setdefault(m.group(0), 0)
            hits[m.group(0)] += 1
    if hits:
        hy[str(p.relative_to(PKG))] = hits
xml_hits = {}
for k, v in list(hy.items()):
    if k.endswith(".xml"):
        for h, n in v.items():
            xml_hits[h] = xml_hits.get(h, 0) + n
        del hy[k]
out["hygiene"] = {"non_fixture_hits": hy, "fixture_hits_total": xml_hits}
print(json.dumps(out, indent=1, default=str))
