---
id: RESEARCH-PHASE4-PROBE-BATCH
type: research
status: draft
updated: 2026-10-23
access: analysis
target: Ableton Live 12 Suite 12.4.3 / retained macOS run sheet and separate Windows VM profile
---

# Phase 4 reference observation batch

> **Reinstated 2026-10-21** by [ADR 0006](../decisions/adr-0006-reference-observation-reopened.md)
> as the first observation packet's record set, at the retained hashes, pending
> the host decision D-07 in [plan revision 5](full-live-specification-plan.md#revision-5--reference-observation-route-2026-10-21).
> The note below is history.
>
> **Will not run as planned (2026-10-18).** No macOS host will be available
> ([ADR 0003](../decisions/adr-0003-no-reference-execution.md)). This page is kept as the record of what
> reference observation would have settled. Each record's question is now an
> extracted-execution target (original x86_64 functions run on this host), a
> static investigation target, or a permanent unknown. See
> [extracted execution](extracted-execution.md) for the method and the first
> triage.

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

## Windows guest adaptation and first sitting — 2026-10-22

[D-07 now selects a local Windows VM](../decisions/adr-0006-reference-observation-reopened.md#windows-guest-profile-selected--2026-10-22). The retained macOS run sheet, batch JSON, source pins and original questions above stay unchanged. This amendment prepares a distinct Windows/VM sitting; it does not claim that macOS-only records became runnable or that the guest is ready. Root chose Windows11Pro x64 after user delegation and the local authorized-installer path `~/Downloads/Live-12.4.3-Windows-Suite.zip`. Edition/license/activation status, exact guest build and actual installer/executable hashes still require recording. The user will reboot for KVM later; no reboot or silent TCG fallback is selected during active analysis.

The first Windows sitting is **Session0 setup, then all nine SessionA records in their retained order**, subject to their individual prerequisites. This uses the existing plan's first-sitting order and generic save/load/display questions. Unready records are explicitly not-observed/U with a reason; they are not dropped, replaced by invented expectations or counted as successful. Other macOS/hardware/plugin/debug/modified-copy sessions remain separate pending applicability decisions. No complete146-record Windows applicability claim is made.

| Record | Windows sitting input/observation boundary | Readiness |
| --- | --- | --- |
| PRB-N1-07 | Retain specified tempo121.2, meter7/8 and loop0.5+3.3 input/edit/save procedure; export exact saved ALS, screenshot and decoded numeric text/order | Original base and actual Windows UI/save acceptance unverified; no macOS result transfer |
| PRB-N2-01 | Create a fresh set and save; record actual gzip header/XML envelope/build text | Requires authorized exact Live12.4.3Windows guest |
| PRB-S9-07 | New set plus one audio and return track; record saved mixer/send/EnabledByUser fields | Do not infer a mixer law from file text |
| PRB-S7-09 | Draw the specified muted/probability/deviation/release/MPE note cases and save | Record unsupported UI/action or absent MPE control as not-observed rather than substituting inputs |
| PRB-N1-04 | Preserve three Manual/EnumEvent meter pairs and display/resave comparisons | Exact literal variants must be retained and hashed before opening |
| PRB-N1-05 | Preserve three tempo variants including scene-tempo enablement | No source/filename/value normalization that changes the discriminating inputs |
| PRB-N2-02 | Open original plain-XML N2-002 and save; record resulting envelope bytes | Opening/saving occurs only in disposable guest data; retained input immutable |
| PRB-N2-03 | All ten corrupt-document cases; dialog/log and prior-set survival, in original order | Each case has its own stop/result; no malformed-input omission or destructive host access |
| PRB-N2-04 | Preserve N2-013/N2-019 and Creator-omitted variant; record named version | Variant creation is a new analyst fixture with provenance, not a rewrite of retained sources |

**Windows setup substitutions are recorded procedure changes, not behavior equivalence.** Hash the actual Windows installer/executable and build; a macOS universal hash cannot verify the Windows executable. Use a guest-only account/VM disk and snapshot, not `ditto` or a host-home backup. Use Windows-supported capture/file/process/hash tools and record versions instead of pretending `vmmap`, Rosetta, IAC, CoreAudio or macOS paths exist. Capture actual Windows Log.txt path and preserve screenshots/recordings, ALS outputs and logs. No guest share may write this checkout, retained source or the host home. Stage inputs read-only and export evidence to a dedicated new analyst directory, with whole-sitting/per-record manifests and verified source/destination hashes; a copy is not proof of continuous custody.

The old no-sign-in step was a macOS isolation assumption whose authorization route was unknown. D-07 expressly allows use of the user's authorized Windows installer; establish activation only through the user's own legitimate method, without collecting credentials or touching host account data. Record authorization/network setup separately, then disconnect guest networking for the sitting and decline updates/firmware changes. No guest build/update is silently substituted after identity capture. Windows guest save/load observations remain Windows/VM/build-specific. Native macOS/CoreAudio/AudioUnit/arm64/FP/timing predicates remain U unless separate evidence supports them.

Each record carries the unchanged question, existing evidence/reason, exact input hashes, actual procedure, discriminating observation, stopping condition, host/guest/Live identity, raw hashes, outcome and deviation or explicit not-observed reason. Any hypothesis/expected value is labeled separately from observation; Grade/portable comparator stays NULL unless its owning criterion has separately been established. One sole independent actual/sitting review covers the frozen packet under design12/14. Approval admits only the bounded observed values to the relevant owner's next revision; no second actual review, candidate comparison or whole-product closure is created by this setup sheet.

### Selected SessionA document preparation — 2026-10-22

Prepare one analyst-only frozen INPUT packet for the first Windows sitting: original N2-001 base; all six exact PRB-N1-04/05 meter/tempo variants from their original literal recipes; the thirteen existing N2 cases used by SessionA (plain XML, ten corrupt cases and two newer-version cases); and the N2-019 Creator-omitted variant. Pin the two original probe records, case index and every retained input. Preserve decompressed source bytes outside the declared attribute edits, use deterministic new gzip envelopes for the six N1 variants and preserve the existing plain-XML envelope for the Creator-omitted variant, record exact substitutions and full reversal, and independently compare parsed XML trees/allowed attribute changes. Existing corrupt case bytes stay byte-identical and are not reparsed or normalized. This selects fixture construction only, under D07 local-guest preparation, with no Live/xdev/helper execution, input acceptance, expected-output/grade transfer or new behavior law. Preserve original files and manifests; do not run the historical batch builder. Newly created-in-Live sets/notes remain deferred to the actual sitting. Other missing N1/S5–S9 fixtures remain outside this nine-record SessionA preparation scope.

### Windows first-sitting INPUT packet prepared — 2026-10-22

The [frozen INPUT manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/phase4-windows-session-a-inputs-v2/manifest.json),4854bytes/SHA256 `35a3dd50d40aeb62dd2e74bd51e11e47489bb4bb6e0808e5088ce9e27bb607ac`, retains21inputs:14byte-identical source copies and seven attribute-only variants. The [catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/phase4-windows-session-a-inputs-v2/input-catalog.json) pins original N1/N2 probe records, case index and each input; all six original PRB-N1-04/05 recipes match exactly. Named XML attribute edits have independent parsed-tree comparisons and full reversal; other decompressed bytes stay exact, gzip mtime0 is a new transport envelope for N1 only. The Creator-omitted variant preserves N2-019's original plain XML and removes only that root attribute. Original corrupt-case bytes remain exact copies, without normalization. Five controls reject missing/multiple targets, wrong original value/target and structural edits. No Live/loader/helper/model execution, input acceptance, observed value, criterion or grade occurred.

The first authoring attempt assumed N2-019 was gzip, stopped after20prepared inputs and is retained immutable with AUTHORING_FAIL metadata at [v1](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/phase4-windows-session-a-inputs-v1/manifest.json). Diagnosis confirmed the220byte original starts with plain XML. V2 preserves that envelope and retains its authoring history; no original source/manifest changed or original application was retried. Generated-in-Live sets/notes, exact Windows guest/build/activation, native UI acceptance, capture and evidence export remain pending. Input preparation is not a readiness review gate or behavior proof.

### Prepared isolated Windows input and export route — 2026-10-22

The [new private VM/transfer preparation](full-live-specification-plan.md#prepared-transfer-media-and-current-stop-points--2026-10-22) stages the21SessionA documents in a read-only64MiB FAT input image, plus a separate empty256MiB evidence-export image. All24transferred files (21ALS plus catalog/manifest/README) roundtrip exactly in owned-image tests. The input image is a declared subset, not a complete mirror of the28payload source packet. The offline export plan uses a new private directory and exact allowlisted filenames under SESSIONA with size/count bounds, not recursive/wildcard copying into the checkout. Guest USB/drive letters/input hashes and guest-write/export bytes still need actual checks. Those preparation controls establish no Live acceptance, observed value, grade or usable guest. MicrosoftISO download is blocked byHTTP403 here; the user will supply media and reboot for KVM later. The first sitting remains Session0 then SessionA in retained order when ready.

## Remaining137 Windows triage preparation selected — 2026-10-23

**User-selected preparation only; no guest boot, install, download or observation sitting.** Route O waits on the user’s deferred KVM reboot, Windows ISO and authorized Live installer. Prepare one packet covering every remaining Phase 4 record outside Session 0+A: all 137 remaining records, including the original deferred Session X and unassigned proposals alongside sessions B–Q. Auto authors it after the Analog R15 owner packet seals; Root provides the sole review of the new triage, inputs and code. Inherit the earlier 21 Session A inputs by their frozen preparation manifest. A separate sole-review report locator is not established; its existence remains unknown and is not a new preparation gate. Preserve the original 146-record macOS run sheet, its 79+67 source distinction and every procedure, discriminator and stop condition.

For each record retain its ID, session, source locator, affected requirements and prerequisites. Assign a Windows-profile disposition of **applicable**, **needs macOS** or **needs hardware or plugin**, with a reason and any additional unresolved dependencies. These categories are planning judgments; they do not establish guest availability or successful observation. Preserve mixed dependencies and record Windows procedure substitutions separately. Missing fixtures, tools, builds and permissions remain explicit unknowns. Use a complete record mapping rather than a session-level approximation; invent no expected output or criterion.

The same packet supplies the Session 0 Windows tool and version-record checklist: installer, executable and artifact hashing; screen capture at 60 fps or above; audio capture; MIDI loopback; process inspection; file inspection; and the exact Windows Live Log.txt location. Name the tools, required capabilities and official source versions where available. The future sitting must record actual tool, OS, driver and plugin versions, executable hashes, capture settings and the actual log path. Do not describe proposed tools as installed or ready. Distinguish Windows substitutes from vmmap, IAC, CoreAudio, Rosetta and macOS paths.

Retain D-07’s account, snapshot, isolation, authorization, offline-sitting and export-hash requirements. Do not create a writable guest share into the host home or checkout, request credentials, change providers or claim platform equivalence. Use the existing analyst store, prebind and inertly read new authoring and checker code, and check completeness, duplicate IDs, missing records and classification boundaries. Freeze one packet for one independent review. Do not run the historical batch builder, original helper, application or plugin.

This preparation adds no observation, case, grade, release or whole-Live completion credit. After the selected X classes drain, S work proceeds in ledger order while this preparation runs independently.

## Remaining137 Windows preparation adopted — 2026-10-23

[Root’s sole preparation review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/phase4-windows-remaining137-preparation-v1-review.json),1,399,851 bytes / SHA256 `453220c2b66dbcd3bfde274d394b35c4386110051418cc577904034f69d2b28a`, approves the complete 137-record view with two resolved disposition corrections. Its `approved_qualified_triage` is the complete reviewed catalog; original records, presets, procedures, discriminators, stop conditions, requirements context and source-version qualifications remain attached to every row. This is one preparation packet and one sole review, with no observation or guest-readiness approval.

| Windows-profile planning disposition | Records | Meaning |
| --- | --- | --- |
| Applicable, subject to prerequisites | 107 | A distinct Windows question can be prepared; missing fixtures, tools, API bindings, criteria and permissions remain unknown. |
| Needs hardware or plugin | 15 | Physical devices or exact test modules are required; availability, builds and passthrough remain unknown. |
| Needs macOS | 15 | The whole original predicate requires its macOS context; simultaneous hardware/plugin dependencies remain explicit. |

The 137 are the original 146 minus the nine current Session A records; Session 0 is setup. Fifteen deferred Session X records and unassigned/incomplete proposals remain inside the catalog with their original labels. Intended L/G associations do not invent executable recipes. Seven of 22 historical version-register entries match selected current parents, three differ and twelve are unselected/unknown; changed pages do not repair original-version or execution evidence. All 137 retained record objects/common fields and Markdown row/bullet locators were independently checked against the 15 exact pinned declaration/governance parents. No original builder, fixture or earlier Session A payload/proof was acquired or executed.

The [original manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/phase4-windows-remaining137-preparation-v1/manifest.json),3,669 bytes / SHA256 `bb3596f77f1adf49bd14f26ad80d654259209600752077672f95b4d3213632d1`, seals 24 payloads / 1,413,473 bytes, all 25 files0444 under private0700. Original catalog836152bytes/SHA256 `12d3bbd07188f0d59e458a32bf319aaea4c338ef224368f2745c1585235f946a` and its original107/17/13 author counts remain unchanged. [The additive two-row correction](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/phase4-windows-remaining137-two-disposition-qualification-v1.json),9,175 bytes / SHA256 `0c8be6ae3cdf9a9133afc9c4b3846ea22f189a951647bee2636ac9c9d0111e6c`, is POST-target/seal, not prebound. P5-08’s CoreMIDI-versus-Push-channel predicate and PRB-N4-08’s original Unix-socket listener predicate require macOS as well as Push hardware. Only four fields per row change; full reversal restores both original rows and all other135rows remain exact. This claims no universal absence of Windows Unix sockets or MIDI. A Windows-only restart or MIDI-path question would need its own explicit adaptation.

Four new methods155lines and the original failed synthetic fixture draft were read before the only safe checker. Seventeen owned and twelve independent controls passed; output was byte-exact and all25sealed files stayed unchanged. The initial BI-field fixture failure was corrected before the one materialization; original draft, empty stdout and traceback remain. Worker-loss continuation only finalized retained metadata. The checker validates the original author view; the sole review separately validates the two-row correction and complete qualified view. No target regeneration or guest/reference/helper execution occurred.

The [Session0 tool checklist](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/phase4-windows-remaining137-preparation-v1/session0-tools.json) is retained in the approved view. All actual guest/tool versions and capabilities remain NULL:

| Capability | Proposed Windows tool or route | Record at the future sitting |
| --- | --- | --- |
| Hashing | [PowerShell Get-FileHash](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash?view=powershell-7.5), SHA256 | Actual PowerShell/executable version and hash; media, Live, input and exported-evidence hashes. |
| Screen capture | [OBS Studio](https://obsproject.com/kb/OBS-Studio-Overview), at least60fps | Version/hash, configured FPS, effective timestamps, dropped/duplicated frames, resolution and VM load. A60fps setting is not timing proof. |
| Audio capture | Original Live export/resampling, or [Audacity WASAPI loopback](https://manual.audacityteam.org/man/tutorial_recording_computer_playback_on_windows.html) after route validation | Tool/driver/device/API versions, channels, sample rate, bit depth, buffer/routing and original WAV criteria. WASAPI may pause during silence and does not establish ASIO capture. |
| MIDI loopback | [Ableton-listed loopMIDI candidate](https://help.ableton.com/hc/en-us/articles/209774225-Setting-up-a-virtual-MIDI-bus) | Actual driver/sender/monitor versions and hashes, exact ports/bytes/Remote settings, clock/latency/jitter characterization where required. |
| Process inspection | [Win32_Process/CIM](https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-process), [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon), [Process Explorer](https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer) | Actual versions/hashes, privileges, image/argv/PID/parent/timestamps, short-lived capture completeness, handles/DLL/file/Registry scope. |
| File inspection | PowerShell/Explorer and read-only byte/XML/gzip inspection; sqlite3 on copies if available | Actual tool versions/hashes, paths, raw envelope/text order and copy hashes. Do not normalize corrupt fixtures. |
| Live log | [Ableton’s documented Windows pattern](https://help.ableton.com/hc/en-us/articles/5301568366354-Reading-Ableton-Live-Crash-Reports) | Resolve and record `%APPDATA%\Ableton\Live 12.4.3\Preferences\Log.txt` for the actual account/version; its existence is unverified. |

Official documentation supports proposed capabilities, not installed versions or guest performance. Retain D-07 isolation, clean snapshot, legitimate authorization, offline sitting and read-only input/allowlisted export requirements. Session A’s21prepared inputs remain a manifest citation; a separate independent review remains UNKNOWN. No boot, installation, software/media download, reference call, O observation, case, grade, release or whole-product completion credit follows. Whole-Live coverage remains OPEN.


## D-07 setup update; no sitting yet — 2026-10-23

[Host KVM readiness](../decisions/adr-0006-reference-observation-reopened.md#kvm-readiness-verified-media-present-but-unverified--2026-10-23) now passes the device API and one paused diskless initialization. Both selected media paths are present but unverified; guest OS/build/license/authorization/capture/copy prerequisites remain open. The latest user requires both media before future OS boot. No guest OS boot or Live observation occurred in this task; independent production guest state is unknown. The frozen137-record preparation and actual tool-version NULLs are unchanged; reviewed O remains0.


## Windows ISO documentary identity update — 2026-10-23

[Current D-07](../decisions/adr-0006-reference-observation-reopened.md#windows-iso-provenance-update--2026-10-23) now retains the supplied26H2ISO page/hash association and servedfilename26300.9457 label; this is media evidence, not an observed guest build or application behavior. User Windowslicence/authorized exact12.4.3Live installer remain needed, existing localZIP unidentified;25H2partial excluded. Session0actualguest/toolversion/capture/copy fields remain unobserved, the frozen137-record triage unchanged/reviewedO0.


## Unactivated Windows Session0 conditions — 2026-10-23

[D-07](../decisions/adr-0006-reference-observation-reopened.md#unactivated-windows-profile-adopted--2026-10-23) now selects Windows11Pro installed withoutproductkey/notactivated; no activation/key wait. This is a declared configuration, not an observed installedguest. AtSession0 record actual edition/build/activation state, watermark visibility/location in raw screen recordings and any relevant lockedpersonalization. Identify the watermark as an OS overlay, not Live output. Only authorized exactLive12.4.3 installer remains user-supplied; capture/tool/copy/guest capability measurements still await the actual sitting. Frozen137triage/tool proposals unchanged; observedO0.


## Observed Windows and Live identity; authorization setup pending — 2026-10-23

[Current D-07](../decisions/adr-0006-reference-observation-reopened.md#live-media-supplied-windows-and-installed-live-identities-observed--2026-10-23) records alluserbootmedia MET and the existingguestWindows11Pro26H2/build26300.9457, installedmainLiveProductVersion/FileVersion12.4.3/hash andguestAuthenticodeValid. This is setup identity, not a SessionA/Ocompatibilityresult or macOS/ARM equivalence. ActivationCIMtimeoutstaysunknown/notablocker. [Offline profile/copy-route setup](../decisions/adr-0006-reference-observation-reopened.md#offline-profile-copy-route-and-hardware-code-observed--2026-10-23) is observed: E:readonlyinput/G:writableexport, guest EthernetDown, exact32-byte guest-to-host probe via normal eject/backend closure/same-image reattachment. Actual hardwarecode sent; userAUZ file/path pending, no credentials/import/authorization claim. Capture>=60fps/CPU/audio/MIDI/tool fields still requireactualSession0records. The137triage/21preparedinputs remain asdeclared, priorseparateINPUTindependentreviewUNKNOWN unchanged.


[Latest D-07 coordination](../decisions/adr-0006-reference-observation-reopened.md#guest-operations-assigned-to-claude-concurrent-interaction-held--2026-10-23) assigns Claude guestboot/OSLiveinstallation; Root/workers hold QEMUlaunch, guest-v1 modification and all guest/QMP/UI/media/profile/AUZ interaction until its completion report. Earlier raw guest/software/copy/hardwarecode findings remain ASOF; no unchanged final profile or matching code is inferred. Readonly inventory commands were never launched; frozen focus-only partial adds no tool/capture capability. Static work continues; reviewedO0 and wholeLiveOPEN unchanged.

## Session0 capability methods; primary-source followup adopted — 2026-10-23

The [sole Root SOURCE/documentary review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session0-source-methods-2026-10-23-v1-root-review.json),2918bytes/SHA256 `802d83c6020f4a9279809b7958475dc84de51dde684935df8aff109fd8584cf6`, approves six qualified method additions to the existing checklist, not a second tool catalog or an executed readiness result. [Frozen source manifest](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-source-methods-2026-10-23-v1/manifest.json),6441bytes/SHA256 `415ee6f31d08805f92f3ac238519d50552badd87f55adeb24ec2d977352461bb`, seals42payloads1465648bytes/all43files0444/private0700. Root read the new collector and complete method proposal, catalog/version/locator fields and supporting retained source passages, then checked all42payload pins and six method/source joins. No collector/helper/guest action was repeated.

The [source catalog](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-source-methods-2026-10-23-v1/source-catalog.json),20350bytes/SHA256 `6639855301aa187f16d00e02f296d69c13e513da1e2dbbce99d9883d6c62b73a`, identifies17primary official documents captured2026-10-23:14direct HTML/text sources at11:27:31–11:27:44UTC and three exact Ableton web-tool renderings at11:29:33UTC after preserved once-only direct403s. The alternate responses are not raw origin HTML. Source versions below are documentation versions, never installed guest-tool versions. Full draft/method rows remain in the frozen packet as unexecuted proposals.

| Method | Source-supported limit and selected documentary followup |
| --- | --- |
| Final profile | After Claude's completion report, reconcile actual OS/Live/configuration/media and matching hardware code. Coordinate CPU exposure, display/GPU and any audio controller/codec/backend before final AUZ pairing. QEMU master lists Intel HDA as a candidate, not tested8.2.2syntax/Windows driver support (`VM_AUDIO`, text34/52–53). Ableton's hardware-code article explains the displayed code/offline file (`LIVE_HARDWARE_CODE`, rendered13–32), but these sources establish no fingerprint effect of an arbitrary USB change. No guest change is selected here. |
| Actual identities | Later inventory measures actual PowerShell version/edition/PSHOME and executing EXE/Explorer hashes, explicit proposed tool paths and the actual account/version Log.txt existence/length. Missing one candidate path is not global absence or a capability result. Retain normal setup/OS/console writes; tool launch/EULA/driver state is not a write-free guest. `HASH` uses the PowerShell5.1 documentation view, text40/50; `LIVE_LOG`, rendered28, supplies the Windows path pattern. Neither establishes installed runtime or file existence. |
| CPU/OS | Future official Coreinfo feature output can record literal AVX2/XSAVE/OSXSAVE fields; documentation header4.02/published2026-08-12 and embedded4.0example are not guest versions (`CPU_COREINFO`, text29/34/332/355). Managed Avx2.IsSupported applies only if the measured runtime contains that API; the retained page is a.NET9view (`CPU_DOTNET`, text41/54–69). Windows defines separate AVX2/XSAVE flags (`CPU_WINDOWS_API`, text128–149). No native invocation, compile/PInvoke/helper, raw XCR0/YMM measurement or OS-support result is supplied. Unsupported fields remainU. |
| Audio route | For records needing real-time audio, establish the actual endpoint/driver/API/channels/rate/buffer, then nominate a pinned owned tone–silence–tone PCM calibration with known sample positions/duration. Audacity's matching WASAPI loopback route can pause without active audio (`AUDIO_AUDACITY`, text60–75; manual footer2026-09-02). Windows loopback is shared-mode (`AUDIO_WASAPI`, text58). Preserve raw WAV/route/settings and test silence length; contraction limits that capture route, not Live's silence behavior. No ASIO/CoreAudio, numerical-WAV or latency equivalence follows. |
| Screen cadence | OBS's compatible DirectX10.1GPU requirement and FPS settings do not prove recording performance (`OBS_REQUIREMENTS`, text22/25; `OBS_SETTINGS`, text75–76). Nominate one bounded60-second calibration at intended resolution and>=60fps, preserving settings, raw recording/log and render/encode counters. Future official ffprobe frame/stream inspection on an immutable copy records actual version/hash, rational timebase, presentation timestamps, interval distribution and count (`FRAME_TIMESTAMP_NOMINATION`, text662/769/851). Predeclare tolerances and independently admit a changing-marker source: identical static pictures, nominal FPS and network-drop counters cannot identify capture loss/duplication. `OBS_NETWORK_DROP`, text30–34, concerns streaming transport. No ffprobe executable is acquired or selected to run by this source study. |
| MIDI route | loopMIDI remains the existing candidate. Its vendor page states Windows7–10, per-user ports and running-process lifetime (`MIDI_VENDOR`, text15/18–22); Ableton lists it as a Windows option (`MIDI_ABLETON`, rendered41–45). This is no Windows11usability proof or global unsupported verdict. Later record actual app/driver/account/ports and use a pinned note/CC/sync sequence with separately identified sender/receiver and timestamp reference. Port presence/Live's indicator establishes neither exact bytes nor jitter; sender/monitor/timing methods remain unselected/U. |

These are **source-supported future methods**, not a validated runnable guide, universal inventory-completeness gate or new user-approval requirement. Only per-record prerequisites and unchanged criteria govern applicability. Coreinfo, ffprobe, owned audio calibration, changing-marker and MIDI sender/timestamp methods are nominations; no executable download/install/launch, native helper, guest/QMP/UI/media/profile change, capture or authorization occurred. Client bounds and the observed source-collection span are not a global network/parent-watchdog guarantee. All actual guest capability fields remainNULL/U; D-07's ownership hold and final-profile correspondence remain open. No O observation, behavioral case/grade, macOS/arm64 proof, release or whole-product closure follows.


## Owned audio and MIDI calibration inputs selected — 2026-10-23

Select one new private **session0-audio-midi-owned-inputs-2026-10-23-v1** INPUT packet under the existing VM evidence store, using stdlib only. Two self-authored PCM16LE stereo WAVs are exactly3seconds at44100/48000Hz (132300/144000frames), amplitude±2048. First second: left-only squarewave/rightzero; second: bothzero; third: right-only squarewave/leftzero. Integer periods42/48samples respectively, equal positive/negative halves, positive first. These are arbitrary owned calibration definitions, not missing original files, device inputs, original waveform equivalence or compatibility oracles.

One self-authored raw MIDI-vector JSON declares seven records at0–600ms in100ms steps, literal payloads `90 3c 40`, `b0 01 60`, `f8`, `b0 01 00`, `f8`, `80 3c 00`, `f8` (15bytes total). Desired input offsets establish no observed delivery, tempo, clock, byte-fidelity or jitter law. No SMF/player/sender/driver or MIDI I/O is selected.

Tension_owner_finish authors; Root solely reviews the frozen NEW INPUT/code packet. Fully read/pin new generator and independent RIFF/PCM/vector validation methods before one construction; meaningful malformed owned-toy controls and exact header/geometry/segment/channel/value checks, not self-validation through the writer. Preserve partials/no retry/oldfixture replay, fullunchanged6039814144phase floor including S/concurrent allowances plus complete own outputs/headroom or larger, private0700/0444sealing. No guest/QMP/UI/QEMU/guest-v1/media/profile/authorization, originalLive/DSP/harness/provider, playback/sending/capture, executable acquisition/install/tool launch or native helper. Changing-marker/video remains only a nomination; no new media product is selected. No actual guest capability/O grade or universal gate follows.

## Owned audio and MIDI calibration inputs adopted — 2026-10-23

The [sole Root NEW INPUT/code review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session0-audio-midi-owned-inputs-2026-10-23-v1-root-review.json),2605bytes/SHA256 `f9fc1956d8d9184b4d0cd485776041a00464d133d5e9e27a7f8ef11c73757455`, approves the self-authored input bytes only. [Frozen manifest](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-audio-midi-owned-inputs-2026-10-23-v1/manifest.json),2626bytes/SHA256 `22f6fa3950e27b99ffd81b83737c1a9beafdc14fabd7eb17f79a10a7b6805671`, seals16payloads1196004bytes/all17files0444/private0700. The [input catalog](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-audio-midi-owned-inputs-2026-10-23-v1/input-catalog.json),2820bytes/SHA256 `178f387523acc3eb1066cf048c5619a2d3f402f81b9477ca7008c4f5d08fd133`, names exactly these assets:

| Owned input | Geometry | Bytes / SHA256 |
| --- | --- | --- |
| owned-44100-stereo-square-silence.wav |44100Hz,132300frames, PCM16LE L/R; three1-second segments and42-sample period as selected above |529244 / `78952d33caf59fef922093e0f033b838b9eaf7db60f81a727a74e477023288d2` |
| owned-48000-stereo-square-silence.wav |48000Hz,144000frames, same segment/channel definition with48-sample period |576044 / `dc9ce15bd5d919a1a604a5a90f2fa44ccc1209464679f83ba2434c032a1bdfeb` |
| owned-raw-midi-vector.json |Seven desired offsets0–600ms;15literal payload bytes; no SMF/player/sender |836 / `e6f762dcc57c39ddb790cd3b699e4d99dda6a1c240f32d3815cf2c21f1a1a449` |

One construction at12:05:36.645792–.783786UTC exited0/empty stderr after fully read/prebound7016-byte generator and6835-byte separate validator. The writer uses stdlib wave/integer packing; validation parses RIFF/fmt/data and checks channel, silence, amplitude, run and boundary invariants without calling the writer. Two memory-only positives and15malformed negatives passed before asset creation; no third WAV/old fixture was written or run. Root read the new code and choice/prebinding/result/catalog/control metadata, checked all16payload pins, independently parsed every PCM sample and the exact MIDI schedule, and rejected four additional in-memory corruptions. No generator/author-validator replay; all17frozen files unchanged.

Recorded host Python3.12.3/interpreter and76runtime-file/13mapped-path pins are discrete generator-runtime evidence, not hermetic/continuous or guest identity proof. Five resource guards preserved the full6039814144phase floor plus2MiB own output/16MiB headroom,6058688512required bytes, with account11932692480→11931570176bytes and RAMminimum93606232064bytes. These are unreserved points, not quotas or later lifecycle capacity.

**Unchanged limits:** these arbitrary owned stimuli are not recovered/missing original files, device data, waveform comparators, numerical/public laws or original-device equivalence. WAV container/data validation proves no guest acceptance, endpoint/capture or audio timing; the MIDI schedule proves no delivery, clock, tempo or jitter. No guest/QMP/UI/QEMU/guest-v1/media/profile/AUZ action, playback/capture/port I/O, tool acquisition/install/launch, video marker, originalLive/DSP/harness/provider or native helper occurred. Do not transfer them into guest media during Claude's ownership hold. Actual capabilities remainNULL/U, reviewedO0/current24051draft additions/wholeLiveOPEN unchanged. Existing21SessionA INPUT independent-review status is unaffected.


## Host-only official tool archives selected — 2026-10-23

Select one private **session0-official-tool-archives-2026-10-23-v1** source/package-intake packet for exactly the existing candidates: official Coreinfo portableZIP, OBS Windowsx64standalone package, Audacity Windowsx64standalone package without MuseHub, and vendor loopMIDI. Resolve fixed public links/current page versions from official primary sites/repos, retain source/date/provenance and attempt each selected package once. Normal official download redirects are allowed; no credentials, mirror, alternative product/version fallback or retry. Independent source/HTTP gaps get explicit dispositions; resource/custody violation stops the cohort. No new user boot-media prerequisite or approval gate follows.

Scope is host bytes only: max512MiBtotal/max256MiBperpackage,16MiBsource/logs and128MiBownheadroom **in addition to** the unchanged6039814144phase floor and fullremaining source/package/output allowance. No actual-size budget shrink; preserve full S/concurrent limits at every fetch. Record URLs/status/redirectorigin/headers/bytes/localSHA256 and any actually published digest separately. Page/filename versions are not measured ProductVersion; source origin/localhash is not publisher-signature/Win11-usability proof. Bounded ZIP central-directory metadata may be listed; no extraction or executable/code interpretation. Signature, binary version and usable capability remain future legitimate guest checks.

Tension_owner_finish authors; Root solely reviews the frozen NEW source/package packet after fully read/prebound collector/guards and meaningful URL/domain/path/size controls. No extra preparation/review chain. No installation, tool/version/signature execution, driver/EULA change, ffmpeg/video/newproduct, provider/library mutation, playback/capture/MIDI, originalLive/DSP/harness, guest/QMP/UI/QEMU/guest-v1/config/media/VMdisk/AUZ action. Files remain private host inputs; do not copy them onto existing media while Claude owns the guest. All actual guest capabilities/O grades remainU/0.

## Host-only official tool archives adopted — 2026-10-23

The [sole Root SOURCE/package review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session0-official-tool-archives-2026-10-23-v1-root-review.json), 5778 bytes/SHA256 `9a98771f43173d9c555e9c6f8bc9c197443865e8076cb959c756f2da99c6a27b`, approves the selected official-source associations and retained package bytes. The [frozen manifest](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-official-tool-archives-2026-10-23-v1/manifest.json), 4744 bytes/SHA256 `2b6a98ca704a1bdb1a521b7315eed55ec10e5d88f6fa5b890a74f0f4d5830c64`, seals 26 payloads/221462444 bytes, all 27 files0444/private0700. Eight official pages/APIs (699060 bytes) and all four selected packages (220671154 bytes) completed HTTP200 once, without gap, retry or fallback. Root checked the 26 payload pins, eight source/four receipt joins and two published digests; those approvals are inherited below, with no collection or proof replay.

| Retained package | Source label; local bytes / SHA256 | Evidence limit |
| --- | --- | --- |
| Coreinfo portable ZIP | Official page v4.02, distinct from its v4.0 sample; 3182276 / `da7d48956d66cfc2ac3766c30e7f46209cdc5824eb25b1bbd4cb10f124b2d7a4` | Official origin and local hash only; no published digest in the selected page. |
| OBS Windows x64 installer | Official page/API 32.2.2; 159809104 / `c3a0b880adbe64dc4bcb68f93016916ab5b55ae43fd227115287bf80257d92dc` | Official-page CDN bytes match the corresponding official repository asset's published SHA256 and size. |
| Audacity standalone x86_64 MSI | Official page/API 4.0.1; 49795072 / `efb652bf04168f5d4893f28b7cefaaf5ef385d9251544540ac774e3bf54793a3` | Official direct standalone MSI, without MuseHub; published page/repository SHA256 and size match. |
| loopMIDI vendor ZIP | Link filename 1_0_16_27; 7884702 / `975399eb76e2c5a1d553ecd8975ab361261ccab8fd9412b8060b19877cb4e0d5` | Official origin and local hash only; no published digest in the selected page. Vendor Windows7–10 documentation is no demonstrated Windows11 usability. |

[Selection/source locators](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-official-tool-archives-2026-10-23-v1/package-selection.json) and [actual receipts](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-official-tool-archives-2026-10-23-v1/package-results.json) retain URLs, capture dates, HTTP/redirect metadata and exact source associations. Only bounded ZIP central-directory metadata was inspected (7 Coreinfo entries/1 loopMIDI entry); no member payload, extraction, executable semantics, installation, EULA acceptance or version/signature command occurred. Source labels and digest matches establish no actual ProductVersion/FileVersion, Authenticode signer, CPU feature or usable capture/audio/MIDI capability. Those remain UNKNOWN.

Every fetch preserved the full unshrunk **6727680000-byte** root/store account-available floor: unchanged6039814144 phase/concurrent allowance plus512MiB packages,16MiB source/logs and128MiB headroom, with8GiB MemAvailable. These are unreserved points, not continuous capacity or quotas. No guest/QMP/UI/QEMU/guest-v1/existing media/profile/AUZ, originalLive/DSP/harness or provider action occurred. Claude's guest ownership hold remains in force; no O observation/grade, Windows capability result or new user boot prerequisite follows.

## Host-only tools and calibration transfer selected and adopted — 2026-10-23

Select and adopt one new private **session0-tools-calibration-transfer-2026-10-23-v1** INPUT/media packet: a **256MiB FAT32 image labelled LIVETOOLS**, prepared only on the host and **not attached to a VM**. It contains exactly the four approved opaque archives under `TOOLS/`, the [two approved owned WAVs and raw MIDI JSON](#owned-audio-and-midi-calibration-inputs-adopted--2026-10-23) under `CAL/` (7 datafiles/221777278 bytes), and three declared metadata files: `CATALOG.JSON`, `MANIFEST.JSON`, `README.TXT`. These describe the exact subset and bind every copied byte hash/source class, both parent manifests and their Root review pins. They do not mirror either source packet; code/runtime/source pages, old21ALS and AUZ files are excluded. The whole-image hash is outer-only, avoiding self-reference. Source approvals are inherited without a second source or archive review.

The [sole Root INPUT/media/code review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session0-tools-calibration-transfer-2026-10-23-v1-root-review.json), 2869 bytes/SHA256 `f3444ad2738258335528931334579f869c21350d8dd05193e6eb2ae99afdfaef`, approves this bounded host preparation. The [frozen outer manifest](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-tools-calibration-transfer-2026-10-23-v1/manifest.json), 12498 bytes/SHA256 `f694b3e1c5e2f200fdb6bafd1936e79f7e3929f8d1044b6593e22eb93cea2cf8`, seals77payloads490365113 bytes/all78files0444/private0700. [LIVETOOLS.img](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-tools-calibration-transfer-2026-10-23-v1/LIVETOOLS.img) is268435456 bytes/SHA256 `6637f899fb30491b7a5184c6cbaed6cb0c42157d8e6f661c4a6f953889b74771`.

The [actual result](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-tools-calibration-transfer-2026-10-23-v1/result.json) records one format/copy cohort:26 existing private mformat/mmd/mcopy/mdir children, all exit0/empty stderr;10 exact allowlisted readbacks match selected sizes/hashes, and root/TOOLS/CAL listings contain exactly the declared subset. All10 readonly source descriptors retain equal four path/FD endpoints and before/after hashes. Four positive/six negative owned guards ran, with no old fixture/version/proof replay. The first sector's FAT32/LIVETOOLS/55aa metadata and mtools roundtrip establish only this owned host filesystem preparation, **not guest recognition or drive letters**. Original source bytes/templates and all existing media remain unchanged.

Before parent/every child, the unchanged **6727680000-byte** root/store account-available guard preserved6039814144 phase/concurrent bytes plus the full256MiB image,256MiB readback,16MiB metadata and128MiB headroom, with8GiB MemAvailable; actual-size budget shrink was not used. These remain unreserved points. Last retained point13:29:38.584191UTC: account8057028608/raw33022730240 bytes on root/store, MemAvailable93540622336 bytes. No current or future capacity reservation follows.

The image remains unattached and static0444. Future attachment requires coordination after Claude's completion/handoff and final-profile reconciliation; this adoption selects no guest/QMP/UI/QEMU/guest-v1, existing-image/media/profile, AUZ or authorization action. No archive extraction, install, executable/driver/EULA action, playback, capture or MIDI sending occurred. Actual binary versions/signatures, Windows11 usability, attachment/fingerprint effects and guest filesystem recognition remain UNKNOWN/UNTESTED; arbitrary USB fingerprint effects are not inferred. Claude's hold remains unchanged, with no added user boot prerequisite, O observation/grade, macOS proof or whole-product closure.


## SessionA prepared-input sole review selected — 2026-10-23

Select the independent INPUT/code review of all21already-prepared SessionA inputs in the [unchanged v2 packet](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/phase4-windows-session-a-inputs-v2/manifest.json),4854bytes/SHA256 `35a3dd50d40aeb62dd2e74bd51e11e47489bb4bb6e0808e5088ce9e27bb607ac`. Tension_owner_finish first establishes independent eligibility and absence of a prior sole review from retained metadata/history; uncertain independence remainsU. Review the complete declared payload/code/catalog and original two probe recipes/case index:14exact source copies, six literal N1 attribute variants and Creator-omitted plain XML. Check permitted edit/reversal, unchanged decompressed bytes and new N1 gzip envelopes; corrupt inputs are exact byte copies, never reparsed/normalized. Preserve the v1 authoring failure and all frozen files. No builder, old batch/checker/fixture, input regeneration or original/runtime execution is selected.

One sole report directly supplies approved SAFE facts, limits, source pins and retained history; Root cites it without underlying-input re-review. Any NEW audit methods and meaningful in-memory controls are read before their one bounded execution, with full6039814144phase/concurrent allowance plus complete own output/log/final/headroom budget at parent/everychild, no actual-size shrink or retry. This is host-only INPUT review, not guest acceptance, expected-output/criterion transfer, O observation, capability or readiness proof. All guest/QMP/UI/guest-v1/existing-media/profile/AUZ operations remain held under Claude ownership.

## SessionA prepared-input sole review adopted — 2026-10-23

The [sole independent INPUT/code report](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/review-session-a-inputs-v2-independent-v1/report.json),94114bytes/SHA256 `34b8bc6eec72bf6bb718e3d8943dc5590a541abda3db2ed9737abd6741771504`, approves all21prepared inputs with zero findings. Root verified the6916-byte [approved SAFE projection](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/review-session-a-inputs-v2-independent-v1/safe-summary.json),SHA256 `12c382b554692d84d46cd4c72ba5a6efa6dd9cd70952dba1958f90cb4c0f6300`, and read only its scalar pins, approved facts, eligibility disclosure, history, method metadata, resources and limits. Detailed input/custody rows, code and underlying sources remain the sole peer's proof; no second INPUT review or builder/checker replay. [Review manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/review-session-a-inputs-v2-independent-v1/manifest.json),1608bytes/SHA256 `3ae5645c68a1bd4da3dc0f8642271ae35c81a99cf9323ed166179e20fecfb92a`, seals8payloads124378bytes/all9files0444/private0700.

**Admitted INPUT facts:**14raw source copies are exact; six N1 variants match the literal original recipes, preserving all decompressed bytes outside the named attribute edits and permitting full reversal, with new gzipmtime0 envelopes; one Creator-omitted variant preserves N2-019's plain-XML envelope and only removes that attribute. Source probe/case-index joins are pinned. All28v2payloads plus its manifest remain unchanged. The independent Expat structural/text/attribute and lexical byte-span audit used no imported author routines, parsed no corrupt input and generated no new fixture/envelope. The10602-byte/106line author builder was read inertly, not executed. One fully read/prebound17130-byte NEW audit exited0/empty stderr; two in-memory positives/six negatives passed, zero old controls rerun.

**Independence/history qualifications:**the reviewer disclosed no SessionA authoring/alteration in its retained own history; v2 has no named-author field, so author identity remainsunknown. The scoped prior-review search found only an earlier routing/count check explicitly excluding INPUT/code proof; this is not a global hidden-history search. The first author's incorrect gzip assumption for220-byte N2-019 remains a failed20-input partial. Recorded20prefix pins join v2; no oldv1input/builder was reopened or rerun. Forty-eight source-custody records have equal readonlyFD/endpoints/finalhashes. Legacy originalr2paths are0664, not immutable; frozen packet files are0444. Discrete equality proves no global writer exclusion or historical/continuous identity.

Two retained resource points preserve6039814144phase/concurrent bytes plus32MiBcomplete ownoutput/log/final and128MiBheadroom, **6207586304bytes**, without shrink. Account8051355648bytes/RAMminimum93653344256bytes; these are unreserved points. No children;60CPU/512MiBaddress-space/4MiBperfile/core0/cooperative60s limits are not a parent watchdog, absolute wall bound, quota or crash-durability proof.

The earlier independent INPUT-review unknown is now resolved **only for this exact prepared packet**. Actual guest hashes/acceptance, Live outcomes/expected values/criteria/grades remainNULL/U; no Windows/macOS equivalence or O credit follows. Claude retains guest ownership: no guest/QMP/UI/QEMU/image/media/profile/AUZ operation or originalLive/loader/helper/native/provider action occurred. No new input class, behavioral case, release or universal readiness gate. Current24051draft additions/reviewedO0/wholeLiveOPEN remain.


## Windows raw-MIDI method SOURCE followup selected — 2026-10-23

Select one host-only primary-source packet to make the existing Session0 raw-MIDI sender/monitor/timestamp nomination concrete for the owned seven-record/15-byte vector. Use only exact official Microsoft Windows MIDI/monotonic-time documentation needed for one minimal method, retaining actual versions, capture dates, URLs and bytes/hashes. Earlier approved loopMIDI sources are inherited by citation; no second vendor-source review. Distinguish raw short-message packing and clock bytes, receive timestamps/clock origins, scheduling limits and documented support from actual Windows11/loopMIDI behavior. No invented timing tolerance, portable criterion or pass follows; missing source support staysU.

Tension_owner_finish authors, Root solely reviews the frozen NEW SOURCE packet and qualified method/limits. Read/prebind any new collector/guards before once-bounded fetches, preserve failures/no retry/mirror or old source/helper/fixture proof replay. Full6039814144phase/concurrent floor plus complete16MiBsource/output/log/final and128MiBheadroom or larger at parent/everyfetch, without actual-size shrink. No sender implementation, compilation, driver/executable/package acquisition, install, MIDI I/O, originalLive/runtime/model action or guest/QMP/UI/media/profile/AUZ interaction. Claude guest hold remains; this is documentary method work, not new measured capability or a universal readiness gate.


## Windows raw-MIDI method SOURCE followup adopted — 2026-10-23

The [sole Root SOURCE/code review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session0-winmm-midi-method-sources-2026-10-23-v1-root-review.json),4725bytes/SHA256 `fb97ec690935894a8f3f5106fd140ac5cc2048a1cf9c9a95c17cb7d7e06f4454`, approves the qualified documentary method, retaining one explicit callback-contract gap. [Frozen manifest](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-winmm-midi-method-sources-2026-10-23-v1/manifest.json),5083bytes/SHA256 `56988b554ba12aae6c85f088022ba9b833778fabca7019ede0cc8987426d0d4f`, seals30payloads710310bytes/all31files0444/private0700. Root fully read the6909-byte collector,7090-byte method and ten retained primary documents; checked all30pins, exact source/selection/HTTP/catalog joins, derived-text ordering against rawHTML, version metadata and all seven literal DWORD mappings. No collector, old source/helper/fixture/controls or API execution was repeated. Earlier owned-vector and loopMIDI approvals are inherited by citation, not reopened.

One acquisition at14:03:00.575786–14:03:02.761012UTC retained ten official Microsoft pagesHTTP200:577198rawHTML+67828derived-text bytes. The selected IN_CALLBACK locator returned404 with no retained body, retry or alternate fetch. This is a selected-URL gap, not global absence of official callback documentation. The [catalog](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-winmm-midi-method-sources-2026-10-23-v1/source-catalog.json) owns exact URLs, raw/text hashes, capture times and differing ms.date/updated_at/footer labels; none is an actual guest binary version. The [method](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-winmm-midi-method-sources-2026-10-23-v1/method.md) supplies stable per-source text-line locators.

**Document-supported distinctions:**WinMM short messages pack status in the low byte, then optional data1/data2. The seven owned stimuli map to00403c90/006001b0/000000f8/000001b0/000000f8/00003c80/000000f8. Full outgoing statuses are proposed; received running status is expanded, so API messages are not physical-wire bytes and unused received bytes are not assumedzero. Three literalF8stimuli prove no normative24PPQN/tempo law. Input driver's millisecond receipt timestamps start from midiInStart, while sender QPC brackets and later receiving-worker QPC observations describe different events/epochs; subtracting them as synchronized latency is unsupported. QPC documentation distinguishes monotonic interval timing from UTC, cross-thread±1tick order ambiguity and conversion/precision limits; actual guest timing is unmeasured. Sleep readiness is no scheduling guarantee, and midiOutShortMsg can block until output. No timer-resolution/priority/affinity/spin policy or jitter tolerance is selected.

The proposed input-open/start/output-short-message/stop/close sequence remains **not a runnable guide**:callback-safe operations, lifetime/concurrency/queue/overflow detail and high-resolution callback entry timing remainunknown because of the selected callback-source gap. No QPC, managed/file I/O, lock or other WinMM call is asserted safe inside a callback. Error/overflow/unexpected messages must remain visible in any future method; a matching subsequence cannot establish completeness. Actual endpoints, driver/runtime versions, Windows11/loopMIDI usability, receipt, scheduler error and clock correlation remainU. No sender, language binding, compilation, tool/product or execution is selected.

Two new memory positives/five URL negatives passed before acquisition. Thirteen resource points preserve full6039814144phase/concurrent bytes+16MiBcomplete source/output/log/final+128MiBheadroom=**6190809088bytes**, no actual-size shrink. Lastaccount8050262016/raw33015963648bytes/RAM93679919104bytes; unreserved points,30CPU/256MiBaddress-space/2MiBperfile/core0/15ssocket/cooperative240s limits are not an absolute wall bound, parent watchdog, quota, hermetic or continuous provider proof. No guest/QMP/UI/QEMU/media/profile/AUZ, executable/driver/MIDI I/O/WinMM/QPC/Sleep/originalLive/model/provider action, O observation, criterion, readiness gate or whole-product closure. Claude ownership hold/current24051draft additions/reviewedO0/wholeLiveOPEN unchanged.


## Explicit legacy callback-document SOURCE selected — 2026-10-23

The already approved IN_OPEN rawHTML (55024bytes/SHA256 `dbee651449b307e566e0062d23182b709e25978c0c45bf6fc25620d3356744fb`) links text MidiInProc to `/en-us/previous-versions/dd798460(v=vs.85)`. Root extracted only this href/text metadata, without a new source-behavior review. Select that exact [Microsoft legacy document](https://learn.microsoft.com/en-us/previous-versions/dd798460(v=vs.85)) for one new documentary packet. This explicit finite selection does not retry the failed modern-path URL, erase its404 or silently repair the frozen method. No mirror, alternative document, automatic fallback or additional source traversal is selected.

Tension_owner_finish authors; Root solely reviews the new SOURCE/code/addendum packet. Capture raw/text/version/signature and callback-contract facts actually supported, preserving legacy-version/pointer-width and current-Windows applicability unknowns. No permitted-operation, lifetime, queue or timing conclusion may exceed that source; no runnable implementation follows. Inherit approved parent/vector/vendor facts by citation, no old proof/collector/controls replay. Fully read/prebind minimal new acquisition methods and meaningful controls, one bounded official-origin fetch/no retry, full6039814144phase/concurrent+16MiBcomplete source/output/log/final+128MiBheadroom or larger at parent/everyfetch, without shrink. No sender/tool/compiler/package/WinMM/MIDI I/O/original/model/guest/QMP/UI/media/profile/AUZ action. Original404 and all frozen methods stay unchanged; Claude ownership hold remains.


## Legacy callback-document SOURCE adopted with locator erratum — 2026-10-23

The [sole Root SOURCE/code report](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session0-winmm-midiinproc-legacy-source-2026-10-23-v1-root-review.json),5124bytes/SHA256 `3b26604a43c7c51d5bc8f51f4fee50a0ffd90e49e4778d7454dbc2384509c7ab`, approves the exact legacy source and qualified addendum with its additive locator correction. [Final manifest](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-winmm-midiinproc-legacy-source-2026-10-23-v1/final-manifest.json),2510bytes/SHA256 `95a6b79dc6956104621b089fde53c4c0b9123e4839fddeb2d425ea975041cabc`, seals13payloads67827bytes/all14files0444/private0700. Root read the6066-byte new collector,4073-byte addendum, complete source and metadata; checked all13pins/tree/modes/initial-seal joins, HTTP/source/selection/prebinding/resources and derived-text order against rawHTML. No fetch, collector, control or old-source proof replay.

The literal selected legacy URL returnedHTTP200 once/no redirect at14:14:30.045931–.175076UTC. [Raw source](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-winmm-midiinproc-legacy-source-2026-10-23-v1/source.html),38583bytes/SHA256 `5ab3a2943de873d351dc0aa8258da31fb7522003b0ef223244bcf800545d6318`, and [derived text](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-winmm-midiinproc-legacy-source-2026-10-23-v1/source.txt),2191bytes/SHA256 `346368dfe4ac5c0fd074d75aa72650972558351454f7ed41ae120ad69a841038`, retain differing labels:ms.date/footer2016-06-06,updated_at2021-12-02,HTTPmodified2024-11-01. They are documentary versions, not installed SDK/runtime or Windows11 proof.

**Adopt only corrected locators:**source.txt29 calls MidiInProc an application-supplied placeholder whose address is passed to midiInOpen, not an exported function to discover or invoke. Lines31–37 declare voidCALLBACK,HMIDIIN,UINT and threeDWORD_PTR parameters; a packed MIDI DWORD does not justify truncating callback parameters. Line52 makes message parameters message-specific. Line53 warns that multimedia calls inside the callback can deadlock and describes other system functions as safe, in this legacy document. These are source statements with current applicability unknown. A future proposal keeps WinMM send/stop/close outside its input callback. Combining the inherited QPC system-API category with the general legacy allowance nominates callback QPC only conditionally; no current safety, callback-entry latency or measured guest behavior follows.

The [additive locator erratum](../../analysis/ableton-live-12.4.3/r2-large/reference-windows-vm/session0-winmm-midiinproc-legacy-source-2026-10-23-v1/locator-erratum.json),1543bytes/SHA256 `adcc0550cf4d77245d99745cfb83c7021bcb58597fd5a257ce745db8c97464b6`, preserves initial frozen prose/summary/manifest and corrects their off-by-two references to52/53. Root's first metadata reader stopped at the third correction's `correct` field after completing pin/source/line checks; continuation covered only the unfinished erratum/final-manifest/report tail, with no completed-prefix replay. Both histories remain explicit, not overwritten or treated as failed original execution.

Two new positives/four URL negatives and three unreserved resource points preserve full6190809088bytes=6039814144phase/concurrent+16MiBcomplete outputs+128MiBheadroom, no shrink. Finalaccount8049852416/raw33015554048bytes/RAM93674496000bytes. CPU15/256MiBaddress-space/2MiBperfile/core0/15ssocket/cooperative30s limits give no absolute wall, quota, continuous/hermetic provider or crash-durability guarantee.

This narrows the documentary callback gap while preserving the earlier404/frozen method and inherited vendor/vector proof. Actual Windows11 ABI/header/binding/usability, callback threading/reentrancy/serialization/lifetime, queue/overflow/close synchronization, dispatch delay and timing remainU. No sender, runtime/tool/driver/API/MIDI I/O/guest/QMP/UI/media/profile/AUZ/original/model action or runnable/capability/O/readiness/timing criterion follows. Claude ownership hold/current24051draft additions/reviewedO0/wholeLiveOPEN unchanged.


[The user reports Live authorized](../decisions/adr-0006-reference-observation-reopened.md#user-reports-live-authorized-guest-handoff-status-pending--2026-10-23). Current routing no longer asks for AUZ or credentials. Claude handoff status and final-profile/authorization reconciliation precede guest observations; capability fields remain unmeasured and reviewed O stays zero. Static analyst work continues.


## Current Windows sitting priority after confirmed handoff — 2026-10-23

[ADR0006's current routing](../decisions/adr-0006-reference-observation-reopened.md#confirmed-handoff-and-windows-sitting-priority-supersede-static-queues--2026-10-23) supersedes the dated Claude-hold statements in this run sheet. The user/Claude handoff is confirmed; Root alone resumes the offline/no-NIC guest for Session0 profile/authorization/capability reconciliation, then all nine SessionA records in the retained order above. Static author/reviewer queues are parked; host-only support/docs do not operate guest/QMP/UI/media. Earlier host archive/INPUT/media/source-method approvals remain inherited; no second source/INPUT review, universal inventory gate or new key/AUZ/credentials request is added. Each record retains its own prerequisites, stopping conditions and explicit not-observed/U disposition when unavailable.

Claude's reported Live12.4.3/build/hash, WindowsPro26300/unactivated observer profile and44.1kHz ich9HDA audio are handoff claims awaiting current evidence; the203924 authorization-session crash is separate setup history. Root's first process disappeared before a keyboard action, followed by one supplied-script existing-disk offline relaunch, not reinstall/revert/duplicate boot. New guest identity, actual tool versions, capture/audio/MIDI/CPU/Save/Export results remain UNVERIFIED until retained and solely reviewed. The first sitting has one sole NEW actual-evidence/code review after freeze, without re-reviewing the21INPUT fixtures or approved tool sources. Current24,051draft additions/reviewedO0/main25,095of268,015/releases36current19/wholeLiveOPEN remain unchanged.


## Three-source Session0 and SessionA execution — 2026-10-23

The user-amended [plan revision6](full-live-specification-plan.md#revision-6--paired-observation-and-static-analysis-2026-10-23) supersedes the earlier sitting-only scheduling restriction: O, S and X run as three concurrent subagents on document container/save path, transport state, mixer values and MIDI note storage. O=tension_owner_finish alone drives the guest; S=tension_review_finish and X=o137_finish stay on the host. Root relinquished guest input after handing over the active first SessionA case. Already known authorization/identity facts are inherited; no repeated readiness confirmation delays the sitting. Each route adopts through its existing separate packet and sole review, with no combined packet, extra review, required ordering or platform-equivalence inference. Root solely reviews NEW S/X scope; o137 is the sole O reviewer after its own natural closed X boundary. Old unrelated static author freezes and their unbegun reviews remain parked; their bytes and unknowns are unchanged.

## Reference guest operation — 2026-10-23

How to run the Windows reference guest that Claude built on 2026-10-23. The
guest's identity is recorded in
[ADR 0006](../decisions/adr-0006-reference-observation-reopened.md). All paths
are under `/var/tmp/sound-analysis/reference-windows-vm/`.

- **Launch.** `install-v1/run-guest.sh run` starts the software TPM and QEMU
  with KVM and no network card, in a window on the host desktop.
  `run-guest.sh run net` adds a user-mode network card; it was used once, for
  online authorization. The script does not attach the session input and
  evidence images, so the driver attaches its own.
- **One driver.** Only one QEMU may use `guest-v1/guest.qcow2` at a time, and
  only one worker drives the guest. QMP settings persist until the guest
  restarts: a link set down through QMP on 2026-10-23 silently blocked the
  authorization login until it was set up again.
- **Control.** QMP listens on `install-v1/qmp.sock`. The helper
  `install-v1/qmp.py` takes `shot FILE.png`, `keys` (chords such as
  `meta_l-r`), `type TEXT`, `click X Y` in 1920 by 1080 screen pixels, and
  `cmd JSON`.
- **Account.** Local account `observer` with automatic logon. Its password is
  in `install-v1/autounattend.xml`.
- **Baselines.** The guest disk holds two internal snapshots:
  `live1243-installed-unauthorized` and `live1243-authorized-offline-audio`.
  Matching firmware variables and TPM state are copied in
  `install-v1/snap-<snapshot name>/`. To restore, with the guest off, run
  `qemu-img snapshot -a <snapshot name> guest-v1/guest.qcow2` using the
  private `qemu-img` in `tools-v1/root/usr/bin/`, then copy `OVMF_VARS.fd` and
  `tpm/` back into `guest-v1/`.
- **Audio.** The guest's Intel HDA output is written to
  `install-v1/guest-audio.wav` whenever Live's audio engine runs, silence
  included. That is 176,400 bytes a second, about 15 GB a day. Truncating the
  file while QEMU runs corrupts it, so move or delete it between launches.
