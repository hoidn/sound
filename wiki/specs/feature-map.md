---
id: SPEC-FEATURE-MAP
type: feature-map
status: draft
updated: 2026-10-17
access: analysis
---

# Whole application feature map

This is a proposed coverage inventory from the workflow discussion, not a
claim that all behaviors have been discovered. Expand it against versioned
manuals, package inventory, API surfaces, and observed user workflows.

| Feature ID | Area | Initial questions | Spec state |
| --- | --- | --- | --- |
| FEAT-TRANSPORT | Transport and timing | Tempo, meter, looping, launch boundaries, clock changes | Draft [SPEC-TRANSPORT-STATE](transport-state.md) r2 (document fields); [transport-state-v1](../../handoff/transport-state-v1/README.md) released, partial; evidence in [transport-state static](../research/transport-state-static.md) and [native](../research/transport-state-native.md); Start, Stop and loop request paths and a static transition table in [transport transitions](../research/transport-transitions-native.md); launch grid and boundary rule in [clip launch](../research/clip-launch.md#from-a-quantization-value-to-a-launch-boundary) |
| FEAT-SESSION | Session View | Clips, scenes, follow actions, recording, Arrangement override | Candidates CL-01 to CL-23 in [clip launch](../research/clip-launch.md#candidate-requirements-for-spec-clip-launch); no draft spec |
| FEAT-ARRANGEMENT | Arrangement | Editing, comping, fades, clip boundaries, recording | Unspecified |
| FEAT-AUDIO | Audio engine | Mixing, routing, monitoring, latency, device changes | Unspecified; mixer storage, fader curves, display text, −∞ floor, pan law and crossfade assign in [mixer values](../research/mixer-values.md) (candidates MX-01 to MX-15) |
| FEAT-MIDI | MIDI engine | Scheduling, note state, expression, recording, MPE; audio-to-MIDI conversion | Unspecified; clip note storage (KeyTracks, MidiNoteEvent, NoteIds, per-note expression) in [MIDI note storage](../research/midi-note-storage.md), candidates MN-01 to MN-24; audio-to-note library identified in [x86_64-only bundles](../research/x86-only-bundles.md) |
| FEAT-AUTOMATION | Automation and modulation | Curves, overrides, interpolation, recording, undo | Unspecified |
| FEAT-DEVICES | Devices and racks | Chains, macros, state, mapping, signal behavior | Unspecified; static interface and parameter inventory for the seven bundled devices in [device bundles](../research/device-bundles-static.md) |
| FEAT-HOSTING | Plug-in hosting | Discovery, lifecycle, state, latency, failures | Draft [SPEC-PLUGIN-DISCOVERY](plugin-discovery.md) r1 (VST3 and VST2 discovery only); evidence in [plug-in scanner](../research/plugin-scanner-static.md) and [helper launch](../research/helper-launch-live-side.md#plug-in-scanner) |
| FEAT-WARP | Warping | Markers, modes, tempo/pitch behavior, boundaries | Unspecified |
| FEAT-PERSISTENCE | Files and recovery | Sets, presets, media references, migration, recovery | Draft [SPEC-ALS-CONTAINER](als-container.md) r1, envelope only ([static](../research/document-container-static.md), [native](../research/document-container-native.md)); schema still declares `ReWireDeviceMidiTargetId`; XMP tag sidecars and `filerefmap.db` in [browser index](../research/browser-index-static.md) |
| FEAT-UI | Desktop interface | Browser, selection, shortcuts, drag/drop, focus, undo | Draft [SPEC-BROWSER-INDEX](browser-index.md) r1 (browser content kinds, tag sidecars, previews, rebuild); static evidence in [browser index](../research/browser-index-static.md) |
| FEAT-MIDI-USER-MAPPING | User-defined controller mapping (ecosystem subset) | Configuration, channels, banks, buttons and native/host gaps | [Revision 2 draft](midi-user-mapping.md) with S4 closure applied; [finite configuration release](../../handoff/midi-config-v1/README.md), partial clauses only; [midi-config-v2](../../handoff/midi-config-v2/README.md) released, partial REQ-002/003/005–013 |
| FEAT-ECOSYSTEM | Integrations | Link, controllers, Push, Max for Live, Packs, ReWire | Unspecified; ReWire mixer and device modes appear x86_64-only ([x86_64-only bundles](../research/x86-only-bundles.md)); Push 3 helper interfaces in [Push 3 helper](../research/push3-helper-static.md); add-on and extension helper in [web, add-ons, swapper](../research/web-addons-swapper-static.md); Packs remain in Live |
| FEAT-DELIVERY | Delivery and export | Preferences, install, audio export, teardown, crash handling | Unspecified; self-update (`.asu`, xdelta, swap with rollback) static evidence in [web, add-ons, swapper](../research/web-addons-swapper-static.md) |

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
