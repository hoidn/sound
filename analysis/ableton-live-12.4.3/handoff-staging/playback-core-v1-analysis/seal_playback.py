"""Check and seal the playback-core-v1 candidate (analyst side; never shipped).

Usage: python3 -I -B seal_playback.py            (after build_playback.py build)
       python3 -I -B seal_playback.py verify DIR  (hashes, links, inputs and deny list of a package copy)
Checks: Live Set validity (r2/t11-structure-v1 schema_check.py and fixture_audit.py, unchanged); fixture and WAV form;
cross-check of the generated expectations against the SPEC-PLAYBACK-CORE r1 case values and the T1.3 extracted-execution
results; case and manifest consistency; sanitization deny list; links. Writes manifest.json files[],
author-validation.json and traceability.json. Requires the shipped schema file (read only) for the structure checks.
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import wave
import zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent / "playback-core-v1"
T11 = ROOT / "analysis/ableton-live-12.4.3/r2/t11-structure-v1"
T13 = ROOT / "analysis/ableton-live-12.4.3/r2/t13-playback-v1"
X2 = ROOT / "analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1/results/launch.json"
SCHEMA = "/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt"
sys.path.insert(0, str(HERE))
import manifest_meta as mm  # noqa: E402
import model_playback as m  # noqa: E402
from cases_playback import CASES as DEFS  # noqa: E402

DENY = [r"analysis/", r"wiki/", r"\.\./", r"0x[0-9a-fA-F]{4,}", r"FUN_", r"disassembl", r"decompil", r"pseudocode",
        r"Ghidra", r"vtable", r"corpus", r"excerpt", r"matching", r"\bslice", r"harness", r"xexec", r"\bgdb\b",
        r"\bpoke", r"::", r"\b[OA][A-Z][a-z]+[A-Z]\w+", r"\bS-cond", r"\bA[1-7]\b", r"PBC-", r"CLC-", r"PRB-", r"\bQ-0",
        r"\bADR", r"SPEC-(?!PLAYBACK-CORE\b)", r"REQ-(?!PLAYBACK-CORE-)", r"T11", r"\bt13", r"\bT1\.\d", r"x2-",
        r"Drums Lesson", r"Slide", r"\bRim\b", r"APC20", r"Sample Reference", r"Wavetable", r"Engine",
        r"/home/", r"/var/", r"/tmp/", r"\+0x", r"ev_[0-9a-f]", r"powf", r"exp10f", r"sinf", r"fmadd", r"fcvtps",
        r"evidence appendix", r"research"]
ALLOWED_HITS = {"AGENTS.md": {"decompil", "research"}}  # forbidden-inputs list, as in released packages
SPEC_ON = {  # note-on samples (each an allowed set) that SPEC-PLAYBACK-CORE r1 states for the same configuration
    1: [[0], [6000], [24000], [32000], [80000], [96000], [1536000]], 2: [[5143], [20572], [82286], [144000]],
    3: [[5513], [73500]], 4: [[20672], [20671875]], 5: [[87327]], 6: [[30858], [216000]],
    7: [[32000, 32001], [85334], [256000, 256001]], 8: [[0], [20572], [329143]], 10: [[66715]], 66: [[192000]],
    67: [[155820]], 69: [[155820]], 70: [[0]], 72: [[105000], [189000]], 75: [[108000]], 81: [[96219]],
    82: [[128000, 128001]]}
SPEC_JUMPS = {11: [96000, 192000, 288000, 384000], 12: [82286, 164572, 246858, 329144], 13: [151200, 226800, 302400],
              14: [128000, 208000, 288000], 16: [24000, 48000, 72000]}
SPEC_TRIPLET = {2.6666666666666665: (78400, 85334), 1.3333333333333333: (39200, 42667),
                0.6666666666666666: (19600, 21334), 0.3333333333333333: (9800, 10667)}
SPEC_STEP = {"tone44.wav@48000": 3946001203, "tone48.wav@48000/12": 8589939712}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def payload(d):
    return sorted(p for p in d.rglob("*") if p.is_file() and p.name != "manifest.json")


def links(md, root):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
        if re.match(r"[a-z]+:", target):
            out.append((target, "external URL not allowed"))
            continue
        path, _, anchor = target.partition("#")
        dest = (md.parent / path).resolve() if path else md.resolve()
        ok = dest.is_file() and root.resolve() in dest.parents
        if ok and anchor:
            slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
            ok = anchor in slugs
        out.append((target, "ok" if ok else "UNRESOLVED"))
    return out


def text_of(p):
    raw = p.read_bytes()
    if p.suffix == ".als":
        return zlib.decompress(raw, 31).decode("utf-8")
    if p.suffix == ".wav":
        return ""
    return raw.decode("utf-8")


def verify(d):
    d = Path(d)
    man = json.loads((d / "manifest.json").read_text())
    files = payload(d)
    bad = [f["path"] for f in man["files"] if not (d / f["path"]).is_file()
           or sha((d / f["path"]).read_bytes()) != f["sha256"] or (d / f["path"]).stat().st_size != f["bytes"]]
    inventory = sorted({str(p.relative_to(d)) for p in files} ^ {f["path"] for f in man["files"]})
    rows = {str(p.relative_to(d)): links(p, d) for p in d.glob("*.md")}
    unresolved = {k: [t for t, s in v if s != "ok"] for k, v in rows.items() if any(s != "ok" for _, s in v)}
    cases = json.loads((d / "cases.json").read_text())["cases"]
    missing = sorted({x for c in cases for x in [c["input"], *c.get("samples", [])] if not (d / x).is_file()})
    deny = {}
    for p in [*files, d / "manifest.json"]:
        hits = sorted({mt for pat in DENY for mt in re.findall(pat, text_of(p))})
        hits = [h for h in hits if not any(h.startswith(a) for a in ALLOWED_HITS.get(p.name, ()))]
        if hits:
            deny[str(p.relative_to(d))] = hits
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "hash_or_size_mismatches": bad,
            "inventory_differences": inventory, "markdown_links": {k: len(v) for k, v in rows.items()},
            "unresolved_links": unresolved, "missing_case_inputs": missing, "deny_list_hits": deny,
            "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()},
            "symlinks": [str(p) for p in d.rglob("*") if p.is_symlink()]}


def structure():
    """Every .als through the T1.1 schema checker and the released-fixture audit (refusals of the validation walk)."""
    als = sorted(str(p) for p in (STAGE / "fixtures").glob("*.als"))
    out = subprocess.run([sys.executable, "-I", str(T11 / "schema_check.py"), SCHEMA, *als], capture_output=True,
                         text=True, check=True).stdout.splitlines()
    rows = [json.loads(x) for x in out]
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "playback-core-v1").symlink_to(STAGE)
        res = Path(tmp) / "audit.json"
        subprocess.run([sys.executable, "-I", "-B", str(T11 / "fixture_audit.py"), SCHEMA, tmp, str(res)],
                       capture_output=True, text=True, check=True)
        audit = json.loads(res.read_text())["releases"][0]
    return {"schema_check": {"documents": len(rows), "with_deviations": [r["doc"] for r in rows if r["deviations"]],
                             "errors": [r["doc"] for r in rows if "error" in r],
                             "rules_all_equal": len({json.dumps(r["rules"]["player_tracks"]) for r in rows}) == 1,
                             "rules": rows[0]["rules"]},
            "fixture_audit": audit["summary"],
            "fixture_audit_refusals": {e["fixture"]: e["refusals"] for e in audit["fixtures"] if e.get("refusals")},
            "fixture_audit_unknown_shapes": {e["fixture"]: e["unknown_shapes"] for e in audit["fixtures"]
                                             if e.get("unknown_shapes")}}


def fixture_form():
    probs, als = {}, {}
    for p in sorted((STAGE / "fixtures").glob("*.als")):
        raw = p.read_bytes()
        data = zlib.decompress(raw, 31)
        errs = []
        if raw[:10] != bytes.fromhex("1f8b0800000000000213"):
            errs.append("gzip header")
        if raw[-8:] != (zlib.crc32(data) & 0xFFFFFFFF).to_bytes(4, "little") + len(data).to_bytes(4, "little"):
            errs.append("gzip trailer")
        if b"\r" in data or not data.endswith(b"\n") or any(b > 127 for b in data):
            errs.append("not ASCII with LF endings")
        if not data.startswith(b'<?xml version="1.0" encoding="UTF-8"?>\n<Ableton MajorVersion="5" '
                               b'MinorVersion="12.0_12402" SchemaChangeCount="1">\n'):
            errs.append("envelope")
        if errs:
            probs[p.name] = errs
        als[p.name] = {"bytes": len(raw), "xml_bytes": len(data), "lines": data.count(b"\n")}
    wavs = {}
    for p in sorted((STAGE / "fixtures/Samples").glob("*.wav")):
        raw = p.read_bytes()
        with wave.open(str(p)) as w:
            info = {"channels": w.getnchannels(), "bits": 8 * w.getsampwidth(), "rate": w.getframerate(),
                    "frames": w.getnframes(), "comptype": w.getcomptype()}
        chunks, i = [], 12
        while i < len(raw):
            chunks.append(raw[i:i + 4].decode())
            i += 8 + int.from_bytes(raw[i + 4:i + 8], "little")
        info.update({"bytes": len(raw), "chunks": chunks, "riff_size_ok": int.from_bytes(raw[4:8], "little") == len(raw) - 8})
        wavs[p.name] = info
        if chunks != ["fmt ", "data"] or info["channels"] != 1 or info["bits"] != 16 or not info["riff_size_ok"]:
            probs[p.name] = ["WAV form"]
    return probs, als, wavs


def evidence_checks(cases):
    """Cross-check the generated expectations against the draft spec's case values and the retained X results."""
    errs = []
    by = {int(c["id"][-3:]): c for c in cases}
    ons = {n: [e["samples"] for e in c["expected"]["midi"]["events"] if e["type"] == "note-on"]
           for n, c in by.items() if "midi" in c["expected"]}
    for n, want in SPEC_ON.items():
        errs += [f"{n}: spec on {w} missing" for w in want if w not in ons[n]]
    for n, want in SPEC_JUMPS.items():
        got = by[n]["informative"]["song_loop_jump_samples"]
        if got[:len(want)] != want:
            errs.append(f"{n}: jumps {got[:len(want)]} != {want}")
    xb = {r["label"]: float.fromhex(r["B"]["hex"]) for r in json.loads(X2.read_text())["boundary_cases"]}
    for d, c in zip(DEFS, cases):
        src = d["source"]
        lab = next((k for k in xb if k.startswith("CLC") and src.endswith(k)), None)
        if lab and c["informative"]["launch_boundary_beat"] != xb[lab]:
            errs.append(f"{c['id']}: B {c['informative']['launch_boundary_beat']} != X {xb[lab]}")
        if src.startswith("PBC-020"):
            B, first = c["informative"]["launch_boundary_beat"], ons[int(c["id"][-3:])][0]
            if B in SPEC_TRIPLET:
                want = [SPEC_TRIPLET[B][0 if c["sample_rate"] == 44100 else 1]]
            else:
                want = [round(29400 * B)] if c["sample_rate"] == 44100 else [round(32000 * B), round(32000 * B) + 1]
            if first != want:
                errs.append(f"{c['id']}: first on {first} != spec {want}")
    p40 = [e for e in by[71]["expected"]["midi"]["events"]]
    want40 = [([96000 + 12000 * k + 96000 * p], "note-on") for p in (0, 1) for k in range(8)]
    if [(e["samples"], e["type"]) for e in p40 if e["type"] == "note-on"] != want40:
        errs.append("71: PBC-040 note-ons differ")
    if [e["samples"] for e in p40 if e["type"] == "note-off"] != [[102000 + 12000 * k + 96000 * p] for p in (0, 1) for k in range(8)]:
        errs.append("71: PBC-040 note-offs differ")
    ev73 = by[73]["expected"]["midi"]["events"]
    i = next(i for i, e in enumerate(ev73) if e["samples"] == [192000])
    if (ev73[i]["type"], ev73[i]["velocity"], ev73[i + 1]["type"], ev73[i + 1]["samples"]) != ("note-off", 64.0, "note-on", [192000]):
        errs.append("73: PBC-042 order or velocity")
    if [e for e in by[75]["expected"]["midi"]["events"] if e["samples"] == [108001]][0]["type"] != "note-off":
        errs.append("75: PBC-043 zero-length off")
    ev76 = by[76]["expected"]["midi"]["events"]
    if ev76[-1]["samples"] != [186000] or len(ev76) != 16:
        errs.append("76: PBC-044")
    if by[77]["expected"]["midi"]["events"][-1] != {"samples": [192000], "type": "note-off", "key": 60, "velocity": 64.0}:
        errs.append("77: PBC-045")
    if any(e["samples"] in ([120000], [126000]) for e in by[78]["expected"]["midi"]["events"]):
        errs.append("78: PBC-046")
    if by[79]["expected"]["midi"]["events"] != by[71]["expected"]["midi"]["events"]:
        errs.append("79: PBC-047")
    inc = {(r["semitones"], r["file_rate"], r["engine_rate"]): r["fixed_32_32"]
           for r in json.loads((T13 / "audio/results/inc.json").read_text())}
    for c in cases:
        if "audio" not in c["expected"]:
            continue
        rate = 44100 if "tone44" in c["samples"][0] else 48000
        semis = 12 if "12" in c["purpose"].split("PitchCoarse ")[-1][:2] else 0
        if c["informative"]["read_step_fixed_32_32"] != inc[(semis, rate, c["sample_rate"])]:
            errs.append(f"{c['id']}: step differs from X")
    gains = {r["sample_volume"]: float(r["engine_gain"]) for r in json.loads((T13 / "audio/results/gain.json").read_text())["rows"]}
    for k, g in {"0.5011872336272722": 0.5011872053146362, "0.0": 0.0003162277571391314, "10.0": 9.999999046325684,
                 "20.0": 15.848933219909668, "1.0": 1.0}.items():
        if gains[k] != g:
            errs.append(f"gain {k}: X {gains[k]} != {g}")
    t16 = np.round(0.5 * np.sin(2 * np.pi * np.arange(256) / 32.0) * 32767).astype(int)
    for r in json.loads((T13 / "audio/results/kernels.json").read_text()):
        if r["kernel"] in ("T16Lin", "T16Non"):
            got = m.render_clip(list(t16), 0, r["inc_fixed"], 96)
            if got != r["out_L"]:
                errs.append(f"kernel {r['kernel']} {r['inc']}: model differs from X")
    return errs


def consistency(cases, spec_text):
    errs = []
    scopes = set(mm.SCOPES)
    used = {r for c in cases for r in c["requirements"]}
    errs += [f"{c['id']}: requirement outside scope {r}" for c in cases for r in c["requirements"] if r not in scopes]
    errs += [f"scope without case: {r}" for r in sorted(scopes - used)]
    errs += [f"{c['id']}: unknown assumption {a}" for c in cases for a in c["stated_assumptions"] if a not in mm.ASSUMPTIONS]
    labels = set(mm.manifest_meta(0)["expectation_provenance_labels"])
    errs += [f"{c['id']}: provenance label" for c in cases if c["expectation_provenance"] not in labels]
    for r in sorted(scopes):
        if f"### {r}" not in spec_text:
            errs.append(f"spec.md lacks heading for {r}")
    for r in mm.UNRELEASED:
        if r not in spec_text or f"### {r}" in spec_text:
            errs.append(f"spec.md unreleased listing for {r}")
    for a, t in mm.ASSUMPTIONS.items():
        if f"**{a}.**" not in spec_text:
            errs.append(f"spec.md lacks {a}")
    return errs


def traceability(cases):
    ev = {
        "clock": "r2/t13-playback-v1/transport/results/fire.json (1,216 placements), sweep.json (4,000), plus_one_check.json "
                 "(240,000 classified); spec REQ-001/002",
        "stop": "r2/t13-playback-v1/transport/results/stop_resume.json", "loop": "r2/t13-playback-v1/transport/results/loop.json",
        "tempo": "spec REQ-003 binary32 tempo (S; DoSetTempo spb bit-equal in fire.json)",
        "launch": "r2/x2-notes-launch-v1/results/launch.json boundary_cases (B, X); r2/t13-playback-v1/launch/results.json "
                  "(pre-delay 0 on MIDI, 16 of 16); launch/matching.tsv and x86-fireclip-caller-tree.txt (path S)",
        "grid": "r2/x2-notes-launch-v1/results/launch.json grid table (REQ-CLIP-LAUNCH-015, 6,463 of 6,463)",
        "midi": "r2/t13-playback-v1/midi/results/clip-position.json (234 inputs), note-events.json (12 cases), cases.json",
        "midi-static": "r2/t13-playback-v1/midi/excerpts.jsonl (priority table, pass and cut rules; x86_64-only, spec A1)",
        "audio": "r2/t13-playback-v1/audio/results/inc.json (78), kernels.json, gain.json, quant.json; audio/summary.txt",
        "audio-static": "r2/t13-playback-v1/audio/corpus-excerpts.jsonl (first frame, fraction 0, past-end hold; spec A1, A3)",
        "structure": "r2/t11-structure-v1/make_fixture.py rules; schema_check.py and fixture_audit.py results in "
                     "author-validation.json"}
    amap = {"AS-1": "spec A1 (x86_64-only matches) and the arm64 equivalence of every X result",
            "AS-2": "spec A3", "AS-3": "spec A4", "AS-4": "SPEC-CLIP-LAUNCH A4 (grid anchor 0)",
            "AS-5": "glibc powf and exp10f bindings of REQ-017 and REQ-019 (spec appendix, Harness)"}
    rows = {}
    for d, c in zip(DEFS, cases):
        keys = ["structure"]
        if c["kind"] == "audio":
            keys += ["clock", "launch", "grid", "audio", "audio-static"]
        else:
            keys += ["clock", "midi", "midi-static"]
            if "REQ-PLAYBACK-CORE-007" in c["requirements"]:
                keys += ["launch", "grid"]
            keys += [k for k, r in (("stop", "005"), ("loop", "006"), ("tempo", "003")) if f"REQ-PLAYBACK-CORE-{r}" in c["requirements"]]
        rows[c["id"]] = {"source": d["source"], "fixture": c["input"], "evidence": keys,
                         "assumptions": c["stated_assumptions"]}
    return {"schema": "playback-core-traceability-v1", "spec": "SPEC-PLAYBACK-CORE r1 (with SPEC-CLIP-LAUNCH r4 REQ-015/017 "
            "arithmetic restated)", "evidence_root": "analysis/ableton-live-12.4.3/",
            "evidence_manifest_sha256": sha((T13 / "manifest.json").read_bytes()), "evidence": ev,
            "assumptions": amap, "cases": rows,
            "parent_cases_not_released": {
                "PBC-014, PBC-015, PBC-068": "tempo changes during a render: outside this release's named scope",
                "PBC-020 with CLC-062": "LaunchQuantisation -99 read as Global rests on an unreleased load rule",
                "PBC-023": "relaunch at beat 8 coincides with the playing clip's wrap and note events (order U); "
                           "on-line presses carried as CLC-054 at t = 4",
                "PBC-024 at 48,000 Hz": "no request sample has song beat exactly 10/3 at 90 BPM, 48 kHz",
                "PBC-028 to PBC-032": "audio pre-delay above 0 or Fade on: activation observable only through crossfade "
                                      "and fade values (U, Q-024)",
                "PBC-048, PBC-080 to PBC-094, PBC-096": "clip stops (REQ-022): outside this release's named scope",
                "PBC-095": "REQ-023: first sample after Play U",
                "PBC-051, PBC-063, PBC-069": "unresolved (U) in the draft",
                "PBC-061, PBC-064": "REQ-021 end sample not observable through the released outputs (Fade off)"}}


def main():
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    spec_text = (STAGE / "spec.md").read_text()
    st = structure()
    form_probs, als, wavs = fixture_form()
    ev_errs = evidence_checks(cases)
    cons = consistency(cases, spec_text)
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    v = verify(STAGE)
    report = {"schema": "author-validation-v1", "package": "playback-core-v1 (staged candidate)",
              "python": sys.version.split()[0], "numpy": np.__version__, "zlib": zlib.ZLIB_RUNTIME_VERSION,
              "cases": len(cases), "manifest_case_count": man["case_count"],
              "kinds": {k: sum(c["kind"] == k for c in cases) for k in ("timing", "midi", "audio")},
              "provenance": {lab: sum(c["expectation_provenance"] == lab for c in cases)
                             for lab in sorted({c["expectation_provenance"] for c in cases})},
              "either_of_two_events": sum(len(e["samples"]) == 2 for c in cases if "midi" in c["expected"]
                                          for e in c["expected"]["midi"]["events"]),
              "structure": st, "fixture_form_problems": form_probs, "fixtures": als, "wavs": wavs,
              "evidence_cross_check_errors": ev_errs, "consistency_errors": cons, **v,
              "limits": "Checks authored consistency only: no reference or candidate executed. The expectation model "
                        "restates the same evidence; its agreement with the draft's case values and the retained X "
                        "results is a consistency check, not an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    (HERE / "traceability.json").write_text(json.dumps(traceability(cases), indent=1) + "\n")
    keys = ("cases", "fixture_form_problems", "evidence_cross_check_errors", "consistency_errors", "payload_files",
            "hash_or_size_mismatches", "inventory_differences", "unresolved_links", "missing_case_inputs",
            "deny_list_hits", "manifest_sha256")
    print(json.dumps({k: report[k] for k in keys}, indent=1))
    print(json.dumps({"schema_check": st["schema_check"]["with_deviations"], "audit": st["fixture_audit"],
                      "refusals": st["fixture_audit_refusals"], "unknown": st["fixture_audit_unknown_shapes"]}))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        main()
