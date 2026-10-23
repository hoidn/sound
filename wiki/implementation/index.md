---
id: NAV-IMPLEMENTATION
type: index
status: active
updated: 2026-10-20
access: implementation
---

# Implementation documentation

This is the implementation-only entry point. Read the [handoff catalog](../../handoff/index.md)
and pin a released specification before compatibility implementation. The
[first configuration release](../../handoff/midi-config-v1/README.md) is available
for its explicit partial scope. No application code has been written. The
restricted implementation workspace was provisioned on 2026-10-19: the sparse
git worktree `~/Documents/sound-impl` on branch `impl`, holding only this page's
permitted inputs. Start implementation only in a fresh session there.

## Start here: the T1 candidate

- Target: T1 as defined in [ADR 0004](../decisions/adr-0004-target-scope-t1.md):
  open and save T1 Live Sets, an offline render driven by a transport and launch
  script, the mixer, automation and the released devices. The acceptance
  dimensions and the settled-start render convention are in that ADR.
- Inputs: the current releases in the [handoff catalog](../../handoff/index.md)
  (19 as of 2026-10-20). Each carries `spec.md`, `cases.json` and `manifest.json`.
  Eleven release directories are provisional copies not yet committed on `main`
  (device-analog-v1, device-collision-v1, device-corpus-v1, device-corpus-v2, device-corpus-v3, device-corpus-v4, device-corpus-v5, device-electric-v1,
  device-electric-v2, device-tension-v1, playback-core-v1); their manifests carry
  the package hashes. Once `main` has committed them, drop the copies
  (`git clean -fd handoff && git checkout -- handoff/index.md`) before merging.
- Suggested order: a case runner over `cases.json`; the container and Live Set
  structure releases; transport, clip launch, notes, warp and playback core;
  mixer values and mix graph; then the device releases against their reference
  renders.
- Decide the stack in an implementation ADR (candidates in
  [architecture](architecture.md)). Put code under a new top-level `candidate/`
  directory on branch `impl`. Record progress in [coverage](coverage.md) and the
  [implementation log](log.md).
- Raise every behavioral gap as an `IQ-` entry in [questions](questions.md).
  Answers arrive as new releases on `main`; merge `main` into `impl` to receive
  them. Never read analyst material, including other branches' history.

| Page | Purpose |
| --- | --- |
| [Architecture candidates](architecture.md) | Proposed implementation structure and undecided technology choices |
| [Candidate coverage](coverage.md) | Requirement-to-code/test mapping for released handoffs |
| [Implementation questions](questions.md) | Requests for clarification through the handoff boundary |
| [Implementation log](log.md) | Append-only candidate-side work history |

Permitted governance: [project scope](../project.md), [schema](../schema.md),
[workflows](../workflows.md), and [root routing](../../AGENTS.md). These describe
process; they do not provide original behavioral authority. Do not follow
governance links into analyst-only source, spec, research, or verification pages.

Use the [implementation template](../../templates/implementation.md) and
[decision template](../../templates/decision.md). Add module docs when modules
exist, and a technical decision index when the first technical ADR is adopted.
