---
id: RESEARCH-FULL-LIVE-COVERAGE-INVENTORY
type: research
status: current
updated: 2026-10-19
access: analysis
target: Ableton Live 12 Suite 12.4.3
revision: 3
---

# Full Live specification inventory

At the start of this inventory, the [feature map](../specs/feature-map.md) had 14
broad planning families and 19 draft specifications. Those drafts and finite
partial handoffs cover portions of those
families. They do not describe the whole product. This inventory adds a finite,
auditable discovery baseline from the installed package and the official manual.
Inventory membership establishes an obligation to investigate; it establishes no
behavioral requirement, implementation result, or compatibility pass.

## Sources and method

Observed package: [SRC-ABLETON-12-4-3](sources/ableton-live-12.4.3.md), local
`/home/ollie/Ableton Live 12 Suite.app`. The current capture rehashes the universal
Live executable to `52289af638f1b26590c84a9bc08eabdc35127883087057add909d2718a7a35ef`.
The [capture manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manifest.json)
pins every initial output, exact source paths, byte counts and SHA-256 digests. Its
[retained extractor](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/capture_inventory.py)
uses Python standard-library directory reads, gzip/XML parsing and HTML parsing.
No original executable, bytecode, Max patch or device function was executed.

Observed manual: Ableton's [Version 12 manual contents](https://www.ableton.com/en/live-manual/12/welcome-to-live/),
captured 2026-10-19. Exact [HTML bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manual-12-toc-2026-10-19.html)
hash to `584d4b61d119c96ecdb7941ef34ac9d4e0282a3e40c8bc474b6cf24892640d80`.
The document says Version 12, without a 12.4.3 revision pin. Each extracted
[TOC row](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manual-toc.json)
retains its URL, anchor, original section number and exact captured HTML line.
The anchor-derived `SURF-MAN-...` IDs are stable within this captured revision;
future title/anchor changes require explicit aliases rather than silent ID reuse.

Observed latest installed schema: `Contents/App-Resources/Schema/12.0_12402.txt`,
SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Its [retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt)
and [412 class records](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/schema-classes.json)
give exact top-level class lines and field declarations. A class declares stored
structure, not a separate user feature or an accepted-file behavioral contract.
Prior [package findings](ableton-package-structure.md) remain the canonical account
of package boundaries and the limits of dependency observations.

## Denominator and status rules

The machine-readable [denominator](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/coverage-denominator.json)
freezes initial discovery revision1. These are separate, overlapping dimensions;
adding them would count the same surface several times.

| Dimension | Finite denominator | Meaning and limit |
| --- | ---: | --- |
| Manual | 880 numbered headings, 708 leaves, 43 chapters | Every captured topic gets an applicability decision and a behavioral mapping or a reviewed reason why it creates no new obligation |
| Device profiles | 102 | 63 current native devices, 4 racks, 8 legacy native devices, 20 Max devices, 2 Max MIDI tools and 5 Max templates; profiles overlap manual topics and tool rows |
| MIDI tools | 17 | Twelve transformation and five generation topics; includes the two shipped Max tool profiles |
| Persistence vocabulary | 412 classes | Every latest-schema class needs a disposition; classes are not all devices or user features |
| Service/package identities | 13 files | 12 executable candidates and the application plist; package presence does not establish runtime topology |
| Controller/module profiles | 149 directories | Includes internal/framework support directories; does not mean 149 supported controllers |
| Keyboard binding discovery (revision2 addition) | 292 rows in27 tables | Separate retained shortcut chapter; contextual duplicates, alternatives and gestures, not292 unique or completely specified commands |

**Mapped** means a stable surface ID is routed to a proposed owning feature/spec
and an applicability question. **Specified partially** means cited clauses and
cases exist for a bounded subset. **Specified completely** requires a reviewed
finite contract covering the applicable surface's states, errors, timing,
persistence, interactions and acceptance cases, with no unresolved in-scope
clauses. **Released** means a reviewed immutable handoff exists for its declared
subset. **Implemented** and **verified** require independent evidence and are
tracked separately. The current device ledger has **zero complete profiles**.
This revision does not claim the entire discovery denominator is mapped.
The frozen JSON ledger retains discovery-time statuses. The tables on this page
route later reviewed partial drafts; those additions do not rewrite the retained
baseline or close a profile.

Every future discovery adds a new revision and changes the denominator visibly.
An unresolved platform or manual-version question stays open; it cannot be
removed from the denominator to improve a completion percentage. A reviewed
post-target or nonbehavioral disposition may close that inventory obligation,
while retaining its evidence and reason.

## Revision2 integration and keyboard discovery

The original twelve-payload inventory manifest and all initial JSON denominators
remain unchanged. This mutable revision routes later partial contracts and adds
a finer-grained [shortcut binding discovery catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/shortcut-bindings.json).
Its [source manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/manifest.json)
pins the separately retained current keyboard chapter and exact HTML row locators.
The292 rows overlap manual topics and actions already in the feature map. They
remain unclosed pending per-binding context, applicability and canonical action
reconciliation; do not add them to device/manual/schema counts or call them
executable cases. [Navigation/accessibility](../specs/keyboard-navigation.md)
provides a bounded partial owner, not coverage of every command.

## Revision3 corrected spectral-device associations

The original ledger crossed Spectral Resonator and Spectral Time's schema classes
and factory examples. The [companion device ledger revision2](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r2-spectral-aliases/devices-r2.json)
corrects only those two existing profiles: all eight named Resonator factory
presets have `Transmute` roots, while all six Time presets have `Spectral` roots.
The respective schema control vocabularies corroborate that association. Exact
14 source hashes, original attributes, class lines and a read-only audit are
pinned by the [correction manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r2-spectral-aliases/manifest.json).
The [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/inventory-spectral-alias-review.json)
verified all original presets and unchanged source history; the other100 rows,
102IDs/order/statuses and zero-complete count are unchanged. This corrects
package associations only; runtime alias/DSP behavior is unobserved.

Use the companion ledger for current class/example associations. The original
`inventory/devices.json`, all twelve initial payloads and original review remain
exact historical evidence. Their two crossed associations are superseded, not
silently rewritten. Profile/manual/schema denominators have not changed.

## Package corroboration and version uncertainty

Observed [directory captures](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/package-device-directories.json)
show all 63 native manual device names in `Builtin/Devices` category directories.
The [device ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/devices.json)
also binds them to latest-schema classes and, where available, an exact hashed
shipped preset and XML locator. Matching a named preset's root supports a device
alias. A schema name and directory alone leave the semantic alias inferred.
Shipped default/preset files are historical content carried by 12.4.3; their
Creator attributes must not be treated as reference captures made by this build.

The [preset-root inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/preset-device-roots.json)
records the parsed document denominator, zero parser failures, type occurrence
counts and exact hashed examples. Repeated preset occurrences do not add device
profiles. Max AMXD profiles retain source byte hashes and paths; their presence
does not establish patch behavior. Max application examples and arbitrary third
party content are outside this shipped Live-device list and remain part of the
separate Max-host/API scope decision.

All manual clauses remain **version-uncertain** until individually reconciled
with target evidence. Installed product-name corroboration does not validate
the current manual's detailed parameters or behavior. In particular, current
manual topics for Stem Separation, Bounce to Audio, Link Audio, Splice,
Ableton Cloud, accessibility settings and later device revisions require an
explicit 12.4.3 applicability check. No conclusion here says these features are
absent; a later manual can add behavior to an already present feature.

## Device profiles

Rows below route the device denominator; exact paths, hashes and schema locators
belong to the machine-readable ledger. `partial` means selected parameter or DSP
clauses only. Every other profile remains behaviorally unspecified. Common
device-chain persistence does not specify a device's sound or interaction model.

### Current native devices (63)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-DEVICE-AMP` | Amp | `Amp` | [Partial storage](../specs/bundled-device-parameters.md); host-emulation deferred |
| `SURF-DEVICE-AUTO-FILTER` | Auto Filter | `AutoFilter2` | [Partial filter/EQ draft](../specs/filter-eq-devices.md); corrected partial draft reviewed; exact-build U |
| `SURF-DEVICE-AUTO-PAN-TREMOLO` | Auto Pan-Tremolo | `AutoPan2` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-AUTO-SHIFT` | Auto Shift | `AutoShift` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-BEAT-REPEAT` | Beat Repeat | `BeatRepeat` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-CABINET` | Cabinet | `Cabinet` | [Partial storage](../specs/bundled-device-parameters.md); host-emulation deferred |
| `SURF-DEVICE-CHANNEL-EQ` | Channel EQ | `ChannelEq` | [Partial filter/EQ draft](../specs/filter-eq-devices.md); corrected partial draft reviewed; exact-build U |
| `SURF-DEVICE-CHORUS-ENSEMBLE` | Chorus-Ensemble | `Chorus2` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-COMPRESSOR` | Compressor | `Compressor2` | [Partial dynamics draft](../specs/dynamics-devices.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-CORPUS` | Corpus | `Corpus` | [Partial DSP/storage](../specs/device-corpus.md) |
| `SURF-DEVICE-DELAY` | Delay | `Delay` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-DRUM-BUSS` | Drum Buss | `DrumBuss` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-DYNAMIC-TUBE` | Dynamic Tube | `Tube` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-ECHO` | Echo | `Echo` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-EQ-EIGHT` | EQ Eight | `Eq8` | [Partial filter/EQ draft](../specs/filter-eq-devices.md); corrected partial draft reviewed; exact-build U |
| `SURF-DEVICE-EQ-THREE` | EQ Three | `FilterEQ3` | [Partial filter/EQ draft](../specs/filter-eq-devices.md); corrected partial draft reviewed; exact-build U |
| `SURF-DEVICE-EROSION` | Erosion | `Erosion2` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-EXTERNAL-AUDIO-EFFECT` | External Audio Effect | `BufferAudioDevice` | [Partial hardware-routing contract](../specs/external-hardware-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-FILTER-DELAY` | Filter Delay | `FilterDelay` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-GATE` | Gate | `Gate` | [Partial dynamics draft](../specs/dynamics-devices.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-GLUE-COMPRESSOR` | Glue Compressor | `GlueCompressor` | [Partial dynamics draft](../specs/dynamics-devices.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-GRAIN-DELAY` | Grain Delay | `GrainDelay` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-HYBRID-REVERB` | Hybrid Reverb | `Hybrid` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-LIMITER` | Limiter | `Limiter` | [Partial dynamics draft](../specs/dynamics-devices.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-LOOPER` | Looper | `Looper` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-MULTIBAND-DYNAMICS` | Multiband Dynamics | `MultibandDynamics` | [Partial dynamics draft](../specs/dynamics-devices.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-OVERDRIVE` | Overdrive | `Overdrive` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-PEDAL` | Pedal | `Pedal` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-PHASER-FLANGER` | Phaser-Flanger | `PhaserNew` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-REDUX` | Redux | `Redux2` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-RESONATORS` | Resonators | `Resonator` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-REVERB` | Reverb | `Reverb` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-ROAR` | Roar | `Roar` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-SATURATOR` | Saturator | `Saturator` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-SHIFTER` | Shifter | `Shifter` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-SPECTRAL-RESONATOR` | Spectral Resonator | `Transmute` (corrected association) | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-SPECTRAL-TIME` | Spectral Time | `Spectral` (corrected association) | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-SPECTRUM` | Spectrum | `SpectrumAnalyzer` | [Reviewed partial contract](../specs/device-spectrum.md); exact-build U |
| `SURF-DEVICE-TUNER` | Tuner | `Tuner` | [Reviewed partial contract](../specs/device-tuner.md); exact-build U |
| `SURF-DEVICE-UTILITY` | Utility | `StereoGain` | [Reviewed partial contract](../specs/device-utility.md); exact-build U |
| `SURF-DEVICE-VINYL-DISTORTION` | Vinyl Distortion | `Vinyl` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-VOCODER` | Vocoder | `Vocoder` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-ARPEGGIATOR` | Arpeggiator | `MidiArpeggiator` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-CC-CONTROL` | CC Control | `MidiCcControl` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-CHORD` | Chord | `MidiChord` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-NOTE-LENGTH` | Note Length | `MidiNoteLength` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-PITCH` | Pitch | `MidiPitcher` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-RANDOM` | Random | `MidiRandom` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-SCALE` | Scale | `MidiScale` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-VELOCITY` | Velocity | `MidiVelocity` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-ANALOG` | Analog | `UltraAnalog` | [Partial DSP/storage](../specs/device-analog.md) |
| `SURF-DEVICE-COLLISION` | Collision | `Collision` | [Partial DSP/storage](../specs/device-collision.md) |
| `SURF-DEVICE-DRIFT` | Drift | `Drift` | [Partial instrument contract](../specs/synthesis-instruments.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-DRUM-SAMPLER` | Drum Sampler | `DrumCell` | [Partial instrument contract](../specs/synthesis-instruments.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-ELECTRIC` | Electric | `LoungeLizard` | [Partial DSP/storage](../specs/device-electric.md) |
| `SURF-DEVICE-EXTERNAL-INSTRUMENT` | External Instrument | `BufferInstrument` | [Partial hardware-routing contract](../specs/external-hardware-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-IMPULSE` | Impulse | `InstrumentImpulse` | [Partial sample-instrument draft](../specs/device-impulse.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-MELD` | Meld | `InstrumentMeld` | [Partial instrument contract](../specs/synthesis-instruments.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-OPERATOR` | Operator | `Operator` | [Partial instrument contract](../specs/synthesis-instruments.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-SAMPLER` | Sampler | `MultiSampler` | [Partial sample-instrument draft](../specs/device-sampler.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-SIMPLER` | Simpler | `OriginalSimpler` | [Partial sample-instrument draft](../specs/device-simpler.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-TENSION` | Tension | `StringStudio` | [Partial DSP/storage](../specs/device-tension.md) |
| `SURF-DEVICE-WAVETABLE` | Wavetable | `InstrumentVector` | [Partial instrument contract](../specs/synthesis-instruments.md), partial scope reviewed; exact-build U |

### Racks (4)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-DEVICE-AUDIO-EFFECT-RACK` | Audio Effect Rack | `AudioEffectGroupDevice` | [Reviewed partial rack contract](../specs/device-racks.md); exact-build U |
| `SURF-DEVICE-MIDI-EFFECT-RACK` | MIDI Effect Rack | `MidiEffectGroupDevice` | [Reviewed partial rack contract](../specs/device-racks.md); exact-build U |
| `SURF-DEVICE-INSTRUMENT-RACK` | Instrument Rack | `InstrumentGroupDevice` | [Reviewed partial rack contract](../specs/device-racks.md); exact-build U |
| `SURF-DEVICE-DRUM-RACK` | Drum Rack | `DrumGroupDevice` | [Reviewed partial rack contract](../specs/device-racks.md); exact-build U |

### Legacy native devices (8)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-DEVICE-LEGACY-AUTO-FILTER-LEGACY` | Auto Filter Legacy | `AutoFilter` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-AUTO-PAN` | Auto Pan | `AutoPan` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-CHORUS` | Chorus | `Chorus` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-EROSION-LEGACY` | Erosion Legacy | `Erosion` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-FLANGER` | Flanger | `Flanger` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-FREQUENCY-SHIFTER` | Frequency Shifter | `FrequencyShifter` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-PHASER` | Phaser | `Phaser` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-REDUX-LEGACY` | Redux Legacy | `Redux` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |

### Shipped Max devices (20)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-MAX-ALIGN-DELAY` | Align Delay | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-ENVELOPE-FOLLOWER` | Envelope Follower | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-LFO` | LFO | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-SHAPER` | Shaper | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-CLANG` | DS Clang | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-CLAP` | DS Clap | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-CYMBAL` | DS Cymbal | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-FM` | DS FM | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-HH` | DS HH | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-KICK` | DS Kick | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-SAMPLER` | DS Sampler | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-SNARE` | DS Snare | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-TOM` | DS Tom | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-ENVELOPE-MIDI` | Envelope MIDI | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-EXPRESSION-CONTROL` | Expression Control | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-EXPRESSION-CONTROL-LEGACY` | Expression Control Legacy | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-MIDI-MONITOR` | MIDI Monitor | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-MPE-CONTROL` | MPE Control | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-NOTE-ECHO` | Note Echo | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-SHAPER-MIDI` | Shaper MIDI | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |

### Shipped Max MIDI tools (2)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-MAX-EUCLIDEAN` | Euclidean | Hashed AMXD in ledger | [Partial tool contract](../specs/midi-editing-tools.md); algorithm/Max-host/exact-build U |
| `SURF-MAX-VELOCITY-SHAPER` | Velocity Shaper | Hashed AMXD in ledger | [Partial tool contract](../specs/midi-editing-tools.md); algorithm/Max-host/exact-build U |

### Max templates (5)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-MAX-TEMPLATE-MAX-AUDIO-EFFECT` | Max Audio Effect | Hashed AMXD in ledger | [Partial host/template contract](../specs/max-for-live-hosting.md), corrected partial scope independently reviewed; runtime/API U |
| `SURF-MAX-TEMPLATE-MAX-INSTRUMENT` | Max Instrument | Hashed AMXD in ledger | [Partial host/template contract](../specs/max-for-live-hosting.md), corrected partial scope independently reviewed; runtime/API U |
| `SURF-MAX-TEMPLATE-MAX-MIDI-EFFECT` | Max MIDI Effect | Hashed AMXD in ledger | [Partial host/template contract](../specs/max-for-live-hosting.md), corrected partial scope independently reviewed; runtime/API U |
| `SURF-MAX-TEMPLATE-MAX-MIDI-GENERATOR` | Max MIDI Generator | Hashed AMXD in ledger | [Partial host/template contract](../specs/max-for-live-hosting.md), corrected partial scope independently reviewed; runtime/API U |
| `SURF-MAX-TEMPLATE-MAX-MIDI-TRANSFORMATION` | Max MIDI Transformation | Hashed AMXD in ledger | [Partial host/template contract](../specs/max-for-live-hosting.md), corrected partial scope independently reviewed; runtime/API U |


## Services, controllers and platform boundaries

The [service identities](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/services-platforms.json)
pin main Live, AddOns, Index, Plugin Scanner, Web Connector, Swapper, xdelta3,
Push2DisplayProcess, Push3, Max, the Live Engine bundle and ReWire, plus plist.
Canonical helper findings already exist for
[scanner discovery](plugin-scanner-static.md), [browser indexing](browser-index-static.md),
[helper launches](helper-launch-live-side.md), [Push3](push3-helper-static.md),
[web/add-ons/updating](web-addons-swapper-static.md), and
[x86-only/ReWire/MultiF0](x86-only-bundles.md). These remain partial findings,
without full service lifecycle or failure contracts. Third party frameworks and
dependencies are recorded by the existing package/dependency inventory; their
presence must not create invented user-visible features.

The [controller/module ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/controller-profiles.json)
retains each shipped top-level MIDI Remote Script directory and its hashed
`__init__.pyc` when present. Names beginning with `_` and `ableton` are explicitly
marked support/internal; other names are discovery candidates rather than
behavioral support claims. Existing [user mapping](midi-user-mapping.md) covers a
small controller-configuration path. Push1, Push2, Push3, Move integration, NKS,
all other named scripts, hardware setup and reconnection need individual
applicability and interaction contracts. A bytecode hash proves identity only.

The target source is a macOS universal package. Separate applicability is needed
for macOS arm64, macOS x86_64 and any Windows behavior. The existing x86-only
findings prohibit assuming that ReWire's presence establishes arm64 support.
Windows behavior is not established by this package or by macOS captures.

## Feature families requiring explicit owners

These are proposed refinements to the broad feature map, not recovered behavior.
The manual section numbers below are exact locators in this captured revision.

| Proposed owner | Manual/package seeds | Missing contract |
| --- | --- | --- |
| FEAT-MIDI-TOOLS | §11; [17 tool profiles](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/midi-tools.json); schema Algorithm classes | Arpeggiate, Chop, Connect, Glissando, LFO, Ornament, Quantize, Recombine, Span, Strum, Time Warp, Velocity Shaper; Rhythm, Seed, Shape, Stacks, Euclidean; selection, defaults, randomness, undo |
| FEAT-MIDI-EDIT | §10, §12 | Note operations, probability/deviation, multi-clip focus, MPE editing and external MPE setup, separate from note storage |
| FEAT-TUNING | §3.13, §15; TuningSystem classes and shipped Tunings | Scale awareness, tuning import, reference pitch, layouts, bypass and device interaction |
| FEAT-GROOVES | §14; Groove/GroovePool/ClipGrooveSettings | Extract, preview, timing/velocity/randomness, commit and persistence |
| FEAT-RECORDING | §7.5, §19; AudioRecorder/MidiRecorder | Arm/monitor, punch/count-in, overdub, capture, quantization, Session-to-Arrangement and cancellation |
| FEAT-COMPING | §21; TakeLane/TakeLanes/LinkedTrackGroup | Take creation, audition, promoting regions, linked edits and undo |
| FEAT-RENDER | §5.1.3, §20, §38.1.4, §39 | Audio/video/MIDI export, conversion/dither, bounce, freeze/flatten, tails and cancellation |
| FEAT-MEDIA | §8.4, §9, §13, §22, §28 | Formats, decoding cache, ASD, destructive editing, reverse, warp DSP, conversion, stem separation applicability, video |
| FEAT-PROJECT-MANAGEMENT | §5 | Merge, templates, dependencies, missing files, collect, unused-file management and pack creation; ALS envelope alone leaves these open |
| FEAT-BROWSER-WORKFLOW | §3.4, §4 | Search/filter/tag editing, similarity, preview interaction, loading and browser history; index records alone leave these open |
| FEAT-RACKS | §25; four rack types and macro schemas | Chains, key/velocity/selector zones, macros, variations/randomization, Drum Rack I/O/choke and nesting |
| FEAT-DEVICE-CATALOG | §23, §29–33; 102 profiles | Each device's full interaction/state/audio contract, including legacy loading; five finite DSP releases leave most modes and Live host protocol open |
| FEAT-PLUGIN-HOST | §24; AU/VST schema types | AU/VST2/VST3 lifecycle, editor, automation/MPE, buses, latency, crashes, missing plug-ins, state and platform restrictions; discovery alone leaves these open |
| FEAT-SYNC | §37; Link settings | Link, Link Audio applicability, tempo follower, MIDI clock/timecode, sync delay, join/leave and loss recovery |
| FEAT-MAX | §32–33; Max app/templates/AMXD | Lifecycle, live API, patch state/dependencies, scheduling, edit/reload, offline/failure behavior and host security boundary |
| FEAT-CONTROLLERS | §34–36; 149 script folders and Push helpers | Controller identities, modes, display, mappings, device banks, connect/disconnect and hardware limits |
| FEAT-ACCESSIBILITY | §41–42 | Focus/order, screen reader semantics, keyboard navigation, menus, shortcuts and conflict handling |
| FEAT-SETTINGS-PLATFORM | §2, §38; plist/helpers | Authorization, updates, preferences, themes, audio/MIDI devices, sample-rate changes, performance, failure and teardown |

Arrangement editing (§6), Session follow actions (§7/16), automation recording and
override (§26/27), routing/monitoring/latency (§17/18), undo history (§5.4.2), file
recovery and desktop interactions remain gaps inside existing broad families.
The new list must not imply that previously named families are already complete.

## Concrete next draft packets

1. Reconcile the existing specifications and current releases against stable
   surface IDs and exact clauses; keep all unresolved clauses open. Keep T1.6
   pending by user decision; specification mapping does not depend on provisioning
   an implementation workspace.
2. Draft the four rack contracts from latest schemas, shipped racks and bounded
   native readers: state/chain/zones/macros first, then routing and audio. Start
   native device packets with Utility, MIDI effects, sample instruments and
   common device lifecycle, each with finite states/cases rather than one
   omnibus device spec. Amp/Cabinet host-emulation work stays deferred by the
   user's 2026-10-19 decision.
3. Draft MIDI editing/tools, groove and tuning contracts from their per-tool and
   schema inventories, keeping random seed distributions and selection/undo
   behavior unknown until supported. Separate Max tools from native algorithms.
4. Draft Arrangement editing, recording/comping, rendering/media and project
   management as workflow packets. Bind version-uncertain stem/bounce topics to
   target evidence before turning them into 12.4.3 requirements.
5. Draft platform/host/Max/controller/synchronization/UI packets, using the
   existing helper findings as seeds. Public manual prose can identify a user
   task but cannot establish sample-exact DSP, timing or recovery behavior.

Each packet must update its owning research/spec page and inventories, state
preconditions and negative/boundary/cancellation/teardown cases, and pass the
existing review/handoff workflow. Extracted execution remains available only
under the governing bounded-probe rules. Missing evidence is unknown, never a
pass; no original-versus-candidate verification or clean implementation has
been performed by this inventory.

## Focused validation

The completed capture parsed 3,634 shipped ALS/ALC/ADV/ADG documents without
parser failures. All 880 manual URL/HTML-line locators and all 412 schema
class/line locators resolve in retained bytes. The 102 device IDs are unique;
the current Erosion profile uses `Erosion2`, with legacy `Erosion` separate.
All manifest payload hashes and sizes were checked, all page-relative file
links resolve, frontmatter fields are present, and all 102 profiles have a table
row. No device profile is complete. Root integration owns this page's inbound
index, coverage, roadmap and analyst log changes.

## Independent inventory review — 2026-10-19

The [coordinator review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/inventory-review.json)
verified all twelve payload hashes/sizes, all manual URL/line and schema/class
locators, unique device IDs and no-complete statuses, plus 261 external source
hashes (715,732,194 bytes read). Approved only as an open discovery baseline.
Later draft additions and feature-map refinements do not change its frozen
source denominators; a future inventory revision must retain explicit mappings.
