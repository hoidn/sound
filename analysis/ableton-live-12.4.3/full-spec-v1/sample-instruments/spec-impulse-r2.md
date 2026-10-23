---
id: SPEC-DEVICE-IMPULSE
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Impulse sample-instrument behavior

## Scope and evidence rules

Owns `SURF-DEVICE-IMPULSE` in [the product inventory](../research/full-live-coverage-inventory.md).
This is a **partial draft**, not a released contract or a complete instrument family.
Requirements marked **D** describe the captured current Live 12 manual; **U** identifies
an unresolved outcome. Every D clause has **U exact 12.4.3 applicability**. Installed
schema/preset presence corroborates device identity and storage vocabulary only.
No application, original function or candidate was executed.

Canonical analysis and source pins: [sample instruments](../research/sample-instruments.md).
Generic chain/rack editing belongs to [device racks](device-racks.md), media/dependencies
to [project/media workflows](project-media-workflows.md), Set structure to
[live-set structure](live-set-structure.md), marker storage to [warp markers](warp-markers.md),
and automation ownership to [automation envelopes](automation-envelopes.md).
These links assign ownership; they do not resolve an interaction automatically.

## Requirements

### REQ-IMPULSE-001 — Eight sample slots and editing focus (D)

Impulse has eight sample slots, loadable by dragging samples from browser/Session/Arrangement or per-slot Hot-Swap. Delete/Backspace removes loaded sample. Clicking a slot exposes that slot’s parameters. Hover controls offer play, solo, mute and Hot-Swap. Replacement settings retention and multi-drop distribution remain unknown.

Evidence: [manual §31.7.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#sample-slots) (retained HTML line 1040); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-002 — Trigger mapping and editor labels (D)

Default C3 triggers the leftmost slot and remaining slots are mapped across the C3–C4 octave. The manual does not enumerate the six middle pitches; these remain unknown. With MIDI Editor Fold enabled, all eight slot labels appear even for keys without stored notes. Pitch/Scale MIDI effects may transpose/rearrange incoming triggers; those devices own transformation behavior.

Evidence: [manual §31.7.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#sample-slots) (retained HTML line 1040); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-003 — Parameters captured at new notes (D)

Per-sample parameter changes take effect for newly triggered notes, leaving playing notes unchanged; this also applies to those parameters changed by clip envelopes or automation. This clause does not establish the update timing of mute/solo/Link/global controls. Continuous curves and same-timestamp note/control ordering are unknown.

Evidence: [manual §31.7.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#sample-slots) (retained HTML line 1040); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-004 — Reciprocal link of slots7 and8 (D)

Slot8’s Link switch joins slots7/8 so triggering either stops playback of the other. It does not establish choke behavior among other slots. Note-simultaneity order and click suppression are unknown.

Evidence: [manual §31.7.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#sample-slots) (retained HTML line 1040); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-005 — Start, transpose and stretch (D)

Start offsets playback up to100 ms from source beginning. Per-slot Transpose spans±48 semitones and accepts velocity/random modulation. Stretch spans−100%…100%; negative shortens and positive lengthens; Modes A/B select alternate algorithms, with velocity modulation of Stretch. Exact time/pitch transfer, endpoint−100 behavior and random laws are unknown.

Evidence: [manual §31.7.2](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#start-transpose-and-stretch) (retained HTML line 1040); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-006 — Filter and saturation controls (D)

Per-slot filter offers type/Frequency/Resonance and velocity/random frequency modulation. Per-slot Saturator can be enabled/disabled and Drive changes input boost/distortion (saturator-and-envelope). Filter response, nonlinear shape, gain compensation and oversampling are unknown.

Evidence: [manual §31.7.3](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#filter) (retained HTML line 1040); [manual §31.7.4](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#saturator-and-envelope) (retained HTML line 1040); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-007 — Trigger/Gate decay (D)

Per-slot Decay reaches a documented maximum10.0 seconds. Trigger begins decay with the note; Gate waits for Note Off before starting decay. This differs from Simpler’s One-Shot Trigger/Gate envelope. Sample-end truncation, envelope equation and minimum Decay are unknown.

Evidence: [manual §31.7.4](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#saturator-and-envelope) (retained HTML line 1040); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-008 — Per-slot and global controls (D)

Each sample has Pan/Volume; Pan accepts velocity/random modulation and Volume velocity modulation. Global Volume and Transpose act on all samples; global Time controls both stretch and decay (global-controls). Exact global/per-slot composition, units/limits for global Time and whether a global change affects held voices are unknown.

Evidence: [manual §31.7.5](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#pan-and-volume) (retained HTML line 1040); [manual §31.7.6](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#global-controls) (retained HTML line 1040); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-009 — Mixed and individual outputs (D)

An inserted instance feeds its track’s audio chain. Routing can select the overall instrument signal or individual sample slots as sources for other tracks. Source naming, pre/post-fader and mute/solo effects on separate outputs, channel layout and latency belong to unresolved routing interaction; no sum identity or duplicate-feed law is inferred.

Evidence: [manual §31.7.7](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#individual-outputs) (retained HTML line 1040); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-010 — Persistence and dependent media (U)

Exact save/reopen restoration of device modes, layer/slot assignments, markers, modulation, voice options and external media references is unknown. Stored fields in shipped content do not prove writer coverage, crash recovery or reload equivalence. Generic Set/media container behavior remains with live-set-structure.md and project-media-workflows.md.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-011 — Undo and redo (U)

Undo grouping, restoration of device/sample settings, marker/layer edits, generated files, conversion and routing changes are unknown. No promise of file deletion or resurrection is derived from a non-destructive operation.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-012 — Malformed or unavailable sample failure (U)

Acceptance of corrupt/truncated/unsupported audio, zero-length or missing samples, dependency resolution, out-of-range imported controls and failed allocation is unknown. No silence/no-crash or atomic rollback promise is invented.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-013 — Cancellation and voice teardown (U)

Cancel during sample replacement/import/conversion and remove or bypass while held notes play: resource cleanup, voice tail, pending-note handling and state restoration are unknown. Sample-rate changes, transport stop/restart and device reset have no established output oracle here.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-IMPULSE-014 — DSP, scheduling and modulation fidelity (U)

Interpolation, filter/warp/stretch/saturation equations, gain/pan curves, modulation sums, random sequences, denormal/overload handling and sample-accurate note/control order are unknown. No numeric audio-error tolerance, performance bound or exact12.4.3 parity follows from manual descriptions.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

## Timing, state and comparison rules

Use fresh device state for each scenario; explicitly pin edition, mode, source hashes,
engine/sample rate, tuning, note duration and routing. MIDI note names use the manual’s
C3 convention; no numeric-note alias is inferred. Time/frequency/cent/semitone units
are those named in each clause. “Before/after” describes causal order, without an
invented audio-block latency. Endpoints and values are exact displayed choices;
float/audio comparisons require a separately supported tolerance. No sample-exact
DSP or timing oracle is supplied.

[Fixture definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/fixtures.json)
pin three synthetic stereo PCM files with separated source bands. Their hashes and
known segment order identify test inputs, never Live output. `state` means compare
named visible states/counts/values exactly; `source-identity` distinguishes loaded
layers/regions, refusing ambiguous observations; `presence` tests only the named
continuation/termination or independence predicate, never waveform equality.
`unknown` records an observation without a pass/fail oracle. Cases with unavailable
third-party/official-Pack input stay unexecuted. All cases are plans and have not run.

## Acceptance cases

The [frozen case index](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/cases.json)
also retains requirement, every supporting source anchor/section/HTML line, fixture and execution status per case.
All D expectations remain version-uncertain for the pinned target; all U cases are ungraded.

| Case | Requirement | Kind | Setup and action | Expected result / comparator |
| --- | --- | --- | --- | --- |
| IMPULSE-001 | REQ-IMPULSE-001 | positive | Empty Impulse. Load segmented.wav in slot 1 and layer-b.wav in slot 8; click each. | Eight slots exist; selected parameters follow clicked slot. / state |
| IMPULSE-002 | REQ-IMPULSE-001 | positive | Slot1 selected and loaded. Delete using platform Delete/Backspace. | Selected slot loses its loaded sample; other slots are retained. / state |
| IMPULSE-003 | REQ-IMPULSE-002 | positive | All eight slots loaded with named samples, default upstream MIDI. Play C3; inspect folded MIDI Editor on an empty clip. | C3 triggers leftmost sample; all eight slot labels displayed under Fold. / source-identity |
| IMPULSE-004 | REQ-IMPULSE-002 | boundary | All slots loaded. Send all integer pitches C3 through C4 separately; record slot identity. | Mapping of middle pitches is a required unknown; record only, no invented diatonic map. / unknown |
| IMPULSE-005 | REQ-IMPULSE-003 | positive | Long sample sustaining from slot 1; per-slot Transpose=0. Change per-slot Transpose to+12; trigger another note. | Existing note retains old sample settings; new note takes+12. / source-identity |
| IMPULSE-006 | REQ-IMPULSE-004 | positive | Long samples in slots7/8; Link on. Trigger7 then 8, then 7 again. | 8 stops7; following7 stops8. / presence |
| IMPULSE-007 | REQ-IMPULSE-004 | negative | Same setup with Link off. Trigger7 then 8 before7 ends. | Link imposes no mutual stop while disabled; other voice-limit behavior ungraded. / presence |
| IMPULSE-008 | REQ-IMPULSE-005 | boundary | Selected loaded slot. Set Start 0 then 100 ms, Transpose−48/+48, Stretch−100/+100; inspect modes. | Documented endpoints and Modes A/B available; exact DSP at boundaries ungraded. / state |
| IMPULSE-009 | REQ-IMPULSE-006 | positive | Loaded slot selected. Inspect filter modulation fields and toggle Saturator. | Frequency has velocity/random controls; Saturator has on/off and Drive controls. / state |
| IMPULSE-010 | REQ-IMPULSE-007 | positive | Long sample, Decay1 seconds, Gate. Hold note1 seconds then release. | Gate delays decay until release; Trigger comparison starts decay on note start. / presence |
| IMPULSE-011 | REQ-IMPULSE-007 | boundary | Selected slot. Set Decay to10.0 seconds. | 10.0 seconds maximum is selectable. / state |
| IMPULSE-012 | REQ-IMPULSE-008 | positive | Two slots loaded, one selected. Inspect selected Pan/Volume modulation and global controls. | Pan has velocity/random, Volume velocity; global Volume/Transp/Time are distinct from selected-slot controls. / state |
| IMPULSE-013 | REQ-IMPULSE-009 | positive | Impulse on MIDI track; separate audio track destination. Inspect available input sources for that instrument. | Overall instrument and individual sample-slot output sources available; bus timing and level comparator unknown. / state |
| IMPULSE-014 | REQ-IMPULSE-010 | persistence | Impulse configured with all applicable sample assignments and nondefault controls; retain original hashes. Save Set/preset, close and reopen with media available; repeat after moving one dependency. | Unknown — collect observations; no graded expected outcome. / unknown |
| IMPULSE-015 | REQ-IMPULSE-011 | undo | Impulse with documented sample state snapshot. Perform one sample/layer/marker edit as applicable, undo, redo; record control state and source-file hashes. | Unknown — collect observations; no graded expected outcome. / unknown |
| IMPULSE-016 | REQ-IMPULSE-012 | malformed/failure | Impulse loaded with valid segmented.wav; retain complete state snapshot. Try truncated WAV, empty file and deleted dependency separately; also inspect a zero-width sample/zone region where applicable. | Unknown — collect observations; no graded expected outcome. / unknown |
| IMPULSE-017 | REQ-IMPULSE-013 | cancellation/teardown | Impulse with an actively held long sample and original dependency hashes retained. In separate runs cancel a load, remove device during sustain, stop/restart transport and change engine sample rate; record outputs and media state. | Unknown — collect observations; no graded expected outcome. / unknown |
| IMPULSE-018 | REQ-IMPULSE-014 | audio/timing | Impulse with retained fixtures, explicit 48kHz engine and event schedule. Render documented modes, repeat under different block/rate/event alignments and compare retained outputs only after an original-derived oracle exists. | Unknown — collect observations; no graded expected outcome. / unknown |

Negative/boundary cases are included where a documented constraint supports an oracle.
Malformed, cancellation, teardown, persistence and undo cases are present but ungraded.
Unsupported controls, note-zero semantics, edge ties and resource exhaustion cannot
receive a pass from this packet. No case kind is treated as covered merely by naming it.

## Open questions and analyst evidence appendix

See [unresolved interactions](../research/sample-instruments.md#unresolved-interactions)
for exact-build parity, audio/timing, media, lifecycle and routing gaps. These are
required unknown outcomes, not authorized exclusions from full Live coverage.
The [source manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/sources.json)
pins current manual bytes/date/URL and original shipped schema/presets. The manual
heading map links each D clause to its retained section. Static field names impose
no candidate layout, enum value or processing architecture.

## Revision and handoff

Revision 2, 2026-10-19: qualified Sampler loop-end behavior, active modulation controls and exact cross-section evidence locators. Revision 1 remains archived with its original manifest and payloads.
Independent review is required. No handoff or candidate compatibility result exists.
