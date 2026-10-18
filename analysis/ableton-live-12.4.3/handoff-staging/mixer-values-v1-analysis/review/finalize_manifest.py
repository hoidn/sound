# Reviewer step (analyst-side; not payload): set the review and release fields of the staged
# mixer-values-v1 manifest and re-hash every payload file except the manifest itself.
# usage: python3 -I finalize_manifest.py <package dir>
import hashlib, json, sys
from pathlib import Path
d = Path(sys.argv[1]); mp = d / 'manifest.json'
m = json.loads(mp.read_text())
m['release_status'] = 'released'
m['release_date'] = '2026-10-18'
m['review'] = {
    'status': 'approved',
    'reviewers': ['separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; not the author; will not implement'],
    'date': '2026-10-18',
    'findings': [
        'RVM-01 medium: track switch On/Off text and the crossfade curve name binding lacked evidence citations; confirmed by the reviewer\'s own static check; clauses kept, curve-binding assumption removed from the contract, no case changed',
        'RVM-02 low: the upper volume bound was called the binary32 number nearest to 10^(6/20), but it is one step above it; wording corrected, no expectation changed',
        'RVM-03 low: the assumption that some display shows the texts, computed from the value as read, was unstated; named in the contract, no case changed',
        'RVM-04 editorial: comparison obligation now names the On and Off form for the track switch',
        'RVM-05 editorial: payload status wording set to reviewed release; review record added; inventory re-hashed',
        'RVM-06 info: evidence identity re-checked; all hashes matched',
        'RVM-07 info: author inferences ruled on; split pan text and curve binding confirmed; reading rule, code names and display accepted as stated assumptions; no graded text depends on the logarithm last digit',
        'RVM-08 info: the author\'s nine proposed parent-specification corrections confirmed',
        'RVM-09 info: sharing review of three bare numbers also found in shipped sets; acceptable',
    ],
    'disposition': 'Approved with listed corrections (RVM-02 to RVM-04), only for the explicit partial clauses; expectations static-derived; reference and candidate execution not-run; restricted implementation workspace required',
    'record': 'REVIEW.md',
}
files = sorted(p for p in d.rglob('*') if p.is_file() and p.name != 'manifest.json')
m['files'] = [{'path': str(p.relative_to(d)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size} for p in files]
mp.write_text(json.dumps(m, indent=1) + '\n')
print(len(m['files']), 'payload files; manifest sha256', hashlib.sha256(mp.read_bytes()).hexdigest())
