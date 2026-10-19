"""Reviewer: verify retained corpus excerpts against the corpora (analyst side; output is data).
usage: python3 -I -B excerpt_check.py <excerpts.jsonl> <corpus dir> [entry ...]   (prints code of the entries)"""
import hashlib, json, os, sys
path, corpus, show = sys.argv[1], sys.argv[2], {e.lower() for e in sys.argv[3:]}
ok = bad = 0
for line in open(path):
    r = json.loads(line)
    chunk = r['chunk'] if os.path.isabs(r['chunk']) else os.path.join(corpus, 'decomp/chunks', os.path.basename(r['chunk']))
    with open(chunk, 'rb') as fh:
        fh.seek(r['offset'])
        raw = fh.readline()
    good = hashlib.sha256(raw.rstrip(b'\n')).hexdigest() == r['line_sha256'] or hashlib.sha256(raw).hexdigest() == r['line_sha256']
    good = good and json.loads(raw)['entry'] == r['record']['entry']
    ok += good; bad += not good
    if r['record']['entry'] in show:
        print(f"// {r['record']['entry']}\n{r['record']['code']}")
print(f'{path}: {ok} excerpts match the corpus, {bad} differ')
