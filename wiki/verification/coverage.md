---
id: VAL-COVERAGE
type: coverage
status: planned
updated: 2026-10-18
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
| FEAT-TRANSPORT | Draft [SPEC-TRANSPORT-STATE](../specs/transport-state.md) r4; [transport-state-v3](../../handoff/transport-state-v3/README.md) released (33 cases, supersedes v1) | Not started | Unknown; 33 release cases and 36 draft cases not run (26 of them backed by extracted execution) | PRB-N1-01 to 08; transition logic |
| FEAT-SESSION | Draft [SPEC-CLIP-LAUNCH](../specs/clip-launch.md) r4; [clip-launch-v1](../../handoff/clip-launch-v1/README.md) released (50 cases) | Not started | Unknown; 50 release cases and 61 draft cases not run | PRB-S5-01 to 11; set-level variant for missing or out-of-range global quantization; launch-mode branches |
| FEAT-ARRANGEMENT | None | Not started | Unknown | Editing/recording state and persistence paths |
| FEAT-AUDIO | Draft [SPEC-MIXER-VALUES](../specs/mixer-values.md) r4; [mixer-values-v2](../../handoff/mixer-values-v2/README.md) released (80 cases); [mix-graph-v1](../../handoff/mix-graph-v1/README.md) released (28 cases) | Not started | Unknown; 37 release cases and 48 draft cases not run (11 need audio measurement) | Q-019 (stored gain to fader position; send path); PRB-S9-01 to 08; routing and DSP paths; flag latency for later measurement |
| FEAT-MIDI | Draft [SPEC-MIDI-NOTE-STORAGE](../specs/midi-note-storage.md) r3 (clip note storage only); [midi-note-storage-v2](../../handoff/midi-note-storage-v2/README.md) released (72 cases) | Not started | Unknown; 67 release cases and 75 draft cases not run | PRB-S7-01 to 10 with the PRB-S7-07 boundary variants; scheduling and note-state logic |
| FEAT-AUTOMATION | Draft [SPEC-AUTOMATION-ENVELOPES](../specs/automation-envelopes.md) r4; [automation-envelopes-v1](../../handoff/automation-envelopes-v1/README.md) released (21 cases) | Not started | Unknown; 21 release cases and 26 draft cases not run | PRB-S6-01 to 07 (Pan variant for 04); proposed PRB-S6-08 to 11; per-parameter value conversion |
| FEAT-DEVICES | Draft [SPEC-BUNDLED-DEVICE-PARAMETERS](../specs/bundled-device-parameters.md) r2; [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md) released (82 cases) | Not started | Unknown; 82 release cases and 37 draft cases not run | P4-H4-01 to 05, P4-N5-01 to 04, P4-N6-01; racks, chains and other devices; DSP derivations |
| FEAT-HOSTING | Draft [SPEC-PLUGIN-DISCOVERY](../specs/plugin-discovery.md) r2 (discovery only); [plugin-discovery-v1](../../handoff/plugin-discovery-v1/README.md) released (35 cases) | Not started | Unknown; 35 release cases and 62 draft cases not run | PRB-H1-01 to 08, PRB-N4-01, 02, 05; lifecycle, state, latency |
| FEAT-WARP | Draft [SPEC-WARP-MARKERS](../specs/warp-markers.md) r4; [warp-markers-v1](../../handoff/warp-markers-v1/README.md) released (38 cases) | Not started | Unknown; 38 release cases and 32 draft cases not run | PRB-S8-01 to 11; assumptions A1 to A3 (Q-021); per-mode audio measurements |
| FEAT-PERSISTENCE | Draft [SPEC-ALS-CONTAINER](../specs/als-container.md) r2 (envelope only); [als-container-v1](../../handoff/als-container-v1/README.md) released (35 cases); [live-set-structure-v1](../../handoff/live-set-structure-v1/README.md) released (34 cases) | Not started | Unknown; 35 release cases and 27 draft cases not run | PRB-N2-01 to 07; Live Set save call site; set content, migration, recovery |
| FEAT-UI | Draft [SPEC-BROWSER-INDEX](../specs/browser-index.md) r2 (browser index and tag sidecars); [browser-index-v1](../../handoff/browser-index-v1/README.md) released (26 cases) | Not started | Unknown; 26 release cases and 66 draft cases not run | PRB-BI-01 to 05 (proposed), PRB-H2-03 to 06 and 09; UI bindings and command/focus dispatch |
| FEAT-MIDI-USER-MAPPING | [Revision 5 draft](../specs/midi-user-mapping.md); [finite configuration release](../../handoff/midi-config-v1/README.md); [midi-config-v2](../../handoff/midi-config-v2/README.md) released; [midi-config-v4](../../handoff/midi-config-v4/README.md) released, supersedes v3 | Not started | Unknown; 161 v4 release cases (127 carried from v3, 34 from extracted execution), 46 broader draft groups and 16 probe records not run | Independently observe released routes; PRB-S4-01–16 on the macOS host |
| FEAT-ECOSYSTEM | None | Not started | Unknown | Shipped integration contracts and protocol handlers |
| FEAT-DELIVERY | None | Not started | Unknown | Package/configuration and export/teardown paths |

As specs are released, add per-requirement reports with exact versions and
results. Summaries must not conceal unknown subcases. Do not turn a deferred
requirement into a pass or silently delete it from coverage.

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
