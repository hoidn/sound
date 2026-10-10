---
id: VAL-COVERAGE
type: coverage
status: planned
updated: 2026-10-09
access: analysis
---

# Whole application verification coverage

The [feature map](../specs/feature-map.md) defines the current planning scope.
One bounded ecosystem draft exists; all families remain unimplemented and unverified. This
matrix is an analyst view; the implementer has a separate mapping of released
requirements to candidate code and tests.

| Feature ID | Spec/handoff | Implementation | Verification | Next evidence |
| --- | --- | --- | --- | --- |
| FEAT-TRANSPORT | None | Not started | Unknown | Transport schema and native transition/boundary logic |
| FEAT-SESSION | None | Not started | Unknown | Launch/follow-action and override control flow |
| FEAT-ARRANGEMENT | None | Not started | Unknown | Editing/recording state and persistence paths |
| FEAT-AUDIO | None | Not started | Unknown | Routing and DSP paths; flag latency for later measurement |
| FEAT-MIDI | None | Not started | Unknown | Event formats, scheduling and note-state logic |
| FEAT-AUTOMATION | None | Not started | Unknown | Curve/override schemas, interpolation and undo paths |
| FEAT-DEVICES | None | Not started | Unknown | Preset/state schemas and bounded DSP derivations |
| FEAT-HOSTING | None | Not started | Unknown | Host interfaces, lifecycle and error paths |
| FEAT-WARP | None | Not started | Unknown | Mode/settings and algorithm analysis; flag numerical comparisons |
| FEAT-PERSISTENCE | None | Not started | Unknown | Packaged files, schema and loader/migration paths |
| FEAT-UI | None | Not started | Unknown | UI resources, bindings and command/focus dispatch |
| FEAT-MIDI-USER-MAPPING | [Draft revision 1](../specs/midi-user-mapping.md); no handoff | Not started | Unknown; 46 case groups not run | Review static expectations; resolve selected host/native gaps |
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
authorized work: reviewed analyst tooling, a disk-limited full-analysis attempt,
and actual selected main Live pseudocode exports with explicit failed entries.
Full-inventory throughput/recovery remains unknown (Q-011); these artifacts
establish no original-versus-candidate compatibility. All comparison statuses
above remain unchanged.

## Artifact navigation

The [artifact catalog](../research/artifacts/index.md) exposes retained binary,
pseudocode and disassembly coverage. Readable extracts and the offline browser
change discoverability only; every compatibility status remains unknown.

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
