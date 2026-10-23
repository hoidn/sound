---
id: RESEARCH-AUTOMATION-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documentary target parity unknown
specs: SPEC-AUTOMATION-WORKFLOWS
---

# Automation workflow evidence

## Question and boundary

Which observable record/edit/override and clip-envelope workflows are documented
outside the existing finite storage/evaluator contract? The
[canonical draft](../specs/automation-workflows.md) owns the new partial clauses;
the [coverage plan](full-live-specification-plan.md) and
[coverage design](full-live-specification-design.md) govern F-04/F-09 closure.
This is an analyst context. No original function/application, candidate,
hardware/controller, audio renderer or implementation was executed.

The [existing research](automation-envelopes.md) and
[r5 spec](../specs/automation-envelopes.md) distinguish logic evaluation from
engine playback and preserve REQ013 runtime unknowns. The unchanged
[automation-envelopes-v2 release](../../handoff/automation-envelopes-v2/README.md)
has 21 finite storage cases, excludes REQ004/010/011/013, and is not a workflow or
live-recording oracle. Mix-graph owner/time offset assumptions and finite fader
laws remain unchanged. New manual clauses do not silently replace unknowns.

## Retained evidence

No existing exact chapter capture was found in retained source catalogs. The
inventory [manual TOC](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manual-toc.json)
identifies §26 Automation and §27 Clip Envelopes with exact official URLs. Two
bounded HTML captures were retained once, including URL/final URL, UTC, edition,
size and SHA in [sources](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/sources.json). They prove Version 12 publication
text, not the command surface of 12.4.3. All new target applicability is U.

- D12-AUTOMATION: [manual-12-automation-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-12-automation-2026-10-19.html), 298398 bytes, SHA256 `7f570823443a88643c8cff3f43f7c9a35b85fa4574a16b990d4add23726f5d20`, captured `2026-10-19T21:57:17.700220+00:00`. [Official chapter](https://www.ableton.com/en/live-manual/12/automation/).
- D12-CLIP-ENVELOPES: [manual-12-clip-envelopes-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-12-clip-envelopes-2026-10-19.html), 267351 bytes, SHA256 `0c64741c3cb5dffd61d45483bb6b2a414cc5e4c6f2ef1854bd1fcaea00a3c536`, captured `2026-10-19T21:57:18.963096+00:00`. [Official chapter](https://www.ableton.com/en/live-manual/12/clip-envelopes/).

The pure [parser](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/source_parser.py) extracts headings, paragraphs and list
items only within numbered chapter content, stopping before manual navigation.
114 Automation plus 78 Clip Envelopes blocks retain text, original HTML line,
anchor, section and heading context. Image captions/figure text are not parsed
or visually inspected. Original bytes remain immutable; normalized text is derived.

## Source-supported interpretation

Automation A008–A018 distinguishes Session arm/preference/record gating from
Arrangement all-track recording and the two stop controls. A007/A013 distinguishes
clip-based writing from Session performance transfer to track envelopes. This
does not settle point generation, overwrite edges, automation transfer merge or
clock timing. A020/A021 distinguishes first pass, existing Session overwrite,
mouse release and accepted MIDI controller hold; these are ungraded timing roles,
not generalized controller/takeover laws or signal comparators.

A023–A027 distinguishes nonrecording manual override from recording overwrite,
per-target/global re-enable and Session relaunch. Back to Arrangement retains its
existing owner and is not equated with re-enable. A031–A057 supplies chooser,
filter/focus, None, lane visibility/ordering/duplication/removal contexts. The two
duplicate-lane limit is a documented view limit, not multiple automation sources.

A059–A104 supplies mouse/draw/shape/point/segment/transform/simplify and delete
workflow. Simplify's word optimal does not specify an optimization metric or
error bound. Shape names and source extent descriptions are not sampled kernels.
Discrete presentation is not a new Bool/Enum evaluator. A107–A114 gives tempo
display/mapped range and selected-envelope edit scope. Lock-on movement is already
Arrangement REQ032; no duplicate law or lock-off transformation is adopted.

Clip C004–C012 distinguishes audio/MIDI chooser entries, Session kinds and
Arrangement modulation-only Clip View. C017–C034 describes non-destructive audio,
Warp-dependent transposition, gain and Beats-only Sample Offset. The examples'
numeric ranges, imagined tape head and escalation/fade anecdotes are retained
context, not new audio, resampling or timing recipes. C038–C049 distinguishes
absolute automation from relative modulation and clip versus post-effect volume,
send and pan roles; no universal percentage arithmetic or normalization follows.
Active nonzero input/base/envelope/wet paths and paired positive baselines are
required before any ceiling/edge/no-effect investigation.

C051–C054 offers listed MIDI controller editing but says most numbers through
119, not every number, and cautions that receivers need not honor names. C056–C078
describes local unlinked loop/region independence, start/zoom-grid contexts and
Linked Warp response without proving clip-time equations, phase restart, frame
rounding or generated envelope values. The audio sample-pitch example is not
MPE per-note behavior. Generic MIDI/MPE, Warp, clock and recording owners remain.

## Source context questions

| Local ID | Exact context | Treatment |
| --- | --- | --- |
| Q-AW-001 | automation:B099 describes parameter Delete Automation with direct Ctrl-Backspace/Cmd-Delete. clip-envelopes:B011 uses wording about those keys opening a context menu followed by Clear Envelope. | Preserve parameter versus editor/context distinction and both texts. Adopt explicit context-menu Clear only for clip editor; shortcut dispatch remains U. No contradiction or global alias is asserted without same control/focus/preconditions/build. |
| Q-AW-002 | clip-envelopes:B036 says all clip settings including envelopes remain on sample replacement, whereas existing Clip View REQ041/CV:B172–B173 conditions Warp-marker retention on equal sample length. | Sample replacement remains Clip View owned. All-settings is not broadened into unequal-length marker preservation; both source contexts and exact-target state remain U. Future equal/different-duration probes retain envelope/marker inventories separately. |
| Q-AW-003 | clip-envelopes:B012 names certain MIDI auto-reset messages without their identities/values; B053 says most controller numbers up to119; automation:B109 connects displayed tempo range to assigned-controller range. | Retain option/role only; no complete reset table, number set, message bytes, takeover, normalization or tempo-clock law. |

Automation B003 qualifies colors by theme, while Clip B038/B041 uses red/blue
language. The draft retains the theme qualifier and functional distinction, not
a fixed pixel metric. Chooser labels also vary slightly across the two chapters;
the texts do not establish exact aliases for every target build/localization.

## Cases, prerequisites and limits

[Fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/fixtures.json) are future scenarios, not retained ALS/WAV/MIDI or
accepted host/controller setups. They require valid nonempty source, actual
eligible target and recording context, enabled relevant section, nonzero
base/amount/depth/gain/send, nonmuted positive output/wet return, explicit running
transport for recording and matched positive path before negative gates. Correct
receiver Monitor/arm/clip state and Session/Arrangement ownership are independent.
Missing capability or failed baseline is U, never a no-effect or exclusion pass.

The packet has 62 requirements (54 D12/eight U)
and 76 proposed cases: 44 visible documentary
predicates and 32 null documentary oracles. All target
expected/comparison fields are null/U and unexecuted. Signal/timing/MIDI/controller
probes retain source_claim separately, never as an outcome comparator. Compound
clauses require individual retained branches before coverage closure.

Unknown probes cover record output, return/ownership, ambiguous source contexts,
mapping, empty/equal-time/transform boundaries, inactive gates, Undo/Redo, cancel,
save/reopen, transport/rates, target/controller/media loss, admitted malformed
inputs, concurrency and teardown. No arbitrary hidden command, format, fake
hardware, samplerate invariance, universal latency or atomic rollback is invented.

## Freeze and checks

[Authority pins](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/existing-authority-pins.json) identify ten pre-existing
specs and three immutable automation release identities unchanged. The
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manifest-author-r1.json) freezes HTML, derivatives, catalogs,
fixtures, analyst author/parser/validator and both canonical snapshots. The
read-only [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/validate.py) reproduces 192 blocks, checks all source
and authority hashes/full finite release payload pins, exact requirement/case/
browser ID sets, null oracles, snapshots, local links/anchors and untracked-aware
whitespace. It prints stdout and never creates or rewrites a sealed result.

Independent semantic review is required. No whole feature, release readiness,
candidate or application compatibility follows from packet integrity. Root owns
shared index/coverage/question/log integration; broader applicability remains
[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage).
