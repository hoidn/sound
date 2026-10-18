---
id: NAV-HANDOFF
type: index
status: active
updated: 2026-10-17
access: handoff
---

# Reviewed implementation handoffs

Two finite MIDI configuration releases exist. midi-config-v2 is a strict
superset of v1: CC and pad enablement, channels, map-mode labels, button kinds,
bank span and device, mixer, transport and pad targets. Approval is limited to
explicitly partial requirement clauses; runtime compatibility is unverified. A
fresh restricted implementation workspace remains required.

| Release | Target scope | Spec revisions | Review record | Manifest SHA-256 | Supersedes |
| --- | --- | --- | --- | --- | --- |
| [midi-config-v1](midi-config-v1/README.md) | Master/cue/crossfader configuration interpretation | SPEC-MIDI-USER-MAPPING r1, partial REQ-002/003/010/013 only | [Approved review](midi-config-v1/REVIEW.md) | `9e3ab46efba170f61bcd7b9fce5d579c263aefd90097dc06695339594308b6ee` | None |
| [midi-config-v2](midi-config-v2/README.md) | Configuration interpretation: CC and pad enablement, channels, device/mixer/transport/pad targets, map-mode labels, button kinds, bank span | SPEC-MIDI-USER-MAPPING r2, partial REQ-002/003/005–013 only; 001 and 004 unreleased | [Approved with narrowing](midi-config-v2/REVIEW.md) | `889b52fa3b7f19c1bd085f26db39e0f62f00cbf7dc85be050e32207f012eb4d7` | midi-config-v1 (strict superset) |

## Release contract

Each future release is a self-contained immutable directory with:

- A role-scoped `AGENTS.md` for the implementation environment.
- Behavioral specs with stable requirement IDs and explicit acceptance cases.
- Reviewed fixtures and approved public sources with versions and provenance.
- A manifest listing scope, exclusions, unknowns, file digests, and reviewer disposition.
- A change list and explicit supersession relationship when replacing a release.

The catalog can advance; existing release payloads cannot. Implementation docs
pin a release and spec revision. Analysts keep the source/evidence traceability
mapping separately; handoffs must not link to private analysis to be intelligible.

Use the [manifest template](../templates/handoff-manifest.md) and
[release workflow](../wiki/workflows.md#release-a-handoff). The isolated export
must include self-contained copies of necessary neutral instructions with links
rewritten for that package. This repository is the staging workspace, not the
isolated export itself.

Implementation begins at its [own index](../wiki/implementation/index.md).
