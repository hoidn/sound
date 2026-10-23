---
id: RES-MAX-FOR-LIVE-HOSTING
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Max for Live host and five template evidence

## Scope and selection

This partial F-05/F-08 analyst packet supports the
[canonical host/template draft](../specs/max-for-live-hosting.md), under the
[coverage design](full-live-specification-design.md). Existing inventory/TOC
selected official `/en/live-manual/12/max-for-live/`; no existing chapter capture
was found among active packets. One retained
[HTML capture](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/manual-max-for-live-2026-10-19.html), 250,005 bytes, SHA-256
`2f771ab26d3e08d4c7df737fbf2a2f95e62cc501739ba65a4531de90d0de69dc`, has exact
UTC/URL in [source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/source.json). Version 12 is established,
exact 12.4.3 applicability remains U. [42 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/manual-blocks.json)
retain HTML paragraph lines and heading context through 32.6; sidebar/footer
excluded. Figures were not inspected separately. Nothing was executed in Max,
Live, a dynamic loader/emulator or a candidate; no tooling was installed.

## Evidence boundaries and individual template roles

[Source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/sources.json) retains eight pins: chapter, device
inventory, TOC and five copied template sources. [Template files](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/template-files.json)
match the inventoried supplied bytes, original paths, size/SHA and 16-byte prefix.
Contents were intentionally left unparsed: there is no graph, constructor,
interface, I/O, parameter/domain, algorithm or runtime proof from AMXD bytes.
The source copies are analyst evidence, not working user patches or clean-room
implementation inputs. Exactly five small inventoried sources were read; no
broader patch/native binary analysis was launched.

| Template | Documentary support | Limit |
| --- | --- | --- |
| Max Audio Effect | MAX:B014-B017: drag default into Set and edit; default passes incoming chain audio onward. | No numerical unity, bit/phase/latency/channel/bypass law or arbitrary edited-patch behavior. |
| Max Instrument | MAX:B015-B017: new editable device from named browser default. | No documented default synth/voice/audio/note response in this chapter. |
| Max MIDI Effect | MAX:B015-B017: new editable device from named browser default. | No default MIDI pass-through, message order/codec or transformation law. |
| Max MIDI Generator | MAX:B024/B026-B027/B030: Generative panel starting point, Edit, Save/Save As and default folder. | No default note/random/occupied-region or expression output. |
| Max MIDI Transformation | MAX:B024/B026-B027/B029: Transformation panel starting point, Edit, Save/Save As and default folder. | No default selection, pass-through, replacement or expression transformation. |

[Inventory boundary](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/inventory-boundary.json) contains 27 entries:
20 shipped Max devices, 2 MIDI Tools, 5 templates. Twenty devices retain separate
pending F-06 scope. [MIDI editing research](midi-editing-tools.md)/its canonical
spec own Euclidean and VelocityShaper algorithms. Tool host/template editing does
not silently extend their version parity or API coverage. General third-party
plug-in contracts and seven bundled native host component models likewise do
not establish Max patch hosting. Shared file/preset/browser/mapping/automation
owners apply only inside their already bounded clauses.

## Context distinctions and open outcomes

Device context MAX:B016-B019 distinguishes current Edit in Max from pre12.2
button and describes optional developer setting. Tool context MAX:B026 names
its own Edit button; context alone explains the different UI and no contradiction
is declared. No Options.txt was edited. MAX:B007-B008 editor path/restart prose
supports selection workflow only, not compatible-Max-version negotiation.
MAX:B019 Save/Save As instance scope is not automatically copied to tools.
MAX:B021 separate AMXD references are not an embedded-Set or transactional-save
codec. MAX:B031-B032 location eligibility supplies no indexing deadline/cache
invalidation rule. MAX:B035-B037 dependency freezing is not Freeze Track, nor
proof of arbitrary external object/sample/license/platform packaging.

No linked API/Max object reference was fetched or treated as an API contract;
MAX:B003 only establishes an advertised Live API surface. Complete Max API,
object/message scheduling, security/permissions, host process isolation, DSP,
MIDI/MPE/tuning, file codec, defaults, clock/performance and arbitrary patch
compatibility require their own exact sources and tests. The host/template
partial draft names those obligations rather than supplying an emulator or fake
host. Unknown dependency loss/save/cancel/history/transport/teardown cannot be
closed by a readable file or a manual statement.

## Finite packet and checks

[38 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/requirements.json): 22 D12, 5 Dpkg, 11 U.
[64 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/cases.json): 22 documentary, 5 package identity and 37 U
runtime/lifecycle obligations; all target expected/comparison null/U/unexecuted.
[Inputs](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/fixtures.json) are future owned-patch/media/clip recipes,
not supplied reference fixtures. Positive baselines require correct offered type,
valid dependency/input, active nonzero signal route/depth and unmuted output;
failed prerequisites stay U. Template-specific five-case groups preserve I/O,
save/reference loss, malformed dependency/AMXD, cancel/undo and teardown/transport
unknowns. Host groups retain app selection, instance/preset identity, discovery,
dependencies/freeze, engine/API and automation/state gaps.

[Author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/manifest-author-r1.json) freezes both canonical
snapshots and every payload; [validation](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/validation-author-r1.json)
checks hashes, source locator text/context, original/copy template identity,
inventory roles/counts, cases/null outcomes, local files/metadata and untracked
whitespace. Run
`python3 analysis/ableton-live-12.4.3/full-spec-v1/max-host/validate.py`.
Structural success is no behavioral pass. Separate semantic review and root's
shared catalog/coverage/question/plan/log integration remain required; this
packet modifies none of those shared surfaces and publishes no handoff.
