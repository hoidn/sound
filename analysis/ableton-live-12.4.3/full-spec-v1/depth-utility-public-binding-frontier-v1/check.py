"""Data-only whole-frontier check; no inherited scripts, binaries or original calls."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read(name):
    return json.loads((HERE / name).read_text())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pointer(value, path):
    for token in path.split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def guards(ledger, queries, observations):
    rows = ledger['frontiers']
    assert [x['id'] for x in rows] == [f'G{i:02}' for i in range(1, 7)]
    assert ledger['frontier_count'] == 6
    assert ledger['complete_public_bridges_newly_closed'] == 0
    assert ledger['selected_successor'] is None and ledger['new_execution'] is False
    assert ledger['new_indirect_resolution_credit'] == 0
    assert not any(ledger['object_identity_guards'].values())
    assert ledger['preserved_family_inventory'] == dict(
        predicates=48, S_retained_file=2, no_established_public_route=46, X=0,
        application_case_outcomes_U=38, case_objects_navigation=41,
        required_outcome_denominator=None, new_grades=0)
    assert ledger['existing_local_X']['children'] == 2
    assert ledger['existing_local_X']['returned_calls'] == 6
    assert ledger['existing_local_X']['new_calls'] == 0
    prefix = ledger['prefix_provenance']
    assert prefix['decoded_rows'] == 16 and prefix['decoded_bytes'] == 47
    assert prefix['opaque_selected_bytes'] == 193
    for key in ['original_instruction_executions', 'creation_success_established',
                'class_identity_established', 'complete_extent_established', 'callee_following']:
        assert not prefix[key]
    assert prefix['unselected_targets'] == ['0x101ad08a0', '0x102231400']
    obs = {x['id']: x for x in observations['observations']}
    assert len(obs) == len(observations['observations'])
    qs = {x['id'] for x in queries['C_queries'] + queries['metadata_queries']}
    for row in rows:
        assert row['classification'] == 'unknown'
        assert row['public_bridge_closed'] is row['same_instance_established'] is False
        assert row['source_absence_means'] == 'unknown-not-infeasible'
        assert row['actual_expected'] is row['actual'] is row['comparison'] is row['new_grade'] is None
        assert row['missing_source'] and row['contexts'] and row['owner_rows']
        assert row['candidate_source_frontier']['selected'] is False
        assert set(row['evidence']) <= set(obs) and set(row['queries']) <= qs
    for item in obs.values():
        assert item['native_call_pc'] is None
        assert item['actual_instance_identity'] is item['public_bridge_closed'] is False
    assert queries['query_results_are_not_outcomes'] is True
    assert queries['counts']['frontier_units'] == 6
    for q in queries['C_queries']:
        assert q['negative_scope'] and q['interpretation']
    assert queries['class_slot_query']['searched_rows'] == 24


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no collection or write mode.')
    pins, ledger, queries, loc = [read(n) for n in
        ['pins.json', 'frontier-ledger.json', 'query-records.json', 'evidence-locators.json']]
    assert pins['no_full_spec_snapshots'] and not pins['predecessor_universe_replayed']
    providers = {}
    for item in pins['providers']:
        path = ROOT / item['path']
        assert path.suffix in {'.json', '.jsonl'}
        raw = path.read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256'], item['id']
        providers[item['id']] = json.loads(raw) if path.suffix == '.json' else [
            json.loads(line) for line in raw.splitlines()]
    prefix = pins['research_prefix']
    research = (ROOT / prefix['path']).read_bytes()
    assert sha(research[:prefix['bytes']]) == prefix['sha256']
    change = read('research-change.json')
    assert change['prefix'] == prefix and change['append_start_byte'] == prefix['bytes']
    start, size = change['append_start_byte'], change['append_bytes']
    assert sha(research[start:start + size]) == change['append_sha256']
    assert change['old_bytes_preserved'] and change['pending_review']
    for target in re.findall(r'\]\(([^)]+)\)', (HERE / 'structure.md').read_text()):
        assert (HERE / target.split('#')[0]).is_file(), target
    guards(ledger, queries, loc)
    records = {r['id']: r for r in queries['record_references']}
    assert len(records) == 74 and len(queries['deduplicated_C_records']) == 73
    codes = {}
    for item in records.values():
        rec = pointer(providers[item['provider']], item['pointer'])
        assert item['domain'] == 'Live.arm64' and item['source_kind'] == 'retained-recovered-C-only'
        for key in ['entry', 'code_bytes', 'code_sha256', 'state', 'partial_code', 'warnings']:
            assert item[key] == rec.get(key), (item['id'], key)
        code = rec['code']
        assert len(code.encode()) == item['code_bytes'] and sha(code.encode()) == item['code_sha256']
        codes[item['id']] = code
    for q in queries['C_queries']:
        hits = []
        for rid in q['record_set']:
            text = codes[rid]
            base = text.find('{') + 1 if q['mode'] == 'direct-call' else 0
            for match in re.finditer(q['pattern'], text[base:]):
                start, end = base + match.start(), base + match.end()
                hits.append(dict(record=rid, code_char_start=start, code_char_end_exclusive=end,
                    code_line=text.count('\n', 0, start) + 1,
                    matched_sha256=sha(text[start:end].encode())))
        assert hits == q['hits'] and len(hits) == q['hit_count'], q['id']
    meta = providers['x86-metadata']['selection']['rows']
    for q in queries['metadata_queries']:
        hits = [dict(pointer=f'/selection/rows/{kind}/{n}', nlist_index=x['nlist_index'],
            name=x['name'], value=x['n_value_hex']) for kind, arr in meta.items()
            for n, x in enumerate(arr) if re.search(q['pattern'], x['name'])]
        assert hits == q['hits'] and len(hits) == q['hit_count']
        assert q['searched_rows'] == sum(map(len, meta.values()))
    iq = queries['class_slot_query']
    hits = [dict(row=n + 1, site=x['site'], target=x['target'])
        for n, x in enumerate(providers['indirect24']) if x.get('target') in iq['selections']]
    assert iq['hits'] == hits
    for item in loc['observations']:
        value = pointer(providers[item['provider']], item['pointer'])
        assert sha(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()) == item['canonical_JSON_sha256']
    family = providers['family-edges']['edges']
    valid_rows = {r['id'] for r in providers['family-ledger']['rows']}
    for row in ledger['frontiers']:
        source = pointer(providers['family-edges'], row['predecessor_edge_pointer'])
        assert source['id'] == row['id'] and source['classification'] == 'unknown'
        assert row['predecessor_obligation'] == {k: source[k] for k in ['from', 'to', 'premises_or_missing_join']}
        assert set(row['owner_rows']) <= valid_rows
    assert [x['id'] for x in family if x['id'].startswith('G')] == [f'G{i:02}' for i in range(1, 7)]
    assert providers['prefix-review']['disposition'] == 'approved-bounded-static-capture-provenance-only'
    controls = []

    def reject(name, mutation):
        l, q, e = copy.deepcopy((ledger, queries, loc))
        mutation(l, q, e)
        try:
            guards(l, q, e)
        except (AssertionError, KeyError):
            controls.append(dict(name=name, status='rejected'))
        else:
            raise AssertionError('false promotion accepted: ' + name)

    reject('omit a predecessor bridge', lambda l,q,e: l['frontiers'].pop())
    reject('name becomes actual model/processor identity', lambda l,q,e: l['object_identity_guards'].update(D_equals_P_established=True))
    reject('role flag becomes current public float', lambda l,q,e: l['object_identity_guards'].update(model_role_flag_equals_current_public_float_established=True))
    reject('builder callback becomes processor callback', lambda l,q,e: l['object_identity_guards'].update(registration_builder_equals_callback_processor_established=True))
    reject('equal state offsets prove same receiver', lambda l,q,e: l['object_identity_guards'].update(P_equals_M_established=True))
    reject('owned buffers become host output', lambda l,q,e: l['object_identity_guards'].update(owned_buffers_equal_host_buffers_established=True))
    reject('cross-slice offsets prove equivalence', lambda l,q,e: l['object_identity_guards'].update(architecture_equivalence_established=True))
    reject('static bridge upgraded to closed X route', lambda l,q,e: l['frontiers'][0].update(classification='X', public_bridge_closed=True))
    reject('bounded zero matches prove infeasibility', lambda l,q,e: l['frontiers'][1].update(source_absence_means='infeasible'))
    reject('registration gains indirect credit', lambda l,q,e: l.update(new_indirect_resolution_credit=1))
    reject('prefix approval proves creation', lambda l,q,e: l['prefix_provenance'].update(creation_success_established=True))
    reject('opaque bytes silently decoded', lambda l,q,e: l['prefix_provenance'].update(decoded_bytes=240, opaque_selected_bytes=0))
    reject('successor or callee automatically selected', lambda l,q,e: l.update(selected_successor='0x102231400'))
    reject('invented actual/grade', lambda l,q,e: l['frontiers'][0].update(actual='pass', new_grade='X'))
    for path in HERE.iterdir():
        if path.suffix in {'.json', '.md', '.py'}:
            assert not any(x.rstrip() != x for x in path.read_text().splitlines()), path
    if (HERE / 'manifest.json').is_file():
        for item in read('manifest.json')['files']:
            raw = (HERE / item['path']).read_bytes()
            assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
    print(json.dumps(dict(status='PASS-data-only-whole-frontier', frontier_units=6,
        complete_public_bridges_newly_closed=0, immutable_selected_pins=len(pins['providers']),
        mutable_asof_identities=len(pins['asof_context']), research_prefix_preserved=True,
        C_record_references=74, deduplicated_C_records=73, C_queries=26,
        zero_hit_C_queries=sum(not x['hits'] for x in queries['C_queries']),
        metadata_queries=5, class_slot_query_rows=24, qualified_local_associations=len(loc['observations']),
        false_promotion_controls=controls, original_calls=0, new_binary_bytes=0,
        new_provider_decoder_harness_model_comparator_build_runs=0, new_grades=0,
        new_indirect_resolution_credit=0, selected_successor=None,
        limits='Retained-data inventory only; bounded negative queries are not native absence. No complete public route, outcome denominator, behavioral compatibility or accepted numerical oracle.'), indent=2))


if __name__ == '__main__':
    main()
