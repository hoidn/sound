"""Initial documentary Warp audit adoption only. No original/runtime calls."""
from pathlib import Path
from copy import deepcopy
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent;A=B/'warping-source-audit'
load=lambda q:json.loads(q.read_text())
def identity(q):
 x=q.read_bytes();return dict(bytes=len(x),sha256=sha256(x).hexdigest())
def write():
 assert sys.argv[1:]==['--write'] and not (P/'manifest-author-r2.json').exists(),'Initial unsealed authoring only'
 prior=load(P/'manifest-author-r1.json');assert identity(P/'manifest-author-r1.json')['sha256']=='b17efb2eb29b165239bab421e53e49f69117e69fa80f97927ad0e54dac76ba68'
 assert len(prior['files'])==14
 oldnames=set(prior['files'])|{'manifest-author-r1.json'};old={n:identity(P/n) for n in sorted(oldnames)}
 for n,r in prior['files'].items():assert old[n]==r
 for n,path in prior['canonical_snapshots'].items():assert (P/n).read_bytes()==(ROOT/path).read_bytes()
 review=B/'reviews/warping-source-audit-review.json';assert identity(A/'manifest.json')['sha256']=='b225aed9cdd516e68e98aee32c2cd06a814667a97ba20701a2ea85abb45f9700';assert identity(review)['sha256']=='b2ff0863665df4bc4d3e3e463be1238aaeb50040955ba2d81819dc5cbbab19d6' and load(review)['required_findings']==[]
 oldreq=load(P/'requirements.json');oldcases=load(P/'cases.json');reqs=deepcopy(oldreq);cases=deepcopy(oldcases);rm={r['id']:r for r in reqs};cm={c['id']:c for c in cases}
 contracts={
 1:'The Control Bar tempo field adjusts Set playback tempo through coarse BPM and fine hundredths-of-BPM controls, which can be key/MIDI mapped separately. This supplies named direct edit/control roles only; numeric storage, ranges, interpolation and mapping protocol retain existing owners.',
 3:'Start Playback with Tap Tempo in Record, Warp & Launch Settings enables tap-triggered playback; the source describes four taps in 4/4. It also describes tap-start automatically synchronizing connected Link-app playback positions within the current phrase. This is a qualitative source role, with no estimator, interval tolerance, other-meter count, phase/phrase arithmetic, Link alignment or scheduling oracle.',
 21:'Hovering a transient shows a gray pseudo-Warp Marker; the source contrasts this with a yellow real Warp Marker. Double-click or drag converts the pseudo-marker to a real Warp Marker. Literal color names supply no palette/RGB/image oracle. The source says clip tempo changes if no Warp Markers follow the new one, without a numerical tempo oracle.',
 29:'For a seamlessly edited loop, Warp Sample as in the Sample Editor context menu can be invoked to adjust Auto-Warp results and displays a suggested loop length fitting Set tempo. This is a public command/suggestion role only; the suggested value, algorithm, accepted bounds, generated markers and audio results remain ungraded.'}
 for n,text in contracts.items():rm[f'REQ-WFW-{n:03}']['contract']=text
 # Keep source_claim synchronized without changing unsupported actual oracles.
 for c in cases:
  if c['requirements'][0] in {f'REQ-WFW-{n:03}' for n in contracts}:
   c['source_claim']=rm[c['requirements'][0]]['contract']
   if c['documentary_expected'] is not None:c['documentary_expected']=c['source_claim']
 cm['WFW-001']['documentary_expected']='Named offered coarse/fine controls, accepted visible edit and mapping states only; no numeric tempo response, storage, interpolation or dispatch result.'
 cm['WFW-021']['documentary_expected']='Literal gray-pseudo/yellow-real, hover and named conversion roles only; no pixel/palette, generated list, clip-tempo or delivered audio result.'
 cm['WFW-003']['documentary_expected']='Named Start Playback with Tap Tempo setting and explicit selected state only; four-tap/Link position and timing outcomes remain null.'
 cm['WFW-029']['documentary_expected']='Named offered Warp Sample as command, suggestion presentation and accepted invocation role only; no suggested numeric value or generated map/audio result.'
 actions={
 1:'F-TEMPO: after independently productive nonzero playback, separately edit accepted coarse BPM and fine hundredths controls on reset copies, retaining offered fields and selected values without inferring step/range or audible tempo arithmetic. Separately map each control through actually accepted key/MIDI mapping as in R1, with mapping/focus declared. Actual tempo/audio/dispatch observations remain U.',
 7:'F-LEAD: independently establish an actually active playing audio leader with admitted nonidentity map and genuine nonempty generated Main tempo automation; retain the genuine generated/uneditable before-state separately from unrelated editable automation. Flags, audio activity or an empty lane are insufficient. With valid distinguishable source/Set tempo histories, inspect editability then move only the admitted leader on reset copies and retain corresponding automation observations. Numeric points, scheduling, file identity and Undo remain U.',
 10:'F-LEAD: show and explicitly activate Tempo Follower on independently admitted nonzero input, with no active leader, and independently establish genuine interpretation/tempo following first; active input, a lit Follow or flags alone are insufficient. Separately establish an actually active playing audio leader with a distinct admitted nonidentity map and productive output, then enter the source-described leader-automation override context. Record source states/observations without complete precedence, acquisition/cessation deadlines, fallback or restoration/re-enable outcomes.',
 24:'F-AUTO: independently establish saved markers for an owned non-library sample through the existing media owner. In separately admitted histories inspect availability of each actually offered basic Warp From Here, Start At, Straight and BPM From Here variant, with exact selected-marker/grid/source and saved-marker context retained. This control proposal records availability only; actual invocation/generation is separately null in054. No all-variant presence, source acceptance, ASD identity or save-control equivalence is assumed.',
 27:'F-LOOP: with independently known downbeat in an eligible uneven short source, move insert marker there and invoke Set 1.1.1 Here; retain the short-example Warp Marker role. Separately establish an admitted long Auto-Warp result with appropriate tempo but wrong downbeat, move insert marker to its independently known downbeat and explicitly invoke Set 1.1.1 Here, retaining the long-example start-marker role. Keep the short/long histories distinct; no full coordinate, source/region transform, detector correctness or numerical sync oracle.',
 29:'F-LOOP: independently admit a seamlessly edited nonempty loop and productive nonzero source/output, explicit Set tempo and actually offered Warp Sample as suggestion. Retain that genuine eligible before-state, explicitly invoke the admitted offered entry and retain selected command/control state plus map/source/tempo observations separately as U. Suggested numeric length, generated markers, bar-selection algorithm and delivered audio have null oracles; inspection alone is not this invocation history.',
 32:'F-MARKER: independently retained left/right marker inventories and eligible source before basic Warp From Here; separately admit an interior selected real marker and the start marker as context. Invoke the actually offered basic command and retain left/right observations with no exact generated-list/selected-point/boundary oracle. Do not equate this selected-marker branch with057 no-selection grid insertion or extend that branch to every variant.',
 33:'F-AUTO: in separate interior versus start-marker histories retain known left/right inventories, valid long source and explicitly admitted Set tempo before actually offered Start At. Separately preserve the source preparation: Warp off, genuinely productive original-speed playback, accepted Tap input with independently known source tempo context, Warp on, then invoke Start At. Retain selected controls/maps as available, no estimator, audio alignment, original-speed waveform or generated-map oracle.',
 34:'F-LOOP: independently admit a constant-tempo source with productive output and retained left/right marker inventory; in separate interior and start-marker histories inspect actual Straight availability. Source suitability is guidance, not rejection of other material. Actual invocation/maps are separately null in059; no estimated-BPM, one-marker or boundary oracle.',
 35:'F-LOOP: independently known source BPM and eligible positive source; enter that admitted value in the Set tempo field before inspecting the actually offered BPM From Here command in separate interior and start-marker contexts. Retain known left/right inventory and actual selections; invocation/maps separately null in060. No numeric conversion, source/Set equality proof from a label, marker count or boundary law.',
 45:'F-TEMPO: after a genuine working assignment/accepted-input baseline for each route, separately retain mouse, mapped-key, accepted MIDI-note and MIDI-controller Tap histories. Eight nominal half-second intervals remain analyst choices, never estimator bounds. With independently known timestamps, retain shorter and longer histories separately, including more-than-one accepted history length. Record actual tempo/dispatch observations as U; no guaranteed accuracy improvement, immediate deadline or footswitch/profile protocol follows.',
 46:'F-TEMPO: stopped4/4 with tap-start explicitly on and independently productive local clip/output, after genuine usable connected Link-peer tempo/transport and independently nonzero peer output baselines. Deliver four accepted timestamped taps and retain local/peer positions and phrase/tempo histories; separately compare tap-start off on a reset owned copy. Missing peer/input or failed baseline is U, not alignment/exclusion evidence. No phase, phrase arithmetic, sample/tolerance, schedule or other-meter oracle.',
 47:'F-TEMPO: independently productive local Set source and a separately admitted productive external reference with separately known roughly matched tempo context before Nudge; no numerical rough-match bound is invented. On reset histories hold/release each actually offered Up/Down direction and separately accepted mapped entry routes, retaining local/reference before/during/after observations. No speed, duration, phase alignment, recovery curve or return deadline.',
 48:'F-LEAD: independently establish actually active playing audio leader status using admitted track order/playing context and separately known nonidentity map before observing Set tempo. A flag, merely active clip audio, generic peer tempo or positive follower output alone is not active-leader proof. Retain genuinely productive leader/follower outputs and actual source states while switching the admitted history to follower on reset copies. No unwarped waveform equality, numerical tempo map or arbitrary handoff arithmetic.',
 54:'F-AUTO: independently establish genuinely saved-marker and readable/writable owned non-library sample baseline through the media owner, then reimport with Auto on separately from manual operations. For saved-marker and independently known no-saved-marker histories explicitly invoke each actually offered basic, Start At, Straight and BPM From Here variant on reset copies, declaring class/preferences/selection and known left/right inventories with interior/start-marker contexts. Absence of saved data cannot prove suppression; no exact ASD/source identity, reanalysis, precedence or generated-map oracle.',
 57:'F-MARKER: retain known left/right map and admitted grid point with no selected real marker, separately at eligible interior versus start-marker context. Invoke only the actually offered basic Warp From Here; do not borrow its no-selection insertion branch for other variants. Actual new marker/list/selected-point/boundary/rounding outcomes remain U.',
 58:'F-AUTO: independently positive source, known left/right inventories and chosen point; explicitly set two distinct admitted Set tempi in separate reset copies before invoking offered Start At. Keep interior versus start-marker contexts and the separate off/tap/on preparation in033. No estimator, equal-map, phrase/phase, left-boundary or generated-marker oracle.',
 59:'F-LOOP: independently constant-tempo positive source, chosen point and known left/right inventory; separately at interior and start marker invoke actually offered Straight and retain controls/maps/BPM as U. Source suitability is not an exclusion gate; no single-marker count, estimated original BPM or exact preservation/boundary oracle.',
 60:'F-LOOP: independently known source BPM and productive eligible source; explicitly enter that independently accepted source BPM as Set tempo before invoking actually offered BPM From Here. Retain known left/right inventories in separate interior/start-marker histories and actual source/control states; no numerical equality/conversion, single-marker, generated map or boundary oracle.',
 80:'F-MARKER/F-AUTO: retain original save/reopen interactive/mode/leader and owned-default/reimport/migration histories. Separately record the actually offered clip-title Save source entry and existing ClipView046/Media010 Save Default Clip controls as distinct named contexts until identity is independently established. After genuinely successful readable/writable owned-sample save/reimport baseline, inspect offered own-sample versus already available independently identified Core Library/Pack eligibility without modifying original Library/Pack content, download, installation or account action. Set-save versus sample-default reuse, exact persisted fields, eligibility refusal, ASD/source identity, marker/automation persistence and recovery outputs remain U.',
 87:'Future independently valid readable accepted sources only: separately record exact MP3, AAC, Ogg Vorbis, Ogg FLAC or FLAC histories from the source list, and any independently accepted uncompressed alternative as a separate ungraded context, not a new codec guarantee. With exact platform/codec, admitted short/long class, first versus previously analyzed/default history and explicit Auto-Warp state, compare selected-audio-track Create Import Audio File against folder drag. Retain Arrangement insert marker versus selected Session slot explicitly, and both playback and editor eligibility before/during/after actual analysis. Keep Q032 all-first-import versus media long-analysis and most-cases tempo-sync qualification open; no format rejection, threshold, completion or readiness oracle.'}
 contexts={1:['direct coarse edit','direct fine edit','separate accepted key/MIDI field mappings'],7:['genuine active leader','nonempty generated uneditable Main automation','move only admitted leader'],10:['genuine interpreted Tempo Follower without leader','separately admitted active audio leader','override observations U'],24:['basic','Start At','Straight','BPM From Here','saved-marker availability only'],27:['uneven-short insert-marker→Warp Marker','long correct-tempo/wrong-downbeat→start marker'],29:['eligible seamless loop/suggestion before-state','explicit command invocation','generated output U'],45:['mouse','mapped key','MIDI note','MIDI controller','shorter/longer accepted histories'],46:['genuine working peer/local output before-state','explicit stopped4/4/on/four taps','separate off history'],47:['independently productive local and external reference','independently roughly matched context','Up/Down and admitted input routes'],48:['independently actual active leader, not flags/audio alone','separate follower history'],54:['saved and no-saved histories','basic','Start At','Straight','BPM From Here','interior/start marker'],80:['Set save/reopen','owned sample-default save/reimport','clip-title Save versus default-save identity U','owned versus available Core Library/Pack eligibility'],87:['exact source formats/platform','selected audio track command versus drag','Arrangement insert marker versus Session selected slot','first/prior analysis and short/long','playback AND editor before/during/after analysis']}
 for n,action in actions.items():
  c=cm[f'WFW-{n:03}'];c['setup_and_action']=action
  c['finite_contexts']=contexts.get(n,['known left/right inventory','interior point','start-marker context','only actually offered source-specific command branch'])
 cm['WFW-021']['setup_and_action'] += ' Additionally compare the literal source gray-pseudo versus yellow-real presentation with independently known real/pseudo identities; no RGB, palette, geometry or image-derived claim.'
 cm['WFW-021']['finite_contexts']=['known transient hover/gray pseudo','existing double-click/drag conversion routes','literal yellow-real contrast only']
 # All other pre-existing case fields/IDs remain exact unless the finite diff explicitly records them.
 def unknown(n,rid,title,kind,action,blocks,contexts):
  r=rm[rid];return dict(id=f'WFW-{n:03}',requirements=[rid],title=title,kind=kind,preconditions=['F0','positive-path-gate'],setup_and_action=action,source_claim=r['contract'],documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,source_blocks=r['source_blocks'],source_context_blocks=blocks,finite_contexts=contexts)
 cases += [unknown(89,'REQ-WFW-U-STATE','Initial and prior preference histories','boundary','Future independently admitted known initial preference provenance is separate from explicit edits, existing saved markers/ASD, templates, prior choices or migration. Before any policy edit retain source-described warped-follow default, short Auto default, long Auto-Warp enabled default, Beats initial Default Warp Mode and short/long-example setup wording as distinct histories. Then explicitly choose admitted settings on separate owned copies. No factory/reset/migration or universal Auto-always-warp outcome is supplied; missing provenance remains U.',['WFW:B025','WFW:B043','WFW:B044','WFW:B045','WFW:B065','WFW:B081'],['known initial provenance','explicit prior preference edits','saved marker/default/template history','literal short enabled wording not a fifth policy']),unknown(90,'REQ-WFW-U-AUTO','Short and long correction example histories','analysis','Future independently known musical length/downbeats, source/display/region bounds and genuine eligible productive Auto-Warp context first. Preserve literal odd/default4/4/nine-versus-eight/bar-eight advice without silently correcting it or predicting a target coordinate. In separate admitted odd-loop histories retain end-marker insertion and end-marker visibility drag; in uneven-short history use downbeat insert marker/Set1.1.1 then basic Warp From and separately a marker before independently known tail silence. Separately establish a long result with appropriate tempo but wrong downbeat before each source method: selected-real-marker Shift waveform, long Set1.1.1 moving start marker, and zoom/create known downbeat marker then drag to first bar. Generic gestures or muted output do not establish these preparation histories. No silence detector, sync/cycle, crop, true-marker map, region transform or generated outcome oracle.',['WFW:B071','WFW:B072','WFW:B073','WFW:B075','WFW:B076','WFW:B077','WFW:B085','WFW:B086','WFW:B087','WFW:B088'],['literal odd nine/eight/bar-eight context','odd-loop endpoint/visibility examples','uneven-short origin then Warp From','known-tail-silence marker advice','genuine long correct-tempo/wrong-downbeat before three methods']),unknown(91,'REQ-WFW-U-TIMING','Editor Follow positive scrolling and restart contexts','timing','Future ClipView031-owned display histories: independently establish genuine Sample Editor scrolling Follow during productive playback, then make the admitted editor edit and retain actual display observations. In separate histories request playback, click Arrangement scrub and click clip scrub to request restart. Enabled switch or active input alone is not scrolling proof. Keep this editor Follow distinct from Tempo Follower and keep CV001 entry routes partial: its Arrangement MIDI action does not establish Arrangement-audio entry. No display deadline, clock, detector, tempo, automatic restoration or input-unavailability pass.',['WFW:B054'],['genuine scrolling Follow before edit','launch playback','Arrangement scrub','clip scrub','existing owner context, no duplicate normative role'])]
 fixture=deepcopy(load(P/'fixtures.json'));fixture['R2-positive-contexts']='Future only: actually active playing leader and genuine nonempty generated uneditable tempo automation; genuinely interpreted Tempo Follower without leader before override; genuinely scrolling editor Follow before pause/restart; productive independent roughly matched external reference for Nudge; eligible seamless-loop suggestion before Warp Sample as invocation. Flags, input, button state or generic output alone do not prove those processing roles.'
 fixture['R2-source-history']='Record independent source class/beat/downbeat/true length, actual saved-marker/no-saved history, first/prior analysis and exact platform/format, initial preference provenance versus explicit edits, source/display/region bounds, left/right marker inventory and each offered variant/interior/start-marker context. No default, detector, automatic map or universal readiness oracle.'
 fixture['R2-owner-boundaries']='ClipView046/Media010 retain sample-default save laws; clip-title Save control identity remains U. Editor Follow remains CV031; CV001 scoped route is not all Arrangement-audio entry coverage. Sync R3 current canonical has29/42, but pinned audit Sync R1 catalogs remain historical and are not silently substituted.'
 outputs={'old-files-r2.json':dict(files=old,original_review=dict(path=str((B/'reviews/warping-workflows-review.json').relative_to(ROOT)),**identity(B/'reviews/warping-workflows-review.json')),scope='All14originalpayloads+manifest remain exact in place; original review remains at its external path. No full archive.'),'requirements-r2.json':reqs,'cases-r2.json':cases,'fixtures-r2.json':fixture}
 # Finite exact-path pin inventory, captured before canonical mutation. No fuzzy/ancestor matching.
 targets={path:identity(P/n) for n,path in prior['canonical_snapshots'].items()};consumer_rows=[];consumer_files=set()
 def scan(v,ptr=''):
  if isinstance(v,dict):
   matches=[(k,x) for k,x in v.items() if isinstance(x,str) and x in targets and v.get('sha256')==targets[x]['sha256']]
   if matches:
    route=matches[0][1];asof=any(k in v for k in ['snapshot','source_bytes_as_of'])
    yield ptr,v,route,'as-of copied snapshot, unaffected' if asof else 'historical live canonical pin; resolve exact R1 snapshot'
   for k,x in v.items():yield from scan(x,ptr+'/'+k.replace('~','~0').replace('/','~1'))
  elif isinstance(v,list):
   for i,x in enumerate(v):yield from scan(x,ptr+'/'+str(i))
 for q in sorted(B.rglob('*.json')):
  try:d=load(q)
  except (UnicodeError,json.JSONDecodeError):continue
  for ptr,row,path,kind in scan(d):
   consumer_rows.append(dict(consumer=str(q.relative_to(ROOT)),consumer_identity_as_of=identity(q),pointer=ptr,canonical=path,record=deepcopy(row),disposition=kind,historical_snapshot=str((P/('spec-r1.md' if '/specs/' in path else 'research-r1.md')).relative_to(ROOT))))
   if kind.startswith('historical live'):consumer_files.add(q)
 assert len(consumer_files)==5
 outputs['canonical-consumers-r2.json']=dict(scope='As-of full-spec-v1 JSON exact path plus original canonical hash in same pin record. Own R1 canonical_snapshot routes also remain historical. No continuing or repository-wide sweep.',own_R1_snapshot_routes=prior['canonical_snapshots'],records=consumer_rows,direct_live_pin_records=sum(r['disposition'].startswith('historical live') for r in consumer_rows),resolution='Five exact direct spec rows resolve existing spec-r1 bytes; copied as-of contexts already use their snapshots. Do not rewrite consumers, old data or root tools, and do not run old validators against current R2 canonical pages. Root owns historical replay.')
 adopted={1:[1],2:[45],3:[46],4:[47],5:[89],6:[7,48],7:[10],8:[87],9:[90],10:[91],11:[21],12:[80],13:[24,54],14:[27,90],15:[29],16:[32,33,34,35,57,58,59,60]}
 groups=[]
 for g in load(A/'proposed-deltas-derived.json'):
  n=int(g['id'][1:]);groups.append(dict(audit_group=g['id'],audit_pointer='/'+str(n-1),title=g['title'],claim_ids=g['claim_ids'],source_blocks=g['source_blocks'],case_ids=[f'WFW-{i:03}' for i in adopted[n]],case_pointers=['/'+str(i-1) for i in adopted[n]],adoption='bounded finite actions/source-role context only; actual outcomes stay U, not complete group closure',retained_unknowns=g['scope'],new_normative_IDs=[],private_or_numerical_law=False))
 outputs['audit-adoption-r2.json']=dict(audit_manifest=dict(path=str((A/'manifest.json').relative_to(ROOT)),**identity(A/'manifest.json')),audit_review=dict(path=str(review.relative_to(ROOT)),**identity(review)),groups=groups,original_explicit_routes_retained=['WFW-008','WFW-018','WFW-022'],source_clauses_refined=[f'REQ-WFW-{n:03}' for n in contracts],Q032='open',zero_completed_topics=True)
 def diff(old,new,ptr=''):
  if old==new:return []
  if isinstance(old,dict) and isinstance(new,dict):
   out=[]
   for k in sorted(set(old)|set(new)):
    pp=ptr+'/'+k.replace('~','~0').replace('/','~1')
    if k not in old:out.append(dict(pointer=pp,operation='add',old=None,new=new[k]))
    elif k not in new:out.append(dict(pointer=pp,operation='remove',old=old[k],new=None))
    else:out+=diff(old[k],new[k],pp)
   return out
  if isinstance(old,list) and isinstance(new,list) and ptr=='':
   out=[]
   for i,x in enumerate(old):out+=diff(x,new[i],'/'+str(i))
   for i,x in enumerate(new[len(old):],len(old)):out.append(dict(pointer='/'+str(i),operation='add',old=None,new=x))
   return out
  return [dict(pointer=ptr,operation='replace',old=old,new=new)]
 deltas=[]
 for a,z,x,y in [('requirements.json','requirements-r2.json',oldreq,reqs),('cases.json','cases-r2.json',oldcases,cases),('fixtures.json','fixtures-r2.json',load(P/'fixtures.json'),fixture)]:
  deltas += [dict(old_file=a,new_file=z,**d) for d in diff(x,y)]
 outputs['delta-r2.json']=dict(prior_manifest=dict(path=str((P/'manifest-author-r1.json').relative_to(ROOT)),**identity(P/'manifest-author-r1.json')),field_deltas=deltas,old_requirement_IDs_retained=50,old_case_IDs_retained=88,new_normative_IDs=[],new_case_IDs=['WFW-089','WFW-090','WFW-091'],untouched_fields='Every field not in this exact delta is unchanged; old files remain byte-identical.',scope='Four clause contracts, finite action/source-claim/documentary-context refinements and three all-null U proposals; no numeric/DSP/protocol/lifecycle law.')
 paths={P/n for n in oldnames}|{A/'manifest.json'}|{A/n for n in load(A/'manifest.json')['files']}|{ROOT/r['path'] for r in load(A/'input-pins.json')}|consumer_files|{review,B/'reviews/warping-workflows-review.json',ROOT/'tools/spec_browser.py'}
 outputs['inputs-r2.json']=[dict(path=str(q.relative_to(ROOT)),**identity(q)) for q in sorted(paths)]
 for n,v in outputs.items():
  assert not (P/n).exists(),n
  (P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
 spec=(P/'spec-r1.md').read_text().replace('revision: 1\n','revision: 2\n',1)
 for before,after in zip(oldreq,reqs):
  if before['contract']!=after['contract']:assert before['contract'] in spec;spec=spec.replace(before['contract'],after['contract'],1)
 spec=spec.replace('/warping-workflows/fixtures.json','/warping-workflows/fixtures-r2.json')
 spec=spec.replace('All 88 cases are unexecuted and target-U/null. Forty-one have documentary visible\ncontrol/state predicates; 47 have null documentary oracles.','All91 current cases are unexecuted and target-U/null. Forty-one have documentary\nvisible control/state predicates;50 have null documentary oracles.')
 spec=spec.replace('[cases.json](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/cases.json)','[cases-r2.json](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/cases-r2.json)')
 newrows=''.join(f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} | U / null; source claim only |\n" for c in cases[88:])
 spec=spec.replace('\n## Open obligations','\n'+newrows+'\n## Open obligations',1)
 spec=spec.replace('[Counts](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/counts.json)','[Historical R1 counts](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/counts.json)').replace('identify the bounded review packet. The read-only validator checks integrity,','identify the historical R1 review packet. Its preserved validator expects R1\ncanonical bytes and is historical after R2. The current checker below checks integrity,')
 spec+='''
## R2 retained-source audit adoption

[Current50 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/requirements-r2.json)
retain the same50IDs (44D12/sixU), with only001 direct tempo edit,003 source-only
Link tap-start position,021 gray/yellow textual distinction and029 invocation
role refined. No DSP, detector, timing or research claim gained a normative ID.
[Current91 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/cases-r2.json)
retain all88IDs and untouched fields. Fourteen future/operational families stay U;
three added cases cover initial/prior preferences, source-specific short/long
correction examples and ClipView-owned scrolling Follow contexts. All actual
outcomes are null/U/unexecuted; timing/signal/analysis/file/operational documentary
oracles remain null. Named visible predicates never grade Link alignment,
tempo numbers, generated markers or file results.

[Sixteen adoption routes](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/audit-adoption-r2.json)
come from the [reviewed source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-source-audit/README.md).
Known productive active leader/generated automation, genuinely interpreted
Tempo Follower and actual editor scrolling precede negative/override observations;
flags, input or a lit button alone are insufficient. Nudge now admits a separate
productive roughly matched external reference. Warp Sample as is explicitly
invoked after a genuine eligible seamless-loop suggestion before-state. Each
actually offered Warp From variant retains left/right inventories and interior/
start-marker histories; basic no-selection insertion is not borrowed by variants.

Already explicit008 Unfollow and018/021/022 transient/pseudo gestures stay partial
routes; they were not newly invented. Short Set1.1.1 Warp Marker versus long
start-marker roles, literal nine/eight/bar-eight advice and Q032 all-first-import
versus media long-analysis wording remain distinct and unresolved where needed.
CV001's Arrangement-MIDI action is not all Arrangement-audio entry coverage.
ClipView046/Media010 retain default-save laws; clip-title Save control identity
and all actual save/file/eligibility outcomes remain U. Current Sync R3 has29/42;
the audit's old R1 Sync catalogs remain as-of context, not silently substituted.

[Exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/delta-r2.json)
and [consumer inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/canonical-consumers-r2.json)
preserve all original14payloads/seal and existing snapshots in place; no whole
archive or consumer/tool rewrite. Five exact direct spec-canonical pins require
old spec-r1 bytes, while copied as-of contexts are already independent. Root
owns combined replay/shared integration. [Read-only R2 checker](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/validate-r2.py)
and [R2 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manifest-author-r2.json)
freeze this partial successor pending separate independent owner review.
'''
 research=(P/'research-r1.md').read_text().replace('revision: 1\n','revision: 2\n',1).replace('## Packet and verification limits','## Historical R1 packet and verification limits',1)
 research+='''
## R2 bounded retained-source audit adoption

The [full retained-chapter audit](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-source-audit/README.md)
and [independent audit review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/warping-source-audit-review.json)
assessed131blocks/248facets against the original50clauses/88actions. The reviewer
was independent from that audit's author while disclosing original Warp-owner
authorship; this is not renewed independent approval of that owner. R2 awaits a
separate owner reviewer. All16 groups are adopted only as bounded source/control/
action contexts; text accounting and proposals do not close every implication.

[Versioned requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/requirements-r2.json)
keep50IDs/44D12/sixU. Four contracts add direct tempo edits, qualitative Link
positions on tap-start, gray-pseudo/yellow-real wording and Warp Sample as
invocation role. [Versioned cases](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/cases-r2.json)
keep88existing IDs/untouched fields and add three all-null U histories (91total;
41visible documentary/50null). No private mechanism, research-only recommendation,
initial preference, automatic marker, source example or lifecycle unknown gets a
new normative ID, signal/tempo/timing/file/numeric oracle or exact-target grade.

Actual Leader means independently active playing leader, not a flag or audio
activity; generated Main automation must be genuinely nonempty/uneditable before
movement. Actual Tempo Follower interpretation precedes leader override without
an active leader in the initial history. Editor Follow must genuinely scroll
before edit/pause/restart histories, and remains CV031-owned. WFW008/018/022 old
explicit actions remain exact, and021 preserves its double-click/drag routes.
WFW048 no longer treats positive audio/flags as proof of actual tempo leadership.
Rough external reference context is admitted independently for Nudge; no roughness
bound, curve, phase or correction guarantee is invented. Each Tap input and
shorter/longer history remains qualified without accuracy/deadline laws.

Initial/default provenance stays separate from explicit policies/saved samples/
templates/migration. The source's short enabled wording is not a fifth selector
or Auto-always-warp. Q032 remains open: source exact formats, selected audio track,
command-versus-drag destinations and both playback/edit readiness are recorded,
without replacing media long-analysis context or making a universal codec law.
Short-loop versus long Set1.1.1 roles, literal nine/eight/bar-eight advice,
source/display/region lengths and genuine wrong-downbeat Auto-Warp histories
stay distinct. No source example becomes a guaranteed detector/coordinate result.

Sample-default Save scope remains ClipView046/Media010-owned. Clip-title Save
entry and default-save control identity are retained as distinct until proven;
owned successful baseline precedes available Core Library/Pack eligibility
contrast, without mutating original content or claiming missing content proves
exclusion. Saved-marker ordinary Auto-Warp is separate from analysis and all
actually offered manual Warp From variants; left/right and interior/start-marker
histories are explicit without generated map/list/boundary laws. Warp Sample as
now invokes the admitted command after actual offered suggestion context, with
all generated values/audio U. CV001 entry remains scoped, not all audio/view
coverage. Current Sync R3 canonical29/42 does not rewrite audit R1 catalog context.

[Original file pins](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/old-files-r2.json)
retain every14payload+seal and original review in place. [Consumer inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/canonical-consumers-r2.json)
records five direct live spec pins for exact spec-r1 resolution and already copied
as-of contexts, with no consumer/root-tool change. Original checkers expecting
live R1 pages are historical. [R2 delta](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/delta-r2.json)
and [R2 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manifest-author-r2.json)
bind the partial successor; root owns shared maps and combined historical replay.
No recapture, original/helper execution, runtime, network/account/hardware/media
trial, tool installation or candidate work occurred. All target outcomes remain
null/U/unexecuted and no source-topic/product/leaf is complete.
'''
 for name,text,path in [('spec-r2.md',spec,ROOT/'wiki/specs/warping-workflows.md'),('research-r2.md',research,ROOT/'wiki/research/warping-workflows.md')]:
  assert not (P/name).exists();(P/name).write_text(text);path.write_text(text)
if __name__=='__main__':write()
