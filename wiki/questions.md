---
id: RESEARCH-QUESTIONS
type: questions
status: active
updated: 2026-10-22
access: analysis
---

# Open research questions

Keep one record per durable gap or contradiction. Each record needs affected
IDs, evidence for each competing claim where applicable, state, responsible
role, next action, and eventual resolution link. These are planning gaps;
no experimental contradiction has been established yet.

## Q-001 Compatibility targets

- State: resolved for target T1 ([ADR 0004](decisions/adr-0004-target-scope-t1.md)); open beyond T1; owner: project maintainer.
- Affects: all features in the [feature map](specs/feature-map.md).
- Gap: supported platform/version and behavior/audio/file/UI/timing acceptance
  criteria have not been selected.
- Next action: define dimension-specific targets in the first spec review;
  choose numeric tolerances before accepting comparisons.
- Progress 2026-10-18: ADR 0004 sets the T1 scope, the Linux x86_64 platform and the acceptance criteria for files, values, device audio, timing and whole-mix conformance. Numeric metrics for device audio are set per device spec.

- Progress 2026-10-19: [ADR 0005](decisions/adr-0005-full-live-specification-coverage.md)
  expands specification work to the entire product. It does not supply new
  whole-product numeric tolerances, platform acceptance or compatibility evidence.
  Q-027 tracks the evidence/applicability gaps; T1 criteria remain bounded.

## Q-002 Durable reference identity

- State: resolved for this installed build; owner: analyst.
- Affects: [investigation plan](research/ableton-plan.md), all future evidence.
- Resolution: [SRC-ABLETON-12-4-3](research/sources/ableton-live-12.4.3.md)
  retains exact build, original/slice digests, extraction provenance and environment.
  Ghidra accepted the Live slice. Subsequent selected main-Live code exports
  are recorded in the [execution ledger](research/native-phase-execution.md);
  systematic export coverage and cold recovery remain open in Q-011.
- Retention limitation: installed resources remain mutable external originals;
  evidence tracked in local Git since 2026-10-17 is not an off-machine backup
  until pushed, and the `origin` remote is a public GitHub repository, so pushing
  would publish decompiled material. Q-003 remains open.

## Q-003 Isolation and evidence retention

- State: open; owner: project maintainer.
- Affects: [handoff workflow](workflows.md#release-a-handoff).
- Gap: no isolated implementation environment or durable large-evidence store
  is provisioned. Ignored directories and agent roles are not access controls.
- Next action: prepare a restricted implementation workspace and retention
  destination before releasing work to a clean implementer.

## Q-004 Implementation foundation

- State: open; owner: implementation architect after first handoff.
- Affects: [architecture candidates](implementation/architecture.md).
- Gap: the proposed stack has not been evaluated against released requirements.
- Next action: evaluate a small integrated workflow and record a technical ADR.

## Q-005 Whole app scope expansion

- State: open; owner: analyst/spec author.
- Affects: FEAT-DEVICES, FEAT-WARP, FEAT-ECOSYSTEM, FEAT-PERSISTENCE.
- Gap: supported device catalog, interoperability breadth, Max/Push behavior,
  and full native-format expectations are not bounded.
- Next action: expand the feature families into explicit required/optional/deferred
  contracts while keeping every deferred obligation visible.
- Evidence 2026-10-17: Push 3 support needs a separate helper process with a USB
  display protocol, the Push sysex protocol and a document-sync API with 369 message
  names ([Push 3 helper](research/push3-helper-static.md)). Decide whether Push
  support is required, optional or deferred before drafting a Push spec.
- Progress 2026-10-17: [device bundles](research/device-bundles-static.md) bounds
  the seven natively bundled devices. The 63 other `.adv` root elements (3 are Max
  for Live wrappers) have no bundle under `Devices/Mac`; where they are implemented
  is not established.

## Q-006 Native analysis and resource decoding

- State: open; owner: analyst.
- Affects: FEAT-TRANSPORT, FEAT-PERSISTENCE, FEAT-ECOSYSTEM and FEAT-DEVICES.
- Evidence: [decompilation preparation](research/ableton-decompilation-preparation.md)
  and [structure findings](research/ableton-package-structure.md).
- Gap: core Live auto-analysis, remaining Python modules, proprietary ALP/AGR
  formats, schema migration semantics and resource-to-runtime bindings remain unknown.
- Progress: [MIDI mapping bytecode](research/midi-user-mapping.md) decoded and scoped paths traced; this does not cover all shipped Python.
- Progress 2026-10-17: the bundle side of the device boundary is traced in [device bundles](research/device-bundles-static.md); the Live side (bundle loading, `GetPlugInfoU` use, index mapping, value conversion) is six open queries for the main Live project.
- Progress 2026-10-17: [document container static](research/document-container-static.md) identified `.agr` encodings and the `.alp` header/trailer layout; `.alp` encoding and runtime use of `Schema/` remain unknown.
- Next action: choose a bounded feature question, validate the matching decoder or
  trace its prepared native symbol; derive the contract and escalate only material
  gaps under [ADR 0002](decisions/adr-0002-static-first-analysis.md).
- Progress 2026-10-17: [document container native](research/document-container-native.md) traced stream
  detection, root and version checks and the save writer statically; 12.4.3 reads
  `Schema/<MinorVersion>.txt` on the version-check path (code read, not executed).
  `.alp` and the Live Set save call site remain unknown.
- Progress 2026-10-17: [device parameter mapping](research/device-parameter-mapping-native.md)
  traces the Live side of the device boundary: bundle loading, `GetPlugInfoU`
  selectors, and index and conversion tables for 4 of 7 devices. The Analog,
  Tension and Collision tables, the document reader and a Corpus position-range
  contradiction (probe P4-N5-01) remain open.
- Progress 2026-10-17: [SPEC-ALS-CONTAINER](specs/als-container.md) r2 makes six untraced
  steps explicit assumptions (I1 to I6); the catch site, integer converter, gzip stream and
  empty-string representation remain open.
- Progress 2026-10-17: [device tables](research/device-tables-native.md) completes the Analog, Tension and
  Collision index and conversion tables (472 entries, cross-checked against the bundles and
  disassembly) and their constructor defaults; [SPEC-BUNDLED-DEVICE-PARAMETERS](specs/bundled-device-parameters.md)
  r1 drafts the storage contract for all seven devices. The device create path on load,
  new-instance defaults and the position contradiction (P4-N5-01, P4-N6-01) remain open.
- Progress 2026-10-18 (r2): [SPEC-BUNDLED-DEVICE-PARAMETERS](specs/bundled-device-parameters.md) r2 applies the v1 review. Under ADR 0003 the position contradiction, the create path (A1), new-instance defaults and save output stay unknown. Static routes: the float parameter unit; the list-item factory.

- Progress 2026-10-19: [bundled parameters r3](specs/bundled-device-parameters.md) and Electric’s extracted execution settle the voice limit as Polyphony index + 2; the UI presentation remains unknown. The Electric Volume default is 0.7047892213 and the corrected reference peak is 0.296.

## Q-007 Reference behavior and timing

- State: open; owner: analyst/spec author.
- Affects: all runtime-dependent feature families.
- Evidence: shipped documentation and static fixtures in [SRC-ABLETON-12-4-3](research/sources/ableton-live-12.4.3.md).
- Gap: current static preparation has not established initialization, numeric
  enum semantics, scheduling, DSP, errors or user override precedence. Further
  static tracing may resolve logical behavior; measured runtime characteristics
  and empirical compatibility remain unverified.
- Next action: derive the bounded [spec preparation cases](research/ableton-decompilation-preparation.md#proposed-first-specification-work)
  from resources and code first. Identify which remaining claims actually need
  execution, then retain minimal probes with exact inputs, outputs and environment.
- Progress 2026-10-17: runtime questions from all revision 2 packets are merged
  into the [Phase 4 run sheet](research/phase4-probe-batch.md); nothing has run.

## Q-008 MIDI profile parsing and host errors

- State: open; owner: analyst/spec author.
- Affects: SPEC-MIDI-USER-MAPPING, REQ-MIDI-USER-002/003/005/013.
- Evidence: [mapping research](research/midi-user-mapping.md), PARSE-01–08.
- Gap: parser exceptions and an unknown mode's representation can be traced,
  but host diagnostics, profile recovery and invalid-mode outcome remain unknown.
- Next action: trace the relevant host/loader exception boundary; only if that
  cannot resolve a selected contract, design a minimal malformed-profile probe.
- Progress 2026-10-17: [spec revision 2](specs/midi-user-mapping.md) fixes statically
  which inputs raise out of profile construction (noninteger pad values,
  interpolation, duplicates, pre-section text, invalid Booleans; no handler) and
  how an unknown mode token is passed on. Host outcomes remain open as PRB-S4-03/04
  in the [S4 probe batch](research/midi-closure-r2.md#phase-4-probe-batch); the
  [midi-config-v2 candidate](specs/midi-config-v2-handoff-plan.md) excludes them.
- Progress 2026-10-18 (X2): PRB-S4-04 cannot be settled by extracted execution; it depends on host behavior outside a self-contained function.

## Q-009 MIDI numerical modes, timing and feedback

- State: open; owner: analyst/spec author.
- Affects: SPEC-MIDI-USER-MAPPING, REQ-MIDI-USER-004/005/007–012.
- Evidence: [mapping research](research/midi-user-mapping.md), PARSE-09, BC-02–09.
- Gap: native transforms, 14-bit pairing, pickup, device parameter ordering,
  feedback bytes, seek/nudge timing and remaining bank/lock boundaries.
- Next action: select a single mode or boundary and trace its native dependency;
  reserve actual timing/audio assertions for measured comparisons.
- Progress 2026-10-17: revision 2 adds static map-mode scope, the 14-bit label
  threshold and, as open S-cond clauses, crossfader takeover off, the absent
  mute-feedback default and feedback eligibility. Transforms, feedback bytes and
  timing remain PRB-S4-05/06/07/13; bank contents need `_Generic/Devices` traced
  before PRB-S4-09.
- Progress 2026-10-17 (N7): native transforms traced statically for all ten modes, 14-bit
  pairing, step sizes, clamping and takeover arithmetic ([native transforms](research/midi-transforms-native.md)).
  Open: takeover preference default and labels, the on/off threshold gate, ordering and
  deferral timing (PRB-N7-01 to 05); feedback bytes and seek and nudge timing are unchanged.
- Progress 2026-10-17 (spec r3): [SPEC-MIDI-USER-MAPPING](specs/midi-user-mapping.md) revision 3 adopts the
  N7 transforms as static clauses (with the None label inferred) and static-conditional clauses
  for Pick-Up, Value Scaling and on/off parameters, with cases MT-01 to MT-23. Open: PRB-N7-01 to
  05; feedback bytes and seek and nudge timing unchanged. A narrow midi-config-v3 candidate
  (REQ-005 static value clauses, the crossfader opt-out, MT-01 to 16, 22, 23) is justified but
  not started.
- Progress 2026-10-18 (r4): midi-config-v3 released (127 cases). [SPEC-MIDI-USER-MAPPING](specs/midi-user-mapping.md) r4 narrows the crossfader exemption to Absolute, states the reversed-range stepped rule, and adds reversed-range takeover as unknown. PRB-N7-01 to 05 will not run (ADR 0003); static or extracted-execution routes remain.
- Progress 2026-10-18 (X2, r5): Pick-Up and Value Scaling takeover, reversed ranges and the first 14-bit pair are settled by [extracted execution](research/extracted-execution.md) (`r2/x2-midi-v1`); PRB-N7-03 is settled except the preference default. The value tolerance is now max(1e-6, 2⁻²² × max(|min|, |max|)), which holds on both slices. Still open: PRB-N7-04 (classes, threshold check), PRB-N7-05, and the display and setter (PRB-N7-01, PRB-S4-05).

- Progress 2026-10-19: [MIDI mapping r6](specs/midi-user-mapping.md) applies RV4 precision limits: exclude stepped half-integer ambiguities, accumulate tolerance for repeated relative messages, and leave stepped Value Scaling moves ungraded.

## Q-010 MIDI discovery, lifecycle and interaction

- State: open; owner: analyst/spec author.
- Affects: SPEC-MIDI-USER-MAPPING, REQ-MIDI-USER-001/003/004/006/008/012/013.
- Evidence: [mapping research](research/midi-user-mapping.md), PARSE-10 and draft
  lifecycle cases; documented placement is not an observed discovery run.
- Gap: reload, disconnect/reconnect, held-control cleanup, routing conflicts,
  bank/lock persistence, automation and undo membership.
- Next action: trace discovery/teardown and persistence entry points for one
  selected lifecycle case before deciding whether runtime capture is necessary.
- Progress 2026-10-17: discovery, reload, teardown, encoding and strip-to-track
  ordering remain PRB-S4-01/02/11/14/15/16; native strings are adjacency only.
  Revision 2 adds a routing refinement pending review: a `Send2Knob`*N* without
  a valid `Send1Knob`*N* reaches the strip's first send, contrary to a literal
  reading of the template (D5) and to S4 draft case S4-MIDI-030.
- Progress 2026-10-18 (X2): another control surface on the same input can empty the previous-value record ([MIDI transforms](research/midi-transforms-native.md)).

## Q-011 Main Live export capacity and recovery

- State: open; owner: native-analysis coordinator.
- Affects: [next-phase roadmap](research/native-decompilation-roadmap.md), main
  Live corpus and downstream native behavior investigations.
- Evidence: the [execution ledger](research/native-phase-execution.md) links the
  successful full-analysis completion, frozen inventory and bounded default-profile
  export checkpoints. The earlier disk stop and separate selected exports remain retained.
- Progress: full analysis completed after disk capacity was freed. Actual JVM
  diagnostics disproved the intended two-worker pool setting; aggregate monitoring
  remained active. The full inventory is available; reviewed grouped ingestion and
  attempted-first browsing have been exercised on a systematic export stage,
  with warnings preserved.
- Gap: full-corpus storage/throughput and cold-provider recovery remain unproven.
  Grouped checkpoints reduce whole-ledger rewriting, but do not remove its cost.
  The two bounded samples do not establish full-corpus fit; the capacity review
  stopped further bulk expansion. The current provider uses an ephemeral database.
- Next action: execute the [compact/archive and recovery plan](research/native-compact-storage.md),
  establish database recovery after the [published offline viewer](research/native-compact-storage.md#measured-reader--2026-10-11), before
  admitting a larger stage. The [real mirror](research/native-compact-storage.md#measured-mirror--2026-10-10)
  passed exact-member preservation and measured allocation; it adds no exports
  and does not establish full-corpus fit. The
  [persistent recovery design](research/native-analysis-recovery.md) is reviewed
  and its loader-matched correction passes scope/quality reviews and 198 tooling
  tests. Actual [target import/save](research/native-analysis-recovery.md#corrected-import-passes-reopen-capacity-stop--2026-10-12)
  passes, but first reopen is capacity-blocked. Retain both incomplete jobs;
  additional capacity precedes a fresh import and accepted cold-reopen proof,
  then measured bounded-analysis admission. No new pseudocode was added.
  Keep selected, linker and default-profile evidence separate.
  The [storage inventory](research/native-analysis-recovery.md#disk-cleanup-inventory--2026-10-12)
  identifies Downloads, the separate Trial app and package caches as reviewable
  capacity candidates. Trash is explicitly excluded; no cleanup was performed
  and suggested allocation is not guaranteed reclaimed space.
- Progress 2026-10-17: the work moved to a Linux workstation with the same
  Ghidra/JDK versions, REA 6.5.0 and far larger RAM/CPU; both arm64 slices were
  re-derived byte-identically. See the [provisioning record](research/native-phase-execution.md#linux-workstation-provisioning--2026-10-17).
- Gap 2026-10-17: the entire retained `analysis/` evidence tree (full inventory,
  2,028 exports, coverage ledger, incomplete persistent jobs) is absent here, so
  every linked capture is unavailable until restored from the macOS host. The
  persistent-project storage location is undecided; see the
  [Linux paths](research/native-analysis-recovery.md#linux-workstation-paths--2026-10-17).
- Proposal 2026-10-17: [roadmap revision 2](research/native-decompilation-roadmap.md#revision-2-proposal--2026-10-17)
  sequences the storage decision, a persistent project, one measured corpus
  batch and outside-in specification packets; adopted and executing 2026-10-17.

## Q-012 Transport-state load and save semantics

- State: open; owner: analyst (S1 native half).
- Affects: FEAT-TRANSPORT, FEAT-PERSISTENCE, the proposed SPEC-TRANSPORT-STATE.
- Evidence: [transport-state static](research/transport-state-static.md) and
  [document container static](research/document-container-static.md).
- Gap: defaults when a field is absent; handling of malformed tokens, duplicates
  and out-of-range values; clamping; precedence between `Manual` values, the
  one-event envelopes and scene values; the meaning of `Time=-63072000`; and the
  exact format 12.4.3 writes.
- Next action: once the saved project exists, trace the callers of
  `Member "{}" of Class {} is missing` and of the `Value … out of range for '`
  message; reserve the 12.4.3 write format for a Phase 4 save capture if static
  tracing cannot fix it.
- Progress 2026-10-17: native half filed in [transport-state native](research/transport-state-native.md);
  tokens, defaults, duplicates, save number format and the time-signature code are
  derived; precedence, post-load clamping, the time-signature default and error
  presentation remain; probes PRB-N1-01 to 08.
- Progress 2026-10-17: [document container native](research/document-container-native.md) found the single
  envelope writer (declaration, attribute order, MajorVersion 5) and its gzip level
  handling; the Live Set save call site and level remain unknown (PRB-N2-01 in
  [SPEC-ALS-CONTAINER](specs/als-container.md)).
- Progress 2026-10-17: [SPEC-TRANSPORT-STATE](specs/transport-state.md) r2 makes the
  both-sides-space, `+`-with-trailing-space and `-` meter spellings and negative zero on
  save unknown. A probe is still needed for TS-010 and for a missing
  `TimeSignature/Manual` (PRB-N1-04 has no such variant).
- Progress 2026-10-18 (X2, r3): settled by [extracted execution](research/extracted-execution.md) (`r2/x2-transport-v1`): the REQ-006 integer spellings (` +201 `, ` 201 `, `+201 ` refused; `-0`, `-201` accepted; 63-character and int32 limits), negative zero (`-0` written and read), the REQ-011 correction (k from log10 rounded to binary64) and the meter codes (`n/d`). TS-010 is refused. The number parser behaves like C `strtod`. transport-state-v2 is staged to correct the released REQ-011. Still open: REQ-009 effective values, REQ-012, the default when the time signature is missing, which display shows the meter, codes outside 0 to 494, and Apple's `log10` near half a binary64 spacing. The loader's handling of an accepted −201 is also unknown.

- Progress 2026-10-19: [transport r5](specs/transport-state.md) records the conditional tempo reconciliation on open; the owner flag and chosen envelope value remain untraced. The int32 member path is shared with note storage; accepting a leading minus is established, while int64 NoteId/NextId uses a different converter.

## Q-013 x86_64-only ReWire and MultiF0 paths

- State: open; owner: analyst.
- Affects: FEAT-ECOSYSTEM, FEAT-MIDI audio-to-MIDI conversion, FEAT-PERSISTENCE.
- Evidence: [x86_64-only bundles](research/x86-only-bundles.md).
- Gap: when the ReWire install runs and what alias it creates; whether 12.4.3
  still offers ReWire to users; the default choice between built-in and dynamic
  MultiF0; whether Convert Drums uses MultiF0; the meaning of MultiF0 result
  fields; why the engine bundle's arm64 stub exists.
- Next action: once the Live x86_64 analysis finishes, query the callers of
  `InstallPropellerheadDlls: `, `Ableton Live Engine_64`,
  `Audio2Midi: Use builtin MultiF0 lib` and `MultiF0: No MultiF0 library found at `.
- Progress 2026-10-17 (N4): arm64 uses the built-in MultiF0 unless a developer option is set; the x86_64 default and ReWire wait for the x86_64 analysis. See [helper launch](research/helper-launch-live-side.md).
- Progress 2026-10-17 (N8): the x86_64 install (ReWire.bundle via ditto, alias `Ableton Live Engine_64`
  via MakeAlias) runs only from one LReWireHost method during song-agent construction, behind a
  predicate that returns 0; host open and the Engine's device open are likewise disabled, so
  12.4.3 offers no working ReWire (inferred). The x86_64 MultiF0 default is built-in; Convert Drums
  uses a separate drum task; result fields mapped (start, end, Hz, trajectory, amplitude; inferred).
  Open: user-visible ReWire remnants, the Engine arm64 stub, time units. See
  [Live x86_64 paths](research/x86-live-paths.md).

## Q-014 Browser index behavior

- State: open; owner: analyst.
- Affects: FEAT-UI (browser), FEAT-PERSISTENCE (tags and sample references).
- Evidence: [browser index](research/browser-index-static.md).
- Gap: Live's spawn site and arguments for the index helper; the real database
  prefix and directory; whether version 12300 is what is written; how the browser
  queries the database; who consults `filerefmap.db` and what its type values mean;
  user-visible handling of missing, corrupt or
  unsupported files. Runtime facts are in probes PRB-H2-01 to 09.
- Next action: query the saved Live project for references to `live->index`,
  `ipc-channel`, `{}-files-{}.db` and `fileref-map-path`.
- Progress 2026-10-17 (N4): spawn site, options-file argument and keys, and the 100-launch restart cap answered in [helper launch](research/helper-launch-live-side.md#index); database prefix, folder, version and queries still open.
- Progress 2026-10-17 (D2): [SPEC-BROWSER-INDEX](specs/browser-index.md) r1 drafted; sidecar names,
  the type-to-kind map and the item `colors` field resolved from the helper corpus. Still open: the
  `<n>` folder, write timing, which kinds are listed, preview playback and `hideKeywords`
  (no probe will run, ADR 0003; static routes in the spec's open questions).
- Progress 2026-10-18 (r2): [SPEC-BROWSER-INDEX](specs/browser-index.md) r2 applies the browser-index-v1 review. Still open: whether a sidecar is rewritten after reading, which edits empty a sidecar, and how built-in and plug-in entries bind.

## Q-015 Helper launch and update handling in Live

- State: open; owner: analyst.
- Affects: FEAT-DELIVERY, FEAT-ECOSYSTEM.
- Evidence: [web, add-ons, swapper](research/web-addons-swapper-static.md),
  [Push 3 helper](research/push3-helper-static.md).
- Gap: how Live writes the web connector's configuration and the add-ons `--cid`;
  start conditions such as the auto-update setting and free space; Live's UI for
  each update event; use of the swapper's sentinel file; Pack and `.alp`
  installation; which side binds each Push nanomsg channel and what Live sends.
- Next action: trace `StartWebConnector`, `AddOns: start process` and the three
  Push channel names in the saved Live project.
- Progress 2026-10-17 (N4): web connector config keys and commands, the 3 GiB free-space rule, update-event states, add-ons `--cid` and restart cap, the swapper startup guard (exit 42), sentinel only via a debug option, and Push channel roles answered in [helper launch](research/helper-launch-live-side.md); Pack and `.alp` handling and the `+0x720` gate open.

## Q-016 Plug-in discovery Live-side contract

- State: open; owner: analyst.
- Affects: FEAT-HOSTING.
- Evidence: [plug-in scanner](research/plugin-scanner-static.md).
- Gap: which folders and domain IDs Live passes and how Rescan maps to `--reset`;
  where Audio Units are scanned; any timeout or kill policy; the meaning of the
  watchdog constants; the message framing; the database folder; the
  `dev_identifier` format; how duplicate class IDs appear in the browser. The crash and limit derivations (PD-10, PD-12) stay unreleased; under ADR 0003 no probe will run.
- Next action: trace the Live callers of `Plugins: start scanner process`, `--cid`,
  `TPluginScannerMediator` and `APluginSettingsPreferencesModel` in the saved Live
  project.
- Progress 2026-10-17 (N4): argv, domain IDs, the Rescan-to-`--reset all` mapping, relaunch policy, Live-side timeouts and message framing answered in [helper launch](research/helper-launch-live-side.md#plug-in-scanner); Audio Unit path, `dev_identifier`, duplicates and the database folder still open; probes PRB-N4-01, 02, 05.
- Progress 2026-10-17 (D1): drafted [SPEC-PLUGIN-DISCOVERY](specs/plugin-discovery.md) r1; PD-10 and PD-12 kept unknown (REQ-012, REQ-014). Resolved statically: VST2 system folders `~/Library/Audio/Plug-Ins/VST` and `/Library/Audio/Plug-Ins/VST`. Still open: Audio Units, scan triggers, source-switch effects, hang, duplicates, progress display, VST3 symlink and unreadable-subfolder handling.
- Progress 2026-10-18 (r2): [SPEC-PLUGIN-DISCOVERY](specs/plugin-discovery.md) r2 applies findings F1 to F7. A plain file cannot record its own load (release cases 021 `J.vst3` and 028); with no observation (ADR 0003), plain-file candidacy stays static-derived. Still statically decidable: the extension of names beginning with a period, VST3 links and unreadable subfolders, Audio Units, switch labels and defaults, scan triggers, duplicates, progress display. Crash, hang and over-limit order have no further static route.

## Q-017 Clip launch timing and launch modes

- State: open; owner: analyst.
- Affects: FEAT-SESSION, FEAT-TRANSPORT.
- Evidence: [clip launch](research/clip-launch.md).
- Gap: the boundary offset (an unresolved virtual call), the track condition in the
  launch path, launching with the transport stopped, Gate, Toggle and Repeat behavior,
  Legato, the velocity law and follow-action timing. CL-13's near-boundary clause stays unreleased unless a static reading settles it (ADR 0003).
- Next action: resolve the offset call's target and interpret the slot-state test (A1); PRB-S5-01 to 11 will not run (ADR 0003).
- Progress 2026-10-17 (D3): [SPEC-CLIP-LAUNCH](specs/clip-launch.md) r1 keeps REQ-017's near-boundary clause
  and REQ-018 to 023 unknown with these probes. New gaps: missing or out-of-range
  `GlobalQuantisation` and `AutoQuantisation` (no S5 probe; extend PRB-S5-09 or 10), reachability of
  migration step 17, clips with several time-signature entries, and the uninterpreted slot-state
  test behind the clip-grid choice (assumption A1).
- Progress 2026-10-18 (r2): [SPEC-CLIP-LAUNCH](specs/clip-launch.md) r2 applies the clip-launch-v1 review and drops the REQ-015 to 018 release proposal. New gaps: out-of-range bounded values, the script-side API error text, opening corrections for scenes, the step-406 clip with both forms, the saved scene form, and A7.
- Progress 2026-10-18 (X2, r3): the grid and boundary arithmetic, the chance rescaling and its 0 to 100 limits (A7; 150/50 gives 75/25) and follow-time rounding are settled by [extracted execution](research/extracted-execution.md) (`r2/x2-notes-launch-v1`). Corrections: a stored −99 is read as 0 and launches as Global (REQ-016). A press exactly on a triplet grid line sometimes launches at the next line (REQ-017; 236 of 720 lines up to beat 64). Whether the scheduler calls this arithmetic (A1) and the near-boundary offset stay unknown, because the offset comes from engine objects that exist only at run time.
- Progress 2026-10-18 (T1.3, clip-launch r4): A1 and the launch offset are settled for Trigger launches ([playback core](specs/playback-core.md) REQ-007). The offset is the track player's pre-delay: 0 for MIDI, the audio crossfade length otherwise. Timing is sample-exact.

- Progress 2026-10-19: [clip launch r5](specs/clip-launch.md) carries PLAYBACK-CORE A4 for the loaded Global-grid choice. Extracted follow-time rounding is established; the final open outcome for out-of-range values remains unknown.

## Q-018 MIDI note key range and ordering after load

- State: open; owner: analyst.
- Affects: FEAT-MIDI, the proposed SPEC-MIDI-NOTE-STORAGE (MN-16, MN-17).
- Evidence: [MIDI note storage](research/midi-note-storage.md).
- Gap: a `MidiKey` outside 0 to 127, a missing `MidiKey`, or two KeyTracks with the same
  key reach a 128-slot table store with no range check, so the outcome may be memory
  corruption; whether notes are re-sorted after load is untraced.
- Next action: under ADR 0003 PRB-S7-05 and 06 will not run. Trace the key-map store's callers for a range guard, the per-note list adjustment call, and the empty-KeyTrack gate; otherwise these stay U and excluded.
- Progress 2026-10-17 (D4): [SPEC-MIDI-NOTE-STORAGE](specs/midi-note-storage.md) r1 excludes MidiKey outside 0
  to 127, a missing MidiKey and repeated keys (REQ-011), and keeps re-sorting after load (REQ-010),
  list Id meaning (REQ-012) and refusal presentation (REQ-017) open. No range guard was traced;
  PRB-S7-05 and 06 remain the next action. Also open: an untraced adjustment of per-note lists
  with events at or outside the note span (REQ-014).
- Progress 2026-10-18 (r2): [SPEC-MIDI-NOTE-STORAGE](specs/midi-note-storage.md) r2 applies the midi-note-storage-v1 review.
- Progress 2026-10-18 (X2, r3): the range-guard part is closed. Neither slice has a guard, and an out-of-range key corrupts the notes object, so REQ-011 stays permanently excluded. Value limits, time-grid rounding and saved number text are now settled by extracted execution. Re-sorting, the list adjustment and the empty-KeyTrack gate remain open.

## Q-019 Mixer volume and send values sent to the engine

- State: open; owner: analyst.
- Affects: FEAT-AUDIO, the proposed SPEC-MIXER-VALUES (MX-05 and the send clauses).
- Evidence: [mixer values](research/mixer-values.md).
- Gap: the value actually sent on the engine's volume and send ports (stored gain or fader
  position), where sends get their curve and silence floor, out-of-range values after load,
  the meaning of SoloSink, which formatter each UI surface uses, and whether volume
  automation interpolates in gain or in fader position (shared with S6).
- Next action: trace the logic-to-engine path for volume and sends statically. No reference observation is available (ADR 0003), so PRB-S9-01 to 08 will not run; anything not settled statically stays unknown.
- Progress 2026-10-17 (D8): narrowed, not settled. On both track-mixer wiring variants the volume
  port output is converted from fader position to gain with the volume curve and then floored; pan,
  split and volume ports share one class bound to their parameters; their pan-law input order is
  confirmed. Open: where the stored gain becomes that position; the send path. Evidence:
  [SPEC-MIXER-VALUES](specs/mixer-values.md) appendix; queries retained in
  `analysis/ableton-live-12.4.3/r2/d8-mixer-v1/`.
- Progress 2026-10-18 (r2): [SPEC-MIXER-VALUES](specs/mixer-values.md) r2 applies the mixer-values-v1 review. New gap: what `EnabledByUser` changes (REQ-003). SPEC-AUTOMATION-ENVELOPES r2: every Float envelope value passes through the same unresolved per-target converter.
- Progress 2026-10-18 (X2, r3): both fader-curve conversions and the then-claimed exact round trip (corrected below on 2026-10-19), the pan law, the seven crossfade curves and the `On`/`Off` text are settled by [extracted execution](research/extracted-execution.md) (`r2/x2-mixer-v1`). The value that reaches the engine ports depends on callers and state and stays open.
- Progress 2026-10-18 (X2 envelopes): automation envelopes evaluate in stored units. Volume's dB converter sits on a separate display path that uses the fader table (`0x101ae2d30`).
- Progress 2026-10-18 (T1.4): settled statically, with conditions A3 to A5 and an arm64 check ([mix graph](specs/mix-graph.md)). Live sends fader positions to the engine, not stored gains: for the manual value, at track creation and for envelope points. The engine applies the fader curve, the crossfade factor and the silence floor. `SoloSink` is the Solo button.

- Correction 2026-10-19: the [mixer-values-v2 review](../handoff/mixer-values-v2/REVIEW.md#scope-and-checks) contradicts general round-trip identity: 765 of 1,601 sampled non-point gains changed. [Mixer values r5](specs/mixer-values.md) and [mix graph r2](specs/mix-graph.md) retain both conversions; only seven tested curve points have an exact-return expectation. No general error bound is established. This narrows the numeric claim, not the T1.4 port-wiring finding.

## Q-020 Automation envelope load robustness

- State: open; owner: analyst.
- Affects: FEAT-AUTOMATION, FEAT-PERSISTENCE, the proposed SPEC-AUTOMATION-ENVELOPES.
- Evidence: [automation envelopes](research/automation-envelopes.md).
- Gap: an envelope whose `PointeeId` matches no target makes Live log `Invalid Pointee ID`,
  fail an assertion and abort when it is accessed; what opening such a set does in a
  release build is unknown. Unsorted events, missing attributes and duplicate event Ids are
  also untraced. A specification must not require a crash; these inputs need exclusion or
  a defined safe behavior chosen by the project.
- Next action: trace which load path dereferences envelope targets (static only); keep these inputs excluded. PRB-S6 probes will not run (ADR 0003).
- Progress 2026-10-17 (D6): draft [SPEC-AUTOMATION-ENVELOPES](specs/automation-envelopes.md) r1 excludes
  dangling `PointeeId` input (REQ-002) and evaluation before an envelope's first event, possible
  when it is at 0 and unguarded in the reference (REQ-010, REQ-011). Unsorted events, missing
  attributes and duplicate Ids stay unknown pending PRB-S6-03 and 07. Probe follow-ups: PRB-S6-04
  needs a Pan variant (Volume 0 is below its stored minimum) and PRB-S6-07 a variant without `Id`.
- Progress 2026-10-18 (r2): [SPEC-AUTOMATION-ENVELOPES](specs/automation-envelopes.md) r2 applies the automation-envelopes-v1 review; dangling-target inputs remain excluded.
- Progress 2026-10-18 (X2, r3): evaluating an envelope before its first event crashes in both evaluators (extracted execution, `r2/x2-envelope-warp-v1`), so that input stays excluded. The load-robustness items remain open.
- Progress 2026-10-18 (T1.1): envelopes with dangling targets are removed on open ([Live Set structure](specs/live-set-structure.md) REQ-014), so REQ-002's exclusion can narrow.

- Progress 2026-10-19: [automation r5](specs/automation-envelopes.md) applies RA2-01 to 03: opening removes clip envelopes with exactly one event and Pan/Speaker/CrossFadeState track envelopes with fewer than two before validation. Live Set open enables normalization (T11 A1 / SF-2). Other target-device relations and malformed/unsorted lists remain open. Ideal segment values are not ramped sample comparisons.

## Q-021 Warp playback mapping and load handling

- State: open; owner: analyst.
- Affects: FEAT-WARP, the draft [SPEC-WARP-MARKERS](specs/warp-markers.md).
- Evidence: [warp markers](research/warp-markers.md).
- Gap: whether playback uses the same piecewise-linear mapping as the scripting conversion;
  load handling of malformed marker lists, missing or out-of-range values; the Transient
  Envelope range; the warp mode an audio clip gets when the element is absent; the spec's
  assumptions A1 to A4 (A2 opening, A4 saving).
- Next action: no reference observation is available (ADR 0003). Static routes: trace the other callers of the scripting interpolation into playback; the open-path check flag (A1) and the auto-warp trigger (A2); the save path (A4); the TransientEnvelope curve; the preference store at load. Per-mode audio stays unknown.
- Progress 2026-10-18 (r2): [SPEC-WARP-MARKERS](specs/warp-markers.md) r2 applies the warp-markers-v1 review: A2 split into opening (A2) and saving (A4); REQ-015 restated as inclusive bounds.
- Progress 2026-10-18 (X2, r3): the scripting beat and sample conversion, the shadow-marker formula and the REQ-015 and 016 edges are settled by extracted execution, which reproduces the shipped shadows exactly. No caller connects these functions to playback, so the playback mapping stays open.
- Progress 2026-10-18 (T1.3, warp r4): playback callers found. Warped playback converts beats to file time with the scripting mapping, and unwarped session clips ignore markers. Per-mode read positions stay unknown and outside T1.

- Progress 2026-10-19: [warp r5](specs/warp-markers.md) marks WMK-019 unexecuted and corrects WMK-039’s rounding example. Structure A1 settles the load-walk assumption; duplicate marker Id refusal remains conditioned by A5. Display, shadow caller arguments and a playback acceptance observable remain open.

## Q-022 Live Set structure load rules

- State: open; owner: analyst.
- Affects: FEAT-PERSISTENCE, every Live Set fixture, [SPEC-LIVE-SET-STRUCTURE](specs/live-set-structure.md).
- Evidence: [Live Set structure](research/live-set-structure.md); `r2/t11-structure-v1`.
- Settled 2026-10-18: every open route runs the validation walk (A1). A track with clip
  slots but no freeze sequencer is refused (A2; rests on the arm64 call graph). 204
  released fixtures fail these rules (see the catalog note).
- Gap: sets whose slot count differs from their scene count; SendsPre count different
  from the number of returns; missing or mismatched samples; decoding of formats other
  than PCM; which `RelativePathType` a save picks; device class per chain (A6);
  duplicate or negative pointee Ids; list items without Ids; outputs other than Main.
- Progress 2026-10-19: the invalid-fixture releases are superseded. [Live Set structure r2](specs/live-set-structure.md) uses the reviewed device-free T11-MIN (NextPointeeId 67), isolates refusal mutations, and leaves end-to-end RelativePathType 2–7 unresolved. Envelope removal is qualified by the other open checks, and the event-count discard follows automation r5.
- Next action: trace the remaining items statically where T1 needs them; no fixture rebuild is owed for the already superseded releases.

## Q-023 Mix-graph T1 conditions

- State: open; owner: analyst.
- Affects: FEAT-AUDIO, FEAT-AUTOMATION, [SPEC-MIX-GRAPH](specs/mix-graph.md).
- Evidence: [mix graph](research/mix-graph.md); `r2/t14-mix-v1`.
- Gap:
  - A1 is settled as a test-vehicle convention by ADR 0004 (not a remaining gap);
  - A2, whether a saved solo takes effect on load;
  - A3 to A5, the Q-019 conditions;
  - A6, default automation range/1000 data step, 200-sample minimum and no smoothing, with no mixer override found;
  - A7, whether EnabledByUser true yields an active send on the T1 graph;
  - A8;
  - the effect of a send with `EnabledByUser` false;
  - what a single-event envelope applies;
  - the time base of clip envelopes;
  - the summation order on the main bus.
- Progress 2026-10-18: A1 is recorded as a T1 render convention in [ADR 0004](decisions/adr-0004-target-scope-t1.md#render-conventions).
- Progress 2026-10-19: [mix graph r2](specs/mix-graph.md) applies the release review: A4/A7 apply only when a nonzero send reaches a playing return; MG-023 needs neither. Float interpolation needs a nonzero data step. The song-time automation offset remains untraced, so values at explicit envelope time do not establish sample timing. Main tempo/meter one-event envelopes are exempt from the unsupported-one-event playback exclusion.
- Next action: trace A2 to A8 and the automation offset statically; preserve their separate scopes.

## Q-024 Playback core render semantics

- State: open; owner: analyst.
- Affects: FEAT-TRANSPORT, FEAT-SESSION, FEAT-MIDI, [SPEC-PLAYBACK-CORE](specs/playback-core.md).
- Evidence: [playback core](research/playback-core.md); `r2/t13-playback-v1`.
- Gap:
  - at some whole-sample positions an event lands on P or P+1, depending on the engine's sample counter;
  - Play's start beat after a set is opened, and when scripted actions take effect;
  - same-key overlapping notes;
  - the flag that enables velocity deviation and probability;
  - exact fade values, and the audio during a crossfade;
  - the HiQ 16-bit sample type (up to 4.9e-4);
  - file formats other than those covered;
  - audio `StartRelative` other than 0 (the MIDI start-relative rule is specified).
- Next action: trace the engine sample counter and the action delivery statically; for T1, keep cases that accept P or P+1.

- Progress 2026-10-19: [playback-core-v1](../handoff/playback-core-v1/README.md) released locally after independent review (92 cases). The draft r2 excludes the unestablished immediate E ≤ t activation observable, 48 kHz PBC-024, crossfade audio and end-sample observables; those exclusions are not compatibility passes.

## Q-025 Device host protocol and device-audio acceptance

- State: open; owner: analyst (protocol); user (Amp and Cabinet decision).
- Affects: FEAT-DEVICES, [SPEC-DEVICE-CORPUS](specs/device-corpus.md) and the other T1 device specs.
- Evidence: [device DSP](research/device-dsp-extracted.md); `r2/t12-device-dsp-v1`.
- Gap:
  - the Live-side protocol: event frame base, transport and flag values, reset timing;
  - whether Live passes Corpus ExcitationX and Listening as 0..1 or −1..1. The strike range
    is 0.5–0.723 under one reading and 0.277–0.723 under the other (see
    REQ-BUNDLED-DEVICE-PARAMETERS-015);
  - the Corpus MIDI side-chain path;
  - LfoSync, and clock-seeded random LFO shapes;
  - Collision’s Live-side grid phase and block partition, listening/excitation position mapping, absolute modal gains, and a stable noise metric;
  - whether the proposed per-device metric is acceptable for T1.
- Decision 2026-10-19: the user chose to keep Amp and Cabinet blocked while
  finishing Corpus, Electric, Tension, Analog and Collision. CoreFoundation,
  Objective-C emulation and a fake host identity are not authorized. T1 still
  names all seven; this is a deferred workstream, not an exclusion or completion pass.
- Next action: follow the [current analyst checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint) for whole eligible X classes and bounded S joins. All five partial drafts have finite releases; this question selects no new calibration or arbitrary parameter renders.
- Progress 2026-10-22: [sole-reviewed host native recovery](research/device-host-protocol.md#three-method-host-native-contract-adopted--2026-10-22) narrows local return/activity/context delivery; public scheduler/stop/restart/tails, x86-bundle meaning and all remaining application gaps stay open.
- Progress 2026-10-18: Electric is specified ([SPEC-DEVICE-ELECTRIC](specs/device-electric.md)). New protocol questions: Live's grid phase and event frame base; whether Live stops processing when a device signals that it may; which block an automated value arrives in, since parameters that act immediately can be off by one block. Values between sampled points need reference renders made on demand.
- Progress 2026-10-18: Tension is specified ([SPEC-DEVICE-TENSION](specs/device-tension.md)). New items: the host block partition, which places notes on Analog's and Tension's 1 ms grid; whether statistical grading of chaotic Tension settings (bow, DamperMass 0) is acceptable; settings that depend on the random seed.
- Progress 2026-10-18: Analog is specified ([SPEC-DEVICE-ANALOG](specs/device-analog.md)). New items: rounding of fractional velocity; stopping when the activity flag is 0; the block in which an automated value arrives.

- Progress 2026-10-19: [Collision r1](specs/device-collision.md) recovers 41 retained renders and 380 event-grid checks. Constructor silence is explained: both resonators are disabled; the Defaults preset enables resonator 1 (peak 0.110951 for retained C4). Its 50 cases remain proposed/partial, with noise, unresolved modes and host protocol U. Two concurrent edits were preserved; exact original bytes are retained through a recovery mapping, not silently substituted.

- Progress 2026-10-19: [device-collision-v1](../handoff/device-collision-v1/README.md) accepts only constructor effective silence and the calibrated 44.1 kHz Pipe reference. This finite metric acceptance leaves modal/noise/Tube and general device protocol requirements open; it does not complete Collision or T1.

- Progress 2026-10-19: [device-corpus-v1](../handoff/device-corpus-v1/README.md) accepts the finite 24-group/68-evaluation metric with 174 explicitly omitted mode occurrences. [Electric v2](../handoff/device-electric-v2/README.md) accepts 117 mono evaluations with frozen stable masks; three unstable settings, random-component level and phase/polarity remain ungraded. These approvals do not settle general device or host-protocol equivalence.

- Progress 2026-10-19: [Tension v1](../handoff/device-tension-v1/README.md) accepts 27 finite outputs, excluding four chaotic settings and 37 uncalibrated outputs. [Analog v1](../handoff/device-analog-v1/README.md) accepts 42 deterministic evaluations with frozen measurement eligibility; noise, uncalibrated modulation, glide and unison remain excluded. All five releases accept only their explicit finite metrics. Host protocol, general synthesis and arm64 equivalence remain open; no candidate comparison has run.

- Progress 2026-10-19: the [host-protocol research](research/device-host-protocol.md)
  distinguishes ordinary Reset/NewRate (no warm-up) from ResetAndDispatch (four
  1,024-frame helper requests). N5/DSP summaries are corrected; earlier one-helper
  harness measurements remain as executed. Event rebasing, queue, parameter and
  transport transforms are non-normative research models, not closed application
  behavior. The reviewed [host draft](specs/bundled-device-hosting.md) retains one
  conditional synthetic output-composition criterion and eleven U requirements;
  all 23 application cases remain unknown. Frame base, insertion/reset audio,
  activity/restart, errors, scheduler sizes and side-chain behavior remain open.

- Progress 2026-10-19: [Position value-source review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-position-value-source-review.json)
  independently supports conditional initialization, same-field pull and finite
  equal-interval conversion bypass. Actual emission/currentcell to player/Indexer
  and publicA1 remain unresolved; no grade is added. [New LFO capture packet](../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-lfo-ramp-up/README.md)
  retains two actual x86 extractions under ADR0003: the new Sine baseline exactly
  matches old bytes, then RampUp yields finite productive stereo output.
  [Capture review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-lfo-ramp-up-review.json) and
  [two additional sensitivity captures](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-lfo-ramp-sensitivity-review.json) passed bounded independent
  review. The [1%per-channel engineering RMS method](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-lfo-ramp-criterion-review.json) and
  [R4 owner](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-owner-r4-review.json) passed separate independent reviews;
  R4 adopts one finite host-input case DCO-029. [Corpus v2](../handoff/device-corpus-v2/README.md)
  releases that one additional comparison after separate review,69evaluations
  including all68old ones. Its1%RMSbudget is a finite engineering criterion.
  This closes no general full-cycle/wrap, Sync, Spin/random, arm64, Live-host,
  modal174 or compatibility question and gives no complete-device/candidate grade.

- Unreviewed query retention 2026-10-19: [bounded current-cell frontier](../analysis/ableton-live-12.4.3/full-spec-v1/queries/corpus-a1-cell-frontier-2026-10-19.json)
  preserves16exact retained source records and the inconclusive bind/initializer/
  accessor selections. It does not join the parameter current-cell to active
  processing, accept A1, prove absence or establish infeasibility. Reuse these
  exact inspected boundaries before repeating that search.

- Later MIDI progress 2026-10-19: [two held-note captures](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-pitch-review.json)
  passed independent bounded evidence review, six actual new Corpus children
  total with the earlier Ramp series. Several components shift approximately
  an octave across fixed views, consistent with note60-to72. No exact note,
  calibrated fundamental, onset/frame base, Live-sidechain or criterion grade.
  [Canonical research](research/corpus-dsp-static.md#later-bounded-midi-pitch-evidence--2026-10-19)
  owns the interpretation and unreviewed source caveats. The [finite modal method](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-modal-method-review.json)
  is independently approved after one data-only calculation/eight controls;
  both window-sensitive mode16observations remain ungraded after reference
  inspection, separately from174historical omissions. [Owner R5](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-owner-r5-review.json)
  is separately approved/adopted for two exact histories DCO030/031 only;
  no general MIDI law, native-pole eligibility or uncertainty is recovered.
  [Corpus v3](../handoff/device-corpus-v3/README.md) releases those two exact
  comparisons after separate handoff/final-seal review; 71 evaluations retain
  all 69 earlier ones. General MIDI behavior remains open. [Three later gate/release captures](../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-gate-release/CAPTURE.md)
  [passed bounded evidence review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-gate-release-capture-review.json): gate1-held/off full-byte equal,
  gate0-off equals older held control. Nine original children total; no
  note-off admission/general gate law or new normative case follows.

- Source progress 2026-10-20: [conditional initialization queue join](research/corpus-dsp-static.md#conditional-initialization-queue-join--2026-10-20)
  independently approved as partial source research. Actual module membership,
  render-time manager argument, item policy and Live delivery remain unknown;
  no case or application outcome is graded. The next source selection is only
  render9300 mode0 argument setup; before-impulse probe preflight is separate.

- Later actual capture 2026-10-20: [before-impulse Off record](research/corpus-dsp-static.md#actual-before-impulse-note-off-captures--2026-10-20)
  retains three further valid extracted captures, twelve original children total.
  Gate1held/off differ only in a tiny prefix; all post-impulse output matches
  historical control. Independent capture review approved bounded observations only; no gate/admission law or
  criterion/case added. Render-specific argument review and two exact queue-item
  source bodies are the selected continuation; Live routing remains unknown.

- Endpoint capture 2026-10-20: [host34 zero record](research/corpus-dsp-static.md#actual-host-index34-zero-captures--2026-10-20)
  retains three further valid captures, fifteen original children in this
  continuation. Gate1-Off now differs after the impulse; matched held/gate0
  controls retain their stated identities. Capture review and the separate
  [finite method review](research/corpus-dsp-static.md#actual-host-index34-zero-captures--2026-10-20) approved bounded scopes. Separate R6 owner review passed and Root adopted only DCO032;
  v4 is independently reviewed/released only for its72finite comparisons.
  All broader gaps stay open; no general
  gate/decay law or full-profile result.

- Pickup observation 2026-10-20: [two matched histories](research/corpus-dsp-static.md#actual-pickup-step-histories--2026-10-20)
  completed with two attempts/PIDs/valid outputs, seventeen original Corpus
  children total. Independent actual-capture review approved bounded observations. The separate
  [finite method review](research/corpus-dsp-static.md#reviewed-pickup-method-and-current-cell-construction--2026-10-20) approved its actual data-only validation. Separate R7 owner review passed and
  Root adopted only DCO033 under001/012; [v5 is now locally released](research/corpus-dsp-static.md#release5-local-publication--2026-10-20)
  after separate content/actual-result/final-seal approvals,73finite evaluations.
  No transition duration or general channel-invariance law follows.
  [A1's callback word](research/corpus-dsp-static.md#a1-registered-callback-word--2026-10-20)
  resolves to a retained wrapper alias; actual consumption/emission stays open.

- Progress 2026-10-20: [Utility native static readback](research/device-audio-utilities.md#utility-native-abi-static-review-approval--2026-10-20) narrows conditional return/argument carriers and initializer-local bytes. Actual admission/current-value/callback receiver/host-output/lifecycle joins remain unknown; no public default or application grade follows. D03 remains open. The current plan separately selects x86 extent metadata only; Amp/Cabinet deferral and the seven-device T1 scope are unchanged.

The later [x86 static approval](research/device-audio-utilities.md#utility-x86-static-review-approval--2026-10-20) narrows conditional carrier/byte relationships only;all six public bridges/38application outcomes remainU. Further wrapper-frontier work is metadata-only.

The [four-target static approval](research/device-audio-utilities.md#utility-x86-four-target-static-review-approval--2026-10-20) adds conditional carrier/member evidence and an unresolved localx86tail;UDN002 excludes inconsistent auxiliary ESIL strings. All public bridges remainU. The [352byte inner-entry actual approval](research/device-audio-utilities.md#utility-x86-inner-entry-static-review-approval--2026-10-20) adds sevenconditionalfacts with late load64(T+10) return,unknownhelperwrites/roles andallESILexcluded;no successor capture selected.

## Q-026 Analog behavior left open

- State: open; owner: analyst.
- Affects: FEAT-DEVICES, [SPEC-DEVICE-ANALOG](specs/device-analog.md).
- Evidence: [Analog DSP](research/device-analog-dsp.md); `r2/t12-analog-v1`.
- Gap:
  - glide and unison;
  - the envelope Loop, FreeRun and Legato modes (REQ-021);
  - the LFO Sync, Delay, FadeIn, Phase and pulse-width laws (REQ-018);
  - the amplifier's keyboard and envelope pan modulation (REQ-015);
  - ramps after parameter changes (REQ-022);
  - Notch4 and formant responses, graded only against renders;
  - whether arm64 fused multiply-adds change the binary32 envelope steps.
- Next action: render each mode under extracted execution and fit its law.

## Q-027 Whole-product specification evidence and version coverage

- State: open; owner: analyst; scope authorized by ADR 0005.
- Affects: every feature family, the [coverage design](research/full-live-specification-design.md)
  and [execution plan](research/full-live-specification-plan.md).
- Evidence: the pinned installed [12.4.3 source](research/sources/ableton-live-12.4.3.md),
  existing partial specs/releases and newly retained official Live 12 chapters.
- Gap: current documentation identifies the major release but not exact patch
  applicability. Product resources establish surfaces, not their complete behavior.
  Editing, recording, racks/hosting, other native devices, UI/control, file/media
  lifecycle and engine interactions need contracts and acceptance cases beyond
  existing finite T1 scopes. Hardware, platform and error outcomes remain unproven.
- Rule: label documented-domain requirements D12 and retain exact-build U until
  corroborated; do not turn inventory assignment or an authored test into a pass.
  Keep each narrower unresolved behavior in its canonical spec/research owner.
- Progress: bounded partial contracts and independent reviews are routed from the
  [spec index](specs/index.md) and current execution plan. Source/scope/case reviews
  do not establish original application behavior or close version applicability.
  The narrower Auto Filter source mismatches are tracked in Q-028 below.
- Next action: continue bounded uncovered contracts and exact-build corroboration;
  reconcile every frozen inventory surface with its current owner and outstanding
  outcomes. No user deferral is silently excluded.

## Q-028 Auto Filter source mismatches

- State: open; owner: analyst; affects Auto Filter documentary requirements and
  exact-build applicability.
- Canonical evidence and interpretation: [filter/EQ research](research/filter-eq-devices.md)
  and [requirements](specs/filter-eq-devices.md) REQ-DEVICE-AF-001/027/030. The
  retained source is the audio-effects HTML SHA-256
  `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`,
  blocks B02/B53 and B59/B63. Both competing wordings are retained there.
- Gap: exact internal detector tap and complete sidechain-filter Type choices
  are not resolved by field names, preset values or the modern device title.
- Next action: trace the exact installed current-device selection/detector paths
  using retained static evidence; retain AF-C043/044 as null-oracle probes until
  a justified source resolves them. Do not merge enums or borrow Legacy behavior.
- Completion rule: preserve exact source/version limits and review any resulting
  behavioral clause before changing its unknown status. No runtime outcome is
  established by this question or a resolved documentation fixture.

## Q-029 MIDI utility source contexts across chapters

- State: open; owner: analyst; historical cross-chapter question retained.
- Current source reconciliation, selected/no-selection Interval actions and the
  unresolved Humanize span context are maintained once in
  [Q-053](#q-053-midi-utility-gesture-and-humanize-source-contexts).
  [MIDI owner R2](specs/midi-editing-tools.md) passed focused independent review;
  [Clip View R2](specs/clip-view-workflows.md#preconditions-and-unresolved-contexts)
  routes those note effects to that owner. All target outcomes remain U.

## Q-030 Session Follow action source contexts

- State: open; owner: analyst; affects documentary launch/Follow applicability,
  not a newly established probability or timing law.
- Canonical evidence/interpretation: [Session launch source contexts](specs/session-launch-workflows.md#source-context-questions)
  and [retained launch research](research/session-launch-workflows.md). The local
  SLC-U-GLOBAL-FOLLOW, SLC-U-CHANCE-COUPLING and SLC-U-ACTION-CONTEXT obligations
  retain exact paragraphs, released-vocabulary limits and unknown comparisons.
- Gap: non-None versus Global Follow quantization, coupled A/B chance editing,
  inline-image action labels and assigned-versus-enabled indicators require
  matched source version and preconditions. No normalized probability law,
  eventual-success guarantee or replacement rule is established.
- Next action: resolve only through exact source/control-context evidence and a
  separately reviewed successor. Existing REQ-CLIP-LAUNCH-020/021/022/023 remain U;
  static released enum vocabulary does not establish live action execution.

## Q-031 New-clip color preference context

- State: open; owner: analyst; affects general Clip View/new-clip color wording.
- Canonical evidence/interpretation: [settings source-context question](specs/settings-learning-workflows.md#source-context-question)
  SET-U-CLIP-COLOR, with [settings research](research/settings-learning-workflows.md).
  Existing REQ-CLIP-VIEW-005 retains exact original source context and now qualifies
  inheritance in the separately reviewed R2; target preference/history stays U.
- Gap: the current First Steps chapter documents random-versus-track color for
  new clips; the Clip View source describes track-color inheritance. The actual
  preference state/version must be matched before selecting a target rule.
- Bounded exact-export progress: [retained native context](../analysis/ableton-live-12.4.3/full-spec-v1/clip-color-static-context/manifest.json)
  [passed independent research-only review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/clip-color-static-context-review.json).
  Fourteen selected decompilation records comprise ten complete small-body reads
  (three incidental unlinked neighbors explicitly unassigned), three registration
  excerpts and one large RTTI metadata-only record. Two followed call edges add
  private preference-model binding navigation, without establishing a specific
  preference-to-new-clip creation boundary. Empty getter-suffix reference arrays
  and unmatched literals in the finite vtable index do not prove unreachability
  or absent features. Source export UTC is unstated, separate from extraction UTC.
  This receives zero requirements, cases, behavioral credit or topic completion.
- Owner scope: [Clip View R2 passed independent partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/clip-view-owner-r2-review.json),
  explicitly qualifying its old inheritance sentence and adding only admitted
  creation-history proposals. The frozen Settings R4 source-question paragraph
  describes the earlier Clip View R1 wording as historical context; its own
  REQ-SETTINGS-LEARNING-016 already permits both preferences and remains U.
  A finite current-wiki search found no accepted generic unconditional new-clip
  color law to carry forward; Bounce track color and API Chain auto-color remain
  distinct scopes, not resolved here.
- Next action: follow only a bounded actual preference/creation boundary from
  these retained leads, retaining both manual contexts and source/build/history
  limits. Further target rule adoption needs reviewed evidence. No contradiction, random color inequality/distribution,
  target default or silent sealed-byte rewrite is inferred.

## Q-032 Warp import readiness and source contexts

- State: open; owner: analyst; affects documentary source import/readiness and
  interactive Warp applicability, not a new codec/analysis algorithm.
- Canonical evidence/interpretation: [Warp load-policy/import research](research/warping-workflows.md#load-policies-and-import-wording)
  and REQ-WFW-U-IMPORT in [Warp workflows](specs/warping-workflows.md#open-obligations).
  The existing [media owner](specs/media-file-workflows.md) retains its source scope.
- Gap: all-first-import analysis/readiness versus long-analysis wording, import
  command versus drag, accepted format/platform variants and short/long contexts
  need matched evidence. No universal readiness/codec rule replaces either source.
- Next action: preserve exact retained paragraphs and independently review any
  successor qualifying the existing owner. All unsupported target outputs remain U.

## Q-033 Automation and clip-envelope source contexts

- State: open; owner: analyst; affects documentary editing/control applicability,
  not the released finite envelope evaluator or playback timebase assumptions.
- Canonical evidence/interpretation: [automation source-context questions](research/automation-workflows.md#source-context-questions)
  and the [automation workflow draft](specs/automation-workflows.md).
- Gap: Q-AW-001 retains clear/delete shortcut focus/context, Q-AW-002 retains
  sample-replacement all-settings wording alongside REQ-CLIP-VIEW-041's
  equal-length Warp-marker predicate, and Q-AW-003 retains unspecified MIDI
  reset/range behavior. No replacement rule or numeric/reset value is inferred.
- Next action: preserve both exact source routes and independently review any
  owner correction after matching preconditions/version. Existing finite
  automation, mix units/timebase and Clip View sources remain unchanged; U stays U.

## Q-034 Resource and fact-sheet comparison contexts

- State: open; owner: analyst; affects composed engine/resource outcomes, not
  replacement finite mix/record/Warp/envelope laws.
- Canonical evidence/interpretation: [engine/resource research](research/engine-resource-workflows.md)
  and [partial contract](specs/engine-resource-workflows.md). Q-ER-001–005 retain
  CPU audio-only/current wording, split/loop context, Freeze parameter snapshot,
  bypass identity with delay alignment and MIDI monitoring-option applicability.
- Next action: match exact source/settings/processing histories and reconcile
  only through reviewed successors. Publisher historical hardware timing results,
  private precision/thread descriptions and general quality claims provide no
  target numerical/performance tolerance or universal waveform inequality.

## Q-035 Public Live API versions and unresolved semantics

- State: open; owner: analyst; affects full public path/object/member/event scope.
- Canonical source/discovery: [Cycling74 inventory](research/sources/cycling74-live-api.md).
  The current LOM index explicitly declares12.4.5; target12.4.3 and matching Max
  reference versions remain unproven. Source discovery is not a behavioral contract.
- Gap: inheritance/root/alias closure, bridge signatures/events/grammar/lifecycle,
  placeholder versus combined command sections and actual target outcomes need
  retained source/context evidence. All45entries/588explicit declarations/6bridge
  references stay visible with zero complete entries; no existing native enum or
  numerical owner is replaced by newer reference prose.
- Next action: independently draft/review bounded public bridge and member
  contracts with exact version/locator and finite case prerequisites. No script,
  Max patch, example or API call is run by source inventory or this question.

## Q-036 Push source-model and workflow contexts

- State: open; owner: analyst; affects documentary Push1/Push2 workflow scope.
- Canonical evidence/interpretation: [Push source questions](research/push-controller-workflows.md#source-context-questions)
  and [per-model partial contract](specs/push-controller-workflows.md).
  Q-PUSH-001–003 retain Note/Layout, selected-track/new-record slot prerequisites
  and light-red/unlit contexts without a target behavior or LED protocol law.
- Next action: match model/firmware/source version/active mode/input context
  before a separately reviewed successor. Push3 standalone,149controller/support
  directory profiles, hardware availability and all timing/pressure/MIDI/USB/
  palette/output cases remain open; generic setup cannot close them.

## Q-037 Delivery and recovery source applicability

- State: open; owner: analyst; affects current official Help versus exact-target
  installation, authorization, update, reset and crash/recovery workflows.
- Canonical evidence: [delivery/recovery research](research/delivery-recovery-workflows.md#ownership-and-unknowns)
  retains Q-DRW-001–005; [partial contracts](specs/delivery-recovery-workflows.md)
  retain platform/edition/prompt prerequisites and null operational comparisons.
- Gap: exact12.4.3 controls, minor-version save context, ambiguous recovery
  destination, independently valid baseline inputs and failure/cancellation/
  persistence outcomes remain U. Existing finite storage and Q002 owners retain
  their scope; public Help does not supply legal entitlement or transaction laws.
- Next action: resolve through exact retained platform/version/context evidence
  and independent successor review. No installer/account/update/reset/recovery
  operation was executed or authorized by this documentary investigation.

## Q-038 Public API bridge source contexts

- State: open; owner: analyst; narrows the bridge portion of Q035.
- Canonical evidence: [seven bridge questions](research/live-api-bridge-workflows.md#source-context-questions)
  Q-LAB-001–007 and [bridge contracts](specs/live-api-bridge-workflows.md).
- Gap: dynamic IDs versus optional Persistent Mapping, standalone getid placeholder,
  omitted this_device root, notification mutation/defer contexts, remote automation/
  envelope identities, thisdevice outlets and JavaScript return annotations remain U.
- Next action: preserve exact reference versions and prerequisites before reviewing
  any successor. No default ID lifetime, output grammar, callback order, threading
  architecture or message/numeric/timing oracle follows from these source contexts.

## Q-039 Browser content and service contexts

- State: open; owner: analyst; affects the new Browser content/service predicates.
- Canonical evidence: [Browser interpretation/questions](research/browser-content-workflows.md#interpretation-and-questions)
  Q-BC-001–009 and [partial contracts](specs/browser-content-workflows.md).
- Gap: filter algebra, analysis readiness, local versus Splice similarity, Pack
  operations, account/rights context, Cloud direction, Push3 pairing, Library/Backup
  copies and preview contexts remain unresolved. Existing generic Browser, project,
  Clip and settings owners retain their separately evidenced behavior.
- Next action: match build/service/device/account/content preconditions with retained
  evidence and independently review revisions. No download/upload/account/hardware
  action, protocol, legal rule, numerical ranking or audio/codec result is implied.

## Q-040 Shared workspace source contexts

- State: open; owner: analyst; affects global Scale, feedback and window contexts.
- Canonical evidence: [workspace questions](research/application-workspace.md#source-questions)
  and [partial workspace contracts](specs/application-workspace.md).
- Gap: selected/no-selected/future-clip scale history, Concepts Fold wording versus
  the existing out-of-scale-note exception and offered insertion-marker context
  remain U. Detailed Clip View/MIDI/keyboard/device owners remain unchanged.
- Next action: reconcile exact source/version/selection/focus prerequisites before
  a reviewed successor. Do not infer existing-clip overwrite, universal scale-only
  rows, marker availability, coordinates or window timing from general UI prose.

## Q-041 Public API Clip/Sample member contexts

- State: open; owner: analyst; narrows Q035 to five typed member references.
- Canonical evidence: [twelve Clip/Sample contexts](research/live-api-clip-sample.md#source-context-questions)
  and [partial member contracts](specs/live-api-clip-sample.md).
- Gap: access/prose conflict, property/function and type differences, Warp enums/
  dictionary units, Session start-time association, note IDs/return fields, omitted
  signatures, deferred operations, capabilities and inherited/lifecycle closure
  remain U. Every one of131 direct members is partial, not semantically complete.
- Next action: admit exact-target valid types/contexts and independent results,
  retaining source differences and existing finite owners before any successor.
  No actual API/message/numeric/signal/timing oracle follows from source declarations.

## Q-042 Public API control, routing, groove and tuning contexts

- State: open; owner: analyst; narrows Q035 to six reference entries.
- Canonical evidence: [control/tuning contexts](research/live-api-control-tuning.md#source-context-questions)
  and [partial member/root contracts](specs/live-api-control-tuning.md).
- Gap: control-surface ordering/ownership and timeout int/float plus unspecified
  unit, routing dictionary identity/lifecycle, Groove Children primitives and
  amounts, tuning dictionary keys/units and zero-member root inheritance remain U.
- Next action: corrected R2 partial scope passed independent focused review; resolve
  remaining gaps using exact-target valid fixtures and retained source/version evidence. No
  hardware/API/protocol action, default, dictionary key or timeout unit is invented.

## Q-043 Public API core/Session source contexts

- State: open; owner: analyst; narrows Q035 to ten references/226 direct members.
- Canonical evidence: [core/Session research](research/live-api-core-session.md)
  and [partial contracts](specs/live-api-core-session.md); local labels are
  packet-qualified, independent of Clip/Sample's similarly spelled Q-LCS labels.
- Gap: topology/name aliases, Arranger/Arrangement spelling, Group ClipSlot
  status, MIDI/audio cross-reference, Push3 predicates, version chronology,
  print/throw/path/lane contexts, omitted units/signatures/results and numerical
  cross-owner interactions remain U.
- Required review corrections: [CORE-REVIEW-001–003](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/live-api-core-session-review.json)
  remove unsupported Track creation beat units, capture prose-supported optional
  destination without a guessed default and retain untyped SMPTE representation.
  The preserved R2 successor passed [focused final review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/live-api-core-session-review-final.json); all three wording/optionality findings are resolved, with remaining behavior U.
- Next action: resolve actual target/typed/lifecycle outcomes with admitted
  exact-version evidence and cases; partial approval does not close the family.

## Q-044 Public API device/rack/mixer source contexts

- State: open; owner: analyst; narrows Q035 to ten references/95 direct members.
- Canonical evidence: [device/rack research](research/live-api-device-rack.md)
  and [partial contracts](specs/live-api-device-rack.md).
- Gap: heading-only DrumPad.delete_all_chains supplies no operation, plural names
  with singular published types cannot be repaired into lists, and
  ChainMixerDevice.sends retains ambiguous Rack context. Value/display units,
  missing arguments/results, inheritance, insertion/AB eligibility, macro RNG,
  observer history and lifecycle remain unknown despite partial-scope approval.
- Next action: retain exact declarations and independently admit target semantics;
  zero arguments/void returns, object lists, sound or native value maps are never
  inferred from names or an existing finite storage owner.

## Q-045 Public API specialized device source contexts

- State: open; owner: analyst; narrows Q035 to fourteen references/108 members.
- Canonical evidence: [specialized device contexts](research/live-api-specialized-devices.md#source-context-questions)
  and [partial contracts](specs/live-api-specialized-devices.md).
- Gap: Compressor source-list owner, Wavetable omitted selector types/oscillator2
  enum/setter amount, Looper buffer/tempo units and nonexhaustive export gates,
  DrumCell/Roar naming/inheritance, bend/gain units, category/list/bank/preset
  dependencies and actual processing/lifecycle outcomes remain unresolved.
- Next action: partial scope passed independent review; admit exact-target
  payload/context/results. No analogous type/enum/unit, default, DSP
  algorithm or complete signature is supplied by the mapping ledger.

## Q-046 Mixing workflow source contexts

- State: open; owner: analyst; affects the additional mixer/group/control scope.
- Canonical evidence: [mixing contexts](research/mixing-workflows.md#unresolved-source-contexts)
  and [partial contracts](specs/mixing-workflows.md), independently reviewed.
- Gap: B014 implicit/preference arm context versus recording001U, B043 group
  slot/stop wording versus Session owner, B066/067 unnamed-curve half-range
  wording versus finite seven curves, B053 Enable Send versus native holder/
  active-bit identity, and multi-edit units/clamping/Ctrl context remain U.
- Next action: preserve source/version/preference/topology differences and review
  owner successors only with sufficient evidence. No finite law, recording gate,
  source graph or native field identity is replaced by mixer overview prose.

## Q-047 Manual citation anchors outside the original TOC

- State: open; owner: analyst; affects ongoing whole-source reconciliation.
- Canonical evidence: [second citation companion](../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r6-citation-crosswalk/summary.json)
  and [independent navigation review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/manual-citation-crosswalk-r6-review.json).
- Gap:330cited Push block direct anchors are null;46Browser references use14exact
  URLs absent from the original numbered TOC. Retained heading context and
  source bodies remain available, but parent/alias/fuzzy matching is not exact
  evidence. Original880rows/708leaves are not asserted to exhaust all paragraphs,
  unnumbered sections, linked services, installed-only or cross-feature behavior.
- Source diagnosis: [R8 reviewed dispositions](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/browser-heading-dispositions-r8-review.json) verify14real numbered h4 headings omitted from both retained navigation sequences; the parser accepts four-part numbers. OriginalTOC rows/leaf metadata and46unmatched refs remain unchanged; causal publication history and behavior remain U.
- Census: [R9 structural review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/captured-manual-headings-r9-review.json) verifies1,066actual heading URLs/186extras, including the14Browser headings. All880originalURLs/708leaf flags remain unchanged; no paragraph, exact-target or semantic coverage follows.
- Next action: retain exact source identities and continue reviewed
  applicability/paragraph/topic disposition, adding discovery companions where
  supported. Never force a TOC match, erase an unmatched obligation or infer a
  completed leaf from a citation. U source-context citations stay explicitly U.

## Q-048 APC metadata versus observable startup contracts

- State: open; owner: analyst; affects eight named APC profiles within the149-row
  controller/support inventory. Other141rows and the separate _APC support row
  remain unchanged; directory or bytecode presence is not supported hardware.
- Canonical evidence: [APC research](research/apc-controller-capabilities.md) and
  [required scope review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/apc-controller-capabilities-review.json)
  APCC-REVIEW-001. Eight exact pinned startup modules support37literal identity/
  port/symbol/omission records, but opaque helper-call inputs alone establish no
  observable descriptor output, registration, matching or port effect.
- Correction: preserved R2 passed [focused reclassification review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/apc-controller-capabilities-review-final.json);37records now remain research-only with distinct META IDs and exact historical traces. SixU obligations/twelveU cases remain unchanged, with zero supported runtime contracts or coverage credit.
- Next action: retain bounded observable
  startup unknowns and positive-prerequisite cases; actual interface/host/USB/
  MIDI/LED/audio/timing/lifecycle behavior stays U. No framework sweep or source/
  helper/hardware execution is implied by this correction, and no metadata count
  receives application coverage credit.

## Q-049 Update-helper static flow and applicability

- State: open; owner: analyst; affects the bounded prepared update handoff.
- Canonical evidence: [helper research questions](research/update-helper-workflows.md#scoped-questions)
  Q-UH-001–008 and [partial draft](specs/update-helper-workflows.md), accepted by
  [independent partial static-role review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/update-helper-workflows-review.json). Retained source roles are21S/oneinference/eightU; all37
  proposed outcomes/comparators remain null/U/unexecuted.
- Gap: CLI/default/constructor wiring, path-wrapper/type predicates, actual parent
  versus waited-process identity, wait-forever semantics, interruption/rollback/
  cleanup, marker/report codecs and OS status, selected startup guard coverage,
  platform/authorization/updater/network/data lifecycle remain unknown. One
  reported restore attempt is not proven recovery, and logged marker failure
  does not establish a new nonzero exit status.
- Next action: retain the reviewed source-flow warnings and inference
  limits; admit new evidence before any owner successor. No helper, prepared installation, swap,
  rollback, account, network, hardware or original function was executed; a
  source/function/string name alone is not a runtime result or candidate design.

## Q-050 Retained-source assertions and missing acceptance contexts

- State: open; owner: analyst; affects full-product source/case reconciliation.
- Canonical evidence: [Stem retained-source audit](../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation-source-audit/README.md)
  and [independent audit review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/stem-separation-source-audit-review.json)
  distinguish94claim/context facets from18clauses/29actions. Thirteen proposed
  delta groups were adopted by the separately [reviewed partial owner R2](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/stem-separation-owner-r2-review.json),
  preserving18old clauses and adding two scoped eligibility/preparation bridges.
  Current32cases name finite contexts; their actual outcomes and completion stay U.
- [Synchronization audit review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synchronization-source-audit-review.json)
  requires SYNC-SOURCE-AUDIT-REVIEW-001: case012 does not explicitly establish
  running Follower before hiding Follow or observe cessation. Available input
  and control visibility alone cannot supply that positive baseline. A preserved
  audit correction [passed focused R2 re-review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synchronization-source-audit-review-final.json);
  [Owner R2 passed independent partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synchronization-owner-r2-review.json)
  with the explicit running-positive-before-hide case.
- [Warp source audit](../analysis/ableton-live-12.4.3/full-spec-v1/warping-source-audit/README.md)
  [passed partial audit review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/warping-source-audit-review.json):
  all131retained blocks/50clauses/88actions were assessed as248claim/context
  facets, with16proposed delta groups. Missing direct tempo edit, actual Warp
  Sample invocation, matched rough-tempo reference and genuine active tempo/leader
  histories are distinct from existing inspected controls. [Owner R2](../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manifest-author-r2.json)
  [passed focused independent review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/warping-workflows-owner-r2-review.json):
  50same requirement IDs/91cases, four clause refinements/22old action changes
  and three newUcontexts. Q032, native finite laws and image/destination unknowns
  remain unchanged. Character accounting only checks textual omission.
- Next action: independently review each preserved owner/case delta and continue
  paragraph/list assertion reconciliation, including the retained Video chapter
  and [First Steps70-block audit](../analysis/ableton-live-12.4.3/full-spec-v1/settings-source-audit/README-r2.md),
  both independently reviewed as retained-text/block audits only. Video R2-spec/R3-research
  and First Steps local-case R3 passed focused owner review. Exact cross-owner
  reconciliation passed scoped review, with the remaining configuration gaps in Q051.
  No raw-caption/image closure follows from the First Steps audit. Preserve all source-silent operational unknowns and uninspected images/
  destinations. Source assignment and citation matches never close a feature.
  Root retains historical catalog/canonical pin mappings and marks only affected
  semantic assumptions stale; original reviews and published payloads are immutable.
  [Design revision8](research/full-live-specification-design.md#revision8-current-checks-and-historical-applicability--2026-10-19)
  separates current successor checks from historical mutable-pin applicability.
  Preserve/enumerate old consumers; replay them only when a concrete dependency,
  failed required check or release gate needs it. No automatic adapter per owner
  revision or blanket green historical cohort is required.
  [Historical R1 replay](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/r4-cohort-historical-replay-2026-10-19-v1.json)
  reproduces the old R4 and Stem/Video audit outputs through eight explicit R1
  snapshot reads. A [preserved v2 tool review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/r4-cohort-historical-replay-v2-review.json)
  also checks the synchronization-audit R2 historical replay; four outputs match
  with195internal/200outer files unchanged. This does not approve current owner
  clauses or close a source topic. Later [finite Warp-dependency successors](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/warp-dependency-historical-replay-review.json)
  preserve the earlier tools/reports and reproduce the same twelve checker outputs
  across two cohorts;611outer files stay unchanged. Only exact absolute old
  Warp spec/research routes are added; current Stem pages remain current.
- [Mixing retained-source audit](../analysis/ableton-live-12.4.3/full-spec-v1/mixing-source-audit/README.md)
  [passed independent partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mixing-source-audit-review.json):
  94blocks/178claim-context records reconcile23clauses/33actual actions and17
  proposed groups. Existing multi-edit/color subsets remain represented; genuinely
  active group-child, arm-insertion, mapped-key and separate Solo/Options contexts
  received bounded refinements in [owner R2](../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/manifest-author-r2.json),
  [independently reviewed as partial](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mixing-workflows-owner-r2-review.json):
  31requirements/50cases, eight old actions refined/eight new UI roles/17new cases.
  All23old clauses and remaining original case fields are exact; Q046 and
  uninspected chart/destinations remain open.
  Keyboard source audit R2 and separate owner R5 are reviewed in Q052; dispatch remains U.
- [Bounded Monitoring reconciliation](../analysis/ableton-live-12.4.3/full-spec-v1/monitoring-source-reconciliation/README.md)
  [passed independent source-only review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/monitoring-source-reconciliation-review.json): all nine §17.1blocks, seven compensation
  context blocks,24overlapping facets and22selected owner references. Existing
  RML006/007/008 already exercise the mode matrix, selected Monitor buttons and
  both resets; brief Recording rows do not imply missing repository coverage.
  The blue In Activator display role and explicit RML009 right-click gesture were
  subsequently adopted in [RML owner R2](../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manifest-author-r2.json),
  [independently reviewed as partial](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/routing-monitoring-owner-r2-review.json):
  41requirements/70cases, preserving all40old clauses and69case identities. No
  color metric, default, timing law or target observation follows.
- [Session retained-source audit](../analysis/ableton-live-12.4.3/full-spec-v1/session-grid-source-audit/README.md)
  [passed independent partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session-grid-source-audit-review.json):
  all77blocks/142facets against29contracts/40actions and17audit-only proposals.
  Existing Mixing R2 productive group-slot probe is a true reused context;
  SessionB074 StopAll Arrangement wording remains U. Separate [owner R3](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session-view-owner-r3-review.json)
  passed focused partial review:30requirements/57cases, preserving all29/40old
  records;13 bounded local groups/two U-only/two external-pending. Source review
  alone does not adopt a law, and every actual outcome remains null/U/unexecuted.
- [Grooves source audit R2](../analysis/ableton-live-12.4.3/full-spec-v1/groove-source-audit/README-r2.md)
  [passed focused partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/groove-source-audit-review-final.json):
  GSA-REVIEW-001 cleared only the two erroneous Groove-extraction links from
  Rack-chain context; correct Racks022/RCK046 is retained. Separate owner R3 is
  [independently reviewed as partial](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/groove-owner-r3-review.json), with14unchanged IDs/34cases, three refined contract rows and ten added actions. Original finite Quantize/Commit and random limits remain exact. [Arrangement audit R2](../analysis/ableton-live-12.4.3/full-spec-v1/arrangement-source-audit/README-r2.md)
  [passed focused correction review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/arrangement-source-audit-review-final.json):
  ASA-REVIEW-001 narrows six assessment strings to old SV001's actual neighboring
  launch gestures, preserving source any-order text without later-case borrowing.
  Both full R1 reviews remain immutable; no source accounting is normative closure.

- [Complete retained MPE audit](../analysis/ableton-live-12.4.3/full-spec-v1/mpe-source-audit/README.md)
  [passed independent partial source review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mpe-source-audit-review.json):
  66blocks/110facets against18actual clauses/27actions,28literalresources and13
  audit-only proposal groups. Selected FAQ matching-range context,26external
  owner records and14Glissando/LFO blocks remain bounded contexts. Offline editing
  needs no controller; generic activity is not a per-note delivery baseline.
  Fold/optional-lane C3, numeric units, output protocol and all target outcomes
  remain U. Source review adopts no normative law or complete topic.
- The [complete retained MIDI chapter audit](../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing-source-audit/README.md)
  [passed independent partial source review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-editing-source-audit-review.json):244blocks/506facets/144literalresources against
  43clauses/60actions and38audit-only proposals. Separate full MIDI Tools chapter
  coverage is not claimed; Q052/Q053/C1–C3 stay open pending evidence.

- [MPE owner R3](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mpe-owner-r3-review.json)
  passed independent partial review:18IDs/50cases, nine rows refined/23actions
  added,27old records and79prior files exact. Ten new UI relations/thirteen null
  documentary outcomes remain distinct; recording/plugin-output probes stayU.
  All157watched paths stayed exact. Full numerical/protocol/lifecycle outcomes
  and Fold/C3 remain open; then-current distinct MPE/Tuning/Groove union116 avoided
  recounting the immutable shared83. Full49-block Tuning audit independently reviewed as partial; Tuning owner R3 independently reviewed as partial (21IDs/43cases).
- MIDI [gesture R3](../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/README-r3.md)
  [passed independent partial owner review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-editing-gesture-owner-r3-review.json):43IDs/72cases,60old records and17toolrows
  exact. Six rows gain explicit source-entry roles; twelve new actions adopt
  selected subsets of eleven audit groups, not all38groups. Q052/Q053/C1–C3 and
  other source contexts stay open. The separate full146-block MIDI Tools chapter
  audit [passed independent partial source review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-tools-source-audit-review.json) (302assessments/21audit-onlygroups); Tools owner R5 (43/93) passed focused partial review after three source-role corrections.

- [Arrangement owner R2 review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/arrangement-editing-owner-r2-review.json)
  required ARR-R2-REVIEW-001: nine inherited numeric/duration predicates were
  copied into new documentary expectations paired with no-numeric comparators,
  while prose/reporting called all52nonnull fields visible-only. All actual
  outcomes remain null/U. Preserve every R1/R2 byte and original source predicate;
  [preserved R3](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/arrangement-editing-owner-r3-review.json) passed focused partial review: exactly18fields nulled,43named/41null
  documentary pairs, all42requirements/84actions and35old files exact. Six unsafe
  fixtures were rejected;166watched paths unchanged. This carries the separate
  full186source/42clause/84action review; no second full-source review, numeric
  law or family completion is claimed.

- Full [Tuning source audit](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tuning-source-audit-review.json)
  passed independent partial review:49blocks/68assessments/12audit-only groups
  against21clauses/32actual actions. Nineteen matching rendered FAQ/ASCL contexts
  and35adjacent records remain bounded; owner R3 passed separate partial review. Actual input and
  effective tuned output remain distinct from labels, metadata and configuration.
- Full40-block [conversion audit](../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi-source-audit/README.md)
  passed independent partial review:40whole-context judgments/five audit-only
  groups against14clauses/29actual actions. No atomic-facet denominator, new
  detector output, generic Rack/recognition-note cap or completed topic follows.

- [MIDI Tools R4 review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-tools-owner-r4-review.json)
  requires three focused source-role corrections: Recombine Dimension chooser
  and Position prerequisite before Rotate on Grid; Strum breakpoint/keyboard
  gestures are Low/High-specific; Euclidean has one shared Pattern randomization
  button, separate from individual voice toggles/Rotation sliders. R4 stays
  immutable; [preserved R5](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-tools-owner-r5-review.json) passed focused partial review: three clause/action corrections,
  all source claims/oracles/guards and72earlier records exact. All actual
  outcomes remain null/U.

- The full124-block [Racks audit](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-source-audit-review.json)
  passed independent partial source review:264assessments/22audit-only groups
  against28actual clauses/61actions. Whole-source review adopts no new laws.
  Separate [full153-block common Devices audit](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/device-chain-source-audit-review.json) passed independent partial source review (20audit-only groups, no adoption). Its source134–139
  allows custom conversion defaults, so supplied Harmony/Melody piano/synth Rack
  preview roles need factory/no-custom-default prerequisites; the conversion
  R3 retains this qualification, with old29records unchanged.
- [Primary Racks R2 review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r2-review.json) requires RACKS-R2-REVIEW-001:007/066/G05 must distinguish resizing either section at edges from moving the zone itself. Independent fade-section translation remains U; no claim it is impossible in Live. [Preserved R3](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r3-review.json) passed independent partial review:one007append/066action correction, matchingtwo substantiveplanfields;28IDs/81cases and allold61records/sourceclaims/oracles/guards exact. Additive qualification pins approved source-audit A089/A090/G05 shorthand without sealed edits. Independent fade translation remains U.

- [Tuning owner R3](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tuning-owner-r3-review.json)
  passed independent partial review:21IDs/43cases, five append fields/eleven new
  histories,32old records/97old packet files exact. Three new named UI/eight null
  documentary pairs retain actual null/U/unexecuted. Current logical MPE50/
  Tuning43/Groove34 union127 (94D12/33U) preserves the original shared83 without
  recounting it. All source, parser, numeric, receiver and lifecycle limits remain.

- [Conversion owner R3](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/audio-to-midi-owner-r3-review.json)
  passed independent partial review:14IDs/37cases,29old records exact; eight new
  histories/five clause appends plus two selected-source qualification fields.
  Four named UI/four null documentary pairs remain actual null/U. Factory/no-
  custom conversion histories qualify supplied Harmony/Melody preview structure.
  The [current integrity guide](../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/README-r3-final.md)
  preserves the first sealed path-check failure and exact two-line checker
  successor. All20old files/initial13payloads+seal remain exact; final checks
  pass with52watched paths unchanged. No new numeric/detector/default law.

- [Utility/Tuner/Spectrum full-section source audit](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/audio-utilities-source-audit-review.json) passed independent partial review:46blocks/101qualified assessments/19literalresources, nineaudit-only groups/threequestions. True old103actions/41clauses and sixDpkg file-only grades retained; no numeric/DSP/detector law or owner adoption. Productive Width AND MidSide, sustainednonzero tail, DC low/DC PLUS downstreamnonlinear necessary condition, Tuner colors/arrows and actual Spectrum manual/Auto/Max histories remain bounded. NativeMIDI112-block/235assessment source audit passed independent partial review (21audit-only groups/6questions),all27clauses146actions/threeprior corrections exact. [Filter/EQ108-block source audit](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/filter-eq-source-audit-review.json) passed independent partial review,12audit-only groups/fourquestions; [bounded ownerR4 passed independent partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/filter-eq-owner-r4-review.json),65IDs/140cases,128old exact/twelvenewnullhistories; [NativeMIDI ownerR3 passed independent partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/native-midi-effects-owner-r3-review.json),27IDs/176cases,146old exact/30newnullhistories. [CommonDevicesR5 focused review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r5-review.json) resolves COMMON-R4-REVIEW-001 historical/current no-adoption ledger clarification,38/101partial with R4behavior unchanged. [Dynamics123-block source audit passed independent partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/dynamics-source-audit-review.json),20audit-only groups/fourquestions; [bounded ownerR2 passed independent partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/dynamics-owner-r2-review.json),62unchanged clauses/153cases,129old exact/24newnullhistories. [Sample-instrument309-block source review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/sample-instruments-source-audit-review.json) required SISA-REVIEW-001/002; [focused sourceR2 review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/sample-instruments-source-audit-r2-review.json) now resolves both while preserving all old bytes. Bounded [ownerR3](../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/README-r3.md) [independently approved as partial](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/sample-instruments-owner-r3-review.json):63IDs/102cases,14newnull histories/13partial groups,20unadopted groups. [Delay/Reverb sourceR2 review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/delay-reverb-source-audit-r2-review.json) resolves DRA-REVIEW-001 inspection versus gesture, old92/149 unchanged. [Distortion216 sourceR2 correction](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/distortion-source-audit-r2-review.json) independently approved, DSA-REVIEW-001 resolved; [Modulation332 source audit](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/modulation-pitch-loop-source-audit-review.json) independently approved as partial; boundedownerR4 (106/208) independently approved as partial. [Synthesis567 sourceR2 correction](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synthesis-instruments-source-audit-r2-review.json) independently approved, SIA-REVIEW-001 resolved; boundedownerR3 (110/190) independently approved as partial. [External20source audit](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/external-hardware-source-audit-review.json) independently approved as partial; bounded [ownerR3](../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/README-r3.md) [independently approved as partial](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/external-hardware-owner-r3-review.json) (24/60,fournewnull). [ModulationownerR4](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/modulation-pitch-loop-owner-r4-review.json) independently approved as partial106/208 after230pointer-only correction; sealedfailedR3 preserved. [DelayownerR3](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/delay-reverb-owner-r3-review.json) (93/176) and[DistortionownerR3](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/distortion-owner-r3-review.json) (67/200) independently approved as partial. [Legacy114source audit](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/legacy-devices-source-audit-review.json) independently approved as partial; [boundedownerR2](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/legacy-devices-owner-r2-review.json) (77/194) independently approved as partial. [SynthesisownerR3](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synthesis-instruments-owner-r3-review.json) (110/190) independently approved as partial. Automation192source audit independently approved as partial/localBrowser194source independently approved as partial; [Project132source](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/project-media-source-audit-review.json) and[Comping38source](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/recording-comping-source-audit-review.json) independently approved as partial;ProjectownerR2 (23/53) independently approved as partial,RecordingownerR4 (34/90) independently approved as partial. No exacttarget or wholeprofile closure. Separate [Utilities ownerR2](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/audio-utilities-owner-r2-review.json) passed independent partial review:41IDs/112cases,103old records exact; only005/013Utilityappends and nineall-null histories,63D12/6file-onlyDpkg/43U. Full-lint v15 in-progress manifest-link failure preserved; [v16](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/documentation-lint-2026-10-19-v16.json) passes afterseal with zero newbrokenlinks.

Current depth selection follows [plan revision 3](research/full-live-specification-plan.md#revision-3--depth-before-breadth-2026-10-19).
[D-02 first-action review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/released-case-depth-census-review.json)
separates 1,070 bounded released case rows from six Plugin/eight Playback ungraded
draft scenarios; no released oracle or U is changed. [D-01 preflight review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-depth-preflight-review.json)
confirms 174 omitted modal occurrences and remaining routes, adding no new grade
or complete profile. [A1 traceR2](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-position-trace-review-final.json)
passed focused review resolving only its source-association finding; A1 remainsU.
[Modal diagnostics](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-modal-observability-review.json)
passed exploratory review; all174omissions remain ungraded, aliasing/measurement
uncertainty open. [Utility Mute trace](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-trace-review.json)
passed function-local static review, without public dispatch/callback delivery
proof or application grade. [Calibration review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-modal-calibration-review.json)
strengthens the lowband interpretation while retaining blocked uncertainty;
[scalar-lane review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-range-lanes-review.json)
resolves only the two local FP query lanes. Combined initialization/currentpull/converter now passed conditional source-only
review, while emission/publicA1 remain open; [model-routing review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-model-routing-review.json)
approves only partial static associations, publicMutejoinU. The later [unreviewed
connection query](../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-connection-frontier-2026-10-19.json)
retains22exactsource records: generic metadata emission/binding is narrowed,
actual queried Mute member/child and processor callback identity still unproved.
Unbacked metadata words are not evidence of runtime zeros or empty tables. The [later membership query](research/device-audio-utilities.md#d03-mute-membership-frontier--2026-10-20) narrows offset/return-register facts; actual type/name/map/processor delivery staysU.
A1/emission remainU. These static packets did not execute original code; the
later six Corpus X captures (four Ramp/sensitivity, two MIDI) and finite Ramp
release are routed underQ025. No
candidate fraction is reported. Local
Browser source review completed its already-in-flight partial scope; no new
breadth owner opens.

Cross-owner navigation remains explicit: Browser Content041 owns entry into the
User Library overview and Current Project folder reveal. Project Media023 owns
the aggregate library/project reference-management workflow and Collect and Save;
its entry mentions are prerequisites, not a new claim that navigation is absent.
Neither scope owns a proven file transaction or target-build runtime result.

## Q-051 Settings configuration and cross-owner acceptance gaps

- State: open; owner: analyst; affects bounded settings-to-operation bridges.
- Evidence: [thirteen-paragraph reconciliation](../analysis/ableton-live-12.4.3/full-spec-v1/settings-owner-reconciliation/README.md)
  and [scoped independent review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-owner-reconciliation-review.json)
  retain40subclaims with55requirement/68packet-qualified case references. These
  are historical/as-of owner subsets, not current complete-owner or target passes.
- Local entry contracts: SET-B059 Sample Editor application choice and
  SET-B066 plug-in folder location/activation controls were adopted by
  [Settings R4](../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r4.json),
  [independently reviewed as partial](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-learning-owner-r4-review.json).
  Its23requirements/33cases retain all prior clauses/actions; only these two
  configuration roles are added. Existing [discovery002](specs/plugin-discovery.md#req-plugin-discovery-002--searched-folders)
  already owns system/custom source-switch search effects; exact labels, path
  admission, initial/default and immediate-change effects remain distinct.
  Do not create a competing scanner/search contract from the overview paragraph.
- Acceptance gaps: Media MF-011 leaves Create Analysis Files at unspecified
  default options, while MF-015 explicitly sets Off. A causal comparison needs
  explicit On and Off on owned fresh no-ASD copies. [Media R4](../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/manifest-author-r4.json)
  [passed focused review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/media-file-workflows-r4-review.json),
  retaining all17clauses/32case IDs and changing only MF-011/MF-015 action fields.
  Existing documentary predicates and target U/not-run states are unchanged.
  Recording RC-020 also names
  default rather than explicitly Off; RC-021 enables its scene-record preference.
  Its [preserved R3 successor](../analysis/ableton-live-12.4.3/full-spec-v1/recording/manifest-author-r3.json)
  [passed focused review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/recording-comping-r3-review.json),
  changing only RC020action after a genuinely productive enabled baseline. All32
  clauses and81documentary comparators remain exact; original Markdown-only cases
  are explicitly transcribed, not misrepresented as an old JSON catalog.
  Source-described defaults are not matched target-state or negative-test evidence.
- Named hardware Resync in SET-B053 is distinct from port Sync enable, sending
  Clock, host tempo changes and Link Start Stop Sync. Narrow retained Routing
  source reconciliation [passed bounded review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/resync-source-reconciliation-review.json).
  [Synchronization R3](../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r3.json)
  [passed independent partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synchronization-owner-r3-review.json):
  29requirements/42cases retain27old clauses/37cases verbatim and append two
  documentary roles/five cases. Hardware results, wire payloads, drift detection,
  timing, fanout, clock phase and correction outcomes remain unknown.
- Qualifiers: Max Standard needs the add-on context in REQ-MAX-HOST-001; the First
  Steps summary does not prove every Standard install entitled. Temporary-to-saved
  recording movement is not an atomic file transaction; global launch preference
  summaries do not specify every clip-local setting. Q031 remains open for matched
  color preference/build/new-clip histories; no contradiction or RNG law is adopted.
- Next action: retain the four reviewed bounded corrections (Settings configuration,
  Media analysis On/Off, Recording scene Off and Resync roles) at their exact
  partial scopes. Continue matched-build/context evidence for remaining defaults,
  path admission, summary qualifiers and interactions; a bounded retained-native
  Q031 color trace was independently reviewed as inconclusive research only. All actual
  outcomes remain U; published releases, source bytes and historical snapshots
  stay immutable.

## Q-052 Keyboard export and MIDI-note modifier source differences

- State: open; owner: analyst; affects keyboard dispatch/source-context coverage.
- Evidence: [frozen keyboard audit questions](../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation-source-audit/source-questions.json)
  KNA-Q02 `/1` and KNA-Q03 `/2`, over seale30f1ccd…fdce1a. Its [full audit review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/keyboard-navigation-source-audit-review.json)
  requires KNA-REVIEW-001: table27 adjacent/general Computer MIDI text is not
  established as a prerequisite for every toggle/binding. The [preserved R2 association correction](../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation-source-audit/README-r2.md)
  [passed focused independent review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/keyboard-navigation-source-audit-review-final.json),
  resolving KNA-REVIEW-001 through fifteen field deltas across five reconciled rows.
  B350 remains supported enabled octave/velocity context, related-only for toggles;
  B351 is general related context. Original292rows and these differences stay exact.
  Root separately [reconstructed these seven raw fragments](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/keyboard-shortcut-source-differences-check.json),
  verifying both original capture hashes, exact character/line/column spans and
  four unchanged original binding identities. This checks only the named source
  differences, not all641audit facets or command behavior.
- Export: accessibility KN1:B079, HTML280:20474, says CtrlR/CmdR opens the export
  dialog after a timeline-region selection. Shortcut table BIND-T04-R007
  (`shortcut-bindings.json /40`, source KN2:B051, HTML280:10853) says
  CtrlShiftR/CmdShiftR for Export Audio/Video. Its Rename row BIND-T06-R008
  (`/60`, KN2:B075, HTML280:13540) says CtrlR/CmdR. Do not select one unqualified
  dispatch behavior or silently repair the retained catalog.
- MIDI notes: accessibility KN1:B093/B094, HTML280:22767/22926, names Windows
  Ctrl with up/down for previous/next note and left/right for the same pitch.
  Shortcut rows BIND-T15-R019/R020 (`/141`, `/142`, KN2:B174/B175,
  HTML280:24883/25021) name Windows Alt for the corresponding selection labels.
  Mac Option agrees in both; focus, selection, same-pitch meaning and version
  context still need matching before declaring identical commands or a defect.
- Source identities: accessibility SHA39757eb6…ea2a8 captured
  2026-10-19T20:38:44.759910+00:00; shortcut chapter SHA9a754776…ce908 captured
  2026-10-19T20:38:45.992669+00:00. Both declare Version12, not exact12.4.3.
  Paragraph/row direct anchors remain null; heading URLs are context only.
  Derived table separators are not literal source text or key grammar.
- Owner adoption: [R5 passed independent partial review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/keyboard-navigation-owner-r5-review.json):
  40requirements/96cases, retaining both source differences and the corrected
  association distinctions. All actual outcomes remain U/null/unexecuted.
- Next action: exact-build/platform/focus dispatch evidence is needed to resolve
  the choice. A [selected macOS menu-resource query](../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-menu-static-context/README.md)
  [passed inconclusive research-only review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/keyboard-menu-static-context-review.json):
  the application/Help scaffold contains no matching Export/Rename/note-selection
  evidence. This is not command absence or runtime dispatch proof; no requirement,
  case or coverage credit follows. All292binding rows remain
  discovery-only; no OS/reader/application/input action was executed.


## Q-053 MIDI utility gesture and Humanize source contexts

- State: open; owner: analyst; affects exact source/gesture/selection applicability.
- Evidence: [Clip View audit questions](../analysis/ableton-live-12.4.3/full-spec-v1/clip-view-source-audit/source-questions.json)
  CVA-Q02/Q03 and [independent partial audit review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/clip-view-source-audit-review.json).
  Complete retained Clip View text was read; this is not renewed complete MIDI
  source/owner acceptance or a target observation.
- Add Interval: CV:B122, HTML708, separates Interval Size selection from the
  Add Interval button. The [selected retained MIDI source query](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-utility-source-context-query.json)
  reconstructs §10.5.9.4, HTML588 paragraph2, characters84834–85289: with selected
  notes, changing Interval Size adds and selects new notes without an extra button;
  with no selection, the slider sets the interval and Add Interval applies it to
  all existing clip notes. Existing [MIDI011](specs/midi-editing-tools.md) already
  owns this distinction; MED-011 exercises Fit to Scale. No new requirement or
  zero-time deadline follows. [Owner R2 passed narrow independent review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-editing-interval-owner-r2-review.json):
  43unchanged requirements/57verbatim old cases plus MED058–060 selected-slider,
  no-selection slider-alone and actual-button trials. Productive matched button
  baseline and exact separate reset precede the no-effect trial.
- Humanize: CV:B126, HTML720, says up to half a grid division with separate Amount
  and Humanize controls. MIDI012 and MED-012 retain a quarter-grid bound in each
  direction. Total span versus one-sided displacement is a hypothesis, not an
  adopted equivalence, changed RNG/displacement law or declared source defect.
- Source identity: Clip View Version12 capture2026-10-19T21:25:35.853607+00:00,
  SHA30f156e6…51bd80; exact12.4.3 applicability remains U. The audit retains exact
  MIDI clause as-of snapshot and qualified MED-011/MED-012 catalog pointers.
  Source paragraph anchors remain null with actual heading ancestry.
- MIDI capture is dated2026-10-19 with exact UTC unknown; the query timestamp
  is separate. Its five complete selected MIDI records and two Clip View records
  were independently checked during the focused owner review, not the entire
  244-block MIDI chapter. Version12 does not establish exact12.4.3 applicability.
- Bounded retained-native progress: [Humanize static context](../analysis/ableton-live-12.4.3/full-spec-v1/humanize-static-context/README.md)
  [passed independent inconclusive research review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/humanize-static-context-review.json). Sixteen complete retained bodies,
  eleven selected relevant index records, seven actual direct-call records and
  512literal binary bytes provide private navigation context. Exact arm64 target
  hash was reverified. Matching names and private coefficients do not establish
  the public control/kernel binding, current-grid/variation input or final note
  transformation. Q053 remains open with zero requirements/cases/behavioral credit;
  no original code, native project or runtime was executed.
- [Producer follow-up](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/humanize-context-producer-followup.json)
  [passed independent inconclusive review](../analysis/ableton-live-12.4.3/full-spec-v1/reviews/humanize-context-producer-followup-review.json):16additional
  complete bodies/43730codebytes identify a conditional privatecontext+0x28setter
  and generic indirect0x190 call. The context initializer uses qword index5
  (sixth slot,byteoffset0x28); the review qualifies the retained report's ordinal
  wording. Seed+0x64 is distinct. Public provider/grid/FP-ABI/control binding and
  Q053 remainU; no runtime or new behavioral credit. All16watched paths exact.
- Next action: establish the actual constructed panel/controller/kernel/input path if retained evidence
  permits. Resolve Humanize's public source context only with that evidence. Setting a value and actually invoking a button stay distinct;
  independent valid notes and productive tool baselines are future prerequisites.
  All60MIDI cases remain actual-null/U/unexecuted; no original tool/UI/MIDI action
  or candidate ran, and no required target outcome closes.


The shared [DeviceKit provider frontier](research/program-structure.md#devicekit-provider-frontier--2026-10-20) records missing retained package/import inputs andunresolved consumerimport→library→providerbody→sameinstance/publicreceiver joins. Its approvedmetadata inventory supplies no publicDeviceKit binding. A capped consumerloadcommand collector is preparationonly;symbol/bind/provider expansion requires separateselection. No absence/infeasibility claim or coverageclosure.


The [consumerloadcommand actualapproval](research/program-structure.md#consumer-load-command-actual-approval--2026-10-20) validates6,976metadata bytes and27prospectivestubindices,without providerbinding. A separatelyselected bounded27word/nlist/name collector is preparationonly;no tabledata read orvaluepointer/providerfiles followed. Existing DeviceKit currentreceiver/control/output/lifecycle gaps remainunknown,notabsence/infeasibility.


DeviceKit frontier update: [selected symbol declarations](research/program-structure.md#selected-devicekit-symbol-review-approval--2026-10-20)
passed independent review. All27 declared values locate retained export records;
the selected whole-set source batch is pending. Actual weak binding, reached
receiver/control/ABI and output delivery remain unknown; no question closes or
gains a behavioral grade from a declaration or source locator alone.


The [Synthesis map approval](research/synthesis-instruments.md#synthesis-family-route-review-approval--2026-10-20)
retains Operator Loop/Beat/Sync and Meld count/scale/sign ambiguities. Typed
Wavetable prefixes establish no current algorithm/phase/voice or output law.
All585required route units remain U; no question is closed by the map.


The [Legacy family map approval](research/legacy-native-devices.md#legacy-family-route-review-approval--2026-10-20)
keeps predecessor applicability, legal oldSet/current receiver/control/output,
exact math and lifecycle unknown. File identity and complete selected metadata
frontiers establish no application outcome or closed question.


[DeviceKit fixed27 source review](research/program-structure.md#devicekit-fixed27-source-review-approval--2026-10-20)
confirms local dispatch/list/queue relationships while actual weak destination,
legal receiver/ABI/helper effects, current controls/timebase and audio consumer
remain unknown. New source anchors and declarations do not close these questions.


[Seven-delegate DeviceKit review](research/program-structure.md#devicekit-seven-delegate-source-review-approval--2026-10-20)
retains visible callee/parent argument and return mismatches; native ABI and
current weak-provider/control/audio binding remain unknown. [Remaining67 Synthesis
review](research/synthesis-instruments.md#remaining67-synthesis-source-review-approval--2026-10-20)
retains expanded four-byte source projections and Operator/Meld/voice/clock/output
gaps. Local offsets, thresholds and arithmetic close no public-behavior question.


[Wavetable17 review](research/synthesis-instruments.md#wavetable-phase17-source-review-approval--2026-10-20)
localizes packed lookup argument/return/native FP questions; conditional 16 KiB
lookup bounds exclude ModernPd's additional +0x4000 field. [Automation50 review](research/automation-envelopes.md#automation-withheld50-construction-review-approval--2026-10-20)
retains legal factory/list/partial-initializer/provider/Pan ABI prerequisites.
Neither closes a current control/voice/timebase/audio or public-behavior question.


[Wavetable's two local lookup native contracts](research/synthesis-instruments.md#wavetable-lookup164-native-review-approval--2026-10-20)
now establish X0/X1/S0 reads, four binary32 lanes, fused stage order and fullV0
availability. Current index remains unmasked; actual table/caller/FP/runtime and
x86 equivalence remain unknown. Metadata counterpart selection answers none of
those behavior questions by itself.


[Automation's M boundary batch](research/automation-envelopes.md#automation-m-boundary-proposal-approval-and-actual-pending-review--2026-10-20)
retains five scoped local-oracle discrepancies pending peer actual review;
native operation order/FP cause and public load/save delivery remain unknown.
[Modulation122](research/modulation-pitch-loop-devices.md#modulation-whole122-source-review-approval--2026-10-20)
source review closes no native-ABI/legalstate/control/audio question. Unused
OnFeedback secondargument is declaredvoid*, not a declaredscalar; no ABI repair.


[Wavetable typed8 locator review](research/synthesis-instruments.md#wavetable-x86-typed8-metadata-review-approval--2026-10-20)
leaves other exact trailing-NUL occurrences unknown. Suffix sharing is a
hypothesis, not an observed cause or native absence; Root separately selected
that exact-eight locator question. M native-operation-order remains unknown;
start metadata is selected to scope a later static investigation only.


[Automation M actual review](research/automation-envelopes.md#automation-m-boundary-actual-review-approval--2026-10-20)
confirms AMB-ACT-F01–F05 as local-oracle discrepancies. Operation-order/FP cause,
ARM and public loaded-event/Save/output questions remain open. No count of NULL
rows or five discrepancies is a whole-product denominator or implementation failure.
