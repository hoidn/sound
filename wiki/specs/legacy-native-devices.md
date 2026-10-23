---
id: SPEC-LEGACY-NATIVE-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3; predecessor documentary applicability unresolved
---

# Eight legacy native audio-effect profiles

The current bounded [owner R2](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/README-r2.md)
has77unchanged requirements and194records:45D11source-content checks,8Dpkg
file-only checks,141target-Uprobes (125old+16new). All current actual outcomes are
null/U/unexecuted. Following original counts, case tables and checker instructions
are retained historical R1 context; current cases/overlay/check are linked below.
D11/file expected strings never grade the application. Do not run the historical
R1 validator as a current-canonical check.


## Scope and authority

This partial FEAT-DEVICES draft owns Auto Filter Legacy, Auto Pan, Chorus,
Erosion Legacy, Flanger, Frequency Shifter, Phaser and Redux Legacy from the
[legacy inventory](../research/full-live-coverage-inventory.md#legacy-native-devices-8).
It is an analyst draft, not an implementation handoff or a complete profile.
The [coverage design](../research/full-live-specification-design.md) governs closure;
the [research owner](../research/legacy-native-devices.md) owns source interpretation.

**D11** clauses below describe the official Version 11 predecessor text only.
Every such clause has exact-12.4.3 applicability **U**. They are documented
precursor contracts and investigation questions, not approved requirements for
the target application. **Dpkg** establishes retained file/schema observations,
not effective device behavior. **U** means unsupported and ungraded. All target
expected outcomes are null; no original, extracted-original or candidate ran.
D11 source-content checks and Dpkg parser checks are never compatibility passes.

[Current filter/EQ](filter-eq-devices.md) owns AutoFilter2;
[current distortion](distortion-devices.md) owns Erosion2/Redux2 and the existing
D12 Erosion migration clause. Their laws do not transfer here. Modern Auto
Pan-Tremolo, Chorus-Ensemble, Phaser-Flanger and Shifter are distinct profiles;
this packet does not substitute their manuals or controls for the older devices.
[Device racks](device-racks.md), [automation](automation-envelopes.md),
[mix graph](mix-graph.md) and [Set structure](live-set-structure.md) retain their
bounded shared ownership. None establishes these devices’ lifecycle or DSP.

## Inputs, acceptance and limits

The [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/fixtures.json)
are authored definitions only. Use disposable Sets and copies of presets, isolate
one actually offered legacy profile, record accepted settings and identify the
source version. A preset is not a constructor default; a schema domain is not a
GUI or effective DSP domain. Do not force predecessor controls into the target.
Absent controls, missing old Sets and failed positive controls remain U.

Before a no-effect, muted-route, zero-depth, channel or modulation observation,
retain a nonzero processed response and the matching active positive control.
Excite the relevant bands and isolate competing dry/send/sidechain paths. Random
modes do not permit sample equality. Documentary examples supply no calibrated
frequency, waveform, loudness, latency, statistical or sample-boundary tolerance.
A later executable packet must establish those criteria independently.

Auto Filter Legacy here means the inventoried AutoFilter class/profile. The
nested pre-9.5 filter subset in its D11 chapter is a separate historical submode;
LegacyMode=false in one preset neither changes this profile into AutoFilter2 nor
proves a target upgrade route. D11 Core Library availability and edition notes
are historical context, not target availability exclusions.

## Requirements

## Auto Filter Legacy

### REQ-LEG-AUTO-FILTER-001 — Retained package identity

**Dpkg.** The pinned schema declares AutoFilter; the single retained preset for Auto Filter Legacy has /Ableton/AutoFilter, Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. This is a file/profile observation only. It proves no current constructor default, UI range, enum interpretation, automation eligibility or audio behavior.

Evidence: [schema-fields.json#class=AutoFilter](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/schema-fields.json), [package-observations.json#class=AutoFilter](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-AUTO-FILTER-002 — Filter choices and circuits

**D11.** Live 11 predecessor only: The predecessor offers low-pass, high-pass, band-pass, notch and Morph, with 12/24 dB slopes. Clean and OSR are described for all types; MS2, SMP and PRD for low/high-pass. This establishes selections, not a transfer function or an internal circuit requirement. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-filter-blocks.json#auto-filter:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json).

### REQ-LEG-AUTO-FILTER-003 — Drive eligibility

**D11.** Live 11 predecessor only: An additional Drive control precedes filtering for low-pass, high-pass or band-pass with a circuit other than Clean. Its numerical gain/distortion law is unspecified. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-filter-blocks.json#auto-filter:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json).

### REQ-LEG-AUTO-FILTER-004 — Frequency and resonance editing

**D11.** Live 11 predecessor only: Frequency and Resonance are editable with knobs, their numeric displays and the X-Y display. No display-to-coefficient mapping is established. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-filter-blocks.json#auto-filter:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json).

### REQ-LEG-AUTO-FILTER-005 — Morph traversal and snapping

**D11.** Live 11 predecessor only: Morph traverses low-pass, band-pass, high-pass, notch and back to low-pass; its knob context menu offers snaps to those four named types. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-filter-blocks.json#auto-filter:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json).

### REQ-LEG-AUTO-FILTER-006 — Envelope control

**D11.** Live 11 predecessor only: Envelope Amount sets influence on frequency; Attack and Release control response to rising and falling signal level. The source gives relative fast/slow behavior, not an envelope formula. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-filter-blocks.json#auto-filter:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json).

### REQ-LEG-AUTO-FILTER-007 — External envelope trigger

**D11.** Live 11 predecessor only: The unfolded Sidechain section can select another track as envelope trigger. Sidechain Gain affects trigger level, not source mix volume; Dry/Wet 100% uses the sidechain alone and 0% effectively bypasses it. The sidechain is described as a trigger, not audible signal admission. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-filter-blocks.json#auto-filter:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json).

### REQ-LEG-AUTO-FILTER-008 — LFO timing and stereo roles

**D11.** Live 11 predecessor only: LFO Amount affects frequency and Rate supports Hz or tempo sync. Shapes include sine, square, triangle, rising/falling saw and mono/stereo sample-and-hold. Phase offsets equal-rate stereo LFOs; Spin detunes their rates. Phase/Spin have no stated sound effect for sample-and-hold; its two selections distinguish independent/shared channel modulation. No RNG distribution or phase law is established. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-filter-blocks.json#auto-filter:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B022](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B025](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B026](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json).

### REQ-LEG-AUTO-FILTER-009 — Quantize Beat

**D11.** Live 11 predecessor only: With Quantize Beat off, frequency modulation follows its control source; on, changes occur rhythmically. Numbered values denote sixteenth notes, so value 4 denotes a quarter-note interval. Exact event rounding and clock phase are unspecified. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-filter-blocks.json#auto-filter:B027](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json).

### REQ-LEG-AUTO-FILTER-010 — Older filter upgrade

**D11.** Live 11 predecessor only: The Live 11 text describes pre-9.5 Sets opening its earlier filter subset without Drive and exposing an Upgrade button. Upgrade permanently changes that instance to the then-new models and may change sound. This is not evidence of a target 12.4.3 upgrade route. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-filter-blocks.json#auto-filter:B028](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json), [manual-auto-filter-blocks.json#auto-filter:B029](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-filter-blocks.json).

### REQ-LEG-AUTO-FILTER-011 — Target parity and migration

**U.** Whether Auto Filter Legacy in 12.4.3 exposes, preserves, migrates or changes any predecessor control/state/audio behavior is unknown. Matching names/classes and the retained preset do not establish historical Set compatibility, replacement with a modern device, a supported upgrade action or an old-filter submode.

Evidence: [package-observations.json#class=AutoFilter](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-AUTO-FILTER-012 — Audio, clock and numerical behavior

**U.** Auto Filter Legacy exact response, latency, smoothing, overload/headroom, disabled/silent path, sample/block dependence, random laws where relevant, modulation/restart phase and tail are unknown. Predecessor adjectives and schema fields supply no target DSP or timing tolerance.

### REQ-LEG-AUTO-FILTER-013 — Automation, persistence and lifecycle

**U.** Auto Filter Legacy automation/clip-envelope/macro/manual ownership, undo grouping, preset/Set/random/tail state, malformed-input policy, cancellation atomicity, missing routes and bypass/removal/engine/Set teardown remain unknown. Shared owners apply only within their stated scopes.

## Auto Pan

### REQ-LEG-AUTO-PAN-001 — Retained package identity

**Dpkg.** The pinned schema declares AutoPan; the single retained preset for Auto Pan has /Ableton/AutoPan, Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. This is a file/profile observation only. It proves no current constructor default, UI range, enum interpretation, automation eligibility or audio behavior.

Evidence: [schema-fields.json#class=AutoPan](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/schema-fields.json), [package-observations.json#class=AutoPan](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-AUTO-PAN-002 — Channel amplitude modulation

**D11.** Live 11 predecessor only: Amount controls influence on incoming audio; left/right amplitudes are modulated using sine, triangle, falling saw or random choices. No attenuation law or random distribution is established. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-pan-blocks.json#auto-pan:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-pan-blocks.json), [manual-auto-pan-blocks.json#auto-pan:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-pan-blocks.json), [manual-auto-pan-blocks.json#auto-pan:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-pan-blocks.json).

### REQ-LEG-AUTO-PAN-003 — Shape and inversion

**D11.** Live 11 predecessor only: Shape hardens waveform extremes; Normal/Invert switches waveform polarity, including turning a falling saw into a rising saw. No sample curve is specified. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-pan-blocks.json#auto-pan:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-pan-blocks.json).

### REQ-LEG-AUTO-PAN-004 — Rate units

**D11.** Live 11 predecessor only: Rate supports Hz and song-tempo synchronization; no scheduler or tempo-change rule follows. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-pan-blocks.json#auto-pan:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-pan-blocks.json).

### REQ-LEG-AUTO-PAN-005 — Phase and offset

**D11.** Live 11 predecessor only: Phase shifts the equal-frequency stereo LFO relationship; 180 degrees is described as opposite extrema. Offset changes their waveform start position. Neither defines restart phase or audio gain normalization. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-auto-pan-blocks.json#auto-pan:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-pan-blocks.json), [manual-auto-pan-blocks.json#auto-pan:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-auto-pan-blocks.json).

### REQ-LEG-AUTO-PAN-006 — Target parity and migration

**U.** Whether Auto Pan in 12.4.3 exposes, preserves, migrates or changes any predecessor control/state/audio behavior is unknown. Matching names/classes and the retained preset do not establish historical Set compatibility, replacement with a modern device, a supported upgrade action or an old-filter submode.

Evidence: [package-observations.json#class=AutoPan](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-AUTO-PAN-007 — Audio, clock and numerical behavior

**U.** Auto Pan exact response, latency, smoothing, overload/headroom, disabled/silent path, sample/block dependence, random laws where relevant, modulation/restart phase and tail are unknown. Predecessor adjectives and schema fields supply no target DSP or timing tolerance.

### REQ-LEG-AUTO-PAN-008 — Automation, persistence and lifecycle

**U.** Auto Pan automation/clip-envelope/macro/manual ownership, undo grouping, preset/Set/random/tail state, malformed-input policy, cancellation atomicity, missing routes and bypass/removal/engine/Set teardown remain unknown. Shared owners apply only within their stated scopes.

## Chorus

### REQ-LEG-CHORUS-001 — Retained package identity

**Dpkg.** The pinned schema declares Chorus; the single retained preset for Chorus has /Ableton/Chorus, Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. This is a file/profile observation only. It proves no current constructor default, UI range, enum interpretation, automation eligibility or audio behavior.

Evidence: [schema-fields.json#class=Chorus](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/schema-fields.json), [package-observations.json#class=Chorus](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-CHORUS-002 — Independent delay and high-pass controls

**D11.** Live 11 predecessor only: The predecessor presents two parallel time-modulated delay paths with separate millisecond times. Delay 1 has a high-pass control that removes lower frequencies from that path. No kernel or filter law follows. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-chorus-blocks.json#chorus:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json), [manual-chorus-blocks.json#chorus:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json).

### REQ-LEG-CHORUS-003 — Delay 2 modes

**D11.** Live 11 predecessor only: Delay 2 Off leaves only Delay 1 audible; Fix modulates only Delay 1; Mod applies the same modulation to Delay 2. No phase/null/tail law follows. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-chorus-blocks.json#chorus:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json).

### REQ-LEG-CHORUS-004 — Delay linking

**D11.** Live 11 predecessor only: The equals link sets both delays to Delay 1 time and permits editing them together. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-chorus-blocks.json#chorus:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json).

### REQ-LEG-CHORUS-005 — Modulation edit axes and multiplier

**D11.** Live 11 predecessor only: Modulation X-Y horizontal changes rate, vertical changes amount; Amount is in milliseconds and Rate in Hz. The *20 switch multiplies modulation frequency by twenty. No interpolation or output metric is specified. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-chorus-blocks.json#chorus:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json), [manual-chorus-blocks.json#chorus:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json), [manual-chorus-blocks.json#chorus:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json).

### REQ-LEG-CHORUS-006 — Feedback polarity

**D11.** Live 11 predecessor only: Feedback controls returned output and Polarity selects its sign; numerical feedback limits and stability are not specified. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-chorus-blocks.json#chorus:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json).

### REQ-LEG-CHORUS-007 — Dry and wet balance

**D11.** Live 11 predecessor only: Dry/Wet balances dry and processed signals; 100% is documented for a return track. This supplies no mix coefficients or null tolerance. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-chorus-blocks.json#chorus:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json).

### REQ-LEG-CHORUS-008 — Crisp and predecessor loading

**D11.** Live 11 predecessor only: The Live 11 text says older Sets retain Chorus and exposes Crisp in the title context menu. Crisp is described as normally enabled except when loading older-version Sets. This does not define a constructor default or migration rule for 12.4.3. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-chorus-blocks.json#chorus:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json), [manual-chorus-blocks.json#chorus:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-chorus-blocks.json).

### REQ-LEG-CHORUS-009 — Target parity and migration

**U.** Whether Chorus in 12.4.3 exposes, preserves, migrates or changes any predecessor control/state/audio behavior is unknown. Matching names/classes and the retained preset do not establish historical Set compatibility, replacement with a modern device, a supported upgrade action or an old-filter submode.

Evidence: [package-observations.json#class=Chorus](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-CHORUS-010 — Audio, clock and numerical behavior

**U.** Chorus exact response, latency, smoothing, overload/headroom, disabled/silent path, sample/block dependence, random laws where relevant, modulation/restart phase and tail are unknown. Predecessor adjectives and schema fields supply no target DSP or timing tolerance.

### REQ-LEG-CHORUS-011 — Automation, persistence and lifecycle

**U.** Chorus automation/clip-envelope/macro/manual ownership, undo grouping, preset/Set/random/tail state, malformed-input policy, cancellation atomicity, missing routes and bypass/removal/engine/Set teardown remain unknown. Shared owners apply only within their stated scopes.

## Erosion Legacy

### REQ-LEG-EROSION-001 — Retained package identity

**Dpkg.** The pinned schema declares Erosion; the single retained preset for Erosion Legacy has /Ableton/Erosion, Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. This is a file/profile observation only. It proves no current constructor default, UI range, enum interpretation, automation eligibility or audio behavior.

Evidence: [schema-fields.json#class=Erosion](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/schema-fields.json), [package-observations.json#class=Erosion](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-EROSION-002 — Carrier and X-Y editing

**D11.** Live 11 predecessor only: The predecessor describes degradation by a short modulated delay using filtered noise or sine. X changes carrier/noise center frequency and Y modulation Amount. This is a signal-role description, not a required internal implementation. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-erosion-blocks.json#erosion:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-erosion-blocks.json), [manual-erosion-blocks.json#erosion:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-erosion-blocks.json).

### REQ-LEG-EROSION-003 — Width eligibility and modifier

**D11.** Live 11 predecessor only: Alt on Windows or Option on macOS makes vertical X-Y dragging edit noise bandwidth; Width has no sound effect and is not adjustable in Sine mode according to this predecessor text. No inactive stored-value behavior is established. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-erosion-blocks.json#erosion:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-erosion-blocks.json), [manual-erosion-blocks.json#erosion:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-erosion-blocks.json).

### REQ-LEG-EROSION-004 — Wide Noise stereo scope

**D11.** Live 11 predecessor only: Noise and Sine use a shared modulation generator; Wide Noise describes independent left/right noise generators. No random samples, distribution or correlation tolerance is established. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-erosion-blocks.json#erosion:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-erosion-blocks.json).

### REQ-LEG-EROSION-005 — Target parity and migration

**U.** Whether Erosion Legacy in 12.4.3 exposes, preserves, migrates or changes any predecessor control/state/audio behavior is unknown. Matching names/classes and the retained preset do not establish historical Set compatibility, replacement with a modern device, a supported upgrade action or an old-filter submode.

Evidence: [package-observations.json#class=Erosion](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-EROSION-006 — Audio, clock and numerical behavior

**U.** Erosion Legacy exact response, latency, smoothing, overload/headroom, disabled/silent path, sample/block dependence, random laws where relevant, modulation/restart phase and tail are unknown. Predecessor adjectives and schema fields supply no target DSP or timing tolerance.

### REQ-LEG-EROSION-007 — Automation, persistence and lifecycle

**U.** Erosion Legacy automation/clip-envelope/macro/manual ownership, undo grouping, preset/Set/random/tail state, malformed-input policy, cancellation atomicity, missing routes and bypass/removal/engine/Set teardown remain unknown. Shared owners apply only within their stated scopes.

## Flanger

### REQ-LEG-FLANGER-001 — Retained package identity

**Dpkg.** The pinned schema declares Flanger; the single retained preset for Flanger has /Ableton/Flanger, Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. This is a file/profile observation only. It proves no current constructor default, UI range, enum interpretation, automation eligibility or audio behavior.

Evidence: [schema-fields.json#class=Flanger](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/schema-fields.json), [package-observations.json#class=Flanger](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-FLANGER-002 — Delay, feedback and X-Y

**D11.** Live 11 predecessor only: The predecessor describes two parallel modulated delays. Delay Time and Feedback are edited together in X-Y; Polarity selects plus/minus feedback sign. No delay interpolation, feedback bound or stability law follows. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-flanger-blocks.json#flanger:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-flanger-blocks.json), [manual-flanger-blocks.json#flanger:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-flanger-blocks.json).

### REQ-LEG-FLANGER-003 — Envelope influence

**D11.** Live 11 predecessor only: Envelope Amount allows positive and negative delay modulation; Attack/Release shape its response. No follower equation is established. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-flanger-blocks.json#flanger:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-flanger-blocks.json).

### REQ-LEG-FLANGER-004 — LFO shapes and timing

**D11.** Live 11 predecessor only: Two channel LFOs modulate delay time with sine, square, triangle, rising/falling saw or random; Amount sets influence and Rate supports Hz or song-tempo subdivisions. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-flanger-blocks.json#flanger:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-flanger-blocks.json), [manual-flanger-blocks.json#flanger:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-flanger-blocks.json).

### REQ-LEG-FLANGER-005 — Phase and Spin

**D11.** Live 11 predecessor only: Phase offsets equal-frequency stereo LFOs, including opposing extrema at 180 degrees; Spin detunes the two LFO rates. Neither defines an output pan or restart law. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-flanger-blocks.json#flanger:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-flanger-blocks.json), [manual-flanger-blocks.json#flanger:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-flanger-blocks.json).

### REQ-LEG-FLANGER-006 — High-pass and mix

**D11.** Live 11 predecessor only: HiPass removes lower frequencies from delayed signal; Dry/Wet balances processed and dry paths and 100% is documented for returns. Filter/mix coefficients are unspecified. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-flanger-blocks.json#flanger:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-flanger-blocks.json), [manual-flanger-blocks.json#flanger:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-flanger-blocks.json).

### REQ-LEG-FLANGER-007 — Quality option

**D11.** Live 11 predecessor only: A title-bar context-menu Hi-Quality option is documented. Brighter-sound wording provides no measured spectral criterion; the CPU adjective is context only, not an application-performance requirement. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-flanger-blocks.json#flanger:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-flanger-blocks.json).

### REQ-LEG-FLANGER-008 — Target parity and migration

**U.** Whether Flanger in 12.4.3 exposes, preserves, migrates or changes any predecessor control/state/audio behavior is unknown. Matching names/classes and the retained preset do not establish historical Set compatibility, replacement with a modern device, a supported upgrade action or an old-filter submode.

Evidence: [package-observations.json#class=Flanger](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-FLANGER-009 — Audio, clock and numerical behavior

**U.** Flanger exact response, latency, smoothing, overload/headroom, disabled/silent path, sample/block dependence, random laws where relevant, modulation/restart phase and tail are unknown. Predecessor adjectives and schema fields supply no target DSP or timing tolerance.

### REQ-LEG-FLANGER-010 — Automation, persistence and lifecycle

**U.** Flanger automation/clip-envelope/macro/manual ownership, undo grouping, preset/Set/random/tail state, malformed-input policy, cancellation atomicity, missing routes and bypass/removal/engine/Set teardown remain unknown. Shared owners apply only within their stated scopes.

## Frequency Shifter

### REQ-LEG-FREQUENCY-SHIFTER-001 — Retained package identity

**Dpkg.** The pinned schema declares FrequencyShifter; the single retained preset for Frequency Shifter has /Ableton/FrequencyShifter, Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. This is a file/profile observation only. It proves no current constructor default, UI range, enum interpretation, automation eligibility or audio behavior.

Evidence: [schema-fields.json#class=FrequencyShifter](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/schema-fields.json), [package-observations.json#class=FrequencyShifter](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-FREQUENCY-SHIFTER-002 — Additive frequency shifting

**D11.** Live 11 predecessor only: Shift moves incoming frequencies by an additive Hz amount through Coarse/Fine, rather than preserving harmonic ratios through pitch transposition. The documentary example maps a 440 Hz sine with +100 Hz shift to 540 Hz. No target tolerance, negative-frequency or aliasing rule follows. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-frequency-shifter-blocks.json#frequency-shifter:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json), [manual-frequency-shifter-blocks.json#frequency-shifter:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json), [manual-frequency-shifter-blocks.json#frequency-shifter:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json).

### REQ-LEG-FREQUENCY-SHIFTER-003 — Ring mode

**D11.** Live 11 predecessor only: Ring adds and subtracts the selected frequency; its 440 Hz input/100 Hz example names 340 and 540 Hz components. Relative amplitudes and implementation are unspecified. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-frequency-shifter-blocks.json#frequency-shifter:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json).

### REQ-LEG-FREQUENCY-SHIFTER-004 — Drive eligibility and post-mix role

**D11.** Live 11 predecessor only: Drive distortion is offered only in Ring mode. Enabling it renames Dry/Wet to Mix; Drive is after Mix, allowing distortion with Mix at 0%. No transfer curve or input/output level law follows. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-frequency-shifter-blocks.json#frequency-shifter:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json), [manual-frequency-shifter-blocks.json#frequency-shifter:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json).

### REQ-LEG-FREQUENCY-SHIFTER-005 — Wide and Spread

**D11.** Live 11 predecessor only: Wide inverts Spread sign for the right channel, moving right downward and left upward with increased positive Spread; Wide has no stated effect at Spread zero. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-frequency-shifter-blocks.json#frequency-shifter:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json).

### REQ-LEG-FREQUENCY-SHIFTER-006 — LFO modes and Rate

**D11.** Live 11 predecessor only: Per-channel frequency LFOs offer sine, square, triangle, rising/falling saw and random; Amount sets influence and Rate supports Hz or tempo subdivisions. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-frequency-shifter-blocks.json#frequency-shifter:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json), [manual-frequency-shifter-blocks.json#frequency-shifter:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json).

### REQ-LEG-FREQUENCY-SHIFTER-007 — Stereo LFO and random exceptions

**D11.** Live 11 predecessor only: Phase offsets equal-rate LFOs and Spin detunes their rates. For random waveform the text says Phase and Spin do not affect sound; no deterministic sample equality or random law follows. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-frequency-shifter-blocks.json#frequency-shifter:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json), [manual-frequency-shifter-blocks.json#frequency-shifter:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json), [manual-frequency-shifter-blocks.json#frequency-shifter:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json).

### REQ-LEG-FREQUENCY-SHIFTER-008 — Mix-dependent tips

**D11.** Live 11 predecessor only: Dry/Wet balances processed and dry. The predecessor tips require both paths for small-shift phasing and describe sub-audible Ring settings as tremolo. These qualitative effects provide no amplitude or perceptual acceptance metric. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-frequency-shifter-blocks.json#frequency-shifter:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json), [manual-frequency-shifter-blocks.json#frequency-shifter:B022](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json), [manual-frequency-shifter-blocks.json#frequency-shifter:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-frequency-shifter-blocks.json).

### REQ-LEG-FREQUENCY-SHIFTER-009 — Target parity and migration

**U.** Whether Frequency Shifter in 12.4.3 exposes, preserves, migrates or changes any predecessor control/state/audio behavior is unknown. Matching names/classes and the retained preset do not establish historical Set compatibility, replacement with a modern device, a supported upgrade action or an old-filter submode.

Evidence: [package-observations.json#class=FrequencyShifter](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-FREQUENCY-SHIFTER-010 — Audio, clock and numerical behavior

**U.** Frequency Shifter exact response, latency, smoothing, overload/headroom, disabled/silent path, sample/block dependence, random laws where relevant, modulation/restart phase and tail are unknown. Predecessor adjectives and schema fields supply no target DSP or timing tolerance.

### REQ-LEG-FREQUENCY-SHIFTER-011 — Automation, persistence and lifecycle

**U.** Frequency Shifter automation/clip-envelope/macro/manual ownership, undo grouping, preset/Set/random/tail state, malformed-input policy, cancellation atomicity, missing routes and bypass/removal/engine/Set teardown remain unknown. Shared owners apply only within their stated scopes.

## Phaser

### REQ-LEG-PHASER-001 — Retained package identity

**Dpkg.** The pinned schema declares Phaser; the single retained preset for Phaser has /Ableton/Phaser, Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. This is a file/profile observation only. It proves no current constructor default, UI range, enum interpretation, automation eligibility or audio behavior.

Evidence: [schema-fields.json#class=Phaser](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/schema-fields.json), [package-observations.json#class=Phaser](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-PHASER-002 — Frequency, Poles and Feedback

**D11.** Live 11 predecessor only: The predecessor describes phase-based spectral notches. Poles, Feedback and Frequency change the response, with Frequency/Feedback available together in X-Y. Exact all-pass structure, pole locations and notch/peak equations are not mandated. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-phaser-blocks.json#phaser:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-phaser-blocks.json), [manual-phaser-blocks.json#phaser:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-phaser-blocks.json).

### REQ-LEG-PHASER-003 — Space, Earth and Color

**D11.** Live 11 predecessor only: Space and Earth select notch spacing character and Color further adjusts it. No spectral-spacing formula is specified. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-phaser-blocks.json#phaser:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-phaser-blocks.json).

### REQ-LEG-PHASER-004 — Envelope influence

**D11.** Live 11 predecessor only: Positive/negative Envelope Amount changes filter-frequency modulation; Attack/Release shape response. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-phaser-blocks.json#phaser:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-phaser-blocks.json).

### REQ-LEG-PHASER-005 — LFO shapes and stereo timing

**D11.** Live 11 predecessor only: Left/right frequency LFOs offer six shapes, Hz or tempo Rate, Amount, Phase and Spin. Phase 180 describes opposing extrema at equal rate; Spin detunes rates. No audio phase matrix or restart law is specified. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-phaser-blocks.json#phaser:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-phaser-blocks.json), [manual-phaser-blocks.json#phaser:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-phaser-blocks.json), [manual-phaser-blocks.json#phaser:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-phaser-blocks.json), [manual-phaser-blocks.json#phaser:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-phaser-blocks.json).

### REQ-LEG-PHASER-006 — Dry and wet balance

**D11.** Live 11 predecessor only: Dry/Wet balances dry/processed paths; 100% is documented for return-track use. No coefficients or phase cancellation tolerance follows. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-phaser-blocks.json#phaser:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-phaser-blocks.json).

### REQ-LEG-PHASER-007 — Target parity and migration

**U.** Whether Phaser in 12.4.3 exposes, preserves, migrates or changes any predecessor control/state/audio behavior is unknown. Matching names/classes and the retained preset do not establish historical Set compatibility, replacement with a modern device, a supported upgrade action or an old-filter submode.

Evidence: [package-observations.json#class=Phaser](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-PHASER-008 — Audio, clock and numerical behavior

**U.** Phaser exact response, latency, smoothing, overload/headroom, disabled/silent path, sample/block dependence, random laws where relevant, modulation/restart phase and tail are unknown. Predecessor adjectives and schema fields supply no target DSP or timing tolerance.

### REQ-LEG-PHASER-009 — Automation, persistence and lifecycle

**U.** Phaser automation/clip-envelope/macro/manual ownership, undo grouping, preset/Set/random/tail state, malformed-input policy, cancellation atomicity, missing routes and bypass/removal/engine/Set teardown remain unknown. Shared owners apply only within their stated scopes.

## Redux Legacy

### REQ-LEG-REDUX-001 — Retained package identity

**Dpkg.** The pinned schema declares Redux; the single retained preset for Redux Legacy has /Ableton/Redux, Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. This is a file/profile observation only. It proves no current constructor default, UI range, enum interpretation, automation eligibility or audio behavior.

Evidence: [schema-fields.json#class=Redux](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/schema-fields.json), [package-observations.json#class=Redux](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-REDUX-002 — Downsample factor

**D11.** Live 11 predecessor only: The predecessor uses Downsample plus a mode switch. Its factor-1 example passes each sample and factor-2 example processes every second sample. This is limited to the Downsample section, not whole-device identity when bit reduction is active. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-redux-legacy-blocks.json#redux-legacy:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-redux-legacy-blocks.json), [manual-redux-legacy-blocks.json#redux-legacy:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-redux-legacy-blocks.json), [manual-redux-legacy-blocks.json#redux-legacy:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-redux-legacy-blocks.json).

### REQ-LEG-REDUX-003 — Soft and Hard

**D11.** Live 11 predecessor only: Soft is described as interpolating over a smaller range up to a factor of 20, Hard as non-interpolating over a larger range up to 200. No interpolation kernel or fractional-factor rule is supplied. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-redux-legacy-blocks.json#redux-legacy:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-redux-legacy-blocks.json).

### REQ-LEG-REDUX-004 — Bit reduction

**D11.** Live 11 predecessor only: The predecessor describes amplitude quantization: 8 bits as 256 levels and 1 bit as full positive/negative output. Zero handling, rounding, scaling and dither are unspecified. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-redux-legacy-blocks.json#redux-legacy:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-redux-legacy-blocks.json), [manual-redux-legacy-blocks.json#redux-legacy:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-redux-legacy-blocks.json).

### REQ-LEG-REDUX-005 — Overload indication and bit enable

**D11.** Live 11 predecessor only: The predecessor describes clipping above its 0 dB input convention and a red overload LED, and permits disabling Bit Reduction. No reference calibration, exact threshold tie, LED hold timing or CPU criterion is established. Target 12.4.3 Legacy applicability is U.

Evidence: [manual-redux-legacy-blocks.json#redux-legacy:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-redux-legacy-blocks.json), [manual-redux-legacy-blocks.json#redux-legacy:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manual-redux-legacy-blocks.json).

### REQ-LEG-REDUX-006 — Target parity and migration

**U.** Whether Redux Legacy in 12.4.3 exposes, preserves, migrates or changes any predecessor control/state/audio behavior is unknown. Matching names/classes and the retained preset do not establish historical Set compatibility, replacement with a modern device, a supported upgrade action or an old-filter submode.

Evidence: [package-observations.json#class=Redux](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/package-observations.json).

### REQ-LEG-REDUX-007 — Audio, clock and numerical behavior

**U.** Redux Legacy exact response, latency, smoothing, overload/headroom, disabled/silent path, sample/block dependence, random laws where relevant, modulation/restart phase and tail are unknown. Predecessor adjectives and schema fields supply no target DSP or timing tolerance.

### REQ-LEG-REDUX-008 — Automation, persistence and lifecycle

**U.** Redux Legacy automation/clip-envelope/macro/manual ownership, undo grouping, preset/Set/random/tail state, malformed-input policy, cancellation atomicity, missing routes and bypass/removal/engine/Set teardown remain unknown. Shared owners apply only within their stated scopes.

## Case index and counts

Full setup, action, expected result, comparison and provenance are in the retained
[cases](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/cases.json). The derived [requirement index](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/requirements.json)
matches the clauses above. Each D11 clause has a source-content case and a
separate ungraded target probe. Lifecycle and numeric gaps retain concrete
unknown probes rather than an invented source-independent oracle.

| Device | Requirements | D11 / Dpkg / U requirements | Cases | D11 / Dpkg / U cases |
| --- | --- | --- | --- | --- |
| Auto Filter Legacy | 13 | 9 / 1 / 3 | 29 | 9 / 1 / 19 |
| Auto Pan | 8 | 4 / 1 / 3 | 19 | 4 / 1 / 14 |
| Chorus | 11 | 7 / 1 / 3 | 25 | 7 / 1 / 17 |
| Erosion Legacy | 7 | 3 / 1 / 3 | 17 | 3 / 1 / 13 |
| Flanger | 10 | 6 / 1 / 3 | 23 | 6 / 1 / 16 |
| Frequency Shifter | 11 | 7 / 1 / 3 | 25 | 7 / 1 / 17 |
| Phaser | 9 | 5 / 1 / 3 | 21 | 5 / 1 / 15 |
| Redux Legacy | 8 | 4 / 1 / 3 | 19 | 4 / 1 / 14 |

Total: **77 requirements (45 D11, 8 Dpkg, 24 U); 178 cases (45 D11, 8 Dpkg, 125 U)**. All 178 target expectations are null.

### Auto Filter Legacy cases

| Case | Requirement | Kind | Scope | Scenario |
| --- | --- | --- | --- | --- |
| LEG-AUTO-FILTER-001 | REQ-LEG-AUTO-FILTER-001 | package | Dpkg; target U | Schema and exemplar identity |
| LEG-AUTO-FILTER-002 | REQ-LEG-AUTO-FILTER-002 | documentary | D11; target U | Filter choices and circuits documentary clause |
| LEG-AUTO-FILTER-003 | REQ-LEG-AUTO-FILTER-002 | positive | U; target U | Filter choices and circuits target probe |
| LEG-AUTO-FILTER-004 | REQ-LEG-AUTO-FILTER-003 | documentary | D11; target U | Drive eligibility documentary clause |
| LEG-AUTO-FILTER-005 | REQ-LEG-AUTO-FILTER-003 | boundary | U; target U | Drive eligibility target probe |
| LEG-AUTO-FILTER-006 | REQ-LEG-AUTO-FILTER-004 | documentary | D11; target U | Frequency and resonance editing documentary clause |
| LEG-AUTO-FILTER-007 | REQ-LEG-AUTO-FILTER-004 | positive | U; target U | Frequency and resonance editing target probe |
| LEG-AUTO-FILTER-008 | REQ-LEG-AUTO-FILTER-005 | documentary | D11; target U | Morph traversal and snapping documentary clause |
| LEG-AUTO-FILTER-009 | REQ-LEG-AUTO-FILTER-005 | positive | U; target U | Morph traversal and snapping target probe |
| LEG-AUTO-FILTER-010 | REQ-LEG-AUTO-FILTER-006 | documentary | D11; target U | Envelope control documentary clause |
| LEG-AUTO-FILTER-011 | REQ-LEG-AUTO-FILTER-006 | positive | U; target U | Envelope control target probe |
| LEG-AUTO-FILTER-012 | REQ-LEG-AUTO-FILTER-007 | documentary | D11; target U | External envelope trigger documentary clause |
| LEG-AUTO-FILTER-013 | REQ-LEG-AUTO-FILTER-007 | positive | U; target U | External envelope trigger target probe |
| LEG-AUTO-FILTER-014 | REQ-LEG-AUTO-FILTER-008 | documentary | D11; target U | LFO timing and stereo roles documentary clause |
| LEG-AUTO-FILTER-015 | REQ-LEG-AUTO-FILTER-008 | positive | U; target U | LFO timing and stereo roles target probe |
| LEG-AUTO-FILTER-016 | REQ-LEG-AUTO-FILTER-009 | documentary | D11; target U | Quantize Beat documentary clause |
| LEG-AUTO-FILTER-017 | REQ-LEG-AUTO-FILTER-009 | positive | U; target U | Quantize Beat target probe |
| LEG-AUTO-FILTER-018 | REQ-LEG-AUTO-FILTER-010 | documentary | D11; target U | Older filter upgrade documentary clause |
| LEG-AUTO-FILTER-019 | REQ-LEG-AUTO-FILTER-010 | positive | U; target U | Older filter upgrade target probe |
| LEG-AUTO-FILTER-020 | REQ-LEG-AUTO-FILTER-011 | migration | U; target U | Load, predecessor and successor identity |
| LEG-AUTO-FILTER-021 | REQ-LEG-AUTO-FILTER-012 | sample-rate | U; target U | Rates, transport and scheduling |
| LEG-AUTO-FILTER-022 | REQ-LEG-AUTO-FILTER-012 | negative | U; target U | Silence, levels and inactive controls |
| LEG-AUTO-FILTER-023 | REQ-LEG-AUTO-FILTER-013 | automation | U; target U | Automation ownership |
| LEG-AUTO-FILTER-024 | REQ-LEG-AUTO-FILTER-013 | persistence | U; target U | Set and preset reopen |
| LEG-AUTO-FILTER-025 | REQ-LEG-AUTO-FILTER-013 | undo | U; target U | Undo and redo |
| LEG-AUTO-FILTER-026 | REQ-LEG-AUTO-FILTER-013 | malformed | U; target U | Malformed and out-of-range state |
| LEG-AUTO-FILTER-027 | REQ-LEG-AUTO-FILTER-013 | cancel | U; target U | Interrupted edit or load |
| LEG-AUTO-FILTER-028 | REQ-LEG-AUTO-FILTER-013 | teardown | U; target U | Bypass, removal and engine loss |
| LEG-AUTO-FILTER-029 | REQ-LEG-AUTO-FILTER-013 | sidechain | U; target U | External route availability |

### Auto Pan cases

| Case | Requirement | Kind | Scope | Scenario |
| --- | --- | --- | --- | --- |
| LEG-AUTO-PAN-001 | REQ-LEG-AUTO-PAN-001 | package | Dpkg; target U | Schema and exemplar identity |
| LEG-AUTO-PAN-002 | REQ-LEG-AUTO-PAN-002 | documentary | D11; target U | Channel amplitude modulation documentary clause |
| LEG-AUTO-PAN-003 | REQ-LEG-AUTO-PAN-002 | positive | U; target U | Channel amplitude modulation target probe |
| LEG-AUTO-PAN-004 | REQ-LEG-AUTO-PAN-003 | documentary | D11; target U | Shape and inversion documentary clause |
| LEG-AUTO-PAN-005 | REQ-LEG-AUTO-PAN-003 | positive | U; target U | Shape and inversion target probe |
| LEG-AUTO-PAN-006 | REQ-LEG-AUTO-PAN-004 | documentary | D11; target U | Rate units documentary clause |
| LEG-AUTO-PAN-007 | REQ-LEG-AUTO-PAN-004 | positive | U; target U | Rate units target probe |
| LEG-AUTO-PAN-008 | REQ-LEG-AUTO-PAN-005 | documentary | D11; target U | Phase and offset documentary clause |
| LEG-AUTO-PAN-009 | REQ-LEG-AUTO-PAN-005 | boundary | U; target U | Phase and offset target probe |
| LEG-AUTO-PAN-010 | REQ-LEG-AUTO-PAN-006 | migration | U; target U | Load, predecessor and successor identity |
| LEG-AUTO-PAN-011 | REQ-LEG-AUTO-PAN-007 | sample-rate | U; target U | Rates, transport and scheduling |
| LEG-AUTO-PAN-012 | REQ-LEG-AUTO-PAN-007 | negative | U; target U | Silence, levels and inactive controls |
| LEG-AUTO-PAN-013 | REQ-LEG-AUTO-PAN-008 | automation | U; target U | Automation ownership |
| LEG-AUTO-PAN-014 | REQ-LEG-AUTO-PAN-008 | persistence | U; target U | Set and preset reopen |
| LEG-AUTO-PAN-015 | REQ-LEG-AUTO-PAN-008 | undo | U; target U | Undo and redo |
| LEG-AUTO-PAN-016 | REQ-LEG-AUTO-PAN-008 | malformed | U; target U | Malformed and out-of-range state |
| LEG-AUTO-PAN-017 | REQ-LEG-AUTO-PAN-008 | cancel | U; target U | Interrupted edit or load |
| LEG-AUTO-PAN-018 | REQ-LEG-AUTO-PAN-008 | teardown | U; target U | Bypass, removal and engine loss |
| LEG-AUTO-PAN-019 | REQ-LEG-AUTO-PAN-008 | sidechain | U; target U | External route availability |

### Chorus cases

| Case | Requirement | Kind | Scope | Scenario |
| --- | --- | --- | --- | --- |
| LEG-CHORUS-001 | REQ-LEG-CHORUS-001 | package | Dpkg; target U | Schema and exemplar identity |
| LEG-CHORUS-002 | REQ-LEG-CHORUS-002 | documentary | D11; target U | Independent delay and high-pass controls documentary clause |
| LEG-CHORUS-003 | REQ-LEG-CHORUS-002 | positive | U; target U | Independent delay and high-pass controls target probe |
| LEG-CHORUS-004 | REQ-LEG-CHORUS-003 | documentary | D11; target U | Delay 2 modes documentary clause |
| LEG-CHORUS-005 | REQ-LEG-CHORUS-003 | boundary | U; target U | Delay 2 modes target probe |
| LEG-CHORUS-006 | REQ-LEG-CHORUS-004 | documentary | D11; target U | Delay linking documentary clause |
| LEG-CHORUS-007 | REQ-LEG-CHORUS-004 | positive | U; target U | Delay linking target probe |
| LEG-CHORUS-008 | REQ-LEG-CHORUS-005 | documentary | D11; target U | Modulation edit axes and multiplier documentary clause |
| LEG-CHORUS-009 | REQ-LEG-CHORUS-005 | positive | U; target U | Modulation edit axes and multiplier target probe |
| LEG-CHORUS-010 | REQ-LEG-CHORUS-006 | documentary | D11; target U | Feedback polarity documentary clause |
| LEG-CHORUS-011 | REQ-LEG-CHORUS-006 | positive | U; target U | Feedback polarity target probe |
| LEG-CHORUS-012 | REQ-LEG-CHORUS-007 | documentary | D11; target U | Dry and wet balance documentary clause |
| LEG-CHORUS-013 | REQ-LEG-CHORUS-007 | positive | U; target U | Dry and wet balance target probe |
| LEG-CHORUS-014 | REQ-LEG-CHORUS-008 | documentary | D11; target U | Crisp and predecessor loading documentary clause |
| LEG-CHORUS-015 | REQ-LEG-CHORUS-008 | positive | U; target U | Crisp and predecessor loading target probe |
| LEG-CHORUS-016 | REQ-LEG-CHORUS-009 | migration | U; target U | Load, predecessor and successor identity |
| LEG-CHORUS-017 | REQ-LEG-CHORUS-010 | sample-rate | U; target U | Rates, transport and scheduling |
| LEG-CHORUS-018 | REQ-LEG-CHORUS-010 | negative | U; target U | Silence, levels and inactive controls |
| LEG-CHORUS-019 | REQ-LEG-CHORUS-011 | automation | U; target U | Automation ownership |
| LEG-CHORUS-020 | REQ-LEG-CHORUS-011 | persistence | U; target U | Set and preset reopen |
| LEG-CHORUS-021 | REQ-LEG-CHORUS-011 | undo | U; target U | Undo and redo |
| LEG-CHORUS-022 | REQ-LEG-CHORUS-011 | malformed | U; target U | Malformed and out-of-range state |
| LEG-CHORUS-023 | REQ-LEG-CHORUS-011 | cancel | U; target U | Interrupted edit or load |
| LEG-CHORUS-024 | REQ-LEG-CHORUS-011 | teardown | U; target U | Bypass, removal and engine loss |
| LEG-CHORUS-025 | REQ-LEG-CHORUS-011 | sidechain | U; target U | External route availability |

### Erosion Legacy cases

| Case | Requirement | Kind | Scope | Scenario |
| --- | --- | --- | --- | --- |
| LEG-EROSION-001 | REQ-LEG-EROSION-001 | package | Dpkg; target U | Schema and exemplar identity |
| LEG-EROSION-002 | REQ-LEG-EROSION-002 | documentary | D11; target U | Carrier and X-Y editing documentary clause |
| LEG-EROSION-003 | REQ-LEG-EROSION-002 | positive | U; target U | Carrier and X-Y editing target probe |
| LEG-EROSION-004 | REQ-LEG-EROSION-003 | documentary | D11; target U | Width eligibility and modifier documentary clause |
| LEG-EROSION-005 | REQ-LEG-EROSION-003 | boundary | U; target U | Width eligibility and modifier target probe |
| LEG-EROSION-006 | REQ-LEG-EROSION-004 | documentary | D11; target U | Wide Noise stereo scope documentary clause |
| LEG-EROSION-007 | REQ-LEG-EROSION-004 | positive | U; target U | Wide Noise stereo scope target probe |
| LEG-EROSION-008 | REQ-LEG-EROSION-005 | migration | U; target U | Load, predecessor and successor identity |
| LEG-EROSION-009 | REQ-LEG-EROSION-006 | sample-rate | U; target U | Rates, transport and scheduling |
| LEG-EROSION-010 | REQ-LEG-EROSION-006 | negative | U; target U | Silence, levels and inactive controls |
| LEG-EROSION-011 | REQ-LEG-EROSION-007 | automation | U; target U | Automation ownership |
| LEG-EROSION-012 | REQ-LEG-EROSION-007 | persistence | U; target U | Set and preset reopen |
| LEG-EROSION-013 | REQ-LEG-EROSION-007 | undo | U; target U | Undo and redo |
| LEG-EROSION-014 | REQ-LEG-EROSION-007 | malformed | U; target U | Malformed and out-of-range state |
| LEG-EROSION-015 | REQ-LEG-EROSION-007 | cancel | U; target U | Interrupted edit or load |
| LEG-EROSION-016 | REQ-LEG-EROSION-007 | teardown | U; target U | Bypass, removal and engine loss |
| LEG-EROSION-017 | REQ-LEG-EROSION-007 | sidechain | U; target U | External route availability |

### Flanger cases

| Case | Requirement | Kind | Scope | Scenario |
| --- | --- | --- | --- | --- |
| LEG-FLANGER-001 | REQ-LEG-FLANGER-001 | package | Dpkg; target U | Schema and exemplar identity |
| LEG-FLANGER-002 | REQ-LEG-FLANGER-002 | documentary | D11; target U | Delay, feedback and X-Y documentary clause |
| LEG-FLANGER-003 | REQ-LEG-FLANGER-002 | positive | U; target U | Delay, feedback and X-Y target probe |
| LEG-FLANGER-004 | REQ-LEG-FLANGER-003 | documentary | D11; target U | Envelope influence documentary clause |
| LEG-FLANGER-005 | REQ-LEG-FLANGER-003 | positive | U; target U | Envelope influence target probe |
| LEG-FLANGER-006 | REQ-LEG-FLANGER-004 | documentary | D11; target U | LFO shapes and timing documentary clause |
| LEG-FLANGER-007 | REQ-LEG-FLANGER-004 | positive | U; target U | LFO shapes and timing target probe |
| LEG-FLANGER-008 | REQ-LEG-FLANGER-005 | documentary | D11; target U | Phase and Spin documentary clause |
| LEG-FLANGER-009 | REQ-LEG-FLANGER-005 | boundary | U; target U | Phase and Spin target probe |
| LEG-FLANGER-010 | REQ-LEG-FLANGER-006 | documentary | D11; target U | High-pass and mix documentary clause |
| LEG-FLANGER-011 | REQ-LEG-FLANGER-006 | boundary | U; target U | High-pass and mix target probe |
| LEG-FLANGER-012 | REQ-LEG-FLANGER-007 | documentary | D11; target U | Quality option documentary clause |
| LEG-FLANGER-013 | REQ-LEG-FLANGER-007 | boundary | U; target U | Quality option target probe |
| LEG-FLANGER-014 | REQ-LEG-FLANGER-008 | migration | U; target U | Load, predecessor and successor identity |
| LEG-FLANGER-015 | REQ-LEG-FLANGER-009 | sample-rate | U; target U | Rates, transport and scheduling |
| LEG-FLANGER-016 | REQ-LEG-FLANGER-009 | negative | U; target U | Silence, levels and inactive controls |
| LEG-FLANGER-017 | REQ-LEG-FLANGER-010 | automation | U; target U | Automation ownership |
| LEG-FLANGER-018 | REQ-LEG-FLANGER-010 | persistence | U; target U | Set and preset reopen |
| LEG-FLANGER-019 | REQ-LEG-FLANGER-010 | undo | U; target U | Undo and redo |
| LEG-FLANGER-020 | REQ-LEG-FLANGER-010 | malformed | U; target U | Malformed and out-of-range state |
| LEG-FLANGER-021 | REQ-LEG-FLANGER-010 | cancel | U; target U | Interrupted edit or load |
| LEG-FLANGER-022 | REQ-LEG-FLANGER-010 | teardown | U; target U | Bypass, removal and engine loss |
| LEG-FLANGER-023 | REQ-LEG-FLANGER-010 | sidechain | U; target U | External route availability |

### Frequency Shifter cases

| Case | Requirement | Kind | Scope | Scenario |
| --- | --- | --- | --- | --- |
| LEG-FREQUENCY-SHIFTER-001 | REQ-LEG-FREQUENCY-SHIFTER-001 | package | Dpkg; target U | Schema and exemplar identity |
| LEG-FREQUENCY-SHIFTER-002 | REQ-LEG-FREQUENCY-SHIFTER-002 | documentary | D11; target U | Additive frequency shifting documentary clause |
| LEG-FREQUENCY-SHIFTER-003 | REQ-LEG-FREQUENCY-SHIFTER-002 | positive | U; target U | Additive frequency shifting target probe |
| LEG-FREQUENCY-SHIFTER-004 | REQ-LEG-FREQUENCY-SHIFTER-003 | documentary | D11; target U | Ring mode documentary clause |
| LEG-FREQUENCY-SHIFTER-005 | REQ-LEG-FREQUENCY-SHIFTER-003 | positive | U; target U | Ring mode target probe |
| LEG-FREQUENCY-SHIFTER-006 | REQ-LEG-FREQUENCY-SHIFTER-004 | documentary | D11; target U | Drive eligibility and post-mix role documentary clause |
| LEG-FREQUENCY-SHIFTER-007 | REQ-LEG-FREQUENCY-SHIFTER-004 | boundary | U; target U | Drive eligibility and post-mix role target probe |
| LEG-FREQUENCY-SHIFTER-008 | REQ-LEG-FREQUENCY-SHIFTER-005 | documentary | D11; target U | Wide and Spread documentary clause |
| LEG-FREQUENCY-SHIFTER-009 | REQ-LEG-FREQUENCY-SHIFTER-005 | positive | U; target U | Wide and Spread target probe |
| LEG-FREQUENCY-SHIFTER-010 | REQ-LEG-FREQUENCY-SHIFTER-006 | documentary | D11; target U | LFO modes and Rate documentary clause |
| LEG-FREQUENCY-SHIFTER-011 | REQ-LEG-FREQUENCY-SHIFTER-006 | positive | U; target U | LFO modes and Rate target probe |
| LEG-FREQUENCY-SHIFTER-012 | REQ-LEG-FREQUENCY-SHIFTER-007 | documentary | D11; target U | Stereo LFO and random exceptions documentary clause |
| LEG-FREQUENCY-SHIFTER-013 | REQ-LEG-FREQUENCY-SHIFTER-007 | boundary | U; target U | Stereo LFO and random exceptions target probe |
| LEG-FREQUENCY-SHIFTER-014 | REQ-LEG-FREQUENCY-SHIFTER-008 | documentary | D11; target U | Mix-dependent tips documentary clause |
| LEG-FREQUENCY-SHIFTER-015 | REQ-LEG-FREQUENCY-SHIFTER-008 | boundary | U; target U | Mix-dependent tips target probe |
| LEG-FREQUENCY-SHIFTER-016 | REQ-LEG-FREQUENCY-SHIFTER-009 | migration | U; target U | Load, predecessor and successor identity |
| LEG-FREQUENCY-SHIFTER-017 | REQ-LEG-FREQUENCY-SHIFTER-010 | sample-rate | U; target U | Rates, transport and scheduling |
| LEG-FREQUENCY-SHIFTER-018 | REQ-LEG-FREQUENCY-SHIFTER-010 | negative | U; target U | Silence, levels and inactive controls |
| LEG-FREQUENCY-SHIFTER-019 | REQ-LEG-FREQUENCY-SHIFTER-011 | automation | U; target U | Automation ownership |
| LEG-FREQUENCY-SHIFTER-020 | REQ-LEG-FREQUENCY-SHIFTER-011 | persistence | U; target U | Set and preset reopen |
| LEG-FREQUENCY-SHIFTER-021 | REQ-LEG-FREQUENCY-SHIFTER-011 | undo | U; target U | Undo and redo |
| LEG-FREQUENCY-SHIFTER-022 | REQ-LEG-FREQUENCY-SHIFTER-011 | malformed | U; target U | Malformed and out-of-range state |
| LEG-FREQUENCY-SHIFTER-023 | REQ-LEG-FREQUENCY-SHIFTER-011 | cancel | U; target U | Interrupted edit or load |
| LEG-FREQUENCY-SHIFTER-024 | REQ-LEG-FREQUENCY-SHIFTER-011 | teardown | U; target U | Bypass, removal and engine loss |
| LEG-FREQUENCY-SHIFTER-025 | REQ-LEG-FREQUENCY-SHIFTER-011 | sidechain | U; target U | External route availability |

### Phaser cases

| Case | Requirement | Kind | Scope | Scenario |
| --- | --- | --- | --- | --- |
| LEG-PHASER-001 | REQ-LEG-PHASER-001 | package | Dpkg; target U | Schema and exemplar identity |
| LEG-PHASER-002 | REQ-LEG-PHASER-002 | documentary | D11; target U | Frequency, Poles and Feedback documentary clause |
| LEG-PHASER-003 | REQ-LEG-PHASER-002 | positive | U; target U | Frequency, Poles and Feedback target probe |
| LEG-PHASER-004 | REQ-LEG-PHASER-003 | documentary | D11; target U | Space, Earth and Color documentary clause |
| LEG-PHASER-005 | REQ-LEG-PHASER-003 | positive | U; target U | Space, Earth and Color target probe |
| LEG-PHASER-006 | REQ-LEG-PHASER-004 | documentary | D11; target U | Envelope influence documentary clause |
| LEG-PHASER-007 | REQ-LEG-PHASER-004 | positive | U; target U | Envelope influence target probe |
| LEG-PHASER-008 | REQ-LEG-PHASER-005 | documentary | D11; target U | LFO shapes and stereo timing documentary clause |
| LEG-PHASER-009 | REQ-LEG-PHASER-005 | positive | U; target U | LFO shapes and stereo timing target probe |
| LEG-PHASER-010 | REQ-LEG-PHASER-006 | documentary | D11; target U | Dry and wet balance documentary clause |
| LEG-PHASER-011 | REQ-LEG-PHASER-006 | boundary | U; target U | Dry and wet balance target probe |
| LEG-PHASER-012 | REQ-LEG-PHASER-007 | migration | U; target U | Load, predecessor and successor identity |
| LEG-PHASER-013 | REQ-LEG-PHASER-008 | sample-rate | U; target U | Rates, transport and scheduling |
| LEG-PHASER-014 | REQ-LEG-PHASER-008 | negative | U; target U | Silence, levels and inactive controls |
| LEG-PHASER-015 | REQ-LEG-PHASER-009 | automation | U; target U | Automation ownership |
| LEG-PHASER-016 | REQ-LEG-PHASER-009 | persistence | U; target U | Set and preset reopen |
| LEG-PHASER-017 | REQ-LEG-PHASER-009 | undo | U; target U | Undo and redo |
| LEG-PHASER-018 | REQ-LEG-PHASER-009 | malformed | U; target U | Malformed and out-of-range state |
| LEG-PHASER-019 | REQ-LEG-PHASER-009 | cancel | U; target U | Interrupted edit or load |
| LEG-PHASER-020 | REQ-LEG-PHASER-009 | teardown | U; target U | Bypass, removal and engine loss |
| LEG-PHASER-021 | REQ-LEG-PHASER-009 | sidechain | U; target U | External route availability |

### Redux Legacy cases

| Case | Requirement | Kind | Scope | Scenario |
| --- | --- | --- | --- | --- |
| LEG-REDUX-001 | REQ-LEG-REDUX-001 | package | Dpkg; target U | Schema and exemplar identity |
| LEG-REDUX-002 | REQ-LEG-REDUX-002 | documentary | D11; target U | Downsample factor documentary clause |
| LEG-REDUX-003 | REQ-LEG-REDUX-002 | boundary | U; target U | Downsample factor target probe |
| LEG-REDUX-004 | REQ-LEG-REDUX-003 | documentary | D11; target U | Soft and Hard documentary clause |
| LEG-REDUX-005 | REQ-LEG-REDUX-003 | positive | U; target U | Soft and Hard target probe |
| LEG-REDUX-006 | REQ-LEG-REDUX-004 | documentary | D11; target U | Bit reduction documentary clause |
| LEG-REDUX-007 | REQ-LEG-REDUX-004 | boundary | U; target U | Bit reduction target probe |
| LEG-REDUX-008 | REQ-LEG-REDUX-005 | documentary | D11; target U | Overload indication and bit enable documentary clause |
| LEG-REDUX-009 | REQ-LEG-REDUX-005 | boundary | U; target U | Overload indication and bit enable target probe |
| LEG-REDUX-010 | REQ-LEG-REDUX-006 | migration | U; target U | Load, predecessor and successor identity |
| LEG-REDUX-011 | REQ-LEG-REDUX-007 | sample-rate | U; target U | Rates, transport and scheduling |
| LEG-REDUX-012 | REQ-LEG-REDUX-007 | negative | U; target U | Silence, levels and inactive controls |
| LEG-REDUX-013 | REQ-LEG-REDUX-008 | automation | U; target U | Automation ownership |
| LEG-REDUX-014 | REQ-LEG-REDUX-008 | persistence | U; target U | Set and preset reopen |
| LEG-REDUX-015 | REQ-LEG-REDUX-008 | undo | U; target U | Undo and redo |
| LEG-REDUX-016 | REQ-LEG-REDUX-008 | malformed | U; target U | Malformed and out-of-range state |
| LEG-REDUX-017 | REQ-LEG-REDUX-008 | cancel | U; target U | Interrupted edit or load |
| LEG-REDUX-018 | REQ-LEG-REDUX-008 | teardown | U; target U | Bypass, removal and engine loss |
| LEG-REDUX-019 | REQ-LEG-REDUX-008 | sidechain | U; target U | External route availability |

## Errors, timing, persistence and interactions

No numeric rejection/clamp, enum interpretation, saved-state identity, upgrade
transaction, undo grouping, cancellation rollback, output continuity, silence,
feedback limiter, random seed, buffer persistence or tail completion is claimed
for 12.4.3. Automation and sidechain probes use only offered interfaces. Missing
controls are observations, not passes. Sample/block rate, tempo transitions,
seek/loop/transport, real-time/offline scheduling, latency compensation,
headroom, permissions and engine loss remain open. Finite signal recipes do not
settle infinite self-oscillation or prove an inactive path is correct.

No version-proven old Set is retained. The single historical preset per profile
cannot close old-Set migration, user-library/Core Library availability or
predecessor behavioral parity. AppleDouble-like non-gzip companion entries in
the folder scan are retained unparsed and do not count as device presets.

## Analyst-only evidence and author freeze

The [source catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/sources-r3.json)
pins the official Version 11 chapter captured 2026-10-19, schema, predecessor
exemplars and derivation catalogs. D11 HTML SHA-256 is
`98a59baaa97cff409894870f26eb04697c28f8c59ecedc40ade395dcf36438d4`.
B-number citations retain exact HTML line and heading locators. The retained
modern Redux extract is context only; none of its Rate/Jitter/Shape/DC Shift
laws is assigned to Redux Legacy. The D12 Erosion migration observation is
linked through the existing distortion owner and does not establish a legacy
kernel or all-version parity.

The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manifest-author-r1.json)
pins source extracts, requirement/case/fixture data, canonical snapshots and
packet validation. This is an author freeze for independent analyst review.
It is not a release, compatibility report or whole-profile completion claim.

## Bounded revision 2 input histories

The [complete eight-section source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices-source-audit/README.md)
passed [independent partial review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/legacy-devices-source-audit-review.json).
Its114whole contexts and23literal resources remain predecessor evidence, not
atomic closure or target parity. [Current cases](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/cases-r2.json)
preserve every178old object and add16independent planned histories under existing
IDs; no normative body, source claim or old oracle changes. [Adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/adoption-r2.json)
separates historical audit zero-adoption from these current partial input additions.

| New case | Existing requirement | Bounded history |
| --- | --- | --- |
| LEG-AUTO-FILTER-030 | REQ-LEG-AUTO-FILTER-008 | AutoFilter LFO entries and simultaneous sources |
| LEG-AUTO-FILTER-031 | REQ-LEG-AUTO-FILTER-007 | AutoFilter named sidechain admission gestures |
| LEG-AUTO-FILTER-032 | REQ-LEG-AUTO-FILTER-012 | Finite self-oscillation context query |
| LEG-AUTO-FILTER-033 | REQ-LEG-AUTO-FILTER-010 | Version-proven nested old-filter Upgrade input |
| LEG-CHORUS-026 | REQ-LEG-CHORUS-008 | Chorus Crisp context-menu toggle |
| LEG-CHORUS-027 | REQ-LEG-CHORUS-002 | Chorus separate delay-time controls |
| LEG-FLANGER-024 | REQ-LEG-FLANGER-004 | Flanger actual LFO selectors and controls |
| LEG-FREQUENCY-SHIFTER-026 | REQ-LEG-FREQUENCY-SHIFTER-002 | FrequencyShifter independent Coarse/Fine inputs |
| LEG-FREQUENCY-SHIFTER-027 | REQ-LEG-FREQUENCY-SHIFTER-006 | FrequencyShifter actual LFO entries |
| LEG-PHASER-022 | REQ-LEG-PHASER-005 | Phaser actual LFO control operations |
| LEG-CHORUS-028 | REQ-LEG-CHORUS-007 | Chorus actual DryWet inputs |
| LEG-PHASER-023 | REQ-LEG-PHASER-006 | Phaser actual DryWet inputs |
| LEG-REDUX-020 | REQ-LEG-REDUX-003 | Redux SoftHard actual selections |
| LEG-EROSION-018 | REQ-LEG-EROSION-003 | Erosion named Width control input |
| LEG-REDUX-021 | REQ-LEG-REDUX-005 | Redux BitReduction enable operation |
| LEG-AUTO-FILTER-034 | REQ-LEG-AUTO-FILTER-003 | AutoFilter eligible Drive input |

[Current fixture overlay](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/fixtures-r2.json)
requires EACH genuine NONEMPTY productive input/control/wet/output before absence,
and BOTH independent relevant sources/channels/delay paths before loss/order.
UI-only choices require no audio. Nonzero observed ringing precedes input-stop
query; finite observation never proves indefinite survival. Version-proven old
Sets, editable controls and target profile admission remain absent prerequisites,
not negative passes. Crisp/SoftHard/LFO/Width/mix/Drive entries are actual future
gestures, not upgraded inspection labels or executed outputs. Existing Morph
sweep/snaps, X-Y/link/*20 and modulation/quality/post-Mix histories stay intact.

All16new documentary/actual pairs and all194current overlay actual pairs remain
null/U/unexecuted. The45D11/8Dpkg historical checks remain source/file-only; no new
quantizer/filter/RNG/clock/default/codec/CPU/migration law is adopted. Phase/Offset
versus Spin, target availability and source questions remain U. No modern law or
new profile is substituted. Current R2 independent semantic review is pending
AS OF AUTHOR FREEZE;16groups are partial and zero profiles complete.

Inspect the [current read-only checker](../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/check-r2.py)
before `python3 -B analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/check-r2.py --check`.
All44prior files/seal, old snapshots and approved source audit are preserved.
No old tool/main/import/decode/scan/replay/adapter, source capture, original/native/
UI/audio/MIDI/hardware/network/configuration/candidate action ran. Root owns
shared status; this partial analyst successor is not compatibility or release.
