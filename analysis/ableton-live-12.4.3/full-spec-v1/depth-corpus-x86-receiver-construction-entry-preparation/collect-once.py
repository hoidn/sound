"""Selected static-data decoder only. Never execute original instructions."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import resource
import struct
import subprocess
import sys

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'depth-corpus-x86-receiver-construction-entry-instructions'
TOOL = Path('/var/tmp/sound-tools/rizin-v0.9.1/bin/rizin')
IMAGE = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Corpus.bundle/Contents/MacOS/Corpus')
START, LENGTH = 0x39a0, 240


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def identity(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def save(name, value):
    with (OUT / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def no_core():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def validate_prefix(rows, raw):
    assert isinstance(raw, bytes) and len(raw) == LENGTH
    assert isinstance(rows, list) and len(rows) == 16
    cursor, pieces = START, []
    for row in rows:
        assert isinstance(row, dict)
        assert type(row.get('offset')) is int and row['offset'] == cursor
        assert type(row.get('size')) is int and 1 <= row['size'] <= 15
        assert isinstance(row.get('type'), str) and row['type'].strip().lower() not in ('', 'invalid', 'ill')
        assert isinstance(row.get('opcode'), str)
        assert row['opcode'].strip().lower() not in ('', 'invalid', 'ill', 'none')
        assert isinstance(row.get('bytes'), str)
        piece = bytes.fromhex(row['bytes'])
        assert len(piece) == row['size']
        pieces.append(piece)
        cursor += row['size']
        assert cursor - START <= LENGTH
    consumed = cursor - START
    assert b''.join(pieces) == raw[:consumed]
    return {'rows': 16, 'consumed_bytes': consumed,
            'decoded_prefix_half_open': [hex(START), hex(cursor)],
            'uninterpreted_selected_bytes': LENGTH - consumed,
            'selected_bytes': LENGTH, 'body_extent_claim': False}


def main():
    if sys.argv[1:] != ['--collect-selected']:
        raise SystemExit('Only separately selected --collect-selected; no default run.')
    if OUT.exists():
        raise SystemExit('Exclusive destination exists; no overwrite/retry.')
    OUT.mkdir()
    status = {'started_utc': utc(), 'attempted_decoder_children': 0,
              'returned_pid_children': 0, 'exit': None, 'exception': None,
              'validation': 'NOT_REACHED', 'original_instruction_execution': False}
    stdout, stderr = b'', b''
    child, before, watched = None, None, []
    try:
        (OUT / 'collect-once.py').write_bytes(Path(__file__).read_bytes())
        manifest = json.loads((HERE / 'manifest.json').read_text())
        for row in manifest['files']:
            got = identity(HERE / row['path'])
            assert (got['bytes'], got['sha256']) == (row['bytes'], row['sha256'])
        inputs = json.loads((HERE / 'inputs.json').read_text())
        watched = sorted({Path(row['path']) for row in inputs['pins']} |
                         {p for p in HERE.iterdir() if p.is_file()})
        before = [identity(p) for p in watched]
        save('before-map.json', {'utc': utc(), 'files': before})
        for row in inputs['pins']:
            assert identity(Path(row['path'])) == {k: row[k] for k in ('path', 'bytes', 'sha256')}
        metadata = json.loads((HERE / 'header-map.json').read_text())
        assert identity(IMAGE) == metadata['bundle']
        with IMAGE.open('rb') as stream:
            fat_header = stream.read(8)
            assert fat_header.hex() == metadata['fat_header_hex']
            magic, nfat = struct.unpack('>II', fat_header)
            assert magic == 0xcafebabe and nfat == 2
            arch_bytes = stream.read(nfat * 20)
            assert arch_bytes.hex() == metadata['fat_arch_table_hex']
            arches = [struct.unpack_from('>IIIII', arch_bytes, i * 20) for i in range(nfat)]
            matches = [r for r in arches if r[0] == 0x1000007 and r[1] == 3]
            assert len(matches) == 1
            cpu, subtype, slice_offset, slice_size, alignment = matches[0]
            assert (slice_offset, slice_size, alignment) == (16384, 250352, 14)
            assert slice_offset + slice_size <= metadata['bundle']['bytes']
            stream.seek(slice_offset)
            assert hashlib.sha256(stream.read(slice_size)).hexdigest() == metadata['slice_sha256']
            stream.seek(slice_offset)
            header = stream.read(32)
            assert header.hex() == metadata['header_hex']
            values = struct.unpack('<IiiIIIII', header)
            assert values[0] == 0xfeedfacf and values[1] == cpu and values[2] == subtype
            assert values[4] == 14 and values[5] == 1696 and 32 + values[5] <= slice_size
            commands = stream.read(values[5])
            assert commands.hex() == metadata['load_commands_hex']
            assert hashlib.sha256(commands).hexdigest() == metadata['load_commands_sha256']
            segments, cursor = [], 0
            for _ in range(values[4]):
                command, size = struct.unpack_from('<II', commands, cursor)
                assert size >= 8 and cursor + size <= len(commands)
                if command == 0x19:
                    name, va, vs, fo, fs, mp, ip, ns, fl = struct.unpack_from('<16sQQQQiiII', commands, cursor + 8)
                    assert fo + fs <= slice_size
                    segments.append(dict(name=name.rstrip(b'\0').decode(), vmaddr=va, vmsize=vs,
                                         fileoff=fo, filesize=fs, maxprot=mp, initprot=ip, nsects=ns, flags=fl))
                cursor += size
            assert cursor == len(commands) and segments == metadata['segments']
            matches = [s for s in segments if s['vmaddr'] <= START and START + LENGTH <= s['vmaddr'] + s['filesize']]
            assert matches == [metadata['selected_segment']] and matches[0]['name'] == '__TEXT'
            assert matches[0]['initprot'] & 4
            slice_file_offset = matches[0]['fileoff'] + START - matches[0]['vmaddr']
            bundle_file_offset = slice_offset + slice_file_offset
            assert slice_file_offset == metadata['slice_file_offset'] == 14752
            assert bundle_file_offset == metadata['bundle_file_offset'] == 31136
            assert metadata['length'] == LENGTH
            stream.seek(bundle_file_offset)
            raw = stream.read(LENGTH)
        assert len(raw) == LENGTH
        with (OUT / 'receiver-entry-240.bin').open('xb') as stream:
            stream.write(raw)
        save('extraction.json', {'image': identity(IMAGE), 'header_map': identity(HERE / 'header-map.json'),
                               'bundle_file_offset': bundle_file_offset, 'slice_file_offset': slice_file_offset, 'start': hex(START),
                               'end_exclusive': hex(START + LENGTH), 'bytes': LENGTH,
                               'raw_sha256': hashlib.sha256(raw).hexdigest()})
        argv = [str(TOOL), '-NN', '-n', '-x', '-f', '-a', 'x86', '-b', '64',
                '-E', 'little', '-m', hex(START), '-s', hex(START), '-q',
                '-c', 'pdj 16', str(OUT / 'receiver-entry-240.bin')]
        env = {key: os.environ[key] for key in ('PATH', 'LANG', 'LC_ALL', 'TZ') if key in os.environ}
        save('invocation-before.json', {'utc': utc(), 'argv': argv, 'cwd': str(OUT),
                                       'environment': env, 'timeout_seconds': 30,
                                       'core_limit': [0, 0], 'stdin': 'DEVNULL',
                                       'attempt_index': 1, 'automatic_retry': False,
                                       'original_instruction_execution': False})
        save('attempt.json', {'utc': utc(), 'attempt_index': 1, 'argv': argv})
        status['attempted_decoder_children'] = 1
        child = subprocess.Popen(argv, cwd=OUT, env=env, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 preexec_fn=no_core)
        status['returned_pid_children'] = 1
        save('returned-pid.json', {'utc': utc(), 'pid': child.pid})
        try:
            stdout, stderr = child.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            child.kill()
            stdout, stderr = child.communicate()
            raise RuntimeError('Decoder timeout after30seconds; no retry')
        status['exit'] = child.returncode
        assert status['exit'] == 0
        rows = json.loads(stdout)
        coverage = validate_prefix(rows, raw)
        save('prefix-coverage.json', coverage)
        status['validation'] = 'PASS16valid-variable-length-rows/exact-prefix-only'
    except BaseException as error:
        status['exception'] = type(error).__name__ + ': ' + str(error)
    finally:
        if child is not None and child.poll() is None:
            child.kill()
            stdout, stderr = child.communicate()
        if child is not None:
            status['exit'] = child.returncode
        (OUT / 'receiver-entry-240.stdout.json').write_bytes(stdout)
        (OUT / 'receiver-entry-240.stderr').write_bytes(stderr)
        try:
            after = [identity(p) for p in watched]
            unchanged = before is not None and before == after
            save('after-map.json', {'utc': utc(), 'files': after, 'unchanged': unchanged})
            status['providers_unchanged'] = unchanged
        except BaseException as error:
            status['after_map_exception'] = type(error).__name__ + ': ' + str(error)
            status['providers_unchanged'] = False
        status['finished_utc'] = utc()
        save('status.json', status)
    print(json.dumps(status, indent=2))
    raise SystemExit(0 if status['exception'] is None and status['providers_unchanged'] else 1)


if __name__ == '__main__':
    main()
