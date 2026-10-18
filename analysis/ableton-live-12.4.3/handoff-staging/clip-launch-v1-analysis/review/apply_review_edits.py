"""Reviewer edits to the staged clip-launch-v1 payload (spec.md, README.md, AGENTS.md, cases.json status).

usage: python3 -I apply_review_edits.py <package dir>
Each replacement must match exactly once. The manifest is edited separately (edit_manifest.py).
"""
import re, sys
from pathlib import Path

pkg = Path(sys.argv[1])


def sub(name, pairs):
    p = pkg / name
    t = p.read_text()
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, (name, n, old[:60])
        t = t.replace(old, new)
    p.write_text(t)


REQ015 = re.compile(r"### REQ-CLIP-LAUNCH-015 .*?(?=## Acceptance representation and comparison)", re.S)

spec = (pkg / "spec.md").read_text()
assert len(REQ015.findall(spec)) == 1
(pkg / "spec.md").write_text(REQ015.sub("", spec))

sub("spec.md", [
    ("**Status: staged candidate, not reviewed and not released.** It is not an\n"
     "implementation input until a separate review approves it.",
     "**Status: reviewed local release.** A separate review approved the clauses\n"
     "below with the narrowing recorded in [the review disposition](REVIEW.md).\n"
     "Implementation requires a fresh, restricted implementation workspace."),
    ("- what each stored value means and how it is labeled, and the grid length that\n"
     "  each quantization value stands for;",
     "- what each stored value means and how it is labeled;"),
    ("It does not describe launching. That includes when a launched clip starts, how\n"
     "quantization places a launch on the grid, and what",
     "It does not describe launching. That includes when a launched clip starts, the\n"
     "grid length that a quantization value stands for, how quantization places a\n"
     "launch on the grid, and what"),
    ("  clip or follow action starts with, and a value that is present is kept as\n"
     "  read, without adjustment to a range;",
     "  clip or follow action starts with, and a value that is present and inside\n"
     "  the ranges of the preconditions is kept as read;"),
    ("6. A written value, read back with the reading rules above, gives the value\n"
     "   held. The exact text written for numbers and Booleans is not part of this\n"
     "   release.",
     "6. A written Boolean, or a written number whose value has at most six\n"
     "   significant decimal digits, read back with the reading rules above, gives\n"
     "   the value held. For other numbers this is not part of this release, and\n"
     "   neither is the exact text written for numbers and Booleans."),
    ("A clip value k from 1 to 14 stands for the setting of global value k − 1. Clip\n"
     "value 0 means that the clip uses the set's global setting.",
     "A clip value k from 1 to 14 denotes the same setting as global value k − 1,\n"
     "with the same label. Clip value 0 (Global) denotes the set's global setting.\n"
     "Which setting, time signature and grid a launch uses is excluded."),
    ("2. Hence a `11.0_405` document passes through steps 406, 417, 421 and 12203; a\n"
     "   `12.0_12117` document through step 12203 only; a `12.0_12402` document\n"
     "   through none of them.",
     "2. Hence, of these steps, a `11.0_405` document passes through 406, 417, 421\n"
     "   and 12203; a `12.0_12117` document through 12203 only; a `12.0_12402`\n"
     "   document through none. Older documents also pass through other conversion\n"
     "   steps. Those are excluded, and none of them changes an item that this\n"
     "   release describes."),
    ("| `saved.clip_order` | A clip path. In the saved document that clip's five launch elements each occur once in the relative order of REQ-CLIP-LAUNCH-001, and its `FollowAction` has exactly the ten children of REQ-CLIP-LAUNCH-002 in that order |\n",
     "| `saved.clip_order` | A clip path. In the saved document that clip's five launch elements each occur once in the relative order of REQ-CLIP-LAUNCH-001, and its `FollowAction` has exactly the ten children of REQ-CLIP-LAUNCH-002 in that order |\n\n"
     "`saved.values` lists only Booleans and numbers with at most six significant\n"
     "decimal digits (REQ-CLIP-LAUNCH-001 clause 6).\n"),
    ("**REQ-CLIP-LAUNCH-010** (the initial launch mode and launch quantization of a\n"
     "new clip, and a clip without `LaunchMode` or `LaunchQuantisation`) and\n"
     "**REQ-CLIP-LAUNCH-016 to 023**",
     "**REQ-CLIP-LAUNCH-010** (the initial launch mode and launch quantization of a\n"
     "new clip, and a clip without `LaunchMode` or `LaunchQuantisation`),\n"
     "**REQ-CLIP-LAUNCH-015** (the grid length that a quantization value stands for\n"
     "with a given time signature; it has no observable outside launching) and\n"
     "**REQ-CLIP-LAUNCH-016 to 023**"),
    ("- in `11.0_405` documents: a clip that already has `FollowAction`; a clip\n"
     "  without `FollowActionA`, `FollowActionB`, `FollowChanceA` or\n"
     "  `FollowChanceB`; scenes;",
     "- in `11.0_405` documents: a clip that already has `FollowAction`; a clip\n"
     "  without `FollowActionA`, `FollowActionB`, `FollowChanceA` or\n"
     "  `FollowChanceB`, or with a `FollowActionEnabled` or `IsLinked` child;\n"
     "  scenes;"),
    ("- launching: when a launched clip starts, grid placement, the time signature a\n"
     "  launch uses,",
     "- launching: when a launched clip starts, the grid length of a quantization\n"
     "  value, grid placement, the time signature a launch uses,"),
    ("- the text written for numbers and Booleans; layout and indentation;",
     "- the text written for numbers and Booleans, and whether a written number with\n"
     "  more than six significant digits reads back exactly; layout and indentation;"),
    ("dependency is approved or included. Review status is recorded in\n"
     "[the manifest](manifest.json).",
     "dependency is approved or included. Review status is recorded in\n"
     "[the manifest](manifest.json) and [the review disposition](REVIEW.md)."),
])

sub("README.md", [
    ("**Staged candidate, not reviewed and not released.** Read [the contract](spec.md),\n"
     "[the cases](cases.json), [the role instructions](AGENTS.md) and\n"
     "[the manifest](manifest.json). The package is not an implementation input\n"
     "until a separate review approves it and it is published. A fresh, restricted\n"
     "implementation workspace has not been provisioned.",
     "**Reviewed local release.** Read [the contract](spec.md), [the cases](cases.json),\n"
     "[the role instructions](AGENTS.md), [the manifest](manifest.json) and\n"
     "[the review disposition](REVIEW.md). The stated partial scope, narrowed as\n"
     "recorded in the review, is approved as a contract for a fresh, restricted\n"
     "implementation workspace. Such a workspace has not been provisioned by this\n"
     "release."),
    ("what each value means and how it is labeled, the grid length each quantization\n"
     "value stands for, which text",
     "what each value means and how it is labeled, which text"),
    ("Requirements 008, 010 and 016 to 023, and every\neffect on launching or playback,",
     "Requirements 008, 010 and 015 to 023, and every\neffect on launching or playback,"),
])

sub("AGENTS.md", [
    ("This is a staged, unreviewed candidate for its explicit partial scope. It is\n"
     "not an implementation input until a separate review approves and publishes\n"
     "it. Application implementation requires a fresh, restricted implementation\n"
     "workspace that contains only permitted materials. Do not begin clean\n"
     "implementation in an analyst checkout.",
     "This is a reviewed local release for its explicit partial scope. Application\n"
     "implementation requires a fresh, restricted implementation workspace that\n"
     "contains only permitted materials. Publication of this package does not\n"
     "provision one. Do not begin clean implementation in an analyst checkout."),
    ("Preserve this package unchanged.", "Preserve this release unchanged."),
])

sub("cases.json", [('"status": "candidate-unreviewed"', '"status": "released-reviewed"')])
print("edits applied")
