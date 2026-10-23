"""Read-only successor validation; retain the R1 validator and frozen bytes."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda n:json.loads((P/n).read_text())
for name,info in load('response-author-r2.json')['archive'].items():
 raw=(P/'archive-r1'/name).read_bytes();assert len(raw)==info['bytes'] and sha(raw)==info['sha256']
before={str(p.relative_to(P)):sha(p.read_bytes()) for p in P.rglob('*') if p.is_file()}
code=(P/'validate.py').read_text()
assert code.count('manifest-author-r1.json')==2
code=code.replace('manifest-author-r1.json','manifest-author-r2.json').replace('spec-r1.md','spec-r2.md').replace('research-r1.md','research-r2.md')
exec(compile(code,str(P/'validate.py'),'exec'),{'__file__':str(P/'validate.py'),'__name__':'__main__'})
a=load('archive-r1/requirements.json');b=load('requirements.json');changes=load('response-author-r2.json')['replacements']
for x,y in zip(a,b):
 expected=dict(x)
 if x['id'] in changes:
  old,new=changes[x['id']];assert expected['contract'].count(old)==1;expected['contract']=expected['contract'].replace(old,new)
 assert expected==y
for x,y in zip(load('archive-r1/cases.json'),load('cases.json')):
 expected=dict(x)
 if x['requirements'][0] in changes and expected['source_claim'] is not None:
  old,new=changes[x['requirements'][0]];expected['source_claim']=expected['source_claim'].replace(old,new)
 assert expected==y
assert before=={str(p.relative_to(P)):sha(p.read_bytes()) for p in P.rglob('*') if p.is_file()}
print('R1 archive and exact two-clause/one-source-claim successor delta: pass')
