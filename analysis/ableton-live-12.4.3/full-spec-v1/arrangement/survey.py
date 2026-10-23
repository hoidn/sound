"""Read-only schema and one shipped Set inventory; no edit operations or Live run."""
from pathlib import Path
import gzip, hashlib, json, xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
BUNDLE = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources')
SCHEMA = BUNDLE / 'Schema/12.0_12402.txt'
DEMO = BUNDLE / 'Core Library/Lessons/Demo Songs/Chuck Sutton - Patience (Live 12 Suite Demo).als'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = ET.fromstring(SCHEMA.read_bytes())
    names = ['AudioClip', 'MidiClip', 'ClipFades', 'Locator', 'CuePointManager',
             'LinkedTrackGroup', 'TimeSelection', 'TimeableMidiClip', 'TimeableSample', 'ListAutomation',
             'AudioTrack', 'MidiTrack', 'GroupTrack', 'LiveSet']
    classes = {}
    for name in names:
        element = root.find(name)
        if element is not None:
            classes[name] = {'attributes': element.attrib,
                             'fields': [{'name': c.tag, **c.attrib} for c in element]}
    assert set(names) <= classes.keys(), 'schema class missing'
    assert any(c['name'] == 'Fades' and c['Class'] == 'ClipFades' for c in classes['AudioClip']['fields'])
    doc = ET.fromstring(gzip.decompress(DEMO.read_bytes()))
    assert doc.attrib['MinorVersion'] == '12.0_12402'
    records = []
    for track in doc.findall('./LiveSet/Tracks/*'):
        container = "Sample" if track.tag == "AudioTrack" else "ClipTimeable"
        base = f"/Ableton/LiveSet/Tracks/{track.tag}[@Id='{track.attrib['Id']}']/DeviceChain/MainSequencer/{container}/ArrangerAutomation/Events"
        for clip in track.findall(f'./DeviceChain/MainSequencer/{container}/ArrangerAutomation/Events/*'):
            if clip.tag not in ('AudioClip', 'MidiClip'):
                continue
            record = {'xpath': base + f"/{clip.tag}[@Id='{clip.attrib['Id']}']", 'type': clip.tag,
                      'attributes': clip.attrib,
                      'fields': {tag: clip.find(tag).attrib if clip.find(tag) is not None else None
                                 for tag in ['Name', 'CurrentStart', 'CurrentEnd', 'Disabled', 'IsWarped']},
                      'fades': {c.tag: c.attrib for c in clip.findall('./Fades/*')}}
            assert record['fields']['CurrentStart'] is not None
            assert record['fields']['CurrentEnd'] is not None
            records.append(record)
    locators = [{'xpath': f"/Ableton/LiveSet/Locators/Locators/Locator[@Id='{e.attrib['Id']}']",
                 'attributes': e.attrib, 'fields': {c.tag: c.attrib for c in e}}
                for e in doc.findall('./LiveSet/Locators/Locators/Locator')]
    assert records and locators
    assert {r['type'] for r in records} == {'AudioClip', 'MidiClip'}
    assert len({r['xpath'] for r in records}) == len(records)
    result = {'schema': {'path': str(SCHEMA), 'sha256': sha(SCHEMA), 'attributes': root.attrib, 'classes': classes},
              'demo': {'path': str(DEMO), 'sha256': sha(DEMO), 'attributes': doc.attrib,
                       'main_lane_clips': records, 'locators': locators,
                       'linked_track_groups': [e.attrib for e in doc.findall('./LiveSet/LinkedTrackGroups/*')]},
              'limits': 'Document bytes only; Creator 12.4d1, not a 12.4.3 save or observed edit. No take-lane/session clips counted.'}
    (OUT / 'schema-demo-survey.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'schema_sha256': sha(SCHEMA), 'demo_sha256': sha(DEMO),
                      'schema_classes': len(classes), 'main_lane_clips': len(records),
                      'audio_clips': sum(r['type'] == 'AudioClip' for r in records),
                      'midi_clips': sum(r['type'] == 'MidiClip' for r in records),
                      'locators': len(locators), 'asserts': 'pass'}, indent=2))


if __name__ == '__main__':
    main()
