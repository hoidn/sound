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
[Media/cache/interchange](../../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/manifest.json)
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
39 blocks. Its18 requirements/28 cases await separate review. Both captures retain
exact URL/UTC metadata; detailed12.4.3 applicability remains unknown.

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
26-requirement/36-case draft that passed independent partial-scope review. Exact12.4.3 Link Audio availability,
wire protocols, detector/numeric/timing laws and all target outcomes remain U.

The [settings/help seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r1.json)
retains First Steps,261023bytes, SHA-256
`59601f2af92f1148b23213edc0471339c9ac1188a401f717e3067d67b55e2746`,
captureUTC2026-10-19T21:59:13.502275+00:00. Its70 blocks support a partial
21-requirement/30-case settings/Learn/Info draft independently reviewed as partial.
Newer feature availability, clip-color preference context Q031, installation,
authorization, update and all exact-target outcomes remain unknown.

The [Warp workflow seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manifest-author-r1.json)
retains Audio Clips, Tempo, and Warping,283979bytes, SHA-256
`295a442252730b7f1bb6154b9cbfe041f09c6d40d45d487a42e793ae8423c2ad`,
captureUTC2026-10-19T21:55:52.320855+00:00. Its131 blocks support50 requirements/
88cases independently reviewed as partial. Q032 retains import-readiness contexts;
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
18-requirement/29-case draft independently reviewed as partial. Feature/model availability, audio,
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

## Use and limitations

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
