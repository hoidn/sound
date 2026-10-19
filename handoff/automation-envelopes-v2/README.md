# Automation envelopes in Live Set documents, release 2

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, narrowed and clarified as recorded in the review, is
approved as a contract for a fresh, restricted implementation workspace. Such
a workspace has not been provisioned by this release.

The finite scope is how the decoded XML of one Live Set format version stores
track and clip automation envelopes: where envelopes are stored and how each
names its parameter, the event elements and their value kinds, the envelopes
that make a document refused when it is opened, how curve controls are kept and
written, and the text read and written for event numbers. Requirement IDs are
retained with explicit partial clauses. Requirements 004 (event Ids), 010 and
011 (the value an envelope supplies at a time) and 013 (editing, override,
recording, undo and the precedence of a parameter's own value over its
envelope) are not released. Envelope values at any time, clip envelope timing
and malformed or dangling envelopes have no expectation. No application source,
shipped file or public dependency is included.

The 21 cases use independently authored minimal XML fixtures. All expected
results are static-derived and unexecuted. They are not captured reference
behavior. The representation is a comparison convention, not an API claimed to
exist in Live and not a required architecture. No compatibility claim is made.
Preserve this release unchanged; corrections require a new revision.

## Supersession

This release supersedes automation-envelopes-v1, which stays immutable. Its
fixtures must not be used to judge that a document opens (change 1), and its
cases 003, 004 and 011 were wrong (change 2).
18 of its 21 case records are carried unchanged with corrected fixtures, and
3 cases are new, for 21 in total. [The manifest](manifest.json) records the
relationship, the superseded manifest digest and the fixture changes.

## Changes from automation-envelopes-v1

1. **Defect corrected: the fixtures could not open.** A Live Set is not opened
   when an audio or MIDI track holds a different number of freeze clip slots
   from session clip slots (static-derived). Every automation-envelopes-v1
   fixture has one session clip slot on its MIDI track and no freeze clip slot,
   so its 13 cases that expect a document to open could not hold, and its 8
   refused cases were also refused for that reason. automation-envelopes-v1
   stated that missing set content must not by itself change a judged outcome;
   for the freeze clip slots that was wrong.
2. **Defect corrected: cases 003, 004 and 011 were wrong.** Each expected a
   refusal for an envelope with fewer than two events: a `Pan` track envelope
   whose only event is at 4, a `Pan` track envelope with no event, and a clip
   envelope whose only event is at 4. Opening a document discards each of these
   envelopes before the checks of REQ-AUTOMATION-ENVELOPES-007 apply
   (REQ-AUTOMATION-ENVELOPES-007 clause 5, static-derived). The checks never see
   the envelope and do not refuse the document because of it. The expected
   refusals were therefore wrong, not only badly fixtured. An implementation
   must not refuse these documents because of that envelope.
   automation-envelopes-v1's REQ-AUTOMATION-ENVELOPES-007 clauses 1 and 2 were
   wrong for such envelopes. Clause 1 now covers clip envelopes only, and
   clause 2 envelopes with at least two events. The three cases are withdrawn,
   not carried with new fixtures, and `AUTOMATION-ENVELOPES-003.xml`, `004.xml`
   and `011.xml` are dropped. Only case 002 has a discarded envelope, and it
   opens with or without the discard.
3. **Fixture change, the 18 carried fixtures.** Each of
   `fixtures/AUTOMATION-ENVELOPES-001.xml`, `002.xml`, `005.xml` to `010.xml` and
   `012.xml` to `021.xml` is the automation-envelopes-v1 file of the same name
   with 40 lines inserted:
   - after the audio track's `</Mixer>` line, a `MainSequencer` and a
     `FreezeSequencer`, each holding one empty clip slot (20 lines);
   - after the MIDI track's `</MainSequencer>` line, a `FreezeSequencer` holding
     one empty clip slot (10 lines);
   - after the `</Tracks>` line, `Scenes` with one scene (10 lines).

   The clip slot and scene forms are those of
   [fixture provenance](spec.md#fixture-provenance). Each track now has one
   session and one freeze clip slot, and the set one scene per session clip
   slot. No line of an automation-envelopes-v1 fixture is changed, removed or
   reordered. The fixtures remain ASCII with LF endings.
4. **Expectations re-checked; none changed.** The inserted elements lie outside
   every judged path and name no envelope target. Each carried case keeps its
   record, outcome and saved texts. Each refused fixture differs from a document
   that opens only in the tested envelope.
5. **New cases 030 and 031.** They test the first-event time check with two
   events whose first is at 4, on a track envelope and on a clip envelope. They
   replace cases 003 and 011 within the narrowed clause. IDs 022 to 029 were
   withdrawn before automation-envelopes-v1 was released and are not reused.
6. **New clause and case 032.** REQ-AUTOMATION-ENVELOPES-001 clause 5 and
   REQ-AUTOMATION-ENVELOPES-007 clause 4: an empty `Events` list in the MIDI
   track's arrangement clip timeline does not make the document refused. This
   rests on stated assumption 3. The exclusion of elements that share the
   `Events` shape is narrowed accordingly.
7. **Save rule corrected (REQ-AUTOMATION-ENVELOPES-012 rule 7).** k now comes
   from the binary64 base-10 logarithm, as in transport-state-v2. The two rules
   differ only for binary64 `Time` and curve-control values just above a power
   of ten 10ⁿ or just below 10⁻ⁿ (n ≥ 1). automation-envelopes-v1 stated the
   exact-logarithm rule without excluding those values; no case of it lies
   there. The band where the logarithm's last bit is not established has no
   expectation (stated assumption 4).
8. **Assumption settled.** That opening a Live Set applies the checks of
   REQ-AUTOMATION-ENVELOPES-007 is now static-derived and is no longer a stated
   assumption.
9. **REQ-AUTOMATION-ENVELOPES-005 restated.** A document whose track envelope
   holds a single event, at L, still opens. Opening discards that envelope
   (change 2). What a later save writes for it is excluded behavior.
10. **Parent revision.** The parent is SPEC-AUTOMATION-ENVELOPES revision 4.
    Its value clauses (REQ-AUTOMATION-ENVELOPES-010 and 011) stay unreleased,
    for the reason stated in [the exclusions](spec.md#exclusions-and-deferred-obligations).
11. **Exclusions and assumptions.** New inputs without expectation: Live Set
    structure other than the fixtures' (other tracks, devices, scenes, clips and
    clip slots, main and cue tracks, sends and returns), and saved values in the
    band of change 7. Narrowed exclusion: elements that share the `Events` shape
    (change 6). New stated assumptions: 3 (change 6), 4 (change 7) and 5, that
    opening discards no envelope of the fixtures other than those of change 2.
    Cases 001, 008, 012, 016 to 021, 030 and 031 depend on assumption 5;
    automation-envelopes-v1 relied on it without stating it. New excluded
    behavior: what a save writes for a discarded envelope.
12. **Unchanged.** Every other clause, case record, expectation and provenance
    label of automation-envelopes-v1 is carried unchanged.
