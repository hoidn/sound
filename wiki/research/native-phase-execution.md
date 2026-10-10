---
id: PLAN-NATIVE-PHASE-EXECUTION
type: research
status: current
updated: 2026-10-09
access: analysis
target: Ableton Live 12 Suite 12.4.3 / arm64
---

# Native phase execution design and task plan

The user authorized drafting associated designs **and executing** the
[next-phase roadmap](native-decompilation-roadmap.md) on 2026-10-09. This page
records the executable sequence, ownership and actual gate dispositions. It
covers analyst tools and evidence; it authorizes no clean candidate implementation
in this shared analyst checkout. Main Live pseudocode is the first output.

## Operational design

Root owns one native provider process/session. An owned local REA stdio client
will use the already installed REA 6.3.0 with explicit process environment:
`GHIDRA_HEADLESS_MAXMEM=4G`, `REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000`,
`GHIDRA_INSTALL_DIR=/opt/homebrew/opt/ghidra/libexec` and the installed
OpenJDK 21 `JAVA_HOME`. The first open rejected missing Ghidra configuration;
that failed capture was retained and closed before the configured retry. The connected
chat REA session is closed and idle; it will not open a competing target. The
transport must pass a real `initialize`/`tools/list` round trip before native work.
The client stores request IDs, operation names and response envelopes locally;
recovered text is data, never executable instructions. No package installation
or server-registration change is required.

Installed provider source establishes an ephemeral read-only import with
`-deleteProject`, not durable native-database persistence. Increasing the startup
timeout gives the single main-image analysis a bounded opportunity to complete;
it is not proof that one hour is sufficient. Source references:
`dist/config/environment.js`, `dist/ghidra/GhidraJavaLaunch.js`, and the installed
`bridge/ghidra/ReaGhidraBridge.java`, under `/opt/homebrew/lib/node_modules/rea-agents`.
Capture relevant source hashes with the run. The current provider decompiler
has no per-function deadline, so monitor progress and isolate problem items;
do not claim independent function timeout/resume support.

## Resource envelope before analysis

Preflight observed 16 GiB physical RAM and approximately 8.3 GiB free disk.
Record precise fresh values in `native-live-arm64-v1/preflight/host.json`.
The initial run used one provider, a 4 GiB Java heap, a 6 GiB Java RSS
threshold and a 3 GiB free-disk floor with 30-second samples. It stopped at
the disk floor after 39.5 minutes without returning an inventory.

The retry uses the same heap and disk floor, but samples the aggregate RSS of
the controller and all owned descendants every second, stopping above 6 GiB
for two consecutive samples. Provider log capture remains every 30 seconds
and on a stop. The user freed disk space; record fresh capacity before retry.
Set `JAVA_TOOL_OPTIONS=-XX:ActiveProcessorCount=2 -Dcpu.core.override=2`
only for the owned process tree. The retained
[pool probe](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/thread-pool-probe-v1/report.json)
observed a default Ghidra pool size of two with both settings, versus nine
without them. This is a per-pool limit, not a total-process bound. A sustained memory excess across two samples or a disk-floor breach
stops new work, retains available logs/checkpoints and terminates only owned
analysis processes if graceful shutdown cannot finish. Do not clear unrelated
files to make space. Capture provider logs before normal ephemeral cleanup.

Initial analysis deadline: 60 minutes. Start export with one function and then
batches of five after success. Measure initialization independently of export.
Checkpoint every completed batch. Flag a nonresponsive export after five minutes
for investigation; a quiet log alone does not prove a hang. Repeated unchanged
retries are prohibited. Exceeding the envelope leaves the affected milestone
incomplete, with retained evidence and a concrete recovery requirement.

## Plans and work products

| Stream | Design / task ownership | Delivery |
| --- | --- | --- |
| Export pipeline | `native-export-design.md` and `native-export-execution.md`; tooling author, root transport owner | Owned transport, evidence ingestor, inventory/coverage, immutable function files and meaningful tests |
| Teaching and program structure | `learning/design-and-plan.md`; documentation author | Reading route, method/glossary, worked evidence narratives and program atlas |
| Browser | Existing `tools/build_artifact_browser.py`; separate scoped author after corpus format settles | Native function search/pages, warnings, failure states, source links and direct-file fallback |
| Behavior packets | [Transport study](native-transport-study.md); root plus independent trace/spec workers after real native outputs | Persistence/transport evidence packets, case fixtures, bounded contracts |
| Handoff | Separate reviewer after finite spec selection | Sanitized self-contained release, checksums and remaining comparison obligations |

Proposed paths in this table become links when the files exist. Source captures,
reviewed planning snapshot and existing checksum inventories stay immutable.
Generated view files are replaceable; captured provider outputs are versioned.

## Execution sequence

1. **Design and preflight.** Capture input identity, host resources and provider
   source settings. Draft the export and learning designs before their changes.
   Validate transport against read-only metadata. Root reviews design boundaries.
2. **First main analysis.** Open the retained main arm64 slice through the owned
   transport. Trigger one procedure inventory; retain source identity, profile,
   diagnostics and actual result. If MCP transport rejects an oversized response,
   export the existing evidence ledger rather than rerunning the inventory.
3. **Pilot source.** Resolve the known transport/song/clip/device factory seeds
   against the actual inventory. Export a deterministic twenty-function pilot,
   beginning with one. Store raw evidence and per-function pseudocode/metadata.
   Measure errors, warnings, sizes and elapsed times; do not call factories
   behavioral implementations merely from their names.
4. **Reliable ingestion.** Run tests for identity/profile mismatch, null/error
   results, duplicate aliases, corrupt/missing outputs, interrupted atomic writes,
   re-ingestion and inventory change. Use independent scope review followed by
   quality review; fix material findings. Demonstrate an interrupted controller
   can resume committed files. Record that killing the provider loses its DB.
5. **Readable delivery.** Publish pilot links immediately. Build the first-code
   walkthrough and initial atlas using actual observed code/evidence. Add native
   pages to the browser and check actual navigation, escaping and text fallback.
6. **Systematic export.** Freeze inventory revision and classify every row.
   Process explicit batches of remaining eligible functions under the resource
   envelope. All rows require an outcome; failures remain failures. Report
   progress, latency, free disk and checkpoint state. Do not claim main-image
   completeness while items remain pending.
7. **Behavior and teaching.** Trace one persisted transport field and one transport
   transition using retained code plus focused native queries. Produce two
   evidence packets and linked walkthroughs; include an uncertainty/failed
   hypothesis lesson. Update the atlas in the same change as each finding.
8. **First handoff.** Prefer the supported minimal persisted transport subset;
   use the roadmap's explicit MIDI fallback only if a useful native subset cannot
   be supported. Independent review removes recovered code/internal architecture,
   validates fixtures and checks links/hashes outside analyst directories. No
   clean implementation is delegated to this unrestricted checkout.
9. **Closure.** Update source/research/spec indexes, coverage, questions and log;
   run wiki/evidence lint and publish the phase report. Report unmet gates and
   empirical unknowns without relabeling partial delivery as phase completion.

## Gate ledger

| Gate | Current state | Evidence needed |
| --- | --- | --- |
| Design/preflight | Passed; aggregate monitor scope/quality reviews passed | Design pages, input digest, resource limits and metadata transport round trip |
| M1 Main analysis/pilot | Selected pilot exported 17 of 24 entries; seven explicit failures; full inventory unavailable | Identified main functions and actual exported pseudocode |
| M2 Reliable export | REA importer reviewed with 31 tests; selected route exercised with sealed manifests; default corpus recovery pending | Scope/quality reviews, tests, recovery demonstration |
| M3 Systematic export | Not started | Frozen inventory with all eligible functions attempted |
| M4 Browser | Both views scope/quality reviewed; 20 browser tests pass; real-browser rendering unverified | Human navigation/filter checks and working text fallback |
| M5 Behavior/teaching | Method, atlas and bytecode lesson reviewed; two native lessons written, reader review pending | Two native packets, walkthroughs and reviewed atlas |
| M6 Handoff/report | Finite MIDI configuration candidate being drafted; no release yet | Released finite contract plus honest coverage report |

This ledger must be updated with actual results. Runtime compatibility is unknown
until comparison evidence exists, regardless of export or documentation success.

## Execution evidence

The full-analysis evidence root is [native-live-arm64-v1](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/).
Preflight retains host/input identity, installed-provider source references,
transport review and exporter review. `transport-pilot-v2` retains the owned
requests/results, resource samples and bounded provider-log captures. The inventory request stopped at the disk floor; its failed response and
`RESOURCE_STOP.json` are retained. No inventory or pseudocode was returned by
that run. Owned processes were reconciled with no survivors and ephemeral
input cleanup was recorded in `transport-pilot-v2/post-stop/cleanup.json`.

A separately reviewed bounded route, `ghidra-selected-entry-noanalysis-v1`,
then ran three batches: [v1](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/run-status.json),
[v2](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/run-status.json),
and [v3](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/run-status.json).
It exported 17 pseudocode files across 24 selected entries; seven failed body
validation. Each run retains assembly, metadata, method, resource samples,
cleanup result and a checksum manifest. These are selected-entry results,
not a discovered inventory or default-profile corpus. The three manifests
were independently verified (27, 75 and 35 files respectively).

The additional capacity and reduced pool size justify one full-analysis retry
with a new spool and resource record; the previous failure remains immutable.
The retry is active in `transport-retry-v3`: target open succeeded and one
full-inventory request is in flight.
[Retry preflight](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/retry-v3.json)
pins 12.1 GiB available disk, scoped CPU settings, tooling and review hashes.
[Monitor scope](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/monitor-aggregate-scope-review-v1.json)
and [quality review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/monitor-aggregate-quality-review-v1.json)
passed before launch. The historical sample replay does not establish that
this policy would have prevented the earlier disk stop.

The browser at `browse/index.html` is a regenerated view of committed evidence.
It will be refreshed at each exported batch/checkpoint; existing `#python` links
remain stable. Learning and program-map links are added alongside native code.
A refresh reflects the last generation, not live process state.
