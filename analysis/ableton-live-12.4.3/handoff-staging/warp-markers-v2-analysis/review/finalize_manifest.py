"""Set the warp-markers-v2 manifest's review and status fields and re-hash the inventory (analyst side).

usage: python3 -I -B finalize_manifest.py
Run after build_v2.py build, apply_review_edits.py and REVIEW.md. Writes manifest.json in the author's layout
(json indent 1, final newline, as check_v2.py seal writes it) and prints its SHA-256.
"""
import hashlib, json
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "warp-markers-v2"
p = PKG / "manifest.json"
m = json.loads(p.read_text())
m["release_status"] = "released"
m["release_date"] = "2026-10-18"
m["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVW2-01 medium: every case rested on the open question of where devices may be placed; both devices removed "
        "from every document (next pointee identifier 67); WARP-MARKERS-018 withdrawn with REQ-001 clause 2 and REQ-004; "
        "devices and sample parts excluded",
        "RVW2-02 medium: the REQ-009 statement was a playback claim that no released output can observe; REQ-009 "
        "unreleased",
        "RVW2-03 low: the extracted-execution label was broader than what ran (frame scaling by the rate; rounding run "
        "in another part of the program); clarified, no label changed",
        "RVW2-04 low: stated assumption 8 added (a conversion right after opening uses the list held after opening)",
        "RVW2-05 low: combined failures clarified: an add is decided by its first failing check (cases 023 to 027)",
        "RVW2-06 info: all 15 extracted-execution cases found in the retained raw outputs and re-run bit for bit",
        "RVW2-07 editorial: payload status set to reviewed release; review record added",
        "RVW2-08 info: the 7 computed-by-rules cases have inputs inside the run's range; outcomes unchanged under "
        "alternative operation orders consistent with the run",
        "RVW2-09 info: all 20 documents pass the structural checker; 007 and 008 refused only for their marker text; "
        "the WAV is generated",
        "RVW2-10 info: evidence identity re-hashed and matched",
    ],
    "disposition": "Approved with listed narrowing (RVW2-01, RVW2-02), only for the explicit partial clauses; "
                   "expectations static-derived, extracted execution or computed by extracted-execution rules as "
                   "labelled; reference and candidate execution not-run; restricted implementation workspace required",
    "record": "REVIEW.md",
}
files = sorted(f for f in PKG.rglob("*") if f.is_file() and f.name != "manifest.json")
m["files"] = [{"path": str(f.relative_to(PKG)), "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
               "bytes": f.stat().st_size} for f in files]
p.write_text(json.dumps(m, indent=1) + "\n")
print(len(m["files"]), "files;", "manifest sha256", hashlib.sha256(p.read_bytes()).hexdigest())
