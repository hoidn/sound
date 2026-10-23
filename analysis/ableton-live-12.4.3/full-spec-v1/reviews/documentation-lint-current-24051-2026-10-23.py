from pathlib import Path
import datetime,json,re,subprocess,hashlib
root=Path('/home/ollie/Documents/sound');D=root/'analysis/ableton-live-12.4.3/full-spec-v1/reviews';h=D/'documentation-lint-v2.py';ns={'__file__':str(h.resolve())};exec(compile(h.read_text().split("assert slug('REQ-ONE")[0],str(h),'exec'),ns)
base=json.loads((D/'documentation-lint-2026-10-19-v1.json').read_text())['existing_broken_links']
names=['wiki/specs/feature-map.md','wiki/research/full-live-coverage-inventory.md','wiki/decisions/adr-0006-reference-observation-reopened.md','wiki/specs/device-analog.md','wiki/research/phase4-probe-batch.md','wiki/research/native-analysis-recovery.md','wiki/project.md','wiki/specs/device-tension.md','wiki/specs/device-corpus.md','wiki/specs/device-electric.md','wiki/research/device-collision-dsp.md','wiki/research/device-electric-dsp.md','wiki/specs/index.md','wiki/research/device-tension-dsp.md','wiki/research/corpus-dsp-static.md','wiki/research/device-analog-dsp.md','wiki/research/index.md','wiki/research/full-live-specification-plan.md','wiki/research/session-handoff.md','wiki/research/native-decompilation-roadmap.md','wiki/verification/coverage.md','wiki/log.md','wiki/research/full-live-specification-design.md']
errors=[]
for name in names:
 p=root/name;s=p.read_text();m=re.match(r'^---\n(.*?)\n---\n',s,re.S);meta=dict(re.findall(r'^(\w+):\s*(.+)$',m[1],re.M))if m else{}
 for k in ['id','type','status','updated','access']:
  if k not in meta:errors.append(name+' missing '+k)
 datetime.date.fromisoformat(meta['updated']);assert '\x00'not in s
 bad=set(ns['broken'](p.resolve(),s))-set(base.get(name,[]))
 if bad:errors.append([name,sorted(bad)])
a=(root/'wiki/research/full-live-specification-plan.md').read_text().split('### Current execution checkpoint',1)[1].split('#### Earlier checkpoint',1)[0].strip();b=(root/'wiki/research/session-handoff.md').read_text().split('## Current selection',1)[1].split('## Read first',1)[0].strip();assert a==b and '**24,051 new draft case IDs**'in a
old=subprocess.check_output(['git','show','HEAD:wiki/log.md'],cwd=root);assert(root/'wiki/log.md').read_bytes().startswith(old)
design=(root/'wiki/research/full-live-specification-design.md').read_text()
for start,end,want in [('## Revision 15 proposal','## User-adopted revision 15 decision','7dd7bbf101a2ed2b5781b912b3c820d6dc8b1e94806a1a3af147b47039bd8431'),('## Revision 16 proposal','## Revision 16 DATA-policy review','ce691335946dfd360115b926f8f63d765eb557f7bb37603961cafddc81941a7a')]:
 fragment=design[design.index(start):design.index(end)];assert hashlib.sha256(fragment.encode()).hexdigest()==want
check=subprocess.run(['git','diff','--check','--',*names],cwd=root,capture_output=True,text=True)
if check.returncode:errors.append(check.stdout+check.stderr)
print(json.dumps(dict(status='PASS'if not errors else'FAIL',pages=len(names),errors=errors,checkpoint_equal=a==b,appendonly_log=True,historical_proposals_unchanged=True),indent=2));assert not errors
