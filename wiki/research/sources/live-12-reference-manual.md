---
id: SRC-LIVE-12-REFERENCE-MANUAL
type: source
status: current
updated: 2026-10-19
access: analysis
target: Official Ableton Reference Manual Version 12; exact 12.4.3 applicability unknown
---

# Official Live 12 manual captures

## Identity and authority

Publisher: Ableton. Entry URL:
[Reference Manual Version 12](https://www.ableton.com/en/live-manual/12/welcome-to-live/).
Captured 2026-10-19. The online manual names the major release, not a patch/build
or immutable publication revision. Publication/update date is not established.
Each captured byte stream has its own SHA-256 and UTC/URL metadata where retained.
A page fetched twice may differ; neither capture supersedes pinned product bytes.

The manual is an official documented-behavior source, not a run of Live. D12
contracts describe the captured documentation. Their applicability to installed
[Live 12.4.3](ableton-live-12.4.3.md) stays unknown until corroborated. A matching
product/device name or stored class does not verify the chapter's detailed rules.

## Retained captures and owners

| Source group | Exact identity and retention | Canonical analysis/specification owner |
| --- | --- | --- |
| Manual contents | [Inventory manifest](../../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manifest.json); HTML SHA-256 `584d4b61d119c96ecdb7941ef34ac9d4e0282a3e40c8bc474b6cf24892640d80`; 880 numbered entries / 708 leaves / 43 chapters | [Product inventory](../full-live-coverage-inventory.md); discovery only |
| Arrangement and Concepts | [Arrangement manifest](../../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manifest.json) and its source metadata; HTML digests `caf57b34a10fa4163300bced0a4384656d2823eefba340ad82327e9118e05842` and `da51ae19eab185813aac3b4240b7fad6022885421a3794155ca1207fd6e2eed5` | [Arrangement evidence](../arrangement-editing.md) and [contract](../../specs/arrangement-editing.md) |
| Recording, Comping, Routing and Session | [Recording manifest](../../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manifest.json); `sources.json` retains individual URLs/times/hashes | [Recording evidence](../recording-comping.md) and [contract](../../specs/recording-comping.md) |
| Browser | [Source manifest](../../../analysis/ableton-live-12.4.3/full-spec-v1/browser/source-manifest.json) and `capture.json`; HTML SHA-256 `4e34895d5d37d6579e29cb65156b83c53672e89bd01b3bd8233596fc5b17e8b3` | [Browser workflow evidence](../browser-workflows.md) and [contract](../../specs/browser-workflows.md) |

The [rack packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manifest.json)
adds the official racks and common-device chapters; the
[MIDI editing packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/manifest.json)
adds editor/tool chapters; the
[project/media packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manifest.json)
adds Managing Files and Sets. Their own source metadata pins every capture;
their owning research/spec pages are linked from the domain indexes. All retain
the same exact-build applicability limit.
The [export packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/audio-video-export/manifest.json)
reuses the exact project/media Managing Files HTML, SHA-256
`04fef126e1085053b790ea43b16596e33e82598ec54449418208e2b5fb9ad3d6`.
The [native MIDI-effects revision 2](../../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/manifest-author-r2.json)
pins its MIDI-effect chapter and source metadata; the
[Utility/Tuner/Spectrum packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manifest-author-r1.json)
pins audio-effect chapter HTML SHA-256
`9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`.
These partial drafts have independent source/scope/case reviews, with all
application exact-build outcomes still unknown.

HTML is the captured source. Normalized text is a derived navigation aid, not a
replacement original. Captures remain analyst evidence; this record authorizes
neither republication of the whole manual nor its inclusion in a clean handoff.
Only bounded reviewed contracts/public references cross that boundary.

The [MPE/tuning/groove revision2 packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/manifest-author-r2.json)
pins three manual chapters and explicitly limited retained web-rendered support
responses after direct HTTP403; rendered bytes are not claimed as publisher HTML.
The [sample-instrument revision2 packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manifest-author-r2.json)
pins instrument chapter HTML SHA-256
`3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a`.
The [filter/EQ packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manifest-author-r3.json)
and [dynamics packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/manifest-author-r1.json)
reuse the exact audio-effects chapter rather than recapturing it.
[Third-party hosting](../../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/manifest.json)
pins Using Plug-Ins HTML SHA-256
`df44bdab506fa5422fbe4da0fceaff6e8250e3117d9f5b53802889c83e3e7a1a`.
[Media/cache/interchange](../../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/manifest.json) retains the original packet.
[R4 explicit-On/Off case refinement](../../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/manifest-author-r4.json)
passed [focused partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/media-file-workflows-r4-review.json); it
reuses Managing Files; [navigation/accessibility](../../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/manifest.json)
pins two new chapters with full URL/UTC/hash metadata and292 extracted shortcut
rows. All detailed current-manual exact-build applicability remains U.

[Audio-to-MIDI conversion](../../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/manifest.json)
pins the newly retained chapter, SHA-256
`52c513cf72f707a5298d74c745015eccb5bc9db0f735a7e2219f7f77353e6123`.
Its source metadata records exact URL/UTC/bytes; documented conversion workflows
remain distinct from exact-build classifier or audio results.

The [delay/reverb revision2](../../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manifest-author-r2.json),
[distortion revision2](../../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/manifest-author-r2.json)
and [modulation/pitch/loop packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manifest-author-r2.json)
reuse the exact retained audio-effects HTML. All three partial scopes have
independent reviews; the Echo internal idle-shutdown statement stays U/null,
and spectral schema associations use the reviewed inventory correction. None
adds observed audio, lifecycle or exact-build applicability.

The [synthesis packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manifest-author-r2.json)
reuses the exact instrument chapter; its five partial profiles passed source/case
review. The [external-hardware packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manifest-author-r2.json)
reuses both instrument/audio-effect captures; formatting correction passed review.
The [Clip View packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/manifest-author-r1.json)
adds official chapter HTML SHA-256
`30f156e6d83c8f4caf3fe9dcf55bb2b764dc42ed8cbd3847863a53747851bd80`,
306606 bytes/180 blocks; reviewed partial scope retains all target outcomes U.
The [Session revision2 packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/manifest-author-r2.json)
reuses the original recording Session chapter with77 locators; metadata ownership
correction passed focused review. The [legacy packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/legacy-devices/manifest-author-r1.json)
separately retains official **Version11** audio-effects HTML SHA-256
`98a59baaa97cff409894870f26eb04697c28f8c59ecedc40ade395dcf36438d4`,
497168 bytes. Its reviewed predecessor contracts are D11/target-U, not Version12
parity or modern-device aliases. All source identities/UTC/locators stay in the
owning packets; source-content/file audits never become application tests.

The [Max host/template packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/manifest-author-r2.json)
adds the official Max for Live chapter,250005 bytes, SHA-256
`2f771ab26d3e08d4c7df737fbf2a2f95e62cc501739ba65a4531de90d0de69dc`,
42 blocks. Its38 requirements/64 cases are partial; browser formatting correction
passed focused review; template hashes do not establish arbitrary patch or public API behavior.
The [video packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manifest-author-r1.json)
adds Working with Video,251482 bytes, SHA-256
`76c940973456cf47c91157e308345544f058d0e98a9fa3f92ad6b88efc8a238a`,
39 blocks. Original18/28 R1 is preserved; [R2 spec/R3 research](../../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manifest-author-r3.json)
now support20requirements/34cases, [independently reviewed as partial](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/video-workflows-owner-r3-review-final.json).
Both captures retain exact URL/UTC metadata; detailed12.4.3 applicability remains unknown.

The [routing/monitoring packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manifest-author-r1.json)
reuses exact earlier Routing and I/O and Working with Instruments and Effects
captures, and adds Mixing,276916 bytes, SHA-256
`255923c650a256ea0c663e83351e3ac0d8f14ba8dfe12706825754b2066de02e`.
Its226-block corpus includes selected compensation/cue/track-delay contexts;
40 requirements/69 cases passed partial-scope review, with all target outcomes U.

The [twenty Max-device packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/manifest-author-r1.json)
retains current Max for Live Devices HTML,299403 bytes, SHA-256
`b95a0d3ed3d7217505437a0d7d65de68d37e0f894d27e9869122fbfb89728a46`,
218 blocks. Current English headings omit DS Sampler and Expression Control
Legacy. Those two profiles use a separately retained official Version12 PDF
under a2025-06-02 path,76333838 bytes, SHA-256
`42fbd3794df0d69aaf522aea589bf08dd3dc8db3eb0e135cab041093875db976`.
Only physical pages721/730/731 supply15 retained blocks. D12-2025 is explicitly
dated/context evidence, not current-build parity or current Expression Control
behavior assigned to Legacy. The partial135-requirement/315-case packet passed
independent source/scope review; all target outcomes remain U.

## Workflow extensions — 2026-10-19 continuation

The [bundled-workflow seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manifest-author-r1.json)
reuses the exact instrument/audio-effect captures for401 selected blocks.
Its55 requirements/118 cases passed independent partial-scope review; existing
parameter/storage/finite-DSP source authorities and releases remain unchanged.

The [launch/Follow freeze](../../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/freeze-author-r1.json)
retains the Launching Clips capture,73 blocks and scoped released-enum pin.
Its43 requirements/68 cases passed independent partial-scope review; source
contexts remain in Q030 and no RNG/timing/launch execution oracle is inferred.

The [Bounce/Freeze seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manifest-author-r1.json)
retains three exact pages: current Version12 Bounce, current Version12 Resources
Freeze, and Version11 Resources only as predecessor context. The59 selected
blocks distinguish current Bounce/Freeze from predecessor Flatten and conflicting
Arrangement sample-count wording. The41-requirement/77-case draft passed independent partial-scope review.
All URL/UTC/byte/hash identities and unchanged reused Mixing pins are in its
[sources catalog](../../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/sources.json).

The [synchronization seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r1.json)
retains the official Version12 Link/Tempo Follower/MIDI chapter,261580bytes,
SHA-256 `55dcef3b8171e721c641ab69476a075db8c3c8893055914538f9e4eb801d00ac`,
captureUTC2026-10-19T21:48:54.932595+00:00. Its54 blocks support a partial
original26/36 R1 draft. [R2](../../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r2.json)
with27requirements/37cases passed [independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synchronization-owner-r2-review.json)
after exact source-claim/case reconciliation. [R3](../../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r3.json)
with29requirements/42cases passed [independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synchronization-owner-r3-review.json),
adding only Resync public controls and three symbolic mode roles from exact
retained Routing source. Exact12.4.3 Link Audio availability,
wire protocols, detector/numeric/timing laws and all target outcomes remain U.

[Recording R3](../../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manifest-author-r3.json)
passed [focused partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/recording-comping-r3-review.json).
Only RC020action now explicitly sets the scene-recording preference Off after a
genuinely productive enabled baseline;32clauses/81documentary comparators and
original source identities are unchanged. The original Markdown-only cases have
a disclosed historical transcription, not a retroactively invented JSON catalog.

The [settings/help seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r1.json)
retains First Steps,261023bytes, SHA-256
`59601f2af92f1148b23213edc0471339c9ac1188a401f717e3067d67b55e2746`,
captureUTC2026-10-19T21:59:13.502275+00:00. Its70 blocks support a partial
original21/30 settings/Learn/Info draft. [R3 local cases](../../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r3.json)
retain21unchanged requirements and31cases, [independently reviewed as partial](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-learning-owner-r3-review.json).
[R4 configuration bridges](../../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r4.json)
with23requirements/33cases then passed [independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-learning-owner-r4-review.json).
The reviewed audit covers70retained blocks only, with exact cross-owner gaps separately retained.
Newer feature availability, clip-color preference context Q031, installation,
authorization, update and all exact-target outcomes remain unknown.

The [Warp workflow seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manifest-author-r1.json)
retains Audio Clips, Tempo, and Warping,283979bytes, SHA-256
`295a442252730b7f1bb6154b9cbfe041f09c6d40d45d487a42e793ae8423c2ad`,
captureUTC2026-10-19T21:55:52.320855+00:00. Its131 blocks support the original
50requirements/88cases R1 partial draft. [R2](../../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manifest-author-r2.json)
with the same50requirement IDs/91cases passed [focused independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/warping-workflows-owner-r2-review.json).
Q032 retains import-readiness contexts;
no automatic marker, DSP or clock outcome is established.

The [remote-control seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/manifest-author-r2.json)
retains MIDI and Key Remote Control,264686bytes, SHA-256
`63dfe96294283a8f5d1bb0876dad48c29a9173a82fe81cfa1ce74ac24726b523`,
captureUTC2026-10-19T21:57:26.580620+00:00. Its90 blocks support a partial
37-requirement/47-case corrected R2 draft independently reviewed as partial; exact native/config token parity,
message codecs/feedback and all149profile obligations remain open.

The [stem-separation seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/manifest-author-r1.json)
retains Stem Separation,254199bytes, SHA-256
`62235634fac7ed29ff6bf6a586e8bf0d4980890a444f20becb0eb250a6499dcf`,
captureUTC2026-10-19T22:02:16.363028+00:00. Its32 blocks support a partial
original18-requirement/29-case partial draft. The unchanged source also supports a
[preserved R2](../../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/manifest-author-r2.json)
with20requirements/32cases, [independently reviewed as partial](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/stem-separation-owner-r2-review.json)
after32-block/94facet source reconciliation. Feature/model availability, audio,
region/nongroup/file outputs and exact-target outcomes remain U; private model/
pass/CPU/GPU narratives are context, not candidate architecture or performance law.

The [automation/clip-envelope seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manifest-author-r1.json)
retains Automation,298398bytes SHA-256
`7f570823443a88643c8cff3f43f7c9a35b85fa4574a16b990d4add23726f5d20`,
and Clip Envelopes,267351bytes SHA-256
`0c64741c3cb5dffd61d45483bb6b2a414cc5e4c6f2ef1854bd1fcaea00a3c536`,
capturedUTC2026-10-19T21:57:17.700220+00:00 and21:57:18.963096+00:00.
Their192 blocks support62requirements/76cases independently reviewed as partial.
Existing finite envelope/mix/timebase/storage authorities remain unchanged;
Q033 retains shortcut/sample-replace/MIDI reset contexts, all target outcomes U.

## Later controller, engine, Browser and workspace captures

[Push sources](../../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/sources.json)
retain exact Push1/Push2 URLs, UTC captures, HTML hashes and706 blocks.
The [independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/push-controller-workflows-review.json)
read all65 clauses/77 actions and330 selected blocks semantically; all706 were
mechanically reproduced. Unread passages, figures, hardware/protocol and target
outcomes remain unknown; source capture is not full-chapter semantic approval.

[Engine/resource sources](../../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/sources-all.json)
retain Audio/MIDI Fact Sheet captures and the reused, unchanged complete Resources
capture. All195 blocks and the28-clause/50-case partial scope passed
[independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/engine-resource-workflows-review.json).
Private precision/thread architecture descriptions and historical performance
comparisons are not candidate design choices or exact-target numeric tolerances.

[Browser content sources](../../../analysis/ableton-live-12.4.3/full-spec-v1/browser-content/sources.json)
reuse268 Browser blocks and six similarity blocks from the earlier Concepts
capture with SHA-256
`da51ae19eab185813aac3b4240b7fad6022885421a3794155ca1207fd6e2eed5`.
All274 blocks and56 requirements/71 actions passed
[independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/browser-content-workflows-review.json).
Service/account/protocol/similarity and exact-target outcomes remain U.

[Workspace sources](../../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/source.json)
retain a distinct later Concepts capture,306807 bytes, SHA-256
`611eeb0d7ffa1cb63aacd5bafbfbb3e60803836f4ca02f0e4aabb017fb7cf5c9`,
captureUTC2026-10-19T22:23:42.054730+00:00. Its125 blocks and13 requirements/
23 actions passed [independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/application-workspace-review.json).
This capture never replaces the earlier Concepts identity used by Browser;
Scale/Fold/marker contexts and all exact-target outcomes remain U.

The [editorial-topic companion](../../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r5-nonbehavioral-topics/manifest.json)
retains Welcome/Credits identities and31 blocks. Its
[independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/nonbehavioral-manual-topics-review.json)
accepts only the three named source headings/two leaves as editorial. Original
TOC rows remain visible; no application help/credits/branding/legal obligation is
removed, and no legal interpretation is established. Welcome capture UTC remains
unknown beyond its original date; no timestamp was invented.

The [additional mixing interaction seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/manifest-author-r1.json)
reuses the original276916byte Mixing capture SHA-256
`255923c650a256ea0c663e83351e3ac0d8f14ba8dfe12706825754b2066de02e`,
captureUTC2026-10-19T21:33:28.556179+00:00. All94blocks/18new clauses/33actions
were read during [independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mixing-workflows-review.json).
No source was recaptured, source gap-scope history rewritten, chart inspected or
numeric/graph/recording rule replaced. Five source contexts and target outcomes U.

The [captured-heading census](../../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r9-captured-manual-headings/README.md)
and [structural review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/captured-manual-headings-r9-review.json)
reconcile44distinct retained Version12 captures at43chapter URLs, preserving
both Concepts hashes and every physical binding. They identify1,066distinct
actual heading URLs,186beyond the original880navigation URLs, including the14
Browser discoveries. This is a finite heading ledger, not a paragraph read or
behavioral closure; eight captures retain unknown UTC. Original source bytes,
TOC rows and historical citation joins remain unchanged.

The [Keyboard source audit R2](../../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation-source-audit/README-r2.md)
and [focused correction review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/keyboard-navigation-source-audit-review-final.json)
preserve the full541block/two-chapter audit and292binding discovery rows. Five
context-association rows are corrected; this audit alone establishes no dispatch
or owner adoption. The separate [Keyboard owner R5 review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/keyboard-navigation-owner-r5-review.json)
approves partial40requirements/96cases, with19new clauses/54new cases, ten old
clause refinements/four old action refinements and292unchanged discovery rows.
Q052 retains two exact source differences and all target outcomes U. The [Mixing source audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-source-audit/README.md)
[passed independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mixing-source-audit-review.json),
reconciling94blocks/178facets with23clauses/33actions. Its17proposed groups remain
non-normative until separately reviewed owner adoption; all target outcomes U.
The separately [reviewed Mixing owner R2](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mixing-workflows-owner-r2-review.json)
now has31requirements/50cases, retaining all23old clauses and changing only eight
old actions before adding eight UI roles/17cases. All17audit groups retain open
outcomes; source94blocks and original snapshots stay exact. The [bounded Monitoring subsection reconciliation](../../../analysis/ableton-live-12.4.3/full-spec-v1/monitoring-source-reconciliation/README.md)
[passed independent source-only review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/monitoring-source-reconciliation-review.json),
retaining complete nine-block §17.1text and seven compensation-context blocks.
Its two proposals received separate [RML owner R2 partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/routing-monitoring-owner-r2-review.json):
41requirements/70cases, with blue In Activator display and explicit right-click
history; all40old clauses and69case identities are preserved. No duplicate
mode/multiselect/reset case, default or timing law follows.
Both audits retain literal resource text/attributes, with image pixels and linked
destinations uninspected. Source assignment and character accounting are not closure.

The [complete retained Clip View text audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view-source-audit/README.md)
[passed independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/clip-view-source-audit-review.json):
180blocks/309overlapping claim-context facets reconcile54clauses/62actions,
with24audit-only proposals. Source306606bytes/SHA30f156e6…51bd80 and its original
captureUTC remain exact. All source text and actual owner actions were read;
41image pixels/46linked destinations stay uninspected. Q031 and Q053 remain
open. Existing Mixing group-color coverage is a true cross-owner route to reuse;
source-accounting and selected-owner gaps do not demand duplicate cases or laws.
The separate [Clip View owner R2 review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/clip-view-owner-r2-review.json)
approves partial55requirements/92cases, six contract refinements/one old action
refinement/two documentary qualifiers and30local gesture trials. It reuses the
existing Mixing group-color case, preserves actual Gain edits and adds no new
Gain/numeric/file/audio law. Q031 and Humanize remain U; Groove/Media/MIDI/shared-
reference extensions remain with their actual owners.

The [complete Session chapter source audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/session-grid-source-audit/README.md)
[passed independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session-grid-source-audit-review.json):
77blocks/142facets against29contracts/40actions,59literalresources and17audit-only
proposals. It preserves capture2026-10-19T19:53:59.135059+00:00 and
SHA16e29141…9470a31, with no pixels/destinations inspected. Existing productive
Mixing group-slot branches are reused; SessionB074 StopAll Arrangement wording
stays U. Source review alone adds no normative adoption or completion. Separate
[Session owner R3 review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session-view-owner-r3-review.json)
approves partial30requirements/57cases:29old requirement/40oldcase records exact,
one scene Edit-entrypoint clause/17 contexts appended, with two U-only and two
external-pending groups; all target outcomes remain U/null/unexecuted.

The [MIDI Interval owner R2 review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-editing-interval-owner-r2-review.json)
independently checks five complete selected §10.5.9.4/§10.5.9.7 MIDI records and
two Clip View paragraphs against original HTML. The [retained query](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-utility-source-context-query.json)
clarifies selected versus no-selection Interval Size/Add Interval contexts;
43old clauses/57old cases are exact and three explicit actions are added.
MIDI source date2026-10-19 has unknown exact UTC. This is not a new full MIDI
chapter read; Humanize Q053, C1–C3 and all target outcomes remain U.

The [complete retained Grooves text audit R2](../../../analysis/ableton-live-12.4.3/full-spec-v1/groove-source-audit/README-r2.md)
[passed focused independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/groove-source-audit-review-final.json):32blocks/17literalresources against14actual
clauses/24actions, with ten audit-only proposal groups and no normative adoption.
Exact249336-byte SHA b8cb67fd…54cad89 is unchanged; original date-only capture
keeps UTC unknown. Selected Clip View062–064 and Racks022/RCK046 contexts
prevent duplicate extraction cases and distinguish shared replacement/positive-
velocity audio Commit from narrower current cases. Image pixels and linked
contents remain uninspected; all actual outcomes U/null/unexecuted. The R2
correction clears two erroneous primary Groove012/GRV012 links from Rack-chain
extraction, retaining correct external Racks022/RCK046. Every R1 byte remains exact.
Separate [Groove owner R3 passed independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/groove-owner-r3-review.json):14unchanged IDs/34cases, only001/010/014 refined and ten source-context actions appended. Positive-velocity audio Commit requires a productive effect plus nonflat prior volume envelope; old finite Quantize/Commit arithmetic is exact. Seven new actions have named documentary relations and three retain null documentary comparators; all actual outcomes null/U/unexecuted. Random advice stays research-only and Rack extraction is reused, not duplicated.

The [Arrangement source audit R2](../../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement-source-audit/README-r2.md)
[passed focused independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/arrangement-source-audit-review-final.json)
after the full164Arrangement/22selectedConcepts read:314facets against35clauses/
65actions and19audit-only proposal groups. Both Transport/Playback and Arrangement
Mixer are included. Six assessment strings now describe the pinned old SV001
neighboring launch gestures accurately, preserving the any-order source claim
without borrowing later Session R3.137literalresources retain uninspected pixels/
destinations, all actual outcomes U and zero normative adoption/completion.

The [complete retained MPE audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-source-audit/README.md)
[passed independent partial source review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mpe-source-audit-review.json):
66blocks/110facets against18clauses/27actions,28literalresources and13audit-only
proposals. Exact259102-byte SHA11d135bd…633568e/date-only2026-10-19 capture is
preserved, UTC unknown. Only selected rendered FAQ L102–106,26external records
and14Glissando/LFO blocks supply neighboring context; no full neighboring source
review. All111watched paths remained unchanged. Public per-note reception,
offline editing, generic indicators, plugin defaults/output and output-only zones
remain distinct; Fold/C3 and numeric/protocol/target outcomes U. No new normative
IDs, actual execution, pixel/destination inspection or completed topic follows.

The [complete retained MIDI chapter audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing-source-audit/README.md)
[passed independent partial source review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-editing-source-audit-review.json):244blocks/506facets/144literalresources against
43actual clauses/60actions,58selected external contexts and38audit-only groups.
This does not claim full MIDI Tools chapter reconciliation or target observation.

Separate [MPE owner R3 passed independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mpe-owner-r3-review.json):
18IDs/50cases, nine refined rows/23new actions with27oldrecords/79priorfiles exact.
Ten new UI relations and13null documentary outcomes distinguish recording/output,
editor/configuration, generic activity/per-note delivery and over-note/optional
lane contexts. All157watched paths exact; no new numeric/protocol/build oracle.
At that increment the distinct MPE50/Tuning32/Groove34 union116 preserved the original shared83; current127routing is below.
Full49-block Tuning audit independently reviewed as partial; Tuning owner R3 independently reviewed as partial (21IDs/43cases). Separately the full146-block MIDI Tools
text audit [passed independent partial source review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-tools-source-audit-review.json):302assessments/101literalresources,
43R2clauses/60actions/30selected external records and21audit-only proposals.
All51watched paths exact;17true tool subsets remain, with genuine nonzero Strum
and nonempty generator prerequisites. C1/C2/C3 and implicit-loop selection context
stayU; Standard/Suite bundled-tool use differs from edit/build/add-on context.
This source audit is not part of the Editing MIDI chapter audit or a target pass.

Separate [MIDI gesture R3 passed independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-editing-gesture-owner-r3-review.json):
43IDs/72cases, six rows/nine append-fields and12new actions; all60old cases/17tool
rows and25old files exact. Eight new named/four null documentary comparators and
all actual U/null/unexecuted;17selected raw paragraphs were checked and77review
watch paths exact. Only eleven audit-group subsets adopted, not all38groups.
At that source checkpoint Tools owner R4 was authoring; its preserved focused R5 review is below. Humanize/C1–C3/Q052 remain unresolved.

## Use and limitations

The incremental records below preserve the disposition of each named audit or
owner freeze. Earlier authoring/no-adoption statements describe that historical
phase; the [sole execution plan](../full-live-specification-plan.md) and
[spec index](../../specs/index.md) own current assignments and review status.

Use exact HTML heading anchors plus capture digest for citations; section numbers
can change. Keep contradictory passages together and route unresolved outcomes
to the owning spec or [Q-027](../../questions.md#q-027-whole-product-specification-evidence-and-version-coverage).
Text inspection does not establish an inspected image, layout measurement,
keyboard accessibility result, timing/DSP law or observed failure behavior.

This is a selected capture register, not a claim that every chapter has been
read, that every manual leaf is a normative requirement or that the TOC is the
complete product denominator. Installed-only, platform, service and cross-feature
surfaces remain separately inventoried. Preserve original bytes and add new
captures for changed source content.

Arrangement [owner R3 focused review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/arrangement-editing-owner-r3-review.json)
approved the minimum ARR-R2-REVIEW-001 correction: nine numeric/duration
documentary pairs become null, giving43named/41null across84cases. All42clauses,
actions, source claims and35old files remain exact. This carries the separate
full R2 semantic review; no second full-source read or numeric law is claimed.
At that checkpoint the full124-block Racks primary chapter audit was authoring against
28clauses/61actions. Common Devices153blocks are only selected adjacent context.

The [Tuning source audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/tuning-source-audit/README.md)
[passed independent partial review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tuning-source-audit-review.json):49primary manual blocks/68assessments,32literal resources,21actual
clauses/32actions,19selected rendered FAQ/ASCL contexts and35adjacent records.
Twelve groups in the source-only packet remain audit-only; the separate owner R3 review is below. Date-only UTC
null, rendered-response/direct403 and ASCL-asof12.1 limits remain explicit.
Actual configuration, effective tuned audio, SCL reference, ASCL special case,
Tuner and API boundaries remain distinct. No normative adoption or target pass.

The full40-block [conversion audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi-source-audit/README.md)
is frozen for independent review:14resources,14clauses/29actions,40whole-context
judgments and five audit-only groups. Mixed judgments are not atomic-facet or
completion denominators. Original commands, slicing threshold/correspondence,
existing multiactions and documentary expected predicates remain exact; actual
and new documentary results remain null/U/unexecuted.

[Tuning owner R3](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tuning-owner-r3-review.json)
passed independent partial review:21IDs/43cases with32old records/97old files
exact, five fields refined and eleven bounded histories. Three new named UI
pairs/eight null documentary pairs preserve actual null/U/unexecuted. Logical
current MPE50/Tuning43/Groove34 union127 supersedes the previous union116 route
without changing original shared83. No new numeric/parser/audio/protocol law.

[Racks source audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-source-audit-review.json)
passed independent partial review:124blocks/264assessments/53literalresources
against28clauses/61actions;22audit-only groups. Twenty-one file pins/two embedded
asof canonicals and29watched paths stay exact. Separate153-block common Devices
chapter audit is authoring. [Tools R5 focused review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-tools-owner-r5-review.json)
approved three source-role corrections carrying unchanged full R4 review scope;
43IDs/93cases,72earlier records/source claims/oracles/guards exact.

The full153-block [common Devices audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/device-chain-source-audit-review.json)
passed independent partial source review:110paragraphs/25listitems/18headings,
140literal resources,153whole-context judgments and20audit-only groups. All54
immutable input pins/four embedded asof snapshots and60watched paths unchanged;
14semantic rejection fixtures and parser fixture pass. A/B state-specific
automation, selected-state copy/presets, plug-in exposed-list versus values,
sample swap hover exception and separate default histories remain bounded.
No new owner IDs/cases/coverage, image pixels or target execution.

[Conversion owner R3](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/audio-to-midi-owner-r3-review.json)
passed independent partial review:14IDs/37cases,29old records exact; five clause
appends/two qualification references/eight new histories. Six selected common
paragraphs134–139 qualify factory/no-custom preview contexts. First sealed
checker failed relative/absolute path identity; initial bytes/seal preserved,
exact two-line additive checker successor passes. Use the [current integrity guide](../../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/README-r3-final.md).

[Primary Racks R2](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r2-review.json)
requires one narrow clarification: resize either main/fade section at edges,
move the zone itself; independent fade-section translation is not established.
Focused preserved R3 subsequently passed independent partial review (below). Original primary source audit shorthand
A089/A090/G05 needs additive qualification, not a rewritten source/audit.

[Utility/Tuner/Spectrum full-section source audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/audio-utilities-source-audit-review.json)
passed independent partial review:46selected blocks/101qualified assessments,
19literalresources, nineaudit-only groups/threequestions. Full1137chapter parse
was filtering only. Fiftyimmutable pins/four exact asof snapshots,60watchpaths,
14negative fixtures/inline-glyph parser/refusal passed. Old41clauses/103actions
and sixDpkg file-only grades preserved; no owner adoption/coverage credit.
Productive control/detector/history prerequisites remain distinct from proposed
signal definitions, UI flags, source numeric labels and installed file values.
Separate filter/EQ full108-block four-section audit is authoring.

[Racks owner R3](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r3-review.json)
passed focused independent partial review after the full R2 semantic review.
One007append/066action separates either-section edge resize from moving the
whole zone; independent fade-section translation remains U. Additive audit
qualification pins rawB044 and exact oldA089/A090/G05 without changing old bytes.
Current28IDs/81cases=3installed/66documentary/12U,all61oldrecords and all81
sourceclaims/oracles/guards exact. Retained18meaningfulfixtures+threefocused/
10true subsets pass,63watched paths unchanged. No CommonDevices adoption or
wholeRack/exact-build completion.

[Native MIDI full-chapter source audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/native-midi-effects-source-audit-review.json)
passed independent partial review:112blocks/235qualified assessments,19literal
resources,27clauses/146fullactions and30selected adjacent actual records.
Twenty-one proposals/sixquestions remain audit-only, allnewdocactualnullU.
Original54D12/92U,80lifecycle probes and threeR2narrowings remain exact; finite
32random trials do not prove liveness/proportions, enumeration not sufficient
fixture/closure proof. Fiftyimmutable pins/all32oldfiles/opaquearchive/twoasof
snapshots/58rootwatchpaths exact;14negative/45true/parser/refusedwriter pass.
Root read preseal plan/checker/inputs and reconfirmed exact frozen identities.
No archive extraction/package decode/oldtool/native/runtime/hardware/network
execution or owner adoption; exact12.4.3 and all eight profiles remain open.

[Utility/Tuner/Spectrum ownerR2](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/audio-utilities-owner-r2-review.json)
passed independent partial review:41IDs/112cases (Utility41/Tuner35/Spectrum36),
103oldrecords/41oldfiles exact. OnlyUtility005continuous0→100M and013DCsonic
necessarycondition appends; ninecompound futurehistories allnewdocactualnullU.
SixtythreeD12/sixhistoricalfile-onlyDpkg/43U,all106applicationcases ungraded.
Fullnineactions/twoappends/ninegroupdeltas/currentchecker read;62sealedpayloads/
59packetfiles/58pins/fourpagereconstructions/14asofconsumerpointers verified,
18negativefixtures/41BrowserIDs/142links/81watchpaths pass. No pixel/detector/
DSP/numeric/timing/filelaw or completeprofile; original46-block source audit
remains source-only, current owner adopts only its bounded group subsets.

[Filter/EQ full selected-section source review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/filter-eq-source-audit-review.json)
approves partial108blocks/108whole-context judgments (notatomicfacets),28literal
resources,65clauses/128fullactions/finitefixtures. Twelveaudit-only proposals/
fourquestions; bothAutoFilterdetector/Type discrepancies andmodern/Legacy scope
remainU. Trueisolatedmodulator/combinedpath/stochasticUI/PeakScale/threeLED
positivehistories preserved; newRes/Circuit eligiblepositives beforeineligible
noeffect andfullspecificgesture/tap/Listen/shelf/Audition histories proposed.
All105pins/99oldfiles/twoasofproviders/113watchpaths exact;15negativefixtures/
inlineimage-listparser/refusedwriter pass. No owneradoption inthisaudit; bounded
ownerR4authoring separately. No imagepixels/destination/DSP/runtimeproof.


[Filter/EQ ownerR4](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/filter-eq-owner-r4-review.json)
passed separate independent partial review:65IDs/140cases,128old exact; twelve
new compound control/positive histories have null documentary and actual pairs.
NinetyD12/fourhistorical file-onlyDpkg/46U; fullcurrent source/read/delta checks,
110sealedpayloads/99oldfiles/7own105inheritedpins/125outerwatch unchanged.
Seventeen negative fixtures/133links pass; no new DSP/Legacy/detector law.
The source audit above retains its original no-adoption/as-of disposition.

[NativeMIDI ownerR3](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/native-midi-effects-owner-r3-review.json)
passed independent partial review:27IDs/176cases,146old exact/30new all-null U
histories; one008per-ShiftLED append only. Full112selected source texts and all
30new fullrecords/21group subsets/currentoverlay freshly read; earlier235
judgments/27clauses146actions/19resources carried under exact pins. All47payloads/
48packetfiles/60pins/sixasofconsumerpointers verified,16unsafevariants/27BrowserIDs/
58links pass;76outerwatch unchanged. Fixed32trials prove no liveness/proportion;
all-upHold,Alt,LatchOffrelease,Rangeupper,Scale13×13 andVelocitydisplacement U.
First unsealed planned-seal-link failure and preseal mouseclick correction retained.
No archive decode/oldtool/runtime/newnumeric/protocol law or completeprofile.

[CommonDevicesR4 review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r4-review.json)
requires only historical/current ledger clarification:20remaining_U fields copy
source-audit no-adoption without AS-OF qualification despite current10IDs/20cases.
FrozenR4 preserved; metadata-only R5 authoring preserves38contracts/101cases and
allguards/sourceclaims/oracles, no current38/101semantic approval yet.


[CommonDevices/Racks R5 focused review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r5-review.json)
approves partial38IDs/101cases and resolves COMMON-R4-REVIEW-001: all20copied
no-adoption sentences now explicitly AS-OF SOURCE AUDIT, current10IDs/20cases
adoption and currentunknown outcomes separate. AllR4contracts/caseobjects/guards/
sourceclaims/oracles unchanged;67priorfiles/74sealpayloads/exact75tree preserved.
Five focused rejection fixtures/110links/126outerwatch unchanged; no replay.
Current3installedfile-only/86D12/12U, all101actualnullU/unexecuted; sevennewUI
pairs/thirteennullpairs unchanged. No wholeprofile/target completion.

[Dynamics full five-section source audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/dynamics-source-audit-review.json)
passed independent partial source review:123whole contexts,38literalresources,
62clauses/129actualactions/sevenfixturedefinitions read. Twenty audit-only groups/
fourquestions;0adoption/newcredit.32pins/26oldpayloads/seal,105clause+105action+
129reverse pointers verified;19negativefixtures/parser/11links pass,40outerwatch
unchanged.47oldD12/5historicalfile-onlyDpkg/77U exact; N01/N02ratefixture U.
Glueoversampling MAY>0 exception, independent productive main/detector/Listen,
Limiter BOTHLinkpairpositive and Amount0notgain/crossoveridentity retained.
BoundedownerR2authoring separately; no olddecode/installed/runtime evidence.


[Dynamics ownerR2](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/dynamics-owner-r2-review.json)
passed independent partial review:62unchanged requirement bodies/153cases,129old
objects/27oldfiles exact;24newdocactualnullU histories. Current47D12/5historical
file-onlyDpkg/101U;148applicationcases ungraded,153actualoverlaynullU/unexecuted.
Root freshly read123primarytexts/all24newfullfields/20groups/overlay/fourquestions/
175linechecker/entirecanonicaldiff/originalreview/sevenfixturedefinitions;
old62/129/38resource semanticreviews carried under exactpins, notclaimedfresh.
All38payloads/exact39recursivefiles/41pins/15asofconsumerpointers/fivefiles verified;
18negativefixtures/62BrowserIDs/60links/55outerwatch unchanged, write refused.
N01/N02/targetDSP/lifecycle open, no numericlaw or newgroup/profile completion.

[Sample-instrument fullsource audit freeze](../../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments-source-audit/README.md)
awaits separate independent review:309whole contexts/33audit-only proposals/six
questions/104literalresources,61clauses88actions unchanged. Known captureUTC
2026-10-19T20:27:58.247940+00:00 remains distinct from audioeffectdate-onlysource.
Currentmanifest595a14d9fcc40a1d14ec4bff87c53dc3fb180c81d4fedc4659ca8d811cdace99,
no owneradoption/credit. Delay/Reverb207-block andDistortion216-block source-only
reconciliation continue; these currentassignments live in the soleplan.


[Sample source review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/sample-instruments-source-audit-review.json)
requires two association corrections, preserving all source/owner bytes:
SISA-REVIEW-001 A096/A100 must distinguish generic layer focus/Detune and expected
chooser display from actual Samplechooser invocation; existing G18 invocation
proposal remains. SISA-REVIEW-002 A260/G07 must distinguish Warp-as2bars setup
from actual÷2/reset/×2 actions; sourcebutton invocation remains unexercised/U
or gains an explicit bounded proposed action. No oldowner contradiction or
normative/oracle change. Full309source/309wholejudgments/33proposals6questions/
104literalresources/61bodies88fullfields/fixtures/reviews independently read;
239clause+155action+88reverse pointers checked.28negativefixtures/parser/68pins/
35R2+28R1payloads checked,78outerwatch unchanged/write refused. Mechanicalpass
is not semanticapproval; minimal additive R2 authoring before further adoption.

Delay/Reverb207-block source audit is frozen under separate independentreview;
Distortion216-block and Modulation332-block source-only audits authoring. Root
fullDelay207primaryread and partialassessmentread are preparation only, no new
specification/credit. Existing published releases and allactualoutcomes unchanged.


[Sample source R2 focused review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/sample-instruments-source-audit-r2-review.json)
approved the minimal 18 literal field changes (six plan/twelve audit), resolving
SISA-REVIEW-001/002 while preserving all six original audit files,309source
contexts/33groups/sixquestions/61ownerclauses88cases. Chooser display and Warp-as
setup remain distinct from actual invocation. Effective R2 seal63398b63d563cd5ace3b19be25dd0a2ecc3a8898a7830a452524f268c4852b87;
83outerwatched paths unchanged, six focused unsafe variants rejected. Earlier
full R1 semantic review scope is carried separately; focused review is not a
renewed complete primary-source audit or behavioral adoption.

[Delay source R2 focused review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/delay-reverb-source-audit-r2-review.json)
approved the one logical field correction in both plan/audit, resolving
DRA-REVIEW-001: actual Filter toggle and control-role inspection are retained,
X/Y drags and Freq/Width slider changes remain unexercised/U. All other206of207
assessments and all92clauses149caseobjects unchanged. Effective R2 seal9e75cb77bf07b6a3260405041a6e3209192dc04bef319cc431a0f1fb62abfc38;
82immutable inputs/tenpacketfiles/threeunsafevariants/93outerwatch verified.
One nonblocking README denominator typo remains qualified by the review, with
no cosmetic rewrite. Prior full R1 review is carried, not claimed freshly read.

[Sample owner R3](../../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/README-r3.md)
is separately frozen pending independent review:63IDs/102cases,65oldfiles61old
objects88oldcases exact, two UI clauses/14actual-entry planned histories in13
partial groups,20groups unadopted. All new documentary pairs and all current
actual pairs null/U/unexecuted. Seal4d6efd98dbc388716997499085450c82cf35193006a7f56a75b626c54c781373,
78payloads/79recursivefiles; twelveunsafevariants and95read-onlywatch passed.
Distortion216/Modulation332source audits are separately frozen under independent
reviews; Synthesis567source reconciliation authoring. No runtime/compatibility,
new release, completed group/profile or fullLive coverage follows from these counts.


[Sample ownerR3 independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/sample-instruments-owner-r3-review.json)
approved the bounded partial successor63IDs/102cases. Reviewer freshly read two
new full clauses/14fullcaseobjects/93distinct cited primaryblocks/13selectedgroups/
all33adoptionrecords/sixquestions/fourcanonicaldiffs; prior full309/61/88semantic
audit carried separately. All65oldfiles78payloads79tree/63IDs/102actualnullU verified,
12unsafevariants/158links/95outerwatch unchanged. No group/profile completion.

[Modulation source audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/modulation-pitch-loop-source-audit-review.json)
passed independent partial review:332wholecontexts/22audit-onlygroups/eightquestions,
106clauses186fullfields/commonrecipe/105literalresources read, two intro links
excluded by exact selected h2intervals.17unsafevariants/parser/106Browser/122pins/
107oldfiles/128outerwatch unchanged. True Blend/DutyCycle/Rate0/Looperbothhalves/
Undo/taps preserved; Hertz/STXFade/order/spectralalias/modernLegacy qualifications U.
Its independent reviewer now authors a separate bounded owner successor.

[Distortion focused sourceR2 review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/distortion-source-audit-r2-review.json)
resolves DSA-REVIEW-001: actual type/Pre/bothpositive setup retained, gain-stage
Frequency operation documented-unexercised/U; analysis/feedback controls separate.
Fourliteralfields only, original6auditfiles89pins83ownerhistory exact; seven
unsafevariants/102outerwatch unchanged. Full216/67/190/48resource scope is carried
from separate fullreview, not a renewed focusedreader fullsemanticclaim. Root
scratch initially compared derived G06 to narrower manualplan fields and failed;
sharedfield projection/literalrestore corrected scratch only before reportwriting,
with no packet/gate edit. Denominator wording ambiguity remains qualified.

[Synthesis full567-block source audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments-source-audit/README.md)
and [External full20-block source audit](../../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware-source-audit/README.md)
are frozen under separate independent reviewers. External rootauthor read all20
sourcecontexts/nineresourceroles/24bodies56fullfields/fixtures/priorreviews, three
audit-only groups/fourquestions,39oldfiles49pins preserved. Seal93c2b5fa898659a77b3ed784426dc0416e13f7a2dc3518bacc0d367e9f1b864d,
fivepayloads+seal;12unsafevariants/parserfixture/57watchpassed/writeguardrefused.
No hardware/plugin/calibration/configuration/ratechange/network/runtime executed.
All source-only oracles U; neither frozen packet grants owner adoption/closure.

+
+[External fullsource review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/external-hardware-source-audit-review.json)
+independently approved as partial20contexts/9resources/24bodies56fullfields/3groups4Qs;
+39oldfiles49pins57outerwatch exact,12jointunsafevariants/parserfixture/50links.
+Root separately froze [bounded ownerR3](../../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/README-r3.md):
+24unchanged requirementobjects/normativesection,56oldcases39oldfiles exact, fournew
+null histories/60actualnullU inthreepartialgroups. Seal07c831ed625580667427d0b13e57e3065dbb23b941f90a0ad1f6cd26b2467721,
+49payloads/50recursivefiles;11unsafevariants/67links59watchpass/writerrefused.
+No calibration/hardware/plugin/configuration/rate change or measured timing was run;
+optional unit workflow remains advice, independent semantic owner review pending.
+
+Modulation ownerR3author self-detected a material postseal reference defect:
+208actual-overlay and22adoption pointers incorrectly prefix /cases/i although the
+case catalog is a top-level list. Preserve original sealed bytes/check report
+(8ba80186176daff3a920f23abd94e24f83273f847ff4a5fe27a18fc172c0d36b).
+The earlier checker mirrored the same prefix and passed; it did not dereference
+those paths. Minimal additive correction is authoring before independent review,
+with actual case-ID dereferencing and joint-prefix/index negative fixtures.
+No case action/oracle/count/body change is reported; do not promote that failed
+navigation freeze to current reviewed owner or behavior evidence.
+

[Modulation ownerR4 independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/modulation-pitch-loop-owner-r4-review.json)
approved as partial106IDs/208cases afterfull22newobjects/148distinct cited primary
texts/22proposals/common+tenrecipes/canonicaldeltas andremaining-scopes read.
All186oldobjects107oldfiles unchanged;126payload127tree/all118R3files retained,
130pins/13consumerptrs6files/152outerwatch exact.230oldpaths independently fail,
230correctedpaths dereference tocaseIDs;8independentref+20substantive fixturespass.
New22docnull/all208actualnullU; no profile/group completion or numericlaw.
Author sealedR3defect andR4presealNameError remain disclosed. Rootreview scratch
had a syntax typo before execution/reportwriting, corrected withoutpacket/gateedit.

[External ownerR3 independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/external-hardware-owner-r3-review.json)
approved as partial24unchanged IDs/60cases; fullfournewobjects/20sourcecontexts/
9literalresources/24contracts/56oldaction projections/fixture/proposals read.
All39oldfiles56oldobjects/normativesection exact;49payload50tree,4sourcepointers/
3grouppointers independentlydereferenced;11negative/67links/expanded69outerwatch
unchanged. Optionalunitguidance remains advice; no hardware/config/timing result.

[Synthesis sourceR2 focused review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synthesis-instruments-source-audit-r2-review.json)
resolvesSIA-REVIEW-001 through25literalfields:6manual8forward8reverse1membership2
dispositioncounts. OperatorFilterDrive/Morph table rows nowOP015/G25, actualsnaps/
eligibilityinspection distinct fromunexercisedDrive/continuousMorph; trueOP017
ShaperDrive/wet100to0 remains elsewhere. Rootfreshread current113linechecker,
all25fields/sevenprimarytexts/fourcompleteOPclauses+cases/G25/commonpositive
context; full567/112/109/154review carried separately. Original6auditfiles88pins/
81ownerhistory exact; independentrestore/allforwardreverse/37groupmaps/raw7spans,
11negative/101outerwatch unchanged/refusalpass. No adoption fromroutingcounts.
Bounded synthesis owner authoring active; DelayownerR3 frozen93/176pendingreview,
Distortionowner authoring, Legacy114predecessor sourceaudit authoring. Source
read/grade counts remain distinct from allactualunknowns/fullLivecoverage.


[Delay/Reverb ownerR3 independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/delay-reverb-owner-r3-review.json)
approved bounded partial93IDs/176cases,92old bodies149oldobjects72oldfiles exact,
27newnullhistories/oneHybridUIclause; all176actualnullU,169appungraded7file-only.
Rootfresh27fullnewfields26proposals/adoptions7Qs59distinctprimarytexts andfixtures;
full207/92/149prior review carried distinctly.60source refs/59rawspans/sectionordinal
confirmed, including identical Shimmer/Tides Damping text;95pins110watch exact,
16unsafe/93BrowserIDs/230links pass; writer refused. No group/family completion.

[Distortion ownerR3 independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/distortion-owner-r3-review.json)
approved bounded partial67unchanged IDs/200cases,190old objects83oldfiles exact,
tennewnullhistories/all200actualnullU. Reviewerfresh10newfullcases/adoptions/
proposals31directprimary+35neighborcontexts13actualclauses26oldfullcases/fixture/
sixquestions; full216/67/190priorreview explicitly carried.31rawspans/4sourceR2
fields/210actualptrs/103pins116watch/30negative+5ownpointerfixtures pass. Actual
Roar gain-stage Frequency is distinct from analysis/feedback; trueErosion003006
preserved. No new numericlaw/adapters or wholedevice closure.

[Legacy source audit independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/legacy-devices-source-audit-review.json)
approved partial source-only114wholecontexts23literalresources16proposals8Qs.
994chapterblocks parsed only for filtering; all77clauses178cases44oldfiles53pins
preserved;295actualcontract/casepointerderefs/114rawspans23tags/16negativefixtures
pass,59rootwatch unchanged. Rootfresh114source-note pairs,16groups8questions,
77bodies125Uactions preparation plus45D11metadata expectedwrapper/evidence equality
and8fullDpkgrecords; historicalscan/decodes carried only, no renewedexecution.
Scratch fullbody equality assertion failed because canonical requirement wraps
D11expected in versionprefix/suffix; literalwrapper equality thenpassed without
packet/gatechanges. All178exacttargetnull;45D11sourcechecks8filechecks125Utarget
remain separate. Bounded Legacy owner nowauthoring, no sourceaudit adoption.
SynthesisownerR3 frozen110/190pending independent review. Automation192 and
Project§5.4–5.10 source audits selected within existing planF04/F07/F09; no newqueue.


[Synthesis ownerR3 independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synthesis-instruments-owner-r3-review.json)
approved bounded partial110IDs/190cases,109old bodies154oldobjects81files exact;
36newnullhistories/oneOP024shell-center-foldUIclause,37partialgroups/G19overlayonly.
Reviewerfresh36fullnewactions37proposals/adoptions350unique selectedtexts361refs,
25oldactions+ME003 andcurrentchecker/deltas/fixtures; full567source review carried
explicitly, no freshall567claim.350rawspans/156historicalptrs/190actualoverlayIDs/
25R2literalfields (19auditfields)/100pins115watch/16negative+5independentfixtures
pass,110BrowserIDs72links/threeasofconsumers,writerrefused. LFO1-onlymacros,
DS003TriggerGatebridge/G12twotype st-to-sdsemitones/G20noInfoView preserved;
OperatorLoop/Meldcounts-unit/contextQs unresolved. All190actualnullU/unexecuted.
Comping§21fullsource audit nowassigned afterreview, no wholeRecording sourceclaim.


[Legacy ownerR2 independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/legacy-devices-owner-r2-review.json)
approves bounded partial77unchanged IDs/194records,178old objects44oldfiles exact,
16newnullhistories/16partialgroups.45D11sourcecontent8historicalfile141targetU
remain separate; all194actualoverlaynullU. Rootfresh16completefields in common+
uniqueequalityprojection/fulladoption/overlay/deltas/checker, carries just-read
114source/23roles77body125Uactions45D11metadata8filechecks underseparatereview.
29source refs28distinctrawspans/16proposal16adoption16fixture actualptrs/6historic
navigationptrs/60pins72watchpass,16unsafe+3independentbadptrs,77IDs190links.
Finite ringingquery correctexistingUclause/conditionaloldSetUpgrade, actualCrisp/
selectors/Width/mix/Drive preserve trueoldgestures. No numeric/default/targetlaw.
An initialprojectiontruncation fullyreread; guessed separateconsumerfile absent,
actualembeddednavigationcensusread, no packet/guard change. No authorcheckfailure.

Project/source-only audit nowfrozen132wholecontexts83literalresources20groups8Qs,
22oldclauses34oldcases6oldfiles preserved;315actualrefs18negative/16internalwatch,
18expandedwatch unchanged/refusalpass,7payloads+seal. Independentreviewpending;
no normativeadoption/atomicclaim. Automation192 andComping38sourceauditwork active.


[Project source independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/project-media-source-audit-review.json)
approves source-only132contexts/83literalresources/22fullrows34fullactions20groups8Qs.
Independent315actualreq-case pointers/132rawspans83tags/18unsafe19watchpass;
7payloads8pins/two necessaryasofproviders exact. No requiredfindings, adoption or
runtime/target/atomic/completioncredit. OriginalPMR01–03 corrections andnondefault
fourmarker fixture preserved. Boundedowner nowauthoring23IDs/53cases planned,
oneaggregate-manager UIclause/19newnullhistories, first-templateG06unadopted.
Counts remain planned untilseal/review; current reviewedowner still22/34.

[Comping source independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/recording-comping-source-audit-review.json)
approves full38chaptercontexts24literalresources12selectedclauses29fullselected
records/13groups6Qs/fiveimmutableexternalexcerpts. OtherRecordingchapters20clauses/
52cases notfreshlyreaudited. Fourselectedartifactcases stayinventoryonly; old26
files33pins intact. Rootfresh38texts24fullres12bodies29fullrecords/38notes13full
proposals/sixQs5excerpts, currentchecker. Independent99assessment+proposalrefs,
29originpointers/38rawspanslinecolumns/24tags/15negative+3ownbadptrs/41watchpass,
write refused. Author137dereferencecensus also includes38source-pointer checks;
root99count deliberately separate. Preseal APIindex tokenassertionfailure and
incidentalshape queries disclosed; no sealedfailure or source/judgmentchange.
BoundedRecordingowner authoring from32/81baseline, no newapprovalyet.

LocalBrowser partition approved forsourceaudit:194selectedtexts95literalresources
coverintro/local4.1–4.6,Placesintro,4.7.6–.8(including9UserLibraryh4),4.8–4.10.
Remaining74service texts65resources inclfiveSpliceh4 stay outsidefreshsemantic
scope.268wholeBrowserparse is filtering/discovery only;6selectedConceptssimilarity
contexts distinct, not fullConcepts. No application/network/service operation.


[Recording ownerR4](../../../analysis/ableton-live-12.4.3/full-spec-v1/recording/README-r4.md)
frozen pending independent review:34requirements/90records,32oldcompleteobjects/
81oldcaseobjects26oldfiles exact; twoqualifiedD12targetU UIroles033LeftArrowmain/
fold and034file-to-take/multisample→sequentialTRACKS, nineallnullhistories.
Fourhistoricalartifact-only/86appungraded; all90actualnullU/unexecuted.13groups
partial:9casegroups/G05G11positiveoverlaysonly/G12colorQ031G13APIunadopted.
Rootfresh38source24fullresources12selectedclauses29oldfullfields/13proposals/
38notes6Qs5excerpts andnewcase readback, other20clauses52cases unchangedscope
carried. Rawline/spanmetadata forold32explicitlyR3asof; exactcurrentbodydelta.
36payload37tree41pins,29consumerrows26files36literaloccurrences verifiedasofonly;
14unsafe34BrowserIDs72links54watch/refusal--write/--seal pass, no authorcheckfailure.
No oldtool/parser/inventory/decode/replay/adapter/original/runtime/candidate.
Automation192source audit frozen5payload+seal398217a4…08fca pendingrootreview;
localBrowser194source andProjectowner (23/53planned) authoring. Notcomplete.


[Recording owner R4 independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/recording-comping-owner-r4-review.json)
approves bounded partial34requirements/90records,32oldbodies81oldobjects26files
preserved, twoUIroles/nineallnullhistories. Reviewer fresh38Compingtexts24resources,
12oldselectedclauses29fulloldrecords, twofullnewclauses/ninefullhistories/13groups;
other20clauses52cases carried, not a fresh full Recording audit. Independent
38rawspans24tags/90actualnullrows/36payloads/77watch unchanged;14currentnegative
plus6independent fixtures. Four artifact-only cases remain distinct;86application
outcomes ungraded. Review SHA61cf31b6d08bd74e8d2ab82687651485b911f5a53ac577353f2c3d7b12266378.

[Automation source audit independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/automation-workflows-source-audit-review.json)
approves bounded source-only192wholecontexts154literalroles/62clauses76fullcases,
19proposals/fivequestions, no adoption. Root freshall192notes/texts62bodies76casefields,
154URL/alt/label/caption roles; responsiveattributes mechanical only. Fourteen
adjacent predicates/actions fresh; remaining metadata and13historical authorities/
26releasedpayloads carried by exact identity/asof resolution. Independent361actual
assessment-contract/case refs192rawspans154tags/62pins70watch unchanged;16current
unsafe plus4independent pointer fixtures; write refused. No target/runtime/DSP/
atomic completion credit. Review7479B SHAa4cefa4400dd4fa67e0de235e994f766cdb9bb25ebb073fb8f9edd2e24774bb8.

Project ownerR2 frozen23IDs/53cases pending separate review; localBrowser194source
already in flight finishes only its source audit. Root reread the concurrent
plan revision3 vertical-slice decision: no new breadth owner/sourceaudit opens.
D-01 Corpus read-only preflight/D-02 released-case census selected; D-03 Utility
static feasibility next. No original execution/provider started, candidate built
or scope reduced. Earlier log statements about T1.6pending/design8 retain their
asof meaning; the later decision and current plan govern. Shared routing updated.


[Project ownerR2 independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/project-media-owner-r2-review.json)
approves partial23requirements/53cases:22oldclauses34oldrows preserved, oneUI
aggregate-manager role/nineteennewnullhistories. Reviewerfresh132sourcecontexts/
83literalroles, alloldrows/newhistories/PMR01–03/fourmarkerfixture; source-audit
judgments carried explicitly. Independent102source/20proposal/5newclause refs/
23consumer pointers,40watch unchanged; current15negative/23BrowserIDs31links.
All53actualnullU; G06unadopted/G08availability/G19sharedsampleonlyqueries. Review
24114B SHAd5d1927d60f0119f079c7ed4ee29019ce54acd9b90d77e1083127bf18b6f1f84.


[Independent Browser source review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/browser-source-audit-review.json)
approves only the selected local partition:194 primary contexts plus six
Sound Similarity secondary contexts,95 literal roles,42 selected clauses and
56 full selected cases. The reviewer freshly read23 proposals/eight questions/
12 neighbors. The74 service contexts/65 resources, pixels, destinations and full
native index appendices remain outside semantic scope. No owner adoption,
new normative ID, target outcome, protocol closure or complete family follows.

Current16 rejection fixtures/parser check pass. Independent194 raw spans/six
secondary source associations/95 starttags,693 source-owner-case references and
12 external providers pass;80 watched paths unchanged and write refused. The
reviewer corrected a scratch KeyError caused by the compact secondary records'
metadata shape, without changing a packet or source. Review10,678bytes, SHA-256
`8e670f8aa230f12784d442ca7e29a7fb067718343b8603b09a473a4051d8ec6f`.
Seal remains `a3bb24c7b87c19f92633452342a1db4536074759eae25cd5368603c25d2b0c18`.
Browser Content041 navigation and Project Media023 aggregate-management delegation
remain separate; original positive search/preview/indexing cases are preserved.

No further Browser owner or whole-chapter breadth opens under plan revision3.
Shared plan, indexes, coverage, Q050 and session routing updated. Corpus A1,
Corpus retained-modal diagnostics and Utility static trace/review continue in
parallel. No original application/functions/providers or candidate execute.
