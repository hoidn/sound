import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('persistent_native', Path(__file__).parents[1] / 'run_persistent_native.py')
if SPEC and SPEC.loader and Path(SPEC.origin).exists():
    pn = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(pn)
else:
    pn = None

class PersistentCore(unittest.TestCase):
    def test_target_and_raw_fixture_have_distinct_loader_matched_profiles(self):
        self.require_tool();real_sha=pn.sha
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();fixture=root/'fixture.bin';fixture.write_bytes(pn.FIXTURE_BYTES)
            raw=pn.make_config(root,fixture,fixture=True,mode='verify-only')
            target=root/'target-standin';target.write_bytes(b'independent test data')
            # This config-only stand-in models the already verified target digest; it is never launched.
            def digest(path):return pn.TARGET_SHA if Path(path)==target else real_sha(path)
            with patch.object(pn,'sha',side_effect=digest):macho=pn.make_config(root,target,fixture=False,mode='verify-only')
            self.assertEqual(raw['language'],'AARCH64:LE:64:v8A');self.assertEqual(raw['profile']['language'],raw['language'])
            self.assertEqual(macho['language'],'AARCH64:LE:64:AppleSilicon');self.assertEqual(macho['profile']['language'],macho['language'])
            self.assertEqual(raw['compiler'],'default');self.assertEqual(macho['compiler'],'default')
            self.assertEqual(raw['profile']['id'],'ghidra-persistent-bounded-analysis-raw-arm64-fixture-v2')
            self.assertEqual(macho['profile']['id'],'ghidra-persistent-bounded-analysis-apple-silicon-v2')
            self.assertNotEqual(raw['profile_sha256'],macho['profile_sha256'])
            raw_command,_=pn.launch_command(root,raw,root/'raw-project',importing=True);target_command,_=pn.launch_command(root,macho,root/'target-project',importing=True)
            self.assertIn('-noanalysis',raw_command);self.assertIn('-noanalysis',target_command)
            self.assertEqual(raw_command[raw_command.index('-loader')+1],'BinaryLoader')
            self.assertEqual(raw_command[raw_command.index('-processor')+1],raw['language'])
            self.assertNotIn('-loader',target_command);self.assertNotIn('-processor',target_command);self.assertNotIn('-cspec',target_command)
    def test_profile_definitions_are_immutable_and_configs_do_not_mutate_them(self):
        self.require_tool();self.assertTrue(hasattr(pn,'TARGET_PROFILE'));self.assertTrue(hasattr(pn,'FIXTURE_PROFILE'))
        for profile in (pn.TARGET_PROFILE,pn.FIXTURE_PROFILE):
            with self.assertRaises(TypeError):profile['language']='wrong'
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();fixture=root/'fixture.bin';fixture.write_bytes(pn.FIXTURE_BYTES)
            config=pn.make_config(root,fixture,fixture=True,mode='verify-only');config['profile']['language']='changed-config'
            self.assertEqual(pn.FIXTURE_PROFILE['language'],'AARCH64:LE:64:v8A');self.assertEqual(pn.TARGET_PROFILE['language'],'AARCH64:LE:64:AppleSilicon')
    def require_tool(self):
        self.assertIsNotNone(pn, 'persistent controller must exist')
    def test_duplicate_json_keys_rejected(self):
        self.require_tool()
        with self.assertRaises(ValueError): pn.decode_json('{"schema":1,"schema":1}')
    def test_publication_never_overwrites_existing_report(self):
        self.require_tool()
        with tempfile.TemporaryDirectory() as td:
            path=Path(td).resolve()/'report.json'; pn.publish(path, {'first':True})
            with self.assertRaises(FileExistsError): pn.publish(path, {'second':True})
            self.assertEqual(pn.read_json(path), {'first':True})
    def test_checkpoint_rejects_symlink_and_detects_changed_bytes(self):
        self.require_tool()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve(); (root/'recover.gpr').write_bytes(b'project'); (root/'recover.rep').mkdir(); (root/'recover.rep'/'db').write_bytes(b'database')
            manifest=pn.project_snapshot(root)
            pn.verify_project(root,manifest)
            (root/'recover.rep'/'db').write_bytes(b'changed')
            with self.assertRaises(ValueError): pn.verify_project(root,manifest)
            (root/'recover.rep'/'alias').symlink_to('db')
            with self.assertRaises(ValueError): pn.project_snapshot(root)
    def test_resource_limits_need_two_rss_samples_but_disk_is_immediate(self):
        self.require_tool(); policy=pn.ResourcePolicy(rss_limit=100,disk_floor=50,allocation_limit=500,deadline=5)
        self.assertIsNone(policy.observe(1,101,100,10)); self.assertEqual(policy.observe(2,101,100,10),'rss-limit')
        policy=pn.ResourcePolicy(rss_limit=100,disk_floor=50,allocation_limit=500,deadline=5)
        self.assertEqual(policy.observe(1,1,49,10),'disk-floor')
    def test_signal_requires_creation_identity_and_group(self):
        self.require_tool()
        identity={'pid':42,'start_us':1000,'pgid':42}
        with patch.object(pn,'process_identity',return_value={'pid':42,'start_us':1001,'pgid':42}),patch.object(pn.os,'kill') as kill:
            self.assertFalse(pn.signal_matching(identity,15)); kill.assert_not_called()
        with patch.object(pn,'process_identity',return_value={'pid':42,'start_us':1000,'pgid':43}),patch.object(pn.os,'kill') as kill:
            self.assertFalse(pn.signal_matching(identity,15)); kill.assert_not_called()
    def test_stage_b_capacity_uses_actual_baseline_allocation(self):
        self.require_tool()
        self.assertEqual(pn.required_free('analyze',3*pn.GIB),14*pn.GIB)
        self.assertEqual(pn.required_free('analyze',1000),12*pn.GIB)
    def test_fixture_identity_is_separate_and_pinned(self):
        self.require_tool(); self.assertEqual(len(pn.FIXTURE_BYTES),8)
        self.assertEqual(hashlib.sha256(pn.FIXTURE_BYTES).hexdigest(),pn.FIXTURE_SHA)
        self.assertNotEqual(pn.FIXTURE_SHA,pn.TARGET_SHA)
    def test_negative_exit_zero_does_not_accept_missing_outcome(self):
        self.require_tool()
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError): pn.validate_milestones(Path(td), {'nonce':'n'}, '',0,False)

if __name__=='__main__': unittest.main()

class AttestationTests(unittest.TestCase):
    def test_effective_diagnostics_require_last_flags_and_matching_properties(self):
        self.assertTrue(hasattr(pn,'verify_diagnostics'),'diagnostic parser must exist')
        config={'nonce':'abc','home':'/isolated/home','tmp':'/isolated/tmp','jdk':str(pn.JDK)}
        outputs={'VM.command_line':'jvm_args: -Dcpu.core.override= -Dcpu.core.override=2 -Dsound.recovery.nonce=abc\n',
                 'VM.flags':'-XX:ActiveProcessorCount=2 -XX:MaxHeapSize=4294967296',
                 'VM.system_properties':'cpu.core.override=2\ncpu.core.limit=2\nuser.home=/isolated/home\njava.io.tmpdir=/isolated/tmp\njava.home='+str(pn.JDK)+'\nsound.recovery.nonce=abc\njava.version=21.0.12.1\n'}
        pn.verify_diagnostics(outputs,config)
        outputs['VM.flags']='-XX:ActiveProcessorCount=3 -XX:MaxHeapSize=4294967296'
        with self.assertRaises(ValueError):pn.verify_diagnostics(outputs,config)
    def test_target_launch_always_noanalysis_and_fixture_never_target(self):
        self.assertTrue(hasattr(pn,'make_config'),'stage configuration must exist')
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve(); target=root/'fixture.bin'; target.write_bytes(pn.FIXTURE_BYTES)
            config=pn.make_config(root,target,fixture=True,mode='verify-only')
            argv,env=pn.launch_command(root,config,root/'project',importing=True)
            self.assertIn('-noanalysis',argv); self.assertNotIn('JAVA_TOOL_OPTIONS',env)
            self.assertNotIn('_JAVA_OPTIONS',env); self.assertNotIn('GHIDRA_JAVA_OPTIONS',env)
            with self.assertRaises(ValueError):pn.make_config(root,target,fixture=False,mode='verify-only')
    def test_checkpoint_copy_changes_cannot_modify_sealed_source(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve(); source=root/'source'; source.mkdir(); (source/'recover.gpr').write_bytes(b'gpr'); (source/'recover.rep').mkdir(); (source/'recover.rep'/'db').write_bytes(b'db')
            manifest=pn.project_snapshot(source); dest=pn.copy_project(source,root/'copy',manifest)
            (dest/'recover.rep'/'db').write_bytes(b'new')
            pn.verify_project(source,manifest)
            with self.assertRaises(ValueError):pn.verify_project(dest,manifest)

class ScriptContractTests(unittest.TestCase):
    def test_production_gate_and_outcome_sources_exist_for_actual_integration(self):
        for name in ('RecoveryLaunchGate.java','RecoveryAnalysisOutcome.java','RecoveryNativeExport.java'):
            self.assertTrue((pn.SCRIPT_ROOT/name).is_file(),name+' must be compiled and exercised by fixture integration')
    def test_exact_export_entries_reject_duplicate_unqualified_and_external(self):
        self.assertTrue(hasattr(pn,'validate_export_entries'),'inventory-bound exporter validator must exist')
        records=[{'key':'ram:0x0','external':False,'entry_space':'ram','entry_offset':'0x0'}, {'key':'EXTERNAL:0x1','external':True,'entry_space':'EXTERNAL','entry_offset':'0x1'}]
        self.assertEqual(pn.validate_export_entries(records,['ram:0x0']),[records[0]])
        for entries in (['0x0'],['ram:0x0','ram:0x0'],['ram:0x1'],['EXTERNAL:0x1']):
            with self.assertRaises(ValueError):pn.validate_export_entries(records,entries)

class CheckpointAdmissionTests(unittest.TestCase):
    def test_invalid_checkpoint_cannot_be_loaded_by_exit_zero_result(self):
        self.assertTrue(hasattr(pn,'load_checkpoint'),'checkpoint publication/validation must exist')
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();(root/'manifest.json').write_text('{"schema":1,"status":"unverified"}')
            with self.assertRaises(ValueError):pn.load_checkpoint(root)
    def test_stream_inventory_reconciles_counts_and_rejects_duplicate_keys(self):
        self.assertTrue(hasattr(pn,'read_inventory'),'inventory acceptance must exist')
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();line=json.dumps({'key':'ram:0x0','entry_space':'ram','entry_offset':'0x0','external':False,'body_bytes':8,'body_ranges':[],'name':'f','aliases':[],'thunk':False})+'\n'
            payload=root/'inventory.jsonl';payload.write_text(line+line)
            summary={'schema':1,'status':'pass','total':2,'ordinary':2,'external':0,'payload_sha256':pn.sha(payload),'payload_bytes':payload.stat().st_size}
            pn.publish(root/'inventory-summary.json',summary)
            with self.assertRaises(ValueError):pn.read_inventory(root)

class OwnershipRaceTests(unittest.TestCase):
    def test_final_sweep_sees_unsampled_child_after_leader_exit(self):
        owner=pn.Owner();leader={'pid':100,'start_us':1000,'pgid':100,'sid':100};child={'pid':101,'ppid':1,'start_us':1100,'pgid':100,'sid':100,'rss_bytes':5}
        owner.roots[100]=leader;owner.identities[100]=leader
        with patch.object(pn,'process_table',return_value={101:child}):
            self.assertEqual(owner.sample(),[child])
    def test_reused_leader_group_does_not_adopt_or_signal_unrelated_child(self):
        owner=pn.Owner();leader={'pid':100,'start_us':1000,'pgid':100,'sid':100};unrelated={'pid':100,'ppid':1,'start_us':2000,'pgid':100,'sid':100,'rss_bytes':5}
        owner.roots[100]=leader;owner.identities[100]=leader
        with patch.object(pn,'process_table',return_value={100:unrelated}),patch.object(pn.os,'kill') as kill:
            self.assertEqual(owner.sample(),[]);self.assertTrue(owner.gaps);kill.assert_not_called()
    def test_cleanup_prevents_late_diagnostic_launch(self):
        owner=pn.Owner();owner.closing=True
        with patch.object(pn.subprocess,'Popen') as launch:
            with self.assertRaises(RuntimeError):owner.launch(['unused'],stdout=None,stderr=None)
            launch.assert_not_called()
    def test_outcome_watchdog_is_positive_validated_not_file_existence(self):
        self.assertTrue(hasattr(pn,'validate_outcome'),'bounded positive outcome watchdog helper must exist')
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();pn.publish(root/'analysis-outcome.json',{'schema':1,'nonce':'wrong'})
            with self.assertRaises(ValueError):pn.validate_outcome(root,{'nonce':'right','_sha':'hash'})

class CopyBudgetTests(unittest.TestCase):
    def test_copy_admission_rejects_whole_job_budget_before_destination_exists(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();source=root/'source';source.mkdir();(source/'recover.gpr').write_bytes(b'gpr');(source/'recover.rep').mkdir();(source/'recover.rep'/'db').write_bytes(b'db')
            dest=root/'copy';manifest=pn.project_snapshot(source)
            with self.assertRaises(ValueError):pn.copy_project(source,dest,manifest,budget_root=root,budget_limit=1)
            self.assertFalse(dest.exists())
    def test_log_scanner_preserves_tokens_split_across_appends_without_rereads(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td).resolve()/'log';path.write_bytes(b'REPORT: Analysis time');scanner=pn.LogScanner([path]);self.assertEqual(scanner.scan(),'')
            with path.open('ab') as stream:stream.write(b'd out at 1 seconds\n')
            self.assertIn('REPORT: Analysis timed out at ',scanner.scan());offset=scanner.offsets[path];scanner.scan();self.assertEqual(scanner.offsets[path],offset)
    def test_interrupted_copy_retains_partial_tree_and_sealed_source(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();source=root/'source';source.mkdir();(source/'recover.gpr').write_bytes(b'gpr');(source/'recover.rep').mkdir()
            manifest=pn.project_snapshot(source);destination=root/'copy'
            def interrupted(src,dest,**kwargs):Path(dest).mkdir();(Path(dest)/'partial').write_bytes(b'partial');raise OSError('injected copy interruption')
            with patch.object(pn.shutil,'copytree',side_effect=interrupted):
                with self.assertRaises(OSError):pn.copy_project(source,destination,manifest)
            self.assertTrue((destination/'partial').exists());self.assertFalse((destination/'manifest.json').exists());pn.verify_project(source,manifest)

class PeakAdmissionTests(unittest.TestCase):
    def test_four_retained_b_representations_are_reserved_before_analysis(self):
        self.assertTrue(hasattr(pn,'required_peak_free'),'retained copy strategy needs peak admission')
        self.assertGreaterEqual(pn.required_peak_free('analyze',3*pn.GIB),24*pn.GIB)
        self.assertGreaterEqual(pn.required_peak_free('analyze',3*pn.GIB),pn.required_free('analyze',3*pn.GIB))

class ActualOwnedPythonTests(unittest.TestCase):
    @unittest.skipUnless(__import__('sys').platform=='darwin','libproc is macOS-specific')
    def test_real_unsampled_orphan_is_stopped_after_group_leader_exit(self):
        import subprocess,sys,time
        with tempfile.TemporaryDirectory() as td:
            path=Path(td).resolve()/'child.pid';owner=pn.Owner()
            child_code='import time;time.sleep(60)'
            code='import subprocess,sys,time;from pathlib import Path;p=subprocess.Popen([sys.executable,"-c",'+repr(child_code)+']);Path('+repr(str(path))+').write_text(str(p.pid));time.sleep(.2)'
            with open(__import__('os').devnull,'wb') as stream:
                p=owner.launch([sys.executable,'-c',code],stdout=stream,stderr=stream)
                try:
                    p.wait(timeout=5);child=int(path.read_text());self.assertNotIn(child,owner.identities)
                    self.assertIn(child,[x['pid'] for x in owner.sample()])
                finally:closure=owner.close()
            # macOS may briefly retain a child zombie after init adoption; it cannot run.
            identity=pn.process_identity(child)
            self.assertTrue(identity is None or identity['status']==5)
            self.assertTrue(closure['reaped'])
    @unittest.skipUnless(__import__('sys').platform=='darwin','libproc is macOS-specific')
    def test_monitor_exception_and_repeated_interrupts_still_close_owned_worker(self):
        import os,signal,sys,time
        real_owner=pn.Owner;owners=[]
        class InjectedOwner(real_owner):
            def __init__(self):super().__init__();self.once=True;owners.append(self)
            def sample(self):
                if self.once:
                    self.once=False
                    raise OSError('injected first monitor sample failure')
                return super().sample()
            def close(self):
                os.kill(os.getpid(),signal.SIGINT);os.kill(os.getpid(),signal.SIGTERM)
                return super().close()
        with tempfile.TemporaryDirectory() as td:
            job=Path(td).resolve();target=job/'fixture.bin';target.write_bytes(pn.FIXTURE_BYTES);project=job/'project';project.mkdir()
            pn.publish(job/'admission.json',{'allocation_limit_bytes':pn.GIB})
            argv=[sys.executable,'-c','import time;time.sleep(60)']
            with patch.object(pn,'Owner',InjectedOwner),patch.object(pn,'launch_command',return_value=(argv,None)):
                with self.assertRaises(RuntimeError):pn.run_stage(job/'stage',project,target,fixture=True,importing=True,allocation_root=job,deadline=5)
            result=pn.read_json(job/'stage/stage-result.json')
            self.assertEqual(result['status'],'fail');self.assertIn('injected first monitor',result['error'])
            self.assertTrue(result['closure']['closed']);self.assertTrue(result['closure']['reaped']);self.assertFalse(result['closure']['survivors'])
            self.assertTrue(all(pn.process_identity(item['pid']) is None for item in result['closure']['identities']))
    @unittest.skipUnless(__import__('sys').platform=='darwin','libproc is macOS-specific')
    def test_injected_rss_samples_stop_and_reap_owned_python_worker(self):
        import sys
        real_table=pn.process_table;real_owner=pn.Owner;owners=[]
        def create_owner():owner=real_owner();owners.append(owner);return owner
        def high_owned_rss():
            table=real_table()
            for owner in owners:
                for pid in owner.roots:
                    if pid in table:table[pid]['rss_bytes']=6*pn.GIB+1
            return table
        with tempfile.TemporaryDirectory() as td:
            job=Path(td).resolve();target=job/'fixture.bin';target.write_bytes(pn.FIXTURE_BYTES);project=job/'project';project.mkdir();pn.publish(job/'admission.json',{'allocation_limit_bytes':pn.GIB})
            with patch.object(pn,'Owner',side_effect=create_owner),patch.object(pn,'process_table',side_effect=high_owned_rss),patch.object(pn,'launch_command',return_value=([sys.executable,'-c','import time;time.sleep(60)'],None)):
                with self.assertRaises(RuntimeError):pn.run_stage(job/'stage',project,target,fixture=True,importing=True,allocation_root=job,deadline=5)
            result=pn.read_json(job/'stage/stage-result.json');self.assertEqual(result['error'],"RuntimeError('rss-limit')")
            self.assertEqual(len(result['samples']),2);self.assertTrue(result['closure']['closed']);self.assertTrue(result['closure']['reaped'])
    @unittest.skipUnless(__import__('sys').platform=='darwin','libproc is macOS-specific')
    def test_uncooperative_owned_worker_needs_identity_checked_kill(self):
        import os,signal,sys,time
        owner=pn.Owner()
        with tempfile.TemporaryDirectory() as td,open(os.devnull,'wb') as stream:
            ready=Path(td).resolve()/'ready'
            code='import signal,time;from pathlib import Path;signal.signal(signal.SIGTERM,signal.SIG_IGN);Path('+repr(str(ready))+').write_text("ready");time.sleep(60)'
            worker=owner.launch([sys.executable,'-c',code],stdout=stream,stderr=stream)
            try:
                until=time.monotonic()+5
                while not ready.exists() and time.monotonic()<until:time.sleep(.01)
                self.assertTrue(ready.exists());closure=owner.close()
            finally:
                if worker.poll() is None:owner.close()
            self.assertTrue(closure['closed']);self.assertTrue(closure['reaped']);self.assertEqual(worker.returncode,-signal.SIGKILL)
            self.assertIn(signal.SIGKILL,[item['signal'] for item in closure['signaled']]);self.assertIsNone(pn.process_identity(worker.pid))

class StrictMilestoneTests(unittest.TestCase):
    def test_wrong_effective_version_or_nonce_properties_are_rejected(self):
        config={'nonce':'abc','home':'/h','tmp':'/t','jdk':str(pn.JDK)}
        base={'VM.command_line':'-Dsound.recovery.nonce=abc','VM.flags':'-XX:ActiveProcessorCount=2 -XX:MaxHeapSize=4294967296',
              'VM.system_properties':'cpu.core.override=2\ncpu.core.limit=2\nuser.home=/h\njava.io.tmpdir=/t\njava.home='+str(pn.JDK)+'\nsound.recovery.nonce=abc\njava.version=21.0.12.1\n'}
        for old,new in [('cpu.core.override=2','cpu.core.override=3'),('user.home=/h','user.home=/wrong'),('java.io.tmpdir=/t','java.io.tmpdir=/wrong'),('java.home='+str(pn.JDK),'java.home=/wrong'),('sound.recovery.nonce=abc','sound.recovery.nonce=wrong'),('java.version=21.0.12.1','java.version=wrong')]:
            changed=dict(base);changed['VM.system_properties']=base['VM.system_properties'].replace(old,new)
            with self.subTest(property=old),self.assertRaises(ValueError):pn.verify_diagnostics(changed,config)
    def test_launch_environment_does_not_repurpose_home(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();target=root/'fixture';target.write_bytes(pn.FIXTURE_BYTES);config=pn.make_config(root,target,fixture=True,mode='verify-only')
            argv,env=pn.launch_command(root,config,root/'project',importing=True)
            self.assertNotIn('HOME',env);self.assertIn('-Duser.home='+config['home'],env['JDK_JAVA_OPTIONS'])
            self.assertIn('-XX:+StartAttachListener',env['GHIDRA_HEADLESS_JAVA_OPTIONS'])

class ProvenanceAcceptanceTests(unittest.TestCase):
    def test_rehashed_manifest_cannot_turn_failed_stage_into_checkpoint(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();job=root/'job';job.mkdir();checkpoint=job/'checkpoint';checkpoint.mkdir();project=checkpoint/'project';project.mkdir();(project/'recover.gpr').write_bytes(b'gpr');(project/'recover.rep').mkdir()
            result=job/'result.json';pn.publish(result,{'schema':1,'status':'fail','closure':{'closed':False},'returncode':0})
            profile={'id':'fixture'};manifest={'schema':1,'status':'verified-closed','project':pn.project_snapshot(project),
                      'profile':profile,'profile_sha256':hashlib.sha256(json.dumps(profile,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                      'evidence':[{'path':str(result),'sha256':pn.sha(result)}]}
            pn.publish(checkpoint/'manifest.json',manifest)
            with self.assertRaises(ValueError):pn.load_checkpoint(checkpoint)
    def test_export_rejects_missing_metadata_pin_even_when_summary_rehashed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();exports=root/'exports';exports.mkdir();ident='capture-'+32*'a'+'-'+16*'b';cap=exports/ident;cap.mkdir()
            pn.publish(cap/'manifest.json',{'schema':1,'capture_id':ident,'files':[]})
            pn.publish(root/'export-summary.json',{'schema':1,'status':'pass','total':1,'captures':[{'capture_id':ident,'manifest_sha256':pn.sha(cap/'manifest.json'),'state':'failed'}]})
            with self.assertRaises(ValueError):pn.verify_exports(root,{'profile_sha256':'p'},checkpoint_sha='c',expected_entries=['ram:0x0'])

class CopiedMethodsTests(unittest.TestCase):
    def test_changed_copied_script_is_rejected_before_launch(self):
        self.assertTrue(hasattr(pn,'validate_copied_methods'),'copied source authority must be checked')
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();(root/'scripts').mkdir();(root/'methods').mkdir();methods={}
            for name in pn.SCRIPT_NAMES:
                path=root/'scripts'/name;path.write_bytes(b'method');methods[name]=pn.sha(path)
            controller=root/'methods'/'run_persistent_native.py';controller.write_bytes(b'controller');methods['controller']=pn.sha(controller)
            for name in ('analyzeHeadless','launch.sh','java','jcmd'):
                path=root/'methods'/name;path.write_bytes(b'installed');methods[name]=pn.sha(path)
            pn.validate_copied_methods(root,{'methods':methods})
            (root/'scripts'/'RecoveryLaunchGate.java').write_bytes(b'changed')
            with self.assertRaises(ValueError):pn.validate_copied_methods(root,{'methods':methods})

class NativeProcessPinTests(unittest.TestCase):
    def test_native_decompiler_executable_is_pinned_in_execution_methods(self):
        self.assertTrue(hasattr(pn,'NATIVE_DECOMPILER'),'native child executable identity needs a pin')
        self.assertEqual(pn.method_pins()['native_decompiler'],pn.sha(pn.NATIVE_DECOMPILER))

class ExportEvidenceConsistencyTests(unittest.TestCase):
    def make_export(self,root):
        key='ram:0x0';ident='capture-'+32*'a'+'-'+hashlib.sha256(key.encode()).hexdigest()[:16]
        cap=root/'exports'/ident;cap.mkdir(parents=True);code=cap/'pseudocode.c';code.write_text('int f(void) { return 0; }\n')
        entry={'key':key,'entry_space':'ram','entry_offset':'0x0','external':False,'body_bytes':8,'body_ranges':[],'name':'f','thunk':False,'aliases':[]}
        config={'schema':1,'nonce':32*'a','mode':'verify-only','profile_sha256':'profile','checkpoint_sha256':'checkpoint','checkpoint_partial':False}
        pn.publish(root/'stage-config.json',config);config['_sha']=pn.sha(root/'stage-config.json')
        common={'schema':1,'nonce':config['nonce'],'config_sha256':config['_sha'],'pid':1,'start_ms':2,'status':'pass'}
        pn.publish(root/'gate-report.json',common);gate=pn.sha(root/'gate-report.json');pn.publish(root/'controller-ack.json',{**common,'gate_sha256':gate});ack=pn.sha(root/'controller-ack.json')
        pn.publish(root/'gate-complete.json',{**common,'gate_sha256':gate,'ack_sha256':ack,'analysis_enabled':False});complete=pn.sha(root/'gate-complete.json')
        pn.publish(root/'analysis-outcome.json',{**common,'gate_sha256':gate,'complete_sha256':complete,'analysis_enabled':False,'timeout':False})
        pn.publish(root/'stage-result.json',{'schema':1,'status':'pass','returncode':0,'config_sha256':config['_sha'],'closure':{'closed':True,'reaped':True,'survivors':[],'ownership_gaps':[],'signaled':[]},
                 'milestones':{name:pn.sha(root/(name+'.json')) for name in ('gate-report','controller-ack','gate-complete','analysis-outcome')}})
        meta={'schema':1,'nonce':config['nonce'],'config_sha256':config['_sha'],'outcome_sha256':pn.sha(root/'analysis-outcome.json'),'capture_id':ident,'entry':entry,'state':'exported','profile_sha256':'profile','checkpoint_sha256':'checkpoint','partial':False,
              'completed':True,'timed_out':False,'cancelled':False,'failed_to_start':False,'null_code':False,'warnings':[],
              'code_sha256':pn.sha(code),'code_bytes':code.stat().st_size,'native_children':[]}
        pn.publish(cap/'metadata.json',meta)
        self.repin(root,ident)
        return ident,meta,entry
    def repin(self,root,ident):
        cap=root/'exports'/ident
        manifest={'schema':1,'capture_id':ident,'files':[{'path':x.name,'sha256':pn.sha(x),'bytes':x.stat().st_size} for x in (cap/'metadata.json',cap/'pseudocode.c') if x.exists()]}
        (cap/'manifest.json').write_text(json.dumps(manifest))
        meta=pn.read_json(cap/'metadata.json')
        (root/'export-summary.json').write_text(json.dumps({'schema':1,'nonce':meta['nonce'],'config_sha256':meta['config_sha256'],'outcome_sha256':meta['outcome_sha256'],'status':'pass','total':1,'profile_sha256':'profile','checkpoint_sha256':'checkpoint','partial':False,
            'captures':[{'capture_id':ident,'manifest_sha256':pn.sha(cap/'manifest.json'),'state':'exported'}]}))
    def test_completed_false_cannot_be_rehashed_into_successful_export(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();ident,meta,entry=self.make_export(root);meta['completed']=False
            (root/'exports'/ident/'metadata.json').write_text(json.dumps(meta));self.repin(root,ident)
            with self.assertRaises(ValueError):pn.verify_exports(root,{'profile_sha256':'profile','partial':False},checkpoint_sha='checkpoint',expected_entries=['ram:0x0'])
    def test_entry_body_contradiction_to_pinned_inventory_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();ident,meta,entry=self.make_export(root);original=dict(entry);meta['entry']['body_bytes']=12
            (root/'exports'/ident/'metadata.json').write_text(json.dumps(meta));self.repin(root,ident)
            with self.assertRaises(ValueError):pn.verify_exports(root,{'profile_sha256':'profile','partial':False},checkpoint_sha='checkpoint',expected_entries=['ram:0x0'],expected_records=[original])
    def test_forged_outcome_pin_cannot_be_rehashed_into_export_success(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();ident,meta,entry=self.make_export(root);meta['outcome_sha256']='0'*64
            (root/'exports'/ident/'metadata.json').write_text(json.dumps(meta));self.repin(root,ident)
            with self.assertRaises(ValueError):pn.verify_exports(root,{'profile_sha256':'profile','partial':False},checkpoint_sha='checkpoint',expected_entries=['ram:0x0'],expected_records=[entry])
    def test_warning_null_failure_and_partial_code_remain_distinct_captures(self):
        for state in ('exported-with-warnings','failed','failed-with-partial-code'):
            with self.subTest(state=state),tempfile.TemporaryDirectory() as td:
                root=Path(td).resolve();ident,meta,entry=self.make_export(root);meta['state']=state;meta['warnings']=['controlled unresolved-call diagnostic'];meta['completed']=state=='exported-with-warnings'
                if state=='failed':
                    (root/'exports'/ident/'pseudocode.c').unlink();meta['null_code']=True;meta.pop('code_sha256');meta.pop('code_bytes')
                (root/'exports'/ident/'metadata.json').write_text(json.dumps(meta));self.repin(root,ident)
                summary=pn.read_json(root/'export-summary.json');summary['captures'][0]['state']=state;(root/'export-summary.json').write_text(json.dumps(summary))
                accepted=pn.verify_exports(root,{'profile_sha256':'profile','partial':False},checkpoint_sha='checkpoint',expected_entries=['ram:0x0'],expected_records=[entry])
                self.assertEqual(accepted['captures'][0]['state'],state)

class SourceExitPublicationTests(unittest.TestCase):
    def source_exit_failure(self,job,checkpoint,parent):
        from contextlib import contextmanager
        @contextmanager
        def context():
            yield
            raise ValueError('injected source-after publication failure')
        return context()
    def fixture(self,root):
        job=root/'job';job.mkdir();checkpoint=root/'source';checkpoint.mkdir();(checkpoint/'manifest.json').write_bytes(b'parent');(job/'.incomplete').write_bytes(b'working')
        pn.publish(job/'admission.json',{'allocation_limit_bytes':pn.GIB})
        parent={'fixture':True,'target':str(root/'target'),'project':{},'partial':False,'profile':{}}
        return job,checkpoint,parent
    def test_analysis_source_exit_failure_prevents_checkpoint_and_success_publication(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();job,checkpoint,parent=self.fixture(root)
            def seal(*args,defer_commit=False,**kwargs):
                output=job/'checkpoint';output.mkdir()
                if defer_commit:return output,{'prepared':True}
                pn.publish(output/'manifest.json',{'status':'verified-closed'});pn.publish(job/'job-result.json',{'status':'pass'});return output
            with patch.object(pn,'load_checkpoint',return_value=parent),patch.object(pn,'prepare_job',return_value=(job,parent)),patch.object(pn,'copy_project',return_value=job/'project'),patch.object(pn,'run_stage',return_value=({},{})),patch.object(pn,'verify_project'),patch.object(pn,'source_integrity',side_effect=self.source_exit_failure),patch.object(pn,'seal_checkpoint',side_effect=seal):
                with self.assertRaises(ValueError):pn.analysis_job(root/'unused',checkpoint,fixture=True)
            self.assertFalse((job/'checkpoint/manifest.json').exists());self.assertFalse((job/'job-result.json').exists())
    def test_export_source_exit_failure_prevents_success_publication(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();job,checkpoint,parent=self.fixture(root)
            with patch.object(pn,'load_checkpoint',return_value=parent),patch.object(pn,'prepare_job',return_value=(job,parent)),patch.object(pn,'copy_project',return_value=job/'project'),patch.object(pn,'run_stage'),patch.object(pn,'verify_project'),patch.object(pn,'read_inventory'),patch.object(pn,'source_integrity',side_effect=self.source_exit_failure):
                with self.assertRaises(ValueError):pn.export_job(root/'unused',checkpoint,fixture=True)
            self.assertFalse((job/'job-result.json').exists())

class CompletionCommitTests(unittest.TestCase):
    def test_failed_success_report_publication_retains_checkpoint_acceptance_guard(self):
        with tempfile.TemporaryDirectory() as td:
            job=Path(td).resolve();checkpoint=job/'checkpoint';checkpoint.mkdir();(job/'.incomplete').write_bytes(b'working')
            pn.publish(job/'admission.json',{'started_monotonic':pn.time.monotonic(),'job_deadline_seconds':20,'allocation_limit_bytes':pn.GIB})
            manifest={'parent_checkpoint_sha256':'','project':{'allocated_bytes':1},'partial':False}
            real_publish=pn.publish
            def fail_report(path,value):
                if Path(path).name=='job-result.json':raise OSError('injected report fsync/publication failure')
                real_publish(path,value)
            with patch.object(pn,'validate_checkpoint_manifest'),patch.object(pn,'publish',side_effect=fail_report):
                with self.assertRaises(OSError):pn.commit_checkpoint(job,checkpoint,manifest)
            self.assertTrue((checkpoint/'manifest.json').exists());self.assertTrue((job/'.incomplete').exists())
            with self.assertRaises(ValueError):pn.load_checkpoint(checkpoint)
    def test_export_acceptance_rejects_valid_captures_until_commit(self):
        with tempfile.TemporaryDirectory() as td:
            job=Path(td).resolve();stage=job/'export';stage.mkdir();(job/'.incomplete').write_bytes(b'working')
            pn.publish(job/'admission.json',{'started_monotonic':pn.time.monotonic(),'job_deadline_seconds':20,'allocation_limit_bytes':pn.GIB})
            _,_,entry=ExportEvidenceConsistencyTests().make_export(stage)
            parent={'profile_sha256':'profile','partial':False}
            with self.assertRaises(ValueError):pn.verify_exports(stage,parent,checkpoint_sha='checkpoint',expected_entries=['ram:0x0'],expected_records=[entry])
            pn.verify_exports(stage,parent,checkpoint_sha='checkpoint',expected_entries=['ram:0x0'],expected_records=[entry],precommit=True)
            pn.commit_job_result(job,{'status':'pass'})
            pn.verify_exports(stage,parent,checkpoint_sha='checkpoint',expected_entries=['ram:0x0'],expected_records=[entry])

class FinalMilestoneAgreementTests(unittest.TestCase):
    def test_timeout_log_cannot_be_accepted_as_false_after_exit_zero(self):
        with tempfile.TemporaryDirectory() as td:
            stage=Path(td).resolve();config={'nonce':'n','_sha':'c','mode':'enable-analysis-after-ack'}
            common={'schema':1,'nonce':'n','config_sha256':'c','pid':1,'start_ms':2,'status':'pass'}
            pn.publish(stage/'gate-report.json',common);gate=pn.sha(stage/'gate-report.json')
            pn.publish(stage/'controller-ack.json',{**common,'gate_sha256':gate});ack=pn.sha(stage/'controller-ack.json')
            pn.publish(stage/'gate-complete.json',{**common,'gate_sha256':gate,'ack_sha256':ack,'analysis_enabled':True});complete=pn.sha(stage/'gate-complete.json')
            pn.publish(stage/'analysis-outcome.json',{**common,'gate_sha256':gate,'complete_sha256':complete,'analysis_enabled':False,'timeout':False})
            with self.assertRaises(ValueError):pn.validate_milestones(stage,config,'ANALYZING all memory and code:\nREPORT: Analysis timed out at 1 seconds\nREPORT: Save succeeded for:',0,False)
    def test_missing_or_negative_save_milestone_rejects_otherwise_valid_exit_zero(self):
        with tempfile.TemporaryDirectory() as td:
            stage=Path(td).resolve();config={'nonce':'n','_sha':'c','mode':'verify-only'};common={'schema':1,'nonce':'n','config_sha256':'c','pid':1,'start_ms':2,'status':'pass'}
            pn.publish(stage/'gate-report.json',common);gate=pn.sha(stage/'gate-report.json');pn.publish(stage/'controller-ack.json',{**common,'gate_sha256':gate});ack=pn.sha(stage/'controller-ack.json')
            pn.publish(stage/'gate-complete.json',{**common,'gate_sha256':gate,'ack_sha256':ack,'analysis_enabled':False});complete=pn.sha(stage/'gate-complete.json')
            pn.publish(stage/'analysis-outcome.json',{**common,'gate_sha256':gate,'complete_sha256':complete,'analysis_enabled':False,'timeout':False})
            for log in ('','REPORT: Save succeeded for:\nREPORT: Error trying to save','REPORT: Save succeeded for:\nREPORT: Save failed for:'):
                with self.subTest(log=log),self.assertRaises(ValueError):pn.validate_milestones(stage,config,log,0,False)
            pn.validate_milestones(stage,config,'REPORT: Save succeeded for:',0,False)

class LaunchRegistrationFailureTests(unittest.TestCase):
    @unittest.skipUnless(__import__('sys').platform=='darwin','libproc is macOS-specific')
    def test_constructor_signals_are_delivered_only_after_owned_registration(self):
        import os,signal,subprocess,sys,time
        real_execute=subprocess.Popen._execute_child
        for injected in (signal.SIGTERM,signal.SIGALRM,signal.SIGINT):
            with self.subTest(signal=injected),tempfile.TemporaryDirectory() as td,open(os.devnull,'wb') as stream:
                ready=Path(td).resolve()/'ready.json';owner=pn.Owner();children=[]
                code='import json,signal,time;from pathlib import Path;Path('+repr(str(ready))+').write_text(json.dumps({"term":int(signal.getsignal(signal.SIGTERM)),"alarm":int(signal.getsignal(signal.SIGALRM)),"mask":[int(x) for x in signal.pthread_sigmask(signal.SIG_BLOCK,[])]}));time.sleep(60)'
                previous=signal.getsignal(injected)
                def interrupt(sig,frame):raise RuntimeError('injected constructor cancellation')
                def after_spawn(child,*args,**kwargs):
                    real_execute(child,*args,**kwargs);children.append(child)
                    until=time.monotonic()+3
                    while not ready.exists() and time.monotonic()<until:time.sleep(.01)
                    if not ready.exists():raise AssertionError('actual child did not report signal disposition')
                    os.kill(os.getpid(),injected)
                try:
                    signal.signal(injected,interrupt)
                    with patch.object(subprocess.Popen,'_execute_child',after_spawn),self.assertRaisesRegex(RuntimeError,'injected constructor cancellation'):
                        owner.launch([sys.executable,'-c',code],stdout=stream,stderr=stream)
                    self.assertEqual(len(owner.processes),1,'constructor cancellation must not lose the owned Popen')
                    self.assertEqual(json.loads(ready.read_text()),{'term':0,'alarm':0,'mask':[]},'child must retain ordinary unmasked signal disposition')
                    closure=owner.close()
                    self.assertTrue(closure['closed']);self.assertTrue(closure['reaped']);self.assertFalse(closure['ownership_gaps']);self.assertFalse(closure['survivors'])
                finally:
                    signal.signal(injected,previous)
                    for child in children:
                        identity=pn.process_identity(child.pid)
                        if identity and child.poll() is None:pn.signal_matching(identity,signal.SIGKILL)
                        child.wait(timeout=5)
    def test_missing_identity_tracks_unreaped_child_without_unverified_signals(self):
        import subprocess
        class FakeChild:
            pid=987654321;returncode=None
            def poll(self):return None
            def wait(self,timeout):raise subprocess.TimeoutExpired('fake child',timeout)
            def terminate(self):raise AssertionError('unsafe unverified TERM')
        owner=pn.Owner();child=FakeChild()
        with patch.object(pn.subprocess,'Popen',return_value=child),patch.object(pn,'process_identity',return_value=None),patch.object(pn,'process_table',return_value={}):
            with self.assertRaises(RuntimeError):owner.launch(['fake'],stdout=None,stderr=None)
            closure=owner.close()
        self.assertEqual(owner.processes,[child]);self.assertFalse(closure['closed']);self.assertFalse(closure['reaped']);self.assertTrue(closure['ownership_gaps'])
    def test_identity_lookup_exception_is_registered_and_never_signaled(self):
        import subprocess
        class FakeChild:
            pid=987654321;returncode=None
            def poll(self):return None
            def wait(self,timeout):raise subprocess.TimeoutExpired('fake',timeout)
        owner=pn.Owner();child=FakeChild()
        with patch.object(pn.subprocess,'Popen',return_value=child),patch.object(pn,'process_identity',side_effect=OSError('lookup failed')),patch.object(pn,'process_table',return_value={}):
            with self.assertRaises(OSError):owner.launch(['fake'],stdout=None,stderr=None)
            closure=owner.close()
        self.assertEqual(owner.processes,[child]);self.assertFalse(closure['closed']);self.assertFalse(closure['reaped']);self.assertTrue(closure['ownership_gaps'])
    def test_pending_child_outside_birth_window_cannot_be_adopted(self):
        from types import SimpleNamespace
        owner=pn.Owner();owner.pending[42]=SimpleNamespace(returncode=None);owner.launch_windows[42]={'pid':42,'parent_pid':1,'before_us':10,'after_us':20}
        item={'pid':42,'ppid':1,'pgid':42,'sid':42,'start_us':21,'rss_bytes':1}
        with patch.object(pn,'process_table',return_value={42:item}),patch.object(pn.os,'kill') as kill:
            self.assertEqual(owner.sample(),[]);self.assertFalse(owner.roots);kill.assert_not_called()
    @unittest.skipUnless(__import__('sys').platform=='darwin','libproc is macOS-specific')
    def test_actual_term_ignoring_child_recovers_for_cleanup_but_gap_never_passes(self):
        import os,signal,sys,time
        real_identity=pn.process_identity;real_popen=pn.subprocess.Popen;children=[];owner=pn.Owner();first=True
        with tempfile.TemporaryDirectory() as td,open(os.devnull,'wb') as stream:
            ready=Path(td).resolve()/'ready'
            code='import os,signal,time;from pathlib import Path;signal.signal(signal.SIGTERM,signal.SIG_IGN);Path('+repr(str(ready))+').write_text(str(os.getpid()));time.sleep(60)'
            def launch(*args,**kwargs):child=real_popen(*args,**kwargs);children.append(child);return child
            def initially_missing(pid):
                nonlocal first
                if first:
                    first=False;until=time.monotonic()+5
                    while not ready.exists() and time.monotonic()<until:time.sleep(.01)
                    return None
                return real_identity(pid)
            try:
                with patch.object(pn.subprocess,'Popen',side_effect=launch),patch.object(pn,'process_identity',side_effect=initially_missing):
                    with self.assertRaises(RuntimeError):owner.launch([sys.executable,'-c',code],stdout=stream,stderr=stream)
                    closure=owner.close()
                self.assertFalse(closure['closed']);self.assertTrue(closure['reaped']);self.assertTrue(closure['ownership_gaps']);self.assertFalse(closure['survivors'])
                self.assertIsNone(real_identity(children[0].pid))
            finally:
                # Test-red cleanup retains its own actual identity even if the old owner forgot Popen.
                for child in children:
                    identity=real_identity(child.pid)
                    if identity and child.poll() is None:pn.signal_matching(identity,signal.SIGKILL)
                    child.wait(timeout=5)

class WholeJobDeadlineTests(unittest.TestCase):
    def test_stage_tail_hash_is_cancelled_after_owned_cleanup_finishes(self):
        import os,time
        from types import SimpleNamespace
        events=[];real_sha=pn.sha
        class FakeOwner:
            def launch(self,*args,**kwargs):return SimpleNamespace(returncode=0,poll=lambda:0)
            def sample(self):return []
            def close(self):events.append('cleanup-finished');return {'closed':True,'reaped':True,'signaled':[],'survivors':[],'ownership_gaps':[]}
        with tempfile.TemporaryDirectory() as td:
            job=Path(td).resolve();target=job/'fixture.bin';target.write_bytes(pn.FIXTURE_BYTES);project=job/'project';project.mkdir();(job/'.incomplete').write_bytes(b'working')
            def config(*args,**kwargs):return {'profile':{},'methods':{'native_decompiler':'offline-pin'},'nonce':'offline','target_sha256':pn.FIXTURE_SHA}
            def delayed_sha(path):
                if Path(path)==pn.NATIVE_DECOMPILER:return 'offline-pin'
                if Path(path)==pn.GHIDRA/'support/analyzeHeadless':return pn.LAUNCH_SHA
                if Path(path)==target and events:
                    events.append('tail-hash');time.sleep(1.1);events.append('tail-hash-returned')
                return real_sha(path)
            started=time.monotonic()
            with patch.object(pn,'Owner',FakeOwner),patch.object(pn,'make_config',side_effect=config),patch.object(pn,'validate_copied_methods'),patch.object(pn,'launch_command',return_value=(['offline-no-launch'],{})),patch.object(pn.shutil,'copy2'),patch.object(pn,'sha',side_effect=delayed_sha),patch.object(pn,'validate_milestones',side_effect=ValueError('offline missing outcome')),patch.object(pn,'process_table',return_value={os.getpid():{'rss_bytes':1024}}),patch.object(pn.shutil,'disk_usage',return_value=SimpleNamespace(free=8*pn.GIB)),self.assertRaises(RuntimeError):
                with pn.JobGuard(job,.3) as guard:
                    guard.owns_root=True;pn.run_stage(job/'stage',project,target,fixture=True,allocation_root=job)
            self.assertLess(time.monotonic()-started,.6,'non-cleanup tail must remain cancellable')
            self.assertIn('cleanup-finished',events);self.assertIn('tail-hash',events);self.assertNotIn('tail-hash-returned',events)
            self.assertTrue((job/'.incomplete').exists());self.assertFalse((job/'stage/stage-result.json').exists());self.assertFalse((job/'job-result.json').exists())
    def test_failure_monitor_publication_does_not_disable_cancellation(self):
        import time
        real_publish=pn.publish;events=[]
        with tempfile.TemporaryDirectory() as td:
            job=Path(td).resolve();(job/'.incomplete').write_bytes(b'working')
            def delayed_report(path,value):
                if Path(path).name=='job-monitor-failure.json':events.append('failure-report');time.sleep(1.1);events.append('failure-report-returned')
                return real_publish(path,value)
            started=time.monotonic()
            with patch.object(pn,'publish',side_effect=delayed_report),self.assertRaisesRegex(ValueError,'original failure'):
                with pn.JobGuard(job,.3) as guard:guard.owns_root=True;raise ValueError('original failure')
            self.assertLess(time.monotonic()-started,.6,'failure reporting must remain cancellable')
            self.assertEqual(events,['failure-report']);self.assertTrue((job/'.incomplete').exists());self.assertFalse((job/'job-monitor-failure.json').exists())
    def test_existing_incomplete_output_is_never_mutated_by_failure_report(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();job=root/'existing';job.mkdir();(job/'.incomplete').write_bytes(b'historical');target=root/'fixture.bin';target.write_bytes(pn.FIXTURE_BYTES)
            before={x.name:x.read_bytes() for x in job.iterdir()}
            with self.assertRaises(FileExistsError):pn.import_job(job,target,fixture=True)
            self.assertEqual({x.name:x.read_bytes() for x in job.iterdir()},before)
    def test_expired_checkpoint_cannot_publish_even_with_valid_preparation(self):
        with tempfile.TemporaryDirectory() as td:
            job=Path(td).resolve();checkpoint=job/'checkpoint';checkpoint.mkdir();(job/'.incomplete').write_bytes(b'working')
            pn.publish(job/'admission.json',{'started_monotonic':100,'job_deadline_seconds':600,'allocation_limit_bytes':pn.GIB})
            manifest={'parent_checkpoint_sha256':'','project':{'allocated_bytes':1},'partial':False}
            with patch.object(pn.time,'monotonic',return_value=701),patch.object(pn,'validate_checkpoint_manifest'):
                with self.assertRaises(RuntimeError):pn.commit_checkpoint(job,checkpoint,manifest)
            self.assertTrue((job/'.incomplete').exists());self.assertFalse((checkpoint/'manifest.json').exists());self.assertFalse((job/'job-result.json').exists())
    def test_actual_non_jvm_wait_is_cancelled_and_retains_guard(self):
        import time
        self.assertTrue(hasattr(pn,'JobGuard'),'whole-job cancellation context must exist')
        with tempfile.TemporaryDirectory() as td:
            job=Path(td).resolve();(job/'.incomplete').write_bytes(b'working');start=time.monotonic()
            with self.assertRaises(RuntimeError):
                with pn.JobGuard(job,.2):time.sleep(5)
            self.assertLess(time.monotonic()-start,1);self.assertTrue((job/'.incomplete').exists());self.assertFalse((job/'job-result.json').exists())
    def test_actual_copy_wait_is_cancelled_with_partial_tree_retained(self):
        import time
        with tempfile.TemporaryDirectory() as td:
            job=Path(td).resolve();source=job/'source';source.mkdir();(source/'recover.gpr').write_bytes(b'gpr');(source/'recover.rep').mkdir();manifest=pn.project_snapshot(source)
            (job/'.incomplete').write_bytes(b'working')
            def slow_copy(src,dest,**kwargs):Path(dest).write_bytes(b'partial');time.sleep(5)
            started=time.monotonic()
            with patch.object(pn.shutil,'copy2',side_effect=slow_copy),self.assertRaises(RuntimeError):
                with pn.JobGuard(job,.3):pn.copy_project(source,job/'copy',manifest)
            self.assertLess(time.monotonic()-started,1);self.assertTrue((job/'copy/recover.gpr').exists());self.assertTrue((job/'.incomplete').exists());pn.verify_project(source,manifest)
