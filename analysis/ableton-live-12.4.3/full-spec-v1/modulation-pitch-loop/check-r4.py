"""Read-only pointer-only successor. No historical main/parser/replay/decoder."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import ast
import json
import re
import sys

D = Path(__file__).resolve().parent
F = D.parent
R = F.parents[2]
A = F / 'modulation-pitch-loop-source-audit'
ADDITIONS = ['actual-overlay-r4.json', 'adoption-r4.json', 'pointer-correction-r4.json', 'delta-r4.json', 'spec-r4.md', 'research-r4.md', 'README-r4.md', 'check-r4.py']


def load(q):
    return json.loads(q.read_text())


def path(s):
    return Path(s) if Path(s).is_absolute() else R / s


def dg(q):
    b = q.read_bytes()
    return dict(bytes=len(b), sha256=sha256(b).hexdigest())


def ptr(v, route):
    for k in route.strip('/').split('/') if route else []:
        k = k.replace('~1', '/').replace('~0', '~')
        try:
            v = v[int(k)] if isinstance(v, list) else v[k]
        except (ValueError, IndexError, KeyError, TypeError):
            raise AssertionError('Invalid actual JSON pointer: ' + route) from None
    return v


def actual_references(cases, overlay, ledger):
    assert len(overlay['cases']) == 208 and len(ledger['groups']) == 22
    assert len({x['id'] for x in overlay['cases']}) == 208
    assert len({x['case_id'] for x in ledger['groups']}) == 22
    for x in overlay['cases']:
        assert x['catalog'] == 'cases-r3.json'
        assert ptr(cases, x['case_pointer'])['id'] == x['id']
    for x in ledger['groups']:
        assert ptr(cases, x['case_pointer'])['id'] == x['case_id']
    assert {x['id'] for x in overlay['cases']} == {c['id'] for c in cases}
    assert {x['case_id'] for x in ledger['groups']} == {c['id'] for c in cases[186:]}


def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only; no historical main/replay/write/decode'
    inputs = load(D / 'inputs-r3.json')
    owned = {q for q in D.rglob('*') if q.is_file()}
    wiki = {R / x['canonical'] for x in inputs['canonical_before']}
    watch = {path(x['path']) for x in inputs['files']} | owned | wiki
    before = {str(q): dg(q) for q in watch}
    assert len(inputs['files']) == 130
    for x in inputs['files']:
        assert not x['path'].startswith('wiki/')
        assert dg(path(x['path'])) == {k: x[k] for k in ('bytes', 'sha256')}
    assert dg(D / 'manifest-author-r3.json') == dict(bytes=22477, sha256='8ba80186176daff3a920f23abd94e24f83273f847ff4a5fe27a18fc172c0d36b')
    previous = load(D / 'manifest-author-r3.json')
    assert len(previous['files']) == 117
    for name, pin in previous['files'].items():
        assert dg(D / name) == pin, name
    correction = load(D / 'pointer-correction-r4.json')
    assert correction['total_field_changes'] == 230 and correction['case_requirement_source_action_oracle_changes'] == 0
    cases = load(D / 'cases-r3.json')
    overlay = load(D / 'actual-overlay-r4.json')
    ledger = load(D / 'adoption-r4.json')
    for before_name, current, array, offset, count in [('actual-overlay-r3.json', overlay, 'cases', 0, 208), ('adoption-r3.json', ledger, 'groups', 186, 22)]:
        old = load(D / before_name)
        assert len(old[array]) == len(current[array]) == count
        restored = deepcopy(current)
        for i, (b, a) in enumerate(zip(old[array], current[array]), offset):
            assert b['case_pointer'] == f'/cases/{i}' and a['case_pointer'] == f'/{i}'
            restored[array][i - offset]['case_pointer'] = b['case_pointer']
        assert restored == old, 'Only literal pointer fields may change'
    # Compile only the fully inspected, hash-pinned analyst pure guard function.
    # Correct its two pointer-format checks; do not compile imports/main/assignments.
    code = (D / 'check-r3.py').read_text()
    assert dg(D / 'check-r3.py') == previous['files']['check-r3.py']
    tree = ast.parse(code)
    selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'guards']
    assert len(selected) == 1
    body = ast.get_source_segment(code, selected[0])
    assert body.count("f'/cases/{i}'") == 2
    body = body.replace("f'/cases/{i}'", "f'/{i}'")
    namespace = dict(D=D, load=load, pointer=ptr)
    exec(compile(ast.parse(body), '<selected analyst guard with two pointer-format corrections>', 'exec'), namespace)
    audit = load(A / 'audit.json')
    def current_guard(cs, ov, le):
        namespace['guards'](cs, ov, le, audit)
        actual_references(cs, ov, le)
    current_guard(cases, overlay, ledger)
    rejected = []
    names = ['joint-invalid-cases-prefix', 'wrong-valid-index', 'missing-overlay', 'duplicate-overlay', 'missing-adoption', 'duplicate-adoption', 'out-of-range-overlay', 'out-of-range-adoption']
    for name in names:
        ov, le = deepcopy(overlay), deepcopy(ledger)
        if name == 'joint-invalid-cases-prefix':
            for x in ov['cases'] + le['groups']:
                x['case_pointer'] = '/cases' + x['case_pointer']
        elif name == 'wrong-valid-index':
            ov['cases'][186]['case_pointer'] = '/0'
        elif name == 'missing-overlay':
            ov['cases'].pop()
        elif name == 'duplicate-overlay':
            ov['cases'][-1] = deepcopy(ov['cases'][0])
        elif name == 'missing-adoption':
            le['groups'].pop()
        elif name == 'duplicate-adoption':
            le['groups'][-1] = deepcopy(le['groups'][0])
        elif name == 'out-of-range-overlay':
            ov['cases'][0]['case_pointer'] = '/208'
        else:
            le['groups'][0]['case_pointer'] = '/208'
        try:
            # This independent dereference check must reject even without format guards.
            actual_references(cases, ov, le)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Invalid references accepted: ' + name)
    # Retain current substantive R3 guard coverage with all20 prior unsafe variants.
    variants = [('old-case-mutation', None), ('new-doc-oracle', None), ('actual-overlay-grade', None), ('invent-new-requirement', None), ('wrong-source-pointer', None), ('wrong-case-pointer', None)]
    variants += [(name, (g, key)) for name, g, key in [('no-received-note-positive', 3, 'positive_baseline'), ('Rate-inspection-not-operation', 6, 'setup_and_action'), ('one-LFO-before-loss', 7, 'positive_baseline'), ('envelope-zero-without-positive', 8, 'positive_baseline'), ('repair-Hertz', 9, 'limits'), ('Poly-default-for-MonoGate', 11, 'positive_baseline'), ('conversion-completed-as-notes', 14, 'positive_baseline'), ('freeze-flag-as-capture', 15, 'positive_baseline'), ('XFade-equation', 15, 'limits'), ('unconditional-order', 16, 'setup_and_action'), ('one-Vocoder-channel', 19, 'positive_baseline'), ('automatic-RepeatOn', 20, 'setup_and_action'), ('clear-empty-flag', 21, 'positive_baseline'), ('insert-tap-name-as-effect', 22, 'positive_baseline')]]
    for name, edit in variants:
        cs, ov, le = deepcopy(cases), deepcopy(overlay), deepcopy(ledger)
        if edit:
            g, key = edit; cs[185 + g][key] = 'Enabled flag only'
        elif name == 'old-case-mutation':
            cs[0]['setup_and_action'] = 'Different action'
        elif name == 'new-doc-oracle':
            cs[186]['documentary_expected'] = 'always equal'
        elif name == 'actual-overlay-grade':
            ov['cases'][0]['actual_expected'] = 'pass'
        elif name == 'invent-new-requirement':
            cs[186]['requirements'] = ['REQ-MPL-NEW-001']
        elif name == 'wrong-source-pointer':
            le['groups'][0]['source_pointers'][0] = '/blocks/0/text'
        else:
            le['groups'][0]['case_pointer'] = '/0'
        try:
            current_guard(cs, ov, le)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Unsafe current mutation accepted: ' + name)
    links = 0
    for page in load(D / 'delta-r4.json')['pages']:
        text = (D / page['original_provider']).read_text()
        for edit in page['replacements']:
            assert text.count(edit['before']) == edit['occurrences'] == 1
            text = text.replace(edit['before'], edit['after'], 1)
        text += page['append']
        assert text == (D / page['current_snapshot']).read_text() == (R / page['canonical']).read_text()
        for url in re.findall(r'\]\(([^)]+)\)', text):
            if re.match(r'https?://', url):
                continue
            target = (R / page['canonical']).parent / url.split('#')[0]
            assert target.exists() or (target.name == 'manifest-author-r4.json' and not (D / 'manifest-author-r4.json').exists()), url
            links += 1
    spec = (D / 'spec-r4.md').read_text()
    ids = set(re.findall(r'^\|\s*(REQ-[A-Z0-9-]+)\s*\|', spec, re.M)) | set(re.findall(r'^###\s+(REQ-[A-Z0-9-]+)(?:\s|$)', spec, re.M))
    req = load(D / 'requirements.json')
    assert ids == {r['id'] for r in req} and len(ids) == 106
    for name in ADDITIONS:
        raw = (D / name).read_bytes()
        assert raw.endswith(b'\n') and b'\0' not in raw and all(x.rstrip(b' \t') == x for x in raw.splitlines())
    for url in re.findall(r'\]\(([^)]+)\)', (D / 'README-r4.md').read_text()):
        target = D / url.split('#')[0]
        assert target.exists() or (url == 'manifest-author-r4.json' and not target.exists()), url
        links += 1
    seal = D / 'manifest-author-r4.json'
    if seal.exists():
        m = load(seal); assert len(m['files']) == 126
        assert set(m['files']) == {str(q.relative_to(D)) for q in D.rglob('*') if q.is_file()} - {seal.name}
        for name, pin in m['files'].items():
            assert dg(D / name) == pin, name
    assert before == {str(q): dg(q) for q in watch}
    print(json.dumps(dict(status='pass', sealed=seal.exists(), preserved_R3_files=118, immutable_original_inputs=130, actual_case_pointers_dereferenced=208, adoption_case_pointers_dereferenced=22, exact_pointer_only_changes=230, case_action_oracle_changes=0, current_cases=208, unchanged_requirements=106, actual_all_null_U=True, browser_IDs=106, independent_reference_fixtures=rejected[:8], retained_substantive_negative_fixtures=rejected[8:], links=links, watched_paths=len(watch), all_unchanged=True, writes=False, historical_main_replay=False), indent=2))


if __name__ == '__main__':
    main()
