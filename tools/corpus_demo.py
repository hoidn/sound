#!/usr/bin/env python3
"""Analyst-only: build the interactive Corpus resonator demo from shipped Live 12.4.3 files.

Usage: python3 tools/corpus_demo.py [--resources APP_RESOURCES] [--out DIR]

Reads the Corpus class of Schema/12.0_12402.txt and every shipped Corpus preset (.adv, gzip XML),
writes corpus-parameters.json (field list, per-preset values, observed ranges, input SHA-256s)
and an offline index.html built from tools/corpus_demo.html. Nothing is executed from the bundle
and no decompiled code is used: the page's sound comes from a labelled textbook stand-in model.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

from build_artifact_browser import STYLE

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = Path.home() / 'Ableton Live 12 Suite.app/Contents/App-Resources'
OUT = ROOT / 'analysis/ableton-live-12.4.3/demos/corpus'
SCHEMA = 'Schema/12.0_12402.txt'
PRESETS = 'Core Library/Devices/Audio Effects/Corpus'
# Title patterns that name a resonance type; used only to corroborate an assumed index order.
TYPE_WORDS = {'Beam': r'\bBeam', 'Marimba': r'\bMarimba', 'String': r'\bString', 'Membrane': r'\bMembrane',
              'Plate': r'\bPlate', 'Pipe': r'\bPipe', 'Tube': r'\bTub(e|ular)'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def schema_fields(data):
    """Field names and classes of the Corpus class, in declared order."""
    root = ET.fromstring(data)
    corpus = root.find('Corpus')
    if corpus is None:
        raise ValueError('Schema has no Corpus class')
    return [{'name': f.tag, 'class': f.get('Class')} for f in corpus]


def value(element, path):
    found = element.find(path)
    if found is None or found.get('Value') is None:
        raise ValueError(f'{element.tag}: missing {path} Value')
    return found.get('Value')


def preset_values(data):
    """Manual value and MidiControllerRange of every parameter of one preset's Corpus element."""
    corpus = ET.fromstring(data).find('Corpus')
    if corpus is None:
        raise ValueError('Preset has no Corpus element')
    values, ranges = {}, {}
    for param in corpus:
        manual = param.find('Manual')
        if manual is None:
            continue
        values[param.tag] = manual.get('Value')
        r = param.find('MidiControllerRange')
        if r is not None:
            ranges[param.tag] = [float(value(r, 'Min')), float(value(r, 'Max'))]
    return values, ranges


def extract(resources):
    schema_bytes = (resources / SCHEMA).read_bytes()
    fields = schema_fields(schema_bytes)
    presets, ranges, type_names = [], {}, {}
    for path in sorted((resources / PRESETS).glob('*.adv')):
        if path.name.startswith('._'):
            continue
        raw = path.read_bytes()
        values, preset_ranges = preset_values(gzip.decompress(raw))
        for name, r in preset_ranges.items():
            if ranges.setdefault(name, r) != r:
                raise ValueError(f'{path.name}: {name} range {r} differs from {ranges[name]}')
        presets.append({'name': path.stem, 'path': f'{PRESETS}/{path.name}', 'sha256': sha(raw), 'values': values})
        for word, pattern in TYPE_WORDS.items():
            if re.search(pattern, path.stem):
                type_names.setdefault(word, set()).add(int(values['ResonanceType']))
    return {
        'schema': {'path': SCHEMA, 'sha256': sha(schema_bytes), 'fields': fields},
        'presets': presets,
        'ranges': dict(sorted(ranges.items())),
        'type_index_from_preset_names': {w: sorted(v) for w, v in sorted(type_names.items())},
    }


def build(resources, out):
    data = extract(resources)
    out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=1, sort_keys=True)
    (out / 'corpus-parameters.json').write_text(text + '\n', encoding='utf-8')
    template = (Path(__file__).with_name('corpus_demo.html')).read_text(encoding='utf-8')
    embedded = text.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    page = template.replace('/*STYLE*/', STYLE).replace('/*CORPUS_DATA*/null', embedded)
    (out / 'index.html').write_text(page, encoding='utf-8')
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--resources', type=Path, default=RESOURCES)
    parser.add_argument('--out', type=Path, default=OUT)
    args = parser.parse_args(argv)
    data = build(args.resources, args.out)
    print(json.dumps({'out': str(args.out / 'index.html'), 'presets': len(data['presets']),
                      'parameters_with_ranges': len(data['ranges']),
                      'type_index_from_preset_names': data['type_index_from_preset_names']}, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
