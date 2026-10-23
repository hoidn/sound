"""Read-only source/owner audit checks; imports only our pinned pure HTML parser."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def load(path):
    return json.loads(path.read_text())


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def pointer(value, path):
    for key in path.strip('/').split('/') if path else []:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def guards(audit):
    blocks = audit['blocks']
    assert len(blocks) == len(audit['assessments']) == 32, 'source omission'
    assert len(audit['owner_requirements']) == 14 and len(audit['owner_cases']) == 24
    for index, (block, assessment) in enumerate(zip(blocks, audit['assessments'])):
        assert assessment['source_block_pointer'] == '/' + str(index)
        assert assessment['source_block'] == block['id']
        assert assessment['source_text_sha256'] == hashlib.sha256(block['text'].encode()).hexdigest()
        for ref in assessment['requirement_refs'] + assessment['case_refs']:
            row = pointer(audit[ref['catalog']], ref['json_pointer'])
            assert (row['id'] if 'id' in row else row['row']['id']) == ref['id'], 'wrong valid owner association'
    groups = {item['id']: item for item in audit['proposals']}
    assert len(groups) == 10 and {x for a in audit['assessments'] for x in a['proposals']} <= set(groups)
    for record in audit['assessments'] + audit['proposals']:
        assert record['actual_expected'] is None and record['actual_comparison'] is None, 'invented actual oracle'
        assert record['target'] == 'U' and record['executed'] is False and record['complete'] is False
    for record in audit['proposals']:
        assert record['documentary_expected'] is None and record['documentary_comparison'] is None
    assert audit['source']['exact_capture_utc'] is None, 'invented source capture UTC'
    assert audit['complete_topics'] == 0
    assert 'genuinely confirmed groove timing effect' in groups['GSA-G05']['proposed_action'], 'Warp flag is not a productive baseline'
    assert 'independently confirmed positive velocity influence' in groups['GSA-G08']['proposed_action']
    assert 'nonflat pre-existing clip-volume envelope' in groups['GSA-G08']['proposed_action'], 'missing overwrite prerequisite'
    assert 'Quantize100 with Velocity0 in old010 is not this trial' in groups['GSA-G08']['proposed_action']
    assert 'No guaranteed distinct' in groups['GSA-G09']['limits'], 'random guarantee inferred'
    assert 'double-click selected alternative versus Enter' in groups['GSA-G10']['proposed_action']
    assert 'old/new clip and Groove Pool entry identities' in groups['GSA-G10']['proposed_action']
    assert [r['json_pointer'] for r in groups['GSA-G08']['external_context_refs']] == ['/2']
    assert [r['json_pointer'] for r in groups['GSA-G10']['external_context_refs']] == ['/0', '/1']
    for record in audit['assessments'] + audit['proposals']:
        for ref in record.get('external_context_refs', []):
            pointer(audit[ref['catalog']], ref['json_pointer'])


def fixtures(audit):
    mutations = [
        ('source omission', lambda a: a['blocks'].pop()),
        ('wrong valid owner association', lambda a: a['assessments'][2]['case_refs'][0].update(json_pointer='/13')),
        ('invented actual oracle', lambda a: a['proposals'][0].update(actual_expected='pass')),
        ('invented capture UTC', lambda a: a['source'].update(exact_capture_utc=a['authored_utc'])),
        ('missing productive Warp baseline', lambda a: a['proposals'][4].update(proposed_action='Warp enabled; then off')),
        ('missing prior envelope', lambda a: a['proposals'][7].update(proposed_action=a['proposals'][7]['proposed_action'].replace('nonflat pre-existing clip-volume envelope', 'unknown initial envelope'))),
        ('random separation guarantee', lambda a: a['proposals'][8].update(limits='Require every realization to differ')),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(audit)
        mutate(changed)
        try:
            guards(changed)
        except AssertionError:
            continue
        raise AssertionError('unsafe mutation accepted: ' + name)
    return [name for name, _ in mutations]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    inputs = load(HERE / 'inputs.json')
    for pin in inputs:
        assert identity(ROOT / pin['path']) == {key: pin[key] for key in ['bytes', 'sha256']}, pin['path']
    audit = load(HERE / 'audit.json')
    guards(audit)
    module_path = ROOT / next(p['path'] for p in inputs if p['path'].endswith('/clip-view-source-audit/source_parser.py'))
    spec = importlib.util.spec_from_file_location('groove_audit_our_pure_parser', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    html = (ROOT / audit['source']['file']['path']).read_text()
    blocks, resources = module.extract(html, 'GRV')
    assert blocks == audit['blocks']
    assert len(resources) == len(audit['resources']) == 17
    for raw, annotated in zip(resources, audit['resources']):
        assert all(annotated[key] == value for key, value in raw.items())
        assert annotated['pixels_or_destination_inspected'] is False and annotated['complete'] is False
    source_records = load(ROOT / next(p['path'] for p in inputs if p['path'].endswith('/mpe-tuning-grooves/sources.json')))
    original = next(r for r in source_records if r['id'] == audit['source']['id'])
    assert all(audit['source'][key] == value for key, value in original.items())
    assert audit['source']['file']['sha256'] == original['sha256']
    owner = (ROOT / audit['owner_provider']['path']).read_text().splitlines()
    for row in audit['owner_requirements']:
        assert owner[row['line'] - 1] == row['row']
        cells = [x.strip() for x in row['row'].strip('|').split('|')]
        assert cells == [row[k] for k in ['id', 'preconditions', 'contract', 'evidence']]
    for case in audit['owner_cases']:
        assert pointer(load(ROOT / case['catalog']), case['json_pointer']) == case['row']
        assert case['row']['target_build_grade'] == 'U' and case['row']['execution'] == 'unexecuted'
    for row in audit['external_contexts']:
        if row['kind'] == 'JSON':
            assert pointer(load(ROOT / row['catalog']), row['json_pointer']) == row['row']
        else:
            text = (HERE / row['snapshot']).read_text()
            assert text[row['raw_start']:row['raw_end']] == row['quote']
            assert identity(HERE / row['snapshot']) == {key: row['canonical_asof'][key] for key in ['bytes', 'sha256']}
    clip_html_path = next(p['path'] for p in inputs if '/clip-view/' in p['path'] and p['path'].endswith('.html'))
    clip_blocks, _ = module.extract((ROOT / clip_html_path).read_text(), 'CV')
    for selected in audit['external_contexts'][:3]:
        assert selected['row'] == next(b for b in clip_blocks if b['id'] == selected['row']['id'])
    tiny = '<div id="chapter_content"><h1 id="x" data-number="14">Grooves</h1><p>1.5 beats</p><ul><li>Base</li></ul><table><tr><td>a</td><td>0.5</td></tr></table><img alt=""><figcaption>Literal</figcaption></div>'
    test_blocks, test_resources = module.extract(tiny, 'FIX')
    assert [b['text'] for b in test_blocks] == ['Grooves', '1.5 beats', 'Base', 'a | 0.5']
    assert test_blocks[2]['heading_context'][-1]['anchor'] == 'x'
    assert test_resources[0]['attributes']['alt'] == '' and test_resources[1]['text'] == 'Literal'
    rejected = fixtures(audit)
    sealed = HERE / 'manifest.json'
    if sealed.exists():
        manifest = load(sealed)
        assert {p.name for p in HERE.iterdir() if p.is_file() and p != sealed} == {p['file'] for p in manifest['payloads']}
        for pin in manifest['payloads']:
            assert identity(HERE / pin['file']) == {key: pin[key] for key in ['bytes', 'sha256']}
        assert manifest['immutable_inputs'] == inputs
    for path in HERE.iterdir():
        if path.is_file() and path.name != 'racks-asof.md':
            raw = path.read_bytes()
            assert raw.endswith(b'\n') and b'\r\n' not in raw
            assert not any(line.rstrip(b' \t') != line for line in raw.splitlines()), path
    print(json.dumps({'status': 'pass', 'mode': 'read-only', 'sealed': sealed.exists(), 'blocks': 32, 'resources': 17, 'requirements': 14, 'cases': 24, 'audit_only_proposals': 10, 'immutable_inputs': len(inputs), 'negative_fixtures': rejected, 'parser_fixture': 'pass', 'actual_nonnull': 0, 'executed': 0, 'complete_topics': 0}))


if __name__ == '__main__':
    main()
