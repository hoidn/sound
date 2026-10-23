"""Finite read-only Mixing R2 checks. No original/runtime/old validator execution."""
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
assert not preflight or not (P/'manifest-author-r2.json').exists(), 'Preflight only before seal'
load = lambda p: json.loads(p.read_text())


def digest(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=sha256(b).hexdigest())


def pin(p, record):
    assert digest(p) == {k: record[k] for k in ['bytes', 'sha256']}, p


def pointer(value, path):
    for key in path.lstrip('/').split('/') if path else []:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def check_cases(current, old, reqs, delta):
    assert len(current) == len({c['id'] for c in current}) == 50
    assert [c['id'] for c in current[:33]] == [c['id'] for c in old]
    assert [c['id'] for c in current[33:]] == delta['new_case_ids']
    permitted = {d['id'] for d in delta['refined_actions']}
    for prior, c in zip(old, current):
        assert set(c) == set(prior)
        for key, value in prior.items():
            if key == 'setup_and_action' and c['id'] in permitted:
                continue
            assert c[key] == value, (c['id'], key)
    for c in current:
        assert set(c['requirements']) <= set(reqs)
        assert c['preconditions'] == ['owned-context', 'positive-guard']
        assert c['expected'] is c['comparison'] is None
        assert c['target_grade'] == 'U' and c['executed'] is False
        assert len(c['setup_and_action']) > 100
        if c['kind'] in {'unresolved', 'signal', 'file', 'timing', 'transform'} or c['id'] in {'MXW-003', 'MXW-007'}:
            assert c['documentary_expected'] is c['documentary_comparator'] is None
        if c['id'].startswith('MXW-U-'):
            assert c['source_claim'] is None
        else:
            assert c['source_claim'] == reqs[c['requirements'][0]]['contract']
    assert {rid for c in current for rid in c['requirements']} == set(reqs)
    cm = {c['id']: c['setup_and_action'] for c in current}
    assert 'prove each mapped key independently genuinely changes' in cm['MXW-016']
    assert 'EACH mapped key independently genuinely changes' in cm['MXW-U-CROSSFADE-UNDO']
    assert 'genuinely playing nonempty contained clips' in cm['MXW-U-GROUP-SLOT']
    assert 'genuinely UNARMED before-state' in cm['MXW-U-ARM-INSERT']
    assert 'NEW versus EMPTY' in cm['MXW-U-ARM-INSERT'] and 'actually inserted/accepted' in cm['MXW-U-ARM-INSERT']
    assert 'noncenter pan' in cm['MXW-018'] and 'Solo in Place ON then OFF' in cm['MXW-018']
    assert 'Solo button context menu' in cm['MXW-029'] and 'Options menu default entry' in cm['MXW-029']
    assert 'A/C' in cm['MXW-006'] and 'drag-drop' in cm['MXW-006'] and 'Ctrl+arrow' in cm['MXW-006']
    assert 'one-clip' not in cm['MXW-008'] or cm['MXW-008'] == old[7]['setup_and_action']
    assert 'two independently known owned clips' in cm['MXW-027'] and 'same known source track' in cm['MXW-027']


def check_delta(delta, old, current):
    changes = [dict(id=a['id'], old_pointer=f'/{i}/setup_and_action', new_pointer=f'/{i}/setup_and_action',
                    old_action=a['setup_and_action'], new_action=b['setup_and_action'])
               for i, (a, b) in enumerate(zip(old, current)) if a['setup_and_action'] != b['setup_and_action']]
    assert delta['refined_actions'] == changes and len(changes) == 8
    assert {d['id'] for d in changes} == {'MXW-001', 'MXW-005', 'MXW-006', 'MXW-009', 'MXW-013', 'MXW-016', 'MXW-017', 'MXW-018'}
    for d in changes:
        assert pointer(old, d['old_pointer']) == d['old_action']
        assert pointer(current, d['new_pointer']) == d['new_action']


before = {str(p.relative_to(P)): digest(p) for p in P.rglob('*') if p.is_file()}
assert not any('__pycache__' in n for n in before)
inputs = load(P/'inputs-r2.json')
assert len(inputs) == len({r['path'] for r in inputs}) == 62
assert not any(r['path'].startswith('wiki/') for r in inputs)
external_before = {r['path']: digest(ROOT/r['path']) for r in inputs}
for r in inputs:
    pin(ROOT/r['path'], r)
prior = load(P/'prior-files-r2.json')
assert len(prior) == 13
for name, record in prior.items():
    pin(P/name, record)
assert digest(P/'manifest-author-r1.json')['sha256'] == '7d1fd0bcb36be47060757b3055a8b25dbb633b7a497202306984a984b0c37e2b'
for name, record in load(P/'manifest-author-r1.json')['files'].items():
    pin(P/name, record)
for kind in ['spec', 'research']:
    assert (P/f'{kind}-before-r2.md').read_bytes() == (P/f'{kind}-r1.md').read_bytes()

source = load(P/'source.json')
pin(Path(source['path']), source)
assert source == load(B/'routing-monitoring/mixing-capture.json')
# Inspected analyst parser only; guarded source writer main remains inactive.
parser = runpy.run_path(str(B/'routing-monitoring/capture.py'))['Extract']('mixing')
parser.feed(Path(source['path']).read_text())
for i, b in enumerate(parser.rows, 1):
    b['locator'] = f'mixing:B{i:03}'
blocks = load(P/'source-blocks.json')
assert parser.rows == blocks and len(blocks) == 94
bm = {b['locator']: b for b in blocks}
oldreq, oldcases = load(P/'requirements.json'), load(P/'cases.json')
req, cases = load(P/'requirements-r2.json'), load(P/'cases-r2.json')
assert req[:23] == oldreq and len(req) == len({r['id'] for r in req}) == 31
assert Counter(r['provenance'] for r in req) == {'D12': 26, 'U': 5}
rm = {r['id']: r for r in req}
for r in req:
    assert r['target_applicability'] == 'U'
    for e in r['evidence']:
        assert e['anchor'] == bm[e['block']]['anchor'] and e['html_line'] == bm[e['block']]['html_line']
for c in cases[33:]:
    for e in c['evidence']:
        assert e['anchor'] == bm[e['block']]['anchor'] and e['html_line'] == bm[e['block']]['html_line']
delta = load(P/'delta-r2.json')
assert delta['old_manifest_sha256'] == digest(P/'manifest-author-r1.json')['sha256']
assert delta['old_requirements_identity'] == digest(P/'requirements.json')
assert delta['old_cases_identity'] == digest(P/'cases.json')
assert delta['old_requirements_verbatim'] == 23 and delta['old_case_ids_preserved'] == 33
assert delta['allowed_prior_case_field_changes'] == ['setup_and_action']
assert delta['new_requirement_ids'] == [r['id'] for r in req[23:]]
check_cases(cases, oldcases, rm, delta)
check_delta(delta, oldcases, cases)
assert cases[11] == oldcases[11]  # Active-view color/members/control remain exact.
contexts = load(P/'finite-contexts-r2.json')
assert set(contexts) == {d['id'] for d in delta['refined_actions']} | set(delta['new_case_ids'])
assert contexts['MXW-027']['selected_clip_count'] == 2
assert contexts['MXW-016']['fields'] == ['left', 'center', 'right']
assert contexts['MXW-018']['SoloInPlace'] == contexts['MXW-029']['SoloInPlace'] == ['ON', 'OFF']
assert len(contexts['MXW-026']['TrackOptions_entries']) == 3
assert contexts['MXW-U-GROUP-SLOT']['source_law_choice'] is None
fixture = load(P/'fixtures-r2.json')
assert fixture['target'] == 'U' and fixture['executed'] is False
assert fixture['application_expected'] is fixture['application_comparison'] is None
for text in ['genuinely productive operation', 'Each mapped key must independently change value', 'genuinely playing nonempty child clips', 'genuinely unarmed', 'noncenter pan', 'never a negative pass']:
    assert text in fixture['positive-guard']

adopt = load(P/'audit-adoption-r2.json')
pin(ROOT/adopt['audit_manifest']['path'], adopt['audit_manifest'])
pin(ROOT/adopt['audit_review']['path'], adopt['audit_review'])
assert adopt['audit_manifest']['sha256'] == '0f48108a114597822a3e83763859beefaa5059efea79cc91816175c69cef9e94'
review = load(ROOT/adopt['audit_review']['path'])
assert review['findings'] == [] and review['disposition'] == 'approved-as-partial-retained-source-audit'
assert review['reviewed_manifest_sha256'] == adopt['audit_manifest']['sha256']
proposals = load(B/'mixing-source-audit/proposed-deltas.json')
claims = load(B/'mixing-source-audit/claims.json')
assert [g['id'] for g in adopt['groups']] == [g['id'] for g in proposals]
for group, proposal in zip(adopt['groups'], proposals):
    assert pointer(proposals, group['audit_proposal_pointer']) == proposal
    assert group['audit_proposal_sha256'] == sha256(json.dumps(proposal, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    assert group['audit_claim_ids'] == [c['id'] for c in claims if group['id'] in c['gaps']]
    assert set(group['current_requirement_ids']) <= set(rm)
    assert set(group['current_case_ids']) <= {c['id'] for c in cases}
    assert group['remaining'] and group['target'] == 'U' and group['complete'] is False
assert adopt['local_role_or_action_groups'] == 14 and adopt['U_only_cross_owner_or_recommendation_groups'] == ['M09', 'M10', 'M17']
assert adopt['fully_closed_groups'] == adopt['new_behavioral_completion_credit'] == 0

impact = load(P/'consumer-impact-r2.json')
for rec in impact['canonical_before']:
    pin(ROOT/rec['snapshot'], rec)
for rec in impact['records']:
    pin(ROOT/rec['consumer'], rec['consumer_identity'])
    if 'record_pointer' in rec:
        original = pointer(load(ROOT/rec['consumer']), rec['record_pointer'])
        snap = rec['historical_snapshot']
        pin(ROOT/snap['path'], snap)
        assert original['sha256'] == snap['sha256'] and original['bytes'] == snap['bytes']
        assert 'as-of' in rec['role']
for rec in load(P/'owner-boundaries-r2.json'):
    assert rec['excerpt_sha256'] == sha256(rec['excerpt'].encode()).hexdigest()
    assert 'not a mutable inputpin' in rec['role']

# Meaningful omission/weakening/pointer/oracle fixtures act only on memory copies.
for mutation in ['drop-positive-key-baseline', 'weaken-playing-child-baseline', 'promote-target-oracle', 'alter-preserved-color-case', 'wrong-action-pointer']:
    cc, dd = deepcopy(cases), deepcopy(delta)
    if mutation == 'drop-positive-key-baseline':
        next(c for c in cc if c['id'] == 'MXW-016')['setup_and_action'] = next(c for c in cc if c['id'] == 'MXW-016')['setup_and_action'].replace('prove each mapped key independently genuinely changes', 'accept mapping for')
    elif mutation == 'weaken-playing-child-baseline':
        next(c for c in cc if c['id'] == 'MXW-U-GROUP-SLOT')['setup_and_action'] = next(c for c in cc if c['id'] == 'MXW-U-GROUP-SLOT')['setup_and_action'].replace('genuinely playing nonempty contained clips', 'available clips')
    elif mutation == 'promote-target-oracle':
        cc[-1]['expected'] = 'fabricated actual result'
    elif mutation == 'alter-preserved-color-case':
        cc[11]['setup_and_action'] = 'Only inspect active clips without nonmember control.'
    else:
        dd['refined_actions'][0]['new_pointer'] = '/1/setup_and_action'
    try:
        check_cases(cc, oldcases, rm, dd)
        check_delta(dd, oldcases, cc)
    except AssertionError:
        pass
    else:
        raise AssertionError('Fixture was not rejected: '+mutation)

specpath = ROOT/'wiki/specs/mixing-workflows.md'
researchpath = ROOT/'wiki/research/mixing-workflows.md'
for canonical, snap in [(specpath, P/'spec-r2.md'), (researchpath, P/'research-r2.md')]:
    assert canonical.read_bytes() == snap.read_bytes() and 'revision: 2\n' in canonical.read_text()
spec = specpath.read_text()
for r in req:
    assert f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}" in spec
# Reuse only the four inspected pure Browser parsing functions, without building output.
tree = ast.parse((ROOT/'tools/spec_browser.py').read_text())
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'anchor', 'frontmatter', 'cells', 'spec_rows'}]
assert len(functions) == 4
ns = {'re': re}
exec(compile(ast.Module(body=functions, type_ignores=[]), 'analyst-browser-parser-functions', 'exec'), ns)
rows = ns['spec_rows'](specpath, spec)
assert len(rows) == 31 and {r['id'] for r in rows} == set(rm)
counts = load(P/'counts-r2.json')
assert counts == dict(requirements=31, provenance={'D12':26, 'U':5}, cases=50, visible_documentary_cases=21, null_documentary_cases=29,
                     all_actual_null_U_unexecuted=True, old_requirements_verbatim=23, old_case_ids=33, action_only_refinements=8,
                     new_requirements=8, new_cases=17, audit_groups_addressed=17, local_role_or_action_groups=14,
                     U_only_groups=3, source_blocks=94, complete_topics=0)
assert sum(c['documentary_expected'] is not None for c in cases) == 21
links = 0
for path in [specpath, researchpath, P/'README-r2.md']:
    for target in re.findall(r'\]\(([^)\s]+)\)', path.read_text()):
        if re.match(r'[A-Za-z]+:', target):
            continue
        name, _, fragment = target.partition('#')
        dest = (path.parent/name).resolve() if name else path
        if preflight and dest == P/'manifest-author-r2.json':
            continue
        assert dest.is_file(), (path, target)
        if fragment and dest.suffix == '.md':
            assert fragment in {ns['anchor'](h) for h in re.findall(r'^#+\s+(.+)$', dest.read_text(), re.M)}, (path, target)
        links += 1
newfiles = [P/n for n in before if n not in prior]
for path in [specpath, researchpath]+newfiles:
    if path.suffix == '.json':
        load(path)
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)
if not preflight:
    manifest = load(P/'manifest-author-r2.json')
    assert manifest['counts'] == counts
    assert set(before) == set(manifest['files']) | {'manifest-author-r2.json'}
    for name, record in manifest['files'].items():
        pin(P/name, record)
assert before == {str(p.relative_to(P)): digest(p) for p in P.rglob('*') if p.is_file()}
assert external_before == {r['path']: digest(ROOT/r['path']) for r in inputs}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen', counts=counts,
                      prior_files_preserved=13, immutable_inputs=len(inputs), browser_exact_ids=31, local_links=links,
                      rejection_fixtures=5, historical_consumers_edited_or_replayed=False,
                      original_runtime_network_hardware_execution=False, writes=False), indent=2))
