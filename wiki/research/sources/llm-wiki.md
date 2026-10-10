---
id: SRC-LLM-WIKI
type: source
status: current
updated: 2026-10-09
access: analysis
---

# LLM Wiki source

The user supplied an idea file titled LLM Wiki as the basis for project
documentation on 2026-10-09. It proposes persistent synthesis maintained by an
LLM across immutable sources, a mutable wiki, and a governing schema.

## Provenance

- Source: the user's documentation request in the current project conversation.
- Original author/publication date: not supplied.
- Capture: [selected verbatim excerpts](../../../raw/public/2026-10-09-llm-wiki-excerpts.md).
- Capture scope: excerpts only; the complete source was supplied in the conversation.
- Capture integrity: see [checksum record](../../../raw/public/SHA256SUMS).
- Access: source available to analysts; approved project policy is neutral governance.

## Synthesis

The key operating rule is to keep synthesized understanding current rather than
rediscovering it from source material on each query. Topic pages accumulate
cross-references, contradictions, and updated conclusions. A content index and
an append-only chronological log serve different navigation needs.

The user's full supplied text also describes ingest, query, and lint operations,
filing durable query answers, and optional search/Obsidian tooling. Those points
are sourced to the full conversation text; the local excerpt capture is not a
complete archive of those sections.

## Project adaptation

[The schema](../../schema.md) adopts the three layers, canonical pages, relative
links, indexes, logs, and ongoing reconciliation. [ADR 0001](../../decisions/adr-0001-documentation.md)
adds separate behavioral specs, implementation docs, verification records, and
immutable handoffs for this project's research boundary. Those additions are
project decisions, not claims made by the source.

No external search tool, hosted wiki, or scheduled maintenance job is required.
