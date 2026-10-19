"""Reviewer: set the release and review fields of the live-set-structure-v1 manifest (analyst side; never shipped).
usage: python3 -I -B finalize_manifest.py ; then build_lss.py seal re-hashes the inventory (it keeps these fields)."""
import json
from pathlib import Path

P = Path(__file__).resolve().parents[2] / "live-set-structure-v1/manifest.json"
m = json.loads(P.read_text())
assert m["release_status"] == "candidate-unreviewed" and m["review"]["status"] == "pending"
m["release_status"] = "released"
m["release_date"] = "2026-10-18"
m["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RV1-01 medium: 15 opening cases rested on the open device-placement question through T11-MIN's two devices; "
        "narrowed: devices removed from every fixture (NextPointeeId 67; case 025 uses 66; case 022 targets 67, 68 and "
        "NextPointeeId 69); assumption withdrawn; any device now has no expectation",
        "RV1-02 low: the repeated-child refusal named every non-list element, which refused T11-MIN's KeyTrack/Notes "
        "array; arrays added as an element form; rule limited to compound elements; no case changed",
        "RV1-03 low: REQ-009 clause 2 stated Path use for codes 2 to 7 without a case while relocation and the "
        "missing-file search are outside the release; narrowed to codes 0 and 1; no case affected",
        "RV1-04 low: the element status table required a MIDI or audio track; restated as no audio, MIDI or group "
        "track there, in REQ-002 clause 2 and in the manifest scope; no case affected",
        "RV1-05 low: keyed state values (send_texts, automated_parameters) now judged only for the listed track "
        "numbers; no expectation changed",
        "RV1-06 editorial: payload status set to reviewed release; review record added; manifest fields filled",
        "RV1-07 info: every traced open route runs the structural checks, and no read step adds freeze slots; "
        "confirmed with the stated remaining inference",
        "RV1-08 info: every fixture expected to open passes the structural checker; each refused fixture fails only "
        "for its tested reason",
    ],
    "disposition": "Approved with listed narrowing and corrections, only for the explicit partial clauses; 34 cases; "
                   "expectations documented, static-derived or extracted execution as labeled; reference and "
                   "candidate execution not-run; restricted implementation workspace required",
    "record": "REVIEW.md",
}
P.write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n")
print("manifest review fields set")
