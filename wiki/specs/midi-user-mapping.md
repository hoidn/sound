---
id: SPEC-MIDI-USER-MAPPING
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 3
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
new clause against its listing. Revision 3 adds the value transforms of the
[native transform packet](../research/midi-transforms-native.md), each clause
re-checked against its kept disassembly or extracted constants.

Excluded: arbitrary control-surface scripts, MIDI Learn, other controller
profiles, exact device-bank contents, parameter display curves, audio output,
quantization other than stepped-parameter rounding (REQ-MIDI-USER-005), sample
timing, SysEx, MPE, MIDI clock, and the wider behavior of the
targeted mixer/device/transport commands. Mapping a transport button does not
specify the complete transport engine. No controller hardware is assumed.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Observed text of a shipped document (D1–D7); documentation, not an observed run |
| S | Static derivation from shipped bytecode (S1–S3, E1–E9) or from native disassembly and image constants of the pinned executable (E10–E14), conditional on host initialization and MIDI delivery; not executed |
| S-cond | Static handler logic whose observable effect passes through a named native property, an inferred native link or an untraced setting; open until traced or probed |
| N / R | Unknown: needs native tracing (N) or a runtime probe (R); PRB-S4 IDs refer to the [S4 probe batch](../research/midi-closure-r2.md#phase-4-probe-batch), PRB-N7 IDs to the [N7 probe records](../research/midi-transforms-native.md#probe-records) |

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

Value cases (REQ-MIDI-USER-005 and 010) also need the takeover preference set
and recorded explicitly, because its default is unknown. They need a target
parameter of known kind, range, stepped state and current value, and a MIDI
input opened before the case with no other message on the case's controllers.

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
- **S. Value mapping (revision 3).** Each assigned continuous control (encoder,
  track volume, send knob, master volume, cue volume or crossfader) maps its
  effective channel and CC number, with its map mode, to its target parameter.
  The range is the parameter's reported minimum and maximum (min, max), except
  for on/off parameters below. Parameters are of four kinds: continuous, on/off,
  enumerated and other. A parameter is *stepped* when it reports quantized. The
  rules below give a target value per message, applied once, with no smoothing
  before it is set (E10, E13).
- **S. Absolute.** Data value v gives min + (max − min) × v/127. A stepped
  parameter takes the nearest integer, with halves rounded away from zero (E12).
- **S. Absolute14Bit.** CC n carries the most significant and CC n + 32 the
  least significant 7 bits, on the same channel. A received half is held until
  the other half arrives, in either order. A newer half replaces a held half of
  the same kind; a lone half changes nothing. When both halves are held, the
  target value is min + (max − min) × (128 × MSB + LSB)/16383, rounded as for
  Absolute, and both halves are discarded (E11).
- **S. Relative.** In the eight relative modes, data value v decodes to a
  signed step d by the table below. A parameter that is not stepped becomes
  clamp(current + (max − min) × d/256, min, max). A stepped parameter moves one
  unit per message, up when d > 0 and down otherwise, so a decoded 0 moves it
  down. The result is clamped to [min, max] and rounded as for Absolute (E12, E13).

  | Mode | d for data value v |
  | --- | --- |
  | `LinearSignedBit` | v ≤ 64: +v; v ≥ 65: −(v − 64) |
  | `LinearSignedBit2` | v ≤ 64: −v; v ≥ 65: +(v − 64) |
  | `LinearTwoCompliment` | v ≤ 64: +v; v ≥ 65: v − 128 |
  | `LinearBinaryOffset` | v − 64 |
  | `AccelSignedBit` | v ≤ 64: +A(v); v ≥ 65: −A(v − 64) |
  | `AccelSignedBit2` | v ≤ 64: −B(v); v ≥ 65: +B(v − 64) |
  | `AccelTwoCompliment` | v ≤ 65: +B(v); v ≥ 66: −B(128 − v) |
  | `AccelBinaryOffset` | v ≥ 64: +B(v − 64); v ≤ 63: −B(64 − v) |

  A(k) is 1, 2, 3, 4, 5, 8, 10, 20, 50 for k = 1…9 and 20 for any other k,
  including 0. B(k) is 1, 2, 3, 4, 5, 8, 20, 50 for k = 1…8 and 50 for any
  other k, including 0. Hence `AccelSignedBit` 10–64 gives +20,
  `AccelBinaryOffset` 64 gives +50 and `AccelTwoCompliment` 65 gives +50.
- **S. Takeover exemptions.** Takeover can act only on absolute target values
  (`Absolute` messages and completed `Absolute14Bit` pairs) of continuous
  parameters. Relative messages, the other parameter kinds and the crossfader
  are never subject to it, whatever the takeover preference; their target value
  applies directly. With the takeover preference set to None, every absolute
  target value applies. The correspondence of the label None to this behavior
  is inferred from the order of the preference's three settings (E10, E14).
- **S-cond. Pick-Up and Value Scaling.** For an absolute target value n subject
  to takeover, let c be the current value clamped to [min, max] and
  w = (max − min)/64. Let p be the target value that the previous data value
  received on the same input, channel and controller number would have produced.
  For a 14-bit pair, use the previous data values on both controller numbers.
  Any earlier message counts, whether or not it was mapped.
  - An `Absolute` message with no previous data value on its controller since
    the input opened keeps c.
  - When |p − c| ≤ (max − min)/256, n applies.
  - Otherwise, Pick-Up applies n only when c lies in
    [min(n, p) − w, max(n, p) + w]; else it keeps c.
  - Otherwise, Value Scaling applies n when |n − c| ≤ w and keeps c when p = n.
    Else it moves c by the travelled fraction of the remaining distance:
    c + (max − c)(n − p)/(max − p) when n > p, and c − (c − min)(p − n)/(p − min)
    when n < p.
  - The result is clamped to [min, max]. These tolerances also apply to 14-bit
    pairs (E14). Open: the label correspondence and the reset of previous
    values other than at input open (PRB-N7-03).
- **S-cond. On/off parameters.** An absolute data value v turns an on/off
  parameter on exactly when v lies between the parameter's stored MIDI CC on/off
  thresholds, minimum and maximum inclusive. The result is inverted when the
  minimum exceeds the maximum. A completed 14-bit pair is compared as
  (128 × MSB + LSB)/129. A relative message turns the parameter on when d > 0
  and off otherwise. Neither takeover nor rounding applies (E13). Open: that the
  bounds are the stored thresholds is inferred, and an unexplained host check
  can substitute the parameter's ordinary range (PRB-N7-04).
- **Unknown.** A present token outside the ten reaches the host as a plain
  string instead of a mode value (E1 L52); no Absolute fallback is promised.
  N and R: PRB-S4-04. Also unknown:
  - the takeover preference default (PRB-N7-03);
  - delivery ordering, coalescing and deferred application of back-to-back
    messages (PRB-N7-05);
  - displayed values and any processing after a value is set (PRB-N7-01);
  - the first 14-bit pair after the input opens, or a pair with a half lacking
    a previous value, under Pick-Up or Value Scaling (PRB-N7-01, PRB-N7-03);
  - which parameters belong to each kind, and which are stepped without
    reporting quantized (PRB-N7-04);
  - several assignments on one channel and controller number. Each appears to
    receive every message, but this is inferred.

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
  L205–212). Values follow REQ-MIDI-USER-005. The crossfader is the only
  continuous control with takeover disabled (E2 L216), so its absolute values
  apply whatever the takeover preference; see the
  [takeover exemptions](#req-midi-user-005--map-modes) (E10, E13). Master and
  cue volume are subject to takeover like other continuous controls.
- **Unknown.** Reported ranges and kinds of these three parameters, displayed
  values, processing after a value is set and values for absent targets:
  PRB-N7-01, which refines PRB-S4-05.

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
values in these cases are integer bytes in 0–127. Value cases compare a
parameter value on its own scale within an absolute tolerance of 1e-6. No
wall-clock, musical-clock, latency, jitter or other numerical tolerance is
established. Do not use an arbitrary timeout as evidence of a no-action result.
A later execution harness must establish a bounded completion/observation
method before claiming pass.

Relevant state includes selected and locked device, device bank, mixer bank,
track states, transport states, the takeover preference and held 14-bit halves.
It also includes, per input, the last data value received on each channel and
controller number, which is empty when the input opens. Documented state
changes are confined to the requirements above. Selection retention,
simultaneous-message ordering, delivery coalescing (PRB-N7-05), duplicate
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

Four case sets exist; none has run against a reference or candidate.

| Set | Cases | Status |
| --- | --- | --- |
| Revision 1 matrix `acceptance-cases.json` (MIDI-USER-001–046) | 46 groups over all requirements, including unresolved ones | Retained in the macOS `midi-user-mapping-v1` evidence tree, which is absent on this host |
| [S4 draft cases](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/draft-cases-v2.json) (S4-MIDI-001–055) | 55 configuration-interpretation cases | Analyst draft. S4-MIDI-030 expected Send B for a lone `Send2Knob1`, which fails the REQ-009 check; corrected in the staged candidate |
| [Staged midi-config-v2](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v2/README.md) (MIDI-CONFIG-001–109) | 54 v1 cases restated plus 55 new | Released on 2026-10-17 as [midi-config-v2](../../handoff/midi-config-v2/README.md), approved with narrowing; see the [v2 plan](midi-config-v2-handoff-plan.md) |
| [N7 transform cases](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/out/acceptance-cases.json) (MT-01–MT-23) | 23 value sequences for REQ-005 and REQ-010 | Static derivations, listed below |

Logical comparisons use exact integer/channel/target identifiers or exact Boolean
state where an expected state is supported. Value cases compare the parameter
value after each message within 1e-6. Display curves, bank contents and
feedback bytes have no oracle yet and must not be graded as passes.
An unknown expected result has comparator `unresolved`, never an invented
golden output. Documentation provenance is not an observed reference result.

### Value transform cases MT-01 to MT-23

These cases test REQ-MIDI-USER-005; MT-22 also tests REQ-MIDI-USER-010. Unless a
row says otherwise, the assignment is CC 20 on channel 0, sent as `B0 14 vv`.
For `Absolute14Bit` the least significant half is CC 52 (`B0 34 vv`), written
L:vv. The target is a continuous parameter, not stepped, with min 0, max 1 and
current value 0.5. Nothing has been received on CC 20 or CC 52 since the input
opened. Data bytes are hexadecimal. Relative cases MT-06 to MT-14, MT-16 and
MT-23 hold under any takeover setting. MT-22 assumes the crossfader reports
the range 0–1; for another range its values are min + (max − min) × v/127.

S rows are static expected outputs. S-cond rows give static predictions, not
expected outputs; their comparator stays `unresolved` until the named probe
has run. Rows with None depend on the inferred None label (REQ-MIDI-USER-005,
takeover exemptions). Reference measurements: PRB-N7-01 (MT-01–05), PRB-N7-02
(MT-06–14), PRB-N7-03 (MT-19–23), PRB-N7-04 (MT-15–18) and PRB-N7-05
(ordering). None has run.

| Case  | Label  | Map mode and condition                                              | Data bytes              | Value after each message                                           |
| ----- | ------ | ------------------------------------------------------------------- | ----------------------- | ------------------------------------------------------------------ |
| MT-01 | S      | Absolute; None                                                      | 00 40 7F                | 0, 0.503937, 1                                                     |
| MT-02 | S      | Absolute14Bit; None; MSB first                                      | 64 L:32                 | 0.5, 0.78435                                                       |
| MT-03 | S      | Absolute14Bit; None; LSB first                                      | L:32 64                 | 0.5, 0.78435                                                       |
| MT-04 | S      | Absolute14Bit; None; newer MSB replaces the held one; lone LSB held | 10 64 L:32 L:00         | 0.5, 0.5, 0.78435, 0.78435                                         |
| MT-05 | S      | Absolute14Bit; None; full scale                                     | 7F L:7F 00 L:00         | 0.5, 1, 1, 0                                                       |
| MT-06 | S      | LinearSignedBit                                                     | 01 41 40 7F             | 0.503906, 0.5, 0.75, 0.503906                                      |
| MT-07 | S      | LinearSignedBit2                                                    | 01 41 40                | 0.496094, 0.5, 0.25                                                |
| MT-08 | S      | LinearTwoCompliment                                                 | 01 7F 41 40             | 0.503906, 0.5, 0.253906, 0.503906                                  |
| MT-09 | S      | LinearBinaryOffset                                                  | 41 3F 40 00             | 0.503906, 0.5, 0.5, 0.25                                           |
| MT-10 | S      | AccelSignedBit; 10 falls back to 20                                 | 01 07 09 0A 41 49 00    | 0.503906, 0.542969, 0.738281, 0.816406, 0.8125, 0.617188, 0.695312 |
| MT-11 | S      | AccelSignedBit2                                                     | 01 41 07 47 00          | 0.496094, 0.5, 0.421875, 0.5, 0.304688                             |
| MT-12 | S      | AccelTwoCompliment; 65 counts up                                    | 01 7F 08 41 42 00       | 0.503906, 0.5, 0.695312, 0.890625, 0.695312, 0.890625              |
| MT-13 | S      | AccelBinaryOffset; 64 gives +50                                     | 41 3F 46 39 40          | 0.503906, 0.5, 0.53125, 0.453125, 0.648438                         |
| MT-14 | S      | LinearBinaryOffset; clamping at max and min                         | 7F 7F 7F 00 00 00 00 00 | 0.746094, 0.992188, 1, 0.75, 0.5, 0.25, 0, 0                       |
| MT-15 | S      | Absolute; None; stepped, range 0–3, from 1                          | 15 16 3F 40 7F          | 0, 1, 1, 2, 3                                                      |
| MT-16 | S      | LinearSignedBit; stepped, range 0–3, from 1                         | 05 01 41 46 46 46       | 2, 3, 2, 1, 0, 0                                                   |
| MT-17 | S-cond | Absolute; on/off, thresholds 64–127, from off                       | 3F 40 7F 00             | off, on, on, off                                                   |
| MT-18 | S-cond | LinearSignedBit; on/off as MT-17                                    | 01 41 03                | on, off, on                                                        |
| MT-19 | S-cond | Absolute; Pick-Up                                                   | 0A 0B 0C 3F 46          | 0.5, 0.5, 0.5, 0.496063, 0.551181                                  |
| MT-20 | S-cond | Absolute; Value Scaling                                             | 0A 14 1E                | 0.5, 0.542735, 0.58547                                             |
| MT-21 | S-cond | Absolute; Pick-Up; first message                                    | 64                      | 0.5                                                                |
| MT-22 | S      | Absolute; Pick-Up; crossfader (takeover disabled)                   | 0A 64                   | 0.07874, 0.787402                                                  |
| MT-23 | S      | LinearSignedBit; Pick-Up                                            | 01                      | 0.503906                                                           |

## Open questions

See the canonical [question register](../questions.md): Q-008 covers parser/host
error recovery and unknown-mode outcomes; Q-009 covers the open transform
points (PRB-N7-01 to 05), timing and feedback; Q-010 covers discovery/reload,
disconnect, persistence, undo and the send-position refinement. The 16 S4 and
five N7 probe records name the remaining runtime questions. Prefer a focused static trace for material
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

Revision 3 native evidence is the
[N7 packet](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/notes.md)
([manifest](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/manifest.json)).
It is a static reading of the arm64 slice `Live.arm64`, SHA-256
`3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`, recomputed
on this host on 2026-10-17. Live was not run. Addresses below are in that image.
Dossiers are the kept results `results/n7-0001`–`n7-0004`, printed with
`scripts/dis.py`. "Decompiler only" marks text from `out/corpus-excerpts.jsonl`.
Python locators are the S4 listings above.

| Label | Locator | What was checked for revision 3 / limitation |
| --- | --- | --- |
| E10 | `_Framework/ControlSurface` `_install_mapping` L735–743 (offsets 814–1044); `InputControlElement.__init__` L191 `_needs_takeover = True`, L197 `_mapping_sensitivity = 1.0`; `GenericScript` L216; enum `TControllerMapMode` (`elements_base` L27–47, registration 0x103b4ca90, decompiler only); wrapper 0x103b4d744 (n7-0004); install 0x102593258 (n7-0001); validation 0x1025931ac (n7-0003); receiver init 0x101b7f32c (n7-0003); dispatch 0x101b69248 → 0x101b65b68 (n7-0002) → 0x101b7842c (n7-0004) | Python passes channel, CC, mode, `not needs_takeover()` and sensitivity 1.0; only the crossfader clears takeover within the decoded S4 listings. Install passes Zoom 1.0 and stores avoid at +0x44 and sensitivity at +0x48. The previous-value table is −129.0 filled (0x105849f70, re-read), read as PriorCValue and then overwritten. Every handler on a (channel, CC) list is called. Inferred: the registry 0x101b84798/0x10260535c is the MidiMap handler lookup, and entry+0x30 is the map mode. Reset 0x101b65c1c is decompiler only; its trigger is unknown. Install refusals 0x1026f9488 and MidiMap +0x30 are uninterpreted |
| E11 | 14-bit install 0x1026094e0 (`mov w3,#0x0` at 0x102609548); MSB store 0x101b8028c, LSB store 0x101b802bc, combine 0x101b7fcc0 (all n7-0002); constructor 0x101b7fc28 (decompiler only) | Each store overwrites its own half and prior, then combines when both value slots are not FLT_MAX. Combine computes (MSB<<7 \| LSB)/129.0 (0x10584a8b4, re-read 129.0), passes MapMode 0 and sensitivity 1.0, then resets all four slots to FLT_MAX. With the avoid flag clear, −129 priors give (−1)/129, not the no-prior sentinel, so the first pair is left open |
| E12 | Value function 0x101b76bf0 (n7-0002); decoder 0x101b7b96c (n7-0001); table init 0x101b842cc (n7-0003); divisor 0x1011afc2c (decompiler only: 127.0, or 8191.0 for −2) | Absolute: t = v/127, lo·(1−t)+hi·t by `fmadd`. Relative: (hi−lo)·(1/256)·d·s or ±1 when quantized, then clamp. `frinta` at 0x101b76cd4 rounds when quantized. Decoder branches were checked against the table above. Vectors at 0x106fba2a8 (B, 8 floats from 0x10584a580) and 0x106fba2c0 (A, 8 floats from 0x10584a5a0 plus 50.0 stored at +0x20) were re-read with `scripts/readvm.py` and match `out/native-constants.json` |
| E13 | Details 0x1026fa5c8 → 0x1026fa684 and 0x1024dd61c (n7-0003); apply 0x101b7fde4 (n7-0001); CC receiver 0x101b7f894 (n7-0002); Python `DeviceParameter` getters 0x103afe2cc/3c0/3d0 (decompiler only); [on/off thresholds](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/out/onoff-thresholds.json) | Type is 1 `ATimeableFloat`, 2 `ATimeableBool`, 3 `ATimeableEnum` or 0 for other. Min/Max come from vtable +0x2f0/+0x2f8, or from the +0x388 range object when the Bool flag is set; registry 0x1011aeb80 can clear that flag and is unexplained. Quantized is +0x2e0, or an internal byte equal to 2. Apply, with Zoom ≤ 1: Type 2 absolute uses lower ≤ v ≤ upper XOR (Min > Max), and Type 2 relative uses d·s > 0. Other types use the value function; takeover runs only for MapMode 0/5, Type 1 and prior ≠ FLT_MAX. When 0x1011c0ee8(0x100500) ≠ 0, the fields are posted as `OChangeControllerDataCommand` (timing unknown). Setter 0x101b0d328 was not traced. The receiver blanks the prior when avoid is set and Zoom = 1.0. Quantized relative accumulates ±s and fires at \|acc\| ≥ 1. Shipped sets carry Min 64/Max 127 in 22,059 of 22,303 threshold pairs |
| E14 | Takeover 0x101b7c508 and Pick-Up 0x101b7c344 (n7-0001); preference setter 0x101b83750 (n7-0003); UI entry order 0x1022df424 (decompiler only) | The global mode at 0x106fb2110 has three cases. 0 returns clamp(new). Otherwise a prior equal to −129.0 keeps c, and \|p − c\| ≤ (hi−lo)·0.5/128 applies new. Mode 2 uses w = (hi−lo)·2/128 and proportional scaling. Mode 1 uses the [min(n,p) − w, max(n,p) + w] window and posts a pick-up notification. Inferred: index 0/1/2 = None/Pick-Up/Value Scaling, from the declaration order and the notification. The default was not found |

Case derivation: `scripts/derive_cases.py` (SHA-256
`b7fe6ce1c176a0b5f1a518c499f1661c534977eb7562598b9e034204de88c717`) regenerated
`out/acceptance-cases.json` byte-identically (SHA-256
`bffc375a1aacf278b8dda6426049e70941e0f049c7df4c7b6fdc8b53efe19d27`) on
2026-10-17. It is a float32 model, not an oracle. The revision 3 author
independently recomputed MT-02 to MT-05, MT-10, MT-12, MT-13, MT-16 and MT-19
to MT-22 in exact rational arithmetic from the checks above. All agree within
1e-6. That spot-check script was not retained.

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

Revision 3, 2026-10-17: applied the
[N7 native transform packet](../research/midi-transforms-native.md) after
re-checking each clause against the kept dossier disassembly and the image
constants. REQ-MIDI-USER-005 gains the S clauses value mapping, Absolute,
Absolute14Bit, relative step table and takeover exemptions. It also gains the
S-cond clauses Pick-Up and Value Scaling, and on/off parameters, with evidence
labels E10–E14. Its "numeric transforms" unknown is replaced by explicit open
items, PRB-N7-01 to 05. REQ-MIDI-USER-010 now points at the crossfader takeover
opt-out. The timing/state section adds the per-input previous-value record and
the 1e-6 value tolerance. Acceptance cases MT-01 to MT-23 were added: 18 S
and 5 S-cond. This revision departs from the packet's proposal in four ways.
Takeover None and the exemptions are S, with the None label stated as an
inference; the packet's takeover clause, including None, was S-cond. The rule that a message
without a previous value keeps the value is limited to `Absolute`, because 14-bit
priors combine to a value that is not the no-prior marker. Transforms are stated
for enumerated and other parameter kinds, whose path differs only by having no
takeover. MT-15/16 are labelled S, with parameter selection left to PRB-N7-04.
The [midi-config-v2](../../handoff/midi-config-v2/README.md) release of
2026-10-17 is recorded in the case-set table. Requirements released there are
unchanged. No application code or original-versus-candidate comparison has run.

Released 2026-10-18: [midi-config-v3](../../handoff/midi-config-v3/README.md), 127 cases, approved by a separate review agent (partial REQ-002/003/005–013 only; 001 and 004 unreleased; MT-17 to 21 out). The review findings to apply in the next revision are on the [handoff plan](midi-config-v3-handoff-plan.md#review-outcome). This revision's text is unchanged.
