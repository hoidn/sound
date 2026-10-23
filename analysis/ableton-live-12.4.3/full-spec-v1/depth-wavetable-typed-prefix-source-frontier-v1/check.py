#!/usr/bin/env python3
"""Retained-data-only checks; no acquisition or external execution path."""
import collections
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXED = {
    'selection-metadata-only.json': (20782, '54bf9b113a061232532b8dfface49b451628c8b52003258c67585d235c2f9312'),
    'candidate-census.json': (79348, '6c7964af415066f9cee129a1bd4eea95d3fcf6db57904ab51251cf7d207d055f'),
    'selection-source-read.json': (2421, 'd2961dd9fe36ca26f28bb25d96fd5b5f09494710682576ef3de939b50b9dd5d1'),
    'selected-records.jsonl': (324282, 'bf1a1a7f80f9a08ebd3d871b6f34282220ad74e17f413715000c6c7b5d6c5c9d'),
    'source-retention-receipt.json': (16676, '5dab6217d3f03a48e3293a195b3c0a9d25e428ce7ae88608f903fe0f5623d630'),
}
ROLES = ('exported-return-only', 'warned-delete-wrapper', 'input-value-state-update',
         'phase/update-wrapper-with-open-dependencies', 'mode-and-array-setup',
         'increment-state-update')


def sha(value):
    return hashlib.sha256(value).hexdigest()


def need(value, message):
    if not value:
        raise ValueError(message)


def validate(data):
    selection, census, source_selection, receipt, rows, assessment, readmap = (
        data[k] for k in ('selection', 'census', 'source_selection', 'receipt',
                         'rows', 'assessment', 'readmap'))
    expected = source_selection['entries']
    need(len(expected) == len(set(expected)) == 48, 'fixed48 source selection')
    need(expected == selection['entries'] == [r['entry'] for r in census['records']],
         'selection/census entry order')
    need([r['entry'] for r in rows] == expected, 'exact whole48 source rows')
    need(len(selection['selected_headers']) == 8, 'eight typed headers')
    slots = {r['target']: r for r in selection['selected_slots']}
    headers = {r['address_point']: r for r in selection['selected_headers']}
    need(len(slots) == 48 and set(slots) == set(expected), '48 distinct selected slots')
    for address in headers:
        need(sorted(s['slot_index'] for s in slots.values() if s['address_point'] == address)
             == list(range(6)), 'six slots per exact typed prefix')
    code_bytes = line_count = warnings = raw_byte = anchor_count = 0
    need(receipt['raw_range_reads'] == 48 and len(receipt['records']) == 48,
         'exact48 raw retention receipt')
    need(len(assessment['records']) == len(readmap['entries']) == 48, 'whole48 assessment/read map')
    for i, (row, meta, item, read) in enumerate(zip(rows, census['records'],
                                                  assessment['records'], readmap['entries'])):
        entry = expected[i]
        code = row['code']
        encoded = code.encode('utf-8')
        lines = code.splitlines(keepends=True)
        slot = slots[entry]
        header = headers[slot['address_point']]
        need(sha(encoded) == meta['code_sha256'] == item['code_sha256'], 'whole C hash')
        need(len(encoded) == meta['code_utf8_bytes'], 'C byte size')
        need(len(lines) == meta['C_lines'] == item['C_lines'] <= 830, 'C line count')
        need(row['warnings'] == meta['warnings'] == item['warnings'], 'all warning text preserved')
        for key in ('body_bytes', 'body_ranges', 'state', 'error', 'timed_out', 'partial_code', 'thunk'):
            need(row.get(key) == meta[key], 'export metadata preserved: ' + key)
        need(row['error'] is None and row['timed_out'] is False and row['partial_code'] is False,
             'selected exporter status')
        rec = receipt['records'][i]
        need(rec['entry'] == entry and rec['retained_byte'] == raw_byte,
             'retained raw row geometry')
        need(rec['raw_bytes'] == meta['raw_bytes'] and rec['raw_sha256'] == meta['raw_sha256'],
             'source raw range identity')
        need((rec['original_path'], rec['original_byte'], rec['original_line']) ==
             (meta['source_path'], meta['source_byte'], meta['source_line']), 'original range locator')
        raw_byte += rec['raw_bytes']
        need(item['entry'] == entry and item['source_record'] == i + 1, 'assessment row identity')
        need((item['selected_slot_id'], item['header_id'], item['address_point'], item['slot_index'],
              item['literal_type_encoding']) ==
             (slot['id'], header['id'], slot['address_point'], slot['slot_index'],
              header['literal_type_encoding']), 'slot/header/full type association')
        need(item['role'] == ROLES[slot['slot_index']], 'source-operation role, no constructor promotion')
        for flag in ('complete_callable_X_leaf', 'complete_callable_math_leaf',
                     'actual_receiver_or_ABI_proved', 'public_route'):
            need(item[flag] is False, 'no unproved execution/public credit: ' + flag)
        need(item['legal_inputs'] is None and item['expected_result'] is None, 'no invented vector/oracle')
        need(len(item['missing_frontiers']) >= 5, 'explicit legal setup/output gaps')
        need(item['native_extent_status'] == 'inherited export metadata only; no native bytes or instruction verification',
             'native metadata qualification')
        need(bool(item['anchors']), 'each full record assessed with source anchors')
        for anchor in item['anchors']:
            need(anchor['entry'] == entry, 'anchor entry association')
            a, b = anchor['C_lines']
            need(1 <= a <= b <= len(lines), 'anchor line bounds')
            text = ''.join(lines[a-1:b])
            need((anchor['character_start'], anchor['character_end']) ==
                 (sum(map(len, lines[:a-1])), sum(map(len, lines[:b]))), 'anchor character geometry')
            need(anchor['quote'] == text.rstrip('\n') and anchor['sha256'] == sha(text.encode()),
                 'exact anchor quote/hash')
            anchor_count += 1
        need(read['entry'] == entry and read['whole_C_lines'] == [1, len(lines)], 'whole-body read scope')
        if i < 16:
            need(read['method'] == 'direct complete numbered C body' and
                 read['code_sha256'] == sha(encoded), 'direct full source read identity')
        else:
            j = expected.index(read['base_entry'])
            need(j < i, 'lossless base was read earlier')
            base = rows[j]['code'].splitlines(keepends=True)
            rebuilt = []
            source_cursor = target_cursor = 0
            for op, a, b, c, d in read['opcodes']:
                need(op in ('equal', 'replace', 'delete', 'insert'), 'valid lossless opcode')
                need(a == source_cursor and c == target_cursor and
                     a <= b <= len(base) and c <= d <= len(lines), 'complete lossless cursor coverage')
                if op == 'equal':
                    need(base[a:b] == lines[c:d], 'exact unchanged source spans; no normalization')
                    rebuilt.extend(base[a:b])
                else:
                    rebuilt.extend(lines[c:d])
                source_cursor, target_cursor = b, d
            need(source_cursor == len(base) and target_cursor == len(lines), 'whole lossless reconstruction extent')
            need(''.join(rebuilt) == code and sha(''.join(rebuilt).encode()) == read['reconstruction_sha256'],
                 'full reconstructed source hash')
        code_bytes += len(encoded)
        line_count += len(lines)
        warnings += bool(row['warnings'])
    need((code_bytes, line_count, warnings, raw_byte, anchor_count) ==
         (296613, 8116, 18, 324282, 116), 'exact whole-set quantities')
    need(receipt['raw_content_bytes'] == raw_byte and receipt['expansion'] is False,
         'no source acquisition expansion')
    need(readmap['complete_records'] == 48 and readmap['code_utf8_bytes'] == code_bytes and
         readmap['C_lines'] == line_count and readmap['warning_records'] == warnings and
         readmap['source_expansion'] is False, 'honest whole read summary')
    need(readmap['direct_truncation_repair'] == dict(entry='0x10404b560', C_lines=[250, 710]),
         'retained truncation repair receipt')
    need(len(assessment['whole_set_claims']) == 8, 'whole-set claim coverage')
    for index, claim in enumerate(assessment['whole_set_claims']):
        need(claim['id'] == f'WTC{index+1:02}', 'claim identity')
        if index < 6:
            need(claim['entries'] == [e for e in expected if slots[e]['slot_index'] == index],
                 'each full eight-member source-role claim')
        elif index == 6:
            need(claim['entries'] == ['0x10404b560', '0x10404bed0', '0x104050d2c', '0x10405169c'],
                 'four exact FM nonreturn limitations')
        else:
            need(claim['entries'] == expected, 'whole48 conservative claim')
    need(len(assessment['frontiers']) == 8 and
         {f['id'] for f in assessment['frontiers']} == {f'WT{i:02}' for i in range(1, 9)},
         'all eight open dependency frontiers')
    need(all(f['status'] == 'OPEN' and f['missing'] for f in assessment['frontiers']),
         'no unproved dependency closure')
    summary = assessment['summary']
    need(summary == dict(records=48, typed_prefixes=8, slots_each=6, code_utf8_bytes=296613,
        C_lines=8116, max_C_lines_each=830, warning_records=18, role_counts={r:8 for r in ROLES},
        complete_callable_X_leaves=0, complete_callable_math_leaves=0, public_routes=0,
        new_grade_site_case_release=0), 'no aggregate/grade promotion')
    need(assessment['scope_boundary'] == dict(callee_global_native_image_provider_original_follow=False,
        legal_X_vectors=None, semantic_source_expansion=False, successor_selected=False,
        required_unsupported='U', coverage_gate='OPEN'), 'fixed bounded U/OPEN scope')
    need(assessment['upstream_inventory_unchanged'] == dict(requirements=110, cases=190,
        predicates=585, X=0, S=0, no_established_route=585, required_unsupported='U',
        coverage_gate='OPEN'), 'upstream inventory unchanged and unsupported OPEN')


def main():
    payloads = {name: (HERE / name).read_bytes() for name in FIXED}
    for name, (size, digest) in FIXED.items():
        need(len(payloads[name]) == size and sha(payloads[name]) == digest, 'fixed retained pin: ' + name)
    raw_rows = payloads['selected-records.jsonl'].splitlines(keepends=True)
    census = json.loads(payloads['candidate-census.json'])
    need(len(raw_rows) == 48, 'exact retained raw row count')
    for raw, meta in zip(raw_rows, census['records']):
        need(len(raw) == meta['raw_bytes'] and sha(raw) == meta['raw_sha256'], 'exact raw row SHA')
    data = dict(selection=json.loads(payloads['selection-metadata-only.json']), census=census,
        source_selection=json.loads(payloads['selection-source-read.json']),
        receipt=json.loads(payloads['source-retention-receipt.json']),
        rows=[json.loads(raw) for raw in raw_rows],
        assessment=json.loads((HERE / 'source-assessment.json').read_text()),
        readmap=json.loads((HERE / 'source-read-map.json').read_text()))
    validate(data)
    controls = [
        ('drop-selected-source', lambda d: d['rows'].pop()),
        ('duplicate-selected-source', lambda d: d['rows'].__setitem__(1, d['rows'][0])),
        ('alter-C-body', lambda d: d['rows'][0].update(code='void forged(void) {}')),
        ('erase-wrapper-warning', lambda d: d['rows'][1].update(warnings=[])),
        ('repair-native-extent', lambda d: d['rows'][1].update(body_bytes=8)),
        ('repair-nonreturn-metadata', lambda d: d['rows'][21].update(warnings=[])),
        ('wrong-retained-range', lambda d: d['receipt']['records'][0].update(retained_byte=1)),
        ('wrong-original-locator', lambda d: d['receipt']['records'][0].update(original_byte=0)),
        ('drop-typed-specialization', lambda d: d['selection']['selected_headers'].pop()),
        ('collapse-full-type', lambda d: d['assessment']['records'][0].update(literal_type_encoding='Wavetable')),
        ('wrong-slot-binding', lambda d: d['assessment']['records'][0].update(slot_index=3)),
        ('infer-constructor-role', lambda d: d['assessment']['records'][4].update(role='constructor')),
        ('promote-callable-X', lambda d: d['assessment']['records'][0].update(complete_callable_X_leaf=True)),
        ('promote-math-leaf', lambda d: d['assessment']['records'][2].update(complete_callable_math_leaf=True)),
        ('invent-public-route', lambda d: d['assessment']['records'][3].update(public_route=True)),
        ('invent-native-ABI', lambda d: d['assessment']['records'][1].update(actual_receiver_or_ABI_proved=True)),
        ('invent-legal-vector', lambda d: d['assessment']['records'][5].update(legal_inputs=[1.0])),
        ('invent-expected-output', lambda d: d['assessment']['records'][5].update(expected_result=1.0)),
        ('promote-native-metadata', lambda d: d['assessment']['records'][0].update(native_extent_status='native verified')),
        ('alter-anchor-text', lambda d: d['assessment']['records'][0]['anchors'][0].update(quote='different')),
        ('alter-anchor-span', lambda d: d['assessment']['records'][0]['anchors'][0].update(character_start=0)),
        ('alter-anchor-hash', lambda d: d['assessment']['records'][0]['anchors'][0].update(sha256='0'*64)),
        ('drop-lossless-opcode', lambda d: d['readmap']['entries'][16]['opcodes'].pop()),
        ('future-lossless-base', lambda d: d['readmap']['entries'][16].update(base_entry=d['rows'][17]['entry'])),
        ('wrong-lossless-hash', lambda d: d['readmap']['entries'][16].update(reconstruction_sha256='0'*64)),
        ('processing-only-subset', lambda d: d['assessment']['whole_set_claims'][0]['entries'].pop()),
        ('close-helper-frontier', lambda d: d['assessment']['frontiers'][3].update(status='closed')),
        ('follow-global', lambda d: d['assessment']['scope_boundary'].update(callee_global_native_image_provider_original_follow=True)),
        ('select-successor', lambda d: d['assessment']['scope_boundary'].update(successor_selected=True)),
        ('close-coverage', lambda d: d['assessment']['scope_boundary'].update(coverage_gate='CLOSED')),
        ('promote-upstream-grade', lambda d: d['assessment']['upstream_inventory_unchanged'].update(X=1)),
    ]
    results = []
    for name, mutate in controls:
        corrupted = copy.deepcopy(data)
        mutate(corrupted)
        try:
            validate(corrupted)
        except (ValueError, KeyError, IndexError, TypeError):
            results.append(dict(name=name, rejected=True))
        else:
            raise ValueError('negative control accepted: ' + name)
    print(json.dumps(dict(status='PASS', retained_source_records=48, C_utf8_bytes=296613,
        C_lines=8116, warning_records=18, source_anchors=116, typed_prefixes=8,
        full_set_claims=8, open_frontiers=8, negative_count=len(results),
        negative_controls=results, external_source_or_binary_reads=0,
        acquisition_children=0, original_decoder_provider_model_harness_runs=0,
        new_grade_site_case_release=0, required_unsupported='U', coverage_gate='OPEN',
        limitations='Retained-data integrity and corruption checks; no semantic oracle or new source/native/runtime acquisition.'), indent=2))


if __name__ == '__main__':
    main()
