---
id: PLAN-MIDI-NOTE-STORAGE-V2-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Second MIDI note storage handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [midi-note-storage-v2](../../handoff/midi-note-storage-v2/README.md), approved with listed clarifications by a separate review agent ([review record](../../handoff/midi-note-storage-v2/REVIEW.md)). It has 72 cases: 67 carried, each fixture its v1 file plus 20 added lines, and 5 new extracted-execution cases that re-run in agreement. No expectation changed.

Narrowings:
- REQ-007 now says a `Duration` of positive zero.
- Negative zero in `TimeOffset` is explicitly excluded.
- MNS-072 now lists REQ-002.

The change list is completed.

For the spec author:
- fix the "unchanged" wording in REQ-006 and REQ-007;
- correct the case table's requirement IDs for MNS-072 to 075;
- REQ-002 should state that `-0` reads as negative zero.

## Decision and boundary

Stage a corrected candidate, midi-note-storage-v2, from
[SPEC-MIDI-NOTE-STORAGE revision 3](midi-note-storage.md). It follows the
[midi-note-storage-v1 plan](midi-note-storage-handoff-plan.md), the
[transport-state-v2 plan](transport-state-v2-handoff-plan.md) (a superseding release with
extracted execution), the [als-container plan](als-container-handoff-plan.md), the
[midi-config-v2 plan](midi-config-v2-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff).

Why a new release:

- **Invalid fixtures.** The released [midi-note-storage-v1](../../handoff/midi-note-storage-v1/README.md)
  fixtures hold a MIDI track with one session slot and no freeze sequencer. Under
  [SPEC-LIVE-SET-STRUCTURE](live-set-structure.md) REQ-006 (S, A2 settled) such a set is not
  opened. The [audit](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/released-fixture-audit.json)
  finds 66 of the 67 fixtures refused: 51 cases expect `loads` and are contradicted, and 15
  refused cases no longer isolate their rule. MNS-012 is not well-formed XML, so the audit
  could not evaluate it. The [handoff catalog](../../handoff/index.md) warns against those
  expectations, and [Q-022](../questions.md#q-022-live-set-structure-load-rules) names this
  rebuild as its next action. Released payloads are immutable, so the fix is a new release.
- **Clauses settled since v1.** Revision 3 adds extracted-execution (X) results of
  [x2-notes-launch-v1](../../analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1/manifest.json)
  for the value limits (REQ-005), the time grid (REQ-006) and the saved number text
  (REQ-016), including negative zero. v1 excluded negative zero and had no case next to a
  halfway point or at the binary32 limit bounds.

Under [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code)
the five new cases carry the label "extracted execution (x86_64 slice, glibc substitutions);
arm64 equivalence inferred", as in transport-state-v2. Locating the notes, reading other text,
opening and saving stay static-derived. No reference application or candidate has run, and no
compatibility is claimed.

This page is the analyst-side plan and traceability record, not an implementation input. The
candidate is **unreviewed and unpublished**. Nothing has been written into `handoff/`.

## Scope

Selection rule: release only D, S or X clauses with exact values. Exclude U clauses, clauses that
depend on an open question, values outside the v1 ranges and runtime behavior. Unreleased:
REQ-011 (permanently excluded, Q-018), 012, 015 and 017.

| Requirement | Included in v2 | Excluded remainder |
| --- | --- | --- |
| 001, 003, 004, 007 to 010, 013, 014 | v1 clauses, unchanged | As in v1 |
| 002 | v1 clauses. New: a zero keeps the prefix's sign, so `-0` reads as negative zero (REQ-TRANSPORT-STATE-004 r4; X in x2-transport-v1) | `-0` in `VelocityDeviation`, event `Value` and curve controls; otherwise as v1 |
| 005 | v1 clauses. New (X): exact at the binary32 bounds; Velocity −0 becomes 1; OffVelocity and Probability −0 kept; Duration −0 kept by the limits | NaN and infinities (X recorded, excluded as in v1) |
| 006 | v1 clauses. New (X): the formula governs next to halfway points; −0 stored as +0; a value rounding to zero from below stored as −0 | ±1.7976931348623155e308 and +∞ (X, but outside the v1 magnitude range); `Time` `Invalid` after load (U, MNS-024) |
| 016 | v1 clauses. New (X): negative zero written `-0` | `Invalid` and `#` output (S, but no in-scope input produces them); values within 1e-12 of an integer logarithm (F5) |
| 011, 012, 015, 017 | None | All, as in v1 |

### Case disposition

| Draft cases | Candidate | Change |
| --- | --- | --- |
| The 67 midi-note-storage-v1 cases | Carried | Records identical to v1. Fixtures rebuilt (below). X corroborates MNS-014 to 022, 025, 067 and 069; records keep the static label (F6) |
| MNS-023 | New, X | Was U in r1 and r2; gradable since r3 (`-0`) |
| MNS-072 to 075 | New, X | Added in r3. MNS-073 to 075 also list REQ-002, and MNS-073 REQ-004 (F1) |
| MNS-011, 024, 034, 035, 037, 038, 053, 060 | Not released | Unresolved, as in v1 |
| MNS-054 to 059 | Not released | Blocked by the group shape, as in v1 |

That gives 72 cases: 56 expect `loads` and 16 `refused`; 54 are open-save. 67 are labelled
static-derived and 5 X.

## Fixture changes

The addendum to the staging brief requires every Live Set fixture on T11-MIN's rules, checked
with the T11 checker, and changes limited to what validity requires. Every fixture change:

| Fixtures | Change | Why |
| --- | --- | --- |
| All 67 carried | Add `<FreezeSequencer><ClipSlotList>` with one empty slot (`ClipSlot Id="0"`, inner `ClipSlot` with an empty `Value`, `HasStop` true) after the MIDI track's `MainSequencer` | The audit's `minimal_addition` for each of the 66 refused fixtures. Without it the set is refused (REQ-LIVE-SET-STRUCTURE-006, S) |
| All 67 carried | Add `<Scenes>` with one `Scene Id="0"` (empty `Name`, `Color` −1, `Tempo` 120, `IsTempoEnabled` false, `TimeSignatureId` 201, `IsTimeSignatureEnabled` false) after `Tracks` | The audit's `recommended_addition`. A set with slots but no scenes is REQ-006 U and an open gap of Q-022, so a `loads` expectation without it would rest on an open question |
| MNS-012 | The same two additions | The audit cannot parse it. With the additions, removing its repeated attribute gives exactly the MNS-001 fixture, which opens, so the repeat is its only defect |
| MNS-023, 072 to 075 (new) | v1 carrier plus the same two additions | Same carrier for every case |

Nothing else changes: the decompressed text of each carried fixture, with the 20 added lines
removed, equals its v1 fixture byte for byte, and its parsed tree equals the audit's repaired copy.
Elements T11-MIN writes but the fixtures omit stay absent. Absence is not an error by itself
(REQ-LIVE-SET-STRUCTURE-001, S). None of them affects the notes, and the audit and the checker
find no refusal and no unknown shape. They are track `Name`, `Color` and `AudioOutputRouting`,
the mixer, the main and cue tracks, `SendsPre` (no return tracks, so 0 items is the required
count), `NextPointeeId` (no pointees; absent reads 1), the session slot's `HasStop`, the
quantization fields and the other clip fields. One of them could in principle refuse a set:
`TrackGroupId`, if absence did not mean −1 (REQ-002). The track initializer sets it to −1
(corpus pseudocode, `traceability.json` `structure_evidence.track_group_default`; not re-read
in disassembly).

## Findings while staging

Spec errors and gaps (revision 3), for a later revision; this page does not edit the spec:

- **F1 (gap).** MNS-073 and MNS-074 read the text `-0`. That reading belongs to REQ-002 (through
  REQ-TRANSPORT-STATE-004 and 005), but the case table lists only 005 and 016 (MNS-073) and 005,
  006 and 016 (MNS-074). MNS-075 depends on the binary32 rounding of REQ-002 clause 4. MNS-073's
  saved `Probability` of −0 is written because REQ-004 omits only 1. The candidate adds 002 to all
  three and 004 to MNS-073, as v1's F4 did for `Invalid`.
- **F2 (precision).** REQ-006 says, as S, that values already on the grid are unchanged, and, as
  X, that −0 is stored as +0. −0 is on the grid, so the two clauses conflict. The candidate says
  "unchanged, except negative zero".
- **F3 (wording).** REQ-002 r3 does not repeat that `-0` reads as negative zero; it holds through
  REQ-TRANSPORT-STATE-004 r4. The candidate states it in REQ-002 clause 3, limited to the five
  note attributes with a negative-zero expectation. Not an error.

Points for the reviewer:

- **F4 (scope).** Negative zero stays excluded in `VelocityDeviation` (whether the omission
  test treats −0 as 0 was not run), in an event's `Value` (the clamp was not run) and in the curve
  controls (no X). A `TimeOffset` of −0 becomes +0, which is excluded by the edge rule.
- **F5 (number rule).** The candidate keeps v1's REQ-016 step 1 (exact logarithm) with its 1e-12
  exclusion. transport-state-v2 replaced that rule with the binary64 logarithm and a half-gap
  band. Outside the 1e-12 band both give the same k (transport-state-v2 F1, accepted in its
  review). The new saved values are `-0`, `0`, `1`, `127` and one grid unit (log10 −6.58).
  Aligning the rule with transport-state-v2 would widen the scope without a case, so it is left
  for a later revision.
- **F6 (carried labels).** The carried records keep the static-derived label, although X agrees
  with 12 of them (`x_corroboration` in `traceability.json`). Relabelling would change v1
  records, as transport-state-v2's review ruled.
- **F7 (assumptions).** MNS-073 rests on the `-0` reading assumption. MNS-074's results hold for
  either zero. MNS-023 and MNS-073 rest on the save text keeping the sign. All five rest on arm64
  equivalence. The v1 assumptions (refusal stops reading, open-save changes only by the rules,
  exact conversions with ties to even) are restated.
- **F8 (inference I4).** v1's inference that a carrier holding only the path to the clip reads
  the notes as a full set does now applies to a carrier that also satisfies the known structure
  rules. The reference comparison obligation is unchanged.
- **F9 (evidence identity).** The `t11-structure-v1` manifest lists `run.sh` as `0f04bd8e…`
  (1,311 bytes), but the committed file is `450c5f3e…` (1,314 bytes). The files this candidate
  uses match: `schema_check.py`, `fixture_audit.py`, `released-fixture-audit.json` and
  `make_fixture.py`. The x2-notes-launch-v1 (16 files) and x2-transport-v1 (14 files) manifests
  match.

## Deliverables

- Payload: [midi-note-storage-v2/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v2/README.md)
  (scope, supersession, change list), `AGENTS.md`, `spec.md` (contract, both provenance labels,
  stated assumptions, comparison convention and reference obligation), `cases.json` (72 cases),
  `fixtures/` (72 gzip `.als`) and a draft `manifest.json`. The manifest has review pending,
  `supersedes: midi-note-storage-v1` with the superseded manifest digest `90e79915…cc08e0d4`, the
  change list, the provenance labels and the stated assumptions. It lists 76 payload files; with
  itself the package has 77. Draft manifest SHA-256:
  `16463275ee3d7342807a3279c080bfb404f4d06a171161858bfa85a640b132fb`. Review edits will change it.
- Analyst side, never shipped: `midi-note-storage-v2-analysis/` with
  [build_v2.py](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v2-analysis/build_v2.py),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v2-analysis/traceability.json),
  [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v2-analysis/author-validation.json),
  [v1-to-v2-text.diff](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v2-analysis/v1-to-v2-text.diff),
  and the T11 checker outputs
  [t11-schema-check.jsonl](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v2-analysis/t11-schema-check.jsonl)
  and [t11-fixture-audit.json](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v2-analysis/t11-fixture-audit.json).
  - `build_v2.py` makes the fixtures, cases and manifest. It runs the cross-check model, the X
    agreement check, the carry check and the structure checks, then seals and verifies the
    package. It imports v1's `mns_cases`, `mns_model`, `mns_trace` and `build_mns`, and T11's
    `schema_check` and `fixture_audit`, all unchanged. The model is v1's with the negative-zero
    clauses swapped in for the duration of each call.
  - `traceability.json` maps every case to its v1 record or its X records, and records the
    structure evidence.

## Evidence traceability

| v2 cases | Evidence | Residual inference |
| --- | --- | --- |
| Carried 67 | v1 [traceability](midi-note-storage-handoff-plan.md#evidence-traceability) and [review](../../handoff/midi-note-storage-v1/REVIEW.md); `traceability.json` repeats each v1 entry | As in v1 (I2 to I7, RVN-11) |
| MNS-014 to 022, 025, 067, 069 | Also X: `results/notes.json` vectors of the same values, then `writer_texts` | None new; records unchanged |
| MNS-023, 072 | `notes.json` `MNS-023 n1` and `tie k=0 -1ulp`: held Time bits `8000000000000000` and `3e9175746e8cba40` (h); `writer_texts` double −0 → `-0`, h → `0.000000260156510156510156`. The X input bits equal the correctly rounded reading of the case text | arm64 (slice-compare: sign and grid sequences equal, no FMA effect); save text sign (glibc) for MNS-023 |
| MNS-073, 074 | `notes.json` `offvel -0`, `prob -0`, `vel -0`, `dur -0`, `time -0`; [x2-transport-v1](../../analysis/ableton-live-12.4.3/r2/x2-transport-v1/manifest.json) `results/parse.json` `-0` (double and float) → sign bit set, through the same text conversion as REQ-002; `writer_texts` float −0 → `-0`, 1 → `1`, double 0 → `0` | arm64; `-0` reading (glibc `strtod`) for MNS-073; save text sign for MNS-073 |
| MNS-075 | `notes.json` `vel above 127` (input bits `0x42fe0001`) and `vel below 1` (`0x3f7fffff`) → `0x42fe0000` and `0x3f800000`; `writer_texts` float 127 and 1 | arm64; binary32 reading of the text (static, as v1 MNS-019) |
| Every fixture | T11 checker (`schema_check.py`, `fixture_audit.py`), shipped schema `12.0_12402.txt` (SHA-256 `b7c9d4c7…`); audit entries for release midi-note-storage-v1 | REQ-LIVE-SET-STRUCTURE A2 settled; TrackGroupId default (corpus pseudocode) |

`build_v2.py seal` checks every new expectation against those X records and every corroborated
carried expectation the same way.

## Mechanical checks performed

`python3 -I build_v2.py build` then `seal` (CPython 3.13.9, zlib 1.3.1) wrote the author
validation. A second build and seal reproduced the same manifest digest.

- **Carry.** All 67 records equal v1's `cases.json`. Each carried fixture's text, with the added
  lines removed, equals the v1 fixture, and each new fixture's equals the v1 carrier form.
- **Structure.** `schema_check.py` and `fixture_audit.py` were run on all 72 fixtures, in process
  and from the command line (outputs above). They find no refusal and no unknown shape (71 Live
  Sets, 0 refused, 0 contradicted, 0 not isolating). Every slot count equals the freeze count and
  the scene count. The only schema deviation is MNS-013's `Foo`, the element that case tests.
  MNS-012 fails to parse only at its repeated attribute. Each carried fixture's tree equals the
  audit's repaired copy, which used exactly the two listed additions.
- **Model.** The cross-check model agrees with all 72 expectations, outcome and saved notes. It
  shares the same evidence and is not an oracle.
- **X agreement.** All five new expectations equal the X records they cite, input bits included.
  The 12 corroborated carried cases agree.
- **Mutations.** Eleven mutated expectations were each detected: v1's six by the model, and one
  per new case by both the model and the X check.
- **Probes.** 22 excluded or unresolved inputs got no saved expectation from the model. They are
  v1's list without the now-released rounding to −0, plus −0 in `VelocityDeviation`, an event
  `Value`, a curve control and a `TimeOffset`, and a `Time` of 1,000,000.
- **Package.** 72 distinct single-member gzip fixtures with the v1 header, UTF-8, LF endings and a
  final newline. Hashes and sizes of the 76 listed files match. The inventory equals the
  directory, all case inputs exist, and there are no symlinks. All 11 Markdown links (README 5,
  spec 6) resolve inside the package.
- **Deny list.** v1's list plus transport-state-v2's harness, library and instruction patterns,
  plus the structure-spec terms (T11, LSS-, audit, pointee, validation walk, Q-02x, A4 to A7).
  Whitespace is normalized and SHA-256 digests are skipped. There are no hits beyond the
  provenance wording, v1's forbidden-inputs line in `AGENTS.md` and one carried v1 sentence.
- **Export.** In `/tmp/claude-1000/-home-ollie-Documents-sound/5c433942-c5e3-420d-833a-756602393383/scratchpad/export-mns2/midi-note-storage-v2/`,
  `verify` passed everything above. `sha256sum -c` matched all 76 files, and the copy is
  byte-identical to staging.
- **Evidence identity.** See F9.

Not checked: any reference or candidate execution, the arm64 slice at run time, Apple's `strtod`
and formatter, and whether the structure rules are complete for these fixtures (only the rules of
SPEC-LIVE-SET-STRUCTURE r1 were checked).

## Review gates still required

1. **Scope review** in a separate context. Check the five new cases one by one against the X
   records and the static open and save evidence. Rule on F1 to F8, especially the added
   requirement IDs, the narrowed negative-zero exclusion and the stated assumptions.
2. **Supersession and fixture check.** From `v1-to-v2-text.diff`, the carry check and the
   structure outputs, confirm that no v1 record or expectation changed and that each fixture
   changed only by the two additions. Confirm that the scene addition is required, not optional
   (Q-022), and rule on the absent `TrackGroupId`.
3. **Quality and sanitization.** The provenance definition must be intelligible without
   analysis. The payload must have no internal names, addresses, structure-spec references or
   analyst links, and the exclusions must agree between `spec.md` and the manifest.
4. **Evidence identity.** Re-hash the X2 and T11 runs (F9), and decide whether to re-run
   `sh run.sh` for x2-notes-launch-v1.
5. **Finalize.** Add `REVIEW.md`; set the manifest review fields, `release_status` and
   `release_date`; re-run `seal`; verify an isolated export; record the manifest hash in the
   catalog.
6. **Publish** only after approval. Copy the package unchanged to `handoff/midi-note-storage-v2/`.
   Add a catalog row superseding midi-note-storage-v1 and update the catalog's fixture-defect
   note. Then update the spec status, coverage, the specs index, Q-018, Q-022 and the log. Never
   edit midi-note-storage-v1.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate with 72 cases: 67 carried (records unchanged,
fixtures rebuilt on T11-MIN's rules) and 5 new, all of the new ones X-labelled. It covers partial
REQ-MIDI-NOTE-STORAGE-001 to 010, 013, 014 and 016. REQ-011 stays excluded, and 012, 015 and 017
unreleased. It is not published. midi-note-storage-v1 remains the current release in the
catalog, with its fixture defect noted there.
