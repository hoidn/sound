---
id: SPEC-DISTORTION-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documentary Live 12 behavior with exact-build applicability unknown
---

# Distortion devices

## Scope and authority

This partial draft owns individual distortion profiles under FEAT-DEVICE-CATALOG:
Drum Buss, Dynamic Tube, modern Erosion, Overdrive, Pedal, current Redux, Roar,
Saturator and Vinyl Distortion. It does not merge modern Erosion2 with Erosion
Legacy or Redux2 with Redux Legacy. These are nine partial profiles, none complete.
[Device racks](device-racks.md) owns serial/parallel chains, generic insertion,
activation, presets and macros; [automation envelopes](automation-envelopes.md)
owns retained envelope representation and finite evaluation laws;
[mix graph](mix-graph.md) owns its bounded routing/mixing laws. The seven
[bundled-device host](bundled-device-hosting.md) internals do not prove these
native devices' application behavior. This draft specifies no candidate design.

**D12** means a documentary clause from the official Version 12 manual captured
2026-10-19. Every D12 application clause has **exact 12.4.3 applicability U**.
**Dpkg** means a documentary assertion about the pinned installed bytes only.
**U** means ungraded, with null expected result. Source identity and locators
are retained below. No original function, application, emulator or candidate ran.
All requirements remain draft; there is no release or compatibility pass.

## Inputs, observables and prerequisites

Use a valid editable Set and isolate one device on an independently established
audio path. Record device identity, mode, displayed units, control values,
activators, sidechain/matrix state, quality modes, host rate/block size and
source signal before each case. Factory defaults are not assumed. Finite source
signals S0–S3 and required path checks P-AUDIO are in
[fixture-signals.json](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/fixture-signals.json).
Rate changes recreate the same-duration analytic signal, not a resampled capture.

Any asserted effect or no-effect needs independent active-path evidence, nonzero
source in the tested band, effective nonzero tested control/modulation depth,
nonmuted processed output and control-sensitive positive baselines. Isolate dry,
return, sidechain, crackle/noise and other stages. A zero control by itself is not
proof of bypass. If a required baseline or path is unestablished, record **U**.
All packet audio experiments remain U; documentary audio descriptions provide
no calibrated waveform, spectrum, envelope, CPU or delay oracle. A UI/state case
never substitutes for an audio comparator. Observable units/frequencies below
are documentary nominal values, not measured filter/DSP tolerances.

## Drum Buss

### REQ-DST-DRUM-BUSS-001 — installed representation

**Dpkg** (schema-fields.json#class=DrumBuss, package-values.json#class=DrumBuss). The pinned schema declares DrumBuss; the frozen single shipped preset has /Ableton/DrumBuss. Its Creator is historical Ableton Live 12.4d1 and MinorVersion is 12.0_12402. Exact field records are in schema-fields.json and package-values.json. These facts establish vocabulary and one stored example only; neither constructor defaults, GUI bounds, automation legality, model indices nor DSP are inferred.

### REQ-DST-DRUM-BUSS-002 — input order and distortion choices

**D12** (manual-drum-buss-blocks.json#drum-buss:B003, manual-drum-buss-blocks.json#drum-buss:B004, manual-drum-buss-blocks.json#drum-buss:B005, manual-drum-buss-blocks.json#drum-buss:B006, manual-drum-buss-blocks.json#drum-buss:B007, manual-drum-buss-blocks.json#drum-buss:B008, manual-drum-buss-blocks.json#drum-buss:B009). Trim reduces the input ahead of processing. Comp enables an input compressor ahead of distortion; its attack/release/ratio descriptions do not specify numerical settings. Drive increases the level entering distortion. Soft denotes waveshaping, Medium limiting, and Hard clipping with bass emphasis. No transfer equation, threshold, normalization or compressor envelope is supplied.

### REQ-DST-DRUM-BUSS-003 — mid/high shaping

**D12** (manual-drum-buss-blocks.json#drum-buss:B013, manual-drum-buss-blocks.json#drum-buss:B014, manual-drum-buss-blocks.json#drum-buss:B015). Crunch controls sine-shaped mid/high distortion; Damp is a low-pass stage. Transients addresses frequencies above 100 Hz: positive settings emphasize attack and sustain, while negative settings add attack and reduce sustain. Exact crossover, transient detector, boost and damping laws are U.

### REQ-DST-DRUM-BUSS-004 — low enhancement and tuning

**D12** (manual-drum-buss-blocks.json#drum-buss:B017, manual-drum-buss-blocks.json#drum-buss:B018, manual-drum-buss-blocks.json#drum-buss:B019, manual-drum-buss-blocks.json#drum-buss:B020). Boom sets resonant bass enhancement and has a Bass Meter. Freq sets its frequency; Force To Note moves that frequency to the nearest MIDI-note frequency. Decay affects the incoming post-distortion lows at Boom=0 and both incoming and resonant lows at Boom>0. Exact tuning reference, rounding ties, decay curves and zero-Boom residuals are U.

### REQ-DST-DRUM-BUSS-005 — audition and output

**D12** (manual-drum-buss-blocks.json#drum-buss:B021, manual-drum-buss-blocks.json#drum-buss:B023, manual-drum-buss-blocks.json#drum-buss:B024). Boom Audition solos the low enhancer. Dry/Wet balances dry and processed paths; Output Gain sets processed-path gain. Neither these balances nor audition establish a mixer curve, compensated level or sample-exact bypass.

### REQ-DST-DRUM-BUSS-006 — automation, state, errors and teardown

**U** (packet limits). For Drum Buss, exact parameter automation/clip-modulation/macro precedence, mode-change smoothing, sample/block-rate behavior, transport history, preset/Set reopen and migration, undo/redo transactions, malformed/invalid input handling, cancellation rollback and teardown are unresolved. Schema persistence vocabulary does not resolve these behaviors. No failure response, silence, continuity, reset, equality, timing or accepted-input policy is asserted.

## Dynamic Tube

### REQ-DST-DYNAMIC-TUBE-001 — installed representation

**Dpkg** (schema-fields.json#class=Tube, package-values.json#class=Tube). The pinned schema declares Tube; the frozen single shipped preset has /Ableton/Tube. Its Creator is historical Ableton Live 12.4d1 and MinorVersion is 12.0_12402. Exact field records are in schema-fields.json and package-values.json. These facts establish vocabulary and one stored example only; neither constructor defaults, GUI bounds, automation legality, model indices nor DSP are inferred.

### REQ-DST-DYNAMIC-TUBE-002 — models and drive/bias

**D12** (manual-dynamic-tube-blocks.json#dynamic-tube:B002, manual-dynamic-tube-blocks.json#dynamic-tube:B003, manual-dynamic-tube-blocks.json#dynamic-tube:B004, manual-dynamic-tube-blocks.json#dynamic-tube:B005). Models A, B and C have distinct saturation characteristics. A at low Bias is described as non-distorting until a signal threshold is reached; C is described as continually distorting; B is intermediate. Drive sets input to the tube, Bias changes the operating point, and Tone changes the spectral distribution of distortion. The words low and threshold supply no measured boundary, and silence is not evidence of nonlinear processing.

### REQ-DST-DYNAMIC-TUBE-003 — envelope sign

**D12** (manual-dynamic-tube-blocks.json#dynamic-tube:B006). Envelope applies input-level-following modulation to Bias. Positive values increase distortion on loud input; negative values reduce it. Modulation depth grows with Envelope magnitude. Detector response, scaling, sign crossing and compensation are U.

### REQ-DST-DYNAMIC-TUBE-004 — zero envelope boundary

**D12** (manual-dynamic-tube-blocks.json#dynamic-tube:B007). Attack and Release set follower response timing. At Envelope=0 they have no effect through that follower path. This documentary no-effect rule does not specify static Bias distortion or an equality tolerance.

### REQ-DST-DYNAMIC-TUBE-005 — output and quality

**D12** (manual-dynamic-tube-blocks.json#dynamic-tube:B008, manual-dynamic-tube-blocks.json#dynamic-tube:B009). Output cuts or boosts final signal level. The title context menu exposes Hi-Quality, documented to reduce aliasing at increased CPU cost. Oversampling factor, filters, delay and numerical/CPU targets are U. The schema DryWet field does not establish an additional exposed control.

### REQ-DST-DYNAMIC-TUBE-006 — automation, state, errors and teardown

**U** (packet limits). For Dynamic Tube, exact parameter automation/clip-modulation/macro precedence, mode-change smoothing, sample/block-rate behavior, transport history, preset/Set reopen and migration, undo/redo transactions, malformed/invalid input handling, cancellation rollback and teardown are unresolved. Schema persistence vocabulary does not resolve these behaviors. No failure response, silence, continuity, reset, equality, timing or accepted-input policy is asserted.

## Erosion

### REQ-DST-EROSION-001 — installed representation

**Dpkg** (schema-fields.json#class=Erosion2, package-values.json#class=Erosion2). The pinned schema declares Erosion2; the frozen single shipped preset has /Ableton/Erosion2. Its Creator is historical Ableton Live 12.4d1 and MinorVersion is 12.0_12402. Exact field records are in schema-fields.json and package-values.json. These facts establish vocabulary and one stored example only; neither constructor defaults, GUI bounds, automation legality, model indices nor DSP are inferred.

### REQ-DST-EROSION-002 — modulation and XY controls

**D12** (manual-erosion-blocks.json#erosion:B002, manual-erosion-blocks.json#erosion:B003). Current Erosion modulates a short delay using sine and filtered-noise carriers. Display X changes carrier/noise-center frequency; Y changes Amount. Alt on Windows or Option on macOS with vertical drag changes Filter Width. Playback display shows spectrum/modulation. Delay length, carrier phase and audio formula are U.

### REQ-DST-EROSION-003 — carrier blend and disabled width

**D12** (manual-erosion-blocks.json#erosion:B004, manual-erosion-blocks.json#erosion:B005). Noise Blend=0% uses only sine, and 100% only noise. At 0% Filter Width is grayed out and has no effect on the sine carrier. Carrier icons change emphasis with blend. Width changes noise-band bandwidth away from the sine-only endpoint; exact bandwidth mapping and blend gain law are U.

### REQ-DST-EROSION-004 — stereo carrier

**D12** (manual-erosion-blocks.json#erosion:B006). Stereo Width morphs the modulation source from mono at 0% to stereo at 100%; exact correlation, image metric and noise sequence remain U.

### REQ-DST-EROSION-005 — legacy loading boundary

**D12** (manual-erosion-blocks.json#erosion:B007). The manual says pre-12.4 Sets containing Erosion load Erosion Legacy. This current Erosion2 contract does not define legacy Erosion algorithms, parameters, migration rewriting or an upgrade action. Exact 12.4.3 old-Set loading remains U.

### REQ-DST-EROSION-006 — automation, state, errors and teardown

**U** (packet limits). For Erosion, exact parameter automation/clip-modulation/macro precedence, mode-change smoothing, sample/block-rate behavior, transport history, preset/Set reopen and migration, undo/redo transactions, malformed/invalid input handling, cancellation rollback and teardown are unresolved. Schema persistence vocabulary does not resolve these behaviors. No failure response, silence, continuity, reset, equality, timing or accepted-input policy is asserted.

## Overdrive

### REQ-DST-OVERDRIVE-001 — installed representation

**Dpkg** (schema-fields.json#class=Overdrive, package-values.json#class=Overdrive). The pinned schema declares Overdrive; the frozen single shipped preset has /Ableton/Overdrive. Its Creator is historical Ableton Live 12.4d1 and MinorVersion is 12.0_12402. Exact field records are in schema-fields.json and package-values.json. These facts establish vocabulary and one stored example only; neither constructor defaults, GUI bounds, automation legality, model indices nor DSP are inferred.

### REQ-DST-OVERDRIVE-002 — input filter

**D12** (manual-overdrive-blocks.json#overdrive:B003). The distortion stage follows a band-pass filter. Its XY vertical axis controls bandwidth and horizontal axis center position; slider boxes address the same parameters. Filter transfer and frequency bounds are U.

### REQ-DST-OVERDRIVE-003 — drive zero and post tone

**D12** (manual-overdrive-blocks.json#overdrive:B004, manual-overdrive-blocks.json#overdrive:B005). Drive sets distortion intensity; 0% is explicitly not a zero-distortion guarantee. Tone is post-distortion EQ; higher values add high-frequency content. No nonzero-distortion oracle for arbitrary silence/low signals, threshold or tone response is supplied.

### REQ-DST-OVERDRIVE-004 — dynamics

**D12** (manual-overdrive-blocks.json#overdrive:B006). Dynamics changes compression associated with increasing distortion: lower Dynamics applies more internal compression and makeup gain, while higher values apply less. Exact detector, compression curve, recovery and makeup normalization are U.

### REQ-DST-OVERDRIVE-005 — wet balance

**D12** (manual-overdrive-blocks.json#overdrive:B007). Dry/Wet balances processed and dry signals; 100% is documented for return-track use. Exact balance law, latency alignment, endpoint precision and gain remain U.

### REQ-DST-OVERDRIVE-006 — automation, state, errors and teardown

**U** (packet limits). For Overdrive, exact parameter automation/clip-modulation/macro precedence, mode-change smoothing, sample/block-rate behavior, transport history, preset/Set reopen and migration, undo/redo transactions, malformed/invalid input handling, cancellation rollback and teardown are unresolved. Schema persistence vocabulary does not resolve these behaviors. No failure response, silence, continuity, reset, equality, timing or accepted-input policy is asserted.

## Pedal

### REQ-DST-PEDAL-001 — installed representation

**Dpkg** (schema-fields.json#class=Pedal, package-values.json#class=Pedal). The pinned schema declares Pedal; the frozen single shipped preset has /Ableton/Pedal. Its Creator is historical Ableton Live 12.4d1 and MinorVersion is 12.0_12402. Exact field records are in schema-fields.json and package-values.json. These facts establish vocabulary and one stored example only; neither constructor defaults, GUI bounds, automation legality, model indices nor DSP are inferred.

### REQ-DST-PEDAL-002 — models and gain zero

**D12** (manual-pedal-blocks.json#pedal:B003, manual-pedal-blocks.json#pedal:B004, manual-pedal-blocks.json#pedal:B005, manual-pedal-blocks.json#pedal:B006, manual-pedal-blocks.json#pedal:B007, manual-pedal-blocks.json#pedal:B008). Pedal types are Overdrive, Distortion and Fuzz, with distinct saturation character. Gain controls distortion intensity; 0% does not guarantee zero distortion. Output sets global output gain. Prior input level affects response; no curve or zero-Gain equality is specified.

### REQ-DST-PEDAL-003 — post-distortion adaptive EQ

**D12** (manual-pedal-blocks.json#pedal:B009, manual-pedal-blocks.json#pedal:B010, manual-pedal-blocks.json#pedal:B011, manual-pedal-blocks.json#pedal:B012, manual-pedal-blocks.json#pedal:B013, manual-pedal-blocks.json#pedal:B014, manual-pedal-blocks.json#pedal:B015, manual-pedal-blocks.json#pedal:B016). The three-band EQ follows distortion and increases resonance with EQ boost. Bass is a 100 Hz peak band; Mid switch positions select 500 Hz, 1 kHz and 2 kHz, with a narrower low-position band and wider high-position band. Treble is shelving at 3.3 kHz. These documented nominal frequencies do not supply filter coefficients, boost scaling or tolerances.

### REQ-DST-PEDAL-004 — sub shelf

**D12** (manual-pedal-blocks.json#pedal:B018). Sub enables a shelf that boosts below 250 Hz; it can interact with Bass cut/boost. Exact boost amount, shelving law and net cancellation are U.

### REQ-DST-PEDAL-005 — wet balance and quality

**D12** (manual-pedal-blocks.json#pedal:B019, manual-pedal-blocks.json#pedal:B020). Dry/Wet sets processed/dry balance. Hi-Quality in the title context menu is documented to reduce aliasing with more CPU usage. No oversampling ratio, anti-alias filter, CPU or latency target follows.

### REQ-DST-PEDAL-006 — signal-chain and recipe controls

**D12** (manual-pedal-blocks.json#pedal:B023, manual-pedal-blocks.json#pedal:B025, manual-pedal-blocks.json#pedal:B026, manual-pedal-blocks.json#pedal:B027, manual-pedal-blocks.json#pedal:B029, manual-pedal-blocks.json#pedal:B030, manual-pedal-blocks.json#pedal:B031, manual-pedal-blocks.json#pedal:B033, manual-pedal-blocks.json#pedal:B034, manual-pedal-blocks.json#pedal:B036). Upstream gain/EQ/compression alters Pedal response. The documented kick, fizzle, broken-speaker and sub recipes select existing type/EQ/Sub/Gain/Output/DryWet controls; their subjective character is not a numerical compatibility metric. Recipe values are not defaults.

### REQ-DST-PEDAL-007 — automation, state, errors and teardown

**U** (packet limits). For Pedal, exact parameter automation/clip-modulation/macro precedence, mode-change smoothing, sample/block-rate behavior, transport history, preset/Set reopen and migration, undo/redo transactions, malformed/invalid input handling, cancellation rollback and teardown are unresolved. Schema persistence vocabulary does not resolve these behaviors. No failure response, silence, continuity, reset, equality, timing or accepted-input policy is asserted.

## Redux

### REQ-DST-REDUX-001 — installed representation

**Dpkg** (schema-fields.json#class=Redux2, package-values.json#class=Redux2). The pinned schema declares Redux2; the frozen single shipped preset has /Ableton/Redux2. Its Creator is historical Ableton Live 12.4d1 and MinorVersion is 12.0_12402. Exact field records are in schema-fields.json and package-values.json. These facts establish vocabulary and one stored example only; neither constructor defaults, GUI bounds, automation legality, model indices nor DSP are inferred.

### REQ-DST-REDUX-002 — downsampling rate and jitter

**D12** (manual-redux-blocks.json#redux:B003, manual-redux-blocks.json#redux:B005, manual-redux-blocks.json#redux:B006, manual-redux-blocks.json#redux:B007). Rate selects a degraded sample rate; reducing it can add imaging/inharmonic content depending on source spectrum. Jitter randomizes the downsample clock and can add noise/stereo spread. Exact resampling phase, algorithm, noise distribution and stereo correlation are U.

### REQ-DST-REDUX-003 — pre/post filters

**D12** (manual-redux-blocks.json#redux:B008, manual-redux-blocks.json#redux:B009). Pre filters before downsampling, reducing bandwidth and also stereo width when Jitter is used. Post low-passes after downsampling to reduce imaging. Post-Filter Octave expresses octaves relative to half the displayed Rate; no exact filter slope or Nyquist clipping law follows.

### REQ-DST-REDUX-004 — bits and shape

**D12** (manual-redux-blocks.json#redux:B011, manual-redux-blocks.json#redux:B012, manual-redux-blocks.json#redux:B013). Bits describes the encoding bit count; reducing it reduces dynamic range and adds quantization noise/distortion. Higher Shape allocates finer resolution to smaller amplitudes; its net effect depends on input dynamics. Rounding, saturation, dithering and compander formula are U.

### REQ-DST-REDUX-005 — DC offset and wet balance

**D12** (manual-redux-blocks.json#redux:B014, manual-redux-blocks.json#redux:B015). DC Shift offsets amplitude before quantization, changing low-bit distortion. Dry/Wet balances processed/dry paths, with 100% documented for returns. Offset magnitude, DC removal, integer conventions and mix law are U.

### REQ-DST-REDUX-006 — legacy and unmatched state

**U** (packet limits). Current Redux2 controls do not establish Redux Legacy behavior, old-Set migration or the semantics of the stored EcoProcessing field. No exposed control or processing-performance law is inferred from that field.

### REQ-DST-REDUX-007 — automation, state, errors and teardown

**U** (packet limits). For Redux, exact parameter automation/clip-modulation/macro precedence, mode-change smoothing, sample/block-rate behavior, transport history, preset/Set reopen and migration, undo/redo transactions, malformed/invalid input handling, cancellation rollback and teardown are unresolved. Schema persistence vocabulary does not resolve these behaviors. No failure response, silence, continuity, reset, equality, timing or accepted-input policy is asserted.

## Roar

### REQ-DST-ROAR-001 — installed representation

**Dpkg** (schema-fields.json#class=Roar, package-values.json#class=Roar). The pinned schema declares Roar; the frozen single shipped preset has /Ableton/Roar. Its Creator is historical Ableton Live 12.4d1 and MinorVersion is 12.0_12402. Exact field records are in schema-fields.json and package-values.json. These facts establish vocabulary and one stored example only; neither constructor defaults, GUI bounds, automation legality, model indices nor DSP are inferred.

### REQ-DST-ROAR-002 — input and color compensation

**D12** (manual-roar-blocks.json#roar:B004, manual-roar-blocks.json#roar:B005, manual-roar-blocks.json#roar:B006, manual-roar-blocks.json#roar:B007, manual-roar-blocks.json#roar:B008). Drive controls input level before gain stages. Positive Tone tilts toward highs and negative Tone toward lows; Tone Frequency sets its low shelf frequency. Color Compensation applies a mirrored filter after distortion stages to complement pre-shaper coloring. No exact inverse transfer or level normalization is inferred.

### REQ-DST-ROAR-003 — routing modes

**D12** (manual-roar-blocks.json#roar:B009, manual-roar-blocks.json#roar:B010, manual-roar-blocks.json#roar:B011, manual-roar-blocks.json#roar:B012, manual-roar-blocks.json#roar:B013, manual-roar-blocks.json#roar:B014, manual-roar-blocks.json#roar:B015). Seven routing modes are documented. Single uses one stage. Serial concatenates two, with Blend between stage 1 and the combined result. Parallel independently processes two, with Blend between their outputs. Multi Band splits Low/Mid/High with two crossovers. Mid Side processes mono/stereo content separately. Feedback separately processes input and feedback. Delay sends a delayed stage-1 signal into stage 2 without feedback-gain scaling on that first repeat; stage-2 output feeds back with gain. All except Single and Multi Band have Blend. Crossover law, blend law, exact feedback topology and delays are U.

### REQ-DST-ROAR-004 — gain-stage controls

**D12** (manual-roar-blocks.json#roar:B017, manual-roar-blocks.json#roar:B018, manual-roar-blocks.json#roar:B019, manual-roar-blocks.json#roar:B020, manual-roar-blocks.json#roar:B033, manual-roar-blocks.json#roar:B034). Available gain stages have independent Stage on/off, shaper on/off, Shaper Amount, Shaper Bias and Filter Frequency. Amount can be dragged on the shaper visualization. Bias offsets the signal to produce asymmetry and can silence output at unspecified extremes. Shaper Level compensates output changes manually; no automatic loudness matching is implied.

### REQ-DST-ROAR-005 — twelve shapers

**D12** (manual-roar-blocks.json#roar:B021, manual-roar-blocks.json#roar:B022, manual-roar-blocks.json#roar:B023, manual-roar-blocks.json#roar:B024, manual-roar-blocks.json#roar:B025, manual-roar-blocks.json#roar:B026, manual-roar-blocks.json#roar:B027, manual-roar-blocks.json#roar:B028, manual-roar-blocks.json#roar:B029, manual-roar-blocks.json#roar:B030, manual-roar-blocks.json#roar:B031, manual-roar-blocks.json#roar:B032). The shaper list contains Soft Sine, Digital Clip, Bit Crusher, Diode Clipper, Tube Preamp, Half Wave Rectifier, Full Wave Rectifier, Polynomial, Fractal, Tri Fold, Noise Injection and Shards. Their documented characters include soft/hard clipping, quantization/companding, asymmetry/rectification, folding and noise/time-varying shapes. Names and visualization do not establish transfer functions, harmonic amplitudes, seeds or equality to other devices.

### REQ-DST-ROAR-006 — filters and order

**D12** (manual-roar-blocks.json#roar:B035, manual-roar-blocks.json#roar:B036, manual-roar-blocks.json#roar:B037, manual-roar-blocks.json#roar:B038, manual-roar-blocks.json#roar:B039, manual-roar-blocks.json#roar:B040, manual-roar-blocks.json#roar:B041, manual-roar-blocks.json#roar:B042, manual-roar-blocks.json#roar:B043). Filter types are LP, BP, HP, Notch, Peak, Morph, Comb, Resampling and Dispersion. Pre places the filter before the shaper, so it does not directly filter newly generated harmonics. All except Resampling have Resonance; Peak has Peak Gain and Morph has a morph parameter. LP/BP/HP/Notch/Comb give their named attenuation forms; Morph moves LP through BP toward HP; Dispersion shifts frequency-dependent timing without documented level change. Filter coefficients, order, resonance limits and phase response remain U.

### REQ-DST-ROAR-007 — LFO sources and timing

**D12** (manual-roar-blocks.json#roar:B045, manual-roar-blocks.json#roar:B046, manual-roar-blocks.json#roar:B047, manual-roar-blocks.json#roar:B048). The Mod Sources/Matrix panel is opened by its toggle. LFO1 and LFO2 select sine, triangle, square, up or down. Rate modes are Free, Synced, Triplet, Dotted and Sixteenth; Free uses Hertz and others beat divisions. Morph sculpts shape and Smooth smooths transitions. Initial phase, sync reset, tempo-change response and numerical waveforms are U.

### REQ-DST-ROAR-008 — envelope follower and listen

**D12** (manual-roar-blocks.json#roar:B049, manual-roar-blocks.json#roar:B050, manual-roar-blocks.json#roar:B051, manual-roar-blocks.json#roar:B052, manual-roar-blocks.json#roar:B053). The follower tracks input with Attack/Release. Hold completes attack before release. Threshold and Gain set sensitivity/strength; Frequency/Width select its analysis band. Envelope Input Listen auditions that input. Exact detector/window/timing and listen routing beyond the documented audition remain U.

### REQ-DST-ROAR-009 — noise source

**D12** (manual-roar-blocks.json#roar:B054, manual-roar-blocks.json#roar:B055, manual-roar-blocks.json#roar:B056, manual-roar-blocks.json#roar:B057). Noise types are Simplex, Wander, S & H and Brown. Rates can be Hertz or tempo-synced and smoothed. Simplex/Wander are differently interpolated random signals; S & H changes a held random value per Noise Rate interval; Brown is low-passed white noise. Exact PRNG, distribution, shared seed, rate/tempo reset and noise bandwidth are U.

### REQ-DST-ROAR-010 — matrix editing and display

**D12** (manual-roar-blocks.json#roar:B058, manual-roar-blocks.json#roar:B059, manual-roar-blocks.json#roar:B060, manual-roar-blocks.json#roar:B061). With Matrix open, clicking a parameter selects a target; sources form columns and targets rows. Vertical cell drag changes assignment amount. Global Modulation Amount scales overall application. X clears matrix assignments. Header expansion exposes all stages and matrix targets/sources; LEDs indicate source activity with source-associated color. Undo, modulation sum, clipping, destination units and zero-depth identity remain U.

### REQ-DST-ROAR-011 — feedback modes and processing

**D12** (manual-roar-blocks.json#roar:B064, manual-roar-blocks.json#roar:B065, manual-roar-blocks.json#roar:B066, manual-roar-blocks.json#roar:B067, manual-roar-blocks.json#roar:B068). Feedback modes are Time, Synced, Triplet, Dotted and Note; Note sets a pitched feedback ring. Feedback Amount sets reinjection; in-loop compression can attenuate feedback on loud input. Invert reverses feedback polarity. Gate on fades feedback after input ceases; Gate off permits indefinite feedback. Frequency/Width set a feedback band-pass. Infinite duration is conditional on established nonzero feedback and sustaining path; no decay rate, stability, tail threshold or silence-generation guarantee follows.

### REQ-DST-ROAR-012 — global compression and output

**D12** (manual-roar-blocks.json#roar:B070, manual-roar-blocks.json#roar:B071, manual-roar-blocks.json#roar:B072, manual-roar-blocks.json#roar:B073). Compression Amount controls output compression and hence feedback. Sidechain HP filters the compressor analysis signal to reduce low-frequency response. Output Gain sets wet level followed by hard clipping, then Dry/Wet balance. Neither clip threshold, gain law, compressor constants nor final-output peak under dry mixing is specified.

### REQ-DST-ROAR-013 — external audio sidechain

**D12** (manual-roar-blocks.json#roar:B075, manual-roar-blocks.json#roar:B076, manual-roar-blocks.json#roar:B077, manual-roar-blocks.json#roar:B078, manual-roar-blocks.json#roar:B081). The default follower source is main input. External SC enables a selectable external source and Post FX/Post Mixer tap. Mix=100% follows only external, 0% only internal. SC Gain changes analysis level without changing the source track volume. Sidechain Listen bypasses Roar output to audition the sidechain. Missing source, feedback during listen, tap latency and changes during routing are U.

### REQ-DST-ROAR-014 — MIDI feedback note

**D12** (manual-roar-blocks.json#roar:B079, manual-roar-blocks.json#roar:B080). MIDI > FB Note uses a selected MIDI source, Pre FX/Post FX tap, and MIDI to set feedback pitch in Note mode. The manual says Feedback Mode and Feedback Amount are inactive while MIDI sidechain is active. Note priority, channel, velocity, transpose, note-off, sustain and held-note teardown are U.

### REQ-DST-ROAR-015 — unmatched installed controls

**U** (packet limits). Stored HiQuality, SteppedDiscreteParameterModulation and other schema members do not independently establish exposed controls, automation steps, DSP quality or latency. Mode switching and automation of discrete controls remain unknown at exact build.

### REQ-DST-ROAR-016 — automation, state, errors and teardown

**U** (packet limits). For Roar, exact parameter automation/clip-modulation/macro precedence, mode-change smoothing, sample/block-rate behavior, transport history, preset/Set reopen and migration, undo/redo transactions, malformed/invalid input handling, cancellation rollback and teardown are unresolved. Schema persistence vocabulary does not resolve these behaviors. No failure response, silence, continuity, reset, equality, timing or accepted-input policy is asserted.

## Saturator

### REQ-DST-SATURATOR-001 — installed representation

**Dpkg** (schema-fields.json#class=Saturator, package-values.json#class=Saturator). The pinned schema declares Saturator; the frozen single shipped preset has /Ableton/Saturator. Its Creator is historical Ableton Live 12.4d1 and MinorVersion is 12.0_12402. Exact field records are in schema-fields.json and package-values.json. These facts establish vocabulary and one stored example only; neither constructor defaults, GUI bounds, automation legality, model indices nor DSP are inferred.

### REQ-DST-SATURATOR-002 — eight curves and visualization

**D12** (manual-saturator-blocks.json#saturator:B003, manual-saturator-blocks.json#saturator:B004, manual-saturator-blocks.json#saturator:B005, manual-saturator-blocks.json#saturator:B006, manual-saturator-blocks.json#saturator:B008, manual-saturator-blocks.json#saturator:B009). Curve choices are Analog Clip, Soft Sine, Bass Shaper, Medium Curve, Hard Curve, Sinoid Fold, Digital Clip and Waveshaper. Analog/Digital Clip are documented linear below an unspecified clipping point, with smoother versus immediate transition. Sinoid Fold folds at increasing input. Shaper Curve display relates live input to the curve; exact transfer functions and clipping levels are U.

### REQ-DST-SATURATOR-003 — bass threshold

**D12** (manual-saturator-blocks.json#saturator:B007). Bass Shaper has a displayed threshold from 0 to -50 dB. Below threshold it is documented linear; above it clipping increases smoothly. Lower thresholds give softer clipping, higher thresholds harder clipping. Input/drive normalization, exact dB reference, continuity and quantitative curve remain U.

### REQ-DST-SATURATOR-004 — color filters and drive

**D12** (manual-saturator-blocks.json#saturator:B011, manual-saturator-blocks.json#saturator:B012, manual-saturator-blocks.json#saturator:B013, manual-saturator-blocks.json#saturator:B016, manual-saturator-blocks.json#saturator:B017, manual-saturator-blocks.json#saturator:B018). Drive sets pre-shaper input gain. Color enables EQ before shaping and an inverted counterpart after it. Amt Lo addresses low-frequency saturation; Amt Hi, Frequency and Width address a second band. Positive amounts increase saturation and negatives reduce it in their band. Expanded curve handles address Amt Lo and Amt Hi/Frequency. No exact EQ cancellation or filter law follows.

### REQ-DST-SATURATOR-005 — post clip and output

**D12** (manual-saturator-blocks.json#saturator:B010, manual-saturator-blocks.json#saturator:B014, manual-saturator-blocks.json#saturator:B015). Post Clip Mode can select Soft Clip or Hard Clip for all curve types; the manual bounds output by the Output setting in these modes. Soft Clip applies an Analog Clip instance to the output. Dry/Wet balances dry/processed signals, with 100% for returns. This does not assert a peak bound on a mixture containing an unconstrained dry path; threshold, normalization and precision remain U.

### REQ-DST-SATURATOR-006 — waveshaper controls and zero influence

**D12** (manual-saturator-blocks.json#saturator:B020, manual-saturator-blocks.json#saturator:B022, manual-saturator-blocks.json#saturator:B023, manual-saturator-blocks.json#saturator:B024, manual-saturator-blocks.json#saturator:B025, manual-saturator-blocks.json#saturator:B026, manual-saturator-blocks.json#saturator:B027). Waveshaper activates six expanded controls. Waveshaper Drive sets their influence: 0% removes their curve influence and 100% fully applies it. Curve adds mainly third harmonics; Depth superposes a sine component with no influence at 0%; Linear changes the linear region jointly with Curve/Depth; Damp flattens near center; Period sets ripple density relative to Depth. This Drive is distinct from main input Drive. Equations, inactive-control persistence and no-effect equality tolerances remain U.

### REQ-DST-SATURATOR-007 — context quality and input DC filter

**D12** (manual-saturator-blocks.json#saturator:B029). The context menu exposes Hi-Quality and Pre-DC Filter. Hi-Quality reduces aliasing with higher CPU cost; Pre-DC Filter removes input DC offsets. Factor, kernels, transient response, attenuation, latency and CPU metric remain U.

### REQ-DST-SATURATOR-008 — automation, state, errors and teardown

**U** (packet limits). For Saturator, exact parameter automation/clip-modulation/macro precedence, mode-change smoothing, sample/block-rate behavior, transport history, preset/Set reopen and migration, undo/redo transactions, malformed/invalid input handling, cancellation rollback and teardown are unresolved. Schema persistence vocabulary does not resolve these behaviors. No failure response, silence, continuity, reset, equality, timing or accepted-input policy is asserted.

## Vinyl Distortion

### REQ-DST-VINYL-DISTORTION-001 — installed representation

**Dpkg** (schema-fields.json#class=Vinyl, package-values.json#class=Vinyl). The pinned schema declares Vinyl; the frozen single shipped preset has /Ableton/Vinyl. Its Creator is historical Ableton Live 12.4d1 and MinorVersion is 12.0_12402. Exact field records are in schema-fields.json and package-values.json. These facts establish vocabulary and one stored example only; neither constructor defaults, GUI bounds, automation legality, model indices nor DSP are inferred.

### REQ-DST-VINYL-DISTORTION-002 — tracing and pinch bands

**D12** (manual-vinyl-distortion-blocks.json#vinyl-distortion:B003, manual-vinyl-distortion-blocks.json#vinyl-distortion:B004, manual-vinyl-distortion-blocks.json#vinyl-distortion:B005). Tracing Model adds even harmonics; Pinch adds odd harmonics, typically opposing in phase between channels. Each band has Drive, Freq and Q: vertical XY changes Drive, horizontal changes Freq, and Alt/Option vertical changes Q. Overall Drive changes both models. Exact harmonic/phase laws, band activation and distortion transfer remain U.

### REQ-DST-VINYL-DISTORTION-003 — mode and pinch stereo

**D12** (manual-vinyl-distortion-blocks.json#vinyl-distortion:B006, manual-vinyl-distortion-blocks.json#vinyl-distortion:B007). Soft and Hard are distinct vinyl-distortion modes. Stereo/mono determines whether Pinch distortion is stereo or mono. No disk-speed model, transfer curve, stereo gain law or broad input downmixing rule is inferred.

### REQ-DST-VINYL-DISTORTION-004 — crackle generator

**D12** (manual-vinyl-distortion-blocks.json#vinyl-distortion:B002, manual-vinyl-distortion-blocks.json#vinyl-distortion:B008). Crackle adds generated noise. Density sets noise density, while Volume changes noise gain independently of harmonic distortion controls. Exact event distribution, seed, spectrum, density-zero output, silence behavior and channel relation are U.

### REQ-DST-VINYL-DISTORTION-005 — automation, state, errors and teardown

**U** (packet limits). For Vinyl Distortion, exact parameter automation/clip-modulation/macro precedence, mode-change smoothing, sample/block-rate behavior, transport history, preset/Set reopen and migration, undo/redo transactions, malformed/invalid input handling, cancellation rollback and teardown are unresolved. Schema persistence vocabulary does not resolve these behaviors. No failure response, silence, continuity, reset, equality, timing or accepted-input policy is asserted.

## Finite acceptance cases

The [cases JSON](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/cases.json)
is the machine-readable copy of this table, with execution/comparison metadata.
Dpkg grades source bytes only. D12 grades the documented UI/state domain only;
exact-build applicability remains U. All execution is unexecuted. U expected
values are null, never zero, true, pass, a presumed rejection or a tolerance.
Positive/negative labels describe scenario purpose, not execution outcome.

| Case | Requirement | Kind / evidence | Concrete setup and action | Expected comparator |
| --- | --- | --- | --- | --- |
| DST-DRUM-BUSS-001 | REQ-DST-DRUM-BUSS-001 | positive / Dpkg | Parse exact PKG-SCHEMA bytes and select class DrumBuss; compare all declared fields and class start line with schema-fields.json. | Exact class, line and field attributes match retained source. |
| DST-DRUM-BUSS-002 | REQ-DST-DRUM-BUSS-001 | persistence / Dpkg | Decode frozen package preset for Drum Buss; inspect /Ableton/DrumBuss, root attributes and recorded field XML. | Exact class/root attributes/field XML match package-values.json; no load/save behavior asserted. |
| DST-DRUM-BUSS-003 | REQ-DST-DRUM-BUSS-002 | positive / D12 | Open Drum Buss, enumerate distortion choices, toggle Comp and adjust Trim and Drive. | Soft, Medium and Hard are available; Comp, Trim and Drive are separately addressable controls. |
| DST-DRUM-BUSS-004 | REQ-DST-DRUM-BUSS-003 | positive / U | Use S2 with Boom=0, change Crunch, Damp and Transients independently through negative, zero and positive displayed values; establish active-path prerequisites and capture envelope/spectrum. | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-005 | REQ-DST-DRUM-BUSS-004 | boundary / D12 | Set Freq to a displayed non-note value, invoke Force To Note; set Boom to 0% and then 50%, changing Decay at each. | Force To Note is exposed and updates Freq to a note frequency; Boom and Decay remain separate controls. Exact frequency and all audio outcomes U. |
| DST-DRUM-BUSS-006 | REQ-DST-DRUM-BUSS-005 | positive / U | With Boom=50% and independently established resonant output, toggle Boom Audition; then compare Dry/Wet=0%,50%,100% and Output=-12 dB,0 dB using S2. | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-007 | REQ-DST-DRUM-BUSS-006 | automation / U | {"signal": "S2", "parameter": "DriveAmount", "sequence": ["record current displayed value", "automate at0s,0.5s,1s using recorded legal low/mid/high values", "apply opposing clip modulation", "perform manual edit", "re-enable automation", "map to rack macro and repeat"], "observe": ["effective control ownership", "undo grouping", "audio discontinuity", "stage/mode gating"]} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-008 | REQ-DST-DRUM-BUSS-006 | boundary / U | {"signal": "S1", "sequence": ["record displayed control endpoints and current factory state", "enter each endpoint and one display step inside", "switch every mode at each endpoint", "set all documented zero/inactive depths", "restore captured starting state"], "observe": ["accepted domain", "disabled controls", "retained values", "audio stability"], "numeric_parameter": "DriveAmount"} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-009 | REQ-DST-DRUM-BUSS-006 | persistence / U | {"sequence": ["load retained named preset copy", "record all controls/modes/quality/routing and matrix assignments if present", "save new Set and new preset", "close and reopen each", "compare displayed/stored state and audible continuation"], "observe": ["loss/migration", "source identity", "modulation memory", "tail/random state"], "not_a_default": "The retained named preset is not an initialized constructor."} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-010 | REQ-DST-DRUM-BUSS-006 | undo / U | {"sequence": ["record all controls", "change numeric control, mode if present, quality/routing if present", "Undo each action", "Redo each action", "delete device and Undo"], "observe": ["transaction grouping", "restored identity/state", "automation references", "audible tail/seed"]} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-011 | REQ-DST-DRUM-BUSS-006 | malformed / U | {"base": "frozen preset copy; never modify retained bytes", "mutations": ["truncate decompressed XML at midpoint", "set DriveAmount/Manual/@Value to NaN", "set DriveAmount/Manual/@Value to 1e309", "remove device element", "set DriveType/Manual/@Value to999"], "observe": ["rejection/repair", "error text", "prior-state mutation", "partial processing"]} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-012 | REQ-DST-DRUM-BUSS-006 | negative / U | {"parameter": "DriveAmount", "sequence": ["enter text nan", "enter 1e309", "enter empty text", "enter just outside displayed legal bounds"], "observe": ["accepted/clamped/rejected state", "error", "undo"], "note": "UI entry and malformed-file loading are different trust boundaries."} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-013 | REQ-DST-DRUM-BUSS-006 | cancellation / U | {"sequence": ["start preset replacement and cancel chooser before selection", "enter hot-swap and exit without selection", "start numeric drag and press Escape before release"], "observe": ["restoration versus commit", "undo entry", "focus", "partial routing/state mutation"]} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-014 | REQ-DST-DRUM-BUSS-006 | transport / U | {"signal": "S2", "sequence": ["play from0s", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s three times"], "observe": ["follower/history reset", "buffer content", "feedback/generator/phase continuity if present", "first output samples"]} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-015 | REQ-DST-DRUM-BUSS-006 | rate / U | {"signal": "S1 and S2 regenerated at each host rate", "host_sample_rates_hz": [44100, 48000, 96000], "block_sizes": [64, 512], "sequence": ["record control values and warmup", "process identical-duration inputs", "change rate/block while active if host permits", "compare real-time and offline export"], "observe": ["rate-dependent state", "latency", "aliasing", "random stream", "reset/error"], "device_rate_not_host_rate": true} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-016 | REQ-DST-DRUM-BUSS-006 | teardown / U | {"signal": "S2", "sequence": ["process nonzero input with automation and audible wet path", "delete device during playback", "Undo deletion", "close Set during processing"], "observe": ["tail/feedback/noise cessation", "stale references", "automation restoration", "error/hang"], "routing": "No device-specific external sidechain is established by this manual section."} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-017 | REQ-DST-DRUM-BUSS-006 | negative / U | {"signal": "S0 then S1", "sequence": ["activate then bypass device", "compare silent input and active signal", "toggle processed/dry endpoints only if a control is independently available", "isolate direct/return/rack paths"], "observe": ["bypass latency", "generator tails", "state memory", "wet output"], "prerequisite": "Apply P-AUDIO independently for any effect or no-effect claim; no silence implies bypass or absent algorithm."} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-001 | REQ-DST-DYNAMIC-TUBE-001 | positive / Dpkg | Parse exact PKG-SCHEMA bytes and select class Tube; compare all declared fields and class start line with schema-fields.json. | Exact class, line and field attributes match retained source. |
| DST-DYNAMIC-TUBE-002 | REQ-DST-DYNAMIC-TUBE-001 | persistence / Dpkg | Decode frozen package preset for Dynamic Tube; inspect /Ableton/Tube, root attributes and recorded field XML. | Exact class/root attributes/field XML match package-values.json; no load/save behavior asserted. |
| DST-DYNAMIC-TUBE-003 | REQ-DST-DYNAMIC-TUBE-002 | positive / D12 | Enumerate A/B/C and adjust Drive, Bias and Tone separately. | A, B and C are selectable; Drive, Bias and Tone are separate controls. |
| DST-DYNAMIC-TUBE-004 | REQ-DST-DYNAMIC-TUBE-003 | positive / U | Use S2 and record negative, zero and positive Envelope settings at fixed nonzero Drive/Bias; establish follower response and wet distortion baselines before comparing. | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-005 | REQ-DST-DYNAMIC-TUBE-004 | boundary / U | At Envelope=0, compare minimum and maximum displayed Attack and Release with S2. Positive baseline: at a nonzero Envelope, establish that both controls affect an active follower path; hold Bias/Drive/model/output fixed. If baseline fails remain U. | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-006 | REQ-DST-DYNAMIC-TUBE-005 | positive / D12 | Open title context menu and toggle Hi-Quality; adjust Output. | Hi-Quality is a context-menu option; Output is separately adjustable. |
| DST-DYNAMIC-TUBE-007 | REQ-DST-DYNAMIC-TUBE-006 | automation / U | {"signal": "S2", "parameter": "Bias", "sequence": ["record current displayed value", "automate at0s,0.5s,1s using recorded legal low/mid/high values", "apply opposing clip modulation", "perform manual edit", "re-enable automation", "map to rack macro and repeat"], "observe": ["effective control ownership", "undo grouping", "audio discontinuity", "stage/mode gating"]} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-008 | REQ-DST-DYNAMIC-TUBE-006 | boundary / U | {"signal": "S1", "sequence": ["record displayed control endpoints and current factory state", "enter each endpoint and one display step inside", "switch every mode at each endpoint", "set all documented zero/inactive depths", "restore captured starting state"], "observe": ["accepted domain", "disabled controls", "retained values", "audio stability"], "numeric_parameter": "Bias"} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-009 | REQ-DST-DYNAMIC-TUBE-006 | persistence / U | {"sequence": ["load retained named preset copy", "record all controls/modes/quality/routing and matrix assignments if present", "save new Set and new preset", "close and reopen each", "compare displayed/stored state and audible continuation"], "observe": ["loss/migration", "source identity", "modulation memory", "tail/random state"], "not_a_default": "The retained named preset is not an initialized constructor."} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-010 | REQ-DST-DYNAMIC-TUBE-006 | undo / U | {"sequence": ["record all controls", "change numeric control, mode if present, quality/routing if present", "Undo each action", "Redo each action", "delete device and Undo"], "observe": ["transaction grouping", "restored identity/state", "automation references", "audible tail/seed"]} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-011 | REQ-DST-DYNAMIC-TUBE-006 | malformed / U | {"base": "frozen preset copy; never modify retained bytes", "mutations": ["truncate decompressed XML at midpoint", "set Bias/Manual/@Value to NaN", "set Bias/Manual/@Value to 1e309", "remove device element", "set Type/Manual/@Value to999"], "observe": ["rejection/repair", "error text", "prior-state mutation", "partial processing"]} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-012 | REQ-DST-DYNAMIC-TUBE-006 | negative / U | {"parameter": "Bias", "sequence": ["enter text nan", "enter 1e309", "enter empty text", "enter just outside displayed legal bounds"], "observe": ["accepted/clamped/rejected state", "error", "undo"], "note": "UI entry and malformed-file loading are different trust boundaries."} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-013 | REQ-DST-DYNAMIC-TUBE-006 | cancellation / U | {"sequence": ["start preset replacement and cancel chooser before selection", "enter hot-swap and exit without selection", "start numeric drag and press Escape before release"], "observe": ["restoration versus commit", "undo entry", "focus", "partial routing/state mutation"]} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-014 | REQ-DST-DYNAMIC-TUBE-006 | transport / U | {"signal": "S2", "sequence": ["play from0s", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s three times"], "observe": ["follower/history reset", "buffer content", "feedback/generator/phase continuity if present", "first output samples"]} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-015 | REQ-DST-DYNAMIC-TUBE-006 | rate / U | {"signal": "S1 and S2 regenerated at each host rate", "host_sample_rates_hz": [44100, 48000, 96000], "block_sizes": [64, 512], "sequence": ["record control values and warmup", "process identical-duration inputs", "change rate/block while active if host permits", "compare real-time and offline export"], "observe": ["rate-dependent state", "latency", "aliasing", "random stream", "reset/error"], "device_rate_not_host_rate": true} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-016 | REQ-DST-DYNAMIC-TUBE-006 | teardown / U | {"signal": "S2", "sequence": ["process nonzero input with automation and audible wet path", "delete device during playback", "Undo deletion", "close Set during processing"], "observe": ["tail/feedback/noise cessation", "stale references", "automation restoration", "error/hang"], "routing": "No device-specific external sidechain is established by this manual section."} | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-017 | REQ-DST-DYNAMIC-TUBE-006 | negative / U | {"signal": "S0 then S1", "sequence": ["activate then bypass device", "compare silent input and active signal", "toggle processed/dry endpoints only if a control is independently available", "isolate direct/return/rack paths"], "observe": ["bypass latency", "generator tails", "state memory", "wet output"], "prerequisite": "Apply P-AUDIO independently for any effect or no-effect claim; no silence implies bypass or absent algorithm."} | U — expected outcome null; ungraded. |
| DST-EROSION-001 | REQ-DST-EROSION-001 | positive / Dpkg | Parse exact PKG-SCHEMA bytes and select class Erosion2; compare all declared fields and class start line with schema-fields.json. | Exact class, line and field attributes match retained source. |
| DST-EROSION-002 | REQ-DST-EROSION-001 | persistence / Dpkg | Decode frozen package preset for Erosion; inspect /Ableton/Erosion2, root attributes and recorded field XML. | Exact class/root attributes/field XML match package-values.json; no load/save behavior asserted. |
| DST-EROSION-003 | REQ-DST-EROSION-002 | positive / D12 | Play S1; drag display X and Y separately, then modifier-drag Y. | Ordinary X changes Freq; ordinary Y changes Amount; modifier Y changes Filter Width. Spectrum/modulation presentation is available during playback. |
| DST-EROSION-004 | REQ-DST-EROSION-003 | boundary / D12 | Set Noise Blend to 0%,50%,100%; inspect Filter Width and carrier icons. | At 0% Filter Width is gray; sine and noise indicators change relative prominence with blend. |
| DST-EROSION-005 | REQ-DST-EROSION-003 | negative / U | At Blend=0%, vary stored/automated Filter Width using S1. First establish audible noise-width effect at Blend=100%, Amount>0, active wet path. Isolate mono/stereo and carrier blend; no established baseline means U. | U — expected outcome null; ungraded. |
| DST-EROSION-006 | REQ-DST-EROSION-004 | positive / U | With nonzero Amount and Noise Blend=100%, test Stereo Width=0%,50%,100% on identical-channel S1; establish width-sensitive nonmuted modulation first. | U — expected outcome null; ungraded. |
| DST-EROSION-007 | REQ-DST-EROSION-005 | persistence / U | Obtain separately pinned pre-12.4 Set with Erosion and a current Erosion2 Set; load copies and inspect device identity, values, saving and undo. No qualifying old Set is retained here. | U — expected outcome null; ungraded. |
| DST-EROSION-008 | REQ-DST-EROSION-006 | automation / U | {"signal": "S2", "parameter": "NoiseBlend", "sequence": ["record current displayed value", "automate at0s,0.5s,1s using recorded legal low/mid/high values", "apply opposing clip modulation", "perform manual edit", "re-enable automation", "map to rack macro and repeat"], "observe": ["effective control ownership", "undo grouping", "audio discontinuity", "stage/mode gating"]} | U — expected outcome null; ungraded. |
| DST-EROSION-009 | REQ-DST-EROSION-006 | boundary / U | {"signal": "S1", "sequence": ["record displayed control endpoints and current factory state", "enter each endpoint and one display step inside", "switch every mode at each endpoint", "set all documented zero/inactive depths", "restore captured starting state"], "observe": ["accepted domain", "disabled controls", "retained values", "audio stability"], "numeric_parameter": "NoiseBlend"} | U — expected outcome null; ungraded. |
| DST-EROSION-010 | REQ-DST-EROSION-006 | persistence / U | {"sequence": ["load retained named preset copy", "record all controls/modes/quality/routing and matrix assignments if present", "save new Set and new preset", "close and reopen each", "compare displayed/stored state and audible continuation"], "observe": ["loss/migration", "source identity", "modulation memory", "tail/random state"], "not_a_default": "The retained named preset is not an initialized constructor."} | U — expected outcome null; ungraded. |
| DST-EROSION-011 | REQ-DST-EROSION-006 | undo / U | {"sequence": ["record all controls", "change numeric control, mode if present, quality/routing if present", "Undo each action", "Redo each action", "delete device and Undo"], "observe": ["transaction grouping", "restored identity/state", "automation references", "audible tail/seed"]} | U — expected outcome null; ungraded. |
| DST-EROSION-012 | REQ-DST-EROSION-006 | malformed / U | {"base": "frozen preset copy; never modify retained bytes", "mutations": ["truncate decompressed XML at midpoint", "set NoiseBlend/Manual/@Value to NaN", "set NoiseBlend/Manual/@Value to 1e309", "remove device element"], "observe": ["rejection/repair", "error text", "prior-state mutation", "partial processing"]} | U — expected outcome null; ungraded. |
| DST-EROSION-013 | REQ-DST-EROSION-006 | negative / U | {"parameter": "NoiseBlend", "sequence": ["enter text nan", "enter 1e309", "enter empty text", "enter just outside displayed legal bounds"], "observe": ["accepted/clamped/rejected state", "error", "undo"], "note": "UI entry and malformed-file loading are different trust boundaries."} | U — expected outcome null; ungraded. |
| DST-EROSION-014 | REQ-DST-EROSION-006 | cancellation / U | {"sequence": ["start preset replacement and cancel chooser before selection", "enter hot-swap and exit without selection", "start numeric drag and press Escape before release"], "observe": ["restoration versus commit", "undo entry", "focus", "partial routing/state mutation"]} | U — expected outcome null; ungraded. |
| DST-EROSION-015 | REQ-DST-EROSION-006 | transport / U | {"signal": "S2", "sequence": ["play from0s", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s three times"], "observe": ["follower/history reset", "buffer content", "feedback/generator/phase continuity if present", "first output samples"]} | U — expected outcome null; ungraded. |
| DST-EROSION-016 | REQ-DST-EROSION-006 | rate / U | {"signal": "S1 and S2 regenerated at each host rate", "host_sample_rates_hz": [44100, 48000, 96000], "block_sizes": [64, 512], "sequence": ["record control values and warmup", "process identical-duration inputs", "change rate/block while active if host permits", "compare real-time and offline export"], "observe": ["rate-dependent state", "latency", "aliasing", "random stream", "reset/error"], "device_rate_not_host_rate": true} | U — expected outcome null; ungraded. |
| DST-EROSION-017 | REQ-DST-EROSION-006 | teardown / U | {"signal": "S2", "sequence": ["process nonzero input with automation and audible wet path", "delete device during playback", "Undo deletion", "close Set during processing"], "observe": ["tail/feedback/noise cessation", "stale references", "automation restoration", "error/hang"], "routing": "No device-specific external sidechain is established by this manual section."} | U — expected outcome null; ungraded. |
| DST-EROSION-018 | REQ-DST-EROSION-006 | negative / U | {"signal": "S0 then S1", "sequence": ["activate then bypass device", "compare silent input and active signal", "toggle processed/dry endpoints only if a control is independently available", "isolate direct/return/rack paths"], "observe": ["bypass latency", "generator tails", "state memory", "wet output"], "prerequisite": "Apply P-AUDIO independently for any effect or no-effect claim; no silence implies bypass or absent algorithm."} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-001 | REQ-DST-OVERDRIVE-001 | positive / Dpkg | Parse exact PKG-SCHEMA bytes and select class Overdrive; compare all declared fields and class start line with schema-fields.json. | Exact class, line and field attributes match retained source. |
| DST-OVERDRIVE-002 | REQ-DST-OVERDRIVE-001 | persistence / Dpkg | Decode frozen package preset for Overdrive; inspect /Ableton/Overdrive, root attributes and recorded field XML. | Exact class/root attributes/field XML match package-values.json; no load/save behavior asserted. |
| DST-OVERDRIVE-003 | REQ-DST-OVERDRIVE-002 | positive / D12 | Drag XY horizontally then vertically and compare corresponding slider boxes. | Horizontal movement addresses filter frequency; vertical movement addresses bandwidth. |
| DST-OVERDRIVE-004 | REQ-DST-OVERDRIVE-003 | boundary / U | At Drive=0%, use S1 at several levels with Tone held fixed and Dry/Wet=100%; require independent nonlinear-path baseline. Repeat Drive=50%,100% and lower/higher Tone. | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-005 | REQ-DST-OVERDRIVE-004 | positive / U | Use S2 at Dynamics=0%,50%,100%, Drive=50% and 100%, fixed band-pass and Tone, nonmuted full wet output; compare attack and level only after active-path baseline. | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-006 | REQ-DST-OVERDRIVE-005 | positive / U | Set Dry/Wet=0%,50%,100% with S1 on a single track, then in an isolated return; disable other sends and direct output when measuring return. | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-007 | REQ-DST-OVERDRIVE-006 | automation / U | {"signal": "S2", "parameter": "Drive", "sequence": ["record current displayed value", "automate at0s,0.5s,1s using recorded legal low/mid/high values", "apply opposing clip modulation", "perform manual edit", "re-enable automation", "map to rack macro and repeat"], "observe": ["effective control ownership", "undo grouping", "audio discontinuity", "stage/mode gating"]} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-008 | REQ-DST-OVERDRIVE-006 | boundary / U | {"signal": "S1", "sequence": ["record displayed control endpoints and current factory state", "enter each endpoint and one display step inside", "switch every mode at each endpoint", "set all documented zero/inactive depths", "restore captured starting state"], "observe": ["accepted domain", "disabled controls", "retained values", "audio stability"], "numeric_parameter": "Drive"} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-009 | REQ-DST-OVERDRIVE-006 | persistence / U | {"sequence": ["load retained named preset copy", "record all controls/modes/quality/routing and matrix assignments if present", "save new Set and new preset", "close and reopen each", "compare displayed/stored state and audible continuation"], "observe": ["loss/migration", "source identity", "modulation memory", "tail/random state"], "not_a_default": "The retained named preset is not an initialized constructor."} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-010 | REQ-DST-OVERDRIVE-006 | undo / U | {"sequence": ["record all controls", "change numeric control, mode if present, quality/routing if present", "Undo each action", "Redo each action", "delete device and Undo"], "observe": ["transaction grouping", "restored identity/state", "automation references", "audible tail/seed"]} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-011 | REQ-DST-OVERDRIVE-006 | malformed / U | {"base": "frozen preset copy; never modify retained bytes", "mutations": ["truncate decompressed XML at midpoint", "set Drive/Manual/@Value to NaN", "set Drive/Manual/@Value to 1e309", "remove device element"], "observe": ["rejection/repair", "error text", "prior-state mutation", "partial processing"]} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-012 | REQ-DST-OVERDRIVE-006 | negative / U | {"parameter": "Drive", "sequence": ["enter text nan", "enter 1e309", "enter empty text", "enter just outside displayed legal bounds"], "observe": ["accepted/clamped/rejected state", "error", "undo"], "note": "UI entry and malformed-file loading are different trust boundaries."} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-013 | REQ-DST-OVERDRIVE-006 | cancellation / U | {"sequence": ["start preset replacement and cancel chooser before selection", "enter hot-swap and exit without selection", "start numeric drag and press Escape before release"], "observe": ["restoration versus commit", "undo entry", "focus", "partial routing/state mutation"]} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-014 | REQ-DST-OVERDRIVE-006 | transport / U | {"signal": "S2", "sequence": ["play from0s", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s three times"], "observe": ["follower/history reset", "buffer content", "feedback/generator/phase continuity if present", "first output samples"]} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-015 | REQ-DST-OVERDRIVE-006 | rate / U | {"signal": "S1 and S2 regenerated at each host rate", "host_sample_rates_hz": [44100, 48000, 96000], "block_sizes": [64, 512], "sequence": ["record control values and warmup", "process identical-duration inputs", "change rate/block while active if host permits", "compare real-time and offline export"], "observe": ["rate-dependent state", "latency", "aliasing", "random stream", "reset/error"], "device_rate_not_host_rate": true} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-016 | REQ-DST-OVERDRIVE-006 | teardown / U | {"signal": "S2", "sequence": ["process nonzero input with automation and audible wet path", "delete device during playback", "Undo deletion", "close Set during processing"], "observe": ["tail/feedback/noise cessation", "stale references", "automation restoration", "error/hang"], "routing": "No device-specific external sidechain is established by this manual section."} | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-017 | REQ-DST-OVERDRIVE-006 | negative / U | {"signal": "S0 then S1", "sequence": ["activate then bypass device", "compare silent input and active signal", "toggle processed/dry endpoints only if a control is independently available", "isolate direct/return/rack paths"], "observe": ["bypass latency", "generator tails", "state memory", "wet output"], "prerequisite": "Apply P-AUDIO independently for any effect or no-effect claim; no silence implies bypass or absent algorithm."} | U — expected outcome null; ungraded. |
| DST-PEDAL-001 | REQ-DST-PEDAL-001 | positive / Dpkg | Parse exact PKG-SCHEMA bytes and select class Pedal; compare all declared fields and class start line with schema-fields.json. | Exact class, line and field attributes match retained source. |
| DST-PEDAL-002 | REQ-DST-PEDAL-001 | persistence / Dpkg | Decode frozen package preset for Pedal; inspect /Ableton/Pedal, root attributes and recorded field XML. | Exact class/root attributes/field XML match package-values.json; no load/save behavior asserted. |
| DST-PEDAL-003 | REQ-DST-PEDAL-002 | boundary / D12 | Enumerate types; set Gain=0% then 50%; adjust global Output. | Overdrive, Distortion and Fuzz are available; Gain and Output are independent controls. |
| DST-PEDAL-004 | REQ-DST-PEDAL-003 | positive / D12 | Move Mid Frequency through left, center, right; set EQ knobs negative, neutral and positive. | Three Mid Frequency switch positions are available, documented as 500 Hz, 1 kHz and 2 kHz. |
| DST-PEDAL-005 | REQ-DST-PEDAL-004 | positive / U | Use S3; compare Sub off/on with Bass=-100%,0%,100%, fixed model/Gain. Require active processed low-frequency baseline. | U — expected outcome null; ungraded. |
| DST-PEDAL-006 | REQ-DST-PEDAL-005 | positive / D12 | Open title menu and toggle Hi-Quality; set Dry/Wet=0%,50%,100%. | Hi-Quality is available in the context menu; Dry/Wet is a distinct control. |
| DST-PEDAL-007 | REQ-DST-PEDAL-006 | positive / U | With Fuzz, Sub off, Gain=50%, Bass=Mid=-100%, Treble=100%, Output=-20 dB, start Dry/Wet=0% and raise it on S2. Independently establish wet output and input level before sound comparison. | U — expected outcome null; ungraded. |
| DST-PEDAL-008 | REQ-DST-PEDAL-007 | automation / U | {"signal": "S2", "parameter": "Gain", "sequence": ["record current displayed value", "automate at0s,0.5s,1s using recorded legal low/mid/high values", "apply opposing clip modulation", "perform manual edit", "re-enable automation", "map to rack macro and repeat"], "observe": ["effective control ownership", "undo grouping", "audio discontinuity", "stage/mode gating"]} | U — expected outcome null; ungraded. |
| DST-PEDAL-009 | REQ-DST-PEDAL-007 | boundary / U | {"signal": "S1", "sequence": ["record displayed control endpoints and current factory state", "enter each endpoint and one display step inside", "switch every mode at each endpoint", "set all documented zero/inactive depths", "restore captured starting state"], "observe": ["accepted domain", "disabled controls", "retained values", "audio stability"], "numeric_parameter": "Gain"} | U — expected outcome null; ungraded. |
| DST-PEDAL-010 | REQ-DST-PEDAL-007 | persistence / U | {"sequence": ["load retained named preset copy", "record all controls/modes/quality/routing and matrix assignments if present", "save new Set and new preset", "close and reopen each", "compare displayed/stored state and audible continuation"], "observe": ["loss/migration", "source identity", "modulation memory", "tail/random state"], "not_a_default": "The retained named preset is not an initialized constructor."} | U — expected outcome null; ungraded. |
| DST-PEDAL-011 | REQ-DST-PEDAL-007 | undo / U | {"sequence": ["record all controls", "change numeric control, mode if present, quality/routing if present", "Undo each action", "Redo each action", "delete device and Undo"], "observe": ["transaction grouping", "restored identity/state", "automation references", "audible tail/seed"]} | U — expected outcome null; ungraded. |
| DST-PEDAL-012 | REQ-DST-PEDAL-007 | malformed / U | {"base": "frozen preset copy; never modify retained bytes", "mutations": ["truncate decompressed XML at midpoint", "set Gain/Manual/@Value to NaN", "set Gain/Manual/@Value to 1e309", "remove device element", "set Type/Manual/@Value to999"], "observe": ["rejection/repair", "error text", "prior-state mutation", "partial processing"]} | U — expected outcome null; ungraded. |
| DST-PEDAL-013 | REQ-DST-PEDAL-007 | negative / U | {"parameter": "Gain", "sequence": ["enter text nan", "enter 1e309", "enter empty text", "enter just outside displayed legal bounds"], "observe": ["accepted/clamped/rejected state", "error", "undo"], "note": "UI entry and malformed-file loading are different trust boundaries."} | U — expected outcome null; ungraded. |
| DST-PEDAL-014 | REQ-DST-PEDAL-007 | cancellation / U | {"sequence": ["start preset replacement and cancel chooser before selection", "enter hot-swap and exit without selection", "start numeric drag and press Escape before release"], "observe": ["restoration versus commit", "undo entry", "focus", "partial routing/state mutation"]} | U — expected outcome null; ungraded. |
| DST-PEDAL-015 | REQ-DST-PEDAL-007 | transport / U | {"signal": "S2", "sequence": ["play from0s", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s three times"], "observe": ["follower/history reset", "buffer content", "feedback/generator/phase continuity if present", "first output samples"]} | U — expected outcome null; ungraded. |
| DST-PEDAL-016 | REQ-DST-PEDAL-007 | rate / U | {"signal": "S1 and S2 regenerated at each host rate", "host_sample_rates_hz": [44100, 48000, 96000], "block_sizes": [64, 512], "sequence": ["record control values and warmup", "process identical-duration inputs", "change rate/block while active if host permits", "compare real-time and offline export"], "observe": ["rate-dependent state", "latency", "aliasing", "random stream", "reset/error"], "device_rate_not_host_rate": true} | U — expected outcome null; ungraded. |
| DST-PEDAL-017 | REQ-DST-PEDAL-007 | teardown / U | {"signal": "S2", "sequence": ["process nonzero input with automation and audible wet path", "delete device during playback", "Undo deletion", "close Set during processing"], "observe": ["tail/feedback/noise cessation", "stale references", "automation restoration", "error/hang"], "routing": "No device-specific external sidechain is established by this manual section."} | U — expected outcome null; ungraded. |
| DST-PEDAL-018 | REQ-DST-PEDAL-007 | negative / U | {"signal": "S0 then S1", "sequence": ["activate then bypass device", "compare silent input and active signal", "toggle processed/dry endpoints only if a control is independently available", "isolate direct/return/rack paths"], "observe": ["bypass latency", "generator tails", "state memory", "wet output"], "prerequisite": "Apply P-AUDIO independently for any effect or no-effect claim; no silence implies bypass or absent algorithm."} | U — expected outcome null; ungraded. |
| DST-REDUX-001 | REQ-DST-REDUX-001 | positive / Dpkg | Parse exact PKG-SCHEMA bytes and select class Redux2; compare all declared fields and class start line with schema-fields.json. | Exact class, line and field attributes match retained source. |
| DST-REDUX-002 | REQ-DST-REDUX-001 | persistence / Dpkg | Decode frozen package preset for Redux; inspect /Ableton/Redux2, root attributes and recorded field XML. | Exact class/root attributes/field XML match package-values.json; no load/save behavior asserted. |
| DST-REDUX-003 | REQ-DST-REDUX-002 | positive / U | Use S1 at displayed Rate=4000 Hz and 12000 Hz, Jitter=0% and 50%, Pre/Post filters off. Host rate is independently varied later; device Rate is not the host rate. | U — expected outcome null; ungraded. |
| DST-REDUX-004 | REQ-DST-REDUX-003 | positive / D12 | With Rate=8000 Hz, enable Pre and Post independently; set Post-Filter Octave=-1,0,+1. | Pre and Post are separate switches; Post-Filter Octave is expressed relative to Rate/2. Exact audio cutoff remains U. |
| DST-REDUX-005 | REQ-DST-REDUX-004 | positive / U | Use S3 at displayed Bits=4 and 8 with Shape=0% and 50%; compare low and high input levels after active-path baseline. Device Rate fixed; Jitter off and filters fixed. | U — expected outcome null; ungraded. |
| DST-REDUX-006 | REQ-DST-REDUX-005 | positive / U | At Bits=4, toggle DC Shift on S3, then test Dry/Wet=0%,50%,100%; establish nonmuted quantized wet output and isolate the return if used. | U — expected outcome null; ungraded. |
| DST-REDUX-007 | REQ-DST-REDUX-006 | persistence / U | Obtain independently pinned Redux Legacy state; compare loading, device identity and controls with current Redux2; inspect EcoProcessing changes separately without assuming GUI meaning. | U — expected outcome null; ungraded. |
| DST-REDUX-008 | REQ-DST-REDUX-007 | automation / U | {"signal": "S2", "parameter": "SampleRate", "sequence": ["record current displayed value", "automate at0s,0.5s,1s using recorded legal low/mid/high values", "apply opposing clip modulation", "perform manual edit", "re-enable automation", "map to rack macro and repeat"], "observe": ["effective control ownership", "undo grouping", "audio discontinuity", "stage/mode gating"]} | U — expected outcome null; ungraded. |
| DST-REDUX-009 | REQ-DST-REDUX-007 | boundary / U | {"signal": "S1", "sequence": ["record displayed control endpoints and current factory state", "enter each endpoint and one display step inside", "switch every mode at each endpoint", "set all documented zero/inactive depths", "restore captured starting state"], "observe": ["accepted domain", "disabled controls", "retained values", "audio stability"], "numeric_parameter": "SampleRate"} | U — expected outcome null; ungraded. |
| DST-REDUX-010 | REQ-DST-REDUX-007 | persistence / U | {"sequence": ["load retained named preset copy", "record all controls/modes/quality/routing and matrix assignments if present", "save new Set and new preset", "close and reopen each", "compare displayed/stored state and audible continuation"], "observe": ["loss/migration", "source identity", "modulation memory", "tail/random state"], "not_a_default": "The retained named preset is not an initialized constructor."} | U — expected outcome null; ungraded. |
| DST-REDUX-011 | REQ-DST-REDUX-007 | undo / U | {"sequence": ["record all controls", "change numeric control, mode if present, quality/routing if present", "Undo each action", "Redo each action", "delete device and Undo"], "observe": ["transaction grouping", "restored identity/state", "automation references", "audible tail/seed"]} | U — expected outcome null; ungraded. |
| DST-REDUX-012 | REQ-DST-REDUX-007 | malformed / U | {"base": "frozen preset copy; never modify retained bytes", "mutations": ["truncate decompressed XML at midpoint", "set SampleRate/Manual/@Value to NaN", "set SampleRate/Manual/@Value to 1e309", "remove device element"], "observe": ["rejection/repair", "error text", "prior-state mutation", "partial processing"]} | U — expected outcome null; ungraded. |
| DST-REDUX-013 | REQ-DST-REDUX-007 | negative / U | {"parameter": "SampleRate", "sequence": ["enter text nan", "enter 1e309", "enter empty text", "enter just outside displayed legal bounds"], "observe": ["accepted/clamped/rejected state", "error", "undo"], "note": "UI entry and malformed-file loading are different trust boundaries."} | U — expected outcome null; ungraded. |
| DST-REDUX-014 | REQ-DST-REDUX-007 | cancellation / U | {"sequence": ["start preset replacement and cancel chooser before selection", "enter hot-swap and exit without selection", "start numeric drag and press Escape before release"], "observe": ["restoration versus commit", "undo entry", "focus", "partial routing/state mutation"]} | U — expected outcome null; ungraded. |
| DST-REDUX-015 | REQ-DST-REDUX-007 | transport / U | {"signal": "S2", "sequence": ["play from0s", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s three times"], "observe": ["follower/history reset", "buffer content", "feedback/generator/phase continuity if present", "first output samples"]} | U — expected outcome null; ungraded. |
| DST-REDUX-016 | REQ-DST-REDUX-007 | rate / U | {"signal": "S1 and S2 regenerated at each host rate", "host_sample_rates_hz": [44100, 48000, 96000], "block_sizes": [64, 512], "sequence": ["record control values and warmup", "process identical-duration inputs", "change rate/block while active if host permits", "compare real-time and offline export"], "observe": ["rate-dependent state", "latency", "aliasing", "random stream", "reset/error"], "device_rate_not_host_rate": true} | U — expected outcome null; ungraded. |
| DST-REDUX-017 | REQ-DST-REDUX-007 | teardown / U | {"signal": "S2", "sequence": ["process nonzero input with automation and audible wet path", "delete device during playback", "Undo deletion", "close Set during processing"], "observe": ["tail/feedback/noise cessation", "stale references", "automation restoration", "error/hang"], "routing": "No device-specific external sidechain is established by this manual section."} | U — expected outcome null; ungraded. |
| DST-REDUX-018 | REQ-DST-REDUX-007 | negative / U | {"signal": "S0 then S1", "sequence": ["activate then bypass device", "compare silent input and active signal", "toggle processed/dry endpoints only if a control is independently available", "isolate direct/return/rack paths"], "observe": ["bypass latency", "generator tails", "state memory", "wet output"], "prerequisite": "Apply P-AUDIO independently for any effect or no-effect claim; no silence implies bypass or absent algorithm."} | U — expected outcome null; ungraded. |
| DST-ROAR-001 | REQ-DST-ROAR-001 | positive / Dpkg | Parse exact PKG-SCHEMA bytes and select class Roar; compare all declared fields and class start line with schema-fields.json. | Exact class, line and field attributes match retained source. |
| DST-ROAR-002 | REQ-DST-ROAR-001 | persistence / Dpkg | Decode frozen package preset for Roar; inspect /Ableton/Roar, root attributes and recorded field XML. | Exact class/root attributes/field XML match package-values.json; no load/save behavior asserted. |
| DST-ROAR-003 | REQ-DST-ROAR-002 | positive / D12 | Adjust Drive, Tone Amount and Tone Frequency; toggle Color Compensation. | Input controls are distinct and Color Compensation is switchable. |
| DST-ROAR-004 | REQ-DST-ROAR-003 | positive / D12 | Select Single, Serial, Parallel, Multi Band, Mid Side, Feedback, Delay and inspect Blend, stage tabs and crossover controls. | All seven choices are available; Blend is provided except Single/Multi Band; Multi Band provides Low and High crossovers. |
| DST-ROAR-005 | REQ-DST-ROAR-004 | positive / D12 | In Serial and Multi Band, adjust each displayed stage independently; toggle Stage and Shaper; drag shaper display and adjust Bias and Shaper Level. | Stage/shaper toggles are distinct; visualization dragging addresses Shaper Amount. |
| DST-ROAR-006 | REQ-DST-ROAR-005 | positive / D12 | Enumerate all twelve choices in stage 1 and switch each at a fixed Shaper Amount. | Exactly the twelve documented shaper labels are selectable; audio consequences remain U. |
| DST-ROAR-007 | REQ-DST-ROAR-006 | positive / D12 | Select each of nine filters; inspect Resonance, Peak Gain and Morph; toggle Pre. | Nine types are selectable; Resonance is available except Resampling; Peak and Morph expose their respective controls. |
| DST-ROAR-008 | REQ-DST-ROAR-007 | positive / D12 | Open Mod Sources; for each LFO enumerate five waveforms and five modes, then adjust Morph and Smooth. | Each LFO has the documented five waveform/mode choices; Rate units change between Hz and tempo divisions. |
| DST-ROAR-009 | REQ-DST-ROAR-008 | positive / U | With S2, set a nonzero Env-to-Shaper Amount matrix route, test Hold off/on, Attack/Release, Threshold/Gain and analysis Frequency/Width; independently establish modulation and audible wet path; audition Input Listen. | U — expected outcome null; ungraded. |
| DST-ROAR-010 | REQ-DST-ROAR-009 | positive / D12 | Select all four Noise types; switch rate between free and synchronized, adjust Smooth. | Four named types and free/synchronized rate choices are available; no sequence equality asserted. |
| DST-ROAR-011 | REQ-DST-ROAR-010 | positive / D12 | Add LFO1-to-stage-1 Shaper Amount and Env-to-Dry/Wet routes, set nonzero cell amounts, expand panel, use X. | Selected targets appear as rows; sources occupy columns; X clears matrix assignments. Parameter bases and audio after clear are U. |
| DST-ROAR-012 | REQ-DST-ROAR-011 | positive / D12 | Enumerate five Feedback modes, toggle Invert/Gate and adjust feedback Filter Frequency/Width. | Five modes and separate Invert, Gate and filter controls are available; tail/audio outcomes remain U. |
| DST-ROAR-013 | REQ-DST-ROAR-012 | positive / U | Use nonmuted full wet S2; vary compression and sidechain HP at fixed feedback, then Output Gain and Dry/Wet. Disable unrelated modulation; capture peaks only after positive baseline. | U — expected outcome null; ungraded. |
| DST-ROAR-014 | REQ-DST-ROAR-013 | positive / D12 | Use distinct S2 main and S3 sidechain tracks with source audible output isolated; enable External SC, choose Post FX then Post Mixer, set Mix=0%,50%,100%, toggle Listen. | External source/tapping controls, Mix, SC Gain and Listen are available; selected tapping point updates. Audio/no-effect outcomes U. |
| DST-ROAR-015 | REQ-DST-ROAR-014 | positive / D12 | Set Note mode; enable MIDI > FB Note, choose a dedicated MIDI source and each tapping point; inspect Feedback Mode and Feedback Amount. | MIDI source and tapping selections are available; the manual describes Feedback Mode and Amount as inactive while MIDI sidechain is active. |
| DST-ROAR-016 | REQ-DST-ROAR-015 | positive / U | Inspect available menu controls and stored fields without inferring equivalence; compare preset variants only if independently retained. | U — expected outcome null; ungraded. |
| DST-ROAR-017 | REQ-DST-ROAR-016 | automation / U | {"signal": "S2", "parameter": "Stage1_Shaper_Amount", "sequence": ["record current displayed value", "automate at0s,0.5s,1s using recorded legal low/mid/high values", "apply opposing clip modulation", "perform manual edit", "re-enable automation", "map to rack macro and repeat"], "observe": ["effective control ownership", "undo grouping", "audio discontinuity", "stage/mode gating"]} | U — expected outcome null; ungraded. |
| DST-ROAR-018 | REQ-DST-ROAR-016 | boundary / U | {"signal": "S1", "sequence": ["record displayed control endpoints and current factory state", "enter each endpoint and one display step inside", "switch every mode at each endpoint", "set all documented zero/inactive depths", "restore captured starting state"], "observe": ["accepted domain", "disabled controls", "retained values", "audio stability"], "numeric_parameter": "Stage1_Shaper_Amount"} | U — expected outcome null; ungraded. |
| DST-ROAR-019 | REQ-DST-ROAR-016 | persistence / U | {"sequence": ["load retained named preset copy", "record all controls/modes/quality/routing and matrix assignments if present", "save new Set and new preset", "close and reopen each", "compare displayed/stored state and audible continuation"], "observe": ["loss/migration", "source identity", "modulation memory", "tail/random state"], "not_a_default": "The retained named preset is not an initialized constructor."} | U — expected outcome null; ungraded. |
| DST-ROAR-020 | REQ-DST-ROAR-016 | undo / U | {"sequence": ["record all controls", "change numeric control, mode if present, quality/routing if present", "Undo each action", "Redo each action", "delete device and Undo"], "observe": ["transaction grouping", "restored identity/state", "automation references", "audible tail/seed"]} | U — expected outcome null; ungraded. |
| DST-ROAR-021 | REQ-DST-ROAR-016 | malformed / U | {"base": "frozen preset copy; never modify retained bytes", "mutations": ["truncate decompressed XML at midpoint", "set Stage1_Shaper_Amount/Manual/@Value to NaN", "set Stage1_Shaper_Amount/Manual/@Value to 1e309", "remove device element", "set Input_RoutingMode/@Value to999"], "observe": ["rejection/repair", "error text", "prior-state mutation", "partial processing"]} | U — expected outcome null; ungraded. |
| DST-ROAR-022 | REQ-DST-ROAR-016 | negative / U | {"parameter": "Stage1_Shaper_Amount", "sequence": ["enter text nan", "enter 1e309", "enter empty text", "enter just outside displayed legal bounds"], "observe": ["accepted/clamped/rejected state", "error", "undo"], "note": "UI entry and malformed-file loading are different trust boundaries."} | U — expected outcome null; ungraded. |
| DST-ROAR-023 | REQ-DST-ROAR-016 | cancellation / U | {"sequence": ["start preset replacement and cancel chooser before selection", "enter hot-swap and exit without selection", "start numeric drag and press Escape before release"], "observe": ["restoration versus commit", "undo entry", "focus", "partial routing/state mutation"]} | U — expected outcome null; ungraded. |
| DST-ROAR-024 | REQ-DST-ROAR-016 | transport / U | {"signal": "S2", "sequence": ["play from0s", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s three times"], "observe": ["follower/history reset", "buffer content", "feedback/generator/phase continuity if present", "first output samples"]} | U — expected outcome null; ungraded. |
| DST-ROAR-025 | REQ-DST-ROAR-016 | rate / U | {"signal": "S1 and S2 regenerated at each host rate", "host_sample_rates_hz": [44100, 48000, 96000], "block_sizes": [64, 512], "sequence": ["record control values and warmup", "process identical-duration inputs", "change rate/block while active if host permits", "compare real-time and offline export"], "observe": ["rate-dependent state", "latency", "aliasing", "random stream", "reset/error"], "device_rate_not_host_rate": true} | U — expected outcome null; ungraded. |
| DST-ROAR-026 | REQ-DST-ROAR-016 | teardown / U | {"signal": "S2", "sequence": ["process nonzero input with automation and audible wet path", "delete device during playback", "Undo deletion", "close Set during processing"], "observe": ["tail/feedback/noise cessation", "stale references", "automation restoration", "error/hang"], "routing": "Remove/reconnect external audio and MIDI sources as a separate Roar subcase if active."} | U — expected outcome null; ungraded. |
| DST-ROAR-027 | REQ-DST-ROAR-016 | negative / U | {"signal": "S0 then S1", "sequence": ["activate then bypass device", "compare silent input and active signal", "toggle processed/dry endpoints only if a control is independently available", "isolate direct/return/rack paths"], "observe": ["bypass latency", "generator tails", "state memory", "wet output"], "prerequisite": "Apply P-AUDIO independently for any effect or no-effect claim; no silence implies bypass or absent algorithm."} | U — expected outcome null; ungraded. |
| DST-SATURATOR-001 | REQ-DST-SATURATOR-001 | positive / Dpkg | Parse exact PKG-SCHEMA bytes and select class Saturator; compare all declared fields and class start line with schema-fields.json. | Exact class, line and field attributes match retained source. |
| DST-SATURATOR-002 | REQ-DST-SATURATOR-001 | persistence / Dpkg | Decode frozen package preset for Saturator; inspect /Ableton/Saturator, root attributes and recorded field XML. | Exact class/root attributes/field XML match package-values.json; no load/save behavior asserted. |
| DST-SATURATOR-003 | REQ-DST-SATURATOR-002 | positive / D12 | Enumerate eight Curve Types; select Waveshaper and open expanded view. | Eight named choices are selectable; expanded Waveshaper controls can be shown. |
| DST-SATURATOR-004 | REQ-DST-SATURATOR-003 | boundary / D12 | Select Bass Shaper; set threshold to 0,-25,-50 dB; request values beyond displayed bounds without assuming clamp/reject. | The documented threshold endpoints are 0 and -50 dB; legal endpoint values are representable. Out-of-range outcome U. |
| DST-SATURATOR-005 | REQ-DST-SATURATOR-004 | positive / D12 | Toggle Color, open expanded view and move first/second handles while observing Amt Lo, Amt Hi and Frequency. | First handle addresses Amt Lo; second addresses Amt Hi/Frequency according to drag axis. Color can be enabled independently. |
| DST-SATURATOR-006 | REQ-DST-SATURATOR-005 | positive / U | Use independently verified nonmuted wet-only path, Dry/Wet=100%, Color negative and positive, select Soft Clip then Hard Clip at Output=-12 dB and 0 dB. Also examine Dry/Wet=0% separately without applying wet peak bound. | U — expected outcome null; ungraded. |
| DST-SATURATOR-007 | REQ-DST-SATURATOR-006 | positive / D12 | Select Waveshaper and expand; distinguish main Drive from Waveshaper Drive; enumerate six controls. | Waveshaper Drive, Curve, Depth, Linear, Damp and Period are active in Waveshaper mode. |
| DST-SATURATOR-008 | REQ-DST-SATURATOR-006 | negative / U | At Waveshaper Drive=0%, vary Curve/Depth/Linear/Damp/Period. Separately at Depth=0%, vary Period. Establish positive influence at Drive=100% and Depth>0, selected Waveshaper, nonzero nonlinear wet output, fixed color/post clip; otherwise U. | U — expected outcome null; ungraded. |
| DST-SATURATOR-009 | REQ-DST-SATURATOR-007 | positive / D12 | Open context menu and toggle Hi-Quality and Pre-DC Filter separately. | Both menu controls are available and independently switchable. |
| DST-SATURATOR-010 | REQ-DST-SATURATOR-008 | automation / U | {"signal": "S2", "parameter": "PreDrive", "sequence": ["record current displayed value", "automate at0s,0.5s,1s using recorded legal low/mid/high values", "apply opposing clip modulation", "perform manual edit", "re-enable automation", "map to rack macro and repeat"], "observe": ["effective control ownership", "undo grouping", "audio discontinuity", "stage/mode gating"]} | U — expected outcome null; ungraded. |
| DST-SATURATOR-011 | REQ-DST-SATURATOR-008 | boundary / U | {"signal": "S1", "sequence": ["record displayed control endpoints and current factory state", "enter each endpoint and one display step inside", "switch every mode at each endpoint", "set all documented zero/inactive depths", "restore captured starting state"], "observe": ["accepted domain", "disabled controls", "retained values", "audio stability"], "numeric_parameter": "PreDrive"} | U — expected outcome null; ungraded. |
| DST-SATURATOR-012 | REQ-DST-SATURATOR-008 | persistence / U | {"sequence": ["load retained named preset copy", "record all controls/modes/quality/routing and matrix assignments if present", "save new Set and new preset", "close and reopen each", "compare displayed/stored state and audible continuation"], "observe": ["loss/migration", "source identity", "modulation memory", "tail/random state"], "not_a_default": "The retained named preset is not an initialized constructor."} | U — expected outcome null; ungraded. |
| DST-SATURATOR-013 | REQ-DST-SATURATOR-008 | undo / U | {"sequence": ["record all controls", "change numeric control, mode if present, quality/routing if present", "Undo each action", "Redo each action", "delete device and Undo"], "observe": ["transaction grouping", "restored identity/state", "automation references", "audible tail/seed"]} | U — expected outcome null; ungraded. |
| DST-SATURATOR-014 | REQ-DST-SATURATOR-008 | malformed / U | {"base": "frozen preset copy; never modify retained bytes", "mutations": ["truncate decompressed XML at midpoint", "set PreDrive/Manual/@Value to NaN", "set PreDrive/Manual/@Value to 1e309", "remove device element", "set Type/Manual/@Value to999"], "observe": ["rejection/repair", "error text", "prior-state mutation", "partial processing"]} | U — expected outcome null; ungraded. |
| DST-SATURATOR-015 | REQ-DST-SATURATOR-008 | negative / U | {"parameter": "PreDrive", "sequence": ["enter text nan", "enter 1e309", "enter empty text", "enter just outside displayed legal bounds"], "observe": ["accepted/clamped/rejected state", "error", "undo"], "note": "UI entry and malformed-file loading are different trust boundaries."} | U — expected outcome null; ungraded. |
| DST-SATURATOR-016 | REQ-DST-SATURATOR-008 | cancellation / U | {"sequence": ["start preset replacement and cancel chooser before selection", "enter hot-swap and exit without selection", "start numeric drag and press Escape before release"], "observe": ["restoration versus commit", "undo entry", "focus", "partial routing/state mutation"]} | U — expected outcome null; ungraded. |
| DST-SATURATOR-017 | REQ-DST-SATURATOR-008 | transport / U | {"signal": "S2", "sequence": ["play from0s", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s three times"], "observe": ["follower/history reset", "buffer content", "feedback/generator/phase continuity if present", "first output samples"]} | U — expected outcome null; ungraded. |
| DST-SATURATOR-018 | REQ-DST-SATURATOR-008 | rate / U | {"signal": "S1 and S2 regenerated at each host rate", "host_sample_rates_hz": [44100, 48000, 96000], "block_sizes": [64, 512], "sequence": ["record control values and warmup", "process identical-duration inputs", "change rate/block while active if host permits", "compare real-time and offline export"], "observe": ["rate-dependent state", "latency", "aliasing", "random stream", "reset/error"], "device_rate_not_host_rate": true} | U — expected outcome null; ungraded. |
| DST-SATURATOR-019 | REQ-DST-SATURATOR-008 | teardown / U | {"signal": "S2", "sequence": ["process nonzero input with automation and audible wet path", "delete device during playback", "Undo deletion", "close Set during processing"], "observe": ["tail/feedback/noise cessation", "stale references", "automation restoration", "error/hang"], "routing": "No device-specific external sidechain is established by this manual section."} | U — expected outcome null; ungraded. |
| DST-SATURATOR-020 | REQ-DST-SATURATOR-008 | negative / U | {"signal": "S0 then S1", "sequence": ["activate then bypass device", "compare silent input and active signal", "toggle processed/dry endpoints only if a control is independently available", "isolate direct/return/rack paths"], "observe": ["bypass latency", "generator tails", "state memory", "wet output"], "prerequisite": "Apply P-AUDIO independently for any effect or no-effect claim; no silence implies bypass or absent algorithm."} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-001 | REQ-DST-VINYL-DISTORTION-001 | positive / Dpkg | Parse exact PKG-SCHEMA bytes and select class Vinyl; compare all declared fields and class start line with schema-fields.json. | Exact class, line and field attributes match retained source. |
| DST-VINYL-DISTORTION-002 | REQ-DST-VINYL-DISTORTION-001 | persistence / Dpkg | Decode frozen package preset for Vinyl Distortion; inspect /Ableton/Vinyl, root attributes and recorded field XML. | Exact class/root attributes/field XML match package-values.json; no load/save behavior asserted. |
| DST-VINYL-DISTORTION-003 | REQ-DST-VINYL-DISTORTION-002 | positive / D12 | For Tracing and Pinch separately drag X, Y and modifier-Y; compare Freq/Drive/Q, then change overall Drive. | Each model exposes frequency, drive and Q adjustment by the documented XY gestures; global Drive is distinct. |
| DST-VINYL-DISTORTION-004 | REQ-DST-VINYL-DISTORTION-003 | positive / D12 | Select Soft then Hard and toggle Stereo/Mono with Pinch active. | Two modes and a Stereo/Mono switch are available; audio behavior remains U. |
| DST-VINYL-DISTORTION-005 | REQ-DST-VINYL-DISTORTION-004 | positive / U | Test Density=0%,50%,100% with nonzero Crackle Volume, then vary Volume at fixed Density on silence S0 and active S1; first establish generator output independently, not just harmonic path. | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-006 | REQ-DST-VINYL-DISTORTION-005 | automation / U | {"signal": "S2", "parameter": "Drive", "sequence": ["record current displayed value", "automate at0s,0.5s,1s using recorded legal low/mid/high values", "apply opposing clip modulation", "perform manual edit", "re-enable automation", "map to rack macro and repeat"], "observe": ["effective control ownership", "undo grouping", "audio discontinuity", "stage/mode gating"]} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-007 | REQ-DST-VINYL-DISTORTION-005 | boundary / U | {"signal": "S1", "sequence": ["record displayed control endpoints and current factory state", "enter each endpoint and one display step inside", "switch every mode at each endpoint", "set all documented zero/inactive depths", "restore captured starting state"], "observe": ["accepted domain", "disabled controls", "retained values", "audio stability"], "numeric_parameter": "Drive"} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-008 | REQ-DST-VINYL-DISTORTION-005 | persistence / U | {"sequence": ["load retained named preset copy", "record all controls/modes/quality/routing and matrix assignments if present", "save new Set and new preset", "close and reopen each", "compare displayed/stored state and audible continuation"], "observe": ["loss/migration", "source identity", "modulation memory", "tail/random state"], "not_a_default": "The retained named preset is not an initialized constructor."} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-009 | REQ-DST-VINYL-DISTORTION-005 | undo / U | {"sequence": ["record all controls", "change numeric control, mode if present, quality/routing if present", "Undo each action", "Redo each action", "delete device and Undo"], "observe": ["transaction grouping", "restored identity/state", "automation references", "audible tail/seed"]} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-010 | REQ-DST-VINYL-DISTORTION-005 | malformed / U | {"base": "frozen preset copy; never modify retained bytes", "mutations": ["truncate decompressed XML at midpoint", "set Drive/Manual/@Value to NaN", "set Drive/Manual/@Value to 1e309", "remove device element", "set SoftHard/Manual/@Value to999"], "observe": ["rejection/repair", "error text", "prior-state mutation", "partial processing"]} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-011 | REQ-DST-VINYL-DISTORTION-005 | negative / U | {"parameter": "Drive", "sequence": ["enter text nan", "enter 1e309", "enter empty text", "enter just outside displayed legal bounds"], "observe": ["accepted/clamped/rejected state", "error", "undo"], "note": "UI entry and malformed-file loading are different trust boundaries."} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-012 | REQ-DST-VINYL-DISTORTION-005 | cancellation / U | {"sequence": ["start preset replacement and cancel chooser before selection", "enter hot-swap and exit without selection", "start numeric drag and press Escape before release"], "observe": ["restoration versus commit", "undo entry", "focus", "partial routing/state mutation"]} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-013 | REQ-DST-VINYL-DISTORTION-005 | transport / U | {"signal": "S2", "sequence": ["play from0s", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s three times"], "observe": ["follower/history reset", "buffer content", "feedback/generator/phase continuity if present", "first output samples"]} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-014 | REQ-DST-VINYL-DISTORTION-005 | rate / U | {"signal": "S1 and S2 regenerated at each host rate", "host_sample_rates_hz": [44100, 48000, 96000], "block_sizes": [64, 512], "sequence": ["record control values and warmup", "process identical-duration inputs", "change rate/block while active if host permits", "compare real-time and offline export"], "observe": ["rate-dependent state", "latency", "aliasing", "random stream", "reset/error"], "device_rate_not_host_rate": true} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-015 | REQ-DST-VINYL-DISTORTION-005 | teardown / U | {"signal": "S2", "sequence": ["process nonzero input with automation and audible wet path", "delete device during playback", "Undo deletion", "close Set during processing"], "observe": ["tail/feedback/noise cessation", "stale references", "automation restoration", "error/hang"], "routing": "No device-specific external sidechain is established by this manual section."} | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-016 | REQ-DST-VINYL-DISTORTION-005 | negative / U | {"signal": "S0 then S1", "sequence": ["activate then bypass device", "compare silent input and active signal", "toggle processed/dry endpoints only if a control is independently available", "isolate direct/return/rack paths"], "observe": ["bypass latency", "generator tails", "state memory", "wet output"], "prerequisite": "Apply P-AUDIO independently for any effect or no-effect claim; no silence implies bypass or absent algorithm."} | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-018 | REQ-DST-DRUM-BUSS-002 | signal-interaction / U | Test Soft/Medium/Hard on S1 at low/high levels, Comp off/on, Drive at minimum/mid/maximum displayed values; fix Trim and output. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-DRUM-BUSS-019 | REQ-DST-DRUM-BUSS-004 | signal-interaction / U | With S2 and independently audible Boom=50%, compare Decay min/max at Boom=0% and >0%; test Force To Note near each side of a semitone midpoint and the exact midpoint, tuning reference unresolved. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-018 | REQ-DST-DYNAMIC-TUBE-002 | signal-interaction / U | For A/B/C sweep input level and Bias at recorded endpoints with Envelope=0; do not infer threshold from an inactive path. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-EROSION-019 | REQ-DST-EROSION-002 | signal-interaction / U | Test modern Erosion2 at Blend=0%,50%,100%, Amount=0 and >0 on S1, compare ordinary/modifier XY control routes; do not compare generated noise sample equality. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-OVERDRIVE-018 | REQ-DST-OVERDRIVE-002 | signal-interaction / U | Compare band-pass bandwidth/center endpoints on S3 with Drive>0 and fixed Dynamics/Tone/full-wet output. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-PEDAL-019 | REQ-DST-PEDAL-002 | signal-interaction / U | Test Overdrive/Distortion/Fuzz with Gain=0%,50%,100% on S1 and S2; hold post EQ and Output fixed and independently establish distorted wet output. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-PEDAL-020 | REQ-DST-PEDAL-003 | signal-interaction / U | At each Mid Frequency position and Bass/Mid/Treble neutral/cut/boost, use S3; measure documented band tendencies without invented Q/boost tolerance. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-REDUX-019 | REQ-DST-REDUX-003 | signal-interaction / U | At Rate=8000Hz test Pre/Post off/off,on/off,off/on,on/on; Post-Filter Octave=-1,0,+1; Jitter=0%,50%. Establish bandwidth and width baselines independently. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-ROAR-028 | REQ-DST-ROAR-003 | signal-interaction / U | Test Single, Serial, Parallel, Multi Band, Mid Side, Feedback and Delay using S1/S2/S3; for each independently establish active stage output and stage-sensitive contrast. Hold other stages/shapers at contrasting known settings, test Blend endpoints only where present; test both crossovers only in Multi Band. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-ROAR-029 | REQ-DST-ROAR-005 | signal-interaction / U | For each of twelve shapers use S1 at two input levels, nonzero Shaper Amount, Bias=0, then recorded positive/negative Bias. Disable feedback and compression, bypass filter, full wet and fixed output; establish active nonlinear baseline per shaper. Noise/Shards remain statistical/sequence U. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-ROAR-030 | REQ-DST-ROAR-006 | signal-interaction / U | Test all nine filter types on S3 with shaper on, contrasting Amount>0, Pre off/on. Establish both filter-sensitive and nonlinear baselines; isolate generated harmonics to distinguish Pre placement. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-ROAR-031 | REQ-DST-ROAR-007 | signal-interaction / U | For LFO1/2 assign nonzero amount to a proven active stage-1 Amount target; test five waveforms and five rate modes with Morph/Smooth endpoints, tempo60/120BPM and stop/seek. Zero matrix depth tests require independent positive depth effect. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-ROAR-032 | REQ-DST-ROAR-009 | signal-interaction / U | Assign Noise at nonzero depth to active Shaper Amount, test four types, free/synced rates and Smooth min/max on S1. PRNG state/seed/distribution and repeatability have no oracle. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-ROAR-033 | REQ-DST-ROAR-011 | signal-interaction / U | Establish nonzero feedback with S2 in Feedback/Delay modes; test all five feedback modes, Invert off/on and Gate off/on, remove input for5s. Gate-off persistence requires independently established sustaining feedback, not merely Amount>0; no universal infinite-tail pass. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-ROAR-034 | REQ-DST-ROAR-013 | signal-interaction / U | With independently effective Env-to-Shaper Amount modulation, test Mix=0/100 using distinct internal S2 and external S3, selected PostFX/PostMixer path, SC Gain changes, Listen off/on and missing source. Isolate source track audible path; active nonzero matrix and wet output required. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-ROAR-035 | REQ-DST-ROAR-014 | signal-interaction / U | In Feedback Note mode route MIDI notes60,64,67 separately then overlapping, sustain on/off and note-offs; verify MIDI source path and nonzero pitched feedback first. Compare MIDI source deletion and Listen separately; pitch mapping/priority unknown. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-SATURATOR-021 | REQ-DST-SATURATOR-002 | signal-interaction / U | For eight curves use S1 at low/high levels, Drive fixed, Color off, Post Clip disabled only if independently available, full wet. Repeat with Color on and contrasting amounts; curves and clipping thresholds remain U. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-SATURATOR-022 | REQ-DST-SATURATOR-006 | signal-interaction / U | With Waveshaper active and full wet, test each six-control endpoint, Depth=0 and >0, Waveshaper Drive=0% and 100%; establish nonzero positive-depth/drive baseline before any no-effect comparison. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-SATURATOR-023 | REQ-DST-SATURATOR-007 | signal-interaction / U | Compare Hi-Quality off/on on S1 near Nyquist, then Pre-DC Filter off/on on S3 including DC segment; establish nonzero nonlinear and DC output baselines separately. No aliasing/CPU/delay tolerance specified. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-DYNAMIC-TUBE-019 | REQ-DST-DYNAMIC-TUBE-005 | signal-interaction / U | Compare Hi-Quality off/on on S1 high-frequency segment, at nonzero distortion with fixed model/drive/bias/output; no factor, aliasing metric or CPU target specified. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-PEDAL-021 | REQ-DST-PEDAL-005 | signal-interaction / U | Compare Hi-Quality off/on with high-frequency S1, nonzero Gain and active processed output; no aliasing/CPU/latency target specified. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |
| DST-VINYL-DISTORTION-017 | REQ-DST-VINYL-DISTORTION-002 | signal-interaction / U | Isolate Tracing then Pinch by independently established band on/off/zero paths; test Soft/Hard, Stereo/Mono and Q/Frequency/Drive endpoints on S1/S3; disable or independently isolate Crackle before harmonic comparisons. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U. | U — expected outcome null; ungraded. |

## Cross-feature obligations and unresolved results

Exact transfer curves, oversampling factors/filters, normalization, clipping
thresholds, smoothing, aliasing, delay compensation, random seeds/distributions,
noise correlation, filter phase and all audio tolerances remain unknown. Random
behavior is specifically relevant to Erosion noise, Redux Jitter, Roar Noise/
Noise Injection/Shards and Vinyl Crackle; other modes have no proven determinism.
No generic host fallback resolves those gaps. Silent input can still carry
feedback, tails, DC or generated noise and is tested separately from bypass.

Each device has explicit automation, endpoint, persistence, undo, malformed,
invalid UI entry, cancellation, transport, rate/block and teardown cases.
Cancellation includes chooser exit and interrupted edit; no rollback is assumed.
Roar additionally needs audio/MIDI sidechain disconnection, held-note, Listen,
feedback and matrix interactions. Arrangement/Session ownership and mapped
parameters use their own owners without asserting preserved transaction/state.
Selection/focus follows host controls; exact focus restoration remains part of
cancel/teardown observations. Device-only sections establish no hardware
permissions prompt: engine/platform failures remain a required downstream
obligation, not an inapplicable success. Real-time/export parity is unresolved.
Legacy profiles remain separate open inventory obligations. Unknown application
outcomes and manual/build parity prevent full-profile closure.

## Analysis-only evidence appendix

- **E1 / D12-AUDIO-EFFECTS:** retained official
  [audio-effect manual](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/),
  Version 12 without exact 12.4.3 publication, captured 2026-10-19.
  Reuse the original source identity in audio-utilities/sources.json and exact
  [HTML bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html),
  SHA-256 `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`.
  Per-device manual blocks carry exact HTML start lines and stable B locators.
  Sections are Drum Buss29.12, Dynamic Tube29.13, Erosion29.17,
  Overdrive29.27, Pedal29.28, Redux29.30, Roar29.33, Saturator29.34,
  Vinyl Distortion29.41. These documentary sections are not observed execution.
- **E2 / PKG-SCHEMA:** installed latest 12.0_12402 schema,
  SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
  The [schema fields](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/schema-fields.json)
  preserve class/line/field attributes. Classes and lines: DrumBuss at line 1873,
  Tube at line 8203, Erosion2 2377, Overdrive at line 5913, Pedal at line 5942, Redux2 6321,
  Roar at line 6568, Saturator at line 6878 and Vinyl at line 8495. Timeable or Oversampling vocabulary
  establishes no runtime automation or DSP factor.
- **E3 / bounded package presets:** one inventory-pinned shipped preset per
  device. [Source records](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/sources.json)
  retain source/retained paths, byte counts, hashes and original identities;
  [package values](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/package-values.json)
  preserve root attributes, locators and XML fields. All nine carry historical
  Creator 12.4d1; none establishes the constructor/default or migration behavior.

The [requirement map](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/requirements.json)
links each documentary clause to exact B blocks or installed records. The
[author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/manifest-author-r1.json)
freezes exact sources, cases, validation and both canonical snapshots for separate
review. It is an author freeze, not an independent review or handoff release.
