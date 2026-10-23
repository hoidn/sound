"""Finite review correction; --check reads only, --write refuses after R3 seal.
Retained source predicates stay data. No old checker or original code executes.
"""
from pathlib import Path
from copy import deepcopy
import json,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
assert sys.dont_write_bytecode and sys.argv[1:] in (['--write'],['--check'])
write=sys.argv[1:]==['--write']
assert not(write and (P/'manifest-author-r3.json').exists()),'Frozen R3: writes refused before mutation'
load=lambda p:json.loads(p.read_text())
def emit(n,x):
 raw=x.encode() if isinstance(x,str) else (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
 if write:(P/n).write_bytes(raw)
 else:assert (P/n).read_bytes()==raw,n
old=load(P/'cases-r2.json');now=deepcopy(old);numbers=[10,16,17,24,25,26,27,28,29];deltas=[]
for n in numbers:
 r=now[n-1];assert r['id']==f'AR-{n:03}'
 for field in ['documentary_expected','documentary_comparator']:
  assert r[field] is not None
  deltas.append(dict(pointer=f'/{n-1}/{field}',before=r[field],after=None));r[field]=None
assert sum(r['documentary_expected'] is not None for r in old)==52 and sum(r['documentary_expected'] is not None for r in now)==43
emit('cases-r3.json',now)
emit('delta-r3.json',dict(finding='ARR-R2-REVIEW-001',scope='Nine numeric/duration documentary pairs only. All source/predicate/action/requirement/actual fields unchanged.',case_ids=[f'AR-{n:03}' for n in numbers],field_deltas=deltas,requirements_unchanged=42,cases_unchanged=84,documentary_named=43,documentary_null=41,new_requirements=0,new_cases=0,new_source_claims=0,target='U',executed=0,complete=0))
spec=(P/'spec-r2.md').read_text().replace('revision: 2\n','revision: 3\n',1)
for n in numbers:
 oldrow=next(s for s in spec.splitlines() if s.startswith(f'| AR-{n:03} |'))
 predicate=old[n-1]['original_documentary_predicate'];assert oldrow.endswith(' | '+predicate+' |')
 newrow=oldrow[:-len(predicate)-2]+'Source claim only; documentary numeric/duration outcome and comparator null. '+predicate+' |'
 spec=spec.replace(oldrow,newrow,1)
spec=spec.replace('## Revision 2 source-audit adoption','## Historical revision 2 source-audit adoption',1)
spec+='''\n## Revision 3 documentary oracle correction\n\nRequired ARR-R2-REVIEW-001 found nine numeric/duration predicates paired with\nno-numeric documentary comparators in R2. Current [cases R3](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/cases-r3.json)\nsets both documentary fields null for AR010/016/017/024–029. Exact original\ndocumentary predicates and source claims remain retained source data; no\nrequirement, action, gesture or numerical law changes. Current counts are\n43named documentary pairs and41null pairs across84cases. All actual outcomes\nremain null/U/unexecuted and all42requirement IDs remain unchanged.\n\nThe [R3 packet](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/README-r3.md)\nand [exact eighteen-field delta](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/delta-r3.json)\nretain all R1/R2 files, snapshots and the independent R2 review unchanged.\nR2's52non-null/32null report is historical and its visible-only classification\nis not endorsed. The seven added public-role clauses remain within the held\npartial owner review scope pending separate focused R3 review. No completed\nbehavior, exact12.4.3parity, new runtime result or historical replay is claimed.\n'''
emit('spec-r3.md',spec)
research=(P/'research-r2.md').read_text().replace('revision: 2\n','revision: 3\n',1)
research=research.replace('current checking uses validate-r2.py --check:', 'the historical R2 check was validate-r2.py --check; current R3 uses validate-r3.py --check:',1)
research=research.replace('## Revision 2 retained-source adoption','## Historical revision 2 retained-source adoption',1)
research=research.replace('Current checking uses only the new read-only `validate-r2.py --check`.', 'Historical R2 checking used `validate-r2.py --check`; that whole-file checker is not a current R3 entrypoint and is not replayed.',1)
research+='''\n## Revision 3 review correction\n\nThe [independent R2 review](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/review-owner-r2.json)\nheld adoption for ARR-R2-REVIEW-001: nine numeric/duration documentary\nexpectations conflicted with their no-numeric comparators. The minimum\n[R3 successor](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/README-r3.md)\nsets those eighteen fields null in AR010/016/017/024–029. Historical source\nclaims, predicates, all42requirements/all84actions and actual U/null status\nare unchanged. Current classification is43named/41null; R2's52/32 report and\nits inaccurate visible-only label remain preserved historical evidence.\n\nNo new source, gesture, numeric behavior or case was adopted. All R1/R2 files\nand reviews remain immutable; requirements still use requirements-r2.json,\nwhile current documentary pairs use cases-r3.json. Current checking is only\n`python3 -B analysis/ableton-live-12.4.3/full-spec-v1/arrangement/validate-r3.py --check`.\nIt uses two explicitly inspected pure R2 assertion functions and four pure\nBrowser definitions, never the old main checker/author or a live-canonical\nadapter. Source and delta integrity do not replace the required independent\nfocused review. All exact-build, lifecycle, signal/timing/file and retained\nother unknowns remain U; no compatibility or completion credit follows.\n'''
emit('research-r3.md',research)
if write:
 for file,canonical in [('spec-r3.md','wiki/specs/arrangement-editing.md'),('research-r3.md','wiki/research/arrangement-editing.md')]:
  (ROOT/canonical).write_bytes((P/file).read_bytes())
else:
 for file,canonical in [('spec-r3.md','wiki/specs/arrangement-editing.md'),('research-r3.md','wiki/research/arrangement-editing.md')]:assert (ROOT/canonical).read_bytes()==(P/file).read_bytes()
print(json.dumps(dict(status='authored' if write else 'passed-read-only-derivation',changed_documentary_fields=18,requirements=42,cases=84,documentary_named=43,documentary_null=41,source_or_action_changes=0,target='U',executed=0,complete=0)))
