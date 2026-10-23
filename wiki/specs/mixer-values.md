---
id: SPEC-MIXER-VALUES
type: spec
status: draft
updated: 2026-10-21
access: analysis
revision: 7
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Track mixer values: storage, display text and gain

## Scope

Feature FEAT-AUDIO, with FEAT-PERSISTENCE, in the [feature map](feature-map.md).
User task: open a Live Set whose tracks carry mixer settings (volume, pan, pan mode,
split-stereo pans, sends, speaker, crossfade assign), see those settings as text,
save them back, and hear the volume, pan and crossfade settings applied. This draft
specifies:

- where each track type stores its mixer values, their domains and initial values;
- the volume and send fader curves (position ↔ gain);
- the dB and pan value text;
- the crossfade-assign values and the set's crossfader and crossfade-curve fields;
- the number text written on save;
- the gain, silence floor, pan law and crossfade effect on audio, as **static
  derivations only**. No reference measurement is available
  ([ADR 0003](../decisions/adr-0003-no-reference-execution.md)), so they support no audio
  compatibility claim.

Every requirement is a **proposed contract** supported by shipped bytes, by a static
derivation from the 12.4.3 program, or explicitly unknown. Nothing was run against
Live. [ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits a
static-first draft, and under ADR 0003 nothing will be: the Phase 4 probes named below
will not run. Target: 12.4.3, documents with `MinorVersion="12.0_12402"`. The
gzip/XML envelope belongs to the draft [SPEC-ALS-CONTAINER](als-container.md); the
number text rule is [REQ-TRANSPORT-STATE-011](transport-state.md#req-transport-state-011--number-text-on-save),
and `Tempo`, `TimeSignature` in the main mixer belong to
[SPEC-TRANSPORT-STATE](transport-state.md). Document examples are fragments of the
decoded XML.

Excluded: rack chain mixers; `GlobalGrooveAmount`; automation and clip envelopes on
mixer parameters and their interpolation (SPEC-AUTOMATION-ENVELOPES candidates);
MIDI and key mapping of mixer parameters and the scaling of a controller value to a
fader (Q-009 area); routing, solo, monitoring and send pre/post (their T1 rules are in [SPEC-MIX-GRAPH](mix-graph.md)); text entry into
value fields; arrow-key and mouse edits; edits after load except the track creation
named in MV-027 and MV-028; documents older than `12.0_12402` and their migration
(for example `TrackSendHolder/Active` before `12.0_12001`); the exact text of error
messages; which UI surface (mixer strip, Info View, automation lane, controller
display) shows which text.

Revision 6 adds finite scalar-helper expectations under REQ-014; the application
audio-path scope and unknowns above remain unchanged.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema files or the 376 Live Sets and clips in the 12.4.3 bundle. These were written by Live 12.4d1 or 12.1d1, not by a 12.4.3 save |
| S | Static derivation from the 12.4.3 executable or shipped bytes; not an observed run |
| X | Extracted execution: the original x86_64 function was run in a harness on the recorded inputs ([ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code), packets [x2-mixer-v1](../../analysis/ableton-live-12.4.3/r2/x2-mixer-v1/manifest.json), [reviewed mix boundary batch](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-mix-leaves-v1/manifest.json), and the x1 pilot for text). X shows what the code computes for those inputs with glibc substitutes; it does not show that Live reaches the code, nor what the user hears. The release target is arm64; equivalence is checked by comparing the two slices (noted per clause) |
| S/Q-019 | Static derivation that rests on the Q-019 result of [SPEC-MIX-GRAPH](mix-graph.md) r1: the logic layer sends fader positions and the engine applies the curve and the floor. Revision 4: settled statically under that spec's conditions A3 to A5 (envelope owner, send conversion node, wiring branch), which a static trace could settle ([Q-019](../questions.md#q-019-mixer-volume-and-send-values-sent-to-the-engine)) |
| U | Unknown; no expected result, or only a static reading that must not be graded. A PRB ID names the Phase 4 probe that would have settled it. No reference observation is available (ADR 0003), so the clause stays unknown unless the static route or an extracted-execution run named with it settles it |

Only D, S and X clauses may enter a release. An S/Q-019 clause may enter one only together
with the conditions it names. Revision 4 applies the T1.4 static trace
([mix graph](../research/mix-graph.md#q-019-values-on-the-volume-and-send-ports)):

- The logic layer puts the fader position on the engine's volume and send ports.
- The engine applies the curve of REQ-005, the crossfade factor and the floor.
- The round trip of REQ-005 is exact only for the seven tested curve points (X);
  revision 5 withdraws the general identity claim.

Every clause about *audio
output* (REQ-011, 013, 014) rests on a computed gain, X where the gain function was run and
static otherwise; no original-versus-candidate rendered-audio measurement is available
(ADR 0003), so these clauses support no audio compatibility claim. U clauses block the
behavior they name.

Terms. *Gain* is a linear amplitude factor (1 = 0 dB). *Position* is a fader
position in [0, 1]. *float32* is IEEE-754 single precision. "Track A", "return R",
"main M" and "cue C" are the mixers of fixture B0 named under
[Acceptance cases](#acceptance-cases).

Reading and display assumptions (inferred, not traced to the end). A mixer number
written as plain decimal text (an optional `-`, ASCII digits, optionally `.` and
digits) is read as the nearest float32; Booleans are `true`/`false`, codes decimal
integers; a code's name is its entry in the constructor's list (the enum text routine
is not traced). The loader was not re-traced for the mixer classes. SPEC-TRANSPORT-STATE's
value-text rules were derived for the transport and `Tempo`, a `TimeableSongTempo`;
volume, pan and send are `TimeableFloat` in schema `12.0_12402`, so those rules do not
carry over by class identity. The text clauses (REQ-006, 007, 008) give the text rule
attached to each value. That some display shows these texts, computed from the value
as read, is assumed; which display shows which form is unknown (REQ-006).

## Requirements

### REQ-MIXER-VALUES-001 — mixer location and fields per track type

- **D.** Every `AudioTrack`, `MidiTrack`, `GroupTrack`, `ReturnTrack`, `MainTrack`
  and `PreHearTrack` (the cue/preview track) stores one mixer at
  `<Track>/DeviceChain/Mixer`. 1,340 of 1,340 shipped mixers follow this.
- **D.** Each mixer holds these value elements, in this relative order: `Sends`,
  `Speaker`, `SoloSink`, `PanMode`, `Pan`, `SplitStereoPanL`, `SplitStereoPanR`,
  `Volume`, `CrossFadeState`. Other mixer children (`On`, `LomId`, view state) are
  outside this spec. No shipped mixer has a `*KeyMidi` child.
- **D.** `Volume`, `Pan`, `SplitStereoPanL`, `SplitStereoPanR` and each `Send` hold
  `LomId`, `Manual` (32-bit float), `MidiControllerRange` (`Min`, `Max`),
  `AutomationTarget` and `ModulationTarget`. `CrossFadeState` holds `LomId`, `Manual`
  (integer), `AutomationTarget` and `MidiControllerRange` (`0`–`2`). `Speaker` holds
  `LomId`, `Manual` (Boolean), `AutomationTarget` and `MidiCCOnOffThresholds`.
  `SoloSink` and `PanMode` are single-`Value` elements (Boolean, integer).
- **D.** The main mixer additionally holds `Tempo`, `TimeSignature`,
  `GlobalGrooveAmount` and `CrossFade` (32-bit float, the crossfader) after the
  fields above.
- **S.** All six track types use the same value domains, defaults, curves and text
  rules (REQ-002 to REQ-009); only the send holders (REQ-003) and the main-only fields
  differ.

### REQ-MIXER-VALUES-002 — volume domain, default and range

- **S.** `Volume/Manual` is a float32 gain. The controlled range is 0.0003162277571
  (−70 dB) to 1.99526238 (+6 dB), the float32 values of these two texts. They lie
  within 0.000001 dB of −70 dB and +6 dB. The lower one is the float32 nearest to
  10^(−70/20). The upper one is one float32 step above the float32 nearest to
  10^(6/20) (1.9952622652) and equals the volume curve's top gain G[100] (REQ-005). A
  new mixer's volume is `1` (0 dB).
- **S, D.** A new mixer's volume `MidiControllerRange` is `Min` = gain at position 0
  and `Max` = gain at position 1 of the volume curve (REQ-005), written
  `0.0003162277571` and `1.99526238`. 1,318 shipped mixers store exactly this text;
  22 mixers in 5 documents store `0.00031622799`/`1.99526203` instead (REQ-015).
- **D.** Shipped volumes range from −29.0 to +6.0 dB; 1,285 of 1,340 lie on a 1 dB
  grid.
- **U.** Whether the cue track's volume is the preview level. No reference observation
  is available (ADR 0003, PRB-S9-04); a static trace from the cue volume to the preview
  player could settle it.

### REQ-MIXER-VALUES-003 — send holders and send values

- **D.** The `Sends` list of an audio, MIDI, group or return mixer holds one
  `TrackSendHolder` per `ReturnTrack` in the set (588 of 588 shipped mixers). Main and
  cue mixers hold none (`<Sends />`), also when returns exist. A return mixer holds a
  send to every return, itself included.
- **S.** `Send/Manual` is a float32 gain in [0.0003162277571, 1] (−70 to 0 dB). A new
  send is `0.0003162277571` (−70 dB, text `-inf dB`) with `MidiControllerRange`
  `0.0003162277571`–`1`.
- **S.** A new send holder's `EnabledByUser` is `true`.
- **D.** Every shipped send on a return mixer has `EnabledByUser` `false` (38 of 38);
  every other shipped send has `true` (179 of 179).
- **U.** What `EnabledByUser` changes that can be observed, including the text and
  effect of a send whose `EnabledByUser` is `false`. No case grades it. A static trace
  of the consumers of that holder member could settle it.
- **U.** Which code path sets the return-track holders to `false`, the value a new
  return gets in each mixer, the mapping of holder position to return when holder
  `Id`s have gaps (13 shipped mixers have `0 2`), and a holder count that differs from
  the return count. No reference observation is available (ADR 0003, PRB-S9-07); static
  traces of the holder creation path and of the loader's holder-list reading could
  settle them.

### REQ-MIXER-VALUES-004 — pan, split-stereo pans and pan mode

- **S.** `Pan/Manual`, `SplitStereoPanL/Manual` and `SplitStereoPanR/Manual` are
  float32 values in [−1, 1] (−1 hard left, +1 hard right). New values: pan `0`,
  left split `-1`, right split `1`. Each `MidiControllerRange` is `-1`–`1`.
- **S.** `PanMode/@Value` is `0` (Stereo, the default) or `1` (Split Stereo).
- **D.** All 1,340 shipped mixers store pan mode 0 and split pans −1/1.

### REQ-MIXER-VALUES-005 — volume and send fader curves

- **S.** Each curve is a table of 101 points D[0..100], indexed by position × 100, with
  gain G[k] = float32(10^(float32(D[k] × 0.05))). Rounded to 4 decimals:

  Volume curve, dB at position (row + column):

  | Position | +0.00 | +0.01 | +0.02 | +0.03 | +0.04 | +0.05 | +0.06 | +0.07 | +0.08 | +0.09 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | 0.0 | -70 | -66.4 | -63.3733 | -60.92 | -59.04 | -57.2 | -55.4 | -53.64 | -51.92 | -50.24 |
  | 0.1 | -48.6 | -47 | -45.44 | -43.92 | -42.44 | -41 | -39.6 | -38.24 | -36.92 | -35.64 |
  | 0.2 | -34.4 | -33.2 | -32.04 | -30.92 | -29.84 | -28.8 | -27.8 | -26.84 | -25.92 | -25.04 |
  | 0.3 | -24.2 | -23.4 | -22.64 | -21.92 | -21.24 | -20.6 | -20 | -19.44 | -18.92 | -18.44 |
  | 0.4 | -18 | -17.6 | -17.2 | -16.8 | -16.4 | -16 | -15.6 | -15.2 | -14.8 | -14.4 |
  | 0.5 | -14 | -13.6 | -13.2 | -12.8 | -12.4 | -12 | -11.6 | -11.2 | -10.8 | -10.4 |
  | 0.6 | -10 | -9.6 | -9.2 | -8.8 | -8.4 | -8 | -7.6 | -7.2 | -6.8 | -6.4 |
  | 0.7 | -6 | -5.6 | -5.2 | -4.8 | -4.4 | -4 | -3.6 | -3.2 | -2.8 | -2.4 |
  | 0.8 | -2 | -1.6 | -1.2 | -0.8 | -0.4 | 0 | 0.4 | 0.8 | 1.2 | 1.6 |
  | 0.9 | 2 | 2.4 | 2.8 | 3.2 | 3.6 | 4 | 4.4 | 4.8 | 5.2 | 5.6 |
  | 1.0 | 6 | | | | | | | | | |

  Send curve, dB at position:

  | Position | +0.00 | +0.01 | +0.02 | +0.03 | +0.04 | +0.05 | +0.06 | +0.07 | +0.08 | +0.09 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | 0.0 | -70 | -69.4 | -68.3733 | -66.92 | -65.04 | -63.2 | -61.4 | -59.64 | -57.92 | -56.24 |
  | 0.1 | -54.6 | -53 | -51.44 | -49.92 | -48.44 | -47 | -45.6 | -44.24 | -42.92 | -41.64 |
  | 0.2 | -40.4 | -39.2 | -38.04 | -36.92 | -35.84 | -34.8 | -33.8 | -32.84 | -31.92 | -31.04 |
  | 0.3 | -30.2 | -29.4 | -28.64 | -27.92 | -27.24 | -26.6 | -26 | -25.44 | -24.92 | -24.44 |
  | 0.4 | -24 | -23.6 | -23.2 | -22.8 | -22.4 | -22 | -21.6 | -21.2 | -20.8 | -20.4 |
  | 0.5 | -20 | -19.6 | -19.2 | -18.8 | -18.4 | -18 | -17.6 | -17.2 | -16.8 | -16.4 |
  | 0.6 | -16 | -15.6 | -15.2 | -14.8 | -14.4 | -14 | -13.6 | -13.2 | -12.8 | -12.4 |
  | 0.7 | -12 | -11.6 | -11.2 | -10.8 | -10.4 | -10 | -9.6 | -9.2 | -8.8 | -8.4 |
  | 0.8 | -8 | -7.6 | -7.2 | -6.8 | -6.4 | -6 | -5.6 | -5.2 | -4.8 | -4.4 |
  | 0.9 | -4 | -3.6 | -3.2 | -2.8 | -2.4 | -2 | -1.6 | -1.2 | -0.8 | -0.4 |
  | 1.0 | 0 | | | | | | | | | |

- **S.** Exact construction, in float32 arithmetic, with top T (+6 volume, 0 send)
  and bottom B = −70, indexed from the top (E[i] = D[100 − i]): E[0] = T;
  E[i] = E[i−1] − 0.4 for i = 1…60; with s = 0.4, for i = 61…96 set s = s + 0.04 and
  E[i] = E[i−1] − s; then a = s + 0.04, E[97] = E[96] − a,
  b = (3a + (B − E[97])) / 6 with the product and sum rounded once,
  E[98] = E[97] − (a − b), E[99] = E[98] + (b − (a − b)), E[100] = B. A result whose
  magnitude is below 0.0001 becomes 0 before computing the next point. The snap
  feeds forward (mixer-values-v2 review, RVM2-07).
- **X.** Position → gain: p ≤ 0 gives G[0]; p ≥ 1 gives G[100]; otherwise k = ⌊100p⌋,
  f = 100p − k (f ≤ 2⁻¹⁷ counts as 0 and f ≥ 1 − 2⁻¹⁷ as 1), gain =
  float32(f·G[k+1] + (1 − f)·G[k]), evaluated in a double intermediate. Gain → position is
  the inverse on the same table: below G[0] gives 0, at or above G[100] gives 1, otherwise
  linear between the two neighbouring points. Both conversions were run on the x86_64 slice
  (`0x101aecbd0`, `0x101aecc90`) and reproduce the derived gains (MV-023 to MV-025). Slice
  note: arm64 (`0x101ac3498`, `0x101ac353c`) fuses the interpolation with `fmadd`/`fnmsub` but
  computes in the same double intermediate, so the float32 outputs match; the x86 slice does
  not call `fma`/`fmaf` here. The three lowest table points (positions 0.01–0.03) can differ
  by one float32 ulp between slices (the dB-table landing correction is `fmadd` on arm64 and a
  separate multiply-add on x86); the table endpoints are exact in both.
- **X.** Round trip: exact only for the seven tested curve points in
  [mixer-values-v2](../../handoff/mixer-values-v2/spec.md), cases MIXER-VALUES-058 to 064,
  under that release’s exponential accuracy assumption. The
  [review](../../handoff/mixer-values-v2/REVIEW.md#scope-and-checks) found that 765 of
  1,601 sampled non-point binary32 gains did not return unchanged, by up to two
  binary32 steps; volume 0.3 returns 0.30000004. That sample maximum is not a
  general bound. Other gains have neither an exact-return guarantee nor an
  established error bound. REQ-011 must retain both conversions.
- **S.** Consequences: on the volume curve 0 dB is position 0.85 and −6 dB is 0.70;
  on the send curve 0 dB is position 1 and −6 dB is 0.85.
- **U.** That the on-screen fader and controller mappings use these positions (the curves are
  established in the gain conversion, run above, but not traced to the UI). No reference
  observation is available (ADR 0003, PRB-S9-04); a static trace from the fader and controller
  code to the curve conversions could settle it (Q-009).

### REQ-MIXER-VALUES-006 — volume and send value text

Applies to track volume and send values.

- **S.** Let dB = float32(float32(log10(g)) × 20); a gain g ≤ 0 counts as −140 dB.
- **S.** If dB ≤ −70 + 0.3 (that is, at or below −69.7 dB), the text is `-inf dB`.
- **S.** Otherwise dB is printed in fixed notation with 3 decimals; trailing zeros
  are removed down to one decimal; a value that rounds to zero at 3 decimals prints
  as `0.0` (no minus sign); then ` dB` is appended. A |dB| of 100 or more would print
  with no decimals (not reachable inside the controlled range).
- Examples: 1 → `0.0 dB`; 0.5011872053 → `-6.0 dB`; 0.5 → `-6.021 dB`;
  0.7367056608 → `-2.654 dB`; 1.99526238 → `6.0 dB`; 0.0003311311302 (−69.6 dB) →
  `-69.6 dB`; 0.0003235936455 (−69.8 dB) → `-inf dB`; 0.0003162277571 → `-inf dB`.
- **U.** Which surfaces show this text, and whether any surface shows the same digits
  without `-inf` or without the unit. No reference observation is available (ADR 0003,
  PRB-S9-04); a static trace of which views call each text form could settle it.
- **U.** Gains whose exact dB value 20·log10(g) lies within 0.00005 dB of −69.7, of
  ±0.0005, or of a number halfway between two consecutive multiples of 0.001 are not
  graded: their text depends on the platform `log10` in the last float32 ulp. The width
  is at least 2.5 times the worst-case uncertainty in range (about 2·10⁻⁵ dB near
  −70 dB, from a two-ulp `log10f` error plus the product rounding).

### REQ-MIXER-VALUES-007 — pan value text

Applies to `Pan`, `SplitStereoPanL` and `SplitStereoPanR`.

- **S.** The float32 value p, widened exactly to double, prints `C` when
  −0.01 ≤ p ≤ 0.01. Otherwise |p| × 50 (in double) is printed with no decimals,
  followed by `L` when p < 0 or `R` when p > 0.
- Examples: −1 → `50L`; −0.6 → `30L`; 0.5 → `25R`; 1 → `50R`; 0.004999999888 → `C`;
  0.01 → `C`; 0.0101 → `1R`; −0.0101 → `1L`; 0.33 → `17R` (float32 0.3300000131 × 50 =
  16.50000066, not a tie).
- **U.** Values where |p| × 50 is exactly halfway between integers (0.25 → 12.5,
  0.75 → 37.5). The static reading is the C library's round-half-to-even (`12R`,
  `38R`); not graded. No reference observation is available (ADR 0003, PRB-S9-04), and
  no static route remains in the program: the rounding is done by the platform C
  library.

### REQ-MIXER-VALUES-008 — speaker and solo-cue values

- **X.** `Speaker/Manual` is a Boolean, default `true`; its value text is `On` for
  true and `Off` for false. The formatter `0x1014353b0` (arm64 `0x10143ba28`) was run: a
  non-zero value gives `On`, zero gives `Off` (x2 `switch_text`).
- **D.** `SoloSink/@Value` is `false` in all 1,340 shipped mixers.
- **U.** What `SoloSink` controls (its parameter is named "Solo-Cue") and its default
  for a new mixer.

### REQ-MIXER-VALUES-009 — crossfade assign, crossfader and crossfade curve values

- **S.** `CrossFadeState/Manual` is `0` (A), `1` (None) or `2` (B), with value text
  `A`, `None`, `B`. A new mixer stores `1`. All 1,340 shipped mixers store `1` (D).
- **D.** The crossfader is `MainTrack/DeviceChain/Mixer/CrossFade/Manual`, a float32
  in [−1, 1] with `MidiControllerRange` `-1`–`1`; shipped sets store `0`.
- **S.** `LiveSet/CrossfadeCurve/@Value` selects the crossfade curve: 0 Dipped,
  1 Intermediate, 2 Constant Power, 3 Slow Fade, 4 Slow Cut, 5 Fast Cut, 6 Transition.
  The set is constructed with `2` (Constant Power).
- **D.** 375 of the 376 shipped LiveSet documents store `2`, B0 among them; one stores
  `6`.

### REQ-MIXER-VALUES-010 — number text on save

- **S.** Mixer float values (`Manual`, `MidiControllerRange/Min`, `Max`) are written by
  the 32-bit rule of [REQ-TRANSPORT-STATE-011](transport-state.md#req-transport-state-011--number-text-on-save)
  (P = 9, trailing zeros removed).
  Booleans are written `true`/`false`, and integers in plain decimal.
- **D.** All 6,329 shipped mixer float `Manual` values and all 1,852 `FloatEvent`s on
  mixer targets match that rule.
- Examples: 1 → `1`; float32(0.6) → `0.6000000238`; float32(−0.6) →
  `-0.6000000238`; float32(0.1) → `0.1000000015`; float32(0.005) →
  `0.004999999888`; the volume range ends → `0.0003162277571`, `1.99526238`.
- **U.** That a 12.4.3 save writes mixer values through this rule unchanged (only
  12.4d1/12.1d1 writes were inspected). No reference observation is available
  (ADR 0003, PRB-S9-07); a static trace of the writer for the mixer classes could
  settle it.

### REQ-MIXER-VALUES-011 — volume gain applied to audio and the silence floor

- **S/Q-019.** With crossfade assign None, the track gain is the volume
  position → gain result after converting the stored gain to position (REQ-005),
  followed by the silence floor: any resulting gain at or below
  float32(0.00032) = 0.0003199999919 (−69.897 dB) becomes exactly 0. The stored
  minimum (−70 dB) therefore renders silence. For A or B assignments use
  [REQ-MIX-GRAPH-003](mix-graph.md#req-mix-graph-003--volume-gain), including its
  Transition branch and A5 condition.
- **S/Q-019.** A gain can be audible while its text is `-inf dB` (REQ-006).
  Test the converted gain against the floor, not the stored value directly;
  rounding near the boundary is not covered by a general round-trip bound.
- **S.** The silence test follows the crossfade stage; the resulting gain scales
  the pan law (REQ-013). Transition (curve 6) applies the factor to position
  before evaluating the curve, as defined by REQ-MIX-GRAPH-003.
- **S/Q-019 (revision 4; replaces the revision-3 condition).** The logic layer sends
  p = the volume position of g, clamped to [0, 1]: the gain → position conversion of REQ-005
  (converter slot +0x28, x86_64 `0x102683d70` ✓). It does so for the manual value, at
  timeable creation and for envelope points.
  - The engine computes the gain by REQ-MIX-GRAPH-003, including the
    distinct Transition branch, and then applies the floor.
  - REQ-005 does not establish identity for arbitrary in-range g; retain the
    converted gain before applying crossfade and the floor.
  - Remaining conditions are those of
    [REQ-MIX-GRAPH-003](mix-graph.md#req-mix-graph-003--volume-gain): the wiring branch for
    A or B assignments (A5), and the envelope owner for automated volume (A3).
- **S.** Volume changes have no smoothing beyond ramps:
  - A constant volume produces no ramp after the start.
  - Automated volume moves linearly in fader position through ramps of 200 to 65,536
    samples ([REQ-MIX-GRAPH-014](mix-graph.md#req-mix-graph-014--how-often-automated-values-are-applied)).
  - The gain is curve 1 evaluated at each ramp end, linear in between, applied per sample
    ([REQ-MIX-GRAPH-009](mix-graph.md#req-mix-graph-009--when-gains-change)).

  This replaces revision 3's U on ramp length and smoothing.

### REQ-MIXER-VALUES-012 — send gain applied to audio

- **S/Q-019 (A4 of SPEC-MIX-GRAPH).** The gain a stored send value s applies to the signal
  sent to its return is g = floor(curve0(r)). Here r is the send-curve position of s (send
  converter of kind 0, ✓ x86_64 `0x102788389`), clamped to [0, 1], and the floor is that of
  REQ-011. Revision 4 settles this statically.
  - For in-range s retain both conversions: the general identity g = s is not
    established (REQ-005).
  - A converted send gain at or below 0.0003199999919 contributes nothing;
    the threshold is applied after conversion, not directly to stored s.
  - The engine converts through a level node of the send curve (✓ `0x1026f8ccd`); its
    connection to the send port is condition A4.
- **X, S.** Where the gain applies:
  - Pre-fader sends carry g times the device-chain output.
  - Post-fader sends carry g times the track's pan-law and volume matrix.
  - Pre or post is chosen per return by `LiveSet/SendsPre`.

  These rules are canonical in
  [REQ-MIX-GRAPH-005](mix-graph.md#req-mix-graph-005--sends-pre-and-post).

### REQ-MIXER-VALUES-013 — pan law

- **X.** For one track, with input channels L, R, output channels L′, R′, track gain
  v (REQ-011), split weight w and θ(x) = (x + 1)·π/4:
  - L′ = v·(w·cos θ(sL) + (1 − w)·max(10⁻⁵, √2·cos θ(p)))·L + v·w·cos θ(sR)·R
  - R′ = v·w·sin θ(sL)·L + v·(w·sin θ(sR) + (1 − w)·max(10⁻⁵, √2·sin θ(p)))·R
  - v = 0 gives silence.

  Here p is the pan, sL and sR the split pans, and w the pan-mode amount. The matrix function
  `0x101b719e0` (arm64 `0x101b3b95c`) was run on these inputs and produced exactly the gains in
  MV-035 to MV-037. It uses glibc `cos` (double); Apple's build may differ in the last float32
  ulp. arm64 fuses θ with `fmadd`; the float32 gains agree. These are computed gains, not
  rendered audio.
- **X, S.** In Stereo mode (w = 0) the pan is a balance control without cross-feed:
  0 dB at centre; at p = −1 the left channel is +3.01 dB and the right channel
  −100 dB (factor 10⁻⁵), not silent; at p = −0.5, +2.32 dB and −5.33 dB (X: the computed gains
  1.41421/10⁻⁵ and 1.30656/0.541196). In Split Stereo mode (w = 1) each input channel is panned
  by sin/cos with no lift: default splits (−1, +1) pass L and R unchanged (X: 1 and 1, with
  6·10⁻¹⁷ cross-feed); splits (0, 0) send each input to both outputs at −3.01 dB (X: 0.707107
  each). That w = 0 for pan mode 0 and w = 1 for pan mode 1 is still S (next bullet).
- **S (revision 4).** w is the stored `PanMode` code: w = 0 for pan mode 0 and w = 1 for
  pan mode 1. The track's `PanMode` passes through a ramp node into the pan-mode amount, so
  a change ramps w linearly over 75 samples
  ([REQ-MIX-GRAPH-004](mix-graph.md#req-mix-graph-004--main-matrix),
  [REQ-MIX-GRAPH-010](mix-graph.md#req-mix-graph-010--fade-lengths); wiring pseudocode). It
  replaces revision 3's U; MV-035 to MV-037 rest on it.
- **S (revision 4).** Pan and split-pan ramps:
  - Constant values produce no ramp after the start.
  - Automated values move along their segments through ramps of 200 to 65,536 samples
    (REQ-MIX-GRAPH-014).
  - The pan-law matrix is evaluated at the end of the shortest running input ramp and is
    linear in between (REQ-MIX-GRAPH-009, X).

  It replaces revision 3's U.

### REQ-MIXER-VALUES-014 — crossfade effect

- **S.** A track with crossfade assign None is not affected by the crossfader.
- **S.** A track assigned A is scaled by T(c) and a track assigned B by T(−c), where c is
  the crossfader value and T is the selected crossfade curve, a 129-point table over
  [−1, 1] with linear interpolation. Consequence: at c = 0, A and B tracks get the
  same factor, and an A track at c gets the factor a B track gets at −c.
- **S.** For curves 0–5 the factor multiplies the track gain. For Transition (6) it
  multiplies the fader position before the volume curve.
- **S.** A change of crossfade assign ramps over 2 ms. At the end of a ramp to None the
  crossfade factor is removed.
- **X.** The shape of each curve T(p), p = crossfader·(±1), from running all seven
  `OCrossFadeHelper::CrossfadeToLevel*` functions (x86 `0x101b1a470`…`0x101b1a8e0`, arm64
  `0x101aee8b8`…`0x101aeedb8`): every curve gives T(−1) = 1 and T(+1) = 0, and at p = 0
  Dipped = 0.5, Intermediate = 0.582, Constant Power = 0.707, Slow Fade/Slow Cut/Fast Cut = 1,
  Transition = 1; full values in MV-047. Combined with the static ramp sign (A → +1), the
  crossfader at −1 (full left) gives an A track unity and a B track silence. Slice note: Dipped
  and Intermediate fuse one multiply-add on arm64 (x86 separate, ≤1 float32 ulp); all seven use
  `cosf` (glibc, ±1 ulp vs Apple). The curves are computed gains; per-track application and
  ramps stay static (REQ-014 S bullets above, PRB-S9-06).

- **X (revision 6; finite helper annex).** For each exact binary32 input and curve
  code in [MV-049–MV-300](../../analysis/ableton-live-12.4.3/full-spec-v1/mixer-values-owner-r6-batch/cases-added.json),
  the supplied x86 scalar helper returns the listed `level_binary32_hex` bit
  pattern with the batch's recorded Linux math substitutions. These 252 distinct
  new input/function pairs adopt the already-reviewed whole boundary batch; its
  49 historical-X2 overlaps remain supporting controls rather than new cases.
  The annex specifies exact reference values for this finite calculation only.
  It supplies no new tolerance for ARM/Apple math. ADR 0003's ARM equivalence is
  an inference; the prior slice note does not establish a general one-ulp bound
  for these additional positions.
- **X (same finite scope).** Fast Cut at binary32 input `0x3f75c28f`
  (`0x1.eb851e0000000p-1`, binary32 0.96) returns `0xb33bbd2e`
  (−4.371138828673793e−8). A nonnegative clamp would contradict this local helper
  expectation. This position is off the runtime table's 1/64 grid: neither its
  sign nor another helper sample determines the interpolated 129-point table,
  actual track factor, host output, or an ARM/Apple result.

- **X (revision 7; finite regular-grid scalar references only).**
  [MV-301–MV-1126](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-mixer-r7-regular-nodes-finite-v1/cases903.json)
  record all 826 newly observed exact input/output binary32 pairs in the seven
  supplied scalar helpers' regular grid; the complete 903-point catalog also
  retains 77 historical references without new IDs or replay. These are exact
  native reference bits for the recorded x86 calculation and Linux substitutions,
  not pre-execution predictions, portable candidate expectations or new grades.
  Each fresh pre-call expectation remains NULL. Portable expected values,
  comparators and candidate grades remain NULL in the new catalog. Matching the
  nominal i = 0..128 coordinates does not identify actual runtime table contents,
  construction or interpolation. No current receiver, per-track ramp/audio/public
  delivery, ARM/Apple equivalence, general one-ulp bound or calibration follows.
  The existing revision 6 cases, static clauses and native precision limitations
  remain unchanged. The [revision 7 annex](#finite-regular-grid-scalar-observations-revision-7)
  states the finite input and provenance boundary.

### REQ-MIXER-VALUES-015 — out-of-range and alternative stored values

- **S/Q-019 (revision 4), rendering of out-of-range volume and send.** The position
  conversion clamps to [0, 1]
  ([REQ-MIX-GRAPH-003](mix-graph.md#req-mix-graph-003--volume-gain), 005). So:
  - a volume above 1.99526238 renders at 1.99526238 (+6 dB);
  - a send above 1 renders at 1;
  - a volume or send below 0.0003162277571, including 0 and negative values, renders
    silence.

  This assumes the value is held as written (next clause).
- **U.** What opening, displaying, rendering and saving do for any value outside the
  domains of REQ-002 to 004 and 009, except the rendering clause above: a volume below 0.0003162277571 (0 and negative
  values included) or above 1.99526238; a send below 0.0003162277571 (0 and negative
  values included) or above 1; a pan or split pan outside [−1, 1]; a pan mode other
  than 0 or 1; a crossfade assign outside 0–2; a crossfader outside [−1, 1]; a
  crossfade curve code outside 0–6. The static reading is that the set opens and the
  value is stored as written, and that controlled edits clamp; neither is established
  for these fields. No reference observation is available (ADR 0003, PRB-S9-05); a
  static trace of the loader for the mixer classes could settle the opening part.
- **U.** Whether a loaded `MidiControllerRange` text such as `0.00031622799`/`1.99526203`
  is kept, re-derived or rewritten on save. No reference observation is available
  (ADR 0003, PRB-S9-05, PRB-S9-07); a static trace of the writer could settle it.

## Timing and state

- Units: gain is linear amplitude; dB is 20·log10(gain); pan is −1…+1; positions are
  0…1.
- Persistent state: the values in REQ-001 to REQ-004, REQ-008 and REQ-009. Positions
  are not stored.
- Determinism: the text and save rules (REQ-006, 007, 010) are deterministic for a
  given float32 value. The curve gains depend on the platform `exp10` and `log10` and
  may differ in the last float32 ulp.
- Timing: the 2 ms crossfade-assign ramp (REQ-014) is derived here. Revision 4: volume, pan
  and send changes follow the per-sample ramp rules of [SPEC-MIX-GRAPH](mix-graph.md)
  (REQ-MIX-GRAPH-009, 010, 014). Undo and edits after load are out of scope.
- Interaction: REQ-MIX-GRAPH-003 defines the crossfade/curve branch; its floored
  gain is the pan-matrix gain input of REQ-013.

## Acceptance cases

Base document B0: the shipped `Core Library/Lessons/Sets/Recording Audio.als`
(SHA-256 `af57ff8f9eb1c2c51220ef6633a58838532350d53640df5f48dc01659023c043`), the
same base as SPEC-TRANSPORT-STATE. It is decoded, changed only as stated, and
re-encoded as gzip. Mixers: A = `/Ableton/LiveSet/Tracks/AudioTrack[@Id="0"]/DeviceChain/Mixer`,
R = `/Ableton/LiveSet/Tracks/ReturnTrack[@Id="2"]/DeviceChain/Mixer` (B0's only
return), M = `/Ableton/LiveSet/MainTrack/DeviceChain/Mixer`,
C = `/Ableton/LiveSet/PreHearTrack/DeviceChain/Mixer`. As shipped, every volume is
`1`, every pan `0`, splits `-1`/`1`, `PanMode` `0`, `CrossFadeState` `1`, `Speaker`
`true`, `SoloSink` `false`; A and R each hold one send with `Manual`
`0.00031622799`; the volume ranges are `0.00031622799`–`1.99526203`; M's
`CrossFade` is `0` and `LiveSet/CrossfadeCurve` is `2`.

A fragment such as A `Volume/Manual` = `0.5` means replacing the `Value` attribute of
`<Manual>` under that element. Kinds: P positive, B boundary, N negative or
out-of-range, S save, C computation (checks a derived function used by other
cases), R audio render (static expectation; no reference measurement is available,
ADR 0003), U unresolved (must not be graded).

Render fixture TT (proposed, not built): B0 with a 1 kHz sine at −12 dBFS on both
channels looped in a clip on track A, A routed to M, M volume `1`, pan `0`, R's send
from A at its minimum. Level comparators: the RMS level of the main output relative to
the same render with A at volume `1` and pan `0`; proposed tolerance ±0.05 dB down to
−60 dB, and "silence" means every A-derived output sample is exactly 0. These
tolerances are a proposal and must be decided before a run is accepted. A candidate
render can be compared only with these static expectations, never with a reference
render (ADR 0003).

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Label |
| --- | --- | --- | --- | --- | --- |
| MV-001 | 001, 003 | P | Open B0 unchanged | Opens. A and R each have one send; M and C have no sends. Volumes `0.0 dB`, pans `C`, pan mode Stereo, crossfade assign None, speaker On, A's send text `-inf dB`; crossfader 0, curve Constant Power. Not judged: `EnabledByUser` (B0 stores `true` on A's send and `false` on R's) and R's send to itself, because no clause defines an observable effect of `EnabledByUser` (REQ-003) | D/S |
| MV-002 | 002, 006 | P | A `Volume/Manual` = `0.5011872053` | A volume text `-6.0 dB` | S |
| MV-003 | 002, 006 | P | M `Volume/Manual` = `0.7367056608` | M volume text `-2.654 dB` | S |
| MV-004 | 006 | P | A `Volume/Manual` = `0.5`; separately `0.25` | `-6.021 dB`; `-12.041 dB` | S |
| MV-005 | 002, 006 | B | A `Volume/Manual` = `1.99526238` | `6.0 dB` | S |
| MV-006 | 002, 006 | B | A `Volume/Manual` = `0.0003162277571` | `-inf dB` | S |
| MV-007 | 006 | B | A `Volume/Manual` = `0.99999` | `0.0 dB` (no minus sign) | S |
| MV-008 | 006 | B | A `Volume/Manual` = `0.0003311311302` (−69.6 dB) | `-69.6 dB` | S |
| MV-009 | 006 | B | A `Volume/Manual` = `0.0003235936455` (−69.8 dB) | `-inf dB` | S |
| MV-010 | 003, 006 | P | A `Send/Manual` = `0.1` | A send text `-20.0 dB` | S |
| MV-011 | 003, 006 | B | A `Send/Manual` = `1` | A send text `0.0 dB` | S |
| MV-012 | 004, 007 | P | A `Pan/Manual` = `-0.6` | A pan text `30L` | S |
| MV-013 | 007 | B | A `Pan/Manual` = `0.004999999888`; separately `0.01` | `C`; `C` | S |
| MV-014 | 007 | B | A `Pan/Manual` = `0.0101`; separately `-0.0101` | `1R`; `1L` | S |
| MV-015 | 007 | B | A `Pan/Manual` = `1`; separately `-1` | `50R`; `50L` | S |
| MV-016 | 004, 007 | P | A `PanMode/@Value` = `1`, `SplitStereoPanL/Manual` = `-0.5`, `SplitStereoPanR/Manual` = `0.5` | Pan mode Split Stereo; split texts `25L` and `25R` | S |
| MV-017 | 009 | P | A `CrossFadeState/Manual` = `0`; separately `2` | Assign A; assign B | S |
| MV-018 | 008 | P | A `Speaker/Manual` = `false` | A speaker Off | X (x2, `0x1014353b0`) |
| MV-019 | 009 | P | `LiveSet/CrossfadeCurve/@Value` = `5` | Crossfade curve Fast Cut | S |
| MV-020 | 010 | S | A `Pan/Manual` = `0.6`; open, save | Saved A `Pan/Manual` `0.6000000238` | U: grades only REQ-010's U part |
| MV-021 | 010 | S | A `Send/Manual` = `0.1`; open, save | Saved `0.1000000015` | U: grades only REQ-010's U part |
| MV-022 | 010 | S | Open B0, save | Saved A, R, M, C `Volume`, `Pan`, split, `PanMode`, `CrossFadeState`, `Speaker`, `SoloSink` and `Send/Manual` values have the B0 text (`1`, `0`, `-1`, `1`, `0`, `1`, `true`, `false`, `0.00031622799`); `MidiControllerRange` text is MV-045 | U: grades only REQ-010's U part |
| MV-023 | 005 | C | Volume curve, position → gain | 0 → 0.0003162277571; 0.5 → 0.1995263398 (−14.0 dB); 0.7 → 0.5011872053; 0.85 → 1; 1 → 1.99526238; within 1 float32 ulp | X (x2, `0x101aecbd0`) |
| MV-024 | 005 | C | Send curve, position → gain | 0 → 0.0003162277571; 0.5 → 0.1000001132 (−20.0 dB); 0.85 → 0.5011872053; 1 → 1; within 1 ulp | X (x2, `0x101aecbd0`) |
| MV-025 | 005 | C | Gain → position | Volume: 0.5 → 0.699474, 0.001 → 0.034624; send: 0.1000000015 → 0.5; volume 2 → 1; within 1e-6 | X (x2, `0x101aecc90`) |
| MV-026 | 002, 005 | C | Default volume and send ranges | gain(0) writes `0.0003162277571`, volume gain(1) `1.99526238`, send gain(1) `1` | S, D |
| MV-027 | 002–004, 008, 009 | P | No user default set or default-track preset installed; open B0, insert one new audio track, save | New mixer: volume `1` with range `0.0003162277571`–`1.99526238`; pan `0`, splits `-1`/`1` with range `-1`–`1`; `PanMode` `0`; `CrossFadeState` `1`; `Speaker` `true`; one send `0.0003162277571`, range `0.0003162277571`–`1`, `EnabledByUser` `true` | U: graded only through the save, REQ-010's U part (defaults S) |
| MV-028 | 003 | U | Open B0, insert a second return track, save | `EnabledByUser` of each new holder in A, R and the new return: unresolved (static: A's new holder `true`) | U |
| MV-029 | 011 | R | TT, A volume `1` | 0.00 dB relative level | S/Q-019 |
| MV-030 | 011 | R | TT, A volume `0.5011872053` | −6.00 dB | S/Q-019 |
| MV-031 | 011 | R | TT, A volume `0.001` | −60.0 dB | S/Q-019 |
| MV-032 | 011 | R | TT, A volume `0.0003162277571` | Silence | S/Q-019 |
| MV-033 | 011 | R, B | TT, A volume `0.0003235936455` (text `-inf dB`) | −69.8 dB, not silent | S/Q-019 |
| MV-034 | 011 | U | TT, A volume `0.0003199999919` | Unresolved at the exact stored boundary: grade the gain after both conversions; no exact-return guarantee or general error bound applies here | U |
| MV-035 | 013 | R | TT, A pan `-1` | Left +3.01 dB, right −100 dB (not silent); gains MV-048 | S; gains X (MV-048); w mapping S; render not measured |
| MV-036 | 013 | R | TT, A pan `-0.5` | Left +2.32 dB, right −5.33 dB; gains MV-048 | S; gains X (MV-048); w mapping S; render not measured |
| MV-037 | 013 | R | TT with the sine on the left channel only; A pan mode `1`, splits `0`/`0` | Left and right outputs each −3.01 dB; gains MV-048 | S; gains X (MV-048); w mapping S; render not measured |
| MV-038 | 014 | R | TT, A assign None; crossfader `-1`, `0`, `1` in three renders | Same level in all three | S |
| MV-039 | 014 | R | TT, renders with A assign A at crossfader c and with A assign B at −c, for c in {−1, −0.5, 0, 0.5} | Pairwise equal levels; absolute levels from MV-047 | S; curve levels X (MV-047); render not measured |
| MV-040 | 012 | R | TT, A send `0.5011872053` (post-fader, `SendPreBool` `false`), R volume `1`, return routed to M | Main level +3.53 dB relative (A plus R: 1.5011872 times the A-only output) | S/Q-019 (A4 and A7 of SPEC-MIX-GRAPH); gains X; render not measured |
| MV-041 | 015 | U | A `Volume/Manual` = `2`; open, display, render, save | Unresolved (static reading: opens; text `6.021 dB`). Render part S/Q-019: +6.0 dB if held as written | U |
| MV-042 | 015 | U | A `Volume/Manual` = `0`; separately `-1` | Unresolved (static reading: opens; text `-inf dB`). Render part S/Q-019: silence if held as written | U |
| MV-043 | 015 | U | A `Pan/Manual` = `1.5` | Unresolved | U |
| MV-044 | 015 | U | A `CrossFadeState/Manual` = `3`; separately `PanMode` `2` | Unresolved | U |
| MV-045 | 015 | U | Open B0 unchanged, save | Saved `MidiControllerRange` texts unresolved (static reading: `0.00031622799`/`1.99526203` kept) | U |
| MV-046 | 007 | B | A `Pan/Manual` = `0.33` | `17R` (float32 value × 50 = 16.50000066, not a tie) | S |
| MV-047 | 014 | C | Crossfade curve level T(p) for each `CrossfadeCurve` code, at p = −1, −0.5, 0, 0.5, 1 | T(−1) = 1 and T(+1) = 0 for every curve. At p = 0: Dipped 0.5, Intermediate 0.582107, Constant Power 0.707107, Slow Fade 1, Slow Cut 1, Fast Cut 1, Transition 1. At p = −0.5: Dipped 0.791322, Intermediate 0.846931, Constant Power 0.931591, Slow Fade/Slow Cut/Fast Cut 1, Transition 1. At p = 0.5: Dipped 0.223238, Intermediate 0.278848, Constant Power 0.363508, Slow Fade 0.677282, Slow Cut 0.994978, Fast Cut 1, Transition 0.5. Rounded examples only; compare full-precision X levels in x2 results with one adjacent binary32 step or absolute error ≤ 10⁻¹² | X (x2, `0x101b1a470`–`0x101b1a8e0`) |
| MV-048 | 013 | C | Pan-law output-gain matrix (L→L, L→R, R→L, R→R) for `0x101b719e0` on [w, pan, splitL, splitR, vol] | Stereo (w 0, splits −1/+1, vol 1): pan −1 → (1.41421, 0, 0, 1e−5); −0.5 → (1.30656, 0, 0, 0.541196); 0 → (1, 0, 0, 1). Split (w 1, pan 0, vol 1): splits −1/+1 → (1, 6.1e−17, 6.1e−17, 1); 0/0 → (0.707107, 0.707107, 0.707107, 0.707107). vol 0 → all 0. Rounded examples only; compare full-precision X gains in x2 results with one adjacent binary32 step or absolute error ≤ 10⁻¹² (the 6·10⁻¹⁷ cross-feed is covered by the absolute bound, not one ulp at zero) | X (x2, `0x101b719e0`) |

### Finite helper cases added in revision 6

[MV-049–MV-300](../../analysis/ableton-live-12.4.3/full-spec-v1/mixer-values-owner-r6-batch/cases-added.json)
are 252 separately identified C/X cases: all 36 new-relative-X2 binary32 positions
for each of the seven scalar helpers, in retained source order. Each case records
curve code, exact input bits, exact expected output bits and its reviewed result
pointer. The action is a direct helper computation with the batch's supplied
inputs and substitutions. The expected bits describe that recorded x86
calculation; no portable ARM/Apple tolerance is established for these new inputs,
and no application or candidate grade is assigned by adopting them.

The [batch review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/batch-mix-leaves-v1-review.json)
approved all 301 boundary observations. The
[corrected lineage review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mix-boundary-owner-reconciliation-v2-review.json)
distinguishes 49 repeated historical-X2 pairs from the 49 released pairs: only
35 boundary pairs occur at released positions, 266 lie outside them, and 14
released pairs are absent from the boundary batch. Per curve the historical
nine inputs include both ±0.25 and ±binary32(0.95); the seven released positions
include ±0.25 and exclude ±0.95, while the 43 boundary positions include ±0.95
and exclude ±0.25. The ±0.95 observations are historical controls here, not new
cases or a release extension. Existing MV-001–MV-048 rows and all 80 released
objects, including the 49 released crossfade inputs and their comparators,
remain unchanged. The 36 allocator-patched setup rows remain withheld.

Comparators: "opens" is judged by whether the set finishes loading. Text comparisons
are exact strings, against an observation in the forms of REQ-006 to 008 (with ` dB`
and `-inf dB`; with `C`, `L` or `R`; `On` or `Off`). An observation in another form,
for example the digits without the unit, is inconclusive, not a mismatch. Saved
values are exact attribute text. The preserved table's C cases compare numbers within the stated tolerance;
the revision 6 annex instead records exact bits in its stated x86-helper scope. For MV-047/048 the
full-precision reference is `results/mixer.json` in the
[x2 packet](../../analysis/ableton-live-12.4.3/r2/x2-mixer-v1/manifest.json),
not the rounded display examples above. The tolerance is the released
[mixer-values-v2 comparison](../../handoff/mixer-values-v2/spec.md#acceptance-representation-and-comparison).
R cases follow the TT comparator. Cases labelled U, and the U parts named in the
label column, must not be graded as passes. Cancellation and teardown kinds are
omitted: loading, displaying and saving these values has no cancellable step in this
scope. Malformed text (a `Manual` that is not plain decimal
text, other Boolean or code text) has no case and no expectation: the reading is
assumed for plain decimal text only (see the reading assumption above).

The preserved MV-001–MV-048 table has 48 cases. 6 are extracted execution (X): MV-018 (On/Off text), MV-023 to MV-025
(fader-curve conversions and round trip), MV-047 (crossfade curve levels) and MV-048 (pan-law
gains). 20 are static or documented (MV-001 to MV-017, MV-019, MV-026, MV-046). 11 are audio
renders with static or X-derived gain expectations that remain unmeasured against a reference
(MV-029 to MV-033 and MV-035 to MV-040). MV-029 to MV-033 and MV-040 rest on the Q-019 result and its conditions,
and the gains of MV-035 to MV-039 are X via MV-047/MV-048. 11 are ungraded (MV-034; MV-020 to MV-022
and MV-027, which grade only REQ-010's U part; MV-028; MV-041 to MV-045). The dB and pan value texts of MV-002 to MV-017
were independently confirmed by the x1 extracted-execution pilot
([extracted execution](../research/extracted-execution.md)); they keep the S label here because
the x2 packet did not re-run them.

Revision 6 adds 252 C/X finite helper cases to that table, giving 300 draft case
IDs: 258 X, 20 static/documented, 11 unmeasured renders and 11 ungraded. These
case counts are not required-outcome coverage or application grades.

## Open questions

[Q-019](../questions.md#q-019-mixer-volume-and-send-values-sent-to-the-engine). Revision 4:
the engine-port value (REQ-011) and the send gain path (REQ-012) are settled statically by
T1.4 ([SPEC-MIX-GRAPH](mix-graph.md) r1). The logic layer sends fader positions; the engine
applies the curve, the crossfade factor and the floor. Conditions A3 to A5 of that spec remain.

Still open:

- out-of-range values on open and save (REQ-015);
- which surface shows which text (REQ-006, 007);
- the cue volume (REQ-002).

`SoloSink` (REQ-008): SPEC-MIX-GRAPH r1 reads it statically as the Solo/Cue button state.
Applying that here is left to a later revision. The pan law (REQ-013), crossfade curves (REQ-014)
and On/Off text (REQ-008) are X (revision 3). The
[probe batch](../../analysis/ableton-live-12.4.3/r2/s9-mixer-v1/probe-batch.json)
PRB-S9-01 to 08 records what observation would have settled; under ADR 0003 it will not run,
and the extracted-execution results are in [x2-mixer-v1](../../analysis/ableton-live-12.4.3/r2/x2-mixer-v1/manifest.json).
PRB-S9-08 (automation interpolation) belongs to the automation spec. The records map to cases
as follows: PRB-S9-01, 02, 03 and 06 to MV-029–039, MV-047 and MV-048; PRB-S9-04 to
MV-001–022; PRB-S9-07 to MV-022, 027, 028 and 045.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical research:
[mixer values](../research/mixer-values.md), retained run
`analysis/ableton-live-12.4.3/r2/s9-mixer-v1/` (image `Live.arm64` SHA-256
`3a99ceea…d1c383cfad`, image base `0x100000000`). D8 added two query rounds,
`d8-0001` (8 dossiers) and `d8-0002` (6), in
`/var/tmp/sound-analysis/query-spool/results/`. They are not yet copied into the
repository. Pointer reads used `s9-mixer-v1/read_ptrs.py` on `derived/Live.arm64`.
✓ means the cited branch was read in a dossier's disassembly. "RC §n" cites section n
of the mixer-values-v1 reviewer's [static checks](../../analysis/ableton-live-12.4.3/handoff-staging/mixer-values-v1-analysis/review/review-checks-static.txt),
which disassembled the cited sites in `derived/Live.arm64` (RVM-01, RVM-07).

| Requirement | Evidence | Strength |
| --- | --- | --- |
| 001 | Schema `12.0_12402`, `static-survey.json` `schema`, `documents.tracks` (1,340 mixers in 376 documents); B0 lines 105–240 | D; S for "same domains" from one shared constructor `0x10271b660` |
| 002 | Constructor `0x10271b660` ✓ s9-0001: volume control `0x10255d93c(…,1)`, float setup `0x1026f0bcc(0,1,1,…,"Track Volume",0)`; gain table `0x10588302c`/`0x105883044` (`image-reads.txt`; mode 1 `0x39a5cb5f`–`0x3fff64c2`, the upper one step above float32(10^(6/20)) = `0x3fff64c1`, RVM-02); MIDI range `0x1025856a0` ✓ d8-0002 (Min/Max = control slot +0x30 of s0, s1); `derive_curves.py` self-check | S + D |
| 003 | Send holder init `0x102658f54` ✓ s9-0002 (default = control slot +0x30(0), `EnabledByUser` true); send control `0x1026605c8` (mode 0); census `returns_per_doc`, `rare_value_docs` | S + D; return default site U |
| 004 | Pan setup `0x10271c734` ✓ s9-0001: linear control `0x1015757c0(-1,1,1/63,0.01)`, Pan (−1,1,0), Left (−1,1,−1), Right (−1,1,1); `PanMode` enum `0x101567ad8` ✓ (index 0) | S + D |
| 005 | Table `0x101ac2bf8` ✓, gain table `0x101ac2ad8`, position → gain `0x101ac3498` ✓, gain → position `0x101ac353c`/`0x101ac3c94` ✓, mode ranges `0x1058486a8`/`0x1058486c4`; identity bypass flag `DAT_106f7e914` set only by scope helpers `0x101ac3d74` (runtime use unknown); tables regenerated in D8 from `derive_curves.py` `db_table`. **X (x2):** position → gain `0x101aecbd0` and gain → position `0x101aecc90` run on the built curves; values match (MV-023–025) and exact round trips are established only at the seven released curve points (mixer-values-v2 review RVM2-01). Slice: both slices use a double intermediate so float32 outputs agree (no `fma` call); the dB-table landing `fmadd` (`0x101ac30ec`, x86 separate at `0x101aec640`) gives ≤1 ulp at positions 0.01–0.03 only (`fma-scan.txt`) | S; X for the conversions; UI binding U |
| 006 | `0x102183bf4` ✓ (gain → dB, ≤ 0 → −140), `0x102183abc` ✓ (floor −70, 3/1 decimals, suffix), `0x101437334` ✓, `0x101431c6c` ✓; formatter `(3,1,1,1)` ✓ `0x10271c138`; second slot `0x1014374b4` (no `-inf`, no unit; pseudocode) | S |
| 007 | `0x10143a290` ✓ s9-0002: double compares with ±0.01 (`0x3f847ae147ae147b`), multiply by ±50 in double, wrapper `0x101431c60` ✓ d8-0002 sets max = min = 0 decimals; same formatter singleton `0x101439ec4` for pan and both splits (`0x10271c734`, all three call sites ✓ RC §4) | S; ties U |
| 008 | `0x1026ec1cc` ✓ s9-0004 (bool init writes 1 to value and Manual). On/Off text: `0x10271b660.c` lines 284–287 (s9-0001) pass the text object from `0x10143b884` (corpus record kept; vtable `0x106670bc8`) to `0x1026ec1cc`; `image-reads.txt` gives that vtable's `+0x28` as `0x10143ba28`, which returns "Off" for 0.0 and "On" otherwise (✓ RC §2: call site `0x10271bcb0`–`0x10271bcc4`, `0x10143ba28`–`0x10143ba40`, strings `0x105af67ac`, `0x105bafc64`). **X (x2):** `0x1014353b0` (x86 twin of `0x10143ba28`) run — value ≠ 0 → "On", 0 → "Off". "Solo-Cue" with `SoloPrehearSinkController` | S; X for On/Off; SoloSink U |
| 009 | Constructor call `0x1026ef060(xf, 1, ["A","None","B"], …)` at `0x10271bf38` ✓ s9-0001; wrapper `0x1026ef060` passes arguments through (pseudocode); `0x1026ef0dc` ✓ d8-0002 passes index x1 to `0x101567bfc` for value and Manual; curve names `0x102672204`, helpers `0x101aed36c` ✓. Curve binding (✓ RC §3): the set constructor `0x102672448` (C1 record, kept in the review's `corpus-excerpts-review.jsonl`) loads member `[this+0x1f0]`, calls the name list at `0x1026740d8` and the enum init `0x101567bfc` with index 2 at `0x1026740f8`; the LiveSet registry call at `0x10266e148`–`0x10266e174` names the member at `0x1e8` `mpCrossfadeCurve` (+8 convention). Census: `CrossfadeCurve` in the 376 documents of `inputs-documents.tsv`, 2 in 375 and 6 in 1 (recounted 2026-10-18) | S (default index upgraded from inferred) + D |
| 010 | N1 writer rule ([transport-state native](../research/transport-state-native.md#writer-number-format)); `static-survey.json` `lexical_rule_match` | S + D |
| 011 | Consumers of the volume port output, `0x1027200f8` ✓ d8-0001: when an integer read from the track (`0x10248256c(track,1)`, slot 0x370) is ≥ 0, port +0x68 `Out` → crossfade unit +0x28 `Volume` (`0x1027202b8`–`0x1027202e8`), unit `Volume` → track-out +0x20 (`0x102720300`); otherwise `0x10246a3d4(+0xa8, 1)` at `0x102720378` sets an `AConvertLevel` (`0x10246a1a4` ✓, same constructor as `SNewCompound<AConvertLevel>`) to curve 1 and `Out` → converter → track-out `Volume` (`0x102720394`–`0x1027203c4`). `OCrossFadeVolumeProcessor` `0x101aede40` ✓ applies `0x101ac3bac(x,1)` then `≤ 0x39a7c5ac → 0`; `OConvertLevelRampEventProcessor::OnIn` `0x101aee660` ✓ d8-0002 and `OConvertLevelProcessor::OnIn` `0x101aee5e8` ✓ apply curve then the same floor. Port binding: volume port +0x68 and pan port +0x50 are one class (`0x1024f5674`, vtable `0x1067c7a48`) bound to timeables +0x318 and +0x2d0 by slot 0xb8 (`0x102720bd4`–`0x102720be8` ✓); bind `0x1024f5c08` ✓ d8-0001 wires a sub-unit (`0x1024f4b08` ✓: `TimeablePlayer`, `ModulationPlayer`, `Modulator` = `FloatModulatorProcessor`, `Out`); combiner `0x101b09ac8` ✓ is linear with a clamp. Default envelope event = constructor default value in the stored (gain) domain, `0x1026f0d84` (pseudocode). Gain → position conversion site not found Revision 4 (T1.4, [t14-mix-v1](../../analysis/ableton-live-12.4.3/r2/t14-mix-v1/manifest.json), `notes-q019.txt` §1–2): volume converter `ALevelUserFloatConverter` kind 1 (✓ x86_64 `0x10284f013`); slot +0x28 = clamped gain → position ✓ `0x102683d70`; manual value AUserFloat slot 0x208 ✓ `0x1015650c0`; timeable creation slot 0x310 `0x10282ea20` (pc); envelope points via the owner provider (pc, condition A3); x86_64 wiring `0x102853480` = arm64 `0x1027200f8`, curve-1 converter ✓ `0x102853727`; ramps `notes-mix.txt`. | S/Q-019 |
| 012 | `OTrackOutVolumeProcessor::OnSend<k>` `0x101b191d4` → `0x101b18bb4` → `0x101b10efc` (pseudocode, no curve); send unit `0x1025c36ec` ✓ d8-0001 is built from a node graph cached per class descriptor (`0x1025d2264`), whose node list was not resolved; an `AConvertLevel` node factory with a configurable curve exists (`0x1025d2aa8`, no direct caller) Revision 4: send converter kind 0 ✓ `0x102788389`; level node of the holder graph builder ✓ `0x1026f8ccd` (connection to `Send<k>` pc, condition A4); send matrix `TSendVolumes::Calc` x86_64 `0x101b40d30` (X, t14) = arm64 `0x101b10efc`. | U |
| 013 | Matrix `0x101b3b95c` ✓ s9-0002; ramp inputs `0x101afb494` ✓. Input names, D8: `0x101b10fe4` ✓ d8-0002 registers `PanModeAmount`, `Pan`, `StereoSplitPanL`, `StereoSplitPanR`, `Volume` with handler pointers `0x1065423f8`/`400`/`408`/`410`/`4a0` → `OnPanRampEvent<0..3>` `0x101b18834`/`880`/`8cc`/`918` and `OnVolume` `0x101b18964` (pointer reads). Index meaning upgraded from inferred (port order) to static; `PanModeAmount` from `PanMode` not traced. **X (x2):** the matrix (x86 `0x101b719e0`) run on [w, pan, splitL, splitR, vol] gives MV-048's gains; glibc `cos`, ±1 ulp Revision 4: `PanMode` → `PanModeRamp` (75-sample `OMakeRampProcessor`) → `PanModeAmount`, x86_64 builder `0x102866450` (pc); fade time X (t14); matrix ramp recompute `0x101b27860` (X, t14). | S; gains X (MV-048); w mapping S |
| 014 | `0x101aedff0` ✓ (target 1 − state, 0.002 s ramp), `0x101aee124` ✓ (factor off when target 0), `0x101aede40` ✓ (x = (c·s′ + 1)·64 into a 129-point table; byte table `0x105bb3a43`), Dipped `0x101aee8b8` ✓; other shapes pseudocode. **X (x2):** all seven `OCrossFadeHelper::CrossfadeToLevel*` (x86 `0x101b1a470`–`0x101b1a8e0`) run — levels in MV-047; T(−1)=1, T(+1)=0; table builder `0x101b191e0` fills T(i/64−1); glibc `cosf`, Dipped/Intermediate have one arm64 `fmadd` (≤1 ulp) | S; shapes X (MV-047); per-track application U |
| 015 | Loader direct store (N1 rule, not re-traced for mixer classes; schema `12.0_12402` types `Tempo` as `TimeableSongTempo` and the mixer floats as `TimeableFloat`); `rare_value_docs` (Driver Error Compensation, Playing Software Instruments, Recording Audio, 8-Track Template, Podcast & Radio) Revision 4: rendering clause from the clamp in `0x102683d70` ✓ and the floor (REQ-MIX-GRAPH-003, 005). | U |

Revision 6 adopts the finite boundary results from the
[approved batch](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/batch-mix-leaves-v1-review.json)
under design revision 12's one-review batch-adoption rule. Historical source
inputs are X2; execution used the unchanged T14-derived loader. The
[corrected lineage](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mix-boundary-owner-reconciliation-v2.json)
and its approved review supersede the old T14 input label, not original bytes.
The [adoption packet](../../analysis/ableton-live-12.4.3/full-spec-v1/mixer-values-owner-r6-batch/README.md)
pins the revision 5 baseline and the result-to-case projection. Its finite annex
supersedes the older discovery-only disposition for these 252 pairs; old research
and review dispositions remain historical. No second observation review, original
run, new source/receiver proof or release is supplied. Glibc 2.39 is supplementary
post-run context, not a per-child loaded-library/FP-control trace.

Corrections and contradictions:

- `curves.txt` prints pan `0.33` → `16R`. `derive_curves.py` used the double 0.33.
  A stored float32 0.33 (0.330000013) gives 16.50000066 → `17R`. REQ-007 uses
  float32 inputs and excludes exact ties.
- The research example "−69.7 dB → `-69.7 dB`" sits about 3·10⁻⁶ dB from the
  threshold, within float32 `log10` ulp error. This draft grades −69.6 and −69.8 dB
  instead.
- Research marked the pan input order and the crossfade-assign default as inferred.
  D8 dossiers upgrade both to static (rows 009 and 013).
- Revision 1's REQ-002 called 1.99526238 float32(10^(6/20)). It is one float32 step
  above it (`0x3fff64c2` against `0x3fff64c1`) and equals G[100] of the volume curve
  (RVM-02). The research page's MX-02 had the same error; a correction note was added
  there.
- Revision 1 said malformed `Manual` text follows SPEC-TRANSPORT-STATE. That is not
  supported for the mixer classes (F5, row 015); revision 2 assumes the reading for
  plain decimal text only.
- Revision 3 (x2 extracted execution). The fader-curve conversions, pan law, crossfade
  curves and On/Off text were run on the x86_64 slice. `derive_curves.py`'s `gain_to_norm`
  rounds each operation to float32, but both slices use a double intermediate, so the script can
  be one float32 ulp off (e.g. position 0.85 from gain 1.0: script 0.84999996, X 0.85000002);
  this is inside MV-025's 1e-6 tolerance. The x86_64 slice imports `fma`/`fmaf` but none of these
  mixer functions call them, so glibc's exact `fma` does not reproduce the arm64 fused operations;
  the surviving ≤1 ulp slice differences are the dB-table landing points and the Dipped/Intermediate
  crossfade curves (`fma-scan.txt`), neither in any released or graded value. The crossfade result
  gives T(−1)=1 and T(+1)=0 for every curve, so with the static ramp sign (A → +1) the crossfader
  at −1 favours A; REQ-014 still marks the per-track application static. The enum code names
  (`A`/`None`/`B`, `Stereo`/`Split Stereo`, the curve names) and the crossfader value text were not
  run: a value→name run needs a constructed enum object, and no value-text formatter for the
  crossfader was located, so they stay as RVM-03/04's stated assumption and REQ-009's unknowns.

Not drafted from the candidates, or narrowed:

- Arrow-key ±1/±0.1 dB steps (MX research, slots +0x40–0x58) and text parsing
  (`0x102183c64`, `0x10143a3d8`): these are edits, out of scope.
- Curves 2–6 (`-40 to +3 dB` … `-70 to 6 dB RMS`): not used by the mixer.
- The second formatter slot: its surface is unknown (REQ-006 U).
- Cue volume as the preview level: inferred from a string; REQ-002 U.
- Holder `Id` gaps: no behavior found; REQ-003 U.
- MX-06's "fader and MIDI mapping domain": kept only as REQ-005 U.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from candidates MX-01–MX-15 and two D8 query rounds. 15 requirements: 3 D/S only (001, 004, 009); 9 D/S with U parts (002, 003, 005, 006, 007, 008, 010, 013, 014); 1 S/Q-019 with a U part (011); 2 U only (012, 015). 45 unexecuted cases: 27 static or documented, 11 renders needing measurement (6 also conditional on Q-019), 7 unresolved |
| 2 | 2026-10-18 | Applies the mixer-values-v1 staging findings and review ([plan](mixer-values-handoff-plan.md#review-outcome), [review](../../handoff/mixer-values-v1/REVIEW.md)). Applied: F1, F2 and RVM-01 (citations for the REQ-008 On/Off text and the REQ-009 curve binding; curve census and initial code 2); RVM-02 (REQ-002 upper bound); F7 and review fix 3 (MV-001 no longer grades `EnabledByUser` or R's own send; new REQ-003 U clause); F3 (candidate list below); F4 (MV-020–022 relabelled U, and MV-027 for the same reason); F5 (malformed-text sentence replaced by a stated reading assumption); F6 (REQ-015 lists every out-of-domain value); F8 (0.00005 dB width at −69.7 dB, ±0.0005 dB and three-decimal halfway points); F9 (new MV-046, pan 0.33 → `17R`); RVM-03 and RVM-04 (display assumption; `On`/`Off` among the text forms); RVM-07 (split-pan text object confirmed, row 007; code-name assumption stated). Rejected: none. ADR 0003: probe-dependent clauses stay U and name a static route where one exists. Requirement counts unchanged. 46 unexecuted cases: 24 static or documented, 11 renders with static expectations only (6 also conditional on Q-019), 11 ungraded |
| 3 | 2026-10-18 | Extracted execution of the x86_64 slice ([x2-mixer-v1](../../analysis/ableton-live-12.4.3/r2/x2-mixer-v1/manifest.json), label X; ADR 0003). New X label (evidence table). REQ-005 position ↔ gain conversions are X, with an exact round trip (bears on Q-019); REQ-008 On/Off text is X; REQ-013 pan-law gains are X; REQ-014 crossfade curve shapes are X. REQ-011's condition now cites the exact round trip; the engine-port value stays unknown (Q-019 narrowed, not closed). New cases MV-047 (crossfade curve levels) and MV-048 (pan-law gains), both X; MV-018, MV-023–025 relabelled X; MV-035–039 note the X-derived gains while the render stays unmeasured. Slice comparison recorded (`fma-scan.txt`): no `fma`/`fmaf` call in these functions, ≤1 ulp differences at the dB-table landing points and the Dipped/Intermediate curves, outside any graded value. `derive_curves.py` `gain_to_norm` correction. Requirement count unchanged. 48 cases: 6 X, 20 static/documented, 11 unmeasured renders, 11 ungraded |
| 4 | 2026-10-18 | T1.4 static trace ([SPEC-MIX-GRAPH](mix-graph.md) r1, [t14-mix-v1](../../analysis/ableton-live-12.4.3/r2/t14-mix-v1/manifest.json)). Q-019's engine-port value is settled statically with SPEC-MIX-GRAPH's conditions A3 to A5; the S/Q-019 label is redefined accordingly. REQ-011: the logic layer sends the clamped fader position, and the volume ramp and smoothing U is replaced by the mix-graph ramp rules. REQ-012: the U becomes S/Q-019, the send-curve gain with the floor, pre and post per REQ-MIX-GRAPH-005. REQ-013: both U clauses become S (w = `PanMode`, 75-sample ramp; pan ramps per the mix-graph rules). REQ-015: the rendering of out-of-range volume and send becomes S/Q-019; open, display and save stay U. MV-040 becomes a render case; MV-041 and 042 note their render parts. Requirement count unchanged. 48 cases: 6 X, 20 static or documented, 12 unmeasured renders, 10 ungraded |
| 5 | 2026-10-19 | Correct REQ-005, 011 and 012’s general exact-round-trip claim using mixer-values-v2 review RVM2-01; the seven tested curve points remain exact under the release assumption. Clarify the forward-fed snap (RVM2-07). No general round-trip bound is established. Pan-mode mapping labels aligned to the static trace; MV-047/048 use full-precision references and absolute 10⁻¹² bounds alongside adjacent-float comparisons. Out-of-range load behavior remains U; MV-034’s exact stored silence-boundary expectation is ungraded. 48 IDs: 6 X, 20 static/documented, 11 conditional renders, 11 ungraded. |
| 6 | 2026-10-21 | Adopt all 252 new-relative-X2 scalar crossfade-helper pairs from the already independently reviewed boundary batch as exact finite X reference expectations under REQ-014, with cases MV-049–MV-300. All 49 historical agreements remain supporting controls; released ±0.25/±0.95 lineage and all 80 released objects remain unchanged. Exact bits apply only to the supplied x86 calculation with recorded glibc substitutions; no new portable ARM tolerance, runtime-table interpolation, public sign/audio law, application grade or release. All other 14 requirement bodies and prior 48 case rows remain exact. |
| 7 | 2026-10-21 | Add 826 new finite regular-grid scalar observations MV-301–MV-1126 from the sole approved903-point summary;77 inherited joins receive no new IDs or replay. Preserve the 14 other requirement bodies, prior REQ-014 text, 48 old rows, 252 R6 case objects and 80 released objects. Native bits describe only captured x86/Linux calculations; pre-call NULL history and portable expected/comparator/grade NULL remain. No runtime129-table, public/ARM/tolerance/calibration or coverage law. |

Before the 2026-10-18 review, revision 1 proposed a first candidate with MV-001–026.
Those cases exercise REQ-001 to 010; its list (001, 002, 003, 004, 006, 007, 009 and
010) omitted REQ-005 (MV-023–026) and REQ-008 (MV-018). The release took a narrower
scope, below. REQ-005 is needed by any renderer. REQ-010's save cases stay ungraded,
and REQ-011, 013 and 014 stay out: no reference observation or measurement is
available (ADR 0003), and REQ-011 also needs Q-019.

Released 2026-10-18: [mixer-values-v1](../../handoff/mixer-values-v1/README.md), 37 cases, approved with corrections by a separate review agent (partial REQ-001 to 004, 006 to 009 only; 005, 010 to 015 unreleased). The review findings to apply in the next revision are on the [handoff plan](mixer-values-handoff-plan.md#review-outcome). Revision 2 applies those findings; the release is unchanged and still pins revision 1. Draft clauses outside the release's partial scope, listed per requirement in the plan's [scope table](mixer-values-handoff-plan.md#scope), are broader than mixer-values-v1.

A later release revision may now add the REQ-005 fader-curve conversions, the REQ-013 pan-law
gains and the REQ-014 crossfade curve shapes as X-supported clauses (MV-023–025, MV-047, MV-048),
and REQ-008's On/Off text as X; these are computed-gain and text results, not a rendered-audio
comparison, so they still carry no audio compatibility claim (ADR 0003). Revision 4: REQ-011 and
REQ-012 could join a later release only with SPEC-MIX-GRAPH's Q-019 conditions (A3 to A5) stated.
They remain computed-gain contracts without a reference measurement. mixer-values-v1 is not
contradicted by revision 4. It releases no audio-path clause, and it leaves `SoloSink`'s meaning,
the curves and every effect on audio unreleased.

Current release: [mixer-values-v2](../../handoff/mixer-values-v2/README.md),
80 cases, supersedes v1. Its review RVM2-01 to 05 narrows computed values to
the listed inputs; audio application remains outside that release.

## Finite regular-grid scalar observations (revision 7)

This annex adopts 826 fresh finite scalar observations as MV-301–MV-1126 and
preserves 77 exact inherited references without new IDs, fresh receipts or replay.
Its [complete 903-point catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-mixer-r7-regular-nodes-finite-v1/cases903.json)
is a finite supplied-input extension under REQ-014, not a new application law.
The [sole independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mixer-regular-knots-v1-review.json)
is the authority for every input word, output word and provenance join. The owner
mapping adds no new measurements, model, fit or second review of actual captures.

**Complete supplied class.** For each of the seven selected scalar helpers,
i ranges over every integer 0..128 inclusive; k = i − 64 and p = k/64. Each exact
binary32 p is supplied by the recorded `f:` hexadecimal token. Every input token,
input word and output word appears in the catalog. Eleven existing k values per
helper (−64, −60, −48, −32, −16, 0, 16, 32, 48, 60, 64) are inherited: 77 joins.
The other 118 per helper are newly observed: 826 calls across seven once-only
children, with no initializer, buffer, constructor, setter or patch. This covers
the whole finite grid class, not every real-valued position or every mixer outcome.

| Curve code | Recorded helper / name | New observation IDs | New / inherited |
| --- | --- | --- | --- |
| 0 | `0x101b1a470` / NormalDip / Dipped | MV-301–MV-418 | 118 / 11 |
| 1 | `0x101b1a550` / SlightDip / Intermediate | MV-419–MV-536 | 118 / 11 |
| 2 | `0x101b1a630` / ConstantPower | MV-537–MV-654 | 118 / 11 |
| 3 | `0x101b1a6f0` / Dipless / SlowFade | MV-655–MV-772 | 118 / 11 |
| 4 | `0x101b1a7b0` / SlowCut | MV-773–MV-890 | 118 / 11 |
| 5 | `0x101b1a880` / FastCut | MV-891–MV-1008 | 118 / 11 |
| 6 | `0x101b1a8e0` / Transition | MV-1009–MV-1126 | 118 / 11 |

**Native reference bits and NULL history.** Each new case records an exact
observed `output_bits32` from the approved scalar low32 return. It is a native
reference expectation only for that captured input/function and recorded Linux
math environment. Its `precall_expected` remains NULL: the observation was not
an oracle agreement or an output fitted after a failed prediction. Every new
portable expected value, comparator and candidate grade remains NULL. Neither
MV-047/048's adjacent-float/absolute 10⁻¹² rule nor a general one-ulp assumption
is assigned to these new positions. No portable sign, tolerance or deterministic
public waveform criterion is added. Higher/volatile return lanes remain capture
provenance, not additional results or candidate criteria.

All 826 fresh results are finite: 809 nonzero and 17 raw positive zeros. The full
903-point inventory has 879 nonzero finite values and 24 raw positive zeros; no
negative-zero, Inf or NaN normalization was performed. These are classification
counts of the captured words, not stable/chaotic classes, physical calibration
or a new nonnegative clamp. In particular, revision 6's off-grid Fast Cut negative
reference and its precision limitations remain exact and are not overridden.

**Historical references and preservation.** None of the 77 inherited points
receives a new case ID or fresh receipt. Twenty-eight already match existing
revision 6 case objects exactly and retain those IDs only as navigation; 49 are
other approved historical references. All 252 MV-049–MV-300 objects remain exact,
as do every MV-001–MV-048 row, all 14 other requirement bodies, all prior REQ-014
text and all 80 released objects. This gives 1126 draft case/observation IDs
(300 existing plus 826 new), with 77 references outside that added-ID count.
The old revision 6 count describes its unchanged 300-ID cut. These are input/case
inventory counts, not atomic required-outcome coverage or application grades.

**Table and runtime limits.** The regular grid coincides only nominally with
129 equally spaced coordinates. Calling the seven scalar helpers does not read
or prove a current 129-point runtime table, its constructor, stored words, linear
interpolation, port/current receiver, per-track branch, smoothing ramp, host
audio or visible crossfader. The existing S clauses retain their prior evidence
and conditions; this batch does not promote them or resolve an existing U.
ARM/Apple results, FP environment/exception behavior, actual entry registers,
public lifecycle and calibration remain unproved. Linux `cosf` substitutions
support the captured words only, not a general Apple/ARM error bound.

**Custody and execution scope.** The sole actual review approves seven sequential
once-only children with 826 returned direct helper calls and no historical replay.
Its 18 COMMON recorded baseline identities were compared with each of seven
child-after sets and the final after set; these are not per-child before records.
Used-code counters report only `_cosf` (759 calls total), not every host/library
data access or transitive effect. Raw stdout/stderr were closed and hashed without
explicit raw-FD fsync; JSON bookkeeping fsync and readonly/hash seals do not prove
directory/crash durability or independent OS attestation. These qualifications
are inherited by citation, not re-audited in the owner mapping.

The published mixer-values-v2 remains 80 cases with its exact inputs and criteria.
This analyst proposal adds no release, tolerance, source/receiver proof,
public/native ABI requirement or complete-family claim and performs
no original execution.
Unsupported required behavior remains U and the coverage gate remains OPEN.
