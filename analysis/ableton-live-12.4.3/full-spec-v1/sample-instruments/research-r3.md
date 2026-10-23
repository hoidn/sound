---
id: RESEARCH-SAMPLE-INSTRUMENTS
type: research
status: current
updated: 2026-10-19
access: analysis
target: Ableton Live 12 Suite 12.4.3
revision: 3
---

# Sample instruments: Simpler, Sampler and Impulse

## Authority and bounded result

The [full coverage design](full-live-specification-design.md) and
[inventory](full-live-coverage-inventory.md) assign each native instrument an
observable behavioral owner. This packet authors partial drafts for
[Simpler](../specs/device-simpler.md), [Sampler](../specs/device-sampler.md) and
[Impulse](../specs/device-impulse.md). It does not close any device profile.

| Draft | Requirements | D clauses | U clauses | Planned cases |
| --- | ---: | ---: | ---: | ---: |
| Simpler | 23 | 18 | 5 | 35 |
| Sampler | 24 | 19 | 5 | 35 |
| Impulse | 14 | 9 | 5 | 18 |
| Total | 61 | 46 | 15 | 88 |

**D** means documented in a pinned current Version 12 manual capture. All 46 D
requirements have **unknown exact 12.4.3 applicability**; none is S/X execution
evidence. There are 72 D case predicates and 16 ungraded U case entries (the 15
lifecycle/audio gap cases plus Impulse's unresolved middle trigger-note map).
All 88 are unexecuted; no compatibility pass follows from writing them. Some D
clauses contain explicitly narrower unknowns and multiple behaviors; the case
count does not imply every subclause already has a separate scenario.

The retained [case index](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/cases.json)
and [requirements index](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/requirements.json)
are packet snapshots, not competing canonical specs. Root owns shared indexes,
coverage, open questions and the append-only analyst log.

## Source identities and method

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/sources.json)
records five source identities and exact capture time/path/byte count/hash.
The bounded [capture script](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/capture.py)
uses standard-library HTML/gzip/XML parsing and reads three inventory-selected
shipped presets. No original code, instrument, patch or Live process was run.

| Source | Pin / exact locator | Limit |
| --- | --- | --- |
| `SAMPLE-INSTRUMENTS-MANUAL` | [Official instrument chapter](https://www.ableton.com/en/live-manual/12/live-instrument-reference/), captured `2026-10-19T20:27:58.247940+00:00`; 618,718 bytes; SHA-256 `3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a` | Current Version 12, no patch-level claim |
| `SAMPLE-INSTRUMENTS-SCHEMA` | Installed `Contents/App-Resources/Schema/12.0_12402.txt`; 441,285 bytes; SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299` | Stored vocabulary; no reader, writer or DSP proof |
| `SAMPLE-INSTRUMENTS-PRESET-SIMPLER` | `Defaults/Dropping Samples/On Device View/Sample on Device View Default.adv`, `/Ableton/OriginalSimpler`; SHA-256 `a309c8fc6eea1591997e4ee2cca3da98075ef140116cc370207508d9b9aec189` | Empty historical sample-on-drop default |
| `SAMPLE-INSTRUMENTS-PRESET-SAMPLER` | `Defaults/Instruments/Sampler.adv`, `/Ableton/MultiSampler`; SHA-256 `7d1eb5950125579568f3abff3650b1813705c0f4fb47013e7c790a999b15c068` | Empty historical instrument default |
| `SAMPLE-INSTRUMENTS-PRESET-IMPULSE` | `Devices/Instruments/Impulse/Impulse 606.adv`, `/Ableton/InstrumentImpulse`; SHA-256 `e1ce3a8350df64827be822abeda1cf78a455c390b962cc8b2e702aef9b20f195` | Eight stored sample references; no playback observation |

All three preset Creator fields say `Ableton Live 12.4d1`, Revision
`42bc084cd8152e4fb737ef3fefd04b2bea5320e7`. They are content carried by the
12.4.3 package, not sessions observed running that build. Exact compressed bytes,
decompressed XML and [preset observations](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/preset-observations.json)
are retained. The empty Simpler/Sampler examples cannot corroborate actual
multisample dependencies, saved zones or loaded slices. This limitation is
retained rather than widening the scan without a concrete question.

Exact [manual HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-instruments-2026-10-19.html),
[derived text](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-instruments.txt)
and [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json)
give heading anchors, titles and original HTML line numbers. The source is
minified in places, so several headings share a line; anchors disambiguate them.

## Observed storage vocabulary

Observed [schema fields](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/schema-fields.json)
retain nine relevant class declarations. All line numbers below refer to the
retained schema bytes, not mutable wiki pages.

| Class / line | Observed fields | Meaning and limitation |
| --- | --- | --- |
| `InstrumentImpulse`, 3106 | Eight indexed slot families, `TabSample.0`–`.7`, `LinkVoices7and8`, `GlobalVolume/Time/Pitch` | Supports slot/control vocabulary; no MIDI-note map, latch timing or link audio oracle |
| `MultiSamplePart`, 5198 | Key/velocity/selector ranges, root/detune/pan/volume, sample start/end, sustain/release loops, sample reference, slice/warp fields | Declared shared storage does not make every field user-accessible in both devices |
| `MultiSampler`, 5235; `OriginalSimpler`, 5857 | Player/Pitch/Filter/Shaper/VolumeAndPan/AuxEnv/Lfo/AuxLfos/MIDI destinations/Globals/ViewSettings/SimplerSlicing | Presence establishes schemas and stored control families; no equivalence or signal path |
| `SampleLoop`, 6843 | Start/End/Mode/Crossfade/Detune | Enum meanings and valid intervals are not proven by names |
| `SampleRef`, 6850 | FileRef and sample metadata | Dependency vocabulary; no resolution, reload or failure behavior |
| `SampleWarpProperties`, 6862 | Warp markers/mode/parameters/onsets/beat grid | Marker storage stays with [warp markers](../specs/warp-markers.md); no stretch algorithm here |
| `ZoneRange`, 8759; `ZoneSettings`, 8765 | Min/Max/CrossfadeMin/CrossfadeMax; key/velocity ranges | No inclusive-edge, fade-curve or accepted-import law follows |

No schema field is promoted into a behavioral requirement solely because it is
present. The retained Impulse preset has eight `SampleRef` elements. Their file
references are evidence of dependencies, not proof that those files exist,
resolve correctly or decode into the described sample.

## Documented distinctions preserved by the drafts

The manual locators are §31.7 `#impulse` (HTML line 1026), §31.10 `#sampler`
(1500) and §31.11 `#simpler` (1942); each requirement links the narrower heading.

- Simpler's modes, slice edits, warped clip import, voice stealing, sample
  replacement and non-destructive copy operations receive separate predicates.
  Warp mode names and “constant power” never become invented numerical algorithms.
- Sampler's eligibility combines key, velocity and selector zones. Changing the
  selector affects later triggers and does not switch a held voice. Global
  Reverse does not generate a file, unlike Simpler's Reverse command. Link
  retains the previous Sample Start value while substituting Loop Start.
- Current manual Sampler Round Robin clauses are useful D requirements, with
  specific Forward/Backward/Other predicates. The section's target-build
  applicability, reset state, unequal-zone interaction and single-layer Other
  behavior remain unresolved. A control name in another source would not settle
  all of those outcomes.
- Impulse's per-sample parameter changes are latched for later notes, including
  automation. This is not generalized to every global, mute, solo or Link
  control. Its Gate begins decay at Note Off; Simpler One-Shot Gate instead
  starts Fade Out then. The eight-slot mapping is not filled in from recollection.

These are documented facts/constraints, with target-version uncertainty. No
inference of sound-equivalence between the instruments is part of the packet.

## Unresolved interactions

These local labels let root route the gaps into the shared question register;
they are not separately assigned global question IDs.

| Gap | Affected requirements and required outcome | Missing evidence |
| --- | --- | --- |
| Exact-build parity | Every D requirement; notably Sampler RR | Target-specific control/reader/native behavior corroboration, not product name alone |
| DSP and clocks | Final U requirement of every draft; Simpler warp/filter/LFO, Sampler modulation/interpolation/loop fades, Impulse stretch/filter/saturation | Original-derived audio/timing oracle with justified tolerances; random seed/distribution and event ties |
| Persistence/media | Simpler019, Sampler020, Impulse010; dependencies, generated copies, conversion | Device writer/load behavior and roundtrip/error predicates; generic [media owner](../specs/project-media-workflows.md) does not close instrument restoration |
| Undo/redo | Simpler020, Sampler021, Impulse011 | Atomic edit grouping, restored values, generated-file lifecycle and conversion ownership |
| Failure/cancel/teardown | Simpler021–022, Sampler022–023, Impulse012–013 | Corrupt/missing/empty input, resource exhaustion, interrupted replacement and held-voice cleanup |
| MPE/tuning/automation | Simpler013–015, Sampler014/018, Impulse003 | Source combination, mapping/control timing, tuning exceptions and note-off interactions; storage fields alone insufficient |
| Routing | Impulse009 and parent rack/device host | Per-slot source names, mono/stereo topology, pre/post-fader, mute/solo, sends and latency |
| Boundaries | Simpler003/007–009; Sampler002–006/009–010; Impulse002/005 | Zero-width/crossed intervals, slice-note overflow, endpoint inclusivity, loop note-off ties, eight-slot complete note mapping |

Arrangement/Session affect sample input selection and upstream clip automation;
selection/focus affects the edited layer/slot; transport/tempo affects warped
playback, beat envelopes and RR reset; routing selects destination tracks. Their
canonical contracts remain linked rather than copied. Permission errors and
platform Finder/Explorer differences stay unknown except the documented
official-Pack reveal-command restriction. No platform was executed.

## Fixtures, validation and review

The [fixture ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/fixtures.json)
pins three analyst-created 4-second, stereo, 48kHz PCM16 WAVs: segmented 220/330/440/550Hz
seconds, constant 660Hz and constant 880Hz. These identify source layers/regions;
they are not captured outputs. External REX/official-Pack prerequisites are
explicitly absent rather than silently claimed as supplied fixtures.

The [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/validate.py)
checks source hashes/lengths, anchor/line identity, schema declarations, gzip/XML,
sample counts, fixture format/hashes, case/requirement references, metadata,
relative links and frozen snapshots. The
[author validation report](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/validation-author-r2.json)
records the actual static check results. The
[frozen author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manifest-author-r2.json)
pins revision 2 draft snapshots and current packet payloads. The original revision 1
manifest and all 28 original payloads are retained under `revisions/r1/`; its manifest
SHA-256 remains `277da7d53e395b45bf9d58ea803636d79002e20101163ec244f20a9ce100cf4b`. It proves retention and structural consistency, not behavior.

Independent revision 1 review requested three corrections, now addressed for focused revision 2 review. The [review response](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/review-response-r2.json) records the changes. Sample End termination is now explicitly unlooped-only; the selected sustain/release-loop cases retain their existing predicates. The unlooped-end subclause remains outside this finite case selection. Two negative modulation cases now override neutral fixture defaults with active paths and positive controls; ambiguous controls produce unknown. Requirements and case metadata retain every supporting sibling-section locator, including the separate Gain/Volume evidence without inferring sample-Gain/filter order.

Independent focused review is pending. No handoff, publication, implementation or
original-versus-candidate comparison has occurred. Full-family completeness is
not claimed; root integrates the shared catalogs and review result.

## Bounded owner revision 3

The [full 309-block source audit correction](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments-source-audit/README-r2.md) passed [focused independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/sample-instruments-source-audit-r2-review.json). SISA-REVIEW-001/002 distinguish expected chooser display and Warp-as setup from actual invocation. Original audit and owner bytes remain preserved.

The [owner R3](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/README-r3.md) adds two manual-derived UI clauses and 14 concrete selected histories across 13 source-audit groups. All 61 old bodies and 88 old objects remain exact. There are 63 IDs and 102 planned cases; all new documentary pairs and all current actual pairs are null/U/unexecuted. Explicit actual chooser and Warp-as operations, unlooped-only End termination, loop exceptions, productive modulation/voice paths and Impulse control-source/route histories prevent setup/display/silence from becoming proof.

[Adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/adoption-r3.json) distinguishes this bounded subset from the source audit historical zero-adoption freeze. Twenty proposal groups have no new cases here; even selected groups retain unadopted actions. External REX/Pack/hardware prerequisites remain absent. Current-version overlays preserve original historical expectations without promoting them to measurements. R3 independent semantic review is pending; lifecycle, DSP, exact target, numeric tolerances and full-family closure remain unresolved.
