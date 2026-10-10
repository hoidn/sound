---
id: DESIGN-NATIVE-COMPACT-STORAGE
type: research
status: draft
updated: 2026-10-10
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

Design drafted; implementation and measured storage savings pending. The first
scope review found a publication-window failure, fixed in author revision 2.
Separate quality review then reproduced a later publication-window failure and
archive/source-authority disagreement. The same author is correcting both before
scope and quality rereview. These fixture findings have not changed the retained
Live corpus. See the retained [scope review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-scope-review-v2/scope-review.json)
and [sealed quality review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-quality-review-v1/quality-review.json),
whose two blockers are not certified by the 55 passing author tests.
The prior
[phase checkpoint](native-phase-execution.md#stratified-checkpoint-and-phase-report--2026-10-10)
retains the initial capacity stop. Fresh capacity is measured for each new gate;
this plan is not proof that full export will fit.
