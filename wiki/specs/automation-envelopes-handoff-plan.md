---
id: PLAN-AUTOMATION-ENVELOPES-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Automation envelopes handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [automation-envelopes-v1](../../handoff/automation-envelopes-v1/README.md),
approved with narrowing by a separate review agent
([review record](../../handoff/automation-envelopes-v1/REVIEW.md)); manifest SHA-256
`793c1d7d5432de529c21c628e7fa6c46eecb1fa9128a4da9db1d1dfc34378302`. The review cut
the 29 staged cases below to 21. The 8 value cases (022 to 029) rest on assumption
A1, whose per-target conversion is untraced, so REQ-004, 010 and 011 are
unreleased. REQ-005 keeps only one-event acceptance and REQ-006 only order and
later negative times. Case 021 was reworked so its first event equals the next.
Findings for the spec author: widen A1 to cover every Float value, not only
interior times; back the Bool and Enum claim with evidence (PRB-S6-04 plus a Pan
variant); reword AEN-003. The tables below describe the staged candidate.

## Decision and boundary

Stage a finite candidate, automation-envelopes-v1, from
[SPEC-AUTOMATION-ENVELOPES revision 1](automation-envelopes.md). It follows the
pattern and gates of the [als-container plan](als-container-handoff-plan.md),
the [transport-state plan](transport-state-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff). The scope is the D and S
part of REQ-AUTOMATION-ENVELOPES-001 to 012 whose expected values are exact.
Under [ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary)
every expectation is a static derivation, and nothing was executed.

Excluded are the inputs of
[Q-020](../questions.md#q-020-automation-envelope-load-robustness): dangling
targets, unsorted events, missing attributes and duplicate Ids. Also excluded
are evaluation before an envelope's first event, every U case and every value
that depends on the interpolation domain (PRB-S6-04) or on the value at a step
(PRB-S6-06). Float, Bool and Enum values are released only at event times,
after the last event and between two equal values. There they follow exactly
from the stored events at the stated times. They are not rendered output. The
spec's revision note proposes the same first handoff.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
reference or candidate execution has run, and no compatibility is claimed.

## Scope

| Requirement | Included | Excluded remainder |
| --- | --- | --- |
| 001 | Track and clip envelope lists; envelope shape; empty transform state | Stored transforms (U); `LoopSlot`, `ScrollerTimePreserver`; arrangement clip timelines; shipped-document statistics |
| 002 | PointeeId names the target Id; binding by Id, not position; the release's target relations | Dangling, wrong-kind and cross-track targets (Q-020, PRB-S6-02); two envelopes on one target; `LockEnvelope` meaning (U) |
| 003 | Event element by value kind; attribute types; stored units for four targets | Mismatched class (U); other targets; units beyond the four |
| 004 | Ids play no part in order or evaluation | Duplicate or missing Ids, missing `Time` or `Value` (Q-020, PRB-S6-07); saved Ids |
| 005 | Leading event is ordinary; one-event list accepted | Main-track tempo and meter envelopes (PRB-N1-07, REQ-TRANSPORT-STATE-012); writer rule (inferred) |
| 006 | Document order; steps as ordinary events around the step; later negative times | Unsorted events (Q-020, PRB-S6-03); three or more at one time |
| 007 | All S clauses except the timeline clause | Timeline clause (no case, finding F4); presentation (PRB-S6-01) |
| 008 | Attribute names; missing control 0.5; four 0.5 no curve; save omission and text | Curve shape and values (PRB-S6-04); controls on first, last or equal-value events |
| 009 | Controls satisfying K are kept | Reset of other controls and whether it runs (PRB-S6-05); M at its boundary |
| 010 | Rules 1, 2 (no step) and 3 equal values, track envelopes, t ≥ 0 | Interior values (A1, PRB-S6-04); steps (PRB-S6-06); range handling; clip time base; t < t0 (Q-020) |
| 011 | Times other than event times | Event times (PRB-S6-06); time-signature envelope; t < t0 |
| 012 | Load rules as released in transport-state-v1; save rule; refusal of rejected text | Hex, `inf`, `nan`, `Invalid`, `#` forms; `EnumEvent` forms left open by transport-state-v1; saved negative zero |
| 013 | None | All of it (U) |

K is the release's sufficient condition for M: both controls in [0, 1] and
either c1 ≤ c2 or c1² + c2² − c1·c2 − c1 ≤ −10⁻⁶. K implies M. Step 2 of M
covers the first form. For the second, the computed D is far below 2⁻⁵². No
expectation rests on M's threshold or root test.

### Case disposition

The candidate has 29 cases: 19 from the 20 gradable r1 cases (AEN-018 at t = 4
only) and 10 new ones. Release case *n* is AUTOMATION-ENVELOPES-*n*.

| r1 case | Release | Change |
| --- | --- | --- |
| AEN-001, 002 | Not released | Open shipped sets; their D parts are survey facts about shipped content (F3). One-event acceptance is new case 002 |
| AEN-003 | 001 | Saved `PointeeId` judged against the saved target Id, not literal 323 (F2) |
| AEN-004 to 009 | 003, 004, 005, 006, 008, 009 | Re-authored on the release template |
| AEN-010, 011 | 011, 012 | Re-authored without B1; positive control 010 added |
| AEN-012, 013 | 017, 018 | As written |
| AEN-015, 019, 021, 023, 025 | 022, 024, 025, 026, 027 | As written; rests on I1 (Float) and I2 |
| AEN-018 | 023 | t = 4 only; t = 0 is U |
| AEN-026, 027 | 016, 013 | As written |
| AEN-014, 016, 017, 020, 022, 024 | Not released | U (PRB-S6-04, 05, 06) |
| AEN-028 to 031 | Not released | U, Q-020 (PRB-S6-03, 07) |

New cases and the clause each exercises: 002 (one event at L, REQ-007), 007
(`-6.3072e7`, numeric comparison), 010 (clip envelope that opens), 014 and 015
(`BoolEvent` and `EnumEvent` text refusal), 019 (missing control reads 0.5),
020 (four 0.5 controls written as none), 021 (Bool and integer save text), 028
(Ids out of document order) and 029 (binding by Id, not position).

## Findings while staging

Proposed corrections for a spec revision 2. This page does not edit the spec.

- **F1.** A1's scope is understated. The A1 row says only interior-time values
  rest on it, and AEN-015, 019, 021 and AEN-018 at t = 4 are graded S (A2). The
  appendix row "010 domain" and the evaluator disassembly (`0x1024095b4`, s6-0001)
  show that the event-time, end-of-list and equal-value branches also pass
  their result through the per-target conversion (`0x101574bb0`). Those values
  are exact only if that conversion returns in-range stored values unchanged.
  The release states this as an assumption (I1) and in the contract. Proposed:
  widen A1, or add an assumption for these cases. PRB-S6-04 with a Pan variant
  would settle both.
- **F2.** AEN-003 expects the saved `PointeeId` to be `323`. Whether a save keeps
  or renumbers target Ids is not traced. REQ-004 leaves event Ids U and is
  silent on target Ids. The release judges only that the saved `PointeeId`
  equals the saved target's Id (I5). Proposed: reword AEN-003.
- **F3.** AEN-001 and AEN-002 mix survey facts about shipped files (envelope and
  curve counts, one-event values) with an S claim that the file opens. The D
  part is not a behavior, and a shipped file cannot be a shareable fixture.
  Proposed: keep the counts in the research page and make "opens" a
  reference-comparison obligation.
- **F4.** REQ-007's S clause, that the check skips arrangement clip timelines,
  has no case. The release excludes timelines. Proposed: an r2 case with an
  empty `ClipTimeable/ArrangerAutomation/Events` in a minimal set.

## Deliverables

- Payload:
  [automation-envelopes-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v1/README.md),
  `AGENTS.md`, `spec.md` (contract and comparison convention), `cases.json`
  (29 cases), `fixtures/` (29 XML files) and a draft `manifest.json`
  (`release_status: candidate-unreviewed`, review pending). The manifest lists
  33 payload files, 34 with itself. Draft manifest SHA-256:
  `573532d84a48eb5a3c9d27111e5fb472870f2c85d4ed1557b956e9264943aedb`. Review
  edits will change it.
- Analyst side, never shipped: `automation-envelopes-v1-analysis/` with
  [build_aen.py](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v1-analysis/build_aen.py)
  (fixtures, cases, manifest, seal and verify),
  [crosscheck_model.py](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v1-analysis/crosscheck_model.py),
  [trace_aen.py](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v1-analysis/trace_aen.py),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v1-analysis/traceability.json)
  and [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v1-analysis/author-validation.json).

## Evidence traceability

Evidence is the [S6 run](../../analysis/ableton-live-12.4.3/r2/s6-automation-v1/manifest.json)
(`Live.arm64` `3a99ceea…d1c383cfad`; dossiers s6-0001 to s6-0003;
`documents-survey.json`, `schema-survey.json`, `curve-check.json`). The text
rules come from the [N1 run](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/manifest.json)
in the wording released and reviewed as transport-state-v1. The analyst re-read
the evaluator, validation, monotone test, curve hook and save predicate dossiers
on 2026-10-18 before inclusion. `traceability.json` holds per-case locators,
and the payload contains none of them.

| Release cases | Clauses | Kept evidence | Inferred links |
| --- | --- | --- | --- |
| 001, 016, 021 | 001–003, 012 save | survey containers, target relations, event classes; N1 `number-format-check.txt`; generic writer | I3 (021), I4, I5 |
| 002–009, 011–013 | 007, 012 load | `0x102561a28` disassembly (empty list; `fcmp` with L; `fcmp d0,#0.0`); envelope hooks `0x1024050d8`, `0x10245194c`; walk `0x101486fe4`, `0x101487198` | I4 |
| 010 | 001, 002, 007 | as above; shipped clip-envelope shape | I4 |
| 014, 015 | 003, 012 | N1 `0x10152bfb8` Boolean branch, `0x1002fd908` integer rule; event constructors | I3, I4 |
| 017–020 | 008, 009 | `0x102778828` (`== 0.5` per control); `0x1027785a0` (defaults 0.5); `0x102778870`, `0x1012132d8`; `curve-check.json` | I4, I5 |
| 022–025, 028 | 004–006, 010 | `0x1024095b4` branches (end of list, event time, equal values before curve); searches `0x102565974`, `0x102565a48` | I1, I2, I6 |
| 026, 027 | 011 | `0x10240a84c`, `0x102565e10` | I2, I3, I6 |
| 029 | 002, 010, 011 | lookup by Id `0x101535e0c`; both evaluators | I1, I2, I3, I6 |

| Link | Inference not established by kept evidence | Affects |
| --- | --- | --- |
| I1 | The per-target conversion returns in-range stored values unchanged. The curve branch clamps to the same range (`0x102404218`), which suggests a range operation. Bool and Enum use no conversion | Float value cases (F1) |
| I2 | Spec A2: after open, with automation active and no override, the parameter follows E(t). `Manual` precedence is U (REQ-013) | Reference observation of value cases; the contract makes a non-following parameter inconclusive |
| I3 | `BoolEvent` and `EnumEvent` values are Bool and Int members read with the Boolean and integer rules. Their registries were not re-read; the constructors set false and INT_MIN | 014, 015, 021, 026, 027, 029 |
| I4 | Opening a Live Set reaches the validation walk. The walk's caller `0x101484108` is the general XML reader; document kinds per caller are untraced in S6 | Every case |
| I5 | Save keeps each envelope bound to its target; Id handling on save is untraced | Save cases |
| I6 | Track envelope time is song time in beats (inferred from shipped sets) | Reference observation of value cases |

## Fixture construction and sanitization

`build_aen.py build` writes all 29 fixtures from one template written for this
release, and no shipped file is read. The template has the declaration, a root
with `MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1"` and
no `Creator` or `Revision`, and `NextPointeeId` 40. It holds an audio track with
`Speaker`, `Pan` and `CrossFadeState` targets (invented Ids 21 to 23) and a MIDI
track with a session MIDI clip and `ControllerTargets.6` (Id 31). Each case
adds only its envelopes. B0, B1 and B2 are replaced: the event lists of the
released r1 cases are carried over unchanged, and the B1 clip envelope is
rebuilt in the template's clip. The payload names public document elements and one schema identifier.
It holds no shipped content, recovered message text, internal names, addresses,
probe, question or r1 case IDs, or analyst links.

## Mechanical checks performed

`build_aen.py seal` (CPython 3.13.9 `-I`) wrote the author validation:

- The cross-check model agrees with all 29 expectations. A mutated expectation
  was detected for each of the 29 cases. Fifteen probes of excluded inputs give
  no expectation, among them a dangling target, unsorted events, duplicate Ids,
  interior, step and curved values, and evaluation before a first event at 0.
  The model shares the static evidence and is not an oracle.
- Fixtures are ASCII with LF endings and a final newline. Two pairs are
  identical by design (001 and 022, 017 and 025), and the contract states this.
- Evidence identity: all 79 files of the S6 manifest and the `Live.arm64`
  digest matched on 2026-10-18.
- Hashes and sizes of the 33 listed files match, and the inventory equals the
  directory. The deny list covers analyst paths, addresses, internal class and
  member names, recovered messages, tool names, probe, question, r1 case and
  event-list IDs, assumption labels, shipped file names and absolute paths. It
  has no hit. A copy with planted terms was flagged.
- A copy in the session scratchpad, outside the checkout, passed `verify`: all
  33 hashes, all 8 Markdown links inside the package, all case inputs. An
  independent re-hash matched, and the copy is byte-identical to staging.

Not checked: any reference or candidate execution, and any proof of I1 to I6.

## Review gates still required

1. **Scope review** in a separate context. Check every included clause and all
   29 expectations against the locators. Rule on I1 to I6 and F1 to F4, the 10
   new cases, the K narrowing of REQ-009, and the rule that makes a parameter
   not following its envelope inconclusive.
2. **Quality and sanitization review**: behavioral completeness and the
   comparison convention, with exclusions in both spec and manifest. Confirm no
   internal structure or analyst link remains and nothing claims more than
   static derivation.
3. **Evidence identity**: re-check the S6 manifest and image digest.
4. **Fixture and sharing review** of the 29 authored fixtures.
5. **Finalize**: add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the handoff catalog.
6. **Publish** only after approval: copy unchanged to
   `handoff/automation-envelopes-v1/`, then update the catalog, spec status,
   coverage, indexes and log. Q-020 stays open.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate: 29 cases, partial
REQ-AUTOMATION-ENVELOPES-001 to 012, with 013 unreleased. It is not published,
and no handoff exists for SPEC-AUTOMATION-ENVELOPES. This page has no inbound
catalog link yet; the staging task did not edit the spec index.
