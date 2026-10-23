---
id: RES-ARRANGEMENT-EDITING
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Arrangement editing evidence

## Conclusion and limit

The retained Live 12 manual supports a substantive workflow contract for
Arrangement selection, clip movement/slip/split, consolidation, time commands,
locators, meter markers, loops, Session overrides, fades and linked-track editing.
It does **not** pin those behaviors to 12.4.3: the captured pages identify major
version 12 only. The [canonical draft](../specs/arrangement-editing.md) therefore
labels manual behavior D-manual and exact-build parity U. No edit command has
been run in Live or extracted execution, and no candidate exists.

The installed schema and one shipped demo establish representable Arrangement
objects, and a retained arm64 native registry establishes selected command names.
Neither source closes gesture edge behavior, undo/cancel/teardown, persistence
transitions or rendered fade/consolidation output. The draft records those gaps
as cases with no invented expected result. This is partial specification coverage,
not whole-Arrangement completion or a reviewed handoff.

## Retained sources

Packet: [full-spec-v1/arrangement](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manifest.json).
The manifest hashes every retained packet payload; source entries retain target,
version, location, capture date and limits. The web HTML/text were captured on
2026-10-19 and remain separate from the immutable `raw/` tree. Prose was read;
linked illustrations were not visually inspected.

| Source ID | Exact retained location | Authority and limitation |
| --- | --- | --- |
| SRC-ARRANGEMENT-MANUAL-12-20261019 | [capture metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manual-source.json), [text](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manual-arrangement.txt); sections 6.1–6.15, heading/ANCHOR delimiters | Official [Arrangement chapter](https://www.ableton.com/en/live-manual/12/arrangement-view/); D-manual, not proof of patch parity |
| SRC-CONCEPTS-MANUAL-12-20261019 | [capture metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/concepts-source.json), [text](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manual-concepts.txt); sections 3.6–3.8 | Official [Concepts chapter](https://www.ableton.com/en/live-manual/12/live-concepts/); D-manual, same version limit |
| SRC-ARRANGEMENT-PACKAGE-12403 | [schema/demo inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/schema-demo-survey.json); `schema.classes`, `demo.main_lane_clips`, `demo.locators` | D-package: exact schema bytes and a demo shipped in 12.4.3, created by 12.4d1 |
| SRC-ARRANGEMENT-REGISTRY-12403 | [native record](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/native-command-registry.jsonl); arm64 `0x101741430`, `chunk-00918.jsonl` offset 161795, line SHA-256 `f8ee6065cf891077a83968af4123219db9748ef0dc0a9b8cfc66227f98d8737e` | S: static command-name registry; no dispatch, error or transformation law |

Official captures have exact HTML and normalized-text SHA-256 digests in their
metadata and in the draft evidence appendix. Both pages can drift after capture;
the local version, not a future live page, is the cited source revision.

## Observations from the pinned package

**Observed, D-package.** Installed
`Contents/App-Resources/Schema/12.0_12402.txt` has SHA-256
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
The inventory retains fourteen relevant classes and their direct fields. AudioClip
and MidiClip expose separate visible start/end values; AudioClip has ClipFades;
Locator has time, name, annotation, mapping and song-start fields; the schema
also has linked-track membership/group declarations and TimeSelection fields.
Presence is not a legal range/default, nor proof of a UI or persistence transition.
Exact class names and fields are retained as evidence data, not proposed candidate
architecture. (Inventory `schema.classes`; REQ-031.)

**Observed, D-package.** The demo at
`Core Library/Lessons/Demo Songs/Chuck Sutton - Patience (Live 12 Suite Demo).als`
hashes to `3f1c0f924b750c2adba2525838f2bc00856e52faea09d43b9279c6a0fe40952b`.
Its document root identifies `MinorVersion=12.0_12402`, Creator Ableton Live
12.4d1 and revision `42bc084cd8152e4fb737ef3fefd04b2bea5320e7`.
The bounded survey finds 64 **main-lane** Arrangement clips: 55 MIDI clips under
`MainSequencer/ClipTimeable/ArrangerAutomation/Events`, nine audio clips under
`MainSequencer/Sample/ArrangerAutomation/Events`. It also finds nine named locators
from Intro at 0 to Outro at 352. The demo has an empty LinkedTrackGroups list, so
it offers no positive grouped-edit example. The inventory records exact track
and clip Id-qualified XPath locators. (`demo.main_lane_clips`, `demo.locators`,
`demo.linked_track_groups`; REQ-031.)

The [clip-launch draft](../specs/clip-launch.md) counts 90 Arrangement and take-lane
clips in its MIDI launch-quantization subset of the same demo. This packet's
64-count includes audio main lanes and excludes take lanes; the denominators
differ. The first audio clip found by a recursive search was a Session clip,
which is why the retained survey uses explicit main-lane containers rather than
`.//AudioClip`. No contradictory count is silently reconciled.

**Observed, S.** Native arm64 entry `0x101741430` registers names including Split,
Consolidate, Duplicate, LoopSelection, CreateFade, BackToArrangement, Undo and
Redo. Its retained original record is exported with warnings. The independent
string-index capture contains selected Split/Consolidate/Back to Arrangement
strings and referring locations, in
[native-command-strings.json](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/native-command-strings.json).
This corroborates vocabulary in the 12.4.3 executable, not behavior of the commands.
The original arm64 image SHA-256 is
`3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`, pinned by the
[installed source record](sources/ableton-live-12.4.3.md).

## Manual-derived contract and boundaries

The canonical behavior and individual source-section mapping live only in
[SPEC-ARRANGEMENT-EDITING](../specs/arrangement-editing.md). This research page owns
source interpretation and limits; it does not repeat each requirement.

The manual explicitly distinguishes ordinary selected-material edits from
all-track time insertion/removal (6.9, 6.11), clip fades from automation (6.8),
per-track Session override from a view change (Concepts 3.6–3.7), and simultaneous
linked fades with matching start positions from other fades (6.14.2). Those
boundaries support positive and negative cases without inventing internal laws.

The manual does not define an ordinary Duplicate destination/overlap policy,
minimum clip lengths, MIDI note ownership at Split, exact fade curves, waveform
rendering thresholds, or cancellation/undo/failure outcomes. The draft's local
questions Q-ARR-001–008 select narrower native investigations rather than using
strings as proof. Its D-manual and D-package labels must remain distinct in any
future release; no exact-build X edit behavior is present.

## Historical R1 reproduction and checks

The following historical inventory author writes its output. It is preserved for provenance only and must not be rerun for this successor; the historical R2 check was validate-r2.py --check; current R3 uses validate-r3.py --check:

```sh
python3 -I -B analysis/ableton-live-12.4.3/full-spec-v1/arrangement/survey.py
```

It reads the pinned schema/demo paths and asserts required classes/fields,
schema version, nonempty main-lane/locator results and unique retained clip
locators before writing the packet inventory. Its successful output is retained
in [validation](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/validation.json).
The first exploratory schema name `TrackClipTimeable` did not exist; it was
replaced with the observed classes `TimeableMidiClip`/`TimeableSample` before the
successful survey. The initial MIDI-only path missed audio; the explicit audio
`Sample` branch was added and both clip types are now independently asserted.
These were evidence-tool query corrections, not changed reference behavior.

Packet hash verification, focused Markdown metadata/link checks and
`git diff --check` are recorded in validation. They establish documentation
integrity only. Source capture requires network access; inventory needs the
installed package; the retained native excerpt is sufficient for its bounded
registry claim without reopening Ghidra or launching Live.

## Historical R1 disposition

The draft is ready for independent analyst-side review with exact-build parity,
edge behavior and lifecycle gaps kept visible. It contains 35 requirements and
65 scenario definitions, not 65 executable fixtures. No released payload, existing
handoff, implementation material or runtime validation was changed. Shared index,
coverage and analyst-log updates are owned by the parent integration task.

## Historical revision 2 retained-source adoption

The [Arrangement source audit R2](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement-source-audit/README-r2.md)
was independently reviewed after ASA-REVIEW-001 corrected three historical
Session action associations. Its full-read scope is 164 Arrangement and 22
selected Concepts text blocks, including Transport/Playback and Arrangement
Mixer; literal image/link/caption attributes/text were read, pixels and linked
destinations were not. Full source text is not a compatibility denominator.

The [owner successor](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/README-r2.md)
retains all 35 old requirement and 65 case IDs, adds seven public-role clauses
and nineteen separately reset compound proposals, and records exact field deltas.
Signal, numeric, timing, file, public-dispatch and unresolved outcomes remain
null/U; no native law, render formula, default constructor or runtime evidence
was added. Current Session R3 SV041 is the explicit deliberate-nonsequential
route; old SV001 remains its neighboring A/B history. Current Clip R2 already
provides editor Follow and Overview contexts; Arrangement-specific contexts
remain separate. Existing owners retain storage, playback, note, Warp, recording,
mixing, media and export laws. All original packet files and canonical bytes
are preserved, and consumer pins are enumerated as historical dependencies.
No adapter or old live-canonical gate was added.

Historical R2 checking used `validate-r2.py --check`; that whole-file checker is not a current R3 entrypoint and is not replayed. The older
`survey.py` is an original inventory author that writes its JSON output; it was
not rerun/imported for this successor and is not the read-only reproduction
entrypoint. The earlier reproduction prose is retained as R1 history in the
[research snapshot](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/research-r1.md).
Independent owner review is pending as of this freeze; shared indexes/reviews
will route its current disposition. All lifecycle and exact12.4.3 gaps remain.

## Revision 3 review correction

The [independent R2 review](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/review-owner-r2.json)
held adoption for ARR-R2-REVIEW-001: nine numeric/duration documentary
expectations conflicted with their no-numeric comparators. The minimum
[R3 successor](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/README-r3.md)
sets those eighteen fields null in AR010/016/017/024–029. Historical source
claims, predicates, all42requirements/all84actions and actual U/null status
are unchanged. Current classification is43named/41null; R2's52/32 report and
its inaccurate visible-only label remain preserved historical evidence.

No new source, gesture, numeric behavior or case was adopted. All R1/R2 files
and reviews remain immutable; requirements still use requirements-r2.json,
while current documentary pairs use cases-r3.json. Current checking is only
`python3 -B analysis/ableton-live-12.4.3/full-spec-v1/arrangement/validate-r3.py --check`.
It uses two explicitly inspected pure R2 assertion functions and four pure
Browser definitions, never the old main checker/author or a live-canonical
adapter. Source and delta integrity do not replace the required independent
focused review. All exact-build, lifecycle, signal/timing/file and retained
other unknowns remain U; no compatibility or completion credit follows.
