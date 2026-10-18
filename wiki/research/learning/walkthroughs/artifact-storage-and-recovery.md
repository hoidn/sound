---
id: LESSON-ARTIFACT-STORAGE-RECOVERY
type: research
status: current
updated: 2026-10-12
access: analysis
---

# Why readable code and recoverable analysis need different storage

A decompiled function is text, but preserving an investigation takes more than
that text. Our function directories also record warnings, target/profile identity,
where the answer came from, and checksums. This keeps a readable result tied to
the exact evidence that produced it.

Open the [artifact browser's native section](../../../../analysis/ableton-live-12.4.3/browse/index.html#native),
search an address or alias, then open its pseudocode link. The separate
[selected-function section](../../../../analysis/ableton-live-12.4.3/browse/index.html#selected-native)
includes the [small LoopOn factory walkthrough](first-native-loop-factory.md).
For a first example, search `0x10276e5d4` in that selected-function section,
open its pseudocode, then follow the walkthrough's instruction comparison.
These are reconstructed C-like files, not Ableton's original source repository.

The current [offline code reader](../../../../analysis/ableton-live-12.4.3/native-compact-view-v2/index.html)
lets you search those default-profile exports, select a revision, read its
warnings/provenance and download the exact code bytes. Try `0x1015645a0` for a
short example. Press “Read revisions” to jump to the code; expand provenance
when you want its source identity or archive locations. The
[original publication checks](../../native-compact-storage.md#measured-reader--2026-10-11)
compare all retained downloads to the archive. The later
[interaction repair](../../native-compact-storage.md#read-revisions-interaction-fix--2026-10-12)
also checks one real Chrome local-file interaction. A successful loader test
can still miss an interface problem: the old button loaded code far below the
viewport. Geometry, focus and readable placement need their own observation.

The [current export checkpoint](../../native-phase-execution.md#stratified-checkpoint-and-phase-report--2026-10-10)
retains 2,028 default-profile exports: 1,716 without warnings and 312 with warnings.
Another 416,390 eligible functions are pending. Finding an address in the full
inventory does not mean readable code has been generated for it. The separately
profiled selected functions have their own records and do not increase this count.

## Text length and disk allocation

The [continuation preflight](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/continuation-v1/host-and-storage.json)
measured the existing function payloads using each file's length and allocated
blocks (`st_blocks * 512`). Code alone totals about 3.3 MB. Code, metadata and
checksum-file lengths together sum to about 8.3 MB, while the regular
files occupy about 26.7 MB. This does not count directories, source envelopes,
the full inventory, or unrelated system files. The difference is a property of
how these particular files occupy storage, not extra recovered source code.

For a small function, the metadata and checksum files can each occupy a disk
allocation unit despite containing much less text. Repeating this layout hundreds
of thousands of times makes the file layout itself a capacity issue. Free disk
also changes when other applications, swap or temporary files change; it cannot
be attributed entirely to our export files.

The [compact-storage design](../../native-compact-storage.md) groups
exact payload bytes into immutable ZIP shards. A manifest says which member
contains a function's code and pins its checksum. Compression and fewer separate
files can reduce retained allocation. The [real mirror experiment](../../native-compact-storage.md#measured-mirror--2026-10-10)
preserved every member and reduced representation allocation from about 465.8 MB
to 26.9 MB. That comparison includes inventory and source envelopes as well as
function files; it has a larger scope than the function-only measurement above.
Neither this retained sample nor an average proves the whole program will fit.

A useful archive test extracts a named function and compares the original bytes
and checksums. A readable text preview alone cannot establish preservation of
warnings, failed attempts, provenance or every original byte. The existing
captures remain available while the new representation is evaluated.
Creating this mirror neither generates additional code nor frees disk while
the original files are retained. Its immediate purpose is to measure a more
compact representation for future exports without losing existing evidence.

## What a real capture can teach a tested tool

The first [real reader build](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-execution-v1/failed-execution-report.json)
stopped before publication despite passing its synthetic tests. Some revisions
retain a workflow profile which contains an upstream native-analysis profile;
the corpus run identifies that native profile directly. The reader compared
the outer workflow description with the inner native description and rejected
valid evidence. Its original fixtures covered direct native profiles only.

The [export authority](../../../../tools/export_native_corpus.py) already defines
how to resolve that relationship from the retained evidence record's provider.
The correction must preserve the original description and record the resolved
native identity, then test their relationship. Silently replacing provenance
would conceal the mistake. Successful fixture tests establish their cases;
running against a representative real capture can reveal an omitted case.
This storage-reader failure did not alter the original files or publish a
partial viewer.
The [current reader status](../../native-compact-storage.md#status) records the
later corrections and their reviews; the failed capture remains historical evidence.

## Saving an answer and saving the analyzer

The [closed REA session](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-retry-v3/post-run/manifest-v1.json)
saved its observation snapshot and exported results. Those let us reread and audit
answers already produced. Its temporary Ghidra project was removed when the
provider closed. Opening an observation snapshot has not demonstrated that a
new native function can be decompiled without importing/analyzing again.

A persistent Ghidra project stores the program's analyzed instructions, function
boundaries, references and recovered types. The [recovery design](../../native-analysis-recovery.md)
therefore requires saving the project, closing its owner, recording every file's
hash, and reopening a working copy read-only to verify program identity. A project
filename or a successful process exit is insufficient proof of a reusable database.

Even a saved database does not mean an interrupted analyzer resumes at its former
position. The installed headless processing route schedules reanalysis when it is
enabled. We preserve established facts and report timeout/partial status; we do
not claim to have preserved an unfinished analyzer queue.

## Why the recovery experiment starts with eight bytes

The [preparation observations](../../native-analysis-recovery.md#preparation-observations--2026-10-11)
use a small independently authored raw program, whose bytes are analyzed rather
than executed. A fixture-only script supplies one known function and a marker.
That makes the expected identity and persistence checks simple while exercising
the actual Ghidra launcher, JVM diagnostics, save operation and project layout.

The first attempt rejected an exact JDK-version mismatch; the next rejected a
diagnostic attach failure. These failures test a useful distinction: a requested
launch setting is not yet a measured setting. The gate permits progress only
after the running JVM and external diagnostics agree. Later historical fixture
runs saved and reopened copies successfully, but changing the controller's
acceptance rules still requires new proofs and reviews.

For a checkpoint, we keep a closed working project, reopen a disposable copy,
copy the original into its checkpoint layout, then reopen another disposable
copy of that layout. The source checkpoint itself stays closed. This protects
its recorded bytes from lock creation or other reopen effects, and tests the
layout that future exports will use. Keeping every tree costs disk space: the
current conservative analysis budget counts four full representations, even if
the filesystem could make a copy cheaply.

A one-function success does not establish Live's database size, timeout behavior
or export coverage. Those are separate experiments with their own acceptance
conditions. The small fixture lets us find launch and recovery mistakes before
spending the resources needed for the real program.

The [first Live import](../../native-analysis-recovery.md#first-live-import-rejected--2026-10-12)
demonstrates another boundary. Ghidra selected an Apple Silicon language model
for the Mach-O program; the raw fixture had explicitly selected generic ARM64.
The gate correctly rejected the mismatch. A fixture can prove saving, reopening
and cancellation while missing a target-specific loader choice. We retain both
the successful fixture cases and the failed target case, then correct the exact
assumption with separate profiles rather than weakening the check.

## Why a result file is not yet a committed result

The [driver guide](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/README.md)
shows the evidence paths inside a job. A job begins with an `.incomplete` marker.
That marker stays while the controller checks saved files, closes processes,
reopens disposable copies and publishes the final reports. Readers reject jobs
which still have it. A report named “pass” can exist before these checks finish;
the name and file presence alone do not establish a usable checkpoint.

For analysis and export, the original checkpoint must also be rechecked after
use. The marker is removed only after those checks and all fallible publication
steps finish. This order makes handled failures discoverable without accepting
a partially published result. It does not prove survival of power loss. The
[proof matrix](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/proof-matrix.json)
identifies which cases actually ran and which used injected failures.

Cancellation needs its own experiment. In the [deadline investigation](../../native-analysis-recovery.md#deadline-boundary-correction--2026-10-12),
a deliberately slow file hash continued after process cleanup even though the
job ultimately rejected its output. Rejection answered whether the result was
accepted; it did not answer whether work stopped on time. A real short alarm
exposed that difference. The corrected fixture probes measure both elapsed time
and the absence of an accepted result. This is why a failure case needs an
observable stopping condition as well as an error message.

## Reading the next checkpoint

Use the [artifact catalog](../../artifacts/index.md) for available code, and the
[execution ledger](../../native-phase-execution.md) for actual progress. Keep four
questions separate: did we preserve the bytes, can a reader find the function,
can the analyzer continue after restart, and what behavior does the code support?
Each needs its own evidence.

In the [corrected Live attempt](../../native-analysis-recovery.md#corrected-import-passes-reopen-capacity-stop--2026-10-12),
importing and saving passed, but the first reopening could not start because its
fresh disk-space gate failed. A 345 MB closed project and its exact copy are useful
evidence, yet they do not prove that Ghidra can reopen the database. The incomplete
marker preserves that distinction. The loader reported 3,639 functions without
analysis; the older fully analyzed inventory is a separate measurement. Saving,
reopening, analyzing and exporting are four different milestones.
