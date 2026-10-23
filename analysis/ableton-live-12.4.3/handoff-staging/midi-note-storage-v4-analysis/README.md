# MIDI note storage v4 staging evidence

Analyst-only sibling; never copy it into a released handoff. The
[candidate](../midi-note-storage-v4/README.md) is unreviewed and unpublished.
The [handoff plan](../../../../wiki/specs/midi-note-storage-v4-handoff-plan.md)
owns selection, boundaries and remaining gates. The package carries all 78 v3
objects/fixtures and 14 bodies exactly, adding two projected local comparisons
and partial012 for 80 cases/15 IDs. No fixture is generated.

[pins.json](pins.json) binds v3, the approved r6 owner prefix, its additive current
as-of draft, owner review/adoption and source review. [traceability.json](traceability.json)
records only the two approved case additions. [release-spec-delta.patch](release-spec-delta.patch)
is the exact sanitized spec delta, with the old 14 bodies preserved; no full
source or canonical spec snapshot is copied.

Run the new read-only checker from the repository root:

`python3 -B analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v4-analysis/check.py`

The checker imports only stdlib, writes nothing and computes no expected reader
outcome. It checks authored input edits, carry identities, gzip structure, isolated
links, sanitization, pins and payload hashes. [author-validation.json](author-validation.json)
retains its report. No old helper is executed/imported. The original malformed
MNS-012 fixture is preserved; only the well-formed authored MNS-001 base is parsed
for the two projections. Prior schema/structure approval is inherited by exact
bytes, not rerun through old tooling. No native/original/model/comparator/build
or candidate execution occurs.

Independent staged-content review, external exact-tree approval and coordinator
full prerelease lint remain pending. Package and analyst manifests are distinct;
the future external exact-tree seal must not hash itself through a payload field.
