---
id: RESEARCH-R2-CORPUS-TOOLING
type: research
status: draft
updated: 2026-10-17
access: analysis
---

# Revision 2 bulk corpus and index tooling (C1/C2)

Analyst-only tooling for [roadmap revision 2](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17)
Phase 1 items C1 (bulk decompile) and C2 (derived indexes). It runs against an
already analyzed, saved Ghidra project, opened read-only. It was validated on
`Push2DisplayProcess.arm64`. It has **not** been run on `Live.arm64`; the Live
numbers below are projections. Nothing here is application code or crosses the
handoff boundary.

## Design

**C1, [R2BulkDecompile.java](../../tools/ghidra/R2BulkDecompile.java).** One
headless JVM, `-process PROGRAM -noanalysis -readOnly`, opens no transaction.
Eligible functions are all non-external functions in `FunctionManager` address
order; externals are counted as excluded. Behavior:

- A fixed pool of `threads` workers, each with its own `DecompInterface` (C code
  and syntax tree, default options) and the 60-second per-function timeout used
  by `RecoveryNativeExport.java`.
- Chunk *k* holds eligible functions `[k*chunk, (k+1)*chunk)`. Each chunk is one
  JSONL file. It is built in memory, written to a temp file, fsynced and
  committed by hard link, so a committed chunk is never replaced.
- Each record holds the entry (`0x…` in the default space, `SPACE:0x…`
  otherwise, the same canonical form as `export_native_corpus.address()`),
  the qualified name, thunk flag, body bytes, body ranges, listing signature and
  state. It also holds the error, `timed_out`, `partial_code`, warnings (decompiler
  message plus `WARNING` lines), milliseconds, code byte count, code SHA-256 and
  the exact code text.
- `exported` and `exported-with-warnings` require complete code. `failed`
  requires an error message. Partial code on failure is kept and flagged; it is
  never promoted.
- If the decompiler cannot start or an I/O error occurs, the run aborts and the
  chunk stays pending. Such a failure is never recorded as a function failure.
- `run.json` pins the program name, executable SHA-256, language, compiler,
  Ghidra version, eligible count, SHA-256 of the eligible entry list, chunk size
  and timeout. A rerun with any difference aborts.
- A rerun validates every committed chunk against the pinned list and code
  hashes, then skips it. Failures are not retried.
- `coverage.json` is rebuilt from committed files at the end of every
  invocation, under a file lock shared by concurrent JVMs. Its counts for
  `exported`, `exported-with-warnings`, `failed` and `pending` must sum to
  `eligible`, or the script throws. It also records attempted and successful
  counts, timeouts, latency percentiles, bytes, the failure list and the last
  invocation.
- `shard=i/n` attempts chunks with `k % n == i`. Use it for a spread sample, or
  for *n* JVMs on separate project copies writing disjoint chunk files into one
  output.
- `instances=K` opens K−1 extra read-only instances of the same program file
  (`DomainFile.getReadOnlyDomainObject`) and assigns threads round-robin. Each
  instance has its own database lock.
- Unknown script arguments fail before any output.

**C2, [R2ExportIndexes.java](../../tools/ghidra/R2ExportIndexes.java).** It can
be a second `-postScript` in the same invocation. Each file is replaced by
rename, and `manifest.json` (line count, bytes and SHA-256 per file, plus
program identity) is written last. Order is address order with sorted
sub-lists, and there are no timestamps.

| File | One line per | Content |
| --- | --- | --- |
| `strings.jsonl` | Defined string (`DefinedStringIterator`, including strings nested in composites) | Value, type, length. Each reference into the string gives `from`, offset and type, plus the containing function. For a reference from data it gives `via`: the functions that reference the containing data item, one level deep. |
| `calls.jsonl` | Direct call edge | Caller, site, callee, ref type and `kind`. `kind` is `call`, or `tail-jump` for a non-computed jump to another function's entry. A thunk callee also carries its resolved target. |
| `indirect.jsonl` | Computed call or jump site | Function, `in_thunk`, flow type, instruction text and any analysis-resolved targets |
| `vtables.jsonl` | Address carrying a `__ZTV*`/`_ZTV*`/`vtable`/`vtable for*` symbol | All symbol names and function-pointer slots by offset. The scan starts at +16 and stops at the next non-default symbol, three consecutive non-function words, block end or 4,096 words, and records the stop reason. Imported vtables are marked `external-block`. |
| `aliases.jsonl` | Function entry, non-external then external | Qualified name, thunk target, library and every symbol with its source and primary flag |

**Verifier, [r2_corpus.py](../../tools/r2_corpus.py).** It never runs Ghidra.
`corpus` re-derives the counts from the chunks and applies the same record
rules as the Java script. It checks code hashes and that `coverage.json` agrees.
Once nothing is pending, it also checks the entries against the pinned
eligible-list digest. It reports leftover temp files. `indexes` checks lines,
bytes and SHA-256 against the manifest and parses every line. Ten unit tests in
[test_r2_corpus.py](../../tools/tests/test_r2_corpus.py) cover:

- a complete corpus and pending chunks;
- changed code bytes and a failure without an error;
- stale coverage and entries that differ from the pinned list;
- a short chunk and an unexpected file;
- a modified index.

## Measured on Push2

Target: `analysis/ableton-live-12.4.3/derived/Push2DisplayProcess.arm64`,
SHA-256 `5988ef09f5ff69ab916a7b399d81b28b401bb2a170fd1eb4505394f2527d5465`,
Ghidra 12.1.4, `AARCH64:LE:64:AppleSilicon`. A scratch import with default full
analysis (`-max-cpu 8`, 8 GiB heap) took 71.7 s wall with 2.0 GB peak RSS. The
project is 52 MB, one 52 MB `db.1.gbf`. It has 13,611 functions: 12,626 eligible
and 985 external.

**Outcome (identical in every run).** All 12,626 eligible functions were
attempted, with these results:

- 8,859 `exported`;
- 3,766 `exported-with-warnings`;
- 1 `failed`: `FUN_1001fe718` (32,000-byte body), `Exception while decompiling
  1001fe718: process: timeout` after 60.0 s, no partial code.

The next slowest functions took 20.1 s and 7.1 s. Latency at one thread was p50
1 ms, p90 9 ms, p99 50 ms, sum 137 s. Common warnings were "Subroutine does not
return" (2,201), "Treating indirect jump as call" (1,138), "Could not recover
jumptable … Too many branches" (1,137) and "Unknown calling convention"
(924).

The SHA-256 over (entry, state, code hash) is identical across all 11 scratch
corpora: every thread and instance setting, the two-JVM run and the
killed-and-resumed run. Decompiler output was byte-identical in every
configuration.

**Scaling.** Each run used `chunk=50` (253 chunks) on a fresh output. The table
shows:

- **fn/s**: first-half throughput, from chunk commit times measured from the
  in-JVM start. The one-thread figure excludes the 20 s and 7 s outliers, which
  fall in its first half.
- **Speedup**: relative to one thread.
- **Latency sum**: the per-function decompile time summed over all functions.
- **CPU**: includes decompiler children.
- **JVM / group RSS**: peak RSS of the JVM alone, and peak summed RSS of the JVM
  plus its decompiler children, sampled each second.

Every wall time is at least 72 s because of the single 60 s timeout.

| Threads | Program instances | JVMs | fn/s | Speedup | Latency sum (s) | CPU % | JVM / group RSS (MiB) | Wall |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 1 | 1 | 1 | 222 | 1.0 | 137 | 112 | 641 / 1,011 | 2:30 |
| 4 | 1 | 1 | 419 | 1.9 | 150 | 201 | 964 / 1,493 | 1:28 |
| 8 | 1 | 1 | 458 | 2.1 | 215 | 261 | 1,184 / 1,819 | 1:23 |
| 16 | 1 | 1 | 592 | 2.7 | 308 | 290 | 1,293 / 1,986 | 1:19 |
| 4 | 4 | 1 | 438 | 2.0 | 140 | 199 | 1,380 / 1,916 | 1:27 |
| 8 | 8 | 1 | 789 | 3.6 | 154 | 241 | 1,414 / 2,049 | 1:16 |
| 16 | 4 | 1 | 428 | 1.9 | 445 | 408 | 1,720 / 2,558 | 1:29 |
| 16 | 8 | 1 | 505 | 2.3 | 424 | 415 | 2,181 / 2,807 | 1:29 |
| 16 | 16 | 1 | 596 | 2.7 | 314 | 410 | 2,252 / 3,091 | 1:23 |
| 2×8 | 2×8 | 2 (hard-linked copy) | 815 | 3.7 | 257 | — | 1,488 + 1,516 / 1,730 + 2,123 | 1:19 |

**Confounding load.** The host is a Ryzen 9 5950X with 16 physical cores and 32
SMT threads. Other agents were running about eight concurrent Ghidra imports at
110–130% CPU each. Observed load averages:

- 15-minute load rose from 11.9 to 22.0 during the first two series (`uptime`
  at 19:21:22);
- 35.5–35.9 during the one-instance thread dump;
- 24.6 mean during the two-JVM run.

At 8 threads and above, the throughput differences are within this noise and are
not a clean scaling curve. The direct evidence of contention comes from five
`jstack` samples per configuration at 16 threads, retained under
`thread-dumps/`:

- **One program instance:** 28 of 80 worker samples (35%) were in
  `ghidra.util.Lock.acquire`, the program database lock (15 BLOCKED, 13
  WAITING). Another 38 were reading decompiler output.
- **Sixteen instances:** no lock waits. 39 samples were reading decompiler
  output and 17 were writing callback responses.

*Inferred:* the decompiler callbacks serialize on the program lock. Separate
instances remove that lock contention. On this loaded host, the remaining limit
was CPU available to the native decompiler processes, so the throughput plateau
of about 600–800 functions/s is a property of the shared host, not of the tool.
JVM RSS grew by about 64 MiB per extra Push2 instance.

**Concurrency, resume and C2.**

- *Project lock.* A second JVM on the **same** project fails with `LockException:
  Unable to lock project!`, even with `-readOnly`. Separate JVMs need separate
  project directories.
- *Hard-linked copy.* `cp -al` costs 0 bytes beyond directory entries; a full
  copy costs the project size, 52 MB here. Two JVMs on the original and a
  hard-linked copy (`shard=0/2` and `1/2`) merged into one coverage that
  verifies and sums to 12,626.
- *Hard links are not fully isolated.* After read-only opens, `db.1.gbf` kept its
  shared inode and unchanged content. `idata/~index.dat` and
  `versioned/~index.dat` were replaced with new inodes. `project.prp` and
  `user/~index.dat` kept the shared inode, received newer mtimes and had
  identical content: they are rewritten in place. Give each copy private copies
  of every non-`.gbf` file.
- *Kill and resume.* A 4-thread run was killed with SIGKILL after 25 s, with 178
  of 253 chunks committed and no temp files left. The rerun validated those
  chunks, wrote the remaining 75 chunks (3,726 functions) and produced the
  identical output digest.
- *Validation cost.* A validation-only rerun on a complete corpus took
  0.4–0.7 s.
- *C2.* C2 took 3.0–3.4 s. It ran after C1 in the same JVM and again
  separately, with byte-identical manifests and files. Push2 index contents:
  - strings: 14,824, of which 4,410 are referenced; 9,691 references, 4,910
    from functions and 61 resolved through one data level;
  - calls: 42,775 direct edges, including 137 tail-jumps; 24,871 edges go to
    thunks with a resolved target;
  - indirect: 5,407 sites, of which 4,068 are calls (3,426 unresolved) and 810
    are inside thunks;
  - vtables: 31, of which 17 stop at the next symbol, 13 are imported and 1
    stops after a non-function run; 128 slots in total;
  - aliases: 13,611, of which 570 entries carry more than one symbol.

## Storage choice

Measured on the complete Push2 corpus with
[layout_probe.py](../../analysis/ableton-live-12.4.3/r2/c-tooling-v1/layout_probe.py)
on 4 KiB-block ext4 under `/var/tmp`. Mean code is 997 bytes per function (p50
329, p99 9,859, max 128,826).

| Layout | Files | Allocated | Per function | Projected to 418,418 |
| --- | ---: | ---: | ---: | ---: |
| Chunked JSONL, this tool | 256 | 18.8 MB | 1,491 B | 0.62 GB; 4.2 k chunk files at `chunk=100` |
| `export_native_corpus.py` per-function revisions | 37,877 files + 25,252 directories | 263.4 MB | 20,862 B | 8.73 GB, plus about 0.62 GB of retained evidence copies, plus inventory and coverage; about 2.1 M inodes |

**Decision: chunked JSONL.** The per-function layout projects to about 9.4 GB
at Push2's code sizes, at the edge of the 10 GB limit before Live's code-size
bias. It is also incompatible for a reason storage does not change:
`export_native_corpus.py` `init`/`ingest`/`check` accept only REA records (`ev_`
evidence IDs, REA analysis-profile digest, an REA `list_procedures` inventory),
and [native export design](native-export-design.md#conditional-selected-entry-fallback)
forbids presenting custom script output under invented REA evidence IDs. The
roadmap line "ingest through `export_native_corpus.py check`" therefore cannot
be met as written.

**Conversion path, if the per-function layout is required later.** This is
proposed, not implemented. Add a second evidence kind to `export_native_corpus.py`
through a reviewed change:

- the retained source is the committed chunk file, keyed by its SHA-256;
- the profile digest is SHA-256(`run.json`);
- the inventory is the eligible list (`run.json` digest plus `aliases.jsonl`);
- revision IDs are `r2_<chunk sha256>-<line>`, not `ev_`.

`check` would then verify each revision against its chunk line. Until then,
consumers read chunks directly, for example
`grep -h '"entry":"0x100130668"' CORPUS/chunks/*.jsonl | jq -r .code`. A
function's chunk is its eligible position divided by `chunk_size`.

## Live projection (not measured)

**Sample bias.** Push2 is a small display helper:

- 12,626 functions, small (p50 329 code bytes);
- Qt, spdlog and fmt heavy;
- a 52 MB project, against a 149.7 MB Live image with 418,418 eligible functions
  in the earlier REA inventory (the Ghidra 12.1.4 count comes from G0.3).

Live functions and its program database are larger, so per-function latency and
per-instance memory are expected to be higher by an unknown factor. The scaling
was measured on a loaded host.

| Quantity | Basis | Projection |
| --- | --- | --- |
| C1 thread-time | 10.9 ms mean per function (Push2, including outliers) × 418,418 × an assumed 1–4 latency factor | 1.3–5.1 thread-hours |
| C1 effective parallelism | 3.6–3.7 measured (loaded host); 8–14 assumed for 28 threads on an idle 16-core/32-thread host | — |
| C1 wall | Thread-time ÷ parallelism | About 6 min to 1.5 h, plus project open and the final coverage scan (a few seconds per 100 MB of chunks) |
| Timeouts | 1 per 12,626 on Push2 | About 33 × 60 s of thread time; negligible at 28 threads |
| C1 output | 1,491 B per function × 1–3 for code size | 0.6–1.9 GB |
| C2 output and time | 20.2 MB and 3 s for Push2; scaled by function count | About 0.7 GB, minutes |
| Memory | Push2: about 64 MiB JVM RSS per extra instance; group-minus-JVM peak 0.37 GiB at 1 thread, 0.68–0.82 GiB at 16 threads | Unknown for Live; measured by the sample step below |

**Recommendation.** Use one JVM with 28 threads and one program instance per 2
threads (`instances=14`). Raise to `instances=28` only if the sample's peak group
RSS leaves at least 25% of RAM free.

Fall back to K JVMs (`shard=i/K`) on hard-linked project copies only if the
one-JVM sample shows idle CPU with no lock waits, which would point to a
JVM-wide limit. Copy cost:

- full copy: the saved `LiveR2` size, which is unknown until G0.3 finishes (690
  MB at import);
- hard-linked copy: about 0 bytes, provided the non-`.gbf` files are made
  private.

Each extra JVM duplicates JVM base memory and project open time. Validated
hard-linked copy recipe:

```sh
mkdir -p $R/copies/c1 && cp -al $R/projects/LiveR2.gpr $R/projects/LiveR2.rep $R/copies/c1/
find $R/copies/c1 -type f ! -name '*.gbf' -exec sh -c 'cp -p "$1" "$1.p" && mv "$1.p" "$1"' _ {} \;
```

## Live run command

Run this after G0.3 has finished and its process has released `projects/LiveR2`,
since one process holds the project lock. The A/B sample (5% of chunks)
measures Live throughput, latency spread, bytes and memory. The full run then
resumes and skips the sampled chunks.

```sh
R=/var/tmp/sound-analysis REPO=/home/ollie/Documents/sound
G=$HOME/.local/opt/ghidra_12.1.4_PUBLIC MEASURE=$REPO/analysis/ableton-live-12.4.3/r2/c-tooling-v1/measure.sh
export JAVA_HOME=$HOME/.local/opt/jdk-21.0.12.1+1 PATH=$HOME/.local/opt/jdk-21.0.12.1+1/bin:/usr/bin:/bin
unset JAVA_TOOL_OPTIONS _JAVA_OPTIONS GHIDRA_JAVA_OPTIONS
export XDG_CONFIG_HOME=$R/ghidra-home/config XDG_CACHE_HOME=$R/ghidra-home/cache
export GHIDRA_HEADLESS_JAVA_OPTIONS="-Duser.home=$R/ghidra-home -Djava.io.tmpdir=$R/tmp -XX:ParallelGCThreads=8"
export GHIDRA_HEADLESS_MAXMEM=48G
live() { local name=$1; shift
  $MEASURE $R/corpus/logs/$name $G/support/analyzeHeadless $R/projects LiveR2 -process Live.arm64 \
    -noanalysis -readOnly -scriptPath $REPO/tools/ghidra -log $R/corpus/logs/$name/headless.log "$@"; }
# 1. A/B sample on adjacent 1/40 slices (about 10,500 functions each): one instance vs 14.
live sample-i1  -postScript R2BulkDecompile.java out=$R/corpus/decomp threads=28 instances=1  chunk=100 shard=0/40
live sample-i14 -postScript R2BulkDecompile.java out=$R/corpus/decomp threads=28 instances=14 chunk=100 shard=1/40
# 2. Full run in the better configuration (validates and skips sampled chunks), then indexes in the same JVM.
live full -postScript R2BulkDecompile.java out=$R/corpus/decomp threads=28 instances=14 chunk=100 \
          -postScript R2ExportIndexes.java out=$R/corpus/indexes
# 3. Independent verification.
python3 $REPO/tools/r2_corpus.py corpus $R/corpus/decomp
python3 $REPO/tools/r2_corpus.py indexes $R/corpus/indexes
```

Each run directory gets `time.txt`, `stdout.txt` (with the `R2_INVOCATION` and
`R2_COVERAGE` lines), `samples.txt` (epoch, group RSS in KiB, load average) and
`result.json` (exit code, peak group RSS). Compare the samples by
`functions_written / decompile_seconds`. `chunk=100` keeps about 4 chunks per
thread in each sample. Every later run on the same output must keep `chunk=100`,
because the chunk size is part of `run.json`.

## Measured on Live — 2026-10-17

The coordinator ran the command above through
[`c1-live-v1/run.sh`](../../analysis/ableton-live-12.4.3/r2/c1-live-v1/run.sh) against
`projects/LiveR2`, while a query server held a hard-linked copy and other analyses
ran. Evidence and timings: [c1-live-v1 manifest](../../analysis/ableton-live-12.4.3/r2/c1-live-v1/manifest.json).

| Run | Functions | Wall | Peak group RSS | Rate between first and last chunk |
| --- | --- | --- | --- | --- |
| Sample, 1 instance, shard 0/40 | about 10,500 | 1:09 | 10.8 GB | about 181 per second |
| Sample, 14 instances, shard 1/40 | about 10,500 | 2:18 | 14.4 GB | about 82 per second |
| Full, 14 instances, plus C2 | 418,417 (sampled chunks validated and skipped) | 13:13 | 29.0 GB | about 848 per second over a two-minute window |

The short samples reversed the Push2 result, but the full run with 14 instances
sustained about 4.7 times the one-instance sample rate. Inferred, not measured:
the 14-instance sample was dominated by per-instance cache warm-up over a small
slice. Outcome: 320,967 exported, 97,387 exported with warnings, 63 failed;
`r2_corpus.py` reports the corpus complete with no stale temporary files and the
indexes consistent. Sizes: corpus 755 MB, indexes 679 MB. Index counts: 452,752
strings, 1,599,830 direct call edges, 268,015 indirect call sites, 420,470 aliases
and only 80 symbol-named vtables, so vtable recovery in Live needs constructor and
vtable-store tracing.

## Live x86_64 cross-check corpus — 2026-10-17

Live's x86_64 slice (SHA-256 `1bae9a97…be999b0`) was analyzed in its own project
(1:39:43 wall, 33.8 GB peak RSS; 414,791 non-external functions, 557,145 strings)
and decompiled with the same settings in 17:17: 317,021 exported, 97,725 with
warnings, 45 failed; indexes verified (1,572,950 call edges, 271,501 indirect
sites, 80 symbol-named vtables). Evidence:
[c1-live-x86-v1 manifest](../../analysis/ableton-live-12.4.3/r2/c1-live-x86-v1/manifest.json).
This is a second compile of the same source for cross-checking arm64 readings; the
specifications are derived from the arm64 build.

## Limitations and unknowns

- **Untested paths.** The decompiler start-failure and I/O abort paths were not
  exercised. No Push2 function produced partial code.
- **Leftover temp files.** A hard kill during a commit can leave a
  `.chunk-*.tmp` file. It is ignored, and the verifier reports it.
- **String references.** `strings.jsonl` follows data references only one level.
  Typeinfo-name and metadata strings stay without a function. References from
  Ghidra's `Entry Point` pseudo-space appear as `from: "Entry Point:0x0"`, type
  `EXTERNAL`.
- **Vtables.** Vtable candidates require a symbol, so stripped classes are
  absent. The slot scan is a heuristic and does not separate secondary tables in
  a group.
- **Indirect calls.** `indirect.jsonl` does not recover vtable offsets from
  computed calls; read the pseudocode for those.
- **Static edges.** Call edges are static references and do not establish
  runtime execution.
- **Measurement noise.** Scaling numbers come from a loaded shared host. The
  first scaling series ran the script before `instances` and argument validation
  were added; the output digest shows the decompiler output is the same.

Retained evidence:
[analysis/ableton-live-12.4.3/r2/c-tooling-v1/](../../analysis/ableton-live-12.4.3/r2/c-tooling-v1/)
holds the per-run time, samples, coverage and invocation lines, the thread dumps,
[checks.txt](../../analysis/ableton-live-12.4.3/r2/c-tooling-v1/checks.txt), the
driver scripts, the complete Push2 corpus and indexes, and `manifest.json`.
Scratch corpora remain under `/var/tmp/sound-analysis/scratch/c-tooling/runs`.
