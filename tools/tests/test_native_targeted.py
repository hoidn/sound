"""Selected-export model/process tests; do not import any native binary."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock,patch

spec=importlib.util.spec_from_file_location('targeted',Path(__file__).resolve().parents[1]/'run_targeted_native.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)

class TargetedTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        self.target=self.base/'synthetic.bin';self.target.write_bytes(b'synthetic tooling fixture, not native code')
        self.sha=hashlib.sha256(self.target.read_bytes()).hexdigest()
        self.ghidra=self.base/'ghidra';(self.ghidra/'Ghidra').mkdir(parents=True);(self.ghidra/'support').mkdir()
        (self.ghidra/'Ghidra/application.properties').write_text('application.version=12.1.4\n')
        (self.ghidra/'support/analyzeHeadless').touch();self.jdk=self.base/'jdk';(self.jdk/'bin').mkdir(parents=True);(self.jdk/'bin/java').touch()
        self.seed={'address':'0x1000','window_bytes':4096,'source':'synthetic test','label':'fixture'}
        self.config={'target':str(self.target),'target_sha256':self.sha,'seeds':[self.seed]}
        self.config_path=self.base/'config.json';self.config_path.write_text(json.dumps(self.config));self.output=self.base/'output'
        self.identity=patch.object(t,'TARGET_SHA256',self.sha);self.identity.start()
        self.disk=patch.object(t.shutil,'disk_usage',return_value=Mock(free=10*1024**3));self.disk.start()
    def tearDown(self):self.disk.stop();self.identity.stop();self.tmp.cleanup()
    def test_plan_is_separate_noanalysis_profile_and_bounded(self):
        settings,command,method=t.plan(self.config,self.output,self.ghidra,self.jdk)
        self.assertIn('-noanalysis',command);self.assertIn('-readOnly',command)
        self.assertEqual(settings['profile'],t.PROFILE);self.assertEqual(settings['overall_timeout_seconds'],600)
        self.assertEqual(settings['decompile_timeout_seconds'],60)
        self.assertEqual(settings['method_sha256'],t.digest(method));self.assertFalse(self.output.exists())
    def test_invalid_seed_windows_duplicates_and_limits(self):
        for address,size in [('0x1001',4096),('0x01000',4096),('EXTERNAL:0x1',4096),('../escape',4),('0x1000',0),('0x1000',65540),('0x1000',5),('0x1000',True),('0xfffffffffffffffc',8)]:
            with self.assertRaises(ValueError):t.validate_seeds([{**self.seed,'address':address,'window_bytes':size}])
        for seeds in ([],[self.seed]*2,[self.seed]*21):
            with self.assertRaises(ValueError):t.validate_seeds(seeds)
    def test_identity_and_version_fail_before_launch(self):
        self.target.write_bytes(b'changed')
        with self.assertRaises(ValueError):t.plan(self.config,self.output,self.ghidra,self.jdk)
        self.target.write_bytes(b'synthetic tooling fixture, not native code')
        (self.ghidra/'Ghidra/application.properties').write_text('application.version=99.0\n')
        with self.assertRaises(ValueError):t.plan(self.config,self.output,self.ghidra,self.jdk)
    def args(self,execute=False):
        return ['run_targeted_native.py','--config',str(self.config_path),'--output',str(self.output),'--ghidra',str(self.ghidra),'--jdk',str(self.jdk)]+(['--execute'] if execute else [])
    def test_default_prepares_without_starting_process(self):
        with patch('sys.argv',self.args()),patch.object(t.subprocess,'Popen') as process,contextlib.redirect_stdout(io.StringIO()):t.main()
        process.assert_not_called();self.assertFalse(self.output.exists())
    def test_failed_execution_retains_missing_results_and_manifest(self):
        peer=Mock(pid=1234);peer.wait.return_value=2;peer.poll.return_value=2
        with patch('sys.argv',self.args(True)),patch.object(t.subprocess,'Popen',return_value=peer),patch.object(t,'group_members',return_value={}),patch.object(t.signal,'signal'),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):t.main()
        status=json.loads((self.output/'run-status.json').read_text());self.assertEqual(status['exit_code'],2)
        self.assertEqual(status['items'][0]['state'],'missing')
        manifest=json.loads((self.output/'manifest.json').read_text());self.assertIn('method/SelectedNativeExport.java',manifest);self.assertIn('headless.log',manifest)
        self.assertEqual(manifest['run.json'],t.digest(self.output/'run.json'))
    def test_stop_group_escalates_only_owned_group_and_waits_for_survivors(self):
        peer=Mock(pid=6543);peer.poll.return_value=0
        members={7000:{'started':'known child','rss_bytes':1024}}
        values=iter(range(2,40,2))
        with patch.object(t,'capture_group',side_effect=[(members,True),(members,True),(members,True),({},False)]),patch.object(t.time,'monotonic',side_effect=lambda:next(values)),patch.object(t.time,'sleep'),patch.object(t.os,'killpg') as kill:
            result=t.stop_group(peer,{7000:'known child'})
        self.assertTrue(result['cleaned'])
        self.assertEqual([call.args[0] for call in kill.call_args_list],[6543,6543])
        self.assertEqual([call.args[1] for call in kill.call_args_list],[t.signal.SIGTERM,t.signal.SIGKILL])
    def test_identity_change_immediately_before_escalation_refuses_kill(self):
        peer=Mock(pid=6543);peer.poll.return_value=0
        members={7000:{'started':'known child','rss_bytes':1}};replacement={7000:{'started':'reused PID','rss_bytes':1}}
        values=iter(range(2,40,2))
        with patch.object(t,'capture_group',side_effect=[(members,True),(members,True),(replacement,False)]),patch.object(t.time,'monotonic',side_effect=lambda:next(values)),patch.object(t.time,'sleep'),patch.object(t.os,'killpg') as kill:
            result=t.stop_group(peer,{7000:'known child'})
        self.assertFalse(result['cleaned']);self.assertEqual(len(kill.call_args_list),1)
        self.assertEqual(kill.call_args.args,(6543,t.signal.SIGTERM))
    def test_resource_floor_stops_and_records_sample(self):
        peer=Mock(pid=6543,args=['synthetic']);peer.poll.return_value=None;peer.wait.side_effect=subprocess.TimeoutExpired('synthetic',1)
        self.output.mkdir()
        with patch.object(t,'group_members',return_value={6543:{'started':'fixture start','rss_bytes':1024}}),patch.object(t.shutil,'disk_usage',return_value=Mock(free=2*1024**3)):
            with self.assertRaisesRegex(RuntimeError,'3GiB'):t.supervise(peer,self.output,{})
        self.assertIn('free_disk_bytes',(self.output/'resources.jsonl').read_text())
    def test_pid_reuse_does_not_signal_unrelated_group(self):
        peer=Mock(pid=6543);peer.poll.return_value=0
        with patch.object(t,'group_members',return_value={7000:{'started':'new identity','rss_bytes':1}}),patch.object(t.os,'killpg') as kill:
            t.stop_group(peer,{7000:'old identity'})
        kill.assert_not_called()

    def test_invalid_metadata_does_not_prevent_closure_manifest(self):
        peer=Mock(pid=1234);peer.wait.return_value=0;peer.poll.return_value=0
        def fake_start(*args,**kwargs):
            directory=self.output/'functions'/'0x1000';directory.mkdir(parents=True);(directory/'metadata.json').write_text('{malformed')
            return peer
        with patch('sys.argv',self.args(True)),patch.object(t.subprocess,'Popen',side_effect=fake_start),patch.object(t,'group_members',return_value={}),patch.object(t.signal,'signal'),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):t.main()
        status=json.loads((self.output/'run-status.json').read_text());self.assertEqual(status['items'][0]['state'],'invalid')
        self.assertIn('functions/0x1000/metadata.json',json.loads((self.output/'manifest.json').read_text()))
    def test_exported_claim_without_payloads_is_invalid(self):
        settings,_,method=t.plan(self.config,self.output,self.ghidra,self.jdk)
        directory=self.output/'functions'/'0x1000';directory.mkdir(parents=True);(self.output/'method').mkdir();(self.output/'method/SelectedNativeExport.java').write_bytes(method.read_bytes())
        value={'address':'0x1000','target_sha256':self.sha,'profile':t.PROFILE,'provider':'ghidra-headless-selected-script','ghidra_version':'12.1.4','method_sha256':settings['method_sha256'],'state':'exported'}
        (directory/'metadata.json').write_text(json.dumps(value))
        self.assertEqual(t.outcomes(self.output,[self.seed],settings)[0]['state'],'invalid')
    def test_unverified_cleanup_defers_manifest_sealing(self):
        peer=Mock(pid=1234);peer.wait.return_value=0;peer.poll.return_value=0
        with patch('sys.argv',self.args(True)),patch.object(t.subprocess,'Popen',return_value=peer),patch.object(t,'group_members',return_value={}),patch.object(t.signal,'signal'),patch.object(t,'stop_group',return_value={'cleaned':False,'survivors':[7000]}),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):t.main()
        self.assertTrue((self.output/'run-status.json').exists());self.assertTrue((self.output/'manifest-pending.json').exists());self.assertFalse((self.output/'manifest.json').exists())

if __name__=='__main__':unittest.main()
