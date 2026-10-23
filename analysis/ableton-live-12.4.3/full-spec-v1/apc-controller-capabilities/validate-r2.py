"""Read-only R2 scope/source checks; original functions remain uncalled."""
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
assert sys.argv[1:] in (['--check'], ['--preflight'])
preflight = sys.argv[1:] == ['--preflight']
assert not preflight or not (P/'manifest-author-r2.json').exists(), 'Preflight only before freeze'
oldmanifest = load(P/'manifest-author-r1.json')
assert hashlib.sha256((P/'manifest-author-r1.json').read_bytes()).hexdigest() == '075be23b9fa4d76667a62df308793b20278a2a3004328bd8a7674c251a75acaa'
assert len(oldmanifest['files']) == 28
for name, record in oldmanifest['files'].items():
    assert pin(P/name,record) == pin(P/'archive-r1'/name,record)
assert (P/'manifest-author-r1.json').read_bytes() == (P/'archive-r1/manifest-author-r1.json').read_bytes()
archive = load(P/'archive-r1-pins.json')
assert len(archive) == 29
for record in archive:
    pin(ROOT/record['path'],record)
assert {str(p.relative_to(ROOT)) for p in (P/'archive-r1').rglob('*') if p.is_file()} == {r['path'] for r in archive}
for record in load(P/'input-pins-r2.json'): pin(ROOT/record['path'],record)
oldreq, oldcases = load(P/'requirements.json'), load(P/'cases.json')
requirements,cases = load(P/'requirements-r2.json'),load(P/'cases-r2.json')
assert requirements == [r for r in oldreq if r['provenance'] == 'U']
reqmap = {r['id']:r for r in requirements}
assert len(reqmap) == len(requirements) == 6
assert cases == [c for c in oldcases if set(c['requirements']) <= set(reqmap)]
assert len(cases) == 12 and len({c['id'] for c in cases}) == 12
assert {r for c in cases for r in c['requirements']} == set(reqmap)
for r in requirements:
    assert r['provenance'] == r['target_applicability'] == 'U' and not r['complete']
    assert r['source_id'] is None and r['source_offsets'] == []
for c in cases:
    assert c['source_id'] is None and c['source_offsets'] == [] and c['source_claim'] is None
    assert all(c[k] is None for k in ('documentary_expected','documentary_comparator','expected','comparison'))
    assert c['target_grade'] == 'U' and c['executed'] is False
    assert c['preconditions'] == ['admitted-context','positive-baseline'] and c['setup_and_action']
metadata,retired_cases = load(P/'declaration-research-r2.json'),load(P/'declaration-case-ledger-r2.json')
assert len(metadata) == len(retired_cases) == 37
assert {r['retired_requirement_id'] for r in metadata} == {r['id'] for r in oldreq if r['provenance']=='S-literal'}
assert set(reqmap).isdisjoint(r['retired_requirement_id'] for r in metadata)
assert len({r['id'] for r in metadata}) == 37
expected_retired_cases = []
for r in metadata:
    old = oldreq[int(r['r1_requirement_pointer'][1:])]
    assert old['id'] == r['retired_requirement_id'] and r['id'] == old['id'].replace('REQ-','META-',1)
    assert r['title'] == old['title'] and r['declaration_fact'] == old['contract']
    assert r['source_id'] == old['source_id'] and r['source_offsets'] == old['source_offsets']
    assert r['role'] == 'nonnormative-static-declaration-research' and r['target_applicability']=='U'
    assert r['source_strength'] == 'S-literal research data only' and r['observable_contract_supported'] is False and r['behavioral_coverage_credit']==0
    declared = next(d for d in declarations if d['id']==r['source_id'])
    assert set(r['source_offsets']) <= {x['offset'] for x in declared['get_capabilities']['instructions']}
    for i,c in enumerate(oldcases):
        if c['requirements']==[old['id']]:
            expected_retired_cases.append(dict(metadata_id=r['id'],role='retired-metadata-proposal-not-normative-case',r1_case_pointer='/'+str(i),original_case=c))
assert retired_cases == expected_retired_cases
assert {r['original_case']['id'] for r in retired_cases}.isdisjoint(c['id'] for c in cases)
assert len(cases)+len(retired_cases)==len(oldcases)==49
counts=load(P/'counts-r2.json')
assert counts == dict(baseline_rows=149,selected_named_APC_entries=8,unselected_rows=141,excluded_family_support_rows=['_APC'],retained_init_sources=8,decoded_init_sources=8,decode_failures=0,identity_input_declarations=8,port_declarations=21,auto_load_true_declarations=3,auto_load_omitted_declarations=5,opaque_helper_call_nodes=29,research_declaration_records=37,retired_metadata_case_records=37,requirements=6,requirement_grades={'U':6},cases=12,actual_documentary_oracles=0,target_oracles=0,supported_runtime_contracts=0,complete_profiles=0,behavioral_coverage_credit=0)
response=load(P/'response-r2.json')
assert response['finding']=='APCC-REVIEW-001' and response['counts']==counts
assert response['retired_ids']==[r['retired_requirement_id'] for r in metadata]
assert response['current_ids']==[r['id'] for r in requirements]
pin(ROOT/response['review']['path'], response['review'])
review=load(ROOT/response['review']['path'])
assert review['reviewed_manifest_sha256']==hashlib.sha256((P/'manifest-author-r1.json').read_bytes()).hexdigest()
assert review['required_findings'][0]['id']==response['finding']
fixture=load(P/'fixtures.json')
assert all(s in fixture['positive-baseline'] for s in ('genuine profile/device/port','nonempty','nonzero','nonmuted','calibrated positive','U, never pass'))
sys.path.insert(0,str(ROOT/'tools'))
from spec_browser import spec_rows
specpath=ROOT/'wiki/specs/apc-controller-capabilities.md';researchpath=ROOT/'wiki/research/apc-controller-capabilities.md'
spec=specpath.read_text();research=researchpath.read_text()
headings=re.findall(r'^### (REQ-APCC-[A-Z0-9-]+) — (.+)$',spec,re.M)
assert len(headings)==6 and {r[0] for r in headings}==set(reqmap)
rows=spec_rows(specpath,spec)
assert len(rows)==6 and {r['id'] for r in rows}==set(reqmap)
assert not re.search(r'^### REQ-',research,re.M)
for r in requirements:
    assert f"### {r['id']} — {r['title']}\n\n**U/target-U.** {r['contract']}" in spec
for c in cases: assert f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} |" in spec
assert not any(r['retired_requirement_id'] in spec for r in metadata)
for q in load(P/'questions.json'): assert q['id'] in spec and q['id'] in research
links=0
for path in (specpath,researchpath):
    text=path.read_text();match=re.match(r'---\n(.*?)\n---\n',text,re.S);assert match
    meta=dict(line.split(': ',1) for line in match[1].splitlines() if ': ' in line)
    assert meta['revision']=='2' and meta['access']=='analysis' and meta['status']=='draft'
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',text):
        if re.match(r'[A-Za-z]+:',target):continue
        name,_,fragment=target.partition('#');dest=(path.parent/name).resolve() if name else path
        if preflight and dest==P/'manifest-author-r2.json':continue
        assert dest.exists(),(path,target)
        if fragment and dest.suffix=='.md':assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)},(path,target)
        links+=1
assert (P/'spec-r2.md').read_bytes()==specpath.read_bytes()
assert (P/'research-r2.md').read_bytes()==researchpath.read_bytes()
if not preflight:
    manifest=load(P/'manifest-author-r2.json')
    assert manifest['counts']==counts and manifest['prior_manifest_sha256']==response['r1_manifest']['sha256']
    assert set(before)==set(manifest['files'])|{'manifest-author-r2.json'}
    for name,record in manifest['files'].items():pin(P/name,record)
    assert manifest['canonical_snapshots']=={'spec-r2.md':'wiki/specs/apc-controller-capabilities.md','research-r2.md':'wiki/research/apc-controller-capabilities.md'}
for path in [specpath,researchpath]+[P/n for n in before if Path(n).suffix in ('.json','.md','.txt','.py')]:
    if path.suffix=='.json':load(path)
    result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(path)],capture_output=True,text=True)
    assert result.returncode in (0,1) and not result.stdout and not result.stderr,(path,result.stdout,result.stderr)
assert before=={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',counts=counts,source_pins=8,original_R1_payloads_preserved=28,archive_R1_files=29,research_records=37,retired_metadata_cases=37,current_browser_ID_equality=6,current_cases=12,decoder_selfchecks=selfchecks,canonical_snapshot_pairs=2,local_links=links,writes=False,original_module_function_helper_execution=False),indent=2))
