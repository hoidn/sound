---
id: PLAN-AUTOMATION-ENVELOPES-V2-HANDOFF
type: research
status: current
updated: 2026-10-19
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Second automation-envelopes handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [automation-envelopes-v2](../../handoff/automation-envelopes-v2/README.md), approved with listed corrections by a separate review agent ([review record](../../handoff/automation-envelopes-v2/REVIEW.md)). It has 21 cases: 18 carried on repaired fixtures and 3 new.

The review confirmed a removal step in both builds that runs on open, before the checks:
- clip envelopes with exactly one event are removed;
- Speaker, Pan and CrossFadeState envelopes with fewer than two events are removed.

v1 cases 003, 004 and 011 were therefore wrong, and the change list says so. Case 012 stands. REQ-007 clause 5 now states the removal, and REQ-005 is restated. New assumption 5, that other envelopes are kept, carries 8 cases. No value is implied anywhere.

For the spec author:
- fix REQ-005 and REQ-007 in SPEC-AUTOMATION-ENVELOPES;
- fix REQ-014's open condition in SPEC-LIVE-SET-STRUCTURE;
- correct SF-3's unconfirmed status.

## Draft reconciliation (2026-10-19)

Applied SF-1 to SF-6 and review RA2-01 to 03 in draft r5. SF-3’s original
unconfirmed status below is superseded by the independent review: the discard
was confirmed in both builds. The timeline base is now v2 case 032. Ideal
segment values are not a comparison for ramped samples. No release changed.

## Decision and boundary

Stage a corrective candidate, automation-envelopes-v2, from
[SPEC-AUTOMATION-ENVELOPES revision 4](automation-envelopes.md). It follows the
[automation-envelopes-v1 plan](automation-envelopes-handoff-plan.md), the
[transport-state-v2 plan](transport-state-v2-handoff-plan.md) (a superseding release),
the [als-container plan](als-container-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff).

Why a new release: all 21 fixtures of the released
[automation-envelopes-v1](../../handoff/automation-envelopes-v1/README.md) are refused by
the structural rules of [SPEC-LIVE-SET-STRUCTURE](live-set-structure.md) REQ-006: the MIDI
track has a session clip slot and no freeze sequencer
([audit](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/released-fixture-audit.json)).
13 "opens" cases are contradicted and 8 refusal cases do not isolate their rule. Released
payloads are immutable, so v2 carries the cases on corrected fixtures. Staging also found
that 3 v1 refusal cases rest on an envelope removal that runs before the checks
(finding SF-3), and that v1's save rule has the step-1 defect that transport-state-v2
corrected.

Every expectation is static-derived; nothing was executed against Live or a candidate
([ADR 0002](../decisions/adr-0002-static-first-analysis.md),
[ADR 0003](../decisions/adr-0003-no-reference-execution.md)). This page is the analyst-side
plan and traceability record, not an implementation input. The candidate is
**unreviewed and unpublished**. Nothing has been written into `handoff/`.

## Scope

Selection rule: D and S clauses with exact values; S clauses only with their stated
assumptions. Excluded are U clauses, runtime and render clauses, anything on an open
item of [Q-020](../questions.md#q-020-automation-envelope-load-robustness),
[Q-022](../questions.md#q-022-live-set-structure-load-rules) or
[Q-023](../questions.md#q-023-mix-graph-t1-conditions), and every evaluated value.

| Requirement | Included in v2 | Excluded remainder |
| --- | --- | --- |
| 001 | v1 clauses. New clause 5: the MIDI track's `ClipTimeable/ArrangerAutomation` has the `Events` shape and is not an envelope (D; r2) | Other timelines; non-empty timelines |
| 002, 003, 006, 008, 009 | v1 clauses, unchanged | As in v1 |
| 004, 010, 011, 013 | None | All (see [value cases](#value-cases)) |
| 005 | A single track event at L: the document opens | Whether the envelope is kept (SF-3) |
| 007 | Clip envelope with an empty list refused; first-event time check for envelopes with at least two events; later times unchecked; empty MIDI-track timeline opens (S, assumption I7) | Track envelopes with fewer than two events and clip envelopes with exactly one (SF-3) |
| 012 | v1 load rules. Save step 1 from the binary64 logarithm, with the transport-state-v2 band and assumption (r4 defers to REQ-TRANSPORT-STATE-011) | Saved negative zero; the band |

Assumption A3 (open reaches the checks) is settled by SPEC-LIVE-SET-STRUCTURE A1 and is
no longer stated. A4 and A5 stay stated, with I7 (timeline) and the logarithm accuracy.

### Case disposition

21 cases. Release case *n* is AUTOMATION-ENVELOPES-*n*.

| v1 case | v2 | Note |
| --- | --- | --- |
| 001, 002, 005–010, 012–021 | Carried | Records identical to v1; fixture = v1 file + 40 inserted lines |
| 003, 004 | Not carried | Track envelope with one event at 4 / no event, expected refused: removed on open unless an untraced target flag is set (SF-3) |
| 011 | Not carried | Clip envelope with one event at 4, expected refused: removed on open (SF-3) |
| — | 030, 031 | New: first event at 4 with two events, track and clip (replace 003, 011) |
| — | 032 | New: r4 AEN-033 on v1 case 010's document plus the structural lines |

IDs 022 to 029 were withdrawn in the v1 review and are not reused.

## Value cases

The v1 review (RVE-01) withdrew every value case because A1 was untraced. Revision 4 per
target:

| Target | A1 in revision 4 | Value case possible? |
| --- | --- | --- |
| Pan (and split pans) | Identity on [−1, 1] (X, `A1_pan_converter_slot0x28_on_range`); revision 3's reading also gives the identity | Conversion settled |
| Speaker, CrossFadeState | No conversion (X, REQ-011) | Conversion settled |
| `ControllerTargets.6` | Clip envelope; clip time base U | No |
| Volume, Send | Fader positions, S-cond on SPEC-MIX-GRAPH A3 (Q-019, Q-023) | No; no fixture has them |

The settled targets still get no value case:

- **Evaluator E(t)** (AEN-015 to 025, X). Revision 4's A2: which user-visible reading shows
  E(t) is untraced, and playback does not apply it to Float envelopes. No observable framing
  exists without a traced reading.
- **Playback P(t)** (AEN-015 to 025, S with X arithmetic). It is not marked settled. Every
  playback expectation rests on SPEC-MIX-GRAPH A8: that a loaded track's arrangement
  envelopes drive its parameters, with the initial automation index inferred. A8 is an open
  item of Q-023. Values also reach the parameter through ramps (REQ-MIX-GRAPH-014, S (A6)),
  so the 32-bit applied value at a sample is not established (SF-6). P(t) is also a runtime
  clause.
- **AEN-014** (reset of non-monotone controls): r4 keeps the enablement U (but see SF-2).

## Findings while staging

Spec errors and gaps for the spec author. This page does not edit the spec.

- **SF-1.** r4's A3 row and REQ-007's "S (A3)" are stale. SPEC-LIVE-SET-STRUCTURE r1 A1
  (settled) states that it settles this A3 for Live Sets.
- **SF-2.** r4 REQ-009 keeps "whether opening runs the normalization" U. Its named static
  route is the reading context's post-load flag. Its getter `0x1015192c0` is the gate cited in
  r4's appendix, and the T11 A1 trace (`traces/a1a2/trace.txt`) shows the flag set on every
  Live Set open. The reset to 0.5, and AEN-014's save part, look static-derivable.
- **SF-3.** r4 REQ-007 omits a removal step. A further envelope removal runs in the song
  post-load step, before the validation walk that applies REQ-007. SPEC-LIVE-SET-STRUCTURE
  REQ-014 marks its conditions U. The arm64 pseudocode
  ([retained excerpts](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v2-analysis/purge-excerpts.jsonl))
  shows the conditions:
  - **Track envelopes** (`0x102406378`): removed when the target-device relation fails, or
    when the envelope has at most one event. The second test is skipped when the target's
    `+0x1e8` object reports `+0x338` true; that flag is untraced.
  - **Clip envelopes** (`0x1024559b8`): removed when the relation fails or when the envelope
    has exactly one event. The count is the list size (`0x1025654e8` over ±DBL_MAX).
  - **Consequences.** AEN-004 and 005 (if the flag is false for Pan) and AEN-010 open rather
    than being refused, and so would v1 cases 003, 004 and 011. AEN-011 (empty clip
    envelope) is still refused. AEN-032 opens either way.
  - **Status.** This reading is P only, not confirmed in x86 disassembly. REQ-007 needs the
    qualification, and SPEC-LIVE-SET-STRUCTURE REQ-014's U needs resolving.
- **SF-4.** r4's AEN-033 is built on T0, the v1 case-010 fixture, which REQ-006 refuses. v2
  case 032 adds the structural lines.
- **SF-5.** r4's "Released automation-envelopes-v1 is not contradicted" no longer holds
  (T11 audit; SF-3).
- **SF-6.** r4's value comparator gives playback values exact at 32 bits. REQ-MIX-GRAPH-014
  delivers them through ramps: the last ramp before a point is within one data step, and the
  per-sample interpolation is untraced. The playback column is the segment value P(t), not
  the value applied at a sample.
- The Q-020 note that REQ-002's dangling exclusion can narrow (SPEC-LIVE-SET-STRUCTURE
  REQ-014) is not yet applied in r4. v2 keeps the exclusion.

## Deliverables

- **Payload.** [README.md](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v2/README.md)
  (supersession and an 11-item change list), `AGENTS.md`, `spec.md`, `cases.json` (21 cases),
  `fixtures/` (21 XML files) and a draft `manifest.json`. The manifest records review
  pending, `supersedes: automation-envelopes-v1` with the superseded digest `793c1d7d…378302`,
  the change list, the fixture changes and the stated assumptions. It lists 25 payload files,
  26 with itself. Draft manifest SHA-256:
  `455075c02d055be5842e0256a753eb5baa70b9cefd81fc8418e07b59bf1685fd`. Review edits will change
  it.
- **Analyst side, never shipped.** `automation-envelopes-v2-analysis/`:
  - [build_v2.py](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v2-analysis/build_v2.py)
    (build, seal, verify). It imports the v1 generator, the v1 model and the T11 checker
    unchanged.
  - [trace_v2.py](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v2-analysis/trace_v2.py)
    and [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v2-analysis/traceability.json):
    per case, clause, value disposition and finding.
  - [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/automation-envelopes-v2-analysis/author-validation.json).
  - `t11-fixture-audit.json` and `t11-schema-check.jsonl`: the T11 checkers' own output on
    the v2 fixtures.
  - `purge-excerpts.jsonl`: 10 corpus records with line SHA-256 (SF-3).
  - `v1-to-v2-text.diff`.

## Evidence traceability

| v2 cases | Evidence | Residual inference |
| --- | --- | --- |
| Carried 18 | v1 [traceability](automation-envelopes-handoff-plan.md#evidence-traceability); open path settled by T11 A1 | I3 (014, 015, 021), I5 (save cases), I8 |
| 002 | Opens whether or not the removal of SF-3 applies | None |
| 012 | REQ-007 empty-list check (s6-0001); the clip removal keeps a zero-event list (SF-3, P) | I8; if the reviewer rejects the P reading, withdraw 012 and leave clause 1 unreleased |
| 030, 031 | REQ-007 first-time check; two events, so the count test cannot remove them | I8 |
| 032 | AListAutomation +0x100 is a no-op; the check is reached only from the envelope classes (s6-0003); shipped sets hold empty timeline lists | I7 |
| Every fixture | T11 schema and structure rules: no refusal, no unknown shape, no deviation | A5 of SPEC-LIVE-SET-STRUCTURE (list-item Ids, all unique here) |

I7: no open step refuses an empty MIDI-track timeline. I8: envelopes with two or more
events on their own track's mixer or MIDI-controller targets pass the relation test. The
relation test was not evaluated for these targets; SPEC-LIVE-SET-STRUCTURE's fixture rule
covers it.

## Fixture construction and sanitization

`build_v2.py build` makes each fixture from the v1 template with the case's envelopes. It
then inserts 40 whole lines after unique anchors: on the audio track, a `MainSequencer` and
a `FreezeSequencer` with one empty clip slot each; on the MIDI track, a `FreezeSequencer`
with one empty slot; and one `Scene`. The forms are the audit's minimal and recommended
additions, from T11-MIN's skeleton. No v1 line changes. The other elements of the
minimal-set table that v1 lacks are value-bearing or W. REQ-001 makes their absence no
error, and no judged output depends on them, so they are not added ("change only what
validity requires").

The payload holds no shipped content, recovered text, internal names, addresses, analysis
identifiers or analyst links. The deny list is v1's, widened with T11, removal and
playback terms and non-automation spec IDs, and it has no hit.

## Mechanical checks performed

`python3 -I -B build_v2.py build` then `seal` (CPython 3.13.9, `TMPDIR` in the session
scratchpad):

- The model (v1's, with the v2 narrowing and save step 1) agrees with all 21
  expectations. A mutated expectation is detected for 21 of 21.
- **Isolation.** Each of the 7 refused fixtures has a control with only the tested
  defect repaired. Each control opens and passes T11, and differs in one line (four for
  012).
- **Excluded inputs.** 12 probes give no expectation. The two step-1 examples of
  transport-state-v2 reproduce.
- **Carried cases.** Each carried fixture equals the v1 released file with the insertions,
  and each carried record equals v1's.
- **T11 checkers.** `fixture_audit.py`, run by its own command line on a copy, finds 21
  Live Sets, 0 refused, 0 contradicted and 0 not isolating. `schema_check.py` finds no
  deviation.
- **Evidence identity.** The 79 S6 files, the 74 T11 files and the `Live.arm64` digest
  match. The 10 excerpts match their corpus lines.
- **Package.** The 25 hashes and sizes match, and the inventory equals the directory.
  Links and case inputs resolve, with no deny-list hit. A copy in the scratchpad passed
  `verify`, an independent re-hash matched, and the copy is identical to staging.

Not checked: any reference or candidate execution; SF-3 in x86 disassembly; the track
removal's target flag.

## Review gates still required

1. **Scope review** in a separate context:
   - SF-3 and the narrowing of REQ-005 and 007;
   - carrying 012 on the P reading;
   - the timeline clause and I7;
   - save step 1 and its assumption;
   - the value-case disposition.
2. **Quality and sanitization review**:
   - the change list against `v1-to-v2-text.diff`;
   - exclusions in both the spec and the manifest;
   - no internal structure.
3. **Evidence identity**: the S6 and T11 manifests and the image digest.
4. **Fixture review**: the 40 inserted lines and the 3 new inputs.
5. **Finalize and publish** only after approval, as in the
   [workflow](../workflows.md#release-a-handoff). The catalog, spec status, coverage, indexes
   and log are updated then, not by this staging task.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate:
- 21 cases;
- partial REQ-AUTOMATION-ENVELOPES-001 to 003, 005 to 009 and 012;
- 004, 010, 011 and 013 unreleased.

It is not published, and automation-envelopes-v1 remains the current release with its
catalog warning. This page has no inbound catalog link yet; the staging task did not edit
the spec index.
