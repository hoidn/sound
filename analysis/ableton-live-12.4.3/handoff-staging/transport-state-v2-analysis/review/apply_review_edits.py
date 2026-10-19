"""Apply the reviewer's text edits to the staged transport-state-v2 payload (run once; fails on any miss).

usage: python3 -I -B apply_review_edits.py
Edits README.md, AGENTS.md, spec.md and cases.json in place by exact replacement; the manifest is
finalized separately by finalize_manifest.py after REVIEW.md exists.
"""
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "transport-state-v2"

EDITS = {
    "spec.md": [
        ("**Status: staged candidate; not reviewed; not released.** Do not implement from\n"
         "it. A separate review must approve it first.",
         "**Status: reviewed local release.** A separate review approved the clauses\n"
         "below with the clarifications recorded in [the review disposition](REVIEW.md).\n"
         "Implementation requires a fresh, restricted implementation workspace."),
        ("- **Extracted execution**: the original program's own code for converting the\n"
         "  value text was run on the case's text. It ran on a Linux x86_64 host, from the\n"
         "  program's x86_64 build, with glibc in place of the macOS system libraries. The\n"
         "  macOS arm64 build is inferred to give the same result.\n\n"
         "Locating the value, opening the document and saving it are static-derived in\n"
         "every case. The extracted-execution cases rest on three stated assumptions:\n\n"
         "- the macOS arm64 build converts these texts as the x86_64 build does;\n"
         "- on save, the base-10 logarithm is within 0.8 of a binary64 gap of the exact\n"
         "  value at the values of TS-024 to TS-027, whose logarithms lie 0.02 to 0.17 gaps\n"
         "  from an integer;\n"
         "- the decimal reading in TS-034 and TS-035 follows the C-standard number grammar.\n",
         "- **Extracted execution**: the original program's own code that reads the value\n"
         "  text was run on the case's text and, where a saved text is judged, its code\n"
         "  that writes the value text was run on the value read. It ran on a Linux x86_64\n"
         "  host, from the program's x86_64 build, with glibc in place of the macOS system\n"
         "  libraries. The macOS arm64 build is inferred to give the same result.\n\n"
         "Locating the value, opening the document and saving it are static-derived in\n"
         "every case. The extracted-execution cases rest on four stated assumptions:\n\n"
         "- the macOS arm64 build converts these texts and values as the x86_64 build does;\n"
         "- on save, the base-10 logarithm the program computes is within 3/4 of a\n"
         "  binary64 gap of the exact value wherever its last bit decides k in REQ-011,\n"
         "  outside the values excluded there. TS-024 to TS-027, whose logarithms lie 0.02\n"
         "  to 0.17 gaps from an integer, need only an error below 0.8 of a gap;\n"
         "- the decimal reading in TS-024 to TS-028, TS-034 and TS-035 follows the\n"
         "  C-standard number grammar and gives the nearest binary64 value, keeping the\n"
         "  sign of `-0`, as the glibc run did;\n"
         "- the fixed-point text on save is exact, rounds exact decimal ties to even and\n"
         "  keeps the sign of negative zero, as the glibc run did. No case lies on a tie.\n"),
        ("  Tempo values are never affected.\n- Examples: 120",
         "  Tempo values are never affected.\n"
         "- Values whose log10|x| is not an integer but lies between 1/4 and 3/4 of a\n"
         "  binary64 gap from one have no expectation, because the last bit of L is not\n"
         "  established there ([exclusions](#exclusions-and-deferred-obligations)).\n"
         "- Examples: 120"),
        ("Review status is recorded in [the manifest](manifest.json); this\n"
         "candidate has no review record yet.",
         "Review status is recorded in [the manifest](manifest.json) and\n"
         "[the review disposition](REVIEW.md)."),
    ],
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
        ("When published, this release supersedes transport-state-v1.",
         "This release supersedes transport-state-v1."),
        ("The original program takes it from the logarithm rounded to\n"
         "   the nearest binary64 value.",
         "The original program takes it from its binary64\n"
         "   logarithm, stated here as the logarithm rounded to the nearest binary64 value\n"
         "   outside the band of change 5."),
        ("TS-010 and TS-029 to\n   TS-033 are new. An accepted code outside 0 to 494 still has no expectation.",
         "TS-010 and TS-029 to\n   TS-033 are new. An accepted code outside 0 to 494 still has no expectation.\n"
         "   transport-state-v1 gave no expectation for opening a document whose code is\n"
         "   not 201; TS-030 now judges only that a document with code 0 (text `-0`)\n"
         "   opens. Whether a code other than 201 takes effect stays excluded."),
        ("5. **Exclusions.** One exclusion is narrowed and one is added. Values whose\n"
         "   logarithm lies within 1e-12 of an integer are no longer excluded. Values whose\n"
         "   logarithm lies between 1/4 and 3/4 of a binary64 gap from an integer now have no\n"
         "   expectation.",
         "5. **Exclusions.** The exclusion near integer logarithms is narrowed. Values\n"
         "   whose logarithm lies within 1e-12 of an integer are no longer excluded; only\n"
         "   values whose logarithm lies between 1/4 and 3/4 of a binary64 gap from an\n"
         "   integer have no expectation. Accepted time-signature codes outside 0 to 494,\n"
         "   which transport-state-v1 left without expectation through its value ranges,\n"
         "   are now also listed as an exclusion."),
        ("6. **Provenance.** The extracted-execution label is new. Every new case carries\n"
         "   it. Carried cases keep their records and the static-derived label.",
         "6. **Provenance.** The extracted-execution label is new. Every new case carries\n"
         "   it. Carried cases keep their records and the static-derived label. The\n"
         "   contract states the assumptions the extracted-execution cases rest on."),
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
        ('"status": "staged candidate; not reviewed; not released"', '"status": "released-reviewed"'),
    ],
}

for name, edits in EDITS.items():
    p = PKG / name
    t = p.read_text()
    for old, new in edits:
        assert t.count(old) == 1, f"{name}: expected one match for {old[:60]!r}, found {t.count(old)}"
        t = t.replace(old, new)
    p.write_text(t)
    print(f"{name}: {len(edits)} edits")
