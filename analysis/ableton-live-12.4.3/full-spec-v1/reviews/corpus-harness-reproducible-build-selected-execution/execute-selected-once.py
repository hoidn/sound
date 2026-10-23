"""Root-selected one-shot own-harness build coordinator; never executes built/original output."""
from pathlib import Path
import datetime, hashlib, json, os, resource, signal, subprocess, sys
ROOT = Path('/home/ollie/Documents/sound')
BASE = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'
HERE = Path(__file__).resolve().parent
PRE = BASE / 'depth-corpus-harness-reproducible-build-preparation'
DEST = BASE / 'depth-corpus-harness-reproducible-build'
CWD = ROOT / 'analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1'
SEAL = '9dbe8a953d7f9e64a65dd265edc03d80eb558a65edffb73f4cca37327bb1ae1d'
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C'}

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(p):
    h = hashlib.sha256(); n = 0
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): n += len(b); h.update(b)
    return dict(path=str(p), bytes=n, sha256=h.hexdigest())
def save(name, value):
    with (HERE / name).open('x') as f:
        json.dump(value, f, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
def raw(name, value):
    with (HERE / name).open('xb') as f: f.write(value); f.flush(); os.fsync(f.fileno())

def main():
    if sys.argv[1:] != ['--execute-root-selected-once'] or not sys.dont_write_bytecode:
        raise SystemExit('Exact separately selected flag and python -B required')
    assert not DEST.exists() and not DEST.is_symlink() and not (HERE / 'receipt.json').exists()
    selected = json.loads((HERE / 'selection.json').read_text())
    assert selected['preparation']['sha256'] == SEAL and identity(PRE / 'manifest.json')['sha256'] == SEAL
    assert selected['collector']['sha256'] == '73345ec5ed2c01d575033e05d7555d021a1e7659ea36fa638211c658d17daf5f'
    assert selected['root_preflight']['sha256'] == '421d164dd75d7bf4c43da12f5fa10c6463e8a6087d93944ef9b066f306f5c392'
    assert selected['peer_preflight']['sha256'] == '06604e4b4c41d2cf006d14611c92934fc86619063473ba997ba8c8b28458fdf8'
    inputs = json.loads((PRE / 'inputs.json').read_text())
    pins = [selected[k] for k in ['preparation', 'collector', 'root_preflight', 'peer_preflight']] + inputs['pins']
    pins += [identity(Path(sys.executable).resolve()), identity(Path(__file__).resolve())]
    for row in pins: assert identity(Path(row['path'])) == row
    save('pins.json', pins)
    old_paths = sorted(p.resolve() for p in CWD.rglob('*') if p.is_file())
    watched = {Path(r['path']).resolve() for r in pins} | set(old_paths)
    for base in [ROOT / 'handoff', ROOT / 'analysis/ableton-live-12.4.3/handoff-staging']:
        watched.update(p.resolve() for p in base.rglob('*') if p.is_file())
    for base in BASE.glob('depth-*'):
        if base.is_dir(): watched.update(p.resolve() for p in base.rglob('*') if p.is_file())
    watched.update((HERE / n).resolve() for n in ['selection.json', 'pins.json', 'execute-selected-once.py'])
    watched = sorted(watched)
    before = [identity(p) for p in watched]
    save('before-map.json', dict(utc=utc(), files=before, old_cwd_file_paths=[str(p) for p in old_paths]))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0)); assert resource.getrlimit(resource.RLIMIT_CORE) == (0, 0)
    argv = [sys.executable, '-B', str(PRE / 'build-once.py'), '--build-selected']
    save('invocation-before.json', dict(utc=utc(), argv=argv, cwd=str(ROOT), environment=ENV,
         inherited_RLIMIT_CORE=[0, 0], stdin='DEVNULL', timeout_seconds=75, compiler_timeout_seconds=60,
         start_new_session=True, automatic_retry=False, original_or_built_output_execution=False))
    state = dict(started_utc=utc(), outer_wrapper_pid=os.getpid(), attempted_collector_launches=0,
                 returned_collector_pid=None, exit=None, exception=None, timeout=False,
                 cleanup_group_killed=False, original_or_built_output_execution=False)
    child, stdout, stderr = None, b'', b''
    try:
        save('attempt.json', dict(utc=utc(), attempt=1, argv=argv))
        state['attempted_collector_launches'] = 1
        child = subprocess.Popen(argv, cwd=ROOT, env=ENV, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        state['returned_collector_pid'] = child.pid
        save('collector-pid.json', dict(utc=utc(), pid=child.pid))
        try: stdout, stderr = child.communicate(timeout=75)
        except subprocess.TimeoutExpired:
            state['timeout'] = True; os.killpg(child.pid, signal.SIGKILL); state['cleanup_group_killed'] = True
            stdout, stderr = child.communicate(); raise RuntimeError('Outer timeout75s; stop without retry')
        state['exit'] = child.returncode
    except BaseException as error:
        state['exception'] = type(error).__name__ + ': ' + str(error)
    finally:
        if child is not None and child.poll() is None:
            os.killpg(child.pid, signal.SIGKILL); state['cleanup_group_killed'] = True
            stdout, stderr = child.communicate()
        if child is not None: state['exit'] = child.returncode
        raw('collector.stdout.json', stdout); raw('collector.stderr', stderr)
        after = []
        for p in watched:
            try: after.append(identity(p))
            except BaseException as error: after.append(dict(path=str(p), identity_error=type(error).__name__ + ': ' + str(error)))
        after_old_paths = sorted(str(p.resolve()) for p in CWD.rglob('*') if p.is_file())
        unchanged = before == after and after_old_paths == [str(p) for p in old_paths]
        save('after-map.json', dict(utc=utc(), files=after, old_cwd_file_paths=after_old_paths, unchanged=unchanged))
        state.update(finished_utc=utc(), watched=len(watched), unchanged=unchanged,
                     stdout=identity(HERE / 'collector.stdout.json'), stderr=identity(HERE / 'collector.stderr'),
                     inherited_RLIMIT_CORE=[0, 0], environment=ENV, destination=str(DEST), automatic_retry=False,
                     compiler_descendants='Inner one gcc group owns timeout60; outer group owns collector timeout75; not individually enumerated or universal process-tree cleanup proof')
        save('receipt.json', state)
    print(json.dumps(state, indent=2))
    return 0 if state['exception'] is None and state['exit'] == 0 and state['unchanged'] else 1
if __name__ == '__main__': raise SystemExit(main())
