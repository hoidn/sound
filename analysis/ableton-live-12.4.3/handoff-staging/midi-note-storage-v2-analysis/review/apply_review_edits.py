"""Apply the reviewer's text edits to the staged midi-note-storage-v2 payload (run once; fails on any miss).

usage: python3 -I -B apply_review_edits.py
Edits README.md, AGENTS.md, spec.md and cases.json in place by exact replacement; the manifest is
finalized separately by finalize_manifest.py after REVIEW.md exists. No fixture changes.
"""
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "midi-note-storage-v2"

EDITS = {
    "README.md": [
        ("**Unreviewed release candidate.** Read [the contract](spec.md),\n"
         "[the cases](cases.json), [the role instructions](AGENTS.md) and\n"
         "[the manifest](manifest.json). A separate review has not yet checked this\n"
         "package, and it is not published. It is not an implementation input until\n"
         "then.\n",
         "**Reviewed local release.** Read [the contract](spec.md),\n"
         "[the cases](cases.json), [the role instructions](AGENTS.md),\n"
         "[the manifest](manifest.json) and [the review disposition](REVIEW.md). The\n"
         "stated partial scope, with the clarifications recorded in the review, is\n"
         "approved as a contract for a fresh, restricted implementation workspace.\n"
         "Such a workspace has not been provisioned by this release.\n"),
        # RVM2-01, RVM2-02
        ("2. **Negative zero** (REQ-002, 005, 006 and 016). The text `-0` reads as\n",
         "2. **Negative zero** (REQ-002, 005, 006, 007 and 016). The text `-0` reads as\n"),
        ("   negative zero. Negative zero is saved as `-0`. The midi-note-storage-v1\n"
         "   exclusion of negative zero is narrowed: it remains only for\n"
         "   `VelocityDeviation`, an event's `Value` and the curve controls. MNS-023\n"
         "   (from the parent draft), MNS-073 and MNS-074 are new.\n",
         "   negative zero. Negative zero is saved as `-0`. REQ-007 now says that a\n"
         "   note whose `Duration` is positive zero saves unchanged; a `Duration` of −0\n"
         "   is saved as `0`. REQ-006's statement that values on the grid are\n"
         "   unchanged now excepts negative zero. The midi-note-storage-v1 exclusion of\n"
         "   negative zero is narrowed: it remains only for `VelocityDeviation`, an\n"
         "   event's `TimeOffset` and `Value`, and the curve controls. MNS-023 (from the\n"
         "   parent draft), MNS-073 and MNS-074 are new.\n"),
        # RVM2-03, RVM2-04
        ("   label. The contract states the assumptions the new label rests on.\n",
         "   label. The contract states the assumptions the new label rests on. The\n"
         "   general assumption on number text now also names ties to even on save,\n"
         "   which REQ-016 already stated, and MNS-072, which depends on the\n"
         "   nearest-value reading of its text.\n"),
    ],
    "AGENTS.md": [
        ("This is an unreviewed release candidate. It is not an implementation input\n"
         "until a separate review approves it and it is published. Application\n"
         "implementation then requires a fresh, restricted implementation workspace that\n",
         "This is a reviewed local release for its explicit partial scope. Application\n"
         "implementation requires a fresh, restricted implementation workspace that\n"),
    ],
    "spec.md": [
        ("**Status: unreviewed release candidate.** A separate review has not yet\n"
         "checked the clauses below. Implementation requires an approved, published\n"
         "release and a fresh, restricted implementation workspace.\n",
         "**Status: reviewed local release.** A separate review approved the clauses\n"
         "below with the clarifications recorded in [the review disposition](REVIEW.md).\n"
         "Implementation requires a fresh, restricted implementation workspace.\n"),
        # RVM2-03
        ("- that decimal number text is read and written with exact, correctly rounded\n"
         "  conversions, and that exact decimal ties on save round to even (no case lies\n"
         "  on a tie).\n",
         "- that decimal number text is read and written with exact, correctly rounded\n"
         "  conversions, and that exact decimal ties on save round to even (no case lies\n"
         "  on a tie). MNS-072 depends on the reading at full precision: a value one\n"
         "  binary64 step below the nearest value to its text would be stored as 0.\n"),
        # RVM2-01
        ("A note outside the clip's loop region, and a note with `Duration` 0, load and\n"
         "save unchanged.\n",
         "A note outside the clip's loop region, and a note whose `Duration` is positive\n"
         "zero, load and save unchanged. A `Duration` of −0 is saved as `0`\n"
         "(REQ-MIDI-NOTE-STORAGE-006 clause 4).\n"),
        # RVM2-02
        ("  more, other than `Invalid`; non-finite values; negative zero read in\n"
         "  `VelocityDeviation`, an event's `Value` or a curve control; saved values\n",
         "  more, other than `Invalid`; non-finite values; negative zero read in\n"
         "  `VelocityDeviation`, an event's `TimeOffset` or `Value`, or a curve control\n"
         "  (REQ-MIDI-NOTE-STORAGE-002 clause 3); saved values\n"),
        ("dependency is approved or included. Review status is recorded in\n"
         "[the manifest](manifest.json).\n",
         "dependency is approved or included. Review status is recorded in\n"
         "[the manifest](manifest.json) and [the review disposition](REVIEW.md).\n"),
    ],
    "cases.json": [
        (' "status": "staged candidate; not reviewed; not released",\n', ' "status": "released-reviewed",\n'),
        # RVM2-03: MNS-072 depends on REQ-002 clause 3 at full precision (as MNS-075 on clause 4)
        ('   "id": "MNS-072",\n   "kind": "boundary",\n'
         '   "purpose": "Time 0.00000013007825507825505 on n1, one binary64 step below the binary64 value of half a '
         'grid unit, is stored as one grid unit",\n   "requirements": [\n    "REQ-MIDI-NOTE-STORAGE-006",\n',
         '   "id": "MNS-072",\n   "kind": "boundary",\n'
         '   "purpose": "Time 0.00000013007825507825505 on n1, one binary64 step below the binary64 value of half a '
         'grid unit, is stored as one grid unit",\n   "requirements": [\n    "REQ-MIDI-NOTE-STORAGE-002",\n'
         '    "REQ-MIDI-NOTE-STORAGE-006",\n'),
    ],
}

for name, edits in EDITS.items():
    p = PKG / name
    t = p.read_text()
    for old, new in edits:
        assert t.count(old) == 1, (name, old[:80])
        t = t.replace(old, new)
    p.write_text(t)
    print(name, len(edits), "edits")
