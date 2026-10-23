"""Write partial video-workflow analyst contracts from retained paragraph routes."""
from pathlib import Path
import hashlib
import json

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
blocks = {r['id']: r for r in json.loads((P / 'source-blocks.json').read_text())}
DATA = [
('Movie import', 'The current manual documents .mov QuickTime movies appearing in Browser and drag import into a Set. This is not a complete accepted extension/container/codec profile, OS entitlement or a rejection rule for other formats.', [6], 'Use a separately validated owned .mov with nonempty video/audio and import from Browser into an Arrangement audio track. Identify codec/streams independently; an unsupported fixture leaves U.', 'Named Browser/import route, not actual decode accuracy or all-codec compatibility.', 'control'),
('Arrangement versus Session', 'Video display is documented for movie clips in Arrangement. A movie placed in Session is treated as an audio clip. Audio-only Session treatment does not specify source-file rewriting or the behavior of a simultaneous Arrangement movie.', [7], 'On separately reset copies import the same known movie into Arrangement and Session; inspect clip type/view eligibility. Establish audible/visible positive input controls before observing the Session limitation.', 'View-dependent documented media role; rendering/audio and multi-movie window arbitration are ungraded.', 'control'),
('Video title indication', 'An Arrangement video clip is described with sprocket-hole markings in its title bar. Pixel geometry, asset, color, scale and accessible description are unknown; the source figure was not inspected.', [10], 'Compare known video clip title with a plain audio clip in Arrangement at an admitted view scale.', 'Documented video-title indication only; no image/pixel oracle.', 'control'),
('Edge trimming', 'Dragging the left or right Arrangement clip edge trims the video clip. The underlying audio/Arrangement edge-edit contract remains in SPEC-ARRANGEMENT-EDITING; frame/sample rounding, bounds and audio-video boundary alignment are unknown.', [11], 'With owned movie long enough for an interior region, trim left and right edges in separate copies, retaining source identity and displayed region.', 'The named edge gesture changes the clip region; exact decoded frames/samples and endpoints are ungraded.', 'control'),
('Audio-only results of processing commands', 'Consolidate, Reverse and Crop applied to a video clip replace it with an audio clip without altering the original movie file. This is a video-retention boundary, not a new audio processing/codec law. General command semantics remain with Arrangement and Clip View.', [11], 'In separate owned copies run Consolidate, Reverse and Crop in their supported Arrangement/Clip View contexts on the same video asset; inspect resulting clip media role and independently hash the original movie before/after.', 'Result is audio-only and original movie bytes remain unchanged according to D12; no generated-audio byte oracle or path cleanup guarantee.', 'state'),
('Floating Video Window', 'Video Window floats above Live\'s main window, can be moved, and has a visibility command in View. The text does not promise priority over other applications, OS dialogs or all display configurations.', [13], 'Open an Arrangement movie, move Video Window, toggle its View command, and place Live\'s main window under it. Do not infer OS-wide topmost behavior.', 'Named visibility/move and above-main relation; z-order conflicts and pixel geometry are unknown.', 'control'),
('Window size and location retention', 'Dragging the bottom-right Video Window corner resizes it. Its size/location are not Set-specific and are described as restored when a video is opened again. Persistence across full application/OS restarts, missing monitors and invalid geometry is unknown.', [13], 'Resize/move the window, close/hide and open a video again in the same session; separately open another owned Set/movie after recording the prior geometry.', 'Documented non-Set-specific size/location restoration; exact rounding, restart scope and cross-monitor fallback remain unknown.', 'state'),
('Full screen and original size', 'Double-clicking Video Window shows full screen, optionally on another monitor. Alt on Windows or Option on Mac plus double-click restores original video size. Full-screen exit gestures and OS-specific exclusive display policy are not supplied.', [13], 'With identified source dimensions, double-click Video Window, then perform the documented platform-modified double-click in a separate controlled trial. Use second monitor only if independently available.', 'Documented full-screen/original-size gestures; source-pixel-to-screen scaling and other exit behavior are unknown.', 'control'),
('Partial stream gaps', 'QuickTime movie audio/video streams may cover different intervals. During a video gap Video Window shows black; an audio gap plays silence. Missing-stream files, decoded sample floor, gap boundary inclusivity and background RGB are unknown.', [15], 'Use future owned .mov with independently indexed nonempty video/audio before and after a video-only gap and separate audio-only gap. Confirm valid positive playback on both sides before inspecting gaps.', 'Documented black/silence roles, with no frame/sample, color, timing or audio-threshold comparator.', 'signal'),
('Video tempo-leader prerequisite', 'The video clip Warp switch must be on to set Tempo Leader. The documented scoring setup uses video as leader and audio as follower; these are described defaults/guidance, not evidence of target constructor defaults. Warp algorithms and tempo-map arithmetic remain outside this packet.', [17,28], 'With movie in Arrangement, inspect Leader availability with Warp off/on, then explicitly select Leader and a separate audio follower. Do not rely on defaults.', 'Named Warp/Leader precondition and selection; clock/audio-video synchronization accuracy is ungraded.', 'control'),
('Active leader selection in the video setup', 'Of warped Arrangement clips marked Leader, the bottom-most currently playing clip is documented as the actual tempo leader. A nonplaying flagged clip is not described as the active leader. Exact overlapping-region boundary, hierarchy order and mapping from marker positions to tempo remain unknown.', [18], 'Use two overlapping owned warped Arrangement movie/audio clips flagged Leader, with independently distinguishable valid tempo maps; place them in different track order and repeat with one not playing.', 'Documented active/bottom-most role, but actual clock, precedence at a boundary and signal/time comparator remain unknown.', 'timing'),
('Nonleader video warping', 'An Arrangement video clip that is not the active tempo leader may become warped and produce warped video output. The source gives no frame interpolation/drop/repeat, codec, frame-rate or synchronization tolerance.', [19], 'Retain active positive video output and a separately confirmed different active leader; change its tempo map while movie is nonleader and record output for future analysis.', 'Documented possibility of warped video; no frame/time numerical oracle.', 'signal'),
('Warp-marker visual feedback', 'Dragging a video clip Warp Marker updates Video Window to the corresponding frame. The source does not give frame selection rounding, delivery deadline, exact decoded image or behavior while media is unavailable.', [21,29], 'On an owned movie with independently indexed distinguishable frames, drag a video Warp Marker between two interior positions with window visible; record marker and frame feedback.', 'Named video feedback during marker drag; exact frame/time/latency remains ungraded.', 'timing'),
('Embedded QuickTime markers', 'Embedded QuickTime markers are displayed as visual cues for placing Warp Markers. Accepted marker codecs, text encoding, counts, naming, duplicate positions and exact time conversion are unknown.', [22], 'Use future owned movie with independently verified embedded named markers at two interior times; import and inspect cue presentation before setting Warp Markers.', 'Documented marker cues, not a marker parser/serialization or frame-time oracle.', 'control'),
('Pre-roll working region', 'The documented scoring example puts a movie at Arrangement1.1.1 and moves its Clip View Start Marker past pre-roll so action begins at song start. This changes the working region, not the original movie. Generic start-marker editing remains with Clip View; SMPTE/sample conversion is unknown.', [33,34,35,36], 'Use owned movie with known two-second pre-roll and distinct action onset; place at1.1.1, open Clip View and move Start to that onset in a disposable copy.', 'Documented pre-roll exclusion in the working composition; exact display/timecode alignment and audio/video boundary remain unknown.', 'state'),
('Restoring pre-roll for delivery', 'The example restores pre-roll by moving the whole composition later, selecting the video alone and extending its left edge back to reveal the omitted material. Its selected movie then supplies the example export range. General export range/options/codecs remain in SPEC-AUDIO-VIDEO-EXPORT, not a universal output-duration promise here.', [37,38,39], 'After the pre-roll working-region setup and adding owned music, move all composition later by the known omitted interval; select video alone, reveal its left pre-roll and inspect intended selection before invoking the existing export workflow.', 'Documented edit sequence and selection intent only; exact snapping, recovered frame/sample boundaries and rendered bytes require separate oracles.', 'state'),
]
reqs, cases = [], []
for i, (title, contract, refs, action, expected, kind) in enumerate(DATA, 1):
    evidence = [{'block': f'VID-B{n:03d}', 'anchor': blocks[f'VID-B{n:03d}']['anchor'], 'html_line': blocks[f'VID-B{n:03d}']['html_line']} for n in refs]
    rid = f'REQ-VIDEO-WORKFLOW-{i:03d}'
    reqs.append({'id': rid, 'title': title, 'contract': contract, 'strength': 'D12', 'target_applicability': 'U', 'evidence': evidence})
    cases.append({'id': f'VID-{i:03d}', 'requirements': [rid], 'kind': kind, 'fixture': 'fixtures.json#VID-OWNED', 'setup_and_action': action, 'documentary_expected': expected, 'documentary_comparator': None if kind in {'signal', 'timing'} else 'Named visible controls, choices, source identity or state relationship only; no pixel, sample/frame or timing grade.', 'expected': None, 'comparison': None, 'target_grade': 'U', 'executed': False, 'evidence': evidence})
gaps = [
('MEDIA', 'Media/codec and numerical outputs', 'Decode, source/container/codec/frame-rate/marker/timecode/track-gap handling, missing streams, frame selection, audio output and resource limits remain required unknowns.', [
('FORMAT', 'Import unsupported/invalid extension, truncated .mov, valid container with unsupported stream codec and audio-only/video-only file in separate disposable trials.'),
('BOUNDARY', 'Move region/markers to source start/end, just outside bounds and adjacent to partial-stream gap; enter zero/negative/extreme positions without assuming clamp/reject policy.'),
('AUDIO-VIDEO', 'Capture active nonmuted positive audio/video baselines, then inspect known gaps, nonleader warping, frame/sample synchronization and processing transitions; no tolerance exists.'),
('MARKERS', 'Use duplicate/non-ASCII/large-count embedded markers and two distinct frame rates; observe text/order/time without presupposing a QuickTime marker codec.'),
('RATE', 'Use separately validated24/25/30fps/VFR inputs where accepted, request44.1/48kHz audio rates and window resizes; retain decoder/driver settings and no timing guarantee.')]),
('LIFECYCLE', 'Lifecycle, state and failure outcomes', 'Undo/cancel/save/source-loss, editing/tempo/transport ordering, window/display recovery, concurrency and teardown remain required unknowns.', [
('UNDO', 'Trim, Reverse/Crop into audio-only clip and change leader; Undo/Redo separately, inspecting media role, source files and visible state.'),
('CANCEL', 'Cancel an offered import/progress/processing dialog before commit; dismiss window gesture separately. Cancellation availability and partial-output cleanup are unknown.'),
('PERSISTENCE', 'Save/reopen a Set with trimmed movies, leader flags/markers and window geometry; reopen another Set and restart application in separate trials.'),
('SOURCE-LOSS', 'On owned copy rename/remove movie source, reopen and relink; repeat while pending frame feedback, without modifying retained originals.'),
('TRANSPORT', 'Stop/seek/restart across gap, clip end and active-leader boundary; change tempo/automation concurrently in separate trials. Record ordering without inventing deadlines.'),
('DISPLAY', 'Move Video Window to an independently available second monitor, disconnect/change scale in future supported setup and reopen video; record fallback, focus and accessibility.'),
('TEARDOWN', 'Close/remove video clip, track, Set and application during active video and separate pending import/editor action; observe prompts, resources and retained files.')]),
]
for group, title, contract, probes in gaps:
    rid = 'REQ-VIDEO-WORKFLOW-U-'+group
    reqs.append({'id': rid, 'title': title, 'contract': contract, 'strength': 'U', 'target_applicability': 'U', 'evidence': []})
    for suffix, action in probes:
        cases.append({'id': 'VID-U-'+suffix, 'requirements': [rid], 'kind': suffix.lower(), 'fixture': 'fixtures.json#VID-OWNED', 'setup_and_action': action, 'documentary_expected': None, 'documentary_comparator': None, 'expected': None, 'comparison': None, 'target_grade': 'U', 'executed': False, 'evidence': []})
assert len(reqs) == 18 and len(cases) == 28 and len({c['id'] for c in cases}) == 28


def save(name, value):
    raw = (json.dumps(value, indent=2, ensure_ascii=False)+'\n').encode() if not isinstance(value, str) else value.encode()
    path = P / name
    assert not path.exists() or path.read_bytes() == raw, 'Refuse changed authored artifact: '+name
    path.write_bytes(raw)


save('requirements.json', reqs)
save('cases.json', cases)
helper = P.parent / 'session-workflows/capture.py'
save('dependencies.json', [{'path': str(helper.relative_to(ROOT)), 'bytes': helper.stat().st_size, 'sha256': hashlib.sha256(helper.read_bytes()).hexdigest(), 'role': 'existing analyst chapter_content parser only; no original code'}])
save('fixtures.json', {'id': 'VID-OWNED', 'status': 'future owned setup; no movies, frames, audio or reference results supplied', 'media': 'Independently validate/hash owned QuickTime MOV with distinct frame landmarks, nonzero audio, two-second pre-roll and both streams on either side of separately indexed audio/video gaps; retain frame-rate/timebase/codec/stream intervals/marker metadata. Separate movie with embedded QuickTime markers and audio-only control asset.', 'set': 'Disposable editable Set; Arrangement audio tracks for movies/music, Session audio-only comparison, explicit Warp/Leader/region/markers/project tempo and meter/automation, known focus and display config. No implicit target defaults.', 'positive_guard': 'First retain working visible video and active nonmuted/nonzero audio output. For gap/absence tests confirm appropriate streams/paths on both sides independently; absent codec/source, hidden window, muted output or zero audio is not a passing gap test.', 'platform': 'Record target OS/build, decoder, displays, audio driver/rate and supported settings. Linux analyst host does not establish original UI/video availability; second monitor/editor/hardware are not provisioned.', 'destructive': 'Use owned disposable copies; retain source hashes before/after commands. Never edit immutable source captures or published releases.'})
front = '---\nid: {id}\ntype: {type}\nstatus: {status}\nupdated: 2026-10-19\naccess: analysis\nrevision: 1\ntarget: Ableton Live 12 Suite 12.4.3\n---\n\n'
spec = front.format(id='SPEC-VIDEO-WORKFLOWS', type='spec', status='draft')+'''# Video import, presentation and scoring workflows

This partial F-07 contract owns video-specific import/presentation, movie-to-audio
processing boundaries, scoring/marker feedback and pre-roll editing. The
[coverage design](../research/full-live-specification-design.md) governs closure;
[research](../research/video-workflows.md) owns exact evidence and interpretation.
It is not a complete video/codec specification or a released implementation input.

**D12/target-U:** the official Version12 chapter captured2026-10-19 supports
documentary prose only. Every exact12.4.3 outcome/comparison is null/U/unexecuted.
Figures were not inspected; there are no movie/frame/audio reference fixtures,
codec proofs, pixel/signal/time tolerances, runtime runs or candidate results.
U never passes. Missing assets/decoder/display capabilities remain prerequisites.

[Media](media-file-workflows.md) owns general source/cache behavior;
[Arrangement](arrangement-editing.md) and [Clip View](clip-view-workflows.md) own
generic clip editing and audio processing. This page adds only video-specific
predicates; video replacement does not change their audio algorithms. [Warp](warp-markers.md)
owns marker storage/finite conversion; its broader tempo-leader/algorithm scope
remains open. Leader selection here is only the captured video setup's documented
role, without a tempo-map or frame scheduler law. [Export](audio-video-export.md)
owns render ranges/options/encoding/errors, [project/media](project-media-workflows.md)
owns general relinking, and [keyboard navigation](keyboard-navigation.md) owns
global focus/Tab settings. The chapter's generic Tab/view instructions are routed
there rather than repeated without their preference conditions. External video
synchronization remains a separate pending contract.

## Requirements

Use the [finite future setup](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/fixtures.json)
and reset histories/configuration per case. Independently confirm visible video
and active nonzero audio before any black/silence/continuity assertion. Nominal
MOV extension, zero send, absent stream, hidden window or failed decoder cannot
establish the tested behavior. All compound clauses remain partial until their
individual branches, source outcomes and required case kinds are closed.

'''
for r in reqs:
    spec += f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}\n\n"
    if r['evidence']:
        spec += 'Evidence: '+', '.join('`'+e['block']+'`' for e in r['evidence'])+'; [exact source routes](#analysis-only-evidence).\n\n'
spec += '''## Finite acceptance proposals

The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/cases.json)
contains full finite actions, source references and documentary proposals; the
table is an index. There are18requirements (16 D12/2 U) and28cases:16 documented
proposals plus12operational U probes. Two signal/two timing proposals have null
documentary comparators; every target expectation/comparison is null and grade U.

| Case | Requirement | Kind / action |
| --- | --- | --- |
'''
for c in cases:
    spec += '| '+c['id']+' | '+c['requirements'][0]+' | '+c['kind']+': '+c['setup_and_action']+' |\n'
source = json.loads((P / 'source.json').read_text())
spec += f'''
## Analysis-only evidence

- Official [Version12 video chapter]({source['url']}),
  captured{source['capture_utc']}, {source['bytes']}bytes, SHA-256
  `{source['sha256']}`; [exact HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/{source['file']}).
- [39 paragraph/heading/list locators](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/source-blocks.json)
  retain exact section anchors/HTML lines; [text view](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/source-blocks.txt)
  is navigation only. The imported existing analyst parser is pinned in dependencies.json.
- [Requirement catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/requirements.json)
  and [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manifest-author-r1.json)
  freeze the partial draft for independent review. No prior release is expanded.

No domain/codec enumeration, performance promise, CPU/decoder/thread architecture,
memory law, synchronization limit or complete platform support follows from this
manual. All error/cancel/undo/persistence/source-loss/rate/teardown, missing-stream,
frame/timecode and image/audio numerical outcomes remain required unknowns.
'''
research = front.format(id='RES-VIDEO-WORKFLOWS', type='research', status='current')+f'''# Video workflow evidence and limits

The [canonical draft](../specs/video-workflows.md) owns behavior under the
[full specification plan](full-live-specification-plan.md). This source review
adds a bounded video contract without changing export, audio editing or Warp's
finite computations. No original program, decoder or candidate ran.

## Exact capture

Official [Version12 chapter]({source['url']}), retained
[HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/{source['file']}),
{source['bytes']}bytes, SHA-256 `{source['sha256']}`,
captureUTC {source['capture_utc']}. The current website says Version12, without
an immutable publication revision or exact12.4.3 guarantee. A separate web-tool
view was used for reading; this retained HTML is the evidentiary byte identity.
Figures were not inspected. Exact capture metadata is in
[source.json](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/source.json).

[39 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/source-blocks.json)
are extracted only from chapter_content using the existing Session analyst parser,
pinned independently in dependencies.json; inline image glyphs are not inferred.
The source supports16documentary requirements, not full movie/codec compatibility.
Two additional requirements retain12operational U probes. Every target outcome
is null/U/unexecuted; proposed input movies/frames/audio are not supplied results.

## Interpretation and ownership

- MOV/QuickTime is a documented import case, not a complete decoder or extension
  table. Browser presence, a file extension or resource service identity cannot
  establish codec support, unsupported-format errors or Linux UI availability.
- Video is displayed in Arrangement; Session uses the movie as audio. Other
  simultaneous movies, window arbitration and missing streams remain unknown.
- Consolidate/Reverse/Crop's audio-only replacement and source-movie preservation
  are video-specific predicates. The existing editing owners retain audio paths,
  generated file formats, processing methods and transaction/error gaps.
- Video Window floats above Live's main window, not every OS application. Its
  geometry is not Set-specific; restart/missing-display persistence is unproven.
- Black/silent gaps need independently verified partial streams and positive
  playback on both sides. No color value, silence floor or frame boundary follows.
- Leader flag/Warp prerequisite and active-bottom-most relation are documentary
  setup roles. Exact tempo-map/frame interpolation, leader handoff and event
  scheduling are unknown; no private candidate mechanism is required.
- Embedded marker and Warp-drag feedback prose gives no QuickTime marker codec,
  timebase/rounding or decoded-frame comparison. Other chapter links are context,
  not captures or additional source support.
- Pre-roll steps describe one selected-movie delivery example. They do not
  override the export owner's range/options or promise every render matches the
  source duration. Generic view Tab shortcut follows its global settings owner.

## Review and next evidence

[Future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/fixtures.json)
must retain exact movie/stream/frame/marker metadata, source hashes and accepted
target configuration before execution. Owned copies isolate destructive command,
undo/cancel/persistence/source-loss/display/rate/teardown probes. No window, video
decoder, external editor/display or synchronization hardware was provisioned.
The [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manifest-author-r1.json)
pins the reviewable draft. Separate semantic review, exact-build evidence and
calibrated output comparisons remain pending. No whole family is complete.
'''
for name, value, canonical in [('spec-r1.md', spec, 'wiki/specs/video-workflows.md'), ('research-r1.md', research, 'wiki/research/video-workflows.md')]:
    path = ROOT / canonical
    assert not path.exists() or path.read_text() == value
    path.write_text(value)
    save(name, value)
print('18 requirements /28 null-target cases authored; freeze/check separately')
