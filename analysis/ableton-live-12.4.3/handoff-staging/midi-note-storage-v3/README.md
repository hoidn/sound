# MIDI clip note storage in Live Sets, release 3 candidate

**Staged, unreviewed and unpublished.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review gate](REVIEW.md).
This candidate is not an approved implementation input or a compatibility pass.

The candidate has 78 independently authored gzip Set fixtures and case records.
All 72 midi-note-storage-v2 case objects and their fixture bytes are unchanged.
Their partial reading/saving clauses, extracted-execution labels and assumptions
remain unchanged. Six existing parent-draft IDs, MNS-054 to MNS-059, add only
bounded static-derived probability-group comparisons under A1: four refusals
and two nonrefusals of the supplied Notes/group data. Their `validate-notes`
action and `local_reader_outcome` labels are a project comparison projection,
not a public Live API or a required implementation architecture.

The two admissions do not mean that the clip or Set opens successfully.
No added case judges saved groups, group-counter repair across a whole load,
playback or later missing-note effects. The exact input form uses a `GroupId`
child, nested `NoteId` attributes and separate list `Id` values, with group
type 0 and probability 1 only. Other enum values or playback meanings are
outside scope. No new original or candidate execution has occurred.

## Supersession

If independently approved and locally published, this candidate will supersede
midi-note-storage-v2. No existing release is changed. The v2 fixture repair
(one matching freeze slot and one scene) is retained exactly. The six additions
use its authored MNS-001 Set carrier and replace only its Notes content.

## Changes from midi-note-storage-v2

1. Partial REQ-MIDI-NOTE-STORAGE-015 and the six concrete local cases are added.
2. The comparison convention distinguishes local group rejection/nonrejection
   from the 72 carried public open/open-save comparisons.
3. Exclusions narrow only for those six exact inputs; public lifecycle, final
   group save, complete-load counter repair and later effects remain unknown.
4. The 72 existing records, fixtures and 13 requirement bodies stay exact.

All expectations are static-derived or carry the unchanged extracted-execution
provenance stated in the contract. None is captured application behavior.
No application code, shipped content or public dependency is included.
