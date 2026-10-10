---
id: RESEARCH-QUESTIONS
type: questions
status: active
updated: 2026-10-09
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
  Ghidra accepted the Live slice; only Push2 received deep analysis in this pass.
- Retention limitation: installed resources remain mutable external originals;
  local ignored evidence is not an off-machine backup. Q-003 remains open.

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

## Q-006 Native analysis and resource decoding

- State: open; owner: analyst.
- Affects: FEAT-TRANSPORT, FEAT-PERSISTENCE, FEAT-ECOSYSTEM and FEAT-DEVICES.
- Evidence: [decompilation preparation](research/ableton-decompilation-preparation.md)
  and [structure findings](research/ableton-package-structure.md).
- Gap: core Live auto-analysis, remaining Python modules, proprietary ALP/AGR
  formats, schema migration semantics and resource-to-runtime bindings remain unknown.
- Progress: [MIDI mapping bytecode](research/midi-user-mapping.md) decoded and scoped paths traced; this does not cover all shipped Python.
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

## Q-009 MIDI numerical modes, timing and feedback

- State: open; owner: analyst/spec author.
- Affects: SPEC-MIDI-USER-MAPPING, REQ-MIDI-USER-004/005/007–012.
- Evidence: [mapping research](research/midi-user-mapping.md), PARSE-09, BC-02–09.
- Gap: native transforms, 14-bit pairing, pickup, device parameter ordering,
  feedback bytes, seek/nudge timing and remaining bank/lock boundaries.
- Next action: select a single mode or boundary and trace its native dependency;
  reserve actual timing/audio assertions for measured comparisons.

## Q-010 MIDI discovery, lifecycle and interaction

- State: open; owner: analyst/spec author.
- Affects: SPEC-MIDI-USER-MAPPING, REQ-MIDI-USER-001/003/004/006/008/012/013.
- Evidence: [mapping research](research/midi-user-mapping.md), PARSE-10 and draft
  lifecycle cases; documented placement is not an observed discovery run.
- Gap: reload, disconnect/reconnect, held-control cleanup, routing conflicts,
  bank/lock persistence, automation and undo membership.
- Next action: trace discovery/teardown and persistence entry points for one
  selected lifecycle case before deciding whether runtime capture is necessary.

## Q-011 Main Live export capacity and recovery

- State: open; owner: native-analysis coordinator.
- Affects: [next-phase roadmap](research/native-decompilation-roadmap.md), main
  Live corpus and downstream native behavior investigations.
- Evidence: [preparation](research/ableton-decompilation-preparation.md) establishes
  that Ghidra accepted the main slice, while deep analysis was tested only on
  Push2; the retained [capability note](../analysis/ableton-live-12.4.3/phase-2-plan/tool-capabilities.json)
  identifies advertised tool arguments, not exercised main-image capacity.
- Progress: the [execution ledger](research/native-phase-execution.md) records
  the full-analysis disk-floor stop, successful selected-entry exports and
  the changed resource policy for a capacity-enabled retry. Readable main
  pseudocode exists; full inventory and systematic export do not.
- Gap: full-analysis completion cost, discovered-function count, default-profile
  export throughput and cold-provider recovery remain unmeasured.
- Next action: retry with the newly freed capacity, two-worker default pools and
  aggregate process monitoring; retain the result before scheduling exports.
  Selected-entry manifests must remain separate from the default corpus.
