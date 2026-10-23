#!/usr/bin/env python3
"""Read-only stdlib owner-delta/integrity check. Never import prior scripts or audio tools."""
import hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];F='analysis/ableton-live-12.4.3/full-spec-v1/'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(b,p):assert len(b)==p['bytes'] and sha(b)==p['sha256'],p
pins=read(H/'source-pins.json');delta=read(H/'owner.delta.json');preserve=read(H/'preservation.json')
for p in pins['pins']:verify((R/p['path']).read_bytes(),p)
for p in pins['selected_history_source_spans']:
 a,b=p['lines'];text=(R/p['path']).read_text().splitlines(keepends=True);assert sha(''.join(text[a-1:b]).encode())==p['span_sha256']
current=(R/'wiki/specs/device-analog.md').read_bytes();verify(current,delta['new_owner'])
assert delta['new_owner']==preserve['new_owner']==pins['current_owner_as_of']
assert delta['old_owner']==preserve['old_owner']==pins['historical_owner']
assert delta['old_owner']['bytes']==45184 and delta['old_owner']['sha256']=='a63ceb8be20b5c24a7b3270ead540f45f79ee2eb01032d7f17516913c4ccd993'
def reverse(s):
 for e in reversed(delta['edits']):
  if e.get('append'):
   assert s.endswith(e['new']);s=s[:-len(e['new'])]
  else:
   assert s.count(e['new'])==1;s=s.replace(e['new'],e['old'],1)
 return s
def forward(s):
 for e in delta['edits']:
  if e.get('append'):s+=e['new']
  else:
   assert s.count(e['old'])==1;s=s.replace(e['old'],e['new'],1)
 return s
old=reverse(current.decode());verify(old.encode(),delta['old_owner']);assert forward(old).encode()==current
assert sum(len(e['old'].encode())for e in delta['edits'])<45184//4,'full snapshot or excessive historical duplication'
def reqs(s):return {m[1]:m[0]for m in re.finditer(r'^### REQ-DEVICE-ANALOG-(\d{3})[^\n]*\n.*?(?=^### REQ-|^## Timing and state)',s,re.M|re.S)}
def protected(s):
 req=reqs(s);assert set(req)=={f'{i:03}'for i in range(1,24)}
 for key,p in preserve['unchanged_requirement_bodies'].items():
  verify(req[key].encode(),dict(p,path='REQ'+key))
 rows=''.join(l for l in s.splitlines(keepends=True)if l.startswith('| DAN-'));p=preserve['case_rows'];verify(rows.encode(),dict(p,path='39case rows'))
 ids=[]
 for l in rows.splitlines():
  for a,b in re.findall(r'(\d{3})(?:–(\d{3}))?',l.split('|')[1].replace('DAN-','')):ids.extend(range(int(a),int(b or a)+1))
 assert ids==list(range(1,48)) and len(rows.splitlines())==39
 accept=s[s.index('## Acceptance cases'):s.index('## Open questions')];verify(accept.encode(),dict(preserve['acceptance_section'],path='acceptance section'))
 return req
protected(old);req=protected(current.decode());assert len(preserve['unchanged_requirement_bodies'])==22
assert req['022']!=reqs(old)['022']
def scope(s):
 r=reqs(s)['022'];assert '- **X.**' not in r and '| Parameter |' not in r
 for unsupported in ['Amplifier AttackTime, during sustain','g′ + 4,402','is graded only after the change has settled','early or late by up to one Live block plus one period']:
  assert unsupported not in r,unsupported
 for required in ['- **U.** The first output change','smoothing','prior note/control history','settling time and timing for other controls','trajectories are not graded','No general first-change rule, 100 ms settling bound or portable','- **U.** In Live','no\n  host-arrival or automation-delay bound','**Ungraded discovery only.**','A held key does not\n  establish an accepted envelope stage','neither\n  general latching nor absence of an effect in other histories','No ARM execution']:
  assert required in r,required
 assert 'evidence_status: partial (REQ-022 timing/trajectories U; r2 pending independent review)' in s
 assert '\nrevision: 2\n' in s and '## Revision 2 disposition' in s and '## Historical revision 1 evidence qualification' in s
 assert 'its “being authored” and unchanged-body statements describe that\nstage, not current work' in s
scope(current.decode())
# The prior historical stale notice body remains verbatim; only heading framing changed.
old_notice=old[old.index('## Current evidence qualification'):].split('\n',1)[1]
new_notice=current.decode()[current.decode().index('## Historical revision 1 evidence qualification'):current.decode().index('## Revision 2 disposition')].split('\n',1)[1]
assert new_notice.rstrip('\n')==old_notice.rstrip('\n')
reviewpath=F+'reviews/batch-analog-change-history-v1-actual-review.json';review=read(R/reviewpath)
assert (R/reviewpath).stat().st_size==20514 and sha((R/reviewpath).read_bytes())=='42883ae34c203ce530c203e9826520532aaffe4be81a58eb3d7b1c5aa9f73bbe'
assert review['disposition']=='approved-bounded-ungraded-actual-results' and review['result_grade']=='UNGRADED-discovery-only' and review['findings']==[]
assert review['reviewed_manifest']['sha256']=='655b36ebb0f639e0d83522167159efe076fed2867aaa9e246530ba74f601d54a'
obs=review['finite_observations'];assert len(obs)==8 and [v['index']for v in obs]==[52,45,68,2,71,31,34,105]
assert sum(v['first_numeric_difference']['joint']is not None for v in obs)==7
assert obs[-1]['first_numeric_difference']==dict(left=None,right=None,joint=None) and obs[-1]['full_byte_identity']is True
actual=read(R/(F+'batch-analog-change-history-v1-actual/actual-record.json'));assert len(actual['pairs'])==8 and len(actual['runs'])==16
for pair,ob in zip(actual['pairs'],obs):
 m=pair['measurement'];assert m['prechange_numeric_identity'] and m['prechange_byte_identity']
 assert m['first_numeric_difference']==ob['first_numeric_difference'] and pair['expectation']=='unknown; no grade'
readiness=read(R/(F+'reviews/analog-change-history-v1-readiness-review.json'));assert readiness['ready_for_root_execution']is True and readiness['reviewed_manifest']['sha256']==review['preparation_manifest']['sha256']
correction=read(R/(F+'reviews/family-analog-routes-v2-review.json'));assert correction['disposition']=='approved-bounded-family-route-correction'
assert correction['reviewed_manifest']['sha256']=='44e0d729932f4d6626641b959d50db9ee178b07d141e666c55127b5ccb1e087d'
route=read(H/'route-delta.json');assert route['predecessor_contexts']['outcome_ids']==[f'AN-OUT-{i}'for i in range(222,232)] and route['actual_result_grade']=='UNGRADED-discovery-only'
assert 'not a newly derived' in route['counting'] and 'No route/outcome/grade is re-derived' in route['preservation']
# Selected raw files are pinned, not remeasured; no obsolete checker is run.
neg=[]
def rejects(name,fn):
 try:fn()
 except (AssertionError,ValueError,KeyError):neg.append(name)
 else:raise AssertionError('negative fixture accepted '+name)
rejects('changed canonical byte',lambda:verify(current+b'x',delta['new_owner']))
rejects('bad reversal suffix',lambda:reverse(current.decode()+'x'))
rejects('other requirement body mutation',lambda:protected(current.decode().replace('### REQ-DEVICE-ANALOG-001 — reference renders define the output','### REQ-DEVICE-ANALOG-001 — MUTATED')))
rejects('existing case row mutation',lambda:protected(current.decode().replace('| DAN-001 |','| DAN-999 |')))
rejects('old unsupported REQ022 restored',lambda:scope(current.decode().replace(req['022'],reqs(old)['022'])))
rejects('100ms grade reintroduced',lambda:scope(current.decode().replace('**Ungraded discovery only.**','is graded only after the change has settled')))
rejects('discovery generalized into X law',lambda:scope(current.decode().replace('**Ungraded discovery only.**','- **X.** AttackTime is always unchanged')))
rejects('U removed',lambda:scope(current.decode().replace('- **U.** The first output change','- **X.** The first output change')))
assert len(forward(old).encode())==delta['new_owner']['bytes']
if (H/'manifest.json').exists():
 manifest=read(H/'manifest.json')
 for name,p in manifest['files'].items():verify((H/name).read_bytes(),dict(p,path=name))
print(json.dumps({'status':'PASS','scope':'data-only selected pins/spans/review metadata and reversible owner correction; no original/measurement/model/comparator execution','old_owner':delta['old_owner'],'new_owner':delta['new_owner'],'preserved_requirement_bodies':22,'requirement_ids':23,'preserved_case_rows':39,'preserved_case_ids':47,'historical_notice_body':'exact','retained_reviewed_discoveries':8,'discovery_grade':'UNGRADED-only','negative_controls_rejected':neg,'snapshot_retained':False,'new_case_or_grade_or_release':False,'route_qualification':'AN222–231 predecessor-r1 only; no new r2 denominator'},indent=2))
