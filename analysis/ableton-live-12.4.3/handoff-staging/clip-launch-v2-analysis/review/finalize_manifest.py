"""Set the reviewed fields of the clip-launch-v2 manifest and re-hash its inventory (reviewer, analyst side).

usage: python3 -I -B finalize_manifest.py
Run after build_v2.py build (which writes the manifest from meta_v2.py, edited by apply_tooling_edits.py),
apply_review_edits.py and REVIEW.md. Keeps key order and the author's json.dumps(indent=1) layout.
"""
import hashlib, json
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "clip-launch-v2"
p = PKG / "manifest.json"
m = json.loads(p.read_text())
R = "REQ-CLIP-LAUNCH-"

assert m["release_status"] == "candidate-unreviewed" and m["review"]["status"] == "pending"
assert "rounded beat" in m["partial_requirement_scopes"][R + "017"]          # tooling edits applied
m["release_status"] = "released"
m["release_date"] = "2026-10-18"
m["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVC2-01 medium: REQ-015 to 018 were worded as computations that launching uses (press beat, "
        "launch-boundary, song position, a Global clip 'uses' the song's time signature) and could be read as launch "
        "timing; narrowed: rounded_beat and grid-boundary, stated not to be launch timing, boundary not stated to be "
        "a launch's start, value cases not launch cases; no computed value changed",
        "RVC2-02 low: the global argument was called the set's stored GlobalQuantisation, which could state which "
        "global value a launch uses; narrowed to values on the stored items' scale, and which global value, time "
        "signatures and grid a launch uses excluded; selection static-derived from the clip-grid function",
        "RVC2-03 low: for a follow time outside 0 to below 1,000,000 only the held value was excluded; whether the "
        "document opens is now excluded too, since a later opening step was not traced",
        "RVC2-04 info: the structure audit measures 11.0_405 documents with current names and reports false "
        "problems; fixtures checked against their own version and the structure rules directly; analyst-side tool "
        "to be corrected",
        "RVC2-05 editorial: README fixture change list omitted HasStop on each session slot and the empty device "
        "chain on each track; completed",
        "RVC2-06 editorial: REQ-017 clause 4's verification note restated as clause 5, a rule for q = 5 to 13 with "
        "anchor 0",
        "RVC2-07 editorial: payload status set to reviewed release; review record added",
        "RVC2-08 info: evidence identity re-hashed; reviewer's own extracted-execution run (63 processes, at most 58 "
        "calls) agrees with all 146 computations and 25 document values",
        "RVC2-09 info: conversion of the fixtures' other content partly checked statically; assumption stays stated",
    ],
    "disposition": "Approved with listed narrowing (RVC2-01 to RVC2-03), only for the explicit partial clauses; "
                   "100 cases; REQ-015 to 018 as value functions of explicit inputs only, not launch timing; "
                   "expectations static-derived or extracted execution as labeled; reference and candidate "
                   "execution not-run; restricted implementation workspace required",
    "record": "REVIEW.md",
}
files = sorted(q for q in PKG.rglob("*") if q.is_file() and q.name != "manifest.json")
m["files"] = [{"path": str(q.relative_to(PKG)), "sha256": hashlib.sha256(q.read_bytes()).hexdigest(),
               "bytes": q.stat().st_size} for q in files]
p.write_text(json.dumps(m, indent=1) + "\n")
print(len(m["files"]), "files listed; manifest sha256", hashlib.sha256(p.read_bytes()).hexdigest())
