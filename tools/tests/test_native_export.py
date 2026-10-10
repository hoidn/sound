"""Corpus integrity tests against synthetic evidence, never provider execution."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

spec=importlib.util.spec_from_file_location('exporter',Path(__file__).resolve().parents[1]/'export_native_corpus.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
TARGET='a'*64
PROFILE={'digest':'b'*64,'provider':{'id':'ghidra','version':'12.1.4'},'parameters':{'architecture':'arm64'}}

def record(op,value,n=1):
    return {'evidence_id':'ev_'+f'{n:064x}','subject':{'digest':{'sha256':TARGET},'architecture':'arm64'},
            'provider':{'id':'ghidra','version':'12.1.4'},'analysis_profile':copy.deepcopy(PROFILE),
            'operation':op,'parameters':{'procedure':'0x1000'},'normalized_result':value,'limitations':[]}

def row(addr='0x1000',name='first',external=False):
    return {'address':addr,'value':name,'procedure':{'external':external,'thunk':False,'thunk_target':None}}

class ExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.root=self.base/'corpus'
        self.root.mkdir();self.source=self.base/'inventory.json';self.source.write_bytes(e.encoded(record('list_procedures',[row(),row(name='alias'),row('0x2000','import',True),row('0x3000','other')])))
        e.initialize(self.root,self.source,TARGET,'arm64')
    def tearDown(self):self.tmp.cleanup()
    def output(self,code='void first(void) {}',n=2):
        path=self.base/f'output-{n}.json';path.write_bytes(e.encoded(record('procedure_pseudo_code',code,n)));return path
    def test_duplicate_alias_and_explicit_external(self):
        c=e.coverage(self.root);self.assertEqual(c['unique_functions'],3);self.assertEqual(c['eligible'],2)
        self.assertEqual(c['functions'][0]['aliases'],['first','alias']);self.assertEqual(c['counts']['external'],1)
    def test_unchanged_resume_preserves_bytes(self):
        source=self.output();e.ingest(self.root,source)
        files={str(p):p.stat().st_mtime_ns for p in (self.root/'functions').rglob('*') if p.is_file()}
        c=e.ingest(self.root,source);self.assertEqual(c['successful'],1)
        self.assertEqual(files,{str(p):p.stat().st_mtime_ns for p in (self.root/'functions').rglob('*') if p.is_file()})
    def test_interrupted_staging_resumes(self):
        source=self.output()
        with self.assertRaises(InterruptedError):e.ingest(self.root,source,interrupt_before_commit=True)
        self.assertEqual(e.coverage(self.root)['attempted'],0)
        self.assertEqual(e.ingest(self.root,source)['successful'],1)
    def test_corrupt_committed_pseudocode_rejected(self):
        e.ingest(self.root,self.output());next((self.root/'functions').rglob('pseudocode.c')).write_text('tampered')
        with self.assertRaises(e.IntegrityError):e.coverage(self.root)
    def test_identity_and_profile_rejected(self):
        for key in ('subject','analysis_profile'):
            r=record('procedure_pseudo_code','code',4)
            if key=='subject':r[key]['digest']['sha256']='c'*64
            else:r[key]['digest']='c'*64
            source=self.base/'bad.json';source.write_bytes(e.encoded(r))
            with self.assertRaises(e.IntegrityError):e.ingest(self.root,source)
    def test_inventory_change_rejected(self):
        self.source.write_bytes(e.encoded(record('list_procedures',[row('0x9000')])))
        with self.assertRaises(e.IntegrityError):e.initialize(self.root,self.source,TARGET,'arm64')
    def test_conflicting_duplicate_rejected(self):
        with self.assertRaises(e.IntegrityError):e.freeze_inventory([row(),row(external=True)])
    def test_null_failure_and_warning(self):
        c=e.ingest(self.root,self.output(None));self.assertEqual(c['counts']['failed'],1)
        c=e.ingest(self.root,self.output('/* WARNING: unresolved jump */\ncode',3));self.assertEqual(c['counts']['exported-with-warnings'],1)
        self.assertEqual(c['attempted'],1);self.assertEqual(c['functions'][0]['attempts'],2)
    def test_partial_batch_mcp_envelope(self):
        r=record('batch_decompile',{'items':[{'address':'0x1000','procedure':{'status':'resolved','address':'0x1000','name':'first'},'status':'ok','pseudocode':'code'},
              {'address':'0x3000','procedure':{'status':'resolved','address':'0x3000'},'status':'error','error':{'message':'timeout'}}]},5)
        r['provider']={'id':'rea-workflow'};r['analysis_profile']={'digest':'d'*64,'parameters':{'upstream_analysis_profile':PROFILE}}
        source=self.base/'batch.json';source.write_bytes(e.encoded({'ok':True,'result':{'structuredContent':r}}))
        c=e.ingest(self.root,source);self.assertEqual(c['successful'],1);self.assertEqual(c['counts']['failed'],1)
    def test_corrupted_inventory_rejected(self):
        path=self.root/'inventory'/'v1.json';inv=json.loads(path.read_bytes());inv['functions'][0]['classification']='external';path.write_bytes(e.encoded(inv))
        with self.assertRaises(e.IntegrityError):e.coverage(self.root)
    def test_missing_authoritative_source_rejected(self):
        source=self.output();e.ingest(self.root,source)
        (self.root/'evidence'/f'{e.sha(source.read_bytes())}.json').unlink()
        with self.assertRaises(e.IntegrityError):e.coverage(self.root)
    def test_metadata_rewrite_cannot_override_evidence(self):
        e.ingest(self.root,self.output());path=next((self.root/'functions').rglob('metadata.json'))
        metadata=json.loads(path.read_bytes());metadata['state']='failed';path.write_bytes(e.encoded(metadata))
        manifest=path.parent/'manifest.json';m=json.loads(manifest.read_bytes());m['metadata.json']=e.sha(path.read_bytes());manifest.write_bytes(e.encoded(m))
        with self.assertRaises(e.IntegrityError):e.coverage(self.root)
    def test_error_with_partial_code_is_not_success(self):
        r=record('batch_decompile',{'items':[{'address':'0x1000','procedure':{'status':'resolved','address':'0x1000'},'status':'error','error':{'message':'partial'},'pseudocode':'partial code'}]},6)
        source=self.base/'partial.json';source.write_bytes(e.encoded(r));c=e.ingest(self.root,source)
        self.assertEqual(c['successful'],0);self.assertEqual(c['counts']['failed'],1)
        self.assertEqual(next((self.root/'functions').rglob('pseudocode.c')).read_text(),'partial code')
    def test_provider_external_address_space_inventory_and_queue(self):
        # ReaGhidraBridge procedures() includes getExternalFunctions(), whose
        # canonicalOffset() uses EXTERNAL:0x... instead of the default space.
        source=self.base/'external-inventory.json'
        source.write_bytes(e.encoded(record('list_procedures',[
            row('EXTERNAL:0x10','_external_later',True),
            row('0x1','_local',False), row('EXTERNAL:0x1','_external',True),
            row('EXTERNAL:0x2','_external_next',True)])))
        root=self.base/'external-corpus';root.mkdir()
        c=e.initialize(root,source,TARGET,'arm64')
        self.assertEqual([v['address'] for v in c['functions']],['0x1','EXTERNAL:0x1','EXTERNAL:0x2','EXTERNAL:0x10'])
        self.assertEqual(c['unique_functions'],4);self.assertEqual(c['eligible'],1)
        self.assertEqual(c['counts'],{'pending':1,'external':3})
        command=[sys.executable,str(Path(e.__file__)),'queue','--root',str(root)]
        self.assertEqual(json.loads(subprocess.check_output(command)),['0x1'])
        failure=record('procedure_pseudo_code',None,8);failure['parameters']['procedure']='EXTERNAL:0x1'
        failed=self.base/'external-null.json';failed.write_bytes(e.encoded(failure))
        c=e.ingest(root,failed);self.assertEqual(c['attempted'],0)
        self.assertEqual(c['functions'][1]['attempts'],1);self.assertEqual(c['functions'][1]['state'],'external')
        self.assertTrue((root/'functions'/'EXTERNAL:0x1').is_dir())
    def test_address_space_spelling_is_preserved_without_decoding(self):
        for value in ['EXTERNAL:0x1','overlay%20one:0x10','space%2Fname:0x1','..%2Foutside:0x1']:
            self.assertEqual(e.address(value),value)
            self.assertEqual(Path('functions')/e.address(value),Path('functions',value))
        self.assertEqual(e.address('EXTERNAL:0X000A'),'EXTERNAL:0xa')
        for value in ['../outside:0x1','space/name:0x1','space\\name:0x1','space%:0x1','space%2f:0x1',':0x1','EXTERNAL:0x1/../../bad','EXTERNAL:0x1\n']:
            with self.assertRaises(e.IntegrityError,msg=value):e.address(value)
    def test_case_distinct_space_paths_fail_before_corpus_writes(self):
        single=e.freeze_inventory([row('MixedCase:0x1','external',True)])
        self.assertEqual(single[0]['address'],'MixedCase:0x1')
        source=self.base/'case-collision.json'
        source.write_bytes(e.encoded(record('list_procedures',[
            row('SPACE:0x1','upper',True),row('space:0x1','lower',True)])))
        root=self.base/'case-collision-corpus';root.mkdir()
        with self.assertRaisesRegex(e.IntegrityError,'case-insensitive storage'):
            e.initialize(root,source,TARGET,'arm64')
        self.assertEqual(list(root.iterdir()),[])
    def test_unknown_classification_remains_visible(self):
        self.assertEqual(e.freeze_inventory([{'address':'0x1000','value':'unknown'}])[0]['classification'],'unclassified')

if __name__=='__main__':unittest.main()
