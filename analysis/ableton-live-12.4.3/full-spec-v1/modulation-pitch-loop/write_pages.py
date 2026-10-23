"""Render the canonical analyst contract from the authored source-block view."""
from pathlib import Path
import json,collections
P=Path(__file__).resolve().parent;R=P.parents[3]
req=json.loads((P/'requirements.json').read_text());cases=json.loads((P/'cases.json').read_text());schema={r['class']:r for r in json.loads((P/'schema-fields.json').read_text())}
devs=[]
for line in (P/'authored-contracts.txt').read_text().splitlines():
 if line.startswith('['):
  slug,prefix,name,cls=line[1:-1].split('|');devs.append((slug,prefix,name,cls))
rel='../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/'
s='''---
id: SPEC-MODULATION-PITCH-LOOP-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Live 12 documentary behavior with exact-build applicability unknown
---

# Modulation, pitch, spectral and looping devices

## Scope and authority

This partial F-06 draft owns ten individual current native profiles under the
[full product inventory](../research/full-live-coverage-inventory.md). It covers
documented modes, controls, routing, capture and state roles. It establishes
neither full DSP nor completed device profiles and is not a released implementation
input. [Coverage design](../research/full-live-specification-design.md) governs
closure; the [research owner](../research/modulation-pitch-loop-devices.md) owns
source interpretation and the reviewed spectral association correction.

**D12** means documentary prose from the retained official Version 12 manual,
captured 2026-10-19. **Every runtime clause's exact 12.4.3 applicability is U.**
Installed schema/preset observations are Dpkg presence only; names and historical
preset Creator values prove no DSP, constructor default, enum domain or runtime
control law. U outcomes have `expected: null`, no comparator and no pass.
There is no S/X execution or original-versus-candidate result in this packet.

[Device chains/racks](device-racks.md) owns common insertion, bypass, presets,
chain order and tail gating. [Automation envelopes](automation-envelopes.md)
owns its finite storage/evaluation contract; it does not prove these controls'
automation eligibility or smoothing. [Tuning systems](tuning-systems.md) and
[MPE workflows](mpe-workflows.md) retain global context/codec gaps; Auto Shift,
Shifter and Spectral Resonator keep their own destinations and voice behavior.
[Recording/comping](recording-comping.md) owns track recording/Capture MIDI,
which do not specify Looper recording or Spectral Time freezing. The seven-device
[bundled-host draft](bundled-device-hosting.md) does not cover these ten devices.
[Clip launch](clip-launch.md), [transport](transport-state.md),
[media files](media-file-workflows.md) and [mix graph](mix-graph.md) supply only
their already bounded contracts. Looper-specific quantization, import/export and
Insert-Looper paths belong here. Common Link/network behavior remains open.

The legacy Auto Pan, Chorus, Phaser, Flanger and Frequency Shifter profiles
remain separate owners; current device prose is not their alias or behavior
contract. Spectral Resonator is associated with `Transmute` (schema line 8118),
Spectral Time with `Spectral` (line 7423) by checked shipped folder/root/control
vocabulary. This corrects two discovery associations without changing frozen
inventory bytes or deriving runtime semantics from field names.

## Inputs, observations and grading

Use a valid editable test-owned Set and an isolated enabled device; select all
named modes, source/tapping points and amounts explicitly. Reset memory, latches,
held notes and capture histories between independent trials. Source, wet path,
monitoring and output must be active and unmuted. No-effect or silence proposals
need a paired positive baseline with an active path, appropriate stimulus and
nonzero amount. A dry-only path, disabled section, zero send, absent carrier/note,
muted output or zero modulation is insufficient evidence about active processing.
Only deliberate documented zero exceptions change their target setting to zero.

[Stimulus recipes](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/stimulus-recipes.json)
retain concrete 4/4, 120 BPM, 48 kHz, four-second tone/burst and owned MIDI setups.
These are analyst choices, not product limits or captured reference outputs.
Input tone formulas define inputs only. Distinct stereo inputs are not assumed
to yield equal signals merely because channel LFO waveforms coincide.
Unpitched/voiced recordings and hardware inputs must be retained and identified
before a future case uses them. No source material was played or recorded here.

The packet contains **106 requirements: 96 D12 clauses and ten U lifecycle
obligations**; **186 unexecuted cases** contain 46 documented control proposals,
9 documented state proposals, 41 ungraded signal obligations and 90 U lifecycle
cases. Documentary proposals compare only the named choices/units/endpoints or
visible transitions. All 186 exact-target expectations/grades remain null/U.
No waveform, frequency/pitch codec, filter/FFT/coefficient, random seed/distribution,
clock rounding, measured latency, deadline or tolerance is invented. Public
processing descriptions impose no private algorithm or candidate architecture.

## Individual requirements

Every following behavioral row is D12/target-U. Evidence cells identify exact
block IDs in this packet; each block retains HTML line, section/heading context
and text in the analyst appendix. Corresponding `MPL-<device>-NNN` cases retain
finite setup/action and a documentary expectation, with signal grading null.

'''
for slug,prefix,name,cls in devs:
 rows=[r for r in req if r['device']==name and r['strength']=='D12']
 s+=f'### {name}\n\nCurrent surface `SURF-DEVICE-{slug.upper()}`; artifact association `{cls}` / latest schema line {schema[cls]["line"]}.\n\n| Requirement | Documented observable contract and limits | Evidence |\n| --- | --- | --- |\n'
 for r in rows:
  refs=', '.join(x['block'].split(':')[1] for x in r['evidence'])
  s+=f'| {r["id"]} | {r["contract"]} | `{slug}:{refs}` |\n'
 s+=f'\n**REQ-MPL-{prefix}-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.\n\n'
s+='''## Device-specific lifecycle and boundary obligations

Each row has nine distinct retained cases, one each for numeric/tempo boundary,
automation, transport stop/seek/restart, persistence/source loss, global undo/redo,
malformed input/state, cancellation, teardown and sample-rate change. Case IDs
are `MPL-<prefix>-U-BOUNDARY`, `-AUTOMATION`, `-TRANSPORT`, `-PERSISTENCE`, `-UNDO`,
`-MALFORMED`, `-CANCEL`, `-TEARDOWN` and `-SAMPLE-RATE`. Their expected values and
comparators are null. There is no lifecycle omission classified inapplicable:
these are required unknowns. Malformed tests use disposable copies and input
text, never immutable evidence or recovered source code.

| Device / U requirement | Concrete state requiring those nine outcomes |
| --- | --- |
'''
recipes=json.loads((P/'stimulus-recipes.json').read_text())
for slug,prefix,name,cls in devs:s+=f'| {name} / REQ-MPL-{prefix}-LIFECYCLE | {recipes[prefix]["initial_device_state"]}; controls under transition: {recipes[prefix]["controls"]}. |\n'
s+='''
Documented numeric endpoints are already present in the control cases; the
boundary cases add adjacent/invalid entries and clock/event boundaries without
asserting clamp/reject policy. Native local Looper Undo is distinct from global
Undo History. MIDI mode in Shifter or Spectral Resonator is not assigned Auto
Shift's no-notes silence rule. Spectral Time Freezer requires both section On
and Freeze; Delay's Dry/Wet is separate from global Dry/Wet. Pure control
eligibility cases (for example Vibrato-disabled Feedback) do not grade signal
invariance. Modulation/no-effect cases require the enabled/nonzero positive
conditions above and still leave their quantitative signal result unknown.

## Acceptance catalog

The [requirement view](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/requirements.json)
and [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/cases.json)
retain exact requirement-to-source-to-case links. All cases have `executed:false`;
all target expectations are null and target grades U. Only the documentary
control/state comparator can compare visible named fields; acoustic adjectives,
internal buffers or latent DSP state are not a reference comparator.

| Device | D12 / U requirements | Control / state / signal proposals | Additional U cases |
| --- | --- | --- | --- |
'''
for slug,prefix,name,cls in devs:
 rr=[r for r in req if r['device']==name];cc=collections.Counter(c['kind'] for c in cases if c['device']==name)
 s+=f'| {name} | {len(rr)-1} / 1 | {cc["documented-control"]} / {cc["documented-state"]} / {cc["signal-obligation"]} | 9 |\n'
s+='''
## Analyst evidence appendix

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/sources.json)
pins the external shared capture, schema/inventory and retained preset copies.
The [dependency ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/dependencies.json)
additionally pins the original capture catalog and reviewed spectral correction;
[reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/association-reconciliation.json)
identifies historical R1 spectral source IDs explicitly.
The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manifest-author-r1.json)
freezes payloads plus both canonical page snapshots for independent review.
These links are analysis-only and must be sanitized/reviewed before handoff.

- D12-AUDIO-EFFECTS: [official Version 12 chapter](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/),
  retained [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html),
  captured 2026-10-19, SHA-256 `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`.
  It supports documented prose, not pinned-patch behavior; figures were not separately inspected.
- PKG-SCHEMA: [12.0_12402 schema](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt),
  SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`;
  [class/field observations](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/schema-fields.json)
  prove storage vocabulary only.
- Ten shipped [preset observations](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/package-values.json)
  retain roots, fields, source paths and historical Creator metadata. No constructor/default/audio claim follows.
- The [bounded spectral folder ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/spectral-folder-observations.json)
  records eight Resonator `Transmute` presets and six Time `Spectral` presets plus
  fourteen excluded `._` sidecars; all bytes/paths are pinned. Discovery aliases
  are an artifact association, not proof that private names expose any particular control law.

| Device | Exact manual section / blocks | Retained paragraph/heading view |
| --- | --- | --- |
'''
for slug,prefix,name,cls in devs:
 blocks=json.loads((P/f'manual-{slug}-blocks.json').read_text());section=blocks[0]['text'].split()[0]
 s+=f'| {name} | §{section}; `{slug}:B001–B{len(blocks):03d}` | [Blocks]({rel}manual-{slug}-blocks.json), [line-numbered text]({rel}manual-{slug}.txt) |\n'
(R/'wiki/specs/modulation-pitch-loop-devices.md').write_text(s)
research='''---
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
'''
assert sum(len(json.loads((P/f'manual-{d[0]}-blocks.json').read_text())) for d in devs)==332
(R/'wiki/research/modulation-pitch-loop-devices.md').write_text(research)
print('wrote canonical pages')
