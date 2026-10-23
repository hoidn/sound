"""Bounded Video R2 analyst authoring. No capture/runtime; refuse after R2 seal."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert sys.argv[1:]==['--write'] and not (P/'manifest-author-r2.json').exists(),'Unsealed explicit authoring only'
def load(q):return json.loads(q.read_text())
def put(n,v):(P/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def pin(q):
 b=q.read_bytes();return dict(path=str(q.relative_to(ROOT)),bytes=len(b),sha256=sha256(b).hexdigest())
oldreq=load(P/'requirements.json');oldcases=load(P/'cases.json');reqs=deepcopy(oldreq);cases=deepcopy(oldcases);assert len(oldreq)==18 and len(oldcases)==28
blocks={b['id']:b for b in load(P/'source-blocks.json')}
def ev(n):
 b=blocks[f'VID-B{n:03}'];return dict(block=b['id'],anchor=b['anchor'],html_line=b['html_line'])
new=[dict(id='REQ-VIDEO-WORKFLOW-017',title='Video Window appearance after movie drop',contract='For an admitted QuickTime movie dragged from Browser into an Arrangement audio track, the chapter describes the Video Window appearing to display the movie video. This adds the source-specific import-to-window presentation role only. Actual decode/frame output, unsupported media, hidden-window history, window priority and opening latency remain unknown.',strength='D12',target_applicability='U',evidence=[ev(26)]),dict(id='REQ-VIDEO-WORKFLOW-018',title='Arrangement waveform feedback during video Warp edits',contract='In the documented scoring setup, adding and adjusting video Warp Markers is accompanied by updates to the video clip waveform in Arrangement to reflect those changes. This is distinct from Video Window corresponding-frame feedback. Exact waveform shape, marker/time/sample mapping, hit-point synchronization, pixels and update timing remain unknown; existing Warp and Arrangement owners retain their finite laws.',strength='D12',target_applicability='U',evidence=[ev(29)])]
reqs+=new;cm={c['id']:c for c in cases}
def refine(cid,action,contexts):
 c=cm[cid];c['setup_and_action']=action;c['finite_contexts']=contexts;c['refines_R1_case']=cid
refine('VID-001','After an independently successful accepted owned movie/decoder/video/audio baseline, explicitly drag the known nonempty QuickTime .mov from Browser onto an Arrangement audio track in a reset copy. Record source/codec/stream and import-route identities; no other-extension rejection or all-codec acceptance is inferred.',[dict(source='Browser admitted QuickTime movie',gesture='drag/drop',destination='Arrangement audio track')])
refine('VID-007','With an independently visible working movie, move the Video Window and resize it by its bottom-right corner. In separate histories close or hide it and open a video again without closing Live; separately open another owned Set/movie after retaining geometry. Inspect named size/location roles, not exact geometry/restart/display-fallback outcomes.',[dict(history=h) for h in ['bottom-right corner resize and move','close/reopen video, same session','hide/reopen video, same session','open another owned Set/movie, same session']])
refine('VID-008','From a known visible movie/window with independently identified source dimensions, explicitly double-click for full screen in separately admitted Windows and Mac contexts. Separately use Alt+double-click on Windows or Option+double-click on Mac for source-described original size. Where a real second monitor is independently available retain its optional full-screen placement context separately; missing hardware/platform remains U, and no exit gesture or pixel-scaling law is supplied.',[dict(platform=p,gesture=g,display=d) for p,k in [('Windows','Alt'),('Mac','Option')] for g,d in [('double-click','admitted primary display'),(k+'+double-click','admitted primary display'),('double-click full screen, placement observed','independently available second display')]])
refine('VID-009','Use only independently accepted complete owned QuickTime containers with separately indexed partial video-track or partial audio-track intervals. Retain leading, interior and trailing gaps separately for each stream, with actual productive decoded video/nonmuted nonzero audio controls wherever the stream is present; an interior gap additionally needs positive portions on both sides. Keep partial tracks distinct from missing streams and truncated/partial movie bytes. All black/silence/frame/sample/interval documentary and target outputs/comparators remain null.',[dict(partial_stream=s,gap_position=p,outcome='U') for s in ['video','audio'] for p in ['leading','interior','trailing']])
refine('VID-010','With an independently admitted movie in Arrangement, double-click its title bar to enter Clip View, inspect the Audio tab/panel and compare Leader availability with Warp off and on in reset histories. Then explicitly enable Warp and select video Leader with a separate eligible audio follower. Use existing Clip View/Warp entry laws; do not rely on defaults or infer all-clip tempo adaptation.',[dict(Warp=w,Leader_context=l) for w,l in [(False,'inspect offered eligibility'),(True,'positive offered eligibility and explicit Leader with eligible audio follower')]])
refine('VID-013','On an independently accepted owned movie with distinguishable indexed frames and visible working Video Window, use an independently supported Warp-owner route to add an interior marker, then drag that marker between two interior positions in reset copies. Retain source/marker/window identities and frame-feedback observations separately from Arrangement waveform observations; all frame/time/sample/latency documentary and target oracles remain null.',[dict(stage=s) for s in ['supported marker addition setup','drag between two admitted interior positions; window frame observation ungraded']])
refine('VID-015','Use an admitted owned movie with independently known pre-roll and distinct action onset. Place it at Arrangement1.1.1, double-click its title bar to open Clip View and explicitly drag Start Marker right to the action onset in a disposable copy. Two seconds is a possible retained fixture choice, never a universal source duration. Inspect working-region setup only; exact timecode/frame/sample relations remain U.',[dict(stage=s) for s in ['place movie at1.1.1','title-bar double-click to Clip View','drag Start right to independently known action onset']])
refine('VID-016','After the pre-roll working setup and adding owned music, invoke Edit/Select All and drag the entire composition later in a disposable copy. Click video title to select it alone and deselect other material, then extend its left edge to reveal the omitted pre-roll. Retain selected-movie range intent and use the existing export workflow for dialog/options. Actual restored boundaries, render values and original-movie duration equality remain separate null/U observations, never a universal export law.',[dict(stage=s) for s in ['Edit/Select All','drag entire composition later','video-title click selects it alone','extend left edge to reveal pre-roll','route selected-movie range intent to existing export owner']])
refine('VID-U-FORMAT','After independently admitted complete movie/decoder/stream positive baselines, retain separate owned malformed-extension, truncated/partial movie bytes, valid complete container with unsupported codec, audio-only, video-only and valid partial-track interval contexts. These identities are distinct; no alias, universal acceptance/refusal or repair result is inferred.',[dict(context=s) for s in ['invalid extension','truncated or partial movie bytes','complete container unsupported codec','audio-only stream','video-only stream','accepted complete container partial-track intervals']])
refine('VID-U-BOUNDARY','After known productive movie/region/marker baselines, separately retain source-start/end, admitted just-outside, zero/negative/extreme and partial-track-gap-adjacent region/marker observations. Accepted input, clip bounds, exact frame/sample/gap edges and clamp/reject behavior remain U.',[dict(context=s) for s in ['source start','source end','just outside independently known bounds','zero/negative/extreme admitted input','partial-track gap adjacent']])
refine('VID-U-AUDIO-VIDEO','Retain active nonmuted/nonzero audio and visible productive video baselines from independently indexed owned sources. Separately inspect accepted partial-track gaps, nonleader warp, frame/sample synchronization and processing-to-audio transitions. Hidden window, absent/failed decoder or stream and zero signal remain inconclusive; no color/floor, frame/sample or AV tolerance exists.',[dict(context=s) for s in ['accepted partial video gap','accepted partial audio gap','nonleader video warp','AV synchronization observation','video-to-audio processing transition']])
refine('VID-U-RATE','After independently accepted productive decoder/audio/display baselines, retain separately validated24/25/30fps and VFR sources only where accepted; independently admitted44.1/48kHz audio-rate requests and window-resize/monitor-scale changes are separate trials. All codec/rate/frame/timing/glitch/output comparisons remain null.',[dict(context=s) for s in ['independently accepted24fps','independently accepted25fps','independently accepted30fps','independently accepted VFR','offered44.1kHz','offered48kHz','window resize','accepted monitor-scale change']])
refine('VID-U-UNDO','After successful owned import/trim, each supported Consolidate/Reverse/Crop conversion and leader/marker edit in separate copies, invoke actually offered Undo/Redo. Retain clip media role, original hashes, generated references, leader/window state and pending prompts without assuming undoability or file rollback.',[dict(operation=o,history=h) for o in ['trim','Consolidate','Reverse','Crop','leader/marker edit'] for h in ['offered Undo','offered Redo']])
refine('VID-U-CANCEL','After independently successful corresponding positive baselines, retain actually offered Cancel/close before import or processing acceptance and during admitted pending import/processing/frame-feedback work. Window close is a separate presentation gesture. Record source/media/window/partial-output state without inventing cancellation, cleanup or rollback.',[dict(checkpoint=s,action=a) for s in ['before import accept','pending import, if offered','before processing accept','pending processing, if offered','pending marker feedback, if offered'] for a in ['offered Cancel','offered close']])
refine('VID-U-PERSISTENCE','Save/reopen owned Sets after successful loaded/trimmed movie, supported video-to-audio processing and leader/marker edits; retain original/generated references, media role and window state. Separately open another Set and restart in an independently admitted setup, distinguishing source-described same-session non-Set geometry from unproved restart retention.',[dict(context=s) for s in ['loaded movie','trimmed movie','processed audio-only replacement','leader/marker edit','different Set','independently admitted application restart']])
refine('VID-U-SOURCE-LOSS','After successful readable-source/decoder/video/audio baselines, define only owned source-unavailable and later restored/relinked histories at loaded-movie, pending marker-feedback and processing checkpoints where meaningful. Retain file identities, window/media state and prompts without original mutation, automatic repair, cleanup or failure-atomicity assumptions.',[dict(checkpoint=s) for s in ['loaded movie','pending marker feedback, if applicable','pending supported processing, if applicable','completed audio-only replacement']])
refine('VID-U-TRANSPORT','After independently productive video/audio and eligible leader/playback baselines, separately stop/seek/restart across admitted clip/gap/active-leader boundaries; retain actually offered recording, tempo and automation changes at loaded/pending-marker/processing checkpoints. Record actual acceptance/order only, without default arbitration, dispatch or deadline law.',[dict(context=s) for s in ['stop/seek/restart','partial-track gap boundary','active-leader boundary','recording, if eligible','tempo change','automation change']])
refine('VID-U-DISPLAY','After a productive primary-display/movie baseline, use an independently available real second monitor for supported window placement; separately retain actually supported disconnect/scale/reopen histories. Record fallback, focus and accessibility without inferred geometry recovery, OS-wide topmost or exclusive full-screen behavior.',[dict(context=s) for s in ['second-monitor placement, if available','supported display disconnect','accepted scale change','video reopen after supported display change']])
refine('VID-U-TEARDOWN','From successful owned movie and corresponding positive operation baselines, separately close/remove offered Video Window, clip, track, Set and application at loaded, pending import, pending Warp feedback and processing checkpoints where meaningful. Record prompts/media/source/generated references and resources; no cleanup, persistence, cancel or leak guarantee.',[dict(object=o,checkpoint=s) for o in ['Video Window','clip','track','Set','application'] for s in ['loaded and productive','pending import, if applicable','pending marker feedback, if applicable','pending processing, if applicable']])
cm['VID-005']['kind']='file'
for c in cases:
 c['fixture']='fixtures-r2.json#VID-OWNED';c['source_claim']=None if c['id'].startswith('VID-U-') else next(r['contract'] for r in reqs if r['id']==c['requirements'][0])
 if c['kind'] in {'signal','file','timing'}:c['documentary_expected']=None;c['documentary_comparator']=None
cases.append(dict(id='VID-017',requirements=[new[0]['id']],kind='control',fixture='fixtures-r2.json#VID-OWNED',setup_and_action='After independently productive accepted movie/decoder/audio/video baseline, explicitly drag the same owned Browser movie into an Arrangement audio track in reset copies and inspect Video Window appearance. Retain prior hidden/visible window histories separately; actual decoding, pixels and opening latency remain U.',source_claim=new[0]['contract'],documentary_expected='Named Video Window appearance after the admitted Arrangement movie-drop entry only.',documentary_comparator='Visible named window role only; no decoded frame, pixel, geometry, priority or timing comparator.',expected=None,comparison=None,target_grade='U',executed=False,evidence=new[0]['evidence'],finite_contexts=[dict(prior_window=s) for s in ['independently known hidden','independently known visible']]))
cases.append(dict(id='VID-018',requirements=[new[1]['id']],kind='timing',fixture='fixtures-r2.json#VID-OWNED',setup_and_action='Establish an independently accepted movie and eligible explicit video-Leader/audio-follower scoring setup with productive visible video/nonzero audio. Use existing Warp-owner marker-add/edit entry on an interior region and retain Arrangement waveform presentation as markers are added/adjusted, separately from corresponding-frame Video Window feedback. All waveform shape, numeric/frame/audio/time documentary and target oracles remain null.',source_claim=new[1]['contract'],documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,evidence=new[1]['evidence'],finite_contexts=[dict(observation=s) for s in ['Arrangement waveform after supported marker addition','Arrangement waveform during supported marker adjustment','Video Window frame context retained separately, ungraded']]))
def unknown(cid,kind,action,contexts):cases.append(dict(id=cid,requirements=['REQ-VIDEO-WORKFLOW-U-LIFECYCLE'],kind=kind,fixture='fixtures-r2.json#VID-OWNED',setup_and_action=action,source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,evidence=[],finite_contexts=contexts))
unknown('VID-U-DEFAULT-HISTORY','default-history','After independently admitted exact build/platform and accepted fresh movie/audio imports, retain initial Warp/Leader/Follower states before manual edits in separate new/known-history Set copies. Publisher default language is research context only; templates/preferences/history precedence and target constructor defaults remain unknown.',[dict(history=s) for s in ['new independently known Set context','known existing Set context','known template/preferences context, if admitted']])
unknown('VID-U-LEADER-COUNTS','leader-counts','After a separately established two-flagged positive setup, retain zero, one and three explicitly named warped Arrangement clips in independently active/inactive histories. These are finite unknown flag/eligibility observations, not adoption of any-number flag support by old011, an infinite-resource law or an active-leader timing comparator.',[dict(flagged_count=n,play_context=s) for n in [0,1,3] for s in ['independently active eligible clips where nonempty','known nonplaying context']])
unknown('VID-U-EXPORT-RANGE','timing','After independently admitted restored-pre-roll composition, select movie alone, open Export Audio/Video through the existing owner and retain offered range/options plus original movie metadata. Separately retain only independently admitted rendered-file observations if available. B039 selected-duration prose remains research/U, not exact duration, codec-padding, default-precedence or endpoint equality.',[dict(stage=s) for s in ['video-alone selected before export dialog','offered render start/length/options','independently admitted future rendered-file metadata, if available']])
unknown('VID-U-AVAILABILITY','availability','Record independently established exact build/edition/platform and actually offered movie/decoder/video/window/display features before every input or absence trial. Current Version12 source does not prove exact12.4.3 presence, codec entitlement or installed resources. No original, account, install or download operation is performed or authorized; unavailable capability remains U.',[dict(context=s) for s in ['exact build/edition/platform identity','independently accepted movie/decoder capability','actual video/window availability','real display capability, if available']])
put('requirements-r2.json',reqs);put('cases-r2.json',cases)
f=load(P/'fixtures.json');f['status']='R2 future owned setup only; no movie/frame/audio/marker/reference results supplied';f['media']='Independently validate/hash accepted complete owned QuickTime containers with distinct frame landmarks, nonzero audio and known source pre-roll/embedded marker identities. Retain separate independently indexed leading/interior/trailing partial audio-track and video-track intervals and actual productive stream portions wherever present. Only interior gaps require positive material on both sides; leading/trailing gaps are not missing streams or truncated movie bytes.';f['positive_guard']='First independently verify available exact-build movie/decoder/display capability, accepted owned nonempty streams, working visible video and nonmuted/nonzero productive audio/output. For gap/absence observations retain actual decoded/productive stream portions wherever present; interior gaps need positives on both sides. Hidden window, missing/failed decoder/source/stream and zero signal are U, never a successful absence test.';f['partial_track_identity']='Accepted complete-container partial audio/video intervals are not aliases for truncated/partial movie bytes or entirely missing streams. Leading/interior/trailing intervals require independently retained identities.';f['history']='Record focus/platform/transport/Warp/Leader, source/codec/frame/marker metadata, window/displays, explicit initial histories and successful paired operation baselines before negative/failure/loss probes. Actually offered cancel/undo/recovery only; use disposable owned copies.';put('fixtures-r2.json',f)
redirects=[]
for rel in ['inventory-revisions/r4-citation-crosswalk/inputs.json','video-source-audit/input-pins.json']:
 data=load(B/rel);prefix='/pins/' if isinstance(data,dict) else '/';rows=data['pins'] if isinstance(data,dict) else data
 for i,r in enumerate(rows):
  if r['path'] in ['wiki/specs/video-workflows.md','wiki/research/video-workflows.md']:
   q=P/'archive-r1'/('spec-r1.md' if '/specs/' in r['path'] else 'research-r1.md');p=pin(q);assert all(p[k]==r[k] for k in ['bytes','sha256']);redirects.append(dict(consumer=str((B/rel).relative_to(ROOT)),record_pointer=prefix+str(i),original_path=r['path'],original_bytes=r['bytes'],original_sha256=r['sha256'],historical_snapshot=p,reason='Exact historical R1 canonical bytes only; no rewritten consumer or current R2 bytes substituted. Source/citation meaning unchanged.'))
assert len(redirects)==4;put('historical-pin-redirects-r2.json',redirects)
review=B/'reviews/video-source-audit-review.json';assert pin(review)['sha256']=='e0fd362930fe0514e164cfd4aaecdde9139851d64e2b75e57ffe7b1ae9da8524'
inputs=[ROOT/'tools/spec_browser.py',ROOT/'tools/build_artifact_browser.py',review,B/'reviews/video-workflows-review.json',P/'manifest-author-r1.json']+[P/n for n in load(P/'manifest-author-r1.json')['files']]
for rel in ['video-source-audit','inventory-revisions/r4-citation-crosswalk']:
 folder=B/rel;inputs+=[folder/'manifest.json']+[folder/n for n in load(folder/'manifest.json')['files']]
inputs +=[ROOT/r['path'] for r in load(B/'video-source-audit/input-pins.json') if r['path'] not in ['wiki/specs/video-workflows.md','wiki/research/video-workflows.md']]
put('inputs-r2.json',[pin(q) for q in sorted(set(inputs))]);put('archive-r1-pins.json',[pin(q) for q in sorted((P/'archive-r1').iterdir())])
counts=dict(requirements=len(reqs),strengths=dict(Counter(r['strength'] for r in reqs)),cases=len(cases),documentary_visible_cases=sum(c['documentary_expected'] is not None for c in cases),all_target_null_U_unexecuted=True,old_requirements_retained=18,old_case_IDs_retained=28,new_requirement_IDs=2,new_case_IDs=len(cases)-28,adopted_audit_groups=9,historical_Video_pin_redirects=4,source_blocks_unchanged=39,completed_topics=0);put('counts-r2.json',counts)
put('audit-adoption-r2.json',dict(review=pin(review),audit_manifest=pin(B/'video-source-audit/manifest.json'),status='partial-successor-author-adoption-awaiting-independent-review',groups=[dict(id=f'G{i:02}',adopted=True,route=r) for i,r in enumerate(['new017 drop-to-window role/case and explicit001 drag','new018 Arrangement waveform role/case,010/013 setup','007/008 resize/platform/second-display contexts','009 partial-track positions and U-format identity','research default context + U-DEFAULT-HISTORY','U-LEADER-COUNTS only; old011 unchanged active-role law','015/016 title/Start/EditSelectAll/selection gestures','research selected-duration context + U-EXPORT-RANGE','U checkpoint refinements and U-AVAILABILITY'],1)],review_note_001='Old011 remains verbatim active leader relation; arbitrary any-number flag support is not adopted. Finite zero/one/three observations remain U.',original_unsuffixed_catalogs_unchanged=True,new_timing_frame_DSP_codec_constructor_laws=False,counts=counts))
# Exact field-level successor delta, including old literal values; no hidden catalog changes.
changes=[]
for i,(a,b) in enumerate(zip(oldcases,cases)):
 for field in sorted(set(a)|set(b)):
  if a.get(field)!=b.get(field) or (field in a)!=(field in b):changes.append(dict(id=a['id'],old_pointer='/'+str(i)+'/'+field,new_pointer='/'+str(i)+'/'+field,field=field,old_present=field in a,new_present=field in b,old=a.get(field),new=b.get(field)))
put('delta-r2.json',dict(old_manifest=pin(P/'manifest-author-r1.json'),old_requirement_catalog=pin(P/'requirements.json'),old_case_catalog=pin(P/'cases.json'),old_requirement_records_verbatim=18,old_case_IDs_preserved=28,new_requirement_ids=[r['id'] for r in new],new_case_ids=[c['id'] for c in cases[28:]],existing_case_field_changes=changes,changed_existing_action_IDs=[a['id'] for a,b in zip(oldcases,cases) if a['setup_and_action']!=b['setup_and_action']],cleared_signal_file_timing_documentary_expectation_IDs=[a['id'] for a,b in zip(oldcases,cases) if a['documentary_expected'] is not None and b['documentary_expected'] is None],historical_redirects='historical-pin-redirects-r2.json'))
oldspec=(P/'spec-r1.md').read_text();intro=oldspec[:oldspec.index('## Requirements')].replace('revision: 1','revision: 2',1)
intro+='''R2 minimally adopts the [independently reviewed source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/video-source-audit-review.json).
All eighteen R1 clauses remain verbatim. Two bounded roles add movie-drop window
appearance and Arrangement waveform feedback, distinct from Video Window frame
feedback. [Audit adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/audit-adoption-r2.json)
records nine groups; no default, frame, tempo, codec or numerical law is added.

## Requirements

Use [R2 future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/fixtures-r2.json).
First establish actual accepted movie/decoder/display capability, visible productive
video and nonmuted/nonzero audio/output. Absent source/stream, hidden window,
failed decoder or zero signal is U, never a passing gap/absence case. Complete
partial-track intervals and truncated/partial movies remain distinct contexts.

'''
spec=intro
for r in reqs[:16]+new+reqs[16:18]:
 spec+=f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}\n\n"
 if r['evidence']:spec+='Evidence: '+', '.join('`'+e['block']+'`' for e in r['evidence'])+'; [exact source routes](#analysis-only-evidence).\n\n'
spec+='''## Finite acceptance proposals

[Current R2 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/cases-r2.json)
retain all28 old IDs and add six cases: two source roles and four explicit U
observations. Twenty requirements (18D12/2U) map to34 cases. Twelve named visible
control/state proposals retain qualified documentary expectations; every actual
outcome/comparator and every signal/file/timing/U documentary outcome/comparator
is null/U/unexecuted. Finite contexts refine drag, resize, platform/display,
partial-track positions, scoring, pre-roll, exact selection and lifecycle actions.
They do not supply fixtures or full branch coverage. Default histories, finite
Leader counts and selected-movie export-duration observations remain U; old011
does not adopt arbitrary-count support from the source's any-number wording.

'''+oldspec[oldspec.index('## Analysis-only evidence'):]
spec=spec.replace('[Requirement catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/requirements.json)','[Current R2 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/requirements-r2.json)').replace('[author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manifest-author-r1.json)','[R2 author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manifest-author-r2.json)')
spec+='''
## Preserved history and checks

[R1 archive](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/archive-r1/manifest-author-r1.json)
retains all fourteen original files. Unsuffixed catalogs, snapshots, validation
and checker are historical R1. The [R2 read-only checker](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/validate-r2.py)
checks this successor and exactly four disclosed historical Video canonical pin
reads against immutable R1 snapshots. R4 and Video audit files/pins are unchanged;
their old direct-current-canonical tools are not current R2 replay entrypoints.
Root owns combined crosspacket replay. Focused independent R2 review is pending;
no release, complete topic or compatibility result follows.
'''
research=(P/'research-r1.md').read_text().replace('revision: 1','revision: 2',1);research=research[:research.index('## Review and next evidence')]+'''## Reviewed source-audit adoption

[The independently approved retained-text audit](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/video-source-audit-review.json)
assesses all39 blocks and97 claim/context facets. R2 adopts its nine groups in
[audit-adoption-r2.json](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/audit-adoption-r2.json).
The only new documentary clauses are accepted Arrangement movie-drop Video Window
appearance (B026) and Arrangement waveform updates during video Warp edits (B029).
The latter is distinct from corresponding-frame feedback in Video Window (B021);
citing B029 under the original013 clause did not specify the waveform observation.
Existing audio/Clip View/Warp/Arrangement/export laws remain canonical.

B017 describes video-Leader/audio-follower default warp roles. Actual imported,
new-Set, template/preferences and constructor histories remain U, separate from
explicit Leader setup. B018's any-number flag wording is not adopted by old011,
which remains the active bottom-most currently playing leader relation. Finite
zero/one/three flagged contexts are source-silent U observations, never unlimited
resource support, a flag-count law or a numerical leader/scheduling oracle.

B039 describes default Arrangement-selection export range and, in its restored
selected-movie example, original movie duration including pre-roll. This exact
qualified source context remains research/U, not a new duration equality, default
precedence, render-endpoint or codec-padding law. The export owner retains its
selection/options rules. B028's rest-of-clips adaptation is a scoring setup,
not universal adaptation of unwarped or otherwise ineligible clips. B033 colon
SMPTE and B036 dotted notation remain raw source strings without codec/conversion.
Two seconds in an existing future fixture is not a universal pre-roll duration.

The actual h4 headings Movies with Partial Tracks / movies-with-partial-tracks and
this chapter's Warp Markers / warp-markers remain absent from literal original
TOC joins. Partial Movies, Partial Tracks and Movies with Partial Tracks are not
aliases. Accepted complete-container partial-track intervals differ from absent
streams and truncated/partial movie bytes. All three original R4 unmatched rows
are unchanged; no parent, other chapter's Warp anchor or semantic alias repairs
a literal join. Current Version12 source still does not prove exact12.4.3 presence.

## Future evidence and preserved history

[Current cases](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/cases-r2.json)
and [future setups](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/fixtures-r2.json)
retain owned source/codec/frame/marker identities and productive visible-video /
nonmuted nonzero audio baselines. Leading/interior/trailing partial-track contexts
need independently known productive stream portions; interior gaps also need
positive material on both sides. Missing feature/display/stream/decoder is U,
never successful absence. No stimulus, original/candidate/video/audio/hardware,
account/network/install or source capture operation was performed.

[Exact field delta](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/delta-r2.json)
retains old18 requirement records verbatim, old28 case IDs and all14 original
files at their paths plus exact archive copies. Only versioned R2 catalogs and
snapshots are current. Signal/file/timing documentary expectations/comparators
are null, as are all actual outcomes; source_claim is distinct prose provenance.

[Historical pin disclosures](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/historical-pin-redirects-r2.json)
resolve exactly the two R4 and two Video-audit old canonical records to identical
R1 snapshots, without changing consumers or borrowing current R2 bytes. Other
Stem/Synchronization or cross-owner pin changes are outside that local resolver;
root owns combined replay and shared navigation updates. Old source-audit and
R4 direct-current-canonical checks are historical, not current successor checks.
[R2 validation](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/validate-r2.py)
is read-only; [R2 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manifest-author-r2.json)
freezes partial author material for independent review. No whole family is complete.
'''
for name,text,path in [('spec-r2.md',spec,'wiki/specs/video-workflows.md'),('research-r2.md',research,'wiki/research/video-workflows.md')]:
 (P/name).write_text(text);(ROOT/path).write_text(text)
