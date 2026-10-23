#!/usr/bin/env python3
"""Four fixed x86 linker-start nominations; metadata only, no instructions/decoder."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SELECTED = (0x101ac8330, 0x101acf4c0, 0x101acf650, 0x102247e80)
U64 = (1 << 64) - 1
SELECTION_SHA = 'fd34700cb6d90dc2d5af4e866b754c3edace3a198edef0434c65c29dc8fb9a01'

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
         'exact four selected entries required')
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


def selection():
    data = (HERE/'selection.json').read_bytes()
    need(sha(data) == SELECTION_SHA, 'fixed candidate selection changed')
    plan = json.loads(data)
    need(tuple(int(x,16) for x in plan['selected_entries']) == SELECTED, 'fixed four nominations')
    need(plan['metadata_read_ranges'] == [dict(file_offset=0,bytes=32),dict(file_offset=32,bytes=6832),dict(file_offset=147556352,bytes=559744)] and plan['metadata_read_limit'] == 566608, 'exact metadata read budget')
    for pin in plan['immutable']:
        pin_bytes((ROOT/pin['path']).read_bytes(),pin)
    return plan


def local_rows(rows, info):
    total = validate_rows(rows)
    for row in rows:
        for item in (row['entry'],row['next_start']):
            need(type(item['index']) is int and item['index'] >= 0, 'nonnegative source ordinal')
            need(0 <= item['uleb_blob_offset'] < info['function_starts']['datasize'], 'ULEB metadata table bounds')
            need(item['uleb_blob_offset']+len(bytes.fromhex(item['uleb_hex'])) <= info['function_starts']['datasize'], 'ULEB metadata witness end')
            need(item['uleb_file_offset'] == info['function_starts']['dataoff']+item['uleb_blob_offset'], 'ULEB source file offset')
            need(item['slice_file_offset'] == info['text']['fileoff']+int(item['address'],16)-info['text']['vmaddr'], 'selected physical file offset')
            section = info['text_section']
            need(section['vmaddr'] <= int(item['address'],16) < section['vmaddr']+section['bytes'], 'selected text section bound')
    return total


def encode(value):
    result = []
    while value >= 128:
        result.append((value & 127) | 128)
        value >>= 7
    return bytes(result+[value])


def synthetic(plan):
    retained = json.loads((ROOT/plan['header_map']['path']).read_text())
    info = header(bytes.fromhex(retained['header_hex']),bytes.fromhex(retained['load_commands_hex']),retained['image']['bytes'])
    need(info['load_command_count'] == 54 and info['load_command_bytes'] == 6832 and info['function_starts']['dataoff'] == 147556352 and info['function_starts']['datasize'] == 559744, 'selected retained header metadata spans')
    addresses = sorted([value for entry in SELECTED for value in (entry,entry+16)])
    previous, parts = info['text']['vmaddr'], []
    for address in addresses:
        parts.append(encode(address-previous)); previous = address
    rows, table = selected_rows(b''.join(parts)+b'\x00',info)
    need(local_rows(rows,info) == 64 and table['parsed_start_count'] == 8, 'four synthetic source ordinals and caps')
    controls = []
    def rejects(name,operation):
        try: operation()
        except (ValueError,KeyError,struct.error): controls.append(dict(name=name,result='rejected'))
        else: raise ValueError('negative accepted: '+name)
    bad=copy.deepcopy(rows);bad.pop();rejects('missing selected entry',lambda:local_rows(bad,info))
    for name,part,key,value in [('non-immediate next ordinal','next_start','index',4),('bad source file offset','entry','uleb_file_offset',0),('bad image file offset','entry','slice_file_offset',0),('outside table witness','entry','uleb_blob_offset',559744),('bad cap','next_start','address','0x101ac8341')]:
        altered=copy.deepcopy(rows);altered[0][part][key]=value
        rejects(name,lambda altered=altered:local_rows(altered,info))
    def with_bound(row,length):
        row['physical_bound_bytes']=length
        row['next_start']['address']=hex(int(row['entry']['address'],16)+length)
        row['next_start']['uleb_hex']=encode(length).hex()
    over=copy.deepcopy(rows);with_bound(over[0],8193)
    rejects('coherent per-range proposal cap overflow',lambda:validate_rows(over))
    aggregate=copy.deepcopy(rows)
    for index in [0,2,3]:with_bound(aggregate[index],8192)
    rejects('coherent aggregate proposal cap overflow',lambda:validate_rows(aggregate))
    rejects('truncated ULEB',lambda:uleb(b'\x80',0))
    rejects('noncanonical ULEB',lambda:uleb(b'\x81\x00',0))
    rejects('uint64 overflow ULEB',lambda:uleb(b'\xff'*9+b'\x02',0))
    raw=bytearray.fromhex(retained['header_hex']);raw[4]=12
    rejects('ARM header',lambda:header(bytes(raw),bytes.fromhex(retained['load_commands_hex']),retained['image']['bytes']))
    cmds=bytearray.fromhex(retained['load_commands_hex']);cmds[4:8]=(7).to_bytes(4,'little')
    rejects('invalid command size',lambda:header(bytes.fromhex(retained['header_hex']),bytes(cmds),retained['image']['bytes']))
    tiny=dict(text=dict(vmaddr=0,filesize=100,fileoff=0),text_section=dict(vmaddr=0,bytes=100,fileoff=0),function_starts=dict(dataoff=0))
    rejects('nonzero data after terminator',lambda:selected_rows(b'\x01\x00\x01',tiny))
    rejects('missing table terminator',lambda:selected_rows(b'\x01',tiny))
    odd,oddtable=selected_rows(b'\x01\x02\x00',tiny)
    need(odd == [] and oddtable['parsed_start_count'] == 2,'odd x86 starts accepted')
    overflow=copy.deepcopy(tiny);overflow['text']['vmaddr']=U64
    rejects('cumulative address overflow',lambda:selected_rows(b'\x01\x00',overflow))
    rejects('source pin corruption',lambda:pin_bytes(b'a',dict(bytes=1,sha256='0'*64)))
    return dict(status='PASS',synthetic_negative_controls=controls,synthetic_positive='Four exact synthetic selected rows with absolute ordinals/local ULEB witnesses; odd x86 starts accepted.',source_pins=len(plan['immutable']),image_opened=False,decoder_run=False,collector_called=False)


def collect():
    plan=selection()
    need(sys.dont_write_bytecode, 'requires -B')
    ready=json.loads((HERE/'source-preflight.json').read_text())
    need(ready['collector_sha256'] == sha(Path(__file__).read_bytes()) and ready['selection_sha256'] == SELECTION_SHA and ready['synthetic_check']['status'] == 'PASS', 'same-source pre-acquisition synthetic preflight required')
    need(not (HERE/'metadata.json').exists(), 'metadata already frozen')
    retained=json.loads((ROOT/plan['header_map']['path']).read_text())
    state=dict(started_utc=datetime.now(timezone.utc).isoformat(),collector_sha256=sha(Path(__file__).read_bytes()),selection_sha256=SELECTION_SHA,source_preflight_sha256=sha((HERE/'source-preflight.json').read_bytes()),image_reads=[],metadata_bytes_read=0,instruction_window_reads=0,decoder_children=0,original_executions=0)
    write('attempt.json',state)
    image=Path(plan['image']['path'])
    try:
        before=image.stat();need(before.st_size == plan['image']['bytes'],'image size changed')
        with image.open('rb') as stream:
            def read_at(offset,length,role):
                need(state['metadata_bytes_read']+length <= 566608,'metadata read budget')
                stream.seek(offset);data=stream.read(length)
                state['image_reads'].append(dict(file_offset=offset,bytes=len(data),role=role))
                state['metadata_bytes_read'] += len(data)
                need(len(data) == length,'short metadata read')
                return data
            raw=read_at(0,32,'Mach-O header');need(raw.hex() == retained['header_hex'],'header changed')
            need(struct.unpack('<8I',raw)[5] == 6832,'bounded load commands')
            commands=read_at(32,6832,'load commands');need(commands.hex() == retained['load_commands_hex'],'load commands changed')
            info=header(raw,commands,before.st_size)
            cmd=info['function_starts'];need((cmd['dataoff'],cmd['datasize']) == (147556352,559744),'exact selected metadata table')
            blob=read_at(147556352,559744,'LC_FUNCTION_STARTS metadata')
        after=image.stat();fields=('st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns')
        need(all(getattr(before,k) == getattr(after,k) for k in fields),'image stat changed')
        rows,table=selected_rows(blob,info);total=local_rows(rows,info)
        result=dict(schema='utility-x86-four-wrapper-frontier-starts-v1',status='metadata-only-pending-independent-review',utc=datetime.now(timezone.utc).isoformat(),inherited_full_image_pin=plan['image'],full_image_rehashed=False,stat_before_after={k:getattr(before,k) for k in fields},header=info,table=dict(**table,sha256=sha(blob)),rows=rows,physical_bounds_total_bytes=total,**state,finished_utc=datetime.now(timezone.utc).isoformat(),all_six_public_bridges='unknown',application_U=38,new_grades=0)
        scope(result);write('metadata.json',result)
    except BaseException as failure:
        write('failure.json',dict(**state,error=type(failure).__name__+': '+str(failure),automatic_retry=False))
        raise


def check():
    plan=selection();result=synthetic(plan)
    x=json.loads((HERE/'metadata.json').read_text())
    retained=json.loads((ROOT/plan['header_map']['path']).read_text())
    info=header(bytes.fromhex(retained['header_hex']),bytes.fromhex(retained['load_commands_hex']),plan['image']['bytes'])
    need(x['header'] == info,'retained metadata header association')
    need(local_rows(x['rows'],info) == x['physical_bounds_total_bytes'],'retained caps')
    need(x['inherited_full_image_pin'] == plan['image'],'inherited full image pin')
    need(x['metadata_bytes_read'] == 566608 and [{k:r[k] for k in ('file_offset','bytes')} for r in x['image_reads']] == plan['metadata_read_ranges'],'exact recorded metadata reads')
    need(x['collector_sha256'] == sha(Path(__file__).read_bytes()) and x['selection_sha256'] == SELECTION_SHA,'acquisition source chronology')
    need(x['source_preflight_sha256'] == sha((HERE/'source-preflight.json').read_bytes()),'pre-acquisition preflight receipt')
    scope(x)
    result.update(selected_entries=4,physical_bound_bytes=x['physical_bounds_total_bytes'],metadata_receipt_checked=True,absolute_source_ordinal_limit='Checker checks retained associations and acquisition table digest/ordinal receipt; only the acquisition traversal established absolute source membership, no source table replay.')
    return result


if __name__ == '__main__':
    need(len(sys.argv) == 2 and sys.argv[1] in ['--check-synthetic','--check','--read-selected-metadata'],'choose exactly one fixed action')
    if sys.argv[1] == '--read-selected-metadata': collect()
    else: print(json.dumps(synthetic(selection()) if sys.argv[1] == '--check-synthetic' else check(),indent=2))
