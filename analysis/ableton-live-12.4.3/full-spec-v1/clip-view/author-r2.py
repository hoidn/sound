#!/usr/bin/env python3
"""Bounded Clip View owner successor. Pure JSON/text derivation; no vendor execution."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
AUDIT=HERE.parent/'clip-view-source-audit'
REL=HERE.relative_to(ROOT).as_posix()
AREL=AUDIT.relative_to(ROOT).as_posix()
def load(p):return json.loads(Path(p).read_text())
def encoded(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def ident(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def build():
 data=load(HERE/'adoption-data-r2.json');blocks=load(AUDIT/'source-blocks.json');bm={b['id']:(i,b) for i,b in enumerate(blocks)}
 def evidence(ids):return [{'catalog':AREL+'/source-blocks.json','json_pointer':'/'+str(bm[b][0]),'block':b,'role':'retained public source role, not target observation'} for b in ids]
 oldreq=load(HERE/'requirements.json');oldcases=load(HERE/'cases.json');reqs=copy.deepcopy(oldreq)
 for r in reqs:
  r['contract']=data['requirement_contract_patches'].get(r['id'],r['contract'])
  r['source_blocks']=list(dict.fromkeys(r['source_blocks']+data['requirement_source_block_additions'].get(r['id'],[])))
 reqs+=copy.deepcopy(data['new_requirements'])
 for r in reqs:
  r['html_lines']=sorted({bm[b][1]['html_line'] for b in r['source_blocks']})
  r['evidence']=evidence(r['source_blocks']);r['complete']=False
 rmap={r['id']:r for r in reqs};cases=copy.deepcopy(oldcases)
 for c in cases:
  c['setup_and_action']=data['case_action_patches'].get(c['id'],c['setup_and_action'])
  c['documentary_expected']=data['case_documentary_patches'].get(c['id'],c['documentary_expected'])
 cases+=copy.deepcopy(data['new_cases'])
 for c in cases:
  c['fixture']='fixtures-r2.json#CV-BASE-R2'
  c['expected']=None;c['comparison']=None;c['target_grade']='U';c['executed']=False;c['complete']=False
  c['source_claim']=' '.join(rmap[x]['contract'] for x in c['requirements'])
  c['evidence']=evidence(c['source_blocks'])
  if c['id'] in {x['id'] for x in data['new_cases']}:
   c['documentary_comparator']='Named visible input/control role only; no numeric, timing, signal, file, process or hidden-state comparison' if c['documentary_expected'] is not None else None
   c['unknown']='All target outcomes U; missing input/capability/positive baseline is U, never a pass. Numeric/signal/timing/file/protocol and complete context outcomes are not inferred.'
 fixtures=copy.deepcopy(load(HERE/'fixtures.json'));fixtures['id']='CV-BASE-R2'
 fixtures['preconditions'] += ['Opening/toggle trials retain known closed/open initial view state and actual eligible focus; a Toggle is not an unconditional always-open command. Every negative/unavailable/malformed/teardown/history trial first requires independently admitted real input/capability and a genuinely productive matched control/action baseline. A selected label/enabled flag alone is insufficient; missing source/output/editor/support remains U.',
 'Follow trials require nonempty audio/MIDI, actual moving playhead crossing zoomed boundary, genuinely confirmed automatic scrolling before an actual editor edit and an independently established paused-Follow relation. Stop alone is eligibility context, not scrolling while stopped; reset each Options/toggle/stop/restart/Arrangement-scrub/clip-scrub branch.',
 'Color creation needs matched preference/version/history (Q031). Group Assign remains Mixing012/MXW012. All file/editor/default/transmission/algorithm effects stay with actual owners; local input roles do not fabricate source fixtures or platform success.']
 groups=load(AUDIT/'proposed-deltas.json');recon=copy.deepcopy(data['audit_reconciliation'])
 for item in recon:
  g=next(g for g in groups if g['id']==item['audit_group'])
  item['audit_proposal']={'catalog':AREL+'/proposed-deltas.json','json_pointer':'/'+str(groups.index(g))}
  item['requirement_refs']=[{'catalog':REL+'/requirements-r2.json','json_pointer':'/'+str(next(i for i,r in enumerate(reqs) if r['id']==rid)),'id':rid} for rid in item['requirements']]
  item['case_refs']=[{'catalog':REL+'/cases-r2.json','json_pointer':'/'+str(next(i for i,c in enumerate(cases) if c['id']==cid)),'id':cid} for cid in item['cases']]
  item['retained_source_blocks']=g['source_blocks'];item['source_evidence']=evidence(g['source_blocks'])
  item['limits']=g['limits'];item['source_filled_is_not_completion']=True
 routed=[]
 for n in [4,8,13,19,21,22,24]:
  g=copy.deepcopy(groups[n-1]);g['role']='Retained external-owner extension/context proposal only; not new normative clauses/cases or execution'
  g['actual_expected']=None;g['actual_comparison']=None;g['target']='U';g['executed']=False;g['complete']=False
  if n==13:g['current_context']='Selected/no-selection Interval distinction checked in pinned MIDI query original HTML588 paragraph2, owned by existing MIDI011; actual-case adoption belongs MIDI successor. Humanize half-grid versus quarter-before/after remains Q053/U. Frozen audit proposal is retained as-of, not silently rewritten.'
  routed.append(g)
 reused=[{'scope':'Group Assign only, existing active-view/member/nonmember case reused; no duplicate Clip View case/law','requirement':{'catalog':HERE.parent.relative_to(ROOT).as_posix()+'/mixing-workflows/requirements.json','json_pointer':'/11','row':load(HERE.parent/'mixing-workflows/requirements.json')[11]},'case':{'catalog':HERE.parent.relative_to(ROOT).as_posix()+'/mixing-workflows/cases.json','json_pointer':'/11','row':load(HERE.parent/'mixing-workflows/cases.json')[11]}}]
 used=list(dict.fromkeys(b for r in reqs for b in r['source_blocks']))
 used=list(dict.fromkeys(used+[b for c in cases for b in c['source_blocks']]+[b for g in groups for b in g['source_blocks']]))
 source=load(HERE/'source.json');contexts=[]
 for bid in used:
  ix,b=bm[bid];contexts.append({'block':bid,'catalog':AREL+'/source-blocks.json','json_pointer':'/'+str(ix),'quote':b['text'],'kind':b['kind'],'source':source,'literal_element_id':b['attributes'].get('id'),'heading_context':b['heading_context'],'html_line':b['html_line'],'html_column':b['html_column'],'raw_start':b['raw_start'],'raw_end':b['raw_end'],'offset_unit':'Unicode characters in decoded retained HTML','raw_html_sha256':hashlib.sha256(b['raw_html'].encode()).hexdigest(),'requirements':[r['id'] for r in reqs if bid in r['source_blocks']],'cases':[c['id'] for c in cases if bid in c['source_blocks']],'audit_groups':[g['id'] for g in groups if bid in g['source_blocks']]})
 def field_delta(old,new):
  return [{'id':a['id'],'fields':[{'field':k,'before_present':k in a,'after_present':k in b,'before_sha256':hashlib.sha256(encoded(a[k])).hexdigest() if k in a else None,'after_sha256':hashlib.sha256(encoded(b[k])).hexdigest() if k in b else None} for k in sorted(set(a)|set(b)) if (k in a)!=(k in b) or a.get(k)!=b.get(k)]} for a,b in zip(old,new)]
 delta={'role':'Exact semantic edits plus every retained-record top-level field identity delta; original and current catalogs supply full values','retained_requirements':54,'retained_cases':62,'added_requirements':1,'added_cases':30,'requirement_contract_changes':[{'id':a['id'],'before':a['contract'],'after':b['contract']} for a,b in zip(oldreq,reqs) if a['contract']!=b['contract']],
 'case_action_changes':[{'id':a['id'],'before':a['setup_and_action'],'after':b['setup_and_action']} for a,b in zip(oldcases,cases) if a['setup_and_action']!=b['setup_and_action']],
 'case_documentary_changes':[{'id':a['id'],'before':a['documentary_expected'],'after':b['documentary_expected']} for a,b in zip(oldcases,cases) if a['documentary_expected']!=b['documentary_expected']],
 'requirement_field_changes':field_delta(oldreq,reqs),'case_field_changes':field_delta(oldcases,cases),'preservation':'preservation-r1-before-r2.json','all_original_runtime_oracles_unchanged_null':True,'new_requirement_ids':[r['id'] for r in reqs[54:]],'new_case_ids':[c['id'] for c in cases[62:]],'schema_note':'Adds exact block pointers/source_claim/complete:false and strengthened fixture reference. Public source prose is not an actual result. Existing pending text inside original files remains historical as-of authorfreeze.'}
 stats={'requirements':len(reqs),'D12':sum(r['provenance']=='D12' for r in reqs),'U':sum(r['provenance']=='U' for r in reqs),'cases':len(cases),'new_cases':30,'new_requirements':1,'new_visible_documentary_cases':sum(c['documentary_expected'] is not None for c in cases[62:]),'new_null_documentary_cases':sum(c['documentary_expected'] is None for c in cases[62:]),'actual_nonnull':0,'executed':0,'target':'U','complete':0,'audit_groups':len(recon),'source_blocks_used':len(contexts),'full_retained_source_blocks_read':180}
 return {'requirements-r2.json':encoded(reqs),'cases-r2.json':encoded(cases),'fixtures-r2.json':encoded(fixtures),'reconciliation-r2.json':encoded(recon),'routed-proposals-r2.json':encoded(routed),'reused-external-cases-r2.json':encoded(reused),'source-context-r2.json':encoded(contexts),'delta-r2.json':encoded(delta),'summary-r2.json':encoded(stats),'spec-r2.md':spec(reqs,cases,stats).encode(),'research-r2.md':research(stats).encode()}

def spec(reqs,cases,stats):
 text='''---
id: SPEC-CLIP-VIEW-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3; documentary Version12 applicability U
---

# Shared Clip View workflows and audio clip properties

## Scope and authority

This partial successor reconciles all24 groups from the independently reviewed
retained-source audit. It adds bounded local input/control gestures and explicit
prerequisites; no source topic or target feature is complete. Audit approval is
not approval of this owner successor, runtime behavior or an implementation
handoff. Separate independent owner review remains pending as of author freeze.

Shared panels, editor selection, local region/sample UI and audio command entries
remain here. [Session](session-view-workflows.md) owns statuses/launch selection;
[launch](session-launch-workflows.md), [finite launch](clip-launch.md) and
[playback](playback-core.md) retain scheduling/engine laws. [Warp workflows](warping-workflows.md)
and [native markers](warp-markers.md) own their respective interactive and finite
subsets. [MIDI editing](midi-editing-tools.md), [MPE](mpe-workflows.md),
[grooves](groove-workflows.md), [automation](automation-workflows.md),
[media defaults](media-file-workflows.md), [project/media](project-media-workflows.md),
[Arrangement](arrangement-editing.md), [settings](settings-learning-workflows.md),
[Browser](browser-content-workflows.md), [mixing](mixing-workflows.md),
[remote mapping](remote-control-workflows.md) and [keyboard](keyboard-navigation.md)
retain underlying effects. In particular Group Assign uses existing Mixing012/
MXW012; no duplicate group-color case or new color law is added here.

D12 means retained current Version12 documentation, not exact12.4.3 evidence.
Every actual `expected`/`comparison` is null, target U and unexecuted. Original
source/cache/quality/CPU/default prose never mandates private architecture or
proves timing, numeric, signal, file, process, protocol or random outcomes. New
sensitive cases also keep documentary outcomes null; `source_claim` is prose
only. Legacy documentary fields retain only their stated bounded source roles.
No application, original function, candidate, reader, hardware, editor, media,
network/account or configuration operation was executed. Images/destinations
remain uninspected. [Research](../research/clip-view-workflows.md) gives provenance.

## Preconditions and unresolved contexts

The [future owned-input fixture](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/fixtures-r2.json)
requires independently validated A/B/C media or editable MIDI M, matched focus,
platform, source/region/loop/Warp/grid/meter, quantization/UpdateRate and output
state. Every unavailable/negative trial begins from a genuinely productive
matched input/control/output baseline. Missing input/capability is U, not a pass.
No media fixture/reference render was fabricated.

Follow needs genuine automatic scrolling across the visible boundary before a
real edit and a separately established pause. Options/toggle, stop alone/restart,
Arrangement scrub and clip scrub use separate reset histories. Stop alone is
resumption/eligibility context; it does not require moving scrolling while stopped.

[Q-031](../questions.md#q-031-new-clip-color-preference-context) retains color preference/version/history uncertainty.
[Q-053](../questions.md#q-053-midi-utility-gesture-and-humanize-source-contexts) retains Humanize context uncertainty.
The exact detailed MIDI Intervals paragraph distinguishes selected-slider
addition from no-selection slider-setting/button application; existing MIDI011
owns it, with actual future actions routed to that owner. This is source context,
not a new Clip View note law or full Q053 resolution. Half-grid versus quarter-
before/after Humanize is not adopted as equivalence or RNG/displacement policy.

## Requirements

Each bare first-cell ID is current and browser-discoverable. Source/context
blocks resolve to [exact quotes and HTML locators](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/source-context-r2.json).
Numeric representations do not establish stored-time/PCM/note or control laws.

| Requirement | Documentary contract and limits | Basis | Source blocks |
| --- | --- | --- | --- |
'''
 for r in reqs:text+=f"| {r['id']} | {r['contract']} | {r['provenance']}; target U | {', '.join(r['source_blocks']) or 'No supported outcome'} |\n"
 text+='''
## Finite future actions

The [92-case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/cases-r2.json)
preserves all62 existing IDs and their true bounded subsets. It strengthens
CV031's Follow baseline and scopes CV005/CV031 documentary descriptions;30
cases add actual local gestures. CV027's known Gain values are not every slider
gesture; CV045 already genuinely changes Gain. Existing opening/window/editor,
repeated zoom, scrub preference, all crop branches/replacement routes and both
mixed-value extrema remain represented subsets, not missing or complete topics.

| Case | Requirements | Kind | Target |
| --- | --- | --- | --- |
'''
 for c in cases:text+=f"| {c['id']} | {', '.join(c['requirements'])} | {c['kind']} | U; not executed |\n"
 text+='''
## Preservation, routes and gaps

[Exact deltas](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/delta-r2.json)
retain54 requirements/62 cases, add one audio Duplicate Loop entry clause and30
cases, and record six contract refinements, one action refinement and two bounded
documentary descriptions. All17 R1 files remain exact in place, including its
seal/freeze/checker/reports/snapshots. Exact pre-edit canonical pages are retained;
old pending-review prose remains historical as-of its author freeze.

The [24-group reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/reconciliation-r2.json)
separates local adoption, existing predicates and external-owner extensions.
[Routed proposals](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/routed-proposals-r2.json)
are not new normative IDs/cases, and do not close Groove/Media/MIDI/shared-reference
gaps. Historical consumer identities are enumerated without automatic adapter or
replay obligations; concrete dependency/check/release gates still require narrow
replay. Full defaults/history/build/platform/reader, malformed/undo/persistence,
source-loss/cancel/teardown, numeric/timing/file/audio/API/protocol outcomes remain U.
'''
 return text

def research(stats):
 return '''---
id: RES-CLIP-VIEW-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Shared Clip View and audio property evidence

The [partial owner successor](../specs/clip-view-workflows.md) reconciles all24
approved audit proposal groups against the actual54 prior contracts and62
actions. All180 retained chapter blocks (137paragraphs,6list items,37headings)
were read with qualifiers for this adoption; actual old actions and fixture were
read, not inferred from labels. The audit approval is partial source analysis;
this owner successor awaits separate independent semantic review as of freeze.
It has55 requirements (47D12/8U),92 future cases and zero completed outcomes.

The [original official Version12 source](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/source.json)
remains306606bytes, SHA30f156e6d83c8f4caf3fe9dcf55bb2b764dc42ed8cbd3847863a53747851bd80,
captured2026-10-19T21:25:35.853607+00:00. No exact12.4.3 publication identity is
supplied; target behavior remains U. Source quotes and raw decoded HTML spans
retain literal element IDs and heading ancestry separately. Images and linked
destinations were not inspected, nor was a source parser/vendor example executed.

R2 preserves true opening/window/editor, repeatedZ/X, scrub preference, three
ordinary-crop branches, selection crop, all replacement routes and both extrema
subsets. New cases perform distinct metadata/palette, automatic/title panels,
bank-selector context, Reverse readiness, explicit Edit click, knob/semitone/cents,
zoom/overview, productive Follow, marker/brace, ordinary crop and interior mixed-
value gestures. Source numeric/timing/file/signal/reader/configuration descriptions
are prose only in new sensitive cases. Every actual expectation/comparison is
null, target U, not executed. Missing positive baseline is never a negative pass.

Group Assign active-view/member/nonmember behavior reuses Mixing012/MXW012;
local title/palette/creation histories do not duplicate that case or law.
CV027 establishes known Gain values/split handles and named Pitch/cents edits;
it does not prove every Gain gesture. CV045 already changes Gain for timing;
the new pitch trials distinguish knob, semitone field and cents field, without a
numeric/audio law or additional Gain trial.
Follow must genuinely scroll automatically before a real edit and independently
pause, with separate Options/toggle, stop-alone/restart and Arrangement/clip scrub
histories. No moving scrolling while stopped, restoration or deadline is implied.

[Q-031](../questions.md#q-031-new-clip-color-preference-context) retains source inheritance versus Clip Color preference/version/history.
[Q-053](../questions.md#q-053-midi-utility-gesture-and-humanize-source-contexts) remains open for Humanize half-grid versus quarter-grid-before/after.
The [pinned finite MIDI source query](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-utility-source-context-query.json) is original-text context, not independent
review or runtime evidence. Its five full Intervals/Humanize records and exact
MIDI HTML588 paragraph2 decodedchars84834–85289 were independently checked here.
Selected Interval Size adjustment immediately adds/selects; with no notes selected
the slider only sets interval and Add Interval applies to all existing notes.
Existing MIDI011 already owns these source roles; its original MED011 only did
Fit to Scale. Actual branch-case adoption belongs the MIDI owner, not this page.
No all-button-with-selection behavior, zero-time deadline, repeat accumulation,
Humanize span equivalence or RNG law was inferred. MIDI capture is date-only;
query UTC is not capture UTC. Frozen audit questions remain unchanged as-of.

Groove chooser/shared-pool HotSwap and positive-velocity Commit envelope effects,
Media saved-default/reimport/ASD behavior, MIDI crop/duplicate and shared-instrument
File Manager effects remain their owners and explicit routed extension proposals.
Panel/control availability does not close those computations or file contracts.
All17 original R1 files remain exact; before canonicals, field/semantic deltas,
immutable inputs and current snapshots are retained. Historical consumer pins
are enumerated as-of; no automatic replay adapter or blanket green old-checker
claim was added. Root owns shared routes, Qs, indexes, coverage and log updates.
No original function/application/UI, editor, hardware, media, network/account,
configuration, reader or candidate operation ran. No handoff was published.
'''

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();assert a.write!=a.check
 if a.write and (HERE/'manifest-author-r2.json').exists():raise SystemExit('refusing writes: R2 sealed')
 out=build()
 for name,raw in out.items():
  if a.write:(HERE/name).write_bytes(raw)
  else:assert (HERE/name).read_bytes()==raw,name
 for path,snapshot in [('wiki/specs/clip-view-workflows.md','spec-r2.md'),('wiki/research/clip-view-workflows.md','research-r2.md')]:
  if a.write:(ROOT/path).write_bytes(out[snapshot])
  else:assert (ROOT/path).read_bytes()==out[snapshot],path
 print(json.dumps({'mode':'write' if a.write else 'readonly','summary':json.loads(out['summary-r2.json'])}))
if __name__=='__main__':main()
