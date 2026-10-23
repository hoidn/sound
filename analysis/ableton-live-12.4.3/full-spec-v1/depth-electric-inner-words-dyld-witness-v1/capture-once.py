#!/usr/bin/env python3
"""Fixed Electric static capture; self-test and --check are owned-data-only."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import struct
import sys

HERE = Path(__file__).resolve().parent
IMAGE = Path('/var/tmp/sound-analysis/helpers/Electric/Electric.arm64')
IMAGE_SIZE = 265920
IMAGE_SHA = 'fcf490a084b755ba6a045abe9df990f72f52051805554e48e3176c9c246de8db'
WORDS = [0x300c0, 0x300e8, 0x30100, 0x30108, 0x30110, 0x30118]
COMMANDS = [0x19]*4 + [0x80000022, 2, 0xb, 0x1b, 0x32, 0x2a, 0xc, 0xc, 0x26, 0x29, 0x1d]
STREAMS = ['rebase', 'bind', 'weak_bind', 'lazy_bind']

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def identity(path):
    h = hashlib.sha256()
    size = 0
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            size += len(block)
            h.update(block)
    return {'path': str(path), 'bytes': size, 'sha256': h.hexdigest()}

def put(path, data):
    with open(path, 'xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

def put_json(path, data):
    put(path, (json.dumps(data, indent=2) + '\n').encode())

def header(data):
    require(len(data) == 32, 'header length')
    fields = struct.unpack('<8I', data)
    magic, cpu, subtype, ft, count, size, flags, reserved = fields
    require(magic == 0xfeedfacf, 'magic/endian')
    require(cpu == 0x100000c and ft == 8, 'CPU/filetype')
    require(count == len(COMMANDS), 'command count')
    require(size % 8 == 0 and count * 8 <= size and 32 + size <= 0x3d74, 'table bounds/alignment')
    return dict(zip(['magic', 'cpu', 'subtype', 'filetype', 'ncmds', 'sizeofcmds', 'flags', 'reserved'], fields))

def interval(off, size, lower, upper, label):
    require(0 <= off <= IMAGE_SIZE and 0 <= size <= IMAGE_SIZE - off, label + ' image bounds')
    if size:
        require(lower <= off and off + size <= upper, label + ' LINKEDIT bounds')
    return (off, off + size)

def overlaps(a, b):
    return a[0] < a[1] and b[0] < b[1] and max(a[0], b[0]) < min(a[1], b[1])

def geometry(h, table):
    require(len(table) == h['sizeofcmds'], 'table length')
    cursor, commands, segments, dyld = 0, [], [], None
    for ordinal in range(h['ncmds']):
        require(cursor + 8 <= len(table), 'command header crossing')
        cmd, size = struct.unpack_from('<2I', table, cursor)
        require(size >= 8 and size % 8 == 0 and cursor + size <= len(table), 'command size/crossing')
        require(cmd == COMMANDS[ordinal], 'unexpected command/encoding sequence')
        record = {'ordinal': ordinal, 'file_offset': 32+cursor, 'command': cmd, 'bytes': size}
        if cmd == 0x19:
            require(size >= 72, 'segment size')
            name, vmaddr, vmsize, fileoff, filesize, maxprot, initprot, nsects, flags = struct.unpack_from('<16s4Q4I', table, cursor+8)
            require(nsects <= (size-72)//80 and size == 72 + 80*nsects, 'section count/size')
            require(fileoff <= IMAGE_SIZE and filesize <= IMAGE_SIZE-fileoff, 'segment file bounds')
            sections = []
            for j in range(nsects):
                p = cursor + 72 + j*80
                sn, sg, addr, ss, offset = struct.unpack_from('<16s16sQQI', table, p)
                sections.append({'name': sn.rstrip(b'\0').decode('ascii'), 'segment': sg.rstrip(b'\0').decode('ascii'), 'address': addr, 'bytes': ss, 'file_offset': offset})
            record['segment'] = {'name': name.rstrip(b'\0').decode('ascii'), 'vmaddr': vmaddr, 'vmsize': vmsize, 'fileoff': fileoff, 'filesize': filesize, 'sections': sections}
            segments.append(record['segment'])
        if cmd == 0x80000022:
            require(size == 48 and dyld is None, 'DYLD_INFO_ONLY size/duplicate')
            fields = struct.unpack_from('<10I', table, cursor+8)
            dyld = {name: {'file_offset': fields[2*i], 'bytes': fields[2*i+1]} for i, name in enumerate(STREAMS+['exports_excluded'])}
            record['declared_ranges'] = dyld
        commands.append(record)
        cursor += size
    require(cursor == len(table) and dyld is not None, 'table coverage/encoding')
    require([s['name'] for s in segments] == ['__TEXT', '__DATA_CONST', '__DATA', '__LINKEDIT'], 'segment sequence')
    text = next(x for x in segments[0]['sections'] if x['name'] == '__text')
    const = next(x for x in segments[1]['sections'] if x['name'] == '__const')
    require(text['address'] == text['file_offset'] == 0x3d74 and text['bytes'] == 152672, 'retained text mapping')
    require(const['address'] == const['file_offset'] == 0x300a0 and const['bytes'] == 5752, 'retained word mapping')
    for word in WORDS:
        require(const['address'] <= word and word+8 <= const['address']+const['bytes'], 'word section bounds')
        require(segments[1]['fileoff'] <= word and word+8 <= segments[1]['fileoff']+segments[1]['filesize'], 'word file mapping')
    link = segments[3]
    require(link['vmaddr'] == 0x38000 and link['vmsize'] == 49152 and link['filesize'] <= 49152, 'retained LINKEDIT bounds')
    lo, hi = link['fileoff'], link['fileoff']+link['filesize']
    intervals = {name: interval(r['file_offset'], r['bytes'], lo, hi, name) for name, r in dyld.items()}
    require(sum(dyld[n]['bytes'] for n in STREAMS) <= 49152, 'combined stream cap')
    names = list(intervals)
    for i, name in enumerate(names):
        for other in names[i+1:]:
            require(not overlaps(intervals[name], intervals[other]), 'stream/export overlap')
    for name in STREAMS:
        for excluded in [(0, 32+len(table))]+[(x, x+8) for x in WORDS]:
            require(not overlaps(intervals[name], excluded), 'stream selected-range crossing')
    return {'commands': commands, 'segments': segments, 'streams': dyld, 'stream_bytes': sum(dyld[n]['bytes'] for n in STREAMS)}

def projected(h, g, raws):
    require(set(raws) == set(STREAMS), 'stream names')
    for name in STREAMS:
        require(len(raws[name]) == g['streams'][name]['bytes'], 'stream length ' + name)
    return {'header': h, 'geometry': g, 'stream_witnesses': {n: {'bytes': len(raws[n]), 'sha256': digest(raws[n])} for n in STREAMS}, 'stream_opcodes_decoded': False, 'runtime_bindings_proved': False}

def synthetic():
    def seg(name, va, vs, off, fs, sections):
        b = struct.pack('<2I16s4Q4I', 0x19, 72+80*len(sections), name.encode(), va, vs, off, fs, 7, 3, len(sections), 0)
        for sn, addr, sz, so in sections:
            b += struct.pack('<16s16sQQ8I', sn.encode(), name.encode(), addr, sz, so, 0, 0, 0, 0, 0, 0, 0)
        return b
    chunks = [seg('__TEXT', 0, 196608, 0, 196608, [('__text', 0x3d74, 152672, 0x3d74)]), seg('__DATA_CONST', 0x30000, 16384, 196608, 16384, [('__const', 0x300a0, 5752, 0x300a0)]), seg('__DATA', 0x34000, 16384, 212992, 16384, []), seg('__LINKEDIT', 0x38000, 49152, 229376, 36544, []), struct.pack('<12I', 0x80000022, 48, 229376, 8, 229384, 8, 0, 0, 229392, 8, 229400, 8)]
    chunks += [struct.pack('<2I', cmd, 8) for cmd in COMMANDS[5:]]
    table = b''.join(chunks)
    hdr = struct.pack('<8I', 0xfeedfacf, 0x100000c, 0, 8, 15, len(table), 0, 0)
    return hdr, table, sum(len(x) for x in chunks[:4])

def self_test():
    hb, tb, dp = synthetic()
    h = header(hb)
    g = geometry(h, tb)
    require(g['stream_bytes'] == 24, 'positive synthetic')
    tests = []
    def reject(name, hh=hb, tt=tb, projection=False):
        try:
            if projection:
                projected(h, g, {n: b'' for n in STREAMS})
            else:
                geometry(header(hh), tt)
        except (ValueError, StopIteration, UnicodeError, struct.error):
            tests.append(name)
            return
        raise AssertionError('negative accepted: '+name)
    def word(data, at, value):
        b = bytearray(data)
        struct.pack_into('<I', b, at, value)
        return bytes(b)
    reject('short header', hh=hb[:-1])
    reject('wrong magic', hh=word(hb, 0, 0xcffaedfe))
    reject('wrong CPU', hh=word(hb, 4, 7))
    reject('wrong filetype', hh=word(hb, 12, 2))
    reject('count mismatch', hh=word(hb, 16, 16))
    reject('table cap', hh=word(hb, 20, 0x3d74))
    reject('unaligned table', hh=word(hb, 20, len(tb)-1))
    reject('truncated table', tt=tb[:-1])
    reject('command crossing', tt=word(tb, 4, len(tb)+8))
    reject('command alignment', tt=word(tb, 4, 73))
    reject('section count crossing', tt=word(tb, 64, 100))
    reject('unexpected chained encoding', tt=word(tb, dp, 0x80000034))
    reject('DYLD command length', tt=word(tb, dp+4, 40))
    reject('stream image crossing', tt=word(tb, dp+8, IMAGE_SIZE-1))
    reject('stream outside LINKEDIT', tt=word(tb, dp+8, 200000))
    reject('stream overlap', tt=word(tb, dp+16, 229376))
    reject('export overlap', tt=word(tb, dp+40, 229376))
    reject('raw stream truncation', projection=True)
    zero = tb
    for at in range(dp+8, dp+48, 8):
        zero = word(zero, at, 0)
        zero = word(zero, at+4, 0)
    zg = geometry(h, zero)
    projected(h, zg, {n: b'' for n in STREAMS})
    return {'positive_geometry': True, 'zero_streams': True, 'rejected_controls': tests, 'count': len(tests), 'image_or_original_access': False}

def capture():
    pre = json.loads((HERE/'pre-call-manifest.json').read_text())
    require(pre['custody'][0] == {'path': str(IMAGE), 'bytes': IMAGE_SIZE, 'sha256': IMAGE_SHA}, 'fixed image identity')
    out = HERE/'capture'
    out.mkdir(exist_ok=False)
    receipt = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'pid': os.getpid(), 'argv': sys.argv, 'reads': [], 'status': 'INCOMPLETE', 'original_execution': 0, 'decoder_children': 0, 'automatic_retry': False}
    try:
        before = [identity(Path(x['path'])) for x in pre['custody']]
        receipt['before'] = before
        require(before == pre['custody'], 'before custody mismatch')
        with open(IMAGE, 'rb') as f:
            def read(name, offset, size):
                f.seek(offset)
                data = f.read(size)
                put(out/name, data)
                receipt['reads'].append({'file': name, 'file_offset': offset, 'requested_bytes': size, 'bytes': len(data), 'sha256': digest(data)})
                require(len(data) == size, 'short read '+name)
                return data
            hb = read('header.bin', 0, 32)
            h = header(hb)
            tb = read('load-commands.bin', 32, h['sizeofcmds'])
            g = geometry(h, tb)
            raws = {n: read(n+'.bin', g['streams'][n]['file_offset'], g['streams'][n]['bytes']) for n in STREAMS}
            words = []
            for address in WORDS:
                b = read('word-'+format(address, 'x')+'.bin', address, 8)
                words.append({'virtual_address': hex(address), 'file_offset': address, 'raw_hex': b.hex(), 'little_endian_u64': struct.unpack('<Q', b)[0]})
            result = projected(h, g, raws)
            result['selected_words'] = words
            put_json(out/'projection.json', result)
        after = [identity(Path(x['path'])) for x in pre['custody']]
        receipt['after'] = after
        require(after == before, 'after custody mismatch')
        receipt['status'] = 'PASS_STATIC_CAPTURE'
    except Exception as e:
        receipt['failure'] = type(e).__name__+': '+str(e)
    receipt['ended_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    put_json(out/'receipt.json', receipt)
    print(json.dumps({'status': receipt['status'], 'reads': len(receipt['reads']), 'bytes': sum(x['bytes'] for x in receipt['reads']), 'failure': receipt.get('failure')}))
    return 0 if receipt['status'] == 'PASS_STATIC_CAPTURE' else 1

def check():
    pre = json.loads((HERE/'pre-call-manifest.json').read_text())
    out = HERE/'capture'
    receipt = json.loads((out/'receipt.json').read_text())
    require(receipt['status'] == 'PASS_STATIC_CAPTURE', 'capture status')
    require(receipt['before'] == receipt['after'] == pre['custody'], 'recorded custody')
    require(receipt['original_execution'] == receipt['decoder_children'] == 0 and not receipt['automatic_retry'], 'execution scope')
    h = header((out/'header.bin').read_bytes())
    g = geometry(h, (out/'load-commands.bin').read_bytes())
    raw = {n: (out/(n+'.bin')).read_bytes() for n in STREAMS}
    result = projected(h, g, raw)
    result['selected_words'] = []
    for address in WORDS:
        b = (out/('word-'+format(address,'x')+'.bin')).read_bytes()
        require(len(b) == 8, 'word length')
        result['selected_words'].append({'virtual_address': hex(address), 'file_offset': address, 'raw_hex': b.hex(), 'little_endian_u64': struct.unpack('<Q', b)[0]})
    require(result == json.loads((out/'projection.json').read_text()), 'projection identity')
    expected = [('header.bin', 0, 32), ('load-commands.bin', 32, h['sizeofcmds'])]+[(n+'.bin', g['streams'][n]['file_offset'], g['streams'][n]['bytes']) for n in STREAMS]+[('word-'+format(a,'x')+'.bin', a, 8) for a in WORDS]
    require(len(receipt['reads']) == len(expected), 'read count')
    for row, (name, offset, size) in zip(receipt['reads'], expected):
        data = (out/name).read_bytes()
        require(row == {'file': name, 'file_offset': offset, 'requested_bytes': size, 'bytes': len(data), 'sha256': digest(data)} and len(data) == size, 'read receipt '+name)
    return {'status': 'PASS', 'owned_data_only': True, 'raw_files': len(expected), 'selected_bytes': sum(x[2] for x in expected), 'controls': self_test()}

if __name__ == '__main__':
    require(len(sys.argv) == 2, 'one explicit mode required')
    if sys.argv[1] == '--self-test':
        print(json.dumps(self_test(), indent=2))
    elif sys.argv[1] == '--check':
        print(json.dumps(check(), indent=2))
    elif sys.argv[1] == '--capture-once':
        sys.exit(capture())
    else:
        raise ValueError('unknown mode')
