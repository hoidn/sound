"""Read-only recording evidence inventory; does not run Live or original code."""
import gzip
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
BUNDLE = Path('/home/ollie/Ableton Live 12 Suite.app')
SCHEMA = BUNDLE / 'Contents/App-Resources/Schema/12.0_12402.txt'
CORPUS = Path('/var/tmp/sound-analysis/corpus')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def lane_records(node, path=''):
    path += '/' + node.tag
    if 'Id' in node.attrib:
        path += '[@Id="' + node.attrib['Id'] + '"]'
    if node.tag == 'TakeLane':
        yield {'path': path, 'attributes': node.attrib,
               'fields': {e.tag: e.attrib for e in node if e.tag != 'ClipAutomation'},
               'clips': [{'class': e.tag, 'attributes': e.attrib,
                          'fields': {f.tag: f.attrib for f in e if f.tag in
                                     {'Name', 'TakeId', 'CurrentStart', 'CurrentEnd'}}}
                         for e in node.findall('./ClipAutomation/Events/*')]}
    for child in node:
        yield from lane_records(child, path)


def main():
    schema_bytes = SCHEMA.read_bytes()
    schema = ET.fromstring(schema_bytes)
    classes = {'TakeLane', 'TakeLanes', 'Transport', 'Metronome', 'AudioTrack',
               'MidiTrack', 'AudioClip', 'MidiClip', 'TrackDevice', 'LiveSet'}
    rows = []
    for cls in schema:
        if cls.tag in classes:
            rows.append({'class': cls.tag, 'fields': [dict(name=e.tag, **e.attrib) for e in cls]})
    assert {'TakeLane', 'TakeLanes'}.issubset({r['class'] for r in rows})
    write('schema-fields.json', {'source': str(SCHEMA), 'sha256': digest(schema_bytes), 'classes': rows})
    documents = []
    for path in sorted((BUNDLE / 'Contents/App-Resources').rglob('*')):
        if path.suffix not in {'.als', '.alc'} or path.name.startswith('._'):
            continue
        data = path.read_bytes()
        root = ET.fromstring(gzip.decompress(data) if data[:2] == b'\x1f\x8b' else data)
        lanes = list(lane_records(root))
        documents.append({'source': str(path), 'sha256': digest(data),
                          'take_lane_count': len(lanes),
                          'take_lanes': lanes,
                          'take_ids': [e.attrib for e in root.iter('TakeId')],
                          'monitor_states': [e.attrib for e in root.iter('CurrentMonitoringState')],
                          'punch_in': [e.attrib for e in root.iter('PunchIn')],
                          'punch_out': [e.attrib for e in root.iter('PunchOut')]})
    assert documents
    write('shipped-documents.json', documents)
    wanted = {'TakeLane', 'CaptureMidi', 'CountInDurationInBars', 'PunchIn', 'PunchOut', 'Audition'}
    strings = []
    source = CORPUS / 'indexes/strings.jsonl'
    with source.open('rb') as f:
        for number, line in enumerate(f, 1):
            record = json.loads(line)
            if record.get('value') in wanted and record.get('refs'):
                strings.append({'line': number, 'line_sha256': digest(line), 'record': record})
    assert wanted == {r['record']['value'] for r in strings}
    write('native-string-excerpts.json', {'source': str(source), 'sha256': digest(source.read_bytes()),
                                        'scope': 'Inventory only; no runtime behavior inferred.', 'rows': strings})
    write('summary.json', {'documents': len(documents),
                          'documents_with_take_lanes': sum(bool(d['take_lane_count']) for d in documents),
                          'take_lanes': sum(d['take_lane_count'] for d in documents),
                          'clips_with_take_id': sum(len(d['take_ids']) for d in documents),
                          'native_strings': len(strings),
                          'schema_sha256': digest(schema_bytes),
                          'executed_original_code': False})


if __name__ == '__main__':
    main()
