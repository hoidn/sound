"""Route retained manual topics for reconciliation; no coverage or applicability proof."""
from pathlib import Path
import collections
import hashlib
import json
import re
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[4]
I = P.parents[1]/'inventory'
assert sys.argv[1:] in ([], ['--check'])
checking = sys.argv[1:]==['--check']
for pin in json.loads((P/'inputs.json').read_text()):
    raw=(ROOT/pin['path']).read_bytes()
    assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
# Existing canonical entry points only. Missing owners stay explicit; F-01/F-10
# review intro/credits rather than silently excluding them as nonbehavioral.
ROUTES = {
1: ('F-01/F-10', []), 2: ('F-07/F-08', []), 3: ('F-01/F-10', []),
4: ('F-07', ['browser-workflows']), 5: ('F-07', ['project-media-workflows','media-file-workflows']),
6: ('F-02', ['arrangement-editing']), 7: ('F-04', ['session-view-workflows']),
8: ('F-04', ['clip-view-workflows']), 9: ('F-04', ['warp-markers','clip-view-workflows']),
10: ('F-04', ['midi-editing-tools']), 11: ('F-04', ['midi-editing-tools']),
12: ('F-04', ['mpe-workflows']), 13: ('F-04', ['audio-to-midi']),
14: ('F-04', ['groove-workflows']), 15: ('F-04', ['tuning-systems']),
16: ('F-04', ['session-launch-workflows','clip-launch']),
17: ('F-09', ['routing-monitoring-latency']), 18: ('F-09', ['routing-monitoring-latency','mixer-values']),
19: ('F-03', ['recording-comping']), 20: ('F-07', ['bounce-freeze-workflows']),
21: ('F-03', ['recording-comping']), 22: ('F-04/F-07', []),
23: ('F-05', ['bundled-device-hosting']), 24: ('F-05', ['plugin-hosting']),
25: ('F-05', ['device-racks']), 26: ('F-09', ['automation-envelopes']),
27: ('F-04/F-09', ['automation-envelopes','clip-view-workflows']),
28: ('F-07', ['video-workflows']), 29: ('F-06', []), 30: ('F-06', ['native-midi-effects']),
31: ('F-06', []), 32: ('F-05/F-08', ['max-for-live-hosting']),
33: ('F-05/F-08', ['max-for-live-devices']), 34: ('F-08', ['midi-user-mapping']),
35: ('F-08', []), 36: ('F-08', []), 37: ('F-08/F-09', ['synchronization-workflows']),
38: ('F-09', ['bounce-freeze-workflows']), 39: ('F-09', ['mix-graph','mixer-values','audio-video-export']),
40: ('F-09', []), 41: ('F-08', ['keyboard-navigation']),
42: ('F-08', ['keyboard-navigation']), 43: ('F-01/F-10', [])}
assert set(ROUTES)==set(range(1,44))
toc = json.loads((I/'manual-toc.json').read_text())
devices = json.loads((I/'devices.json').read_text())
snapshot = (P/'inventory-owner-routing-input.md').read_text()
device_owners = {}
for line in snapshot.splitlines():
    match = re.match(r'\| `(SURF-[^`]+)` \|', line)
    if match and match[1] in {d['id'] for d in devices}:
        device_owners[match[1]] = re.findall(r'\]\(\.\./specs/([^)#]+\.md)', line)
assert len(device_owners)==102 and all(device_owners.values())
by_id = {r['id']:r for r in toc}
overrides = []
for d in devices:
    if d.get('manual_id') in by_id:
        row = by_id[d['manual_id']]
        owners = device_owners[d['id']]
        if d['name'] in {'Analog','Collision','Corpus','Electric','Tension','Amp','Cabinet'}:
            owners = ['bundled-device-workflows.md']+owners
        overrides.append((row['number'], owners, d['id']))
rows=[]
for row in toc:
    chapter = int(row['number'].split('.')[0])
    plan, names = ROUTES[chapter]
    owners = [n+'.md' for n in names]
    basis = 'chapter-level reconciliation entry points; not a requirement mapping'
    matched = [(prefix, paths, did) for prefix,paths,did in overrides if row['number']==prefix or row['number'].startswith(prefix+'.')]
    profile = None
    if matched:
        prefix,owners,profile = max(matched,key=lambda x:len(x[0]))
        basis = 'exact retained device-manual identity and descendant section number; source semantics pending'
    rows.append(dict(surface_id=row['id'],number=row['number'],title=row['title'],url=row['url'],html_line=row['html_line'],leaf=row['leaf'],plan_parent=plan,candidate_owners=['wiki/specs/'+n for n in owners],device_surface_id=profile,routing_basis=basis,routing_status='candidate-entry-points' if owners else 'canonical-owner-missing',target_applicability='U',requirement_mapping='pending-per-clause-evidence',requirements=[],cases=[],complete=False))
assert len(rows)==880 and sum(r['leaf'] for r in rows)==708 and len({r['surface_id'] for r in rows})==880
assert all((ROOT/path).is_file() for row in rows for path in row['candidate_owners'])
assert all(not row['complete'] and not row['requirements'] and not row['cases'] and row['target_applicability']=='U' for row in rows)
summary=dict(headings=880,leaves=708,chapters=43,headings_with_candidate_entry_points=sum(bool(r['candidate_owners']) for r in rows),headings_without_canonical_owner=sum(not r['candidate_owners'] for r in rows),leaves_with_candidate_entry_points=sum(r['leaf'] and bool(r['candidate_owners']) for r in rows),leaves_without_canonical_owner=sum(r['leaf'] and not r['candidate_owners'] for r in rows),per_clause_mappings_pending=708,complete_topics=0,by_missing_chapter=dict(collections.Counter(r['number'].split('.')[0] for r in rows if not r['candidate_owners'])))
for name,value in [('manual-routing.json',rows),('summary.json',summary),('chapter-routes.json',{str(k):dict(plan_parent=v[0],candidate_owners=['wiki/specs/'+n+'.md' for n in v[1]]) for k,v in ROUTES.items()})]:
    raw=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode();p=P/name
    assert not p.exists() or p.read_bytes()==raw, name
    if checking:
        assert p.is_file(), name
    else:
        p.write_bytes(raw)
if checking:
    for name,pin in json.loads((P/'manifest.json').read_text())['files'].items():
        raw=(P/name).read_bytes()
        assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'],name
print(json.dumps(summary,indent=2))
