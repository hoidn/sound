---
id: SPEC-MIXER-VALUES
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 2
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
fader (Q-009 area); routing, solo, monitoring and send pre/post; text entry into
value fields; arrow-key and mouse edits; edits after load except the track creation
named in MV-027 and MV-028; documents older than `12.0_12402` and their migration
(for example `TrackSendHolder/Active` before `12.0_12001`); the exact text of error
messages; which UI surface (mixer strip, Info View, automation lane, controller
display) shows which text.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema files or the 376 Live Sets and clips in the 12.4.3 bundle. These were written by Live 12.4d1 or 12.1d1, not by a 12.4.3 save |
| S | Static derivation from the 12.4.3 executable or shipped bytes; not an observed run |
| S/Q-019 | Static derivation that holds only if the stored gain reaches the audio path through the volume curve's round trip (see REQ-011 and [Q-019](../questions.md#q-019-mixer-volume-and-send-values-sent-to-the-engine)) |
| U | Unknown; no expected result, or only a static reading that must not be graded. A PRB ID names the Phase 4 probe that would have settled it. No reference observation is available (ADR 0003), so the clause stays unknown unless the static route named with it settles it |

Only D and S clauses may enter a release. S/Q-019 clauses need Q-019 settled first,
which only a static trace can now do. Every clause about audio output (REQ-011, 013,
014) is static-derived at best. No original-versus-candidate measurement is available
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
  magnitude is below 0.0001 becomes 0.
- **S.** Position → gain: p ≤ 0 gives G[0]; p ≥ 1 gives G[100]; otherwise k = ⌊100p⌋,
  f = 100p − k (f ≤ 2⁻¹⁷ counts as 0 and f ≥ 1 − 2⁻¹⁷ as 1), gain =
  float32(f·G[k+1] + (1 − f)·G[k]). Gain → position is the inverse on the same
  table: below G[0] gives 0, at or above G[100] gives 1, otherwise linear between
  the two neighbouring points, in float32.
- **S.** Consequences: on the volume curve 0 dB is position 0.85 and −6 dB is 0.70;
  on the send curve 0 dB is position 1 and −6 dB is 0.85.
- **U.** That the on-screen fader and controller mappings use these positions (the
  curves are established in the gain conversion, not traced to the UI). No reference
  observation is available (ADR 0003, PRB-S9-04); a static trace from the fader and
  controller code to the curve conversions could settle it (Q-009).

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

- **S.** `Speaker/Manual` is a Boolean, default `true`; its value text is `On` for
  true and `Off` for false.
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

- **S/Q-019.** The gain applied to the track's audio equals the stored volume gain g
  for g in [0.0003162277571, 1.99526238], except that any resulting gain at or below
  float32(0.00032) = 0.0003199999919 (−69.897 dB) is replaced by exactly 0. Hence the
  stored minimum (−70 dB) renders silence, and so does any stored gain in
  (0.0003162277571, 0.0003199999919].
- **S/Q-019.** Gains in (0.0003199999919, 0.0003273407] are audible although their
  text is `-inf dB` (REQ-006).
- **S.** The silence test is applied after the crossfade factor (REQ-014), and the
  resulting gain also scales the pan law (REQ-013).
- **Condition.** Static evidence shows the audio path converts a *fader position* to
  gain with the volume curve (REQ-005) and then applies the floor, for every
  track-mixer variant traced. The conversion of the stored gain into that position
  was not located. If the position is the stored gain mapped by REQ-005's
  gain → position (the reading above), the round trip returns g within float32
  rounding. If the stored gain were used as the position directly, a stored `1`
  would render at +6.0 dB. No reference observation is available (ADR 0003,
  PRB-S9-01); only locating the gain → position conversion statically (Q-019) can
  discriminate.
- **U.** Volume change ramp length and smoothing.

### REQ-MIXER-VALUES-012 — send gain applied to audio

- **U.** Which gain a stored send value applies to the signal sent to a return, whether
  the send curve (REQ-005) and a silence floor are applied, and where (Q-019). No
  reference observation is available (ADR 0003, PRB-S9-01). The static path that
  delivers the send level to the mix applies no curve itself; resolving the part that
  would convert the send is the remaining static route.

### REQ-MIXER-VALUES-013 — pan law

- **S.** For one track, with input channels L, R, output channels L′, R′, track gain
  v (REQ-011), split weight w and θ(x) = (x + 1)·π/4:
  - L′ = v·(w·cos θ(sL) + (1 − w)·max(10⁻⁵, √2·cos θ(p)))·L + v·w·cos θ(sR)·R
  - R′ = v·w·sin θ(sL)·L + v·(w·sin θ(sR) + (1 − w)·max(10⁻⁵, √2·sin θ(p)))·R
  - v = 0 gives silence.

  Here p is the pan, sL and sR the split pans, and w the pan-mode amount.
- **S.** In Stereo mode (w = 0) the pan is a balance control without cross-feed:
  0 dB at centre; at p = −1 the left channel is +3.01 dB and the right channel
  −100 dB (factor 10⁻⁵), not silent; at p = −0.5, +2.32 dB and −5.33 dB. In Split
  Stereo mode (w = 1) each input channel is panned by sin/cos with no lift: default
  splits (−1, +1) pass L and R unchanged; splits (0, 0) send each input to both
  outputs at −3.01 dB.
- **U.** The mapping from pan mode to w and any ramp between them were not traced.
  The static reading is w = 0 for pan mode 0 and w = 1 for pan mode 1; MV-035 to
  MV-037 assume it. No reference observation is available (ADR 0003, PRB-S9-02,
  PRB-S9-03); tracing how the pan-mode amount is derived from `PanMode` could settle
  it.
- **U.** Pan and split-pan ramp lengths, and smoothing when the pan mode changes.

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
- **U.** The shapes of T, including which crossfader end gives full level to A. No
  reference observation is available (ADR 0003, PRB-S9-06); confirming the remaining
  shape routines in disassembly could settle the shapes.

### REQ-MIXER-VALUES-015 — out-of-range and alternative stored values

- **U.** What opening, displaying, rendering and saving do for any value outside the
  domains of REQ-002 to 004 and 009: a volume below 0.0003162277571 (0 and negative
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
- Timing: only the 2 ms crossfade-assign ramp (REQ-014) is derived. Volume and pan
  ramps are unknown. Automation, undo and edits after load are out of scope.
- Interaction: REQ-011 and REQ-013 combine as gain → crossfade factor → silence floor
  → pan matrix.

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
| MV-018 | 008 | P | A `Speaker/Manual` = `false` | A speaker Off | S |
| MV-019 | 009 | P | `LiveSet/CrossfadeCurve/@Value` = `5` | Crossfade curve Fast Cut | S |
| MV-020 | 010 | S | A `Pan/Manual` = `0.6`; open, save | Saved A `Pan/Manual` `0.6000000238` | U: grades only REQ-010's U part |
| MV-021 | 010 | S | A `Send/Manual` = `0.1`; open, save | Saved `0.1000000015` | U: grades only REQ-010's U part |
| MV-022 | 010 | S | Open B0, save | Saved A, R, M, C `Volume`, `Pan`, split, `PanMode`, `CrossFadeState`, `Speaker`, `SoloSink` and `Send/Manual` values have the B0 text (`1`, `0`, `-1`, `1`, `0`, `1`, `true`, `false`, `0.00031622799`); `MidiControllerRange` text is MV-045 | U: grades only REQ-010's U part |
| MV-023 | 005 | C | Volume curve, position → gain | 0 → 0.0003162277571; 0.5 → 0.1995263398 (−14.0 dB); 0.7 → 0.5011872053; 0.85 → 1; 1 → 1.99526238; within 1 float32 ulp | S |
| MV-024 | 005 | C | Send curve, position → gain | 0 → 0.0003162277571; 0.5 → 0.1000001132 (−20.0 dB); 0.85 → 0.5011872053; 1 → 1; within 1 ulp | S |
| MV-025 | 005 | C | Gain → position | Volume: 0.5 → 0.699474, 0.001 → 0.034624; send: 0.1000000015 → 0.5; volume 2 → 1; within 1e-6 | S |
| MV-026 | 002, 005 | C | Default volume and send ranges | gain(0) writes `0.0003162277571`, volume gain(1) `1.99526238`, send gain(1) `1` | S, D |
| MV-027 | 002–004, 008, 009 | P | No user default set or default-track preset installed; open B0, insert one new audio track, save | New mixer: volume `1` with range `0.0003162277571`–`1.99526238`; pan `0`, splits `-1`/`1` with range `-1`–`1`; `PanMode` `0`; `CrossFadeState` `1`; `Speaker` `true`; one send `0.0003162277571`, range `0.0003162277571`–`1`, `EnabledByUser` `true` | U: graded only through the save, REQ-010's U part (defaults S) |
| MV-028 | 003 | U | Open B0, insert a second return track, save | `EnabledByUser` of each new holder in A, R and the new return: unresolved (static: A's new holder `true`) | U |
| MV-029 | 011 | R | TT, A volume `1` | 0.00 dB relative level | S/Q-019 |
| MV-030 | 011 | R | TT, A volume `0.5011872053` | −6.00 dB | S/Q-019 |
| MV-031 | 011 | R | TT, A volume `0.001` | −60.0 dB | S/Q-019 |
| MV-032 | 011 | R | TT, A volume `0.0003162277571` | Silence | S/Q-019 |
| MV-033 | 011 | R, B | TT, A volume `0.0003235936455` (text `-inf dB`) | −69.8 dB, not silent | S/Q-019 |
| MV-034 | 011 | R, B | TT, A volume `0.0003199999919` | Silence | S/Q-019 |
| MV-035 | 013 | R | TT, A pan `-1` | Left +3.01 dB, right −100 dB (not silent) | S; w mapping U |
| MV-036 | 013 | R | TT, A pan `-0.5` | Left +2.32 dB, right −5.33 dB | S; w mapping U |
| MV-037 | 013 | R | TT with the sine on the left channel only; A pan mode `1`, splits `0`/`0` | Left and right outputs each −3.01 dB | S; w mapping U |
| MV-038 | 014 | R | TT, A assign None; crossfader `-1`, `0`, `1` in three renders | Same level in all three | S |
| MV-039 | 014 | R | TT, renders with A assign A at crossfader c and with A assign B at −c, for c in {−1, −0.5, 0, 0.5} | Pairwise equal levels; absolute levels unresolved | S; shapes U |
| MV-040 | 012 | U | TT, A send `0.5011872053`, R volume `1`, return routed to M | Return level unresolved | U |
| MV-041 | 015 | U | A `Volume/Manual` = `2`; open, display, render, save | Unresolved (static reading: opens; text `6.021 dB`) | U |
| MV-042 | 015 | U | A `Volume/Manual` = `0`; separately `-1` | Unresolved (static reading: opens; text `-inf dB`) | U |
| MV-043 | 015 | U | A `Pan/Manual` = `1.5` | Unresolved | U |
| MV-044 | 015 | U | A `CrossFadeState/Manual` = `3`; separately `PanMode` `2` | Unresolved | U |
| MV-045 | 015 | U | Open B0 unchanged, save | Saved `MidiControllerRange` texts unresolved (static reading: `0.00031622799`/`1.99526203` kept) | U |
| MV-046 | 007 | B | A `Pan/Manual` = `0.33` | `17R` (float32 value × 50 = 16.50000066, not a tie) | S |

Comparators: "opens" is judged by whether the set finishes loading. Text comparisons
are exact strings, against an observation in the forms of REQ-006 to 008 (with ` dB`
and `-inf dB`; with `C`, `L` or `R`; `On` or `Off`). An observation in another form,
for example the digits without the unit, is inconclusive, not a mismatch. Saved
values are exact attribute text. C cases compare numbers within the stated tolerance.
R cases follow the TT comparator. Cases labelled U, and the U parts named in the
label column, must not be graded as passes. Cancellation and teardown kinds are
omitted: loading, displaying and saving these values has no cancellable step in this
scope. Malformed text (a `Manual` that is not plain decimal
text, other Boolean or code text) has no case and no expectation: the reading is
assumed for plain decimal text only (see the reading assumption above).

Count: 46 cases. 24 are static or documented (MV-001–019, MV-023–026, MV-046), 11
audio renders with static expectations only (MV-029–039, 6 of them conditional on
Q-019), and 11 ungraded (MV-020–022 and MV-027, which grade only REQ-010's U part;
MV-028; MV-040–045).

## Open questions

[Q-019](../questions.md#q-019-mixer-volume-and-send-values-sent-to-the-engine) holds:
the conversion of a stored volume into the fader position the audio path uses
(REQ-011); the send gain path (REQ-012); out-of-range values (REQ-015); `SoloSink`
(REQ-008); which surface shows which text (REQ-006, 007). The
[probe batch](../../analysis/ableton-live-12.4.3/r2/s9-mixer-v1/probe-batch.json)
PRB-S9-01 to 08 records what observation would have settled; under ADR 0003 it will
not run. PRB-S9-08 (automation interpolation) belongs to the automation spec. The
records map to cases as follows: PRB-S9-01, 02, 03 and 06 to MV-029–039; PRB-S9-04 to
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
| 005 | Table `0x101ac2bf8` ✓, gain table `0x101ac2ad8`, position → gain `0x101ac3498` ✓, gain → position `0x101ac353c`/`0x101ac3c94` ✓, mode ranges `0x1058486a8`/`0x1058486c4`; identity bypass flag `DAT_106f7e914` set only by scope helpers `0x101ac3d74` (runtime use unknown); tables regenerated in D8 from `derive_curves.py` `db_table` | S; UI binding U |
| 006 | `0x102183bf4` ✓ (gain → dB, ≤ 0 → −140), `0x102183abc` ✓ (floor −70, 3/1 decimals, suffix), `0x101437334` ✓, `0x101431c6c` ✓; formatter `(3,1,1,1)` ✓ `0x10271c138`; second slot `0x1014374b4` (no `-inf`, no unit; pseudocode) | S |
| 007 | `0x10143a290` ✓ s9-0002: double compares with ±0.01 (`0x3f847ae147ae147b`), multiply by ±50 in double, wrapper `0x101431c60` ✓ d8-0002 sets max = min = 0 decimals; same formatter singleton `0x101439ec4` for pan and both splits (`0x10271c734`, all three call sites ✓ RC §4) | S; ties U |
| 008 | `0x1026ec1cc` ✓ s9-0004 (bool init writes 1 to value and Manual). On/Off text: `0x10271b660.c` lines 284–287 (s9-0001) pass the text object from `0x10143b884` (corpus record kept; vtable `0x106670bc8`) to `0x1026ec1cc`; `image-reads.txt` gives that vtable's `+0x28` as `0x10143ba28`, which returns "Off" for 0.0 and "On" otherwise (✓ RC §2: call site `0x10271bcb0`–`0x10271bcc4`, `0x10143ba28`–`0x10143ba40`, strings `0x105af67ac`, `0x105bafc64`). "Solo-Cue" with `SoloPrehearSinkController` | S; SoloSink U |
| 009 | Constructor call `0x1026ef060(xf, 1, ["A","None","B"], …)` at `0x10271bf38` ✓ s9-0001; wrapper `0x1026ef060` passes arguments through (pseudocode); `0x1026ef0dc` ✓ d8-0002 passes index x1 to `0x101567bfc` for value and Manual; curve names `0x102672204`, helpers `0x101aed36c` ✓. Curve binding (✓ RC §3): the set constructor `0x102672448` (C1 record, kept in the review's `corpus-excerpts-review.jsonl`) loads member `[this+0x1f0]`, calls the name list at `0x1026740d8` and the enum init `0x101567bfc` with index 2 at `0x1026740f8`; the LiveSet registry call at `0x10266e148`–`0x10266e174` names the member at `0x1e8` `mpCrossfadeCurve` (+8 convention). Census: `CrossfadeCurve` in the 376 documents of `inputs-documents.tsv`, 2 in 375 and 6 in 1 (recounted 2026-10-18) | S (default index upgraded from inferred) + D |
| 010 | N1 writer rule ([transport-state native](../research/transport-state-native.md#writer-number-format)); `static-survey.json` `lexical_rule_match` | S + D |
| 011 | Consumers of the volume port output, `0x1027200f8` ✓ d8-0001: when an integer read from the track (`0x10248256c(track,1)`, slot 0x370) is ≥ 0, port +0x68 `Out` → crossfade unit +0x28 `Volume` (`0x1027202b8`–`0x1027202e8`), unit `Volume` → track-out +0x20 (`0x102720300`); otherwise `0x10246a3d4(+0xa8, 1)` at `0x102720378` sets an `AConvertLevel` (`0x10246a1a4` ✓, same constructor as `SNewCompound<AConvertLevel>`) to curve 1 and `Out` → converter → track-out `Volume` (`0x102720394`–`0x1027203c4`). `OCrossFadeVolumeProcessor` `0x101aede40` ✓ applies `0x101ac3bac(x,1)` then `≤ 0x39a7c5ac → 0`; `OConvertLevelRampEventProcessor::OnIn` `0x101aee660` ✓ d8-0002 and `OConvertLevelProcessor::OnIn` `0x101aee5e8` ✓ apply curve then the same floor. Port binding: volume port +0x68 and pan port +0x50 are one class (`0x1024f5674`, vtable `0x1067c7a48`) bound to timeables +0x318 and +0x2d0 by slot 0xb8 (`0x102720bd4`–`0x102720be8` ✓); bind `0x1024f5c08` ✓ d8-0001 wires a sub-unit (`0x1024f4b08` ✓: `TimeablePlayer`, `ModulationPlayer`, `Modulator` = `FloatModulatorProcessor`, `Out`); combiner `0x101b09ac8` ✓ is linear with a clamp. Default envelope event = constructor default value in the stored (gain) domain, `0x1026f0d84` (pseudocode). Gain → position conversion site not found | S/Q-019 |
| 012 | `OTrackOutVolumeProcessor::OnSend<k>` `0x101b191d4` → `0x101b18bb4` → `0x101b10efc` (pseudocode, no curve); send unit `0x1025c36ec` ✓ d8-0001 is built from a node graph cached per class descriptor (`0x1025d2264`), whose node list was not resolved; an `AConvertLevel` node factory with a configurable curve exists (`0x1025d2aa8`, no direct caller) | U |
| 013 | Matrix `0x101b3b95c` ✓ s9-0002; ramp inputs `0x101afb494` ✓. Input names, D8: `0x101b10fe4` ✓ d8-0002 registers `PanModeAmount`, `Pan`, `StereoSplitPanL`, `StereoSplitPanR`, `Volume` with handler pointers `0x1065423f8`/`400`/`408`/`410`/`4a0` → `OnPanRampEvent<0..3>` `0x101b18834`/`880`/`8cc`/`918` and `OnVolume` `0x101b18964` (pointer reads). Index meaning upgraded from inferred (port order) to static; `PanModeAmount` from `PanMode` not traced | S; w mapping inferred |
| 014 | `0x101aedff0` ✓ (target 1 − state, 0.002 s ramp), `0x101aee124` ✓ (factor off when target 0), `0x101aede40` ✓ (x = (c·s′ + 1)·64 into a 129-point table; byte table `0x105bb3a43`), Dipped `0x101aee8b8` ✓; other shapes pseudocode | S; shapes U |
| 015 | Loader direct store (N1 rule, not re-traced for mixer classes; schema `12.0_12402` types `Tempo` as `TimeableSongTempo` and the mixer floats as `TimeableFloat`); `rare_value_docs` (Driver Error Compensation, Playing Software Instruments, Recording Audio, 8-Track Template, Podcast & Radio) | U |

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

Before the 2026-10-18 review, revision 1 proposed a first candidate with MV-001–026.
Those cases exercise REQ-001 to 010; its list (001, 002, 003, 004, 006, 007, 009 and
010) omitted REQ-005 (MV-023–026) and REQ-008 (MV-018). The release took a narrower
scope, below. REQ-005 is needed by any renderer. REQ-010's save cases stay ungraded,
and REQ-011, 013 and 014 stay out: no reference observation or measurement is
available (ADR 0003), and REQ-011 also needs Q-019.

Released 2026-10-18: [mixer-values-v1](../../handoff/mixer-values-v1/README.md), 37 cases, approved with corrections by a separate review agent (partial REQ-001 to 004, 006 to 009 only; 005, 010 to 015 unreleased). The review findings to apply in the next revision are on the [handoff plan](mixer-values-handoff-plan.md#review-outcome). Revision 2 applies those findings; the release is unchanged and still pins revision 1. Draft clauses outside the release's partial scope, listed per requirement in the plan's [scope table](mixer-values-handoff-plan.md#scope), are broader than mixer-values-v1.
