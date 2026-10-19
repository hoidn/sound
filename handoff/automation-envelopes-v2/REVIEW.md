# Review disposition

Release: automation-envelopes-v2, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this
candidate and will not implement it. The one reviewer performed the scope and
evidence, supersession, fixture-validity, quality and sanitization,
evidence-identity and packaging checks. Publication metadata outside this
package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of
REQ-AUTOMATION-ENVELOPES-001 to 003, 005 to 009 and 012 in
[the contract](spec.md), corrected as listed below.
REQ-AUTOMATION-ENVELOPES-004, 010, 011 and 013 remain unreleased.

- **The discard on open.** The candidate withdrew automation-envelopes-v1
  cases 003, 004 and 011 because opening might discard an envelope with fewer
  than two events before the checks of REQ-AUTOMATION-ENVELOPES-007. Its
  author had read this in one build only and called it unconfirmed. The
  reviewer re-derived it from the static evidence of both the arm64 and the
  x86_64 build of 12.4.3, independently of the author's reading.
  - Every opened Live Set runs the discard, before the checks.
  - It discards a clip envelope that holds exactly one event.
  - It discards a track envelope that holds no event or one event. Some
    parameter kinds can be exempt from this; the audio track's `Speaker`,
    `Pan` and `CrossFadeState` are not.
  - The event count it uses is the number of events in the list.

  The discard is therefore confirmed for this release's targets, and the three
  v1 expectations were wrong (RA2-01). The author's further reading also holds:
  a clip envelope with no event is kept and then refused (RA2-02).
- **Fixture validity.** The Live Set structure checker was run on every
  fixture, by its own command line on a copy holding only this release. It
  found 21 Live Sets, none refused, no unknown shape and no case contradicted
  or failing to isolate its rule. Its schema check found no deviation in any
  fixture. For each of the seven refused fixtures (008, 012 to 015, 030 and
  031), the reviewer wrote a control repairing only the tested defect. Six
  controls change one attribute; 012's adds two events. Every control passes
  the structure checker and opens under the reviewer's restatement. So each
  refused fixture fails only for the reason its case tests. The three withdrawn
  v1 inputs pass the checker once completed with its own structural additions.
  Under this release's clauses they open (RA2-05).
- **Expectations.** The reviewer restated the contract from `spec.md` alone,
  without the author's model, and evaluated every case with it. The
  restatement agrees with all 21 outcomes and every saved attribute text. This
  covers each released requirement:
  - storage and shape: 001, 010 and 032;
  - binding by Id: 021;
  - value kinds: 014, 015 and 021;
  - the one-event list at L: 002;
  - a later negative time: 009;
  - every load check: 005 to 008, 012, 030 and 031;
  - curve controls: 017 to 020;
  - number text on open and save: 006, 007, 013 to 016 and 018.

  Under v1's reading, without the discard, all 21 outcomes stay the same. Only
  case 012 would change if a clip envelope with no event were also discarded;
  the evidence rules that reading out (RA2-07).
- **Weakest cases.** 012 rests on the clip discard's exact count (RA2-02).
  Cases 030 and 031 are new and replace 003 and 011 within the narrowed clause
  2. Case 032 rests on stated assumption 3; shipped Live Sets of this format
  version hold empty arrangement clip timelines. All are accepted.
- **No value cases.** No case, comparison field or representation carries the
  value an envelope supplies at a time or while the transport plays. Such
  wording appears only in the exclusions and in the reason that
  REQ-AUTOMATION-ENVELOPES-010 and 011 stay unreleased (RA2-06).
- **Supersession.** The superseded manifest digest equals the catalog value,
  and every file automation-envelopes-v1 lists still matches. The 18 carried
  case records are identical to v1's. Each carried fixture is the v1 file with
  exactly 40 lines inserted and nothing else changed (RA2-08). The change list
  was incomplete; it now matches the text differences (RA2-04).
- **Sanitization.** The reviewer scanned every payload file with a deny list
  wider than the author's. No source code, recovered program text or
  messages, internal identifiers, addresses, analyst paths, private evidence
  links, planning identifiers or per-case evidence fields are present. The
  remaining hits are neutral: "recovered" in the forbidden-inputs list of
  `AGENTS.md`, and "dangling" in the README's scope statement.
- **Packaging.** Exclusions in the contract and the manifest agree. Every
  expectation is labeled static-derived, reference and candidate execution
  have not run, and no compatibility is claimed. In a copy outside the analyst
  checkout, every Markdown link and case input resolves inside the package,
  and every listed hash and size matches. The 21 fixtures are distinct, ASCII
  with LF endings and a final newline. They were authored for these cases and
  contain no shipped content.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RA2-01 | High | The discard of envelopes with fewer than two events is established for this release's targets, not merely possible. automation-envelopes-v1 cases 003, 004 and 011 expected refusals that do not occur, and its REQ-AUTOMATION-ENVELOPES-007 clauses 1 and 2 were wrong for such envelopes. The candidate called the refusal "not established", left the inputs without expectation and excluded whether such an envelope is kept. | Corrected. README change 2 and the manifest now state that the three cases were wrong, not only badly fixtured. REQ-AUTOMATION-ENVELOPES-007 clause 5 now states the discard. REQ-AUTOMATION-ENVELOPES-005 now says the one-event envelope is discarded. The input exclusion for these envelopes was removed. "Whether opening keeps an envelope" became "what a save writes for a discarded envelope". No case was added or changed. |
| RA2-02 | Medium | Case 012 (empty clip envelope refused) holds only if the clip discard counts exactly one event, not at most one. The author had this from one build. | Confirmed in both builds; upheld. The case also rests on assumption 5 (RA2-03). |
| RA2-03 | Medium | The discard also removes an envelope whose target does not belong to its device. That test was not evaluated for the mixer and MIDI controller targets. Cases 001, 008, 012, 016 to 021, 030 and 031 need their envelopes kept. automation-envelopes-v1 relied on this without stating it. | Stated as assumption 5 in the contract and the manifest, with its dependent cases; README change 11 records it. An implementation keeps these envelopes. The parameters are the track's own mixer and controller targets, so the assumption is accepted. |
| RA2-04 | Low | The change list omitted several changes: the new input exclusions (Live Set structure other than the fixtures', and the save-logarithm band), stated assumptions 3 and 4, and the removed one-event exclusion. Its "unchanged" item also claimed every v1 exclusion was carried. | Completed: README change 11 added, change 12 corrected, manifest changes aligned. No expectation changed. |
| RA2-05 | Info | Fixture validity (structure checker; single-defect controls). | All 21 fixtures pass. Each refused fixture fails only for its tested rule. |
| RA2-06 | Info | Value expectations. | None released or implied. |
| RA2-07 | Info | Independent restatement. | Agrees with all 21 expectations and saved texts. |
| RA2-08 | Info | Supersession. | Digest, carried records and carried fixtures verified. |
| RA2-09 | Info | Evidence identity. | The pinned arm64 and x86_64 images, the schema file and every file of the evidence runs relied on were re-hashed on 2026-10-18. All matched the recorded digests. |
| RA2-10 | Editorial | Payload status lines described an unreviewed candidate. The fixture provenance cited README change 1 for the template insertions, which are change 3. | Status set to reviewed local release, this record added and linked, cross-reference corrected, manifest review fields filled and inventory re-hashed. |
| RA2-11 | Info | Clause 5 of REQ-AUTOMATION-ENVELOPES-007 has one case (002), which opens with or without the discard. | A later revision should add opening cases for a `Pan` envelope with one event at 4, a `Pan` envelope with no event and a clip envelope with one event at 4, and should extend the comparison obligation to them. No expectation was invented here. |

Two inferences behind RA2-01 are accepted. First, the mixer's `Pan`,
`Speaker` and `CrossFadeState` are of the format's plain float, Boolean and
enumeration parameter kinds, as the format declares them. Second, the setting
that enables the discard keeps the value it receives at application start: no
other change to it was found.

## Disposition

**Approved with listed corrections** (RA2-01, RA2-03 and RA2-04), only for the
explicit partial clauses in the contract. All expected outcomes remain
static-derived. Neither reference nor candidate application cases have run,
and no compatibility pass is claimed. Candidate-only checks cannot replace
independent reference observations. An isolated implementation workspace
remains a prerequisite.

The parent specification's REQ-AUTOMATION-ENVELOPES-005 and 007 still describe
the discard as open. The analyst must align them with this release.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
