---
id: RES-MAX-FOR-LIVE-DEVICES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Twenty shipped Max-device source profiles

## Scope and evidence selection

This partial F-06 packet supports the
[canonical device draft](../specs/max-for-live-devices.md) under
[coverage design](full-live-specification-design.md). The frozen inventory owns
twenty max-device records, distinct from five templates and two MIDI Tools.
[Max host/templates](max-for-live-hosting.md) owns its workflows; the tools remain
[MIDI editing](midi-editing-tools.md). No host-generic clause substitutes for any
of these twenty device profiles. No Max patch/original/candidate ran, no tooling
was installed and no broad binary analysis was launched.

The exact inventory TOC URL selected current English
`/en/live-manual/12/max-for-live-devices/`. No existing capture of that chapter
was found. [Source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/source.json) retains one capture of
299,403 bytes, SHA-256
`b95a0d3ed3d7217505437a0d7d65de68d37e0f894d27e9869122fbfb89728a46`.
[218 paragraph/heading blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/manual-blocks.json) preserve HTML lines
and full heading contexts through 33.3.6, excluding sidebar/footer. Version 12
exact 12.4.3 applicability remains U. Figures were not separately inspected.

## Two profiles omitted by current English headings

Current HTML has 18 individual profiles; installed inventory has 20, nine of which
are DS instruments. DS Sampler and Expression Control Legacy are absent from
current English headings. Bounded official-source search found both named in
an official dated English Version 12 PDF under 2025-06-02 path. The entire immutable
PDF was retained because the web reader rejected its 76,333,838-byte size; the
existing `pdftotext` extracted only physical pages 721/730/731. No dependency was
installed. Exact SHA-256 is
`42fbd3794df0d69aaf522aea589bf08dd3dc8db3eb0e135cab041093875db976` in
[metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/source-dated-pdf.json).

[15 dated blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/dated-blocks.json) comprise DS Sampler 6
heading/caption/paragraph blocks on p721, Expression Control Legacy 8 on p731 and
one separately labelled current-to-Legacy migration paragraph on p730. The p731
text preceding the Legacy heading belongs to current Expression Control and is
excluded, preventing Random/Increment/smoothing-source contamination. Source
revision mismatch is explicit D12-2025/target-U, not silently current-build proof.
The p730 Live 11-Set migration statement has no retained old Set/target output.

## Individual device interpretation

The draft assigns each device its own controls/modes/state/finite cases from its
own paragraphs. Nine DS profiles retain distinct tone/noise/filter/pitch/envelope
roles. DS Sampler sample-drop is not inferred as a preview action. Align Delay
keeps unit/temperature/Link UI without deriving sound-speed or frame arithmetic.
Envelope Follower carries main-versus-donor, taps/meters/mix and mapped envelope;
LFO carries waveform exclusions, Depth/Hold/Phase; Shaper its editor/trigger modes;
Envelope MIDI its ADSR/Loop/Sync/Echo/Sustain/velocity roles. Current Expression
Control differs from Legacy's five global-source/one-target-per-source document.
MIDI Monitor display Freeze is not a MIDI-pass-through law. MPE Control keeps
source-specific curves/conversion/modes and the unexpanded 2x example. Note Echo
retains time/Input/MPE distinction; Shaper MIDI its note/sustain/loop/velocity and
echo envelope behavior. Numerical transfer/curve/MIDI/RNG/timing laws stay U.

[Package identities](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) were rehashed at the
exact twenty inventoried AMXD paths, checking sizes and 16-byte prefixes. These
bounded reads supply identity only. No patch content/control graph was parsed,
no original algorithm was recovered/executed and no field/default/API behavior
was inferred. External files are not duplicated here; retention depends on
recorded paths and checksums. The two manual versions are separate pinned sources.

## Packet, review and remaining evidence

[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/requirements.json), [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/cases.json)
and [counts](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/counts.json) retain exact device/source links.
Each device has one file-identity clause and one U lifecycle clause with ten
separate, device-specific setup cases, alongside its supported documentary rows.
All exact-target expectations/comparisons are null, U, unexecuted. Documentary
control/state checks grade no application; acoustic/timing obligations have no
numeric comparator. [Future inputs](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/fixtures.json) require accepted
controls, valid notes/media, mapping targets and paired active positive baselines.
Missing dependencies, absent controls or silent source never yields pass.

Exact-version parity, current menu/constructor defaults, AMXD/API protocols,
all DSP/filter/oscillator/envelope/curve/random/message codecs, voice allocation,
automation/transport/rate/latency, reference/persistence/undo/malformed/cancel/
dependency-loss/routing/teardown and complete accessibility remain required U.
All twenty profiles are partial. Source-supported eligibility/role prose and
browser discovery do not close combinations or entire families.

[Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/manifest-author-r1.json) freezes exact sources/payloads
and both canonical snapshots. [Validation](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/validation-author-r1.json)
checks source/file/hash identity, paragraph locators, counts/case kinds, null target
oracles, all normative IDs through existing `tools/spec_browser.py`, local links,
metadata and untracked-aware whitespace. Run
`python3 analysis/ableton-live-12.4.3/full-spec-v1/max-devices/validate.py`.
Separate semantic review is pending. Root owns shared catalogs, coverage, questions,
execution plan and append-only log; no shared surface or released handoff is edited.
