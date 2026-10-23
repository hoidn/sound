# MIDI probability groups: one mapped source batch

Unreviewed analyst evidence, selected after the approved MIDI family map.
This addresses all five open REQ-MIDI-NOTE-STORAGE-015 questions and the existing
six blocked MNS-054–059 cases together. No requirement, current case, release,
behavior grade or original execution changes here. [selection.json](selection.json)
records that initial consultation preceded formal capture; it invents no first-read
time. [pins.json](pins.json) identifies the approved map/review and exact providers.

## Source and body boundaries

[source-locators.json](source-locators.json) identifies 39 complete retained C1
records (86,545 C bytes), selected from 16 chunks checked against approved 1a
class-input pins. [source-rows.jsonl](source-rows.jsonl) preserves exact JSONL
bytes, warnings and code digests. Five [class-table rows](class-table-rows.jsonl)
are inherited conditional layouts from approved 1a, not fresh binary reads or
new indirect-resolution credit. [call-locators.json](call-locators.json) identifies
70 exact call-index rows for six relevant callers. No 4,185-chunk universe replay.

**Warning-bearing C can run beyond the native body.** Callback wrapper
`10290ad68` has a four-byte native body and tail-jumps at that PC to `1028f8e48`;
its 7,036-byte C projection is not a four-byte method's independent semantics.
Target `1028f8e48` has 176 native bytes, ending `1028f8ef7`; only its bounded
prefix is used. Its last listed call at `1028f8ef4` is `105424df0`. Registration
`1028f5770` has 244 native bytes ending `1028f5863`; the last call at
`1028f5860` is `105424d90`. Expanded C after those calls is not attributed to
these bodies. The separate AMidiNotes post-load record `1028f5864` owns its own
1,480-byte, discontiguous body and the group validation/error path. Native PCs
come from the retained index, not a new decoder run.

## Static findings and remaining questions

| Question | Selected evidence and disposition |
| --- | --- |
| Group XML shape | Schema `12.0_12402.txt` lines 5609–5620; group registry `10292627c`; ANoteId registry `102925eb4`; generic writer `101486cdc`. GroupId is a child member (type Int64, flag 0), while each NoteId is an attribute (Int64, flag 4). Group child order is GroupType, Notes, Probability, GroupId. Generic list item Id is separate from GroupId. This supports the concrete conditional shape below, not an observed public save. |
| Group type values | Constructor `102926720`, label builder `1029265f4` and enum initialization `101567bfc` associate ordered labels PlayAll/PlayOne with indices 0/1; constructor selects 0 and probability 1. Labels do not prove playback meaning, UI names or unsupported enum admission. |
| Missing note after load | `1028f5640` validates ordered group IDs then calls registration `1028f5770`. Its bounded loop copies eight-byte NoteIds into the owner+4b8 map via `102911e04`; that helper inserts/returns the supplied key/group pair without checking clip-note existence. Callback event 1 calls registration; event 2 erases supplied IDs via `1029116f8`. This narrows local registration; later playback effect and public lifecycle remain unknown. |
| Saved representation | Group factory/constructor installs vptr106829f60; inherited slots +138/+140 reach generic writer/loader and +150 generic false omission. Notes array constructor installs 10682a6e0, whose +138/+140 reach generic array writing/loading. ANoteId translator subobject 106829f38 has +0/+8 to 1029260a0/1029260b8, copying its eight-byte field to/from array storage. Conditional member shape is supported. Exact omission, final normalized values, public Save and reopen remain unobserved/unknown. |
| Group NextId repair | `102920ecc` only compares the supplied group ID unsigned below generator value. Validator rejects zero/non-increasing/out-of-counter IDs. Separate post-load `1028f5864` raises the note counter at owner+598; group validation uses owner+5b0. This does not prove whole-load absence of group-counter mutation, notification ordering or public repair. The existing malformed-group refusal premise stays scoped; general repair remains unknown. |

The list setup is explicit: AMidiNotes constructor `1028f4048` creates the
RemoteableList through `10156b17c → 10156b1d4`, installs the group descriptor from
`1029260d4` using `10156da84` and the named ProbabilityGroupsListNotifier.
List vptr10667ec98's +138 reaches `10156de64 → 101468408`, which writes each
item using its own stored Id and compound writer. The array descriptor uses
ANoteId and eight-byte stride (`10155ed5c`). These are class/constructor-based
conditional relationships; a current live receiver/ABI and public open/save
sequence are not established by them. The shipped schema supplies simple
GroupType/Probability Value attributes; it is not a shipped nonempty-group save.

```xml
<NoteProbabilityGroups>
  <NoteProbabilityGroup Id="0">
    <GroupType Value="0" />
    <Notes><NoteId NoteId="1" /><NoteId NoteId="2" /></Notes>
    <Probability Value="1" />
    <GroupId Value="1" />
  </NoteProbabilityGroup>
</NoteProbabilityGroups>
<ProbabilityGroupIdGenerator><NextId Value="2" /></ProbabilityGroupIdGenerator>
```

## Six concrete proposals, no adopted case changes

[case-proposals.json](case-proposals.json) and six [fixtures](fixtures/MNS-058.xml)
materialize all existing G cases using current F0's Notes fragment. Group list Ids
0/1 are distinct from tested GroupIds. Type 0/probability 1 and existing note IDs
1/2 are concrete defaults, including previously unspecified notes in 055–057.
Case059 uses missing note99. No new case IDs, numeric outcome padding, synthetic
execution or compatibility pass. These are Notes fragments under the existing B0
carrier/premises, not complete loadable Sets. Existing r4 shape-blocked cases
remain unchanged until a separate owner revision and independent review adopts
these forms. Saved text and later missing-note effect stay unknown.

The owned [checker](check.py) verifies exact retained rows/locators/code digests,
conditional table links, native-body PC boundaries and all six XML proposals.
Its negative controls reject a GroupId attribute, a NoteId child and a changed
case vector. It never invokes a source script, loader, original, compiler,
provider, decoder or model. A pass is documentary integrity only. Root owns the
packet seal, independent review, canonical adoption and any later owner revision.
