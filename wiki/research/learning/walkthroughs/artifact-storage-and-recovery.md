---
id: LESSON-ARTIFACT-STORAGE-RECOVERY
type: research
status: current
updated: 2026-10-10
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
These are reconstructed C-like files, not Ableton's original source repository.

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

The [compact-storage design](../../native-compact-storage.md) proposes grouping
exact payload bytes into immutable ZIP shards. A manifest says which member
contains a function's code and pins its checksum. Compression and fewer separate
files can reduce retained allocation. The reduction must be measured on actual
exports; neither a tiny example nor an average proves the whole program will fit.

A useful archive test extracts a named function and compares the original bytes
and checksums. A readable text preview alone cannot establish preservation of
warnings, failed attempts, provenance or every original byte. The existing
captures remain available while the new representation is evaluated.
Creating this mirror neither generates additional code nor frees disk while
the original files are retained. Its immediate purpose is to measure a more
compact representation for future exports without losing existing evidence.

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

## Reading the next checkpoint

Use the [artifact catalog](../../artifacts/index.md) for available code, and the
[execution ledger](../../native-phase-execution.md) for actual progress. Keep four
questions separate: did we preserve the bytes, can a reader find the function,
can the analyzer continue after restart, and what behavior does the code support?
Each needs its own evidence.
