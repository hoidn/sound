# usage: python3 -I build.py <corpus-root> <out.pkl>
# Builds entry->chunk offset, caller/callee and name maps from a read-only R2 corpus.
import json, os, pickle, glob, sys
C, out = sys.argv[1], sys.argv[2]
off = {}
for f in sorted(glob.glob(C + '/decomp/chunks/*.jsonl')):
    with open(f, 'rb') as fh:
        pos = 0
        for line in fh:
            i = line.find(b'"entry":"') + 9
            off[line[i:line.index(b'"', i)].decode()] = (os.path.basename(f), pos)
            pos += len(line)
callers, callees = {}, {}
with open(C + '/indexes/calls.jsonl') as fh:
    for line in fh:
        r = json.loads(line)
        t = r.get('callee_resolved') or r.get('callee') or r.get('to')
        callees.setdefault(r['caller'], []).append((r['site'], t, r.get('callee_resolved_name') or r.get('callee_name'), r['kind']))
        callers.setdefault(t, []).append((r['site'], r['caller'], r['kind']))
names = {}
with open(C + '/indexes/aliases.jsonl') as fh:
    for line in fh:
        r = json.loads(line); names[r['entry']] = r['name']
pickle.dump((C, off, callers, callees, names), open(out, 'wb'))
print(len(off), len(callers), len(callees), len(names))
