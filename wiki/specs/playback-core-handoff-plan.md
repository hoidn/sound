---
id: PLAN-PLAYBACK-CORE-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Playback core handoff: candidate and review plan

## Decision and boundary

This page stages playback-core-v1 as a finite candidate from
[SPEC-PLAYBACK-CORE revision 1](playback-core.md). It is a first release with no
supersession. It follows the [als-container plan](als-container-handoff-plan.md),
the [transport-state plan](transport-state-handoff-plan.md), the
[midi-config-v2 plan](midi-config-v2-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff).

The coordinator named four areas for release: transport play, stop and loop;
Trigger launch timing in samples; MIDI note-on and note-off emission positions;
and unwarped audio read positions. The candidate uses the offline-render framing of
[ADR 0004](../decisions/adr-0004-target-scope-t1.md#render-conventions), including
its settled-start convention. The staging brief's generic rule excludes runtime,
timing and audio-render clauses. This release instruction overrides it, because
ADR 0004 makes render-sample timing a T1 acceptance dimension. **Review gate 1 must
accept that override.**

Every expectation is one of two kinds:

- arithmetic confirmed by extracted execution of the x86_64 code (ADR 0003), with
  a static-derived path;
- static-derived.

Comparison status stays not-run (ADR 0002). The Q-024 unknowns are excluded.
Where the draft accepts P or P + 1, the case lists both samples and accepts
either; the payload states this as an observable comparator.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**.

## Scope

| Requirement | Included (partial) | Excluded remainder |
| --- | --- | --- |
| 001 | spb and bps; song beat from the anchor; anchors at Play, Continue and jump; buffer independence | Tempo-change anchor |
| 002 | P(b) rule, P or P + 1 in its stated class; note-off, then wrap, then note-on at one beat | Song-loop brace order (no case); launch or stop against notes at one beat (U) |
| 003 | Tempo used as binary32 | Limits 20–999; tempo changes and their quarter-beat timing (outside the named scope) |
| 004 | Stated start beat: lattice, negative raised to 0, plays on sample 0 | How Live picks t\* after opening (U); bar-line rule; count-in |
| 005 | Stop holds the beat; Continue re-anchors | Second Stop (U); Play after Stop (REQ-023); user controls (U) |
| 006 | Length at least 1; jump placement and re-anchor; no jump from at or after the end; clip not moved | Start clamp below 0 (no case); loop switched on during play |
| 007 | Press semantics; own, Global and None grid; grid table for values 1–13 | −99 and out-of-range values; other gestures (U) |
| 008 | Press beat; B arithmetic; pre-delay 0 on MIDI and on an audio track with no clip playing | Pre-delay above 0 and the move to B + g (audio crossfade, U); E ≤ t at R (no observable, finding F6) |
| 009 | Activation at B with pre-delay 0; clip start at B | Replaced clip; crossfade audio (U) |
| 010 | No grid: start at the press beat; stopped launch from start beat 0 | Other start beats and the downbeat helper (U); chasing (U) |
| 011 | S, Ls, Le, LoopOn; clip time; passes; note beats per pass; unlooped end | MIDI clips with IsWarped false (U) |
| 012 | On and off beats and velocities; zero length; IsEnabled false | Same-Time drops (no case); overlaps (U); retrigger (no case) |
| 013 | Pass membership; under way at S not started; on at Le never; off at Le own velocity first | Chasing (U) |
| 014 | Wrap cut with velocity 64 at Ls = 0; unlooped end velocity 64 | Cut velocity with Ls above 0; stops; replacing launch; all-notes-off (U) |
| 015 | VelocityAmount 0, deviation 0, probability 1, GrooveId −1: stored velocity and times | Velocity scaling; capability flag (U) |
| 017 | Seconds; transposition; step and 32.32 fixed point; first frame; positions; start sample | StartRelative other than 0 (U); clips starting late |
| 018 | Direct copy at step 1 whatever HiQ; linear with HiQ off | HiQ windowed sinc for 16-bit (U, Q-024); padding (U) |
| 019 | Gain mapping, limits and stated values; mono on both channels; int16 ÷ 32,768 | Other formats (U); gain or pitch changed during play |
| 020 | Fade off: no fade; silence past the last frame | Fade on and its values (U) |
| 016, 021–023 | None | Per-note expression; unwarped end sample and tempo independence (F7); stops (outside the named scope); clips after transport Stop (U parts) |

The 92 cases use 58 generated Live Sets and two generated WAV files:

- **Clock and transport (001–016):** probe clips in MIDI tracks.
- **Launch (017–070):** the 23 CLC presses of PBC-020 to 022, each at
  44,100 Hz and 48,000 Hz. CLC-062 is excluded. The press at t = 4 exactly is
  added, along with PBC-024 at 44,100 Hz only, PBC-025, PBC-026 at both rates,
  CLC-053 and PBC-027.
- **MIDI (071–082):** PBC-040 to 047 without 048, PBC-049 and PBC-050. Two
  cases are new: a note-off exactly at Le, and velocity 63.5.
- **Audio (083–092):** PBC-060 with HiQ on and off, 062, 065, the four PBC-066
  gains and 067 with LoopStart 0.00251. One case is new: a 48 kHz file at
  44,100 Hz.

At 48,000 Hz and 90 BPM, 104 events list two samples.

### Case disposition

The draft's fixtures F1 to F3 are shipped sets, so none could travel. Each case
was rebuilt on a generated set with the same musical content:

- Pulse stands in for "Slide" (eight 0.25-beat notes, loop 0 to 4) on key 60.
- tone48.wav and tone44.wav stand in for the Rim files.

The audio values are therefore new. Each was computed by the X-confirmed kernel
model and cross-checked against the retained runs. The launch and MIDI samples
equal the draft's values; the seal checks this automatically. The traceability
file lists the draft cases that are not released, with reasons:

- tempo changes (PBC-014, 015, 068);
- CLC-062;
- PBC-023 (F3);
- PBC-024 at 48 kHz (F2);
- audio pre-delay and crossfades (PBC-028 to 032);
- clip stops (PBC-048, 080 to 094, 096);
- PBC-095;
- the U cases;
- PBC-061 and 064 (F7).

## Findings while staging

Proposed corrections for a spec revision 2. This page does not edit the spec.

- **F1.** PBC-004 calls tempo 93.33333587646484 "binary32 of 93.3333". It is
  the binary32 value nearest 280/3. The binary32 value of 93.3333 is
  93.33329772949219.
- **F2.** PBC-024's 48 kHz expectation needs a press exactly at song beat 10/3,
  and no request sample gives it at 90 BPM and 48,000 Hz: 32,000 × 10/3 is not an
  integer. Only the 44,100 Hz case is carried.
- **F3.** PBC-023 relaunches a playing clip at beat 8. That is the clip's own
  wrap and note-on beat, a coincidence REQ-002 calls U and says cases avoid. The
  on-line press is carried as CLC-054 at t = 4 instead.
- **F4.** The linear tolerance "2 binary32 ulp (relative)" (REQ-018, Timing and
  state) is not a safe bound where (1 − f)·x_i and f·x_{i+1} nearly cancel. A
  fused operation's error scales with the product, not the result. The candidate
  instead uses 2 ulp of the largest frame magnitude in the window, as an absolute
  tolerance.
- **F5.** For REQ-010 / PBC-026, "starts at R" is the activation. The first
  note-on is a beat event at L(t), placed by REQ-002, so it can be R + 1 in
  general; in the carried cases it is R. The clause should name the observable.
- **F6.** REQ-009's "E at or before t takes effect at R itself" has no
  observable on a MIDI track. There the pre-delay is 0, E = B ≥ t, and notes are
  placed from their beats. With audio and a pre-delay of 0 it coincides with
  P(B) at exact rates. It is not released.
- **F7.** REQ-021 (PBC-061, 064): with Fade off and a region equal to the file,
  the end sample is not visible in the clip signal. The samples after the last
  frame are silent whether or not the clip still plays. A later revision needs
  an observable, for example a following launch, before grading it.
- **F8.** REQ-006 says a clip continues "as if song time had not jumped". The
  mechanism instead shifts the clip's events by the jump and places them from
  the new anchor. The two can differ by one sample when the two ceilings round
  differently. The candidate states the shift rule and asserts that both
  readings agree in every case.
- **F9.** The clock and loop cases (PBC-001 to 016) name "events at beats" and
  jump samples, but nothing in a session render is scheduled at those beats.
  REQ-006's last clause also makes jumps invisible through clips that are
  playing. The candidate observes the clock through probe clips and the jumps
  through presses after them. PBC-007 needs a quantized press: a no-grid probe
  is relative to its own launch.
- **F10.** Q-024 lists "StartRelative other than 0" without saying which clip
  kind. The spec places that unknown in REQ-017 (audio). MIDI StartRelative is
  REQ-011 X, and the candidate releases it (PBC-041). [Q-024](../questions.md)
  should say "audio".
- **F11.** The grid lengths and the boundary arithmetic are SPEC-CLIP-LAUNCH r4
  REQ-015 and 017. clip-launch-v1 left them unreleased. The candidate restates
  them inside REQ-PLAYBACK-CORE-007 and 008 to stay self-contained. Review should
  decide whether a clip-launch revision should also release them under their own
  IDs.

## Deliverables

- **Payload:**
  [playback-core-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/playback-core-v1/README.md),
  `AGENTS.md`, `spec.md` (the contract, render conventions and observables),
  `cases.json` (92 cases), `fixtures/` (58 `.als` and `Samples/` with 2 WAV
  files) and a draft `manifest.json` (`release_status: candidate-unreviewed`,
  review pending). The manifest lists 64 payload files; with itself the package
  has 65. The draft manifest SHA-256 is
  `410f21c75f1add988fb7a86878330f07a741f1716ca60960849c247d84564aaf`. Review
  edits will change it.
- **Analyst side, never shipped:** `playback-core-v1-analysis/` with:
  - [build_playback.py](../../analysis/ableton-live-12.4.3/handoff-staging/playback-core-v1-analysis/build_playback.py)
    (fixtures, cases and manifest meta);
  - `cases_playback.py` (case definitions);
  - `model_playback.py` (the expectation model);
  - `manifest_meta.py` (scope, exclusions and assumptions text);
  - `seal_playback.py` (checks, seal and verify);
  - [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/playback-core-v1-analysis/traceability.json);
  - [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/playback-core-v1-analysis/author-validation.json).

## Evidence traceability

Evidence is the T1.3 run [t13-playback-v1](../../analysis/ableton-live-12.4.3/r2/t13-playback-v1/manifest.json),
manifest SHA-256 `40f57a923afe…d5af`. All 153 files it lists were re-hashed on
2026-10-18 and match. Two other sources were used: the X2 launch results
`r2/x2-notes-launch-v1/results/launch.json` (`b2ef1031…621e`) and the T1.1
structure tools `r2/t11-structure-v1/`. Per-case sources, evidence keys and
assumptions are in `traceability.json`. The payload contains none of them.

| Cases | Draft source | Kept evidence |
| --- | --- | --- |
| 001–008 | PBC-001 to 006 | `transport/results/fire.json`, `sweep.json`, `plus_one_check.json`; the no-grid probe start (REQ-010, S) |
| 009, 010 | PBC-007, 008 | `fire.json`; `stop_resume.json`; the launch boundary as below |
| 011–016 | PBC-009 to 013, 016 | `transport/results/loop.json`; clip shift by the jump (S, both slices) |
| 017–065 | PBC-020 to 022, 024 (CLC-031 to 051, 054, 064) | X2 `launch.json` boundary cases, compared bit for bit; `launch/results.json` (MIDI pre-delay 0); `launch/matching.tsv` |
| 066–070 | PBC-025 to 027, CLC-053 | As above; the no-grid and stopped launch paths (S) |
| 071–082 | PBC-040 to 047, 049, 050, two new | `midi/results/clip-position.json`, `note-events.json`, `cases.json`; priorities, pass and cut rules in `midi/excerpts.jsonl` (x86_64 only) |
| 083–092 | PBC-060, 062, 065 to 067, one new | `audio/results/inc.json` (steps equal), `kernels.json` (the model reproduces T16Lin and T16Non bit for bit), `gain.json` (gains equal); first frame and past-end hold in `audio/corpus-excerpts.jsonl` |

The release's assumptions map to the spec as follows:

- AS-1 is A1, plus the arm64 equivalence of every X result.
- AS-2 is A3.
- AS-3 is A4.
- AS-4 is SPEC-CLIP-LAUNCH A4, the grid anchor 0.
- AS-5 is the glibc `powf` and `exp10f` binding of REQ-017 and 019.

A2 and A5 are not needed. With VelocityAmount 0 the velocity is unchanged
whatever the path, and the candidate has no stop presses.

## Fixture construction and sanitization

`build_playback.py build` imports the T11-MIN helpers of
`r2/t11-structure-v1/make_fixture.py` unchanged. It builds each set on T11-MIN's
rules:

- one MIDI or audio track with matching session and freeze slot lists;
- the main and preview tracks with the one-event tempo and time-signature
  envelopes;
- one scene, the transport, and the global values;
- no devices or return track, which the minimal-set table allows.

Only the explicit values a case needs are added: `LoopIsSongStart`,
`GrooveSettings`, the note attributes, and the audio `HiQ`, `Fade`, pitch and
`SampleVolume`. The gzip header is the shipped and als-container-v1 form
`1F 8B 08 00 00000000 02 13`, not T11-MIN's OS byte 255. That keeps every
fixture inside the released container scope. The WAVs are generated by integer
arithmetic: a sawtooth plus noise from a linear congruential generator, 16-bit
mono, with only a format and a data chunk. Two builds were byte-identical.

The deny list covers:

- analyst paths, addresses, internal and C-library function names;
- spec assumption IDs, case IDs of the draft, Q, ADR and SPEC identifiers;
- shipped file names, tool and harness words.

It has no hits. The only allowed words are "decompil" and "research" in the
forbidden-inputs list of `AGENTS.md`, with the same wording as released
packages.

## Mechanical checks performed

`python3 -I -B seal_playback.py` (CPython 3.13.9, numpy 2.3.1) wrote
`author-validation.json`.

- **Validity.** All 58 sets pass `schema_check.py` with no schema deviation and
  T11-MIN's rule values. `fixture_audit.py` gives 0 refused, 0 contradicted, 0
  not isolating and 0 unknown shapes.
- **Fixture form.** The gzip header and trailer, ASCII and LF, and the envelope
  are correct. Both WAVs are well formed.
- **Cross-check.** The expectations reproduce every draft value they carry:
  - PBC-001 to 008;
  - the jump lists;
  - PBC-020 to 022 at both rates, including the triplets, PBC-024 at 44,100 Hz and PBC-025;
  - PBC-040 to 047, 049 and 050.

  B equals X2 bit for bit. The model reproduces the X steps, gains and kernels.
  Planted changes to a sample, a step and the kernel were all detected.
- **Placement.** Each placement is asserted against the X placement formula at
  six engine counters.
- **Consistency.** Every case requirement is in scope, every released
  requirement has a case, and the spec and manifest requirement, assumption and
  provenance lists agree.
- **Export.** In the copy `/tmp/claude-1000/…/scratchpad/export/playback-core-v1/`,
  `verify` matched all 64 hashes and resolved all 6 links. An independent re-hash
  matched, and the copy is byte-identical to staging.

Not checked: any reference or candidate execution, and any proof of AS-1 to
AS-5.

## Review gates still required

1. **Scope review**, in a separate context.
   - Accept or reject overriding the brief's timing and audio exclusion with the
     ADR 0004 framing.
   - Check every included clause and the 92 expectations against the evidence.
   - Decide F4 (tolerance), F8 (shift rule) and F11 (restated clip-launch
     arithmetic).
   - Confirm the exclusion of tempo changes, stops and crossfades.
2. **Quality and sanitization review.**
   - Check behavioral completeness of the render conventions and observables.
   - Confirm that the exclusions in the spec and the manifest agree.
   - Confirm there is no internal structure: the contract gives arithmetic
     formulas for observable values, which the reviewer must accept as
     behavioral.
3. **Evidence identity:** re-hash the T13 manifest, X2 `launch.json` and the
   program images.
4. **Fixture and sharing review** of the 58 sets and the 2 WAVs.
5. **Finalize:**
   - add `REVIEW.md`;
   - set the review fields, `release_status` and the date;
   - re-run `seal_playback.py`;
   - verify an isolated export.
6. **Publish** to `handoff/playback-core-v1/` only after approval. Then update
   the catalog, spec status, coverage, indexes, Q-024 (F10) and the log.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate:

- 92 cases;
- partial REQ-PLAYBACK-CORE-001 to 015 and 017 to 020;
- 016 and 021 to 023 unreleased.

It is not published, and no handoff exists for SPEC-PLAYBACK-CORE.
