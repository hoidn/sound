---
id: RES-DYNAMICS-DEVICES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Five native dynamics devices: documentary contracts and open audio behavior

## Question and canonical ownership

What observable control/routing contracts can the retained manual and bounded
installed artifacts support for Compressor, Gate, Glue Compressor, Limiter and
Multiband Dynamics? The [individual requirements](../specs/dynamics-devices.md)
own the contract; this page owns evidence interpretation and limitations. These
are five assigned partial profiles under the [coverage design](full-live-specification-design.md)
and F-06 of the [execution plan](full-live-specification-plan.md). They are not
complete profiles, releases or application compatibility results.

Consulted existing owners: [rack/chain workflows](../specs/device-racks.md),
[mix graph](../specs/mix-graph.md), [bundled hosting](../specs/bundled-device-hosting.md)
and [Utility/Tuner/Spectrum evidence](device-audio-utilities.md). No gain law,
ramp, latency or host assumption migrates from those narrower scopes into these
five devices just because the same terms occur. This packet adds no candidate
implementation and no original executable/function execution.

## Sources, capture and boundedness

The [capture program](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/capture.py)
uses the Python standard library to parse exact retained manual bytes and five
inventoried shipped presets. It reads only the latest schema and inventory
needed to identify these devices; it does not scan native binaries or execute
product code. The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/sources.json)
retains source identities, paths, dates, sizes and SHA-256 digests.

| Evidence | Identity and exact locator | Establishes | Limit |
| --- | --- | --- | --- |
| D12-AUDIO-EFFECTS | [Original official URL](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/); reused [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html), captured 2026-10-19, SHA-256 `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`; original identity D12-AUDIO-EFFECTS in audio-utilities/sources.json | Version 12 documented prose | Not exact 12.4.3 applicability or observed audio; source figures not separately inspected |
| PKG-SCHEMA | [Latest retained schema](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt), SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`; [five class records](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/schema-fields.json) | Installed classes/field types | No exposed control, default, legal domain, enum or DSP semantics inferred from names |
| Five bounded presets | [Retained copies, hashes and original source paths](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/sources.json); [parsed root/field records](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/package-values.json) | One stored representation per device, historical Creator metadata | No constructor defaults or full parameter domains inferred; no Set/preset was loaded in Live |

The shared HTML is an external packet dependency pinned by hash and original
source identity rather than silently copied as a fresh web capture. Five per-device
block JSON/text pairs retain paragraph identity and exact HTML line; the current
manual snapshot has 123 selected blocks:

| Device | Manual section / selected blocks | Latest class / line | Bounded shipped example |
| --- | --- | --- | --- |
| Compressor | §29.9 / 33; compressor:B001–B033 | Compressor2 / 1381 | Acoustic Kick Compressor.adv |
| Gate | §29.20 / 16; gate:B001–B016 | Gate / 2630 | Flipside.adv |
| Glue Compressor | §29.21 / 16; glue-compressor:B001–B016 | GlueCompressor / 2670 | Bass - Low Extender.adv |
| Limiter | §29.24 / 13; limiter:B001–B013 | Limiter / 3754 | Defaults/Audio Effects/Limiter.adv |
| Multiband Dynamics | §29.26 / 45; multiband-dynamics:B001–B045 | MultibandDynamics / 5279 | A Standard Multiband Comp.adv |

All five files have `MinorVersion="12.0_12402"`, `Creator="Ableton Live 12.4d1"`
and Revision `42bc084cd8152e4fb737ef3fefd04b2bea5320e7`. Their presence in the
pinned 12.4.3 installation establishes installed examples, not that their
historical Creator equals the application target or constructor behavior.

## Observed documentary findings

**Observed D12:** the manual distinguishes normal audio Dry/Wet from external
trigger Dry/Wet for Compressor and Glue. Sidechain audio drives detection and
is heard directly only under Listen, which replaces normal output. Compressor
also disables automatic Makeup for external-sidechain use. Gate, Glue and
Compressor document detector EQ; Multiband's captured sidechain section documents
source/Gain/Dry-Wet/Listen without adding an EQ control. Limiter's section does
not establish external sidechain controls. Exact per-claim blocks are mapped in
[requirements.json](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/requirements.json).

**Observed D12:** Compressor and Gate offer 0/1/10 ms Lookahead; Limiter offers
1.5/3/6 ms. Limiter documents greater latency for longer lookahead and M/S mode.
Glue documents a two-times internal sample-rate oversampling toggle. These values
are documented choices or rate factors, not measured delays or a prescribed
implementation filter. Sample counts, scheduling and compensation remain unknown.

**Observed D12:** Limiter's Link endpoints explicitly qualify channel interaction:
0% independent reduction versus 100% shared limiting for the selected L/R or M/S
pair (limiter:B005,B012). Therefore the L/R paragraph cannot be generalized into
unconditional channel independence. No other device in this packet has a
supported effective stereo detector/linking law.

**Observed D12:** Glue's fixed Soft Clip waveshaper has a documented -0.5 dB
maximum but an explicit oversampling exception in the same source: loud peaks
may exceed 0 dB (glue-compressor:B007,B016). The draft preserves the caveat rather
than asserting an all-mode ceiling. The waveform, reconstruction and calibration
needed for numerical testing remain unknown. Limiter's True Peak description
similarly supplies no reconstruction kernel, tolerance or test signal denominator.

**Observed D12:** Multiband Amount=0% gives an effective ratio of 1 for dynamics;
band input/output gains and crossover processing are separate. Glue Range=0 dB
means no compression while Makeup/Soft Clip remain independent. Compressor
Ratio=1 means no compression. These statements do not establish whole-device
neutral sample identity (multiband-dynamics:B015,B027; glue-compressor:B005–B007;
compressor:B004,B006–B007).

**Observed Dpkg, representation only:** selected Compressor preset stores
Threshold/Manual `0.1791548878`, Knee/Manual `0.421875`, Ratio/Manual `4` and
LookAhead/Manual `1`. Gate Flipside stores Gain/Manual `-75` and LookAhead/Manual
`0`. Glue Bass - Low Extender stores Range/Manual `25`, Ratio/Manual `1`,
PeakClipIn/Manual `true` and Oversample/@Value `true`. These differing encodings
are a concrete reason to avoid copying displayed dB values directly into every
private field or inferring enum meaning. Limiter stores Mode/Manual `0`,
Routing/Manual `0`, LinkAmount/Manual `1`, Maximize/Manual `false`; those do not
prove the user-visible labels of their codes. Multiband stores SplitLowMid/Manual
`159.999985` and SplitMidHigh/Manual `6000.00049` as example representations.
Each locator is /Ableton/class/field in package-values.json and the retained ADV.

## Draft, cases and unresolved outcomes

The packet has 62 requirements and 129 case entries: 47 D12 documentary cases,
five Dpkg file-only cases and 77 U cases. Every D12 runtime clause has target
12.4.3 applicability U. Dpkg cases establish bytes, never application acceptance.
There are 15 or more U cases per device covering effective audio and lifecycle;
none has an invented expected fallback or a passing status.

[Finite signal definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/fixture-signals.json)
use explicit sample amplitudes and mathematical frequencies without pretending
they are detector dB levels. The [case ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/cases.json)
retains explicit mode combinations, requested settings, signal references,
provenance, comparison rule and null unknown oracles. Requesting unavailable
values does not imply acceptance. Formula-to-audio rounding is an open probe
prerequisite. No fixture is captured device output.

Open effective laws include knee/threshold/ratio/gain calibration, envelope and
auto response, peak/RMS windows, stereo detector interaction, dry/wet and
sidechain blending, EQ, crossover filters/summation, waveshaping, oversampling,
True Peak reconstruction, latency, parameter ramps and all required state and
failure cases. Close these with independently reviewed exact-target evidence;
manual prose or controller-range metadata cannot discharge them. Required
cross-feature gaps include real-time/export parity, sample-rate changes,
Arrangement/Session ownership, reconnection, undo, save/reopen, legacy migration,
malformed/canceled loads, transport discontinuities and deletion/close.

The [frozen author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/manifest-author-r1.json)
records every packet payload plus spec/research snapshots and external pins.
The [focused validator](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/validate.py)
checks source/locator/field integrity and requirement/case coverage. Mechanical
checks are not semantic acceptance. Separate review and root-owned catalog,
coverage, question and log updates are required before integration. No current
handoff, original evidence file or shared index was edited by this worker.
