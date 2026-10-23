---
id: RESEARCH-SAMPLE-INSTRUMENTS
type: research
status: current
updated: 2026-10-20
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


## 2026-10-20: sample-instrument route map v1 (pending review)

The amended revision-4 selector selected one whole-family analyst route map for
Simpler, Sampler and Impulse to extend the retained T1 sample/playback boundary.
The [packet structure](../../analysis/ableton-live-12.4.3/full-spec-v1/family-sample-instruments-routes-v1/structure.md)
and [route ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/family-sample-instruments-routes-v1/route-ledger.json)
are pending Root sealing and independent structure review. No application
behavior, grade, owner clause, case, release or successor execution is adopted.
The earlier pending R3 prose above remains historical; the
[owner-R3 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/sample-instruments-owner-r3-review.json)
and [focused corrected-source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/sample-instruments-source-audit-r2-review.json)
already approve only their stated partial scopes.

All 63 current requirement bodies and all 102 current complete case actions were
freshly read (Simpler 24/39, Sampler 25/42, Impulse 14/21). The map inventories
350 bounded required application predicates, all with no established route and
unknown actual/comparison. It separately records 221 D12 documentary annotations;
these are not exact-12.4.3 S routes or extra outcomes. Its 571 context records,
63 clause IDs and 102 case pointers are different navigation units, not a
whole-product denominator. Numeric input examples, source contexts and helper
metadata do not add predicates. Continuous DSP, malformed-input and state/error
history enumeration remains unresolved.

Source semantics are inherited from the approved corrected 309-context audit,
104 literal resource roles, 33 source groups and six open questions. This map
pins their selected spans and 18 association replacements; it does not claim a
fresh full source-semantic audit or pixel/link-destination inspection. Old
SAMPLER-011 selects layers and edits Detune, with expected chooser display; it
does not invoke the chooser. Old SIMPLER-018 has Warp as in setup and actually
performs half/reset/double; it does not click Warp as. Their new R3 entry cases
remain null. All 61 old requirement objects and 88 old case objects are exact;
14 added null cases cover partial entries in 13 groups, leaving 20 groups open.

The metadata-first census retains the approved exact 32 class prefixes: 93
selected slots from 512 available, 59 stores, 222 aliases and 118 memberships,
and 92 direct-call/57 unresolved-indirect rows. The 16 model prefixes retain
leading three-or-less construction metadata; 16 small prefixes retain their
whole exported prefixes. Neither establishes complete native tables, classes,
functions, constructor roles or public instances. Every selected record has an
exact old-index byte locator and hash. Excluded ASamplerBase, oscillator,
modulation, voice and other type metadata leaves their contract predicates
unknown; exclusion is not native absence. All 57 indirect targets remain
unresolved and native-site credit is zero. No source body or binary/native bytes
were expanded. The 16 small-prefix source frontiers are prospective auxiliary
candidates only, with construction/ABI/legal-state/sample/provider/oracle gates.

Five separate retained-fixture S records establish input-file bytes and fixed
headers, not application routes. Three files are four-second stereo PCM inputs;
the truncated and empty files have no application failure oracle. No waveform
samples were decoded or generated, no ten-second input was silently substituted,
and REX/Pack/hardware remains unprovisioned. SampleRef/schema/preset fields do
not establish media resolution, loaded layer/slot identity or productive audio.
Actual note/control delivery, sample clock/order, held/new voice state,
Warp/slice/cache/algorithm, zone/RR/random state, output taps, Save/undo/cancel and
voice/resource teardown all remain missing joins. Constructed mix ports do not
close instrument-to-host delivery. Corrected Warp v2's untraced notification and
partial-initialization qualifications remain in force.

The [author check](../../analysis/ableton-live-12.4.3/full-spec-v1/family-sample-instruments-routes-v1/author-check.json)
checks pinned providers, clause/case/span identities, selected metadata rows,
fixture-only scope and prefix preservation, with synthetic false-promotion
controls. It is data-only and does not execute an inherited helper, model,
comparator, decoder, provider, harness or original. Independent review is still
required before adopting this packet's route structure; all application grades
and unknown joins remain unchanged.


## Sample-instrument family route review approval — 2026-10-20

Root read/adopted the complete [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-sample-instruments-routes-v1-review.json),SHA256222a1a7c5f0c7cc1d30bca5cc8afe6d3622d133bc14569461256a404f440f9e2. Manifest0058dda3aecd87e65aaabbf7d600b0f654fd395c36e742756d2ef9a94996cdcd binds13payloads/1,989,524bytes. Fresh63fullclauses/350predicate wordings/102full action-control-limit fields preserve all350applicationnone/U,zeroS/X;221D12annotations and five auxiliary fixture-onlyS stay separate. The571contexts are not atomic outcomes. All61oldrequirements/88oldcases remain exact.

Thirty-one pins/580selected rawrows(431metadata+149call-indirect),32tables/93slots/59stores/222aliases/118memberships/118seeds/92calls/57unresolved indirect rows and21negative controls passed. Full309block source semantics remain inherited;18association corrections/geometry checked. Research14,359byte prefix restores date-only;4,694append bytes exact. Four-second input headers prove no application admission/audio/error;longer histories need sufficient admitted source or stayU. Sixteen prospective prefixes establish no executable leaf.

SI-MAP-REVIEW-001 preserves original25,071+24conditional=25,095combined sites,zero sample credit. SI-MAP-REVIEW-002 is filed as [reference erratum](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/sample-instruments-r3-reference-interpretation-erratum.json):old017 stays inactive-loop negative;039 requires its own productive BOTHloops and actual active-loop actions. [Canonical acceptance qualification](../specs/device-sampler.md#r3-acceptance-reference-correction--2026-10-20) changes no case/oracle/grade;frozenR3/map remain exact. Earlier canonical identity checks are as-of before this explicit addendum,not future mutable-page gates. Actual sample/voice/currentcontrol/provider/clock/output/load/Undo/lifecycle stayunknown;no native/original/site/norm/case/release/grade or family/product closure follows.
