---
id: NAV-SPECS
type: index
status: active
updated: 2026-10-19
access: analysis
---

# Behavioral specification index

Specifications define what must be observable, independent of the original's
internal implementation. This directory contains analyst-side drafts. 30 reviewed releases approve
explicitly partial clauses only; 19 are current. The
[handoff catalog](../../handoff/index.md) lists them with their supersession chains.
Each handoff plan's Review outcome section lists the corrections owed to its draft
spec.

| Page                                                                 | Purpose                                                                                                                                                                                                                                                                                                                                                   |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [MIDI configuration handoff plan](midi-config-handoff-plan.md)       | Finite static-supported release candidate and review gates                                                                                                                                                                                                                                                                                                |
| [MIDI configuration v2 handoff plan](midi-config-v2-handoff-plan.md) | Released midi-config-v2 (109 cases): scope, narrowing, traceability                                                                                                                                                                                                                                                                                       |
| [Full Live coverage design](../research/full-live-specification-design.md) | Governing full-product denominator and behavioral/case closure rules |
| [Full Live execution plan](../research/full-live-specification-plan.md) | Current work selector for extending coverage beyond T1 |
| [Feature map](feature-map.md)                                        | Whole-app planning inventory and stable feature IDs                                                                                                                                                                                                                                                                                                       |
| [ALS container](als-container.md)                                    | Revision 2 draft: container recognition, root and version envelope, save envelope; 9 requirements, 27 unexecuted cases, 7 probes; partial 001 to 006 released as als-container-v1 |
| [ALS container handoff plan](als-container-handoff-plan.md)          | Released als-container-v1 (35 cases, approved with narrowing): scope, exclusions, traceability |
| [Transport state](transport-state.md)                                | Revision 5 draft: 12 requirements; REQ-011 k from binary64-rounded log10 with its 1/4 to 3/4 band and accuracy assumption, negative zero, REQ-006 integer rule and meter codes settled by extracted execution; 36 graded cases (26 X, 7 S, 3 U), TS-023 withdrawn; 33 released as [transport-state-v3](../../handoff/transport-state-v3/README.md), superseding transport-state-v2 |
| [Plug-in discovery](plugin-discovery.md)                             | Revision 2 draft: 16 requirements (2 D and S with U parts, 10 S with U parts, 4 U only); 62 unexecuted cases (56 graded, 6 unresolved); release cases adopted as PD-043 to 062; partial clauses released as [plugin-discovery-v1](../../handoff/plugin-discovery-v1/README.md) (35 cases) |
| [Plug-in hosting workflows](plugin-hosting.md) | Reviewed partial draft: 21 requirements/40 cases for configuration, editor, sidechain and program workflows; independent partial review approved, all exact-build outcomes unknown |
| [Arrangement editing](arrangement-editing.md) | Revision 1 partial draft: 35 requirements, 65 scenarios; independent source/scope review approved; exact-build parity and error/undo/cancel/persistence outcomes unknown |
| [Recording and comping](recording-comping.md) | Revision 1 partial draft: 32 requirements, 81 scenarios; documentary/observed-file expectations distinguished from target unknowns; independent review approved corrected partial scope |
| [Bundled-device hosting](bundled-device-hosting.md) | Revision 2 partial draft: 12 requirements (one synthetic conditional composition, eleven U), 26 entries (3 arithmetic/23 U); eleven internal models excluded from compatibility coverage; independent review approved classification |
| [Device chains and racks](device-racks.md) | Revision 1 partial draft: 28 requirements/61 cases for four rack types and selected common device actions; review corrections independently verified |
| [MIDI editing and tools](midi-editing-tools.md) | Revision 1 partial draft: 43 requirements/57 cases, including individual clauses for 17 tools; manual conflicts and exact-build U retained; separate partial-draft review approved |
| [Sets, projects and media workflows](project-media-workflows.md) | Revision 1 partial draft: 22 requirements/34 authored cases; Set/template/merge/reference/collect/Pack/Undo History scope; corrected partial draft independently reviewed |
| [Browser workflows](browser-workflows.md) | Revision 1 partial draft: ten D12 interaction requirements, twelve acceptance setups; exact-build applicability and error/lifecycle outcomes unknown; independent partial-draft review approved |
| [Audio and video export](audio-video-export.md) | Partial draft: 23 requirements/34 scenarios; corrected documentary predicates independently reviewed; encoding, timing, failures and exact-build behavior remain unknown |
| [Media import/cache/analysis/interchange](media-file-workflows.md) | Reviewed partial draft: 17 requirements/32 cases for audio import, cache/ASD/default clips, MIDI and Live Clip workflows; reviewed with citation/count corrections confirmed; codec/numerical/lifecycle and target behavior unknown |
| [Native MIDI effects](native-midi-effects.md) | Partial draft: 27 requirements/146 cases for eight devices; corrected author revision 2 independently reviewed; all exact-build outcomes unknown |
| [Utility](device-utility.md) | Reviewed partial draft: 15 requirements/37 cases; documentary control behavior and three package-file checks; audio interactions and exact-build behavior unknown |
| [Tuner](device-tuner.md) | Reviewed partial draft: 12 requirements/32 cases; documentary controls and one package-file check; pitch detection/calibration and exact-build behavior unknown |
| [Spectrum](device-spectrum.md) | Reviewed partial draft: 14 requirements/34 cases; documentary controls and two package-file checks; FFT/window/averaging/calibration and exact-build behavior unknown |
| [MPE workflows](mpe-workflows.md) | Reviewed corrected partial draft: 18 requirements/27 cases; codec/channel/allocation/lifecycle and build outcomes U |
| [Tuning systems](tuning-systems.md) | Reviewed corrected partial draft: 21 requirements/32 cases; parser/tuning/numeric/build gaps remain |
| [Groove workflows](groove-workflows.md) | Reviewed corrected partial draft: 14 requirements/24 cases; nonidentity Commit fixture corrected; random/numerical and exact-build outcomes unknown |
| [Simpler](device-simpler.md) | Reviewed corrected partial draft: 23 requirements/35 cases |
| [Sampler](device-sampler.md) | Reviewed corrected partial draft: 24 requirements/35 cases; multisample/zone/control/version and lifecycle gaps retained |
| [Impulse](device-impulse.md) | Reviewed corrected partial draft: 14 requirements/18 cases |
| [Filter and EQ devices](filter-eq-devices.md) | Partial draft: 65 requirements/128 cases for four current devices; nonvacuous modulation fixtures corrected and independently verified; legacy applicability and numerical outcomes remain open |
| [Keyboard navigation and accessibility](keyboard-navigation.md) | Partial author draft: 21 requirements/42 cases plus a separate 292-row shortcut discovery catalog; corrected partial scope independently reviewed, context/platform/build and lifecycle gaps remain |
| [Dynamics devices](dynamics-devices.md) | Reviewed partial draft: 62 requirements/129 cases across Compressor, Gate, Glue Compressor, Limiter and Multiband Dynamics; independent partial review approved; numerical, lifecycle and exact-build gaps remain |
| [Audio-to-MIDI conversion](audio-to-midi.md) | Partial author draft: 14 requirements/29 cases for audio-clip Slice/Harmony/Melody/Drums wrappers; corrected partial scope reviewed; recognition/numerical/lifecycle and exact-build outcomes unknown |
| [Delay and reverb devices](delay-reverb-devices.md) | Reviewed corrected partial draft for seven devices; 92 requirements/149 cases; Echo internal idle-shutdown context left U/null; exact-build, feedback/timing/DSP and lifecycle gaps remain |
| [Distortion devices](distortion-devices.md) | Frozen partial author packet for nine devices: 67 requirements/190 cases; corrected partial review approved; signal laws, numerical, legacy/build and lifecycle outcomes unknown |
| [Modulation, pitch, spectral and looping devices](modulation-pitch-loop-devices.md) | Reviewed partial draft for ten devices: 106 requirements/186 proposed cases; all exact-target outcomes null/U; signal, lifecycle, clock and codec gaps remain |
| [Synthesis and drum instruments](synthesis-instruments.md) | Reviewed partial draft for Drift, Drum Sampler, Meld, Operator and Wavetable: 109 requirements/154 cases; independent partial-scope review approved; source/context and all target outcomes remain unknown |
| [External hardware devices](external-hardware-devices.md) | Partial author draft:24 requirements/56 cases for External Audio Effect/Instrument; corrected partial scope independently reviewed; all target outcomes null/U |
| [Legacy native devices](legacy-native-devices.md) | Reviewed partial predecessor/file packet for eight profiles:77 requirements/178 cases; D11 contracts do not establish target legacy parity |
| [Clip View workflows](clip-view-workflows.md) | Reviewed partial draft:54 requirements/62 cases; shared panels/regions/audio properties; MIDI utility source contexts and all target outcomes remain U |
| [Session View workflows](session-view-workflows.md) | Corrected partial draft:29 requirements/40 cases for grid/scenes/selection/transfer; metadata ownership narrowed and independently verified |
| [Max for Live hosting/templates](max-for-live-hosting.md) | Partial author draft:38 requirements/64 cases, five template roles/file identities; corrected partial scope independently reviewed; API/patch/lifecycle/build outcomes remain U |
| [Max for Live devices](max-for-live-devices.md) | Twenty individual partial profiles:135 requirements/315 cases; current and dated documentary sources separated; partial scope independently reviewed, all target outcomes U |
| [Video workflows](video-workflows.md) | Frozen partial author draft:18 requirements/28 cases for import/presentation/scoring/pre-roll; independent partial-scope review approved; no movie/codec/frame/audio execution |
| [Routing, monitoring and latency](routing-monitoring-latency.md) | Frozen partial author draft:40 requirements/69 cases; general route/tap/monitor/cue/compensation controls, partial scope independently reviewed; all target outcomes U |
| [Bundled-device workflows](bundled-device-workflows.md) | 55 requirements/118 cases; seven broader profiles independently reviewed as partial; numeric/DSP owners unchanged; all target outcomes U |
| [Session launch and Follow workflows](session-launch-workflows.md) | 43 requirements/68 cases; partial scope independently reviewed; timing/chance/action-context questions retained; all target outcomes U |
| [Bounce and Freeze workflows](bounce-freeze-workflows.md) | 41 requirements/77 cases; partial scope independently reviewed; current/D11 predecessor contexts separated; all target outcomes U |
| [Synchronization workflows](synchronization-workflows.md) | 26 requirements/36 cases; partial scope independently reviewed; Link/Link Audio/Follower/Clock/MTC roles; all target outcomes U |
| [Settings, Learn and Info View](settings-learning-workflows.md) | 21 requirements/30 cases; partial scope independently reviewed; target/newer-feature applicability and delivery/lifecycle unknowns retained |
| [Warp editing/playback workflows](warping-workflows.md) | 50 requirements/88 cases; partial scope independently reviewed; automatic/DSP/clock/import/lifecycle gaps retained |
| [Remote-control workflows](remote-control-workflows.md) | 37 requirements/47 cases; corrected R2 partial scope independently reviewed; generic MIDI/key/surface setup, all target outcomes U |
| [Stem separation](stem-separation.md) | 18 requirements/29 cases; partial scope independently reviewed; source/group/file roles, signal and target applicability U |
| [Automation workflows](automation-workflows.md) |62 requirements/76 cases from192 Automation/Clip Envelopes source blocks; partial scope independently reviewed; finite existing owners and source questions retained |
| [Push1/Push2 workflows](push-controller-workflows.md) |65 requirements/77 cases from706 retained per-model blocks; partial scope independently reviewed (330blocks semantically read,706mechanically reproduced); hardware/LED/MIDI/Push3/profile gaps remain U |
| [Engine/resource workflows](engine-resource-workflows.md) |28 requirements/50 cases from195 resource/audio/MIDI fact-sheet blocks; partial scope independently reviewed; all numerical/performance/target outcomes U |
| [Delivery and recovery workflows](delivery-recovery-workflows.md) | 45 requirements/60 cases from300 official Help body blocks; partial scope independently reviewed; original HTML403 retained, target/platform/operational outcomes U |
| [Live API bridge workflows](live-api-bridge-workflows.md) | 52 requirements/61 cases from893 publisher reference blocks; partial scope independently reviewed; alltargetU and588LOM member semantics separate |
| [Browser content/services workflows](browser-content-workflows.md) | 56 requirements/71 cases from274 retained blocks; partial scope independently reviewed; accounts/services/similarity/protocol/target outcomes U |
| [Shared workspace controls](application-workspace.md) | 13 requirements/23 cases; partial scope independently reviewed; ControlBar/globalScale/StatusBar/dual-window predicates, detailed owner boundaries retained |
| [Clip/Sample API members](live-api-clip-sample.md) | Five references/131 direct declarations;143 requirements/163 cases, independent partial-scope review approved; inherited/version/typed-payload/lifecycle outcomes U |
| [Control/routing/groove/tuning API members](live-api-control-tuning.md) | Six references/28 direct declarations plus zero-member root;33 requirements/41 cases, corrected R2 partial scope independently reviewed; dictionary/unit/ownership/target outcomes U |
| [Core/Session API members](live-api-core-session.md) | Ten references/226 direct declarations;234 requirements/262 cases, corrected R2 partial scope independently reviewed; source-specific typed/member/lifecycle/target gaps remain U |
| [Device/rack API members](live-api-device-rack.md) | Ten references/95 direct declarations;103 requirements/113 cases, independent partial-scope review approved; heading-only DrumPad.delete_all_chains stays U |
| [Specialized device API members](live-api-specialized-devices.md) | Fourteen references/108 direct declarations;113 requirements/123 cases, partial scope independently reviewed; omitted signatures/types/units and all target outcomes U |
| [Mixer interactions and groups](mixing-workflows.md) | 23 requirements/33 cases from94 retained Mixing blocks; partial scope independently reviewed; numeric/routing/record/Session owners retained and five source contexts U |
| [APC startup source evidence and unknowns](apc-controller-capabilities.md) | Eight exact startup-module captures; corrected R2 retains37nonnormative research records,6U obligations/12U cases; reclassification independently reviewed,zero supported runtime contracts |
| [Update helper workflows](update-helper-workflows.md) | 30 requirements/37 all-null proposals from bounded retained Swapper/launcher evidence;21S/1inference/8U, independently reviewed as partial static roles; no helper executed |
| [Browser index](browser-index.md)                                    | Revision 2 draft: 13 requirements (12 with static-derived clauses, 012 unknown only); 68 case IDs (66 active: 36 static-derived, 30 unknown; 2 withdrawn); sidecars bind to direct files only; partial clauses released as [browser-index-v1](../../handoff/browser-index-v1/README.md) (26 cases) |
| [Clip launch](clip-launch.md)                                        | Revision 5 draft: 23 requirements; launch timing settled for Trigger (A1, via SPEC-PLAYBACK-CORE); REQ-017 offset is the track player's pre-delay; sample-exact timing replaces the ±1/64-beat tolerance; 64 cases (61 graded, 3 with unresolved parts); partial clauses released as [clip-launch-v2](../../handoff/clip-launch-v2/README.md) (100 cases) |
| [MIDI note storage](midi-note-storage.md)                            | Revision 4 draft: 17 requirements; value limits, time grid and saved number text settled by extracted execution; no MidiKey range guard (REQ-011 permanently excluded); 75 cases (61 gradable: 17 X, 44 S or D; 6 blocked; 8 U); partial clauses released as [midi-note-storage-v2](../../handoff/midi-note-storage-v2/README.md) (72 cases) |
| [Bundled device parameters](bundled-device-parameters.md)            | Revision 3 draft: 15 requirements (1 D only, 2 D and S, 12 with U parts) and tables in document order for the seven bundled devices; 37 cases (4 not graded, 4 with unresolved parts); Cabinet microphone labels corrected; DryWet 0..1; partial clauses released as [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md) (82 cases) |
| [Automation envelopes](automation-envelopes.md)                      | Revision 5 draft: 13 requirements; evaluator values (X) separated from playback values: playback curves are a 16-piece polyline, the first point sits at −10⁷ beats, and at a step the later event applies; Volume and Send envelopes hold fader positions; 33 case IDs (27 gradable, 4 unresolved, 2 withdrawn); partial clauses released as [automation-envelopes-v2](../../handoff/automation-envelopes-v2/README.md) (21 cases) |
| [Warp markers](warp-markers.md)                                      | Revision 5 draft: 16 requirements; beat and sample conversion, shadow marker and REQ-015 and 016 edges by extracted execution; REQ-009 corrected: warped playback uses the scripting mapping, unwarped session clips ignore markers; 39 cases (7 X, 25 D or S, 7 U); partial clauses released as [warp-markers-v2](../../handoff/warp-markers-v2/README.md) (63 cases) |
| [Mixer values](mixer-values.md)                                      | Revision 5 draft: 15 requirements; round-trip identity limited to seven tested curve points; values reaching the engine settled statically under mix-graph conditions A3 to A5; 48 cases (6 X, 20 static, 11 renders, 11 ungraded); partial clauses released as [mixer-values-v2](../../handoff/mixer-values-v2/README.md) (80 cases) |
| [Live Set structure](live-set-structure.md) | Revision 2 draft (T1.1): 18 requirements covering the reading model, tracks, chains, slots and scenes, clip containers, sample references, device chains, sends, automation targets, Ids and save. Opening always runs the validation walk (A1 and A2 settled). 40 cases (33 graded, including 1 X, and 7 U). Device-free minimal set T11-MIN; 34 cases released as [live-set-structure-v1](../../handoff/live-set-structure-v1/README.md) |
| [Mix graph](mix-graph.md) | Revision 2 draft (T1.4): general round-trip identity withdrawn; 16 requirements covering mixer matrices, pre- and post-fader sends, summing, mute and solo, per-sample ramps and automation playback. Q-019 settled with conditions. 34 cases (12 X, 11 conditional composed renders, 10 U, 1 withdrawn). Partial clauses in 28 cases released as [mix-graph-v1](../../handoff/mix-graph-v1/README.md) |
| [Playback core](playback-core.md) | Revision 2 draft (T1.3): 23 requirements (15 with X parts, 13 S-cond, 3 with D parts, 19 with U parts) covering transport, launch timing, MIDI note emission and unwarped audio playback. Launch timing settled for Trigger. 68 case IDs (60 fully graded, 2 partly graded, 6 ungraded; 7 accept P or P+1 at 48 kHz). Partial clauses released as [playback-core-v1](../../handoff/playback-core-v1/README.md) (92 cases) |
| [Corpus device](device-corpus.md) | Revision 3 draft (T1.2): Corpus audio specified from extracted execution of the bundle's own x86_64 code; 13 requirements; 28 cases (24 graded against retained reference renders, 4 U). Filter default and startup numerical floor corrected; proposed metric: per-mode frequency, decay and amplitude bounds, third-octave levels for broadband. Partial output clauses released as [device-corpus-v1](../../handoff/device-corpus-v1/README.md) (24 groups, 68 evaluations) |
| [Corpus device handoff plan](device-corpus-handoff-plan.md) | Released device-corpus-v1: 24 groups / 68 finite evaluations, independent metric review and omitted-mode scope |
| [Electric device](device-electric.md) | Revision 2 draft (T1.2): Electric audio from extracted execution; 16 requirements; voice limit is the Polyphony index + 2; 32 cases (23 graded by renders, 5 by X rules, 4 U); tolerances derived from reseeded and libm variants. Partial output clauses released as [device-electric-v2](../../handoff/device-electric-v2/README.md) (117 evaluations) |
| [Electric device handoff plan](device-electric-handoff-plan.md) | Released device-electric-v2: 117 finite mono output evaluations with calibrated masks and exclusions |
| [Tension device](device-tension.md) | Revision 2 draft (T1.2): Tension audio from extracted execution; 15 requirements; 42 cases (27 graded by renders, 12 exact-value checks, 3 U); metric on waveform and partials, statistical for chaotic settings. Partial outputs released as [device-tension-v1](../../handoff/device-tension-v1/README.md) (27 finite evaluations) |
| [Tension device handoff plan](device-tension-handoff-plan.md) | Released device-tension-v1: 27 calibrated outputs; chaotic/uncalibrated settings excluded |
| [Analog device](device-analog.md) | Revision 1 draft (T1.2): Analog audio from extracted execution; 23 requirements; exact laws for pitch, filters, envelopes and saturators; 47 cases (42 graded by renders, 1 statistical, 4 U). Selected outputs released as [device-analog-v1](../../handoff/device-analog-v1/README.md) (38 groups, 42 finite evaluations) |
| [Analog device handoff plan](device-analog-handoff-plan.md) | Finite device-audio release; independent review and publication complete |
| [Collision device](device-collision.md) | Revision 1 partial draft (T1.2): resonator-default silence explained; event grid, pitch, voices and routing from retained extracted execution. 18 requirements, 50 cases (31 retained fixtures with proposed comparisons, five measurement checks including partly U DCL-046, 14 U); draft metrics provisional; 2 cases released as [device-collision-v1](../../handoff/device-collision-v1/README.md); exact recovered-original evidence is mapped separately from two concurrent edits |
| [Collision device handoff plan](device-collision-handoff-plan.md) | Released device-collision-v1 (2 cases): effective silence and calibrated Pipe only |
| [Transport-state handoff plan](transport-state-handoff-plan.md)      | Released transport-state-v1 (18 cases, approved with narrowing): scope, exclusions, traceability |
| [Transport-state v2 handoff plan](transport-state-v2-handoff-plan.md) | Released transport-state-v2 (33 cases, approved with listed clarifications; supersedes v1): scope, change list, traceability, review outcome |
| [MIDI user mapping](midi-user-mapping.md)                            | Revision 6 draft: 13 requirements; takeover (Pick-Up, Value Scaling, reversed ranges, first 14-bit pair) settled by extracted execution; tolerance max(1e-6, 2⁻²² × max(abs min, abs max)); cases MT-01 to 56 (18 S, 34 X, 4 S-cond); [midi-config-v4](../../handoff/midi-config-v4/README.md) released (161 cases) |
| [MIDI configuration v3 handoff plan](midi-config-v3-handoff-plan.md) | Released midi-config-v3 (127 cases, approved): scope, exclusions, traceability, review outcome |
| [Clip launch handoff plan](clip-launch-handoff-plan.md) | Released clip-launch-v1 (50 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [MIDI note storage handoff plan](midi-note-storage-handoff-plan.md) | Released midi-note-storage-v1 (67 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [Mixer values handoff plan](mixer-values-handoff-plan.md) | Released mixer-values-v1 (37 cases, approved with corrections): scope, exclusions, traceability, review outcome |
| [Automation envelopes handoff plan](automation-envelopes-handoff-plan.md) | Released automation-envelopes-v1 (21 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [Bundled device parameters handoff plan](bundled-device-parameters-handoff-plan.md) | Released bundled-device-parameters-v1 (82 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [Browser index handoff plan](browser-index-handoff-plan.md) | Released browser-index-v1 (26 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [Plug-in discovery handoff plan](plugin-discovery-handoff-plan.md) | Released plugin-discovery-v1 (35 cases, approved with clarifications): scope, exclusions, traceability, review outcome |
| [Warp markers handoff plan](warp-markers-handoff-plan.md) | Released warp-markers-v1 (38 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [MIDI configuration v4 handoff plan](midi-config-v4-handoff-plan.md) | Released midi-config-v4 (161 cases, approved with narrowing): scope, change list, traceability, review outcome |
| [Transport-state v3 handoff plan](transport-state-v3-handoff-plan.md) | Released transport-state-v3 (33 cases, approved with listed clarifications): scope, change list, traceability, review outcome |
| [MIDI note storage v2 handoff plan](midi-note-storage-v2-handoff-plan.md) | Released midi-note-storage-v2 (72 cases, approved with listed clarifications): scope, change list, traceability, review outcome |
| [Mixer values v2 handoff plan](mixer-values-v2-handoff-plan.md) | Released mixer-values-v2 (80 cases, approved with narrowing): scope, change list, traceability, review outcome |
| [Mix graph handoff plan](mix-graph-handoff-plan.md) | Released mix-graph-v1 (28 cases, approved with narrowing): scope, change list, traceability, review outcome |
| [Playback core handoff plan](playback-core-handoff-plan.md) | Released playback-core-v1 (92 cases): independent review, finite scope, exclusions and comparison checks |
| [Live Set structure handoff plan](live-set-structure-handoff-plan.md) | Released live-set-structure-v1 (34 cases, approved with narrowing): scope, change list, traceability, review outcome |
| [Automation envelopes v2 handoff plan](automation-envelopes-v2-handoff-plan.md) | Released automation-envelopes-v2 (21 cases, approved with listed corrections): scope, change list, traceability, review outcome |
| [Warp markers v2 handoff plan](warp-markers-v2-handoff-plan.md) | Released warp-markers-v2 (63 cases, approved with narrowing): scope, change list, traceability, review outcome |
| [Clip launch v2 handoff plan](clip-launch-v2-handoff-plan.md) | Released clip-launch-v2 (100 cases, approved with narrowing): scope, change list, traceability, review outcome |

**Browse every requirement in one place:** the
[requirements browser](../../analysis/ableton-live-12.4.3/browse/specs/index.html)
lists each draft-spec requirement and each candidate below in one searchable
table, linked back to its source section. Regenerate it with
`python3 tools/spec_browser.py`.

## Candidate specifications

Revision 2 research packets propose candidate requirements from shipped files
and decompiled code. None is a draft spec yet and none is released. The source
section owns the evidence, its strength and the open questions. One row per
target spec:

| Target | Candidates | Source section | Next step |
| --- | --- | --- | --- |
| SPEC-CORPUS-DEVICE | CD-C01–CD-C08 (8) | [Corpus DSP (decompiled)](../research/corpus-dsp-static.md#candidate-requirements-for-spec-corpus-device) | Live-side conversion (N5), then Phase 4 measurements |

When a candidate set becomes a draft under this directory, replace its row
here with the draft's catalog row above.

Author bounded contracts with the [spec template](../../templates/spec.md).
Each future spec gets requirement IDs, a feature-map link, original-side evidence,
and acceptance cases. Add its catalog row here in the same change.

Approved snapshots are listed in the [handoff index](../../handoff/index.md).
Candidate code and design are maintained in [implementation](../implementation/index.md);
original-versus-candidate results are maintained in [verification](../verification/index.md).
