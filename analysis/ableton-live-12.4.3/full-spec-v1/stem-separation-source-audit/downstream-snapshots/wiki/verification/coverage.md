---
id: VAL-COVERAGE
type: coverage
status: planned
updated: 2026-10-19
access: analysis
---

# Whole application verification coverage

The [feature map](../specs/feature-map.md) defines the current planning scope.
A bounded ecosystem draft and a finite configuration release exist; all
families remain unimplemented and unverified. This
matrix is an analyst view; the implementer has a separate mapping of released
requirements to candidate code and tests.

Since 2026-10-18 no run of the whole reference application is possible
([ADR 0003](../decisions/adr-0003-no-reference-execution.md)). "Not run" for reference comparison is
therefore permanent, and the probe IDs in the last column will not run as
planned. Each probe's question is re-routed to extracted execution of original
x86_64 functions, to static investigation, or to a permanent unknown.

| Feature ID | Spec/handoff | Implementation | Verification | Next evidence |
| --- | --- | --- | --- | --- |
| FEAT-TRANSPORT | Draft [transport state](../specs/transport-state.md) r5; [transport-state-v3](../../handoff/transport-state-v3/README.md) (33 cases); [playback-core-v1](../../handoff/playback-core-v1/README.md) (92 finite cases) | Not started | Unknown; released expectations have not been compared with a candidate or Live | Remaining playback/launch clauses and host timing; Q-024 |
| FEAT-SESSION | Partial [Session grid/scenes](../specs/session-view-workflows.md)29 requirements/40 cases, corrected partial scope independently reviewed; draft [clip launch](../specs/clip-launch.md) r5 (64 case IDs); [clip-launch-v2](../../handoff/clip-launch-v2/README.md) (100 cases); partial launch computations in playback-core-v1 | Not started | Unknown; reference/candidate comparison not run | Global-grid condition A4, launch modes, Legato, velocity and follow actions |
| FEAT-ARRANGEMENT | Partial [Arrangement editing](../specs/arrangement-editing.md) draft: 35 requirements/65 scenarios, separately reviewed documentary scope | Not started | Unknown; no application comparisons; build parity U | Exact editing boundaries, undo/cancel/failure and post-edit persistence |
| FEAT-AUDIO | Draft [mixer values](../specs/mixer-values.md) r5 and [mix graph](../specs/mix-graph.md) r2; [mixer-values-v2](../../handoff/mixer-values-v2/README.md) (80 cases); [mix-graph-v1](../../handoff/mix-graph-v1/README.md) (28 cases) | Not started | Unknown; reference/candidate comparison not run; exact stored silence boundary remains ungraded | Conditional routing/automation paths, sample ramps and unresolved mixer boundaries; Q-023 |
| FEAT-MIDI | Draft [note storage](../specs/midi-note-storage.md) r4 (75 case IDs); [midi-note-storage-v2](../../handoff/midi-note-storage-v2/README.md) (72 cases); finite MIDI computations in playback-core-v1 | Not started | Unknown; reference/candidate comparison not run | Recording, note state, expression and unreleased scheduling cases |
| FEAT-AUTOMATION | Draft [automation envelopes](../specs/automation-envelopes.md) r5 (33 case IDs); [automation-envelopes-v2](../../handoff/automation-envelopes-v2/README.md) (21 cases) | Not started | Unknown; reference/candidate comparison not run; segment values do not establish ramped samples | Discarded/missing/empty envelope outcomes, interpolation domain and playback interaction |
| FEAT-DEVICES | Draft [bundled parameters](../specs/bundled-device-parameters.md) r3; [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md) (82 cases); five finite audio packages below; [host draft](../specs/bundled-device-hosting.md): 23 application cases U, three synthetic arithmetic cases only | Not started | Unknown; retained-reference self-comparisons validate comparison tools only | Live-side protocol/mapping, general device behavior; Amp/Cabinet blocked by user choice; Q-025/Q-026 |
| FEAT-RECORDING | Partial [recording/comping](../specs/recording-comping.md) draft: 32 requirements/81 scenarios, 65 documentary/4 artifact/12 U | Not started | Unknown; all 77 application cases ungraded for exact 12.4.3; artifact audits are not recording tests | Build applicability, timing, Capture heuristics, take identity, undo, files and failures |
| FEAT-RACKS | Partial [device racks](../specs/device-racks.md): 28 requirements/61 cases | Not started | Unknown; no runtime tests; documentary exact-build applicability U | Macro numerical semantics, routing/audio/lifecycle and malformed-state gaps |
| FEAT-MIDI-EDIT / FEAT-MIDI-TOOLS | Partial [editor and 17 tools](../specs/midi-editing-tools.md): 43 requirements/57 cases | Not started | Unknown; all target cases ungraded | Source conflicts, numerical/random/undo behavior and nonempty generator fixtures; MPE/tuning/grooves separate |
| FEAT-AUDIO-TO-MIDI | Partial [audio-to-MIDI conversion](../specs/audio-to-midi.md):14 requirements/29 cases, corrected partial review approved | Not started | Unknown;17 documentary/12null-U, all target-U/unexecuted | Plan/count/marker/recognition laws, input/result fixtures, exact-build and lifecycle gaps |
| FEAT-MPE / FEAT-TUNING / FEAT-GROOVES | Partial [MPE](../specs/mpe-workflows.md), [tuning](../specs/tuning-systems.md), [grooves](../specs/groove-workflows.md): 53 requirements/83 cases, corrected partial scope reviewed | Not started | Unknown; 52 documentary proposals and31 U, all 83 exact-target U/unexecuted | Codec/channel, parser/tuning math, groove RNG/numeric/commit and lifecycle gaps |
| FEAT-PROJECT-MANAGEMENT | Partial [project/media workflows](../specs/project-media-workflows.md): 22 requirements/34 scenarios | Not started | Unknown; documentary criteria only, no file-operation/application tests | Exact-build applicability, search/merge/remapping, format and failure/cancel/recovery gaps |
| FEAT-MEDIA-FILES | Partial [media workflows](../specs/media-file-workflows.md): 17 requirements/32 cases, reviewed; citation/count corrections confirmed | Not started | Unknown; all target cases unexecuted, no codec/cache/ASD operations performed | Source/case review, exact-build, input grammars, algorithms and error/cancel/undo/teardown outcomes |
| FEAT-RENDER | Reviewed partial [audio/video export](../specs/audio-video-export.md): 23 requirements/34 scenarios | Not started | Unknown; documentary predicates only, no render/application execution | Exact-build applicability, PCM/video combinations, resampling/dither/normalization, output bytes and failure/cancel/teardown |
| FEAT-NATIVE-MIDI-EFFECTS | Partial [eight MIDI effects](../specs/native-midi-effects.md): 27 requirements/146 cases; corrected revision independently reviewed | Not started | Unknown; 54 documentary predicates and 92 U cases, all 146 target outcomes U | Algorithm/timing/persistence/lifecycle, manual-version applicability and further evidence closure |
| FEAT-SAMPLE-INSTRUMENTS | Partial [Simpler](../specs/device-simpler.md), [Sampler](../specs/device-sampler.md), [Impulse](../specs/device-impulse.md): 61 requirements/88 cases, corrected partial drafts reviewed | Not started | Unknown; all exact-target cases U/unexecuted; synthetic inputs do not prove output | Version applicability, voice/sample/zone/routing/DSP and lifecycle gaps |
| FEAT-DELAY-REVERB | Partial [seven delay/reverb devices](../specs/delay-reverb-devices.md):92 requirements/149 cases, corrected partial scope reviewed | Not started | Unknown; no target/output comparisons; 77 documentary/7 file-only/65 null-U cases | Source/case review, feedback/delay/kernel/random/transition/latency and lifecycle/build gaps |
| FEAT-DISTORTION | Partial [nine distortion devices](../specs/distortion-devices.md):67 requirements/190 cases, corrected partial scope reviewed | Not started | Unknown;29 documentary/18file-only/143null-U, all target-U | Transfer/drive/oversampling/normalization/aliasing/RNG and lifecycle/build gaps |
| FEAT-MODULATION-PITCH-LOOP | Partial [ten modulation/pitch/loop devices](../specs/modulation-pitch-loop-devices.md):106 requirements/186 cases, partial scope reviewed | Not started | Unknown;46 control/9 state/41 signal/90 lifecycle proposals, all exact-target null/U/unexecuted | Individual mode/negative branches, algorithms/clock/RNG/MIDI codec/voice and lifecycle/build gaps |
| FEAT-SYNTHESIS-INSTRUMENTS | Partial [five synthesis/drum instruments](../specs/synthesis-instruments.md):109 requirements/154 cases, partial scope reviewed | Not started | Unknown;42 controls/16 state/46 signal/50 lifecycle proposals, all exact-target null/U/unexecuted | Operator/Meld context questions, DSP/voice/MPE/tuning and lifecycle/build gaps |
| FEAT-EXTERNAL-HARDWARE | Partial [External Audio Effect/Instrument](../specs/external-hardware-devices.md):24 requirements/56 cases, corrected partial scope reviewed | Not started | Unknown;20documentary/10signal/26lifecycle proposals, all target-null/U/unexecuted | Physical/plugin path calibration, codecs/gain/phase/metering/compensation and lifecycle gaps |
| FEAT-LEGACY-DEVICES | Reviewed partial [eight legacy profiles](../specs/legacy-native-devices.md):77 requirements/178 cases | Not started | Unknown;45D11source-content/8file checks/125U; every exact-target expectation null | Target-version/control/migration/behavior mapping, DSP and lifecycle; D11 source checks are not target tests |
| FEAT-CLIP-VIEW | Reviewed partial [Clip View](../specs/clip-view-workflows.md):54 requirements/62 cases | Not started | Unknown; all target-null/U/unexecuted; no media, UI or sample operations | Per-mode branches, Q029sourcecontexts, parsing/numeric/timing/audio/file transaction and lifecycle/build gaps |
| FEAT-MAX-HOST | Partial [Max host/five templates](../specs/max-for-live-hosting.md):38 requirements/64 cases, corrected partial scope independently reviewed | Not started | Unknown;22documentary/5file/37U proposals, all target-null/U/unexecuted | Supported Max/API/patch versions, identity/save/dependency/I/O/clock and lifecycle gaps |
| FEAT-MAX-DEVICES | Partial [twenty Max devices](../specs/max-for-live-devices.md):135 requirements/315 cases, partial scope reviewed | Not started | Unknown;88current/7dated documentary,20file,200U proposals; all target-null/U/unexecuted | Dated-source applicability, modulation/MIDI/DS DSP, public API and lifecycle/build gaps |
| FEAT-ROUTING-MONITORING | Partial [routing/monitoring/latency](../specs/routing-monitoring-latency.md):40 requirements/69 cases, partial scope reviewed | Not started | Unknown;33 documentary control/state and36null-oracle proposals; all target-null/U/unexecuted | Route/monitor/cue composition, compensation calibration, formats/clock and lifecycle/build gaps |
| FEAT-VIDEO | Partial [video workflows](../specs/video-workflows.md):18 requirements/28 cases, partial scope reviewed | Not started | Unknown; all target-null/U/unexecuted; no movie/frame/audio operations | Codec/timebase/marker/frame/stream-gap/window/display and lifecycle/build gaps |
| FEAT-BUNDLED-WORKFLOWS | [Seven bundled devices' broader workflows](../specs/bundled-device-workflows.md):55 requirements/118 cases; partial scope reviewed; exact-build, numeric and lifecycle gaps remain | Not started | Unknown;33 visible documentary/85 null-oracle proposals; all target-null/U/unexecuted | Broader controls/modes/voice/tuning, exact-build and numerical/lifecycle outcomes; Amp/Cabinet host emulation blocked |
| FEAT-SESSION-LAUNCH | [Session launch and Follow actions](../specs/session-launch-workflows.md):43 requirements/68 cases; partial scope reviewed; Q030 source contexts, timing/RNG and lifecycle remain U | Not started | Unknown;11 visible documentary/57 null-oracle proposals; all target-null/U/unexecuted | Global Follow/chance/context Q030, actual timing/RNG/output, boundary/lifecycle and build applicability |
| FEAT-BOUNCE-FREEZE | [Bounce and track Freeze workflows](../specs/bounce-freeze-workflows.md):41 requirements/77 cases; partial scope independently reviewed; signal/lifecycle/build and Flatten outcomes U | Not started | Unknown;42 visible documentary/35 null-oracle proposals; all target-null/U/unexecuted | Target command surface/Flatten, source/effect/mixer/automation/tails/files/rates/lifecycle |
| FEAT-SYNCHRONIZATION | [Link, Link Audio, Tempo Follower and MIDI sync](../specs/synchronization-workflows.md):26 requirements/36 cases; partial scope independently reviewed; wire/clock/detector/numeric/lifecycle/build outcomes U | Not started | Unknown;24 source-role/12 operational proposals; signal/timing documentary outputs null; all target-null/U/unexecuted | Target Link Audio availability, network/clock/MTC codecs/detector/audio calibration and lifecycle |
| FEAT-SETTINGS-LEARNING | Partial [settings/help](../specs/settings-learning-workflows.md):21 requirements/30 cases; partial scope independently reviewed | Not started | Unknown;18 visible documentary/12 null-oracle proposals, all target-null/U/unexecuted | New-feature availability, Q031 color preference context, content/media/OS behavior, delivery and lifecycle |
| FEAT-WARP-WORKFLOWS | Partial [Warp controls and editing](../specs/warping-workflows.md):50 requirements/88 cases, partial scope reviewed | Not started | Unknown;41 visible documentary/47 null proposals; all target-null/U/unexecuted | Q032 import wording, automatic BPM/markers, DSP/clock/quantization and lifecycle |
| FEAT-REMOTE-CONTROL | Partial [MIDI/key remote and generic surface setup](../specs/remote-control-workflows.md):37 requirements/47 cases, corrected R2 partial scope independently reviewed | Not started | Unknown;19 visible documentary/28 null proposals; all target-null/U/unexecuted | Review, UI/native token/context parity, actual bytes/feedback and149profile protocols |
| FEAT-APC-STARTUP | Assigned [startup unknowns](../specs/apc-controller-capabilities.md),6U obligations/12U proposals;37records remain research-only after reviewed correction | Not started | Unknown;zero positive runtime contracts,actual oracles null/U/unexecuted,zero coverage credit | Exact descriptor return,matching/usable ports/firmware/protocol/output/lifecycle for8source identities;other141rows retained |
| FEAT-STEM-SEPARATION | Partial [Stem separation](../specs/stem-separation.md):18 requirements/29 cases, partial scope independently reviewed | Not started | Unknown;8 visible documentary/21 null proposals; all target-null/U/unexecuted | Review, target availability, model/audio/format/region/nongroup placement and lifecycle |
| FEAT-AUTOMATION-WORKFLOWS | Partial [Automation workflows](../specs/automation-workflows.md):62 requirements/76 cases, partial scope independently reviewed | Not started | Unknown;44 visible documentary/32 null-oracle proposals, all target-null/U/unexecuted | Source shortcut/replace/MIDI reset contexts, exact recording/override/timebase/numerical/lifecycle outcomes |
| FEAT-PUSH-WORKFLOWS | Partial [Push1/Push2 workflows](../specs/push-controller-workflows.md):65 requirements/77 cases, partial scope independently reviewed | Not started | Unknown;18 visible documentary/59 null proposals; all target-null/U/unexecuted | Per-branch/model evidence; hardware/firmware/LED/MIDI/pressure/clock,Push3 and149profiles |
| FEAT-ENGINE-RESOURCES | Partial [Engine/resource workflows](../specs/engine-resource-workflows.md):28 requirements/50 cases, partial scope independently reviewed | Not started | Unknown;10 visible documentary/40 null proposals; all target-null/U/unexecuted | Source/processing context evidence; CPU/meter/source contexts, latency/audio/MIDI/quality/numerical/lifecycle outcomes |
| FEAT-MAX-API | Partial [bridge](../specs/live-api-bridge-workflows.md), [Clip/Sample](../specs/live-api-clip-sample.md), corrected [control/tuning](../specs/live-api-control-tuning.md) [device/rack](../specs/live-api-device-rack.md), corrected [core/Session](../specs/live-api-core-session.md) and [specialized](../specs/live-api-specialized-devices.md) independently reviewed | Not started | Unknown; all actual member oracles null/U/unexecuted;45entries/588declarations have partial owners, one heading-only member semanticU, zero complete | Exact-target applicability, inherited/root/alias closure, complete typed payloads/member branches/events/lifecycle |
| FEAT-BROWSER-CONTENT | Partial [Browser content](../specs/browser-content-workflows.md),56 requirements/71 cases; partial scope independently reviewed | Not started | Unknown;33 visible documentary/38 null proposals, all target-null/U/unexecuted | Source contexts/tag algebra, actual service/account/Pack/file/similarity/Push3 and lifecycle outcomes |
| FEAT-WORKSPACE-CONTROLS | Partial [workspace](../specs/application-workspace.md),13 requirements/23 cases; partial scope independently reviewed | Not started | Unknown;8 visible documentary/15 null proposals, all target-null/U/unexecuted | Scale propagation/folding, Status Bar/marker contexts, paired-window/focus and lifecycle/build outcomes |
| FEAT-MIXING-WORKFLOWS | Partial [mixing workflows](../specs/mixing-workflows.md),23 requirements/33 cases independently reviewed | Not started | Unknown;13visible documentary/20null proposals; all33targetnull/U/unexecuted | Source preference/group-slot/curve/send/multi-unit contexts and full target processing/lifecycle |
| FEAT-DYNAMICS | Partial [five dynamics devices](../specs/dynamics-devices.md): 62 requirements/129 cases, partial draft reviewed | Not started | Unknown;47 documentary/5file-only/77U cases, no application/audio comparisons | Review, transfer/envelope/lookahead/sidechain/analysis, build parity and lifecycle gaps |
| FEAT-FILTER-EQ | Partial [four filter/EQ devices](../specs/filter-eq-devices.md): 65 requirements/128 cases, corrected partial draft reviewed | Not started | Unknown; 78 documentary/4 file-only/46 U cases; no audio or application execution | Detector/chooser ambiguities, Legacy, DSP/numerical/build/lifecycle gaps |
| FEAT-AUDIO-UTILITIES | Reviewed partial [Utility](../specs/device-utility.md), [Tuner](../specs/device-tuner.md), [Spectrum](../specs/device-spectrum.md): 41 requirements/103 cases | Not started | Unknown; six package-file checks are not application tests; all 97 application cases ungraded | Signal interactions, detection/rounding, FFT/window/averaging/calibration and exact-build applicability |
| FEAT-HOSTING | Partial [hosting workflow draft](../specs/plugin-hosting.md), 21 requirements/40 cases, partial scope reviewed, all target U; draft [SPEC-PLUGIN-DISCOVERY](../specs/plugin-discovery.md) r2 (discovery only); [plugin-discovery-v1](../../handoff/plugin-discovery-v1/README.md) released (35 cases) | Not started | Unknown; 35 release cases and 62 draft cases not run | PRB-H1-01 to 08, PRB-N4-01, 02, 05; lifecycle, state, latency |
| FEAT-WARP | Draft [warp markers](../specs/warp-markers.md) r5 (39 case IDs); [warp-markers-v2](../../handoff/warp-markers-v2/README.md) (63 cases) | Not started | Unknown; reference/candidate comparison not run | Playback mapping/stretching, marker rounding gaps and open structural conditions; Q-021 |
| FEAT-PERSISTENCE | Draft [ALS container](../specs/als-container.md) r2 and [Live Set structure](../specs/live-set-structure.md) r2 (40 structure case IDs); [als-container-v1](../../handoff/als-container-v1/README.md) (35 cases); [live-set-structure-v1](../../handoff/live-set-structure-v1/README.md) (34 cases) | Not started | Unknown; reference/candidate comparison not run | Remaining path codes, class-specific refusals, save/reopen and recovery |
| FEAT-KEYBOARD-ACCESSIBILITY | Partial [navigation/accessibility](../specs/keyboard-navigation.md): 21 requirements/42 cases and292 discovered binding rows, corrected partial scope reviewed | Not started | Unknown; no OS/reader/UI/application execution | Context/order/platform/source review, per-command ownership and full lifecycle/protocol coverage |
| FEAT-UI | Partial [browser workflow draft](../specs/browser-workflows.md) (10 D12 requirements; exact-build U); draft [SPEC-BROWSER-INDEX](../specs/browser-index.md) r2 (browser index and tag sidecars); [browser-index-v1](../../handoff/browser-index-v1/README.md) released (26 cases) | Not started | Unknown; 26 release cases and 66 draft cases not run | PRB-BI-01 to 05 (proposed), PRB-H2-03 to 06 and 09; UI bindings and command/focus dispatch |
| FEAT-MIDI-USER-MAPPING | [Mapping draft](../specs/midi-user-mapping.md) r6 (55 configuration and 56 transform cases); [midi-config-v4](../../handoff/midi-config-v4/README.md) (161 cases, supersedes v3) | Not started | Unknown; reference/candidate comparison not run | Host assignments, stepped precision near half-integers and Value Scaling output; Q-009 |
| FEAT-ECOSYSTEM | None | Not started | Unknown | Shipped integration contracts and protocol handlers |
| FEAT-DELIVERY | Partial [delivery/recovery](../specs/delivery-recovery-workflows.md),45 requirements/60 cases independently reviewed; [helper handoff](../specs/update-helper-workflows.md),30/37 review pending; export routes to FEAT-RENDER | Not started | Unknown;13 visible documentary/47 null proposals, all target-null/U/unexecuted | Exact platform/build/entitlement/install/update/reset/recovery/consent/protocol/files/lifecycle outcomes |

As specs are released, add per-requirement reports with exact versions and
results. Summaries must not conceal unknown subcases. Do not turn a deferred
requirement into a pass or silently delete it from coverage.

## Finite device-audio releases — 2026-10-19

These packages release measured comparisons for fixed vectors, event histories and
capture lengths. They do not release arbitrary synthesis, stored-value mappings,
Live integration, or arm64 equivalence. A passing retained-reference self-check is
not an implementation or compatibility result. The five packages contain 256
finite evaluations; all candidate comparisons remain unknown.

| Current handoff | Evaluations | Explicit limits |
| --- | --- | --- |
| [Corpus v1](../../handoff/device-corpus-v1/README.md) | 68 in 24 groups | 174 mode occurrences omitted; host mapping and MIDI side-chain open |
| [Electric v2](../../handoff/device-electric-v2/README.md) | 117 | Stable mono measurements; three unstable settings, random level and phase/polarity ungraded; v1 superseded only for prose |
| [Tension v1](../../handoff/device-tension-v1/README.md) | 27 | Four chaotic settings and 37 uncalibrated outputs excluded |
| [Analog v1](../../handoff/device-analog-v1/README.md) | 42 in 38 groups | Deterministic selected outputs; noise, uncalibrated modulation, glide and unison excluded |
| [Collision v1](../../handoff/device-collision-v1/README.md) | 2 | Constructor effective silence and one calibrated Pipe capture only; modal/noise/Tube requirements open |

## Full-product specification target — 2026-10-19

[ADR 0005](../decisions/adr-0005-full-live-specification-coverage.md) expands the
analyst target beyond T1. The [coverage design](../research/full-live-specification-design.md)
requires a reconciled product denominator, supported behavioral contracts and
explicit acceptance cases; the [plan](../research/full-live-specification-plan.md)
tracks active work. Inventory and new drafts do not change any compatibility
status above. The whole-product specification target remains incomplete.

## Evidence priority

The next-evidence columns prioritize static specification work under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md). They do not waive later
comparison requirements. Derive acceptance cases first; retain runtime-dependent
claims as unknown until justified targeted probes or comparisons establish them.
No feature needs broad GUI automation as a default prerequisite. All current
verification statuses remain unknown.

## Current next-phase gates

The [decompilation and learning roadmap](../research/native-decompilation-roadmap.md)
separates export completeness, semantic coverage, pedagogical review and empirical
compatibility. Its [execution ledger](../research/native-phase-execution.md) now records the
authorized work: reviewed analyst tooling, a retained full inventory and bounded default-profile
export checkpoints, plus separate selected main Live exports with explicit failed entries.
Further bulk work stopped at the measured capacity gate; whole-corpus fit and
cold recovery remain unestablished (Q-011). These artifacts
establish no original-versus-candidate compatibility. All comparison statuses
above remain unchanged.

## Artifact navigation

The [artifact catalog](../research/artifacts/index.md) exposes retained binary,
pseudocode and disassembly coverage. Readable extracts and the offline browser
change discoverability only; every compatibility status remains unknown.

The [compact mirror](../research/native-compact-storage.md#measured-mirror--2026-10-10)
passed exact-byte preservation and named extraction against retained static
artifacts. This validates an analyst storage representation, not original
behavior, cold analyzer recovery or candidate compatibility.

The [original offline reader publication](../research/native-compact-storage.md#measured-reader--2026-10-11)
passed exact actual-code downloads under a DOM stub and browser link/hash checks.
The [v2 interaction repair](../research/native-compact-storage.md#read-revisions-interaction-fix--2026-10-12)
adds a bounded Chrome local-file check of visible code, focus, mouse/keyboard
activation, return navigation and exact downloaded bytes. This verifies analyst
navigation for the captured case, not broad accessibility, cross-browser behavior
or Ableton/candidate compatibility. Application compatibility remains unknown.

The [current persistent driver](../research/native-analysis-recovery.md#loader-matched-profiles--2026-10-12)
retains scoped synthetic persistence, timeout and export proofs. Independent
scope and quality reviews pass the loader-matched revision. Actual target
language/JVM verification, import/save and owned closure pass; first reopen is
blocked before launch by capacity. Cold persistence and decompilation remain
unverified. Synthetic tooling results
are separate from every application compatibility row above.

## Static preparation evidence — 2026-10-09

[Package preparation](../research/ableton-package-structure.md) establishes the
reference identity, inventory and static evidence seeds. The Push2 native
pipeline check produced pseudocode; this is tool-readiness evidence, not a
behavior/audio/file/UI/timing compatibility result. All verification statuses
above remain unknown and no implementation exists.

| Feature families | Available preparation | Remaining evidence |
| --- | --- | --- |
| Transport, Session, Arrangement, MIDI, persistence | XML schemas and named packaged set/clip samples | Trace loader/editor paths and units; isolate timing measurement needs |
| Ecosystem | Shipped MIDI configuration contract, Push2 QML and helper dossier | Trace mapping arithmetic/errors, bindings and lifecycle paths |
| Devices, audio | Named Utility preset and native symbols | Trace DSP/routing/automation; retain signal and latency measurement gaps |
| UI, delivery, hosting | Native helper paths, dependency model and WebView script sources | Trace dispatch, host errors, export and teardown; probe only unresolved behavior |
| Warp, automation | Schema/symbol search seeds | Derive algorithms and transitions; retain numerical comparison obligations |
