---
id: NAV-SPECS
type: index
status: active
updated: 2026-10-17
access: analysis
---

# Behavioral specification index

Specifications define what must be observable, independent of the original's
internal implementation. This directory contains analyst-side drafts. The
[first configuration release](../../handoff/midi-config-v1/README.md) and its superset
[midi-config-v2](../../handoff/midi-config-v2/README.md) approve
explicitly partial clauses only; REQ-001, REQ-004 and the runtime clauses remain unreleased.

| Page                                                           | Purpose                                                                     |
| -------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [MIDI configuration handoff plan](midi-config-handoff-plan.md) | Finite static-supported release candidate and review gates                  |
| [MIDI configuration v2 handoff plan](midi-config-v2-handoff-plan.md) | Released midi-config-v2 (109 cases): scope, narrowing, traceability |
| [Feature map](feature-map.md)                                  | Whole-app planning inventory and stable feature IDs                         |
| [MIDI user mapping](midi-user-mapping.md)                      | Revision 2 draft: documented, static, static-conditional and unknown clauses; static expectations, unexecuted cases |

Author bounded contracts with the [spec template](../../templates/spec.md).
Each future spec gets requirement IDs, a feature-map link, original-side evidence,
and acceptance cases. Add its catalog row here in the same change.

Approved snapshots are listed in the [handoff index](../../handoff/index.md).
Candidate code and design are maintained in [implementation](../implementation/index.md);
original-versus-candidate results are maintained in [verification](../verification/index.md).
