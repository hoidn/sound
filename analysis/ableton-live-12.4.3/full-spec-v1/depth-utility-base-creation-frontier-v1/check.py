"""Read-only stdlib verification of four fixed retained C1 projections and scope."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SELECTED = {'0x101aff380', '0x101bc3aa0', '0x10214b954', '0x1023a1004'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name):
    return json.loads((HERE / name).read_text())


def guards(gate, facts, composition, ledger):
    assert gate['metadata_before_expanded_C'] and gate['gate_passed']
    assert set(gate['selection_fixed']) == SELECTED
    assert len(gate['records']) == gate['record_cap'] == 4
    assert gate['expanded_C_total_cap'] == 65536
    assert gate['lines_per_record_cap'] == 500
    assert gate['expanded_C_total'] == 3544 <= 65536
    for rec in gate['records']:
        assert rec['decoded_C_lines_metadata_only'] <= 500
        m = rec['record_metadata']
        assert not m['thunk'] and not m['partial_code'] and not m['timed_out']
        assert m['state'] == 'exported' and m['error'] is None and not m['warnings']
    assert len(facts['roles']) == 4 and len(facts['facts']) == 10
    for role in facts['roles']:
        assert not role['formal_constructor_established']
        assert not role['formal_destructor_established']
        assert not role['actual_public_factory_established']
        assert not role['native_return_register_established']
    for fact in facts['facts']:
        assert fact['native_pc'] is None
        assert not fact['actual_instance_established'] and not fact['public_bridge_established']
    gaps = {x['id']: x for x in facts['projection_gaps']}
    assert gaps['VOID-CONSUMED']['own_C_return'] == 'void'
    assert gaps['VOID-CONSUMED']['caller_consumes_return']
    assert not gaps['VOID-CONSUMED']['native_return_established']
    assert not gaps['VOID-CONSUMED']['implicit_incoming_register_established']
    assert gaps['MODEL-ARG-OMITTED']['own_C_named_arguments'] == 1
    assert gaps['MODEL-ARG-OMITTED']['predecessor_C_named_arguments'] == 0
    assert not gaps['MODEL-ARG-OMITTED']['outer_B_equals_T_established']
    assert gaps['THUNK-EXTRA-ARG']['source_call_arguments'] == 3
    assert gaps['THUNK-EXTRA-ARG']['target_projection_named_arguments'] == 2
    assert not gaps['THUNK-EXTRA-ARG']['native_argument_correspondence_established']
    assert composition['flag_range'] == [0x15f, 0x162]
    starts = [0x168 + 0x18*i for i in range(9)]
    assert composition['member_starts'] == starts
    ranges = [[s, s+19] for s in starts]
    assert composition['member_write_ranges'] == ranges
    assert composition['explicit_store_offsets'] == [[0, 7], [8, 15], [16, 19]]
    a, z = composition['flag_range']
    assert not any(x <= z and y >= a for x, y in ranges)
    assert all(ranges[i][1] < ranges[i+1][0] for i in range(8))
    assert not composition['overlaps_flag'] and composition['member_ranges_pairwise_disjoint']
    assert not composition['public_flag_preserved_established']
    assert [r['id'] for r in ledger['frontiers']] == [f'G{i:02}' for i in range(1, 7)]
    assert ledger['newly_closed_public_bridges'] == 0
    assert ledger['application_outcomes_U'] == 38 and ledger['family_predicates_unchanged'] == 48
    assert not any(ledger['identity_guards'].values())
    for key in ['new_resolved_sites', 'new_native_pc', 'new_original_calls', 'new_binary_bytes']:
        assert ledger[key] == 0
    assert ledger['unknown_not_infeasible'] and ledger['no_new_outcome_denominator']
    assert ledger['selected_successor'] is facts['selected_successor'] is None
    assert facts['unselected_prefix_callees'] == ['0x101ad08a0', '0x102231400']
    for row in ledger['frontiers']:
        assert row['classification'] == 'unknown' and not row['public_bridge_closed']
        assert row['actual_expected'] is row['actual'] is row['comparison'] is row['new_grade'] is None
        assert row['selected_successor'] is None and row['remaining_source_frontier']


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no collection/provider/source expansion/write mode.')
    gate, facts, comp, ledger, pins = [load(n) for n in ['metadata-gate.json',
        'source-facts.json', 'composition.json', 'frontier-ledger.json', 'pins.json']]
    guards(gate, facts, comp, ledger)
    providers = {}
    for pin in pins['providers']:
        path = Path(pin['path'])
        path = path if path.is_absolute() else ROOT / path
        assert path.suffix in {'.json', '.jsonl'}
        raw = path.read_bytes()
        assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], pin['id']
        providers[pin['id']] = raw
    authority = {x['path']: x for x in json.loads(providers['component-inputs'])['decomp_chunk_pins']}
    component_files = {x['path']: x for x in json.loads(providers['component'])['files']}
    assert component_files['class-inputs.json']['sha256'] == sha(providers['component-inputs'])
    assert component_files['packet-inputs.json']['sha256'] == sha(providers['index-authority'])
    class_files = {x['path']: x for x in json.loads(providers['class-predecessor'])['files']}
    for id, name in [('class-selected-records', 'selected-records.jsonl'),
                     ('class-call-associations', 'call-associations.json'), ('class-ledger', 'frontier-ledger.json')]:
        assert class_files[name]['sha256'] == sha(providers[id])
    review = json.loads(providers['class-review'])
    assert review['disposition'] == 'approved-bounded-utility-class-source-frontier'
    rawrows = (HERE / 'selected-records.jsonl').read_bytes().splitlines(keepends=True)
    records = [json.loads(x) for x in rawrows]
    assert len(records) == 4 and {r['entry'] for r in records} == SELECTED
    assert sum(len(r['code'].encode()) for r in records) == 3544
    aliases = next(x for x in json.loads(providers['index-authority'])['retained_indexes_verified']
                   if x['path'] == pins['retained_alias_authority']['path'])
    assert aliases['sha256'] == pins['retained_alias_authority']['sha256']
    assert aliases['bytes'] == pins['retained_alias_authority']['bytes']
    for raw, record, loc in zip(rawrows, records, gate['records']):
        assert record['entry'] == loc['entry']
        assert {k: v for k, v in record.items() if k != 'code'} == loc['record_metadata']
        assert sha(raw) == loc['raw_sha256'] and len(raw) == loc['bytes']
        assert len(record['code'].encode()) == record['code_bytes']
        assert sha(record['code'].encode()) == record['code_sha256']
        assert len(record['code'].splitlines()) == loc['decoded_C_lines_metadata_only']
        assert sum(int(z, 16)-int(a, 16)+1 for a, z in record['body_ranges']) == record['body_bytes']
        assert loc['chunk_pin'] == authority[loc['path']]
        with Path(loc['path']).open('rb') as stream:
            stream.seek(loc['byte_start'])
            assert stream.read(loc['bytes']) == raw
        with Path(loc['alias_path']).open('rb') as stream:
            stream.seek(loc['alias_byte_start'])
            alias_raw = stream.read(loc['alias_bytes'])
        assert sha(alias_raw) == loc['alias_sha256']
        assert json.loads(alias_raw) == loc['alias'] and loc['alias']['entry'] == record['entry']
        assert not loc['alias']['thunk'] and loc['alias']['thunk_target'] is None
    by_entry = {r['entry']: r for r in records}
    predecessors = {r['entry']: r for r in map(json.loads, providers['class-selected-records'].splitlines())}
    for fact in facts['facts']:
        record = records[fact['record_index']]
        assert record['entry'] == fact['entry']
        a, z = fact['code_lines']
        assert sha(''.join(record['code'].splitlines(keepends=True)[a-1:z]).encode()) == fact['span_sha256']
    helper = by_entry['0x101aff380']['code']
    assert '*param_1 = 0;' in helper and 'param_1[1] = 0;' in helper
    assert '*(undefined4 *)(param_1 + 2) = 0;' in helper
    parent = predecessors['0x10215f2b8']['code']
    for start in comp['member_starts']:
        assert f'FUN_101aff380(param_1 + 0x{start:x});' in parent
    assert '*(undefined4 *)(param_1 + 0x15f) = 0;' in parent
    base = by_entry['0x101bc3aa0']['code']
    assert 'void FUN_101bc3aa0(void)' in base and 'return;' in base
    assert 'return puVar2' not in base and 'FUN_101bc3aa0();' in parent
    caller = by_entry['0x10214b954']['code']
    assert 'thunk_FUN_10215f2b8(*(undefined8 *)(lVar2 + 0x18),param_1,param_2);' in caller
    assert 'return lVar2;' in caller
    model = by_entry['0x1023a1004']['code']
    assert 'long FUN_1023a1004(long param_1)' in model and 'return param_1;' in model
    assert 'FUN_1023a1004();' in predecessors['0x102f4fadc']['code']
    call = json.loads(providers['class-call-associations'])['hits'][0]
    assert call['record']['caller'] == '0x10214b954'
    assert call['record']['to'] == '0x10215f3d8'
    assert call['record']['callee_resolved'] == '0x10215f2b8'
    assert predecessors['0x10215f3d8']['thunk']
    assert predecessors['0x10215f3d8']['body_bytes'] == 4
    with Path(json.loads(providers['class-call-associations'])['path']).open('rb') as stream:
        stream.seek(call['byte_start'])
        assert sha(stream.read(call['bytes'])) == call['raw_sha256']
    prior = json.loads(providers['class-ledger'])
    for index, row in enumerate(ledger['frontiers']):
        assert row['predecessor_pointer'] == f'/frontiers/{index}'
        assert prior['frontiers'][index]['id'] == row['id']
        assert prior['frontiers'][index]['classification'] == 'unknown'
    prefix = pins['research_prefix']
    research = (ROOT / prefix['path']).read_bytes()
    assert sha(research[:prefix['bytes']]) == prefix['sha256']
    change = load('research-change.json')
    assert change['prefix'] == prefix and change['append_start_byte'] == prefix['bytes']
    start, size = change['append_start_byte'], change['append_bytes']
    assert sha(research[start:start+size]) == change['append_sha256']
    negatives = []

    def reject(name, mutation):
        g, f, c, l = copy.deepcopy((gate, facts, comp, ledger))
        mutation(g, f, c, l)
        try:
            guards(g, f, c, l)
        except (AssertionError, KeyError):
            negatives.append(dict(name=name, status='rejected'))
        else:
            raise AssertionError('unsafe promotion accepted: ' + name)

    reject('fifth body added', lambda g,f,c,l: g['records'].append(g['records'][0]))
    reject('C byte cap exceeded', lambda g,f,c,l: g.update(expanded_C_total=65537))
    reject('per-record line cap exceeded', lambda g,f,c,l: g['records'][0].update(decoded_C_lines_metadata_only=501))
    reject('metadata gate bypassed', lambda g,f,c,l: g.update(metadata_before_expanded_C=False))
    reject('warning ignored', lambda g,f,c,l: g['records'][0]['record_metadata'].update(warnings=['partial']))
    reject('void projection promoted to native return', lambda g,f,c,l: f['projection_gaps'][0].update(native_return_established=True))
    reject('implicit incoming register assumed', lambda g,f,c,l: f['projection_gaps'][0].update(implicit_incoming_register_established=True))
    reject('model missing argument assumed', lambda g,f,c,l: f['projection_gaps'][1].update(outer_B_equals_T_established=True))
    reject('third caller argument assigned by ABI convention', lambda g,f,c,l: f['projection_gaps'][2].update(native_argument_correspondence_established=True))
    reject('overlapping helper range admitted', lambda g,f,c,l: c['member_write_ranges'][0].__setitem__(0, 0x161))
    reject('source disjointness becomes public flag preservation', lambda g,f,c,l: c.update(public_flag_preserved_established=True))
    reject('base return equated to Q', lambda g,f,c,l: l['identity_guards'].update(B_equals_Q_established=True))
    reject('nearby factory conflated with caller', lambda g,f,c,l: l['identity_guards'].update(caller_equals_nearby_factory_established=True))
    reject('size literal proves allocation success', lambda g,f,c,l: l['identity_guards'].update(allocation_success_established=True))
    reject('source pattern proves formal constructor', lambda g,f,c,l: f['roles'][2].update(formal_constructor_established=True))
    reject('one public bridge closed', lambda g,f,c,l: l['frontiers'][0].update(public_bridge_closed=True))
    reject('source earns native site credit', lambda g,f,c,l: l.update(new_resolved_sites=1))
    reject('unselected x86 prefix callee followed', lambda g,f,c,l: l.update(selected_successor='0x101ad08a0'))
    for path in HERE.iterdir():
        if path.suffix in {'.json', '.jsonl', '.md', '.py'}:
            assert not any(line.rstrip() != line for line in path.read_text().splitlines()), path
    for target in re.findall(r'\]\(([^)]+)\)', (HERE / 'structure.md').read_text()):
        assert (HERE / target.split('#')[0]).is_file(), target
    if (HERE / 'manifest.json').is_file():
        for item in load('manifest.json')['files']:
            raw = (HERE / item['path']).read_bytes()
            assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
    print(json.dumps(dict(status='PASS-fixed-base-creation-source-data-check',
        selected_C_records=4, expanded_C_bytes=3544, max_C_lines=85,
        selected_chunk_pins_verified=4, source_fact_spans=10,
        exact_alias_rows=4, inherited_call_row_verified=1,
        finite_member_write_ranges=9, all_six_bridges='unknown',
        application_outcomes_U=38, family_predicates_unchanged=48,
        new_public_routes=0, new_binary_or_native_reads=0,
        new_original_or_model_or_comparator_calls=0, new_indirect_site_credit=0,
        selected_successor=None, research_prefix_preserved=True,
        false_promotion_controls=negatives,
        limits='Four fixed C projections and selected predecessor data only. No native ABI/return/implicit-register/actual-instance/default/host/lifecycle proof. No entire old source/index/release universe or unrelated body replay.'), indent=2))


if __name__ == '__main__':
    main()
