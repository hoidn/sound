---
id: PLAN-MIX-GRAPH-HANDOFF
type: research
status: current
updated: 2026-10-21
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Mix graph handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [mix-graph-v1](../../handoff/mix-graph-v1/README.md), approved with listed narrowing by a separate review agent ([review record](../../handoff/mix-graph-v1/REVIEW.md)). All 28 cases are released unchanged: 17 computations and 11 composed renders, labelled spec conformance.

- **RMG-01:** REQ-013's interpolated Float value and REQ-014 hold only under the default automation settings. Nothing depends on Q-023, A6 or A7.
- **RMG-02:** the main track's one-event tempo and time-signature envelopes are exempt from the envelope exclusion.
- **RMG-03:** REQ-013's sample-timing sentence is moved out of the released clause.

For the spec author: F1, F2, F3 and F6 hold; objdump confirms that L is 200 for r ≥ 2³¹. REQ-013's interpolation needs a value step in the settings; without one, the value is held. REQ-012's one-event rule conflicts with the T11-MIN envelopes.

## Draft reconciliation (2026-10-19)

Draft r2 applies F1–F6 and review RMG-01 to 03: internal predicate case withdrawn, out-of-range load outcomes ungraded, ramp overflow documented, default/data-step conditions explicit, song-time offset untraced, one-event tempo/meter exemption and narrower send dependencies. The preparation instructions below are the historical staging plan.

## Decision and boundary

Stage a finite first release, mix-graph-v1, from
[SPEC-MIX-GRAPH revision 1](mix-graph.md). The candidate follows the pattern
and gates of the [als-container plan](als-container-handoff-plan.md), the
[transport-state plan](transport-state-handoff-plan.md), the
[midi-config-v2 plan](midi-config-v2-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff). Evidence is the T1.4
packet [t14-mix-v1](../../analysis/ableton-live-12.4.3/r2/t14-mix-v1/manifest.json),
with the pan-law and fader gains of
[x2-mixer-v1](../../analysis/ableton-live-12.4.3/r2/x2-mixer-v1/manifest.json).
No reference execution exists or will exist
([ADR 0003](../decisions/adr-0003-no-reference-execution.md)).

Selection rule, applied clause by clause:

- **Released:** D, S and X clauses with exact values that rest on no unsettled
  [Q-023](../questions.md#q-023-mix-graph-t1-conditions) item.
- **A1 settled:** A1 (render start) is settled for T1 as the
  [ADR 0004](../decisions/adr-0004-target-scope-t1.md#render-conventions)
  render convention. It is released as REQ-011, labelled a project convention.
- **Unsettled, so excluded:** A2, A3, A4, A5, A7 and A8; the single-event
  envelope; the clip-envelope time base.
- **A7:** treated as part of Q-023's send-active item (see F5).
- **Summation order:** handled by the render tolerance.
- **A6:** not a Q-023 item. It is stated in the payload as an assumption
  (REQ-014).

Every U case is excluded. Render cases are released only with the label
"composed render (spec conformance)", stated plainly in the README, the
contract and every render case. ADR 0004 counts whole-mix results as spec
conformance, not measured compatibility.

Each render case has a fixture Live Set and an input signal definition:

- **Fixtures:** built on the T11-MIN rules with
  [make_fixture.py](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/make_fixture.py)'s
  element builders, and checked with that packet's `schema_check.py` and
  `fixture_audit.py` (addendum of the stage brief).
- **No shipped base:** the spec's base document B0, a shipped set, is not used.
- **Signals:** two generated 64-frame 16-bit WAV signals. They are placed at a
  track's mixer-stage input, so clip playback (SPEC-PLAYBACK-CORE, unreleased)
  plays no part. No Ableton audio is shipped.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
compatibility is claimed.

## Scope

| Requirement | Included | Excluded remainder |
| --- | --- | --- |
| 001 | One mixer stage per track; source → devices → mixer; one main and one send output per return; send k and `SendPreBool` k belong to the k-th return by list order; outputs to Main; render output is the main track's main output | More than 12 returns and the thirteenth-`SendPreBool` error; holder gaps and count mismatch (U) |
| 002 | All S clauses | None |
| 003 | Crossfade assignment None, volume not automated: v = g in the stored domain, 0 at or below 0.0003199999919; main the same | A or B assignment (A5); automated volume (A3); out-of-range stored values (F2); main with A/B or `Speaker` false (U) |
| 004 | M_main = m·P (X); the pan law restated from SPEC-MIXER-VALUES r4 REQ-013 (X); w = `PanMode` code, ramps over the fade length (S) | None |
| 005 | Matrix and consequences (X); `SendPreBool` → q, ramp (S); a send at the exact stored minimum contributes nothing (narrowed, F4); s_k to the k-th return | g for other stored values (A4); a_k for `EnabledByUser` true (A7) and false (U); groups |
| 006 | Per-sample sums, binary64 send sums, binary32 main outputs; return mixer; main has no sends | Main-sum order (U; tolerance) |
| 007 | X and S as written, returns included | Main `Speaker` false (U, REQ-003) |
| 008 | X gate table for categories 0–6, as named categories; "no `SoloSink` true → no soloed track" | Category assignment from a set (S, A2); main or cue solo (U); the cue output; type 7 |
| 009 | All S and X clauses; the volume-curve evaluation narrowed to the volume gain | None |
| 010 | 75 samples (X); scope (S); no ramp for unchanged values | Developer option (U); crossfade-assign ramp (with A5); automation ramps (→ 014) |
| 011 | The ADR 0004 convention, without its automation clause | First samples of the original (U) |
| 013 | Point list, 16-piece curve, lookup at envelope time with the later point at a step, segment value, hold, Bool and Enum, all as computations | Song position → envelope time, including the untraced automation offset (F6); which envelope drives (012); units (015); comparison with REQ-AUTOMATION-ENVELOPES-010 (analyst-side) |
| 014 | Ramp length rule, shortening and the transport-stopped clause; A6 and the pan step stated | Volume and send example (A3, A4); r ≥ 2³¹ (F3); smoothing (U) |
| 012, 015, 016 | None | All of it: A8 and U (012); A3 (015); 016's only observable is 012's drive state |

### Case disposition

The 28 release cases are 12 of the 13 X computation cases, 5 new computation
cases (3 of them re-authored from render cases), 2 render cases from the draft
(1 as written, 1 narrowed) and 9 new render cases.

| Draft case | Release case | Change |
| --- | --- | --- |
| MG-001 to 006 | 001 to 006 | As written; multi-part cases as evaluations |
| MG-007 | 007 | Narrowed: solo types 0–6 only, as category names; the cue column dropped |
| MG-008 | Not released | Internal predicates with no released observable (F1) |
| MG-009 to 012 | 008 to 011 | As written |
| MG-031 | 012 | As written |
| MG-032, 033, 034 | 013, 014, 015 | Value parts re-authored as `playback-value` computations at envelope time. The render claim that M's arrangement envelope drives M's pan (A8) is dropped |
| New | 016 | Bool and Enum lookup and the step rule (static-derived) |
| New | 017 | REQ-014 ramp lengths: 200, 2822, 65,536, a flat segment, and a stopped transport (static-derived) |
| New | 018 | Template: main = x_A; sends at their minimum, the return idle |
| MG-029 | 019, 020 | Narrowed to in-range values: stored 2 → 1.99526238, and 0 or −1 → 0.0003162277571 (F2) |
| New | 021, 022 | Silence limit inside the domain: 0.000319 silent, 0.00033 audible |
| MG-030 | 023 | Without A's send, so A4 and A7 are not needed: main = 0.5011872·x_A |
| MG-022 | 024 | Without A's send: pan −1 gives L = 1.4142135·x_L and R = 10⁻⁵·x_R |
| New | 025 | Split Stereo with split pans (0, 0): both outputs 0.70710677·(x_L + x_R) |
| New | 026 | Main sum: x_A + 0.5011872·x_B |
| MG-023 | 027 | As written. Its label names A7, but the expectation needs neither A4 nor A7 (F4) |
| New | 028 | Return switched off while A sends 0.5011872053 to it: main = x_A, independent of A4 and A7 |
| MG-020, 021, 022, 030 (with send) | Not released | A send above its minimum reaching a playing return: A4 and A7 |
| MG-024 to 027 | Not released | Loaded solo: A2 |
| MG-028 | Not released | Crossfade assignment A: A5 (also A4 and A7) |
| MG-035 | Not released | A3, A6, A8 |
| MG-036 | Not released | A7, A8 |
| MG-037 | Not released | A8 |
| MG-038 to 041 | Not released | U |

Draft case IDs do not appear in the payload. The mapping is in
`traceability.json`.

## Findings while staging

These are proposed corrections for a spec revision 2. This page does not edit
the spec.

- **F1. MG-008 grades internal predicates.** Their names come from the X runs,
  and they have no released observable. The case's "speaker ignored for
  {1, 3, 4}" also contradicts REQ-008's own X table: for type 4, the main gate
  equals s (`results/mix.json` `solo.switch_word`: type 4 gives MainOn 0 with
  `Speaker` off and 1 with it on). Proposed: drop MG-008, or restate it as
  behavior that someone can observe.
- **F2. REQ-003's out-of-range consequences omit an assumption.** For a stored
  volume above 1.99526238, or 0, or negative, the consequences assume the value
  is held as written on opening. SPEC-MIXER-VALUES r4 REQ-015 states that
  assumption and marks it U. MG-029 (stored 2, 0, −1) therefore rests on an
  unknown, although it is labelled S-cond (A1) only. Proposed: name the
  condition in REQ-003 and in MG-029.
- **F3. REQ-014's ramp-length formula ignores the 32-bit conversion.** The
  Live x86_64 code at `0x101b39587` is `cvttsd2si %xmm0,%eax` (32-bit), then
  `cmovl` with 0x10000 and `cmovg` with the minimum segment length. When
  r = q/|s| is 2³¹ or more, eax is 0x80000000, so L becomes 200, not 65,536.
  The same code returns the sentinel 1.7976931348623155e308 for a zero slope
  (`0x101b1f3d0`), which turns into "no ramp". Re-read with objdump on
  2026-10-18; the payload excludes r ≥ 2³¹. Proposed: state
  L = 200 for r ≥ 2³¹ (|s| ≤ 9.3·10⁻¹³ per sample at q = 0.002).
- **F4. The A4 and A7 labels are broader than the dependencies.**
  - The assumption table limits A4 to "every R case with a send above its
    minimum". Yet REQ-005's S-cond (A4) clause also carries "a stored send at
    or below 0.0003199999919 contributes nothing". At the exact stored minimum
    the send-curve position is 0 (X2 `gain_to_position`), so g = 0 with or
    without the level node. For stored sends in
    (0.0003162277571, 0.0003199999919], the result holds only under A4. The
    payload narrows the claim to the exact minimum.
  - MG-023's label names A7. Its expectation does not depend on A7 or A4,
    because the send gate 0 zeroes every send entry (MG-004).
- **F5. Q-023 and the spec list different items.** Q-023's gap list omits A6
  and A7. The spec's open questions count "the send-active rule and the
  automation index (A7, A8)" among the unknowns that limit T1. Q-023 lists only
  the `EnabledByUser`-false half of the send-active question. This candidate
  treats A7 as unsettled, because it is the same untraced derivation. Proposed:
  add A7 (and A6, if it is meant to stay open) to Q-023.
- **F6. REQ-013's automation offset is untraced.** REQ-013 defines
  t′ = t − (automation offset), rounded to the grid. The notes record that
  offset as present but untraced for any envelope (`notes-automation.txt`
  §1b, §3), and none of them says that it is 0 for arrangement envelopes.
  MG-032 to 034 assume it implicitly. The release takes envelope time as
  input and leaves the song-position mapping unreleased. Proposed: state the
  arrangement offset as an assumption or trace it.
- **F7. The base document B0 cannot be shipped.** B0 is a shipped Live Set. The
  release rebuilds the render setup on the T11-MIN rules: tracks A, B and R,
  no devices, no clips. The spec's "source" (A's clip launched at beat 0)
  becomes a signal placed at A's mixer-stage input.

## Deliverables

- **Payload:**
  [mix-graph-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/mix-graph-v1/README.md),
  `AGENTS.md`, `spec.md` (contract and comparison convention), `cases.json`
  (28 cases), `fixtures/` (11 Live Set XML documents and
  `signals/x-a.wav`, `signals/x-b.wav`) and a draft `manifest.json`
  (`release_status: candidate-unreviewed`, review pending).
  - The manifest lists 17 payload files; with the manifest itself the package
    has 18.
  - Draft manifest SHA-256:
    `f4b48b1415a358eb48cf3c34bfc606ed10d6b36e620915ea919ad77c36e4e952`.
    Review edits will change it.
- **Analyst side, never shipped:** `mix-graph-v1-analysis/` with
  [build_mg1.py](../../analysis/ableton-live-12.4.3/handoff-staging/mix-graph-v1-analysis/build_mg1.py)
  (fixtures, signals, cases, manifest, cross-check model, structure checks,
  seal and verify),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/mix-graph-v1-analysis/traceability.json)
  and
  [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/mix-graph-v1-analysis/author-validation.json).

## Evidence traceability

The X values are copied at build time from t14 `results/mix.json` and
x2-mixer-v1 `results/mixer.json`. Per-case locators are in
`traceability.json`; the payload contains none of them.

| Release cases | Evidence | Label |
| --- | --- | --- |
| 001–005 | t14 `sends[]`: Live x86 `0x101b40d30`, the twin of engine `TSendVolumes::Calc` `0x171a20`; `notes-q019.txt` 3d–3e | X |
| 006 | t14 `main_switch[]` (`0x101b40cf0`) | X |
| 007 | t14 `solo.switch_word` (`0x101b3fdc0`, `0x101b3ff50`); `notes-solo.txt` | X |
| 008 | t14 `solo.track_fade_time` (`0x101b0ee70`: 75) | X |
| 009, 010 | t14 `ramp_interpolator[]` (`0x101b2b970`, `0x101b2bae0`, `0x101b2ba30`) | X |
| 011 | t14 `volume_panner[]` (setters `0x101b243f0`, `0x101b244a0`; recompute `0x101b27860`); x2-mixer-v1 `pan_law` | X |
| 012 | t14 `automation.E9_polyline.points` (`0x1011f1610`); emission at s = (i+1)/16 in `notes-automation.txt` §1a | X |
| 013–015 | t14 `E9_polyline.played`, `E13_t0`, `E1_linear` (`0x101b1f400`; `subss` then `divsd`, re-read in `x86-disasm.txt`); first time −10⁷ (`0x102823d84`); lookup (engine `0x141110`, pseudocode) | X, S |
| 016 | `notes-automation.txt` §1b lookup, mode 1 | S |
| 017 | `notes-automation.txt` §2; defaults hook `0x10282b410`; ramp length `0x101b39550` (F3) | S (A6) |
| 018–028 | Graph and per-sample notes (`notes-mix.txt`; `0x101b4d870`, `0x101b4c400`); manual volume as position, curve and floor (`notes-q019.txt` 1–2, 5; x2-mixer-v1 `fader.roundtrip_Q019`); pan law (x2-mixer-v1); send at the minimum (`notes-q019.txt` 3a, x2-mixer-v1 `gain_to_position`); switch words (t14); ADR 0004 | Composed |

Evidence identity, re-hashed by `seal` on 2026-10-18:

| Item | SHA-256 | Result |
| --- | --- | --- |
| t14-mix-v1 manifest | `32a2a38b…` | 33 files, all match |
| x2-mixer-v1 manifest | `662481cd…` | 12 files, all match |
| t11-structure-v1 manifest | `6981daa7…` | 74 files, all match |
| Live x86_64 slice | `1bae9a97…` | Matches |
| `Live.arm64` | `3a99ceea…` | Matches |
| Schema `12.0_12402.txt` | `b7c9d4c7…` | Matches |

## Fixture construction and sanitization

`build_mg1.py build` writes every fixture from one template.

- **Template:** assembled with the T11-MIN builders (`mixer`, `track`, `slots`,
  `envelope`, `render`).
  - Tracks: two audio tracks `A` (`Id="1"`) and `B` (`Id="2"`), with two empty
    session clip lists and two empty freeze clip lists each, and a return track
    `R` (`Id="3"`). All output to `AudioOut/Main` and have empty device chains.
  - Main track: as in T11-MIN, with tempo 120, 4/4 and their one-event
    envelopes. The cue track is present.
  - Set level: one `SendPreBool` (`false`), two scenes, the transport, the
    global quantisation values and `CrossfadeCurve` 2.
  - Pointees 1 to 66; `NextPointeeId` 67.
- **Per case:** each fixture changes only the mixer values its purpose names.
  `author-validation.json` lists the changed lines.
- **Validity:** every fixture passes the T11 checks, with no schema deviation,
  no refusal and no unknown shape. That means one player track or more, freeze
  counts equal to session counts, slots equal to scenes, `SendsPre` equal to
  the returns, one holder per return, and unique non-zero pointee Ids below
  `NextPointeeId`.
- **No shipped content:** no shipped file is read into a fixture.
- **Signals:** generated from integer formulas, 300 bytes each.
- **Sanitization:** the payload names only public document element names. The
  deny list covers these, and a probe with planted terms was flagged:
  - analyst paths and addresses;
  - internal and port names (`MainOn`, `SendsOn` and others), which are
    replaced by "main gate", "send gate", "post amount" and "split amount";
  - draft case and assumption IDs, and the fixture names E1, E9, E13, B0 and
    T11;
  - tool names.

## Mechanical checks performed

`build_mg1.py seal` (CPython 3.13.9 `-I -B`) wrote the author validation:

- **Cross-check model:** all 28 cases agree with the model, an independent
  restatement of the released clauses. It covers the pan law, the gates, ramps,
  the polyline, the segment value, the ramp length and a coefficient render of
  each fixture. It shares the evidence and is not an oracle.
- **Exclusion probes:** the model rejects all ten excluded inputs:
  - `SoloSink` true;
  - crossfade assignment A;
  - stored volume 2 or 0;
  - sends at 0.5 or 0.000318 that can reach a playing return;
  - a return send at 0.5;
  - `PanMode` 2;
  - the main switch off;
  - r ≥ 2³¹.
- **Mutation probe:** a mutation of every case was caught.
- **Render comparator:** checked frame by frame on the shipped signals.
- **Package:** hashes and sizes of the 17 listed files match, the inventory
  equals the directory, and every case input and signal exists. There is no
  deny-list hit beyond the forbidden-inputs wording in `AGENTS.md`.
- **Export copy:** in a copy outside the checkout (scratchpad `export/`),
  `verify` matched every hash and resolved all 18 Markdown links. An
  independent hash recheck agreed, and the copy is identical to staging.
- **Determinism:** two consecutive build-and-seal runs gave the same manifest.

Not checked: any reference or candidate execution, A1 to A8, and the arm64
per-sample track-output functions (`fma-scan.txt` names them as not compared).

## Review gates still required

1. **Scope review**, in a separate context.
   - Check every included clause and expectation against the locators.
   - Decide F1 to F6.
   - Accept or reject the treatment of A7 as unsettled, the narrowing of the
     A4 clause to the exact minimum, and the re-authoring of MG-029, 030, 022
     and 032 to 034.
   - Confirm that the computation-only clauses (REQ-013, 014, and the
     gate rows for categories other than unaffected) may be released without a
     render observable.
2. **Comparator decision.** The spec calls the render comparator (10⁻⁵ ×
   max|x|) "proposed, to be decided before grading". The release adopts it.
   The reviewer must accept or replace it. It does not separate the pan law's
   10⁻⁵ floor from silence.
3. **Quality and sanitization review.** Check behavioral completeness and that
   exclusions agree between the contract and the manifest. Confirm that no
   internal structure is present, including in the computation names and the
   category names.
4. **Evidence identity:** re-check the hashes above before release.
5. **Fixture and sharing review** of the 11 Live Sets and two signals,
   including their validity under SPEC-LIVE-SET-STRUCTURE.
6. **Overlap with mixer-values-v2.** That candidate, staged at the same time,
   includes REQ-MIXER-VALUES-013. This package restates the same pan law,
   which matches its wording, for self-containment. If both are released,
   keep the two consistent or replace one by a reference.
7. **Finalize:** add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the catalog.
8. **Publish** only after approval. Copy the package to `handoff/mix-graph-v1/`.
   Then update the catalog, spec status, coverage, indexes and log.
9. An isolated implementation workspace remains unprovisioned.

## Historical staging disposition — 2026-10-18

Staged on 2026-10-18 as an unreviewed candidate: 28 cases (17 computation,
11 render) for partial REQ-MIX-GRAPH-001 to 011, 013 and 014. REQ-012, 015
and 016 are unreleased. It is not published, and no handoff exists for
SPEC-MIX-GRAPH.

## Current disposition — 2026-10-21

The reviewed local [mix-graph-v1](../../handoff/mix-graph-v1/README.md) was released2026-10-18 as the review outcome above records. Its28cases remain current/immutable; the preceding unpublished-candidate statements are historical staging text. [Draft R3](../research/mix-graph.md#mix-owner-r3-finite-annex-adoption--2026-10-21) separately adds25finite native-output observations/seven inheritedreferences, preserving all16bodies/34old rows/released28scope. Portable expectations/comparators remainNULL, with no publicgroup/MainOn/currentreceiver/ARM/calibration law. No new release is selected. Current implementation-workspace status belongs to [project status](../project.md#current-phase); the old unprovisioned statement above records its staging date.
