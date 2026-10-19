"""Apply the reviewer's payload edits to the mix-graph-v1 staging copy (analyst side; never shipped).

usage: python3 -I -B apply_review_edits.py
Each edit replaces text that must occur exactly once; a re-run skips edits already applied. Run before
finalize_manifest.py. RMG-01: REQ-013's Float value and REQ-014 stated for the default automation settings;
which parameters use them, and any parameter's value step, not released; stated assumptions 2 and 3 removed.
RMG-02: the render-case envelope exclusion exempts the main track's one-event tempo and time-signature
envelopes that every fixture holds. RMG-03: REQ-013's sample-timing sentence moved to the not-released
list; first-time replacement scoped to Float envelopes; Bool and Enum values at or after the first event.
RMG-11: category labels, pan-law provenance, send-reach wording, draft-case sentence. RMG-12: status lines.
No case record, fixture or signal is touched (cases.json: top-level status only).
"""
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "mix-graph-v1"
EDITS = {
    "README.md": [
        ("**Unreviewed handoff candidate.** Read [the contract](spec.md),\n"
         "[the cases](cases.json), [the role instructions](AGENTS.md) and\n"
         "[the manifest](manifest.json). This package has not been reviewed and is not a\n"
         "released contract. It must not be used for implementation until a separate\n"
         "review approves it.",
         "**Reviewed local release.** Read [the contract](spec.md),\n"
         "[the cases](cases.json), [the role instructions](AGENTS.md),\n"
         "[the manifest](manifest.json) and [the review disposition](REVIEW.md). The\n"
         "stated partial scope, with the narrowing recorded in the review, is approved\n"
         "as a contract for a fresh, restricted implementation workspace. Such a\n"
         "workspace has not been provisioned by this release."),
        ("events become the values it plays. Requirement IDs are retained with explicit\n"
         "partial clauses. Requirements 012, 015 and 016 (which envelope drives a\n"
         "parameter, the units of automated values, automated against manual values)\n"
         "are not released.",
         "events become the values it plays under the default automation settings.\n"
         "Requirement IDs are retained with explicit partial clauses. Requirements 012,\n"
         "015 and 016 (which envelope drives a parameter, the units of automated values,\n"
         "automated against manual values) are not released."),
    ],
    "AGENTS.md": [
        ("This is an unreviewed handoff candidate for its explicit partial scope. It is\n"
         "not a released contract and must not be used for implementation before a\n"
         "separate review approves it. Application implementation requires a fresh,\n"
         "restricted implementation workspace that contains only permitted materials. Do\n"
         "not begin clean implementation in an analyst checkout.",
         "This is a reviewed local release for its explicit partial scope. Application\n"
         "implementation requires a fresh, restricted implementation workspace that\n"
         "contains only permitted materials. Publication of this package does not\n"
         "provision one. Do not begin clean implementation in an analyst checkout."),
    ],
    "cases.json": [
        ('"status": "candidate-unreviewed"', '"status": "released-reviewed"'),
    ],
    "spec.md": [
        ("**Status: unreviewed handoff candidate.** It is not a released contract.",
         "**Status: reviewed local release.** A separate review approved the clauses\n"
         "below with the narrowing recorded in [the review disposition](REVIEW.md).\n"
         "Implementation requires a fresh, restricted implementation workspace."),
        # RMG-01: assumptions 2 and 3 removed; 4 renumbered
        ("2. Mixer parameters use the application's default automation settings: no\n"
         "   smoothing, a minimum ramp of 200 samples, and a value step of one\n"
         "   thousandth of the parameter's range ([REQ-014](#req-mix-graph-014--partial-how-often-an-automated-value-moves)).\n"
         "   No other setting was found for them.\n"
         "3. The range of pan and split pans for that step is −1 to 1.\n"
         "4. A Live Set in which no mixer stores `SoloSink` as `true` has no soloed\n"
         "   track.",
         "2. A Live Set in which no mixer stores `SoloSink` as `true` has no soloed\n"
         "   track."),
        ("  0.00032.\n"
         "- The **stored minimum**",
         "  0.00032.\n"
         "- The **default automation settings** are the application's defaults for an\n"
         "  automated value: a value step q of one thousandth of the parameter's value\n"
         "  range, a minimum ramp of 200 samples and no smoothing. REQ-013's Float value\n"
         "  and REQ-014 are stated for these settings. Which parameters use them, and so\n"
         "  the value step of any parameter, is not released.\n"
         "- The **stored minimum**"),
        # RMG-11: pan-law provenance aligned with the formula's support
        ("  gain of REQ-003, and P the pan-law matrix below (extracted execution).",
         "  gain of REQ-003, and P the pan-law matrix below. The product m·P is\n"
         "  extracted execution."),
        ("  I; with split pans (0, 0): 0.70710677 for all four gains.\n- The split amount",
         "  I; with split pans (0, 0): 0.70710677 for all four gains. The formula is\n"
         "  static-derived; extracted execution of the original code gave exactly the\n"
         "  example gains.\n- The split amount"),
        # RMG-11: category labels; renumbered assumption
        ("  A soloed track therefore plays even when its track switch is off.\n"
         "- Which category a track is in is not released, with one exception: in a Live\n"
         "  Set in which no mixer stores `SoloSink` as `true`, no track is soloed and\n"
         "  every track is unaffected (stated assumption 4).",
         "  A soloed track therefore plays even when its track switch is off. The\n"
         "  categories are labels of this rule; they imply no stored value and no\n"
         "  required internal state.\n"
         "- Which category a track is in is not released, with one exception: in a Live\n"
         "  Set in which no mixer stores `SoloSink` as `true`, no track is soloed and\n"
         "  every track is unaffected (stated assumption 2)."),
        # RMG-01, RMG-03: REQ-013
        ("computation. Not released here: which envelope drives a parameter and when, the\n"
         "mapping from song position to envelope time, and the units in which the values\n"
         "of any parameter's envelope are played. Values below are in the envelope's own\n"
         "value units.",
         "computation. Not released here: which envelope drives a parameter and when, the\n"
         "mapping from song position to envelope time and the samples at which point\n"
         "times take effect, the automation settings of any parameter, and the units in\n"
         "which the values of any parameter's envelope are played. Values below are in\n"
         "the envelope's own value units."),
        ("  - The first event's time is replaced by −10,000,000 beats, whatever it was.\n"
         "    In documents the first event is the leading event at −63,072,000 beats.",
         "  - In a Float envelope, the first event's time is replaced by −10,000,000\n"
         "    beats, whatever it was. In documents the first event is the leading event\n"
         "    at −63,072,000 beats."),
        ("  the same time, the later one applies. Point times take effect at exact\n"
         "  samples, independent of the buffer size.",
         "  the same time, the later one applies."),
        ("- **Float value.** In a segment from (ta, va) to (tb, vb), with S samples per\n"
         "  beat (sample rate × 60 / tempo):",
         "- **Float value**, with the default automation settings. In a segment from\n"
         "  (ta, va) to (tb, vb), with S samples per beat (sample rate × 60 / tempo):"),
        ("  - after the last point the value holds.\n"
         "- **Bool and Enum values.** The value of the current point, without\n"
         "  interpolation.",
         "  - after the last point the value holds;\n"
         "  - other automation settings have no expectation.\n"
         "- **Bool and Enum values.** At an envelope time at or after the first event's\n"
         "  time, the value of the current point, without interpolation."),
        # RMG-01: REQ-014
        ("- While the transport plays, a Float parameter driven by an envelope moves\n"
         "  along its current segment (REQ-013) through ramps of L samples. With slope s\n"
         "  per sample and value step q, let r = q/|s| in binary64.",
         "- With the default automation settings, while the transport plays, a Float\n"
         "  value driven by an envelope moves along its current segment (REQ-013)\n"
         "  through ramps of L samples. With slope s per sample and value step q, let\n"
         "  r = q/|s| in binary64."),
        ("- q is one thousandth of the parameter's value range (stated assumption 2). For\n"
         "  pan and split pans, whose range is −1 to 1, q is 0.002 (stated assumption 3).\n"
         "  Volume and send automation are not released.",
         "- q is an input of this rule: one thousandth of the value range of the\n"
         "  parameter the envelope drives. Which parameters use the default automation\n"
         "  settings, and so the q of any parameter, is not released. Volume and send\n"
         "  automation are not released."),
        # RMG-11: send-reach wording; RMG-02: envelope exclusion
        ("  main track, that is, its track's send gate is on and its return track plays;",
         "  main track, that is, its track's send gate is not 0 and its return track's\n"
         "  main gate is not 0;"),
        ("- in render cases, automation envelopes on any mixer or device parameter, and\n"
         "  clip envelopes;",
         "- in render cases, automation envelopes on any mixer or device parameter, other\n"
         "  than the main track's one-event tempo and time-signature envelopes whose\n"
         "  single event equals the stored value (every fixture holds these two); clip\n"
         "  envelopes;"),
        ("- which envelope drives a parameter and when; the mapping from song position to\n"
         "  envelope time; automated against manual values;",
         "- which envelope drives a parameter and when; the mapping from song position to\n"
         "  envelope time and the samples at which point times take effect; automated\n"
         "  against manual values;\n"
         "- which parameters use the default automation settings, and the value step of\n"
         "  any parameter;"),
        ("the draft's unresolved cases; and a draft case on internal solo predicates\n"
         "that has no observable here.",
         "the draft's unresolved cases; and a draft case with no observable in this\n"
         "release."),
        ("public source or dependency is approved or included. Review status is recorded\n"
         "in [the manifest](manifest.json).",
         "public source or dependency is approved or included. Review status is recorded\n"
         "in [the manifest](manifest.json) and [the review disposition](REVIEW.md)."),
    ],
}

for name, edits in EDITS.items():
    p = PKG / name
    text = p.read_text()
    for old, new in edits:
        if old not in text and new in text:
            continue  # already applied
        assert text.count(old) == 1, (name, old[:60])
        text = text.replace(old, new)
    p.write_text(text)
    print(name, "edited")
