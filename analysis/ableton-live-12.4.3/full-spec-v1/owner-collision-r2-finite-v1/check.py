#!/usr/bin/env python3
"""Owner preservation and finite-adoption joins only, no actual re-review or original calls."""
import copy
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads(path.read_text())


def pinned(pin):
    raw = (ROOT / pin['path']).read_bytes()
    assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], pin['path']
    return json.loads(raw)


def bodies(text):
    headings = list(re.finditer(r'^### (REQ-DEVICE-COLLISION-\d{3})[^\n]*\n', text, re.M))
    return {m[1]: text[m.start():headings[i + 1].start() if i + 1 < len(headings)
                      else text.index('## Proposed comparison metric')] for i, m in enumerate(headings)}


def preserve(text, delta, baseline):
    assert 'revision: 2\n' in text and 'status: draft\n' in text
    assert len(text.encode()) == delta['current']['bytes'] and sha(text.encode()) == delta['current']['sha256']
    old = text
    for op in reversed(delta['operations_in_forward_order']):
        assert old.count(op['after']) == 1
        old = old.replace(op['after'], op['before'], 1)
    assert len(old.encode()) == baseline['predecessor']['bytes'] and sha(old.encode()) == baseline['predecessor']['sha256']
    previous, current = bodies(old), bodies(text)
    assert len(current) == 18
    for b in baseline['requirement_bodies']:
        assert len(previous[b['id']].encode()) == b['bytes'] and sha(previous[b['id']].encode()) == b['sha256']
        assert current[b['id']].startswith(previous[b['id']])
        if b['id'] != 'REQ-DEVICE-COLLISION-017':
            assert current[b['id']] == previous[b['id']]
    rows = [row for row in text.splitlines() if re.match(r'^\| DCL-\d{3} \|', row)]
    assert len(rows) == 62
    assert [row.split('|')[1].strip() for row in rows] == [f'DCL-{i:03d}' for i in range(1, 63)]
    for row, pin in zip(rows[:50], baseline['old_case_rows']):
        assert len(row.encode()) == pin['bytes'] and sha(row.encode()) == pin['sha256']
    assert sha(text[text.index('## Proposed comparison metric'):text.index('## Acceptance cases')].encode()) == baseline['old_proposed_comparison_metric_sha256']
    assert sha(text[text.index('## Open questions and handoff'):text.index('## Analyst evidence appendix')].encode()) == baseline['old_open_questions_section_sha256']
    return {'old_body_prefixes_exact': 18, 'other_whole_bodies_exact': 17, 'old_case_rows_exact': 50,
            'current_case_rows_IDs': 62, 'old_proposed_metric_and_open_questions_exact': True,
            'reverse_reconstructed_predecessor': baseline['predecessor']}


def mapping(catalog, documents, review):
    assert catalog['approved_actual_review'] is not None
    assert review['blocking_findings'] == []
    assert review['disposition'].startswith('APPROVED')
    assert catalog['approved_actual_review']['disposition'] == review['disposition']
    # Exact actual manifest association is supplied by the reviewed report, not re-derived from raw audio.
    assert catalog['approved_actual_review']['manifest'] == catalog['source_authorities']['batch-manifest']
    packet = review['exact_packet']
    assert {'path': packet['path'] + '/manifest.json', 'bytes': packet['manifest_bytes'],
            'sha256': packet['manifest_sha256']} == catalog['source_authorities']['batch-manifest']
    assert catalog['approved_actual_review']['nonblocking_qualifications'] == review['nonblocking_qualifications']
    assert catalog['approved_actual_review']['handoff'] == review['handoff']
    assert catalog['observation_re_reviewed_here'] is False
    assert catalog['canonical_unedited_while_actual_review_pending'] is True
    records = catalog['records']
    assert len(records) == 12 and [r['id'] for r in records] == [f'DCL-{i:03d}' for i in range(51, 63)]
    inp, obs, captures = documents['batch-inputs'], documents['batch-observations'], documents['batch-results']
    for i, (row, source, observation, capture) in enumerate(zip(records, inp['inputs'], obs['observations'], captures['children'])):
        assert row['source_history_id'] == source['id'] == observation['id'] == capture['id']
        assert row['requirement'] == 'REQ-DEVICE-COLLISION-017'
        assert row['input'] == source and row['finite_reference_observation'] == observation
        assert row['input_ref'] == {'source': 'batch-inputs', 'pointer': f'/inputs/{i}'}
        assert row['observation_ref'] == {'source': 'batch-observations', 'pointer': f'/observations/{i}'}
        assert row['capture_ref'] == {'source': 'batch-results', 'pointer': f'/children/{i}'}
        assert row['pre_run_prediction'] is row['candidate_comparator'] is row['candidate_grade'] is row['public_A1_A2_or_ARM_result'] is None
        assert row['evidence'] == 'X: approved finite supplied-host reference observation; candidate criterion unresolved'
    lookup = {row['source_history_id']: row['id'] for row in records}
    assert len(catalog['relations']) == 8
    for i, (relation, source) in enumerate(zip(catalog['relations'], obs['comparisons'])):
        assert relation['id'] == f'COLLISION-ENABLE-PAIR-{i + 1:03d}'
        assert relation['kind'] == 'finite comparison relation, not a new case'
        assert relation['transition_case'] == lookup[source['transition']]
        assert relation['matched_control_case'] == lookup[source['matched_no_setter_control']]
        assert relation['observation'] == source
        assert relation['observation_ref'] == {'source': 'batch-observations', 'pointer': f'/comparisons/{i}'}
        assert relation['pre_run_prediction'] is relation['portable_candidate_criterion'] is None
    assert catalog['counts'] == {'old_case_IDs': 50, 'new_case_IDs': 12, 'current_case_IDs': 62,
                                 'new_control_history_cases': 4, 'new_transition_history_cases': 8,
                                 'pair_relations_not_cases': 8, 'requirements': 18}
    return {'exact_new_history_joins': 12, 'new_control_history_cases': 4,
            'new_transition_history_cases': 8, 'pair_relations_not_cases': 8,
            'approved_observation_review_inherited': True}


def reject(name, callback):
    try:
        callback()
    except (AssertionError, KeyError, IndexError):
        return {'name': name, 'rejected': True}
    raise AssertionError('negative accepted: ' + name)


def main():
    c = load(HERE / 'case-catalog.json')
    delta, baseline = load(HERE / 'owner.delta.json'), load(HERE / 'predecessor.json')
    text = (ROOT / delta['current']['path']).read_text()
    documents = {name: pinned(pin) for name, pin in c['source_authorities'].items()}
    review = pinned(c['approved_actual_review'])
    preservation = preserve(text, delta, baseline)
    joins = mapping(c, documents, review)
    negatives = []
    for name, mutate in [
        ('omit-control-history', lambda d: d['records'].pop(0)),
        ('reuse-old-case-ID', lambda d: d['records'][0].update(id='DCL-050')),
        ('change-R2-enable-word', lambda d: d['records'][0]['input']['parameter_tokens'].__setitem__(58, '1.0')),
        ('change-event-coordinate', lambda d: d['records'][0]['input']['events'][0].__setitem__(0, 4096)),
        ('invent-candidate-waveform-criterion', lambda d: d['records'][0].update(candidate_comparator='exact raw SHA')),
        ('invent-public-law', lambda d: d['records'][0].update(public_A1_A2_or_ARM_result='pass')),
        ('lose-tiny-difference', lambda d: d['relations'][2]['observation']['post_setter_second_segment'].update(max_abs_difference=0.0)),
        ('promote-pair-to-case', lambda d: d['counts'].update(current_case_IDs=70)),
        ('rewritten-history-prediction', lambda d: d['records'][0].update(pre_run_prediction='silent'))]:
        altered = copy.deepcopy(c)
        mutate(altered)
        negatives.append(reject(name, lambda: mapping(altered, documents, review)))
    negatives.append(reject('old-U-promotion', lambda: preserve(text.replace('| DCL-048 | 017 | U |', '| DCL-048 | 017 | X |'), delta, baseline)))
    negatives.append(reject('proposed-metric-change', lambda: preserve(text.replace('≤ 10⁻¹⁸', '≤ 10⁻¹⁷', 1), delta, baseline)))
    print(json.dumps({'status': 'PASS', 'preservation': preservation, 'mapping': joins,
                      'negative_controls': negatives, 'negative_control_count': len(negatives),
                      'scope': 'Data-only wording/preservation/adoption joins, no observation re-review, raw-audio recomparison, original or model execution.'}, indent=2))


if __name__ == '__main__':
    main()
