"""Read-only whole122 metadata check; no original aliases/chunks/source or reader execution."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import sys

P = Path(__file__).resolve().parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def validate(c, selection, named, parent):
    rows = c['records']
    expected = sorted([x['entry'] for x in named['entries'] if x['selected_outgoing_seed']], key=lambda x: int(x, 16))
    excluded = [x['entry'] for x in named['entries'] if not x['selected_outgoing_seed']]
    assert len(rows) == len(expected) == len(set(expected)) == 122
    assert [r['entry'] for r in rows] == selection['entries'] == expected
    assert len(named['entries']) == len(parent) == 133 and len(excluded) == 11
    assert c['excluded_UI_group']['entries'] == excluded and c['excluded_UI_group']['count'] == 11
    chunks = {x['path']: x for x in c['selected_chunk_pins']}
    assert len(chunks) == 12 and sum(x['bytes'] for x in chunks.values()) == 2412471
    ranges = collections.defaultdict(list)
    for r in rows:
        line, old = parent[r['entry']]
        assert r['parent_alias_native_data_line'] == line and r['alias_record'] == old['record']
        assert r['alias_source'] == dict(path=old['provider'], line=old['source_line'], byte=old['source_byte'], bytes=old['raw_bytes'], sha256=old['raw_sha256'])
        assert not r['alias_record']['external']
        assert r['chunk_number'] == r['nonexternal_ordinal'] // 100
        assert Path(r['source_path']).name == f"chunk-{r['chunk_number']:05}.jsonl"
        chunk = chunks[r['source_path']]
        assert r['source_line'] > 0 and r['source_byte'] >= 0 and r['raw_bytes'] > 0
        assert r['source_byte'] + r['raw_bytes'] <= chunk['bytes']
        assert len(r['raw_sha256']) == len(r['code_sha256']) == 64 and 'code' not in r
        assert r['code_present'] and r['code_utf8_bytes'] > 0 and r['C_lines'] > 0
        assert not r['partial_code'] and not r['timed_out'] and r['error'] is None
        assert sum(int(b, 16) - int(a, 16) + 1 for a, b in r['body_ranges']) == r['body_bytes'] > 0
        assert r['state'] == ('exported-with-warnings' if r['warnings'] else 'exported')
        ranges[r['source_path']].append((r['source_byte'], r['source_byte'] + r['raw_bytes']))
    for rr in ranges.values():
        rr.sort()
        assert all(a[1] <= b[0] for a, b in zip(rr, rr[1:]))
    s = c['summary']
    assert s == dict(selected_entries=122, original_aliases_found=122, export_records_found=122, missing_alias_entries=[], missing_export_entries=[], missing_is_absence_claim=False,
        code_utf8_bytes=360530, C_lines=9041, max_C_lines=609, chunks=12, chunk_custody_bytes=2412471,
        warning_records=20, warning_occurrences=31, thunk_records=0, four_byte_extent_records=47,
        partial_records=0, error_records=0, timed_out_records=0, empty_code_records=0,
        state_counts={'exported': 102, 'exported-with-warnings': 20}, within_proposed_whole_source_caps=True)
    assert sum(r['code_utf8_bytes'] for r in rows) == 360530 and sum(r['C_lines'] for r in rows) == 9041
    assert max(r['C_lines'] for r in rows) == 609
    assert sum(bool(r['warnings']) for r in rows) == 20 and sum(len(r['warnings']) for r in rows) == 31
    assert sum(r['thunk'] for r in rows) == 0 and sum(r['body_bytes'] == 4 for r in rows) == 47
    assert c['source_caps_proposal'] == selection['proposed_source_caps'] == dict(records=122, C_bytes=2097152, C_lines=50000)
    assert c['source_semantics_selected'] is c['source_retention_selected'] is False
    assert c['new_callee_global_slot_native_image_provider_original_model_harness_follow'] == c['new_site_grade_case_release'] == 0
    assert c['required_unsupported'] == 'U' and c['coverage_gate'] == 'OPEN'
    assert c['alias_pass'] == dict(path='/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl', bytes=122340555, lines=420470,
        sha256='6f05d75085ffb5f74826b4d44f3708fe89466b0b14581e538d912944f8167fcb', nonexternal_rows=418417, passes=1, stat_endpoints_equal=True)


def main():
    assert sys.argv[1:] == ['--check']
    raw = (P / 'candidate-census.json').read_bytes()
    c = json.loads(raw)
    sr = (P / 'selection-metadata-only.json').read_bytes()
    assert (len(sr), sha(sr)) == (5048, 'b5b67aa71d5ddd970c2fffc5d55b81a61726486c818891d74ba3e5148a1d4e2c')
    selection = json.loads(sr)
    parent_payloads = {}
    for key in ['parent_metadata', 'parent_seeds']:
        q = selection[key]
        b = Path(q['path']).read_bytes()
        assert len(b) == q['bytes'] and sha(b) == q['sha256']
        parent_payloads[key] = b
    parent = {r['record']['entry']: (i, r) for i, r in enumerate(map(json.loads, parent_payloads['parent_metadata'].splitlines()), 1) if r['kind'] == 'alias-data'}
    named = json.loads(parent_payloads['parent_seeds'])
    validate(c, selection, named, parent)
    negatives = []
    def reject(name, fn):
        bad = copy.deepcopy(c)
        fn(bad)
        try:
            validate(bad, selection, named, parent)
        except (AssertionError, ValueError, KeyError, IndexError, TypeError):
            negatives.append(dict(name=name, rejected=True))
            return
        raise AssertionError(name)
    warned = next(i for i, r in enumerate(c['records']) if r['warnings'])
    four = next(i for i, r in enumerate(c['records']) if r['body_bytes'] == 4)
    reject('drop-selected122', lambda q: q['records'].pop())
    reject('duplicate-selected122', lambda q: q['records'].__setitem__(1, q['records'][0]))
    reject('follow-excluded-UI', lambda q: q['records'][0].update(entry=excluded_entry(named)))
    reject('change-retained-alias', lambda q: q['records'][0]['alias_record'].update(name='other'))
    reject('wrong-parent-alias-line', lambda q: q['records'][0].update(parent_alias_native_data_line=1))
    reject('change-original-alias-byte', lambda q: q['records'][0]['alias_source'].update(byte=0))
    reject('wrong-nonexternal-ordinal', lambda q: q['records'][0].update(chunk_number=0))
    reject('negative-source-offset', lambda q: q['records'][0].update(source_byte=-1))
    reject('source-range-beyond-chunk', lambda q: q['records'][0].update(raw_bytes=9999999))
    reject('retain-original-C', lambda q: q['records'][0].update(code='void f(){}'))
    reject('alter-C-byte-size', lambda q: q['records'][0].update(code_utf8_bytes=0))
    reject('erase-warning', lambda q: q['records'][warned].update(warnings=[]))
    reject('repair-four-byte-extent', lambda q: q['records'][four].update(body_bytes=4096))
    reject('repair-thunk-flag', lambda q: q['records'][four].update(thunk=True))
    reject('drop-chunk-custody-pin', lambda q: q['selected_chunk_pins'].pop())
    reject('promote-source-semantics', lambda q: q.update(source_semantics_selected=True))
    reject('promote-source-retention', lambda q: q.update(source_retention_selected=True))
    reject('follow-callee', lambda q: q.update(new_callee_global_slot_native_image_provider_original_model_harness_follow=1))
    reject('missing-means-absence', lambda q: q['summary'].update(missing_is_absence_claim=True))
    reject('second-alias-pass', lambda q: q['alias_pass'].update(passes=2))
    reject('invent-grade-site', lambda q: q.update(new_site_grade_case_release=122))
    reject('close-coverage', lambda q: q.update(coverage_gate='CLOSED'))
    print(json.dumps(dict(status='PASS', metadata_records=122, C_utf8_bytes=360530, C_lines=9041, max_C_lines=609,
        warning_records=20, warning_occurrences=31, thunk_records=0, four_byte_extents=47, source_chunks=12,
        original_alias_passes_inherited=1, original_alias_chunk_source_native_image_provider_reads_by_checker=0,
        source_semantic_reads=0, source_retention=0, negative_count=len(negatives), negative_controls=negatives,
        coverage_gate='OPEN', required_unsupported='U', source_approval='Separate Root whole122 source decision required'), indent=2))


def excluded_entry(named):
    return next(x['entry'] for x in named['entries'] if not x['selected_outgoing_seed'])


if __name__ == '__main__':
    main()
