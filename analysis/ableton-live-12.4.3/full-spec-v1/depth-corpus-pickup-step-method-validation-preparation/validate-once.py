"""One explicitly selected stdlib measurement; no native code, DSP, fitting or FFT."""
from pathlib import Path
import datetime, hashlib, json, math, struct, sys

PRE = Path(__file__).resolve().parent
DEST = PRE.with_name('depth-corpus-pickup-step-method-validation')
REF_SHA = '1336d90115bd24c058e556aa95e9140014d168dad7111dec64eb8edd1d977e73'
TAU = 0.01
AXES = [('preL', 4096, 8192, 0), ('preR', 4096, 8192, 1),
        ('postL', 8192, 16384, 0), ('postR', 8192, 16384, 1)]

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()
def ident(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': sha(data)}
def save(path, value):
    with path.open('x') as f: f.write(json.dumps(value, indent=2, allow_nan=False) + '\n')
def pack(values): return struct.pack('<32768f', *values)

def decode(data):
    if len(data) != 131072: raise ValueError('Expected exactly 16384 stereo binary32 frames')
    values = struct.unpack('<32768f', data)
    if not all(math.isfinite(v) for v in values): raise ValueError('Nonfinite full-file sample')
    return values

def admit(error):
    return math.isfinite(error) and 0 <= error <= TAU

def invalid(reason):
    return {'valid': False, 'pass': False, 'reason': reason,
            'axes': [dict(axis=a, window=[lo, hi], channel=c, valid=False,
                          reference_energy=None, candidate_energy=None, error_energy=None,
                          error=None, tolerance=TAU, **{'pass': False}) for a, lo, hi, c in AXES]}

def compare_arithmetic(reference, candidate):
    """Pure arithmetic fixture entry: no real-reference trust; compare_real gates before reuse."""
    try: ref, trial = decode(reference), decode(candidate)
    except ValueError as exc: return invalid(str(exc))
    rows = []
    for axis, lo, hi, channel in AXES:
        r, y = ref[lo*2+channel:hi*2:2], trial[lo*2+channel:hi*2:2]
        er, ey = math.fsum(v*v for v in r), math.fsum(v*v for v in y)
        delta = math.fsum((a-b)*(a-b) for a, b in zip(y, r))
        valid = math.isfinite(er) and math.isfinite(ey) and er > 0 and ey > 0
        error = math.sqrt(delta/er) if valid else None
        rows.append(dict(axis=axis, window=[lo, hi], channel=channel, valid=valid,
                         reference_energy=er, candidate_energy=ey, error_energy=delta,
                         error=error, tolerance=TAU, **{'pass': valid and admit(error)}))
    return {'valid': all(r['valid'] for r in rows), 'pass': all(r['pass'] for r in rows), 'axes': rows}

def compare_real(reference, candidate):
    """Mandatory identity gate for EVERY real-reference measurement, no bypass option."""
    if sha(reference) != REF_SHA: return invalid('Real reference hash differs from pinned pickup step')
    return compare_arithmetic(reference, candidate)

def controls(reference, control, dest):
    results, requirements = [], []
    raw = dest/'controls'
    raw.mkdir(exist_ok=False)
    def require(name, ok):
        requirements.append({'name': name, 'pass': bool(ok)})
    def record(name, ref, data, *, synthetic=False, expected=None):
        path = raw/(name+'.f32')
        with path.open('xb') as f: f.write(data)
        result = compare_arithmetic(ref, data) if synthetic else compare_real(ref, data)
        row = {'name': name, 'path': str(path), 'bytes': len(data), 'sha256': sha(data),
               'reference_sha256': sha(ref), 'synthetic_arithmetic_only': synthetic,
               'expected_pass': expected, 'result': result}
        results.append(row)
        save(raw/(name+'.json'), row)  # Each actual four-axis result survives a later failure.
        if expected is not None: require(name+' outcome', result['pass'] is expected)
        return result
    self_result = record('step-self', reference, reference, expected=True)
    require('self all four zero', all(r['valid'] and r['error'] == 0 for r in self_result['axes']))
    ignored = record('ignored-step-control', reference, control, expected=False)
    require('ignored-step positive postL failure only', ignored['valid']
            and ignored['axes'][2]['error'] > TAU
            and all(ignored['axes'][i]['pass'] and ignored['axes'][i]['error'] == 0 for i in (0, 1, 3)))
    values, control_values = list(decode(reference)), decode(control)
    # Four independent positive-energy corruption files, one per axis.
    for index, (axis, lo, hi, channel) in enumerate(AXES):
        changed = values.copy()
        for i in range(lo*2+channel, hi*2, 2): changed[i] *= 1.02
        result = record('scaled-1p02-'+axis, reference, pack(changed), expected=False)
        require(axis+' positive finite error rejects', result['valid'] and result['axes'][index]['error'] > TAU
                and not result['axes'][index]['pass'])
        require(axis+' other three remain self', all(result['axes'][i] == self_result['axes'][i]
                                                    for i in range(4) if i != index))
    for axis, lo, hi, channel in AXES:
        changed = values.copy()
        for i in range(lo*2+channel, hi*2, 2): changed[i] = 0.0
        result = record('zero-'+axis, reference, pack(changed), expected=False)
        require(axis+' zero energy invalid', not result['valid'])
    for name, data in [('all-zero', bytes(131072)), ('short', reference[:-4]),
                       ('extra', reference+bytes(4)), ('odd', reference[:-1]),
                       ('prefix-NaN', struct.pack('<f', math.nan)+reference[4:]),
                       ('last-Inf', reference[:-4]+struct.pack('<f', math.inf))]:
        result = record(name, reference, data, expected=False)
        require(name+' invalid not a scored pass', not result['valid'])
    # Real identity must reject wrong references even on their own self-comparison.
    wrong = record('wrong-real-reference', control, control, expected=False)
    require('wrong hash gated before math', wrong.get('reason') == 'Real reference hash differs from pinned pickup step')
    # A synthetic reference is explicitly separated from compare_real, never a runtime option.
    synthetic = [0.0]*32768
    for _, lo, _, channel in AXES: synthetic[lo*2+channel] = 100.0
    synthetic_ref = pack(synthetic)
    with (raw/'synthetic-reference.f32').open('xb') as f: f.write(synthetic_ref)
    record('synthetic-self', synthetic_ref, synthetic_ref, synthetic=True, expected=True)
    result = record('synthetic-rejected-by-real-gate', synthetic_ref, synthetic_ref, expected=False)
    require('synthetic has no real trust', result.get('reason') == 'Real reference hash differs from pinned pickup step')
    bits = struct.unpack('<I', struct.pack('<f', 101.0))[0]
    boundary_values = [('below', struct.unpack('<f', struct.pack('<I', bits-1))[0]),
                       ('boundary', 101.0), ('above', struct.unpack('<f', struct.pack('<I', bits+1))[0])]
    for index, (axis, lo, _, channel) in enumerate(AXES):
        for label, value in boundary_values:
            changed = synthetic.copy()
            changed[lo*2+channel] = value
            result = record('synthetic-'+axis+'-'+label, synthetic_ref, pack(changed), synthetic=True,
                            expected=label != 'above')
            require(axis+' '+label+' numeric boundary', result['valid']
                    and (result['axes'][index]['error'] == TAU if label == 'boundary'
                         else (result['axes'][index]['error'] > TAU if label == 'above'
                               else result['axes'][index]['error'] < TAU)))
            require(axis+' '+label+' other axes zero', all(result['axes'][i]['error'] == 0
                                                         for i in range(4) if i != index))
    result = record('synthetic-zero-reference', bytes(131072), synthetic_ref, synthetic=True, expected=False)
    require('synthetic reference energy checked', not result['valid'])
    nan_ref = struct.pack('<f', math.nan)+synthetic_ref[4:]
    with (raw/'synthetic-NaN-reference-input.f32').open('xb') as f: f.write(nan_ref)
    result = record('synthetic-NaN-reference', nan_ref,
                    synthetic_ref, synthetic=True, expected=False)
    require('synthetic reference full finite checked', not result['valid'])
    scalar_tests = []
    for name, value, expected in [('zero', 0., True), ('inclusive', TAU, True),
                                  ('outside', math.nextafter(TAU, math.inf), False),
                                  ('negative', -1., False), ('NaN', math.nan, False), ('Inf', math.inf, False)]:
        got = admit(value)
        scalar_tests.append({'name': name, 'value_repr': repr(value), 'pass': got, 'expected': expected})
        require('scalar '+name, got is expected)
    # Deliberate aggregate-budget limitations; no latency or smoothing interpretation.
    point = values.copy()
    point[-1] += .005*math.sqrt(self_result['axes'][3]['reference_energy'])
    record('last-sample-concentrated-error', reference, pack(point), expected=True)
    for delay in (1, 512):
        changed = values.copy()
        for n in range(8192, 16384):
            for channel in (0, 1):
                changed[2*n+channel] = control_values[2*n+channel] if n < 8192+delay else values[2*(n-delay)+channel]
        record('artificial-waveform-splice-'+str(delay), reference, pack(changed))
    tail = values.copy()
    tail[15872*2:] = [0.0]*(512*2)
    record('last512-zeroed-limit', reference, pack(tail))
    prefix = values.copy()
    prefix[0] = 123.
    record('finite-prefix-not-scored', reference, pack(prefix), expected=True)
    return {'comparisons': results, 'requirements': requirements, 'scalar_boundary_tests': scalar_tests,
            'comparison_count': len(results), 'axis_records': sum(len(r['result']['axes']) for r in results),
            'all_required_controls_pass': all(r['pass'] for r in requirements),
            'grade': None, 'new_cases': 0, 'new_native_calls': 0,
            'limits': 'Finite criterion validation only; no smoothing duration/latency/right-invariance/A1/Live/candidate law.'}

def main():
    if sys.argv[1:2] != ['--validate-selected-once'] or len(sys.argv) != 3:
        raise SystemExit('Exact Root-selected one-shot invocation and reviewed manifest SHA required; no replay/self-test mode.')
    assert sys.dont_write_bytecode, 'Run with python3 -B'
    seal = PRE/'manifest-preparation.json'
    if sha(seal.read_bytes()) != sys.argv[2]: raise SystemExit('Preparation manifest hash mismatch')
    manifest = json.loads(seal.read_text())
    assert {r['path'] for r in manifest['files']} == {f.name for f in PRE.iterdir() if f.is_file() and f != seal}
    for row in manifest['files']:
        data = (PRE/row['path']).read_bytes()
        assert len(data) == row['bytes'] and sha(data) == row['sha256']
    inputs = json.loads((PRE/'inputs.json').read_text())
    pins = inputs['pins']
    for row in pins: assert ident(Path(row['path'])) == {k:row[k] for k in ('path','bytes','sha256')}
    watched = {Path(r['path']) for r in pins} | {f for f in PRE.iterdir() if f.is_file()}
    for role in ('capture_manifest', 'published_v4_manifest'):
        parent = next(r for r in pins if r['role'] == role)
        for row in json.loads(Path(parent['path']).read_text())['files']:
            path = Path(parent['path']).parent/row['path']
            data = path.read_bytes()
            assert len(data) == row['bytes'] and sha(data) == row['sha256']
            watched.add(path)
    before = [ident(f) for f in sorted(watched)]
    reference = Path(next(r['path'] for r in pins if r['role']=='step_reference')).read_bytes()
    control = Path(next(r['path'] for r in pins if r['role']=='matched_control')).read_bytes()
    assert sha(reference) == REF_SHA
    DEST.mkdir(exist_ok=False)  # Never reuse or remove a partial run.
    source = DEST/'source-preparation'
    source.mkdir(exist_ok=False)
    for path in PRE.iterdir():
        if path.is_file():
            with (source/path.name).open('xb') as f: f.write(path.read_bytes())
    save(DEST/'watch-before.json', before)
    save(DEST/'attempt.json', {'started_utc': utc(), 'manifest_sha256': sys.argv[2],
        'argv': sys.argv, 'python': sys.version, 'platform': sys.platform, 'byteorder': sys.byteorder,
        'scope': 'One data-only validator run, no native/model/fit/FFT/comparator imports.',
        'grade': None, 'source_selection_is_separate': True})
    result = None
    try:
        result = controls(reference, control, DEST)
        save(DEST/'results.json', result)
    except Exception as exc:
        save(DEST/'failure.json', {'exception': repr(exc), 'ended_utc': utc(),
                                 'scope': 'Partial files retained; no retry or criterion change selected.'})
        raise
    finally:
        after = [ident(f) for f in sorted(watched)]
        changed = [{'before': a, 'after': z} for a, z in zip(before, after) if a != z]
        save(DEST/'watch-after.json', {'ended_utc': utc(), 'files': after, 'changed': changed})
    print(json.dumps({'destination': str(DEST), 'comparisons': result['comparison_count'],
        'axis_records': result['axis_records'], 'required_checks': len(result['requirements']),
        'all_required_controls_pass': result['all_required_controls_pass'],
        'watched': len(before), 'watch_unchanged': not changed, 'grade': None}, indent=2))
    return 0 if result['all_required_controls_pass'] and not changed else 1

if __name__ == '__main__': raise SystemExit(main())
