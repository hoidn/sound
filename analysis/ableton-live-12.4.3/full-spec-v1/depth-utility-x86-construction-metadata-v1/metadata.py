#!/usr/bin/env python3
"""Exactly three x86 linker-start nominations; no instruction reads or decoding."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SELECTED = (0x101ad08a0, 0x1022313c0, 0x102231400)
U64 = (1 << 64) - 1


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin_bytes(data, pin):
    need(len(data) == pin['bytes'] and sha(data) == pin['sha256'], 'source pin changed')


def scope(x):
    need(x['all_six_public_bridges'] == 'unknown' and x['application_U'] == 38
         and x['new_grades'] == 0 and not x['full_image_rehashed']
         and x['instruction_window_reads'] == x['decoder_children'] == x['original_executions'] == 0,
         'scope or false promotion')


def write(name, value):
    with (HERE / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def uleb(data, offset):
    value = 0
    for i in range(10):
        need(offset < len(data), 'truncated ULEB')
        byte = data[offset]
        offset += 1
        need(i != 9 or byte <= 1, 'ULEB overflow')
        value |= (byte & 127) << (7 * i)
        if not byte & 128:
            need(i == 0 or byte != 0, 'noncanonical ULEB')
            return value, offset
    raise ValueError('overlong ULEB')


def header(raw, commands, image_size):
    need(len(raw) == 32, 'header length')
    magic, cpu, subtype, kind, count, size, _, reserved = struct.unpack('<8I', raw)
    need((magic, cpu, subtype, kind, reserved) ==
         (0xfeedfacf, 0x1000007, 3, 2, 0), 'requires selected x86_64 MH_EXECUTE')
    need(size == len(commands) and count <= size // 8, 'command region/count')
    segments, starts, text_sections, offset = [], [], [], 0
    for index in range(count):
        need(offset + 8 <= size, 'command header bounds')
        cmd, length = struct.unpack_from('<II', commands, offset)
        need(length >= 8 and length % 8 == 0 and offset + length <= size,
             'command size/bounds')
        if cmd == 0x19:
            need(length >= 72, 'segment length')
            _, _, name, vm, vmsize, fileoff, filesize, maximum, initial, nsects, _ = \
                struct.unpack_from('<II16sQQQQiiII', commands, offset)
            need(length == 72 + 80 * nsects, 'segment section count')
            need(vm + vmsize <= U64 and filesize <= vmsize and
                 fileoff + filesize <= image_size and initial & ~maximum == 0,
                 'segment bounds/protections')
            segments.append(dict(name=name.split(b'\0', 1)[0].decode('ascii'),
                                 vmaddr=vm, vmsize=vmsize, fileoff=fileoff,
                                 filesize=filesize, initprot=initial))
            for section_index in range(nsects):
                section_offset = offset + 72 + 80 * section_index
                section_name, segment_name, section_va, section_size, section_fileoff = \
                    struct.unpack_from('<16s16sQQI', commands, section_offset)
                if section_name.rstrip(b'\0') == b'__text' and segment_name.rstrip(b'\0') == b'__TEXT':
                    need(vm <= section_va and section_va + section_size <= vm + vmsize
                         and fileoff <= section_fileoff
                         and section_fileoff + section_size <= fileoff + filesize,
                         'text section bounds')
                    text_sections.append(dict(vmaddr=section_va, bytes=section_size,
                                              fileoff=section_fileoff,
                                              section_header_file_offset=32 + section_offset))
        elif cmd == 0x26:
            need(length == 16, 'function-start command size')
            _, _, dataoff, datasize = struct.unpack_from('<4I', commands, offset)
            need(0 < datasize <= image_size - dataoff, 'function-start payload bounds')
            starts.append(dict(command_index=index, command_file_offset=32 + offset,
                               command_hex=commands[offset:offset + length].hex(),
                               dataoff=dataoff, datasize=datasize))
        offset += length
    need(offset == size and len(starts) == 1, 'unique function-start command')
    texts = [s for s in segments if s['name'] == '__TEXT']
    command = starts[0]
    links = [s for s in segments if s['name'] == '__LINKEDIT' and
             s['fileoff'] <= command['dataoff'] and
             command['dataoff'] + command['datasize'] <= s['fileoff'] + s['filesize']]
    need(len(texts) == len(links) == len(text_sections) == 1, 'unique TEXT/text/LINKEDIT mapping')
    need(texts[0]['initprot'] & 4, 'TEXT executable metadata')
    return dict(header_hex=raw.hex(), load_command_count=count,
                load_command_bytes=size, load_commands_sha256=sha(commands),
                text=texts[0], text_section=text_sections[0],
                linkedit=links[0], function_starts=command)


def selected_rows(blob, info):
    address, offset, count, pending = info['text']['vmaddr'], 0, 0, None
    kept = []
    while offset < len(blob):
        start, previous = offset, address
        delta, offset = uleb(blob, offset)
        if delta == 0:
            need(not any(blob[offset:]), 'nonzero terminator padding')
            need(pending is None, 'selected entry has no successor')
            return kept, dict(parsed_start_count=count, terminator_blob_offset=start,
                              padding_bytes=len(blob) - offset)
        need(delta <= U64 - address, 'cumulative address overflow')
        address += delta
        t = info['text']
        need(t['vmaddr'] <= address < t['vmaddr'] + t['filesize'], 'start outside file-backed TEXT')
        row = dict(index=count, address=hex(address), previous_address=hex(previous),
                   uleb_blob_offset=start,
                   uleb_file_offset=info['function_starts']['dataoff'] + start,
                   uleb_hex=blob[start:offset].hex(),
                   slice_file_offset=t['fileoff'] + address - t['vmaddr'])
        if pending is not None:
            section = info['text_section']
            need(section['vmaddr'] <= address <= section['vmaddr'] + section['bytes'],
                 'selected successor outside text section')
            pending['next_start'] = row
            pending['physical_bound_bytes'] = address - int(pending['entry']['address'], 16)
            kept.append(pending)
            pending = None
        if address in SELECTED:
            section = info['text_section']
            need(section['vmaddr'] <= address < section['vmaddr'] + section['bytes'],
                 'selected entry outside text section')
            pending = dict(entry=row)
        count += 1
    raise ValueError('missing terminator')


def validate_rows(rows):
    need(tuple(int(r['entry']['address'], 16) for r in rows) == SELECTED,
         'exact three selected entries required')
    total = 0
    previous_end = 0
    for row in rows:
        entry, nxt = row['entry'], row['next_start']
        for item in (entry, nxt):
            data = bytes.fromhex(item['uleb_hex'])
            delta, end = uleb(data, 0)
            need(end == len(data) and delta > 0 and
                 int(item['previous_address'], 16) + delta == int(item['address'], 16),
                 'selected ULEB/address association')
        need(nxt['index'] == entry['index'] + 1 and
             nxt['uleb_blob_offset'] == entry['uleb_blob_offset'] + len(bytes.fromhex(entry['uleb_hex'])) and
             nxt['previous_address'] == entry['address'], 'immediate successor association')
        length = int(nxt['address'], 16) - int(entry['address'], 16)
        need(0 < length <= 8192 and length == row['physical_bound_bytes'], 'per-range cap')
        need(previous_end <= int(entry['address'], 16), 'selected physical bounds overlap')
        previous_end = int(nxt['address'], 16)
        total += length
    need(total <= 16384, 'aggregate cap')
    return total


def collect():
    """Explicit metadata-only one-shot; never called by check()."""
    need(not (HERE / 'metadata.json').exists(), 'output already frozen')
    pins = json.loads((HERE / 'pins.json').read_text())
    retained = json.loads((ROOT / pins['header_map']['path']).read_text())
    image = Path(retained['image']['path'])
    before = image.stat()
    need(before.st_size == retained['image']['bytes'], 'image size changed')
    with image.open('rb') as stream:
        raw = stream.read(32)
        need(raw.hex() == retained['header_hex'], 'header changed')
        size = struct.unpack('<8I', raw)[5]
        need(size == 6832, 'selected command-byte bound')
        commands = stream.read(size)
        need(commands.hex() == retained['load_commands_hex'], 'commands changed')
        info = header(raw, commands, before.st_size)
        cmd = info['function_starts']
        need((cmd['dataoff'], cmd['datasize']) == (147556352, 559744), 'selected metadata span')
        stream.seek(cmd['dataoff'])
        blob = stream.read(cmd['datasize'])
        need(len(blob) == cmd['datasize'], 'short metadata table')
    after = image.stat()
    stat_fields = ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    need(all(getattr(before, k) == getattr(after, k) for k in stat_fields), 'image stat changed')
    rows, table = selected_rows(blob, info)
    total = validate_rows(rows)
    write('metadata.json', dict(schema='utility-x86-three-construction-starts-v1',
          status='frozen-metadata-only-pending-independent-review',
          utc=datetime.now(timezone.utc).isoformat(),
          inherited_full_image_pin=retained['image'], full_image_rehashed=False,
          stat_before_after={k: getattr(before, k) for k in stat_fields},
          header=info, table=dict(**table, sha256=sha(blob)), rows=rows,
          physical_bounds_total_bytes=total,
          image_reads=[dict(file_offset=0, bytes=32, role='Mach-O header'),
                       dict(file_offset=32, bytes=size, role='load commands'),
                       dict(file_offset=cmd['dataoff'], bytes=len(blob), role='LC_FUNCTION_STARTS metadata')],
          instruction_window_reads=0, decoder_children=0, original_executions=0,
          all_six_public_bridges='unknown', application_U=38, new_grades=0))


def check():
    pins = json.loads((HERE / 'pins.json').read_text())
    for pin in pins['immutable']:
        data = (ROOT / pin['path']).read_bytes()
        pin_bytes(data, pin)
    x = json.loads((HERE / 'metadata.json').read_text())
    total = validate_rows(x['rows'])
    retained = json.loads((ROOT / pins['header_map']['path']).read_text())
    info = header(bytes.fromhex(retained['header_hex']),
                  bytes.fromhex(retained['load_commands_hex']), retained['image']['bytes'])
    need(info == x['header'], 'retained header relationship')
    need(x['inherited_full_image_pin'] == retained['image'] and not x['full_image_rehashed'],
         'inherited identity qualification')
    for row in x['rows']:
        for item in (row['entry'], row['next_start']):
            need(item['uleb_file_offset'] == info['function_starts']['dataoff'] + item['uleb_blob_offset'],
                 'table file locator')
            need(item['slice_file_offset'] == info['text']['fileoff'] + int(item['address'], 16) - info['text']['vmaddr'],
                 'TEXT file locator')
            section = info['text_section']
            need(section['vmaddr'] <= int(item['address'], 16) < section['vmaddr'] + section['bytes'],
                 'selected entry/successor inside text section')
    need(x['physical_bounds_total_bytes'] == total, 'physical total')
    scope(x)
    controls = []
    def rejects(name, operation):
        try:
            operation()
        except (ValueError, KeyError):
            controls.append(dict(name=name, result='rejected'))
        else:
            raise ValueError('negative control accepted: ' + name)
    bad = copy.deepcopy(x['rows']); bad.pop()
    rejects('missing selected entry', lambda: validate_rows(bad))
    bad2 = copy.deepcopy(x['rows']); bad2[0]['next_start']['index'] += 1
    rejects('non-immediate next start', lambda: validate_rows(bad2))
    bad3 = copy.deepcopy(x['rows']); bad3[0]['physical_bound_bytes'] = 8193
    rejects('wrong or oversized physical bound', lambda: validate_rows(bad3))
    def with_bound(row, length):
        row['physical_bound_bytes'] = length
        row['next_start']['address'] = hex(int(row['entry']['address'], 16) + length)
        encoded, value = [], length
        while value >= 128:
            encoded.append((value & 127) | 128)
            value >>= 7
        row['next_start']['uleb_hex'] = bytes(encoded + [value]).hex()
    over = copy.deepcopy(x['rows']); with_bound(over[0], 8193)
    rejects('coherent per-range cap overflow', lambda: validate_rows(over))
    aggregate = copy.deepcopy(x['rows']); with_bound(aggregate[0], 8192); with_bound(aggregate[2], 8192)
    rejects('coherent aggregate cap overflow', lambda: validate_rows(aggregate))
    rejects('truncated ULEB', lambda: uleb(b'\x80', 0))
    rejects('noncanonical ULEB', lambda: uleb(b'\x81\x00', 0))
    rejects('uint64 overflow ULEB', lambda: uleb(b'\xff' * 9 + b'\x02', 0))
    raw = bytearray.fromhex(retained['header_hex']); raw[4] = 12
    rejects('ARM64 header used as x86', lambda: header(bytes(raw), bytes.fromhex(retained['load_commands_hex']), retained['image']['bytes']))
    badcmd = bytearray.fromhex(retained['load_commands_hex']); badcmd[4:8] = (7).to_bytes(4, 'little')
    rejects('invalid command size', lambda: header(bytes.fromhex(retained['header_hex']), bytes(badcmd), retained['image']['bytes']))
    tinyinfo = dict(text=dict(vmaddr=0, filesize=100, fileoff=0),
                    text_section=dict(vmaddr=0, bytes=100, fileoff=0),
                    function_starts=dict(dataoff=0))
    rejects('nonzero data after terminator', lambda: selected_rows(b'\x01\x00\x01', tinyinfo))
    rejects('missing table terminator', lambda: selected_rows(b'\x01', tinyinfo))
    odd, odd_table = selected_rows(b'\x01\x02\x00', tinyinfo)
    need(odd == [] and odd_table['parsed_start_count'] == 2, 'x86 odd-byte starts rejected')
    overflow_info = copy.deepcopy(tinyinfo); overflow_info['text']['vmaddr'] = U64
    rejects('cumulative address overflow', lambda: selected_rows(b'\x01\x00', overflow_info))
    witness = b'pin-control'
    rejects('source digest corruption', lambda: pin_bytes(witness + b'!', dict(bytes=len(witness) + 1, sha256=sha(witness))))
    promotion = copy.deepcopy(x); promotion['all_six_public_bridges'] = 'answered'
    rejects('metadata promoted to public binding', lambda: scope(promotion))
    rehashed = copy.deepcopy(x); rehashed['full_image_rehashed'] = True
    rejects('inherited full-image pin called fresh', lambda: scope(rehashed))
    return dict(status='PASS', source_pins=len(pins['immutable']), selected_entries=3,
                physical_bound_bytes=total, negative_controls=controls,
                positive_control='x86 starts at odd addresses 1 and 3 accepted as metadata',
                image_opened=False, decoder_run=False, collector_called=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--read-selected-metadata', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    need(args.read_selected_metadata != args.check, 'choose exactly one action')
    if args.read_selected_metadata:
        collect()
    else:
        print(json.dumps(check(), indent=2))
