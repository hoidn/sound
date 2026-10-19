"""Stage the transport-state-v3 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3, -I and -B, from anywhere:
  python3 -I -B build_v3.py build          # fixtures/, cases.json, draft manifest.json, traceability.json, diff
  python3 -I -B build_v3.py seal           # manifest files[] + checks -> author-validation.json
  python3 -I -B build_v3.py verify <dir>   # same checks against an exported copy (no manifest rewrite)

Inputs (all read-only):
- handoff/transport-state-v2: case records (carried unchanged) and fixture bytes (each extended);
- r2/t11-structure-v1/released-fixture-audit.json: the minimal T11-MIN addition for each v2 fixture;
- r2/t11-structure-v1/schema_check.py and fixture_audit.py with the shipped schema 12.0_12402: the
  structure checker every fixture must pass (no traced refusal, no unknown shape, no new deviation);
- build_v2.py (and through it build_ts1.py): the cross-check model of the transport clauses, the judge and
  the X agreement check, imported unchanged.
spec.md, README.md and AGENTS.md are hand-written. The model is a re-reading of the same evidence, not an
oracle. Each fixture is the v2 fixture with the audit's addition inserted as the first LiveSet child (its
schema position, where fixture_audit.insert_ordered puts it); check() confirms that the result equals the
audit's own repaired copy and that no v2 line changed.
"""
import difflib, hashlib, json, re, shutil, sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.dont_write_bytecode = True  # never write a cache into the v1, v2 or T11 directories
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent / "transport-state-v3"
V2 = ROOT / "handoff/transport-state-v2"
T11 = ROOT / "analysis/ableton-live-12.4.3/r2/t11-structure-v1"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
V2_MANIFEST_SHA = "398a88a62114552595830f99ba2fc1bc4d8c0e1f0d2ae65a70d21aa2324c17c8"  # handoff catalog value
sys.path.insert(0, str(HERE.parent / "transport-state-v2-analysis"))
sys.path.insert(0, str(T11))
import build_v2 as v2  # noqa: E402  (model, x_check, X_EVIDENCE, X_CORROBORATES, DENY, ALLOWED)
import fixture_audit as fa  # noqa: E402  (read, measure, refusals, unknowns, repairs)
from schema_check import load_schema  # noqa: E402

v1 = v2.v1
R = "REQ-TRANSPORT-STATE-"
LIVESET_LINE = "  <LiveSet>\n"
VALUE_LINE = re.compile(r"^\s+<(LoopOn|LoopStart|LoopLength|CurrentTime|Manual)\b")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def audit_entries():
    doc = json.loads((T11 / "released-fixture-audit.json").read_text())
    rel = next(r for r in doc["releases"] if r["release"] == "transport-state-v2")
    return {e["fixture"]: e for e in rel["fixtures"]}


def block(xml):
    """The audit's addition, indented as a LiveSet child in the v2 fixtures' two-space layout."""
    el = ET.fromstring(xml)
    ET.indent(el, space="  ", level=2)
    return "    " + ET.tostring(el, encoding="unicode") + "\n"


def v3_text(v2_text, entry):
    adds = entry["minimal_addition"]
    assert len(adds) == 1 and adds[0]["insert"] == "/Ableton/LiveSet, before MainTrack", adds
    assert v2_text.count(LIVESET_LINE) == 1
    return v2_text.replace(LIVESET_LINE, LIVESET_LINE + block(adds[0]["xml"]))


# ---- packaging ----
def manifest_skeleton(n_cases, fixtures):
    m2 = json.loads((V2 / "manifest.json").read_text())
    excl = json.loads(json.dumps(m2["exclusions"]))
    excl["inputs_without_expectation"].insert(
        5, "a Tracks element that is absent or holds no AudioTrack or MidiTrack; track content other than the "
           "fixtures' one MIDI track")
    return {
        "schema": "handoff-manifest-v1",
        "release_id": "transport-state-v3",
        "release_status": "staged candidate; not reviewed; not released",
        "release_date": None,
        "target": m2["target"],
        "specification": {"id": "SPEC-TRANSPORT-STATE", "parent_revision": 4, "release_revision": 4},
        "feature_ids": m2["feature_ids"],
        "partial_requirement_scopes": m2["partial_requirement_scopes"],
        "unreleased_requirements": m2["unreleased_requirements"],
        "compatibility_dimensions": m2["compatibility_dimensions"],
        "expectation_provenance_labels": m2["expectation_provenance_labels"],
        "stated_assumptions": m2["stated_assumptions"],
        "exclusions": excl,
        "fixture_origin": "independently authored minimal XML documents, each with one fixed MIDI track, and "
                          "expected logical results",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None,
                   "record": None},
        "supersedes": "transport-state-v2",
        "supersession": {
            "relationship": "corrective: the same clauses, case records and expectations as transport-state-v2, on "
                            "fixtures that can open; transport-state-v2 stays immutable, but its fixtures (and the 18 "
                            "transport-state-v1 fixtures it carried) must not be used to judge that a document opens",
            "superseded_manifest_sha256": sha((V2 / "manifest.json").read_bytes()),
            "restated_cases": "all 33 case records (TS-001 to 016, TS-020 to 022 and TS-024 to 037) identical to "
                              "transport-state-v2; every fixture changed as in fixture_changes",
            "defect_corrected": "no transport-state-v2 fixture has a track list; a Live Set whose track list holds no "
                                "audio or MIDI track is not opened (static-derived), so the 23 cases expecting a "
                                "document to open could not hold and the 10 refused cases were also refused for "
                                "that reason; the v2 precondition that missing set content must not change a judged "
                                "outcome was wrong for the track list",
            "fixture_changes": {
                "fixtures": fixtures,
                "change": "21 lines inserted directly after the <LiveSet> start tag: a Tracks element holding one "
                          "MidiTrack (Id 1, EffectiveName 1-MIDI, empty UserName, Color 15, TrackGroupId -1, "
                          "AudioOutputRouting Target AudioOut/Main, empty MainSequencer and FreezeSequencer "
                          "ClipSlotList), as shown in spec.md",
                "unchanged": "every line of the transport-state-v2 fixture of the same name, in order",
            },
            "changes": [
                "defect corrected (defect_corrected): every fixture listed in fixture_changes, all 33, gains the "
                "track list; no other byte of a fixture changed",
                "precondition on missing set content restated to name the track list; inputs without that track "
                "list, or with other track content, added to the inputs without expectation",
                "parent revision 4: it states the transport-state-v2 review clarifications that v2 already carries "
                "(REQ-011 band, logarithm-accuracy assumption, library dependence of -0 reading and save text); "
                "no clause or case added",
                "case records, expectations, provenance labels and requirement clauses unchanged",
            ],
        },
        "entrypoint": "README.md",
        "case_count": n_cases,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def traceability(cases, audit):
    t2 = json.loads((HERE.parent / "transport-state-v2-analysis/traceability.json").read_text())
    loc = "analysis/ableton-live-12.4.3/r2/t11-structure-v1/released-fixture-audit.json"
    out = {"schema": "transport-state-v3-traceability-v1", "spec": "SPEC-TRANSPORT-STATE r4",
           "carried_from": "transport-state-v2-analysis/traceability.json (clauses and per-case evidence unchanged)",
           "x_evidence": t2["x_evidence"], "static_evidence": t2["static_evidence"],
           "structure_evidence": {
               "spec": "wiki/specs/live-set-structure.md r1: REQ-001 (absence is not an error, S), REQ-002 (no "
                       "player track: not opened, S, A1 settled), REQ-006 (freeze count equal to session count, S, "
                       "A2 settled), REQ-013, REQ-015 (S), REQ-016 (S-cond A5; the one list item, MidiTrack Id 1, has a "
                       "valid Id and both clip lists are empty, so no refusal depends on A5)",
               "audit": loc + " releases[transport-state-v2]",
               "checker": "analysis/ableton-live-12.4.3/r2/t11-structure-v1/schema_check.py, fixture_audit.py",
               "rev4": "wiki/specs/transport-state.md revision table row 4: no expectation changed, no clause added"},
           "clauses_added": [],
           "cases": {}}
    for c in cases:
        e = audit[c["input"]]
        out["cases"][c["id"]] = {
            "requirements": c["requirements"], "provenance": c["expectation_provenance"],
            "transport_evidence": t2["cases"][c["id"]],
            "fixture_change": f"{loc} fixtures[{c['input']}].minimal_addition[0]",
            "v2_fixture": {"refusals": e["refusals"], "effect": [x["effect"] for x in e["cases"]]},
            "v3_fixture": "no traced refusal (author-validation.json structure)"}
    return out


def text_diff():
    out = []
    for name in ("README.md", "AGENTS.md", "spec.md"):
        a = (V2 / name).read_text().splitlines(keepends=True)
        b = (STAGE / name).read_text().splitlines(keepends=True)
        out += difflib.unified_diff(a, b, f"transport-state-v2/{name}", f"transport-state-v3/{name}")
    return "".join(out)


def check_v2_identity():
    m2 = json.loads((V2 / "manifest.json").read_text())
    assert sha((V2 / "manifest.json").read_bytes()) == V2_MANIFEST_SHA, "v2 manifest differs from the catalog"
    bad = [f["path"] for f in m2["files"] if sha((V2 / f["path"]).read_bytes()) != f["sha256"]]
    assert not bad, f"v2 payload changed: {bad}"


def build():
    check_v2_identity()
    audit = audit_entries()
    shutil.rmtree(STAGE / "fixtures", ignore_errors=True)
    (STAGE / "fixtures").mkdir(parents=True)
    d2 = json.loads((V2 / "cases.json").read_text())
    for c in d2["cases"]:
        (STAGE / c["input"]).write_text(v3_text((V2 / c["input"]).read_text(), audit[c["input"]]))
    (STAGE / "cases.json").write_text(json.dumps({
        "schema": d2["schema"], "target": d2["target"],
        "scope": "transport-state-v3 partial requirement clauses only (see spec.md)",
        "status": "staged candidate; not reviewed; not released",
        "fixture_origin": "Independently authored minimal XML documents, each with one fixed MIDI track; no shipped "
                          "file copied or excerpted",
        "oracle_status": d2["oracle_status"], "representation": d2["representation"],
        "cases": d2["cases"]}, indent=1) + "\n")
    fixtures = [c["input"] for c in d2["cases"]]
    (STAGE / "manifest.json").write_text(json.dumps(manifest_skeleton(len(d2["cases"]), fixtures), indent=1) + "\n")
    (HERE / "traceability.json").write_text(json.dumps(traceability(d2["cases"], audit), indent=1) + "\n")
    (HERE / "v2-to-v3-text.diff").write_text(text_diff())
    print(len(d2["cases"]), "cases staged")


# ---- checks ----
def structure(schema, raw):
    """T11 checker on one fixture: (traced refusals, unknown shapes, schema deviations)."""
    root = ET.fromstring(raw)
    dev, r = fa.measure(schema, root)
    return fa.refusals(r, dev), fa.unknowns(r), sorted(dev)


def outcome_of(schema, raw):
    """Combined cross-check: structure rules first refuse, else the transport model."""
    ref, _, _ = structure(schema, raw)
    if ref:
        return "refused", None, None
    return v2.model(raw.decode("ascii"))


def mutation_check(schema, pkg, cases):
    """Each case with its expectation changed must be caught by the combined judge."""
    caught = 0
    for c in cases:
        m = json.loads(json.dumps(c["expected"]))
        if m.get("saved", {}).get("values"):
            path = next(iter(m["saved"]["values"]))
            m["saved"]["values"][path] += "0" if "." in m["saved"]["values"][path] else ".5"
        elif m.get("state"):
            k = next(iter(m["state"]))
            m["state"][k] = (not m["state"][k]) if isinstance(m["state"][k], bool) else m["state"][k] + 1
        else:
            m = {"outcome": "opens"} if m["outcome"] == "refused" else {"outcome": "refused"}
        caught += bool(v1.judge(m, *outcome_of(schema, (pkg / c["input"]).read_bytes())))
    return caught


def check(pkg, rewrite):
    pkg = pkg.resolve()
    schema = load_schema(SCHEMA)
    fa.LIVESET_ORDER[:] = list(schema["LiveSet"])
    doc_ = json.loads((pkg / "cases.json").read_text())
    cases = doc_["cases"]
    v2cases = json.loads((V2 / "cases.json").read_text())["cases"]
    conv, writes = v2.x_results()
    base = (pkg / "fixtures/TS-022.xml").read_bytes()  # the unchanged document
    problems, x_problems, struct_rep, isolation = {}, {}, {}, {}
    audit_equal, insert_only, v2_refused = 0, 0, 0
    for c in cases:
        raw = (pkg / c["input"]).read_bytes()
        raw2 = (V2 / c["input"]).read_bytes()
        errs = [] if raw.isascii() and b"\r" not in raw and b"\t" not in raw and raw.endswith(b"\n") else ["format"]
        ref, unk, dev = structure(schema, raw)
        ref2, _, dev2 = structure(schema, raw2)
        v2_refused += bool(ref2)
        if ref or unk or set(dev) - set(dev2):
            errs.append(f"structure: refusals {ref}, unknown {unk}, new deviations {sorted(set(dev) - set(dev2))}")
        struct_rep[c["id"]] = {"refusals": ref, "unknown_shapes": unk, "schema_deviations": dev}
        try:
            errs += v1.judge(c["expected"], *outcome_of(schema, raw))
        except v1.Excluded as e:
            errs.append(f"fixture hits an exclusion: {e}")
        fixed = fa.repairs(ET.fromstring(raw2))[2]
        audit_equal += (ET.canonicalize(raw.decode(), strip_text=True)
                        == ET.canonicalize(ET.tostring(fixed, encoding="unicode"), strip_text=True))
        a, b = raw2.decode().splitlines(), raw.decode().splitlines()
        ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != "equal"]
        insert_only += (len(ops) == 1 and ops[0][0] == "insert" and a[ops[0][1] - 1] == LIVESET_LINE.rstrip("\n")
                        and "\n".join(b[ops[0][3]:ops[0][4]]) + "\n" == block(fa.MIDI_TRACK))
        if c["expected"]["outcome"] == "refused":
            d = [ln for ln in difflib.ndiff(base.decode().splitlines(), b) if ln[:2] in ("- ", "+ ")]
            isolation[c["id"]] = {"lines_differing_from_TS-022": [ln[2:].strip() for ln in d],
                                  "only_tested_elements": all(VALUE_LINE.match(ln[2:]) for ln in d) and bool(d)}
            if not isolation[c["id"]]["only_tested_elements"]:
                errs.append("refused fixture differs from the opening base outside the tested element")
        if errs:
            problems[c["id"]] = errs
        if c["id"] in v2.X_EVIDENCE and (xe := v2.x_check(c, v2.X_EVIDENCE[c["id"]], conv, writes)):
            x_problems[c["id"]] = xe
    base_outcome = outcome_of(schema, base)[0]
    corroboration = {cid: v2.x_check(next(c for c in cases if c["id"] == cid), ev, conv, writes) or "agrees"
                     for cid, ev in v2.X_CORROBORATES.items()}
    files = sorted(p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.json")
    manifest = json.loads((pkg / "manifest.json").read_text())
    if rewrite:
        manifest["files"] = [{"path": str(p.relative_to(pkg)), "sha256": sha(p.read_bytes()),
                              "bytes": p.stat().st_size} for p in files]
        (pkg / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    listed = {f["path"]: f for f in manifest["files"]}
    deny = v2.DENY + [r"T11", r"make_fixture", r"fixture_audit", r"schema_check", r"\baudit", r"\bwalk",
                      r"LSS-", r"LIVE-SET-STRUCTURE", r"S-cond", r"\bRV2-"]

    def scan(p):
        t = " ".join(p.read_text().split())  # the allowed phrases may wrap across lines (as in v2's spec.md)
        for a in v2.ALLOWED:
            t = t.replace(a, "")
        return sorted({m for pat in deny for m in re.findall(pat, t)})
    n = len(cases)
    return {
        "cases": n, "manifest_case_count": manifest["case_count"],
        "outcomes": {k: sum(c["expected"]["outcome"] == k for c in cases) for k in ("opens", "refused")},
        "provenance_counts": {k: sum(c["expectation_provenance"] == k for c in cases)
                              for k in sorted({c["expectation_provenance"] for c in cases})},
        "case_problems": problems,
        "structure_checker": {"schema": str(SCHEMA), "schema_sha256": sha(SCHEMA.read_bytes()),
                              "v2_fixtures_refused_by_traced_rules": f"{v2_refused}/{n}",
                              "v3_fixtures_refused_by_traced_rules": sum(bool(s["refusals"]) for s in struct_rep.values()),
                              "v3_fixtures_with_unknown_shapes": sum(bool(s["unknown_shapes"]) for s in struct_rep.values()),
                              "per_fixture": struct_rep},
        "equal_to_audit_repaired_copy": f"{audit_equal}/{n}",
        "v2_lines_kept_and_only_the_track_list_inserted": f"{insert_only}/{n}",
        "base_TS-022_outcome": base_outcome,
        "refused_case_isolation": isolation,
        "x_evidence_problems": x_problems,
        "x_corroboration_of_static_cases": corroboration,
        "mutations_caught": f"{mutation_check(schema, pkg, cases)}/{n}",
        "case_records_changed_from_v2": [c["id"] for c, d in zip(cases, v2cases) if c != d] + (
            [] if [c["id"] for c in cases] == [d["id"] for d in v2cases] else ["order or IDs"]),
        "duplicate_fixtures": len(files) - len({p.read_bytes() for p in files}),
        "payload_files": len(files), "files_including_manifest": len(files) + 1,
        "manifest_sha256": sha((pkg / "manifest.json").read_bytes()),
        "hash_or_size_mismatches": [k for k, f in listed.items() if not (pkg / k).is_file()
                                    or sha((pkg / k).read_bytes()) != f["sha256"] or (pkg / k).stat().st_size != f["bytes"]],
        "inventory_differences": sorted({str(p.relative_to(pkg)) for p in files} ^ set(listed)),
        "symlinks": [str(p) for p in pkg.rglob("*") if p.is_symlink()],
        "markdown_links": {md.name: len(v1.links(pkg, md)) for md in pkg.glob("*.md")},
        "unresolved_links": {md.name: [t for t, ok in v1.links(pkg, md) if not ok] for md in pkg.glob("*.md")
                             if not all(ok for _, ok in v1.links(pkg, md))},
        "missing_case_inputs": [c["input"] for c in cases if not (pkg / c["input"]).is_file()],
        "deny_list_hits": {str(p.relative_to(pkg)): hits for p in [*files, pkg / "manifest.json"] if (hits := scan(p))},
        "limits": "Checks authored consistency, the T11 structure rules as implemented by its checker, and agreement "
                  "with the retained extracted-execution results only. The reference application and a candidate were "
                  "not executed; the model and the checker re-read the same evidence and are not oracles.",
    }


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "seal":
        check_v2_identity()
        rep = check(STAGE, rewrite=True)
        rep = {"schema": "author-validation-v1", "package": "transport-state-v3 (staged candidate)",
               "python": sys.version.split()[0], **rep}
        (HERE / "author-validation.json").write_text(json.dumps(rep, indent=1) + "\n")
        print(json.dumps({k: v for k, v in rep.items() if k not in ("structure_checker", "refused_case_isolation",
                                                                      "x_corroboration_of_static_cases")}, indent=1))
    elif cmd == "verify":
        print(json.dumps(check(Path(sys.argv[2]), rewrite=False), indent=1))
