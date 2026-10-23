"""Private data-only preparation tests; new comparator functions only, no device synthesis."""
from pathlib import Path
import hashlib
import json
import math
import runpy
import struct
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
V3 = ROOT / 'handoff/device-corpus-v3'
FULL = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check():
    inputs = json.loads((HERE / 'inputs.json').read_text())
    watched = {p: p.read_bytes() for p in HERE.iterdir() if p.is_file()}
    for pin in inputs['pins']:
        p = Path(pin['path']); raw = p.read_bytes()
        assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256']
        watched[p] = raw
    for version in ('v1', 'v2', 'v3'):
        directory = ROOT / ('handoff/device-corpus-' + version)
        seal = directory / 'manifest.json'
        raw = seal.read_bytes(); watched[seal] = raw
        for row in json.loads(raw)['files']:
            p = directory / row['path']; raw = p.read_bytes()
            assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
            watched[p] = raw
    canonical = ROOT / 'wiki/specs/device-corpus.md'
    watched[canonical] = canonical.read_bytes()  # As-of watch only, not an evolving equality pin.
    old, current = (V3 / 'compare.py').read_text(), (HERE / 'compare.py').read_text()
    start = current.index("        elif kind == 'noteoff_decay_zero_waveform':")
    end = current.index("        elif kind == 'startup':", start)
    new_branch = current[start:end]
    start = current.index("                if evaluation['metric']['kind'] == 'noteoff_decay_zero_waveform':")
    end = current.index('                result = compare(', start)
    new_guard = current[start:end]
    assert current.replace(new_branch, '').replace(new_guard, '') == old
    assert len(new_branch.splitlines()) == 9 and len(new_guard.splitlines()) == 4
    assert sha(old.encode()) == 'f4d660c0c8a798d99f8e560f9505705dea9517174fdc0d5fb8151dc126ad0c83'
    assert sha(current.encode()) == '9964de11da79eb61c0624d34e402d238cd5c466093d15ccc91fd630ac4c54110'
    # Disable bytecode before importing even the NEW private module and dependencies.
    bytecode_before = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        module = runpy.run_path(str(HERE / 'compare.py'), run_name='private_comparator_preparation')
        compare, audio, runner, np = [module[k] for k in ('compare', 'audio', 'run', 'np')]
        cases = json.loads((V3 / 'cases.json').read_text())['cases']
        regressions = []
        for case in cases:
            for evaluation in case['evaluations']:
                try:
                    reference = audio(V3 / evaluation['reference'])
                    result = compare(reference, reference, evaluation['metric'], evaluation['sample_rate_hz'])
                except (ValueError, OSError, FloatingPointError, ZeroDivisionError) as exc:
                    result = {'pass': False, 'error': str(exc), 'measurements': []}
                regressions.append({'id': evaluation['id'], **result})
        assert len(regressions) == 71
        rows = [row for result in regressions for row in result['measurements']]
        old_summary = dict(evaluations=len(regressions), measurements=len(rows),
                           passed_evaluations=sum(r['pass'] for r in regressions),
                           passed_measurements=sum(r['pass'] for r in rows),
                           nonzero_errors=[r for r in rows if r['error'] != 0],
                           errors=[r for r in regressions if 'error' in r])
        capture = FULL / 'depth-corpus-midi-noteoff-decay-zero'
        reference = audio(capture / 'raw/gate1-off.f32')
        metric = {'kind': 'noteoff_decay_zero_waveform'}
        fresh = {}
        for name, path in [('B-self', capture / 'raw/gate1-off.f32'),
                           ('wrong-A', capture / 'raw/gate1-held.f32'),
                           ('wrong-C', capture / 'raw/gate0-off.f32'),
                           ('wrong-old-B', FULL / 'depth-corpus-midi-gate-before-impulse/raw/gate1-off.f32')]:
            fresh[name] = compare(audio(path), reference, metric, 44100)
        known = json.loads((FULL / 'depth-corpus-midi-noteoff-decay-zero-criterion-proposal/results.json').read_text())
        for actual, expected in [('B-self', 'B-self'), ('wrong-A', 'wrong-fresh-A-held'),
                                 ('wrong-C', 'wrong-fresh-C-gate0-off'), ('wrong-old-B', 'wrong-old-host34-one-B')]:
            assert [r['error'] for r in fresh[actual]['measurements']] == [r['relative_rms'] for r in known['comparisons'][expected]['channels']]
        tests = []

        def outcome(name, y, r, expected):
            result = compare(y, r, metric, 44100)
            assert result['pass'] is expected, name
            tests.append({'name': name, **result})
            return result

        def invalid(name, y, r):
            try:
                compare(y, r, metric, 44100)
            except ValueError as exc:
                tests.append(dict(name=name, invalid=True, error=str(exc)))
            else:
                raise AssertionError(name)

        r = np.zeros((16384, 2), dtype=np.float64); r[4096, :] = 100.0
        def pair(left, right):
            y = r.copy(); y[4096, :] = (left, right); return y
        outcome('identical-synthetic', r, r, True)
        boundary = outcome('inclusive-boundary', pair(101.0, 101.0), r, True)
        assert [x['error'] for x in boundary['measurements']] == [0.01, 0.01]
        bits = struct.unpack('<I', struct.pack('<f', 101.0))[0]
        below, above = [struct.unpack('<f', struct.pack('<I', bits + step))[0] for step in (-1, 1)]
        outcome('adjacent-below', pair(below, below), r, True)
        outcome('adjacent-above', pair(above, above), r, False)
        outcome('left-only-fail', pair(above, 100.0), r, False)
        outcome('right-only-fail', pair(100.0, above), r, False)
        outcome('half-gain', pair(50.0, 50.0), r, False)
        outcome('polarity', pair(-100.0, -100.0), r, False)
        y = reference.copy(); y[8192:, :] = 0
        tail = outcome('late-zero-limit', y, reference, True)
        assert [x['error'] for x in tail['measurements']] == [x['relative_rms'] for x in known['deliberately_zeroed_last8192_scope_control']['channels']]
        y = reference.copy(); y[4095, 0] = 123.0
        outcome('finite-prefix-outside-metric', y, reference, True)
        y = r.copy(); y[-1, 1] = 2.0
        outcome('last-frame-included', y, r, False)
        invalid('zero-candidate-left', pair(0, 100), r)
        invalid('zero-candidate-right', pair(100, 0), r)
        invalid('zero-candidate-both', pair(0, 0), r)
        invalid('zero-reference-left', r, pair(0, 100))
        # Actual NEW run() exercises each reference guard and file validity, never old CLI/main.
        with tempfile.TemporaryDirectory(prefix='data-only-', dir=HERE) as scratch:
            temporary = Path(scratch); candidates = temporary / 'outputs'; candidates.mkdir()
            ramp_eval = next(e for c in cases for e in c['evaluations'] if e['metric']['kind'] == 'ramp_waveform')
            ramp = (V3 / ramp_eval['reference']).resolve()
            bref = capture / 'raw/gate1-off.f32'
            records = [{'id': 'private-ramp', 'reference': str(ramp), 'metric': {'kind': 'ramp_waveform'}, 'sample_rate_hz': 44100},
                       {'id': 'private-B', 'reference': str(bref), 'metric': metric, 'sample_rate_hz': 44100}]
            (candidates / 'private-ramp.f32').write_bytes(ramp.read_bytes())
            (candidates / 'private-B.f32').write_bytes(bref.read_bytes())
            globals_used = runner.__globals__; original_here = globals_used['HERE']
            globals_used['HERE'] = temporary
            guard_results = {}
            def run_rows(rows):
                (temporary / 'cases.json').write_text(json.dumps({'cases': [{'evaluations': rows}]}))
                return runner(candidates)
            try:
                guard_results['both-correct'] = run_rows(records)
                assert guard_results['both-correct']['pass']
                wrong_B = [dict(r) for r in records]; wrong_B[1]['reference'] = str(ramp)
                guard_results['wrong-B-reference'] = run_rows(wrong_B)
                assert not guard_results['wrong-B-reference']['pass'] and 'NoteOff zero endpoint reference hash' in guard_results['wrong-B-reference']['results'][1]['error']
                wrong_ramp = [dict(r) for r in records]; wrong_ramp[0]['reference'] = str(bref)
                guard_results['wrong-Ramp-reference'] = run_rows(wrong_ramp)
                assert not guard_results['wrong-Ramp-reference']['pass'] and 'Ramp reference hash' in guard_results['wrong-Ramp-reference']['results'][0]['error']
                for name, bad in [('short', bytes(131064)), ('extra', bytes(131080)),
                                  ('NaN-prefix', struct.pack('<f', math.nan) + bytes(131068)),
                                  ('Inf-active', bytes(4096 * 8) + struct.pack('<f', math.inf) + bytes(131072 - 4096 * 8 - 4)),
                                  ('finite-zero', bytes(131072))]:
                    (candidates / 'private-B.f32').write_bytes(bad)
                    guard_results[name] = run_rows(records)
                    assert not guard_results[name]['pass']
            finally:
                globals_used['HERE'] = original_here
    finally:
        sys.dont_write_bytecode = bytecode_before
    for p, raw in watched.items():
        assert p.read_bytes() == raw
    success = old_summary['passed_evaluations'] == 71 and all(r['pass'] for r in rows) and fresh['B-self']['pass']
    return dict(status='Private comparator preparation only; not adopted/released', pass_=success,
                old_summary=old_summary, old_results=regressions, new_actual_results=fresh,
                arithmetic_controls=tests, file_and_identity_controls=guard_results,
                source_reconstruction='Remove only9line newbranch and4line newguard -> exact v3 bytes',
                old_evaluation_objects='Exact unchanged v3cases bytes read; none rewritten',
                preserved_paths=len(watched), all_unchanged=True, original_calls=0, candidate_DSP_calls=0,
                measured_old_plus_new_self=len(rows) + len(fresh['B-self']['measurements']),
                criterion_approval=False, owner_adoption=False, release_approval=False, grade=None)


if __name__ == '__main__':
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no native, model or old-main execution.')
    result = check()
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(0 if result['pass_'] else 1)
