#!/usr/bin/env python3
"""Check adoption joins and preservation; never re-run/re-review observations."""
import copy
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def load(path):
    return json.loads(path.read_text())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def at(value, pointer):
    for part in pointer.split('/')[1:]:
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def validate_aliases(catalog):
    rows = catalog['cases']
    assert len(rows) == 28
    assert [r['id'] for r in rows] == ['DAN-' + str(i).zfill(3) for i in range(48, 76)]
    assert all(r['kind'] == 'X-finite' and r['comparison_grade'] is None and r['portable_waveform_metric'] is None for r in rows)
    assert [r['source_case'] for r in rows[:8]] == ['CTRL-' + str(i).zfill(2) for i in range(1, 9)]
    assert all(r['requirements'] == ['REQ-DEVICE-ANALOG-022'] for r in rows[:8])
    assert all(r['requirements'] == ['REQ-DEVICE-ANALOG-016', 'REQ-DEVICE-ANALOG-021'] for r in rows[8:])
    assert {(r['mode_change']['host_index'], r['mode_change']['host_value']) for r in rows[8:]} == {
        (i, v) for i in (89, 101, 172, 184) for v in (1, 2, 3)} | {(i, 1) for i in (90, 91, 102, 103, 173, 174, 185, 186)}
    assert sum(r['expected_finite_observation']['difference_from_control']['byte_identical'] for r in rows[8:]) == 16
    assert catalog['baseline_control']['existing_case'] == 'DAN-028'
    assert catalog['baseline_control']['not_a_new_case'] is True
    for r in rows:
        review_pin = r['observation_review']['pin']
        raw = (ROOT / review_pin['path']).read_bytes()
        assert len(raw) == review_pin['bytes'] and sha(raw) == review_pin['sha256']
        review = json.loads(raw)
        reviewed_row = at(review, r['observation_review']['pointer'])
        assert reviewed_row.get('id', reviewed_row.get('control_id')) == r['source_case']
        if r in rows[:8]:
            assert review['disposition'] == 'approved-bounded-ungraded-actual-results' and review['findings'] == []
        else:
            assert review['disposition'] == 'APPROVED-BOUNDED-ACTUAL-EXTRACTED-BATCH-EVIDENCE'
            assert review['blocking_findings'] == [] and review['required_corrections'] == []
        source = r['observation_source']['pin']
        raw = (ROOT / source['path']).read_bytes()
        assert len(raw) == source['bytes'] and sha(raw) == source['sha256']
        value = at(json.loads(raw), r['observation_source']['pointer'])
        if r in rows[:8]:
            assert value['id'] == r['source_case']
            for key in ('first_numeric_difference', 'prechange_byte_identity', 'prechange_numeric_identity'):
                assert r['expected_finite_observation'][key] == value['measurement'][key]
        else:
            assert value['id'] == r['source_case']
            assert r['expected_finite_observation']['output'] == value['observed_output']
            assert r['expected_finite_observation']['difference_from_control'] == value['observed_difference_from_same_batch_baseline']
            assert r['expected_finite_observation']['capture_end_censored'] == (value['observed_output']['last_nonzero_frame'] == 44099)
            assert r['expected_finite_observation']['last_nonzero_is_capture_statistic_not_voice_end'] is True
            assert r['output_reference']['sha256'] == value['output_sha256']
            assert r['parameter_vector_sha256'] == value['input_vector_sha256']


def main():
    before = load(HERE / 'predecessor.json')
    delta = load(HERE / 'owner.delta.json')
    catalog = load(HERE / 'case-aliases.json')
    text = (ROOT / before['predecessor']['path']).read_text()
    reversed_text = text
    for op in reversed(delta['operations']):
        if op.get('position') == 'end':
            assert reversed_text.endswith(op['after'])
            reversed_text = reversed_text[:-len(op['after'])]
        else:
            assert reversed_text.count(op['after']) == 1, op['scope']
            reversed_text = reversed_text.replace(op['after'], op['before'])
    assert len(reversed_text.encode()) == before['predecessor']['bytes']
    assert sha(reversed_text.encode()) == before['predecessor']['sha256']
    starts = list(re.finditer(r'^### (REQ-DEVICE-ANALOG-\d{3})[^\n]*\n', text, re.M))
    assert [m.group(1) for m in starts] == before['required_ids']
    bodies = {m.group(1): text[m.start():starts[i + 1].start() if i + 1 < len(starts) else text.index('## Timing and state')]
              for i, m in enumerate(starts)}
    for b in before['requirement_bodies']:
        if b['id'] not in before['allowed_changed_requirement_bodies']:
            assert sha(bodies[b['id']].encode()) == b['sha256'] and len(bodies[b['id']].encode()) == b['bytes']
    prefix = bodies['REQ-DEVICE-ANALOG-022'].split('  **X, finite observations adopted in revision 3.**')[0]
    assert sha(prefix.encode()) == before['approved_R2_withdrawal_guard']['REQ022_prefix_before_discovery_sha256']
    rows = [line for line in text.splitlines() if line.startswith('| DAN-')]
    assert len(rows) == 67
    current = {r.split('|')[1].strip(): r for r in rows}
    assert len(current) == 67
    for r in before['case_rows']:
        assert sha(current[r['id_label']].encode()) == r['sha256']
    validate_aliases(catalog)
    negatives = []
    for name, change in (
        ('missing-finite-case', lambda c: c['cases'].pop()),
        ('duplicate-ID', lambda c: c['cases'][1].update(id=c['cases'][0]['id'])),
        ('drop-unchanged-mode', lambda c: c['cases'].pop(8)),
        ('portable-tolerance-invented', lambda c: c['cases'][0].update(portable_waveform_metric='100ms')),
        ('baseline-counted-new', lambda c: c['baseline_control'].update(not_a_new_case=False)),
        ('window-tail-overclaim', lambda c: c['cases'][15]['expected_finite_observation'].update(capture_end_censored=False))):
        value = copy.deepcopy(catalog)
        change(value)
        try:
            validate_aliases(value)
        except AssertionError:
            negatives.append(name)
        else:
            raise AssertionError('Control accepted: ' + name)
    return {'status': 'PASS', 'predecessor_reconstructed_exactly': True, 'unchanged_other_bodies': 20,
            'REQ022_withdrawal_prefix_exact': True, 'old_case_rows_exact': 39, 'old_case_IDs': 47,
            'new_finite_case_IDs': 28, 'current_case_IDs': 75, 'history_pairs': 8, 'mode_vectors': 20,
            'baseline_control_not_new_case': True, 'author_negative_controls': negatives,
            'scope': 'Mechanical adoption/preservation only; prior observation reviews inherited; no original/raw output recomparison or new model execution.'}


if __name__ == '__main__':
    print(json.dumps(main()))
