"""Independent data/isolated-expression checks; never calls supplied functions or tools."""
from pathlib import Path
import ast,copy,datetime,hashlib,json,struct
BASE=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');PRE=BASE/'depth-corpus-x86-selected-entry-preparation';OUT=BASE/'reviews/corpus-x86-selected-entry-code-preflight-review-evidence.json'
ROOTREVIEW=BASE/'reviews/corpus-x86-selected-entry-root-code-preflight.json'

def load(p):return json.loads(p.read_text())
def identity(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  while True:
   x=f.read(1048576)
   if not x:break
   h.update(x);n+=len(x)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def sha(x):return hashlib.sha256(x).hexdigest()
assert not OUT.exists();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs=load(PRE/'inputs.json');manifest=load(PRE/'manifest-preparation.json');paths=sorted({Path(r['path']) for r in inputs['pins']}|{q for q in PRE.iterdir() if q.is_file()});before=[identity(p) for p in paths]
assert len(inputs['pins'])==14 and len(paths)==27 and identity(PRE/'manifest-preparation.json')['sha256']=='194d30df5c0a753fc51f3e066c2707867028df1917f8012904aa030d23f5b6e0'
assert len(manifest['files'])==12 and len(list(PRE.iterdir()))==13 and {r['path'] for r in manifest['files']}=={q.name for q in PRE.iterdir() if q.name!='manifest-preparation.json'}
for r in inputs['pins']:assert identity(Path(r['path']))==r
for r in manifest['files']:
 got=identity(PRE/r['path']);assert (got['bytes'],got['sha256'])==(r['bytes'],r['sha256'])
java=(PRE/'CorpusX86SelectedExport.java').read_text();driver=(PRE/'run-selected.py').read_text();checker=(PRE/'check.py').read_text();builder=(PRE/'build-fixture.py').read_text();tree=ast.parse(driver);fns={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
assert identity(PRE/'CorpusX86SelectedExport.java')['sha256']=='20f1e239b9842fbe4cf0add000232d977652ca547e88ee58b0cfb4be48ed8d31'
assert identity(PRE/'run-selected.py')['sha256']=='16abca7d24593741052e3aebb0cb4533d6523e9b845e8ab9639596a06d84f6f0'
assert identity(PRE/'check.py')['sha256']=='afe5f0f3c75556f86b912562f38ae1d41735ab45369008961284a5165e3ebc7d'
reconstructed=[];delta=load(PRE/'source-delta.json')
for file in delta['files']:
 assert identity(Path(file['before']['path']))==file['before'] and identity(Path(file['after']['path']))==file['after']
 lines=Path(file['before']['path']).read_text().splitlines(keepends=True)
 for edit in reversed(file['edits']):
  first,last=edit['old_line_start_zero'],edit['old_line_end_exclusive'];assert sha(''.join(lines[first:last]).encode())==edit['old_text_sha256'];lines[first:last]=edit['replacement'].splitlines(keepends=True)
 assert ''.join(lines)==Path(file['after']['path']).read_text();reconstructed.append(dict(before=file['before'],after=file['after'],edits=len(file['edits'])))
parent_java=Path(inputs['source_parents']['java']['path']).read_text();a='            MemoryBlock block=currentProgram.getMemory().getBlock(entry);';z='            else function.setBody(body);'
assert java[java.index(a):java.index(z)+len(z)]==parent_java[parent_java.index(a):parent_java.index(z)+len(z)]
oldtree=ast.parse(Path(inputs['source_parents']['driver']['path']).read_text());oldfns={n.name:n for n in oldtree.body if isinstance(n,ast.FunctionDef)}
for name in ['capture_group','stop_group','supervise']:
 assert ast.dump(ast.Module(body=fns[name].body,type_ignores=[]))==ast.dump(ast.Module(body=oldfns[name].body,type_ignores=[]))
# Independent owned-fixture reconstruction in memory; do NOT run fixture builder.
raw=(PRE/'synthetic-corpus-x86.macho').read_bytes();expected=bytearray(12288)
expected[:32]=struct.pack('<8I',0xfeedfacf,0x01000007,3,8,1,152,0,0)
expected[32:104]=struct.pack('<II16sQQQQiiII',0x19,152,b'__TEXT',0,0x3000,0,0x3000,5,5,1,0)
expected[104:184]=struct.pack('<16s16sQQIIIIIIII',b'__text',b'__TEXT',0x2000,0x1000,0x2000,4,0,0,0x80000400,0,0,0)
expected[0x2000:]=b'\xcc'*0x1000;expected[0x23b0:0x23b6]=b'\xb8\x2a\0\0\0\xc3';expected[0x29c0:0x29c3]=b'\x31\xc0\xc3'
assert raw==bytes(expected) and sha(raw)=='688f2e17c99b0c70aaa55c856cc687c2a28ce54e3dc6909b693f4bd4e0af93d2'
assert raw[0x23b0]==0xb8 and struct.unpack_from('<I',raw,0x23b1)[0]==42 and raw[0x23b5]==0xc3 and raw[0x29c0:0x29c3]==bytes.fromhex('31c0c3')
assert all(0x2000<=x and x+1024<=0x3000 for x in [0x23b0,0x29c0])
# Only inspect/evaluate the fully read boolean guard expressions; no supplied function compiled/called.
vc=fns['validate_config'];assert isinstance(vc.body[0],ast.If) and isinstance(vc.body[1],ast.For)
first=vc.body[0].test;numeric=vc.body[1].body[0].test;boolean=vc.body[2].test;window=vc.body[3].test;source=vc.body[4].test;output_guard=vc.body[5].test;path_guard=vc.body[6].test
seeds=[dict(address='0x23b0',window_bytes=1024,label='_CreateInstanceU',source='Root-fixed address nomination; fixture shares address only, not original behavior.'),dict(address='0x29c0',window_bytes=1024,label='_CalcA',source='Root-fixed address nomination; fixture shares address only, not original behavior.')]
common=dict(schema=1,profile='corpus-x86-two-entry-noanalysis-v1',architecture='x86_64',language='x86:LE:64:default',compiler='gcc',image_base='0x0',ghidra_version='12.1.4',seeds=seeds,auto_analysis=False,incremental_code_analysis=False,decompile_timeout_seconds=60,overall_timeout_seconds=180,java_heap='4G',disk_reserve_bytes=3*1024**3,group_rss_limit_bytes=6*1024**3,cpu=2)
fixed={}
fixed['fixture']={**common,'target_sha256':sha(raw),'source':dict(kind='analyst-owned-fixture',path=str(PRE/'synthetic-corpus-x86.macho'),bytes=12288,sha256=sha(raw))}
fixed['actual']={**common,'target_sha256':'03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d','source':dict(kind='universal-x86-slice',path='/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Corpus.bundle/Contents/MacOS/Corpus',bytes=527152,sha256='2164ec08805b35f1571687a08b7ce7df9831102981f0e2fdbd07719dbf3ef422',offset=16384,length=250352)}
configs={mode:load(PRE/(mode+'-config.json')) for mode in ['fixture','actual']};assert configs==fixed
assert {k for k in configs['actual'] if configs['actual'][k]!=configs['fixture'][k]}=={'source','target_sha256'}
def reviewer_destination(mode):return BASE/('depth-corpus-x86-selected-entry-'+mode)
def guard(expr,ns):return bool(eval(compile(ast.Expression(expr),'<fully-read-isolated-scope-expression>','eval'),{'__builtins__':{},'int':int,'type':type,'str':str,'any':any,'expected_config':lambda m:fixed[m],'destination':reviewer_destination,**ns}))
def config_accept(cfg,mode,out=None):
 ns=dict(config=cfg,mode=mode,output=out if out is not None else reviewer_destination(mode))
 if guard(first,ns):return False
 if any(guard(numeric,{**ns,'key':k}) for k in ['schema','decompile_timeout_seconds','overall_timeout_seconds','disk_reserve_bytes','group_rss_limit_bytes','cpu']):return False
 return not any(guard(expr,ns) for expr in [boolean,window,source,output_guard,path_guard])
for mode in fixed:assert config_accept(configs[mode],mode)
controls=[]
for name,key,value in [('wrongSHA','target_sha256','0'*64),('wrongarchitecture','architecture','arm64'),('wronglanguage','language','AARCH64:LE:64:AppleSilicon'),('analysisON','auto_analysis',True),('analysisnumericzero','auto_analysis',0),('incrementalON','incremental_code_analysis',True),('float_timeout','overall_timeout_seconds',180.0)]:
 cfg=copy.deepcopy(fixed['fixture']);cfg[key]=value;controls.append((name,cfg,None))
for name,mutate in [('duplicateentry',lambda d:d['seeds'].__setitem__(1,copy.deepcopy(d['seeds'][0]))),('reorderedentries',lambda d:d['seeds'].reverse()),('thirdseed',lambda d:d['seeds'].append(copy.deepcopy(d['seeds'][0]))),('wrongwindow',lambda d:d['seeds'][0].__setitem__('window_bytes',1025)),('wrongsource',lambda d:d['source'].__setitem__('path','/tmp/other'))]:
 cfg=copy.deepcopy(fixed['fixture']);mutate(cfg);controls.append((name,cfg,None))
controls.append(('oldoutput',copy.deepcopy(fixed['fixture']),Path('/var/tmp/sound-analysis/helpers/Corpus/project')))
for label,cfg,out in controls:assert not config_accept(cfg,'fixture',out),label
# Reviewer literal command; isolated supplied comparator only, not command() function.
def reviewer_command(out):return ['/home/ollie/.local/opt/ghidra_12.1.4_PUBLIC/support/analyzeHeadless',str(out/'project'),'CorpusX86Selected','-import',str(out/'input/Corpus.x86_64'),'-readOnly','-deleteProject','-noanalysis','-max-cpu','2','-log',str(out/'ghidra.log'),'-scriptlog',str(out/'script.log'),'-scriptPath',str(out/'method'),'-postScript',str(out/'method/CorpusX86SelectedExport.java'),str(out/'run.json'),str(out)]
cmdexpr=fns['validate_command'].body[0].test;out=reviewer_destination('fixture');cmd=reviewer_command(out)
def bad_command(argv):return bool(eval(compile(ast.Expression(cmdexpr),'<fully-read-isolated-command-guard>','eval'),{'__builtins__':{},'argv':argv,'output':out,'command':reviewer_command}))
assert not bad_command(cmd)
command_controls=[('missingnoanalysis',[x for x in cmd if x!='-noanalysis']),('analysisflag',cmd+['-analysis']),('extraexecute',cmd+[str(out/'input/Corpus.x86_64')])]
for label,argv in command_controls:assert bad_command(argv),label
main=ast.get_source_segment(driver,fns['main']);assert main.index('verify_selection(')<main.index('source_bytes(config)')<main.index('subprocess.Popen(')
assert main.index('signal.signal(signal.SIGTERM')<main.index('subprocess.Popen(')
assert main.index("status['tool_attempts']=1")<main.index('subprocess.Popen(')<main.index("status['returned_pid']=process.pid")
assert "fixture_independently_approved" in driver and "fixture_actual_review" in driver and "status['cleanup']['cleaned']" in driver
assert java.index('enableHeadlessAnalysis(false)')<java.index('config=JsonParser') and 'enableHeadlessAnalysis(true)' not in java and 'whole_program_available_to_decompiler' in java
for token in ['seeds.size()!=2','getAsInt()!=1024','maxMemory()!=4294967296L','availableProcessors()!=2','SystemUtilities.getDefaultThreadPoolSize()!=2','decompileFunction(function,60,monitor)','partial_code','exported-with-warnings']:
 assert token in java
for token in ["'GHIDRA_HEADLESS_MAXMEM':'4G'",'free<3*1024**3','rss>6*1024**3','timeout=180','timeout=3','preexec_fn=no_core','stdin=subprocess.DEVNULL',"'cpu.core.override=2'"]:
 if token=="'cpu.core.override=2'":assert '-Dcpu.core.override=2' in driver
 else:assert token in driver,token
assert len([x for x in ast.walk(tree) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='Popen'])==1
assert not reviewer_destination('fixture').exists() and not reviewer_destination('actual').exists()
assert before==[identity(p) for p in paths]
result=dict(status='PASS PREPARATION ONLY',started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer_method=identity(Path(__file__)),manifest=identity(PRE/'manifest-preparation.json'),root_preflight=identity(ROOTREVIEW),payloads=12,tree_files=13,pins=14,source_delta_files=reconstructed,Java_body_guard_block_byteidentical=True,resource_function_bodies_ASTidentical=['capture_group','stop_group','supervise'],fixture=dict(identity=identity(PRE/'synthetic-corpus-x86.macho'),whole_bytes_equal_independent_owned_reconstruction=True,machO_header=[0xfeedfacf,0x1000007,3,8,1,152,0,0],windows_fit_section=True,known_bodies=[dict(address='0x23b0',bytes='b82a000000c3',meaning='MOV EAX,42;RET',size=6),dict(address='0x29c0',bytes='31c0c3',meaning='XOR EAX,EAX;RET',size=3)],guest_execution=False),config_positives=2,command_positives=1,config_rejection_controls=[n for n,c,o in controls],command_rejection_controls=[n for n,c in command_controls],total_negative_controls=len(controls)+len(command_controls),only_guard_expressions_compiled=True,no_supplied_functions_or_main_compiled_or_called=True,original_bundle_pinned_as_opaque_whole_file_only=True,watch=dict(paths=27,before=before,after_equal_before=True,before_digest=sha(json.dumps(before,sort_keys=True).encode()),after_digest=sha(json.dumps([identity(p) for p in paths],sort_keys=True).encode()),scope='Current frozenprep/pins verification interval only; not historicalwholemachine watch.'),activities=dict(supplied_checker_driver_builder_import_main=False,Java_Ghidra_compiler_decoder_or_original_execution=False,original_slice_or_instruction_window_extraction=False,process_or_resource_monitor_runs=False),limits=['No API/launch/import/decompiler success tested; strict nominated language/compiler/heap/pool can fail future fixture.','Wholethin Program data available internally outside function windows; no byte-read sandbox.','Sampling/ps/cleanup bounds not hard realtime or universal escaped-descendant/PIDidentity closure.','Actual mode needs successful currentfixture and separately Root-pinned independent actualreview; this preflight selects no launch.'])
with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=result['status'],evidence=identity(OUT),valid_configs=2,valid_commands=1,negative_controls=result['total_negative_controls'],watch=27),indent=2))
