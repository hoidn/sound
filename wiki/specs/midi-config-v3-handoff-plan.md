---
id: PLAN-MIDI-CONFIG-V3-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Third MIDI configuration handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [midi-config-v3](../../handoff/midi-config-v3/README.md),
approved without narrowing by a separate review agent
([review record](../../handoff/midi-config-v3/REVIEW.md)); manifest SHA-256
`2e7d93767bbb9fffa79cec191b242d7eec52aeb1d20f6f33f1bbdc0beff40458`. It has
127 cases and supersedes midi-config-v2 as a strict superset: the 109 carried
cases and fixtures are byte-identical to v2. The reviewer kept cases 110 to 114 and 124, because
their values need only a takeover choice that never acts, read directly from
the retained evidence; which label a reference run selects (None) stays a stated
assumption. Findings F1 (the crossfader takeover exemption holds for Absolute
values only) and F2 (the stepped rule with a reversed range) are confirmed for
the draft spec.

## Decision and boundary

Stage a third finite candidate, midi-config-v3, from
[revision 3 of the MIDI specification](midi-user-mapping.md). It follows the
structure and gates of the [midi-config-v2 plan](midi-config-v2-handoff-plan.md)
and the [als-container plan](als-container-handoff-plan.md), and the
[release workflow](../workflows.md#release-a-handoff). The scope is
everything in [midi-config-v2](../../handoff/midi-config-v2/README.md),
carried unchanged, plus the REQ-MIDI-USER-005 value transforms that revision 3
labels S and the REQ-MIDI-USER-010 crossfader exemption. Those clauses come
from the [native transform packet](../research/midi-transforms-native.md).
Configuration interpretation stays as classified in the
[S4 closure assessment](../research/midi-closure-r2.md#clause-classification).
When published, the candidate supersedes midi-config-v2 as a strict superset.
v2 stays immutable and valid for its narrower scope.

The 18 S rows of the revision 3 transform table (MT-01 to MT-16, MT-22,
MT-23) are released with exact values. The five S-cond rows (MT-17 to MT-21)
are left out, because their conditions are unresolved. PRB-N7-03 (Pick-Up,
Value Scaling, labels and default) and PRB-N7-04 (on/off thresholds) have not
run; [the probe records](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/probe-records.json)
are `proposed; not run`, and [Q-009](../questions.md#q-009-midi-numerical-modes-timing-and-feedback)
is open. Under [ADR 0002](../decisions/adr-0002-static-first-analysis.md),
every expectation is a static derivation.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
reference or candidate execution has run, and no compatibility is claimed.

## Scope

| Requirement | Included in v3 | Excluded remainder |
| --- | --- | --- |
| 001, 004 | None | As in v2 |
| 002, 003, 006–009, 011–013 | v2 clauses, unchanged | As in v2 |
| 005 | v2 label clauses. New: messages and routing (channel, number, and *n* + 32 for 14-bit); target parameter with min, max, stepped and four kinds; Absolute; Absolute14Bit pairing; relative decode table, A and B; relative steps, clamping, stepped ±1; stepped rounding; takeover choice `none` (assumption I1); exemptions for relative values, enumerated and other kinds, and crossfader Absolute | Pick-Up and Value Scaling (S-cond, PRB-N7-03); on/off parameters (S-cond, PRB-N7-04); takeover default and labels (PRB-N7-03); ordering, coalescing, deferral (PRB-N7-05); displayed values and post-set processing (PRB-N7-01); parameter kind membership (PRB-N7-04); unknown tokens (PRB-S4-04); several assignments on one address; first 14-bit pair under other choices; crossfader Absolute14Bit under other choices (F1); min ≥ max (F2); stepped parameters with non-integer bounds |
| 010 | v2 clauses; master, cue and crossfader values follow 005; crossfader Absolute exempt | Crossfader Absolute14Bit takeover (F1); reported ranges and kinds of the three parameters (PRB-N7-01) |

Case mapping: MT-01 to MT-16 become MIDI-CONFIG-110 to 125, MT-22 becomes 126
and MT-23 becomes 127. The `takeover` field is `none` for MT-01 to MT-05 and
MT-15, and `any` for the rest. The spec states that MT-06 to MT-14, MT-16
and MT-23 hold under any setting, and the crossfader exemption makes MT-22
hold under any setting too. The N7 case file says "Takeover Mode None" for
MT-16; apply 0x101b7fde4 evaluates takeover only for map modes 0 and 5, so
`any` is supported. Each value fixture assigns `Encoder1` (or
`CrossfaderSlider` for 126) to CC 20 on channel 0 with an explicit map-mode
key. That is the minimal input of PRB-N7-01.

## Findings while staging

Proposed corrections for a spec revision 4. This page does not edit the spec.

- **F1 (spec error).** REQ-MIDI-USER-005, takeover exemptions, says the
  crossfader is never subject to takeover, "whatever the takeover preference".
  REQ-MIDI-USER-010 says its absolute values apply whatever the preference.
  Both hold only for `Absolute`. The 14-bit install `0x1026094e0` is called at
  `0x10259338c` with x0–x4 only, so no avoid argument reaches it. It builds the
  pair receiver with the flag cleared (`mov w3,#0x0` at `0x102609548`; N7 notes
  item 8; the research page says "The 14-bit receiver's opt-out flag is fixed at
  false"). The completed pair goes to apply as map mode 0 with its priors
  present, so takeover is evaluated for a crossfader set to `Absolute14Bit`
  at CC 95 or below. In the N7 model, starting from 0.5 under Pick-Up, a
  crossfader `Absolute` 0x20 sets 0.251969, while an `Absolute14Bit` pair
  (0x20, 0x00) leaves 0.5. The candidate narrows the exemption to crossfader
  `Absolute` values and excludes crossfader `Absolute14Bit` values under the
  other choices.
- **F2 (imprecision).** The value function works on the lower and upper bound
  and inverts when the reported maximum is below the minimum: t = (127 − v)/127
  and the step is negated (`0x101b76bf0`, inversion argument `Max < Min` from
  apply). The Absolute and non-stepped relative formulas as written still hold.
  The stepped rule "+1 when d > 0", however, means toward max, which is
  numerically down for a reversed range. The spec does not mention reversed
  ranges. The candidate requires min < max.
- **F3 (case file, not spec).** MT-16 in `out/acceptance-cases.json` names
  Takeover Mode None; the spec's "any takeover setting" is correct. Both give
  the same values.

## Deliverables

- Payload: [midi-config-v3/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v3/README.md)
  (scope, supersession, change list), `AGENTS.md`, `spec.md` (v2 contract plus
  value transforms and value cases), `cases.json` (127 cases), `fixtures/` (127
  files) and a draft `manifest.json` (`release_status: candidate-unreviewed`,
  review pending, `supersedes: midi-config-v2` with the superseded manifest
  digest and the change list). The manifest lists 131 payload files; with
  itself the package has 132. Draft manifest SHA-256:
  `575af45d2340b5ad74a865d1be56145e2754be9039abc874bcb52a1b87dcd192`. Review
  edits will change it.
- Analyst side, never shipped: `midi-config-v3-analysis/` with
  [build_v3.py](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v3-analysis/build_v3.py)
  (fixtures, cases, manifest, exact restatement, cross-checks, seal and
  verify), [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v3-analysis/traceability.json)
  (every case and clause to its evidence and inferences),
  [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v3-analysis/author-validation.json)
  and [v2-to-v3-text.diff](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v3-analysis/v2-to-v3-text.diff).

## Evidence traceability

Evidence is the [N7 packet](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/notes.md)
(manifest SHA-256 `385d3ea6…78912ec`; all 77 listed files re-hashed on
2026-10-18 and matched; `Live.arm64` `3a99ceea…383cfad`), cited by its labels
E10 to E14 in the spec appendix, plus the v2 release for cases 001 to 109.
Per-case and per-clause locators are in `traceability.json`; the payload
contains none of them.

| v3 cases | Source | Kept evidence | Inferred links |
| --- | --- | --- | --- |
| 001–109 | midi-config-v2, same IDs; records and fixture bytes identical | v2 review and v2 traceability | As in v2 |
| 110 | MT-01 | E10 install and dispatch; E12 value function, absolute branch; E13 apply; E14 takeover choice 0 | I1–I4 |
| 111–114 | MT-02 to MT-05 | E11 pairing, stores and combine; E12; E13; E14 | I1–I4 |
| 115–123 | MT-06 to MT-14 | E12 decoder, tables and relative branch; E13 apply (no takeover outside modes 0 and 5) | I2–I4 |
| 124 | MT-15 | E12 `frinta` at 0x101b76cd4; E13; E14 | I1–I4 |
| 125 | MT-16 | E12 ±1 step; E13 receiver accumulator | I2–I4 |
| 126 | MT-22 | E10 GenericScript L216 and `_install_mapping`; E13 receiver prior blanking and the apply condition | I2–I4 |
| 127 | MT-23 | E13 apply condition | I2–I4 |

| Link | Inference not established by kept evidence | Affects |
| --- | --- | --- |
| I1 | Takeover choice 0 is the preference choice labelled None: the UI entries are declared in the order no takeover, pick-up, value scaling (`0x1022df424`, decompiler only), and choice 1 posts the pick-up notification | Cases 110–114 and 124. The contract states it as an assumption with a comparison obligation |
| I2 | The handler registry is the MidiMap's, and dispatch entry +0x30 holds the installed map mode (spec E10 inference) | Every value case |
| I3 | Setter `0x101b0d328` (untraced) stores the value without further processing | Every value case; the contract makes it a precondition and excludes parameters that change a value |
| I4 | One application per message, in arrival order; the queued-command path has unknown timing | Every multi-message case; the contract applies messages one at a time and excludes back-to-back behavior |
| I5 | `Layer` wiring from control to setter, assumed since revision 1 | Every target association, as in v2 |

## Mechanical checks performed

`build_v3.py build` then `seal`, run with CPython 3.11.13 `-I`, wrote the
author validation. A second build and seal reproduced the same draft manifest
digest.

- **Carry.** The first 109 case records equal midi-config-v2's, the fixture
  bytes are identical, and the v2 representation fields are kept.
  `v2-to-v3-text.diff` lists every changed v2 line: the title, status and
  release lines; the summary, evidence, REQ-005 and REQ-010 sentences that left
  values unspecified; the excluded-behavior phrase; the v1 change heading; and
  the review link in the provenance note.
- **Fixtures.** All 127 are ASCII with LF endings, a final newline and no
  control characters. Each parses in the host 3.11.13 parser. The v2 cross-check
  model agrees with all 127 assignment expectations, and the MIDI addresses
  are distinct.
- **Values.** The build computes every expected value in exact rational
  arithmetic from the released clauses and rounds it to nine decimals. Three
  other sources agree with each value within 1e-6: the revision 3 MT table,
  the N7 case file, and the N7 float32 model. For `any` cases the model was run
  under all three takeover choices. The restated decode table matches the N7
  decoder over all 8 × 128 data values. A and B equal the image constants. The
  payload's decode rows equal the spec's.
- **Selection.** The released rows are exactly the spec's S rows, and the
  excluded rows exactly its S-cond rows. The restatement gives no expectation
  for on/off parameters, min above max, a stepped non-integer value, a
  continuous `Absolute` value under `any`, or a crossfader `Absolute14Bit`
  value under `any`.
- **Package.** The hashes and sizes of the 131 listed files match, and the
  inventory equals the directory. All 18 Markdown links (README 5, spec 13)
  resolve inside the package, and all case inputs exist. The deny-list
  (analyst paths, addresses, internal and native names, tool and arithmetic
  terms, probe, case and evidence IDs, absolute paths) hits only "decompil" in
  the forbidden-inputs list of `AGENTS.md`, worded as in the released
  packages. A planted copy was flagged.
- **Export.** `verify` of the export copy in the session scratchpad matched
  everything above, and the copy is byte-identical to staging.

Not checked: reference or candidate execution, any proof of I1 to I5, and
independent recomputation. The restatement, the table, the case file and the
model share the same static evidence; none is an oracle.

## Review gates still required

1. **Scope review**, in a separate context. Check every new clause against
   E10 to E14 and read all 18 value cases one by one. Rule on I1: if it is not
   accepted, remove cases 110 to 114 and 124 and the `none` choice, which
   leaves 12 value cases. Rule on the F1 and F2 narrowings, and confirm `any`
   for MT-16 and MT-22.
2. **Strict superset**: confirm from the diff and the carry checks that no v2
   clause, case or fixture changed and no v2 statement is contradicted.
3. **Quality and sanitization review**: behavioral completeness and the value
   comparison convention. Confirm the exclusions agree between spec and
   manifest, there are no internal names or analyst links, and nothing is
   claimed beyond static derivation. The public preference choice labels
   (None, Pick-Up, Value Scaling) are named only as UI labels.
4. **Evidence identity**: the N7 files matched on 2026-10-18. Decide whether
   the `Live.arm64` digest needs recomputing before release.
5. **Fixture and sharing review** of the 18 new fixtures: short authored files
   with public key names.
6. **Finalize**: add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the handoff catalog.
7. **Publish** only after approval. Copy the package unchanged to
   `handoff/midi-config-v3/`. Add a catalog row superseding midi-config-v2.
   Update the spec status, coverage, indexes, Q-009 and the log, and carry
   F1 and F2 into a spec revision. Never edit midi-config-v2.
8. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate with 127 cases (109 carried, 18
new value cases). It covers partial REQ-MIDI-USER-002, 003 and 005 to 013;
001 and 004 remain unreleased. It is not published, and midi-config-v2 remains
the current MIDI release.
