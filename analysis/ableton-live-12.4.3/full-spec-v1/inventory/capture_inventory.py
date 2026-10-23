"""Static inventory; run only in a new capture directory to preserve evidence."""
import collections
import gzip
import hashlib
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

OUT = pathlib.Path(__file__).resolve().parent
APP = pathlib.Path('/home/ollie/Ableton Live 12 Suite.app')
RES = APP / 'Contents/App-Resources'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(name, value):
    path = OUT / name
    assert not path.exists(), f'Preserve previous capture: {path}'
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def source(path, locator):
    data = path.read_bytes()
    return {'path': str(path.relative_to(APP)), 'sha256': sha(data),
            'bytes': len(data), 'locator': locator}


class Toc(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get('href', '')
        if tag == 'a' and '/live-manual/12/' in href:
            self.anchor = [href, '', self.getpos()[0]]

    def handle_data(self, data):
        if self.anchor is not None:
            self.anchor[1] += data

    def handle_endtag(self, tag):
        if tag != 'a' or self.anchor is None:
            return
        href, title, line = self.anchor
        self.anchor = None
        match = re.match(r'^(\d+(?:\.\d+)*)(?:\.)?\s+(.+)$', title.strip())
        if match:
            number, title = match.groups()
            slug, anchor = href.split('/12/')[1].split('/#')
            self.rows.append({'id': 'SURF-MAN-' + slug.upper() + '--' + anchor.upper(),
                              'number': number, 'title': title, 'url': 'https://www.ableton.com' + href,
                              'html_line': line, 'target_match': 'version-uncertain',
                              'specification': 'unmapped', 'complete': False})


manual_path = OUT / 'manual-12-toc-2026-10-19.html'
toc = Toc()
toc.feed(manual_path.read_text())
assert len({r['id'] for r in toc.rows}) == len(toc.rows)
assert len([r for r in toc.rows if '.' not in r['number']]) == 43
for row in toc.rows:
    row['leaf'] = not any(other['number'].startswith(row['number'] + '.') for other in toc.rows)
save('manual-toc.json', toc.rows)

schema_path = RES / 'Schema/12.0_12402.txt'
schema_bytes = schema_path.read_bytes()
schema_text = schema_bytes.decode()
schema = ET.fromstring(schema_bytes)
classes = []
for cls in schema:
    match = re.search(r'(?m)^\t<' + re.escape(cls.tag) + r'(?:\s|>)', schema_text)
    assert match, cls.tag
    line = schema_text[:match.start()].count('\n') + 1
    classes.append({'id': 'SURF-SCHEMA-' + cls.tag.upper(), 'class': cls.tag, 'line': line,
                    'fields': [{'name': el.tag, **el.attrib} for el in cls],
                    'specification': 'unmapped', 'complete': False})
assert len(classes) == 412 and len({r['id'] for r in classes}) == 412
save('schema-classes.json', {'source': source(schema_path, '/AbletonSchema'), 'classes': classes})
schema_capture = OUT / '12.0_12402.txt'
if schema_capture.exists():
    assert schema_capture.read_bytes() == schema_bytes
else:
    schema_capture.write_bytes(schema_bytes)

directories = []
for library in ('Builtin', 'Core Library'):
    for category in ('Audio Effects', 'MIDI Effects', 'Instruments'):
        for path in sorted((RES / library / 'Devices' / category).iterdir()):
            if path.is_dir() and not path.name.startswith('._'):
                directories.append(str(path.relative_to(RES)))
save('package-device-directories.json', directories)

# A root element is directly observed; the product-name alias remains an inference
# unless a matching default/preset name or product directory supplies the pairing.
examples = {}
root_counts = collections.Counter()
document_count = 0
for library in ('Builtin', 'Core Library'):
    for path in sorted((RES / library).rglob('*')):
        if path.name.startswith('._') or path.suffix not in ('.adv', '.adg', '.alc', '.als'):
            continue
        data = path.read_bytes()
        xml = gzip.decompress(data) if data.startswith(b'\x1f\x8b') else data
        root = ET.fromstring(xml)
        document_count += 1
        elements = list(root) if path.suffix == '.adv' else []
        elements += [el for parent in root.findall('.//Devices') for el in parent]
        for el in elements:
            if el.tag not in {r['class'] for r in classes}:
                continue
            root_counts[el.tag] += 1
            if el.tag not in examples:
                examples[el.tag] = source(path, '/Ableton/' + el.tag if el in list(root) else './/Devices/' + el.tag)
save('preset-device-roots.json', {'parsed_documents': document_count, 'parse_failures': 0,
                                 'counts': dict(sorted(root_counts.items())), 'examples': examples})

aliases = {
    'Auto Filter': 'AutoFilter2', 'Auto Pan-Tremolo': 'AutoPan2', 'Channel EQ': 'ChannelEq',
    'Chorus-Ensemble': 'Chorus2', 'Compressor': 'Compressor2', 'Drum Buss': 'DrumBuss',
    'Dynamic Tube': 'Tube', 'EQ Eight': 'Eq8', 'EQ Three': 'FilterEQ3', 'External Audio Effect': 'BufferAudioDevice',
    'Glue Compressor': 'GlueCompressor', 'Hybrid Reverb': 'Hybrid', 'Phaser-Flanger': 'PhaserNew',
    'Redux': 'Redux2', 'Erosion': 'Erosion2', 'Resonators': 'Resonator', 'Spectral Resonator': 'Spectral',
    'Spectral Time': 'Transmute', 'Spectrum': 'SpectrumAnalyzer', 'Utility': 'StereoGain',
    'Vinyl Distortion': 'Vinyl', 'CC Control': 'MidiCcControl', 'Arpeggiator': 'MidiArpeggiator',
    'Chord': 'MidiChord', 'Note Length': 'MidiNoteLength', 'Pitch': 'MidiPitcher',
    'Random': 'MidiRandom', 'Scale': 'MidiScale', 'Velocity': 'MidiVelocity',
    'Analog': 'UltraAnalog', 'Electric': 'LoungeLizard', 'Tension': 'StringStudio',
    'Drum Sampler': 'DrumCell', 'External Instrument': 'BufferInstrument',
    'Impulse': 'InstrumentImpulse', 'Meld': 'InstrumentMeld', 'Sampler': 'MultiSampler',
    'Simpler': 'OriginalSimpler', 'Wavetable': 'InstrumentVector',
}
devices = []
for row in toc.rows:
    if re.fullmatch(r'(29|30|31)\.\d+', row['number']):
        name = row['title']
        cls = aliases.get(name, name.replace(' ', ''))
        assert cls in {r['class'] for r in classes}, (name, cls)
        category = {'29': 'Audio Effects', '30': 'MIDI Effects', '31': 'Instruments'}[row['number'].split('.')[0]]
        directory = f'Builtin/Devices/{category}/{name}'
        assert directory in directories
        devices.append({'id': 'SURF-DEVICE-' + row['url'].split('#')[1].upper(), 'name': name,
                        'kind': 'native', 'manual_id': row['id'], 'package_directory': directory,
                        'schema_class': cls, 'schema_line': next(r['line'] for r in classes if r['class'] == cls),
                        'alias_basis': 'preset-root-and-name' if cls in examples else 'schema-and-product-directory; semantic alias inferred',
                        'example': examples.get(cls), 'target_match': 'installed-product-name-and-schema',
                        'specification': 'partial' if name in ('Analog', 'Electric', 'Tension', 'Corpus', 'Collision', 'Amp', 'Cabinet') else 'unspecified',
                        'complete': False,
                        'deferred': name in ('Amp', 'Cabinet')})
for name, cls, category in [('Audio Effect Rack','AudioEffectGroupDevice','Audio Effects'),
                            ('MIDI Effect Rack','MidiEffectGroupDevice','MIDI Effects'),
                            ('Instrument Rack','InstrumentGroupDevice','Instruments'),
                            ('Drum Rack','DrumGroupDevice','Instruments')]:
    devices.append({'id': 'SURF-DEVICE-' + name.upper().replace(' ', '-'), 'name': name,
                    'kind': 'rack', 'schema_class': cls, 'example': examples.get(cls),
                    'package_directory': f'Builtin/Devices/{category}/{name}',
                    'target_match': 'installed', 'specification': 'partial-structure-only', 'complete': False})
legacy = {'Auto Filter Legacy':'AutoFilter','Auto Pan':'AutoPan','Chorus':'Chorus',
          'Erosion Legacy':'Erosion','Flanger':'Flanger','Frequency Shifter':'FrequencyShifter',
          'Phaser':'Phaser','Redux Legacy':'Redux'}
for name, cls in legacy.items():
    devices.append({'id': 'SURF-DEVICE-LEGACY-' + name.upper().replace(' ', '-'), 'name': name,
                    'kind':'legacy-native', 'schema_class':cls, 'example':examples.get(cls),
                    'package_directory':'Core Library/Devices/Audio Effects/Legacy/' + name,
                    'target_match':'installed', 'specification':'unspecified','complete':False})
for path in sorted((RES / 'Builtin/Devices').rglob('*.amxd')):
    if path.name.startswith('._'):
        continue
    devices.append({'id':'SURF-MAX-' + path.stem.upper().replace(' ', '-'), 'name':path.stem,
                    'kind':'max-midi-tool' if '/MIDI Tools/' in str(path) else 'max-device',
                    'source':source(path, 'complete AMXD bytes; no patch execution'),
                    'target_match':'installed','specification':'unspecified','complete':False})
for path in sorted((RES / 'Misc').rglob('*.amxd')):
    if path.name.startswith('._'):
        continue
    devices.append({'id':'SURF-MAX-TEMPLATE-' + path.stem.upper().replace(' ', '-'), 'name':path.stem,
                    'kind':'max-template', 'source':source(path, 'complete AMXD bytes; no patch execution'),
                    'target_match':'installed','specification':'unspecified','complete':False})
assert len({row['id'] for row in devices}) == len(devices)
save('devices.json', devices)

services = []
paths = ['Contents/MacOS/Live', 'Contents/Info.plist']
paths += [str(path.relative_to(APP)) for path in sorted((RES / 'Extensions').rglob('*'))
          if path.is_file() and not path.name.startswith('._')]
paths += ['Contents/Push2/Push2DisplayProcess.app/Contents/MacOS/Push2DisplayProcess',
          'Contents/Helpers/Push3.app/Contents/MacOS/Push3',
          'Contents/App-Resources/Max/Max.app/Contents/MacOS/Max']
paths += [str(path.relative_to(APP)) for path in sorted((APP/'Contents/Resources').rglob('*'))
          if path.is_file() and not path.name.startswith('._') and path.parent.name == 'MacOS']
for item in paths:
    path = APP/item
    if not path.exists():
        continue
    services.append({'id':'SURF-SERVICE-' + path.stem.upper().replace(' ', '-'),
                     'source':source(path, 'whole file'), 'target_match':'installed-mac-package',
                     'specification':'unmapped','complete':False})
save('services-platforms.json', {'services':services,
                               'platform_obligations':['macOS arm64','macOS x86_64','Windows version applicability unknown'],
                               'limits':'Package presence does not establish invocation or supported runtime behavior.'})
controllers = []
for path in sorted((RES / 'MIDI Remote Scripts').iterdir()):
    if not path.is_dir() or path.name.startswith('._'):
        continue
    init = path / '__init__.pyc'
    controllers.append({'id':'SURF-SCRIPT-' + path.name.upper().replace(' ', '-'),
                        'name':path.name, 'path':str(path.relative_to(APP)),
                        'kind':'support-or-internal' if path.name.startswith('_') or path.name == 'ableton' else 'named-controller-module; identity not behavior',
                        'source':source(init, 'complete bytecode bytes; not executed') if init.exists() else None,
                        'specification':'unmapped','complete':False})
assert len({row['id'] for row in controllers}) == len(controllers)
save('controller-profiles.json', controllers)
tools = [row for row in toc.rows if re.fullmatch(r'11\.[23]\.\d+', row['number'])]
save('midi-tools.json', tools)
denominator = {'revision':'full-spec-v1', 'target':'Ableton Live 12 Suite 12.4.3',
               'inventory_status':'finite-open-baseline; not all behavior discovered',
               'manual_headings':len(toc.rows), 'manual_leaves':sum(r['leaf'] for r in toc.rows),
               'manual_chapters':43, 'device_profiles':len(devices),
               'device_kinds':dict(collections.Counter(r['kind'] for r in devices)),
               'schema_classes':412, 'service_files':len(services),
               'controller_and_support_modules':len(controllers), 'midi_tool_profiles':len(tools),
               'complete_profiles':0,
               'rules':'Separate overlapping inventory dimensions; never add these counts or use page count as behavior coverage. Every leaf and profile requires reviewed applicability and behavioral mapping before closure.'}
save('coverage-denominator.json', denominator)
manifest = {'capture_date':'2026-10-19', 'target':'Ableton Live 12 Suite 12.4.3',
            'source_root':str(APP), 'method':'Python stdlib static reads, XML/gzip parsing, HTML TOC parsing; no original code execution',
            'manual':{'url':'https://www.ableton.com/en/live-manual/12/welcome-to-live/',
                      'version':'12, mutable current manual; not pinned to 12.4.3',
                      'sha256':sha(manual_path.read_bytes())},
            'source_identity':source(APP/'Contents/Info.plist','CFBundleShortVersionString'),
            'files':{path.name:{'sha256':sha(path.read_bytes()),'bytes':path.stat().st_size}
                     for path in sorted(OUT.iterdir()) if path.is_file() and path.name != 'manifest.json'},
            'retention':'Manual HTML and latest schema bytes retained. External installed preset, AMXD and executable bytes are hash-addressed by exact original paths; not copied here.'}
save('manifest.json', manifest)
print(json.dumps(denominator, indent=2))
