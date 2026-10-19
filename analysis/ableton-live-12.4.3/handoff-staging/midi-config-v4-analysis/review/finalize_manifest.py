"""Set the reviewed fields of the midi-config-v4 manifest and re-hash its inventory (reviewer, analyst side).

  python3 -I -B finalize_manifest.py           # once: reviewed fields, then the inventory
  python3 -I -B finalize_manifest.py rehash    # after a later payload text edit: the inventory only

Keeps key order and the author's json.dumps(indent=1) layout; fails if an expected field is absent or already edited.
"""
import hashlib
import json
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / 'midi-config-v4'
p = PKG / 'manifest.json'
m = json.loads(p.read_text())


def rehash():
    files = sorted(q for q in PKG.rglob('*') if q.is_file() and q.name != 'manifest.json')
    m['files'] = [{'path': str(q.relative_to(PKG)), 'sha256': hashlib.sha256(q.read_bytes()).hexdigest(),
                   'bytes': q.stat().st_size} for q in files]
    p.write_text(json.dumps(m, indent=1) + '\n')
    print(len(m['files']), 'files listed; manifest sha256', hashlib.sha256(p.read_bytes()).hexdigest())


if sys.argv[1:] == ['rehash']:
    assert m['release_status'] == 'released'
    rehash()
    sys.exit()
X = 'extracted execution of the original x86_64 code (glibc substitutions); arm64 equivalence inferred'
assert m['release_status'] == 'candidate-unreviewed' and X in m['expectation_provenance_labels']

m['release_status'] = 'released'
m['release_date'] = '2026-10-18'
r5 = m['partial_requirement_scopes']['REQ-MIDI-USER-005']
assert r5.endswith('; value tolerance tau')
m['partial_requirement_scopes']['REQ-MIDI-USER-005'] = r5 + ' per message, k tau after k relative messages in a row'
m['expectation_provenance_labels'][X] += (
    '; not run: a notification Pick-Up gives after it has decided a value, and the route that applies a value later '
    'instead of at once (the run applied each value at once)')
ex = m['exclusions']['inputs_without_expectation']
vs = [e for e in ex if e.startswith('a Value Scaling move')]
near = [e for e in ex if e.startswith('a takeover comparison or test')]
assert len(vs) == 1 and len(near) == 1
ex[ex.index(vs[0])] = vs[0] + ' (none of them is on a stepped parameter)'
ex.insert(ex.index(near[0]) + 1, 'a target value n or p of a stepped parameter whose exact value lies within 8 tau of a '
          'half-integer, and every later value of its sequence')
assert m['value_tolerance'].endswith('1e-6 for cases MIDI-CONFIG-110 to 127')
m['value_tolerance'] += ('; tau covers one message: a value reached by k relative messages in a row on a parameter '
                         'that is not stepped is compared within k * tau')
s = m['supersession']
s['relationship'] = ('superset with two precision corrections to general midi-config-v3 value clauses: a value reached '
                     'by k relative messages in a row is compared within k * tau, and a stepped target value within '
                     '8 tau of a half-integer has no expectation; no midi-config-v3 case affected; midi-config-v3 stays '
                     'immutable and valid for its own scope apart from those corrections')
ch = s['changes']
assert len(ch) == 11 and ch[4].startswith('value tolerance tau') and ch[5].startswith('stepped rounding') \
    and ch[6].startswith('exclusions') and ch[7].startswith('provenance') and ch[10].startswith('no midi-config-v3')
ch[4] += ('; a value reached by k relative messages in a row on a parameter that is not stepped is compared within '
          'k * tau, because rounding adds up (midi-config-v3: 1e-6); each step of the carried relative cases is exact')
ch[5] += "; a stepped parameter's value after a move has no expectation"
ch[6] = ch[6].replace('added tests within 8 tau of a bound and Value Scaling moves outside the listed cases',
                      'added tests within 8 tau of a bound, stepped target values within 8 tau of a half-integer '
                      '(narrowing the midi-config-v3 rounding rule for such values; no midi-config-v3 case affected) '
                      'and Value Scaling moves outside the listed cases')
assert 'half-integer' in ch[6]
ch[7] += '; the parts of the original code that did not run are named'
ch.insert(9, 'comparison obligations: each choice selected by its entry position with the wording recorded, instead of '
             'confirming the never-acting choice; the crossfader rescaling rule extended to MIDI-CONFIG-150')
ch[11] = ('no midi-config-v3 case, fixture or expectation changed; apart from the two precision corrections, nothing in '
          'midi-config-v3 is contradicted or narrowed; the sentences that left takeover unspecified now point to the '
          'new rules')
m['review'] = {
    'status': 'approved',
    'reviewers': ['separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; '
                  'not the author; will not implement'],
    'date': '2026-10-18',
    'findings': [
        'RV4-01 low: stepped target values within single-precision rounding of a half-integer can round the other '
        'way (14-bit pairs, stepped ranges from 0 to 5000 up); narrowed with the 8 tau band; narrows a midi-config-v3 '
        'clause, no case affected',
        'RV4-02 low: rounding adds up over relative messages in a row (re-run of the original code: 5.2 tau after 200 '
        'messages); compared within k * tau; no case or comparator changed',
        'RV4-03 low: change list missed the comparison obligations; strict-superset wording no longer accurate; '
        'completed and reworded',
        'RV4-04 low: extracted-execution definition did not name the two parts of the code that did not run; named',
        "RV4-05 editorial: a stepped parameter's value after a Value Scaling move has no expectation; clarified",
        'RV4-06 info: the author\'s Value Scaling error figure was sampled; the true error reaches hundreds of tau; '
        'exclusion upheld',
        'RV4-07 info: evidence identity re-hashed, evidence run reproduced byte for byte, every new case re-run',
        'RV4-08 info: catalog wording outside the package not edited',
        'RV4-09 editorial: payload status set to reviewed release; review record added',
    ],
    'disposition': 'Approved with listed narrowing (RV4-01) and clarifications (RV4-02 to RV4-05), only for the '
                   'explicit partial clauses; expectations static-derived or extracted execution as labeled; '
                   'reference and candidate execution not-run; restricted implementation workspace required',
    'record': 'REVIEW.md',
}
rehash()
