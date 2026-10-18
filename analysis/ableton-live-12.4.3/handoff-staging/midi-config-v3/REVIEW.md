# Review disposition

Release: midi-config-v3, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope and evidence,
supersession, quality and sanitization, evidence-identity and fixture-sharing
checks. Publication metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-MIDI-USER-002, 003
and 005 to 013 in [the contract](spec.md). REQ-MIDI-USER-001 and 004 remain
unreleased.

- Every new clause was checked against the reviewed static evidence for the
  pinned build: the channel and number a control acts on and the *n* + 32
  pairing, the `Absolute` and `Absolute14Bit` formulas and the holding and
  replacing of halves, every row of the decode table over all 128 data values
  and both step tables, the continuous and stepped relative rules, rounding
  with halves away from zero, clamping, the condition under which takeover can
  act, the `none` choice and the crossfader exemption. The step tables were
  re-read from the pinned program image. The author's cross-check was not
  relied on.
- All 18 value cases were read one by one. Two reviewer models agreed with
  every expected value within 1e-6: an exact restatement of the contract text,
  whose results rounded to nine decimals equal the expected values, and an
  independent single-precision transliteration of the reviewed evidence, whose
  largest difference was 1.8e-8. For each `any` case the second model was run
  under each of the three takeover choices; no value reached takeover and the
  values were identical.
- A reviewer-side interpretation model, written for the midi-config-v2 review
  and not by the author, agreed with all 127 assignment and bank-span
  expectations. This re-derives at least one expectation for every released
  requirement.
- Supersession. Cases MIDI-CONFIG-001 to 109 are byte-identical case records,
  and their fixtures byte-identical files, to the released midi-config-v2. That
  release's manifest digest equals the catalog value and every file it lists
  still matches. The changed midi-config-v2 text is limited to titles, status
  and release lines, the sentences that left values unspecified, the general
  value-transform exclusion and the earlier change-list heading. No v2 clause
  is changed or contradicted; v2 left values unspecified and this release
  specifies some of them. The strict-superset claim holds.
- Sanitization was checked by the reviewer's own scan of every payload file.
  No source code, recovered program text, internal identifiers or addresses,
  analyst paths, private evidence links, planning identifiers or per-case
  evidence fields are present. The only flagged word is in the forbidden-inputs
  list of `AGENTS.md`, worded as in the released packages. None, Pick-Up and
  Value Scaling appear only as preference labels.
- Scope. Every expectation is labeled static-derived, with reference and
  candidate execution not run. No timing, display or audio result is released.
  No expected value depends on an open item: the default choice, the behavior
  and labels of the other two choices, on/off parameters and back-to-back
  timing are excluded. Exclusions appear in both the contract and the manifest
  and agree.
- Every new fixture was read. Each assigns `Encoder1`, or `CrossfaderSlider`
  for MIDI-CONFIG-126, to number 20 on channel 0 with an explicit map-mode key.
  They are short authored ASCII files with LF endings and public key names, and
  contain no shipped file content. The message bytes and parameter
  descriptions are authored for these cases.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists, and every listed hash and size matches
  the inventory.

## Scope rulings

- Cases MIDI-CONFIG-110 to 114 and 124, takeover `none`: kept. Their expected
  values need only a choice under which takeover never acts, and the reviewer
  read that branch directly in the evidence. The contract defines `none` by
  that behavior, so an implementation does not depend on any label. Only the
  label used in a reference run rests on inference. It is supported by the
  declared order of the three choice texts and by the other two choices
  behaving as pick-up and as value scaling. The label is a stated assumption
  in the contract and the manifest, with a comparison obligation, like the
  assumptions accepted in earlier releases.
- Crossfader takeover narrowed to `Absolute` values: upheld (RV3-02).
- Range order narrowed to *min* < *max*: upheld (RV3-03).
- `any` for MIDI-CONFIG-125 and 126: confirmed (RV3-04).

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RV3-01 | Medium | Six value cases rest on the inference that the takeover choice under which takeover never acts is the one labelled None. | Accepted as a stated assumption, as ruled above. Cases kept; no change. |
| RV3-02 | Low | The parent draft says the crossfader is never subject to takeover whatever the preference. The evidence supports this only for `Absolute` values. A completed `Absolute14Bit` pair ignores the control's takeover opt-out, so under the other two choices a crossfader pair can be held where an `Absolute` value would apply. | Upheld the author's narrowing: the exemption covers crossfader `Absolute` values only, and crossfader `Absolute14Bit` values under the other two choices have no expectation, in the contract and the manifest. No case is affected. The parent draft's takeover exemptions and its master, cue and crossfader requirement need the same correction. |
| RV3-03 | Low | For a parameter reporting its maximum below its minimum, the `Absolute` and continuous relative formulas hold as written, but a stepped parameter moves one unit toward the maximum, which is numerically down, when *d* > 0. The parent draft's "+1 when *d* > 0" is wrong for such a range, and the draft does not mention reversed ranges. | Upheld the author's narrowing: *min* < *max* is required, and other ranges have no expectation. No case is affected. The parent draft should state the reversed-range rule or exclude reversed ranges. |
| RV3-04 | Info | MIDI-CONFIG-125 (stepped, relative) and MIDI-CONFIG-126 (crossfader `Absolute`) are labelled `any`. | Confirmed: relative values never reach takeover, and the crossfader's `Absolute` path skips it. Expected values unchanged. |
| RV3-05 | Info | Remaining inferences: the installed map mode governs each message; the target keeps exactly the value set; one application per message, in arrival order; the control-to-target association carried from earlier releases. | Accepted. The contract makes the second a precondition, requires each message to be applied before the next, and excludes back-to-back timing. No expectation invented. |
| RV3-06 | Info | Evidence identity. | The pinned program image and every file of the evidence run were re-hashed on 2026-10-18; all matched the recorded digests. |
| RV3-07 | Info | No case exercises enumerated or other kinds, master, cue, send or track-volume values, crossfader `Absolute14Bit` values under `none`, a decoded 0 on a stepped parameter, or values of an `Absolute14Bit` control above number 95. The 1e-6 absolute tolerance assumes ranges of order one; the crossfader substitute rule keeps it. | Clauses are supported; cases and a range-scaled tolerance are proposed for a later revision. No expectation was invented. |
| RV3-08 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release; this record added and linked. Manifest review and status fields filled; inventory re-hashed by the reviewer. |

## Disposition

**Approved**, only for the explicit partial clauses in the contract, with the
author's narrowing upheld (RV3-02 and RV3-03). All expected outcomes remain
static-derived. Neither reference nor candidate application cases have run,
and no compatibility pass is claimed. Candidate-only checks cannot replace
independent reference observations. An isolated implementation workspace
remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. midi-config-v2 remains valid for its narrower
scope. Preserve this release unchanged.
