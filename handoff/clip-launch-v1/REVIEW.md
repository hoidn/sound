# Review disposition

Release: clip-launch-v1, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the coordinator
in its own handoff-review context. It did not author this candidate and will
not implement it. The one reviewer performed the scope and evidence, quality
and sanitization, evidence-identity and fixture-sharing checks. Publication
metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-CLIP-LAUNCH-001 to
007, 009 and 011 to 014 in [the contract](spec.md), narrowed as listed below.
REQ-CLIP-LAUNCH-008, 010 and 015 to 023 remain unreleased.

- Every included clause was checked against the reviewed static evidence for
  the pinned 12.4.3 build. The reviewer re-derived the item names, nesting,
  order and value types against the shipped `12.0_12402` and `11.0_405`
  schemas and the program's own item lists; the four label lists; the initial
  clip and follow-action values; the text rules, which follow the same reading
  path as the released transport-state rules; refusal of a repeated child; each
  binary32 operation and the halves-away rounding of the chance rescaling; the
  follow-time rounding sequence; and the four conversion steps, including every
  comparison and every default value of step 12203. The author's cross-check
  was not relied on.
- All 50 cases were read one by one. Every fixture was compared with the
  template, and each differs from it only as its purpose states. The reviewer's
  own executable restatement of the narrowed contract, written from the evidence
  and not from the author's model, agreed with all 50 expected results and with
  the worked examples in REQ-012, 013 and 014.
- The reviewer listed every conversion step numbered above 405 that applies to
  clip, follow-action, scene, track or song elements. Apart from the four named
  steps, none changes a launch element, a follow-action item,
  `GlobalQuantisation` or `AutoQuantisation` (RVC-04).
- Sanitization was checked by the reviewer's own scan of every payload file. No
  source code, recovered program text or messages, internal identifiers or
  addresses, analyst paths, private evidence links, planning, probe, question or
  assumption identifiers or per-case evidence fields are present. The only
  flagged word is in the forbidden-inputs list of `AGENTS.md`, worded as in the
  released packages. The conversion-step numbers are format-version thresholds
  on the scale of the MinorVersion suffix number and are stated as behavior. The
  three MinorVersion values are document data, as in the earlier releases.
- The 50 fixtures are distinct, well-formed XML, ASCII with LF endings and a
  final newline, without tabs. They were authored from a template written for
  this release. `Id` and `Time` values are invented. No fixture contains shipped
  file content, and all are suitable for sharing.
- Exclusions appear in both the contract and the manifest and now agree
  (RVC-06). Every expectation is labeled static-derived, with reference and
  candidate execution not run. No compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists and every listed hash and size matches.

## Rulings on the points raised for this review

1. **Launch path and launch timing.** No released clause or case rests on
   either. Launching, REQ-016 to 023 and missing or out-of-range set
   quantization stay unreleased or excluded. The clip-to-global correspondence
   in REQ-005 rests on the label lists, in which clip value k and global value
   k − 1 carry the same label. Its wording no longer says how a launch uses the
   setting (RVC-05). REQ-015 is removed (point 5).
2. **Message prefixes for out-of-range values.** The parent draft graded two
   message prefixes, given when the scripting interface is assigned an
   out-of-range launch mode or launch quantization. The program builds a
   message with that text, but the kept evidence does not show what text a
   script receives, and the draft's own scope excludes message text. The
   prefixes are therefore not established as observable. This package carries
   none of them and excludes the scripting interface. REQ-011 keeps only the
   opening of a document (RVC-10).
3. **Saved number text.** No case grades saved text. REQ-001 clause 6 claimed
   exact read-back for every written value. It now covers only Booleans and
   numbers of at most six significant digits (RVC-02). Every graded saved
   value is of that kind. CLIP-LAUNCH-038 and 040, whose follow times need more
   digits, are graded only as values held after opening.
4. **Chances outside 0 to 100.** No case uses a chance outside 0 to 100, or any
   other value outside the precondition ranges, except the three REQ-011
   cases, which grade only that the document opens. Unchecked storage on
   opening is established for list values, not for bounded binary32 values.
   The assumption sentence that could be read as covering them is narrowed
   (RVC-03).
5. **REQ-015.** Removed. It is static-supported, but a grid length is
   observable only through launching, which this release excludes and which is
   still open. The parent draft's acceptance cases for it are all launch-timing
   cases. Unlike the definitional time-signature code clause of
   transport-state-v1, no stored value in this release exercises it. It may
   return with those cases in a later release (RVC-01).

Other rulings: the scene cases CLIP-LAUNCH-046 to 050 stay graded as values
held after opening, while the saved scene form stays excluded (RVC-08). The
authored `11.0_405` fixtures are accepted. The comparison obligation already
requires an authentic set of that version (RVC-13).

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVC-01 | Medium | REQ-015 defined the grid length of each quantization value. It had no case and no observable outside launching, which is excluded and open. | Removed from the release; REQ-015 is unreleased in the contract, README and manifest. The contract's scope now names the grid length among the excluded launch behavior. No case is affected. |
| RVC-02 | Low | REQ-001 clause 6 said that any written value reads back as the value held. The written number text is not established, so read-back is shown only for short values. | Narrowed to Booleans and to numbers of at most six significant digits. Read-back of longer numbers is excluded in the contract and the manifest, and the comparison section says that only such values are listed. No case is affected. |
| RVC-03 | Low | The first assumption sentence said that a present value is "kept as read, without adjustment to a range". That suggested unchecked storage of out-of-range binary32 values, which is not established. | Narrowed to values inside the precondition ranges. Out-of-range values keep no expectation. No case is affected. |
| RVC-04 | Low | REQ-014 clause 2 read as a complete list of the conversion steps an older document passes through. Other steps apply to `11.0_405` and `12.0_12117` documents. | Reworded to "of these steps" and stated that the other steps are excluded and change no item of this release. The reviewer checked the second statement against every relevant step. No expectation changed. |
| RVC-05 | Low | REQ-005 said that clip value 0 means the clip "uses" the global setting, which describes launching. | Reworded as meaning: clip value k denotes the setting of global value k − 1, with the same label, and value 0 denotes the global setting. The use at launch is excluded. |
| RVC-06 | Editorial | The contract and the manifest listed different exclusions. | Aligned: item shape for every item of the table, non-finite values and negative zero, more than one clip at a named location, a `11.0_405` clip with a direct `FollowActionEnabled` or `IsLinked` child, loop iterations and jump indices at launch, documents older than `11.0_405` and the key and MIDI assignment of the global quantization. |
| RVC-07 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record was added and linked. The manifest review and status fields were filled and the inventory was re-hashed by the reviewer. |
| RVC-08 | Info | The author had checked the scene step 12203 only at a higher level and asked for a closer check. | The reviewer's own static check of the pinned build confirmed every condition and all ten default values. The scene cases stay graded. |
| RVC-09 | Info | Follow-time rounding. | Re-checked in the pinned build. It gives the nearest multiple of 1/3,843,840, with halves away from zero. Values near a half-multiple stay excluded. |
| RVC-10 | Info | REQ-011 message prefixes of the parent draft. | Not carried, as ruled above. |
| RVC-11 | Info | Assumptions. | Accepted as stated in the contract. Clips and follow actions are read in the same way as the released transport-state values, which keeps a present list value as read, without a range check. For bounded binary32 values this is not established (RVC-03). That an absent item keeps its initial value, that the corrections run for every clip, the conversion order and the kept chance values remain stated assumptions. The comparison obligation covers them. |
| RVC-12 | Info | Evidence identity. | The pinned program image, the evidence run's manifest and all 87 files it lists were re-hashed on 2026-10-18. All matched the recorded digests. |
| RVC-13 | Info | Remaining author findings and coverage. | A clip that has both follow-action forms stays excluded: whether opening refuses it or the application stops is not established. Whether the opening corrections apply to scenes is not graded, since scene chances of 100 and 0 are unchanged either way. No case exercises the homonym clause of REQ-001, integer text with trailing spaces or Boolean text `0`; cases are proposed for a later revision. The evidence would also support refusing a repeated follow-action child, which stays excluded. No expectation was invented. |

## Corrections for the parent draft

These do not change this package. The draft specification should be revised
to:

- remove the graded message prefixes from REQ-011, or mark them unknown, in
  line with its own exclusion of message text;
- grade the saved follow time 11,531,521 ÷ 3,843,840 as a value held after
  opening, not as exact read-back of saved text;
- remove or mark unknown the chance example 150 and 50, which lies outside
  the chance bounds;
- mark unknown the outcome for a clip that has both follow-action forms;
- state that other conversion steps exist and are outside the requirement;
- drop the proposal to release the launch-grid requirements and REQ-015 while
  the launch path stays open.

## Disposition

**Approved with listed narrowing** (RVC-01 to RVC-05), only for the explicit
partial clauses in the contract. All expected results remain static-derived.
Neither reference nor candidate application cases have run, and no
compatibility pass is claimed. Candidate-only checks cannot replace
independent reference observations. An isolated implementation workspace
remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
