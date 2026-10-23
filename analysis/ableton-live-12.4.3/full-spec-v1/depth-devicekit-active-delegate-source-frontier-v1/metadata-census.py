"""Fixed seven-delegate metadata census; selected C is measured, never printed or retained."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import re
import sys

P = Path(__file__).resolve().parent
B = P.parent
ROOT_SELECTION = B / 'reviews/devicekit-active-delegates-root-metadata-selection.json'
SELECTION_SHA = '51a5c9416abbeaa09228a9d60fc8a3045bc7c1b31d1185a92e47ed0172acbd44'
COMPONENT_SHA = '392a738005f7d776dca96d7c78220cb94091081ef7086ec45b9397afccbe438b'
INPUTS_SHA = '47b807f450b33ad537eba9cd0e0e8e8346f5f65c973b6011ecef9012326414d0'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=sha(raw))


def save(name, value):
    with (P / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def entry_prefix(raw):
    match = re.search(br'"entry"\s*:\s*"([^"]+)"', raw[:100])
    return match[1].decode() if match else None


def measure(raw, entry):
    record = json.loads(raw)
    assert record['entry'] == entry
    code = (record.get('code') or '').encode()
    ranges = record['body_ranges']
    assert sum(int(hi, 16) - int(lo, 16) + 1 for lo, hi in ranges) == record['body_bytes']
    assert isinstance(record['warnings'], list)
    return dict(code_utf8_bytes=len(code), C_lines=len(code.decode().splitlines()),
                code_sha256=sha(code), native_body_bytes=record['body_bytes'],
                native_body_ranges=ranges, state=record['state'], warnings=record['warnings'],
                error=record['error'], timed_out=record['timed_out'],
                partial_code=record['partial_code'], record_thunk=record['thunk'])


def census():
    selection_raw = ROOT_SELECTION.read_bytes()
    assert len(selection_raw) == 4940 and sha(selection_raw) == SELECTION_SHA
    assert (P / 'selection-metadata-only.json').read_bytes() == selection_raw
    selection = json.loads(selection_raw)
    wanted = selection['entries']
    assert len(wanted) == len(set(wanted)) == len(selection['selected']) == 7
    assert wanted == [x['target_entry'] for x in selection['selected']]
    assert not (P / 'candidate-census.json').exists()
    parent = B / 'depth-devicekit-defined-method-source-frontier-v1'
    parent_manifest_raw = (parent / 'manifest.json').read_bytes()
    assert sha(parent_manifest_raw) == selection['parent_manifest_sha256']
    assert sha((B / 'reviews/devicekit-defined-method-source-v1-review.json').read_bytes()) == selection['parent_review_sha256']
    parent_raw = (parent / 'sources.jsonl').read_bytes()
    parent_source_pin = next(x for x in json.loads(parent_manifest_raw)['files'] if x['path'] == 'sources.jsonl')
    assert len(parent_raw) == parent_source_pin['bytes'] and sha(parent_raw) == parent_source_pin['sha256']
    parent_records = {r['entry']: r for r in map(json.loads, parent_raw.splitlines())}
    for row in selection['selected']:
        lo, hi = row['source_C_lines']
        code_lines = parent_records[row['parent_entry']]['code'].splitlines()
        assert lo == hi and code_lines[lo - 1] == row['quote']
        assert sha(row['quote'].encode()) == row['quote_sha256']
    component = B / 'component-resolution-v1'
    component_raw = (component / 'manifest.json').read_bytes()
    assert sha(component_raw) == COMPONENT_SHA
    input_pin = next(x for x in json.loads(component_raw)['files'] if x['path'] == 'class-inputs.json')
    input_raw = (component / 'class-inputs.json').read_bytes()
    assert len(input_raw) == input_pin['bytes'] == 834035
    assert sha(input_raw) == input_pin['sha256'] == INPUTS_SHA
    chunk_authorities = {x['path']: x for x in json.loads(input_raw)['decomp_chunk_pins']}
    alias_pin = selection['alias_provider']
    aliases = Path(alias_pin['path'])
    before = aliases.stat()
    digest = hashlib.sha256()
    offset = ordinal = 0
    matches = {}
    with aliases.open('rb') as stream:
        for line, raw in enumerate(stream, 1):
            digest.update(raw)
            record = json.loads(raw)
            if record['entry'] in wanted:
                assert record['entry'] not in matches, 'ambiguous selected alias'
                matches[record['entry']] = dict(alias=record,
                    alias_source=dict(path=str(aliases), line=line, byte=offset,
                                      bytes=len(raw), sha256=sha(raw)),
                    chunk_number=None if record['external'] else ordinal // 100)
            if not record['external']:
                ordinal += 1
            offset += len(raw)
    after = aliases.stat()
    assert (before.st_size, before.st_mtime_ns, before.st_ino) == (after.st_size, after.st_mtime_ns, after.st_ino)
    assert offset == alias_pin['bytes'] == 122340555 and digest.hexdigest() == alias_pin['sha256']
    groups = collections.defaultdict(set)
    gaps = [dict(entry=e, reason='selected alias locator not found; no absence inference')
            for e in wanted if e not in matches]
    for entry, found in matches.items():
        if found['chunk_number'] is None:
            gaps.append(dict(entry=entry, reason='selected alias external; no export locator assumed'))
        else:
            groups[found['chunk_number']].add(entry)
    records, chunk_pins = [], []
    for number, entries in sorted(groups.items()):
        path = Path('/var/tmp/sound-analysis/corpus/decomp/chunks') / f'chunk-{number:05}.jsonl'
        if str(path) not in chunk_authorities:
            gaps += [dict(entry=e, reason='corresponding chunk pin locator gap; no absence inference') for e in sorted(entries)]
            continue
        fixed = chunk_authorities[str(path)]
        try:
            before = path.stat()
        except FileNotFoundError:
            gaps += [dict(entry=e, reason='pinned corresponding chunk currently unavailable; no absence inference') for e in sorted(entries)]
            continue
        digest = hashlib.sha256()
        offset = 0
        found_entries = set()
        with path.open('rb') as stream:
            for line, raw in enumerate(stream, 1):
                digest.update(raw)
                entry = entry_prefix(raw)
                if entry in entries:
                    assert entry not in found_entries, 'ambiguous selected export'
                    found = matches[entry]
                    measured = measure(raw, entry)
                    records.append(dict(entry=entry, alias_name=found['alias']['name'],
                        alias_thunk=found['alias']['thunk'],
                        alias_thunk_target=found['alias'].get('thunk_target'),
                        alias_source=found['alias_source'], source_path=str(path),
                        source_line=line, source_byte=offset, raw_bytes=len(raw),
                        raw_sha256=sha(raw), **measured))
                    found_entries.add(entry)
                offset += len(raw)
        after = path.stat()
        assert (before.st_size, before.st_mtime_ns, before.st_ino) == (after.st_size, after.st_mtime_ns, after.st_ino)
        assert offset == fixed['bytes'] and digest.hexdigest() == fixed['sha256']
        chunk_pins.append(fixed)
        gaps += [dict(entry=e, reason='selected export locator gap in its pinned corresponding chunk; no absence inference')
                 for e in sorted(entries - found_entries)]
    records.sort(key=lambda x: wanted.index(x['entry']))
    size = sum(x['code_utf8_bytes'] for x in records)
    max_lines = max((x['C_lines'] for x in records), default=0)
    caps = selection['body_caps_proposal']
    summary = dict(selected_values=7, alias_matches=len(matches), records_found=len(records),
                   missing_values=[e for e in wanted if e not in {r['entry'] for r in records}],
                   code_utf8_bytes=size, C_lines=sum(x['C_lines'] for x in records),
                   max_C_lines=max_lines, chunks=len(chunk_pins),
                   warning_records=sum(bool(x['warnings']) for x in records),
                   within_proposed_source_caps=len(records) == 7 and size <= caps['total_C_utf8_bytes'] and max_lines <= caps['max_C_lines_each'])
    result = dict(schema='fixed-seven-active-delegate-metadata-census-v1',
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), selection=pin(ROOT_SELECTION),
        parent_manifest_sha256=selection['parent_manifest_sha256'],
        parent_review_sha256=selection['parent_review_sha256'], records=records, summary=summary,
        locator_gaps=gaps, selected_chunk_pins=chunk_pins,
        metadata_scan=dict(alias_passes=1, alias_bytes=alias_pin['bytes'],
                           alias_sha256=alias_pin['sha256'], nonexternal_ordinal=ordinal,
                           alias_stat_unchanged=True, chunk_stat_unchanged=True,
                           unselected_C_records_parsed=0),
        chunk_pin_authority=dict(path=str(component / 'class-inputs.json'),
                                 bytes=len(input_raw), sha256=sha(input_raw)),
        read_scope='Exact7 retained aliases plus corresponding pinned export metadata only. Selected C strings measured/hashed transiently, never printed/retained/semantically read. Relevant whole chunk hashes custody only. Parent reviewed anchors are existing source, not newly selected target semantics.',
        semantic_source_selection='PENDING separate Root census/size/scope decision',
        new_body_native_provider_original_model_harness_calls_or_site_grade=0,
        required_unsupported='U;coverageOPEN')
    save('candidate-census.json', result)
    print(json.dumps(summary))
    print(json.dumps([dict(entry=x['entry'], name=x['alias_name'], C_bytes=x['code_utf8_bytes'],
                           C_lines=x['C_lines'], native_body_bytes=x['native_body_bytes'],
                           warnings=x['warnings']) for x in records], indent=2))


def check():
    record = dict(entry='0x1', code='\nvoid f() {}\n', body_ranges=[['0x1', '0x4']],
                  body_bytes=4, state='synthetic', warnings=[], error=None,
                  timed_out=False, partial_code=False, thunk=False)
    raw = json.dumps(record).encode()
    assert entry_prefix(raw) == '0x1'
    assert entry_prefix(b'{"other":1}') is None
    assert measure(raw, '0x1')['C_lines'] == 2
    assert measure(raw, '0x1')['code_utf8_bytes'] == len(record['code'].encode())
    assert measure(raw, '0x1')['code_sha256'] == sha(record['code'].encode())
    negatives = []
    def reject(name, candidate, entry='0x1'):
        try:
            measure(json.dumps(candidate).encode(), entry)
        except (AssertionError, KeyError, TypeError, ValueError):
            negatives.append(name)
            return
        raise AssertionError('negative accepted: ' + name)
    reject('wrong-selected-entry', record, '0x2')
    reject('wrong-native-extent-metadata', dict(record, body_bytes=8))
    reject('malformed-warning-field', dict(record, warnings='warning'))
    reject('missing-source-state', {k: v for k, v in record.items() if k != 'state'})
    reject('missing-thunk-metadata', {k: v for k, v in record.items() if k != 'thunk'})
    save('script-check.json', dict(status='PASS-synthetic-metadata-only', positive_assertions=5,
        negatives=negatives, negative_count=len(negatives),
        aliases_chunks_target_C_original_native_provider_reads=0))
    print(json.dumps(dict(status='PASS-synthetic-metadata-only', negatives=negatives)))


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        check()
    elif sys.argv[1:] == ['--census']:
        census()
    else:
        raise SystemExit('Only fixed --check or --census is supported; no reads performed.')

