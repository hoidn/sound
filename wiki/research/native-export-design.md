---
id: DESIGN-NATIVE-EXPORT
type: research
status: current
updated: 2026-10-09
access: analysis
---

# Native export controller design

This analyst tool implements the mechanical export portion of the
[phase roadmap](native-decompilation-roadmap.md). It does not implement the
independent application or interpret recovered behavior.

## Transport and ownership

One coordinator owns one REA process and its Ghidra session. A Node stdio MCP
client starts the installed REA entrypoint once, performs the MCP handshake,
retains the actual tool catalog, then executes sequential file-spooled requests.
Each request/result is retained under a unique immutable identifier; no process
is started per function. Investigators read these exports and queue requests
through the coordinator. The client has no implicit analysis operation.

The installed REA 6.3.0 source establishes the initial configuration:
`REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000`, `GHIDRA_HEADLESS_MAXMEM=4G`.
`dist/config/parseConfig.js:49` maps the former; `GhidraJavaLaunch.js` selects the
latter before its default 2G heap. `GhidraLauncher.js` imports with `-readOnly`
and `-deleteProject`, retaining `ghidra.log` and `script.log` only for the session.
`GhidraClient.js` removes runtime artifacts on close. Logs must be captured before
cleanup. Cold restart reimports/reanalyzes; file-ledger resume does not preserve
a Ghidra database. These are inspected code properties, not measured main-image
capacity. Source provenance will be retained with the actual run.

The Java bridge `decompile()` supplies timeout zero and serializes operations.
Client cancellation can destroy the ephemeral database. Use explicit bounded
batches, preserve completed outputs immediately, and treat timeout recovery as
a session event. A root-owned watchdog enforces disk/memory limits; this client
reports transport errors but does not guess which system processes are safe to
kill. Initial budget: Java heap 4GiB, aggregate owned-process RSS 6GiB, disk stop at
3GiB free; coordinator must set/monitor these before launching analysis. Java RSS
alone misses native decompiler children. Following the first resource stop,
[target-free source inspection and a JVM probe](native-export-execution.md#thread-pool-resource-correction-for-a-possible-retry)
established that owned `JAVA_TOOL_OPTIONS='-XX:ActiveProcessorCount=2 -Dcpu.core.override=2'`
sets the default Ghidra pools to two workers each. The processor flag alone yields
three. Pool sizing supplements the resource monitor; it is not an OS quota.

## Corpus integrity

The file ingestor consumes retained REA evidence JSON, never the chat `tools`
object. Its run configuration pins target SHA-256, architecture, provider and
analysis-profile digest. A frozen inventory retains all original rows and
canonicalizes addresses for deduplication. Default-space `0x1` and qualified
`EXTERNAL:0x1` remain distinct identities. Qualified spaces use REA
`GhidraInventoryValues.js` syntax (`[A-Za-z0-9._~-]` or uppercase percent-encoded
bytes); keep them encoded in filesystem components. Never decode `%2F` into a
separator. Sort by space name then numeric offset, with the default space first.
This matches the installed bridge
`ReaGhidraBridge.java::canonicalOffset` (line 3015) and `encodeAddressSpace`
(line 3105); `procedures()` includes external functions (lines 1563–1570).
The current literal-directory layout rejects case-distinct addresses whose
complete path components collide under case folding (for example `SPACE:0x1`
and `space:0x1`), before retaining inventory or writing function files. This
explicit limitation protects case-insensitive corpus volumes; a future path
encoding revision is needed to admit both safely. A single mixed-case space
keeps its original case. Aliases do not enlarge the denominator.
Explicit external or empty-body records are excluded with reasons; missing body
metadata alone is not an exclusion.

Each accepted result retains its full source evidence and exact record locator.
Pseudocode is emitted unchanged as UTF-8. Null results/errors become failed
attempts; warnings remain visible. A unique revision directory contains metadata,
pseudocode where available and a checksum manifest. Directory rename commits a
whole revision atomically. Replaying the same evidence is idempotent; a partial
staging directory is never mistaken for committed output. Conflicting committed
bytes, target/profile mismatch and contradictory duplicate addresses stop ingest.
Coverage is rebuilt from verified committed records. No success is inferred from
file presence alone.

## Review and acceptance

Transport is first proven with the installed server handshake and tool listing,
without opening a binary. Main-image calls happen only after coordinator preflight.
Meaningful automated tests cover interruption before commit, unchanged replay,
corrupted payload, identity/profile mismatch, duplicate aliases, failures and
unknown classifications. Separate independent scope and quality reviews precede
acceptance. Main-image provenance and limitations remain in the
[execution record](native-export-execution.md).

## Conditional selected-entry fallback

This is a separately profiled fallback if the default main-image analysis reaches
its coordinator deadline or resource floor. It must not run concurrently with
that analysis or replace its frozen-inventory completion gate. Installed REA
6.3.0 exposes no generic analyzer-options or `-noanalysis` setting: its launcher
uses default analysis and the profile declares `ghidra-default`. Optional NativeAOT
extensions do not provide general analysis configuration.

The installed Ghidra `support/analyzeHeadlessREADME.md` documents `-noanalysis`
(line 287), `-readOnly` (273), and `-postScript` (191). Its
`Base-src.zip::ghidra/app/util/headless/HeadlessAnalyzer.java` gates initial
analysis at line 1043 and post-script analysis at line 1121 on `options.analyze`.
A direct headless script can therefore import once with `-noanalysis`, decode
selected bounded windows, create/update only the selected functions, and call
the decompiler without a whole-program analysis pass. This is source-supported
feasibility, not an executed fallback result.

The proposed `tools/ghidra/SelectedNativeExport.java` and
`tools/run_targeted_native.py` pin a distinct profile and output directory
`native-live-arm64-targeted-v1`. Inputs are at most twenty explicit arm64 entries
with their source locators and windows of at most 65,536 bytes. The default pilot
uses one entry. The Java script uses `DisassembleCommand` with restricted address
sets and `enableCodeAnalysis(false)`; the convenient `FlatProgramAPI.disassemble`
would otherwise allow incremental analysis. Every accepted body must contain
its entry, remain inside its window, avoid overlap with other functions and have
no unresolved/out-of-window non-call control transfer. Reaching a window boundary
is a failure, not silent truncation. Indirect branches remain failures unless a
later profile establishes their targets. Body ranges are recovered in this
restricted context, not asserted original source boundaries.

`DecompInterface.decompileFunction` uses an explicit sixty-second deadline per
entry. The driver bounds the complete batch at 600 seconds and samples its owned
process group every second, stopping below 3GiB free disk or above 6GiB aggregate
RSS. This deadline includes import, disassembly and body construction, which do
not have separate per-entry deadlines. Output retains raw pseudocode, assembly, body ranges,
errors/warnings, target and script hashes, version/settings, and per-file hashes.
These are custom script records, clearly identified as such; they do not invent
REA evidence IDs or share the default-profile ledger. Imported names and seed
labels are retained separately from inferred function structure. This fallback
can deliver a first real pseudocode walkthrough while broad inventory remains
unknown; it cannot count as completion of the default full-inventory export.

Before any fallback launch, compile against the installed Ghidra libraries and
review model tests for limits/identity, entry/window handling, failure retention,
script provenance and process lifetime. Compilation does not import a target.
The coordinator alone decides whether the fallback trigger has occurred.
