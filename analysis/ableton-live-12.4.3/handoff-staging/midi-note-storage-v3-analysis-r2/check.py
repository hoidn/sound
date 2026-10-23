"""Read-only corrected-candidate checks; write reports only beside this script."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent
OLD = BASE / "midi-note-storage-v3"
NEW = BASE / "midi-note-storage-v3-r2"
CHECKER = BASE / "midi-note-storage-v3-analysis/build.py"
REVIEW = ROOT / "analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-note-storage-v3-handoff-review.json"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pin(p):
    return {"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p)}


def dump(p, value):
    p.write_text(json.dumps(value, indent=2) + "\n")


assert sha(OLD / "manifest.json") == "d30432db1bd851bd6df5e83b8512657a02f08895b649d183cebb86b739d744ac"
assert sha(REVIEW) == "60147aa28eeb2b68785940294059dce2fcf62696ed1df5c57064b5f8398f483a"
assert sha(CHECKER) == "6cfe513e240635160ffdef51f1dfe2034b90ca4edec1a672d24444dd0fa3685a"
old = json.loads((OLD / "manifest.json").read_text())
new = json.loads((NEW / "manifest.json").read_text())
for f in old["files"]:
    p = OLD / f["path"]
    assert sha(p) == f["sha256"] and p.stat().st_size == f["bytes"]
old_paths = {str(p.relative_to(OLD)) for p in OLD.rglob("*") if p.is_file()}
new_paths = {str(p.relative_to(NEW)) for p in NEW.rglob("*") if p.is_file()}
assert old_paths == new_paths
changed = sorted(p for p in old_paths if (OLD / p).read_bytes() != (NEW / p).read_bytes())
assert changed == ["REVIEW.md", "manifest.json"]
keys_changed = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
assert keys_changed == ["files", "release_status", "review", "supersession"]
assert "supersession" not in new
assert new["supersedes"] == old["supersedes"]
assert new["supersedes"]["release_id"] == "midi-note-storage-v2"
assert new["supersedes"]["manifest_sha256"] == "697f09ffc4951d5f3b6d67c20b8f851d68671078a0b3d730a220383f94d2dd15"
assert new["case_count"] == 78 and new["case_units"]["carried_v2"] == 72
assert new["case_units"]["new_local_group_cases"] == 6
assert new["release_status"] == new["review"]["status"] == "final-seal-pending"
assert new["review"]["content_review"]["sha256"] == sha(REVIEW)
assert len(new["files"]) == 83
assert not (ROOT / "handoff/midi-note-storage-v3").exists()

# Reuse the inspected data-only checker; bypass its builder/main and redirect only its report.
spec = importlib.util.spec_from_file_location("mns_v3_author_data_checker", CHECKER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.STAGE = NEW
module.dump = lambda p, value: dump(HERE / p.name, value)
module.check()

links = []
with tempfile.TemporaryDirectory(prefix="mns-v3-r2-export-") as td:
    dst = Path(td) / "candidate"
    shutil.copytree(NEW, dst)
    for f in new["files"]:
        p = dst / f["path"]
        assert sha(p) == f["sha256"] and p.stat().st_size == f["bytes"]
    for md in dst.glob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", md.read_text()):
            filename, _, anchor = target.partition("#")
            p = md.parent / filename if filename else md
            assert p.is_file() and p.resolve().is_relative_to(dst.resolve())
            if anchor:
                headings = [re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-")
                            for h in re.findall(r"^#+ (.*)$", p.read_text(), re.M)]
                assert anchor in headings
            links.append({"file": md.name, "target": target})
for p in list(NEW.glob("*.md")) + list(HERE.glob("*")):
    if p.is_file() and p.suffix in {".md", ".json", ".py"}:
        assert not any(line.rstrip() != line for line in p.read_text().splitlines())
assert sha(OLD / "manifest.json") == "d30432db1bd851bd6df5e83b8512657a02f08895b649d183cebb86b739d744ac"
dump(HERE / "final-seal-author-check.json", {
    "status": "pass-metadata-only-correction-independent-final-seal-review-pending",
    "review": pin(REVIEW), "predecessor_stage_manifest": pin(OLD / "manifest.json"),
    "corrected_manifest": pin(NEW / "manifest.json"), "data_only_checker": pin(CHECKER),
    "changed_files": changed, "changed_manifest_keys": keys_changed,
    "unchanged_payload_files": 82, "unchanged_case_objects": 78,
    "unchanged_gzip_fixtures": 78, "unchanged_partial_requirement_bodies": 14,
    "old_v2_case_objects_and_fixture_bytes_exact": 72,
    "all_payload_hashes_pass_in_isolated_copy": 83, "local_links": links,
    "new_original_calls": 0, "new_candidate_execution": 0,
    "publication_performed": False,
    "limits": "Metadata correction only. Data checks do not establish public Set-open/save, counter repair, later effects or compatibility. Final-seal review and parent prepublication checks remain pending."
})
