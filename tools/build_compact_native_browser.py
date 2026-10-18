#!/usr/bin/env python3
"""Build a separate offline reader from an already verified exact native archive.

No target/analyzer/browser is launched. Builds require the complete archive
source authority. Later reader verification streams current archive file hashes
and compares every rendered revision/code to its original ZIP members, without
reloading the large inventory authority. Referenced evidence sources are read
once each, one complete envelope at a time (a count bound, not a byte bound).
ZIP archives remain immutable.
The generated JavaScript is trusted local code, not a hostile-script sandbox.
"""
import argparse
from collections import defaultdict
import html
import io
import json
import math
from pathlib import Path
import re
import compact_native_corpus as compact

IntegrityError=compact.IntegrityError
FORMAT='compact-native-view-v1'
INDEX='compact-native-index-v1'
CHUNK='compact-native-code-v1'
PAGE_ROWS=100
CHUNK_REVISIONS=100
CHUNK_BYTES=512*1024
CACHED_CHUNKS=2
BOUNDS={'page_rows':PAGE_ROWS,'chunk_revisions':CHUNK_REVISIONS,'chunk_data_bytes':CHUNK_BYTES,'cached_chunks':CACHED_CHUNKS}
INDEX_PREFIX='window.compactIndex='
CHUNK_PREFIX='window.receiveCompactChunk('


def json_data(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':'),allow_nan=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').replace('\u2028','\\u2028').replace('\u2029','\\u2029')


def same_json(a,b):
    """Compare JSON values: ordered arrays, unordered objects, distinct booleans.

    JSON numbers compare numerically (1 and 1.0 agree), independently of Python's
    bool subclass relationship. This matches the reader's sameJson rule for
    finite JSON values; unsupported Python objects are not JSON values.
    """
    if a is None or b is None:return a is None and b is None
    if isinstance(a,bool) or isinstance(b,bool):return type(a) is bool and type(b) is bool and a==b
    if type(a) in (int,float) or type(b) in (int,float):
        return (type(a) in (int,float) and type(b) in (int,float)
                and (type(a) is not float or math.isfinite(a))
                and (type(b) is not float or math.isfinite(b)) and a==b)
    if isinstance(a,str) or isinstance(b,str):return isinstance(a,str) and isinstance(b,str) and a==b
    if isinstance(a,list) or isinstance(b,list):
        return isinstance(a,list) and isinstance(b,list) and len(a)==len(b) and all(same_json(x,y) for x,y in zip(a,b))
    if isinstance(a,dict) and isinstance(b,dict):
        return (all(isinstance(key,str) for key in a) and all(isinstance(key,str) for key in b)
                and set(a)==set(b) and all(same_json(a[key],b[key]) for key in a))
    return False


def identity(verified,root):
    original=verified['manifest']['source_identity'];run=original['run']
    return {key:run[key] for key in ('target_sha256','architecture','analysis_profile','inventory_evidence_id')} | {
        'inventory_sha256':original['inventory_sha256'],'coverage_sha256':original['coverage_sha256'],
        'archive_manifest_sha256':compact.exporter.file_sha(root/'manifest.json'),
        'archive_catalog_sha256':verified['manifest']['catalog']['sha256']}


def method():
    return {'builder_sha256':compact.exporter.file_sha(Path(__file__)),
            'archive_tool_sha256':compact.exporter.file_sha(Path(compact.__file__)),
            'export_authority_sha256':compact.exporter.file_sha(Path(compact.exporter.__file__))}


def read_exact(bundle,descriptor):
    with bundle.open(descriptor['path']) as stream:data=stream.read()
    if len(data)!=descriptor['bytes'] or compact.exporter.sha(data)!=descriptor['sha256']:
        raise IntegrityError('Archive member changed while creating reader')
    return data


def effective_profile(profile,provider):
    """Use the exporter authority; metadata alone has no record-provider field."""
    if not isinstance(provider,dict):raise IntegrityError('Missing/malformed evidence provider')
    try:return compact.exporter.native_profile({'analysis_profile':profile,'provider':provider})
    except (AttributeError,TypeError) as cause:raise IntegrityError('Malformed native/workflow profile') from cause


def project_revisions(root,verified):
    members={entry['path']:(archive,entry) for archive,entry in compact.iter_members(verified)}
    grouped=defaultdict(list)
    functions=[];records=[];source_rows=defaultdict(list)
    for original in verified['catalog']['functions']:
        function={key:original[key] for key in ('address','aliases','classification','state')};function['revisions']=[];functions.append(function)
        for revision in original['revisions']:
            grouped[revision['archive']].append((function,revision))
    for name,group in grouped.items():
        with compact.open_archive(root,verified,name) as bundle:
            for function,revision in group:
                prefix=f"functions/{function['address']}/{revision['revision']}/"
                metadata_bytes=read_exact(bundle,members[prefix+'metadata.json'][1])
                metadata=compact.json_value(io.StringIO(metadata_bytes.decode('utf-8')))
                row={key:metadata[key] for key in ('revision','state','partial_pseudocode','warnings','evidence_id','source_sha256','source_record_index','source_item_index','error','limitations','details','analysis_profile')}
                source_rows[metadata['source_sha256']].append(row)
                for label in ('metadata','manifest'):
                    original_path=prefix+label+'.json'
                    row[label]={'archive':name,'member':original_path,**{k:members[original_path][1][k] for k in ('bytes','sha256')}}
                code_path=prefix+'pseudocode.c';row['code']=None
                if code_path in revision['members']:
                    descriptor=members[code_path][1];raw=read_exact(bundle,descriptor)
                    try:code=raw.decode('utf-8')
                    except UnicodeError as cause:raise IntegrityError('Code is not exact UTF-8') from cause
                    if code.encode('utf-8')!=raw:raise IntegrityError('Code UTF-8 round trip changed bytes')
                    row['code']={'archive':name,'member':code_path,**{k:descriptor[k] for k in ('bytes','sha256')}}
                    records.append({'key':function['address']+'|'+revision['revision'],'code':code})
                function['revisions'].append(row)
    # Resolve using the exact evidence-record provider, not an inferred provider
    # inside its profile. Read each referenced source once, one envelope at a
    # time; the inventory envelope is not loaded unless a revision references it.
    sources_by_archive=defaultdict(list)
    for source_hash in source_rows:
        member='evidence/'+source_hash+'.json'
        if member not in members:raise IntegrityError('Missing revision evidence source')
        name,descriptor=members[member];sources_by_archive[name].append((source_hash,descriptor))
    run=verified['manifest']['source_identity']['run']
    for name,sources in sources_by_archive.items():
        with compact.open_archive(root,verified,name) as bundle:
            for source_hash,descriptor in sources:
                incoming=compact.json_value(io.StringIO(read_exact(bundle,descriptor).decode('utf-8')))
                evidence=compact.exporter.records(incoming);resolved={}
                for row in source_rows[source_hash]:
                    number=row['source_record_index']
                    if type(number) is not int or not 0<=number<len(evidence):raise IntegrityError('Invalid revision evidence-record index')
                    if number not in resolved:
                        original=evidence[number];provider=original.get('provider',{})
                        profile=effective_profile(original.get('analysis_profile'),provider)
                        compact.exporter.validate(original,run)
                        if not same_json(profile,run['analysis_profile']):raise IntegrityError('Source native profile differs from run JSON values')
                        resolved[number]=(original,provider,profile)
                    original,provider,profile=resolved[number]
                    if row['evidence_id']!=original['evidence_id'] or not same_json(row['analysis_profile'],original['analysis_profile']):
                        raise IntegrityError('Revision profile/identity differs from exact source record')
                    row['evidence_provider']=provider
                    row['effective_analysis_profile']=effective_profile(row['analysis_profile'],provider)
                    if not same_json(row['effective_analysis_profile'],profile):raise IntegrityError('Resolved revision profile differs from source authority')
                # Do not retain complete envelopes between source members. The
                # returned rows retain only provider/profile fields and metadata.
                del incoming,evidence,resolved,original
    # ZIP grouping may have reordered revisions; preserve authoritative order.
    for function,original in zip(functions,verified['catalog']['functions']):
        order={r['revision']:i for i,r in enumerate(original['revisions'])};function['revisions'].sort(key=lambda r:order[r['revision']])
    order={function['address']+'|'+revision['revision']:i for i,(function,revision) in enumerate((f,r) for f in functions for r in f['revisions'])}
    records.sort(key=lambda record:order[record['key']])
    return functions,records


def counts(functions):
    revisions=[r for f in functions for r in f['revisions']]
    return {'addresses':len(functions),'revisions':len(revisions),'code_revisions':sum(r['code'] is not None for r in revisions),
            'failed_revisions':sum(r['state']=='failed' for r in revisions),'partial_revisions':sum(r['partial_pseudocode'] for r in revisions)}


def chunk_payload(number,records,generation):
    return {'schema':CHUNK,'generation':generation,'id':number,'records':records}


def split_records(records):
    groups=[];current=[]
    for record in records:
        candidate=current+[record]
        size=len(json_data(chunk_payload(len(groups),candidate,'0'*64)).encode('utf-8'))
        if current and (len(candidate)>CHUNK_REVISIONS or size>CHUNK_BYTES):
            groups.append(current);current=[]
        current.append(record)
        if len(json_data(chunk_payload(len(groups),current,'0'*64)).encode('utf-8'))>CHUNK_BYTES:
            groups.append(current);current=[]
    if current:groups.append(current)
    return groups


def generation(index,method_identity):
    base={key:value for key,value in index.items() if key!='generation'}
    return compact.exporter.sha(compact.exporter.encoded({'index':base,'method':method_identity}))


def parse_script(path,prefix):
    content=path.read_text(encoding='utf-8')
    suffix=');\n' if prefix==CHUNK_PREFIX else ';\n'
    if not content.startswith(prefix) or not content.endswith(suffix):raise IntegrityError('Invalid reader data script wrapper')
    return compact.json_value(io.StringIO(content[len(prefix):-len(suffix)]))


def validate_index(index):
    if (not isinstance(index,dict) or set(index)!={'schema','generation','identity','bounds','counts','functions','chunks'}
        or index['schema']!=INDEX or index['bounds']!=BOUNDS or not isinstance(index['generation'],str) or not compact.DIGEST.fullmatch(index['generation'])):
        raise IntegrityError('Unsupported reader index')
    functions=index['functions'];chunks=index['chunks']
    if not isinstance(functions,list) or not isinstance(chunks,list):raise IntegrityError('Invalid reader arrays')
    identity_keys={'target_sha256','architecture','analysis_profile','inventory_evidence_id','inventory_sha256','coverage_sha256','archive_manifest_sha256','archive_catalog_sha256'}
    info=index['identity']
    if (not isinstance(info,dict) or set(info)!=identity_keys
        or any(not isinstance(info[k],str) or not compact.DIGEST.fullmatch(info[k]) for k in ('target_sha256','inventory_sha256','coverage_sha256','archive_manifest_sha256','archive_catalog_sha256'))
        or not isinstance(info['architecture'],str) or not isinstance(info['analysis_profile'],dict)
        or not isinstance(info['inventory_evidence_id'],str) or not re.fullmatch(r'ev_[0-9a-f]{64}',info['inventory_evidence_id'])):
        raise IntegrityError('Invalid reader identity')
    effective_profile(info['analysis_profile'],{})
    seen=set();code_keys={}
    for function in functions:
        if (not isinstance(function,dict) or set(function)!={'address','aliases','classification','state','revisions'}
            or compact.exporter.address(function['address'])!=function['address'] or function['address'] in seen
            or not isinstance(function['aliases'],list) or any(not isinstance(v,str) for v in function['aliases'])
            or function['classification'] not in ('eligible','external','unclassified')
            or function['state'] not in ('pending','external','unclassified','exported','exported-with-warnings','failed')
            or not isinstance(function['revisions'],list) or not function['revisions']):raise IntegrityError('Malformed reader function')
        seen.add(function['address']);revisions=set()
        for row in function['revisions']:
            keys={'revision','state','partial_pseudocode','warnings','evidence_id','source_sha256','source_record_index','source_item_index','error','limitations','details','analysis_profile','evidence_provider','effective_analysis_profile','metadata','manifest','code'}
            if not isinstance(row,dict) or set(row)!=keys or not isinstance(row['revision'],str) or not compact.REVISION.fullmatch(row['revision']) or row['revision'] in revisions:
                raise IntegrityError('Malformed reader revision')
            revisions.add(row['revision'])
            if (row['state'] not in ('exported','exported-with-warnings','failed') or type(row['partial_pseudocode']) is not bool
                or not isinstance(row['evidence_id'],str) or not re.fullmatch(r'ev_[0-9a-f]{64}',row['evidence_id'])
                or not isinstance(row['source_sha256'],str) or not compact.DIGEST.fullmatch(row['source_sha256'])
                or any(type(row[k]) is not int or row[k]<0 for k in ('source_record_index','source_item_index'))
                or any(not isinstance(row[k],list) or any(not isinstance(v,str) for v in row[k]) for k in ('warnings','limitations'))
                or not same_json(row['effective_analysis_profile'],effective_profile(row['analysis_profile'],row['evidence_provider']))
                or not same_json(row['effective_analysis_profile'],index['identity']['analysis_profile'])):raise IntegrityError('Malformed reader revision provenance')
            for label in ('metadata','manifest','code'):
                descriptor=row[label]
                if descriptor is None:
                    if label!='code':raise IntegrityError('Missing metadata locator')
                    continue
                expected={'archive','member','bytes','sha256'}|({'chunk'} if label=='code' else set())
                if not isinstance(descriptor,dict) or set(descriptor)!=expected:raise IntegrityError('Malformed reader locator')
                compact.valid_descriptor({'path':descriptor['member'],'bytes':descriptor['bytes'],'sha256':descriptor['sha256']})
                expected_member=f"functions/{function['address']}/{row['revision']}/"+('pseudocode.c' if label=='code' else label+'.json')
                if descriptor['member']!=expected_member or not isinstance(descriptor['archive'],str) or not re.fullmatch(r'archives/functions-[0-9]{6}\.zip',descriptor['archive']):raise IntegrityError('Invalid reader ZIP locator')
                if label=='code':
                    if type(descriptor['chunk']) is not int or descriptor['chunk']<0:raise IntegrityError('Invalid chunk reference')
                    code_keys[function['address']+'|'+row['revision']]=descriptor
            if row['partial_pseudocode'] and (row['state']!='failed' or row['code'] is None):raise IntegrityError('Invalid failed/partial label')
            if row['state']!='failed' and row['code'] is None:raise IntegrityError('Successful revision has no code')
    if index['counts']!=counts(functions):raise IntegrityError('Reader counts disagree')
    assigned=set()
    for number,chunk in enumerate(chunks):
        if (not isinstance(chunk,dict) or set(chunk)!={'id','path','keys','oversized','data_bytes','records_sha256'}
            or type(chunk['id']) is not int or chunk['id']!=number or chunk['path']!=f'chunks/code-{number:06d}.js'
            or type(chunk['oversized']) is not bool or type(chunk['data_bytes']) is not int or chunk['data_bytes']<0
            or not isinstance(chunk['records_sha256'],str) or not compact.DIGEST.fullmatch(chunk['records_sha256'])
            or not isinstance(chunk['keys'],list) or not 1<=len(chunk['keys'])<=CHUNK_REVISIONS
            or any(not isinstance(k,str) or k not in code_keys or k in assigned or code_keys[k]['chunk']!=number for k in chunk['keys'])):
            raise IntegrityError('Malformed code chunk descriptor')
        if len(set(chunk['keys']))!=len(chunk['keys']):raise IntegrityError('Duplicate chunk keys')
        assigned.update(chunk['keys'])
        if chunk['oversized']!=(chunk['data_bytes']>CHUNK_BYTES) or chunk['oversized'] and len(chunk['keys'])!=1:raise IntegrityError('Invalid oversized chunk exception')
    if assigned!=set(code_keys):raise IntegrityError('Unassigned code revision')
    return code_keys


def validate_chunk(payload,index,chunk,code_keys):
    if (not isinstance(payload,dict) or set(payload)!={'schema','generation','id','records'} or payload['schema']!=CHUNK
        or payload['generation']!=index['generation'] or type(payload['id']) is not int or payload['id']!=chunk['id']
        or not isinstance(payload['records'],list) or len(payload['records'])!=len(chunk['keys'])):raise IntegrityError('Malformed/stale code chunk')
    for row,key in zip(payload['records'],chunk['keys']):
        if not isinstance(row,dict) or set(row)!={'key','code'} or row['key']!=key or not isinstance(row['code'],str):raise IntegrityError('Malformed code record')
        raw=row['code'].encode('utf-8');descriptor=code_keys[key]
        if len(raw)!=descriptor['bytes'] or compact.exporter.sha(raw)!=descriptor['sha256']:raise IntegrityError('Derived code bytes differ from original hash')
    if (len(json_data(payload).encode('utf-8'))!=chunk['data_bytes']
        or compact.exporter.sha(json_data(payload['records']).encode('utf-8'))!=chunk['records_sha256']):raise IntegrityError('Code chunk payload digest/size disagrees')


def archive_snapshot(root,expected_manifest,expected_catalog):
    root=compact.safe_path(root);files=compact.regular_files(root)
    if '.incomplete.json' in files:raise IntegrityError('Archive has not committed')
    manifest=compact.read_json(root/'manifest.json')
    if compact.exporter.file_sha(root/'manifest.json')!=expected_manifest:raise IntegrityError('Reader archive manifest changed')
    if manifest.get('format')!=compact.FORMAT or manifest.get('status')!='complete' or manifest.get('schema')!=1:raise IntegrityError('Invalid archive snapshot')
    catalog_descriptor=manifest['catalog'];compact.valid_descriptor(catalog_descriptor)
    if catalog_descriptor['path']!='catalog.json' or catalog_descriptor['sha256']!=expected_catalog:raise IntegrityError('Reader archive catalog changed')
    descriptors=[catalog_descriptor,*manifest['archives']];expected={'manifest.json'};members={};archive_index={}
    for descriptor in descriptors:
        compact.valid_descriptor({k:descriptor[k] for k in ('path','bytes','sha256')})
        if descriptor['path'] in expected:raise IntegrityError('Duplicate archive file')
        expected.add(descriptor['path']);path=compact.safe_path(root/descriptor['path'],kind='file')
        if path.stat().st_size!=descriptor['bytes'] or compact.exporter.file_sha(path)!=descriptor['sha256']:raise IntegrityError('Current archive file differs from pinned snapshot')
        if descriptor is not catalog_descriptor:
            if not re.fullmatch(r'archives/(sources|functions)-[0-9]{6}\.zip',descriptor['path']):raise IntegrityError('Invalid ZIP file locator')
            archive_index[descriptor['path']]=descriptor
            for member in descriptor['members']:
                compact.valid_descriptor(member);compact.original_path(member['path'])
                if member['path'] in members:raise IntegrityError('Duplicate archive member')
                members[member['path']]=(descriptor['path'],member)
    if set(files)!=expected:raise IntegrityError('Archive files differ from snapshot manifest')
    catalog=compact.read_json(root/'catalog.json')
    if not same_json(catalog['source_identity'],manifest['source_identity']) or catalog['format']!=compact.FORMAT:raise IntegrityError('Archive snapshot identities disagree')
    return {'manifest':manifest,'catalog':catalog,'_member_index':members,'_archive_index':archive_index}


@compact.integrity_errors
def check(root,*,archive=None,expected_target=None,expected_profile=None,expected_inventory=None,_allow_incomplete=False):
    root=compact.safe_path(root);files=compact.regular_files(root)
    if not _allow_incomplete and '.incomplete.json' in files:raise IntegrityError('Unpublished incomplete reader')
    manifest=compact.read_json(root/'manifest.json')
    if (not isinstance(manifest,dict) or set(manifest)!={'schema','format','status','generation','identity','counts','method','outputs','source_archive','limits','limitations'}
        or manifest.get('schema')!=1 or manifest.get('format')!=FORMAT or manifest.get('status')!='complete'
        or manifest['method']!=method() or manifest['limits']!=BOUNDS or not isinstance(manifest['outputs'],list)
        or not isinstance(manifest['source_archive'],str) or not isinstance(manifest['limitations'],list)
        or any(not isinstance(v,str) for v in manifest['limitations'])):raise IntegrityError('Invalid or stale reader manifest/method')
    expected={'manifest.json'}|({'.incomplete.json'} if _allow_incomplete else set());pins=[]
    for descriptor in manifest['outputs']:
        compact.valid_descriptor(descriptor);name=descriptor['path']
        if name not in ('index.html','index.js','reader.js') and not re.fullmatch(r'chunks/code-[0-9]{6}\.js',name):raise IntegrityError('Unknown reader output')
        if name in expected:raise IntegrityError('Duplicate reader output')
        expected.add(name);path=compact.safe_path(root/name,kind='file')
        if path.stat().st_size!=descriptor['bytes'] or compact.exporter.file_sha(path)!=descriptor['sha256']:raise IntegrityError('Reader output hash/size mismatch')
        pins.append(path)
    if set(files)!=expected or not {'index.html','index.js','reader.js'}<=expected:raise IntegrityError('Reader output file set differs')
    index=parse_script(root/'index.js',INDEX_PREFIX);code_keys=validate_index(index)
    required={'manifest.json','index.html','index.js','reader.js'}|{chunk['path'] for chunk in index['chunks']}|({'.incomplete.json'} if _allow_incomplete else set())
    if expected!=required:raise IntegrityError('Reader has unindexed/missing chunks')
    if ((root/'reader.js').read_bytes()!=SCRIPT.encode('utf-8')
        or (root/'index.html').read_bytes()!=page(index).encode('utf-8')):raise IntegrityError('Reader scripts/page differ from the pinned generator')
    if generation(index,manifest['method'])!=index['generation'] or index['generation']!=manifest['generation'] or not same_json(manifest['identity'],index['identity']) or manifest['counts']!=index['counts']:
        raise IntegrityError('Reader generation binding disagrees')
    if expected_target is not None and index['identity']['target_sha256']!=expected_target:raise IntegrityError('Reader target mismatch')
    if expected_profile is not None and not same_json(index['identity']['analysis_profile'],expected_profile):raise IntegrityError('Reader profile mismatch')
    if expected_inventory is not None and index['identity']['inventory_sha256']!=expected_inventory:raise IntegrityError('Reader inventory mismatch')
    derived=[]
    for chunk in index['chunks']:
        payload=parse_script(root/chunk['path'],CHUNK_PREFIX);validate_chunk(payload,index,chunk,code_keys);derived.extend(payload['records'])
    archive_pins=[]
    if archive is not None:
        archive=compact.safe_path(archive);verified=archive_snapshot(archive,index['identity']['archive_manifest_sha256'],index['identity']['archive_catalog_sha256'])
        if not same_json(identity(verified,archive),index['identity']):raise IntegrityError('Reader/archive identity mismatch')
        originals,records=project_revisions(archive,verified)
        rows=json.loads(json.dumps(index['functions']))
        for function in rows:
            for revision in function['revisions']:
                if revision['code'] is not None:revision['code'].pop('chunk')
        if not same_json(rows,originals) or derived!=records:raise IntegrityError('Reader revisions/code disagree with exact archive members')
        archive_pins=list(compact.regular_files(archive).values())
    return {'root':str(root),'generation':index['generation'],'identity':index['identity'],'counts':index['counts'],
            'inputs':[root/'manifest.json',*pins,*archive_pins],
            'verification':'all derived code hashes; exact current ZIP members' if archive is not None else 'derived payload hashes only; archive not checked'}


@compact.integrity_errors
def build(archive,output,*,interrupt_before_publish=False):
    archive=compact.safe_path(archive);output=compact.safe_path(output,fresh=True)
    if output.is_relative_to(archive):raise IntegrityError('Reader destination must be outside immutable archive')
    verified=compact.check(archive);functions,records=project_revisions(archive,verified)
    groups=split_records(records);chunks=[];references={}
    for number,group in enumerate(groups):
        keys=[row['key'] for row in group];references.update((key,number) for key in keys)
        size=len(json_data(chunk_payload(number,group,'0'*64)).encode('utf-8'))
        chunks.append({'id':number,'path':f'chunks/code-{number:06d}.js','keys':keys,'oversized':size>CHUNK_BYTES,
                       'data_bytes':size,'records_sha256':compact.exporter.sha(json_data(group).encode('utf-8'))})
    for function in functions:
        for revision in function['revisions']:
            if revision['code'] is not None:revision['code']['chunk']=references[function['address']+'|'+revision['revision']]
    index={'schema':INDEX,'identity':identity(verified,archive),'bounds':BOUNDS,'counts':counts(functions),'functions':functions,'chunks':chunks}
    method_identity=method();index['generation']=generation(index,method_identity);code_keys=validate_index(index)
    stage=compact._new_stage(output)
    compact.exporter.durable(stage/'index.js',(INDEX_PREFIX+json_data(index)+';\n').encode('utf-8'))
    compact.exporter.durable(stage/'reader.js',SCRIPT.encode('utf-8'))
    compact.exporter.durable(stage/'index.html',page(index).encode('utf-8'))
    for chunk,group in zip(chunks,groups):
        payload=chunk_payload(chunk['id'],group,index['generation']);validate_chunk(payload,index,chunk,code_keys)
        path=stage/chunk['path'];path.parent.mkdir(exist_ok=True)
        compact.exporter.durable(path,(CHUNK_PREFIX+json_data(payload)+');\n').encode('utf-8'))
    outputs=[compact.descriptor(path,name) for name,path in sorted(compact.regular_files(stage).items()) if name!='.incomplete.json']
    manifest={'schema':1,'format':FORMAT,'status':'complete','generation':index['generation'],'identity':index['identity'],
              'counts':index['counts'],'method':method_identity,'outputs':outputs,'source_archive':str(archive),
              'limits':BOUNDS,'limitations':['Exact compact mirror adds no decompilation coverage. Pseudocode is not original or guaranteed compilable source.',
                  'Node DOM fixtures test reader logic, not visual rendering/accessibility in a real browser.',
                  'Two code chunks are cached; metadata and one in-flight chunk remain resident. Oversized single code records are explicit exceptions.',
                  'Projection parses one referenced evidence envelope at a time; this bounds envelope count, not envelope bytes.',
                  'No hostile script isolation or power-loss publication durability is claimed.']}
    compact.write_json(stage/'manifest.json',manifest);check(stage,archive=archive,_allow_incomplete=True)
    if interrupt_before_publish:raise InterruptedError('Test interruption: unpublished reader stage retained')
    compact._publish(stage,output)
    return {'root':str(output),'generation':index['generation'],'counts':index['counts'],'manifest_sha256':compact.exporter.file_sha(output/'manifest.json')}


def project(artifacts,corpus,href):
    roots=[artifacts/name for name in ('native-compact-view-v2','native-compact-view-v1')]
    root=next((path for path in roots if path.exists() or path.is_symlink()),roots[-1]);archive=artifacts/'native-compact-mirror-v1'
    if not root.exists() and not root.is_symlink():return None,[]
    try:
        run=compact.read_json(compact.safe_path(corpus/'run.json',kind='file'))
        report=check(root,archive=archive,expected_target=run['target_sha256'],expected_profile=run['analysis_profile'],
                     expected_inventory=compact.exporter.file_sha(corpus/'inventory/v1.json'))
        return {'state':'verified','counts':report['counts'],'generation':report['generation'],'identity':report['identity'],
                'url':href(root/'index.html'),'manifest_url':href(root/'manifest.json')},[corpus/'run.json',corpus/'inventory/v1.json',*report['inputs']]
    except (IntegrityError,OSError,KeyError,TypeError,ValueError) as cause:
        return {'state':'invalid','error':str(cause)},[]


def page(index):
    # Only fixed markup and generator-created identity values occur in HTML.
    token=html.escape(index['generation'],quote=True);n=index['counts']
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Native pseudocode reader</title>
<style>body{{font:16px/1.5 system-ui;margin:0;background:#edf3f6;color:#182d3b}}main{{max-width:1240px;margin:auto;padding:24px}}section{{background:white;border:1px solid #c9d6df;border-radius:8px;padding:18px;margin:20px 0}}a{{color:#075d85}}input,select,button{{font:inherit;padding:8px;border:1px solid #7a909d;background:white;border-radius:4px;max-width:100%}}button{{cursor:pointer}}:focus-visible{{outline:3px solid #ad6100;outline-offset:2px}}table{{border-collapse:collapse;width:100%}}td,th{{padding:9px;border-bottom:1px solid #c9d6df;text-align:left;vertical-align:top;overflow-wrap:anywhere}}.table{{overflow:auto}}#reader{{min-height:100vh}}.controls{{display:flex;gap:12px;flex-wrap:wrap;align-items:end}}label{{display:block}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;tab-size:4;font:13px/1.5 ui-monospace,monospace}}code{{overflow-wrap:anywhere}}[hidden]{{display:none!important}}.notice{{background:#fff6e2;padding:10px;border-left:4px solid #956009}}small{{color:#425c6c}}</style></head>
<body><main><h1>Read the retained native pseudocode</h1><p>This exact compact mirror adds no decompilation coverage. Search {n['addresses']:,} committed addresses and {n['revisions']:,} revisions; pending addresses without an attempt are outside this reader. Pseudocode approximates compiled behavior and is not original or guaranteed compilable source.</p>
<p>Local offline snapshot. Code loads only when selected. At most 100 addresses per page; 100 revisions and 512 KiB of data per code chunk. A larger single revision is identified without truncation. Two chunks are cached; oversized records can exceed this bound.</p><p>Revision provenance preserves its original evidence/workflow profile and identifies the effective native profile used for corpus comparison.</p><p><a href="manifest.json">Viewer manifest and source identity</a></p><noscript><p>Enable JavaScript to read code here. The manifest identifies the original ZIP archive, whose function members preserve exact code and metadata.</p></noscript>
<section aria-labelledby="browse-title"><h2 id="browse-title">Find a function</h2><div class="controls"><div><label for="code-search">Address, alias or state</label><input id="code-search" type="search"></div><div><label for="code-state">Revision or aggregate state</label><select id="code-state"><option value="">All states</option></select></div></div><p id="code-count" role="status" aria-live="polite"></p><button id="code-prev" type="button">Previous 100</button> <button id="code-next" type="button">Next 100</button><div class="table"><table><thead><tr><th>Address</th><th>Aliases</th><th>Aggregate state</th><th>Revisions</th><th>Open</th></tr></thead><tbody id="code-rows"></tbody></table></div></section>
<section id="reader" aria-labelledby="code-title"><h2 id="code-title" tabindex="-1">Select a function</h2><p><a href="#browse-title">Back to function list</a></p><label for="code-revision">Exact revision</label><select id="code-revision" disabled></select><p id="code-load-status" role="status" aria-live="polite"></p><button id="code-retry" type="button" hidden>Retry code load</button> <a id="code-download" hidden>Download exact original UTF-8 code</a><p id="code-warning" class="notice" hidden></p><pre id="code-text" tabindex="0" aria-label="Pseudocode text"></pre><details><summary>Revision provenance and archive locations</summary><pre id="code-provenance"></pre></details></section>
</main><script>window.compactGeneration="{token}";</script><script src="index.js"></script><script src="reader.js"></script></body></html>'''


SCRIPT=r"""
(() => {
  'use strict';
  const byId=id=>document.getElementById(id);
  const search=byId('code-search'),filter=byId('code-state'),body=byId('code-rows'),count=byId('code-count');
  const title=byId('code-title'),revisionControl=byId('code-revision'),status=byId('code-load-status');
  const retry=byId('code-retry'),download=byId('code-download'),warning=byId('code-warning');
  const provenance=byId('code-provenance'),text=byId('code-text');
  const object=value=>value!==null && typeof value==='object' && !Array.isArray(value);
  const exact=(value,keys)=>object(value) && Object.keys(value).sort().join('|')===keys.slice().sort().join('|');
  function sameJson(a,b){
    if(a===b)return true;
    if(Array.isArray(a)||Array.isArray(b))return Array.isArray(a)&&Array.isArray(b)&&a.length===b.length&&Array.from(a).every((v,i)=>sameJson(v,b[i]));
    if(!object(a)||!object(b))return false;
    const keys=Object.keys(a);return keys.length===Object.keys(b).length&&keys.every(key=>Object.hasOwn(b,key)&&sameJson(a[key],b[key]));
  }
  const integer=value=>Number.isSafeInteger(value)&&value>=0;
  const strings=value=>Array.isArray(value)&&Array.from(value).every(v=>typeof v==='string');
  const digest=value=>typeof value==='string'&&/^[0-9a-f]{64}$/.test(value);
  const revisionId=value=>typeof value==='string'&&/^ev_[0-9a-f]{64}-[0-9]+$/.test(value);
  const evidenceId=value=>typeof value==='string'&&/^ev_[0-9a-f]{64}$/.test(value);
  const safeAddress=value=>typeof value==='string'&&/^(?:(?:[A-Za-z0-9._~-]|%[0-9A-F]{2})+:)?0x(?:0|[1-9a-f][0-9a-f]*)$/.test(value);
  const utf8=value=>new TextEncoder().encode(value);
  const jsonData=value=>JSON.stringify(value).replace(/</g,'\\u003c').replace(/>/g,'\\u003e').replace(/&/g,'\\u0026').replace(/\u2028/g,'\\u2028').replace(/\u2029/g,'\\u2029');
  const fail=message=>{throw new Error(message);};
  // Mirrors export_native_corpus.native_profile: only a record's exact provider
  // selects workflow unwrapping. Keep the original profile alongside this result.
  function nativeProfile(profile,provider){
    if(!object(profile)||!object(provider))fail('Malformed native/workflow profile');
    if(provider.id==='rea-workflow'){
      if(!object(profile.parameters))fail('Missing workflow profile parameters');
      profile=profile.parameters.upstream_analysis_profile;
    }
    if(!object(profile)||!digest(profile.digest))fail('Missing native profile identity');
    return profile;
  }
  // Synchronous SHA-256 over UTF-8 bytes also works under file URLs. No WebCrypto
  // availability assumption. Chunk validation is corruption detection, not a
  // sandbox against executing untrusted JavaScript.
  const K=new Uint32Array([0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]);
  const rotate=(x,n)=>(x>>>n)|(x<<(32-n));
  function sha256(bytes) {
    const size=Math.ceil((bytes.length+9)/64)*64,data=new Uint8Array(size);data.set(bytes);data[bytes.length]=0x80;
    const view=new DataView(data.buffer),bitLength=bytes.length*8;
    view.setUint32(size-8,Math.floor(bitLength/4294967296));view.setUint32(size-4,bitLength>>>0);
    const hash=new Uint32Array([0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]),w=new Uint32Array(64);
    for(let offset=0;offset<size;offset+=64){
      for(let i=0;i<16;i++)w[i]=view.getUint32(offset+i*4);
      for(let i=16;i<64;i++){const a=w[i-15],b=w[i-2];w[i]=(w[i-16]+(rotate(a,7)^rotate(a,18)^(a>>>3))+w[i-7]+(rotate(b,17)^rotate(b,19)^(b>>>10)))>>>0;}
      let [a,b,c,d,e,f,g,h]=hash;
      for(let i=0;i<64;i++){
        const t1=(h+(rotate(e,6)^rotate(e,11)^rotate(e,25))+((e&f)^(~e&g))+K[i]+w[i])>>>0;
        const t2=((rotate(a,2)^rotate(a,13)^rotate(a,22))+((a&b)^(a&c)^(b&c)))>>>0;
        h=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0;
      }
      [a,b,c,d,e,f,g,h].forEach((v,i)=>hash[i]=(hash[i]+v)>>>0);
    }
    return Array.from(hash,v=>v.toString(16).padStart(8,'0')).join('');
  }
  const index=window.compactIndex,codeMap=new Map(),cache=new Map();
  let selected=null,pending=null,attempt=0,objectUrl=null,matches=[],page=0,searchable=[];
  function clearDownload(){if(objectUrl!==null){URL.revokeObjectURL(objectUrl);objectUrl=null;}download.hidden=true;download.removeAttribute?.('href');}
  function cancelPending(){if(pending!==null){pending.script.remove();pending=null;}}
  function locator(value,member,code){
    if(!exact(value,code?['archive','member','bytes','sha256','chunk']:['archive','member','bytes','sha256']) || value.member!==member || typeof value.archive!=='string' || !/^archives\/functions-[0-9]{6}\.zip$/.test(value.archive) || !integer(value.bytes) || !digest(value.sha256) || code&&!integer(value.chunk))fail('Malformed ZIP locator');
  }
  function validateIndex(){
    if(!exact(index,['schema','generation','identity','bounds','counts','functions','chunks']) || index.schema!=='compact-native-index-v1' || !digest(index.generation) || index.generation!==window.compactGeneration || !exact(index.bounds,['page_rows','chunk_revisions','chunk_data_bytes','cached_chunks']) || index.bounds.page_rows!==100 || index.bounds.chunk_revisions!==100 || index.bounds.chunk_data_bytes!==524288 || index.bounds.cached_chunks!==2 || !Array.isArray(index.functions) || !Array.isArray(index.chunks))fail('Malformed or stale reader index');
    if(!exact(index.identity,['target_sha256','architecture','analysis_profile','inventory_evidence_id','inventory_sha256','coverage_sha256','archive_manifest_sha256','archive_catalog_sha256']) || !['target_sha256','inventory_sha256','coverage_sha256','archive_manifest_sha256','archive_catalog_sha256'].every(k=>digest(index.identity[k])) || typeof index.identity.architecture!=='string' || !evidenceId(index.identity.inventory_evidence_id) || !object(index.identity.analysis_profile))fail('Malformed reader identity');
    nativeProfile(index.identity.analysis_profile,{});
    const seen=new Set(),states=new Set(),totals={addresses:0,revisions:0,code_revisions:0,failed_revisions:0,partial_revisions:0};
    for(const fn of Array.from(index.functions)){
      if(!exact(fn,['address','aliases','classification','state','revisions']) || !safeAddress(fn.address) || seen.has(fn.address) || !strings(fn.aliases) || !['eligible','external','unclassified'].includes(fn.classification) || !['pending','external','unclassified','exported','exported-with-warnings','failed'].includes(fn.state) || !Array.isArray(fn.revisions) || !fn.revisions.length)fail('Malformed function row');
      seen.add(fn.address);totals.addresses++;states.add(fn.state);const revisions=new Set();
      for(const row of Array.from(fn.revisions)){
        if(!exact(row,['revision','state','partial_pseudocode','warnings','evidence_id','source_sha256','source_record_index','source_item_index','error','limitations','details','analysis_profile','evidence_provider','effective_analysis_profile','metadata','manifest','code']) || !revisionId(row.revision) || revisions.has(row.revision) || !['exported','exported-with-warnings','failed'].includes(row.state) || typeof row.partial_pseudocode!=='boolean' || !strings(row.warnings) || !strings(row.limitations) || !evidenceId(row.evidence_id) || !digest(row.source_sha256) || !integer(row.source_record_index) || !integer(row.source_item_index) || !object(row.analysis_profile) || !object(row.effective_analysis_profile) || !sameJson(nativeProfile(row.analysis_profile,row.evidence_provider),row.effective_analysis_profile) || !sameJson(row.effective_analysis_profile,index.identity.analysis_profile))fail('Malformed revision row');
        revisions.add(row.revision);states.add(row.state);totals.revisions++;if(row.state==='failed')totals.failed_revisions++;if(row.partial_pseudocode)totals.partial_revisions++;
        const prefix='functions/'+fn.address+'/'+row.revision+'/';locator(row.metadata,prefix+'metadata.json',false);locator(row.manifest,prefix+'manifest.json',false);
        if(row.code!==null){locator(row.code,prefix+'pseudocode.c',true);codeMap.set(fn.address+'|'+row.revision,row.code);totals.code_revisions++;}
        if(row.partial_pseudocode&&(row.state!=='failed'||row.code===null) || row.state!=='failed'&&row.code===null)fail('Invalid partial/success label');
      }
    }
    if(!exact(index.counts,Object.keys(totals)) || !Object.keys(totals).every(k=>integer(index.counts[k])&&index.counts[k]===totals[k]))fail('Reader counts disagree');
    const assigned=new Set();
    for(const [number,chunk] of Array.from(index.chunks).entries()){
      if(!exact(chunk,['id','path','keys','oversized','data_bytes','records_sha256']) || chunk.id!==number || chunk.path!=='chunks/code-'+String(number).padStart(6,'0')+'.js' || !strings(chunk.keys) || !chunk.keys.length || chunk.keys.length>100 || typeof chunk.oversized!=='boolean' || !integer(chunk.data_bytes) || !digest(chunk.records_sha256) || chunk.oversized!==(chunk.data_bytes>524288) || chunk.oversized&&chunk.keys.length!==1)fail('Malformed chunk index');
      for(const key of chunk.keys){if(!codeMap.has(key)||assigned.has(key)||codeMap.get(key).chunk!==number)fail('Duplicate or unassigned code');assigned.add(key);}
    }
    if(assigned.size!==codeMap.size)fail('Missing code chunk');
    return states;
  }
  function validateChunk(payload,chunk){
    if(!exact(payload,['schema','generation','id','records']) || payload.schema!=='compact-native-code-v1' || payload.generation!==index.generation || payload.id!==chunk.id || !Array.isArray(payload.records) || payload.records.length!==chunk.keys.length)fail('Malformed or stale code chunk');
    const records=new Map();
    for(const [i,row] of Array.from(payload.records).entries()){
      if(!exact(row,['key','code']) || row.key!==chunk.keys[i] || typeof row.code!=='string')fail('Malformed code record');
      const descriptor=codeMap.get(row.key),bytes=utf8(row.code);
      if(bytes.length!==descriptor.bytes || sha256(bytes)!==descriptor.sha256)fail('Code bytes differ from original hash');
      records.set(row.key,row.code);
    }
    if(utf8(jsonData(payload)).length!==chunk.data_bytes || sha256(utf8(jsonData(payload.records)))!==chunk.records_sha256)fail('Chunk payload differs from frozen generation');
    return records;
  }
  function show(code){
    clearDownload();text.textContent=code;
    const bytes=utf8(code);objectUrl=URL.createObjectURL(new Blob([bytes],{type:'text/plain;charset=utf-8'}));
    download.href=objectUrl;download.download=selected.fn.address.replace(/[^A-Za-z0-9_.-]/g,'_')+'-'+selected.row.revision+'.c';download.hidden=false;
    status.textContent='Exact original UTF-8 code loaded ('+bytes.length.toLocaleString('en-US')+' bytes).';retry.hidden=true;
  }
  function loadFailure(message){if(selected&&selected.row.code){status.textContent='Code load failed: '+message+'. Navigation remains available; retry or choose another revision.';retry.hidden=false;}}
  window.receiveCompactChunk=payload=>{
    if(pending===null || document.currentScript!==pending.script)return;
    pending.seen++;pending.payload=payload;
  };
  function loadSelected(){
    if(!selected||!selected.row.code)return;
    const id=selected.row.code.chunk;
    if(cache.has(id)){cancelPending();const records=cache.get(id);cache.delete(id);cache.set(id,records);try{show(records.get(selected.key));}catch(error){loadFailure(error.message);}return;}
    status.textContent='Loading exact code chunk '+id+'…';retry.hidden=true;
    if(pending!==null&&pending.id===id)return;
    cancelPending();const chunk=index.chunks[id],script=document.createElement('script');
    const request={id,script,payload:null,seen:0};pending=request;script.src=chunk.path+'?generation='+index.generation+'&attempt='+(++attempt);
    script.onload=()=>{
      if(pending!==request)return;
      pending=null;script.remove();
      try{
        if(request.seen!==1)fail('Missing or duplicate chunk callback');
        const records=validateChunk(request.payload,chunk); // Entire schema/hash validates before cache or visible mutation.
        cache.delete(id);cache.set(id,records);while(cache.size>2)cache.delete(cache.keys().next().value);
        if(selected&&selected.row.code&&selected.row.code.chunk===id)show(records.get(selected.key));
      }catch(error){loadFailure(error.message);}
    };
    script.onerror=()=>{if(pending!==request)return;pending=null;script.remove();loadFailure('Local script could not be read');};
    document.head.append(script);
  }
  function selectRevision(){
    const row=selected&&selected.fn.revisions.find(r=>r.revision===revisionControl.value);
    text.textContent='';clearDownload();retry.hidden=true;warning.hidden=true;
    if(!row){cancelPending();if(selected)selected.row=null;status.textContent='Choose an exact revision before loading code.';provenance.textContent='';return;}
    selected={fn:selected.fn,row,key:selected.fn.address+'|'+row.revision};
    provenance.textContent=JSON.stringify({identity:index.identity,address:selected.fn.address,revision:row.revision,state:row.state,evidence_provider:row.evidence_provider,analysis_profile:row.analysis_profile,effective_analysis_profile:row.effective_analysis_profile,evidence_id:row.evidence_id,source_member:'evidence/'+row.source_sha256+'.json',source_sha256:row.source_sha256,source_record_index:row.source_record_index,source_item_index:row.source_item_index,metadata:row.metadata,manifest:row.manifest,code:row.code,error:row.error,limitations:row.limitations,details:row.details},null,2);
    const warnings=[];
    if(row.state==='failed')warnings.push(row.partial_pseudocode?'Failed revision: partial pseudocode. This output is incomplete.':'Failed revision: no successful code output.');
    warnings.push(...row.warnings);
    if(row.code!==null&&index.chunks[row.code.chunk].oversized)warnings.push('Oversized single revision: retained without truncation; this chunk exceeds 512 KiB.');
    warning.textContent=warnings.join('\n');warning.hidden=!warnings.length;
    if(row.code===null){cancelPending();status.textContent='No code payload was retained for this revision.';return;}
    loadSelected();
  }
  function selectFunction(fn){
    cancelPending();selected={fn,row:null,key:null};title.textContent=fn.address+' · '+(fn.aliases.join(', ')||'(unnamed)');revisionControl.replaceChildren();revisionControl.disabled=false;
    const placeholder=document.createElement('option');placeholder.value='';placeholder.textContent='Choose an exact revision';revisionControl.append(placeholder);
    for(const row of fn.revisions){const option=document.createElement('option');option.value=row.revision;option.textContent=row.revision+' · '+row.state+(row.partial_pseudocode?' · partial':'');revisionControl.append(option);}
    revisionControl.value=fn.revisions.length===1?fn.revisions[0].revision:'';selectRevision();
    title.focus({preventScroll:true});title.scrollIntoView({block:'start'});
  }
  function render(){
    body.replaceChildren();
    for(const n of matches.slice(page*100,(page+1)*100)){
      const fn=index.functions[n],tr=document.createElement('tr');
      for(const value of [fn.address,fn.aliases.join('\n')||'(unnamed)',fn.state,String(fn.revisions.length)]){const td=document.createElement('td');td.textContent=value;tr.append(td);}
      const td=document.createElement('td'),button=document.createElement('button');button.type='button';button.textContent='Read revisions';button.addEventListener('click',()=>selectFunction(fn));td.append(button);tr.append(td);body.append(tr);
    }
    const pages=Math.ceil(matches.length/100);count.textContent=matches.length.toLocaleString('en-US')+' of '+index.functions.length.toLocaleString('en-US')+' archived addresses · page '+(pages?page+1:0)+' of '+pages;
    byId('code-prev').disabled=page===0;byId('code-next').disabled=page+1>=pages;
  }
  function apply(){const terms=search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);matches=[];index.functions.forEach((fn,i)=>{if(terms.every(t=>searchable[i].includes(t))&&(!filter.value||fn.state===filter.value||fn.revisions.some(r=>r.state===filter.value)))matches.push(i);});page=0;render();}
  try{
    const states=validateIndex();searchable=index.functions.map(fn=>[fn.address,...fn.aliases,fn.state,...fn.revisions.map(r=>r.state)].join(' ').toLowerCase());
    for(const state of [...states].sort()){const option=document.createElement('option');option.value=state;option.textContent=state;filter.append(option);}
    search.addEventListener('input',apply);filter.addEventListener('input',apply);
    byId('code-prev').addEventListener('click',()=>{if(page>0){page--;render();}});byId('code-next').addEventListener('click',()=>{if((page+1)*100<matches.length){page++;render();}});
    revisionControl.addEventListener('change',selectRevision);retry.addEventListener('click',loadSelected);apply();
  }catch(error){cancelPending();clearDownload();count.textContent='Reader index validation failed: '+error.message+'. Refresh a complete matching viewer snapshot.';status.textContent='Code is unavailable for this invalid snapshot.';}
})();

"""


def main():
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='command',required=True)
    build_args=commands.add_parser('build');build_args.add_argument('--archive',type=Path,required=True);build_args.add_argument('--output',type=Path,required=True)
    check_args=commands.add_parser('check');check_args.add_argument('--root',type=Path,required=True);check_args.add_argument('--archive',type=Path)
    args=parser.parse_args()
    try:
        report=build(args.archive,args.output) if args.command=='build' else check(args.root,archive=args.archive)
        report={k:v for k,v in report.items() if k!='inputs'}
    except (IntegrityError,OSError,ValueError) as cause:parser.exit(1,f'compact viewer error: {cause}\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
