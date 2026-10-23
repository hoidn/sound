"""Read-only stdlib check of fixed retained C records and class-source scope."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SELECTED = {'0x10215f2b8', '0x10215f3d8', '0x102f4fadc',
            '0x10216412c', '0x10216416c', '0x101aa4b90'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name):
    return json.loads((HERE / name).read_text())


def pointer(value, path):
    for key in path.split('/')[1:]:
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def guards(gate, census, facts, ledger):
    assert gate['metadata_before_expanded_C'] is True
    assert set(gate['selection_fixed']) == SELECTED
    assert len(gate['records']) == 6 and gate['record_cap'] == 6
    assert gate['expanded_C_total_cap'] == 32768 and gate['lines_per_record_cap'] == 300
    assert gate['expanded_C_total'] == 3198 <= gate['expanded_C_total_cap']
    for item in gate['records']:
        assert item['decoded_C_lines_metadata_only'] <= 300
    thunk = next(x for x in gate['records'] if x['entry'] == '0x10215f3d8')
    assert thunk['alias']['thunk'] and thunk['alias']['thunk_target'] == '0x10215f2b8'
    assert thunk['record_metadata']['thunk'] and thunk['record_metadata']['body_bytes'] == 4
    assert census['table_count'] == 5 and census['prefix_slot_count'] == 87
    assert census['store_match_count'] == 3 <= census['store_match_cap'] == 128
    assert census['native_table_extent_established'] is census['class_instances_counted'] is False
    assert census['new_indirect_resolution_credit'] == 0
    assert len(facts['roles']) == 6 and len(facts['facts']) == 8
    for role in facts['roles']:
        assert role['formal_constructor_established'] is False
        assert role['formal_destructor_established'] is False
        assert role['independent_native_implementation_claim'] is False
    for item in facts['facts']:
        assert item['native_pc'] is None and item['actual_instance_established'] is False
        assert item['public_default_established'] is False
    assert [x['id'] for x in ledger['frontiers']] == [f'G{i:02}' for i in range(1, 7)]
    assert ledger['newly_closed_public_bridges'] == 0 and ledger['application_outcomes_U'] == 38
    assert ledger['family_predicates_unchanged'] == 48
    assert not any(ledger['identity_guards'].values())
    assert ledger['unknown_not_infeasible'] and ledger['no_new_outcome_denominator']
    for key in ['new_resolved_sites', 'new_native_pc', 'new_original_calls', 'new_binary_bytes']:
        assert ledger[key] == 0
    assert ledger['selected_successor'] is None
    for item in ledger['frontiers']:
        assert item['classification'] == 'unknown' and item['public_bridge_closed'] is False
        assert item['actual_expected'] is item['actual'] is item['comparison'] is item['new_grade'] is None
        assert item['selected_successor'] is None and item['remaining_source_frontier']


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no source/provider/collection/write mode.')
    pins, gate, census, facts, ledger, calls = [load(n) for n in ['pins.json',
        'metadata-gate.json', 'class-census.json', 'source-facts.json',
        'frontier-ledger.json', 'call-associations.json']]
    providers = {}
    for item in pins['providers']:
        path = Path(item['path'])
        path = path if path.is_absolute() else ROOT / path
        assert path.suffix in {'.json', '.jsonl'}
        raw = path.read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256'], item['id']
        providers[item['id']] = raw
    guards(gate, census, facts, ledger)
    chunk_authority = {x['path']: x for x in json.loads(providers['component-inputs'])['decomp_chunk_pins']}
    raw_records = (HERE / 'selected-records.jsonl').read_bytes().splitlines(keepends=True)
    records = [json.loads(x) for x in raw_records]
    assert len(records) == 6 and {x['entry'] for x in records} == SELECTED
    assert sum(x['code_bytes'] for x in records) == 3198
    by_entry = {x['entry']: x for x in records}
    for index, (raw, rec, meta, loc) in enumerate(zip(raw_records, records, gate['records'], gate['source_locators'])):
        assert rec['entry'] == meta['entry'] == loc['entry']
        assert {k: v for k, v in rec.items() if k != 'code'} == meta['record_metadata']
        assert sha(raw) == loc['sha256'] == meta['raw_sha256'] and len(raw) == loc['bytes']
        assert rec['code_bytes'] == len(rec['code'].encode())
        assert rec['code_sha256'] == sha(rec['code'].encode())
        assert len(rec['code'].splitlines()) == meta['decoded_C_lines_metadata_only'] <= 300
        assert sum(int(z, 16) - int(a, 16) + 1 for a, z in rec['body_ranges']) == rec['body_bytes']
        assert loc['chunk_pin'] == chunk_authority[loc['path']]
        with Path(loc['path']).open('rb') as stream:
            stream.seek(loc['byte_start'])
            assert stream.read(loc['bytes']) == raw
        alias_path = Path(pins['retained_source_index_authority']['aliases.jsonl']['path'])
        with alias_path.open('rb') as stream:
            stream.seek(meta['alias_byte_start'])
            alias_raw = stream.read(meta['alias_bytes'])
        assert sha(alias_raw) == meta['alias_sha256'] and json.loads(alias_raw) == meta['alias']
        assert meta['alias']['thunk'] == rec['thunk']
    # Expanded thunk source has the same block but remains a four-byte metadata thunk.
    assert by_entry['0x10215f3d8']['code'].split('{', 1)[1] == by_entry['0x10215f2b8']['code'].split('{', 1)[1]
    assert sum(not r['thunk'] for r in records) == ledger['actual_units']['nonthunk_records'] == 5
    for item in facts['facts']:
        rec = records[item['record_index']]
        assert rec['entry'] == item['entry']
        a, z = item['code_lines']
        assert sha(''.join(rec['code'].splitlines(keepends=True)[a-1:z]).encode()) == item['span_sha256']
    table_rows = []
    for loc in census['table_rows'] + census['store_rows']:
        with (ROOT / loc['path']).open('rb') as stream:
            stream.seek(loc['byte_start'])
            raw = stream.read(loc['bytes'])
        assert sha(raw) == loc['raw_sha256']
        obj = json.loads(raw)
        assert obj['address_point'] == loc['address_point']
        if 'prefix_slot_count' in loc:
            assert len(obj['slots']) == loc['prefix_slot_count']
            assert obj['literal_type_encoding'] == loc['literal_type_encoding']
            assert obj['native_table_extent'] is None
            table_rows.append(obj)
        else:
            assert obj['entry'] == loc['entry']
            assert by_entry[obj['entry']]['code_sha256'] == loc['code_sha256']
    model = {x['address_point']: x['offset_to_top'] for x in table_rows if x['literal_type_encoding'] == '11AStereoGain'}
    assert model == {'0x1068ae7f8': 0, '0x1068aedc0': -80,
                     '0x1068aedf8': -88, '0x1068aee70': -440}
    assert [0, 10*8, 0xb*8, 0x37*8] == [-x for x in model.values()]
    assert len(calls['hits']) == 4 <= calls['match_cap'] == 128
    for loc in calls['hits']:
        with Path(calls['path']).open('rb') as stream:
            stream.seek(loc['byte_start'])
            raw = stream.read(loc['bytes'])
        assert sha(raw) == loc['raw_sha256'] and json.loads(raw) == loc['record']
    prior = json.loads(providers['prior-bridge-ledger'])
    for row in ledger['frontiers']:
        assert pointer(prior, row['predecessor_pointer'])['id'] == row['id']
    assert json.loads(providers['prior-review'])['disposition'] == 'approved-bounded-utility-public-binding-static-frontier'
    prefix = pins['research_prefix']
    research = (ROOT / prefix['path']).read_bytes()
    assert sha(research[:prefix['bytes']]) == prefix['sha256']
    change = load('research-change.json')
    assert change['prefix'] == prefix and change['append_start_byte'] == prefix['bytes']
    start = change['append_start_byte']
    assert sha(research[start:start + change['append_bytes']]) == change['append_sha256']
    negatives = []

    def reject(name, mutation):
        g, c, f, l = copy.deepcopy((gate, census, facts, ledger))
        mutation(g, c, f, l)
        try:
            guards(g, c, f, l)
        except (AssertionError, KeyError):
            negatives.append(dict(name=name, status='rejected'))
        else:
            raise AssertionError('unsafe promotion accepted: ' + name)

    reject('seventh source record admitted', lambda g,c,f,l: g['records'].append(g['records'][0]))
    reject('expanded C byte cap exceeded', lambda g,c,f,l: g.update(expanded_C_total=32769))
    reject('per-record line cap exceeded', lambda g,c,f,l: g['records'][0].update(decoded_C_lines_metadata_only=301))
    reject('metadata gate skipped', lambda g,c,f,l: g.update(metadata_before_expanded_C=False))
    reject('expanded thunk counted as independent implementation', lambda g,c,f,l: f['roles'][2].update(independent_native_implementation_claim=True))
    reject('table prefix becomes complete native table', lambda g,c,f,l: c.update(native_table_extent_established=True))
    reject('vptr store becomes proved constructor', lambda g,c,f,l: f['roles'][1].update(formal_constructor_established=True))
    reject('deleting pattern becomes formal destructor contract', lambda g,c,f,l: f['roles'][4].update(formal_destructor_established=True))
    reject('base return equated to incoming receiver', lambda g,c,f,l: l['identity_guards'].update(B_equals_Q_established=True))
    reject('dynamic vptr continuity assumed', lambda g,c,f,l: l['identity_guards'].update(dynamic_vptr_continuity_established=True))
    reject('local zero store becomes public default', lambda g,c,f,l: f['facts'][1].update(public_default_established=True))
    reject('public bridge promoted', lambda g,c,f,l: l['frontiers'][0].update(public_bridge_closed=True))
    reject('new native/site credit invented', lambda g,c,f,l: l.update(new_resolved_sites=1))
    reject('encountered caller automatically selected', lambda g,c,f,l: l.update(selected_successor='0x10214b954'))
    for path in HERE.iterdir():
        if path.suffix in {'.json', '.jsonl', '.md', '.py'}:
            assert not any(x.rstrip() != x for x in path.read_text().splitlines()), path
    for target in re.findall(r'\]\(([^)]+)\)', (HERE / 'structure.md').read_text()):
        assert (HERE / target.split('#')[0]).is_file(), target
    if (HERE / 'manifest.json').is_file():
        for item in load('manifest.json')['files']:
            raw = (HERE / item['path']).read_bytes()
            assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
    print(json.dumps(dict(status='PASS-fixed-class-source-data-check',
        tables=5, prefix_slots=87, store_candidates=3, selected_C_records=6,
        expanded_C_bytes=3198, max_C_lines=38, nonthunk_records=5,
        selected_chunk_pins_verified=4, source_fact_spans=8, retained_call_rows_verified=4,
        all_six_bridges='unknown', new_public_routes=0, new_binary_or_native_reads=0,
        new_original_or_model_or_comparator_calls=0, new_indirect_site_credit=0,
        selected_successor=None, research_prefix_preserved=True,
        false_promotion_controls=negatives,
        limits='Selected retained source/metadata only. Calls verified by exact retained row locators; no fresh complete call-index or old frontier replay in this checker. No current ABI/class instance/vptr continuity/public defaults/behavior or table/function completeness.'), indent=2))


if __name__ == '__main__':
    main()
