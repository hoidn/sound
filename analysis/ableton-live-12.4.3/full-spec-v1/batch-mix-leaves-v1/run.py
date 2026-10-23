"""One selected batch of existing unpatched harness calls; never build or retry."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def validate(row):
    tokens = row['tokens']
    assert tokens and tokens[0] == 'call'
    assert not any(x.startswith('--') for x in tokens)
    assert 1 <= tokens.count('call') <= 256
    assert not row.get('source_locator', {}).get('recorded_patches')


def selfcheck():
    validate({'tokens': ['call', '0x101b1a8e0', 'f:0x0p+0']})
    for bad in [[], ['--patch', '0x1=alloc32'], ['call'] * 257]:
        try:
            validate({'tokens': bad})
        except AssertionError:
            pass
        else:
            raise AssertionError('unsafe input accepted')
    try:
        validate({'tokens': ['call', '0x1'], 'source_locator': {'recorded_patches': ['patch']}})
    except AssertionError:
        pass
    else:
        raise AssertionError('patched source accepted')


def no_core():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def main():
    selfcheck()
    if sys.argv[1:] == ['--self-check']:
        print('PASS: valid call accepted; empty, patched and over-cap inputs rejected')
        return
    assert sys.argv[1:] == ['--run-selected-batch']
    pins = json.loads((HERE / 'pins.json').read_text())
    for pin in pins:
        raw = Path(pin['path']).read_bytes()
        assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256']
    selection = json.loads((HERE / 'selection.json').read_text())
    rows = json.loads((HERE / 'inputs.json').read_text())
    assert len(rows) == 144 and len({r['id'] for r in rows}) == len(rows)
    for row in rows:
        validate(row)
    binary, image = selection['binary']['path'], selection['slice']['path']
    env = {'PATH': os.environ.get('PATH', ''), 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC'}
    results = HERE / 'results.jsonl'
    with results.open('x') as out:
        for index, row in enumerate(rows):
            argv = [binary, image, *(['--imports'] if index == 0 else []), *row['tokens']]
            record = {'id': row['id'], 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      'argv': argv, 'environment': env, 'timeout_seconds': 20, 'automatic_retry': False}
            try:
                child = subprocess.run(argv, cwd=HERE, env=env, stdin=subprocess.DEVNULL,
                                       capture_output=True, text=True, timeout=20, preexec_fn=no_core)
                record.update(rc=child.returncode, stdout=child.stdout, stderr=child.stderr, timeout=False)
            except subprocess.TimeoutExpired as error:
                def decode(value):
                    return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                record.update(rc=None, stdout=decode(error.stdout), stderr=decode(error.stderr), timeout=True)
            record['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            out.write(json.dumps(record) + '\n')
            out.flush()
            print(json.dumps({'row': index + 1, 'id': row['id'], 'rc': record['rc'], 'timeout': record['timeout']}), flush=True)
            if record['rc'] != 0 or record['timeout']:
                raise SystemExit('Stopped after failed selected row; results retained, no retry.')


if __name__ == '__main__':
    main()
