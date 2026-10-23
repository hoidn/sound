"""One fixed157-child capture through unchanged xdev; never build or retry."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import runpy
import signal
import subprocess
import sys
import time
import shutil

HERE = Path(__file__).resolve().parent
D = runpy.run_path(str(HERE / 'data.py'), run_name='owned_data_functions')


def utc():
    return datetime.now(timezone.utc).isoformat()


def save(name, value):
    path = HERE / name
    with path.open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n'); f.flush(); os.fsync(f.fileno())


def local_seal():
    pre = json.loads((HERE / 'pre-call-manifest.json').read_text())
    for item in pre['payloads']:
        observed = D['identity'](HERE / item['path'])
        assert all(observed[k] == item[k] for k in ('bytes', 'sha256'))


def runtime(config, row):
    result = []
    for expected in config['runtime_expected']:
        actual = D['identity'](expected['path'])
        assert actual == expected, 'Runtime identity mismatch: ' + expected['path']
        result.append(actual)
    image = config['bundle_slice_expected']
    with Path(image['path']).open('rb') as f:
        f.seek(image['x86_64_offset']); raw = f.read(image['x86_64_size'])
    assert len(raw) == image['x86_64_size'] and hashlib.sha256(raw).hexdigest() == image['x86_64_sha256']
    result.append({'path': image['path'], 'slice_offset': image['x86_64_offset'], 'bytes': len(raw), 'sha256': image['x86_64_sha256']})
    for name in ('inputs.json', 'data.py', 'run_batch.py', 'check_data.py', 'launch.py', 'input.f32'):
        result.append(D['identity'](HERE / name))
    actual = D['identity'](row['script']['path']); assert actual == row['script']
    result.append(actual)
    return result


def limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (20, 20))
    resource.setrlimit(resource.RLIMIT_FSIZE, (4194304, 4194304))


def main(config):
    local_seal()
    launch = json.loads((HERE / 'launch-receipt.json').read_text())
    pre_raw=(HERE/'pre-call-manifest.json').read_bytes()
    D['parent_valid'](launch,config,os.getpid(),{'bytes':len(pre_raw),'sha256':hashlib.sha256(pre_raw).hexdigest()})
    (HERE / 'attempts').mkdir(exist_ok=False)
    source_before = [D['identity'](p['path']) for p in config['source_pins']]
    assert source_before == config['source_pins']
    inherited = json.loads((HERE / 'inherited-controls.json').read_text())
    context = {'utc_start': utc(), 'outer_pid': os.getpid(), 'outer_argv': sys.argv, 'python': sys.version,
               'host': list(os.uname()), 'child_environment': config['environment'], 'source_before': source_before,
               'limits': config['limits'], 'parent_launch_receipt': launch, 'historical_controls_not_replayed': [x['id'] for x in config['rows'] if x['disposition']=='inherited-no-replay'], 'outer_environment_not_attested': True}
    save('execution-context.json', context)
    fresh = [r for r in config['rows'] if r['disposition'] == 'fresh-planned']
    error = None
    completed, attempted, initializers = 0, 0, 0
    first_imports = first_exports = None
    with (HERE / 'results.jsonl').open('x') as records:
        for row in fresh:
            attempted += 1
            folder = HERE / 'attempts' / row['id']; folder.mkdir()
            argv = [config['executable']['path'], config['bundle_slice_expected']['path'], row['script']['path'], str(folder / 'output.f32'), '--imports']
            receipt = {'id': row['id'], 'unique_vector': row['unique_vector'], 'fresh_ordinal': row['fresh_ordinal'],
                       'argv': argv, 'child_environment': config['environment'], 'utc_start': utc(), 'pid': None,
                       'exit': None, 'timeout': False, 'cleanup': [], 'attempts': 1, 'error': None,
                       'waveform_prediction': None, 'portable_comparator': None, 'portable_expected': None, 'candidate_grade': None, 'observed_output': None}
            child = None
            try:
                used_bytes=sum(p.stat().st_size for p in HERE.rglob('*') if p.is_file())
                free_bytes=shutil.disk_usage(HERE).free
                receipt['resource_admission']={'packet_bytes':used_bytes,'free_bytes':free_bytes}
                assert used_bytes <= config['resource_policy']['packet_stop_before_next_child_bytes'], 'Packet budget stop'
                assert free_bytes >= config['resource_policy']['minimum_free_before_next_child_bytes'], 'Free-space budget stop'
                receipt['custody_before'] = runtime(config, row)
                with (folder / 'stdout.txt').open('xb') as out, (folder / 'stderr.txt').open('xb') as err:
                    receipt['spawn_utc'] = utc()
                    child = subprocess.Popen(argv, cwd=HERE, env=config['environment'], stdin=subprocess.DEVNULL,
                                             stdout=out, stderr=err, start_new_session=True, preexec_fn=limits)
                    receipt['pid'] = child.pid; started = time.monotonic()
                    try:
                        receipt['exit'] = child.wait(timeout=20)
                    except subprocess.TimeoutExpired:
                        receipt['timeout'] = True
                        os.killpg(child.pid, signal.SIGKILL)
                        receipt['cleanup'].append('SIGKILL selected process group')
                        receipt['exit'] = child.wait(timeout=5)
                    receipt['child_wall_seconds'] = time.monotonic() - started; receipt['child_end_utc'] = utc()
                    out.flush(); err.flush(); os.fsync(out.fileno()); os.fsync(err.fileno())
                for key, name in [('stdout', 'stdout.txt'), ('stderr', 'stderr.txt'), ('output', 'output.f32')]:
                    path = folder / name
                    receipt[key] = D['identity'](path) if path.exists() else None
                assert receipt['exit'] == 0 and not receipt['timeout'], 'Child failed'
                assert receipt['stderr']['bytes'] == 0, 'Nonempty stderr'
                assert receipt['output'] and receipt['output']['bytes'] == 131072, 'Output shape fault'
                assert receipt['stdout']['bytes'] <= 4194304
                protocol = D['protocol']((folder / 'stdout.txt').read_text(), row, config)
                receipt['protocol'] = protocol
                if first_imports is None:
                    first_imports, first_exports = protocol['import_declarations'], protocol['exports_declared_not_all_invoked']
                assert protocol['import_declarations'] == first_imports and protocol['exports_declared_not_all_invoked'] == first_exports
                with (folder / 'output.f32').open('rb') as f:
                    raw = f.read(); os.fsync(f.fileno())
                receipt['observed_output'] = D['metrics'](raw)
                assert receipt['observed_output']['all_finite'], 'Nonfinite in either channel'
                initializers += len(protocol['initializer_entries_logged'])
                completed += 1
            except BaseException as exc:
                receipt['error'] = {'type': type(exc).__name__, 'message': str(exc)}
                if child is not None and child.poll() is None:
                    try:
                        os.killpg(child.pid, signal.SIGKILL); child.wait(timeout=5)
                        receipt['cleanup'].append('failure cleanup SIGKILL selected group/reaped child')
                    except BaseException as cleanup:
                        receipt['cleanup'].append('cleanup error: ' + repr(cleanup))
            finally:
                for key, name in [('stdout', 'stdout.txt'), ('stderr', 'stderr.txt'), ('output', 'output.f32')]:
                    path = folder / name
                    if path.exists():
                        receipt[key] = D['identity'](path)
                try:
                    receipt['custody_after'] = runtime(config, row)
                    assert receipt['custody_after'] == receipt.get('custody_before'), 'Before/after custody mismatch'
                except BaseException as exc:
                    receipt['custody_error'] = repr(exc)
                    if receipt['error'] is None:
                        receipt['error'] = {'type': type(exc).__name__, 'message': 'Custody: ' + str(exc)}
                receipt['utc_end'] = utc()
                records.write(json.dumps(receipt, allow_nan=False) + '\n'); records.flush(); os.fsync(records.fileno())
            print(json.dumps({'ordinal': attempted, 'unique_vector': row['unique_vector'], 'pid': receipt['pid'], 'exit': receipt['exit'], 'error': receipt['error']}), flush=True)
            if receipt['error']:
                error = receipt['error']; break
    source_after = [D['identity'](p['path']) for p in config['source_pins']]
    try:
        assert source_before == source_after
        local_seal()
    except BaseException as exc:
        error = {'type': type(exc).__name__, 'message': 'Final seal/source mismatch: ' + str(exc)}
    save('execution-summary.json', {'status': 'COMPLETE-157-ONCE' if error is None else 'STOPPED-NO-RETRY',
                                  'utc_start': context['utc_start'], 'utc_end': utc(), 'outer_pid': os.getpid(),
                                  'attempted_children': attempted, 'successful_protocols': completed, 'error': error,
                                  'selected_export_calls_with_valid_protocol': completed * 73, 'CalcA_with_valid_protocol': completed * 32,
                                  'loader_initializer_entries_logged_separately': initializers, 'all_native_calls_count': None,
                                  'source_before': source_before, 'source_after': source_after,
                                  'inherited_not_replayed': 1, 'retries': 0, 'unattempted_ids': [r['id'] for r in fresh[attempted:]]})
    if error:
        raise SystemExit('Stopped; retain all partial history. No retry.')


if __name__ == '__main__':
    assert sys.argv[1:] in (['--check-inputs'], ['--run-once'])
    config = json.loads((HERE / 'inputs.json').read_text())
    controls = D['selfchecks'](config)
    if sys.argv[1:] == ['--check-inputs']:
        print(json.dumps({'status': 'PASS data-only inputs', 'controls': controls, 'original_calls': 0, 'image_runtime_reads': 0}))
    else:
        main(config)
