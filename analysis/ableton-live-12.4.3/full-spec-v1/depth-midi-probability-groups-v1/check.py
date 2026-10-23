"""Data-only provenance and proposal checks; never executes original code."""
from pathlib import Path
import copy
import hashlib
import json
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fixture_shape(root, proposal):
    groups = root.find('NoteProbabilityGroups')
    assert groups is not None and len(groups) == len(proposal['group_ids'])
    for i, group in enumerate(groups):
        assert group.tag == 'NoteProbabilityGroup'
        assert group.attrib == {'Id': str(i)}
        assert [x.tag for x in group] == ['GroupType', 'Notes', 'Probability', 'GroupId']
        assert group.find('GroupType').attrib == {'Value': '0'}
        assert group.find('Probability').attrib == {'Value': '1'}
        assert group.find('GroupId').attrib == {'Value': str(proposal['group_ids'][i])}
        notes = group.find('Notes')
        assert [x.tag for x in notes] == ['NoteId'] * len(proposal['note_ids'])
        assert [x.attrib for x in notes] == [{'NoteId': str(n)} for n in proposal['note_ids']]
        assert all(len(x) == 0 for x in notes)
    assert root.find('ProbabilityGroupIdGenerator/NextId').attrib == {
        'Value': str(proposal['group_next_id'])}


def main():
    pins = json.loads((BASE / 'pins.json').read_text())
    # Mutable wiki pins describe consultation time, not future identity gates.
    for pin in pins['providers'] + pins['selected_chunks']:
        if pin.get('kind') == 'mutable-as-of-only':
            continue
        data = Path(pin['path']).read_bytes()
        assert len(data) == pin['bytes'] and digest(data) == pin['sha256'], pin['path']
    counts = {}
    for stem in ['source', 'class-table', 'call']:
        data = (BASE / (stem + '-rows.jsonl')).read_bytes()
        rows = data.splitlines(keepends=True)
        locs = json.loads((BASE / (stem + '-locators.json')).read_text())
        assert len(rows) == len(locs)
        providers = {}
        for row, loc in zip(rows, locs):
            path = loc['source']
            if path not in providers:
                providers[path] = Path(path).read_bytes()
            assert len(row) == loc['bytes'] and digest(row) == loc['sha256']
            assert providers[path][loc['byte_offset']:loc['byte_offset'] + loc['bytes']] == row
            record = json.loads(row)
            if stem == 'source':
                assert record['entry'] == loc['entry']
                code = record['code'].encode()
                assert len(code) == record['code_bytes'] and digest(code) == record['code_sha256']
            elif stem == 'class-table':
                assert record['address_point'] == loc['address_point']
            else:
                assert (record['caller'], record['site'], record['to']) == (
                    loc['caller'], loc['site'], loc['to'])
        counts[stem] = len(rows)
    assert counts == {'source': 39, 'class-table': 5, 'call': 70}
    sources = {r['entry']: r for r in map(json.loads, (BASE / 'source-rows.jsonl').read_text().splitlines())}
    calls = list(map(json.loads, (BASE / 'call-rows.jsonl').read_text().splitlines()))
    for call in calls:
        source = sources[call['caller']]
        assert any(int(a, 16) <= int(call['site'], 16) <= int(b, 16)
                   for a, b in source['body_ranges'])
    assert sources['0x10290ad68']['body_bytes'] == 4
    assert sources['0x1028f8e48']['body_bytes'] == 176
    assert sources['0x1028f5770']['body_bytes'] == 244
    assert any(r['caller'] == '0x10290ad68' and r['site'] == '0x10290ad68'
               and r['kind'] == 'tail-jump' and r['to'] == '0x1028f8e48' for r in calls)
    tables = {r['address_point']: r for r in map(json.loads, (BASE / 'class-table-rows.jsonl').read_text().splitlines())}
    expected = {'0x106829f38': {0: '0x1029260a0', 8: '0x1029260b8'},
                '0x106829f60': {0x138: '0x101486cdc', 0x140: '0x101487310'},
                '0x10682a6e0': {0x138: '0x101560258', 0x140: '0x101560424'},
                '0x10667ec98': {0x138: '0x10156de64', 0x140: '0x10156d7d8'}}
    for address, slots in expected.items():
        actual = {s['offset']: s['target'] for s in tables[address]['slots']}
        assert all(actual[k] == v for k, v in slots.items())
    proposal = json.loads((BASE / 'case-proposals.json').read_text())
    cases = proposal['cases']
    assert [c['case_id'] for c in cases] == ['MNS-' + str(n).zfill(3) for n in range(54, 60)]
    assert [c['group_ids'] for c in cases] == [[0], [5], [2, 1], [1, 1], [1], [1]]
    assert [c['group_next_id'] for c in cases] == [1, 1, 3, 2, 2, 2]
    for case in cases:
        data = (BASE / case['fixture']).read_bytes()
        assert len(data) == case['bytes'] and digest(data) == case['sha256']
        fixture_shape(ET.fromstring(data), case)
    good = ET.parse(BASE / cases[4]['fixture']).getroot()
    for mutation in range(3):
        bad = copy.deepcopy(good)
        group = bad.find('NoteProbabilityGroups/NoteProbabilityGroup')
        if mutation == 0:
            group.set('GroupId', '1')
        elif mutation == 1:
            note = group.find('Notes/NoteId')
            note.attrib.clear()
            ET.SubElement(note, 'NoteId', {'Value': '1'})
        else:
            group.find('GroupId').set('Value', '5')
        try:
            fixture_shape(bad, cases[4])
        except AssertionError:
            continue
        raise AssertionError('malformed proposal escaped check')
    assert proposal['owner_revision'] == 4 and proposal['new_original_calls'] == 0
    assert proposal['new_behavior_grades'] == 0 and proposal['no_new_case_ids']
    print(json.dumps({'status': 'PASS-documentary-only', 'counts': counts, 'fixtures': 6,
                      'negative_controls': 3, 'new_original_calls': 0, 'new_behavior_grades': 0}))


if __name__ == '__main__':
    main()
