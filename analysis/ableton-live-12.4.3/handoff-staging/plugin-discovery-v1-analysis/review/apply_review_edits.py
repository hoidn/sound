"""Apply the reviewer's text edits to the staged payload. Each old text must occur exactly once.

Usage: python3 -I apply_review_edits.py STAGE_DIR
"""
import sys
from pathlib import Path

stage = Path(sys.argv[1])
EDITS = {
    "README.md": [(
        "**Unreviewed candidate.** This package is not an implementation input until a\n"
        "separate review approves it and it is published as a release. Read\n"
        "[the contract](spec.md), [the cases](cases.json),\n"
        "[the role instructions](AGENTS.md) and [the manifest](manifest.json).\n",
        "**Reviewed local release.** Read [the contract](spec.md),\n"
        "[the cases](cases.json), [the role instructions](AGENTS.md),\n"
        "[the manifest](manifest.json) and [the review disposition](REVIEW.md). The\n"
        "stated partial scope, with the clarifications recorded in the review, is\n"
        "approved as a contract for a fresh, restricted implementation workspace.\n"
        "Such a workspace has not been provisioned by this release.\n")],
    "AGENTS.md": [(
        "This package is an unreviewed release candidate. Until a separate review\n"
        "approves it and it is published, it is not an implementation input. After\n"
        "publication, application implementation requires a fresh, restricted\n"
        "implementation workspace that contains only permitted materials. Publication\n"
        "does not provision one. Do not begin clean implementation in an analyst\n"
        "checkout.\n",
        "This is a reviewed local release for its explicit partial scope. Application\n"
        "implementation requires a fresh, restricted implementation workspace that\n"
        "contains only permitted materials. Publication of this package does not\n"
        "provision one. Do not begin clean implementation in an analyst checkout.\n")],
    "spec.md": [
        ("**Status: unreviewed candidate.** This contract is not an implementation input\n"
         "until a separate review approves it and it is published as a release.\n",
         "**Status: reviewed local release.** A separate review approved the clauses\n"
         "below with the clarifications recorded in [the review disposition](REVIEW.md).\n"),
        ("3. The observation is the set of recorded loads from the creation of the tree\n"
         "   until no further examination occurs, attributed to the format of the folder\n"
         "   that contains the entry.\n",
         "3. The observation is the set of recorded loads from the creation of the tree\n"
         "   until no further examination occurs. A load is attributed to the format\n"
         "   whose searched folder contains the entry; in every case, the searched\n"
         "   folders of at most one format contain any given entry. A load of an entry\n"
         "   that no searched folder contains, as in PLUGIN-DISCOVERY-016 and 035, is a\n"
         "   mismatch unless another method shows that it was not an examination as a\n"
         "   VST3 or VST2 module.\n"),
        ("   that are plain files the observation is inconclusive unless another method\n"
         "   shows whether the application examined them.\n",
         "   that are plain files the observation is inconclusive unless another method\n"
         "   shows whether the application examined them. In this release that applies\n"
         "   to `J.vst3` in PLUGIN-DISCOVERY-021 and to all of PLUGIN-DISCOVERY-028.\n"),
        ("behavioral data. No public source or dependency is approved or included.\n"
         "Review status is recorded in [the manifest](manifest.json).\n",
         "behavioral data. No public source or dependency is approved or included.\n"
         "Review status is recorded in [the manifest](manifest.json) and\n"
         "[the review disposition](REVIEW.md).\n"),
    ],
    "cases.json": [('"status": "candidate-unreviewed"', '"status": "released-reviewed"')],
    "manifest.json": [(
        '"examination order, including VST3 before VST2 and the order of folders (REQ-PLUGIN-DISCOVERY-003)"',
        '"examination order, including any order between the formats and between folders (REQ-PLUGIN-DISCOVERY-003)"')],
}
for name, pairs in EDITS.items():
    p = stage / name
    text = p.read_text()
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            sys.exit(f"{name}: expected one occurrence, found {n}: {old[:60]!r}")
        text = text.replace(old, new)
    p.write_text(text)
    print("edited", name, len(pairs))
