---
id: PLAN-MIXER-VALUES-V2-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Second mixer-values handoff: candidate and review plan

## Decision and boundary

Stage a superseding candidate, mixer-values-v2, from
[SPEC-MIXER-VALUES revision 4](mixer-values.md). It follows the
[mixer-values-v1 plan](mixer-values-handoff-plan.md), the
[als-container plan](als-container-handoff-plan.md), the
[transport-state-v2 plan](transport-state-v2-handoff-plan.md) (a superseding
release with extracted-execution cases) and the
[release workflow](../workflows.md#release-a-handoff).

Two reasons for a new release:

- **Fixture validity.** Opening a Live Set always runs the validation walk of
  [SPEC-LIVE-SET-STRUCTURE](live-set-structure.md) r1. The 37
  [mixer-values-v1](../../handoff/mixer-values-v1/README.md) fixtures are not
  refused by any traced rule, but every one lacks `SendsPre`, whose absence has
  an unknown effect (REQ-LIVE-SET-STRUCTURE-013 U;
  [audit](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/released-fixture-audit.json),
  `mixer-values-v1`: 37 with unknown shapes, 0 refused). They also lack every
  element that the minimal-set table of REQ-LIVE-SET-STRUCTURE-018 marks W
  (write it; absence unknown): names, colours, `TrackGroupId`, routing, clip
  slot lists, scenes and the quantisation values. v1's precondition that
  absent content cannot change a judged outcome is therefore not established.
- **Clauses settled since v1** by the [x2-mixer-v1](../../analysis/ableton-live-12.4.3/r2/x2-mixer-v1/manifest.json)
  extracted execution (label X, revision 3): both fader-curve conversions and
  the round trip (REQ-005), the pan-law gains (REQ-013), the crossfade curve
  levels (REQ-014) and the `On`/`Off` text (REQ-008).

Following [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code),
the new cases carry "extracted execution (x86_64 slice, glibc substitutions);
arm64 equivalence inferred". The computed gains are released as computed
values. Where and when the engine applies them belongs to
[SPEC-MIX-GRAPH](mix-graph.md) and stays out: revision 4 settles that path only
as S/Q-019 under SPEC-MIX-GRAPH's conditions A3 to A5
([Q-019](../questions.md#q-019-mixer-volume-and-send-values-sent-to-the-engine),
[Q-023](../questions.md#q-023-mix-graph-t1-conditions)), and rendered audio is
excluded by the selection rule. No reference application or candidate has run,
and no compatibility is claimed.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. Nothing
has been written into `handoff/`.

## Scope

Selection rule: documented, static-derived or X clauses with exact values.
Excluded: U clauses, S/Q-019 clauses, audio renders, timing, and anything that
rests on an open question.

| Requirement | Included in v2 | Excluded remainder |
| --- | --- | --- |
| 001–004, 006, 007, 009 | v1 clauses, unchanged. 001 states the further mixer children the fixtures hold; 003 states the fixtures' `SendsPre`; 009 points to 014 for curve levels | As in v1 |
| 005 | S construction of both 101-point curves; S rules for both conversions, confirmed by X at the 20 run inputs; exact round trip (X) at the seven curve points run | Fader and controller binding (U, Q-009); every input not run; the round trip of other gains (see F1) |
| 008 | v1 clause; the `On`/`Off` rule is also X. Cases 001 and 030 keep their static-derived records | `SoloSink` meaning (read statically as the Solo button in SPEC-MIX-GRAPH A2, not applied here) |
| 013 | Pan-law formula (S), confirmed by X at the nine run inputs; expectations for w and v in {0, 1} only | Which w and v the audio path supplies (w = `PanMode`: see F3; v = track gain: S/Q-019), the 75-sample ramp, application to audio |
| 014 | Levels of the seven curves at the X positions that are multiples of 1/64: −1, −0.5, −0.25, 0, 0.25, 0.5, 1 | ±0.95 (run, but not table points; the engine applies a 129-point table, S), the crossfader-to-position mapping and A/B orientation, Transition on position, ramps, application to audio |
| 010, 011, 012, 015 | None | All: 010 U for a 12.4.3 save; 011 and 012 S/Q-019 and audio; 015 U |

### Case disposition

| Draft case | Candidate | Note |
| --- | --- | --- |
| v1 cases MIXER-VALUES-001–037 | Carried, 001–037 | Records byte-identical to the released v1 `cases.json`; fixtures rebuilt |
| MV-023 | 038–043 | Volume position → gain at 0, 0.25, 0.5, 0.7, 0.85, 1 (binary32 positions), one step |
| MV-024 | 044–049 | Send position → gain at the same positions, one step |
| MV-025 | 050–057 | All eight X gain → position inputs (MV-025 lists four), within 1e-6. Send 0.1 gives 0.49999976, within MV-025's 0.5 ± 1e-6 |
| REQ-005 round-trip bullet | 058–064 | Seven distinct (curve, gain) pairs of the X run; exact. The run's duplicate send 1.0 is dropped |
| MV-048 | 065–073 | Nine X input vectors, one step or 1e-12 |
| MV-047 | 074–080 | One case per curve code, seven positions each, one step or 1e-12 |
| MV-018 | Carried as 030 | Label kept (transport-state-v2 RV ruling on carried records) |
| MV-026 | Not released | The written range text is REQ-010's U part; the gains are 038, 043, 044, 049 |
| MV-020–022, 027, 028, 041–045 | Not released | U or U part |
| MV-029–040 | Not released | Audio renders (S/Q-019 or unmeasured) |

Draft case IDs do not appear in the payload. `traceability.json` maps every case
to its source and X record.

## Fixture rebuild on T11-MIN

All 37 fixtures come from one template set built with the T1.1 generator
`make_fixture.py`, imported unchanged: T11-MIN with three parts removed.

- The clips in the first MIDI and audio slots, and with them the sample file,
  are removed. Opening then does not involve A4 (sample resolution), and the
  set carries no SPEC-CLIP-LAUNCH, SPEC-MIDI-NOTE-STORAGE or SPEC-WARP-MARKERS
  content.
- `UltraAnalog` and `Amp` are removed. Opening then does not involve A6
  (device class per chain). The device lists stay, empty, as T11-MIN's main
  track has.
- The MIDI track's volume envelope is removed. It targets a mixer value, which
  v1 excludes.

Everything else is T11-MIN's, including the tempo and time-signature envelopes
of the main track and every W element. The removed device targets were the
last pointees allocated, so the mixer Ids are T11-MIN's and `NextPointeeId` is
67. Track order and Ids are T11-MIN's: MIDI 1, audio 2, return 3. Each case's
edits are v1's, applied to the same mixer elements. The per-fixture edits and
v1 digests are in the manifest's `supersession.fixture_changes`. The README
change list enumerates the template-set changes.

The opening outcome of every fixture rests on REQ-LIVE-SET-STRUCTURE-001, 002,
004 to 006 and 013 to 016, which are S since A1 to A3 were settled, and on
writing every W element as T11-MIN does. A5 concerns only refusals, and A7 only
saving. The contract does not name SPEC-LIVE-SET-STRUCTURE; it states the
template set's structure and excludes other structures.

## Findings while staging

These are proposed corrections for the parent specifications. This page does
not edit them.

- **F1, the round trip is not exact in general.** REQ-005's X bullet says that
  for a stored gain g, gain → position → gain returns g bit-exactly. The run
  covers four curve points per curve. A binary32 position cannot carry every
  binary32 gain: between −6 and 0 dB on the volume curve there are about 2.5
  million binary32 positions for 8.4 million gains. The candidate's model of
  the two conversions, which reproduces all 20 X fader outputs exactly, finds
  1,905 of 4,000 random volume gains and 2,023 of 4,000 send gains not
  returned exactly (worst 2 and 3 binary32 steps; for example volume 0.3
  returns 0.30000004). Affected statements: REQ-005, REQ-011 ("the applied
  gain equals g for g in range"), the revision 4 evidence-label paragraph,
  REQ-MIX-GRAPH-003's X bullet and Q-019's 2026-10-18 progress line.
  Proposed: exact at curve points, within a few binary32 steps elsewhere, with
  an X sweep to bound it. The candidate releases only the seven run points and
  says so.
- **F2, the snap feeds forward.** REQ-005's construction ends with "A result
  whose magnitude is below 0.0001 becomes 0". The x86_64 builder replaces each
  stored point before the next is computed from it. Applied only to the
  finished points, 37 volume gains would differ by a binary32 step, among them
  G[50] and G[70] (MV-023's −14 dB and −6 dB values); the send curve does not
  cross 0. The contract states the forward rule.
- **F3, the w mapping is labelled three ways.** REQ-013's revision 4 bullet
  labels w = `PanMode` code as S. The case rows MV-035 to 037 still say
  "w mapping U", and appendix row 013 says "w mapping inferred". The candidate
  releases the pan law for w in {0, 1} without the mapping.
- **F4, MV-048's comparison.** "Within 1 float32 ulp" cannot hold for the
  cross-feed entries. The original gives 6.12·10⁻¹⁷ where the formula gives 0
  (binary64 cos(π/2)). The candidate adds a 1e-12 absolute bound to the
  pan-law and crossfade comparisons. Crossfade levels at +1 stay exactly 0.
- **F5, MV-047 positions.** The X run also evaluated the curve functions at
  ±0.95. The engine applies a 129-point table over [−1, 1] (REQ-014 S), so off
  the multiples of 1/64 the function value is not the applied level. The
  candidate releases multiples of 1/64 only. The parent should say which
  quantity MV-047 grades.
- **F6, slice note.** REQ-005 says the three lowest table points
  (positions 0.01 to 0.03) can differ by one ulp between slices. The fused
  operation is 3a + (B − e₉₇) in b, which enters only e₉₈ and e₉₉, that is
  D[2] and D[1]; D[3] = e₉₇ does not depend on it. The note is conservative,
  not wrong. The candidate keeps the three-point wording in its stated
  assumption, and case 051, which uses D[3] and D[4], is unaffected either way.

## Deliverables

- Payload: [mixer-values-v2/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/mixer-values-v2/README.md)
  (scope, supersession, change list), `AGENTS.md`, `spec.md`, `cases.json`
  (80 cases), `fixtures/` (37 XML files) and a draft `manifest.json`. The manifest
  has review pending, `supersedes: mixer-values-v1` with the superseded digest
  `5f6b8401…39cd60` (equal to the catalog value), the change list, the
  per-fixture changes, both provenance labels and the stated assumptions. It
  lists 41 payload files; with itself the package has 42. Draft manifest SHA-256:
  `791c22e5c39b2a944c92aed762aa079fae9655c43da0329bbf9672beb8ef3ac0`. Review
  edits will change it.
- Analyst side, never shipped:
  `mixer-values-v2-analysis/` with
  - [build_mv2.py](../../analysis/ableton-live-12.4.3/handoff-staging/mixer-values-v2-analysis/build_mv2.py):
    the template set, fixtures, cases and manifest. It imports `make_fixture.py`
    and `build_mv1.py` unchanged, and reads the X2 results;
  - [seal_mv2.py](../../analysis/ableton-live-12.4.3/handoff-staging/mixer-values-v2-analysis/seal_mv2.py):
    the structure checks, the cross-check models, the mutation probe,
    evidence identity, verification and traceability;
  - [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/mixer-values-v2-analysis/traceability.json),
    [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/mixer-values-v2-analysis/author-validation.json),
    and `structure-check/` (`schema-check.jsonl`, `fixture-audit.json`).

## Evidence traceability

| v2 cases | Evidence | Residual inference |
| --- | --- | --- |
| 001–037 | v1 [traceability](mixer-values-handoff-plan.md#evidence-traceability) and [review](../../handoff/mixer-values-v1/REVIEW.md); template set: `make_fixture.py`, `structure-check/` | v1's I1–I6; I10 (the template set opens, above) |
| 030 (and 001's `On`) | Also X2 `switch_text` (1.0 → `On`, 0.0 → `Off`) | How the Boolean reaches the formatter (not run) |
| 038–064 | X2 `results/mixer.json` `fader.*`; `x86-disasm.txt` builder and both conversions; the 2⁻¹⁷ fraction snap from `s9-mixer-v1/derive_curves.py` (static, arm64) | I7 arm64 equivalence; I8 for 058–064; I9 |
| 065–073 | X2 `pan_law`; `x86-disasm.txt` matrix (binary64 θ and cos, binary32 combination) | I7; I9 |
| 074–080 | X2 `crossfade`; code order of the seven functions as the names (s9-0003) | I7; I9 |

Inferences new in v2 (`traceability.json`):

| Link | Inference | Affects |
| --- | --- | --- |
| I7 | The arm64 build gives the same results within each comparison. Its fused operations are the curve-builder landing point, the binary64 interpolation, the pan θ, and Dipped and Intermediate (`fma-scan.txt`) | 038–080 |
| I8 | The macOS `exp10f` rounds the round-trip curve points to nearest. Model margins: the 1.0 points are exact; +6 dB 0.38, −70 dB 0.19 and −6 dB 0.17 of a step | 058–064 |
| I9 | The macOS `exp10f`, `cos` and `cosf` are within one binary32 step of glibc at these inputs | 038–057, 065–080 |
| I10 | The template set opens (static, as above) | 001–037 |

`seal` checks every new expectation against the X2 record it comes from, and
against an independent model where one exists (fader curves, pan law). The
model uses correctly rounded exponentials (`decimal`) and glibc's `cos`.
It equals X exactly in 35 of 36 modelled cases. The 36th is 070, where the
model gives 0 and X gives 6.12·10⁻¹⁷, within the comparison. Crossfade levels
have no model; seal checks their shape only.

## Fixture construction and sanitization

The fixtures are generated by `build_mv2.py build`; no shipped file is read.
They are ASCII, LF, tab-indented, about 19 KB, and contain no sample. Invented
content: the T11-MIN names `Lead`, `2-Audio`, `A-Return`, `Main`, `Scene 1`,
`Scene 2`, colours and Ids. The three bare numbers shared with shipped sets
(v1 RVM-09) are unchanged. The payload names public document elements,
UI-visible texts, the seven curve names and the provenance terms "x86_64" and
"glibc". It contains no function names, addresses, internal identifiers,
draft case or question IDs, other spec IDs or analyst links.

## Mechanical checks performed

`python3 -I build_mv2.py build` then `seal`, with CPython 3.13.9, wrote
`author-validation.json`:

- The 37 carried records are identical to released v1. The v1 cross-check
  model (`build_mv1.model`) agrees with every carried expectation on the new
  fixtures. Each fixture differs from the template set only in its case's v1
  edits, and the 37 are distinct. The ten v1 excluded-input probes are all
  rejected.
- The T1.1 checkers ran unchanged on all 37 fixtures:
  - `schema_check.py` against the shipped schema `12.0_12402` (SHA-256
    `b7c9d4c7…0f299`) found no schema deviation. Every rule measure is as
    required: two player tracks, the return last, two scenes, session and
    freeze slots equal to the scenes, one holder per track mixer and none on the
    main and cue mixers, `SendsPre` equal
    to the returns, 66 unique nonzero pointee Ids below `NextPointeeId` 67, and
    no dangling envelope.
  - `fixture_audit.py` found 37 Live Sets, 0 refused, 0 with unknown shapes and
    no addition needed. Every case effect is "consistent".
- Computed cases: none differs from X2 or, where modelled, from the model under
  its comparator. The round-trip margins are at least 0.167 of a step. A
  one-step change of G[3] moves case 051 by 3.7·10⁻⁹. Findings F1 and F2 are
  recorded under `computed_checks`.
- A mutation of one expected entry in each of the 80 cases was caught 80 times.
  Six planted deny-list terms were flagged.
- Evidence identity on 2026-10-18 matched:
  - X2 (12 files; manifest `662481cd…6858b`) and the x86_64 slice `1bae9a97…be999b0`;
  - the T1.1 generator and both checkers against the t11 manifest (`6981daa7…49db2e`);
  - S9, D8 and `Live.arm64`;
  - the released v1 manifest and all 42 of its files.
- In the export copy
  `/tmp/claude-1000/-home-ollie-Documents-sound/5c433942-c5e3-420d-833a-756602393383/scratchpad/export/mixer-values-v2/`,
  `verify` matched all 41 hashes and sizes and resolved all 11 Markdown links
  inside the package. It found no symlink, no missing input, no unused fixture
  and no deny-list hit. An independent hash recheck also passed, and the copy
  is byte-identical to staging. Two consecutive build and seal runs gave the
  same manifest digest.

Not checked: any reference or candidate execution; arm64 equivalence beyond
the X2 slice scan; the macOS libm accuracy assumed by I8 and I9.

## Review gates still required

1. **Scope review**, in a separate context. Check the new clauses and all 43
   computed expectations against X2, and the 37 rebuilt fixtures against the
   v1 edits. Rule on:
   - F1–F6;
   - releasing computed values that have no observation channel in Live
     (clip-launch-v1 RVC-01 removed a clause without an observable; here the
     coordinator directed computed values as such);
   - the 1e-12 bound and the exact round-trip comparison under I8.
2. **Live Set validity.** Confirm that the template set needs no structural
   assumption beyond I10, and that the removed T11-MIN parts are right to
   remove.
3. **Supersession.** Confirm that the carried records are identical, that the
   superseded digest matches and that the change list is complete,
   including every fixture change.
4. **Quality and sanitization review**: exclusions present and in agreement
   in both the spec and the manifest, no internal structure or analyst link,
   no claim beyond static derivation and X.
5. **Evidence identity**: re-hash X2, the slice, the T1.1 files, S9 and D8.
   Re-running X2 needs the harness of ADR 0003; it is optional.
6. **Finalize**: add `REVIEW.md`; set the manifest review and status fields;
   re-seal; verify an isolated export; record the manifest hash in the
   catalog.
7. **Publish** only after approval. Copy the package unchanged to
   `handoff/mixer-values-v2/`. Then update the catalog (mark mixer-values-v1
   superseded), the spec revision table, coverage, the indexes, Q-019 and Q-022,
   and the log. This page has no inbound index link yet.
8. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate. It has 80 cases. 37 carry v1's
partial REQ-MIXER-VALUES-001 to 004 and 006 to 009 on rebuilt fixtures; 43
release partial REQ-005, 013 and 014 as computed values. REQ-010, 011, 012 and
015 are unreleased. It is not published. mixer-values-v1 remains the current
release.
