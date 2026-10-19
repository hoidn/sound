# Live Set structure, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-PERSISTENCE, FEAT-SESSION, FEAT-AUDIO. Parent
specification identity: SPEC-LIVE-SET-STRUCTURE revision 1. Release:
live-set-structure-v1. Only the clauses explicitly included below are in
scope. No other clause of a listed requirement is implicitly approved. This
document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the narrowing recorded in [the review disposition](REVIEW.md).
Implementation requires a fresh, restricted implementation workspace.

## What the contract means

A user opens a Live Set file. After its envelope is accepted, the application
reads the document's structure: the track list, the main and cue tracks, each
track's mixer, session slots and freeze slots, the scenes, the clips in the
session slots, their sample references, the sends, the targets of automation
envelopes, and the Ids that tie them together. Some structures make the set
fail to open. Others are repaired while the set opens. This contract covers:

- which elements a Live Set of this format holds, and where;
- the structural conditions under which a set does not open;
- the repairs that let a set open: send holders added, envelopes whose target
  does not exist removed, a new main or cue track, unknown elements skipped,
  and new Ids for target elements that are absent;
- how a sample reference names its file, how the file is found when the set
  opens, and the size and checksum values that identify the file;
- the reference minimal set T11-MIN, with the status of each of its elements.

It does not specify what a save writes, how a refusal is shown, where devices
may be placed or what they hold, or how anything sounds.

Expectations have three kinds of provenance:

- **Documented**: taken from the form of the Live Sets and clips shipped with
  the target build, and of the sample files they reference.
- **Static-derived**: derived for the target build without running it.
- **Extracted execution**: in one case, the original program's own checksum
  routine was run on the case's file. It ran on a Linux x86_64 host, from the
  program's x86_64 build. The macOS arm64 build is inferred to give the same
  result.

None is an observed run of the original application, and none was run against
a candidate. No compatibility result is established. The original application
remains the authority for a later comparison. Two derived steps rest on the
[stated assumptions](#stated-assumptions), and each case lists the ones its
expectation needs.

## Terms

| Term | Meaning |
| --- | --- |
| Paths | Relative to `/Ableton/LiveSet` unless they start with `/` |
| Track | An item of `Tracks`: `MidiTrack`, `AudioTrack`, `ReturnTrack` or `GroupTrack`. Group tracks are outside this release apart from REQ-LIVE-SET-STRUCTURE-002 clause 4 |
| Player track | An audio, MIDI or group track |
| Track n | The n-th item of `Tracks`, counting from 1 |
| R | The number of `ReturnTrack` items at the end of `Tracks`, counted from the last item back to the first item that is not a return track |
| Main track, cue track | The `MainTrack` and `PreHearTrack` elements. They are not items of `Tracks` |
| Session slots | The `ClipSlot` items of `<track>/DeviceChain/MainSequencer/ClipSlotList` |
| Freeze slots | The `ClipSlot` items of `<track>/DeviceChain/FreezeSequencer/ClipSlotList` |
| Value element | An element that holds one value in its `Value` attribute and has no other attribute and no child, for example `<NextPointeeId Value="67" />` |
| Array | An element whose children are items of one name without an `Id`. In the fixtures only `KeyTrack/Notes`, whose items are `MidiNoteEvent` elements |
| List | An element whose children are items named by their kind, each with an `Id` attribute. The lists that hold items in the fixtures are `Tracks`, `Scenes`, `SendsPre`, `ClipSlotList`, `Sends`, `Envelopes`, `Events`, `KeyTracks`, `TimeSignatures` and `WarpMarkers`. The inner `ClipSlot/Value` of a slot has the same form and holds at most one item, the clip |
| List-item Id | The `Id` attribute of a list item |
| Target element | An element named `AutomationTarget`, `ModulationTarget`, `Pointee`, `VolumeModulationTarget`, `TranspositionModulationTarget`, `TransientEnvelopeModulationTarget`, `GrainSizeModulationTarget`, `FluxModulationTarget`, `SampleOffsetModulationTarget`, `ComplexProFormantsModulationTarget`, `ComplexProEnvelopeModulationTarget`, or `ControllerTargets.0` to `ControllerTargets.130`, at a place where its parent holds it. The fixtures contain only `AutomationTarget` and `ModulationTarget` |
| Target Id | The `Id` attribute of a target element. Target Ids and list-item Ids are separate: the same number may occur in both |
| Opens | The document is read without refusal and the set is shown |
| Refused | The set does not open. How the refusal is reported, and what is open afterwards, are excluded |

## Document scope and preconditions

- Every fixture is a gzip file of one member. The 10-byte header is
  `1F 8B 08 00 00 00 00 00 02 13`; raw deflate data at maximum compression and
  the CRC-32 and length trailer follow, and nothing follows the trailer.
- The decoded content is UTF-8 XML with line-feed line endings and tab
  indentation. It starts with `<?xml version="1.0" encoding="UTF-8"?>`. The
  root element is `Ableton` with exactly the attributes `MajorVersion="5"`,
  `MinorVersion="12.0_12402"` and `SchemaChangeCount="1"`, and its only child
  is `LiveSet`. Other envelopes, other format versions and their conversion
  are outside this release.
- The sample is the WAV file `fixtures/Samples/T11-tone.wav`. A set refers to
  it as `Samples/T11-tone.wav` relative to the set's folder, so the set file
  and the `Samples` folder are copied together unless a case says otherwise.
- Every fixture other than T11-MIN is T11-MIN with exactly the change its
  purpose states.

## Outcomes and comparison convention

Each case in [cases.json](cases.json) names an input, a setup and an action.
For the action `open`, the setup is carried out in a new, empty folder on a
local volume that is not inside a Live project folder, and the copied set is
opened in a fresh application state:

| Setup | Meaning |
| --- | --- |
| `with-samples` | Copy the input file and the folder `fixtures/Samples` into the new folder, keeping the folder name `Samples` |
| `without-samples` | Copy only the input file |
| `with-samples-absolute-path` | As `with-samples`. Then, in the decoded document, replace the value `/T11/Samples/T11-tone.wav` of the audio clip's `SampleRef/FileRef/Path` with the absolute path of the copied `Samples/T11-tone.wav`, and store the document again in the fixtures' gzip form |

The action `compute-identity` takes the input sample file and computes the four
values of REQ-LIVE-SET-STRUCTURE-008 clause 4 from it.

Each case's `kind` is informative: `positive` (the set opens as stored),
`refusal` (the set is refused), `repair` (the set opens after a stated
repair), `missing-element` (the set opens without an element) or `computed`
(an identity computation).

The result is described with these labels:

| Label | Values |
| --- | --- |
| `outcome` | `opens` or `refused` |
| `state` | Values held after opening; only the keys listed in a case are judged |
| `identity` | For `compute-identity`: `OriginalFileSize`, `OriginalCrc`, `DefaultDuration` and `DefaultSampleRate` as integers |

State keys:

| Key | Meaning |
| --- | --- |
| `track_kinds` | The tracks in display order as `midi`, `audio` or `return`; the main and cue tracks are not included |
| `scene_names` | The scene names in display order. The list length is the number of scenes |
| `session_clips` | For each audio or MIDI track, in track order, its session slots in order: the clip's name, or `null` for an empty slot |
| `send_counts` | For each track, in track order, the number of sends its mixer has |
| `send_texts` | Keyed by track number: the value text of each send of that track, in order |
| `automated_parameters` | Keyed by track number: the number of that track's parameters that have a track automation envelope |
| `tempo` | The song tempo in beats per minute |
| `audio_clip_file` | The file the audio clip in the first session slot of track 2 uses, as a path relative to the new folder |

Comparison rules:

- `outcome` compares exactly. A refused case has no `state`.
- Each listed state key compares exactly: strings character for character,
  numbers as numbers, lists element for element. Keys that a case does not
  list are not judged. For `send_texts` and `automated_parameters`, which are
  keyed by track number, only the track numbers a case lists are judged.
- `identity` values compare exactly.
- Message text, dialogs, notices about missing files, logs and the state after
  a refusal are not compared.
- Each case is independent. No timing applies.

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may translate its own
result into these labels. The fixture set is not an executable harness for the
original application.

## Selected requirement clauses

Each clause below is included only as stated.

### REQ-LIVE-SET-STRUCTURE-001: reading model (partial)

1. A document element is one of these forms: a compound element whose
   children are its members; a value, written either as an attribute of its
   parent or as a value element; a list; or an array. Which values are
   attributes follow the fixtures, for example `<MidiTrack Id="1">`,
   `<MidiClip Id="0" Time="0">` and `<SendPreBool Id="0" Value="false" />`.
2. The children of a compound element are matched by name. Their order in the
   document does not change what is read.
3. An absent element is not by itself a refusal. The item keeps the value a new
   item of its kind has. The refusals caused by absent elements are those of
   REQ-LIVE-SET-STRUCTURE-002, 006 and 015.
4. A child element whose name its parent does not have is skipped together
   with its content, and the set opens. The case uses `<Foo Value="1" />` in a
   `MidiTrack`. Which names a parent has, beyond those in the fixtures, is not
   part of this release.
5. The set is refused when:
   - `NextPointeeId` is written as `<NextPointeeId />`, without `Value`;
   - a compound element holds two children of the same name (lists and
     arrays are not compound elements). The
     case duplicates `Color` in a `MidiTrack`. Names ending in `KeyMidi` are
     excluded;
   - an item of `Tracks` has a name that is no kind of item in this format,
     for example `FooTrack`.

### REQ-LIVE-SET-STRUCTURE-002: the track list (partial)

1. `Tracks` holds the audio, MIDI, group and return tracks in display order.
   The main and cue tracks are not in it.
2. The set is refused when `Tracks` holds no player track, that is no audio,
   MIDI or group track. This includes an
   empty `Tracks`, an absent `Tracks` element and a list of return tracks only.
3. The set is refused when a player track follows a return track in `Tracks`.
4. `TrackGroupId` −1 means that a track is not grouped. A track with any other
   `TrackGroupId` must lie inside the group track with that Id; in a set
   without group tracks, any other value is refused.

### REQ-LIVE-SET-STRUCTURE-003: track Id, name and colour (partial)

1. Every track carries an `Id` attribute, a non-negative integer unique within
   `Tracks`. The values are arbitrary and are not positions. A track Id may
   equal a target Id of the same set.
2. `Name` holds `EffectiveName` and `UserName` value elements, and `Color` is a
   value element with an integer. The fixtures write both names and the colour
   of every track.

### REQ-LIVE-SET-STRUCTURE-004: main and cue tracks (partial)

1. `MainTrack` and `PreHearTrack` occur once each, after `Tracks`, without an
   `Id`. Neither has session slots.
2. The main track's mixer holds the song tempo
   (`MainTrack/DeviceChain/Mixer/Tempo`), the time signature
   (`MainTrack/DeviceChain/Mixer/TimeSignature`) and the crossfader
   (`MainTrack/DeviceChain/Mixer/CrossFade`). This release states their
   locations only, and the tempo of a new main track.
3. A set without `MainTrack` opens with a new main track, whose tempo is 120.
   A set without `PreHearTrack` opens with a new cue track.

### REQ-LIVE-SET-STRUCTURE-005: track device chain layout (partial)

1. A set of this format stores these children of a track's `DeviceChain` in
   this order. Reading does not depend on their order (REQ-LIVE-SET-STRUCTURE-001
   clause 2).

   | Track | Children of `DeviceChain` |
   | --- | --- |
   | `MidiTrack`, `AudioTrack` | `AutomationLanes`, `ClipEnvelopeChooserViewState`, `AudioInputRouting`, `MidiInputRouting`, `AudioOutputRouting`, `MidiOutputRouting`, `Mixer`, `MainSequencer`, `FreezeSequencer`, `DeviceChain` |
   | `ReturnTrack` | the same up to `Mixer`, then `DeviceChain`, `FreezeSequencer` |
   | `MainTrack` | the same up to `Mixer`, then `FreezeSequencer`, `DeviceChain` |
   | `PreHearTrack` | the same up to `Mixer`, then `DeviceChain` |

2. The mixer of every track kind is `DeviceChain/Mixer`. The inner
   `DeviceChain/DeviceChain/Devices` is the track's device list.
3. Every audio, MIDI and return track of the fixtures stores
   `DeviceChain/AudioOutputRouting/Target` with value `AudioOut/Main`. Other
   targets, and an absent routing, are outside this release.

### REQ-LIVE-SET-STRUCTURE-006: session slots, freeze slots and scenes (partial)

1. `Scenes` holds `Scene` items in display order. Audio and MIDI tracks have
   session slots and freeze slots. Return, main and cue tracks have none.
2. A slot is written
   `<ClipSlot Id="…"><ClipSlot><Value>…</Value></ClipSlot><HasStop Value="true" /></ClipSlot>`.
   The inner `Value` holds one clip, or nothing for an empty slot
   (`<Value />`).
3. Slot Ids and scene Ids are arbitrary non-negative integers. Slots and scenes
   are ordered by their position in the document, not by Id.
4. The set is refused when an audio or MIDI track has a different number of
   freeze slots from session slots. A track with one or more session slots and
   no `FreezeSequencer` element is such a track.
5. A `Scene` of the fixtures holds `FollowAction`, `Name`, `Color`, `Tempo`,
   `IsTempoEnabled`, `TimeSignatureId` and `IsTimeSignatureEnabled`. A scene's
   name is held as read.
6. Every audio and MIDI track of the fixtures has one session slot and one
   freeze slot per scene.

### REQ-LIVE-SET-STRUCTURE-007: clip containers (partial)

1. A session clip is the `MidiClip` or `AudioClip` element in a slot's
   `ClipSlot/Value`: `MidiClip` on a MIDI track, `AudioClip` on an audio track.
   It carries the attributes `Id` and `Time`, and `Time` is `0`.
2. A clip's `Name` is a value element, held as read.
3. The other children of a clip are outside this release. The fixtures write
   them as listed under [T11-MIN](#t11-min).

### REQ-LIVE-SET-STRUCTURE-008: sample reference fields (partial)

1. An audio clip's file is named by `SampleRef/FileRef`. `SampleRef` holds
   `FileRef`, `LastModDate`, `DefaultDuration` and `DefaultSampleRate`. A set of
   this format also stores `SourceContext`, `SampleUsageHint` and
   `SamplesToAutoWarp` there; the fixtures omit them. `FileRef` holds, as value
   elements, `RelativePathType`, `RelativePath`, `Path`, `Type`, `LivePackName`,
   `LivePackId`, `OriginalFileSize`, `OriginalCrc` and `SourceHint`.
2. `RelativePathType` 1, and 0, resolve `RelativePath` against the folder of
   the set file (REQ-LIVE-SET-STRUCTURE-009 clause 1). The codes 2 to 7 name
   other bases; this release states nothing more about them.
3. `Path` is an absolute path. `Type` is written as 2; its meaning is outside
   this release.
4. The identity of a sample file:
   - `OriginalFileSize` is the file's size in bytes.
   - `OriginalCrc` is a 16-bit CRC of the file's first min(size, 16,384)
     bytes, with polynomial 0x8005, most significant bit first, initial value
     0, no reflection of input or output and no final exclusive-or. For the
     nine ASCII bytes `123456789` the value is 65,256.
   - `DefaultDuration` is the file's length in sample frames, and
     `DefaultSampleRate` its sample rate as an integer.
5. `LastModDate` is the file's modification time in whole seconds since
   1970-01-01 UTC. No case judges it.

### REQ-LIVE-SET-STRUCTURE-009: sample resolution on open (partial)

1. Under the sample-folder assumption: for `RelativePathType` 0 or 1 with a
   non-empty `RelativePath`, the relative path is joined to the folder of the
   set file. If a file exists there, the clip uses it.
2. When the relative path gives no existing file, `RelativePathType` 0 and 1
   use the absolute `Path`, if it is not empty, without comparing the file
   with the stored size and checksum. Whether the codes 2 to 7 use `Path` is
   outside this release.
3. A sample that cannot be found does not stop the set from opening. The clip
   is kept in its slot.

### REQ-LIVE-SET-STRUCTURE-010: sample file content (partial)

1. In a set of this format, `DefaultDuration` and `DefaultSampleRate` equal
   the frame count and the sample rate of the referenced file.
2. The fixtures' sample is an uncompressed 16-bit PCM WAV file whose frame
   count and rate equal the stored values. Other files have no expectation.

### REQ-LIVE-SET-STRUCTURE-013: sends and returns (partial)

1. Every audio, MIDI and return track's mixer holds one `TrackSendHolder` per
   return track in `Mixer/Sends`, and the main and cue mixers hold none. A
   return track's mixer holds a send to every return track, itself included.
2. `SendsPre` holds one `SendPreBool` item per `ReturnTrack` item of `Tracks`,
   for example `<SendPreBool Id="0" Value="false" />`.
3. When the mixer of a track in `Tracks` holds fewer send holders than R,
   holders are added to make R. An added send is at gain 0.0003162277571
   (−70 dB), whose value text is `-inf dB`.
4. The set is refused when the mixer of a track in `Tracks` holds more send
   holders than R.

### REQ-LIVE-SET-STRUCTURE-014: envelope placement and targets (partial)

1. Track envelopes are the `AutomationEnvelope` items of
   `<track>/AutomationEnvelopes/Envelopes`, and clip envelopes the items of
   `<clip>/Envelopes/Envelopes`. An envelope names its target with
   `EnvelopeTarget/PointeeId`, whose value is a target Id.
2. On opening, every track or clip envelope whose `PointeeId` is 0, or is not
   the Id of a target element of the set, is removed, and the set opens without
   it.

### REQ-LIVE-SET-STRUCTURE-015: target Ids and NextPointeeId (partial)

1. A set of this format writes every target Id as a nonzero integer unique in
   the whole document, and `NextPointeeId` as one more than the largest target
   Id.
2. An absent `NextPointeeId` reads as 1.
3. The set is refused when a target element has `Id` 0 or has no `Id`.
4. The set is refused when `NextPointeeId` is not greater than the largest
   target Id.
5. A target element absent from the document, for example a parameter written
   without its `AutomationTarget`, does not stop the set from opening. The
   target receives a new Id; which one is outside this release.

### REQ-LIVE-SET-STRUCTURE-016: list-item Ids (partial)

1. A set of this format gives every list item an `Id` attribute, unique within
   its list. The values are arbitrary non-negative integers.
2. Under the list-item Id assumption, the set is refused when a list item's
   `Id` is negative (`-1`), contains a letter (`a`), or equals the `Id` of
   another item of the same list.
3. List-item Ids do not order or link anything. A list's order is its document
   order, and different lists use separate Id spaces.

### REQ-LIVE-SET-STRUCTURE-018: the reference minimal set (partial)

T11-MIN opens and holds the content listed below. The status table states,
for each element, what follows from the clauses above.

#### T11-MIN

`fixtures/T11-MIN.als`, with `fixtures/Samples/T11-tone.wav` beside it.
`fixtures/T11-MIN.xml` is a copy of the decoded document for reading; it is
not a case input.

- Envelope as in the preconditions; `NextPointeeId` 67; 66 target elements
  with Ids 1 to 66.
- `Tracks`: `MidiTrack Id="1"` (`EffectiveName` and `UserName` `Lead`, colour
  15), `AudioTrack Id="2"` (`UserName` empty, `EffectiveName` `2-Audio`, colour
  3) and `ReturnTrack Id="3"` (`UserName` empty, `EffectiveName` `A-Return`,
  colour 55). Each has output `AudioOut/Main`, `TrackGroupId` −1 and a mixer
  with one send holder (`Id="0"`, gain 0.0003162277571).
- The MIDI track has two session slots and two empty freeze slots. Session
  slot 1 holds the `MidiClip` `Two Notes`: 4 beats, looped, 4/4, two notes of
  key 60 at beats 0 and 2 with length 1 and velocity 100. Its device list is
  empty. Its track envelope sets the volume target (Id 11) to 1 from the start
  and to 0.5 at beat 4.
- The audio track has two session slots and two empty freeze slots. Session
  slot 1 holds the `AudioClip` `Tone`: 2 beats, looped, `IsWarped` false,
  `WarpMode` 0, warp markers at (0 s, 0 beats) and (0.015625 s, 0.03125
  beats). Its `FileRef` has `RelativePathType` 1, `RelativePath`
  `Samples/T11-tone.wav`, `Path` `/T11/Samples/T11-tone.wav`, `Type` 2, empty
  pack fields and `SourceHint`, `OriginalFileSize` 176444 and `OriginalCrc`
  47018. `LastModDate` is 1760000000, `DefaultDuration` 44100 and
  `DefaultSampleRate` 44100. Its device list is empty.
- The return and main tracks also have empty device lists.
- `MainTrack` (`EffectiveName` `Main`, colour 69) with tempo 120, time
  signature code 201, each with a one-event envelope, and crossfader 0;
  `PreHearTrack` with a mixer; `SendsPre` with one `false` item; two scenes
  (`Id` 0 and 1, named `Scene 1` and `Scene 2`, colour −1, tempo 120 not
  enabled, time signature 201 not enabled); `Transport` (loop off, start 0,
  length 8, position 0); `GlobalQuantisation` 4, `AutoQuantisation` 0 and
  `CrossfadeCurve` 2.
- The sample is 1 s of a 441 Hz sine wave at amplitude 8,192 on both
  channels: 44,100 Hz, 16-bit PCM, 2 channels, 176,444 bytes.

#### Element status

**Required**: absence, or the stated violation, refuses the set.
**Tolerated**: absence does not stop the set from opening, with the stated
effect. **Write**: this release has no expectation for absence; write the
element as T11-MIN does.

| Element | Status | Rule |
| --- | --- | --- |
| `/Ableton` envelope | Precondition | As stated in the preconditions |
| `/Ableton/LiveSet` | Required | Every case keeps it |
| `NextPointeeId` | Required | Greater than every target Id; absent reads as 1 (REQ-LIVE-SET-STRUCTURE-015) |
| `Tracks` with at least one audio, MIDI or group track, return tracks last | Required | REQ-LIVE-SET-STRUCTURE-002 |
| Track `Id` | Required | Not negative, without letters and unique in `Tracks`, under the list-item Id assumption (REQ-LIVE-SET-STRUCTURE-016); absence: Write |
| Track `TrackGroupId` −1 | Required | Another value refuses a set without group tracks; absence: Write |
| Track `Name`, `Color` | Write | |
| Track `AutomationEnvelopes/Envelopes` | Write | |
| `DeviceChain/AudioOutputRouting/Target` `AudioOut/Main` | Write | |
| `DeviceChain/Mixer` and its values | Write | |
| `Mixer/Sends`, one `TrackSendHolder` per return | Required | More than R refuses; fewer are added (Tolerated) |
| Session slots, one per scene | Write | |
| `FreezeSequencer/ClipSlotList`, as many slots as session slots | Required | REQ-LIVE-SET-STRUCTURE-006 |
| `DeviceChain/DeviceChain/Devices`, empty | Write | A device in a device list has no expectation |
| Clip with `Id` and `Time` 0 | Write | `Id` follows REQ-LIVE-SET-STRUCTURE-016 |
| Clip children other than `Name` | Write | |
| `AudioClip/WarpMarkers` with two markers, as in T11-MIN | Write | Fewer markers have no expectation |
| `AudioClip/SampleRef` with the children of T11-MIN | Write | REQ-LIVE-SET-STRUCTURE-008 to 010 |
| `MainTrack` | Tolerated | Absent: a new main track, tempo 120 |
| `PreHearTrack` | Tolerated | Absent: a new cue track |
| `SendsPre`, one `SendPreBool` per return | Write | |
| `Scenes`, one `Scene` per session slot | Write | |
| `Transport`, `GlobalQuantisation`, `AutoQuantisation`, `CrossfadeCurve` | Write | |
| A target element | Required | `Id` nonzero (REQ-LIVE-SET-STRUCTURE-015); absence: Tolerated, a new Id. Write every target that an envelope names |
| An envelope whose target does not exist | Tolerated | Removed (REQ-LIVE-SET-STRUCTURE-014) |
| A child element with an unknown name | Tolerated | Skipped (REQ-LIVE-SET-STRUCTURE-001) |

### Combined failures

Every refusal case breaks exactly one rule of this release, and every other
case breaks none. A document that breaks more than one rule has no
expectation.

## Stated assumptions

| Assumption | Statement | Cases |
| --- | --- | --- |
| `list-item-ids` | The list-item Id rule of REQ-LIVE-SET-STRUCTURE-016 clause 2 applies to every list of a Live Set when it is opened, `Tracks` included | LIVE-SET-STRUCTURE-009 to 011 |
| `sample-folder` | When a set is opened from a file, the folder that REQ-LIVE-SET-STRUCTURE-009 clause 1 joins a relative path to is the folder that holds the set file | LIVE-SET-STRUCTURE-031 |

## Exclusions and deferred obligations

Requirements not released: **REQ-LIVE-SET-STRUCTURE-011** (the sample
reference a save writes), **REQ-LIVE-SET-STRUCTURE-012** (device chains and
where the bundled devices may be placed) and **REQ-LIVE-SET-STRUCTURE-017**
(the structure a save writes).

Inputs with **no expectation** in this release:

- envelopes, containers and format versions other than the preconditions';
- a session slot count that differs from the scene count; a set with slots and
  no scenes, or no `Scenes` element; a slot holding two clips, or a clip of the
  other track kind;
- a `SendsPre` list whose length differs from the number of return tracks;
- a missing sample, apart from REQ-LIVE-SET-STRUCTURE-009 clause 3; a sample
  file other than the fixtures' form, or whose length or rate differs from the
  stored values; `RelativePathType` 2 to 7;
- any device in a device list;
- target Ids that occur more than once, and negative target Ids;
- list items without an `Id`; list-item Id text other than digits, `-1` and
  `a`;
- items of `Tracks` of a known kind that is not a track, such as `MainTrack`,
  `PreHearTrack` or a clip; items of other lists whose kind is unknown or not
  accepted there;
- an output routing other than `AudioOut/Main`, or none, on an audio, MIDI or
  return track;
- group tracks, apart from REQ-LIVE-SET-STRUCTURE-002 clause 4;
- a value element without `Value` other than `NextPointeeId`; repeated
  children whose names end in `KeyMidi`; unknown attributes;
- whether a track envelope whose target exists is kept: a further removal of
  envelopes after opening is not established, so no case expects an envelope
  to remain;
- documents that break more than one rule.

Excluded behavior:

- what a save writes (REQ-LIVE-SET-STRUCTURE-011 and 017);
- how a refusal is shown, its text and the state afterwards;
- the displayed name of a track, how `EffectiveName` is derived, and which
  colour each `Color` value shows;
- which scene a session slot belongs to;
- the effect of a scene's tempo and time signature, and scene launching;
- device content, and what a device does;
- the meaning of the clip timing and loop fields, playback and audio;
- which new Id an absent target element receives;
- how a missing sample is reported, any search for it, and what a clip with a
  missing sample plays;
- which return a send feeds and what `SendPreBool` selects;
- the meaning of `Type`, and any use of `LastModDate`, `OriginalFileSize` or
  `OriginalCrc` when a set opens;
- undo, editing after opening, cancellation and timing.

Before claiming reference compatibility, a separately designed bounded probe
must run these cases, or a justified equivalent set, against the original. It
must pin the original and candidate builds and the fixture bytes, retain
independent observations, and report mismatches. Obligations specific to this
release:

- The application uses its factory default set, not a user template.
- `opens` is observed as the loading finishing with the set shown and no
  document error; `refused` as a document error with the set not opened. A
  notice about a missing file (LIVE-SET-STRUCTURE-032) is not compared.
- State is read through the application's scripting interface or its user
  interface. A send's value text is the text the mixer shows.
- If the original refuses T11-MIN (LIVE-SET-STRUCTURE-001), every case that
  expects `opens` is inconclusive.
- LIVE-SET-STRUCTURE-034 is judged against the candidate's own computation.
  The original exposes these values only in a saved set, which is outside this
  release; its checksum routine was run directly instead.

Candidate-only success proves agreement with this contract, not with the
running original.

## Fixture provenance

Every fixture was generated for this release by one program written for it.
T11-MIN's values, Ids and names are invented, and its device lists are
empty. The sample is a generated sine tone. Each other fixture is T11-MIN with the one change its purpose states,
stored in the gzip form of the preconditions. No fixture contains shipped file
content, program code, schema content or recorded audio. Expected outcomes are
newly authored behavioral data. No public source or dependency is approved or
included. Review status is recorded in [the manifest](manifest.json) and
[the review disposition](REVIEW.md).
