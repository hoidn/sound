---
id: NAV-HANDOFF
type: index
status: active
updated: 2026-10-09
access: handoff
---

# Reviewed implementation handoffs

No handoff has been released. There are no approved behavioral requirements or
fixtures for compatibility implementation yet.

| Release | Target scope | Spec revisions | Review record | Manifest SHA-256 | Supersedes |
| --- | --- | --- | --- | --- | --- |

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
