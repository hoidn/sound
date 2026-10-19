"""Set the reviewed fields of the transport-state-v2 manifest and re-hash its inventory (reviewer, analyst side).

usage: python3 -I -B finalize_manifest.py
Keeps key order and the author's json.dumps(indent=1) layout; fails if an expected field is absent.
"""
import hashlib, json
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "transport-state-v2"
p = PKG / "manifest.json"
m = json.loads(p.read_text())
X = "extracted execution (x86_64 slice, glibc substitutions); arm64 equivalence inferred"
assert X in m["expectation_provenance_labels"] and len(m["stated_assumptions"]) == 4

m["release_status"] = "released"
m["release_date"] = "2026-10-18"
m["partial_requirement_scopes"]["REQ-TRANSPORT-STATE-011"] = (
    "Boolean and integer text; fixed-precision decimal text with P=17 or 9, k from the binary64 logarithm, "
    "for in-range finite values outside the half-gap band; positive and negative zero")
m["expectation_provenance_labels"][X] = (
    "the original program's x86_64 build read the case's text and, where a saved text is judged, wrote the value "
    "read, on a Linux x86_64 host with glibc in place of the macOS system libraries; locating, opening and saving "
    "remain static-derived")
m["stated_assumptions"] = [
    "The macOS arm64 build converts these texts and values as the x86_64 build does. All cases with the "
    "extracted-execution label depend on it.",
    "The reference's binary64 base-10 logarithm errs by less than 3/4 of a binary64 gap wherever its last bit "
    "decides k in REQ-011, outside the half-gap band. TS-024 to TS-027, whose logarithms lie 0.02 to 0.17 gaps from "
    "an integer, need only an error below 0.8 of a gap.",
    "The reference's decimal reading follows the C-standard number grammar in a locale whose decimal separator is "
    "'.', and gives the nearest binary64 value with the sign of -0 kept, as the glibc run did. TS-024 to TS-028, "
    "TS-034 and TS-035 depend on it.",
    "The reference's fixed-point text on save is exact, rounds exact decimal ties to even and keeps the sign of "
    "negative zero, as the glibc run did; transport-state-v1 accepted exactness and ties to even as inferences. "
    "TS-024 to TS-028 depend on it; no case lies on a tie.",
]
ex = m["exclusions"]["inputs_without_expectation"]
old = "saved binary64 values whose log10 is not an integer but lies between 1/4 and 3/4 of a binary64 gap from one"
assert ex.count(old) == 1
ex[ex.index(old)] = old + " (the gap on the side of log10, as in spec.md)"
s = m["supersession"]
s["relationship"] = ("superset in effect: within transport-state-v1's scope both give the same expectations; "
                     "transport-state-v1 stays immutable and valid for its own scope; its REQ-011 step 1 wording is "
                     "exact only within that scope")
ch = s["changes"]
assert ch[2].endswith("TS-010, TS-029 to TS-033") and ch[5].startswith("provenance label")
ch[2] += ("; TS-030 judges only that a document with code 0 opens (v1 gave no expectation for opening a code "
          "other than 201); whether such a code takes effect stays excluded")
ch[5] = "provenance label extracted execution added, with the stated assumptions it rests on; carried records unchanged"
m["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RV2-01 low: change list incomplete (TS-030 opening a code other than 201; unnamed added exclusion; stated "
        "assumptions); completed, no expectation changed",
        "RV2-02 low: REQ-011 step 1 outside the band rested on an unstated logarithm-accuracy assumption; stated, "
        "band referenced from REQ-011, README change 1 reworded; no case affected",
        "RV2-03 low: decimal reading and save-text dependence on the substituted library unstated; assumptions "
        "widened; no expectation changed",
        "RV2-04 editorial: extracted-execution definition now covers the writer run on save cases",
        "RV2-05 editorial: payload status set to reviewed release; review record added",
        "RV2-06 info: evidence identity re-hashed and the evidence run reproduced byte for byte",
        "RV2-07 info: half-gap band conservative on the side toward zero; accepted",
        "RV2-08 info: coverage notes for a later revision; no defect",
    ],
    "disposition": "Approved with listed clarifications, only for the explicit partial clauses; expectations "
                   "static-derived or extracted execution as labeled; reference and candidate execution not-run; "
                   "restricted implementation workspace required",
    "record": "REVIEW.md",
}
files = sorted(q for q in PKG.rglob("*") if q.is_file() and q.name != "manifest.json")
m["files"] = [{"path": str(q.relative_to(PKG)), "sha256": hashlib.sha256(q.read_bytes()).hexdigest(),
               "bytes": q.stat().st_size} for q in files]
p.write_text(json.dumps(m, indent=1) + "\n")
print(len(m["files"]), "files listed; manifest sha256", hashlib.sha256(p.read_bytes()).hexdigest())
