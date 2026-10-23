#!/usr/bin/env python3
"""One fixed Wavetable export-metadata census; never emit or retain C bodies."""
import collections
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SELECTION_SHA = '54bf9b113a061232532b8dfface49b451628c8b52003258c67585d235c2f9312'
CHUNK_NAMES = ('chunk-03319.jsonl', 'chunk-03320.jsonl', 'chunk-03321.jsonl')
INPUTS_SHA = '47b807f450b33ad537eba9cd0e0e8e8346f5f65c973b6011ecef9012326414d0'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pinned(path, size, digest):
    data = path.read_bytes()
    if len(data) != size or sha(data) != digest:
        raise ValueError('pin mismatch: ' + str(path))
    return data


def measure(record):
    code = record.get('code')
    if code is None:
        code = ''
    if not isinstance(code, str):
        raise ValueError('code must be string or null')
    encoded = code.encode('utf-8')
    return dict(code_utf8_bytes=len(encoded), C_lines=len(code.splitlines()),
                code_sha256=sha(encoded), code_present=bool(code))


def checks():
    assert measure({'code': 'a\nb\n'})['C_lines'] == 2
    assert measure({'code': '\u03bb\n'})['code_utf8_bytes'] == 3
    assert measure({'code': None})['code_utf8_bytes'] == 0
    assert measure({})['code_present'] is False
    assert measure({'code': ''})['C_lines'] == 0
    for code in ([], {}, 1):
        try:
            measure({'code': code})
        except ValueError:
            pass
        else:
            raise AssertionError('nontext code accepted')
    print(json.dumps(dict(status='PASS', positive_controls=5,
                          rejected_nontext_controls=3, acquisition=False)))


def main():
    selection_path = HERE / 'selection-metadata-only.json'
    selected = pinned(selection_path, 20782, SELECTION_SHA)
    selection = json.loads(selected)
    assert selection['stage'] == 'SELECTED-retained-export-metadata-only'
    assert selection['maximum_entries'] == 48
    assert selection['body_caps_proposal'] == dict(total_C_utf8_bytes=524288,
                                                   max_C_lines_each=3000)
    wanted = set(selection['entries'])
    assert len(wanted) == len(selection['entries']) == 48
    assert {s['target'] for s in selection['selected_slots']} == wanted
    assert len(selection['selected_slots']) == 48
    for pin in selection['pins']:
        pinned(Path(pin['path']), pin['bytes'], pin['sha256'])
    retained_pin = selection['pins'][1]
    retained = [json.loads(line) for line in Path(retained_pin['path']).read_text().splitlines()]
    by_id = {row['id']: row for row in retained}
    aliases = {row['record']['entry']: row for row in retained
               if row['kind'] == 'alias' and row['record']['entry'] in wanted}
    assert len(aliases) == 48
    for s in selection['selected_slots']:
        assert by_id[s['id']]['record'] == {k: v for k, v in s.items() if k != 'id'}
        assert aliases[s['target']]['record']['external'] is False
    for h in selection['selected_headers']:
        row = by_id[h['id']]['record']
        assert row['address_point'] == h['address_point']
        assert row['literal_type_encoding'] == h['literal_type_encoding']
    # These three chunk locators are already present in retained stores of the
    # selected headers. They bound this lookup, without reopening aliases.jsonl.
    headers = {h['address_point'] for h in selection['selected_headers']}
    stores = [r for r in retained if r['kind'] == 'literal-store-candidate'
              and r['record']['address_point'] in headers]
    chunk_paths = {r['record']['source_provider'] for r in stores}
    assert {Path(q).name for q in chunk_paths} == set(CHUNK_NAMES)
    inputs_path = BASE / 'component-resolution-v1/class-inputs.json'
    inputs = json.loads(pinned(inputs_path, 834035, INPUTS_SHA))
    all_pins = {q['path']: q for q in inputs['decomp_chunk_pins']}
    chunk_pins = [all_pins[q] for q in sorted(chunk_paths)]
    locator_path = BASE / 'reviews/wavetable-typed-prefix-root-locator-scope.json'
    locator_bytes = pinned(locator_path, 1521,
                           'ea290a40e5aa96dced3deb15f6f2e3d200f492960ff425f2e256b37666c5b6f9')
    locator_scope = json.loads(locator_bytes)
    assert locator_scope['base_selection_sha256'] == SELECTION_SHA
    assert locator_scope['chunk_pins'] == chunk_pins
    records = []
    found = set()
    custody_bytes = 0
    for pin in chunk_pins:
        path = Path(pin['path'])
        data = pinned(path, pin['bytes'], pin['sha256'])
        custody_bytes += len(data)
        byte = 0
        for line, raw in enumerate(data.splitlines(keepends=True), 1):
            # Inspect only a bounded entry-field prefix for unselected rows.
            match = re.search(br'"entry"\s*:\s*"([^"]+)"', raw[:100])
            entry = match[1].decode('ascii') if match else None
            if entry in wanted:
                assert entry not in found
                found.add(entry)
                record = json.loads(raw)
                assert record['entry'] == entry
                alias = aliases[entry]
                result = dict(entry=entry, alias_metadata=alias['id'],
                              alias_record=alias['record'], alias_source=alias['provider'],
                              selected_slot_ids=[s['id'] for s in selection['selected_slots']
                                                 if s['target'] == entry],
                              export_record_name=record.get('name'),
                              source_path=str(path), source_line=line, source_byte=byte,
                              raw_bytes=len(raw), raw_sha256=sha(raw), **measure(record))
                for key in ('body_bytes', 'body_ranges', 'state', 'warnings', 'error',
                            'timed_out', 'partial_code', 'thunk'):
                    result[key] = record.get(key)
                records.append(result)
            byte += len(raw)
        assert byte == len(data)
    records.sort(key=lambda row: int(row['entry'], 16))
    missing = sorted(wanted - found, key=lambda entry: int(entry, 16))
    total = sum(row['code_utf8_bytes'] for row in records)
    max_lines = max((row['C_lines'] for row in records), default=0)
    summary = dict(selected_entries=48, records_found=len(records),
                   missing_metadata_entries=missing, missing_is_absence_claim=False,
                   code_utf8_bytes=total, C_lines=sum(row['C_lines'] for row in records),
                   max_C_lines=max_lines, chunks=len(chunk_pins),
                   warning_records=sum(bool(row['warnings']) for row in records),
                   empty_code_records=sum(not row['code_present'] for row in records),
                   state_counts=dict(collections.Counter(row['state'] for row in records)),
                   within_proposed_body_caps=not missing and total <= 524288 and max_lines <= 3000)
    result = dict(schema='selected-wavetable-typed-prefix-export-metadata-census-v1',
                  utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  selection=dict(path=str(selection_path), bytes=len(selected), sha256=sha(selected)),
                  inputs_pin=dict(path=str(inputs_path), bytes=834035, sha256=INPUTS_SHA),
                  locator_scope_pin=dict(path=str(locator_path), bytes=len(locator_bytes),
                                         sha256=sha(locator_bytes)),
                  chunk_locator_basis='Only three chunk paths already named by retained stores for the exact selected eight headers; no original alias-index scan or broader chunk search.',
                  retained_store_locator_ids=[row['id'] for row in stores],
                  records=records, summary=summary, selected_chunk_pins=chunk_pins,
                  chunk_custody_bytes=custody_bytes,
                  read_scope='Whole selected chunks hashed for custody; unselected rows inspected only for bounded entry locator, never parsed as full JSON. Exactly selected C strings measured/hashed without semantic reading, printing or retention.',
                  semantic_source_reading_selected=False,
                  semantic_source_selection='Pending separate Root coherent source scope decision; proposed caps are not semantic-read authorization.',
                  forbidden_following='No original alias index, calls, indirect, callees, globals, slot destinations, provider, native, image, original, model, comparator or harness accessed or executed.',
                  new_site_grade_case_release=0, required_unsupported='U', coverage_gate='OPEN')
    output = HERE / 'candidate-census.json'
    with output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(summary))
    print(json.dumps([dict(entry=r['entry'], name=r['alias_record']['name'],
                           C_bytes=r['code_utf8_bytes'], C_lines=r['C_lines'],
                           warnings=r['warnings'], state=r['state']) for r in records], indent=2))


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        checks()
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit('usage: census.py [--check]')
