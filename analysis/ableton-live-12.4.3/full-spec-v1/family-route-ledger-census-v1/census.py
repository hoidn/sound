#!/usr/bin/env python3
"""Retained-document route census. No imports/execution of predecessor tooling."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ROUTES = {'X': 'X', 'X-route': 'X', 'S': 'S', 'S-route': 'S',
          'S-retained-file-only': 'S', 'none': 'none',
          'no-established-route': 'none'}


def load(path):
    return json.loads(path.read_text())


def normalized(value):
    if value not in ROUTES:
        raise ValueError('Unknown required-route spelling: ' + repr(value))
    return ROUTES[value]


def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def counter(rows):
    result = dict.fromkeys(('X', 'S', 'none'), 0)
    for row in rows:
        result[row['route']] += 1
    return result


def overlay(base, patch):
    result = copy.deepcopy(base)
    rows = {r['id']: r for r in result['rows']}
    assert len(rows) == len(result['rows'])
    seen = set()
    allowed = set(patch['allowed_changed_row_fields'])
    assert not allowed.intersection({'route', 'id', 'requirement', 'observable_predicate'})
    for update in patch['row_updates']:
        assert update['id'] not in seen and update['id'] in rows
        seen.add(update['id'])
        assert set(update['set']) <= allowed
        rows[update['id']].update(update['set'])
    result['contexts'].update(patch['context_updates'])
    for key, values in patch['auxiliary_dependency_updates'].items():
        result['auxiliary_dependencies'][key].update(values)
    assert [r['route'] for r in result['rows']] == [r['route'] for r in base['rows']]
    return result


def predicate_join(ledger, family):
    """Required predicates have one application/file context; D12 is annotation."""
    predicates = ledger['predicates']
    ids = [p['id'] for p in predicates]
    assert len(set(ids)) == len(ids)
    joined, annotations = {}, collections.defaultdict(list)
    for i, context in enumerate(ledger['contexts']):
        pid = context['predicate_id']
        assert pid in ids
        if context['route'] == 'no-established-exact-target-route':
            if family == 'sample-instruments':
                assert context['source_annotation_not_extra_outcome'] is True
            else:
                assert context['record_kind'] == 'source-evidence-annotation'
            annotations[pid].append('/contexts/' + str(i))
        else:
            if family == 'sample-instruments':
                assert context['source_annotation_not_extra_outcome'] is False
            else:
                assert context['record_kind'] == 'required-observable-context'
            assert pid not in joined
            normalized(context['route'])
            joined[pid] = (i, context)
    assert set(joined) == set(ids)
    assert all(len(v) == 1 for v in annotations.values())
    return joined, annotations


def synth():
    controls = []
    def reject(name, action):
        try:
            action()
        except (AssertionError, ValueError, KeyError):
            controls.append(name)
        else:
            raise AssertionError('Control was accepted: ' + name)
    assert normalized('X-route') == 'X' and normalized('S-retained-file-only') == 'S'
    assert normalized('none') == 'none'
    for value in (None, 'U', 'no-established-exact-target-route', 'S-retained-fixture-only', 'X-ish'):
        reject('reject-required-route-' + repr(value), lambda v=value: normalized(v))
    data = {'predicates': [{'id': 'P'}], 'contexts': [
        {'predicate_id': 'P', 'route': 'no-established-exact-target-route', 'record_kind': 'source-evidence-annotation'},
        {'predicate_id': 'P', 'route': 'S', 'record_kind': 'required-observable-context'}]}
    joined, annotation = predicate_join(data, 'dynamics')
    assert len(joined) == 1 and len(annotation) == 1
    for name, change in (
        ('duplicate-required-context', lambda j: j['contexts'].append(copy.deepcopy(j['contexts'][1]))),
        ('missing-required-context', lambda j: j['contexts'].pop()),
        ('dangling-predicate', lambda j: j['contexts'][1].update(predicate_id='Q')),
        ('documentary-as-required', lambda j: j['contexts'][0].update(route='S')),
        ('missing-route', lambda j: j['contexts'][1].pop('route'))):
        changed = copy.deepcopy(data)
        change(changed)
        reject(name, lambda j=changed: predicate_join(j, 'dynamics'))
    # Contexts/auxiliary arrays never implicitly become required rows.
    assert counter([{'route': 'none'}]) == {'X': 0, 'S': 0, 'none': 1}
    base = {'rows': [{'id': 'A', 'route': 'X', 'context': 'old'}], 'contexts': {}, 'auxiliary_dependencies': {'AUX': {}}}
    patch = {'allowed_changed_row_fields': ['context'], 'row_updates': [{'id': 'A', 'set': {'context': 'corrected'}}], 'context_updates': {}, 'auxiliary_dependency_updates': {}}
    assert overlay(base, patch)['rows'][0]['route'] == 'X' and base['rows'][0]['context'] == 'old'
    for name, change in (
        ('overlay-route-mutation', lambda j: j['row_updates'][0]['set'].update(route='S')),
        ('overlay-missing-id', lambda j: j['row_updates'][0].update(id='B')),
        ('overlay-duplicate-id', lambda j: j['row_updates'].append(copy.deepcopy(j['row_updates'][0])))):
        changed = copy.deepcopy(patch)
        change(changed)
        reject(name, lambda p=changed: overlay(base, p))
    return {'negative_controls': len(controls), 'names': controls, 'positive_checks': ['known route spellings', 'one required context plus one documentary annotation', 'auxiliary never added by default', 'overlay preserves route and base']}


def derive():
    selection = load(HERE / 'selection.json')['families']
    pins = load(HERE / 'source-pins.json')['pins']
    pinned = {p['path']: p for p in pins}
    mutable = []
    for p in pins:
        actual = pin(ROOT / p['path'])
        if p['kind'] == 'immutable':
            assert all(actual[k] == p[k] for k in ('bytes', 'sha256')), p['path']
        else:
            mutable.append({'path': p['path'], 'as_of': {k: p[k] for k in ('bytes', 'sha256')}, 'current': actual,
                            'equal': all(actual[k] == p[k] for k in ('bytes', 'sha256'))})
    authorities = load(HERE / 'authority-snapshots.json')['authorities']
    for authority in authorities:
        raw = authority['text'].encode()
        assert len(raw) == authority['bytes'] and hashlib.sha256(raw).hexdigest() == authority['sha256']
    atlas = next(a['text'] for a in authorities if a['path'].endswith('program-structure.md'))
    atlas_names = set(re.findall(r'full-spec-v1/(family-[a-z0-9-]+-routes-v[0-9]+)/structure.md', atlas))
    atlas_names.remove('family-analog-routes-v1')
    assert len(selection) == 32 and {Path(e['directory']).name for e in selection} == atlas_names
    assert len({e['family'] for e in selection}) == 32
    assert next(e for e in selection if e['family'] == 'warp')['directory'].endswith('v2')
    all_rows, families = [], []
    for entry in selection:
        directory = entry['directory']
        manifest_path, ledger_path = directory + '/manifest.json', directory + '/route-ledger.json'
        manifest, ledger = load(ROOT / manifest_path), load(ROOT / ledger_path)
        declared = next(f for f in manifest['files'] if f['path'] == 'route-ledger.json')
        assert all(declared[k] == pinned[ledger_path][k] for k in ('bytes', 'sha256'))
        effective_path, patch = ledger_path, None
        if entry['family'] == 'analog':
            patch = ledger
            effective_path = patch['base_ledger']['path']
            assert all(patch['base_ledger'][k] == pinned[effective_path][k] for k in ('bytes', 'sha256'))
            assert all(patch['predecessor_manifest'][k] == pinned[patch['predecessor_manifest']['path']][k] for k in ('bytes', 'sha256'))
            base_manifest = load(ROOT / patch['predecessor_manifest']['path'])
            base_declared = next(f for f in base_manifest['files'] if f['path'] == 'route-ledger.json')
            assert all(base_declared[k] == pinned[effective_path][k] for k in ('bytes', 'sha256'))
            ledger = overlay(load(ROOT / effective_path), patch)
        array = entry['required_array']
        joined, annotations = predicate_join(ledger, entry['family']) if array == 'predicates' else ({}, {})
        rows = []
        for i, row in enumerate(ledger[array]):
            pointer = '/' + array + '/' + str(i)
            if array == 'predicates':
                ci, route_row = joined[row['id']]
                route_pointer = '/contexts/' + str(ci) + '/route'
                raw = route_row['route']
            else:
                route_pointer = pointer + '/' + entry['route_field']
                raw = row[entry['route_field']]
            unit = {'family': entry['family'], 'id': row['id'], 'required_pointer': pointer,
                    'route_pointer': route_pointer, 'raw_route': raw, 'route': normalized(raw),
                    'requirement': row.get('requirement', row.get('requirements'))}
            unit['qualifier_field_pointers'] = [pointer + '/' + key for key in row
                if any(term in key for term in ('missing_join', 'premis', 'unknown', 'unresolved', 'grade', 'binding', 'enumeration', 'qualification'))]
            if array == 'predicates':
                unit['qualifier_field_pointers'] += ['/contexts/' + str(ci) + '/' + key for key in route_row
                    if any(term in key for term in ('missing_join', 'premis', 'unknown', 'unresolved', 'grade', 'binding', 'enumeration', 'qualification'))]
            if annotations.get(row['id']):
                unit['excluded_annotation_pointers'] = annotations[row['id']]
            if patch:
                matched = [j for j, update in enumerate(patch['row_updates']) if update['id'] == row['id']]
                if matched:
                    unit['overlay_pointer'] = '/row_updates/' + str(matched[0])
            rows.append(unit)
        assert len({r['id'] for r in rows}) == len(rows)
        counts = counter(rows)
        assert counts == entry['canonical_counts_crosscheck'], entry['family']
        # Preserve all explicit gap/auxiliary/exclusion declarations without counting them.
        extra = {k: v for k, v in ledger.items() if any(t in k for t in ('auxiliary', 'unresolved', 'enumeration', 'excluded', 'cross_reference', 'collapsed'))}
        contract = {k: v for k, v in ledger.items() if not isinstance(v, list) and any(t in k for t in ('unit', 'count', 'scope', 'required', 'revision', 'denominator'))}
        omitted = {k: {'records': len(v), 'reason': 'Route witnesses for selected predicates plus documentary annotations; not separate inventory units.' if array == 'predicates' and k == 'contexts' else 'Not selected by this family declared required-unit contract; navigation/source/auxiliary context, not extra required units.',
                       'raw_route_counts_not_additive': dict(collections.Counter(str(r.get('route', r.get('route_class', 'NO-ROUTE-FIELD'))) for r in v if isinstance(r, dict)))}
                   for k, v in ledger.items() if isinstance(v, list) and k != array}
        f = {**entry, 'counts': counts, 'required_units': len(rows),
             'manifest': pinned[manifest_path], 'ledger': pinned[ledger_path],
             'required_rows_source': pinned[effective_path], 'required_json_pointer': '/' + array,
             'route_field': entry['route_field'], 'context_join': array == 'predicates',
             'excluded_documentary_annotations': sum(map(len, annotations.values())),
             'declared_contract': contract, 'excluded_arrays': omitted, 'gap_auxiliary_exclusion_declarations': extra}
        if patch:
            f['effective_cut'] = 'Frozen base plus exactly ten permitted context/history updates; all241 routes inherit base. Current R2 is NOT re-enumerated.'
            f['overlay_route_counts'] = patch['inheritance_assertions']['counts_inventory_only']
        families.append(f)
        all_rows.extend(rows)
    fixture_path = next(p for p in pinned if p.endswith('family-sample-instruments-routes-v1/fixture-routes.json'))
    fixtures = load(ROOT / fixture_path)
    assert len(fixtures['records']) == fixtures['auxiliary_S_records'] == 5
    assert all(r['counts_as_required_predicate'] is False for r in fixtures['records'])
    fm = load(ROOT / str(Path(fixture_path).parent / 'manifest.json'))
    fd = next(f for f in fm['files'] if f['path'] == 'fixture-routes.json')
    assert all(fd[k] == pinned[fixture_path][k] for k in ('bytes', 'sha256'))
    delta_path = next(p for p in pinned if p.endswith('analog-owner-r2-anrmap001/route-delta.json'))
    delta = load(ROOT / delta_path)
    assert delta['predecessor_contexts']['map_v2_manifest'] == next(f for f in families if f['family'] == 'analog')['manifest']['sha256']
    priority = sorted(families, key=lambda f: (-f['counts']['X'], f['family']))
    return {'schema': 'whole-32-family-required-route-census-v1',
            'status': 'PROPOSAL; pending independent review; no shared edits or automatic batch selection',
            'totals': counter(all_rows), 'total_heterogeneous_inventory_units': len(all_rows),
            'unit_limit': 'Mixed bounded predicates/contexts and whole-clause bundles, with historical owner cuts. Sum is inventory bookkeeping only; not atomic denominator, fraction, current-owner completeness, behavior grade or public binding.',
            'indirect_sites_separate': {'export_baseline': 25071, 'conditional_overlay': 24, 'combined': 25095, 'site_universe': 268015, 'new_credit': 0, 'basis': 'authority-snapshots.json program-structure.md lines66–83; inherited, not recounted here'},
            'priority_proposal': [{'rank': i + 1, 'family': f['family'], 'X': f['counts']['X'], 'owner_scope': f['owner_scope'], 'batch_automatically_selected': False} for i, f in enumerate(priority)],
            'priority_ties': 'Equal X counts ordered lexicographically by family solely for stable presentation; no semantic tie-break/admission. 1X bundled-parameters/structure-als tie; all0X parked under amendment.',
            'families': families, 'sample_fixture_auxiliary': {'source': pinned[fixture_path], 'pointer': '/records', 'records': 5, 'required_credit': 0},
            'analog_current_owner_delta': {'source': pinned[delta_path], 'content': delta},
            'mutable_authorities_current_comparison': mutable,
            'fresh_scope': 'Own strict document identity checks, schema-specific required-route extraction, per-row joins/counts/sort and synthetic controls. No source-body semantics re-audit; prior family approvals/source semantics inherited explicitly. No paths nested in evidence opened.'}, all_rows


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


if __name__ == '__main__':
    assert len(sys.argv) == 2 and sys.argv[1] in ('--build', '--check')
    tests = synth()
    census, units = derive()
    payloads = {'census.json': encode(census), 'required-units.jsonl': ''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in units).encode()}
    if sys.argv[1] == '--build':
        for name, raw in payloads.items():
            (HERE / name).write_bytes(raw)
    else:
        # Mutable current comparisons can legitimately advance; the as-of snapshot remains exact.
        prior = load(HERE / 'census.json')
        for value in (prior, census):
            value.pop('mutable_authorities_current_comparison')
        assert prior == census
        assert (HERE / 'required-units.jsonl').read_bytes() == payloads['required-units.jsonl']
    print(json.dumps({'status': 'PASS', 'mode': sys.argv[1], 'families': 32, 'required_units': len(units), 'routes': counter(units), 'synthetic': tests, 'new_source_or_original_execution': 0}))
