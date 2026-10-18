---
id: RESEARCH-R2-QUERY-ROUTE
type: research
status: draft
updated: 2026-10-17
access: analysis
---

# Investigator query route against the saved Live project

**Question.** How can investigators get function dossiers, cross-references and
pseudocode from the analyzed, saved `LiveR2` project without re-running analysis,
and how can two or three of them work at the same time?

**Answer (proposed).** Do not use REA for this. Run one long-lived, read-only
[`R2FunctionDossier.java`](../../tools/ghidra/R2FunctionDossier.java) server against a
hard-linked copy of the frozen project. Investigators submit query files to a
spool directory. An investigator who needs custom Ghidra scripts gets their own
hard-linked copy. Evidence is in
[e-rea-v1](../../analysis/ableton-live-12.4.3/r2/e-rea-v1/manifest.json):
[source citations](../../analysis/ableton-live-12.4.3/r2/e-rea-v1/rea-source-inspection.json)
and [measurements](../../analysis/ableton-live-12.4.3/r2/e-rea-v1/measurements.json).
The Push2 measurements use the re-derived `Push2DisplayProcess.arm64`
(SHA-256 `5988ef09…d5465`). They were taken while other jobs were loading the
host, so treat wall times as upper bounds.

## REA 6.5.0 cannot open a saved project

Observed in the installed 6.5.0 source. File and line citations are in the
source-inspection record.

- **Inputs.** `open_binary` accepts only `path`, `format`, `architecture`,
  `entry_point`, `provider_id` and `snapshot_path` (`sessionLifecycleInputs.js:20-34`).
  The only "analysis database" target kind is a Hopper `.hop` document
  (`BinaryTargetResolver.js:103-114`). The Ghidra provider rejects every
  non-executable target (`GhidraProvider.js:110-116`).
- **Measured rejection.** `rea function` rejected `Push2E.gpr`, `Push2E.rep`
  and `Push2.gzf` in under 1 s, each with `target_unavailable`.
- **Import mode.** Every session runs `-import <copy of target> … -readOnly
  -deleteProject` into `<TMPDIR>/…/project` (`GhidraLauncher.js:326-381`).
  The target is copied into the runtime root first. REA's default analysis is
  followed by `ReaGhidraNoReturnFix.java`, so REA's analyzed state is not the
  same as `LiveR2`'s.
- **`--snapshot`.** A snapshot is an exact-query result cache, not a database. It
  holds at most 10,000 entries, keyed by target, profile, operation and
  parameters. Results with truncated references are never stored
  (`AnalysisSnapshotCache.js:30-41,161-223`). The CLI checks for a replay before
  launching Ghidra; any miss does a full import and analysis
  (`DirectAnalysis.js:97-178`). On Push2:
  - cold `rea function --provider ghidra --snapshot`: 80.9 s, 2.46 GB RSS
  - the same query again: 1.35 s, no JVM, same `evidence_id`
  - a different function with the same snapshot: 79.4 s, a full re-analysis
- **Auto provider selection.** Without `--provider ghidra`, selection now fails
  as ambiguous because Hopper and IDA are also candidates.

### Comparison with the 6.3.0 observations

The 6.3.0 observations are in [export execution](native-export-execution.md) and
[operational design](native-phase-execution.md#operational-design).

| 6.3.0 observation | 6.5.0 |
| --- | --- |
| Ephemeral read-only import with `-deleteProject` | Holds |
| `GHIDRA_HEADLESS_MAXMEM` honoured | Holds. Default when unset is `2G`. Fixed `-XX:ParallelGCThreads=2 -XX:CICompilerCount=2` (`GhidraJavaLaunch.js:134-136`); the 6.3.0 values were not recorded |
| `REA_GHIDRA_STARTUP_TIMEOUT_MS` bounds analysis | Holds. Default 330,000 ms, maximum 2,147,483,647 ms, one absolute deadline for import, analysis and readiness. Live needs it raised |
| No per-function decompiler deadline | Holds (`ReaGhidraBridge.java:3311`, timeout 0). Ordinary tool calls also have no client deadline; only the shutdown request has one (10 s) |
| Java option variables cleared (`GhidraInstallation.js:262-270`) | Holds, now at lines 290-298 |
| Direct JVM launch, no CPU-limit option | Holds. The only way to bound CPUs is OS affinity (`taskset`) |
| Project under `TMPDIR` or `/tmp` | Holds. `TMPDIR` is used unless a path element starts with `.` (`GhidraSessionRoot.js:28-38`). The measured peak runtime-directory size was 80 MB for Push2; the directory was removed afterwards |
| Shutdown timings 3/6/9 s | These belong to our transport and are unchanged. REA itself sends a bridge `shutdown` (10 s), waits 500 ms, then sends SIGKILL to the token-verified process group (1 s grace, one retry), then removes the runtime roots |
| 139 MCP tools | Now 207. New `REA_MCP_MAX_RESPONSE_BYTES`, default and minimum 10 MiB |
| Query snapshot is not a saved database | Holds; see the snapshot bullet above |

`open_binary` is now lazy: Ghidra starts on the first provider query (`GhidraClient.js:187-192`).

[`run_native_analysis.mjs`](../../tools/run_native_analysis.mjs) still works with
`NATIVE_REA_ENTRY` pointing at the 6.5.0 `rea.mjs`. Measured on Push2:

| Step | Time |
| --- | --- |
| Handshake | 1.5 s |
| `open_binary` | 48 ms |
| First `analyze_function` (includes import and analysis) | 68.7 s |
| Second `analyze_function` | 0.28 s |
| `xrefs` | 4 ms |
| `close_binary` with snapshot | 1.4 s |

The shutdown was clean and `TMPDIR` was empty afterwards. A Push2 function result
envelope was 5.06 MB, so large Live functions may need `REA_MCP_MAX_RESPONSE_BYTES`.

## Ghidra's project lock and the copy options

**Lock (observed).** While one read-only `analyzeHeadless` held `Push2E`, a
second `-process … -readOnly` aborted with `LockException: Unable to lock
project!`. `-readOnly` does not relax the lock.

**Side effects of a read-only session (observed).** The session replaced the
`~index.dat`/`~index.bak` files with new inodes but identical bytes. A writable
save on the source wrote `db.2.gbf` and removed `db.1.gbf`. In both cases a
hard-linked copy stayed byte-identical. This is one probe, not a guarantee;
re-check hashes on Live.

| Option | Push2 measurement | Per investigator on Live |
| --- | --- | --- |
| (a) One server JVM, spool requests | Startup 4.9 s. Three simultaneous requests finished 2.9/3.2/5.2 s after submission (14.7/15.4/26.4 s at load average 30). Repeat function served in 0.04 s. 0.96 GB RSS | 0 bytes and 0 startup; one Live open shared. Latency is the queue |
| (b) Hard-linked copy `cp -al` | 0.00 s, 360 bytes. Three concurrent one-shot runs on the original and copies: 12.4–12.7 s each, about 1 GB RSS each, outputs byte-identical | About 0 bytes and milliseconds, plus one Live open and its RAM per process |
| (b′) Full copy `cp -a` | 0.12 s (warm page cache), 52.5 MB | Full project size each. Estimated 2.2–3.3 GB (inferred from the measured Push2 ratios and Live's 690 MB unanalyzed import), plus copy time |
| (c) Packed `.gzf` | Pack 7.6 s → 15.8 MB (30 %). Import 4.3 s → 52.5 MB project | Full project size each plus an unpack. Useful only for archive or transfer to the macOS host |

The Live open time and memory are not yet measured. The G0.3 `c-reopen` step and
`project-bytes.txt` will supply them.

## Recommended route

Once G0.3 has finished and nothing holds `LiveR2`:

1. Freeze the project and make the query copy:

   ```sh
   P=/var/tmp/sound-analysis
   test ! -e $P/projects/LiveR2.lock && mkdir -p $P/query $P/query-spool && \
     cp -al $P/projects/LiveR2.gpr $P/projects/LiveR2.rep $P/query/
   ```

2. Start the server once. It is the only process that holds the copy.

   ```sh
   export JAVA_HOME=$HOME/.local/opt/jdk-21.0.12.1+1 PATH=$HOME/.local/opt/jdk-21.0.12.1+1/bin:/usr/bin:/bin
   export XDG_CONFIG_HOME=$P/ghidra-home/config XDG_CACHE_HOME=$P/ghidra-home/cache GHIDRA_HEADLESS_MAXMEM=16G
   export GHIDRA_HEADLESS_JAVA_OPTIONS="-Duser.home=$P/ghidra-home -Djava.io.tmpdir=$P/tmp"
   $HOME/.local/opt/ghidra_12.1.4_PUBLIC/support/analyzeHeadless $P/query LiveR2 \
     -process Live.arm64 -noanalysis -readOnly -max-cpu 4 \
     -scriptPath /home/ollie/Documents/sound/tools/ghidra \
     -postScript R2FunctionDossier.java --serve $P/query-spool \
     -log $P/query-spool/server.log > $P/query-spool/server.stdout 2>&1 &
   ```

   The server is ready when `server.stdout` contains `R2FunctionDossier serving`.
   The 16G heap is proposed; size it from the `c-reopen` RSS.

3. Each investigator writes one query per line, publishes it by renaming, and
   reads `results/<name>/` after it appears:

   ```sh
   Q=/var/tmp/sound-analysis/query-spool
   printf '%s\n' 'str:LoopOn' '0x10276e5d4' > $Q/requests/inv1-0001.tmp && \
     mv $Q/requests/inv1-0001.tmp $Q/requests/inv1-0001.txt
   ```

   Use a unique `<agent>-<sequence>` name for each request. To stop the server,
   run `touch $Q/requests/STOP`.

4. **Custom scripts or a direct run.** For a single process with nothing else
   holding the project, or for an investigator's own hard-linked copy:

   ```sh
   analyzeHeadless <project-dir> LiveR2 -process Live.arm64 -noanalysis -readOnly -max-cpu 4 \
     -scriptPath /home/ollie/Documents/sound/tools/ghidra \
     -postScript R2FunctionDossier.java <fresh-out-dir> 'str:LoopOn' 0x10276e5d4
   ```

Ghidra admits only one process per project at a time. The coordinator's own jobs,
such as bulk decompilation, keep `projects/LiveR2`; the server uses `query/LiveR2`.

## Query tool output

`R2FunctionDossier.java` takes these queries:

- `0x<hex>`
- a symbol name, optionally qualified as `Ns::name`
- `str:<exact value>`
- `@file`, with one query per line

For a function, `functions/<entry>.json` contains:

- body ranges and size, signature, calling convention and thunk target
- callers and callees
- references from the body; a referenced data target gets one hop to the strings
  it points to
- incoming references to the entry
- decompile status (`ok`, `failed` or `timeout`, with a 60 s limit) and warnings
- disassembly with bytes

`functions/<entry>.c` holds the pseudocode. An address inside a function also gets
`refs/<addr>.json`.

Non-function addresses and matched strings produce `refs/<addr>.json`. It lists
the target description and the incoming references to every byte of the
containing data item, up to 4,096 bytes. When a referrer is itself data, the
report adds that item's own referrers, one hop back. References are capped at
10,000 per address, and a cap is reported as truncated.

`queries.json` records each query's matches or error. `manifest.json` lists the
SHA-256 and size of every file. Outputs contain no timings. Two JVM runs, and the
server versus a one-shot run, produced byte-identical files.

## Unknowns and limits

- **Not yet measured on Live:**
  - open time and RSS
  - project size
  - cost of each `str:` query, which scans every defined string
  - queue latency under real request mixes
- **Requests are serial.** A 60 s decompiler timeout can delay other investigators.
- **No retained provenance.** The server does not record which agent asked.
- **Untested string paths.** On Push2, references to C strings arrived directly
  from code. The CFString hop is implemented but no Push2 case exercised it.
- **Static evidence only.** A reference is not proof of runtime execution.
