"""Read-only narrow Monitoring R2 checks; no historical/vendor runtime execution."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import ast
import json
import re
import runpy
import subprocess
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
B = P.parent
assert sys.dont_write_bytecode, 'Use -B'
assert sys.argv[1:] in (['--check'], ['--preflight'])
preflight = sys.argv[1:] == ['--preflight']
assert not preflight or not (P/'manifest-author-r2.json').exists(), 'Preflight only before author seal'
load = lambda p: json.loads(p.read_text())


def digest(p):
    data = p.read_bytes()
    return dict(bytes=len(data), sha256=sha256(data).hexdigest())


def pin(p, record):
    assert digest(p) == {k: record[k] for k in ['bytes', 'sha256']}, p


def pointer(value, path):
    for k in path.lstrip('/').split('/') if path else []:
        k = k.replace('~1', '/').replace('~0', '~')
        value = value[int(k)] if isinstance(value, list) else value[k]
    return value


def check_catalogs(reqs, cases, oldreq, oldcases, adoption):
    assert reqs[:40] == oldreq and len(reqs) == len({r['id'] for r in reqs}) == 41
    assert [c['id'] for c in cases[:69]] == [c['id'] for c in oldcases]
    assert len(cases) == len({c['id'] for c in cases}) == 70
    for a, c in zip(oldcases, cases):
        assert set(a) == set(c)
        for k, v in a.items():
            if a['id'] == 'RML-009' and k == 'setup_and_action':
                continue
            assert c[k] == v, (a['id'], k)
    assert reqs[-1]['id'] == 'REQ-RML-036' and cases[-1]['id'] == 'RML-070'
    assert reqs[-1]['source_blocks'] == cases[-1]['source_blocks'] == ['routing:B013']
    assert reqs[-1]['provenance'] == 'D12' and reqs[-1]['target_applicability'] == 'U'
    assert Counter(r['provenance'] for r in reqs) == {'D12': 36, 'U': 5}
    rm = {r['id']: r for r in reqs}
    assert {rid for c in cases for rid in c['requirements']} == set(rm)
    for r in reqs:
        assert r['target_applicability'] == 'U'
    for c in cases:
        assert c['expected'] is c['comparison'] is None
        assert c['target_grade'] == 'U' and c['executed'] is False
        assert len(c['requirements']) == 1
        r = rm[c['requirements'][0]]
        assert c['source_blocks'] == r['source_blocks']
        if c['kind'] == 'signal' or r['provenance'] == 'U':
            assert c['documentary_expected'] is c['documentary_comparator'] is None
        else:
            assert c['documentary_expected'] == r['contract']
    assert cases[-1]['preconditions'] == ['F0', 'positive-path-gate', 'F-MONITOR-INDICATOR']
    assert 'genuinely visible source-described blue In Activator indicator positive baseline' in cases[-1]['setup_and_action']
    assert 'independently verify actual Monitor In state' in cases[-1]['setup_and_action']
    assert 'actually right-click the corresponding In or Auto Monitor button' in cases[8]['setup_and_action']
    assert 'Off-mode availability' in cases[8]['setup_and_action']
    assert adoption['already_represented'] == ['RML-006 full arm/clip/mode matrix', 'RML-007 selected Monitor dispatch', 'RML-008 Delete and Edit Return to Default']
    assert adoption['new_duplicate_matrix_reset_selected_cases'] == 0
    assert adoption['complete_topics'] == 0 and adoption['all_target_U'] is True


before = {str(p.relative_to(P)): digest(p) for p in P.rglob('*') if p.is_file()}
assert not any('__pycache__' in n for n in before)
inputs = load(P/'inputs-r2.json')
assert len(inputs) == len({r['path'] for r in inputs}) == 58
assert not any(r['path'].startswith('wiki/') for r in inputs)
external_before = {r['path']: digest(ROOT/r['path']) for r in inputs}
for r in inputs:
    pin(ROOT/r['path'], r)
prior = load(P/'prior-files-r2.json')
assert len(prior) == 19
for name, rec in prior.items():
    pin(P/name, rec)
assert digest(P/'manifest-author-r1.json')['sha256'] == '5a80e84823f4e8381446f65c5eb4824adbd61311efc1e4966b0194e0da29d6b3'
for name, rec in load(P/'manifest-author-r1.json')['files'].items():
    pin(P/name, rec)
for kind in ['spec', 'research']:
    assert (P/f'{kind}-before-r2.md').read_bytes() == (P/f'{kind}-r1.md').read_bytes()
for source in load(P/'sources.json'):
    pin(Path(source['path']), source)

adoption = load(P/'source-adoption-r2.json')
for field in ['companion_manifest', 'independent_review']:
    pin(ROOT/adoption[field]['path'], adoption[field])
assert adoption['companion_manifest']['sha256'] == '344a039d9df7bf3dac85e2f7bc72796f652f431fec5755e891fa8afaeea93a8a'
review = load(ROOT/adoption['independent_review']['path'])
assert review['findings'] == [] and review['disposition'] == 'approved-as-partial-source-reconciliation'
assert review['reviewed_manifest_sha256'] == adoption['companion_manifest']['sha256']
C = B/'monitoring-source-reconciliation'
selected = load(C/'selected-source.json')
assert selected['blocks'] == load(P/'manual-routing-blocks.json')[8:17]
assert selected['compensation_context'] == load(P/'manual-compensation-blocks.json')
context = load(C/'source-context.json')
sl = context['raw_selection']
raw = (ROOT/sl['source_path']).read_text()
fragment = raw[sl['character_start']:sl['character_end_exclusive']]
assert fragment == (C/sl['file']).read_text()
# Inspected pure analyst parser class; its checker/sealing main never runs.
parser = runpy.run_path(str(C/'check.py'))['Extract']()
parser.feed(fragment)
assert [(r['tag'], r['text']) for r in parser.blocks] == [(r['kind'], r['text']) for r in selected['blocks']]
assert 'blue color of the track’s Activator switch' in selected['blocks'][4]['text']
assert 'right-click on the “In” or “Auto” monitor buttons' in selected['blocks'][6]['text']
proposals = load(C/'proposals.json')
assert [(a['proposal'], a['source_block']) for a in adoption['adoptions']] == [('MON-P01', 'routing:B013'), ('MON-P02', 'routing:B015')]
for a in adoption['adoptions']:
    proposal = pointer(proposals, a['proposal_pointer'])
    assert proposal['id'] == a['proposal'] and proposal['source_facets'] == [a['facet']]
    assert proposal['expected'] is proposal['comparison'] is None

oldreq, oldcases = load(P/'requirements.json'), load(P/'cases.json')
reqs, cases = load(P/'requirements-r2.json'), load(P/'cases-r2.json')
check_catalogs(reqs, cases, oldreq, oldcases, adoption)
delta = load(P/'delta-r2.json')
assert delta['old_manifest_sha256'] == digest(P/'manifest-author-r1.json')['sha256']
assert delta['old_requirements_identity'] == digest(P/'requirements.json')
assert delta['old_cases_identity'] == digest(P/'cases.json')
assert delta['old_requirements_verbatim'] == 40 and delta['old_cases_preserved_ids'] == 69
assert delta['sole_changed_field'] == dict(case='RML-009', pointer='/8/setup_and_action', old=oldcases[8]['setup_and_action'], new=cases[8]['setup_and_action'])
assert pointer(oldcases, delta['sole_changed_field']['pointer']) == delta['sole_changed_field']['old']
assert pointer(cases, delta['sole_changed_field']['pointer']) == delta['sole_changed_field']['new']
assert delta['new_requirement_ids'] == ['REQ-RML-036'] and delta['new_case_ids'] == ['RML-070']
fixture = load(P/'fixtures-r2.json')
for k, v in load(P/'fixtures.json').items():
    if k != 'id':
        assert fixture[k] == v
assert 'genuinely visible blue In Activator indicator positive baseline' in fixture['F-MONITOR-INDICATOR']
assert 'never a passing absence test' in fixture['F-MONITOR-INDICATOR']
finite = load(P/'finite-contexts-r2.json')
assert set(finite) == {'RML-009', 'RML-070'}
assert finite['RML-009']['monitor_modes'] == ['In', 'Auto'] and finite['RML-009']['option_choices'] == ['off', 'on']
assert finite['RML-070']['track_types'] == ['audio', 'MIDI'] and len(finite['RML-070']['reset_IO_states']) == 3
assert finite['RML-070']['RGB_theme_other_modes_audio_timing_oracle'] is None

for mutation in ['wrong-source', 'false-missing-context', 'invented-oracle', 'weaken-indicator-baseline']:
    rr, cc, aa = deepcopy(reqs), deepcopy(cases), deepcopy(adoption)
    if mutation == 'wrong-source':
        rr[-1]['source_blocks'] = cc[-1]['source_blocks'] = ['routing:B015']
    elif mutation == 'false-missing-context':
        aa['already_represented'][1] = 'missing RML-007 multiselect'
    elif mutation == 'invented-oracle':
        cc[-1]['comparison'] = 'fabricated actual blue-color pass'
    else:
        cc[-1]['setup_and_action'] = cc[-1]['setup_and_action'].replace('genuinely visible source-described blue In Activator indicator positive baseline', 'available Monitor control')
    try:
        check_catalogs(rr, cc, oldreq, oldcases, aa)
    except AssertionError:
        pass
    else:
        raise AssertionError('Mutation accepted: '+mutation)

impact = load(P/'consumer-impact-r2.json')
assert len(impact['direct_canonical_hash_records']) == 18
for r in impact['direct_canonical_hash_records']:
    pin(ROOT/r['consumer'], r['consumer_identity'])
    assert pointer(load(ROOT/r['consumer']), r['record_pointer']) == r['record']
    pin(ROOT/r['historical_snapshot']['path'], r['historical_snapshot'])
    pin(ROOT/r['historical_snapshot']['path'], r['record'])
for r in impact['exact_before_canonicals']:
    pin(ROOT/r['snapshot'], r)
assert 'does not automatically trigger' in impact['current_policy']

specpath = ROOT/'wiki/specs/routing-monitoring-latency.md'
researchpath = ROOT/'wiki/research/routing-monitoring-latency.md'
canonical_before = {str(p): digest(p) for p in [specpath, researchpath]}
for canonical, snapshot in [(specpath, P/'spec-r2.md'), (researchpath, P/'research-r2.md')]:
    assert canonical.read_bytes() == snapshot.read_bytes() and '\nrevision: 2\n' in canonical.read_text()
    assert 'AS-OF AUTHOR FREEZE' in canonical.read_text()
spec = specpath.read_text()
for r in reqs:
    assert f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}" in spec
for c in cases:
    grade = 'visible control/state only' if c['documentary_expected'] is not None else 'U / null'
    assert f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} | {grade} |" in spec
tree = ast.parse((ROOT/'tools/spec_browser.py').read_text())
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'anchor', 'frontmatter', 'cells', 'spec_rows'}]
assert len(functions) == 4
ns = {'re': re}
exec(compile(ast.Module(body=functions, type_ignores=[]), 'analyst-browser-parser-functions', 'exec'), ns)
rows = ns['spec_rows'](specpath, spec)
assert len(rows) == 41 and {r['id'] for r in rows} == {r['id'] for r in reqs}
counts = load(P/'counts-r2.json')
assert counts == dict(requirements=41, requirement_grades={'D12':36, 'U':5}, cases=70,
                     documentary_oracles=34, null_documentary_oracles=36, target_oracles=0,
                     old_requirement_records_verbatim=40, old_case_ids_preserved=69, prior_action_fields_refined=1,
                     new_requirement_ids=1, new_case_ids=1, proposals_adopted_as_bounded_subsets=2, complete_topics=0)
assert sum(c['documentary_expected'] is not None for c in cases) == 34
links = 0
for path in [specpath, researchpath, P/'README-r2.md']:
    for target in re.findall(r'\]\(([^)\s]+)\)', path.read_text()):
        if re.match(r'[A-Za-z]+:', target):
            continue
        filename, _, fragment = target.partition('#')
        dest = (path.parent/filename).resolve() if filename else path
        if preflight and dest == P/'manifest-author-r2.json':
            continue
        assert dest.is_file(), (path, target)
        if fragment and dest.suffix == '.md':
            assert fragment in {ns['anchor'](h) for h in re.findall(r'^#+\s+(.+)$', dest.read_text(), re.M)}, (path, target)
        links += 1
for path in [specpath, researchpath]+[P/n for n in before if n not in prior]:
    if path.suffix == '.json':
        load(path)
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)
if not preflight:
    manifest = load(P/'manifest-author-r2.json')
    assert manifest['counts'] == counts and set(before) == set(manifest['files']) | {'manifest-author-r2.json'}
    for name, r in manifest['files'].items():
        pin(P/name, r)
assert before == {str(p.relative_to(P)): digest(p) for p in P.rglob('*') if p.is_file()}
assert external_before == {r['path']: digest(ROOT/r['path']) for r in inputs}
assert canonical_before == {str(p): digest(p) for p in [specpath, researchpath]}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen', counts=counts,
                      prior_files_preserved=19, immutable_input_pins=58, consumer_pointer_records=18,
                      source_subsection_blocks_reconstructed=9, unchanged_historical_source_blocks=226,
                      browser_exact_ids=41, local_links=links, rejection_fixtures=4,
                      old_validators_or_consumers_replayed=False, writes=False, original_runtime_network_hardware_execution=False), indent=2))
