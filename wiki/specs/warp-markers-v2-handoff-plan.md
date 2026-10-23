---
id: PLAN-WARP-MARKERS-V2-HANDOFF
type: research
status: current
updated: 2026-10-19
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Second warp-markers handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [warp-markers-v2](../../handoff/warp-markers-v2/README.md), approved with narrowing by a separate review agent ([review record](../../handoff/warp-markers-v2/REVIEW.md)). It has 63 cases.

The narrowings:
- **Devices:** both devices are removed from every fixture, because device placement is not established. Case 018 is withdrawn, and REQ-001 clause 2 and REQ-004 go with it.
- **REQ-009:** unreleased, because no released output can observe it.
- **Labels and order:** the extracted-execution label is reworded so it claims no more than was run. An add is decided by its first failing check.

All 15 extracted-execution labels match the raw runs, and a fresh re-run reproduced them bit for bit.

Draft reconciliation, 2026-10-19: [revision 5](warp-markers.md#revision-and-handoff)
applies F1 to F6 and RVW2-02: WMK-019 is computed by confirmed rules; WMK-039
adds the below-half discriminator; the shadow formula is evidence without an
observable acceptance case; A1 is settled by the structure trace; duplicate marker
Ids inherit the conditional shared rule; REQ-009 needs playback acceptance.
No released byte or expectation changed.

## Decision and boundary

Stage a superseding candidate, warp-markers-v2, from
[SPEC-WARP-MARKERS revision 4](warp-markers.md). It follows the
[warp-markers-v1 plan](warp-markers-handoff-plan.md), the
[transport-state-v2 plan](transport-state-v2-handoff-plan.md) (a superseding
release), the [als-container plan](als-container-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff).

Why a new release: [SPEC-LIVE-SET-STRUCTURE](live-set-structure.md) shows that
opening a Live Set always runs a validation walk, and that the walk refuses a
track with clip slots but no matching freeze slots (REQ-LIVE-SET-STRUCTURE-006).
The [fixture audit](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/released-fixture-audit.json)
finds that 17 of the 18 [warp-markers-v1](../../handoff/warp-markers-v1/README.md)
documents fail it, contradicting 35 cases, and that the refusal cases 007 and 008
no longer isolate their rule. Released payloads are immutable. v2 carries every
v1 case record unchanged on fixtures rebuilt on the minimal set T11-MIN. It also
adds the clauses that revisions 2 to 4 settled: the scripting conversion values
(X), the beat bounds and grid rounding as binary64 sequences (X), the REQ-015
edges of revision 2, while the proposed statement that a session clip that is not warped ignores its
markers (revision 4) was excluded by review RVW2-02. Per-mode warped playback stays out.

Under [ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary)
and [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code)
the expectations are static-derived, or come from the
[X2 run](../../analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/manifest.json)
of the x86_64 slice. Each new case is labelled "extracted execution" when X2 ran
its deciding values on its inputs, and "computed by extracted-execution rules"
when they come from the X-confirmed sequences on inputs X2 did not run. No
reference application or candidate has run, and no compatibility is claimed.

This page is the analyst-side plan and traceability record, not an
implementation input. The staging and review-gate sections below record the pre-review candidate; the
released outcome above governs current status.

## Scope

Selection rule: release only D, S and X clauses with exact values. Exclude U
clauses, clauses resting on an assumption the spec still labels open (A1, A4),
anything that depends on [Q-021](../questions.md#q-021-warp-playback-mapping-and-load-handling),
and runtime, timing and audio behavior, except the one statement the task asked
for (REQ-009).

| Requirement | Included in v2 | Excluded remainder |
| --- | --- | --- |
| 001, 003, 010 to 013 | v1 clauses, unchanged | As in v1: save (A4), `TransientEnvelope` (range U, Q-021), `WarpMode` default (U), labels (inferred), out-of-range values (REQ-014) |
| 002 | v1 clauses, unchanged | As in v1; `Id` (U here; duplicates refused under REQ-LIVE-SET-STRUCTURE-016, S-cond A5, finding F6) |
| 004 | v1 clause (sample part) | Audio-clip empty list refused (A1; finding F4); presentation (U) |
| 005, 006, 014 | None | All (U or Q-021) |
| 007 | v1 clauses; the shadow segment governs the conversions past the last visible marker (S, X); a spacing other than 1/32 beat is kept on opening (S, A2) | Where and when Live creates or re-places a shadow, and the append formula (X for the routine, operands and callers U: finding F5); re-placement after edits or saves (U); sample-part lists |
| 008 | v1 clause; the conversion values: x = t / R, segment choice, both extensions, the fused evaluation, x × R, for a call right after opening (S; X for the cores) | n = 1, equal or unsorted lists (U); results after edits (A3's untraced half); non-audio clips |
| 009 | Statement only, no case: a session clip that is not warped does not use its markers (S, revision 4) | The warped conversion step (S, but whether it drives the audio is U); per-mode read positions (U); arrangement clips; audio |
| 015 | v1 clauses, with clause 5 restated as the binary64 beat bounds (X); no left neighbour below the first marker, Δs = 0, move without a warped check, remove on two markers accepted (S, revision 2) | List after accepted edits (U); move limits and accepted moves (U); a move on fewer than three markers; `warp_mode` setter (U); interactive edits (U) |
| 016 | v1 clauses, with clause 1 restated as the binary64 sequence (X) | Sentinels and non-finite values (outside the argument scope); interactive beat setter |

Combined failures have no expectation. Release case IDs are WARP-MARKERS-001 to
064; the payload carries no draft case ID.

### Case disposition

| Draft case | Release cases | Note |
| --- | --- | --- |
| As in the [v1 disposition](warp-markers-handoff-plan.md#case-disposition) | 001 to 038 | Records identical to v1; fixtures rebuilt |
| WMK-016 | 039 to 045 | Frames divided by 6 for the 8,000 Hz WAV: the same seconds as the X2 inputs at 48,000 Hz |
| WMK-017 | 046, 047 | New document `first-marker-later.xml` (draft list M2) |
| WMK-018 | 048 to 050 | Results × 8,000 |
| WMK-019 | 051 | New document `two-markers.xml` (draft list M0); not run by X2 (finding F1) |
| WMK-037 | 052, 053 | |
| WMK-038 | 054, 055 | |
| WMK-039 | 056, 058, and new 057 | 057 is X2's value one ulp below the halfway point (finding F3) |
| WMK-036 second call | 062 | v1 carried the first call as 038 |
| WMK-014 | 064 | Load part only, re-authored on the three-marker list (shadow 1/16 beat after) |
| None | 059, 060, 061, 063 | Revision 2 clauses without a draft case: Δs = 0 accepted and refused, no left neighbour, remove on two markers |
| WMK-006 | None | A1 (finding F4) |
| WMK-008 to 013, 022, 025 to 027 | None | U, or REQ-014 |
| Save parts of WMK-001 to 005, 007, 014, 021, 023, 024 | None | A4 |

Of the 26 new cases, 15 are labelled extracted execution (039 to 050, 052, 056,
057), 7 computed by extracted-execution rules (051, 053 to 055, 058 to 060) and 4
static-derived (061 to 064). Under v1's rules, 24 of the 26 had no expectation
(conversion values, the three bands, the add below the first marker, a remove
on two markers); 062 and 064 agree with v1's rules. So v2 contradicts no v1
expectation.

## Findings while staging

Spec errors and proposed corrections for a revision 5. This page does not edit
the spec.

- **F1. WMK-019 is not X.** The acceptance-case paragraph ("revision 3: WMK-016
  to 019 and 037 to 039") and the revision 3 row ("WMK-016 to 019 confirmed")
  say extracted execution confirmed WMK-019. X2 ran only the M1 and M2 tables
  (`results/envelope-warp.json` `warp_WMK016_M1`, `warp_WMK017_M2`; run labels
  M1 and M2 in `raw/runs.jsonl`; `run_x2.py` lines 293 to 296), as REQ-008's own
  X clause says ("WMK-016 to 018"). WMK-019's value follows from the confirmed
  formula. Proposed: say so in both places. v2 labels case 051 accordingly.
- **F2. WMK-037 to 039 partly computed.** X2 ran q() on 2.0416666666666665 and
  2.0000001300782553 and the bounds at p = 1.5. q(2.0416664065101564),
  q(11.325), q(11.325000260156509), q(2.0000001300782544) and the bounds at
  p = 2.5 come from `check_rules.py`. The spec's wording ("take their outcomes
  from the X-settled 64-bit sequences") is accurate; v2's labels follow it.
- **F3. WMK-039 does not discriminate.** 2.0000001300782553 lies above the
  exact halfway point, so exact rounding also rounds it up, and
  2.0000001300782544 gives 2 under both rules. The value that tells the binary64
  sequence from exact rounding is 2.000000130078255, one ulp below the halfway
  point, which X2 ran and REQ-016's X clause names. Proposed: add it to WMK-039.
  v2 adds it as case 057.
- **F4. A1 looks settled.** SPEC-LIVE-SET-STRUCTURE's A1 (settled S on
  2026-10-18) traces that every set-open path reads with the XML reader, whose
  reading context sets the post-load flag `+0x2c`, so each member's post-load
  step runs. REQ-004's appendix row gates the empty-list test on exactly that
  flag ("Post-load runs when context flag +0x2c is set (A1)"). Revision 4 still
  calls A1 "inferred, not traced", and Q-021 lists it open. Proposed: mark
  REQ-004's first clause S with that citation and close A1 in Q-021. A later
  release could then carry WMK-006 on a T11-MIN document. v2 does not, because
  revision 4 labels it A1.
- **F5. The shadow-marker formula has no releasable observable.** The task
  asked to add it. REQ-007's X clause is a property of the append routine: its
  operands p₁ and p₂ are U at every caller, which user operations call it is U,
  and the spec gives it no case ("no procedure here makes the clip recompute its
  shadow"). Stating it in the payload would need the routine's internal
  arguments. v2 releases only the shadow's observable roles (clauses 7.3 and
  7.4) and lists "the values it gives a new shadow" as excluded. A release needs
  a static trace of the callers' arguments first.
- **F6. Marker `Id`.** REQ-002 keeps `Id` handling U. SPEC-LIVE-SET-STRUCTURE
  REQ-016 (S-cond A5) makes a duplicate or negative list-item `Id`, marker Ids
  included, refuse the set. Proposed: cross-reference it in REQ-002. v2 keeps
  repeated `Id`s as an input without expectation.
- **F7. No contradiction on value-less settings.** REQ-LIVE-SET-STRUCTURE-001
  refuses a base value written as an element without `Value`
  (`<NextPointeeId />`; corpus `0x10152b45c` → `0x10152d54c`, "Required
  attribute"). The eight settings are compounds (schema `UserFloat` and
  `RemoteableEnum`, type 0) whose `Value` is an attribute member, so the loader
  skips a missing one and REQ-010's "without its `Value` attribute" clause, and
  case 010, stand. The spec could say so.

## Deliverables

- Payload under `analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2/`:
  [README.md](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2/README.md)
  (scope, supersession, change list with every fixture change), `AGENTS.md`,
  `spec.md`, `cases.json` (64 cases), `fixtures/` (21 XML documents and
  `sample.wav`) and a draft `manifest.json` (`release_status:
  candidate-unreviewed`, review pending, `supersedes: warp-markers-v1` with the
  superseded manifest digest `f8546a3e…1764ef46`, the change list, the three
  provenance labels and seven stated assumptions). The manifest lists 26 payload
  files; with itself the package has 27 (683,424 bytes). Draft manifest SHA-256:
  `6ff7f7e2fd828544de8535b2b066d1156cc744ee9c8ecaaed2ab367f52fbddb3`. Review
  edits will change it.
- Analyst side, never shipped: `warp-markers-v2-analysis/` with
  - [build_v2.py](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2-analysis/build_v2.py):
    fixtures from the T11-MIN generator, the 26 new cases, the 38 v1 records
    copied verbatim, the draft manifest;
  - [check_v2.py](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2-analysis/check_v2.py):
    cross-check model (binary64 rules, and v1's exact rules for the carried
    cases), X2 agreement and label check, carry check, mutation check, seal and
    verify;
  - [fixture_checks.py](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2-analysis/fixture_checks.py):
    runs `schema_check.py` and `fixture_audit.py` unchanged, the single-change
    comparison and the fixture report;
  - [v2_meta.py](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2-analysis/v2_meta.py):
    evidence, inferred links, traceability tables, deny list, manifest metadata;
  - outputs [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2-analysis/traceability.json),
    [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2-analysis/author-validation.json),
    [schema-check.jsonl](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2-analysis/schema-check.jsonl),
    [fixture-audit.json](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2-analysis/fixture-audit.json)
    and [v1-to-v2-text.diff](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v2-analysis/v1-to-v2-text.diff).

## Evidence traceability

The v1 evidence ([v1 plan](warp-markers-handoff-plan.md#evidence-traceability),
[v1 review](../../handoff/warp-markers-v1/REVIEW.md)) carries over; the d7 rounds
are now cited from their retained run
[d7-warp-v1](../../analysis/ableton-live-12.4.3/r2/d7-warp-v1/manifest.json).
Per-case and per-clause locators are in `traceability.json`; the payload contains
none of them.

| v2 cases | Kept evidence | Inferred links |
| --- | --- | --- |
| 001 to 038 | As in v1. The warped test is now evidence (v1 review RVW-06), not an inference. X2 also ran q(2.0000001), q(2.001) and the bounds at p = 1.5 used by 028, 031 and 035 to 037 | I1 to I6 as in v1 |
| 039 to 050 | Conversion entry points `0x1033bf160`, `0x1033bf250` and the table builder `0x1028939a4`, `0x10277b71c` (d7-0001); X2 `warp_WMK016_M1`, `warp_WMK017_M2` | I3, I8 (divisor is the sample rate, pseudocode `0x1027b7514`), I9 (arm64), I10 (A3) |
| 051 | As 039, value from `check_rules.py` (F1) | As 039 |
| 052 to 060 | Add `0x1033bf42c` (s8-0001, re-read: first node has no left check; shadow as last position), bounds `0x1027afd40`; X2 `beat_grid_round` and `add_bounds_lo_hi`; `check_rules.py` for the inputs X2 did not run; lookup and insert/delete records of the v1 review | I3, I4, I5, I6, I9 |
| 061 | Add `0x1033bf42c` (left check skipped for the first node); v1 review section 5 (c) | I3 to I5 |
| 062 | Move `0x1033bfb94` (s8-0003, re-read: class test only) | I3, I6 |
| 063 | Remove `0x1033bfa68` (s8-0002); delete `0x1027c6eec` returns below three markers (v1 review corpus record) | I3, I5, I6 |
| 064 | Loader; v1 review section 5 (a): no completion step moves the last marker | I1, I3 |
| REQ-009 statement | [t13-playback-v1](../../analysis/ableton-live-12.4.3/r2/t13-playback-v1/manifest.json) `audio/match-x86.txt` lines 1 to 4 and 94 to 98; [playback core](../research/playback-core.md); SPEC-PLAYBACK-CORE REQ-017 | None |
| Fixture validity | [t11-structure-v1](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/manifest.json): `make_fixture.py`, `schema_check.py`, `fixture_audit.py` | SPEC-LIVE-SET-STRUCTURE A6 (device placement), stated in the payload |

| Link | Inference not established by kept evidence |
| --- | --- |
| I1 to I6 | As in v1 (I3 now narrowed by the v1 review's static check of the read and the completion steps) |
| I8 | The conversions divide and multiply by the clip's sample rate (divisor source pseudocode) |
| I9 | The arm64 build computes the X-confirmed sequences as the x86_64 slice did (same operation order; fused steps single-rounding in both) |
| I10 | The first conversion after opening uses the list held after opening (spec A3: table built once on first use) |

## Fixture construction and sanitization

`build_v2.py build` imports the T1.1 generator `make_fixture.py` unchanged; its
SHA-256 `ef81e835…a5908` is checked against the t11 run manifest. It builds
T11-MIN with the generated WAV's bytes, so the generator computes
`OriginalFileSize` 48044 and `OriginalCrc` 23034 itself. The base set then
changes only the clip:

- `IsWarped` true, `WarpMode` 4 and v1's eight settings after `WarpMode`;
- v1's marker list M1 with Ids 10 to 13;
- the sample reference `RelativePath` `sample.wav`, `Path` `/Fixtures/sample.wav`,
  `DefaultDuration` 24000 and `DefaultSampleRate` 8000.

Compared with T11-MIN, base.xml differs in 30 lines, all inside the clip. Each
v1 document is the base set with v1's change. Ignoring indentation, its changed
lines equal v1's, and they all lie inside the clip. The Simpler document
replaces the MIDI track's `UltraAnalog` with `OriginalSimpler Id="0"`, which
holds the same `On` parameter (same pointee Id) and v1's `Player` subtree. The
three new documents change only the marker list.

The WAV is v1's generator output, byte-identical to v1's `sample.wav`
(`59db6dfb…bdcc0ec`), with its modification time set to `LastModDate`
1,760,000,000 as T11-MIN does. Two builds are byte-identical. Every value and
name is invented; nothing is copied from a shipped file. The deny list adds
planning, harness, instruction, engine-name and library-call patterns to v1's.

## Mechanical checks performed

`python3 -I build_v2.py build` then `python3 -I check_v2.py seal` (CPython
3.13.9) wrote the author validation:

- **Structure.** `schema_check.py` reports no schema deviation in any of the 21
  documents. `fixture_audit.py`, run on a copy of the stage directory, finds 0
  refused documents, 0 unknown shapes, 0 contradicted and 0 non-isolating cases.
  Cases 007 and 008 are therefore refused only for their number text.
- **Carry.** All 38 v1 records are textually identical to the released
  `cases.json`. Both the binary64 model and v1's exact-rule model agree with
  each of them.
- **Model.** The cross-check model agrees with all 64 expectations, and every
  conversion value is bit-identical. A mutated copy of each expectation is
  detected (64 of 64). The model restates the released clauses from the same
  evidence and is not an oracle.
- **X2 agreement.** Each case labelled extracted execution has every deciding
  value in the X2 results, and each one equals the expectation. Each case
  labelled computed has at least one deciding value that X2 did not run, and
  every value that X2 did run agrees. `check_rules.py` re-ran with "mismatches:
  none".
- **Package.** The hashes and sizes of all 26 files match, and the inventory
  equals the directory. All 12 Markdown links resolve inside the package, and
  every case input and sample exists. The deny list has no hit, apart from the
  allowed "decompil" in `AGENTS.md`. A probe copy with planted terms was
  flagged.
- **Export.** In a scratchpad copy, `verify` matched everything above, and an
  independent `sha256sum -c` of the manifest inventory passed.
- **Evidence identity.** The s8 (76 files), d7 (34), x2 (18), t11 (74) and t13
  (153) runs match their manifests, as do the arm64 image and the v1 release
  manifest `f8546a3e…`.

Not checked: any reference or candidate execution, the arm64 build at run time,
and any proof of I1 to I10 or of the T1.1 structure assumptions.

## Pre-review gates (historical)

1. **Scope review** in a separate context. Read each of the 26 new cases
   against its locator, and rule on:
   - the three provenance labels;
   - the ungraded REQ-009 statement;
   - the exclusion of the shadow-marker formula (F5);
   - the base set as fixture context, and stated assumption 1 (structure, A6).
2. **Superset check.** From `v1-to-v2-text.diff` and the carry and
   single-change checks, confirm that no v1 record changed and that every v1
   document keeps its change. Confirm that REQ-015 clause 5 and REQ-016 clause 1
   give v1's outcomes within v1's scope.
3. **Quality and sanitization.** Check behavioral completeness, the agreement
   of exclusions between `spec.md` and the manifest, and the absence of
   internal names, addresses and analyst links. The fused multiply-add wording
   must read as arithmetic, not as code.
4. **Evidence identity.** Decide whether to re-run X2 (`sh run.sh`) before
   release.
5. **Finalize.** Add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the handoff catalog.
6. **Publish** only after approval. Copy the package unchanged to
   `handoff/warp-markers-v2/`. Then add a catalog row superseding
   warp-markers-v1, update the known-fixture-defect note, the spec status,
   coverage, Q-021, Q-022, the indexes and the log, and apply F1 to F7 in a
   spec revision 5. Never edit warp-markers-v1.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Released 2026-10-18 as warp-markers-v2 with 63 cases after withdrawal of device
case 018. It is current and supersedes v1. Partial REQ-001, 002, 003, 007, 008,
010 to 013, 015 and 016 are released; 004 to 006, 009 and 014 remain unreleased.
Device/sample-part placement, playback and unobservable shadow creation remain
excluded. Draft revision 5 reconciles the review and later settled A1; it does not
retroactively widen the release.
