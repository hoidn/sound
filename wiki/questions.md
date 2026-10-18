---
id: RESEARCH-QUESTIONS
type: questions
status: active
updated: 2026-10-17
access: analysis
---

# Open research questions

Keep one record per durable gap or contradiction. Each record needs affected
IDs, evidence for each competing claim where applicable, state, responsible
role, next action, and eventual resolution link. These are planning gaps;
no experimental contradiction has been established yet.

## Q-001 Compatibility targets

- State: open; owner: project maintainer.
- Affects: all features in the [feature map](specs/feature-map.md).
- Gap: supported platform/version and behavior/audio/file/UI/timing acceptance
  criteria have not been selected.
- Next action: define dimension-specific targets in the first spec review;
  choose numeric tolerances before accepting comparisons.

## Q-002 Durable reference identity

- State: resolved for this installed build; owner: analyst.
- Affects: [investigation plan](research/ableton-plan.md), all future evidence.
- Resolution: [SRC-ABLETON-12-4-3](research/sources/ableton-live-12.4.3.md)
  retains exact build, original/slice digests, extraction provenance and environment.
  Ghidra accepted the Live slice. Subsequent selected main-Live code exports
  are recorded in the [execution ledger](research/native-phase-execution.md);
  systematic export coverage and cold recovery remain open in Q-011.
- Retention limitation: installed resources remain mutable external originals;
  evidence tracked in local Git since 2026-10-17 is not an off-machine backup
  until pushed, and the `origin` remote is a public GitHub repository, so pushing
  would publish decompiled material. Q-003 remains open.

## Q-003 Isolation and evidence retention

- State: open; owner: project maintainer.
- Affects: [handoff workflow](workflows.md#release-a-handoff).
- Gap: no isolated implementation environment or durable large-evidence store
  is provisioned. Ignored directories and agent roles are not access controls.
- Next action: prepare a restricted implementation workspace and retention
  destination before releasing work to a clean implementer.

## Q-004 Implementation foundation

- State: open; owner: implementation architect after first handoff.
- Affects: [architecture candidates](implementation/architecture.md).
- Gap: the proposed stack has not been evaluated against released requirements.
- Next action: evaluate a small integrated workflow and record a technical ADR.

## Q-005 Whole app scope expansion

- State: open; owner: analyst/spec author.
- Affects: FEAT-DEVICES, FEAT-WARP, FEAT-ECOSYSTEM, FEAT-PERSISTENCE.
- Gap: supported device catalog, interoperability breadth, Max/Push behavior,
  and full native-format expectations are not bounded.
- Next action: expand the feature families into explicit required/optional/deferred
  contracts while keeping every deferred obligation visible.
- Evidence 2026-10-17: Push 3 support needs a separate helper process with a USB
  display protocol, the Push sysex protocol and a document-sync API with 369 message
  names ([Push 3 helper](research/push3-helper-static.md)). Decide whether Push
  support is required, optional or deferred before drafting a Push spec.
- Progress 2026-10-17: [device bundles](research/device-bundles-static.md) bounds
  the seven natively bundled devices. The 63 other `.adv` root elements (3 are Max
  for Live wrappers) have no bundle under `Devices/Mac`; where they are implemented
  is not established.

## Q-006 Native analysis and resource decoding

- State: open; owner: analyst.
- Affects: FEAT-TRANSPORT, FEAT-PERSISTENCE, FEAT-ECOSYSTEM and FEAT-DEVICES.
- Evidence: [decompilation preparation](research/ableton-decompilation-preparation.md)
  and [structure findings](research/ableton-package-structure.md).
- Gap: core Live auto-analysis, remaining Python modules, proprietary ALP/AGR
  formats, schema migration semantics and resource-to-runtime bindings remain unknown.
- Progress: [MIDI mapping bytecode](research/midi-user-mapping.md) decoded and scoped paths traced; this does not cover all shipped Python.
- Progress 2026-10-17: the bundle side of the device boundary is traced in [device bundles](research/device-bundles-static.md); the Live side (bundle loading, `GetPlugInfoU` use, index mapping, value conversion) is six open queries for the main Live project.
- Progress 2026-10-17: [document container static](research/document-container-static.md) identified `.agr` encodings and the `.alp` header/trailer layout; `.alp` encoding and runtime use of `Schema/` remain unknown.
- Next action: choose a bounded feature question, validate the matching decoder or
  trace its prepared native symbol; derive the contract and escalate only material
  gaps under [ADR 0002](decisions/adr-0002-static-first-analysis.md).

## Q-007 Reference behavior and timing

- State: open; owner: analyst/spec author.
- Affects: all runtime-dependent feature families.
- Evidence: shipped documentation and static fixtures in [SRC-ABLETON-12-4-3](research/sources/ableton-live-12.4.3.md).
- Gap: current static preparation has not established initialization, numeric
  enum semantics, scheduling, DSP, errors or user override precedence. Further
  static tracing may resolve logical behavior; measured runtime characteristics
  and empirical compatibility remain unverified.
- Next action: derive the bounded [spec preparation cases](research/ableton-decompilation-preparation.md#proposed-first-specification-work)
  from resources and code first. Identify which remaining claims actually need
  execution, then retain minimal probes with exact inputs, outputs and environment.

## Q-008 MIDI profile parsing and host errors

- State: open; owner: analyst/spec author.
- Affects: SPEC-MIDI-USER-MAPPING, REQ-MIDI-USER-002/003/005/013.
- Evidence: [mapping research](research/midi-user-mapping.md), PARSE-01–08.
- Gap: parser exceptions and an unknown mode's representation can be traced,
  but host diagnostics, profile recovery and invalid-mode outcome remain unknown.
- Next action: trace the relevant host/loader exception boundary; only if that
  cannot resolve a selected contract, design a minimal malformed-profile probe.
- Progress 2026-10-17: [spec revision 2](specs/midi-user-mapping.md) fixes statically
  which inputs raise out of profile construction (noninteger pad values,
  interpolation, duplicates, pre-section text, invalid Booleans; no handler) and
  how an unknown mode token is passed on. Host outcomes remain open as PRB-S4-03/04
  in the [S4 probe batch](research/midi-closure-r2.md#phase-4-probe-batch); the
  [midi-config-v2 candidate](specs/midi-config-v2-handoff-plan.md) excludes them.

## Q-009 MIDI numerical modes, timing and feedback

- State: open; owner: analyst/spec author.
- Affects: SPEC-MIDI-USER-MAPPING, REQ-MIDI-USER-004/005/007–012.
- Evidence: [mapping research](research/midi-user-mapping.md), PARSE-09, BC-02–09.
- Gap: native transforms, 14-bit pairing, pickup, device parameter ordering,
  feedback bytes, seek/nudge timing and remaining bank/lock boundaries.
- Next action: select a single mode or boundary and trace its native dependency;
  reserve actual timing/audio assertions for measured comparisons.
- Progress 2026-10-17: revision 2 adds static map-mode scope, the 14-bit label
  threshold and, as open S-cond clauses, crossfader takeover off, the absent
  mute-feedback default and feedback eligibility. Transforms, feedback bytes and
  timing remain PRB-S4-05/06/07/13; bank contents need `_Generic/Devices` traced
  before PRB-S4-09.

## Q-010 MIDI discovery, lifecycle and interaction

- State: open; owner: analyst/spec author.
- Affects: SPEC-MIDI-USER-MAPPING, REQ-MIDI-USER-001/003/004/006/008/012/013.
- Evidence: [mapping research](research/midi-user-mapping.md), PARSE-10 and draft
  lifecycle cases; documented placement is not an observed discovery run.
- Gap: reload, disconnect/reconnect, held-control cleanup, routing conflicts,
  bank/lock persistence, automation and undo membership.
- Next action: trace discovery/teardown and persistence entry points for one
  selected lifecycle case before deciding whether runtime capture is necessary.
- Progress 2026-10-17: discovery, reload, teardown, encoding and strip-to-track
  ordering remain PRB-S4-01/02/11/14/15/16; native strings are adjacency only.
  Revision 2 adds a routing refinement pending review: a `Send2Knob`*N* without
  a valid `Send1Knob`*N* reaches the strip's first send, contrary to a literal
  reading of the template (D5) and to S4 draft case S4-MIDI-030.

## Q-011 Main Live export capacity and recovery

- State: open; owner: native-analysis coordinator.
- Affects: [next-phase roadmap](research/native-decompilation-roadmap.md), main
  Live corpus and downstream native behavior investigations.
- Evidence: the [execution ledger](research/native-phase-execution.md) links the
  successful full-analysis completion, frozen inventory and bounded default-profile
  export checkpoints. The earlier disk stop and separate selected exports remain retained.
- Progress: full analysis completed after disk capacity was freed. Actual JVM
  diagnostics disproved the intended two-worker pool setting; aggregate monitoring
  remained active. The full inventory is available; reviewed grouped ingestion and
  attempted-first browsing have been exercised on a systematic export stage,
  with warnings preserved.
- Gap: full-corpus storage/throughput and cold-provider recovery remain unproven.
  Grouped checkpoints reduce whole-ledger rewriting, but do not remove its cost.
  The two bounded samples do not establish full-corpus fit; the capacity review
  stopped further bulk expansion. The current provider uses an ephemeral database.
- Next action: execute the [compact/archive and recovery plan](research/native-compact-storage.md),
  establish database recovery after the [published offline viewer](research/native-compact-storage.md#measured-reader--2026-10-11), before
  admitting a larger stage. The [real mirror](research/native-compact-storage.md#measured-mirror--2026-10-10)
  passed exact-member preservation and measured allocation; it adds no exports
  and does not establish full-corpus fit. The
  [persistent recovery design](research/native-analysis-recovery.md) is reviewed
  and its loader-matched correction passes scope/quality reviews and 198 tooling
  tests. Actual [target import/save](research/native-analysis-recovery.md#corrected-import-passes-reopen-capacity-stop--2026-10-12)
  passes, but first reopen is capacity-blocked. Retain both incomplete jobs;
  additional capacity precedes a fresh import and accepted cold-reopen proof,
  then measured bounded-analysis admission. No new pseudocode was added.
  Keep selected, linker and default-profile evidence separate.
  The [storage inventory](research/native-analysis-recovery.md#disk-cleanup-inventory--2026-10-12)
  identifies Downloads, the separate Trial app and package caches as reviewable
  capacity candidates. Trash is explicitly excluded; no cleanup was performed
  and suggested allocation is not guaranteed reclaimed space.
- Progress 2026-10-17: the work moved to a Linux workstation with the same
  Ghidra/JDK versions, REA 6.5.0 and far larger RAM/CPU; both arm64 slices were
  re-derived byte-identically. See the [provisioning record](research/native-phase-execution.md#linux-workstation-provisioning--2026-10-17).
- Gap 2026-10-17: the entire retained `analysis/` evidence tree (full inventory,
  2,028 exports, coverage ledger, incomplete persistent jobs) is absent here, so
  every linked capture is unavailable until restored from the macOS host. The
  persistent-project storage location is undecided; see the
  [Linux paths](research/native-analysis-recovery.md#linux-workstation-paths--2026-10-17).
- Proposal 2026-10-17: [roadmap revision 2](research/native-decompilation-roadmap.md#revision-2-proposal--2026-10-17)
  sequences the storage decision, a persistent project, one measured corpus
  batch and outside-in specification packets; adopted and executing 2026-10-17.

## Q-012 Transport-state load and save semantics

- State: open; owner: analyst (S1 native half).
- Affects: FEAT-TRANSPORT, FEAT-PERSISTENCE, the proposed SPEC-TRANSPORT-STATE.
- Evidence: [transport-state static](research/transport-state-static.md) and
  [document container static](research/document-container-static.md).
- Gap: defaults when a field is absent; handling of malformed tokens, duplicates
  and out-of-range values; clamping; precedence between `Manual` values, the
  one-event envelopes and scene values; the meaning of `Time=-63072000`; and the
  exact format 12.4.3 writes.
- Next action: once the saved project exists, trace the callers of
  `Member "{}" of Class {} is missing` and of the `Value … out of range for '`
  message; reserve the 12.4.3 write format for a Phase 4 save capture if static
  tracing cannot fix it.

## Q-013 x86_64-only ReWire and MultiF0 paths

- State: open; owner: analyst.
- Affects: FEAT-ECOSYSTEM, FEAT-MIDI audio-to-MIDI conversion, FEAT-PERSISTENCE.
- Evidence: [x86_64-only bundles](research/x86-only-bundles.md).
- Gap: when the ReWire install runs and what alias it creates; whether 12.4.3
  still offers ReWire to users; the default choice between built-in and dynamic
  MultiF0; whether Convert Drums uses MultiF0; the meaning of MultiF0 result
  fields; why the engine bundle's arm64 stub exists.
- Next action: once the Live x86_64 analysis finishes, query the callers of
  `InstallPropellerheadDlls: `, `Ableton Live Engine_64`,
  `Audio2Midi: Use builtin MultiF0 lib` and `MultiF0: No MultiF0 library found at `.

## Q-014 Browser index behavior

- State: open; owner: analyst.
- Affects: FEAT-UI (browser), FEAT-PERSISTENCE (tags and sample references).
- Evidence: [browser index](research/browser-index-static.md).
- Gap: Live's spawn site and arguments for the index helper; the real database
  prefix and directory; whether version 12300 is what is written; how the browser
  queries the database; who consults `filerefmap.db` and what its type values mean;
  how XMP sidecar names are derived; user-visible handling of missing, corrupt or
  unsupported files. Runtime facts are in probes PRB-H2-01 to 09.
- Next action: query the saved Live project for references to `live->index`,
  `ipc-channel`, `{}-files-{}.db` and `fileref-map-path`.

## Q-015 Helper launch and update handling in Live

- State: open; owner: analyst.
- Affects: FEAT-DELIVERY, FEAT-ECOSYSTEM.
- Evidence: [web, add-ons, swapper](research/web-addons-swapper-static.md),
  [Push 3 helper](research/push3-helper-static.md).
- Gap: how Live writes the web connector's configuration and the add-ons `--cid`;
  start conditions such as the auto-update setting and free space; Live's UI for
  each update event; use of the swapper's sentinel file; Pack and `.alp`
  installation; which side binds each Push nanomsg channel and what Live sends.
- Next action: trace `StartWebConnector`, `AddOns: start process` and the three
  Push channel names in the saved Live project.

## Q-016 Plug-in discovery Live-side contract

- State: open; owner: analyst.
- Affects: FEAT-HOSTING.
- Evidence: [plug-in scanner](research/plugin-scanner-static.md).
- Gap: which folders and domain IDs Live passes and how Rescan maps to `--reset`;
  where Audio Units are scanned; any timeout or kill policy; the meaning of the
  watchdog constants; the message framing; the database folder; the
  `dev_identifier` format; how duplicate class IDs appear in the browser. The crash
  and limit derivations (PD-10, PD-12) must not be released without probes
  PRB-H1-02 and PRB-H1-04.
- Next action: trace the Live callers of `Plugins: start scanner process`, `--cid`,
  `TPluginScannerMediator` and `APluginSettingsPreferencesModel` in the saved Live
  project.
