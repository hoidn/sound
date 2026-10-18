---
id: PLAN-MIDI-NOTE-STORAGE-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# MIDI note storage handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [midi-note-storage-v1](../../handoff/midi-note-storage-v1/README.md),
approved with one narrowing (RVN-03) by a separate review agent
([review record](../../handoff/midi-note-storage-v1/REVIEW.md)). The manifest
SHA-256 is `90e799158256b226dde22aff88bae18cdc789d49952469611a455b25cc08e0d4`.
All 67 cases remain.

The reviewer's own static check found that the note value limits apply when a
set is opened. The same condition also governs the NoteId checks and the
per-note list rules, so 46 cases relied on it, not 4. The assumption is now
removed from the contract.

- **Draft MNS-001:** no case expects probability-group content or the group
  NextId. MNS-001 and the comparator were reworded so they no longer read as if
  they did.
- **Evidence round d4-0001:** the 16 per-note list cases that depended on it
  were re-established from the corpus and the binary. Their excerpts are kept
  in the review directory.
- **RVN-03:** REQ-009's numbering order now requires key tracks to be stored in
  ascending key order.

For the draft spec:

- Widen assumption A1 to every open-time step and mark it established.
- Add the REQ-009 precondition.
- Retain d4-0001.

The tables below describe the staged candidate.

Applied in revision 2 (2026-10-18); rejected: copying d4-0001 into the retained run (the review excerpts are cited instead) and F1's PRB-S7-09 extension (no probe will run, ADR 0003).

## Decision and boundary

Stage a finite candidate, midi-note-storage-v1, from
[SPEC-MIDI-NOTE-STORAGE revision 1](midi-note-storage.md). The candidate follows
the pattern and gates of the [als-container plan](als-container-handoff-plan.md),
the [transport-state plan](transport-state-handoff-plan.md) and the
[midi-config-v2 plan](midi-config-v2-handoff-plan.md), and the
[release workflow](../workflows.md#release-a-handoff). Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary)
every expectation is a static derivation; nothing was executed.

The scope is every D or S clause of REQ-001 to 010, 013, 014 and 016 that has an
exact expected value and does not depend on an open question. REQ-011 is excluded
outright, and REQ-012, 015 and 017 are unreleased. Everything that
[Q-018](../questions.md#q-018-midi-note-key-range-and-ordering-after-load) keeps
open stays out: MIDI keys outside 0 to 127, a missing key and repeated keys;
re-sorting after load; list Ids and empty KeyTracks; refusal presentation; and the
adjustment of lists that reach the edges of their note. No fixture has a key other
than 36 or 38, and no release expectation names a key range.

Two choices differ from the draft spec:

- **Fixtures.** The spec builds each case from a shipped clip file (B0) and
  places it in a set by drag and drop. Shipped content cannot travel, so each
  fixture is an authored gzip Live Set holding F0 or F1 with one edit, and the
  action is open, then save. Assumption A2 is restated for that action (I2).
  The release's reference obligation embeds the fixture's notes element in a
  full set saved by 12.4.3.
- **Refusal.** REQ-017 leaves open whether a refusal rejects the whole set or
  drops only the clip. The outcome `refused` therefore matches either, and
  presentation is never compared (I3).

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
reference or candidate execution has run, and no compatibility is claimed.

## Scope

| Requirement | Included in v1 | Excluded remainder |
| --- | --- | --- |
| 001 | Five children in order; KeyTrack `Notes` then `MidiKey`; non-`MidiNoteEvent` child refused; structure saved in order | Missing structural children (U); shipped key statistics |
| 002 | Types; any order; repeated attribute refused; decimal text rule, `Invalid` in Duration and TimeOffset, binary32 rounding; Boolean tokens; integer forms and refusals | ` 7 `, `+7 ` (U); `-` sign; `#`, `0x`, `inf`, `nan`; values of 1,000,000 or more; integer values above 1,000,000 |
| 003 | All S clauses | Omitted required attributes (exclusion) |
| 004 | All S clauses | Shipped-writer facts (D, not behavior) |
| 005 | All S clauses, under I1 | NaN |
| 006 | Formula, sentinel unchanged, on-grid unchanged, examples | Negative-zero results (U); Time `Invalid` after load (U) |
| 007 | S clause: note outside the loop and Duration 0 kept | Meanings (U); shipped domains (D, not behavior) |
| 008 | All S clauses | Negative ids |
| 009 | Next-id raise; numbering in ascending key order; saved ids and next id; NoteId absent everywhere | Missing generator, unsorted keys (U); negative next id |
| 010 | Sorted, non-overlapping input keeps its order; overlap or equal Time not refused | Re-sorting, trimming, merging (U, Q-018) |
| 011 | None | All of it (U, Q-018) |
| 012 | None; Ids are not compared | Id meaning, preservation, repeats, empty KeyTracks (U, Q-018) |
| 013 | Structure; curve default 0.5 and omission; TimeOffset and Value always written | Meanings (U); omitted TimeOffset or Value |
| 014 | Removal rules; duplicate pair refused; Invalid drop; Value limits; stable sort; empty list removed; lists strictly inside their note unchanged | Lists reaching the note's edges (U, Q-018; MNS-053) |
| 015 | None | All of it: group shape unknown, cases blocked |
| 016 | Number, integer and Boolean text for in-scope values | Negative zero (U); values within 1e-12 of a power of ten in log10 |
| 017 | None | All of it (U, PRB-S7-02) |

### Case disposition

| Draft cases | Candidate | Change |
| --- | --- | --- |
| MNS-001 to 010, 012 to 022, 025 to 033, 039 to 042, 046 to 048, 050, 052 | Released | Full saved notes element given for every open-save case. MNS-001: group content and group NextId not compared (F2). MNS-003: n2 expectation added (F9). MNS-017, MNS-051: REQ-002 added (F4). MNS-041, 046, 052: the unstated event Value set to 1 |
| MNS-043, 044, 045, 049, 051 | Released as 043a to 043f, 044a to 044c, 045a and b, 049a and b, 051a and b | One fixture per variant |
| MNS-036 | Released, narrowed | Outcome only; saved notes unknown (PRB-S7-06) |
| MNS-011, 023, 024, 034, 035, 037, 038, 053, 060 | Not released | Unresolved |
| MNS-054 to 059 | Not released | Blocked: group shape unknown |
| New MNS-061 to 071 (071a, b) | Released | One case each for a released clause without a case (F8) |

That gives 67 cases: 55 from the 45 gradable draft cases, and 12 new. 51 expect
`loads` and 16 `refused`; 49 are open-save. Four (MNS-014 to 017) rest on I1, and
their `expectation_provenance` says so.

## Findings while staging

Proposed corrections for a spec revision 2; this page does not edit the spec.

- **F1.** The draft's construction uses a shipped clip and drag and drop; see
  the decision above. The S7 probe procedure stays valid for the clip-file
  route. PRB-S7-09 should also cover an open-save of a set.
- **F2 (error).** MNS-001 expects the saved `Notes` to equal F0 apart from Ids.
  That includes an empty `NoteProbabilityGroups` and group `NextId` 1. REQ-015
  leaves the saved group text and whether the group NextId is raised on load
  unknown, so MNS-001 claims more than the spec supports. Proposed: "apart from
  Ids, `NoteProbabilityGroups` and the group generator".
- **F3 (gap).** REQ-002 gives integer text rules only for NoteId, both NextIds and
  the group id. `MidiKey` and `CC` are Int fields read by the int parser
  `0x1002fd908` (n1-0006 `0x10152bfb8.c`, type 0x11), whose `-` handling is U in
  REQ-TRANSPORT-STATE-006. The list `NoteId` is Int64 and presumably uses
  `0x101533e14`. The candidate limits these fields to plain decimal and relies on
  I7 for CC −2, −1 and −3.
- **F4 (error).** MNS-017 and MNS-051 read the text `Invalid`. That reading
  belongs to REQ-002 through REQ-TRANSPORT-STATE-004 r2, which transport-state-v1
  excluded. The cases list only 005 or 014. The candidate adds 002 and states
  the `Invalid` rule for Duration and TimeOffset only.
- **F5 (gap).** REQ-010's order clause does not mention same-key overlap, yet
  REQ-010 U leaves the saved form of overlapping notes open. The candidate's
  clause adds "no note starting before the previous note of its key ends". No
  F0 or F1 case overlaps.
- **F6 (gap).** Neither the saved order of per-note lists nor the attribute order
  of a saved event is stated. The list writer emits list order (research,
  Writer). The candidate compares neither.
- **F7 (precision).** "The value must fit in 64 bits" is signed. The whole-span
  converter `0x101524d8c` (corpus chunk-00813, offset 61888) is a signed 64-bit
  `from_chars`: it skips leading zeros, accepts `-`, and fails with errc 0x22
  above 9,223,372,036,854,775,807. Proposed wording: "at most
  9,223,372,036,854,775,807". The 63-character limit counts leading zeros.
- **F8.** Proposed r2 case rows: MNS-061 to 071, with sources in
  `traceability.json`. They cover the accepted spellings ` 1`, `+2` and `3 `;
  the refusals `+-3`, three spaces, a fullwidth digit, 64 digits and 2^63;
  ` 0.5abc` and `abc` number text; TimeOffset rounding; equal-Time notes; and
  CC 31 and 33.
- **F9.** MNS-003 states only n1. The candidate also expects n2 unchanged, which
  exercises REQ-003's "independently of the notes before it".
- **F10 (evidence).** Query round d4-0001 is still only in
  `/var/tmp/sound-analysis/query-spool-2/results/d4-0001/`. Its five file hashes
  match the spec appendix. REQ-014 clause 5 depends on it, so review gate 3 needs
  it retained or re-read.

## Deliverables

- Payload: [midi-note-storage-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1/README.md),
  `AGENTS.md`, `spec.md` (behavioral contract, comparison convention and
  reference obligation), `cases.json` (67 cases), `fixtures/` (67 gzip `.als`)
  and a draft `manifest.json` (`release_status: candidate-unreviewed`, review
  pending). The manifest lists 71 payload files; with itself the package has 72.
  Draft manifest SHA-256:
  `746ad0bdf5130d18d68446e1b5286898abfbba552fe033f39fefd62ce3598734`. Review
  edits will change it.
- Analyst side, never shipped: `midi-note-storage-v1-analysis/` with
  [build_mns.py](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/build_mns.py)
  (build, seal, verify, probes and mutations),
  [mns_cases.py](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/mns_cases.py)
  (carrier, F0 and F1 edits, hand-authored expectations),
  [mns_model.py](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/mns_model.py)
  (cross-check model),
  [mns_trace.py](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/mns_trace.py),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/traceability.json)
  and [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/author-validation.json).

## Evidence traceability

Evidence is the [S7 run](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/manifest.json)
(manifest SHA-256 `43a0298525e0…`; all 92 listed files matched on 2026-10-18),
`Live.arm64` `3a99ceea…d1c383cfad` (matched), the
[N1 run](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/manifest.json)
for value text, d4-0001 (F10), and one corpus record for F7 (corpus `run.json`
names the same executable hash). These locators were re-read on 2026-10-18:
`0x1028e2c80` and `0x1028e2e24` (disassembly), `0x1025c7a0c`, `0x101533e14`,
`0x101524d8c`, `0x101560424`, `0x1028e2fcc`, `0x1028e2fe4`, `0x1025c7b10`,
`0x102920db4`, `0x1028f5864` (step order), `0x1011afdac`, `0x10292b730`,
`0x10292b9ec` (early return) and n1-0006 `0x10152bfb8`. The others are the
spec author's ✓ readings. Per-case locators are in `traceability.json`; the
payload contains none of them.

| Release cases | Kept evidence | Inferred links |
| --- | --- | --- |
| MNS-001, 013 | static-survey schema segments and child orders; array loader `0x101560424`; generic writer n1-0008 `0x101486cdc` | I2 to I6 |
| MNS-005 to 012, 019, 061 to 068 | n1-0006 `0x10152bfb8` (`Invalid` by length 7, `strtod` with no-consumption throw, `(float)`, bool, int64); s7-0004 `0x101533e14`; corpus `0x101524d8c`; MNS-012 as not well-formed XML | I2 to I6 |
| MNS-002 to 004 | reset `0x1028e2fcc`; omit `0x1028e2fe4`; registration `0x1028e26c0`; array writer `0x101560258`; copy-out `0x1028e2f90` | I2, I4 to I6 |
| MNS-014 to 018 | post-load `0x1028e2c80`: Duration `fcmp`, `fccmp` DBL_MAX, `str xzr`; Velocity `fcsel`; OffVelocity and Probability `fcmlt`, `fcmgt`, `bit`, `bic` (positive zero); Time and VelocityDeviation untouched | **I1** (014 to 017), I2, I4 to I6 |
| MNS-020 to 022, 025, 069 | quantizer `0x1028e2e24` and `0x1025c7a0c`: h = `0x3e9175746e8cba40`, 3,843,840 = `0x414d538000000000`, `frintm`; examples recomputed by `mns_model.grid` | I2, I4 to I6 |
| MNS-026 to 033, 052 | `0x1028f5864` order: key map, id collection `0x1028f6154`, uniqueness throw, raise `0x102920db4`, orphans `0x1028f64d0`, per-note `0x10292c960`, zero-id pass `0x1028f6664`, groups | I2 to I6 |
| MNS-036, 070 | no sort after load; `documents.checks` overlap 261 | I4, I6 |
| MNS-039 to 051, 071 | list post-load `0x10292b730`, `0x1011afdac`, clamps `0x1011afc18` and `0x1011afc2c`, stable sort `0x1029307b8`; store post-load `0x10292cd70`; d4-0001 `0x10292b9ec` early return (first offset > 0 and last < Duration) | I2 to I7 |

| Link | Inference not established by kept evidence | Affects |
| --- | --- | --- |
| I1 | The limits run when a set is opened: gated by load-context flag `+0x2c`, inferred set for document loads (spec A1, PRB-S7-03) | MNS-014 to 017 |
| I2 | Open, then save, changes notes only by the released rules (spec A2 restated, PRB-S7-09) | Every open-save case |
| I3 | A refusal while the notes are read stops reading the document; catch site untraced. The outcome accepts a set not opened or opened without the clip | Every refused case |
| I4 | A carrier set with only the path to the clip reads the notes as a full set does | Every case |
| I5 | `strtod` is correctly rounded and the formatter prints exact binaries (accepted in the transport-state-v1 review) | Number text |
| I6 | gzip of the fixtures' form is decompressed in the standard way (als-container-v1 RVA-09) | Every case |
| I7 | `MidiKey`, `CC` and `Id` use the int parser; its converter accepts a leading `-` (CC −2, −1, −3); shipped lists carry CC −1 and −2 | Every base-list case |

## Fixture construction and sanitization

`mns_cases.py` writes every fixture from a carrier written for this release: the
declaration; the root with `MajorVersion="5" MinorVersion="12.0_12402"
SchemaChangeCount="1" Creator="Ableton Live 12.4.3"` and the invented Revision of
als-container-v1; the path `LiveSet` … `MidiClip Id="0" Time="0"`; a `Loop` of 0
to 8; and the notes element with F0 or F1 plus one edit. No shipped file is read.
The gzip form is that of als-container-v1: header `1F 8B 08 00 00000000 02 13`,
raw deflate level 9, CRC-32 and length trailer (CPython 3.13.9, zlib 1.3.1).
Element and attribute names are public document names. The payload names no
shipped file, writer version or statistic.

## Mechanical checks performed

`python3 -I build_mns.py seal` (CPython 3.13.9) wrote the author validation:

- The cross-check model agrees with all 67 expectations, outcome and saved notes.
  It shares the same static evidence and is not an oracle.
- Six mutated expectations (next id, a dropped attribute, attribute order, an
  unrounded Time, event order, an outcome) were each detected.
- Eighteen excluded or unresolved inputs got no expectation from the model: keys
  128 and −1, a repeated key, descending keys, an empty KeyTrack, a repeated
  KeyTrack Id, unsorted notes (outcome only), ` 7 `, negative NoteId and next id,
  NoteId absent from one note, Time absent, a negative-zero result, Time
  `Invalid`, `inf`, and events at 0, at the Duration and before 0.
- The 67 fixtures are distinct, single-member gzip with the stated header, UTF-8
  with LF endings and a final newline.
- Hashes and sizes of the 71 listed files match. The inventory equals the
  directory, all case inputs exist, and there are no symlinks. Two consecutive
  builds produced the same manifest digest.
- The deny list covers addresses and offsets, internal class and function names,
  recovered messages, tool names, analyst paths, probe, question, assumption and
  packet IDs, fragment and base names, shipped-content names, writer versions and
  the Q-018 mechanism terms. Its only hit is "decompil" in the forbidden-inputs
  list of `AGENTS.md`, worded as in the released packages.
- In the export copy
  `/tmp/claude-1000/-home-ollie-Documents-sound/5c433942-c5e3-420d-833a-756602393383/scratchpad/export-mns/midi-note-storage-v1/`,
  `verify` matched all 71 hashes and resolved all 9 Markdown links inside the
  package. `sha256sum -c` against the manifest also passed, and the copy is
  byte-identical to staging.

Not checked: any reference or candidate execution, and any proof of I1 to I7.

## Review gates still required

1. **Scope review**, in a separate context. Check every included clause and all
   67 expectations against the locators. Rule on I1 to I7, the open-save action in
   place of the draft's clip-file procedure, the disjunctive `refused` outcome,
   the 12 new cases, F2 to F7 and the narrowing of MNS-036.
2. **Quality and sanitization review**: behavioral completeness, the comparison
   convention and reference obligation, and exclusions that agree between spec
   and manifest. Confirm that no Q-018 input has an expectation, that the
   payload holds no internal structure or analyst link, and that nothing claims
   more than static derivation.
3. **Evidence identity**: the S7 manifest, its 92 files and the image hash
   matched on 2026-10-18. Retain or re-read d4-0001 (F10) and the corpus record
   for `0x101524d8c`.
4. **Fixture and sharing review** of the 67 authored Live Sets, including the
   product name in `Creator` and the invented Revision.
5. **Finalize**: add `REVIEW.md`, set the manifest review fields,
   `release_status` and `release_date`, re-run `seal`, verify an isolated
   export, and record the manifest hash in the handoff catalog.
6. **Publish** only after approval. Copy the package unchanged to
   `handoff/midi-note-storage-v1/`. Then update the catalog, spec status and
   revision note, coverage, the specs index (which has no entry for this page
   yet), Q-018 and the log.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate: 67 cases for partial
REQ-MIDI-NOTE-STORAGE-001 to 010, 013, 014 and 016. REQ-011 is excluded and 012,
015 and 017 are unreleased. It is not published, and no handoff exists for
SPEC-MIDI-NOTE-STORAGE.
