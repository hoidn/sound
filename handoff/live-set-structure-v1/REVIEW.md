# Review disposition

Release: live-set-structure-v1, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope and evidence,
fixture-validity, quality and sanitization, cross-release, evidence-identity
and fixture-sharing checks. Publication metadata outside this package is left
to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-LIVE-SET-STRUCTURE-001
to 010, 013 to 016 and 018 in [the contract](spec.md).
REQ-LIVE-SET-STRUCTURE-011, 012 and 017 remain unreleased.

- Expectations. The reviewer's own executable restatement of the contract,
  written without the author's tools, agrees with all 34 expected outputs: the
  outcome of the 33 cases whose action opens a set, every judged state key, and
  the four identity values of the computed case. At least one expectation per released
  requirement, and every case whose basis looked weakest, was re-derived from
  the static evidence: the track-list, slot-count and send-holder checks, the
  target Id and `NextPointeeId` checks, the list-item Id checks, the removal of
  envelopes without a target, the added send's value, the new main track's
  tempo and the sample-path fallback. The checksum was recomputed from the
  fixture sample and agrees with the retained result of the original's own
  routine on the same bytes. The author's cross-check was not relied on.
- Opening always runs the structural checks. The reviewer re-read the static
  evidence for every traced way of opening a set (opening for the user, from
  the command line and on restore). Each reads a gzip XML document through the
  same reader, and that reader's load step runs the members' checks, the set's
  own check and then the check of every track and the track list, with no
  branch that skips them. The retained records match their sources. A track's
  freeze slots exist from construction with no slots, and the reviewer's own
  scan of every document class found no check that runs on the freeze slots
  before the slot-count comparison, and no step reached from the set, track,
  device-chain or sequencer read steps that adds slots. The remaining
  inference is the one already stated: that no indirect call outside the
  enumerated ones adds slots while a set is read, and that menu and system open
  events use the traced entries.
- Fixture validity. The analysts' structural checker for Live Sets was run
  unchanged on an exported copy of every set fixture. Each fixture that is
  expected to open passes it: no structural refusal and no shape without an
  outcome. Each refused fixture fails it only for its tested reason, or, where
  that reason is a shape the checker does not evaluate (a repeated member, a
  value element without `Value`, a lettered Id, a grouped track, an unknown
  track kind), passes everything else. The checker cannot read the
  value-less `NextPointeeId` of case 014; that fixture was measured again with
  the value restored and shows nothing else. The checker's one note on a
  refused fixture, for case 005, compares the `SendPreBool` count with the
  return tracks at the end of the track list, of which there are none there;
  the count equals the number of return tracks, as the contract requires, and
  no check of it on opening was found. The reviewer's restatement finds
  exactly one broken rule in each of the 18 refused fixtures, the tested one,
  and none in T11-MIN or in any fixture that opens. Each variant differs from
  T11-MIN only by its stated change. No fixture falls under an exclusion.
- Refusal isolation of the corrected draft cases. The return-before-audio case
  (005) empties every send list, so the send-holder rule is not broken first;
  its one `SendPreBool` equals the number of return tracks, as the contract
  requires. The two track-list cases (002, 003) remove the `SendPreBool` with
  the tracks. The freeze-slot case (018) removes a freeze slot and keeps one
  session slot per scene. Each fails only for its tested rule.
- Cross-release. T11-MIN's envelopes, notes, launch settings, warp markers and
  transport values were checked against the refusal rules of the released
  contracts for those fields. None applies.
- Sanitization was checked by the reviewer's own scan of every payload file and
  decoded fixture. No source code, recovered program text, internal
  identifiers, addresses, analyst paths, private evidence links, planning or
  question identifiers or per-case evidence fields are present. The flagged
  words are document element names, one word of the forbidden-inputs list in
  [the role instructions](AGENTS.md), "x86_64" in the provenance of the
  extracted-execution label, and "probe" in the comparison obligation.
- Scope. No runtime, timing, display or audio result is released. No
  expectation depends on an open question. Exclusions appear in both the
  contract and the manifest and agree. Reference and candidate execution have
  not run, and no compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists, and every listed hash and size
  matches. The 31 set fixtures are distinct, have the stated gzip header, one
  member, a valid trailer and nothing after it, and decode to ASCII XML with
  LF endings. The reading copy equals the decoded T11-MIN. The sample is a
  generated tone. No fixture contains shipped file content.

## Scope rulings

- Device placement. The candidate's T11-MIN placed an instrument directly in
  the MIDI track's device list and an effect directly in the audio track's.
  Whether a track's device list accepts those devices is open, and 15 cases
  that expect a set to open rested on it, although none judges a device. The
  devices are removed from T11-MIN, and so from every fixture. An empty device
  list on a MIDI or audio track is a form of the shipped sets, so no case rests
  on device placement any more. The two removed devices held the targets with
  Ids 67 and 68: `NextPointeeId` is now 67, case 025 uses 66, the largest
  target Id, and the holder added in case 022 has targets 67 and 68 with
  `NextPointeeId` 69. No other expectation changed. Devices remain excluded
  with REQ-LIVE-SET-STRUCTURE-012.
- The `list-item-ids` assumption (cases 009 to 011) and the `sample-folder`
  assumption (case 031) are accepted as stated, behaviorally named
  assumptions. Each rests on documented forms and static evidence and is not
  contradicted. If either fails, the cases that name it have no expectation.
- A missing sample (case 032) does not refuse the set: static-derived on the
  traced resolution path, which raises no error. That nothing else in opening
  depends on the file is accepted as an inference.
- The new main track's tempo (case 015) and the added send's value (case 021)
  are derived here from how the set creates them when it is opened. They do
  not rest on clauses that other releases leave unreleased. The value text of
  the added send follows the released mixer text rule.
- The element status table of REQ-LIVE-SET-STRUCTURE-018 cites only this
  contract's clauses. Elements whose absence another contract governs, or for
  which no rule is released, are marked Write.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RV1-01 | Medium | Fifteen cases that expect a set to open rested on the open question of where devices may be placed, through the two devices of T11-MIN. | Narrowed: both devices removed from T11-MIN and every variant, with the target Id changes listed under scope rulings. The `device-placement` assumption is withdrawn from the contract, cases and manifest; any device in a device list now has no expectation. |
| RV1-02 | Low | REQ-001 refused a set when "an element that is not a list" holds two children of one name. T11-MIN's `KeyTrack/Notes` is an array holding two `MidiNoteEvent` items, so the clause as written refused T11-MIN. | Corrected: arrays are a fourth element form and a defined term; the repeated-child refusal applies to compound elements only. No case changed. |
| RV1-03 | Low | REQ-009 clause 2 stated for the codes 2, 3, 5, 6 and 7 whether `Path` is used. No case judges them, and resolution steps outside this release (library relocation, the missing-file search) can apply to some of them. | Narrowed to the codes 0 and 1; the codes 2 to 7 have no expectation, in REQ-008 clause 2, REQ-009 clause 2, the exclusions and the manifest. No case affected. |
| RV1-04 | Low | The element status table required "at least one `MidiTrack` or `AudioTrack`". The derived rule refuses a set with no audio, MIDI or group track. | Restated in those words in the table, REQ-002 clause 2 and the manifest scope. No case affected. |
| RV1-05 | Low | `send_texts` and `automated_parameters` are keyed by track number, and the cases list one track. "Compares exactly" could be read as judging the whole map. | Clarified: only the track numbers a case lists are judged. No expectation changed. |
| RV1-06 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release; this record added and linked; manifest review and status fields filled and inventory re-hashed. |
| RV1-07 | Info | Opening always runs the structural checks, and freeze slots are not added while a set is read. | Confirmed on the static evidence, with the remaining inference stated above. |
| RV1-08 | Info | Fixture validity. | Every fixture that should open passes the structural checker; each refused fixture fails only for its tested reason. |

## Disposition

**Approved with listed narrowing** (RV1-01 and RV1-03) and corrections
(RV1-02, RV1-04 and RV1-05), only for the explicit partial clauses in the
contract. The package has 34 cases: 18 refusals, 9 positive, 3
missing-element, 3 repair and 1 computed. Expected results are documented,
static-derived or, for one checksum, extracted execution, as labeled per case.
Extracted execution ran the original program's x86_64 checksum routine on a
Linux host; the arm64 build is inferred to give the same result. Neither
reference nor candidate application cases have run, and no compatibility pass
is claimed. Candidate-only checks cannot replace independent reference
observations. An isolated implementation workspace remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
