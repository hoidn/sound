---
id: SPEC-LIVE-API-CONTROL-TUNING
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3; current public API applicability U
---

# Public API control, routing, groove and tuning members

Partial F-05/F-08 contracts for six exact public reference entries,28 explicit
direct member declarations and this_device root context. The publisher index
explicitly names12.4.5; every exact12.4.3 applicability/outcome remains U.
D-current-public records source prose, not a tested API result or complete typed
payload schema. No original application/function, Max/JS/patch/API/script,
candidate, audio/MIDI/hardware or network operation was executed.

[Bridge](live-api-bridge-workflows.md) owns generic path/object/message roles.
[Remote](remote-control-workflows.md), [Push](push-controller-workflows.md),
[routing](routing-monitoring-latency.md), [racks](device-racks.md),
[grooves](groove-workflows.md), [tuning](tuning-systems.md),
[MIDI editing](midi-editing-tools.md) and [notes](midi-note-storage.md) retain
workflow/finite values/storage/signal laws. Device inheritance belongs to the
separate device/rack API owner; no inherited member is flattened or declared
covered here. Groove's primitive members remain under their published Children
category; that placement is not repaired into a different API model.

## Direct documentary contracts

### REQ-LAPI-CONTROL-001 — ControlSurface.pad_layout

**D-current-public/target-U.** The symbol is get/observe only. Printed Push2/3 layouts distinguish melodic64, melodic64+variations, sequencer, sequencer+32notes; drum variations,64pads,loop selector,16velocities,16pitches; and session. Instrument and Note/Session/Layout context conditions apply. This is not a settable layout selector or a Push1 protocol.

Published declaration: `pad_layout symbol`; [exact source section](https://docs.cycling74.com/apiref/lom/controlsurface/#pad_layout); `C74-LOM-CONTROLSURFACE` B0006, B0007, B0008, B0009, B0010, B0011.

### REQ-LAPI-CONTROL-002 — ControlSurface.get_control

**D-current-public/target-U.** Parameter name is printed without a declared type; the function returns the named control. Control object class, missing-name return and usable name grammar are not supplied.

Published declaration: `get_control`; [exact source section](https://docs.cycling74.com/apiref/lom/controlsurface/#get_control); `C74-LOM-CONTROLSURFACE` B0013, B0014.

### REQ-LAPI-CONTROL-003 — ControlSurface.get_control_names

**D-current-public/target-U.** Returns a list of all control names for that surface. Ordering, name encoding, list length and implicit function arguments are unspecified.

Published declaration: `get_control_names`; [exact source section](https://docs.cycling74.com/apiref/lom/controlsurface/#get_control_names); `C74-LOM-CONTROLSURFACE` B0015, B0016.

### REQ-LAPI-CONTROL-004 — ControlSurface.grab_control

**D-current-public/target-U.** Parameter control is printed without a type. Taking ownership releases standard functionality of that control for exclusive Max for Live use; the statement is scoped to that owned control, not a global hardware mute.

Published declaration: `grab_control`; [exact source section](https://docs.cycling74.com/apiref/lom/controlsurface/#grab_control); `C74-LOM-CONTROLSURFACE` B0017, B0018.

### REQ-LAPI-CONTROL-005 — ControlSurface.grab_midi

**D-current-public/target-U.** Forwarding concerns messages the surface script receives; the source limits engine channel-message delivery to those the script explicitly requests from Live. Pure realtime track messages can bypass that script; Push Note pads are the source example, contrasted with Session. This does not promise all raw MIDI from the hardware.

Published declaration: `grab_midi`; [exact source section](https://docs.cycling74.com/apiref/lom/controlsurface/#grab_midi); `C74-LOM-CONTROLSURFACE` B0019, B0020.

### REQ-LAPI-CONTROL-006 — ControlSurface.register_midi_control

**D-current-public/target-U.** MaxForLive surface only: name[symbol],status[int],number[int]. Printed status codes are144 note-on,176 CC,224 pitchbend. Returns the control LOM ID; associated forwarding is described after registration plus grab. A send_value call on the returned control is mentioned without defining that separate object member.

Published declaration: `register_midi_control`; [exact source section](https://docs.cycling74.com/apiref/lom/controlsurface/#register_midi_control); `C74-LOM-CONTROLSURFACE` B0021, B0022.

### REQ-LAPI-CONTROL-007 — ControlSurface.release_control

**D-current-public/target-U.** Parameter control is printed without a type. Release re-establishes the standard functionality for that control; return value and repeated/unowned-release semantics are unspecified.

Published declaration: `release_control`; [exact source section](https://docs.cycling74.com/apiref/lom/controlsurface/#release_control); `C74-LOM-CONTROLSURFACE` B0023, B0024.

### REQ-LAPI-CONTROL-008 — ControlSurface.release_midi

**D-current-public/target-U.** Stops forwarding messages received from that surface to Max for Live. Interaction with other receivers or automatic cleanup is unspecified.

Published declaration: `release_midi`; [exact source section](https://docs.cycling74.com/apiref/lom/controlsurface/#release_midi); `C74-LOM-CONTROLSURFACE` B0025, B0026.

### REQ-LAPI-CONTROL-009 — ControlSurface.send_midi

**D-current-public/target-U.** Parameter midi_message is a list of int, sent to the surface. Range, message framing, running status, supported message classes, acknowledgement and return type are unspecified.

Published declaration: `send_midi`; [exact source section](https://docs.cycling74.com/apiref/lom/controlsurface/#send_midi); `C74-LOM-CONTROLSURFACE` B0027, B0028.

### REQ-LAPI-CONTROL-010 — ControlSurface.send_receive_sysex

**D-current-public/target-U.** Printed parameters sysex_message[list of int],timeout[symbol,int] coexist with prose specifying timeout followed by a float and a default0.2 with no unit in this entry. It awaits a response: ungrabbed timed-out response is not forwarded; grabbed MIDI is always forwarded while timeout is still reported. Exact report grammar, units, response correlation and boundary timing remain U.

Published declaration: `send_receive_sysex`; [exact source section](https://docs.cycling74.com/apiref/lom/controlsurface/#send_receive_sysex); `C74-LOM-CONTROLSURFACE` B0029, B0030.

### REQ-LAPI-CONTROL-011 — DeviceIO.available_routing_channels

**D-current-public/target-U.** Dictionary get/observe. Printed key available_routing_channels holds a list of dictionaries described by routing_channel. This is an availability listing, not audio-path activation proof.

Published declaration: `available_routing_channels dictionary`; [exact source section](https://docs.cycling74.com/apiref/lom/deviceio/#available_routing_channels); `C74-LOM-DEVICEIO` B0004, B0005, B0006.

### REQ-LAPI-CONTROL-012 — DeviceIO.available_routing_types

**D-current-public/target-U.** Dictionary get/observe. Printed key available_routing_types holds a list of dictionaries described by routing_type; ordering and empty-list meaning are unspecified.

Published declaration: `available_routing_types dictionary`; [exact source section](https://docs.cycling74.com/apiref/lom/deviceio/#available_routing_types); `C74-LOM-DEVICEIO` B0007, B0008, B0009.

### REQ-LAPI-CONTROL-013 — DeviceIO.default_external_routing_channel_is_none

**D-current-public/target-U.** Bool get/set, described since Live11:1 means the default channel for External routing types is none. Other values, initialization, persistence and switching/selection side effects are not specified.

Published declaration: `default_external_routing_channel_is_none bool`; [exact source section](https://docs.cycling74.com/apiref/lom/deviceio/#default_external_routing_channel_is_none); `C74-LOM-DEVICEIO` B0010, B0011, B0012.

### REQ-LAPI-CONTROL-014 — DeviceIO.routing_channel

**D-current-public/target-U.** Dictionary get/set/observe with display_name[symbol] and identifier[symbol]; can be set to values found in available_routing_channels. Label alone is not the stable identity or a complete serialization law.

Published declaration: `routing_channel dictionary`; [exact source section](https://docs.cycling74.com/apiref/lom/deviceio/#routing_channel); `C74-LOM-DEVICEIO` B0013, B0014, B0015.

### REQ-LAPI-CONTROL-015 — DeviceIO.routing_type

**D-current-public/target-U.** Dictionary get/set/observe with display_name[symbol] and identifier[symbol]; can be set to values found in available_routing_types. Compatibility with current channel and invalid/stale selection behavior remain U.

Published declaration: `routing_type dictionary`; [exact source section](https://docs.cycling74.com/apiref/lom/deviceio/#routing_type); `C74-LOM-DEVICEIO` B0016, B0017, B0018.

### REQ-LAPI-CONTROL-016 — Groove.base

**D-current-public/target-U.** Printed under Children despite primitive int; get/set only. Index-based values are0=1/4,1=1/8,2=1/8T,3=1/16,4=1/16T,5=1/32. Do not silently reclassify as an object child or infer an observable capability.

Published declaration: `base int`; [exact source section](https://docs.cycling74.com/apiref/lom/groove/#base); `C74-LOM-GROOVE` B0007, B0008, B0009.

### REQ-LAPI-CONTROL-017 — Groove.name

**D-current-public/target-U.** Printed under Children as symbol get/set/observe; represents the groove name. Encoding, duplicate-name identity and persistence are unspecified.

Published declaration: `name symbol`; [exact source section](https://docs.cycling74.com/apiref/lom/groove/#name); `C74-LOM-GROOVE` B0010, B0011, B0012.

### REQ-LAPI-CONTROL-018 — Groove.quantization_amount

**D-current-public/target-U.** Printed under Children as float get/set/observe; represents the quantization amount. No unit, accepted range, percent conversion or timing algorithm is provided.

Published declaration: `quantization_amount float`; [exact source section](https://docs.cycling74.com/apiref/lom/groove/#quantization_amount); `C74-LOM-GROOVE` B0013, B0014, B0015.

### REQ-LAPI-CONTROL-019 — Groove.random_amount

**D-current-public/target-U.** Printed under Children as float get/set/observe; represents random amount. Range, units, random distribution, seed and note correlation are unspecified.

Published declaration: `random_amount float`; [exact source section](https://docs.cycling74.com/apiref/lom/groove/#random_amount); `C74-LOM-GROOVE` B0016, B0017, B0018.

### REQ-LAPI-CONTROL-020 — Groove.timing_amount

**D-current-public/target-U.** Printed under Children as float get/set/observe; represents timing amount. Units, scale, extrapolation, mapping and timing transformation remain unknown.

Published declaration: `timing_amount float`; [exact source section](https://docs.cycling74.com/apiref/lom/groove/#timing_amount); `C74-LOM-GROOVE` B0019, B0020, B0021.

### REQ-LAPI-CONTROL-021 — Groove.velocity_amount

**D-current-public/target-U.** Printed under Children as float get/set/observe; represents velocity amount. Units, signed range, clipping and interaction with notes/groove dynamics remain unknown.

Published declaration: `velocity_amount float`; [exact source section](https://docs.cycling74.com/apiref/lom/groove/#velocity_amount); `C74-LOM-GROOVE` B0022, B0023, B0024.

### REQ-LAPI-CONTROL-022 — GroovePool.grooves

**D-current-public/target-U.** Child list of Groove, get/observe only; source says top-to-bottom pool order, accessible by index. Empty/stale indices, reordering, loading/removal and notification ordering are unspecified.

Published declaration: `grooves list of Groove`; [exact source section](https://docs.cycling74.com/apiref/lom/groovepool/#grooves); `C74-LOM-GROOVEPOOL` B0006, B0007, B0008.

### REQ-LAPI-CONTROL-023 — TuningSystem.name

**D-current-public/target-U.** Symbol get/set/observe; names the currently active tuning system. Renaming is not evidence of loading a different system or changing pitch.

Published declaration: `name symbol`; [exact source section](https://docs.cycling74.com/apiref/lom/tuningsystem/#name); `C74-LOM-TUNINGSYSTEM` B0006, B0007, B0008.

### REQ-LAPI-CONTROL-024 — TuningSystem.pseudo_octave_in_cents

**D-current-public/target-U.** Float get only; pseudo-octave in cents for the current system. No setter, accepted numerical range or relationship to an octave number is specified.

Published declaration: `pseudo_octave_in_cents float`; [exact source section](https://docs.cycling74.com/apiref/lom/tuningsystem/#pseudo_octave_in_cents); `C74-LOM-TUNINGSYSTEM` B0009, B0010, B0011.

### REQ-LAPI-CONTROL-025 — TuningSystem.lowest_note

**D-current-public/target-U.** Dictionary get/set/observe describing note index within pseudo-octave and octave of the lowest note. Key names, key types, integer ranges and inclusive/exclusive boundary behavior are not supplied.

Published declaration: `lowest_note dictionary`; [exact source section](https://docs.cycling74.com/apiref/lom/tuningsystem/#lowest_note); `C74-LOM-TUNINGSYSTEM` B0012, B0013, B0014.

### REQ-LAPI-CONTROL-026 — TuningSystem.highest_note

**D-current-public/target-U.** Dictionary get/set/observe describing note index within pseudo-octave and octave of the highest note. Missing schema and range/interaction rules remain U.

Published declaration: `highest_note dictionary`; [exact source section](https://docs.cycling74.com/apiref/lom/tuningsystem/#highest_note); `C74-LOM-TUNINGSYSTEM` B0015, B0016, B0017.

### REQ-LAPI-CONTROL-027 — TuningSystem.reference_pitch

**D-current-public/target-U.** Dictionary get/set/observe for current reference pitch. Keys, units, tuning reference coordinate and validation rules are unspecified.

Published declaration: `reference_pitch dictionary`; [exact source section](https://docs.cycling74.com/apiref/lom/tuningsystem/#reference_pitch); `C74-LOM-TUNINGSYSTEM` B0018, B0019, B0020.

### REQ-LAPI-CONTROL-028 — TuningSystem.note_tunings

**D-current-public/target-U.** Dictionary get/set/observe; relative note tunings in cents, described as a single-element dictionary holding an array. The key, array size/order, reference meaning and accepted values are not supplied.

Published declaration: `note_tunings dictionary`; [exact source section](https://docs.cycling74.com/apiref/lom/tuningsystem/#note_tunings); `C74-LOM-TUNINGSYSTEM` B0021, B0022, B0023.

### REQ-LAPI-CONTROL-029 — this_device root context

**D-current-public/target-U.** The root identifies the Device containing the live.path object receiving goto this_device. The entry prints an ordinary track/device canonical path example; nested/return/Main placements and lifetime follow their own evidence, not an all-devices-on-tracks law. The entry declares zero direct members; Device inheritance is routed to its separate owner.

Published declaration: `root context`; [exact source section](https://docs.cycling74.com/apiref/lom/this_device/); `C74-LOM-THIS_DEVICE` B0001, B0002, B0003, B0004.

### REQ-LAPI-CONTROL-U-CONTROL — Controller ownership, timeout and lifecycle

**U/target-U.** The Application control-surface list follows Preferences order; the same root-path order is not guaranteed; script-requested versus realtime forwarding, grab/release ownership, wrong-owner cleanup, disconnect, timeout parameter int/float discrepancy and unspecified units need matched evidence.

### REQ-LAPI-CONTROL-U-ROUTING — Routing dictionary and bus lifecycle

**U/target-U.** Bus identity/cardinality, dictionary serialization, stale/invalid routing IDs, type/channel interaction, persistence and actual signal/latency outcomes remain unknown.

### REQ-LAPI-CONTROL-U-GROOVE — Groove amounts and pool lifecycle

**U/target-U.** Printed Children primitives do not establish navigable object children; amount units/ranges/algorithms, pool mutation/identity, probability/timing and commit/persistence remain unknown.

### REQ-LAPI-CONTROL-U-TUNING — Tuning dictionaries and active-system lifecycle

**U/target-U.** Missing dictionary keys/units/ranges and empty/no-system behavior prevent complete typed payload contracts; scale/clip/device/pitch conversion and persistence remain unknown.

## Finite acceptance proposals and unresolved contexts

[41 proposed actions](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/cases.json)
cover29 documentary roles and12 explicit U probes across33 requirements. Every
actual message/numeric/signal/timing documentary and target expectation/comparator
is null/U/unexecuted. Actions require [independently admitted positive setups](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/fixtures.json);
source prose is stored separately as source_claim, not used as a fabricated result.

ControlSurface.send_receive_sysex prints int in the timeout parameter annotation
but float in prose and supplies no timeout unit here. Tuning dictionaries omit
keys; Groove amounts omit units/ranges. These gaps stay unresolved, with no
runtime call, invented schema, seconds conversion or numeric comparator.

## Analysis-only evidence and denominator

[Six retained source identities](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/sources.json)
include original URLs/capture timestamps/full hashes and unchanged local paths
relative to the max-api inventory directory.
[Exact blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/source-blocks.json)
retain source IDs/HTML lines/columns/anchors. This reuses the independently reviewed
[R1 inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/manifest-inventory-r1.json),
not mutable source-family prose or recaptured pages. [Source/owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/inventory-pins.json)
and [member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/member-ledger.json)
map all28 declarations to partial contracts/cases; zero members are semantically
complete. this_device has zero direct declarations and one separately labeled
root-context contract, not an invented member. Full45-entry/588-declaration
coverage, inheritance, version, lifecycle and legal/profile obligations remain open.
[Author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/manifest-author-r2.json)
freezes this partial packet for independent review.

## Preserved R1 and focused correction

The [initial independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/live-api-control-tuning-review.json)
required LAC-REVIEW-001/002: restrict the explicit-request caveat to engine channel
messages and state that matching surface order is not guaranteed. R1 payloads,
manifest and freeze remain byte-exact in archive-r1. R2 changes only those two
contract/source-claim phrases and successor metadata/snapshots; cases/actions,
counts, source bytes and all null outcomes remain unchanged. Independent focused
review is pending; no behavioral or target completion follows from the correction.
