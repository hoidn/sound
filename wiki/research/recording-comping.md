---
id: RES-RECORDING-COMPING
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 4
target: Ableton Live 12 Suite 12.4.3
---

# Recording and comping evidence

Current bounded [owner R4](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/README-r4.md)
has34requirements/90case records:32oldclauses81oldobjects exact, twoqualifiedUI
roles andnine newnull histories. All90actualoutcomes remain null/U/unexecuted;
fourhistorical artifact-only scenarios are not application tests,86application
cases ungraded. Earlier counts, tables and R3 checker instructions below are
retained historical R3 context. Use current R4 links/checker in the final section.


## Scope and conclusion

Recording input, Capture MIDI and take-lane comping now have a bounded
[behavioral draft](../specs/recording-comping.md). It contains 32 requirements
and 81 unexecuted cases: 65 documentary Live 12 expectations, four pinned-bundle
artifact audits and 12 unknown cases. None is a recording compatibility pass.
The public manual does not identify its patch version, so **all 77 application
cases remain ungraded for the pinned 12.4.3 target**. The four artifact cases
grade only stored inventory. No recording-path extracted execution was run.

The draft owns behavioral clauses; this page owns provenance, synthesis and
gaps. Existing [clip-launch](clip-launch.md), [MIDI-note](midi-note-storage.md)
and [Set-structure](live-set-structure.md) conclusions remain authoritative for
their storage/playback subjects and do not become recording evidence.

## Retained sources

The [recording packet](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/README.md)
retains public HTML bytes, URL/final URL, UTC capture timestamps, SHA-256 values,
a read-only bundle/corpus inventory script and its results. The public sources
are the official Live 12 manual chapters [Recording New
Clips](https://www.ableton.com/en/live-manual/12/recording-new-clips/),
[Comping](https://www.ableton.com/en/live-manual/12/comping/),
[Routing and I/O](https://www.ableton.com/en/live-manual/12/routing-and-i-o/)
(monitoring/channel boundaries only), and [Session
View](https://www.ableton.com/en/live-manual/12/session-view/)
(§7.5 only). Capture date: 2026-10-19. They declare manual Version 12, with
no patch/build or publication date observed. Images were not inspected, so
this draft makes no screenshot/colorimetric/layout claim.

Pinned source bytes are from `/home/ollie/Ableton Live 12 Suite.app`, target
12.4.3 as identified by the [source record](sources/ableton-live-12.4.3.md).
The schema `Contents/App-Resources/Schema/12.0_12402.txt` has SHA-256
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
The existing retained C1/C2 arm64 corpus at
`/var/tmp/sound-analysis/corpus` supplies string/reference records; this packet
does not decompile or execute original code. The target arm64 slice remains
`3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.

## Observed storage inventory

[schema-fields.json](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/schema-fields.json)
retains the selected class/field declarations, with the original schema hash.
`AudioTrack` and `MidiTrack` declare a `TakeLanes` compound. `TakeLanes` declares
a list also named `TakeLanes` and `AreTakeLanesFolded`. Each `TakeLane` declares
`LomId`, `Height`, `IsContentSelectedInDocument`, `ClipAutomation`, `Name`,
`Annotation`, `Audition` and `ArrangementClipsListWrapper`, in that order.
`AudioClip` and `MidiClip` declare `TakeId`. The Transport declares PunchIn and
PunchOut and remote record/session/new/overdub controls; LiveSet declares
ArrangementOverdub and AutoQuantisation; Metronome declares
CountInDurationInBars. **Observed declarations, not proved interaction rules.**

[shipped-documents.json](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/shipped-documents.json)
lists all 376 `.als`/`.alc` documents under App-Resources, excluding AppleDouble
companions, with original byte hashes. Nine documents hold 140 lanes; their
lane paths include exact track/lane Ids. The lanes hold 140 MidiClip event
entries and no AudioClip entries. All 140 Audition values are false. There are
4,130 saved TakeId elements across all clips, of which 3,744 are zero; nonzero
values are present. **Inference deliberately withheld:** a TakeId number does
not by itself establish source identity, highlight equivalence, uniqueness or
allocation rules. The bundled files include content authored for earlier
versions; their presence in the pinned bundle is what the inventory establishes.

Concrete locators:

| Shipped source under `Contents/App-Resources/Core Library/` | Lanes | Original SHA-256 | What it establishes |
| --- | --- | --- | --- |
| `Lessons/Demo Songs/Chuck Sutton - Patience (Live 12 Suite Demo).als` | 26 | `3f1c0f924b750c2adba2525838f2bc00856e52faea09d43b9279c6a0fe40952b` | Saved MIDI take clips under `TakeLane/ClipAutomation/Events`; exact per-lane paths retained |
| `Templates/Vocal Recording.als` | 5 | `d12d2102137fbe08331d69a526518868d5bdc8d3a577815a9f404d73dbb3c26e` | Lane entries with empty Events; this template does not demonstrate recording execution |

The other seven documents and all individual lane metadata are in E-DOCS.
The survey retains selected metadata rather than copying note/event content.
It confirms an existing canonical clip-container observation in
[REQ-CLIP-LAUNCH-001](../specs/clip-launch.md#req-clip-launch-001--clip-launch-fields-location-types-and-order);
it does not change that requirement's scope.

## Native inventory and evidence limit

[native-string-excerpts.json](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/native-string-excerpts.json)
retains seven corpus records with line number, original line SHA-256, string
address and references: TakeLane (two referenced encodings), CaptureMidi,
CountInDurationInBars, Audition, PunchIn and PunchOut. Exact records include
CaptureMidi at `0x105ba7dec`, referenced from `0x101741978` in
`0x101741430`; Audition at `0x1062ecefc`, referenced from `0x10382c1b8`
in `0x10382c068`; PunchIn/PunchOut at `0x105bf34a3`/`0x105bf34eb`.
These are **S-inventory navigation seeds**, not a trace from a UI action to a
recording state transition. No S or X behavioral comparator is asserted.

## Documentary distinctions that affect the contract

The draft keeps ordinary recording, looping MIDI overdub, Capture and Session
performance recording separate. R19 §19.5 treats ordinary recording and looping
overdub differently when changing Record Quantization; a general rule that
freezes the setting in every record mode would erase the documented exception.
R7 §7.5 describes Session performance recording as Arrangement clip creation
without newly recorded audio data, distinct from R19's input recording.
These distinctions are documentation observations with patch applicability U.

The independent review found that R7 §7.5 limits recorded scene tempo/meter to
values included in launched-scene names. REQ-031 now preserves that qualifier;
RC-079 exercises the named-scene branch and RC-081 leaves the broader field-based
branch U. Playback ownership/return laws are linked to Arrangement REQ-020/021
instead of duplicated. RC-080 adds one finite selected-format/depth recording
scenario; it does not assert an unobserved menu enumeration. The scenarios
remain partial clause coverage, with no original execution or fixtures.

R21 §21.6 describes comp clips as independent copies of take clips; §21.7
conditions highlights on matching positions and properties. A persistent number
or common sample file is therefore insufficient evidence for a complete
highlight predicate. R21 §21.3 gives a lane-reuse condition without specifying
search ordering. These are limits on what the current draft can require.

Monitoring defaults need contextual handling. R19 §19.2 describes armed-track
auto-monitoring as the default, while R17 §17.1 explicitly names Off for audio
and Auto for MIDI when resetting Monitor. The draft retains the actual mode
semantics and leaves a universal factory/new-track default unresolved (R-G08).
No downstream default is silently changed.

## Open evidence gaps

| Gap | Missing evidence and impact | Bounded next evidence route |
| --- | --- | --- |
| R-G01 | Public manual patch applicability; every D12 behavior has exact-build U | Trace the corresponding pinned native command/state path or retain suitable exact-build evidence; do not infer compatibility from resource names |
| R-G02 | Recording timestamp/latency compensation; quantization rounding and note-offs; punch/count-in/loop endpoint ownership | Static trace from recorded input event to stored time; use extracted execution only for a bounded self-contained function if later authorized |
| R-G03 | Capture buffer size/reset/eviction, controllers/expression, phrase/tempo inference, repeated/no-input capture | Trace Capture input history and command dispatch; no heuristic is chosen from examples |
| R-G04 | Take allocation/reuse order, partial passes, exact source-highlight predicate and drag limits | Trace lane construction, comp replacement and matching; retain finite source/path evidence |
| R-G05 | Undo/redo boundaries for record/overdub/capture/comp, physical-media retention/deletion | Trace command transaction and media ownership; the three documented Undo clauses do not generalize |
| R-G06 | Save/reopen of comp/lane metadata, in-progress recording, unsaved media and first-save transaction | Trace serialization hooks and reference relocation; schema declarations alone do not settle restore behavior |
| R-G07 | Cancellation before start/during count-in/comp drag, disk/permission errors, disconnect/delete/close/crash finalization | Trace each bounded error/cancel path separately; retain errors and partial-media outcomes as unknown until supported |
| R-G08 | Exclusive/implicit arm preferences, new/reset monitoring defaults, frozen tracks and overlapping record commands | Read relevant pinned preference/command path; preserve both contextual manual statements |
| R-G09 | Crossfade curve/rounding and short-clip behavior; audition switching and signal suppression boundaries | Static audio-control trace plus retained finite numeric evidence if obtainable; four-ms documentation does not establish output DSP |

These are evidence gaps, not an authorization to run Live, install tooling or
execute original functions. No new original-runtime comparison is available.

## Validation and boundary

The inventory script is read-only with respect to bundle/corpus inputs; it
asserts that required schema classes, shipped documents and all selected native
string identities were found. A second run reproduced the retained summary:
376 documents, nine with lanes, 140 lanes, 4,130 TakeId elements, seven native
records. The packet's manifest hashes retain the exact outputs. This validates
inventory extraction only. Static artifact cases are not application tests.

No existing published handoff is edited. No application code or independent
candidate was written. All recording/capture/comp implementation and runtime
compatibility remain unestablished.

## R3 explicit scene-recording Off history

The [approved Settings owner reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-owner-reconciliation-review.json)
identified that RC-020 named a default preference state, while RC-021 named the
enabled state. The retained [recording-into-session-slots source](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-recording-new-clips-2026-10-19.html#recording-into-session-slots)
distinguishes ordinary scene launch from using Start Recording on Scene Launch
to record empty record-enabled slots. R3 changes only RC-020's setup/action to
explicit Off, actual recorded preference/transport/input/arm states and a matched
genuinely productive enabled RC-021 baseline. Use separate copied histories with
fresh empty slots, eligible record-enabled tracks and active admitted owned
input. Feature/source/track unavailability, occupied slots or a missing enabled
recording baseline cannot prove the negative. RC-021 itself is unchanged.

The original owner had no JSON requirement/case catalogs: its canonical
Markdown is the original case source. [Historical transcription](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/case-transcription-before-r3.json)
retains all81 exact old rows and their line/character spans against
[spec before R3](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/spec-before-r3.md).
[Current case view](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/cases-r3.json)
transcribes those six documentary cells, changing only RC-020 action. Explicit
actual expectation/comparison null, target-grade U and unexecuted fields are
new status fields, not assertions of historical measurement or grading.
All32 requirement clauses and all81 documentary comparators/evidence/kinds/IDs
are unchanged, including four static artifact-only scenarios. No new default,
constructor, numeric, recording-gate, persistence, lifecycle or timing law is
adopted. Existing explicit preference/source eligibility must be established;
no actual audio, MIDI, recording or application operation was run.

All12 prior packet files, including the revision2 manifest and its11 payloads,
remain unchanged in place; no whole archive is duplicated. Old canonical spec
frontmatter says revision1 and the old research page has no revision field.
Their exact bytes are preserved in the local before-R3 snapshots.
[Impact identities](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/impact-r3.json)
retain exact as-of JSON pointers and historical hashes. Frozen consumers remain
unmodified and were not replayed against the changed current pages; root owns
historical integration. Older first-review hashes remain historical mismatches.

[Focused source context](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/source-context-r3.json),
[delta](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/delta-r3.json) and
[read-only packet check](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/README-r3.md)
bound this correction. The retained section paragraphs/list items and RC-020/021
were read; unchanged requirements/actions are checked for exact preservation.
This is not a fresh semantic audit of all chapters, package inventories, figures,
linked destinations or downstream owners. Current public Version12 documentary
applicability remains U for exact12.4.3. Focused independent review is pending.

## Bounded revision 4 Comping inputs

The complete retained Comping-only [source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/recording-comping-source-audit/README.md)
passed [independent partial review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/recording-comping-source-audit-review.json).
Its38wholecontexts/24literalresources are not atomic facets or fullRecording
closure. Only12selectedclauses29selectedcasefields were freshly reaudited; other
old32/81 semantics carry prior independently reviewed scope and exact objects.

### REQ-RECORDING-COMPING-033 — take-to-main navigation and folding

**D12/target-U.** From a selected take lane, Left Arrow navigates to the main lane and folds all take lanes. This names the documented lane-focus input and visible folding role, not a global key alias, default, accessibility/animation timing or persistence law. Exact 12.4.3 action remains U.

Evidence: retained Comping source audit CMP:B008.

### REQ-RECORDING-COMPING-034 — file-to-take input roles

**D12/target-U.** Samples and MIDI files can be dragged onto take lanes from the Browser or platform File Explorer/Finder in admitted audio/MIDI contexts. With multiple samples selected, Ctrl on Windows or Cmd on macOS while dragging inserts each sample into sequential tracks. The latter scope is multiple samples, not a claim about multi-MIDI-file distribution. Supported-file admission, ordering, decoder/format grammar, copy ownership, cancellation and exact-build outcome remain U.

Evidence: retained Comping source audit CMP:B026.

[Current requirement view](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/requirements-r4.json)
preserves everyold32body andadds only those two publicroles. [Current cases](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/cases-r4.json)
preserve81old R3objects exactly. Nine newhistories are future input definitions,
not documentary/actual pass criteria.

| New case | Requirement suffixes | Bounded history |
| --- | --- | --- |
| RC-082 | 019,033 | Visibility/navigation and Automation Mode entry branches |
| RC-083 | 020 | Lane insert/duplicate/delete actual entry alternatives |
| RC-084 | 020 | Resize entry gestures and selected-lane scope |
| RC-085 | 020 | Reorder and rename routes/multiselection traversal |
| RC-086 | 034 | Actual library/file-to-take insertion and multiple-sample track destination |
| RC-087 | 021 | Audition entry routes and last-selected lane per track |
| RC-088 | 022,023 | Copy-context entry and alternate-take selection origins |
| RC-089 | 022 | Take-lane editing context and both Session transfer entries |
| RC-090 | 025 | Actual manual crossfade command complements automatic history |

[Adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/adoption-r4.json)
retains13partialgroups: nine selected actualinput histories, G05/G11 positive
prerequisite overlays only, G12 recordedcolor/Q031 research andG13 posttarget API
route unadopted. True RC054 BOTH Drawrelease/main-selection-click,RC052BOTH
independence directions,RC048unused,RC053emptyskip,RC055/056highlights andRC057
autofade remain intact. Explicit manualfade command is separate from automatic
fade proof; fourms remains documentary, curve/rounding/shortclip outputs U.

[Current fixture overlay](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/fixtures-r4.json)
requires genuine completed NONEMPTY takes and BOTH independent takes/maincomp
productive before absence/reuse/loss/order; audio requires each NONZERO nonmuted
output, UI-only gestures require no sound/hardware. Actual matched highlights
precede mismatch inquiry; sharedTakeId/sample alone is insufficient. Sequential
TRACK destinations for multiple samples are not sequential take lanes or a
multiMIDI-distribution law. Source clip independence is not physicalmedia copies.

Allnew documentary/actual pairs andall90current actualpairs remain nullU, with
no original/candidate execution. Unknown allocation/partialpasses/undo-media/restore/
cancel/teardown/timing/default/RNG/codec/file outcomes remain. No fullgroup, profile,
Recording or product completion; review pending AS OF AUTHOR FREEZE.

Inspect [current read-only check](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/check-r4.py)
before `python3 -B analysis/ableton-live-12.4.3/full-spec-v1/recording/check-r4.py --check`.
[Seal](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manifest-author-r4.json)
preserves26oldfiles andallsource/review pins; oldR3 providers/seals/consumers stay
exactasof, no oldtool/main/inventory/parser/decode/replay/adapter or newcapture.
No runtime/UI/audio/MIDI/hardware/network/install/configuration/candidate action.

## Bounded Recording/Comping family routes — 2026-10-20

Pending independent structure review: [family-recording-comping-routes-v1](../../analysis/ableton-live-12.4.3/full-spec-v1/family-recording-comping-routes-v1/structure.md) reconnects currentR4's34clauses/90unchanged records to approved I09record-into-Arrangement, component, Playback/Transport/Mix/Arrangement context. The ledger has282bounded predicate/context rows:8S retained-inventory routes,274with no established route,0X. Counts are inventory only, not grades or a whole-family/product denominator; all90actualnullU remain, with fourartifact-only roles separate from86appU,81oldobjects exact and9newnullhistories.

Metadata-first discovery exceeded32tables and retained no rows; Root approved a semantic32type scope/eight explicit owner/unbound exclusions. Its fixed census fits allcaps:130selectedslots(16largeheaders with leading3construction/lifetimeprefix),75stores,68aliases+68memberships,103call+30indirect rows.447selectedDATArows retain exact source line/byte/raw identities. Names/prefixes/fields/callbacks and existing registry landmarks are navigation, not public command/receiver/writer/clock/host delivery. Native recording, Capture heuristics, allocation/matching, Undo/Save/audio-file/failure transitions remain unknown. No new C/native/provider/binary/decoder/original/harness/model/comparator/fixture/build or old-script import occurred; no new site credit follows.

The38-blockComping-only audit and earlierRecordingmanual reviews retain their exact partial scopes. Existing90case pointers without additional case, numeric or helper padding preserve explicitOff AFTER productiveenabledRC021, BOTH NONEMPTYtakes/maincomp, EACH NONZEROnonmuted audio, actual matched highlights, separate manual/auto fade histories, sequentialTRACKmulti-sample destinations and CMP-Q01–06/Q031/posttargetAPI guards. Source/package facts close no recording action or runtime grade. Root owns sealing/shared integration and independent review.


## Recording/comping family route review approval — 2026-10-20

Root read/adopted the complete [independent structure review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-recording-comping-routes-v1-review.json) (`de4380735678192cce62110d04fe3fd66fe07454e0ee3e102ed85004dbdf8986`). Manifest `2b9c150e9c4fb5e381d43d420aa6250213d674fcaa0e6cd29f18aee25610525c` binds17payloads/1,012,044bytes. All34clauses/282bounded predicate-context rows/90case pointers and447selected raw metadata identities were checked. Eight retained-inventory S rows remain distinct from274unknown routes/zeroX; four artifact-only roles are distinct from86application cases. All90actual outcomes stayU,81oldobjects exact/nine new null histories. RC076 aliases the existing REQ023 cancellation unknown; RC077 malformed lane/TakeId-open stays explicit unresolved case-only context, not a new normative predicate.

Fresh semantics cover all34current clauses/282contexts/all90actions and selected R4 safeguards. Mechanical24manual-section/38Comping-block/33inherited-edge checks do not rederive whole Recording/Comping source semantics; the complete38-block Comping audit remains inherited and partial. Thirty-two primary tables/130selectedslots,75stores,68aliases plus68memberships and103call/30unresolved indirect rows are bounded metadata;16large prefixes retain only leading-three construction/lifetime slots and eight owner/unbound scopes are explicitly excluded. Forty-six pins/16negative controls passed;19,361research-prefix bytes stayed exact.

Productive enabled-then-explicit-Off scene history, NONEMPTY takes/maincomp, independently NONZERO audio, matched highlights, separate manual/auto fades, sequential TRACK destinations and CMP-Q01–06/Q031/posttarget guards remain required. Names/stores/registries do not join actual recorder/materializer receivers, clocks, writer/media, Undo/Save/reopen, host or failure/lifecycle behavior. No native body/original execution, new resolved site, clause/case/release/grade or family/product closure follows. Earlier pending prose is author history.
