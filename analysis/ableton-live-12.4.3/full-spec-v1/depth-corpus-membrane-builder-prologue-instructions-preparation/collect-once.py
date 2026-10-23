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
OUT = HERE.parent / 'depth-corpus-membrane-builder-prologue-instructions'
TOOL = Path('/var/tmp/sound-tools/rizin-v0.9.1/bin/rizin')
IMAGE = Path('/var/tmp/sound-analysis/helpers/Corpus/Corpus.arm64')
START, LENGTH = 0x243e8, 148


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
        assert identity(IMAGE) == metadata['image']
        with IMAGE.open('rb') as stream:
            header = stream.read(32)
            assert header.hex() == metadata['header_hex']
            values = struct.unpack('<IiiIIIII', header)
            commands = stream.read(values[5])
            assert commands.hex() == metadata['load_commands_hex']
            assert hashlib.sha256(commands).hexdigest() == metadata['load_commands_sha256']
            assert metadata['file_offset'] == 148456 and metadata['length'] == LENGTH
            stream.seek(metadata['file_offset'])
            raw = stream.read(LENGTH)
        assert len(raw) == LENGTH
        with (OUT / 'prologue-148.bin').open('xb') as stream:
            stream.write(raw)
        save('extraction.json', {'image': identity(IMAGE), 'header_map': identity(HERE / 'header-map.json'),
                               'file_offset': metadata['file_offset'], 'start': hex(START),
                               'end_exclusive': hex(START + LENGTH), 'bytes': LENGTH,
                               'raw_sha256': hashlib.sha256(raw).hexdigest()})
        argv = [str(TOOL), '-NN', '-n', '-x', '-f', '-a', 'arm', '-b', '64',
                '-E', 'little', '-m', hex(START), '-s', hex(START), '-q',
                '-c', 'pdj 37', str(OUT / 'prologue-148.bin')]
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
        assert len(rows) == 37
        assert all(row['offset'] == START + 4 * i and row['size'] == 4 and
                   row.get('type') not in ('invalid', 'ill') and isinstance(row.get('opcode'), str) and
                   row['opcode'].strip().lower() not in ('', 'invalid', 'ill', 'none')
                   for i, row in enumerate(rows))
        assert b''.join(bytes.fromhex(row['bytes']) for row in rows) == raw
        status['validation'] = 'PASS37valid4Brows/exact148Broundtrip'
    except BaseException as error:
        status['exception'] = type(error).__name__ + ': ' + str(error)
    finally:
        if child is not None and child.poll() is None:
            child.kill()
            stdout, stderr = child.communicate()
        if child is not None:
            status['exit'] = child.returncode
        (OUT / 'prologue-148.stdout.json').write_bytes(stdout)
        (OUT / 'prologue-148.stderr').write_bytes(stderr)
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
