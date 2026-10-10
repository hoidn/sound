---
id: ADR-0001
type: decision
status: adopted
updated: 2026-10-09
access: neutral
---

# Persistent wiki and documentation routing

## Context

The user requested project documentation practices, including specification and
implementation documentation, based on the supplied LLM Wiki pattern. The
project also needs to preserve a boundary between original-side analysis and
independent implementation.

## Decision

Use local Markdown with immutable raw sources, mutable canonical wiki pages,
and a schema in `AGENTS.md` and `wiki/schema.md`. Add immutable reviewed handoff
releases for specifications and fixtures. Maintain separate analyst and
implementation indexes/logs. Tie requirements to evidence, candidate ownership,
and scoped verification results.

Decision owner: project documentation maintainer (assistant), exercising the
user's authorization to establish these practices on 2026-10-09. This records
the implementation choice; it does not claim a separate human review occurred.

## Alternatives

| Option | Tradeoff |
| --- | --- |
| One flat docs directory | Easy startup, but poor role routing and unclear source/spec/design boundaries |
| Hosted wiki or retrieval service | More setup and another source of state; not required for the current scale |
| Local role-routed Markdown wiki | Chosen: portable, searchable, versionable, with explicit ownership |

## Consequences

Agents maintain documentation in the same change as evidence, specs, or code.
Each claim has a canonical home, and links replace duplicate summaries where
precision matters. Indexes describe current content; logs retain chronology.

The folder layout does not enforce isolation. Before clean implementation,
create a fresh context with access only to an exported reviewed handoff and
candidate materials. The first release must include its own scoped instructions
and resolve links without analyst files. A role switch in an exposed context
does not restore independence.

No application stack is selected by this decision. No behavioral equivalence,
legal conclusion, automatic background maintenance, or external publication is
implied.

## Validation

Check metadata, links, catalog coverage, source integrity, and routing consistency.
Read semantic claims to ensure drafts and plans are not labeled as completed work.
Record actual checks in the relevant append-only log.

Related: [schema](../schema.md), [workflows](../workflows.md), [routing](../../AGENTS.md).
