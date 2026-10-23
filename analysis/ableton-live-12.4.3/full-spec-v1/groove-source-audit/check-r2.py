"""Read-only focused association correction, preserving the reviewed R1 audit."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import runpy
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def load(path):
    return json.loads(path.read_text())


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def current_guard(old, current):
    expected = copy.deepcopy(old)
    expected['assessments'][27]['requirement_refs'] = []
    expected['assessments'][27]['case_refs'] = []
    assert current == expected, 'unexpected current audit change'
    row = current['assessments'][27]
    assert row['source_block'] == 'GRV:B028'
    assert row['requirement_refs'] == row['case_refs'] == [], 'wrong primary extraction association'
    assert [r['json_pointer'] for r in row['external_context_refs']] == ['/3', '/4']
    assert current['external_contexts'][3]['row']['id'] == 'RCK-046'
    assert '### REQ-DEVICE-RACKS-022' in current['external_contexts'][4]['quote']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    assert sys.dont_write_bytecode
    correction = load(HERE / 'correction-r2.json')
    assert identity(HERE / 'manifest.json') == correction['parent_manifest']
    parent = load(HERE / 'manifest.json')
    for pin in parent['payloads']:
        assert identity(HERE / pin['file']) == {k: pin[k] for k in ['bytes', 'sha256']}
    for pin in parent['immutable_inputs']:
        assert identity(ROOT / pin['path']) == {k: pin[k] for k in ['bytes', 'sha256']}
    review_pin = correction['review']
    assert identity(ROOT / review_pin['path']) == {k: review_pin[k] for k in ['bytes', 'sha256']}
    review = load(ROOT / review_pin['path'])
    assert 'GSA-REVIEW-001' in json.dumps(review)
    old = load(HERE / 'audit.json')
    current = copy.deepcopy(old)
    assert [p['pointer'] for p in correction['patches']] == ['/assessments/27/requirement_refs', '/assessments/27/case_refs']
    for patch in correction['patches']:
        field = patch['pointer'].rsplit('/', 1)[1]
        assert current['assessments'][27][field] == patch['before'] and patch['after'] == []
        current['assessments'][27][field] = patch['after']
    current_guard(old, current)
    # Only inspected pure guard definitions from our pinned R1 module; no main/replay.
    runpy.run_path(str(HERE / 'check.py'))['guards'](current)
    for change in ['restore-primary', 'remove-external', 'change-source']:
        bad = copy.deepcopy(current)
        if change == 'restore-primary':
            bad['assessments'][27]['case_refs'] = old['assessments'][27]['case_refs']
        elif change == 'remove-external':
            bad['assessments'][27]['external_context_refs'] = []
        else:
            bad['blocks'][27]['text'] = 'changed source'
        try:
            current_guard(old, bad)
        except AssertionError:
            continue
        raise AssertionError('unsafe correction accepted: ' + change)
    seal = HERE / 'manifest-r2.json'
    if seal.exists():
        manifest = load(seal)
        assert {p.name for p in HERE.iterdir() if p.is_file() and p != seal} == {r['file'] for r in manifest['payloads']}
        for pin in manifest['payloads']:
            assert identity(HERE / pin['file']) == {k: pin[k] for k in ['bytes', 'sha256']}
    for name in ['README-r2.md', 'correction-r2.json', 'check-r2.py']:
        raw = (HERE / name).read_bytes()
        assert raw.endswith(b'\n') and not any(line.rstrip(b' \t') != line for line in raw.splitlines())
    print(json.dumps({'status': 'pass', 'sealed': seal.exists(), 'mode': 'read-only', 'preserved_R1_files': 6, 'changed_current_view_fields': 2, 'external_references_unchanged': True, 'focused_rejections': 3, 'new_normative_IDs': 0, 'actual_nonnull': 0, 'executed': 0, 'complete_topics': 0}))


if __name__ == '__main__':
    main()
