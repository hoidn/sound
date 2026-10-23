---
id: RES-EXTERNAL-HARDWARE-DEVICES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# External routing devices: retained documentary evidence

## Ownership and sources

The [individual-device contract](../specs/external-hardware-devices.md) owns the
documented External Audio Effect and External Instrument behavior. This page
owns source interpretation and limits under the
[coverage design](full-live-specification-design.md) and
[execution plan](full-live-specification-plan.md).

The [capture script](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/capture.py)
uses only retained HTML, frozen inventory/schema and Python standard-library
parsing/hashes. The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/sources.json)
pins seven external dependencies and original source identities/catalogs; the
manuals are reused captures, not newly downloaded or relabeled sources.

| Source identity | Version/capture and exact locator | SHA-256 |
| --- | --- | --- |
| D12-AUDIO-EFFECTS | Version 12, captured 2026-10-19; §29.18 external-audio-effect heading HTML 1144, nine paragraphs HTML 1154; audio-utilities original catalog | `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299` |
| SAMPLE-INSTRUMENTS-MANUAL | Version 12, captured 2026-10-19; §31.6 external-instrument heading HTML 1016, nine paragraphs HTML 1026; sample-instruments original catalog | `3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a` |
| PKG-SCHEMA | Installed latest 12.0_12402 schema; BufferAudioDevice line 939, BufferInstrument line 963 | `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299` |

Observed D12: each bounded manual section has one heading and nine paragraphs.
The retained [effect blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manual-external-audio-effect-blocks.json)
and [instrument blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manual-external-instrument-blocks.json)
preserve normalized text, paragraph/heading kind and original HTML line. Images,
the linked Driver Error Compensation FAQ and Routing and I/O chapter were not
inspected; this packet does not claim their contents.

## Presence and interpretation limits

Observed Dpkg: the frozen inventory associates External Audio Effect with
BufferAudioDevice and External Instrument with BufferInstrument using
`schema-and-product-directory; semantic alias inferred`. The
[retained entries](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/inventory-associations.json)
have `example: null`, `complete: false` and no matched preset. The
[class fields](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/schema-fields.json)
each contain the common device vocabulary and a Gain field. This is not an
observed runtime alias or sufficient evidence for routing serialization,
constructor defaults, numeric range, control exposure or hardware compatibility.

Interpretation notes below explain boundaries in the canonical clauses without
replacing their individual contracts:

- The effect explicitly supplies Configure… in both port choosers (§29.18,
  external-audio-effect:B003). The instrument's availability sentence references
  Audio Settings (§31.6, external-instrument:B005), but establishes no independent
  Configure… command there. Similar device roles do not justify copying a control.
- Instrument hardware-return inputs and plug-in auxiliary outputs belong to
  different route contexts. Its B006 main-output-on-host statement is a signal
  ownership goal, not a numeric mixing/downmix or arbitrary plug-in contract.
- Effect send/return Gains and instrument return Gain have different stated
  roles (effect B005, instrument B007). Neither description supplies a gain
  coefficient, clipping limiter or external hardware transfer function.
- Effect Peak indicators (B004) and processed-return Invert (B007) name
  observable controls/goals. Their sample conventions, reset values, phase
  matrix, update timing and quantitative signal comparisons remain U.
- Both B008 latency paragraphs separate sample-count retention from
  millisecond-duration retention across rate changes. Displayed selected-unit
  state can be proposed separately from physical alignment. Digital/analog
  setup and fine-tune advice do not specify cross-unit rounding or a conversion
  implementation. No physical latency was measured.
- Instrument B008 disables manual latency for internal routing and documents
  automatic compensation. B009 in each section disables the slider when Delay
  Compensation is unchecked. These disabled-state predicates do not prove
  compensation accuracy, bypassed audio or restoration of hidden values.

[Audio/video export](../specs/audio-video-export.md) already owns external-route
real-time/offline decisions and restart/cancel controls. Device names alone
cannot establish whether a particular render is affected. The finite
[mix graph](../specs/mix-graph.md) excludes general physical routing and
latency-reporting devices; its mixer arithmetic supplies no hardware oracle.
Hardware, qualifying plug-ins, active ports, driver permissions, supported audio
rates and calibration are explicit prerequisites for future observations, not
capabilities demonstrated on this analyst host.

## Authored probes and frozen evidence

The packet contains 24 requirements: 20 D12 documentary clauses and four U
signal/lifecycle obligations. Its 56 unexecuted cases comprise 16 control and
four selected-unit state proposals, ten ungraded signal probes and 26 U
lifecycle probes. All exact-target expected outcomes are null; signal/lifecycle
documentary expectations and comparators are also null. Both device profiles
remain partial. [Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
retains the major-release-to-exact-build evidence gap.

The [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/fixtures.json)
require independently known active ports and a nonmuted nonzero return positive
baseline before any signal/no-effect proposal. They define owned input tones,
admitted-unit/rate choices and MIDI setup without claiming returned samples,
MIDI encoding, waveform equality, gain, jitter or timing tolerances. No hardware,
plug-in binary, baseline recording or executable product fixture is supplied.
Missing prerequisites keep cases unexecuted; they never become passes.

The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manifest-author-r1.json)
pins the complete packet and canonical snapshots; the
[validator](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/validate.py)
and [author result](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/validation-author-r1.json)
check source hashes/catalog identity, exact block reproduction, schema/inventory
derivations, requirement/case ownership, source locators, null outcomes,
lifecycle kinds, JSON, snapshots, links and untracked-aware whitespace. These
are integrity checks; independent semantic review remains separate.

No original application/function, candidate, emulator, plug-in or hardware was
run. No network capture, hardware acquisition, tooling installation, calibration,
release, publication or commit occurred. Shared catalog/coverage/question/log
integration is coordinated outside this packet.
