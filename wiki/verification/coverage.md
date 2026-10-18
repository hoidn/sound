---
id: VAL-COVERAGE
type: coverage
status: planned
updated: 2026-10-17
access: analysis
---

# Whole application verification coverage

The [feature map](../specs/feature-map.md) defines the current planning scope.
A bounded ecosystem draft and a finite configuration release exist; all
families remain unimplemented and unverified. This
matrix is an analyst view; the implementer has a separate mapping of released
requirements to candidate code and tests.

| Feature ID | Spec/handoff | Implementation | Verification | Next evidence |
| --- | --- | --- | --- | --- |
| FEAT-TRANSPORT | Draft [SPEC-TRANSPORT-STATE](../specs/transport-state.md) r1; no handoff | Not started | Unknown; 23 draft cases not run | PRB-N1-01 to 08; transition logic |
| FEAT-SESSION | Candidates CL-01 to CL-23 ([clip launch](../research/clip-launch.md)); no draft; no handoff | Not started | Unknown | PRB-S5-01 to 11; launch-mode branches |
| FEAT-ARRANGEMENT | None | Not started | Unknown | Editing/recording state and persistence paths |
| FEAT-AUDIO | None | Not started | Unknown | Routing and DSP paths; flag latency for later measurement |
| FEAT-MIDI | None | Not started | Unknown | Event formats, scheduling and note-state logic |
| FEAT-AUTOMATION | None | Not started | Unknown | Curve/override schemas, interpolation and undo paths |
| FEAT-DEVICES | None | Not started | Unknown | Preset/state schemas and bounded DSP derivations |
| FEAT-HOSTING | Draft [SPEC-PLUGIN-DISCOVERY](../specs/plugin-discovery.md) r1 (discovery only); no handoff | Not started | Unknown; 42 draft cases not run | PRB-H1-01 to 08, PRB-N4-01, 02, 05; lifecycle, state, latency |
| FEAT-WARP | None | Not started | Unknown | Mode/settings and algorithm analysis; flag numerical comparisons |
| FEAT-PERSISTENCE | Draft [SPEC-ALS-CONTAINER](../specs/als-container.md) r1 (envelope only); no handoff | Not started | Unknown; 27 draft cases not run | PRB-N2-01 to 07; Live Set save call site; set content, migration, recovery |
| FEAT-UI | None | Not started | Unknown | UI resources, bindings and command/focus dispatch |
| FEAT-MIDI-USER-MAPPING | [Revision 2 draft](../specs/midi-user-mapping.md); [finite configuration release](../../handoff/midi-config-v1/README.md); [midi-config-v2](../../handoff/midi-config-v2/README.md) released | Not started | Unknown; 109 v2 release cases (54 restated from v1), 46 broader draft groups and 16 probe records not run | Independently observe released routes; PRB-S4-01–16 on the macOS host |
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
