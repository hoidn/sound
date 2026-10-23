#!/usr/bin/env python3
"""Finite approved-result projection and reversible owner preservation only; no original/model/native execution."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BATCH = HERE.parent / 'batch-playback-standing-leaves-v1'
OWNER = ROOT / 'wiki/specs/playback-core.md'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def reqs(text):
    return {m.group(1): m.group(0).encode() for m in re.finditer(r'^### (REQ-PLAYBACK-CORE-\d{3})[^\n]*\n(.*?)(?=^### REQ-|^## |\Z)', text, re.M | re.S)}

def caserows(text):
    return {m.group(1): m.group(0).encode() for m in re.finditer(r'^\| (PBC-\d{3}) \|[^\n]*\n', text, re.M)}

def mapping(cases, agreements, observations):
    selected = [r for r in observations['rows'] if r['historical_expected_output_binary64_hex'] is None]
    known = [r for r in observations['rows'] if r['historical_expected_output_binary64_hex'] is not None]
    assert len(cases) == len(selected) == 109 and len(agreements) == len(known) == 8
    assert [r['id'] for r in cases] == [f'PBC-{i:03d}' for i in range(97, 206)]
    assert len({r['source']['batch_id'] for r in cases}) == 109
    for case, row in zip(cases, selected):
        assert case['source']['batch_id'] == row['id']
        index = int(case['source']['pointer'].split('/')[-1])
        assert observations['rows'][index] == row
        assert case['input']['binary64_hex'] == row['input']['binary64_hex']
        assert case['input']['bytes_le_hex'] == row['input']['bytes_le_hex']
        assert case['input']['classification'] == row['input']['classification']
        assert case['expected'] == {'binary64_hex': row['actual_return']['binary64_hex'], 'classification': row['actual_return']['classification']}
        assert case['requirements'] == ['REQ-PLAYBACK-CORE-017'] and case['label'] == 'X'
        assert case['prior_expectation'] is None
        assert case['application_grade'] == 'unknown' and case['candidate_execution'] == 'not-run'
        assert case['source']['return_projection'] == 'low64 saved XMM0'
    for a, row in zip(agreements, known):
        assert a['batch_id'] == row['id'] and a['new_case'] is None
        assert a['input_binary64_hex'] == row['input']['binary64_hex']
        assert a['known_expected_binary64_hex'] == a['actual_binary64_hex'] == row['historical_expected_output_binary64_hex']
        assert a['agreement'] is True
    finite_overflow = [r for r in cases if r['input']['classification'] not in ['positive-infinity', 'negative-infinity', 'positive-qNaN', 'negative-qNaN'] and r['expected']['classification'].endswith('infinity')]
    assert len(finite_overflow) == 6
    qnans = [r for r in cases if r['input']['classification'].endswith('qNaN')]
    assert {r['input']['binary64_hex'] for r in qnans} == {'7ff8000000000000', 'fff8000000000000'}
    return True

def preservation(before, after, identities):
    assert len(before.encode()) == identities['owner']['bytes'] and sha(before.encode()) == identities['owner']['sha256']
    old, new = reqs(before), reqs(after)
    assert len(old) == len(new) == 23
    for r in identities['requirement_spans']:
        assert len(old[r['id']]) == r['bytes'] and sha(old[r['id']]) == r['sha256']
        if r['id'] != 'REQ-PLAYBACK-CORE-017':
            assert new[r['id']] == old[r['id']], r['id']
    old_rows, new_rows = caserows(before), caserows(after)
    assert len(old_rows) == 68 and old_rows == new_rows
    for row in identities['case_rows']:
        assert len(old_rows[row['id']]) == row['bytes'] and sha(old_rows[row['id']]) == row['sha256']
    return True

def main():
    before = json.loads((HERE / 'before-identities.json').read_text())
    cases = json.loads((HERE / 'cases-added.json').read_text())['cases']
    agreements = json.loads((HERE / 'known-oracle-agreements.json').read_text())['agreements']
    observations = json.loads((BATCH / 'observations.json').read_text())
    mapping(cases, agreements, observations)
    negatives = []
    for name, mutate in [
        ('drop one newcase', lambda a, b: a.pop()),
        ('duplicate ID', lambda a, b: a[1].update(id=a[0]['id'])),
        ('return bit changed', lambda a, b: a[0]['expected'].update(binary64_hex='0' * 16)),
        ('newprior NULL repaired', lambda a, b: a[0].update(prior_expectation='model-true')),
        ('publicgrade promotion', lambda a, b: a[0].update(application_grade='pass')),
        ('wrong output register', lambda a, b: a[0]['source'].update(return_projection='rax')),
        ('knowncontrol made newcase', lambda a, b: b[0].update(new_case='PBC-097')),
        ('knownoracle mismatch hidden', lambda a, b: b[0].update(actual_binary64_hex='f' * 16))]:
        a, b = copy.deepcopy((cases, agreements))
        mutate(a, b)
        try:
            mapping(a, b, observations)
        except AssertionError:
            negatives.append(name)
        else:
            raise AssertionError('False promotion accepted: ' + name)
    if sys.argv[1:] == ['--mapping-only']:
        raw = OWNER.read_bytes()
        assert len(raw) == before['owner']['bytes'] and sha(raw) == before['owner']['sha256']
        mode = 'mapping-only, canonical untouched'
    else:
        assert sys.argv[1:] == ['--check']
        delta = json.loads((HERE / 'owner-delta.json').read_text())
        after = OWNER.read_text()
        previous = after
        for op in reversed(delta['operations']):
            assert previous.count(op['new']) == 1
            previous = previous.replace(op['new'], op['old'], 1)
        preservation(previous, after, before)
        assert 'revision: 3\n' in after and 'PBC-097–PBC-205' in after
        assert 'cause remains unknown' in after and 'no portable ARM/Apple' in after
        assert 'no sNaN' in after and 'not an input-register' in after
        pins = json.loads((HERE / 'pins.json').read_text())['pins']
        for p in pins:
            raw = (ROOT / p['path']).read_bytes()
            assert len(raw) == p['bytes'] and sha(raw) == p['sha256']
        for name, altered in [('otherREQchanged', after.replace('The scheduler measures song time', 'The scheduler loses song time', 1)), ('oldrowchanged', after.replace('| PBC-001 | 001, 002, 004 |', '| PBC-001 | 017 |', 1))]:
            try:
                preservation(previous, altered, before)
            except AssertionError:
                negatives.append(name)
            else:
                raise AssertionError('Preservation control accepted: ' + name)
        mode = 'owner3 exact reverse/preservation and selected pins'
    print(json.dumps({'status': 'PASS', 'mode': mode, 'all_observations_represented': 117, 'newfinite_cases': 109, 'knownoracle_agreements_not_newcases': 8, 'negative_controls': negatives, 'original_calls': 0, 'observation_review_runs': 0, 'models_or_comparators': 0}))

if __name__ == '__main__':
    main()
