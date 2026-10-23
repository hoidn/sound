"""One future Root-selected own-harness build; never execute its output or original code."""
from pathlib import Path
import datetime, hashlib, json, os, resource, signal, subprocess, sys
ROOT = Path('/home/ollie/Documents/sound')
BASE = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'
PRE = BASE / 'depth-utility-xexec-owned-build-preparation'
DEST = BASE / 'depth-utility-xexec-owned-build'
CWD = ROOT
OLD = Path('/var/tmp/sound-analysis/xexec/xexec')
GCC = Path('/usr/bin/gcc')
SOURCE = ROOT / 'tools/xexec/xexec.c'
SOURCES = [str(SOURCE)]
FLAGS = ['-O1', '-g', '-Wall', '-Wextra', '-no-pie']
OUTPUT = DEST / 'xexec'
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C'}
TIMEOUT = 45

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(p):
    h = hashlib.sha256(); n = 0
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): n += len(b); h.update(b)
    return {'path': str(p), 'bytes': n, 'sha256': h.hexdigest()}
def save(name, value):
    with (DEST / name).open('x') as f:
        json.dump(value, f, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
def raw(name, value):
    with (DEST / name).open('xb') as f: f.write(value); f.flush(); os.fsync(f.fileno())
def no_core(): resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
def command(): return [str(GCC), *FLAGS, '-o', str(OUTPUT), *SOURCES, '-ldl', '-lm']
def validate_spec(argv, cwd, output, environment):
    if argv != command() or cwd != str(CWD) or output != str(OUTPUT) or environment != ENV:
        raise ValueError('Only the fixed compiler command, selected cwd, exclusive new output and minimal environment are selected')
    if str(OLD) in argv or output in SOURCES or not str(OUTPUT).startswith(str(DEST) + '/'):
        raise ValueError('Old output/source overwrite forbidden')

def main():
    if sys.argv[1:] != ['--build-selected']:
        print('REFUSED: preparation only; Root and independent peer preflight plus separate explicit execution selection are required', file=sys.stderr)
        return 1
    # Human selection is supplied by a separate frozen Root receipt, not inferred from this flag.
    if DEST.exists() or DEST.is_symlink(): raise FileExistsError(str(DEST))
    inputs = json.loads((PRE / 'inputs.json').read_text())
    for row in inputs['pins']:
        if identity(Path(row['path'])) != row: raise ValueError('Provider identity changed: ' + row['path'])
    tool = inputs['gcc_filesystem_metadata']
    if str(GCC.resolve(strict=True)) != tool['resolved_path'] or os.readlink(GCC) != tool['selected_symlink_target']:
        raise ValueError('Compiler path resolution changed')
    argv = command(); validate_spec(argv, str(CWD), str(OUTPUT), ENV)
    manifest = json.loads((PRE / 'manifest.json').read_text())
    for row in manifest['files']:
        got = identity(PRE / row['path'])
        if (got['bytes'], got['sha256']) != (row['bytes'], row['sha256']): raise ValueError('Preparation changed')
    old_paths = sorted([SOURCE, OLD])
    paths = sorted(set(old_paths) | {Path(r['path']) for r in inputs['pins']} | {p for p in PRE.iterdir() if p.is_file()})
    before = [identity(p) for p in paths]
    # This is the only selected new output directory; no historical file is opened for writing.
    DEST.mkdir()
    child = None; stdout = b''; stderr = b''
    result = dict(started_utc=utc(), top_level_compiler_attempts=0, returned_pid=None,
                  exit=None, timeout=False, exception=None, automatic_retry=False,
                  original_or_built_output_execution=False, compiler_descendants='not individually enumerated')
    try:
        raw('build-once.py', Path(__file__).read_bytes())
        save('before-map.json', dict(utc=utc(), files=before, protected_old_file_paths=[str(p) for p in old_paths]))
        save('invocation.json', dict(utc=utc(), argv=argv, cwd=str(CWD), environment=ENV,
             stdin='DEVNULL', core_limit=[0, 0], timeout_seconds=TIMEOUT,
             start_new_session=True, shell=False, output_execution=False))
        result['top_level_compiler_attempts'] = 1
        save('attempt.json', dict(utc=utc(), attempt=1, argv=argv))
        child = subprocess.Popen(argv, cwd=CWD, env=ENV, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=no_core, start_new_session=True)
        result['returned_pid'] = child.pid
        save('returned-pid.json', dict(utc=utc(), pid=child.pid))
        try: stdout, stderr = child.communicate(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            result['timeout'] = True
            os.killpg(child.pid, signal.SIGKILL); stdout, stderr = child.communicate()
            raise
        result['exit'] = child.returncode
        if child.returncode != 0: raise RuntimeError('Compiler failed')
        if OUTPUT.is_symlink() or not OUTPUT.is_file() or OUTPUT.stat().st_size == 0:
            raise ValueError('Missing, empty or nonregular compiler output')
        rebuilt = OUTPUT.read_bytes(); historic = OLD.read_bytes()
        equal = rebuilt == historic
        save('whole-output-comparison.json', dict(output=identity(OUTPUT), historical=identity(OLD),
             exact_whole_bytes_equal=equal, status='EXACT_BYTES_MATCH' if equal else 'MISMATCH_UNRESOLVED',
             output_executed=False, normalization=False, section_editing=False,
             limitation='Equality is finite compiler-input/output provenance evidence, not current runtime binding, object validity, allocation bounds or behavioral proof. Mismatch is retained U, not a retry.'))
    except BaseException as error:
        result['exception'] = type(error).__name__ + ': ' + str(error)
    finally:
        if child is not None and child.poll() is None:
            os.killpg(child.pid, signal.SIGKILL); stdout, stderr = child.communicate()
        if child is not None: result['exit'] = child.returncode
        raw('compiler.stdout', stdout); raw('compiler.stderr', stderr)
        after = []
        for p in paths:
            try: after.append(identity(p))
            except BaseException as error: after.append(dict(path=str(p), error=type(error).__name__ + ': ' + str(error)))
        after_old_paths = sorted(str(p) for p in [SOURCE, OLD])
        unchanged = before == after and after_old_paths == [str(p) for p in old_paths]
        save('after-map.json', dict(utc=utc(), files=after, protected_old_file_paths=after_old_paths, unchanged=unchanged))
        result.update(finished_utc=utc(), watched=len(paths), providers_and_protected_files_unchanged=unchanged,
                      stdout_bytes=len(stdout), stderr_bytes=len(stderr))
        save('status.json', result)
    print(json.dumps(result, indent=2))
    return 0 if result['exception'] is None and result['exit'] == 0 and result['providers_and_protected_files_unchanged'] else 1
if __name__ == '__main__': raise SystemExit(main())
