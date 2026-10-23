"""Initial bounded Resync documentary successor; never original/runtime execution."""
from pathlib import Path
from copy import deepcopy
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
load=lambda q:json.loads(q.read_text())
def pin(q):
 raw=q.read_bytes();return dict(bytes=len(raw),sha256=sha256(raw).hexdigest())
def write():
 assert sys.argv[1:]==['--write'] and not (P/'manifest-author-r3.json').exists(),'Initial unsealed authoring only'
 prior=load(P/'manifest-author-r2.json');assert pin(P/'manifest-author-r2.json')['sha256']=='7ebf0944815b79373d660c74ba9a3dfbae60668d079cfa3fdeec9d00c1cb5e77'
 oldnames=set(prior['files'])|{'manifest-author-r2.json','validation-author-r2.json','freeze-author-r2.json'};assert len(oldnames)==48
 old={n:pin(P/n) for n in sorted(oldnames)}
 for n,r in prior['files'].items():assert old[n]==r
 for r in prior['canonical_snapshots']:assert pin(ROOT/r['canonical'])==pin(P/r['snapshot'])=={k:r[k] for k in ['bytes','sha256']}
 comp=B/'resync-source-reconciliation';review=B/'reviews/resync-source-reconciliation-review.json'
 assert pin(comp/'manifest.json')['sha256']=='73c27ff10d9ce3999ac93f01e618e770bbe532f86f8fb2c065c14699a6fe97e5'
 assert pin(review)['sha256']=='84b1b4187b9159118e68239689ded2a0748efc56fdbb22dcfe96e21748c804ff'
 assert load(review)['findings']==[]
 targets={r['canonical']:r for r in prior['canonical_snapshots']};consumers=[]
 def walk(v,ptr=''):
  if isinstance(v,dict):
   for k,x in v.items():
    if isinstance(x,str) and x in targets and v.get('sha256')==targets[x]['sha256']:consumers.append(dict(pointer=ptr,path_key=k,record=deepcopy(v),kind='as-of snapshot context, no live redirect' if k=='source_path' else 'preserved R2 self-history pin'))
    walk(x,ptr+'/'+k.replace('~','~0').replace('/','~1'))
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,ptr+'/'+str(i))
 findings=[]
 for q in sorted(B.rglob('*.json')):
  try:d=load(q)
  except (UnicodeError,json.JSONDecodeError):continue
  consumers=[];walk(d)
  for c in consumers:findings.append(dict(consumer=str(q.relative_to(ROOT)),consumer_identity_as_of=pin(q),**c))
 assert len(findings)==5 and sum(c['kind']=='preserved R2 self-history pin' for c in findings)==4
 changes={}
 changes['old-files-r3.json']=dict(status='All48 original R2-tree files retained in place, no archive copy',files=old)
 changes['canonical-consumers-r3.json']=dict(scope='Initial as-of full-spec-v1 JSON scan for exact canonical-path plus current R2 SHA in the same record. Not repository-wide proof or a continuing live dependency sweep.',current_R2_snapshots=prior['canonical_snapshots'],matching_records=findings,resolution='Four self-history pin rows continue to describe exact existing R2 snapshots; old validate-r2.py expects live R2 canonicals and is historical after R3. Warping source-audit row explicitly reads its own as-of snapshot and needs no redirect. No consumer/tool is edited or new resolver added. Four prior R1 redirects remain exact and root owns combined replay.')
 route=load(B/'routing-monitoring/manual-routing-blocks.json');idx={x['locator']:(i,x) for i,x in enumerate(route)}
 def ev(n):
  i,x=idx['routing:B%03d'%n];assert x['heading_context'][-1]['anchor']=='sync'
  return dict(block=x['locator'],anchor='sync',html_line=x['html_line'])
 r026=dict(id='REQ-SYNC-WORKFLOW-026',title='Hardware Resync configuration and command',contract='For a MIDI output with Sync enabled, the triangle next to the port name opens additional options. Hardware Resync selects a resync behavior when Resync External Hardware is enabled; when enabled, the Resync External Hardware button appears in the Control Bar and can be used to send resync messages to external gear. Drift during playback is a documented useful context, not an exclusive eligibility condition or a correction guarantee. The shared button versus per-port fanout and exact option-enable location beyond the named context remain unknown.',strength='D12',target_applicability='U',evidence=[ev(38),ev(41),ev(42)])
 r027=dict(id='REQ-SYNC-WORKFLOW-027',title='Hardware Resync symbolic mode roles',contract='The manual describes Stop and Start as the default resync behavior: a MIDI Clock Stop event followed by a MIDI Clock Start event. Start Only sends just the MIDI Clock Start resync event; Don’t Resync sends no resync messages. These symbolic source roles supply no byte encoding, total event count, spacing, timestamp, drift/phase correction, convergence or successful-device guarantee. Documentary default is not an exact-build constructor/reset/migration observation. Don’t Resync does not establish suppression of ordinary MIDI Clock traffic; per-output/all-output fanout and interactions with tempo, preroll, transport, Clock Type or Sync Delay remain unknown.',strength='D12',target_applicability='U',evidence=[ev(43)])
 reqs=deepcopy(load(P/'requirements-r2.json'));cases=deepcopy(load(P/'cases-r2.json'));assert len(reqs)==27 and len(cases)==37
 reqs += [r026,r027]
 guard='Independently admitted exact-build feature and compatible owned receiver; genuine usable outgoing MIDI Clock, receiver synchronization and identifiable nonzero active outputs before any negative/no-effect trial. Port activity, a lit button, absent gear or silence alone is insufficient. Missing feature, eligible port or successful positive baseline remains U, never a passing negative.'
 def case(cid,r,kind,action,contexts):
  return dict(id=cid,requirements=[r['id']],kind=kind,fixture='fixtures-r3.json#SYNC-RESYNC-OWNED',setup_and_action=action,source_claim=r['contract'],documentary_expected='Named offered output-option, selector and enabled Control Bar command roles only.' if kind=='control' else None,documentary_comparator='Visible offered controls/selections only; no traffic, message, timing, drift, device or fanout outcome.' if kind=='control' else None,expected=None,comparison=None,target_grade='U',executed=False,evidence=r['evidence'],finite_contexts=contexts,positive_guard=guard)
 cases.append(case('SYNC-026',r026,'control','In an independently admitted future build/platform and productive output-Clock/receiver context, explicitly enable Sync for the chosen output, expand its port-name triangle and inspect offered Hardware Resync choices. In a separate declared history explicitly enable Resync External Hardware, inspect its Control Bar button and invoke the offered command while retaining visible control state. No exact enable-option picker path, layout, shortcut, disabled/hidden-off presentation, port fanout or successful timing result is inferred. Mode traffic observations belong to separate null-oracle proposals.',['Sync-enabled output and port-name triangle','offered Hardware Resync selector','explicit Resync External Hardware enable then Control Bar command']))
 modes=[('STOP-START','Stop and Start','symbolic Stop followed by Start source role'),('START-ONLY','Start Only','symbolic Start-only resync source role'),('DONT-RESYNC','Don’t Resync','no resync-message source role; ordinary clock suppression not inferred')]
 for suffix,label,role in modes:
  cases.append(case('SYNC-027-'+suffix,r027,'protocol/timing','Future owned evidence only: establish genuine usable outgoing Clock from Live and receiver synchronization with separately identifiable nonzero outputs. For the documented use context admit an independently established drifting receiver during playback, without inventing a drift amount or inducing unsafe hardware changes. In its own reset history explicitly select '+label+' for the admitted output context, enable the actually offered Resync External Hardware option and invoke the Control Bar command. Retain control, usable traffic and receiver/output observations separately. '+('For this no-resync history, first retain a genuine known-positive resync-capable history with compatible receiver; absent gear, muted output, failed Clock or failed resync baseline cannot prove suppression. Ordinary Clock remains a separate observation, with no inferred suppression. ' if suffix=='DONT-RESYNC' else '')+'No symbolic source event role is a concrete byte/event-count/scheduling, phase/drift correction, success or fanout oracle. Hardware capability absence and failed positive baseline remain U. Drift is a useful context, not an exclusive command gate.',[label,role,'known usable Clock/receiver and nonzero output baseline','source-described drift during playback context; actual result U']))
 u=dict(id='SYNC-U-RESYNC-LIFECYCLE',requirements=['REQ-SYNC-WORKFLOW-U-LIFECYCLE','REQ-SYNC-WORKFLOW-U-PROTOCOL'],kind='boundary/lifecycle',fixture='fixtures-r3.json#SYNC-RESYNC-OWNED',setup_and_action='Future separate owned histories declare an independently valid productive Resync/Clock/receiver baseline before changing one context: output Sync off, feature enable off, port loss/reconnect, incompatible/unavailable receiver, multiple outputs, stopped/running transport, preroll/count-in, tempo change, Song/Pattern mode, Sync Delay, repeated command, cancel/undo, save/reopen, sample-rate change or teardown. Retain actual controls, traffic and receiver observations as available without constructing bytes or inducing resource/hardware failures. No listed outcome, restoration, fanout, ordinary-Clock suppression or numeric correction law is supplied.',source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,evidence=[],finite_contexts=['output Sync off','feature enable off','port loss/reconnect','unavailable/incompatible receiver','multiple outputs/shared button fanout','stopped/running transport','preroll/count-in','tempo changes','Song/Pattern','Sync Delay','repeat','cancel/undo','save/reopen','rate change','teardown'],positive_guard=guard)
 cases.append(u);changes['requirements-r3.json']=reqs;changes['cases-r3.json']=cases
 changes['fixtures-r3.json']=dict(id='SYNC-RESYNC-OWNED',status='future owned prerequisites only; no devices/traffic/assets/results supplied',positive_guard=guard,setup='Use separately owned reset histories, independently known compatible usable output port and receiver, declared tempo/transport/source direction/Sync/Clock Type/Sync Delay/Link/Follower state. Establish active nonmuted nonzero identifiable Live/receiver output paths and genuine synchronization before drift/no-resync/disabled comparisons. Record exact build/platform/device identity and feature availability. No present runtime operation authorized or performed.',no_inference='The per-port selector and shared Control Bar button do not establish fanout. No ordinary-clock suppression, timer/clock/drift algorithm, successful correction, default factory state or preroll law follows.')
 changes['source-r3.json']=dict(status='reuse only; all full sources remain at pinned original paths',primary_R2_source=load(P/'source.json'),additional_routing_source=load(comp/'source-context.json')['routing'],source_context=load(comp/'source-context.json'),new_evidence=[dict(**ev(n),direct_paragraph_anchor=idx['routing:B%03d'%n][1]['anchor'],heading_context=idx['routing:B%03d'%n][1]['heading_context'],block_catalog=str((B/'routing-monitoring/manual-routing-blocks.json').relative_to(ROOT)),block_pointer='/'+str(idx['routing:B%03d'%n][0]),text=idx['routing:B%03d'%n][1]['text']) for n in [38,41,42,43]],limits='Current Version12 publication only, exact12.4.3 availability U; images uninspected. Routing B039 outgoing Sync Delay and B040 Song/Pattern are adjacent distinct roles, not new adopted laws; existing Sync023 input-relative delay remains distinct. No primal protocol/phase/drift correction result.')
 changes['delta-r3.json']=dict(prior_manifest=dict(path=str((P/'manifest-author-r2.json').relative_to(ROOT)),**pin(P/'manifest-author-r2.json')),source_reconciliation=dict(path=str((comp/'manifest.json').relative_to(ROOT)),**pin(comp/'manifest.json')),source_review=dict(path=str(review.relative_to(ROOT)),**pin(review)),old_requirements_verbatim=27,old_cases_verbatim=37,new_requirements=[r026['id'],r027['id']],new_cases=[x['id'] for x in cases[37:]],field_deltas=[dict(old_file='requirements-r2.json',new_file='requirements-r3.json',pointer='/'+str(i),operation='add',old=None,new=x) for i,x in enumerate(reqs[27:],27)]+[dict(old_file='cases-r2.json',new_file='cases-r3.json',pointer='/'+str(i),operation='add',old=None,new=x) for i,x in enumerate(cases[37:],37)],adopted_scope='Only two reviewed source roles; three explicitly chosen mode proposals and a source-silent lifecycle case. No other source/category closure.',no_old_record_or_oracle_changes=True)
 paths={P/n for n in oldnames}|{comp/'manifest.json'}|{comp/n for n in load(comp/'manifest.json')['files']}|{ROOT/x['path'] for x in load(comp/'input-pins.json')}|{review,B/'reviews/synchronization-owner-r2-review.json',ROOT/'tools/spec_browser.py',ROOT/load(P/'dependencies.json')[0]['path']}
 changes['inputs-r3.json']=[dict(path=str(q.relative_to(ROOT)),**pin(q)) for q in sorted(paths)]
 for n,v in changes.items():
  assert not (P/n).exists(),n
  (P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
 spec=(P/'spec-r2.md').read_text().replace('revision: 2\n','revision: 3\n',1)
 intro='''R3 adds only two reviewed Hardware Resync roles, preserving every R2 clause and
case record. [Resync source reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/resync-source-reconciliation/README.md)
and [independent source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/resync-source-reconciliation-review.json)
retain exact output-Sync contexts and symbolic mode names/order. They supply no
byte codec, total event count, schedule, correction algorithm or actual hardware
result. A shared Control Bar button does not establish per-port/all-port fanout;
Don’t Resync concerns resync messages, not ordinary Clock suppression.\n\n'''
 spec=spec.replace('## Requirements\n',intro+'## Requirements\n',1)
 added=''
 for r in [r026,r027]:added+=f"### {r['id']} — {r['title']}\n\n**D12/target-U.** {r['contract']}\n\nEvidence: "+', '.join('`'+e['block']+'`' for e in r['evidence'])+'; [additional source](#resync-source-and-preserved-history).\n\n'
 spec=spec.replace('### REQ-SYNC-WORKFLOW-U-PROTOCOL',added+'### REQ-SYNC-WORKFLOW-U-PROTOCOL',1)
 a=spec.index('## Finite acceptance proposals');z=spec.index('## Analysis-only evidence',a)
 spec=spec[:a]+'''## Finite acceptance proposals

[Current R3 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/requirements-r3.json)
and [current R3 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/cases-r3.json)
retain all27 R2 requirements and37 R2 case records verbatim, adding two clauses,
one visible-control proposal, three separate accepted-mode proposals and one
explicit U lifecycle proposal. There are29 requirements (27D12/2U),42 cases,
nine visible documentary proposals and33 null documentary proposals. All actual
expected/comparison fields remain null/U/unexecuted. Every Resync message/timing,
signal, numeric and operational outcome/comparator is null. Mode prose is only
source_claim; no encoded events, count, spacing, phase or successful correction
oracle follows. Existing running-Follower-before-hide and third-peer continuity
positive guards remain unchanged. Future no-resync/disabled histories require
separately genuine usable Clock/receiver synchronization and identifiable
nonzero unmuted output, including a known positive resync-capable baseline for
Don’t Resync. Missing feature, receiver or failed baseline stays U.

'''+spec[z:]
 spec+='''
## Resync source and preserved history

The additional official [Routing Sync subsection](https://www.ableton.com/en/live-manual/12/routing-and-i-o/#sync)
is retained at its original [full HTML path](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-routing-and-i-o-2026-10-19.html).
Its exact capture identity, direct paragraph anchors (null), actual heading
ancestry, source catalogs and locators are in [R3 sources](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/source-r3.json).
No recapture occurred. Preroll, tempo/transport transitions, Sync Delay/Clock Type
interactions, device compatibility and lifecycle outcomes remain unknown.
The published default is documentary context, not target constructor/reset proof.

All48 existing R2-tree files remain exact in place, including old catalogs,
snapshots, failed-preflight evidence, seal and validation/freeze records; no full
archive was added. [Canonical consumer inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/canonical-consumers-r3.json)
discloses four R2 self-history rows and an unaffected as-of Warp context. Older
checkers expecting live R2 canonicals are historical; exact spec-r2/research-r2
snapshots remain available. Existing four R1 routes remain unchanged. Root owns
combined historical replay/shared integration; consumers/tools were not edited.
[R3 delta](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/delta-r3.json),
[read-only checker](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/validate-r3.py)
and [R3 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r3.json)
bind this partial successor; independent review remains pending.
'''
 research=(P/'research-r2.md').read_text().replace('revision: 2\n','revision: 3\n',1)
 research=research.replace('## R2 retained-source audit adoption','## Historical R2 retained-source audit adoption',1)
 research+='''
## R3 bounded Hardware Resync adoption

[Reviewed Resync reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/resync-source-reconciliation/README.md)
and its [independent source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/resync-source-reconciliation-review.json)
read the complete retained Routing Sync subsection, adjacent context and the
SET-B053 referral. This is not a complete Routing source/behavior audit. R3 adopts
only the output-Sync triangle/Hardware Resync/enabled Control Bar command role
and the three symbolic mode roles. Stop then Start is published symbolic order;
Start Only and Don’t Resync do not supply bytes, total event counts, spacing,
timestamps, phase/drift correction, convergence, interruption deadline or measured
success. The source’s device recommendations are not a compatibility matrix.

The selector is in output-port context while the command is a shared Control Bar
button. Per-output versus all-output fanout remains U. Don’t Resync describes
resync-message absence only; suppression of ordinary Clock traffic is not inferred.
Drift during playback is a useful documented context, not an exclusive eligibility
gate. Default Stop and Start is documentary only, not exact-build factory/reset/
migration proof. Source text does not establish the exact option-enable path
beyond its named context; image glyphs were not inspected. Preroll/count-in,
stopped transport, tempo changes, Song/Pattern, outgoing/input Sync Delay and
lifecycle interactions stay separate unknowns. No algorithms or results follow
from the Resync label. Existing Clock-host tempo following is unchanged.

[Sources R3](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/source-r3.json)
retain original Routing URL/captureUTC/286397bytes/SHA-256
`1a9c9c842c7a2d04b59794ee12d959f7fad15e3b67f41622109ea14e06e4b9b9`
and actual h4 §17.3.1.2 #sync ancestry; paragraph direct anchors remain null.
The complete source is reused at the original capture path. Current Version12
publication is not exact12.4.3 availability or observed target behavior.

[Requirements R3](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/requirements-r3.json)
retain27 old clause records verbatim plus two (29total/27D12/2U).
[Cases R3](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/cases-r3.json)
retain37 old records verbatim plus five (42total/nine visible documentary/33null).
All actual outcomes remain null/U/unexecuted; new protocol/timing and lifecycle
documentary oracles are null. Future owned independently eligible productive
Clock/receiver and identifiable nonzero unmuted output precede negative/no-effect
histories; a positive resync-capable baseline is additionally required for
Don’t Resync. No traffic, gear or assets were supplied or exercised.

[All48 prior file pins](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/old-files-r3.json)
remain exact in place; original archives/seals/checkers/snapshots and failed
preflight evidence are unchanged. No duplicate full archive is added. The
[as-of consumer inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/canonical-consumers-r3.json)
preserves exact R2 canonical bytes through existing R2 snapshots; four own
manifest/preflight rows and Warp’s already copied as-of context need no consumer
rewrite. Historical checker expectations are disclosed rather than graded
against new pages. Root owns shared integration and full historical replay.
[R3 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r3.json)
awaits independent owner review. No original/helper/runtime, hardware, network,
installation, source recapture or candidate operation occurred; zero topics close.
'''
 for n,text,target in [('spec-r3.md',spec,ROOT/'wiki/specs/synchronization-workflows.md'),('research-r3.md',research,ROOT/'wiki/research/synchronization-workflows.md')]:
  assert not (P/n).exists();(P/n).write_text(text);target.write_text(text)
if __name__=='__main__':write()
