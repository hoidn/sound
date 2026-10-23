#!/usr/bin/env python3
"""Bounded Keyboard R5 author derivation; no vendor code or runtime. --write refuses after seal."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
AUDIT = HERE.parent / 'keyboard-navigation-source-audit'
REL = HERE.relative_to(ROOT).as_posix()
AREL = AUDIT.relative_to(ROOT).as_posix()

def read(path):
    return json.loads(Path(path).read_text())

def encoded(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()

def identity(path):
    raw = Path(path).read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

OLD_CASE_BLOCKS = [
 ['KN1:B002','KN1:B003','KN1:B004','KN1:B005','KN1:B006','KN1:B007'],
 ['KN1:B013','KN1:B014','KN1:B015'], ['KN1:B019'], ['KN1:B021'], ['KN1:B017','KN1:B018','KN1:B059'],
 ['KN1:B022'], ['KN1:B022'], ['KN1:B024','KN1:B025'], ['KN1:B026'],
 ['KN1:B027'], ['KN1:B028'], ['KN1:B029'], ['KN1:B031','KN1:B032','KN1:B034'],
 ['KN1:B047','KN1:B048','KN1:B051','KN1:B061','KN1:B081','KN1:B110','KN1:B121','KN1:B129','KN1:B132'],
 ['KN1:B050'], ['KN1:B053','KN1:B054','KN1:B055','KN1:B057','KN1:B058','KN1:B059'], ['KN1:B060'],
 ['KN1:B065','KN1:B066','KN1:B068','KN1:B070'], ['KN1:B077'], ['KN1:B077'],
 ['KN1:B085'], ['KN1:B084','KN1:B085','KN2:B019'],
 ['KN1:B112','KN1:B119'],
 ['KN1:B123','KN1:B124','KN1:B125','KN1:B126'], ['KN1:B125','KN1:B126','KN1:B128'],
 ['KN1:B131'], ['KN1:B132','KN1:B133'], ['KN1:B138','KN1:B139','KN1:B140'], ['KN1:B140'],
 ['KN1:B148'], ['KN1:B148'], ['KN1:B145','KN1:B149'], ['KN1:B151','KN1:B152'],
 # Inventory and U cases retain only related context, never invented direct evidence.
 ['KN2:B037','KN2:B081','KN2:B110','KN2:B336','KN2:B350','KN2:B351'],
 ['KN1:B045'], [], [], ['KN2:B351'], ['KN1:B002'], [], [], []
]

def build():
    data = read(HERE/'adoption-data-r5.json')
    blocks = read(AUDIT/'source-blocks.json')
    source_meta = read(HERE/'sources.json')
    bmap = {b['id']: (i,b) for i,b in enumerate(blocks)}
    def evidence(ids):
        return [{'catalog': AREL+'/source-blocks.json', 'json_pointer': '/'+str(bmap[x][0]),
                 'block': x, 'role': 'source declaration/context; not target execution'} for x in ids]
    def anchors(ids):
        return list(dict.fromkeys(h['anchor'] for x in ids for h in bmap[x][1]['heading_context'] if h.get('anchor')))
    reqs = copy.deepcopy(read(HERE/'requirements.json'))
    for r in reqs:
        r['body'] = data['requirement_body_patches'].get(r['id'],r['body'])
        r['source_blocks'] = data['old_requirement_source_blocks'][r['id']]
    reqs += copy.deepcopy(data['new_requirements'])
    for r in reqs:
        r['exact_target'] = 'U'
        r['execution'] = 'not-run'
        r['complete'] = False
        r['source_anchors'] = list(dict.fromkeys(r.get('source_anchors',[])+anchors(r['source_blocks'])))
        r['evidence'] = evidence(r['source_blocks'])
        r['source_relation'] = 'Documentary role only' if r['basis']=='D12' else 'Unresolved; listed sources are context, not evidence of a target outcome'
    rmap = {r['id']:r for r in reqs}
    cases = copy.deepcopy(read(HERE/'cases.json'))
    for i,c in enumerate(cases):
        c['action'] = data['old_case_action_patches'].get(c['id'],c['action'])
        c['source_blocks'] = OLD_CASE_BLOCKS[i]
    cases += copy.deepcopy(data['new_cases'])
    for c in cases:
        c['basis'] = rmap[c['requirement']]['basis']
        c['exact_target'] = 'U'
        c['execution'] = 'not-run'
        c['actual_expected'] = None
        c['actual_comparison'] = None
        c['complete'] = False
        c['source_claim'] = rmap[c['requirement']]['body']
        c['source_anchors'] = list(dict.fromkeys(c.get('source_anchors',[])+anchors(c['source_blocks'])))
        c['evidence'] = evidence(c['source_blocks'])
        c['source_relation'] = 'Documentary input/control role only' if c['basis']=='D12' else 'Related source context only; no supported outcome assigned'
        c['expected_role'] = 'legacy/current documentary role; never an actual oracle' if c['expected'] is not None else 'no documentary output oracle'
        c['documentary_comparison'] = 'documentary stated role only; no target comparison' if c['expected'] is not None else None
    # The two old unknown requirements are not retroactively converted to D12 by related context.
    assert [r['basis'] for r in reqs[:21]] == [r['basis'] for r in read(HERE/'requirements.json')]
    used = list(dict.fromkeys(x for r in reqs for x in r['source_blocks']))
    used += [x for c in cases for x in c['source_blocks'] if x not in used]
    used += [x for g in data['audit_reconciliation'] for x in g.get('retained_context_blocks',[]) if x not in used]
    used = list(dict.fromkeys(used))
    contexts = []
    for bid in used:
        ix,b = bmap[bid]; meta = source_meta[0 if bid.startswith('KN1:') else 1]
        contexts.append({'block':bid,'catalog':AREL+'/source-blocks.json','json_pointer':'/'+str(ix),
            'kind':b['kind'],'quote':b['text'], 'quote_role':'normalized table cells joined with audit separators' if b['kind']=='tr' else 'normalized retained source text',
            'source':meta,'html_line':b['html_line'],'html_column':b['html_column'],
            'raw_start':b['raw_start'],'raw_end':b['raw_end'],'offset_unit':'Unicode characters in decoded retained HTML',
            'raw_html_sha256':hashlib.sha256(b['raw_html'].encode()).hexdigest(),
            'literal_element_id':b['attributes'].get('id'),
            'heading_context':b['heading_context'],
            'requirements':[r['id'] for r in reqs if bid in r['source_blocks']],
            'cases':[c['id'] for c in cases if bid in c['source_blocks']],
            'retained_research_groups':[g['audit_group'] for g in data['audit_reconciliation'] if bid in g.get('retained_context_blocks',[])]})
    groups = read(AUDIT/'proposed-deltas.json')
    reconciled = copy.deepcopy(data['audit_reconciliation'])
    for item in reconciled:
        item['audit_proposal']={'catalog':AREL+'/proposed-deltas.json','json_pointer':'/'+str(next(i for i,g in enumerate(groups) if g['id']==item['audit_group']))}
        item['requirement_refs']=[{'catalog':REL+'/requirements-r5.json','json_pointer':'/'+str(next(i for i,r in enumerate(reqs) if r['id']==rid)),'id':rid} for rid in item['requirements']]
        item['case_refs']=[{'catalog':REL+'/cases-r5.json','json_pointer':'/'+str(next(i for i,c in enumerate(cases) if c['id']==cid)),'id':cid} for cid in item['cases']]
        item['retained_context_evidence']=evidence(item.get('retained_context_blocks',[]))
        item['target']='U'; item['complete']=False
    fixtures = copy.deepcopy(read(HERE/'fixtures.json'))
    fixtures['F1'] += ' R5 adds genuine per-operation positive control/selection/content baselines; each new negative or unavailable scenario must first admit the actual supported input/capability and productive control. Missing capability is U, never a negative pass. For NAV-088 Tab view-switch latching explicitly override global Use Tab OFF and prove ordinary switching first; this is not an exception to enabled focus traversal.'
    fixtures['F4'] = 'Lifecycle/malformed/reader-loss histories inherit an actually productive F1/F2/F3 baseline before disappearance/failure. All actual oracles remain null. A retained documentary shortcut is neither proof of target feature availability nor permission to guess a missing constructor, key dispatch, value, event, default or timing law.'
    delta = {'role':'Semantic and schema delta, not execution or closure',
        'old_catalogs_unchanged':['requirements.json','cases.json','shortcut-bindings.json'],
        'retained_requirements':21,'retained_cases':42,'added_requirements':19,'added_cases':54,
        'old_requirement_body_changes':[{'id':r['id'],'before':r['body'],'after':rmap[r['id']]['body']} for r in read(HERE/'requirements.json') if r['body']!=rmap[r['id']]['body']],
        'old_case_action_changes':[{'id':c['id'],'before':c['action'],'after':cases[i]['action']} for i,c in enumerate(read(HERE/'cases.json')) if c['action']!=cases[i]['action']],
        'old_documentary_expectations_unchanged':True,
        'added_requirement_ids':[r['id'] for r in reqs[21:]],'added_case_ids':[c['id'] for c in cases[42:]],
        'metadata_changes':'Adds exact source-block pointers, source relation, target U/not-run/complete false, actual null fields, documentary comparison role and group reconciliation. Existing expected remains documentary, not actual.',
        'canonical_before':'preservation-r4-before-r5.json', 'canonical_rebuild':'Both canonical pages rendered as revision5 from this bounded successor; exact prior bytes retained in canonical-before-r5; all original R4/history payloads in place.',
        'deferred':'Q052 conflicts, target versions, whole292 commands, unsupported focus/platform/reader/settings/file/history/numeric/signal/timing/RNG/protocol results remain U.'}
    def field_changes(before, after):
        changes=[]
        for old,new in zip(before,after):
            fields=[]
            for key in sorted(set(old)|set(new)):
                if (key in old)!=(key in new) or old.get(key)!=new.get(key):
                    fields.append({'field':key,'before_present':key in old,'after_present':key in new,
                        'before_value_sha256':hashlib.sha256(encoded(old[key])).hexdigest() if key in old else None,
                        'after_value_sha256':hashlib.sha256(encoded(new[key])).hexdigest() if key in new else None})
            changes.append({'id':old['id'],'fields':fields})
        return changes
    delta['exact_retained_record_field_changes']={
        'role':'Every changed top-level field on the21 retained requirement and42 case records; hashes cover JSON value plus terminal newline. Full before/after values are in immutable old and versioned current catalogs.',
        'requirements':field_changes(read(HERE/'requirements.json'),reqs),
        'cases':field_changes(read(HERE/'cases.json'),cases)}
    stats = {'requirements':len(reqs),'requirements_D12':sum(r['basis']=='D12' for r in reqs),'requirements_U':sum(r['basis']=='U' for r in reqs),
        'cases':len(cases),'cases_D12':sum(c['basis']=='D12' for c in cases),'cases_U':sum(c['basis']=='U' for c in cases),
        'documentary_nonnull':sum(c['expected'] is not None for c in cases),'actual_oracles_nonnull':0,
        'target_U':len(cases),'unexecuted':len(cases),'complete':0,'audit_groups':len(reconciled),
        'discovery_rows':292,'source_blocks_used':len(contexts),'full_retained_source_blocks':541}
    spec = render_spec(reqs,cases,stats)
    research = render_research(stats)
    return {'requirements-r5.json':encoded(reqs),'cases-r5.json':encoded(cases),
        'source-context-r5.json':encoded(contexts),'binding-context-r5.json':encoded(read(AUDIT/'binding-reconciliation-r2.json')[-5:]),'reconciliation-r5.json':encoded(reconciled),
        'fixtures-r5.json':encoded(fixtures),'delta-r5.json':encoded(delta),'summary-r5.json':encoded(stats),
        'spec-r5.md':spec.encode(),'research-r5.md':research.encode()}

def render_spec(reqs,cases,stats):
    text = '''---
id: SPEC-KEYBOARD-NAVIGATION
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 5
target: Ableton Live 12 Suite 12.4.3
---

# Keyboard navigation and accessibility workflows

## Scope and authority

This partial successor owns keyboard focus, navigation, accessible-control and
input-entry roles. The [approved partial source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation-source-audit/README-r2.md)
was reconciled through all 23 proposal groups; that audit approval is not owner
adoption approval, runtime evidence, or source-topic completion. The separate
292-row shortcut catalog remains discovery, with zero commands marked complete.

Underlying behavior stays with [Arrangement](arrangement-editing.md),
[MIDI editing](midi-editing-tools.md), [automation](automation-envelopes.md),
[native Warp markers](warp-markers.md), [Warp workflows](warping-workflows.md),
[Browser](browser-workflows.md), [Browser content](browser-content-workflows.md),
[Session](session-view-workflows.md), [launch](session-launch-workflows.md),
[mixing](mixing-workflows.md), [recording](recording-comping.md),
[routing](routing-monitoring-latency.md), [remote control](remote-control-workflows.md),
[settings](settings-learning-workflows.md), [device/racks](device-racks.md),
[plug-in hosting](plugin-hosting.md), [grooves](groove-workflows.md) and
[export](audio-video-export.md). Keyboard entries do not replace those owners'
numeric, edit, scheduling, launch, file, signal, API or protocol contracts.

D12 means captured current Version12 documentation, not exact12.4.3 evidence.
Every target outcome is U and every case is unexecuted. No application, UI,
reader, original function, candidate, image, hardware or network was run or
inspected for this successor. See [research](../research/keyboard-navigation.md).

## Inputs, contexts and oracles

Record platform, language/layout/IME, actual key chord, focused region, selection,
visibility, enabled controls, navigation settings, editor/modal state, valid
parameter domain, reader and genuinely productive control baseline. Main-window
Tab traversal requires global Use Tab ON; deliberate view switching requires OFF.
Settings traversal has the source-supported independent exception. Unsupported
capability or absent baseline remains U, never a negative pass.

The machine case field `expected` retains the old documentary expectations
and narrowly added visible input/control roles. It is never an actual target
oracle. Every `actual_expected` and `actual_comparison` is null. New numeric,
reader, timing, signal, analysis, configuration, clipboard/history and unresolved
cases also have null documentary outputs; their prose `source_claim` records
only the public role. No exact accessible tree, utterance, palette, waveform,
value, RNG result, deadline, key priority, default or platform equivalence follows.

[Q-052](../questions.md#q-052-keyboard-export-and-midi-note-modifier-source-differences) remains open: conflicting export and selected-note modifier texts are
retained without choosing dispatch. B350 is enabled-use context for Computer
MIDI octave/velocity rows, not the three toggle rows. B351 is related general
single-letter text, not a proved row-specific prerequisite or forced Shift rule.

## Requirements

'''
    for r in reqs:
        text += f"### {r['id']} — {r['title']}\n\n**{r['basis']}; target U; not run.** {r['body']}\n\n"
        text += 'Source/context blocks: '+', '.join(r['source_blocks'])+f". Exact quotes and locators: [source context](../../{REL}/source-context-r5.json); [typed requirement](../../{REL}/requirements-r5.json).\n\n"
        if r.get('owners'):
            text += 'Related owner context: '+', '.join(f'[{Path(x).stem}]({Path(x).name})' for x in r['owners'])+'.\n\n'
    text += '## Finite future cases\n\nThe [96-case catalog](../../'+REL+'/cases-r5.json) retains all42 prior IDs and documentary expectations. Four actions are refined;54 cases are added. Shared [fixtures](../../'+REL+'/fixtures-r5.json) require productive baselines. The table is navigation; catalog actions, exact block pointers and null oracles are authoritative.\n\n| Case | Requirement | Kind | Documentary output | Target |\n| --- | --- | --- | --- | --- |\n'
    for c in cases:
        text += f"| {c['id']} | {c['requirement']} | {c['kind']} | {'documentary role only' if c['expected'] is not None else 'null'} | U; not run |\n"
    text += '''
## Evidence, preservation and remaining work

Two original official chapters retain exact URLs, capture UTCs, Version12 labels,
bytes and hashes in [source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/sources.json).
All541 source blocks and292 discovery rows retain their original identities.
R5 selects exact text/row contexts, not uninspected figure labels or link content.
Full source audit enumeration is distinct from this bounded owner adoption.

The [23-group reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/reconciliation-r5.json)
routes existing predicates and records retained unknowns rather than asserting
whole-group completion. [Exact deltas](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/delta-r5.json)
retain21 prior requirements and42 cases, add19 requirements and54 cases, and
explain the10 body and4 action refinements. Original R4/history files remain
byte-identical in place; exact prior canonical bytes are retained separately.

Independent owner semantic review and any handoff remain pending. Q052, target
availability, every reader/platform/context combination, full292-command
applicability, malformed/intercepted input, persistence, undo, transport/rate,
teardown and unavailable-capability results remain U. Source-filled rows are
neither product completion nor reference/candidate comparison success.
'''
    return text

def render_research(stats):
    return '''---
id: RESEARCH-KEYBOARD-NAVIGATION
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 5
target: Ableton Live 12 Suite 12.4.3
---

# Navigation, accessibility and shortcut evidence

The [canonical partial contract](../specs/keyboard-navigation.md) now reconciles
all23 proposal groups from the independently reviewed source audit R2. Its full
review and focused context correction are pinned by exact bytes. Audit approval
is partial source reconciliation, not owner adoption approval or target parity.
The owner successor contains40 requirements (37D12/3U),96 proposed cases and
zero completed requirements/cases. All actual expectations/comparisons are null;
every target outcome remains U and every case is not run.

The original two Version12 manual captures remain byte-identical. Their
[URLs, UTCs and source hashes](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/sources.json)
are retained. The source audit read all541 blocks and all292 shortcut discovery
rows; this adoption refreshed the full relevant prose/list contexts and actual
qualifiers against proposed actions. Exact selected text/row quotes and raw HTML
positions are in [R5 source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json).
Paragraph heading ancestry is context, not an invented paragraph anchor. Table
quotes preserve normalized cell text; joined audit separators are not literal
source prose. Images and linked destinations remain uninspected.

R5 adds bounded menu/settings/Control Bar, Session/Arrangement/editor command
entry, envelope feedback, latching, Computer MIDI range-use and selected-panel
focus roles. It refines ten existing bodies and four actions, preserving all old
IDs and documentary expectations. Input roles link the existing domain owners
rather than replacing edit, playback, marker, preview, numeric or protocol laws.
Source numeric/timing/reader/signal/configuration descriptions remain prose with
null documentary outputs in new sensitive cases. Productive control and owned
content/capability baselines precede negative, unavailable or lifecycle probes.

Main-window Tab traversal requires ON, view switching OFF, and Settings has its
own documented exception. Tab latching explicitly establishes ordinary switching
with global Tab traversal OFF first. B350 supplies enabled Computer MIDI use
context only to octave/velocity rows; it is not a prerequisite for MIDI Map,
Key Map or Computer MIDI toggles. B351 remains related general context, not a
forced modifier or global dispatch exception.

[Q-052](../questions.md#q-052-keyboard-export-and-midi-note-modifier-source-differences) remains unresolved: accessibility export Ctrl+R/Cmd+R conflicts with table
export Ctrl+Shift+R/Cmd+Shift+R and Rename Ctrl+R/Cmd+R; Windows previous/next and
same-pitch note modifiers differ (Ctrl versus Alt). Mac Option agreement does
not prove contexts identical. Original292 discovery bytes remain untouched.
No selected default, precedence, global Shift extension or negative dispatch law
was inferred. Source support limitations likewise do not exclude target features.

All108 original R4/history packet files remain byte-identical in place. Exact
pre-edit canonical copies and hashes are retained in canonical-before-r5 and
preservation-r4-before-r5.json. Old tools/manifests are historical: do not replay
old live-canonical checks against R5. New readonly validation uses exact retained
old bytes and current R5 snapshots; it never rewrites frozen reports.
[Consumer routing](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/historical-consumer-routing-r5.json)
identifies exact historical source pins for root integration, without modifying
consumers or declaring all their semantics stale. This successor is pending a
separate independent owner review and any approved handoff. No OS, reader, app,
original function, candidate, image, hardware, network or runtime was executed.
'''

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--write', action='store_true'); parser.add_argument('--check', action='store_true'); args=parser.parse_args()
    assert args.write != args.check, 'choose exactly --write or --check'
    if args.write and (HERE/'manifest-author-r5.json').exists():
        raise SystemExit('refusing writes: R5 sealed')
    outputs=build()
    for name,raw in outputs.items():
        if args.write: (HERE/name).write_bytes(raw)
        else: assert (HERE/name).read_bytes()==raw, name+' differs from bounded derivation'
    for canonical,snapshot in [('wiki/specs/keyboard-navigation.md','spec-r5.md'),('wiki/research/keyboard-navigation.md','research-r5.md')]:
        if args.write: (ROOT/canonical).write_bytes(outputs[snapshot])
        else: assert (ROOT/canonical).read_bytes()==outputs[snapshot],canonical
    print(json.dumps({'mode':'write' if args.write else 'readonly-check','outputs':len(outputs),'summary':json.loads(outputs['summary-r5.json'])}))

if __name__=='__main__': main()
