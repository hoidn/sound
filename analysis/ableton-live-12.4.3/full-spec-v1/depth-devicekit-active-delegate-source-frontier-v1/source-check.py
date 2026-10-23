"""Read-only seven-source integrity check; never opens original chunks, indexes or target bytes."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import sys

P = Path(__file__).resolve().parent
B = P.parent
J = lambda p: json.loads(p.read_text())
H = lambda raw: hashlib.sha256(raw).hexdigest()


def validate(d):
    raw, rows, census, ret, read, front, joins, assessment = [d[k] for k in
        ['raw', 'rows', 'census', 'retention', 'read', 'front', 'joins', 'assessment']]
    wanted = d['source_selection']['entries']
    assert len(wanted) == len(set(wanted)) == len(rows) == 7
    assert [r['entry'] for r in rows] == wanted == [r['entry'] for r in census['records']]
    assert len(raw) == 10797 and H(raw) == 'ebdd6147604e4674868e22b4334de90eaedf212ad10c27e63c2a28f58eb15289'
    rawrows = raw.splitlines(keepends=True)
    assert [json.loads(x) for x in rawrows] == rows
    assert sum(len(r['code'].encode()) for r in rows) == 7851
    assert sum(len(r['code'].splitlines()) for r in rows) == 277
    assert sum(bool(r['warnings']) for r in rows) == 2
    assert ret['original_record_range_reads'] == 7 and ret['fresh_whole_chunk_hashes'] == ret['aliases_rescans'] == 0
    assert ret['raw_bytes'] == len(raw) and ret['raw_sha256'] == H(raw)
    assert ret['inherited_chunk_pins'] == census['selected_chunk_pins']
    assert len(read['premises']) == 8 and 'not validated native ABI' in read['premises'][0]
    assert 'opaque' in read['premises'][2] and 'unsimplified' in read['premises'][5]
    assert len(read['records']) == len(front['records']) == len(joins['records']) == 7
    statement_ids = []; boundary_ids = []; references = collections.Counter(); offset = 0
    for i, (r, m, loc, rd, fr, join) in enumerate(zip(rows, census['records'], ret['records'],
            read['records'], front['records'], joins['records'])):
        assert r['entry'] == m['entry'] == loc['entry'] == rd['entry'] == fr['entry'] == join['target_entry']
        assert len(rawrows[i]) == m['raw_bytes'] == loc['raw_bytes'] and H(rawrows[i]) == m['raw_sha256'] == loc['raw_sha256']
        assert loc['retained_byte'] == offset and loc['source_byte'] == m['source_byte'] and loc['source_line'] == m['source_line'] and loc['source_path'] == m['source_path']
        offset += len(rawrows[i])
        code = r['code'].encode(); lines = r['code'].splitlines(keepends=True)
        assert len(code) == m['code_utf8_bytes'] == loc['C_bytes'] and H(code) == m['code_sha256'] == loc['C_sha256']
        assert len(lines) == m['C_lines'] == loc['C_lines']
        assert r['warnings'] == m['warnings'] == rd['warnings']
        assert r['body_bytes'] == m['native_body_bytes'] and r['body_ranges'] == m['native_body_ranges']
        assert not r['thunk'] and not m['alias_thunk'] and not m['record_thunk']
        assert not r['timed_out'] and not r['partial_code'] and r['error'] is None
        assert rd['metadata'] == m and rd['whole_C_read'] and rd['read_C_lines'] == [1, len(lines)] and rd['constraint']
        assert rd['legal_inputs'] is rd['expected_output'] is rd['stub_recipe'] is None and not rd['math_leaf'] and not rd['execution_ready']
        assert rd['statements']
        for s in rd['statements']:
            assert 1 <= s['C_start'] <= s['C_end'] <= len(lines)
            span = ''.join(lines[s['C_start'] - 1:s['C_end']]).encode()
            assert len(span) == s['span_bytes'] and H(span) == s['span_sha256']
            assert s['premises'] == list(range(1, 9)) and s['status'] == 'observed-static-projection'
            assert not s['public_route'] and not s['complete_callable_leaf']
            statement_ids.append(s['id'])
        expected = []
        for n, line in enumerate(lines, 1):
            if n == 2:
                assert line.startswith('void FUN_' + r['entry'][2:] + '(')
                continue  # Selected function declaration is not an outgoing call.
            expected += [('opaque-direct-call', x, n, n) for x in re.findall(r'\b(FUN_[0-9a-f]+)\s*\(', line)]
            expected += [('projection-intrinsic', x, n, n) for x in re.findall(r'\b(NEON_[A-Za-z0-9_]+)\s*\(', line)]
            expected += [('pointer-literal' if x.startswith(('PTR_manage_', 'PTR_invoke_')) else 'global-pointer-read', x, n, n) for x in re.findall(r'\bPTR_[A-Za-z0-9_]+\b', line)]
            if '___stack_chk_fail(' in line: expected.append(('named-direct-call', '___stack_chk_fail', n, n))
            if '::invoke(' in line: expected.append(('named-direct-call', 'InvokeFunctionFactory<...ChannelEq::tick...>::invoke', n - 2, n))
            for token in ['(*local_30)(&local_38,0,1)', '(*(code *)*puVar2)(puVar2[1])',
                          '(**(code **)(param_1 + 0x330))(param_1 + 0x338,&local_48)']:
                if token in line: expected.append(('indirect-call', token, n, n))
        assert collections.Counter(expected) == collections.Counter((r['kind'], r['token'], r['C_start'], r['C_end']) for r in fr['references'])
        for ref in fr['references']:
            span = ''.join(lines[ref['C_start'] - 1:ref['C_end']]).encode()
            assert len(span) == ref['span_bytes'] and H(span) == ref['span_sha256']
            assert not ref['target_read'] and not ref['followed'] and ref['binding'] == 'unknown'
            references[ref['kind']] += 1
        ops = [(n, x) for n, line in enumerate(lines, 1) for x in re.findall(r'\b(ABS|NAN)\s*\(', line)]
        assert ops == [(r['C_line'], r['operator']) for r in fr['projection_operators']]
        assert not fr['complete_callable_X'] and fr['new_original_batch'] is None and len(fr['missing']) == 3
        selected = d['metadata_selection']['selected'][i]
        assert join['parent_entry'] == selected['parent_entry'] and join['quote'] == selected['quote'] and join['quote_sha256'] == selected['quote_sha256'] == H(join['quote'].encode())
        assert join['parent_C_lines'] == selected['source_C_lines']
        parent = d['parent_records'][join['parent_entry']]
        lo, hi = join['parent_C_lines']; assert lo == hi and parent['code'].splitlines()[lo - 1] == join['quote']
        pj = next(p for p in d['parent_joins'] if p['entry'] == join['parent_entry'])
        assert join['parent_declaration_navigation'] == pj and join['new_target_alias'] == m['alias_name'] and join['new_target_alias_source'] == m['alias_source']
        assert not join['parent_stub_runtime_binding'] and not join['new_target_current_receiver'] and not join['new_target_provider_binding'] and join['new_site_credit'] == 0
        boundary_ids += pj['boundary_rows']
    assert len(statement_ids) == len(set(statement_ids)) == read['conditional_statements'] == 19
    assert read['not_required_outcome_denominator']
    assert references == front['reference_counts'] == {'opaque-direct-call': 7, 'global-pointer-read': 4, 'pointer-literal': 4, 'named-direct-call': 3, 'indirect-call': 3, 'projection-intrinsic': 3}
    assert front['reference_total'] == 24 and front['projection_operator_occurrences'] == 10
    assert not front['new_follow'] and front['new_body_native_provider_reads'] == 0 and not front['successor_selected']
    assert boundary_ids == joins['current_parent_subset_source_ids'] and len(boundary_ids) == len(set(boundary_ids)) == 7
    assert joins['inherited_parent_records'] == 27 and joins['inherited_parent_source_occurrences'] == 37 and not joins['new_runtime_binding'] and joins['new_site_credit'] == 0
    for k in ['complete_callable_math_leaves', 'complete_callable_X_leaves', 'ready_original_batches', 'new_site_credit', 'new_required_outcomes', 'new_case_grade_release']:
        assert assessment[k] == 0
    for k in ['current_receiver_binding', 'actual_control_binding', 'actual_audio_host_delivery', 'runtime_weak_stub_binding', 'documentary_fallback', 'successor_selected']:
        assert assessment[k] is False
    assert assessment['legal_inputs'] is assessment['calibrated_metric'] is None
    assert assessment['unsupported_required'] == 'U' and assessment['coverage_gate'] == 'OPEN'
    assert len(assessment['whole_set_constraints']) == 7 and 'Separate Root selection' in assessment['setup_gate']
    receipt = d['receipt']; assert receipt['fresh'] == dict(records=7, C_bytes=7851, C_lines=277, whole_bodies=True, untruncated_display=True, warnings=2, original_record_ranges=7, aliases_rescans=0, new_whole_chunk_hashes=0)
    assert receipt['metadata_stage_files_preserved'] == 7 and receipt['Root_source_selection_preserved']
    assert receipt['new_callee_global_slot_native_image_provider_original_model_harness_reads_or_runs'] == receipt['canonical_shared_writes'] == 0 and not receipt['successor_selected']


def main():
    assert sys.argv[1:] == ['--check'], 'read-only --check, before reads'
    protected = J(P / 'metadata-preservation.json')['protected_files']
    assert len(protected) == 8 and len({p['path'] for p in protected}) == 8
    for pin in protected:
        assert '/' not in pin['path']
        raw = (P / pin['path']).read_bytes()
        assert len(raw) == pin['bytes'] and H(raw) == pin['sha256']
    assert H((P / 'source-selection-root.json').read_bytes()) == '6e05dada98e72dab38f05d64c7f743a8e67c9e54ddb683a85cd263dc8fed1048'
    assert H((P / 'candidate-census.json').read_bytes()) == 'ee5dc80ff16db40c2b99249c175aade22cd5c0c8c7170dad598f585274709c54'
    allowed = {(B / 'depth-devicekit-defined-method-source-frontier-v1' / n).resolve() for n in ['manifest.json', 'sources.jsonl', 'declaration-source-joins.json']} | {(B / 'reviews/devicekit-defined-method-source-v1-review.json').resolve()}
    immutable = J(P / 'source-pins.json')['immutable']
    assert {Path(p['path']) for p in immutable} == allowed
    for pin in immutable:
        raw = Path(pin['path']).read_bytes()
        assert len(raw) == pin['bytes'] and H(raw) == pin['sha256']
    parent = B / 'depth-devicekit-defined-method-source-frontier-v1'
    raw = (P / 'sources.jsonl').read_bytes()
    d = dict(raw=raw, rows=[json.loads(x) for x in raw.splitlines()], census=J(P / 'candidate-census.json'),
        retention=J(P / 'source-retention.json'), read=J(P / 'source-read-map.json'),
        front=J(P / 'dependency-frontier.json'), joins=J(P / 'parent-joins.json'),
        assessment=J(P / 'source-assessment.json'), source_selection=J(P / 'source-selection-root.json'),
        metadata_selection=J(P / 'selection-metadata-only.json'), receipt=J(P / 'source-read-receipt.json'),
        parent_records={r['entry']: r for r in map(json.loads, (parent / 'sources.jsonl').read_bytes().splitlines())},
        parent_joins=J(parent / 'declaration-source-joins.json')['joins'])
    validate(d)
    negatives = []
    def reject(name, change):
        bad = copy.deepcopy(d); change(bad)
        try: validate(bad)
        except (AssertionError, KeyError, IndexError, TypeError, ValueError):
            negatives.append(name); return
        raise AssertionError('negative accepted: ' + name)
    reject('omit-selected-source', lambda x: x['rows'].pop())
    reject('change-retained-C', lambda x: x['rows'][0].update(code='void f(){}'))
    reject('erase-warning', lambda x: x['rows'][1].update(warnings=[]))
    reject('invent-native-extent', lambda x: x['rows'][0].update(body_bytes=4))
    reject('wrong-retained-offset', lambda x: x['retention']['records'][0].update(retained_byte=1))
    reject('wrong-original-offset', lambda x: x['retention']['records'][0].update(source_byte=0))
    reject('drop-whole-method', lambda x: x['read']['records'].pop())
    reject('drop-ABI-premise', lambda x: x['read']['premises'].__setitem__(0, 'valid native ABI'))
    reject('helper-effects-known', lambda x: x['read']['premises'].__setitem__(2, 'helpers known'))
    reject('simplify-FP-law', lambda x: x['read']['premises'].__setitem__(5, 'exact simplified math'))
    reject('wrong-claim-span', lambda x: x['read']['records'][0]['statements'][0].update(C_start=15))
    reject('invent-public-route', lambda x: x['read']['records'][0]['statements'][0].update(public_route=True))
    reject('invent-complete-subleaf', lambda x: x['read']['records'][0]['statements'][0].update(complete_callable_leaf=True))
    reject('invent-input-recipe', lambda x: x['read']['records'][0].update(legal_inputs=[0]))
    reject('drop-dependency', lambda x: x['front']['records'][0]['references'].pop())
    reject('function-declaration-as-call', lambda x: x['front']['records'][0]['references'].append(dict(x['front']['records'][0]['references'][0], token='FUN_103fec998', C_start=2, C_end=2)))
    reject('wrong-dependency-token', lambda x: x['front']['records'][0]['references'][0].update(token='FUN_100000000'))
    reject('auto-follow-dependency', lambda x: x['front']['records'][0]['references'][0].update(followed=True))
    reject('claim-new-helper-body', lambda x: x['front']['records'][0]['references'][0].update(target_read=True))
    reject('drop-packed-FP-operator', lambda x: x['front']['records'][0]['projection_operators'].pop())
    reject('swap-parent-entry', lambda x: x['joins']['records'][0].update(parent_entry=x['joins']['records'][1]['parent_entry']))
    reject('corrupt-parent-quote', lambda x: x['joins']['records'][0].update(quote='wrong'))
    reject('invent-runtime-stub-binding', lambda x: x['joins']['records'][0].update(parent_stub_runtime_binding=True))
    reject('invent-provider-binding', lambda x: x['joins']['records'][0].update(new_target_provider_binding=True))
    reject('seven-subset-as37-new-sites', lambda x: x['joins'].update(new_site_credit=37))
    reject('invent-math-leaf', lambda x: x['assessment'].update(complete_callable_math_leaves=1))
    reject('invent-X-leaf', lambda x: x['assessment'].update(complete_callable_X_leaves=1))
    reject('invent-current-receiver', lambda x: x['assessment'].update(current_receiver_binding=True))
    reject('invent-current-control', lambda x: x['assessment'].update(actual_control_binding=True))
    reject('invent-audio-delivery', lambda x: x['assessment'].update(actual_audio_host_delivery=True))
    reject('invent-metric', lambda x: x['assessment'].update(calibrated_metric={'rms': 0.01}))
    reject('bypass-setup-selection', lambda x: x['assessment'].update(setup_gate='automatic'))
    reject('close-unsupported', lambda x: x['assessment'].update(unsupported_required='PASS'))
    reject('close-coverage', lambda x: x['assessment'].update(coverage_gate='CLOSED'))
    reject('documentary-fallback', lambda x: x['assessment'].update(documentary_fallback=True))
    reject('select-successor', lambda x: x['assessment'].update(successor_selected=True))
    print(json.dumps(dict(status='PASS-read-only-seven-source-integrity',
        checker_sha256=H(Path(__file__).read_bytes()), protected_metadata_and_Root_files=8,
        minimal_parent_document_pins=4, records=7, raw_bytes=10797, C_bytes=7851, C_lines=277,
        warnings=2, conditional_claims=19, dependency_references=24, projection_operators=10,
        inherited_parent_records=27, inherited_parent_source_ids=37, current_parent_subset_ids=7,
        negatives=negatives, negative_count=len(negatives),
        new_chunk_index_native_image_provider_original_model_harness_reads_or_runs=0,
        original_record_reads_in_this_checker=0, new_site_grade_case_release=0,
        complete_callable_math_X_leaves=0, coverage='OPEN', required_unsupported='U',
        successor_selected=False), indent=2))


if __name__ == '__main__':
    main()

