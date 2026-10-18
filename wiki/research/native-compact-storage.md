---
id: DESIGN-NATIVE-COMPACT-STORAGE
type: research
status: draft
updated: 2026-10-12
access: analysis
---

# Compact native artifacts and continuation plan

**Goal:** continue native source export within measured storage limits while keeping
code readable and prior captures immutable. This is analyst tooling, not the
independent application. Root owns target launches and shared execution status.

**Architecture:** retain new immutable ZIP shards containing exact payload bytes,
with a hashed manifest and explicit member locators. Generate a separate offline
code viewer from verified shards. Existing per-function captures remain intact;
a compact mirror is a storage experiment and does not add decompilation coverage.
Persistent Ghidra checkpoints use their own analysis profile and coverage.

**Tools:** installed Python standard library, existing exporter validator, local
HTML/JavaScript, installed Ghidra 12.1.4 and JDK21. No installation or external
publication is part of this work. Continue using the existing shared analyst
checkout; its pending edits and evidence must be preserved.

## Task 1: Exact compact archives

Create `tools/compact_native_corpus.py` and meaningful tests in
`tools/tests/test_native_compact.py`. Provide `build`, `check` and `extract` commands.
Add a small `coverage(..., persist=False)` option to the existing exporter,
keeping its default behavior unchanged. Use that read-only integrity authority
and source writer lock before archiving a corpus; compare recomputed coverage
with the retained bytes and reject disagreement without correcting the source. Require a fresh destination; reject symlink roots, ancestors,
input payloads and unsafe member paths before any write. Never edit/delete old
payloads, manifests or released handoffs.

Archive every committed revision's original metadata, manifest and any code
payload byte-for-byte, preserving failed states and partial code labels. Also
preserve each authoritative source envelope and run/inventory/coverage files;
store source captures once, separately from bounded function shards. Bind the
archive to exact target, profile, input manifest and inventory identity. Each
member has its original path, size and SHA-256; each ZIP and catalog is hashed.
Zip members must be regular files with canonical relative names. Reject duplicate,
unlisted, missing, tampered, traversal or symlink members on verification.

Commit a complete verified archive using an atomic new-directory publication.
Incomplete staging is explicit and never a published success. `extract` selects
an explicit canonical address/revision, verifies bytes and refuses to overwrite
an existing destination. Test round trips including warning/failure records,
qualified addresses, Unicode, corrupt members/manifests, interrupted publication,
unsafe paths and symlinks. Bound source copying/ZIP streaming and report logical
and allocated sizes separately. Submit scope review then quality review before
root runs a compact mirror of the retained corpus.

## Task 2: Offline code access

After archive review, create a derived viewer builder and reader tests. The reader
opens under local-file URLs and uses generated local script chunks rather than
fetch. Search address/alias/state, paginate, open an exact function, read warnings
and provenance, and download the original code bytes. Keep data out of executable
markup with text rendering and safe JSON serialization. Bind lazy chunks to the
viewer generation; malformed/stale chunks must leave prior navigation usable.
Do not load all code to open the page. Chunk sizes/counts and memory limits are
explicit. Link this viewer from the existing artifact browser, preserve `#python`
and all current native shelves, and describe mirrored counts without double
counting. Run scope then quality review, exact archive/viewer byte comparison,
local-link/hash checks and feasible interaction checks. Report visual checks
separately from DOM-stub tests.

The proposed interface is `tools/build_compact_native_browser.py build --archive
ROOT --output NEW`, with a separate fresh viewer directory rather than files
inside the immutable archive. The first viewer indexes the mirror's committed
addresses and revisions, including failed outcomes; it does not repeat the full
420,472-entry inventory. Display at most 100 address rows, with explicit revision
selection where needed. Load no pseudocode on initial page open. Code chunks
contain at most 100 revisions and at most 512 KiB of serialized data, except a
single larger revision which must be identified and retained without truncation.
Bound loaded chunk retention and allow retry after load errors. Preserve exact
UTF-8 code bytes in downloads, including Unicode and line endings. Verify every
derived code record against its archive member. Expose target/profile, warnings,
source evidence and original member locators beside each opened revision.

Add a link and mirrored-count explanation in `tools/build_artifact_browser.py`;
keep the existing browser's `#python`, `#native`, `#selected-native` and
`#declared-starts` anchors. Missing mirror/viewer must leave the existing browser
build usable. Test invalid/stale chunks, rapid selection while loading, retry,
multiple revisions, code containing markup, and exact download bytes. Generated
script chunks require a frozen generation identity and complete schema checking
before replacing visible state.

## Task 3: Durable native analysis

Implement the separately reviewed [recovery design](native-analysis-recovery.md),
including owned process groups, actual JVM verification/nonce acknowledgment,
no-analysis import, save/close/hash/read-only reopen proof, bounded analysis and
separate-profile exports. Author and test the driver and gate/outcome/export
scripts before target work. Run a tiny synthetic persistence test first. Root
then admits the target baseline from fresh disk/RAM measurements, and decides
whether analysis can begin using the baseline's actual allocated size. Do not
lower the resource reserve based on compression guesses, mistake a saved import
for analyzed code, or repeat a lost full REA analysis without durable outputs.

## Task 4: Evidence and teaching

Measure the compact mirror without deleting its source. Record exact commands,
method hashes, source identity, archive logical/allocated sizes and extraction
agreement. Document why filesystem allocation differs from text length, why
saving observations differs from saving an analyzer database, and how readers
reach code. Update source/research indexes, phase ledger, questions and coverage;
retain failed investigations. Add new code/structure findings only when actual
exports support them. Run wiki lint and final source/hash checks. The first
released MIDI handoff and compatibility statuses remain governed by their own
evidence.

## Status

Archive and offline reader tooling are independently reviewed; the real mirror
and reader publication passed. Durable analysis tooling has a
[current recovery revision](native-analysis-recovery.md#loader-matched-profiles--2026-10-12)
with passing independent scope and quality reviews. After the first language
rejection, the corrected [target import/save](native-analysis-recovery.md#corrected-import-passes-reopen-capacity-stop--2026-10-12)
passes, but its first reopen is stopped before a JVM launch by capacity. No target
checkpoint or new pseudocode is accepted. Tooling, retained evidence and teaching
are delivered for this bounded stage; target recovery remains capacity-blocked.
The first
scope review found a publication-window failure, fixed in author revision 2.
Separate quality review then reproduced a later publication-window failure and
archive/source-authority disagreement. Author revision 3 corrects both; its
[fresh scope review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-scope-review-v3/scope-review.json)
passed with 63 tests and independent publication/authority replays. The separate
[quality rereview](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-quality-review-v2/quality-review.json)
also passed. A minor malformed-identity diagnostic can produce a traceback while
correctly rejecting an archive; it is retained as a limitation. Review of root's
execution wrapper found exception/worker-cleanup gaps, corrected in retained
revision 3 and independently replayed before admission. Offline viewer revision 1
passed 43 synthetic browser tests and independent scope review. Separate quality
review then reproduced malformed profile/identity types
[accepted by the JavaScript reader](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-quality-v1/reader-replay-results.json)
but [rejected by Python](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-quality-v1/schema-python-results.json).
The [sealed failed review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-quality-v1/quality-review.json)
retains all six variants. The same author's
[revision 2](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-author-v2/report.json)
corrects explicit type checks and passes 44 tests, including paired JavaScript/
Python rejection cases. Final scope/quality rereviews passed revision 2.
The first [actual reader execution](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-execution-v1/failed-execution-report.json)
then rejected valid composed-workflow profile metadata: the original evidence
wraps its native profile, while the run uses the export authority's resolved
native profile. The worker closed cleanly and no viewer was published; original
source, archive and prior browser hashes/mtimes were unchanged. The failed
packet is sealed. The same author's
[revision 3](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-author-v3/report.json)
preserves the raw profile, binds the provider to its exact retained source record,
and uses the existing export authority to derive the effective profile. Its
[scope review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-scope-v3/scope-review.json)
passes all 48 browser tests and independent malformed/source-binding cases.
A [read-only projection](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-execution-v2/real-profile-projection.json)
also validates all 2,028 real revisions from 47 referenced source envelopes,
without loading the inventory envelope. Separate quality review then reproduced
a [scalar-type binding gap](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-quality-v3/profile-scalar-type-probe.json):
Python's ordinary profile equality accepts a boolean replaced by the number `1`
against unchanged source data. The same author's
[revision 4](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-author-v4/report.json)
passes 51 browser tests with typed JSON equality: booleans remain distinct from
numbers, objects ignore key order, and equivalent JSON numbers agree. Its final
[scope review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-scope-v4/scope-review.json)
and separate [quality review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-quality-v4/quality-review.json)
pass. The [actual publication](#measured-reader--2026-10-11) then passed from a
fresh destination; the failed packets remain intact.
These fixture findings have not changed the retained
Live corpus. See the retained [scope review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-scope-review-v2/scope-review.json)
and [sealed quality review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-quality-review-v1/quality-review.json),
whose two blockers are not certified by the 55 passing author tests.
The prior
[phase checkpoint](native-phase-execution.md#stratified-checkpoint-and-phase-report--2026-10-10)
retains the initial capacity stop. Fresh capacity is measured for each new gate;
this plan is not proof that full export will fit.

## Read revisions interaction fix — 2026-10-12

**Observed:** clicking “Read revisions” in the original reader loaded the first
function's code, but its panel began about 6,559 pixels below the viewport and
the code began about 9,844 pixels below it. The
[local-file reproduction](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/read-revisions-fix-v1/browser-before-repro.json)
records Chrome, viewport, selected revision and successful hidden code load.
DOM-stub loader success had not established that a person could see the result.

The [current v2 reader](../../analysis/ableton-live-12.4.3/native-compact-view-v2/index.html)
focuses and reveals the selected heading, reserves a viewport of reader height
before asynchronous code arrives, places code before collapsed provenance and
provides a return link. Multiple revisions still require an explicit choice;
warnings, exact code and source metadata remain intact. The main browser now
prefers v2, rejects invalid v2, and considers current-method v1 only when v2 is
absent. Original v1 files remain unchanged; an unsuccessful intermediate layout
candidate is retained in the new repair packet.

The [final browser check](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/read-revisions-fix-v1/browser-verification.json)
passes under Chrome 153.0.8010.53 at 1280 × 900 with a `file:` URL: zero initial
code chunks, one after selection, focused heading at the top, code about 251
pixels down, collapsed provenance and an exact 134-byte Blob download. The
[screenshot](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/read-revisions-fix-v1/browser-verification.png)
was visually inspected. Mouse selection, return navigation and Enter activation
pass. The browser harness required corrected local-file request counting,
one-pixel scroll rounding allowance and a complete Enter event; earlier probe
results are retained rather than represented as product failures.

The [scope review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/read-revisions-scope-v1/scope-review.json)
passes the final builder's 26 scoped tests and independent preservation checks.
Three added regressions were first observed failing. The broader 54-test browser
suite passed before the final CSS height correction, which the scoped rerun and
Chrome check cover. Fresh build and archive verification preserve all 2,028
revisions and exact code hashes; this adds no decompilation coverage. Browser
evidence is one captured interaction, not broad accessibility or cross-browser
certification. Application compatibility and cold analyzer recovery are unchanged.

The [repair packet](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/read-revisions-fix-v1/README.md)
retains commands, candidate/probe failures, earlier derived publications and final
receipts. This new publication supersedes the reader interface, not the original
2026-10-11 evidence or the immutable compact archive.

## Measured reader — 2026-10-11

**Observed:** the [actual execution report](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-execution-v2/report.json)
records successful reader build, independent check and main-browser regeneration
after root verified all 152 final author/scope/quality payload pins. The
[sealed packet](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-execution-v2/manifest-v1.json)
retains admission, commands, resource samples, prior-browser backup and
before/after source/archive records. Original payload and archive bytes/hashes/
modification times remain unchanged. All three monitored workers closed with
no survivors or stop reason.

Open the [offline code reader](../../analysis/ableton-live-12.4.3/native-compact-view-v1/index.html)
to search the same 2,028 retained addresses and select an exact revision. The
[main browser](../../analysis/ableton-live-12.4.3/browse/index.html#compact-native)
links it and retains `#python`, `#native`, `#selected-native` and `#declared-starts`.
The [viewer manifest](../../analysis/ableton-live-12.4.3/native-compact-view-v1/manifest.json)
pins generation `0e8ba9a0374d805a8fa1165a35b66f9643d9c9e0750d6677ee550fa797d5127d`.

| Measurement | Result |
| --- | ---: |
| Reader files / code chunks | 25 / 21 |
| Reader logical / allocated bytes | 11,542,577 / 11,591,680 |
| Build / check / main-browser build seconds | 29.70 / 1.08 / 5.16 |
| Build maximum sampled owned RSS bytes | 1,417,494,528 |
| Main-browser maximum sampled owned RSS bytes | 818,675,712 |

The [structural browser check](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-execution-v2/browser-check.json)
verified 2,239 input/output hashes, 6,223 local links, stable anchors and exact
initial/full inventory agreement. The [executed reader check](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-execution-v2/reader-node-result.json)
opened every actual revision under a Node DOM stub, verified all 3,312,468
downloaded code bytes against their archive hashes, and checked all 312 warning
labels. Initial state has 100 rows and no code requests; code came from 21 lazy
chunks. Fixture tests separately establish retry, stale-load, multiple-revision,
failed and partial outcome cases absent from this real sample.

These are exact-byte, structural and DOM-stub results. Real-browser rendering,
accessibility and local-file script loading remain untested. One-second RSS
samples are not lifetime peaks. The reader adds no decompilation coverage or
application compatibility result; 416,390 eligible entries remain pending.

## Measured mirror — 2026-10-10

**Observed:** the [execution report](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-mirror-v1/report.json)
records successful build, independent check and named extraction against the
retained default-profile corpus. All 6,135 archived members match original
bytes and hashes. Before/after source records also agree on modification times
and allocation. The 2,028 addresses/revisions remain 1,716 unwarned exports and
312 warned exports; 416,390 eligible entries are still pending.

| Representation | Regular files | Logical bytes | Allocated bytes |
| --- | ---: | ---: | ---: |
| Original mirrored payloads, inventory and source envelopes | 6,135 | 447,280,353 | 465,838,080 |
| Compact archive: ten ZIPs, catalog and manifest | 12 | 26,897,538 | 26,927,104 |

The compact representation occupies about 94% less regular-file allocation for
these exact payloads. Directories and filesystem metadata are excluded. Original
captures remain intact, so the experiment **adds** 26.9 MB rather than reclaiming
space. Code payloads still total 3,312,468 bytes; the mirror generates no new code.
Compression of this retained sample is not a whole-corpus capacity forecast.

The [archive manifest](../../analysis/ableton-live-12.4.3/native-compact-mirror-v1/manifest.json)
has SHA-256 `2f3272fa2f1c5fc2fc4b108f41d6799bc202ea5e7510f45709038c217c970364`.
The [sealed execution packet](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-mirror-v1/manifest-v1.json)
has SHA-256 `2dfdf247ca8c649b5ff2d7f454a9eee7dcd84c0f2927fcb0f729cfa1f9a55405`;
its report SHA-256 is `3f4dd1eef89c8b356ea47efe8352a170e166e1376c828ff270f6f19a9e2407d0`.
It retains admission/method pins, all-member comparisons, source before/after
records, command outputs and resource/closure records. Extraction of
`0x1015645a0`, explicit revision
`ev_ea0c2c075b907722383b0a10a3cd27bd9542112b1dda356e7b8f7f91b680d61e-3`,
matched its three original payload hashes.

Build/check/extract took 37.86/28.87/27.63 seconds. Maximum one-second sampled
owned RSS was 1,521,647,616 bytes; this is not an exact lifetime peak. All three
owned Python children exited and were reaped with no stop reason or group
survivors. Fresh free disk after execution was 9,438,433,280 bytes. Global disk
changes may include unrelated applications. Persistent native recovery remains
unknown until its separate save/close/reopen proof succeeds.
