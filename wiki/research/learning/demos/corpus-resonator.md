---
id: DEMO-CORPUS-RESONATOR
type: research
status: current
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# Interactive demo: Corpus with real controls and a stand-in sound

**Purpose.** A playable page for learning what a resonator effect does and how
we know what we know. The controls, ranges and presets are the ones Live 12.4.3
ships for its Corpus audio effect. The sound is a labelled textbook model,
because Corpus's own processing code has not been traced. This is analyst
material and a teaching aid. It is not a specification, a compatibility claim
or a clean-implementation input.

**Open it:** [local demo page](../../../../analysis/ableton-live-12.4.3/demos/corpus/index.html)
(offline, no server). Use headphones with the microphone source. Keep the page
local; it repeats Ableton's device name, parameter names and preset values.

## Plan and status (2026-10-17)

| Step | Work | State |
| --- | --- | --- |
| 1 Extract | [`tools/corpus_demo.py`](../../../../tools/corpus_demo.py) reads the Corpus class from the schema and every shipped Corpus preset, recording input SHA-256s | Done |
| 2 Build | One offline page from [`tools/corpus_demo.html`](../../../../tools/corpus_demo.html): generated controls, preset menu, click/noise/drum-loop/file/microphone sources, mode plot, spectrum, an evidence badge on every control | Done |
| 3 Check | Extractor unit tests and a headless Chromium self-test of the audio graph | Passed (below) |
| 4 Faithful version | Trace `SetParameterA` and `CalcA` in the Corpus corpus and replace the stand-in model, kept local | Not started |

## What is observed

- **Fields.** The `Corpus` class of `Schema/12.0_12402.txt` (SHA-256
  `b7c9d4c7…89d0f299`) declares 60 fields. 39 are timeable device parameters;
  the page shows 38 of them as controls, all except the device's `On` switch.
- **Values and ranges.** Each parameter of the 26 presets under
  `Core Library/Devices/Audio Effects/Corpus/` stores a `Manual` value, and 34
  of them also store a `MidiControllerRange`. The other five are on/off
  fields. Every preset gives the same range for a given parameter, and the
  extractor fails if one differs. Examples: `ResonanceType` 0–6,
  `ResonatorQuality` 0–3, `Transpose` −48–48, `FineTranspose` −50–50,
  `FilterMidFreq` 50–18,000, `FilterBandWidth` 0.5–9. `Frequency`, `Decay` and
  most other values are normalized to 0–1 or −1–1, so their units are unknown.
- **Type usage.** Of the 26 presets, nine use type 3, five type 6, four each
  types 2 and 5, two type 0, and one each types 1 and 4. Data:
  [corpus-parameters.json](../../../../analysis/ableton-live-12.4.3/demos/corpus/corpus-parameters.json).
- **The device bundle.** Its C1 corpus has 644 functions (446 exported, 198
  with warnings, 0 failed). It exports `CreateInstanceU`, `DestroyInstanceU`,
  `SetSampleRateU`, `GetPlugInfoU`, `SetParameterA`, `CalcA` and `ResetA`. Its
  strings include `StereoAudioIn`, `Filters`, `Resonator`, `Gain`, `DryWet`,
  `StereoWidth`, `StereoLfo` and `StereoAudioOut`. Read the code in the
  [corpus browser](../../../../analysis/ableton-live-12.4.3/browse/r2/Corpus/index.html).
  The coordinator's device-bundle packet (`wiki/research/device-bundles-static.md`,
  in preparation) owns the host-interface findings.

## What is assumed

- **Type labels.** The order Beam, Marimba, String, Membrane, Plate, Pipe, Tube
  for indices 0–6 is assumed; no shipped file maps them. Two preset titles
  agree: "Pipe Resonator" uses 5 and "Tubular Pan" uses 6. Five of the labels
  (Beam, Marimba, Membrane, Plate, Pipe) sit together in Live's string pool
  near file offset `0x5be2dac`, next to resonator parameter names that look
  like Collision's, not Corpus's.
- **On-screen names.** The page labels controls with schema field names
  (`FreqDamping`, `AmpFreq`, `ExcitationX`). Live's display names for Corpus
  are not in our evidence.
- **LFO shapes.** `LfoType` indices are assumed to mean sine, square, triangle,
  two sawtooths and two random shapes.

## The stand-in model

A bank of up to 40 band-pass filters per channel, one per mode, built from
native Web Audio nodes. Textbook mode ratios for each type:

- **Beam:** free-free beam.
- **Marimba:** a tuned bar, 1:4:10.
- **String, Pipe, Tube:** harmonic series. Pipe suppresses even modes as
  `TubeOpening` falls.
- **Membrane:** Bessel zeros, computed in the page and self-checked.
- **Plate:** a simply supported rectangle whose side ratio follows `Ratio`.

The other controls:

- **Strike and pickups:** strike position and the two listening positions
  scale each mode by its shape there.
- **Decay:** sets the lowest mode's T60. `FreqDamping` makes high modes decay
  faster.
- **Bandwidth:** each filter's Q follows its mode's decay time.
- **Unchanged from real Corpus parameters:** Transpose, Fine, Detune, filter,
  drive, width, bleed and dry/wet act on the signal path, but every mapping
  from a normalized value to a physical one is a guess.
- **Not modelled:** LFO sync, phase and offset, and the MIDI controls.

The page describes each mapping beside its control. The excitation is mono.

## Checks

- [Unit tests](../../../../tools/tests/test_corpus_demo.py) (3) cover:
  - extracting values, ranges and type-name evidence from synthetic files, with
    AppleDouble companions skipped;
  - rejecting a preset whose range disagrees;
  - preset names containing markup, which are escaped in the embedded data.
- **Headless Chromium self-test** (`index.html#selftest`): an offline render of
  a click through the String type tuned to 220 Hz. The strongest spectral peak
  between 150 and 300 Hz was 220.0 Hz, all samples were finite, and the
  computed second membrane ratio was 1.59334 (j₁₁/j₀₁ = 1.5933). Result
  `"pass":true`.
- **Normal page render:** 26 presets, 38 controls and "Pipe Resonator" loaded
  as type 5. No script errors in Chromium's log.
- **Not checked:** live audio output and interactive use in a desktop browser.

## Next lesson

Trace how `SetParameterA` maps a parameter index to an internal module, and
what `CalcA` does per sample. Then compare the result with the stand-in, mode
by mode. That trace is analyst-side and stays local.
