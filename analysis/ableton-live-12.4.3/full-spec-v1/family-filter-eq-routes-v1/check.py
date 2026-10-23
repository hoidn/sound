#!/usr/bin/env python3
"""Read-only stdlib integrity and false-promotion checks; recovered code is data."""
import copy
import hashlib
import json
from pathlib import Path
import re
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent


def require(test, message):
    if not test:
        raise AssertionError(message)


def load(path):
    return json.loads(path.read_text())


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def same_pin(data, pin):
    return identity(data) == {k: pin[k] for k in ['bytes', 'sha256']}


def selected_row(row):
    loc = row['locator']
    path = Path(loc['path']) if loc['path'].startswith('/') else ROOT / loc['path']
    with path.open('rb') as stream:
        stream.seek(loc['byte_start'])
        raw = stream.read(loc['bytes'])
    require(same_pin(raw, loc), 'selected source row identity')
    parsed = json.loads(raw)
    if row['kind'] == 'literal-store-candidate':
        parsed.pop('quote')
    require(parsed == row['record'], 'selected source row projection')
    require('code' not in row['record'] and 'quote' not in row['record'], 'no native body/pseudocode materialization')


def semantics(ledger, inputs, requirements, cases):
    clauses = ledger['clauses']
    navigation = ledger['case_navigation']
    contexts = ledger['state_error_lifecycle_contexts']
    require([x['requirement'] for x in clauses] == [r['id'] for r in requirements], 'all65 owner IDs')
    require([x['id'] for x in navigation] == [c['id'] for c in cases], 'all140 current case pointers')
    require(len({x['id'] for x in navigation}) == 140, 'case IDs unique')
    require([x['case_id'] for x in contexts] == [c['id'] for c in cases if c['provenance'] == 'U'], 'all46 U actions')
    for row, req in zip(clauses, requirements):
        require(row['route'] == ('S' if req['provenance'] == 'Dpkg' else 'none'), 'D12/native name promoted to exact-target route')
        require(row['runtime_target_status'] == 'U', 'file evidence promoted to runtime/defaults')
        require(row['case_ids'] == [c['id'] for c in cases if req['id'] in c['requirements']], 'requirement/case navigation')
        require(row['source']['catalog_record_sha256'] == hashlib.sha256(canonical(req)).hexdigest(), 'requirement record identity')
    for i, (row, case) in enumerate(zip(navigation, cases)):
        require(row['pointer'] == '/cases/' + str(i), 'case pointer')
        require(row['record_sha256'] == hashlib.sha256(canonical(case)).hexdigest(), 'case full object identity')
        require(row['setup_action_sha256'] == hashlib.sha256(case['setup_action'].encode()).hexdigest(), 'case full action identity')
        require(row['requirements'] == case['requirements'] and row['kind'] == case['kind'] and row['provenance'] == case['provenance'], 'case scope')
        require(row['route'] == ('S' if case['provenance'] == 'Dpkg' else 'none') and row['target_observation'] is None, 'case target promotion')
    require(all(c['route'] == 'none' and c['target_observation'] is None for c in contexts), 'lifecycle oracle manufactured')
    require(ledger['inventory'] == {'requirements':65,'case_pointers':140,'U_action_contexts':46,'clause_routes':{'none':61,'S':4},'case_navigation_routes':{'none':136,'S':4},'new_native_bodies':0,'new_original_calls':0,'new_behavior_grades':0,'new_indirect_resolution_credit':0}, 'units/promotion error')
    guard = inputs['guard_policy']
    required = ['productive_nonzero_source_and_control_required_for_signal_contrast', 'accepted_controls_and_nonmuted_wet_output_required', 'AF_isolated_other_modulator_zero_required', 'AF_curve_AND_output_response_required', 'AF_hold_attack_outlasts_pulse_required', 'EQ8_both_audition_contributions_productive_required', 'EQ8_actual_press_hold_release_required', 'EQ3_stable_lit_before_disable_required']
    require(all(guard[k] is True for k in required), 'productive prerequisite dropped')
    require(guard['EQ8_audition_return_state'] == guard['missing_or_indeterminate_prerequisite_status'] == 'U', 'unknown return/prerequisite promoted')
    require(guard['prerequisite_success_observed'] is False and guard['merged_sidechain_Type_enum_or_chosen_detector_tap'] is False, 'source ambiguity or fixture success manufactured')
    require(all(x['route_credit'] == 'none' and x['new_body_read'] is False for x in inputs['auxiliary_leaves']), 'auxiliary computation promoted')


def main():
    pins = load(HERE / 'pins.json')
    asof_changed = []
    for pin in pins['files']:
        data = (ROOT / pin['path']).read_bytes()
        if pin['role'].startswith('mutable'):
            if not same_pin(data[:pin['bytes']], pin):
                asof_changed.append(pin['path'])
        else:
            require(same_pin(data, pin), 'immutable pin ' + pin['path'])
    req = load(BASE / 'filter-eq/requirements.json')
    cases = load(BASE / 'filter-eq/cases-r4.json')['cases']
    require(len(req) == 65 and len(cases) == 140, 'current R4 providers')
    require(Counter(c['provenance'] for c in cases) == {'D12':90,'Dpkg':4,'U':46}, 'historical128/current140 distinction')
    for c in cases[-12:]:
        require(c['expected'] is None and c['actual_expected'] is None and c['documentary_expected'] is None and c['exact_target'] == 'U' and c['status'] == 'unexecuted', 'R4 null history preserved')
    ledger, inputs = load(HERE / 'route-ledger.json'), load(HERE / 'input-sets.json')
    semantics(ledger, inputs, req, cases)
    census = load(HERE / 'query-census.json')
    meta, calls = rows(HERE / 'metadata-rows.jsonl'), rows(HERE / 'call-rows.jsonl')
    counts = Counter(r['kind'] for r in meta)
    require(counts == {'lexical-owner':129,'membership':177,'table':7,'RTTI':7,'literal-store-candidate':10,'alias':202}, 'selected metadata unit counts')
    tables = [x['record'] for x in meta if x['kind'] == 'table']
    require({t['literal_type_encoding'] for t in tables} == set(census['selection']['literal_types']), 'exact selected type names')
    require(sum(len(t['slots']) for t in tables) == 21 and len(tables) <= census['caps']['tables'], 'table/slot cap')
    require(counts['membership'] + counts['alias'] == 379 <= census['caps']['aliases_plus_memberships'], 'alias/membership cap')
    require(counts['literal-store-candidate'] <= census['caps']['literal_stores'] and len(calls) == 492 <= census['caps']['calls_total'], 'store/call cap')
    require(Counter(x['kind'] for x in calls) == {'call':453,'indirect':39}, 'native record units')
    require(Counter(x['record']['ref_type'] for x in calls if x['kind'] == 'call') == {'UNCONDITIONAL_CALL':429,'UNCONDITIONAL_JUMP':24}, 'call versus jump units')
    require(all(x['record']['resolved_targets'] == [] for x in calls if x['kind'] == 'indirect'), 'unresolved sites unchanged')
    roots = set(census['selection']['fixed_call_roots'])
    require('0x101aa4b90' not in roots, 'shared hub excluded')
    for x in calls:
        r = x['record']
        require((r['function'] in roots) if x['kind'] == 'indirect' else (r['caller'] in roots or any(r.get(k) in roots for k in ['to','callee','callee_resolved'])), 'fixed set only; no transitive roots')
    for row in meta + calls:
        selected_row(row)
    audit = load(BASE / 'filter-eq-source-audit/audit.json')
    locators = load(HERE / 'source-locators.json')
    require(len(locators['audit_blocks']) == len(audit['blocks']) == 108, 'all approved source-context locators')
    for i, (loc, block) in enumerate(zip(locators['audit_blocks'], audit['blocks'])):
        require(loc['id'] == block['id'] and loc['pointer'] == '/blocks/' + str(i), 'source pointer')
        require(loc['text_sha256'] == hashlib.sha256(block['text'].encode()).hexdigest(), 'source context text identity')
        require(all(loc[k] == block[k] for k in ['raw_start','raw_end','html_line','html_column']), 'source coordinate units')
    require([q['id'] for q in locators['source_questions']] == [q['id'] for q in audit['source_questions']], 'all four unresolved source questions')
    provider = (BASE / 'filter-eq/spec-r4.md').read_bytes()
    for loc in locators['canonical_clause_spans']:
        require(identity(provider[loc['byte_start']:loc['byte_start'] + loc['bytes']]) == {k:loc[k] for k in ['bytes','sha256']}, 'exact reused R4 clause span')
    pkg = load(BASE / 'filter-eq/package-values.json')
    file_assertions = 0
    for case in cases:
        if case['provenance'] != 'Dpkg':
            continue
        assertion = case['file_assertions']
        record = next(x for x in pkg if x['source'] == assertion['path'])
        require(record['class'] == assertion['class'] and record['root_attributes']['Creator'] == 'Ableton Live 12.4d1', 'historical package/source domain')
        for suffix, expected in assertion['values'].items():
            path = '/Ableton/' + assertion['class'] + '/' + suffix
            value = next(x['attributes']['Value'] for x in record['values'] if x['path'] == path)
            require(value == expected, 'retained file string')
            file_assertions += 1
    change = load(HERE / 'research-change.json')
    research = (ROOT / change['path']).read_bytes()
    require(same_pin(research[:change['after_prefix']['bytes']], change['after_prefix']), 'research additive prefix')
    date_base = research[:change['date_only_base']['bytes']]
    require(same_pin(date_base, change['date_only_base']), 'research date-only base')
    restored = date_base.decode().replace('updated: 2026-10-20\n', 'updated: 2026-10-19\n', 1).encode()
    require(same_pin(restored, change['before']), 'all old research bytes preserved except date')
    chain = load(HERE / 'chain-edges.json')
    require(len(chain['edges']) == 17 and chain['runtime_sequence_established'] is False and chain['new_indirect_resolution_credit'] == 0, 'chain unit/premise policy')
    require(all(e['runtime_sequence_established'] is False and e['public_outcome_credit'] == 0 for e in chain['edges']), 'metadata edge promoted')
    negatives = []
    def reject(name, changed_ledger=None, changed_inputs=None):
        try:
            semantics(changed_ledger or ledger, changed_inputs or inputs, req, cases)
        except (AssertionError, KeyError):
            negatives.append({'name':name,'status':'rejected'})
            return
        raise AssertionError('negative not rejected ' + name)
    d = copy.deepcopy(ledger); d['clauses'][0]['route'] = 'S'; reject('D12 becomes exact-target static behavior', changed_ledger=d)
    d = copy.deepcopy(ledger); next(r for r in d['clauses'] if r['provenance'] == 'Dpkg')['runtime_target_status'] = 'known-default'; reject('historical file becomes current default', changed_ledger=d)
    d = copy.deepcopy(ledger); d['case_navigation'].pop(); reject('missing current R4 case', changed_ledger=d)
    d = copy.deepcopy(ledger); d['state_error_lifecycle_contexts'].pop(); reject('omitted lifecycle/error context', changed_ledger=d)
    d = copy.deepcopy(inputs); d['auxiliary_leaves'][0]['route_credit'] = 'X'; reject('external math promoted to public X route', changed_inputs=d)
    for key in ['AF_curve_AND_output_response_required','AF_hold_attack_outlasts_pulse_required','EQ8_both_audition_contributions_productive_required','EQ8_actual_press_hold_release_required','EQ3_stable_lit_before_disable_required']:
        d = copy.deepcopy(inputs); d['guard_policy'][key] = False; reject('dropped ' + key, changed_inputs=d)
    d = copy.deepcopy(inputs); d['guard_policy']['merged_sidechain_Type_enum_or_chosen_detector_tap'] = True; reject('guessed source ambiguity resolution', changed_inputs=d)
    d = copy.deepcopy(inputs); d['guard_policy']['EQ8_audition_return_state'] = 'restored'; reject('invented Audition return oracle', changed_inputs=d)
    damaged = copy.deepcopy(meta[0]); damaged['locator']['sha256'] = '0' * 64
    try:
        selected_row(damaged)
    except AssertionError:
        negatives.append({'name':'changed retained native metadata identity','status':'rejected'})
    else:
        raise AssertionError('metadata negative not rejected')
    links = 0
    for path in [HERE / 'README.md', HERE / 'structure.md']:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            require('://' not in target and (path.parent / target.split('#')[0]).resolve().exists(), 'packet link')
            links += 1
    print(json.dumps({'schema':'bounded-family-readonly-check-v1','status':'pass','requirements':65,'case_pointers':140,'U_action_contexts':46,'clause_routes':{'X':0,'S_file_only':4,'none':61},'metadata_rows_verified':len(meta),'selected_call_rows_verified':453,'selected_unresolved_indirect_rows_verified':39,'selected_tables':7,'selected_slots':21,'selected_literal_stores':10,'selected_aliases_plus_memberships':379,'native_body_reads':0,'source_context_locators_verified':108,'native_jsonl_rows_verified_by_seek_and_hash':len(meta)+len(calls),'file_only_strings_verified':file_assertions,'pins':len(pins['files']),'asof_contexts_changed_since_selection':asof_changed,'research_prefix_preserved_except_updated_date':True,'local_packet_links':links,'negative_controls':negatives,'new_original_calls':0,'new_behavior_grades':0,'new_indirect_resolution_credit':0,'limits':['Documentary integrity and bounded metadata only; no native body/provider/binary/decoder/harness/original/model/comparator/build/fixture generation or old-module execution.','No whole predecessor payload universe or main image replay; full108-block source-audit semantics and owner R4 approval are inherited as partial.','Case/source/group units are not atomic outcomes or complete family/product denominator.','Native symbols/slots/calls and four file-only S routes do not prove public runtime behavior.']},indent=2))


if __name__ == '__main__':
    main()
