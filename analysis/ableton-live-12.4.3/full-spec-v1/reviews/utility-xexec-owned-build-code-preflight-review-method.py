"""Independent stdlib identity/delta audit; only current read-only checker may run."""
from pathlib import Path
import ast,datetime,hashlib,json,os,subprocess,sys
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-utility-xexec-owned-build-preparation'
OUT=B/'reviews/utility-xexec-owned-build-code-preflight-review-evidence.json'
def identity(p):
 raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def j(p):return json.loads(p.read_text())
inputs=j(P/'inputs.json');plan=j(P/'plan.json');manifest=j(P/'manifest.json')
paths={Path(r['path']) for r in inputs['pins']}|{p for p in P.iterdir() if p.is_file()}|{Path(__file__).resolve()}
before=[identity(p) for p in sorted(paths)]
assert identity(P/'manifest.json')['sha256']=='74fb5ac0045bc379b960a4ac051030c67b9dd92859107bfcc97ccc0fc8534893'
assert len(inputs['pins'])==9 and len(manifest['files'])==6
assert {r['path'] for r in manifest['files']}=={p.name for p in P.iterdir() if p.name!='manifest.json'}
for r in inputs['pins']:assert identity(Path(r['path']))==r
for r in manifest['files']:
 v=identity(P/r['path']);assert (v['bytes'],v['sha256'])==(r['bytes'],r['sha256'])
tool=inputs['gcc_filesystem_metadata'];assert str(Path('/usr/bin/gcc').resolve(strict=True))==tool['resolved_path'] and os.readlink('/usr/bin/gcc')==tool['selected_symlink_target']
assert identity(Path(tool['resolved_path']))==tool['resolved_identity']
source=(P/'build-once.py').read_text();parent=Path(plan['method_parent']['path'])
assert identity(parent)==plan['method_parent']
lines=parent.read_text().splitlines(True);edits=plan['source_delta']['line_edits'];assert len(edits)==9
for edit in reversed(edits):
 lo,hi=edit['old_line_start'],edit['old_line_end'];old=''.join(lines[lo:hi]);assert hashlib.sha256(old.encode()).hexdigest()==edit['old_text_sha256'];lines[lo:hi]=edit['replacement'].splitlines(True)
assert ''.join(lines)==source
expected=['/usr/bin/gcc','-O1','-g','-Wall','-Wextra','-no-pie','-o',str(B/'depth-utility-xexec-owned-build/xexec'),'/home/ollie/Documents/sound/tools/xexec/xexec.c','-ldl','-lm']
assert plan['fixed_argv']==expected and plan['cwd']=='/home/ollie/Documents/sound' and plan['timeout_seconds']==45
assert plan['environment']==dict(PATH='/usr/bin:/bin',LANG='C',LC_ALL='C')
assert not Path(plan['exclusive_destination']).exists() and not Path(plan['exclusive_destination']).is_symlink()
tree=ast.parse(source);calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call)]
popens=[n for n in calls if isinstance(n.func,ast.Attribute) and n.func.attr=='Popen'];assert len(popens)==1
assert ast.unparse(popens[0].args[0])=='argv'
assert {n.arg:ast.unparse(n.value) for n in popens[0].keywords}==dict(cwd='CWD',env='ENV',stdin='subprocess.DEVNULL',stdout='subprocess.PIPE',stderr='subprocess.PIPE',preexec_fn='no_core',start_new_session='True')
assert all(not (isinstance(n.func,ast.Attribute) and n.func.attr in ('run','system','execv','execve')) for n in calls)
results=[]
for flag,exit_expected in [('--check',0),('--write',1)]:
 argv=[sys.executable,'-B',str(P/'check.py'),flag]
 run=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=20)
 assert run.returncode==exit_expected
 results.append(dict(argv=argv,exit=run.returncode,stdout=run.stdout,stderr=run.stderr))
passed=json.loads(results[0]['stdout']);assert passed['valid_controls']==1 and len(passed['unsafe_scope_rejections'])==7 and passed['pins']==9 and passed['watched']==16 and passed['unchanged'] is True
assert passed['compiler_or_output_or_original_execution'] is False
assert not Path(plan['exclusive_destination']).exists()
after=[identity(p) for p in sorted(paths)];assert before==after
x=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=identity(Path(__file__).resolve()),status='PASS CODE/PREPARATION ONLY',parent_edits=9,manifest_payloads=6,input_pins=9,watch_count=len(paths),before=before,after_equal=True,readonly_checks=results,compiler_or_original_execution=False)
with OUT.open('x') as f:json.dump(x,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in x.items() if k not in ('before','readonly_checks')},indent=2))
