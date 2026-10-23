---
id: RES-MODULATION-PITCH-LOOP-DEVICES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Modulation, pitch, spectral and looping: retained documentary evidence

## Ownership and method

The [individual-device draft](../specs/modulation-pitch-loop-devices.md) owns
observable contracts for ten current F-06 devices. This page owns documentary
interpretation, source limitations and the spectral alias correction. It follows
[coverage design](full-live-specification-design.md) and the
[execution plan](full-live-specification-plan.md). It does not supersede the
rack, host, MPE, tuning or recording owners linked in the specification.

The [capture program](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/capture.py)
uses Python standard-library HTML parsing, gzip/XML preset reading and SHA-256.
It reuses the exact audio-utilities HTML, reads ten selected shipped presets,
the latest schema and preexisting discovery inventories, and audits only the
two spectral preset folders for the discovered alias discrepancy. No tooling
was installed. No native binary, original function, Live instance, emulation,
hardware or candidate was run. No implementation context was created.

## Source identities and observations

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/sources.json)
records external paths, sizes, hashes, official URL, capture date and retained
local preset copies. The manual's original identity is D12-AUDIO-EFFECTS in the
audio-utilities packet; it is not relabeled a fresh capture. Its SHA-256 is
`9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`.
The latest retained schema SHA-256 is
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Both are external pinned dependencies rather than copied raw history.
The canonical spec appendix gives exact per-device manual sections and links
to 332 extracted heading/paragraph/list blocks with their HTML line locators.

**Observed Dpkg:** all ten chosen preset XML roots carry
`MinorVersion="12.0_12402"`, `Creator="Ableton Live 12.4d1"`, Revision
`42bc084cd8152e4fb737ef3fefd04b2bea5320e7`.
Their presence in the 12.4.3 package does not make 12.4d1 its runtime identity or
these stored values constructor defaults. One example per class is sufficient
for field-presence corroboration only; full legal domains and semantics are U.

## Spectral discovery-association correction

**Observed Dpkg:** the immutable initial discovery inventory associated Spectral
Resonator with `Spectral`/line 7423 and a preset physically stored in Spectral
Time's folder, and Spectral Time with `Transmute`/line 8118 and a preset in
Spectral Resonator's folder. The
[bounded folder ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/spectral-folder-observations.json)
retains exact paths, sizes and hashes for all 28 `.adv`-suffixed files in those
two folders. Fourteen names beginning `._` are excluded sidecars, not fourteen
additional product presets. The remaining eight Spectral Resonator presets all
have root `/Ableton/Transmute`; the remaining six Spectral Time presets all have
root `/Ableton/Spectral`. No non-sidecar preset parse failed.

**Observed vocabulary:** checked `Transmute` schema/preset fields include
`MidiPitch`, `PartialFrequencies`, `Global_NumHarmonics`; checked `Spectral`
fields include `Freezer`, `Delay`, `ProcessingOrder`.
[Exact class fields](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/schema-fields.json)
and [example root/fields](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/package-values.json)
retain the actual flattened field spellings. The manual Resonator sections
29.36.1–29.36.5 discuss MIDI/partials/harmonics, and Time sections 29.37.1–29.37.4
discuss Freezer/Delay/order. This supports the corrected **artifact association**
Resonator→Transmute and Time→Spectral. It does not establish runtime equivalence,
DSP semantics, exposure of every field, or a public serialized API. The frozen
inventory and original preset bytes remain unchanged. The independently reviewed
[companion inventory revision](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r2-spectral-aliases/devices-r2.json)
and its [review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/inventory-spectral-alias-review.json)
now own the corrected discovery routing. This packet retains the original
inventory ID in historical source records rather than hiding it; the
[association reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/association-reconciliation.json)
explicitly maps those crossed spectral IDs to the checked physical preset
identity. Neither retained R1 label is a current device association.

## Documentary distinctions that affect cases

The spec's source-mapped requirements remain canonical; these are evidence
interpretation notes, not competing control specifications.

- Auto Pan-Tremolo §29.3's channel-LFO descriptions concern modulation. Equal LFO
  values do not mean equal output samples from arbitrary stereo input. Random
  Phase Offset wording and beat-mode availability do not establish extra
  free-running control eligibility.
- Auto Shift §29.4.1.1's no-MIDI sound statement must be tested on its processed
  path, with Dry/Wet full wet and prior latch/release history excluded. It is
  not assigned to Shifter or Spectral Resonator by similarity. Voice Count,
  MIDI On and MIDI panel visibility have distinct roles.
- Chorus-Ensemble §29.8 disables Feedback and Dry/Wet in Vibrato; that is a
  control eligibility proposal. It supplies no independent audio invariance
  comparator when a disabled control is manipulated.
- Phaser-Flanger §29.29 explicitly requires Env Fol enabled and nonzero amount;
  negative Amount reverses envelope phase. Random-waveform Duty Cycle/no-effect
  testing still needs active nonzero modulation and an audible positive baseline.
- Shifter §29.35.1 calls the Delay free slider Hertz. Its preset field spelling
  `Delay_TimeSeconds` does not authorize silently correcting the UI unit or
  inventing a conversion. §29.35.2 describes Random S&H Width in LFO terms,
  which supplies no exact stereo audio law.
- Spectral Resonator §29.36.1 makes MIDI Gate always active in Poly and Glide
  Mono-only; §29.36.3's Chorus Mod Rate zero exception still concerns active
  amplitude modulation. Quantize needs explicit scale/tuning/chromatic context.
- Spectral Time §29.37 initially describes Freezer feeding Delay, while
  §29.37.4 supplies both orders. The specific order control prevents an
  unconditional Freezer-first contract. §29.37.1 requires Freeze enabled in
  both trigger modes, and its X-Fade sentence mixes ms/percentage language;
  no exact conversion or fade coefficient is specified. Section-local and
  global Dry/Wet remain distinct.
- Vocoder §29.42's Sens endpoints control unvoiced detection/generator activity,
  not guaranteed audible noise at zero Unvoiced level. External carrier and
  modulator paths require separate positive baselines. Filterbank mode names
  do not supply filter coefficients or channel downmix weights.
- Beat Repeat §29.5 distinguishes automatic Chance/Interval/Offset/Gate from
  manual Repeat and separates three output modes. Endpoint no-repeat proposals
  require Repeat off, a valid nonzero repeat path and Chance 100 positive trial.
- Looper §29.25 distinguishes its own recording, overdub Undo, monitoring and
  tempo ownership from track recording/global Undo. Reverse changes existing
  and newly overdubbed material differently. No retained audio proves those
  time-domain outputs or supplies a resampler/clock oracle.

## Unknowns and retained checks

The packet has 96 D12 clauses plus ten U lifecycle obligations and 186 cases:
55 control/state documentary proposals, 41 ungraded audio obligations and 90
device-specific U lifecycle cases. Every exact-target expected outcome is null,
every target grade U, and every case unexecuted. Boundary/automation/transport/
persistence/undo/malformed/cancel/teardown/sample-rate questions remain required
for every device. Figures, CPU performance, MPE codecs, voice stealing, onset
thresholds, latency, FFT/filter/resampler/gain/fade laws, random distributions,
state migration and crash recovery were not established.

The [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/validate.py)
checks source pins and manual-line/block reproduction, schema locators,
folder-root evidence, all requirement references, distinct device ownership,
null unknowns, per-device lifecycle coverage, metadata, page-relative links and
whitespace including untracked files. Its
[author result](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/validation-author-r1.json)
is a packet integrity check, not a behavioral pass. The
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manifest-author-r1.json)
freezes all payload bytes and canonical spec/research snapshots for a separate
analyst review. Shared index, question, coverage and append-only log integration
is coordinated outside this owned packet.
