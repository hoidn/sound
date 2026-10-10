---
id: DESIGN-NATIVE-ANALYSIS-RECOVERY
type: research
status: draft
updated: 2026-10-10
access: analysis
target: Ableton Live 12 Suite 12.4.3 / arm64
---

# Recoverable native analysis after the REA retry

**Execution preparation authorized; target stages not yet run.** The full REA
retry produced usable results and closed with retained observations, but its
native database was ephemeral. On the user's 2026-10-10 continuation, implement
this separately profiled persistent route alongside the
[compact-storage tasks](native-compact-storage.md). First prove actual JVM settings
and synthetic save/reopen behavior, then admit a saved target import and decide
one bounded analysis pass from measured capacity. Installed REA/Ghidra stay
unchanged. The prior owner and descendants were reconciled before this work.

The [phase ledger](native-phase-execution.md) remains authoritative for execution
status; the [export design](native-export-design.md) defines corpus integrity.
This route needs a new profile, provisionally
`ghidra-persistent-bounded-analysis-v1`. Its records are custom headless evidence,
not REA evidence IDs or additions to the existing default-profile denominator.

## What failed, and what the installed tools support

**Observed:** the [launch correction record](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/launch-pool-correction-v1/report.json)
and actual JVM diagnostics show that REA 6.3.0 cleared the intended CPU options.
Its POSIX launcher constructs JVM arguments directly; setting another shell-only
variable cannot repair that path. It also imports with `-readOnly -deleteProject`.
Query exports survive separately, but the analysis database is not a checkpoint.
The correction record's installed-source and retained-copy hashes were rechecked
for this design and matched.

**Source-supported:** installed Ghidra 12.1.4's standard `analyzeHeadless` script
appends `GHIDRA_HEADLESS_JAVA_OPTIONS` after launch-property defaults. It accepts
`-max-cpu 2`; `HeadlessOptions.setMaxCpu` sets `cpu.core.limit=2`. The explicit
`-Dcpu.core.override=2` is also necessary for two default workers per pool; the
[isolated pool probe](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/thread-pool-probe-v1/report.json)
measured the processor-only setting as three. Neither setting limits all threads,
all pools together, or total memory.

Ghidra documents `-import ... -noanalysis` for an import without auto-analysis and
`-process Live.arm64` for an existing program. Omitting `-readOnly` and
`-deleteProject` permits saving. `-analysisTimeoutPerFile 900` cancels analysis
cooperatively and permits completed analyzer results to be saved. It does not
bound import, scripts, saving, or an analyzer that fails to cooperate.

Three source details affect the design:

- `HeadlessAnalyzer.java:1047–1069` calls `reAnalyzeAll(null)` on ordinary
  processing. Reopening preserves database facts; it does **not** resume the
  interrupted analyzer queue at its former instruction or analyzer position.
- `HeadlessAnalyzer.java:1121–1129` starts an additional untimed analysis pass
  after post-scripts when analysis remains enabled. The proposed outcome script
  must first call `enableHeadlessAnalysis(false)`, then capture
  `analysisTimeoutOccurred()` and return without editing the program. These are
  the actual installed `HeadlessScript` APIs; the README's timeout-query method
  name is outdated. If that script fails to load, it cannot suppress this branch;
  the controller must reject the stage and stop it as described below.
- `HeadlessAnalyzer.java:968–973` catches script load/constructor/provider
  exceptions and can return the incoming `CONTINUE`. Starting B with analysis
  enabled would therefore bypass a missing gate. Start **every** stage with
  `-noanalysis`; only a successfully running gate in B may enable analysis after
  receiving the controller's verified acknowledgment. Execution failure of an
  instantiated `HeadlessScript` returns `ABORT` at lines 950–955, but that does
  not cover script-loading failure.

## Exact launch route and verification gate

The following is a **command specification**, not a ready-to-run tool. The named
gate/outcome/export scripts and owned controller must be authored, compiled and
independently reviewed first. Create the project, home, temporary, log and script
directories inside a fresh recovery root. Refuse an existing root, symlinks,
whitespace in JVM property paths, and a changed target hash. Target SHA-256:
`3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.

```sh
RECOVERY_ROOT=/Users/ollie/sound/analysis/ableton-live-12.4.3/native-persistent-v1
RECOVERY_GHIDRA=/opt/homebrew/Cellar/ghidra/12.1.4/libexec
RECOVERY_JDK=/opt/homebrew/Cellar/openjdk@21/21.0.12.1/libexec/openjdk.jdk/Contents/Home
RECOVERY_TARGET=/Users/ollie/sound/analysis/ableton-live-12.4.3/derived/Live.arm64

recovery_headless() {
  env -u JAVA_TOOL_OPTIONS -u _JAVA_OPTIONS -u GHIDRA_JAVA_OPTIONS \
    JAVA_HOME="$RECOVERY_JDK" \
    PATH="$RECOVERY_JDK/bin:/usr/bin:/bin:/usr/sbin:/sbin" \
    JDK_JAVA_OPTIONS="-Duser.home=$RECOVERY_ROOT/home -Djava.io.tmpdir=$RECOVERY_ROOT/tmp" \
    GHIDRA_HEADLESS_MAXMEM=4G \
    GHIDRA_HEADLESS_JAVA_OPTIONS="-XX:ActiveProcessorCount=2 -Dcpu.core.override=2 -Duser.home=$RECOVERY_ROOT/home -Djava.io.tmpdir=$RECOVERY_ROOT/tmp" \
    "$RECOVERY_GHIDRA/support/analyzeHeadless" "$@"
}

# A: import baseline; no whole-program auto-analysis.
recovery_headless "$RECOVERY_ROOT/work" LiveRecovery \
  -import "$RECOVERY_TARGET" -noanalysis -max-cpu 2 \
  -scriptPath "$RECOVERY_ROOT/scripts" \
  -preScript RecoveryLaunchGate.java "$RECOVERY_ROOT/import-gate.json" verify-only "$RECOVERY_ROOT/import-ack.json" \
  -log "$RECOVERY_ROOT/logs/import.log" \
  -scriptlog "$RECOVERY_ROOT/logs/import-script.log"

# B: one analysis pass on a disposable working copy of the verified baseline.
recovery_headless "$RECOVERY_ROOT/work" LiveRecovery \
  -process Live.arm64 -noanalysis -max-cpu 2 -analysisTimeoutPerFile 900 \
  -scriptPath "$RECOVERY_ROOT/scripts" \
  -preScript RecoveryLaunchGate.java "$RECOVERY_ROOT/analysis-gate.json" enable-analysis-after-ack "$RECOVERY_ROOT/analysis-ack.json" \
  -postScript RecoveryAnalysisOutcome.java "$RECOVERY_ROOT/analysis-outcome.json" \
  -log "$RECOVERY_ROOT/logs/analysis.log" \
  -scriptlog "$RECOVERY_ROOT/logs/analysis-script.log"
```

The wrapper isolates Java's home/temp for LaunchSupport as well as Ghidra; it does
not repurpose the user's `HOME`. Installed `launch.sh` uses LaunchSupport to select
a JDK and save its selection, so `JAVA_HOME` alone is not proof of the final JVM.
Record the resolved executable, version, complete argv and effective properties.

Before A, exercise the exact standard-shell launch and gate with a tiny synthetic
analyst fixture in a separate project. Before B, reopen the saved target with
`-process Live.arm64 -noanalysis -readOnly` and the same gate. These tests are
**planned**, not covered by the earlier standalone pool probe or selected export.
Every launch must own one process group and bind PIDs to creation identities.
Capture `jcmd <owned-java-pid> VM.command_line`, `VM.flags`, and
`VM.system_properties` with short deadlines. Do not attach to a historical PID.

The in-JVM gate must retain and require: Ghidra 12.1.4, the selected JDK, target
hash and arm64 language, `Runtime.availableProcessors()==2`,
`SystemUtilities.getDefaultThreadPoolSize()==2`, `cpu.core.override=2`,
`cpu.core.limit=2`, the effective 4 GiB maximum heap, and isolated home/temp paths.
External JVM flags must independently show `ActiveProcessorCount=2` and the heap
limit. The gate starts by disabling analysis and setting
`HeadlessContinuationOption.ABORT`. It writes its checked in-JVM record, then
waits at most ten seconds for an atomic controller acknowledgment. That
acknowledgment must match a fresh run/stage nonce, target hash, gate-record hash
and the current JVM PID/creation identity, and attest that the external command,
flags and properties passed. A stale acknowledgment or elapsed time is not
approval. Only after matching acknowledgment may B's gate explicitly call
`enableHeadlessAnalysis(true)`. Every successful mode then finishes with
`CONTINUE`; `verify-only`, used by import, reopen and export with fresh per-stage
record/acknowledgment paths, leaves analysis disabled. The controller must
also retain a positive gate-completion milestone; a missing/load-failed gate can
neither start analysis nor produce an accepted checkpoint, even if headless
saves the unchanged program and exits zero.

Missing or contradictory records fail the stage. The external watchdog is
active from process creation, including import before its pre-script runs.
On `REPORT SCRIPT ERROR`, an explicit gate/outcome error, or missing required
milestone, close the queue and stop the owned process promptly. After the
analysis-completed or analysis-timeout log milestone, allow at most ten seconds
for a valid outcome record. An outcome-script load failure may enter the untimed
post-analysis branch **before** the controller observes the failure. This design
does not claim to prevent that work completely: the external 1,200-second hard
deadline and resource stops remain active, the error triggers earlier shutdown,
and the resulting working tree is never accepted as a checkpoint. Normal
successful outcome-script execution disables that additional pass. Do not treat
a zero exit, a save log, or an outcome record alone as sufficient stage success.

## Persistence, checkpoints and exported artifacts

1. **Save the import baseline.** Give A a 600-second external deadline. Require
   a successful save log, clean process-tree closure, and a separate read-only,
   no-analysis reopen proving program identity. After closing that check, move
   the project directory into the baseline revision and hash its `.gpr` file and
   entire `.rep` tree; create the next working copy from that baseline. Do not
   copy or seal an open database. An imported program is not an analyzed program.
2. **Run one bounded analysis stage.** Start B only from a copy of that baseline.
   Allow 900 seconds of cooperative analysis and at most 1,200 seconds total
   including startup, outcome script and save. Retain timeout status separately
   from process exit. A cooperative timeout can yield a **partial** checkpoint
   after successful save, close, hash and read-only reopen. A kill, failed save,
   failed/missing gate or outcome record, any script-load error, or failed reopen leaves an unverified working tree;
   retain its failure evidence and use the last verified baseline for recovery.
3. **Export without reanalysis.** On a disposable working copy of a verified
   analysis checkpoint, run `-process Live.arm64 -noanalysis -readOnly -max-cpu 2`, the launch gate,
   and a separately reviewed custom export script. First stream an inventory
   with address-space identity, external/body classification and counts. Bind
   that snapshot to the checkpoint manifest and analysis outcome. Label a
   timed-out snapshot partial; never call it a complete default-profile inventory.
   Export one function, then batches of five, with a 60-second decompiler deadline
   per function and a 600-second whole export-stage deadline. Commit each outcome
   independently; retain warnings, nulls and failures. Do not recreate a body
   merely to convert a failed export into success under this profile. Recheck
   the sealed source checkpoint hashes afterward; read-only processing may still
   create project locks, so do not open the immutable checkpoint itself.
4. **Choose the next stage from evidence.** Compare analyzer logs, saved function
   counts, exported outcomes, peak resources and elapsed times. If timed out,
   retain the partial checkpoint and investigate the specific blocking analyzer.
   Do not loop ordinary `-process` calls and describe that as queue resume. Any
   changed analyzer options require a new profile and checkpoint lineage. Keep
   the already available selected-entry and linker metadata views accessible.

The live working project is mutable. Captured methods, inputs, closed checkpoints,
logs and exported evidence are separately revisioned and hashed. A complete
checkpoint requires actual reopen evidence, not merely `.gpr` file presence or
a zero process exit code. Protect the baseline from cleanup; do not remove lock
files or recovery records to force access to a project still owned by a process.

## Resource admission and stop conditions

These are **proposed conservative budgets**, not measurements of database size.
Use the reviewed monitor's one-second aggregate-owned RSS policy: stop after two
successive samples above 6 GiB, with a 4 GiB Java heap and immediate stop below
3 GiB free disk. Retain logs every 30 seconds and on a stop. Resource observations
include all owned native decompiler children; pool sizing is supplementary.

Before A require at least 6 GiB free disk and allocate at most 2 GiB to its new
project/home/temp/log tree. Measure the closed baseline size `B`. Before B require
free disk of at least `max(12 GiB, 2*B + 8 GiB)`, measured **after** retaining the
baseline. This reserves a working copy and a new checkpoint (`2*B`), up to 2 GiB
of database growth in each (`4 GiB`), 1 GiB for temporary files/logs, and the
3 GiB floor. Count copies at full allocated size; do not assume APFS clones,
compression, or purgeable space is available. The full database may exceed this
budget; that is a stop and capacity finding, not authorization to delete evidence.

The controller additionally stops B if working database growth exceeds 2 GiB or
new temporary/log allocation exceeds 1 GiB. If capacity is insufficient, stop
before starting B and retain the baseline; continue using existing bounded
exports while storage is resolved. Never delete unrelated files or silently
prune older evidence to pass admission. Recheck space before checkpoint copying
and each export batch; admit export only when a full working copy plus the
planned output allowance fits above the floor. Physical RAM, swap and memory-pressure readings are
recorded too; RSS excludes compressed/swapped memory and does not promise host
responsiveness. Halt if the coordinator observes renewed sustained host pressure.

On any deadline, failed JVM gate or resource stop: close the work queue, capture
logs and samples, request shutdown, then escalate TERM/KILL only against the
still-matching owned PID/creation identities. Do not wait indefinitely for a
save past the resource floor. Record all survivors; no next stage, checkpoint
seal or cleanup while ownership/closure is unresolved. Never run alongside the
active REA analyzer or another writer to the project.

## Delivery and review gates

The next authorized preparation task is the small owned driver plus three analyst
scripts described above. Preserve exact source copies and command arrays; compile
against the installed API; test ineffective JVM settings, gate load/constructor/
execution failures, absent/stale/mismatched controller acknowledgments, outcome
load failures, missing outcome milestones, timeout reporting, successful-script
suppression of post-script analysis, failed saves, interrupted
copies, PID reuse, low disk and malformed export records. Exercise the synthetic
save/reopen/timeout path before the target. Obtain independent scope and quality
reviews, then let the coordinator run A and decide B from its measured admission
gate. This design alone does not establish a working persistent export pipeline.

## Source locators and review record

The launch correction record linked above pins REA's `GhidraInstallation.js:262–270`,
`GhidraJavaLaunch.js`, `GhidraLauncher.js:238–243,324–335`, Ghidra's shell scripts,
and `HeadlessOptions.java:497–500`. The following additional installed sources
were inspected read-only; capture their exact bytes with the future method.

| Source in Ghidra 12.1.4 | Exact locator | SHA-256 |
| --- | --- | --- |
| `support/analyzeHeadlessREADME.md` | `-process`, `-readOnly`, `-deleteProject`, `-noanalysis`, `-analysisTimeoutPerFile`, `-max-cpu` | `7c652d030b02b89f23c4853eafbaec51fa2eef5cc8243def5cc704cb78c4b7c2` |
| `Ghidra/Features/Base/lib/Base-src.zip` | Archive containing the two members below | `4c51fc79a73ac7187fb5138a16b1952040585df9599cd50546c35fbc37e05627` |
| `ghidra/app/util/headless/HeadlessAnalyzer.java` | Lines 915–973, 1008–1135, 1183–1227, 1586–1629: script-loading failure, pre-gate, timeout, extra analysis, processing/import save | `3351b9aae4519b61bfae2cd8cc40cc78912cb63135041b4054c5f638f350b299` |
| `ghidra/app/util/headless/HeadlessScript.java` | Lines 202–203, 240–243, 384–386: explicit abort, disable analysis, actual timeout API | `422cbfe4be0f4e0b0079ba929429ac60ef7b77c6a47fa6a83a5389d804f0e31f` |

**Review performed:** canonical execution/export pages, retained launch correction,
current installed launch sources, documented command syntax, headless save/timeout
control flow and source hashes. **Not performed:** a new JVM probe, synthetic
headless execution, target import/analysis, persistence demonstration, tooling
installation, provider edits, or application implementation. Root owns the index,
phase ledger and shared investigation log updates for this proposed route.


## Continuation preparation audit

The [revision-2 preparation packet](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-preparation-v2/preparation-report.md)
retains exact installed API sources, concrete driver/script interfaces and
synthetic failure cases. Its [manifest](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-preparation-v2/manifest.json)
was verified after capture. The audit establishes feasibility against those
source versions; it did not launch a JVM or target.

The inventory exporter must combine ordinary and external function iterators
and reconcile their sum with the reported function count. Read-only processing
can change project bookkeeping; reopen/export disposable full copies and check
the sealed source afterward. A deterministic timeout test needs a fixture-only
analyzer that receives and polls the timed cancellation monitor. All three
points have exact retained source locators in the packet.

The prior design review pins an earlier page version. The packet preserves the
current page and an explicitly reconstructed prior page; reversing only the
activation paragraph/date edits reproduced the original review hash. This does
not extend the prior review to new implementation or this page's current hash.
Actual compilation, handshake, save/reopen, timeout and target results remain
pending.
