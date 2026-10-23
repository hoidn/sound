"""Owner mapping/wording/preservation only: no actual-packet or executable reads."""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def digest(data):
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': digest(data)}


def load(name):
    return json.loads((HERE / name).read_text())


def requirements(text):
    result = []
    for m in re.finditer(r'^### (REQ-MIX-GRAPH-\d{3})[^\n]*\n', text, re.M):
        following = re.search(r'^#{1,3} ', text[m.end():], re.M)
        end = m.end() + following.start() if following else len(text)
        body = text[m.start():end]
        result.append({'id': m[1], 'bytes': len(body.encode()), 'sha256': digest(body), 'start_line': text[:m.start()].count('\n') + 1})
    return result


def case_rows(text):
    return [{'id': m[1], 'bytes': len(m[0].encode()), 'sha256': digest(m[0])}
            for m in re.finditer(r'^\| (MG-\d{3}) \|[^\n]*\n', text, re.M)]


def apply(base, delta, annex):
    assert base.endswith('\n') and annex.startswith('\n')
    for r in delta['replacements']:
        assert base.count(r['old']) == 1
        base = base.replace(r['old'], r['new'], 1)
    return base + annex


def reverse(composed, delta, annex):
    assert composed.endswith(annex)
    text = composed[:-len(annex)]
    for r in reversed(delta['replacements']):
        assert text.count(r['new']) == 1
        text = text.replace(r['new'], r['old'], 1)
    return text


def preserve(base, proposed, before):
    assert len(base.encode()) == before['owner']['bytes'] and digest(base) == before['owner']['sha256']
    # Frontmatter changes do not move requirement start lines.
    assert requirements(base) == requirements(proposed) == before['requirement_bodies']
    old_ids = before['old_case_ids']
    assert case_rows(base) == before['old_case_rows']
    assert [r for r in case_rows(proposed) if r['id'] in old_ids] == before['old_case_rows']
    assert len(requirements(proposed)) == 16 and len(case_rows(proposed)) == 59
    for section in before['protected_sections']:
        if section['heading'] == '## Revision and handoff':
            continue  # Its only permitted edits are checked by exact reversal.
        start = proposed.index(section['heading'] + '\n')
        following = re.search(r'^## ', proposed[start + len(section['heading']):], re.M)
        end = start + len(section['heading']) + following.start() if following else len(proposed)
        body = proposed[start:end]
        assert len(body.encode()) == section['bytes'] and digest(body) == section['sha256']


def mapping(catalog, summary, old_ids):
    rows = catalog['full_catalog_in_source_order']
    points = summary['approved_points']
    assert len(rows) == len(points) == 32 and len({r['logical_id'] for r in rows}) == 32
    assert [r['boolean_bits'] for r in rows] == [list(b) for b in itertools.product((0, 1), repeat=4)] * 2
    assert [r['context'] for r in rows] == ['identity-G'] * 16 + ['nonidentity-G'] * 16
    new = [r for r in rows if 'case_id' in r]
    old = [r for r in rows if 'historical_reference' in r]
    assert catalog['new_case_count'] == len(new) == 25 and catalog['historical_reference_count'] == len(old) == 7
    assert [r['case_id'] for r in new] == [f'MG-{i:03d}' for i in range(42, 67)]
    assert not set(old_ids) & {r['case_id'] for r in new}
    enabled = []
    for i, (r, p) in enumerate(zip(rows, points)):
        assert r['logical_id'] == p['id'] and r['context'] == p['context']
        assert r['boolean_bits'] == p['boolean_bits'] and r['gate_word_indices'] == [0, 1, 2, 8]
        assert r['input_words_u32_hex'] == p['word_u32_hex'] and r['input_hex'] == p['input_hex']
        assert p['tokens'] == ['call', '0x101b40d30', 'buf:8', 'hex:' + r['input_hex'], 'buf:16', 'dump', 'b2', '16']
        assert r['observed_native_b2_hex'] == p['output_hex']
        assert r['portable_expected'] is r['candidate_comparator'] is r['candidate_grade'] is None
        assert r['requirement_context'] == 'REQ-MIX-GRAPH-005'
        assert r['source_catalog_pointer'] == '#/rows/' + str(i)
        assert r['sole_actual_approved_summary_pointer'] == '#/approved_summary/approved_points/' + str(i)
        if 'case_id' in r:
            assert p['provenance'] == 'fresh-once-only'
            assert r['provenance'] == 'fresh-once-only-original-call'
            assert p['predicted_before_call'] is r['expected_prediction_in_immutable_batch'] is None
            assert p['output_hex'] == '00' * 16
            assert r['fresh_receipt_pointer'] == p['receipt_pointer'].removeprefix('results.jsonl')
            assert r['raw_output_payload'] == p['raw_output']
        else:
            assert p['provenance'] == 'inherited-approved-not-reexecuted'
            assert r['provenance'] == 'inherited-approved-historical-output-not-new-call'
            assert r['historical_reference'] == p['inherited_id']
            assert r['fresh_receipt'] is r['new_case_id'] is p['fresh_receipt'] is None
            assert r['historical_provider_pointer'] == p['historical_provider_pointer']
            assert r['copied_approved_projection_pointer'] == p['inherited_projection_pointer'].removeprefix('inherited-controls.json')
            assert 'fresh_receipt_pointer' not in r
            if all(r['boolean_bits'][j] for j in (0, 1, 3)):
                enabled.append({'id': p['id'], 'output_hex': p['output_hex'], 'output_u32_hex': p['output_u32_hex'], 'inherited_id': p['inherited_id']})
    assert enabled == summary['inherited_enabled_outputs'] and len(enabled) == 4


def wording(annex, catalog):
    assert '{ACTUAL_' not in annex
    text = ' '.join(annex.split())
    for required in ['Group tracks remain excluded by Scope.', 'cannot establish MainOn independence',
                     'Every portable expected value, candidate comparator and candidate grade below remains NULL',
                     'existing C-case10⁻⁶ precision is not silently assigned', 'four inherited nonzero enabled pre/post tuples',
                     'X in this annex labels the extracted source of a finite observation', 'Unsupported required behavior remains U']:
        assert required in text
    actual_rows = re.findall(r'^\| (MG-\d{3}) \|[^\n]*$', annex, re.M)
    assert actual_rows == [r['case_id'] for r in catalog['full_catalog_in_source_order'] if 'case_id' in r]
    for r in [r for r in catalog['full_catalog_in_source_order'] if 'case_id' in r]:
        expected = f"| {r['case_id']} | 005 | {'G0' if r['context'] == 'identity-G' else 'G1'} | {''.join(map(str, r['boolean_bits']))} | Four `00000000` words; finite X observation only | NULL | NULL / NULL |"
        assert expected in annex.splitlines()
    for r in [r for r in catalog['full_catalog_in_source_order'] if 'historical_reference' in r]:
        expected = f"| {r['historical_reference']} | {'G0' if r['context'] == 'identity-G' else 'G1'} | {''.join(map(str, r['boolean_bits']))} | `{r['observed_native_b2_hex']}` |"
        assert expected in annex.splitlines()


def check():
    before, delta, catalog, adoption = [load(n) for n in ('owner-before.json', 'owner.delta.json', 'finite-catalog.json', 'adoption-map.json')]
    # Only this approved peer document is read externally for observations.
    report_pin = adoption['actual_review']
    assert pin(report_pin['path']) == report_pin == catalog['sole_actual_review']
    report = json.loads(Path(report_pin['path']).read_text())
    assert report['disposition'] == adoption['actual_disposition'] == 'APPROVED_FINITE_25_FRESH_SEND_GATE_OBSERVATIONS_AND_7_INHERITED_JOINS'
    assert report['blocking_findings'] == report['required_corrections'] == []
    summary = report['approved_summary']
    assert digest(json.dumps(summary, sort_keys=True, separators=(',', ':'))) == adoption['approved_summary_canonical_sha256']
    assert report['frozen_packet'] == adoption['actual_packet_reference_only']
    for a, b in [(catalog['batch_manifest'], report['frozen_packet']['manifest']), (catalog['source_catalog'], summary['catalog_pin'])]:
        assert a['bytes'] == b['bytes'] and a['sha256'] == b['sha256']
        assert a['path'] == str(ROOT / b['path'])
    mapping(catalog, summary, before['old_case_ids'])
    assert adoption['new_ids'] == [r['case_id'] for r in catalog['full_catalog_in_source_order'] if 'case_id' in r]
    assert adoption['batch_manifest'] == catalog['batch_manifest']
    assert delta['base_owner'] == before['owner'] and len(delta['replacements']) == 2
    assert delta['replacements'][0] == {'name': 'revision metadata',
                                     'old': 'updated: 2026-10-19\naccess: analysis\nrevision: 2\n',
                                     'new': 'updated: 2026-10-21\naccess: analysis\nrevision: 3\n'}
    history = delta['replacements'][1]
    assert history['name'] == 'append revision row' and history['old'].startswith('| 2 | 2026-10-19 |')
    assert len(history['old'].splitlines()) == 1 and history['new'].startswith(history['old'] + '| 3 | 2026-10-21 |')
    assert len(history['new'].splitlines()) == 2
    annex = (HERE / delta['append_file']).read_text()
    wording(annex, catalog)
    current = Path(before['owner']['path']).read_text()
    if digest(current) == before['owner']['sha256']:
        base, canonical_state = current, 'unchanged predecessor R2'
    else:
        base, canonical_state = reverse(current, delta, annex), 'exact composed R3 proposal already applied'
    proposed = apply(base, delta, annex)
    assert reverse(proposed, delta, annex) == base
    preserve(base, proposed, before)
    assert case_rows(proposed)[34:] == case_rows(annex)
    rejected = []
    changes = [('missing fresh case', lambda c: c['full_catalog_in_source_order'].pop(0)),
               ('missing inherited reference', lambda c: c['full_catalog_in_source_order'].pop(7)),
               ('reused old ID', lambda c: c['full_catalog_in_source_order'][0].__setitem__('case_id', 'MG-001')),
               ('portable expected promoted', lambda c: c['full_catalog_in_source_order'][0].__setitem__('portable_expected', [0, 0, 0, 0])),
               ('comparator invented', lambda c: c['full_catalog_in_source_order'][0].__setitem__('candidate_comparator', 1e-6)),
               ('new grade', lambda c: c['full_catalog_in_source_order'][0].__setitem__('candidate_grade', 'pass')),
               ('wrong fixed input word', lambda c: c['full_catalog_in_source_order'][0]['input_words_u32_hex'].__setitem__(3, '3f800000')),
               ('wrong native observation', lambda c: c['full_catalog_in_source_order'][0].__setitem__('observed_native_b2_hex', 'ff' * 16)),
               ('wrong approved summary join', lambda c: c['full_catalog_in_source_order'][0].__setitem__('sole_actual_approved_summary_pointer', '#/other')),
               ('reordered class', lambda c: c['full_catalog_in_source_order'].reverse())]
    for name, mutate in changes:
        bad = copy.deepcopy(catalog)
        mutate(bad)
        try:
            mapping(bad, summary, before['old_case_ids'])
        except (AssertionError, KeyError):
            rejected.append(name)
        else:
            raise AssertionError('Bad catalog accepted: ' + name)
    for name, bad in [('erased group exclusion', annex.replace('Group tracks remain excluded by Scope.', '')),
                      ('invented row comparator', annex.replace('| NULL | NULL / NULL |', '| 0 | 1e-6 / pass |', 1))]:
        try:
            wording(bad, catalog)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Bad wording accepted: ' + name)
    for name, bad in [('changed old unresolved case', proposed.replace('| MG-039 | 005 | U |', '| MG-039 | 005 | X |')),
                      ('changed old requirement', proposed.replace('M_main = MainOn', 'M_main = 2 * MainOn', 1)),
                      ('changed old precision', proposed.replace('C cases compare within 10⁻⁶', 'C cases compare within 10⁻³', 1))]:
        try:
            preserve(base, bad, before)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Changed protected owner accepted: ' + name)
    return {'status': 'PASS', 'canonical_state': canonical_state, 'base_owner': before['owner'],
            'proposed_owner_bytes': len(proposed.encode()), 'proposed_owner_sha256': digest(proposed),
            'reversal_exact_predecessor': True, 'unchanged_requirement_bodies': 16, 'unchanged_old_case_rows': 34,
            'new_observation_ids': [r['case_id'] for r in catalog['full_catalog_in_source_order'] if 'case_id' in r], 'total_named_case_observation_ids': 59,
            'historical_references_not_new_cases': 7, 'summary_points_mapped': 32, 'portable_expectations_comparators_grades': None,
            'release_mutations': 0, 'original_calls': 0, 'actual_payload_reads': 0, 'negative_controls': rejected,
            'approved_actual_report': report_pin}


if __name__ == '__main__':
    assert sys.argv[1:] == ['--check']
    print(json.dumps(check(), indent=2))
