#!/usr/bin/env python3
"""Read retained menu archives as plain data; no Cocoa decoding or selectors."""
from pathlib import Path
import copy
import hashlib
import json
import plistlib
import xml.etree.ElementTree as ET

P = Path(__file__).resolve().parent


def identity(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def reconcile(report):
    info = plistlib.loads((P / 'Info.plist').read_bytes())
    archive = plistlib.loads((P / 'keyedobjects.nib').read_bytes())
    objects = archive['$objects']
    assert archive['$archiver'] == 'NSKeyedArchiver' and len(objects) == 167
    strings = [{'object_index': i, 'literal': o} for i, o in enumerate(objects) if isinstance(o, str)]
    def primitive(value):
        if isinstance(value, plistlib.UID):
            assert 0 <= value.data < len(objects)
            target = objects[value.data]
            return {'uid': value.data, 'literal': target if isinstance(target, (str, int, bool, float)) else None}
        return value
    menus = [{'object_index': i, 'fields': {k: primitive(v) for k, v in obj.items()}}
             for i, obj in enumerate(objects) if isinstance(obj, dict)
             and any(k in obj for k in ['NSTitle', 'NSKeyEquiv', 'NSAction', 'NSKeyEquivModMask'])]
    xml = ET.fromstring((P / 'designable.nib').read_bytes())
    labels = [{'element_index': i, 'tag': e.tag, 'attributes': dict(e.attrib), 'literal': e.text}
              for i, e in enumerate(xml.iter()) if e.attrib.get('key') in ['NSName', 'label']]
    assert report['reported_bundle_version'] == {k: info[k] for k in ['CFBundleShortVersionString', 'CFBundleVersion']}
    assert info['CFBundleShortVersionString'] == '12.4.3 (2026-07-07_e3d8be4d07)'
    assert report['archive']['archiver'] == archive['$archiver']
    assert report['archive']['objects'] == len(objects)
    assert report['archive']['literal_strings'] == strings and len(strings) == 65
    assert report['archive']['menu_keyed_records'] == menus and len(menus) == 17
    queries = {q: [x['object_index'] for x in strings if q in x['literal'].casefold()]
               for q in ['export', 'rename', 'midi', 'audio']}
    assert report['archive']['literal_negative_queries'] == queries and not any(queries.values())
    assert report['designable'] == {'root_tag': xml.tag, 'root_attributes': dict(xml.attrib),
        'element_count': sum(1 for _ in xml.iter()), 'selected_name_and_connection_label_records': labels}
    assert len(labels) == 19
    assert report['target_grade'] == 'U' and report['expected'] is report['comparison'] is None
    assert report['executed'] is report['original_vendor_code_executed'] is False
    assert report['new_requirements'] == report['new_cases'] == report['complete_topics'] == 0


def run():
    watch = {p: identity(p) for p in P.iterdir() if p.is_file()}
    manifest = json.loads((P / 'manifest.json').read_text())
    assert set(manifest['files']) == {p.name for p in P.iterdir() if p.is_file() and p.name != 'manifest.json'}
    assert all(identity(P / name) == item for name, item in manifest['files'].items())
    report = json.loads((P / 'query.json').read_text())
    for item in report['inputs']:
        assert identity(P / item['retained_file']) == {k: item[k] for k in ['bytes', 'sha256']}
    reconcile(report)
    variants = []
    wrong = copy.deepcopy(report); wrong['archive']['literal_strings'][0]['literal'] = 'Export'; variants.append(wrong)
    wrong = copy.deepcopy(report); wrong['archive']['menu_keyed_records'][0]['fields']['NSTitle']['uid'] = 999; variants.append(wrong)
    wrong = copy.deepcopy(report); wrong['comparison'] = 'dispatch passes'; variants.append(wrong)
    for wrong in variants:
        try:
            reconcile(wrong)
        except AssertionError:
            continue
        raise AssertionError('mutation accepted')
    assert all(identity(p) == data for p, data in watch.items())
    print(json.dumps({'status': 'pass', 'archive_objects': 167, 'literal_strings': 65,
                      'menu_keyed_records': 17, 'selected_xml_records': 19, 'input_resources': 3,
                      'negative_rejection_fixtures': 3, 'files_unchanged': len(watch),
                      'Q052_resolved': False, 'behavioral_credit': 0, 'runtime': False, 'writes': False}))


if __name__ == '__main__':
    run()
