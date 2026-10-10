"""Exact compact-mirror tests; all evidence and code are synthetic fixtures."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile

TOOLS=Path(__file__).resolve().parents[1]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
c=module('compact_native',TOOLS/'compact_native_corpus.py')
e=c.exporter
TARGET='a'*64
PROFILE={'digest':'b'*64,'provider':{'id':'ghidra','version':'12.1.4'},'parameters':{'architecture':'arm64'}}

def record(op,value,n):
    return {'evidence_id':'ev_'+f'{n:064x}','subject':{'digest':{'sha256':TARGET},'architecture':'arm64'},
            'provider':{'id':'ghidra'},'analysis_profile':copy.deepcopy(PROFILE),'operation':op,
            'parameters':{'procedure':'0x1000'},'normalized_result':value,'limitations':[]}

class CompactTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name).resolve();self.source=self.base/'corpus';self.source.mkdir()
        inventory=record('list_procedures',[
            {'address':'0x1000','value':'café <script>','procedure':{'external':False}},
            {'address':'overlay%20one:0x10','value':'測定','procedure':{'external':False}},
            {'address':'EXTERNAL:0x1','value':'external','procedure':{'external':True}},
            {'address':'0x2000','value':'pending','procedure':{'external':False}}],1)
        path=self.base/'inventory.json';path.write_bytes(e.encoded(inventory));e.initialize(self.source,path,TARGET,'arm64')
        for number,addr,status,code in [(2,'0x1000','ok','/* café 測定 */\nvoid f() {}\n'),
                                        (3,'0x1000','error','/* incomplete */\n'),
                                        (4,'overlay%20one:0x10','ok','/* WARNING: unresolved */\nvoid g() {}')]:
            item={'address':addr,'status':status,'pseudocode':code}
            if status=='error':item['error']={'message':'timed out'}
            path=self.base/f'output-{number}.json';path.write_bytes(e.encoded(record('batch_decompile',{'items':[item]},number)))
            e.ingest(self.source,path)
        (self.source/'.ingest.lock').touch()
        self.output=self.base/'compact'
    def tearDown(self):self.tmp.cleanup()
    def build(self):return c.build(self.source,self.output,shard_size=1)
    def files(self,root):
        return {str(p.relative_to(root)):(p.read_bytes(),p.stat().st_mtime_ns) for p in root.rglob('*') if p.is_file()}
    def rewrite_zip(self,archive,modify):
        path=self.output/archive
        with zipfile.ZipFile(path) as z:items=[(info,z.read(info.filename)) for info in z.infolist()]
        items=modify(items)
        with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for info,data in items:z.writestr(info,data)
        # Keep the outer hash consistent to exercise member validation itself.
        manifest=json.loads((self.output/'manifest.json').read_bytes())
        entry=next(a for a in manifest['archives'] if a['path']==archive)
        entry['sha256']=e.file_sha(path);entry['bytes']=path.stat().st_size
        (self.output/'manifest.json').write_bytes(e.encoded(manifest))
    def function_archive(self):
        manifest=json.loads((self.output/'manifest.json').read_bytes())
        return next(a['path'] for a in manifest['archives'] if a['kind']=='functions')
    def test_roundtrip_preserves_all_revisions_and_source_bytes(self):
        before=self.files(self.source);result=self.build();self.assertEqual(self.files(self.source),before)
        verified=c.check(self.output)
        self.assertEqual(verified['coverage']['counts'],{'exported':1,'exported-with-warnings':1,'external':1,'pending':1})
        self.assertEqual(len(verified['catalog']['functions']),2)
        self.assertEqual(sum(len(row['revisions']) for row in verified['catalog']['functions']),3)
        for row in verified['catalog']['functions']:
            for revision in row['revisions']:
                destination=self.base/f"extract-{revision['revision']}"
                c.extract(self.output,row['address'],destination,revision=revision['revision'])
                for relative in revision['members']:
                    self.assertEqual((destination/relative).read_bytes(),(self.source/relative).read_bytes())
        self.assertEqual(result['storage']['source']['logical_bytes'],sum(len(v[0]) for key,v in before.items() if key!='.ingest.lock'))
        self.assertGreater(result['storage']['compact']['allocated_bytes'],0)
    def test_failed_partial_code_and_unicode_labels_preserved(self):
        self.build();verified=c.check(self.output)
        row=verified['catalog']['functions'][0];self.assertIn('café <script>',row['aliases'])
        failed=next(r for r in row['revisions'] if r['state']=='failed')
        self.assertTrue(failed['partial_pseudocode']);self.assertTrue(any(p.endswith('pseudocode.c') for p in failed['members']))
    def test_qualified_address_canonicalization_and_revision_ambiguity(self):
        self.build()
        with self.assertRaises(c.IntegrityError):c.extract(self.output,'0x1000',self.base/'ambiguous')
        c.extract(self.output,'overlay%20one:0X0010',self.base/'qualified')
        for invalid in ['../0x1000','space/name:0x10','overlay%20one:0x10/../../bad']:
            with self.assertRaises(c.IntegrityError):c.extract(self.output,invalid,self.base/'invalid')
    def test_build_and_extract_refuse_existing_outputs(self):
        self.build();before=self.files(self.output)
        with self.assertRaises(c.IntegrityError):self.build()
        self.assertEqual(self.files(self.output),before)
        destination=self.base/'extract';destination.mkdir();(destination/'sentinel').write_bytes(b'preserve')
        with self.assertRaises(c.IntegrityError):c.extract(self.output,'overlay%20one:0x10',destination)
        self.assertEqual((destination/'sentinel').read_bytes(),b'preserve')
    def test_source_authority_and_stale_coverage_are_rejected_without_repair(self):
        checkpoint=self.source/'coverage.json';checkpoint.write_bytes(b'{"stale":true}\n');before=self.files(self.source)
        with self.assertRaises(c.IntegrityError):self.build()
        self.assertEqual(self.files(self.source),before);self.assertFalse(self.output.exists())
        e.coverage(self.source);code=next((self.source/'functions').rglob('pseudocode.c'));code.write_bytes(b'tampered')
        before=self.files(self.source)
        with self.assertRaises(c.IntegrityError):self.build()
        self.assertEqual(self.files(self.source),before)
    def test_source_validation_runs_under_writer_lock(self):
        import fcntl
        original=e.coverage;calls=[]
        def validating(root,*args,**kwargs):
            calls.append((root,kwargs.get('reader')))
            if root==self.source:
                with (root/'.ingest.lock').open('r+') as probe:
                    with self.assertRaises(BlockingIOError):fcntl.flock(probe,fcntl.LOCK_EX|fcntl.LOCK_NB)
            else:self.assertIsInstance(kwargs.get('reader'),c.ArchiveCorpusReader)
            self.assertEqual(kwargs.get('persist'),False)
            return original(root,*args,**kwargs)
        with patch.object(e,'coverage',validating):self.build()
        self.assertEqual(len(calls),2);self.assertEqual(calls[0],(self.source,None))
    def test_symlink_source_root_ancestor_payload_and_destination_rejected(self):
        alias=self.base/'alias';alias.symlink_to(self.source)
        with self.assertRaises(c.IntegrityError):c.build(alias,self.output)
        ancestor=self.base/'ancestor';ancestor.symlink_to(self.base)
        with self.assertRaises(c.IntegrityError):c.build(ancestor/'corpus',self.output)
        with self.assertRaises(c.IntegrityError):c.build(self.source,ancestor/'new')
        destination=self.base/'dangling';destination.symlink_to(self.base/'missing')
        with self.assertRaises(c.IntegrityError):c.build(self.source,destination)
        code=next((self.source/'functions').rglob('pseudocode.c'));saved=code.read_bytes();code.unlink();outside=self.base/'outside';outside.write_bytes(saved);code.symlink_to(outside)
        with self.assertRaises(c.IntegrityError):self.build()
        self.assertEqual(outside.read_bytes(),saved)
    def test_interruption_leaves_only_explicit_incomplete_stage(self):
        with self.assertRaises(InterruptedError):c.build(self.source,self.output,interrupt_before_publish=True)
        self.assertFalse(self.output.exists());stages=list(self.base.glob('.compact.incomplete-*'));self.assertEqual(len(stages),1)
        self.assertTrue((stages[0]/'.incomplete.json').is_file())
        with self.assertRaises(c.IntegrityError):c.check(stages[0])
        self.build();c.check(self.output)
    def test_build_does_not_archive_uncommitted_staging(self):
        stage=self.source/'.staging'/'incomplete';stage.mkdir(parents=True);(stage/'pseudocode.c').write_bytes(b'not committed')
        self.build();paths={m['path'] for a in c.check(self.output)['manifest']['archives'] for m in a['members']}
        self.assertFalse(any(path.startswith('.staging/') for path in paths))
    def test_tampered_archive_catalog_missing_and_extra_root_files_rejected(self):
        self.build();archive=self.output/self.function_archive();archive.write_bytes(archive.read_bytes()+b'bad')
        with self.assertRaises(c.IntegrityError):c.check(self.output)
        shutil.rmtree(self.output);self.build();catalog=self.output/'catalog.json';catalog.write_bytes(catalog.read_bytes()+b'bad')
        with self.assertRaises(c.IntegrityError):c.check(self.output)
        shutil.rmtree(self.output);self.build();(self.output/'extra').write_bytes(b'extra')
        with self.assertRaises(c.IntegrityError):c.check(self.output)
    def test_duplicate_unlisted_missing_traversal_symlink_zip_members_rejected(self):
        modifiers=[lambda items:items+[items[0]],lambda items:items+[(zipfile.ZipInfo('extra'),b'x')],lambda items:items[1:],
                   lambda items:items+[(zipfile.ZipInfo('../outside'),b'x')]]
        def symlink(items):
            info,data=items[0];info=copy.copy(info);info.create_system=3;info.external_attr=(stat.S_IFLNK|0o777)<<16;return [(info,data)]+items[1:]
        modifiers.append(symlink)
        for number,modify in enumerate(modifiers):
            with self.subTest(number=number):
                self.build();self.rewrite_zip(self.function_archive(),modify)
                with self.assertRaises(c.IntegrityError):c.check(self.output)
                shutil.rmtree(self.output)
    def test_rehashed_catalog_cannot_change_revision_state_or_locators(self):
        self.build();path=self.output/'catalog.json';catalog=json.loads(path.read_bytes());catalog['functions'][0]['revisions'][0]['state']='failed';path.write_bytes(e.encoded(catalog))
        manifest_path=self.output/'manifest.json';manifest=json.loads(manifest_path.read_bytes());manifest['catalog']['sha256']=e.file_sha(path);manifest['catalog']['bytes']=path.stat().st_size;manifest_path.write_bytes(e.encoded(manifest))
        with self.assertRaises(c.IntegrityError):c.check(self.output)
    def test_extract_verifies_before_creating_destination(self):
        self.build();archive=self.output/self.function_archive();archive.write_bytes(b'broken');destination=self.base/'extract'
        with self.assertRaises(c.IntegrityError):c.extract(self.output,'overlay%20one:0x10',destination)
        self.assertFalse(destination.exists());self.assertFalse(list(self.base.glob('.extract.incomplete-*')))
    def test_shard_boundaries_and_source_members_are_unique(self):
        self.build();manifest=c.check(self.output)['manifest'];archives=[a for a in manifest['archives'] if a['kind']=='functions']
        self.assertEqual(len(archives),3);paths=[m['path'] for a in manifest['archives'] for m in a['members']]
        self.assertEqual(len(paths),len(set(paths)));self.assertEqual(len([p for p in paths if p.startswith('evidence/')]),4)
        for invalid in [0,-1,True,10001]:
            with self.assertRaises(c.IntegrityError):c.build(self.source,self.base/f'bad-{invalid}',shard_size=invalid)
    def test_archive_check_rejects_symlink_root_file_and_dangling_extract(self):
        self.build();alias=self.base/'archive-alias';alias.symlink_to(self.output)
        with self.assertRaises(c.IntegrityError):c.check(alias)
        destination=self.base/'dangling-extract';destination.symlink_to(self.base/'missing')
        with self.assertRaises(c.IntegrityError):c.extract(self.output,'overlay%20one:0x10',destination)
        catalog=self.output/'catalog.json';saved=catalog.read_bytes();catalog.unlink();outside=self.base/'outside-catalog';outside.write_bytes(saved);catalog.symlink_to(outside)
        with self.assertRaises(c.IntegrityError):c.check(self.output)
    def test_unsafe_manifest_member_name_rejected(self):
        self.build();path=self.output/'manifest.json';manifest=json.loads(path.read_bytes());manifest['archives'][0]['members'][0]['path']='../outside';path.write_bytes(e.encoded(manifest))
        with self.assertRaises(c.IntegrityError):c.check(self.output)

    def test_malformed_manifest_catalog_and_missing_payload_raise_integrity_errors(self):
        changes=[lambda m:m.pop('source_identity'),lambda m:m.update({'source_storage':None}),
                 lambda m:m.update({'shard_size':True}),lambda m:m['archives'][0].update({'members':None})]
        for change in changes:
            with self.subTest(change=change):
                self.build();path=self.output/'manifest.json';manifest=json.loads(path.read_bytes());change(manifest);path.write_bytes(e.encoded(manifest))
                with self.assertRaises(c.IntegrityError):c.check(self.output)
                shutil.rmtree(self.output)
        self.build();(self.output/self.function_archive()).unlink()
        with self.assertRaises(c.IntegrityError):c.check(self.output)

    def test_selected_extract_interruption_and_archive_api(self):
        self.build();verified=c.check(self.output);row=verified['catalog']['functions'][1];revision=row['revisions'][0]
        path=next(path for path in revision['members'] if path.endswith('pseudocode.c'))
        with c.open_member(self.output,verified,path) as stream:self.assertEqual(stream.read(),(self.source/path).read_bytes())
        with c.open_archive(self.output,verified,revision['archive']) as bundle:self.assertEqual(bundle.read(path),(self.source/path).read_bytes())
        with self.assertRaises(c.IntegrityError):
            with c.open_member(self.output,verified,'run-does-not-exist.json'):self.fail('unknown opened')
        destination=self.base/'extract-interrupted'
        with self.assertRaises(InterruptedError):c.extract(self.output,row['address'],destination,interrupt_before_publish=True)
        self.assertFalse(destination.exists());stages=list(self.base.glob('.extract-interrupted.incomplete-*'))
        self.assertEqual(len(stages),1);self.assertTrue((stages[0]/'.incomplete.json').exists())

    def test_zip_copy_and_hashing_avoid_zipfile_read(self):
        # Copy/hash paths stream ZIP members. The shared JSON authority reads
        # one source at a time via open(), with its existing bounded cache.
        with patch.object(zipfile.ZipFile,'read',side_effect=AssertionError('whole member read')):
            self.build();c.check(self.output)

    def test_null_failure_has_no_invented_code_payload(self):
        path=self.base/'null.json';item={'address':'0x2000','status':'error','pseudocode':None,'error':{'message':'no output'}}
        path.write_bytes(e.encoded(record('batch_decompile',{'items':[item]},5)));e.ingest(self.source,path)
        self.build();verified=c.check(self.output);row=next(row for row in verified['catalog']['functions'] if row['address']=='0x2000')
        revision=row['revisions'][0];self.assertEqual(revision['state'],'failed');self.assertFalse(revision['partial_pseudocode'])
        self.assertFalse(any(path.endswith('pseudocode.c') for path in revision['members']))
        destination=self.base/'null-extract';c.extract(self.output,'0x2000',destination)
        self.assertFalse(list(destination.rglob('pseudocode.c')))

    def test_corrupt_member_rejected_even_when_outer_zip_hash_is_updated(self):
        self.build()
        def tamper(items):
            info,data=items[0];return [(info,bytes([data[0]^1])+data[1:])]+items[1:]
        self.rewrite_zip(self.function_archive(),tamper)
        with self.assertRaisesRegex(c.IntegrityError,'member content mismatch'):c.check(self.output)

    def test_cli_build_check_extract(self):
        import subprocess,sys
        command=[sys.executable,str(TOOLS/'compact_native_corpus.py')]
        report=json.loads(subprocess.check_output(command+['build','--corpus',str(self.source),'--output',str(self.output),'--shard-size','2']))
        self.assertEqual(report['coverage']['successful'],2)
        report=json.loads(subprocess.check_output(command+['check','--root',str(self.output)]));self.assertEqual(report['coverage']['attempted'],2)
        destination=self.base/'cli-extract';report=json.loads(subprocess.check_output(command+['extract','--root',str(self.output),'--address','overlay%20one:0x10','--output',str(destination)]))
        self.assertEqual(report['address'],'overlay%20one:0x10');self.assertTrue(destination.exists())

    def test_failed_rename_keeps_build_and_extract_staging_incomplete(self):
        self.build();source_before=self.files(self.source);compact_before=self.files(self.output)
        sentinel=self.base/'outside-sentinel';sentinel.write_bytes(b'preserve')
        for operation in ('build','extract'):
            destination=self.base/f'{operation}-rename-failed'
            with self.subTest(operation=operation),patch.object(c.os,'rename',side_effect=OSError('injected rename failure')):
                with self.assertRaises(c.IntegrityError):
                    if operation=='build':c.build(self.source,destination)
                    else:c.extract(self.output,'overlay%20one:0x10',destination)
            self.assertFalse(destination.exists())
            stages=list(self.base.glob('.'+destination.name+'.incomplete-*'));self.assertEqual(len(stages),1)
            self.assertTrue((stages[0]/'.incomplete.json').is_file())
            with self.assertRaises(c.IntegrityError):c.check(stages[0])
        self.assertEqual(self.files(self.source),source_before);self.assertEqual(self.files(self.output),compact_before)
        self.assertEqual(sentinel.read_bytes(),b'preserve')

    def test_failed_marker_removal_keeps_renamed_destinations_incomplete(self):
        self.build();source_before=self.files(self.source);compact_before=self.files(self.output)
        original_unlink=Path.unlink
        for operation in ('build','extract'):
            destination=self.base/f'{operation}-marker-failed'
            def failing_unlink(path,*args,**kwargs):
                if path==destination/'.incomplete.json':raise OSError('injected marker removal failure')
                return original_unlink(path,*args,**kwargs)
            with self.subTest(operation=operation),patch.object(Path,'unlink',failing_unlink):
                with self.assertRaises(c.IntegrityError):
                    if operation=='build':c.build(self.source,destination)
                    else:c.extract(self.output,'overlay%20one:0x10',destination)
            self.assertTrue(destination.is_dir());self.assertTrue((destination/'.incomplete.json').is_file())
            self.assertFalse(list(self.base.glob('.'+destination.name+'.incomplete-*')))
            with self.assertRaises(c.IntegrityError):c.check(destination)
            retained=self.files(destination)
            with self.assertRaises(c.IntegrityError):
                if operation=='build':c.build(self.source,destination)
                else:c.extract(self.output,'overlay%20one:0x10',destination)
            self.assertEqual(self.files(destination),retained)
        self.assertEqual(self.files(self.source),source_before);self.assertEqual(self.files(self.output),compact_before)

    def test_interruption_after_rename_leaves_marked_destination(self):
        source_before=self.files(self.source);original_rename=os.rename
        def rename_then_interrupt(source,destination):
            original_rename(source,destination);raise InterruptedError('injected interruption after rename')
        with patch.object(c.os,'rename',rename_then_interrupt):
            with self.assertRaises(InterruptedError):self.build()
        self.assertTrue((self.output/'.incomplete.json').is_file())
        with self.assertRaises(c.IntegrityError):c.check(self.output)
        self.assertEqual(self.files(self.source),source_before)

    def test_output_directory_open_and_fsync_fail_before_completion_commit(self):
        self.build();source_before=self.files(self.source);compact_before=self.files(self.output)
        original_open=os.open;original_fsync=os.fsync
        for operation in ('build','extract'):
            for failure in ('open','fsync'):
                destination=self.base/f'{operation}-final-{failure}';target_fds=set()
                def fail_open(path,*args,**kwargs):
                    if Path(path)==destination:
                        if failure=='open':raise OSError('injected final directory open failure')
                        fd=original_open(path,*args,**kwargs);target_fds.add(fd);return fd
                    return original_open(path,*args,**kwargs)
                def fail_fsync(fd):
                    if failure=='fsync' and fd in target_fds:raise OSError('injected final directory fsync failure')
                    return original_fsync(fd)
                with self.subTest(operation=operation,failure=failure),patch.object(c.os,'open',fail_open),patch.object(c.os,'fsync',fail_fsync):
                    with self.assertRaises(c.IntegrityError):
                        if operation=='build':c.build(self.source,destination)
                        else:c.extract(self.output,'overlay%20one:0x10',destination)
                self.assertTrue((destination/'.incomplete.json').is_file())
                with self.assertRaises(c.IntegrityError):c.check(destination)
        self.assertEqual(self.files(self.source),source_before);self.assertEqual(self.files(self.output),compact_before)

    def reauthor_revision(self,code=None,metadata_change=None):
        """Rehash a mutation without changing its authoritative source capture."""
        manifest_path=self.output/'manifest.json';manifest=json.loads(manifest_path.read_bytes())
        catalog_path=self.output/'catalog.json';catalog=json.loads(catalog_path.read_bytes())
        revision=catalog['functions'][0]['revisions'][0]
        archive=next(a for a in manifest['archives'] if a['path']==revision['archive']);archive_path=self.output/archive['path']
        with zipfile.ZipFile(archive_path) as bundle:
            infos=bundle.infolist();payloads={info.filename:bundle.read(info.filename) for info in infos}
        prefix=f"functions/{catalog['functions'][0]['address']}/{revision['revision']}/"
        if code is not None:payloads[prefix+'pseudocode.c']=code
        if metadata_change is not None:
            metadata=json.loads(payloads[prefix+'metadata.json']);metadata_change(metadata)
            payloads[prefix+'metadata.json']=e.encoded(metadata)
            revision['source_sha256']=metadata['source_sha256']
        payload_manifest=json.loads(payloads[prefix+'manifest.json'])
        for name in payload_manifest:payload_manifest[name]=e.sha(payloads[prefix+name])
        payloads[prefix+'manifest.json']=e.encoded(payload_manifest)
        with zipfile.ZipFile(archive_path,'w') as bundle:
            for info in infos:bundle.writestr(info,payloads[info.filename])
        for member in archive['members']:
            member['bytes']=len(payloads[member['path']]);member['sha256']=e.sha(payloads[member['path']])
        archive['bytes']=archive_path.stat().st_size;archive['sha256']=e.file_sha(archive_path)
        catalog_path.write_bytes(e.encoded(catalog));manifest['catalog']['bytes']=catalog_path.stat().st_size;manifest['catalog']['sha256']=e.file_sha(catalog_path)
        manifest['source_storage']['logical_bytes']=sum(m['bytes'] for a in manifest['archives'] for m in a['members'])
        manifest_path.write_bytes(e.encoded(manifest))

    def assert_authority_disagreement(self,**case):
        self.build();source_before=self.files(self.source);self.reauthor_revision(**case)
        with self.assertRaises(c.IntegrityError):c.check(self.output)
        self.assertEqual(self.files(self.source),source_before)

    def test_rehashed_code_disagreement_with_authority_is_rejected(self):
        self.assert_authority_disagreement(code=b'/* self-consistent altered code */\nvoid replacement() {}')

    def test_rehashed_metadata_profile_disagreement_with_authority_is_rejected(self):
        self.assert_authority_disagreement(metadata_change=lambda metadata:metadata['analysis_profile'].update({'digest':'c'*64}))

    def test_rehashed_metadata_inventory_source_link_is_rejected(self):
        self.assert_authority_disagreement(metadata_change=lambda metadata:metadata.update({'source_sha256':json.loads((self.source/'run.json').read_bytes())['inventory_source_sha256']}))

    def test_archive_authority_is_read_only_and_needs_no_original_files(self):
        self.build();renamed=self.base/'original-away';self.source.rename(renamed)
        verified=c.check(self.output);self.assertEqual(verified['coverage']['successful'],2)
        self.assertFalse((self.output/'inventory').exists());self.assertFalse((self.output/'evidence').exists());self.assertFalse((self.output/'functions').exists())

    def test_rehashed_inventory_disagreement_with_retained_source_is_rejected(self):
        self.build();manifest_path=self.output/'manifest.json';manifest=json.loads(manifest_path.read_bytes())
        archive=next(a for a in manifest['archives'] if any(m['path']=='inventory/v1.json' for m in a['members']))
        archive_path=self.output/archive['path']
        with zipfile.ZipFile(archive_path) as bundle:
            infos=bundle.infolist();payloads={info.filename:bundle.read(info.filename) for info in infos}
        inventory=json.loads(payloads['inventory/v1.json']);inventory['rows'][0]['value']='forged inventory alias'
        inventory['functions']=e.freeze_inventory(inventory['rows']);payloads['inventory/v1.json']=e.encoded(inventory)
        with zipfile.ZipFile(archive_path,'w') as bundle:
            for info in infos:bundle.writestr(info,payloads[info.filename])
        for member in archive['members']:
            member['bytes']=len(payloads[member['path']]);member['sha256']=e.sha(payloads[member['path']])
        archive['bytes']=archive_path.stat().st_size;archive['sha256']=e.file_sha(archive_path)
        manifest['source_identity']['inventory_sha256']=e.sha(payloads['inventory/v1.json'])
        manifest['source_storage']['logical_bytes']=sum(m['bytes'] for a in manifest['archives'] for m in a['members'])
        catalog_path=self.output/'catalog.json';catalog=json.loads(catalog_path.read_bytes());catalog['source_identity']=manifest['source_identity'];catalog_path.write_bytes(e.encoded(catalog))
        manifest['catalog']['bytes']=catalog_path.stat().st_size;manifest['catalog']['sha256']=e.file_sha(catalog_path);manifest_path.write_bytes(e.encoded(manifest))
        with self.assertRaisesRegex(c.IntegrityError,'Frozen inventory corrupted'):c.check(self.output)

if __name__=='__main__':unittest.main()
