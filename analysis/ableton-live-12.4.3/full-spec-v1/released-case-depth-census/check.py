"""D-02 read-only expectation census; does not run release comparators or candidates."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RELEASES = '''als-container-v1 automation-envelopes-v2 browser-index-v1
bundled-device-parameters-v1 clip-launch-v2 device-analog-v1 device-collision-v1
device-corpus-v1 device-electric-v2 device-tension-v1 live-set-structure-v1
midi-config-v4 midi-note-storage-v2 mix-graph-v1 mixer-values-v2 playback-core-v1
plugin-discovery-v1 transport-state-v3 warp-markers-v2'''.split()


def digest(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def form(case):
    fields = {k: v for k, v in case.items()
              if k in ['expected', 'comparator', 'metric']}
    assert not re.search(r'unknown|ungraded|not[- ]graded|unresolved', json.dumps(fields), re.I)
    if 'expected' in case:
        assert case['expected'] is not None and case['expected'] != {}
        assert isinstance(case.get('comparator'), str) and case['comparator']
        return 'explicit-expected-and-comparator'
    if 'evaluations' in case:
        assert case['evaluations']
        for e in case['evaluations']:
            assert not re.search(r'unknown|ungraded|not[- ]graded|unresolved',
                                 json.dumps({k: v for k, v in e.items()
                                             if k in ['expected', 'metric']}), re.I)
            if 'expected' in e:
                assert e['expected'] is not None and case.get('comparator')
            else:
                assert e.get('reference') and e.get('metric')
        return 'evaluation-expectations-or-reference-metrics'
    assert case.get('reference') and case.get('metric')
    return 'reference-and-metric'


def build():
    families, omissions, pins = [], [], []
    for name in RELEASES:
        folder = ROOT / 'handoff' / name
        manifest = json.loads((folder / 'manifest.json').read_text())
        files = {x['path']: x for x in manifest['files']}
        pins.append({'path': str((folder / 'manifest.json').relative_to(ROOT)),
                     **digest(folder / 'manifest.json')})
        cases = json.loads((folder / 'cases.json').read_text())['cases']
        assert len({c['id'] for c in cases}) == len(cases)
        forms = Counter()
        for i, c in enumerate(cases):
            forms[form(c)] += 1
            # Null values inside a concrete state are not missing case oracles.
            if name == 'als-container-v1' and c['expected'].get('refusal_class') == 'unspecified':
                assert c['expected']['outcome'] == 'refused'
                assert c['comparator'] == 'outcome exact; refusal_class not compared'
                omissions.append({'release': name, 'id': c['id'],
                                  'case_pointer': f'/cases/{i}',
                                  'scope': 'Refusal class unspecified; refusal outcome graded.'})
            for e in ([c] if 'reference' in c else c.get('evaluations', [])):
                if 'reference' in e:
                    ref = e['reference']
                    assert ref in files
                    assert digest(folder / ref) == {k: files[ref][k] for k in ['bytes', 'sha256']}
        families.append({'release': name, 'case_rows': len(cases),
                         'expectation_forms': dict(forms),
                         'candidate_execution': 'not-assessed'})
        for filename in ['cases.json', 'spec.md']:
            p = folder / filename
            assert digest(p) == {k: files[filename][k] for k in ['bytes', 'sha256']}
            pins.append({'path': str(p.relative_to(ROOT)), **digest(p)})
    return {'releases': RELEASES, 'release_cases': sum(f['case_rows'] for f in families),
            'families': families, 'bounded_omissions': omissions,
            'immutable_release_pins': pins, 'missing_top_level_expectations': 0,
            'limits': 'Schema census only; no new X/S grade, semantic completeness, comparison, or candidate pass.'}


if __name__ == '__main__':
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check']
    for bad in [{'expected': None}, {'expected': {}, 'comparator': 'exact'},
                {'expected': {'outcome': 'opens'}}, {'evaluations': []},
                {'evaluations': [{'reference': 'a'}]}, {},
                {'expected': {'outcome': 'unknown'}, 'comparator': 'exact'},
                {'evaluations': [{'expected': 'ungraded'}], 'comparator': 'exact'}]:
        try:
            form(bad)
        except AssertionError:
            pass
        else:
            raise AssertionError('Missing expectation accepted')
    result = build()
    assert result == json.loads((HERE / 'census.json').read_text())
    assert len(RELEASES) == 19 and result['release_cases'] == 1070
    assert len(result['bounded_omissions']) == 5
    triage = json.loads((HERE / 'triage.json').read_text())
    for source in triage['sources'] + [triage['iq_snapshot']]:
        assert digest(HERE / source['provider']) == {k: source[k] for k in ['bytes', 'sha256']}
    for row in triage['draft_only_flagged_rows']:
        assert (HERE / row['provider']).read_text().splitlines()[row['markdown_line'] - 1] == row['raw_markdown']
    assert len(triage['draft_only_flagged_rows']) == 14
    seal = HERE / 'manifest.json'
    if seal.exists():
        m = json.loads(seal.read_text())
        assert {p.name for p in HERE.iterdir()} == set(m['files']) | {'manifest.json'}
        for name, pin in m['files'].items():
            assert digest(HERE / name) == pin
    print(json.dumps({'status': 'pass', 'releases': 19, 'case_rows': 1070,
                      'missing_top_level_expectations': 0, 'bounded_refusal_class_omissions': 5,
                      'missing_expectation_fixtures_rejected': 8, 'writes': False,
                      'runtime_or_candidate_execution': False}, indent=2))
