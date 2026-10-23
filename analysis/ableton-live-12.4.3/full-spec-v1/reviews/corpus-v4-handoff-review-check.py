"""Independent finite export checks: isolated new B CLI only; no old numerical fits."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile

ROOT = Path('/home/ollie/Documents/sound')
S = ROOT/'analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v4'
A = S.parent/'device-corpus-v4-analysis'
OLD = ROOT/'handoff/device-corpus-v3'


def identity(path):
    raw = path.read_bytes()
    return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def main():
    assert sys.argv[1:] == ['--check']
    assert identity(S/'manifest.json') == dict(bytes=20042,sha256='8b306ac4e25128b2790bdb46e8e9bd1dae9e6fe06770755a4b126bc714f78c5d')
    inputs = json.loads((A/'inputs.json').read_text())
    paths = {p for d in (S,A,OLD) for p in d.rglob('*') if p.is_file()}
    paths.update(Path(r['path']) for r in inputs['pins'])
    paths.add(Path(__file__))
    full = ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
    paths.add(full/'depth-corpus-midi-noteoff-decay-zero/raw/gate1-held.f32')
    paths.add(full/'depth-corpus-midi-noteoff-decay-zero-criterion-proposal/results.json')
    before = {str(p):identity(p) for p in sorted(paths)}
    for row in inputs['pins']:
        assert identity(Path(row['path'])) == {k:row[k] for k in ('bytes','sha256')}
    for directory in (S,OLD,A/'comparator-preparation'):
        manifest = json.loads((directory/'manifest.json').read_text())
        for row in manifest['files']:
            assert identity(directory/row['path']) == {k:row[k] for k in ('bytes','sha256')}
    manifest = json.loads((S/'manifest.json').read_text())
    assert len(manifest['files']) == 87
    assert {str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()} == {'manifest.json'} | {r['path'] for r in manifest['files']}
    old = json.loads((OLD/'cases.json').read_text())
    new = json.loads((S/'cases.json').read_text())
    assert new['cases'][:25] == old['cases'] and len(new['cases']) == 26
    assert sum(len(c['evaluations']) for c in old['cases']) == 71
    assert sum(len(c['evaluations']) for c in new['cases']) == 72
    physical = list(OLD.rglob('*.f32'))
    assert len(physical) == 80
    assert all(p.read_bytes() == (S/p.relative_to(OLD)).read_bytes() for p in physical)
    assert len(list(S.rglob('*.f32'))) == 81
    code = (S/'compare.py').read_text()
    branch = code[code.index("        elif kind == 'noteoff_decay_zero_waveform':"):code.index("        elif kind == 'startup':")]
    guard = code[code.index("                if evaluation['metric']['kind'] == 'noteoff_decay_zero_waveform':"):code.index('                result = compare(')]
    assert len(branch.splitlines()) == 9 and len(guard.splitlines()) == 4
    assert code.replace(branch,'').replace(guard,'') == (OLD/'compare.py').read_text()
    assert code.encode() == (A/'comparator-preparation/compare.py').read_bytes()
    owner = json.loads(next(Path(r['path']).read_text() for r in inputs['pins'] if r['role']=='R6_case'))[0]
    e = new['cases'][-1]['evaluations'][0]
    for key in ('sample_rate_hz','frames','block_frames','parameters','parameter_order','before_parameters','after_parameters','events','metric'):
        assert e[key] == owner['evaluation'][key]
    assert e['id'] == 'CORPUS-AUDIO-026-01' and inputs['case_mapping'][e['id']] == 'DCO-032'
    assert identity(S/e['reference']) == {k:owner['evaluation']['reference'][k] for k in ('bytes','sha256')}
    # Validate carried ACTUAL measurements as DATA; never invoke preparation checker.
    prior = json.loads((A/'comparator-preparation/numeric-results.json').read_text())
    rows = [r for result in prior['old_results'] for r in result['measurements']]
    assert len(prior['old_results']) == 71 and len(rows) == 4793
    assert all(r['pass'] for r in prior['old_results']) and all(r['pass'] for r in rows)
    assert sum(r['error'] != 0 for r in rows) == 311
    assert prior['measured_old_plus_new_self'] == 4795 and len(prior['new_actual_results']['B-self']['measurements']) == 2
    receipt = json.loads((A/'comparator-preparation/execution-receipt.json').read_text())
    assert identity(A/'comparator-preparation/numeric-results.json') == dict(bytes=receipt['stdout_bytes'],sha256=receipt['stdout_sha256'])
    # Inspect source before running only this new stdlib structural checker.
    structural = subprocess.run([sys.executable,'-B',str(A/'check-draft.py'),'--check'],capture_output=True,timeout=30)
    assert structural.returncode == 0 and not structural.stderr
    structural_result = json.loads(structural.stdout)
    assert len(structural_result['unsafe_mutations_rejected']) == 8
    scenarios = []
    with tempfile.TemporaryDirectory(prefix='corpus-v4-review-') as temporary:
        temp = Path(temporary); package = temp/'export'; candidates = temp/'candidate'; candidates.mkdir()
        shutil.copytree(S,package)
        assert all((package/r['path']).read_bytes() == (S/r['path']).read_bytes() for r in manifest['files'])
        for document in package.glob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)',document.read_text()):
                assert (document.parent/target).is_file()
        for document in package.rglob('*'):
            if document.is_file() and document.suffix != '.f32':
                assert not re.search(r'/home/|/var/tmp|wiki/|analysis/|0x10[0-9a-fA-F]{6}',document.read_text())
        ref = (package/e['reference']).read_bytes()
        wrong = (ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-noteoff-decay-zero/raw/gate1-held.f32').read_bytes()
        known = json.loads((ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-noteoff-decay-zero-criterion-proposal/results.json').read_text())
        cases = [('B-self',ref,True),('wrong-held',wrong,False),
                 ('finite-prefix',struct.pack('<ff',3.,-7.)+ref[8:],True),
                 ('late8192-zero',ref[:65536]+bytes(65536),True),
                 ('zero-energy',bytes(131072),False),('short',ref[:-4],False),
                 ('nonfinite-prefix',struct.pack('<f',float('nan'))+ref[4:],False)]
        for name,raw,expected in cases:
            (candidates/(e['id']+'.f32')).write_bytes(raw)
            done = subprocess.run([sys.executable,'-I','-B',str(package/'compare.py'),str(candidates)],cwd=temp,capture_output=True,timeout=30)
            report = json.loads(done.stdout)
            assert done.returncode == 1 and not done.stderr and report['pass'] is False
            assert len(report['results']) == 72 and all(not r['pass'] and 'error' in r for r in report['results'][:-1])
            result = report['results'][-1]
            assert result['id'] == e['id'] and result['pass'] is expected
            if name == 'wrong-held':
                assert [r['error'] for r in result['measurements']] == [r['relative_rms'] for r in known['comparisons']['wrong-fresh-A-held']['channels']]
            if name == 'late8192-zero':
                assert [r['error'] for r in result['measurements']] == [r['relative_rms'] for r in known['deliberately_zeroed_last8192_scope_control']['channels']]
            scenarios.append(dict(name=name,exit=done.returncode,new_B=result,missing_old=71))
        # Alter only TEMPORARY exported reference; frozen package is untouched.
        (package/e['reference']).write_bytes(wrong)
        (candidates/(e['id']+'.f32')).write_bytes(ref)
        done = subprocess.run([sys.executable,'-I','-B',str(package/'compare.py'),str(candidates)],cwd=temp,capture_output=True,timeout=30)
        report = json.loads(done.stdout); result = report['results'][-1]
        assert done.returncode == 1 and not done.stderr and not result['pass']
        assert 'NoteOff zero endpoint reference hash' in result['error']
        scenarios.append(dict(name='wrong-B-reference',exit=done.returncode,new_B=result,missing_old=71))
    after = {str(p):identity(p) for p in sorted(paths)}
    assert before == after
    print(json.dumps(dict(status='PASS finite export/new-B only; no candidate grade',
        stage_manifest=identity(S/'manifest.json'),payloads=87,old_groups_exact=25,old_evaluations_exact=71,old_F32_exact=80,
        new_B_owner_match=True,source_insertions=[9,4],carried_measurements=4795,carried_nonzero_old_errors=311,
        structural=structural_result,isolated_cli=scenarios,
        isolated_cli_limit='Only B candidate file supplied;71oldfiles intentionally missing. Full72object CLI runs return1 with71missing failures, no oldfit/FFT branch executes. These are new-B/export controls, not a wholepackage/candidate pass.',
        watched=len(paths),watch_unchanged=True,watch_sha256=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        comparator_cli_calls=8,original_calls=0,old_numeric_replays=0,grade=None),indent=2))


if __name__ == '__main__':
    main()
