---
id: SPEC-MEDIA-FILE-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Media import, cache, analysis and clip interchange

## Scope and evidence boundary

This partial contract owns documented audio import eligibility, decoding cache,
analysis sidecars/default clips, MIDI file import/export and Live Clip device-load
rules. [Project/media workflows](project-media-workflows.md) owns collection and
reference repair; [audio/video export](audio-video-export.md) owns rendering.
[MIDI note storage](midi-note-storage.md) owns stored note structure, not SMF.
[Warp markers](warp-markers.md) owns marker serialization, not ASD codecs.

D12 predicates describe the retained Version12 manual; exact12.4.3 applicability
is unknown. No media, sidecar, codec, application or candidate operation was run.
No format test corpus is supplied. Input files must be independently validated;
unsupported input or unavailable prerequisites cannot produce a passing test.
See [the research owner](../research/media-file-workflows.md) for source limits.

## Observable model

Inputs are file/container/channel properties, import destination, cache volume
and settings, source/sidecar identity, analysis state and clip defaults/devices.
Observe accepted workflow/destination, cache/sidecar files, notification, waveform
readiness, clip membership and reference/device content. Internal decoder/kernel
selection and file structures are not prescribed. Numerical audio/time/byte
oracles remain U; qualitative defaults do not supply arbitrary metric tolerances.

## Requirements

### REQ-MEDIA-FILE-001 — Audio import surface

**D12; exact-build U.** Documented mono/stereo native formats are WAV, AIFF, AIFF-C, FLAC and OGG Vorbis. MP3 is importable; M4A import is macOS-only. Uncompressed input need not be converted beforehand solely for its sample rate/bit depth/length. Codec profiles, container variants, channels beyond stereo and practical bounds remain U. [Source sample-files](#source-sample-files).

### REQ-MEDIA-FILE-002 — Compressed source and cache

**D12; exact-build U.** Compressed import writes decoded uncompressed WAV data to a temporary cache file under Cache/Decoding. Cache retention and PCM contents are distinct from source identity; decode quality, early-playback readiness and completion timing remain U. [Source the-decoding-cache](#source-the-decoding-cache).

### REQ-MEDIA-FILE-003 — Cache eviction controls

**D12; exact-build U.** Older decoded files are automatically removed to make space. Maximum Cache Size can impose a configured limit; Cleanup deletes cached files not used by the open Set. Eviction order, active-reference definition and locking/transactions remain U. [Source the-decoding-cache](#source-the-decoding-cache).

### REQ-MEDIA-FILE-004 — Free-space refusal

**D12; exact-build U.** Minimum Free Space controls reserved disk space. A decoded file that cannot fit under the configured space policy produces a too-large/cache-full notification. Exact byte accounting, equality boundary and partial-file cleanup remain U. [Source the-decoding-cache](#source-the-decoding-cache).

### REQ-MEDIA-FILE-005 — Cache relocation

**D12; exact-build U.** Cache Folder Browse selects a different cache location. Migration, existing entries, unavailable destinations, permissions, concurrent readers and Set portability remain U. [Source the-decoding-cache](#source-the-decoding-cache).

### REQ-MEDIA-FILE-006 — Analysis file identity

**D12; exact-build U.** Analysis creates a sibling .asd associated with the sample, containing waveform/warp/tempo-analysis data. The filename retains the sample name with .asd. Exact naming edge cases and binary layout remain U. Analysis files are hidden from Live browser listings; a sample icon indicates presence. [Source analysis-files-asd](#source-analysis-files-asd).

### REQ-MEDIA-FILE-007 — Analysis readiness

**D12; exact-build U.** While long-sample analysis is in progress its waveform is grayed and the sample cannot play until analysis completes. Duration/threshold/thread scheduling and compressed-import interaction remain U; quick decoding does not imply analysis completion. [Source analysis-files-asd](#source-analysis-files-asd).

### REQ-MEDIA-FILE-008 — Existing analysis and long auto-warp

**D12; exact-build U.** A sample with an existing .asd is not analyzed again in the documented ordinary case. With Auto-Warp Long Samples off, long samples are not analyzed by that path. Stale/corrupt/version-mismatched sidecars and other analysis triggers remain U. [Source analysis-files-asd](#source-analysis-files-asd).

### REQ-MEDIA-FILE-009 — Disable sidecar creation

**D12; exact-build U.** Create Analysis Files off avoids ordinary-load .asd creation but analyzes samples on each load. It does not delete existing sidecars. Save Default Clip still generates a sidecar to store settings. Interactions with existing .asd/Auto-Warp and read-only media remain U. [Source analysis-files-asd](#source-analysis-files-asd).

### REQ-MEDIA-FILE-010 — Save Default Clip scope

**D12; exact-build U.** Save Default Clip stores default clip settings with the sample analysis file for later imports, including warp/gain/pitch settings. It does not change already existing clips using that sample. Exact persisted field set, precedence and identity matching remain U. [Source analysis-files-asd](#source-analysis-files-asd); [gain/pitch default context](#source-live-clips).

### REQ-MEDIA-FILE-011 — MIDI import ownership and destination

**D12; exact-build U.** MIDI file data is incorporated into the Set and resulting MIDI clips retain no reference to the source file. Import MIDI File inserts at the Arrangement Insert Marker or selected Session slot. SMF types, track expansion, channels, tempo/meter/program/SysEx and malformed input rules remain U. [Source midi-files](#source-midi-files).

### REQ-MEDIA-FILE-012 — MIDI export

**D12; exact-build U.** Export MIDI Clip opens a save dialog for a Standard MIDI File; it differs from saving a Live Clip. SMF type, timing division, quantization, event ordering/encoding and omitted data remain U; note-storage XML is not a MIDI codec oracle. [Source exporting-midi-files](#source-exporting-midi-files).

### REQ-MEDIA-FILE-013 — Live Clip source representation

**D12; exact-build U.** An exported audio Live Clip references external audio rather than embedding sample data. Live Clips retain clip/envelope settings and the original track devices. Save by dragging to Current Project or a user folder in Places; sample copying remains owned by project/media collection requirements. [Source live-clips](#source-live-clips).

### REQ-MEDIA-FILE-014 — Live Clip load destination

**D12; exact-build U.** Loading a Live Clip into a track with no clips or devices, or into empty no-track space, recreates its device chain. Loading into a track already containing clips or devices imports clip settings without its devices. Selected-track/return/group/nested-chain exceptions remain U. [Source live-clips](#source-live-clips).

### REQ-MEDIA-FILE-015 — Malformed and missing resources

**U; exact-build U.** Corrupt/truncated/unsupported audio, MIDI, ASD and Live Clip inputs, stale sidecars, missing referenced samples and unavailable cache volumes need exact refusal/repair/retry/data-retention outcomes. No blanket failure behavior is inferred from format names. [Source sample-files](#source-sample-files).

### REQ-MEDIA-FILE-016 — Cancellation and teardown

**U; exact-build U.** Cancel during decode/analysis/import/export, close Set/application, cache cleanup during active decoding and disk-full/permission races have no established termination, residual-file or rollback oracle. [Source the-decoding-cache](#source-the-decoding-cache).

### REQ-MEDIA-FILE-017 — Undo and persistence

**U; exact-build U.** Undo/redo of import/default-save/cache cleanup and save/reopen of decoded/analysis/default/reference state remain unknown beyond the narrower documented import/default clauses. No general byte equality or undoability is assumed. [Source live-clips](#source-live-clips).

## Acceptance cases

[Finite fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/fixtures.json)
are declarative prerequisites only. All32 [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/cases.json)
are unexecuted and ungraded for target compatibility. Unknown probes have null
predicates. File manipulation must use disposable copies when eventually run.

| Case | Requirement suffix | Kind | Action | Predicate or unknown |
| --- | --- | --- | --- | --- |
| MF-001 | 001 | positive | F1: import independently valid mono/stereo examples of each named native format at two supported rates/depths | Format eligibility only; sample identity/duration/value accuracy remain U |
| MF-002 | 001 | platform | F1: import valid MP3 and M4A separately on recorded macOS and Windows environments | M4A documented eligibility macOS-only; MP3 import eligibility; exact refusal UI elsewhere U |
| MF-003 | 002 | positive | F1: import MP3 into writable empty cache; record source and cache inventory before/after | Decoded temporary WAV under Decoding; exact PCM and source-deletion policy U |
| MF-004 | 002 | timing | F1: request playback before decode/analysis completes on large compressed file | No timing/ready oracle; independently capture decode and analysis states |
| MF-005 | 003 | positive | F2: one known cache entry referenced by open Set and one unused; invoke Cleanup | Unused cached file deleted; used open-Set entry is outside documented Cleanup target |
| MF-006 | 003 | boundary | F2: enable small Maximum Cache Size then import enough files to require eviction | Configured limit and automatic reclamation apply; exact victim/order/transient accounting U |
| MF-007 | 004 | negative | F2: independently measure insufficient usable space beyond Minimum Free Space for new decoded output | Too-large/cache-full notification; compare only documented refusal condition |
| MF-008 | 004 | boundary | F2: decoded output meets nominal free-space equality and differs by one byte | U: reservation/metadata/rounding/equality boundary unestablished |
| MF-009 | 005 | positive | F2: select separate valid writable folder with Cache Folder Browse | Selected cache location changes; whether prior entries migrate is U |
| MF-010 | 005 | error | F2: choose read-only/disconnected/nonexistent destination | U: rejection/fallback/dialog/dirty-state/file effects unestablished |
| MF-011 | 006 | positive | F3: never-analyzed sample in writable directory, default analysis options, ordinary first add | Sibling analysis sidecar created; precise pathological basename handling U |
| MF-012 | 006 | negative | F3: compare browser sample entries with/without sidecar and list sidecars in external directory inspection | Sidecar itself absent from browser listing; sample presence indication differs; icon pixels unmeasured |
| MF-013 | 007 | timing | F3: known long sample with confirmed analysis-in-progress state; request playback before and after completion | Gray/ineligible until complete; duration and threshold U |
| MF-014 | 008 | negative | F3: existing valid matching ASD in ordinary load case; separately no-ASD long sample with Auto-Warp Long Samples off | Ordinary reanalysis suppressed with existing valid ASD; documented long-sample path suppressed when off; other triggers U |
| MF-015 | 009 | negative | F3: Create Analysis Files off, no ASD initially; load sample, then load again with same independently recorded other settings | No ordinary-load sidecar creation; analysis each load under stated applicable analysis path; option interaction U |
| MF-016 | 009 | positive | F3: existing ASD, disable creation; separately Save Default Clip with no ASD while creation disabled | Disabling does not delete existing ASD; explicit Save Default Clip generates ASD |
| MF-017 | 010 | persistence | F3: clips A/B use same sample; adjust A warp/gain/pitch, Save Default Clip; import sample as C | C receives saved defaults; existing B unchanged by default-save; exact fields/values comparator U where unspecified |
| MF-018 | 010 | interaction | F3: altered source bytes/path identity or stale ASD after default-save, reimport | U: identity matching/default precedence/invalidation absent |
| MF-019 | 011 | positive | F4: Import MIDI File in Arrangement with known Insert Marker; repeat in selected empty Session slot | Insertion uses marker versus selected slot respectively; multitrack expansion U |
| MF-020 | 011 | persistence | F4: import source MIDI into copied Set, separately record resource reference before source file move | Imported MIDI loses source-file reference; exact note translation and reopen behavior U |
| MF-021 | 012 | positive | F4: select MIDI clip and invoke Export MIDI Clip, choose disposable output path | Save dialog and Standard MIDI File operation, distinct from Live Clip; no exact codec bytes oracle |
| MF-022 | 012 | boundary | F4: notes with equal times, overlapping notes, off-grid ticks, expression/tempo/SysEx/long delta fields | U: SMF encoding/inclusion/timing/event-ordering oracle absent |
| MF-023 | 013 | positive | F5: audio Live Clip with known sample reference and distinct device chain; save to supported Places folder | Reference-based audio and retained clip/envelope/device content; copying policy delegated to project/media |
| MF-024 | 013 | interaction | F5: save two variations of same source sample with distinct pitch/warp/envelope settings | Independent Live Clip ideas can share source reference; exact serialization U |
| MF-025 | 014 | positive | F5: import saved clip into empty track, then empty no-track space | Device chain recreated for both documented destination classes |
| MF-026 | 014 | negative | F5: import same clip into track with one existing clip but no devices, then one device but no clips | Clip settings imported without source devices for each nonempty condition |
| MF-027 | 015 | malformed | F1/F4/F5: separately truncated audio/SMF/ASD/Live Clip and missing sample reference | U: exact refusal/repair/partial result/error state absent |
| MF-028 | 015 | error | F2/F3: disk full or write permission denied while creating cache/ASD | U: retry/fallback/partial-file/Set-state outcomes absent |
| MF-029 | 016 | cancel | F1/F3/F4: cancel decode/analysis/import/MIDI export at individually recorded progress states | U: termination/rollback/output and source retention absent |
| MF-030 | 016 | teardown | F2: active decode/analysis, Cleanup then close Set/application on copied workspace | U: concurrency/handle/resource/residual-file outcomes absent |
| MF-031 | 017 | undo | F3/F5: import, Save Default Clip and Cleanup separately; request undo/redo | U: history availability/grouping and file/content restoration absent |
| MF-032 | 017 | persistence | F2/F3: save copied Set and reopen after relocating cache or removing sidecars | U: rebuild/reference/default/save behavior absent |

## Open obligations

Format names do not establish codec profile support or lossless round-trip.
Default analysis, existing sidecars, explicit Save Default Clip and disabled
Auto-Warp have different conditions; their complete interaction matrix is U.
A cache reclamation description does not establish LRU, active-reference locking
or crash recovery. MIDI codec and ASD/ALC accepted-byte grammars, all numerical
DSP, migration, races, error/cancel/undo/teardown outcomes remain unknown and
prevent complete coverage. No whole media or persistence family is closed.

## Analyst source appendix

Exact retained Managing Files and Sets source is reused without recapture:
SHA-256 `04fef126e1085053b790ea43b16596e33e82598ec54449418208e2b5fb9ad3d6`, with capture identity in the project/media
source metadata. No figures inspected. All citations are official documentary
predicates rather than observations of the installed build.

### Source analysis-files-asd

[analysis-files-asd](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manual-files-2026-10-19.html#analysis-files-asd), captured HTML line 296; exact digest above.

### Source exporting-midi-files

[exporting-midi-files](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manual-files-2026-10-19.html#exporting-midi-files), captured HTML line 460; exact digest above.

### Source live-clips

[live-clips](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manual-files-2026-10-19.html#live-clips), captured HTML line 460; exact digest above.

### Source midi-files

[midi-files](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manual-files-2026-10-19.html#midi-files), captured HTML line 448; exact digest above.

### Source sample-files

[sample-files](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manual-files-2026-10-19.html#sample-files), captured HTML line 280; exact digest above.

### Source the-decoding-cache

[the-decoding-cache](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manual-files-2026-10-19.html#the-decoding-cache), captured HTML line 280; exact digest above.
