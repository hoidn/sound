"""Stage the midi-note-storage-v1 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3 and -I from any directory:
  python3 -I build_mns.py build          # fixtures/, cases.json, draft manifest.json in ../midi-note-storage-v1/
  python3 -I build_mns.py seal           # manifest files[], author-validation.json, traceability.json
  python3 -I build_mns.py verify <dir>   # the same checks against an exported copy (no rewrite)

Fixtures and cases are authored in mns_cases.py: a carrier Live Set written for this release holds
the base notes of SPEC-MIDI-NOTE-STORAGE r1 (fragments F0 and F1) with one edit per case. No shipped
file is read. Expected results are hand-authored static expectations. seal cross-checks each against
model() in mns_model.py, an independent restatement of the released clauses; it shares the same
static evidence and is not an oracle. mns_trace.py holds the analyst-only traceability. README.md,
AGENTS.md and spec.md in the stage directory are hand-written.
"""
import copy, hashlib, json, re, shutil, sys, zlib
from pathlib import Path

sys.dont_write_bytecode = True  # keep the analysis directory free of caches
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mns_model  # noqa: E402  (analyst-side cross-check; never shipped)
from mns_trace import EVIDENCE, INFERRED, TRACE  # noqa: E402
from mns_cases import CASES, COMPARATOR, GZ_HEADER, LOADS, PROBES, PROV, PROV_LIMITS, R, document, gz  # noqa: E402

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent / "midi-note-storage-v1"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"


# ---- packaging ----
def sha(b):
    return hashlib.sha256(b).hexdigest()


REVIEW = {  # set by the separate handoff review, 2026-10-18 (see REVIEW.md)
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; not the "
                  "author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVN-01 medium: the open-time steps (value limits, NoteId checks and numbering, list validation) rested on an "
        "untraced load condition, which the author applied to four cases only; established by the reviewer's own "
        "static check; assumption removed, no case changed",
        "RVN-02 medium: 16 per-note list cases traced to an evidence round not retained in the repository; "
        "re-established from retained records of the pinned build and the build itself; no case changed",
        "RVN-03 low: REQ-009 numbering order stated without its sorted-key-track precondition; narrowed",
        "RVN-04 low: MNS-001 purpose and the open-save comparator did not name the group generator's NextId as not "
        "compared; reworded, no expectation changed",
        "RVN-05 low: the manifest excluded all magnitudes of 1,000,000 or more, including Invalid; aligned with the "
        "contract",
        "RVN-06 editorial: a reference observation of the clip present without notes was unclassified; marked "
        "inconclusive",
        "RVN-07 editorial: payload status wording set to reviewed release; review record added; inventory re-hashed",
        "RVN-08 info: evidence identity re-checked; all hashes matched",
        "RVN-09 info: Invalid text cases carry REQ-002; reading confirmed",
        "RVN-10 info: no MIDI key outside 36 and 38 and no key-range, key-order or edge-list expectation",
        "RVN-11 info: remaining stated assumptions accepted; leading minus in the integer converter confirmed",
        "RVN-12 info: 12 new cases, MNS-036 narrowing and the open-save action accepted; sharing acceptable",
    ],
    "disposition": "Approved with listed narrowing (RVN-03), only for the explicit partial clauses; "
                   "expectations static-derived; reference and candidate execution not-run; restricted implementation "
                   "workspace required",
    "record": "REVIEW.md",
}


def manifest_meta():
    return {
        "schema": "handoff-manifest-v1", "release_id": "midi-note-storage-v1", "release_status": "released",
        "release_date": "2026-10-18", "target": TARGET,
        "specification": {"id": "SPEC-MIDI-NOTE-STORAGE", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-MIDI", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": {
            R + "001": "Notes element children and order, key track children, MidiNoteEvent-only key track notes "
                       "(other elements refused), structure written in order on save",
            R + "002": "Attribute types; any order; repeated attribute refused; decimal number text, Invalid in Duration "
                       "and TimeOffset, Boolean text and integer text forms as listed in spec.md",
            R + "003": "Defaults 0, 1 and true for omitted VelocityDeviation, Probability and IsEnabled, per note",
            R + "004": "Saved attribute order; omission of VelocityDeviation 0, Probability 1 and IsEnabled true",
            R + "005": "Velocity, OffVelocity, Probability and Duration limits on opening; "
                       "Time, VelocityDeviation and NoteId not limited",
            R + "006": "Rounding of Time, Duration and TimeOffset to multiples of 1/3,843,840, half away from zero",
            R + "007": "A note outside the clip loop and a note of Duration 0 load and save unchanged",
            R + "008": "Non-zero NoteIds unique within the clip; NoteId 0 repeatable",
            R + "009": "Next id raise, numbering of NoteId 0 notes in ascending key and document order, saved next id; "
                       "NoteId absent from every note",
            R + "010": "Sorted key tracks and strictly ascending notes keep their order; overlapping or equal-Time notes "
                       "of one key do not refuse (saved text excluded)",
            R + "013": "Per-note list and event structure; curve-control default 0.5 and omission; TimeOffset and Value "
                       "always written",
            R + "014": "List removal by NoteId 0, CC and NoteId naming no stored note; duplicate NoteId and CC refused; "
                       "Invalid TimeOffset dropped; Value limits; stable sort; empty lists removed; lists strictly inside "
                       "their note unchanged",
            R + "016": "Saved number text with 17 or 9 significant-digit rule, plain integers, IsEnabled false",
        },
        "unreleased_requirements": [R + "011", R + "012", R + "015", R + "017"],
        "compatibility_dimensions": {
            "project-files": "static-derived expectations for the clip notes element read and written; reference "
                             "execution not-run",
            "behavior-after-open": "excluded (editing, playback, recording, undo)",
            "ui": "excluded (REQ-MIDI-NOTE-STORAGE-017)", "audio": "excluded", "timing": "excluded",
        },
        "exclusions": {
            "inputs_without_expectation": [
                "a note without Time, Duration, Velocity or OffVelocity; NoteId absent from some but not all notes; an "
                "event without TimeOffset or Value",
                "MidiKey outside 0 to 127, a key track without MidiKey, two key tracks with the same key, key tracks "
                "not in ascending key order, an empty key track, repeated key track or list Id values",
                "notes of one key not in strictly ascending Time after rounding, or overlapping, beyond the "
                "not-refused outcome of REQ-MIDI-NOTE-STORAGE-010",
                "a kept list with an event at or before offset 0 or at or after its note's Duration",
                "NaN, infinite, # and hexadecimal number text, inf and nan words, leading whitespace other than "
                "U+0020; Invalid outside Duration and TimeOffset; magnitudes of 1,000,000 or more other than Invalid; "
                "negative zero "
                "read or produced by rounding; saved values whose log10 is within 1e-12 of an integer without being "
                "an exact power of ten",
                "integer text with spaces on both sides of the digits or a + with trailing spaces; a - sign; "
                "accepted integer values above 1,000,000; MidiKey, CC, list NoteId and Id text other than plain "
                "decimal (a leading - only in CC)",
                "a missing structural element; unknown attributes or child elements in the note structures; a "
                "non-empty NoteProbabilityGroups",
                "documents that break more than one refusal rule",
                "other containers, envelopes, format versions and document kinds, including clip files",
            ],
            "behavior": [
                "what is shown after a refusal and what remains open (REQ-MIDI-NOTE-STORAGE-017)",
                "probability groups and the saved group next id (REQ-MIDI-NOTE-STORAGE-015)",
                "key track and list Id values on save; whether empty key tracks are kept (REQ-MIDI-NOTE-STORAGE-012)",
                "MIDI key range and repeated keys (REQ-MIDI-NOTE-STORAGE-011)",
                "re-sorting, trimming or merging of unsorted or overlapping notes; adjustment of per-note lists at "
                "their note's edges",
                "meaning of the values: time units, muting, chance, expression controllers",
                "editing, playback, recording, undo; the rest of the clip and the set",
            ],
            "parent_cases_not_released": ["MNS-011", "MNS-023", "MNS-024", "MNS-034", "MNS-035", "MNS-037", "MNS-038",
                                          "MNS-053", "MNS-054", "MNS-055", "MNS-056", "MNS-057", "MNS-058", "MNS-059",
                                          "MNS-060"],
            "parent_cases_narrowed": {"MNS-036": "outcome only; saved notes not judged"},
        },
        "fixture_origin": "independently authored gzip Live Sets from a carrier written for this release; no shipped "
                          "file content or program code",
        "approved_public_sources": [],
        "review": REVIEW,
        "supersedes": None, "entrypoint": "README.md", "case_count": len(CASES),
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def build():
    shutil.rmtree(STAGE / "fixtures", ignore_errors=True)
    (STAGE / "fixtures").mkdir(parents=True)
    cases = []
    for cid, kind, reqs, purpose, frag, action, exp, limits in CASES:
        rel = f"fixtures/{cid}.als"
        (STAGE / rel).write_bytes(gz(document(frag)))
        expected = {"outcome": exp} if isinstance(exp, str) else {"outcome": LOADS, "saved_notes": exp}
        cases.append({"id": cid, "kind": kind, "purpose": purpose, "requirements": [R + r for r in reqs],
                      "input": rel, "action": action, "expected": expected,
                      "expectation_provenance": PROV_LIMITS if limits else PROV,
                      "reference_execution": "not-run", "candidate_execution": "not-run",
                      "comparator": COMPARATOR[action]})
    assert len({c["id"] for c in cases}) == len(cases)
    (STAGE / "cases.json").write_text(json.dumps({
        "schema": "midi-note-storage-cases-v1", "target": TARGET,
        "scope": "midi-note-storage-v1 partial requirement clauses only (see spec.md)",
        "status": "released-reviewed",
        "fixture_origin": "Independently authored gzip Live Sets; no shipped file copied or excerpted",
        "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
        "representation": {
            "action": "open, or open-save (open, then save as a new set without other changes)",
            "outcome": "loads or refused",
            "saved_notes": "key_tracks (midi_key, notes as attribute name to exact text), event_lists (NoteId, CC, "
                           "events as attribute name to exact text), note_id_next",
            "note": "project comparison representation, not an API of the original application or a required design"},
        "cases": cases}, indent=1, ensure_ascii=False) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(), indent=1) + "\n")
    print(len(cases), "cases staged")


DENY = [r"0x[0-9a-fA-F]{5,}", r"FUN_", r"\bA(MidiNote|KeyTrack|PerNote|MidiNotes)\w*", r"Remoteable", r"[Tt]ranslator",
        r"vtable", r"\+0x[0-9a-fA-F]+", r"128-slot", r"constructor", r"loader", r"post-load", r"registr", r"\bflag", r"from_chars", r"strtod",
        r"printf", r"DBL_MAX", r"FLT_MAX", r"Class mismatch", r"not unique", r"Multiple sets", r"Note-group",
        r"Unexpected value", r"Ghidra", r"decompil", r"pseudocode", r"disassembl", r"dossier", r"corpus", r"\bs7-",
        r"\bd4-", r"\bn[12]-0", r"PRB-", r"\bQ-0\d", r"\bA[12]\b", r"\bB0\b", r"\bF[01]\b", r"\bMN-\d", r"\bI[1-9]\b",
        r"analysis/", r"wiki/", r"\.\./", r"/home/", r"/var/", r"/tmp/", r"derivation", r"traceab", r"build_mns",
        r"mns_model", r"Python", r"[Ee]xpat", r"zlib", r"Live\.arm64", r"Core Library", r"909", r"12\.4d1", r"memory",
        r"range guard", r"unsigned", r"\bobject", r"\breus", r"\bev_[0-9a-f]", r"\bpacket"]
ALLOWED_HITS = {"AGENTS.md": {"decompil"}}  # forbidden-inputs list, same wording as released packages


def links(pkg, md):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
        path, _, anchor = target.partition("#")
        dest = (md.parent / path).resolve() if path else md
        ok = not re.match(r"[a-z]+:", target) and dest.is_file() and pkg in dest.parents
        if ok and anchor:
            ok = anchor in {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                            for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
        out.append((target, ok))
    return out


def text_of(p):
    data = p.read_bytes()
    return zlib.decompress(data, 31).decode("utf-8") if data[:2] == b"\x1f\x8b" else data.decode("utf-8")


def check(pkg, rewrite):
    pkg = pkg.resolve()
    doc_ = json.loads((pkg / "cases.json").read_text())
    problems, fixtures = {}, {}
    for c in doc_["cases"]:
        raw_ = (pkg / c["input"]).read_bytes()
        errs = mns_model.judge(c, mns_model.model(raw_))
        txt = zlib.decompress(raw_, 31)
        if raw_[:10] != GZ_HEADER or b"\r" in txt or not txt.endswith(b"\n"):
            errs.append("fixture form")
        if errs:
            problems[c["id"]] = errs
        fixtures[c["id"]] = {"bytes": len(raw_), "decompressed_bytes": len(txt), "lines": txt.count(b"\n")}
    files = sorted(p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.json")
    manifest = json.loads((pkg / "manifest.json").read_text())
    if rewrite:
        manifest["files"] = [{"path": str(p.relative_to(pkg)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                             for p in files]
        (pkg / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    listed = {f["path"]: f for f in manifest["files"]}
    deny = {}
    for p in [*files, pkg / "manifest.json"]:
        hits = sorted({m for pat in DENY for m in re.findall(pat, text_of(p))} - ALLOWED_HITS.get(p.name, set()))
        if hits:
            deny[str(p.relative_to(pkg))] = hits
    return {
        "cases": len(doc_["cases"]), "manifest_case_count": manifest["case_count"], "case_problems": problems,
        "distinct_inputs": len({(pkg / c["input"]).read_bytes() for c in doc_["cases"]}),
        "payload_files": len(files), "files_including_manifest": len(files) + 1,
        "manifest_sha256": sha((pkg / "manifest.json").read_bytes()),
        "hash_or_size_mismatches": [k for k, f in listed.items() if not (pkg / k).is_file()
                                    or sha((pkg / k).read_bytes()) != f["sha256"] or (pkg / k).stat().st_size != f["bytes"]],
        "inventory_differences": sorted({str(p.relative_to(pkg)) for p in files} ^ set(listed)),
        "symlinks": [str(p) for p in pkg.rglob("*") if p.is_symlink()],
        "markdown_links": {md.name: len(links(pkg, md)) for md in pkg.glob("*.md")},
        "unresolved_links": {md.name: [t for t, ok in links(pkg, md) if not ok] for md in pkg.glob("*.md")
                             if not all(ok for _, ok in links(pkg, md))},
        "missing_case_inputs": [c["input"] for c in doc_["cases"] if not (pkg / c["input"]).is_file()],
        "deny_list_hits": deny, "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()},
        "fixtures": fixtures,
        "limits": "Checks authored consistency only: no reference or candidate executed; the cross-check model is an "
                  "independent restatement of the same static evidence, not an oracle.",
    }


def probe_report():
    out = {}
    for name, frag in PROBES.items():
        got = mns_model.model(gz(document(frag)))
        ok = got[0] == "no-expectation" or (got[0] == "loads" and got[1] is None)
        out[name] = ("no expectation" if got[0] == "no-expectation" else "loads; saved notes undetermined") if ok \
            else f"UNEXPECTED {got[0]}"
    return out


def first_note(c):
    return c["expected"]["saved_notes"]["key_tracks"][0]["notes"][0]


# Mutated expectations that the cross-check must detect (it is not vacuous).
MUTATIONS = {
    "MNS-028 next id 4": ("MNS-028", lambda c: c["expected"]["saved_notes"].__setitem__("note_id_next", "4")),
    "MNS-003 VelocityDeviation dropped": ("MNS-003", lambda c: first_note(c).pop("VelocityDeviation")),
    "MNS-004 attribute order reversed": ("MNS-004", lambda c: c["expected"]["saved_notes"]["key_tracks"][0]["notes"]
                                         .__setitem__(0, dict(reversed(list(first_note(c).items()))))),
    "MNS-020 Time unrounded": ("MNS-020", lambda c: first_note(c).__setitem__("Time", "0.123456789")),
    "MNS-049b events reversed": ("MNS-049b", lambda c: c["expected"]["saved_notes"]["event_lists"][0]["events"]
                                 .reverse()),
    "MNS-046 outcome loads": ("MNS-046", lambda c: c["expected"].__setitem__("outcome", "loads")),
}


def mutation_report():
    cases = {c["id"]: c for c in json.loads((STAGE / "cases.json").read_text())["cases"]}
    out = {}
    for name, (cid, mutate) in MUTATIONS.items():
        c = copy.deepcopy(cases[cid])
        mutate(c)
        out[name] = "detected" if mns_model.judge(c, mns_model.model((STAGE / c["input"]).read_bytes())) else "MISSED"
    return out


def seal():
    rep = check(STAGE, rewrite=True)
    rep = {"schema": "author-validation-v1", "package": "midi-note-storage-v1 (staged candidate)",
           "python": sys.version.split()[0], "zlib": zlib.ZLIB_RUNTIME_VERSION, **rep,
           "excluded_input_probes": probe_report(), "mutated_expectations": mutation_report()}
    (HERE / "author-validation.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    ids = [c[0] for c in CASES]
    assert set(TRACE) == set(ids), sorted(set(TRACE) ^ set(ids))
    trace = {"schema": "midi-note-storage-traceability-v1", "spec": "SPEC-MIDI-NOTE-STORAGE r1",
             "evidence": EVIDENCE, "inferred_links": INFERRED,
             "cases": {i: {"source": TRACE[i][0], "evidence": TRACE[i][1], "inferred": TRACE[i][2]} for i in ids}}
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: rep[k] for k in ("cases", "distinct_inputs", "case_problems", "payload_files",
                                          "hash_or_size_mismatches", "inventory_differences", "unresolved_links",
                                          "missing_case_inputs", "deny_list_hits", "manifest_sha256", "mutated_expectations",
                                          "excluded_input_probes")}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "seal":
        seal()
    elif cmd == "verify":
        print(json.dumps(check(Path(sys.argv[2]), rewrite=False), indent=1, ensure_ascii=False))
