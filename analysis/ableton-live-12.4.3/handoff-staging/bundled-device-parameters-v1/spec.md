# Device parameters in device presets, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-DEVICES with FEAT-PERSISTENCE. Parent
specification identity: SPEC-BUNDLED-DEVICE-PARAMETERS revision 1. Release:
bundled-device-parameters-v1. Only the clauses explicitly included below are in
scope. No other clause of a listed requirement is implicitly approved. This
document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the narrowing recorded in [the review disposition](REVIEW.md).
Implementation requires a fresh, restricted implementation workspace.

## What the contract means

A device preset file stores one device with its parameter values. For seven
devices that come with Live (Amp, Cabinet, Analog, Tension, Collision, Electric
and Corpus) and one document format version, this contract describes:

- the element that stores each device in a device preset;
- the members of the device element, their order and the shape of each
  parameter element;
- each parameter's path, kind and value range;
- which value text is accepted or refused when the preset is opened, and the
  value then read;
- what duplicated and unknown elements do;
- the labels the user interface shows for the values of seven parameters.

It does not describe the value of a parameter whose element is missing, the
values a newly inserted device starts with, what happens to a value outside its
parameter's range, anything written when a device is saved, parameters bound to
rack macros or MIDI, how the device sounds, or any other display text.

Every rule and expected result is **documented** or **static-derived**.
Documented means taken from the form of the device presets, racks, clips and
Live Sets shipped with the target build; those documents were not written by a
save of the target build. Static-derived means derived for the target build
without running it. Neither is an observed execution of the original
application, and no case was run against a candidate. No compatibility result
is established. The original application remains the authority for a later
comparison. Some derived steps rest on assumptions that were not traced to the
end:

- a read error anywhere in a device preset stops the preset from opening, as
  it does for a Live Set;
- a value read from the preset is not changed afterwards while the device is
  created;
- the label lists of REQ-BUNDLED-DEVICE-PARAMETERS-014 are the texts the user
  interface shows.

The [comparison obligation](#reference-comparison-obligation-not-executed)
covers them.

## Terms

| Term | Meaning |
| --- | --- |
| Device preset | The decoded XML of a device preset file (`.adv`). The compressed file container is outside this release |
| Device element | The only child of the root element. Its name identifies the device (REQ-BUNDLED-DEVICE-PARAMETERS-001) |
| Member | A child element of the device element or of a group that the [parameter tables](#parameter-tables) list |
| Group | A member that only holds other members, for example `SignalChain1` in Analog. Its members are listed under paths that start with its name |
| Parameter | A member of kind Float, Enum or Bool, with the shape of REQ-BUNDLED-DEVICE-PARAMETERS-003 |
| Plain field | A member that is an empty element with one `Value` attribute and is not a parameter |
| Path | The element names from below the device element to a member, joined by `/`, for example `Resonator1/Quality` in Collision. A `.` belongs to the name: `Envelope.0` is one element |
| Text | An attribute value after standard XML attribute-value decoding |
| Domain | The value range of a parameter as its `MidiControllerRange` stores it in documents of this format version (REQ-BUNDLED-DEVICE-PARAMETERS-006) |
| Value | The value of a parameter: the value read from its `Manual` element |
| Opens | The preset is read without refusal and the device is created from it |
| Refused | No device is created from the preset. How a refusal is reported is excluded |

## Document scope and preconditions

- The input is XML 1.0 in UTF-8, well-formed except in the one case that
  repeats an attribute. Its root element is `Ableton` with exactly the
  attributes `MajorVersion="5"`, `MinorVersion="12.0_12402"` and
  `SchemaChangeCount="1"`, and the device element is its only child. Shipped
  device presets also carry `Creator` and `Revision` root attributes. They are
  outside this release, and the fixtures omit them.
- In shipped documents every device element first holds members that all Live
  devices share, for example the device's on switch, its view state and a
  reference to its preset. They are outside this release. The fixtures omit
  them, and their absence must not by itself change a judged outcome.
- Each fixture contains every member of its device's table exactly once, in
  table order and in the fixture form of REQ-BUNDLED-DEVICE-PARAMETERS-003,
  apart from a duplicated or unknown element that its case's purpose states.
  Expectations exist only for such documents.
- Numbers use `.` as the decimal separator. Expectations assume a host locale
  whose decimal separator is `.`; locale-dependent behavior is excluded.

## Selected requirement clauses

### REQ-BUNDLED-DEVICE-PARAMETERS-001 — partial: device elements and placement

| Device | Device element |
| --- | --- |
| Amp | `Amp` |
| Cabinet | `Cabinet` |
| Analog | `UltraAnalog` |
| Tension | `StringStudio` |
| Collision | `Collision` |
| Electric | `LoungeLizard` |
| Corpus | `Corpus` |

In a device preset the device element is the only child of the root element
`Ableton`. Where the device element sits in racks, Live Sets and clips is not
part of this release.

### REQ-BUNDLED-DEVICE-PARAMETERS-002 — partial: device element content

1. In documents of this format version, a device element holds, after the
   shared members, exactly the members of its device's table, in table order. A
   group holds exactly the members listed under its path, in order, and has no
   attributes.
2. These duplications refuse the preset: two parameters with the same name in
   the device element or in one group; two groups with the same name in one
   parent; two `Manual` elements in one parameter. A repeated attribute makes
   the XML not well-formed, and a preset that is not well-formed XML is
   refused.

### REQ-BUNDLED-DEVICE-PARAMETERS-003 — partial: element shapes

Each parameter element holds these children in order:

| Kind | Children |
| --- | --- |
| Float | `LomId`, `Manual`, `MidiControllerRange` (holding `Min`, `Max`), `AutomationTarget`, `ModulationTarget` |
| Enum | `LomId`, `Manual`, `AutomationTarget`, `MidiControllerRange` (holding `Min`, `Max`) |
| Bool | `LomId`, `Manual`, `AutomationTarget`, `MidiCCOnOffThresholds` (holding `Min`, `Max`) |

- Each value is in the `Value` attribute of an otherwise empty element.
  `AutomationTarget` and `ModulationTarget` carry an `Id` attribute
  (REQ-BUNDLED-DEVICE-PARAMETERS-012) and hold one empty `LockEnvelope`
  element with a `Value` attribute.
- The **fixture form** is the form device presets of this format version store
  for a parameter that is not bound to a rack macro or MIDI: `LomId` 0,
  `LockEnvelope` 0, `Min` and `Max` of `MidiControllerRange` equal to the bounds
  of the parameter's domain, and `MidiCCOnOffThresholds` `Min` 64 and `Max`
  127. Every fixture uses it.
- A plain field is an empty element whose only attribute is `Value`. A group is
  an element without attributes that holds its members.

Example, the Float parameter `Bass` of Amp with value 2.5:

```xml
<Bass>
  <LomId Value="0" />
  <Manual Value="2.5" />
  <MidiControllerRange>
    <Min Value="0" />
    <Max Value="10" />
  </MidiControllerRange>
  <AutomationTarget Id="0">
    <LockEnvelope Value="0" />
  </AutomationTarget>
  <ModulationTarget Id="0">
    <LockEnvelope Value="0" />
  </ModulationTarget>
</Bass>
```

### REQ-BUNDLED-DEVICE-PARAMETERS-004 — partial: value text on load

These rules apply to the text of the `Value` attribute of `Manual`.

**Float.** Leading space characters (U+0020) are skipped. The value is then
read from the longest prefix of the remaining text that forms a decimal number:
an optional `+` or `-`; digits with an optional `.` and fraction digits, at
least one digit in total; and an optional exponent of `e` or `E`, an optional
sign and at least one digit. An exponent marker without digits is not part of
the prefix. Text after the prefix is ignored, so `0.5abc` reads as 0.5. The
decimal prefix is rounded to the nearest IEEE 754 binary64 value, ties to even,
and that value to the nearest binary32 value, ties to even. The binary32 value
is the parameter's value: `0.3` reads as 0.300000011920928955078125. Text
without such a prefix refuses the preset, for example `abc`, `e5` or the empty
string.

**Enum.** The value is a decimal integer.

- Accepted: ASCII digits preceded by any number of spaces and at most one `+`,
  in that order, with nothing after the digits (`3`, ` 3`, `+3`, ` +3`); or
  ASCII digits followed only by spaces (`3 `).
- Refused: text that is empty or only spaces; text with any character outside
  ASCII; text in which, after leading spaces and one leading `+`, the rest is
  empty, starts with `-` after that `+`, contains a character other than an
  ASCII digit (apart from a single leading `-` and trailing spaces), or, when
  the text does not end in a space, is longer than 63 characters. Examples:
  `3.0`, `0x3`, `+-3`.

**Bool.** `true` or `1` reads as true; `false` or `0` reads as false. Matching
is exact and case-sensitive, with no trimming. Any other text refuses the
preset, including `TRUE`, `True`, the empty string and ` true`.

### REQ-BUNDLED-DEVICE-PARAMETERS-006 — partial: domains

1. The domain of a Float or Enum parameter is `Min..Max` of its
   `MidiControllerRange` in the fixture form, as listed in the
   [parameter tables](#parameter-tables), bounds included. An Enum domain
   `0..N-1` has the N values 0 to N-1. A Bool parameter takes false and true.
2. A value within its domain, read by REQ-BUNDLED-DEVICE-PARAMETERS-004, is the
   parameter's value when the preset opens. This clause does not apply to the
   position parameters marked "position" in the tables
   (REQ-BUNDLED-DEVICE-PARAMETERS-015): their values have no expectation.

### REQ-BUNDLED-DEVICE-PARAMETERS-007 — partial: whole-number Float parameters

The Float parameters marked "whole numbers" in the tables hold whole numbers in
documents of this format version. Expectations exist only for whole-number
values of these parameters.

### REQ-BUNDLED-DEVICE-PARAMETERS-011 — partial: unknown elements and plain fields

1. An element whose name the format does not define for its parent, placed as a
   child of the device element, of a group or of a parameter element, is
   skipped together with its content. The preset opens, and every member is
   read as if the element were absent. The cases use the name `Foo`. Names that
   this release does not list but that the original application may define for
   that parent, including the shared members of all devices and `KeyMidi`, are
   not covered by this rule and have no expectation.
2. In documents of this format version the plain fields hold the `Value` texts
   listed in the tables, and the fixtures use them. Their meaning is outside
   this release.

### REQ-BUNDLED-DEVICE-PARAMETERS-012 — partial: target identifiers

The `AutomationTarget` of every parameter and the `ModulationTarget` of every
Float parameter carry an `Id` attribute. Device presets of this format version
store `Id="0"`, and every fixture does. Other identifiers, and how identifiers
are assigned when a document is saved, are outside this release.

### REQ-BUNDLED-DEVICE-PARAMETERS-014 — partial: enumeration labels

The user interface shows these labels for the values of these parameters, in
order from value 0:

- Amp `AmpType`: Clean, Boost, Blues, Rock, Lead, Heavy, Bass.
- Cabinet `CabinetType`: 1x12, 2x12, 4x12, 4x10, 4x10 Bass.
- Cabinet `MicrophonePosition`: Near On-Axis, Near Off-Axis, Far.
- Electric `PickupModel`: R, W.
- Corpus `ResonanceType`: Beam, Marimba, String, Membrane, Plate, Pipe, Tube.
- Corpus `ResonatorQuality`: Eco, Low, Med, High.
- Corpus `MidiMode`: Last, Low.

Labels of every other parameter are excluded, including Cabinet
`MicrophoneTypeSwitch`, Electric `Polyphony`, Corpus `LfoType`, `LfoSync` and
`LfoStereoMode`, and every parameter of Analog, Tension and Collision.

## Parameter tables

The tables list every member of each device element in document order. Kinds and domains are
defined in REQ-BUNDLED-DEVICE-PARAMETERS-003 and REQ-BUNDLED-DEVICE-PARAMETERS-006. In the note column,
"whole numbers" marks the parameters of REQ-BUNDLED-DEVICE-PARAMETERS-007 and "labels" the
parameters of REQ-BUNDLED-DEVICE-PARAMETERS-014. "position" marks the parameters of
REQ-BUNDLED-DEVICE-PARAMETERS-015, whose values have no expectation in this release.
For a plain field the third column gives the `Value` text that documents of this format version
store and that the fixtures use.

### Amp (`Amp`)

9 parameters.

| Path below the device element | Kind | Domain or stored value | Note |
| --- | --- | --- | --- |
| `AmpType` | Enum | 0..6 | labels |
| `Bass` | Float | 0..10 |  |
| `Middle` | Float | 0..10 |  |
| `Treble` | Float | 0..10 |  |
| `Presence` | Float | 0..10 |  |
| `Gain` | Float | 0..10 |  |
| `Volume` | Float | 0..10 |  |
| `DualMono` | Bool | false, true |  |
| `DryWet` | Float | 0..1 |  |

### Cabinet (`Cabinet`)

5 parameters.

| Path below the device element | Kind | Domain or stored value | Note |
| --- | --- | --- | --- |
| `CabinetType` | Enum | 0..4 | labels |
| `MicrophoneTypeSwitch` | Bool | false, true |  |
| `MicrophonePosition` | Enum | 0..2 | labels |
| `DualMono` | Bool | false, true |  |
| `DryWet` | Float | 0..1 |  |

### Analog (`UltraAnalog`)

171 parameters and 7 plain fields.

| Path below the device element | Kind | Domain or stored value | Note |
| --- | --- | --- | --- |
| `Polyphony` | Enum | 0..9 |  |
| `PitchBendRange` | Float | 0..1 |  |
| `Volume` | Float | 0..1 |  |
| `PerNotePitchBendRange` | Float | 0..48 | whole numbers |
| `ChannelPressureTarget1` | Enum | 0..46 |  |
| `ChannelPressureAmount1` | Float | -1..1 |  |
| `ChannelPressureTarget2` | Enum | 0..46 |  |
| `ChannelPressureAmount2` | Float | -1..1 |  |
| `MpeCC74Target1` | Enum | 0..46 |  |
| `MpeCC74Amount1` | Float | -1..1 |  |
| `MpeCC74Target2` | Enum | 0..46 |  |
| `MpeCC74Amount2` | Float | -1..1 |  |
| `Octave` | Float | -3..3 | whole numbers |
| `OctaveRelativePosition` | Plain integer | `"-1073741824"` |  |
| `Transpose` | Float | -12..12 | whole numbers |
| `TransposeRelativePosition` | Plain integer | `"-1073741824"` |  |
| `KeyboardFineTune` | Float | 0..1 |  |
| `KeyboardUnisonToggle` | Bool | false, true |  |
| `KeyboardUnison` | Enum | 0..1 |  |
| `KeyboardDetune` | Float | 0..1 |  |
| `KeyboardUnisonDelay` | Float | 0..1 |  |
| `KeyboardPriority` | Enum | 0..2 |  |
| `KeyboardStretch` | Float | 0..1 |  |
| `KeyboardError` | Float | 0..1 |  |
| `VibratoToggle` | Bool | false, true |  |
| `VibratoSpeed` | Float | 0..1 |  |
| `VibratoFadeIn` | Float | 0..1 |  |
| `VibratoAmount` | Float | 0..1 |  |
| `VibratoError` | Float | 0..1 |  |
| `VibratoDelay` | Float | 0..1 |  |
| `VibratoModWheel` | Float | 0..1 |  |
| `PortamentoToggle` | Bool | false, true |  |
| `PortamentoTime` | Float | 0..1 |  |
| `PortamentoMode` | Enum | 0..1 |  |
| `PortamentoLegato` | Bool | false, true |  |
| `NoiseToggle` | Bool | false, true |  |
| `NoiseColor` | Float | 0..1 |  |
| `NoiseBalance` | Float | 0..1 |  |
| `NoiseLevel` | Float | 0..1 |  |
| `SignalChain1/OscillatorToggle` | Bool | false, true |  |
| `SignalChain1/OscillatorWaveShape` | Enum | 0..3 |  |
| `SignalChain1/OscillatorOct` | Float | -3..3 | whole numbers |
| `SignalChain1/OscillatorOctRelativePosition` | Plain integer | `"-1073741824"` |  |
| `SignalChain1/OscillatorSemi` | Float | -12..12 | whole numbers |
| `SignalChain1/OscillatorSemiRelativePosition` | Plain integer | `"-1073741824"` |  |
| `SignalChain1/OscillatorMode` | Enum | 0..1 |  |
| `SignalChain1/OscillatorEnvTime` | Float | 0..1 |  |
| `SignalChain1/OscillatorDetune` | Float | 0..1 |  |
| `SignalChain1/OscillatorModulation1` | Float | 0..1 |  |
| `SignalChain1/OscillatorPulseWidth` | Float | 0..1 |  |
| `SignalChain1/OscillatorSubAmount` | Float | 0..1 |  |
| `SignalChain1/OscillatorBalance` | Float | 0..1 |  |
| `SignalChain1/OscillatorEnvAmount` | Float | -1..1 |  |
| `SignalChain1/OscillatorLFOModPitch` | Float | -1..1 |  |
| `SignalChain1/OscillatorLFOModPW` | Float | -1..1 |  |
| `SignalChain1/OscillatorLevel` | Float | 0..1 |  |
| `SignalChain1/FilterToggle` | Bool | false, true |  |
| `SignalChain1/FilterType` | Enum | 0..9 |  |
| `SignalChain1/FilterDrive` | Enum | 0..6 |  |
| `SignalChain1/FilterKbdCutoffMod` | Float | -1..1 |  |
| `SignalChain1/FilterCutoffFrequency` | Float | 0..1 |  |
| `SignalChain1/FilterKbdQMod` | Float | -1..1 |  |
| `SignalChain1/FilterQFactor` | Float | 0..1 |  |
| `SignalChain1/FilterLFOCutoffMod` | Float | -1..1 |  |
| `SignalChain1/FilterEnvCutoffMod` | Float | -1..1 |  |
| `SignalChain1/FilterLFOQMod` | Float | -1..1 |  |
| `SignalChain1/FilterEnvQMod` | Float | -1..1 |  |
| `SignalChain1/AmplifierToggle` | Bool | false, true |  |
| `SignalChain1/AmplifierKbdAmpMod` | Float | -1..1 |  |
| `SignalChain1/AmplifierLevel` | Float | 0..1 |  |
| `SignalChain1/AmplifierKbdPanMod` | Float | -1..1 |  |
| `SignalChain1/AmplifierPan` | Float | 0..1 |  |
| `SignalChain1/AmplifierLFOAmpMod` | Float | -1..1 |  |
| `SignalChain1/AmplifierLFOPanMod` | Float | -1..1 |  |
| `SignalChain1/AmplifierEnvPanMod` | Float | -1..1 |  |
| `SignalChain1/LFOToggle` | Bool | false, true |  |
| `SignalChain1/LFOWaveShape` | Enum | 0..4 |  |
| `SignalChain1/LFOSync` | Float | 0..23 | whole numbers |
| `SignalChain1/LFOSyncToggle` | Enum | 0..1 |  |
| `SignalChain1/LFOGateReset` | Bool | false, true |  |
| `SignalChain1/LFOPulseWidth` | Float | 0..1 |  |
| `SignalChain1/LFOSpeed` | Float | 0..1 |  |
| `SignalChain1/LFOPhase` | Float | 0..1 |  |
| `SignalChain1/LFODelay` | Float | 0..1 |  |
| `SignalChain1/LFOFadeIn` | Float | 0..1 |  |
| `SignalChain1/Envelope.0/ExponentialSlope` | Bool | false, true |  |
| `SignalChain1/Envelope.0/Loop` | Enum | 0..3 |  |
| `SignalChain1/Envelope.0/FreeRun` | Bool | false, true |  |
| `SignalChain1/Envelope.0/Legato` | Bool | false, true |  |
| `SignalChain1/Envelope.0/AttackMod` | Float | 0..1 |  |
| `SignalChain1/Envelope.0/AttackTime` | Float | 0..1 |  |
| `SignalChain1/Envelope.0/DecayTime` | Float | 0..1 |  |
| `SignalChain1/Envelope.0/AmpMod` | Float | 0..1 |  |
| `SignalChain1/Envelope.0/SustainLevel` | Float | 0..1 |  |
| `SignalChain1/Envelope.0/SustainTime` | Float | 0..1 |  |
| `SignalChain1/Envelope.0/ReleaseTime` | Float | 0..1 |  |
| `SignalChain1/Envelope.1/ExponentialSlope` | Bool | false, true |  |
| `SignalChain1/Envelope.1/Loop` | Enum | 0..3 |  |
| `SignalChain1/Envelope.1/FreeRun` | Bool | false, true |  |
| `SignalChain1/Envelope.1/Legato` | Bool | false, true |  |
| `SignalChain1/Envelope.1/AttackMod` | Float | 0..1 |  |
| `SignalChain1/Envelope.1/AttackTime` | Float | 0..1 |  |
| `SignalChain1/Envelope.1/DecayTime` | Float | 0..1 |  |
| `SignalChain1/Envelope.1/AmpMod` | Float | 0..1 |  |
| `SignalChain1/Envelope.1/SustainLevel` | Float | 0..1 |  |
| `SignalChain1/Envelope.1/SustainTime` | Float | 0..1 |  |
| `SignalChain1/Envelope.1/ReleaseTime` | Float | 0..1 |  |
| `SignalChain1/FilterToFilter2` | Float | 0..1 |  |
| `SignalChain2/OscillatorToggle` | Bool | false, true |  |
| `SignalChain2/OscillatorWaveShape` | Enum | 0..3 |  |
| `SignalChain2/OscillatorOct` | Float | -3..3 | whole numbers |
| `SignalChain2/OscillatorOctRelativePosition` | Plain integer | `"-1073741824"` |  |
| `SignalChain2/OscillatorSemi` | Float | -12..12 | whole numbers |
| `SignalChain2/OscillatorSemiRelativePosition` | Plain integer | `"-1073741824"` |  |
| `SignalChain2/OscillatorMode` | Enum | 0..1 |  |
| `SignalChain2/OscillatorEnvTime` | Float | 0..1 |  |
| `SignalChain2/OscillatorDetune` | Float | 0..1 |  |
| `SignalChain2/OscillatorModulation1` | Float | 0..1 |  |
| `SignalChain2/OscillatorPulseWidth` | Float | 0..1 |  |
| `SignalChain2/OscillatorSubAmount` | Float | 0..1 |  |
| `SignalChain2/OscillatorBalance` | Float | 0..1 |  |
| `SignalChain2/OscillatorEnvAmount` | Float | -1..1 |  |
| `SignalChain2/OscillatorLFOModPitch` | Float | -1..1 |  |
| `SignalChain2/OscillatorLFOModPW` | Float | -1..1 |  |
| `SignalChain2/OscillatorLevel` | Float | 0..1 |  |
| `SignalChain2/FilterToggle` | Bool | false, true |  |
| `SignalChain2/FilterType` | Enum | 0..9 |  |
| `SignalChain2/FilterDrive` | Enum | 0..6 |  |
| `SignalChain2/FilterKbdCutoffMod` | Float | -1..1 |  |
| `SignalChain2/FilterCutoffFrequency` | Float | 0..1 |  |
| `SignalChain2/FilterKbdQMod` | Float | -1..1 |  |
| `SignalChain2/FilterQFactor` | Float | 0..1 |  |
| `SignalChain2/FilterLFOCutoffMod` | Float | -1..1 |  |
| `SignalChain2/FilterEnvCutoffMod` | Float | -1..1 |  |
| `SignalChain2/FilterLFOQMod` | Float | -1..1 |  |
| `SignalChain2/FilterEnvQMod` | Float | -1..1 |  |
| `SignalChain2/AmplifierToggle` | Bool | false, true |  |
| `SignalChain2/AmplifierKbdAmpMod` | Float | -1..1 |  |
| `SignalChain2/AmplifierLevel` | Float | 0..1 |  |
| `SignalChain2/AmplifierKbdPanMod` | Float | -1..1 |  |
| `SignalChain2/AmplifierPan` | Float | 0..1 |  |
| `SignalChain2/AmplifierLFOAmpMod` | Float | -1..1 |  |
| `SignalChain2/AmplifierLFOPanMod` | Float | -1..1 |  |
| `SignalChain2/AmplifierEnvPanMod` | Float | -1..1 |  |
| `SignalChain2/LFOToggle` | Bool | false, true |  |
| `SignalChain2/LFOWaveShape` | Enum | 0..4 |  |
| `SignalChain2/LFOSync` | Float | 0..23 | whole numbers |
| `SignalChain2/LFOSyncToggle` | Enum | 0..1 |  |
| `SignalChain2/LFOGateReset` | Bool | false, true |  |
| `SignalChain2/LFOPulseWidth` | Float | 0..1 |  |
| `SignalChain2/LFOSpeed` | Float | 0..1 |  |
| `SignalChain2/LFOPhase` | Float | 0..1 |  |
| `SignalChain2/LFODelay` | Float | 0..1 |  |
| `SignalChain2/LFOFadeIn` | Float | 0..1 |  |
| `SignalChain2/Envelope.0/ExponentialSlope` | Bool | false, true |  |
| `SignalChain2/Envelope.0/Loop` | Enum | 0..3 |  |
| `SignalChain2/Envelope.0/FreeRun` | Bool | false, true |  |
| `SignalChain2/Envelope.0/Legato` | Bool | false, true |  |
| `SignalChain2/Envelope.0/AttackMod` | Float | 0..1 |  |
| `SignalChain2/Envelope.0/AttackTime` | Float | 0..1 |  |
| `SignalChain2/Envelope.0/DecayTime` | Float | 0..1 |  |
| `SignalChain2/Envelope.0/AmpMod` | Float | 0..1 |  |
| `SignalChain2/Envelope.0/SustainLevel` | Float | 0..1 |  |
| `SignalChain2/Envelope.0/SustainTime` | Float | 0..1 |  |
| `SignalChain2/Envelope.0/ReleaseTime` | Float | 0..1 |  |
| `SignalChain2/Envelope.1/ExponentialSlope` | Bool | false, true |  |
| `SignalChain2/Envelope.1/Loop` | Enum | 0..3 |  |
| `SignalChain2/Envelope.1/FreeRun` | Bool | false, true |  |
| `SignalChain2/Envelope.1/Legato` | Bool | false, true |  |
| `SignalChain2/Envelope.1/AttackMod` | Float | 0..1 |  |
| `SignalChain2/Envelope.1/AttackTime` | Float | 0..1 |  |
| `SignalChain2/Envelope.1/DecayTime` | Float | 0..1 |  |
| `SignalChain2/Envelope.1/AmpMod` | Float | 0..1 |  |
| `SignalChain2/Envelope.1/SustainLevel` | Float | 0..1 |  |
| `SignalChain2/Envelope.1/SustainTime` | Float | 0..1 |  |
| `SignalChain2/Envelope.1/ReleaseTime` | Float | 0..1 |  |
| `SignalChain2/FilterControllee` | Bool | false, true |  |
| `SelectedFinger` | Plain integer | `"7"` |  |

### Tension (`StringStudio`)

107 parameters and 3 plain fields.

| Path below the device element | Kind | Domain or stored value | Note |
| --- | --- | --- | --- |
| `Polyphony` | Enum | 0..9 |  |
| `PitchBendRange` | Float | 0..12 | whole numbers |
| `Octave` | Float | -3..3 | whole numbers |
| `OctaveRelativePosition` | Plain integer | `"-1073741824"` |  |
| `Transpose` | Float | -12..12 | whole numbers |
| `TransposeRelativePosition` | Plain integer | `"-1073741824"` |  |
| `KeyboardFineTune` | Float | 0..1 |  |
| `KeyboardPriority` | Enum | 0..2 |  |
| `KeyboardUnisonToggle` | Bool | false, true |  |
| `KeyboardUnison` | Enum | 0..1 |  |
| `KeyboardDetune` | Float | 0..1 |  |
| `KeyboardUnisonDelay` | Float | 0..1 |  |
| `KeyboardStretch` | Float | 0..1 |  |
| `KeyboardError` | Float | 0..1 |  |
| `VibratoToggle` | Bool | false, true |  |
| `VibratoSpeed` | Float | 0..1 |  |
| `VibratoFadeIn` | Float | 0..1 |  |
| `VibratoAmount` | Float | 0..1 |  |
| `VibratoError` | Float | 0..1 |  |
| `VibratoDelay` | Float | 0..1 |  |
| `VibratoModWheel` | Float | 0..1 |  |
| `PortamentoToggle` | Bool | false, true |  |
| `PortamentoTime` | Float | 0..1 |  |
| `PortamentoProportional` | Bool | false, true |  |
| `PortamentoLegato` | Bool | false, true |  |
| `GeoExcitatorPosition` | Float | 0..1 |  |
| `GeoExcitatorAbsolute` | Bool | false, true |  |
| `GeoExcitatorKbdModulation` | Float | -1..1 |  |
| `GeoExcitatorVelModulation` | Float | -1..1 |  |
| `GeoDamperPosition` | Float | 0..1 |  |
| `GeoDamperAbsolute` | Bool | false, true |  |
| `GeoDamperKbdModulation` | Float | -1..1 |  |
| `GeoDamperVelModulation` | Float | -1..1 |  |
| `ExcitatorToggle` | Bool | false, true |  |
| `ExcitatorType` | Enum | 0..3 |  |
| `ExcitatorParameterX` | Float | 0..1 |  |
| `ExcitatorParameterXKbdMod` | Float | -1..1 |  |
| `ExcitatorParameterXVelMod` | Float | -1..1 |  |
| `ExcitatorStiffness` | Float | 0..1 |  |
| `ExcitatorStiffnessKbdMod` | Float | -1..1 |  |
| `ExcitatorStiffnessVelMod` | Float | -1..1 |  |
| `ExcitatorVelocity` | Float | 0..1 |  |
| `ExcitatorVelocityKbdMod` | Float | -1..1 |  |
| `ExcitatorVelocityVelMod` | Float | -1..1 |  |
| `ExcitatorDamping` | Float | 0..1 |  |
| `PickupToggle` | Bool | false, true |  |
| `PickupPosition` | Float | 0..1 |  |
| `DamperToggle` | Bool | false, true |  |
| `DamperMass` | Float | 0..1 |  |
| `DamperMassKbdMod` | Float | -1..1 |  |
| `DamperStiffness` | Float | 0..1 |  |
| `DamperStiffnessKbdMod` | Float | -1..1 |  |
| `DamperVelocity` | Float | 0..1 |  |
| `DamperVelocityKbdMod` | Float | -1..1 |  |
| `DamperDamping` | Float | 0..1 |  |
| `DamperGated` | Bool | false, true |  |
| `StringDamping` | Float | 0..1 |  |
| `StringDampingKbdMod` | Float | -1..1 |  |
| `StringDecay` | Float | 0..1 |  |
| `StringDecayKbdMod` | Float | -1..1 |  |
| `StringDecayRatio` | Float | 0..1 |  |
| `StringInharmonicity` | Float | 0..1 |  |
| `TerminationToggle` | Bool | false, true |  |
| `TerminationFingerStiffness` | Float | 0..1 |  |
| `TerminationFingerForce` | Float | 0..1 |  |
| `TerminationFingerForceKbdMod` | Float | -1..1 |  |
| `TerminationFingerForceVelMod` | Float | -1..1 |  |
| `TerminationFretStiffness` | Float | 0..1 |  |
| `LFOToggle` | Bool | false, true |  |
| `LFOWaveShape` | Enum | 0..4 |  |
| `LFOSync` | Float | 0..23 | whole numbers |
| `LFOSyncToggle` | Enum | 0..1 |  |
| `LFODelay` | Float | 0..1 |  |
| `LFOSpeed` | Float | 0..1 |  |
| `LFOFadeIn` | Float | 0..1 |  |
| `FilterToggle` | Bool | false, true |  |
| `FilterType` | Enum | 0..9 |  |
| `FilterCutoffFrequency` | Float | 0..1 |  |
| `FilterCutoffFrequencyKbdMod` | Float | -1..1 |  |
| `FilterCutoffFrequencyLFOMod` | Float | -1..1 |  |
| `FilterCutoffFrequencyEnvMod` | Float | -1..1 |  |
| `FilterQFactor` | Float | 0..1 |  |
| `FilterQFactorKbdMod` | Float | -1..1 |  |
| `FilterQFactorLFOMod` | Float | -1..1 |  |
| `FilterQFactorEnvMod` | Float | -1..1 |  |
| `FilterEnvelopeToggle` | Bool | false, true |  |
| `FilterEnvelopeAttack` | Float | 0..1 |  |
| `FilterEnvelopeDecay` | Float | 0..1 |  |
| `FilterEnvelopeSustain` | Float | 0..1 |  |
| `FilterEnvelopeRelease` | Float | 0..1 |  |
| `FilterEnvelopeAttackMod` | Float | 0..1 |  |
| `FilterEnvelopeAmpMod` | Float | 0..1 |  |
| `BodyToggle` | Bool | false, true |  |
| `BodyType` | Enum | 0..3 |  |
| `BodySize` | Enum | 0..4 |  |
| `BodyDecay` | Float | 0..1 |  |
| `BodyLowCut` | Float | 0..1 |  |
| `BodyHighCut` | Float | 0..1 |  |
| `BodyLevel` | Float | 0..1 |  |
| `BodyMix` | Float | 0..1 |  |
| `PerNotePitchBendRange` | Float | 0..48 | whole numbers |
| `ChannelPressureTarget1` | Enum | 0..12 |  |
| `ChannelPressureRange1` | Float | -1..1 |  |
| `ChannelPressureTarget2` | Enum | 0..12 |  |
| `ChannelPressureRange2` | Float | -1..1 |  |
| `SlideTarget1` | Enum | 0..12 |  |
| `SlideRange1` | Float | -1..1 |  |
| `SlideTarget2` | Enum | 0..12 |  |
| `SlideRange2` | Float | -1..1 |  |
| `CurrentTab` | Plain integer | `"0"` |  |

### Collision (`Collision`)

139 parameters and 3 plain fields.

| Path below the device element | Kind | Domain or stored value | Note |
| --- | --- | --- | --- |
| `Mallet/OnOff` | Bool | false, true |  |
| `Mallet/Volume` | Float | 0..1 |  |
| `Mallet/VelToVolume` | Float | -5..5 |  |
| `Mallet/KeyToVolume` | Float | -2..2 |  |
| `Mallet/Stiffness` | Float | 0..1 |  |
| `Mallet/VelToStiffness` | Float | -5..5 |  |
| `Mallet/KeyToStiffness` | Float | -2..2 |  |
| `Mallet/NoiseAmount` | Float | 0..1 |  |
| `Mallet/VelToNoiseAmount` | Float | -5..5 |  |
| `Mallet/KeyToNoiseAmount` | Float | -2..2 |  |
| `Mallet/NoiseColor` | Float | 0..1 |  |
| `Noise/OnOff` | Bool | false, true |  |
| `Noise/Volume` | Float | 0..1 |  |
| `Noise/VelToVolume` | Float | -5..5 |  |
| `Noise/KeyToVolume` | Float | -2..2 |  |
| `Noise/FilterType` | Enum | 0..3 |  |
| `Noise/Freq` | Float | 0..1 |  |
| `Noise/VelToFreq` | Float | -8..8 |  |
| `Noise/KeyToFreq` | Float | -2..2 |  |
| `Noise/EnvToFreq` | Float | -5..5 |  |
| `Noise/Q` | Float | 0..1 |  |
| `Noise/Attack` | Float | 0..1 |  |
| `Noise/Decay` | Float | 0..1 |  |
| `Noise/Sustain` | Float | 0..1 |  |
| `Noise/Release` | Float | 0..1 |  |
| `Resonator1/OnOff` | Bool | false, true |  |
| `Resonator1/Type` | Enum | 0..6 |  |
| `Resonator1/Quality` | Enum | 0..3 |  |
| `Resonator1/Transpose` | Float | -48..48 | whole numbers |
| `Resonator1/TransposeRelativePosition` | Plain integer | `"-1073741824"` |  |
| `Resonator1/FineTranspose` | Float | -50..50 | whole numbers |
| `Resonator1/KeyToTranspose` | Float | -2..2 |  |
| `Resonator1/StartTranspose` | Float | -1..1 |  |
| `Resonator1/VelToStartTranspose` | Float | -5..5 |  |
| `Resonator1/StartTime` | Float | 0..1 |  |
| `Resonator1/Decay` | Float | 0..1 |  |
| `Resonator1/VelToDecay` | Float | -5..5 |  |
| `Resonator1/KeyToDecay` | Float | -2..2 |  |
| `Resonator1/DecayOnNoteOff` | Float | 0..1 |  |
| `Resonator1/Damp` | Float | -1..1 |  |
| `Resonator1/VelToDamp` | Float | -5..5 |  |
| `Resonator1/KeyToDamp` | Float | -2..2 |  |
| `Resonator1/Radius` | Float | 0..1 |  |
| `Resonator1/VelToRadius` | Float | -5..5 |  |
| `Resonator1/KeyToRadius` | Float | -2..2 |  |
| `Resonator1/Ratio` | Float | 0..1 |  |
| `Resonator1/AmpFreq` | Float | -1..1 |  |
| `Resonator1/Bleed` | Float | 0..1 |  |
| `Resonator1/Inharmonics` | Float | -1..1 |  |
| `Resonator1/VelToInharmonics` | Float | -5..5 |  |
| `Resonator1/TubeOpening` | Float | 0..1 |  |
| `Resonator1/VelToTubeOpening` | Float | -5..5 |  |
| `Resonator1/HitX` | Float | 0..1 | position |
| `Resonator1/RandomToHitX` | Float | 0..1 |  |
| `Resonator1/ListeningXL` | Float | 0..1 | position |
| `Resonator1/ListeningXR` | Float | 0..1 | position |
| `Resonator1/Pan` | Float | -1..1 |  |
| `Resonator1/KeyToPan` | Float | -1..1 |  |
| `Resonator1/Volume` | Float | 0..1 |  |
| `Resonator2/OnOff` | Bool | false, true |  |
| `Resonator2/Type` | Enum | 0..6 |  |
| `Resonator2/Quality` | Enum | 0..3 |  |
| `Resonator2/Transpose` | Float | -48..48 | whole numbers |
| `Resonator2/TransposeRelativePosition` | Plain integer | `"-1073741824"` |  |
| `Resonator2/FineTranspose` | Float | -50..50 | whole numbers |
| `Resonator2/KeyToTranspose` | Float | -2..2 |  |
| `Resonator2/StartTranspose` | Float | -1..1 |  |
| `Resonator2/VelToStartTranspose` | Float | -5..5 |  |
| `Resonator2/StartTime` | Float | 0..1 |  |
| `Resonator2/Decay` | Float | 0..1 |  |
| `Resonator2/VelToDecay` | Float | -5..5 |  |
| `Resonator2/KeyToDecay` | Float | -2..2 |  |
| `Resonator2/DecayOnNoteOff` | Float | 0..1 |  |
| `Resonator2/Damp` | Float | -1..1 |  |
| `Resonator2/VelToDamp` | Float | -5..5 |  |
| `Resonator2/KeyToDamp` | Float | -2..2 |  |
| `Resonator2/Radius` | Float | 0..1 |  |
| `Resonator2/VelToRadius` | Float | -5..5 |  |
| `Resonator2/KeyToRadius` | Float | -2..2 |  |
| `Resonator2/Ratio` | Float | 0..1 |  |
| `Resonator2/AmpFreq` | Float | -1..1 |  |
| `Resonator2/Bleed` | Float | 0..1 |  |
| `Resonator2/Inharmonics` | Float | -1..1 |  |
| `Resonator2/VelToInharmonics` | Float | -5..5 |  |
| `Resonator2/TubeOpening` | Float | 0..1 |  |
| `Resonator2/VelToTubeOpening` | Float | -5..5 |  |
| `Resonator2/HitX` | Float | 0..1 | position |
| `Resonator2/RandomToHitX` | Float | 0..1 |  |
| `Resonator2/ListeningXL` | Float | 0..1 | position |
| `Resonator2/ListeningXR` | Float | 0..1 | position |
| `Resonator2/Pan` | Float | -1..1 |  |
| `Resonator2/KeyToPan` | Float | -1..1 |  |
| `Resonator2/Volume` | Float | 0..1 |  |
| `ResonatorOrder` | Enum | 0..1 |  |
| `Lfo1/OnOff` | Bool | false, true |  |
| `Lfo1/Type` | Enum | 0..6 |  |
| `Lfo1/Retrigger` | Bool | false, true |  |
| `Lfo1/Sync` | Enum | 0..1 |  |
| `Lfo1/Rate` | Float | 0..1 |  |
| `Lfo1/SyncRate` | Float | 0..21 | whole numbers |
| `Lfo1/KeyToRate` | Float | -2..2 |  |
| `Lfo1/Phase` | Float | 0..360 |  |
| `Lfo1/Amount` | Float | 0..1 |  |
| `Lfo1/VelToAmount` | Float | -5..5 |  |
| `Lfo1/Target1/Target` | Enum | 0..16 |  |
| `Lfo1/Target1/Amount` | Float | -5..5 |  |
| `Lfo1/Target2/Target` | Enum | 0..16 |  |
| `Lfo1/Target2/Amount` | Float | -5..5 |  |
| `Lfo2/OnOff` | Bool | false, true |  |
| `Lfo2/Type` | Enum | 0..6 |  |
| `Lfo2/Retrigger` | Bool | false, true |  |
| `Lfo2/Sync` | Enum | 0..1 |  |
| `Lfo2/Rate` | Float | 0..1 |  |
| `Lfo2/SyncRate` | Float | 0..21 | whole numbers |
| `Lfo2/KeyToRate` | Float | -2..2 |  |
| `Lfo2/Phase` | Float | 0..360 |  |
| `Lfo2/Amount` | Float | 0..1 |  |
| `Lfo2/VelToAmount` | Float | -5..5 |  |
| `Lfo2/Target1/Target` | Enum | 0..16 |  |
| `Lfo2/Target1/Amount` | Float | -5..5 |  |
| `Lfo2/Target2/Target` | Enum | 0..16 |  |
| `Lfo2/Target2/Amount` | Float | -5..5 |  |
| `PitchBendRange` | Float | 0..24 | whole numbers |
| `PitchBendTarget1/Target` | Enum | 0..17 |  |
| `PitchBendTarget1/Amount` | Float | -5..5 |  |
| `ModWheelTarget1/Target` | Enum | 0..17 |  |
| `ModWheelTarget1/Amount` | Float | -5..5 |  |
| `ModWheelTarget2/Target` | Enum | 0..17 |  |
| `ModWheelTarget2/Amount` | Float | -5..5 |  |
| `ChannelPressureTarget1/Target` | Enum | 0..17 |  |
| `ChannelPressureTarget1/Amount` | Float | -5..5 |  |
| `ChannelPressureTarget2/Target` | Enum | 0..17 |  |
| `ChannelPressureTarget2/Amount` | Float | -5..5 |  |
| `Polyphony` | Enum | 0..8 |  |
| `Retrigger` | Bool | false, true |  |
| `Volume` | Float | 0..1 |  |
| `PerNotePitchBendRange` | Float | 0..48 | whole numbers |
| `MpeCC74Target1/Target` | Enum | 0..17 |  |
| `MpeCC74Target1/Amount` | Float | -5..5 |  |
| `MpeCC74Target2/Target` | Enum | 0..17 |  |
| `MpeCC74Target2/Amount` | Float | -5..5 |  |
| `CurrentTab` | Plain integer | `"0"` |  |

### Electric (`LoungeLizard`)

33 parameters.

| Path below the device element | Kind | Domain or stored value | Note |
| --- | --- | --- | --- |
| `Polyphony` | Enum | 0..30 |  |
| `PitchBendRange` | Float | 0..1 |  |
| `PerNotePitchBendRange` | Float | 0..48 | whole numbers |
| `Volume` | Float | 0..1 |  |
| `KeyboardTranspose` | Float | 0..24 | whole numbers |
| `KeyboardFineTune` | Float | 0..1 |  |
| `KeyboardStretch` | Float | 0..1 |  |
| `MalletStiffness` | Float | 0..1 |  |
| `MalletStiffnessKeyboard` | Float | 0..1 |  |
| `MalletStiffnessVelocity` | Float | 0..1 |  |
| `MalletForceStrength` | Float | 0..1 |  |
| `MalletForceKeyboard` | Float | 0..1 |  |
| `MalletForceVelocity` | Float | 0..1 |  |
| `MalletNoisePitch` | Float | 0..1 |  |
| `MalletNoiseDecay` | Float | 0..1 |  |
| `MalletNoiseAmount` | Float | 0..1 |  |
| `MalletNoiseKeyboardScaling` | Float | 0..1 |  |
| `ForkReleaseTime` | Float | 0..1 |  |
| `ForkTineDecay` | Float | 0..1 |  |
| `ForkTineVolume` | Float | 0..1 |  |
| `ForkTineKeyboardScaling` | Float | 0..1 |  |
| `ForkTineColor` | Float | 0..1 |  |
| `ForkToneBarDecay` | Float | 0..1 |  |
| `ForkToneBarVolume` | Float | 0..1 |  |
| `PickupSymmetry` | Float | 0..1 |  |
| `PickupDistance` | Float | 0..1 |  |
| `PickupModel` | Enum | 0..1 | labels |
| `PickupAmpIn` | Float | 0..1 |  |
| `PickupAmpOut` | Float | 0..1 |  |
| `PickupAmpKeyboardScaling` | Float | 0..1 |  |
| `DamperTone` | Float | 0..1 |  |
| `DamperAmount` | Float | 0..1 |  |
| `DamperBalance` | Float | 0..1 |  |

### Corpus (`Corpus`)

38 parameters and 7 plain fields.

| Path below the device element | Kind | Domain or stored value | Note |
| --- | --- | --- | --- |
| `SideChain/RoutedInput/Routable/Target` | Plain text | `"MidiIn/None"` |  |
| `SideChain/RoutedInput/Routable/UpperDisplayString` | Plain text | `"No Output"` |  |
| `SideChain/RoutedInput/Routable/LowerDisplayString` | Plain text | `""` |  |
| `SideChain/RoutedInput/Routable/MpeSettings/ZoneType` | Plain integer | `"0"` |  |
| `SideChain/RoutedInput/Routable/MpeSettings/FirstNoteChannel` | Plain integer | `"1"` |  |
| `SideChain/RoutedInput/Routable/MpeSettings/LastNoteChannel` | Plain integer | `"15"` |  |
| `SideChain/RoutedInput/Routable/MpePitchBendUsesTuning` | Plain Boolean | `"true"` |  |
| `ResonanceType` | Enum | 0..6 | labels |
| `ResonatorQuality` | Enum | 0..3 | labels |
| `Frequency` | Float | 0..1 |  |
| `Transpose` | Float | -48..48 | whole numbers |
| `FineTranspose` | Float | -50..50 | whole numbers |
| `Detune` | Float | -1..1 |  |
| `Decay` | Float | 0..1 |  |
| `FreqDamping` | Float | -1..1 |  |
| `Radius` | Float | 0..1 |  |
| `AmpFreq` | Float | -1..1 |  |
| `Inharmonics` | Float | -1..1 |  |
| `TubeOpening` | Float | 0..1 |  |
| `Ratio` | Float | 0..1 |  |
| `ExcitationX` | Float | 0..1 | position |
| `ListeningXL` | Float | 0..1 | position |
| `ListeningXR` | Float | 0..1 | position |
| `LfoOnOff` | Bool | false, true |  |
| `LfoType` | Enum | 0..6 |  |
| `LfoSync` | Enum | 0..1 |  |
| `LfoRate` | Float | 0..1 |  |
| `LfoSyncRate` | Float | 0..21 | whole numbers |
| `LfoStereoMode` | Enum | 0..1 |  |
| `LfoSpin` | Float | 0..0.5 |  |
| `LfoPhase` | Float | 0..360 |  |
| `LfoOffset` | Float | 0..360 |  |
| `LfoAmount` | Float | 0..1 |  |
| `FilterOn` | Bool | false, true |  |
| `FilterMidFreq` | Float | 50..18000 |  |
| `FilterBandWidth` | Float | 0.5..9 |  |
| `MidiPitch` | Bool | false, true |  |
| `MidiMode` | Enum | 0..1 | labels |
| `PitchBendRange` | Float | 0..24 | whole numbers |
| `MidiGate` | Bool | false, true |  |
| `DecayOnNoteOff` | Float | 0..1 |  |
| `Drive` | Float | 0..1 |  |
| `StereoWidth` | Float | 0..1 |  |
| `Bleed` | Float | 0..1 |  |
| `DryWet` | Float | 0..1 |  |

## Acceptance representation and comparison

[cases.json](cases.json) lists 82 cases. Each has a `device`, an input fixture,
the action `open` and an expected result with these parts:

| Field | Meaning |
| --- | --- |
| `outcome` | `opens` or `refused` |
| `state` | Parameter values when the preset opens, by path; only listed keys are judged. A Float value is a JSON number equal to its binary32 value; an Enum value is an integer; a Bool value is `true` or `false` |
| `labels` | Text the user interface shows for the listed parameter's value, by path |

`outcome` compares exactly. A Float value compares exactly after its exact
widening to binary64; Enum and Bool values compare exactly; labels compare as
exact text. Anything a case does not list is not judged. A refused case has no
`state` or `labels` part. Each case starts from a fresh state with its fixture
alone. Each case also has a `kind`: `positive`, `negative` (the preset is
refused, including one fixture that is not well-formed XML) or `boundary`
(every parameter at a bound of its domain). Reading has no timing tolerance,
cancellation step or teardown within this scope, so those case kinds are
omitted.

`expectation_provenance` labels each case. `documented and static-derived`
means the document form comes from the shipped documents and the reading rules
are static-derived. `static-derived` means the rule exercised is static-derived.
Every case has `reference_execution` and `candidate_execution` `not-run`.

This is a **project comparison representation**, not an API claimed to exist in
Live and not a required design. A candidate adapter may translate its own
result into these labels. The fixture set is not an executable harness for the
original application.

## Reference comparison obligation (not executed)

A later comparison against the original application needs a device preset file
per case. The validation analyst builds it from the fixture: insert, as the
first children of the device element, the members shared by all devices as the
original application writes them for the same device in a device preset of this
format version; keep the fixture's members unchanged; keep the fixture's three
root attributes and add `Creator` and `Revision` as such a preset carries them;
store the result in the gzip container with the `.adv` extension. Open it in a
new Live Set created from the factory default set, not a user template: an
instrument (Analog, Tension, Collision, Electric) on a MIDI track, an audio
effect (Amp, Cabinet, Corpus) on an audio track. A refusal is observed when no
device from the file is added. A label is observed as the text the device shows
for that parameter's value. The host locale uses `.` as the decimal separator.

The observation channel is chosen by the validation analyst. The value text a
device displays is not its stored value, and this release does not give the
mapping, so `state` needs a channel that reports the stored number. A channel
that rounds must be compared at its rounding. A channel that saves the opened
device rests on save behavior this release does not specify, and its use must
be justified separately. The three assumptions under
[What the contract means](#what-the-contract-means) are part of what a
reference comparison tests. None of this has been run.

Before claiming reference compatibility, a separately designed bounded probe
must run these cases, or a justified equivalent set, against the original. It
must pin the original and candidate builds and the fixture bytes, retain
independent observations, and report mismatches. Candidate-only success proves
agreement with this contract, not with the running original.

## Exclusions and deferred obligations

Requirements not released:

- **REQ-BUNDLED-DEVICE-PARAMETERS-005**: value text and every other content
  written when a device is saved;
- **REQ-BUNDLED-DEVICE-PARAMETERS-008**: the value of a parameter whose element
  or `Value` is missing;
- **REQ-BUNDLED-DEVICE-PARAMETERS-009**: the values of a newly inserted device;
- **REQ-BUNDLED-DEVICE-PARAMETERS-010**: values outside the domain, a range that
  differs from the domain, and fractional values of whole-number parameters;
- **REQ-BUNDLED-DEVICE-PARAMETERS-013**: parameters bound to rack macros or MIDI;
- **REQ-BUNDLED-DEVICE-PARAMETERS-015**: which part of the resonator the
  position values of Corpus (`ExcitationX`, `ListeningXL`, `ListeningXR`) and
  Collision (`HitX`, `ListeningXL`, `ListeningXR` of each resonator) address,
  and the value read for each of them. Their paths, kind and stored range are
  in the tables, marked "position", and the fixtures store them in the fixture
  form; no case judges their values.

These inputs have **no expectation** in this release:

- a device element that lacks a member of its table, holds its members in
  another order, or differs from the fixture form in a way its case does not
  state;
- a `Manual` element without a `Value` attribute, and every other missing
  element or attribute;
- a parameter element with a `KeyMidi` child;
- `MidiControllerRange` or `MidiCCOnOffThresholds` values other than the
  fixture form; `LomId`, `LockEnvelope` or target `Id` values other than 0;
- plain field values other than those in the tables;
- Float, Enum or Bool values outside their domain, and fractional values of
  whole-number parameters;
- Float text whose remainder, after leading spaces and an optional sign, starts
  with `0x` or `0X`, or with `inf` or `nan` in any letter case; the text
  `Invalid`; text starting with `#`; leading whitespace other than U+0020;
- Enum text with spaces both before and after the digits, or with a `+` and
  trailing spaces (for example ` 3 ` and `+3 `); Enum text with a `-` sign;
  Enum text longer than 63 characters that ends in a space;
- duplicated plain fields, duplicated children of a parameter other than
  `Manual`, and repeated unknown elements;
- element names that the original application may define for a parent although
  this release does not list them, including the shared members of all devices
  and `KeyMidi`;
- unknown attributes on any element;
- root attributes other than exactly the three of the preconditions, other
  format versions and their upgrade, and a second child of the root;
- XML that differs from the fixtures' form in a way no rule of this release
  names, for example another declaration or encoding, a document type
  declaration, comments or processing instructions, namespaces, entity or
  character references, or carriage returns;
- the compressed file container; racks, Live Sets, clips and every other
  document kind;
- documents that break more than one rule.

Excluded behavior: everything written on save; defaults of missing parameters
and of new devices; display, use and saving of out-of-range values; rack macro
and MIDI bindings; the meaning of plain fields; the values read for the
position parameters and their meaning; labels other than those of
REQ-BUNDLED-DEVICE-PARAMETERS-014, display text and units; the members shared
by all devices; sound, the values sent to the sound engine,
playback and timing; edits after opening, automation and modulation, undo; and
how a refusal is presented.

## Fixture provenance

All 82 fixtures were written for this release from the parameter tables. Each
is a device preset as described in the preconditions: the declaration
`<?xml version="1.0" encoding="UTF-8"?>`, the root with its three attributes
and the device element with every member of its table in the fixture form,
indented by two spaces per level. Parameter values were computed for the cases,
not taken from shipped presets. In a fixture with values inside every domain, a
Float parameter holds the point one quarter of the way from its lower to its
upper bound (rounded down to a whole number for whole-number parameters), an
Enum parameter holds half its highest value rounded up, and Bool parameters
alternate between true and false in table order. Other fixtures hold every
parameter at its lower or upper bound, or change that first fixture as their
purpose states. Plain fields hold the texts in the tables. Text is ASCII with
line-feed line endings and no tabs.

No fixture contains shipped file content, program code or assets. Expected
results are newly authored behavioral data. No public source or dependency is
approved or included. Review status is recorded in [the manifest](manifest.json).
