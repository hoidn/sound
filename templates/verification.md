---
id: VAL-REPLACE
type: verification
status: planned
updated: YYYY-MM-DD
access: analysis
---

# Scenario comparison

## Claim and identity

- Requirement IDs and exact spec/handoff revision:
- Original build and artifact SHA-256:
- Candidate revision and artifact SHA-256:
- Tool/provider versions and environment:
- Audio/MIDI settings, clock basis, and adapter versions where applicable:

## Reproduction

Inputs and fixture hashes, initial state, ordered actions, actual commands,
reset/cleanup procedure, repetitions, and raw-result retention locations.
State whether the original scenario is repeatable and what variability exists.

## Comparison rules

Behavior/audio/files/UI/timing dimensions, expected results, tolerances,
alignment rules, and nondeterminism policy selected before comparison.
Report timing offsets separately; alignment must not hide a latency defect.

## Results

| Case/requirement | Original observation | Candidate observation | Result | Evidence locator |
| --- | --- | --- | --- | --- |

## Interpretation and limits

First divergence, inferred explanation, unresolved alternatives, incomplete
coverage, and stale dependencies. Passing cases do not establish global parity.

## Follow-up

Affected coverage/spec/question pages and the reviewed behavioral discrepancy
to return through handoff. Keep raw binary evidence analyst-only.
