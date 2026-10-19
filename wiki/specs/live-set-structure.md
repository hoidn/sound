---
id: SPEC-LIVE-SET-STRUCTURE
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Live Set structure

## Scope

Feature FEAT-PERSISTENCE, with FEAT-SESSION, FEAT-AUDIO and FEAT-DEVICES, in the
[feature map](feature-map.md). Workstream T1.1 of target T1
([ADR 0004](../decisions/adr-0004-target-scope-t1.md)). User task: open a Live Set whose content
lies in T1, read its tracks, mixers, session slots and scenes, clips, sample references, device
chains, sends and returns, and automation targets, and save it again. This draft specifies the
document structure that the field-level specs assume:

- the reading model: which elements a set may contain, and what an unknown, absent or
  duplicated element does;
- the track list: track types, order, Ids, names and colours, and the main and cue tracks;
- where each track's mixer, session sequencer, freeze sequencer and device chain sit;
- session clip slots and scenes: count rules, empty slots, scene fields;
- clip containers, and where the fields of the other T1 specs sit in them;
- sample references: their fields, how a path is resolved on open, what the file must hold,
  and what a save writes;
- device chains holding the seven bundled devices;
- send and return wiring;
- automation envelope placement and the target Id scheme;
- the two Id spaces, `NextPointeeId`, and the structural conditions that make a set unopenable;
- a minimal T1 set with an element-by-element list of what is required.

The envelope (gzip or XML, root element and version attributes) belongs to
[SPEC-ALS-CONTAINER](als-container.md). Value text rules come from
[SPEC-TRANSPORT-STATE](transport-state.md). The fields inside the structure belong to
[SPEC-MIXER-VALUES](mixer-values.md), [SPEC-CLIP-LAUNCH](clip-launch.md),
[SPEC-MIDI-NOTE-STORAGE](midi-note-storage.md), [SPEC-WARP-MARKERS](warp-markers.md),
[SPEC-AUTOMATION-ENVELOPES](automation-envelopes.md) and
[SPEC-BUNDLED-DEVICE-PARAMETERS](bundled-device-parameters.md); this spec says only where they
sit. Target: 12.4.3, documents with `MinorVersion="12.0_12402"`. Document examples are fragments
of the decoded XML.

Every requirement is a **proposed contract** supported by shipped bytes, by a static derivation
from the 12.4.3 program, by extracted execution of the shipped x86_64 code, or explicitly
unknown. Nothing was run against Live, and under
[ADR 0003](../decisions/adr-0003-no-reference-execution.md) nothing will be.

Excluded: group tracks beyond the rule that a T1 track is not grouped; Arrangement clips, take
lanes and the groove pool; racks; plug-in and Max for Live devices; freezing and the content of
frozen slots; input routing, monitoring and recording; view state (selection, zoom, scroll,
folding, view data); clip files (`.alc`) and presets as documents of their own; older documents
and their migration; the text of error messages and how a refusal is shown
([REQ-ALS-CONTAINER-009](als-container.md#req-als-container-009--failure-presentation-and-state)).

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema `12.0_12402.txt`, the 26 Live Sets and 350 clip files of the 12.4.3 bundle (written by Live 12.4d1 or 12.1d1, not by a 12.4.3 save), and the sample files they reference |
| S | Static derivation from the 12.4.3 executable or shipped bytes; not an observed run |
| S-cond | Static derivation that holds only if the named open assumption (A4–A7 below) holds |
| X | Extracted execution: the shipped x86_64 function was run on the stated inputs in the harness of [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code). It shows what the function computes, not that Live calls it with those inputs |
| U | Unknown; no expected result, or only a static expectation that must not be graded. No reference observation is available (ADR 0003). A static route, where named, is a reading that could still settle it |

Only D, S, S-cond and X clauses may enter a release, an S-cond clause only together with its
assumption. U clauses block the behavior they name. "The set does not open" means the document
reader stops with the corrupt-document error of SPEC-ALS-CONTAINER; how Live presents it is
excluded.

## Assumptions

Each open assumption is supported by the evidence but not established. If one fails, the clauses
that name it become unknown. No reference observation will test them (ADR 0003). A1 to A3 were
settled by a static trace of the open path after revision 1 was first written; the clauses that
named them are now labelled S.

| ID | Assumption | What rests on it |
| --- | --- | --- |
| A1 | **Settled (S, both slices; revision 1, 2026-10-18).** Opening a Live Set runs each member's post-load step as it is read, the set's root post-load step, and then the post-order validation walk over every compound. Every application path that opens a `.als` (opening for the user, the command line, restore) ends in the application's load method, which reads the file with the XML reader; that reader's load step always runs the walk, and its reading context enables the post-load steps. This also settles SPEC-AUTOMATION-ENVELOPES's A3 for Live Sets. Remaining inference: that menu and OS open events use these application entries | REQ-002, 006, 013, 014, 015 (now S) |
| A2 | **Settled (S; revision 1, 2026-10-18).** Nothing adds slots to a track's freeze sequencer while a set is read, so after reading, the freeze sequencer holds exactly the slots of the document's `FreezeSequencer/ClipSlotList` (none when the element is absent). The track chain constructors create the freeze sequencer with an empty slot list, and the only routines that add slots outside the list reader (inserting a scene, creating a track) are edit paths that no load step reaches. Remaining inference: no virtual call outside those enumerated adds slots | REQ-006 (now S) |
| A3 | **Settled (S; revision 1, 2026-10-18).** The preset-extraction flag that exempts presets from the pointee Id check is clear when a set is opened. It is set only around preset extraction, device presets and a debug browser, none of which the set-open path calls | REQ-015 (now S) |
| A4 | When a set is opened from a file, the sample-path resolution context is present and its base is the folder of the set file | REQ-009 |
| A5 | Every list field (schema type −1, class `RemoteableList`) is read by the one generic list loader, which has 26 callers | REQ-016, and REQ-001's list-class clause for lists other than `Tracks` |
| A6 | A device list accepts a bundled device class wherever shipped racks place it: an instrument (`UltraAnalog`, `StringStudio`, `Collision`, `LoungeLizard`) in a `MidiToAudioDeviceChain` device list, an effect (`Amp`, `Cabinet`, `Corpus`) in an `AudioToAudioDeviceChain` or `MidiToAudioDeviceChain` list. A MIDI track's inner chain is a `MidiToAudioDeviceChain`; an audio, return or main track's is an `AudioToAudioDeviceChain`. The list's class test was not read | REQ-012 |
| A7 | A 12.4.3 save writes the set through the generic member and list writers that were read. The Live Set save call site was not traced | REQ-011, 017 |

Terms. A *pointee* is an element of schema class `Pointee`, `FloatAutomationTarget`,
`EnumAutomationTarget`, `BoolAutomationTarget`, `TimeableModulationTarget` or
`UserFloatModulationTarget`: in documents the `AutomationTarget` and `ModulationTarget` of every
parameter, the `Pointee` of every device, the eight `…ModulationTarget` elements of an audio
sequencer and the `ControllerTargets.0` to `ControllerTargets.130` elements of a MIDI track. Its
`Id` attribute is a *pointee Id*. A *list item* is a child of a list field (`Tracks`, `Scenes`,
`SendsPre`, `ClipSlotList`, `Devices`, `Sends`, `Envelopes`, `Events`, `KeyTracks`,
`WarpMarkers`, …); its `Id` attribute is a *list-item Id*. A *player track* is an `AudioTrack`,
`MidiTrack` or `GroupTrack`. *R* is the number of `ReturnTrack` items at the end of `Tracks`.

## Requirements

### REQ-LIVE-SET-STRUCTURE-001 — reading model

- **D.** The schema file lists each class with its fields. Each field has a class and one of
  four forms: a compound child element (type 0); a base value (type −4), written either as an
  attribute of the parent or as a child element with one `Value` attribute; a list or slot
  (type −1) whose children are elements named by their own class, each list item with an `Id`
  attribute; an array (type −3) whose items are named by the field's array class. In all 375
  shipped `12.0_12402` documents every element is a field of its parent's class, every list item
  is a schema class, and children occur in the class's field order. The only exceptions are two
  base values with several attributes, `LiveSet/VideoWindowRect` and
  `AbletonDefaultPresetRef/DeviceId`. Which base values are attributes is not in the schema; the
  shipped documents show it (for example `<MidiTrack Id="12" SelectedToolPanel="7">`,
  `<MidiClip Id="0" Time="0">`, `<LomId Value="0" />`).
- **S.** A compound's children are matched by name, so their order in the document does not
  change what is read. An absent member keeps the value the object's constructor gives it;
  absence is not in itself an error. The consequences of absence named in REQ-002, 006, 013 and
  015 come from later checks.
- **S.** A child element whose name the parent class does not declare is skipped with its
  content, as in REQ-TRANSPORT-STATE-008, including its exception for a versioned read whose
  `SchemaChangeCount` equals the schema's change count.
- **S.** The set does not open when:
  - a base value written as an element has no `Value` attribute (for example `<NextPointeeId />`);
  - a compound holds two children of the same name (REQ-TRANSPORT-STATE-008);
  - a list or slot child is not a known class, or is a class that list does not accept.
- **U.** Which classes each list accepts beyond those shipped in it. Static route: the class
  test of each list owner.

### REQ-LIVE-SET-STRUCTURE-002 — the track list

- **D.** `LiveSet/Tracks` holds the audio, MIDI, group and return tracks as `AudioTrack`,
  `MidiTrack`, `GroupTrack` and `ReturnTrack` items, in their display order. Shipped sets hold
  124 MIDI, 91 audio, 20 return and 3 group tracks; in all 26 every return track follows every
  other track. The main and cue tracks are not in this list (REQ-004).
- **S.** The set does not open when `Tracks` holds no player track. This includes an
  empty list, an absent `Tracks` element and a list of return tracks only.
- **S.** The set does not open when a player track follows a return track.
- **S.** A track whose `TrackGroupId` is not −1 must lie inside the group track with
  that Id, and a group track must have a member; otherwise the set does not open. T1 tracks are
  not grouped and store `TrackGroupId` −1, as 225 of 238 shipped tracks do.
- **U.** What any other class in `Tracks` does, such as `MainTrack`, `PreHearTrack` or a clip
  class (REQ-001). Static route: the track list's class test.

### REQ-LIVE-SET-STRUCTURE-003 — track Id, name and colour

- **D.** Every track item has an `Id` attribute, unique within `Tracks`. Values are arbitrary
  non-negative integers, not positions (`12 13 8 14 2 3` in the default template). In 39 of 238
  shipped tracks the value equals a pointee Id of the same set: track Ids and pointee Ids are
  separate spaces (REQ-015, REQ-016).
- **D.** `Name` holds `EffectiveName`, `UserName`, `Annotation` and `MemorizedFirstClipName`,
  each with a `Value` attribute. `UserName` is the name the user gave and is empty in 80 of 238
  tracks; `EffectiveName` then holds a generated text such as `1-MIDI` or `2-Audio`. 22 tracks
  have a `UserName` that differs from `EffectiveName`.
- **D.** `Color/@Value` is an integer. Shipped audio, MIDI, group, return and main tracks use
  0 to 69; every cue track stores −1.
- **S.** Names and colours are held as read (the generic loader stores base values directly).
- **U.** How `EffectiveName` is derived when `UserName` is empty, whether a loaded
  `EffectiveName` is kept or recomputed, and which colour each index shows. Static route: the
  name class's update and the colour palette. T1 needs only that both values survive a save.

### REQ-LIVE-SET-STRUCTURE-004 — main and cue tracks

- **D.** `LiveSet/MainTrack` and `LiveSet/PreHearTrack` (the cue, or preview, track) occur once
  each, after `Tracks`, without an `Id`. Shipped main tracks have `EffectiveName` `Main` and an
  empty `UserName` (26 of 26). The main track's `DeviceChain` holds four routings, `Mixer`,
  `FreezeSequencer` and `DeviceChain`; the cue track's holds four routings, `Mixer` and
  `DeviceChain`. Neither has session slots.
- **D.** The main mixer holds the song tempo and time signature
  ([REQ-TRANSPORT-STATE-001](transport-state.md#req-transport-state-001--field-locations)) and
  the crossfader ([REQ-MIXER-VALUES-009](mixer-values.md#req-mixer-values-009--crossfade-assign-crossfader-and-crossfade-curve-values)).
  Its `AutomationEnvelopes` hold the one-event tempo and time-signature envelopes of
  [REQ-AUTOMATION-ENVELOPES-005](automation-envelopes.md#req-automation-envelopes-005--the-leading-event-at-the-lower-time-bound).
- **S.** A set without a `MainTrack` or `PreHearTrack` element opens with the track the set
  object creates for itself; its values are the constructor's, for example tempo 120
  (REQ-TRANSPORT-STATE-007).

### REQ-LIVE-SET-STRUCTURE-005 — track device chain layout and routing

- **D.** Each track's `DeviceChain` element holds, in this order (26 of 26 sets):

  | Track | Children of `DeviceChain` |
  | --- | --- |
  | `MidiTrack`, `AudioTrack` | `AutomationLanes`, `ClipEnvelopeChooserViewState`, `AudioInputRouting`, `MidiInputRouting`, `AudioOutputRouting`, `MidiOutputRouting`, `Mixer`, `MainSequencer`, `FreezeSequencer`, `DeviceChain` |
  | `ReturnTrack` | the same up to `Mixer`, then `DeviceChain`, `FreezeSequencer` |
  | `MainTrack` | as `ReturnTrack`, with `FreezeSequencer` before `DeviceChain` |
  | `PreHearTrack` | as `ReturnTrack`, without `FreezeSequencer` |

  `MainSequencer` is the session sequencer: a MIDI sequencer on a MIDI track, an audio sequencer
  on an audio track. The inner `DeviceChain` is the device chain (REQ-012).
- **D.** The mixer is `DeviceChain/Mixer` for every track type; its fields are
  [REQ-MIXER-VALUES-001](mixer-values.md#req-mixer-values-001--mixer-location-and-fields-per-track-type).
- **D.** `AudioOutputRouting/Target/@Value` is `AudioOut/Main` on every shipped MIDI and return
  track and on 77 of 91 audio tracks; 13 audio tracks output to their group (`AudioOut/GroupTrack`)
  and one to a hardware output. Main and cue tracks output to hardware
  (`AudioOut/External/…`). A routing also stores display strings and MPE settings.
- **U.** The output a track gets when `AudioOutputRouting` is absent, and the meaning of the
  other targets. **T1 limit:** a T1 track outputs to the main track; a set whose audio, MIDI or
  return track names another output is outside T1.

### REQ-LIVE-SET-STRUCTURE-006 — session clip slots and scenes

- **D.** `LiveSet/Scenes` holds `Scene` items. The session slots of an audio or MIDI track are
  the `ClipSlot` items of `DeviceChain/MainSequencer/ClipSlotList`. In every shipped track the
  number of slots equals the number of scenes (215 of 215), and the freeze sequencer's
  `ClipSlotList` has the same number of slots (215 of 215; 350 of 350 in clip files). Scene
  counts run from 1 to 511. Return, main and cue tracks have no slots.
- **D.** A slot is `<ClipSlot Id="…"><LomId Value="0" /><ClipSlot><Value>…</Value></ClipSlot><HasStop Value="true" /></ClipSlot>`.
  The inner `ClipSlot/Value` holds one clip, or nothing for an empty slot (`<Value />`). 3,385
  of 7,498 shipped session slots hold a clip; `HasStop` is `true` in all.
- **D.** Slot Ids are `0 … n−1` in 176 of 215 tracks. The other 39 reuse the scene Ids in scene
  order, and one set mixes both forms. Scene Ids are `0 … n−1` in 15 of 26 sets.
- **Inferred.** Slot k of every track belongs to scene k, by position. Neither slot Ids nor
  scene Ids link the two.
- **S.** The set does not open when an audio or MIDI track's freeze sequencer
  holds a different number of slots from its session sequencer. A track with one or more
  session slots and no `FreezeSequencer` element is such a track.
- **U.** A set whose session slot count differs from its scene count, or that has slots and no
  scenes. No load check comparing the two was found, and no shipped set has the shape. Static
  route: the scene-list post-load and the per-scene loop in the player track's validation.
  **T1 limit:** such a set is outside T1; a T1 writer writes one slot per scene in both
  sequencers.
- **U.** A slot whose `Value` holds two clips, or a clip of the other track kind (an
  `AudioClip` on a MIDI track).
- **D.** A `Scene` holds `FollowAction`, `Name`, `Annotation`, `Color`, `Tempo`,
  `IsTempoEnabled`, `TimeSignatureId`, `IsTimeSignatureEnabled`, `LomId` and
  `ClipSlotsListWrapper` (706 of 706). `Name` is empty in 586. `Tempo` is `120` with
  `IsTempoEnabled` false in 697; 9 scenes enable a tempo (74 to 160). `TimeSignatureId` is a
  time-signature code ([REQ-TRANSPORT-STATE-010](transport-state.md#req-transport-state-010--time-signature-code)),
  `201` (4/4) in all but one (`302`). `Color` is −1 in 697 scenes and 69 in 9.
- **U.** What a scene's tempo and time signature do when the scene is launched. Scene launching
  is outside T1, so these fields are stored and saved only.

### REQ-LIVE-SET-STRUCTURE-007 — clip containers

- **D.** A session clip is the `MidiClip` or `AudioClip` element in a slot's `ClipSlot/Value`,
  with the attributes `Id` and `Time` (`Time` is `0` on every shipped session clip). Both
  classes start with the same 28 fields; then `MidiClip` holds `Notes` and its program and
  editor fields, and `AudioClip` holds `SampleRef`, `Onsets`, the warp fields, fades, pitch,
  `SampleVolume` and `WarpMarkers`.
- **D.** Field owners:

  | Fields of the clip element | Owner |
  | --- | --- |
  | `LaunchMode`, `LaunchQuantisation`, `Legato`, `VelocityAmount`, `FollowAction` | [REQ-CLIP-LAUNCH-001](clip-launch.md#req-clip-launch-001--clip-launch-fields-location-types-and-order), 002 |
  | `Notes` | [REQ-MIDI-NOTE-STORAGE-001](midi-note-storage.md#req-midi-note-storage-001--note-container-structure) |
  | `IsWarped`, `WarpMode`, the eight mode settings, `WarpMarkers` | [REQ-WARP-MARKERS-001](warp-markers.md#req-warp-markers-001--where-warp-state-is-stored) |
  | `Envelopes/Envelopes/ClipEnvelope` | [REQ-AUTOMATION-ENVELOPES-001](automation-envelopes.md#req-automation-envelopes-001--envelope-containers) |
  | `SampleRef` | REQ-008 to REQ-011 |
  | `CurrentStart`, `CurrentEnd`, `Loop` (`LoopStart`, `LoopEnd`, `StartRelative`, `LoopOn`, `OutMarker`, `HiddenLoopStart`, `HiddenLoopEnd`), `TimeSignature` | Playback core (T1.3); the clip time signature is also read by [REQ-CLIP-LAUNCH-016](clip-launch.md#req-clip-launch-016--which-grid-a-launch-uses) |
  | `Name`, `Color` | Held as read, like track names (REQ-003) |

- **U.** The meaning of `CurrentStart`, `CurrentEnd` and the `Loop` fields for playback; T1.3
  owns them.

### REQ-LIVE-SET-STRUCTURE-008 — sample reference fields

- **D.** An audio clip's file is named by `SampleRef/FileRef`. `SampleRef` holds `FileRef`,
  `LastModDate`, `SourceContext`, `SampleUsageHint`, `DefaultDuration`, `DefaultSampleRate` and
  `SamplesToAutoWarp`; `FileRef` holds `RelativePathType`, `RelativePath`, `Path`, `Type`,
  `LivePackName`, `LivePackId`, `OriginalFileSize`, `OriginalCrc` and `SourceHint`, all as
  `Value` elements. All 2,845 shipped session audio clips use this form with
  `RelativePathType` 5, a `RelativePath` under `Samples/`, an absolute `Path` on the authoring
  machine, `Type` 2 and a non-empty `LivePackName`.
- **S.** `RelativePathType` codes: 0 unknown, 1 relative to the set's folder (Document),
  2 Library, 3 relative to the project folder (Project), 4 Id-based, 5 relative to a Live Pack
  named by `LivePackName` and `LivePackId`, 6 relative to the user library, 7 relative to the
  built-in content.
- **D, S.** `OriginalFileSize` is the file's size in bytes. `OriginalCrc` is a 16-bit CRC of the
  file's first min(size, 16,384) bytes: polynomial 0x8005, most significant bit first, initial
  value 0, no reflection, no final exclusive-or. Shipped values match this rule for 2,984 of
  2,984 referenced bundle files (D).
- **X.** The original x86_64 CRC step returns the rule's value for every input run, including
  47,018 for the first 16,384 bytes of the T11-MIN sample and 65,256 (0xFEE8) for the ASCII
  text `123456789`.
- **D.** `DefaultDuration` is the file's length in sample frames and `DefaultSampleRate` its
  sample rate as an integer, in 2,983 of 2,983 shipped WAV and AIFF references.
- **S.** `LastModDate` is the file's modification time in whole seconds since 1970-01-01 UTC,
  or 0 when it cannot be read.
- **S, D.** `Type` is written as 2, and every shipped sample reference stores 2. **U.** Its
  meaning.

### REQ-LIVE-SET-STRUCTURE-009 — sample resolution on open

- **S-cond (A4).** A non-empty `RelativePath` is joined to a base chosen by `RelativePathType`:
  0 or 1, the folder of the set file; 3, the project folder found from that folder; 5, the root
  of the pack with `LivePackId`; 6, the user library; 7, the built-in content. Type 2 gives no
  base, and type 4 gives no file at all. The first candidate that exists is used.
- **S.** When the relative path gives no existing file, types 0, 1, 2 and 6 use the absolute
  `Path` if it is not empty. Types 3, 5 and 7 do not use `Path`.
- **S.** A sample that cannot be resolved does not stop the set from opening. The clip is kept
  and its file is marked missing.
- **U.** What the user is shown for a missing file, the missing-file search, the
  project-folder rule of type 3, the library relocation of types 2, 5 and 7, how the size and
  CRC identity is used, and what a clip with a missing file plays. **T1 limit:** a T1 set's
  samples resolve; a set with a missing sample is outside T1's playback.

### REQ-LIVE-SET-STRUCTURE-010 — sample file content

- **D.** Every shipped session audio clip references a `.wav` (1,904) or `.aif` (941) file. In
  every checked reference the file's frame count and rate equal `DefaultDuration` and
  `DefaultSampleRate`.
- **S.** `DefaultDuration` and `DefaultSampleRate` set the sample's length and rate before the
  file is read.
- **U.** Which formats Live decodes for a clip, whether it decides by extension or by content,
  and what happens when the file's real length or rate differs from the stored values. Static
  route: the sample object's update after the file is read. **T1 limit:** a T1 sample is an
  uncompressed PCM WAV or AIFF file whose frame count and rate equal the stored
  `DefaultDuration` and `DefaultSampleRate`.

### REQ-LIVE-SET-STRUCTURE-011 — sample reference on save

- **S-cond (A7).** When the referenced file exists, a save writes `Path` as the file's absolute
  path and `Type` 2. It writes the first `RelativePathType` that applies, in this order:
  7 built-in content, 5 Live Pack, 6 user library, 3 project folder, 1 the set's folder.
  Types 7, 5, 6 and 3 apply only to a file inside that root; type 1 may climb out of the set's
  folder with `..` (all 7,322 shipped type-1 references, which name presets and source files,
  start with `..`; D). When none applies it writes type 0 with an empty `RelativePath`.
- **S-cond (A7).** The save recomputes `OriginalFileSize` and `OriginalCrc` when the file changed
  and writes the file's current `LastModDate`.
- **U.** When type 1 applies (inferred: when the file and the set are on the same volume), the
  project-folder rule, the `SourceHint` text, and whether every reference is written with all
  nine `FileRef` children (4 shipped references omit `SourceHint`, D). **T1 effect:** the exact
  `RelativePathType` a 12.4.3 save chooses cannot be predicted for a file inside a project
  folder, so a T1 writer is judged by the file the reference resolves to, not by its text.

### REQ-LIVE-SET-STRUCTURE-012 — device chains and the seven devices

- **D.** A track's devices are the items of its inner `DeviceChain/Devices` list, in signal
  order. Each device element carries an `Id` attribute as a list item. Its content is
  [REQ-BUNDLED-DEVICE-PARAMETERS-002](bundled-device-parameters.md#req-bundled-device-parameters-002--device-element-content).
- **D.** The seven bundled devices occur 36 times in the shipped sets and 577 times in the
  clip files, every time inside a rack branch: in `…/InstrumentBranch/DeviceChain/MidiToAudioDeviceChain/Devices`
  or `…/AudioEffectBranch/DeviceChain/AudioToAudioDeviceChain/Devices`. No shipped document
  places one directly in a track's chain; ordinary native devices do sit there (`Operator` and
  `Drift` on MIDI tracks, `Reverb` and `Delay` on audio and return tracks).
- **D.** A MIDI track's inner chain has the class of an instrument branch's chain
  (`MidiToAudioDeviceChain`), and an audio, return or main track's has the class of an effect
  branch's chain (`AudioToAudioDeviceChain`). Both classes hold only `Devices` and
  `SignalModulations`.
- **S-cond (A6).** An instrument placed in a MIDI track's `DeviceChain/DeviceChain/Devices`, or
  an effect placed in any track's, is read as it is in a rack branch, with the element form
  shown there:
  `<MidiTrack Id="1">…<DeviceChain>…<DeviceChain><Devices><UltraAnalog Id="0">…</UltraAnalog></Devices></DeviceChain></DeviceChain></MidiTrack>`.
- **U.** Whether a chain refuses a device class (an instrument on an audio track, two
  instruments on one chain) and what a refused class does. **T1 limit:** T1 chains hold at most
  one instrument, first on a MIDI track, followed by effects; audio, return and main chains
  hold effects only.

### REQ-LIVE-SET-STRUCTURE-013 — sends and returns

- **D.** Every audio, MIDI, group and return mixer holds one `TrackSendHolder` per return track
  in `Mixer/Sends`, and the main and cue mixers hold none (26 of 26 sets;
  [REQ-MIXER-VALUES-003](mixer-values.md#req-mixer-values-003--send-holders-and-send-values)).
  A return mixer holds a send to every return, itself included. `LiveSet/SendsPre` holds one
  `SendPreBool` item, `<SendPreBool Id="0" Value="false" />`, per return track (26 of 26), `false`
  in all 20 shipped.
- **D.** Holder Ids equal the `SendsPre` Ids in 235 of 238 tracks; 3 MIDI tracks of one set have
  `0 1` against `0 2`, so the Ids do not link holders to returns. Which return a send feeds,
  and what `SendPreBool` selects, belong to the draft [SPEC-MIX-GRAPH](mix-graph.md)
  (REQ-MIX-GRAPH-001: send k and `SendPreBool` k belong to the k-th return, by list order).
- **S.** When a mixer holds fewer send holders than R, holders are appended to make R.
  An appended send has the new-send values of REQ-MIXER-VALUES-003 (−70 dB; `EnabledByUser`
  true, but false on a return track's mixer, inferred).
- **S.** The set does not open when a mixer of a track in `Tracks` holds more send
  holders than R.
- **U.** A `SendsPre` list whose length differs from the number of return tracks: no load check
  was found here (SPEC-MIX-GRAPH reports an error for a thirteenth item). **T1 limit:** a T1 set
  has one `SendPreBool` per return; a set with a different count is outside T1.
- **D.** Every shipped return track outputs to `AudioOut/Main` (20 of 20).

### REQ-LIVE-SET-STRUCTURE-014 — automation placement and target Ids

- **D.** Track envelopes sit in `<Track>/AutomationEnvelopes/Envelopes` and clip envelopes in
  `<Clip>/Envelopes/Envelopes`
  ([REQ-AUTOMATION-ENVELOPES-001](automation-envelopes.md#req-automation-envelopes-001--envelope-containers)).
  An envelope names its target by `EnvelopeTarget/PointeeId`, whose value is the pointee Id of a
  parameter's `AutomationTarget` or of a modulation or controller target
  ([REQ-AUTOMATION-ENVELOPES-002](automation-envelopes.md#req-automation-envelopes-002--envelope-targets)).
  Every shipped track envelope names an `AutomationTarget` (355 of 355).
- **S.** On opening, every track or clip envelope whose `PointeeId` is 0 or names no
  pointee of the set is removed, and the set opens without it.
- **U.** A further removal of "empty" or "half-dangling" envelopes follows; its conditions were
  not read. Fixtures keep each envelope on a parameter of its own track.

### REQ-LIVE-SET-STRUCTURE-015 — pointee Ids and NextPointeeId

- **D.** In every shipped set and clip file (376 of 376) pointee Ids are nonzero and unique in
  the whole document, and `LiveSet/NextPointeeId/@Value` is exactly one more than the largest
  pointee Id. The sets hold 215,734 pointees.
- **S.** An absent `NextPointeeId` reads as 1.
- **S.** The set does not open when a pointee element is present with `Id` 0 or
  without an `Id`.
- **S.** The set does not open when `NextPointeeId` is not greater than the largest
  pointee Id (negative Ids count as 0 here).
- **S.** A pointee whose element is absent from the document (for example a parameter written
  without its `AutomationTarget`) receives a new Id on opening, counting up from
  `NextPointeeId`, before dangling envelopes are removed (REQ-014).
- **U.** Which new Id each such pointee receives (the registration order was not read). A T1
  writer therefore writes every target that an envelope names.
- **S.** When two pointees share an Id, the set is not opened as stored. Live asks
  whether to repair it. On repair, every pointee inside a track or the main track whose Id is
  shared receives a new Id counting up from `NextPointeeId`, the first occurrence included;
  envelope references in the same track follow it, and references that cannot be assigned are
  removed.
- **U.** The repair dialog's text, the outcome when the user declines (inferred: the set is not
  opened), duplicates outside tracks, and negative pointee Ids. **T1 limit:** a set with
  duplicate pointee Ids is outside T1.

### REQ-LIVE-SET-STRUCTURE-016 — list-item Ids

- **D.** Every list item in every shipped document carries an `Id`, unique within its list (all
  27,632 lists with more than one item: 10,750 in the sets, 16,882 in the clip files). Values
  are arbitrary non-negative integers.
- **S-cond (A5).** The set does not open when a list item's `Id` is negative or is not an
  integer (the integer text rule of REQ-TRANSPORT-STATE-006), or when two items of one list
  have the same `Id`.
- **U.** A list item without an `Id`: refused under a reader condition that was not interpreted.
  A T1 writer gives every list item an `Id`.
- **S.** List-item Ids do not order or link anything: a list's order is its document order
  (REQ-002, REQ-006), and the Id spaces of different lists and of pointees are separate.

### REQ-LIVE-SET-STRUCTURE-017 — structure written on save

- **S-cond (A7).** A save writes the envelope of
  [REQ-ALS-CONTAINER-008](als-container.md#req-als-container-008--envelope-written-on-save), then
  each object's members in schema field order, base values marked as attributes as attributes
  and the rest as elements, and omits key and MIDI assignment members that are unassigned
  (REQ-TRANSPORT-STATE-002). Every shipped `12.0_12402` document has this form (D).
- **S-cond (A7).** Each list item is written with the Id it holds: the Id read for an item that
  had one. Each pointee is written with its Id, and `NextPointeeId` with the set's counter,
  which is at least one more than every pointee Id.
- **U.** Whitespace and indentation, compression (REQ-ALS-CONTAINER-007), which view-state
  members are written, and the number text of fields that no T1 spec owns. **T1 effect:** a T1
  candidate's save is judged by the meaning of the T1 fields after reopening (ADR 0004 Files),
  not by its bytes.

### REQ-LIVE-SET-STRUCTURE-018 — minimal T1 set

- **S-cond (A4–A6).** The set T11-MIN (Acceptance cases) opens and holds the content listed
  there. Its structure is the minimum a T1 writer writes; the table states for each element
  whether it is required, value-bearing or optional.

  Status: **R** required: absence or the stated violation makes the set not open. **V**
  value-bearing: absence is tolerated and gives the stated default, so write it to carry a T1
  value. **O** optional: absence gives a constructor value and does not affect T1. **W** write
  it: whether absence is tolerated, or the value absence gives, is unknown. Where two letters
  are given, the first applies to the stated violation and the second to absence.

  | Element (below `/Ableton/LiveSet` unless absolute) | Status | Rule or default when absent |
  | --- | --- | --- |
  | Declaration, `/Ableton` with `MajorVersion` 5 and `MinorVersion` `12.0_12402` | R | SPEC-ALS-CONTAINER 001–006; `SchemaChangeCount` optional (written 1) |
  | `/Ableton/LiveSet` | R | No document element is refused |
  | `NextPointeeId` | R | Greater than every pointee Id; absent reads 1 (REQ-015) |
  | `Tracks` with at least one `MidiTrack` or `AudioTrack`, returns last | R | REQ-002 |
  | Track `Id` attribute | R | Non-negative integer, unique in `Tracks` (REQ-016); write it |
  | Track `Name` (`EffectiveName`, `UserName`), `Color` | W | Held as read; absent value unknown (REQ-003) |
  | Track `AutomationEnvelopes/Envelopes` | V | Absent: no envelopes |
  | Track `TrackGroupId` −1 | W | Constructor default not read; −1 means not grouped |
  | `DeviceChain/AudioOutputRouting/Target` `AudioOut/Main` | W | REQ-005 |
  | `DeviceChain/Mixer` and its value elements | V | REQ-MIXER-VALUES defaults for absent values |
  | `Mixer/Sends/TrackSendHolder` (with `Id`), one per return | R/V | More than R is refused; fewer are appended (REQ-013) |
  | `DeviceChain/MainSequencer/ClipSlotList/ClipSlot` (with `Id`), one per scene | W | Count against scenes unknown (REQ-006) |
  | `ClipSlot/ClipSlot/Value`, `ClipSlot/HasStop` `true` | W | Empty `Value` is an empty slot |
  | `DeviceChain/FreezeSequencer/ClipSlotList` with as many empty slots | R | REQ-006 |
  | `DeviceChain/DeviceChain/Devices/<device Id>` | V | REQ-012 placement (A6); absent parameters take REQ-BUNDLED-DEVICE-PARAMETERS-008 defaults |
  | `MidiClip` / `AudioClip` with `Id` and `Time` 0 | R | `Id` rules of REQ-016 |
  | Clip `CurrentStart`, `CurrentEnd`, `Loop` | V | T1.3; write them |
  | Clip `Name`, `Color` | V | Held as read |
  | Clip `LaunchMode`, `LaunchQuantisation` | W | REQ-CLIP-LAUNCH-010: absent gives a preference value |
  | Clip `TimeSignature`, `Envelopes/Envelopes`, `Legato`, `VelocityAmount`, `FollowAction` | V | REQ-CLIP-LAUNCH-009 and 016 |
  | `MidiClip/Notes` with all five children | W | REQ-MIDI-NOTE-STORAGE-001: a missing structural child is unknown |
  | `AudioClip/IsWarped` `false`, `WarpMode` | V/W | T1 plays unwarped; absent `WarpMode` unknown ([Q-021](../questions.md#q-021-warp-playback-mapping-and-load-handling)) |
  | `AudioClip/SampleRef/FileRef` with the nine children; `LastModDate`, `DefaultDuration`, `DefaultSampleRate` | V | REQ-008 to 010 |
  | `AudioClip/WarpMarkers` with at least one marker (T11-MIN: two, the second 1/32 beat after the first) | R | REQ-WARP-MARKERS-004 refuses an empty list |
  | `MainTrack` with `DeviceChain/Mixer` (`Tempo`, `TimeSignature`, `CrossFade`) and the one-event tempo and time-signature envelopes | V | Absent: constructed, tempo 120 (REQ-004) |
  | `PreHearTrack` | O | Absent: constructed |
  | `SendsPre/SendPreBool` (`Id`, `Value` `false`), one per return | W | REQ-013 |
  | `Scenes/Scene` (with `Id`), one per slot, with `Name`, `Color`, `Tempo`, `IsTempoEnabled`, `TimeSignatureId`, `IsTimeSignatureEnabled` | W | REQ-006 |
  | `Transport` | V | REQ-TRANSPORT-STATE-007 defaults |
  | `GlobalQuantisation`, `AutoQuantisation` | W | REQ-CLIP-LAUNCH-008: absent is unknown |
  | `CrossfadeCurve` | V | REQ-MIXER-VALUES-009 |
  | Each pointee element written (`AutomationTarget`, `ModulationTarget`, `Pointee`, …) | R/O | Nonzero unique `Id` (REQ-015); omitted ones get new Ids, so write the targets that envelopes name |
  | View state (`LomId`, `SelectedToolPanel`, `ViewData`, `AutomationLanes`, wrappers, …) | O | Constructor values |

## T1 limits

These unknowns bound what T1 can claim. Each names the input or output it excludes.

| Clause | Effect on T1 |
| --- | --- |
| REQ-005 U | Tracks whose audio output is not the main track are outside T1 |
| REQ-006 U | Sets whose slot count differs from their scene count are outside T1 |
| REQ-009 U | Sets with an unresolved sample are outside T1 playback; how Live reports them is not specified |
| REQ-010 U | T1 samples are uncompressed PCM WAV or AIFF matching their stored length and rate |
| REQ-011 U, REQ-017 U | A saved set is judged by meaning after reopening, not by text or `RelativePathType` |
| REQ-012 U | Device placement is limited to A6's positions |
| REQ-013 U | `SendsPre` must have one item per return |
| REQ-015 U | Sets with duplicate or negative pointee Ids are outside T1 |
| REQ-016 U | Every list item has an `Id` |

## Timing and state

Loading is one operation whose outcome is "opens", "does not open" or, for duplicate pointee Ids,
a repair question (REQ-015). Ordering within the load: list, value and pointee-Id checks apply
while the elements are read (REQ-001, REQ-015, REQ-016); the root post-load step then checks
`NextPointeeId`, repairs duplicate pointee Ids, registers pointees, removes dangling envelopes
and appends missing send holders (REQ-013 to 015); the validation walk then checks the track
list and slot counts (REQ-002, REQ-006). Sample files are resolved as each reference is read (REQ-009); a
missing file changes no outcome. Persistent state: everything in the document. Undo, edits after
load and cancellation are out of scope.

## Errors, cancellation and teardown

The structural conditions under which a set does not open are those of REQ-001 (unknown list
class, base element without `Value`, duplicate member), REQ-002 (no player track, a player track
after a return, grouping), REQ-006 (freeze slot count), REQ-013 (more send holders than returns),
REQ-015 (pointee Id 0 or absent, `NextPointeeId` too low) and REQ-016 (bad or duplicate list-item
Id). Conditions owned by other specs: the envelope (SPEC-ALS-CONTAINER 001 to 006), value text
(SPEC-TRANSPORT-STATE 003 to 006, 008), an envelope without events or with a bad first event
time (SPEC-AUTOMATION-ENVELOPES 007), an empty audio-clip marker list (SPEC-WARP-MARKERS 004, 005),
notes (SPEC-MIDI-NOTE-STORAGE 001, 014) and clip migration (SPEC-CLIP-LAUNCH 014). Repairs that
let a set open: appended send holders (REQ-013), removed dangling envelopes (REQ-014), new Ids for
absent pointees (REQ-015), constructed main and cue tracks (REQ-004), skipped unknown compound
children (REQ-001). No cancel affordance is specified; the state after a refusal is
REQ-ALS-CONTAINER-009 and unknown.

## Acceptance cases

None of these cases has been run against Live, and under ADR 0003 none will be. Expectations are
static derivations, shipped facts, or X results; each row names its basis and assumptions.
Kinds: P positive, N does not open, R opens after a repair, M missing element, S save,
X computed value, U unresolved (not graded).

### Fixtures

**T11-MIN** is authored for this spec by `make_fixture.py` (appendix); it contains no shipped
bytes. Files: `T11-MIN.als` (gzip, one member, FLG 0, MTIME 0) with the same content as
`T11-MIN.xml` (882 lines, tab-indented, LF), and `Samples/T11-tone.wav` beside it (1 s, 44,100 Hz,
16-bit PCM, 2 channels, a 441 Hz sine at amplitude 8,192, 176,444 bytes, modification time
1,760,000,000). Content:

- envelope `MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1"`;
- `NextPointeeId` 69; 68 pointees with Ids 1 to 68;
- `Tracks`: `MidiTrack Id="1"` named `Lead` (colour 15), `AudioTrack Id="2"` with an empty
  `UserName` and `EffectiveName` `2-Audio` (colour 3), `ReturnTrack Id="3"` (`A-Return`,
  colour 55); each with output `AudioOut/Main`, `TrackGroupId` −1 and a mixer at the new-mixer
  values with one send holder (`Id="0"`, −70 dB, `EnabledByUser` true, false on the return);
- the MIDI track: two session slots and two empty freeze slots; slot 0 holds `MidiClip`
  `Two Notes` (4 beats, looped, 4/4, launch 0/0, two notes of key 60 at beats 0 and 2, length 1,
  velocity 100); its device chain holds `UltraAnalog Id="0"` with only its `On` parameter; its
  track envelope sets the volume target (Id 11) to 1 at L and 0.5 at beat 4;
- the audio track: two session slots and two empty freeze slots; slot 0 holds `AudioClip` `Tone`
  (2 beats, looped, `IsWarped` false, `WarpMode` 0, markers (0 s, 0 beats) and
  (0.015625 s, 0.03125 beats)) whose `FileRef` is `RelativePathType` 1, `RelativePath`
  `Samples/T11-tone.wav`, `Path` `/T11/Samples/T11-tone.wav`, `Type` 2, empty pack fields,
  `OriginalFileSize` 176444, `OriginalCrc` 47018, with `LastModDate` 1760000000,
  `DefaultDuration` 44100 and `DefaultSampleRate` 44100; its device chain holds `Amp Id="0"`
  with only `On`;
- `MainTrack` (`Main`, colour 69) with tempo 120 and time signature 201, each with its
  one-event envelope, and crossfader 0; `PreHearTrack` with a mixer; `SendsPre` with one `false` item; two scenes
  (`Id` 0 and 1, `Scene 1` and `Scene 2`, colour −1, tempo 120 disabled, 201 disabled);
  `Transport` (loop off, start 0, length 8, position 0); `GlobalQuantisation` 4,
  `AutoQuantisation` 0, `CrossfadeCurve` 2.

The set and its `Samples` folder are copied together to any folder before each case. Each case's
setup is a T11-MIN edit unless it says otherwise: the decoded XML changed only as stated and
re-encoded as gzip. Comparators: "opens"
and "does not open" are judged by whether loading finishes; a held value is read through the Live
API or the user interface; a saved value is compared per attribute value after reopening.

### Cases

| Case ID | Requirement | Kind | Setup/action | Expected result | Basis |
| --- | --- | --- | --- | --- | --- |
| LSS-001 | 001–016, 018 | P | Open T11-MIN | Opens; tracks `Lead`, `2-Audio`, `A-Return` in that order, then the main track; two scenes; MIDI slot 1 holds `Two Notes`, audio slot 1 holds `Tone`, the other slots are empty; the MIDI track holds Analog and the audio track Amp; each of the three tracks has one send | S-cond (A4–A6) |
| LSS-002 | 002 | N | Remove all three tracks and the `SendPreBool` | Does not open | S |
| LSS-003 | 002 | N | Remove the MIDI and audio tracks, keep the return | Does not open | S |
| LSS-004 | 002 | N | Move `ReturnTrack Id="3"` before `AudioTrack Id="2"` | Does not open | S |
| LSS-005 | 002 | N | Remove `Tracks` | Does not open | S |
| LSS-006 | 001, 002 | N | Add `<FooTrack Id="9" />` to `Tracks` | Does not open | S (unknown class) |
| LSS-007 | 006 | N | Remove the audio track's `FreezeSequencer` | Does not open | S |
| LSS-008 | 006 | N | Append `<ClipSlot Id="2"><ClipSlot><Value /></ClipSlot><HasStop Value="true" /></ClipSlot>` to the MIDI track's session list only | Does not open | S |
| LSS-009 | 006 | U | Append that slot to the MIDI track's session and freeze lists (3 slots, 2 scenes) | Unresolved | U |
| LSS-010 | 006 | U | Remove `Scenes` | Unresolved | U |
| LSS-011 | 006 | P | Change the scene Ids to 7 and 3 | Opens; the scene named `Scene 1` is first | D (shipped arbitrary Ids), S |
| LSS-012 | 006 | P | Change the audio track's slot Ids to 7 and 3 | Opens; `Tone` is in the first slot | D, S |
| LSS-013 | 013 | R | Empty the MIDI track's `Sends` | Opens; the MIDI track has one send, at −70 dB (shown `-inf dB`) | S; value REQ-MIXER-VALUES-003 |
| LSS-014 | 013 | N | Add a second `TrackSendHolder Id="1"` to the audio track's `Sends` | Does not open | S |
| LSS-015 | 013 | U | Empty `SendsPre` | Unresolved | U |
| LSS-016 | 003, 016 | N | Change the audio track's `Id` to 1 | Does not open | S-cond (A5) |
| LSS-017 | 016 | N | Change the audio track's `Id` to `-1` | Does not open | S-cond (A5) |
| LSS-018 | 016 | U | Remove the audio track's `Id` attribute | Unresolved | U |
| LSS-019 | 003, 015 | P | Change the audio track's `Id` to 5 (also a pointee Id) | Opens | D (39 shipped tracks), S |
| LSS-020 | 015 | N | `NextPointeeId` 68 | Does not open | S |
| LSS-021 | 015 | N | Remove `NextPointeeId` | Does not open (it reads as 1) | S |
| LSS-022 | 015 | P | `NextPointeeId` 100000 | Opens | S |
| LSS-023 | 001 | N | `<NextPointeeId />` | Does not open | S |
| LSS-024 | 015 | N | The audio track's Pan `AutomationTarget` `Id="0"` | Does not open | S |
| LSS-025 | 015 | N | Remove that `Id` attribute | Does not open | S |
| LSS-026 | 015 | U | Set that Id to 5, the MIDI track's Pan target Id | Unresolved: a repair question is expected (S); the dialog and outcome are U | U |
| LSS-027 | 015 | M | Remove the audio track's Pan `AutomationTarget` element | Opens | S |
| LSS-028 | 014 | R | Set the MIDI track envelope's `PointeeId` to 999999 | Opens; the MIDI track has no envelope; after a save and reopen it still has none | S |
| LSS-029 | 004 | M | Remove `MainTrack` | Opens; tempo 120 | S |
| LSS-030 | 004 | M | Remove `PreHearTrack` | Opens | S |
| LSS-031 | 001 | P | Add `<Foo Value="1" />` as a child of the MIDI track | Opens; a save does not write `Foo` | S (REQ-TRANSPORT-STATE-008 rule; `SchemaChangeCount` 1 is not 5); S-cond (A7) for the save |
| LSS-032 | 009 | P | Open from a new folder with `Samples` beside it | Opens; `Tone` references `Samples/T11-tone.wav` in the set's folder | S-cond (A4) |
| LSS-033 | 009 | P | Delete `Samples/T11-tone.wav` | Opens; `Tone` is kept and its file is reported missing | S (opening); U (report) |
| LSS-034 | 009 | P | `RelativePath` `Samples/absent.wav`; `Path` the absolute path of the sample at test time | Opens; `Tone` uses the file at `Path` | S (with or without A4) |
| LSS-035 | 009 | P | As LSS-034 with `RelativePathType` 7 | Opens; `Tone`'s file is missing (`Path` not used) | S (with or without A4) |
| LSS-036 | 008 | X | Compute the identity of `Samples/T11-tone.wav` | `OriginalFileSize` 176444, `OriginalCrc` 47018 | X (CRC), D (size) |
| LSS-037 | 012 | P | Move `Amp Id="0"` to the return track's device list | Opens; the return track holds Amp | S-cond (A6) |
| LSS-038 | 012 | U | Move `UltraAnalog Id="0"` to the audio track's device list | Unresolved | U |
| LSS-039 | 001–017 | S | Open, save, reopen | Opens; tracks, names, colours, Ids, slots and their clips, scenes and their fields, devices, sends, the envelope and its target, and the sample reference resolving to the same file all as in LSS-001 | S-cond (A4–A7); text not graded (REQ-017) |
| LSS-040 | 011 | S | Open, save to a folder outside any project, reopen | The saved `FileRef` has `Path` the sample's absolute path and `Type` 2; `OriginalFileSize` 176444 and `OriginalCrc` 47018 | S-cond (A7); `RelativePathType` not graded (REQ-011 U) |

Counts: 40 cases: 6 unresolved (LSS-009, 010, 015, 018, 026, 038) and 34 graded: 1 X (LSS-036),
3 with a D part (011, 012, 019), the rest S or S-cond. LSS-033 grades the opening only. Omitted kinds: cancellation (no affordance), and
group tracks (outside T1). Cases owned by other specs are not repeated here; their fixtures
should adopt the T11-MIN skeleton (Open questions).

## Open questions

Canonical gaps go to [Q-022](../questions.md) (proposed; not yet filed) and the existing
[Q-012](../questions.md#q-012-transport-state-load-and-save-semantics),
[Q-020](../questions.md#q-020-automation-envelope-load-robustness) and
[Q-021](../questions.md#q-021-warp-playback-mapping-and-load-handling). Items:

- Settled in revision 1 (follow-up trace): A1, A2 and A3. Still open: that menu and OS open
  events reach the application entries traced, and A4 to A7.
- REQ-006 slot count against scene count, and zero scenes.
- REQ-013 `SendsPre` length and meaning.
- REQ-009 and 010: missing-file handling, decoding, and stored length or rate that differ from
  the file.
- REQ-012: the device-class test of each chain.
- REQ-015: the repair dialog and negative pointee Ids; REQ-016: Id-less list items.
- Released fixtures
  ([audit](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/released-fixture-audit.json)).
  Live refuses 204 released fixtures used by 178 cases that expect the set to open:
  - REQ-002, no player track: transport-state-v1 18 fixtures (13 cases) and transport-state-v2 33
    (23 cases);
  - REQ-006, session slots without freeze slots: automation-envelopes-v1 21 (13), clip-launch-v1
    49 (43), midi-note-storage-v1 66 (51) and warp-markers-v1 17 (35, several cases per fixture).

  Another 64 cases expect a refusal and still get one, but their fixtures no longer isolate the
  rule under test. The 29 als-container-v1 sets are refused after the envelope, and their cases
  grade the envelope only, so they stay valid. The 37 mixer-values-v1 fixtures lack `SendsPre`
  (REQ-013 U). Each release requires that missing set content not change a judged outcome, so a
  candidate that implements this spec cannot pass those cases. The audit records, for each
  refused fixture, the T11-MIN elements to add (a MIDI track with empty session and freeze slot
  lists, or the missing freeze slots), which change no existing element. A re-check of every
  amended copy finds no refusal. A corrective fixture revision is needed for those five families.
- SPEC-AUTOMATION-ENVELOPES: its dangling-target exclusion (REQ-002, Q-020) can become REQ-014's
  removal. Under A5 its duplicate event Ids (REQ-004), like SPEC-MIDI-NOTE-STORAGE REQ-012's
  repeated KeyTrack Ids and SPEC-WARP-MARKERS REQ-002's marker Ids, would make the set not open.
- SPEC-MIXER-VALUES REQ-003 and the draft SPEC-MIX-GRAPH REQ-001 keep a holder count that
  differs from the return count unknown; REQ-013 settles it (fewer are appended, more make the
  set not open).

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical findings:
[Live Set structure](../research/live-set-structure.md). Retained run:
[t11-structure-v1](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/manifest.json), regenerated
by `sh run.sh`. Image `Live.arm64` SHA-256 `3a99ceea…d1c383cfad`; x86_64 slice SHA-256
`1bae9a97…be999b0`. "P" marks arm64 corpus pseudocode, "D86" x86_64 disassembly read with
objdump. Every address is listed with its observation in `traces/*/trace.txt`, and every
pseudocode record relied on is kept in `traces/*/corpus-excerpts*.jsonl`.

| Requirement | Evidence | Strength |
| --- | --- | --- |
| 001 | `schema_check.py` over 375 documents (`out/schema-check-{als,alc}.jsonl`); start element `0x1015299e0`, field lookup `0x10152ac0c`, required attribute `0x10152b45c`, add-member `0x101472624` (N1); list loader `0x1014674b4`: unknown class `0x10148229c`, class test list slot +0x190 (P; x86 `0x10145f320` D86) | D; S |
| 002 | ASong +0x100 `0x1026969d8` → `0x102687a7c` (P); x86 `0x1027b1a00` D86 (`1027b1a48`–`1027b1ac5`: empty or no player track → string `0x106135387`; player after return → `0x1061353a0`); player predicate: APlayerTrack class or slot +0x230 (IsGroup); grouping and empty group in the same function | S |
| 003 | Survey `track_ids_unique`, `name_form`, `color_values`; 39 track-Id collisions (research page) | D |
| 004 | ASong ctor `0x10266f738` creates the cue track (+0x200), the main track (+0x260) and empty `SendsPre`, `Scenes` and `Tracks` lists (P); `AMainTrackDevice` tempo default (N1) | S |
| 005 | Survey `chain_children`, `routing` | D |
| 006 | APlayerTrack +0x100 `0x1025cb248` (P); x86 `0x1026f1720` D86 (session count from slot +0x300, freeze count `0x102784e60`, mismatch → string `0x106133548`); chain ctors `0x10291f76c`, `0x1027df560` and sequencer base `0x10265b61c` create both sequencers with empty lists (P); `traces/tracks/slot-counts.txt` | D; S |
| 007 | Schema classes `MidiClip`, `AudioClip`; survey `clip_children`, `clip_attrs` | D |
| 008 | AFileRef registry `0x1014e7ad4`, names `0x1014e8b88` (P; x86 `0x1014d94a0`); size and CRC `0x1014e98cc`, `0x101279eac`, step `0x1011b6e88` (P); `traces/fileref/crc-check.txt` (2,984 of 2,984), `duration-check.txt` (2,983 of 2,983); `LastModDate` `0x1014e7678` (P). X: x86 step `0x101191310` (caller `0x10125a540`), 8 inputs, `out/x-crc.json`, no import called. The step is integer-only (shift, exclusive-or with 0x8005), the same operations in both slices | D; S; X |
| 009 | ASampleRef post-load `0x102877af8` → `0x10279aba8` → `0x10279aae0` → `0x1014e8504` (P; x86 `0x1014d8e20`, fallback branch `0x1014d90e5` D86); candidates `0x1014ead80`; existence `0x1014e9d78`; media manager `0x10279a170`, missing status `0x10279d228` (P) | S-cond (A4); S |
| 010 | Extension table `0x10127ec24` (P); seeding `0x102876594` (P); survey `fileref_ext` | D; S |
| 011 | `0x10279a590`, `0x10279a744`, `0x1014e8eb8`, `0x1014e9230` (P; x86 `0x1014d99d0` D86: inside-root flag 1 for 7, 5, 6, 3 and 0 for Document), `0x1014e986c` (P) | S-cond (A7) |
| 012 | Survey `seven_paths`, `chain_devices`; schema `MidiToAudioDeviceChain`, `AudioToAudioDeviceChain` | D; S-cond (A6) |
| 013 | ASong +0xd0 `0x102695f78` (P); x86 `0x1027c1640` D86 (`1027c18a2`–`1027c18f3`: fewer → append `0x102850a50`, more → error); R = trailing returns `0x10267c60c`; return-mixer holder flag via `0x102659620` (inferred); survey `holders_vs_returns`, `sendspre_vs_returns` | D; S |
| 014 | ASong +0x318 `0x1026869b0` → `0x102456050`, `0x1024067e8` (P), gated on application byte +0x350 set to 1 by its constructor `0x1018499a4`; dangling test `0x101536090`; later purge `0x102406378` (not interpreted) | S |
| 015 | APointee `Id` registration `0x10153575c`; post-load `0x101535954` (P; x86 `0x101525600` D86) with preset flag `0x106f50550`; ADocument `NextPointeeId` +0x140, constructor value 1 (`0x10153fbbc`, constant `0x105818b28`); check `0x1015441a8` (P; x86 `0x10153df90`, `0x101533ae0` D86); registration `0x10154368c` (x86 `0x101533040` D86); repair `0x102686a3c` (P) | D; S; S |
| 016 | List-item `Id` attribute `0x10152b77c` (P); duplicate Ids in the list loader (P; x86 `0x10145f320` D86, string `0x1060f6a7a`); survey `list_ids_unique` | D; S-cond (A5) |
| 017 | Writer `0x101486cdc` (N1); list writer `0x101468408` (P) | S-cond (A7) |
| 018 | `make_fixture.py`, `out/schema-check-fixture.jsonl` (no deviation; every rule measurement as REQ-002 to 016 require) | S-cond |

**A1 to A3, settled by the follow-up trace** (`traces/a1a2/trace.txt`, `reach.txt`,
`vtable-owners.txt`, `x86-load-sequence.txt`, `corpus-excerpts*.jsonl`; `sh traces/a1a2/run_a1a2.sh`):

| Link | arm64 (x86_64) | Strength |
| --- | --- | --- |
| Open for the user, command line, restore | ALiveApp slot +0x730 `0x101854f54` ("Loading Document For User"; x86 `0x10186edc0`), `0x10184df98` (x86 `0x101867dc0`), `0x1018517cc`, each → slot +0x840 | P; R (vtable `0x10659ad00`) |
| ALiveApp slot +0x840 | `0x1002e6e00` (x86 `0x10035eec0`): Note sets (file types 12 and 13, `.abl`, `.ablbundle`) to an import path, every other file to `0x1018536d4` "Loading document " (x86 `0x10186d760`) | P; R |
| Readers | general reader `0x10148389c` (x86 `0x10147ad50`) → XML reader `0x101484108` (x86 `0x10147b550`) → load step `0x101486fe4` (x86 `0x10147e150`). The version-aware reader `0x10146c258` returns nodes only and is not reached | P; reach.txt |
| Post-load enabled | reading context `0x10151e0d8` sets +0x2c to 1 (x86 `0x10150cb5d`, `0x10150cb7f`); only the undo-history stream clears it (`0x1015192b8` from `0x101546518`, `0x101547ef4`) | D86; P |
| Walk always runs | load step: +0xd0 when +0x2c is set (x86 `0x10147e23c`–`0x10147e256`), then the walk `0x10147e2e0` unconditionally, which tail-calls +0x100 (x86 `0x10147e37d`) | D86 |
| Freeze sequencer exists, empty | chain constructors `0x1027df560` (via `0x1027e3118`, AAudioSequencer `0x1027d8ea0`) and `0x10291f76c` (`0x1027d8e48`) | P |
| No slot added while reading | slot insertion `0x10265d22c` only via `0x10265e1d8` (callers `0x1023bfed4`, `0x1025776b4`, `0x10257770c`, `0x1025cde68`), reached from InsertScene `0x10268dfc8` and create-track `0x10267bfc0` only; none reached from the load hooks `0x102695f78`, `0x1025cb2b8`, `0x1027de958`, `0x1023c6d80`, `0x1014674b4`, `0x101486fe4`, `0x101487310` | P; reach.txt |
| Preset exemption off | setter `0x101535944` callers are preset, device-preset and debug-browser functions; not reached from `0x1002e6e00` or `0x1018536d4` | P; reach.txt |

Extracted execution was not used: the checks read object graphs, and none is a self-contained
function.

Corrections and contradictions found:

- **Released fixtures** (see Open questions): `out/schema-check-released-fixtures.jsonl`
  measures, per released fixture, the structure that REQ-002, 006, 013 and 015 test.
- **Q-020 premise.** The question says a dangling `PointeeId` makes Live abort when accessed.
  The abort is in the pointer resolution, which the load-time removal of REQ-014 precedes; the
  removal runs before the validation walk. Revision 1 does not claim that no other access
  happens first.
- **SPEC-BUNDLED-DEVICE-PARAMETERS REQ-012** says no static route for assigning target Ids is
  known: REQ-015's registration assigns new Ids from `NextPointeeId` to pointees read with Id 0
  (presets) or absent.
- **Fork reports.** The track trace found no uniqueness check for track Ids; the pointee
  trace found the generic list loader's duplicate-Id refusal. REQ-016 follows the second, under
  A5.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-18 | First draft from workstream T1.1 (packet t11-structure-v1): 18 requirements; 40 unexecuted cases on the authored fixture T11-MIN (34 graded: 1 X, 33 S, S-cond or D; 6 unresolved); T1 limits for 9 unknown clauses; released-fixture contradictions recorded |
| 1 (revised in place, unreleased) | 2026-10-18 | Follow-up trace of the open path in both corpora settles A1, A2 and A3 statically; the clauses and cases that named them change from S-cond to S. No expectation changed. `released-fixture-audit.json` added: 233 released Live Set fixtures refused by the traced rules, 178 cases contradicted, each with its minimal T11-MIN addition |

Not released. A first release could carry REQ-001 to 018 with assumptions A4 to A7 stated, and
cases LSS-001 to 008, 011 to 014, 016, 017, 019 to 025, 027 to 037, 039 and 040. It should be
reviewed together with fixture revisions of the families named under Open questions.
