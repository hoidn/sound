# MIDI storage: one remaining-unknown source batch

**Unreviewed source/proposal packet.** Selected under amended plan4 after the
approved MIDI family map, r5 probability-group source/owner reviews and exact
local midi-note-storage-v3 publication. It extends I-01/I-02 parsing/post-load
and I-10 save/error frontiers. No owner, case, normative expectation, release,
grade or implementation changes. Parent review/adoption remains separate.

[questions-and-proposals.json](questions-and-proposals.json) covers all eight
current U case IDs together: MNS-011,024,034,035,037,038,053,060; plus the three
retained partial group questions: final Save, later missing-note effect and
whole-load counter repair. Eleven bounded questions are not eleven new outcomes
or a whole-family denominator. No numeric/helper/example padding or new case IDs.

## Local source answers and blocking frontiers

| Question | Source refinement | Still unknown / proposal boundary |
| --- | --- | --- |
| MNS-011 | Existing Int64 wrapper chooses a substring that still includes trailing space for the stored space-digit-space input; whole-span converter success is required. This supports the existing local-refusal reading. | Conditional local parser refusal proposal only; no owner U change or public error/remaining-state result. No translated parser/model oracle runs. |
| MNS-024 | `Invalid` becomes DBL_MAX and is excluded from ordinary grid rounding. Generic held-number serialization does not establish which note survives or its final saved value. | Actual clip mutation/retention, same-object Save and final text remain unknown under A2. |
| MNS-034 | Signed Int64 parsing and unsigned next-id max are separate layers; no nonnegative repair guard follows from the latter. | Negative next id remains excluded/U. No safe refusal, admission, saved text or repair expectation. |
| MNS-035 | Selected load and writers preserve held order; the collected nonzero NoteId vector is sorted separately from notes. | No later public clip/edit/save sort/trim/merge chain; no final saved-order conclusion. |
| MNS-037 | Unsafe/missing/duplicate MidiKeys stay permanently excluded. | **Zero required safe-refusal outcomes.** No invented guard or required behavior, including for duplicate keys. |
| MNS-038 | KeyTrack list construction/descriptor and inherited generic-list loader now connect conditionally to its explicit duplicate parsed-Id refusal. | Proposal only: local duplicate-Id refusal for the existing two-Id5 input. Actual public catch and saved Id identity/meaning remain U; empty-KeyTrack removal's global flag owner remains untraced. |
| MNS-053 | The temporary receiver has a conditional APerNoteAutomationAdapter construction route; old class table +308 identifies a thunk and actual body, which forwards to further virtual/transaction operations. | All four boundary variants stay U. Exact next conditional targets and unresolved native sites are retained; resulting event array/commit semantics are not derived. |
| MNS-060 | Local corrupt-document error carries detail. | ALS009 shared top-level catch/notification/rollback and whole-Set/clip/UI result remain missing, not another local throw. |
| Group final Save | Reviewed registered shape/member/list writer still applies conditionally. | No public final group state, default omission, save/reopen or durability claim. |
| Group missing-note later effect | Registration stores supplied ids without validating note existence under the predecessor's body limits. | Actual map consumer, listener/player delivery and later effects unknown. |
| Group whole-load counter | Note counter +598 and group generator +5b0 are distinct; local comparison is not global repair analysis. | All counter writes and notification/load order remain untraced. Retain supplied-counter premise. |

## Exact source and class associations

[source-locators.json](source-locators.json) references 25 already retained
records in S7, its release review, T11's pointee trace and the group packet.
Those records are not copied again. Six needed C1 records are retained once in
[new-source-rows.jsonl](new-source-rows.jsonl), selected from two chunks checked
against approved packet1a chunk hashes. Selection was an exact known-entry lookup,
not a broad source dump. Original source C is data, never a compiled/translated
model oracle. [pins.json](pins.json) pins predecessor manifests and selected
as-of inputs without copied specifications or released payload-universe replay.

MNS-038's conditional chain is AMidiNotes constructor `1028f4048`: member wrapper
at +428 holds the list object at +430, initialized through `10156b17c` and bound
through `10156da84` to descriptor `1028ab68c`, whose DAT106e58710 also identifies
the retained AKeyTrack registry `1028ab80c`. The inherited ARemoteableList table
10667ec98 +140 points to `10156d7d8`, whose C expression calls generic loader
`1014674b4` on its +70 list subobject. The loader's local seen-Id set rejects a
duplicate parsed Id with the corrupt-document detail before constructing/loading
that duplicate item. These are constructor/descriptor/table-based conditions,
not a live receiver/ABI observation. Generic writer `101468408` emitting held Id
does not prove loaded Id preservation through the public lifecycle.

MNS-053's construction route is `10292b9ec → 1025c442c → 1025c4484`, with setup
`1025c4708`. The constructor stores vptr1067decd8, identified by the approved
table as APerNoteAutomationAdapter. Its +308 slot points to `1025c6068`:
**four native bytes**, with an exact retained tail jump to `1025c606c`, whose
body is **312 native bytes**. The thunk's expanded C is not a second 1,317-byte
implementation. The actual body invokes +2e8 and +398 and transaction helpers.
The same conditional table associates those slots with `10256314c` and
`1025654e8`. Their bodies and event-array/callback/commit effects are the next
untraced frontier; no resulting event text or retention is proposed.

[call-rows.jsonl](call-rows.jsonl) preserves eight exact existing call-index
rows for the thunk/body. [indirect-rows.jsonl](indirect-rows.jsonl) retains two
unresolved native sites, 1025c6110/1025c6148. Relative C ordering suggests their
slot association, but no new instruction decode verifies the operands; do not
present them as newly resolved native sites. Main inventory remains
25,071/268,015 with zero added credit. The class-table projections retain their
extent limits and exact parent-row locators. No binary, decoder or provider runs.

The predecessor group packet's native-body restrictions remain mandatory for
registration/callback C that expands beyond its 244/176/4-byte native bodies.
MNS-053's concrete new frontier does not remove A1, valid-object, same-class or
transaction premises. A1 is the existing static ordinary Set-read gate; it is
not a public catch or whole-load counter-order proof. A2/A3 and all unsupported
enum/playback, malformed-required-field, special-number and other exclusions
remain unchanged. No new XML examples or fixtures are manufactured.

## Integrity and freeze

[check.py](check.py) performs stdlib data-only selected row/span/body/class/call
integrity and meaningful negative controls. [author-check.json](author-check.json)
records only those checks. No old script/module, original function, harness,
model, comparator, build, fixture, native tooling or candidate runs. Proposals
must receive independent review before any later batch owner reconciliation;
this packet neither promotes a U case nor authorizes a new execution.
