"""Retain the separately Root-selected seven exact export records once; no whole-chunk replay."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

P = Path(__file__).resolve().parent
H = lambda b: hashlib.sha256(b).hexdigest()


def main():
    assert sys.argv[1:] == ['--retain'], 'fixed --retain only, before reads'
    selection_raw = (P / 'source-selection-root.json').read_bytes()
    census_raw = (P / 'candidate-census.json').read_bytes()
    assert len(selection_raw) == 2366 and H(selection_raw) == '6e05dada98e72dab38f05d64c7f743a8e67c9e54ddb683a85cd263dc8fed1048'
    assert len(census_raw) == 10963 and H(census_raw) == 'ee5dc80ff16db40c2b99249c175aade22cd5c0c8c7170dad598f585274709c54'
    selection, census = json.loads(selection_raw), json.loads(census_raw)
    assert [m['entry'] for m in census['records']] == selection['entries']
    assert len(selection['entries']) == 7
    assert not (P / 'sources.jsonl').exists() and not (P / 'source-retention.json').exists()
    raw_records, receipts, offset = [], [], 0
    for m in census['records']:
        path = Path(m['source_path'])
        assert str(path) in {p['path'] for p in census['selected_chunk_pins']}
        before = path.stat()
        with path.open('rb') as stream:
            stream.seek(m['source_byte'])
            raw = stream.read(m['raw_bytes'])
        after = path.stat()
        assert (before.st_size, before.st_mtime_ns, before.st_ino) == (after.st_size, after.st_mtime_ns, after.st_ino)
        assert len(raw) == m['raw_bytes'] and H(raw) == m['raw_sha256']
        record = json.loads(raw)
        code = record['code'].encode()
        assert record['entry'] == m['entry']
        assert len(code) == m['code_utf8_bytes'] and H(code) == m['code_sha256']
        assert len(record['code'].splitlines()) == m['C_lines']
        assert record['body_bytes'] == m['native_body_bytes'] and record['body_ranges'] == m['native_body_ranges']
        assert record['warnings'] == m['warnings'] and record['thunk'] == m['record_thunk']
        raw_records.append(raw)
        receipts.append(dict(entry=m['entry'], source_path=str(path),
            source_line=m['source_line'], source_byte=m['source_byte'], raw_bytes=len(raw),
            raw_sha256=H(raw), retained_byte=offset, C_bytes=len(code),
            C_lines=m['C_lines'], C_sha256=H(code), stat_unchanged=True))
        offset += len(raw)
    payload = b''.join(raw_records)
    assert len(payload) == 10797
    assert sum(r['C_bytes'] for r in receipts) == 7851 and sum(r['C_lines'] for r in receipts) == 277
    with (P / 'sources.jsonl').open('xb') as stream:
        stream.write(payload)
    receipt = dict(schema='exact-seven-retained-delegate-source-custody-v1',
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source_selection_sha256=H(selection_raw), census_sha256=H(census_raw),
        records=receipts, raw_bytes=len(payload), raw_sha256=H(payload),
        inherited_chunk_pins=census['selected_chunk_pins'], fresh_whole_chunk_hashes=0,
        original_record_range_reads=7, aliases_rescans=0,
        semantic_read_status='retained now; full source semantic read follows',
        scope='Only exact seven selected original byte ranges, once each. No encountered body, global, slot, index, native, image, provider or original execution.')
    with (P / 'source-retention.json').open('x') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(records=7, raw_bytes=len(payload), raw_sha256=H(payload),
                         C_bytes=7851, C_lines=277, whole_chunk_hashes=0,
                         original_record_range_reads=7)))


if __name__ == '__main__':
    main()

