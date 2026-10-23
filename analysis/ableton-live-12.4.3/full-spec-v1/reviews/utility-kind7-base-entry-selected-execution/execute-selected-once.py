"""Root-selected one-shot analyst wrapper; static-data decoding only."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import resource
import signal
import subprocess
import sys

ROOT = Path('/home/ollie/Documents/sound')
BASE = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'
HERE = Path(__file__).resolve().parent
PRE = BASE / 'depth-utility-kind7-base-entry-instruction-preparation'
DEST = BASE / 'depth-utility-kind7-base-entry-instruction-data'
SEAL = 'df3d4dec7a4aa6f61397e0ae0ebec883f0b1c574ad969d32708548b308bbdfb1'
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def save(name, value):
    with (HERE / name).open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def main():
    if sys.argv[1:] != ['--execute-root-selected-once'] or not sys.dont_write_bytecode:
        raise SystemExit('Use python3 -B and exact separately selected flag.')
    assert not DEST.exists() and not (HERE / 'receipt.json').exists()
    selection = json.loads((HERE / 'selection.json').read_text())
    assert selection['preparation']['sha256'] == SEAL
    assert identity(PRE / 'manifest-preparation.json')['sha256'] == SEAL
    assert identity(PRE / 'extract-decode-once.py')['sha256'] == '8b93f5c13fdb7a12708f2c38e91a046bc9cd7cdc432953d45e449333ecf0a0d3'
    plan = json.loads((PRE / 'plan.json').read_text())
    prior_path = BASE / 'reviews/corpus-x86-create-c150-root-execution/before-map.json'
    pins = [selection[key] for key in ['preparation', 'collector', 'root_preflight', 'peer_preflight']]
    pins += [plan['image'], plan['tool'], *plan['providers']]
    pins += [identity(Path(sys.executable).resolve()), identity(Path(__file__).resolve()), identity(prior_path)]
    for row in pins:
        assert identity(Path(row['path'])) == row
    save('pins.json', pins)
    # Preserve the prior coordinator scope and add every current handoff/depth file.
    prior = json.loads(prior_path.read_text())
    watched = {Path(row['path']).resolve() for row in prior + pins}
    watched.update(path.resolve() for path in (ROOT / 'handoff').rglob('*') if path.is_file())
    for directory in BASE.glob('depth-*'):
        if directory.is_dir():
            watched.update(path.resolve() for path in directory.rglob('*') if path.is_file())
    watched.update(path.resolve() for path in PRE.iterdir() if path.is_file())
    watched.update((HERE / name).resolve() for name in ['selection.json', 'pins.json', 'execute-selected-once.py'])
    watched = sorted(watched)
    before = [identity(path) for path in watched]
    save('before-map.json', before)
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    core_limit = list(resource.getrlimit(resource.RLIMIT_CORE))
    assert core_limit == [0, 0]
    argv = [sys.executable, '-B', str(PRE / 'extract-decode-once.py'),
            '--extract-decode-selected-once', SEAL]
    save('invocation-before.json', dict(utc=utc(), argv=argv, cwd=str(ROOT),
         environment=ENV, inherited_RLIMIT_CORE=core_limit, stdin='DEVNULL',
         timeout_seconds=55, collector_timeout_seconds=30,
         start_new_session=True, retry=False, original_instruction_execution=False))
    state = dict(started_utc=utc(), outer_wrapper_pid=os.getpid(), attempted_collector_launches=0,
                 returned_collector_pid=None, exit=None, exception=None, timeout=False,
                 cleanup_group_killed=False, original_instruction_execution=False)
    child, stdout, stderr = None, b'', b''
    try:
        save('attempt.json', dict(utc=utc(), attempt=1, argv=argv))
        state['attempted_collector_launches'] = 1
        child = subprocess.Popen(argv, cwd=ROOT, env=ENV, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        state['returned_collector_pid'] = child.pid
        save('collector-pid.json', dict(utc=utc(), pid=child.pid))
        try:
            stdout, stderr = child.communicate(timeout=55)
        except subprocess.TimeoutExpired:
            state['timeout'] = True
            os.killpg(child.pid, signal.SIGKILL)
            state['cleanup_group_killed'] = True
            stdout, stderr = child.communicate()
            raise RuntimeError('Outer timeout55s; stop without retry.')
        state['exit'] = child.returncode
    except BaseException as error:
        state['exception'] = type(error).__name__ + ': ' + str(error)
    finally:
        if child is not None and child.poll() is None:
            os.killpg(child.pid, signal.SIGKILL)
            state['cleanup_group_killed'] = True
            stdout, stderr = child.communicate()
        if child is not None:
            state['exit'] = child.returncode
        for name, raw in [('collector.stdout.json', stdout), ('collector.stderr', stderr)]:
            with (HERE / name).open('xb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
        after = [identity(path) for path in watched]
        save('after-map.json', after)
        state.update(finished_utc=utc(), watched=len(watched), unchanged=before == after,
                     stdout=identity(HERE / 'collector.stdout.json'),
                     stderr=identity(HERE / 'collector.stderr'), inherited_RLIMIT_CORE=core_limit,
                     environment=ENV, destination=str(DEST), automatic_retry=False)
        save('receipt.json', state)
    print(json.dumps(state, indent=2))
    return 0 if state['exception'] is None and state['exit'] == 0 and state['unchanged'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
