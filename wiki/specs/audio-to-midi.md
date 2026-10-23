---
id: SPEC-AUDIO-TO-MIDI
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3
---

# Audio-to-MIDI conversion workflows

## Scope and observability

This partial owner covers selected audio-clip Slice and Harmony/Melody/Drums
conversion commands. [Simpler](device-simpler.md) retains its instrument-context
slice/convert commands; [racks](device-racks.md), [MIDI editing](midi-editing-tools.md),
[Warp](warp-markers.md), [note storage](midi-note-storage.md) and
[project/media](project-media-workflows.md) retain their narrower action/format
contracts. Same command words do not erase different input contexts.

D12 means current Version12 documentation with exact12.4.3 applicability U.
No original code, source audio, conversion, application or candidate was executed.
No fixtures or reference output supplied. Observe menu/dialog eligibility and
new track/clip/rack/note/source-region relations; do not substitute native task
classes for user-visible requirements. Algorithms and numeric tolerances remain U.
See [research evidence](../research/audio-to-midi.md).

## Requirements

### REQ-AUDIO-TO-MIDI-001 — Command eligibility

**D12; exact-build U.** Selecting an audio clip exposes Slice and Convert Harmony/Melody/Drums commands in Create or clip context menu. Multi-selection, frozen/group/return/video/take-lane and unsupported source eligibility remain U. The four named entries are Slice to New MIDI Track, Convert Harmony to New MIDI Track, Convert Melody to New MIDI Track and Convert Drums to New MIDI Track; each is documented through either Create or the selected clip context menu. [Source converting-audio-to-midi](#source-converting-audio-to-midi).

### REQ-AUDIO-TO-MIDI-002 — Slicing choices

**D12; exact-build U.** Slice opens a dialog with beat-resolution, transient or Warp Marker divisions and slicing-preset selection. Slicing partitions source time rather than recognizing pitch. Exact division counting, first/last markers and boundary rounding remain U. Choose the top division chooser’s beat-resolution, transient or Warp Marker branch and the Slicing Preset chooser before clicking OK for an independently admitted nonempty plan; no exact division list or count computation is added. [Source slice-to-new-midi-track](#source-slice-to-new-midi-track).

### REQ-AUDIO-TO-MIDI-003 — Slicing limit

**D12; exact-build U.** The slicing workflow prevents proceeding when the chosen plan would exceed128 slices; lower resolution or smaller selected region can reduce the count. This is the slicing-command limit, not a blanket cap on arbitrary rack chains. Exact counting and other eligibility errors remain U. [Source slice-to-new-midi-track](#source-slice-to-new-midi-track).

### REQ-AUDIO-TO-MIDI-004 — Slicing presets and warped timing

**D12; exact-build U.** Slicing presets include supplied templates and user templates from the User Library Defaults folder. Preserve warped timing retains Warp timing changes; disabled follows raw source timing instead. Exact field/default precedence, resampling, fades and audio equality remain U. [Source slice-to-new-midi-track](#source-slice-to-new-midi-track).

### REQ-AUDIO-TO-MIDI-005 — Sliced result structure

**D12; exact-build U.** On successful Slice confirmation a new MIDI track contains a MIDI clip with one chromatically ordered note per slice and a Drum Rack with one chain/Simpler per slice. Each chain responds to its corresponding note and loads the corresponding source region. Starting pitch, note lengths/velocities, media copying and exact reference/boundary representation remain U. [Source slice-to-new-midi-track](#source-slice-to-new-midi-track).

### REQ-AUDIO-TO-MIDI-006 — Slicing macros and sequence

**D12; exact-build U.** Mappings come from the chosen slicing preset; supplied examples include envelope/loop/crossfade controls. A mapped macro adjusts corresponding parameters across the Simplers. Playback triggers slices in original sequence and selected/source timing; exact sample equivalence and processing duration remain U. [Source slice-to-new-midi-track](#source-slice-to-new-midi-track).

### REQ-AUDIO-TO-MIDI-007 — Resequencing and per-slice effects

**D12; exact-build U.** Editing slice notes or swapping rack pad note mappings can reorder playback. Per-chain effects process individual slices; selected chains can be grouped into a nested rack and effects placed after it for shared processing. Generic note/rack operations remain owned by their existing contracts. For the documented subgroup entry, multi-select the slice chains in the Drum Rack chain list, press CtrlG (Win) / CmdG (Mac) to form their own nested Rack, then insert the effects after that sub-Rack. [Source resequencing-slices](#source-resequencing-slices). [Effects source](#source-using-effects-on-slices).

### REQ-AUDIO-TO-MIDI-008 — Harmony result

**D12; exact-build U.** Harmony extracts pitched polyphonic content into a new MIDI track/clip with a piano-sound Instrument Rack. It is note recognition and resynthesis, not playback of the original waveform. Exact detected pitches/times/velocities, polyphony and default preset identity are U. The supplied piano-sound Rack role above is qualified by an independently known factory conversion history without a custom Harmony default override; custom defaults may instead use a single instrument. The instrument can be replaced through an independently admitted existing replacement route; no replacement gesture, preset identity or custom-default selection law is specified here. [Default-history qualification](#source-conversion-default-qualification). [Source convert-harmony-to-new-midi-track](#source-convert-harmony-to-new-midi-track).

### REQ-AUDIO-TO-MIDI-009 — Melody result

**D12; exact-build U.** Melody targets monophonic pitched audio, creating a new MIDI track/clip with a synthesizer Instrument Rack. Its Synth to Piano macro spans analog-style synth/electric-piano character. Exact detection, macro mapping and preset/DSP identity remain U. The supplied synthesizer Rack and Synth to Piano roles above are qualified by an independently known factory conversion history without a custom Melody default override; custom defaults may instead use a single instrument. The instrument can be replaced through an independently admitted existing replacement route; no replacement gesture, preset identity or custom-default selection law is specified here. [Default-history qualification](#source-conversion-default-qualification). [Source convert-melody-to-new-midi-track](#source-convert-melody-to-new-midi-track).

### REQ-AUDIO-TO-MIDI-010 — Drums result

**D12; exact-build U.** Drums extracts unpitched percussive rhythm into a new MIDI track/clip and preloaded Drum Rack, attempting kick/snare/hihat classification. No perfect classifier or exact MIDI key/sample/velocity assignment is promised. [Source convert-drums-to-new-midi-track](#source-convert-drums-to-new-midi-track).

### REQ-AUDIO-TO-MIDI-011 — Transient influence and quality

**D12; exact-build U.** Convert uses source transients for note divisions; changing those markers can alter conversion. Clear isolated attacks and uncompressed audio are recommendations, not guaranteed detection. Wrong-source-class conversion may add notes; reconstruction/precision/recall, onset tie, polyphony and lossy-codec effects remain U. [Source optimizing-for-better-conversion-quality](#source-optimizing-for-better-conversion-quality).

### REQ-AUDIO-TO-MIDI-012 — Recognition algorithms

**U; exact-build U.** Pitch/onset/classifier thresholds, tuning/reference pitch, amplitude-to-velocity, overlap/length, silent/ambiguous/invalid source behavior and deterministic repeatability have no finite target oracle here. Retained native task names do not supply a full recognition contract. [Source convert-harmony-to-new-midi-track](#source-convert-harmony-to-new-midi-track).

### REQ-AUDIO-TO-MIDI-013 — Timing and source ownership

**U; exact-build U.** Tempo/meter/warp/loop/region/selection changes during processing, source preservation, routing/monitoring, launch ownership, undo grouping, error or cancellation and result placement have no complete oracle. [Source slice-to-new-midi-track](#source-slice-to-new-midi-track).

### REQ-AUDIO-TO-MIDI-014 — Files persistence and teardown

**U; exact-build U.** Save/reopen, sample copy/collect, missing files, malformed audio/preset, CPU/memory/disk failure, cancellation at progress boundaries and device/Set/application teardown require exact outcomes beyond normal documented creation. [Source converting-audio-to-midi](#source-converting-audio-to-midi).

## Cases and prerequisites

All37 [current case definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/cases-r3.json)
remain unexecuted/ungraded for the target. [Fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/fixtures.json)
need independently established nonempty plans/capabilities; missing prerequisites
yield U. No exact count is inferred merely from output being tested. Unknown
probes have null oracles; input annotation is not recognizer expected output.
The29 historical records below remain byte-preserved in the old catalog. Their
`expected` text is documentary source context, not an actual target result. The
[current oracle policy](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/oracle-policy-r3.json)
keeps all37 actual pairs null/U/unexecuted. Numeric, timing, recognition, signal
and file comparisons have no executable oracle.

[Future prerequisites](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/fixtures-r3.json)
also apply to these unchanged historical actions. Before assuming supplied
piano/synth Rack or Synth to Piano roles in ATM015/016, independently establish
the matched factory/no-custom conversion-default history; F4 input validity
alone does not establish it. Custom Harmony/Melody defaults can be single
instruments. Before any preview, processing, timing or negative contrast, require
genuinely observed NONEMPTY generated notes plus independently nonzero active
instrument/effect contribution through nonmuted output. A nominal enabled flag
or empty result is insufficient; unavailable prerequisites yield U/unexecuted.
This does not promise nonempty conversion for every input.

| Case | Requirement suffix | Kind | Action | Predicate or unknown |
| --- | --- | --- | --- | --- |
| ATM-001 | 001 | positive | F1: select one valid audio clip and inspect Create plus clip context menu | Four documented slicing/conversion command choices available under applicable clip conditions |
| ATM-002 | 001 | negative | F1: select MIDI clip, multiple clips, frozen/take-lane/video/unsupported source separately | U: exact menu eligibility/disabled-action outcomes absent |
| ATM-003 | 002 | positive | F1: select audio region, open Slice dialog and inspect division/preset controls | Beat-resolution/transient/Warp Marker modes and slicing-preset choice exposed; exact legal values U |
| ATM-004 | 002 | boundary | F1: compare clip start/end, repeated/same-time transients and Warp Markers; record proposed slice count | U: first/last inclusion, deduplication and boundary/count arithmetic absent |
| ATM-005 | 003 | boundary | F2: independently established valid prospective slice plan of129 regions; open Slice dialog | Proceeding blocked by over128-slice condition; exact displayed error UI U |
| ATM-006 | 003 | positive | F2: reduce selected source region or resolution until independently established count is below limit | Slice-count condition no longer bars proceeding; unrelated errors and exact count computation U |
| ATM-007 | 004 | positive | F3: supplied presets and correctly located user slicing template, open preset chooser | Both supplied and applicable user template sources participate; precedence/cache/corrupt templates U |
| ATM-008 | 004 | interaction | F1: nonidentity Warp timing, identical source region/plan/preset, compare Preserve warped timing on/off | On retains warped timing relation; off follows raw timing; exact note/sample positions and equality U |
| ATM-009 | 005 | positive | F2: successful confirmed4-slice plan with known ordered source regions | New MIDI track/clip with4 chromatically ordered notes and Drum Rack4 chains/4Simplers assigned corresponding slices; exact keys/times/velocity U |
| ATM-010 | 005 | negative | F2: examine generated source-region identities and chromatic order against independently retained slice plan | One corresponding source region per generated chain/note; sample copying/representation and byte equality U |
| ATM-011 | 006 | positive | F3: known slicing template maps one macro to distinct accepted nonzero controls on each of4Simplers; change macro | Mapped parameter on each included Simpler adjusts; exact mapping law U |
| ATM-012 | 006 | timing | F2: play generated slice MIDI clip with active nonmuted signal path and independently distinguishable slice signals | Slices trigger original order under specified timing; exact onset/audio/gap/overlap tolerance U |
| ATM-013 | 007 | positive | F2: swap two sequence notes or two pad mappings in separate copies | Order can be rearranged; generic edit semantics delegated to MIDI/rack contracts |
| ATM-014 | 007 | interaction | F2: add distinguishable supported effect to one slice chain; separately group two chains and place same effect after nested rack | Individual versus selected-subgroup processing placement available; effect waveform/rack law delegated |
| ATM-015 | 008 | positive | F4: Harmony on independently valid polyphonic pitched clip | New MIDI clip/track with Instrument Rack; piano preview identity/recognition output U |
| ATM-016 | 009 | positive | F4: Melody on independently valid monophonic clip | New MIDI clip/track with Instrument Rack and documented Synth to Piano macro; exact macro/audio/detection U |
| ATM-017 | 010 | positive | F4: Drums on independently valid isolated percussion clip | New MIDI clip/track with Drum Rack; classification accuracy/keys/samples remain U |
| ATM-018 | 011 | interaction | F4: fixed source, separately add/move/delete retained transient markers before each Convert command | Documented transient influence only; exact generated note divisions/output U |
| ATM-019 | 011 | negative | F4: Harmony on monophonic source, Drums on mixed pitched/percussive source, slow fades and lossy copies | No perfect-accuracy or only-original-notes criterion valid; actual errors/additions/detection U |
| ATM-020 | 012 | numeric | F4: finite exact source notes with overlap/chords/pitch bend/tuning and known onset/level variants | U: detected pitch/time/length/velocity/polyphony/classification and tolerance absent |
| ATM-021 | 012 | boundary | F4: silence, near-silence, single attack, >128detectednotes for Convert rather than Slice, extreme accepted rates | U: empty/result/refusal/normalization; slicing cap not imported to recognition |
| ATM-022 | 012 | repeatability | F4: repeat same command/input/environment across restart and preset changes | U: determinism, hidden state and output equality absent |
| ATM-023 | 013 | timing | F1/F4: processing active while tempo/loop/region/warp/selection changes or transport starts/stops | U: snapshot/cancel/retry/source/result ownership absent |
| ATM-024 | 013 | undo | F2/F4: complete Slice or Convert, Undo/Redo and inspect tracks/devices/notes/files | U: history grouping, source preservation, media lifetime and complete restoration absent |
| ATM-025 | 013 | cancel | F1/F4: cancel Slice dialog; separately cancel recognition at independently recorded progress state | U: source/selection/partial results/files/dirty-state outcomes absent |
| ATM-026 | 014 | malformed | F3/F4: truncated audio or malformed slicing preset on disposable copies | U: refusal/repair/partial output/warning and original preservation absent |
| ATM-027 | 014 | error | F3/F4: missing source or unwritable/full destination/cache during processing | U: error/retry/fallback/rollback and source/result state absent |
| ATM-028 | 014 | persistence | F2/F4: save/reopen copied Set, collect media, relocate originals after result creation | U: generated reference/copy/default/state preservation absent |
| ATM-029 | 014 | teardown | F1/F4: close Set/application or delete source during active operation | U: worker termination, pending result/files/resources and recovery absent |

## R3 explicit future actions

These eight compound/reset definitions refine the five independently reviewed
audit groups. Four carry named UI-role documentary comparisons; ATM032,033,034
and037 have null documentary pairs and retain only source claims. All actual
expectations/comparisons stay null. No audio/template/recognized result or
executable fixture is supplied. Generic Rack/MIDI/device laws retain their
existing owners.

| Case | Requirement suffix | Kind | Action | Source claim only |
| --- | --- | --- | --- | --- |
| ATM-030 | 001 | entrypoint | On separate reset copies for EACH route, select the independently applicable nonempty audio clip for each of the four named commands. Actually invoke Slice to New MIDI Track, Convert Harmony to New MIDI Track, Convert Melody to New MIDI Track and Convert Drums to New MIDI Track once through Create and once through the selected clip context menu; retain each route/selection history. Use independently admitted plans/presets for Slice and appropriate independently valid polyphonic/monophonic/percussive inputs for the respective Convert commands. Do not infer an audio or recognition result from command invocation. | Selecting audio exposes the four chapter command roles through Create or clip context menu. |
| ATM-031 | 002 | dialog | On THREE separate reset copies with independently corroborated valid NONEMPTY plans, select a beat-resolution division, the transient division and the Warp Marker division respectively in the Slice dialog top chooser. Choose a separately admitted compatible Slicing Preset for each, then actually click OK. Record the named division/preset controls and conditional new MIDI track/clip/Drum Rack roles; exact plan arithmetic, keys, positions and media representation stay unknown. | Slice offers the three documented division kinds plus Slicing Preset selection; clicking OK precedes documented creation. |
| ATM-032 | 003 | recovery | Restore the SAME independently corroborated valid prospective129-region Slice plan before EACH of two separate trials and establish the overlimit blocked-proceed context independently. First lower the slice resolution to a separately corroborated below-limit nonempty plan and attempt confirmation. Reset to the original129 plan; separately select a smaller source region giving a separately corroborated below-limit nonempty plan and attempt confirmation. Hold unrelated admitted eligibility/preset state fixed; record outcomes without deriving the counts from the result being tested. | Chosen Slice plans over128 cannot proceed; lower resolution or smaller source region can reduce the plan. This is not a generic Rack or Convert-note cap. |
| ATM-033 | 004 | timing | With independently corroborated genuine nonidentity Warp and a productive distinguishable nonzero slice/instrument/nonmuted-output baseline, explicitly set Preserve warped timing ON and complete an admitted Slice. Reset to matched source/region/plan/preset state, explicitly set it OFF and complete Slice again. Retain both control histories and proposed warped-versus-raw timing observations; no numerical timing, audio, file or onset equality oracle is supplied. | Preserve warped timing On retains Warp timing alterations; Off follows original raw timing. Exact timing/audio/file comparisons remain null. |
| ATM-034 | 006 | factory-mapping | Retain exact compatible UNMODIFIED factory slicing-template bytes, distinct from ATM011 custom-template history. On independently admitted nonempty sliced results, inspect independently corroborated basic envelope, loop and crossfade example associations in the applicable factory templates; use separate admitted templates/control copies where needed rather than assume every template exposes every example. Actually change an admitted mapped Macro from a genuinely active nondegenerate starting state and inspect corresponding parameters across the included Simplers. Retain genuinely productive mapped-control/output baseline before any negative contrast; no macro index/name/range/curve or numeric/sound result is assumed. | Factory slicing examples include envelope/loop/crossfade mappings; a mapped Macro adjusts corresponding Simpler parameters. No exact factory template or mapping law follows. |
| ATM-035 | 007 | group-entry | Start from an independently admitted successful sliced Rack containing at least TWO actual distinguishable nonempty slice chains and productive supported processing through nonmuted wet/output. In separate platform-admitted reset copies, actually multi-select the two chains in the Drum Rack chain list, press CtrlG (Win) or CmdG (Mac) respectively to form their own nested Rack, then insert the admitted effect AFTER that sub-Rack. Retain chain selection/group/placement evidence; generic Rack mechanics and audio processing outcomes are not inferred from placement. | Multiselect slice chains, CtrlG Win / CmdG Mac creates their nested Rack; insert shared effects after it. |
| ATM-036 | 008 + 009 | replacement | On separate reset copies for Harmony and Melody, first establish the matched factory/no-custom conversion-default history and independently valid respective polyphonic/monophonic nonempty source. After admitted successful conversion genuinely observe NONEMPTY generated notes plus independently nonzero active instrument contribution through nonmuted output. Actually replace the instrument for EACH result using a separately independently admitted existing supported replacement route and compatible instrument; retain before/after device role and productive preview context. Missing route, factory history or productive result yields U/unexecuted. No replacement gesture, piano/preset identity or sound-equivalence law is invented. | Harmony and Melody supplied instruments can be replaced, qualified by factory/no-custom histories; DEV:B134–139 permits other custom result structures and is scope context only. |
| ATM-037 | 009 | macro-preview | Independently establish matched factory/no-custom Melody conversion-default history, admitted monophonic nonempty source, successful result with genuinely observed NONEMPTY generated notes and a genuinely nonzero active instrument/nonmuted-output preview baseline. Actually move the supplied Rack Synth to Piano Macro through separately admitted supported states and preview the result, preserving source/history and productive output. Retain its documented analog-style-synth/electric-piano character as source context only; no numerical endpoint, macro curve, exact piano/synth identity, audio, timing or detection comparator follows. | The supplied Melody Rack Synth to Piano Macro adjusts synth/electric-piano character, qualified by factory/no-custom history; no exact sound/mapping/numeric law. |

R3 advances the canonical revision directly from1 to3 because packet R2 only
corrected machine-readable source routing (including both evidence anchors for
requirement007); it changed no canonical clause, action or oracle. Exact R1
canonical providers, both old seals and all20 old packet files remain in place.
The [R3 packet](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/README-r3.md)
records exact deltas, source qualifications and as-of consumers. This successor
requires its own independent review; no whole conversion family is complete.

## Remaining obligations and evidence limits

The documented128-slice threshold applies to the Slice operation. It does not
prove a generic rack cap or restrict recognition to128 generated notes. Audio
slicing can retain source regions while recognition resynthesizes notes; no
waveform equality follows. Full conversion models, marker/count arithmetic,
program/default identities, tuning, source/transaction behavior and all listed
error/cancel/undo/save/reopen/teardown outcomes remain unknown. No whole conversion,
MIDI, device or file family is complete.

## Analyst source appendix

Captured official [Converting Audio to MIDI](https://www.ableton.com/en/live-manual/12/converting-audio-to-midi/),
Version12. Exact source metadata, UTC/size/URL are in
[source.json](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/source.json),
HTML SHA-256 `52c513cf72f707a5298d74c745015eccb5bc9db0f735a7e2219f7f77353e6123`.
No figures inspected. Existing native selection research identifies different
recognition tasks but is not a complete classifier/output oracle.

### Source convert-drums-to-new-midi-track

[convert-drums-to-new-midi-track](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/manual-conversion-2026-10-19.html#convert-drums-to-new-midi-track), retained HTML line 338; digest above.

### Source convert-harmony-to-new-midi-track

[convert-harmony-to-new-midi-track](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/manual-conversion-2026-10-19.html#convert-harmony-to-new-midi-track), retained HTML line 324; digest above.

### Source convert-melody-to-new-midi-track

[convert-melody-to-new-midi-track](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/manual-conversion-2026-10-19.html#convert-melody-to-new-midi-track), retained HTML line 324; digest above.

### Source converting-audio-to-midi

[converting-audio-to-midi](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/manual-conversion-2026-10-19.html#converting-audio-to-midi), retained HTML line 280; digest above.

### Source optimizing-for-better-conversion-quality

[optimizing-for-better-conversion-quality](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/manual-conversion-2026-10-19.html#optimizing-for-better-conversion-quality), retained HTML line 338; digest above.

### Source resequencing-slices

[resequencing-slices](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/manual-conversion-2026-10-19.html#resequencing-slices), retained HTML line 304; digest above.

### Source slice-to-new-midi-track

[slice-to-new-midi-track](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/manual-conversion-2026-10-19.html#slice-to-new-midi-track), retained HTML line 292; digest above.

### Source using-effects-on-slices

[using-effects-on-slices](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/manual-conversion-2026-10-19.html#using-effects-on-slices), retained HTML line 324; digest above.

### Source conversion-default qualification

Only six selected CommonDevices paragraphs DEV:B134–139 are used to qualify
factory/no-custom result histories. Their complete raw contexts, capture
metadata and retained full-source hash are in
[source-context-r3.json](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/source-context-r3.json).
They allow custom Harmony/Melody single instruments, so the supplied Rack/preview
roles above are conditional. No custom-default creation, folder grammar,
last-added precedence, nested-Drum-Rack admission or other chapter contract is
adopted here. No full CommonDevices chapter audit, figure inspection or followed
destination is claimed.
