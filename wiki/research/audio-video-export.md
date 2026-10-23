---
id: RESEARCH-AUDIO-VIDEO-EXPORT
type: research
status: current
updated: 2026-10-20
access: analysis
target: Ableton Live 12 Suite 12.4.3; current Live 12 documentation, patch parity unknown
---

# Audio and video export evidence

[Audio/video export](../specs/audio-video-export.md) owns the partial documentary
contract. [Project/media workflows](project-media-workflows.md) owns dependency
collection, Set/Pack management and the canonical source capture:
[Managing Files and Sets HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manual-files-2026-10-19.html),
SHA-256 `04fef126e1085053b790ea43b16596e33e82598ec54449418208e2b5fb9ad3d6`,
with [URL/UTC metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/source.json).
The export packet [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-video-export/manifest.json)
pins that source and the authored contract/scenario inventory. The major-release
manual does not identify an exact patch, so every D12 behavior retains target U.

Selected section 5.1.3 supplies observable option, track/range, encoding/video and
external-device workflow proposals. The contract distinguishes those observations
from backend explanations: the manual's named downsampling library and processing
passes are not candidate architecture requirements. Metadata/UI checks cannot
stand in for resampling, dither, normalization, return processing or tail quality.
A specific documented real-time Cancel deletes its partial file; this does not
establish cancellation atomicity for all exports or deletion-failure behavior.

The author inspected source text only and executed no original/candidate codec,
audio renderer, hardware or UI scenario. The packet has 23 requirements and 34
unexecuted scenarios with quantitative and platform gaps explicit. Next: separate
review of scope, source anchors, fixture preconditions, metadata-versus-audio
comparators and the difference between a supported observable outcome and an
internal processing explanation. [Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
tracks the whole-product applicability boundary. No whole-render or compatibility
claim follows from the existing finite T1 mix expectations.


## T1 audio/video export family route map — 2026-10-20 (pending independent structure review)

The [corrected independent export review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/audio-video-export-review.json) approved the partial23requirement/34scenario owner;earlier pending-review prose above is author-time history. Root selected one [T1 end-scenario structure/route map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-audio-video-export-routes-v1/structure.md),extending approved1a/1b I01/I02/I07/I08/I10–I12 and Playback/Mix/StructureALS/Arrangement context. No active/unreviewed Recording map is a dependency. No owner,case,criterion,release or grade changes.

The [ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/family-audio-video-export-routes-v1/route-ledger.json) enumerates91required application predicates,all no-established-route/U,zeroX andzero required retained-fileS.46D12source annotations reuse those predicate IDs and have no-established-exact-target-route;they are not targetS or extra outcomes.137total context records is not an atomic or whole-product denominator. All23owner rows/34case pointers are preserved. Format/settings/control roles remain separate from exact numeric/encoding/dither/timing/dropout/file-failure predicates. No historical fixture/header/ASD parser route or local mix expectation supplies an observed Live export result.

The [metadata-first census](../../analysis/ableton-live-12.4.3/full-spec-v1/family-audio-video-export-routes-v1/query-census.json) retains32exact table associations/150selected of845available exported-prefix slots,63store candidates,184aliases+35memberships=219,and37boundary seeds→61calls+10unresolved indirect rows. Whole14small writer/encoder/operation/event prefixes contribute102slots;18model/dialog/preference prefixes have only leading3-or-less construction frontier slots/48slots.695slots stay unselected. Large model prefixes are not processing interfaces/fullclasses. BroadAPI/XML/logging/graphics/MIDI/StemSeparation export/writer/capture names are not silently attached. There are0new C bodies/native reads/site credits or original routes;class names,constructor-like stores,OnCancel labels and encoder/dither interfaces prove no actual instance,ABI,input/model/calibration or successful file behavior.

I11's retained token/callback/context association remains conditional:106530bd8→100294f20→guarded10028dfcc,with registry selection/context/fields/nativeABI premises. Stored-function dispatch is not a guessed vtable slot. I07constructed ports and I08local processor/helper outputs do not identify real render buffers or host delivery. I12movie-backend expressions remain an inherited landmark,not a joined audio/video pipeline. Actual loaded/edited song,active clips,range,sample/frame clock,settings,encoder/writer/import identity,Save/publication and lifecycle remain unknown. The [14possible local source frontiers](../../analysis/ableton-live-12.4.3/full-spec-v1/family-audio-video-export-routes-v1/prospective-frontiers.json) select no body or original batch.

[Source scope](../../analysis/ableton-live-12.4.3/full-spec-v1/family-audio-video-export-routes-v1/source-scope.json) keeps six E1–E6export spans separate from the320,889-byte whole ManagingFiles capture. The separate132context source audit covers5.4–5.10 and excludes5.1–5.3/export;it is not an export audit. Export semantics remain inherited from the corrected review;source geometry/hashes are freshly checked. Version12/capture2026-10-19T20:07:46.423249+00:00 is not exact12.4.3applicability. Pixels/destinations remain uninspected.

Preserve productive nonzero pre/post-fader/main/return/tail paths and MFzero-input silence premise;EXP009toggles inclusion while effects stay enabled. Video needs Arrangement video+PCM,andEXP023both encoderclasses or staysunexecuted. Hardware object names do not classify real-time routes. EXP027needs AutoRestart plus an acknowledged/detected-by-Live dropout,not any physicalgap. Specific real-time Cancel/partial-file deletion does not establish general cancellation,crash atomicity or deletion-failure policy. Dither32behavior remainsU outside the documentedsub32condition. Samples/frames/rounding,resampling/mono/normalize/tails,noise/codec/padding,timing/retry/filefailure/Undo/close-replace remain U. Passes/named libraries remain explanations,not implementation architecture.

[Read-only author checks](../../analysis/ableton-live-12.4.3/full-spec-v1/family-audio-video-export-routes-v1/author-check.json) verify clause/case/source/metadata/pin identities and12false-promotion controls. Earlier research bytes are preserved except this date update and additive section. No original/native/source-body/provider/decoder/harness/model/comparator/fixture/build/tool execution or old-helper import occurred. Root owns final seal,independent review and shared atlas/index/log/coverage adoption;this packet selects no successor.


## Audio/video export family route review approval — 2026-10-20

Root read/adopted the complete [independent structure review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-audio-video-export-routes-v1-review.json) (`b444d49048bfd8a03ac21da357e5514d221b574f822d1e26707d18565c7572c3`). Manifest `700023a8434b8fe6b48fc7c7f5f6f3ef5c83d8c1a7593f1856ba7da7b2da3e22` binds14payloads/564,709bytes. All23clauses/91required application predicates/34full actions and comparators were freshly reviewed. All91routes remain unknown/zeroS/zeroX;46mirrored D12annotations add no outcome,137contexts are not an atomic denominator. Nineteen pins/385selected raw rows/six source geometries and12negative controls passed;2,263research-prefix bytes restore exactly after date-only reversal, with4,967append bytes.

Six export-section semantics remain inherited from the corrected export review; the separate132-context ManagingFiles audit explicitly excludes export. Metadata retains32tables/150of845prefixslots/63stores/184aliases plus35memberships/37seeds/61calls and10unresolved indirect rows. Fourteen prospective prefixes/102slot targets select no body or original batch. LFlacEncoder slot+16 target100259a0c has no retained exact alias and function:null; it is executable-section-only metadata, not callable-body or absence proof. Conditional stored callback106530bd8→100294f20→10028dfcc remains unjoined to actual registry context/ABI/current render buffers and encoder/writer completion.

Productive pre/post-fader/effect paths, both encoder classes for EXP023, detected-by-Live dropout for EXP027, sub32-only dither qualification and specific active real-time Cancel limits remain preserved. Actual samples/frames/resampling/encoding/noise/clock/file failures/Undo/teardown and host/public delivery remain unknown. No new body/native/original execution, resolved site, clause/case/release/grade or completed family/product follows. Earlier pending prose is author history.
