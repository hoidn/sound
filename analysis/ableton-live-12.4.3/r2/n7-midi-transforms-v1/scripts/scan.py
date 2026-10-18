"""scan.py OUT REGEX... : list corpus functions whose code matches all regexes (entry, name, lines)."""
import sys, json, glob, re
pats = [re.compile(p) for p in sys.argv[2:]]
out = open(sys.argv[1], 'w')
for p in sorted(glob.glob('/var/tmp/sound-analysis/corpus/decomp/chunks/chunk-*.jsonl')):
    with open(p) as f:
        for line in f:
            r = json.loads(line); c = r.get('code') or ''
            if all(q.search(c) for q in pats):
                out.write('%s %s %d\n' % (r['entry'], r['name'], c.count('\n')))
