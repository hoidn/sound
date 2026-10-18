# N7 notes: native MIDI map-mode transforms (Q-009)

Target: `Live.arm64` SHA-256 `3a99ceea…383cfad` (Ableton Live 12 Suite 12.4.3,
arm64 slice). Static analysis only; Live was not run and nothing from the bundle
was imported or executed. Python listings are the S4 `dis` listings
(`../s4-midi-v1/listings/`). Native evidence is the C1/C2 corpus and indexes plus
four dossier rounds on query server 1, kept under `results/`.

Labels: **Observed** = present in a kept disassembly listing, decompiler text, the
binary's bytes or a shipped file; **Inferred** = interpretation; **Unknown**.
Every native claim below was checked against disassembly unless it says
"decompiler only".

## Rounds

| Round | Result id | Functions (dossiers) |
| --- | --- | --- |
| 1 | n7-0001 | 0x101b7b96c decoder, 0x101b7bd1c zoom delta, 0x101b7fde4 apply, 0x101b7c508 takeover, 0x101b7c344 pick-up, 0x101b7f354 CC receiver (variant), 0x101b7fc90 14-bit MSB store (variant), 0x102593258 map_midi_cc implementation |
| 2 | n7-0002 | 0x101b76bf0 value function, 0x101b7f894 CC receiver (registered), 0x1026094e0 14-bit install, 0x101b7fcc0 14-bit combine, 0x101b8028c MSB store, 0x101b802bc LSB store, 0x101b65b68 prior table, 0x101b84798 handler registration |
| 3 | n7-0003 | 0x1026fa684 kind/range, 0x1026fa5c8 details builder, 0x101b83750 takeover preference setter, 0x101b7f32c receiver init, 0x10260535c handler lookup, 0x101b842cc table init, 0x1025931ac argument validation, 0x1024dd61c |
| 4 | n7-0004 | 0x103b4d744 Python wrapper, 0x101b7842c CC dispatch, 0x101b69248 input dispatch |

27 dossiers in four rounds. `out/corpus-excerpts.jsonl` holds decompiler text
for 26 further cited functions (`scripts/extract.py`). No `str:` query was used.

## Python side (bytecode, Observed)

- `_Framework/ControlSurface._install_mapping` L735–743 (offsets 814–1044) calls
  `Live.MidiMap.map_midi_cc_with_feedback_map(handle, parameter, channel,
  identifier, control.message_map_mode(), feedback_rule, not
  control.needs_takeover(), control.mapping_sensitivity)`.
- `_Framework/InputControlElement.__init__` L191 `_needs_takeover = True`, L197
  `_mapping_sensitivity = 1.0`; `install_connections` L332–337 installs the
  mapping when a parameter is connected.
- `_Generic/GenericScript` L216: crossfader `set_needs_takeover(False)`. No
  user-script module sets `mapping_sensitivity` (grep of the listings).
- `ableton/v3/control_surface/elements_base` `MapMode` L27–47: `Absolute` →
  `absolute`, `Absolute14Bit` → `absolute_14_bit`, `AccelSignedBit` →
  `relative_signed_bit`, `AccelSignedBit2` → `relative_signed_bit2`,
  `AccelBinaryOffset` → `relative_binary_offset`, `AccelTwoCompliment` →
  `relative_two_compliment`, `LinearSignedBit` → `relative_smooth_signed_bit`,
  `LinearSignedBit2` → `relative_smooth_signed_bit2`, `LinearBinaryOffset` →
  `relative_smooth_binary_offset`, `LinearTwoCompliment` →
  `relative_smooth_two_compliment`.

## Native chain (Observed unless marked)

1. **Enum** (`0x103b4ca90`, decompiler + strings index): Boost.Python enum
   `NRemoteMapperTypes::TControllerMapMode`: absolute 0, relative_signed_bit 1,
   relative_binary_offset 2, relative_two_compliment 3, relative_signed_bit2 4,
   absolute_14_bit 5, relative_smooth_signed_bit 6, relative_smooth_binary_offset 7,
   relative_smooth_two_compliment 8, relative_smooth_signed_bit2 9. Caller type
   string at 0x10597ee86: `bool(unsigned, TPyHandle<ATimeableValue> const&, int,
   int, TControllerMapMode, NPythonMidiMap::TCCFeedbackRule const&, bool, float)`;
   keyword names `avoid_takeover`, `sensitivity` (default 1.0).
2. **Wrapper** `0x103b4d744` (n7-0004): resolves the handle (0x1026048f0),
   converts the feedback rule, forwards channel w2, CC w3, mode w4, avoid w6 and
   sensitivity s0 unchanged to `0x102593258`.
3. **Install** `0x102593258` (n7-0001): validates via `0x1025931ac` (channel ≥ 16
   → "Invalid channel parameter."; CC > 127, or CC ≥ 96 with mode 5 → "Invalid
   cc_no parameter."). Returns false without installing when `0x1026f9488`
   (param+0x1c0 ≥ 0) holds, or when MidiMap vtable +0x38 is nonzero and +0x30
   (channel, CC) reports true (meaning Unknown). Builds `TTimeableDetails` through
   the parameter's vtable +0x350 with s0 = 1.0 and flag = "parameter is an
   ATimeableBool" unless registry lookup `0x1011aeb80` hits (then 0). Mode 5 →
   `0x1026094e0`; otherwise a 0x50-byte CC receiver initialised by `0x101b7f32c`
   (avoid → +0x44, sensitivity → +0x48), handler type 3, key (channel, CC, mode).
4. **Details** `0x1026fa5c8` → `0x1026fa684` (n7-0003): Type 1 if the
   parameter class is `ATimeableFloat`, 2 if `ATimeableBool`, 3 if
   `ATimeableEnum`, else 0 (class names from registration `0x1026f3290`). Min/Max
   = vtable +0x2f0/+0x2f8; with the flag set and vtable +0x388 non-null, Min/Max
   come from that range object instead. Quantized = vtable +0x2e0, or (when false)
   an internal byte (+0x8c of a sub-object, 0x1024dd61c) equal to 2. Zoom
   (+0x1c) = the float argument (1.0 here). Field names are Observed in the
   `OChangeControllerDataCommand` registration (0x101b7c70c): TrackIndex,
   TimeableIndex, UniqueAObjectId, Min, Max, Zoom, Quantized, InterpretReverse,
   Type, HasBeenPickeUp, CValue, PriorCValue, MapMode, Sensitivity.
   The Python `DeviceParameter` getters `is_quantized`, `min`, `max`
   (0x103afe2cc/3c0/3d0, decompiler) call the same vtable slots +0x2e0/+0x2f0/+0x2f8.
   `ATimeableBool` registers member `mpMidiCCOnOffThresholds` (0x1026eb938).
5. **Handler registry** `0x101b84798` (n7-0002): type 3 → `0x101b7f894`, type 5
   → `0x101b8028c`, type 6 → `0x101b802bc` (also 1 → 0x101b7f75c, 2 → 0x101b7f7f8,
   4 → 0x101b7fad4). Lookup `0x10260535c` (n7-0003) returns the same registry slot
   (0x101ab9f5c). *Inferred*: it is the MidiMap vtable +0x60 used by the install
   functions (it has DATA refs from a vtable; the exact class is not named).
6. **Dispatch** `0x101b69248` → `0x101b65b68` → `0x101b7842c` (n7-0002/0004):
   for a CC message the per-input table entry (channel × 131 floats, index CC+2)
   is read as PriorCValue and overwritten with the new value; then every handler
   in the (channel, CC) list is called with (value, prior, receiver, entry+0x30).
   *Inferred*: entry+0x30 holds the key's map mode. Table fill = -129.0
   (0x105849f70) at construction (0x101b6569c) and on reset (0x101b65c1c, caller
   0x101b68f98; trigger Unknown).
7. **CC receiver** `0x101b7f894`: if avoid and Zoom == 1.0, PriorCValue := FLT_MAX.
   For relative modes on a quantized parameter: acc += (decode > 0 ? +s : −s);
   fire only when |acc| ≥ 1, then acc −= sign. Calls the apply callback
   (`0x101b83974` → `0x101b7fde4`) with {CValue, PriorCValue, MapMode, Sensitivity}.
8. **14-bit** `0x1026094e0`: receiver avoid flag hard-coded 0 (`mov w3,#0x0`
   at 0x102609548); key (ch, n, 5) → type 5, key (ch, n+32, 5) → type 6.
   `0x101b8028c` stores MSB/prior at +0x34/+0x3c, `0x101b802bc` LSB/prior at
   +0x38/+0x40; either calls `0x101b7fcc0` once both value slots ≠ FLT_MAX.
   `0x101b7fcc0`: value = (MSB<<7 | LSB)/129.0 (constant 0x10584a8b4), prior
   likewise when both priors are present; MapMode 0, Sensitivity 1.0; afterwards
   all four slots := FLT_MAX.
9. **Apply** `0x101b7fde4` (Zoom ≤ 1 branch): Type 2: absolute → on iff
   lower ≤ v ≤ upper XOR (Min > Max); relative → on iff decode(v)·s > 0.
   Otherwise `0x101b76bf0`, then for MapMode 0/5, Type 1 and PriorCValue ≠ FLT_MAX
   → `0x101b7c508`. Result goes to setter 0x101b0d328. When `0x1011c0ee8(0x100500)`
   is nonzero the same fields are serialized as `OChangeControllerDataCommand`
   and re-applied by `0x101b8363c` (timing Unknown).
10. **Value function** `0x101b76bf0`: absolute: t = (inverted ? 127−v : v)/127;
    r = lo·(1−t) + hi·t (fmadd). Relative: step = quantized ? (decode·s > 0 ? +1 :
    −1) : (hi−lo)·(1/256)·decode·s; r = clamp(cur ± step, lo, hi). Quantized →
    `frinta` (nearest, ties away from zero). The decompiler showed an int cast; the
    disassembly shows `frinta` at 0x101b76cd4.
11. **Decoder** `0x101b7b96c` (value truncated with fcvtzs for comparisons):
    see the research page table. Tables: mode 1 uses A = [1,2,3,4,5,8,10,20,50]
    (fallback 20.0), modes 2–4 use B = [1,2,3,4,5,8,20,50] (fallback 50.0)
    (`out/native-constants.json`; init 0x101b842cc stores A[8] = 50.0 at +0x20).
12. **Takeover** `0x101b7c508`/`0x101b7c344`: global mode DAT 0x106fb2110 set by
    `OSetMidiTakeOverMode` (0x101b83750). Index 1 posts
    `RemoteMapper.PickUpNotification`; index 2 performs proportional scaling;
    index 0 passes through. UI entries are declared in the order
    sControlNoTakeOverEntry, sControlPickUpTakeOverEntry,
    sControlValueScalingTakeOverEntry (0x1022df424). *Inferred* index→label map:
    0 None, 1 Pick-Up, 2 Value Scaling.

## Shipped-set observation

`out/onoff-thresholds.json`: 26 parsed `.als` sets carry 22,303
`MidiCCOnOffThresholds` pairs; Min 64 / Max 127 in 22,059. Other pairs: 1/127
(175), 1/0 (34), 0/126 (12), 65/63 (10), 127/126 (5), 20/127 (4), 2/127 (3),
64/0 (1).

## Inconclusive or failed steps

- `vtables.jsonl` has only 80 named vtables; no `ATimeableValue` family, so the
  +0x350 implementation was found through its callee `0x101b7c214` instead.
- Scans for a details writer by field offsets returned unrelated filters
  (0x101c3f994, 0x102955ef0).
- The registry behind `0x1011aeb80` (32-byte key at 0x1058838e4) is unexplained.
- Takeover preference default: not found.

## Derived cases

`scripts/derive_cases.py` models items 6–12 in float32 and writes
`out/acceptance-cases.json` (MT-01 to MT-23, with a self-check). Outputs are
static derivations, not observed runs.
