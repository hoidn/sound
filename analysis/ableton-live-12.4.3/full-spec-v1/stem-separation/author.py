"""Author observable stem-separation workflows; no model or original-code execution."""
from pathlib import Path
import hashlib
import json

P=Path(__file__).resolve().parent
ROOT=P.parents[3]
blocks={r['id']:r for r in json.loads((P/'source-blocks.json').read_text())}
DATA=[
('Offline separation and source roles','The manual describes separation inside Live without Internet or additional external tools, for mono/stereo recorded audio. This is an offline-workflow claim, not a requirement to reproduce the named private deep-learning mechanism or accept every file/container. Existing media owners retain import/decode eligibility.',[6,7,8],'Use owned independently validated mono and stereo audio in separate copies with the feature already available, then compare admitted online and offline future trials without installing a tool.','control'),
('Command entry and options dialog','Separate Stems to New Audio Tracks is documented in context/Create menus for Browser audio files and Session/Arrangement audio clips; invoking it opens the separation options dialog. Exact unsupported input, command enablement and platform shortcut behavior remain unknown.',[10,11],'Select a known supported audio file in Browser, then an audio clip in each view in separate trials; invoke the documented offered command and inspect the options dialog.','control'),
('Element selection','Vocals, Drums, Bass and Others toggles choose included elements. Others denotes parts not detected as the other three. No exact classifier, perceptual-purity, reconstruction, source-isolation or stochastic-output law follows.',[7,12,32],'Inspect all four named toggles on a known multicomponent nonzero input; select each alone and distinct combinations separately without treating known source labels as an output audio oracle.','control'),
('Merge selection eligibility','Merge to Single Track combines selected parts and can be enabled only with two or three elements selected. With one or all four selected the checkbox cannot be activated. Zero-selected behavior, changing selection after enable and disabled-versus-hidden presentation are unknown.',[13],'After confirming Merge enabled with two selected elements, test one, three and four selected elements in separate reset dialogs, retaining the exact selected count. Keep zero-selected and selection-change history ungraded.','control'),
('Quality selector','The dialog offers High Speed and High Quality. They represent documented speed/quality choices, without a processing-time bound, SDR threshold, universal quality ordering, model identity or output-sample oracle.',[14,26,27,28,31,32],'On the same owned input inspect both offered modes and select each in separately reset dialogs. Any actual processing comparison needs independently retained output and a new calibrated metric.','control'),
('Separate and transport stop','Separate starts the process; if playback is running it stops when separation begins. Completion latency, stop timing, recording interaction, cancellation and failure atomicity remain unknown.',[15],'First establish active audible Set playback and a valid dialog/input; invoke Separate, retaining transport and process-state events. Repeat from stopped state separately; no timing deadline is supplied.','timing'),
('Separate multiple-element structure and colors','For multiple unmerged output elements, each resulting stem is a clip on its own track in a new Group Track. Stem track/clip colors correspond to dialog toggles; the group uses the source clip track color. Exact palette, source-less Browser color and track placement/order are unknown.',[16],'In an owned Set with explicit source-track color choose two and then four unmerged elements in separate copies; inspect created clip/track/group roles and displayed color relationships, without pixel values.','state'),
('Single and merged output structure','One separated element creates a single track/clip instead of a group. With Merge enabled the merged stem is placed on a new track whose track/clip color uses source track color. Exact input insertion position and effect/automation placement in these nongroup branches are unknown.',[17,18],'Use explicit source-track color and known eligible input; separate one element and then a merged pair in different Set copies, inspecting track/group presence and color roles.','state'),
('Clip region and warped-loop processing','For Session/Arrangement clips, adjusted start/end markers restrict separation to the audible region. With a warped loop, the manual describes processing from the start marker through the active loop region. Exact end inclusivity, loop cycles, offset mapping, Warp rendering and sample boundaries remain unknown.',[19],'Use independently indexed nonzero audio with distinct landmarks before/inside/after an interior region. Explicitly set start/end, Warp, loop start/end and transport; compare region and warped-loop setups in separate copies without a frame/sample oracle.','signal'),
('Arrangement time-selection command','Separate Stems for Time Selection is a clip context-menu route on an Arrangement time selection and opens the same dialog. After Separate, the clip splits at selection edges and only selected audio is processed. Exact boundary rounding, overlapping clips and transaction/undo behavior remain unknown.',[20],'Create a nonempty interior time selection in one owned Arrangement clip with distinct source landmarks, invoke its context command and Separate, then inspect resulting clip segmentation and stem region.','signal'),
('Effects and automation transfer for grouped outputs','In the documented grouped-output case, source-track audio effects are added to the Group Track rather than baked into separated audio; track automation goes to the group and clip automation/modulation to individual stem clips. This is a placement role, not a rendered equivalence or device identity/deep-copy law. Single/merged nongroup target placement is unresolved.',[21],'With two unmerged outputs, an independently active audible source effect, track automation and clip envelope/modulation at explicit distinguishable settings, inspect the new group/clip placements after separation. Retain positive wet/automation baselines before testing absence from stem files.','signal'),
('Source clip deactivation','After stems are created, the source clip is deactivated to prevent doubled output; selecting it and pressing 0 reactivates it. Exact key focus/layout, failed-process/cancel behavior and source-file rewriting are unknown; general clip activation remains with the editing owner.',[22],'Retain active nonzero source clip and successful stem creation in an owned copy, inspect deactivation, explicitly select it outside text/map mode and press0. Do not infer failed/cancelled work deactivates it.','state'),
('Browser destination and empty-Set tempo condition','Browser-source results go to Session or Arrangement according to focus. In an empty Set with warping for samples enabled in Record, Warp & Launch settings, project tempo is updated to source audio tempo. This conditional role does not define detection, empty-Set predicate, tempo estimate, beat conversion or behavior when the conditions are false.',[23],'In separate owned empty Set copies explicitly focus each view and enable sample warping, then select one known nonzero source in Browser and Separate. Retain source and tempo settings; compare nonempty/Warp-off only as ungraded branches.','timing'),
('Generated file destination and format roles','Stem files are documented under Current Project Samples/Processed/Stems. Merge also creates individual stem files along with the merged file. Output uses Record, Warp & Launch file type,44100Hz and source bit depth according to this captured chapter. Accepted source representations, names, collisions, file codec/resampling, metadata and target output values remain unverified.',[24],'With owned saved Project and independently validated source metadata, explicitly choose an offered file type, separate a merged pair and inspect created paths/headers independently. Retain source and output hashes without predicting bytes or resampling audio.','file'),
('High Quality Others dependencies','For High Quality with Others selected, all parts are processed even if only some are requested. The example Vocals+Others adds only those two to the Set, while Drums/Bass files are stored in Stems. This gives an externally documented file/Set distinction; it does not mandate private pass structure or a completion-time relation.',[30],'With High Quality explicitly selected and a known supported input, request Vocals+Others, then inspect Set clips and generated Stems files separately. Compare a no-Others subset in another copy without a performance or algorithm oracle.','file'),
]
GAPS={
 'OUTPUT':('Algorithm, numerical and boundary outcomes','Classifier/model output, quality/SDR/reconstruction, stochastic behavior, Warp/time/sample boundaries, accepted formats, bit-depth/file codecs and unsupported input/output remain required unknowns.',[
 ('AUDIO','Retain independent nonzero multicomponent owned stimuli, accepted positive separation, each output and source metadata; compare bleed, reconstruction and quality only after defining supported finite oracles.'),
 ('FORMAT','Use independently validated mono/stereo sources of distinct accepted rates/bit depths/file types, then separately truncated/unsupported/missing media, with no universal acceptance expectation.'),
 ('BOUNDARY','Test zero/one/two/three/four selected elements, Merge toggled before selection changes, empty/zero-length and edge clip/time/loop regions, retaining actual validity and no clamp/wrap rule.'),
 ('MODE','Compare repeated High Speed/High Quality and Others-selected/unselected runs on identical owned inputs; retain output hashes and file/Set state without a stochastic or speed/accuracy tolerance.')]),
 'PLACEMENT':('Single, merged and interaction gaps','Effects/automation placement for nongroup branches, Browser source-less color, device identity/parameter bindings, multiple-source/track ordering, time-selection fragment activation and source preservation remain unknown.',[
 ('NONGROUP','After a positive active-effect/automation grouped baseline, separate one element and a merged pair in reset copies, inspecting device/track/clip automation placement and actual nonzero output.'),
 ('BROWSER','Use a known Browser audio file with no source track, explicit focus and new-clip color preferences; inspect result/group colors and placement without importing a source-track color rule.'),
 ('SELECTION','With distinct nonzero audio before/inside/after an interior Arrangement selection, retain resulting original fragments and activation separately from stem clips; no atomicity or source-copy law is assumed.')]),
 'LIFECYCLE':('Lifecycle, failure and resource outcomes','Undo/redo/cancel/save, source/output loss, disk/network/build/feature availability, rate/resource limits, transport/record ordering and teardown remain required unknowns.',[
 ('UNDO','After successful owned separation, Undo/Redo separately and inspect tracks/groups/clips/effects/envelopes/source activation/generated files.'),
 ('CANCEL','Cancel an offered dialog before Separate and an offered active-process cancellation separately; inspect transport, source activation, partial files and cleanup without assuming cancellation availability.'),
 ('PERSISTENCE','Save/reopen a Project after grouped/single/merged/time-selection separation; inspect output references, activation and copied automation/effect ownership.'),
 ('LOSS','After positive admitted setup, remove/rename only owned source or output, make destination unavailable and constrain disk space in separate authorized disposable trials; inspect failures/partial outputs.'),
 ('RATE','Use supported changed sample rate/buffer/quality settings and separately repeated offline trials, retaining elapsed time and output without CPU/GPU topology, timeout or speedup claims.'),
 ('TRANSPORT','Request separation from playing/stopped/recording states, seek or change focus while pending and record ordering without presuming concurrent-command acceptance.'),
 ('TEARDOWN','Close dialog/clip/track/Set/application during pending separation in separate trials; inspect prompts, source activation and retained resources/files.')])}
reqs,cases=[],[]
for i,(title,contract,refs,action,kind) in enumerate(DATA,1):
 rid=f'REQ-STEM-SEPARATION-{i:03d}'
 evidence=[dict(block=f'STEM-B{n:03d}',anchor=blocks[f'STEM-B{n:03d}']['anchor'],html_line=blocks[f'STEM-B{n:03d}']['html_line']) for n in refs]
 reqs.append(dict(id=rid,title=title,contract=contract,strength='D12',target_applicability='U',evidence=evidence))
 visible=kind in {'control','state'}
 cases.append(dict(id=f'STEM-{i:03d}',requirements=[rid],kind=kind,fixture='fixtures.json#STEM-OWNED',setup_and_action=action,source_claim=contract,documentary_expected=contract if visible else None,documentary_comparator='Named visible menu/dialog/selection/track/clip state role only; no pixel, signal, timing, model or format grade.' if visible else None,expected=None,comparison=None,target_grade='U',executed=False,evidence=evidence))
for group,(title,contract,probes) in GAPS.items():
 rid='REQ-STEM-SEPARATION-U-'+group;reqs.append(dict(id=rid,title=title,contract=contract,strength='U',target_applicability='U',evidence=[]))
 for suffix,action in probes:cases.append(dict(id='STEM-U-'+suffix,requirements=[rid],kind=suffix.lower(),fixture='fixtures.json#STEM-OWNED',setup_and_action=action,source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,evidence=[]))
assert len(reqs)==18 and len(cases)==29 and len({c['id'] for c in cases})==29
def save(name,value):
 raw=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode() if not isinstance(value,str) else value.encode();p=P/name
 assert not p.exists() or p.read_bytes()==raw,name
 p.write_bytes(raw)
save('requirements.json',reqs);save('cases.json',cases)
helper=P.parent/'session-workflows/capture.py'
save('dependencies.json',[dict(path=str(helper.relative_to(ROOT)),bytes=helper.stat().st_size,sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),role='existing analyst chapter_content parser, no original code')])
save('fixtures.json',dict(id='STEM-OWNED',status='future owned setup only; no audio stimuli/stems/model/reference results supplied',setup='Owned saved editable Project, known accepted mono/stereo nonzero audio with independently indexed distinct start/interior/end landmarks and independently validated file type/rate/bit depth. Explicit Session/Arrangement/Browser focus, view, source/track/clip activation/color, nonempty region/loop/Warp, sample-Warp setting, quality/element/Merge choices and output file type. Active nonzero wet source effect, distinguishable track automation and clip envelope/modulation in placement cases; retain admitted positive baseline separately.',guard='First verify available feature and supported source, successful positive separation and active nonmuted/nonzero source/effect/output. Missing feature, source, permissions, muted signal or absent wet contribution leaves U, never a successful absence test. Use disposable copies for destructive commands and retain source/output hashes.',platform='Record exact target/build/edition, OS/hardware/audio rate/buffer and model availability independently. No installation, model download, original runtime, audio processing, hardware or candidate is executed by authoring this packet.'))
front='---\nid: {id}\ntype: {type}\nstatus: {status}\nupdated: 2026-10-19\naccess: analysis\nrevision: 1\ntarget: Ableton Live 12 Suite 12.4.3\n---\n\n'
spec=front.format(id='SPEC-STEM-SEPARATION',type='spec',status='draft')+'''# Stem separation workflows

This partial F-04/F-07 contract covers documented stem selection, dialog commands,
result placement, source-region/effect/automation roles and generated-file context.
The [coverage design](../research/full-live-specification-design.md) governs closure;
[research](../research/stem-separation.md) owns exact sources and interpretations.
This is not an audio/model specification, complete chapter coverage or released input.

**D12/target-U:** current Version12 manual prose only. Feature/command/model
availability in12.4.3 and all target outcomes/comparisons remain null/U/unexecuted.
All signal/timing/file documentary outputs/comparators are also null; source
claims are retained as context. No model, original application, audio processing,
native function, network, hardware or candidate ran. Figures were not inspected.

## Canonical boundaries

[Media](media-file-workflows.md) owns admitted source import/decode and generic
file/cache behavior; [Clip View](clip-view-workflows.md), [Arrangement](arrangement-editing.md)
and [Warp](warp-markers.md) retain region/loop/split/crop and finite marker laws.
This adds only stem-specific region/placement predicates, without stretching or
boundary algorithms. [Recording](recording-comping.md) retains output-format
settings; [project/media](project-media-workflows.md) owns file management.
[Racks](device-racks.md), [hosting](bundled-device-hosting.md),
[automation](automation-envelopes.md) and [routing](routing-monitoring-latency.md)
retain device/track/envelope semantics. This page adds transfer roles only.
Existing owner/releases and unknowns are preserved; no algorithm or finite law is expanded.

## Requirements

Use [future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/fixtures.json).
Confirm supported available inputs and active nonzero source/effect/automation
before absence/placement trials. Compound branches and missing case kinds stay
open. Feature label, silence, track presence or a file extension is not DSP proof.

'''
for r in reqs:
 spec+=f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}\n\n"
 if r['evidence']:spec+='Evidence: '+', '.join('`'+e['block']+'`' for e in r['evidence'])+'; [exact routes](#analysis-only-evidence).\n\n'
spec+='''## Source-context questions and acceptance proposals

**STEM-U-NONGROUP:** the source says effects/track automation go to a Group Track,
but one-element/merged results have no group. Retain the grouped predicate and
leave nongroup placement unknown rather than inventing a destination. Similarly,
Browser input has no source track for the source-track color relation.

**STEM-U-REGION:** start/end and warped-loop prose gives no inclusive endpoint,
cycle count, marker-to-sample/tempo map or fragment activation rule. Separate
Stems for Time Selection's split does not specify all original-fragment state.

[29 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/cases.json)
cover15D12 source-role proposals and14operational U probes, for18requirements
(15D12/3U). Eight documentary visible-control/state roles have proposed outputs;
seven signal/timing/file and all14U cases have null documentary outputs. All29
target expected/comparison values are null, grade U and unexecuted.

## Analysis-only evidence

'''
source=json.loads((P/'source.json').read_text())
spec+=f'''Official [Version12 Stem Separation]({source['url']}), captureUTC
{source['capture_utc']}, {source['bytes']}bytes, SHA-256 `{source['sha256']}`;
[retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/{source['file']}).
[32 source blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/source-blocks.json)
retain anchors/HTML lines; figures uninspected. The current website has no
immutable publication revision or exact12.4.3 pin. The parser is independently
pinned in dependencies.json. [Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/requirements.json)
and [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/manifest-author-r1.json)
freeze only this partial analyst scope. The manual's learning model/pass/CPU/GPU
statements remain research context, not candidate architecture or measured performance.
'''
research=front.format(id='RES-STEM-SEPARATION',type='research',status='current')+f'''# Stem separation evidence and unknown outcomes

The [canonical draft](../specs/stem-separation.md) follows the
[execution plan](full-live-specification-plan.md). No model, original application,
audio processing, network/download, native code, hardware or candidate ran.

## Exact source

Official [current Version12 chapter]({source['url']}), captureUTC
{source['capture_utc']}, {source['bytes']}bytes, SHA-256 `{source['sha256']}`;
[retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/{source['file']}).
No immutable publication revision or target12.4.3 feature/command/model guarantee
is established. The separate web reading view is not this byte identity.
The existing pinned Session analyst parser extracts only chapter_content;
[32 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/source-blocks.json)
retain headings/text/anchor/HTML lines. Figures and dialog colors were not inspected.

## Interpretation and scope questions

- Mono/stereo and offline-in-Live workflow prose supplies no every-format codec,
  model entitlement/download, neural architecture or exact output algorithm.
  The retained source describes a local learning model and pass structure;
  these internal explanations remain context, not required candidate design.
- High Speed/High Quality, SDR improvements, CPU/GPU distinctions and system-speed
  adjectives provide no retained benchmark, quality threshold or universal output
  ranking. Overlap between perceived sources is expressly possible. There is no
  pure-voice/drum/bass oracle, reconstruction identity or randomness guarantee.
- Merge eligibility has explicit two/three versus one/four source contexts.
  Zero selection and dynamic selection changes are unknown. Individual stem
  files for merged output and High Quality Others dependency files are observable
  distinctions; they do not require a private number of model inference passes.
- STEM-U-NONGROUP: effects/track automation placement prose names Group Track,
  while single/merged output has none. The draft scopes it to grouped results,
  retaining nongroup placement as U. Browser lacks a source-track color context;
  no fallback color or exact palette is inferred. Transfer does not establish
  device identity, parameter binding, DSP equivalence or envelope time base.
- STEM-U-REGION: audible-region/warped-loop and time-selection splitting gives
  no boundary inclusivity, loop cycle or marker/sample rounding law, or all
  original-fragment activation state. Existing editing/Warp owners stay canonical.
- Source deactivation follows successful creation, not every cancelled/failed
  attempt. Key0 needs actual focus/layout. Browser empty-Set/sample-Warp tempo
  role does not establish detection math, empty-Set definition or false-case law.
- Documented44100Hz/source-bit-depth/settings-file-type is an unexecuted file
  claim. Bit depth for compressed/float/unadmitted source, resampling and file
  names/metadata/collisions remain unknown. No generated file is supplied.

## Required next evidence and review

[18 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/requirements.json)
cover15D12roles/3U obligations; [29 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/cases.json)
retain15documentary proposals and14operational U probes. Eight visible-state
proposals have documentary outputs; all signal/timing/file/unknown outputs and
every target result remain null/U/unexecuted. Future owned stimuli and case setup
are not evidence of algorithm, target availability or source-output equivalence.
The [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/manifest-author-r1.json)
supports independent partial-scope review. Actual assets, algorithms, file and
region boundaries, single/merged placement, cancel/undo/persistence/source-loss,
rate/transport/teardown and exact-build applicability remain required unknowns.
'''
for name,text,canonical in [('spec-r1.md',spec,'wiki/specs/stem-separation.md'),('research-r1.md',research,'wiki/research/stem-separation.md')]:
 path=ROOT/canonical;assert not path.exists() or path.read_text()==text
 path.write_text(text);save(name,text)
print('18 requirements /29 cases authored; freeze/check separately')
