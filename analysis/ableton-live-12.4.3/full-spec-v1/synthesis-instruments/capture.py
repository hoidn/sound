"""Read five inventory-selected presets and reuse two already pinned sources."""
from pathlib import Path
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
PRIOR = OUT.parent / 'sample-instruments'
APP = Path('/home/ollie/Ableton Live 12 Suite.app')
DEVICES = {'Drift': 'Drift', 'Drum Sampler': 'DrumCell', 'Meld': 'InstrumentMeld',
           'Operator': 'Operator', 'Wavetable': 'InstrumentVector'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

sources = []
for original in json.loads((PRIOR / 'sources.json').read_text())[:2]:
    record = dict(original)
    record['file'] = '../sample-instruments/' + original['file']
    assert digest((OUT / record['file']).read_bytes()) == record['sha256']
    record['reuse'] = 'External pin; retained capture reused without recapture or mutation'
    sources.append(record)
assert sources[0]['sha256'] == '3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a'
assert sources[1]['sha256'] == 'b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
schema_bytes = (OUT / sources[1]['file']).read_bytes()
schema = ET.fromstring(schema_bytes)
lines = schema_bytes.decode().splitlines()
records = {node.tag: {'line': next(i + 1 for i, line in enumerate(lines)
                                 if line.strip() == f'<{node.tag}>'),
                      'fields': [{'name': child.tag, **child.attrib} for child in node]}
           for node in schema if node.tag in DEVICES.values()}
assert set(records) == set(DEVICES.values())
write('schema-fields.json', records)
inventory = json.loads((OUT.parent / 'inventory/devices.json').read_text())
observations = []
for name, cls in DEVICES.items():
    entry = next(item for item in inventory if item['name'] == name)
    data = (APP / entry['example']['path']).read_bytes()
    assert len(data) == entry['example']['bytes']
    assert digest(data) == entry['example']['sha256']
    xml = gzip.decompress(data)
    root = ET.fromstring(xml)
    node = root.find(cls)
    assert root.tag == 'Ableton' and node is not None
    slug = name.lower().replace(' ', '-')
    filename = f'preset-{slug}.adv'
    (OUT / filename).write_bytes(data)
    (OUT / f'preset-{slug}.xml').write_bytes(xml)
    sources.append({'id': 'SYNTHESIS-PRESET-' + slug.upper(), 'path': str(APP / entry['example']['path']),
                    'file': filename, 'bytes': len(data), 'sha256': digest(data),
                    'version': root.attrib, 'locator': f'/Ableton/{cls}',
                    'limit': 'Shipped preset root/field presence only; no constructor defaults, enum map, reader/writer or sound proof'})
    observations.append({'device': name, 'class': cls, 'inventory_id': entry['id'],
                         'schema_line': records[cls]['line'], 'preset_locator': f'/Ableton/{cls}',
                         'creator': root.attrib, 'top_level_fields': [child.tag for child in node],
                         'sample_refs': len(list(node.iter('SampleRef')))})
write('preset-observations.json', observations)
write('sources.json', sources)
print(json.dumps({'sources': len(sources), 'schema_classes': len(records), 'presets': len(observations),
                  'original_execution': False, 'network_capture': False}))
