---
id: SPEC-MIDI-USER-MAPPING
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 6
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
shipped documentation, labeled static derivations and, from revision 5,
extracted execution of original x86_64 functions (X). None of them rests on a
run of the application. No compatibility result or implementation is claimed.
This revision remains a draft until evidence contradictions, required unknowns
and separate review are resolved. [ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits this
static-first draft without a prior runtime capture. Revision 2 applies the
[S4 closure assessment](../research/midi-closure-r2.md) after re-checking each
new clause against its listing. Revision 3 adds the value transforms of the
[native transform packet](../research/midi-transforms-native.md), each clause
re-checked against its kept disassembly or extracted constants. Revision 4
applies the midi-config-v3 review findings. Under
[ADR 0003](../decisions/adr-0003-no-reference-execution.md) no reference run of
the application will happen, so a clause or case that waited on a probe stays
unknown or ungraded. Revision 5 settles the takeover clauses, takeover with a
reversed range, the first 14-bit pair and the value tolerance by
[extracted execution](../research/midi-transforms-native.md#extracted-execution-results-x2-2026-10-18)
and a static trace of the takeover preference.

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
| S | Static derivation from shipped bytecode (S1–S3, E1–E9) or from native disassembly and image constants of the pinned executable (E10–E15), conditional on host initialization and MIDI delivery; not executed |
| X | Extracted execution of the original x86_64 functions on stated inputs, with the harness stubs listed in E16 ([ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code)). It shows what that code computes, not how the application reaches it; arm64 equivalence rests on the static slice comparison in E16 |
| S-cond | Static handler logic whose observable effect passes through a named native property, an inferred native link or an untraced setting; open until traced, because no reference observation is available (ADR 0003) |
| N / R | Unknown: needs native tracing (N) or needed a runtime probe (R). No probe will run (ADR 0003), so an R item stays unknown unless static work or extracted execution of the original x86_64 code settles it. PRB-S4 IDs refer to the [S4 probe batch](../research/midi-closure-r2.md#phase-4-probe-batch), PRB-N7 IDs to the [N7 probe records](../research/midi-transforms-native.md#probe-records); each records what a probe would have observed |

Only D, S and X clauses can enter a release. S-cond, N and R clauses have no
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
  for on/off parameters below. The reported maximum can be below the minimum, a
  *reversed range*. The rules below hold for either order: clamping is to the
  closed interval between min and max, and toward max is numerically down for a
  reversed range (revision 4, E12; broader than midi-config-v3, which requires
  min < max). Parameters are of four kinds: continuous, on/off,
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
  current + (max − min) × d/256, clamped to the interval between min and max. A
  stepped parameter moves one unit per message, toward max when d > 0 and
  toward min otherwise, so a decoded 0 moves it toward min. With min < max that
  is +1 and −1; with a reversed range it is −1 when d > 0 and +1 otherwise
  (revision 4). The result is clamped to the interval between min and max and
  rounded as for Absolute (E12, E13).

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
  parameters. Relative messages, the other parameter kinds and `Absolute`
  messages of the crossfader are never subject to it, whatever the takeover
  preference; their target value applies directly. The crossfader's opt-out does
  not reach the 14-bit pair path, so a completed `Absolute14Bit` pair on the
  crossfader is subject to takeover like any other continuous control's pair
  (revision 4; E10, E11). The takeover preference offers three entries, in
  this order: None, Pick-Up and Value Scaling (text keys
  `sControlNoTakeOverEntry`, `sControlPickUpTakeOverEntry`,
  `sControlValueScalingTakeOverEntry`). Choosing one sends its position, 0, 1
  or 2. Takeover applies no rule for 0 and the Pick-Up or Value Scaling rule
  below for 1 or 2 (revision 5, E15; revision 4 inferred this from the entry
  order). With None, every absolute target value applies. X agrees: MT-06 to
  MT-14, MT-16 to MT-18, MT-22 and MT-23 give the same values under all three
  settings (E16).
- **X. Pick-Up and Value Scaling (revision 5; was S-cond).** For an absolute
  target value n subject to takeover, let lo and hi be the smaller and the
  larger of min and max, c the current value clamped to [lo, hi], and
  w = (hi − lo)/64. Let p be the target value that the previous data value
  received on the same input, channel and controller number would have produced.
  It is formed like n, including rounding for a stepped parameter, and may lie
  outside [lo, hi]. Any earlier message counts, whether or not it was mapped.
  For a 14-bit pair the previous data value is ((128 × m) | l)/129. Here m and l are
  the previous data values on the two controller numbers, a missing one counts
  as −129, and | is the bitwise OR of 32-bit two's-complement integers. So it is
  −1/129 when neither exists, −128 + l/129 when only l exists, and −1/129 for an
  odd m or −1 for an even m when only m exists.
  - An `Absolute` message with no previous data value on its controller since
    the input opened keeps c. A p of exactly −129 also keeps c.
  - When |p − c| ≤ (hi − lo)/256, n applies.
  - Otherwise, Pick-Up applies n only when c lies in
    [min(n, p) − w, max(n, p) + w]; else it keeps c.
  - Otherwise, Value Scaling applies n when |n − c| ≤ w and keeps c when p = n.
    Else it moves c by the travelled fraction of the remaining distance:
    c + (hi − c)(n − p)/(hi − p) when n > p, and c − (c − lo)(p − n)/(p − lo)
    when n < p. This is the unrounded value passed to the setter. A stepped
    parameter's value after such a move has no expectation; the setter was not traced.
  - Every bound is inclusive. The result is clamped to [lo, hi].

  These rules also hold for 14-bit pairs, the crossfader's included, and for a
  reversed range (E11, E14, E16). They are X: the original receivers, Apply,
  value function and takeover ran on MT-19 to MT-21 and MT-24 to MT-56, and on
  MT-19 to MT-21 they agree with revision 4. Revision 4 read literally, with
  w and the scaling formed from the reported min and max, gives other values for
  a reversed range (MT-29 to MT-33) and for a p of −129 (MT-42). The entry
  mapping is S (E15). The previous-value record is emptied when the input opens
  and otherwise only by the control-surface call `reset_input_history`, which
  no user-mapping module calls (E15).
- **S-cond. On/off parameters.** An absolute data value v turns an on/off
  parameter on exactly when v lies between the parameter's stored MIDI CC on/off
  thresholds, minimum and maximum inclusive. The result is inverted when the
  minimum exceeds the maximum. A completed 14-bit pair is compared as
  (128 × MSB + LSB)/129. A relative message turns the parameter on when d > 0
  and off otherwise. Neither takeover nor rounding applies (E13). Open: that the
  bounds are the stored thresholds is inferred, and an unexplained host check
  can substitute the parameter's ordinary range (PRB-N7-04). No reference
  observation is available (ADR 0003); a static trace of that check (E13)
  could still settle it. X (revision 5): given those bounds, the comparison,
  the inversion, the 14-bit comparison and the relative rule ran as stated,
  under all three takeover settings (MT-17, MT-18, MT-43, MT-44; E16).
- **Unknown.** A present token outside the ten reaches the host as a plain
  string instead of a mode value (E1 L52); no Absolute fallback is promised.
  N and R: PRB-S4-04. Also unknown:
  - the takeover preference default (PRB-N7-03);
  - delivery ordering, coalescing and deferred application of back-to-back
    messages (PRB-N7-05);
  - displayed values and any processing after a value is set (PRB-N7-01);
  - what a stepped parameter shows after a Value Scaling result that is not an
    integer. The setter was not traced; for range 0–3 the value passed to it
    can be 2.3333335 (E16, run TK-21);
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
  that has not been traced. PRB-S4-09 will not run (ADR 0003); tracing those
  tables is the remaining static route.

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
  partial banks and bank limits: PRB-S4-11, which will not run (ADR 0003). The
  static route is `_Framework/MixerComponent` track ordering.

### REQ-MIDI-USER-010 — master, cue and crossfader

- **D.** `MasterVolumeSlider`, `CueVolumeSlider` and `CrossfaderSlider` target
  master volume, cue/preview volume and the crossfader (D6).
- **S.** Released v1 clauses, plus mode scope: `VolumeMapMode` covers master and
  cue (E2 L140, L188–203); `CrossfaderMapMode` covers the crossfader (E2
  L205–212). Values follow REQ-MIDI-USER-005. The crossfader is the only
  continuous control with takeover disabled (E2 L216), so its `Absolute` values
  apply whatever the takeover preference (E10, E13). Its completed
  `Absolute14Bit` pairs ignore that opt-out and are subject to takeover like
  those of other continuous controls (revision 4; E11); see the
  [takeover exemptions](#req-midi-user-005--map-modes). Master and cue volume
  are subject to takeover like other continuous controls.
- **Unknown.** Reported ranges and kinds of these three parameters, displayed
  values, processing after a value is set and values for absent targets:
  PRB-N7-01, which refines PRB-S4-05. No self-contained function decides the
  displayed master volume: the reported range and the set path go through the
  volume parameter's own methods, which were not traced (E13). Only the later
  fader curve and gain text are pure (revision 5, E16).

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
parameter value on its own scale within τ = max(1e-6, 2⁻²² × R), where
R = max(|min|, |max|) (revision 5; was 1e-6). The rules use exact arithmetic;
the original computes in binary32. A value reached by k relative messages in a row
on a parameter that is not stepped is compared within k × τ (revision 6, RV4-02).
Rounding can accumulate: the retained review ran 200 messages on 0–5.3 and found
5.2τ drift, and on −3.3–4.9 it first exceeded τ after 25 messages
([midi-config-v4 review](../../handoff/midi-config-v4/REVIEW.md#findings)).
For one message, τ covers the one computation
the two slices perform differently. arm64 forms the absolute target
lo·(1 − t) + hi·t with one fused multiply-add, and x86_64 rounds twice. Over
every data value and every 14-bit pair in ten ranges, the two results differ by
at most one binary32 unit in the last place of R, and not at all when lo = 0
(E16). Value Scaling can magnify that difference: a model of both slices gives
up to 18 × 2⁻²² × R for range −999 to 999. A takeover comparison that lies
within about one such unit of its bound can also come out differently. Cases
with a Value Scaling result or a boundary input therefore use lo = 0.

Revision 6 also adopts the [v4 review](../../handoff/midi-config-v4/REVIEW.md#scope-rulings)
precision limits. Outside explicitly stated X case expectations, these have no expectation,
and neither do subsequent values in the same sequence:

- A takeover test whose two sides lie within 8τ: c and a window bound, |p − c| and
  (hi − lo)/256, |n − c| and w, p and −129, or p and n (except p = n from the same
  data value). The existing X boundary cases retain their stated values.
- A stepped target n or p within 8τ of a half-integer (RV4-01); binary32 rounding
  can select the other adjacent integer.
- A Value Scaling move. Even at lo = 0, binary32 can magnify error beyond τ. The
  reviewer's operation-order model found 96τ on 0–1, 386τ on 0–3 and 408τ on
  0–127 for 14-bit pairs near the upper bound with c at the lower bound; the author's
  earlier 3.8τ was a sample result, not a bound (RV4-06). These are model results,
  not additional extracted executions. Only the explicitly stated X moves are graded;
  a stepped parameter's value after a move remains unknown (RV4-05).

No wall-clock, musical-clock, latency, jitter or other numerical tolerance is
established. Do not use an arbitrary timeout as evidence of a no-action result.
A later execution harness must establish a bounded completion/observation
method before claiming pass.

Relevant state includes selected and locked device, device bank, mixer bank,
track states, transport states, the takeover preference and held 14-bit halves.
It also includes, per input, the last data value received on each channel and
controller number, which is empty when the input opens. Only the
control-surface call `reset_input_history` empties it later. No user-mapping
module calls it; the shipped Launch Control XL script does, so another surface
on the same input could (E15). Documented state changes are confined to the
requirements above. Selection retention,
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

Five case sets exist. None has run against a candidate, and no reference run
of the application will happen (ADR 0003). Revision 5 runs the original x86_64
mapping chain on MT-01 to MT-23 and adds MT-24 to MT-56 from those runs (E16).

| Set | Cases | Status |
| --- | --- | --- |
| Revision 1 matrix `acceptance-cases.json` (MIDI-USER-001–046) | 46 groups over all requirements, including unresolved ones | Retained in the macOS `midi-user-mapping-v1` evidence tree, which is absent on this host |
| [S4 draft cases](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/draft-cases-v2.json) (S4-MIDI-001–055) | 55 configuration-interpretation cases | Analyst draft. S4-MIDI-030 expected Send B for a lone `Send2Knob1`, which fails the REQ-009 check; corrected in the staged candidate |
| [Staged midi-config-v2](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v2/README.md) (MIDI-CONFIG-001–109) | 54 v1 cases restated plus 55 new | Released on 2026-10-17 as [midi-config-v2](../../handoff/midi-config-v2/README.md), approved with narrowing; see the [v2 plan](midi-config-v2-handoff-plan.md) |
| [N7 transform cases](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/out/acceptance-cases.json) (MT-01–MT-23) | 23 value sequences for REQ-005 and REQ-010 | Static derivations, listed below; X agrees with all 23 |
| [X2 cases](../../analysis/ableton-live-12.4.3/r2/x2-midi-v1/acceptance-cases-x2.json) (MT-24–MT-56) | 33 value sequences: takeover, reversed ranges, 14-bit previous values, boundaries, a wide range | Expected values from X runs, listed below |

Logical comparisons use exact integer/channel/target identifiers or exact Boolean
state where an expected state is supported. Value cases compare the parameter
value after each message within τ (see Timing and state). Display curves, bank
contents and feedback bytes have no oracle yet and must not be graded as passes.
An unknown expected result has comparator `unresolved`, never an invented
golden output. Documentation provenance is not an observed reference result.

### Value transform cases MT-01 to MT-56

These cases test REQ-MIDI-USER-005; MT-22 and MT-45 also test
REQ-MIDI-USER-010. Unless a row says otherwise, the assignment is CC 20 on
channel 0, sent as `B0 14 vv`. For `Absolute14Bit` the least significant half
is CC 52 (`B0 34 vv`), written L:vv. The target is a continuous parameter, not
stepped, with min 0, max 1 and current value 0.5. Nothing has been received on
CC 20 or CC 52 since the input opened. Data bytes are hexadecimal. A row's
"from" value is the current value before the first message; it is a binary32
number, and 2⁻¹⁹ or 2⁻¹⁸ is one binary32 step there. Relative cases MT-06 to
MT-14, MT-16 and MT-23 hold under any takeover setting. So does MT-22, because
crossfader `Absolute` values are exempt; a crossfader `Absolute14Bit` pair is
not (MT-45). MT-22 assumes the crossfader reports the range 0–1; for another
range its values are min + (max − min) × v/127.

S rows are static expected outputs, and X agrees with every one (E16). X rows
take their expected values from X runs; MT-19 to MT-21 were S-cond in revision
4. S-cond rows give predictions, not expected outputs: MT-17, MT-18, MT-43 and
MT-44 assume that the on/off bounds are the stored thresholds, which the host
check in E13 leaves open. X agrees with them given those bounds. Their
comparator stays `unresolved`. The probes that would have measured these cases
are PRB-N7-01 (MT-01–05), PRB-N7-02 (MT-06–14), PRB-N7-03 (MT-19–23), PRB-N7-04
(MT-15–18) and PRB-N7-05 (ordering); none will run (ADR 0003). MT-47 to MT-56
place the current value on a takeover bound and one binary32 step outside it.

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
| MT-19 | X      | Absolute; Pick-Up                                                   | 0A 0B 0C 3F 46          | 0.5, 0.5, 0.5, 0.496063, 0.551181                                  |
| MT-20 | X      | Absolute; Value Scaling                                             | 0A 14 1E                | 0.5, 0.542735, 0.58547                                             |
| MT-21 | X      | Absolute; Pick-Up; first message                                    | 64                      | 0.5                                                                |
| MT-22 | S      | Absolute; Pick-Up; crossfader (takeover disabled)                   | 0A 64                   | 0.07874, 0.787402                                                  |
| MT-23 | S      | LinearSignedBit; Pick-Up                                            | 01                      | 0.503906                                                           |
| MT-24 | X      | Absolute; Pick-Up; from above, crossing down                        | 78 64 3C 32             | 0.5, 0.5, 0.472441, 0.393701                                       |
| MT-25 | X      | Absolute; Pick-Up; one jump past the value                          | 0A 64                   | 0.5, 0.7874016                                                     |
| MT-26 | X      | Absolute; Value Scaling; downward to min                            | 78 6E 00                | 0.5, 0.4583333, 0                                                  |
| MT-27 | X      | Absolute; Value Scaling; same data value twice                      | 0A 0A                   | 0.5, 0.5                                                           |
| MT-28 | X      | Absolute; Value Scaling; first message                              | 64                      | 0.5                                                                |
| MT-29 | X      | Absolute; Pick-Up; reversed range, min 1, max 0                     | 0A 3F 40 46             | 0.5, 0.503937, 0.496063, 0.448819                                  |
| MT-30 | X      | Absolute; Value Scaling; min 1, max 0; target falling               | 0A 14 1E                | 0.5, 0.457265, 0.41453                                             |
| MT-31 | X      | Absolute; Value Scaling; min 1, max 0; target rising                | 64 5A                   | 0.5, 0.55                                                          |
| MT-32 | X      | Absolute; Pick-Up; min 1, max 0, from 0.25; in sync                 | 5F 64                   | 0.25, 0.2125984                                                    |
| MT-33 | X      | Absolute; Pick-Up; min 3, max −1, from 1.06                         | 28 3C                   | 1.06, 1.110236                                                     |
| MT-34 | X      | Absolute14Bit; Pick-Up; first pair, target above                    | 50 L:00                 | 0.5, 0.625038                                                      |
| MT-35 | X      | Absolute14Bit; Pick-Up; first pair, target below                    | 10 L:00                 | 0.5, 0.5                                                           |
| MT-36 | X      | Absolute14Bit; Value Scaling; first pair, target below              | 10 L:00                 | 0.5, 0.5625305                                                     |
| MT-37 | X      | Absolute14Bit; Value Scaling; previous MSB only                     | 10 60 L:00              | 0.5, 0.5, 0.8759993                                                |
| MT-38 | X      | Absolute14Bit; Value Scaling; previous LSB only                     | L:20 L:00 60            | 0.5, 0.5, 0.937696                                                 |
| MT-39 | X      | Absolute14Bit; Pick-Up; three pairs                                 | 30 L:00 41 L:00 50 L:00 | 0.5, 0.5, 0.5, 0.5078435, 0.5078435, 0.625038                      |
| MT-40 | X      | Absolute; Pick-Up; stepped, range 0–3, from 1                       | 32 7F                   | 1, 3                                                               |
| MT-41 | X      | Absolute; Pick-Up; enumerated, range 0–3, from 1                    | 7F                      | 3                                                                  |
| MT-42 | X      | Absolute; Pick-Up; range −129 to 0, from −10                        | 00 7F                   | −10, −10                                                           |
| MT-43 | S-cond | Absolute14Bit; on/off, thresholds 64–127, from off                  | 40 L:00 40 L:7F 7F L:7F | off, off, off, on, on, on                                          |
| MT-44 | S-cond | Absolute; on/off, thresholds min 127, max 64, from off              | 3F 40 7F                | on, off, off                                                       |
| MT-45 | X      | Absolute14Bit; Pick-Up; crossfader; first pair, target below        | 10 L:00                 | 0.5, 0.5                                                           |
| MT-46 | X      | Absolute; None; range 20–999, from 500                              | 04 05 08 7F             | 50.8346, 58.5433, 81.6693, 999                                     |
| MT-47 | X      | Absolute; Value Scaling; range 0–127, from 30.49609375              | 1E 0A                   | 30.4961, 10                                                        |
| MT-48 | X      | Absolute; Value Scaling; range 0–127, from 30.49609375 + 2⁻¹⁹       | 1E 0A                   | 30.4961, 10.16537                                                  |
| MT-49 | X      | Absolute; Value Scaling; range 0–127, from 29.50390625              | 1E 32                   | 29.5039, 50                                                        |
| MT-50 | X      | Absolute; Value Scaling; range 0–127, from 29.50390625 − 2⁻¹⁹       | 1E 32                   | 29.5039, 49.6062                                                   |
| MT-51 | X      | Absolute; Pick-Up; range 0–127, from 31.984375                      | 0A 1E                   | 31.98438, 30                                                       |
| MT-52 | X      | Absolute; Pick-Up; range 0–127, from 31.984375 + 2⁻¹⁹               | 0A 1E                   | 31.98438, 31.98438                                                 |
| MT-53 | X      | Absolute; Pick-Up; range 0–127, from 28.015625                      | 32 1E                   | 28.01562, 30                                                       |
| MT-54 | X      | Absolute; Pick-Up; range 0–127, from 28.015625 − 2⁻¹⁹               | 32 1E                   | 28.01562, 28.01562                                                 |
| MT-55 | X      | Absolute; Value Scaling; range 0–127, from 61.984375                | 0A 3C                   | 61.98438, 60                                                       |
| MT-56 | X      | Absolute; Value Scaling; range 0–127, from 61.984375 + 2⁻¹⁸         | 0A 3C                   | 61.98438, 89.76884                                                 |

## Open questions

See the canonical [question register](../questions.md): Q-008 covers parser/host
error recovery and unknown-mode outcomes; Q-009 covers the open transform
points (PRB-N7-01 to 05), timing and feedback; Q-010 covers discovery/reload,
disconnect, persistence, undo and the send-position refinement. The 16 S4 and
five N7 probe records name the questions a reference run would have answered.
Under [ADR 0003](../decisions/adr-0003-no-reference-execution.md) no probe
will run. A material gap is closed by a focused static trace or by extracted
execution of a self-contained function of the original x86_64 code, or it
stays unknown. Concrete expected outcomes absent from this draft remain unknown
and block release of the affected behavior.

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
| E11 | 14-bit install 0x1026094e0 (`mov w3,#0x0` at 0x102609548); MSB store 0x101b8028c, LSB store 0x101b802bc, combine 0x101b7fcc0 (all n7-0002); constructor 0x101b7fc28 (decompiler only) | Each store overwrites its own half and prior, then combines when both value slots are not FLT_MAX. Combine computes (MSB<<7 \| LSB)/129.0 (0x10584a8b4, re-read 129.0), passes MapMode 0 and sensitivity 1.0, then resets all four slots to FLT_MAX. With the avoid flag clear, −129 priors give (−1)/129, not the no-prior sentinel, so the first pair is left open. Revision 4 (F1): install 0x102593258 passes the avoid argument (x6, kept in x24) only to the CC receiver init 0x101b7f32c. Its mode-5 call at 0x10259338c passes x0–x4, and 0x1026094e0 calls the pair receiver init 0x101b7fc74 (decompiler only: fourth argument stored at +0x44) with `mov w3,#0x0`. Combine reads +0x44 at 0x101b7fce4, so with the flag clear the pair's prior is formed and apply can reach takeover for any control, the crossfader included. Re-read on 2026-10-18; the [reviewer checks](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v3-analysis/review/review-checks.txt) agree |
| E12 | Value function 0x101b76bf0 (n7-0002); decoder 0x101b7b96c (n7-0001); table init 0x101b842cc (n7-0003); divisor 0x1011afc2c (decompiler only: 127.0, or 8191.0 for −2) | Absolute: t = v/127, lo·(1−t)+hi·t by `fmadd`. Relative: (hi−lo)·(1/256)·d·s or ±1 when quantized, then clamp. `frinta` at 0x101b76cd4 rounds when quantized. Decoder branches were checked against the table above. Vectors at 0x106fba2a8 (B, 8 floats from 0x10584a580) and 0x106fba2c0 (A, 8 floats from 0x10584a5a0 plus 50.0 stored at +0x20) were re-read with `scripts/readvm.py` and match `out/native-constants.json`. Revision 4 (F2): apply 0x101b80148–0x101b80170 passes lo = min(Min, Max), hi = max(Min, Max) and the flag Max < Min. When the flag is set, the value function uses t = (127 − v)/127 (0x101b76c44–0x101b76c4c) and negates the relative step (0x101b76cb4–0x101b76cbc), so a stepped d > 0 moves toward Max. Re-read on 2026-10-18; the reviewer's probe (min 3, max 0, from 1, d > 0 gives 0) agrees |
| E13 | Details 0x1026fa5c8 → 0x1026fa684 and 0x1024dd61c (n7-0003); apply 0x101b7fde4 (n7-0001); CC receiver 0x101b7f894 (n7-0002); Python `DeviceParameter` getters 0x103afe2cc/3c0/3d0 (decompiler only); [on/off thresholds](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/out/onoff-thresholds.json) | Type is 1 `ATimeableFloat`, 2 `ATimeableBool`, 3 `ATimeableEnum` or 0 for other. Min/Max come from vtable +0x2f0/+0x2f8, or from the +0x388 range object when the Bool flag is set; registry 0x1011aeb80 can clear that flag and is unexplained. Quantized is +0x2e0, or an internal byte equal to 2. Apply, with Zoom ≤ 1: Type 2 absolute uses lower ≤ v ≤ upper XOR (Min > Max), and Type 2 relative uses d·s > 0. Other types use the value function; takeover runs only for MapMode 0/5, Type 1 and prior ≠ FLT_MAX. When 0x1011c0ee8(0x100500) ≠ 0, the fields are posted as `OChangeControllerDataCommand` (timing unknown). Setter 0x101b0d328 was not traced. The receiver blanks the prior when avoid is set and Zoom = 1.0. Quantized relative accumulates ±s and fires at \|acc\| ≥ 1. Shipped sets carry Min 64/Max 127 in 22,059 of 22,303 threshold pairs |
| E14 | Takeover 0x101b7c508 and Pick-Up 0x101b7c344 (n7-0001); preference setter 0x101b83750 (n7-0003); UI entry order 0x1022df424 (decompiler only) | The global mode at 0x106fb2110 has three cases. 0 returns clamp(new). Otherwise a prior equal to −129.0 keeps c, and \|p − c\| ≤ (hi−lo)·0.5/128 applies new. Mode 2 uses w = (hi−lo)·2/128 and proportional scaling. Mode 1 uses the [min(n,p) − w, max(n,p) + w] window and posts a pick-up notification. Inferred: index 0/1/2 = None/Pick-Up/Value Scaling, from the declaration order and the notification. The default was not found |

Revision 5 evidence. E15 is a static reading of both slices; E16 is the X
packet [x2-midi-v1](../../analysis/ableton-live-12.4.3/r2/x2-midi-v1/manifest.json),
regenerated by `sh run.sh` there. The [research page](../research/midi-transforms-native.md#extracted-execution-results-x2-2026-10-18)
gives the method and results in full.

| Label | Locator | What was checked for revision 5 / limitation |
| --- | --- | --- |
| E15 | Preference: `LMidiPreferences` constructor x86 0x1023e0050 / arm64 0x1022cc18c; change handler x86 0x1023e2a60 / arm64 0x1022cec38 (`CallMemberFunc<&LMidiPreferences::OnTakeOverModeChanged>`); index getter x86 0x101556330 / arm64 0x1015661b8; entry text x86 0x1015566d0; engine handler x86 0x101bc0770 / arm64 0x101b83750. Reset: `MidiInputRouter.ResetInputHistory` handler arm64 0x101b68f98 (registered in 0x101b67c9c), refill 0x101b65c1c, sole poster 0x10259b710, Python method `reset_input_history` (0x1039fa2a4) | Excerpts in [static-e15.txt](../../analysis/ableton-live-12.4.3/r2/x2-midi-v1/static-e15.txt); the x86 handler, index getter and engine handler were also read in disassembly (`x86-disasm.txt`). In both slices the constructor builds the entry list from the three keys in the order None, Pick-Up, Value Scaling, installs it on the chooser at +0x148 and binds `OnTakeOverModeChanged` to it. The handler, the only code that posts `OSetMidiTakeOverMode`, sends the chooser index; an unset index (−99) sends 0. The engine stores it in the global the takeover reads. The displayed words of the keys were not read, because the language resources are packed. The preference default was not found. Of the shipped MIDI Remote Scripts, only `Launch_Control_XL/LaunchControlXL.pyc` contains `reset_input_history` |
| E16 | X runs in `run_x2.py`, results `results/{mt,takeover,tolerance,value_scaling_model}.json`, cases `acceptance-cases-x2.json`; x86 → arm64 matches in `addresses.json`: CC receiver 0x101bbc3b0 → 0x101b7f894, 14-bit setters 0x101bbced0/0x101bbcf10 → 0x101b8028c/0x101b802bc, combiner 0x101bbc870 → 0x101b7fcc0, Apply 0x101bbc9c0 → 0x101b7fde4, value function 0x101bb27b0 → 0x101b76bf0, takeover 0x101bb8b70 → 0x101b7c508, Pick-Up 0x101bb8990 → 0x101b7c344 | The receivers, Apply, value function and takeover ran; the takeover index was set by the original handler. Stubbed under gdb: the owner and parameter accessors (0x101abb210, 0x101b3d680), the current-value read (0x101b6f830) and the setter (0x101b3d360), which together simulate the parameter, and the pick-up notification post, which is jumped over after the result is stored. Not run: the dispatcher and previous-value table (the harness supplies the previous value as E10 states), the parameter-details builder and the setter. Imports used: `operator new`, C++ guards, `__cxa_atexit`, pthread keys; no libm. Static slice comparison: the same operations and constants in all these functions. The only fused instructions are the value function's `fmadd` (E12) and the takeover's `fmadd s10,s0,s1,s10` with s1 = ±1, an exact product |

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

| Revision | Date | Change |
| --- | --- | --- |
| 6 | 2026-10-19 | applies the released [midi-config-v4 review](../../handoff/midi-config-v4/REVIEW.md) RV4-01, RV4-02, RV4-05 and RV4-06: stepped half-integer exclusion, k × τ for repeated relative messages, no stepped value after a Value Scaling move, and 96–408τ model examples replacing the earlier sample figure. The exact rules are now qualified by those precision limits. 13 requirements, 55 configuration cases and 56 transform cases remain; no case expectation changes. midi-config-v4 is the current released partial contract with 161 cases, a superset of v3 with two precision corrections. |

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

Released 2026-10-18: [midi-config-v3](../../handoff/midi-config-v3/README.md), 127 cases, approved by a separate review agent (partial REQ-002/003/005–013 only; 001 and 004 unreleased; MT-17 to 21 out). The review findings to apply in the next revision are on the [handoff plan](midi-config-v3-handoff-plan.md#review-outcome). Revision 4 applies the review findings; see the next paragraph.

Revision 4, 2026-10-18: applied the
[midi-config-v3 review findings](midi-config-v3-handoff-plan.md#review-outcome)
after re-reading the kept disassembly (E11, E12) and the [reviewer checks](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v3-analysis/review/review-checks.txt).
Applied: F1 (RV3-02), the crossfader takeover exemption holds for `Absolute`
values only, because the 14-bit pair path ignores the opt-out; the
REQ-MIDI-USER-005 takeover exemptions and Pick-Up clause and REQ-MIDI-USER-010
are corrected. F2 (RV3-03), the reversed-range rule is stated: the formulas hold
for either order, clamping is to the interval between min and max, and a
stepped parameter moves toward max when d > 0. Takeover with a reversed range
is a new unknown. RV3-04 (F3): MT-22, like the relative cases, now states that
it holds under any takeover setting. Rejected: RV3-07, which proposes further
cases and a range-scaled tolerance. It reports no wrong clause or value, and its
cases need new derivations and a case-file update outside this revision. No
change needed: RV3-01 (the None label is already stated as inferred), RV3-05
(the inferences are already in E10 and the unknowns), RV3-06 (evidence identity)
and RV3-08 (release metadata). Under [ADR 0003](../decisions/adr-0003-no-reference-execution.md),
probe-dependent wording now says that no reference observation is available and
names the remaining static route. Requirement and case IDs are unchanged and no
case is withdrawn. Every MT row uses min < max and none is a crossfader 14-bit
pair, so no expected value changes. midi-config-v3 is unchanged and remains the
current release.

Revision 5, 2026-10-18: applied the
[X2 extracted-execution results](../research/midi-transforms-native.md#extracted-execution-results-x2-2026-10-18)
(E16) and a static trace of the takeover preference and the previous-value reset
(E15). New label X. Changed from S-cond to X: Pick-Up and Value Scaling. They
are restated with lo and hi, the sorted bounds, which settles the reversed-range
unknown of revision 4. They also gain five rules: the previous value of a
14-bit pair, which settles the first-pair unknown; the rounded previous target
of a stepped parameter; a previous target of −129; the unrounded Value Scaling
result; and inclusive bounds. Changed from inferred to S: the None, Pick-Up and
Value Scaling entry mapping, and the reset of the previous-value record. The
on/off clause stays S-cond and gains its X check. The value tolerance changes
from 1e-6 to τ = max(1e-6, 2⁻²² × R), because the arm64 fused multiply-add
differs from the x86_64 result by up to one binary32 unit of R. The
master-volume display (PRB-S4-05) stays unknown: no self-contained function
decides it. No S clause or expected value of revision 4 was wrong. Two revision
4 texts were wrong. The 1e-6 tolerance cannot hold on both slices for wide
ranges with min ≠ 0. The Pick-Up and Value Scaling text, read with the reported
min and max, gives wrong values for a reversed range; revision 4 had listed
that case as unknown. Cases: MT-19 to MT-21 become X, and MT-24 to MT-56 are
new, 31 X and 2 S-cond. X agrees with all of MT-01 to MT-23. Requirement and
case IDs are unchanged and no case is withdrawn. midi-config-v3 is unchanged:
its cases use min 0 and min < max, so τ equals its 1e-6, and it excludes MT-17
to MT-21.
