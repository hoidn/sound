---
id: SPEC-FEATURE-MAP
type: feature-map
status: draft
updated: 2026-10-23
access: analysis
---

# Whole application feature map

This is a proposed coverage inventory from the workflow discussion, not a
claim that all behaviors have been discovered. Expand it against versioned
manuals, package inventory, API surfaces, and observed user workflows.

The full-product target is now authorized by [ADR 0005](../decisions/adr-0005-full-live-specification-coverage.md).
The [coverage design](../research/full-live-specification-design.md) distinguishes
inventory/partial drafts from complete reviewed contracts. The
[execution plan](../research/full-live-specification-plan.md) selects work; this
coarse family table is not the full behavioral denominator.

| Feature ID | Area | Initial questions | Spec state |
| --- | --- | --- | --- |
| FEAT-TRANSPORT | Transport and timing | Tempo, meter, looping, launch boundaries, clock changes | [playback-core-v1](../../handoff/playback-core-v1/README.md) released (92 cases, partial playback/launch/MIDI/audio computations); Draft [SPEC-TRANSPORT-STATE](transport-state.md) r6 (document fields); [transport-state-v3](../../handoff/transport-state-v3/README.md) released, partial, superseding transport-state-v2; evidence in [transport-state static](../research/transport-state-static.md) and [native](../research/transport-state-native.md); Start, Stop and loop request paths and a static transition table in [transport transitions](../research/transport-transitions-native.md); launch grid and boundary rule in [clip launch](../research/clip-launch.md#from-a-quantization-value-to-a-launch-boundary) |
| FEAT-SESSION | Session View | Clips, scenes, follow actions, recording, Arrangement override | Partial [Session grid/scenes](session-view-workflows.md),R3:30 requirements/57 cases independently reviewed as partial; original metadata ownership preserved. Draft [SPEC-CLIP-LAUNCH](clip-launch.md) r5 (stored launch fields, values, load corrections, migration, grid and launch boundary; boundary offset, stopped launch, launch modes, Legato, velocity and follow-action timing open); evidence in [clip launch](../research/clip-launch.md); [clip-launch-v2](../../handoff/clip-launch-v2/README.md) released, partial (100 cases) |
| FEAT-ARRANGEMENT | Arrangement | Editing, comping, fades, clip boundaries, recording | [Arrangement editing](arrangement-editing.md): R3:42requirements/84scenarios independently reviewed as partial after focused oracle correction;43named/41null documentary pairs, all requirements/actions/history exact, target/lifecycle U |
| FEAT-AUDIO | Audio engine; [mix-graph-v1](../../handoff/mix-graph-v1/README.md) released (28 cases) | Mixing, routing, monitoring, latency, device changes | Draft [SPEC-MIXER-VALUES](mixer-values.md) r7 (general round-trip identity withdrawn; seven tested curve points only) (mixer storage, fader curves, value text, crossfade assign; audio-path clauses static-derived and need measurement); evidence in [mixer values](../research/mixer-values.md); [mixer-values-v2](../../handoff/mixer-values-v2/README.md) released, partial (80 cases) |
| FEAT-MIDI | MIDI engine | Scheduling, note state, expression, recording, MPE; audio-to-MIDI conversion | Draft [SPEC-MIDI-NOTE-STORAGE](midi-note-storage.md) r6 (bounded group/local-reader refinements reviewed;77draft IDs,publicU unchanged; clip note storage only; evidence in [MIDI note storage](../research/midi-note-storage.md)); finite note emission is released in [playback-core-v1](../../handoff/playback-core-v1/README.md); remaining scheduling, note-state and recording behavior open; audio-to-note library identified in [x86_64-only bundles](../research/x86-only-bundles.md); [midi-note-storage-v4](../../handoff/midi-note-storage-v4/README.md) released,partial (80cases/78fixtures;78oldobjects plus two local-reader projections) |
| FEAT-AUTOMATION | Automation and modulation | Curves, overrides, interpolation, recording, undo | Draft [SPEC-AUTOMATION-ENVELOPES](automation-envelopes.md) r6 (storage, targets, load checks, curves, Float, Bool and Enum evaluation; interpolation domain, steps, override, recording and undo open); evidence in [automation envelopes](../research/automation-envelopes.md); [automation-envelopes-v2](../../handoff/automation-envelopes-v2/README.md) released, partial (21 cases) |
| FEAT-DEVICES | Devices and racks | Chains, macros, state, mapping, signal behavior | Draft [SPEC-BUNDLED-DEVICE-PARAMETERS](bundled-device-parameters.md) r3 (stored parameters of the seven bundled devices; new-instance defaults and out-of-range handling open); evidence in [device bundles](../research/device-bundles-static.md), [device parameter mapping](../research/device-parameter-mapping-native.md) and [device tables](../research/device-tables-native.md); [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md) released, partial (82 cases)  Five device-audio drafts have finite reviewed releases: [Corpus v5](../../handoff/device-corpus-v5/README.md), [Electric v2](../../handoff/device-electric-v2/README.md), [Tension v1](../../handoff/device-tension-v1/README.md), [Analog v1](../../handoff/device-analog-v1/README.md) and [Collision v1](../../handoff/device-collision-v1/README.md), totaling 261 evaluations; general behavior and Live protocol remain open. Amp/Cabinet blocked by user decision 2026-10-19 [Bundled-device host draft](bundled-device-hosting.md) is reviewed only as conditional synthetic composition plus application gaps; its internal research models are excluded from compatibility coverage. Current partial observation owners are [Analog R15](../research/device-analog-dsp.md#analog-owner-r15-producer-partial-annex-adopted--2026-10-23), [Tension R17](../research/device-tension-dsp.md#tension-owner-r17-provided-bright-annex-adopted--2026-10-23), [Electric R16](../research/device-electric-dsp.md#electric-owner-r16-supplied-sine-annex-adopted--2026-10-23), [Corpus R21](../research/corpus-dsp-static.md#corpus-owner-r21-base-case-annex-adoption--2026-10-23) and [Collision R7](../research/device-collision-dsp.md#collision-owner-r7-stiffness-annex-adoption--2026-10-22). Their bounded observations preserve prior unknowns and released scopes; draft navigation counts are not compatibility passes. |
| FEAT-RECORDING | Recording and comping | Arm, monitor, record, Capture MIDI, take lanes and comp assembly | [Recording/comping](recording-comping.md): boundedownerR4 independently approved as partial,34requirements/90records (32oldbodies81oldobjects exact,twoUIroles/nineallnullhistories); explicit Off/positive-recording histories, manual build parity, timing, capture heuristics, errors/undo and saved transitions unknown |
| FEAT-RACKS | Device racks | Chains, zones, macros, variations, Drum Rack routing | [Device racks](device-racks.md), reviewed R5:38requirements/101cases,81prior records exact; historical/current ledger clarification resolved; full124/153-block primary/common source audits reviewed as partial; exact-build and audio/lifecycle gaps |
| FEAT-MIDI-EDIT | MIDI editing | Selection, draw/grid, note/velocity/probability and multi-clip operations | [MIDI editor/tools](midi-editing-tools.md), R5:43IDs/93cases independently reviewed as partial after three focused source-role corrections; all72earlier records/source claims/oracles exact; general [Clip View](clip-view-workflows.md) adds reviewed partial R2:55 requirements/92 cases; complete Clip View/MIDI/MPE outcomes remain open |
| FEAT-AUDIO-TO-MIDI | Audio-clip slicing and recognition | Slice plans/presets/timing, Harmony/Melody/Drums result workflows | [Audio-to-MIDI](audio-to-midi.md), R3 independently reviewed as partial:14IDs/37cases,29old records exact; factory/no-custom preview qualifications; algorithms/counting/build/lifecycle outcomes U |
| FEAT-MPE | Per-note expression and MPE | Editing, receiver/controller ranges, routing and lifecycle | [MPE workflows](mpe-workflows.md), R3 independently reviewed as partial:18 IDs/50 cases,27old records exact; numeric/protocol/target outcomes U |
| FEAT-TUNING | Tuning systems | Import/reference/layout, retuning and interoperability | [Tuning systems](tuning-systems.md), R3 independently reviewed as partial:21IDs/43cases,32old records exact; parser/math/build applicability U |
| FEAT-GROOVES | Grooves | Pool/extract/apply/commit, timing/velocity/random | [Groove workflows](groove-workflows.md), R3:14 requirements/34 cases independently reviewed as partial; chooser/audio-envelope/clip-and-pool roles refined, numerical/random/build applicability U |
| FEAT-MIDI-TOOLS | Note transformations/generators | 12 transformations and 5 generators | [MIDI editor/tools](midi-editing-tools.md), 17 individual tool clauses within 43 requirements; numerical/random/lifecycle and source-conflict gaps remain |
| FEAT-PROJECT-MANAGEMENT | Projects and media | Save/templates/merge, reference repair/collect, unused files and Packs | [Project/media workflows](project-media-workflows.md), ownerR2 independently approved as partial:23requirements/53scenarios,22oldclauses34oldrows exact/19newnullhistories; all53actualnullU; exact-build, file-format and failure/transaction gaps remain |
| FEAT-MEDIA-FILES | Media import and clip interchange | Audio format eligibility, cache/ASD/defaults, MIDI files and Live Clips | [Media workflows](media-file-workflows.md), partial author draft with 17 requirements/32 cases; partial R4 acceptance refinement reviewed with explicit analysis-On/Off histories, exact codec/algorithm/lifecycle and build outcomes U |
| FEAT-RENDER | Audio and video export | Track/range selection, encoding, tails and external-device rendering | [Audio/video export](audio-video-export.md), reviewed partial draft with 23 requirements/34 scenarios; exact-build, numerical and failure outcomes unknown |
| FEAT-NATIVE-MIDI-EFFECTS | Native MIDI effects | Eight devices, input/control/output transitions and lifecycle | [Native MIDI effects](native-midi-effects.md), 27 requirements/176 cases; bounded R3 independently reviewed as partial, all target outcomes unknown |
| FEAT-SAMPLE-INSTRUMENTS | Simpler, Sampler and Impulse | Sample/voice/mode/zone/control/routing interactions | Individual [Simpler](device-simpler.md), [Sampler](device-sampler.md) and [Impulse](device-impulse.md) bounded ownerR3:63IDs/102cases independently approved as partial;61old bodies88old cases exact; all actual pairs U and DSP/lifecycle/build gaps remain |
| FEAT-DELAY-REVERB | Delay, Echo, Filter Delay, Grain Delay, Reverb, Hybrid Reverb, Resonators | Modes, feedback, freeze/tails and modulation | [Delay/reverb devices](delay-reverb-devices.md), reviewed corrected partial draft93IDs/176cases, bounded ownerR3 independently approved as partial;92old bodies149old cases exact; exact DSP/build/lifecycle gaps remain |
| FEAT-DISTORTION | Nine distortion/character effects | Modes, drive/routing/filter and state interactions | [Distortion devices](distortion-devices.md), ownerR3 independently approved as partial,67unchanged IDs/200cases (190old exact,tennewnull); audio/transfer/aliasing and exact-build gaps remain |
| FEAT-MODULATION-PITCH-LOOP | Ten modulation, pitch, spectral and looping devices | Modes, sidechains, voices, freeze/capture, modulation and Looper transitions | [Modulation/pitch/loop devices](modulation-pitch-loop-devices.md), ownerR4 independently approved as partial,106unchanged IDs/208cases (186old exact,22newnull); all target outcomes null/U; numeric, lifecycle and protocol gaps remain |
| FEAT-SYNTHESIS-INSTRUMENTS | Drift, Drum Sampler, Meld, Operator and Wavetable | Oscillators/sample playback, modulation/voices, MPE/tuning and state | [Synthesis instruments](synthesis-instruments.md), ownerR3 independently approved as partial110IDs/190cases (109old bodies154oldcases exact), target applicability and signal/lifecycle outcomes U |
| FEAT-EXTERNAL-HARDWARE | External Audio Effect and External Instrument | Port/channel/return controls, gain/phase roles and latency-unit state | [External hardware devices](external-hardware-devices.md), bounded ownerR3 independently approved as partial,24unchanged IDs/60cases;56old objects exact; physical/plugin signal and build/lifecycle outcomes U |
| FEAT-LEGACY-DEVICES | Eight retained native legacy profiles | Predecessor controls versus target package identity and migration | [Legacy native devices](legacy-native-devices.md), boundedownerR2 independently approved as partial77unchanged IDs/194records and114-block source audit approved as partial;45D11precursor clauses/8file clauses/24U; target parity remains unknown |
| FEAT-CLIP-VIEW | Shared Clip View and audio properties | Selection/panels, region/loop/scrub, reverse/crop/replace, multi-edit and defaults | [Clip View](clip-view-workflows.md), reviewed partial R2:55 requirements/92 cases; media/timing/algorithm/lifecycle gaps and Q029 remain |
| FEAT-MAX-HOST | Max device/tool hosting and five templates | Editor selection/edit/save/discovery/dependencies/template roles | [Max hosting](max-for-live-hosting.md), partial38 requirements/64 cases; corrected partial scope independently reviewed; full API/patch/engine/lifecycle applicability U |
| FEAT-MAX-DEVICES | Twenty shipped Max devices | Individual audio/MIDI/control/DS instrument roles, controls and lifecycle | [Max devices](max-for-live-devices.md),135 requirements/315 cases partially reviewed; dated DS Sampler/Expression Control Legacy source applicability and all target outcomes U |
| FEAT-ROUTING-MONITORING | General track routing and compensation | Source/destination/taps, monitor contexts, submix/group/Main/cue and latency controls | [Routing/monitoring/latency](routing-monitoring-latency.md), reviewed partial R2:41 requirements/70 cases, physical/numerical/clock/lifecycle outcomes U |
| FEAT-VIDEO | Video import, presentation and scoring | View eligibility, movie-to-audio operations, window/gaps/markers/pre-roll | [Video workflows](video-workflows.md), reviewed R2-spec/R3-research partial20 requirements/34 cases; codec/frame/audio/sync/build/lifecycle outcomes U |
| FEAT-BUNDLED-WORKFLOWS | Seven bundled devices' broader workflows | Modes, controls, modulation/voices/tuning and interactions | [Seven bundled devices' broader workflows](bundled-device-workflows.md), 55 requirements/118 cases; partial scope reviewed; exact-build, numeric and lifecycle gaps remain |
| FEAT-SESSION-LAUNCH | Session launch and Follow actions | Gestures/modes, Legato/velocity, Follow groups/scene/chain controls | [Session launch and Follow actions](session-launch-workflows.md), 43 requirements/68 cases; partial scope reviewed; Q030 source contexts, timing/RNG and lifecycle remain U |
| FEAT-BOUNCE-FREEZE | Bounce and track Freeze workflows | Individual/group/source/effects/mixer/automation/tails and predecessor Flatten | [Bounce and track Freeze workflows](bounce-freeze-workflows.md), 41 requirements/77 cases; partial scope independently reviewed; signal/lifecycle/build and Flatten outcomes U |
| FEAT-SYNCHRONIZATION | Link, Link Audio, Tempo Follower and MIDI sync | Peer/transport/audio source roles, Clock/MTC and settings | [Link, Link Audio, Tempo Follower and MIDI sync](synchronization-workflows.md), R3:29 requirements/42 cases; Resync documentary control/modes independently reviewed as partial; wire/clock/detector/numeric/lifecycle/build outcomes U |
| FEAT-SETTINGS-LEARNING | Settings, Learn and Info View | Appearance/input/audio setting entry points, lessons/player/help and preference contexts | [Settings/help](settings-learning-workflows.md),R4:23 requirements/33 cases independently reviewed as partial; Sample Editor/plug-in folder configuration roles added; target/delivery/numeric/media/lifecycle unknowns remain |
| FEAT-WARP-WORKFLOWS | Warp controls and editing | Interactive markers/transients, load policies, auto-command/mode and tempo roles | [Warp controls and editing](warping-workflows.md),R2:50 requirements/91 cases, source-audit successor independently reviewed as partial; all target outcomes U |
| FEAT-REMOTE-CONTROL | MIDI/key remote and generic surface setup | Assignment/takeover/mode/feedback/bank/lock and key-context roles | [MIDI/key remote and generic surface setup](remote-control-workflows.md),37 requirements/47 cases, corrected R2 partial scope independently reviewed; all target outcomes U |
| FEAT-APC-STARTUP | APC controller startup | Eight source identities, actual descriptor/matching/ports/protocol lifecycle unresolved | [Startup unknowns](apc-controller-capabilities.md),6U obligations/12U cases;37metadata facts research-only, reclassification reviewed;zero supported runtime contracts or coverage credit |
| FEAT-STEM-SEPARATION | Stem separation | Element/Merge/mode/region, clip/track/effects/envelopes and generated-file roles | [Stem separation](stem-separation.md),R2:20 requirements/32 cases, source-audit successor independently reviewed as partial; all target outcomes U |
| FEAT-AUTOMATION-WORKFLOWS | Automation and clip envelope workflows | Recording/editing/override/re-enable, linked-unlinked/modulation/loop/control roles | [Automation workflows](automation-workflows.md),62 requirements/76 cases independently reviewed as partial; full192-context source audit independently approved as partial,19proposals unadopted; finite envelope/mix/timebase owners unchanged, all target outcomes U |
| FEAT-PUSH-WORKFLOWS | Push1/Push2 workflows | Per-model pad/mode/session/record/device/browse/setup roles | [Push1/Push2 workflows](push-controller-workflows.md),65 requirements/77 cases partially reviewed; all target outcomes U |
| FEAT-ENGINE-RESOURCES | Engine/resource workflows | CPU/load/impact/I-O/overload controls and cross-owner fact-sheet comparisons | [Engine/resource workflows](engine-resource-workflows.md),28 requirements/50 cases partially reviewed; all target outcomes U |
| FEAT-MAX-API | Public Live API | Object/path/ID/property/function/event/remote/lifecycle contracts | [Bridge](live-api-bridge-workflows.md), [Clip/Sample](live-api-clip-sample.md), corrected [control/tuning](live-api-control-tuning.md) [device/rack](live-api-device-rack.md), corrected [core/Session](live-api-core-session.md) and [specialized devices](live-api-specialized-devices.md) partially reviewed. All45entries/588direct declarations have partial mapping owners; one heading-only member stays U, zero complete; original source inventory unchanged |
| FEAT-BROWSER-CONTENT | Browser content/services | Advanced filters/tags/collections/Places, Packs/similarity/Splice/Cloud/Push file workflows | [Browser content](browser-content-workflows.md),56 requirements/71 cases partially reviewed; local194primary/6secondary source audit independently approved as partial,95literal roles/74servicecontexts excluded, no adoption; full protocol/account/similarity/build/lifecycle outcomes U |
| FEAT-WORKSPACE-CONTROLS | Shared workspace controls | Global scale selection/default context, Status Bar, paired-window views and entry gestures | [Workspace](application-workspace.md),13 requirements/23 cases partially reviewed; existing domain controls/scale/numeric owners retained, all target U |
| FEAT-MIXING-WORKFLOWS | Mixer interactions and groups | Mixer presentation/multi-edit/group/solo/crossfade gestures and entrypoints | [Mixing workflows](mixing-workflows.md),R2:31 requirements/50 cases independently reviewed as partial; eight bounded UI roles added, numeric/signal, routing, record/Session and lifecycle laws retain owners/U |
| FEAT-DYNAMICS | Compressor, Gate, Glue Compressor, Limiter and Multiband Dynamics | Detection, timing, gain, sidechain, channel/display and lifecycle | [Dynamics devices](dynamics-devices.md), 62 requirements/153 cases, bounded R2 independently reviewed as partial; DSP/numerical/build and lifecycle outcomes U |
| FEAT-FILTER-EQ | Auto Filter, Channel EQ, EQ Eight and EQ Three | Filter/EQ controls, modes, modulation/sidechain and signal interactions | [Filter/EQ devices](filter-eq-devices.md): 65 requirements/140 cases, bounded R4 independently reviewed as partial; legacy and numeric/build outcomes remain open |
| FEAT-AUDIO-UTILITIES | Utility, Tuner and Spectrum | Signal controls, pitch display and spectral analysis | [Utility](device-utility.md), [Tuner](device-tuner.md), [Spectrum](device-spectrum.md): independently reviewed partial R2drafts,41requirements/112cases,103old exact; detector, DSP and exact-build gaps remain |
| FEAT-HOSTING | Plug-in hosting | Discovery, lifecycle, state, latency, failures | [Hosting workflows](plugin-hosting.md), reviewed partial draft (21 requirements/40 cases); API/state/timing remain unknown. Draft [SPEC-PLUGIN-DISCOVERY](plugin-discovery.md) r2 (VST3 and VST2 discovery only); evidence in [plug-in scanner](../research/plugin-scanner-static.md) and [helper launch](../research/helper-launch-live-side.md#plug-in-scanner); [plugin-discovery-v1](../../handoff/plugin-discovery-v1/README.md) released, partial (35 cases) |
| FEAT-WARP | Warping | Markers, modes, tempo/pitch behavior, boundaries | Draft [SPEC-WARP-MARKERS](warp-markers.md) r5 (marker storage, shadow marker, empty-list refusal, enumerations, setting domains, scripting sample/beat conversion and edit limits); playback mapping and stretching audio unspecified; evidence in [warp markers](../research/warp-markers.md); [warp-markers-v2](../../handoff/warp-markers-v2/README.md) released, partial (63 cases) |
| FEAT-PERSISTENCE | Files and recovery; [live-set-structure-v1](../../handoff/live-set-structure-v1/README.md) released (34 cases) | Sets, presets, media references, migration, recovery | Draft [SPEC-ALS-CONTAINER](als-container.md) r2, envelope only; [als-container-v1](../../handoff/als-container-v1/README.md) released, partial ([static](../research/document-container-static.md), [native](../research/document-container-native.md)); schema still declares `ReWireDeviceMidiTargetId`; XMP tag sidecars and `filerefmap.db` in [browser index](../research/browser-index-static.md)  [Live Set structure r2](live-set-structure.md) reconciles the reviewed device-free fixture |
| FEAT-KEYBOARD-ACCESSIBILITY | Keyboard navigation/accessibility | Focus, Tab/Wrap/settings, envelope keyboard edits and shortcut contexts | [Navigation/accessibility](keyboard-navigation.md), R5:40 requirements/96 cases independently reviewed as partial; separate292-row binding discovery/source audit R2 retained; Q052 dispatch contexts U |
| FEAT-UI | Desktop interface | Browser, selection, shortcuts, drag/drop, focus, undo | [Browser workflows](browser-workflows.md) adds selected documented-domain search/navigation/preview interactions; exact 12.4.3 applicability U. Draft [SPEC-BROWSER-INDEX](browser-index.md) r2 (browser content kinds, tag sidecars, previews, rebuild); static evidence in [browser index](../research/browser-index-static.md); [browser-index-v1](../../handoff/browser-index-v1/README.md) released, partial (26 cases) |
| FEAT-MIDI-USER-MAPPING | User-defined controller mapping (ecosystem subset) | Configuration, channels, banks, buttons and native/host gaps | [Revision7 draft](midi-user-mapping.md) with S4 closure and1,006finite supplied-state relative-byte X cases; public/ARM behavior qualified, portable comparators NULL; [finite configuration release](../../handoff/midi-config-v1/README.md), partial clauses only; [midi-config-v2](../../handoff/midi-config-v2/README.md) released, partial REQ-002/003/005–013; [midi-config-v4](../../handoff/midi-config-v4/README.md) released, partial (161 cases) |
| FEAT-ECOSYSTEM | Integrations | Link, controllers, Push, Max for Live, Packs, ReWire | Unspecified; ReWire mixer and device modes appear x86_64-only ([x86_64-only bundles](../research/x86-only-bundles.md)); Push 3 helper interfaces in [Push 3 helper](../research/push3-helper-static.md); add-on and extension helper in [web, add-ons, swapper](../research/web-addons-swapper-static.md); Packs remain in Live |
| FEAT-DELIVERY | Delivery and export | Preferences, install, audio export, teardown, crash handling | [Delivery/recovery](delivery-recovery-workflows.md),45 requirements/60 cases partially reviewed; exact platform/build/install/auth/update/recovery outcomes U. [Helper handoff](update-helper-workflows.md),30/37 independently reviewed as partial static roles; actual outcomes remain U. Export routes to FEAT-RENDER. Self-update (`.asu`, xdelta, swap with rollback) static evidence in [web, add-ons, swapper](../research/web-addons-swapper-static.md) |

Split these families into bounded feature pages as evidence arrives. Require
separate statuses for documentation, implementation, and verification; do not
mark a family complete when only one scenario passes.

## Compatibility dimensions

- Behavior: state transitions, outputs, errors, and user task outcomes.
- Audio: deterministic equality where applicable; otherwise declared signal metrics.
- Files: semantic interchange and preservation, with byte equality only when required.
- UI: interactions/accessibility and separately declared visual expectations.
- Real-time operation: scheduling, latency, jitter, load, and failure recovery.

Numeric tolerances, supported versions/platforms, and required scenarios are
unresolved in [Q-001](../questions.md#q-001-compatibility-targets).
Track current evidence in the [coverage matrix](../verification/coverage.md).


Earlier checkpoint records below retain their as-of scopes/counts. Current
release availability belongs to the catalog and current rows above.

## Depth selection checkpoint — D-02 first action

The [independently reviewed census](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/released-case-depth-census-review.json)
checked19then-current releases/1070 case rows as a bounded schema/triage operation; those are retained report counts, not the advancing catalog.
It adds no X/S/shipped-data outcome grade, completes no profile/family and runs
no candidate. Five ALS refusal classes remain unspecified although refusal
outcomes are concrete. Required-outcome depth counts are not recomputed by
this scan; candidate conformance remains unexecuted, with no fraction reported.
That checkpoint used revision3's candidate-demand order. The
[current plan](../research/full-live-specification-plan.md#current-selection--revision-4-amended-2026-10-20)
now selects component/indirect-call recovery, integration, family maps and
batch grading; D-01 capability is answered, D-03 stays open and T1.7 is deferred.
Draft unknowns do not become released cases through matching local numbers.
Whole-product completion remains open; no depth grade changes with this routing. The
[reviewed integration context](../research/program-structure.md#t1-scenario-integration-map--2026-10-20)
now supports family route-ledger selection; its static boundaries and unknown
joins supply no new application outcome or completeness grade. The
[family route atlas](../research/program-structure.md#family-route-cuts--2026-10-20)
owns current per-family structure reviews, qualified route inventories and
unresolved public joins. These inventories change no case grade or family
completeness status. Current assignments/counts belong to the execution plan.
The
[reviewed mix leaf batch](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-mix-leaves-v1/README.md)
adds finite x86 helper evidence; its 252 additional boundary pairs remain
ungraded and do not establish a runtime-table, public mix or ARM outcome.


The [Corpus D-01 first-action review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-depth-preflight-review.json)
confirms the retained baseline: all seven models have finite vectors, while 174
modal measurement occurrences remain omitted across 14 evaluations. This adds
zero graded outcomes and no complete profile; the required-outcome denominator
is not frozen by that inventory. [A1 traceR2](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-position-trace-review-final.json)
passed focused independent review after a one-field citation correction; A1
remains unresolved. [Modal diagnostics](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-modal-observability-review.json)
passed exploratory research review, with aliasing, nuisance/rank/window and
uncertainty gates still open. All174omissions remain ungraded; no estimator or
criterion is adopted. [Calibration](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-modal-calibration-review.json) and
[scalar-lane](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-range-lanes-review.json) companions passed
independent partial research review: lowband evidence strengthened, uncertainty
stillblocked; two local FP query lanes resolved, current-value/emission/A1stillU.
[Combined value-source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-position-value-source-review.json)
approves conditional initialization/currentpull/converter arithmetic bypass only;
emission/publicA1 remainU. [Two new finite X captures](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-lfo-ramp-up/README.md)
succeeded through the unchanged loader: exact retained Sine baseline then RampUp.
[Independent capture review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-lfo-ramp-up-review.json) approves these two bounded captures.
[Separate sensitivity review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-lfo-ramp-sensitivity-review.json) approves two additional ±1math-import
captures, without treating their differences as portability bounds. The
[1%per-channel waveform-RMS criterion](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-lfo-ramp-criterion-review.json) passed independent method review.
[Corpus R4](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-owner-r4-review.json) passed separate owner review and is adopted with one finite
host-input case DCO-029, preserving all28earlier case rows. [Corpus v2](../../handoff/device-corpus-v2/README.md) is released locally after separate
handoff review and final inventory approval (24groups/69evaluations, old68exact). No aggregate required-outcome numerator, application grade or
complete profile is asserted. Candidate conformance remains unexecuted.


[Utility D-03 static preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-depth-preflight-review.json)
is independently approved as bounded research. Exact retained wrapper/kernel,
setter, callback-slot and conditional zero-return evidence provides a concrete
next route; it grades no application outcome. [Unreviewed connection query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-connection-frontier-2026-10-19.json) retains the bounded metadata/model-binding
frontier without closing the actual Mute member/processor identity. It adds no
behavioral grade and does not establish a missing or infeasible runtime route.
Current Utility has41 scenarios:
26documentary/3historical file-only/12U; all38application scenarios remain U with
named paths. No atomic outcome denominator, candidate fraction or no-route
finding is established. The [conditional Mute trace](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-trace-review.json)
is independently approved only as function-local static research under its
valid-memory/same-object/no-interference/actual-invocation predicate. Public
dispatch, callback delivery and lifecycle remain open. [Model-routing review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-model-routing-review.json)
approves observer/enrollment/descriptor associations only; public model to
processor join remains unknown. A Utility feasibility result cannot classify every other in-binary
device automatically.


[Two later Corpus MIDI captures](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-pitch-review.json) passed independent bounded
evidence review: at that checkpoint, six actual new original-x86 children including the four
Ramp/sensitivity calls. Qualitative multi-component octave-like response is
consistent with the note60/72 intervention. That capture review alone adopted
no calibrated fundamental, event onset, Live-sidechain law, normative case or
criterion; the finite device total was 257 at that checkpoint. The later
method/owner/release decisions below have separate review. Details
and unreviewed source frontiers belong to [Corpus research](../research/corpus-dsp-static.md#later-bounded-midi-pitch-evidence--2026-10-19).


[Utility membership frontier](../research/device-audio-utilities.md#d03-mute-membership-frontier--2026-10-20)
retains seven unreviewed complete-source bodies and40instruction bytes as data.
Descriptor offset/return-register facts are narrowed; actual type/name/map and
processor delivery remain unproved. No application grade, complete profile or
route-absence finding; all38Utility application scenarios stayU.


[Corpus finite MIDI modal method](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-modal-method-review.json) is independently approved
as a bounded engineering criterion; both post-observation mode16omissions
and all32research rows remain retained. [Owner R5](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-owner-r5-review.json) is separately
approved/adopted for DCO030/031:31cases (27finite/fourU),13IDs/all29oldrows
retained. [Corpus v3](../../handoff/device-corpus-v3/README.md) is released locally
after separate handoff and final-seal review: 25 groups/71 evaluations, all 69
earlier evaluations retained. The five current device packages total 259
evaluations. No general MIDI/pole/uncertainty proof, application grade, complete
profile or candidate fraction follows.


[Three later Corpus gate/release captures](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-gate-release/CAPTURE.md)
[passed bounded X evidence review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-gate-release-capture-review.json) after the R2 accounting fix. Nine
original children total at that earlier checkpoint; gate1-held/off full-byte equal and gate0-off equal
to the older held control. No admitted note-off/gate law, new criterion/case
or coverage credit follows. Current v3/259 device evaluations remain unchanged.


The [conditional Corpus initialization queue join](../research/corpus-dsp-static.md#conditional-initialization-queue-join--2026-10-20)
and later [selected render-site carrier](../research/corpus-dsp-static.md#actual-before-impulse-note-off-captures--2026-10-20)
passed independent partial source reviews. Actual module membership, the unread
intraprocedural branch and all-path event delivery remain unknown. The
[control-dispatch frontier](../research/corpus-dsp-static.md#conditional-control-message-dispatch--2026-10-20)
passed independent partial source review; the later index34 endpoint captures
are filed as observations below. No application outcome, new criterion/case or coverage credit is added.


The [later before-impulse Corpus probe](../research/corpus-dsp-static.md#actual-before-impulse-note-off-captures--2026-10-20)
adds three valid extracted observations (twelve children total), with independent
capture review now approved as bounded observations only. Its tiny prefix-only
contrast adds no normative case, acceptance criterion or coverage credit; all post-impulse bytes remain equal.


[Host-index34 zero captures](../research/corpus-dsp-static.md#actual-host-index34-zero-captures--2026-10-20)
add three valid original-x86 observations, fifteen children total in this
continuation. Capture and separate finite-method reviews approved bounded
scopes; [current research](../research/corpus-dsp-static.md#actual-host-index34-zero-captures--2026-10-20) records the explicit engineering budget and its tail/prefix limits.
Separate R6 owner review passed and Root adopted only DCO032:13IDs/32cases,
28finite/fourU, all31oldrows/001–012 literal. V4 is independently reviewed/released with72evaluations,
all71oldobjects retained; five current device packages total260evaluations. No application
outcome, frozen required-outcome fraction or complete-profile credit.


[Corpus R7 owner adoption](../research/corpus-dsp-static.md#corpus-r7-owner-adoption--2026-10-20)
adds only DCO033 under001/012:13IDs/33cases,29finite/fourU, all32oldrows retained.
The four-axis engineering rule covers one exact pickup-step history; no broader
smoothing/latency/A1/modal or application outcome is closed. At owner adoption v4 was current; [v5 is now released](../research/corpus-dsp-static.md#release5-local-publication--2026-10-20)
with73evaluations (five device packages261) after separate content/actual-result
and final-seal approvals. No
frozen required-outcome fraction or complete-profile credit follows.


[Corpus v5 publication](../research/corpus-dsp-static.md#release5-local-publication--2026-10-20)
adds only one finite history:27groups/73evaluations, all72oldobjects exact.
Actual4799reference-self measurements/38controls/threeguards pass; all candidate
comparisons remain unknown. No frozen depth denominator or complete profile
follows; the unchanged modal/A1/general host obligations remain open.


The reviewed [Corpus x86 entry exports](../research/corpus-dsp-static.md#reviewed-constructor-span-and-setup-nomination--2026-10-20)
and [Utility reviewed owned-state call histories](../research/device-audio-utilities.md#reviewed-owned-state-history-and-public-binding-gap--2026-10-20)
are bounded analyst evidence. They add no application outcome, released case,
frozen-denominator credit or candidate conformance. Current selections belong to
the sole depth plan; the owning research pages retain source and method limits.


The 2026-10-20 [Utility class-source approval](../research/device-audio-utilities.md#utility-class-construction-source-review-approval--2026-10-20) and native MIDI [initialization](../research/native-midi-effects.md#native-midi-initialization-source-review-approval--2026-10-20) / [processing-source approvals](../research/native-midi-effects.md#native-midi-processing-source-review-approval--2026-10-20) refine conditional analyst evidence. Their canonical pages own the review scope and residuals. No application outcome, required-outcome fraction, released case or candidate conformance changes.


The [Filter/EQ family map approval](../research/filter-eq-devices.md#filtereq-family-route-review-approval--2026-10-20) adds bounded route/metadata navigation for all four current profiles. Historical file-only routes remain distinct from unknown public processing/control/lifecycle outcomes. No required-outcome fraction, new grade or candidate conformance follows.


The [Dynamics family-map approval](../research/dynamics-devices.md#dynamics-family-route-review-approval--2026-10-20) adds bounded navigation for all five current profiles. Documentary annotations and retained-file-only S predicates remain separate from unknown application outcomes. No new outcome grade, complete profile or candidate conformance follows.


The [Utility native static readback](../research/device-audio-utilities.md#utility-native-abi-static-review-approval--2026-10-20) narrows conditional register and initializer-local state relationships. All public control/receiver/host-output and lifecycle bridges remain unknown; no application grade, complete profile or candidate conformance changes.


The [Recording/comping family-map approval](../research/recording-comping.md#recordingcomping-family-route-review-approval--2026-10-20) and [audio/video-export approval](../research/audio-video-export.md#audiovideo-export-family-route-review-approval--2026-10-20) add bounded analyst navigation at T1 recording/export boundaries. Retained inventory/source annotations remain distinct from actual application outcomes, which stay unknown. No required-outcome fraction, new grade, released case or candidate conformance changes.


The [Utility x86 static review approval](../research/device-audio-utilities.md#utility-x86-static-review-approval--2026-10-20) records conditional carrier/byte evidence and its explicit auxiliary count correction. All public bridges and38Utility application outcomes remain unknown; no new behavior grade,released case or candidate conformance changes.


The [sample-instrument family approval](../research/sample-instruments.md#sample-instrument-family-route-review-approval--2026-10-20) and [distortion approval](../research/distortion-devices.md#distortion-family-route-review-approval--2026-10-20) add bounded analyst navigation. Application outcomes stayunknown;fileS/documentary contexts stayseparate. The reviewed Sampler reference erratum preserves017asnegative and039own productive-loop prerequisites. No newcase/oracle/grade/release,candidate conformance or complete profile changes.


[Utility four-target static approval](../research/device-audio-utilities.md#utility-x86-four-target-static-review-approval--2026-10-20) narrows conditional local carrier/member flow. The localx86indirect target remainsunknown and inconsistent auxiliary ESIL is excluded. All38application outcomes stayU;no grade,site credit,complete profile or candidate conformance follows.


The [device chains/Racks route approval](../research/device-racks.md#device-chains-and-racks-family-route-review-approval--2026-10-20) adds bounded analyst navigation:38non-atomic bundles,1file-onlyS/37applicationnone/zeroX,101actualU;35D12annotations remain separate. No application grade,new case/release,candidate conformance or complete family/profile follows. Required unsupported behavior keeps coverage open.


The [Delay/Reverb route approval](../research/delay-reverb-devices.md#delay-and-reverb-family-route-review-approval--2026-10-20) adds bounded navigation:562requirednone/U(0S/0X),316D12+246Uannotations on those SAMEunits;sevenfileS assertions remain auxiliary. All176actualresults stayU. No newcase/oracle/grade/release,candidate conformance or complete profile/family follows;unsupported required behavior keeps coverageOPEN.


The [Utility inner-entry actual approval](../research/device-audio-utilities.md#utility-x86-inner-entry-static-review-approval--2026-10-20) adopts352staticbytes/64rows/sevenconditionallocalfacts,zerooriginalcalls. Late load64(T+10) return is not a publicidentity or zero law;ninehelperwrites remainunknown. UDN002qualifies further auxiliaryESIL conflict;allESILexcluded. All6G/38publicU/48inventory unchanged;no grade/site/case/release or coverageclosure.


The [DeviceKit provider inventory](../research/program-structure.md#devicekit-provider-frontier--2026-10-20) is approved metadata navigation only:external names/content profiles do not establish a provider/runtime binding. Missing retained-input routes remainunknown. No grade/site/case/release or family/productclosure;unsupportedrequiredU staysopen. Consumerheader/loadcommand capture remains unselected while preparation proceeds.


The [fixed14Delay/Reverb source approval](../research/delay-reverb-devices.md#fixed-fourteen-method-source-review-approval--2026-10-20) adds conditional retained-C facts,zero complete callablemath/Xleaf. Publicreceiver/control/FP/helper/consumer dependencies stayunknown;all562requiredunits/176actualresults stayU. No norm/case/oracle/grade/site/release or family/productclosure;unsupportedcoverage staysopen.


The [Modulation/Pitch/Loop map approval](../research/modulation-pitch-loop-devices.md#modulation-family-route-review-approval--2026-10-20) adds106wholeclause bundles allnone/U;96D12+10U labelSAME106,tenauxfileS outside,all208appactualU. Correctedspectralartifact IDs imply no runtimeidentity. [Consumermetadata actual approval](../research/program-structure.md#consumer-load-command-actual-approval--2026-10-20) establishes declarations/locations only,no provider/publicbinding orgrade. No norm/case/release/site/candidateconformance or family/productclosure;unsupportedrequiredU remainsopen.


The [Synthesis family map](../research/synthesis-instruments.md#synthesis-family-route-review-approval--2026-10-20)
passed bounded independent review: all110wholeclauses / 190actualU cases,
585unsupported route units. Documentary390 and lifecycle195 are those same585,
not grades or a whole-product denominator. Source567 semantic judgments remain
inherited; no complete callable leaf or public voice/control/output route is
established. No requirement, case, release or compatibility state changes.


The [Legacy family map](../research/legacy-native-devices.md#legacy-family-route-review-approval--2026-10-20)
passed bounded independent review:77wholeclauses, eight retained-file-only S
routes and69unsupported application clauses. All194actual records remain U,
including documentary/file checks. D11 applicability, current controls/receiver/
output and lifecycle stay unknown. No application grade, release or closure.

## Current observation preparation — 2026-10-23

[The reviewed137-record Windows preparation](../research/phase4-probe-batch.md#remaining137-windows-preparation-adopted--2026-10-23) classifies prospective questions and supplies the Session0tool/version checklist. Its107conditionally applicable,15hardware/plugin-dependent and15macOS-dependent records preserve mixed prerequisites, original predicates and source-version gaps. These are preparation dispositions, not supported feature outcomes. Actual guest/tool capabilities remain unknown; no O observation or family completion is added. Amp/Cabinet’s blocked extracted-audio route, the idle implementation workspace and the deferred implementation milestone remain governed by the [current plan](../research/full-live-specification-plan.md#current-execution-checkpoint).

The current owner pointers above supersede older draft-revision navigation in this table. They do not change the feature inventory, published release payloads or required unsupported outcomes. The full inventory and behavioral denominator remain distinct.


[Analog local-chain static progress](../research/device-analog-dsp.md#expanded49-native-study-adopted-local-chains-and-complete-frontier--2026-10-23) narrows conditional internal receiver/output legs without a new externally observable contract or acceptance grade. Current R15 case scope and every unresolved runtime/public behavior remain unchanged; the [atlas](../research/program-structure.md#analog-factory-dependency-chain-progress--2026-10-23) routes further metadata work. No whole-device or whole-product completion follows.


[Current S evidence disposition](../research/full-live-coverage-inventory.md#frozen-s-route-scope-assessment-and-new-metadata-questions--2026-10-23):the qualified whole AClip hook is adopted as local static evidence, while Automationnativev2 remains unreviewed partial and MNSmetadata remains pre-acquisition. Their public joins stayU. [Shared capacity hold](../research/native-analysis-recovery.md#shared-filesystem-capacity-stop--2026-10-23) changes execution eligibility, not requirement/case/grade/release counts or product completion.
