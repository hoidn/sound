---
id: PROJECT-OVERVIEW
type: overview
status: active
updated: 2026-10-18
access: neutral
---

# Project scope and status

The project is establishing an evidence-based process for an independent
desktop application covering Ableton Live workflows. The user requested a
persistent LLM-maintained wiki including specification and implementation
documentation. Whole-app coverage is the planning scope; completion of the
documentation structure is not completion of the application.

## Current state

| Area | State |
| --- | --- |
| Documentation routing and schema | Established in this workspace |
| Reference target | Ableton Live 12 Suite 12.4.3; identity pinned and arm64 slices re-derived on the current host; the earlier static evidence tree is absent here (see research index) |
| Analysis workstation | Linux host provisioned 2026-10-17 with Ghidra 12.1.4, JDK 21 and REA 6.5.0; Push2 smoke test reproduced prior counts; persistent Live project at `/var/tmp/sound-analysis`, analysis running (see [execution ledger](research/native-phase-execution.md#linux-workstation-provisioning--2026-10-17)) |
| Research | Package evidence, browsable native pseudocode, method/structure guides and reviewed recovery tooling; target reopening is capacity-blocked (see research index) |
| Behavioral specifications | Eleven draft specs, revised with release reviews and extracted execution; fourteen partial releases, eleven current (see [spec index](specs/index.md)) |
| Implementation | No application code; architecture choices remain proposals |
| Verification | No retained original-versus-candidate compatibility results |
| Clean implementation workspace | Not provisioned; this checkout contains analyst material |
| Published handoffs | [midi-config-v1](../handoff/midi-config-v1/README.md): four partial clauses, 54 unexecuted cases; [midi-config-v2](../handoff/midi-config-v2/README.md): partial REQ-002/003/005–013, 109 unexecuted cases, supersedes v1; [transport-state-v1](../handoff/transport-state-v1/README.md): transport values in Live Sets, 18 unexecuted cases; [als-container-v1](../handoff/als-container-v1/README.md): Live Set container and version envelope, 35 unexecuted cases; on 2026-10-18 [midi-config-v3](../handoff/midi-config-v3/README.md) (127 cases, supersedes v2) and eight first releases: clip-launch-v1 (50), midi-note-storage-v1 (67), mixer-values-v1 (37), automation-envelopes-v1 (21), bundled-device-parameters-v1 (82), browser-index-v1 (26), plugin-discovery-v1 (35), warp-markers-v1 (38); [transport-state-v2](../handoff/transport-state-v2/README.md) (33 cases, supersedes transport-state-v1); all cases unexecuted against Live ([catalog](../handoff/index.md)) |

## Current phase

The user authorized the analyst-side [roadmap](research/native-decompilation-roadmap.md):
systematic main Live decompilation, browsable function exports, an accessible
method guide and evolving program-structure atlas, native behavior studies and
a first reviewed handoff. The [execution plan](research/native-phase-execution.md)
records actual progress and resource limits. Current implementation and
verification states remain unchanged. A [revision 2 proposal](research/native-decompilation-roadmap.md#revision-2-proposal--2026-10-17)
for restarting on the Linux workstation was adopted on 2026-10-17 and is executing.
On 2026-10-18 [ADR 0004](decisions/adr-0004-target-scope-t1.md) set the first completion
target, T1, and [roadmap revision 3](research/native-decompilation-roadmap.md#revision-3--t1-completion-plan-2026-10-18)
plans its gaps.

## Milestones

1. Record the reference build, artifact digests, environment, and package inventory.
2. Establish the whole-app feature matrix and explicit compatibility dimensions.
3. Derive bounded behavioral specifications from static evidence; resolve only
   material gaps with targeted reference probes under [ADR 0002](decisions/adr-0002-static-first-analysis.md).
   Since 2026-10-18 no whole-application reference run is possible; gaps are
   closed by extracted execution of original functions or stay unknown
   ([ADR 0003](decisions/adr-0003-no-reference-execution.md)).
4. Release the first reviewed behavioral specification and fixture package.
5. Provision an isolated implementation workspace and build a candidate.
6. Compare reference and candidate; revise specifications and implementation
   through reviewed handoffs until the declared cases meet their criteria.
   Under ADR 0003 the comparison is against released expectations, which are
   static-derived or from extracted execution, never a run of Live itself.

The proposed first integrated scenario is two audio tracks, quantized clip
launching, recording into Arrangement, editing, save/reopen, and audio export.
It is a proposed milestone, not a requirement already validated against Live.

## Decisions still to make

- Compatibility targets and tolerances for behavior, audio, files, UI, and timing.
- Implementation platform and dependency/license choices.
- Priority and scope of devices, Warp, Max for Live, Push, and project interchange.
- Durable artifact storage and enforced analyst/implementer access boundaries.

Use [the routing table](../AGENTS.md) to choose the next task. Implementation-only
contexts proceed through the [handoff index](../handoff/index.md) and
[implementation index](implementation/index.md).
