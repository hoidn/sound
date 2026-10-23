"""Inventory the reviewed finite payload; publication is a separate step."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.with_name('device-tension-v1')
cases = json.loads((PACKAGE/'cases.json').read_text())['cases']
requirements = sorted({r for c in cases for r in c['requirements']})
manifest = dict(schema='handoff-manifest-v1', release_id='device-tension-v1', release_status='released', release_date='2026-10-19',
    target='Ableton Live 12 Suite 12.4.3 / macOS arm64; reference audio from original x86_64 code with substituted libraries',
    specification=dict(id='SPEC-DEVICE-TENSION', parent_revision=2, release_revision=1),
    feature_ids=['FEAT-DEVICES'], case_count=len(cases), evaluation_count=len(cases),
    partial_requirement_scopes={r:'Only enumerated comparison-domain vectors, events, histories and graded signal measurements; no general synthesis or application integration' for r in requirements},
    unreleased_requirements=['REQ-DEVICE-TENSION-'+f'{n:03}' for n in [2,3,13,14,15]],
    compatibility_dimensions=dict(audio='Finite measured original-code outputs under reviewed finite criteria; no original-application compatibility', timing='Exact first onset of listed stable/repeated-strike settings only', project_files='excluded', ui='excluded', real_time='excluded'),
    exclusions=['Four chaotic settings and 37 outputs without per-setting numerical calibration; unmeasured modes', 'Unlisted inputs/histories; stored-value mapping; project files; device placement; application integration; general timing, allocator and gain laws; controller and MPE behavior; arm64 execution'],
    reviewer_disposition=dict(status='approved-with-finite-scope', reviewer='Independent handoff-review context separate from candidate author', date='2026-10-19', record='REVIEW.md', corrections=['Explicit nonempty, mono-shape, finite-input, valid-window and required-stable-partial guards'], disposition='27 finite comparisons only; no Live, arm64 or candidate compatibility claim'),
    fixture_origin='Generated zero inputs, generated note sequences, exact numerical vectors and retained original-code output samples; no shipped musical recording or project document',
    files=[dict(path=str(p.relative_to(PACKAGE)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name!='manifest.json'])
(PACKAGE/'manifest.json').write_text(json.dumps(manifest, indent=1)+'\n')
print(hashlib.sha256((PACKAGE/'manifest.json').read_bytes()).hexdigest())
