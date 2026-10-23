#!/usr/bin/env python3
"""Read-only stdlib documentary/input-data checks; no reference or model execution."""
import copy
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent / 'midi-note-storage-v4'
OLD = ROOT / 'handoff/midi-note-storage-v3'
NOTES_PATH = './LiveSet/Tracks/MidiTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/MidiClip/Notes'


def require(test, message):
    if not test:
        raise AssertionError(message)


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def load(path):
    return json.loads(path.read_text())


def bodies(text):
    rows = list(re.finditer(r'^### (REQ-MIDI-NOTE-STORAGE-\d{3})[^\n]*\n(.*?)(?=^#{2,3} |\Z)', text, re.M | re.S))
    require(len(rows) == len({m.group(1) for m in rows}), 'duplicate requirement heading')
    return {m.group(1): m.group(2) for m in rows}


def raw_case_objects(text):
    decoder = json.JSONDecoder()
    pos = text.index('[', text.index('"cases"')) + 1
    result = []
    while True:
        while text[pos].isspace() or text[pos] == ',':
            pos += 1
        if text[pos] == ']':
            return result
        start = pos
        _, pos = decoder.raw_decode(text, pos)
        result.append(text[start:pos])


def exact_gzip(data):
    require(data[:10] == bytes.fromhex('1f8b0800000000000213'), 'fixture gzip header')
    decoder = zlib.decompressobj(-15)
    xml = decoder.decompress(data[10:]) + decoder.flush()
    trailer = decoder.unused_data
    require(decoder.eof and len(trailer) == 8, 'one gzip member / no extra bytes')
    crc, size = struct.unpack('<II', trailer)
    require(crc == zlib.crc32(xml) and size == len(xml) % (1 << 32), 'gzip CRC/size')
    require(gzip.decompress(data) == xml, 'gzip data agreement')
    return xml


def validate_fixture(data, predecessor):
    require(data == predecessor, 'fixture exact carry')
    return exact_gzip(data)


def validate_delta(old_text, new_text, patch):
    expected = ''.join(difflib.unified_diff(old_text.splitlines(True), new_text.splitlines(True), fromfile='midi-note-storage-v3/spec.md', tofile='midi-note-storage-v4/spec.md', n=3))
    require(patch == expected, 'exact minimal sanitized spec delta')


def validate_cases(cases, predecessor):
    require(len(cases) == 80, '80 cases')
    require(cases[:78] == predecessor, 'all 78 old case objects exact')
    require(len({c['id'] for c in cases}) == 80, 'unique IDs')
    templates = [('MNS-076', '002', 'KeyTracks/KeyTrack[2]/Notes/MidiNoteEvent[1]', 'NoteId', ' 7 '), ('MNS-077', '012', 'KeyTracks/KeyTrack', 'Id', '5')]
    for case, (cid, req, element, attribute, value) in zip(cases[78:], templates):
        require(case['id'] == cid and case['requirements'] == ['REQ-MIDI-NOTE-STORAGE-' + req], 'new IDs/requirement scope')
        require(case['action'] == 'validate-notes' and case['expected'] == {'local_reader_outcome': 'refused'}, 'local expected only')
        require(case['input'] == 'fixtures/MNS-001.als', 'authored base fixture only')
        require(case['input_projection'] == {'domain': 'decoded MidiClip/Notes', 'edits': [{'element': element, 'attribute': attribute, 'value': value}]}, 'exact input projection')
        require(case['reference_execution'] == case['candidate_execution'] == 'not-run', 'execution labels')
        require(case['expectation_provenance'] == 'static-derived; not observed reference output', 'static provenance')
        require(all(s in case['preconditions'] for s in ['conditional current field/list associations', 'ordinary reader context', 'A3 integer-field premise', 'A1 post-read checks do not gate', 'A2 supplies no saved result']), 'conditional premises')
        require(all(s in case['comparator'] for s in ['no public load/refusal', 'loaded state', 'rollback', 'saved text']), 'local/public separation')


def edited_input(case, fixture):
    # Projection of authored input data only; no expected output is computed.
    tree = ET.fromstring(fixture)
    original = tree.find(NOTES_PATH)
    require(original is not None, 'base Notes path')
    notes = copy.deepcopy(original)
    for edit in case['input_projection']['edits']:
        matches = notes.findall(edit['element'])
        require(len(matches) == (1 if case['id'] == 'MNS-076' else 2), 'exact projection match count')
        for node in matches:
            require(edit['attribute'] in node.attrib, 'edit existing attribute only')
            node.set(edit['attribute'], edit['value'])
    differences = []
    old_nodes, new_nodes = list(original.iter()), list(notes.iter())
    require(len(old_nodes) == len(new_nodes), 'projection element count')
    for index, (before, after) in enumerate(zip(old_nodes, new_nodes)):
        require(before.tag == after.tag and list(before.attrib) == list(after.attrib) and before.text == after.text and before.tail == after.tail, 'no shape/whitespace/attribute-set edit')
        for attr in before.attrib:
            if before.attrib[attr] != after.attrib[attr]:
                differences.append({'node_index': index, 'tag': before.tag, 'attribute': attr, 'before': before.attrib[attr], 'after': after.attrib[attr]})
    require(len(differences) == (1 if case['id'] == 'MNS-076' else 2), 'only intended attributes differ')
    if case['id'] == 'MNS-076':
        require(differences == [{'node_index': 9, 'tag': 'MidiNoteEvent', 'attribute': 'NoteId', 'before': '3', 'after': ' 7 '}], 'exact n3 text')
    else:
        require([(d['tag'], d['attribute'], d['before'], d['after']) for d in differences] == [('KeyTrack', 'Id', '0', '5'), ('KeyTrack', 'Id', '1', '5')], 'exact both Id edits')
    return differences


def main():
    pins = load(HERE / 'pins.json')
    for p in pins['files']:
        require(identity((ROOT / p['path']).read_bytes()) == {k: p[k] for k in ['bytes', 'sha256']}, 'pin ' + p['path'])
    for name in ['owner_asof', 'reviewed_owner_prefix']:
        p = pins[name]
        require(identity((ROOT / p['path']).read_bytes()[:p['bytes']]) == {k: p[k] for k in ['bytes', 'sha256']}, 'owner prefix ' + name)
    predecessor_manifest = load(OLD / 'manifest.json')
    for item in predecessor_manifest['files']:
        require(identity((OLD / item['path']).read_bytes()) == {k: item[k] for k in ['bytes', 'sha256']}, 'v3 predecessor payload ' + item['path'])
    old_cases = load(OLD / 'cases.json')['cases']
    case_text = (STAGE / 'cases.json').read_text()
    data = json.loads(case_text)
    validate_cases(data['cases'], old_cases)
    require(raw_case_objects(case_text)[:78] == raw_case_objects((OLD / 'cases.json').read_text()), 'all 78 raw serialized objects exact')
    old_spec, new_spec = (OLD / 'spec.md').read_text(), (STAGE / 'spec.md').read_text()
    validate_delta(old_spec, new_spec, (HERE / 'release-spec-delta.patch').read_text())
    old_bodies, new_bodies = bodies(old_spec), bodies(new_spec)
    require(len(old_bodies) == 14 and len(new_bodies) == 15, '14 carried/15 total requirement IDs')
    require(all(new_bodies[k] == v for k, v in old_bodies.items()), 'all 14 old bodies exact')
    require(set(new_bodies) - set(old_bodies) == {'REQ-MIDI-NOTE-STORAGE-012'}, 'only partial 012 added')
    old_fixtures = sorted((OLD / 'fixtures').glob('*.als'))
    require(len(old_fixtures) == 78 and {f.name for f in old_fixtures} == {f.name for f in (STAGE / 'fixtures').iterdir()}, 'same 78 fixture files only')
    gzip_results = {}
    for f in old_fixtures:
        data_bytes = (STAGE / 'fixtures' / f.name).read_bytes()
        gzip_results[f.name] = validate_fixture(data_bytes, f.read_bytes())
    projections = {c['id']: edited_input(c, gzip_results['MNS-001.als']) for c in data['cases'][78:]}
    links, anchors = 0, 0
    forbidden = re.compile(r'(?:\.\./|/)(?:analysis|wiki|raw)/|FUN_[0-9a-f]+|DAT_[0-9a-f]+|0x[0-9a-fA-F]{8,}|APerNoteAutomationAdapter|ARemoteableList|vptr|vtable|\b(?:param_\d+|uVar\d+)\b')
    for name in ['AGENTS.md', 'README.md', 'REVIEW.md', 'spec.md', 'cases.json', 'manifest.json']:
        text = (STAGE / name).read_text()
        require(not forbidden.search(text), 'sanitization ' + name)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in target:
                raise AssertionError('unapproved external link')
            filepart = target.split('#')[0]
            if filepart:
                resolved = (STAGE / filepart).resolve()
                require(resolved.is_relative_to(STAGE.resolve()) and resolved.exists(), 'isolated link ' + target)
                links += 1
            if '#' in target:
                linked = STAGE / filepart if filepart else STAGE / name
                headings = re.findall(r'^#{1,6} (.*)$', linked.read_text(), re.M)
                slugs = {re.sub(r'\s+', '-', re.sub(r'[^\w\s-]', '', h.lower())) for h in headings}
                require(target.split('#', 1)[1] in slugs, 'isolated heading ' + target)
                anchors += 1
    manifest = load(STAGE / 'manifest.json')
    require(manifest['case_count'] == 80 and manifest['fixture_count'] == 78 and len(manifest['partial_requirement_scopes']) == 15, 'manifest current units')
    require(manifest['supersedes']['release_id'] == 'midi-note-storage-v3' and manifest['supersedes']['manifest_sha256'] == pins['files'][0]['sha256'], 'single active v4-v3 supersession')
    require(manifest['release_status'] == data['status'] == 'candidate-unreviewed-unpublished', 'consistent candidate metadata')
    listed = {v['path'] for v in manifest['files']}
    actual = {str(f.relative_to(STAGE)) for f in STAGE.rglob('*') if f.is_file() and f.name != 'manifest.json'}
    require(listed == actual and len(listed) == 83, 'exact 83-payload candidate tree')
    for row in manifest['files']:
        require(identity((STAGE / row['path']).read_bytes()) == {k: row[k] for k in ['bytes', 'sha256']}, 'candidate payload ' + row['path'])
    negative = []
    def reject(name, altered):
        try:
            validate_cases(altered, old_cases)
        except (AssertionError, KeyError):
            negative.append({'name': name, 'status': 'rejected'})
            return
        raise AssertionError('negative not rejected ' + name)
    c = copy.deepcopy(data['cases']); c[0]['action'] = 'open'; reject('carried case changed', c)
    c = copy.deepcopy(data['cases']); c[-2]['expected']['outcome'] = 'refused'; reject('local refusal becomes public outcome', c)
    c = copy.deepcopy(data['cases']); c[-1]['expected']['saved_notes'] = {}; reject('local refusal gains saved state', c)
    c = copy.deepcopy(data['cases']); c[-2]['input_projection']['edits'][0]['value'] = '7'; reject('mixed spaces erased', c)
    c = copy.deepcopy(data['cases']); c[-1]['input_projection']['edits'][0]['attribute'] = 'MidiKey'; reject('duplicate Id becomes unsafe key edit', c)
    c = copy.deepcopy(data['cases']); c[-1]['input'] = 'fixtures/MNS-059.als'; reject('different input carrier', c)
    c = copy.deepcopy(data['cases']); c[-1]['preconditions'] = 'unconditional'; reject('premises erased', c)
    changed_fixture = bytearray((STAGE / 'fixtures/MNS-001.als').read_bytes()); changed_fixture[12] ^= 1
    try:
        validate_fixture(bytes(changed_fixture), (OLD / 'fixtures/MNS-001.als').read_bytes())
    except AssertionError:
        negative.append({'name': 'changed carried fixture', 'status': 'rejected'})
    else:
        raise AssertionError('fixture negative not rejected')
    for label, damaged in [('extra gzip member/trailing byte', (STAGE / 'fixtures/MNS-001.als').read_bytes() + b'x'), ('bad CRC', (STAGE / 'fixtures/MNS-001.als').read_bytes()[:-8] + b'\x00\x00\x00\x00' + (STAGE / 'fixtures/MNS-001.als').read_bytes()[-4:])]:
        try:
            exact_gzip(damaged)
        except (AssertionError, zlib.error):
            negative.append({'name': label, 'status': 'rejected'})
        else:
            raise AssertionError('gzip negative not rejected ' + label)
    try:
        validate_delta(old_spec, new_spec, (HERE / 'release-spec-delta.patch').read_text() + 'unapproved appended row\n')
    except AssertionError:
        negative.append({'name': 'corrupt minimal spec delta', 'status': 'rejected'})
    else:
        raise AssertionError('patch negative not rejected')
    print(json.dumps({'schema':'bounded-handoff-staging-check-v1','status':'pass','carried_case_objects_exact':78,'raw_serialized_case_objects_exact':78,'carried_requirement_bodies_exact':14,'partial_requirement_ids':15,'case_count':80,'fixture_count':78,'fixture_bytes_exact':True,'gzip_single_member_crc_size_checked':78,'new_fixtures_generated':0,'decoded_input_projection_differences':projections,'isolated_local_links_checked':links,'isolated_heading_anchors_checked':anchors,'minimal_spec_delta_exact':True,'candidate_payloads_hashed':83,'predecessor_payloads_hashed':len(predecessor_manifest['files']),'pins_checked':len(pins['files']),'owner_prefixes_checked':2,'negative_controls':negative,'sanitization':'bounded forbidden native/source identifier and restricted-link scan plus authored content inspection','new_original_or_candidate_calls':0,'public_U_resolutions':0,'limits':['Input edits are authored XML-data projections; no parser/list expectation is re-derived by a model.','The deliberately malformed carried MNS-012 XML is not reparsed or repaired.','Predecessor structure/schema approval is inherited through exact bytes, not rerun through old helpers.','Independent handoff content review/external exact-tree seal/full coordinator prerelease lint remain pending.']},indent=2))


if __name__ == '__main__':
    main()
