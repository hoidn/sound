# Warp markers: corrected bounded family route map — v2

Authored 2026-10-20 20:58 UTC; pending independent structure review.
Successor to frozen v1, manifest SHA256
`24c3706394b0024ac5c1d8d9b680e8d6f5c72f392ffc0b47c79dd9206813ee8b`.
The [v1 correction-required review](../reviews/family-warp-routes-v1-review.json)
identified WARP-ROUTE-REVIEW-001; v1 remains wholly preserved.
The 80 predicates, 39 case identities, routes, finite input sets and scope
records are inherited unchanged; this successor corrects selected q setup provenance. Owner:
[SPEC-WARP-MARKERS revision 5](../../../../wiki/specs/warp-markers.md),
requirements 001–016 and 39 draft case IDs. The current
[warp-markers-v2 release](../../../../handoff/warp-markers-v2/manifest.json)
remains partial and unchanged. This packet changes no normative clause, case,
release, grade or expectation and selects no execution.

## Integration context and method

The cut inherits approved integration packet 1b, manifest SHA256
`7dddd59650ca3395d10e1b3c8aded3cda01d66b522dda4973a08f32e7bfb8f83`,
and [its independent review](../reviews/integration-structure-v1-review.json).
I-04 supplies launch preparation/activation context and I-06 supplies audio
parameter/marker serialization. The approved
[playback map](../family-playback-routes-v1/structure.md), manifest SHA256
`d69a45b394e6f1143a0efbaee61634aa5330ece0e1afe6c3d87a61d2304dc981`,
and [review](../reviews/family-playback-routes-v1-review.json) preserve the
missing parameter→active voice→chunk/kernel→pre-device output joins. I-01/I-02
and I-10 qualify loading, error handling and save/reopen; a stored marker list
does not identify the active playback table or a successful later save.

The inherited component layer uses symbol clusters, qualified aliases,
constructor/vtable and RTTI/type-name evidence. Packet 1a has 25,071 exported
resolved-reference sites of 268,015, separately 21,685 function-target sites
and 24 conditional class-slot additions (combined inventory 25,095). None is
Warp coverage. This map adds zero resolutions; a conditional OSend receiver
proof cannot transfer to clip/helper/voice receivers.

No new traversal was performed. The integration transport neighborhood used
three depths, top 1,000 incoming-row hubs pruned except explicit seeds, caps of
80 nodes/200 accepted edges per direction/level, and retained 121 considered
unknown-site associations. Its terminal 24 forward/19 backward nodes were not
exhaustively expanded. Zero intersections do not prove no route. Source/index
references, conditional dispatch and semantic donor associations remain distinct.
No original instruction, provider, decoder, harness, candidate, new binary read
or tooling installation ran. Only retained source/index material and stdlib
documentary integrity checks were used.

## Predicate inventory and protected scope

[route-ledger.json](route-ledger.json) enumerates 80 required predicates:
5 X routes, 50 S routes and 25 without an established route. These are bounded
route inventory counts, not grades, coverage percentages or a frozen product
denominator. All 16 owner requirements and 78 parent clauses have exact source
spans or explicit auxiliary dispositions; the 39 case identities remain separate.
Twenty-one auxiliary records preserve shipped counts, inferred names/units,
corrections and repeated mapping/grid/edit references without counting them twice.
[scope-gaps.json](scope-gaps.json) keeps 12 excluded/unresolved contexts explicit.

X means a required calculation has a retained original-function route for supplied
inputs. S means a source-supported static/conditional predicate, with its premises.
No-established-route means the stated observable lacks a complete established
route in this packet under ADR 0003; future static recovery is not ruled out.
All current U and inference-only labels remain intact. Helpers and numeric case
instances are not added as required outcomes.

The shadow-append seconds formula is auxiliary research only: revision 5 removed
it from release-ready requirements because its caller arguments and triggering
user operation remain untraced. It supplies no counted X outcome or behavior
batch. WMK-019 uses M0 and was computed from the confirmed rule; the historical
conversion run used M1/M2 only. Public wrappers, frame scaling, scripting dispatch
and opening were not executed. Current 32 gradable/7 unresolved dispositions are
unchanged: WMK-006 is refusal only, WMK-025–027 opening only. REQ-009 has no case,
requires playback acceptance and remains unreleased. The current 63-case partial
release's withdrawn sample-part/device placement remains withdrawn (RVW2-01).

## State, data ownership and call-chain cut

[source-map.json](source-map.json) retains 16 evidence groups, 53 selected source
records and eight exact source associations. Retained JSONL rows carry original
chunk/offset/hash and code identity; D7 records reference the unchanged `.c` and
dossier `.json` paths. No code or spec snapshot is copied. C-line locators are
source-string positions, not native instruction PCs. Semantic names, scratch
vtable reads and Engine donor equivalence retain their original qualifications.

| Boundary | Exact retained route/state | Classification and missing join |
| --- | --- | --- |
| Stored fields → read objects | S8 registration `0x10260fdd8`: marker seconds `+0x50`, beats `+0x58`; AudioClip marker holder `+0x658`; `0x1026105ec` initializes positions to DBL_MAX | Observed-static field/schema relationships. Double text dispatch inferred from schema/getters. Marker IDs inherit conditional shared list-loader A5; no unconditional malformed-ID refusal. Missing IDs/preservation remain U. |
| Completion and empty checks | `0x1027c1c7c` tests AudioClip marker array and reaches `0x101488e64 → 0x10148229c`; `0x10288538c` has no equivalent sample-part empty check | Static A1 Set-load gate is settled. A2 completion/onset/indirect/automatic-warp effects remain conditional. Empty/single/malformed/sentinel lists must not be conflated; public catch and remaining loaded state unknown. |
| Public frame API → clip method | D7 `0x1033bf160` C25 calls current virtual `+0x4b8` after audio/warped tests and division by rate; inverse `0x1033bf250` C23 calls `+0x4c0` then multiplies rate | Observed-static expressions; named scripting role and slot association carried from D7/X2. Actual clip receiver, sample reference/rate and runtime public dispatch remain premises, not X. |
| Clip → helper/cache | `0x1027beb9c` C5 obtains helper at clip `+0x5b0`, current virtual `+0x198`; C7 calls extrapolating wrapper `0x102248700` | Static local source route, with scratch-vtable and ABI premises. This is not a live same-object trace. Clamping alternative `w1=0` is not this scripting path. |
| Lazy cache → ordered table | `0x1028939a4` reads/writes helper `+0x28`, C19 calls `0x10277b71c` when absent; builder calls `0x101b39d74` for BeatTime array and `0x101b39d80` for SecTime array | Observed-static build-on-first-use. Runtime table identity/rebuild/reindex after edits unknown (A3). Harness arrays reproduce layout directly; they do not exercise actual allocation/cache lifecycle. |
| Table → conversion cores | x86 `0x101b6fa60/0x101b6f970`, ARM `0x101b39e20/0x101b39d8c`: upper-bound segment selection and two fused interpolation steps | X for M1/M2 supplied tables, static for wrappers/rate scaling. Both slices fuse equivalent operations; glibc fma substitution and slice inference retained. n=1, equal coordinates and unsorted maps remain U. No physical playback is established. |
| Marker list → shadow/edit identity | `0x1026102c0` treats last list element as shadow; edit paths `0x1033bf42c/0x1033bfa68/0x1033bfb94` exclude it | Static source. Shadow creation/replacement beat rule is conditional on an unknown trigger. Sampler shadow role, unusual-spacing replacement after edit/save, and append operand meanings remain U. |
| API add → bounds/grid → mutation | `0x1033bf42c` class/warped/sample range, insertion position, original neighbor beat checks, q then inclusive bounds; `0x1027afd40` returns bounds; `0x1027baad8` insertion and `0x1027c6eec` deletion have no-op paths | Checks/comparison order static, bounds arithmetic X. Sample length source `0x1027b6954` and its seconds interpretation remain assumed. Weak lookup/pseudocode/insertion-callee qualifications retained. Accepted status does not establish the resulting general list. |
| Marker setter → held beat | x86 `0x102736ce0`, ARM `0x1026101b4`; SecTime setter `0x1026101a0` leaves seconds unrounded | q arithmetic X on original marker objects with historical registry subset/partial initialization; no notification interception is established. Loaded BeatTime bypasses setter and is unrounded. Exact binary64 sequence governs ties/zero/sentinels; no post-edit reconstruction inference. |
| Stored state → defaults/modes | `0x1027b0e40`, sample constructor `0x102883578`, preference map `0x1026a9ec4`, creator `0x1015743b0 → 0x101568960` | Static creation. Absent loaded WarpMode/preference factory remains U. TransientEnvelope initial 100 is stored without clamp despite remoteable maximum 1; effective range U. Stored code names are not proven display labels. |
| Marker cores → playback | T13 named Engine warper functions matched to x86 `0x10235d1c0/0x10235bff0/0x10235b6f0`; 23 caller counts in each Live slice | Static conversion-step relation only. ARM callers not individually matched. Actual voice/sample/chunk, time map, mode algorithm/read positions/preload/rounding and feedback versus audio remain unknown. ARM StartFileSmpl is position calculation, not proved voice activation. |
| Held list/settings → saved file | Generic serializer/member writer through integration I-10 | A4 no intervening mutation/autowarp/analysis and actual Save receiver remain unproved. Saved order/value source rules do not establish full file durability/reopen. |

## Premises, malformed inputs and finite candidates

A1 is settled static Set-load gating. A2 qualifies held state immediately after
opening; two onset helpers and five completion indirect calls were untraced.
A3 qualifies first-use conversion-table binding and preserves post-edit rebuild
as unknown. A4 qualifies every saved comparison. They are distinct boundaries.
Unit origins of SecTime/BeatTime remain inferred; public conversion takes sample
frames, divides/multiplies the actual rate statically, and does not use song tempo.

Unordered/inverted/equal-time/single-marker lists, missing/Invalid positions,
missing/duplicate IDs, nonfinite fields and out-of-range settings retain their
stated conditional or excluded scopes. A selected unchecked load is not a safe
post-load/display/save result. q's explicitly stated special-input arithmetic
does not broaden document acceptance. Mode-specific audio, post-read automatic
changes, clip region semantics, interactive edits, move limits and older formats
remain outside or U exactly as the owner states.

[candidate-batches.json](candidate-batches.json) nominates three finite sets:
12 M1/M2 conversion result values, four neighbor-bound results, and 18 q inputs.
These 34 result rows refer to four exact retained command rows; rows are not
original call counts or required outcomes. Inverse displayed frame results
include static driver scaling; original cores return seconds. The bounds raw row
also has four Bezier-monotonicity calls, explicitly auxiliary and excluded from
this family nomination. WMK-019's M0 vector remains separately enumerable,
computed rather than historically executed.

Conversion tables and bounds use recorded owned buffers. q's retained run built
original AWarpMarker objects after a class-registry subset and partial static
initialization. The selected `beat-grid-q` receipt and driver establish no
debugger interception: notification execution or absence was not independently
traced. A future replay of that construction remains
outside standing self-contained-call scope and requires preparation/peer review.
Old successful setup confers no blanket permission. Future batches must freeze
slice/harness/inputs/stubs/timeout/results and use the current allowed call model.
The original driver, sequence helper and loader source are pinned, not run here.

The selected raw row 17 has no `gdb_script` field and no HIT rows.
`run_x2.py` lines 187–199 select `run('beat-grid-q', s)`; lines 96–99 call
`s.run()`. `Seq.run` at `seq.py` lines 69–70 delegates to
`R.run(self.tokens)`. The separately defined `run_skip` facility (lines 73–93)
is unused by this selected driver. Its existence supplies no evidence of a
notification skip. Historical canonical prose claiming a gdb skip is retained
as history and superseded by the additive correction.

Initialization is partial: the historical manifest reports 295 of 3,322
initializers reaching trap/fault and being abandoned; selected raw row 17 has
294 `initfail` rows. Those distinct retained counts are not reconciled into a
claim of full successful initialization. Setup, notification side effects and
application binding remain qualified; the returned arithmetic results do not
resolve them.

## Integrity and review gate

The small `author-check.py` validates all owner spans/parent dispositions, case
identities, source rows/C-line associations, selected pins/predecessor payloads,
finite result pointers, raw command identities, selected direct-run method and
partial-initialization assertions, and the protected canonical
research prefix including the v1 pending section. Unchanged ledger/batch/scope
bytes are checked against the v1 manifest pins; their contents are not re-derived.
Negative controls reject bad digests/spans/cases, an omitted
parent clause, duplicate outcomes, unrecognized bases and a helper-only outcome.
Focused link/whitespace checks are recorded separately. These are documentary
checks, not independent semantic review or application/candidate validation.

Root owns the seal, independent review and shared atlas/index/plan/coverage/log
updates. Author files lock after final checks; only a review correction reopens
them. Batch selection follows review. All source/release bytes and owner grades
remain unchanged.
