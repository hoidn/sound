"""Inventory the unreviewed payload; publication is a separate step."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.with_name('device-electric-v1')
cases = json.loads((PACKAGE/'cases.json').read_text())['cases']
requirements = sorted({r for c in cases for r in c['requirements']})
manifest = dict(schema='handoff-manifest-v1', release_id='device-electric-v1', release_status='staged-unreviewed', release_date=None,
    target='Ableton Live 12 Suite 12.4.3 / macOS arm64; reference audio from original x86_64 code with substituted libraries',
    specification=dict(id='SPEC-DEVICE-ELECTRIC', parent_revision=2, release_revision=1),
    feature_ids=['FEAT-DEVICES'], case_count=len(cases), evaluation_count=len(cases),
    partial_requirement_scopes={r:'Only enumerated comparison-domain vectors, events, histories and graded signal measurements; no general synthesis or application integration' for r in requirements},
    unreleased_requirements=['REQ-DEVICE-ELECTRIC-'+f'{n:03}' for n in [2,3,4,13,16]],
    compatibility_dimensions=dict(audio='Finite measured original-code outputs under proposed criteria; no original-application compatibility', timing='Frozen onset windows and three named parameter histories only', project_files='excluded', ui='excluded', real_time='excluded'),
    exclusions=['Three unstable-envelope settings; random waveform and random-component level; ungraded windows/bands/partials', 'Unlisted inputs/histories; stored-value mapping; project files; device placement; application integration; general timing, allocator and gain laws; controller and MPE behavior; arm64 execution'],
    reviewer_disposition=dict(status='pending', reviewer=None),
    fixture_origin='Generated zero inputs, generated note sequences, exact numerical vectors and retained original-code output samples; no shipped musical recording or project document',
    files=[dict(path=str(p.relative_to(PACKAGE)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name!='manifest.json'])
(PACKAGE/'manifest.json').write_text(json.dumps(manifest, indent=1)+'\n')
print(hashlib.sha256((PACKAGE/'manifest.json').read_bytes()).hexdigest())
