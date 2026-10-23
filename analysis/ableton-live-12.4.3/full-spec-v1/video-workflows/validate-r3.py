"""Read-only research-only R3 editorial successor; immutable R2 checker adapted in memory."""
from pathlib import Path
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--preflight'])
preflight=sys.argv[1:]==['--preflight'];assert not preflight or not (P/'manifest-author-r3.json').exists()
def load(q):return json.loads(q.read_text())
def info(q):
 b=q.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(q,r):assert info(q)=={k:r[k] for k in ['bytes','sha256']},q
before={str(q):info(q) for q in P.rglob('*') if q.is_file()}
response=load(P/'response-r3.json');oldmanifest=P/response['prior_manifest']
assert response['prior_manifest_sha256']==info(oldmanifest)['sha256']=='ab750e6c80197995efb285330c939abb592bfc458d5ab626e68f53543c6fc55f'
m=load(oldmanifest);assert len(m['files'])==42
for n,r in m['files'].items():pin(P/n,r)
pin(ROOT/response['review']['path'],response['review'])
assert response['review']['sha256']=='d9ed5acc8d655f0fd083c77f2743083282e885b10af731d0d5c5808897d4716c'
assert response['resolved_findings']==['VIDEO-R2-REVIEW-001','VIDEO-R2-REVIEW-002'] and response['source_catalog_case_ID_oracle_delta'] is None
assert response['spec_remains_revision']==2 and response['new_full_archive'] is False
text=(P/'research-r2.md').read_text();assert len(response['page_changes'])==5
for change in response['page_changes']:
 assert text.count(change['before'])==1; text=text.replace(change['before'],change['after'],1)
assert text==(P/'research-r3.md').read_text()==(ROOT/'wiki/research/video-workflows.md').read_text()
assert 'revision: 3\n' in text
assert 'Current R2 catalogs retain20requirements\n(18D12/2U) and34cases, including16operational U cases.' in text
assert 'Interior gaps need\n  productive playback on both sides; leading/trailing gaps need independently\n  productive present stream portions and matched positive evidence elsewhere.' in text
assert (P/'spec-r2.md').read_bytes()==(ROOT/'wiki/specs/video-workflows.md').read_bytes()
# Only inspected analyst checker code is compiled. No product/source/example code runs.
old=P/'validate-r2.py';pin(old,m['files']['validate-r2.py']);code=old.read_text()
assert code.count('manifest-author-r2.json')==4
code=code.replace('manifest-author-r2.json','manifest-author-r3.json')
assert code.count("P/'research-r2.md'")==1
code=code.replace("P/'research-r2.md'","P/'research-r3.md'")
before_revision="for q in [sp,rp]:assert 'revision: 2\\n' in q.read_text()"
after_revision="for q in [sp,rp]:assert ('revision: 2\\n' if q==sp else 'revision: 3\\n') in q.read_text()"
assert code.count(before_revision)==1;code=code.replace(before_revision,after_revision)
exec(compile(code,str(old),'exec'),{'__name__':'__main__','__file__':str(old)})
assert before=={str(q):info(q) for q in P.rglob('*') if q.is_file()}
print(json.dumps(dict(editorial_status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',prior_R2_payloads_unchanged=42,prior_R2_manifest_unchanged=True,exact_research_replacements=5,spec_revision=2,research_revision=3,normative_or_case_delta=None,writes=False),indent=2))
