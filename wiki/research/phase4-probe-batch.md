---
id: RESEARCH-PHASE4-PROBE-BATCH
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Phase 4 reference observation batch

Phase 4 of [roadmap revision 2](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17)
collects every runtime-dependent question into one prepared batch for the macOS
host, under the [ADR 0002 escalation rule](../decisions/adr-0002-static-first-analysis.md#runtime-escalation-rule).
This page is the run sheet. Nothing here has been run. Live cannot run on the
Linux analysis host, and the batch is not a gate for Phases 1–3.

**Files** (all in `analysis/ableton-live-12.4.3/r2/phase4-batch-v1/`):

- [batch.json](../../analysis/ableton-live-12.4.3/r2/phase4-batch-v1/batch.json): the merged records.
- [fixture-plan.json](../../analysis/ableton-live-12.4.3/r2/phase4-batch-v1/fixture-plan.json): every input, and whether it exists.
- [manifest.json](../../analysis/ableton-live-12.4.3/r2/phase4-batch-v1/manifest.json): SHA-256 of each file and of each source read.
- `build_batch.py`: regenerates all three from the sources (`python3 -I`, from the repository root).

Each record keeps its original ID and source locator. The builder adds normalized
fields: question, why static evidence is insufficient, affected IDs, prerequisites,
minimal inputs, procedure, discriminating observation, stop condition, host risk,
minutes and what it unblocks. `batch_derived_fields` names the fields the batch
wrote rather than copied. Observations and stop conditions are copied verbatim
and never invented.

## Sources and counts

| Packet | Source of the records | Records |
| --- | --- | --- |
| S4 MIDI | [s4 probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/probe-batch.json), listed in [MIDI closure](midi-closure-r2.md#phase-4-probe-batch) | PRB-S4-01–16 (16) |
| N1 transport state | [n1 probe-batch.json](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/probe-batch.json), listed in [transport-state native](transport-state-native.md#phase-4-probes) | PRB-N1-01–08 (8) |
| N2 container | [n2 probe-batch.json](../../analysis/ableton-live-12.4.3/r2/n2-container-v1/probe-batch.json), listed in [document container native](document-container-native.md#remaining-unknowns-and-phase-4-probes) | PRB-N2-01–07 (7) |
| N3 transitions | [escalation record](transport-transitions-native.md#adr-0002-escalation-record) (no ID on the page) | ESC-N3-01 (1, ID assigned here) |
| N4 helper launch | [helper launch](helper-launch-live-side.md#phase-4-probe-records) | PRB-N4-01–09 (9) |
| N5 device mapping | [device parameter mapping](device-parameter-mapping-native.md#phase-4-probe-records) | P4-N5-01–04 (4) |
| H1 plug-in scanner | [h1 probe-batch.json](../../analysis/ableton-live-12.4.3/r2/h1-plugin-scanner-v1/probe-batch.json), listed in [plug-in scanner](plugin-scanner-static.md#phase-4-probe-batch) | PRB-H1-01–08 (8) |
| H2 browser index | [h2 probe-batch.json](../../analysis/ableton-live-12.4.3/r2/h2-index-v1/probe-batch.json), listed in [browser index](browser-index-static.md#phase-4-probe-batch) | PRB-H2-01–09 (9) |
| H4 device bundles | [device bundles](device-bundles-static.md#phase-4-probe-records) | P4-H4-01–05 (5) |
| H5 Push 3 | [Push 3 helper](push3-helper-static.md#phase-4-probe-records) | P5-01–09 (9) |
| Unprepared requests | [Corpus candidates](corpus-dsp-static.md#candidate-requirements-for-spec-corpus-device), [H6 unknowns](web-addons-swapper-static.md#unknowns-and-questions-for-the-main-live-project), [study P1](native-transport-study.md#study-p1-loop-enable-persistence) | P4B-CORPUS-01, P4B-H6-01, P4B-T1-01 (3, IDs assigned here) |

Total: 79 records, 75 with original IDs. No other probe or escalation record was
found under `analysis/ableton-live-12.4.3/r2/` (searched for `probe`, `Phase 4`,
`escalat` and the ID patterns). Every other `Phase 4` mention in `wiki/research`
and `wiki/specs` points at one of these records. The H4 section on device signal
behavior is not a Phase 4 record. It asks for measured original-versus-candidate
audio under FEAT-AUDIO, which is verification work.

## Merged and duplicate records

All original IDs are kept. A record folded into another costs 0 minutes.

| Group | Records | Disposition |
| --- | --- | --- |
| M-SAVE | PRB-N1-07 (primary), PRB-N2-01 | Two 12.4.3 saves back to back, with one decode routine; the inputs differ (edited lesson set versus new set) |
| M-SCAN-ARGV | PRB-N4-01 (primary), PRB-H1-01 (duplicate) | Same question; N4-01 carries the sharper static prediction. H1-01's custom-folder and VST2 toggles are kept as steps |
| M-SCAN-RELAUNCH | PRB-H1-02, PRB-H1-04 (primaries), PRB-N4-02 (near-duplicate) | N4-02's log lines and launch counts are read during H1-02 and H1-04 |
| M-INDEX-LAUNCH | PRB-N4-03 (primary), PRB-H2-01 (duplicate) | One capture; H2-01 adds its 60 s stop |
| M-PUSH3-PROC | P5-02 (primary), PRB-N4-08 (near-duplicate) | Same socket capture; N4-08 keeps its kill-and-relaunch timing step |
| M-DEV-DEFAULTS | P4-H4-01 (primary), P4-H4-03, P4-N5-03 (near-duplicates) | Fresh-insert saves in H4-01 answer N5-03 and half of H4-03. H4-03 keeps its `Defaults/*.adv` edit step |
| M-T1-LOOP | P4B-T1-01 (superseded) | Covered by PRB-N1-01, 02, 07 and 08, except for P1-F |

Related but kept separate: PRB-N1-01, 06 and 08 with PRB-N2-03 (they share the read-error dialog);
PRB-N2-04 with 05; PRB-H1-03 with PRB-N4-05 (hung versus never-connected helper);
PRB-S4-06 with ESC-N3-01 (Play and Stop from MIDI versus the UI).

## Flagged records

**Incomplete. These lack a discriminating observation or a stop condition, and none was invented:**

- P4B-CORPUS-01. The Corpus page asks Phase 4 to measure CD-C01–CD-C08, but it gives
  no input, observation or stop condition. It also needs an audio capture harness and
  tolerances ([Q-001](../questions.md#q-001-compatibility-targets)).
- P4B-H6-01. "Runtime confirmation" of helper order, timing and network traffic. It
  would need network access, which conflicts with the safety rules below.
  PRB-N4-06 and 07 cover part of it.
- P4B-T1-01. The optional probe from study P1 has no stop condition and no chosen
  discriminating result. P1-F (undo and redo of loop enable) is not covered by any
  prepared probe.

**Contradiction to resolve.** The `requirements` in the N1 probe-batch.json predate
the r1 numbering of [SPEC-TRANSPORT-STATE](../specs/transport-state.md):

| Record | Lists | The spec cites it under |
| --- | --- | --- |
| PRB-N1-02 | 006 | 007 |
| PRB-N1-06 | 010 only | 009 and 010 |
| PRB-N1-07 | 011 and a nonexistent 013 | 002 and 008, with 011 |
| PRB-N1-08 | 007 and 008 | 008 |

`affected_ids` follows the spec and the original list is kept as `original_affected`.
PRB-N2-02 adds REQ-ALS-CONTAINER-007 from the spec's table.

**Input or tool gaps.**

- PRB-N2-04 needs an N2-019 copy without Creator, which is not among the 27 cases.
- PRB-S4-10 does not name its 3-bank device.
- PRB-H2-09 has no source for a `.wma` file.
- PRB-H2-07 needs a destination pack installed.
- ESC-N3-01 and P4-H4-04 need a LOM harness.
- P5-05 needs a USB capture tool.
- No record covers TS-010 (a meter code with spaces on both sides). The staged
  transport-state candidate excludes it, along with REQ-009, REQ-012, TS-017–019
  and TS-023 (`analysis/ableton-live-12.4.3/handoff-staging/transport-state-v1/spec.md`,
  read on 2026-10-17 while still in progress).

PRB-S4-09 and S4-11 wait for cheaper static traces, as their own records say.

## Safety measures

1. Never run or modify the installed application. Make a disposable copy with `ditto`.
   Check the universal executable SHA-256 `52289af6…7a35ef`
   ([source page](sources/ableton-live-12.4.3.md#identity-and-retained-evidence)) before each session.
   Use a second, modifiable copy only in session J, and delete it afterwards.
2. Use a separate macOS user account. If that is not possible, back up Live's
   preference, application-support, cache and User Library folders, and record
   their paths and hashes before and after each session.
3. Keep the network off. Only P5-07 needs a local link (no internet route). With
   the network off, an update cannot download and the swapper cannot act on the
   app (see [web connector](helper-launch-live-side.md#web-connector)).
4. Never sign in to an Ableton account. Decline any update, authorization or
   Push firmware prompt.
5. Test plug-ins go into the test account's `~/Library` only. `/Library` is used
   only for PRB-N4-01 and H1-08, and only with approval.
   Remove them after session H.
6. Restart Live between probes unless the procedure says otherwise. Capture
   Live's `Log.txt` after every probe and record its actual path at setup.

## Run sheet

Times include relaunches and capture, but not fixture construction. The sessions
total 1,425 minutes (about 24 hours) before the deferred group. That is more than
one sitting; see [decisions needed](#decisions-needed-before-the-sitting).
Sessions 0 and A–D (415 minutes) settle the handoff blockers and all document probes.

### Session 0 — Setup and identity pinning (45 min)

Create the account (or the backup) and the app copy, and pin the hashes. Check
every tool the later sessions rely on: `shasum`, `gzip`, `xxd`, `sqlite3`, `ps`,
`lsof`, `vmmap`, `tcpdump`, screen recording at 60 fps or more, the IAC bus, a
MIDI sender and monitor, and a debugger. Record any missing tool. Do not
install one without approval.

### Session A — Handoff blockers: saves, precedence, container failures (110 min)

Needs the app copy, [N2 cases](../../analysis/ableton-live-12.4.3/r2/n2-container-v1/cases.json),
`N2-001.als` as the N1 base, and the constructed N1 variants.

| # | Record | Do and observe | Min | Unblocks |
| --- | --- | --- | --- | --- |
| 1 | PRB-N1-07 | Edit the base to tempo 121.2, 7/8, loop 0.5 + 3.3 beats; save; decode number text, child order, KeyMidi, envelopes, SchemaChangeCount | 15 | H2 transport-state candidate: REQ-002, 008, 011 |
| 2 | PRB-N2-01 | New set, save; first 10 gzip bytes and first three XML lines | 10 | H3 container candidate: REQ-007, 008 |
| 3 | PRB-N1-04 | Three Manual/EnumEvent meter pairs; displayed meter and re-saved values | 15 | REQ-TRANSPORT-STATE-012 and the 007 meter default |
| 4 | PRB-N1-05 | Three tempo variants including an enabled scene tempo; displayed tempo | 15 | REQ-TRANSPORT-STATE-012 |
| 5 | PRB-N2-02 | Open plain-XML N2-002, save; magic `1f 8b` or `<?` | 10 | REQ-ALS-CONTAINER-001, 007 |
| 6 | PRB-N2-03 | Ten corrupt cases; dialog text, Log.txt, whether the previous set stays open | 30 | REQ-ALS-CONTAINER-009 |
| 7 | PRB-N2-04 | N2-013, N2-019, N2-019 without Creator; the version named | 15 | REQ-ALS-CONTAINER-004 |

### Session B — Transport timing, S3 escalation (40 min)

Needs screen recording; the LOM harness is needed for the lag measurement only.

| # | Record | Do and observe | Min | Unblocks |
| --- | --- | --- | --- | --- |
| 1 | ESC-N3-01 | Play, Stop, Stop from bar 5; Play+Stop within 50 ms; loop-is-song-start Play. Position display, saved `CurrentTime`, `is_playing` lag | 40 | T-03, T-05, T-08 and T-13 of the [transition table](transport-transitions-native.md#transition-table); no transitions spec yet |

### Session C — Corpus position range (80 min)

Needs a debuggable re-signed copy (a user decision). Skip to session D if it is not approved.

| # | Record | Do and observe | Min | Unblocks |
| --- | --- | --- | --- | --- |
| 1 | P4-N5-01 | Log (index, value) at `_SetParameterA` for Amp, Electric, Corpus; ExcitationX 0/1 arrives as 0/1 or −1/1 | 60 | SPEC-CORPUS-DEVICE candidates and the [position range](corpus-dsp-static.md#host-parameters) contradiction |
| 2 | P4-N5-02 | `_CreateInstanceU` hits per inserted device | 20 | DEV-M08 |

### Session D — Remaining document-load probes (140 min)

Same prerequisites as session A.

| # | Record | Do and observe | Min | Unblocks |
| --- | --- | --- | --- | --- |
| 1 | PRB-N1-01 | LoopOn `1`, `0`, `TRUE`, empty | 15 | REQ-TRANSPORT-STATE-003 |
| 2 | PRB-N1-02 | Missing LoopStart, Value, tempo Manual: 8/16/120 or template | 20 | REQ-TRANSPORT-STATE-007 |
| 3 | PRB-N1-03 | Six out-of-range values; displayed and re-saved | 30 | TS-017, TS-018 |
| 4 | PRB-N1-06 | Meter codes 495, −1, `201.0` | 15 | TS-019 |
| 5 | PRB-N1-08 | Duplicate child, unknown child, unknown attribute (uses A1's SchemaChangeCount) | 20 | REQ-TRANSPORT-STATE-008 |
| 6 | PRB-N2-05 | N2-018, N2-020: corrupt or newer-version | 10 | REQ-ALS-CONTAINER-004, 005 |
| 7 | PRB-N2-06 | Six accepted envelope variants open as sets | 25 | Cases N2-012, N2-014 |
| 8 | PRB-N2-07 | Truncated gzip N2-027 | 5 | Case N2-027 |

### Session E — Built-in device saves and defaults (135 min)

| # | Record | Do and observe | Min | Unblocks |
| --- | --- | --- | --- | --- |
| 1 | P4-H4-01 | Save each device fresh and from presets, plus one set; XML diff | 60 | DEV-C01–C09 |
| 2 | P4-N5-03 | Read Electric `PickupAmpIn` (0.42 or 0.5) from E1 | 0 | DEV-M04 |
| 3 | P4-H4-02 | Out-of-domain Amp and Analog preset copies; shown and re-saved value | 30 | DEV-C05, DEV-M06 |
| 4 | P4-H4-04 | Parameter-table dump, only if the API and harness exist | 30 | DEV-M05 |
| 5 | P4-H4-05 | Amp at 32 kHz: output and message | 15 | Device rate behavior |

### Session F — MIDI remote-script profiles (190 min)

Needs the IAC bus, a MIDI sender and a monitor, and the probe profiles. Order
follows the records. Run S4-02 only after S4-01 shows listing works.

| Records | Min | Unblocks |
| --- | --- | --- |
| PRB-S4-01, 02 (listing, names, restart) | 25 | REQ-MIDI-USER-001, unreleased in [midi-config-v2](../../handoff/midi-config-v2/README.md) |
| PRB-S4-03, 04 (raising profile, unknown mode) | 30 | Q-008 host outcomes excluded from midi-config-v2 |
| PRB-S4-05 (Absolute scaling) | 10 | REQ-005d, 010d |
| PRB-S4-06, 07 (transport toggles, seek timing) | 25 | REQ-MIDI-USER-004, unreleased |
| PRB-S4-08, 10, 11, 12 (pads, bank and lock, strip order, toggles) | 55 | REQ-006, 008, 009, 011 clauses |
| PRB-S4-13 (mute feedback bytes) | 15 | REQ-011e |
| PRB-S4-14, 15, 16 (reload, teardown, encoding) | 30 | [Q-010](../questions.md#q-010-midi-discovery-lifecycle-and-interaction) |

### Session G — Helpers and browser index, no plug-ins or hardware (240 min)

Needs a small disk image (under 3 GiB free) and a removable one, and generated media.

| Records in order | Min | Unblocks |
| --- | --- | --- |
| PRB-N4-03 with H2-01 (index argv and options file), H2-02 (database name and version) | 15 | [Q-014](../questions.md#q-014-browser-index-behavior) |
| PRB-H2-03, 05, 09 (change detection, unmount and move, bad media) | 60 | BI-C05, C07, C08, C11 |
| PRB-N4-07 (swapper guard, exit 42), N4-09 (built-in MultiF0 log line) | 25 | Q-015, Q-013 |
| PRB-N4-04 (restart caps 100 and 10) | 40 | Q-014, Q-015 |
| PRB-N4-06 (web connector args; under 3 GiB free) | 40 | Q-015 |
| PRB-H2-06 (corrupt, newer and foreign databases), H2-08 (sound analysis) | 60 | BI-C09 |

### Session H — Plug-in scanner with test plug-ins (195 min)

Needs the test VST3 builds (a user decision) and process-argument capture.

| Records in order | Min | Unblocks |
| --- | --- | --- |
| PRB-N4-01 with H1-01 (argv per source configuration and Rescan kind) | 30 | PD-02, PD-11, PD-14 |
| PRB-H1-02 with N4-02 (crash: launches, scanstate 0→4→2), then H1-05 (fingerprint) | 50 | PD-10 and PD-07; [Q-016](../questions.md#q-016-plug-in-discovery-live-side-contract) bars PD-10 without it |
| PRB-H1-03 (hang; stop at 15 min) | 25 | Timeout policy |
| PRB-H1-04 with N4-02 (60 modules; chunks) | 40 | PD-12; Q-016 bars it without this probe |
| PRB-H1-06, 07, 08 (AU path, database folder, duplicates) | 50 | PD-14, Q-016 |

### Session I — Push hardware (155 min)

Needs a Push 3, and a Push 2 for P5-06. P5-07 alone needs a local link.

| Records in order | Min | Unblocks |
| --- | --- | --- |
| P5-01, P5-02 with N4-08 (launch arguments, sockets, relaunch after 1.5 s) | 40 | Q-015; Push scope ([Q-005](../questions.md#q-005-whole-app-scope-expansion)) |
| P5-03, 04 (watchdog, hotplug) | 45 | Q-015 |
| P5-05, 06, 07, 08, 09 (display frames, Push 2, network, MIDI path, shared memory) | 70 | Q-015 |

### Session J — Modified-copy probes, run last (95 min)

Use a second disposable copy that may be modified, and delete it afterwards.

| Records | Min | Unblocks |
| --- | --- | --- |
| P4-H4-03 (edited `Defaults/Instruments/Analog.adv`) | 15 | DEV-C08 |
| P4-N5-04 (no `Corpus.bundle`; record as infeasible if the copy will not launch) | 20 | DEV-M10 |
| PRB-N4-05 (stub helpers: about 60 s and 5 s kills) | 45 | Q-015, Q-016 |
| PRB-H2-04 (tag a user sample and a Core Library preset; find the XMP) | 15 | BI-C08 |

### Deferred

- PRB-S4-09 waits for the `_Generic/Devices` trace.
- PRB-H2-07 waits until a destination pack is available.
- P4B-CORPUS-01, P4B-H6-01 and P4B-T1-01 are incomplete (see above).

## Evidence per probe

Retain one directory per record at `analysis/ableton-live-12.4.3/r2/phase4-run-v1/<record id>/`
on the macOS host, then copy it to this host:

- `inputs/`: each input used, with its SHA-256;
- `captures/`: screenshots or recordings, the `Log.txt` excerpt, `ps`, `lsof` and
  `sqlite3` output, saved files and their decoded XML;
- `result.json`: date and time, the app copy's path and executable SHA-256,
  preference hashes before and after, the steps actually run, the observation
  verbatim, an outcome (`matches prediction`, `contradicts` or `inconclusive`),
  the stop reason, and any deviation.

Add a run `manifest.json` with every file's SHA-256. Keep recordings, packet
captures and USB captures out of Git until they have been reviewed, because they
may hold identifiers. There is no copy route from the macOS host yet
([G0.2](native-phase-execution.md)). After the run, update each source page's
probe section and the affected spec, mark derived assumptions stale where an
outcome contradicts them, and append a log entry.

## Checklist before the sitting

- [ ] Get the user's decisions below.
- [ ] Build and hash the missing documents: the 25 N1 variants, N2-019 without
      Creator, and the H4 and N5 preset copies. Build them in a separate, approved
      step; this packet builds no documents from shipped content.
- [ ] Write the S4 profiles (about 25 folders), generate the WAV files and the
      bad-media set, and pick the 3-bank device for PRB-S4-10.
- [ ] Verify the N2 cases against `cases.json`.
- [ ] Build and sign the test VST3s and the stub helpers, if approved.
- [ ] Try the cheap static traces first: `_Generic/Devices` (S4-09) and
      `_Framework/MixerComponent` (S4-11).
- [ ] Prepare the disk images, and the hardware if it is available.
- [ ] Settle the evidence copy route to the Linux host.
- [ ] Print this sheet and the `result.json` field list.

## Decisions needed before the sitting

- **Length.** Run everything over two or three days, or only sessions 0 and A–D
  (about 7 hours) first.
- **Isolation.** Use a separate macOS account or a backup of the preferences.
  How Live is authorized in a new account without signing in is not known.
- **Debugging (session C).** Re-sign a copy, change SIP, or skip P4-N5-01 and 02.
- **LOM harness** for ESC-N3-01 and P4-H4-04: a Max for Live device or a
  control-surface script.
- **Test plug-ins (session H).** Needs a build toolchain and the public VST3 SDK,
  which needs network on a build machine. Installing into `/Library` needs admin.
- **Modified copies (session J)** and the stub helpers.
- **Hardware.** Push 3 and Push 2, a 32 kHz audio device, and a USB capture tool.
- **Network.** A local link for P5-07; P4B-H6-01 stays out unless approved.
- **Tool installation on the macOS host**, such as a MIDI sender.

## Limitations

Time estimates are planning guesses. Static predictions in the records are
derivations, not observations. Tool availability on the macOS host is unverified.
Sources were read at the hashes in `manifest.json`. Pages edited later may add
records that this batch does not include.
