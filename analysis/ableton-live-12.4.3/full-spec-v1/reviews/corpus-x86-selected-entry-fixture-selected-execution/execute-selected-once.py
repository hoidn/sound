"""One separately selected SYNTHETIC fixture; never select the original-image mode."""
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
PRE = BASE / 'depth-corpus-x86-selected-entry-preparation'
OUTPUT = BASE / 'depth-corpus-x86-selected-entry-fixture'
SEAL = '194d30df5c0a753fc51f3e066c2707867028df1917f8012904aa030d23f5b6e0'


def identity(path):
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            size += len(block)
            h.update(block)
    return dict(path=str(path), bytes=size, sha256=h.hexdigest())


def save(name, value):
    with (HERE / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


if sys.argv[1:] != ['--execute-root-selected-synthetic-once'] or not sys.dont_write_bytecode:
    raise SystemExit('Exact separately selected synthetic flag and python -B required')
assert not OUTPUT.exists() and not (HERE / 'attempt.json').exists()
selection = json.loads((HERE / 'selection.json').read_text())
assert selection['mode'] == 'fixture' and selection['preparation']['sha256'] == SEAL
assert identity(PRE / 'manifest-preparation.json')['sha256'] == SEAL
assert selection['driver']['sha256'] == '16abca7d24593741052e3aebb0cb4533d6523e9b845e8ab9639596a06d84f6f0'
for key in ('preparation', 'driver', 'root_preflight', 'peer_preflight'):
    assert identity(Path(selection[key]['path'])) == selection[key]
paths = {Path(selection[k]['path']) for k in ('preparation', 'driver', 'root_preflight', 'peer_preflight')}
paths.update(Path(r['path']) for r in json.loads((PRE / 'inputs.json').read_text())['pins'])
for folder in [ROOT / 'handoff', *[p for p in BASE.glob('depth-*') if p.is_dir()]]:
    paths.update(p.resolve() for p in folder.rglob('*') if p.is_file())
paths.update((Path(__file__).resolve(), (HERE / 'selection.json').resolve(), Path(sys.executable).resolve()))
watched = sorted(paths)
before = [identity(p) for p in watched]
save('before-map.json', before)
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
env = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}
argv = [sys.executable, '-B', str(PRE / 'run-selected.py'), 'fixture', SEAL,
        identity(HERE / 'selection.json')['sha256']]
save('invocation-before.json', dict(utc=utc(), argv=argv, cwd=str(ROOT), environment=env,
     stdin='DEVNULL', inherited_core=[0, 0], timeout_seconds=240, termination_grace_seconds=25,
     original_image_mode=False, automatic_retry=False))
state = dict(started_utc=utc(), outer_pid=os.getpid(), attempts=0, driver_pid=None,
             driver_exit=None, exception=None, forced_driver_kill=False)
child, stdout, stderr = None, b'', b''


def interrupted(signum, frame):
    raise KeyboardInterrupt('Signal ' + str(signum))


signal.signal(signal.SIGTERM, interrupted)
signal.signal(signal.SIGINT, interrupted)
try:
    save('attempt.json', dict(utc=utc(), argv=argv, attempt=1))
    state['attempts'] = 1
    child = subprocess.Popen(argv, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    state['driver_pid'] = child.pid
    save('driver-pid.json', dict(utc=utc(), pid=child.pid))
    stdout, stderr = child.communicate(timeout=240)
except BaseException as error:
    state['exception'] = type(error).__name__ + ': ' + str(error)
finally:
    if child is not None and child.poll() is None:
        # Let the reviewed driver's signal handler clean its separate headless group.
        os.killpg(child.pid, signal.SIGTERM)
        try:
            stdout, stderr = child.communicate(timeout=25)
        except subprocess.TimeoutExpired:
            state['forced_driver_kill'] = True
            os.killpg(child.pid, signal.SIGKILL)
            stdout, stderr = child.communicate()
    if child is not None:
        stdout, stderr = child.communicate()
        state['driver_exit'] = child.returncode
    for name, raw in [('driver.stdout.json', stdout), ('driver.stderr', stderr)]:
        with (HERE / name).open('xb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    groups = {child.pid} if child is not None else set()
    if (OUTPUT / 'process.json').is_file():
        groups.add(json.loads((OUTPUT / 'process.json').read_text())['process_group_id'])
    try:
        result = subprocess.run(['/usr/bin/ps', '-axo', 'pid=,pgid=,lstart='], capture_output=True,
                                text=True, check=True, timeout=3, env=env)
        residuals = [line for line in result.stdout.splitlines() if int(line.split()[1]) in groups]
    except Exception as error:
        residuals = ['UNPROVEN: ' + type(error).__name__ + ': ' + str(error)]
    after = [identity(p) for p in watched]
    save('after-map.json', after)
    inner = json.loads((OUTPUT / 'run-status.json').read_text()) if (OUTPUT / 'run-status.json').is_file() else None
    state.update(finished_utc=utc(), watched=len(watched), unchanged=before == after,
                 observed_group_residuals=residuals, inner_status=inner,
                 limits='Finite group check; escaped descendants/pretry/IO/uncatchable failures not exhaustively covered.')
    save('receipt.json', state)
    files = [dict(path=p.name, bytes=p.stat().st_size, sha256=identity(p)['sha256'])
             for p in sorted(HERE.iterdir()) if p.is_file()]
    save('manifest.json' if not residuals else 'manifest-pending.json', dict(files=files, synthetic_only=True))
print(json.dumps(state, indent=2))
raise SystemExit(0 if state['driver_exit'] == 0 and not state['exception'] and state['unchanged']
                 and not state['observed_group_residuals'] and not state['forced_driver_kill'] else 1)
