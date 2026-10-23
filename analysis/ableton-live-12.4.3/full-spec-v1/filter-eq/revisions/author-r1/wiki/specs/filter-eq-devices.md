---
id: SPEC-FILTER-EQ-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Filter and equalizer devices

This page owns partial behavioral contracts for `SURF-DEVICE-AUTO-FILTER`,
`SURF-DEVICE-CHANNEL-EQ`, `SURF-DEVICE-EQ-EIGHT` and `SURF-DEVICE-EQ-THREE`.
The [research packet](../research/filter-eq-devices.md) owns source identity,
package observations and evidence limits. This is an analyst draft, not a release,
complete device specification or candidate compatibility result.

**D12 exact-target U:** D12 is the captured current official Version 12 manual;
its behavioral clauses have no exact 12.4.3 applicability proof. Dpkg grades only
retained target-package files/strings. A schema field or saved value cannot prove
a DSP law, runtime default, mode mapping, automation schedule or live persistence.
U means no oracle and cannot pass. There are no original application/function or
candidate executions in this packet; all application scenarios are unexecuted.

[Device chains and racks](device-racks.md) own generic insertion, removal, order,
activation and preset actions. [Automation envelopes](automation-envelopes.md)
own their stated representation/evaluation scope, not these devices’ live
scheduling. [Set structure](live-set-structure.md) and [ALS containers](als-container.md)
own their narrower storage scopes; they do not establish these devices’ round trips.
[Mix graph](mix-graph.md) owns track routing; [mixer values](mixer-values.md) do not
supply device gain laws. Set musical context does not establish filter LFO reset or tonal-frequency semantics.

Inputs are the audio at the device’s chain position, controls, mode/state changes,
and Auto Filter’s selected detector source. Outputs are processed/monitored audio
and documented displays. Full stereo matrices, processing order, coefficient
precision, frequency-dependent transfer, latency, smoothing, oversampling filters,
random distributions, overload behavior and tolerances remain U unless a clause
explicitly documents a narrower relation. Control values used in probes are
chosen setups, not factory defaults or proven transparent neutral states.
No device-specific asynchronous cancel operation is documented: Escape/menu/hold
cancellation is tested as a concrete U state transition. Permissions, keyboard
focus/accessibility, Arrangement/Session automation ownership and engine failure
remain shared host interaction gaps; none is silently excluded from full coverage.

## Requirements

## Auto Filter

### REQ-DEVICE-AF-001 — frequency-selective processing

**D12.** Incoming device-chain audio is filtered by the selected filter. LFO and envelope follower can modulate the filtering; the envelope follower can use internal or external sidechain audio. Exact internal detector tap is not established: the opening summary says filtered signal, whereas the sidechain section says input source.

Evidence: `auto-filter:B02,B53`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-002 — filter selection

**D12.** The documented Filter Type chooser offers Low-pass, High-pass, Band-pass, Notch, Morph, DJ, Comb, Resampling, Notch + LP and Vowel. Numeric enum mapping and mode-change state retention are U.

Evidence: `auto-filter:B04`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-003 — low/high/band/notch slope choices

**D12.** Low-pass attenuates above cutoff; High-pass attenuates below; Band-pass passes a range around cutoff; Notch attenuates a narrow range. Each offers 12 and 24 dB slope choices. These labels do not establish measured slope at cutoff, Q law, pole locations or coefficients.

Evidence: `auto-filter:B05–B08`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-004 — Morph filter slopes

**D12.** Morph traverses low-pass through band-pass to high-pass with increasing Morph. Its documented slope options are 6, 12, 24 and 48 dB. Transition law and endpoint transfer functions are U.

Evidence: `auto-filter:B09,B18`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-005 — DJ bipolar control

**D12.** DJ uses a bipolar Control: above zero removes low frequencies; below zero removes high frequencies. Emphasis grows as values approach −100%/+100%. The description does not establish a transparent 0% transfer function or a numeric resonance law.

Evidence: `auto-filter:B10,B15`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-006 — Comb, Resampling, Vowel and Notch + LP

**D12.** Comb produces repeated peaks/notches. Resampling continuously resamples at a rate determined by cutoff, reducing high-frequency content with aliasing. Vowel emphasizes vocal formants. Notch + LP combines a notch with low-pass rolloff, with 12/24 dB choices. Delay lengths, sampling ratios, formant tables and coefficients are U.

Evidence: `auto-filter:B11–B14`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-007 — frequency and vowel controls

**D12.** Freq sets cutoff except DJ, where Control replaces Freq, and Vowel, where Pitch shifts formants in semitones. For Vowel, Formant replaces Res and traverses a, e, i, o, u. No numeric pitch/formant domain or map is established.

Evidence: `auto-filter:B15–B16`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-008 — resonance availability

**D12.** Res emphasizes cutoff for applicable filters. Res has no effect in Resampling and is grayed out. Exact resonance scale, instability boundary and self-oscillation are U.

Evidence: `auto-filter:B16`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-009 — filter Morph variants

**D12.** Morph, Comb, Notch + LP and Vowel have Morph controls. Comb moves from peaks at low Morph toward notches at high Morph at cutoff multiples. In Notch + LP the notch approaches cutoff as Morph rises and reaches cutoff at 100%. Vowel Morph increasingly normalizes formant gain. Exact frequency/gain interpolation is U.

Evidence: `auto-filter:B17–B21`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-010 — filter display and dragging

**D12.** The display shows selected filter curve, modulated left/right curves and output spectrum. Dragging its handle changes Freq and Res, or Pitch and Formant for Vowel. Pixel mapping, display FFT and other modes’ handle mapping are U.

Evidence: `auto-filter:B23`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-011 — modulation-section selection

**D12.** LFO and Envelope sections below the display expose their section parameters at the display bottom when selected. Selection alone supplies no documented reset or sound-change rule.

Evidence: `auto-filter:B24`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-012 — stereo LFO modes

**D12.** Phase keeps L/R LFO frequency equal with offset in degrees: 180° places one peak at the other minimum. Spin detunes L/R rates by its percentage. Phase 0° or Spin 0% modulates channels identically. Random-waveform caveats belong to REQ-DEVICE-AF-016.

Evidence: `auto-filter:B26–B27`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-013 — phase-offset time-mode dependency

**D12.** LFO Phase Offset shifts both waveform starting points only for tempo-synced beat divisions or sixteenth-note time modes. Its parameter has no effect in the other documented time modes. Transport-start reset, phase origin and seek behavior are U.

Evidence: `auto-filter:B28`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-014 — LFO quantization

**D12.** Steps divides an LFO cycle into the number of intervals selected by LFO Steps. S&H quantizes LFOs to the LFO S&H beat-time setting. Exact sampling edge, interpolation and legal divisions are U.

Evidence: `auto-filter:B29`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-015 — LFO amount and time modes

**D12.** LFO Amt controls modulation depth and can combine with envelope modulation. Rate is expressed in Hz, seconds, synced beat divisions or sixteenth-note values according to Mode; Time mode labels the control Time. Rate domains, tempo-change smoothing and amount scaling are U.

Evidence: `auto-filter:B30–B31`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-016 — LFO waveform controls

**D12.** Wave offers Sine, Triangle, Saw, Square, Ramp Up, Ramp Down, Wander and S&H. S&H generates random positive and negative modulation. Wander and S&H disable Spin with a gray control. LFO Morph transforms waveform shape; for S&H it is replaced by Smooth. Random distributions, seeds, repeatability and waveform equations are U.

Evidence: `auto-filter:B32–B33`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-017 — envelope attack and release

**D12.** Envelope modulates filter frequency. Lower Attack responds faster to rising input; higher Attack integrates changes more slowly. Lower Release responds faster to falling level; higher Release extends decay. No detector transfer, time-constant definition or sum/clamp law with LFO is established.

Evidence: `auto-filter:B35–B36,B38`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-018 — envelope Hold

**D12.** With Envelope Hold on the entire attack phase completes before release starts. Exact attack-completion criterion, retrigger and release interruption are U.

Evidence: `auto-filter:B37`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-019 — envelope sample-and-hold

**D12.** Envelope S&H enables envelope quantization at the beat-time value selected with Envelope S&H Rate. Exact clock edge and off-state phase retention are U.

Evidence: `auto-filter:B39`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-020 — envelope polarity/depth

**D12.** Envelope control determines direction and extent of modulation. Numeric endpoints and polarity-to-cutoff map for each filter are U.

Evidence: `auto-filter:B40`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-021 — input Drive

**D12.** Drive applies drive before filtering. At 0.0% the drive contribution is described as unaltered; increasing Drive produces progressively greater distortion/saturation. This does not prove whole-device identity, a transfer curve, headroom or oversampling.

Evidence: `auto-filter:B42`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-022 — circuit selection and availability

**D12.** Filter Circuit offers SVF, DFM, MS2 and PRD and affects only Low-pass, High-pass, Band-pass, Notch and Morph. SVF is described as clean with distortion possible above zero Drive; DFM has distortion feedback; MS2 soft-clips resonance; PRD has no explicit resonance limiting. Architectural descriptions are documentary characterizations, not recovered algorithms.

Evidence: `auto-filter:B43–B47`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-023 — output, Clip and Dry/Wet

**D12.** Clip soft-clips effect output and its LED flashes on clipping. Output sets processed-signal level; Dry/Wet balances processed and unprocessed audio. Exact threshold, clipping function, gain range, mix law and stage ordering beyond named input Drive/output clipping remain U.

Evidence: `auto-filter:B49–B51`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-024 — external sidechain routing

**D12.** The Sidechain Section toggle exposes controls; External enables external triggering. External Source selects a signal, and External Tapping Point offers Pre FX, Post FX or Post Mixer. Missing/deleted source, routing cycles, compensation and device off-state are U.

Evidence: `auto-filter:B53–B54`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-025 — sidechain mix and gain

**D12.** Mix 100% follows external sidechain exclusively; Mix 0% follows internal sidechain only. SC Gain changes external detector input level, not source-track volume. Mix interpolation, internal tap and detector calibration are U.

Evidence: `auto-filter:B55–B56`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-026 — sidechain Listen

**D12.** Sidechain Listen bypasses Auto Filter output and exposes sidechain input for monitoring. Exact monitored stage, stereo/mono relationship, gain and switching ramp are U.

Evidence: `auto-filter:B57`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-027 — sidechain filtering

**D12.** SC Filter enables frequency-selective detection. Sidechain Filter Frequency sets cutoff; low-shelf, peak and high-shelf use signed gain for boost/cut, with shelf response leveling at gain rather than continued rolloff. Sidechain Filter Q controls bandwidth. The complete Type enum is U: B59 lists band-pass while B63 instead explains Notch. Neither a merged enum nor a correction is inferred.

Evidence: `auto-filter:B58–B63`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-028 — mono sidechain

**D12.** By default the sidechain is converted to mono, giving identical L/R envelope modulation. The Mono Sidechain context-menu option disables that conversion. Off-state stereo detector mapping, summing coefficients and interactions with Listen/LFO are U.

Evidence: `auto-filter:B65`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-029 — retained current-device state

**Dpkg.** The retained named Auto Filter default has an AutoFilter2 root and the schema declares its filter, LFO, envelope, sidechain and output vocabulary. Exact file observations are retained in package-values.json. Filename default does not prove a runtime constructor default; HiQuality naming does not prove oversampling.

Evidence: `PKG-SCHEMA:AutoFilter2; PKG-AUTO-FILTER`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-AF-030 — unresolved lifecycle and exact audio

**U.** Every D12 clause remains exact-12.4.3 U. Automation scheduling, transport restart/seek, undo/redo, edit cancellation, invalid fields/ranges, saved-state migration, routing source failure, sample-rate/block-size changes, deletion and teardown have no outcome oracle. Numerical response, modulation kernels, stochastic laws, smoothing, latency, clipping thresholds and tolerances are U. Legacy AutoFilter behavior is a separate unmapped obligation; the current manual is not its behavioral source.

Evidence: `U`; [exact retained locators](#analysis-only-evidence).

Acceptance scenarios are defined completely in [cases.json](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/cases.json); every row below retains its setup/action and documented outcome or ungraded unknown. Documentary comparisons grade only named controls, settings or relations, never sample/pixel/timing equivalence.

| Case | Requirement suffixes | Kind and setup/action | Expected outcome | Evidence |
| --- | --- | --- | --- | --- |
| AF-C001 | 001, 002 | positive: Open Filter Type chooser and enumerate its entries. | The ten names in REQ-DEVICE-AF-002 are available. | D12: `auto-filter:B04` |
| AF-C002 | 003 | positive/boundary: SIG-MULTI; choose Low-pass, cutoff 1000 Hz; inspect 12 and 24 dB choices. | Both slope settings exist; documented relation: above-cutoff content is attenuated. Numeric levels/width U. | D12: `auto-filter:B05` |
| AF-C003 | 003 | positive/boundary: SIG-MULTI; choose High-pass, cutoff 1000 Hz; inspect 12 and 24 dB choices. | Both slope settings exist; documented relation: below-cutoff content is attenuated. Numeric levels/width U. | D12: `auto-filter:B06` |
| AF-C004 | 003 | positive/boundary: SIG-MULTI; choose Band-pass, cutoff 1000 Hz; inspect 12 and 24 dB choices. | Both slope settings exist; documented relation: a range around cutoff passes while lower/higher content attenuates. Numeric levels/width U. | D12: `auto-filter:B07` |
| AF-C005 | 003 | positive/boundary: SIG-MULTI; choose Notch, cutoff 1000 Hz; inspect 12 and 24 dB choices. | Both slope settings exist; documented relation: a narrow range attenuates while surrounding content is largely unaffected. Numeric levels/width U. | D12: `auto-filter:B08` |
| AF-C006 | 004 | positive/boundary: Select Morph; inspect slopes 6/12/24/48 dB and sweep Morph low, middle, high. | Four documented slope choices; low-pass, band-pass, high-pass progression. Exact positions/response U. | D12: `auto-filter:B09,B18` |
| AF-C007 | 005 | boundary: DJ on SIG-MULTI; set Control −100%, 0%, +100%. | Bipolar endpoints exist; negative values remove highs, positive remove lows. Zero transparency and emphasis magnitudes U. | D12: `auto-filter:B10,B15` |
| AF-C008 | 006, 009 | positive: Comb; cutoff 500 Hz; compare low and high Morph on a swept test tone. | Peak character at low Morph changes toward notch character at high Morph at cutoff multiples. Exact frequencies/strength U. | D12: `auto-filter:B11,B19` |
| AF-C009 | 006, 008 | negative: Resampling; SIG-MULTI; lower cutoff, inspect Res and attempt to change it. | Res is gray and has no effect; Resampling reduces high-frequency content by its documented resampling behavior, but no numeric aliasing or output oracle is supplied. | D12: `auto-filter:B13,B16` |
| AF-C010 | 006, 007 | positive: Select Vowel after Low-pass; inspect frequency and resonance locations; change Pitch and Formant. | Pitch replaces Freq; Formant replaces Res; Pitch shifts formants in semitones and Formant traverses vowels. Numeric mapping U. | D12: `auto-filter:B15,B16` |
| AF-C011 | 006, 009 | boundary: Notch + LP at cutoff 1000 Hz; increase Morph to 100%. | Notch reaches low-pass cutoff at 100%; 12/24 dB slope choices exist for Notch + LP. Measured gain/width U. | D12: `auto-filter:B14,B20` |
| AF-C012 | 009 | positive: Vowel on SIG-MULTI; sweep Morph upward. | Formant gains become increasingly normalized; exact normalization U. | D12: `auto-filter:B21` |
| AF-C013 | 010 | positive: Low-pass; drag the display handle horizontally/vertically; repeat Vowel. | First edits Freq/Res, second Pitch/Formant. Selected/modulated L/R curves and output spectrum are displayed. | D12: `auto-filter:B23` |
| AF-C014 | 011 | positive: Select LFO section then Envelope section. | Bottom-of-display parameters correspond to selected section; no reset behavior graded. | D12: `auto-filter:B24` |
| AF-C015 | 012 | boundary: Deterministic Sine LFO, amount nonzero, Phase mode; inspect 0° and 180°. | 0° gives identical channel modulation; 180° places one peak at the other minimum. Numeric modulation/output tolerance U. | D12: `auto-filter:B26,B27` |
| AF-C016 | 012 | boundary: Sine LFO, Spin mode, Spin 0% then nonzero. | 0% gives identical channel modulation; nonzero detunes channel rates. Detune formula U. | D12: `auto-filter:B27` |
| AF-C017 | 013 | negative: Sine LFO in Hz then Time mode; move Phase Offset. | Phase Offset has no effect in these two modes; audio tolerance U. | D12: `auto-filter:B28` |
| AF-C018 | 013 | positive: Sine LFO in synced beat divisions then sixteenth-note mode; change Phase Offset. | Starting point of both LFO channels shifts; transport origin U. | D12: `auto-filter:B28` |
| AF-C019 | 014 | positive: Sine LFO with Steps selected; set Steps=8. | LFO cycle is divided into eight update intervals; edge phase U. | D12: `auto-filter:B29` |
| AF-C020 | 014 | positive: LFO quantization S&H; select available quarter-note beat-time setting at Set tempo 120 BPM. | LFO is quantized to that selected beat-time; exact edge/transport coupling U. | D12: `auto-filter:B29` |
| AF-C021 | 015 | positive: Switch time modes through Hz, Time, synced beat, sixteenth values; adjust Amt with Envelope nonzero. | Rate units follow mode and Time label appears in Time mode; LFO and envelope can coexist. Numeric composition U. | D12: `auto-filter:B30,B31` |
| AF-C022 | 016 | positive: Enumerate Wave choices. | Sine, Triangle, Saw, Square, Ramp Up, Ramp Down, Wander and S&H are available. | D12: `auto-filter:B32` |
| AF-C023 | 016 | negative: Select Wander; attempt Spin editing. | Spin is grayed out and does not affect sound. | D12: `auto-filter:B32` |
| AF-C024 | 016 | negative: Select S&H; attempt Spin editing. | Spin is grayed out and does not affect sound. | D12: `auto-filter:B32` |
| AF-C025 | 016 | positive: Select Sine and inspect Morph, then select S&H and inspect same area. | S&H replaces Morph with Smooth; S&H supplies random positive/negative modulation, with no distribution oracle. | D12: `auto-filter:B32,B33` |
| AF-C026 | 017 | positive: SIG-PULSE; compare displayed Attack low versus high, then Release low versus high. | Higher Attack responds more gradually to rises; higher Release decays longer. Numeric durations U. | D12: `auto-filter:B35,B36,B38` |
| AF-C027 | 018 | positive: SIG-PULSE with pulse shorter than chosen Attack; enable Hold. | Entire attack completes before release. Attack endpoint timing U. | D12: `auto-filter:B37` |
| AF-C028 | 019 | positive: Enable Envelope S&H and select available eighth-note setting at 120 BPM. | Envelope modulation is quantized to selected beat-time; phase/grid edge U. | D12: `auto-filter:B39` |
| AF-C029 | 020 | positive: Envelope enabled on SIG-PULSE; move signed Envelope control through opposite sides. | Control adjusts modulation direction and extent; cutoff mapping U. | D12: `auto-filter:B40` |
| AF-C030 | 021 | boundary: SVF Low-pass; Drive 0.0% then increased Drive; fixed input. | Zero Drive adds no documented drive alteration; higher values add progressively more distortion/saturation. Whole-filter identity U. | D12: `auto-filter:B42,B44` |
| AF-C031 | 022 | positive: For Low-pass, High-pass, Band-pass, Notch, Morph inspect Circuit choices. | SVF, DFM, MS2 and PRD available and have effect in these five filter types. Numeric sound U. | D12: `auto-filter:B43–B47` |
| AF-C032 | 022 | negative: For DJ, Comb, Resampling, Notch + LP and Vowel change Circuit if possible. | Circuit choice has no effect for these five filters; disablement appearance is not specified. | D12: `auto-filter:B43` |
| AF-C033 | 023 | positive: High-resonance filtered SIG-MULTI; enable Clip and raise level until clipping is indicated. | Clip applies output soft clipping; LED flashes on clipping. Threshold/waveform U. | D12: `auto-filter:B49` |
| AF-C034 | 023 | positive: Move Output then Dry/Wet while SIG-MULTI streams. | Output adjusts processed level; Dry/Wet balances processed/unprocessed signal. Numeric endpoints/mix law U. | D12: `auto-filter:B50,B51` |
| AF-C035 | 024 | positive: Expose Sidechain Section, enable External, select an audio source and enumerate tapping points. | Pre FX, Post FX, Post Mixer are offered for external source. Routing latency/cycles U. | D12: `auto-filter:B53,B54` |
| AF-C036 | 025 | boundary: Internal SIG-PULSE, external continuous SIG-440; compare Mix 0% and 100%. | At 0% envelope uses internal source only; at 100% external only. Exact internal tap and detector transfer U. | D12: `auto-filter:B55` |
| AF-C037 | 025 | negative: External selected, source-track fader fixed; vary SC Gain. | External detector input level changes without changing source-track volume. Effect-output amplitude can change through modulation. | D12: `auto-filter:B56` |
| AF-C038 | 026 | positive: Internal audio SIG-MULTI, external SIG-440; enable Listen. | Sidechain input becomes audible in place of Auto Filter output. Exact monitored tap U. | D12: `auto-filter:B57` |
| AF-C039 | 027 | positive: Enable SC Filter; select low-shelf, peak, high-shelf in turn; vary signed gain. | Detector filtering boosts/cuts corresponding ranges; shelves level at gain rather than continuous rolloff. Transfer curves U. | D12: `auto-filter:B58–B62` |
| AF-C040 | 028 | boundary: Stereo sidechain with dissimilar L/R pulses; Mono Sidechain enabled; LFO amount zero. | Envelope modulation is identical across L/R. Summing law U. | D12: `auto-filter:B65` |
| AF-C041 | 028 | positive: Open device context menu and disable Mono Sidechain. | Option permits disabling mono conversion; resulting stereo detector mapping ungraded. | D12: `auto-filter:B65` |
| AF-C042 | 029 | file observation: Decode retained package/Auto Filter/Auto Filter.adv using gzip/XML and read /Ableton/AutoFilter2. | Exact stored strings: {"DryWet/Manual": "1", "Envelope_HoldOn/Manual": "true", "Filter_Frequency/Manual": "9999.99805", "HiQuality": "false"}. No display-unit/enum/DSP inference. | Dpkg: `PKG-AUTO-FILTER` |
| AF-C043 | 030 | source ambiguity: SIG-PULSE main input; compare inferred prefilter/postfilter detector hypotheses while moving cutoff from 200 to 5000 Hz; LFO amount zero. Record envelope trace and output. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C044 | 030 | enum discrepancy: Open Sidechain Filter Type chooser and record all labels/ordering; test whether Band-pass and/or Notch exists; correlate saved enum only after observing selection. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C045 | 030 | legacy applicability: Decode retained Auto Filter Legacy preset; open only under a future authorized reference route. Record separate control list, saved root, sound and conversion when replacing with current Auto Filter. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C046 | 030 | automation: At 120 BPM automate Filter Frequency 200→5000 Hz, Filter Type Low-pass→DJ, LFO Rate and Dry/Wet; manually override then re-enable. Capture control/output changes at bar boundary. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C047 | 030 | timing: Sine LFO 1/4 beat, Phase Offset 90°; Start/Stop/continue/seek to bar 3, change tempo 120→90 BPM; repeat Hz/Time modes and Steps/S&H with eight steps/eighth-note setting. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C048 | 030 | randomness: Wander then S&H wave, Spin 0, capture five eight-bar passes across Stop/Start and save/reopen; record seed/state/repeatability without expected distribution. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C049 | 030 | boundary: Freq text 0, −1, 100000 Hz; Morph below/above control range; external/internal Mix midpoint. Record clamping, rejection and nonlinear mapping. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C050 | 030 | malformed: On separate copies of AutoFilter2 preset remove Filter_Type, duplicate Filter_Frequency, set Filter_Type=999 and Envelope_Attack=-1; record error/normalization and original-file preservation. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C051 | 030 | cancel: Begin Freq numeric edit 1000→2000 then Escape; open Type and sidechain-source menus then Escape. Record control, sound and undo history. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C052 | 030 | undo: Change Low-pass to Vowel, edit Pitch/Formant, enable Sidechain Listen; Undo three actions then Redo. Record hidden filter values, monitor state and output. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C053 | 030 | persistence: Save/reopen Set and device preset with DJ Control −50%, S&H waveform/Smooth, envelope Hold/S&H, external Post FX source, Mono Sidechain off, Clip on and Dry/Wet 35%; compare all visible/hidden values and envelope/LFO phase. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C054 | 030 | error: While externally sidechained, delete selected source track; disconnect its input; attempt self/feedback routing. Record routing display, fallback, output, error and undo. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C055 | 030 | teardown: During sidechain Listen and held envelope, delete Auto Filter, undo deletion, disable/re-enable engine and close Set. Record routed audio, resource release and restored state. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C056 | 030 | sample-rate: Sweep high cutoff with resonance/Drive at fixed displayed settings at 44.1/48/96 kHz and blocks 64/512; toggle Clip. Capture response, aliasing, latency, smoothing and headroom. | Unknown; no oracle, record without grading. | U: `U` |
| AF-C057 | 030 | detector composition: Stereo pulses offset by 250 ms; Mono Sidechain off, Spin nonzero and Envelope enabled; compare modulation and Listen while varying SC Gain, SC filter and Mix 0/50/100%. Record monitor tap and summing/order. | Unknown; no oracle, record without grading. | U: `U` |

## Channel EQ

### REQ-DEVICE-CEQ-001 — three-band signal processing

**D12.** Channel EQ is a three-band audio equalizer. Its host chain position determines incoming signal; insertion/routing/preset lifecycle belongs to the rack/host owner. No processing order or channel-coupling matrix is established.

Evidence: `channel-eq:B02,B10–B12`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-CEQ-002 — HP 80 Hz switch

**D12.** HP 80 Hz toggles a high-pass filter. Its label supplies the documented nominal frequency, not a measured −3 dB location, order, slope or coefficient set.

Evidence: `channel-eq:B03`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-CEQ-003 — adaptive low shelf

**D12.** Low controls a low shelf tuned to 100 Hz over −15 to +15 dB; its curve changes dynamically relative to applied gain. Q-versus-gain law, gain normalization and meaning of tuning are U.

Evidence: `channel-eq:B04`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-CEQ-004 — sweepable mid peak

**D12.** Mid gain ranges from −12 to +12 dB. Its frequency slider sets peak center over 120 Hz–7.5 kHz. Bandwidth and exact response around center are U.

Evidence: `channel-eq:B05`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-CEQ-005 — asymmetric High control

**D12.** Positive High boosts a high shelf up to +15 dB. Negative High combines shelf attenuation with low-pass: from 0 toward −15 dB, low-pass cutoff moves from 20 kHz to 8 kHz. Intermediate mapping, shelf frequency and filter slope are U.

Evidence: `channel-eq:B06`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-CEQ-006 — spectrum and curves

**D12.** Visualization shows resulting filter curves and processed-signal spectrum in real time. FFT, window, amplitude calibration, pixel rendering and update latency are U.

Evidence: `channel-eq:B07`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-CEQ-007 — processed output gain

**D12.** Output adjusts gain of processed signal. Track mixer laws do not establish this control’s conversion, domain, saturation or smoothing. Placing Saturator after it is a documented use case, not a Channel EQ distortion algorithm.

Evidence: `channel-eq:B08,B12`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-CEQ-008 — retained state vocabulary

**Dpkg.** Schema ChannelEq declares HighpassOn, LowShelfGain, MidGain, MidFrequency, HighShelfGain and Gain; Boom Capture.adv retains concrete values. Raw saved values do not establish displayed dB conversion, constructor defaults or accepted ranges.

Evidence: `PKG-SCHEMA:ChannelEq; PKG-CHANNEL-EQ`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-CEQ-009 — lifecycle and response gaps

**U.** Exact-build D12 applicability, complete stereo response, automation, undo/redo, persistence, invalid text/state, cancel, bypass, sample-rate/block-size changes and teardown remain U. Cases below retain finite probes without success oracles.

Evidence: `U`; [exact retained locators](#analysis-only-evidence).

Acceptance scenarios are defined completely in [cases.json](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/cases.json); every row below retains its setup/action and documented outcome or ungraded unknown. Documentary comparisons grade only named controls, settings or relations, never sample/pixel/timing equivalence.

| Case | Requirement suffixes | Kind and setup/action | Expected outcome | Evidence |
| --- | --- | --- | --- | --- |
| CEQ-C001 | 002 | positive: SIG-MULTI; toggle HP 80 Hz. | High-pass toggles; nominal label 80 Hz. Exact response U. | D12: `channel-eq:B03` |
| CEQ-C002 | 003 | boundary: Set Low −15, 0, +15 dB. | Both endpoints accepted as documented control settings; low shelf tuned 100 Hz and curve adapts with gain. Exact gain/curve U. | D12: `channel-eq:B04` |
| CEQ-C003 | 004 | boundary: Set Mid −12 then +12 dB; Mid Frequency 120 Hz then 7.5 kHz. | Documented gain/frequency endpoints exist. Peak bandwidth/response U. | D12: `channel-eq:B05` |
| CEQ-C004 | 005 | boundary: High at 0 dB then −15 dB. | Low-pass cutoff documented from 20 kHz to 8 kHz, alongside shelf attenuation. No interpolation or measured cutoff criterion. | D12: `channel-eq:B06` |
| CEQ-C005 | 005 | positive: High at +15 dB on SIG-MULTI. | High-shelf boosting available up to +15 dB. Exact response U. | D12: `channel-eq:B06` |
| CEQ-C006 | 006 | positive: SIG-MULTI; change Low, Mid, High with device visible. | Filter curves and processed spectrum visualized in real time. Pixel/latency oracle U. | D12: `channel-eq:B07` |
| CEQ-C007 | 007 | positive: Hold EQ settings; change Output. | Processed-signal gain changes; numeric range/conversion U. | D12: `channel-eq:B08` |
| CEQ-C008 | 001 | interaction: Place Channel EQ after a reverb, then on a Drum Rack pad; inspect processed signal. | Documented chain placements allow shaping those upstream signals. No reverb/Drum Rack DSP or lifecycle assertion. | D12: `channel-eq:B10,B11` |
| CEQ-C009 | 008 | file observation: Decode retained package/Channel EQ/Boom Capture.adv using gzip/XML and read /Ableton/ChannelEq. | Exact stored strings: {"HighpassOn/Manual": "false", "LowShelfGain/Manual": "4.15796185", "MidFrequency/Manual": "119.999985"}. No display-unit/enum/DSP inference. | Dpkg: `PKG-CHANNEL-EQ` |
| CEQ-C010 | 009 | automation: At bar 2 automate HP off→on, Low −15→+15 dB, Mid Frequency 120→7500 Hz and High 0→−15 dB; manually override/re-enable. Record scheduling and smoothing. | Unknown; no oracle, record without grading. | U: `U` |
| CEQ-C011 | 009 | negative/boundary: Enter Low +16 dB, Mid −13 dB and frequency 0/8000 Hz; record reject/clamp/step behavior and cutoff law at High −7.5 dB. | Unknown; no oracle, record without grading. | U: `U` |
| CEQ-C012 | 009 | malformed: Separate copies of ChannelEq preset: remove MidFrequency, duplicate HighpassOn, set MidGain=NaN and Gain=infinity. Record errors, normalization and source preservation. | Unknown; no oracle, record without grading. | U: `U` |
| CEQ-C013 | 009 | cancel: Mid Frequency numeric edit 1000→2000 then Escape; record value, audio and undo history. | Unknown; no oracle, record without grading. | U: `U` |
| CEQ-C014 | 009 | undo: Toggle HP, change Low to +9 dB and High to −9 dB; Undo three times, Redo three times; record complete filter state and output. | Unknown; no oracle, record without grading. | U: `U` |
| CEQ-C015 | 009 | persistence: Save/reopen Set and preset with HP on, Low +9 dB, Mid −6 dB at 2 kHz, High −9 dB, nonzero Output; compare displayed controls, saved values and response. | Unknown; no oracle, record without grading. | U: `U` |
| CEQ-C016 | 009 | teardown: Stream SIG-STEREO; bypass, delete, undo deletion, suspend/resume engine and close Set. Record channel continuity, click/ramp, state and resources. | Unknown; no oracle, record without grading. | U: `U` |
| CEQ-C017 | 009 | sample-rate: Measure impulse/sweep at HP off/on, low gain endpoints and High attenuation endpoints across 44.1/48/96 kHz, blocks 64/512; include unequal L/R input. Determine response, channel mapping, latency and headroom. | Unknown; no oracle, record without grading. | U: `U` |

## EQ Eight

### REQ-DEVICE-EQ8-001 — filter count and channel modes

**D12.** Up to eight parametric filters per input channel are documented. Stereo applies one curve equally to both input channels; L/R independently edits L and R; M/S provides independently editable curves for the documented M/S-encoded signal use. Encoding/decoding matrix and normalization are U.

Evidence: `eq-eight:B02–B03`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-002 — active editing channel

**D12.** In L/R and M/S both curves are visible, but only the Edit-selected channel is editable. Edit toggles curves. Mode-switch copying, inactive-value retention and saved selection are U.

Evidence: `eq-eight:B04`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-003 — eight response choices

**D12.** Per band the chooser offers 48 and 12 dB/octave low cut, low shelf, peak, notch, high shelf, and 12 and 48 dB/octave high cut, in that documented vertical order. Response labels establish directional selection, not coefficient sets, exact cutoff attenuation or numeric stored enums.

Evidence: `eq-eight:B05–B11`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-004 — independent band enable

**D12.** Each band has its own activator under the chooser. More than one filter can share parameters for stronger combined filtering. Bypass ramps, internal execution/CPU measurements and summation order are U.

Evidence: `eq-eight:B12`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-005 — graph editing and selection

**D12.** Dragging dots horizontally changes frequency and vertically changes gain for gain-supporting filters. Drag-enclosing multiple dots selects them for simultaneous mouse or arrow-key changes. Selection geometry, key increment and mixed-response constraints are U.

Evidence: `eq-eight:B13`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-006 — Q and cut/notch restrictions

**D12.** Alt on Windows or Option on macOS while dragging adjusts Q. Low cut, Notch and High cut do not support gain changes; vertical dragging changes Q for these response types. Numeric Q range and bandwidth convention are U.

Evidence: `eq-eight:B13`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-007 — expanded display

**D12.** The title-bar button moves the display between device chain and main window. In expanded view all eight filters can be edited simultaneously in Device View. Layout sizes, focus transfer and hidden-state persistence are U.

Evidence: `eq-eight:B14`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-008 — output spectrum visibility

**D12.** Analyze displays output spectrum behind curves in every processing mode. The output spectrum is shown by default according to the manual; Analyze off disables spectrum view. FFT/window, channel combination, display latency and runtime constructor default are U.

Evidence: `eq-eight:B03,B15`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-009 — Adaptive Q

**D12.** With Adaptive Q enabled, Q increases as boost/cut amount increases. Exact gain-to-Q relation, shelf applicability and interaction with Scale are U; AdaptiveQFactor=1.12 in one file is not such a law.

Evidence: `eq-eight:B16`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-010 — held Audition

**D12.** Enabling Audition with the headphone icon permits temporary single-filter solo by clicking and holding a filter dot, so only that filter’s effect is heard. Release ends the described temporary hold; exact audition transfer, transitions and transport interaction are U.

Evidence: `eq-eight:B17`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-011 — numeric editing

**D12.** Clicking near a band number selects it for Freq/Gain/Q dials or direct numeric-field entry. Text parsing, units, malformed input and out-of-range normalization are U.

Evidence: `eq-eight:B18`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-012 — global Gain

**D12.** Global Gain adjusts output level. Its range, dB conversion, processing order relative to oversampling and smoothing are U.

Evidence: `eq-eight:B19`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-013 — Scale eligibility

**D12.** Scale adjusts gain of all gain-supporting filters, excluding low cut, notch and high cut. Scale domain, arithmetic law, sign/inversion and parameter mutation versus effective-gain behavior are U.

Evidence: `eq-eight:B20`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-014 — Oversampling context option

**D12.** Oversampling is available from the device title-bar context menu. When enabled, internal processing is documented at twice the current sample rate. This is a D12 rate statement only; resampling filters, latency, precision, transition handling and exact target operation are U.

Evidence: `eq-eight:B21–B23`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-015 — response-specific sound

**D12.** Low cut removes below-frequency content; high cut above-frequency content; shelves boost/cut their respective sides, peak a range, notch a narrow range. No ideal brick wall, perfect null, linear-phase design, minimum-phase coefficients or response tolerance is specified.

Evidence: `eq-eight:B06–B11`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-016 — retained two-bank storage

**Dpkg.** Schema declares Bands.0–Bands.7 as Eq8Band, each with ParameterA/ParameterB; Eq8BandParameter declares IsOn, Mode, Freq, Gain, Q. Retained EQ Eight.adv stores both banks plus Precision/Mode/EditMode, gain/Scale/analyzer/AdaptiveQ state. The A/B-to-L/R/M/S mapping and Precision-to-Oversampling mapping are U.

Evidence: `PKG-SCHEMA:Eq8,Eq8Band,Eq8BandParameter; PKG-EQ-EIGHT`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ8-017 — lifecycle and numerical gaps

**U.** Exact-build applicability, mode conversion, live automation and overrides, state save/reopen, legacy migration, undo/cancel, malformed state, engine and display teardown and numerical DSP remain U. The independent Spectrum device’s fields do not supply EQ Eight analyzer algorithms.

Evidence: `U`; [exact retained locators](#analysis-only-evidence).

Acceptance scenarios are defined completely in [cases.json](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/cases.json); every row below retains its setup/action and documented outcome or ungraded unknown. Documentary comparisons grade only named controls, settings or relations, never sample/pixel/timing equivalence.

| Case | Requirement suffixes | Kind and setup/action | Expected outcome | Evidence |
| --- | --- | --- | --- | --- |
| EQ8-C001 | 001 | positive: SIG-STEREO; Stereo mode; one active peak at 1000 Hz, +6 dB, Q displayed 1. | Same curve filters both input channels; absolute response U. | D12: `eq-eight:B02,B03` |
| EQ8-C002 | 001, 002 | positive: L/R mode; Edit left; set peak 1000 Hz +6 dB; Edit right, set 4000 Hz −6 dB. | Curves independently editable; both visible; only active channel editable. Numeric response U. | D12: `eq-eight:B03,B04` |
| EQ8-C003 | 001, 002 | positive: Use documented M/S-encoded source; choose M/S; toggle Edit and change one curve. | Independent active-curve editing available as documented; encoding/decoding matrix not graded. | D12: `eq-eight:B03,B04` |
| EQ8-C004 | 003 | positive: Inspect response chooser for a selected band. | Eight responses in documented order: low cut 48/12, low shelf, peak, notch, high shelf, high cut 12/48 dB/octave. Numeric enum mapping U. | D12: `eq-eight:B05–B11` |
| EQ8-C005 | 004 | positive: Set bands 1 and 2 to same peak 1000 Hz +6 dB Q 1; independently toggle each activator. | Independent activators exist; simultaneous matched filters can strengthen filtering. Numeric additivity U. | D12: `eq-eight:B12` |
| EQ8-C006 | 005 | positive: Peak selected; drag dot horizontally then vertically. | Frequency changes horizontally, gain vertically. Pixel law/step size U. | D12: `eq-eight:B13` |
| EQ8-C007 | 005 | positive: Drag-enclose dots 2 and 3; drag group then use arrow key once. | Selected dots are editable together with mouse or keyboard. Exact increments U. | D12: `eq-eight:B13` |
| EQ8-C008 | 006 | positive: Peak dot; drag while holding Option on macOS (Alt on Windows). | Gesture changes Q. Modifier cancellation and platform target parity U. | D12: `eq-eight:B13` |
| EQ8-C009 | 006 | negative: Select Low cut; attempt vertical gain drag. | Gain is not adjustable; vertical drag adjusts Q. Stored unused gain retention U. | D12: `eq-eight:B13` |
| EQ8-C010 | 006 | negative: Select Notch; attempt vertical gain drag. | Gain is not adjustable; vertical drag adjusts Q. Stored unused gain retention U. | D12: `eq-eight:B13` |
| EQ8-C011 | 006 | negative: Select High cut; attempt vertical gain drag. | Gain is not adjustable; vertical drag adjusts Q. Stored unused gain retention U. | D12: `eq-eight:B13` |
| EQ8-C012 | 007 | positive: Click expansion button, inspect eight band controls, return to chain display. | Display switches location; expanded Device View permits simultaneous editing of all eight filters. Geometry/focus persistence U. | D12: `eq-eight:B14` |
| EQ8-C013 | 008 | positive: For Stereo/L/R/M/S, enable Analyze then turn it off on SIG-MULTI. | On shows output spectrum behind curves; off disables spectrum view. Analysis-to-audio transparency ungraded. | D12: `eq-eight:B03,B15` |
| EQ8-C014 | 009 | positive: Peak filter at fixed displayed Q; Adaptive Q on; compare boost/cut magnitudes 3 and 9 dB. | Higher absolute boost/cut increases effective Q as described. Exact amount/effective-vs-displayed representation U. | D12: `eq-eight:B16` |
| EQ8-C015 | 010 | positive/cancel: Two active peaks; Audition on; press-hold first dot then release. | Holding temporarily solos that filter’s effect; release ends held audition. Exact signal/ramp U. | D12: `eq-eight:B17` |
| EQ8-C016 | 011 | positive: Click near band 3 number; type frequency 1000 in its Freq field and change Gain/Q dials. | Band selected for dial/numeric editing; parsing variants/boundaries U. | D12: `eq-eight:B18` |
| EQ8-C017 | 012 | positive: SIG-MULTI with fixed bands; move global Gain. | Output level can be adjusted. Conversion/range/smoothing U. | D12: `eq-eight:B19` |
| EQ8-C018 | 013 | negative/interaction: Active Peak plus Low cut, Notch and High cut; change Scale. | Only gain-supporting filters are affected by Scale; three named response types excluded. Stored-value mutation and arithmetic U. | D12: `eq-eight:B14,B20` |
| EQ8-C019 | 014 | positive/boundary: Set sample rate 48 kHz, enable Oversampling in title-bar context menu. | The menu offers an enabled Oversampling state. The documented doubled internal rate is 96 kHz for this setup; the menu-state comparison cannot verify that rate or audio behavior. | D12: `eq-eight:B21–B23` |
| EQ8-C020 | 015 | positive: SIG-MULTI; compare low shelf, high shelf, peak and notch at 1000 Hz with documented boost/cut capability. | Responses act on their documented frequency regions. Exact transfer/attenuation U. | D12: `eq-eight:B07–B10` |
| EQ8-C021 | 016 | file observation: Decode retained package/EQ Eight/EQ Eight.adv using gzip/XML and read /Ableton/Eq8. | Exact stored strings: {"AdaptiveQFactor": "1.12", "Bands.0/ParameterA/Freq/Manual": "30", "Bands.0/ParameterB/Freq/Manual": "40", "Mode": "0", "Precision": "0"}. No display-unit/enum/DSP inference. | Dpkg: `PKG-EQ-EIGHT` |
| EQ8-C022 | 017 | mode conversion: Set distinct L/R and M/S curves and unused bands, switch Stereo→L/R→M/S→Stereo and edit each active curve; inspect copying, hidden-value retention and A/B saved mapping. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C023 | 017 | automation: Automate band 3 frequency 500→5000 Hz, enable, Q and global Scale; change Mode/Edit during playback, override and re-enable. Record active-bank ownership and effective response. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C024 | 017 | boundary: Enter Freq 0/100000, Gain 1000, Q 0/−1, Scale negative/zero/above displayed maximum. Record parser, units, clamping and response. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C025 | 017 | malformed: Separate Eq8 preset copies: remove ParameterB, duplicate Bands.0, set Mode=999 and band Q=NaN. Record refusal/repair, diagnostics and source preservation. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C026 | 017 | cancel: Begin Freq edit 1000→2000 then Escape; drag multi-selection then Escape; open context menu and dismiss. Record state, output and undo ownership. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C027 | 017 | undo: Set L/R different curves, change Scale, enable Oversampling and Adaptive Q; Undo/Redo each change. Record both banks, selection, analyzer and output. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C028 | 017 | persistence: Save/reopen Set and preset with L/R different banks, disabled bands carrying nondefault gains, Scale nondefault, Analyze off, Audition on, expanded view and Oversampling on; compare state and output. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C029 | 017 | legacy: Use old preset with Live8ShelfScaleLegacyMode changed on a copy; load/save through a future authorized route. Record shelf/Scale/AdaptiveQAffectsShelves migration and behavior, not inferred from field names. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C030 | 017 | audition teardown: Hold Audition dot while transport stops, focus changes, mouse release occurs outside device and device is deleted; undo deletion and close Set. Record whether audition clears and resource state. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C031 | 017 | sample-rate: At 44.1/48/96 kHz compare Oversampling off/on with high-frequency sweep and moving cutoff; blocks 64/512. Measure effective rate evidence, response, latency and transition discontinuities. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C032 | 017 | adaptive law: Peak and shelves at Q 0.7, gains −12/−6/0/+6/+12 dB, Scale 50/100/150%; Adaptive Q off/on. Determine effective bandwidth/gain without treating saved factor 1.12 as a formula. | Unknown; no oracle, record without grading. | U: `U` |
| EQ8-C033 | 017 | engine failure: With Analyze and Oversampling on, disable/re-enable engine and remove source track while device remains visible. Record stale spectrum clearing, audio recovery and saved state. | Unknown; no oracle, record without grading. | U: `U` |

## EQ Three

### REQ-DEVICE-EQ3-001 — independent low/mid/high levels

**D12.** EQ Three independently adjusts low, mid and high frequency bands of incoming audio. This is an audible band-split processor, not a guaranteed transparent path with gains at zero.

Evidence: `eq-three:B02,B08`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ3-002 — gain endpoints

**D12.** Each band gain ranges from minus infinity dB to +6 dB. Complete removal at the lower endpoint is documentary band removal, not a measured full-signal null at any frequency. Gain conversion, clipping and ramps are U.

Evidence: `eq-three:B03`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ3-003 — band On/Off

**D12.** Each band has an independent On/Off button below gain. A disabled band can still indicate input-band activity with its LED; numeric gain value retention and toggling transitions are U.

Evidence: `eq-three:B04–B05`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ3-004 — band activity LEDs

**D12.** Three LEDs indicate signal presence in the three bands even if a band is disabled. The documented internal threshold is −24 dB. Reference level, detector stage/window, equality tie, hold and fall times are U.

Evidence: `eq-three:B05`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ3-005 — crossover meaning

**D12.** FreqLo and FreqHi define low/mid/high divisions. At FreqLo=500 Hz and FreqHi=2000 Hz, documented ranges are 0–500, 500–2000 and above 2000 Hz to the sample-rate/soundcard limit. These labels do not specify response at either crossover, exclusive frequency bins or Nyquist handling.

Evidence: `eq-three:B06`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ3-006 — 24/48 slope switch

**D12.** 24 dB/48 dB selects crossover filter sharpness; higher setting is described as more drastic filtering with higher CPU cost. Actual measured slope, phase and cost are U.

Evidence: `eq-three:B07`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ3-007 — nonflat 48 dB mode

**D12.** 48 dB mode is documented as slightly coloring input even when all gain controls are 0.00 dB; 24 dB is described as more linear. No exact coloration curve, null tolerance or assertion of perfectly flat 24 dB mode is supported.

Evidence: `eq-three:B08`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ3-008 — retained state vocabulary

**Dpkg.** FilterEQ3 declares three gains, two crossover frequencies, three enables, Slope and FlatResponse. Boost HiHats.adv retains exact values. FlatResponse=false is a file observation, not a migration law or response oracle.

Evidence: `PKG-SCHEMA:FilterEQ3; PKG-EQ-THREE`; [exact retained locators](#analysis-only-evidence).

### REQ-DEVICE-EQ3-009 — lifecycle and numerical gaps

**U.** Exact-build applicability, crossing/equal/out-of-range crossover values, automation and modulation, undo/persistence/cancel, malformed state, bypass, engine changes and teardown remain U. Threshold and slope labels do not supply DSP coefficients or calibration.

Evidence: `U`; [exact retained locators](#analysis-only-evidence).

Acceptance scenarios are defined completely in [cases.json](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/cases.json); every row below retains its setup/action and documented outcome or ungraded unknown. Documentary comparisons grade only named controls, settings or relations, never sample/pixel/timing equivalence.

| Case | Requirement suffixes | Kind and setup/action | Expected outcome | Evidence |
| --- | --- | --- | --- | --- |
| EQ3-C001 | 001, 005 | positive: SIG-MULTI; FreqLo 500 Hz, FreqHi 2000 Hz; adjust three gains separately. | Documented low/mid/high divisions and independent band level controls; crossover response U. | D12: `eq-three:B02,B06` |
| EQ3-C002 | 002 | boundary: For Low set gain −infinity then +6 dB. | Both documented endpoints exist; minimum removes that band. Exact total output/null U. | D12: `eq-three:B03` |
| EQ3-C003 | 002 | boundary: For Mid set gain −infinity then +6 dB. | Both documented endpoints exist; minimum removes that band. Exact total output/null U. | D12: `eq-three:B03` |
| EQ3-C004 | 002 | boundary: For High set gain −infinity then +6 dB. | Both documented endpoints exist; minimum removes that band. Exact total output/null U. | D12: `eq-three:B03` |
| EQ3-C005 | 003, 004 | negative: Feed energy in Low band, disable its On button; inspect corresponding LED. | Band remains able to show activity while disabled; threshold calibration/tie/timing U. | D12: `eq-three:B04,B05` |
| EQ3-C006 | 003, 004 | negative: Feed energy in Mid band, disable its On button; inspect corresponding LED. | Band remains able to show activity while disabled; threshold calibration/tie/timing U. | D12: `eq-three:B04,B05` |
| EQ3-C007 | 003, 004 | negative: Feed energy in High band, disable its On button; inspect corresponding LED. | Band remains able to show activity while disabled; threshold calibration/tie/timing U. | D12: `eq-three:B04,B05` |
| EQ3-C008 | 006 | positive: Inspect 24/48 dB switch and select both settings with fixed crossovers. | Two documented choices; 48 dB described as sharper. Measured slope/CPU U. | D12: `eq-three:B07` |
| EQ3-C009 | 007 | negative: All band gains displayed 0.00 dB, all enabled; compare 48 and 24 dB modes. | No perfect-null criterion is valid: 48 dB is documented to color sound, 24 dB is described as more linear. Exact coloration U. | D12: `eq-three:B08` |
| EQ3-C010 | 008 | file observation: Decode retained package/EQ Three/Boost HiHats.adv using gzip/XML and read /Ableton/FilterEQ3. | Exact stored strings: {"FlatResponse": "false", "FreqHi/Manual": "2037.84412", "FreqLo/Manual": "464.754883", "GainHi/Manual": "1.99526203"}. No display-unit/enum/DSP inference. | Dpkg: `PKG-EQ-THREE` |
| EQ3-C011 | 009 | automation: Automate FreqLo 250→1000 Hz, FreqHi 4000→1500 Hz, Low On and High gain −infinity→+6 dB across bar boundary; override and re-enable. Record effective split, smoothing and schedule. | Unknown; no oracle, record without grading. | U: `U` |
| EQ3-C012 | 009 | boundary: Set FreqLo=FreqHi=1000 Hz then FreqLo=4000/FreqHi=500; enter negative/zero/above-Nyquist crossover and +7 dB gain. Record limits, ordering, rejection and response. | Unknown; no oracle, record without grading. | U: `U` |
| EQ3-C013 | 009 | threshold calibration: Hold single-tone input at −24.1/−24/−23.9 dB relative to a recorded full-scale convention in low/mid/high bands; sweep durations 1/10/100/1000 ms, band enabled/disabled. Determine detector, tie and hold/release. | Unknown; no oracle, record without grading. | U: `U` |
| EQ3-C014 | 009 | malformed: Separate FilterEQ3 preset copies: remove FreqLo, duplicate LowOn, set Slope=999 and GainHi=NaN; record errors/repair and source preservation. | Unknown; no oracle, record without grading. | U: `U` |
| EQ3-C015 | 009 | cancel: Begin FreqHi numeric edit 2000→4000 then Escape; record control, output and undo history. | Unknown; no oracle, record without grading. | U: `U` |
| EQ3-C016 | 009 | undo: Change three band enables, crossovers 500/2000→250/4000 and slope 24→48; Undo/Redo individual actions. Record gains, LED state and response. | Unknown; no oracle, record without grading. | U: `U` |
| EQ3-C017 | 009 | persistence: Save/reopen Set and preset with Low off, Mid −infinity, High +6 dB, FreqLo 500/FreqHi 2000 and 48 dB slope; inspect both settings and FlatResponse without presuming its meaning. | Unknown; no oracle, record without grading. | U: `U` |
| EQ3-C018 | 009 | teardown: During SIG-MULTI streaming and LED activity, bypass/delete device, undo deletion, suspend/resume engine and close Set. Record output transitions, restored state and resource release. | Unknown; no oracle, record without grading. | U: `U` |
| EQ3-C019 | 009 | sample-rate: Record impulse/sweep in 24/48 dB modes with all gains 0 and varied levels, at 44.1/48/96 kHz, blocks 64/512; determine transfer coloration, crossover phase, latency and headroom. | Unknown; no oracle, record without grading. | U: `U` |

## Auto Filter Legacy obligation

`SURF-DEVICE-LEGACY-AUTO-FILTER-LEGACY` remains **behaviorally unmapped**.
The retained `Auto Filter (Legacy).adv` has an `AutoFilter` root, distinct from
current `AutoFilter2`; its `LegacyMode=false` does not erase that distinction.
The schema and file support stored-vocabulary observations only. No distinct
legacy interaction/audio source is retained, so none of the current Auto Filter
D12 laws is assigned to Legacy. AF’s ungraded legacy-applicability scenario
records the investigation obligation without pretending to specify Legacy’s sound.
This is an unresolved inventory entry, not a supported exclusion or fifth complete profile.

## Acceptance scope and cross-feature gaps

[Signal recipes](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/fixture-signals.json)
define finite hypothetical probes; no WAV/audio result was produced. Each case’s
machine record includes stable requirements, setup/action, expected result or
null, provenance, comparison rule and unexecuted state. Positive, negative,
boundary, automation, persistence, undo/redo, malformed/error, cancel, timing and
teardown scenarios are device-specific. Detector-source loss is specific to Auto
Filter; no external detector is invented for the three equalizers. File errors
are distinct from valid audio input: silence, overload and near-Nyquist response
still require calibrated audio evidence. Subjective terms such as clean, warmer,
coloration or smoother are documentary descriptions without an audio pass metric.

## Analysis-only evidence

`D12-AUDIO-EFFECTS` is the [official Version 12 reference](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/),
captured 2026-10-19, with no publication pin to 12.4.3. The exact
[HTML bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html)
are reused by external hash pin, not downloaded/copied again. The
[source manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/sources.json)
records URL, capture date, version uncertainty, source path, byte size and SHA-256.
Block IDs below retain exact text, heading anchor and HTML start line:

- [Auto Filter B01–B65](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manual-auto-filter-blocks.json), h2 §29.2 `#auto-filter`, line 292.
- [Channel EQ B01–B12](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manual-channel-eq-blocks.json), h2 §29.7 `#channel-eq`, line 684.
- [EQ Eight B01–B23](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manual-eq-eight-blocks.json), h2 §29.15 `#eq-eight`, line 1074.
- [EQ Three B01–B08](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manual-eq-three-blocks.json), h2 §29.16 `#eq-three`, line 1122.

Ranges in citations are inclusive; a comma keeps the same device prefix. `PKG-SCHEMA`
refers to the externally pinned [latest shipped schema](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt).
[Filtered class declarations](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/schema-fields.json)
retain original class lines, names and types. `PKG-AUTO-FILTER`, `PKG-CHANNEL-EQ`,
`PKG-EQ-EIGHT` and `PKG-EQ-THREE` resolve in sources.json; full
[package-value locators](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/package-values.json)
retain XML paths and root Creator/revision. Historical presets shipped in 12.4.3
are not target-application saves. Figures were not inspected. Sidechain Type
and internal detector-tap wording discrepancies are preserved in research,
not silently resolved by naming schema fields.

The [author freeze](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manifest-author-r1.json)
pins this page, the research page and packet payloads for separate review. No
release, implementation or verification claim follows from packet consistency.

## Revision history

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-19 | First partial four-device documentary/file contract; Legacy and numerical/lifecycle outcomes stay open |
