---
id: PLAN-NATIVE-PHASE-EXECUTION
type: research
status: current
updated: 2026-10-17
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
in the transport environment. The retained
[pool probe](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/thread-pool-probe-v1/report.json)
observed a default Ghidra pool size of two with both settings, versus nine
without them. This is a per-pool limit in the standalone probe, not a
validated REA launch setting. The active retry later exposed empty
`cpu.core.override` and no `ActiveProcessorCount` in its actual JVM arguments;
nine decompiler workers appeared. Thus the intended pool constraint did not
reach this provider launch. Aggregate monitoring remains the operative guard.
The retained [launch investigation](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/launch-pool-correction-v1/report.json)
establishes that REA clears the requested environment flags before launching
Java. Do not claim this run has two-worker default pools. A sustained memory excess across two samples or a disk-floor breach
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
| M1 Main analysis/pilot | Full inventory retained; 20 default-profile pilot exports saved (16 warned); selected profile remains separate | Identified main functions and actual exported pseudocode |
| M2 Reliable export | Grouped ingestion and immutable exports independently reviewed and exercised; cold database recovery unproven | Scope/quality reviews, tests, recovery demonstration |
| M3 Systematic export | Inventory frozen; two 1,000-entry stages complete; 416,390 eligible entries pending; capacity gate stops further bulk export | Frozen inventory with all eligible functions attempted |
| M4 Browser | Selected, default and declared-start navigation reviewed; 28 browser tests pass; real-browser rendering unverified | Human navigation/filter checks and working text fallback |
| M5 Behavior/teaching | Native packets, profile comparison and shared-helper follow-up reviewed; external native contract unresolved | Two native packets, walkthroughs and reviewed atlas |
| M6 Handoff/report | MIDI fallback handoff released; checkpoint report below records partial native delivery and remaining gates | Released finite contract plus honest coverage report |

Revision 2 gates (adopted 2026-10-17; the [roadmap](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17)
defines them). M1–M6 above remain the revision 1 record.

| Gate | Current state | Evidence needed |
| --- | --- | --- |
| G0.1 Storage | Decided: `/var/tmp/sound-analysis` on the root filesystem; see [Linux paths](native-analysis-recovery.md#linux-workstation-paths--2026-10-17) | Path and measured free bytes |
| G0.2 Evidence | Not restorable from this host: no SSH route to the macOS host is configured. Revision 1 counts remain historical until the tree is copied | Verified copy or recorded loss |
| G0.3 Persistent project | **Passed 2026-10-17.** Import 26 s with `AARCH64:LE:64:AppleSilicon:default`; full default analysis 1:14:30 wall, 14.6 GB peak RSS (24 CPUs allowed, 32 GiB heap, other jobs running); saved project 2.03 GB; cold read-only reopen 2:54, 4.47 GB RSS, executable SHA-256 matches; 418,417 non-external functions, 20,059 thunks, 2,053 external, 452,752 strings. Revision 1's inventory had 418,418 and 2,054; the one-entry differences are unexplained. Evidence: [g03-v1](../../analysis/ableton-live-12.4.3/r2/g03-v1/manifest.json) | Saved project, cold reopen, measured cost |
| C1–C3 Corpus | **C1 and C2 passed 2026-10-17.** Every one of 418,417 eligible Live functions has an outcome: 320,967 exported, 97,387 with warnings, 63 failed; indexes verified ([Live measurements](r2-corpus-tooling.md#measured-on-live--2026-10-17)). Revision 1 had exported 2,028. 15 helper corpora also complete. C3 browsers built for the helpers; the Live browser is being built | Every eligible row has an outcome |
| S1, S2 Static halves | Filed: [transport-state static](transport-state-static.md), [document container static](document-container-static.md). Native halves N1 and N2 in progress via the query server | Draft research pages with evidence |
| S3 Transitions | N3 in progress via the query server, with the x86_64 engine bundle as a symbol donor | Transition table or escalation record |
| S4 MIDI closure | Done: [closure assessment](midi-closure-r2.md), spec revision 2, [midi-config-v2](../../handoff/midi-config-v2/README.md) released | Clause classification |
| H2, H3 Handoffs | Pending | Reviewed releases |
| Phase 4 probe batch | Collecting | Prepared probe records |

The current [combined tool check](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/tool-suite-v2.json)
records 84 passing analyst-tool tests with exact source hashes. These cover
transport, ingestion, selected export, metadata extraction and browser projection,
not original Live behavior.

This ledger must be updated with actual results. Runtime compatibility is unknown
until comparison evidence exists, regardless of export or documentation success.

The [recovery design](native-analysis-recovery.md) specifies a persistent,
separately profiled route if the current retry fails. It is designed, not
implemented or tested. Its saved database would retain completed facts, not
resume an interrupted analyzer queue. The current run must close before any
recovery target launch; actual JVM verification and measured disk admission
remain required.

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

The additional disk capacity and aggregate resource guard support one
full-analysis retry with a new spool and resource record; the previous failure
remains immutable. The intended reduced pool size did not take effect.
The retry in `transport-retry-v3` completed analysis and returned a full retained
inventory. The provider session completed the bounded exports below and then closed with
a retained observation snapshot; no analyzer remains running.
[Retry preflight](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/retry-v3.json)
pins 12.1 GiB available disk, requested CPU settings, tooling and review hashes.
The actual JVM [command capture](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-retry-v3/diagnostics/command-line-v1.json)
and [properties](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-retry-v3/diagnostics/system-properties-v1.json)
show those requested CPU settings were not effective.
[Monitor scope](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/monitor-aggregate-scope-review-v1.json)
and [quality review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/monitor-aggregate-quality-review-v1.json)
passed before launch. The historical sample replay does not establish that
this policy would have prevented the earlier disk stop.

The browser at `browse/index.html` is a regenerated view of committed evidence.
It will be refreshed at each exported batch/checkpoint; existing `#python` links
remain stable. Learning and program-map links are added alongside native code.
A refresh reflects the last generation, not live process state.


## Full-analysis checkpoint

The [completion record](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/analysis-completion-v1.json)
pins the full inventory and analysis log. Ghidra reported 3,016 seconds of
analysis; the inventory request took 3,068,869 ms including startup and delivery.
The query exceeded the 10 MiB MCP response budget, so the coordinator exported
its retained evidence without repeating analysis. That 121,206,515-byte bundle
contains 420,472 distinct discovered entries: 418,418 nonexternal eligible entries
and 2,054 external entries. Local thunks remain eligible and distinct from
externals. Analyzer completion coexists with retained type/address-space errors;
it does not imply complete control-flow or type recovery.

The frozen inventory and [coverage ledger](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/coverage.json)
now exist. All twenty pilot entries exported: four without warnings and sixteen
with warnings. Eighteen original symbol seeds matched exact inventory entries;
the Start/Stop wrapper seeds did not. Their previously observed branch targets
were exact nonexternal entries and completed the twenty-entry pilot, as pinned
by the [resolution](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/pilot-inventory-resolution-v1.json)
and [additions](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/pilot-inventory-additions-v1.json).
No functions were created to force those matches. The reason for the two missing
wrapper entries remains unknown.

Pilot provider calls took 653 ms combined, excluding cold analysis and ingestion.
These small factory/wrapper selections cannot support a whole-program ETA.
The initial per-batch importer repeatedly scanned the full inventory and rewrote
approximately 97 MB of coverage. The reviewed grouped importer now shares one
validated inventory context and writes coverage once per checkpoint; immutable
function revisions still commit independently. The browser starts with attempted
entries and loads the full inventory on request. Storage fit and cold database
recovery remain open gates; neither optimization establishes them.

The [persistent recovery design review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/native-recovery-quality-review-v1.json)
passed after fixing the proposed gate-load failure path. This is a reviewed
contingency design, not a tested replacement for the current ephemeral session.


## Bounded export checkpoint

The first [systematic stage](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/bulk-stage-v1/summary-v1.json)
completed 1,000 previously pending entries in 20 batches of 50, with four audited
ingestion checkpoints. Provider requests took 7.749 seconds combined and
ingestion took 31.109 seconds; these exclude cold analysis, coordination and
browser generation. The final checkpoint measured 23,625,728 additional allocated
regular-file bytes within the corpus and spool. Free disk fell from 10,671,747,072
to 9,582,792,704 bytes during the stage; the larger global change cannot be
attributed to those retained files. Directory allocation is not counted.

After eight focused helper exports and this stage, coverage reached 1,028
default-profile exports: 937 without per-function warnings, 91 with warnings,
417,390 eligible entries pending and 2,054 external entries excluded. A warning-free
export is not a semantic correctness result. This contiguous low-address sample
cannot forecast the whole binary. Subsequent progress must use a separately
admitted stage and fresh resource checks.

The [reviewed method snapshot](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/methods/export-and-browser-v2/manifest.json)
preserves the exporter, browser and tests used for bulk work. Grouped ingestion
received independent scope and quality reviews, including a corrected pre-write
symlink escape. Every successful checkpoint audits committed revisions before
publishing coverage. Browser regeneration follows the writer transaction;
`#python` remains stable, and `#native` opens attempted entries with a lazy full
inventory button. Browser tests include malformed lazy data and stale-snapshot
handling; no real-browser rendering pass was obtained.


## Stratified checkpoint and phase report — 2026-10-10

The separately admitted [stratified stage](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/stratified-stage-v1/summary-v1.json)
selected the midpoint entry from each of 1,000 equal-count strata in the sorted
remaining inventory. Its [admission review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/stratified-stage-v1-quality-admission.json)
verified the selection and corrected the deadline check after filesystem admission.
The earlier stage's methods remain immutable. All 20 new batches and four
checkpoints completed: 779 exports without warnings and 221 with warnings.
Provider requests took 16.808 seconds combined; ingestion took 33.119 seconds.
Additional allocated regular-file storage at its final checkpoint was 22,761,472
bytes. Those timings exclude cold analysis and browser/coordinator work.

Current default-profile coverage is **2,028 exports**, comprising **1,716 without
per-function warnings and 312 with warnings**, with **416,390 eligible entries
pending** and **2,054 external entries excluded**. No per-function failures were
reported in these default-profile batches; selected-profile failures remain in
their separate historical corpus. This is partial export coverage, not recovered
original source, semantic completeness or behavior compatibility.

The [final browser checkpoint](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/browser-checkpoint-2026-10-10-v1/report.json)
independently verified 2,200 input/output hashes, five helper pins, 6,219 local
links, all 420,472 full-index rows and exactly 2,028 initial attempted rows.
`#python`, `#native`, `#selected-native` and `#declared-starts` remain available.
The initial native data is 1,002,291 bytes; the optional full index is 35,274,039
bytes. This was a file/structure check, without browser or JavaScript execution.

The independent [stage and capacity review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/stratified-stage-v1/quality-review-v1.json)
verified all new payloads and that prior payloads were unchanged.
**Capacity decision:** stop systematic expansion at this checkpoint. At final review,
10,650,132,480 bytes were free, leaving about 7.43 GB above the 3 GiB reserve.
The earlier admission decision saw 9,590,841,344 bytes free; the subsequent global
change is recorded separately from retained corpus growth.
Applying the stratified stage's allocation rate to the remaining entries gives
a planning scenario of about 9.48 GB, before unmeasured directory overhead and
unrelated disk movement. This is not a reliable forecast or a proof of inability
to fit. It does not provide sufficient margin to admit full expansion. A larger
durable volume/budget or a separately designed and reviewed compact future
format is required before the next bulk stage; existing captures and manifests
remain intact. Additional sampling is not the default next action.

Delivered work includes the full native inventory, accessible code checkpoints,
reviewed exporter/browser tooling, a method guide, program atlas revision 6,
worked native evidence packets and the immutable
[MIDI configuration handoff](../../handoff/midi-config-v1/README.md). The native
transport packets establish construction, forwarding and record-building evidence;
they do not yet establish the persisted LoopOn field or an external Start/Stop
contract. The MIDI release covers four partial clauses with 54 unexecuted cases.
No isolated candidate workspace or independent application has been built, and
no original-versus-candidate scenario has run.

Next work is to satisfy the durable capacity and cold-recovery gates, resume
only the pending inventory entries under reviewed limits, and resolve the native
packet's named semantic gaps before releasing a native behavioral contract.
The roadmap's whole-corpus and native-contract milestones remain incomplete.


## Session closure

The [closure manifest](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-retry-v3/post-run/manifest-v1.json)
pins a 155,425,925-byte provider-neutral snapshot with 52 reported evidence records,
final logs, resource samples, close/shutdown receipts and owned-process identities.
All five recorded owned processes exited; the transport lock and owned temporary
Ghidra directory were absent at reconciliation. The retained arm64 source digest
was reverified. No unrelated processes or files were removed.

This snapshot preserves observations and cached analysis entries; it is **not**
a persistent Ghidra database or a tested cold decompilation resume. The full retry
record has 5,636 resource samples, minimum free disk 8,353,005,568 bytes and maximum
aggregate owned RSS 4,339,400,704 bytes, with no monitor stop reason. These metrics
exclude independent Python ingesters and do not describe total system pressure.
The session is closed; no unattended export job remains.


## Authorized continuation — 2026-10-10

The user requested continuation after closure. The
[compact storage and durable analysis plan](native-compact-storage.md) sequences
exact archive tooling, offline code access, persistent save/reopen proof and
then new target admission. A fresh
[host/storage record](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/continuation-v1/host-and-storage.json)
reverified target bytes and the absence of an owned analyzer/transport lock.
Free disk remains variable; earlier resource decisions are retained for their
measured states.

The archive tool and corrected execution wrapper passed scope and quality reviews.
The [real mirror](native-compact-storage.md#measured-mirror--2026-10-10) preserves
all original member bytes with measured smaller representation allocation; old
captures remain intact. The [offline reader publication](native-compact-storage.md#measured-reader--2026-10-11)
passed final scope/quality reviews, actual build/check and exact code-byte
checks; the main browser and its stable `#python` anchor were regenerated. The
[canonical plan](native-compact-storage.md#status) records findings and task state.
The later [Read revisions repair](native-compact-storage.md#read-revisions-interaction-fix--2026-10-12)
publishes v2 with final scoped review and one real Chrome interaction check.
It changes navigation, preserves v1 and the archive, and adds no exported code.
The separate persistent-design audit is complete without a JVM
launch; its [preparation packet](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-preparation-v2/preparation-report.md)
defines the controller, scripts and synthetic proof matrix. The
[current recovery revision](native-analysis-recovery.md#loader-matched-profiles--2026-10-12)
now retains actual synthetic persistence/timeout/export proofs and their exact
method lineage. The loader-matched correction passes fresh scope and quality
reviews and the full 198-test tooling suite. Its
[actual Live import/save](native-analysis-recovery.md#corrected-import-passes-reopen-capacity-stop--2026-10-12)
passes; the first disposable reopen is refused before a JVM for insufficient
fresh-launch capacity. Both incomplete target attempts remain sealed, with
positive owned closure. No accepted cold Live database or new pseudocode results.
Next: additional capacity, a fresh original import and accepted reopen proof,
then separately measured bounded-analysis admission. Existing export counts and compatibility statuses do
not change when mirrored or compressed. The
[storage/recovery lesson](learning/walkthroughs/artifact-storage-and-recovery.md)
links the measured payload allocation and explains the separate proof obligations.

## Decompilation to specification status — 2026-10-12

The [default-profile ledger](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/coverage.json)
retains 2,028 code exports out of 418,418 eligible inventoried entries, about
0.485% by function count: 1,716 without warnings, 312 with warnings, and 416,390
pending. This is export coverage, not feature understanding or whole-app progress.
Separate selected-entry evidence does not change this denominator. The
[reader repair](native-compact-storage.md#read-revisions-interaction-fix--2026-10-12)
adds access to the same code, not new decompilation.

Native semantic work has reached bounded factory/callee, transport-wrapper and
record-building findings in the [transport study](native-transport-study.md).
Its load/save, state and timing questions remain unresolved. The
[incoming-register lesson](learning/walkthroughs/incoming-registers.md)
additionally demonstrates why even a warning-free export needs interface checks.
These studies have not yielded a released native behavioral contract.

The broader [MIDI draft](../specs/midi-user-mapping.md) has 13 requirement IDs
and 46 unexecuted acceptance groups. Its [finite release](../../handoff/midi-config-v1/README.md)
approves four explicitly partial clauses for master/cue/crossfader configuration,
with 54 unexecuted static-derived cases. This release comes from the earlier
configuration/documentation and Python-bytecode investigation; it is not the
conversion of the main native corpus into specs. Other feature families have
no released contracts, candidate implementation or compatibility results in the
[coverage matrix](../verification/coverage.md).

The next specification milestone is a finite native behavior contract grounded
in the retained [transport study](native-transport-study.md), after its material
interface/data-flow gaps are resolved. Existing artifacts can support selective
investigation without exporting the whole inventory. Large persistent analysis
still requires changed [disk capacity](native-analysis-recovery.md#disk-cleanup-inventory--2026-10-12)
and accepted cold recovery; saved import alone has not established that milestone.
Tooling and pedagogy are useful deliverables, but do not close native spec coverage.

## Linux workstation provisioning — 2026-10-17

The analysis moved to a Linux workstation: Ubuntu 24.04, kernel 7.0.0-38-generic,
x86_64, 32 logical CPUs, 125 GiB RAM. `/home` (1.8 TiB) had 4.4 GiB free before
and 2.7 GiB after the installs; the root filesystem had 37 GiB free but is not
user-writable outside `/tmp` and `/var/tmp` because `sudo` requires a password.
The [installed source page](sources/ableton-live-12.4.3.md) records the bundle's
new location and the byte-identical re-derivation of both arm64 slices.

Installed without root under `~/.local/opt`, with archive digests verified
against the publishers' published values and pinned in the retained
[provisioning manifest](../../analysis/ableton-live-12.4.3/linux-provisioning-v1/manifest.json):

| Component | Identity | Note |
| --- | --- | --- |
| Ghidra | 12.1.4 (`ghidra_12.1.4_PUBLIC_20260921.zip`, SHA-256 `ddac49f9…d2d4db`) | Same version as the macOS captures |
| JDK | Eclipse Temurin `jdk-21.0.12.1+1` | Same version as the macOS JDK; the system package is a JRE without `javac` |
| REA | `rea-agents` 6.5.0 on Node 22.23.2 via nvm | macOS used 6.3.0; 6.5.0 source inspected 2026-10-17, see [query route](r2-query-route.md#rea-650-cannot-open-a-saved-project); startup deadline now defaults to 330 s |

`rea doctor --provider ghidra` reports the provider available: installation,
headless script, `linux_x86_64` native decompiler and JDK all accepted. Hopper,
IDA and JADX are absent and no agent-client MCP registration was created; the
coordinator and CLI do not need one. The [doctor output](../../analysis/ableton-live-12.4.3/linux-provisioning-v1/rea-doctor-ghidra.json)
is retained.

**Smoke test.** `rea analyze` on the re-derived Push2 slice with an 8 GiB heap
completed in 71.22 s wall with 2.32 GB peak resident memory and reported 13,611
procedures and 14,769 strings, the same counts the macOS pipeline check
recorded in [decompilation preparation](ableton-decompilation-preparation.md).
Retained as [analyze.json](../../analysis/ableton-live-12.4.3/linux-provisioning-v1/push2-smoke/analyze.json)
(evidence `ev_8906461b71a01f3f5d418748146c914915b7ac77fd8f11b086a166e162415baf`).
The ephemeral project left no measurable residue on the root filesystem. This
proves the Linux toolchain reproduces provider inventory counts for a small
target; it does not establish Live analysis duration, storage or any behavior.

**Not present here.** The retained `analysis/` evidence tree from the macOS host
(full inventory, 2,028 default-profile exports, coverage ledger, compact archive
and reader, both incomplete persistent jobs) was not transferred. Every evidence
link in this ledger and its sibling pages is unresolved on this host. The counts
and statuses above remain the record of that work, not re-verified facts.

**Next.** (1) Decide where a persistent Live project lives; see the
[Linux paths](native-analysis-recovery.md#linux-workstation-paths--2026-10-17).
(2) Restore the macOS `analysis/` tree or record it as lost. (3) Fresh
`-noanalysis` import of `Live.arm64`, then measure a full analysis on this host;
the macOS run needed 3,016 s of analysis under a 4 GiB heap and two CPUs, and
those gates should be re-measured rather than reused. (4) Resume the
[transport study](native-transport-study.md) questions against the new project.
No Live import, new pseudocode or compatibility claim was produced today.

### REA analyzer dependencies — 2026-10-17

Installed at user request, without root, under `/var/tmp/sound-tools` on the
root filesystem so `/home` keeps at least 1.5 GB for evidence writes; about
1.1 GB used. Source [`tools/rea-env.sh`](../../tools/rea-env.sh) before `rea`.
Observed: without `JAVA_HOME` and `GHIDRA_INSTALL_DIR`, `rea providers` reports
Ghidra unavailable. Retained outputs and full package digests are in
[`linux-provisioning-v1/rea-analyzers/`](../../analysis/ableton-live-12.4.3/linux-provisioning-v1/rea-analyzers/manifest.sha256).

| Component | Identity | Observed result |
| --- | --- | --- |
| Hopper | 6.4.2 Linux demo `.deb`, 35,755,772 bytes, SHA-1 `e4f79dff…0dc65`, matching REA 6.5.0's pinned values. Launcher SHA-256 `0294ced1…e7ded` is in REA's supported set. Extracted with `dpkg-deb -x`; Ubuntu `libqt6printsupport6t64` 6.4.2+dfsg-21.1build5 added to its `lib/`; linked from `~/.local/share/rea/hopper` | `available` in `providers.json`; no analysis run. Demo limits on Live are unmeasured |
| Node | 24.22.0 linux-x64, SHASUMS256 verified; runs the Node 22-installed REA 6.5.0 | `inspect-sqlite-database` on a scratch copy of `App-Resources/Database/filerefmap.db` (SHA-256 `97b29374…67897`): evidence `ev_8d5e74b0…77b57`, `filerefmap-sqlite.json` |
| rizin | 0.9.1 static x86_64; release digest `9102249a…7e8cf` verified | `execute-rizin-command … iI` on the Push2 slice reported `mach0`, `arm`, 64-bit: evidence `ev_17166e37…5c2b2`, `push2-rizin-iI.json` |
| GNU objdump | Ubuntu `binutils-multiarch` 2.42 tried, then removed | Its BFD has no Mach-O targets (`invalid bfd target` for `mach-o-arm64`), so REA's objdump analyzer cannot read the slices |
| IDA | Not installed | REA needs an `ida-pro-mcp` registration (`REA_IDA_MCP_CONFIG`) and a licensed Hex-Rays installer; neither is obtainable from this host |

Not installed: the Android, browser, packet-capture, signal, firmware and Frida
dependencies. The bundle has no such targets, and Live cannot execute here.
Routing is decided in the [roadmap](native-decompilation-roadmap.md#proposed-sequencing).
