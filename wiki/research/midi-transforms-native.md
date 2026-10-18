---
id: RESEARCH-MIDI-TRANSFORMS-NATIVE
type: research
status: draft
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64 (Live.arm64 SHA-256 3a99ceea…383cfad)
---

# MIDI map-mode transforms (native, N7)

**Question** (Q-009, [SPEC-MIDI-USER-MAPPING](../specs/midi-user-mapping.md)
REQ-MIDI-USER-005/010). The user-mapping script passes one of ten map-mode tokens
to native Live. Which native transform turns an incoming CC value, or a 14-bit
pair, into a parameter change? What are the pairing rule, relative sign
conventions and step sizes, takeover behavior and clamping?

**Answer.** All ten modes reach one native mapping path. Absolute sets
min + (max − min) × v/127. Absolute14Bit pairs CC n (MSB) with CC n+32 (LSB) in
either order and applies pair/16383. Each relative mode decodes the byte to a
signed delta d. Four "Linear" modes use the raw magnitude. Four "Accel" modes
map the magnitude through a fixed 8- or 9-entry table. The parameter moves by
(max − min) × d/256, clamped, or by one step when it is quantized. Takeover
(None, Pick-Up, Value Scaling) applies only to absolute modes on continuous
float parameters, and the crossfader opts out. These are **static derivations**
from disassembly. Nothing was executed.

## Evidence and method

Evidence: [n7-midi-transforms-v1](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/notes.md)
([manifest](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/manifest.json)).
Method: the Python call site was taken from the S4 listings, and the native path
was found through the strings, calls and decompiled-corpus indexes
([tooling](r2-corpus-tooling.md)). Material branches were then confirmed in 27
dossiers over four rounds on query server 1 (kept results n7-0001 to n7-0004), under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md). Constants were read
from the image (`out/native-constants.json`). On/off thresholds were counted in
the 26 shipped sets (`out/onoff-thresholds.json`).

Value path, all Observed in disassembly unless marked:

1. `_Framework/ControlSurface._install_mapping` L735–743 calls
   `Live.MidiMap.map_midi_cc_with_feedback_map(…, map_mode, feedback_rule,
   not needs_takeover, mapping_sensitivity)`. Python defaults are takeover needed
   and sensitivity 1.0 (`InputControlElement` L191, L197). Only the crossfader
   clears takeover (`GenericScript` L216).
2. The tokens map to the native enum `NRemoteMapperTypes::TControllerMapMode`
   (`elements_base` L27–47; registration 0x103b4ca90). The Accel tokens map to
   the plain relative modes (1–4) and the Linear tokens to the "smooth" modes
   (6–9). Live's own chooser labels, in enum order, read "Relative (Signed Bit)"
   … "Relative (lin. Signed Bit 2)" (strings at 0x105bce29b–0x105bce353).
3. The wrapper 0x103b4d744 forwards everything unchanged to 0x102593258. That
   function rejects a channel above 15, a CC above 127, and a CC of 96 or higher
   in 14-bit mode. It then builds the parameter details: Type, Min, Max,
   Quantized and Zoom = 1.0 (0x1026fa5c8/0x1026fa684). It installs a CC receiver
   or, in 14-bit mode, a pair receiver.
4. Each incoming CC first updates a per-input table of last values for each
   channel and controller. The table is filled with −129 when the input opens or
   is reset. The old value becomes the "prior" (0x101b65b68). Every receiver on
   that channel and CC is then called (0x101b7842c). The mode-to-handler binding
   goes through a handler registry (0x101b84798, 0x10260535c); the link to the
   MidiMap vtable is **Inferred**.
5. Apply (0x101b7fde4) → value function 0x101b76bf0 → takeover 0x101b7c508 →
   parameter setter. Off the expected thread, the same fields are queued as
   `OChangeControllerDataCommand` and applied later (timing **Unknown**).

Parameter classes (Observed, 0x1026fa684): Type 1 = `ATimeableFloat`, 2 =
`ATimeableBool`, 3 = `ATimeableEnum`, 0 = other. Min, Max and Quantized use the
same vtable slots as the Python `DeviceParameter.min`, `max` and `is_quantized`
getters. Quantized is also set by an internal flag of unknown meaning. For an
`ATimeableBool`, Min and Max come from its `MidiCCOnOffThresholds` range. A
registry lookup (0x1011aeb80) can suppress this; that lookup is unexplained.
Shipped sets carry Min 64 and Max 127 in 22,059 of 22,303 occurrences.

## Per-mode transform table

v is the 7-bit data byte. For relative modes, d is the decoded delta. Tables
(Observed, `out/native-constants.json`):

- A(k) = 1, 2, 3, 4, 5, 8, 10, 20, 50 for k = 1…9, and 20 for k ≥ 10 or k < 1.
- B(k) = 1, 2, 3, 4, 5, 8, 20, 50 for k = 1…8, and 50 otherwise.

| Token (native enum) | Transform | Label |
| --- | --- | --- |
| Absolute (0) | min + (max − min) × v/127; no clamp needed | Observed (0x101b76bf0) |
| Absolute14Bit (5) | MSB = CC n, LSB = CC n+32, same channel, n ≤ 95. Each half is held until the other arrives, in either order, and a newer half replaces a held one. On completion, (MSB<<7 \| LSB)/129 is applied as Absolute (= pair/16383), sensitivity 1, and both halves are cleared | Observed (0x101b8028c, 0x101b802bc, 0x101b7fcc0) |
| LinearSignedBit (6) | v ≤ 64 → d = +v; v ≥ 65 → d = −(v − 64) | Observed (0x101b7b96c) |
| LinearSignedBit2 (9) | v ≤ 64 → −v; v ≥ 65 → +(v − 64) | Observed |
| LinearTwoCompliment (8) | v ≤ 64 → +v; v ≥ 65 → v − 128 | Observed |
| LinearBinaryOffset (7) | d = v − 64 | Observed |
| AccelSignedBit (1) | v ≤ 64 → +A(v); v ≥ 65 → −A(v − 64); v = 0 → +20 | Observed |
| AccelSignedBit2 (4) | v ≤ 64 → −B(v); v ≥ 65 → +B(v − 64); v = 0 → −50 | Observed |
| AccelTwoCompliment (3) | v ≤ 65 → +B(v); v ≥ 66 → −B(128 − v); v = 0 → +50 | Observed |
| AccelBinaryOffset (2) | v ≥ 65 → +B(v − 64); v ≤ 63 → −B(64 − v); v = 64 → +50 | Observed |

Application of d (Observed, 0x101b76bf0, 0x101b7f894, 0x101b7fde4):

- **Continuous, not quantized.** The new value is
  clamp(current + (max − min) × d × s/256, min, max), with s = 1 for this script.
- **Quantized.** The receiver accumulates ±s per message and fires at |acc| ≥ 1,
  which is every message when s = 1. The value moves +1 when d·s > 0, otherwise
  −1, so d = 0 also gives −1. It is clamped, then rounded to the nearest integer
  with halves away from zero (`frinta`). Absolute values on a quantized parameter
  are rounded the same way. The decompiler's integer cast was wrong.
- **On/off (Type 2).** In absolute modes the parameter is on exactly when v lies
  between the threshold Min and Max, inclusive. The result is inverted when
  Min > Max. Relative modes turn it on when d·s > 0, otherwise off. There is no
  takeover. This is Observed in code; that the range is the thresholds is
  **Inferred**.

Edge results that look surprising but are confirmed in disassembly:
AccelSignedBit gives 20 rather than 50 for magnitudes of 10 and above;
AccelBinaryOffset 64 gives +50; AccelTwoCompliment 65 counts as positive; and a
zero delta moves a quantized parameter down.

Correction 2026-10-18 (midi-config-v3 review, F2/RV3-03): the quantized rule
above, and the matching proposed clause below, hold only when Min < Max. Apply
(0x101b80148) passes the value function the sorted bounds and a flag that is
set when Max < Min. With the flag set, the absolute branch uses t = (127 − v)/127
and the relative step is negated. The Absolute and non-quantized formulas
therefore hold for either order, clamped to the interval between the bounds.
A quantized parameter moves one unit toward Max when d·s > 0, which is down for
a reversed range. "Zero delta moves down" likewise means toward Min.
[Spec revision 4](../specs/midi-user-mapping.md) states this rule.

## Takeover

Takeover is evaluated (0x101b7c508) only when all of the following hold: the
mode is Absolute or Absolute14Bit, the parameter is `ATimeableFloat`, and the
control did not opt out. The crossfader opts out, so its receiver blanks the
prior (0x101b7f894). The 14-bit receiver's opt-out flag is fixed at false
(`mov w3,#0x0` at 0x102609548). Let c be the current value, clamped. Let n be
the new absolute value and p the value the prior CC would have produced.

- **Mode 0 (None):** n is applied.
- **Any other mode:**
  - If the prior is −129 (none since the input opened or was reset), the value
    stays at c.
  - If |p − c| ≤ (max − min)/256, n is applied.
- **Mode 1 (Pick-Up), out of sync:**
  - n is applied only if c lies in [min(n, p) − w, max(n, p) + w], where
    w = (max − min)/64.
  - Otherwise the value stays.
  - Every call posts `RemoteMapper.PickUpNotification`.
- **Mode 2 (Value Scaling), out of sync:**
  - If |n − c| ≤ w, n is applied. If p = n, the value stays.
  - Moving up: c + (max − c)(n − p)/(max − p).
  - Moving down: c − (c − min)(p − n)/(p − min).
- The result is clamped in every mode.

The step divisor is 128 even for 14-bit pairs, because the pair arrives as mode 0.

Labels: the arithmetic is Observed. The index-to-preference-label mapping is
**Inferred**: index 1 posts the pick-up notification, and the UI entries are
declared in the order None, Pick-Up, Value Scaling. The preference default, the
trigger that resets the prior table, and the first 14-bit pair are **Unknown**.
For that first pair the −129 priors combine to −1/129, which a static reading
treats as a prior near min; this is not proposed as a clause.

Correction 2026-10-18 (midi-config-v3 review, F1/RV3-02): the answer above and
the proposed S clause below say that the crossfader opts out of takeover. That
holds only for its non-14-bit mappings. Install 0x102593258 passes the opt-out
only to the CC receiver; its 14-bit call (0x10259338c) passes no opt-out, and the
pair receiver's flag is fixed at false, as stated above. A crossfader
`Absolute14Bit` pair therefore reaches takeover like any other control's pair.
[Spec revision 4](../specs/midi-user-mapping.md) narrows the exemption to
`Absolute` values.

## Proposed clauses for SPEC-MIDI-USER-MAPPING revision 3

These would replace the "Numeric transforms…" sentence of REQ-MIDI-USER-005
Unknown and the REQ-MIDI-USER-010 "the effect is N" phrase. Evidence labels
E10–E14 are new: E10 install and dispatch, E11 14-bit pairing, E12 value
function, decoder and tables, E13 parameter details and apply, E14 takeover. All
are in the n7 evidence tree.

- **S.** Each continuous control maps its channel and CC number to the target
  parameter with its map mode and sensitivity 1. Takeover is enabled for every
  continuous control except the crossfader. The mapping range is the
  parameter's reported minimum and maximum (E10, E13).
- **S. Absolute.** A value v sets min + (max − min) × v/127. A quantized
  parameter takes the nearest integer, with halves rounded away from zero (E12).
- **S. Absolute14Bit.** CC n carries the most significant and CC n+32 the least
  significant 7 bits on the same channel. A received half is held until the
  other half arrives, in either order, and a newer half replaces a held one. When
  both are held, the parameter is set to min + (max − min) × (MSB × 128 +
  LSB)/16383 and both halves are discarded (E11).
- **S. Relative.** Each message's value v gives a delta d by table R. A
  non-quantized parameter becomes clamp(current + (max − min) × d/256, min,
  max). A quantized parameter moves one step per message, +1 when d > 0 and −1
  otherwise, within its range (E12, E13). Table R is the per-mode table above.
- **S-cond. On/off parameters.** An absolute value turns the parameter on
  exactly when v lies between its MIDI CC on/off thresholds Min and Max,
  inclusive, and the result is inverted when Min > Max. A relative message turns
  it on when d > 0 and off otherwise (E13). Open: PRB-N7-04.
- **S-cond. Takeover.** Takeover applies only to Absolute and Absolute14Bit
  mappings of continuous float parameters with takeover enabled. Let p be the
  value that the previous CC value of the same controller number, on the same
  input and channel, would have produced; any earlier message counts.
  - Takeover None: the new value applies.
  - Otherwise, with no previous value since the input opened, the value is
    unchanged. When p is within (max − min)/256 of the current value c, the new
    value applies.
  - Pick-Up applies the new value only when c lies within (max − min)/64 of the
    span between p and the new value.
  - Value Scaling applies the new value when it is within (max − min)/64 of c,
    and leaves c unchanged when p equals the new value. Otherwise it moves c by
    the travelled fraction of the remaining distance toward max or min.
  - The result is clamped (E14). Open: PRB-N7-03.
- **Unknown.** The takeover preference default, delivery ordering, coalescing
  and deferred application (PRB-N7-05), displayed values, and parameters of
  neither class. Also unknown: duplicate addresses (every mapping on an address
  is called, Inferred), the first 14-bit pair after the input opens, and when the
  prior table is reset.

REQ-MIDI-USER-010 "Scaling, clipping, smoothing" becomes the clauses above. No
smoothing occurs before the parameter setter: the value is applied once per
message (Observed). The setter itself was not traced. PRB-S4-05 is refined by
PRB-N7-01.

## Acceptance cases (static derivations, unexecuted)

[acceptance-cases.json](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/out/acceptance-cases.json)
holds 23 cases from
[derive_cases.py](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/scripts/derive_cases.py),
a float32 model with a self-check. It is not an oracle.

Unless a case says otherwise: input is CC 20 (`B0 14 vv`), with LSB CC 52
(`B0 34 vv`, written L:vv). The parameter is continuous, min 0, max 1, starting
at 0.5. Nothing has been received on the controller since the input opened.
Values are listed after each message, tolerance 1e-6.

| Case | Mode, condition | Data bytes | Expected values |
| --- | --- | --- | --- |
| MT-01 | Absolute, None | 00 40 7F | 0, 0.503937, 1 |
| MT-02 | Absolute14Bit, None | 64 L:32 | 0.5, 0.78435 |
| MT-03 | Absolute14Bit, None | L:32 64 | 0.5, 0.78435 |
| MT-04 | Absolute14Bit, None | 10 64 L:32 L:00 | 0.5, 0.5, 0.78435, 0.78435 |
| MT-05 | Absolute14Bit, None | 7F L:7F 00 L:00 | 0.5, 1, 1, 0 |
| MT-06 | LinearSignedBit | 01 41 40 7F | 0.503906, 0.5, 0.75, 0.503906 |
| MT-07 | LinearSignedBit2 | 01 41 40 | 0.496094, 0.5, 0.25 |
| MT-08 | LinearTwoCompliment | 01 7F 41 40 | 0.503906, 0.5, 0.253906, 0.503906 |
| MT-09 | LinearBinaryOffset | 41 3F 40 00 | 0.503906, 0.5, 0.5, 0.25 |
| MT-10 | AccelSignedBit | 01 07 09 0A 41 49 00 | 0.503906, 0.542969, 0.738281, 0.816406, 0.8125, 0.617188, 0.695312 |
| MT-11 | AccelSignedBit2 | 01 41 07 47 00 | 0.496094, 0.5, 0.421875, 0.5, 0.304688 |
| MT-12 | AccelTwoCompliment | 01 7F 08 41 42 00 | 0.503906, 0.5, 0.695312, 0.890625, 0.695312, 0.890625 |
| MT-13 | AccelBinaryOffset | 41 3F 46 39 40 | 0.503906, 0.5, 0.53125, 0.453125, 0.648438 |
| MT-14 | LinearBinaryOffset, clamp | 7F 7F 7F 00 00 00 00 00 | 0.746094, 0.992188, 1, 0.75, 0.5, 0.25, 0, 0 |
| MT-15 | Absolute; quantized 0–3 from 1 | 15 16 3F 40 7F | 0, 1, 1, 2, 3 |
| MT-16 | LinearSignedBit; quantized 0–3 from 1 | 05 01 41 46 46 46 | 2, 3, 2, 1, 0, 0 |
| MT-17 | Absolute; on/off, thresholds 64/127, off | 3F 40 7F 00 | 0, 1, 1, 0 |
| MT-18 | LinearSignedBit; same on/off | 01 41 03 | 1, 0, 1 |
| MT-19 | Absolute, Pick-Up | 0A 0B 0C 3F 46 | 0.5, 0.5, 0.5, 0.496063, 0.551181 |
| MT-20 | Absolute, Value Scaling | 0A 14 1E | 0.5, 0.542735, 0.58547 |
| MT-21 | Absolute, Pick-Up | 64 | 0.5 |
| MT-22 | Absolute, Pick-Up, crossfader opt-out | 0A 64 | 0.07874, 0.787402 |
| MT-23 | LinearSignedBit, Pick-Up | 01 | 0.503906 |

Relative cases MT-06 to MT-14 hold for any takeover setting. MT-15 to MT-21 carry
the S-cond and Inferred dependencies named above.

## Probe records

[probe-records.json](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/probe-records.json):
PRB-N7-01 (absolute and 14-bit, MT-01 to MT-05), PRB-N7-02 (relative tables),
PRB-N7-03 (takeover, prior table and preference default), PRB-N7-04 (quantized
and on/off classes, threshold gate) and PRB-N7-05 (timing: ordering, coalescing
and deferred application of back-to-back messages). All need the macOS host and
a verified virtual MIDI port, as for the [S4 batch](midi-closure-r2.md#phase-4-probe-batch).

## Limitations

- Static call and data edges do not establish runtime execution.
- The handler-registry link to the MidiMap vtable and the mode stored per
  dispatch entry are Inferred.
- The value setter (0x101b0d328) and any parameter-side post-processing were not
  traced.
- Which Live parameters are `ATimeableFloat`, `ATimeableEnum` or another class is
  not listed.
- The install refusals (0x1026f9488 and the MidiMap +0x30 check) are
  uninterpreted. They may decide competing-mapping priority.
- Feedback bytes (PRB-S4-13), pitch-bend and note mappings, and the Zoom > 1
  centered-pickup branch are outside this question; script mappings always use
  Zoom 1.0.
