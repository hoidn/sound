"""Root-selected one owned4B Rizin data experiment; never opens shipped images."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import resource
import signal
import subprocess
import sys

OUT = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-byte-count-json-fixture')
TOOL = Path('/var/tmp/sound-tools/rizin-v0.9.1/bin/rizin')
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def save(name, value):
    with (OUT / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def core0():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def main():
    assert sys.argv[1:] == ['--root-selected-owned-once'] and sys.dont_write_bytecode
    assert not OUT.exists()
    tool = identity(TOOL)
    assert (tool['bytes'], tool['sha256']) == (59344432, 'ab5614cf137608cffc5a3f4f471a91c995cfa7c0c35465bfb73876e5b95561ba')
    OUT.mkdir()
    fixture = OUT / 'owned-four.bin'
    with fixture.open('xb') as stream:
        stream.write(bytes.fromhex('906690c3'))
    argv = [str(TOOL), '-NN', '-n', '-x', '-f', '-a', 'x86', '-b', '64', '-E', 'little',
            '-m', '0x1000', '-s', '0x1000', '-q', '-c', 'pDj 4', str(fixture)]
    paths = [TOOL, Path(sys.executable).resolve(), Path(__file__).resolve(), fixture]
    before = [identity(p) for p in paths]
    save('selection.json', dict(utc=utc(), selector='Root explicit ONE owned4B pDj4 method experiment',
        raw_hex='906690c3', mapped_va='0x1000', expected_sizes=[1, 2, 1],
        maximum_tool_attempts=1, shipped_image_access=False, original_execution=False))
    save('before-map.json', before)
    save('invocation.json', dict(utc=utc(), argv=argv, cwd=str(OUT), environment=ENV,
        core_limit=[0, 0], stdin='DEVNULL', timeout_seconds=10, start_new_session=True,
        retry=False, tool_identity=tool))
    state = dict(started_utc=utc(), attempted_tool_children=0, returned_pid=None, exit=None,
        exception=None, timeout=False, group_killed=False, original_calls=0, shipped_image_access=False)
    child, stdout, stderr = None, b'', b''
    try:
        save('attempt.json', dict(utc=utc(), attempt=1, argv=argv))
        state['attempted_tool_children'] = 1
        child = subprocess.Popen(argv, cwd=OUT, env=ENV, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=core0, start_new_session=True)
        state['returned_pid'] = child.pid
        save('returned-pid.json', dict(utc=utc(), pid=child.pid))
        try:
            stdout, stderr = child.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            state['timeout'] = True
            os.killpg(child.pid, signal.SIGKILL)
            state['group_killed'] = True
            stdout, stderr = child.communicate()
            raise
        state['exit'] = child.returncode
    except BaseException as error:
        state['exception'] = type(error).__name__ + ': ' + str(error)
    finally:
        if child is not None and child.poll() is None:
            os.killpg(child.pid, signal.SIGKILL)
            state['group_killed'] = True
            stdout, stderr = child.communicate()
        if child is not None:
            state['exit'] = child.returncode
        (OUT / 'stdout.json').write_bytes(stdout)
        (OUT / 'stderr').write_bytes(stderr)
        after = [identity(p) for p in paths]
        save('after-map.json', after)
        state.update(finished_utc=utc(), unchanged=before == after)
        save('status.json', state)
    print(json.dumps(state, indent=2))
    return 0 if state['exit'] == 0 and not state['exception'] and state['unchanged'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
