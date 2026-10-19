"""Set the reviewed fields of the automation-envelopes-v2 manifest and re-hash its inventory (reviewer, analyst side).

usage: python3 -I -B finalize_manifest.py   (after apply_review_edits.py and once REVIEW.md exists)
Keeps key order and the author's json.dumps(indent=1) layout; fails if an expected field is absent.
"""
import hashlib, json
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "automation-envelopes-v2"
p = PKG / "manifest.json"
m = json.loads(p.read_text())
assert m["review"]["status"] == "pending" and len(m["stated_assumptions"]) == 4 and (PKG / "REVIEW.md").is_file()

m["release_status"] = "released"
m["release_date"] = "2026-10-18"
sc = m["partial_requirement_scopes"]
sc["REQ-AUTOMATION-ENVELOPES-005"] = (
    "A document whose track envelope holds a single event, at the lower bound, opens; opening discards that "
    "envelope; what a later save writes for it is not specified")
sc["REQ-AUTOMATION-ENVELOPES-007"] = (
    "Before the checks, opening discards each track envelope on Speaker, Pan or CrossFadeState with no event or one "
    "event and each clip envelope with exactly one event, so the checks never refuse a document because of them; "
    "a clip envelope with no event is kept and refused; for envelopes with at least two events, a first event time "
    "other than the lower bound or 0 is refused (binary64 comparison, -0 counts as 0); later times not checked; an "
    "empty arrangement clip timeline of the MIDI track does not cause a refusal (stated assumption 3); other "
    "envelopes are kept (stated assumption 5)")
m["stated_assumptions"].append(
    "Opening discards no envelope of this release's targets other than those of REQ-AUTOMATION-ENVELOPES-007 "
    "clause 5: a track envelope with at least two events, and a clip envelope with no event or at least two events, "
    "are kept and reach the checks of REQ-AUTOMATION-ENVELOPES-007. Cases 001, 008, 012, 016 to 021, 030 and 031 "
    "depend on it.")
ex = m["exclusions"]
old_in = "a track envelope with no event, or with one event at a time other than L; a clip envelope with exactly one event"
assert ex["inputs_without_expectation"].count(old_in) == 1
ex["inputs_without_expectation"].remove(old_in)
old_b = "whether opening keeps an envelope with fewer than two events"
assert ex["behavior"].count(old_b) == 1
ex["behavior"][ex["behavior"].index(old_b)] = (
    "what a save writes for an envelope that opening discards (REQ-AUTOMATION-ENVELOPES-007 clause 5)")
s = m["supersession"]
s["relationship"] = (
    "corrective and narrowing: automation-envelopes-v1 stays immutable, but its fixtures must not be used to judge "
    "that a document opens, and its cases 003, 004 and 011 were wrong: opening discards their envelopes before the "
    "checks of REQ-AUTOMATION-ENVELOPES-007, so the refusals they expect do not occur; its "
    "REQ-AUTOMATION-ENVELOPES-007 clauses 1 and 2 were wrong for envelopes with fewer than two events")
ch = s["changes"]
assert ch[1].startswith("Not carried: cases 003, 004 and 011") and ch[6].startswith("REQ-AUTOMATION-ENVELOPES-005 restated")
assert ch[7].startswith("Unchanged:")
ch[1] = (
    "Defect corrected: cases 003, 004 and 011 were wrong. Each expected a refusal for an envelope with fewer than two "
    "events (a Pan track envelope whose only event is at 4, a Pan track envelope with no event, a clip envelope whose "
    "only event is at 4). Opening discards each of these envelopes before the checks of REQ-AUTOMATION-ENVELOPES-007 "
    "apply (REQ-AUTOMATION-ENVELOPES-007 clause 5, static-derived), so the expected refusals were wrong, not only "
    "badly fixtured, and an implementation must not refuse these documents because of that envelope. "
    "automation-envelopes-v1's REQ-AUTOMATION-ENVELOPES-007 clauses 1 and 2 were wrong for such envelopes: clause 1 "
    "now covers clip envelopes only, clause 2 envelopes with at least two events. The three cases are withdrawn, "
    "not carried with new fixtures")
ch[6] = ("REQ-AUTOMATION-ENVELOPES-005 restated: the document still opens; opening discards the one-event envelope; "
         "what a later save writes for it is excluded")
ch[7:8] = [
    "Exclusions and assumptions: new inputs without expectation (Live Set structure other than the fixtures'; saved "
    "values in the logarithm band); narrowed exclusion of elements that share the Events shape; new stated "
    "assumptions 3, 4 and 5 (opening discards no envelope of the fixtures other than those of "
    "REQ-AUTOMATION-ENVELOPES-007 clause 5; automation-envelopes-v1 relied on it without stating it); new excluded "
    "behavior: what a save writes for a discarded envelope",
    "Unchanged: every other clause, the 18 carried case records and every carried expectation; the value an "
    "envelope supplies at a time stays unreleased (REQ-AUTOMATION-ENVELOPES-010 and 011), with the reason stated",
]
m["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RA2-01 high: the discard on open of envelopes with fewer than two events is confirmed in both builds; "
        "automation-envelopes-v1 cases 003, 004 and 011 were wrong; change list says so; REQ-AUTOMATION-ENVELOPES-007 "
        "clause 5 states the discard instead of leaving it open; REQ-AUTOMATION-ENVELOPES-005 restated; excluded "
        "behavior aligned",
        "RA2-02 medium: case 012 rests on the clip discard applying to exactly one event, not to an empty list; "
        "confirmed in both builds; upheld",
        "RA2-03 medium: cases 001, 008, 012, 016 to 021, 030 and 031 rested on an unstated assumption that opening "
        "keeps envelopes with two or more events (and an empty clip envelope); stated as assumption 5",
        "RA2-04 low: change list incomplete (new exclusions and assumptions; 'unchanged' claim too wide); completed",
        "RA2-05 info: fixture validity: the structure checker passes all 21 fixtures; each refused fixture fails only "
        "for its tested rule; reviewer's single-defect controls open",
        "RA2-06 info: no evaluated or playback value is implied by any case, field or comparison rule",
        "RA2-07 info: reviewer's independent restatement agrees with all 21 expectations",
        "RA2-08 info: supersession checked: superseded digest equals the catalog; 18 records identical; carried "
        "fixtures are the v1 files with 40 inserted lines only",
        "RA2-09 info: evidence identity re-checked; all digests matched",
        "RA2-10 editorial: status set to reviewed release; review record added; a cross-reference corrected; "
        "inventory re-hashed",
        "RA2-11 info: clause 5 has one case (002); cases for the three withdrawn inputs proposed for a later revision",
    ],
    "disposition": "Approved with listed corrections (RA2-01, RA2-03, RA2-04), only for the explicit partial clauses; "
                   "expectations static-derived; reference and candidate execution not-run; restricted "
                   "implementation workspace required",
    "record": "REVIEW.md",
}
files = sorted(x for x in PKG.rglob("*") if x.is_file() and x.name != "manifest.json")
m["files"] = [{"path": str(x.relative_to(PKG)), "sha256": hashlib.sha256(x.read_bytes()).hexdigest(),
               "bytes": x.stat().st_size} for x in files]
p.write_text(json.dumps(m, indent=1) + "\n")
print(len(m["files"]), "files;", "manifest sha256", hashlib.sha256(p.read_bytes()).hexdigest())
