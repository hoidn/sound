"""Bounded documentary launch workflows using four preserved source files; no execution."""
from pathlib import Path
from collections import Counter
import json
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
BLOCKS={b['id']:b for b in json.loads((P/'source-blocks.json').read_text())}
REQ=[]; CASES=[]
def write(name, value):(P/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
def add(numbers, kind, title, contract, action, fixture='CLIPS'):
 n=len(REQ)+1; rid=f'REQ-SESSION-LAUNCH-{n:03d}'; refs=[f'LC-B{i:03d}' for i in numbers]
 assert all(r in BLOCKS for r in refs)
 REQ.append({'id':rid,'provenance':'D12','target_applicability':'U','title':title,'contract':contract,'source_id':'D12-LAUNCHING-CLIPS','source_blocks':refs})
 graded=kind in ['documented-control','documented-state']
 CASES.append({'id':f'SLC-{n:03d}','requirements':[rid],'kind':kind,'provenance':'D12','fixture':'fixtures.json#SLC-F0','fixture_group':fixture,'preconditions':['common','active-follow-guard' if fixture in ['FOLLOW','SCENES','CHAIN'] else 'active-signal-guard'],'setup_and_action':action,'source_claim':contract,'documentary_expected':contract if graded else None,'documentary_comparator':'Compare only named visible setting eligibility/selection/indicator relations. This is a documentary proposal, not a target runtime grade.' if graded else None,'expected':None,'comparison':None,'target_grade':'U','executed':False,'source_blocks':refs})
rows=[
([4,5,6],'documented-control','Session launch setting scope','Launch settings apply to Session clips, not Arrangement timeline clips. Session Clip View exposes them; multi-selection supports editing launch settings together. Shared panel/grid selection belongs to existing owners.','Select A then B Session clips and inspect launch panel; multi-select A/B and edit one offered mode. Select Arrangement copy and inspect launch-setting eligibility. Full multi-edit transaction/domain rules remain U.'),
([8,9],'launch-obligation','Trigger gesture role','Trigger: down starts clip; release is ignored. The source covers mouse, key and mapped MIDI-note gesture categories but supplies no dispatch/frame/note-off matching law.','A Trigger, clip quantization None, transport running; down at recorded beat1.25, release beat1.75. Repeat with stopped transport and declared supported key/MIDI mapping in independent trials; actual playback/timing is U.'),
([8,10],'launch-obligation','Gate gesture role','Gate: down starts and up stops. Exact quantized release, held/repeated MIDI pairing and cancellation remain U.','A Gate, clip None then1 Bar; press/release spanning and entirely before one grid boundary. Use audible active baseline; compare mouse/key/MIDI routes only when independently mapped.'),
([8,11],'launch-obligation','Toggle gesture role','Toggle: down starts, up is ignored, next down stops. Multiple input-source arbitration and grid-boundary timing remain U.','A Toggle; down/up/down with recorded distinct request times at clip None then1 Bar. Repeat mixed-source duplicate downs only as unknown control-context probe.'),
([8,12],'timing-obligation','Repeat gesture role','Repeat retriggers while input remains held at clip quantization rate. None/Global edge behavior, first/last repeat and exact timing are not supplied.','A Repeat with explicit clip 1/4, down at off-grid time, hold through four grid opportunities then release; retain output/request log. Repeat at None/Global only in U boundary cases; no numeric cadence comparator.'),
([14,15,16],'launch-obligation','Legato takeover role','Launching Legato clip takes previous clip play position in same track, including with quantization off. Position units, wrap, unequal lengths and activation timing are unproven for target.','A/B equal-length audible loops on same track, distinct content, Legato enabled on incoming B, clip None. Launch A then B off-grid and switch back in reset trials; inspect future position evidence without presuming modulo/start-field formula.'),
([17],'signal-obligation','Legato media and RAM context','Different-sample Legato jumps may cause dropouts because material was not preloaded; Clip RAM is documented as remedy. This is no zero-dropout, deadline or RAM/disk-load guarantee.','Same-sample A/B differing settings then distinct-sample A/B at Legato; RAM off/on, nonzero output and actual valid media in each. Retain render if future evidence exists; no dropout count or continuity acceptance threshold.'),
([19,20],'documented-control','Quantization selector roles','None disables launch onset correction; Global selects Control Bar quantization. Existing enum/grid/Trigger arithmetic retains its canonical owner and assumptions; Follow Action Global behavior is separately unresolved.','Inspect clip None, Global and explicit1 Bar under global1/4; compare selector states only. Global shortcuts/settings ownership remains keyboard/clip-launch canon, not redefined here.'),
([23],'signal-obligation','Launch velocity endpoints','Velocity Amount0 gives no launch-note-velocity volume influence;100% says softest notes play silently. Softest valid launch velocity, interpolation, volume codec and non-MIDI launch response remain U.','Valid mapped MIDI-note launch, active output: velocities1/64/127 if supported, Amount0 then100. First establish positive output at127/nonzero gain; no velocity0 NoteOn assumption or amplitude formula.'),
([25],'timing-obligation','Nudge role','Nudge Backward/Forward jumps within playing clip by global quantization period. Source/file/loop bounds, None behavior and exact rounding remain U.','A playing, global1/4 then1 Bar, clip region longer than both; invoke each nudge at retained play positions. Playback-position and clock output remain ungraded.'),
([26],'documented-control','Nudge and scrub mapping affordances','Nudge buttons can map to keys/MIDI; MIDI Map Mode reveals a scrub control between buttons for rotary-encoder continuous scrubbing. Mapping codec/takeover/relative interpretation remains outside this clause.','Enter MIDI Map Mode with A selected; inspect scrub control and Nudge targets, exit and inspect ordinary panel. Actual controller setup must come from an independently supported mapping context.'),
([27],'timing-obligation','Offset relative to master clock','Sub-bar quantization plus launch, nudge or scrub can offset clip playback relative to master clock. It does not specify a phase-offset equation or reset law.','A global 1/16 and explicit clip 1/16, launch off-grid then nudge/scrub separately; retain master/clip positions and settings. Do not accept an offset formula from launch arithmetic.'),
([29],'documented-state','Clip Follow groups','Clip Follow Actions operate within successive occupied slots on one track; empty slots separate groups. Group definition here is clips, not a proven scene-group/empty-scene rule.','FOLLOW setup:slots 1-3 A/B/C,4 empty,5-6 D/E. Inspect/retain occupied/empty layout and action target roles; moving/removing/filling slots remains U boundary probe.' ,'FOLLOW'),
([30,31],'documented-control','Scene Follow entry and local enable','Follow Actions also have Scene View controls. Selected clip/scene local Follow button enables/disables them; source describes default disabled and Shift+Enter toggle. Actual constructor/focus/default-load state remains U.','Select A then populated scene S1 separately, record local button state and focused Shift+Enter off/on; keep global Follow enabled and valid populated targets. Do not treat scene selection itself as launch.','SCENES'),
([32],'documented-control','Two action choices','Each clip/scene exposes two Follow Action choices, A and B. Exact labels/images versus stored-code associations stay with scoped enum evidence and U control-context work.','Select A then scene S1, inspect A/B choice controls without reading inline action images as text; record actual offered actions/context.','FOLLOW'),
([33],'rng-obligation','Chance endpoints','The source says A 100%/B 0% selects A every launch and0% suppresses its action. The later B 90%/~one-in-ten example leaves actual coupled-field changes unspecified; no general probability or normalization law follows.','A with both local/global Follow enabled and valid Next-role positive baseline, set A 100/B 0 via actual UI, retain both displayed and saved fields. Future action outcomes remain U; record but never impose statistical convergence in finite trials.','FOLLOW'),
([34],'documented-control','Linked versus scene eligibility','Linked/Unlinked is clip-only; Linked is described as default. Follow Time is exposed for both clips and scenes. No saved-field/default constructor parity is inferred.','Inspect A clip and scene S1 Follow controls, including Time; compare Linked/Unlinked switch eligibility. Test fresh versus loaded defaults separately as U.','SCENES'),
([34],'timing-obligation','Linked timing role','Linked clip Follow occurs at clip end or after number of loops in Multiplier. Which region/end/loop accounting, nonlooped clips and clock rounding require target evidence.','A Loop on, distinct nonzero Start and LoopStart, Multiplier 1 then2; local/global Follow on, Next role to audible B. Repeat loop off with same fields; record positions/outcomes without imposing numerical schedule.','FOLLOW'),
([34],'timing-obligation','Unlinked Time role','Unlinked clip Follow uses duration in Follow Time; clip/scene Time is bars-beats-sixteenths from point where play starts. Default one bar and editor marker drag are documentary only; exact meter/offset codec remains U.','A Unlinked Time 1.0.0 then0.2.0 and nonzero Start; drag editor marker and inspect Time. SceneS1 separately Time 1.0.0, global/local enabled, populated destination. No launch-grid formula transferred.','SCENES'),
([36],'follow-obligation','No-follow role','The no-follow description says no Follow occurs; once clip is triggered with No Action, other selected Follow Action in that clip no longer gets a chance even if its Chance100%. Re-launch/re-enable/reset scope remains U.','A local/global enabled, choose documented no-follow role versus Next role in separate reset trials, valid B and active audio; retain branch/activation and later relaunch state. Never infer probability ordering from both chances100.','FOLLOW'),
([37],'follow-obligation','Stop role','Stop description stops clip after chosen Follow Time, overriding clip loop/region settings. Exact linked/unlinked preconditions, stop grid and note/tail cutoff are U.','A looping with region longer than Time, Follow enabled locally/globally, Stop role and nonzero output; compare with Next positive transition to B. Source role label association/frame/audio result remains U.','FOLLOW'),
([38],'follow-obligation','Restart role','Restart description restarts clip; start marker, Legato interaction, repeat counters and exact dispatch are not provided.','A nonzero Start with audible marked content, local/global Follow enabled, restart role and explicit Time; separate Legato off/on trials. Positive restart/transition prerequisites retained; no assumed sample position.','FOLLOW'),
([39],'follow-obligation','Previous role','Previous description triggers clip immediately above current. Top-of-group wrap or escape across empty slot is not documented here.','B within valid A/B/C group, Previous role and active local/global Follow; compare top A only as U boundary. A and B independently audible; no automatic top-wrap assumption.','FOLLOW'),
([40],'follow-obligation','Next and clip wrap','Next description selects next clip down within group; last clip wraps to first. This clip statement is not applied automatically to scene-empty-group boundaries.','B Next to C, then C Next to A in independent FOLLOW trials; D/E separate group beyond empty slot. All targets populated, audible and local/global Follow enabled; runtime identity/time ungraded.','FOLLOW'),
([41],'follow-obligation','First role','First description launches top clip in group. Exact empty-slot/reordering/concurrent group edits remain U.','B First-role targeting groupA/B/C, distinct active A; D/E beyond gap remain outside this clip group setup. Local/global Follow and active nonzero output required.','FOLLOW'),
([42],'follow-obligation','Last role','Last description launches bottom clip in group; self-target behavior when already last remains unresolved.','A Last-role withinA/B/C, distinct activeC, enabled local/global; test C Last separately in U boundaries without assuming self-retrigger/sustain.','FOLLOW'),
([43],'rng-obligation','Any role','Any description permits any clip in group; source gives no uniformity, independence, seed, repeat history or finite completion guarantee.','A/B/C group, Any role with local/global enabled; each member independently active/audible. Retain a finite trace only as observations; do not require every member or absence of repeat in a finite run.','FOLLOW'),
([44],'rng-obligation','Nonconsecutive role','Other-like description excludes consecutive same clip while current clip is not alone in group; singleton exception does not establish a specific fallback/retrigger law.','A/B/C group with active valid members, then isolatedD singleton in separate layout; local/global enabled. Future repeat trace U; no uniformity or guarantee every other clip chosen.','FOLLOW'),
([45],'documented-control','Jump selector role','Jump exposes Jump Target slider for target clip slot or scene; drag or numeric entry adjusts target. UI numbering, stored jump fields, invalid/empty target behavior and action/image associations remain U.','A clip then scene S1, choose actually offered Jump, inspect slider and two populated targets with retained actual displayed numbers; do not infer one-based/zero-based encoding from existing stored enum fields.','SCENES'),
([46],'documented-state','Assigned Follow indicator','Clips/scenes with assigned Follow Actions show striped launch buttons. Assigned versus enabled versus stored default fields is unresolved control context.','Independently retain assigned/local-enabled/global-enabled state for A and S1; inspect striped launch indicator, then vary local/global switches in separate U trials. No pixel/image-source interpretation.','SCENES'),
([48],'documented-state','Global Follow enable','Enable Follow Actions Globally governs all clip and scene Follow Actions. Source says grayed when Set contains none; which fields count as present versus assigned/enabled remains U.','Valid enabled clipA and scene S1, global on/off with active positive transition baseline. Inspect button eligibility in separately confirmed no-Follow Set; do not equate default stored A/B values with presence.','SCENES'),
([49],'follow-obligation','Scene precedence role','Clip Follow continues while scene Follow is created/scheduled; scene Follow takes precedence once triggered. Exact same-time priority, affected tracks and pending-request cancellation are U.','A clip Follow scheduled before S1 scene Follow in separate non-tie windows, both local enabled plus global enabled; S1/S2 populated active clips. Retain selected/playing/pending states; no frame or tie oracle.','SCENES'),
([60,61],'follow-obligation','Cycle construction role','Source describes Next cycles of clips or scenes and occasional alternatives using lower relative chances. This is no general scene-group/wrap or RNG law.','Three populated clips in one group, then three populated scenes separately; Next-only configuration and global/local Follow enabled. Observe finite trace without claiming ad infinitum success or extending clip empty-slot grouping to scenes.','SCENES'),
([62],'documented-control','Create Follow Action Chain','Clip context Create Follow Action Chain sets selected clips to cycle; selection need not be contiguous. Generated action codes, order, times, chances, enable flags and gap crossing are not specified.','Select A, C, E noncontiguously on one track in CHAIN setup, invoke context command and retain resulting controls/selection. Each source clip valid, audible; enable local/global if needed for later ungraded playback.','CHAIN'),
([53,54,55,56,57,58],'follow-obligation','Intro into loop composition','Documented recipe splits nonlooped introduction from looping tail, places adjacent Session clips, sets first Next 100 and Time to first duration, second Loop on. Editing/transfer owners retain their own laws; exact derived timing remains U.','Owned long source split at retained intro/tail boundary via existing Arrangement owner, place A/B adjacent. First local/global enabled, Unlinked Time retained with Next 100/B No Action 0; second Loop on with its Follow disabled to isolate example. Positive A/B playback confirmed; no sample equality.','FOLLOW'),
([65,66],'rng-obligation','Temporary restart composition','Single-clip Play Again 80/No Action 20 example restarts a portion and may later continue; the source eventual-language supplies no bounded-trial deadline or finite guarantee. A subsequent looping clip can have separate Follow configuration.','Singleton A, long audible source, Time one bar, Unlinked, Loop off, A restart80/B no-follow20, local/global enabled. Finite traces retained U; never require No Action within N trials or infer RNG seed/distribution.','FOLLOW'),
([68,69],'follow-obligation','Legato Follow variation role','Legato Follow can transfer beat-time position among similar clips with differing settings/envelopes/notes. This describes composed roles, not audible identity or complete automation/warp interaction.','A/B/C equal-length same-note clips, all incoming Legato on, Next-only locally/globally enabled; alter one clip envelope under its owner. Confirm each active/nonzero baseline; future position/audio output U.','FOLLOW')]
for row in rows:add(*row)

unknowns=[
('GLOBAL-FOLLOW','Global Follow quantization wording is unresolved between LC-B021 and LC-B047; no rule is selected.',[
('GLOBAL-FOLLOW','timing','FOLLOW A Unlinked at retained off-grid Time, Next-role B; local/global Follow on, valid A/B, active output. Compare clip None, clip Global with global 1 Bar, clip Global with global None, and explicit clip 1/4 in reset copies.','LC-B021 includes Global in non-None quantization; LC-B047 says Global bypassed. Same mode/preconditions and engine path are unproven; timing/frame oracle null.'),
('GLOBAL-UI','control-context','For the same cases retain selected UI quantization, actual saved fields, global Follow enable and exact request/trigger context; compare Linked versus Unlinked and clip versus scene separately.','Source scope/version/implicit controls may differ; existing Trigger dispatch/grid laws do not settle Follow paths.')]),
('CHANCE-COUPLING','Chance A/B coupled editing, actual fields and probability/RNG law remain unknown.',[
('CHANCE-UI','control-context','FOLLOW A 100/B 0, drag B to90 then separately type90 and use central slider; record both displayed controls and saved values after each gesture. Repeat on scene S1 with global/local enabled and valid active destinations.','No inference A stays100 or becomes10; source example omits coupling/actual state. Old load-time normalization is not UI editing or chance-selection proof.'),
('CHANCE-TRACE','rng','Retain finite trace of valid A/B choices under independently captured displayed/saved fields at0/100,80/20 and100/90 if actually accepted; repeat restart/seed contexts only as observations.','No normalization,100/(100+90), uniformity, independence, statistical tolerance or eventual finite success criterion supplied.')]),
('ACTION-CONTEXT','Image/label/action identity and target control contexts remain unknown beyond released stored enum vocabulary.',[
('ACTION-LABELS','control-context','Compare actually offered action labels/menus, selected numeric fields and retained runtime context for all ten role descriptions. Inline action images remain uninspected; do not derive text from filenames/alt strings.','Released enum vocabulary does not prove current UI label set or source image-to-role/runtime mapping. Where labels unavailable, record U rather than invent association.'),
('ENABLE-INDICATORS','control-context','A/S1:record assigned choices/local enabled/global enabled independently, including default choices while local off and global gray/non-gray. Active transition baseline uses both enables.','Assigned/present/striped/global eligibility and Shift+Enter focus are not settled from stored default fields or prose alone.')]),
('BOUNDARIES','Region/group/target/time endpoints and ordering require exact target evidence.',[
('GROUP-BOUNDARY','boundary','FOLLOW layout A/B/C-gap-D/E; Previous from top, Next from C/E, First/Last self-target, Other in singleton. Fill gap, move/delete current/destination while pending in separate trials.','Only documented clip Next wrap is supported as source role; previous wrap, regrouping snapshot, destination loss and singleton fallback U.'),
('JUMP-BOUNDARY','boundary','Clip/scene Jump to populated, empty, self, first/last displayed target then zero, negative and out-of-range entry on owned copies; global/local on.','UI indexing/clamp/reject/empty-scene effects, stored conversion and pending target identity U.'),
('TIME-BOUNDARY','boundary','Linked Multiplier 1/2 then0/negative/large if offered; Unlinked Time zero/negative/one-sixteenth and across nonzero Start/LoopStart, unequal lengths/meters and Loop off.','Input acceptance, end/loop count/units/normalization/default and zero-time scheduling U; no launch arithmetic assigned.'),
('PRESS-BOUNDARY','boundary','Trigger/Gate/Toggle/Repeat with duplicate down/up, release-before-quantized-start and missed release; different mapped keys/MIDI same target; Repeat None/Global; Legato no prior clip or unequal loops.','Gesture pairing/cancellation/voice/note cleanup, Repeat period/first-last event and Legato wrapping U.'),
('SCENE-BOUNDARY','boundary','Populated S1/S2/S3 plus empty S4; sceneNext/Previous/Jump across gaps, simultaneous sceneFollow and clipFollow/manuallaunch/globaldisable at captured time.','Scene grouping/wrap/empty targets, same-time priorities and atomic track/clip outcomes U.')]),
('CLIP-LIFECYCLE','Clip-specific automation, storage/error/cancel/rate/teardown remain required unknowns.',[]),
('SCENE-LIFECYCLE','Scene-specific automation, storage/error/cancel/rate/teardown remain required unknowns.',[])]
life=[
('AUTOMATION','automation','Automate two accepted settings and one mode/enable change, manual override/re-enable, clip envelope/mapping where offered.','Eligibility, precedence, smoothing, transaction grouping and pending Follow edit ownership U.'),
('TRANSPORT','transport','Stop, seek/restart, loop and tempo120/90/meter4/4-to3/4 changes while Follow/held input pending; repeat when global Follow disabled/re-enabled.','Counts, phase, clock origin, pending request restoration and no-grid behavior U.'),
('PERSISTENCE','persistence','Save/reopen owned Set and preset/Live Clip where supported; retain A/B/Linked/Time/Jump/enables, group identities and pending state; import into another Set.','Full saved fieldset, defaults, migration, copy/duplicate identity, pending RNG/position state U.'),
('UNDO','undo-redo','Change modes/chances/Time/targets and Create Follow Action Chain, move/remove group member, Undo/Redo each in owned copies.','Undo grouping, source/selection/enable/playing state restoration and playback effect U.'),
('MALFORMED','malformed','Enter abc/NaN/infinity in offered numeric fields, or open disposable state with duplicate/invalid/missing Follow fields while keeping originals unchanged.','Actual parser/load/edit acceptance, errors, normalization and old-load-law applicability beyond released scope U.'),
('CANCEL','cancellation','Begin chance/Jump/Time edit or target/mapping operation and Escape; cancel Set/file replacement or chain dialog if actually offered.','Cancel availability, rollback/atomicity, dirty state, partial chain and pending action state U.'),
('SOURCE-LOSS','source-loss','Remove/move selected or destination clip/scene, delete source track and make referenced media unavailable while action pending in separate trials.','Snapshot versus live target lookup, missing media/destination fallback, error/retry/cleanup U.'),
('TEARDOWN','teardown','During held Gate/Repeat or pending Follow/unreleased MIDI input, close Set, remove track, disconnect controller and suspend engine separately.','Release/note-off delivery, tails, queued actions, resources/restoration/error behavior U.'),
('RATE','sample-rate','Retain inputs then repeat at 44.1/48/96 kHz,64/256 frames and120/90 BPM; stopped/active rate changes andoffline recording where supported.','Frame/clock/rate rounding, latency and real-time versus offline behavior U.'),
('OUTPUT','signal-obligation','For each active mode/action, retain actual nonzero audio/MIDI source and output, launch velocity and mapped control paths; compare explicit zero amount or disabled enable only against positive baseline.','Audio amplitudes, velocities, Legato/dropout/RAM behavior, note lifecycle, tuning/MPE, interpolation/fade and quantitative tolerance U.')]
for group, contract, entries in unknowns:
 if group.endswith('LIFECYCLE'):
  scene=group.startswith('SCENE'); entries=[(group.split('-')[0]+'-'+suffix, kind,('SCENES setup:S1/S2 populated, multiple active tracks, scene local/global Follow enabled, valid time/targets and nonzero output. ' if scene else 'FOLLOW setup:A/B/C valid same-track group, clip local/global Follow enabled, Next positive transition and nonzero output. ')+action, missing) for suffix, kind, action, missing in life]
 rid='REQ-SESSION-LAUNCH-U-'+group
 refs=['LC-B021','LC-B047'] if group=='GLOBAL-FOLLOW' else ['LC-B033'] if group=='CHANCE-COUPLING' else []
 REQ.append({'id':rid,'provenance':'U','target_applicability':'U','title':group,'contract':contract,'source_id':'D12-LAUNCHING-CLIPS' if refs else None,'source_blocks':refs})
 for suffix, kind, action, missing in entries:
  CASES.append({'id':'SLC-U-'+suffix,'requirements':[rid],'kind':kind,'provenance':'U','fixture':'fixtures.json#SLC-F0','fixture_group':'SCENES' if suffix.startswith('SCENE') else 'FOLLOW','preconditions':['common','active-follow-guard'],'setup_and_action':action,'source_claim':None,'documentary_expected':None,'documentary_comparator':None,'expected':None,'comparison':None,'target_grade':'U','executed':False,'source_blocks':refs,'unknown':missing})
write('requirements.json', REQ); write('cases.json', CASES)
write('fixtures.json',{'id':'SLC-F0','status':'Finite future analyst setups; no media/MIDI/reference execution or supplied renders','common':['For launch-mode,Legato,velocity and nudge trials disable local/global Follow to isolate gestures; Follow and scene trials instead require both enables explicitly on.','Editable owned Set, copies reset between trials; declare original platform/focus, transport, tempo/meter, clipStart/End/Loop/warp, envelopes/groove/scale, global and clip quantization, Clip Update Rate, launch modes/Legato/VelocityAmount, controller mappings, playing/selected identities and current local/global Follow states.','Own independently validated audio/MIDI content with distinct audible markers/notes on active tracks. No input bytes supplied here; retain byte/rate/channel/note identity before evaluation.','Analyst baseline 4/4,120 BPM,48 kHz,256 frames; these are stimulus choices, not product limits. Candidate/source compatibility is not assumed.'],'active-signal-guard':'Correct valid clip/source, enabled clip/track/instrument, unmuted active output, nonzero gain/velocity and source content. Establish separately audible/observable positive baseline for each member and tested route before a no-effect/silence claim.','active-follow-guard':'Both local Follow Action enable for each tested clip/scene and Enable Follow Actions Globally on, valid explicitly retained occupied group/target slots, accepted nonzero Time/Multiplier and nonzero source/output gains; each destination independently active/audible. Record Chance fields and ensure exercised branch has actual nonzero chance. Pair disabled/zero/no-effect test with matched enabled/nonzero active positive baseline. Missing prerequisites remain U, never pass.','groups':{'CLIPS':'One track with A/B distinct4-bar looping clips, valid media/notes; additional Arrangement copies only for UI context.','FOLLOW':'Same track slots1=A,2=B,3=C,4 empty,5=D,6=E; clips distinct, audible and long enough for retained regions. GroupsA/B/C andD/E. Singleton trial uses separate D-only group. Global/local enable explicitly on for all evaluated paths.','SCENES':'S1/S2/S3 populated on two active tracks with independently audible valid clips; S4 empty, S5 populated only in U boundary trial. Scene grouping/empty semantics unproven. Scene Follow local/global enabled and its clips active; clip Follow only enabled when explicitly compared.','CHAIN':'One track selectedA, C, E across noncontiguous slots with gaps/otherclips retained; record actual selection/contextcommand/resultfields, then independently set enables for ungraded playback.'},'original_execution':False,'candidate_comparison':False})
counts={'requirements':len(REQ),'requirement_provenance':dict(Counter(r['provenance'] for r in REQ)),'cases':len(CASES),'case_provenance':dict(Counter(c['provenance'] for c in CASES)),'case_kinds':dict(Counter(c['kind'] for c in CASES)),'target_graded':0}
write('counts.json', counts)
assert len({r['id'] for r in REQ})==len(REQ) and len({c['id'] for c in CASES})==len(CASES)
assert {r['id'] for r in REQ}=={r for c in CASES for r in c['requirements']}
link='../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/'
spec='''---
id: SPEC-SESSION-LAUNCH-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Version 12 documentary parity unknown
---

# Session launch gestures and Follow Action workflows

## Scope and canonical boundaries

This partial F-04/F-08 draft owns broader documentary runtime roles for launch
modes, Legato, velocity, nudge/scrub and clip/scene Follow workflows. **D12** means
the retained official Version 12 chapter; **every exact 12.4.3 runtime outcome is
U**. It is not a release, compatibility result or complete Session specification.
[Coverage design](../research/full-live-specification-design.md) and
[research](../research/session-launch-workflows.md) govern evidence/limits.
No original application/function, host/emulator, controller or candidate ran.

[Clip launch](clip-launch.md) owns finite storage/enums/load-normalization/grid
clauses and its existing unknown runtime requirements. Specifically:

| Existing canonical requirement | New documentary context only | Exact-target disposition |
| --- | --- | --- |
| `REQ-CLIP-LAUNCH-020` Gate/Toggle/Repeat | Press/release/held input roles below | Remains U; no runtime timing or event matching result |
| `REQ-CLIP-LAUNCH-021` Legato | Same-track play-position takeover role | Remains U; no position/wrap/activation formula |
| `REQ-CLIP-LAUNCH-022` Velocity Amount | Documentary endpoints | Remains U; no launch-velocity gain law |
| `REQ-CLIP-LAUNCH-023` Follow execution | Group/action/enable/time/scene roles | Remains U; no scheduling, chance or jump codec |

[Playback core](playback-core.md) owns finite Trigger/engine dispatch, regions and
stop/fade/output computations, with its own assumptions; they are not transferred
to Follow, scene, Gate/Toggle/Repeat, nudge or scrub. No existing canonical/release is
changed. [Session view](session-view-workflows.md) owns grid/scenes/selection and
cross-view gestures; [Clip View](clip-view-workflows.md) owns region/panel/scrub UI.
[Mapping](midi-user-mapping.md) owns its bounded configuration/takeover; arbitrary
MIDI Learn/user-controller event pairing is not proved. [Arrangement](arrangement-editing.md),
[recording](recording-comping.md), [automation](automation-envelopes.md),
[media](media-file-workflows.md), [warp](warp-markers.md), [MPE](mpe-workflows.md)
and [transport](transport-state.md) retain their bounded scopes.

The ten action-role names use the
[released stored enum vocabulary](../../handoff/clip-launch-v2/spec.md#req-clip-launch-007--partial-follow-action-values)
only as vocabulary. That release specifies stored values, not the label set shown
in every UI or runtime action mapping. Several action labels in current source
are inline images. Figures were not inspected, and no label is recovered from
image filenames/alt text. Descriptive prose supports role contracts below;
exact image/label-to-source/runtime association remains U.

## State, preconditions and oracles

[Finite setups](REPLACE_LINKfixtures.json) require retained selected/playing clip
and scene identities, active valid source/output, region/loop/tempo/meter/mode,
quantization/Clip Update Rate, mapping/focus and local/global Follow state.
Every Follow probe requires both local and global enable, valid occupied clip
groups or populated scene targets, accepted timing values, nonzero source/gain and
an independently audible/observable paired positive baseline. A disabled source,
zero chance, empty target, muted output or missing mapping never establishes no
processing. No-action/Stop/disable tests change only their explicit tested state.

All cases have target `expected:null`, `comparison:null`, `target_grade:U` and
`executed:false`. Documentary visible-control/state proposals have separate
comparators; **signal, timing, RNG, launch/Follow event outcomes are ungraded/null**.
Their retained `source_claim` is source prose, not an output oracle. No launch
grid arithmetic, normalization equation, RNG distribution/seed/independence,
finite-success deadline, MIDI codec, velocity/gain formula, Legato wrap, frame
ordering, tolerance or candidate architecture is invented.

## Documentary requirements and cases

Bare first-column IDs are discoverable with the existing requirements browser.
Each D12 row has one same-number `SLC-NNN` case with concrete settings/actions.

| Requirement | Documentary role and limits | Source blocks |
| --- | --- | --- |
'''.replace('REPLACE_LINK', link)
for r in REQ:
 if r['provenance']=='D12':spec+=f'| {r["id"]} | {r["title"]}: {r["contract"]} | '+', '.join('`'+b+'`' for b in r['source_blocks'])+' |\n'
spec+='''
## Required unknowns and lifecycle

| Requirement | Required unresolved behavior | Finite case IDs |
| --- | --- | --- |
'''
for r in REQ:
 if r['provenance']=='U':
  spec+=f'| {r["id"]} | {r["contract"]} | '+', '.join('`'+c['id']+'`' for c in CASES if r['id'] in c['requirements'])+' |\n'
spec+='''
Clip and scene lifecycle groups have separate automation, transport, persistence,
undo, malformed, cancellation, source-loss, teardown, rate and output cases. Boundary
cases add group gaps/reorder/delete, Previous-at-top, singletons, self-target, Jump
empty/invalid indices, Time/Multiplier endpoints, held/released gesture races and
scene/clip/global simultaneity. No malformed/cancel/teardown kind is declared
inapplicable. Work uses disposable owned state; inputs, old Sets and runtime logs
are future prerequisites, not supplied fixtures. Common flags never substitute
for a per-case valid/active/nonzero positive path.

## Source-context questions

**SLC-U-GLOBAL-FOLLOW:** LC-B021 (§16.4) says any non-None clip setting quantizes
Follow launches, which includes Global. LC-B047 (§16.7) says Follow circumvents
Global while explicit non-None/non-Global quantization can apply. Matching runtime
mode/preconditions are unproven. Both statements remain retained; neither is
chosen. Trigger/grid arithmetic and stored enum values do not settle this path.
Root links the shared [Q-030](../questions.md) context; its unresolved target state
is unaffected by this documentary draft.

**SLC-U-CHANCE-COUPLING:** LC-B033 starts A 100/B 0, then says changing B 90 makes A
occur approximately one time in ten. It omits whether A changes through coupled
UI controls and which values are actually stored. No A=10, A=100,100/(100+90),
normalization equation or general probability law follows. Existing load-time
chance rescaling is a separate, unchanged contract. Finite traces establish no
uniformity, independence or guaranteed eventual branch. LC-B065 and LC-B073
examples do not guarantee termination or nonrepetition within bounded trials.

**SLC-U-ACTION-CONTEXT:** Exact label sets/image associations, assigned versus
enabled/default state, global graying criteria, Shift+Enter focus, scene grouping,
Jump UI indexing and created-chain fields remain required U. Next's documented
clip last-to-first wrap is not a Previous-wrap or scene-empty-group law.
Scene precedence after trigger does not settle same-sample tie/cancellation.

## Acceptance counts and evidence

[Requirements](REPLACE_LINKrequirements.json) and [case catalog](REPLACE_LINKcases.json)
contain REQCOUNT requirements (REQGRADES) and CASECOUNT unexecuted cases
(CASEGRADES). Zero target grades. Positive-control and compound case recipes
are finite investigation coverage, not complete mode/event-combination acceptance.

[Source metadata](REPLACE_LINKsource.json) retains official
[Launching Clips chapter](https://www.ableton.com/en/live-manual/12/launching-clips/),
captured 2026-10-19T21:43:52.559317+00:00,262,997 bytes, SHA-256
`dc9c4e21a480e1adeeb2daf548d34547ccb73153a2561fb93f56391f003a82af`.
[73 root-retained blocks](REPLACE_LINKsource-blocks.json) name exact HTML line and
heading anchor;[text](REPLACE_LINKsource-blocks.txt) is navigation only.
[HTML](REPLACE_LINKmanual-launching-clips-2026-10-19.html) is immutable source.
[Initial-input pins](REPLACE_LINKresumed-inputs.json) preserve all four pre-author
files byte-for-byte; there was no recapture or image inspection.
[Manifest](REPLACE_LINKmanifest-author-r1.json) freezes payloads/canonical snapshots;
[validation](REPLACE_LINKvalidation-author-r1.json) checks source/count/case/browser/
link/hash/whitespace scope only. All analysis links require sanitization/review
before handoff. No profile/family completion is claimed.

## Revision and handoff

Revision 1 is author-frozen for independent semantic review. Existing canonical
requirements/releases and shared catalogs, questions, plan/log are not edited.
'''.replace('REPLACE_LINK', link).replace('REQCOUNT', str(len(REQ))).replace('REQGRADES',', '.join(f'{v} {k}' for k, v in Counter(r['provenance'] for r in REQ).items())).replace('CASECOUNT', str(len(CASES))).replace('CASEGRADES',', '.join(f'{v} {k}' for k, v in Counter(c['provenance'] for c in CASES).items()))
(ROOT/'wiki/specs/session-launch-workflows.md').write_text(spec)
research='''---
id: RES-SESSION-LAUNCH-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Launch gestures and clip/scene Follow evidence

## Scope and retained inputs

The [canonical draft](../specs/session-launch-workflows.md) owns broader
Version 12 launch-mode/Legato/velocity/nudge/Follow documentary runtime roles.
[Coverage design](full-live-specification-design.md) governs closure; the existing
[clip-launch research](clip-launch.md) and its spec retain finite storage/enums/
load normalization/grid laws. Nothing here changes their runtime U requirements
020/021/022/023 or released Trigger/engine timing scope. Session/Clip View, mapping,
recording/Arrangement and audio/MIDI owners keep their existing boundaries.

Root supplied four retained files:HTML, source.json, source-blocks.json and text.
[Pre-author inventory](REPLACE_LINKresumed-inputs.json) pins all four unchanged.
[Metadata](REPLACE_LINKsource.json) records official Launching Clips Version 12,
2026-10-19T21:43:52.559317+00:00,262,997 bytes, HTML SHA-256
`dc9c4e21a480e1adeeb2daf548d34547ccb73153a2561fb93f56391f003a82af`.
[73 blocks](REPLACE_LINKsource-blocks.json) retain heading anchors/HTML lines.
No fetch, figure inspection, original function/application/controller/candidate,
installation, emulation or broad native analysis was performed.

## What this source can and cannot support

Source paragraphs support down/up/hold launch roles; Legato same-track position
takeover; velocity endpoint descriptions; nudge/scrub affordances; contiguous clip
groups separated by empty slots; local/global Follow enables; A/B choices; clip-only
Linked versus clip/scene Time; ten descriptive action roles; striped assigned-action
indicators; scene priority after trigger; Next cycles; noncontiguous chain creation;
and examples combining intro/loop, temporary repeats and Legato. Every exact 12.4.3
runtime outcome remains U; no documentary prose is execution evidence.

The ten action descriptions mostly have inline image labels omitted from text.
No image text is recovered from filenames or alt strings. Draft names are role
vocabulary consistent with the separately released stored enum clause, explicitly
not current label-set/source-image/runtime mapping proof. Previous top wrap and
scene grouping/empty targets are not inferred from clip Next wrap. Scene priority
after trigger is not same-time atomicity or a queue cancellation law.

## Source-context questions

**SLC-U-GLOBAL-FOLLOW:** LC-B021 at HTML 328 says non-None quantization applies to
Follow; LC-B047 at HTML 484 excludes Global and says global is circumvented. Clip/
scene, Linked/Unlinked, selected settings and actual dispatch are not matched across
these statements. Both locators remain evidence. Neither a chosen quantization
law nor an exact contradiction under identical preconditions is asserted. Old
Trigger/grid arithmetic and explicit-time fields do not resolve this engine path.

**SLC-U-CHANCE-COUPLING:** LC-B033 at HTML 374 gives A 100/B 0 then B 90/~one-in-ten A,
but does not retain A's post-edit displayed/stored value or central-slider
coupling. UI mutation, load-time normalization and runtime branch selection are
three distinct questions. No 100/(100+90), automatic A 10, general normalized chance,
RNG distribution/seed/independence, tolerance or finite-success guarantee is added.
The 80/20 eventual-language at LC-B065 and long-lived/nonrepeating example LC-B073
are not bounded-trial acceptance or guaranteed completion.

**SLC-U-ACTION-CONTEXT:** Image labels, actual source-role association, local enable
versus assigned/stored defaults, global gray criteria and Shift+Enter focus remain
U. Exact Jump displayed numbering/stored indices and generated-chain action/
chance/time/enables/order are not inferred. Root owns shared Q-030 registration
and canonical reconciliation; the draft preserves required unknowns locally.

## Cases and remaining obligations

[Requirements](REPLACE_LINKrequirements.json), [cases](REPLACE_LINKcases.json) and
[counts](REPLACE_LINKcounts.json) retain finite source-linked actions and all-null
target outcomes. Documentary visible-control/state fields are proposals; every
signal/timing/RNG/launch/Follow event field has no comparator. Separate clip and
scene groups retain automation, transport, persistence, undo, malformed, cancel, source
loss, teardown, rate and output U cases. Additional boundaries cover gaps/reorder/
remove, Jump invalid/empty/self, linked/time endpoints, gesture races and scene ties.
No failure/cancel/teardown kind is silently omitted as inapplicable.

[Future inputs](REPLACE_LINKfixtures.json) distinguish occupied clip groups from
populated scenes. Every Follow path requires both local/global enable, accepted
nonzero timing, chance and gain, valid active destination/source and independently
confirmed positive output; disable/no-effect probes explicitly change tested flag.
Missing controls, mapping, media or failed baseline remains inconclusive/U. No
source/controller/old Set/renderer fixture is supplied or executed here.

[Manifest](REPLACE_LINKmanifest-author-r1.json) freezes payloads/canonical snapshots
and pre-existing canonicals' read-only boundary pins. [Validation](REPLACE_LINKvalidation-author-r1.json)
checks four preserved inputs, source lines/anchors, cases, null outcomes, existing
spec_browser discoverability, links/metadata/hashes and untracked whitespace.
Run `python3 analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/validate.py`.
Separate semantic review remains required; no shared catalog/log/release is edited.
'''.replace('REPLACE_LINK', link)
research=research.replace("pre-existing canonicals' read-only boundary pins", "[retained existing-U boundary context]("+link+"boundary-context.json)")
(ROOT/'wiki/research/session-launch-workflows.md').write_text(research)
print(json.dumps(counts, indent=2))
