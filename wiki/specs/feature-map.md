---
id: SPEC-FEATURE-MAP
type: feature-map
status: draft
updated: 2026-10-09
access: analysis
---

# Whole application feature map

This is a proposed coverage inventory from the workflow discussion, not a
claim that all behaviors have been discovered. Expand it against versioned
manuals, package inventory, API surfaces, and observed user workflows.

| Feature ID | Area | Initial questions | Spec state |
| --- | --- | --- | --- |
| FEAT-TRANSPORT | Transport and timing | Tempo, meter, looping, launch boundaries, clock changes | Unspecified |
| FEAT-SESSION | Session View | Clips, scenes, follow actions, recording, Arrangement override | Unspecified |
| FEAT-ARRANGEMENT | Arrangement | Editing, comping, fades, clip boundaries, recording | Unspecified |
| FEAT-AUDIO | Audio engine | Mixing, routing, monitoring, latency, device changes | Unspecified |
| FEAT-MIDI | MIDI engine | Scheduling, note state, expression, recording, MPE | Unspecified |
| FEAT-AUTOMATION | Automation and modulation | Curves, overrides, interpolation, recording, undo | Unspecified |
| FEAT-DEVICES | Devices and racks | Chains, macros, state, mapping, signal behavior | Unspecified |
| FEAT-HOSTING | Plug-in hosting | Discovery, lifecycle, state, latency, failures | Unspecified |
| FEAT-WARP | Warping | Markers, modes, tempo/pitch behavior, boundaries | Unspecified |
| FEAT-PERSISTENCE | Files and recovery | Sets, presets, media references, migration, recovery | Unspecified |
| FEAT-UI | Desktop interface | Browser, selection, shortcuts, drag/drop, focus, undo | Unspecified |
| FEAT-MIDI-USER-MAPPING | User-defined controller mapping (ecosystem subset) | Configuration, channels, banks, buttons and native/host gaps | [Revision 1 draft](midi-user-mapping.md); [finite configuration release](../../handoff/midi-config-v1/README.md), partial clauses only |
| FEAT-ECOSYSTEM | Integrations | Link, controllers, Push, Max for Live, Packs | Unspecified |
| FEAT-DELIVERY | Delivery and export | Preferences, install, audio export, teardown, crash handling | Unspecified |

Split these families into bounded feature pages as evidence arrives. Require
separate statuses for documentation, implementation, and verification; do not
mark a family complete when only one scenario passes.

## Compatibility dimensions

- Behavior: state transitions, outputs, errors, and user task outcomes.
- Audio: deterministic equality where applicable; otherwise declared signal metrics.
- Files: semantic interchange and preservation, with byte equality only when required.
- UI: interactions/accessibility and separately declared visual expectations.
- Real-time operation: scheduling, latency, jitter, load, and failure recovery.

Numeric tolerances, supported versions/platforms, and required scenarios are
unresolved in [Q-001](../questions.md#q-001-compatibility-targets).
Track current evidence in the [coverage matrix](../verification/coverage.md).
