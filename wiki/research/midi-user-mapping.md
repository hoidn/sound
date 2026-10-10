---
id: RESEARCH-MIDI-USER-MAPPING
type: research
status: current
updated: 2026-10-09
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# MIDI user mapping investigation

Question: which observable configuration and assignment rules can be derived
from the shipped user-controller documents and their bytecode paths before
investigating native MIDI arithmetic? The [source record](sources/midi-user-mapping-12.4.3.md)
pins nineteen retained files and the static decoder. The resulting behavioral
contract lives only in the [draft spec](../specs/midi-user-mapping.md); this page
owns the evidence interpretation and remaining investigation boundaries.

## Evidence and conclusions

The [parser findings](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/parser-findings.json)
(PARSE-01–10) and [mapping findings](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/bytecode-mapping-findings.json)
(BC-01–10) contain exact module, function, source-line and bytecode-offset
locators. All findings are static derivations conditional on the traced path.
They are not observed reference executions.

| Investigation | Result and consequence | Evidence |
| --- | --- | --- |
| Numeric parsing | Ordinary controls use disable/fallback rules; pad parsing has a separate direct-integer path and can raise rather than disable. Template comments alone cannot specify malformed input. | PARSE-01/02/08, BC-01 |
| Mode tokens | Unknown present tokens follow a different representation path from an absent mode. A safe Absolute fallback is not established. Native numeric transforms remain unknown. | PARSE-03/04/09 |
| Configuration syntax | Retained parser code establishes normalized option names, strict duplicate rejection and Boolean lexical rules; host error recovery is outside this trace. | PARSE-05/06/07 |
| Sparse controls and banks | Filtering and retained matrix ordering close the relevant width/order dependency. Counts and compacted order matter, not only numbered labels. | BC-02/03 and matrix supplemental capture |
| Bank navigation | Next-only and Next-plus-Previous follow different branches; extrapolating one navigation case to all configurations would be wrong. | BC-04 |
| Button input | Momentary/toggle and repeated-value behavior depends on control type; a universal rising-edge rule would be wrong. Native target-property side effects remain unresolved. | BC-05/06/07/09/10 |
| Held seeking | Static code nominates a task-based progression, but scheduler cadence and time-unit interpretation are insufficient for a real-time contract. | BC-08 |
| Internal profile naming | A source function transforms a name, but this does not establish discovery timing or the displayed surface list. | PARSE-10 |

The bank matrix dependency was initially a gap and was closed by an additional
bounded static capture. This demonstrates the intended investigation loop:
trace a dependency that changes the answer, without broad analysis of the main
native executable or launching Live.

## Contract and validation boundary

The [case matrix](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/acceptance-cases.json)
is a structured plan, not an executable harness. Expectations identify their
documentary/static provenance; unresolved cases cannot pass. Every case remains
unexecuted. No app implementation exists. A subsequent
[finite configuration handoff](../../handoff/midi-config-v1/README.md) releases
only four partial clauses with a separate 54-case fixture set; the broader
draft and its matrix remain unreleased.

Questions [Q-008–Q-010](../questions.md#q-008-midi-profile-parsing-and-host-errors)
retain host errors, numerical modes, timing/feedback and lifecycle gaps.
Continue with a targeted static dependency only when it blocks the chosen
contract. A runtime probe requires its own bounded question under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md).

Separate author, evidence review and quality review are used for this draft.
The [scope recheck](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/scope-recheck.json)
and [quality review](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/quality-review.json)
approved the bounded draft after two scope corrections. They assess draft
quality, not clean handoff suitability or empirical compatibility.
