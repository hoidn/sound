"""Independent finite retained-byte checks. No instruction or author-code execution."""
from pathlib import Path
import hashlib
import json
import struct
import sys

BASE = Path(__file__).resolve().parents[1]
QUERY = BASE / 'queries/corpus-midi-render-argument-frontier-2026-10-20.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def sx(value, bits):
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def fields(word, address):
    """Only the finite opcode families actually selected in this review."""
    if word & 0xffe0ffe0 == 0xaa0003e0:
        return dict(width=64, Rm=(word >> 16) & 31, Rd=word & 31)
    if word & 0x1f000000 == 0x11000000:
        return dict(width=64 if word >> 31 else 32, subtract=(word >> 30) & 1,
                    Rn=(word >> 5) & 31, Rd=word & 31,
                    immediate=((word >> 10) & 4095) << (12 if word & (1 << 22) else 0))
    if word & 0xffc00000 in (0xf9400000, 0xf9000000):
        return dict(width=64, load=(word >> 22) & 1, Rt=word & 31,
                    Rn=(word >> 5) & 31, byte_offset=((word >> 10) & 4095) * 8)
    if word & 0x7f800000 == 0x52800000:
        return dict(width=64 if word >> 31 else 32, Rd=word & 31,
                    imm16=(word >> 5) & 65535, shift=((word >> 21) & 3) * 16)
    if word & 0x7e000000 == 0x34000000:
        offset = sx((word >> 5) & 0x7ffff, 19) * 4
        return dict(width=64 if word >> 31 else 32, Rt=word & 31,
                    nonzero=(word >> 24) & 1, signed_byte_offset=offset,
                    target=hex(address + offset))
    if word & 0xfffffc1f == 0xd63f0000 or word & 0xfffffc1f == 0xd65f0000:
        return dict(Rn=(word >> 5) & 31)
    if word & 0x3a000000 == 0x28000000:
        mode = (word >> 23) & 3
        assert mode == 2, 'Only selected offset pairs are permitted'
        result = dict(load=(word >> 22) & 1, Rt=word & 31, Rt2=(word >> 10) & 31,
                      Rn=(word >> 5) & 31,
                      signed_scaled_byte_offset=sx((word >> 15) & 127, 7) * 8)
        if word & (1 << 26):
            assert (word >> 30) & 3 == 1
            result.update(width=64, base_writeback=False)
        else:
            assert word >> 30 == 2
            result['address_mode'] = 'signed offset'
        return result
    raise AssertionError(('unselected opcode', hex(address), hex(word)))


def critical(words):
    expected = {0x932c: 0xaa0103f3, 0x9330: 0xaa0003f4, 0x9348: 0x35000540,
                0x9398: 0xf9402697, 0x939c: 0xb4000117, 0x93a0: 0xf94002e0,
                0x93a4: 0xf9402808, 0x93a8: 0xa9007ff3, 0x93ac: 0x52800001,
                0x93b0: 0xd63f0100, 0x93b4: 0xf94006f7, 0x93b8: 0xb5ffff57}
    for address, value in expected.items():
        assert words[address] == value


def main():
    assert sys.argv[1:] == ['--check'], 'Read-only --check only'
    qraw = QUERY.read_bytes()
    assert len(qraw) == 37938 and sha(qraw) == '0e52c14e8c2d91312597964009edf781083e17a82e662d2b55a3baecef8c0223'
    q = json.loads(qraw)
    watch = {str(QUERY): qraw}
    for pin in q['input_pins_asof']:
        p = Path(pin['path']); raw = p.read_bytes()
        assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256']
        watch[str(p)] = raw
    providers = {}
    for route in q['precise_old_callee_proof_routes']:
        p = Path(route['provider']); raw = p.read_bytes()
        watch[str(p)] = raw
        providers[str(p)] = json.loads(raw)
    image = watch[q['instruction_data_and_limited_decodes']['image_path']]
    assert image[:32].hex() == q['instruction_data_and_limited_decodes']['header_hex']
    magic, cpu, sub, kind, ncmds, cmds_size, flags, reserved = struct.unpack_from('<8I', image)
    assert magic == 0xfeedfacf and cpu == 0x100000c and kind == 8
    offset = 32; segments = []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', image, offset)
        assert size >= 8 and offset + size <= 32 + cmds_size
        if cmd == 0x19:
            name = image[offset + 8:offset + 24].split(b'\0')[0].decode()
            va, vs, fo, fs = struct.unpack_from('<4Q', image, offset + 24)
            assert fo + fs <= len(image)
            segments.append(dict(name=name, vmaddr=hex(va), vmsize=vs, fileoff=fo, filesize=fs))
        offset += size
    assert offset == 32 + cmds_size
    assert segments == q['instruction_data_and_limited_decodes']['segments']

    def at(va, size):
        matches = [s for s in segments if int(s['vmaddr'], 16) <= va and
                   va + size <= int(s['vmaddr'], 16) + s['filesize']]
        assert len(matches) == 1
        s = matches[0]; pos = s['fileoff'] + va - int(s['vmaddr'], 16)
        return pos, image[pos:pos + size]

    def span_check(span):
        start = int(span['start'], 16)
        pos, raw = at(start, span['bytes'])
        assert pos == span['file_offset'] and raw.hex() == span['raw_hex']
        assert sha(raw) == span['sha256'] and len(span['words']) * 4 == len(raw)
        rows = []
        for i, row in enumerate(span['words']):
            address = start + i * 4
            word = struct.unpack_from('<I', raw, i * 4)[0]
            assert int(row['address'], 16) == address
            assert int(row['word'], 16) == word
            assert row['raw_le_hex'] == raw[i * 4:i * 4 + 4].hex()
            decoded = fields(word, address)
            assert decoded == row['fields'], (hex(address), decoded, row['fields'])
            rows.append((address, word))
        return rows

    all_words = dict(pair for span in q['instruction_data_and_limited_decodes']['spans']
                     for pair in span_check(span))
    assert len(all_words) == 47
    critical(all_words)
    marker = q['numeric_marker_lookup']
    start = int(marker['function_start'], 16)
    _, function_raw = at(start, marker['function_machine_bytes'])
    assert sha(function_raw) == marker['function_bytes_sha256']
    matches = [start + i for i in range(0, len(function_raw), 4)
               if struct.unpack_from('<I', function_raw, i)[0] & 0xfffffc00 == 0xf9402400]
    assert matches == [0x9398] and marker['match_count'] == 1
    call_data = q['prefix_direct_call_metadata']
    for row in call_data['records']:
        raw = watch[call_data['path']].splitlines(keepends=True)[row['line_1based'] - 1]
        assert len(raw) == row['raw_record_bytes_including_lf'] and sha(raw) == row['raw_record_sha256']
        assert json.loads(raw) == row['record']
    # Recognize only writes in actual selected words; no register-state simulation.
    for address, word in all_words.items():
        if address <= 0x932c:
            continue
        d = fields(word, address)
        if word & 0xfffffc1f == 0xd63f0000:
            writes = {30}
        elif word & 0x7e000000 == 0x34000000:
            writes = set()
        elif 'Rt2' in d:
            writes = {d['Rt'], d['Rt2']} if d['load'] and not word & (1 << 26) else set()
        elif 'load' in d:
            writes = {d['Rt']} if d['load'] else set()
        else:
            writes = {d['Rd']}
        assert not {19, 31} & writes
    rejected = []
    for name, address, wrong in [
        ('wrong entry manager register', 0x932c, 0xaa0203f3),
        ('wrong render object register', 0x9330, 0xaa0103f4),
        ('hide uninspected nonzero branch', 0x9348, 0x35000560),
        ('wrong list offset', 0x9398, 0xf9402a97),
        ('wrong callback slot', 0x93a4, 0xf9402408),
        ('wrong stack carrier', 0x93a8, 0xa9007ff6),
        ('wrong stack offset', 0x93a8, 0xa9017ff3),
        ('nonzero mode', 0x93ac, 0x52800041),
        ('wrong call register', 0x93b0, 0xd63f0120),
        ('wrong loop backedge', 0x93b8, 0xb5ffff37)]:
        altered = dict(all_words); altered[address] = wrong
        try:
            critical(altered)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    enrollment = providers[q['precise_old_callee_proof_routes'][0]['provider']]
    callee = enrollment['instruction_data_and_limited_decodes']['spans'][2]
    assert len(span_check(callee)) == 14
    slots = providers[q['precise_old_callee_proof_routes'][2]['provider']]
    pointers = []
    for row in slots['data_and_target_metadata']['selected_words']:
        pos, raw = at(int(row['virtual_address'], 16), 8)
        assert pos == row['file_offset'] and raw.hex() == row['raw_le_hex']
        assert hex(struct.unpack('<Q', raw)[0]) == row['target']
        pointers.append(row['target'])
    source_rows = []
    selected = [(json.loads(Path(q['reused_source_identity']['provider']).read_bytes())['source_records'][1]),
                providers[q['precise_old_callee_proof_routes'][1]['provider']]['records'][0],
                slots['source_records'][1],
                providers[q['precise_old_callee_proof_routes'][3]['provider']]['new_record']]
    for row in selected:
        p = Path(row['path']); raw_file = p.read_bytes(); watch[str(p)] = raw_file
        raw = raw_file.splitlines(keepends=True)[row['line_1based'] - 1]
        size_key = 'raw_record_bytes_including_lf' if 'raw_record_bytes_including_lf' in row else 'raw_bytes_including_LF'
        hash_key = 'raw_record_sha256' if 'raw_record_sha256' in row else 'raw_sha256_including_LF'
        assert len(raw) == row[size_key] and sha(raw) == row[hash_key]
        actual = json.loads(raw)
        assert actual == row['record']
        code = actual['code'].encode()
        assert len(code) == actual['code_bytes'] and sha(code) == actual['code_sha256']
        source_rows.append(dict(entry=actual['entry'], code_bytes=len(code), sha256=sha(code)))
    code = selected[0]['record']['code']
    assert q['exact_reused_mode0_source']['exact_text'] in code
    caller = selected[3]['record']['code']
    assert '*(undefined8 *)(param_1 + 0xe0028),param_2,param_3,' in caller
    assert '*(code **)((long)pvVar1 + 0x50) = FUN_0000b758;' in selected[1]['record']['code']
    mode = selected[2]['record']['code']
    assert 'plVar4 = (long *)*param_3;' in mode and 'lVar5 = *plVar4;' in mode
    assert 'FUN_0000e4cc(lVar5 + 0xe8,uVar3)' in mode
    assert 'FUN_0000e714(param_1 + 0x60,uVar2)' in mode
    for path, before in watch.items():
        assert Path(path).read_bytes() == before
    return dict(status='PASS: bounded bytes/source data only', selected_render_bytes=188,
                selected_render_words=47, reused_b758_bytes=56, reused_b758_words=14,
                old_pointer_targets=pointers, independently_rejected=rejected,
                source_rows=source_rows, source_pointer_associations=5,
                exact_call_metadata_rows=1, bounded_numeric_marker_matches=matches,
                watch_paths=len(watch), unchanged=True,
                uninspected_branch='9348 nonzero ->93f0; no all-path continuity proof',
                normal_ABI_and_source_alignment='explicit assumptions, not code executed or helper certification',
                native_calls=0, source_execution=0, new_requirements=0, grade=None)


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
