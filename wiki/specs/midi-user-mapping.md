---
id: SPEC-MIDI-USER-MAPPING
type: spec
status: draft
updated: 2026-10-09
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# MIDI user controller mapping

## Scope

This draft specifies the user-defined InstantMappings configuration interface
for FEAT-MIDI-USER-MAPPING, a bounded subset of FEAT-ECOSYSTEM, with
dependencies on FEAT-MIDI, FEAT-DEVICES and
FEAT-TRANSPORT in the [feature map](feature-map.md). The user task is to assign
controller MIDI messages to the supported device, mixer, transport and visible
Drum Rack pad controls. Scope is configuration recognition, assignment routing,
and the documented target of each assignment for the pinned macOS package.

The requirements below are **proposed behavioral contracts** supported by
shipped documentation or labeled static derivations, not reference executions.
No compatibility result or implementation is claimed. This revision remains a
draft until evidence contradictions, required unknowns and separate review are
resolved. [ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits this
static-first draft without a prior runtime capture.

Excluded: arbitrary control-surface scripts, MIDI Learn, other controller
profiles, exact device-bank contents, numerical parameter curves, audio output,
quantization, sample timing, SysEx, MPE, MIDI clock, and the wider behavior of the
targeted mixer/device/transport commands. Mapping a transport button does not
specify the complete transport engine. No controller hardware is assumed.

## Inputs and preconditions

Configuration is a text file named `UserConfiguration.txt`, placed in a
letter-prefixed directory beneath `User Remote Scripts`. Its public section/key
names are part of the input interface. A reference case requires a selected
surface, correctly routed MIDI input/output ports, a known set/device state,
unique assigned MIDI addresses, and no competing MIDI mappings. Discovery and
activation timing are unknown; the acceptance harness must record how it made
the profile active rather than assume live reload.

Unless a case overrides it, start from the retained shipped template with
`GlobalChannel: 0`, all control-number assignments `-1`, per-control channels
`-1`, all map-mode settings `Absolute`, `InvertMuteButtonFeedback: True` and
`MixerButtonsToggle: False`. These are observed template values, not proof that
omitting a key has the same result. See appendix D1–D2.

## Requirements

Evidence references D1–D7 and S1–S3 are defined in the analyst appendix.
D labels denote documentation; S labels denote static derivations. Static paths
are conditional on successful host initialization and MIDI delivery.

| Requirement ID | Preconditions and input | Required output/state transition | Errors and boundary behavior |
| --- | --- | --- | --- |
| REQ-MIDI-USER-001 | A letter-prefixed directory in `User Remote Scripts` contains the exact configuration filename. | The directory name is offered as a Control Surface name. | Character encoding, non-ASCII letters, invalid-name handling, enumeration order and refresh timing unknown. D1. |
| REQ-MIDI-USER-002 | Assign a supported control a MIDI number and channel. | `Pad1Note`–`Pad16Note` address notes; other control-number assignments address CCs. Supported numbers are 0–127 inclusive and channels 0–15 inclusive. | For ordinary CC assignments, missing identifiers, out-of-range integers and ordinary integer-conversion failures (for example `abc`) leave that assignment disabled, including `-1`. Pad parsing differs: an invalid integer note is omitted; noninteger pad values can abort profile construction. Interpolation errors (such as `%` or `%(missing)s`) are outside the safe-disable claim; host diagnostics/recovery unknown. D2, S1–S2. |
| REQ-MIDI-USER-003 | Set `GlobalChannel` to a valid channel. Set an exposed per-control channel to `-1`, or a valid channel. | `-1` selects `GlobalChannel`; a valid explicit channel selects that channel for that control. | Ordinary per-control channels that are missing, outside 0–15, or fail ordinary integer conversion fall back to the valid global channel. Pads inherit only when channel is absent or `-1`; another invalid integer pad channel omits that pad. Missing/invalid global channel falls back to 0 for ordinary controls, but does not rescue pads lacking a valid explicit channel. D2, S1–S2. |
| REQ-MIDI-USER-004 | Configure a non-mixer button and send a positive CC value followed by zero. | A positive value represents press and zero release. For Play/Stop, positive values set playing true/false; zero does not invert playback. Transport toggle buttons invert their named Boolean on positive and ignore zero. PunchIn/Out and NudgeUp/Down are true while positive and false on zero. | Repeated positive values retrigger the transport toggles; Play remains playing. Rewind/fast-forward hold begins on positive and stops on zero; exact seek timing unknown. Alternate Note messages remain outside the CC contract. D2, S3. |
| REQ-MIDI-USER-005 | Set a map-mode key to a supported spelling. | Support `Absolute`, `Absolute14Bit`, `LinearSignedBit`, `LinearSignedBit2`, `LinearTwoCompliment`, `LinearBinaryOffset`, `AccelSignedBit`, `AccelSignedBit2`, `AccelTwoCompliment`, `AccelBinaryOffset`; preserve the literal `Compliment` spelling. | Modes apply to device encoders, volume controls, send controls and crossfader via their respective keys. Missing mode selects Absolute. An Absolute14Bit assignment retains that mode through CC95; CC96–127 selects Absolute at the traced mapping boundary. Unknown/case-mismatched spellings have unknown host-visible outcomes; do not assume an Absolute fallback. Numeric transforms, 14-bit pairing, acceleration and pickup unknown. D2, D6, S1. |
| REQ-MIDI-USER-006 | Assign note numbers/channels to visible Drum Rack pads 1–16. | The assigned notes play visible pads arranged row-major: 1–4 top row, 5–8 next, 9–12 next, 13–16 bottom row. | Note-off handling, velocity transformation, scroll updates and collisions unknown. D3. |
| REQ-MIDI-USER-007 | Assign 1–16 valid device encoders; select an unlocked device. | Valid encoder assignments are considered in slot order, skipping disabled slots. They address up to 16 parameters of that device. With at most 8 valid assignments a bank selects 8 parameters; with 9–16 it selects two banks of 8 parameters. | The threshold uses number of valid assignments, not highest numbered configured slot. Fewer available parameters and actual device-specific parameter ordering remain unknown. D4, S2. |
| REQ-MIDI-USER-008 | Configure device bank and activator/lock buttons. | Configured direct-bank buttons select successive banks in configured slot order, skipping disabled slots; `NextBankButton`/`PrevBankButton` change bank; `OnOffButton` toggles Device Activator; `LockButton` locks the other device controls to the selected device. | With only `Bank8Button` assigned, that button selects the first bank under the traced path; this refines a possible literal reading of its label. Next alone cycles by one bank with wrap; when Previous is configured, Next/Previous step by the active width (one or two banks) without wrapping. Device bank count must be positive. Lock release, deletion of a locked device and simultaneous messages unknown. D4, S2. |
| REQ-MIDI-USER-009 | Configure mixer controls for a known bank of 8 tracks. | Volume sliders target track volume; Send1/Send2 knobs target sends A/B; mute/solo/select/arm buttons target their named track state. Mixer next/previous bank buttons change the controlled bank of 8 tracks. | Track ordering, return/group/hidden tracks, missing sends, partial banks, exclusive arm/solo and bank limits unknown. D5. |
| REQ-MIDI-USER-010 | Assign the master/cue/crossfader controls. | `MasterVolumeSlider` targets master volume, `CueVolumeSlider` cue/preview volume and `CrossfaderSlider` the crossfader. `VolumeMapMode` applies to volume controls; `SendsMapMode` to send controls; `CrossfaderMapMode` to the crossfader. | Scaling, clipping, smoothing and values for absent targets unknown. D6. |
| REQ-MIDI-USER-011 | Set `MixerButtonsToggle` to `True` or `False`; optionally configure mute feedback. | `True` declares toggle buttons; `False` momentary buttons. Momentary mixer buttons act on each positive input and ignore zero; toggle mixer buttons act on both zero and positive input (zero is not a forced-off state). Missing toggle setting acts as toggle, unlike the shipped explicit False. With `InvertMuteButtonFeedback: True`, feedback is on for an unmuted track and off for a muted track. | Mute on a valid track inverts on each actionable input. Solo/arm require controlled exclusive preferences and selection; unarmable tracks ignore arm. Exact MIDI feedback bytes and startup feedback unknown. D5–D6, S2. |
| REQ-MIDI-USER-012 | Configure transport buttons on a loaded set. | Stop/Play target playback stop/start; Rec/SessionRec/Over/Metro/Loop toggle Arrangement Record/Session Record/Arrangement Overdub/Metronome/Arrangement Loop. Rwd/Ffwd target rewind/fast-forward; PunchIn/PunchOut target punch states; NudgeUp/NudgeDown target Phase Nudge; TapTempo targets Tap Tempo. | The actual key is `FfwdButton` despite the adjacent `FwdButton` comment. Seek rate, nudge magnitude, tempo estimation, release and interaction timing unknown. D7. |
| REQ-MIDI-USER-013 | Edit only fields exposed by the configuration interface. | The interface maps the supported features; it does not define new feature commands or edit the underlying device parameter banks. Option names are case-insensitive; section names are case-sensitive. Duplicate normalized options, duplicate sections and pre-section non-comment content fail configuration parsing. Boolean values accept case-insensitive `1/yes/true/on` and `0/no/false/off`; other Boolean text fails parsing. | Host-visible diagnostics/recovery and unknown-key behavior remain unknown; malformed pad/Boolean fields are not safely disabled controls. D1, S1. |

## Timing and state

MIDI channels and control numbers are zero-based integer identifiers; MIDI data
values in these cases are integer bytes in 0–127. No wall-clock, musical-clock,
latency, jitter or numerical parameter tolerance is established. Do not use an
arbitrary timeout as evidence of a no-action result. A later execution harness
must establish a bounded completion/observation method before claiming pass.

Relevant state includes selected and locked device, device bank, mixer bank,
track states and transport states. Documented state changes are confined to the
requirements above. Selection retention, simultaneous-message ordering, duplicate
address priority, missing targets and focus interaction are unknown. Tests use
one assignment at a time except explicit conflict cases.

The file is persistent input; persistence of active banks/lock state across set
save/reopen, surface reselect or process restart is unknown. Whether configuration
edits require restart/reselection is unknown. Undo/redo membership and interaction
with automation recording are unknown and outside known expectations in this
revision.

## Errors, cancellation and teardown

Ordinary numeric CC fields use the derived disable/fallback rules above only
for missing fields, out-of-range integers and ordinary integer-conversion
failures. Configuration interpolation can fail before numeric conversion; it
is outside this safe-fallback contract and its host outcome remains unknown. Pad
integer parsing and Boolean parsing can instead abort profile construction on
malformed values; host-visible error presentation and continued profile
availability remain unknown. Duplicate sections/options and pre-section content
fail parsing under the retained static trace; host presentation and unknown-key
effects remain unknown. No safe unknown-mode fallback is promised.

No asynchronous configuration operation or cancel affordance is established.
Cancellation coverage therefore means changing surface selection while a
momentary control is held; the resulting state is unknown. Teardown covers
MIDI-port disconnect, profile deselection and exit with a held note/button.
Release cleanup, stuck-note prevention, output feedback and reconnect behavior
are unknown. These are applicable gaps, not omitted passing cases.

## Acceptance cases

The canonical detailed cases are in the
[machine-readable matrix](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/acceptance-cases.json).
Each has stable ID, requirement links, explicit input/setup, provenance,
comparison rule, and `execution_status: not-run`. The compact groups below are
navigation only; the matrix owns concrete inputs and expected fields.

| Case group | Requirements | Case kinds | Expected-result limit |
| --- | --- | --- | --- |
| MIDI-USER-001–003 | 001, 013 | Positive, negative | Valid discovery is documentation-derived; invalid names/filename unknown. |
| MIDI-USER-004–009 | 002, 003 | Positive, boundary, negative | Endpoints documented; ordinary range/conversion failures disable assignments or trigger channel fallback; interpolation errors are excluded. |
| MIDI-USER-010–013 | 004, 011, 012 | Positive, boundary | Play/release, device activator and mixer momentary/toggle message effects derived. |
| MIDI-USER-014–016 | 005 | Positive, malformed, boundary | Ten mode spellings established; numeric transforms and unknown-mode host outcomes unknown. |
| MIDI-USER-017–020 | 006–008 | Positive, boundary | Pad geometry, bank width threshold and named lock/activator targets documented. |
| MIDI-USER-021–023 | 009–011 | Positive, boundary | Mixer targets and inverted feedback meaning documented; wire feedback unknown. |
| MIDI-USER-024–028 | 002, 003, 005, 013 | Malformed, negative | Ordinary missing/noninteger values and duplicate parse failure derived; unknown fields and conflicts unresolved. |
| MIDI-USER-029–032 | 003, 004, 006, 008, 012 | State, cancellation, teardown | Reload, held controls and disconnect outcomes unknown. |
| MIDI-USER-033–046 | 002–005, 008, 011–013 | Positive, boundary, malformed | Static-derived pad exceptions, Booleans, 14-bit threshold, repeated inputs, transport holds, sparse/paired bank selection, configuration lexical rules and interpolation gaps. |

Logical comparisons use exact integer/channel/target identifiers or exact Boolean
state where an expected state is supported. Numeric parameter curves, bank
contents and feedback bytes have no oracle yet and must not be graded as passes.
An unknown expected result has comparator `unresolved`, never an invented
golden output. Documentation provenance is not an observed reference result.

## Open questions

See the canonical [question register](../questions.md): Q-008 covers parser/host
error recovery and unknown-mode outcomes; Q-009 covers numeric transforms,
takeover, timing and feedback; Q-010 covers discovery/reload, disconnect,
persistence and undo. Routing conflicts and remaining bank/lock boundaries also
remain unresolved. Prefer a focused static trace for material gaps; use a bounded runtime probe
when static evidence cannot resolve the question or the probe is clearly cheaper,
under ADR 0002. Concrete expected outcomes absent
from this draft remain unknown and block release of the affected behavior.

## Analyst evidence appendix

This section and its restricted links are analysis-only and must be removed or
reviewed when preparing a self-contained handoff. The retained source identity
is [MIDI mapping sources](../research/sources/midi-user-mapping-12.4.3.md), source ID
`SRC-MIDI-USER-MAPPING-1243`. The [source manifest](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/source-manifest.json)
pins the copies and SHA-256 digests. The [research synthesis](../research/midi-user-mapping.md)
owns the analysis findings and limitations.

| Local evidence label | Exact source locator in Ableton Live 12 Suite 12.4.3 | What is observed / limitation |
| --- | --- | --- |
| D1 | `_Tools/InstantMappings-HowTo.txt` lines 8–22 | Documented scope, name and placement convention; no observed loader run. |
| D2 | `_Tools/UserConfiguration.txt` lines 5–55, 68–99, 115–147 | Documented ranges, fallback, message types and modes; template bytes do not prove parser defaults or wire behavior. |
| D3 | `_Tools/UserConfiguration.txt` lines 59–99 | Documented pad geometry and input keys; note lifetime untraced. |
| D4 | `_Tools/UserConfiguration.txt` lines 103–171 | Documented device targets, bank threshold and lock; no parameter-bank fixture or boundary run. |
| D5 | `_Tools/UserConfiguration.txt` lines 175–267 | Documented mixer targets and mute feedback meaning; no feedback packet capture. |
| D6 | `_Tools/UserConfiguration.txt` lines 269–292 | Documented master/cue/crossfader targets, mode scope and mixer toggle setting. |
| D7 | `_Tools/UserConfiguration.txt` lines 296–340 | Documented transport targets; Fwd/Ffwd comment/key discrepancy retained. |

Retained documents: [UserConfiguration.txt](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/source/_Tools/UserConfiguration.txt)
(SHA-256 `52ec71be0a51fd89a0d1cebebc9a3f7c2a2cb62f6a55d25e7a4be3b3228322a4`)
and [InstantMappings-HowTo.txt](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/source/_Tools/InstantMappings-HowTo.txt)
(SHA-256 `6d710bba5610cba5c17213fc46472fb87843857fcba8d28f6f838d69aa1554ef`).
Both originated in `Contents/App-Resources/MIDI Remote Scripts/` in the pinned app.

Static evidence (derived with xdis from CPython 3.11 bytecode, not executed):

- S1: [configuration trace](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_UserScript/__init__.dis.txt),
  `parse_int` source lines 56–66, offsets 2–264; `create_instance` lines 96–97,
  offsets 180–266, pads lines 195–209 offsets 1088–1432 and Boolean reads offsets
  2098–2286; `parse_map_mode` offsets 46–164. The
  [mode declarations](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/ableton/v3/control_surface/elements_base.dis.txt)
  `MapMode` body lines 20–48 establishes token mappings.
- S2: [assignment trace](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Generic/GenericScript.dis.txt),
  `_init_device_component` lines 341–388, offsets 348–1322: filtered direct-bank
  buttons and valid encoders; [bank-width trace](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_UserScript/DeviceComponent.dis.txt),
  `set_parameter_controls` line 16 offsets 4–64;
  [bank button trace](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/DeviceComponent.dis.txt),
  `_bank_value` lines 397–402 offsets 134–308.
- S3: [transport trace](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/TransportComponent.dis.txt),
  initialization lines 63–81 and class line 28 offsets 14–44;
  [toggle trace](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/ToggleComponent.dis.txt),
  `_on_button_value` lines 93–100 offsets 2–244. Host property effects and actual
  scheduler timing are unmeasured.

The [parser findings](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/parser-findings.json)
PARSE-01–09 and [mapping findings](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/bytecode-mapping-findings.json)
BC-01–10 retain additional exact locators, including Boolean lexical rules,
strict duplicate rejection, the 14-bit threshold and mixer input gating.
The [matrix trace](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/ButtonMatrixElement.dis.txt),
with identity in the [supplemental matrix manifest](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/button-matrix-source-manifest.json),
closes the row width/order dependency for sparse assignments (BC-02/03).
Controls must be valid and owned without competing resources. Play behavior also
has direct documentation support; its static constant-transform helper was not
separately decoded. These are static derivations, not observed reference behavior.

Requirements translate these documented contracts into candidate
observable obligations. No generated pseudocode is an implementation input.

## Revision and handoff

Revision 1, 2026-10-09: first bounded draft and unexecuted case matrix.
[Initial independent scope review](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/scope-review.json)
requested two corrections: qualify numeric fallback to exclude interpolation
errors (SCOPE-01), and supply live assignments in channel/default cases
(SCOPE-02). Both are addressed in this draft. The
[scope recheck](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/scope-recheck.json)
and separate [quality review](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/quality-review.json)
approved the bounded analyst draft, not a handoff or compatibility claim.
Post-review editorial changes record these dispositions and align the runtime
escalation wording with ADR 0002; requirements and cases remain unchanged.
Cases 041–043 cover omitted mixer-toggle default and INI lexical rules;
044–046 add valid-CC invalid-channel, unknown interpolation and paired
more-than-eight-encoder banking cases. No handoff snapshot exists, no
implementation coverage is claimed, and no original-versus-candidate comparison
has run.
