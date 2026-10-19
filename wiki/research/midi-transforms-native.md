---
id: RESEARCH-MIDI-TRANSFORMS-NATIVE
type: research
status: draft
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64 (Live.arm64 SHA-256 3a99ceea…383cfad); X2 runs on the x86_64 slice (1bae9a97…be999b0)
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

Update 2026-10-18 (X2): the original x86_64 receivers, Apply, value function and
takeover have now run on these cases and on 40 more. They agree with every case
below, and they settle takeover with a reversed range, the first 14-bit pair and
the value tolerance. A static trace settles the takeover labels and the reset of
the previous-value table. See [extracted execution results](#extracted-execution-results-x2-2026-10-18).

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
X2 confirms this: the takeover receives mode 0 for every pair.

Labels: the arithmetic is Observed. The index-to-preference-label mapping is
**Inferred**: index 1 posts the pick-up notification, and the UI entries are
declared in the order None, Pick-Up, Value Scaling. The preference default, the
trigger that resets the prior table, and the first 14-bit pair are **Unknown**.
For that first pair the −129 priors combine to −1/129, which a static reading
treats as a prior near min; this is not proposed as a clause.

Correction 2026-10-18 (X2): the label mapping is now a static result, not an
inference. The preference chooser's entries are, in order, the keys for None,
Pick-Up and Value Scaling, and its change handler sends the chosen position.
The reset trigger is the control-surface call `reset_input_history`, which no
user-mapping module makes. The first pair and a pair with one missing previous
value are settled by X. Here min and max mean the sorted bounds lo and hi: Apply
passes the takeover min(Min, Max) and max(Min, Max). See
[extracted execution results](#extracted-execution-results-x2-2026-10-18).

Correction 2026-10-18 (midi-config-v3 review, F1/RV3-02): the answer above and
the proposed S clause below say that the crossfader opts out of takeover. That
holds only for its non-14-bit mappings. Install 0x102593258 passes the opt-out
only to the CC receiver; its 14-bit call (0x10259338c) passes no opt-out, and the
pair receiver's flag is fixed at false, as stated above. A crossfader
`Absolute14Bit` pair therefore reaches takeover like any other control's pair.
[Spec revision 4](../specs/midi-user-mapping.md) narrows the exemption to
`Absolute` values.

## Extracted execution results (X2, 2026-10-18)

**Question.** What does the original code compute for takeover (PRB-N7-03),
including a reversed range and 14-bit pairs, and what value tolerance holds on
both slices? Does a self-contained function decide the master-volume display
(PRB-S4-05)? Which other PRB-N7-01 to 05 or PRB-S4 questions does such a
function decide?

**Answer (X, draft).** The x86_64 mapping chain ran as one unit: receiver,
Apply, value function and takeover. It agrees with all 23 cases MT-01 to MT-23.
The takeover arithmetic above holds, with five additions:

1. The bounds are sorted. For a reversed range, n and p are the ordinary
   targets, while w, the sync tolerance and the scaling use lo = min(Min, Max)
   and hi = max(Min, Max).
2. A 14-bit pair always has a previous value. When a half lacks one, the
   combiner's formula below gives a value at or below min, so the first pair
   after the input opens is judged against it instead of being kept.
3. For a stepped parameter, p is rounded like n.
4. A p of exactly −129 counts as no previous value.
5. The Value Scaling result is not rounded.

Every bound is inclusive. The slices differ only by the arm64 fused
multiply-add in the absolute target, by at most one binary32 unit of
max(|min|, |max|); Value Scaling can magnify that difference. The
master-volume display stays unknown.

Evidence: [x2-midi-v1](../../analysis/ableton-live-12.4.3/r2/x2-midi-v1/manifest.json),
regenerated by `sh run.sh` (about 50 s, 131 runs). It holds:

- `run_x2.py`, the harness and case definitions;
- `results/mt.json`, `results/takeover.json` (the TK and TB runs),
  `results/tolerance.json` and `results/value_scaling_model.json`;
- `acceptance-cases-x2.json`, the new cases MT-24 to MT-56;
- `raw/runs.jsonl`, with the argv, gdb script, stdout and stderr of every run;
- `addresses.json`, `x86-disasm.txt` and `imports.txt`;
- `static-e15.txt`, the static excerpts behind the label and reset findings.

Heap addresses in `raw/runs.jsonl` change between runs, so that file is not
byte-stable; the results files are.

Correction 2026-10-18 (harness defect): the first X2 run put 402 calls in each
of the ten 14-bit tolerance processes. `xexec` then stored call results past
its 256-entry table without a check, which could corrupt memory. The loader now
stops at 256 calls. Those batches were re-run with at most 201 calls per
process. Every value in the results and in MT-01 to MT-56 is unchanged; only the
run count (111 to 131) and the import call counts changed. No other process
exceeded 256 calls.

The harness is the unchanged [tools/xexec](../../tools/xexec/xexec.py) under
gdb, as in [X1](extracted-execution.md).

### Method

**Functions.** The x86_64 slice is `Live_x86_64.x86_64`, SHA-256 `1bae9a97…be999b0`.

| Role | x86_64 | arm64 | How matched |
| --- | --- | --- | --- |
| CC receiver (registry type 3) | `0x101bbc3b0` | `0x101b7f894` | Registry `0x101bc1950` registers it for type 3, as arm64 `0x101b84798` does; avoid flag +0x44, Zoom +0x3c, sensitivity +0x48, accumulator +0x4c |
| 14-bit MSB / LSB setter (types 5, 6) | `0x101bbced0` / `0x101bbcf10` | `0x101b8028c` / `0x101b802bc` | Same registry; same bodies as X1's `0x101bbc830` / `0x101bbc980` |
| 14-bit combiner | `0x101bbc870` | `0x101b7fcc0` | X1 |
| Apply callback | `0x101bc09b0` | `0x101b83974` | Installed by the CC receiver; shifts the arguments and jumps to Apply |
| Apply | `0x101bbc9c0` | `0x101b7fde4` | X1; same branch structure, read in both disassemblies |
| Takeover | `0x101bb8b70` | `0x101b7c508` | Called by Apply right after the value function in both; reads the mode global; constants −129, 0.5, {128, 16384}, ±1 |
| Pick-Up | `0x101bb8990` | `0x101b7c344` | The takeover's only other callee; window 2(hi − lo)/{128, 16384}; posts the notification |
| `OSetMidiTakeOverMode` handler | `0x101bc0770` | `0x101b83750` | Registered with that name and the field `TakeOverModeIndex` (`0x101bb8da0`); only writer of the mode global `0x107443e78` (arm64 `0x106fb2110`) |

**Harness.** Each message sequence runs in one gdb process:

- The process calls the unit initializer `0x101bc1360`, then the
  `OSetMidiTakeOverMode` handler with a message buffer holding the index.
- It then calls the original receiver once per message. For CC 20 that is the
  CC receiver, or the MSB setter in 14-bit mode; for CC 52 it is the LSB setter.
- The receiver object is a buffer laid out as the static reading of the receiver
  constructors gives it (E10, E11 of the spec). It holds the details record (Type, Min, Max, Quantized, Zoom 1.0 and so on;
  field names from the `OChangeControllerDataCommand` registration), the avoid
  flag, sensitivity 1 and the held halves.
- Stubbed under gdb: Apply's owner and parameter accessors (`0x101abb210`,
  `0x101b3d680`), the current-value read `0x101b6f830` and the setter
  `0x101b3d360`. Together they simulate the parameter: a read returns the last
  value set, which starts as the case's value.
- The pick-up notification post (`0x101bb8a0d`–`0x101bb8a7f`) is jumped over.
  The Pick-Up result is stored before it and reloaded by the original epilogue.
  Without the jump, the post faults in the message system.
- Apply's thread check `0x10119c480` ran natively and chose the direct path at
  all 312 of its calls, so the deferred `OChangeControllerDataCommand` path never
  ran.
- Not run: the dispatcher and per-input table (arm64 `0x101b65b68`,
  `0x101b7842c`), the details builder and the real setter. The harness supplies
  the previous value as the static reading says: the last data value on the
  same controller, or −129.
- Imports called: `operator new`, the C++ guards, `__cxa_atexit`,
  `pthread_key_create` and `pthread_getspecific`. No libm function is used.

**Static slice comparison.** Read in the kept arm64 dossiers (n7-0001, n7-0002) and
`x86-disasm.txt`:

- The takeover, Pick-Up, Apply, both receivers and the combiner use the same
  operations, comparisons and constants in both slices.
- The combiner truncates both halves to integers, ORs MSB<<7 with LSB and
  divides by 129, in both slices.
- Fused instructions: besides the known `fmadd` in the value function
  (`0x101b76c60`), there is only `fmadd s10,s0,s1,s10` in the takeover. Its s1 is
  ±1, an exact product, so it equals the x86 add.
- The relative branch of the value function, the decoder, Apply, the receivers
  and the combiner contain no fused instruction.

### Results

**MT-01 to MT-23 (X).** All 23 cases agree within 1e-6 (`results/mt.json`):

- MT-17 and MT-18 use Type 2 with thresholds 64 and 127.
- MT-19 to MT-21 use takeover index 1 or 2.
- MT-22 sets the avoid flag; the CC receiver then passes a `FLT_MAX` prior, and
  Apply skips the takeover.
- MT-06 to MT-14, MT-16 to MT-18, MT-22 and MT-23 give the same values under
  all three indexes.
- MT-16's stepped relative steps now run through the receiver's accumulator.
  X1 assumed that step.

**Takeover runs** (`results/takeover.json`, TK-01 to TK-30 and TB-01 to TB-10).
Each starts from an input just opened. A model of the spec revision 5 text,
in exact arithmetic, agrees with every run within the tolerance below.

| Finding | Runs | Detail |
| --- | --- | --- |
| Sorted bounds for a reversed range | TK-08 to TK-12 | Apply passes lo, hi and the reversed flag. The flag only changes how n and p are formed. Revision 4 read with the reported min and max gives other values: TK-09 (min 1, max 0) gives 0.457265, 0.414530 by X against 0, 0 by that reading |
| 14-bit previous value | TK-13 to TK-20 | The combiner forms ((m<<7) \| l)/129 with a missing value −129: −1/129 for none, −1 for an even m alone (TK-17), −128 + l/129 for l alone (TK-18, −127.75194). Pick-Up then applies a first pair whose target is at or above c − w (TK-13) and keeps c otherwise (TK-14). Value Scaling moves c even when the target is below it (TK-15: 0.5 to 0.5625305) |
| Stepped parameter | TK-21, TK-22 | p is rounded like n (TK-22: p = 1 is in sync, so 3 applies). The Value Scaling result is passed unrounded: TK-21 sets 2.3333335 on a range 0–3 parameter. The setter's handling is unknown |
| Enumerated and other kinds | TK-23, TK-24 | No takeover, whatever the index |
| p exactly −129 | TK-25 | Range −129 to 0, previous data value 0: the value stays at −10 |
| Avoid flag on a pair receiver | TK-26 | The combiner passes a `FLT_MAX` prior and the takeover is skipped. This is a harness-only check; install passes the flag 0 for pairs (E11) |
| 14-bit on/off, reversed thresholds | TK-27, TK-28 | 0x40/0x00 gives 63.5, so off; 0x40/0x7F gives 64.49, so on. With Min 127 and Max 64 the result is inverted |
| Inclusive bounds | TB-01 to TB-10 | Range 0–127, so every target is an exact integer. A value exactly on the sync, window or near-target bound applies n; one binary32 step outside it does not |

**Takeover labels and reset (S, both slices; `static-e15.txt`).** Neither is X.

- Labels. The `LMidiPreferences` constructor (x86 `0x1023e0050`, arm64
  `0x1022cc18c`) builds the chooser's entry list from `sControlNoTakeOverEntry`,
  `sControlPickUpTakeOverEntry` and `sControlValueScalingTakeOverEntry`, in that
  order. It binds `OnTakeOverModeChanged` to the chooser.
- The change handler (x86 `0x1023e2a60`, arm64 `0x1022cec38`) is the only code
  that posts `OSetMidiTakeOverMode`. It sends the chooser index at +0xd8; −99,
  unset, sends 0. The engine stores that index for the takeover. The entry text
  shown is entries[index] (x86 `0x1015566d0`).
- The localized words were not read, because `Languages.alp` is packed. The
  preference default was not found.
- Reset. The table is refilled only by the `MidiInputRouter.ResetInputHistory`
  command (arm64 `0x101b68f98`, refill `0x101b65c1c`). Its only poster,
  `0x10259b710`, is the Python method `reset_input_history` of the control
  surface's host object (registration `0x1039fa2a4`).
- Among all shipped MIDI Remote Scripts, only
  `Launch_Control_XL/LaunchControlXL.pyc` contains that name.

**Value tolerance** (`results/tolerance.json`). X ran the value function on all
128 data values and on 401 of the 16,384 14-bit pairs in ten ranges. A binary32
model of the x86 sequence, with two roundings, equals X for every value run. A
model of the arm64 `fmadd`, using glibc `fmaf`, was compared with X on the 128
data values and with the x86 model on all 16,384 pairs:

| Range (min, max) | Values where arm64 differs (7-bit; 14-bit) | Largest difference |
| --- | --- | --- |
| (0, 1), (−1, 1), (1, 0), (−100, −1), (0.001, 2) | 0; 0 | 0 |
| (20, 999), (999, 20) | 35; 3,949 and 35; 4,138 | 6.1e-5, one ulp of 999 |
| (−999, 999) | 52; 6,528 | 6.1e-5 |
| (−70, 6) | 8; 1,292 | 7.6e-6, one ulp of 70 |
| (0.25, 0.75) | 63; 6,989 | 6.0e-8, one ulp of 0.75 |

The difference is never more than one binary32 ulp of R = max(|min|, |max|).
In general it is at most 1.5 ulp(R): the x86 rounding of hi·t moves the sum by
at most half an ulp of R, and each final rounding by at most another half. That
is below 2⁻²² × R. The
spec therefore uses τ = max(1e-6, 2⁻²² × R). The 1e-6 floor covers six-digit
decimal expected values. When lo = 0, lo·(1 − t) is 0 and the slices are
identical.

**Value Scaling magnifies the slice difference** (model, not X;
`results/value_scaling_model.json`). Feeding the binary32 Value Scaling sequence
with each slice's targets, for every previous and new data value and 33
current values, gives these largest differences:

| Range | Largest difference | In units of 2⁻²² × R |
| --- | --- | --- |
| (0, 1) | 0 | 0 |
| (20, 999) | 2.9e-3 | 12.3 |
| (−999, 999) | 4.3e-3 | 17.9 |
| (−70, 6) | 1.1e-5 | 0.69 |
| (0.25, 0.75) | 8.3e-7 | 4.7 |

A decision within about one ulp(R) of its bound can also differ. The new
Value Scaling and boundary cases therefore use lo = 0.

**Master-volume display (PRB-S4-05): unknown.** No self-contained function
decides it:

- Min, Max and Quantized come from the parameter's own virtual methods (E13).
- The set path ends in the untraced setter `0x101b0d328`.
- The parameter's class and its methods were not traced.
- The later steps, the fader curve and the gain text, are pure. The curve is
  covered by [mixer values](mixer-values.md#stored-value--position--gain-the-fader-curves),
  where the fader position as the MIDI domain is inferred. The gain text ran
  in [X1](extracted-execution.md#mixer-value-text).

**Other open items.** These are not settleable this way:

- PRB-S4-04 (unknown token): the conversion happens in the Python binding.
- PRB-N7-04 (parameter classes and the threshold-range check `0x1011aeb80`)
  needs a parameter object.
- PRB-N7-05 (ordering and deferral) is a timing question.
- The takeover preference default needs the preferences loader.

### Limits

- **What X shows.** X shows what these x86_64 functions compute for the given
  details record, current value and previous value. It does not show that Live
  builds that record for a given parameter, which values the dispatcher passes,
  or what the setter or the display does.
- **Assumptions.** The previous value follows the static dispatcher reading.
  The 14-bit receiver's avoid flag is 0, as the static install shows. Sensitivity
  is 1 and Zoom is 1.0, as the script path passes them.
- **Slice.** Equivalence with arm64 is inferred from the static comparison. The
  one numeric difference is bounded above.
- **Notification.** Skipping the pick-up notification hides any UI effect of it,
  such as status text. The value it returns is unaffected.

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
