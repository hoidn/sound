#!/usr/bin/env python3
"""Read-only three-case Interval successor checks, never the historical writer."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import ast
import hashlib
import json
import re
import runpy
import subprocess
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
B = P.parent


def load(p):
    return json.loads(p.read_text())


def identity(p):
    data = p.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def pointer(value, path):
    for key in path.lstrip('/').split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def check_cases(current, old):
    assert set(current) == set(old) | {'actual_result_status'}
    assert current['format_revision'] == 2
    assert all(current[k] == old[k] for k in ['provenance', 'units'])
    cases = current['cases']
    assert len(cases) == len({c['id'] for c in cases}) == 60
    assert cases[:57] == old['cases']
    assert [c['id'] for c in cases[57:]] == ['MED-058', 'MED-059', 'MED-060']
    assert Counter(c['documented_domain_grade'] for c in cases) == {'D12': 46, 'U': 14}
    assert all(c['target_12_4_3_grade'] == 'U' and c['execution'] == 'not-run' for c in cases)
    status = current['actual_result_status']
    assert status['actual_expected'] is status['actual_comparison'] is None
    assert status['target_grade'] == 'U' and status['executed'] is False
    for row in cases[57:]:
        assert row['requirement'] == 'REQ-MIDI-EDIT-011'
        assert row['actual_expected'] is row['actual_comparison'] is None
        assert row['documented_domain_grade'] == 'D12' and row['expected'] and row['comparator']
        assert 'Scale Mode explicitly Off' in row['setup_action']
        assert 'E11' in row['evidence']
    assert 'WITHOUT invoking Add Interval' in cases[57]['setup_action']
    assert 'genuinely productive Add Interval button baseline' in cases[58]['setup_action']
    assert 'separate exact original owned copy' in cases[58]['setup_action']
    assert 'explicitly deselect all notes' in cases[58]['setup_action']
    assert 'DO NOT invoke Add Interval' in cases[58]['setup_action']
    assert 'never a passing no-addition observation' in cases[58]['setup_action']
    assert 'then actually invoke Add Interval' in cases[59]['setup_action']


def check_context(context, query, old):
    row = pointer(query, context['source_paragraph_pointer'])
    assert row['kind'] == 'p' and row['heading_context'][-1]['anchor'] == 'intervals'
    assert 'If there is an existing note selection' in row['text']
    assert 'When no notes are selected, the slider merely sets the interval size' in row['text']
    assert 'with no note selection' in row['text'] and 'all of the existing notes in the clip' in row['text']
    assert context['source_paragraph_pointer'] == '/selected_MIDI_records/2'
    assert pointer(old, context['existing_case_pointer']) == context['existing_case_read']
    assert context['existing_case_read']['id'] == 'MED-011'
    assert 'Fit to Scale' in context['existing_case_read']['setup_action']


def run():
    assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'], ['--preflight'])
    preflight = sys.argv[1:] == ['--preflight']
    seal = P / 'manifest-author-r2.json'
    assert not preflight or not seal.exists(), 'Refuse preflight after seal'
    before = {str(p.relative_to(P)): identity(p) for p in P.iterdir() if p.is_file()}
    pins = load(P / 'inputs-r2.json')
    assert len(pins) == len({p['path'] for p in pins})
    assert not any(p['path'].startswith('wiki/') for p in pins)
    external = {ROOT / p['path']: {k: p[k] for k in ['bytes', 'sha256']} for p in pins}
    assert all(identity(p) == item for p, item in external.items())
    prior = load(P / 'prior-files-r2.json')
    assert len(prior) == 11
    assert all(identity(P / n) == item for n, item in prior.items())
    original = load(P / 'manifest.json')
    snapshots = {'wiki/specs/midi-editing-tools.md': P / 'spec-before-r2.md',
                 'wiki/research/midi-editing-tools.md': P / 'research-before-r2.md'}
    for item in original['files']:
        # Verify immutable former canonical bytes; no old checker is invoked.
        path = snapshots.get(item['path'], ROOT / item['path'])
        assert identity(path) == {k: item[k] for k in ['bytes', 'sha256']}
    for item in original['external_dependencies']:
        assert identity(ROOT / item['path'])['sha256'] == item['sha256']
    old = load(P / 'acceptance-cases.json')
    current = load(P / 'acceptance-cases-r2.json')
    check_cases(current, old)
    context = load(P / 'source-context-r2.json')
    query_path = ROOT / context['query']['path']
    assert identity(query_path) == {k: context['query'][k] for k in ['bytes', 'sha256']}
    query = load(query_path)
    assert all(identity(ROOT / x['path']) == {k: x[k] for k in ['bytes', 'sha256']} for x in query['immutable_inputs'])
    check_context(context, query, old)
    parser = runpy.run_path(str(B / 'clip-view-source-audit/source_parser.py'))['extract']
    raw = (P / 'manual-12-editing-midi-2026-10-19.html').read_text()
    blocks, _ = parser(raw, 'MIDIQ')
    selected = [b for b in blocks if any(h['anchor'] in ['intervals', 'humanize'] for h in b['heading_context'])]
    assert selected == query['selected_MIDI_records'] and len(selected) == 5
    for row in selected:
        assert raw[row['raw_start']:row['raw_end']] == row['raw_html']
        assert raw.count('\n', 0, row['raw_start']) + 1 == row['html_line']
    clip = load(B / 'clip-view-source-audit/source-blocks.json')
    assert query['selected_Clip_records'] == [b for b in clip if b['id'] in ['CV:B122', 'CV:B126']]
    spec = ROOT / 'wiki/specs/midi-editing-tools.md'
    research = ROOT / 'wiki/research/midi-editing-tools.md'
    spec_before = (P / 'spec-before-r2.md').read_text()
    requirement_rows = lambda text: [line for line in text.splitlines() if line.startswith('| REQ-MIDI-EDIT-')]
    assert len(requirement_rows(spec_before)) == 43
    assert requirement_rows(spec.read_text()) == requirement_rows(spec_before)
    assert context['existing_requirement_row'] in requirement_rows(spec_before)
    for canonical, name in [(spec, 'spec-r2.md'), (research, 'research-r2.md')]:
        assert canonical.read_bytes() == (P / name).read_bytes()
        assert 'revision: 2\n' in canonical.read_text() and 'AS-OF AUTHOR FREEZE' in canonical.read_text()
    delta = load(P / 'delta-r2.json')
    assert delta['old_manifest'] == identity(P / 'manifest.json')
    assert delta['old_records_verbatim'] is True and delta['old_record_count'] == 57
    assert delta['old_requirement_rows_verbatim'] == 43 and delta['new_requirements'] == 0
    assert delta['changed_old_case_fields'] == []
    assert delta['old_top_level_fields'] == {k: v for k, v in old.items() if k != 'cases'}
    assert delta['new_case_ids'] == [c['id'] for c in current['cases'][57:]]
    fixture = load(P / 'fixtures-r2.json')
    assert 'genuinely productive Add Interval button baseline' in fixture['no_selection_negative']
    assert fixture['actual_expected'] is fixture['actual_comparison'] is None
    assert fixture['target_grade'] == 'U' and fixture['executed'] is False
    impact = load(P / 'consumer-impact-r2.json')
    assert impact['consumers_mutated_or_replayed'] is False
    for item in impact['records']:
        if item['classification'].startswith('active author as-of'):
            continue  # As-of metadata is not a mutable consumer input pin.
        assert identity(ROOT / item['consumer']) == item['identity_as_of']
        assert pointer(load(ROOT / item['consumer']), item['pointer']) == item['literal_sha256']
    for name in ['changed-old-case', 'wrong-source', 'weak-negative-baseline', 'actual-oracle', 'wrong-old-case-pointer']:
        cc, ctx = deepcopy(current), deepcopy(context)
        if name == 'changed-old-case':
            cc['cases'][10]['expected'] = 'a fabricated older tool result'
        elif name == 'wrong-source':
            ctx['source_paragraph_pointer'] = '/selected_MIDI_records/4'
        elif name == 'weak-negative-baseline':
            cc['cases'][58]['setup_action'] = cc['cases'][58]['setup_action'].replace('genuinely productive Add Interval button baseline', 'offered button')
        elif name == 'actual-oracle':
            cc['actual_result_status']['actual_comparison'] = 'fabricated target pass'
        else:
            ctx['existing_case_pointer'] = '/cases/11'
        try:
            check_cases(cc, old)
            check_context(ctx, query, old)
        except (AssertionError, KeyError, IndexError):
            continue
        raise AssertionError('mutation accepted: ' + name)
    tree = ast.parse((ROOT / 'tools/spec_browser.py').read_text())
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name in {'anchor', 'frontmatter', 'cells', 'spec_rows'}]
    assert len(functions) == 4
    ns = {'re': re}
    exec(compile(ast.Module(body=functions, type_ignores=[]), 'pure-browser-functions', 'exec'), ns)
    rows = ns['spec_rows'](spec, spec.read_text())
    expected_ids = {line.split('|')[1].strip() for line in requirement_rows(spec_before)}
    assert len(rows) == 43 and {r['id'] for r in rows} == expected_ids
    links = 0
    for page in [spec, research, P / 'README-r2.md']:
        for target in re.findall(r'\]\(([^)\s]+)\)', page.read_text()):
            if re.match(r'[A-Za-z]+:', target):
                continue
            name, _, fragment = target.partition('#')
            dest = (page.parent / name).resolve() if name else page
            assert dest.is_file(), (page, target)
            if fragment and dest.suffix == '.md':
                assert fragment in {ns['anchor'](h) for h in re.findall(r'^#+\s+(.+)$', dest.read_text(), re.M)}
            links += 1
    for path in [spec, research] + [P / name for name in before if name not in prior]:
        if path.suffix == '.json':
            load(path)
        result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True)
        assert result.returncode in (0, 1) and not result.stdout and not result.stderr, path
    if not preflight:
        manifest = load(seal)
        assert set(before) == set(manifest['files']) | {'manifest-author-r2.json'}
        assert all(identity(P / name) == item for name, item in manifest['files'].items())
    assert before == {str(p.relative_to(P)): identity(p) for p in P.iterdir() if p.is_file()}
    assert all(identity(p) == item for p, item in external.items())
    print(json.dumps({'status': 'pass', 'sealed': not preflight, 'requirements': 43,
        'old_requirement_rows_verbatim': 43, 'cases': 60, 'old_records_verbatim': 57,
        'documentary_D12': 46, 'documentary_U': 14, 'actual_status': 'null/U/unexecuted',
        'old_files_preserved': 11, 'input_pins': len(pins), 'selected_source_records': 7,
        'browser_exact_ids': 43, 'links': links, 'rejection_fixtures': 5,
        'historical_consumers_replayed': False, 'complete_topics': 0, 'runtime': False, 'writes': False}))


if __name__ == '__main__':
    run()
