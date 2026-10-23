"""Root-selected four original call supervisor; fixed owned-state question only."""
from pathlib import Path
import datetime, hashlib, json, os, resource, signal, subprocess, sys
ROOT = Path('/home/ollie/Documents/sound')
BASE = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'
HERE = Path(__file__).resolve().parent
PRE = BASE / 'depth-utility-xexec-chained-state-preparation'
DEST = BASE / 'depth-utility-xexec-chained-state'
CWD = ROOT
SEAL = '1d1e0a5530f6b31dd37892ffddfd68c92d5f5aacb65b660b2d0f7fa8b74e3ab3'
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
    assert selected['collector']['sha256'] == 'b504cb62e03c2c19343ba429c5e487e1e5fc05b6e381ca4795bfd1566abc065d'
    assert selected['root_preflight']['sha256'] == 'd2205e3e2761aeacd88218eac803d1b882388d703f8a31bdbabb2d3e09aa94dc'
    assert selected['peer_preflight']['sha256'] == '4216270a543caca03195dfaba43bf65a933294d7fc33cc2be7702c1b8b67cffb'
    inputs = json.loads((PRE / 'inputs.json').read_text())
    pins = [selected[k] for k in ['preparation', 'collector', 'root_preflight', 'peer_preflight']] + inputs['pins']
    pins += [identity(Path(sys.executable).resolve()), identity(Path(__file__).resolve())]
    for row in pins: assert identity(Path(row['path'])) == row
    save('pins.json', pins)
    old_paths = sorted([ROOT / 'tools/xexec/xexec.c', Path('/var/tmp/sound-analysis/xexec/xexec')])
    watched = {Path(r['path']).resolve() for r in pins} | set(old_paths)
    for base in [ROOT / 'handoff', ROOT / 'analysis/ableton-live-12.4.3/handoff-staging']:
        watched.update(p.resolve() for p in base.rglob('*') if p.is_file())
    watched.update(p.resolve() for p in PRE.iterdir() if p.is_file())
    watched.update((HERE / n).resolve() for n in ['selection.json', 'pins.json', 'execute-selected-once.py'])
    watched = sorted(watched)
    before = [identity(p) for p in watched]
    save('before-map.json', dict(utc=utc(), files=before, old_cwd_file_paths=[str(p) for p in old_paths]))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0)); assert resource.getrlimit(resource.RLIMIT_CORE) == (0, 0)
    argv = [sys.executable, '-B', str(PRE / 'capture-once.py'), '--capture-root-selected-once']
    save('invocation-before.json', dict(utc=utc(), argv=argv, cwd=str(ROOT), environment=ENV,
         inherited_RLIMIT_CORE=[0, 0], stdin='DEVNULL', timeout_seconds=40, original_child_timeout_seconds=20,
         start_new_session=True, automatic_retry=False, original_instruction_execution_selected=True))
    state = dict(started_utc=utc(), outer_wrapper_pid=os.getpid(), attempted_collector_launches=0,
                 returned_collector_pid=None, exit=None, exception=None, timeout=False,
                 cleanup_group_killed=False, original_instruction_execution_selected=True)
    child, stdout, stderr = None, b'', b''
    try:
        save('attempt.json', dict(utc=utc(), attempt=1, argv=argv))
        state['attempted_collector_launches'] = 1
        child = subprocess.Popen(argv, cwd=ROOT, env=ENV, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        state['returned_collector_pid'] = child.pid
        save('collector-pid.json', dict(utc=utc(), pid=child.pid))
        try: stdout, stderr = child.communicate(timeout=40)
        except subprocess.TimeoutExpired:
            state['timeout'] = True; os.killpg(child.pid, signal.SIGKILL); state['cleanup_group_killed'] = True
            stdout, stderr = child.communicate(); raise RuntimeError('Outer timeout40s; stop without retry')
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
        after_old_paths = sorted(str(p) for p in old_paths)
        unchanged = before == after and after_old_paths == [str(p) for p in old_paths]
        save('after-map.json', dict(utc=utc(), files=after, old_cwd_file_paths=after_old_paths, unchanged=unchanged))
        state.update(finished_utc=utc(), watched=len(watched), unchanged=unchanged,
                     stdout=identity(HERE / 'collector.stdout.json'), stderr=identity(HERE / 'collector.stderr'),
                     inherited_RLIMIT_CORE=[0, 0], environment=ENV, destination=str(DEST), automatic_retry=False,
                     original_scope='Inner selected original group20s; outer collector40s; max4top-levelcalls only. Finite pretry/IO/defaultSIGTERM/escapeddescendant limits, postgroup snapshot required.')
        save('receipt.json', state)
    print(json.dumps(state, indent=2))
    return 0 if state['exception'] is None and state['exit'] == 0 and state['unchanged'] else 1
if __name__ == '__main__': raise SystemExit(main())
