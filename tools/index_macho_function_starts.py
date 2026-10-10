#!/usr/bin/env python3
"""Strict LC_FUNCTION_STARTS metadata index; never a discovered-function inventory."""
import argparse
import hashlib
import json
import mmap
import os
from pathlib import Path
import resource
import shutil
import signal
import struct
import sys
import tempfile
import time

U64 = (1 << 64) - 1
PINNED_SHA256 = '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def span(offset, size, limit, label):
    require(0 <= offset <= limit and 0 <= size <= limit - offset, f'{label} out of bounds')


def header(data):
    require(len(data) >= 32, 'truncated Mach-O header')
    magic, cpu, subtype, kind, count, size, flags, reserved = struct.unpack_from('<8I', data)
    require(magic == 0xfeedfacf, 'requires thin little-endian Mach-O 64')
    require(cpu == 0x0100000c and subtype == 0, 'requires arm64 ALL architecture')
    require(kind == 2, 'requires MH_EXECUTE')
    require(reserved == 0, 'nonzero reserved header field')
    span(32, size, len(data), 'load-command region')
    require(count <= size // 8, 'load-command count exceeds region')
    end, offset, segments, starts = 32 + size, 32, [], []
    for index in range(count):
        span(offset, 8, end, 'load-command header')
        cmd, cmdsize = struct.unpack_from('<II', data, offset)
        require(cmdsize >= 8 and cmdsize % 8 == 0, 'invalid load-command size/alignment')
        span(offset, cmdsize, end, 'load command')
        if cmd == 0x19:
            require(cmdsize >= 72, 'truncated segment command')
            fields = struct.unpack_from('<II16sQQQQiiII', data, offset)
            _, _, rawname, vm, vmsize, fileoff, filesize, maxprot, initprot, nsects, _ = fields
            require(cmdsize == 72 + 80 * nsects, 'segment section-count/size mismatch')
            name = rawname.split(b'\0', 1)[0].decode('ascii', errors='strict')
            require(name and all(32 < ord(c) < 127 for c in name), 'invalid segment name')
            require(vmsize <= U64 - vm, 'segment virtual-address overflow')
            require(filesize <= vmsize, 'segment file size exceeds virtual size')
            span(fileoff, filesize, len(data), 'segment file range')
            require(initprot & ~maxprot == 0, 'segment initial protection exceeds maximum')
            segments.append(dict(name=name, vmaddr=vm, vmsize=vmsize, fileoff=fileoff,
                                 filesize=filesize, initprot=initprot))
        elif cmd == 0x26:
            require(cmdsize == 16, 'invalid LC_FUNCTION_STARTS size')
            _, _, dataoff, datasize = struct.unpack_from('<4I', data, offset)
            span(dataoff, datasize, len(data), 'function-start payload')
            starts.append(dict(load_command_index=index, load_command_offset=offset,
                               dataoff=dataoff, datasize=datasize))
        offset += cmdsize
    require(offset == end, 'load-command region not consumed exactly')
    require(len(starts) <= 1, 'duplicate LC_FUNCTION_STARTS commands')
    texts = [s for s in segments if s['name'] == '__TEXT']
    require(len(texts) == 1, 'requires unique __TEXT segment')
    if not starts:
        return dict(status='absent', segments=segments, command=None, text_vmaddr=texts[0]['vmaddr'])
    command = starts[0]
    require(command['datasize'] > 0, 'empty function-start payload has no terminator')
    links = [s for s in segments if s['name'] == '__LINKEDIT' and
             s['fileoff'] <= command['dataoff'] and
             command['dataoff'] + command['datasize'] <= s['fileoff'] + s['filesize']]
    require(len(links) == 1, 'payload requires unique __LINKEDIT file mapping')
    return dict(status='present', segments=segments, command=command, text_vmaddr=texts[0]['vmaddr'])


def uleb(data, offset, end):
    value = 0
    for index in range(10):
        require(offset < end, 'truncated ULEB128')
        byte = data[offset]
        offset += 1
        require(index != 9 or byte <= 1, 'ULEB128 uint64 overflow')
        value |= (byte & 0x7f) << (7 * index)
        if not byte & 0x80:
            require(index == 0 or byte != 0, 'noncanonical ULEB128')
            return value, offset
    raise ValueError('overlong ULEB128')


def rows(data, info):
    if info['status'] == 'absent':
        return
    cmd = info['command']
    offset, end = cmd['dataoff'], cmd['dataoff'] + cmd['datasize']
    address = info['text_vmaddr']
    while offset < end:
        entry_offset = offset
        delta, offset = uleb(data, offset, end)
        if delta == 0:
            require(all(data[i] == 0 for i in range(offset, end)), 'nonzero data after terminator')
            return
        require(delta <= U64 - address, 'cumulative address overflow')
        address += delta
        require(address % 4 == 0, 'unaligned arm64 function start')
        matches = [s for s in info['segments'] if s['vmaddr'] <= address < s['vmaddr'] + s['vmsize']]
        require(len(matches) == 1, 'start has absent/ambiguous segment mapping')
        segment = matches[0]
        require(segment['initprot'] & 4, 'start maps to non-executable segment')
        relative = address - segment['vmaddr']
        require(relative + 4 <= segment['filesize'], 'start is not fully file-backed')
        yield address, segment['fileoff'] + relative, segment['name'], entry_offset
    raise ValueError('function-start payload lacks zero terminator')


def hash_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def extract(target, output, expected_sha256):
    started = time.monotonic()
    require(len(expected_sha256) == 64 and all(c in '0123456789abcdef' for c in expected_sha256), 'invalid target hash')
    require(not output.exists(), 'output already exists; choose a fresh revision')
    initial = target.stat()
    digest = hash_file(target)
    require(digest == expected_sha256, 'target SHA-256 mismatch')
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.' + output.name + '-', dir=output.parent))
    try:
        method = Path(__file__).resolve()
        shutil.copyfile(method, stage / method.name)
        count, first, last = 0, None, None
        with target.open('rb') as source, mmap.mmap(source.fileno(), 0, access=mmap.ACCESS_READ) as data:
            info = header(data)
            if info['status'] == 'present':
                with (stage / 'addresses.tsv').open('x') as table:
                    table.write('address\tfile_offset\tsegment\tuleb_file_offset\n')
                    for address, fileoff, segment, entry_offset in rows(data, info):
                        table.write(f'0x{address:x}\t0x{fileoff:x}\t{segment}\t0x{entry_offset:x}\n')
                        count += 1
                        first = first if first is not None else address
                        last = address
        final = target.stat()
        require((initial.st_dev, initial.st_ino, initial.st_size, initial.st_mtime_ns, initial.st_ctime_ns) ==
                (final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns, final.st_ctime_ns), 'target changed during extraction')
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss_bytes = rss if sys.platform == 'darwin' else rss * 1024
        summary = dict(schema='macho-linker-function-starts-v1', status=info['status'],
                       target=str(target.resolve()), target_sha256=digest, target_bytes=initial.st_size,
                       method_sha256=hash_file(stage / method.name), architecture='arm64',
                       source='LC_FUNCTION_STARTS', declared_start_count=count,
                       first_address=None if first is None else f'0x{first:x}',
                       last_address=None if last is None else f'0x{last:x}',
                       command=info['command'], segments=info['segments'],
                       text_vmaddr=f"0x{info['text_vmaddr']:x}",
                       elapsed_seconds=time.monotonic() - started, peak_process_rss_bytes=rss_bytes,
                       limitations=['Linker-declared starts only; not discovered functions or complete code.',
                                    'Adjacent starts do not establish body ranges or function sizes.',
                                    'No instruction decoding, names, behavior or type recovery.'])
        write_json(stage / 'summary.json', summary)
        write_json(stage / 'manifest.json', {p.name: {'sha256': hash_file(p), 'bytes': p.stat().st_size}
                                            for p in sorted(stage.iterdir())})
        for p in stage.iterdir():
            with p.open('rb') as stream:
                os.fsync(stream.fileno())
        require(not output.exists(), 'output appeared during extraction')
        stage.rename(output)
        return summary
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--target-sha256', default=PINNED_SHA256)
    args = parser.parse_args()
    def deadline(*_):
        raise TimeoutError('sixty-second extraction deadline reached')
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(60)
    try:
        result = extract(args.target, args.output, args.target_sha256)
        print(json.dumps(result, indent=2))
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()
