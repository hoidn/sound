---
id: PROJECT-OVERVIEW
type: overview
status: active
updated: 2026-10-12
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
| Reference target | Ableton Live 12 Suite 12.4.3; identity and static evidence retained locally (see research index) |
| Research | Package evidence, browsable native pseudocode, method/structure guides and reviewed recovery tooling; target reopening is capacity-blocked (see research index) |
| Behavioral specifications | Broader MIDI mapping draft; first finite configuration handoff released |
| Implementation | No application code; architecture choices remain proposals |
| Verification | No retained original-versus-candidate compatibility results |
| Clean implementation workspace | Not provisioned; this checkout contains analyst material |
| Published handoffs | [midi-config-v1](../handoff/midi-config-v1/README.md): four partial clauses, 54 unexecuted cases |

## Current phase

The user authorized the analyst-side [roadmap](research/native-decompilation-roadmap.md):
systematic main Live decompilation, browsable function exports, an accessible
method guide and evolving program-structure atlas, native behavior studies and
a first reviewed handoff. The [execution plan](research/native-phase-execution.md)
records actual progress and resource limits. Current implementation and
verification states remain unchanged.

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
