"""Offline reader checks use synthetic archives, never a target or GUI browser."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS));sys.path.insert(0,str(Path(__file__).parent))
import compact_native_corpus as compact
from test_native_compact import record,TARGET,PROFILE
try:import build_compact_native_browser as viewer
except ModuleNotFoundError:viewer=None
exporter=compact.exporter


def script_payload(path,prefix):
    text=path.read_text(encoding='utf-8')
    assert text.startswith(prefix) and text.endswith(';\n')
    body=text[len(prefix):-2]
    if prefix.endswith('('):body=body[:-1]
    return json.loads(body)


class ViewerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name).resolve()
        self.corpus=self.base/'corpus';self.corpus.mkdir();self.archive=self.base/'archive';self.output=self.base/'viewer'
        source=self.base/'inventory.json';source.write_bytes(exporter.encoded(record('list_procedures',[
            {'address':'0x1000','value':'café <script>','procedure':{'external':False}},
            {'address':'overlay%20one:0x10','value':'測定','procedure':{'external':False}},
            {'address':'0x2000','value':'no code','procedure':{'external':False}},
            {'address':'0x3000','value':'pending','procedure':{'external':False}}],1)))
        exporter.initialize(self.corpus,source,TARGET,'arm64')
        self.codes=['/* café 測定 🥁 <script>alert(1)</script> */\r\nvoid f() {}\r\n','/* incomplete */\n','/* WARNING: unresolved */\nvoid g() {}']
        for number,addr,status,code in [(2,'0x1000','ok',self.codes[0]),(3,'0x1000','error',self.codes[1]),
                                        (4,'overlay%20one:0x10','ok',self.codes[2]),(5,'0x2000','error',None)]:
            self.add(number,addr,status,code)
        (self.corpus/'.ingest.lock').touch()
        compact.build(self.corpus,self.archive,shard_size=2)
    def tearDown(self):self.tmp.cleanup()
    def add(self,number,addr,status,code):
        item={'address':addr,'status':status,'pseudocode':code}
        if status=='error':item['error']={'message':'timed out'}
        source=self.base/f'code-{number}.json';source.write_bytes(exporter.encoded(record('batch_decompile',{'items':[item]},number)))
        exporter.ingest(self.corpus,source)
    def build(self):
        self.assertIsNotNone(viewer,'Offline compact reader builder has not been implemented')
        return viewer.build(self.archive,self.output)
    def files(self,root):return {p.relative_to(root).as_posix():(p.read_bytes(),p.stat().st_mtime_ns) for p in root.rglob('*') if p.is_file()}
    def test_exact_code_and_provenance_for_every_revision(self):
        before=self.files(self.archive);result=self.build();self.assertEqual(self.files(self.archive),before)
        index=script_payload(self.output/'index.js','window.compactIndex=')
        self.assertEqual(index['counts'],{'addresses':3,'revisions':4,'code_revisions':3,'failed_revisions':2,'partial_revisions':1})
        self.assertEqual(index['identity']['target_sha256'],TARGET)
        self.assertEqual(index['identity']['analysis_profile'],PROFILE)
        self.assertNotIn(self.codes[0],(self.output/'index.js').read_text())
        code_records={}
        for chunk in index['chunks']:
            value=script_payload(self.output/chunk['path'],'window.receiveCompactChunk(')
            self.assertEqual(value['generation'],index['generation']);self.assertLessEqual(len(value['records']),100)
            for row in value['records']:code_records[row['key']]=row['code'].encode('utf-8')
        archived=compact.check(self.archive)
        for function in index['functions']:
            for revision in function['revisions']:
                code=revision['code']
                self.assertIn(revision['metadata']['member'],archived['_member_index'])
                if code is None:continue
                with compact.open_member(self.archive,archived,code['member']) as stream:expected=stream.read()
                self.assertEqual(code_records[function['address']+'|'+revision['revision']],expected)
                self.assertEqual(code['sha256'],exporter.sha(expected));self.assertEqual(code['bytes'],len(expected))
        self.assertEqual(viewer.check(self.output,archive=self.archive)['generation'],result['generation'])
        page=(self.output/'index.html').read_text()
        self.assertNotIn('chunks/code-',page);self.assertNotIn('fetch(',page)
        self.assertIn('adds no decompilation coverage',page)
    def test_fresh_destinations_symlinks_and_interruption(self):
        self.build();before=self.files(self.output)
        with self.assertRaises(compact.IntegrityError):viewer.build(self.archive,self.output)
        self.assertEqual(self.files(self.output),before)
        alias=self.base/'alias';alias.symlink_to(self.archive)
        with self.assertRaises(compact.IntegrityError):viewer.build(alias,self.base/'new')
        with self.assertRaises(compact.IntegrityError):viewer.build(self.archive,self.archive/'nested')
        interrupted=self.base/'interrupted'
        with self.assertRaises(InterruptedError):viewer.build(self.archive,interrupted,interrupt_before_publish=True)
        self.assertFalse(interrupted.exists());stages=list(self.base.glob('.interrupted.incomplete-*'))
        self.assertEqual(len(stages),1)
        with self.assertRaises(compact.IntegrityError):viewer.check(stages[0])
    def test_corruption_and_wrong_identity_fail_closed(self):
        self.build();index=self.output/'index.js';index.write_bytes(index.read_bytes()+b'bad')
        with self.assertRaises(compact.IntegrityError):viewer.check(self.output)
        shutil.rmtree(self.output);self.build()
        with self.assertRaises(compact.IntegrityError):viewer.check(self.output,expected_target='c'*64)
        with self.assertRaises(compact.IntegrityError):viewer.check(self.output,expected_profile=dict(PROFILE,digest='c'*64))
        manifest=compact.read_json(self.archive/'manifest.json');path=self.archive/manifest['archives'][0]['path'];path.write_bytes(path.read_bytes()+b'changed')
        with self.assertRaises(compact.IntegrityError):viewer.check(self.output,archive=self.archive)
    def test_missing_optional_viewer_preserves_existing_browser(self):
        self.assertIsNotNone(viewer,'Offline compact reader builder has not been implemented')
        self.assertEqual(viewer.project(self.base,self.corpus,str),(None,[]))
    def test_main_browser_projection_checks_zip_identity_and_links(self):
        self.assertIsNotNone(viewer,'Offline compact reader builder has not been implemented')
        self.output=self.base/'native-compact-view-v1';self.archive.rename(self.base/'native-compact-mirror-v1');self.archive=self.base/'native-compact-mirror-v1';self.build()
        projected,inputs=viewer.project(self.base,self.corpus,str)
        self.assertEqual(projected['state'],'verified');self.assertEqual(projected['counts']['addresses'],3)
        self.assertTrue(Path(projected['url']).is_file());self.assertTrue(inputs)
        manifest=compact.read_json(self.archive/'manifest.json');path=self.archive/manifest['archives'][0]['path'];path.write_bytes(path.read_bytes()+b'changed')
        projected,_=viewer.project(self.base,self.corpus,str)
        self.assertEqual(projected['state'],'invalid');self.assertNotIn('url',projected)

    def test_main_browser_prefers_new_reader_and_rejects_it_if_invalid(self):
        self.output=self.base/'native-compact-view-v2';self.archive.rename(self.base/'native-compact-mirror-v1');self.archive=self.base/'native-compact-mirror-v1';self.build()
        older=self.base/'native-compact-view-v1';older.mkdir();(older/'index.html').write_text('retained earlier publication')
        projected,_=viewer.project(self.base,self.corpus,str)
        self.assertEqual(projected['state'],'verified')
        self.assertEqual(Path(projected['url']),self.output/'index.html')
        (self.output/'reader.js').write_text('damaged new reader')
        projected,_=viewer.project(self.base,self.corpus,str)
        self.assertEqual(projected['state'],'invalid');self.assertNotIn('url',projected)
        self.assertEqual((older/'index.html').read_text(),'retained earlier publication')
    def test_chunk_size_and_revision_bounds_with_large_single_exception(self):
        self.assertIsNotNone(viewer,'Offline compact reader builder has not been implemented')
        huge='/* '+'🦕'*140000+' */\r\n';self.add(6,'0x2000','ok',huge)
        for i in range(101):self.add(7+i,'0x1000','ok',f'/* revision {i} */\n')
        shutil.rmtree(self.archive);compact.build(self.corpus,self.archive,shard_size=30);self.build()
        index=script_payload(self.output/'index.js','window.compactIndex=');seen=0;oversized=0
        for chunk in index['chunks']:
            payload=script_payload(self.output/chunk['path'],'window.receiveCompactChunk(')
            self.assertLessEqual(len(payload['records']),100);seen+=len(payload['records'])
            if chunk['oversized']:
                oversized+=1;self.assertEqual(len(payload['records']),1);self.assertEqual(payload['records'][0]['code'],huge)
            else:self.assertLessEqual(chunk['data_bytes'],512*1024)
        self.assertEqual(seen,105);self.assertEqual(oversized,1)

    def node_reader(self,assertions,preboot=''):
        self.build();index=script_payload(self.output/'index.js','window.compactIndex=')
        chunks={str(chunk['id']):script_payload(self.output/chunk['path'],'window.receiveCompactChunk(') for chunk in index['chunks']}
        prelude=r'''
const assert=require('node:assert/strict');
function element(tag='div') {return {tag,children:[],value:'',textContent:'',hidden:false,disabled:false,handlers:{},
 append(...children){this.children.push(...children)}, replaceChildren(...children){this.children=[...children]},
 addEventListener(type,callback){this.handlers[type]=callback}, remove(){this.removed=true}, click(){if(this.handlers.click)this.handlers.click()},
 focus(){document.activeElement=this}, scrollIntoView(){document.scrolledElement=this}};}
const ids=Object.fromEntries(['code-search','code-state','code-rows','code-count','code-prev','code-next','code-title','code-revision','code-load-status','code-retry','code-download','code-warning','code-provenance','code-text'].map(id=>[id,element()]));
const requests=[],blobs=[];const revoked=[];
global.document={currentScript:null,getElementById(id){return ids[id]},createElement:element,head:{append(script){requests.push(script)}}};
global.URL={createObjectURL(blob){blobs.push(blob);return 'blob:'+blobs.length},revokeObjectURL(url){revoked.push(url)}};
global.window={compactIndex:INDEX_DATA,compactGeneration:INDEX_DATA.generation};
const payloads=CHUNK_DATA;
function deliver(script,payload){document.currentScript=script;window.receiveCompactChunk(payload);document.currentScript=null;script.onload();}
function openAddress(address,revision){const row=ids['code-rows'].children.find(row=>row.children[0].textContent===address);assert.ok(row,address);row.children[4].children[0].click();if(revision){ids['code-revision'].value=revision;ids['code-revision'].handlers.change();}}
function latestRequest(){return requests.at(-1);}
function chunkOf(script){return Number(script.src.match(/code-(\d+)\.js/)[1]);}
'''.replace('INDEX_DATA',json.dumps(index,ensure_ascii=True)).replace('CHUNK_DATA',json.dumps(chunks,ensure_ascii=True))
        script=prelude+preboot+viewer.SCRIPT+"\n(async()=>{\n"+assertions+"\n})().catch(error=>{console.error(error);process.exitCode=1});"
        # Large payload fixtures belong in a file, not the OS argument vector.
        program=self.base/'reader-check.js';program.write_text(script,encoding='utf-8')
        result=subprocess.run([shutil.which('node'),str(program)],capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stderr)

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_read_revisions_brings_selected_reader_into_view(self):
        self.node_reader(r'''
openAddress('0x1000');
assert.equal(document.activeElement,ids['code-title'],'Reading a function should move keyboard focus to its reader');
assert.equal(document.scrolledElement,ids['code-title'],'Reading a function should reveal the panel below the table');
assert.match(ids['code-title'].textContent,/0x1000/);
assert.equal(requests.length,0,'Multiple revisions still require an explicit choice');
openAddress('0x2000');
assert.equal(document.activeElement,ids['code-title']);
assert.match(ids['code-load-status'].textContent,/No code payload/);
''')

    def test_code_is_before_collapsed_provenance(self):
        from html.parser import HTMLParser
        self.build()
        class Structure(HTMLParser):
            def __init__(self):super().__init__();self.tags=[];self.details=[];self.code=None;self.provenance=None;self.title=None
            def handle_starttag(self,tag,attrs):
                attrs=dict(attrs);self.tags.append((tag,attrs))
                if tag=='details':self.details.append(attrs)
                if attrs.get('id')=='code-text':self.code=(len(self.tags),list(self.details))
                if attrs.get('id')=='code-provenance':self.provenance=(len(self.tags),list(self.details))
                if attrs.get('id')=='code-title':self.title=attrs
            def handle_endtag(self,tag):
                if tag=='details':self.details.pop()
        structure=Structure();structure.feed((self.output/'index.html').read_text())
        self.assertLess(structure.code[0],structure.provenance[0],'Code must precede the long metadata block')
        self.assertEqual(structure.code[1],[])
        self.assertEqual(len(structure.provenance[1]),1)
        self.assertNotIn('open',structure.provenance[1][0],'Provenance should start collapsed')
        self.assertEqual(structure.title.get('tabindex'),'-1')

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_reader_explicit_revisions_safe_text_and_exact_download(self):
        self.node_reader(r'''
assert.equal(requests.length,0);assert.equal(ids['code-rows'].children.length,3);
openAddress('0x1000');assert.equal(requests.length,0);assert.equal(ids['code-revision'].children.length,3);
const first=window.compactIndex.functions.find(f=>f.address==='0x1000').revisions[0];
ids['code-revision'].value=first.revision;ids['code-revision'].handlers.change();
assert.equal(requests.length,1);deliver(latestRequest(),payloads[chunkOf(latestRequest())]);
const raw=payloads[0].records.find(r=>r.key==='0x1000|'+first.revision).code;
assert.equal(ids['code-text'].textContent,raw);assert.match(ids['code-text'].textContent,/<script>/);
assert.deepEqual(new Uint8Array(await blobs.at(-1).arrayBuffer()),new TextEncoder().encode(raw));
assert.match(ids['code-provenance'].textContent,/target_sha256/);assert.match(ids['code-provenance'].textContent,/pseudocode.c/);
const failed=window.compactIndex.functions[0].revisions.find(r=>r.state==='failed');
ids['code-revision'].value=failed.revision;ids['code-revision'].handlers.change();
assert.match(ids['code-warning'].textContent,/Failed.*partial/i);assert.equal(requests.length,1);
openAddress('0x2000');assert.equal(requests.length,1);assert.match(ids['code-load-status'].textContent,/No code/);assert.equal(ids['code-download'].hidden,true);
ids['code-state'].value='failed';ids['code-state'].handlers.input();assert.equal(ids['code-rows'].children.length,2);
ids['code-search'].value='absent';ids['code-search'].handlers.input();assert.equal(ids['code-rows'].children.length,0);
assert.match(ids['code-count'].textContent,/page 0 of 0/);
''')

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_reader_rejects_all_malformed_records_and_allows_retry(self):
        self.node_reader(r'''
const revision=window.compactIndex.functions[0].revisions[0].revision;
const broken=[p=>p.generation='f'.repeat(64),p=>p.records.at(-1).code+='wrong',p=>p.records.at(-1).key='unknown',p=>p.records.push(p.records[0]),p=>delete p.records[1],p=>p.records.at(-1).extra=true];
for(const change of broken){
 openAddress('0x1000',revision);const request=latestRequest();const payload=structuredClone(payloads[chunkOf(request)]);change(payload);deliver(request,payload);
 assert.equal(ids['code-text'].textContent,'');assert.equal(ids['code-retry'].hidden,false);assert.match(ids['code-load-status'].textContent,/failed/i);
 assert.equal(ids['code-rows'].children.length,3);ids['code-retry'].click();latestRequest().onerror();
}
ids['code-retry'].click();deliver(latestRequest(),payloads[chunkOf(latestRequest())]);assert.match(ids['code-text'].textContent,/void f/);
''')

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_reader_rapid_selection_ignores_stale_load_and_bounds_cache(self):
        # Three oversized enough records force distinct ordinary chunks.
        for i in range(3):self.add(20+i,'0x1000','ok','/* '+chr(65+i)*300000+' */\n')
        shutil.rmtree(self.archive);compact.build(self.corpus,self.archive,shard_size=2)
        self.node_reader(r'''
const revisions=window.compactIndex.functions[0].revisions.filter(r=>r.code && r.code.bytes>200000);
assert.equal(revisions.length,3);
openAddress('0x1000',revisions[0].revision);const old=latestRequest();
openAddress('0x1000',revisions[1].revision);const current=latestRequest();assert.notEqual(old,current);assert.equal(old.removed,true);
deliver(old,payloads[chunkOf(old)]);assert.equal(ids['code-text'].textContent,'');
deliver(current,payloads[chunkOf(current)]);assert.match(ids['code-text'].textContent,/BBBBB/);
openAddress('0x1000',revisions[2].revision);deliver(latestRequest(),payloads[chunkOf(latestRequest())]);
openAddress('0x1000',revisions[0].revision);deliver(latestRequest(),payloads[chunkOf(latestRequest())]);
const before=requests.length;openAddress('0x1000',revisions[1].revision);assert.equal(requests.length,before+1);
assert.equal(ids['code-text'].textContent,'');deliver(latestRequest(),payloads[chunkOf(latestRequest())]);assert.match(ids['code-text'].textContent,/BBBBB/);
''')

    def main_browser(self):
        import build_artifact_browser as generator
        if self.corpus.name!='native-live-arm64-v1':
            self.corpus.rename(self.base/'native-live-arm64-v1');self.corpus=self.base/'native-live-arm64-v1'
        fixtures={
            'native-targets.json':{'targets':[{'logical_path':f'Contents/MacOS/fixture-{i}','artifact_format':'Mach-O','sha256':TARGET,'size':8,'hash_status':'fixture'} for i in range(1093)]},
            'native-summary.json':{'plist':{'bundle':{'version':'synthetic'}},'symbol_counts':{'exports':0}},
            'push2-decompilation-summary.json':{'procedure':{'address':'0x1000'}},
            'evidence/push2-entry-dossier.json':{'normalized_result':{'assembly':[],'callees':[],'referenced_strings':[]}}}
        for name,value in fixtures.items():
            path=self.base/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value))
        modules=self.base/'midi-user-mapping-v1/disassembly';modules.mkdir(parents=True,exist_ok=True)
        for i in range(17):(modules/f'fixture-{i}.dis.txt').write_text('Synthetic disassembly fixture\n')
        with patch.object(generator,'ROOT',self.base),patch.object(generator,'ARTIFACTS',self.base),patch.object(generator,'OUT',self.base/'browse'):
            return generator.build(),(self.base/'browse/index.html').read_text()

    def test_main_browser_optional_integration_preserves_existing_anchors(self):
        manifest,page=self.main_browser()
        for anchor in ('python','native','selected-native','declared-starts'):
            self.assertIn('id="'+anchor+'"',page)
        self.assertEqual(manifest['counts']['python_disassembly_files'],17)
        self.assertIn('compact_native',manifest);self.assertIsNone(manifest['compact_native'])
        self.assertIn('artifact-storage-and-recovery.md',page)

    def test_main_browser_verified_mirror_is_linked_without_extra_coverage(self):
        self.assertIsNotNone(viewer,'Offline compact reader builder has not been implemented')
        self.output=self.base/'native-compact-view-v1';self.archive.rename(self.base/'native-compact-mirror-v1');self.archive=self.base/'native-compact-mirror-v1';self.build()
        manifest,page=self.main_browser()
        self.assertIn('../native-compact-view-v1/index.html',page)
        self.assertIn('adds no decompilation coverage',page)
        self.assertEqual(manifest['compact_native']['state'],'verified')
        self.assertEqual(manifest['compact_native']['counts']['addresses'],3)
        self.assertIn('compact_helper',manifest)
        self.assertTrue(any(p['path'].endswith('native-compact-view-v1/manifest.json') for p in manifest['inputs']))
        self.assertTrue(any(p['path'].endswith('.zip') for p in manifest['inputs']))
        bad=self.output/'reader.js';bad.write_bytes(bad.read_bytes()+b'bad')
        manifest,page=self.main_browser();self.assertEqual(manifest['compact_native']['state'],'invalid')
        self.assertNotIn('../native-compact-view-v1/index.html',page)
        self.assertIn('id="python"',page)

    def test_check_rejects_reauthored_script_and_unknown_method_identity(self):
        self.build()
        manifest_path=self.output/'manifest.json';manifest=json.loads(manifest_path.read_bytes())
        script=self.output/'reader.js';script.write_bytes(b'// reauthored reader\n')
        entry=next(row for row in manifest['outputs'] if row['path']=='reader.js')
        entry.update(bytes=script.stat().st_size,sha256=exporter.file_sha(script));manifest_path.write_bytes(exporter.encoded(manifest))
        with self.assertRaises(compact.IntegrityError):viewer.check(self.output,archive=self.archive)
        shutil.rmtree(self.output);self.build();manifest=json.loads(manifest_path.read_bytes());manifest['method']['unrecognized']='a'*64
        manifest_path.write_bytes(exporter.encoded(manifest))
        with self.assertRaises(compact.IntegrityError):viewer.check(self.output)

    def many_addresses(self):
        self.corpus=self.base/'many-corpus';self.corpus.mkdir();self.archive=self.base/'many-archive'
        source=self.base/'many-inventory.json';source.write_bytes(exporter.encoded(record('list_procedures',[
            {'address':hex(4096+i),'value':f'symbol_{i}','procedure':{'external':False}} for i in range(205)],200)))
        exporter.initialize(self.corpus,source,TARGET,'arm64')
        items=[{'address':hex(4096+i),'status':'ok','pseudocode':f'/* {i} */\n'} for i in range(205)]
        items[-1].update(status='error',error={'message':'bounded fixture failure'})
        source=self.base/'many-code.json';source.write_bytes(exporter.encoded(record('batch_decompile',{'items':items},201)))
        exporter.ingest(self.corpus,source);(self.corpus/'.ingest.lock').touch();compact.build(self.corpus,self.archive,shard_size=50)

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_reader_paginates_addresses_and_filters_named_states(self):
        self.many_addresses()
        self.node_reader(r'''
assert.equal(ids['code-rows'].children.length,100);assert.equal(requests.length,0);
ids['code-next'].click();assert.equal(ids['code-rows'].children.length,100);
ids['code-next'].click();assert.equal(ids['code-rows'].children.length,5);assert.equal(ids['code-next'].disabled,true);
ids['code-prev'].click();assert.equal(ids['code-rows'].children.length,100);
ids['code-state'].value='failed';ids['code-state'].handlers.input();assert.equal(ids['code-rows'].children.length,1);
assert.equal(ids['code-rows'].children[0].children[1].textContent,'symbol_204');
ids['code-state'].value='';ids['code-search'].value='0X1000 SYMBOL_0';ids['code-search'].handlers.input();assert.equal(ids['code-rows'].children.length,1);
''')

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_reader_validates_index_beyond_first_page_before_rendering(self):
        self.many_addresses()
        self.node_reader(r'''
assert.equal(ids['code-rows'].children.length,0);assert.equal(requests.length,0);
assert.match(ids['code-count'].textContent,/validation failed/);
''',preboot='window.compactIndex.functions[150].aliases=null;\n')

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_reader_uses_exporter_qualified_address_grammar(self):
        self.corpus=self.base/'spaces-corpus';self.corpus.mkdir();self.archive=self.base/'spaces-archive';address='overlay~%2Fone:0x1'
        source=self.base/'spaces-inventory.json';source.write_bytes(exporter.encoded(record('list_procedures',[
            {'address':address,'value':'encoded named space','procedure':{'external':False}}],300)))
        exporter.initialize(self.corpus,source,TARGET,'arm64');self.add(301,address,'ok','/* named space */\n')
        (self.corpus/'.ingest.lock').touch();compact.build(self.corpus,self.archive)
        self.node_reader(r'''
assert.equal(ids['code-rows'].children.length,1);
openAddress('overlay~%2Fone:0x1');deliver(latestRequest(),payloads[chunkOf(latestRequest())]);
assert.equal(ids['code-text'].textContent,'/* named space */\n');
''')

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_runtime_index_rejects_profile_arrays_and_coerced_provenance(self):
        # Both readers must reject the same JSON-shaped invalid provenance before
        # rendering even one address or starting a code load.
        def matching_profile_arrays(index):
            index['identity']['analysis_profile']=[]
            for function in index['functions']:
                for row in function['revisions']:row['analysis_profile']=[]
        cases=[('matching array profiles',matching_profile_arrays,
                'window.compactIndex.identity.analysis_profile=[];for(const fn of window.compactIndex.functions){for(const row of fn.revisions){row.analysis_profile=[];}}'),
               ('array inventory evidence ID',lambda index:index['identity'].update(inventory_evidence_id=[index['identity']['inventory_evidence_id']]),
                'window.compactIndex.identity.inventory_evidence_id=[window.compactIndex.identity.inventory_evidence_id];'),
               ('array revision evidence ID',lambda index:index['functions'][0]['revisions'][0].update(evidence_id=[index['functions'][0]['revisions'][0]['evidence_id']]),
                'window.compactIndex.functions[0].revisions[0].evidence_id=[window.compactIndex.functions[0].revisions[0].evidence_id];')]
        for label in ('metadata','manifest','code'):
            def coerce_archive(index,label=label):
                locator=index['functions'][0]['revisions'][0][label];locator['archive']=[locator['archive']]
            cases.append((f'array {label} ZIP locator',coerce_archive,
                          f'window.compactIndex.functions[0].revisions[0].{label}.archive=[window.compactIndex.functions[0].revisions[0].{label}.archive];'))
        for number,(name,mutate,preboot) in enumerate(cases):
            with self.subTest(case=name):
                self.output=self.base/f'invalid-viewer-{number}'
                self.node_reader(r'''
assert.equal(ids['code-rows'].children.length,0);
assert.equal(requests.length,0);
assert.match(ids['code-count'].textContent,/validation failed/);
''',preboot=preboot+'\n')
                invalid=script_payload(self.output/'index.js','window.compactIndex=');mutate(invalid)
                with self.assertRaises(compact.IntegrityError):viewer.validate_index(invalid)

    def workflow_archive(self,profile_extra=None):
        self.workflow_profile={'digest':'d'*64,'provider':{'id':'rea-workflow','version':'fixture'},
                               'parameters':{'upstream_analysis_profile':copy.deepcopy(PROFILE),'operation':'batch_decompile'},
                               'workflow_label':'Original workflow provenance'}
        self.workflow_provider={'id':'rea-workflow','version':'fixture','name':'REA composed investigation workflow'}
        if profile_extra is not None:self.workflow_profile['extra']=copy.deepcopy(profile_extra)
        self.workflow_revisions=[]
        for number,addr,status,code in [(400,'0x1000','ok','/* wrapped success */\r\n'),
                                        (401,'overlay%20one:0x10','ok','/* WARNING: wrapped warning */\n'),
                                        (402,'0x2000','error','/* wrapped partial */\n'),
                                        (403,'0x2000','error',None)]:
            item={'address':addr,'status':status,'pseudocode':code}
            if status=='error':item['error']={'message':'wrapped fixture failure'}
            evidence=record('batch_decompile',{'items':[item]},number)
            evidence['provider']=copy.deepcopy(self.workflow_provider);evidence['analysis_profile']=copy.deepcopy(self.workflow_profile)
            source=self.base/f'workflow-{number}.json';source.write_bytes(exporter.encoded(evidence));exporter.ingest(self.corpus,source)
            self.workflow_revisions.append('ev_'+f'{number:064x}'+'-0')
        shutil.rmtree(self.archive);compact.build(self.corpus,self.archive,shard_size=2)

    def test_workflow_profiles_preserve_original_and_resolve_native_authority(self):
        self.workflow_archive();before=self.files(self.archive);self.build();self.assertEqual(self.files(self.archive),before)
        index=script_payload(self.output/'index.js','window.compactIndex=')
        wrapped=[r for fn in index['functions'] for r in fn['revisions'] if r['revision'] in self.workflow_revisions]
        self.assertEqual(len(wrapped),4)
        for row in wrapped:
            self.assertEqual(row['analysis_profile'],self.workflow_profile)
            self.assertEqual(row['evidence_provider'],self.workflow_provider)
            self.assertEqual(row['effective_analysis_profile'],PROFILE)
            self.assertEqual(exporter.native_profile({'provider':row['evidence_provider'],'analysis_profile':row['analysis_profile']}),row['effective_analysis_profile'])
        self.assertEqual({row['state'] for row in wrapped},{'exported','exported-with-warnings','failed'})
        self.assertEqual(viewer.check(self.output,archive=self.archive)['counts']['revisions'],8)

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_reader_opens_wrapped_profiles_and_shows_both_provenances(self):
        self.workflow_archive()
        self.node_reader(r'''
const wrapped=window.compactIndex.functions.flatMap(fn=>fn.revisions.filter(row=>row.evidence_provider.id==='rea-workflow').map(row=>({fn,row})));
assert.equal(wrapped.length,4);
for(const {fn,row} of wrapped){
 openAddress(fn.address,row.revision);
 if(row.code && ids['code-text'].textContent===''){deliver(latestRequest(),payloads[chunkOf(latestRequest())]);}
 const shown=JSON.parse(ids['code-provenance'].textContent);
 assert.deepEqual(shown.analysis_profile,row.analysis_profile);
 assert.deepEqual(shown.evidence_provider,row.evidence_provider);
 assert.deepEqual(shown.effective_analysis_profile,window.compactIndex.identity.analysis_profile);
 if(row.state==='failed'){assert.match(ids['code-warning'].textContent,/Failed revision/);}
 if(!row.code){assert.equal(ids['code-download'].hidden,true);assert.match(ids['code-load-status'].textContent,/No code/);}
}
''')

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_workflow_upstream_and_effective_mismatches_reject_in_both_readers(self):
        self.workflow_archive()
        def wrapped(index):return next(row for fn in index['functions'] for row in fn['revisions'] if row['evidence_provider'].get('id')=='rea-workflow')
        cases=[
            ('missing parameters',lambda row:row['analysis_profile'].pop('parameters'),'delete row.analysis_profile.parameters;'),
            ('array parameters',lambda row:row['analysis_profile'].update(parameters=[]),'row.analysis_profile.parameters=[];'),
            ('missing upstream',lambda row:row['analysis_profile']['parameters'].pop('upstream_analysis_profile'),'delete row.analysis_profile.parameters.upstream_analysis_profile;'),
            ('array upstream',lambda row:row['analysis_profile']['parameters'].update(upstream_analysis_profile=[]),'row.analysis_profile.parameters.upstream_analysis_profile=[];'),
            ('array native digest',lambda row:row['analysis_profile']['parameters']['upstream_analysis_profile'].update(digest=['b'*64]),'row.analysis_profile.parameters.upstream_analysis_profile.digest=["b".repeat(64)];'),
            ('malformed native digest',lambda row:row['analysis_profile']['parameters']['upstream_analysis_profile'].update(digest='bad'),'row.analysis_profile.parameters.upstream_analysis_profile.digest="bad";'),
            ('native profile mismatch',lambda row:row['analysis_profile']['parameters']['upstream_analysis_profile'].update(digest='c'*64),'row.analysis_profile.parameters.upstream_analysis_profile.digest="c".repeat(64);'),
            ('effective profile mismatch',lambda row:row['effective_analysis_profile'].update(digest='c'*64),'row.effective_analysis_profile.digest="c".repeat(64);'),
            ('array effective profile',lambda row:row.update(effective_analysis_profile=[]),'row.effective_analysis_profile=[];'),
            ('array evidence provider',lambda row:row.update(evidence_provider=[]),'row.evidence_provider=[];'),
            ('wrong evidence provider',lambda row:row.update(evidence_provider={'id':'ghidra'}),'row.evidence_provider={id:"ghidra"};')]
        for number,(name,mutate,preboot) in enumerate(cases):
            with self.subTest(case=name):
                self.output=self.base/f'invalid-workflow-{number}'
                self.node_reader(r'''
assert.equal(ids['code-rows'].children.length,0);assert.equal(requests.length,0);
assert.match(ids['code-count'].textContent,/validation failed/);
''',preboot='const row=window.compactIndex.functions.flatMap(fn=>fn.revisions).find(row=>row.evidence_provider.id==="rea-workflow");'+preboot+'\n')
                invalid=script_payload(self.output/'index.js','window.compactIndex=');mutate(wrapped(invalid))
                with self.assertRaises(compact.IntegrityError):viewer.validate_index(invalid)

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_workflow_profile_mapping_order_is_semantically_equal(self):
        self.workflow_archive()
        self.node_reader(r'''
assert.equal(ids['code-rows'].children.length,3);assert.equal(requests.length,0);
const {address,revisions}=window.compactIndex.functions[0];const row=revisions.find(row=>row.evidence_provider.id==='rea-workflow');
openAddress(address,row.revision);deliver(latestRequest(),payloads[chunkOf(latestRequest())]);assert.match(ids['code-text'].textContent,/wrapped success/);
''',preboot='for(const fn of window.compactIndex.functions){for(const row of fn.revisions){row.effective_analysis_profile=Object.fromEntries(Object.entries(row.effective_analysis_profile).reverse());}}\n')

    def test_raw_workflow_source_binding_distinguishes_boolean_and_number(self):
        self.workflow_archive(profile_extra={'bool':True});verified=compact.check(self.archive);original=viewer.read_exact
        def altered_metadata(bundle,descriptor):
            data=original(bundle,descriptor)
            if descriptor['path'].endswith('/metadata.json'):
                metadata=json.loads(data)
                if metadata['analysis_profile'].get('workflow_label'):
                    metadata['analysis_profile']['extra']['bool']=1
                    return exporter.encoded(metadata)
            return data
        # Inject after exact ZIP read verification; retain original source bytes.
        with patch.object(viewer,'read_exact',altered_metadata):
            with self.assertRaises(compact.IntegrityError):viewer.project_revisions(self.archive,verified)

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_profile_json_value_equality_matches_javascript_semantics(self):
        cases=[('boolean versus one',True,1,False),('false versus zero',False,0,False),
               ('nested boolean versus number',{'x':[True,None]},{'x':[1,None]},False),
               ('object key order',{'a':True,'b':[1,None]},{'b':[1,None],'a':True},True),
               ('integer and decimal number',1,1.0,True),('number and string',1,'1',False),
               ('array order',[1,2],[2,1],False),('null',None,None,True)]
        for number,(name,left,right,equal) in enumerate(cases):
            with self.subTest(case=name):
                self.output=self.base/f'typed-profile-{number}'
                preboot='const left='+json.dumps(left)+';const right='+json.dumps(right)+';window.compactIndex.identity.analysis_profile.extra=right;for(const fn of window.compactIndex.functions){for(const row of fn.revisions){row.analysis_profile.extra=left;row.effective_analysis_profile.extra=right;}}\n'
                self.node_reader(f"assert.equal(ids['code-rows'].children.length,{3 if equal else 0});assert.equal(requests.length,0);",preboot=preboot)
                index=script_payload(self.output/'index.js','window.compactIndex=');index['identity']['analysis_profile']['extra']=copy.deepcopy(right)
                for function in index['functions']:
                    for row in function['revisions']:
                        row['analysis_profile']['extra']=copy.deepcopy(left);row['effective_analysis_profile']['extra']=copy.deepcopy(right)
                if equal:viewer.validate_index(index)
                else:
                    with self.assertRaises(compact.IntegrityError):viewer.validate_index(index)

    def test_expected_and_run_profiles_distinguish_boolean_from_number(self):
        self.corpus=self.base/'typed-corpus';self.corpus.mkdir();self.archive=self.base/'typed-archive'
        profile=copy.deepcopy(PROFILE);profile['extra']={'enabled':True}
        inventory=record('list_procedures',[{'address':'0x1000','value':'typed profile','procedure':{'external':False}}],500)
        inventory['analysis_profile']=copy.deepcopy(profile);source=self.base/'typed-inventory.json';source.write_bytes(exporter.encoded(inventory))
        exporter.initialize(self.corpus,source,TARGET,'arm64')
        output=record('batch_decompile',{'items':[{'address':'0x1000','status':'ok','pseudocode':'/* typed profile */\n'}]},501)
        output['analysis_profile']=copy.deepcopy(profile);source=self.base/'typed-code.json';source.write_bytes(exporter.encoded(output));exporter.ingest(self.corpus,source)
        (self.corpus/'.ingest.lock').touch();compact.build(self.corpus,self.archive);self.build()
        changed=copy.deepcopy(profile);changed['extra']['enabled']=1
        with self.assertRaises(compact.IntegrityError):viewer.check(self.output,expected_profile=changed)
        verified=compact.check(self.archive);verified['manifest']['source_identity']['run']['analysis_profile']=changed
        with self.assertRaises(compact.IntegrityError):viewer.project_revisions(self.archive,verified)
