---
id: PLAN-LIVE-SET-STRUCTURE-HANDOFF
type: research
status: current
updated: 2026-10-21
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Live Set structure handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [live-set-structure-v1](../../handoff/live-set-structure-v1/README.md), approved with narrowing and corrections by a separate review agent ([review record](../../handoff/live-set-structure-v1/REVIEW.md)). It has 34 cases.

The review made these changes:
- **Device placement:** devices are removed from T11-MIN and every fixture, so no case depends on device placement.
- **Ids:** `NextPointeeId` is now 67; case 025 uses 66, and case 022 uses targets 67 and 68.
- **Rules held:** the open-path rule and the freeze-slot rule hold, with the stated inference.
- **Track rule:** it reads "no audio, MIDI or group track".
- **Path fallback:** limited to codes 0 and 1.

For the spec author:
- make T11-MIN device-free (LSS-020 becomes 66; LSS-014 becomes 67, 68 and 69);
- add arrays to REQ-001;
- add codes 2 to 7 to REQ-009;
- add the track row to REQ-018;
- cite a source for the added send's value.

## Draft reconciliation (2026-10-19)

Draft r2 applies the device-free fixture, class-specific Value refusal, isolated mutations, code 2–7 uncertainty, constructor evidence and total-return count. Only A4/A5 remain relevant to the released fixture; the device-placement assumption is excluded. The preparation instructions below are the historical staging plan.

## Decision and boundary

Stage a finite first candidate, live-set-structure-v1, from
[SPEC-LIVE-SET-STRUCTURE revision 1](live-set-structure.md). It follows the
pattern and gates of the [als-container plan](als-container-handoff-plan.md),
the [transport-state plan](transport-state-handoff-plan.md), the
[midi-config-v2 plan](midi-config-v2-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff). Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary)
and [ADR 0003](../decisions/adr-0003-no-reference-execution.md), every
expectation is documented, static-derived or, for one checksum, extracted
execution. Nothing was run against Live or a candidate.

The scope is the settled structure: the validation-walk refusals (A1 and A2
settled), the element status of the reference minimal set T11-MIN, the track,
slot and scene rules, sample-reference fields and resolution, and the Id
rules. T11-MIN is a generated fixture of the release, and every other fixture
is T11-MIN with one change. Excluded: the U items listed in
[Q-022](../questions.md#q-022-live-set-structure-load-rules), saving (A7 and
the `RelativePathType` U) and device placement (A6, which Q-022 lists as open).

Three open assumptions stay in the release as stated, behaviorally named
assumptions: A4 (`sample-folder`, one case), A5 (`list-item-ids`, three
cases) and A6 (`device-placement`). A6 cannot be avoided while T11-MIN itself is
the reference set: T11-MIN places `UltraAnalog` and `Amp` directly in track
device lists, so every case that expects T11-MIN or a variant to open rests on
A6 (review gate 1).

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
reference or candidate execution has run, and no compatibility is claimed.

## Scope

| Requirement | Included | Excluded remainder |
| --- | --- | --- |
| 001 | Element forms; match by name; absence not itself a refusal; unknown child skipped; refusals: `<NextPointeeId />`, a repeated child of a non-list element, an unknown item name in `Tracks` | Value-element rule beyond `NextPointeeId` (finding F4); `KeyMidi` duplicates; classes each list accepts (U); other lists' class test (A5) |
| 002 | Display order; no player track; player after return; `TrackGroupId` ≠ −1 without group tracks | Other classes in `Tracks` (U); group tracks otherwise |
| 003 | Track `Id` form; `Name` and `Color` written | Displayed name, `EffectiveName` derivation, colour palette (U) |
| 004 | Placement; tempo, time-signature and crossfader locations; absent main or cue track replaced; new tempo 120 | Values of a new main or cue track beyond tempo |
| 005 | `DeviceChain` children per kind; mixer and device list locations; `AudioOut/Main` in fixtures | Other outputs, absent routing (U, Q-022) |
| 006 | Slots, scenes, slot form; Ids do not order; freeze count = session count | Slots against scenes, zero scenes, two clips, wrong clip kind (U); slot-to-scene binding (Inferred); scene launch (U) |
| 007 | Clip element, kind per track, `Id`, `Time`, `Name` | Other clip fields (other specs, T1.3) |
| 008 | `SampleRef` and `FileRef` children; codes 0 and 1; `Path`, `Type` 2; size, CRC, frames, rate; `LastModDate` definition | Code names and bases 2–7; `Type` meaning (U) |
| 009 | Codes 0 and 1 against the set's folder (A4); `Path` fallback for 0, 1, 2, 6 and not 3, 5, 7; missing sample does not refuse | Report, search, relocation, identity use, playback (U, Q-022) |
| 010 | Stored length and rate equal the file's; fixture sample form | Decoding, mismatched length or rate (U, Q-022) |
| 013 | Holders per return; `SendsPre` form; fewer added at −70 dB; more than R refused | `SendsPre` count (U, Q-022); `EnabledByUser`; send-to-return binding |
| 014 | Envelope locations; `PointeeId` 0 or dangling removed | Later removal of "empty or half-dangling" envelopes (U) |
| 015 | Id form; absent reads 1; Id 0 or none refused; `NextPointeeId` too low refused; absent target tolerated | Which new Id (U); duplicate and negative Ids (U, Q-022) |
| 016 | Id form; negative, lettered, repeated refused (A5); Ids do not order or link | Id-less items (U, Q-022); other Id spellings |
| 018 | T11-MIN opens with its content (A6); element status table | Statuses that cite other specs' unreleased parts (finding F10) |
| 011, 012, 017 | None | Save (A7, U), device placement (A6, U) |

### Case disposition

The payload numbers cases LIVE-SET-STRUCTURE-001 to 034. Draft IDs stay in
`traceability.json`.

| Draft case | Release case | Change |
| --- | --- | --- |
| LSS-001 | 001 | Narrowed: track names, colours and devices not judged (F5); basis A6 only (F6) |
| LSS-002, 003, 006 | 002, 004, 006 | 006: `FooTrack` inserted first so that R stays 1 |
| LSS-005 | 003 | `SendPreBool` also removed (F2) |
| LSS-004 | 005 | Every `Sends` list also emptied (F1) |
| LSS-019, 016, 017 | 008, 009, 010 | As written |
| LSS-031 | 012 | Narrowed: save part removed (A7) |
| LSS-023 | 014 | As written |
| LSS-029, 030 | 015, 016 | 015: factory-default-set obligation (F8) |
| LSS-007 | 017 | As written |
| LSS-008 | 018 | Changed: one freeze slot removed instead of a session slot added (F3) |
| LSS-011, 012, 013, 014 | 019, 020, 021, 022 | 022: the new holder's targets get Ids 69, 70 and `NextPointeeId` 71, by T11-MIN's rules |
| LSS-028 | 023 | Narrowed: save and reopen removed (A7) |
| LSS-020, 021, 022, 024, 025, 027 | 025–030 | As written |
| LSS-032 | 031 | As written (A4) |
| LSS-033 | 032 | Narrowed: missing-file report not judged; sample absent by setup |
| LSS-034 | 033 | Path substituted at setup, as the draft says |
| LSS-036 | 034 | Extended: `DefaultDuration` and `DefaultSampleRate` (REQ-008 D clause) |
| New | 007, 011, 013, 024 | Static clauses without a draft case: grouping (002 clause 4), lettered Id (016), duplicate member (001), `PointeeId` 0 (014) |
| LSS-009, 010, 015, 018, 026, 038 | Not released | U |
| LSS-035 | Not released | The type-7 outcome can change through the U library relocation and missing-file search |
| LSS-037 | Not released | S-cond A6, open in Q-022; REQ-012 unreleased |
| LSS-039, 040 | Not released | Save: S-cond A7 and REQ-011 U |

Counts: 34 cases, 18 refusals and 16 that open or compute: 9 positive, 3
missing-element, 3 repair and 1 computed. Device-placement is listed by 15
cases, list-item-ids by 3 and sample-folder by 1.

## Findings while staging

Proposed corrections for a spec revision 2. This page does not edit the spec.

- **F1.** LSS-004 does not isolate REQ-002's order rule. With
  `ReturnTrack Id="3"` before the audio track, R is 0, and every mixer's one
  holder exceeds it. REQ-013's refusal comes from the root post-load step,
  which runs before the walk (`traces/tracks/trace.txt` items 3 and 5), so the
  set is refused for the holder count first. Release case 005 empties every
  `Sends`. Its one `SendPreBool` then equals the number of return tracks but
  not R, which `schema_check.py` reports as the REQ-013 unknown shape; no load
  check of `SendsPre` was found.
- **F2.** LSS-005 removes `Tracks` but keeps the `SendPreBool`, a `SendsPre`
  count unknown. LSS-002 already removes it; case 003 does the same.
- **F3.** LSS-008 appends a session slot, making 3 session slots against 2
  scenes: the REQ-006 unknown. Removing one freeze slot isolates the rule.
- **F4.** REQ-001 refuses "a base value written as an element" without
  `Value`. The reader applies this to members of base type (−4), such as
  `NextPointeeId`, but not to compound members whose value is an attribute
  member: released transport-state-v2 REQ-007 reads `<LoopOn />` as absent
  ([transport-state native](../research/transport-state-native.md#how-a-set-reaches-the-transport-objects)).
  There is no contradiction in the evidence, but a reader without the class
  schema cannot apply the clause. The release grades `NextPointeeId` only.
- **F5.** LSS-001 expects the track names `Lead`, `2-Audio` and `A-Return`.
  For the two tracks with an empty `UserName` the displayed name rests on
  REQ-003's U clause (derivation and recomputation of `EffectiveName`). Not
  graded; clip and scene names are.
- **F6.** LSS-001's basis "S-cond (A4–A6)": A4 is not needed to open (REQ-009
  says an unresolved sample does not refuse); A6 is, and Q-022 lists A6 as
  open. The revision note's proposed first release (LSS-035, 037, 039, 040
  included) contains cases that rest on A6, A7 and U parts.
- **F7.** `make_fixture.py` writes `T11-MIN.als` with Python's gzip header,
  OS byte 0xFF. als-container-v1 grades only the header
  `1F 8B 08 00 00000000 02 13`. The release stores the byte-identical XML in
  that form; the spec's description (one member, FLG 0, MTIME 0) holds for
  both.
- **F8.** LSS-029's tempo 120 equals T11-MIN's own tempo, so it does not tell a
  new main track from the stored one. transport-state-v2 gives no expectation
  for a missing `MainTrack`; this release adds one, with that release's
  factory-default-set obligation.
- **F9.** LSS-033's "reported missing" part is U. LSS-035 expects type 7 to
  leave the file missing, but the U library relocation of types 2, 5 and 7 and
  the U missing-file search, which may use the size and CRC identity, could
  find the file at `Path`.
- **F10.** REQ-018's table gives statuses from other specs' unreleased parts:
  mixer values V by REQ-MIXER-VALUES defaults (mixer-values-v1 excludes
  new-mixer values); `WarpMarkers` R by REQ-WARP-MARKERS-004 (warp-markers-v1
  excludes audio clip lists with fewer than two markers). The release marks
  them Write, as it does the `AutomationEnvelopes` V row.
- **F11.** REQ-013's U clause compares `SendsPre` with "the number of return
  tracks", and REQ-013's holder rule uses R. They differ only when a return
  is not last (F1). The release counts every `ReturnTrack` item.
- **F12.** Open questions still call Q-022 "proposed; not yet filed". Q-022 is
  filed.

## Deliverables

- Payload: [live-set-structure-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/live-set-structure-v1/README.md),
  `AGENTS.md`, `spec.md` (behavioral contract, comparison convention,
  assumptions and reference obligation), `cases.json` (34 cases), `fixtures/`
  (T11-MIN as `.als` and a decoded `.xml` reading copy, 30 one-change `.als`
  variants, and `Samples/T11-tone.wav`) and a draft `manifest.json`
  (`release_status: candidate-unreviewed`, review pending). The manifest lists
  37 payload files; with itself the package has 38. Draft manifest SHA-256:
  `0582db40dab4a0922851bc3a26667cec4f1520a7019f1de4d00b56f1fff53737`. Review
  edits will change it.
- Analyst side, never shipped: `live-set-structure-v1-analysis/` with
  [build_lss.py](../../analysis/ableton-live-12.4.3/handoff-staging/live-set-structure-v1-analysis/build_lss.py)
  (fixtures, cases, manifest, checks, seal and verify),
  [lss_cases.py](../../analysis/ableton-live-12.4.3/handoff-staging/live-set-structure-v1-analysis/lss_cases.py)
  (case data, edits, isolation declarations, evidence locators),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/live-set-structure-v1-analysis/traceability.json)
  (each case and released clause mapped to evidence keys, assumptions and its
  draft source, plus the excluded draft cases) and
  [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/live-set-structure-v1-analysis/author-validation.json).

## Evidence traceability

Evidence is the [t11-structure-v1 run](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/manifest.json)
(`Live.arm64` `3a99ceea…d1c383cfad`, x86_64 slice `1bae9a97…be999b0`, schema
`12.0_12402.txt` `b7c9d4c7…789d0f299`), the N1 reader notes for the element
rules, and the released mixer-values-v1 text rule for `-inf dB`. Per-case
locators are in `traceability.json`; the payload contains none of them.

| Release cases | Evidence keys | Assumptions |
| --- | --- | --- |
| 001, 031, 032, 034 | `fixture`, `schema-check`, `survey`; `resolution`; `crc`, `duration`, `fileref-fields` | A6; A4 (031) |
| 002–005, 007 | `walk-tracks`, `walk-grouping`, `holders`, `song-ctor`, `open-path` (A1 settled) | none |
| 006, 012–014 | `list-loader`, `reader-n1`, `unknown-child` | A6 (012) |
| 008–011 | `survey`, `list-loader`, `list-id-attr` | A5 (009–011), A6 (008) |
| 015, 016 | `song-ctor`, `tempo-default` | A6 |
| 017, 018 | `walk-slots`, `freeze-empty` (A2 settled), `open-path` | none |
| 019, 020 | `survey`, `list-loader` | A6 |
| 021, 022 | `holders`, `new-send` | A6 (021) |
| 023, 024 | `dangling` | A6 |
| 025–030 | `nextpointee`, `pointee-postload`, `preset-flag` (A3 settled), `registration` | A6 (027, 030) |
| 033 | `resolution` | A6 |

## Fixture construction and sanitization

`build_lss.py build` imports `make_fixture.py` unchanged. It writes the
sample with `wav()` and T11-MIN with `build()` and `render()`, and stores the
XML in gzip with header `1F 8B 08 00 00000000 02 13`, raw deflate at level 9
and the CRC-32 and length trailer. Each variant parses T11-MIN, applies one
edit from `lss_cases.py`, and renders it in make_fixture's layout; a
round trip without an edit reproduces T11-MIN byte for byte. The sample is a
generated sine tone; nothing shipped is read except the schema file, which the
checker reads and which is not copied. `T11` in the file names, the
`Samples/T11-tone.wav` reference and the invented `Path` value
`/T11/Samples/T11-tone.wav` come from T11-MIN itself.

The payload names target elements by element name and uses three behavioral
assumption labels. It carries no draft case IDs, analysis assumption IDs,
addresses, function or class names, recovered message strings, evidence
links or schema content.

## Mechanical checks performed

`build_lss.py seal` (CPython 3.13.9 `-I`, zlib 1.3.1) wrote the author
validation:

- T11-MIN's decoded XML equals `r2/t11-structure-v1/fixtures/T11-MIN.xml`, and
  the sample equals that run's WAV. A rebuild reproduces every staged file
  and the manifest hash. Every `.als` has the stated header, a valid trailer
  and LF text, and the 31 set fixtures are distinct.
- Every case input was checked with the T11 checker (`schema_check.check`,
  `fixture_audit.measure`, `refusals` and `unknowns`) and with `extra()`,
  which measures the four conditions the checker does not: a value element
  without `Value`, a repeated member, grouping without a group track and a
  lettered list-item Id. Each refusal fixture shows exactly its tested reason
  and each other fixture none, as declared per case. The one exception the
  author allowed is case 005's `SendsPre` shape (F1). The checker's `rules()`
  cannot read `<NextPointeeId />` (case 014). That case was measured with the
  value restored; `extra()` measured the missing `Value` itself.
- Case 034's values were recomputed from the staged sample: size 176444, CRC
  47018 (equal to the x86_64 run in `out/x-crc.json` on the same 16,384-byte
  prefix), 44,100 frames at 44,100 Hz. The CRC rule gives 65,256 for
  `123456789`.
- `fixture_audit.py`, run unchanged over an export copy without case 014
  (whose `<NextPointeeId />` stops it), finds 0 contradicted cases. It labels
  the 13 checker-measured refusal fixtures "not isolating". That is its
  released-fixture meaning: the structural rule refuses, which here is the
  rule under test.
- Hashes and sizes of the 37 listed files match, the inventory equals the
  directory, all case inputs exist and the 8 Markdown links resolve inside the
  package. The deny-list scan of every text file and decoded fixture has no
  hit apart from "decompil" in `AGENTS.md`'s forbidden-inputs list, worded as
  in the released packages. A probe copy with planted terms was flagged.
- In the export copy `scratchpad/stage-lss/live-set-structure-v1/` (outside
  the checkout), `verify` and an independent `sha256sum -c` matched all 37
  hashes, and the copy is byte-identical to staging.

Not checked: any reference or candidate execution; A4 to A6; and whether every
field value of T11-MIN also satisfies the other released contracts. The T11
checker tests structure only.

## Review gates still required

1. **Scope review**, in a separate context. Check every included clause and
   all 34 expectations against the locators, F1 to F12, the four new cases
   and the narrowing of LSS-001, 004, 005, 008, 028, 029, 031 and 033. Rule on
   A6: accept it as a stated assumption over T11-MIN, or ask for a device-free
   variant of T11-MIN as the base of every case except 001. Rule on keeping
   A4 (case 031) and A5 (cases 009 to 011) as stated assumptions.
2. **Quality and sanitization review**: behavioral completeness, the setup
   and state-key conventions, case 033's setup-time path substitution and
   case 034's computed comparison. Exclusions must agree between the contract
   and the manifest. Confirm no internal structure or analyst link.
3. **Cross-release consistency**: T11-MIN's field values against the
   released transport-state, mixer-values, clip-launch, midi-note-storage,
   warp-markers, automation-envelopes and als-container contracts.
4. **Evidence identity**: re-hash the t11 run and the pinned image before
   release.
5. **Fixture and sharing review** of the 31 set fixtures and the generated
   WAV, including the product name in element content (none) and the invented
   `Path`.
6. **Sequencing**: the draft says this release should be reviewed together
   with the corrective fixture releases of the five refused families. Its
   rules refuse their fixtures, so a candidate that implements both cannot
   pass those cases until they are superseded.
7. **Finalize**: add `REVIEW.md`, set the manifest review fields,
   `release_status` and `release_date`, re-run `seal`, verify an isolated
   export, and record the manifest hash in the handoff catalog.
8. **Publish** only after approval. Copy the package unchanged to
   `handoff/live-set-structure-v1/`, then update the catalog, spec status,
   coverage, indexes and log. An isolated implementation workspace remains
   unprovisioned.

## Historical staging disposition — 2026-10-18

Staged on 2026-10-18 as an unreviewed candidate: 34 cases, partial
REQ-LIVE-SET-STRUCTURE-001 to 010, 013 to 016 and 018, with 011, 012 and 017
unreleased. It is not published, and no handoff exists for
SPEC-LIVE-SET-STRUCTURE.

## Current disposition — 2026-10-21

The reviewed local [live-set-structure-v1](../../handoff/live-set-structure-v1/README.md) was released2026-10-18 as the review outcome above records. Its34objects remain current/immutable; preceding unpublished-candidate statements retain historical staging context. [Draft R3](../research/live-set-structure.md#live-set-owner-r3-finite-crc-annex-adoption--2026-10-21) adds253finite initial-zero/one-byte nativeCRC16 cases/three inheritedrefs while preserving all18bodies/40oldrows/released34scope. Full32/portableexpected/comparatorNULL; no actualfilematching/OpenSave/public/ARM/lifecycle law. No new release selected. Current implementation-workspace state belongs to [project status](../project.md#current-phase); old unprovisioned statements record staging time.
