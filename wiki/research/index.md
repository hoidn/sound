---
id: NAV-RESEARCH
type: index
status: active
updated: 2026-10-17
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
| [Package structure](ableton-package-structure.md) | Observed native/resource boundaries and coverage limits |
| [x86_64-only bundles](x86-only-bundles.md) | Live Engine is a ReWire device build of the engine; ReWire 1.8.7 install chain is x86_64-only; MultiF0 audio-to-note API; engine as symbol donor for S3 |
| [Live x86_64 paths](x86-live-paths.md) | N8: ReWire install chain gated off by constant-false checks in Live and the Engine; MultiF0 built-in by default; Convert Drums uses a separate drum task; MultiF0 record fields as Live reads them; x86_64 transport matches arm64 including both Stop transfers; PRB-N8-01 to 05 |
| [Plug-in scanner (static)](plugin-scanner-static.md) | H1: scanner options, VST3 and VST2 enumeration, scan-state database, crash and limit derivation, messages to Live, 14 candidate requirements, 8 probes |
| [Browser index (static)](browser-index-static.md) | H2: index helper launch and messages, files database schema and versioning, scan pipeline, XMP tag sidecars, previews, `filerefmap.db`; 12 candidate requirements, 9 probes |
| [Device bundles (static)](device-bundles-static.md) | H4: seven device bundles share one 7-function C interface with three implementations; Live owns parameter names and stored domains; 502-parameter inventory over 1,064 shipped occurrences; 5 probes |
| [Device parameter mapping (native)](device-parameter-mapping-native.md) | N5: how Live loads the seven bundles, uses GetPlugInfoU and sets parameters; complete index and conversion tables for Amp, Cabinet, Electric and Corpus (82 rows); 4 probes |
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
| [Ableton investigation plan](ableton-plan.md) | Static-first loop, optional probes, subsystem order and review of the harness-first proposal |

Use [source storage](../../raw/README.md), the [source template](../../templates/source.md),
and the [ingest workflow](../workflows.md#ingest-a-source). Record unresolved
claims in [open questions](../questions.md). Research findings feed
[draft specifications](../specs/index.md); only reviewed releases cross the
[handoff boundary](../../handoff/index.md).
