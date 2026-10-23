"""One explicit new-v4 public CLI integration; exact reference selfdata, no device DSP."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path('/home/ollie/Documents/sound')
BASE = ROOT/'analysis/ableton-live-12.4.3'
STAGE = BASE/'handoff-staging/device-corpus-v4'
REVIEWS = BASE/'full-spec-v1/reviews'
OUT = REVIEWS/'corpus-v4-handoff-review-cli-evidence'


def identity(path):
    raw = path.read_bytes()
    return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def main():
    assert sys.argv[1:] == ['--once']
    assert not OUT.exists()
    assert identity(STAGE/'manifest.json') == dict(bytes=20042,sha256='8b306ac4e25128b2790bdb46e8e9bd1dae9e6fe06770755a4b126bc714f78c5d')
    manifest = json.loads((STAGE/'manifest.json').read_text())
    watch_paths = set(p for p in STAGE.rglob('*') if p.is_file())
    watch_paths.update(p for p in REVIEWS.glob('corpus-v4-handoff-review*') if p.is_file())
    before = {str(p):identity(p) for p in sorted(watch_paths)}
    OUT.mkdir()
    with tempfile.TemporaryDirectory(prefix='corpus-v4-full-cli-review-') as temporary:
        temp = Path(temporary); exported = temp/'export'; candidates = temp/'selfdata'
        shutil.copytree(STAGE,exported); candidates.mkdir()
        export_before = {str(p.relative_to(exported)):identity(p) for p in exported.rglob('*') if p.is_file()}
        assert len(export_before) == 88
        for row in manifest['files']:
            assert export_before[row['path']] == {k:row[k] for k in ('bytes','sha256')}
        cases = json.loads((exported/'cases.json').read_text())['cases']
        evaluations = [e for c in cases for e in c['evaluations']]
        assert len(cases) == 26 and len(evaluations) == 72
        candidates_map = {}
        for evaluation in evaluations:
            target = candidates/(evaluation['id']+'.f32')
            with target.open('xb') as stream:
                stream.write((exported/evaluation['reference']).read_bytes())
            candidates_map[target.name] = identity(target)
        argv = [sys.executable,'-I','-B',str(exported/'compare.py'),str(candidates)]
        start = datetime.now(timezone.utc).isoformat(); clock = time.monotonic()
        with (OUT/'stdout.json').open('xb') as stdout, (OUT/'stderr.txt').open('xb') as stderr:
            try:
                process = subprocess.run(argv,cwd=temp,stdout=stdout,stderr=stderr,timeout=120,check=False)
                status = dict(exit=process.returncode,timeout=False)
            except subprocess.TimeoutExpired:
                status = dict(exit=None,timeout=True)
        elapsed = time.monotonic()-clock; end = datetime.now(timezone.utc).isoformat()
        # Preserve actual status before validation; no retry or success-only retention.
        receipt = dict(argv=argv,started_utc=start,finished_utc=end,elapsed_seconds=elapsed,**status,
                       stdout=identity(OUT/'stdout.json'),stderr=identity(OUT/'stderr.txt'),
                       selfdata=True,device_DSP_calls=0,original_calls=0,
                       explicit_scope='One new-v4 CLI with all72 selfdata files; copiedoldmeasurement fit/FFT functions authorized for this actual integration. No releasedoldmain/model or native code.')
        with (OUT/'execution.json').open('x') as stream:json.dump(receipt,stream,indent=2);stream.write('\n')
        assert status == dict(exit=0,timeout=False) and (OUT/'stderr.txt').stat().st_size == 0
        result = json.loads((OUT/'stdout.json').read_text())
        assert result['pass'] and len(result['results']) == 72
        assert [r['id'] for r in result['results']] == [e['id'] for e in evaluations]
        measures = [m for r in result['results'] for m in r['measurements']]
        assert len(measures) == 4795 and all(r['pass'] for r in result['results']) and all(r['pass'] for r in measures)
        assert len(result['results'][-1]['measurements']) == 2
        nonzero = sum(r['error'] != 0 for r in measures)
        assert export_before == {str(p.relative_to(exported)):identity(p) for p in exported.rglob('*') if p.is_file()}
        assert candidates_map == {p.name:identity(p) for p in candidates.iterdir()}
        assert before == {str(p):identity(p) for p in sorted(watch_paths)}
        final = dict(status='PASS new-v4 isolated full CLI integration; reference selfdata only',
                     groups=26,evaluations=72,measurements=4795,nonzero_measurement_errors=nonzero,
                     new_B=result['results'][-1],execution=receipt,
                     exported_files_verified_unchanged=88,selfdata_files_verified_unchanged=72,
                     export_map_sha256=hashlib.sha256(json.dumps(export_before,sort_keys=True).encode()).hexdigest(),
                     candidate_map_sha256=hashlib.sha256(json.dumps(candidates_map,sort_keys=True).encode()).hexdigest(),
                     original_watch_paths=len(before),watch_unchanged=True,
                     watch_map_sha256=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),
                     original_calls=0,candidate_DSP_calls=0,candidate_grade=None)
        with (OUT/'summary.json').open('x') as stream:json.dump(final,stream,indent=2);stream.write('\n')
    print(json.dumps(final,indent=2))


if __name__ == '__main__':
    main()
