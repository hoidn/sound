"""Versioned analyst checker: recognize the retained 11.0_405 structural names.

Usage: python3 -I -B schema_check.py <matching-schema.txt> <doc.als|doc.xml>...
Uses the sealed T11 v1 schema walker and measurements unchanged except for the
SceneNames and MasterTrack measurements of 11.0_405. It does not migrate or repair
documents and does not establish that Live accepts them.
"""
import gzip
import importlib.util
import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
_path = Path(__file__).resolve().parent.parent / 't11-structure-v1/schema_check.py'
_spec = importlib.util.spec_from_file_location('t11_schema_v1', _path)
legacy = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(legacy)
load_schema = legacy.load_schema
check = legacy.check


def rules(root, pointees):
    result = legacy.rules(root, pointees)
    if root.get('MinorVersion') != '11.0_405':
        return result
    ls = root.find('LiveSet')
    scenes = ls.find('SceneNames')
    result['scenes'] = 0 if scenes is None else len(scenes)
    result['scenes_present'] = scenes is not None
    result['main_slots_equal_scenes'] = all(
        len(track.findall('DeviceChain/MainSequencer/ClipSlotList/ClipSlot')) == result['scenes']
        for track in ls.findall('Tracks/*') if track.tag in {'AudioTrack', 'MidiTrack'})
    result['main_prehear_no_sends'] = all(
        not track.findall('DeviceChain/Mixer/Sends/TrackSendHolder')
        for name in ('MasterTrack', 'PreHearTrack') for track in ls.findall(name))
    return result


def main():
    schema = load_schema(sys.argv[1])
    for path in sys.argv[2:]:
        data = Path(path).read_bytes()
        try:
            root = ET.fromstring(gzip.decompress(data) if data[:2] == b'\x1f\x8b' else data)
            if root.find('LiveSet') is None:
                raise ValueError('no LiveSet element')
        except (ET.ParseError, OSError, EOFError, ValueError) as error:
            print(json.dumps({'doc': path, 'error': f'{type(error).__name__}: {error}'}))
            continue
        deviations, pointees = check(schema, root)
        print(json.dumps({'doc': path.rsplit('/App-Resources/', 1)[-1], 'minor': root.get('MinorVersion'),
                          'deviations': deviations, 'rules': rules(root, pointees)}, sort_keys=True))


if __name__ == '__main__':
    main()
