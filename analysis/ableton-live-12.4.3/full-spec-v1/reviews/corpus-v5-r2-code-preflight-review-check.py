"""Focused data-only R2 preservation/delta review; no numerical code import."""
from pathlib import Path
import hashlib,json,subprocess,sys,datetime
if sys.argv[1:]!=['--check']:raise SystemExit('Only --check; no numerical execution.')
ROOT=Path('/home/ollie/Documents/sound');BASE=ROOT/'analysis/ableton-live-12.4.3'
S1=BASE/'handoff-staging/device-corpus-v5';P1=BASE/'handoff-staging/device-corpus-v5-analysis/preflight'
S2=BASE/'handoff-staging/device-corpus-v5-r2';P2=BASE/'handoff-staging/device-corpus-v5-r2-analysis/preflight'
OUT=BASE/'full-spec-v1/reviews/corpus-v5-r2-code-preflight-review-evidence.json';assert not OUT.exists()
def load(p):return json.loads(p.read_bytes())
def ident(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
seals={S1:'b3e6bc9089447cea6ebc61bfc3c8763767d269a81ba80eca2caa679ab755de02',P1:'0e9e65ab65fd2764f9f6b6e50d93358f4e87eac558ea7cca1c29cfff83ac85e3',S2:'f3638adab97494b60654270224d1a5dd5100f5a62a44db8272efe8e3804292b0',P2:'174b6a499c243ba13cbcc87c3643945968371f43dcee6e5f3c1ba3bbb57ca37e'}
roles={r['role']:Path(r['path']) for r in load(P2/'providers.json')['pins']}
watched={Path(__file__),*roles.values()}
for directory,sha in seals.items():
 assert ident(directory/'manifest.json')['sha256']==sha
 watched.update(p for p in directory.rglob('*') if p.is_file())
for role in ['v4_manifest','actual_validation_manifest']:
 source=roles[role]
 for r in load(source)['files']:watched.add(source.parent/r['path'])
before=[ident(p) for p in sorted(watched)]
for directory in seals:
 manifest=load(directory/'manifest.json')
 assert {r['path'] for r in manifest['files']}=={str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file() and p!=directory/'manifest.json'}
 for r in manifest['files']:
  actual=ident(directory/r['path']);assert actual['bytes']==r['bytes'] and actual['sha256']==r['sha256']
for pin in load(P2/'providers.json')['pins']:assert ident(Path(pin['path']))=={k:pin[k] for k in ['path','bytes','sha256']}
old=load(S1/'manifest.json');new=load(S2/'manifest.json');correction=load(P2/'metadata-correction.json')
assert new['files']==old['files'] and len(new['files'])==88
for row in old['files']:assert (S1/row['path']).read_bytes()==(S2/row['path']).read_bytes()
expected=json.loads(json.dumps(old));pointers=correction['changed_manifest_pointers']
assert len(pointers)==6 and set(pointers)==set(correction['before_values'])==set(correction['after_values'])
for pointer in pointers:
 keys=pointer.strip('/').split('/');target=expected
 for key in keys[:-1]:target=target[key]
 assert target[keys[-1]]==correction['before_values'][pointer]
 target[keys[-1]]=correction['after_values'][pointer]
assert expected==new and new['supersedes']=='device-corpus-v4'
assert new['readiness']['handoff_review'].startswith('PENDING')
assert new['readiness']['numeric_validation'].startswith('PENDING') and 'HISTORICAL release4' in new['readiness']['numeric_validation']
assert 'R7' in new['readiness']['parent_owner'] and 'pickup-step' in new['readiness']['finite_method']
a=(P1/'validate_once.py').read_text();b=(P2/'validate_once.py').read_text()
oldpath="STAGE = HERE.parent.parent / 'device-corpus-v5'";newpath="STAGE = HERE.parent.parent / 'device-corpus-v5-r2'"
assert a.count(oldpath)==1 and b==a.replace(oldpath,newpath,1)
assert (P1/'source-binding.json').read_bytes()==(P2/'source-binding.json').read_bytes()
assert (P1/'comparator.patch').read_bytes()==(P2/'comparator.patch').read_bytes()
d1=load(P1/'comparator-delta.json');d2=load(P2/'comparator-delta.json');d1['after']['path']=str(S2/'compare.py');assert d1==d2
pins1=load(P1/'providers.json')['pins'];pins2=load(P2/'providers.json')['pins'];assert pins2[:len(pins1)]==pins1 and len(pins2)==len(pins1)+3
for directory in [P1,P2]:assert not (directory.parent/'numeric-validation').exists()
binding=load(P2/'candidate-binding.json');assert binding['manifest']==ident(S2/'manifest.json') and binding['comparator']==ident(S2/'compare.py')
readme=(P2/'README.md').read_text()
for quote in ['partial OUT without a terminal','CLI TimeoutExpired does not retain partial child stdout/stderr','Root outer selection,','no failure injection ran']:
 assert quote in readme
runs=[]
for arg in ['--check','--write']:
 argv=['python3','-B',str(P2/'check_structure.py'),arg];r=subprocess.run(argv,capture_output=True,timeout=30)
 assert r.returncode==(0 if arg=='--check' else 1)
 runs.append({'argv':argv,'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()})
after=[ident(p) for p in sorted(watched)];assert before==after
result={'retained_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS focused metadata/source preflight','before':before,'after':after,'watch_count':len(before),'unchanged':True,'stage_manifest':ident(S2/'manifest.json'),'preflight_manifest':ident(P2/'manifest.json'),'R1_files_preserved':99,'all_public_payloads_identical':88,'six_pointer_delta':pointers,'runner_only_fixed_stage_path_changed':True,'prior_pins_preserved':len(pins1),'pins_appended':3,'total_provider_pins':len(pins2),'runs':runs,'numeric_directory_absent':True,'numerical_execution':0,'audio_decodes':0,'original_calls':0,'grade':None}
with OUT.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['before','after','runs']},indent=2))
