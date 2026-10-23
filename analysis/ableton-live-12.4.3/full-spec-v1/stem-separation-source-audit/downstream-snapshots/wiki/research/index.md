---
id: NAV-RESEARCH
type: index
status: active
updated: 2026-10-19
access: analysis
---

# Research index

Research pages hold original-side evidence and synthesis. They are not inputs
to the isolated implementation workspace.

| Page | Purpose |
| --- | --- |
| [Learning route](learning/index.md) | Human-readable method, glossary and worked investigations |
| [Program structure atlas](program-structure.md) | Observed package boundaries, traced relationships and explicit unknowns |
| [Phase execution plan](native-phase-execution.md) | Authorized sequence, resource envelope and actual milestone ledger |
| [Compact artifacts and continuation](native-compact-storage.md) | Exact compressed archives, current offline reader, interaction repair and durable-analysis tasks |
| [Native analysis recovery design](native-analysis-recovery.md) | Persistent checkpoint tooling, reviewed proofs, resource gates, disk inventory and target recovery status |
| [Native transport study](native-transport-study.md) | Loop-enable persistence and Start/Stop investigation design, exact seeds and case boundaries |
| [Transport transitions (native)](transport-transitions-native.md) | S3: Start/Stop dispatch resolved (OSetPlayingCommand to the engine, reflected by TransportEngineStateChanged), engine-donor symbol matches, static transition table T-01 to T-13, ADR 0002 escalation record |
| [Clip launch](clip-launch.md) | S5: clip and set launch fields over 203 schemas and 4,130 shipped clips; enum values; constructor and preference defaults; load normalization and migration; quantization grid and launch-boundary rule; candidates CL-01 to CL-23; PRB-S5-01 to 11 |
| [MIDI note storage](midi-note-storage.md) | S7: KeyTrack and MidiNoteEvent shape and schema evolution, values in 1,368 shipped clips, reader (reused note object, defaults, clamps, 1/3,843,840 grid, NoteId uniqueness and renumbering, per-note expression and group checks) and writer; MN-01 to MN-24, PRB-S7-01 to 10 |
| [Mixer values](mixer-values.md) | S9: track mixer storage across schemas and 376 shipped sets; defaults and ranges; seven fader curves, dB and pan text, engine −∞ floor (gain ≤ 0.00032 becomes 0), pan law, crossfade assign; candidates MX-01 to MX-15; PRB-S9-01 to 08 |
| [Automation envelopes](automation-envelopes.md) | S6: envelope storage (track AutomationEnvelopes, ClipEnvelope, PointeeId targets), invariants over 4,365 shipped envelopes, load checks, curve rules, float, Bool and Enum evaluation; AE-C01 to C17, PRB-S6-01 to 07 |
| [Warp markers and settings](warp-markers.md) | S8: clip and Simpler/Sampler warp fields over 203 schemas and 14,494 shipped marker lists; shadow marker 1/32 beat after the last marker; empty AudioClip list is a load error; piecewise-linear beat mapping (inferred); warp-mode and transient enumerations, ranges and defaults; WM-01 to WM-16; 11 probes |
| [Linker function-start index design](function-starts-design.md) | Bounded Mach-O metadata navigation, distinct from analyzer-discovered functions |
| [Native export design](native-export-design.md) | Owned transport, immutable ingestion and recovery design |
| [Native export task plan](native-export-execution.md) | Implementation tasks and tool-validation state |
| [Investigator query route](r2-query-route.md) | REA 6.5.0 versus saved projects, Push2 measurements, the R2FunctionDossier query server and concurrency choice |
| [R2 corpus tooling](r2-corpus-tooling.md) | C1 bulk decompile and C2 index scripts: design, Push2 measurements, Live projection and run command |
| [Next major phase roadmap](native-decompilation-roadmap.md) | Main Live code export, method/structure atlas and first handoff milestones; [revision 2](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17) adopted 2026-10-17 |
| [Phase 4 probe batch](phase4-probe-batch.md) | Run sheet for the macOS sitting: 79 runtime records from S4, N1 to N5, H1, H2, H4 and H5 in 11 sessions by prerequisite; 7 merge groups, 3 incomplete; fixture plan and safety measures |
| [Binary and decompilation artifacts](artifacts/index.md) | Start here: searchable browser, package map, pseudocode, symbols and decoded modules |
| [LLM Wiki source](sources/llm-wiki.md) | User-supplied documentation pattern and its project adaptation |
| [REA reading list](sources/rea-reading-list.md) | External methodology references with explicit archival limitations |
| [Ableton analysis intake](sources/ableton-analysis-intake.md) | Historical intake record; superseded by the installed Ableton source page |
| [Installed Ableton source](sources/ableton-live-12.4.3.md) | Pinned build, retained evidence, hashes and environment |
| [Official Ableton Help captures](sources/ableton-live-help.md) | Nine public article JSON/body sources;300 blocks for reviewed partial delivery/recovery workflows, Dhelp distinguished from D12 and target applicability U |
| [Cycling74 Live API inventory](sources/cycling74-live-api.md) |53retained publisher pages;45LOM reference entries/588explicit declarations and6bridges; source inventory independently reviewed as discovery only, index declares12.4.5 and all target applicability U |
| [Package structure](ableton-package-structure.md) | Observed native/resource boundaries and coverage limits |
| [x86_64-only bundles](x86-only-bundles.md) | Live Engine is a ReWire device build of the engine; ReWire 1.8.7 install chain is x86_64-only; MultiF0 audio-to-note API; engine as symbol donor for S3 |
| [Live x86_64 paths](x86-live-paths.md) | N8: ReWire install chain gated off by constant-false checks in Live and the Engine; MultiF0 built-in by default; Convert Drums uses a separate drum task; MultiF0 record fields as Live reads them; x86_64 transport matches arm64 including both Stop transfers; PRB-N8-01 to 05 |
| [Plug-in scanner (static)](plugin-scanner-static.md) | H1: scanner options, VST3 and VST2 enumeration, scan-state database, crash and limit derivation, messages to Live, 14 candidate requirements, 8 probes |
| [Plug-in hosting workflows](plugin-hosting.md) | Current-manual parameter/editor/sidechain/program evidence; partial scope independently reviewed; scanner/API/DSP unknowns separate |
| [Browser index (static)](browser-index-static.md) | H2: index helper launch and messages, files database schema and versioning, scan pipeline, XMP tag sidecars, previews, `filerefmap.db`; 12 candidate requirements, 9 probes |
| [Device bundles (static)](device-bundles-static.md) | H4: seven device bundles share one 7-function C interface with three implementations; Live owns parameter names and stored domains; 502-parameter inventory over 1,064 shipped occurrences; 5 probes |
| [Device parameter mapping (native)](device-parameter-mapping-native.md) | N5: how Live loads the seven bundles, uses GetPlugInfoU and sets parameters; complete index and conversion tables for Amp, Cabinet, Electric and Corpus (82 rows); 4 probes |
| [Device tables (native)](device-tables-native.md) | N6: index and conversion tables for Analog, Tension and Collision (472 entries), checked against the bundles' tables and disassembly; constructor defaults for 417 parameters; loader and value-text checks; probe P4-N6-01 |
| [Corpus DSP (decompiled)](corpus-dsp-static.md) | Corpus signal chain from the decompiled bundle: 37 host parameters with Live- and device-side conversions, module graph, five modal and two waveguide resonator models, quirks, candidates CD-C01 to CD-C08; port checks and the published traced demo |
| [Push 3 helper (static)](push3-helper-static.md) | H5: Push3.app identity, launch options and watchdog, USB and MIDI hardware interfaces, nanomsg, document-sync and shared-memory links to Live, Push 2 comparison, nine probes |
| [Web connector, add-ons, swapper (static)](web-addons-swapper-static.md) | H6: helper roles, launch and messages, service endpoints, `.asu` and xdelta update with swap and rollback, add-on backends; scope classification |
| [Helper launch, Live side](helper-launch-live-side.md) | N4: shared process controller and timeouts, nanomsg bind and connect roles, wire framing, per-helper arguments, start conditions and restart caps for the scanner, index, add-ons, web connector, swapper and Push 3; MultiF0 selection; 9 probes |
| [Document container (static)](document-container-static.md) | S2 static half: gzip/XML envelope, root attributes, schema-version cross-check, native loader anchors |
| [Document container (native)](document-container-native.md) | S2 native half (N2): stream detection, root and version checks, newer-version versus corrupt paths, runtime `Schema/*.txt` lookup, save writer; 27 cases, 7 probes |
| [Transport-state fields (static)](transport-state-static.md) | S1 static half: Transport, tempo and time-signature schema evolution, values in 376 shipped sets and clips, candidate SPEC-TRANSPORT-STATE statements, native anchors and queries |
| [Transport-state fields (native)](transport-state-native.md) | S1 native half: reader, member registry, loader and writer for tempo, time signature and loop fields; tokens, defaults, duplicates, save number format, time-signature code; PRB-N1 probes |
| [Decompilation preparation](ableton-decompilation-preparation.md) | Validated helper pipeline, core targets and prioritized spec work |
| [MIDI mapping source capture](sources/midi-user-mapping-12.4.3.md) | Pinned documents, bytecode and static decoder provenance |
| [MIDI mapping investigation](midi-user-mapping.md) | Parser/mapping findings and unresolved native/host boundaries |
| [MIDI closure assessment (S4)](midi-closure-r2.md) | Clause-level static/native/runtime classification of the 13 MIDI requirements, 55 draft v2 cases, 16 Phase 4 probes |
| [MIDI map-mode transforms (native)](midi-transforms-native.md) | N7: native path from the user script to the parameter value; per-mode table for all ten modes, 14-bit pairing, relative step and acceleration tables, quantized and on/off handling, takeover arithmetic, 23 derived cases, PRB-N7-01 to 05 |
| [Extracted execution (X1)](extracted-execution.md) | Harness that runs original x86_64 Live functions on this host (ADR 0003, label X); pilot agrees with all 70 released checks (mixer text, MIDI values, transport number text); finds REQ-TRANSPORT-STATE-011 imprecise next to powers of ten and an arm64 FMA in Absolute mode; triage of probes it can settle |
| [Live Set structure (T1.1)](live-set-structure.md) | Schema conformance, reader refusals and repairs, sample CRC (X). The open path always runs the validation walk. Audit of released fixtures: 204 refused  Versioned checker successor corrects 11.0_405 scene/main-track measurements; sealed v1 evidence retained |
| [Mix graph (T1.4)](mix-graph.md) | Track output stage, sends, solo, ramps, automation playback. Q-019 settled with conditions. Corrections to automation A1 and REQ-010 |
| [Playback core (T1.3)](playback-core.md) | Engine timing, launch pre-delay, MIDI note emission, unwarped audio playback; launch-timing A1 settled for Trigger |
| [Device DSP by extracted execution (T1.2)](device-dsp-extracted.md) | Gate passed: the bundle loader works, Corpus renders are bit-repeatable and agree with the static model, Analog's note grid is exactly 1 ms, libm and FMA effects are described, effort per device is estimated |
| [Electric device DSP](device-electric-dsp.md) | 120 retained renders; Polyphony settled; KeyboardStretch is a ±7.2-cent detune; corrections to the t12 probe and the Volume default |
| [Tension device DSP](device-tension-dsp.md) | 68 deterministic renders on a 1 ms note grid; partials, sections and voices; floating-point sensitivity sets the metric |
| [Analog device DSP](device-analog-dsp.md) | Renders reproduced bit for bit; exact laws for pitch, filters, envelopes and saturators; voice stealing and mono priority |
| [Collision device DSP](device-collision-dsp.md) | T1.2: constructor silence explained; 380 event-grid checks, modal/voice/level evidence and 41 retained renders; exact original recovery maps two preserved concurrent edits; noise and host-protocol gaps remain |
| [Full Live product inventory](full-live-coverage-inventory.md) | Independently checked discovery baseline: 708 manual leaves, 102 device profiles and separate schema/service/controller inventories; no complete profiles |
| [Arrangement editing](arrangement-editing.md) | Retained manual/schema/demo/native-presence evidence for a partial editing contract; exact-build behavior unknown |
| [Recording and comping](recording-comping.md) | Retained documentary and storage evidence for recording/Capture/take/comp contracts; runtime outcomes unknown |
| [Live 12 manual captures](sources/live-12-reference-manual.md) | Official source register with exact capture identities and current-manual/build applicability limits |
| [Bundled-device host protocol](device-host-protocol.md) | Static processing/reset/parameter/event findings and app-observable gaps; research models excluded from application compatibility coverage |
| [Device chains and racks](device-racks.md) | Manual/schema/demo evidence for zones, macros, drum routing and common device actions; corrected partial draft reviewed |
| [MIDI editing and tools](midi-editing-tools.md) | Editor and 17 per-tool documentary contracts; exact-build gaps and three source conflicts retained |
| [Projects and media workflows](project-media-workflows.md) | Set/project/reference/collection/Pack and generic Undo History documentary evidence; exact-build behavior unknown |
| [Browser workflows](browser-workflows.md) | Retained current-manual evidence for a partial search/navigation/preview draft; exact-build applicability unknown |
| [Audio and video export](audio-video-export.md) | Shared retained Managing Files source, conditional dropout restart and export fixture review; exact-build behavior unknown |
| [Media import/cache/analysis/interchange](media-file-workflows.md) | Reuses exact Managing Files source for selected format/cache/ASD/MIDI/Live Clip contracts; corrected partial scope independently reviewed |
| [Native MIDI effects](native-midi-effects.md) | Eight documentary device contracts, schema/preset corroboration and explicit algorithm/lifecycle gaps |
| [Utility, Tuner and Spectrum](device-audio-utilities.md) | Reviewed manual/schema/preset evidence for three partial control contracts; no audio or detector execution |
| [MPE, tuning and grooves](mpe-tuning-grooves.md) | Source packet for three workflow contracts; corrected partial scope independently reviewed |
| [Sample instruments](sample-instruments.md) | Active Simpler/Sampler/Impulse evidence packet; exact-build, DSP and lifecycle unknowns retained |
| [Filter and EQ devices](filter-eq-devices.md) | Auto Filter/Channel EQ/EQ Eight/EQ Three partial contracts; corrected modulation/Scale/LED fixtures independently reviewed; two source ambiguities and Legacy remain open |
| [Keyboard navigation and accessibility](keyboard-navigation.md) | Exact official chapters, focus/Tab/settings/envelope interactions and unclosed shortcut catalog; corrected partial review approved |
| [Dynamics devices](dynamics-devices.md) | Five reviewed partial device owners with123 exact manual blocks, schema/preset corroboration and ungraded DSP/lifecycle outcomes |
| [Audio-to-MIDI conversion](audio-to-midi.md) | Exact current-manual slicing/recognition workflow evidence, narrow128-slice limit and existing native-selection boundary; corrected partial review approved |
| [Delay and reverb devices](delay-reverb-devices.md) | Seven-device source/control/state and null DSP/timing/lifecycle packet; corrected partial scope independently reviewed |
| [Distortion devices](distortion-devices.md) | Nine-device manual/schema/preset contract evidence; corrected partial scope independently reviewed; modern/Legacy Erosion not merged |
| [Modulation, pitch, spectral and looping devices](modulation-pitch-loop-devices.md) | Ten-device partial contract/source/case review approved; corrected spectral artifact associations retained; all exact-build outcomes U |
| [Synthesis and drum instruments](synthesis-instruments.md) | Five-device partial source/control/voice/MPE/tuning packet independently reviewed; Operator restart and Meld type/sign contexts unresolved |
| [External hardware devices](external-hardware-devices.md) | Two routing/control profiles with24 requirements/56 cases; shared source identities and null signal/latency/lifecycle outcomes; corrected partial scope reviewed |
| [Legacy native devices](legacy-native-devices.md) | Reviewed eight-profile D11 precursor/package packet,77 requirements/178 cases; all target outcomes U; no modern-law substitution |
| [Clip View workflows](clip-view-workflows.md) | Reviewed partial chapter/audio property evidence;180 sourceblocks and54 requirements/62 cases; Humanize/Add Interval source contexts unresolved |
| [Session View workflows](session-view-workflows.md) | Partial77-block source/grid/scene packet;29 requirements/40 cases; shared metadata ownership correction independently verified |
| [Max for Live hosting/templates](max-for-live-hosting.md) |42-block source/host/template packet;38 requirements/64 cases, corrected partial scope reviewed; full API and20device behavior separate |
| [Max for Live devices](max-for-live-devices.md) | Twenty-profile manual/file packet;218 current HTML plus15 dated PDF blocks,20 unparsed AMXD identities;135 requirements/315 cases partially reviewed |
| [Video workflows](video-workflows.md) |39-block chapter/source/role packet;18 requirements/28 cases reviewed partial scope; exact-build/codec/frame/audio/lifecycle gaps retained |
| [Routing, monitoring and latency](routing-monitoring-latency.md) |226 retained source blocks and40 requirements/69 cases; existing recording/mix/external-device ownership retained; partial scope independently reviewed |
| [Bundled-device workflows](bundled-device-workflows.md) | 55 requirements/118 cases; seven broader profiles independently reviewed as partial; numeric/DSP owners unchanged; all target outcomes U |
| [Session launch and Follow workflows](session-launch-workflows.md) | 43 requirements/68 cases; partial scope independently reviewed; timing/chance/action-context questions retained; all target outcomes U |
| [Bounce and Freeze workflows](bounce-freeze-workflows.md) | 41 requirements/77 cases; partial scope independently reviewed; current/D11 predecessor contexts separated; all target outcomes U |
| [Synchronization workflows](synchronization-workflows.md) | 26 requirements/36 cases; partial scope independently reviewed; Link/Link Audio/Follower/Clock/MTC roles; all target outcomes U |
| [Settings, Learn and Info View](settings-learning-workflows.md) |70-block First Steps source packet;21 requirements/30 cases independently reviewed as partial; clip color preference context retained |
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
| [Update helper workflows](update-helper-workflows.md) | 30 requirements/37 all-null proposals from bounded retained Swapper/launcher evidence;21S/1inference/8U, frozen for independent review; no helper executed |
| [Full Live coverage design](full-live-specification-design.md) | Governing inventory, evidence/case and closure rules for the full-product specification target |
| [Full Live specification plan](full-live-specification-plan.md) | Current analyst selector F-01–F-10, parallel packet assignments and review gates |
| [Session handoff](session-handoff.md) | Continuation note: reviewed playback/device releases, reconciled specs, user decisions, Collision recovery and remaining queue (2026-10-19) |
| [Ableton investigation plan](ableton-plan.md) | Static-first loop, optional probes, subsystem order and review of the harness-first proposal |

Use [source storage](../../raw/README.md), the [source template](../../templates/source.md),
and the [ingest workflow](../workflows.md#ingest-a-source). Record unresolved
claims in [open questions](../questions.md). Research findings feed
[draft specifications](../specs/index.md); only reviewed releases cross the
[handoff boundary](../../handoff/index.md).
