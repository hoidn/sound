"""Read-only stdlib integrity/scope check; no inherited imports or source execution."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name):
    return json.loads((HERE / name).read_text())


def guards(ledger, census, history):
    assert ledger['required_predicate_count'] == len(ledger['predicates']) == 271
    assert ledger['bounded_context_count'] == len(ledger['contexts']) == 413
    assert len(ledger['requirements']) == 62 and len(ledger['case_navigation']) == 153
    assert len({p['id'] for p in ledger['predicates']}) == 271
    assert len({r['id'] for r in ledger['contexts']}) == 413
    assert ledger['route_inventory_units'] == {'required_predicates': 271,
        'application_predicates_no_established_route': 251,
        'retained_file_predicates_S': 20,
        'documentary_annotations_not_extra_outcomes': 142,
        'total_context_records': 413}
    assert collections.Counter(r['route'] for r in ledger['contexts']) == {'S': 20, 'no-established-route': 251, 'no-established-exact-target-route': 142}
    predicates = {p['id']: p for p in ledger['predicates']}
    assert {p for r in ledger['requirements'] for p in r['predicate_ids']} == set(predicates)
    assert not ledger['outcome_grade_claim'] and not ledger['whole_product_denominator']
    assert ledger['helper_only_records_are_auxiliary']
    assert ledger['new_X_routes'] == ledger['new_public_routes'] == ledger['new_native_site_credit'] == 0
    assert ledger['selected_successor'] is None
    contexts = collections.defaultdict(list)
    for row in ledger['contexts']:
        p = predicates[row['predicate_id']]
        assert row['requirement'] == p['requirement'] and row['device'] == p['device']
        assert row['native_PC_basis'] is row['actual'] is row['comparison'] is row['new_grade'] is None
        contexts[p['id']].append(row['context'])
        if row['context'] == 'target-application':
            assert row['route'] == 'no-established-route' and row['route_basis'] == 'U-APP'
            assert row['target_applicability'] == 'unknown' and row['missing_joins']
        elif row['context'] == 'documentary':
            assert row['route'] == 'no-established-exact-target-route'
            assert row['route_basis'] == 'D12-SOURCE-ONLY' and row['documentary_evidence'] == 'D12'
            assert row['record_kind'] == 'source-evidence-annotation' and row['missing_joins']
        else:
            assert row['route'] == 'S' and not row['missing_joins'] and row['route_basis'] == 'S-PKG'
            assert row['target_applicability'] == 'not claimed'
        assert row['is_extra_required_predicate'] is False
    for p in predicates.values():
        expected = ['documentary', 'target-application'] if p['source_provenance'] == 'D12' else ['retained-file'] if p['source_provenance'] == 'Dpkg' else ['target-application']
        assert contexts[p['id']] == expected
        assert p['numeric_examples_are_context_not_extra_predicates']
    assert census['selected_table_count'] == census['caps']['tables'] == 32
    assert census['selected_slots'] == 88 <= census['caps']['selected_slots'] == 512
    assert census['available_exported_prefix_slots'] == 784 and census['omitted_exported_prefix_slots'] == 696
    assert census['selected_counts'] == {'table-prefix': 32, 'store-candidate': 26, 'alias': 337, 'membership': 22}
    assert census['combined_alias_membership'] == 359 <= census['caps']['combined_alias_membership'] == 512
    assert census['combined_call_indirect_rows'] == 48 <= census['caps']['combined_call_indirect'] == 512
    assert census['selected_counts']['store-candidate'] <= census['caps']['stores'] == 128
    assert census['unresolved_selected_indirect'] == 2
    assert not census['complete_native_classes'] and not census['source_body_or_abi_roles_established']
    assert census['new_C_bodies_read'] == census['new_native_or_binary_reads'] == census['new_resolved_site_credit'] == 0
    assert history['source_blocks'] == len(history['block_locators']) == 123
    assert len(history['new_histories']) == 24 and history['source_groups'] == 20
    assert history['current_cases'] == 153 and history['original_cases_exact'] == 129
    assert history['case_provenance_counts'] == {'D12': 47, 'Dpkg': 5, 'U': 101}
    assert not history['pixels_and_link_destinations_inspected'] and not history['full_chapter_claim']
    assert history['source_capture_utc'] is None and history['actual_results'] == 0
    for row in history['new_histories']:
        assert row['documentary_expected'] is row['documentary_comparison'] is None
        assert row['actual_expected'] is row['actual_comparison'] is row['new_grade'] is None
        assert row['target'] == 'U' and not row['executed']


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Only read-only --check; no collect/decode/provider/model/write mode.')
    ledger, census, history, pins = [load(n) for n in ['route-ledger.json', 'query-census.json', 'history-scope.json', 'pins.json']]
    guards(ledger, census, history)
    providers = {}
    for pin in pins['providers']:
        path = ROOT / pin['path']
        assert path.suffix in {'.json', '.md', '.html'}
        raw = path.read_bytes()
        assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], pin['id']
        providers[pin['id']] = raw
    assert json.loads(providers['owner-review'])['disposition'] == 'approved-partial'
    assert json.loads(providers['audit-review'])['disposition'] == 'approved-partial-source-audit'
    owner_manifest = json.loads(providers['owner-manifest'])
    owner_files = {r['path']: r for r in owner_manifest['payloads']}
    for pin in pins['providers']:
        if pin['path'] in owner_files:
            assert pin['sha256'] == owner_files[pin['path']]['sha256']
    audit_manifest = json.loads(providers['audit-manifest'])
    assert audit_manifest['files']['audit.json']['sha256'] == sha(providers['audit'])
    assert next(x for x in owner_manifest['canonical_snapshots'] if x['snapshot'] == 'spec-r2.md')['sha256'] == sha(providers['owner-snapshot'])
    req = json.loads(providers['requirements'])
    cases = json.loads(providers['cases'])
    old = json.loads(providers['old-cases'])
    assert len(req) == 62 and len(cases) == 153 and len(old) == 129
    assert cases[:129] == old
    owner_lines = providers['owner-snapshot'].decode().splitlines()
    byreq = {r['id']: r for r in req}
    clause = load('clause-index.json')
    assert clause['requirements'] == ledger['requirements']
    assert clause['current_owner_sha256'] == sha(providers['owner-snapshot'])
    assert {r['id'] for r in ledger['requirements']} == set(byreq)
    for p in ledger['predicates']:
        source = p['source_owner']
        i = int(source['json_pointer'].split('/')[1])
        r = req[i]
        assert r['id'] == p['requirement'] and r['device'] == p['device']
        assert sha(r['text'].encode()) == source['requirement_body_sha256']
        a, z = p['source_text_chars']
        assert r['text'][a:z] == p['source_anchor']
        assert r['text'] in owner_lines[source['body_lines'][0]-1]
        assert owner_lines[source['heading_line']-1].startswith('### ' + r['id'] + ' ')
        assert p['source_provenance'] == r['provenance']
        assert p['case_navigation'] == [c['id'] for c in cases if c['requirement'] == r['id']]
    for nav, case in zip(ledger['case_navigation'], cases):
        raw = (json.dumps(case, sort_keys=True, separators=(',', ':')) + '\n').encode()
        assert nav['id'] == case['id'] and nav['requirement'] == case['requirement']
        assert sha(raw) == nav['object_canonical_sha256']
        assert cases[int(nav['source_pointer'][1:])]['id'] == nav['id']
        assert nav['new_grade'] is nav['actual'] is None
    oldids = {c['id'] for c in old}
    assert {x['id'] for x in history['new_histories']} == {c['id'] for c in cases if c['id'] not in oldids}
    adoption = json.loads(providers['adoption'])
    for row in history['new_histories']:
        case = cases[int(row['case_pointer'][1:])]
        assert row['id'] == case['id']
        assert case.get('documentary_expected') is case.get('documentary_comparison') is None
        for group in row['groups']:
            g = adoption['groups'][int(group['adoption_pointer'].split('/')[-1])]
            assert row['id'] in g['new_cases'] and group['id'] == g['id']
    audit = json.loads(providers['audit'])
    html = providers['manual-html'].decode()
    assert len(audit['blocks']) == 123 and len(audit['proposals']) == 20
    for loc, block in zip(history['block_locators'], audit['blocks']):
        assert loc['id'] == block['id'] and loc['raw_start'] == block['raw_start']
        assert sha(block['text'].encode()) == loc['text_sha256']
        assert sha(block['raw_html'].encode()) == loc['raw_html_sha256']
        assert html[loc['raw_start']:loc['raw_end']] == block['raw_html']
    for r in req:
        for evidence in r['evidence']:
            file, blockid = evidence.split('#')
            if file.startswith('manual-'):
                blocks = json.loads(providers[file.removesuffix('-blocks.json')])
                assert any(x['locator'] == blockid for x in blocks)
    schemas = json.loads(providers['schema-fields'])
    packages = json.loads(providers['package-values'])
    expected_classes = {'Compressor2': 1381, 'Gate': 2630, 'GlueCompressor': 2670,
                        'Limiter': 3754, 'MultibandDynamics': 5279}
    assert {s['class']: s['line'] for s in schemas} == expected_classes
    assert {x['class'] for x in packages} == set(expected_classes)
    for package in packages:
        assert package['locator'] == '/Ableton/' + package['class']
        assert package['root_attributes']['Creator'] == 'Ableton Live 12.4d1'
        assert package['root_attributes']['MinorVersion'] == '12.0_12402'
        schema = next(s for s in schemas if s['class'] == package['class'])
        assert schema['fields'] and package['fields']
    md = [json.loads(l) for l in (HERE / 'metadata-rows.jsonl').read_text().splitlines()]
    calls = [json.loads(l) for l in (HERE / 'call-rows.jsonl').read_text().splitlines()]
    assert collections.Counter(x['kind'] for x in md) == census['selected_counts']
    assert len(calls) == 48 and sum(x['kind'] == 'indirect' for x in calls) == 2
    selected_paths = {x['path'] for x in pins['selected_metadata_authority']}
    components = json.loads(providers['component'])
    component_files = {x['path']: x for x in components['files']}
    index = {x['path']: x for x in json.loads(providers['index-authority'])['retained_indexes_verified']}
    for authority in pins['selected_metadata_authority']:
        source = index[authority['path']] if authority['path'] in index else component_files[Path(authority['path']).name]
        assert source['sha256'] == authority['sha256'] and source['bytes'] == authority['bytes']
    model = set(census['root_selected_model_encodings'])
    proc = set(census['root_selected_processor_encodings'])
    points = set()
    slots = 0
    for item in md + calls:
        loc = item['locator']
        assert loc['path'] in selected_paths
        path = Path(loc['path'])
        path = path if path.is_absolute() else ROOT / path
        with path.open('rb') as stream:
            stream.seek(loc['byte_start'])
            raw = stream.read(loc['bytes'])
        assert sha(raw) == loc['raw_sha256']
        original = json.loads(raw)
        if item['kind'] == 'table-prefix':
            rec = item['record']
            n = original['literal_type_encoding']
            assert n in model | proc
            assert rec['slots'] == (original['slots'] if n in proc else original['slots'][:3])
            assert rec['available_exported_prefix_slots'] == len(original['slots'])
            assert rec['selection'] == ('whole-exported-processor-prefix' if n in proc else 'leading-three-or-less-model-construction-lifetime-frontier')
            assert not rec['complete_class_or_processing_slots_established'] and not rec['public_instance_established']
            assert rec['native_table_extent'] is None
            points.add(rec['address_point'])
            slots += len(rec['slots'])
        else:
            assert item['record'] == original
        if item['kind'] == 'indirect':
            assert original['resolved_targets'] == []
    assert len(points) == 32 and slots == 88
    edges = load('chain-edges.json')
    assert edges['new_native_site_credit'] == edges['actual_device_routes'] == 0
    assert not edges['unreviewed_FilterEQ_map_dependency']
    assert edges['selected_successor'] is None
    research = pins['research_change']
    raw = (ROOT / research['path']).read_bytes()
    prefix = raw[:research['prefix_bytes_after_date_update']]
    assert sha(prefix) == research['prefix_sha256_after_date_update']
    restored = prefix.replace(b'updated: 2026-10-20', b'updated: 2026-10-19', 1)
    assert sha(restored) == research['original_prefix_sha256']
    start, size = research['append_start_byte'], research['append_bytes']
    assert sha(raw[start:start+size]) == research['append_sha256']
    negatives = []

    def reject(name, change):
        l, c, h = copy.deepcopy((ledger, census, history))
        change(l, c, h)
        try:
            guards(l, c, h)
        except (AssertionError, KeyError):
            negatives.append(dict(name=name, status='rejected'))
        else:
            raise AssertionError('unsafe mutation accepted: ' + name)

    reject('required predicate omitted', lambda l,c,h: l['predicates'].pop())
    reject('numeric example becomes another outcome', lambda l,c,h: l['contexts'].append(l['contexts'][0]))
    reject('D12 source promoted to exact-target S', lambda l,c,h: next(r for r in l['contexts'] if r['context']=='documentary').update(route='S'))
    reject('documentary and target contexts collapsed', lambda l,c,h: l['contexts'][1].update(context='documentary'))
    reject('metadata names prove complete class', lambda l,c,h: c.update(complete_native_classes=True))
    reject('arbitrary larger slot window substituted', lambda l,c,h: c.update(selected_slots=512))
    reject('alias membership cap exceeded', lambda l,c,h: c.update(combined_alias_membership=513))
    reject('call frontier cap exceeded', lambda l,c,h: c.update(combined_call_indirect_rows=513))
    reject('unresolved indirect silently resolved', lambda l,c,h: c.update(unresolved_selected_indirect=0))
    reject('new history gets invented oracle', lambda l,c,h: h['new_histories'][0].update(actual_expected=0))
    reject('metadata gains native site credit', lambda l,c,h: c.update(new_resolved_site_credit=1))
    reject('source figures treated as inspected pixels', lambda l,c,h: h.update(pixels_and_link_destinations_inspected=True))
    for target in re.findall(r'\]\(([^)]+)\)', (HERE / 'structure.md').read_text()):
        assert (HERE / target.split('#')[0]).is_file(), target
    for path in HERE.iterdir():
        if path.suffix in {'.json', '.jsonl', '.md', '.py'}:
            assert not any(line.rstrip() != line for line in path.read_text().splitlines()), path
    if (HERE / 'manifest.json').is_file():
        for f in load('manifest.json')['files']:
            raw = (HERE / f['path']).read_bytes()
            assert len(raw) == f['bytes'] and sha(raw) == f['sha256']
    print(json.dumps(dict(status='PASS-bounded-dynamics-family-data-check', requirements=62,
        required_predicates=271, total_context_records=413, documentary_annotations_no_exact_target_route=142,
        retained_file_S=20, target_no_established_route=251, X=0,
        cases=153, preserved_old_cases=129, new_null_histories=24,
        inherited_audit_blocks=123, tables=32, selected_slots=88,
        available_prefix_slots=784, omitted_prefix_slots=696, stores=26,
        aliases=337, memberships=22, method_seeds=22, call_rows=46,
        unresolved_indirect_rows=2, selected_provider_pins=len(pins['providers']),
        new_native_site_credit=0, new_public_routes=0, new_original_calls=0,
        no_new_body_or_native_read=True, research_body_preserved_except_date=True,
        negative_controls=negatives,
        checked_scope='Current clause/case/source pointers and selected metadata rows/declared pins. Audit semantics/RTTI/index recovery inherited. No provider/native/model/comparator/fixture/old-helper or whole release/predecessor replay.'), indent=2))


if __name__ == '__main__':
    main()
