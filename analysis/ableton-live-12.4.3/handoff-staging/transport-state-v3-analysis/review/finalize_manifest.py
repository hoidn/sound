"""Set the transport-state-v3 manifest's review and status fields and re-hash the inventory (analyst side).

usage: python3 -I -B finalize_manifest.py
Run after apply_review_edits.py and after REVIEW.md is written. Writes manifest.json in the author's layout
(json indent 1, final newline) and prints its SHA-256.
"""
import hashlib, json
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "transport-state-v3"
p = PKG / "manifest.json"
m = json.loads(p.read_text())
s = m["supersession"]


def swap(text, old, new):
    if new in text:  # already applied (re-run)
        return text
    assert text.count(old) == 1, old
    return text.replace(old, new)


s["relationship"] = swap(s["relationship"], "must not be used to judge that a document opens",
                         "must not be used to judge any case: those expected to open cannot, and the refused ones "
                         "do not isolate the tested text")
s["defect_corrected"] = swap(s["defect_corrected"], "a Live Set whose track list holds no audio or MIDI track",
                             "a Live Set whose track list is absent or holds no audio, MIDI or group track")
m["release_status"] = "released"
m["release_date"] = "2026-10-18"
m["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RV3-01 low: the track rule was stated as no audio or MIDI track; the derived rule is no audio, MIDI or "
        "group track; restated in spec.md, README change 1 and defect_corrected; no case affected",
        "RV3-02 low: the supersession covered only opening; the refused transport-state-v2 fixtures do not isolate "
        "their tested text; README and relationship now say its fixtures judge no case",
        "RV3-03 editorial: payload status set to reviewed release; review record added",
        "RV3-04 info: all 33 fixtures pass the structural checker; each refused fixture fails only for its tested text",
        "RV3-05 info: the added track changes no transport expectation",
        "RV3-06 info: opening without the omitted set members rests on static-derived evidence; accepted",
    ],
    "disposition": "Approved with listed clarifications, only for the explicit partial clauses; case records and "
                   "expectations carried from transport-state-v2; expectations static-derived or extracted execution "
                   "as labeled; reference and candidate execution not-run; restricted implementation workspace required",
    "record": "REVIEW.md",
}
files = sorted(f for f in PKG.rglob("*") if f.is_file() and f.name != "manifest.json")
m["files"] = [{"path": str(f.relative_to(PKG)), "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
               "bytes": f.stat().st_size} for f in files]
p.write_text(json.dumps(m, indent=1) + "\n")
print(len(m["files"]), "files;", "manifest sha256", hashlib.sha256(p.read_bytes()).hexdigest())
