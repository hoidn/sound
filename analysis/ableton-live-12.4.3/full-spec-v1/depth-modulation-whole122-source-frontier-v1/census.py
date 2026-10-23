"""Whole122 metadata-only reader; original C is transiently measured, never retained/printed.

Adapted as inert source from the reviewed fixed67 reader; no historical module
is imported or executed. --check uses synthetic data only, --census one attempt.
"""
from pathlib import Path
import collections
import copy
import datetime
import hashlib
import json
import os
import re
import sys

P = Path(__file__).resolve().parent
B = P.parent
SELECTION = B / 'reviews/modulation-whole122-root-metadata-selection.json'
SELECTION_PIN = (5048, 'b5b67aa71d5ddd970c2fffc5d55b81a61726486c818891d74ba3e5148a1d4e2c')
ALIASES = Path('/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl')
ALIAS_PIN = (122340555, '6f05d75085ffb5f74826b4d44f3708fe89466b0b14581e538d912944f8167fcb')
INPUTS = B / 'component-resolution-v1/class-inputs.json'
INPUTS_PIN = (834035, '47b807f450b33ad537eba9cd0e0e8e8346f5f65c973b6011ecef9012326414d0')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def need(value, why):
    if not value:
        raise ValueError(why)


def checked(path, expected):
    b = path.read_bytes()
    need((len(b), sha(b)) == expected, 'pin mismatch: ' + str(path))
    return b


def pin(path, b):
    return dict(path=str(path), bytes=len(b), sha256=sha(b))


def selection_guard(selection, named):
    rows = named['entries']
    need(len(rows) == len({r['entry'] for r in rows}) == 133, 'all133 retained named entries')
    chosen = sorted([r['entry'] for r in rows if r['selected_outgoing_seed'] is True], key=lambda x: int(x, 16))
    excluded = sorted([r['entry'] for r in rows if r['selected_outgoing_seed'] is False], key=lambda x: int(x, 16))
    need(len(chosen) == 122 and len(excluded) == 11, 'complete122 selected and11excluded')
    need(excluded == named['policy']['omitted_entries'], 'entire explicit UI method group preserved')
    need(selection['entries'] == chosen, 'exact complete122 scope/order; no firstN')
    need(selection['proposed_source_caps'] == dict(records=122, C_bytes=2097152, C_lines=50000), 'whole source proposal caps')
    need('metadata-only' in selection['decision'], 'metadata-only authority')
    need(any('source retention/semantics pending separate Root' in x for x in selection['not_selected']), 'no source retention/semantics authority')


def measure(record):
    value = record.get('code')
    if value is None:
        value = ''
    need(isinstance(value, str), 'C must be text or null')
    b = value.encode('utf-8')
    return dict(code_utf8_bytes=len(b), C_lines=len(value.splitlines()), code_sha256=sha(b), code_present=bool(value))


def selfcheck():
    positives = 0
    for value, size, lines, present in [('a\nb\n', 4, 2, True), ('\u03bb\n', 3, 1, True), ('', 0, 0, False), (None, 0, 0, False)]:
        r = measure(dict(code=value))
        need((r['code_utf8_bytes'], r['C_lines'], r['code_present']) == (size, lines, present), 'measure positive')
        positives += 1
    named = dict(entries=[dict(entry=hex(i), selected_outgoing_seed=i < 122) for i in range(133)], policy=dict(omitted_entries=[hex(i) for i in range(122, 133)]))
    selection = dict(entries=[hex(i) for i in range(122)], proposed_source_caps=dict(records=122, C_bytes=2097152, C_lines=50000), decision='metadata-only', not_selected=['source retention/semantics pending separate Root'])
    selection_guard(selection, named)
    positives += 1
    negatives = []
    for value in [[], {}, 1, False, b'body']:
        try:
            measure(dict(code=value))
        except ValueError:
            negatives.append(dict(name='reject-nontext-' + type(value).__name__, rejected=True))
        else:
            raise AssertionError('nontext accepted')
    cases = [
        ('drop-seed', lambda s, n: s['entries'].pop()),
        ('duplicate-seed', lambda s, n: s['entries'].__setitem__(1, s['entries'][0])),
        ('include-excluded-UI', lambda s, n: s['entries'].__setitem__(0, '0x7a')),
        ('arbitrary-other-entry', lambda s, n: s['entries'].__setitem__(0, '0xffff')),
        ('reverse-complete-order', lambda s, n: s['entries'].reverse()),
        ('erase-retained133-alias', lambda s, n: n['entries'].pop()),
        ('silently-follow-UI-entry', lambda s, n: n['entries'][-1].update(selected_outgoing_seed=True)),
        ('erase-UI-exclusion', lambda s, n: n['policy']['omitted_entries'].pop()),
        ('widen-source-cap', lambda s, n: s['proposed_source_caps'].update(C_bytes=4194304)),
        ('semantic-read-promotion', lambda s, n: s.update(not_selected=[])),
        ('erase-metadata-authority', lambda s, n: s.update(decision='source semantics'))]
    for name, change in cases:
        s, n = copy.deepcopy((selection, named))
        change(s, n)
        try:
            selection_guard(s, n)
        except ValueError:
            negatives.append(dict(name=name, rejected=True))
        else:
            raise AssertionError(name)
    print(json.dumps(dict(status='PASS', positive_controls=positives, negative_count=len(negatives), negative_controls=negatives, original_alias_chunk_native_image_provider_reads=0, original_model_harness_runs=0), indent=2))


def main():
    os.umask(0o077)
    need(not (P / 'candidate-census.json').exists() and not (P / 'selection-metadata-only.json').exists(), 'exclusive outputs')
    with (P / 'metadata-attempt.json').open('x') as f:
        json.dump(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), pid=os.getpid(), one_attempt=True, source_semantics_selected=False), f)
        f.write('\n')
    raw_selection = checked(SELECTION, SELECTION_PIN)
    selection = json.loads(raw_selection)
    pre, predecessors = {}, []
    for key in ['parent_manifest', 'parent_scope', 'parent_review', 'parent_seeds', 'parent_metadata']:
        q = selection[key]
        path = Path(q['path'])
        b = checked(path, (q['bytes'], q['sha256']))
        pre[key] = [json.loads(x) for x in b.splitlines()] if key == 'parent_metadata' else json.loads(b)
        predecessors.append(pin(path, b))
    selection_guard(selection, pre['parent_seeds'])
    wanted = set(selection['entries'])
    parent = {r['record']['entry']: (i, r) for i, r in enumerate(pre['parent_metadata'], 1) if r['kind'] == 'alias-data'}
    need(len(parent) == 133 and wanted <= set(parent), 'all133 alias DATA retained,122 selected joins')
    for row in pre['parent_seeds']['entries']:
        line, alias = parent[row['entry']]
        need(line == row['alias_native_data_line'] and alias['record']['name'] == row['name'], 'exact named alias line/name')
    input_raw = checked(INPUTS, INPUTS_PIN)
    input_pins = {q['path']: q for q in json.loads(input_raw)['decomp_chunk_pins']}
    before = ALIASES.stat()
    digest = hashlib.sha256()
    offset = ordinal = lines = 0
    found = {}
    with ALIASES.open('rb') as f:
        for line, raw in enumerate(f, 1):
            digest.update(raw)
            row = json.loads(raw)
            if row['entry'] in wanted:
                need(row['entry'] not in found, 'duplicate selected original alias')
                need(row['external'] is False, 'selected original alias nonexternal')
                parent_line, retained = parent[row['entry']]
                need(row == retained['record'], 'original alias equals exact retained parent DATA')
                need((line, offset, len(raw), sha(raw)) == (retained['source_line'], retained['source_byte'], retained['raw_bytes'], retained['raw_sha256']), 'original alias line/byte/hash equals parent')
                found[row['entry']] = dict(parent_alias_native_data_line=parent_line, alias_record=row,
                    alias_source=dict(path=str(ALIASES), line=line, byte=offset, bytes=len(raw), sha256=sha(raw)), nonexternal_ordinal=ordinal, chunk_number=ordinal // 100)
            if not row['external']:
                ordinal += 1
            offset += len(raw)
            lines = line
    after = ALIASES.stat()
    need((before.st_size, before.st_mtime_ns, before.st_ino) == (after.st_size, after.st_mtime_ns, after.st_ino), 'alias stat endpoints equal')
    need((offset, digest.hexdigest()) == ALIAS_PIN and ordinal == 418417, 'whole alias custody/nonexternal ordinal')
    groups = collections.defaultdict(set)
    for entry, row in found.items():
        groups[row['chunk_number']].add(entry)
    records, chunks = [], []
    for number, entries in sorted(groups.items()):
        path = Path('/var/tmp/sound-analysis/corpus/decomp/chunks') / f'chunk-{number:05}.jsonl'
        fixed = input_pins[str(path)]
        b = checked(path, (fixed['bytes'], fixed['sha256']))
        chunks.append(fixed)
        offset = 0
        seen = set()
        for line, raw in enumerate(b.splitlines(keepends=True), 1):
            hit = re.search(br'"entry"\s*:\s*"([^\"]+)"', raw[:100])
            entry = hit[1].decode('ascii') if hit else None
            if entry in entries:
                need(entry not in seen, 'duplicate exact export')
                seen.add(entry)
                row = json.loads(raw)
                need(row['entry'] == entry, 'selected export identity')
                meta = dict(entry=entry, **found[entry], source_path=str(path), source_line=line, source_byte=offset,
                    raw_bytes=len(raw), raw_sha256=sha(raw), export_record_name=row.get('name'), signature=row.get('signature'), **measure(row))
                for key in ['body_bytes', 'body_ranges', 'state', 'warnings', 'error', 'timed_out', 'partial_code', 'thunk']:
                    meta[key] = row.get(key)
                need('code' not in meta, 'original C not retained')
                records.append(meta)
                del row
            offset += len(raw)
        need(offset == len(b), 'whole selected chunk custody')
    records.sort(key=lambda x: int(x['entry'], 16))
    present = {r['entry'] for r in records}
    missing_alias = sorted(wanted - set(found), key=lambda x: int(x, 16))
    missing_export = sorted(set(found) - present, key=lambda x: int(x, 16))
    cb = sum(r['code_utf8_bytes'] for r in records)
    cl = sum(r['C_lines'] for r in records)
    summary = dict(selected_entries=122, original_aliases_found=len(found), export_records_found=len(records), missing_alias_entries=missing_alias,
        missing_export_entries=missing_export, missing_is_absence_claim=False, code_utf8_bytes=cb, C_lines=cl,
        max_C_lines=max([r['C_lines'] for r in records], default=0), chunks=len(chunks), chunk_custody_bytes=sum(q['bytes'] for q in chunks),
        warning_records=sum(bool(r['warnings']) for r in records), warning_occurrences=sum(len(r['warnings'] or []) for r in records),
        thunk_records=sum(bool(r['thunk']) for r in records), four_byte_extent_records=sum(r['body_bytes'] == 4 for r in records),
        partial_records=sum(bool(r['partial_code']) for r in records), error_records=sum(r['error'] is not None for r in records),
        timed_out_records=sum(bool(r['timed_out']) for r in records), empty_code_records=sum(not r['code_present'] for r in records),
        state_counts=dict(collections.Counter(r['state'] for r in records)),
        within_proposed_whole_source_caps=not missing_alias and not missing_export and len(records) == 122 and cb <= 2097152 and cl <= 50000)
    result = dict(schema='whole122-modulation-export-metadata-census-v1', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        selection=pin(SELECTION, raw_selection), predecessor_pins=predecessors, class_inputs_pin=pin(INPUTS, input_raw),
        records=records, summary=summary, selected_chunk_pins=chunks,
        alias_pass=dict(path=str(ALIASES), bytes=ALIASES.stat().st_size, lines=lines, sha256=digest.hexdigest(), nonexternal_rows=ordinal, passes=1, stat_endpoints_equal=True),
        source_reading='METADATA ONLY: original C strings transiently measured/hashed, never retained/printed/semantically read; no firstN or processing-name filter. Missing is a locator gap, never absence.',
        source_caps_proposal=dict(records=122, C_bytes=2097152, C_lines=50000), source_semantics_selected=False, source_retention_selected=False,
        new_callee_global_slot_native_image_provider_original_model_harness_follow=0, new_site_grade_case_release=0,
        excluded_UI_group=dict(count=11, entries=pre['parent_seeds']['policy']['omitted_entries'], scope='Outgoing following excluded only; all133aliases/memberships preserved and required UI/lifecycleU.'),
        required_unsupported='U', coverage_gate='OPEN', successor='Separate Root coherent whole-source approval required; no retention/semantics/execution selected.')
    with (P / 'selection-metadata-only.json').open('xb') as f:
        f.write(raw_selection)
    with (P / 'candidate-census.json').open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        selfcheck()
    elif sys.argv[1:] == ['--census']:
        main()
    else:
        raise SystemExit('usage: census.py --check | --census')
