"""Apply the reviewer's payload edits to the transport-state-v3 staging copy (analyst side; never shipped).

usage: python3 -I -B apply_review_edits.py
Each edit replaces text that must occur exactly once. Run once, before finalize_manifest.py. RV3-01: the track
rule is stated as derived (no audio, MIDI or group track). RV3-02: the supersession says v2's fixtures judge no
case. RV3-03: status lines name the reviewed release and REVIEW.md. No case record or fixture is touched.
"""
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "transport-state-v3"
EDITS = {
    "README.md": [
        ("**Staged candidate; not reviewed; not released.** Read [the contract](spec.md),\n"
         "[cases](cases.json), [role instructions](AGENTS.md) and\n"
         "[the manifest](manifest.json). This package is not an implementation input until\n"
         "a separate review approves it and it is published.",
         "**Reviewed local release.** Read [the contract](spec.md), [cases](cases.json),\n"
         "[role instructions](AGENTS.md), [the manifest](manifest.json) and\n"
         "[the review disposition](REVIEW.md). The stated partial scope, with the\n"
         "clarifications recorded in the review, is approved as a contract for a fresh,\n"
         "restricted implementation workspace. Such a workspace has not been provisioned\n"
         "by this release."),
        ("When published, this release supersedes transport-state-v2, which stays\n"
         "immutable. Its clauses, case records and expectations are carried unchanged,\n"
         "but its fixtures must not be used to judge that a document opens (change 1).",
         "This release supersedes transport-state-v2, which stays immutable. Its\n"
         "clauses, case records and expectations are carried unchanged, but its fixtures\n"
         "must not be used to judge any case: the documents expected to open cannot, and\n"
         "the refused ones do not isolate the text they test (change 1)."),
        ("its track list, and a set whose `Tracks` element is absent or holds no audio\n"
         "   or MIDI track is not opened (static-derived).",
         "its track list, and a set whose `Tracks` element is absent or holds no audio,\n"
         "   MIDI or group track is not opened (static-derived)."),
    ],
    "spec.md": [
        ("**Status: staged candidate; not reviewed; not released.** Do not implement from\n"
         "it. A separate review must approve it first.",
         "**Status: reviewed local release.** A separate review approved the clauses\n"
         "below with the clarifications recorded in [the review disposition](REVIEW.md).\n"
         "Implementation requires a fresh, restricted implementation workspace."),
        ("  A Live Set whose `Tracks` element is absent or holds no audio or MIDI track is\n"
         "  not opened (static-derived). That check, and every other rule for tracks, is\n"
         "  not part of this release; the track is present so that the documents can open.\n"
         "  Its values are fixed and not interpreted, and no case judges it.",
         "  A Live Set whose `Tracks` element is absent or holds no audio, MIDI or group\n"
         "  track is not opened (static-derived). That rule, and every other rule for\n"
         "  tracks, is not part of this release. The track is present only so that the\n"
         "  documents can open; its values are fixed and not interpreted, and no case\n"
         "  judges it."),
        ("Review status is recorded in\n[the manifest](manifest.json); this candidate has no review record yet.",
         "Review status is recorded in\n[the manifest](manifest.json) and [the review disposition](REVIEW.md)."),
    ],
    "AGENTS.md": [
        ("This is a staged, unreviewed handoff candidate. It is not an implementation\n"
         "input. Only a release that a separate review approved and published may be used\n"
         "for implementation, in a fresh, restricted implementation workspace containing\n"
         "only permitted materials. Do not begin clean implementation in an analyst\n"
         "checkout.",
         "This is a reviewed local release for its explicit partial scope. Application\n"
         "implementation requires a fresh, restricted implementation workspace containing\n"
         "only permitted materials. Publication of this package does not provision one.\n"
         "Do not begin clean implementation in an analyst checkout."),
        ("Preserve this package unchanged.", "Preserve this release unchanged."),
    ],
    "cases.json": [
        ('"status": "staged candidate; not reviewed; not released",', '"status": "released-reviewed",'),
    ],
}

for name, edits in EDITS.items():
    p = PKG / name
    t = p.read_text()
    for old, new in edits:
        assert t.count(old) == 1, (name, old[:60])
        t = t.replace(old, new)
    p.write_text(t)
    print(name, len(edits), "edits")
