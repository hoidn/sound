---
id: SPEC-TUNING-SYSTEMS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3; current Live 12 documentation, exact-build applicability unknown
---

# Tuning systems and controller layouts

## Scope and ownership

Canonical F-04 owner for Set tuning import, reference pitch and note range,
retuning, track bypass, controller layout and tuning's interaction with scale
awareness. Partial documented-domain draft only: D12 refers to retained current
official Live 12 documentation. **Every exact 12.4.3 behavioral grade remains U**.
The ASCL public format description identifies its directive set as of Live 12.1;
that statement is not proof that all parser paths behave as documented in 12.4.3.
S-presence observations establish shipped vocabulary/files only. No original
application, hardware, plugin or candidate was executed.

[MIDI editing](midi-editing-tools.md) owns note/scale editing commands and
generators. This page owns the tuning-induced visibility/disable and remapping
consequences. [MPE](mpe-workflows.md) owns MPE controller/channel configuration;
this page supplies the documented ±48-semitone prerequisite for tuning receivers.
[Note storage](midi-note-storage.md) owns note fields; no tuning-to-note/bend
serialization codec is inferred here. MIDI export, devices and browser have
their own owners; this page does not specify their full behavior.

## Inputs, units, state and comparison

Inputs: valid SCL/ASCL tuning, current Set clips, Retune Set option, reference
octave/note/frequency, note-range endpoints, per-track bypass and controller
layout. Frequencies are Hz; cents/ratios are tuning-file interval descriptions;
octave/index are tuning coordinates, not necessarily standard MIDI note names.
Default 12TET without a loaded file differs from a loaded 12-TET ASCL: the latter
still invokes tuning-mode UI restrictions.

Set tuning, physical clip note indices, displayed ruler labels, sounding pitch,
reference label/frequency, track bypass and input layout are distinct states.
Cases compare named UI/data fields and documented constraints. No DSP-frequency
tolerance, bend encoding, rounding, scale-degree arithmetic, nearest-note tie law
or note-frequency equation is assumed. Valid authored text inputs are parser
proposals, not independently loadable fixtures; retained shipped examples retain
their original bytes and are not generated reference outputs.

## Requirements

All rows are D12 with target U. T/H/A locators are in the analyst appendix.

| ID | Inputs / precondition | Observable transition and limits | Evidence |
| --- | --- | --- | --- |
| REQ-TUNING-001 | No loaded tuning; browse Tunings or add SCL/ASCL to a Places folder. | Default pitch system is 12TET. Core tunings are available in Tunings; user files appear under User tag. Hover/select shows description and number of notes per octave in Info View. Browser indexing latency/errors U. The same description is shown when hovering the name of a loaded tuning. | T1 |
| REQ-TUNING-002 | Double-click tuning in browser, or select+Enter; alternatively drag external SCL/ASCL into Tuning section. | Load tuning into Set. Browser operations open initially hidden Tuning section; view menu also opens it. Loaded tuning is saved with Set. Precise reference defaults, multiple drop ordering and missing-file behavior U. The browser view control menu opens the section; the triangle beside the loaded file name expands additional settings and Tuning displays the loaded system name. | T2 |
| REQ-TUNING-003 | Tuning loaded; view/hover/play piano roll note. | Ruler displays tuning notes rather than conventional MIDI pitches; hover reports pitch/frequency in Status Bar and piano-roll/keyboard audition produces specified pitch in a compatible setup. Exact pitch generation/error tolerance U. | T2 |
| REQ-TUNING-004 | Retune Set disabled; change/remove loaded tuning. | Existing piano-roll note positions/indices stay; labels/pitches follow new system and may sound different. No destructive-retune confirmation appears in this mode. Preserve note index does not imply preserved frequency. | T2, H2 |
| REQ-TUNING-005 | Enable Retune Set On Loading Tuning Systems and load/change tuning. The explicit entry is Options > Retune Set On Loading Tuning Systems. | Confirmation precedes retuning; existing notes are moved toward closest available pitches. Overlapping original pitches can map to one new pitch, deleting or shortening a note. Exact matching, ties, survivor, cancellation and bypassed-track treatment U. | T2, H2 |
| REQ-TUNING-006 | Load tuning with scale-aware clips/devices present. | Clip View/Control Bar Scale Mode choosers disappear and scale-aware devices' Use Current Scale is disabled. This applies also to loaded 12-TET tuning. Hidden scale data, previous enable-state restoration and device-specific fallback U. | T2, H3 |
| REQ-TUNING-007 | Expand Tuning section; change reference Octave/Note without changing Ref. Pitch/Freq. | Controls choose reference identity and update displayed frequency to match it without audible pitch change. Exact rescaled number and transient/controller output U. | T3 |
| REQ-TUNING-008 | Loaded tuning; change Ref. Pitch/Freq. | Adjust reference frequency, raising/lowering Set note pitches accordingly. This is the reference edit producing audible change; no global UI frequency control without a loaded tuning is asserted. Exact frequency mapping, limits and held-note transition U. | T3, H3 |
| REQ-TUNING-009 | Change Lowest Note or Highest Note's octave/pitch-class coordinates. | Editing one updates the other while preserving number of intervening notes. Domain limits, nonmonotonic-frequency meaning and endpoint clamping U except documented file-range rules below. | T3 |
| REQ-TUNING-010 | Save loaded tuning using disk button; optionally select link arrow. | Save current tuning as ASCL into browser Tunings. If linked page exists arrow can open related tuning site; absent link grays arrow. Save/overwrite/cancel, URI filtering and browser launch failures U. ASCL SOURCE/LINK metadata does not guarantee a clickable URI. | T3, A5 |
| REQ-TUNING-011 | Select tuning in section and press Delete. | Remove it and return to default 12TET. Note-position versus retuned-note consequences depend on Retune Set option, not an unconditional restoration of original pitches. Exact confirmation on removal and undo grouping U. | T2–T3, H2 |
| REQ-TUNING-012 | Loaded tuning; enable a MIDI track's Bypass Tuning. The track tuning controls appear in MIDI track I/O while a tuning is loaded; no converse unloaded-hide law is asserted. | Track ignores tuning, its clips show 12TET notes, and instruments/plugins receive original MIDI without retuning. Tracks containing Drum Racks automatically bypass tuning. Automatic toggle lifecycle after rack removal/nesting and layout interaction U. | T4, H2 |
| REQ-TUNING-013 | Choose All Keys / Black Keys Only / White Keys Only / Closest in Pitch to Keyboard. Use the MIDI track In/Out layout chooser with a tuning loaded. | Map tuning notes respectively to all keys, black keys centered at C#3, white keys centered at C3, or nearest keyboard pitches. Exact mapping tables, ties, out-of-range keys and incoming-channel behavior U. | T5 |
| REQ-TUNING-014 | Choose Custom Controller Layout, open ellipsis and edit valid layout. | Open Configure MIDI Layout; custom layout is saved/recalled with Set. Allowed map domains, duplicate/unmapped keys, apply/cancel/undo and output routing semantics U. | T5 |
| REQ-TUNING-015 | Use tuning with external hardware, plugin or Max receiver. | Receiver must support and enable MPE, with per-note bend range ±48 semitones for the documented path. Incompatible/range-mismatched setups can be out of tune; there is no required precise failure sound. Manual's general built-in-instrument support is qualified by FAQ's Drum Synth exception; individual device scope remains U. | T1, H3 |
| REQ-TUNING-016 | Import SCL intervals lacking a reference, ASCL, or paired KBM. | SCL intervals do not supply absolute frequency; Live generates a 440-Hz reference near middle of MIDI range. ASCL can carry reference; KBM is unsupported. Exact generated note choice is U except documented ASCL range positioning below; unsupported KBM UI response U. | H3 |
| REQ-TUNING-017 | ASCL extension text follows pitch list using ! @ABL directives. | Extensions are SCL comments; arguments use spaces, double quotes enclose spaces, UTF-8 is required. Files containing extensions with non-UTF-8 bytes must be rejected by a compliant extension parser. Extra initial ! disables a directive. Error UI and transactional recovery U. | A1 |
| REQ-TUNING-018 | ASCL REFERENCE_PITCH and NOTE_NAMES. | Reference arguments: octave integer -2..8, zero-based degree less than pitch count, nonzero positive frequency in Hz. NOTE_NAMES supplies one name per degree beginning at implied zero. Nonfinite, duplicate/missing/mismatched directives and out-of-domain handling U. | A2 |
| REQ-TUNING-019 | Optional ASCL NOTE_RANGE_BY_FREQUENCY or NOTE_RANGE_BY_INDEX. | More than one range directive is an error. Frequency bounds are 4..21000 Hz, max optional; index octave bounds -99..99, upper endpoint optional. Index form requires an earlier REFERENCE_PITCH. Range start is specified index or first note at/above minimum frequency; max is limited by 127 further steps, 21kHz and optional bound. Exact ties/cap priority and malformed reversal U. | A3 |
| REQ-TUNING-020 | No ASCL range directive. | General description centers available notes around A3 440Hz with 64 below and 63 above; twelve-note systems instead put pitch nearest A3 440Hz at index 69. Exact non-12-note center/tie and interaction with nonstandard explicit reference remain U. | A4 |
| REQ-TUNING-021 | ASCL SOURCE/LINK metadata and nonmonotonic tuning with index range. | SOURCE text describes origin; LINK describes URL and software may restrict direct access. Index bounds mean first/last tuning positions even when not lowest/highest frequency. UI safety policy, sorting/normalization and actual URI launch behavior U. | A3, A5 |

## Acceptance cases and lifecycle

The current [Tuning-only R3 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-cases-r3.json)
contains43 records:32 exact old TUN records plus11 future context actions,
32 D12 documentary proposals and11 U. Original shared83 cases remain unchanged.
Only three new named UI entry/selection documentary pairs are nonnull; all new
numeric, parser, file, audio, tuning and timing comparisons are null. Every
actual outcome is null/U/unexecuted, including old legacy expected strings;
the [explicit status](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-actual-status-r3.json)
separates documentary text from runtime evidence. True TUN003 audition/labels,
007 identity,008 direct frequency,009 both endpoints,010 Save,011 DeleteOff,
013 Black/White,014 Custom/edit/reopen,015 configuration,016 SCL and017–021
bounded format examples remain verbatim. TUN033–043 add bounded source actions,
not new tuning arithmetic, parser acceptance or a complete family.

TUN-022–032 cover malformed/truncated/unsupported files, numeric extremes,
reference ties, destructive retune collision boundaries, confirmation cancel,
undo/redo, save/reopen/source removal, custom-layout cancel, track/Set teardown,
held-note changes and device/bypass/scale restoration. The FAQ gives one
documented Undo recipe to return from temporary retuning; it does not establish
atomic rollback for every collision or dialog. Loaded tuning persistence and
layout persistence are supported clauses; recovery from failed writes and
all remaining settings/history persistence remain U. Documented immediate
effects specify no audio-block boundary, smoothing, note-on/off ordering or
mid-note safety guarantee.

Full-product gaps include SCL grammar/import normalization, ASCL duplicate and
unknown directives, encoding/BOM/quotes/errors, exact frequency/reference math,
numeric rounding/range limits, non-octave/nonmonotonic systems, retune ordering,
loss/collision/ties/expression consequences, nested racks/drums and MIDI effects,
all input-layout tables, retuned MIDI encoding/automation and transport/reconnect.
The general manual says all built-in instruments support tuning; the FAQ
qualifies software instruments with a Drum Synth exception. Per-device support
must be reconciled before a full coverage claim. MIDI export's documented loss
of tuning/MPE metadata belongs with export's owner; this draft adds no export
contract or original reference output.

## Analyst evidence appendix

[Research and hashes](../research/mpe-tuning-grooves.md) pins retained manual
HTML, rendered official support pages and capture limitations. T locators use
numbered `manual-12-using-tuning-systems.txt`; text from line 100 is navigation.
Images were not inspected. H/A refer to named sections of the retained
`help-rendered-web-2026-10-19.txt`; each embedded article restarts L numbering.

| Locator | Exact section / retained lines |
| --- | --- |
| T1 | Introduction, numbered text 3–18 |
| T2 | `loading-a-tuning-system`, 19–40 |
| T3 | `the-tuning-section`, 41–65 |
| T4 | `bypass-tuning`, 66–74 |
| T5 | `midi-controller-layouts`, 75–91 |
| H2 | Tuning Systems FAQ, Tunings with MIDI, L37–53 |
| H3 | Tuning Systems FAQ, Tunings with devices/About Tuning Systems, L54–81 |
| A1 | ASCL Specification, general extension notes, L12–62 |
| A2 | ASCL Specification, REFERENCE_PITCH/NOTE_NAMES, L65–83 |
| A3 | ASCL Specification, note range directives, L86–135 |
| A4 | ASCL Specification, no-range default, L105–114 |
| A5 | ASCL Specification, documentation directives, L140–157 |

Installed schema lines 5627–5630, 8268–8296 and the retained shipped 12-TET ASCL
corroborate feature/file vocabulary; the ASCL includes twelve entries, note names,
reference directive and link. That observation validates no parser, tuning engine,
mapping formula or user transition. Existing fields remain analysis evidence.

## Tuning-only R3 source-audit adoption

The [retained full primary-source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/tuning-source-audit/README.md)
and [independent partial source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tuning-source-audit-review.json)
reconcile49manual blocks/68facets/32literalresources. Only19selected rendered
FAQ/ASCL ranges and35adjacent records were reconciled, not full supplementary
chapters. Captured2026-10-19 is date-only, UTCunknown; current Version12 and
ASCLdescriptionasof12.1 are distinct from exacttarget12.4.3, which remainsU.

[The12-group ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-adoption-r3.json)
adds bounded actual selection/name-hover, view-menu/externaldrag/triangle,
keyboard-context, literalOptions, productiveScale/reference/save/link/bypass,
remaining layout entries and valid-before-error/range-format proposals. Five
rows refine explicit input/control roles; no new normative ID is introduced.
Group10 retains TUN015 receiver configuration and source qualification without
a duplicate case. Tuner010/011/012 and DTU028 own Tuner reference interaction;
FAQ Drum Synth exception and individual-device U remain. No universal MPE range,
receiver failure sound, package-field-to-UI or API dictionary law is inferred.

[Common future guards](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-fixtures-r3.json)
apply before grading any old or new proposal: actual effective tuning and a
working nonzero compatible route precede audible equality/bypass; productive
On-load confirmation precedes Off/no-popup; normal Save/enabled-link control
precedes absence; independently recognized valid UTF8 import precedes malformed
encoding/range trials. Configuration controls need no sound or hardware. Missing
input/readiness/capability or failed positives stay U. No actual input/file/
example is supplied, loaded, generated or executed by this analyst packet.

TSA-Q01–04 remain qualified source-context questions. SCL fallback440 near middle
is not twelve-note ASCL index69; nonmonotonic first/last is not sorted frequency
extrema. SOURCE/LINK metadata does not guarantee a clickable arrow or URI launch.
No nearest/tie/survivor/cap-priority, frequency equation, tuning/ASCL/API codec,
parser normalization/recovery, sound tolerance, default/history, cancellation,
full Undo/persistence/transport/rate/teardown law is newly graded.

[Exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-delta-r3.json)
and [preservation](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-prior-files-r3.json)
retain97old combined files and all old seals/snapshots in place. MPE50/Groove34
providers/canonicals and original shared83 are unchanged. [Historical consumers](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/tuning-consumer-impact-r3.json)
remain as-of, without automatic adapters or old-checker replay.
**AS-OF AUTHOR FREEZE:** independent Tuning owner review pending; [spec index](index.md)
owns current disposition. Authoring the source audit is not independent approval
of this owner adoption. No full source-topic, product, release or runtime completion.
