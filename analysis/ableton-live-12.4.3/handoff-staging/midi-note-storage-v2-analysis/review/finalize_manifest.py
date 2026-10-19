"""Set the reviewed fields of the midi-note-storage-v2 manifest and re-hash its inventory (reviewer, analyst side).

usage: python3 -I -B finalize_manifest.py
Keeps key order and the author's json.dumps(indent=1) layout; fails if an expected field is absent.
"""
import hashlib, json
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "midi-note-storage-v2"
p = PKG / "manifest.json"
m = json.loads(p.read_text())
R = "REQ-MIDI-NOTE-STORAGE-"

m["release_status"] = "released"
m["release_date"] = "2026-10-18"
assert m["partial_requirement_scopes"][R + "007"] == "A note outside the clip loop and a note of Duration 0 load and save unchanged"
m["partial_requirement_scopes"][R + "007"] = ("A note outside the clip loop and a note whose Duration is positive zero load "
                                             "and save unchanged; a Duration of -0 is saved as 0 (REQ-MIDI-NOTE-STORAGE-006)")
sa = m["stated_assumptions"]
assert sa[1].endswith("No case lies on a tie.")
sa[1] += (" MNS-072 depends on the reading at full precision: a value one binary64 step below the nearest value to its "
          "text would be stored as 0.")
ex = m["exclusions"]["inputs_without_expectation"]
old = "negative zero read in VelocityDeviation, an event's Value or a curve control"
k = next(i for i, s in enumerate(ex) if old in s)
ex[k] = ex[k].replace(old, "negative zero read in VelocityDeviation, an event's TimeOffset or Value, or a curve control")
s = m["supersession"]
assert s["relationship"].startswith("superset in effect: every midi-note-storage-v1 clause and case is carried")
s["relationship"] = ("superset in effect: every midi-note-storage-v1 clause and case is carried with the same expectation "
                     "within its scope; REQ-006 clause 3 and REQ-007 are qualified only for negative zero, which "
                     "midi-note-storage-v1 excluded; midi-note-storage-v1 stays immutable, but its fixtures lack Live "
                     "Set structure that opening requires and must not be used")
ch = s["changes"]
i = ch.index("REQ-006: the stated formula governs next to halfway points; -0 stored as +0; a value rounding to "
             "zero from below stored as -0; MNS-023, MNS-072, MNS-074")
ch[i] = ("REQ-006: the stated formula governs next to halfway points; -0 stored as +0, so clause 3 (values on the grid "
         "unchanged) now excepts negative zero; a value rounding to zero from below stored as -0; MNS-023, MNS-072, "
         "MNS-074")
ch.insert(i + 1, "REQ-007: the note that loads and saves unchanged has a Duration of positive zero; a Duration of -0 "
                 "is saved as 0 (MNS-074)")
j = ch.index("exclusion of negative zero narrowed to VelocityDeviation, event Value and curve controls; MNS-023 released")
ch[j] = ("exclusion of negative zero narrowed to VelocityDeviation, event TimeOffset and Value, and curve controls; "
         "MNS-023 released")
j = ch.index("provenance label extracted execution added for the five new cases, with the stated assumptions it rests "
             "on; carried records keep the static-derived label")
ch[j] += ("; the general number-text assumption now also names ties to even on save (already in REQ-016) and MNS-072, "
          "which depends on the nearest-value reading of its text")
m["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVN2-01 low: REQ-007 (a note with Duration 0 saves unchanged) conflicted with -0 being saved as 0; clarified "
        "to positive zero in the contract and manifest; no expectation changed",
        "RVN2-02 low: negative-zero exclusion did not name an event's TimeOffset, which REQ-002 clause 3 excludes; "
        "narrowed explicitly; no case affected",
        "RVN2-03 low: MNS-072 depends at full precision on the static nearest-value reading of its text; REQ-002 "
        "added to the case and the case named in the number-text assumption; expected output unchanged",
        "RVN2-04 editorial: change list incomplete (assumption wording, REQ-006 clause 3, RVN2-01, RVN2-02); completed",
        "RVN2-05 editorial: payload status set to reviewed release; review record added",
        "RVN2-06 info: evidence identity re-hashed; the extracted-execution run reproduced byte for byte; the "
        "staging note on the structure run's digest is obsolete",
        "RVN2-07 info: corrections for the parent specification draft (REQ-006 and REQ-007 wording, case "
        "requirement IDs, REQ-002 negative zero); no package defect",
    ],
    "disposition": "Approved with listed clarifications, only for the explicit partial clauses; 72 cases; "
                   "expectations static-derived or extracted execution as labeled; reference and candidate "
                   "execution not-run; restricted implementation workspace required",
    "record": "REVIEW.md",
}
files = sorted(q for q in PKG.rglob("*") if q.is_file() and q.name != "manifest.json")
m["files"] = [{"path": str(q.relative_to(PKG)), "sha256": hashlib.sha256(q.read_bytes()).hexdigest(),
               "bytes": q.stat().st_size} for q in files]
p.write_text(json.dumps(m, indent=1) + "\n")
print(len(m["files"]), "files listed; manifest sha256", hashlib.sha256(p.read_bytes()).hexdigest())
