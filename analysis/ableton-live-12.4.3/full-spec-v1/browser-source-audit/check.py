"""Read-only finite local Browser source audit; no old tool/main/scan/runtime."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import importlib.util
import json
import re
import sys

D = Path(__file__).resolve().parent
R = D.parents[3]
F = D.parent
load = lambda p: json.loads(p.read_text())
NUMBERS = list(range(1, 122)) + list(range(196, 269))


def pin(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=sha256(b).hexdigest())


def ptr(v, route):
    assert route.startswith('/')
    for k in route.split('/')[1:]:
        k = k.replace('~1', '/').replace('~0', '~')
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


def guards(a, p):
    assert len(a['blocks']) == len(a['assessments']) == len(p['judgments']) == 194
    assert [b['id'] for b in a['blocks']] == [f'BR:B{x:03}' for x in NUMBERS]
    assert Counter(b['kind'] for b in a['blocks']) == dict(h1=1, p=121, li=45, h2=10, h3=8, h4=9)
    assert len(a['resources']) == 95 and len(a['secondary_blocks']) == 6
    assert a['partition'] == p['partition'] and a['partition']['selected_ranges'] == [[1, 121], [196, 268]] and a['partition']['excluded_ranges'] == [[122, 195]]
    assert a['partition']['selected_h4'] == [b['attributes']['id'] for b in a['blocks'] if b['kind'] == 'h4']
    assert len(a['partition']['selected_h4']) == 9 and len(a['partition']['excluded_h4']) == 5 and 'pending' in a['partition']['excluded_semantics']
    assert len(a['owner_requirements']) == 42 and len(a['owner_cases']) == 56
    for i, (b, x, j) in enumerate(zip(a['blocks'], a['assessments'], p['judgments'])):
        assert b == ptr(a, x['source_pointer']) and b['id'] == x['block'] == j['block']
        assert x['id'] == f'BRA-A{i+1:03}' and all(x[k] == j[k] for k in ['assessment', 'groups', 'disposition'])
        for field, expected, catalog in [('requirement_refs', 'requirements', 'owner_requirements'), ('case_refs', 'cases', 'owner_cases')]:
            assert [r['id'] for r in x[field]] == j[expected]
            for ref in x[field]:
                assert ref['catalog'] == catalog and ptr(a[catalog], ref['pointer'])['id'] == ref['id']
    assert a['proposals'] == p['proposals'] and a['source_questions'] == p['source_questions'] and a['common_future_prerequisites'] == p['common_future_prerequisites']
    assert [g['id'] for g in a['proposals']] == [f'G{x:02}' for x in range(1, 24)]
    for x in a['assessments'] + a['proposals']:
        assert x['documentary_expected'] is x['documentary_comparison'] is x['actual_expected'] is x['actual_comparison'] is None
        assert x['target'] == 'U' and x['executed'] is x['complete'] is False and x['coverage_credit'] == 0
    for g in a['proposals']:
        assert not g['new_normative_IDs'] and not g['new_cases'] and g['positive_baseline'] and g['proposed_action'] and g['limits']
        for ref in g['source_references'] + g.get('secondary_source_references', []):
            assert ref['catalog'] == 'audit.json' and ptr(a, ref['pointer'])['id'] == ref['id']
    assert a['current_actual_overlay'] == [dict(id=c['id'], expected=None, comparison=None, target='U', executed=False) for c in a['owner_cases']]
    by = {g['id']: g for g in a['proposals']}
    for gid, field, tokens in [
        ('G03', 'limits', ['Esc is NOT search x']),
        ('G08', 'proposed_action', ['inspection is NOT invocation', 'actual retained auto-tag', 'independently completed positive analysis']),
        ('G09', 'proposed_action', ['CHECK AND UNCHECK', 'ONE item then TWO Shift-selected']),
        ('G11', 'proposed_action', ['ACTUALLY choose create-parent-tag then create-tag-group']),
        ('G12', 'limits', ['No global shortcut or new released sidecar color encoding']),
        ('G13', 'proposed_action', ['FOUR independent actual assignments BEFORE', 'absent icon NOT lost assignment']),
        ('G17', 'proposed_action', ['BWF008 register-close-disconnect-reopen', 'completed positive indexing', 'AVAILABLE and UNAVAILABLE']),
        ('G17', 'limits', ['No whole-drive scan, unchanged file hashes, physical deletion']),
        ('G19', 'proposed_action', ['BC046 BOTH Preview-off ShiftEnter/right-arrow', 'SAMPLE, CLIP and INSTRUMENT PRESET']),
        ('G20', 'proposed_action', ['Raw-OFF/Warp-ON SAVED-CLIP scrub positive', 'ACTUALLY toggle Raw', 'keeping both exclusions distinct', 'BOTH productive routes']),
        ('G20', 'positive_baseline', ['EACH', 'NONEMPTY NONZERO', 'BEFORE silence/exclusion']),
        ('G21', 'proposed_action', ['Keep true BWF010', 'Reconcile actual current Session/device/Arrangement cases BEFORE adoption']),
        ('G21', 'limits', ['No repository-wide missing-action claim']),
        ('G22', 'limits', ['No scores/thresholds/ranking/neighbors']),
        ('G23', 'proposed_action', ['IN-PROGRESS', 'separate completed positive corpus', 'no scan triggered']),
    ]:
        assert all(t in by[gid][field] for t in tokens), (gid, field)
    notes = {x['block']: x['assessment'] for x in a['assessments']}
    assert 'true union/asterisk subset' in notes['BR:B080'] and 'Both actual source-specific cases already true' in notes['BR:B025']
    assert 'NOT file hashes' in notes['BR:B245'] and 'does NOT override' in notes['BR:B222'] and 'PMW019' in notes['BR:B211']
    assert 'preserve BOTH' in notes['BR:B257']
    boundary = a['index_boundary']
    assert boundary['released_partial'] == ['001', '003', '004', '005', '006', '007', '008'] and boundary['not_released'] == ['002', '009', '010', '011', '012', '013'] and boundary['no_UI_parity']
    assert a['summary']['original_combined'] == 274 and a['summary']['complete_topics'] == a['summary']['actual_nonnull'] == a['summary']['adopted'] == a['summary']['new_cases'] == a['summary']['new_normative_IDs'] == 0


def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only; no writer/old tools/scans/replays'
    inputs = load(D / 'inputs.json')
    watch = {R / s for s in inputs['files']} | {q for q in D.iterdir() if q.is_file()}
    before = {str(q): pin(q) for q in watch}
    assert len(inputs['files']) == 69 and len(inputs['old_owner_files']) == 27 and len(inputs['release_files']) == 32
    for name, expected in inputs['files'].items(): assert not name.startswith('wiki/') and pin(R / name) == expected, name
    for row in inputs['embedded_asof'].values():
        b = row['text'].encode(); assert dict(bytes=len(b), sha256=sha256(b).hexdigest()) == {k: row[k] for k in ['bytes', 'sha256']}
    a, plan = load(D / 'audit.json'), load(D / 'plan.json')
    guards(a, plan)
    assert a['sources'] == load(F / 'browser-content/sources.json')
    browser = F / 'browser-content/manual-browser-2026-10-19.html'
    assert pin(browser) == dict(bytes=334122, sha256='4e34895d5d37d6579e29cb65156b83c53672e89bd01b3bd8233596fc5b17e8b3')
    assert a['sources'][0]['capture_utc'] == '2026-10-19T19:56:28.639468+00:00'
    # Only the previously inspected pinned pure analyst parser, no source modules/old mains.
    s = importlib.util.spec_from_file_location('our_pure_browser_audit', R / inputs['parser'])
    parser = importlib.util.module_from_spec(s); s.loader.exec_module(parser)
    raw = browser.read_text(); allb, allr = parser.extract(raw, 'BR')
    assert len(allb) == 268 and len(allr) == 160
    assert allb[:121] + allb[195:] == a['blocks']
    lo, hi = allb[121]['raw_start'], allb[195]['raw_start']
    res = [r for r in allr if not lo <= r['raw_start'] < hi]
    for old, row in zip(res, a['resources']): assert all(row[k] == v for k, v in old.items()) and row['pixels_or_destination_inspected'] is row['complete'] is False
    for b in a['blocks']:
        assert raw[b['raw_start']:b['raw_end']] == b['raw_html'] and raw[:b['raw_start']].count('\n') + 1 == b['html_line']
        assert b['raw_start'] - (raw.rfind('\n', 0, b['raw_start']) + 1) == b['html_column']
    old = load(F / 'browser-content/source-blocks.json')
    for n, (b, o) in enumerate(zip(allb, old), 1): assert (o['id'], o['tag'], o['text'], o['html_line'], o['anchor']) == (f'BC-B{n:03}', b['kind'], b['text'], b['html_line'], b['heading_context'][-1]['anchor'])
    assert len(old) == 268
    cb, _ = parser.extract((F / 'browser-content/manual-concepts.html').read_text(), 'CX')
    selected = [b for b in cb if any(h['anchor'] == 'sound-similarity' for h in b['heading_context'])]
    assert len(selected) == len(a['secondary_blocks']) == 6 and a['secondary_blocks'] == load(F / 'browser-content/similarity-blocks.json')
    for b, o in zip(selected, a['secondary_blocks']): assert (o['tag'], o['text'], o['html_line'], o['anchor']) == (b['kind'], b['text'], b['html_line'], b['heading_context'][-1]['anchor'])
    # Transcribed workflow rows are bound to frozen embedded text, not mutable wiki.
    ws = inputs['embedded_asof']['workflow_spec']['text']
    for row in a['owner_requirements'] + a['owner_cases']:
        x = row['record']; assert x['id'] == row['id']
        if row['family'] == 'browser-workflows':
            assert ws[x['raw_start']:x['raw_end']] == x['raw_row'] and ws[:x['raw_start']].count('\n') + 1 == x['line']
            assert x['cells'] == [c.strip() for c in x['raw_row'].strip('|').split('|')]
        else:
            cat = load(F / ('browser-content/requirements.json' if 'contract' in x else 'browser-content/cases.json'))
            assert x == next(z for z in cat if z['id'] == row['id'])
            if 'setup_and_action' in x: assert x['expected'] is x['comparison'] is None and x['target_grade'] == 'U' and x['executed'] is False
    for x in a['external_contexts']:
        if 'pointer' in x: assert ptr(load(R / x['provider']), x['pointer']) == x['record'] and x['record']['id'] == x['id']
        else:
            assert pin(R / x['provider']) == x['provider_pin'] and (R / x['provider']).read_text()[x['raw_start']:x['raw_end']] == x['quote']
    release = R / 'handoff/browser-index-v1'
    rm = load(release / 'manifest.json'); assert len(rm['files']) == 31 and rm['case_count'] == 26
    for x in rm['files']: assert pin(release / x['path']) == {k: x[k] for k in ['bytes', 'sha256']}
    tiny = '<p>outside</p><div id="chapter_content"><h1 id="x" data-number="4">B</h1><h2 id="u" data-number="4.7">U</h2><h4 id="a" data-number="4.7.6.1">Assets</h4><p>0.5</p><ul><li>List</li></ul><table><tr><td>0</td><td>2</td></tr></table><img alt=""><figcaption>Literal</figcaption></div><p>outside</p>'
    bs, rs = parser.extract(tiny, 'FIX')
    assert [b['text'] for b in bs] == ['B', 'U', 'Assets', '0.5', 'List', '0 | 2'] and bs[3]['heading_context'][-1]['section'] == '4.7.6.1' and rs[0]['attributes']['alt'] == '' and rs[1]['text'] == 'Literal'
    tests = [('source-omission', None), ('resource-omission', None), ('wrong-valid-case-pointer', None), ('joint-invalid-source-prefix', None), ('joint-wrong-valid-source-index', None), ('joint-service-h4-inclusion', None), ('new-actual-oracle', None), ('release-preview-promoted', None), ('joint-Esc-equals-x', ('G03', 'limits', 'Esc is NOT search x', 'Esc equals search x')), ('joint-auto-inspection-is-operation', ('G08', 'proposed_action', 'inspection is NOT invocation', 'inspection proves invocation')), ('joint-lost-multiselection', ('G09', 'proposed_action', 'ONE item then TWO Shift-selected', 'one item only')), ('joint-unproven-four-colors', ('G13', 'proposed_action', 'FOUR independent actual assignments BEFORE', 'two enabled colors suffice BEFORE')), ('joint-unchanged-file-hashes', ('G17', 'limits', 'No whole-drive scan, unchanged file hashes, physical deletion', 'Require unchanged file hashes')), ('joint-no-preview-positive', ('G20', 'positive_baseline', 'NONEMPTY NONZERO', 'enabled flag')), ('joint-no-scrub-positive', ('G20', 'proposed_action', 'Raw-OFF/Warp-ON SAVED-CLIP scrub positive', 'Raw-on flag')), ('joint-absence-closure', None)]
    rejected = []
    for name, edit in tests:
        aa, pp = deepcopy(a), deepcopy(plan)
        if edit:
            gid, field, old, new = edit
            for obj in [aa, pp]:
                g = next(g for g in obj['proposals'] if g['id'] == gid); assert old in g[field]; g[field] = g[field].replace(old, new)
        elif name == 'source-omission': aa['blocks'].pop()
        elif name == 'resource-omission': aa['resources'].pop()
        elif name == 'wrong-valid-case-pointer': next(x for x in aa['assessments'] if x['block'] == 'BR:B012')['case_refs'][0]['pointer'] = '/0'
        elif name in ['joint-invalid-source-prefix', 'joint-wrong-valid-source-index']:
            for obj in [aa, pp]: obj['proposals'][0]['source_references'][0]['pointer'] = '/cases/0' if name == 'joint-invalid-source-prefix' else '/blocks/0'
        elif name == 'joint-service-h4-inclusion':
            for obj in [aa, pp]: obj['partition']['selected_h4'][0] = 'logging-into-splice'
        elif name == 'new-actual-oracle': aa['current_actual_overlay'][0]['expected'] = 'pass'
        elif name == 'release-preview-promoted': aa['index_boundary']['not_released'].remove('009')
        else:
            for obj in [aa, pp]: obj['partition']['excluded_semantics'] = 'All services complete'
        try: guards(aa, pp)
        except (AssertionError, KeyError, IndexError, ValueError, TypeError): rejected.append(name)
        else: raise AssertionError('Unsafe mutation accepted: ' + name)
    manifest = D / 'manifest.json'
    if manifest.exists():
        mm = load(manifest); assert set(mm['payloads']) == {q.name for q in D.iterdir() if q.is_file() and q != manifest}
        for n, value in mm['payloads'].items(): assert pin(D / n) == value
        assert mm['immutable_inputs'] == inputs['files']
    for q in D.iterdir():
        if q.is_file():
            b = q.read_bytes(); assert b.endswith(b'\n') and b'\0' not in b and all(x.rstrip(b' \t') == x for x in b.splitlines())
    for dest in re.findall(r'\]\(([^)]+)\)', (D / 'README.md').read_text()): assert (D / dest.split('#')[0]).exists() or dest == 'manifest.json' and not manifest.exists(), dest
    assert before == {str(q): pin(q) for q in watch}
    print(json.dumps(dict(status='pass', sealed=manifest.exists(), selected_primary=194, selected_resources=95, excluded_semantic_pending=74, excluded_resources=65, secondary_contexts=6, selected_requirements=42, selected_cases=56, external_contexts=12, groups=23, old_files=27, finite_release_files=32, pins=69, negative_fixtures=rejected, parser_fixture='pass', watched_unchanged=len(watch), actual_nonnull=0, adoption=0, complete_topics=0, writes=False), indent=2))


if __name__ == '__main__': main()
