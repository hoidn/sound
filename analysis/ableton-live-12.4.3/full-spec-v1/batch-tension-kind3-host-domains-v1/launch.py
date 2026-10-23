"""Frozen parent launch, one exec into the fixed recorder; no original call here."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import sys

HERE = Path(__file__).resolve().parent
assert sys.argv[1:] == ['--run-once']
config = json.loads((HERE / 'inputs.json').read_text())
assert not (HERE / 'attempts').exists()
pre = (HERE / 'pre-call-manifest.json').read_bytes()
argv = ['/usr/bin/python3', '-I', '-B', str(HERE / 'run_batch.py'), '--run-once']
assert argv == config['parent_exec_argv']
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'pid': os.getpid(), 'launch_argv': sys.argv,
           'exec_argv': argv, 'exec_environment': config['environment'], 'core_limit': [0, 0],
           'pre_call_manifest': {'bytes': len(pre), 'sha256': hashlib.sha256(pre).hexdigest()},
           'scope': 'One exec into frozen recorder; same PID expected. No original/harness/model execution in launch.'}
with (HERE / 'launch-receipt.json').open('x') as f:
    json.dump(receipt, f, indent=2, allow_nan=False)
    f.write('\n'); f.flush(); os.fsync(f.fileno())
os.execve(argv[0], argv, config['environment'])
