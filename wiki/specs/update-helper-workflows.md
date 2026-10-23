---
id: SPEC-UPDATE-HELPER-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; static retained arm64 roles only
---

# Update helper handoff workflows

## Scope and authority

This bounded analyst draft concerns externally named CLI, file and process roles in retained exact-build static evidence. It is not released implementation input or a runtime compatibility result. S means a role supported by selected retained static control flow; I means inference; U means unknown. Every target outcome remains U, every case is unexecuted, and every actual and documentary output/comparator is null. A source claim is prose provenance, not an oracle. No implementation algorithm, private identifier or pseudocode is prescribed here.

[Research](../research/update-helper-workflows.md) records evidence and limitations. [Delivery/recovery](delivery-recovery-workflows.md) retains public installation, authorization, update policy and recovery roles; existing project/media/ALS owners retain application-data validity. This packet adds only the selected prepared-handoff CLI/file/process predicates. Whole updater, account/network protocols, package preparation, OS authorization, platform parity and application compatibility remain outside this bounded contract.

## Future evidence prerequisites

Future evidence only, not authorization to execute: independently admitted exact-build actual helper/Live capability, owned disposable current/prepared paths with known distinct nonempty contents, path/permission/dependency identities, known .Old/marker/report states, real launcher identity, independently successful paired baseline and supported recovery route. Missing capability, unavailable input or uninitialized state is U, never a negative pass. No operation is authorized by a case proposal. Audio consequences require their own independently nonzero active-path baseline and existing sound owners.

## Requirements

### REQ-UPDATE-HELPER-001 — Required current and prepared paths

**S; target U.** The retained invocation path requires both --live and --copy, representing the current installation and prepared replacement. Missing required inputs lead to an invalid-invocation path; complete diagnostic grammar and parser recovery are unknown.

Evidence: UH-E01, UH-E02, UH-E03.

### REQ-UPDATE-HELPER-002 — Named optional input roles

**S; target U.** The retained option declarations include --sentinel for a marker path, --usagedata for a reporting path, --parentpid for parent metadata, and the --nowait and --wait-forever controls. The current/copy declarations also name short aliases. These declarations do not establish complete quoting, repetition, encoding or flag-value syntax.

Evidence: UH-E01, UH-E02.

### REQ-UPDATE-HELPER-003 — Handoff argument form

**S; target U.** The traced update handoff supplies --live and --copy and conditionally includes nonempty sentinel/reporting/parent metadata. Its retained argument construction emits option=value text. This is one supplied form, without a complete CLI codec or shell-quoting rule.

Evidence: UH-E09, UH-E10.

### REQ-UPDATE-HELPER-004 — Parent metadata scope

**S; target U.** The supplied --parentpid value has an integer-parsing diagnostic path and an optional reporting role. The retained reporting path can include the supplied parent value. This does not establish that this option selects the process whose completion is awaited, nor an invalid-value refusal or coercion policy.

Evidence: UH-E02, UH-E03.

### REQ-UPDATE-HELPER-005 — Reporting file role

**S; target U.** A --usagedata path is associated with retained reporting calls for process/start/end and replacement/cleanup stages. The role does not specify record bytes, timestamp units, durable flush, upload, consent or successful file creation.

Evidence: UH-E03, UH-E04, UH-E05.

### REQ-UPDATE-HELPER-006 — Conditional orphan wait

**I; target U.** The retained control flow has a conditional wait for the launching process to complete and describes --nowait as bypassing that wait. Connecting option state through the unretained state-construction call is an inference. No timeout, polling unit, infinite-wait guarantee or supplied-PID selection is established.

Evidence: UH-E01, UH-E02, UH-E03.

### REQ-UPDATE-HELPER-007 — Path checks before replacement

**S; target U.** Both supplied locations are checked before the traced replacement stages; an unsuccessful path check takes a failure path. Exact existence/type/access predicate, symbolic-link handling and path repair remain unknown.

Evidence: UH-E04.

### REQ-UPDATE-HELPER-008 — Sibling-path condition

**S; target U.** The retained path comparison rejects current and prepared locations whose parent-directory comparison differs. Path canonicalization, case folding, aliases, mount and same-object policy are not established by that comparison.

Evidence: UH-E04.

### REQ-UPDATE-HELPER-009 — Running-application refusal role

**S; target U.** When the helper running-application check reports Live present, the retained callback takes an abort role instead of invoking replacement. The exact detection predicate and race window remain unknown; an absent or unavailable process fixture cannot prove this exclusion.

Evidence: UH-E07, UH-E03.

### REQ-UPDATE-HELPER-010 — Replacement path names

**S; target U.** The traced normal replacement path uses the current path with an .Old suffix for the old installation and places the prepared replacement at the original current path, followed by attempted cleanup of the old path. This supplies observable location roles, without atomicity, durability or complete metadata preservation.

Evidence: UH-E04, UH-E05.

### REQ-UPDATE-HELPER-011 — First replacement-stage failure

**S; target U.** Failure reported for moving the current installation to its old-path location returns a failure role before the prepared-promotion stage in the retained path. Filesystem partial effects and exact error/status representation remain unknown.

Evidence: UH-E04, UH-E05.

### REQ-UPDATE-HELPER-012 — Second-stage restoration attempt

**S; target U.** If promotion of the prepared copy fails after the first stage, the retained path attempts to restore the old installation to the current path. This is a restoration attempt, not a guarantee of successful rollback, atomicity or recovered content.

Evidence: UH-E04, UH-E05.

### REQ-UPDATE-HELPER-013 — Restoration failure role

**S; target U.** The retained second-stage failure path distinguishes a failed restoration attempt diagnostically and still reports failure. Subsequent recovery, retry, cleanup, surviving paths and application usability remain unknown.

Evidence: UH-E04.

### REQ-UPDATE-HELPER-014 — Cleanup failure is distinct

**S; target U.** Old-installation cleanup is attempted after prepared promotion. Its reported failure causes the replacement operation to report failure; the traced cleanup-failure branch does not itself take the second-stage restoration path. This does not imply the old directory remains intact or the promoted application is usable.

Evidence: UH-E04, UH-E07.

### REQ-UPDATE-HELPER-015 — Optional marker gate

**S; target U.** A nonempty sentinel path is reached for a marker operation only when the replacement operation reports success in the retained callback. Marker presence alone is not evidence of full update compatibility or successful application launch, and a marker attempt is not a successful write oracle.

Evidence: UH-E07, UH-E06.

### REQ-UPDATE-HELPER-016 — Marker-operation error role

**S; target U.** The retained ordinary marker-operation error path records a warning and returns without assigning a new operation status in that routine. This does not establish all exception behavior, exact exit-code mapping or a guarantee that marker failure makes the helper fail.

Evidence: UH-E06, UH-E07.

### REQ-UPDATE-HELPER-017 — Result propagation roles

**S; target U.** The retained helper entry relays the operation result, with distinct invalid-invocation, running-application refusal and replacement-failure branches. Retained numeric constants are source context only; full process-exit mapping, exception/signals and platform representation remain unknown.

Evidence: UH-E08, UH-E03, UH-E07.

### REQ-UPDATE-HELPER-018 — Prepared handoff admission

**S; target U.** The selected update-handoff path first requires a pending prepared update, then waits for the originating application to terminate. A configured crash-marker file or a positive other-application-running check prevents that selected path from launching the swap helper. Other startup, eligibility and concurrency paths remain unclosed.

Evidence: UH-E13, UH-E14, UH-E10.

### REQ-UPDATE-HELPER-019 — Configured helper availability

**S; target U.** The retained handoff checks that a helper executable is configured; absent configuration follows an error role. Relocation also has an error role. Exact exceptions, diagnostics, fallback/retry and user-visible presentation remain unknown.

Evidence: UH-E10, UH-E11, UH-E12.

### REQ-UPDATE-HELPER-020 — Temporary helper process location

**S; target U.** The selected handoff prepares a temporary helper location and requests a separate process there, with that copied executable directory as working directory. Supporting-file selection, loader behavior, collision handling and cleanup lifetime remain unknown; this is an observable process/path role, not an implementation design.

Evidence: UH-E11, UH-E12.

### REQ-UPDATE-HELPER-021 — Live startup admission guard

**S; target U.** The retained Live startup path queries for a running Ableton Swapper. Its positive-result branch prevents startup continuation and has an update-in-progress warning branch; a no-dialog branch also exits. Exact process matching, configuration of the no-dialog branch, rendering and race handling remain unknown.

Evidence: UH-E15, UH-E16, UH-E17, UH-E18, UH-E19, UH-E22.

### REQ-UPDATE-HELPER-022 — Selected Live-to-updater handoff

**S; target U.** The retained Live configuration supplies the updater with a helper location and optional marker location; the selected connector path performs the helper launch. This bounded routing evidence does not prove that no other launch or sentinel-reader path exists in the whole product.

Evidence: UH-E20, UH-E21, UH-E10, UH-E11.

### REQ-UPDATE-HELPER-023 — CLI grammar and malformed inputs

**U; target U.** Full CLI grammar, short-alias spelling, separators, quoting/Unicode, repeated/unknown options, empty arguments, malformed parent metadata and parse-recovery/refusal remain U.

Evidence: none; explicit unknown.

### REQ-UPDATE-HELPER-024 — Path identity and repair

**U; target U.** Exact path validation, canonicalization, case/symlink/mount identities, same-path inputs, existing .Old collisions, permission/space denial and file repair policy remain U.

Evidence: none; explicit unknown.

### REQ-UPDATE-HELPER-025 — Process identity and wait policy

**U; target U.** Parent metadata versus actual launcher identity, PID reuse, process matching/races, wait default/timing/cancel and --wait-forever behavior remain U; its label is not an infinite-wait guarantee.

Evidence: none; explicit unknown.

### REQ-UPDATE-HELPER-026 — Interrupted replacement and recovery

**U; target U.** File-operation partial effects, metadata preservation, interruption/power loss, atomicity/durability, failed restoration and cleanup, retry/restart and repair remain U.

Evidence: none; explicit unknown.

### REQ-UPDATE-HELPER-027 — Marker/report/status representation

**U; target U.** Sentinel touch/create/truncate/content/metadata, reporting/log bytes and event order/flush, full exit/signals/exception mapping and any marker reader remain U.

Evidence: none; explicit unknown.

### REQ-UPDATE-HELPER-028 — Editing and lifecycle

**U; target U.** Persistence across restart, undo/redo, cancellation, source loss, configuration changes, simultaneous updates, teardown and orphan cleanup remain U unless separately supported by existing owners.

Evidence: none; explicit unknown.

### REQ-UPDATE-HELPER-029 — Platform and version closure

**U; target U.** These selected exact12.4.3 arm64 retained branches are not full macOS/Windows/platform, installation, authorization, updater-service, package/delta or current/future-version compatibility.

Evidence: none; explicit unknown.

### REQ-UPDATE-HELPER-030 — Whole-product and service boundary

**U; target U.** Account/consent/upload/protocol, update selection/preparation algorithms, application sound/data compatibility, general recovery and any untraced helper/Live path stay with existing owners or U; source strings alone establish none of them.

Evidence: none; explicit unknown.

## Packet and limits

[Requirement catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/update-helper-workflows/requirements.json), [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/update-helper-workflows/cases.json), [exact static locators](../../analysis/ableton-live-12.4.3/full-spec-v1/update-helper-workflows/evidence.json), [source pins](../../analysis/ableton-live-12.4.3/full-spec-v1/update-helper-workflows/source.json) and [read-only checker](../../analysis/ableton-live-12.4.3/full-spec-v1/update-helper-workflows/validate.py) retain 30 requirements (21 S, 1 I, 8 U), 37 proposed cases and 22 evidence entries. All thirty requirements are semantically incomplete. Restoration attempts are not recovery guarantees; sentinel reachability does not prove successful marker creation; process names or source constants do not establish runtime matching or OS exit behavior.
