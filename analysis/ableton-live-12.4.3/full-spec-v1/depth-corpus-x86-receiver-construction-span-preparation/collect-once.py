"""Selected static-data decoder only. Never execute original instructions."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import resource
import subprocess
import sys

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'depth-corpus-x86-receiver-construction-span'
TOOL = Path('/var/tmp/sound-tools/rizin-v0.9.1/bin/rizin')
RETAINED = HERE.parent / 'depth-corpus-x86-receiver-construction-entry-instructions/receiver-entry-240.bin'
START, LENGTH = 0x39a0, 144


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


def validate_span(rows, raw):
    assert isinstance(raw, bytes) and len(raw) == LENGTH
    assert isinstance(rows, list) and 1 <= len(rows) <= LENGTH
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
        assert row['bytes'] == piece.hex()
        pieces.append(piece)
        cursor += row['size']
        assert cursor - START <= LENGTH
    consumed = cursor - START
    assert cursor == START + LENGTH
    assert b''.join(pieces) == raw
    return {'rows': len(rows), 'consumed_bytes': consumed,
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
        metadata = json.loads((HERE / 'input-selection.json').read_text())
        assert identity(RETAINED) == metadata['retained_input']
        assert metadata['retained_input']['bytes'] == 240
        assert metadata['selected_offset'] == 0 and metadata['selected_bytes'] == LENGTH
        assert metadata['start'] == hex(START) and metadata['end_exclusive'] == hex(START + LENGTH)
        assert metadata['uninterpreted_retained_suffix_bytes'] == 96
        prior = Path(metadata['prior_extraction']['path'])
        assert identity(prior) == metadata['prior_extraction']
        source_record = json.loads(prior.read_text())
        assert source_record['start'] == hex(START) and source_record['bytes'] == 240
        assert source_record['end_exclusive'] == hex(START + 240)
        assert source_record['raw_sha256'] == metadata['retained_input']['sha256']
        with RETAINED.open('rb') as stream:
            raw = stream.read(LENGTH)
        assert len(raw) == LENGTH
        with (OUT / 'receiver-span-144.bin').open('xb') as stream:
            stream.write(raw)
        save('extraction.json', {'source_kind': 'already-retained-prefix-only',
                               'retained_input': identity(RETAINED), 'input_selection': identity(HERE / 'input-selection.json'),
                               'selected_offset': 0, 'start': hex(START), 'end_exclusive': hex(START + LENGTH),
                               'bytes': LENGTH, 'raw_sha256': hashlib.sha256(raw).hexdigest(),
                               'uninterpreted_retained_suffix_bytes': 96, 'original_image_read': False})
        argv = [str(TOOL), '-NN', '-n', '-x', '-f', '-a', 'x86', '-b', '64',
                '-E', 'little', '-m', hex(START), '-s', hex(START), '-q',
                '-c', 'pDj 144', str(OUT / 'receiver-span-144.bin')]
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
        coverage = validate_span(rows, raw)
        coverage['uninterpreted_retained_suffix_bytes'] = 96
        save('span-coverage.json', coverage)
        status['validation'] = 'PASSvalid-variable-length-rows/exact144B-span-only'
    except BaseException as error:
        status['exception'] = type(error).__name__ + ': ' + str(error)
    finally:
        if child is not None and child.poll() is None:
            child.kill()
            stdout, stderr = child.communicate()
        if child is not None:
            status['exit'] = child.returncode
        (OUT / 'receiver-span-144.stdout.json').write_bytes(stdout)
        (OUT / 'receiver-span-144.stderr').write_bytes(stderr)
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
