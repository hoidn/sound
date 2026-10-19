---
id: SPEC-FEATURE-MAP
type: feature-map
status: draft
updated: 2026-10-18
access: analysis
---

# Whole application feature map

This is a proposed coverage inventory from the workflow discussion, not a
claim that all behaviors have been discovered. Expand it against versioned
manuals, package inventory, API surfaces, and observed user workflows.

| Feature ID | Area | Initial questions | Spec state |
| --- | --- | --- | --- |
| FEAT-TRANSPORT | Transport and timing | Tempo, meter, looping, launch boundaries, clock changes | Draft [SPEC-TRANSPORT-STATE](transport-state.md) r4 (document fields); [transport-state-v3](../../handoff/transport-state-v3/README.md) released, partial, superseding transport-state-v2; evidence in [transport-state static](../research/transport-state-static.md) and [native](../research/transport-state-native.md); Start, Stop and loop request paths and a static transition table in [transport transitions](../research/transport-transitions-native.md); launch grid and boundary rule in [clip launch](../research/clip-launch.md#from-a-quantization-value-to-a-launch-boundary) |
| FEAT-SESSION | Session View | Clips, scenes, follow actions, recording, Arrangement override | Draft [SPEC-CLIP-LAUNCH](clip-launch.md) r4 (stored launch fields, values, load corrections, migration, grid and launch boundary; boundary offset, stopped launch, launch modes, Legato, velocity and follow-action timing open); evidence in [clip launch](../research/clip-launch.md); [clip-launch-v1](../../handoff/clip-launch-v1/README.md) released, partial (50 cases) |
| FEAT-ARRANGEMENT | Arrangement | Editing, comping, fades, clip boundaries, recording | Unspecified |
| FEAT-AUDIO | Audio engine | Mixing, routing, monitoring, latency, device changes | Draft [SPEC-MIXER-VALUES](mixer-values.md) r4 (mixer storage, fader curves, value text, crossfade assign; audio-path clauses static-derived and need measurement); evidence in [mixer values](../research/mixer-values.md); [mixer-values-v1](../../handoff/mixer-values-v1/README.md) released, partial (37 cases) |
| FEAT-MIDI | MIDI engine | Scheduling, note state, expression, recording, MPE; audio-to-MIDI conversion | Draft [SPEC-MIDI-NOTE-STORAGE](midi-note-storage.md) r3 (clip note storage only; evidence in [MIDI note storage](../research/midi-note-storage.md)); scheduling, note state and recording unspecified; audio-to-note library identified in [x86_64-only bundles](../research/x86-only-bundles.md); [midi-note-storage-v2](../../handoff/midi-note-storage-v2/README.md) released, partial (72 cases) |
| FEAT-AUTOMATION | Automation and modulation | Curves, overrides, interpolation, recording, undo | Draft [SPEC-AUTOMATION-ENVELOPES](automation-envelopes.md) r4 (storage, targets, load checks, curves, Float, Bool and Enum evaluation; interpolation domain, steps, override, recording and undo open); evidence in [automation envelopes](../research/automation-envelopes.md); [automation-envelopes-v1](../../handoff/automation-envelopes-v1/README.md) released, partial (21 cases) |
| FEAT-DEVICES | Devices and racks | Chains, macros, state, mapping, signal behavior | Draft [SPEC-BUNDLED-DEVICE-PARAMETERS](bundled-device-parameters.md) r2 (stored parameters of the seven bundled devices; new-instance defaults and out-of-range handling open); evidence in [device bundles](../research/device-bundles-static.md), [device parameter mapping](../research/device-parameter-mapping-native.md) and [device tables](../research/device-tables-native.md); [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md) released, partial (82 cases) |
| FEAT-HOSTING | Plug-in hosting | Discovery, lifecycle, state, latency, failures | Draft [SPEC-PLUGIN-DISCOVERY](plugin-discovery.md) r2 (VST3 and VST2 discovery only); evidence in [plug-in scanner](../research/plugin-scanner-static.md) and [helper launch](../research/helper-launch-live-side.md#plug-in-scanner); [plugin-discovery-v1](../../handoff/plugin-discovery-v1/README.md) released, partial (35 cases) |
| FEAT-WARP | Warping | Markers, modes, tempo/pitch behavior, boundaries | Draft [SPEC-WARP-MARKERS](warp-markers.md) r4 (marker storage, shadow marker, empty-list refusal, enumerations, setting domains, scripting sample/beat conversion and edit limits); playback mapping and stretching audio unspecified; evidence in [warp markers](../research/warp-markers.md); [warp-markers-v1](../../handoff/warp-markers-v1/README.md) released, partial (38 cases) |
| FEAT-PERSISTENCE | Files and recovery | Sets, presets, media references, migration, recovery | Draft [SPEC-ALS-CONTAINER](als-container.md) r2, envelope only; [als-container-v1](../../handoff/als-container-v1/README.md) released, partial ([static](../research/document-container-static.md), [native](../research/document-container-native.md)); schema still declares `ReWireDeviceMidiTargetId`; XMP tag sidecars and `filerefmap.db` in [browser index](../research/browser-index-static.md) |
| FEAT-UI | Desktop interface | Browser, selection, shortcuts, drag/drop, focus, undo | Draft [SPEC-BROWSER-INDEX](browser-index.md) r2 (browser content kinds, tag sidecars, previews, rebuild); static evidence in [browser index](../research/browser-index-static.md); [browser-index-v1](../../handoff/browser-index-v1/README.md) released, partial (26 cases) |
| FEAT-MIDI-USER-MAPPING | User-defined controller mapping (ecosystem subset) | Configuration, channels, banks, buttons and native/host gaps | [Revision 5 draft](midi-user-mapping.md) with S4 closure applied; [finite configuration release](../../handoff/midi-config-v1/README.md), partial clauses only; [midi-config-v2](../../handoff/midi-config-v2/README.md) released, partial REQ-002/003/005–013; [midi-config-v4](../../handoff/midi-config-v4/README.md) released, partial (161 cases) |
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
