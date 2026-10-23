"""Read-only bounded analyst data checks; use existing CPython3.11 with -I -B."""
from pathlib import Path
from collections import Counter
import hashlib
import importlib.util
import json
import re
import runpy
import subprocess
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
assert sys.version_info[:2] == (3, 11) and importlib.util.MAGIC_NUMBER.hex() == 'a70d0d0a'
assert sys.dont_write_bytecode, 'Use -B; no cache writes'


def load(path):
    return json.loads(path.read_text())


def pin(path, record):
    data = path.read_bytes()
    assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'], path
    return data


def slug(text):
    text = re.sub(r'<[^>]*>|[`*]', '', text)
    return re.sub(r'[^\w\- ]', '', text.strip().lower()).replace(' ', '-')


before = {str(p.relative_to(P)): hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
assert not any('__pycache__' in p for p in before)
initial = load(P / 'initial-capture-pins.json')
assert len(initial) == 11
for name, record in initial.items():
    pin(P / name, record)
owners = load(P / 'input-owner-pins.json')
assert len(owners) == 11
for record in owners:
    pin(ROOT / record['path'], record)
I = P.parent / 'inventory'
inventory = load(I / 'manifest.json')
assert inventory['target'] == 'Ableton Live 12 Suite 12.4.3'
pin(I / 'controller-profiles.json', inventory['files']['controller-profiles.json'])
baseline = load(I / 'controller-profiles.json')
assert len(baseline) == 149
selected = [r for r in baseline if r['name'].startswith('APC') and r['kind'] == 'named-controller-module; identity not behavior']
assert [r['name'] for r in selected] == ['APC20', 'APC40', 'APC40_MkII', 'APC64', 'APC_Key_25', 'APC_Key_25_mk2', 'APC_mini', 'APC_mini_mk2']
assert next(r for r in baseline if r['name'] == '_APC')['kind'] == 'support-or-internal'
assert selected == load(P / 'selected-rows.json') and all(r['complete'] is False and r['specification'] == 'unmapped' for r in baseline)
environment = load(P / 'capture-environment.json')
assert environment['magic'] == 'a70d0d0a' and environment['version'] == sys.version
assert environment['target_source_execution'] is False
tool = runpy.run_path(str(P / 'decode.py'))
sources, declarations, ledger = load(P / 'sources.json'), load(P / 'declarations.json'), load(P / 'capability-ledger.json')
assert len(sources) == len(declarations) == len(ledger) == 8
headers = load(P / 'header-fields.json')
assert len(headers) == 8 and load(P / 'decode-failures.json') == []
first_raw = None
for source, original, declared, row, header in zip(sources, selected, declarations, ledger, headers):
    assert source['id'] == original['id'] == declared['id'] == row['id']
    assert source['name'] == original['name'] == declared['name'] == row['name']
    assert source['sha256'] == original['source']['sha256'] and source['bytes'] == original['source']['bytes']
    raw = pin(P / source['file'], source)
    assert Path(source['original_path']) == Path(inventory['source_root']) / original['source']['path']
    assert raw == Path(source['original_path']).read_bytes(), source['original_path']
    assert source['magic'] == raw[:4].hex() == 'a70d0d0a' and source['flags'] == int.from_bytes(raw[4:8], 'little') == 0
    assert source['header_hex'] == raw[:16].hex() and source['get_capabilities_count'] == 1
    assert header['source_id'] == source['id'] and header['header_bytes'] == 16 and header['magic'] == source['magic'] and header['flags'] == 0
    assert header['timestamp_field'] == int.from_bytes(raw[8:12], 'little') and header['source_size_field'] == int.from_bytes(raw[12:16], 'little')
    decoded = tool['decode'](raw)
    assert source['module_name'] == decoded['module']['name'] and source['co_filename'] == decoded['module']['filename']
    assert dict(id=source['id'], name=source['name'], source_sha256=source['sha256'], **decoded) == declared
    assert tool['ledger_row'](source['id'], source['name'], source['sha256'], decoded) == row
    assert row['runtime_return'] is None and row['complete'] is False
    assert row['identity_literal_inputs']['vendor_id'] == 2536
    assert all(n['kind'] == 'opaque-call' for n in decoded['get_capabilities']['calls'])
    first_raw = first_raw or raw
assert [r['identity_literal_inputs']['product_ids'] for r in ledger] == [[123], [115], [41], [83], [39], [78], [40], [79]]
assert [len(r['ports']) for r in ledger] == [2, 2, 2, 3, 2, 4, 2, 4]
assert [r['name'] for r in ledger if r['autoload_literal'] is True] == ['APC64', 'APC_Key_25_mk2', 'APC_mini_mk2']
assert all(r['autoload_literal'] is None for r in ledger if r['name'] not in ('APC64', 'APC_Key_25_mk2', 'APC_mini_mk2'))
assert (P / 'listings.txt').read_text() == ''.join('\n## ' + r['name'] + ' ' + c + '\n' + ''.join(f"{i['offset']:4d} {i['op']} {i['text']}".rstrip() + '\n' for i in rows)
    for r in declarations for c, rows in [('module imports/top level (not executed)', r['module']['instructions']), ('get_capabilities (not called)', r['get_capabilities']['instructions'])])
selfchecks = tool['selfchecks'](first_raw)
assert selfchecks == dict(invalid_header_payload_variants_rejected=7, unsupported_branch_rejected=True, unknown_helper_call_rejected=True, compiled_analyst_fixture_executed=False, original_functions_called=False)
denominator = load(P / 'denominator.json')
assert denominator['baseline_rows'] == 149 and denominator['selected_count'] == 8 and denominator['remaining_count'] == 141
assert denominator['selected_rows'] == selected and denominator['excluded_support_name'] == '_APC' and denominator['all_selected_complete'] is False
requirements, cases = load(P / 'requirements.json'), load(P / 'cases.json')
reqmap = {r['id']: r for r in requirements}
assert len(reqmap) == len(requirements) == 43 and Counter(r['provenance'] for r in requirements) == {'S-literal': 37, 'U': 6}
assert len({c['id'] for c in cases}) == len(cases) == 49
assert set(reqmap) == {rid for c in cases for rid in c['requirements']}
instruction_map = {r['id']: {i['offset']: i for i in r['get_capabilities']['instructions']} for r in declarations}
for requirement in requirements:
    assert requirement['target_applicability'] == 'U' and requirement['complete'] is False and requirement['contract']
    if requirement['provenance'] == 'S-literal':
        assert requirement['source_id'] in instruction_map and requirement['source_offsets']
        assert set(requirement['source_offsets']) <= instruction_map[requirement['source_id']].keys()
    else:
        assert requirement['source_id'] is None and requirement['source_offsets'] == []
for case in cases:
    assert len(case['requirements']) == 1 and case['preconditions'] == ['admitted-context', 'positive-baseline'] and case['setup_and_action']
    requirement = reqmap[case['requirements'][0]]
    assert case['source_id'] == requirement['source_id'] and case['source_offsets'] == requirement['source_offsets']
    assert case['source_claim'] == (requirement['contract'] if requirement['source_id'] else None)
    assert all(case[k] is None for k in ('documentary_expected', 'documentary_comparator', 'expected', 'comparison'))
    assert case['target_grade'] == 'U' and case['executed'] is False
counts = dict(baseline_rows=149, selected_named_APC_entries=8, unselected_rows=141, excluded_family_support_rows=['_APC'],
              retained_init_sources=8, decoded_init_sources=8, decode_failures=0, identity_input_declarations=8,
              port_declarations=sum(len(r['ports']) for r in ledger), auto_load_true_declarations=sum(r['autoload_literal'] is True for r in ledger),
              auto_load_omitted_declarations=sum(r['autoload_literal'] is None for r in ledger),
              opaque_helper_call_nodes=sum(len(r['get_capabilities']['calls']) for r in declarations), complete_profiles=0,
              requirements=43, requirement_grades=dict(Counter(r['provenance'] for r in requirements)), cases=49,
              case_kinds=dict(Counter(c['kind'] for c in cases)), actual_documentary_oracles=0, target_oracles=0)
assert counts == load(P / 'counts.json') and counts['port_declarations'] == 21 and counts['opaque_helper_call_nodes'] == 29
fixture = load(P / 'fixtures.json')
assert len(fixture['not_provided']) == 5
assert all(s in fixture['positive-baseline'] for s in ('genuine profile/device/port', 'nonempty', 'nonzero', 'nonmuted', 'calibrated positive', 'U, never pass'))
sys.path.insert(0, str(ROOT / 'tools'))
from spec_browser import spec_rows
specpath, researchpath = ROOT / 'wiki/specs/apc-controller-capabilities.md', ROOT / 'wiki/research/apc-controller-capabilities.md'
spec = specpath.read_text()
headings = re.findall(r'^### (REQ-APCC-[A-Z0-9-]+) — (.+)$', spec, re.M)
assert len(headings) == 43 and {x[0] for x in headings} == set(reqmap)
for requirement in requirements:
    assert f"### {requirement['id']} — {requirement['title']}\n\n**{requirement['provenance']}/target-U.** {requirement['contract']}" in spec
for case in cases:
    assert f"| {case['id']} | {case['requirements'][0]} | {case['kind']} | {case['title']} |" in spec
browser = spec_rows(specpath, spec)
assert len(browser) == 43 and {r['id'] for r in browser} == set(reqmap)
questions = load(P / 'questions.json')
assert [r['id'] for r in questions] == [f'Q-APCC-{i:03d}' for i in range(1, 7)]
for q in questions:
    assert q['id'] in spec and q['id'] in researchpath.read_text()
links = 0
for path in (specpath, researchpath):
    text = path.read_text()
    match = re.match(r'---\n(.*?)\n---\n', text, re.S)
    assert match
    meta = dict(line.split(': ', 1) for line in match[1].splitlines() if ': ' in line)
    assert {'id', 'type', 'status', 'updated', 'access', 'revision', 'target'} <= meta.keys()
    assert meta['access'] == 'analysis' and meta['status'] == 'draft' and meta['revision'] == '1'
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', text):
        if re.match(r'[A-Za-z]+:', target):
            continue
        name, _, fragment = target.partition('#')
        dest = (path.parent / name).resolve() if name else path
        assert dest.exists(), (path, target)
        if fragment and dest.suffix == '.md':
            assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$', dest.read_text(), re.M)}, (path, target)
        links += 1
manifest = load(P / 'manifest-author-r1.json')
assert manifest['counts'] == counts and len(manifest['files']) == 28
assert set(before) == set(manifest['files']) | {'manifest-author-r1.json'}
for name, record in manifest['files'].items():
    pin(P / name, record)
assert len(manifest['canonical_snapshots']) == 2
for snapshot, canonical in manifest['canonical_snapshots'].items():
    assert (P / snapshot).read_bytes() == (ROOT / canonical).read_bytes()
for path in [specpath, researchpath, P / 'manifest-author-r1.json'] + [P / n for n in manifest['files'] if Path(n).suffix in ('.json', '.md', '.txt', '.py')]:
    if path.suffix == '.json':
        load(path)
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)
assert before == {str(p.relative_to(P)): hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
print(json.dumps(dict(status='pass', scope='Bounded analyst static-literal/source integrity only', **counts,
                      initial_capture_pins=11, baseline_owner_pattern_tool_pins=11, exact_raw_source_pins=8,
                      decoder_selfchecks=selfchecks, frozen_payloads=28, canonical_snapshot_pairs=2,
                      browser_ID_equality=43, local_links_and_anchors=links,
                      all_runtime_documentary_target_oracles_null_U_unexecuted=True, writes=False,
                      original_module_import_exec_eval_function_call=False, hardware_script_candidate_execution=False), indent=2))
