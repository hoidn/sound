"""Stage the midi-config-v2 release candidate (analyst side; not reviewed, not released).

Run from this directory with CPython 3.11 and -I:
  python3.11 -I build_v2.py build   # fixtures/ + cases.json in ../midi-config-v2/
  python3.11 -I build_v2.py seal    # manifest.json files[] + author-validation.json + traceability.json

Inputs (read only): the released v1 package (cases + fixture bytes) and the S4 draft
cases/fixtures. Expected outputs are the hand-authored S4/v1 static derivations, with
the one correction listed in CORRECTIONS; nothing here computes an oracle. The seal step
cross-checks every expectation against crosscheck_model.py (an independent re-reading,
not an oracle), verifies hashes, links, ASCII fixtures and a sanitization deny-list.
"""
import configparser, hashlib, io, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # repository root
STAGE = HERE.parent / "midi-config-v2"
V1 = ROOT / "handoff/midi-config-v1"
S4 = ROOT / "analysis/ableton-live-12.4.3/r2/s4-midi-v1"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS"
PROV = "static-derived; not observed reference output"
COMPARATOR = "exact assignment set over all fields; order immaterial; device_parameter_banks exact"
OFFSET = 54  # S4-MIDI-n -> MIDI-CONFIG-(54+n)

PURPOSE = {  # sanitized wording for S4 purposes that mention the shipped template or internal terms
    11: "Only Bank8Button enabled: it occupies direct-bank selector position 1",
    32: "FwdButton is not a recognized key",
    38: "Pad channel text has no effect when the pad note is not enabled",
}
CORRECTIONS = {
    30: {
        "reason": "S4 draft expected Send2Knob1 alone -> track-send-b:1. Re-check: strip send knobs are "
                  "compacted per strip (GenericScript L272-302) and connected by position to sends[index] "
                  "(ChannelStripComponent._connect_parameters L306-319; ButtonMatrixElement.__iter__ L79-82), "
                  "so a lone Send2Knob1 reaches send A. Sparse Send2 is excluded from v2; fixture now enables "
                  "both knobs of strip 1.",
        "purpose": "Mode scope: VolumeMapMode on master/cue, CrossfaderMapMode on crossfader, absent SendsMapMode on both sends",
        "text": "[Globals]\nGlobalChannel: 5\n\n[DeviceControls]\n\n[MixerControls]\nVolumeMapMode: AccelTwoCompliment\n"
                "CrossfaderMapMode: LinearBinaryOffset\nMasterVolumeSlider: 20\nCueVolumeSlider: 21\nCrossfaderSlider: 22\n"
                "Send1Knob1: 23\nSend2Knob1: 24\n\n[TransportControls]\n",
        "assignments": [
            {"section": "MixerControls", "control": "MasterVolumeSlider", "target": "master-volume", "message_type": "control-change", "number": 20, "channel": 5, "map_mode": "AccelTwoCompliment"},
            {"section": "MixerControls", "control": "CueVolumeSlider", "target": "cue-volume", "message_type": "control-change", "number": 21, "channel": 5, "map_mode": "AccelTwoCompliment"},
            {"section": "MixerControls", "control": "CrossfaderSlider", "target": "crossfader", "message_type": "control-change", "number": 22, "channel": 5, "map_mode": "LinearBinaryOffset"},
            {"section": "MixerControls", "control": "Send1Knob1", "target": "track-send-a:1", "message_type": "control-change", "number": 23, "channel": 5, "map_mode": "Absolute"},
            {"section": "MixerControls", "control": "Send2Knob1", "target": "track-send-b:1", "message_type": "control-change", "number": 24, "channel": 5, "map_mode": "Absolute"},
        ],
    },
}
DENY = [r"analysis/", r"wiki/", r"\.\./", r"\.pyc", r"bytecode", r"disassembl", r"decompil", r"pseudocode", r"offset",
        r"\bL\d{2,}", r"Python", r"configparser", r"GenericScript", r"_UserScript", r"_Framework", r"_Generic",
        r"create_instance", r"parse_int", r"parse_map_mode", r"getint", r"getboolean", r"NOTOGGLE", r"c_instance",
        r"MidiMap", r"ButtonMatrix", r"EncoderElement", r"ChannelStrip", r"Component\b", r"\bS4-", r"\bR-[A-Z]",
        r"PRB-", r"derivation", r"Live\.arm64", r"/home/", r"/var/", r"/tmp/", r"ev_[0-9a-f]", r"sha256\s*[0-9a-f]{64}"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def build():
    v1 = json.loads((V1 / "cases.json").read_text())
    s4 = json.loads((S4 / "draft-cases-v2.json").read_text())
    cases, trace = [], []
    for c in v1["cases"]:
        text = (V1 / c["input"]).read_bytes()
        cases.append(dict(
            id=c["id"], purpose=c["purpose"], origin="restated from midi-config-v1",
            requirements=sorted(set(c["requirements"]) | {"REQ-MIDI-USER-005"}),
            input=c["input"],
            expected={"assignments": [dict(section="MixerControls", **a, map_mode="Absolute") for a in c["expected"]["assignments"]],
                      "device_parameter_banks": None}))
        trace.append({"id": c["id"], "source": f"midi-config-v1 {c['id']}", "fixture_bytes": "identical to v1", "rules": ["v1 analyst traceability"]})
        write(c["input"], text)
    for n, c in enumerate(s4["cases"], 1):
        cid = f"MIDI-CONFIG-{n + OFFSET:03d}"
        fix = f"fixtures/{cid}/UserConfiguration.txt"
        fixd = CORRECTIONS.get(n)
        text = fixd["text"].encode("ascii") if fixd else (S4 / c["input"]).read_bytes()
        cases.append(dict(
            id=cid, purpose=(fixd or {}).get("purpose") or PURPOSE.get(n) or c["purpose"], origin="new in midi-config-v2",
            requirements=c["requirements"], input=fix,
            expected={"assignments": fixd["assignments"] if fixd else c["expected"]["assignments"],
                      "device_parameter_banks": c["expected"]["device_parameter_banks"]}))
        trace.append({"id": cid, "source": c["id"], "rules": c["derivation"],
                      "fixture_bytes": "corrected" if fixd else "identical to S4 draft",
                      **({"correction": fixd["reason"]} if fixd else {})})
        write(fix, text)
    for c in cases:
        c.update(expectation_provenance=PROV, reference_execution="not-run", candidate_execution="not-run", comparator=COMPARATOR)
    doc = {
        "schema": "midi-config-cases-v2",
        "target": TARGET,
        "scope": "midi-config-v2 partial requirement clauses only (see spec.md)",
        "status": "staged candidate; not reviewed; not released",
        "fixture_origin": "Independently authored minimal ASCII inputs; no shipped file copied",
        "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
        "representation": {
            "assignment": "section, control, target, message_type, number, channel; map_mode for continuous controls; button_kind for buttons; neither for pads",
            "device_parameter_banks": "null when no Encoder assignment is enabled, else 1 or 2",
            "note": "project comparison representation, not an API of the original application or a required design"},
        "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc, indent=1) + "\n")
    (HERE / "traceability.json").write_text(json.dumps({
        "schema": "midi-config-v2-traceability", "status": "analyst-only; never part of the payload",
        "parent_spec": "SPEC-MIDI-USER-MAPPING revision 2 (wiki/specs/midi-user-mapping.md)",
        "s4_evidence": "analysis/ableton-live-12.4.3/r2/s4-midi-v1/ (draft-cases-v2.json rules{} defines rule IDs)",
        "v1_release": "handoff/midi-config-v1/", "cases": trace}, indent=1) + "\n")
    print(len(cases), "cases staged")


def write(rel, data):
    p = STAGE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def payload():
    return sorted(p for p in STAGE.rglob("*") if p.is_file() and p.name != "manifest.json")


def links(md_path):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md_path.read_text()):
        if re.match(r"[a-z]+:", target):
            out.append((target, "external URL not allowed"))
            continue
        path, _, anchor = target.partition("#")
        dest = (md_path.parent / path).resolve() if path else md_path
        ok = dest.is_file() and STAGE.resolve() in dest.parents
        if ok and anchor:
            slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
            ok = anchor in slugs
        out.append((target, "ok" if ok else "UNRESOLVED"))
    return out


def seal():
    sys.path.insert(0, str(HERE))
    from crosscheck_model import interpret, canon
    doc = json.loads((STAGE / "cases.json").read_text())
    problems = {}
    for c in doc["cases"]:
        raw = (STAGE / c["input"]).read_bytes()
        errs = []
        if not raw.isascii() or b"\r" in raw or not raw.endswith(b"\n"):
            errs.append("fixture not ASCII/LF/newline-terminated")
        configparser.ConfigParser().read_file(io.StringIO(raw.decode("ascii")))  # must not raise
        if canon(interpret(raw.decode("ascii"))) != canon(c["expected"]):
            errs.append("cross-check model disagrees")
        addrs = [(a["message_type"], a["number"], a["channel"]) for a in c["expected"]["assignments"]]
        if len(set(addrs)) != len(addrs):
            errs.append("duplicate MIDI address")
        if errs:
            problems[c["id"]] = errs
    files = payload()
    manifest = json.loads((STAGE / "manifest.json").read_text())
    manifest["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size} for p in files]
    (STAGE / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    rehash = [f["path"] for f in manifest["files"] if sha((STAGE / f["path"]).read_bytes()) != f["sha256"]]
    unlisted = sorted({str(p.relative_to(STAGE)) for p in files} ^ {f["path"] for f in manifest["files"]})
    link_rows = {str(p.relative_to(STAGE)): links(p) for p in STAGE.glob("*.md")}
    bad_links = {k: [t for t, s in v if s != "ok"] for k, v in link_rows.items() if any(s != "ok" for _, s in v)}
    inputs_missing = [c["input"] for c in doc["cases"] if not (STAGE / c["input"]).is_file()]
    deny_hits = {}
    for p in [*files, STAGE / "manifest.json"]:
        text = p.read_text()
        hits = sorted({m for pat in DENY for m in re.findall(pat, text)})
        if hits:
            deny_hits[str(p.relative_to(STAGE))] = hits
    report = {
        "schema": "author-validation-v1", "package": "midi-config-v2 (staged candidate)",
        "python": sys.version.split()[0], "cases": len(doc["cases"]), "case_problems": problems,
        "payload_files": len(files), "files_including_manifest": len(files) + 1,
        "manifest_sha256": sha((STAGE / "manifest.json").read_bytes()),
        "hash_mismatches": rehash, "inventory_differences": unlisted,
        "markdown_links": {k: len(v) for k, v in link_rows.items()}, "unresolved_links": bad_links,
        "missing_case_inputs": inputs_missing, "deny_list_hits": deny_hits,
        "limits": "Checks authored consistency only: no reference or candidate executed; the cross-check model is an "
                  "independent re-reading of the same static evidence, not an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "case_problems", "payload_files", "hash_mismatches",
                                             "inventory_differences", "unresolved_links", "missing_case_inputs",
                                             "deny_list_hits", "manifest_sha256")}, indent=1))


if __name__ == "__main__":
    {"build": build, "seal": seal}[sys.argv[1]]()
