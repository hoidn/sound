"""Read-only finite checks for class-* recovery, never original/native execution."""
from pathlib import Path
import ast
import collections
import hashlib
import json
import struct
import sys

HERE = Path(__file__).resolve().parent


def identity(path):
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        for data in iter(lambda: stream.read(1048576), b''):
            h.update(data)
            size += len(data)
    return dict(path=str(path), bytes=size, sha256=h.hexdigest())


def rows(name):
    with (HERE / name).open() as stream:
        for line in stream:
            yield json.loads(line)


def main():
    assert sys.argv[1:] == ['--check'], 'Read-only --check only.'
    inputs = json.loads((HERE / 'class-inputs.json').read_text())
    pinned = inputs['pins'] + inputs['decomp_chunk_pins']
    current = sorted(set(Path(r['path']) for r in pinned) |
                     set(p for p in HERE.glob('class-*') if p.is_file()))
    before = [identity(p) for p in current]
    for record in pinned:
        assert identity(Path(record['path'])) == record
    image = Path(inputs['pins'][0]['path']).read_bytes()
    segments, sections, cursor = [], [], 32
    count, size = struct.unpack_from('<II', image, 16)
    assert (count, size) == (53, 6944)
    for _ in range(count):
        cmd, length = struct.unpack_from('<II', image, cursor)
        if cmd == 0x19:
            _, va, vs, off, fs, _, prot, ns, _ = struct.unpack_from('<16sQQQQiiII', image, cursor + 8)
            segments.append((va, fs, off))
            for n in range(ns):
                sn, sg, sva, ssize, soff, al, rel, nr, flags, r1, r2, r3 = struct.unpack_from('<16s16sQQ8I', image, cursor + 72 + n * 80)
                if (flags & 255) not in (1, 12, 18):
                    sections.append((sva, ssize, soff, flags))
        cursor += length
    assert cursor == 32 + size

    def executable(address):
        matches = [s for s in sections if s[0] <= address and address + 4 <= s[0] + s[1]]
        return address % 4 == 0 and len(matches) == 1 and bool(matches[0][3] & 0x80000400)

    assert executable(0x101ab7898)
    assert not executable(0x106662d78)  # Actual legacy DATA value, not a function.
    assert not executable(0x10912b600)  # Exporter's external RTTI pseudo-address.
    assert not executable(0x101ab7899)  # Misaligned address inside executable section.

    rtti = {}
    for row in rows('class-rtti.jsonl'):
        va, off = int(row['address'], 16), row['file_offset']
        assert row['raw16_hex'] == image[off:off + 16].hex()
        first, pointer = struct.unpack_from('<QQ', image, off)
        assert pointer == int(row['raw_name_word'], 16)
        assert pointer & ((1 << 63) - 1) == int(row['name_pointer'], 16)
        name = bytes.fromhex(row['name_NUL_hex'])
        assert name == row['literal_type_encoding'].encode('ascii') + b'\0'
        assert image[row['name_file_offset']:row['name_file_offset'] + len(name)] == name
        bind = row['class_typeinfo_bind']
        assert bind['address'] == va and bind['file_offset'] == off and bind['addend'] == 16
        assert first == 16
        assert va not in rtti
        rtti[va] = row
    tables, counts = {}, collections.Counter()
    for row in rows('class-tables.jsonl'):
        ap = int(row['address_point'], 16)
        header = int(row['table_header'], 16)
        off = row['header_file_offset']
        assert ap == header + 16 and row['address_point_file_offset'] == off + 16
        top, ti = struct.unpack_from('<qQ', image, off)
        assert row['raw_header16_hex'] == image[off:off + 16].hex()
        assert top == row['offset_to_top'] and ti in rtti
        assert row['literal_type_encoding'] == rtti[ti]['literal_type_encoding']
        assert 1 <= len(row['slots']) <= 128 and row['native_table_extent'] is None
        for n, slot in enumerate(row['slots']):
            target = int(slot['target'], 16)
            assert slot['offset'] == 8 * n and executable(target)
            assert slot['raw8_hex'] == image[off + 16 + n * 8:off + 24 + n * 8].hex()
            assert struct.unpack_from('<Q', image, off + 16 + n * 8)[0] == target
            counts[slot['status']] += 1
        assert ap not in tables
        tables[ap] = row
    stores = collections.Counter()
    for row in rows('class-stores.jsonl'):
        ap = int(row['address_point'], 16)
        assert ap in tables and row['quote'].lstrip().startswith('*')
        assert '=' in row['quote'] and ap != 0
        stores[ap] += 1
    assert all(r['literal_store_candidate_count'] == stores[ap] for ap, r in tables.items())
    legacy = list(rows('class-legacy-validation.jsonl'))
    assert len(legacy) == 80
    total, nonexec, mismatched, recovered = 0, 0, 0, 0
    for row in legacy:
        recovered += row['recovered_address_point'] is not None
        for slot in row['slots']:
            total += 1
            raw = slot['raw_file_target']
            value = int(raw, 16) if raw is not None else 0
            assert slot['executable_section_target'] == executable(value)
            nonexec += not slot['executable_section_target']
            mismatched += not slot['file_target_agrees']
    assert (total, nonexec, mismatched, recovered) == (2191, 9, 8, 55)
    summary = json.loads((HERE / 'class-summary.json').read_text())
    assert (len(rtti), len(tables), sum(stores.values())) == (summary['rtti_records'], summary['address_points'], summary['literal_store_candidates'])
    assert counts['known-exported-function-entry'] == summary['known_function_entry_slots']
    assert sum(counts.values()) == summary['executable_prefix_slots']
    # Execute only these fully read pure analyst parser/fixture definitions.
    source = ast.parse((HERE / 'class-recovery.py').read_text())
    selected = [n for n in source.body if isinstance(n, ast.FunctionDef) and n.name in ('leb', 'bind_records', 'fixtures')]
    assert len(selected) == 3
    namespace = {}
    exec(compile(ast.Module(body=selected, type_ignores=[]), '<class-pure-fixtures>', 'exec'), namespace)
    assert namespace['fixtures']() == dict(positive=7, rejected=8)
    assert summary['normal_bind_records'] == summary['normal_bind_unique_addresses'] == 41401
    assert summary['normal_bind_duplicate_addresses'] == 0
    assert before == [identity(p) for p in current]
    print(json.dumps(dict(status='PASS data-only class checks', pins=len(pinned), watched=len(current),
                          unchanged=True, rtti_records=len(rtti), address_points=len(tables),
                          prefix_slots=sum(counts.values()), legacy_slot_values=total,
                          legacy_nonexec_values=nonexec, legacy_file_mismatches=mismatched,
                          lexical_store_candidates=sum(stores.values()), new_site_resolution=0,
                          pure_positive=7, pure_rejected=8, executable_classification_controls=4,
                          native_or_original_execution=False), indent=2))


if __name__ == '__main__':
    main()
