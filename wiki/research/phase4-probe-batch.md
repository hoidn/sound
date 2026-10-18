---
id: RESEARCH-PHASE4-PROBE-BATCH
type: research
status: draft
updated: 2026-10-18
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

- [batch.json](../../analysis/ableton-live-12.4.3/r2/phase4-batch-v1/batch.json): the first 79 merged records.
  The 67 later records are merged on this page only; `build_batch.py` does not read their sources yet.
- [fixture-plan.json](../../analysis/ableton-live-12.4.3/r2/phase4-batch-v1/fixture-plan.json): every input, and whether it exists.
- [manifest.json](../../analysis/ableton-live-12.4.3/r2/phase4-batch-v1/manifest.json): SHA-256 of each file and of each source read.
- `build_batch.py`: regenerates all three from the sources (`python3 -I`, from the repository root).
- [sources-2026-10-18.json](../../analysis/ableton-live-12.4.3/r2/phase4-batch-v1/sources-2026-10-18.json): SHA-256 of each source read for the later records.

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
| S5 clip launch | [s5 probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s5-clip-launch-v1/probe-batch.json), listed in [clip launch](clip-launch.md#phase-4-probes) | PRB-S5-01–11 (11) |
| S6 automation | [s6 probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s6-automation-v1/probe-batch.json), listed in [automation envelopes](automation-envelopes.md#phase-4-probes) | PRB-S6-01–07 (7) |
| S6 proposals | [Automation spec open questions](../specs/automation-envelopes.md#open-questions); not in the S6 file | PRB-S6-08–11 (4) |
| S7 MIDI notes | [s7 probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/probe-batch.json), listed in [MIDI note storage](midi-note-storage.md#phase-4-probes) | PRB-S7-01–10 (10) |
| S8 warp | [s8 probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/probe-batch.json), listed in [warp markers](warp-markers.md#phase-4-probes) | PRB-S8-01–11 (11) |
| S9 mixer | [s9 probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s9-mixer-v1/probe-batch.json), listed in [mixer values](mixer-values.md#phase-4-probes) | PRB-S9-01–08 (8) |
| N6 device tables | [device tables native](device-tables-native.md#phase-4-probe-records) | P4-N6-01 (1) |
| N7 MIDI transforms | [n7 probe-records.json](../../analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/probe-records.json), listed in [MIDI transforms](midi-transforms-native.md#probe-records) | PRB-N7-01–05 (5) |
| N8 x86_64 paths | [Live x86_64 paths](x86-live-paths.md#probe-records-runtime-only) | PRB-N8-01–05 (5) |
| Browser index proposals | [Browser index spec open questions](../specs/browser-index.md#open-questions); not in any probe-batch file | PRB-BI-01–05 (5) |

Total: 146 records, 142 with original IDs: the 79 of batch v1 and 67 merged on
2026-10-18 (S5 to the browser index proposals). No other probe or escalation record was
found under `analysis/ableton-live-12.4.3/r2/` (searched for `probe`, `Phase 4`,
`escalat` and the ID patterns) or in `wiki/` (searched again on 2026-10-18 for `PRB-`,
`P4-`, `P5-`, `P4B-` and `ESC-`). Every other `Phase 4` mention in `wiki/research`
and `wiki/specs` points at one of these records. The H4 section on device signal
behavior is not a Phase 4 record. It asks for measured original-versus-candidate
audio under FEAT-AUDIO, which is verification work.

## Merged and duplicate records

All original IDs are kept. A record folded into another costs 0 minutes.

| Group | Records | Disposition |
| --- | --- | --- |
| M-SAVE | PRB-N1-07 (primary), PRB-N2-01, PRB-S9-07, PRB-S7-09 | Four 12.4.3 saves back to back, with one decode routine; the inputs differ (edited lesson set, new set, new set with an inserted audio and return track, newly drawn MIDI clip) |
| M-SCAN-ARGV | PRB-N4-01 (primary), PRB-H1-01 (duplicate) | Same question; N4-01 carries the sharper static prediction. H1-01's custom-folder and VST2 toggles are kept as steps |
| M-SCAN-RELAUNCH | PRB-H1-02, PRB-H1-04 (primaries), PRB-N4-02 (near-duplicate) | N4-02's log lines and launch counts are read during H1-02 and H1-04 |
| M-INDEX-LAUNCH | PRB-N4-03 (primary), PRB-H2-01 (duplicate) | One capture; H2-01 adds its 60 s stop |
| M-PUSH3-PROC | P5-02 (primary), PRB-N4-08 (near-duplicate) | Same socket capture; N4-08 keeps its kill-and-relaunch timing step |
| M-DEV-DEFAULTS | P4-H4-01 (primary), P4-H4-03, P4-N5-03 (near-duplicates) | Fresh-insert saves in H4-01 answer N5-03 and half of H4-03. H4-03 keeps its `Defaults/*.adv` edit step |
| M-T1-LOOP | P4B-T1-01 (superseded) | Covered by PRB-N1-01, 02, 07 and 08, except for P1-F |
| M-MIDI-ABS | PRB-N7-01 (primary), PRB-S4-05 (near-duplicate) | N7-01 refines S4-05 ([MIDI transforms](midi-transforms-native.md#probe-records)). S4-05 keeps its master-volume display readings, the only master, cue or crossfader readings in either record. It moves to session K |
| M-WARP-RENDER | PRB-S8-08 (primary), PRB-S8-11 (near-duplicate) | S8-11 reuses S8-08's WAV and markers (its own input). S8-08's Re-Pitch and Beats renders can serve as two of S8-11's six; S8-11 is deferred (flagged) |

Related but kept separate: PRB-N1-01, 06 and 08 with PRB-N2-03 (they share the read-error dialog);
PRB-N2-04 with 05; PRB-H1-03 with PRB-N4-05 (hung versus never-connected helper);
PRB-S4-06 with ESC-N3-01 (Play and Stop from MIDI versus the UI).
Among the later records: PRB-S6-01, PRB-S7-02 and PRB-S8-01 with PRB-N2-03 (one corrupt-document
throw, `0x101488e64` → `0x10148229c`); PRB-S6-04 with PRB-S9-08 (the Volume interpolation domain,
read on screen versus rendered); PRB-S6-08 with PRB-N1-04 and 05 (`Manual` versus envelope);
P4-N6-01 with P4-N5-01 (the same `_SetParameterA` method and position-range contradiction, on
Collision and Corpus); PRB-N8-03 with PRB-N4-09 (the MultiF0 log line under Rosetta versus arm64);
PRB-BI-01 with PRB-H2-09 (`.xyz` and `.wma` in both folders); PRB-BI-02 with PRB-H2-05 (location
presentation).

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
- PRB-S6-08 to 11. Proposed in the [automation spec](../specs/automation-envelopes.md#open-questions)
  and not in the S6 probe batch. Each names its input (B0 + E1) and what to read, but no
  expected result and no stop condition.
- PRB-BI-01 to 05. Proposed in the [browser index spec](../specs/browser-index.md#open-questions)
  and not filed in any probe-batch file. Each gives a minimal input and what to record. Apart
  from cases BI-001 and BI-003 (PRB-BI-01), the cases they cite carry no expected result, and
  only BI-01 ("once") and BI-03 ("after one start") bound the run. The spec needs PRB-BI-01
  for a first handoff.
- PRB-S8-11. It keeps six renders for a later comparison under metrics not yet declared
  ([Q-001](../questions.md#q-001-compatibility-targets)), so no outcome discriminates. Like the
  H4 signal section, it is comparison work.

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

**Later records whose citations disagree.** The S5–S9 records name research candidates
(CL-, AE-C, MN-, WM-, MX-) and the N7 records packet clause labels, not r1 requirement
numbers; the run sheet's Unblocks column follows the specs. These disagree:

| Record | The record | The spec or research page |
| --- | --- | --- |
| PRB-S5-09 | Includes a set with `GlobalQuantisation` 14 | [SPEC-CLIP-LAUNCH](../specs/clip-launch.md) REQ-011 and its open questions: no S5 probe covers an out-of-range `GlobalQuantisation` |
| PRB-S5-10 | Chances 30/30 and 0/0; preferences set to Gate and 1/4 | REQ-012 cites it for negative chances, REQ-010 for the preferences' factory values and creation paths |
| PRB-S6-04, 06 | Edit and read Volume (target 324) | [SPEC-AUTOMATION-ENVELOPES](../specs/automation-envelopes.md) cases AEN-016–018, 020 and 022 cite them with Pan fixtures (323); the spec asks for a Pan variant of S6-04 |
| PRB-S6-07 | A `FloatEvent` without `Time` or `Value`; duplicate Ids | REQ-004 also cites it for an `EnumEvent` without `Value`, and proposes adding an event without `Id` |
| PRB-S7-02 | Variant B expects NoteIds 1..n | [SPEC-MIDI-NOTE-STORAGE](../specs/midi-note-storage.md) appendix: 59 to 99 and `NextId` 100 for the 909 file |
| PRB-S7-07 | Seven variants | The spec asks for the four MNS-053 variants (REQ-014) |
| PRB-S7-09 | Draws a new clip | REQ-012 cites it for loaded Ids, repeated Ids and empty KeyTracks on load; assumption A2 for a loaded clip file placed in a set |
| PRB-S9-01 | Varies track volume only | [SPEC-MIXER-VALUES](../specs/mixer-values.md) REQ-012 cites it for the send gain |
| PRB-S9-04 | Expects `16R` for pan 0.33 and `-69.7 dB` for 0.0003273407 | The [2026-10-17 correction](mixer-values.md#candidate-requirements-for-spec-mixer-values): 0.33 shows `17R`, and −69.7 dB lies within `log10` rounding. REQ-006 and 011 put 0.0003273407 in the `-inf dB` range. REQ-002, 005 and 007 also cite it for the cue level, fader positions and the halfway pans 0.25 and 0.75, which it does not include |
| PRB-S9-08 | Volume automation midpoint level | SPEC-MIXER-VALUES assigns it to the automation spec, which does not cite it |
| PRB-N7-01 | A device encoder; REQ-MIDI-USER-005 clauses | [SPEC-MIDI-USER-MAPPING](../specs/midi-user-mapping.md) REQ-010 cites it for master, cue and crossfader ranges and absent targets; only PRB-S4-05 reads master volume (M-MIDI-ABS) |

**Input or tool gaps.**

- PRB-N2-04 needs an N2-019 copy without Creator, which is not among the 27 cases.
- PRB-S4-10 does not name its 3-bank device.
- PRB-H2-09 has no source for a `.wma` file.
- PRB-H2-07 needs a destination pack installed.
- ESC-N3-01, P4-H4-04 and PRB-N7-01 to 05 need a LOM harness. N7 asks for a read-only
  observer whose own latency is measured first.
- Session O needs a MIDI-clock-locked sender and a capture of the master output.
- PRB-N8-01 to 05 need Rosetta, and N8-01 a clean user account.
- PRB-S7-08 builds a probability group whose XML shape is unknown (REQ-MIDI-NOTE-STORAGE-015).
- The S9 test tone, the S8 click and known-length WAVs, the S5-08 tone and the N8-05 sines
  must be generated and hashed first.
- PRB-S6-02 and S7-05 may end the process: the static readings are an assertion abort and
  an unchecked key store. Each runs last in its session.
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
total 2,325 minutes (about 39 hours) before the deferred group. That is more than
one sitting; see [decisions needed](#decisions-needed-before-the-sitting).
Sessions 0 and A–D (460 minutes) settle the first batch's handoff blockers and document
probes, and the S7 and S9 saves. Sessions K–Q hold the later records. They run after
session I, and session J still runs last.

### Session 0 — Setup and identity pinning (45 min)

Create the account (or the backup) and the app copy, and pin the hashes. Check
every tool the later sessions rely on: `shasum`, `gzip`, `xxd`, `sqlite3`, `ps`,
`lsof`, `vmmap`, `tcpdump`, screen recording at 60 fps or more, the IAC bus, a
MIDI sender (clock-locked for session O) and monitor, a debugger, a capture of
Live's audio output, and Rosetta (session Q). Record any missing tool. Do not
install one without approval.

### Session A — Handoff blockers: saves, precedence, container failures (135 min)

Needs the app copy, [N2 cases](../../analysis/ableton-live-12.4.3/r2/n2-container-v1/cases.json),
`N2-001.als` as the N1 base, and the constructed N1 variants.

| # | Record | Do and observe | Min | Unblocks |
| --- | --- | --- | --- | --- |
| 1 | PRB-N1-07 | Edit the base to tempo 121.2, 7/8, loop 0.5 + 3.3 beats; save; decode number text, child order, KeyMidi, envelopes, SchemaChangeCount | 15 | H2 transport-state candidate: REQ-002, 008, 011 |
| 2 | PRB-N2-01 | New set, save; first 10 gzip bytes and first three XML lines | 10 | H3 container candidate: REQ-007, 008 |
| 3 | PRB-S9-07 | New set; insert one audio and one return track; save; decode mixer values, send holders, `EnabledByUser` | 10 | REQ-MIXER-VALUES-003, 010, 015; the 12.4.3 save question before a first release |
| 4 | PRB-S7-09 | Draw a clip: one muted note, 50 % probability, deviation +10, release velocity 100, one MPE note; save; attribute order, number text, KeyTrack Ids, NextId | 15 | REQ-MIDI-NOTE-STORAGE-012, assumption A2 |
| 5 | PRB-N1-04 | Three Manual/EnumEvent meter pairs; displayed meter and re-saved values | 15 | REQ-TRANSPORT-STATE-012 and the 007 meter default |
| 6 | PRB-N1-05 | Three tempo variants including an enabled scene tempo; displayed tempo | 15 | REQ-TRANSPORT-STATE-012 |
| 7 | PRB-N2-02 | Open plain-XML N2-002, save; magic `1f 8b` or `<?` | 10 | REQ-ALS-CONTAINER-001, 007 |
| 8 | PRB-N2-03 | Ten corrupt cases; dialog text, Log.txt, whether the previous set stays open | 30 | REQ-ALS-CONTAINER-009 |
| 9 | PRB-N2-04 | N2-013, N2-019, N2-019 without Creator; the version named | 15 | REQ-ALS-CONTAINER-004 |

### Session B — Transport timing, S3 escalation (40 min)

Needs screen recording; the LOM harness is needed for the lag measurement only.

| # | Record | Do and observe | Min | Unblocks |
| --- | --- | --- | --- | --- |
| 1 | ESC-N3-01 | Play, Stop, Stop from bar 5; Play+Stop within 50 ms; loop-is-song-start Play. Position display, saved `CurrentTime`, `is_playing` lag | 40 | T-03, T-05, T-08 and T-13 of the [transition table](transport-transitions-native.md#transition-table); no transitions spec yet |

### Session C — Corpus and Collision position range (100 min)

Needs a debuggable re-signed copy (a user decision) and the Collision preset copies. Skip to
session D if it is not approved.

| # | Record | Do and observe | Min | Unblocks |
| --- | --- | --- | --- | --- |
| 1 | P4-N5-01 | Log (index, value) at `_SetParameterA` for Amp, Electric, Corpus; ExcitationX 0/1 arrives as 0/1 or −1/1 | 60 | SPEC-CORPUS-DEVICE candidates and the [position range](corpus-dsp-static.md#host-parameters) contradiction |
| 2 | P4-N5-02 | `_CreateInstanceU` hits per inserted device | 20 | DEV-M08 |
| 3 | P4-N6-01 | Log (index, value) at Collision `_SetParameterA` (arm64 `0x12a1c`) for `Resonator1/HitX` 0 and 1, `VelToStartTranspose` 3, `Resonator2/Type` 6: (51, 0/1) or (51, −1/1); (32, 3) unclamped; (59, 6) arrives | 20 | REQ-BUNDLED-DEVICE-PARAMETERS-015 for Collision; the three Collision mismatches |

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

### Session F — MIDI remote-script profiles (180 min)

Needs the IAC bus, a MIDI sender and a monitor, and the probe profiles. Order
follows the records. Run S4-02 only after S4-01 shows listing works. PRB-S4-05 runs
in session K with PRB-N7-01 (M-MIDI-ABS).

| Records | Min | Unblocks |
| --- | --- | --- |
| PRB-S4-01, 02 (listing, names, restart) | 25 | REQ-MIDI-USER-001, unreleased in [midi-config-v2](../../handoff/midi-config-v2/README.md) |
| PRB-S4-03, 04 (raising profile, unknown mode) | 30 | Q-008 host outcomes excluded from midi-config-v2 |
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

### Session K — MIDI map-mode transforms (130 min)

Needs the session F MIDI setup, the read-only parameter observer, and the Takeover Mode
preference set explicitly before each record. Open the input before the first message
(N7 common prerequisites).

| Records in order | Min | Unblocks |
| --- | --- | --- |
| PRB-N7-01 with S4-05 (Absolute and Absolute14Bit, MT-01 to MT-05; master volume for CC 0, 64, 127) | 30 | REQ-MIDI-USER-005 value clauses; REQ-005d, 010d |
| PRB-N7-02 (eight relative modes, MT-06 to MT-14; stop at the first mismatch) | 40 | REQ-MIDI-USER-005 relative step table |
| PRB-N7-03 (Pick-Up and Value Scaling, MT-19 to MT-23; reopen the input between cases) | 25 | REQ-MIDI-USER-005 takeover; the preference default |
| PRB-N7-04 (quantized and on/off parameters, MT-15 to MT-18) | 15 | REQ-MIDI-USER-005 on/off clause |
| PRB-N7-05 (bursts of 100 messages, three per mapping) | 20 | [Q-009](../questions.md#q-009-midi-numerical-modes-timing-and-feedback) ordering and coalescing |

### Session L — Envelope and mixer-text documents (105 min)

Needs `Recording Audio.als` edited as each record states (S6 and S9 share it) and screen
captures. The LOM harness is optional for the S6 readings. PRB-S6-02 runs last.

| Records in order | Min | Unblocks |
| --- | --- | --- |
| PRB-S6-01 (first event at 4 or 0, empty list, control; refused or open) | 15 | REQ-AUTOMATION-ENVELOPES-007 presentation |
| PRB-S6-03, 05, 07 (unsorted events; non-monotone curve controls; missing `Time` or `Value`, duplicate Ids) | 30 | REQ-AUTOMATION-ENVELOPES-004, 006, 009 |
| PRB-S6-04, 06 (Volume at fixed beats, linear and curved; values at a step and at Bool event times) | 30 | REQ-AUTOMATION-ENVELOPES-010, 011; assumption A1 |
| PRB-S9-04 (volume, send and pan text; one screenshot per variant) | 20 | REQ-MIXER-VALUES-006, 007 |
| PRB-S6-02 (dangling `PointeeId`; one open, re-save if it opens) | 10 | [Q-020](../questions.md#q-020-automation-envelope-load-robustness) |

### Session M — MIDI note documents (130 min)

Needs the edited copies of `909 Core Kit House 127 bpm.alc`, and the Intro demo set for
S7-07. Drag each clip into an empty MIDI track and save the set as new (S7 common
prerequisites). PRB-S7-05 runs last, in a disposable session.

| Records in order | Min | Unblocks |
| --- | --- | --- |
| PRB-S7-01, 02 (absent attributes; absent or duplicate NoteId) | 30 | REQ-MIDI-NOTE-STORAGE-017; the excluded inheritance reading |
| PRB-S7-03, 04 (clamps on load; grid rounding text) | 10 | REQ-MIDI-NOTE-STORAGE-005 (assumption A1), 006 |
| PRB-S7-06, 10 (unsorted notes and overlaps; NextId variants) | 25 | REQ-MIDI-NOTE-STORAGE-009, 010 |
| PRB-S7-07, 08 (per-note expression lists; probability-group ids) | 45 | REQ-MIDI-NOTE-STORAGE-014, 015 |
| PRB-S7-05 (MidiKey 128, −1, absent, repeated; stop at the first crash) | 20 | REQ-MIDI-NOTE-STORAGE-011, excluded ([Q-018](../questions.md#q-018-midi-note-key-range-and-ordering-after-load)) |

### Session N — Warp documents (95 min)

Needs the edited copies of the Patience Suite demo (clip Vocal Main), the recorded Default
Warp Mode preference, and a known-length WAV for S8-09 (S8 common prerequisites).

| Records in order | Min | Unblocks |
| --- | --- | --- |
| PRB-S8-01, 02 (empty and one-marker lists) | 10 | REQ-WARP-MARKERS-004 presentation (assumption A1), 005 |
| PRB-S8-03, 04 (unordered, inverted and equal-time markers; missing or `Invalid` `BeatTime`) | 25 | REQ-WARP-MARKERS-005, 006 |
| PRB-S8-05, 06 (`WarpMode` 5, 7, −1; out-of-range settings) | 30 | REQ-WARP-MARKERS-013, 014 |
| PRB-S8-07 (1/16-beat shadow spacing; re-save, nudge, re-save) | 10 | REQ-WARP-MARKERS-007 |
| PRB-S8-09, 10 (unwarped region units; absent settings under two Default Warp Mode values) | 20 | Region-field exclusion; REQ-WARP-MARKERS-010 |

### Session O — Clip launch timing and clip settings (180 min)

Needs the S5 base set and `Chord C Minor9 Staggered.alc`, a MIDI-clock-locked sender with the
clip launch mapped to a note, and a capture of the master output (S5 capture rule). Stop
S5-01 if the capture jitter exceeds 1/64 beat, the spec's tolerance.

| Records in order | Min | Unblocks |
| --- | --- | --- |
| PRB-S5-01 (presses at beats 1.5, 3.9, 3.99 and 4.0, twice each) | 30 | REQ-CLIP-LAUNCH-017 near-boundary clause, which must not be released before it |
| PRB-S5-02, 03 (meter change at beat 8; 6/8 clip at 1 Bar) | 20 | REQ-CLIP-LAUNCH-016, 017 |
| PRB-S5-04, 05 (no-grid latency; launch with the transport stopped) | 25 | REQ-CLIP-LAUNCH-018, 019 |
| PRB-S5-06, 07, 11 (Gate, Toggle and Repeat; Legato; linked and unlinked follow actions) | 45 | REQ-CLIP-LAUNCH-020, 021, 023 |
| PRB-S5-08 (velocity amount 0, 0.5, 1 at velocities 127, 64, 1; RMS) | 20 | REQ-CLIP-LAUNCH-022 |
| PRB-S5-09, 10 (out-of-range enums; chance rescaling and missing launch elements under Gate and 1/4) | 40 | REQ-CLIP-LAUNCH-010, 011, 012 |

### Session P — Rendered audio: mixer laws and warp playback (145 min)

Needs the generated 1 kHz test tone and click WAV, hashed before the sitting; 48 kHz, 24-bit
export with dither and normalization off; Main and Cue at 0 dB (S9 common prerequisite).

| Records in order | Min | Unblocks |
| --- | --- | --- |
| PRB-S9-01 (stored minimum, −69.8 dB, −60 dB and 1; peak and RMS) | 20 | REQ-MIXER-VALUES-011 and its condition ([Q-019](../questions.md#q-019-mixer-volume-and-send-values-sent-to-the-engine)) |
| PRB-S9-02, 03 (Stereo and Split Stereo pan laws) | 35 | REQ-MIXER-VALUES-013 |
| PRB-S9-06 (crossfade curves 2 and 0 at −1, 0, 1) | 25 | REQ-MIXER-VALUES-014 |
| PRB-S9-05 (seven out-of-range values: open, display, level, Save As) | 35 | REQ-MIXER-VALUES-015 |
| PRB-S9-08 (Volume envelope midpoint level) | 10 | Assumption A1 of SPEC-AUTOMATION-ENVELOPES |
| PRB-S8-08 (click renders in Re-Pitch, then Beats; second variant with the first marker moved) | 20 | REQ-WARP-MARKERS-009 ([Q-021](../questions.md#q-021-warp-playback-mapping-and-load-handling)) |

### Session Q — Live x86_64 under Rosetta (80 min)

Needs Rosetta and, for N8-01, a clean user account. None of these records is a gate.

| Records in order | Min | Unblocks |
| --- | --- | --- |
| PRB-N8-01, 02 (new Set and quit; ReWire folders and Log.txt; ReWire entries in Preferences, choosers and Help) | 25 | [Q-013](../questions.md#q-013-x86_64-only-rewire-and-multif0-paths) ReWire |
| PRB-N8-03, 04 (Convert Harmony under Rosetta; Convert Drums on both architectures) | 35 | Q-013 MultiF0 |
| PRB-N8-05 (Convert Melody on 440 Hz and 880 Hz sines) | 20 | Meaning of the result fields |

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
- PRB-S8-11 waits for declared comparison metrics (Q-001); it reuses S8-08's WAV and markers.
- PRB-S6-08 to 11 and PRB-BI-01 to 05 are incomplete proposals. Once completed, S6-08 to 11
  fit session L and BI-01 to 05 session G.

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
      Creator, the H4, N5 and N6 preset copies, and the S5–S9 document edits. Build
      them in a separate, approved step; this packet builds no documents from shipped
      content.
- [ ] Write the S4 profiles (about 25 folders), generate the WAV files (with the S5,
      S8, S9 and N8 tones and clicks) and the bad-media set, and pick the 3-bank
      device for PRB-S4-10.
- [ ] Complete PRB-S6-08 to 11 and PRB-BI-01 to 05 at their sources, and settle the
      later citation disagreements above.
- [ ] Verify the N2 cases against `cases.json`.
- [ ] Build and sign the test VST3s and the stub helpers, if approved.
- [ ] Try the cheap static traces first: `_Generic/Devices` (S4-09) and
      `_Framework/MixerComponent` (S4-11).
- [ ] Prepare the disk images, and the hardware if it is available.
- [ ] Settle the evidence copy route to the Linux host.
- [ ] Print this sheet and the `result.json` field list.

## Decisions needed before the sitting

- **Length.** Run everything over four or five days, or only sessions 0 and A–D
  (about 8 hours) first.
- **Isolation.** Use a separate macOS account or a backup of the preferences.
  How Live is authorized in a new account without signing in is not known.
- **Debugging (session C).** Re-sign a copy, change SIP, or skip P4-N5-01, 02 and P4-N6-01.
- **LOM harness** for ESC-N3-01, P4-H4-04 and the N7 observer: a Max for Live device or a
  control-surface script.
- **Rosetta (session Q)**, and a clean account for PRB-N8-01.
- **Test plug-ins (session H).** Needs a build toolchain and the public VST3 SDK,
  which needs network on a build machine. Installing into `/Library` needs admin.
- **Modified copies (session J)** and the stub helpers.
- **Hardware.** Push 3 and Push 2, a 32 kHz audio device, and a USB capture tool.
- **Network.** A local link for P5-07; P4B-H6-01 stays out unless approved.
- **Tool installation on the macOS host**, such as a MIDI sender.

## Limitations

Time estimates are planning guesses. Static predictions in the records are
derivations, not observations. Tool availability on the macOS host is unverified.
The first 79 records' sources were read at the hashes in `manifest.json`, the later 67
at those in `sources-2026-10-18.json`. Pages edited later may add records that this
batch does not include.
