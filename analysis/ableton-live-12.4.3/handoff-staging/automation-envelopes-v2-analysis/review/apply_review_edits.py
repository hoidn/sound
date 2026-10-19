"""Apply the reviewer's text edits to the staged automation-envelopes-v2 payload (run once; fails on any miss).

usage: python3 -I -B apply_review_edits.py
Edits README.md, AGENTS.md, spec.md and the top-level status of cases.json in place by exact replacement. Case
records and fixtures are not touched. The manifest is finalized by finalize_manifest.py after REVIEW.md exists.
"""
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "automation-envelopes-v2"

EDITS = {
    "README.md": [
        ("**Staged candidate; not reviewed; not released.** Read [the contract](spec.md),\n"
         "[the cases](cases.json), [the role instructions](AGENTS.md) and\n"
         "[the manifest](manifest.json). This package is not an implementation input until\n"
         "a separate review approves it and it is published.",
         "**Reviewed local release.** Read [the contract](spec.md),\n"
         "[the cases](cases.json), [the role instructions](AGENTS.md),\n"
         "[the manifest](manifest.json) and [the review disposition](REVIEW.md). The\n"
         "stated partial scope, narrowed and clarified as recorded in the review, is\n"
         "approved as a contract for a fresh, restricted implementation workspace. Such\n"
         "a workspace has not been provisioned by this release."),
        ("After publication the release is immutable; corrections require a new revision.",
         "Preserve this release unchanged; corrections require a new revision."),
        ("When published, this release supersedes automation-envelopes-v1, which stays\n"
         "immutable. Its fixtures must not be used to judge that a document opens\n"
         "(change 1), and its cases 003, 004 and 011 must not be relied on (change 2).",
         "This release supersedes automation-envelopes-v1, which stays immutable. Its\n"
         "fixtures must not be used to judge that a document opens (change 1), and its\n"
         "cases 003, 004 and 011 were wrong (change 2)."),
        ("2. **Not carried: cases 003, 004 and 011.** Each expected a refusal for an\n"
         "   envelope with fewer than two events: a track envelope whose only event is at\n"
         "   4, a track envelope with no event, and a clip envelope whose only event is\n"
         "   at 4. Opening a document may discard such an envelope before the checks of\n"
         "   REQ-AUTOMATION-ENVELOPES-007 apply, so the refusal is not established. These\n"
         "   inputs now have no expectation (REQ-AUTOMATION-ENVELOPES-007 clause 5).\n"
         "   Clause 1 of automation-envelopes-v1's REQ-AUTOMATION-ENVELOPES-007 is\n"
         "   narrowed to clip envelopes, and clause 2 to envelopes with at least two\n"
         "   events. The fixtures\n"
         "   `AUTOMATION-ENVELOPES-003.xml`, `004.xml` and `011.xml` are dropped.",
         "2. **Defect corrected: cases 003, 004 and 011 were wrong.** Each expected a\n"
         "   refusal for an envelope with fewer than two events: a `Pan` track envelope\n"
         "   whose only event is at 4, a `Pan` track envelope with no event, and a clip\n"
         "   envelope whose only event is at 4. Opening a document discards each of these\n"
         "   envelopes before the checks of REQ-AUTOMATION-ENVELOPES-007 apply\n"
         "   (REQ-AUTOMATION-ENVELOPES-007 clause 5, static-derived). The checks never see\n"
         "   the envelope and do not refuse the document because of it. The expected\n"
         "   refusals were therefore wrong, not only badly fixtured. An implementation\n"
         "   must not refuse these documents because of that envelope.\n"
         "   automation-envelopes-v1's REQ-AUTOMATION-ENVELOPES-007 clauses 1 and 2 were\n"
         "   wrong for such envelopes. Clause 1 now covers clip envelopes only, and\n"
         "   clause 2 envelopes with at least two events. The three cases are withdrawn,\n"
         "   not carried with new fixtures, and `AUTOMATION-ENVELOPES-003.xml`, `004.xml`\n"
         "   and `011.xml` are dropped. Only case 002 has a discarded envelope, and it\n"
         "   opens with or without the discard."),
        ("9. **REQ-AUTOMATION-ENVELOPES-005 restated.** A document whose track envelope\n"
         "   holds a single event, at L, opens. Whether that envelope is kept is now\n"
         "   excluded behavior.",
         "9. **REQ-AUTOMATION-ENVELOPES-005 restated.** A document whose track envelope\n"
         "   holds a single event, at L, still opens. Opening discards that envelope\n"
         "   (change 2). What a later save writes for it is excluded behavior."),
        ("11. **Unchanged.** Every other clause, case record, expectation, provenance\n"
         "    label and exclusion of automation-envelopes-v1 is carried unchanged.",
         "11. **Exclusions and assumptions.** New inputs without expectation: Live Set\n"
         "    structure other than the fixtures' (other tracks, devices, scenes, clips and\n"
         "    clip slots, main and cue tracks, sends and returns), and saved values in the\n"
         "    band of change 7. Narrowed exclusion: elements that share the `Events` shape\n"
         "    (change 6). New stated assumptions: 3 (change 6), 4 (change 7) and 5, that\n"
         "    opening discards no envelope of the fixtures other than those of change 2.\n"
         "    Cases 001, 008, 012, 016 to 021, 030 and 031 depend on assumption 5;\n"
         "    automation-envelopes-v1 relied on it without stating it. New excluded\n"
         "    behavior: what a save writes for a discarded envelope.\n"
         "12. **Unchanged.** Every other clause, case record, expectation and provenance\n"
         "    label of automation-envelopes-v1 is carried unchanged."),
    ],
    "AGENTS.md": [
        ("This is a staged, unreviewed handoff candidate. It is not an implementation\n"
         "input. Only a release that a separate review approved and published may be used\n"
         "for implementation, in a fresh, restricted implementation workspace containing\n"
         "only permitted materials. Do not begin clean implementation in an analyst\n"
         "checkout.",
         "This is a reviewed local release for its explicit partial scope. Application\n"
         "implementation requires a fresh, restricted implementation workspace that\n"
         "contains only permitted materials. Publication of this package does not\n"
         "provision one. Do not begin clean implementation in an analyst checkout."),
    ],
    "spec.md": [
        ("**Status: staged candidate; not reviewed; not released.**",
         "**Status: reviewed local release.** A separate review approved the clauses\n"
         "below with the narrowing and clarifications recorded in\n"
         "[the review disposition](REVIEW.md)."),
        ("   binary64 gap, outside the band that has no expectation. No case lies next to\n"
         "   a power of ten, so no case depends on it.\n",
         "   binary64 gap, outside the band that has no expectation. No case lies next to\n"
         "   a power of ten, so no case depends on it.\n"
         "5. Opening discards no envelope of this release's targets other than those of\n"
         "   REQ-AUTOMATION-ENVELOPES-007 clause 5. An `AutomationEnvelope` with at least\n"
         "   two events, and a `ClipEnvelope` with no event or at least two events, are\n"
         "   kept and reach the checks of REQ-AUTOMATION-ENVELOPES-007. Cases 001, 008,\n"
         "   012, 016 to 021, 030 and 031 depend on it.\n"),
        ("A document whose track envelope holds a single event, at L, opens. Whether\n"
         "opening keeps that envelope, and whether a save writes it, are not specified.",
         "A document whose track envelope holds a single event, at L, opens. Opening\n"
         "discards that envelope (REQ-AUTOMATION-ENVELOPES-007 clause 5). What a later\n"
         "save writes for it is not specified."),
        ("5. This release has no refusal expectation for an `AutomationEnvelope` that\n"
         "   holds no event, or one event at a time other than L, nor for a `ClipEnvelope`\n"
         "   that holds exactly one event. Opening may discard such an envelope before the\n"
         "   checks above apply; whether it does is not established.",
         "5. Before the checks above apply, opening discards every `AutomationEnvelope`\n"
         "   on the audio track's `Speaker`, `Pan` or `CrossFadeState` that holds no event\n"
         "   or one event, and every `ClipEnvelope` that holds exactly one event. The\n"
         "   checks therefore never refuse a document because of such an envelope,\n"
         "   whatever its event time. A `ClipEnvelope` that holds no event is not\n"
         "   discarded, and clause 1 refuses it. Of the discarded envelopes only the one\n"
         "   of AUTOMATION-ENVELOPES-002 has a case, and that document opens with or\n"
         "   without the discard. Other envelopes are kept (stated assumption 5)."),
        ("Case IDs 003, 004 and 011 of automation-envelopes-v1 are not carried, and IDs 022\n"
         "to 029 are not used (see [the README](README.md)).",
         "Case IDs 003, 004 and 011 of automation-envelopes-v1 are withdrawn because their\n"
         "expectations were wrong, and IDs 022 to 029 are not used (see\n"
         "[the README](README.md#changes-from-automation-envelopes-v1))."),
        ("- a track envelope with no event, or with one event at a time other than L; a\n"
         "  clip envelope with exactly one event (REQ-AUTOMATION-ENVELOPES-007 clause 5);\n",
         ""),
        ("- whether opening keeps an envelope with fewer than two events;",
         "- what a save writes for an envelope that opening discards\n"
         "  (REQ-AUTOMATION-ENVELOPES-007 clause 5);"),
        ("slots and the scene inserted as whole lines; no line of that template changes\n"
         "(README change 1).",
         "slots and the scene inserted as whole lines; no line of that template changes\n"
         "(README change 3)."),
        ("public source or dependency is approved or included. Review status is recorded\n"
         "in [the manifest](manifest.json).",
         "public source or dependency is approved or included. Review status is recorded\n"
         "in [the manifest](manifest.json) and [the review disposition](REVIEW.md)."),
    ],
    "cases.json": [
        ('"status": "staged candidate; not reviewed"', '"status": "released-reviewed"'),
    ],
}

for name, edits in EDITS.items():
    p = PKG / name
    text = p.read_text()
    for old, new in edits:
        n = text.count(old)
        assert n == 1, f"{name}: {n} matches for {old[:70]!r}"
        text = text.replace(old, new)
    p.write_text(text)
    print(name, len(edits), "edits")
