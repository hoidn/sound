---
id: PLAN-NATIVE-EXPORT-EXECUTION
type: research
status: draft
updated: 2026-10-09
access: analysis
---

# Native export implementation and execution

This is the bounded execution plan for the [controller design](native-export-design.md),
within the [major-phase roadmap](native-decompilation-roadmap.md).

1. Inspect the installed REA lifecycle and record actual heap, timeout and cleanup behavior.
2. Implement one long-lived stdio MCP client with durable command/result spooling.
3. Prove handshake/tool listing without opening a binary; coordinator checks the host resource envelope.
4. Coordinator opens the pinned image, measures auto-analysis and freezes its inventory/profile identity.
5. Implement file ingestion against actual exported evidence, including failure and warning records.
6. Test replay, interruption, corruption and identity rejection; obtain scope then quality reviews.
7. Coordinator runs pilot/batches and publishes measured results and current coverage.

Steps 1–3 and the file-ingestion implementation/tests are complete. Independent
scope and quality reviews passed. The default main-image analysis stopped at its disk floor before returning an
inventory. Separately profiled selected-entry runs now retain fourteen successful
pseudocode exports and six explicit failures across twenty nominated entries
in the initial pilot; the [execution ledger](native-phase-execution.md) records
subsequent follow-up exports and the active full-analysis retry.
Full inventory coverage and cold-recovery measurement remain unproven. Provider-owned analysis and bulk scheduling are coordinator
responsibilities; the file ingestor does not initiate expensive work.

## Implemented transport and ledger

`tools/run_native_analysis.mjs` now owns a single stdio MCP connection. Real
metadata-only smoke capture [v2](../../analysis/ableton-live-12.4.3/native-transport-smoke-v2/initialize.json)
negotiated the protocol, retained 139 tools, executed a spooled tool listing and
exited successfully. The first smoke exposed a log-close race; v2 corrected it.
Subsequent tests cover cancellation, timeout queue stopping and mutated request
replay. The client explicitly removes inherited `HOPPER_TARGET_PATH`, so its
handshake cannot trigger REA's configured initial-target open.

The [installed-source digest record](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/rea-source-inspection-v1.json)
identifies the REA source inspected for lifecycle and profile handling. Source
inspection is separate from measured provider behavior.

The [file ingestor](../../tools/export_native_corpus.py) now initializes a frozen
inventory, ingests full REA records/bundles or spooled MCP result envelopes,
exports function revision directories, and computes coverage. The [integrity
tests](../../tools/tests/test_native_export.py) exercise duplicate aliases,
contradictory classifications, changed inventory, identity/profile mismatch,
null output, partial batch failures, warnings, interrupted staging, payload
corruption and unchanged replay. Seventeen ingestion tests and four [transport
lifecycle tests](../../tools/tests/test_native_transport.py) passed with:

```sh
python3 -m unittest discover -s tools/tests -p 'test_native_*.py' -v
```

These tests use synthetic evidence/fake protocol peers and do not establish
main-image decompilation, cold-analyzer recovery or application compatibility.
Independent scope and quality reviews passed; see the retained [export quality
review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/export-quality-review.json)
and [transport quality review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/transport-quality-review.json).
Main-image operations remain coordinator-owned.

## Coordinator commands

Start a fresh transport spool with:

```sh
GHIDRA_INSTALL_DIR=/opt/homebrew/opt/ghidra/libexec \
JAVA_HOME=/opt/homebrew/Cellar/openjdk@21/21.0.12.1/libexec/openjdk.jdk/Contents/Home \
node tools/run_native_analysis.mjs analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-pilot-v2
```

Publish complete request JSON files by rename into its `requests/` directory.
They use `method: tools/call`, `params: {name, arguments}`, and optional
`timeout_ms`. The coordinator first opens the pinned image, then requests
`list_procedures`; neither happens implicitly. Each request is copied into
`accepted/` with its exact byte SHA-256 before dispatch. Results include the
request identity. A changed completed request is rejected; an accepted request
without a result requires owner reconciliation and a new request ID. Do not
rewrite accepted requests to retry them.

```sh
python3 tools/export_native_corpus.py init \
  --root analysis/ableton-live-12.4.3/native-live-arm64-v1 \
  --evidence PATH_TO_LIST_PROCEDURES_RESULT \
  --target-sha256 3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad
python3 tools/export_native_corpus.py ingest \
  --root analysis/ableton-live-12.4.3/native-live-arm64-v1 \
  --evidence PATH_TO_BATCH_RESULT
python3 tools/export_native_corpus.py queue \
  --root analysis/ableton-live-12.4.3/native-live-arm64-v1 --limit 20
python3 tools/export_native_corpus.py check \
  --root analysis/ableton-live-12.4.3/native-live-arm64-v1
```

`queue` emits pending explicit addresses only. Failed records remain visible;
retrying requires an intentional new attempt rather than an automatic infinite
loop. A changed provider/profile or frozen inventory needs a separately named
corpus revision. Nonexternal inventory entries are eligible even when the list
operation supplies no complete body ranges; body coverage remains unknown.

On a deadline or SIGTERM/SIGINT, the transport cancels pending calls and stops
scheduling; the session is uncertain until reconciled. Shutdown allows three
seconds after stdin EOF, then signals its owned REA server, escalating after six
seconds and bounding the wait at nine. The coordinator's watchdog handles
verified descendant processes and must retain Ghidra logs before cleanup. The
client itself does not discover or kill arbitrary Java processes. Close the
binary and optionally save an REA query snapshot before the `shutdown` spool
request on an ordinary successful exit; a query snapshot is not a saved database.

## Scale and remaining measurements

The initial ingestor verifies all committed payloads and their authoritative
source records when rebuilding coverage. This is deliberately conservative for
the pilot, but repeated full checks after every small batch can grow quadratically
with corpus size. Measure that cost before bulk scheduling. A later checkpoint
optimization must retain full explicit audit mode and verify new commits, rather
than dropping source-integrity checks. Automatic retry scheduling, large-corpus
throughput and cold-provider recovery remain unproven.

The owned REA server initially lacked Ghidra/JDK environment configuration. The
coordinator corrected its launch environment to the paths above and started the
main-image analysis in `transport-pilot-v2`. That attempt subsequently stopped
at its resource floor without returning a function inventory. The configuration correction is a transport/environment finding,
not a decompilation result.

A [synthetic ledger benchmark](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/ledger-benchmark-v1.json)
used 200 functions, 12,000 filler characters per function, and batches of 20.
Full checks grew from 0.013s at 20 committed functions to 0.096s at 200; final
batch ingestion including its check took 0.132s. The benchmark ran at reduced
process priority while main-image analysis was active and deleted its temporary
payloads afterward. It measures ledger mechanics only, with synthetic evidence;
these times are not decompiler throughput or a defensible whole-corpus forecast.
The approximately linear individual checks support the concern about quadratic
cumulative work when repeated after every small batch. Keep the conservative
pilot behavior, then choose checkpoint cadence using real inventory/pilot sizes.

## Qualified address-space correction

Reviewing the installed bridge while main analysis was still running exposed a
format gap: external functions can use `EXTERNAL:0x1` rather than default-space
`0x1`. The ingestor now preserves the space as part of identity, orders offsets
numerically within each space, and rejects unencoded path separators. Percent-
encoded space names remain encoded in filenames. Existing source captures and
corpus records are unchanged. A source-shaped external inventory fixture verifies
that external entries remain visible but never enter the pending decompilation
queue; a null external attempt remains excluded from eligible-attempt counts.
The associated browser uses the same canonicalizer. This is a tooling correction
based on installed provider source, not a newly observed Live function inventory.

Scope review also demonstrated that this corpus volume treats directory names
case-insensitively. Initialization now rejects a pair such as `SPACE:0x1` and
`space:0x1` before any corpus files are written; it never merges their identities.
A single mixed-case space remains supported. This is a declared limitation of
the present literal-directory layout, covered by an additional regression test.

## Conditional fallback preparation

The [selected-entry fallback design](native-export-design.md#conditional-selected-entry-fallback)
is now concrete in [SelectedNativeExport.java](../../tools/ghidra/SelectedNativeExport.java)
and [run_targeted_native.py](../../tools/run_targeted_native.py). It was compiled/reviewed before activation and completed coordinator-owned
selected-entry runs after the default-profile resource stop. The original default-profile attempt and its evidence remain separately retained. [Compilation evidence](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/targeted-compile-v1/compile-report.json)
records successful compilation against installed Ghidra 12.1.4/JDK 21;
[retained provider-source excerpts](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/targeted-compile-v1/provider-sources/manifest.json)
identify the APIs and headless lifecycle inspected for the design.

The driver defaults to preparation only. Its input JSON requires the pinned
`target` path, `target_sha256`, and `seeds`: one to twenty records containing
`address`, `window_bytes`, `source`, and `label`. `source` cites the retained
symbol/location that nominated an entry. Start the eventual pilot with one seed;
an arbitrary label is not proof of its behavior. The output directory must be
fresh and separate from the default-profile corpus.

```sh
python3 tools/run_targeted_native.py --config PATH_TO_SELECTED_SEEDS_JSON \
  --output analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1
```

This command validates identity/configuration and prints the proposed invocation
without starting Ghidra. The coordinator may add `--execute` only after the
current run reaches its defined fallback condition and has stopped. The driver
then imports once with auto-analysis disabled, captures committed per-entry
outputs and writes logs, status and a manifest. It monitors its owned process
group every second, stopping below 3GiB free disk or above 6GiB aggregate RSS.
The whole batch has a 600-second deadline covering import, disassembly, body
construction and decompilation; each decompilation also has a sixty-second limit.
The bounds can abort an entire batch, but previously committed results survive.

Cleanup signals only the owned unreaped child group or a group containing a
previously observed descendant with matching PID/start time. A three-second
termination grace precedes kill escalation. Descendants that detach into a new
session are outside this sampler; the inspected ordinary headless launcher and
Java decompiler use the inherited process group, but hostile/detaching tooling
is not supported. Output is custom selected-entry evidence and cannot be ingested
as fabricated REA records or presented as a complete discovered-function corpus.

Twelve [model/process tests](../../tools/tests/test_native_targeted.py) pass for
configuration bounds, identity/version rejection, default non-execution, failure
retention, manifests, disk-floor handling, owned-group cleanup and PID reuse.
They use synthetic files/mocks and do not validate real disassembly, body recovery
or timeout behavior inside Ghidra. Independent fallback [scope review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/targeted-scope-review-v1.json)
passed, followed by independent [quality review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/targeted-quality-review-v1.json).

The address-space correction separately passed independent [scope review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/address-space-scope-review-v1.json)
and [quality review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/address-space-quality-review-v1.json)
with the combined 31-test export/transport/browser suite.

Fallback scope review tightened closure handling: cleanup now verifies remaining
process-group members after termination/kill before sealing hashes. If ownership
or exit cannot be established, the driver retains `run-status.json` and
`manifest-pending.json` instead of claiming a stable manifest. An orphan created
and detached before any identity sample remains an explicit limitation. Invalid
or truncated per-entry metadata is preserved and reported as invalid; it cannot
prevent the other results and closure status from being recorded. Successful
claims require matching target/profile/method/version plus code, assembly and
body evidence. Java's home and temporary paths are isolated inside the new run
directory, avoiding changes to the installed provider or normal user settings.

## Default-profile stop and selected pilot activation

The default REA/Ghidra analysis stopped on **2026-10-10 at 05:12:52 UTC**, after
approximately 39.5 minutes, when its resource sampler observed 2,169,581,568 free
disk bytes—below the configured 3GiB reserve. This is an observed resource stop,
not evidence that Ghidra cannot analyze this build. No main-image function
inventory or pseudocode was returned by this attempt. The [stop record](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-pilot-v2/RESOURCE_STOP.json)
and [resource log](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-pilot-v2/resource-20261009T213310.jsonl)
retain the actual samples and process list. The sample contains multiple native
decompiler children; Java RSS alone is therefore not total analysis memory use.
Periodic monitoring permits overshoot between samples and is not an OS quota.

The coordinator retained nonbinary temporary metadata/logs, verified no owned
survivors, and removed the abandoned temporary directory. Its duplicate input
was verified against the preserved `derived/Live.arm64`; the [cleanup record](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-pilot-v2/post-stop/cleanup.json)
retains all hashes and before/after free-space observations. The original input,
source captures, stop evidence and archive remain available.

After both fallback reviews passed and cleanup completed, the coordinator
activated one selected entry: `0x10276e5d4`, nominated by the retained
`SNewCompound<ALoopOn>()` symbol, with a 4,096-byte window. The [pilot input](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/targeted-pilot-config-v1.json)
records its exact symbol-source locator; the [selected run configuration](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/run.json)
pins the distinct profile/method/settings. The [first run status](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/run-status.json)
records exit zero, cleanup with no survivors, and 21.36 seconds elapsed. Its
[readable pseudocode](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/functions/0x10276e5d4/pseudocode.c)
is 391 bytes; the recovered body contains 26 instructions over 104 bytes, with
no reported warnings. These are measured selected-entry results under the
restricted no-analysis method, not complete original function/type recovery.

The [second run status](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/run-status.json)
records thirteen exports and six failures among nineteen additional seeds,
22.23 seconds elapsed, exit zero and no cleanup survivors. Five failures reject
non-call transfers outside recovered bodies; one rejects a computed transfer.
They remain explicit failures instead of silently widening the selected windows.
Together, the two runs attempted twenty nominated entries and retained fourteen
pseudocode exports. This denominator describes the selection only; the complete
main-image function inventory, coverage and application compatibility are unknown.

## Thread-pool resource correction for a possible retry

After the resource stop, the coordinator requested a target-free investigation
of JVM processor limits. The [retained probe and installed sources](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/thread-pool-probe-v1/report.json)
show that `-XX:ActiveProcessorCount=2` alone produces a Ghidra default pool of
three: `SystemUtilities.getDefaultThreadPoolSize()` uses available processors
plus one. Adding `-Dcpu.core.override=2` produces a default pool of two. The
actual small JVM probe measured baseline processors/pool as 8/9, processor flag
alone as 2/3, and both flags as 2/2. It imported no target and ran no analysis.

For a coordinator-approved retry, set only the owned process environment:
`JAVA_TOOL_OPTIONS='-XX:ActiveProcessorCount=2 -Dcpu.core.override=2'`.
Installed `ParallelDecompiler.java:94` selects a shared `GThreadPool`, whose
executor initializes from that default; `AutoAnalysisManager.java:83` uses the
same default for its analysis pool. This limits those default pools individually;
it does not impose a total process or memory quota, and explicitly resized pools
can differ. Aggregate owned-process RSS monitoring and the disk reserve remain
necessary. A retry needs its own retained invocation/resource configuration and
new evidence directory; none was launched by this source/probe investigation.
