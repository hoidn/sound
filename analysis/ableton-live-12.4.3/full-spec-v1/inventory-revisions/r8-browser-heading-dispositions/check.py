"""Read-only successor checker; original sealed tuple/list comparison retained."""
from pathlib import Path
import hashlib
import json
import re
import runpy
import sys

P = Path(__file__).resolve().parent
assert sys.argv[1:] == ['--check'] and sys.dont_write_bytecode
before = {str(p.relative_to(P)): hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
tool = runpy.run_path(str(P/'derive.py'))
ROOT, pin, load = tool['ROOT'], tool['pin'], tool['load']
for record in load(P/'inputs.json'): assert pin(ROOT / record['path']) == record
outputs = tool['derive']()
for name,data in outputs.items():
    assert load(P/name) == json.loads(json.dumps(data)), name
for manifest_name in ('manifest.json','manifest-r2.json'):
    manifest = load(P/manifest_name)
    for record in manifest['files']: assert pin(ROOT/record['path']) == record
manifest = load(P/'manifest-r2.json')
assert {r['path'] for r in manifest['files']} == {str(p.relative_to(ROOT)) for p in P.iterdir() if p.is_file() and p.name != 'manifest-r2.json'}
for p in P.iterdir():
    if p.is_file():
        text=p.read_text(); assert text.endswith('\n') and all(line == line.rstrip() for line in text.splitlines()), p
        if p.suffix == '.md':
            for link in re.findall(r'\]\(([^)]+)\)',text): assert (p.parent/link.split('#')[0]).resolve().exists(), link
assert before == {str(p.relative_to(P)): hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
print(json.dumps(dict(status='passed-read-only', manifest_sha256=pin(P/'manifest-r2.json')['sha256'], inputs=len(load(P/'inputs.json')), payloads=len(manifest['files']), summary=outputs['summary.json']),indent=2))
