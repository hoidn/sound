---
id: SPEC-AUTOMATION-ENVELOPES
type: spec
status: draft
revision: 1
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Automation envelopes in Live Set documents

## Scope

Feature FEAT-AUTOMATION, with FEAT-PERSISTENCE, in the [feature map](feature-map.md).
User task: open a Live Set whose tracks and clips carry automation, have each
automated parameter follow its envelope, and save the envelopes back. This draft
specifies:

- where a set stores track and clip envelopes, and how an envelope names its target;
- the event classes, their attributes, initial values and value kinds;
- the leading event at the lower time bound and the order of events;
- the checks that make a set with a malformed envelope fail to open;
- how curve controls are stored, omitted on save and reset on load;
- the value a Float, Bool or Enum envelope supplies at a given time.

Every requirement is a **proposed contract** supported by shipped bytes, by a static
derivation from the 12.4.3 program, or explicitly unknown. Nothing was run against
Live. [ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits a
static-first draft. Target: 12.4.3, documents with `MinorVersion="12.0_12402"`. The
gzip/XML envelope belongs to [SPEC-ALS-CONTAINER](als-container.md); value text rules
come from [SPEC-TRANSPORT-STATE](transport-state.md). Document examples are
fragments of the decoded XML.

**Excluded input.** A document in which an envelope's `PointeeId` names no target
element is outside this specification
([Q-020](../questions.md#q-020-automation-envelope-load-robustness), PRB-S6-02). So
is evaluation at a time before an envelope's first event (REQ-010, REQ-011). No
requirement constrains either input and no acceptance case uses one.

Excluded behavior: documents older than `12.0_12402` and their migration, editing
envelopes after load (drawing, override, re-enable, recording, undo; listed as
unknown in REQ-013), the arrangement clip timelines that reuse the event-list shape
(REQ-001), MPE per-note events, stored automation transforms, the clip envelope time
base (REQ-010), smoothing between evaluated values in audio processing, and the
text of error messages.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema files and the 4,120 parsed documents of the 12.4.3 bundle. These were written by Live 12.4d1, 12.1d1 or older versions, not by a 12.4.3 save |
| S | Static derivation from the 12.4.3 executable or shipped bytes; not an observed run. An assumption is named beside the clause when one is needed |
| U | Unknown; no expected result, or a static expectation that must not be graded. The PRB ID names the probe that would settle it |

Only D and S clauses may enter a release. U clauses block the behavior they name.
"The set does not open" means the document reader stops with a read error, as in
SPEC-TRANSPORT-STATE. How Live presents it is U
([REQ-ALS-CONTAINER-009](als-container.md#req-als-container-009--failure-presentation-and-state), PRB-S6-01).

## Assumptions and definitions

| ID | Assumption | What rests on it |
| --- | --- | --- |
| A1 | A Float target interpolates in its stored units (no value conversion before interpolation). Static evidence shows such a conversion step whose per-target form is unknown | Interior-time expected values of REQ-010 cases; these are U-graded until PRB-S6-04 |
| A2 | With arrangement automation active and not overridden, a parameter's effective value at song time t is the envelope value E(t) of its track envelope | Every evaluation case (comparator) |

- **L** is the lower time bound, −63,072,000 beats (`Time="-63072000"`).
- **E(t)** is the value an envelope supplies to its target at time t: song time in
  beats for track envelopes (unit inferred from shipped sets), clip time for clip
  envelopes (REQ-010).
- A **step** is two adjacent events with the same time.

## Requirements

### REQ-AUTOMATION-ENVELOPES-001 — envelope containers

- **D.** A track's arrangement automation is a list of `AutomationEnvelope`
  elements in the track's `AutomationEnvelopes/Envelopes`. The schema gives this list
  to `AudioTrack`, `MidiTrack`, `GroupTrack`, `ReturnTrack`, `MainTrack` and
  `PreHearTrack`.
- **D.** A clip's automation and modulation is a list of `ClipEnvelope` elements in
  the `Envelopes/Envelopes` child of an `AudioClip` or `MidiClip`. A `ClipEnvelope`
  also holds `LoopSlot` and `ScrollerTimePreserver`, which this spec does not cover.
- **D.** Both carry an `Id` attribute and, in this order, `EnvelopeTarget` with a
  `PointeeId` child element, and `Automation` with `Events` (the event list) and
  `AutomationTransformViewState`:

  ```xml
  <AutomationEnvelope Id="0">
    <EnvelopeTarget><PointeeId Value="323" /></EnvelopeTarget>
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

- **D.** 4,361 of 4,365 shipped envelopes have the empty transform state above.
  **U.** The meaning of a stored `TimeAndValueTransform` (4 shipped); fixtures use the
  empty form.
- **D.** `ClipTimeable/ArrangerAutomation`, `Sample/ArrangerAutomation` and
  `TakeLane/ClipAutomation` use the same `Events` shape for arrangement clips. They
  may be empty and have no event at L. They are not envelopes; REQ-005 to REQ-012
  do not apply to them.

### REQ-AUTOMATION-ENVELOPES-002 — envelope targets

- **D.** `PointeeId/@Value` equals the `Id` attribute of a target element in the same
  document. All 4,365 shipped envelopes resolve:
  - a track envelope names the `AutomationTarget` of a parameter of the same track
    (1,055 / 1,055);
  - a clip envelope names an `AutomationTarget` (2,888), a `ModulationTarget` (24),
    a `VolumeModulationTarget` (12) or a `MidiControllers/ControllerTargets.N`
    element (386; the schema has N from 0 to 130, shipped envelopes use N = 0, 1,
    6, 13, 18, 19, 20, 66 and 90).
- **D.** In every shipped Live Set (376), target-element Ids are unique and smaller
  than `LiveSet/NextPointeeId`. Presets and clip files repeat Ids and are out of scope.
- **S.** The binding is by Id alone; the position of the envelope in the list does not
  select the target.
- **D.** `LockEnvelope` is `0` on every shipped `AutomationTarget` and
  `ModulationTarget` and `1` only on `ControllerTargets.1`, `.11` and `.66`. **U.** Its
  meaning (REQ-013).
- **Excluded (Q-020).** A `PointeeId` that matches no element `Id`, one that names an
  element other than the targets above, and a track envelope naming another track's
  parameter. The reference behavior is unknown (PRB-S6-02). Fixtures keep every
  `PointeeId` resolvable within the shipped relations.

### REQ-AUTOMATION-ENVELOPES-003 — event classes and value kinds

- **D.** The event element follows the target's value kind: `FloatEvent` for Float
  parameters (continuous parameters, tempo, modulation and MIDI controller targets),
  `BoolEvent` for Bool parameters (for example `Speaker`), `EnumEvent` for Enum
  parameters (for example `CrossFadeState` and the time signature). This holds in
  4,365 / 4,365 shipped envelopes. The schema declares the kind: `TimeableFloat`,
  `TimeableBool` and `TimeableEnum` parameters, and Float for modulation and
  controller targets.
- **D.** Attributes: every event has `Id` and `Time` (64-bit). `FloatEvent` has
  `Value` (32-bit) and the optional curve controls of REQ-008 (64-bit). `BoolEvent`
  has `Value` `true` or `false`. `EnumEvent` has an integer `Value`.
- **D, units inferred.** Values are in the parameter's own units: BPM for tempo,
  the time-signature code of
  [REQ-TRANSPORT-STATE-010](transport-state.md#req-transport-state-010--time-signature-code),
  −1 to 1 for modulation targets, 0 to 127 for most MIDI controller targets and
  −3,200 to 8,191 for `ControllerTargets.0`.
- **U.** An event class that does not match the target kind. Not shipped; no probe;
  excluded from fixtures.

### REQ-AUTOMATION-ENVELOPES-004 — event Ids and missing attributes

- **D.** Every shipped event carries an `Id` that is unique within its list. Id order
  differs from document order in 250 track and 1,441 clip envelopes.
- **S.** Ids play no part in ordering or evaluation; REQ-010 and REQ-011 use document
  order.
- **U.** Two events with the same `Id` in one list, and whether a save keeps or
  renumbers Ids: PRB-S6-07. An event without `Id`: no probe yet (a variant of
  PRB-S6-07 is proposed).
- **U.** An event without `Time`, or a `FloatEvent` or `EnumEvent` without `Value`:
  PRB-S6-07. Static reading, not graded: the attribute keeps its unset initial
  value (Time the largest finite double, written `Invalid`; Float value the largest
  finite 32-bit float; Bool `false`; Enum −2,147,483,648), and a first event
  without `Time` fails the time check of REQ-007.

### REQ-AUTOMATION-ENVELOPES-005 — the leading event at the lower time bound

- **D.** In every shipped envelope (1,055 track, 3,310 clip) the first event is at L
  and no other event is at L. Every shipped clip envelope has at least two events.
- **D.** In every shipped envelope with more than one event (303 track, 3,310 clip)
  the leading event's value equals the next event's value. It equals the target's
  `Manual` value in only 126 of 303 track and 1,138 of 2,888 clip-parameter
  envelopes, so `Manual` is not the rule.
- **D.** One-event envelopes occur only as the main track's tempo (`FloatEvent`) and
  time-signature (`EnumEvent`) envelopes, 376 each, with the value of `Manual`
  (752 / 752).
- **D, writer rule inferred.** A writer puts an event at L first, with the value of
  the next event. **U.** Whether a 12.4.3 save always writes the one-event tempo and
  time-signature envelopes (PRB-N1-07); their precedence over `Manual` is
  [REQ-TRANSPORT-STATE-012](transport-state.md#req-transport-state-012--precedence-between-stored-tempo-and-meter-sources).
- **S.** The leading event is an ordinary event for REQ-010 and REQ-011. Because its
  value equals the next event's value, E(t) before the first ordinary event is that
  value. A different leading value makes a ramp across about 63 million beats
  (case AEN-018).

### REQ-AUTOMATION-ENVELOPES-006 — event order and steps

- **D.** Shipped events are in non-decreasing time order (4,365 / 4,365). At most two
  events share a time (steps: 5,372 track and 12,378 clip pairs; 40 and 162 of them
  repeat the value).
- **D.** No track envelope has an event at a negative time other than L. Clip
  envelopes have 335 such events (down to −130.5), and 327 of 3,310 clip envelopes
  have events outside the clip's `LoopStart`–`LoopEnd`.
- **S.** REQ-010 and REQ-011 take events in document order and presume
  non-decreasing times. No reordering on load was found.
- **U.** Events out of time order: sorted, kept or refused, and the resulting values
  (PRB-S6-03, case AEN-030). Three or more events at one time: not shipped, no
  probe, excluded from fixtures.

### REQ-AUTOMATION-ENVELOPES-007 — load checks

- **S.** A Live Set does not open when the `Events` list of any track or clip envelope
  is empty.
- **S.** A Live Set does not open when the first event of any track or clip envelope
  has a time other than L or 0. Times are compared as 64-bit values after REQ-012
  text conversion, so `-0` counts as 0.
- **S.** Only the first event's time is checked. Later events at any time pass this
  check.
- **S.** The check covers `AutomationEnvelope` and `ClipEnvelope` only, not the clip
  timelines of REQ-001.
- **U.** What the user sees (PRB-S6-01). A first event at 0 leaves times before 0
  without a defined value (REQ-010 exclusion).

### REQ-AUTOMATION-ENVELOPES-008 — curve controls: storage and save

- **D.** Curve controls are the `FloatEvent` attributes `CurveControl1X`,
  `CurveControl1Y`, `CurveControl2X` and `CurveControl2Y`. In 4,151 shipped events
  they appear as a full set of four, never on the leading or last event, never on an
  event followed by one at the same time, and only where the next value differs.
  X controls lie in [0, 1], `CurveControl1Y` in [0, 1.0596] and `CurveControl2Y`
  in [0, 1].
- **S.** A missing control reads as 0.5. An event whose four controls all equal 0.5
  has no curve, and its segment is linear (REQ-010).
- **S.** The controls shape the segment from their event to the next event.
- **S.** On save, each control equal to exactly 0.5 is omitted, independently of the
  other three. The others are written with the 64-bit rule of REQ-012. A linear event
  therefore has no control attributes, and a curve with some controls at 0.5 is
  written with fewer than four.

### REQ-AUTOMATION-ENVELOPES-009 — curve normalization on load

For control values c1, c2, let M(c1, c2) be true when the cubic Bézier coordinate
(0, c1, c2, 1) is monotone on [0, 1], decided as follows:

1. false if c1 or c2 is not finite;
2. true if 0 ≤ c1 ≤ c2 ≤ 1;
3. otherwise false if c1², c2² or c1·c2 overflows; else let
   D = c1² + c2² − c1·c2 − c1, and true if D ≤ 2⁻⁵² (no sign change of the
   derivative);
4. otherwise let q = 2(3c1 − 3c2 + 1), a = c2 − 2c1, r1 = (2√D − 2a)/q and
   r2 = (−2√D − 2a)/q; false if 0 < r1 < 1; else true exactly when r2 ≤ 0 or
   r2 ≥ 1 (a NaN r2 gives false).

- **S.** When the load-time normalization runs, an event keeps its controls when
  M(x1, x2) and M(y1, y2) both hold. Otherwise all four become 0.5: the segment is
  linear and no control is written on save (REQ-008).
- **S.** All 4,151 shipped curves pass, including the 315 with x1 > x2 and the 7 with
  a Y control above 1.
- **U.** Whether opening a Live Set runs the normalization (PRB-S6-05). Monotone
  controls are kept either way, so cases AEN-012 and AEN-013 do not depend on it.

### REQ-AUTOMATION-ENVELOPES-010 — Float envelope value

Events e0 … en in document order, with times tᵢ (64-bit) and values vᵢ (32-bit),
and t ≥ t0:

1. If t > tn, E(t) = vn (hold).
2. If an event has tᵢ = t, E(t) = vᵢ. At a step at t, E(t) is the value of the first
   or of the second event, chosen by the consumer (U).
3. Otherwise let a be the last event with time < t and b the first with time > t.
   - If va = vb (as 32-bit values), E(t) = va.
   - Else, if a has a curve (REQ-008): with Δt = tb − ta and Δv = vb − va, take the
     Bézier P0 = (ta, va), P1 = (ta + x1·Δt, va + y1·Δv), P2 = (ta + x2·Δt,
     va + y2·Δv), P3 = (tb, vb). Find s in [0, 1] with |X(s) − t| ≤ 10⁻⁸ beats;
     E(t) = Y(s) as a 32-bit value.
   - Else f = (t − ta)/(tb − ta) and E(t) = va − f·va + f·vb in 64-bit arithmetic,
     rounded to 32 bits.

- **S.** Rules 1–3 and their order.
- **U.** The interpolation domain. The program converts values per target before
  interpolating, and the per-target conversion is unknown. Under A1, the curve and
  linear rules of step 3 give stored units. Cases with interior times are not graded until PRB-S6-04
  settles the domain; PRB-S6-04 reads Volume and needs a Pan variant for these cases.
- **U.** Values outside the target's range, and any clamping of E(t) (PRB-S6-04).
  Fixtures keep values in range.
- **U.** Which value applies at a step (PRB-S6-06).
- **U.** The clip envelope time base relative to clip start, loop and warp
  (proposed PRB-S6-11). The cases use track envelopes only.
- **Excluded (Q-020).** t < t0, possible only when the first event is at 0.

### REQ-AUTOMATION-ENVELOPES-011 — Bool and Enum envelope value

- **S.** Bool and Enum envelopes do not interpolate. For t ≥ t0 that is not an event
  time, E(t) is the value of the last event with time < t, which holds after the last
  event.
- **S.** At an event time t, E(t) is either the value of the last event at t or the
  value of the last event before t, chosen by the consumer. **U.** Which consumer
  uses which (PRB-S6-06).
- **S.** This applies to the time-signature envelope as well. Its effect on the meter
  is [REQ-TRANSPORT-STATE-012](transport-state.md#req-transport-state-012--precedence-between-stored-tempo-and-meter-sources) (U).
- **Excluded (Q-020).** t < t0.

### REQ-AUTOMATION-ENVELOPES-012 — event number text

- **S.** On load, `Time` and the curve controls follow
  [REQ-TRANSPORT-STATE-004](transport-state.md#req-transport-state-004--loop-and-position-number-text-on-load),
  `FloatEvent/@Value` follows
  [REQ-TRANSPORT-STATE-005](transport-state.md#req-transport-state-005--tempo-text-on-load)
  (32-bit), `BoolEvent/@Value`
  [REQ-TRANSPORT-STATE-003](transport-state.md#req-transport-state-003--loop-switch-text-on-load)
  and `EnumEvent/@Value`
  [REQ-TRANSPORT-STATE-006](transport-state.md#req-transport-state-006--time-signature-code-text-on-load).
  Text those rules reject means the set does not open.
- **S, corroborated by D.** On save, numbers follow
  [REQ-TRANSPORT-STATE-011](transport-state.md#req-transport-state-011--number-text-on-save):
  P = 17 for `Time` and curve controls, P = 9 for `FloatEvent/@Value`. All 149,716
  shipped `FloatEvent` values reproduce under that rule. Examples: `-63072000`;
  32-bit 0.3 → `0.3000000119`; 64-bit 0.3 → `0.299999999999999989`; 0.8 →
  `0.800000000000000044`.

### REQ-AUTOMATION-ENVELOPES-013 — editing, override, recording and undo

- **U.** Precedence of a parameter's `Manual` value over its envelope on open: for
  tempo and meter PRB-N1-04 and 05; for other parameters proposed PRB-S6-08.
- **U.** Automation override (a manual change while an envelope exists),
  re-enabling, and whether a set stores that state: proposed PRB-S6-08.
- **U.** Recording automation: events, Ids, leading event and steps written by a
  recording pass (proposed PRB-S6-09).
- **U.** Undo and redo of envelope edits (proposed PRB-S6-10).
- **U.** The meaning of `LockEnvelope` (REQ-002) and of stored transforms (REQ-001):
  no probe proposed.

## Timing and state

- Units: times in beats (inferred), song time for track envelopes. `Time` is held
  in 64 bits and values in 32 bits; E(t) is a 32-bit value (REQ-010).
- E(t) is a deterministic function of the stored events. No real-time behavior,
  latency, scheduling granularity or audio-rate smoothing is specified.
- Persistent state: envelopes as stored. Load may reset non-monotone curves
  (REQ-009, U whether it runs) and refuse malformed envelopes (REQ-007, REQ-012).
  Save omits controls equal to 0.5 (REQ-008). Id handling on save is U (REQ-004).
- Edits, override, recording and undo are U (REQ-013).

## Acceptance cases

None of these cases has been run against Live or a candidate. Expectations are
static derivations or document facts. Kinds: P positive, N refusal, B boundary,
M missing or malformed, S save, V value. Basis: D, S (with assumptions), or U (not
graded; the expectation, if any, is a static reading only).

### Fixtures

- **B0:** `Core Library/Lessons/Sets/Recording Audio.als`, SHA-256
  `af57ff8f9eb1c2c51220ef6633a58838532350d53640df5f48dc01659023c043`,
  `MinorVersion="12.0_12402"`. Decode, change only as stated, re-encode as gzip.
  Track `1-Audio` (`AudioTrack Id="0"`) has `<AutomationEnvelopes><Envelopes /></AutomationEnvelopes>`
  and the targets Pan `AutomationTarget Id="323"` (Float, `Manual` 0, range −1 to 1),
  Speaker `322` (Bool, `Manual` true) and CrossFadeState `325` (Enum, `Manual` 1,
  range 0 to 2). The main track holds the one-event envelopes
  `PointeeId 340` (tempo, `<FloatEvent Id="0" Time="-63072000" Value="120" />`) and
  `341` (time signature, `<EnumEvent Id="0" Time="-63072000" Value="201" />`).
  `NextPointeeId` is 2776.
- **"B0 + Ek"** appends to that track's `Envelopes` the `AutomationEnvelope` shown in
  REQ-001 with `PointeeId` set to Ek's target and `Events` holding Ek's events, Ids
  0, 1, 2 … in order unless stated.
- **B1:** `Core Library/Templates/Quick Start Song.als`, SHA-256
  `3b9a87d67a3c6eac07a17a6ccf09f56234db3fc0adccb8adbd36f34bc4e20ef9`. Its only clip
  envelope, `ClipEnvelope Id="15"` in a MIDI clip of `MidiTrack Id="48"`, targets
  `ControllerTargets.6` (`PointeeId 277263`) with
  `<FloatEvent Id="76" Time="-63072000" Value="127" />` and
  `<FloatEvent Id="78" Time="0" Value="127" />`.
- **B2:** `Core Library/Lessons/Demo Songs/Chuck Sutton - Patience (Live 12 Suite Demo).als`,
  SHA-256 `3f1c0f924b750c2adba2525838f2bc00856e52faea09d43b9279c6a0fe40952b`,
  unchanged.

Event lists, written as (Time, Value) for `FloatEvent` unless stated:

| ID | Target | Events |
| --- | --- | --- |
| E1 | Pan 323 | (−63072000, 0), (4, 0), (8, 1) |
| E2 | Pan 323 | (4, 0) |
| E3 | Pan 323 | none: `<Events />` |
| E4 | Pan 323 | (0, 0), (4, 1) |
| E5 | Pan 323 | (−0, 0), (4, 1), the first written `Time="-0"` |
| E6 | Pan 323 | (−63071999, 0), (4, 1) |
| E7 | Pan 323 | (−63072000, 0), (−10, 0.5), (4, 1) |
| E8 | Pan 323 | (−63072000, 1), (4, 1), (4, −1), (8, −1) |
| E9 | Pan 323 | (−63072000, −1), (0, −1) with `CurveControl1X="0.5" CurveControl1Y="0" CurveControl2X="0.5" CurveControl2Y="0"`, (4, 1) |
| E10 | Pan 323 | as E9 but controls `0.2`, `1.5`, `0.8`, `-0.5` (1X, 1Y, 2X, 2Y) |
| E11 | Pan 323 | as E9 but controls `0.8`, `0`, `0.2`, `1` |
| E12 | Pan 323 | (−63072000, 0), (0, 0), (3, 1) |
| E13 | Pan 323 | (−63072000, 1), (4, 0) |
| E14 | Speaker 322 | `BoolEvent`: (−63072000, `true`), (4, `false`), (8, `true`) |
| E15 | CrossFadeState 325 | `EnumEvent`: (−63072000, 1), (4, 0), (8, 2) |
| E16 | Pan 323 | (−63072000, 0.3), (0.3, 0.3) |
| E17 | Pan 323 | (−63072000, 0), (4, `abc`) |
| E18 | Pan 323 | (−63072000, 0), (8, −0.5), (4, 0.5), in this document order |
| E19 | Pan 323 | (−63072000, 0), then `<FloatEvent Id="1" Value="0.5" />` (no `Time`) |
| E20 | Pan 323 | (−63072000, 0), then `<FloatEvent Id="1" Time="4" />` (no `Value`) |
| E21 | Pan 323 | (−63072000, 0), (4, 0.5), both with `Id="0"` |

Value comparator: open the set with the transport stopped and arrangement
automation active, move the song position to t, and read the target's value (A2).
Float values match exactly at 32-bit precision, except curve values, which match
within 10⁻⁶. "Opens" and "does not open" are judged by whether loading finishes.
Saved text is compared per attribute value; Ids are not compared (REQ-004).

| Case ID | Req | Kind | Setup/action | Expected result | Basis |
| --- | --- | --- | --- | --- | --- |
| AEN-001 | 001, 002, 005, 008 | P | Open B2 | Opens. 83 track and 468 clip envelopes; every first event at L; every `PointeeId` resolves; 1,071 events carry curve controls | D (document), S (opens) |
| AEN-002 | 005 | P | Open B0 | Opens. The main track's two envelopes each hold one event at L, values 120 and 201 | D (document), S (opens) |
| AEN-003 | 001–003, 012 | P, S | B0 + E1; open, save | Opens. The saved track has one envelope with `PointeeId` 323 and events `Time`/`Value` `-63072000`/`0`, `4`/`0`, `8`/`1` in that order | S |
| AEN-004 | 007 | N | B0 + E2; open | Does not open | S |
| AEN-005 | 007 | N | B0 + E3; open | Does not open | S |
| AEN-006 | 007 | B | B0 + E4; open | Opens | S |
| AEN-007 | 007 | B | B0 + E5; open | Opens | S |
| AEN-008 | 007 | N | B0 + E6; open | Does not open | S |
| AEN-009 | 007 | B | B0 + E7; open | Opens | S |
| AEN-010 | 007 | N | B1; delete the event `Id="76"` and set the other event's `Time` to `4`; open | Does not open | S |
| AEN-011 | 007 | N | B1; replace the clip envelope's `Events` with `<Events />`; open | Does not open | S |
| AEN-012 | 008, 009 | S | B0 + E9; open, save | The saved `Time="0"` event carries `CurveControl1Y="0"` and `CurveControl2Y="0"` and no `CurveControl1X` or `CurveControl2X` | S |
| AEN-013 | 008, 009, 012 | S | B0 + E11; open, save | The saved `Time="0"` event carries `CurveControl1X="0.800000000000000044"`, `CurveControl1Y="0"`, `CurveControl2X="0.200000000000000011"`, `CurveControl2Y="1"` | S |
| AEN-014 | 009 | S | B0 + E10; open, save | Static reading: the saved `Time="0"` event has no curve controls and E(2) = 0 | U (PRB-S6-05; value also A1) |
| AEN-015 | 010 | V | B0 + E1; read t = 0, 2, 4, 12, 100 | 0, 0, 0, 1, 1 | S (A2) |
| AEN-016 | 010 | V | B0 + E1; read t = 5, 6, 7 | Static reading: 0.25, 0.5, 0.75 | U (PRB-S6-04, A1) |
| AEN-017 | 010 | V | B0 + E12; read t = 1 | Static reading: 0.3333333432674408 (32-bit) | U (PRB-S6-04, A1) |
| AEN-018 | 005, 010 | B, V | B0 + E13; read t = 0 and t = 4 | t = 4: 0 (S, A2). t = 0, static reading: 6.341958e−8 (the ramp from L ends at 4) | S (A2); t = 0 U (PRB-S6-04, A1) |
| AEN-019 | 006, 010 | V | B0 + E8; read t = 2, 6, 10 | 1, −1, −1 | S (A2) |
| AEN-020 | 010 | V | B0 + E8; read t = 4 | 1 or −1 by consumer | U (PRB-S6-06) |
| AEN-021 | 010 | V | B0 + E9; read t = 0, 4, 6 | −1, 1, 1 | S (A2) |
| AEN-022 | 010 | V | B0 + E9; read t = 1, 2, 3 | Static reading: −0.983523965, −0.75, 0.0164760482 (linear would give −0.5, 0, 0.5) | U (PRB-S6-04, A1) |
| AEN-023 | 011 | V | B0 + E14; read t = 0, 2, 6, 10 | `true`, `true`, `false`, `true` | S (A2) |
| AEN-024 | 011 | V | B0 + E14; read t = 4 and t = 8 | `false` and `true` (last event at t), or `true` and `false` (last event before t), by consumer | U (PRB-S6-06) |
| AEN-025 | 011 | V | B0 + E15; read t = 2, 6, 12 | 1, 0, 2 | S (A2) |
| AEN-026 | 012 | S | B0 + E16; open, save | Saved values `0.3000000119` (both events); saved second `Time` `0.299999999999999989` | S |
| AEN-027 | 012 | M | B0 + E17; open | Does not open | S |
| AEN-028 | 004 | M | B0 + E19; open, save | Unresolved | U (PRB-S6-07) |
| AEN-029 | 004 | M | B0 + E20; open, save | Unresolved | U (PRB-S6-07) |
| AEN-030 | 006 | M | B0 + E18; open, read t = 2, 6, 10, save | Unresolved | U (PRB-S6-03) |
| AEN-031 | 004 | M | B0 + E21; open, save | Unresolved | U (PRB-S6-07) |

31 cases: 20 gradable (2 with a D document part), 10 unresolved (AEN-014, 016, 017,
020, 022, 024, 028–031), and AEN-018 partly unresolved. No case uses an excluded
input (dangling target, time before the first event). Cancellation and teardown are
omitted: reading and evaluating envelopes has no cancellable step or resource in
this scope. Refusal presentation is not graded (PRB-S6-01).

## Open questions

- [Q-020](../questions.md#q-020-automation-envelope-load-robustness): dangling
  `PointeeId` (PRB-S6-02); unsorted events (PRB-S6-03); missing `Time` or `Value`
  and duplicate Ids (PRB-S6-07). Evaluation before an envelope's first event is a
  further gap of the same kind: possible when the first event is at 0, untraced in
  the reference, excluded here.
- Refusal presentation (PRB-S6-01), curve normalization on open (PRB-S6-05), the
  interpolation domain and range handling (PRB-S6-04), the value at steps and at
  Bool event times (PRB-S6-06).
- Proposed probes not yet in the S6 probe batch. Each uses B0 + E1:
  - PRB-S6-08: read Pan at t = 6, set Pan by hand, read again, re-enable automation,
    save; settles `Manual` precedence, override and its persistence.
  - PRB-S6-09: record Pan automation for four beats, save; settles the recorded
    events.
  - PRB-S6-10: delete the event at 8, undo, save; settles undo.
  - PRB-S6-11: put E1 on a clip with `LoopStart` 4, play, read Pan; settles the clip
    time base.
  - A Pan reading of E1, E9 and E12 added to PRB-S6-04, an event without `Id`
    added to PRB-S6-07.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical evidence:
[automation envelopes](../research/automation-envelopes.md) (packet S6), retained run
`analysis/ableton-live-12.4.3/r2/s6-automation-v1/` (image SHA-256
`3a99ceea…d1c383cfad`, Ghidra 12.1.4; dossiers `results/s6-0001` to `s6-0003`;
`documents-survey.json`, `schema-survey.json`, `curve-check.json`,
`probe-batch.json`). This draft issued no new queries: every function cited below
was re-read from the retained dossiers or `corpus-excerpts.jsonl`. "✓" marks a
branch confirmed in retained disassembly. Case values were computed with the
functions of `curve_check.py` plus the REQ-TRANSPORT-STATE-011 formatter (scratch
derivation, not retained).

| Requirement | Evidence | Strength |
| --- | --- | --- |
| 001 | `schema-survey.json` `segments`, `holder_fields`, class lines 839/843/1220/3793 of `12.0_12402.txt`; survey `containers`, `transform_state` | D |
| 002 | survey `target_resolution`, `target_same_track`, `duplicate_target_ids`, `next_pointee_id_vs_max_target`, `target_lockenvelope`; lookup by Id in `0x101535e0c` ✓ (s6-0003); `PointeeId` member registered at `0x101535b34` | D; S for binding by Id |
| 002 exclusion | `0x101535e0c` ✓: missing Id logs `Invalid Pointee ID {id} in APtr`, then `0x1054147b8` ✓ asserts `mpObject` (`APtr.cpp`) and calls `abort`. Whether load dereferences targets is untraced | Excluded (Q-020) |
| 003 | survey `event_tag_vs_target_kind`, `bool_tokens`, `enum_value_is_int`, `minmax`; `AFloatEvent` registry `0x1027782ec` (Value, CurveControl*), event base `0x1024deaf8` (Time) | D; units inferred |
| 004 | survey `event_id_present`, `event_id_unique`, `event_ids_increasing_with_order`; constructors `0x1024deba8` ✓ (Time DBL_MAX), `0x1027785a0` ✓ (Value FLT_MAX, controls 0.5), `0x102777adc` ✓ (Bool false), `0x102777f3c` ✓ (Enum INT_MIN); generic loader `0x101487310` (N1) stores present attributes only | D; U for effects |
| 005 | survey `first_time`, `low_elsewhere`, `multi_event_low_value_equals_next`, `multi_event_low_value_equals_manual`, `one_event_params`, `one_event_value_equals_manual`; legacy translator `0x101492afc` (pseudocode) inserts the leading copy | D; writer rule inferred |
| 006 | survey `sorted`, `max_events_same_time`, `equal_time_adjacent_pairs`, `negative_non_low`, `clip_time_check`; `AListAutomation` +0xd0 generic `0x101486fa8`, +0x100 no-op `0x101487c3c`, change handler `0x102565f84` widens a range only (vtable-reads.txt, corpus) | D; S (no sort found, not exhaustive) |
| 007 | validate `0x102561a28` ✓ (s6-0001): empty list → `Automation has no events.`; first time ≠ −63072000 (`0xc18e133800000000`) and ≠ 0.0 → `First automation event has invalid time.`, both via `0x101488e64`. Reached from `AAutomationEnvelope` +0x100 `0x1024050d8` ✓ and `AClipEnvelope` +0x100 `0x10245194c` ✓ (s6-0003), called by the unconditional post-order walk `0x101487198` ✓ in `0x101486fe4` ✓ (s6-0002), whose caller `0x101484108` is the XML reader of the general document reader ([document container native](../research/document-container-native.md#reader-entry-points-and-stream-detection)) | S; presentation U |
| 008 | survey `curve_attr_count`, `curve_position`, `curve_next_value_differs`, `minmax`; save predicate `0x102778828` ✓ (`*p == 0.5` for each control), consulted per attribute member by the generic writer `0x101486cdc` (N1 n1-0008 pseudocode: member skipped when slot +0x150 returns true); has-curve `0x1027778a4` ✓ | D; S |
| 009 | post-load hook `0x102778870` ✓ (`AFloatEvent` slot +0xd0): monotone test `0x1012132d8` ✓ on (0, x1, x2, 1) and (0, y1, y2, 1), else four 0.5. Slot +0xd0 runs only when `0x1015192c0(context)` is true in `0x101486fe4` ✓; that flag for a Live Set open is untraced. `curve-check.json`: 4,151 / 4,151 kept | S; U for enablement |
| 010 | evaluator `0x1024095b4` ✓ (s6-0001) via `0x1024094c0` (corpus); search `0x102565974` ✓, `0x102565a48`, walker `0x1025669d8`; has-curve `0x1027778a4` ✓; curve points `0x102403c88` (pseudocode); value at t `0x102404218` (pseudocode); bisection `0x101212e30` ✓ (tolerance `0x3e45798ee2308c3a` = 1e−8) | S; domain U |
| 010 domain | Linear, hold and equal-value results pass through `0x101574bb0`: with a converter object it calls the converter's slot +0x28 (min, max); without one it returns the value unchanged (corpus pseudocode). The full-range transform record built by `0x102778c98` makes `0x102779088` and `0x102778f50` identities. The curve branch reads values through `0x102778d28` (not in the retained evidence), not the converter, and clamps to the provider's [min, max] in `0x102404218` | U (A1) |
| 011 | discrete value `0x10240a84c` ✓; search `0x102565e10` ✓; interpolator ownership by `vtable_owner.py` (`interpolator-owners.txt`, heuristic) | S |
| 012 | generic loader and member-type text conversion (N1: `0x101487310`, `0x10152bfb8`); formatter rule and `number-format-check.txt` (N1): 149,716 / 149,716 `FloatEvent` values | S, corroborated D |
| 013 | none traced | U |

Unguarded evaluation before the first event: in `0x1024095b4` ✓ the previous event
is null when the search returns the first event, and it is dereferenced without a
check; `0x10240a84c` returns the list head in the same situation. This is why
REQ-010 and REQ-011 exclude t < t0.

Further analyst notes, not carried into requirements:

- The linear branch has an exact-identity shortcut: when ta equals converted va and
  tb equals converted vb, it returns t. It agrees with the formula after 32-bit
  rounding except in rare cases.
- In the curve branch, segment endpoint times are rounded to a 1/3,843,840-beat
  grid unless they equal one of four special constants (`0x102404218`,
  `0x1024095b4`). The effect is below the case tolerance.
- Correction to the research page: it says unconverted values are "clamped to a
  range". The retained pseudocode shows no clamp on the linear, hold and equal-value
  paths when no converter object exists. A clamp was found only in the curve branch.

Not carried from the research candidates:

- AE-C09 (abort on an unresolvable target): replaced by the exclusion; a
  specification must not require a crash.
- AE-C12 (clamping of evaluated values): pseudocode only, curve branch only;
  REQ-010 lists range handling as U.
- AE-C16 (pre-10 translation): pseudocode only and out of scope (older documents
  excluded).
- AE-C02 target-Id uniqueness "as a requirement": kept as a document fact (D), not
  as a load obligation.
- Plug-in parameter envelopes: owner attribution is heuristic and no shipped set has
  one; not claimed.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from S6 (AE-C01 to AE-C17 except C09, C12 and C16): 13 requirements (1 D and S, 1 S only, 10 with U parts, 1 U only); 31 unexecuted cases, 10 unresolved and 1 partly unresolved; dangling targets and evaluation before the first event excluded (Q-020) |

Not reviewed and not released. A first handoff could carry REQ-008 and 012, the D
and S clauses of REQ-001 to 007 (002 with its exclusion), REQ-009's rule with cases
AEN-012 and 013, and the S clauses of 010 and 011 with the A2 cases (AEN-015, 019,
021, 023, 025 and AEN-018 at t = 4).
