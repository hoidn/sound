---
id: DOC-SCHEMA
type: policy
status: active
updated: 2026-10-09
access: neutral
---

# Documentation schema

Compile durable understanding into canonical Markdown pages. Read the relevant
index first, update existing pages when new information arrives, and keep
sources and conclusions connected. The [routing rules](../AGENTS.md) determine
which indexes and sources a role may read.

## Layers and authority

| Layer | Authority and allowed edits |
| --- | --- |
| Raw sources | Immutable evidence of what was supplied or captured; not automatic proof of every claim inside a source |
| Research | Mutable synthesis grounded in exact sources; distinguish observation from inference |
| Draft specifications | Proposed behavioral contracts; not authorized implementation inputs until released |
| Released handoffs | Immutable, reviewed implementation contracts with a version and manifest |
| Implementation | Our current design and code behavior, linked to the exact handoff revision |
| Verification | What a particular experiment established for a particular build and scenario |
| Decisions | Explicit chosen policy or design, rationale, and consequences; not evidence of original behavior |

The supplied wiki pattern motivates this schema. The additional handoff boundary
and implementation/verification distinctions are project design choices recorded
in [ADR 0001](decisions/adr-0001-documentation.md).

## Paths and canonical ownership

- `wiki/research/sources/<slug>.md`: one summary per source or source family with
  individually identified revisions. Findings spanning sources live in
  `wiki/research/<topic>.md` when they warrant a separate page.
- `wiki/specs/<feature>.md`: canonical draft behavior for a bounded feature.
- `handoff/<release>/`: immutable reviewed snapshots, approved fixtures and sources,
  release manifest, checksums, and a role-scoped `AGENTS.md`.
- `wiki/implementation/<module>.md`: implementation design and current code map.
  Put technical ADRs in `wiki/implementation/decisions/` and link their index.
- `wiki/verification/<scenario-or-report>.md`: original-versus-candidate evidence.
  Candidate-only test results belong under implementation and may be shared.
- `wiki/questions.md`: canonical analysis gaps and contradictions. Clean-room
  implementer questions live in `wiki/implementation/questions.md`.
- Each domain owns an `index.md`. The top index links domains instead of copying
  every nested entry. Every non-index page needs an inbound catalog link.

Create pages when there is a durable question or conclusion; do not create empty
pages for every noun. Move or rename pages only with all inbound links updated.

## Metadata and identifiers

All `wiki/**/*.md` and handoff catalog pages start with YAML frontmatter:

```yaml
id: SPEC-SESSION-LAUNCH
type: spec
status: draft
updated: 2026-10-09
access: analysis
```

Required fields: `id`, `type`, `status`, `updated` (ISO date), and `access`.
`access` is `neutral`, `analysis`, `implementation`, or `handoff`. These labels
describe intended readers and must be enforced by workspace permissions for
isolated implementation. They do not make shared storage safe.

Use stable IDs, not filenames or addresses, to identify requirements. Common
prefixes: `SRC-`, `SPEC-`, `REQ-`, `FEAT-`, `IMPL-`, `ADR-`, `VAL-`, `Q-`.
Do not reuse retired IDs. REA evidence retains its original `ev_...` identity.
Add `target`, `revision`, `specs`, or `supersedes` fields when applicable.
Templates are examples exempt from live-page metadata checks.

Use standard relative Markdown links, including `.md`; stable heading anchors
may narrow citations. Use local links for archived sources and direct URLs for
external sources. Links must resolve in the relevant reader's workspace. A
handoff must not depend on `../../raw` or analyst-only links.

## Claim and evidence conventions

| Label | Meaning |
| --- | --- |
| Observed | Directly present in a named source/capture; state what was observed |
| Inferred | Interpretation supported by evidence but not directly established |
| Proposed | Candidate requirement or design pending decision or review |
| Decided | Project policy/design chosen by a named decision record |
| Unknown | Evidence is absent, incomplete, contradictory, or inaccessible |

Place citations beside substantive claims. A citation needs a source/evidence
ID, exact locator (section, range, function, timestamp, case), target version,
and limitations. For a web source record both its publication/version if known
and capture date. For experiment results record the executed command/scenario,
artifact hashes, environment, raw-result locator, and actual outcome.

Never convert an old chat claim into retained observed evidence. Mark it
`reported in conversation; not independently recaptured` until a durable
capture supports it. A static call edge does not establish runtime execution;
a passing fixture does not prove global equivalence.

## Page lifecycles

- Policy/index: `active` or `superseded`.
- Source/research: `draft`, `current`, `stale`, or `superseded`.
- Spec: `draft` → `in-review` → `released`; later edits create a new revision.
  The mutable draft may advance while an older handoff remains pinned.
- Implementation: `proposed`, `in-progress`, `implemented`, `verified`, `stale`,
  or `superseded`. `verified` always names its tested scope and exact build.
- Verification: `planned`, `pass`, `fail`, `partial`, `unknown`, or `stale`.
- Decision: `proposed`, `adopted`, `rejected`, or `superseded`.

Status is a summary, not a substitute for evidence. Separate documentation,
implementation, and verification status in coverage tables. Mark downstream
results stale when a changed spec/code/fixture invalidates their applicability;
retain the previous result for its original revision.

## Specifications and implementation documents

A spec contains observable inputs, preconditions, outputs, state transitions,
errors, timing, persistence, interaction with other requirements, and measurable
acceptance cases. Enumerate positive, negative, boundary, malformed, cancellation,
and teardown cases as applicable; explicitly justify omissions. Keep analysis
citations in an analyst-only appendix that is removed/reviewed for handoff.

An implementation page names its released spec/requirement IDs, module paths,
public interfaces, state ownership, concurrency, error handling, dependencies,
design decisions, and test/report links. Code changes and documentation changes
travel together. Do not copy recovered internal structures into implementation
docs. Candidate technology choices remain proposed until decided.

Use the [templates](../templates/index.md) as a starting point. State unknowns
instead of filling sections with invented behavior.

## Logging and history

Use `## [YYYY-MM-DD] operation | Subject` entries. Operations include `ingest`,
`query`, `spec`, `implementation`, `decision`, `release`, `lint`, and `maintenance`.
Append entries at the end; correct an old entry with a new entry that references
it. Include affected pages, what changed, and gaps. Log analyst/maintainer work
in `wiki/log.md`; implementation-only work in `wiki/implementation/log.md`.

Git stores mutable-page history. Source captures and release files are immutable
by policy; Git alone does not enforce that policy or role isolation. Do not
commit ignored binary evidence, credentials, or private captures accidentally.
