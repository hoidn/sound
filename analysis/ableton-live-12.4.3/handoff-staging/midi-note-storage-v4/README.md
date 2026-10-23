# MIDI clip note storage in Live Sets, release 4 candidate

**Unreviewed staging candidate; unpublished.** Read [the contract](spec.md),
[the cases](cases.json), [role instructions](AGENTS.md), [manifest](manifest.json)
and [review gates](REVIEW.md). Independent content approval, an external exact-tree
seal and coordinator local publication are required before implementation use.
No application or candidate execution or compatibility result is established.

This candidate carries all 78 midi-note-storage-v3 case objects, all 78 gzip
fixtures and all 14 selected requirement bodies exactly. It adds two conditional
static local-reader cases, MNS-076/077, for 80 case records and 15 partial
requirement IDs. No new fixture is generated. Both additions reuse the existing
independently authored MNS-001 fixture with the explicit decoded Notes edits in
input_projection: n3 NoteId space-7-space, or both KeyTrack Id values 5.

Both use validate-notes and compare only local_reader_outcome=refused. This is a
project comparison projection, not a public validation API, native invocation or
required implementation pipeline. An implementation may validate anywhere suitable.
Field/list associations and ordinary-reader premises remain conditional; A3 is the
integer-field association premise. The read-phase refusals are separate from A1's
post-read checks and A2's same-state Save assumption. Public load, catch, UI,
loaded state, rollback and saved state remain unknown for these inputs.

## Supersession

If independently approved, sealed and published locally, v4 supersedes
midi-note-storage-v3. That release remains immutable. At staging, v3 remains current.
The 72 carried public open/open-save cases and six carried local group comparisons
retain their exact content, fixture bytes, provenance and assumptions.

## Changes from midi-note-storage-v3

1. A separate REQ-002 local supplement judges only the exact MNS-076 input.
2. Partial REQ-012 judges only the exact MNS-077 duplicate parsed-Id input.
3. The two decoded Notes projections share MNS-001; 80 cases use 78 fixtures.
4. No public unknown, expression boundary result, saved group state, later effect,
   complete-load counter repair, unsafe-key outcome or X clause changes.

All expectations are static-derived or retain the existing extracted-execution
labels. No shipped content, original code, application implementation, public
source or dependency is included. Staging is not publication or compatibility.
