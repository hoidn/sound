# usage: python3 -I extract_code.py <out-dir> <label>=<corpus-root>:<entry>[,<entry>...] ...
# Writes <out-dir>/<label>-<entry>.c with the corpus record header and pseudocode, unchanged.
import sys, json, glob, os
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
for spec in sys.argv[2:]:
    label, rest = spec.split('=', 1); root, entries = rest.rsplit(':', 1)
    want = {hex(int(e, 16)) for e in entries.split(',')}
    for f in sorted(glob.glob(root + '/decomp/chunks/*.jsonl')):
        for line in open(f):
            r = json.loads(line)
            if r['entry'] in want:
                want.discard(r['entry'])
                with open(f'{out}/{label}-{r["entry"]}.c', 'w') as o:
                    o.write(f'// {label} {r["entry"]} {r["name"]} state={r["state"]} chunk={os.path.basename(f)} code_sha256={r.get("code_sha256")}\n{r["code"]}')
        if not want: break
    if want: sys.exit(f'{label}: not found {sorted(want)}')
