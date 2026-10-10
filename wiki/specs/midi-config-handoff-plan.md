---
id: PLAN-MIDI-CONFIG-HANDOFF
type: research
status: current
updated: 2026-10-09
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# First MIDI configuration handoff design and task plan

## Decision and boundary

Prepare a finite candidate snapshot from revision 1 of the
[MIDI user mapping specification](midi-user-mapping.md), using the fallback in
[the phase execution plan](../research/native-phase-execution.md). The current
native transport packets establish selected code relationships, not a useful
observable playback or persistence contract. The MIDI candidate can exercise
the review and handoff process without inventing those missing behaviors.

This is an analyst-side proposal, not a published release or application
implementation. A separate reviewer must check completeness, sanitization,
fixtures and independent export before any local handoff publication.

The selected input surface is three ordinary CC assignments: master volume,
cue volume and crossfader. Their public configuration keys identify meaningful
user targets without requiring unspecified track order, device banks, pad
exceptions or transport timing. The candidate includes only these explicit
partial scopes of existing stable requirements:

| Stable requirement | Included clause | Remaining clauses |
| --- | --- | --- |
| REQ-MIDI-USER-002 | Ordinary CC number acceptance/disable for the three selected controls | Other assignments and all pad behavior excluded |
| REQ-MIDI-USER-003 | Global and selected per-control channel acceptance/fallback | Pads and other per-control inputs excluded |
| REQ-MIDI-USER-010 | Assignment targets: master volume, cue volume and crossfader | Numerical response, mode transforms and audio effects excluded |
| REQ-MIDI-USER-013 | Case-insensitive option names within the exact supported sections | General syntax/error policy and other interface limits excluded |

Map modes are fixed to explicit `Absolute` in fixtures; this does not specify
a MIDI-value-to-parameter curve. The normalized assignment JSON is a project
comparison representation, not an asserted API or recovered data structure.
It describes whether a control has a configured CC route, its effective channel,
and the user target. No promise about native routing priority or resource
ownership is implied.

## Deliverables and evidence separation

Stage a self-contained payload at
`analysis/ableton-live-12.4.3/handoff-staging/midi-config-v1/` with an entry page,
role instructions, behavioral spec, case matrix, independently authored minimal
configuration files, and manifest covering every payload file. Preserve the
stable requirement IDs and identify the selected clauses on every requirement
and case. Do not copy template comments, original code, pseudocode, recovered
identifiers or analysis locators into the payload.

Keep traceability outside the payload under the adjacent
`midi-config-v1-analysis/` directory. It will pin the source draft, reviewed
findings, case derivation, payload digest and mechanical validation. Expected
assignment outputs are static-derived; original reference and candidate
execution remain `not-run`. The exported instructions must permit only reviewed
handoff contents, neutral governance and independently authored candidate work.
An unreleased staging package is not an authorized implementation input.

## Sequential tasks and acceptance gates

1. **Design:** write this scope and task plan before generating the package.
2. **Author:** express selected clauses as external configuration behavior;
   enumerate all unsupported syntax and unresolved wider behavior. Create small
   original ASCII fixtures with exact filenames and explicit Absolute modes.
3. **Cases:** cover all three targets, ordinary CC endpoints and disabling,
   global channel endpoints/fallback, explicit channel precedence/fallback,
   and option-name case normalization. State complete expected assignments;
   each case begins from fresh independent input. No unknown expected output
   is given a passing comparator.
4. **Seal candidate:** inventory every payload file with SHA-256 (excluding the
   self-referential manifest); pin the manifest hash outside the package.
   Validate schema, filenames, normalized routes, coverage and all links in a
   copied package without analyst files. This checks authored fixture consistency,
   not agreement with a running reference.
5. **Independent review:** separate author/scope/quality contexts review behavior,
   evidence, sanitization and sharing suitability. Retain findings and corrections;
   pending review is a blocker to publication.
6. **Publish after approval:** root may release a new immutable handoff with the
   completed reviewer record and verified digests, update the handoff catalog,
   canonical spec status/partial scope, indexes, coverage and log. Do not grant
   approval to the unreleased remainder of the canonical MIDI draft.

## Current disposition

Authoring completed: the [candidate entry point](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v1/README.md)
contains four explicitly partial requirement clauses and 54 independent cases.
The [manifest](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v1/manifest.json)
inventories 58 payload files; including itself the package contains 59 files.
Its SHA-256 is `029b7bb35d4b46ea40e0a394d43ac2c515c702c98bb035def9015953e020c932`.

The [author check](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v1-analysis/author-validation.json)
verified hashes, exact file set, self-contained links in a temporary copied
package, fixture structure and expected-value ranges. It did not execute a
reference or candidate, or independently prove expected outcomes. Separate
[analyst traceability](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v1-analysis/analyst-traceability.json)
pins the reviewed source draft, supporting static findings and case derivations.
Independent scope, quality and final release checks passed. The
[local release](../../handoff/midi-config-v1/README.md) retains all 54 fixture
bytes and case expectations unchanged; its manifest covers 59 payload files.
The [final release check](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v1-analysis/final-release-check-v1.json)
verified 60 total files and eight isolated-package links.
[Reviewed wiki snapshots](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v1-analysis/reviewed-wiki-snapshots-v1/manifest.json)
preserve the exact source-draft and plan bytes pinned before publication; their
canonical pages may advance. No reference execution, compatibility pass,
application implementation or isolated implementation workspace is claimed.
