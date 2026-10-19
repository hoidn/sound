---
id: PLAN-TRANSPORT-STATE-V3-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Third transport-state handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [transport-state-v3](../../handoff/transport-state-v3/README.md), approved with listed clarifications RV3-01 and RV3-02 by a separate review agent ([review record](../../handoff/transport-state-v3/REVIEW.md)).

- **Fixtures:** all 33 cases are carried with records identical to v2. Every fixture passes the structure checker, and the 10 refusal fixtures fail only for the text each one tests.
- **The added MIDI track:** it changes no expectation, because it holds none of the value paths.
- **RV3-01:** the rule reads "no audio, MIDI or group track".
- **RV3-02:** v2's fixtures judge no case.

For the spec owner: the cases still describe their fixtures as edits of B0, and the handoff section must name v3. New REQ-012 evidence: on open, a tempo Manual value that disagrees with its automation envelope is replaced by the envelope's value.

## Decision and boundary

Stage a corrective candidate, transport-state-v3, from
[SPEC-TRANSPORT-STATE revision 4](transport-state.md). It follows the
[transport-state-v2 plan](transport-state-v2-handoff-plan.md), the
[midi-config-v3 plan](midi-config-v3-handoff-plan.md) (a superseding release), the
[als-container plan](als-container-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff).

Why a new release: the released [transport-state-v2](../../handoff/transport-state-v2/README.md)
fixtures have no track. [SPEC-LIVE-SET-STRUCTURE](live-set-structure.md) REQ-002 (S;
A1 settled) derives that opening a Live Set always runs a validation walk, and that
the walk refuses a set whose `Tracks` holds no player track. The
[audit](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/released-fixture-audit.json)
finds all 33 v2 fixtures refused for that reason. The 23 cases that expect a set to
open are contradicted, and the 10 refused cases no longer isolate their tested
text. The [handoff catalog](../../handoff/index.md) records the defect. Released
payloads are immutable, so v3 carries every v2 clause, case ID and case record
unchanged and changes only the fixtures. Each gets the minimal addition the audit
lists for it.

Revision 4 settles no clause beyond v2. Its only changes (band, A-LOG, glibc
dependence) are the v2 review clarifications RV2-02 and RV2-03, which the v2 payload
already carries. So no clause or case is added.

Provenance labels are unchanged: 18 static-derived, 15 extracted execution. Opening
and saving stay static-derived, now also resting on SPEC-LIVE-SET-STRUCTURE's S rules
for the added track. No reference application or candidate has run, and no
compatibility is claimed.

This page is the analyst-side plan and traceability record, not an implementation
input. The candidate is **unreviewed and unpublished**. Nothing has been written into
`handoff/`.

## Scope

The selection is the same as v2's, from revision 4.

| Requirement | Included in v3 | Excluded remainder |
| --- | --- | --- |
| 001 to 008, 010, 011 | The v2 partial clauses, verbatim | As in v2 |
| 009, 012 | None | All |

The exclusions are v2's, plus one new input without expectation: a `Tracks` element
that is absent or holds no `AudioTrack` or `MidiTrack`, and track content other than
the fixtures' one MIDI track. The track rules belong to SPEC-LIVE-SET-STRUCTURE,
which has no release.

The v2 review proposed two follow-ups, but revision 4 adopts neither, so v3 leaves
both out:
- RV2-07: narrow the half-gap band;
- RV2-08: cases for `#` text of other lengths and for `1e`.

### Case disposition

| Cases | Disposition | Fixture change |
| --- | --- | --- |
| TS-001 to 003, 006, 008, 011 to 014, 016, 020 to 022, 024 to 028, 030, 032, 034, 036, 037 (23, opens) | Records identical to v2 | v2 file plus the track list; v2 refused it (REQ-002), v3 opens under the traced rules |
| TS-004, 005, 007, 009, 010, 015, 029, 031, 033, 035 (10, refused) | Records identical to v2 | Same addition. The only structural refusal is gone, so each now fails only for its tested text |
| TS-017 to 019, TS-023 | Not released | As in v2 |

The addition is identical for every fixture. It is the audit's T11-MIN `MidiTrack`
skeleton:
- `MidiTrack Id="1"`, `EffectiveName` `1-MIDI`, empty `UserName`;
- `Color` 15, `TrackGroupId` −1;
- output `AudioOut/Main`;
- empty session and freeze `ClipSlotList`s.

It is 21 lines, indented in the fixtures' two-space layout and inserted directly
after `<LiveSet>`. That is the `Tracks` schema position, where `fixture_audit.py`
inserts it.

## Re-check of every expectation

Each case was re-checked in two parts: does the set open with the added track, and
is the transport value read unchanged? Every expectation holds, and none had to
change.

- **Opening.** The T11 checker (`schema_check.py`, `fixture_audit.py` with the
  shipped schema) finds no traced refusal and no unknown shape on any v3 fixture.
  It finds no schema deviation beyond v2's: the existing order deviation, and the
  `Foo` element that TS-016 tests.
  - The track satisfies REQ-002 (one player track, no returns) and REQ-006 (zero
    session and zero freeze slots). REQ-013 is satisfied with no returns and no
    holders, and REQ-015 with no pointees present, where `NextPointeeId` absent
    reads 1.
  - REQ-016 is satisfied: Track `Id` 1 is valid and the clip lists are empty.
  - The track has no clips, devices or envelopes, so no field-level rule of
    another spec applies.
- **Value read.** The track lies under `Tracks`. Every judged path is
  `Transport/…` or `MainTrack/DeviceChain/Mixer/…`, anchored at `LiveSet`.
  REQ-TRANSPORT-STATE-001 makes homonymous elements elsewhere different fields,
  so a track mixer's own `Tempo` would not count. The cross-check model gives
  the same outcome, state and saved values for all 33.
- **Refusals isolated.** Each refused fixture differs from TS-022, the unchanged
  document, only in the tested `Transport` child or `Manual` line. TS-022 opens.
- **Saved paths.** The judged saved paths and `transport_order` do not reach
  into the track. A save writes the track, but no case judges it.

## Findings while staging

Revision 4 contains no requirement error. Points for the reviewer:

- **F1, relationship.** v3 is corrective, not a superset in bytes: every fixture
  changes, and every record and clause is equal. The manifest's
  `supersession.fixture_changes` names all 33 fixtures and the single change. The
  README's change list names them by range and states the defect.
- **F2, remaining omissions.** The fixtures still omit other `LiveSet` members:
  `Scenes`, `PreHearTrack`, `SendsPre`, `NextPointeeId`, `GlobalQuantisation`,
  `AutoQuantisation` and view state. In the T11-MIN table these are O, V or W.
  - Opening without them rests on SPEC-LIVE-SET-STRUCTURE REQ-001 (S: absence is
    not an error) and on the traced checks passing.
  - SPEC-CLIP-LAUNCH REQ-008 leaves the values of absent quantisation fields U.
    No case judges them.
  - v3 keeps the v2 sentence about absent content, qualified "apart from the
    track list". A reviewer who wants the full T11-MIN skeleton would be
    changing more than validity requires, against the brief.
- **F3, audit wording.** The audit records the insert point as "before
  MainTrack". Its own `insert_ordered` puts `Tracks` first, at its schema
  position, which is also before `MainTrack`. v3 follows the code. Each v3
  fixture equals the audit's repaired copy in canonical XML (33/33).
- **F4, kept deviation.** v2's schema order deviation (`Transport` before
  `MainTrack`) is kept. Order does not change what is read
  (SPEC-LIVE-SET-STRUCTURE REQ-001, S), and fixing it would not be a validity
  change.
- **F5, transport-state-v1.** Its 18 fixtures have the same defect. v1 is already
  superseded and immutable. The v3 README and manifest say so, and no separate
  action is planned.
- **F6, spec page (reported, not fixed).** The [spec page](transport-state.md) does
  not record the fixture defect:
  - its "Revision and handoff" section presents transport-state-v2 without it;
  - its Acceptance cases describe the fixtures as edits of the shipped set B0,
    which has tracks, whereas both releases use authored minimal documents.

  The spec owner should note that released fixtures are built on T11-MIN, and
  should name v3 once it is released. Neither point changes an expectation.

## Deliverables

- Payload: [transport-state-v3/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v3/README.md)
  with the scope, the supersession and a six-item change list. The package also
  holds `AGENTS.md`, `spec.md`, `cases.json` (33 cases), `fixtures/` (33 files) and
  a draft `manifest.json`.
  - The manifest has review pending and supersedes `transport-state-v2`, with the
    superseded manifest digest `398a88a6…24c17c8`.
  - It carries `defect_corrected`, `fixture_changes` (all 33 paths), the change
    list, and v2's provenance labels and stated assumptions.
  - It lists 37 payload files; with itself the package has 38. Draft manifest
    SHA-256: `f3dffd745a5d1009d720ff9768524ea0240a523d247606b83dde6832bcac9d0d`.
    Review edits will change it.
- Analyst side, never shipped: `transport-state-v3-analysis/`.
  - [build_v3.py](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v3-analysis/build_v3.py)
    builds the fixtures from the released v2 bytes and the audit addition, then
    the cases and the manifest, and runs the checks. It imports `build_v2.py` (and
    through it `build_ts1.py`) and the T11 checker unchanged.
  - [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v3-analysis/traceability.json)
    gives each case its v2 transport evidence, its audit locator and its v2 and
    v3 structure result.
  - [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v3-analysis/author-validation.json)
    holds the check results, and `t11-fixture-audit.json` the T11 audit tool's
    own output on the staged package.
  - [v2-to-v3-text.diff](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v3-analysis/v2-to-v3-text.diff)
    is the text diff from v2.

## Evidence traceability

| v3 element | Evidence | Residual inference |
| --- | --- | --- |
| All 33 transport expectations | v2 [plan traceability](transport-state-v2-handoff-plan.md#evidence-traceability) and [review](../../handoff/transport-state-v2/REVIEW.md), unchanged | As in v2 |
| The track makes the set openable | [SPEC-LIVE-SET-STRUCTURE](live-set-structure.md) REQ-002 and REQ-006 (S, A1 and A2 settled), REQ-013 and REQ-015 (S); `fixture_audit.py` `after_additions` (no refusal) | A1's remaining inference: that menu and OS open events use the traced entries |
| Omitted content is not refused | SPEC-LIVE-SET-STRUCTURE REQ-001 (S) | As in v2 |
| Defect statement | `released-fixture-audit.json` `releases[transport-state-v2]`: 33 refused, 23 contradicted, 10 not isolating | None |

## Mechanical checks performed

`python3 -I -B build_v3.py build` then `seal`, with CPython 3.13.9, wrote the author
validation. A second build and seal reproduced the same draft manifest digest.

- **v2 identity.** The v2 manifest digest equals the catalog value, and every v2
  payload hash matches.
- **Carry.** All 33 case records are equal to v2's, in the same order.
- **Fixture change.**
  - For 33 of 33 fixtures, every v2 line is kept in order and the only change is
    the 21-line track list, inserted after `<LiveSet>`.
  - 33 of 33 equal the audit's repaired copy in canonical XML.
  - All are ASCII with LF endings and no tabs, and none duplicates another.
- **Structure.** The T11 checker refuses 33 of 33 v2 fixtures and 0 of 33 v3
  fixtures, and finds no unknown shapes and no new schema deviation. Running
  `fixture_audit.py` itself on an exported copy gives 33 Live Sets, 0 refused,
  0 contradicted and 0 not isolating.
- **Model.** The combined judge (structure rules, then the v2 cross-check model)
  agrees with all 33 expectations, and no fixture hits an exclusion. Changing any
  one expectation is caught (33/33).
- **Isolation.** All 10 refused fixtures differ from TS-022 only in the tested
  element line, and TS-022 opens.
- **X agreement.** All 15 X expectations equal their extracted-execution records,
  and the 11 corroborated static cases agree.
- **Package.** The hashes and sizes of the 37 files match, checked again with
  `sha256sum -c`, and the inventory equals the directory. All 13 Markdown links
  (README 6, spec 7) resolve inside the package, and every case input exists.
- **Deny list.** The v2 list plus T11, audit, checker and planning-ID patterns.
  It has no hit; allowed phrases are matched across line wraps.
- **Export.** `verify` on a copy in the session scratchpad matched the seal report.

Not checked: reference or candidate execution, and the open path beyond the traced
rules.

## Review gates still required

1. **Defect and scope review** in a separate context.
   - Confirm that each v3 fixture is its v2 file plus the audit addition, and
     nothing else.
   - Confirm that the addition gives no structural refusal, and rule on F2 to F4.
   - Confirm that revision 4 adds no clause.
2. **Carry check.** From `v2-to-v3-text.diff` and the carry checks, confirm that
   every case record, clause, assumption and exclusion is unchanged except the new
   track exclusion and precondition.
3. **Re-check.** Re-run the T11 checker on the exported fixtures. Re-run the
   transport expectations or rely on the v2 review's runs, which cover
   byte-identical value texts.
4. **Quality and sanitization.** The track-list explanation must be intelligible
   without analysis. Check that the payload has no internal names or analyst
   links, and that the exclusions agree between `spec.md` and the manifest.
5. **Finalize.** Add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated export.
6. **Publish** only after approval.
   - Copy the package unchanged to `handoff/transport-state-v3/`.
   - Add a catalog row superseding transport-state-v2, and narrow the catalog's
     defect note.
   - Update the spec's handoff section (F6), coverage, indexes and the log.
   - Never edit transport-state-v1 or v2.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate with 33 cases, every record carried
from transport-state-v2 and every fixture corrected. It covers partial
REQ-TRANSPORT-STATE-001 to 008, 010 and 011; 009 and 012 remain unreleased. It is not
published. transport-state-v2 remains the current transport release, with its
"opens" expectations flagged by the catalog's defect note.
