"""Finite read-only association correction; no historical main or source execution."""
import ast
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import sys

P = Path(__file__).resolve().parent
R = P.parents[3]
F = P.parent
D = F / 'sample-instruments'


def load(path):
    return json.loads(path.read_text())


def dg(path):
    raw = path.read_bytes()
    return dict(bytes=len(raw), sha256=sha256(raw).hexdigest())


def differences(before, after, prefix=''):
    assert type(before) is type(after), prefix
    if isinstance(before, dict):
        assert before.keys() == after.keys(), prefix
        return sum((differences(before[k], after[k], prefix + '/' + k) for k in before), [])
    if isinstance(before, list):
        # Changed lists are single literal replacements in this finite ledger.
        return [] if before == after else [(prefix, before, after)]
    return [] if before == after else [(prefix, before, after)]


def corrected(plan, ledger):
    """Only six fixed manual-plan fields; no generic patch application."""
    rows = {(x['catalog'], x['pointer']): x['after'] for x in ledger['changes']}
    result = deepcopy(plan)
    for i in (95, 99, 259):
        result['judgments'][i]['assessment'] = rows['plan', f'/judgments/{i}/assessment']
    result['judgments'][99]['proposal_numbers'] = rows['plan', '/judgments/99/proposal_numbers']
    result['judgments'][259]['proposal_numbers'] = rows['plan', '/judgments/259/proposal_numbers']
    result['proposals'][6]['proposed_minimal_delta'] = rows['plan', '/proposals/6/proposed_minimal_delta']
    return result


def focused(a):
    x, y, z = (a['assessments'][i] for i in (95, 99, 259))
    assert x['local_block'] == 'sampler:B074' and y['local_block'] == 'sampler:B078'
    assert z['local_block'] == 'simpler:B040'
    assert a['owner_cases'][45]['action'] == 'Select A, set Detune +25 cents; select B.'
    assert 'chooser and editor follow the selected layer' in a['owner_cases'][45]['expected']
    assert 'Warp as 2 bars' in a['owner_cases'][17]['setup']
    assert a['owner_cases'][17]['action'] == 'Choose ÷2 then reset and choose ×2.'
    assert 'does not invoke the Sample chooser' in x['assessment']
    assert 'not actual selection via the Sample chooser' in y['assessment']
    assert 'expected chooser DISPLAY' in y['assessment']
    assert x['open_proposal_groups'] == y['open_proposal_groups'] == ['SISA-G18']
    assert 'SETUP' in z['assessment'] and 'does not exercise the Warp as button' in z['assessment']
    assert 'actually chooses ÷2, resets, then chooses ×2' in z['assessment']
    assert z['open_proposal_groups'] == ['SISA-G07']
    g = a['proposals'][6]['proposed_minimal_delta']
    assert 'SETUP and actual ÷2/reset/×2' in g
    assert 'explicitly invoke the Warp as button in a separate reset trial' in g
    assert 'independently admitted NONEMPTY sample and productive Warp/output history' in g
    assert 'no numeric or timing result oracle' in g


def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only'
    ledger = load(P / 'correction-r2.json')
    inputs = load(P / 'inputs.json')
    watch = {R / x['path'] for x in inputs['files']} | {p for p in P.iterdir() if p.is_file()} | {R / ledger['review']['path']}
    before = {str(p): dg(p) for p in watch}
    assert dg(P / 'manifest.json')['sha256'] == '595a14d9fcc40a1d14ec4bff87c53dc3fb180c81d4fedc4659ca8d811cdace99'
    old_manifest = load(P / 'manifest.json')
    assert len(old_manifest['files']) == 5
    for name, pin in old_manifest['files'].items():
        assert dg(P / name) == pin
    assert len(inputs['files']) == 68
    for x in inputs['files']:
        assert not x['path'].startswith('wiki/')
        assert dg(R / x['path']) == {k: x[k] for k in ('bytes', 'sha256')}
    review = ledger['review']
    assert review['sha256'] == '32faa7404b5b6efc41f629ac15cb1f7d1c1b27722a934f7aeb2529ece25769ec'
    assert dg(R / review['path']) == {k: review[k] for k in ('bytes', 'sha256')}
    for root, name, count in [(D, 'manifest-author-r2.json', 35), (D / 'revisions/r1', 'manifest-author-r1.json', 28)]:
        previous = load(root / name)
        assert len(previous['payloads']) == count
        for item in previous['payloads']:
            assert dg(root / item['path']) == {k: item[k] for k in ('bytes', 'sha256')}
    # Reuse only explicitly selected, fully read analyst pure functions. The old
    # main and its historical directory-inventory checker are never compiled/run.
    tree = ast.parse((P / 'check.py').read_text())
    names = {'load', 'dg', 'pointer', 'parser', 'derive', 'guards'}
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in functions} == names
    scope = dict(Counter=Counter, deepcopy=deepcopy, sha256=sha256, importlib=importlib, json=json, P=P, R=R, F=F, D=D, NAMES=['impulse', 'sampler', 'simpler'])
    exec(compile(ast.Module(body=functions, type_ignores=[]), '<pinned analyst pure functions only>', 'exec'), scope)
    old_plan = load(P / 'plan.json')
    old_audit = load(P / 'audit.json')
    assert scope['derive'](old_plan, inputs) == old_audit
    plan = corrected(old_plan, ledger)
    audit = scope['derive'](plan, inputs)
    actual = []
    # The top-level assessment/proposal arrays need field-level comparison;
    # all remaining catalog sections must remain entirely equal.
    for catalog, old, new, arrays in [('plan', old_plan, plan, ['judgments', 'proposals']), ('audit', old_audit, audit, ['assessments', 'proposals'])]:
        for key in old:
            if key in arrays:
                assert len(old[key]) == len(new[key])
                for i, (b, a) in enumerate(zip(old[key], new[key])):
                    actual += [dict(catalog=catalog, pointer=p, before=x, after=y) for p, x, y in differences(b, a, f'/{key}/{i}')]
            else:
                assert old[key] == new[key], (catalog, key)
    expected = [{k: x[k] for k in ('catalog', 'pointer', 'before', 'after')} for x in ledger['changes']]
    sortkey = lambda x: (x['catalog'], x['pointer'])
    assert len(actual) == len(expected) == 18 and sorted(actual, key=sortkey) == sorted(expected, key=sortkey)
    scope['guards'](audit)
    focused(audit)
    mutations = []
    for index in (95, 99, 259):
        bad = deepcopy(audit)
        bad['assessments'][index]['assessment'] = old_audit['assessments'][index]['assessment']
        mutations.append((f'restore-setup-or-expected-as-action-{index+1}', bad))
    bad = deepcopy(audit); bad['proposals'][6]['proposed_minimal_delta'] = old_audit['proposals'][6]['proposed_minimal_delta']
    mutations.append(('remove-actual-Warp-button-entry', bad))
    bad = deepcopy(audit); bad['assessments'][99]['open_proposal_groups'] = []
    mutations.append(('drop-unexercised-chooser-route', bad))
    bad = deepcopy(audit); bad['proposals'][6]['actual_expected'] = 'passed'
    mutations.append(('invent-actual-grade', bad))
    rejected = []
    for name, bad in mutations:
        try:
            scope['guards'](bad); focused(bad)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Unsafe correction accepted: ' + name)
    links = 0
    for url in re.findall(r'\]\(([^)]+)\)', (P / 'README-r2.md').read_text()):
        target = P / url.split('#')[0]
        assert target.exists() or (url == 'manifest-r2.json' and not (P / 'manifest-r2.json').exists()), url
        links += 1
    for path in P.iterdir():
        if path.is_file():
            raw = path.read_bytes()
            assert raw.endswith(b'\n') and b'\0' not in raw
            assert all(line.rstrip(b' \t') == line for line in raw.splitlines())
    if (P / 'manifest-r2.json').exists():
        manifest = load(P / 'manifest-r2.json')
        assert set(manifest['files']) == {q.name for q in P.iterdir() if q.is_file()} - {'manifest-r2.json'}
        assert len(manifest['files']) == 9
        for name, pin in manifest['files'].items():
            assert dg(P / name) == pin, name
    assert before == {str(p): dg(p) for p in watch}
    print(json.dumps(dict(status='pass', sealed=(P / 'manifest-r2.json').exists(), exact_replacements=18, old_files_preserved=6, immutable_inputs=68, owner_requirements=61, owner_cases=88, judgments=309, proposals=33, source_questions=6, negative_fixtures=rejected, links=links, watched_paths=len(watch), all_unchanged=True, writes=False, historical_main_run=False, new_normative_IDs=0, new_cases=0, adoption=0, coverage_credit=0, actual_nonnull=0), indent=2))


if __name__ == '__main__':
    main()
