---
id: PROJECT-OVERVIEW
type: overview
status: active
updated: 2026-10-17
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
| Behavioral specifications | MIDI mapping draft revision 2; midi-config-v1 and its superset midi-config-v2 released; transport-state and document-container static halves filed |
| Implementation | No application code; architecture choices remain proposals |
| Verification | No retained original-versus-candidate compatibility results |
| Clean implementation workspace | Not provisioned; this checkout contains analyst material |
| Published handoffs | [midi-config-v1](../handoff/midi-config-v1/README.md): four partial clauses, 54 unexecuted cases; [midi-config-v2](../handoff/midi-config-v2/README.md): partial REQ-002/003/005–013, 109 unexecuted cases, supersedes v1 |

## Current phase

The user authorized the analyst-side [roadmap](research/native-decompilation-roadmap.md):
systematic main Live decompilation, browsable function exports, an accessible
method guide and evolving program-structure atlas, native behavior studies and
a first reviewed handoff. The [execution plan](research/native-phase-execution.md)
records actual progress and resource limits. Current implementation and
verification states remain unchanged. A [revision 2 proposal](research/native-decompilation-roadmap.md#revision-2-proposal--2026-10-17)
for restarting on the Linux workstation was adopted on 2026-10-17 and is executing.

## Milestones

1. Record the reference build, artifact digests, environment, and package inventory.
2. Establish the whole-app feature matrix and explicit compatibility dimensions.
3. Derive bounded behavioral specifications from static evidence; resolve only
   material gaps with targeted reference probes under [ADR 0002](decisions/adr-0002-static-first-analysis.md).
4. Release the first reviewed behavioral specification and fixture package.
5. Provision an isolated implementation workspace and build a candidate.
6. Compare reference and candidate; revise specifications and implementation
   through reviewed handoffs until the declared cases meet their criteria.

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
