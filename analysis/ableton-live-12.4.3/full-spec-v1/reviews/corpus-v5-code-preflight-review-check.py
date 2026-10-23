"""Structural/hash/AST review only; never imports or invokes comparison code."""
from pathlib import Path
import ast,difflib,hashlib,json,re,subprocess,sys,datetime
if sys.argv[1:]!=['--check']:
    raise SystemExit('Only --check; numerical/original execution is not selected.')
ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3'
STAGE=BASE/'handoff-staging/device-corpus-v5'
PRE=BASE/'handoff-staging/device-corpus-v5-analysis/preflight'
OLD=ROOT/'handoff/device-corpus-v4'
DESIGN=BASE/'full-spec-v1/corpus-v5-proposal'
OUT=BASE/'full-spec-v1/reviews/corpus-v5-code-preflight-review-evidence.json'
assert not OUT.exists()
def ident(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(p):return json.loads(p.read_bytes())
def exact_value(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
assert ident(STAGE/'manifest.json')['sha256']=='b3e6bc9089447cea6ebc61bfc3c8763767d269a81ba80eca2caa679ab755de02'
assert ident(PRE/'manifest.json')['sha256']=='0e9e65ab65fd2764f9f6b6e50d93358f4e87eac558ea7cca1c29cfff83ac85e3'
roles={r['role']:Path(r['path']) for r in load(PRE/'providers.json')['pins']}
watched={Path(__file__),*roles.values(),*PRE.iterdir(),*DESIGN.iterdir(),*(p for p in STAGE.rglob('*') if p.is_file())}
for role in ['v4_manifest','actual_validation_manifest']:
    source=roles[role]
    for r in load(source)['files']:watched.add(source.parent/r['path'])
before=[ident(p) for p in sorted(watched)]
counts={}
for directory in [STAGE,PRE,OLD,DESIGN]:
    manifest=load(directory/'manifest.json');listed=manifest['files']
    assert {r['path'] for r in listed}=={str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file() and p!=directory/'manifest.json'}
    for r in listed:
        got=ident(directory/r['path']);assert got['bytes']==r['bytes'] and got['sha256']==r['sha256']
    counts[str(directory)]=len(listed)
for row in load(PRE/'providers.json')['pins']:assert ident(Path(row['path']))=={k:row[k] for k in ['path','bytes','sha256']}
old=load(OLD/'cases.json');new=load(STAGE/'cases.json')
assert exact_value(new['cases'][:-1])==exact_value(old['cases']) and len(old['cases'])==26 and len(new['cases'])==27
old_eval=[e for c in old['cases'] for e in c['evaluations']];new_eval=[e for c in new['cases'] for e in c['evaluations']]
assert len(old_eval)==72 and len(new_eval)==73 and len({e['id'] for e in new_eval})==73
assert all(exact_value(a)==exact_value(b) for a,b in zip(old_eval,new_eval[:72]))
old_f32=[r for r in load(OLD/'manifest.json')['files'] if r['path'].endswith('.f32')]
assert len(old_f32)==81
for row in old_f32:assert (STAGE/row['path']).read_bytes()==(OLD/row['path']).read_bytes()
assert (STAGE/'AGENTS.md').read_bytes()==(OLD/'AGENTS.md').read_bytes()
assert len(list(STAGE.rglob('*.f32')))==82
source,=load(roles['R7_case']);expected=dict(source['evaluation']);expected['id']='CORPUS-AUDIO-027-01';expected['reference']='reference/CORPUS-AUDIO-027-01.f32'
expected['parameter_updates']=[{k:source['parameter_updates'][0][k] for k in ['frame','index','parameter','value']}]
assert exact_value(new_eval[-1])==exact_value(expected)
assert ident(STAGE/expected['reference'])['sha256']=='1336d90115bd24c058e556aa95e9140014d168dad7111dec64eb8edd1d977e73'
code=(STAGE/'compare.py').read_text();previous=(OLD/'compare.py').read_text();delta=load(PRE/'comparator-delta.json')
assert len(delta['literal_branch'].splitlines())==10 and len(delta['literal_hash_guard'].splitlines())==4
assert code.count(delta['literal_branch'])==code.count(delta['literal_hash_guard'])==1
assert code.replace(delta['literal_branch'],'',1).replace(delta['literal_hash_guard'],'',1)==previous
old_ast=ast.parse(previous);new_ast=ast.parse(code);validator_ast=ast.parse((PRE/'validate_once.py').read_text())
imports=lambda tree:[ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))]
assert imports(new_ast)==imports(old_ast)
adoption=load(roles['R7_adoption']);op=adoption['only_canonical_delta_from_frozen_source'];frozen=roles['R7_spec'].read_text()
assert frozen.count(op['anchor'])==1
adopted=frozen.replace(op['anchor'],op['anchor']+op['exact_banner'],1).encode()
assert len(adopted)==66141 and hashlib.sha256(adopted).hexdigest()==load(STAGE/'manifest.json')['specification']['parent_sha256']
public_links=[]
for file in STAGE.iterdir():
    if not file.is_file():continue
    text=file.read_text()
    assert not re.search(r'/home/|/tmp/|analysis/|wiki/research/|FUN_[0-9a-fA-F]|0x[0-9a-fA-F]{8,}',text)
    assert text.endswith('\n') and all(line.rstrip()==line for line in text.splitlines())
    if file.suffix=='.md':
        for target in re.findall(r'\]\(([^)]+)\)',text):
            local=target.split('#',1)[0]
            if local and not local.startswith(('http:','https:')):assert (file.parent/local).is_file();public_links.append({'file':file.name,'target':target})
assert not (PRE.parent/'numeric-validation').exists()
runs=[]
for arg in ['--check','--write']:
    argv=['python3','-B',str(PRE/'check_structure.py'),arg];r=subprocess.run(argv,capture_output=True,timeout=30)
    assert r.returncode==(0 if arg=='--check' else 1)
    runs.append({'argv':argv,'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()})
after=[ident(p) for p in sorted(watched)];assert before==after
manifest=load(STAGE/'manifest.json')
metadata_findings={key:manifest[key] for key in ['supersedes','change_list','readiness']}
assert metadata_findings['supersedes']=='device-corpus-v3'
assert metadata_findings['readiness']['parent_owner']=='Exact independently approvedR6adopted'
evidence={'retained_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS structural preservation; stale manifest readiness/supersession requires correction','before':before,'after':after,'watch_count':len(before),'unchanged':True,'stage_manifest':ident(STAGE/'manifest.json'),'preflight_manifest':ident(PRE/'manifest.json'),'comparator':ident(STAGE/'compare.py'),'one_shot_preparation':ident(PRE/'validate_once.py'),'provider_pins':len(roles),'payload_counts':counts,'old_groups':26,'old_evaluation_objects':72,'old_physical_f32':81,'new_groups':27,'new_evaluations':73,'new_physical_f32':82,'literal_branch_lines':10,'literal_guard_lines':4,'exact_inverse_to_v4':True,'old_imports_literal':True,'fullcode_AST_parses':True,'public_links':public_links,'stale_manifest_values':metadata_findings,'structural_checker_runs':runs,'future_numeric_directory_absent':True,'audio_decodes':0,'numerical_comparator_evaluator_execution':0,'original_calls':0,'grade':None}
with OUT.open('x') as f:json.dump(evidence,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in evidence.items() if k not in ['before','after','stale_manifest_values','structural_checker_runs','public_links']},indent=2))
