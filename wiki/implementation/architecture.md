---
id: IMPL-ARCHITECTURE
type: implementation
status: proposed
updated: 2026-10-09
access: implementation
---

# Architecture candidates

No technology stack or application architecture has been selected. These are
candidate project design choices, not recovered Ableton internals. The
[finite configuration contract](../../handoff/midi-config-v1/spec.md) does not
select an application architecture or establish reference compatibility.

## Proposed responsibilities

- Project state and versioned persistence.
- Editing commands and undo/redo.
- Musical timeline, transport, and event scheduling.
- Real-time audio/MIDI processing and offline rendering.
- Devices, plug-in hosting, and integration adapters.
- Desktop presentation and interaction state.
- Test adapters that expose controlled inputs and observable outputs.

Interface details, thread ownership, supported formats, and error contracts
will be designed against released requirements. Code paths and runtime results
are not available yet.

## Technology candidates

| Candidate | Evaluation question | State |
| --- | --- | --- |
| C++20 and JUCE | Does it support the required audio and desktop interfaces with acceptable maintenance cost? | Proposed |
| Tracktion Engine | Can its scheduling/editing model express the released interaction contracts? | Proposed |
| Ableton Link SDK | Does its public interface satisfy the chosen synchronization requirements? | Proposed |
| Rubber Band | Does its time/pitch behavior meet the selected signal criteria? | Proposed |
| Python comparison harness | Can it reproduce fixtures and report state/audio/timing differences reliably? | Proposed |

Before selection, review current primary documentation and license/distribution
fit. Public references used by isolated implementers must be explicitly listed
in the handoff's approved-source inventory. Do not assume a substitute library
matches reference behavior simply because its feature names are similar.

Record actual choices as implementation ADRs, link their tradeoffs here, and
update [candidate coverage](coverage.md) as implementation proceeds.
