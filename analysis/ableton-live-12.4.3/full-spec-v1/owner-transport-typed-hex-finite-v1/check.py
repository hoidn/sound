#!/usr/bin/env python3
"""Read-only owner preservation and adoption joins; no original execution or FP decoding."""
import copy
import hashlib
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads(path.read_text())


def pinned(pin):
    raw = (ROOT / pin['path']).read_bytes()
    assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], pin['path']
    return json.loads(raw)


def pointer(document, address):
    value = document
    for token in address.lstrip('/').split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def bodies(text):
    headings = list(re.finditer(r'^### (REQ-TRANSPORT-STATE-\d{3})[^\n]*\n', text, re.M))
    return {m[1]: text[m.start():headings[i + 1].start() if i + 1 < len(headings)
                      else text.index('## Timing and state')]
            for i, m in enumerate(headings)}


def preservation(text, delta, predecessor):
    assert 'revision: 6\n' in text and 'status: draft\n' in text
    assert sha(text.encode()) == delta['current']['sha256']
    before = text
    for change in reversed(delta['operations_in_forward_order']):
        assert before.count(change['after']) == 1
        before = before.replace(change['after'], change['before'], 1)
    assert len(before.encode()) == predecessor['predecessor']['bytes']
    assert sha(before.encode()) == predecessor['predecessor']['sha256']
    current_bodies, old_bodies = bodies(text), bodies(before)
    assert len(current_bodies) == 12
    for row in predecessor['requirement_bodies']:
        old = old_bodies[row['id']]
        assert len(old.encode()) == row['bytes'] and sha(old.encode()) == row['sha256']
        assert current_bodies[row['id']].startswith(old)
        if row['id'] not in predecessor['allowed_append_only_requirement_bodies']:
            assert current_bodies[row['id']] == old
    rows = [row for row in text.splitlines() if row.startswith('| TS-')]
    assert len(rows) == 37
    for row, pin in zip(rows, predecessor['old_case_rows']):
        assert row.split('|')[1].strip() == pin['id']
        assert len(row.encode()) == pin['bytes'] and sha(row.encode()) == pin['sha256']
    return {'requirements': 12, 'old_body_prefixes_exact': 12,
            'other_whole_bodies_exact': 10, 'old_case_rows_exact': 37,
            'reverse_reconstructed_predecessor': predecessor['predecessor']}


def catalog_check(catalog, inputs, results, review, historical):
    assert catalog['actual_review']['manifest'] == catalog['sources']['batch-manifest']
    assert review['manifest'] == catalog['sources']['batch-manifest']
    assert review['disposition'] == 'APPROVED_BOUNDED_316_TYPED_SETTER_ARGUMENT_OBSERVATIONS'
    assert not review['blocking_findings'] and not review['nonblocking_findings']
    assert catalog['actual_review']['disposition'] == review['disposition']
    records = catalog['records']
    assert len(records) == catalog['record_count'] == 316
    new = [row for row in records if row['role'] == 'new-finite-converter-case']
    controls = [row for row in records if row['role'] == 'supporting-historical-input-control-not-new-case']
    assert [row['id'] for row in new] == [f'TS-{i:03d}' for i in range(38, 351)]
    assert [row['id'] for row in controls] == [f'TRANSPORT-HEX-CONTROL-{i:03d}' for i in range(1, 4)]
    assert catalog['new_case_IDs'] == len(new) == 313
    assert catalog['support_control_records_not_new_cases'] == len(controls) == 3
    assert catalog['old_case_IDs_including_withdrawn'] == 37
    assert catalog['intended_total_case_IDs_including_withdrawn'] == 350
    assert catalog['intended_total_nonwithdrawn_IDs'] == 349
    assert catalog['observation_re_reviewed_here'] is False
    assert catalog['no_original_or_model_execution'] is True
    assert len(catalog['groups']) == 8
    words, exact_inputs, refs = set(), set(), set()
    for row in records:
        assert row['input_ref']['source'] == 'batch-inputs'
        assert row['observation_ref']['source'] == 'batch-results'
        source = pointer(inputs, row['input_ref']['pointer'])
        observed = pointer(results, row['observation_ref']['pointer'])
        assert row['source_capture_id'] == source['id'] == observed['id']
        value, expectation = row['input'], row['expected']
        assert value['decoded_ASCII_text'] == source['text']
        assert value['exact_bytes_hex'] == source['input_bytes_hex'] == observed['input_bytes_hex']
        assert value['byte_length'] == source['input_length']
        assert value['declared_word_width'] == source['width']
        assert value['recorded_type_id'] == source['type_id'] == observed['type_id']
        assert value['hex_case'] == source['hex_case']
        assert value['sign_bit'] == source['sign']
        assert value['fraction_integer'] == source['fraction_integer']
        assert value['fraction_role'] == source['fraction_role']
        assert value['input_word_hex'] == source['word_hex'] == observed['input_word_hex']
        assert value['layout_label_is_not_FP_trap_state'] is True
        assert expectation['typed_SetValue_argument_bits_hex'] == observed['selected_typed_bits_hex']
        assert expectation['typed_argument_bytes_le'] == observed['selected_typed_bytes_le']
        assert expectation['captured_raw_unsigned_HIT_hex'] == observed['raw_unsigned_HIT']
        assert expectation['selected_SetValue_stub'] == observed['setter_stub']
        assert expectation['observed_owner_bit_oracle_agreement'] is observed['owner_bit_oracle_agreement'] is True
        assert row['requirement'] == ('REQ-TRANSPORT-STATE-005' if source['width'] == 32 else 'REQ-TRANSPORT-STATE-004')
        assert (row['role'] == 'supporting-historical-input-control-not-new-case') == source['historical_exact_kind_text_member']
        group_index = int(row['observation_ref']['pointer'].split('/')[2])
        assert row['raw_stdout_ref']['group'] == results['groups'][group_index]['id']
        assert row['raw_stdout_ref']['pin'] == results['groups'][group_index]['stdout']
        if row in controls:
            assert row['historical_input_ref']['source'] == 'historical-X2-parse'
            previous = pointer(historical, row['historical_input_ref']['pointer'])
            assert (previous['kind'], previous['text'], previous['bytes']) == (source['kind'], source['text'], source['input_bytes_hex'])
        else:
            assert 'historical_input_ref' not in row
        assert row['evidence'] == 'X: approved finite typed-argument observation, not public field admission or setter storage'
        for key in ('public_load_field_admission_save_outcome', 'FP_state', 'ARM_Apple_observation', 'candidate_result', 'candidate_grade'):
            assert row[key] is None
        words.add((source['width'], source['word_hex']))
        exact_inputs.add((source['kind'], source['text']))
        refs.add(row['input_ref']['pointer'])
    assert len(words) == catalog['word_count'] == 158
    assert len(exact_inputs) == len(refs) == 316
    expected_refs = {f'/groups/{i}/conversions/{j}' for i, group in enumerate(inputs['groups'])
                     for j in range(len(group['conversions']))}
    assert refs == expected_refs
    for group, source_group in zip(catalog['groups'], inputs['groups']):
        assert group['id'] == source_group['id']
        selected = [row for row in records if row['raw_stdout_ref']['group'] == group['id']]
        assert len(selected) == group['records'] == len(source_group['conversions'])
        assert group['new_case_IDs'] == [row['id'] for row in selected if row in new]
        assert group['support_control_IDs'] == [row['id'] for row in selected if row in controls]
    return {'records': 316, 'new_case_IDs': 313, 'supporting_controls': 3,
            'width_word_pairs': 158, 'groups': 8, 'joins': 'exact adopted fields only; actual observation review inherited'}


def reject(label, callback):
    try:
        callback()
    except (AssertionError, KeyError, IndexError, ValueError):
        return {'name': label, 'rejected': True}
    raise AssertionError('negative control accepted: ' + label)


def main():
    catalog = load(HERE / 'case-catalog.json')
    delta = load(HERE / 'owner.delta.json')
    predecessor = load(HERE / 'predecessor.json')
    text = (ROOT / delta['current']['path']).read_text()
    documents = {name: pinned(pin) for name, pin in catalog['sources'].items()}
    review = pinned(catalog['actual_review'])
    owner_checks = preservation(text, delta, predecessor)
    joined = catalog_check(catalog, documents['batch-inputs'], documents['batch-results'], review, documents['historical-X2-parse'])
    negatives = []
    mutations = [
        ('omitted finite input', lambda c: c['records'].pop()),
        ('control promoted to new case', lambda c: c['records'][0].update(role='new-finite-converter-case')),
        ('wrong typed width', lambda c: c['records'][1]['input'].update(declared_word_width=64)),
        ('ASCII hex case changed', lambda c: c['records'][1]['input'].update(decoded_ASCII_text='#7f800001')),
        ('canonicalized payload bits', lambda c: c['records'][1]['expected'].update(typed_SetValue_argument_bits_hex='7fc00000')),
        ('raw sign extension erased', lambda c: c['records'][50]['expected'].update(captured_raw_unsigned_HIT_hex='0')),
        ('public opening promoted', lambda c: c['records'][1].update(public_load_field_admission_save_outcome='pass')),
        ('FP state invented', lambda c: c['records'][1].update(FP_state='no exception')),
        ('ARM result invented', lambda c: c['records'][1].update(ARM_Apple_observation='same')),
        ('candidate grade invented', lambda c: c['records'][1].update(candidate_grade='pass')),
        ('group drops a case alias', lambda c: c['groups'][0]['new_case_IDs'].pop()),
        ('review manifest changed', lambda c: c['actual_review']['manifest'].update(sha256='0' * 64)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(catalog)
        mutate(changed)
        negatives.append(reject(name, lambda: catalog_check(changed, documents['batch-inputs'], documents['batch-results'], review, documents['historical-X2-parse'])))
    negatives.append(reject('legacy U changed', lambda: preservation(text.replace('| TS-017 | 009 | B | U |', '| TS-017 | 009 | B | X |'), delta, predecessor)))
    negatives.append(reject('library rounding clause changed', lambda: preservation(text.replace('A-LOG', 'A-NEW', 1), delta, predecessor)))
    negatives.append(reject('new fixture pin fabricated', lambda: pinned({'path': catalog['sources']['batch-manifest']['path'], 'bytes': 0, 'sha256': '0' * 64})))
    for match in re.finditer(r'\]\(([^)]+)\)', text):
        target = match[1].split('#', 1)[0]
        if 'owner-transport-typed-hex-finite-v1' in target or 'batch-transport-standing-leaves-v1' in target or 'transport-standing-leaves-v1-review.json' in target:
            assert (ROOT / 'wiki/specs' / target).resolve().is_file()
    print(json.dumps({'status': 'PASS', 'owner_preservation': owner_checks, 'mapping': joined,
                      'negative_controls': negatives, 'negative_control_count': len(negatives),
                      'scope': 'Data-only owner adoption checks. No original/GDB/collector/model/float-value decoding or fresh observation review.'}, indent=2))


if __name__ == '__main__':
    main()
