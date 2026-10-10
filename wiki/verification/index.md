---
id: NAV-VERIFICATION
type: index
status: active
updated: 2026-10-09
access: analysis
---

# Reference comparison and verification

This domain owns original-versus-candidate experiments. There are no retained
compatibility runs yet. Candidate-only tests belong in implementation docs.

| Page | Purpose |
| --- | --- |
| [Coverage matrix](coverage.md) | Whole-app verification state and next evidence required |

Use the [verification template](../../templates/verification.md). Record the
actual scenario, exact original/candidate identities, environment, comparison
criteria, result artifacts, and limitations. Preserve failed, partial, and
inconclusive runs. Claim success only for the required cases actually exercised.

Reference-side raw captures remain analyst-only. Return reviewed behavioral
discrepancies or approved comparison summaries through the [handoff process](../workflows.md#release-a-handoff).

## Completion rule

A requirement can be verified only when it has a reviewed spec revision,
matching original cases, a named candidate implementation, all required fixture
classes, and a passing comparison whose evidence type supports the claim.
Open contradictions, missing cases, or unavailable runtime evidence prevent
closure. A feature family requires all of its declared required obligations.
