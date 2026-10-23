"""Initial R2 analyst authoring only. No capture/runtime. Refuses after R2 seal."""
from pathlib import Path
from copy import deepcopy
from itertools import combinations
import json
import hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert not (P/'manifest-author-r2.json').exists(),'Frozen successor: refuse mutation'
def load(p):return json.loads(p.read_text())
def put(name,data):(P/name).write_text(json.dumps(data,indent=2)+'\n')
def pin(path):
 data=path.read_bytes();return dict(path=str(path.relative_to(ROOT)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
old=load(P/'requirements.json');oldcases=load(P/'cases.json');requirements=deepcopy(old);cases=deepcopy(oldcases)
assert len(old)==18 and len(oldcases)==29
blocks={b['id']:b for b in load(P/'source-blocks.json')}
def evidence(n):
 b=blocks[f'STEM-B{n:03d}'];return dict(block=b['id'],anchor=b['anchor'],html_line=b['html_line'])
new=[dict(id='REQ-STEM-SEPARATION-016',title='Generated-stem ordinary audio-clip eligibility',contract='The manual describes successfully created stems as ordinary audio clips that can be warped, chopped, rearranged and processed with effects. This adds the generated-stem eligibility bridge only. Existing Clip View, Arrangement, Warp and device-hosting owners retain each operation and all finite laws; no Warp DSP, split boundary, effect algorithm, purity or audio equivalence is established.',strength='D12',target_applicability='U',evidence=[evidence(2)]),dict(id='REQ-STEM-SEPARATION-017',title='Crop preparation entry points',contract='Before separation, the manual describes shortening an intended region using Crop Clip Sample to Time Selection in the Sample Editor or Crop Clip on an Arrangement time selection through the track context menu. The stated shortcut for both applicable Crop commands is CtrlShiftJ on Windows and CmdShiftJ on Mac. Clip View retains crop behavior and its qualified shortcut law; this adds only the source-specific preparation entry points. Keyboard focus, sample boundaries, file rewriting and actual separation-time changes remain unknown.',strength='D12',target_applicability='U',evidence=[evidence(29)])]
requirements+=new
by={c['id']:c for c in cases}
def refine(cid,action,contexts):
 c=by[cid];c['setup_and_action']=action;c['finite_contexts']=contexts;c['refines_R1_case']=cid
names=['Vocals','Drums','Bass','Others'];masks=[list(c) for n in range(1,5) for c in combinations(names,n)]
refine('STEM-002','In six separate reset trials select an independently admitted Browser audio file, Session audio clip or Arrangement audio clip, each through its offered context-menu and Create-menu Separate Stems to New Audio Tracks route. Inspect the options dialog before accepting. Unsupported inputs, absent commands and enablement remain U.',[dict(source=v,menu=m) for v in ['Browser audio file','Session audio clip','Arrangement audio clip'] for m in ['context menu','Create menu']])
refine('STEM-003','Inspect the four named toggles on a known admitted multicomponent nonzero source. Explicitly select every one of the fifteen nonempty masks in separate reset dialogs, retaining selected names and source context. These are toggle/inclusion-role observations, not classifier or reconstructed audio checks. Zero selection remains in the U-boundary case.',[dict(selected_elements=m) for m in masks])
refine('STEM-007','In owned Set copies with explicit source-track color use two, three and four unmerged named elements. Inspect created clip/track/group roles and the textual toggle/group color relationships without image palette or pixel values. Actual output, ordering and Browser source-less color stay U.',[dict(elements=names[:n],merge=False) for n in [2,3,4]])
refine('STEM-008','With known admitted input and explicit source-track color, separate each named singleton in separate copies, then a merged pair and a merged triple. Inspect one-track/clip versus group presence and documented color roles only. Nongroup effects/automation destinations and merged audio remain U.',[dict(elements=[n],merge=False) for n in names]+[dict(elements=names[:n],merge=True) for n in [2,3]])
refine('STEM-009','Use independently indexed nonzero audio with distinct before/inside/after landmarks. In Session and Arrangement copies separately, explicitly set a nonempty adjusted start/end region with loop off, then a warped-loop/start-marker setup with Warp and loop on. Retain exact markers/settings and observations without a sample/frame/loop-cycle or output-audio oracle.',[dict(view=v,region=r) for v in ['Session','Arrangement'] for r in ['adjusted start/end, loop off','warped clip, active loop, explicit start marker']])
refine('STEM-010','Create a nonempty interior time selection in one owned Arrangement clip with independently indexed nonzero before/inside/after landmarks. Invoke Separate Stems for Time Selection from its clip context menu and explicitly inspect the same named separation options dialog before Separate. Then retain segmentation/stem-region observations separately. All boundary, signal and transaction outcomes/comparators remain null.',[dict(stage=s) for s in ['selection and context entry','same options dialog before Separate','post-Separate segmentation and region; ungraded']])
refine('STEM-013','In separate owned empty Set copies focus Session and Arrangement explicitly and enable sample warping, then choose an admitted nonzero Browser source and Separate. Retain focus/source/tempo settings. In separate copies record nonempty and sample-Warp-off branches as unknown; no detector, empty-Set definition or numeric tempo oracle.',[dict(view=v,Set_state=e,sample_warp=w,outcome='U') for v in ['Session','Arrangement'] for e,w in [('empty',True),('nonempty',True),('empty',False),('nonempty',False)]])
refine('STEM-014','Use independently valid source type/rate/depth and an owned saved writable Project with a separately successful file-generation baseline. In separate copies retain actual file inventories for an unmerged subset, merged pair and merged triple. If two independently offered/accepted output types are available, select each separately without inventing their names; retain actual path/header/type/rate/depth metadata. All file, codec, header, numeric and sample-rate outcomes/comparators remain null.',[dict(elements=names[:n],merge=m,output_type_context=t) for n,m in [(2,False),(2,True),(3,True)] for t in ['independently offered accepted type A','distinct independently offered accepted type B, if available']])
refine('STEM-U-AUDIO','Retain independent admitted nonzero multicomponent owned stimuli and genuine successful separation before any bleed/reconstruction/quality observations. Include separately owned hi-hat-rich and chorus-synth contexts only if admitted; the source examples are possible overlap, never expected mandatory content. Preserve each source/output under both modes with null signal/purity comparators.',[dict(source_context=s,mode=m) for s in ['owned multicomponent baseline','owned hi-hat-rich example, if available','owned chorus-synth example, if available'] for m in ['High Speed','High Quality']])
refine('STEM-U-MODE','Use identical independently admitted owned sources after genuine successful positive runs. In reset copies retain High Speed and High Quality with explicit Drums+Vocals, Vocals+Others and all-four masks, plus a nonempty crop preparation in each mode. Retain actual observations and Set/file inventory. Qualified timing and possible-overlap narratives remain research only; no duration equality/speedup, SDR, purity, stochastic, private-pass or reconstruction oracle.',[dict(mode=m,elements=x) for m in ['High Speed','High Quality'] for x in [['Drums','Vocals'],['Vocals','Others'],names]])
refine('STEM-U-UNDO','After independently successful grouped, singleton, merged and time-selection work in separate owned copies, invoke actually offered Undo/Redo separately. Record tracks/clips/devices/envelopes/source activation and generated references/files. No undoability, grouping or file rollback is presumed.',[dict(branch=b,operation=o) for b in ['grouped','singleton','merged','time-selection'] for o in ['offered Undo','offered Redo']])
refine('STEM-U-CANCEL','In separate reset copies observe offered Cancel/close before Separate, then actually offered cancellation/close while pending after a known successful baseline. Record explicit element/mode/Merge state, source activation, transport and partial files; record reopen state separately without a default/retention/cleanup guarantee. Cancellation availability is unknown.',[dict(checkpoint=s,action=a) for s in ['dialog before Separate','active pending process, if offered'] for a in ['offered Cancel','offered dialog close']])
refine('STEM-U-PERSISTENCE','After independently successful grouped, singleton, merged and time-selection separation, save/reopen disposable owned Projects and retain tracks/devices/envelopes, source activation and generated file references. Record reopened dialog element/mode/Merge settings independently. No Set/global retention, automatic repair or deep-copy identity law is supplied.',[dict(branch=b) for b in ['grouped','singleton','merged','time-selection']])
refine('STEM-U-LOSS','After separately established readable-source, writable-destination and successful-separation baselines, define separate authorized disposable owned-source-unavailable, output-unavailable and destination-unavailable trials at before-start/pending/completed checkpoints where actually meaningful. Record failures/partial state only; no real disk exhaustion, file mutation or failure injection is performed by this packet and no transaction/cleanup result is predicted.',[dict(context=c,checkpoint=s) for c in ['owned source unavailable','owned generated output unavailable','owned destination unavailable'] for s in ['before Separate','pending, if applicable','after completion, if applicable']])
refine('STEM-U-RATE','After independently successful supported baselines, retain changed accepted source/output/audio rate, buffer and quality settings in separate reset copies and repeated offline observations. Record actual acceptance, elapsed observations and resources without CPU/GPU topology, speedup, timeout or numeric output law.',[dict(context=c) for c in ['accepted rate change','accepted buffer change','quality-mode change','repeated identical-source trial']])
refine('STEM-U-TRANSPORT','After separately eligible positive separation and recording/playback baselines, request separation from playing/stopped/recording contexts in separate copies. Retain actually accepted pending seek/focus changes and ordering without concurrent-command acceptance, clock or stop-deadline guarantees.',[dict(transport=s) for s in ['playing','stopped','recording, if offered']])
refine('STEM-U-TEARDOWN','From an independently successful owned baseline, close offered dialog/clip/track/Set/application contexts separately before accept, while pending and after completion where meaningful. Record prompts, source activation, resources, references and pending recording state. No cancellation, cleanup, persistence or auto-restart law is assumed.',[dict(object=o,checkpoint=s) for o in ['dialog','clip','track','Set','application'] for s in ['before accept, if applicable','pending, if applicable','after completion']])
for r,action,contexts in [(new[0],'After separately admitted successful stem creation, use reset owned copies to inspect Warp edit eligibility, a nonempty interior chop/split, rearrangement and effect processing entry on generated clips. Retain existing owner predicates and independently active nonzero wet/output baseline before effect/no-effect observations. Observe named clip/track/control roles only; all actual audio and finite-law comparisons require their existing owners.',[dict(operation=x) for x in ['Warp eligibility/edit entry','interior chop/split','rearrange generated clip','effect processing entry']]),(new[1],'In separate disposable owned copies with a successful separation baseline, use a nonempty interior region and invoke each source-described crop preparation route, then reopen separation. Retain the exact source/region/context and existing Clip View crop-owner law. For independently admitted Windows/Mac focus contexts retain the documented applicable CtrlShiftJ/CmdShiftJ shortcut, respectively; absent platform/command stays U. No crop sample, file or timing result is graded.',[dict(route=r,platform=p,shortcut=k) for r in ['Sample Editor: Crop Clip Sample to Time Selection','Arrangement time selection: track context Crop Clip'] for p,k in [('Windows','CtrlShiftJ'),('Mac','CmdShiftJ')]])]:
 c=dict(id='STEM-'+r['id'].split('-')[-1],requirements=[r['id']],kind='control',fixture='fixtures-r2.json#STEM-OWNED',setup_and_action=action,source_claim=r['contract'],documentary_expected=r['contract'],documentary_comparator='Named visible clip/control/command eligibility or entry-point roles only; no signal, sample, file, numerical or timing outcome.',expected=None,comparison=None,target_grade='U',executed=False,evidence=r['evidence'],finite_contexts=contexts);cases.append(c)
cases.append(dict(id='STEM-U-AVAILABILITY',requirements=['REQ-STEM-SEPARATION-U-LIFECYCLE'],kind='availability',fixture='fixtures-r2.json#STEM-OWNED',setup_and_action='Record independently known exact build/edition/platform and actual offered feature/command/model availability before any source or failure trial. Current Version12 text cannot supply target12.4.3 presence, entitlement or installed-model state. No install, account/license action or model download is authorized/performed. Missing availability remains U, never an input-rejection or negative pass.',source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,evidence=[],finite_contexts=[dict(context=c) for c in ['exact build/edition/platform identity','offered command/feature availability','independently established model availability, if obtainable']]))
for c in cases:c['fixture']='fixtures-r2.json#STEM-OWNED'
put('requirements-r2.json',requirements);put('cases-r2.json',cases)
fixture=load(P/'fixtures.json');fixture['status']='R2 future owned setup only; no audio/stems/model/reference results supplied';fixture['source_audit_adoption']='All13 approved delta groups adopted with source-specific entry/context refinements; performance/overlap remain research/U. Explicit exact-target availability is a separate U case.';put('fixtures-r2.json',fixture)
redirects=[]
for rel,key in [('inventory-revisions/r4-citation-crosswalk/inputs.json',None),('stem-separation-source-audit/input-pins.json',None)]:
 data=load(B/rel)
 data=data['pins'] if isinstance(data,dict) else data
 for i,r in enumerate(data):
  if r['path'] in ['wiki/specs/stem-separation.md','wiki/research/stem-separation.md']:
   snap='spec-r1.md' if '/specs/' in r['path'] else 'research-r1.md';q=P/'archive-r1'/snap;v=pin(q);assert all(v[k]==r[k] for k in ['bytes','sha256'])
   redirects.append(dict(consumer=str((B/rel).relative_to(ROOT)),record_pointer=('/pins/' if rel.startswith('inventory-revisions') else '/')+str(i),original_path=r['path'],original_bytes=r['bytes'],original_sha256=r['sha256'],historical_snapshot=v,reason='Exact R1 canonical bytes via immutable snapshot; no current R2 bytes borrowed into historical validation. No source/citation semantic identity changed.'))
assert len(redirects)==4;put('historical-pin-redirects-r2.json',redirects)
review=B/'reviews/stem-separation-source-audit-review.json';assert pin(review)['sha256']=='84ca8ab89bd5fb69c7f7221d0fb14543167257bf420cad09c6029351f4a90828'
inputs=[ROOT/'tools/spec_browser.py']+[P/n for n in load(P/'manifest-author-r1.json')['files']]+[P/'manifest-author-r1.json',review,B/'reviews/stem-separation-review.json']
for rel in ['stem-separation-source-audit','inventory-revisions/r4-citation-crosswalk']:
 folder=B/rel;mf=folder/('manifest.json' if rel.endswith('audit') else 'manifest.json');m=load(mf);inputs+=[mf]
 fs=m['files'];inputs +=[folder/n for n in fs]
inputs +=[ROOT/r['path'] for r in load(B/'stem-separation-source-audit/input-pins.json') if r['path'] not in ['wiki/specs/stem-separation.md','wiki/research/stem-separation.md']]
put('inputs-r2.json',[pin(q) for q in sorted(set(inputs))])
put('archive-r1-pins.json',[pin(q) for q in sorted((P/'archive-r1').iterdir())])
counts=dict(requirements=len(requirements),strengths={'D12':17,'U':3},cases=len(cases),documentary_visible_cases=sum(c['documentary_expected'] is not None for c in cases),all_target_null_U_unexecuted=True,old_requirements_retained=18,old_cases_retained=29,new_requirement_IDs=2,new_case_IDs=3,adopted_audit_groups=13,historical_Stem_pin_redirects=4,source_blocks_unchanged=32,completed_topics=0);put('counts-r2.json',counts)
put('audit-adoption-r2.json',dict(review=pin(review),audit_manifest=pin(B/'stem-separation-source-audit/manifest.json'),status='successor-author-adoption-awaiting-independent-review',groups=[dict(id=f'G{i:02d}',adopted=True,route=route) for i,route in enumerate(['new016 eligibility bridge/case','002 six menu contexts','003 fifteen masks','007 three-unmerged context','008 three-merged context','009 both-view region contexts','010 explicit dialog stage','014 file-generation/type contexts','new017 crop-entry bridge/case and research timing context','research timing + U-MODE masks','research overlap + U-AUDIO contexts','U lifecycle checkpoint refinements','new U-AVAILABILITY case'],1)],unchanged_original_catalogs=['requirements.json','cases.json'],no_new_timing_purity_or_private_architecture_law=True,historical_redirects='historical-pin-redirects-r2.json',counts=counts))
oldspec=(P/'spec-r1.md').read_text();intro=oldspec[:oldspec.index('## Requirements')].replace('revision: 1','revision: 2',1)
intro=intro.replace('result placement, source-region/effect/automation roles and generated-file context.','result placement, source-region/effect/automation roles, generated-file context and\nsource-backed generated-clip/crop-preparation entry points.')
intro+='''R2 adopts the independently reviewed retained-source audit as a partial successor.
[Audit adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/audit-adoption-r2.json)
records all thirteen groups. Original eighteen clauses retain their exact wording;
two narrow entry/eligibility bridges add no finite operation, timing or DSP law.
All current source, target and lifecycle limits above remain.

## Requirements

Use [future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/fixtures-r2.json).
Independently establish available feature/model, admitted nonempty owned source
and successful separation before absence/invalid/failure probes. Active nonzero
wet/output and distinguishable automation are required where relevant. No assets
or execution are supplied. Compound branches remain partial.

'''
spec=intro
for r in requirements[:15]+new+requirements[15:18]:
 spec+=f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}\n\n"
 if r['evidence']:spec+='Evidence: '+', '.join('`'+e['block']+'`' for e in r['evidence'])+'; [exact routes](#analysis-only-evidence).\n\n'
oldtail=oldspec[oldspec.index('## Source-context questions and acceptance proposals'):]
oldtail=oldtail[:oldtail.index('[29 cases]')]+'''[Current R2 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/cases-r2.json)
retain all twenty-nine old IDs with explicit source/menu, nonempty selection,
group/merge, region/view/dialog/file and lifecycle context refinements. Two new
bridge cases and a separate feature-availability U case give thirty-two cases for
twenty requirements (17D12/3U). Ten named visible control/state proposals have
qualified documentary outputs; every signal/file/timing/U documentary result and
every actual target result/comparator remains null/U/unexecuted. Qualitative
crop/subset/Others timing and possible-overlap examples remain research and U
probes, never mandatory performance or purity laws.

## Analysis-only evidence

'''+oldspec.split('## Analysis-only evidence\n\n')[1]
oldtail=oldtail.replace('[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/requirements.json)','[Current requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/requirements-r2.json)').replace('[author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/manifest-author-r1.json)','[R2 author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/manifest-author-r2.json)')
spec+=oldtail+'''
## Preserved history and read-only replay

The [R1 archive](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/archive-r1/manifest-author-r1.json)
retains all fourteen original files. Unsuffixed catalogs/snapshots/checkers are
historical R1 files. The [R2 checker](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/validate-r2.py)
validates current catalogs and exactly four disclosed historical Stem canonical
pin reads against byte-identical R1 snapshots. Old R4/audit rows, inputs and
tools remain unchanged. Their historical direct-current-canonical checker entry
points do not become current R2 checks; root owns combined crosspacket replay.
Focused independent R2 semantic review is pending; no completeness credit follows.
'''
(ROOT/'wiki/specs/stem-separation.md').write_text(spec);(P/'spec-r2.md').write_text(spec)
research=(P/'research-r1.md').read_text().replace('revision: 1','revision: 2',1)
research=research[:research.index('## Required next evidence and review')]+'''## Reviewed source-audit adoption and retained contexts

[The reviewed audit](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/stem-separation-source-audit-review.json)
reconciles all32 blocks and94 claim/context facets; this is source-text accounting,
not source/app completion. R2 minimally adopts its thirteen groups in
[audit-adoption-r2.json](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/audit-adoption-r2.json).
Generated stems gain only the documented bridge to existing ordinary audio-clip
operations. Crop preparation retains Sample Editor Crop Clip Sample to Time
Selection and Arrangement time-selection track-context Crop Clip; existing Clip
View crop laws/qualified Windows CtrlShiftJ and Mac CmdShiftJ remain canonical.
No crop boundary/file rewrite/finite-law duplication is introduced.

B029 says crop preparation can reduce separation time in either mode. B030 says
requesting only needed High Quality stems can shorten time, while including Others
removes that claimed reduction. These remain qualified publisher source contexts
and U-MODE observations with no mandatory speedup, duration equality, benchmark,
private pass count or output law. The old015 file/Set distinction remains unchanged.

B032 gives possible high-frequency hi-hat content in Others and chorus-synth content
in Vocals. Retain both as nonmandatory owned-stimulus contexts in U-AUDIO, with
all actual audio/purity/quality comparisons null. Neither bleed nor purity is
required for any particular input. Model/pass/CPU/GPU/SDR explanations remain
research context rather than required architecture or performance.

## Current catalogs, explicit contexts and limits

[Twenty R2 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/requirements-r2.json)
retain all18 old records verbatim and add only two source-backed bridges.
[Thirty-two R2 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/cases-r2.json)
retain all29 old IDs with finite action/context refinements, two bridge cases and
a separate target-feature-availability U case. Six source/menu routes, all15
nonzero toggle masks, three-unmerged/three-merged branches, both view/region
contexts, explicit selection-dialog inspection and file/type branches are named.
Concrete offered cancel/close, Undo/Redo, save/reopen, source/destination loss,
rate/transport and teardown checkpoints stay unknown, not lifecycle guarantees.

Ten visible control/state proposals have qualified documentary roles only.
All signal/file/timing/U documentary outputs/comparators and every actual target
result remain null/U/unexecuted. Availability, valid owned nonempty inputs,
genuine positive separation and relevant active nonzero wet/output/automation
baselines are prerequisites; missing feature/model/input or failed baseline is
inconclusive. No sources, model/stimuli, account/installation, real disk exhaustion,
file-destructive operation or runtime was acquired/performed.

## History, redirects and read-only frozen validation

All14 original files are byte-identical in place and in the
[R1 archive](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/archive-r1/manifest-author-r1.json).
The original18/29 catalogs, source/parser/tool bytes and old owner/audit reviews
remain unchanged. [Four disclosed redirects](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/historical-pin-redirects-r2.json)
resolve only historical Stem spec/research pin records in R4 and the Stem audit
to exact R1 snapshot bytes. The other Synchronization canonical identities are
excluded and untouched. No frozen inputs or historical pointer rows are rewritten,
and no current R2 bytes are passed off as old evidence. Original historical checker
entry points expecting live R1 canonicals are not claimed to pass against R2;
root owns combined crosspacket historical replay.

Inspect [validate-r2.py](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/validate-r2.py), then run:

```sh
python -B analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/validate-r2.py --check
```

It checks source/R1/archive/audit/review pins, all current IDs/finite contexts,
qualified nulls, exact Browser equality, narrow historical pin resolution,
canonical snapshots, links and whitespace without rewriting reports. The
[R2 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/manifest-author-r2.json)
freezes this partial successor for independent semantic review. Shared catalogs,
coverage, questions and logs remain root-owned; no runtime/completion credit is added.
'''
(ROOT/'wiki/research/stem-separation.md').write_text(research);(P/'research-r2.md').write_text(research)
print(json.dumps(counts,indent=2))
