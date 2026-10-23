"""Read-only ARM64 class/address-point metadata recovery; never load original code.

Only this new analyst script runs. The existing strict Mach-O header parser is
reused as inspected pure AST definitions; xexec's bind parser is source context,
not imported or executed. Structural records are not dynamic receiver proofs.
"""
from pathlib import Path
import ast
import collections
import datetime
import hashlib
import json
import re
import struct
import sys

ROOT = Path('/home/ollie/Documents/sound')
BASE = ROOT / 'analysis/ableton-live-12.4.3'
HERE = Path(__file__).resolve().parent
IMAGE = BASE / 'derived/Live.arm64'
INDEX = Path('/var/tmp/sound-analysis/corpus/indexes')
CHUNKS = Path('/var/tmp/sound-analysis/corpus/decomp/chunks')
HEADER = ROOT / 'tools/index_macho_function_starts.py'
SHA = '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(path):
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        for raw in iter(lambda: stream.read(1048576), b''):
            size += len(raw)
            h.update(raw)
    return dict(path=str(path), bytes=size, sha256=h.hexdigest())


def write(name, value):
    with (HERE / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def jsonlines(name, rows):
    with (HERE / name).open('x') as stream:
        for row in rows:
            stream.write(json.dumps(row, separators=(',', ':')) + '\n')


def leb(blob, pos, signed=False):
    value = 0
    for i in range(10):
        assert pos < len(blob)
        byte = blob[pos]
        pos += 1
        assert i < 9 or (byte <= 1 if not signed else byte in (0, 1, 126, 127))
        value |= (byte & 127) << (7 * i)
        if not byte & 128:
            if signed and byte & 64:
                value -= 1 << (7 * (i + 1))
            return value, pos
    raise AssertionError('overlong LEB')


def bind_records(blob, segments, payload_fileoff):
    """Interpret normal dyld binding metadata only; never apply a fixup."""
    pos, segment, offset, addend, kind, ordinal, name = 0, None, 0, 0, 1, 0, ''
    records = []

    def emit(op_start):
        assert segment is not None and 0 <= segment < len(segments)
        seg = segments[segment]
        assert kind == 1 and name and 0 <= offset <= seg['filesize'] - 8
        records.append(dict(address=seg['vmaddr'] + offset,
                            file_offset=seg['fileoff'] + offset, symbol=name,
                            addend=addend, dylib_ordinal=ordinal,
                            bind_opcode_file_offset=payload_fileoff + op_start))

    while pos < len(blob):
        start = pos
        op, imm = blob[pos] & 240, blob[pos] & 15
        pos += 1
        if op == 0:
            assert all(v == 0 for v in blob[pos:])
            return records
        if op == 0x10:
            ordinal = imm
        elif op == 0x20:
            ordinal, pos = leb(blob, pos)
        elif op == 0x30:
            ordinal = imm if imm == 0 else imm - 16
        elif op == 0x40:
            end = blob.find(b'\0', pos)
            assert end >= pos
            name = blob[pos:end].decode('ascii')
            pos = end + 1
        elif op == 0x50:
            kind = imm
            assert kind == 1
        elif op == 0x60:
            addend, pos = leb(blob, pos, True)
        elif op == 0x70:
            segment = imm
            offset, pos = leb(blob, pos)
        elif op == 0x80:
            n, pos = leb(blob, pos)
            offset += n
        elif op == 0x90:
            emit(start)
            offset += 8
        elif op == 0xa0:
            emit(start)
            n, pos = leb(blob, pos)
            offset += n + 8
        elif op == 0xb0:
            emit(start)
            offset += 8 + imm * 8
        elif op == 0xc0:
            n, pos = leb(blob, pos)
            skip, pos = leb(blob, pos)
            assert n <= 1000000
            for _ in range(n):
                emit(start)
                offset += 8 + skip
        else:
            raise AssertionError('unsupported bind opcode ' + hex(op))
    raise AssertionError('normal bind metadata has no DONE')


def fixtures():
    assert leb(b'\x80\x01', 0) == (128, 2)
    assert leb(b'\x7f', 0, True) == (-1, 1)
    seg = [dict(vmaddr=0x1000, fileoff=0, filesize=32)]
    rows = bind_records(b'\x11\x40symbol\0\x51\x60\x10\x70\x08\x90\0', seg, 200)
    assert rows[0]['address'] == 0x1008 and rows[0]['addend'] == 16
    rejected = 0
    for blob in (b'\x70\x20\x90\0', b'\x40x\0\x52\0', b'\xd0', b'\x40x', b'\0\x01'):
        try:
            bind_records(blob, seg, 0)
        except (AssertionError, ValueError, IndexError):
            rejected += 1
    assert rejected == 5
    return dict(positive=3, rejected=5)


def main():
    assert sys.argv[1:] == ['--build'], 'Explicit --build only; no native/tool calls.'
    outputs = ['class-inputs.json', 'class-rtti.jsonl', 'class-tables.jsonl',
               'class-legacy-validation.jsonl', 'class-stores.jsonl', 'class-summary.json']
    assert all(not (HERE / name).exists() for name in outputs)
    tests = fixtures()
    providers = [IMAGE, HEADER, ROOT / 'tools/xexec/xexec.c',
                 BASE / 'r2/c1-live-v1/indexes-manifest.json',
                 INDEX / 'manifest.json', INDEX / 'aliases.jsonl', INDEX / 'vtables.jsonl',
                 Path(__file__).resolve()]
    before = [identity(p) for p in providers]
    assert before[0]['bytes'] == 149711904 and before[0]['sha256'] == SHA
    expected = json.loads(providers[3].read_text())
    assert before[5]['sha256'] == expected['files']['aliases.jsonl']['sha256']
    assert before[6]['sha256'] == expected['files']['vtables.jsonl']['sha256']
    data = IMAGE.read_bytes()
    source = ast.parse(HEADER.read_text())
    selected = [n for n in source.body if isinstance(n, ast.FunctionDef) and
                n.name in ('require', 'span', 'header')]
    assert len(selected) == 3
    namespace = dict(struct=struct, U64=(1 << 64) - 1)
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(HEADER), 'exec'), namespace)
    info = namespace['header'](data)
    segments = info['segments']
    ncmd, lcbytes = struct.unpack_from('<II', data, 16)
    assert (ncmd, lcbytes) == (53, 6944)
    sections, binds, cursor = [], None, 32
    for _ in range(ncmd):
        command, size = struct.unpack_from('<II', data, cursor)
        if command == 0x19:
            ns = struct.unpack_from('<I', data, cursor + 64)[0]
            for i in range(ns):
                at = cursor + 72 + i * 80
                sn, sg, va, length, off, align, rel, nr, flags, r1, r2, r3 = struct.unpack_from('<16s16sQQ8I', data, at)
                sections.append(dict(name=sn.split(b'\0')[0].decode(), segment=sg.split(b'\0')[0].decode(),
                                     va=va, bytes=length, file_offset=off, flags=flags))
        elif command == 0x80000022:
            assert binds is None
            binds = struct.unpack_from('<10I', data, cursor + 8)
        cursor += size
    assert cursor == 32 + lcbytes and binds is not None

    def mapping(va, size=8):
        hits = [s for s in sections if s['va'] <= va and va + size <= s['va'] + s['bytes']
                and (s['flags'] & 255) not in (1, 12, 18)]
        assert len(hits) == 1
        s = hits[0]
        off = s['file_offset'] + va - s['va']
        assert 0 <= off <= len(data) - size
        return off, s

    def executable(va):
        if va % 4:
            return False
        try:
            _, s = mapping(va, 4)
            return bool(s['flags'] & (0x80000000 | 0x400))
        except AssertionError:
            return False

    boff, blen = binds[2:4]
    assert 0 <= boff <= len(data) - blen
    bindrows = bind_records(data[boff:boff + blen], segments, boff)
    rtti = {}
    for bind in bindrows:
        if bind['symbol'] not in ('__ZTVN10__cxxabiv117__class_type_infoE',
                                  '__ZTVN10__cxxabiv120__si_class_type_infoE',
                                  '__ZTVN10__cxxabiv121__vmi_class_type_infoE'):
            continue
        assert bind['addend'] == 16
        va = bind['address']
        off, section = mapping(va, 16)
        first, rawname = struct.unpack_from('<QQ', data, off)
        nameva = rawname & ((1 << 63) - 1)
        try:
            noff, nsection = mapping(nameva, 1)
        except AssertionError:
            continue
        maximum = min(4096, nsection['va'] + nsection['bytes'] - nameva)
        end = data.find(b'\0', noff, noff + maximum)
        if end < noff:
            continue
        namebytes = data[noff:end]
        if not namebytes or not all(32 < c < 127 for c in namebytes):
            continue
        rtti[va] = dict(address=hex(va), file_offset=off, raw16_hex=data[off:off + 16].hex(),
                        class_typeinfo_bind=bind, raw_name_word=hex(rawname),
                        name_pointer=hex(nameva), name_file_offset=noff,
                        name_pointer_interpretation='direct' if rawname == nameva else 'bit63-cleared candidate interpretation',
                        literal_type_encoding=namebytes.decode('ascii'),
                        name_NUL_hex=data[noff:end + 1].hex(),
                        name_section=[nsection['segment'], nsection['name']],
                        status='bound-class-typeinfo-layout; literal name interpretation qualified')
    functions = {}
    with (INDEX / 'aliases.jsonl').open() as stream:
        for lineno, line in enumerate(stream, 1):
            row = json.loads(line)
            if not row['external']:
                functions[int(row['entry'], 16)] = dict(name=row['name'], alias_line=lineno)
    tables = []
    scan_sections = [s for s in sections if s['segment'] in ('__DATA_CONST', '__DATA')
                     and s['name'] == '__const']
    for section in scan_sections:
        for off in range(section['file_offset'], section['file_offset'] + section['bytes'] - 23, 8):
            top, ti, target = struct.unpack_from('<qQQ', data, off)
            if not (-0x100000000 <= top <= 0 and ti in rtti and executable(target)):
                continue
            base = section['va'] + off - section['file_offset']
            slots, reason = [], 'slot-cap128; not complete extent'
            for i in range(128):
                try:
                    so, ss = mapping(base + 16 + i * 8, 8)
                except AssertionError:
                    reason = 'section boundary'
                    break
                value = struct.unpack_from('<Q', data, so)[0]
                if not executable(value):
                    reason = 'first non-executable-section target; not a complete-table assertion'
                    break
                known = functions.get(value)
                slots.append(dict(offset=i * 8, target=hex(value), raw8_hex=data[so:so + 8].hex(),
                                  status='known-exported-function-entry' if known else 'executable-section address only',
                                  function=known))
            tables.append(dict(table_header=hex(base), address_point=hex(base + 16),
                               header_file_offset=off, address_point_file_offset=off + 16,
                               raw_header16_hex=data[off:off + 16].hex(), offset_to_top=top,
                               typeinfo=hex(ti), literal_type_encoding=rtti[ti]['literal_type_encoding'],
                               status='structurally-validated RTTI/header + nonempty executable prefix; receiver identity unproved',
                               slots=slots, stop_reason=reason, native_table_extent=None,
                               constructor_store_count=0))
    addresspoints = {int(r['address_point'], 16): r for r in tables}
    legacy = []
    with (INDEX / 'vtables.jsonl').open('rb') as stream:
        for lineno, raw in enumerate(stream, 1):
            row = json.loads(raw)
            oldbase = int(row['address'], 16)
            validations = []
            for slot in row['slots']:
                cell = oldbase + slot['offset']
                try:
                    off, _ = mapping(cell)
                    actual = struct.unpack_from('<Q', data, off)[0]
                    agrees = actual == int(slot['function'], 16)
                except AssertionError:
                    actual, agrees = None, False
                validations.append(dict(header_relative_offset=slot['offset'],
                                        exported_target=slot['function'], raw_file_target=None if actual is None else hex(actual),
                                        file_target_agrees=agrees, executable_section_target=executable(actual) if actual else False,
                                        known_function_entry=actual in functions,
                                        addresspoint_offset=slot['offset'] - 16))
            legacy.append(dict(line=lineno, raw_row_sha256=digest(raw), address=row['address'], symbols=row['symbols'],
                               recovered_address_point=hex(oldbase + 16) if oldbase + 16 in addresspoints else None,
                               slots=validations, export_stop=row['stop']))
    # Lexical constructor/store anchors only, not full body interpretation or receiver proofs.
    stores, chunkpins, scanned = [], [], 0
    token = re.compile(r'\b(?:[A-Za-z][A-Za-z0-9]*_)*([0-9a-f]{9})\b')
    for path in sorted(CHUNKS.glob('chunk-*.jsonl')):
        h = hashlib.sha256()
        with path.open('rb') as stream:
            for lineno, raw in enumerate(stream, 1):
                h.update(raw)
                row = json.loads(raw)
                scanned += 1
                code = row.get('code') or ''
                for cn, line in enumerate(code.splitlines(), 1):
                    if '=' not in line or '==' in line or not line.lstrip().startswith('*'):
                        continue
                    lhs, rhs = line.split('=', 1)
                    targets = {int(m.group(1), 16) for m in token.finditer(rhs)} & addresspoints.keys()
                    for target in sorted(targets):
                        stores.append(dict(address_point=hex(target), entry=row['entry'], function_name=row['name'],
                                           source_provider=str(path), source_line=lineno, raw_row_sha256=digest(raw),
                                           code_sha256=row.get('code_sha256'), code_line=cn, quote=line,
                                           state=row['state'], warnings=row['warnings'],
                                           status='literal decompiled store candidate; receiver/ABI/lifetime not established'))
                        addresspoints[target]['constructor_store_count'] += 1
        chunkpins.append(dict(path=str(path), bytes=path.stat().st_size, sha256=h.hexdigest()))
    after = [identity(p) for p in providers]
    assert before == after
    assert len(legacy) == 80
    governance = [ROOT / 'wiki/research' / name for name in
                  ('full-live-specification-plan.md', 'full-live-specification-design.md', 'native-decompilation-roadmap.md')]
    write('class-inputs.json', dict(pins=before, decomp_chunk_pins=chunkpins,
                                   governance_asof=[identity(p) for p in governance],
                                   no_mutable_future_hash_gate=True))
    jsonlines('class-rtti.jsonl', rtti.values())
    jsonlines('class-tables.jsonl', tables)
    jsonlines('class-legacy-validation.jsonl', legacy)
    jsonlines('class-stores.jsonl', stores)
    summary = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   status='Author data recovery; independent review pending',
                   tests=tests, source_image_sha256=SHA, header=[ncmd, lcbytes],
                   normal_bind_records=len(bindrows), rtti_records=len(rtti),
                   distinct_literal_type_encodings=len({r['literal_type_encoding'] for r in rtti.values()}),
                   primary_tables=sum(r['offset_to_top'] == 0 for r in tables),
                   secondary_tables=sum(r['offset_to_top'] < 0 for r in tables),
                   address_points=len(tables), executable_prefix_slots=sum(len(r['slots']) for r in tables),
                   known_function_entry_slots=sum(s['status'] == 'known-exported-function-entry' for r in tables for s in r['slots']),
                   retained_legacy_tables=80,
                   legacy_nonexec_slots=sum(not s['executable_section_target'] for r in legacy for s in r['slots']),
                   literal_store_candidates=len(stores), decomp_records_lexically_scanned=scanned,
                   constructor_store_semantic_full_read=False,
                   table_scan_scope=[dict(s) for s in scan_sections], slot_prefix_cap=128,
                   offset_to_top_scan_bound=[-0x100000000, 0], pins_unchanged=True,
                   limits=['RTTI/header/executable-prefix validation is structural under the Itanium-style layout interpretation, not runtime construction or dynamic receiver proof.',
                           'Bit63 clearing is explicit candidate pointer normalization, not proven global RTTI ABI or a demangled class identity.',
                           'Only normal dyld binding metadata class_type_info/si/vmi records are selected; missing/weak/private/stripped RTTI and other layouts stay unavailable, not absent.',
                           'Slot runs stop before non-executable targets and at128; null/import/other layouts can truncate them. Not complete native table extents.',
                           'Exported-function membership does not establish invocation, callability, dispatch eligibility or method ownership for all callers.',
                           'Store matches are lexical selected lines, not full constructor/body reading. They require source/ABI/receiver/lifetime validation before site attachment.',
                           'No new indirect site is resolved merely by these class/slot memberships; no new behavior/coverage/grade/completed-family credit.',
                           'No original code/tool/loader/native execution or source re-export occurred.'])
    write('class-summary.json', summary)
    print(json.dumps({k: v for k, v in summary.items() if k not in ('limits', 'table_scan_scope')}, indent=2))


if __name__ == '__main__':
    main()
