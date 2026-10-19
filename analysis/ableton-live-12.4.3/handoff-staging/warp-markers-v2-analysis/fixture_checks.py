"""Fixture checks for check_v2.py (analyst side): the T1.1 structure checkers run unchanged as subprocesses,
the single-change comparison against base.xml, warp-markers-v1 and T11-MIN, and the fixture and WAV report.
Writes schema-check.jsonl and fixture-audit.json in this directory; read-only elsewhere."""
import difflib, json, re, shutil, subprocess, sys, tempfile, wave
import xml.etree.ElementTree as ET
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_v2 as B  # noqa: E402
from v2_meta import T11, V1, sha  # noqa: E402

ROOT, STAGE = B.ROOT, B.STAGE
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
CLIP_X = "/".join(B.CLIP_PATH[1:])


# ---- fixtures: structure checks (T1.1 checkers), single change, WAV and sample reference ----
def structure_checks():
    xml = sorted(str(p) for p in (STAGE / "fixtures").glob("*.xml"))
    py = [sys.executable, "-I", "-B"]
    sc = subprocess.run(py + [str(ROOT / T11 / "schema_check.py"), str(SCHEMA), *xml], capture_output=True, text=True,
                        check=True).stdout
    (HERE / "schema-check.jsonl").write_text("".join(
        json.dumps({**json.loads(line), "doc": Path(json.loads(line)["doc"]).name}, sort_keys=True) + "\n"
        for line in sc.splitlines()))
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(STAGE, Path(tmp) / "warp-markers-v2")
        subprocess.run(py + [str(ROOT / T11 / "fixture_audit.py"), str(SCHEMA), tmp, str(HERE / "fixture-audit.json")],
                       capture_output=True, text=True, check=True)
    audit = json.loads((HERE / "fixture-audit.json").read_text())["releases"][0]
    rows = [json.loads(line) for line in sc.splitlines()]
    problems = [r["doc"] for r in rows if r["deviations"]]
    for f in audit["fixtures"]:
        if f["kind"] == "live-set" and (f["refusals"] or f["unknown_shapes"]):
            problems.append(f["fixture"])
        problems += [c["id"] for c in f["cases"] if f["kind"] == "live-set" and c["effect"] != "consistent"]
    return {"schema_deviation_free": sum(not r["deviations"] for r in rows), "documents": len(rows),
            "audit_summary": audit["summary"], "problems": problems}


def changed_lines(a, b):
    return [ln for ln in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0)
            if ln[:1] in "+-" and not ln.startswith(("+++", "---"))]


def single_change():
    """Each document against base.xml (changes must lie inside the clip, or inside the MIDI device list), and the
    same change as in warp-markers-v1 (indentation ignored); base.xml against the generator's T11-MIN.xml."""
    base = (STAGE / "fixtures/base.xml").read_text()
    lines = base.splitlines()
    clip = (next(i for i, s in enumerate(lines) if "<AudioClip " in s), next(i for i, s in enumerate(lines)
                                                                                 if "</AudioClip>" in s))
    v1base = (ROOT / V1 / "fixtures/base.xml").read_text()
    out, bad = {}, []
    for p in sorted((STAGE / "fixtures").glob("*.xml")):
        if p.name == "base.xml":
            continue
        diff = changed_lines(base, p.read_text())
        hunks = [ln for ln in difflib.unified_diff(lines, p.read_text().splitlines(), lineterm="", n=0)
                 if ln.startswith("@@")]
        starts = [int(re.match(r"@@ -(\d+)", h).group(1)) for h in hunks]
        inside = all(clip[0] < s <= clip[1] + 1 for s in starts)
        same_as_v1 = None
        v1 = ROOT / V1 / "fixtures" / p.name
        if v1.is_file() and p.name != "simpler-empty-markers.xml":
            strip = sorted(ln[0] + ln[1:].strip() for ln in diff)
            same_as_v1 = strip == sorted(ln[0] + ln[1:].strip() for ln in changed_lines(v1base, v1.read_text()))
            bad += [] if same_as_v1 and inside else [p.name]
        elif p.name == "simpler-empty-markers.xml":
            bad += [] if all(not clip[0] < s <= clip[1] + 1 for s in starts) else [p.name]
        else:
            bad += [] if inside else [p.name]
        out[p.name] = {"changed_lines": len(diff), "inside_clip": inside, "same_change_as_v1": same_as_v1,
                       "diff": diff if len(diff) <= 12 else diff[:6] + ["..."] + diff[-6:]}
    t11 = (ROOT / T11 / "fixtures/T11-MIN.xml").read_text()
    # review RVW2-01: base.xml is T11-MIN without its two devices (and NextPointeeId 67), plus the clip change
    t11 = re.sub(r"<Devices>\n.*?</Devices>", "<Devices />", t11, flags=re.S)
    assert t11.count('<NextPointeeId Value="69" />') == 1
    t11 = t11.replace('<NextPointeeId Value="69" />', '<NextPointeeId Value="67" />')
    tdiff = list(difflib.unified_diff(t11.splitlines(), lines, lineterm="", n=0))
    t_starts = [int(re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", h).group(1)) for h in tdiff if h.startswith("@@")]
    base_vs_t11 = {"changed_lines": len(changed_lines(t11, base)),
                   "inside_clip": all(clip[0] < s <= clip[1] + 1 for s in t_starts)}
    if not base_vs_t11["inside_clip"]:
        bad.append("base.xml vs T11-MIN.xml")
    return {"documents": out, "base_vs_t11_min": base_vs_t11, "problems": bad}


def fixture_report():
    rep, raws = {}, {}
    for p in sorted((STAGE / "fixtures").iterdir()):
        raw = p.read_bytes()
        raws.setdefault(sha(raw), []).append(p.name)
        if p.suffix == ".wav":
            with wave.open(str(p)) as w:
                rep[p.name] = {"bytes": len(raw), "channels": w.getnchannels(), "sample_width": w.getsampwidth(),
                               "rate": w.getframerate(), "frames": w.getnframes(), "all_zero": set(raw[44:]) == {0},
                               "riff_chunks_only_fmt_data": raw[12:16] == b"fmt " and raw[36:40] == b"data",
                               "identical_to_v1": raw == (ROOT / V1 / "fixtures/sample.wav").read_bytes(),
                               "mtime": int(p.stat().st_mtime)}
            continue
        root = ET.fromstring(raw)
        sref = root.find("LiveSet/" + CLIP_X + "/SampleRef")
        rep[p.name] = {"bytes": len(raw), "ascii": raw.isascii(), "lf_only": b"\r" not in raw,
                       "final_newline": raw.endswith(b"\n"), "root_attrs": root.attrib,
                       "holders": [e.tag for e in root.iter() if e.tag in ("AudioClip", "SampleWarpProperties")],
                       "sample_ref_matches_wav": [sref.find(f"FileRef/{k}").get("Value") for k in
                                                  ("OriginalFileSize", "OriginalCrc")] ==
                       [str(len(B.WAV)), str(B.mf.crc16(B.WAV[:16384]))]}
    dup = [v for v in raws.values() if len(v) > 1]
    return {"files": rep, "duplicates": dup}
