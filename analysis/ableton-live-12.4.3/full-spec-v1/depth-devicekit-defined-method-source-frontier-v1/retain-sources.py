"""Retain only Root-selected exact export-record byte ranges, once. Stdlib data only."""
from pathlib import Path
import datetime
import hashlib
import json

P = Path(__file__).resolve().parent


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    census_raw = (P / 'candidate-census.json').read_bytes()
    selection_raw = (P / 'selection-source-read.json').read_bytes()
    assert digest(census_raw) == '2eeae8cc2f6cddfd9f913c8e169f1d5ff3966d9a8228697b075346746d16fcf6'
    assert digest(selection_raw) == '16754c5909db05926a232210ca0e023e79fe586592adbd52165ba3e2c1658032'
    census, selection = json.loads(census_raw), json.loads(selection_raw)
    assert [r['entry'] for r in census['records']] == selection['entries']
    assert len(selection['entries']) == 27
    assert not (P / 'sources.jsonl').exists()
    assert not (P / 'source-retention.json').exists()
    retained, receipts, offset = [], [], 0
    for m in census['records']:
        source = Path(m['source_path'])
        before = source.stat()
        with source.open('rb') as f:
            f.seek(m['source_byte'])
            raw = f.read(m['raw_bytes'])
        after = source.stat()
        assert (before.st_size, before.st_mtime_ns, before.st_ino) == (after.st_size, after.st_mtime_ns, after.st_ino)
        assert len(raw) == m['raw_bytes'] and digest(raw) == m['raw_sha256']
        d = json.loads(raw)
        assert d['entry'] == m['entry']
        code = (d.get('code') or '').encode()
        assert len(code) == m['code_utf8_bytes'] and digest(code) == m['code_sha256']
        assert len(code.decode().splitlines()) == m['C_lines']
        assert d['warnings'] == m['warnings'] and d['body_bytes'] == m['native_body_bytes']
        assert d['body_ranges'] == m['native_body_ranges']
        retained.append(raw)
        receipts.append(dict(entry=m['entry'], source_path=str(source), source_line=m['source_line'], source_byte=m['source_byte'], raw_bytes=len(raw), raw_sha256=digest(raw), retained_byte=offset, C_bytes=len(code), C_lines=m['C_lines'], C_sha256=digest(code), stat_unchanged=True))
        offset += len(raw)
    payload = b''.join(retained)
    assert sum(x['C_bytes'] for x in receipts) == 121309
    assert sum(x['C_lines'] for x in receipts) == 3601
    with (P / 'sources.jsonl').open('xb') as f:
        f.write(payload)
    result = dict(schema='exact-selected-retained-source-custody-v1', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), source_selection_sha256=digest(selection_raw), census_sha256=digest(census_raw), records=receipts, selected_raw_bytes=len(payload), retained_sha256=digest(payload), inherited_chunk_pins=census['selected_chunk_pins'], fresh_chunk_full_hashes=0, semantic_read_status='retained now; complete source read follows', scope='Only selected exact byte ranges read. No aliases/index rescan, unselected source parsing, native/image/provider/original/callee/global/slot acquisition.', original_calls=0)
    with (P / 'source-retention.json').open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(dict(records=len(receipts), raw_bytes=len(payload), C_bytes=121309, C_lines=3601, sha256=digest(payload))))


if __name__ == '__main__':
    main()
