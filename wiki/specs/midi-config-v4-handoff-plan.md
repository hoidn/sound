---
id: PLAN-MIDI-CONFIG-V4-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Fourth MIDI configuration handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [midi-config-v4](../../handoff/midi-config-v4/README.md), approved with one narrowing (RV4-01) and clarifications RV4-02 to 05 by a separate review agent ([review record](../../handoff/midi-config-v4/REVIEW.md)). All 161 cases are kept: the 127 v3 cases carried byte-identical, plus 34 new cases that match the original code on re-run within 5e-10.

- **RV4-01:** a stepped value within 8τ of a half-integer has no expectation.
- **Relative messages:** after k relative messages in a row, the value is compared within k×τ. A 200-message re-run drifted 5.2τ.
- **Superset wording:** "strict superset" now reads "superset with two precision corrections".
- **Ruling:** the 8τ band stands, and Value Scaling moves stay excluded.

For the spec author (revision 6): the 3.8τ figure for the Value Scaling move error should read 96 to 408τ. Carry both precision corrections into the spec.

## Decision and boundary

Stage a fourth finite candidate, midi-config-v4, from
[revision 5 of the MIDI specification](midi-user-mapping.md). It follows the
structure and gates of the [midi-config-v3 plan](midi-config-v3-handoff-plan.md),
the [transport-state-v2 plan](transport-state-v2-handoff-plan.md) (a release with
extracted-execution cases), the [als-container plan](als-container-handoff-plan.md)
and the [release workflow](../workflows.md#release-a-handoff).

Why a new release: revision 5 settles, by
[extracted execution](../research/midi-transforms-native.md#extracted-execution-results-x2-2026-10-18)
(label X, [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code))
and a static trace (E15), the clauses that
[midi-config-v3](../../handoff/midi-config-v3/README.md) excluded: Pick-Up and
Value Scaling takeover, takeover with a reversed range, the previous value of a
14-bit pair (the first pair included) and a range-scaled value tolerance.
Revision 5 corrected no expected value of a v3 case. Released payloads are
immutable, so v4 carries all 127 v3 cases unchanged and adds the new clauses and
their exact cases. When published it supersedes midi-config-v3 as a strict
superset; v3 stays valid for its narrower scope.

New cases carry the provenance "extracted execution of the original x86_64 code
(glibc substitutions); arm64 equivalence inferred". Carried cases keep
"static-derived; not observed reference output", although X agrees with all 18
v3 value cases (`traceability.json` records the corroboration, as transport-state-v2
did for its carried cases). The interpreted assignments, the previous-value
bookkeeping (E10) and the entry-to-choice mapping (E15) stay static-derived in
every case. No reference application or candidate has run, and no compatibility
is claimed.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. Nothing has
been written into `handoff/`.

## Scope

Selection rule: release only D, S and X clauses with exact values. Exclude S-cond
clauses, runtime and timing, and anything resting on an open item of
[Q-009](../questions.md#q-009-midi-numerical-modes-timing-and-feedback)
(PRB-N7-01, 04, 05; the preference default).

| Requirement | Included in v4 | Excluded remainder |
| --- | --- | --- |
| 001, 004 | None | As in v3 |
| 002, 003, 006–009, 011–013 | v3 clauses, unchanged | As in v3 |
| 005 | v3 clauses. New: three choices `none`, `pick-up`, `value-scaling` by entry position (S, E15); Pick-Up and Value Scaling (X): previous data values per input, channel and number, empty on open and otherwise never emptied (S, E10, E15), the four-case pair previous value, *p* formed and rounded like *n*, the −129 test, sorted bounds, inclusive tests, clamping, unrounded move; reversed ranges for Absolute, 14-bit and relative (S, rev 4) and takeover (X); τ = max(1e-6, 2⁻²² × max(\|min\|, \|max\|)) | On/off parameters (S-cond, PRB-N7-04); the default choice; displayed wording of the entries; ordering, coalescing, deferral (PRB-N7-05); displayed values and post-set processing (PRB-N7-01); kind membership (PRB-N7-04); unknown tokens (PRB-S4-04); several assignments on one address; *min* = *max*; stepped non-integer bounds; tests within 8τ of a bound and Value Scaling moves outside the listed cases (findings F1, F2) |
| 010 | v3 clauses; crossfader `Absolute14Bit` pairs subject to takeover (S, E11; X, MT-45) | Reported ranges and kinds of the three parameters (PRB-N7-01) |

### Case disposition

| Revision 5 row | Candidate | Note |
| --- | --- | --- |
| MT-01 to 16, 22, 23 | MIDI-CONFIG-110 to 127, carried | Records and fixture bytes identical to v3. X agrees within 1e-6, and the v4 rules reproduce them under every named choice |
| MT-19 to 21 | MIDI-CONFIG-128 to 130 | X (were S-cond in revision 4); values from `results/mt.json` |
| MT-24 to 42 | MIDI-CONFIG-131 to 149 | X; values from `acceptance-cases-x2.json` (TK runs) |
| MT-45, 46 | MIDI-CONFIG-150, 151 | X; 150 is the crossfader pair (fixture `CrossfaderSlider`, `Absolute14Bit`) |
| MT-47 to 56 | MIDI-CONFIG-152 to 161 | X boundary cases (TB runs), listed as exceptions to the near-bound exclusion |
| MT-17, 18, 43, 44 | Not released | S-cond: on/off thresholds (PRB-N7-04) |

The task named "MT-17 to 21 (now X)". Revision 5 labels only MT-19 to 21 X;
MT-17 and 18 stay S-cond and are excluded with MT-43 and 44. Takeover fields
are the setting X ran (`pick-up`, `value-scaling` or `none` for MT-46).
Expected values are the X binary32 results rounded to nine decimals. Each new
comparator states its τ: 1e-6 for ranges 0–1, 0–3, 1–0 and 3 to −1,
3.0279e-5 for 0–127, 3.0756e-5 for −129–0 and 2.3818e-4 for 20–999.

## Findings while staging

Proposed for a spec revision 6. This page does not edit the spec.

- **F1 (spec imprecision, Value Scaling precision).** Revision 5 states the rules
  in exact arithmetic and compares within τ. It notes that Value Scaling
  magnifies the *cross-slice* difference (up to 18τ for lo ≠ 0) and puts its
  Value Scaling cases at lo = 0. It does not say that the original's binary32
  move can lie farther than τ from the exact formula even at lo = 0.
  [precision-model.txt](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v4-analysis/precision-model.txt)
  shows up to 3.8τ for 14-bit pairs on 0–1 and 3.3τ on 0–3 (c = 0, previous
  and new targets close to max). It uses the binary32 operation-order model of
  `run_x2.py` (`models`, `vs32`), not X. The candidate excludes Value Scaling
  moves outside the ten cases that state one: 129, 133, 137, 138, 143 to 145,
  153, 155 and 161. All have lo = 0 and lie within 0.16τ of the exact rule.
- **F2 (spec imprecision, bounds).** Revision 5 makes every bound inclusive in
  exact arithmetic and says a comparison near its bound can differ between
  slices. It does not exclude near-bound inputs when lo = 0, where binary32 and
  exact arithmetic can also disagree. The model finds 59 of 1,143 current values
  within four binary32 steps of the in-sync bound on 0–1 decided differently,
  some at the step nearest the bound; 0–127, where every target is an integer,
  has none. The candidate excludes any takeover test whose two sides lie within
  8τ, except *p* = *n* for one data value, and lists cases 149 and 152 to 161 as
  exceptions. All other new cases are at least 1,900τ from every bound
  (`author-validation.json`). The factor 8 is an author choice: about twice the
  rounding of the compared quantities, far above the one-step flips observed.
- **F3 (point for the reviewer).** The −129 test (case 149) and the four-case
  pair previous value (cases 141 to 146, 150) state the original's no-value
  marker arithmetic as behavior. They are observable, X-confirmed and exact, so
  they are kept, worded without the marker. Removing them would drop case 149
  and the first-pair rule.
- **F4 (catalog, not spec).** The [handoff catalog](../../handoff/index.md) row
  for midi-config-v3 says "from incoming CC, pitch-bend and 14-bit values".
  midi-config-v3 has no pitch-bend clause. It is not edited here.

No S clause or expected value of revision 5 was found wrong. All 34 X rows agree
with the exact restatement within 0.16τ and with the revision 5 table within τ.

## Deliverables

- Payload: [midi-config-v4/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v4/README.md)
  (scope, supersession, 11-item change list), `AGENTS.md`, `spec.md` (v3 contract
  plus takeover, reversed ranges, previous values, τ, precision exclusions and
  the two provenance labels with three stated assumptions), `cases.json` (161
  cases) and `fixtures/` (161 files). The draft `manifest.json` has
  `release_status: candidate-unreviewed`, review pending, `supersedes:
  midi-config-v3`, the superseded manifest digest `2e7d9376…ff40458`,
  `corrected_expectations: none`, the change list, the provenance labels,
  `value_tolerance` and the stated assumptions. It lists 165 payload files;
  with itself the package has 166. Draft manifest SHA-256:
  `fc247f3c63ade7dfb14de394e464b6771ac1ef3cafb76646f1f4926481213886`. Review
  edits will change it.
- Analyst side, never shipped: `midi-config-v4-analysis/` with
  - [build_v4.py](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v4-analysis/build_v4.py):
    fixtures, cases and manifest. It imports `build_v3.py` unchanged and takes
    each new value from the X2 results and each message list from the
    revision 5 table. It also holds the exact restatement `model4`.
  - [seal_v4.py](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v4-analysis/seal_v4.py):
    the checks, seal and verify.
  - [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v4-analysis/traceability.json):
    every case and clause to its evidence and inferences.
  - [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v4-analysis/author-validation.json)
    and [v3-to-v4-text.diff](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v4-analysis/v3-to-v4-text.diff).
  - [precision_model.py](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v4-analysis/precision_model.py)
    and its output `precision-model.txt` (F1, F2).

## Evidence traceability

Evidence is the X2 packet [x2-midi-v1](../../analysis/ableton-live-12.4.3/r2/x2-midi-v1/manifest.json)
(manifest SHA-256 `da19636d…0c88c`; all 15 listed files re-hashed on 2026-10-18
and matched). The slice `Live_x86_64.x86_64` (`1bae9a97…be999b0`), the built
loader (`5d236b76…d5385`) and `tools/xexec` were also re-hashed and match. The
E10 to E16 labels are those of the spec appendix, and v3's evidence covers
cases 001 to 127. Per-case X locators are in `traceability.json`; the payload
contains none of them.

| v4 cases | Source | Kept evidence | Inferred links |
| --- | --- | --- | --- |
| 001–127 | midi-config-v3, same IDs; records and fixture bytes identical | v3 review and traceability; X corroborates 110–127 (`results/mt.json`) | As in v3 |
| 128–130 | MT-19 to 21 | E16 `results/mt.json`; E14, E15 choice | I2–I4, I6–I8 |
| 131–140 | MT-24 to 33 | E16 TK-02, 03, 05–12; E12 reversed flag | I2–I4, I6–I8 |
| 141–146, 150 | MT-34 to 39, 45 | E16 TK-13 to 19, 29; E11 pairing and missing-half value, crossfader pair without the opt-out | I2–I4, I6–I8 |
| 147–149 | MT-40 to 42 | E16 TK-22, 23, 25; E13 kinds | I2–I4, I6–I8 |
| 151 | MT-46 | E16 TK-30; tolerance runs | I3, I4, I6 |
| 152–161 | MT-47 to 56 | E16 TB-01 to 10 | I2–I4, I6–I8 |

| Link | Inference not established by kept evidence | Affects |
| --- | --- | --- |
| I1 | The entries display as None, Pick-Up, Value Scaling; the entry-to-choice mapping itself is S (E15) | Reference labels only; stated assumption |
| I2–I5 | As in v3: installed map mode, setter stores unchanged, one application per message in order, `Layer` wiring | Every value case; preconditions as in v3 |
| I6 | arm64 equivalence from the static slice comparison (E16); one differing fused operation, bounded by τ | Cases 128–161; stated assumption |
| I7 | The application passes the previous data value as the static dispatcher reading gives it (E10); X2 supplied it | Every takeover case; stated assumption |
| I8 | X2 built the parameter details and simulated the parameter; which real parameter has which kind is excluded | Every new case; covered by the preconditions |

## Mechanical checks performed

`build_v4.py build`, then `seal_v4.py seal`, were run with CPython 3.11.13 `-I`
and wrote the author validation. A second build and seal reproduced the draft
manifest digest and the analysis outputs byte for byte. No cache was written
into the v2 or v3 analysis directories.

- **Carry.** The first 127 case records equal midi-config-v3's, and the fixture
  bytes are identical. The representation changes only `stimulus` and `values`.
  `v3-to-v4-text.diff` lists every changed v3 line: title, status and release
  lines; the provenance paragraph; target parameter, Absolute, 14-bit and
  relative sentences; the takeover paragraph and its assumption; starting
  state; the value-case table and tolerance; two exclusion paragraphs; the
  comparison obligation; the change and provenance sections. The v4 rules
  reproduce the 18 v3 value cases within 1e-6 under their own choice, and the
  `any` cases under all three choices.
- **Fixtures.** All 161 are ASCII with LF endings and a final newline, parse in
  the host 3.11.13 parser, and agree with the v2 cross-check model.
- **Values.** Every new value equals its X result within 5e-10 (rounding). It
  agrees with the exact restatement within τ (largest 0.154τ, case 161) and with
  the revision 5 table within τ. Messages equal both the table and X. The
  takeover in each case matches the table condition. The near-bound set and the
  move set computed by the restatement equal the payload's exception lists.
  Raising all values of any one new case by 2τ is caught by both checks (34/34).
- **Rules.** The four-case pair previous value equals the bitwise form for all
  16,641 combinations of missing and present halves. Cases 126 and 150,
  rescaled to crossfader ranges −1..1, 0..2, −5..3 and 1..−1, give the rescaled
  values exactly, which supports the comparison obligation. The restatement gives
  no expectation for on/off, *min* = *max*, a stepped non-integer value, a
  value outside the range, or `any` on a value subject to takeover. The decode
  rows equal the parent spec's.
- **Selection.** The released rows equal the revision 5 X rows, and the
  excluded rows equal its S-cond rows.
- **Package.** The hashes and sizes of all 165 listed files match, and the
  inventory equals the directory. All 26 Markdown links (README 5, spec 21)
  resolve inside the package, and every case input exists. The deny-list is v3's
  list without `-129`, which is now a released value, plus X2 harness, function,
  string-key and finding-ID patterns. It has no hit. A planted copy was flagged.
- **Export.** `seal_v4.py verify` of a copy in the session scratchpad matched all
  of the above. The copy is byte-identical to staging.

Not checked: reference or candidate execution, the arm64 slice at run time,
any proof of I1 to I8, and an independent restatement. The restatement, the
table and the X results share one evidence chain; none is an oracle.

## Review gates still required

1. **Scope review** in a separate context. Read the 34 new cases one by one
   against the X2 results and E11 to E16. Rule on F1 and F2, including the
   exception lists and the 8τ band, and on F3. Confirm that the provenance
   label and its definition are intelligible without analysis.
2. **Strict superset.** From the diff and the carry checks, confirm that no v3
   case, fixture or expected value changed and no v3 statement is contradicted.
   The *min* < *max*, `none`-only and 1e-6 statements are widened, not
   reversed.
3. **Quality and sanitization.** Check behavioral completeness, and that the
   exclusions agree between spec and manifest. There must be no internal names,
   addresses or analyst links, and no claim beyond static derivation and X.
4. **Evidence identity.** The X2 files, slice and loader matched on 2026-10-18.
   Decide whether to re-run `sh run.sh` before release.
5. **Fixture and sharing review** of the 34 new fixtures, which are short
   authored files with public key names.
6. **Finalize.** Add `REVIEW.md`. Set the manifest review fields,
   `release_status` and `release_date`. Re-run `seal_v4.py seal`, verify an
   isolated export and record the manifest hash in the handoff catalog.
7. **Publish** only after approval. Copy the package unchanged to
   `handoff/midi-config-v4/` and add a catalog row superseding midi-config-v3.
   Update the spec status, coverage, indexes (including an entry for this
   page), Q-009 and the log. Carry F1 and F2 into a spec revision. Never edit
   midi-config-v3.
8. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate with 161 cases: 127 carried and
34 new, all X-labelled. It covers partial REQ-MIDI-USER-002, 003 and 005 to 013;
001 and 004 remain unreleased. It is not published, and midi-config-v3 remains
the current MIDI release.
