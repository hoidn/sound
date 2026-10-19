---
id: PLAN-TRANSPORT-STATE-V2-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Second transport-state handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [transport-state-v2](../../handoff/transport-state-v2/README.md),
approved with listed clarifications RV2-01 to RV2-04 by a separate review agent
([review record](../../handoff/transport-state-v2/REVIEW.md)). Manifest SHA-256:
`398a88a62114552595830f99ba2fc1bc4d8c0e1f0d2ae65a70d21aa2324c17c8`. All 33 cases
are kept and none changed. The 18 carried cases and fixtures are byte-identical to v1.

The reviewer re-ran every new expectation. The 11 values where glibc's `log10`
is off all fall inside the excluded band of 1/4 to 3/4 of a spacing. No evidence
process exceeded 200 calls.

The clarifications are:
- **RV2-01:** the change list is completed.
- **RV2-02:** the logarithm-accuracy assumption is stated.
- **RV2-03:** the reading of `-0` and the exact save text are marked as
  depending on glibc.
- **RV2-04:** the definition of extracted execution is clarified.

Spec revision 4 applies RV2-02 and RV2-03.

## Decision and boundary

Stage a corrected candidate, transport-state-v2, from
[SPEC-TRANSPORT-STATE revision 3](transport-state.md). It follows the
[transport-state-v1 plan](transport-state-handoff-plan.md), the
[midi-config-v3 plan](midi-config-v3-handoff-plan.md) (a superseding release), the
[als-container plan](als-container-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff).

Why a new release: the released [transport-state-v1](../../handoff/transport-state-v1/README.md)
states REQ-011 step 1 with the exact logarithm. The original program takes k from
the binary64 `log10` result. That gives different texts next to powers of ten, as
the [X1 pilot](../research/extracted-execution.md#findings-beyond-the-released-cases)
found and [X2](../research/transport-state-native.md#extracted-execution-results-x2-2026-10-18)
measured. v1 excluded those values (log10 within 1e-12 of an integer), so no v1
case is wrong. But its rule is exact only within v1's scope, and released payloads
are immutable. v2 carries every v1 clause and case. It replaces step 1 with the
exact rule and adds the clauses that revision 3 settled by extracted execution.

Under [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code),
the new cases carry the provenance "extracted execution (x86_64 slice, glibc
substitutions); arm64 equivalence inferred". Opening and saving stay
static-derived. No reference application or candidate has run, and no
compatibility is claimed.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. Nothing has
been written into `handoff/`.

## Scope

Selection rule: release only documented, static-derived or X clauses with exact
values. Exclude U clauses, clauses that rest on a substituted library at an
uncertain point, values outside the v1 ranges (REQ-009) and runtime behavior.

| Requirement | Included in v2 | Excluded remainder |
| --- | --- | --- |
| 001, 002, 007, 008 | v1 clauses, unchanged | As in v1 |
| 003 | v1 clauses, unchanged (X also agrees) | None |
| 004 | v1 decimal-prefix rule. New: `#` and 16 hex digits of either case, most significant first; other `#` text refused; `-0` reads as −0 | `Invalid` (largest finite, out of range), `0x`, `inf`, `nan`, non-space white space (glibc `strtod` only), locale |
| 005 | v1 clause. New: `#` and 8 hex digits | Overflow to +∞ (out of range) |
| 006 | Five-condition rule (X): ASCII; body `-`? digits ≤ 63 characters; no `+-`; no trailing spaces after leading spaces or `+`; int32 range | Accepted codes outside 0–494 (REQ-009) |
| 009, 012 | None | All |
| 010 | v1 definitional clause, unchanged | Meter texts and decoder (not document observables; display surface U) |
| 011 | Step 1 with L, the binary64 logarithm (X). Positive and negative zero. v1 examples plus four near powers of ten | L within 1/4–3/4 of a binary64 gap from an integer (glibc not correctly rounded near 1/2; Apple's `log10` not run). `Invalid` and `#` output and the most negative value (out of range). Ties keep v1's ties-to-even clause, with no case on a tie |

### Case disposition

| Draft case | Candidate | Note |
| --- | --- | --- |
| TS-001–009, 011–016, 020–022 | Carried | Records and fixture bytes identical to v1. X corroborates TS-001–009, 020 and 021 (`traceability.json`); records unchanged |
| TS-010 | New, refused | Was excluded from v1; X refused ` +201 ` |
| TS-024–027 | New, saved text | REQ-011 step 1 next to 10², 10³, 10⁻¹ and 10⁻⁶; logarithm offsets 0.14, 0.11, 0.16 and 0.02 gaps |
| TS-028 | New, saved `-0` | Negative zero; the state key is not judged, because equality ignores the sign |
| TS-029–033 | New | REQ-006: `+201 ` refused, `-0` opens, `2147483648` refused, 63-character body plus a space opens, `-` plus 63 digits refused |
| TS-034–037 | New | REQ-004/005: ` +4.5 ` opens, `- 4.5` refused, `#4012000000000000` is 4.5, `#42f00000` is 120 |
| TS-017–019 | Not released | REQ-009 |
| TS-023 | Not released | Withdrawn in revision 2 |

The new fixtures use the v1 generator unchanged. For refused time-signature cases,
the comparison obligation keeps the automation event at `201`, as for TS-009.

## Findings while staging

No error was found in revision 3. Points for the reviewer:

- **F1, relationship.** v2 is a superset of v1 in effect, not in text. The REQ-011
  step 1 sentence changes, but within v1's scope (logarithm farther than 1e-12
  from an integer) the old and new rules give the same k. The README and manifest
  say so.
- **F2, ties.** Revision 3 labels ties to even as X with glibc and as inferred for
  Apple's formatter. v1 released that clause as an accepted inference. v2 keeps
  the clause and states the assumption; no case lies on a tie.
- **F3, assumptions.** Three stated assumptions, in `spec.md` and the manifest:
  - arm64 equivalence, for all 15 new cases;
  - a reference `log10` error below 0.8 gap, for TS-024 to TS-027;
  - the C-standard number grammar, for TS-034 and TS-035.
  If the reviewer rejects the second or third, remove the cases that depend on it.
- **F4, carried records.** The carried records keep the static-derived label,
  although X now agrees with 11 of them. Relabelling would change v1 records;
  `traceability.json` records the corroboration instead.

## Deliverables

- Payload: [transport-state-v2/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v2/README.md)
  (scope, supersession, change list), `AGENTS.md`, `spec.md`, `cases.json` (33
  cases), `fixtures/` (33 files) and a draft `manifest.json`. The manifest has
  review pending, `supersedes: transport-state-v1` with the superseded manifest
  digest `b2fdf029…5baba`, the change list, the provenance labels and the stated
  assumptions. It lists 37 payload files; with itself the package has 38. Draft
  manifest SHA-256: `8fa73f29a3b05b91db7ed036da05b79a2eeba77d347c422782e4a49dd58c9592`.
  Review edits will change it.
- Analyst side, never shipped: `transport-state-v2-analysis/` with
  [build_v2.py](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v2-analysis/build_v2.py),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v2-analysis/traceability.json),
  [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v2-analysis/author-validation.json)
  and [v1-to-v2-text.diff](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v2-analysis/v1-to-v2-text.diff).
  - `build_v2.py` makes the fixtures, cases and manifest, runs the cross-check model
    and the X agreement check, and seals and verifies the package. It imports the
    v1 generator and judge unchanged.
  - `traceability.json` maps every case and new clause to its X or static evidence.

## Evidence traceability

| v2 cases | Evidence | Residual inference |
| --- | --- | --- |
| Carried 18 | v1 [traceability](transport-state-handoff-plan.md#evidence-traceability) and [review](../../handoff/transport-state-v1/REVIEW.md) | As in v1 |
| TS-010, 029–033 | [x2-transport-v1](../../analysis/ableton-live-12.4.3/r2/x2-transport-v1/manifest.json) `results/parse.json`: the x86 integer parser and the converter. No library is substituted on this path (`from_chars` is in the slice). The arm64 window and limit are identical (n1-0006) | arm64 equivalence; the open/refuse step (S, as v1) |
| TS-024–027 | `results/writer.json`: the attribute writers on the case values, and the 6,539-value sweep (correctly rounded L model 6,528/6,539, glibc model 6,539/6,539); `parse.json` for the decimal reading | Apple's `log10` within 0.8 gap at offsets ≤ 0.17; save path S |
| TS-028 | `parse.json` `-0` → bits `8000000000000000`; `writer.json` specials `-0.0` → `-0` (both writers) | arm64 zero test (static: `fcmp d0,#0.0` is true for −0) |
| TS-034, 035 | `parse.json` ` +4.5 ` → 4.5, `- 4.5` refused; glibc `strtod` through the original consumption check | Apple `strtod` grammar in the C locale |
| TS-036, 037 | `parse.json`: the `#` branches. No library is substituted; the hex mask is the same in both slices | arm64 equivalence |

`build_v2.py seal` checks each new expectation against those X records.

## Mechanical checks performed

`python3 -I build_v2.py build` then `seal`, run with CPython 3.13.9 `-I`, wrote
the author validation. A second build and seal reproduced the same draft manifest
digest.

- **Carry.** All 18 v1 records are equal to v1's `cases.json` and their fixtures are
  byte-identical. The v1 generator also reproduces each v1 fixture byte for byte.
- **Model.** The cross-check model of the v2 clauses agrees with all 33
  expectations, and no fixture hits an exclusion. Fixtures are ASCII with LF
  endings and no tabs, and none duplicates another.
- **X agreement.** All 15 new expectations equal the X results they cite. The 11
  carried cases with X records also agree. Each of the 15 new cases, with one
  expectation changed, is caught by both the model and the X check (15/15).
- **Package.** The hashes and sizes of the 37 files match, and the inventory equals
  the directory. All 10 Markdown links (README 5, spec 5) resolve inside the
  package, and every case input exists.
- **Deny list.** It covers the v1 list plus harness, library-function,
  instruction, address and evidence-ID patterns. It has no hit. The only allowed
  wording is the provenance label and its definition: x86_64 build or host, glibc,
  macOS arm64 build.
- **Export.** `verify` of a copy in the session scratchpad matched everything
  above, and the copy is byte-identical to staging.

Not checked: reference or candidate execution, the arm64 slice at run time, and
Apple's `log10`, `strtod` and formatter.

## Review gates still required

1. **Scope review** in a separate context. Read the 15 new cases one by one
   against the X results and the static open/save evidence. Rule on F1 to F4,
   especially the stated assumptions.
2. **Superset check.** From `v1-to-v2-text.diff` and the carry checks, confirm
   that no v1 case or fixture changed. Confirm that the REQ-011 step 1 change is
   equivalent within v1's scope.
3. **Quality and sanitization.** The provenance definition must be intelligible
   without analysis. Check that the payload has no internal names, addresses or
   analyst links, and that the exclusions agree between `spec.md` and the
   manifest.
4. **Evidence identity.** The X2 manifest pins the x86_64 slice
   (`1bae9a97…be999b0`) and the loader build. Decide whether to re-run
   `sh run.sh` before release.
5. **Finalize.** Add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated export;
   record the manifest hash in the handoff catalog.
6. **Publish** only after approval. Copy the package unchanged to
   `handoff/transport-state-v2/`, add a catalog row superseding
   transport-state-v1, and update the spec status, coverage, indexes, Q-012 and the
   log. Never edit transport-state-v1.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate with 33 cases: 18 carried and 15
new, all of the new ones X-labelled. It covers partial REQ-TRANSPORT-STATE-001 to
008, 010 and 011; 009 and 012 remain unreleased. It is not published.
transport-state-v1 remains the current transport release.
