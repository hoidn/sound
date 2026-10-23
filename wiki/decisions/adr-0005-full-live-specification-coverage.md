---
id: ADR-0005
type: decision
status: adopted
updated: 2026-10-21
access: neutral
---

# ADR 0005: Full Live behavioral specification coverage

## Decision and authority

On 2026-10-19 the user directed: “proceed. update design / plans / roadmap as
needed. don't stop until the entirely of Live has spec coverage”. The analyst
specification target now includes the entire observable surface of the pinned
Ableton Live 12 Suite 12.4.3 product, including the areas outside T1.

This supersedes only ADR 0004's consequence that families outside T1 remain at
their existing drafts. [T1](adr-0004-target-scope-t1.md) remains the first bounded
implementation/comparison milestone; its criteria and exclusions are unchanged.
A whole-product specification is a separate deliverable from implementing or
verifying a whole-product replacement.

## Scope and completion rule

Maintain a versioned inventory reconciled from the pinned package, shipped
schemas/resources, official documentation and already retained investigations.
Every product area has one canonical contract owner. Include editing, recording,
Arrangement and Session workflows, devices and racks, hosting, files and media,
UI and accessibility, routing and timing, preferences, delivery, control surfaces
and external integrations. Third-party products need host-facing contracts;
their arbitrary internal behavior is not Live's contract.

Do not equate a catalog row, source heading, spec filename, extracted function,
parameter list or passing finite fixture with a fully specified feature. Each
behavior needs supported inputs, preconditions, observable transitions/outputs,
boundaries, errors, timing/state and acceptance criteria. Unknown outcomes stay
unknown and keep the affected completion gate open. Record version and platform
uncertainty explicitly; a current Live 12 manual is not automatically evidence
of the exact 12.4.3 build.

The [coverage design](../research/full-live-specification-design.md) defines the
inventory and evidence gates. The [execution plan](../research/full-live-specification-plan.md)
owns ordering, assignments and actual status. Completion requires an independently
reviewed reconciliation of every inventoried surface, not a target page count.

## Preserved boundaries

- This checkout remains analyst-only. No candidate implementation or clean
  implementation delegation is authorized here.
- T1.6 stays pending by the user's earlier decision. Full specification work
  does not require provisioning it.
- Amp and Cabinet host emulation/fake host identity stay blocked by the user's
  earlier decision. Static or documented investigation can describe supported
  behavior; unavailable audio/protocol evidence remains a gap.
- ADR 0002 and ADR 0003 remain in force. No whole-application execution,
  unapproved tooling installation or external publication is authorized.
- Published handoffs and raw captures remain immutable. Wider drafts do not
  retroactively expand released scope or establish compatibility.

## Consequences

Replace the T1-only work selector with the whole-product analyst plan while
retaining the earlier execution history. Parallel independent analyst packets
may proceed from retained evidence. Shared indexes, coverage, questions, logs
and release publication have one coordinator. An unresolved prerequisite in one
area does not stop independent specification work elsewhere, and is never
silently removed from the whole-product denominator.


## Completion rule confirmation — 2026-10-20

The user explicitly confirmed: “Keep coverage open until evidence supports it
(current rule).” This resolves the disposition question raised in plan revision4.
Required behavior without supporting evidence remains unknown and keeps its
affected family and whole-product completion gates open. A documentary inventory
that lists the unknowns does not satisfy that gate; route absence is not an
exemption or evidence of correctness.

This confirms the completion rule above. It changes no outcome denominator,
evidence strength, independent-review requirement, existing harness authorization,
ADR0003 restriction or Amp/Cabinet block. It authorizes no new host/emulator,
original application run or implementation work. Continue independent permitted
research and batches; release only their reviewed partial scope. The plan owns
current selections, while this decision owns the durable closure rule.

Note, 2026-10-21: [ADR 0006](adr-0006-reference-observation-reopened.md)
reopens whole-application observation as evidence route O once a host is
recorded. The sentence above refusing a new host is superseded as to the host;
the completion rule confirmed here is unchanged.
