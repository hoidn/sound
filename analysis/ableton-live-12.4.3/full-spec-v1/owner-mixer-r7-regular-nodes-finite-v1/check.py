"""Summary-only owner mapping/preservation; no experiment or source/raw replay."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def identity(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': sha(data)}


def canonical_hash(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':')))


def load(name):
    return json.loads((HERE / name).read_text())


def requirements(text):
    result = {}
    for m in re.finditer(r'^### (REQ-MIXER-VALUES-\d{3})[^\n]*\n', text, re.M):
        following = re.search(r'^#{1,3} ', text[m.end():], re.M)
        end = m.end() + following.start() if following else len(text)
        result[m[1]] = text[m.start():end]
    return result


def case_rows(text):
    return [{'id': m[1], 'bytes': len(m[0].encode()), 'sha256': sha(m[0])}
            for m in re.finditer(r'^\| (MV-\d{3}) \|[^\n]*\n', text, re.M)]


def preserve_objects(objects, recorded):
    assert [{'id': x.get('id', x.get('case_id')), 'canonical_sha256': canonical_hash(x)} for x in objects] == recorded


def replacements(delta):
    result = []
    for r in delta['replacements']:
        new = (HERE / r['new_prefix_file']).read_text() + r['new_suffix'] if 'new_prefix_file' in r else r['new']
        result.append((r['old'], new))
    return result


def apply(base, delta, annex):
    for old, new in replacements(delta):
        assert base.count(old) == 1
        base = base.replace(old, new, 1)
    assert base.endswith('\n') and annex.startswith('\n')
    return base + annex


def reverse(proposed, delta, annex):
    assert proposed.endswith(annex)
    text = proposed[:-len(annex)]
    for old, new in reversed(replacements(delta)):
        assert text.count(new) == 1
        text = text.replace(new, old, 1)
    return text


def preserve(base, proposed, before, req_append):
    assert len(base.encode()) == before['owner']['bytes'] and sha(base) == before['owner']['sha256']
    old, new = requirements(base), requirements(proposed)
    assert len(old) == len(new) == 15
    assert [{'id': key, 'bytes': len(body.encode()), 'sha256': sha(body)} for key, body in old.items()] == before['requirement_bodies']
    for key in old:
        assert new[key] == old[key] + (req_append if key == 'REQ-MIXER-VALUES-014' else '')
    assert case_rows(base) == case_rows(proposed) == before['old_case_rows'] and len(case_rows(proposed)) == 48
    for section in before['protected_sections']:
        if section['heading'] == '## Revision and handoff':
            continue
        start = proposed.index(section['heading'] + '\n')
        following = re.search(r'^## ', proposed[start + len(section['heading']):], re.M)
        end = start + len(section['heading']) + following.start() if following else len(proposed)
        body = proposed[start:end]
        assert len(body.encode()) == section['bytes'] and sha(body) == section['sha256']


def mapping(catalog, points, r6_cases):
    rows = catalog['points']
    assert len(rows) == len(points) == 903 and len({r['logical_id'] for r in rows}) == 903
    assert [(r['curve'], r['i'], r['k']) for r in rows] == [(curve, i, i - 64) for curve in range(7) for i in range(129)]
    prior = {(r['input']['curve'], r['input']['position_binary32_hex']): r['id'] for r in r6_cases}
    keys = ['curve', 'i', 'k', 'function', 'token', 'input_bits32', 'output_bits32', 'output_class', 'sign', 'provenance', 'precall_expected', 'portable_comparator']
    new_ids, inherited, overlap = [], [], []
    for i, (r, p) in enumerate(zip(rows, points)):
        assert r['logical_id'] == p['id'] and all(r[k] == p[k] for k in keys)
        assert r['approved_summary_pointer'] == '#/reviewed_points/' + str(i)
        assert r['portable_expected'] is r['portable_comparator'] is r['candidate_grade'] is None
        assert re.fullmatch('[0-9a-f]{8}', r['input_bits32']) and re.fullmatch('[0-9a-f]{8}', r['output_bits32'])
        assert r['existing_r6_case_id'] == prior.get((r['curve'], r['input_bits32']))
        if p['provenance'] == 'fresh-selected':
            assert p['fresh'] is not None and p['inherited'] is None
            assert r['precall_expected'] is None and r['existing_r6_case_id'] is None
            assert r['case_id'] == f'MV-{301 + len(new_ids):03d}'
            new_ids.append(r['case_id'])
        else:
            assert p['provenance'] == 'inherited-approved' and p['inherited'] is not None and p['fresh'] is None
            assert r['case_id'] is None
            inherited.append(r['logical_id'])
            if r['existing_r6_case_id']:
                overlap.append(r['existing_r6_case_id'])
    assert len(new_ids) == 826 and len(inherited) == 77 and len(overlap) == 28
    assert catalog['counts'] == {'logical': 903, 'new_case_ids': 826, 'historical_references_no_new_ids': 77, 'old_draft_ids_unchanged': 300, 'new_total_named_ids': 1126}
    return new_ids, inherited, overlap


def wording(req_append, annex, catalog, curves):
    joined = ' '.join((req_append + annex).split())
    for phrase in ['Each fresh pre-call expectation remains NULL.',
                   'Portable expected values, comparators and candidate grades remain NULL',
                   'not per-child before records', 'does not read or prove a current 129-point runtime table',
                   'These are input/case inventory counts, not atomic required-outcome coverage',
                   'No current receiver, per-track ramp/audio/public delivery, ARM/Apple equivalence',
                   'no original execution', 'negative reference and its precision limitations remain exact']:
        assert phrase in joined
    assert 'cases903.json' in req_append and 'mixer-regular-knots-v1-review.json' in annex
    for curve in curves:
        cases = [r['case_id'] for r in catalog['points'] if r['curve'] == curve['curve'] and r['case_id']]
        expected = f"| {curve['curve']} | `{curve['function']}` / {curve['name']} | {cases[0]}–{cases[-1]} | 118 / 11 |"
        assert expected in annex.splitlines()
    assert len(re.findall(r'^\| [0-6] \|', annex, re.M)) == 7


def check():
    before, delta, catalog, adoption = [load(n) for n in ('owner-before.json', 'owner.delta.json', 'cases903.json', 'adoption-map.json')]
    # Peer summary and existing owner/release objects only; no current actual payload reads.
    report_pin = adoption['actual_review']
    assert identity(report_pin['path']) == report_pin == catalog['sole_actual_review']
    report = json.loads(Path(report_pin['path']).read_text())
    assert report['disposition'] == adoption['actual_disposition'] == 'APPROVED_826_FRESH_FINITE_SCALAR_OBSERVATIONS_AND_77_INHERITED_JOINS'
    assert report['blocking_findings'] == report['required_corrections'] == [] and report['source_pin_window'].startswith('CLEAR')
    points = report['reviewed_points']
    assert canonical_hash(points) == adoption['reviewed_points_canonical_sha256']
    assert catalog['actual_manifest_reference_only'] == adoption['actual_manifest_reference_only'] == report['manifest']
    assert identity(before['r6_cases_file']['path']) == before['r6_cases_file']
    r6 = json.loads(Path(before['r6_cases_file']['path']).read_text())['cases']
    assert len(r6) == 252
    preserve_objects(r6, before['r6_case_objects'])
    assert identity(before['released_cases_file']['path']) == before['released_cases_file']
    released = json.loads(Path(before['released_cases_file']['path']).read_text())['cases']
    assert len(released) == 80
    preserve_objects(released, before['released_case_objects'])
    new_ids, inherited, overlap = mapping(catalog, points, r6)
    assert overlap == adoption['matched_existing_r6_ids'] and len(overlap) == adoption['historical_pairs_already_in_r6'] == 28
    assert adoption['new_pairs_already_in_r6'] == 0
    assert delta['base_owner'] == before['owner'] and len(delta['replacements']) == 3
    assert delta['replacements'][0] == {'name': 'revision metadata', 'old': 'updated: 2026-10-21\naccess: analysis\nrevision: 6\n', 'new': 'updated: 2026-10-21\naccess: analysis\nrevision: 7\n'}
    middle = delta['replacements'][1]
    assert middle == {'name': 'REQ014 append before REQ015', 'old': '### REQ-MIXER-VALUES-015 — out-of-range and alternative stored values\n', 'new_prefix_file': 'req014-append.md', 'new_suffix': '### REQ-MIXER-VALUES-015 — out-of-range and alternative stored values\n'}
    last = delta['replacements'][2]
    assert last['name'] == 'revision row append' and last['old'].startswith('| 6 | 2026-10-21 |') and len(last['old'].splitlines()) == 1
    assert last['new'].startswith(last['old'] + '| 7 | 2026-10-21 |') and len(last['new'].splitlines()) == 2
    req_append, annex = [(HERE / name).read_text() for name in ('req014-append.md', 'annex-append.md')]
    wording(req_append, annex, catalog, report['finite_universe']['per_curve'])
    current = Path(before['owner']['path']).read_text()
    if sha(current) == before['owner']['sha256']:
        base, state = current, 'unchanged predecessor R6'
    else:
        base, state = reverse(current, delta, annex), 'exact composed R7 proposal already applied'
    proposed = apply(base, delta, annex)
    assert reverse(proposed, delta, annex) == base
    preserve(base, proposed, before, req_append)
    rejected = []
    changes = [('omit point', lambda c: c['points'].pop()),
               ('duplicate logical point', lambda c: c['points'].__setitem__(1, c['points'][0])),
               ('reordered grid', lambda c: c['points'].reverse()),
               ('wrong helper', lambda c: c['points'][1].__setitem__('function', '0x1')),
               ('changed input word', lambda c: c['points'][1].__setitem__('input_bits32', '00000000')),
               ('changed native output', lambda c: c['points'][1].__setitem__('output_bits32', 'ffffffff')),
               ('wrong summary pointer', lambda c: c['points'][1].__setitem__('approved_summary_pointer', '#/other')),
               ('reused old case ID', lambda c: c['points'][1].__setitem__('case_id', 'MV-049')),
               ('inherited point given new ID', lambda c: c['points'][0].__setitem__('case_id', 'MV-301')),
               ('portable expected invented', lambda c: c['points'][1].__setitem__('portable_expected', '3f800000')),
               ('portable comparator invented', lambda c: c['points'][1].__setitem__('portable_comparator', 1e-6)),
               ('new grade', lambda c: c['points'][1].__setitem__('candidate_grade', 'pass')),
               ('fresh NULL oracle overwritten', lambda c: c['points'][1].__setitem__('precall_expected', '3f800000')),
               ('old expectation erased', lambda c: c['points'][0].__setitem__('precall_expected', None))]
    for name, mutate in changes:
        bad = copy.deepcopy(catalog)
        mutate(bad)
        try:
            mapping(bad, points, r6)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Bad owner mapping accepted: ' + name)
    for name, bad in [('R6 object mutation', copy.deepcopy(r6)), ('released object mutation', copy.deepcopy(released))]:
        bad[0]['owner_proposal_mutation'] = True
        try:
            preserve_objects(bad, before['r6_case_objects'] if name.startswith('R6') else before['released_case_objects'])
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Changed object accepted')
    for name, bad in [('changed old U row', proposed.replace('| MV-034 | 011 |', '| MV-034 | 014 |', 1)),
                      ('changed runtime interpolation clause', proposed.replace('with linear interpolation', 'with nonlinear interpolation', 1)),
                      ('changed native precision limit', proposed.replace('glibc, ±1 ulp vs Apple', 'glibc, exact vs Apple', 1))]:
        try:
            preserve(base, bad, before, req_append)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Changed protected owner accepted: ' + name)
    for name, bad in [('custody overstated', annex.replace('not per-child before records', 'per-child before records')),
                      ('runtime table caveat erased', annex.replace('does not read\nor prove a current 129-point runtime table', 'proves a current 129-point runtime table'))]:
        try:
            wording(req_append, bad, catalog, report['finite_universe']['per_curve'])
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Bad wording accepted: ' + name)
    return {'status': 'PASS', 'canonical_state': state, 'base_owner': before['owner'],
            'proposed_owner_bytes': len(proposed.encode()), 'proposed_owner_sha256': sha(proposed),
            'exact_predecessor_reversal': True, 'other_requirement_bodies_unchanged': 14,
            'old_REQ014_text_unchanged_before_append': True, 'old_table_rows_unchanged': 48,
            'R6_case_objects_unchanged': 252, 'released_case_objects_unchanged': 80,
            'new_case_ids': len(new_ids), 'first_new_id': new_ids[0], 'last_new_id': new_ids[-1],
            'new_total_named_ids': 1126, 'historical_references_no_new_ids': len(inherited),
            'historical_refs_already_in_R6': len(overlap), 'fresh_pairs_already_in_R6': 0,
            'approved_summary_points_mapped': 903, 'portable_expected_comparator_grade': None,
            'negative_controls': rejected, 'actual_payload_reads': 0, 'original_calls': 0,
            'approved_actual_report': report_pin}


if __name__ == '__main__':
    assert sys.argv[1:] == ['--check']
    print(json.dumps(check(), indent=2))
