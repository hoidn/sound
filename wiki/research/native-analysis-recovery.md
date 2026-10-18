---
id: DESIGN-NATIVE-ANALYSIS-RECOVERY
type: research
status: draft
updated: 2026-10-12
access: analysis
target: Ableton Live 12 Suite 12.4.3 / arm64
---

# Recoverable native analysis after the REA retry

**Target import proved; checkpoint reopening blocked by capacity.** The full REA
retry produced usable results and closed with retained observations, but its
native database was ephemeral. On the user's 2026-10-10 continuation, implement
this separately profiled persistent route alongside the
[compact-storage tasks](native-compact-storage.md). First prove actual JVM settings
and synthetic save/reopen behavior, then admit a saved target import and decide
one bounded analysis pass from measured capacity. Installed REA/Ghidra stay
unchanged. The prior owner and descendants were reconciled before this work.

The [phase ledger](native-phase-execution.md) remains authoritative for execution
status; the [export design](native-export-design.md) defines corpus integrity.
The initial common profile `ghidra-persistent-bounded-analysis-v1` is historical;
the [loader-matched profiles](#loader-matched-profiles--2026-10-12) distinguish
the target and raw fixture. These records are custom headless evidence,
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

The following is a **command specification**. The owned
[controller](../../tools/run_persistent_native.py) and gate/outcome/export scripts
have revisioned author/review packets and actual target import evidence above.
Fresh target admission remains required. Create the project, home, temporary, log and script
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
    GHIDRA_HEADLESS_JAVA_OPTIONS="-XX:ActiveProcessorCount=2 -XX:+StartAttachListener -Dcpu.core.override=2 -Dcpu.core.limit=2 -Duser.home=$RECOVERY_ROOT/home -Djava.io.tmpdir=$RECOVERY_ROOT/tmp" \
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
`-process Live.arm64 -noanalysis -readOnly` and the same gate. Historical tiny
fixture tests and the final author packet are recorded below; independent
tooling reviews and the target test remain pending. The earlier standalone
pool probe and selected export do not cover them.
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
   no-analysis reopen proving program identity. After closing that check, copy
   the closed project into a fresh checkpoint layout and verify that layout
   through a second disposable read-only reopen. Hash its `.gpr` file and
   entire `.rep` tree before publishing the verified manifest; create the next
   working copy from that baseline. Retain the working and verification copies. Do not
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

## Preparation observations — 2026-10-11

**Observed, historical method revisions:** the first tiny fixture
[failed gate](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/fixture-first-v1/import/stdout.txt)
reported `JDK version mismatch`: the installed runtime is `21.0.12.1`, while the
initial gate expected `21.0.12`. The second fixture's concurrent diagnostics
[failed attaching](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/fixture-first-v2/import/VM.command_line.stderr.txt)
while creating an attach file. The method now requests
`-XX:+StartAttachListener` before concurrent diagnostics. Both failed stages
record closed ownership with no survivors; their trees and logs remain retained.

The later [baseline fixture](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/fixture-baseline-v2/job-result.json)
saved an independently authored eight-byte AArch64 raw program and verified two
disposable no-analysis read-only reopens. The
[finite analysis fixture](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/fixture-finite-v1/analysis/analysis-outcome.json)
then recorded one function, `timeout=false`, analysis disabled and an empty
postpass-counter marker. Its subsequent save/reopens produced a
[fixture checkpoint](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/fixture-finite-v1/checkpoint/manifest.json).
Each launch retains its exact methods in `stage-config.json` and `scripts/`.
Imported native bytes were data for analysis, never executed.

These captures prove their tiny fixture cases under their captured methods.
They are historical because acceptance checks are still changing; they do not
certify the final controller or a Live checkpoint. The final author packet below adds timeout, export and failure-path proofs.
Independent reviews remain required before target A.

## Frozen driver and proof packet — 2026-10-11

The [readable design and CLI guide](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/README.md)
explains each output and the save/reopen sequence. Its
[author report](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/author-report.json)
and [proof matrix](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/proof-matrix.json)
separate actual launches, injected tests and unresolved target questions.
Root checked all 4,766 payload hashes and 11 current source captures against the
[sealed manifest](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v1/manifest.json),
SHA `858df1e141df65d6625d204c22eab2a4d30e891795e51def6249a9a30a1dae2f`.
The controller is pinned at
`e9f20549ff9454f2c2d0967bf3b494b49dc75b25e77a2f84fb94cc84533923ca`.

Observed proofs include 43 final unit tests and actual synthetic save/reopen,
cooperative timeout, ordinary/external inventory and one/five-function exports.
The full suite's 31 Ghidra launches used an earlier Python controller; the
publication replay used a later controller for 17 launches. The final controller
ran three inventory/export launches and one stale-timestamp rejection. All eight
Java sources stayed identical across these suites. Exact method differences and
affected replays are retained; the complete suite was not repeated on the final
controller. No Live checkpoint, runtime behavior or compatibility result follows
from these synthetic proofs.

The job's `.incomplete` guard remains until source integrity checks, all supporting
save/reopen evidence and fallible result publication finish. Its removal is the
final commit action; checkpoint and export readers reject guarded jobs. This
ordering addresses handled publication failures, without claiming power-loss
durability. Ordinary processing still reanalyzes applicable code; the saved
project preserves model facts rather than a resumable analyzer queue.

The sealed [scope review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v1/scope-review.json)
failed on that frozen controller, despite 43 tests and 27 offline checks passing.
It reproduced two blockers:
[initial ownership lookup failure](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v1/results/launch-identity-failure.json)
can leave a termination-ignoring launched child unregistered while cleanup reports
success; an [expired checkpoint commit](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v1/results/expired-checkpoint-commit.json)
can pass because the whole-job deadline is checked only during JVM stages.
These are scoped offline reproductions, not Live failures. The same author is
correcting the controller; the sealed v1 packet remains unchanged. A later
[actual Python startup-cancellation probe](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v2/popen-interrupt-probe/result.json)
also reproduced a child launched before cancellation interrupted its constructor
and before ownership registration. The probe safely killed/reaped that exact
child; no JVM or native target ran. The author is protecting that registration
boundary. Fresh scope and separate quality approval remain required before root
target admission.

## Corrected driver ready for review — 2026-10-12

The [revision-2 guide](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v2/README.md)
explains what each failure taught us and how cancellation now preserves ownership.
The [sealed packet](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v2/manifest.json),
SHA `ce7b00e0d15015a18986f41a375e04c37f0715e238a9d1b7e02d703671a2614b`,
contains 2,635 payloads, all independently rehashed by root. Its final controller
is `c51397efd1d1c06c97826c873d86fb8e667d6491aabeef020101db3c39e375d7`.
All Java sources remain unchanged. Earlier candidates and their successful
replays remain historical, with exact method differences retained.

Observed final proofs include 52 passing tests, nine actual synthetic Ghidra
launches covering import/save/two reopens, finite analysis/save/two reopens,
ordinary/external inventory and one/five exports, plus three actual Python
children cancelled during construction. Each child was registered before
cancellation and safely closed/reaped with its normal signal mask and handlers.
The whole-job guard also rejects expired commit and cancels non-JVM file work;
failed requests cannot write reports into a pre-existing output directory.
See the [author report](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v2/author-report.json)
for exact proof locators, methods and limits. Fresh scope review reproduced a
[paused reporting tail](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v2/results/paused-stage-tail.json):
a real short alarm did not cancel an injected hashing wait after process cleanup
because the guard remained paused. The probe published a late stage report,
retained `.incomplete` and accepted no success; eventual rejection still fails
the whole-job cancellation requirement. The author is correcting that narrow
boundary. The sealed [scope-v2 report](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v2/scope-review.json)
records this failure; its 45 payloads were independently rehashed by root.

## Deadline-boundary correction — 2026-10-12

The [revision-3 guide](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v3/README.md)
explains why process cleanup is the bounded cancellation exception and file
evidence remains cancellable. The [sealed delta packet](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v3/manifest.json),
SHA `a0cf1276b326ebefbc97eb5bd0b3883ba4efe59bd2a991f3554672aec2d272ed`,
contains 253 payloads, all independently rehashed by root. Controller SHA is
`835a8e00f01cb459441ccb048b2a9cb1e82a63d735f204deaffa940b2690b55d`;
Java sources remain unchanged.

Observed author results: 54 tests pass, and the [affected fixture replay](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v3/positive-import-replay/report.json)
passes three actual Ghidra launches: import/save and two disposable read-only
reopens. The [alarm probes](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v3/tail-cancellation-proof/report.json)
cancel delayed post-cleanup hashing and failure reporting at about 0.23 seconds
against a 0.3-second deadline. No late stage result or job success is accepted;
`.incomplete` remains. An interrupted report may be absent and is unverified
evidence. Revision 2's nine-launch workflow and constructor-signal proofs remain
historical evidence under their exact earlier controller. The sealed
[scope-v3 review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v3/scope-review.json)
passes: 54 tests, two independently reproduced alarm probes and offline checks
of the three final fixture stages, checkpoint and whole-job monitor. Root
verified all 42 review payloads. It approves the scope of the direct public CLI
for a first target import, subject to separate quality review and fresh host
admission. The sealed [quality-v1 review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-quality-v1/quality-review.json)
also passes: 54 tests and 22 additional checks, including writer-lock contention,
checkpoint corruption refusal, preflight cancellation and resource boundaries.
Root rehashed all 39 review payloads. These reviews approve the recorded tool
revision and cases; the first actual target attempt below exposed a distinct
target-language assumption.

## First Live import rejected — 2026-10-12

Fresh host, target, installed-method and writer-lock checks admitted one direct
import with analysis disabled. The [sealed execution report](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-execution-v1/report.json)
records Ghidra's Mach-O loader selecting `AARCH64:LE:64:AppleSilicon:default`
at `import/stdout.txt:43`; the gate expected generic `AARCH64:LE:64:v8A` and
rejected `Language mismatch` at line 92. The raw eight-byte fixture had used
BinaryLoader with an explicit generic language, so it did not exercise this
loader choice. The target and fixture need separate pinned profiles; the author
is correcting that assumption before fresh reviews and a new output directory.
The strict gate and original resource budgets stay in force.

The rejected stage lasted 23.640 seconds, with peak sampled owned RSS
1,512,144,896 bytes and minimum observed free disk 7,911,743,488 bytes. Owned
processes were closed/reaped using identity-checked signals, with no ownership
gaps or survivors; root independently checked the retained identities afterward.
The target hash remained unchanged. Effective JVM diagnostic proof was not
reached. No analysis, accepted checkpoint, reopen or new pseudocode resulted.
The incomplete tree and project lock files remain as failed evidence and must
not be reused. [Manifest pins](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-execution-v1/failed-job-pin.json)
retain the 57 failed-job payloads; the execution packet has seven payloads.

## Loader-matched profiles — 2026-10-12

The [revision-4 guide](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v4/README.md)
links exact installed loader sources and explains why compiler name `default`
has different meaning for different languages. The
[source index](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v4/installed-source-index.json)
pins `MachoLoader.java`, `CpuTypes.java`, `ProgramLoader.java`, `AARCH64.opinion`
and both language definitions. These explain the actual failed target loader
selection; the raw fixture did not exercise Mach-O selection.

| Input | New profile ID | Exact language and import route |
| --- | --- | --- |
| Live ARM64 Mach-O | `ghidra-persistent-bounded-analysis-apple-silicon-v2` | `AARCH64:LE:64:AppleSilicon/default`; native loader selection |
| Eight-byte raw fixture | `ghidra-persistent-bounded-analysis-raw-arm64-fixture-v2` | `AARCH64:LE:64:v8A/default`; explicit BinaryLoader |

The [sealed author packet](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v4/manifest.json),
SHA `86f277bc1a55770527361afb4472e54826fedbcaa6392749f56fe6673e89dd6e`,
has 255 payloads independently rehashed by root. Controller SHA is
`5839c52d53c87098a322268db00a01af54d4570e2c9c6001cfec475bf4d03d7a`.
Only immutable profile definitions and config selection change; exact Java
language/compiler checks and all budgets stay unchanged. Author results are
56 passing tests and three actual raw-fixture import/reopen launches on this
revision. Its config-routing proof uses a digest-stubbed inert stand-in and is
not a target runtime proof. The sealed [scope-v4 review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v4/scope-review.json)
passes 56 tests, installed-source agreement, independent profile/hash/routing
checks and offline validation of the three final fixture stages and checkpoint.
It also rejects relabeling a raw checkpoint as target or historical profile.
Root verified all 46 review payloads. The sealed [quality-v2 review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-quality-v2/quality-review.json)
also passes: 56 tests and 18 focused checks; root rehashed all 27 payloads.
The full analyst-tool suite passes 198 tests on this exact controller. Historical
matrices retain their original methods; these reviews add no application
compatibility result.

## Corrected import passes; reopen capacity stop — 2026-10-12

The [second execution report](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-execution-v2/README.md)
records a fresh direct import after both reviews, exact method rehash, host
observations and writer-lock probes. The import stage passes in 24.941 seconds:
the exact AppleSilicon/default language, actual 4 GiB heap, two processors,
two default pool workers and Java 21.0.12.1 are verified and independently
acknowledged through captured `jcmd` output. Save succeeds; owned processes close
normally with no signals, ownership gaps or survivors. Peak sampled owned RSS
is 1,906,294,784 bytes. Root revalidated milestones, copied methods, diagnostics,
process identities and byte agreement of the saved project and its first copy.

The closed working project occupies **345,047,040 allocated bytes**, including
directory blocks once. The first disposable reopen is refused before starting
a JVM: **6,116,376,576 bytes free < 6,442,450,944 required**, a 326,074,368-byte
shortfall. The retained job occupies about 691 MB and contains two project
representations. `.incomplete` remains; the public checkpoint reader rejects it.
The import-stage function count is 3,639 with analysis disabled; it is not the
default-profile analyzed inventory denominator. No reopen, accepted checkpoint,
bounded analysis or new pseudocode resulted.

Both target attempts are sealed and retained. Root verified nine second-execution
payloads and all 81 failed-job payloads. The post-import host snapshot has
6,107,656,192 bytes free and no native analyzer. Global free-space movement is
not charged entirely to this roughly 691 MB job. The root verifier initially
passed a job path to a child-path helper; the retained
[setup correction](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-execution-v2/validation-attempts.json)
records the mistake and the actual public reader's incomplete-job rejection.

The later [closure snapshot](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/final-validation-v5/host-final.json)
records 7,191,879,680 bytes free (6.70 GiB) and no native analyzer. This global
increase does not remove the next fresh job's copy requirements; capacity remains
below the coordinator's planned headroom. The
[final validation packet](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/final-validation-v5/README.md)
records the combined results and current gap.

**Next capacity plan:** retain both incomplete jobs and wait for changed available
capacity. Use the original import CLI with a fresh `native-persistent-baseline-v3`;
do not resume or repair these unaccepted trees. The tool still requires 6 GiB
before every launch and at most 2 GiB total job allocation. The coordinator
recommends at least **10 GiB free before a fresh import**, allowing the retained
copies and headroom for observed global allocation changes; this is additional
planning headroom, not a lowered tool gate or guarantee. Recheck at each stage.
B remains unadmitted because no baseline is accepted. Its provisional four-copy
bound from the closed import is **14,533,525,504 bytes (13.54 GiB)**, measured after
retaining a future accepted baseline; remeasure that baseline before using it.

## Disk cleanup inventory — 2026-10-12

**Observed:** the [read-only storage audit, revision 2](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/storage-audit-v2/report-v2.json)
captures 6,336,147,456 bytes free (5.90 GiB), about 4.10 GiB below the proposed
10 GiB fresh-import headroom. Downloads allocate 28.07 GiB, including 2.61 GiB
of top-level DMG/PKG installers; the separate Live Trial application allocates
7.83 GiB. Homebrew, npm and uv caches allocate 1.05, 1.14 and 0.95 GiB
respectively. These are candidates for review or tool-managed cleanup, not
established disposable bytes or guaranteed reclaimed space. APFS sharing and
snapshots limit what directory allocation predicts. Copying files to an external
drive alone does not release their local storage.

**User constraint:** leave Trash untouched and exclude it from cleanup actions.
No files were deleted or moved and no cleanup commands, restarts or process
signals were issued. The Suite reference, original sources, analysis captures,
incomplete recovery jobs and handoffs remain protected. The hidden updater app
lacks its expected metadata; removal is unresolved. The project occupies about
3.01 GiB, so sacrificing evidence is not the principal capacity solution.

**Proposed next action:** review Downloads for files to move to external storage
or remove individually, and review whether the separate Trial app is still used.
Package tools can preview/prune caches through their supported commands; see the
audit's retained [official guidance](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/storage-audit-v1/sources-v1.json).
No cleanup action is authorized by this inventory. Remeasure capacity after any
user-directed change before retrying; launch and analysis gates remain unchanged.

## Resource admission and stop conditions

These are **proposed conservative budgets**, not measurements of database size.
Use the reviewed monitor's one-second aggregate-owned RSS policy: stop after two
successive samples above 6 GiB, with a 4 GiB Java heap and immediate stop below
3 GiB free disk. Retain logs every 30 seconds and on a stop. Resource observations
include all owned native decompiler children; pool sizing is supplementary.

Before A require at least 6 GiB free disk and allocate at most 2 GiB to its new
project/home/temp/log tree, including retained verification copies. Measure the
closed baseline size `B`, including allocated directory blocks once. The original
B minimum `max(12 GiB, 2*B + 8 GiB)` assumed two new project representations:
a working copy and a checkpoint, each allowed 2 GiB growth, plus temporary/log
allocation and the disk floor. It remains a minimum, not sufficient admission
for a design that retains more copies.

The current controller design retains four new representations: working project,
first disposable reopen copy, checkpoint, and second disposable reopen copy.
Its stronger B admission is therefore
`max(12 GiB, 2*B + 8 GiB, 4*B + 12 GiB + 256 MiB)`, measured **after** retaining
the source baseline. The last term reserves all four copies at `B + 2 GiB`,
1 GiB for temporary/log allocation, the 3 GiB floor and a separate 64 MiB
publication allowance per copy. No successful or failed verification tree is
deleted to fit the earlier two-copy assumption. This is a conservative design
bound; accepted-baseline size and analysis growth remain unmeasured. Each copy also requires
fresh space for its full measured allocation above the floor, and A's complete
job must stay within 2 GiB.

Count copies at full allocated size; do not assume APFS clones,
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

The owned driver and analyst scripts now have retained preparation and fixture
proof packets above. Preserve exact source copies and command arrays; compile
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

**Earlier source-only design review:** canonical execution/export pages, retained launch correction,
current installed launch sources, documented command syntax, headless save/timeout
control flow and source hashes. **Not performed in that review:** a new JVM probe, synthetic
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
Historical actual compilation, handshake and save/reopen results are recorded
in [preparation observations](#preparation-observations--2026-10-11). Final-method
proofs are retained in the revisioned author packets above. Their review and
target outcomes are recorded in the current sections above; earlier snapshots
retain their original methods and limits.
