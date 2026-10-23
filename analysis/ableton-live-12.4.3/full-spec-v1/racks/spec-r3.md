---
id: SPEC-DEVICE-RACKS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3; Live 12 documented workflows with build parity unknown
---

# Device chains and racks

## Scope and authority

This partial draft owns FEAT-RACKS and selected common FEAT-DEVICES workflows:
four rack types, parallel chains, zones, macros, variations, drum mapping,
returns, pad editing and extraction. It adds common device insertion, bypass and
preset interactions where they explain rack use. It does not specify the sound
of contained devices or the plug-in host API. The four rack profiles in the
[full inventory](../research/full-live-coverage-inventory.md) are discovery entries,
not four completed behavioral contracts.

The [Live Set structure](live-set-structure.md) owns device-list storage, generic
reader validation and identifiers. [Bundled device parameters](bundled-device-parameters.md)
owns the seven bundles' parameter values and its unresolved macro binding encoding.
[Automation](automation-envelopes.md), [mixer values](mixer-values.md) and
[mix graph](mix-graph.md) retain their existing scope; none implies that every
rack mutation, mixer operation or load is already specified. Browser navigation
belongs to [browser workflows](browser-workflows.md).

**D12** means documented in the retained official Version 12 manual captured
2026-10-19. Every D12 runtime clause has **exact-build applicability U**, even
when a schema name corroborates the feature. **D-installed** means bytes in the
pinned installed package; it specifies a documentary observation only.
**U** means no gradeable expected outcome. No reference application, original
function or candidate was executed for this packet. Nothing here is released.
Evidence keys E1–E5 resolve in the analysis-only appendix.

## Preconditions and observable state

Use a valid, editable Set; readable named samples and devices; an audio path for
audible cases; and MIDI input or clips for note cases. Reset mappings, zones,
selection, sends and exclusions to the values stated in each case. Factory
sample-dropping defaults are required where the case expects Simpler; custom
pad/default presets are a separate source of variation. Disable unrelated
randomization, automation and MIDI processing unless named. Tests of a tail use
a contained effect known independently to produce a tail. They establish rack
routing/attenuation qualitatively, never its samples or gain curve.

Track/chain membership and order, note-to-chain assignment, selection/focus,
macro values/mappings/exclusions, snapshots, send/return destinations and pad
presentation are separate observable state. Cases below compare only named
state and events. No deadline, audio tolerance, MIDI-event ordering or undo
transaction is implied by “immediate” presentation or parallel routing.

## Requirements

### REQ-DEVICE-RACKS-001 — installed vocabulary and examples

**D-installed / E3–E5.** The installed schema declares Audio Effect, MIDI Effect,
Instrument and Drum rack classes. Each declares sixteen macro control fields,
visibility count, randomization and snapshot exclusions, a chain list and macro
variations. ZoneRange declares minimum, maximum and two crossfade bounds;
MacroSnapshot declares sixteen values and sixteen presence flags. The retained
Suite demo contains respectively 23, 1, 8 and 1 rack occurrences. The retained
slicing preset contains five snapshots. These are documentary assertions, not
load/save or semantic rules for the private field names. In particular the Drum
branch's stored selector range does **not** establish a Drum Rack zone editor.

### REQ-DEVICE-RACKS-002 — rack type and legal signal placement

**D12 / E1 §25.2.** MIDI Effect Racks hold MIDI effects on MIDI tracks. Audio Effect
Racks hold audio effects on audio paths, including after an instrument on a MIDI
track. Instrument and Drum chains order MIDI effects before an instrument and
audio effects after it. Invalid placement is outside the documented valid
configuration; exact drag rejection, relocation, replacement and malformed-file
responses are U. This does not resolve the file-reader question in
REQ-LIVE-SET-STRUCTURE-012.

### REQ-DEVICE-RACKS-003 — serial, parallel and nested flow

**D12 / E1 §25.1.1.** Devices within a chain process left to right. Instrument and
effect rack chains receive the same input in parallel subject to their zones;
their outputs combine at the rack output, then feed downstream devices. Drum
chains receive assigned notes instead (REQ-016). A rack may contain racks and
acts as a device in the enclosing chain. Exact summation, ordering of coincident
MIDI events, latency and maximum practical nesting depth are U.

### REQ-DEVICE-RACKS-004 — creation, grouping and dismantling

**D12 / E1 §25.2.** Loading a generic rack creates an empty rack. Group selected
devices, Group to Drum Rack and grouping existing chains create enclosing racks;
repeated grouping can nest them. Selecting a rack title and Ungroup dismantles
that rack. The manual does not define flattening/routing resolution for every
multi-chain or return-containing rack; those outcomes are U.

### REQ-DEVICE-RACKS-005 — chain list and selection

**D12 / E1 §§25.3–25.4.1.** Dropping devices, presets or chains in the chain-list
drop area adds chains. Selecting a chain shows its devices; multiple selections
show their count. Chains expose activator, solo and hot-swap; audio-output rack
chains also expose volume/pan. Rack-title selection addresses the whole rack for
move/copy/delete. Auto Select selects chains currently processing signals;
Drum Rack selection follows receipt of the assigned note. Exact solo/activator
audio interaction, selection expiry and contention with manual selection are U.

Rack view selectors show or hide eligible Macro Controls, Chain List and Devices views, with Pad View unique to Drum Racks; hiding all views, context Fold or title double-click folds the Rack. Right-clicking the Device View selector offers a hierarchical device list whose selected entry is selected and revealed. With Chain List focused, up/down changes selection; dragging and hovering a selected chain over a Session or Arrangement track gives it focus and opens Device View. Rack and chain Rename use Edit; Info Text uses Edit or context, and chain color uses its context palette. Entire chains can be saved/recalled as browser presets without a specified save/recall gesture; file/geometry/timing outcomes remain U.

### REQ-DEVICE-RACKS-006 — available zone filters

**D12 / E1 §§25.5–25.5.1.** Instrument and MIDI Effect Racks have key, velocity and
selector zones; a note enters a chain only if it passes all three. Audio Effect
Racks have selector zones, without MIDI key/velocity zones. Drum Racks have no
zone editor; their Receive choosers filter notes. All matching parallel chains
can receive the same qualifying input.

### REQ-DEVICE-RACKS-007 — zone editing and ranges

**D12 / E1 §§25.5–25.5.4.1.** Zones can be moved and resized, with separately
editable fades. Key zones cover selected MIDI keys; velocity zones use Note On
velocities 1–127. The selector scale is 0–127; the documented initial selector
zone is the single value 0. Multiple chains may share ranges. Exact rounding,
edge inclusion for resized ranges, out-of-range edits and MIDI velocity-zero
interpretation are U here; note encoding belongs to [MIDI note storage](midi-note-storage.md).

Key, Velocity and Chain buttons select their editors; Hide hides them. Main and fade sections resize from their respective left/right edges. Move the zone itself by dragging an admitted interior of its lower main section; independent fade-section translation is not established here and remains U; the Chain selector indicator is draggable. Exact gesture geometry and boundary arithmetic remain U.

### REQ-DEVICE-RACKS-008 — fade destination

**D12 / E1 §§25.5.2–25.5.4.** Key/velocity fades attenuate incoming note velocity.
Selector fades in a MIDI Effect Rack attenuate note velocity. Selector fades in
Instrument and Audio Effect Racks attenuate chain output audio. Exact fade law,
rounding to MIDI velocity, overlap normalization and treatment of a zero-length
fade are U; no linear or equal-power equation is specified.

### REQ-DEVICE-RACKS-009 — selector filtering of controllers

**D12 / E1 §25.5.4.** Instrument and MIDI Effect Rack selector zones filter notes
by default, allowing other MIDI events such as controllers through. Enabling
Chain Selector Filters MIDI Ctrl makes the selector filter all MIDI events.
Held-note release routing and sustain/channel-mode edge cases remain U.

### REQ-DEVICE-RACKS-010 — selector movement and existing tails

**D12 / E1 §25.5.4.** For an audio-output chain with a fade ending its selector
zone, moving outside attenuates the output to zero. With no fade, leaving the
selector zone does not attenuate existing output; an existing effect tail may
finish according to that effect. This distinction does not specify audio effect
input admission, voice lifetime, clicks, smoothing or compensation changes.

### REQ-DEVICE-RACKS-011 — macro count and visibility

**D12 / E1 §25.7; E2 §§23.2.3,23.2.6.1.** A rack supports up to sixteen macros;
a newly created factory rack, with no custom default or loaded preset, shows
eight. Visibility controls change the number shown; shown/hidden state is
saved with the Set. Hidden-control mapping activity and lower visibility bound
are U. E3 corroborates sixteen storage slots, without proving runtime limits.

### REQ-DEVICE-RACKS-012 — mapping and ranges

**D12 / E1 §25.7.1.** Entering Macro Map Mode highlights mappable controls, shows
macro Map buttons and opens the Mapping Browser. Select a contained parameter,
then a macro's Map button to create an assignment; one macro can address several
parameters. Min/Max refine each assignment; Min greater than Max inverts it,
and Invert Range reverses the current range. Assignments can be edited/deleted
in that browser; leaving Map Mode ends this editing mode. Exact interpolation,
quantized parameters and out-of-domain mappings are U.

### REQ-DEVICE-RACKS-013 — delegated control and macro display

**D12 / E1 §25.7.1.** A mapped device parameter is disabled for direct control;
clip-envelope modulation remains possible. A single mapping supplies its name
and units to the macro by default. Multiple mappings restore the generic macro
name regardless of whether their units match, absent a separately applied
custom name. Multiple mappings use 0–127 units unless every target has the same
unit type and range; in that case, the common units and range are retained.
Custom names/colors/info text are editable. Restored values after unmapping and
interactions with automation override are U.

### REQ-DEVICE-RACKS-014 — randomization and exclusions

**D12 / E1 §25.7.2.** Rand randomizes mapped macros. Exclude Macro from
Randomization preserves an excluded mapped control. Macros assigned to Volume
parameters in unmodified factory Instrument Rack presets, without a user
exclusion override, are excluded by default. This last clause
does not assert an automatic exclusion after every new volume mapping.
Distribution, seed, correlation, repeatability, unchanged-value probability,
hidden/unmapped controls and randomization undo granularity are U.

### REQ-DEVICE-RACKS-015 — variations

**D12 / E1 §25.7.3.** New stores current macro state as a variation, initially
named sequentially Variation 1, Variation 2, and so on. Variations can be
renamed, duplicated and deleted. Launch recalls a stored state; Overwrite
replaces it with the current state. Exclude Macro From Variations prevents that
control changing on launch; disabling the exclusion restores participation.
Snapshot behavior during mapping changes, which unmapped values are present,
parameter automation ownership, launch scheduling and interpolation are U.

The Show/Hide Macro Variations selector exposes the variations view. Launch Macro Variation and Overwrite Macro Variation are separate buttons; Edit/context commands manage selected entries.

### REQ-DEVICE-RACKS-016 — drum receive, play and choke

**D12 / E1 §25.6.** Receive selects the note triggering a drum chain; Play selects
the outgoing note delivered to its devices. Chains assigned the same one of
sixteen choke groups silence one another when triggered. Receive All Notes
disables Play/Choke and passes through the received note. Preview fires a note
into a chain. Choke release envelopes, exact stop time, same-sample arbitration,
self-choke and preview velocity are U.

The Receive list presents note names, MIDI note numbers and standard GM drum equivalents; no complete translation table is inferred.

### REQ-DEVICE-RACKS-017 — drum sends and returns

**D12 / E1 §§25.2,25.6.** Drum Racks have up to six audio-effect return chains.
Drum-chain sends feed them after the drum chain's fader; send controls require
at least one return chain. Each return's Audio To can target the rack output or
a Set return track. A seventh return's UI/error behavior, return feedback,
missing destinations, send scaling and compensation are U.

### REQ-DEVICE-RACKS-018 — dropping onto pads

**D12 / E1 §25.6.1.** Each pad denotes a MIDI note. With factory dropping defaults,
a sample on an empty pad creates a chain with Simpler. Dropping an audio effect
on that pad adds it after the instrument. A replacement sample replaces the
Simpler/sample and preserves upstream MIDI and downstream audio effects.
Custom dropping defaults are outside this clause; failed-load atomicity is U.

Independently compatible browser instruments and presets can also be dropped onto pads; this does not establish arbitrary browser-object admission or new sample-dropping defaults.

### REQ-DEVICE-RACKS-019 — pad distribution, swapping and layering

**D12 / E1 §25.6.1.** Multiple samples dropped normally populate chromatically
upward from the destination, replacing samples while preserving effects.
Alt-drag on Windows / Cmd-drag on macOS layers them in a nested Instrument Rack.
Dragging a pad to another swaps note assignments; existing clips keep their
notes and therefore address the new sounds. The same platform modifier layers
both pads' chains in a nested Instrument Rack. Overflow above note 127, sample
ordering within a multiselection and effects during failed loads are U.

### REQ-DEVICE-RACKS-020 — pads represent notes, including multiple chains

**D12 / E1 §25.6.1.** The 128-note pad map shows groups of sixteen. Changing Receive
updates pad presentation; matching chains, including nested ones, respond to
the note. A one-chain pad shows that chain's name and permits rename/hot-swap.
A multiple-chain pad displays Multi; mute/solo/preview address all its chains,
rename/hot-swap are disabled, and delete removes all those chains. Exact mixed
mute/solo icon semantics and controller scrolling protocols are U.

The pad overview can be dragged or navigated with focused up/down keys; Alt Windows/Cmd macOS shifts by single rows. Empty-pad hover shows note and suggested GM instrument in Status Bar. One-chain pads also expose mute, solo, preview and delete. In active Hot-Swap, focused D switches the target between the Drum Rack and last selected pad; no global key exception or rollback is implied.

### REQ-DEVICE-RACKS-021 — rack mixing in Session

**D12 / E1 §25.8.** Instrument/Drum racks with multiple chains can unfold into the
Session mixer. Chains have no clip slots. Their controls mirror the rack list;
selecting a chain's mixer title shows its devices. Multiselected Session chains
share a mixer parameter adjustment; the same adjustment from the rack chain
list does not invoke this multi-chain behavior. Relative scaling/clamping of
unequal starting values is U.

### REQ-DEVICE-RACKS-022 — extracting chains

**D12 / E1 §25.8.1.** Chains can be moved to other racks/tracks. Dragging a drum
chain from the Session mixer to a new track transfers its devices and MIDI
notes. Dragging from the chain list transfers devices only. Dragging a drum
return to the mixer creates a return track. The exact treatment of shared-note
chains, nested mappings, clip ownership, automation, sends and source empty
clips is U; no broad preservation/undo promise is implied.

### REQ-DEVICE-RACKS-023 — inserting common devices

**D12 / E2 §§23,23.2.** Double-clicking a browser device targets the selected track
or creates a track if none is selected. Enter loads a selected device/preset on
a selected destination track. Devices can be dragged into track/device views;
sample drop on an empty MIDI Device View creates Simpler. Chains follow MIDI
effects → instrument → audio effects and process left to right. Exact
insertion position with existing selection and incompatible-device handling
are U beyond the explicit paste rule below.

### REQ-DEVICE-RACKS-024 — move, remove and paste

**D12 / E2 §23.2.** Device title selection and Delete/Backspace removes the device;
dragging its title reorders or moves it between tracks. Cut/copy/paste/duplicate
apply to devices. Paste inserts before the selected device; selecting the empty
space after the last device permits paste at the end. Rack title selection
addresses its whole contents (REQ-005). No audio continuity or retained-tail
guarantee follows from the manual's qualified continuity statement.

### REQ-DEVICE-RACKS-025 — activator bypass

**D12 / E2 §23.2.1.** The activator turns a device on/off; the manual describes an
off device as leaving the signal unprocessed. For an audio effect this provides
a qualitative bypass requirement. It does not establish sample equality,
latency changes, tail retention, CPU counters, retained processor state or the
meaning of unprocessed MIDI at a disabled instrument's audio output; those
outcomes remain U.

### REQ-DEVICE-RACKS-026 — presets and hot-swap

**D12 / E2 §§23.2.3–23.2.5.** Devices/racks can save settings as presets. Save Preset
opens the browser with a prospective name; Enter confirms and Esc cancels the
save process. Dragging a device title into a Places folder is another save
route. Hot-Swap connects a target with the browser, and only compatible device
types can be swapped. Q, Esc or the close controls exit Hot-Swap; exit alone is
not documented as restoring an earlier loaded preset. Overwrite/cancel disk
atomicity, media collection, failed loads and custom-default precedence require
separate evidence. Current-manual A/B device states and newer defaults are not
silently included in this bounded contract.

### REQ-DEVICE-RACKS-027 — malformed state, cancellation and teardown

**U / E1–E5 limits.** For malformed zone bounds, illegal note/choke/return values,
missing/duplicate snapshot members, cancelled pad/extract/mapping operations,
held notes while deleting/unmapping/choking, lost media or closing during load,
no rack-specific refusal, repair, rollback, cleanup or timing outcome has been
established. Generic file parsing remains owned by the container/structure
specifications; their checks do not prove rack-specific semantic validation.

### REQ-DEVICE-RACKS-028 — persistence, automation, undo and timing

**U except REQ-011's D12 visibility persistence.** Exact 12.4.3 reopen preservation
of mappings, zones, variants, exclusions, routing and nested references; migration;
undo/redo grouping; automation/clip modulation precedence across maps and recalls;
note-off/sustain routing across selector changes; transport/scheduler order;
latency/CPU behavior and sample-exact output remain unresolved. Schemas and
examples establish representations, not accepted-input or runtime laws.

## Historical corrected R1 acceptance cases

The following61table rows and original catalog remain exact historical R1
criteria. Current R3 acceptance is selected separately below; original records
are preserved, not executed outcomes or whole-subclause completion.

[Cases JSON](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/cases.json)
retains the same authored cases as this table. **I** cases grade only installed
source assertions. **D** cases have a documented-domain expected comparator,
with exact 12.4.3 applicability U. **U** cases are ungraded experiments with no
invented expectation. All execution results are unexecuted; “graded” describes
available criteria, not a test result. Numbers in the requirement column use
the REQ-DEVICE-RACKS prefix. State-only checks require exact equality of named
fields; event checks compare note/controller admission, without timing or event
order. No case is an original-versus-candidate compatibility pass.

| Case | Req | Kind/domain | Setup and action | Expected comparator or open result |
| --- | --- | --- | --- | --- |
| RCK-001 | 001 | Boundary/I | Parse E3 four rack classes, ZoneRange and MacroSnapshot. | Exactly sixteen macro slots and snapshot values/presence flags; four zone bounds. |
| RCK-002 | 001 | Positive/I | Reparse E4 Suite demo and count rack elements. | Audio 23, MIDI 1, Instrument 8, Drum 1; Creator 12.4d1. |
| RCK-003 | 001 | Positive/I | Decode E5 slicing ADG. | Five MacroSnapshot entries; record their stored value/presence fields without recall inference. |
| RCK-004 | 002 | Positive/D | Put a MIDI effect in a MIDI Effect Rack on a MIDI track. | Valid documented signal configuration. |
| RCK-005 | 002,027 | Negative/U | Drag an instrument into an audio-only rack, then load equivalent malformed XML. | U: refusal vs relocation/replacement and UI/load differences. |
| RCK-006 | 002,003 | Positive/D | Instrument chain: MIDI effect, instrument, audio effect. | MIDI processing precedes synthesis; audio effect follows it. |
| RCK-007 | 003 | Positive/D | Rack with two distinct active chains receiving a qualifying note. | Both chains receive the note; outputs feed the enclosing downstream chain. |
| RCK-008 | 003,004 | Positive/D | Group a device twice, then select outer title. | Two rack levels; outer selection addresses enclosing rack. |
| RCK-009 | 004 | Positive/D | Group two serial effects; Ungroup the resulting one-chain rack. | Group creates an enclosing rack; Ungroup dismantles it. |
| RCK-010 | 004,027 | Boundary/U | Ungroup a rack with parallel outputs, mappings and returns. | U: flattening, routing and mapping disposition. |
| RCK-011 | 005 | Selection/D | Select chain A then B; multiselect both. | Device View follows selected chain; multiselection indicates two. |
| RCK-012 | 005,016 | Positive/D | Enable Auto Select; send note assigned only to drum chain B. | B selected; selection expiry/timing ungraded. |
| RCK-013 | 006 | Positive/negative/D | Key zone 60–72, velocity 50–100, selector 3. Send (64,80) at 3, then (59,80), (64,40), and (64,80) at 2. | First admitted; each of three failing inputs excluded. |
| RCK-014 | 007 | Boundary/U | Send notes 60 and 72 at exact resized key edges; vary selector fractionally. | U: precise inclusive edges and fractional selector rounding. |
| RCK-015 | 007 | Boundary/D | Full-range velocity zone, no fades; send Note On velocities 1 and 127. | Both are in the documented zone range. Velocity zero ungraded. |
| RCK-016 | 006 | Negative/D | Inspect zone editors for Audio Effect Rack and Drum Rack. | Audio rack lacks key/velocity editors; Drum Rack lacks zone editors. |
| RCK-017 | 007 | Boundary/D | Assign two chain zones to single values 0 and 127; select each value. | Only its matching single-value chain is addressed. |
| RCK-018 | 009 | Negative/D | Excluded selector zone, default controller filtering; send a CC and a note. | CC passes selector filter; note does not. |
| RCK-019 | 009 | Positive/D | Repeat RCK-018 with Chain Selector Filters MIDI Ctrl enabled. | Both excluded by selector filter. |
| RCK-020 | 008 | Positive/D | Put a note inside a nonzero key fade, away from endpoints, velocity 100. | Incoming note velocity attenuated; factor/rounding U. |
| RCK-021 | 008,010 | Positive/D | Existing Instrument/Audio Effect Rack tail; leave selector zone through ending fade. | Chain output attenuated to zero outside zone; onset/time samples U. |
| RCK-022 | 010 | Negative/D | Same tail setup with no selector fade. | Leaving zone alone does not attenuate existing tail. |
| RCK-023 | 011 | Boundary/persistence/D | Create a factory rack with no custom rack default or loaded preset; change shown count to sixteen, save/reopen. | Initially eight shown; sixteen available; chosen visibility retained. |
| RCK-024 | 012 | Positive/D | Map contained control to macro; set Min greater than Max; invoke Invert Range. | Mapping Browser lists assignment and inverted range, then reversed bounds. Interpolation U. |
| RCK-025 | 013 | Negative/D | Map a contained control, then inspect direct edit and clip modulation capability. | Direct control disabled; modulation capability remains. Resulting signal U. |
| RCK-026 | 013 | Boundary/D | With no custom macro name, map two targets with the same unit type/range to macro 3; reset mappings, then map two targets with different units. | Both phases show generic Macro 3 name. Same-unit/range phase retains common units/range; different-unit phase shows 0–127 units. |
| RCK-027 | 014 | Negative/D | Mapped macro A excluded from randomization, B included; press Rand. | A unchanged; no demand that B differ on every draw. Distribution U. |
| RCK-028 | 014 | Default/D | Load an unmodified factory Instrument Rack preset with a Volume-assigned macro, with no user exclusion override. | That macro excluded by default; newly created mappings outside claim. |
| RCK-029 | 015 | Positive/D | Set mapped macros A=20,B=90; New; change A=70,B=10; launch saved variation. | A=20,B=90 restored in documented value domain. Exact timing U. |
| RCK-030 | 015 | Negative/D | RCK-029 with A excluded from variations while currently A=70. | A remains 70; B recalls 90. Disable exclusion and relaunch: A recalls 20. |
| RCK-031 | 015 | Lifecycle/D | Store two variations; rename, duplicate, overwrite selected one, delete duplicate. | Named entries and count reflect operations; overwritten variation recalls newly stored state. |
| RCK-032 | 016 | Positive/D | Receive 36, Play 60; send 36 and 37 separately. | 36 triggers chain with output note 60; 37 does not trigger it. |
| RCK-033 | 016 | Boundary/D | Receive All Notes; send 36 then 64. | Play/Choke disabled; received pitches pass unchanged to devices. |
| RCK-034 | 016 | Positive/D | Two sustained drum chains in same choke group; trigger A then B. | B silences A; release curve/time and self-choke U. |
| RCK-035 | 017 | Negative/D | Drum Rack with no returns; add one return. | No send controls initially; sends become available with return. |
| RCK-036 | 017 | Boundary/D | Create six audio-effect drum returns. | Six is documented supported limit; attempted seventh handled in RCK-061. |
| RCK-037 | 017 | Routing/D | Drum send into return; choose rack output, then existing Set return. | Return output destination follows chooser; exact audio/gain/latency U. |
| RCK-038 | 018 | Positive/D | Factory sample-dropping defaults; drop sample A on empty pad 36, then audio effect. | Chain with Simpler A; effect follows it. |
| RCK-039 | 018 | Replacement/D | Chain MIDI effect → Simpler A → audio effect; drop sample B on same pad. | Sample/instrument replaced; both surrounding effects retained. |
| RCK-040 | 019 | Positive/D | Drop samples A/B on empty pad 36 normally. | Two Simplers/chains assigned upward chromatically from 36; multiselection order U. |
| RCK-041 | 019 | State/D | Swap populated pads 36/38 by normal drag; play unchanged clip notes. | Note assignments swapped; clip notes now trigger swapped sounds. |
| RCK-042 | 019 | Positive/D | Cmd-drag two samples on macOS / Alt-drag on Windows onto pad 36. | Both samples layered in nested Instrument Rack; platform parity U. |
| RCK-043 | 020 | Negative/D | Two chains receive 36; inspect pad, then rename/hot-swap and mute. | Multi label; rename/hot-swap unavailable; mute addresses both chains. |
| RCK-044 | 021 | State/D | Unfold two-chain Instrument Rack in Session; change pan in either view. | Chain has no clip slots; corresponding pan display mirrors change. |
| RCK-045 | 021 | Boundary/D | Two chains equal starting volume; multiselect in Session, adjust one; repeat via chain list. | Session adjustment affects both; list adjustment lacks this multi-chain behavior. Unequal starts U. |
| RCK-046 | 022 | Extraction/D | Drum clip notes 36/38; extract only chain receiving 38 to new track from mixer; repeat from chain list on reset Set. | Mixer route transfers chain devices and its MIDI notes; list route devices only. Shared-note/nested ownership U. |
| RCK-047 | 022 | Extraction/D | Drag a Drum Rack return into mixer drop area. | New Set return track; exact send reassignment U. |
| RCK-048 | 023 | Positive/D | Select empty MIDI track; Enter a browser instrument; separately drop sample in its empty Device View. | Instrument loads; sample scenario creates Simpler. |
| RCK-049 | 024 | Order/D | Copy effect X; select effect B in A→B chain and paste, then select empty chain end and paste. | First copy immediately before B; second at end. |
| RCK-050 | 025 | Bypass/D | Audible processing effect active; turn activator off. | Effect processing bypassed qualitatively; delay/tails/state/CPU counts U. |
| RCK-051 | 026 | Cancellation/D | Enter Hot-Swap; load a compatible preset; press Esc. | Hot-Swap exits; rollback to pre-load preset is not an expected result. |
| RCK-052 | 026 | Cancellation/D | Save Preset, give prospective name; press Esc instead of Enter. | Save process cancelled; exact files/temp cleanup and pre-existing overwrite atomicity U. |
| RCK-053 | 027 | Malformed/U | In copied XML set zone Min=100, Max=20; fade outside zone; invalid receiving/choke value. | U: refusal/repair/stored/runtime outcomes. |
| RCK-054 | 027 | Malformed/U | Duplicate/missing snapshot values, absent presence flags; load a copy. | U: rack-specific reader response and defaults. |
| RCK-055 | 027 | Cancellation/U | Begin pad replacement, chain extraction or mapping; cancel before completion. | U: rollback, selection, dirty-state, source MIDI and undo outcome. |
| RCK-056 | 027,028 | Teardown/U | Hold a note/sustain; delete rack/chain, remove mapping, change selector or close Set. | U: note-off, tail, cleanup and scheduler behavior. |
| RCK-057 | 028 | Timing/U | Recall variation and automate selector at transport boundary with delayed contained device. | U: event order, compensation, smoothing and sample timing. |
| RCK-058 | 028 | Persistence/undo/U | Edit zones/maps/exclusions/routing, undo/redo, save/reopen and migrate. | U: exact preserved state and transaction grouping, apart from RCK-023 visibility. |
| RCK-059 | 019,027 | Boundary/U | Drop three samples at pad 127, including missing second sample. | U: overflow handling, partial load and effects retention. |
| RCK-060 | 025,027 | Negative/U | Disable a sounding instrument or entire mixed rack. | U: MIDI-to-audio bypass, retained state/tails and CPU/latency effects. |
| RCK-061 | 017,027 | Boundary/U | Attempt seventh Drum Rack return through UI and copied document. | U: rejection/repair and whether UI vs load differs. |

There are 61 cases: 3 installed-document assertions, 46 documented-domain
criteria, and 12 ungraded U cases. Every runtime case remains unexecuted and has
target-build applicability U. The installed assertions do not grade a program's
runtime conformance. These cases cover all six required kinds at packet level;
each destructive/format/timing uncertainty stays explicit rather than being
replaced by a generic safe behavior.

## Open interactions and completion boundary

This is a partial F-05 contract. [Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
owns target/manual reconciliation. [Q-025](../questions.md#q-025-device-host-protocol-and-device-audio-acceptance)
is relevant to host/mapping uncertainty; its unresolved state is unchanged.
Unspecified rack paths include all exact fade/summing functions, note-off and
sustain ownership, MPE/expression channels, host failure, resource limits,
custom-default precedence, generic rack preset media retention and most
persistence/undo/cancellation/teardown semantics. Plug-in hosting, Max and each
native device require their own contracts. No four-rack profile is complete.

## Analysis-only evidence appendix

Canonical synthesis: [rack research](../research/device-racks.md).
All captures and exact SHA-256 identities: [source records](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/sources.json).

- **E1 / RACKS-MAN-RACKS:** official [Instrument, Drum and Effect Racks](https://www.ableton.com/en/live-manual/12/instrument-drum-and-effect-racks/),
  Version 12, captured 2026-10-19; [retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manual-racks-2026-10-19.html).
  Section numbers cited beside clauses resolve through [heading/HTML-line records](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manual-racks-headings.json)
  and [derived text](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manual-racks.txt).
  Current major-version documentation, not observed 12.4.3 execution.
- **E2 / RACKS-MAN-DEVICES:** official [Working with Instruments and Effects](https://www.ableton.com/en/live-manual/12/working-with-instruments-and-effects/),
  same version/capture limitation; [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manual-devices-2026-10-19.html),
  [heading records](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manual-devices-headings.json).
- **E3 / RACKS-SCHEMA:** installed `12.0_12402`, exact class lines and fields in
  [schema-fields](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/schema-fields.json);
  source bytes also retained by the [inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt).
- **E4 / RACKS-DEMO:** installed Suite Demo, Creator 12.4d1; exact source/hash,
  rack class/ordinal, branch and zone XML in [shipped-racks](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/shipped-racks.json).
  Historical shipped file, not a fresh 12.4.3 save.
- **E5 / RACKS-VARIATION-EXAMPLE:** installed Defaults/Slicing/Default.adg,
  Creator 12.4d1; [retained original bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/variation-example.adg)
  and [decoded snapshot evidence](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/variation-example.json).
  Five stored snapshots; no inferred recall algorithm.

[Native string excerpts](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/native-strings.json)
retain exact export line/hash/reference records for names such as ZoneRange,
DrumBranch and MacroVariations. They corroborate presence only and support no
additional runtime clause. [Frozen packet manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manifest.json)
pins payloads and authored pages for separate analyst review. Native identifiers,
raw XML and these restricted links must be removed or reviewed before handoff.

## Historical R2 bounded primary-Racks source adoption

The [independently reviewed full primary audit](../../analysis/ableton-live-12.4.3/full-spec-v1/racks-source-audit/README.md)
and [source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-source-audit-review.json)
retain124primaryblocks/264judgments/53literalresources plus only seven selected
CommonDevicesdefault/drop paragraphs. This is not the separate153block Common
Devices audit. REQ023–026 and RCK048–052 remain exact; no A/B/default behavior
is adopted. Exact Version12 publication/target12.4.3 parity remainsU. Source UTC
is retained from the original capture, not replaced by author UTC.

[Current R2 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/cases-r2.json)
contain81records:61old verbatim plus20new RCK062–081. Criterion classes are
3installed assertions/66documented-domain proposals/12U. All actual outcomes are
null/U/unexecuted in the [explicit status](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/actual-status-r2.json);
old expected/source assertion strings remain documentary only. Three new named
UI-role documentary pairs are nonnull,17null; allnew legacy expected comparators
and numeric/signal/file/message/RNG/timing comparisons are null.

[The22-group ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/adoption-r2.json)
adds only bounded local control/input branches under the same28IDs, with six
clause refinements. Twenty groups receive compound actions with separate resets.
Group14controller/hardware protocols remainU; Group22 retains053–061U rather
than duplicating placeholders. Missing algorithms and lifecycle paths remain open.

Genuine note AND CC reception precedes018/019 selector exclusions. Sustained
nonzero NO-exit tail precedes021/022 exit with/withoutfade; BOTH mapped controls
must independently work before Rand or variation exclusion. Actual per-chain
input/control precedes mute/delete. All audible comparisons require working
nonzero processing/wet/send/return/output; editor control needs no audio.
[Future guards](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/fixtures-r2.json)
apply before grading old or new trials; failed positives remainU.

Old020KEYfade is not new VELOCITY or MIDI-selector fade; old042BROWSERlayer is
not new pad-to-pad layer; configuredMulti043 is not Receive-change. Pan044 and
equal-volume045 remain true but do not cover every mixer control; extraction046/
047 retains actual mixer-versus-list and return routes. RR01 generic name is
independent of the same-unit AND same-range exception; new third-branch action
uses same-unit/different-range without new numeric law. RR02 factory/no-custom/
no-preset eight macros, unmodified factory Volume/no-exclusion-override, and
factory sample-dropping Simpler qualification remain exact.

Empty-alt images establish no plus/minus glyphs; unseen eight-step image no
geometry/fade law. Sixreturns is documented, seventh061U. No gain/curve/fade/
RNG/codec/timing or controller protocol, custom-default/undo/cancel/persistence/
teardown law is added. [Exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/delta-r2.json),
[preserved old identities](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/prior-files-r2.json)
and [consumer census](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/consumer-impact-r2.json)
retain all18old packet files and both seals in place. Consumers retain historical
as-of providers; no automatic adapter or old author/capture/validator replay.
**AS-OF AUTHOR FREEZE:** independent R2 owner review pending; [spec index](index.md)
owns current disposition. No full Rack/group/source-topic/product completion,
handoff, runtime execution or candidate compatibility is claimed.

## R3 focused zone-gesture clarification

The [independent R2 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r2-review.json)
required separating B044 roles. Both main and fade sections resize at their
respective edges; the move target is the zone itself, using an admitted lower-main
interior drag. Independent fade-section translation remains U. The raw source
and older audit shorthand are preserved; an [additive qualification](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/audit-shorthand-qualification-r3.json)
explains why shorthand is not proof of another movement operation.

[Current R3 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/cases-r3.json)
retain81IDs,3installed assertions/66documentary proposals/12U. Only007's appended
clause and066's proposed setup action are clarified, with matching plan metadata.
All other five R2 appends, all61original records, every81source claim/oracle/guard
and all36R2files/seals remain exact. Existing [actual status](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/actual-status-r2.json)
still covers all81IDs as null/U/unexecuted; no numeric, geometry, signal, time,
file, RNG or source-silent lifecycle law is added. Common023–026/048–052 remain
exact; no Common Devices/A-B/default adoption. [Exact correction](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/correction-r3.json)
uses immutable R2 snapshots as the before providers, with no duplicate archive
or old author/checker/consumer replay/adapter.
**AS-OF AUTHOR FREEZE:** independent focused R3 review pending; [spec index](index.md)
owns current disposition. The author reviewed R2 but does not self-approve R3;
no full Rack, source or exact-build completion follows.
