# Automation envelopes in Live Set documents, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-AUTOMATION with FEAT-PERSISTENCE. Parent
specification identity: SPEC-AUTOMATION-ENVELOPES revision 1. Release:
automation-envelopes-v1. Only the clauses explicitly included below are in
scope. No other clause of a listed requirement is implicitly approved. This
document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the narrowing recorded in [the review disposition](REVIEW.md).

## What the contract means

A Live Set stores automation as envelopes: lists of timed events that give an
automated parameter its value over time. For one document format version, this
contract describes:

- where track and clip envelopes are stored and how an envelope names its
  parameter;
- the event elements, their attributes and value kinds;
- which envelopes make a document refused when it is opened;
- how curve controls are kept on open and written on save;
- the text read and written for event numbers.

It does not describe the value an envelope supplies to its parameter at any
time, processed audio, editing, recording, undo, the user interface, or how a
refusal is reported.

All rules and expected results are **static-derived**: they were derived for the
target build without running it. None is an observed execution of the original
application, and none was run against a candidate. No compatibility result is
established, and the original application remains the authority for a later
comparison. Some derived steps rest on assumptions that were not traced to the
end: that opening a Live Set applies the envelope checks of
REQ-AUTOMATION-ENVELOPES-007; that `BoolEvent` and `EnumEvent` values are read
with the Boolean and integer rules of REQ-AUTOMATION-ENVELOPES-012; and that a
save keeps each envelope bound to its target. The
[comparison obligation](#reference-comparison-obligation-not-executed) covers
them.

## Document scope and preconditions

- The input is the decoded XML of a Live Set: well-formed XML 1.0 in UTF-8 whose
  root element is `Ableton` with exactly the attributes `MajorVersion="5"`,
  `MinorVersion="12.0_12402"` and `SchemaChangeCount="1"`, and whose first
  child is `LiveSet`. Every fixture uses this envelope. The compressed file
  container, other root attributes, other format versions and their upgrade are
  outside this release.
- The **text** of a value is its attribute value after standard XML
  attribute-value decoding. Paths are relative to `/Ableton/LiveSet`.
- **Opens** means the document is read to its end without refusal. **Refused**
  means the document is not opened. How a refusal is reported, what is open
  afterwards, and anything that happens after reading are excluded.
- Numbers use `.` as the decimal separator. Expectations assume a host locale
  whose decimal separator is `.`.
- A full Live Set contains much more than the fixtures: other tracks, devices,
  clip content, scenes and transport state. That content is outside this
  release. Its absence from a fixture must not by itself change a judged
  outcome.
- Every fixture has the layout described under
  [fixture provenance](#fixture-provenance): one audio track with an envelope
  list and three mixer parameters, and one MIDI track holding a MIDI clip in a
  session clip slot and the MIDI controller target 6.

## Terms

| Term | Meaning |
| --- | --- |
| L | The lower time bound −63,072,000, written `-63072000` |
| Event | A `FloatEvent`, `BoolEvent` or `EnumEvent` child of an envelope's `Automation/Events`, taken in document order |
| Stored units | The units in which the parameter's `Manual` value and its event values are written |

## Selected requirement clauses

### REQ-AUTOMATION-ENVELOPES-001: where envelopes are stored (partial)

1. A track's arrangement envelopes are the `AutomationEnvelope` children of the
   track's `AutomationEnvelopes/Envelopes` element. `AudioTrack`, `MidiTrack`,
   `GroupTrack`, `ReturnTrack`, `MainTrack` and `PreHearTrack` elements hold this
   list. The cases use the audio track at `Tracks/AudioTrack`.
2. A clip's envelopes are the `ClipEnvelope` children of the clip's
   `Envelopes/Envelopes` element, in an `AudioClip` or a `MidiClip`. The cases use
   the MIDI clip at
   `Tracks/MidiTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/MidiClip`.
   A `ClipEnvelope` also holds `LoopSlot` and `ScrollerTimePreserver`, which this
   release does not interpret.
3. Both envelope elements carry an `Id` attribute and contain, in this order,
   `EnvelopeTarget` with a `PointeeId` child, and `Automation` with `Events`
   and `AutomationTransformViewState`:

   ```xml
   <AutomationEnvelope Id="0">
     <EnvelopeTarget><PointeeId Value="22" /></EnvelopeTarget>
     <Automation>
       <Events>
         <FloatEvent Id="0" Time="-63072000" Value="0" />
         <FloatEvent Id="1" Time="4" Value="0" />
       </Events>
       <AutomationTransformViewState>
         <IsTransformPending Value="false" />
         <TimeAndValueTransforms />
       </AutomationTransformViewState>
     </Automation>
   </AutomationEnvelope>
   ```

4. Every fixture envelope has the transform state shown: `IsTransformPending`
   `false` and an empty `TimeAndValueTransforms`.

### REQ-AUTOMATION-ENVELOPES-002: envelope targets (partial)

1. `EnvelopeTarget/PointeeId/@Value` equals the `Id` attribute of the envelope's
   target element in the same document. The binding is by this Id alone. The
   position of an envelope in its list does not select its target.
2. The target elements of this release are the `AutomationTarget` children of
   the audio track's `DeviceChain/Mixer/Speaker`, `DeviceChain/Mixer/Pan` and
   `DeviceChain/Mixer/CrossFadeState`, named by that track's envelopes, and the
   MIDI track's `DeviceChain/MainSequencer/MidiControllers/ControllerTargets.6`,
   named by the envelope of that track's clip.
3. In every fixture, each `PointeeId` value equals the `Id` of exactly one
   element, target Ids are distinct and smaller than `NextPointeeId`, each
   target's `LockEnvelope` is `0`, and each parameter is named by at most one
   envelope.
4. The cases judge the binding only through the saved envelope of each target.
   AUTOMATION-ENVELOPES-021 lists its envelopes in an order different from the
   order of their targets.

### REQ-AUTOMATION-ENVELOPES-003: event elements and value kinds (partial)

| Target | Value kind | Event element | `Value` attribute | Range of the cases |
| --- | --- | --- | --- | --- |
| `Pan` | Float | `FloatEvent` | IEEE 754 binary32 | −1 to 1 |
| `ControllerTargets.6` | Float | `FloatEvent` | IEEE 754 binary32 | 0 to 127 |
| `Speaker` | Bool | `BoolEvent` | Boolean | `true` or `false` |
| `CrossFadeState` | Enum | `EnumEvent` | integer | 0 to 2 |

Every event has an `Id` attribute and a `Time` attribute, an IEEE 754 binary64
number. In every fixture, event Ids are distinct within their list. A
`FloatEvent` may also carry the curve controls of REQ-AUTOMATION-ENVELOPES-008.
Event values are in the parameter's stored units, the same units as its
`Manual` value.

### REQ-AUTOMATION-ENVELOPES-005: the event at the lower bound (partial)

A list whose only event is at L is accepted (REQ-AUTOMATION-ENVELOPES-007).
In every `open-save` fixture, the first event is at L and has the value of the
next event.

### REQ-AUTOMATION-ENVELOPES-006: event order (partial)

1. Events are taken in document order. In every fixture their times do not
   decrease, and at most two events share a time.
2. An event after the first may have a negative time.

### REQ-AUTOMATION-ENVELOPES-007: envelopes that refuse a document (partial)

1. A document is refused when the `Events` list of any `AutomationEnvelope` or
   `ClipEnvelope` is empty.
2. A document is refused when the first event of any such envelope has a time,
   read as binary64 under REQ-AUTOMATION-ENVELOPES-012, that is neither L nor 0.
   The comparison is numeric, so `-0` and `-6.3072e7` pass.
3. Only the first event's time is checked. Later events at any time, including
   negative times, do not cause a refusal.
4. These rules apply to track envelopes and clip envelopes alike.

### REQ-AUTOMATION-ENVELOPES-008: curve controls (partial)

1. A `FloatEvent` may carry the attributes `CurveControl1X`, `CurveControl1Y`,
   `CurveControl2X` and `CurveControl2Y`, which are binary64 numbers. The X pair
   is (`CurveControl1X`, `CurveControl2X`) and the Y pair is (`CurveControl1Y`,
   `CurveControl2Y`).
2. A missing control reads as 0.5. An event whose four controls all equal 0.5
   has no curve.
3. On save, each control equal to exactly 0.5 is not written, independently of
   the other three. The others are written with the binary64 rule of
   REQ-AUTOMATION-ENVELOPES-012. An event without a curve is therefore saved
   without control attributes.
4. Expectations exist only for controls on an event that is neither the first
   nor the last of its list and whose next event has a later time and a
   different value.

### REQ-AUTOMATION-ENVELOPES-009: curve controls kept on open (partial)

For a pair of controls (c1, c2), let K(c1, c2) hold when both lie in [0, 1] and
either c1 ≤ c2, or c1² + c2² − c1·c2 − c1 ≤ −10⁻⁶. K is a sufficient condition
for the coordinate of the cubic Bézier curve with control values 0, c1, c2, 1
to be non-decreasing.

An event whose X pair and Y pair both satisfy K keeps its four controls when the
document is opened, and a later save writes them under
REQ-AUTOMATION-ENVELOPES-008. For controls that do not satisfy K, this release
does not say whether they are kept or replaced by 0.5. The margin 10⁻⁶ is a scope
limit of this release.

### REQ-AUTOMATION-ENVELOPES-012: event number text (partial)

On open:

1. `Time` and the curve controls: leading U+0020 spaces are skipped. The value is
   then read from the longest prefix of the remaining text that forms a decimal
   number: an optional `+` or `-`; digits with an optional `.` and fraction
   digits, at least one digit in total; and an optional exponent of `e` or `E`,
   an optional sign and at least one digit. An exponent marker without digits is
   not part of the prefix, and text after the prefix is ignored. The value is the
   binary64 number nearest to the decimal prefix, ties to even. Text without such
   a prefix is refused, for example `abc` or the empty string.
2. `FloatEvent/@Value` is read by rule 1, and the binary64 result is then rounded
   to the nearest binary32 value, ties to even.
3. `BoolEvent/@Value`: `true` or `1` reads as true, `false` or `0` as false.
   Matching is exact and case-sensitive, with no trimming. Any other text is
   refused, including `TRUE`, `True`, the empty string and ` true`.
4. `EnumEvent/@Value` is accepted, as a decimal integer, when it is ASCII digits
   preceded by any number of spaces and at most one `+`, in that order, with
   nothing after the digits (`2`, ` 2`, `+2`, ` +2`), or ASCII digits followed only
   by spaces (`2 `). It is refused when it is empty or only spaces; when it has
   any byte outside ASCII; or when, after leading spaces and one leading `+`, the
   rest is empty, starts with `-` after that `+`, contains a character other than
   an ASCII digit (apart from a single leading `-` and trailing spaces), or, when
   the text does not end in a space, is longer than 63 characters. Examples:
   `2.0`, `2e0`, `0x1` and `abc` are refused.
5. A document is refused when any event attribute holds text that these rules
   refuse.

On save:

6. `BoolEvent/@Value` is written `true` or `false`. `EnumEvent/@Value` is written
   as a plain decimal integer.
7. Let P be 17 for `Time` and the curve controls and 9 for `FloatEvent/@Value`.
   Positive zero is written `0`. For any other value x:
   1. let k be the smallest integer not below log10|x| when |x| ≥ 1, and the
      largest integer not above log10|x| when |x| < 1;
   2. write x in fixed-point notation with max(0, P − k) digits after the
      decimal point, rounded from its exact binary value to nearest, ties to even
      (a binary32 value is first converted exactly to binary64);
   3. if the text contains `.`, remove trailing `0` characters and then a
      trailing `.`.

   Examples: L → `-63072000`; 4 → `4`; a `Value` read from `0.3` →
   `0.3000000119`; a `Time` read from `0.3` → `0.299999999999999989`; controls
   read from `0.8` and `0.2` → `0.800000000000000044` and `0.200000000000000011`.

These text rules are the same as the rules for Boolean, binary64, binary32 and
integer values in the transport-state-v1 release.

## Acceptance representation and comparison

[cases.json](cases.json) lists 21 cases. Each has one input fixture, an action
and an expected result:

| Field | Meaning |
| --- | --- |
| `action` | `open`; `open-save`: open, then save without other changes |
| `outcome` | `opens` or `refused` |
| `saved.envelopes` | `open-save` only. Per listed target (`Pan`, `Speaker` or `CrossFadeState` of the audio track), the saved envelope's events in order, each with its element name and its attributes other than `Id` |

Comparison rules:

- `outcome` compares exactly.
- Saved documents are compared as parsed XML: element names, nesting and
  attribute text, never bytes, whitespace, indentation, attribute order or
  quoting. For each listed target, the saved audio track's
  `AutomationEnvelopes/Envelopes` holds exactly one `AutomationEnvelope` whose
  `PointeeId` value equals the `Id` of the saved `AutomationTarget` of that
  parameter. Its `Events` children are the listed elements, in this order and
  number. Each carries exactly the listed attributes with exactly the listed
  text, plus an `Id` attribute whose presence and value are not compared.
  Anything else is not judged, including other envelopes and elements, the
  transform state and the parameters' `Manual` values.
- A refused case has no `saved` part.

This is a **project comparison representation**, not an API claimed to exist in
Live and not a required design. A candidate adapter may translate its own result
into these labels. Each case starts from its fixture alone. Reading and saving a
stored envelope have no timing tolerance, cancellation step or teardown within
this scope, so those case kinds are omitted.

## Reference comparison obligation (not executed)

A later comparison against the original application needs a full Live Set per
case. The validation analyst builds it from an otherwise unchanged Live Set of
the same format version, whose root carries the fixture's `MajorVersion`,
`MinorVersion` and `SchemaChangeCount` values, and which has an audio track and a
MIDI track whose session clip slot holds a MIDI clip. In that set the analyst:

- replaces the audio track's `AutomationEnvelopes/Envelopes` with the fixture's,
  and the `Manual` values of its `Speaker`, `Pan` and `CrossFadeState` with the
  fixture's;
- replaces the MIDI clip's `Envelopes/Envelopes` with the fixture's;
- sets each `PointeeId` to the `Id` of the corresponding target element of that
  set, and makes sure no other envelope names those targets.

Observations:

- `opens` and `refused` are judged by whether loading finishes without refusal.
  The wording of a refusal is not compared.
- For `open-save`, the set is saved without other changes and its decoded XML is
  compared under the rules above.

None of this has been run. Before claiming reference compatibility, run a
separately designed bounded probe for these cases or a justified equivalent set.
Pin the original and candidate builds and the fixture bytes, retain independent
observations and report mismatches. Candidate-only success proves agreement
with this contract, not with the running original.

## Exclusions and deferred obligations

Requirements not released: **REQ-AUTOMATION-ENVELOPES-004** (event Ids and their
part in envelope values), **REQ-AUTOMATION-ENVELOPES-010** (Float envelope
value), **REQ-AUTOMATION-ENVELOPES-011** (Bool and Enum envelope value) and
**REQ-AUTOMATION-ENVELOPES-013** (editing envelopes, automation override and
re-enable, recording, undo, the precedence of a parameter's `Manual` value over
its envelope, and the meaning of `LockEnvelope` and of stored transforms).

Inputs with **no expectation** in this release:

- a `PointeeId` that names no element, or names an element other than the
  target relations of REQ-AUTOMATION-ENVELOPES-002, including another track's
  parameter; two envelopes naming one target; repeated target Ids; target Ids
  not below `NextPointeeId`; a `LockEnvelope` other than `0`;
- events in time disorder; three or more events at one time; repeated or
  missing event Ids; an event without `Time` or `Value`; an event element that
  does not match its target's value kind;
- stored transforms: a pending transform or a non-empty
  `TimeAndValueTransforms`;
- values outside the ranges of REQ-AUTOMATION-ENVELOPES-003; event times below
  L, at or above 1,000,000, or not finite;
- curve controls outside [0, 1] or not satisfying K, and controls on the first
  or last event, on an event followed by one at the same time, or on an event
  whose next event has the same value;
- `Time`, curve control or `FloatEvent/@Value` text that, after leading spaces
  and an optional sign, starts with `0x` or `0X`, or with `inf` or `nan` in any
  letter case; the text `Invalid`; text starting with `#`; leading whitespace
  other than U+0020;
- `EnumEvent/@Value` text with spaces both before and after the digits, with a
  `+` and trailing spaces, or with a `-` sign, and such text longer than 63
  characters that ends in a space;
- the main track's tempo and time-signature envelopes; envelopes of other
  tracks, devices, modulation targets and other MIDI controller targets; audio
  clip envelopes;
- elements outside `AutomationEnvelope` and `ClipEnvelope` that use the same
  `Events` shape, such as the timelines of arrangement clips;
- any other format version, root attribute or compressed container;
- documents that break more than one rule of this release.

Excluded behavior:

- the value an envelope supplies to its parameter at any time, for Float, Bool
  and Enum envelopes, track and clip envelopes alike
  (REQ-AUTOMATION-ENVELOPES-010 and 011), including at event times, after the
  last event and between equal values, and whether event Ids affect it
  (REQ-AUTOMATION-ENVELOPES-004);
- whether opening replaces controls that do not satisfy K by 0.5;
- whether a save keeps or renumbers event and target Ids, the saved transform
  state, saved negative zero, whether a save writes envelopes that hold a
  single event, and whether a save keeps a leading event whose value differs
  from the next event's value;
- editing, override, recording and undo (REQ-AUTOMATION-ENVELOPES-013);
- texts, dialogs and logging of a refusal, and the state after it;
- audio rendering, smoothing, scheduling and timing.

## Fixture provenance

All 21 fixtures were authored for this release from one template written for
it. The template is the declaration, the root element with the three attributes
above, and a `LiveSet` holding `NextPointeeId` with the value 40 and two tracks:

- `AudioTrack Id="1"` with an `AutomationEnvelopes/Envelopes` list and a
  `DeviceChain/Mixer` holding `Speaker` (`Manual` `true`, `AutomationTarget`
  Id 21), `Pan` (`Manual` `0`, `MidiControllerRange` −1 to 1, `AutomationTarget`
  Id 22) and `CrossFadeState` (`Manual` `1`, `AutomationTarget` Id 23);
- `MidiTrack Id="2"` with a `DeviceChain/MainSequencer` holding a session clip
  slot whose `MidiClip` has an `Envelopes/Envelopes` list, and
  `MidiControllers/ControllerTargets.6` with Id 31.

All Ids are invented. The `Manual` values, the controller range and the clip's
`LoopSlot` and `ScrollerTimePreserver` values only give the elements their
usual shape; they are not judged. Each fixture is the template with the
envelopes that its purpose states. Text is ASCII with line-feed line endings
and tab indentation. The 21 inputs are distinct.

No fixture contains shipped file content, program code, schema content or
assets. Expected results are newly authored static-derived behavioral data. No
public source or dependency is approved or included. Review status is recorded
in [the manifest](manifest.json) and [the review disposition](REVIEW.md).
