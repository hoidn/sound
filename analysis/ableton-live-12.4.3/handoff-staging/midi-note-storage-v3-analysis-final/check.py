"""Focused data-only final-status checks; no native execution or schema replay."""
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent
OLD = BASE / "midi-note-storage-v3-r2"
NEW = BASE / "midi-note-storage-v3-final"
REVIEWS = ROOT / "analysis/ableton-live-12.4.3/full-spec-v1/reviews"
ALLOWED = {"AGENTS.md", "README.md", "spec.md", "cases.json", "REVIEW.md", "manifest.json"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pin(p):
    return {"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p)}


def inventory(directory):
    m = json.loads((directory / "manifest.json").read_text())
    actual = {str(p.relative_to(directory)) for p in directory.rglob("*") if p.is_file()}
    assert actual == {f["path"] for f in m["files"]} | {"manifest.json"}
    assert len(m["files"]) == 83
    for f in m["files"]:
        p = directory / f["path"]
        assert sha(p) == f["sha256"] and p.stat().st_size == f["bytes"]
    return m


assert sha(OLD / "manifest.json") == "b091c0675ff408c40d35aca82bf3f428a4859b77d850e96fee6f1af54926dabd"
first = BASE / "midi-note-storage-v3"
assert sha(first / "manifest.json") == "d30432db1bd851bd6df5e83b8512657a02f08895b649d183cebb86b739d744ac"
inventory(first)
before, after = inventory(OLD), inventory(NEW)
content = REVIEWS / "midi-note-storage-v3-handoff-review.json"
correction = REVIEWS / "midi-note-storage-v3-r2-final-seal-review.json"
assert sha(content) == "60147aa28eeb2b68785940294059dce2fcf62696ed1df5c57064b5f8398f483a"
assert sha(correction) == "d89c39e07f45f8668be8e63efdcc685d402cb33b32798340cd94b6b51f5a381d"
files = {f["path"] for f in after["files"]} | {"manifest.json"}
changed = sorted(p for p in files if (NEW / p).read_bytes() != (OLD / p).read_bytes())
assert set(changed) == ALLOWED
assert sorted(k for k in before if before[k] != after[k]) == ["files", "release_date", "release_status", "review"]
assert set(before) == set(after)
assert after["supersedes"] == before["supersedes"] and "supersession" not in after
assert after["release_status"] == "reviewed-ready-for-coordinator-local-publication"
assert after["release_date"] == "2026-10-20"
assert after["review"]["content_review"]["sha256"] == sha(content)
assert after["review"]["correction_review"]["sha256"] == sha(correction)
oldcases = json.loads((OLD / "cases.json").read_text())
newcases = json.loads((NEW / "cases.json").read_text())
assert sorted(k for k in oldcases if oldcases[k] != newcases[k]) == ["status"]
assert set(oldcases) == set(newcases) and len(newcases["cases"]) == 78
assert newcases["cases"] == oldcases["cases"]
v2cases = json.loads((ROOT / "handoff/midi-note-storage-v2/cases.json").read_text())["cases"]
assert newcases["cases"][:72] == v2cases
for c in v2cases:
    assert (NEW / c["input"]).read_bytes() == (ROOT / "handoff/midi-note-storage-v2" / c["input"]).read_bytes()
for c in newcases["cases"]:
    assert (NEW / c["input"]).read_bytes() == (OLD / c["input"]).read_bytes()
oldspec = (OLD / "spec.md").read_text()
newspec = (NEW / "spec.md").read_text()
pat = r"(?ms)^### (REQ-MIDI-NOTE-STORAGE-\d{3})[^\n]*\n.*?(?=^### |^## |\Z)"
reqs = lambda text: {m[1]: m[0] for m in re.finditer(pat, text)}
assert len(reqs(newspec)) == 14 and reqs(newspec) == reqs(oldspec)
oldpreamble = oldspec[oldspec.index("**Status:"):oldspec.index("## What the contract means")]
newpreamble = newspec[newspec.index("**Status:"):newspec.index("## What the contract means")]
assert newspec.replace(newpreamble, oldpreamble, 1).replace(
    "MNS-054 to MNS-059 are added in release 3", "MNS-054 to MNS-059 are added in this candidate", 1) == oldspec
# Retain every role/access obligation after the permitted status preamble.
oldagents = (OLD / "AGENTS.md").read_text()
newagents = (NEW / "AGENTS.md").read_text()
marker = " Application\nimplementation requires"
assert newagents.split(marker, 1)[1] == oldagents.split(marker, 1)[1]
diff = []
for name in changed:
    diff.extend(difflib.unified_diff((OLD / name).read_text().splitlines(keepends=True),
        (NEW / name).read_text().splitlines(keepends=True),
        fromfile="midi-note-storage-v3-r2/" + name, tofile="midi-note-storage-v3-final/" + name))
assert (HERE / "status-finalization.diff").read_text() == "".join(diff)
links = []
with tempfile.TemporaryDirectory(prefix="mns-v3-final-export-") as td:
    export = Path(td) / "candidate"
    shutil.copytree(NEW, export)
    inventory(export)
    for md in export.glob("*.md"):
        text = md.read_text()
        assert not re.search(r"(?:raw/|analysis/|wiki/research/|wiki/specs/|0x[0-9a-fA-F]{8}|FUN_|DAT_|ghidra|pseudocode)", text, re.I)
        for target in re.findall(r"\]\(([^)]+)\)", text):
            filename, _, anchor = target.partition("#")
            p = md.parent / filename if filename else md
            assert p.is_file() and p.resolve().is_relative_to(export.resolve())
            if anchor:
                anchors = [re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-")
                           for h in re.findall(r"^#+ (.*)$", p.read_text(), re.M)]
                assert anchor in anchors
            links.append({"file": md.name, "target": target})
assert not (ROOT / "handoff/midi-note-storage-v3").exists()
for p in NEW.rglob("*"):
    if p.is_file() and p.suffix in {".md", ".json"}:
        assert not any(line.rstrip() != line for line in p.read_text().splitlines())
assert sha(OLD / "manifest.json") == "b091c0675ff408c40d35aca82bf3f428a4859b77d850e96fee6f1af54926dabd"
report = {
    "status": "pass-status-only-final-successor-awaiting-external-exact-tree-review",
    "final_manifest": pin(NEW / "manifest.json"), "reviewed_r2_manifest": pin(OLD / "manifest.json"),
    "content_review": pin(content), "correction_review": pin(correction),
    "exact_delta": pin(HERE / "status-finalization.diff"), "changed_paths": changed,
    "all_payload_hashes_and_isolated_links_pass": 83, "payload_bytes": sum(f["bytes"] for f in after["files"]),
    "case_objects_exact": 78, "fixture_bytes_exact": 78, "requirement_bodies_exact": 14,
    "v2_case_objects_and_fixture_bytes_exact": 72, "case_top_level_delta": ["status"],
    "manifest_top_level_delta": ["files", "release_date", "release_status", "review"],
    "spec_delta": "current status/review preamble and case-origin release label only; all remaining text exact",
    "role_access_obligations_exact": True, "local_links": links,
    "preserved_frozen_stages": ["midi-note-storage-v3", "midi-note-storage-v3-r2"],
    "new_original_calls": 0, "new_candidate_execution": 0, "publication_performed": False,
    "limits": "Focused metadata/data checks only. No native, schema or original/candidate replay. No compatibility grade. External exact-tree attestation must approve this manifest before coordinator publication; its hash is not embedded in the payload."
}
(HERE / "author-validation.json").write_text(json.dumps(report, indent=2) + "\n")
