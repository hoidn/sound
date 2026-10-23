"""Data-only staging/checks; no native collectors, builders or original execution.

Run: python3 -I -B build.py build|check
The candidate is not a published handoff. Check is read-only except its report.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import zlib
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent / "midi-note-storage-v3"
V2 = ROOT / "handoff/midi-note-storage-v2"
FULL = ROOT / "analysis/ableton-live-12.4.3/full-spec-v1"
SOURCE = FULL / "depth-midi-probability-groups-v1"
T11 = ROOT / "analysis/ableton-live-12.4.3/r2/t11-structure-v1"
SCHEMA = FULL / "audio-utilities/12.0_12402.txt"
PATH = "LiveSet/Tracks/MidiTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/MidiClip/Notes"
IDS = [f"MNS-{n:03}" for n in range(54, 60)]
PROV = "static-derived; not observed reference output"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def record(p):
    return {"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p)}


def dump(p, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def xmlshape(e):
    return (e.tag, dict(e.attrib), [xmlshape(c) for c in e])


def gzip_bytes(data):
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    return bytes.fromhex("1f8b0800000000000213") + c.compress(data) + c.flush() + (zlib.crc32(data) & 0xffffffff).to_bytes(4, "little") + len(data).to_bytes(4, "little")


def carrier(fragment):
    text = zlib.decompress((V2 / "fixtures/MNS-001.als").read_bytes(), 31).decode()
    # Replace only the outer clip Notes, preserving all authored carrier bytes.
    start = text.index("<Notes>")
    stop = text.index("</MidiClip>")
    end = text.rfind("</Notes>", start, stop) + len("</Notes>")
    return (text[:start] + fragment.strip() + text[end:]).encode()


def build():
    assert not STAGE.exists(), "Do not overwrite a staged candidate; inspect the existing packet."
    STAGE.mkdir()
    shutil.copytree(V2 / "fixtures", STAGE / "fixtures")
    cases = json.loads((V2 / "cases.json").read_text())
    cases["scope"] = "midi-note-storage-v3 partial clauses only; six added cases judge only local group reader rules"
    cases["status"] = "staged-unreviewed-unpublished"
    cases["representation"]["local_action"] = "validate-notes: project comparison of the supplied Notes/group data; no public validation API or implementation pipeline is specified"
    cases["representation"]["local_reader_outcome"] = "refused or admitted by the bounded REQ-015 rules only; no assertion about whole-Set opening, counter repair, final save or later effects"
    purposes = [
        "GroupId 0 with group NextId 1 is refused by the group identifier rule",
        "GroupId 5 with group NextId 1 is refused by the group identifier rule",
        "GroupIds 2 then 1 with group NextId 3 are refused by the document-order rule",
        "GroupIds 1 then 1 with group NextId 2 are refused by the strict-order rule",
        "GroupId 1 naming notes 1 and 2 with group NextId 2 is admitted by the bounded rules only",
        "GroupId 1 naming missing note 99 with group NextId 2 is admitted by the bounded rules only; later effects unknown",
    ]
    for i, cid in enumerate(IDS):
        fragment = (SOURCE / "fixtures" / (cid + ".xml")).read_text()
        (STAGE / "fixtures" / (cid + ".als")).write_bytes(gzip_bytes(carrier(fragment)))
        cases["cases"].append({
            "id": cid, "kind": "negative" if i < 4 else ("positive" if i == 4 else "boundary"),
            "purpose": purposes[i], "requirements": ["REQ-MIDI-NOTE-STORAGE-015"],
            "input": f"fixtures/{cid}.als", "action": "validate-notes",
            "expected": {"local_reader_outcome": "refused" if i < 4 else "admitted"},
            "preconditions": "Supplied conditional group shape, GroupType 0, Probability 1 and ordinary Set-read validation enabled (A1); group NextId is the supplied value, with complete-load counter repair outside scope.",
            "expectation_provenance": PROV, "reference_execution": "not-run", "candidate_execution": "not-run",
            "comparator": "local_reader_outcome exact; no public open outcome, final group state, saved text, whole-load counter repair, playback or later missing-note effects compared",
        })
    dump(STAGE / "cases.json", cases)
    pins = [V2 / "manifest.json", V2 / "cases.json", V2 / "spec.md", V2 / "fixtures/MNS-001.als",
            SOURCE / "manifest.json", FULL / "midi-probability-groups-owner-r5/manifest.json",
            FULL / "reviews/depth-midi-probability-groups-v1-review.json",
            FULL / "reviews/midi-probability-groups-owner-r5-review.json",
            FULL / "reviews/midi-probability-groups-owner-r5-adoption.json", SCHEMA,
            T11 / "schema_check.py", T11 / "fixture_audit.py"]
    pins += [SOURCE / "fixtures" / (cid + ".xml") for cid in IDS]
    dump(HERE / "input-pins.json", {"files": [record(p) for p in pins],
        "reviewed_owner_prefix": {"path": "wiki/specs/midi-note-storage.md", "bytes": 63380,
            "sha256": "0f9cfe15d7af8043f604af2377c1c0ad7d5c6352968d6fd5b6e2b6c32caae11b"},
        "original_execution": "none; only XML, gzip and data-only schema/structure helpers used"})


def check():
    for pin in json.loads((HERE / "input-pins.json").read_text())["files"]:
        p = ROOT / pin["path"]
        assert p.stat().st_size == pin["bytes"] and sha(p) == pin["sha256"], pin
    owner = (ROOT / "wiki/specs/midi-note-storage.md").read_bytes()[:63380]
    assert hashlib.sha256(owner).hexdigest() == "0f9cfe15d7af8043f604af2377c1c0ad7d5c6352968d6fd5b6e2b6c32caae11b"
    before = json.loads((V2 / "cases.json").read_text())
    after = json.loads((STAGE / "cases.json").read_text())
    assert after["cases"][:72] == before["cases"] and len(after["cases"]) == 78
    for i, c in enumerate(after["cases"][72:]):
        assert c["id"] == IDS[i] and c["action"] == "validate-notes"
        assert c["requirements"] == ["REQ-MIDI-NOTE-STORAGE-015"]
        assert c["expected"] == {"local_reader_outcome": "refused" if i < 4 else "admitted"}
        assert c["expectation_provenance"] == PROV
        assert c["reference_execution"] == c["candidate_execution"] == "not-run"
    for c in before["cases"]:
        assert (V2 / c["input"]).read_bytes() == (STAGE / c["input"]).read_bytes()
    # Import only the inspected data-only schema and structure helper.
    sys.path.insert(0, str(T11))
    import fixture_audit as fa
    schema = fa.load_schema(SCHEMA)
    rows = []
    for cid in IDS:
        p = STAGE / "fixtures" / (cid + ".als")
        raw = p.read_bytes()
        assert raw[:10] == bytes.fromhex("1f8b0800000000000213")
        d = zlib.decompressobj(31)
        data = d.decompress(raw) + d.flush()
        assert d.eof and not d.unused_data and not d.unconsumed_tail
        assert data == carrier((SOURCE / "fixtures" / (cid + ".xml")).read_text())
        root = ET.fromstring(data)
        frag = ET.parse(SOURCE / "fixtures" / (cid + ".xml")).getroot()
        notes = root.find(PATH)
        assert xmlshape(notes) == xmlshape(frag)
        dev, rules = fa.measure(schema, root)
        assert not dev and not fa.refusals(rules, dev) and not fa.unknowns(rules), (cid, dev, rules)
        groups = notes.findall("NoteProbabilityGroups/NoteProbabilityGroup")
        for g in groups:
            assert set(g.attrib) == {"Id"}
            assert [e.tag for e in g] == ["GroupType", "Notes", "Probability", "GroupId"]
            assert g.find("GroupType").attrib == {"Value": "0"}
            assert g.find("Probability").attrib == {"Value": "1"}
            assert all(n.tag == "NoteId" and set(n.attrib) == {"NoteId"} for n in g.find("Notes"))
        rows.append({"id": cid, "schema_deviations": dev, "structure_refusals": fa.refusals(rules, dev),
                     "structure_unknowns": fa.unknowns(rules), "notes_equal_reviewed_fragment": True,
                     "carrier_outside_notes_byte_identical": True, "rules": rules, "fixture": record(p)})
    # Preserve every carried requirement body, including all extracted-execution clauses.
    old = (V2 / "spec.md").read_text()
    new = (STAGE / "spec.md").read_text()
    pat = r"(?ms)^### (REQ-MIDI-NOTE-STORAGE-\d{3})[^\n]*\n.*?(?=^### |^## |\Z)"
    oldreq = {m[1]: m[0].rstrip() for m in re.finditer(pat, old)}
    newreq = {m[1]: m[0].rstrip() for m in re.finditer(pat, new)}
    assert len(oldreq) == 13 and set(newreq) == set(oldreq) | {"REQ-MIDI-NOTE-STORAGE-015"}
    assert all(newreq[k] == v for k, v in oldreq.items())
    links = []
    for p in STAGE.glob("*.md"):
        t = p.read_text()
        assert not re.search(r"(?:raw/|analysis/|wiki/research/|wiki/specs/|0x[0-9a-fA-F]{8}|FUN_|DAT_|ghidra|pseudocode)", t, re.I), p
        for target in re.findall(r"\]\(([^)]+)\)", t):
            assert not target.startswith(("/", "http:", "https:", "../")), (p, target)
            if target.split("#")[0]:
                assert (p.parent / target.split("#")[0]).is_file(), (p, target)
            links.append({"file": p.name, "target": target})
    m = json.loads((STAGE / "manifest.json").read_text())
    listed = {f["path"] for f in m["files"]}
    actual = {str(p.relative_to(STAGE)) for p in STAGE.rglob("*") if p.is_file() and p.name != "manifest.json"}
    assert listed == actual and len(actual) == 83
    for f in m["files"]:
        p = STAGE / f["path"]
        assert p.stat().st_size == f["bytes"] and sha(p) == f["sha256"]
    dump(HERE / "author-validation.json", {"status": "pass-data-only-author-checks-independent-review-pending",
        "carried_case_records_exact": 72, "carried_fixture_bytes_exact": 72,
        "carried_requirement_bodies_exact": 13, "new_local_cases": 6, "payload_files": len(actual),
        "manifest": record(STAGE / "manifest.json"), "new_fixture_checks": rows, "local_links": links,
        "new_original_calls": 0, "public_load_save_or_candidate_observations": 0,
        "limits": "Structure/schema checks validate authored data only. They do not execute or prove native group rules. No compatibility pass. The carried deliberately malformed MNS-012 is not reparsed or altered."})


if __name__ == "__main__":
    assert len(sys.argv) == 2 and sys.argv[1] in {"build", "check"}
    build() if sys.argv[1] == "build" else check()
