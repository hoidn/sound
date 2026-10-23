---
id: SPEC-BUNDLED-DEVICE-PARAMETERS
type: spec
status: draft
updated: 2026-10-22
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Bundled device parameters in documents

## Scope

Feature FEAT-DEVICES, with FEAT-PERSISTENCE, in the [feature map](feature-map.md).
User task: open a preset, rack, clip or Live Set that contains one of the seven devices
Live ships as separate engine bundles (Amp, Cabinet, Analog, Tension, Collision,
Electric, Corpus), keep every parameter value, and save it back. This draft specifies
the stored representation of their parameters only:

- the element that stores each device, and where it sits in each document kind;
- the shape of each parameter element and the text of its value;
- each parameter's path, value class and value domain;
- the value a parameter has when its element is absent;
- what a malformed, unknown, duplicated or out-of-range item does on load.

Excluded: the shared device envelope (the 21 schema fields from `LomId` to
`OverwriteProtectionNumber` that all 97 device classes share, of which documents store
20; REQ-002), signal processing and sound, the mapping from stored values to engine
values, display strings and units other than enumeration labels, live edits (UI, API,
MIDI, automation playback), undo, older document versions and their migration, Max for
Live devices and `Max/` presets.

Every requirement is a **proposed contract** supported by shipped bytes, by a static
derivation from the 12.4.3 program, or explicitly unknown. Nothing was run against Live.
[ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits a static-first draft.
Under [ADR 0003](../decisions/adr-0003-no-reference-execution.md) no reference observation
will be made: an unknown clause stays unknown unless static work settles it.
Target: 12.4.3, documents with `MinorVersion="12.0_12402"`. The gzip/XML envelope and
root attributes belong to the draft [SPEC-ALS-CONTAINER](als-container.md); value text
rules come from the draft [SPEC-TRANSPORT-STATE](transport-state.md). All document
examples are fragments of the decoded XML.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema files or the 3,634 presets, racks, clips and sets in the 12.4.3 bundle. These were not written by a 12.4.3 save |
| S | Static derivation from the 12.4.3 executable or shipped bytes; not an observed run. An assumption is named beside the clause when one is needed (A1–A3 below) |
| U | Unknown; no expected result, or only a static expectation that must not be graded. No reference observation is available (ADR 0003); the clause names the static route that could still settle it, or says that none is known |

Only D and S clauses may enter a release. U clauses block the behavior they name.
"The document does not open" means the document reader stops with a read error, as in
SPEC-TRANSPORT-STATE. Each parameter is named by its path below the device element, for
example `Resonator1/Quality` below `Collision`.

## Assumptions

Each assumption is supported by the evidence but not established. If one fails, the
clauses that name it become unknown.

| ID | Assumption | What rests on it |
| --- | --- | --- |
| A1 | A device element read from a document is first constructed with the default values of the parameter tables and then receives only the members present in the document, stored as read, without range checks | REQ-006 to REQ-008, REQ-010, the "Default when absent" column |
| A2 | A parameter's `Manual/@Value` has the base type its class shows in shipped text: 32-bit Float for Float parameters, Int for Enum parameters, Bool for Bool parameters, converted by the same reader as the transport values | REQ-004, REQ-005 |
| A3 | The label lists in REQ-014 (enumerations and the Cabinet switch) are the texts the user interface shows for each stored value | REQ-014 |

## Requirements

Release [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md)
carries only the partial clauses that the
[plan's scope table](bundled-device-parameters-handoff-plan.md#scope) lists as included, as
narrowed by its review. Every other clause here is broader than the release and
unreleased. Clauses that differ from v1 because of the review say so.

### REQ-BUNDLED-DEVICE-PARAMETERS-001 — device elements and placement

- **D.** The seven devices are stored as the elements `Amp`, `Cabinet`, `UltraAnalog`
  (Analog), `StringStudio` (Tension), `Collision`, `LoungeLizard` (Electric) and
  `Corpus`. All 1,064 shipped occurrences use these names.
- **D.** In a device preset (`.adv`) the device element is the only child of the root
  `Ableton` element. In a rack preset (`.adg`) it sits at `…/AbletonDevicePreset/Device`.
  In a set (`.als`) or clip (`.alc`) it is a child of a `Devices` list, two to four
  `Devices` levels deep.
- **U.** Whether 12.4.3 writes the same placement for each kind on save. No reference
  observation is available (ADR 0003); static route: the document and member writers
  (REQ-002).

### REQ-BUNDLED-DEVICE-PARAMETERS-002 — device element content

- **D.** A device element holds 20 members of the shared device envelope followed by the
  device-specific fields of schema `12.0_12402` in schema order. None of the 1,064 shipped
  occurrences stores the 21st envelope field, `RemoteSelectionKeyMidi`. Every occurrence
  of a device holds exactly the members of its parameter table below, parameters and
  plain fields, in table order (document order). A group holds exactly the members
  listed under its path, in order, and has no attributes.
- **D.** Besides parameters, `UltraAnalog`, `StringStudio`, `Collision` and `Corpus` carry
  plain fields (REQ-011). `Amp`, `Cabinet` and `LoungeLizard` carry none.
- **D.** No document stores `ToggleDummy`, `IsChain2` or `DummyPerNotePitchBendRange`;
  the schema does not declare them.
- **S.** Two elements with the same name under one parent make the document not open
  (the reader's add-member check, as in REQ-TRANSPORT-STATE-008).
- **U.** The exact order and omissions 12.4.3 writes on save. No reference observation is
  available (ADR 0003); static route: compare the member writer, which writes child
  members in registration order and skips an unassigned key-MIDI member
  ([N1](../research/transport-state-native.md)), with each device class's member
  registration ([N6](../research/device-tables-native.md)).

### REQ-BUNDLED-DEVICE-PARAMETERS-003 — parameter element shape

- **D.** Float parameters (`TimeableFloat`) hold, in order: `LomId`, `KeyMidi` (only when
  mapped, REQ-013), `Manual`, `MidiControllerRange` (`Min`, `Max`), `AutomationTarget`,
  `ModulationTarget`. Each target holds `LockEnvelope`.
- **D.** Enum parameters (`TimeableEnum`) hold `LomId`, `KeyMidi` (only when mapped),
  `Manual`, `AutomationTarget`, `MidiControllerRange`. Bool parameters (`TimeableBool`)
  hold `LomId`, `KeyMidi` (only when mapped), `Manual`, `AutomationTarget`,
  `MidiCCOnOffThresholds` (`Min`, `Max`).
- **D.** Each value sits in a `Value` attribute of an otherwise empty element, for
  example `<Manual Value="5" />`, `<Min Value="0" />`. A plain field (REQ-011) is an empty
  element whose only attribute is `Value`; a group is an element without attributes that
  holds its members.
- **D.** In the 268 shipped device presets every parameter stores `LomId` 0 and
  `LockEnvelope` 0, its domain as range (REQ-006) and target `Id` 0 (REQ-012).

### REQ-BUNDLED-DEVICE-PARAMETERS-004 — value text on load

- **S (A2).** Float `Manual`, `Min` and `Max` text follows REQ-TRANSPORT-STATE-005
  (32-bit float; `#` with 8 hex digits; `Invalid`). Text with no numeric prefix makes the
  document not open.
- **S (A2).** Enum `Manual` text follows REQ-TRANSPORT-STATE-006; for example `3.0` or
  `0x3` makes the document not open.
- **S (A2).** Bool `Manual` text follows REQ-TRANSPORT-STATE-003: `true` or `1` loads on,
  `false` or `0` loads off, anything else (`TRUE`, empty) makes the document not open.
- **D.** Shipped content uses only plain decimal text for Float and Enum values and only
  `true`/`false` for Bool values.

### REQ-BUNDLED-DEVICE-PARAMETERS-005 — value text on save

- **S (A2).** Float values are written with the 32-bit rule of REQ-TRANSPORT-STATE-011
  (nine significant digits, trailing zeros removed): 1/6 as `0.1666666716`, 0.6 as
  `0.6000000238`. Enum values are written as plain decimal integers, Bool values as `true`
  or `false`.
- **D.** All 114,570 Float `Manual`, `Min` and `Max` texts of these devices in the 599
  shipped documents that contain them equal that rule applied to their own value.

### REQ-BUNDLED-DEVICE-PARAMETERS-006 — value domains

- **D.** Each parameter's domain is the `Min..Max` of its `MidiControllerRange` when it has
  no `KeyMidi`, as listed in the parameter tables. In shipped content every unmapped
  occurrence stores exactly this range, except a few occurrences of 13 parameters that
  store a narrower one, and no stored `Manual` lies outside it. None of the narrower
  ranges is in a device preset: all 28,116 parameter instances in the 268 `.adv` store
  exactly the domain.
- **S.** The range the program attaches to a parameter when it constructs the device
  equals the listed domain for all 372 Float parameters and for the 11 Enum parameters of
  Amp, Cabinet, Electric and Corpus. The other 59 Enum domains (Analog, Tension,
  Collision) are D only; for 22 of them no shipped value reaches the upper bound, so they
  rest on the stored range alone.
- **D.** Bool parameters store `MidiCCOnOffThresholds` `Min` 64 and `Max` 127 when
  unmapped. Enum domains are `0..N−1` for N values.
- **S (A1).** A value inside its domain, read by REQ-004, is the parameter's value after
  the document opens. v1 releases this for device presets except for the position
  parameters of REQ-015 (review RVB-02).
- **U.** What a narrower stored `MidiControllerRange` on an unmapped parameter does. No
  reference observation is available (ADR 0003); static route: the create path of A1.

### REQ-BUNDLED-DEVICE-PARAMETERS-007 — integer-stepped Float parameters

- **S.** The Float parameters marked "integer steps" in the tables take whole-number
  values: Analog and Tension `Octave` and `Transpose`, Analog `OscillatorOct`,
  `OscillatorSemi` and `LFOSync`, Tension `PitchBendRange` and `LFOSync`, Collision
  `Resonator*/Transpose`, `Resonator*/FineTranspose`, `Lfo*/SyncRate` and
  `PitchBendRange`, Electric `KeyboardTranspose`, Corpus `Transpose`, `FineTranspose`,
  `PitchBendRange` and `LfoSyncRate`, and `PerNotePitchBendRange` of Analog, Tension,
  Collision and Electric.
- **D.** Shipped content stores integer text for all of them.
- **S (A1).** A fractional value (for example `3.7`) loads without error.
- **U.** Which value is then displayed and written on save. No reference observation is
  available (ADR 0003); static route for the saved value: the create path of A1 and the
  device post-load step. No static route is known for the display.

### REQ-BUNDLED-DEVICE-PARAMETERS-008 — defaults when an element is absent

- **S (A1).** A parameter element that is missing, or whose `Manual` lacks its `Value`,
  does not stop the document from opening. The parameter then has the "Default when absent"
  value of the tables, and a later save writes that value (REQ-005).
- **S.** For Analog, chain 1 and chain 2 differ: `SignalChain1/OscillatorToggle` and
  `SignalChain1/AmplifierToggle` default to `true`, the `SignalChain2` ones to `false`.
- **U.** The `MidiControllerRange` written for a parameter whose element was absent
  (expected: its domain; not traced) and the target `Id` (REQ-012). No reference
  observation is available (ADR 0003); static route: the range the constructors set
  (REQ-006) and the member writer.

### REQ-BUNDLED-DEVICE-PARAMETERS-009 — values of a newly inserted device

- **D.** For Analog, Tension, Collision and Electric a preset
  `Core Library/Defaults/Instruments/<Product>.adv` ships; its values differ from the
  "Default when absent" column where the tables say so (24 Analog, 9 Tension, 2 Collision,
  2 Electric parameters). No such preset ships for Amp, Cabinet or Corpus.
- **U.** Whether a device inserted from the browser starts from the Defaults preset or from
  the table defaults, for each of the seven devices. No reference observation is available
  (ADR 0003); static route: trace the insert path for a read of the Defaults preset.

### REQ-BUNDLED-DEVICE-PARAMETERS-010 — out-of-range values on load

- **S (A1).** A well-formed value outside its parameter's domain does not make the document
  fail to open. This covers Float values above `Max` or below `Min`, Enum indices above
  `N−1`, and a `MidiControllerRange` that does not match the domain.
- **U.** The value then displayed, used and written on save. Whether a negative Enum index
  (`-1`) opens at all: the `-` sign is open in REQ-TRANSPORT-STATE-006. No reference
  observation is available (ADR 0003); static routes: the create path of A1 for the
  first, the integer text reader of REQ-TRANSPORT-STATE-006 for the second.

### REQ-BUNDLED-DEVICE-PARAMETERS-011 — unknown elements and plain fields

- **S.** An unknown child element of a device element, of a group or of a parameter element
  is skipped with its content; the document opens and a later save does not write it. The
  versioned-read exception of REQ-TRANSPORT-STATE-008 applies here too.
- **D.** The plain fields are the Plain rows of the tables: 7 in Analog, 3 in
  Tension, 3 in Collision (`Resonator1/TransposeRelativePosition`,
  `Resonator2/TransposeRelativePosition`, `CurrentTab`), 7 in Corpus, none in Amp, Cabinet
  and Electric. Every device preset stores the text of the tables. In other documents
  every `*RelativePosition` is `-1073741824` as well, except one Tension
  `OctaveRelativePosition` `0` and one `TransposeRelativePosition` `-90`, both in `.als`;
  `UltraAnalog/SelectedFinger` is `7`; `StringStudio/CurrentTab` is `0`;
  `Collision/CurrentTab` is `0` except `3` in one clip. All 36 `Corpus` occurrences store
  the seven side-chain fields below `SideChain/RoutedInput/Routable` with the table texts:
  `Target` `MidiIn/None`, `UpperDisplayString` `No Output`, `LowerDisplayString` empty,
  `MpeSettings/ZoneType` `0`, `MpeSettings/FirstNoteChannel` `1`,
  `MpeSettings/LastNoteChannel` `15` and `MpePitchBendUsesTuning` `true`.
- **S.** The constructors set the same values for these stored fields: `-1073741824` for
  Analog and Tension `OctaveRelativePosition` and `TransposeRelativePosition` and for
  Collision `Resonator1/TransposeRelativePosition` and `Resonator2/TransposeRelativePosition`;
  `7` for Analog `SelectedFinger`; `0` for Tension and Collision `CurrentTab`. The Analog
  signal-chain `*RelativePosition` fields and the Corpus side-chain fields are not set
  there (not traced). The constructors also set members that no document stores and the
  schema does not declare, among them Collision `PitchBendRangeRelativePosition` and
  `Lfo1/SyncRateRelative`, `Lfo2/SyncRateRelative`; they are not part of the format.
- **U.** What these fields mean, and the default when absent of the fields marked "not
  traced" in the tables. No reference observation is available (ADR 0003); static route:
  the Analog signal-chain and Corpus side-chain construction.

### REQ-BUNDLED-DEVICE-PARAMETERS-012 — automation and modulation target identifiers

- **D.** Every parameter's `AutomationTarget` and every Float parameter's
  `ModulationTarget` carry an `Id`. It is `0` in all 37,794 parameter instances in
  `.adv`/`.adg` files and nonzero in all 13,618 in `.als`/`.alc` files, where the nonzero
  values are unique within each document. Each target holds `LockEnvelope`.
- **U.** The rule 12.4.3 uses to assign `Id` values on save. No reference observation is
  available (ADR 0003), and no static route has been identified. No shipped envelope
  targets these devices.

### REQ-BUNDLED-DEVICE-PARAMETERS-013 — rack macro bindings

- **D.** A bound parameter stores `KeyMidi` with `Channel` 16 and `NoteOrController` 0–10,
  and its `MidiControllerRange` holds the bound sub-range (for example Amp `Gain`
  `1.484375..10`). Bindings occur only inside racks and sets (1,672 instances), never in
  standalone `.adv` presets.
- **U.** That `NoteOrController` n is rack macro n, and whether other channels occur for
  these devices. No reference observation is available (ADR 0003), and no static route has
  been identified.

### REQ-BUNDLED-DEVICE-PARAMETERS-014 — enumeration labels

- **S (A3).** Labels of stored values, in order from 0:
  - Amp `AmpType`: Clean, Boost, Blues, Rock, Lead, Heavy, Bass.
  - Cabinet `CabinetType`: 1x12, 2x12, 4x12, 4x10, 4x10 Bass;
    `MicrophonePosition`: Near On-Axis, Near Off-Axis, Far.
  - Electric `PickupModel`: R, W.
  - Corpus `ResonanceType`: Beam, Marimba, String, Membrane, Plate, Pipe, Tube;
    `ResonatorQuality`: Eco, Low, Med, High; `MidiMode`: Last, Low.
- **S (A3).** Cabinet `MicrophoneTypeSwitch` shows Dynamic for true and Condenser for false.
  Not in v1: the release excludes this switch's labels (review RVB-01), because revision 1
  gave them reversed.
- **D.** Corpus `Pipe Resonator.adv` stores `ResonanceType` 5 and `Tubular Pan.adv` stores 6.
- **S (labels), X (voice-count meaning).** Electric `Polyphony` index p = 0..30
  corresponds to labels `2` to `32` and permits p + 2 voices. Extracted execution
  tested all 31 indices ([REQ-DEVICE-ELECTRIC-005](device-electric.md#req-device-electric-005--voices-and-polyphony),
  DEL-025; retained `t12-electric-v1/results/probes_events.json` `voices.limit`).
  The exact display text combining the label and `Voices` remains U.
- **U.** Corpus `LfoType` (Sine, Square,
  Triangle, SawUp, SawDown, Sample & Hold, Random Ramp), `LfoSync` (Free, Sync) and
  `LfoStereoMode` (Phase, Spin): the program holds a second name list after each of these
  label lists, which suggests that the user interface shows icons or short names. These
  static readings must not be graded.
- **U.** Enumeration labels of Analog, Tension and Collision.
- No reference observation is available for the U clauses (ADR 0003). Static route: decode
  the label tables Analog, Tension and Collision build at run time, and trace where the
  second name lists and the `Voices` text are displayed.

### REQ-BUNDLED-DEVICE-PARAMETERS-015 — position parameters of Corpus and Collision

- **D, S.** Corpus `ExcitationX`, `ListeningXL`, `ListeningXR` and Collision
  `Resonator1/2` `HitX`, `ListeningXL`, `ListeningXR` are Float parameters with domain
  0..1 and the defaults of the tables. v1 keeps their table rows but judges none of their
  values (review RVB-02).
- **U.** Which part of the resonator's position range the stored 0..1 covers. Static
  readings disagree. On the traced chain the stored 0..1 reaches the device bundle
  unchanged and becomes controller values of about 64 to 95 out of 0..127 (Corpus
  64 + 31.5v; Collision bundle range −2..2), half of what an input of −1..1 would reach.
  An untraced Live-side rescale to −1..1 would explain this, but nothing found supports
  either reading. This does not change storage. The contradiction is unresolved. No reference observation is available (ADR 0003). A static route remains:
  trace the value the Live-side float parameter unit emits for these parameters. Both
  devices pass them through the same kind of unit, so one trace would settle both.

## Parameter tables

The tables list every device-specific member in document order (REQ-002), one row per
instance, plain fields included. Classes: Float = `TimeableFloat`, Enum = `TimeableEnum`,
Bool = `TimeableBool`; Plain integer, Plain text and Plain Boolean are the plain fields of
REQ-011 (schema `RemoteableInt`, `RemoteableString`, `RemoteableBool`). For a parameter
the third column is the stored domain, `Min..Max` of the unmapped `MidiControllerRange`;
for a plain field it is the text shipped device presets store (REQ-011 lists the
exceptions in other documents). "Default when absent" is written as REQ-005 writes it;
for a plain field it is the value the constructor sets, or "not traced". The last column
gives the shipped Defaults-preset value where it differs (REQ-009). Counts: Amp 9,
Cabinet 5, Analog 171 parameters and 7 plain fields, Tension 107 and 3, Collision 139 and
3, Electric 33, Corpus 38 and 7. Labels: D for paths, classes, order, domains and plain
texts; S (A1) for defaults.

### Amp (`Amp`)

| Path below the device element | Class | Stored domain or text | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `AmpType` | Enum | 0..6 | 2 | |
| `Bass` | Float | 0..10 | 5 | |
| `Middle` | Float | 0..10 | 5 | |
| `Treble` | Float | 0..10 | 5 | |
| `Presence` | Float | 0..10 | 5 | |
| `Gain` | Float | 0..10 | 5 | |
| `Volume` | Float | 0..10 | 9 | |
| `DualMono` | Bool | true/false | false | |
| `DryWet` | Float | 0..1 | 1 | |

### Cabinet (`Cabinet`)

| Path below the device element | Class | Stored domain or text | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `CabinetType` | Enum | 0..4 | 0 | |
| `MicrophoneTypeSwitch` | Bool | true/false | false | |
| `MicrophonePosition` | Enum | 0..2 | 0 | |
| `DualMono` | Bool | true/false | false | |
| `DryWet` | Float | 0..1 | 1 | |

### Analog (`UltraAnalog`)

| Path below the device element | Class | Stored domain or text | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `Polyphony` | Enum | 0..9 | 3 | |
| `PitchBendRange` | Float | 0..1 | 0.1666666716 | |
| `Volume` | Float | 0..1 | 0.7047889829 | |
| `PerNotePitchBendRange` | Float | 0..48, integer steps | 0 | 48 |
| `ChannelPressureTarget1` | Enum | 0..46 | 0 | |
| `ChannelPressureAmount1` | Float | -1..1 | 0.5 | |
| `ChannelPressureTarget2` | Enum | 0..46 | 0 | |
| `ChannelPressureAmount2` | Float | -1..1 | 0.5 | |
| `MpeCC74Target1` | Enum | 0..46 | 0 | |
| `MpeCC74Amount1` | Float | -1..1 | 0.5 | |
| `MpeCC74Target2` | Enum | 0..46 | 0 | |
| `MpeCC74Amount2` | Float | -1..1 | 0.5 | |
| `Octave` | Float | -3..3, integer steps | 0 | |
| `OctaveRelativePosition` | Plain integer | `-1073741824` | -1073741824 | |
| `Transpose` | Float | -12..12, integer steps | 0 | |
| `TransposeRelativePosition` | Plain integer | `-1073741824` | -1073741824 | |
| `KeyboardFineTune` | Float | 0..1 | 0.5 | |
| `KeyboardUnisonToggle` | Bool | true/false | false | |
| `KeyboardUnison` | Enum | 0..1 | 0 | |
| `KeyboardDetune` | Float | 0..1 | 0 | |
| `KeyboardUnisonDelay` | Float | 0..1 | 0 | |
| `KeyboardPriority` | Enum | 0..2 | 2 | |
| `KeyboardStretch` | Float | 0..1 | 0.5 | |
| `KeyboardError` | Float | 0..1 | 0 | |
| `VibratoToggle` | Bool | true/false | false | |
| `VibratoSpeed` | Float | 0..1 | 0.5 | |
| `VibratoFadeIn` | Float | 0..1 | 0 | |
| `VibratoAmount` | Float | 0..1 | 0 | |
| `VibratoError` | Float | 0..1 | 0 | |
| `VibratoDelay` | Float | 0..1 | 0 | |
| `VibratoModWheel` | Float | 0..1 | 0 | |
| `PortamentoToggle` | Bool | true/false | false | |
| `PortamentoTime` | Float | 0..1 | 0.5 | |
| `PortamentoMode` | Enum | 0..1 | 0 | |
| `PortamentoLegato` | Bool | true/false | false | |
| `NoiseToggle` | Bool | true/false | false | |
| `NoiseColor` | Float | 0..1 | 0.5 | |
| `NoiseBalance` | Float | 0..1 | 0.5 | 1 |
| `NoiseLevel` | Float | 0..1 | 0.8062000275 | |
| `SignalChain1/OscillatorToggle` | Bool | true/false | true | |
| `SignalChain1/OscillatorWaveShape` | Enum | 0..3 | 1 | |
| `SignalChain1/OscillatorOct` | Float | -3..3, integer steps | 0 | |
| `SignalChain1/OscillatorOctRelativePosition` | Plain integer | `-1073741824` | not traced | |
| `SignalChain1/OscillatorSemi` | Float | -12..12, integer steps | 0 | |
| `SignalChain1/OscillatorSemiRelativePosition` | Plain integer | `-1073741824` | not traced | |
| `SignalChain1/OscillatorMode` | Enum | 0..1 | 0 | |
| `SignalChain1/OscillatorEnvTime` | Float | 0..1 | 0.5 | |
| `SignalChain1/OscillatorDetune` | Float | 0..1 | 0.5 | |
| `SignalChain1/OscillatorModulation1` | Float | 0..1 | 0.5 | |
| `SignalChain1/OscillatorPulseWidth` | Float | 0..1 | 0.5 | |
| `SignalChain1/OscillatorSubAmount` | Float | 0..1 | 0 | |
| `SignalChain1/OscillatorBalance` | Float | 0..1 | 0.5 | 1 |
| `SignalChain1/OscillatorEnvAmount` | Float | -1..1 | 0 | |
| `SignalChain1/OscillatorLFOModPitch` | Float | -1..1 | 0 | |
| `SignalChain1/OscillatorLFOModPW` | Float | -1..1 | 0 | |
| `SignalChain1/OscillatorLevel` | Float | 0..1 | 0.8062000275 | |
| `SignalChain1/FilterToggle` | Bool | true/false | false | true |
| `SignalChain1/FilterType` | Enum | 0..9 | 0 | 1 |
| `SignalChain1/FilterDrive` | Enum | 0..6 | 0 | 1 |
| `SignalChain1/FilterKbdCutoffMod` | Float | -1..1 | 0 | |
| `SignalChain1/FilterCutoffFrequency` | Float | 0..1 | 1 | |
| `SignalChain1/FilterKbdQMod` | Float | -1..1 | 0 | |
| `SignalChain1/FilterQFactor` | Float | 0..1 | 0 | |
| `SignalChain1/FilterLFOCutoffMod` | Float | -1..1 | 0 | |
| `SignalChain1/FilterEnvCutoffMod` | Float | -1..1 | 0 | 0.7047610879 |
| `SignalChain1/FilterLFOQMod` | Float | -1..1 | 0 | |
| `SignalChain1/FilterEnvQMod` | Float | -1..1 | 0 | |
| `SignalChain1/AmplifierToggle` | Bool | true/false | true | |
| `SignalChain1/AmplifierKbdAmpMod` | Float | -1..1 | 0 | |
| `SignalChain1/AmplifierLevel` | Float | 0..1 | 0.8690000176 | 0.474311769 |
| `SignalChain1/AmplifierKbdPanMod` | Float | -1..1 | 0 | |
| `SignalChain1/AmplifierPan` | Float | 0..1 | 0.5 | |
| `SignalChain1/AmplifierLFOAmpMod` | Float | -1..1 | 0 | |
| `SignalChain1/AmplifierLFOPanMod` | Float | -1..1 | 0 | |
| `SignalChain1/AmplifierEnvPanMod` | Float | -1..1 | 0 | |
| `SignalChain1/LFOToggle` | Bool | true/false | false | |
| `SignalChain1/LFOWaveShape` | Enum | 0..4 | 0 | |
| `SignalChain1/LFOSync` | Float | 0..23, integer steps | 13 | |
| `SignalChain1/LFOSyncToggle` | Enum | 0..1 | 0 | |
| `SignalChain1/LFOGateReset` | Bool | true/false | false | |
| `SignalChain1/LFOPulseWidth` | Float | 0..1 | 0.5 | |
| `SignalChain1/LFOSpeed` | Float | 0..1 | 0.5 | |
| `SignalChain1/LFOPhase` | Float | 0..1 | 0 | |
| `SignalChain1/LFODelay` | Float | 0..1 | 0 | |
| `SignalChain1/LFOFadeIn` | Float | 0..1 | 0 | |
| `SignalChain1/Envelope.0/ExponentialSlope` | Bool | true/false | true | |
| `SignalChain1/Envelope.0/Loop` | Enum | 0..3 | 0 | |
| `SignalChain1/Envelope.0/FreeRun` | Bool | true/false | false | |
| `SignalChain1/Envelope.0/Legato` | Bool | true/false | false | |
| `SignalChain1/Envelope.0/AttackMod` | Float | 0..1 | 0 | |
| `SignalChain1/Envelope.0/AttackTime` | Float | 0..1 | 0 | |
| `SignalChain1/Envelope.0/DecayTime` | Float | 0..1 | 0.6000000238 | |
| `SignalChain1/Envelope.0/AmpMod` | Float | 0..1 | 0 | |
| `SignalChain1/Envelope.0/SustainLevel` | Float | 0..1 | 0 | 0.5 |
| `SignalChain1/Envelope.0/SustainTime` | Float | 0..1 | 1 | |
| `SignalChain1/Envelope.0/ReleaseTime` | Float | 0..1 | 0.6000000238 | 0.4847841263 |
| `SignalChain1/Envelope.1/ExponentialSlope` | Bool | true/false | true | |
| `SignalChain1/Envelope.1/Loop` | Enum | 0..3 | 0 | |
| `SignalChain1/Envelope.1/FreeRun` | Bool | true/false | false | |
| `SignalChain1/Envelope.1/Legato` | Bool | true/false | false | |
| `SignalChain1/Envelope.1/AttackMod` | Float | 0..1 | 0 | |
| `SignalChain1/Envelope.1/AttackTime` | Float | 0..1 | 0 | |
| `SignalChain1/Envelope.1/DecayTime` | Float | 0..1 | 0.6000000238 | |
| `SignalChain1/Envelope.1/AmpMod` | Float | 0..1 | 0 | 0.5 |
| `SignalChain1/Envelope.1/SustainLevel` | Float | 0..1 | 0 | 0.5 |
| `SignalChain1/Envelope.1/SustainTime` | Float | 0..1 | 1 | |
| `SignalChain1/Envelope.1/ReleaseTime` | Float | 0..1 | 0.6000000238 | 0.5718053579 |
| `SignalChain1/FilterToFilter2` | Float | 0..1 | 0 | 1 |
| `SignalChain2/OscillatorToggle` | Bool | true/false | false | true |
| `SignalChain2/OscillatorWaveShape` | Enum | 0..3 | 1 | |
| `SignalChain2/OscillatorOct` | Float | -3..3, integer steps | 0 | |
| `SignalChain2/OscillatorOctRelativePosition` | Plain integer | `-1073741824` | not traced | |
| `SignalChain2/OscillatorSemi` | Float | -12..12, integer steps | 0 | |
| `SignalChain2/OscillatorSemiRelativePosition` | Plain integer | `-1073741824` | not traced | |
| `SignalChain2/OscillatorMode` | Enum | 0..1 | 0 | |
| `SignalChain2/OscillatorEnvTime` | Float | 0..1 | 0.5 | |
| `SignalChain2/OscillatorDetune` | Float | 0..1 | 0.5 | |
| `SignalChain2/OscillatorModulation1` | Float | 0..1 | 0.5 | |
| `SignalChain2/OscillatorPulseWidth` | Float | 0..1 | 0.5 | |
| `SignalChain2/OscillatorSubAmount` | Float | 0..1 | 0 | |
| `SignalChain2/OscillatorBalance` | Float | 0..1 | 0.5 | 1 |
| `SignalChain2/OscillatorEnvAmount` | Float | -1..1 | 0 | |
| `SignalChain2/OscillatorLFOModPitch` | Float | -1..1 | 0 | |
| `SignalChain2/OscillatorLFOModPW` | Float | -1..1 | 0 | |
| `SignalChain2/OscillatorLevel` | Float | 0..1 | 0.8062000275 | |
| `SignalChain2/FilterToggle` | Bool | true/false | false | |
| `SignalChain2/FilterType` | Enum | 0..9 | 0 | |
| `SignalChain2/FilterDrive` | Enum | 0..6 | 0 | 1 |
| `SignalChain2/FilterKbdCutoffMod` | Float | -1..1 | 0 | |
| `SignalChain2/FilterCutoffFrequency` | Float | 0..1 | 1 | |
| `SignalChain2/FilterKbdQMod` | Float | -1..1 | 0 | |
| `SignalChain2/FilterQFactor` | Float | 0..1 | 0 | |
| `SignalChain2/FilterLFOCutoffMod` | Float | -1..1 | 0 | |
| `SignalChain2/FilterEnvCutoffMod` | Float | -1..1 | 0 | 0.7047610879 |
| `SignalChain2/FilterLFOQMod` | Float | -1..1 | 0 | |
| `SignalChain2/FilterEnvQMod` | Float | -1..1 | 0 | |
| `SignalChain2/AmplifierToggle` | Bool | true/false | false | |
| `SignalChain2/AmplifierKbdAmpMod` | Float | -1..1 | 0 | |
| `SignalChain2/AmplifierLevel` | Float | 0..1 | 0.8690000176 | 0.474311769 |
| `SignalChain2/AmplifierKbdPanMod` | Float | -1..1 | 0 | |
| `SignalChain2/AmplifierPan` | Float | 0..1 | 0.5 | |
| `SignalChain2/AmplifierLFOAmpMod` | Float | -1..1 | 0 | |
| `SignalChain2/AmplifierLFOPanMod` | Float | -1..1 | 0 | |
| `SignalChain2/AmplifierEnvPanMod` | Float | -1..1 | 0 | |
| `SignalChain2/LFOToggle` | Bool | true/false | false | |
| `SignalChain2/LFOWaveShape` | Enum | 0..4 | 0 | |
| `SignalChain2/LFOSync` | Float | 0..23, integer steps | 13 | |
| `SignalChain2/LFOSyncToggle` | Enum | 0..1 | 0 | |
| `SignalChain2/LFOGateReset` | Bool | true/false | false | |
| `SignalChain2/LFOPulseWidth` | Float | 0..1 | 0.5 | |
| `SignalChain2/LFOSpeed` | Float | 0..1 | 0.5 | |
| `SignalChain2/LFOPhase` | Float | 0..1 | 0 | |
| `SignalChain2/LFODelay` | Float | 0..1 | 0 | |
| `SignalChain2/LFOFadeIn` | Float | 0..1 | 0 | |
| `SignalChain2/Envelope.0/ExponentialSlope` | Bool | true/false | true | |
| `SignalChain2/Envelope.0/Loop` | Enum | 0..3 | 0 | |
| `SignalChain2/Envelope.0/FreeRun` | Bool | true/false | false | |
| `SignalChain2/Envelope.0/Legato` | Bool | true/false | false | |
| `SignalChain2/Envelope.0/AttackMod` | Float | 0..1 | 0 | |
| `SignalChain2/Envelope.0/AttackTime` | Float | 0..1 | 0 | |
| `SignalChain2/Envelope.0/DecayTime` | Float | 0..1 | 0.6000000238 | |
| `SignalChain2/Envelope.0/AmpMod` | Float | 0..1 | 0 | |
| `SignalChain2/Envelope.0/SustainLevel` | Float | 0..1 | 0 | 0.5 |
| `SignalChain2/Envelope.0/SustainTime` | Float | 0..1 | 1 | |
| `SignalChain2/Envelope.0/ReleaseTime` | Float | 0..1 | 0.6000000238 | 0.4847841263 |
| `SignalChain2/Envelope.1/ExponentialSlope` | Bool | true/false | true | |
| `SignalChain2/Envelope.1/Loop` | Enum | 0..3 | 0 | |
| `SignalChain2/Envelope.1/FreeRun` | Bool | true/false | false | |
| `SignalChain2/Envelope.1/Legato` | Bool | true/false | false | |
| `SignalChain2/Envelope.1/AttackMod` | Float | 0..1 | 0 | |
| `SignalChain2/Envelope.1/AttackTime` | Float | 0..1 | 0 | |
| `SignalChain2/Envelope.1/DecayTime` | Float | 0..1 | 0.6000000238 | |
| `SignalChain2/Envelope.1/AmpMod` | Float | 0..1 | 0 | 0.5 |
| `SignalChain2/Envelope.1/SustainLevel` | Float | 0..1 | 0 | 0.5 |
| `SignalChain2/Envelope.1/SustainTime` | Float | 0..1 | 1 | |
| `SignalChain2/Envelope.1/ReleaseTime` | Float | 0..1 | 0.6000000238 | 0.5718053579 |
| `SignalChain2/FilterControllee` | Bool | true/false | false | |
| `SelectedFinger` | Plain integer | `7` | 7 | |

### Tension (`StringStudio`)

| Path below the device element | Class | Stored domain or text | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `Polyphony` | Enum | 0..9 | 4 | |
| `PitchBendRange` | Float | 0..12, integer steps | 2 | |
| `Octave` | Float | -3..3, integer steps | 0 | |
| `OctaveRelativePosition` | Plain integer | `-1073741824` | -1073741824 | |
| `Transpose` | Float | -12..12, integer steps | 0 | |
| `TransposeRelativePosition` | Plain integer | `-1073741824` | -1073741824 | |
| `KeyboardFineTune` | Float | 0..1 | 0.5 | |
| `KeyboardPriority` | Enum | 0..2 | 0 | |
| `KeyboardUnisonToggle` | Bool | true/false | false | |
| `KeyboardUnison` | Enum | 0..1 | 0 | |
| `KeyboardDetune` | Float | 0..1 | 0.5 | 0 |
| `KeyboardUnisonDelay` | Float | 0..1 | 0.5 | |
| `KeyboardStretch` | Float | 0..1 | 0.5 | |
| `KeyboardError` | Float | 0..1 | 0 | |
| `VibratoToggle` | Bool | true/false | false | |
| `VibratoSpeed` | Float | 0..1 | 0.5 | |
| `VibratoFadeIn` | Float | 0..1 | 0.5 | |
| `VibratoAmount` | Float | 0..1 | 0.5 | |
| `VibratoError` | Float | 0..1 | 0.5 | |
| `VibratoDelay` | Float | 0..1 | 0.5 | |
| `VibratoModWheel` | Float | 0..1 | 0.5 | |
| `PortamentoToggle` | Bool | true/false | false | |
| `PortamentoTime` | Float | 0..1 | 0.5 | |
| `PortamentoProportional` | Bool | true/false | false | |
| `PortamentoLegato` | Bool | true/false | false | |
| `GeoExcitatorPosition` | Float | 0..1 | 0.5 | |
| `GeoExcitatorAbsolute` | Bool | true/false | false | |
| `GeoExcitatorKbdModulation` | Float | -1..1 | 0 | |
| `GeoExcitatorVelModulation` | Float | -1..1 | 0 | |
| `GeoDamperPosition` | Float | 0..1 | 0.5 | |
| `GeoDamperAbsolute` | Bool | true/false | false | |
| `GeoDamperKbdModulation` | Float | -1..1 | 0 | |
| `GeoDamperVelModulation` | Float | -1..1 | 0 | |
| `ExcitatorToggle` | Bool | true/false | true | |
| `ExcitatorType` | Enum | 0..3 | 3 | |
| `ExcitatorParameterX` | Float | 0..1 | 0.75 | 0.5 |
| `ExcitatorParameterXKbdMod` | Float | -1..1 | 0 | |
| `ExcitatorParameterXVelMod` | Float | -1..1 | 0 | |
| `ExcitatorStiffness` | Float | 0..1 | 0.5 | |
| `ExcitatorStiffnessKbdMod` | Float | -1..1 | 0 | |
| `ExcitatorStiffnessVelMod` | Float | -1..1 | 0 | |
| `ExcitatorVelocity` | Float | 0..1 | 0.5 | |
| `ExcitatorVelocityKbdMod` | Float | -1..1 | 0 | |
| `ExcitatorVelocityVelMod` | Float | -1..1 | 0 | |
| `ExcitatorDamping` | Float | 0..1 | 0.5 | |
| `PickupToggle` | Bool | true/false | false | |
| `PickupPosition` | Float | 0..1 | 0.5 | |
| `DamperToggle` | Bool | true/false | false | |
| `DamperMass` | Float | 0..1 | 0.5 | |
| `DamperMassKbdMod` | Float | -1..1 | 0 | |
| `DamperStiffness` | Float | 0..1 | 0.5 | |
| `DamperStiffnessKbdMod` | Float | -1..1 | 0 | |
| `DamperVelocity` | Float | 0..1 | 0.5 | |
| `DamperVelocityKbdMod` | Float | -1..1 | 0 | |
| `DamperDamping` | Float | 0..1 | 0.5 | |
| `DamperGated` | Bool | true/false | false | |
| `StringDamping` | Float | 0..1 | 0.5 | |
| `StringDampingKbdMod` | Float | -1..1 | 0 | |
| `StringDecay` | Float | 0..1 | 0.75 | 1 |
| `StringDecayKbdMod` | Float | -1..1 | 0 | |
| `StringDecayRatio` | Float | 0..1 | 0.5 | |
| `StringInharmonicity` | Float | 0..1 | 0.5 | |
| `TerminationToggle` | Bool | true/false | false | |
| `TerminationFingerStiffness` | Float | 0..1 | 0.5 | |
| `TerminationFingerForce` | Float | 0..1 | 0.5 | |
| `TerminationFingerForceKbdMod` | Float | -1..1 | 0 | |
| `TerminationFingerForceVelMod` | Float | -1..1 | 0 | |
| `TerminationFretStiffness` | Float | 0..1 | 0.5 | |
| `LFOToggle` | Bool | true/false | false | |
| `LFOWaveShape` | Enum | 0..4 | 0 | |
| `LFOSync` | Float | 0..23, integer steps | 13 | |
| `LFOSyncToggle` | Enum | 0..1 | 0 | |
| `LFODelay` | Float | 0..1 | 0.5 | |
| `LFOSpeed` | Float | 0..1 | 0.5 | |
| `LFOFadeIn` | Float | 0..1 | 0.5 | |
| `FilterToggle` | Bool | true/false | false | true |
| `FilterType` | Enum | 0..9 | 0 | 1 |
| `FilterCutoffFrequency` | Float | 0..1 | 0.5 | 1 |
| `FilterCutoffFrequencyKbdMod` | Float | -1..1 | 0 | |
| `FilterCutoffFrequencyLFOMod` | Float | -1..1 | 0 | |
| `FilterCutoffFrequencyEnvMod` | Float | -1..1 | 0 | |
| `FilterQFactor` | Float | 0..1 | 0 | |
| `FilterQFactorKbdMod` | Float | -1..1 | 0 | |
| `FilterQFactorLFOMod` | Float | -1..1 | 0 | |
| `FilterQFactorEnvMod` | Float | -1..1 | 0 | |
| `FilterEnvelopeToggle` | Bool | true/false | false | |
| `FilterEnvelopeAttack` | Float | 0..1 | 0 | |
| `FilterEnvelopeDecay` | Float | 0..1 | 0.5 | |
| `FilterEnvelopeSustain` | Float | 0..1 | 0.5 | |
| `FilterEnvelopeRelease` | Float | 0..1 | 0.5 | |
| `FilterEnvelopeAttackMod` | Float | 0..1 | 0 | |
| `FilterEnvelopeAmpMod` | Float | 0..1 | 0 | |
| `BodyToggle` | Bool | true/false | false | |
| `BodyType` | Enum | 0..3 | 0 | |
| `BodySize` | Enum | 0..4 | 2 | |
| `BodyDecay` | Float | 0..1 | 0 | |
| `BodyLowCut` | Float | 0..1 | 0 | |
| `BodyHighCut` | Float | 0..1 | 0 | |
| `BodyLevel` | Float | 0..1 | 0.7049999833 | |
| `BodyMix` | Float | 0..1 | 0.5 | |
| `PerNotePitchBendRange` | Float | 0..48, integer steps | 0 | 48 |
| `ChannelPressureTarget1` | Enum | 0..12 | 0 | 5 |
| `ChannelPressureRange1` | Float | -1..1 | 0.5 | 0.25 |
| `ChannelPressureTarget2` | Enum | 0..12 | 0 | |
| `ChannelPressureRange2` | Float | -1..1 | 0.5 | |
| `SlideTarget1` | Enum | 0..12 | 0 | |
| `SlideRange1` | Float | -1..1 | 0.5 | |
| `SlideTarget2` | Enum | 0..12 | 0 | |
| `SlideRange2` | Float | -1..1 | 0.5 | |
| `CurrentTab` | Plain integer | `0` | 0 | |

### Collision (`Collision`)

| Path below the device element | Class | Stored domain or text | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `Mallet/OnOff` | Bool | true/false | true | |
| `Mallet/Volume` | Float | 0..1 | 0.5 | |
| `Mallet/VelToVolume` | Float | -5..5 | 0 | |
| `Mallet/KeyToVolume` | Float | -2..2 | 0 | |
| `Mallet/Stiffness` | Float | 0..1 | 0.5 | |
| `Mallet/VelToStiffness` | Float | -5..5 | 0 | |
| `Mallet/KeyToStiffness` | Float | -2..2 | 0 | |
| `Mallet/NoiseAmount` | Float | 0..1 | 0.5 | |
| `Mallet/VelToNoiseAmount` | Float | -5..5 | 0 | |
| `Mallet/KeyToNoiseAmount` | Float | -2..2 | 0 | |
| `Mallet/NoiseColor` | Float | 0..1 | 0.5 | |
| `Noise/OnOff` | Bool | true/false | false | |
| `Noise/Volume` | Float | 0..1 | 0.5 | |
| `Noise/VelToVolume` | Float | -5..5 | 0 | |
| `Noise/KeyToVolume` | Float | -2..2 | 0 | |
| `Noise/FilterType` | Enum | 0..3 | 0 | |
| `Noise/Freq` | Float | 0..1 | 0.5 | |
| `Noise/VelToFreq` | Float | -8..8 | 0 | |
| `Noise/KeyToFreq` | Float | -2..2 | 0 | |
| `Noise/EnvToFreq` | Float | -5..5 | 0 | |
| `Noise/Q` | Float | 0..1 | 0 | |
| `Noise/Attack` | Float | 0..1 | 0 | |
| `Noise/Decay` | Float | 0..1 | 0.200000003 | |
| `Noise/Sustain` | Float | 0..1 | 0 | |
| `Noise/Release` | Float | 0..1 | 0.200000003 | |
| `Resonator1/OnOff` | Bool | true/false | false | true |
| `Resonator1/Type` | Enum | 0..6 | 0 | |
| `Resonator1/Quality` | Enum | 0..3 | 2 | |
| `Resonator1/Transpose` | Float | -48..48, integer steps | 0 | |
| `Resonator1/TransposeRelativePosition` | Plain integer | `-1073741824` | -1073741824 | |
| `Resonator1/FineTranspose` | Float | -50..50, integer steps | 0 | |
| `Resonator1/KeyToTranspose` | Float | -2..2 | 1 | |
| `Resonator1/StartTranspose` | Float | -1..1 | 0 | |
| `Resonator1/VelToStartTranspose` | Float | -5..5 | 0 | |
| `Resonator1/StartTime` | Float | 0..1 | 0.5 | |
| `Resonator1/Decay` | Float | 0..1 | 0.5 | |
| `Resonator1/VelToDecay` | Float | -5..5 | 0 | |
| `Resonator1/KeyToDecay` | Float | -2..2 | 0 | |
| `Resonator1/DecayOnNoteOff` | Float | 0..1 | 0 | |
| `Resonator1/Damp` | Float | -1..1 | 0 | |
| `Resonator1/VelToDamp` | Float | -5..5 | 0 | |
| `Resonator1/KeyToDamp` | Float | -2..2 | 0 | |
| `Resonator1/Radius` | Float | 0..1 | 0.5 | |
| `Resonator1/VelToRadius` | Float | -5..5 | 0 | |
| `Resonator1/KeyToRadius` | Float | -2..2 | 0 | |
| `Resonator1/Ratio` | Float | 0..1 | 0 | |
| `Resonator1/AmpFreq` | Float | -1..1 | 0 | |
| `Resonator1/Bleed` | Float | 0..1 | 0 | |
| `Resonator1/Inharmonics` | Float | -1..1 | 0 | |
| `Resonator1/VelToInharmonics` | Float | -5..5 | 0 | |
| `Resonator1/TubeOpening` | Float | 0..1 | 1 | |
| `Resonator1/VelToTubeOpening` | Float | -5..5 | 0 | |
| `Resonator1/HitX` | Float | 0..1 | 0.5 | |
| `Resonator1/RandomToHitX` | Float | 0..1 | 0 | |
| `Resonator1/ListeningXL` | Float | 0..1 | 0.1000000015 | |
| `Resonator1/ListeningXR` | Float | 0..1 | 0.8999999762 | |
| `Resonator1/Pan` | Float | -1..1 | 0 | |
| `Resonator1/KeyToPan` | Float | -1..1 | 0 | |
| `Resonator1/Volume` | Float | 0..1 | 0.5 | |
| `Resonator2/OnOff` | Bool | true/false | false | |
| `Resonator2/Type` | Enum | 0..6 | 0 | |
| `Resonator2/Quality` | Enum | 0..3 | 2 | |
| `Resonator2/Transpose` | Float | -48..48, integer steps | 0 | |
| `Resonator2/TransposeRelativePosition` | Plain integer | `-1073741824` | -1073741824 | |
| `Resonator2/FineTranspose` | Float | -50..50, integer steps | 0 | |
| `Resonator2/KeyToTranspose` | Float | -2..2 | 1 | |
| `Resonator2/StartTranspose` | Float | -1..1 | 0 | |
| `Resonator2/VelToStartTranspose` | Float | -5..5 | 0 | |
| `Resonator2/StartTime` | Float | 0..1 | 0.5 | |
| `Resonator2/Decay` | Float | 0..1 | 0.5 | |
| `Resonator2/VelToDecay` | Float | -5..5 | 0 | |
| `Resonator2/KeyToDecay` | Float | -2..2 | 0 | |
| `Resonator2/DecayOnNoteOff` | Float | 0..1 | 0 | |
| `Resonator2/Damp` | Float | -1..1 | 0 | |
| `Resonator2/VelToDamp` | Float | -5..5 | 0 | |
| `Resonator2/KeyToDamp` | Float | -2..2 | 0 | |
| `Resonator2/Radius` | Float | 0..1 | 0.5 | |
| `Resonator2/VelToRadius` | Float | -5..5 | 0 | |
| `Resonator2/KeyToRadius` | Float | -2..2 | 0 | |
| `Resonator2/Ratio` | Float | 0..1 | 0 | |
| `Resonator2/AmpFreq` | Float | -1..1 | 0 | |
| `Resonator2/Bleed` | Float | 0..1 | 0 | |
| `Resonator2/Inharmonics` | Float | -1..1 | 0 | |
| `Resonator2/VelToInharmonics` | Float | -5..5 | 0 | |
| `Resonator2/TubeOpening` | Float | 0..1 | 1 | |
| `Resonator2/VelToTubeOpening` | Float | -5..5 | 0 | |
| `Resonator2/HitX` | Float | 0..1 | 0.5 | |
| `Resonator2/RandomToHitX` | Float | 0..1 | 0 | |
| `Resonator2/ListeningXL` | Float | 0..1 | 0.1000000015 | |
| `Resonator2/ListeningXR` | Float | 0..1 | 0.8999999762 | |
| `Resonator2/Pan` | Float | -1..1 | 0 | |
| `Resonator2/KeyToPan` | Float | -1..1 | 0 | |
| `Resonator2/Volume` | Float | 0..1 | 0.5 | |
| `ResonatorOrder` | Enum | 0..1 | 0 | |
| `Lfo1/OnOff` | Bool | true/false | false | |
| `Lfo1/Type` | Enum | 0..6 | 0 | |
| `Lfo1/Retrigger` | Bool | true/false | true | |
| `Lfo1/Sync` | Enum | 0..1 | 0 | |
| `Lfo1/Rate` | Float | 0..1 | 0.5 | |
| `Lfo1/SyncRate` | Float | 0..21, integer steps | 4 | |
| `Lfo1/KeyToRate` | Float | -2..2 | 0 | |
| `Lfo1/Phase` | Float | 0..360 | 0 | |
| `Lfo1/Amount` | Float | 0..1 | 0.5 | |
| `Lfo1/VelToAmount` | Float | -5..5 | 0 | |
| `Lfo1/Target1/Target` | Enum | 0..16 | 0 | |
| `Lfo1/Target1/Amount` | Float | -5..5 | 2.5 | |
| `Lfo1/Target2/Target` | Enum | 0..16 | 0 | |
| `Lfo1/Target2/Amount` | Float | -5..5 | 2.5 | |
| `Lfo2/OnOff` | Bool | true/false | false | |
| `Lfo2/Type` | Enum | 0..6 | 0 | |
| `Lfo2/Retrigger` | Bool | true/false | true | |
| `Lfo2/Sync` | Enum | 0..1 | 0 | |
| `Lfo2/Rate` | Float | 0..1 | 0.5 | |
| `Lfo2/SyncRate` | Float | 0..21, integer steps | 4 | |
| `Lfo2/KeyToRate` | Float | -2..2 | 0 | |
| `Lfo2/Phase` | Float | 0..360 | 0 | |
| `Lfo2/Amount` | Float | 0..1 | 0.5 | |
| `Lfo2/VelToAmount` | Float | -5..5 | 0 | |
| `Lfo2/Target1/Target` | Enum | 0..16 | 0 | |
| `Lfo2/Target1/Amount` | Float | -5..5 | 2.5 | |
| `Lfo2/Target2/Target` | Enum | 0..16 | 0 | |
| `Lfo2/Target2/Amount` | Float | -5..5 | 2.5 | |
| `PitchBendRange` | Float | 0..24, integer steps | 5 | |
| `PitchBendTarget1/Target` | Enum | 0..17 | 0 | |
| `PitchBendTarget1/Amount` | Float | -5..5 | 2.5 | |
| `ModWheelTarget1/Target` | Enum | 0..17 | 0 | |
| `ModWheelTarget1/Amount` | Float | -5..5 | 2.5 | |
| `ModWheelTarget2/Target` | Enum | 0..17 | 0 | |
| `ModWheelTarget2/Amount` | Float | -5..5 | 2.5 | |
| `ChannelPressureTarget1/Target` | Enum | 0..17 | 0 | |
| `ChannelPressureTarget1/Amount` | Float | -5..5 | 2.5 | |
| `ChannelPressureTarget2/Target` | Enum | 0..17 | 0 | |
| `ChannelPressureTarget2/Amount` | Float | -5..5 | 2.5 | |
| `Polyphony` | Enum | 0..8 | 2 | |
| `Retrigger` | Bool | true/false | false | |
| `Volume` | Float | 0..1 | 0.7047892213 | |
| `PerNotePitchBendRange` | Float | 0..48, integer steps | 0 | 48 |
| `MpeCC74Target1/Target` | Enum | 0..17 | 0 | |
| `MpeCC74Target1/Amount` | Float | -5..5 | 2.5 | |
| `MpeCC74Target2/Target` | Enum | 0..17 | 0 | |
| `MpeCC74Target2/Amount` | Float | -5..5 | 2.5 | |
| `CurrentTab` | Plain integer | `0` | 0 | |

### Electric (`LoungeLizard`)

| Path below the device element | Class | Stored domain or text | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `Polyphony` | Enum | 0..30 | 30 | |
| `PitchBendRange` | Float | 0..1 | 1 | |
| `PerNotePitchBendRange` | Float | 0..48, integer steps | 0 | |
| `Volume` | Float | 0..1 | 0.7047892213 | |
| `KeyboardTranspose` | Float | 0..24, integer steps | 12 | |
| `KeyboardFineTune` | Float | 0..1 | 0.5 | |
| `KeyboardStretch` | Float | 0..1 | 0.5 | |
| `MalletStiffness` | Float | 0..1 | 0.5 | |
| `MalletStiffnessKeyboard` | Float | 0..1 | 0.5 | |
| `MalletStiffnessVelocity` | Float | 0..1 | 0.5 | |
| `MalletForceStrength` | Float | 0..1 | 0.5 | |
| `MalletForceKeyboard` | Float | 0..1 | 0.5 | |
| `MalletForceVelocity` | Float | 0..1 | 0.5 | |
| `MalletNoisePitch` | Float | 0..1 | 0.5 | |
| `MalletNoiseDecay` | Float | 0..1 | 0.5 | |
| `MalletNoiseAmount` | Float | 0..1 | 0.5 | |
| `MalletNoiseKeyboardScaling` | Float | 0..1 | 0.5 | |
| `ForkReleaseTime` | Float | 0..1 | 0.5 | |
| `ForkTineDecay` | Float | 0..1 | 0.5 | |
| `ForkTineVolume` | Float | 0..1 | 0.5 | |
| `ForkTineKeyboardScaling` | Float | 0..1 | 0.5 | |
| `ForkTineColor` | Float | 0..1 | 0.5 | |
| `ForkToneBarDecay` | Float | 0..1 | 0.5 | |
| `ForkToneBarVolume` | Float | 0..1 | 0.5 | |
| `PickupSymmetry` | Float | 0..1 | 0.5 | |
| `PickupDistance` | Float | 0..1 | 0.5 | |
| `PickupModel` | Enum | 0..1 | 0 | |
| `PickupAmpIn` | Float | 0..1 | 0.5 | 0.4199999869 |
| `PickupAmpOut` | Float | 0..1 | 0.5 | 0.4199999869 |
| `PickupAmpKeyboardScaling` | Float | 0..1 | 0.5 | |
| `DamperTone` | Float | 0..1 | 0.5 | |
| `DamperAmount` | Float | 0..1 | 0.5 | |
| `DamperBalance` | Float | 0..1 | 0.5 | |

### Corpus (`Corpus`)

| Path below the device element | Class | Stored domain or text | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `SideChain/RoutedInput/Routable/Target` | Plain text | `MidiIn/None` | not traced | |
| `SideChain/RoutedInput/Routable/UpperDisplayString` | Plain text | `No Output` | not traced | |
| `SideChain/RoutedInput/Routable/LowerDisplayString` | Plain text | `""` (empty) | not traced | |
| `SideChain/RoutedInput/Routable/MpeSettings/ZoneType` | Plain integer | `0` | not traced | |
| `SideChain/RoutedInput/Routable/MpeSettings/FirstNoteChannel` | Plain integer | `1` | not traced | |
| `SideChain/RoutedInput/Routable/MpeSettings/LastNoteChannel` | Plain integer | `15` | not traced | |
| `SideChain/RoutedInput/Routable/MpePitchBendUsesTuning` | Plain Boolean | `true` | not traced | |
| `ResonanceType` | Enum | 0..6 | 0 | |
| `ResonatorQuality` | Enum | 0..3 | 2 | |
| `Frequency` | Float | 0..1 | 0.5 | |
| `Transpose` | Float | -48..48, integer steps | 0 | |
| `FineTranspose` | Float | -50..50, integer steps | 0 | |
| `Detune` | Float | -1..1 | 0 | |
| `Decay` | Float | 0..1 | 0.5 | |
| `FreqDamping` | Float | -1..1 | 0 | |
| `Radius` | Float | 0..1 | 0.5 | |
| `AmpFreq` | Float | -1..1 | 0 | |
| `Inharmonics` | Float | -1..1 | 0 | |
| `TubeOpening` | Float | 0..1 | 1 | |
| `Ratio` | Float | 0..1 | 0.5 | |
| `ExcitationX` | Float | 0..1 | 0.5 | |
| `ListeningXL` | Float | 0..1 | 0.1000000015 | |
| `ListeningXR` | Float | 0..1 | 0.8999999762 | |
| `LfoOnOff` | Bool | true/false | false | |
| `LfoType` | Enum | 0..6 | 0 | |
| `LfoSync` | Enum | 0..1 | 0 | |
| `LfoRate` | Float | 0..1 | 0.5 | |
| `LfoSyncRate` | Float | 0..21, integer steps | 4 | |
| `LfoStereoMode` | Enum | 0..1 | 0 | |
| `LfoSpin` | Float | 0..0.5 | 0 | |
| `LfoPhase` | Float | 0..360 | 180 | |
| `LfoOffset` | Float | 0..360 | 0 | |
| `LfoAmount` | Float | 0..1 | 0 | |
| `FilterOn` | Bool | true/false | false | |
| `FilterMidFreq` | Float | 50..18000 | 1000 | |
| `FilterBandWidth` | Float | 0.5..9 | 4 | |
| `MidiPitch` | Bool | true/false | false | |
| `MidiMode` | Enum | 0..1 | 0 | |
| `PitchBendRange` | Float | 0..24, integer steps | 5 | |
| `MidiGate` | Bool | true/false | false | |
| `DecayOnNoteOff` | Float | 0..1 | 0 | |
| `Drive` | Float | 0..1 | 0.5 | |
| `StereoWidth` | Float | 0..1 | 1 | |
| `Bleed` | Float | 0..1 | 0 | |
| `DryWet` | Float | 0..1 | 0.5 | |

## Timing and state

- Persistent state: the parameter values, their ranges and target identifiers, and the
  plain fields of REQ-011. Nothing here depends on time, tempo or transport state.
- Units: the stored numbers carry no units; Hz, semitones and degrees are implied by
  some domains (Corpus `FilterMidFreq` 50..18000, `Transpose` −48..48, `LfoPhase`
  0..360) but display units are out of scope.
- Determinism: loading and the save text of REQ-005 are deterministic for a given
  document. Comparisons can be exact per attribute value.
- Interactions: REQ-004, 005 and 011 reuse the transport-state text and unknown-element
  rules; REQ-001 depends on SPEC-ALS-CONTAINER for the document envelope. Automation of
  these parameters is out of scope (no shipped envelope targets them).
- Undo, live edits and engine behavior are out of scope.

## Acceptance cases

All expectations are static derivations or shipped bytes; none has been run, and under
ADR 0003 none will be run against Live. Kinds:
P positive, N negative or malformed, B boundary or out of range, M missing, S save,
U unresolved (not graded).

### Fixtures

| ID | Shipped document | SHA-256 | Content used (D) |
| --- | --- | --- | --- |
| F1 | `Core Library/Defaults/Instruments/Analog.adv` | `87b750c9c2f7bee20c7d9549c69e8fac371a79c6795bcad240203b124de6b0a6` | `UltraAnalog`; `Polyphony` 3, `PitchBendRange` `0.1666666716`, `SignalChain1/Envelope.0/DecayTime` `0.6000000238`, `SignalChain1/Envelope.0/ReleaseTime` `0.4847841263`, `SignalChain2/OscillatorToggle` `true`, `OctaveRelativePosition` `-1073741824`, `SelectedFinger` 7 |
| F2 | `Core Library/Defaults/Instruments/Tension.adv` | `a597bb50a545a46195eaa345874926cf3b6795f81fd9bdf3af7c5c61be1bad35` | `StringStudio`; `PitchBendRange` 2, `ExcitatorType` 3, `LFOSync` 13, `CurrentTab` 0 |
| F3 | `Core Library/Defaults/Instruments/Collision.adv` | `7b8be93e2595b7cbb4a9c835a1ffcb5df51d2577f6c1ba28e374d1b6ee995d3b` | `Collision`; `Resonator1/Quality` 2, `Resonator1/OnOff` `true`, `Resonator1/Transpose` 0, `Lfo1/SyncRate` 4, `PerNotePitchBendRange` 48 |
| F4 | `Core Library/Defaults/Instruments/Electric.adv` | `4634fa6dbfc9c49467ca41255e73f48e26a6af4e43414a4114c424350de7e9b7` | `LoungeLizard`; `KeyboardTranspose` 12, `PickupAmpIn` `0.4199999869`, `Polyphony` 30 |
| F5 | `Core Library/Devices/Audio Effects/Amp/Clean.adv` | `6b4b56ee7db287a06f53d6c716b487d1ad24006aab828a4df65281b277e27855` | `Amp`; `AmpType` 0, `Bass` 5, `Gain` `5.98425198`, `DualMono` `false`, `DryWet` 1 |
| F6 | `Core Library/Devices/Audio Effects/Cabinet/1x12 Cab.adv` | `e015c623e60d3ad0f857ee56305af9636121495b9af212ce15c93123343e7200` | `Cabinet`; `CabinetType` 0, `MicrophoneTypeSwitch` `false`, `MicrophonePosition` 0 |
| F7 | `Core Library/Devices/Audio Effects/Corpus/Pipe Resonator.adv` | `d402e8f81caeb3bf708033878c02063ba61cc7ff2ad31a9d3226237d26eff184` | `Corpus`; `ResonanceType` 5, `Transpose` 12, `FilterMidFreq` 1000, `LfoPhase` 180 |

Paths are relative to `Contents/App-Resources/` of the 12.4.3 bundle. All seven use
`MinorVersion="12.0_12402"`. A fixture is decoded, changed only as stated, and
re-encoded as gzip. "Open" means opening the preset in a new Live Set's track; "save"
means saving the device as a new `.adv` and decoding it. Unless a case says otherwise the
comparator is the named attribute text in the saved file.

### Cases

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Fixture |
| --- | --- | --- | --- | --- | --- |
| BDP-001 | 001, 003 | P | Open each of F1–F7 | Each opens with the device of its root child; the values listed in the fixture table load | F1–F7 |
| BDP-002 | 005 | S | Open, save | `PitchBendRange` `0.1666666716`, `Envelope.0/DecayTime` `0.6000000238`, `Polyphony` `3`, `SignalChain2/OscillatorToggle` `true` | F1 |
| BDP-003 | 005 | S | Open, save | `Gain` `5.98425198`, `Bass` `5`, `DryWet` `1`, `DualMono` `false` | F5 |
| BDP-004 | 004, 005 | P | `Bass` `<Manual Value="5.5" />`; open, save | Opens; saved `5.5` | F5 edit |
| BDP-005 | 004, 005 | P | `Bass` `<Manual Value="3.3" />`; open, save | Opens; saved `3.29999995` (32-bit rounding, REQ-TRANSPORT-STATE-011) | F5 edit |
| BDP-006 | 004 | N | `Bass` `<Manual Value="abc" />`; open | Does not open | F5 edit |
| BDP-007 | 004 | P | `Bass` `<Manual Value="4.5abc" />`; open, save | Opens; saved `4.5` | F5 edit |
| BDP-008 | 004 | N | `MicrophoneTypeSwitch` `<Manual Value="TRUE" />`; open | Does not open | F6 edit |
| BDP-009 | 004, 005 | P | `MicrophoneTypeSwitch` `<Manual Value="1" />`; open, save | Opens; saved `true` | F6 edit |
| BDP-010 | 004 | N | `Polyphony` `<Manual Value="3.0" />`; open | Does not open | F1 edit |
| BDP-011 | 004 | N | `ResonanceType` `<Manual Value="0x5" />`; open | Does not open | F7 edit |
| BDP-012 | 002 | N | Duplicate the `Bass` element; open | Does not open | F5 edit |
| BDP-013 | 006 | B | `Bass` `<Manual Value="10" />`, then `"0"`; open, save | Opens; saved `10`, `0` | F5 edit |
| BDP-014 | 010 | B | `Bass` `<Manual Value="12" />`; open, save | Opens; displayed and saved value unresolved (REQ-010 U; ADR 0003) | F5 edit |
| BDP-015 | 010 | B | `Polyphony` `<Manual Value="12" />` (domain 0..9); open, save | Opens; display and saved value unresolved (REQ-010 U; ADR 0003) | F1 edit |
| BDP-016 | 010 | B | `FilterMidFreq` `<Manual Value="20" />` (domain 50..18000); open, save | Opens; display and saved value unresolved (REQ-010 U; ADR 0003) | F7 edit |
| BDP-017 | 010 | U | `ResonanceType` `<Manual Value="-1" />`; open | Not graded: whether it opens is open (REQ-TRANSPORT-STATE-006; ADR 0003) | F7 edit |
| BDP-018 | 008 | M | Delete `Resonator1/Quality`; open, save | Opens; saved `Resonator1/Quality/Manual` `2` | F3 edit |
| BDP-019 | 008 | M | Delete `Resonator1/OnOff`; open, save | Opens; saved `false` (the preset had `true`) | F3 edit |
| BDP-020 | 008 | M | Delete `SignalChain1/OscillatorToggle` and `SignalChain2/OscillatorToggle`; open, save | Opens; saved chain 1 `true`, chain 2 `false` | F1 edit |
| BDP-021 | 008, 005 | M | Delete `SignalChain1/Envelope.0/ReleaseTime`; open, save | Opens; saved `0.6000000238` | F1 edit |
| BDP-022 | 008 | M | Delete `PickupAmpIn`; open, save | Opens; saved `0.5` (the preset had `0.4199999869`) | F4 edit |
| BDP-023 | 008 | M | Delete `AmpType` and `Volume`; open, save | Opens; saved `AmpType` `2`, `Volume` `9` | F5 edit |
| BDP-024 | 008 | M | Delete `LfoPhase` and `FilterMidFreq`; open, save | Opens; saved `180` and `1000` | F7 edit |
| BDP-025 | 008 | M | Delete `PitchBendRange` and `ExcitatorParameterX`; open, save | Opens; saved `2` and `0.75` | F2 edit |
| BDP-026 | 008 | M | Delete `Lfo1/SyncRate` and `PerNotePitchBendRange`; open, save | Opens; saved `4` and `0` (the preset had 48) | F3 edit |
| BDP-027 | 008 | M | `Bass` `<Manual />` (no `Value`); open, save | Opens; saved `5` | F5 edit |
| BDP-028 | 007 | B | `Resonator1/Transpose` `<Manual Value="3.7" />`; open, save | Opens; saved text unresolved (REQ-007 U; ADR 0003) | F3 edit |
| BDP-029 | 011 | P | Add `<Foo Value="1" />` as a child of `Amp`; open, save | Opens; saved device has no `Foo` | F5 edit |
| BDP-030 | 011 | P | Add `<Foo Value="1" />` inside `Bass`; open, save | Opens; saved `Bass` has no `Foo` and keeps `5` | F5 edit |
| BDP-031 | 011 | S | Open, save | `OctaveRelativePosition` `-1073741824`, `SelectedFinger` `7` | F1 |
| BDP-032 | 011 | S | Open, save | `CurrentTab` `0` | F2 |
| BDP-033 | 012 | U | Insert F5 into a Live Set, save the set | Not graded: target `Id`s expected nonzero and unique in the set (D pattern), rule unknown (REQ-012 U; ADR 0003) | F5 |
| BDP-034 | 009 | U | Insert Analog, Tension, Collision, Electric, Amp, Cabinet and Corpus from the browser into an empty set; save | Not graded: table defaults or Defaults-preset values (REQ-009 U; ADR 0003) | — |
| BDP-035 | 014 | P | `AmpType` `<Manual Value="4" />`; open | Device shows Lead (A3) | F5 edit |
| BDP-036 | 014 | P | Open | `ResonanceType` shows Pipe (A3) | F7 |
| BDP-037 | 015 | U | `ExcitationX` 0, then 1; open; compare output | Not graded: storage is BDP-013-like; the position effect is unknown (REQ-015 U; ADR 0003) | F7 edit |

Omitted kinds: there is no cancellation or teardown step in loading a single value; a
failed load is covered by the N cases. Enum and Bool boundaries are covered by
BDP-013, 015 and 009. Automation and modulation of these parameters are excluded.

## Open questions

No reference observation is available for any of these ([ADR 0003](../decisions/adr-0003-no-reference-execution.md)).
The last column names the static route that could still settle each one.

| Question | Requirements | Impact | Static route |
| --- | --- | --- | --- |
| Save output of 12.4.3: order, omissions, target `Id`s, ranges of re-created parameters | 001, 002, 008, 012, 013 | Exact file comparison of saved presets and sets | Member writer against each device's registration, for order and omissions; constructor ranges (REQ-006) for re-created parameters; none identified for `Id`s and bindings |
| Value displayed, used and saved after an out-of-range, narrower-range or fractional value | 006, 007, 010 | Round trip of hand-edited or foreign documents | Create path (A1) and device post-load step, for the saved value; none known for the display |
| Defaults of a newly inserted device | 009 | Values of new devices | Insert path, for a read of the Defaults preset |
| Labels of Analog, Tension and Collision; Electric `Voices` display text and Corpus LFO labels | 014 | Display of enum values | Run-time label tables; display of the second name lists and the `Voices` text |
| Meaning of the stored 0..1 positions (contradiction) | 015 | None for storage; sound only | Value emitted by the Live-side float parameter unit |
| Negative Enum text | 010 | Whether such a document opens | Integer text reader, owned by REQ-TRANSPORT-STATE-006 |
| The document create path for device list items (assumption A1) | 007, 008, 010 | All A1 clauses | Trace from the list-item factory |

[Q-006](../questions.md#q-006-native-analysis-and-resource-decoding) tracks the native
analysis behind this page.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical evidence:
[device bundles](../research/device-bundles-static.md) (H4, retained run
`analysis/ableton-live-12.4.3/r2/h4-devices-v1/`),
[device parameter mapping](../research/device-parameter-mapping-native.md) (N5,
`r2/n5-device-mapping-v1/`) and [device tables](../research/device-tables-native.md)
(N6, `r2/n6-device-tables-v1/`). Image `Live.arm64` SHA-256 `3a99ceea…d1c383cfad`, base
`0x100000000`. Revision 2 also cites the v1 review record
`analysis/ableton-live-12.4.3/handoff-staging/bundled-device-parameters-v1-analysis/review/`
(`review-checks.txt` sections 2 and 3, `review-check.json`) and the decompiled arm64
corpus `/var/tmp/sound-analysis/corpus/decomp/chunks/` ("corpus chunk" below, read
2026-10-18). N6 dossiers are cited by query result (`n6-0001` … `n6-0003`); "C1" marks a
record in N6 `out/live_corpus_excerpts.jsonl`. Transport rules come from
[transport-state native](../research/transport-state-native.md) (N1).

| Requirement | Evidence | Strength |
| --- | --- | --- |
| 001 | H4 `out/occurrences.jsonl` (1,064 rows, contexts and depths), `out/scan.json`; element strings in Live (`UltraAnalog` `0x105b9ac34` etc., H4) | D |
| 002 | H4 `out/schema_devices.json` (`device_base_prefix`, 21 fields; `current` device fields in order), `out/params.json` (`distinct_param_path_sets` 1 per device), `out/fields.json`; N6 `registration_classes.json`: `ToggleDummy`, `IsChain2` registered but absent from the schema; add-member check `0x101472624` (N1). Revision 2: analyst re-check 2026-10-18, script not retained, of all 1,064 occurrences in the 599 documents of H4 `out/occurrences.jsonl` (none stores `RemoteSelectionKeyMidi`; members after the shared ones equal `current` in order in every occurrence; no group has attributes); review `shared_member_names` 20. Inferred: the member writer skips an unassigned key-MIDI member (N1 `0x10260dde0`), which would explain the absence | D; S for duplicates |
| 003 | H4 wrapper classes from the schema and 502 parameter rows (`param_table.tsv`); `LomId`, `LockEnvelope` and `Id` 0 in every `.adv` (review `review-checks.txt` section 2) | D |
| 004 | Text converter `0x10152bfb8` and per-type rules (N1, n1-0006); `Tempo/Manual` is `ARemoteableFloat` (`0x1026f0390`) and `TimeSignature/Manual` belongs to `ATimeableEnum` (N1); N6 `loader_slots.txt`: `ATimeableFloat`, `ATimeableEnum`, `ATimeableBool` +0x140 = `0x101487310`, the transport loader | S (A2) |
| 005 | N1 writer rule (`0x101431584`/`0x101431788`); N6 `number_text_check.json`: 114,570 Float, 6,771 Enum, 7,515 Bool texts, 0 mismatches | S (A2); D |
| 006 | H4 modal ranges; N5 constructor arguments (81 stored rows asserted); N6 `conversions_nested.py` asserts converter user domain = modal range for 305 Float parameters; Bool `MidiCCOnOffThresholds` from H4. Revision 2: Amp and Cabinet `DryWet` from `FUN_103197bf8` (converter `FUN_101575868(0, 1.0, …)`, `FUN_1026f0b58(0, 1.0, 1.0, …)`, corpus chunk `chunk-02397`; called in `FUN_1030b4934` and `FUN_1030c9c90`; RVB-04); `.adv` ranges equal the domain (review `adv_range_ne_domain` 0; plan F8); 22 Enum upper bounds never stored (RVB-06, H4 `param_table.tsv`) | D; S |
| 007 | Converters `ALegacyQuantingIntUserFloatConverter` (`0x101577e1c`) and `AQuantizingUserFloatConverter` (`0x101578050`) per N5/N6 `conversions.tsv`; shipped kinds `int` for all 28 (H4 `param_table.tsv`) | S; D |
| 008 | Constructor defaults: N6 `constructors.tsv` (412 of 426 calls re-read in n6-0001/0002 disassembly; fixed default 0.5 of `0x103192a6c` in n6-0003; chain flag from `FUN_1031a7d8c(chain, 0|1, …)` in `0x1031a3acc`), N5 `conversions.py` SPEC and N5 page for Amp/Cabinet `DualMono`/`DryWet`; generic loader visits present members only (N1 `0x101487310`, ✓ n1-0008); missing `Value` on `Tempo/Manual` loads the default (SPEC-TRANSPORT-STATE TS-014) | S (A1) |
| 009 | H4 default-preset values; N6 `spec_defaults.tsv` (`preset_differs`) | D; U |
| 010 | N1: loader stores base-type values without range checks and enum indices directly (`0x101487364`, `0x10156675c` not called); Timeable post-load `0x1026fc4cc` (C1) has no range test | S (A1) |
| 011 | N1 loader skips unknown names; H4 `out/fields.json`; N6 `nonparam_fields.tsv` (setters `0x10156934c`, `0x101568960` in the constructors). Revision 2: stored plain fields from H4 `schema_devices.json` `current`; the constructor-set Collision `PitchBendRangeRelativePosition` and `Lfo*/SyncRateRelative` are absent from the schema and from every document (review `draft_claimed_fields_found` 0; F1); Corpus side chain 36 of 36 with seven fields (review `corpus_sidechain`; F2) | S; D |
| 012 | H4 target counts (37,794 / 13,618; 215 documents; 3,553 envelopes, none on these devices) | D |
| 013 | H4 `KeyMidi` counts (1,672; contexts) | D |
| 014 | N5 constructor label lists (`FUN_1026ef060` label arrays in `0x1030b4934`, `0x1030c9c90`, `0x1030e9578`, `0x1030e277c`, `0x1030e3830`); H4 `out/corpus_resonance.json`. Revision 2: `FUN_1030c9c90` passes `"Dynamic"`, `"Condenser"` to `FUN_102a43394`; `FUN_10143bab0` keeps the first at +0x18 and the second at +0x20; `FUN_10143bb10` returns +0x18 for a nonzero value (corpus chunks `chunk-02350`, `chunk-00780`; RVB-01). `FUN_1030e9578` builds labels `2`…`32` and passes `"Voices"` separately (`chunk-02352`; F4); `FUN_1030e3830` holds `ModulationSine`…, `ModulationHertz`/`ModulationBeat`, `Phi`/`Spin` after the label lists (`chunk-02351`; F5) | S (A3); D; U |
| 015 | N5 position contradiction; N6 cross-check (Collision bundle entries 51, 53, 54, 84, 86, 87 are kind 1 −2..2). 2026-10-22 evidence qualification: the [sole-reviewed five-branch factory study](../research/device-analog-dsp.md#five-branch-factory-source-adoption--2026-10-22) makes the earlier direct AFloat creation association stale; actual class/current receiver and emitted value remain untraced | U |

**Internal mapping (not a requirement).** Each stored parameter reaches the device engine
as an indexed value through Live's mapping. The complete index and conversion tables are
in N5 `out/conversions.tsv` (Amp, Cabinet, Electric, Corpus) and N6 `out/conversions.tsv`
(Analog, Tension, Collision). N6 cross-checks them against the bundles' own tables:
Analog 197 exact and 6 within range; Tension 124 exact, 5 within, 1 unused index; Collision
81 exact, 54 within, 1 unrecovered, 3 mismatches (`Resonator*/VelToStartTranspose`,
`Resonator2/Type`). None of this enters a handoff.

Corrections and contradictions:

- H4 recorded Analog and Tension bipolar ranges as missing from the bundles; N6 shows they
  are sent as magnitude plus sign. H4 DEV-C08 ("new instances take Defaults preset
  values") is downgraded to U in REQ-009, because constructor and preset values differ.
- The constructor default and the shipped Defaults preset disagree for 37 parameters
  (REQ-009). REQ-008 uses the constructor value under A1. No reference observation can
  test A1 (ADR 0003); a trace from the list-item factory could still show that a device
  read from a document is created differently.
- Revision 2 corrects revision 1 after the v1 review: the Cabinet switch labels were
  reversed (RVB-01; the N5 page carried the same error and has a correction note); REQ-011
  listed constructor-set Collision fields as stored (F1; from the N6 non-parameter note,
  now corrected there) and omitted two Corpus side-chain fields (F2); REQ-014 gave inexact
  Electric and Corpus label lists (F4, F5); the envelope count 21 was the schema count,
  while documents store 20 (F7; corrected on the H4 page).
- The Corpus and Collision position contradiction (REQ-015) stays open. Former probe IDs,
  kept in the [probe batch](../research/phase4-probe-batch.md) record only: P4-H4-01 (save
  output), P4-H4-02 (out-of-range, narrower-range and fractional values), P4-H4-03 and
  P4-N5-03 (new-instance defaults), P4-H4-04 (labels), P4-N5-01 and P4-N6-01 (positions),
  PRB-N1-06 (negative Enum text).

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from H4 (DEV-C01 to C10), N5 (DEV-M01 to M10) and N6: 15 requirements (1 D only; 2 D and S; 12 with D or S clauses and U parts; none U only); 37 unexecuted cases, 4 not graded (BDP-017, 033, 034, 037), 4 with unresolved parts (BDP-014–016, 028) |
| 2 | 2026-10-18 | Applies the v1 review findings. Applied: RVB-01 (REQ-014: Cabinet switch true Dynamic, false Condenser; marked not in v1); RVB-02 (REQ-006 value-read clause, positions excluded as in v1; REQ-015); RVB-04 (REQ-006 S: Amp and Cabinet `DryWet` traced, 0..1; 372 of 372 Float); RVB-05 with F1 (REQ-011: unstored Collision fields removed), F2 (seven Corpus side-chain fields), F4 and F5 (Electric `Polyphony` and Corpus `LfoType`, `LfoSync`, `LfoStereoMode` labels moved to U); RVB-06 (REQ-006: 22 Enum domains rest on the stored range); F3 (tables regenerated in document order, one row per instance, plain fields included, cross-checked against H4 `current`, the v1 tables and all 1,064 shipped occurrences); F6 (research note only, N6 page); F7 (REQ-002 and scope: 20 stored envelope members); F8 (REQ-006: no narrower range in `.adv`). A1's dependency list corrected (REQ-006 to 008 and 010, not 009). Also brought into line with v1: REQ-003 plain-field and group shape and `.adv` form, REQ-011 unknown child of a group. RVB-03 and RVB-07 to 09 concern only the release text; none rejected. U clauses, cases and open questions reworded for ADR 0003 with static routes. Counts unchanged: 15 requirements (1 D only; 2 D and S; 12 with D or S clauses and U parts); 37 cases, 4 not graded, 4 with unresolved parts |
| 3 | 2026-10-19 | REQ-014 distinguishes Electric Polyphony's X voice-count meaning (all 31 indices) from the unobserved `Voices` display text. N5's rounded Electric Volume default is corrected in the canonical mapping research to 0.7047892213; the Electric table here already held that value. The t12 peak correction (0.296 with the exact default and settled ramp) is owned by the [Electric research](../research/device-electric-dsp.md#corrections-to-other-pages), not a storage acceptance criterion. 15 requirements and 37 cases remain; no case expectation changes. The current v1 partial release remains immutable and does not include the new Polyphony meaning. |

Before the 2026-10-18 review, a first handoff could carry REQ-001 to 008 and 011 with
the parameter tables, the S and D clauses of REQ-010, 012 and 013, and REQ-014 for Amp,
Cabinet, Electric and Corpus.

Released 2026-10-18: [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md), 82 cases, approved with narrowing by a separate review agent (partial REQ-001 to 004, 006, 007, 011, 012, 014 only; 005, 008 to 010, 013, 015 unreleased). The review findings to apply in the next revision are on the [handoff plan](bundled-device-parameters-handoff-plan.md#review-outcome). Revision 2 applies those review findings.
