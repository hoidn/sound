---
id: RES-REMOTE-CONTROL-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Remote-control documentation and unresolved host contexts

The [canonical draft](../specs/remote-control-workflows.md) follows the
[full coverage plan](full-live-specification-plan.md). Existing
[mapping research](midi-user-mapping.md) and the revision6 canonical spec retain
their finite numeric/configuration/host boundaries. This new source fills a
manual mapping and generic setup gap, not per-profile completion.

## Source identity and method

Official [Version12 chapter](https://www.ableton.com/en/live-manual/12/midi-and-key-remote-control/), captured UTC
2026-10-19T21:57:26.580620+00:00, 264686bytes,
SHA-256 `63dfe96294283a8f5d1bb0876dad48c29a9173a82fe81cfa1ce74ac24726b523`;
[exact bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/manual-midi-key-remote-2026-10-19.html). The separate web-tool reading is not
this capture identity. [90 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/source-blocks.json) were extracted with
the already retained guarded Session chapter parser pinned in dependencies.json.
Anchors and exact HTML lines are preserved; figures/inline glyphs are uninspected.
No application, original function/native host, controller, hardware dump, audio,
MIDI output or independent candidate executed. No tooling was installed.

## Interpretation and source questions

- RC-B003 distinguishes slot binding from clip content, without move/delete or
  empty armed-slot policy. RC-B010/011 describes exclusive remote-note use, but
  supplies no per-port/channel grammar, note-off or MPE interception law.
- RC-B014/015 gives generic named-surface setup and a six-surface documentary
  limit; it is no complete supported-profile list or seventh-row error oracle.
  RC-B016 preset dump is conditional on actual hardware readiness. No dump bytes
  or action are authorized by this documentation task.
- RC-B019/020 manual override/selected-device roles do not establish host
  dispatch. RC-B021 default instrument lock-on-arm, hand status RC-B022 and
  unsupported locking RC-B023 must remain capability/context qualified. These
  observations do not resolve existing REQ-MIDI-USER-007/008 host/bank unknowns.
- RC-B026/027 adds setup/feedback context to routing's existing Remote roles.
  Incoming indicator RC-B028 cannot prove mapped-target response or feedback.
- RC-B031..034 names None/Pick-Up/Value Scaling in current documentation. Existing
  released numeric laws/precision and exact-target label/default assumptions
  stay unchanged. Source smooth/1:1 wording is no new curve or error tolerance.
- RC-B036/037 supports general browser columns/mode visibility, edit/invert/delete
  entrypoints and instant-map exclusion. Rack Macro laws stay with racks; Undo,
  target ownership restoration and held-input cleanup remain unresolved.
- RC-B045..057 and RC-B063..067 describe note/absolute/relative input roles and
  numeric thresholds. Those thresholds are retained context, not new acceptance
  outputs. Manual assignment route, switch grammar, radio quantization, pitch bend,
  high-resolution pairing and parameter display/gain conversion remain U here.
- RC-B060..062 uses UI-family words including Twos Complement, whereas existing
  exact configuration tokens include the literal Compliment spelling. No direct
  family-to-token association or complete UI list is inferred. Auto-detection and
  acceleration are documentary suggestions, without classifier success bounds.
- RC-B070..077 provides relative strip entrypoints; exact navigation/scene number,
  empty/boundary behavior and cancel deadlines are not supplied. Existing scene
  selection/launch/cancel law is linked, not reauthored.
- RC-B079 warns that Clip View mappings can affect selected/multiselected clips;
  it recommends relative controllers, not guaranteed smoothness. Panel rendering
  and selection remain Clip View's. RC-B082..090 KEY mapping cannot establish
  global shortcuts, Computer MIDI Keyboard, IME/text/plugin precedence or repeats.

Root owns canonical question-register integration. Required local questions are
retained as five U requirements and concrete null probes, rather than choosing a
law from another input route or silently narrowing the product denominator.

## Freeze, coverage and remaining evidence

37 requirements = 32 D12 +5 U;
47 cases = 32 documentary roles +15 U probes.
All target outputs/comparisons are null/U/unexecuted; only visible browser/control
predicates have documentary proposals. Signal/event/numeric/timing/protocol
outputs are null as well. [Fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/fixtures.json) are finite future
recipes, not supplied sources/results. Compound branch, automation/transport/
sample-rate, saved-state migration, malformed/cancel/undo/failure/recovery/teardown
and every controller's actual protocol remain partial or unknown.

[Owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/owner-pins.json) retain existing canonical/release bytes;
all 166 midi-config-v4 payload hashes were independently
checked, without editing the release. [Snapshots and manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/manifest-author-r2.json)
freeze the reviewable packet. Read-only validation checks source extraction,
IDs/cases/nulls/guards, exact browser equality, links, pins and untracked whitespace.
Run `python3 -B analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/validate-author-r2.py`.
Separate semantic review is required. Shared catalogs/coverage/plan/questions/log
are integrated by root; this packet closes no entire UI/controller family.

## Revision2 focused correction

RC-REVIEW-001 found that REQ-REMOTE-WORKFLOW-023 used slot down/up shorthand
where RC-B064 explicitly describes increment as Note On and decrement as Note Off.
The clause and RC-023 source_claim now name those roles explicitly, distinct from
RC-B072 highlighted-scene up/down navigation. Launch-mode ownership, source/actions,
codecs/steps/timing unknowns and all null event/target oracles are unchanged.
Exact revision1 manifest, all15 payloads, validation and freeze were archived in
archive-r1 before edits. New snapshots and the revision2 seal preserve the correction;
response-r2.json records the single-predicate delta and remaining partial scope.
