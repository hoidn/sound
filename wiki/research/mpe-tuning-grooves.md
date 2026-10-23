---
id: RESEARCH-MPE-TUNING-GROOVES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 5
target: Ableton Live 12 Suite 12.4.3
---

# MPE, tuning and groove evidence

## Question and canonical owners

Which MPE editing/routing, tuning and groove operations are documented, and
which are established for installed Live 12.4.3? Three distinct user tasks have
separate behavioral owners: [MPE workflows](../specs/mpe-workflows.md),
[tuning systems](../specs/tuning-systems.md) and
[groove workflows](../specs/groove-workflows.md). This is an analyst F-04 packet
under [ADR 0005](../decisions/adr-0005-full-live-specification-coverage.md), not
an implementation/release packet. Root owns shared navigation, inventory,
coverage, questions and append-only log updates.

Canonical [note storage](midi-note-storage.md), [MIDI editing/tools](midi-editing-tools.md),
[Warp](warp-markers.md) and [automation](automation-envelopes.md) were consulted
before sources. They retain note/expression file validation, ordinary note/tool
editing, marker mapping and ordinary automation respectively. New MPE prose
does not establish a CC-to-semitone codec or borrow automation's interpolator.
Groove commit creates marker/note edits but does not duplicate their format
contracts. Tuning UI changes do not specify the full browser/export/device host.

## Sources and capture limitations

Official manual captures are unchanged HTML fetched 2026-10-19; publication/patch
revision is unspecified beyond Version 12. These establish D12 documented
behavior; **every detailed exact-build 12.4.3 behavioral outcome remains U**.
Numbered text retains the chapter body then manual navigation; only body lines
identified in the specs are used. Images and diagrams were not inspected.

| Source | Official URL / retained HTML | SHA-256 |
| --- | --- | --- |
| SRC-MTG-EDITING-MPE | [Editing MPE](https://www.ableton.com/en/live-manual/12/editing-mpe/) / [capture](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/manual-12-editing-mpe-2026-10-19.html) | `11d135bdf08d97e4b1b6d4c8d5f4c8dd30b44aaf5dbe60bf5638ca2c1633568e` |
| SRC-MTG-USING-TUNING-SYSTEMS | [Using Tuning Systems](https://www.ableton.com/en/live-manual/12/using-tuning-systems/) / [capture](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/manual-12-using-tuning-systems-2026-10-19.html) | `90922bd082d31f1c383ceaae31aaece094e5cc769f601380cf7f50e10743eddf` |
| SRC-MTG-USING-GROOVES | [Using Grooves](https://www.ableton.com/en/live-manual/12/using-grooves/) / [capture](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/manual-12-using-grooves-2026-10-19.html) | `b8cb67fd3b8c435891594be31e2b14aebbbe1647c161aec8810c25b8754cad89` |

[sources.json](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/sources.json)
retains URLs/date/hashes/headings. [capture.py](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/capture.py)
uses installed BeautifulSoup and standard library only, refuses differing existing
capture bytes and runs no original code. The current manual is not a 12.4.3
runtime observation, even where schema terms match.

Three official support articles resolve concrete documentary gaps: matching MPE
bend ranges, tuning receiver prerequisites and ASCL directives. Direct HTTP
requests returned 403; those failures are retained in
[supplement-sources.json](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/supplement-sources.json).
The web tool could read the pages. Its exact **rendered response**, not raw HTML,
is retained in [help-rendered-web-2026-10-19.txt](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/help-rendered-web-2026-10-19.txt),
SHA-256 `6bf5a4559fab3edcd92c86c796ab65fc8dcb202e40bb37d2ab3bf495fbed8610`.
Each article restarts its embedded L numbering. Hashing that response establishes
retained text identity, not the publisher's original byte identity. Navigation,
tool citation markup and crawl labels are not original behavioral evidence.

| Supplemental source | Official URL | Exact retained locator / scope |
| --- | --- | --- |
| SRC-MTG-MPE-FAQ | [MPE in Live FAQ](https://help.ableton.com/hc/en-us/articles/360019144999-MPE-in-Live-FAQ) | Troubleshooting, L103–106: matching controller/instrument bend ranges; no codec/default law |
| SRC-MTG-TUNING-FAQ | [Tuning Systems FAQ](https://help.ableton.com/hc/en-us/articles/11535414344476-Tuning-Systems-FAQ) | L37–53: retune/bypass; L54–81: receiver range, Drum Synth exception, reference/KBM and saved tuning. Detailed MIDI export claims routed to export owner |
| SRC-MTG-ASCL-SPECIFICATION | [ASCL Specification](https://help.ableton.com/hc/en-us/articles/10998372840220-ASCL-Specification) | L12 identifies directives as of Live 12.1; L50–157: encoding, reference, names, ranges and documentation. Not runtime parser evidence |

## Installed-package corroboration

Pinned source: [installed 12.4.3](sources/ableton-live-12.4.3.md), currently under
`/home/ollie/Ableton Live 12 Suite.app`. The already captured latest schema
`12.0_12402.txt` hashes to
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
[schema-presence.json](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/schema-presence.json)
retains exact classes/line ranges. This is S-presence, not a supported new S
behavioral law. No native decompilation or original-code execution was needed.

| Surface | Exact pinned schema locator | Direct observation and limit |
| --- | --- | --- |
| MPE routing | MpeSettings, 5183–5187 | Zone and first/last note-channel declarations. Does not establish zone enum, valid range, channel allocation, negotiation or UI |
| Groove assignment/pool | ClipGrooveSettings 1246–1248; Groove 2742–2754; GroovePool 2755–2760 | Assignment, clip, grid and Quantization/Timing/Random/Velocity vocabulary. Does not establish control units/defaults, pairing or random law |
| Tuning | NoteTuning 5627–5630; TuningRatio/TuningSystem/TuningSystemScale/TuningSystemScaleInterval 8268–8296 | Note intervals, reference, range, names/scales/source/link vocabulary. Does not establish note-frequency math, indexing or parser behavior |

Three shipped files are retained byte-for-byte and described in
[shipped-examples.json](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/shipped-examples.json).
The capture performs gzip/XML decoding only for inspecting data. Historical
Creator attributes are explicitly preserved; being shipped in 12.4.3 does not
make a preset a runtime output from 12.4.3.

| File | Retained SHA-256 | Exact observed content / limit |
| --- | --- | --- |
| Core Library/Grooves/Utility/Quantize 8.agr | `9bdf02b9e0c7c5cc64e08ff88636479a42fa8716c4d69a4b8f9574013528559a` | [AGR](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-example.agr) and [decoded XML](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-example.agr.xml): Creator Live 10.1.6; root Groove/Clip/MidiClip; Grid1, Quantization100, Timing/Random/Velocity0. No enum-domain or decoder/runtime inference |
| Core Library/Tunings/EDO/12-TET (EDO).ascl | `6fed7cb55f6bd03ab55fdee3ce7ff6847d61ff9f27a8090f6e37d69af05a10ea` | [ASCL](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-example.ascl): twelve pitch entries, NOTE_NAMES, REFERENCE_PITCH 3 9 440.0 and LINK. Its text describes scale-awareness limitation; no engine/parser is executed |
| Core Library/Defaults/Instruments/Drift.adv | `5372a5f3fcb5abc8c769b40f006a09f83f517103ce0d6913693627894875a393` | [ADV](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-device-example.adv) / [XML](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-device-example.adv.xml): Creator Live 12.4d1; MpePitchBendUsesTuning true and Global_NotePitchBend/Manual true. Neither proves application defaults or output codec |

## Documentary conclusions and open context

Observed documentation gives per-note editor gestures, independent grid,
expression movement/stretch and output zone configuration. It does not specify
numeric UI bounds/codec, curves, channel reuse, sounding-note mutation or cleanup.
Chapter 12's folded Pitch visibility and tool chapter's optional Pitch Bend lane
are a context question: matching panel/control/preconditions are unestablished.
The neighboring [MIDI tool visibility issue C3](../specs/midi-editing-tools.md#contradictions-and-incomplete-behavior)
stays canonical; this packet does not declare another contradiction from shared
terminology. MPE-027 retains the unresolved context comparison.

Tuning documentation separates reference-label edits (no audible change) from
reference-frequency edits, destructive automatic retuning from index-preserving
changes, and track bypass from global tuning. ASCL format text provides useful
input-domain/error clauses without proving parser refusal UI or recovery. The
manual's broad built-in-instrument support is qualified by support FAQ's Drum
Synth exception; individual device reconciliation remains U. No root-frequency
formula, tie-break or retune collision-survivor law is invented.

Groove documentation supports pre-groove straight Quantize endpoints, negative
velocity emphasis, global intensity, Warp prerequisite, extraction playing
portion and commit resetting assignment. Exact groove correspondence, Timing
blend, Random law, velocity arithmetic and Warp Marker generation remain U.
Per-voice random fluctuation does not imply statistical independence or that
every pair differs each trial; cross-voice/cross-clip correlation remains U.
GRV-007 deliberately has no numeric/statistical pass oracle.

## Authored cases and frozen review packet

The original [shared R2 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/cases.json)
remain83 exact unexecuted records across53requirements: MPE27/18requirements,
Tuning32/21 and the historical Groove24/14. Their52D12 documentary proposals and
31U records remain exact; every exact-target grade remains U. That catalog stays current for unchanged Tuning32 and historical for the original
MPE27/Groove24. Current MPE is separately selected through
[mpe-cases-r3.json](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-cases-r3.json):
50 records (27 old verbatim plus23 new;39 D12 documentary contexts/11 U).
Current Groove is selected separately through
[groove-cases-r3.json](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-cases-r3.json):
34 records (24 old verbatim plus10 new;23 D12/11 U). The logical current union
is116 distinct cases (MPE50+Tuning32+Groove34) across53 requirement IDs. Neither
complete selected catalog is added again to the original83, and original IDs are
not counted twice. MPE retains18 IDs with nine bounded refinements; Groove retains
14 IDs with only001/010/014 refined. Legacy expected/comparator strings are documentary proposals, never actual
results. All current actual outcomes remain null/U/unexecuted. No S/X behavioral
case, reference execution or compatibility pass is added. Partly ungraded fields
never become passing outcomes; all operational/source/context gaps remain open.

[author_cases.py](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/author_cases.py)
generates data and checks finite IDs/counts; it is analysis tooling, not candidate
implementation. [validation-author-r2.json](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/validation-author-r2.json)
records focused metadata/link/requirement/case/source integrity checks.
[manifest-author-r2.json](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/manifest-author-r2.json)
pins the original combined R2 snapshots and payloads, including frozen copies
of the four Markdown pages. Its separate partial review is retained. Current
GrooveR3 routing below does not rewrite those payloads or expand that review.

## Review corrections and retained revision 1

The independent [revision-1 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mpe-tuning-grooves-review.json)
requested a nonidentity Commit case. GRV-010 now explicitly sets MIDI starts
0.1/0.6 beats, Base 1/8, Quantize 100% and Timing/Random/Velocity zero; G3's
nearest-grid endpoint rule and G4's writing result support committed positions
0/0.5 with assignment None. The audio subcase grades assignment None only:
existing appropriate markers need not change and marker deltas remain U.
REQ-GROOVE-007 now says separately per voice and explicitly leaves statistical
independence/correlation U. MPE-005 requires three distinct admissible interior
Pressure UI values symbolically; the numeric domain remains unestablished.
The [response](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/review-response-author-r2.json)
records all three dispositions. Counts, grades and source evidence are unchanged.

Before editing, all 26 original payloads and all four original snapshots were
verified and copied into the [revision archive](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/revisions/author-r1/manifest-author-r1.json).
That archived manifest resolves its payload paths inside the archive and hashes
to `548d47418b71b5e85b25a11cea01bbe37d37268b53ae91a6ec6c20fe9c3a9cce`.
The original root `manifest-author-r1.json` bytes are also unchanged; its old
payload inventory describes revision 1, whose complete matching bytes are now
resolved under `revisions/author-r1/`. Those retained R2 files remain pinned by
revision2; current Groove-only additions use their own successor seal below.

No runtime, original-code/hardware execution, candidate conformance, tooling
installation, public publication or clean-workspace isolation was checked.
T1.6 remains pending; Amp/Cabinet host emulation stays blocked. They are
unrelated to completing this independent documentation packet.


## Groove-only R3 source-audit adoption

The [compact full retained Groove audit](../../analysis/ableton-live-12.4.3/full-spec-v1/groove-source-audit/README-r2.md)
and [independent focused final review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/groove-source-audit-review-final.json)
retain32 whole-block judgments/17literalresources against14actualclauses and
24fullactions/commonfixture. This is not32per-claimfacets or chapter completion.
GSA-REVIEW-001 clears exactly two misleading primary Groove012/GRV012 references
from Rack-chain advice; its correct selected Racks022/RCK046 route remains. No
new Rack extraction case or algorithm is adopted here. Source/proposals otherwise
stay exact. The original Groove source is249336bytes/SHA
`b8cb67fd3b8c435891594be31e2b14aebbbe1647c161aec8810c25b8754cad89`,
dated2026-10-19only; exactcaptureUTCunknown, distinct from audit/authorUTC.
Clip062–064 has its own retained Version12 URL/UTC/hash, not new capture or target
parity. All32Grooveblocks and selected3Clipparagraphs/1Rackclause+case were read;
no other MPE/Tuning source semantics, pixels or linked destinations are reopened.

Nine groups receive bounded source-context cases: separate pool visibility,
actual poolSave/Hot-Swap, Base variants without new numeric law, productive
Timing/Velocity suppression, productive Warp history, Global Amount entrypoints,
both groove-to-MIDI routes and genuinely edited re-extraction, positive-velocity
audio Commit envelope and actual chooser/Hot-Swap gestures. Requirements001/010/
014 now retain exact chooser/conditional envelope/clip-and-pool loading roles;
the other eleven rows and all24 old Groove records remain exact. Exactfinite
005/010/013 arithmetic and MTG review limits are not replaced. NewGRV032 requires
positive velocity influence plus a nonflat prior clip-volume envelope for overwrite;
old010 Quantize100/Velocity0 plus audio assignmentNone is a different history.
Marker mutation, velocity-to-gain, point/curve, audio/file/time results remain U.

The [ten-group ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-adoption-r3.json)
keeps GSA-G09 Random texture as research recommendation only; no new case or norm.
Original007/023 numerical/statistical unknowns remain exact. No guaranteed
noncoincidence, independent stream, correlation/seed/distribution or sound-quality
promise. Missing/failed actual control, effect/source/output or Save/Swap positive
history is U, never passing zero/Warp/cancel/no-effect. Clip/pool replacement does
not define all sharing clips, duplicate identities, merge/deletion or persistence.

[Current actual-status](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-actual-status-r3.json),
[exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-delta-r3.json)
and [preservation](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-prior-files-r3.json)
retain all61 old files/seals/reports/archive in place. Shared83cases and current
MPE/Tuning canonicals are untouched; their old immutable R2 providers remain
usable by separately authored MPE/Tuning audit work. Only current Groove and this
shared research routing advance. [Consumer history](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-consumer-impact-r3.json)
records30 qualified old-hash occurrences across21 files as as-of provider/archive/
review metadata, not21 live dependency failures. Two occurrences in one active MPE-audit author
input file are explicitly as-of only, not immutable dependencies. No consumers/oldcheckers or
historical adapters run; current checks own immutable inputs/delta/pointers/nulls/
fixtures/snapshots/Browser IDs. No generic compatibility resolver is introduced.

[GrooveR3 author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-manifest-author-r3.json)
retains this partial increment. **AS-OF AUTHOR FREEZE:** independent Groove owner
review is pending; current status belongs to the [spec index](../specs/index.md).
The author reviewed the source audit, which is not self-approval of this normative
adoption. Root supplies separate review/shared integration. All actual results
remainU/null/unexecuted; no original/vendor/native/runtime/audio/MIDI/editor/input/
hardware/network/account/install/candidate or source capture operation occurred.


## MPE-only R3 adoption and shared research revision 4

This shared research revision routes MPE R3 alongside the already separately
reviewed GrooveR3; every GrooveR3 payload/snapshot/seal and both Groove/Tuning
canonicals remain exact. Historical Groove-author-freeze wording above retains
its as-of disposition; [spec index](../specs/index.md) owns current review status.
The [MPE source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-source-audit/README.md)
and its [independent partial review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mpe-source-audit-review.json)
retain all66 chapter blocks/110 facets,28 literal resources and13 proposals.
All66 source texts,18 old clause rows,27 complete old actions,13 proposals and
selected14 Glissando/LFO blocks were read for this bounded adoption; no full
MIDI Tools/FAQ/device/controller chapter audit, image pixels or destinations.
The MPE HTML is259102bytes/SHA
`11d135bdf08d97e4b1b6d4c8d5f4c8dd30b44aaf5dbe60bf5638ca2c1633568e`.
Capture date2026-10-19 only, exactUTCunknown; Version12 is not12.4.3 proof.
FAQ018 uses only the first rendered article L102–106, not publisher HTML or
full FAQ. Matching bend ranges do not select a universal±48 range.

The [13-group ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-adoption-r3.json)
adopts bounded role/input refinements and23 explicit missing actions, not all
outcomes. Nine old requirement rows refine exact entry/precondition contexts;
nine remain unchanged. All27 original MPE actions/fields are verbatim in the
separate50-case catalog; original shared83 remains byte-identical. NewMPE029
expression-record and048 plug-in-output probes remain U with all documentary
and actual comparators null. Other21 new cases are documentary D12 source
contexts; ten named UI roles have categorical documentary relations and13 new
cases have no documentary comparator. All50 actual outcomes are null/U/unexecuted.
No old numeric expected/comparator string is reclassified as a measurement.

True original005 a/b/c input,006 segment/Shift,007 tab/grid/save,010 move/x2,
014 enabled-default,015 allthree routes,016 two-track zones and0173..8 remain.
Old001's selected-then-enable action is not hot-enable proof; new028 enables the
controller before selecting it, as documented. Old014 saves/instantiates an
enabled default; it neither sends per-note input through a meter nor tests
plug-in output. Lowest blue track-meter dot, Control Bar generic activity and
actual per-note delivery remain separate. New disabled-default history does
not create an arbitrary plug-in, file/transaction/default-constructor law.

Offline clip edits require no controller/hardware/audio. Input/output/recording
or audible recipes require independently recognized nonzero per-note source,
actual accepted active route/receiver, relevant nonzero depth/gain and nonmuted
positive output when relevant before no-effect/bypass observations. Values a,b,c
and active editable expressions must be independently admitted; flags/names do
not substitute. Configuration-only dialog inspection requires no wire/audio.
Source grid-neighbor/create, relative/equal/scaling and fine-edit descriptions
supply no new numeric threshold, domain/codec, formula or interpolator. Literal
Pitch uses Alt Win/Cmd Mac, separate from Alt/Option curve gesture. Folded
over-note Pitch and optional Pitch Bend lane/C3 remain U in their unmatched
contexts. Underlying MED008/MED012 note operations and CV008 mode entry are
reused, not restated as new laws. Source device/Push2 and MIDI-thru examples
prove no exhaustive compatibility, fanout, voice capacity or wire delivery.

[Preservation](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-prior-files-r3.json)
retains all79 original packet files/seals/snapshots/reports in place without a
second whole archive. Exact before canonical snapshots retain MPE revision2
and shared research revision3. [Impact inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-consumer-impact-r3.json)
records23 qualified old-hash occurrences/21 external JSON files, including one
concurrent MIDI Tools audit author input explicitly as-of/non-gating. The other
22 occurrences/20 frozen files remain preserved. These are not21 current
regressions: snapshots, archive/provider records and review watches are historical.
No consumer/old validator, adapter or broad replay is changed/run. Current own
checks use immutable audit/provider/review pins, precise delta, sources/pointers,
retained positive/unsafe mutation fixtures, nulls, snapshots and exact18BrowserIDs.

[MPE author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-manifest-author-r3.json)
retains this partial owner increment and shared research revision4. **AS-OF AUTHOR FREEZE:** independent MPE owner review is pending; current disposition belongs to
the [spec index](../specs/index.md). Authoring this increment is not independent
approval of it. No source capture, original/native/vendor/UI/Max/API/runtime,
hardware/MIDI/audio/OS/account/network/install or candidate operation occurred.


## Tuning-only R3 adoption and shared research revision 5

All earlier research body text is preserved verbatim as-of its named revisions.
Its previous Tuning32/current-union116 routing is historical at this successor.
Current Tuning is now selected through [tuning-cases-r3.json](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-cases-r3.json):
43records,32exactoldplus11new,32D12/11U. Current logical union is127distinct
cases: MPE50+Tuning43+Groove34 across the same53requirement IDs; original83 is
not added again. Current MPE/Groove providers/canonicals and all97old packet
files/seals/reports remain byte-identical. Shared research body advances only
by this append and revision metadata; no MPE/Groove claim is rewritten.

The [Tuning full primary-source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/tuning-source-audit/README.md)
and [independent source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tuning-source-audit-review.json)
retain49blocks/68facets/32resources against21actualclauses/32actualactions.
Allprimaryparagraph/list qualifiers and all12proposals were read for this bounded
adoption, plus19matching renderedFAQ/ASCL ranges and35selected adjacent records;
no fullFAQ/ASCL/SCL/adjacentchapter or image/link-destination audit is claimed.
Primary HTML254421bytes/SHA90922bd082d31f1c383ceaae31aaece094e5cc769f601380cf7f50e10743eddf;
rendered support response SHA6bf5a4559fab3edcd92c86c796ab65fc8dcb202e40bb37d2ab3bf495fbed8610,
notpublisherHTML, with retained direct403. Capturedate2026-10-19only/UTCnull;
ASCLdescriptionasof12.1/currentVersion12 are not12.4.3 observations.

Fiveexisting rows refine explicit loaded-name-hover, browserviewmenu/triangle/
name-readout, Options entry and loaded MIDI I/O control contexts. Eleven actual
future case additions supply bounded input histories in12groups; Group10 only
retains existing qualified receiver config and selected external routes. True old
32TUNrecords remain exact, not reclassified as executed results. Three new named
UI entry/selection documentary pairs are nonnull; eight new pairs and allnew
legacy/actual outcomes are null. Sound, numeric tuning/range/parser/file/URI/
API/message/timing results remain ungraded/U. All43actual outcomesnullU/unexecuted.

Genuine productive control/load/save/import baselines precede absence or error.
For audible invariance/bypass, actual effective accepted tuning on a compatible
active unmuted nonzero route is required; loaded flags/ruler/package fields do
not prove sound. Onconfirmation precedes Offabsence, recognizedvalidUTF8import
precedes nonUTF8/duplicate-range, enabled-link/normalSave precedes no-link.
Settings/configuration-only observations need no audio/hardware. Failed positives
or absent recognized inputs are U. No native/original/API/parser/fixture/source
example, UI, hardware, network, website, file import/export or candidate ran.

Tuner010/011/012+DTU028 own FAQ Tuner-reference context, not TUN015. DrumSynth
exception and per-device support stayU. UI lowest/highest need not be frequency
extrema in nonmonotonic ASCL; SCL440near-middle is not12noteASCLindex69. SOURCE/
LINK metadata does not guarantee clickableURI; ASCLarguments do not supply API
dictionarykeys/units. No nearest/tie/survivor/cap-priority, tuning equation,
parser/format conformance, cancellation/fullUndo/recovery/default or lifecycle
closure.12groups remain bounded partial subsets, not every assertion adopted.

[Preserved old files](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-prior-files-r3.json),
[exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-delta-r3.json)
and [historical census](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-consumer-impact-r3.json)
retain33qualified old-hash occurrences in19files as-of; no consumer/oldvalidator
edit/replay or automatic adapter. Current own immutable source/audit/review pins,
delta, guards, snapshots and independent owner review govern.
[Tuning author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-manifest-author-r3.json)
will retain this bounded successor. **AS-OF AUTHOR FREEZE:** independent Tuning
owner review pending; [spec index](../specs/index.md) owns current disposition.
