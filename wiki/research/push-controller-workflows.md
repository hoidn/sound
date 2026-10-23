---
id: RESEARCH-PUSH-CONTROLLER-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Push 1/Push 2 documentary applicability U
specs: SPEC-PUSH-CONTROLLER-WORKFLOWS
---

# Push 1 and Push 2 documentary evidence

## Question and role

Which bounded observable controller workflows are described for each model?
The [canonical draft](../specs/push-controller-workflows.md) owns proposed clauses,
while the [coverage plan](full-live-specification-plan.md) and
[coverage design](full-live-specification-design.md) govern F-08 closure. This
analyst context has read original-reference documentation and cannot implement.
No original/native/application/controller/hardware/audio/MIDI/firmware/candidate
execution, installation, emulator or hardware acquisition was performed.

## Retained sources and extraction

The inventory [TOC](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manual-toc.json)
identifies exact §35/§36 model URLs. No existing exact chapter capture was found
in retained source catalogs. Two official Version 12 HTML pages were captured
once; [sources](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/sources.json) retains URL/final URL, UTC, edition, size/SHA.
Neither source identifies firmware/platform support or exact 12.4.3 applicability.

- D12-USING-PUSH-1: [manual-12-using-push-1-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-12-using-push-1-2026-10-19.html), 331475 bytes, SHA256 `6af1d63f5d9a8bf5294126c0083e390d7d293a0c4a311a4f3cabf19be4d86eb3`, captured `2026-10-19T22:07:08.162487+00:00`; [official chapter](https://www.ableton.com/en/live-manual/12/using-push-1/).

- D12-USING-PUSH-2: [manual-12-using-push-2-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-12-using-push-2-2026-10-19.html), 382624 bytes, SHA256 `b15611fe327190cfe828f2875e541700524009a692bc19dd925f984145562a69`, captured `2026-10-19T22:07:09.382010+00:00`; [official chapter](https://www.ableton.com/en/live-manual/12/using-push-2/).


The retained pure [parser](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/source_parser.py) extracts numbered chapter
headings/paragraphs/lists only, excluding manual navigation. It is copied unchanged
from the pure automation packet parser; no original code is involved. Push 1 has
303 blocks, Push 2 has 403. Each retains HTML line, anchor/section and heading
context, plus a derived text view. Text controls are used only when explicitly
named; figures/inline glyphs/linked videos/tutorials/PDFs were not inspected.

## Interpretation and limits

Push 1 setup P1-B007 and Push 2 P2-B006/B007 are separate connection/power/firmware
contexts. Automatic/driver-free prose is not proof of a working route on this
host, USB packet specification or updater/recovery law. Browsing P1-B009–B015
and P2-B009–B016 uses different named hierarchy/load/preview controls; source
similarity is not generic controller/plug-in compatibility. Content availability
and positive preview output must be established independently.

Drum layouts/steps and melodic pages have model-specific Note versus Layout,
Select, copy/delete and momentary/lock contexts. All pad-number/velocity/MIDI
outputs and timing oracles are null. Textual note membership, active/inactive
pad roles and shape examples cannot provide a MIDI note map, pad calibration,
quantization or voice equation. Push 1 P1-B049 limits pad-note deletion to loop;
Push 2 P2-B058 adds a no-note pad device-deletion branch, kept distinct.

Record/Fixed Length/New/Workflow/Repeat/Quantize and navigation refer to generic
record/clip/scene owners but require this model's explicit gestures and context.
Push 2 P2-B079 Phrase Sync and B094/B095 focused Arrangement/Shift recording have
no adopted modulo/clock or written-event comparator. Push 1 P1-B069 and Push 2
P2-B083 pressure descriptions supply no pressure-to-volume mapping. Numeric
settings/examples, swing and seamless adjectives are not timing/audio oracles.

Device/mixer/rack modes are scoped to corresponding display context. Push 2
Device Rack unfolding P2-B238 and Mix track/rack expansion P2-B254 are different
controls/contexts; the draft does not collapse them into a contradiction or one
fold law. Split-pan mode exceptions remain explicit. Positive source, enabled
nonzero route and unmuted wet return/output are prerequisites, not observations.

Automation P1-B173–B176 and P2-B257–B260 supplies controller arm/delete/re-enable
entry and different presentation, preserving existing REQ-AUTOMATION-ENVELOPES-013
and [generic automation workflows](../specs/automation-workflows.md) unknowns.
Held-step roles do not settle event production, normalization, Nudge arithmetic
or runtime return. Push 2 Simpler/Clip pages are entrypoints to existing owners,
not rewritten sample/Warp/slicing/loop kernels. User Mode recommended relative
names do not equal historical configuration tokens or prove host protocol.

## Source context questions

| Local ID | Retained context | Treatment |
| --- | --- | --- |
| Q-PUSH-001 | P1-B019/B030/B035/B037 describes Note transitions/holds, whereas P1-B032 calls for Layout to enter velocities. P2-B020/B031–B038 consistently uses Layout. | Preserve both Push 1 texts and leave exact Push 1 transition/control-label association U. Do not silently copy Push 2 physical layout or infer a missing button from figures. |
| Q-PUSH-002 | P1-B195 and P2-B305 say a selected track pad press records a new clip while also describing pad launch, without stating all slot/arm/record preconditions. | Treat new-record sentence as incomplete source context; separate populated/empty, selected/unselected and actual arm/monitor/record trials. No selected-populated-slot unconditional recording law. |
| Q-PUSH-003 | P1-B147 labels a triplet color Light Red while saying columns unlit; other per-model color lists and numeric velocity/aftertouch examples are context-sensitive. | No LED palette/intensity, force law, packet or pad-index oracle adopted. No contradiction claim without matched model/mode/firmware and actual states. |

Push 1 control-reference Clip Mode wording and examples remain in their exact
contexts; no uninspected icon or UI label association is inferred. Model defaults,
scale persistence, preferences and broad recording claims remain target U.
Root owns shared question integration, including broader
[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage).

## Future cases and guards

There are 65 requirements (Push 1: 26 D12/six U; Push 2: 27 D12/six U) and 77 cases
(38/39). Eighteen control/display/membership proposals have documentary predicates;
59 are null, including all signal/timing/pad/recording/protocol/wholly unknown
probes. All target outcomes/comparators are null/U/unexecuted; source_claim is
separate and never an audio/event oracle. Neither profile is complete. Remaining
reference controls/pedals, Push 3 standalone/firmware and 149 controller protocols
remain product obligations rather than silently removed denominator entries.

[Fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/fixtures.json) require accepted genuine matching model/firmware/
host/ports and independently working input/display/output. No hardware or media
is supplied. Each probe declares actual mode/target/source, active eligible
section/envelope, nonzero base/depth/amount/gain/send, correct arm/monitor and
nonmuted positive output/wet return with a matched positive trial. Recording also
requires admitted input, explicit appropriate record/Automation Arm and running
transport. A silent source, absent controller or unsupported path stays U.

Per-model finite unknown cases cover inactive contexts, selected/empty slots,
boundaries/malformed admitted controls, Undo, cancel, save/reopen, automation,
transport/rates, disconnection/source loss and teardown. No fake port/host,
firmware action, protocol/timing/pressure tolerance or cleanup law is invented.
Generic owners keep numerical controls and saved-state representation.

## Frozen review packet

[Owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/owner-pins.json) retain 15 current canonical boundaries unchanged;
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manifest-author-r1.json) seals source/derived bytes, fixtures,
requirements/cases, author/parser/validator and both canonical snapshots.
Read-only [validation](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/validate.py) reproduces all 706 blocks, checks source/
owner hashes, permodel evidence/IDs/counts/oracles, exact browser ID equality,
snapshots, local links/anchors, complete payload inventory and untracked-aware
whitespace. It prints stdout only and never rewrites sealed results.

Separate semantic review is required. Root integrates shared catalogs, coverage,
questions and log. This packet provides no original-reference execution,
independent implementation, hardware compatibility or full-profile closure.
