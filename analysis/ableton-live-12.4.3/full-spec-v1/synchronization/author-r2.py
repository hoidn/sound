"""Initial bounded R2 analyst data/prose author; refuses after R2 freeze.
No network, original/helper/app/peer/hardware or candidate functions run.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import copy,json,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
load=lambda q:json.loads(q.read_text())
def pin(q):
 b=q.read_bytes();return dict(path=str(q.relative_to(ROOT)),bytes=len(b),sha256=sha256(b).hexdigest())
def put(n,v):(P/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

def build():
 reqs=copy.deepcopy(load(P/'requirements.json'));cases=copy.deepcopy(load(P/'cases.json'));assert len(reqs)==26 and len(cases)==36
 r={r['id']:r for r in reqs};c={c['id']:c for c in cases};blocks={b['id']:b for b in load(P/'source-blocks.json')}
 r['REQ-SYNC-WORKFLOW-005']['contract']='The dedicated Link Settings tab configures Link/Link Audio. The chapter describes the Control Bar Link toggle as displayed by default; this is documentary initial-visibility context, not an exact-build constructor, factory/reset, prior-preference or migration observation. Show Link Toggle can hide it; its adjacent menu switches Link/Audio features, lists connected Audio-enabled peers and offers Configure Link.'
 r['REQ-SYNC-WORKFLOW-012']['contract']='Show Tempo Follower Toggle exposes Follow, described alongside other tempo-related parameters at the left of the Control Bar. This textual placement context gives no pixel geometry or all-window-layout guarantee. Activating Follow enables listening; Tempo Follower does not run while Follow is hidden. If its configured input device channel cannot be connected, the feature is disabled and Follow appears grayed out.'
 r['REQ-SYNC-WORKFLOW-015']['contract']='MIDI Clock provides tempo-dependent ticks and song-position messages. Changing the sync host tempo is described as causing the receiving device to follow the change; Live can act as sender/sync host or receiver/device. No byte encoding, tick count, filtering, MIDI transport command sequence, numerical tracking/convergence or timestamp law is established.'
 for case in cases:
  case['fixture']='fixtures-r2.json#SYNC-OWNED'
  if case['source_claim'] is not None:
   case['source_claim']=r[case['requirements'][0]]['contract']
   if case['documentary_expected'] is not None:case['documentary_expected']=case['source_claim']
 def refine(id,action,contexts):
  c[id]['setup_and_action']=action;c[id]['finite_contexts']=contexts;c[id]['refines_R1_case']=id
 refine('SYNC-002','Before ordinary tempo edits, admit a session with an independently known first participant at a valid chosen tempo, then a compatible joining peer with a distinct valid prior tempo; retain actual membership order and initial tempo histories. After a genuine working two-peer baseline, change tempo from each peer separately with Set tempo automation off and active in separate copies. Keep simultaneous-change observations separate, without causal-order, convergence or numerical timing expectations.',[dict(stage=s) for s in ['known first participant before peer joins','joining peer initial tempo context','each peer separately; automation off','each peer separately; automation active','separate simultaneous-change probe, U']])
 refine('SYNC-005','With independently admitted exact-build Link/Audio capabilities, known peers and preference provenance, inspect initial Control Bar Link visibility before any explicit Show/Hide edit; previously customized settings cannot stand in for the documentary default context. In reset owned histories explicitly hide/show it, open the adjacent menu, exercise each actually offered Link/Audio on/off control separately, inspect the connected Audio-enabled peer list with a separately known Link-only/not-Audio peer contrast, and use Configure Link. Keep a connected Audio-positive baseline before exclusion/disabled observations; no reset/install, unknown peer or unavailable feature can prove a default, exclusion or failure.',[dict(context=s) for s in ['independently known initial preference provenance; no prior edit in this history','explicit Show/Hide settings, separate from initial visibility','adjacent menu offered Link on/off','adjacent menu offered Audio on/off; Link prerequisite retained','menu list: admitted connected Audio-enabled peer versus independently known Link-only peer','Configure Link opens dedicated settings tab']])
 refine('SYNC-012','With an independently admitted configured nonzero source and actual feature availability, show Follow and retain its textual placement alongside left Control Bar tempo controls. Explicitly activate Follow and independently establish a separately known genuine positive interpretation/tempo-following baseline; active input, a visible/lit control or generic peer tempo is insufficient. Then hide only Follow with the input/source context unchanged, retaining control and actual processing observations. Do not assume a tracking tolerance, cessation deadline, automatic re-enable or restored running state when shown again. In a separate history after a genuine positive baseline, make only the configured input unavailable and inspect disabled/grayed state. Missing capability or failed baseline remains U, never a negative pass.',[dict(context=s) for s in ['visible Follow and textual placement only','explicit Follow activation plus independently genuine tempo interpretation','hide only Follow; same admitted input/source, processing observations U','separate configured-input unavailable after positive running baseline']])
 c['SYNC-012']['kind']='signal';c['SYNC-012']['documentary_expected']=None;c['SYNC-012']['documentary_comparator']=None
 c['SYNC-012']['positive_processing_guard']='Independently known genuine active Tempo Follower interpreting the admitted input before hiding; active input/control visibility/peer count alone is not this baseline. No unavailable or failed baseline supplies a negative pass.'
 refine('SYNC-015','Use independently admitted compatible MIDI receiver/transmitter and retain genuine usable source traffic before separately configuring Live Clock-host and Clock-receiver roles. In a single-host receiving history with Link and Tempo Follower off, explicitly change the known host between two independently accepted tempos, retaining source traffic and Live tempo/transport observations. Keep the MTC manual-tempo/directional comparison separate. No guessed MIDI bytes, tick count, supported range, delay, tracking/convergence tolerance or transport-command sequence is an oracle.',[dict(context=s) for s in ['Clock host to independently valid receiver','Clock receiver from independently valid single host','host accepted tempo A then distinct accepted tempo B; Link/Follower off','separate Clock-versus-MTC roles; no wire equivalence']])
 refine('SYNC-016','Use an independently validated MTC source, explicitly set Live tempo and sync type, then vary source position separately from tempo and retain Arrangement observations. Preserve a distinct positive MIDI Clock-host trial and a genuine MTC-receiver baseline before requesting independently admitted exact-build evidence for the documented MTC receiver-only/not-host capability. Retain actually offered sync direction/type controls or authoritative evidence; do not infer an absent UI item, send guessed MTC messages or treat unavailable hardware/capability as a passed exclusion. No wire, rate, position, tempo or negative-capability oracle is supplied.',[dict(context=s) for s in ['MTC receiver: admitted source positions, manually set tempo','MTC does not supply tempo tracking; actual result U','distinct positive MIDI Clock-host baseline','MTC not-host capability evidence request, U if unavailable']])
 b=blocks['SYNC-B005'];new=dict(id='REQ-SYNC-WORKFLOW-025',title='Remaining-peer continuity on participant join or leave',contract='The manual describes participants joining or leaving a Link session at any time without interrupting synchronization between other remaining peers. This source continuity role supplies no discovery or membership order, leader election, wire protocol, phase/audio/jitter tolerance, convergence or interruption deadline. Exact-target and arbitrary-peer compatibility remain unknown.',strength='D12',target_applicability='U',evidence=[dict(block=b['id'],anchor=b['anchor'],html_line=b['html_line'])]);reqs.append(new)
 cases.append(dict(id='SYNC-025',requirements=[new['id']],kind='timing',fixture='fixtures-r2.json#SYNC-OWNED',setup_and_action='Independently establish genuine usable synchronization and nonzero active output at two admitted compatible peers A/B before a third known compatible peer C joins and then leaves in separate histories while A/B continue. Retain A/B actual tempo/phase/audio/transport traces as available plus all identities and membership history; peer count/name/LED alone is insufficient. Do not treat a silent path, absent peer, failed baseline or unavailable Link/Audio feature as a passed continuity test. No interruption deadline, numerical synchronization, clock or audio comparator is supplied.',source_claim=new['contract'],documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,evidence=new['evidence'],finite_contexts=[dict(context=s) for s in ['working A/B positive synchronization/output baseline','admitted C joins while A/B continue','separate admitted C leaves while A/B continue']]))
 fixture=copy.deepcopy(load(P/'fixtures.json'));fixture['status']='R2 future owned setup only; no source, peers, hardware, traffic or reference results supplied'
 fixture['Follower_positive_guard']=c['SYNC-012']['positive_processing_guard']
 fixture['initial_visibility_context']='Independently known offered-feature/build and preference provenance before explicit visibility edits; documentary default is not a factory/reset/migration assumption.'
 fixture['three_peer_context']='Continuity requires genuine synchronized/nonzero active A/B before compatible C joins/leaves; not a two-peer membership-only trial.'
 counts=dict(requirements=len(reqs),strengths=dict(Counter(x['strength'] for x in reqs)),cases=len(cases),documentary_visible_cases=sum(x['documentary_expected'] is not None for x in cases),documentary_null_cases=sum(x['documentary_expected'] is None for x in cases),all_target_null_U_unexecuted=True,old_requirement_IDs_retained=26,old_case_IDs_retained=36,new_requirement_IDs=1,new_case_IDs=1,adopted_audit_groups=9,historical_Sync_pin_redirects=4,source_blocks_unchanged=54,completed_topics=0)
 return reqs,cases,fixture,counts

def write():
 assert sys.argv[1:]==['--write'],'authoring requires --write'
 assert not (P/'manifest-author-r2.json').exists(),'Frozen R2: refuse mutation'
 reqs,cases,fixture,counts=build()
 for name,value in [('requirements-r2',reqs),('cases-r2',cases),('fixtures-r2',fixture),('counts-r2',counts)]:put(name+'.json',value)
 redirects=[]
 for relpath,pointerprefix in [('inventory-revisions/r4-citation-crosswalk/inputs.json','/pins/'),('synchronization-source-audit/inputs.json','/pins/')]:
  q=B/relpath
  for i,row in enumerate(load(q)['pins']):
   if row['path'] not in ['wiki/specs/synchronization-workflows.md','wiki/research/synchronization-workflows.md']:continue
   snap='spec-r1.md' if '/specs/' in row['path'] else 'research-r1.md';p=pin(P/'archive-r1'/snap);assert all(p[k]==row[k] for k in ['bytes','sha256'])
   redirects.append(dict(consumer=str(q.relative_to(ROOT)),record_pointer=pointerprefix+str(i),original_path=row['path'],original_bytes=row['bytes'],original_sha256=row['sha256'],historical_snapshot=p,reason='Resolve exact historical R1 canonical bytes only; preserve frozen R4/audit pins and all current/old catalog identities.'))
 assert len(redirects)==4;put('historical-pin-redirects-r2.json',redirects)
 audit=B/'synchronization-source-audit';review=B/'reviews/synchronization-source-audit-review-final.json'
 assert pin(review)['sha256']=='0074915897dcf80dab96c61db16322d1c9265763cdbfb4016582db76281c44f3'
 groups=[('SA-G01','new025 continuity clause/timing case'),('SA-G02','005 known initial visibility context'),('SA-G03','005 explicit adjacent-menu switches'),('SA-G04','005 explicit Audio-peer list contrast'),('SA-G05','002 first-participant initial history'),('SA-G06','012 textual Follow placement'),('SA-G07','015 qualitative Clock-host tempo following'),('SA-G08','016 MTC not-host capability evidence'),('SA-G09','012 genuine active-Follower baseline before hide; signal doc oracle null')]
 put('audit-adoption-r2.json',dict(audit_manifest=pin(audit/'manifest-author-r2.json'),review=pin(review),groups=[dict(id=id,route=route,adopted_as_partial=True) for id,route in groups],status='partial-successor-author-draft-awaiting-independent-review',unchanged_original_catalogs=['requirements.json','cases.json'],counts=counts,no_new_numeric_protocol_detector_or_default_algorithm=True))
 inputs=[ROOT/'tools/spec_browser.py',B/'reviews/synchronization-workflows-review.json',review]+[P/name for name in load(P/'manifest-author-r1.json')['files']]+[P/'manifest-author-r1.json']
 for folder,mname in [(audit,'manifest-author-r2.json'),(B/'inventory-revisions/r4-citation-crosswalk','manifest.json')]:
  mf=folder/mname;inputs.append(mf);inputs +=[folder/name for name in load(mf)['files']]
 for dep in load(P/'dependencies.json'):inputs.append(ROOT/dep['path'])
 for name in ['recording-comping','routing-monitoring-latency','clip-launch','session-launch-workflows','external-hardware-devices','video-workflows']:inputs.append(ROOT/f'wiki/specs/{name}.md')
 put('inputs-r2.json',[pin(q) for q in sorted(set(inputs))])
 spec=(P/'spec-r1.md').read_text();intro=spec[:spec.index('## Requirements')].replace('revision: 1','revision: 2',1)
 intro+='''R2 adopts nine independently reviewed retained-source audit proposals as a
partial successor. [Audit adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/audit-adoption-r2.json)
records the exact routes. A new source-only continuity clause does not broaden
membership indicators into synchronization proof. Existing hidden-Follow law
remains in012; its refined case now requires genuine running processing first.

## Requirements

Use [future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/fixtures-r2.json).
Explicitly establish usable compatible sources and nonzero active paths before
negative/absence trials. Hidden Follow requires independently genuine active
Follower interpretation before hiding; an active input or lit button alone is
insufficient. Initial Link visibility requires known preference provenance,
not assumed factory/reset state. No future action is a result or authorization.

'''
 out=intro
 for req in reqs[:24]+[reqs[-1]]+reqs[24:26]:
  out+=f"### {req['id']} — {req['title']}\n\n**{req['strength']}/target-U.** {req['contract']}\n\n"
  if req['evidence']:out+='Evidence: '+', '.join('`'+e['block']+'`' for e in req['evidence'])+'; [exact routes](#analysis-only-evidence).\n\n'
 out+='''## Finite acceptance proposals

[Current R2 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/cases-r2.json)
retain all36 original IDs and add SYNC-025. Initial-tempo, initial-visibility,
menu/peer-list, Follow placement/processing, Clock-host tempo changes and MTC
capability histories are explicit. There are27 requirements (25D12/2U),37 cases,
eight named visible documentary proposals and29 null documentary proposals.
All actual expected/comparison values are null/U/unexecuted. Every timing,
audio/signal and U documentary output/comparator is null; refined SYNC-012 is
signal with null documentary outputs because it observes actual processing.
There is no new detector, interruption, restoration/re-enable, clock, wire,
leader-election, numeric tracking, jitter, deadline or constructor-default law.
Compound contexts and all lifecycle/source/arbitration/rate failures stay partial.

'''+spec[spec.index('## Analysis-only evidence'):]
 out=out.replace('26requirements','27requirements').replace('manifest-author-r1.json','manifest-author-r2.json')
 out=out.replace('/synchronization/requirements.json','/synchronization/requirements-r2.json')
 out+='''
The [original R1 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/archive-r1/manifest-author-r1.json)
and all original26/36 catalog bytes remain unchanged. The current
[read-only R2 checker](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/validate-r2.py)
checks source identities, exact deltas, browser IDs and explicit historical pin
resolutions; it establishes no compatibility result.
'''
 (ROOT/'wiki/specs/synchronization-workflows.md').write_text(out);(P/'spec-r2.md').write_text(out)
 research=(P/'research-r1.md').read_text().replace('revision: 1','revision: 2',1)
 research=research.replace('## Review and required evidence','## Historical R1 review and required evidence').replace('[26 requirements]','Historical R1 [26 requirements]',1).replace('Independent semantic review follows the\n[author seal]','The original partial semantic review is bound to the\n[R1 author seal]')
 research+='''
## R2 retained-source audit adoption

The [reviewed source-audit successor](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization-source-audit/manifest-author-r2.json)
and its [focused independent approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synchronization-source-audit-review-final.json)
support nine bounded source/context deltas. [Adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/audit-adoption-r2.json)
links each proposal. New025 retains remaining-peer continuity while a third
participant joins/leaves; no membership protocol, leader election, numerical
phase/audio/jitter tolerance, convergence or interruption deadline follows.

Existing005 clarifies the source's displayed-by-default Link-toggle context,
without an exact-build constructor/reset/migration/prior-preference assumption.
Its case explicitly records initial provenance, menu switches, connected
Audio-enabled peer-list contrast and Configure Link. Existing002 now separates
known first-participant initial tempo from later tempo edits. Existing012 adds
only textual left-Control-Bar placement. Its source law that hidden Follow does
not run is unchanged, while its case explicitly activates and independently
establishes genuine positive interpretation before hiding only Follow with input
unchanged. Active input, visibility, a lit button or generic peer tempo is not
that baseline. The whole compound case has null signal documentary outputs;
no cessation deadline, restored running state or automatic re-enable is assumed.

Existing015 makes qualitative Clock-host tempo-change following explicit, with
an isolated receiving history and null timing/byte results. Existing016 retains
MTC receiver-only/not-host unchanged; its refined case requests independently
admitted capability evidence rather than guessing absent controls or sending
unsupported messages. No MIDI Start/Stop codec, preroll, lag/rate/delay/offset
default, enumerated SMPTE set or detector algorithm is inferred.

[Current requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/requirements-r2.json)
and [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/cases-r2.json)
give27 requirements (25D12/2U) and37 cases (eight visible documentary/29null).
All54 source blocks and raw HTML are unchanged, as are original26/36 catalogs
at their original paths. The original review remains scoped to R1. Every actual
target result/comparator is null/U/unexecuted; actual signal/timing/protocol,
exact12.4.3 Link Audio availability and whole-product completion stay unknown.

[Four explicit historical Sync redirects](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/historical-pin-redirects-r2.json)
resolve only R4 and Sync-audit canonical input records to exact archived R1
spec/research snapshots. They do not rewrite those frozen files, change source
or citation semantics, or redirect Stem/Video inputs. Root handles full cohort
replay and any current crosswalk/shared metadata. Independent owner-R2 review
follows the [new seal](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r2.json).
'''
 (ROOT/'wiki/research/synchronization-workflows.md').write_text(research);(P/'research-r2.md').write_text(research)
if __name__=='__main__':write()
