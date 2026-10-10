---
id: RESEARCH-BROWSER-DESIGN
type: research
status: current
updated: 2026-10-09
access: analysis
---

# Living artifact browser: design and execution

The browser is the reader's stable entry point while analysis proceeds. The
existing `browse/index.html#python` address remains valid. Its Python listings
continue to mean bytecode disassembly; native pseudocode has its own section.
The [artifact catalog](index.md) owns the coverage explanation.

## Design

Regenerate the existing offline page after retained evidence changes. Add links
to the learning route, method guide, program atlas and execution ledger now.
Read the native exporter's `coverage.json` when present; show its distinct
pending, exported, warning, failed, external and unclassified states. Absence of
an inventory means no frozen inventory is available, not zero discovered
functions. A retained analysis request can be described as a request, never as
proof that a process is currently running.

Keep pseudocode in its original immutable revision directory. Build a compact
metadata index and display at most 100 functions per page, searchable by address,
alias and status. Link each selected revision's code, metadata and retained
evidence. The selected revision agrees with the ledger's aggregate state; it
is not necessarily the chronologically newest attempt. For excluded or
unclassified functions, preserve the inventory classification while exposing
any retained attempt and its metadata. Failed partial output
must remain labeled failed. Link the full ledger for all revision identities.

The generator reads artifacts and writes derived browser views, using the
exporter's `.ingest.lock` to serialize the entire build and manifest publication
with corpus updates. This prevents a page rendered from one ledger revision
from acquiring a manifest digest for a later ledger revision. It does
not invoke a decompiler, launch the target, approve evidence, or infer behavior.
An exporter integrity check precedes corpus ingestion/publication; browser
generation provides navigation validation, not a second integrity authority.
All recovered names render as text. Offline operation uses a local JavaScript
metadata file rather than fetch, so no local web server is required. Main-page
metadata grows with inventory size, while rendered rows are bounded and code
bytes are never embedded. A no-JavaScript reader can use the raw JSON ledger.

## Execution plan

1. Preserve existing anchors, links and Push2 extracts; add learning navigation.
2. Build optional native coverage projection and bounded searchable table.
3. Test absent inventory, real exporter fixtures, partial failures, escaping,
   pagination and provenance links without invoking native tools.
4. Regenerate current artifacts; verify local links and retained input hashes.
5. Attempt a bounded installed-browser interaction check; report unavailable
   execution distinctly from a pass. Submit the change for independent review.

## Current validation

Implemented in [the generator](../../../tools/build_artifact_browser.py) and
[native projection helper](../../../tools/native_browser.py). Ten focused
[tests](../../../tools/tests/test_native_browser.py) pass. They exercise the real
exporter schema, pending and warning states, failed partial output, classified
functions with failed attempts, missing successful code, escaping, inconsistent
summary rejection, publication locking, qualified address spaces, and the shipped pagination/filter
JavaScript under a DOM stub. The stub establishes logic behavior, not browser rendering.

The initial no-corpus browser snapshot passed 51 local links/anchors and 26
manifest input/output digest checks. `#python` is preserved. An installed Chrome
headless attempt reached its 20-second deadline; no visual or browser interaction
pass is claimed. Its [bounded attempt record](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/browser-headless-check.json)
is retained. Independent scope review passed after fixing classification versus
attempt-state handling and unsupported success claims. Independent
[quality review](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/browser-quality-review.json)
approved the initial change and reran all nine tests after the publication-lock
fix. The [author validation record](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/browser-author-check.json)
pins the code and records static checks and remaining browser limitations.

A subsequent address-space amendment shares the exporter's canonical address
parser, preserving `EXTERNAL:0x1` separately from default-space `0x1`. Browser
links percent-encode the literal address directory without decoding encoded
space names; synthetic tests also cover an encoded slash in a space name. This
amendment has ten passing tests, pinned in the
[amendment validation record](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/browser-author-check-v2.json);
independent [scope](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/address-space-scope-review-v1.json)
and [quality](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/address-space-quality-review-v1.json)
re-review passed. The combined tooling suite has 31 passing tests.

See the [execution ledger](../native-phase-execution.md) for analysis progress
and the generated browser for its last retained snapshot. Rebuild after each
published corpus batch or learning-navigation change; open browsers need a
refresh. The HTML is an offline snapshot, not a continuously updating service.

## Selected-entry capture amendment

Add a separate selected-entry shelf for `native-live-arm64-targeted-v*` captures.
These custom Ghidra script outputs use a no-auto-analysis profile and are neither
REA evidence records nor the default-profile inventory. Never merge their
counts into the whole-corpus ledger. The shelf identifies the run and profile,
then exposes searchable names/addresses, pseudocode, assembly and metadata.

Before publishing function links, verify the sealed manifest's file set and
every digest, require `cleanup.cleaned` with no survivors, and reconcile target,
profile, method hash, seeds and per-function outcomes. Unsealed captures remain
visible as unpublished; corrupt or inconsistent captures show a validation
failure without publishing their code. Sealed failed/missing outcomes stay
visible and cannot count as successful decompilations. Any retained partial
code is explicitly marked failed. Successful entries require nonempty code,
assembly and body evidence. Render all recovered labels as escaped text.

Implementation sequence: add a read-only projection; exercise valid, failed,
unsealed, corrupted and unsafe-path fixtures; regenerate against the actual
sealed capture; verify artifact links, manifest hashes and unchanged `#python`;
submit scope and quality review.

Implemented by [the selected-capture projection](../../../tools/selected_browser.py)
and the existing generator. Three sealed captures currently render: run 1 has
one successful outcome; run 2 has thirteen successful and six failed outcomes;
run 3 has three successful and one failed outcome.
See their [run 1 outcomes](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/run-status.json)
and [run 2 outcomes](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/run-status.json),
plus [run 3 outcomes](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/run-status.json)
for the retained evidence. Failed wrapper assembly remains accessible with its
failure label; no failed attempt is counted as successful pseudocode.

Twenty browser tests pass, including ten new
[selected-capture tests](../../../tools/tests/test_selected_browser.py). These
cover valid links, payload tampering, unlisted files, unsealed/unclean captures,
partial failed code, missing/invalid attempts, identity mismatch, unsafe paths,
payload and manifest symlinks, missing successful body/code and the shipped
search JavaScript under a DOM stub. The
[selected-browser validation record](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/browser-selected-author-check-v2.json)
pins this revision and verifies 129 local links, 166 manifest input/output
digests and 24 selected outcome rows, seven explicitly failed. The browser
validates retained cleanup records; it does not inspect current process state.
Independent [scope review](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/browser-selected-scope-review-v1.json)
and [quality review](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/browser-selected-quality-review-v1.json)
passed on the pinned code/view revision. No new visual-browser pass is claimed.

## Linker-declared starts amendment

Add an optional navigation card for the sealed `derived/function-starts-v1`
capture after its schema is established. Validate the complete manifest and
payload hashes, pinned target identity and captured method identity before
publishing its declared count and direct TSV, summary and provenance links.
Malformed, incomplete or unsealed captures do not publish result links. Do not
embed the large address list in the page.

Linker-declared starts are a separate evidence category: they are not an
analyzer-discovered inventory, recovered bodies or decompiled code. Their count
does not become an export-coverage denominator. Preserve the selected-entry and
default-profile sections and the `#python` address.

Plan: adopt the exporter author's sealed schema; add the smallest read-only
projection and card; test valid, absent, tampered and identity-mismatch captures;
regenerate against retained output and verify links/digests; submit scope and
quality review. This amendment performs no native analysis.

Implemented in [the read-only projection](../../../tools/function_starts_browser.py)
and existing generator. The retained
[capture summary](../../../analysis/ableton-live-12.4.3/derived/function-starts-v1/summary.json)
reports 413,794 declared starts. Publication checks the exact payload set,
manifest sizes and hashes, pinned target, captured method digest, TSV columns,
strict address ordering, row count and first/last entries. TSV rows are streamed
for validation and remain outside the generated HTML.

All 26 browser tests pass, including six new
[declared-starts projection tests](../../../tools/tests/test_function_starts_browser.py)
for valid links/counts, absent metadata, optional missing capture, tampering,
identity/count mismatch and symlink rejection. The
[author validation record](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/browser-function-starts-author-check-v1.json)
pins the code and checks 134 browser links and 170 input/output hashes; all 24
selected outcomes and `#python` remain available. No browser or native process
was launched for this amendment. Independent
[scope review](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/browser-function-starts-scope-review-v1.json)
and [quality review](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/browser-function-starts-quality-review-v1.json)
passed on the pinned production code and generated view.
