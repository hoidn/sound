"""Run the payload CLI from a copy that has no analyst siblings."""
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
source=HERE.with_name('device-corpus-v1')
export=Path(tempfile.mkdtemp(prefix='corpus-handoff-export-'))/'device-corpus-v1'
shutil.copytree(source,export)
report=export.parent/'self-comparison.json'
with report.open('w') as output:
 result=subprocess.run(['python',str(export/'compare.py'),str(export/'reference')],stdout=output,check=False)
r=json.loads(report.read_text());assert result.returncode==0 and r['pass'];assert len(r['results'])==68
m=json.loads((export/'manifest.json').read_text());actual={str(p.relative_to(export)) for p in export.rglob('*') if p.is_file()};assert actual=={f['path'] for f in m['files']}|{'manifest.json'}
for f in m['files']:
 b=(export/f['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==f['sha256'] and len(b)==f['bytes']
out={'status':'pass','directory':str(export),'cli_exit_code':result.returncode,'evaluations_passed':len(r['results']),'manifest_sha256':hashlib.sha256((export/'manifest.json').read_bytes()).hexdigest(),'no_analysis_dependencies':True,'payload_inventory_exact':True}
(HERE/'export-validation.json').write_text(json.dumps(out,indent=1)+'\n');print(json.dumps(out))
