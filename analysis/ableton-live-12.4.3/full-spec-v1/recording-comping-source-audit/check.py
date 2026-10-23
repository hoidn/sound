"""Finite read-only retained Comping source reconciliation; no old tool or runtime."""
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
load = lambda p: json.loads(p.read_text())


def pin(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=sha256(b).hexdigest())


def ptr(value, route):
    assert not route or route.startswith('/')
    for key in route.split('/')[1:]:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def requirements(text):
    rows = []
    for m in re.finditer(r'^### (REQ-RECORDING-COMPING-\d{3}) — ([^\n]+)\n', text, re.M):
        n = re.search(r'^### |^## ', text[m.end():], re.M)
        end = len(text) if n is None else m.end() + n.start()
        rows.append(dict(id=m.group(1), title=m.group(2), contract=text[m.end():end].strip(), raw_start=m.start(), raw_end=end, quote=text[m.start():end], line=text[:m.start()].count('\n') + 1))
    return rows


def guards(a, plan):
    assert len(a['blocks']) == len(a['assessments']) == len(plan['judgments']) == 38, 'source omission'
    assert Counter(b['kind'] for b in a['blocks']) == {'p': 30, 'h2': 7, 'h1': 1}
    assert a['summary'] == dict(blocks=38, paragraphs=30, headings=8, list_items=0, table_rows=0, table_cells=0, literal_resources=24, images=7, captions=7, links=10, selected_requirements=12, selected_cases=29, audit_only_groups=13, new_normative_IDs=0, new_cases=0, actual_nonnull=0, executed=0, adopted=0, complete_topics=0)
    assert len(a['owner_requirements']) == 12 and len(a['owner_cases']) == 29
    assert a['source']['captured_utc'] == '2026-10-19T19:53:10.118294+00:00'
    assert a['source']['sha256'] == 'e750973536d4331342ad392e637a7661b2a75dcd533c3e72c6cabe4a8ceab28b' and a['source']['exact_target_applicability'] == 'U'
    for n, (b, row, judgment) in enumerate(zip(a['blocks'], a['assessments'], plan['judgments'])):
        assert row['block'] == judgment['block'] == b['id'] == f'CMP:B{n+1:03}'
        assert ptr(a, row['source_pointer']) == b and row['source_text_sha256'] == sha256(b['text'].encode()).hexdigest()
        assert row['assessment'] == judgment['assessment'] and row['disposition'] == judgment['disposition'] and row['groups'] == judgment['groups']
        for field, selected, catalog, body in [('requirement_refs', 'requirements', 'owner_requirements', 'contract'), ('case_refs', 'cases', 'owner_cases', 'action')]:
            assert [x['id'] for x in row[field]] == judgment[selected]
            for ref in row[field]:
                assert ref['catalog'] == catalog
                target = ptr(a[catalog], ref['json_pointer'])
                assert target['id'] == ref['id'] and ptr(a[catalog], ref['body_pointer' if body == 'contract' else 'action_pointer']) == target[body]
        assert [x['id'] for x in row['external_context_refs']] == judgment['external_context_refs']
        for ref in row['external_context_refs']:
            assert ref['catalog'] == 'external_contexts' and ptr(a['external_contexts'], ref['json_pointer'])['id'] == ref['id']
    assert a['proposals'] == plan['proposals'] and a['common_future_prerequisites'] == plan['common_future_prerequisites'] and a['source_questions'] == plan['source_questions']
    assert [p['id'] for p in a['proposals']] == [f'G{n:02}' for n in range(1, 14)]
    for row in a['assessments'] + a['proposals']:
        assert row['documentary_expected'] is row['documentary_comparison'] is row['actual_expected'] is row['actual_comparison'] is None
        assert row['target'] == 'U' and row['executed'] is row['complete'] is False and row['coverage_credit'] == 0
    for p in a['proposals']:
        assert not p['new_normative_IDs'] and not p['new_cases'] and p['proposed_action'] and p['positive_baseline'] and p['limits']
        assert set(p['blocks']) <= {b['id'] for b in a['blocks']}
        assert [x['id'] for x in p['source_references']] == p['blocks']
        for ref in p['source_references']:
            source = ptr(a, ref['pointer'])
            assert ref['catalog'] == 'audit.json' and source['id'] == ref['id'] and sha256(source['text'].encode()).hexdigest() == ref['text_sha256']
    # Source-specific semantic distinctions: joint plan+derived edits cannot launder these.
    by = {p['id']: p for p in a['proposals']}
    for group, field, tokens in [
        ('G01', 'proposed_action', ['Left Arrow', 'Automation Mode', 'not Insert']),
        ('G02', 'proposed_action', ['Delete All Take Lanes', 'RC048 Delete All Unused', 'recorded used/unused']),
        ('G03', 'proposed_action', ['modifier+wheel', 'hover-edge resize handles', 'one then multiple']),
        ('G04', 'proposed_action', ['drag/drop then separately Ctrl/Cmd Up and Down', 'Tab/ShiftTab']),
        ('G05', 'positive_baseline', ['genuinely NONEMPTY completed take', 'BOTH distinct takes and main comp independently productive']),
        ('G05', 'limits', ['partial passes', 'reuse search order', 'remain U']),
        ('G06', 'proposed_action', ['sequential TRACK destinations, not sequential take lanes', 'sample and one admitted MIDI file']),
        ('G06', 'limits', ['No decoder/format grammar/universal admission, multi-MIDI distribution']),
        ('G07', 'proposed_action', ['speaker button and separately T', 'time selection then a lane-header selection', 'DIFFERENT tracks']),
        ('G07', 'positive_baseline', ['BOTH distinct identifiable takes on each tested track AND its main comp', 'NONEMPTY NONZERO nonmuted productive output']),
        ('G08', 'proposed_action', ['Keep true RC051 Enter and RC053', 'take-lane time selection', 'empty lane']),
        ('G08', 'limits', ['RC054 BOTH Draw-release/main-click actions and RC076 cancellation U remain unchanged']),
        ('G09', 'proposed_action', ['RC052 main/take edits independent in BOTH directions', 'copy/paste then separately drag/drop']),
        ('G09', 'limits', ['no all-edit completion', 'duplication of physical media inferred']),
        ('G10', 'proposed_action', ['actually invoke CtrlAltF', 'without relying on an already auto-created fade']),
        ('G10', 'positive_baseline', ['BOTH distinct adjacent comp pieces and their source takes', 'NONEMPTY NONZERO nonmuted']),
        ('G10', 'limits', ['no measured curve/rounding/sample alignment/short-clip', 'RC078 remains U']),
        ('G11', 'proposed_action', ['FIRST establishing actual visible highlights', 'unknown probe', 'do not infer its outcome']),
        ('G11', 'limits', ['No shared-TakeId/sample-only sufficiency', 'complete property equivalence']),
        ('G12', 'proposed_action', ['actual offered Clip Color preference/build/creation history', 'without requiring random inequality', 'do not adopt a generic default']),
        ('G13', 'limits', ['API index source12.4.5 versus target12.4.3U', 'No generic API compatibility']),
    ]:
        assert all(t in by[group][field] for t in tokens), (group, field)
    assert [x['id'] for x in a['assessments'][32]['case_refs']] == ['RC-054', 'RC-076']
    assert 'Do not invent a missing Draw-release branch' in a['assessments'][32]['assessment']
    assert [x['id'] for x in a['assessments'][33]['case_refs']] == ['RC-051', 'RC-052']
    assert [x['id'] for x in a['assessments'][36]['case_refs']] == ['RC-055', 'RC-072']
    assert [x['id'] for x in a['assessments'][37]['case_refs']] == ['RC-056']
    assert all(t in ' '.join(a['common_future_prerequisites']) for t in ['BOTH', 'NONEMPTY', 'NONZERO'])


def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only; no writer/old tool/main/replay'
    inputs = load(D / 'inputs.json')
    watch = {R / name for name in inputs['files']} | {q for q in D.iterdir() if q.is_file()}
    before = {str(p): pin(p) for p in watch}
    assert len(inputs['files']) == 33 and len(inputs['old_recording_files']) == 26
    for name, expected in inputs['files'].items():
        assert not name.startswith('wiki/') and pin(R / name) == expected, name
    a, plan = load(D / 'audit.json'), load(D / 'plan.json')
    guards(a, plan)
    spec = (R / a['owner_provider']).read_text()
    full = requirements(spec)
    assert len(full) == a['owner_total_requirements'] == 32
    assert [r for r in full if int(r['id'][-3:]) in a['selected_requirement_suffixes']] == a['owner_requirements']
    oldcases = load(R / 'analysis/ableton-live-12.4.3/full-spec-v1/recording/cases-r3.json')['records']
    assert len(oldcases) == a['owner_total_cases'] == 81 and [c for c in oldcases if c['id'] in a['selected_case_ids']] == a['owner_cases']
    assert len(a['owner_case_origins']) == 29
    for row, origin in zip(a['owner_cases'], a['owner_case_origins']):
        assert ptr(load(R / origin['catalog']), origin['pointer']) == row and row['id'] == origin['id']
        assert row['expected'] is row['comparison'] is None and row['target_grade'] == 'U' and row['executed'] is False
    for row in a['external_contexts']:
        text = (R / row['provider']).read_text()
        assert pin(R / row['provider']) == row['provider_pin'] and text[row['raw_start']:row['raw_end']] == row['quote']
    raw = (R / a['source']['path']).read_text()
    assert pin(R / a['source']['path']) == {k: a['source'][k] for k in ['bytes', 'sha256']}
    assert next(x for x in load(R / 'analysis/ableton-live-12.4.3/full-spec-v1/recording/sources.json') if x['id'] == 'D12-comping') == {k: v for k, v in a['source'].items() if k not in ['path', 'exact_target_applicability']}
    # Only pinned, fully inspected pure analyst HTML parser; no historical packet tools.
    module_path = R / inputs['parser']
    s = importlib.util.spec_from_file_location('our_pure_retained_comping_parser', module_path)
    parser = importlib.util.module_from_spec(s)
    s.loader.exec_module(parser)
    blocks, resources = parser.extract(raw, 'CMP')
    assert blocks == a['blocks'] and len(resources) == len(a['resources']) == 24
    for original, annotated in zip(resources, a['resources']):
        assert all(annotated[k] == v for k, v in original.items()) and annotated['pixels_or_destination_inspected'] is annotated['complete'] is False
    for b in blocks:
        assert raw[b['raw_start']:b['raw_end']] == b['raw_html']
        assert raw[:b['raw_start']].count('\n') + 1 == b['html_line']
        assert b['raw_start'] - (raw.rfind('\n', 0, b['raw_start']) + 1) == b['html_column']
    tiny = '<p>outside</p><div id="chapter_content"><h1 id="x" data-number="21">Comping</h1><p>1.5 beats</p><div><ul><li>Base</li></ul><table><tr><td>0</td><td>2.5</td></tr></table><img alt=""><figcaption>Literal</figcaption></div></div><p>outside again</p>'
    bs, rs = parser.extract(tiny, 'FIX')
    assert [b['text'] for b in bs] == ['Comping', '1.5 beats', 'Base', '0 | 2.5'] and len(bs[-1]['cells']) == 2 and bs[2]['heading_context'][-1]['anchor'] == 'x'
    assert rs[0]['attributes']['alt'] == '' and rs[1]['text'] == 'Literal'
    tests = [('source-omission', None), ('wrong-valid-owner-pointer', None), ('wrong-source-prefix', None), ('joint-invalid-proposal-prefix', None), ('invented-target-oracle', None), ('invented-UTC', None), ('joint-sequential-lanes', ('G06', 'proposed_action', 'sequential TRACK destinations, not sequential take lanes', 'sequential take lanes')), ('joint-multi-MIDI-distribution', ('G06', 'limits', 'No decoder/format grammar/universal admission, multi-MIDI distribution', 'All MIDI files distribute identically')), ('joint-unproductive-audition', ('G07', 'positive_baseline', 'BOTH distinct identifiable takes on each tested track AND its main comp', 'Two enabled flags')), ('joint-auto-fade-substitution', ('G10', 'proposed_action', 'without relying on an already auto-created fade', 'already auto-created fade proves the manual gesture')), ('joint-TakeId-sufficiency', ('G11', 'limits', 'No shared-TakeId/sample-only sufficiency', 'Shared TakeId alone suffices')), ('joint-random-inequality', ('G12', 'proposed_action', 'without requiring random inequality', 'require every random take color to differ')), ('joint-missing-Draw-release', None), ('joint-reuse-algorithm', ('G05', 'limits', 'reuse search order', 'greedy allocation algorithm guaranteed')), ('joint-physical-media-copy', ('G09', 'limits', 'duplication of physical media inferred', 'every clip copy guarantees independent physical media'))]
    rejected = []
    for name, change in tests:
        aa, pp = deepcopy(a), deepcopy(plan)
        if change:
            group, field, old, new = change
            for obj in [aa, pp]:
                row = next(g for g in obj['proposals'] if g['id'] == group)
                assert old in row[field]; row[field] = row[field].replace(old, new)
        elif name == 'source-omission': aa['blocks'].pop()
        elif name == 'wrong-valid-owner-pointer': aa['assessments'][30]['case_refs'][0]['json_pointer'] = '/0'
        elif name == 'wrong-source-prefix': aa['assessments'][0]['source_pointer'] = '/cases/0'
        elif name == 'joint-invalid-proposal-prefix':
            for obj in [aa, pp]: obj['proposals'][0]['source_references'][0]['pointer'] = '/cases/0'
        elif name == 'invented-target-oracle': aa['proposals'][0]['actual_expected'] = 'pass'
        elif name == 'invented-UTC': aa['source']['captured_utc'] = None
        else:
            aa['assessments'][32]['assessment'] = pp['judgments'][32]['assessment'] = 'Missing Draw-release branch'
        try:
            guards(aa, pp)
        except (AssertionError, KeyError, IndexError, ValueError, TypeError):
            rejected.append(name)
        else:
            raise AssertionError('Unsafe mutation accepted: ' + name)
    manifest = D / 'manifest.json'
    if manifest.exists():
        m = load(manifest)
        assert set(m['payloads']) == {q.name for q in D.iterdir() if q.is_file() and q != manifest}
        for name, value in m['payloads'].items(): assert pin(D / name) == value
        assert m['immutable_inputs'] == inputs['files']
    for q in D.iterdir():
        if q.is_file():
            b = q.read_bytes(); assert b.endswith(b'\n') and b'\0' not in b and all(x.rstrip(b' \t') == x for x in b.splitlines())
    for url in re.findall(r'\]\(([^)]+)\)', (D / 'README.md').read_text()):
        assert (D / url.split('#')[0]).exists() or (url == 'manifest.json' and not manifest.exists()), url
    assert before == {str(p): pin(p) for p in watch}
    print(json.dumps(dict(status='pass', sealed=manifest.exists(), blocks=38, paragraphs=30, headings=8, resources=24, selected_contracts=12, selected_cases=29, owner_total_asof='32/81; not fully semantically reaudited', groups=13, external_selected=5, immutable_inputs=33, old_recording_files=26, negative_fixtures=rejected, parser_fixture='pass', watched_unchanged=len(watch), actual_nonnull=0, normative_adoption=0, complete_topics=0, writes=False), indent=2))


if __name__ == '__main__':
    main()
