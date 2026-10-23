"""Read-only preparation checks. No driver/module main, tools or original source slice executed."""
from pathlib import Path
import ast, copy, hashlib, json, struct, sys
P=Path(__file__).resolve().parent
R=Path('/home/ollie/Documents/sound');BASE=R/'analysis/ableton-live-12.4.3/full-spec-v1'
def identity(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
 if sys.argv[1:]!=['--check']:print('REFUSED: readonly --check only',file=sys.stderr);return 1
 inputs=json.loads((P/'inputs.json').read_text());watched={Path(r['path']) for r in inputs['pins']}|{p for p in P.iterdir() if p.is_file()};before={str(p):identity(p) for p in watched}
 for row in inputs['pins']:assert identity(Path(row['path']))==row
 driver=(P/'run-selected.py').read_text();tree=ast.parse(driver);fns={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 seeds=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SEEDS'))
 assert [s['address'] for s in seeds]==['0x23b0','0x85e0'] and all(type(s['window_bytes']) is int and s['window_bytes']==4096 for s in seeds)
 allowed=['destination','expected_config','validate_config','command','validate_command']
 pure=ast.Module(body=[fns[n] for n in allowed],type_ignores=[])
 # Complete newly authored pure config/scope functions only. No old resource, source_bytes, verify_selection or main function evaluated.
 forbidden={'open','read_bytes','read_text','Popen','run','system','exec','eval','import_module'}
 for n in ast.walk(pure):
  if isinstance(n,ast.Call):assert not (isinstance(n.func,ast.Name) and n.func.id in forbidden or isinstance(n.func,ast.Attribute) and n.func.attr in forbidden)
 ns=dict(Path=Path,PRE=P,BASE=BASE,GHIDRA=Path('/home/ollie/.local/opt/ghidra_12.1.4_PUBLIC'),PROFILE='corpus-x86-two-entry-noanalysis-v1',SEEDS=seeds,
   FIXTURE_SHA='7b8b11955de655b259787b79c80cd61a19c851ec2fcb137d8aa3b276e0783719',ACTUAL_SHA='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d')
 exec(compile(pure,'<new-pure-config-scope-only>','exec'),ns)
 configs={m:json.loads((P/(m+'-config.json')).read_text()) for m in ('fixture','actual')}
 for mode,cfg in configs.items():assert ns['validate_config'](cfg,mode,ns['destination'](mode))==cfg
 assert {k for k in configs['fixture'] if configs['fixture'][k]!=configs['actual'][k]}=={'source','target_sha256'}
 bad=[]
 for name,key,value in [('wrongSHA','target_sha256','0'*64),('wrongarchitecture','architecture','arm64'),('wronglanguage','language','AARCH64:LE:64:AppleSilicon'),('analysisON','auto_analysis',True),('analysisnumericzero','auto_analysis',0),('incrementalON','incremental_code_analysis',True)]:
  v=copy.deepcopy(configs['fixture']);v[key]=value;bad.append((name,v))
 v=copy.deepcopy(configs['fixture']);v['seeds'][1]=copy.deepcopy(v['seeds'][0]);bad.append(('duplicateentry',v))
 v=copy.deepcopy(configs['fixture']);v['seeds'].reverse();bad.append(('reorderedentries',v))
 v=copy.deepcopy(configs['fixture']);v['seeds'].append(copy.deepcopy(v['seeds'][0]));bad.append(('thirdseed',v))
 v=copy.deepcopy(configs['fixture']);v['seeds'][0]['window_bytes']=4097;bad.append(('wrongwindow',v))
 v=copy.deepcopy(configs['fixture']);v['source']['path']='/tmp/other';bad.append(('wrongsource',v))
 v=copy.deepcopy(configs['fixture']);v['source']['sha256']='0'*64;bad.append(('wrongownedSHA',v))
 v=copy.deepcopy(configs['fixture']);v['seeds'][1]['address']='0xd090';bad.append(('oldsecondseed',v))
 rejected=[]
 for name,cfg in bad:
  try:ns['validate_config'](cfg,'fixture',ns['destination']('fixture'))
  except ValueError:rejected.append(name)
  else:raise AssertionError(name)
 try:ns['validate_config'](configs['fixture'],'fixture',Path('/var/tmp/sound-analysis/helpers/Corpus/project'))
 except ValueError:rejected.append('oldoutput')
 else:raise AssertionError('oldoutput')
 argv=ns['command'](ns['destination']('fixture'));ns['validate_command'](argv,ns['destination']('fixture'))
 for name,cmd in [('missingnoanalysis',[s for s in argv if s!='-noanalysis']),('analysisflag',argv+['-analysis']),('extraexecute',argv+[str(ns['destination']('fixture')/'input/Corpus.x86_64')])]:
  try:ns['validate_command'](cmd,ns['destination']('fixture'))
  except ValueError:rejected.append(name)
  else:raise AssertionError(name)
 raw=(P/'synthetic-corpus-x86.macho').read_bytes();assert len(raw)==65536 and hashlib.sha256(raw).hexdigest()==ns['FIXTURE_SHA']
 assert struct.unpack_from('<8I',raw)==(0xfeedfacf,0x1000007,3,8,1,152,0,0)
 assert struct.unpack_from('<II',raw,32)==(0x19,152)
 assert struct.unpack_from('<QQQQ',raw,56)==(0,0x10000,0,0x10000)
 assert struct.unpack_from('<QQI',raw,136)==(0x2000,0xe000,0x2000)
 assert raw[0x23b0:0x23b6].hex()=='b82a000000c3' and raw[0x85e0:0x85e3].hex()=='31c0c3'
 assert all(0x2000<=int(seed['address'],16) and int(seed['address'],16)+4096<=0x10000 for seed in seeds)
 receipt=json.loads((P/'fixture-build-receipt.json').read_text());assert receipt['owned_builder_attempts']==1 and receipt['exit_code']==0 and not receipt['stderr_utf8'] and receipt['guest_execution'] is False
 assert receipt['builder_sha256']==identity(P/'build-fixture.py')['sha256'] and json.loads(receipt['stdout_utf8'])==identity(P/'synthetic-corpus-x86.macho')|{'guest_execution':False}
 java=(P/'CorpusX86SelectedExport.java').read_text();parent=Path('/home/ollie/Documents/sound/tools/ghidra/SelectedNativeExport.java').read_text()
 a='            MemoryBlock block=currentProgram.getMemory().getBlock(entry);';z='            else function.setBody(body);'
 assert java[java.index(a):java.index(z)+len(z)]==parent[parent.index(a):parent.index(z)+len(z)]
 for token in ['extends HeadlessScript','enableHeadlessAnalysis(false);','"x86:LE:64:default"','"gcc"','maxMemory()!=4294967296L','availableProcessors()!=2','seeds.size()!=2','getAsInt()!=4096','result.isTimedOut()','meta.put("partial_code"','Whole imported thin Program data/signatures']:
  assert token in java,token
 assert java.index('enableHeadlessAnalysis(false)')<java.index('config=JsonParser') and 'enableHeadlessAnalysis(true)' not in java
 assert 'RecoverySupport' not in driver+java and '/opt/homebrew' not in driver+java
 main_src=ast.get_source_segment(driver,fns['main']);assert main_src.index('verify_selection(')<main_src.index('source_bytes(config)')<main_src.index('subprocess.Popen(')
 assert "fixture_independently_approved" in driver and "fixture_actual_review" in driver
 assert main_src.index('signal.signal(signal.SIGTERM')<main_src.index('subprocess.Popen(')
 assert main_src.index("status['tool_attempts']=1")<main_src.index('subprocess.Popen(')<main_src.index("status['returned_pid']=process.pid")
 assert "'-readOnly','-deleteProject','-noanalysis','-max-cpu','2'" in driver and 'timeout=180' in driver and 'preexec_fn=no_core' in driver and 'stdin=subprocess.DEVNULL' in driver
 assert len([n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='Popen'])==1
 old_java=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-x86-selected-entry-preparation-r5/CorpusX86SelectedExport.java').read_text()
 old_driver=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-x86-selected-entry-preparation-r5/run-selected.py').read_text()
 expected_java=old_java
 for original,replacement,count in [('"0xd090"', '"0x85e0"', 1), ('0xd090L', '0x85e0L', 1)]:
  assert expected_java.count(original)==count;expected_java=expected_java.replace(original,replacement)
 assert java==expected_java
 for original,replacement,count in [("PRE=BASE/'depth-corpus-x86-selected-entry-preparation-r5'", "PRE=BASE/'depth-corpus-x86-selected-entry-preparation-r6'", 1), ("return BASE/('depth-corpus-x86-selected-entry-'+mode+'-r5')", "return BASE/('depth-corpus-x86-selected-entry-'+mode+'-r6')", 1), ("('corpus-x86-selected-entry-'+mode+'-r5-selected-execution')", "('corpus-x86-selected-entry-'+mode+'-r6-selected-execution')", 1), ("'address':'0xd090'", "'address':'0x85e0'", 1), ("'label':'construction-candidate-0xd090'", "'label':'nominal-processing-candidate-0x85e0'", 1), ('1c514938c8b4b28ee47c0f419acb247e63a65ee988d57b5f195957b3aae4c9de', '7b8b11955de655b259787b79c80cd61a19c851ec2fcb137d8aa3b276e0783719', 1)]:
  assert old_driver.count(original)==count;old_driver=old_driver.replace(original,replacement)
 assert driver==old_driver
 old_guard=old_java[old_java.index('        if(!"21.0.12.1"'):old_java.index('        if(!config.get("target_sha256")')]
 assert old_guard==java[java.index('        if(!"21.0.12.1"'):java.index('        if(!config.get("target_sha256")')]
 unsafe_guard=java.replace('maxMemory()!=4294967296L','maxMemory()!=3221225472L',1)
 assert unsafe_guard!=java and unsafe_guard!=expected_java
 unsafe_environment=driver.replace("'GHIDRA_HEADLESS_JAVA_OPTIONS':'-Dcpu.core.override=2'","'GHIDRA_HEADLESS_JAVA_OPTIONS':'-Dcpu.core.override=3'",1)
 assert unsafe_environment!=driver and unsafe_environment!=old_driver
 delta=json.loads((P/'source-delta.json').read_text())
 for f in delta['files']:
  assert identity(Path(f['before']['path']))==f['before'] and identity(Path(f['after']['path']))==f['after']
  lines=Path(f['before']['path']).read_text().splitlines(keepends=True)
  for e in reversed(f['edits']):
   a,z=e['old_line_start_zero'],e['old_line_end_exclusive'];assert hashlib.sha256(''.join(lines[a:z]).encode()).hexdigest()==e['old_text_sha256'];lines[a:z]=e['replacement'].splitlines(keepends=True)
  assert ''.join(lines)==Path(f['after']['path']).read_text()
 if (P/'manifest-preparation.json').exists():
  m=json.loads((P/'manifest-preparation.json').read_text());assert {r['path'] for r in m['files']}=={p.name for p in P.iterdir() if p.is_file() and p.name!='manifest-preparation.json'}
  for row in m['files']:
   got=identity(P/row['path']);assert (got['bytes'],got['sha256'])==(row['bytes'],row['sha256'])
 assert before=={str(p):identity(p) for p in watched}
 print(json.dumps(dict(status='PASS PREPARATION ONLY',valid_configs=2,valid_commands=1,unsafe_rejections=rejected,synthetic_data_header_and_knownbytes=True,inherited_Java_bodyguards_exact=True,pins=len(inputs['pins']),watched=len(watched),unchanged=True,Ghidra_Java_compiler_decoder_original_or_guest_execution=False),indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
