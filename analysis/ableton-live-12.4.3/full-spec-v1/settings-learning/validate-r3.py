"""Read-only single-action Settings correction; exact old checker/source retained."""
from pathlib import Path
import hashlib
import json
import sys

P=Path(__file__).resolve().parent
assert sys.argv[1:]==['--check'] and sys.dont_write_bytecode
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
oldmanifest=load(P/'manifest-author-r2.json')
assert sha(P/'manifest-author-r2.json')=='657a31fa3aa7cd1e86b44653b2abec8d5bee5e62132cd75ce499a3b3882098b7'
for name,pin in oldmanifest['files'].items():
    path=P/name
    assert path.stat().st_size==pin['bytes'] and sha(path)==pin['sha256']
response=load(P/'review-response-r3.json')
a=load(P/'cases-r2.json');b=load(P/'cases-r3.json')
assert len(a)==len(b)==31
assert response['finding']=='SET-R2-REVIEW-001'
assert response['exact_case_field_delta']['old']==a[16]['setup_and_action']
assert response['exact_case_field_delta']['new']==b[16]['setup_and_action']
assert a[16]['id']==b[16]['id']=='SET-017'
expected=json.loads(json.dumps(a));expected[16]['setup_and_action']=response['exact_case_field_delta']['new']
assert b==expected
assert all(x in b[16]['setup_and_action'] for x in ['explicitly select Use System Device','switch OS Sound output','device A','device B','successful output baseline'])
assert sha(P.parents[3]/response['review']['path'])==response['review']['sha256']
code=(P/'validate-r2.py').read_text()
for old,new,count in [("'cases-r2.json'","'cases-r3.json'",1),("'delta-r2.json'","'delta-r3.json'",1),("'spec-r2.md'","'spec-r3.md'",2),("'research-r2.md'","'research-r3.md'",1),("'README-r2.md'","'README-r3.md'",1),("'manifest-author-r2.json'","'manifest-author-r3.json'",4),("'revision: 2\\n'","'revision: 3\\n'",1)]:
    assert code.count(old)==count,(old,code.count(old))
    code=code.replace(old,new)
# The source checker is analyst code only; no author or original product module runs.
exec(compile(code,str(P/'validate-r2.py'),'exec'),{'__name__':'__main__','__file__':str(P/'validate-r2.py')})
