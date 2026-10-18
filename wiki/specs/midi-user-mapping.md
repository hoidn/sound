---
id: SPEC-MIDI-USER-MAPPING
type: spec
status: draft
updated: 2026-10-17
access: analysis
revision: 2
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
static-first draft without a prior runtime capture. Revision 2 applies the
[S4 closure assessment](../research/midi-closure-r2.md) after re-checking each
new clause against its listing.

Excluded: arbitrary control-surface scripts, MIDI Learn, other controller
profiles, exact device-bank contents, numerical parameter curves, audio output,
quantization, sample timing, SysEx, MPE, MIDI clock, and the wider behavior of the
targeted mixer/device/transport commands. Mapping a transport button does not
specify the complete transport engine. No controller hardware is assumed.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Observed text of a shipped document (D1–D7); documentation, not an observed run |
| S | Static derivation from shipped bytecode (S1–S3, E1–E9), conditional on host initialization and MIDI delivery; not executed |
| S-cond | Static Python handler logic whose observable effect passes through a named native property; open until traced or probed |
| N / R | Unknown: needs native tracing (N) or a runtime probe (R); PRB IDs refer to the [S4 probe batch](../research/midi-closure-r2.md#phase-4-probe-batch) |

Only D and S clauses can enter a release. S-cond, N and R clauses have no
expected output and block release of the affected behavior.

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
`MixerButtonsToggle: False`. These are observed template values. REQ-003,
REQ-005, REQ-011 and REQ-013 state the result of omitting a key; only an
omitted `MixerButtonsToggle` differs from its template value. See appendix D1–D2.

The interface has 103 ordinary CC number keys (28 in `DeviceControls`, 61 in
`MixerControls`, 14 in `TransportControls`), 16 pad note keys and 16 pad
channel keys in `Globals`, 27 per-control channel keys, `GlobalChannel`, four
map-mode keys and two Boolean keys (E1).

## Requirements

### REQ-MIDI-USER-001 — profile discovery

- **D.** A letter-prefixed directory in `User Remote Scripts` containing the
  exact configuration filename is offered as a Control Surface name (D1).
- **S.** None observable. The script derives an internal name from the folder
  (E1 L30–47); its display is not established.
- **Unknown.** Character encoding, non-ASCII letters, invalid names, enumeration
  order and refresh timing. N: native enumeration; only string adjacency is
  observed (E8). R: PRB-S4-01, PRB-S4-02.

### REQ-MIDI-USER-002 — control numbers

- **D.** `Pad1Note`–`Pad16Note` address notes; every other number key addresses
  a CC. Numbers are 0–127 (D2).
- **S.** An ordinary CC key enables its assignment for an integer 0–127. A
  missing key, `-1`, another out-of-range integer, or an ordinary conversion
  failure disables it (E1 L56–66, bound L96; E2 L24–25). Integer text follows
  the embedded interpreter's `int()` rules, inferred CPython 3.11.6 (E8):
  `+20` and `0021` are accepted, `1_0` reads as 10 (an underscore is accepted
  only singly between two digits), and `0x14`, `20.0`, empty
  values and trailing comment text are conversion failures (E7). A pad note
  integer 0–127 enables the pad; another integer omits it (E1 L197–200).
  Exception found in the midi-config-v2 review (RV2-01): integer text longer
  than the interpreter's conversion length limit raises out of the pad fields
  instead of disabling the pad. midi-config-v2 excludes pad note text over 640
  characters, and pad channel text over 640 characters when the note is enabled.
- **Unknown.** A noninteger pad note, and interpolation errors such as `%` or
  `%(missing)s` on either path, raise out of profile construction, which has
  no exception handler (E1). The host outcome is N and R: PRB-S4-03.

### REQ-MIDI-USER-003 — channels

- **D.** `-1` selects `GlobalChannel`; a valid explicit channel selects that
  channel; channels are 0–15 (D2).
- **S.** The effective global channel is a valid `GlobalChannel`, otherwise 0,
  including a missing key or missing `[Globals]` section (E1 L125, L182–184;
  E2 L83–95). Per-control channel keys exist only for `EncoderChannel1`–`16`,
  `Slider1`–`8Channel`, `MasterSliderChannel`, `CueSliderChannel` and
  `CrossfaderSliderChannel`. A valid value selects that channel, anything else
  the effective global channel (E1 L148–155, L227–242, L285–291; E2 L147–155,
  L239–249, L368–378). Every button, send knob and transport key uses the
  effective global channel, and invented channel keys are never read (E2
  L136–137, L274–283, L313–316, L399–405). A pad channel is read only after a
  valid note. Missing or `-1` takes `GlobalChannel` only when it is valid,
  otherwise the pad is omitted. Any other integer outside 0–15 omits the pad.
  Pads never fall back to channel 0 (E1 L201–209).
- **Unknown.** A noninteger pad channel after a valid note raises: PRB-S4-03.

### REQ-MIDI-USER-004 — non-mixer button values

- **D.** Non-mixer buttons are expected to send a positive value on press and 0
  on release (D2).
- **S-cond (open).** Transport toggles invert their named Boolean on a nonzero
  value and ignore zero. Play and Stop set playing true and false. PunchIn/Out
  and NudgeUp/Down are true while positive and false on zero; repeated positive
  values retrigger toggles. Rewind/fast-forward hold starts on positive and
  stops on zero (S3). Each effect passes through a native Song property.
- **Unknown.** Exact seek timing, nudge magnitude and tap estimation: PRB-S4-06,
  PRB-S4-07. Alternate Note messages remain outside the CC contract.

### REQ-MIDI-USER-005 — map modes

- **D.** Ten mode spellings, including the literal `Compliment` spelling (D2).
- **S.** The tokens `Absolute`, `Absolute14Bit`, `LinearSignedBit`,
  `LinearSignedBit2`, `LinearTwoCompliment`, `LinearBinaryOffset`,
  `AccelSignedBit`, `AccelSignedBit2`, `AccelTwoCompliment` and
  `AccelBinaryOffset` match exactly and case-sensitively (E6 elements_base
  L20–47; E1 L17). A missing key gives `Absolute` (E1 L51–53). Scope:
  `EncoderMapMode` for encoders; `VolumeMapMode` for track, master and cue
  volume; `SendsMapMode` for both send knobs; `CrossfaderMapMode` for the
  crossfader (E1 L170–171, L245–252; E2 L132–134, L140, L188–212, L289–293).
  `Absolute14Bit` becomes `Absolute` for any continuous control whose CC number
  exceeds 95 (E6 EncoderElement L27, L53–56).
- **Unknown.** A present token outside the ten reaches the host as a plain
  string instead of a mode value (E1 L52); no Absolute fallback is promised.
  N and R: PRB-S4-04. Numeric transforms, 14-bit pairing, acceleration and
  pickup: PRB-S4-05.

### REQ-MIDI-USER-006 — drum pads

- **D.** Assigned notes play visible pads 1–4 in the top row through 13–16 in
  the bottom row (D3).
- **S.** Pad keys are read only from `[Globals]` (E1 L182, L197). Pad *n*
  yields column (n−1) mod 4 and row (n−1) div 4 with its note and channel,
  passed to the host as a translation table (E1 L210–220; E2 L97–98).
- **Unknown.** N: the host pad translation. R: PRB-S4-08. Note-off handling,
  velocity transformation, scroll updates and collisions.

### REQ-MIDI-USER-007 — device encoders

- **D.** Encoder1–16 control up to 16 parameters of the selected device; 8 or
  fewer select one bank of 8 and 9 or more select two banks (D4).
- **S.** Valid encoders are compacted in slot order, skipping disabled slots
  (E2 L366–388). The span counts valid assignments: more than 8 gives two banks,
  regardless of slot numbers (E3 ButtonMatrixElement L33–43; E4 user
  DeviceComponent L15–16).
- **Unknown.** Which parameter occupies each position and the effect of fewer
  available parameters. The bank tables that
  `_Framework/DeviceComponent` imports from `_Generic/Devices` are a static lead
  that has not been traced; PRB-S4-09 is deferred until it is.

### REQ-MIDI-USER-008 — device banks and buttons

- **D.** Bank buttons select banks; Next/Prev change bank; `OnOffButton`
  toggles Device Activator; `LockButton` locks the other device controls (D4).
- **S.** Valid `Bank1Button`–`Bank8Button` are compacted in slot order, so a
  lone `Bank8Button` is the first selector, refining a literal reading of its
  label (E2 L339–363). Named targets: E1 L159–168, E2 L321–336. Every device
  button is momentary on the effective global channel (E2 L312–316).
- **S-cond (open).** Selector *k* selects bank *k* only when the device has at
  least *k* banks; re-pressing the current bank shows a
  "*device* Bank: *name*" status message (E4 framework DeviceComponent
  L394–408). Next alone cycles by one bank with wrap. With Previous configured,
  Next/Previous step by the span without wrapping (E4 user DeviceComponent
  L20–65). OnOff inverts the activator value and Lock calls the host lock on a
  nonzero value (E4 framework DeviceComponent L371–388).
- **Unknown.** Bank count and lock semantics are N. R: PRB-S4-10. Lock release,
  deletion of a locked device and simultaneous messages.

### REQ-MIDI-USER-009 — mixer strips

- **D.** Volume sliders, Send1/Send2 knobs and mute/solo/select/arm buttons
  target the named state of a bank of 8 tracks; mixer Next/Prev change that bank
  (D5).
- **S.** Target association for strips 1–8 and mixer bank buttons (E1 L272–317;
  E2 L169–302). Send knobs are compacted per strip and connected by position:
  the first valid knob reaches the first send (E2 L272–302; E3
  ChannelStripComponent L299–319, ButtonMatrixElement L79–82). `Send2Knob`*N*
  therefore targets Send B only when `Send1Knob`*N* is valid; alone, it reaches
  Send A. This refines D5 and is new in revision 2 and unreviewed.
- **S-cond (open).** Arming a track that changes from unarmed to armed also
  selects it when the host's instrument selection succeeds (E5 L12–27).
- **Unknown.** Track ordering, return/group/hidden tracks, missing sends,
  partial banks and bank limits: PRB-S4-11. The cheaper static step is
  `_Framework/MixerComponent` track ordering.

### REQ-MIDI-USER-010 — master, cue and crossfader

- **D.** `MasterVolumeSlider`, `CueVolumeSlider` and `CrossfaderSlider` target
  master volume, cue/preview volume and the crossfader (D6).
- **S.** Released v1 clauses, plus mode scope: `VolumeMapMode` covers master and
  cue (E2 L140, L188–203); `CrossfaderMapMode` covers the crossfader (E2
  L205–212). The crossfader control disables takeover (E2 L216); the effect is N.
- **Unknown.** Scaling, clipping, smoothing and values for absent targets:
  PRB-S4-05.

### REQ-MIDI-USER-011 — mixer buttons and feedback

- **D.** `MixerButtonsToggle` declares toggle (True) or momentary (False)
  buttons. With `InvertMuteButtonFeedback: True`, feedback is on for an unmuted
  track (D5–D6).
- **S.** A present false Boolean gives momentary; true or absent gives toggle.
  This covers strip buttons and the mixer bank buttons (E1 L255–258; E2
  L129–137, L158–166, L218–224). Boolean spellings are case-insensitive
  `1/yes/true/on` and `0/no/false/off` (E7 L608).
- **S-cond (open).** Momentary buttons act on nonzero values; toggles act on
  every value, so zero is not a forced-off state (E3 ChannelStripComponent
  L353–370). Mute inverts on each actionable input; a strip whose track is the
  master track ignores mute input (L368); unarmable tracks ignore arm (L415).
  An absent `InvertMuteButtonFeedback` is True (E1 L127–142, L260–262).
  Feedback is lit only for regular and return tracks, when mute differs from
  the invert setting (L463–475).
- **Unknown.** Feedback bytes and startup feedback: PRB-S4-13. Solo/arm
  exclusivity: PRB-S4-12. An invalid Boolean raises: PRB-S4-03.

### REQ-MIDI-USER-012 — transport buttons

- **D.** Stop, Play, Rec, SessionRec, Over, Metro, Loop, Rwd, Ffwd, PunchIn,
  PunchOut, NudgeUp, NudgeDown and TapTempo target their named transport
  functions (D7).
- **S.** These 14 `…Button` keys are the only transport keys (E2 L37–55; E1
  L175–178). The key is `FfwdButton`; the adjacent comment's `FwdButton` is not
  a key. All transport buttons are momentary on the effective global channel,
  because the release-suppression key can never be set (E2 L398–420, L409).
- **S-cond (open).** Value handling as in REQ-MIDI-USER-004.
- **Unknown.** Seek rate, nudge magnitude, tempo estimation, release and
  interaction timing: PRB-S4-06, PRB-S4-07.

### REQ-MIDI-USER-013 — configuration syntax

- **D.** The interface maps the supported features; it does not define new
  commands or edit device parameter banks (D1).
- **S.** Option names are case-insensitive; section names are exact (E7
  L890–904; E1 L146, L175, L182, L223, L276, L283). `=` and `:` delimit;
  full-line `#`/`;` lines are comments; text after a value stays in the value;
  keys and values are stripped of leading and trailing whitespace as the reader
  defines it, which includes tabs and some other ASCII control characters;
  midi-config-v2 covers spaces only and excludes the rest (RV2-02). Empty
  values are conversion failures. A `[DEFAULT]` key
  counts as present in each named section that exists and does not define it
  (E7 L611–616, L893–904). Unknown keys and keys in another section are never
  read. Duplicate sections, duplicate normalized options, pre-section text and
  invalid Booleans raise out of profile construction.
- **Unknown.** Host diagnostics and recovery: PRB-S4-03. File encoding and
  non-ASCII input: PRB-S4-16.

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
edits require restart/reselection is unknown (PRB-S4-14). Undo/redo membership
and interaction with automation recording are unknown and outside known
expectations in this revision.

## Errors, cancellation and teardown

Ordinary numeric CC fields use the derived disable/fallback rules above only
for missing fields, out-of-range integers and ordinary integer-conversion
failures. Configuration interpolation can fail before numeric conversion; it
is outside this safe-fallback contract. Pad integer parsing, Boolean parsing,
duplicate sections/options and pre-section content raise out of profile
construction, which has no handler (E1). Host-visible error presentation and
continued profile availability remain unknown (PRB-S4-03). No safe unknown-mode
fallback is promised (PRB-S4-04).

No asynchronous configuration operation or cancel affordance is established.
Cancellation coverage therefore means changing surface selection while a
momentary control is held; the resulting state is unknown. Teardown covers
MIDI-port disconnect, profile deselection and exit with a held note/button.
Release cleanup, stuck-note prevention, output feedback and reconnect behavior
are unknown (PRB-S4-15). These are applicable gaps, not omitted passing cases.

## Acceptance cases

Three case sets exist; none has run against a reference or candidate.

| Set | Cases | Status |
| --- | --- | --- |
| Revision 1 matrix `acceptance-cases.json` (MIDI-USER-001–046) | 46 groups over all requirements, including unresolved ones | Retained in the macOS `midi-user-mapping-v1` evidence tree, which is absent on this host |
| [S4 draft cases](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/draft-cases-v2.json) (S4-MIDI-001–055) | 55 configuration-interpretation cases | Analyst draft. S4-MIDI-030 expected Send B for a lone `Send2Knob1`, which fails the REQ-009 check; corrected in the staged candidate |
| [Staged midi-config-v2](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v2/README.md) (MIDI-CONFIG-001–109) | 54 v1 cases restated plus 55 new | Unreviewed candidate; see the [v2 plan](midi-config-v2-handoff-plan.md) |

Logical comparisons use exact integer/channel/target identifiers or exact Boolean
state where an expected state is supported. Numerical parameter curves, bank
contents and feedback bytes have no oracle yet and must not be graded as passes.
An unknown expected result has comparator `unresolved`, never an invented
golden output. Documentation provenance is not an observed reference result.

## Open questions

See the canonical [question register](../questions.md): Q-008 covers parser/host
error recovery and unknown-mode outcomes; Q-009 covers numeric transforms,
takeover, timing and feedback; Q-010 covers discovery/reload, disconnect,
persistence, undo and the send-position refinement. The 16 probe records name
the remaining runtime questions. Prefer a focused static trace for material
gaps; use a bounded runtime probe when static evidence cannot resolve the
question or the probe is clearly cheaper, under ADR 0002. Concrete expected
outcomes absent from this draft remain unknown and block release of the
affected behavior.

## Analyst evidence appendix

This section and its restricted links are analysis-only and must be removed or
reviewed when preparing a self-contained handoff. The retained source identity
is [MIDI mapping sources](../research/sources/midi-user-mapping-12.4.3.md), source ID
`SRC-MIDI-USER-MAPPING-1243`. The [research synthesis](../research/midi-user-mapping.md)
owns the revision 1 findings; the [closure assessment](../research/midi-closure-r2.md)
owns the S4 classification.

| Local evidence label | Exact source locator in Ableton Live 12 Suite 12.4.3 | What is observed / limitation |
| --- | --- | --- |
| D1 | `_Tools/InstantMappings-HowTo.txt` lines 8–22 | Documented scope, name and placement convention; no observed loader run. |
| D2 | `_Tools/UserConfiguration.txt` lines 5–55, 68–99, 115–147 | Documented ranges, fallback, message types and modes; template bytes do not prove parser defaults or wire behavior. |
| D3 | `_Tools/UserConfiguration.txt` lines 59–99 | Documented pad geometry and input keys; note lifetime untraced. |
| D4 | `_Tools/UserConfiguration.txt` lines 103–171 | Documented device targets, bank threshold and lock; no parameter-bank fixture or boundary run. |
| D5 | `_Tools/UserConfiguration.txt` lines 175–267 | Documented mixer targets and mute feedback meaning; no feedback packet capture. |
| D6 | `_Tools/UserConfiguration.txt` lines 269–292 | Documented master/cue/crossfader targets, mode scope and mixer toggle setting. |
| D7 | `_Tools/UserConfiguration.txt` lines 296–340 | Documented transport targets; Fwd/Ffwd comment/key discrepancy retained. |

Both documents originate in `Contents/App-Resources/MIDI Remote Scripts/` of the
pinned app. Their SHA-256 values
(`52ec71be0a51fd89a0d1cebebc9a3f7c2a2cb62f6a55d25e7a4be3b3228322a4` and
`6d710bba5610cba5c17213fc46472fb87843857fcba8d28f6f838d69aa1554ef`) were
recomputed on this host and match ([S4 hashes](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/hashes.json)).
The revision 1 copies, `source-manifest.json`, xdis listings, `parser-findings.json`
(PARSE-01–10), `bytecode-mapping-findings.json` (BC-01–10), the matrix capture
and review JSON live in `analysis/ableton-live-12.4.3/midi-user-mapping-v1/`,
which is absent on this host until roadmap gate G0.2.

Revision 1 static evidence (xdis, CPython 3.11 bytecode, not executed); every
locator reappears in the S4 listings:

- S1: `_UserScript/__init__` `parse_int` lines 56–66, offsets 2–264;
  `create_instance` lines 96–97, offsets 180–266, pads lines 195–209 offsets
  1088–1432 and Boolean reads offsets 2098–2286; `parse_map_mode` offsets 46–164;
  `elements_base` `MapMode` lines 20–48.
- S2: `_Generic/GenericScript` `_init_device_component` lines 341–388, offsets
  348–1322; `_UserScript/DeviceComponent` `set_parameter_controls` line 16,
  offsets 4–64; `_Framework/DeviceComponent` `_bank_value` lines 397–402, offsets
  134–308.
- S3: `_Framework/TransportComponent` initialization lines 63–81 and class line
  28; `_Framework/ToggleComponent` `_on_button_value` lines 93–100, offsets 2–244.
  Host property effects and scheduler timing are unmeasured.

Revision 2 static evidence, re-decoded with CPython 3.11.13 `dis` via
`marshal.loads` only ([decoder](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/decode.py),
[manifest](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/manifest.json)).
Each module digest is in the S4 hashes; its match with revision 1 is unknown
until G0.2. `L` numbers are source-line metadata in the listings.

| Label | Listing | Locators used above |
| --- | --- | --- |
| E1 | [_UserScript/__init__](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/_UserScript/__init__.dis.txt) | dictcomp L17; name L30–47; `parse_map_mode` L50–53; `parse_int` L56–66; `create_instance` L75–339: no exception table; key reads L96–317 |
| E2 | [_Generic/GenericScript](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/_Generic/GenericScript.dis.txt) | validity L20–25; transport keys L37–55; global channel L83–95; mixer L121–302; device L304–396; transport L398–426 |
| E3 | [ChannelStripComponent](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/_Framework/ChannelStripComponent.dis.txt), [ButtonMatrixElement](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/_Framework/ButtonMatrixElement.dis.txt) | send connection L299–319; select/mute L353–370; mute feedback L463–475; matrix rows L33–43; iteration L79–82 |
| E4 | [user DeviceComponent](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/_UserScript/DeviceComponent.dis.txt), [framework DeviceComponent](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/_Framework/DeviceComponent.dis.txt) | span L15–18; navigation L20–65; lock and on/off L371–388; bank buttons L394–408 |
| E5 | [SelectChanStripComponent](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/_Generic/SelectChanStripComponent.dis.txt) | arm-select L12–27 |
| E6 | [EncoderElement](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/_Framework/EncoderElement.dis.txt), [elements_base](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/ableton/v3/control_surface/elements_base.dis.txt) | 14-bit limit L27, L53–56; `MapMode` L20–47 |
| E7 | [configparser](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/configparser.dis.txt), [equivalence](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/configparser-equivalence.json) | `BOOLEAN_STATES` L608; defaults L611–616; `optionxform`/`has_option` L890–904. Shipped module equals CPython 3.11.13 except `_read`, which differs only on a raising path |
| E8 | [native anchors](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/native-anchors.json) | `3.11.6` beside the interpreter version format (inferred version); discovery strings; adjacency only, not call edges |
| E9 | [S4 draft cases](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/draft-cases-v2.json) `rules` | Rule IDs R-CC … R-INT map each draft case to the locators above |

The `Layer` wiring from control to component setter is assumed for every target
association, as in revision 1; that module was not decoded. Requirements
translate these documented contracts into candidate observable obligations. No
generated pseudocode is an implementation input.

## Revision and handoff

Revision 1, 2026-10-09: first bounded draft and unexecuted case matrix. An
initial independent scope review (`scope-review.json`) requested two
corrections: qualify numeric fallback to exclude interpolation errors
(SCOPE-01), and supply live assignments in channel/default cases (SCOPE-02).
Both were addressed. The scope recheck and a separate quality review approved
the bounded analyst draft, not a handoff or compatibility claim; their JSON
records are in the absent revision 1 tree. Cases 041–046 covered the omitted
mixer-toggle default, INI lexical rules, valid-CC invalid-channel, unknown
interpolation and paired banking. The subsequent
[finite configuration handoff](../../handoff/midi-config-v1/README.md) approves
only selected clauses of REQ-MIDI-USER-002/003/010/013 for master, cue and
crossfader assignments, with 54 independently authored cases. Post-review
editorial changes recorded these dispositions and aligned the runtime escalation
wording with ADR 0002; requirements and cases were unchanged.

Revision 2, 2026-10-17: applied the S4 closure assessment. Each requirement is
split into D, S, S-cond and unknown clauses with E1–E9 locators and PRB IDs. New
static clauses: the effective global channel and per-control channel key list;
pad channel rules with a missing or invalid `GlobalChannel`; integer text forms;
map-mode scope and absent-key default; encoder and bank-button compaction; mixer
bank buttons following `MixerButtonsToggle`; always-momentary device and
transport buttons; the 14 transport keys; and the lexical rules including
`[DEFAULT]`. New S-cond clauses: the
absent-feedback default, feedback eligibility, crossfader takeover, arm-select
and the current-bank message. The send-position refinement in REQ-009 came
from re-checking the closure's draft case S4-MIDI-030, which this revision
does not adopt. A [midi-config-v2 candidate](midi-config-v2-handoff-plan.md) is
staged for separate review. midi-config-v1 remains the only released contract.
No application code or original-versus-candidate comparison has run.
