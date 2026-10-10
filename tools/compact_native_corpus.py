#!/usr/bin/env python3
"""Create and verify exact compact mirrors of the analyst native export corpus.

This tool never invokes an analyzer, deletes source files, or adds coverage.
It uses the exporter authority under its existing writer lock. Validation there
loads the inventory and a bounded cache of evidence envelopes; ZIP copying and
hash checking here stream files in 1 MiB blocks. Source and compact allocation
are measured separately from logical bytes. Path checks cover ordinary local
use, not a hostile process concurrently replacing checked paths.
"""
import argparse
from collections import Counter
from contextlib import contextmanager
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
import zipfile
from functools import wraps

_spec=importlib.util.spec_from_file_location('compact_export_authority',Path(__file__).with_name('export_native_corpus.py'))
exporter=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(exporter)
IntegrityError=exporter.IntegrityError
FORMAT='native-corpus-zip-v1'
REVISION=re.compile(r'ev_[0-9a-f]{64}-[0-9]+')
DIGEST=re.compile(r'[0-9a-f]{64}')
BLOCK=1024*1024
MAX_INDEX_BYTES=512*1024*1024
MAX_METADATA_BYTES=16*1024*1024
SOURCE_SHARD_FILES=64


def integrity_errors(function):
    @wraps(function)
    def guarded(*args,**kwargs):
        try:return function(*args,**kwargs)
        except IntegrityError:raise
        except InterruptedError:raise
        except (OSError,KeyError,TypeError,IndexError,ValueError,zipfile.BadZipFile) as cause:
            raise IntegrityError(f'Invalid or inaccessible compact corpus: {cause}') from cause
    return guarded


def canonical_path(path):
    """Return an absolute lexical path; never resolve away a symlink."""
    path=Path(path).expanduser()
    if '..' in path.parts:raise IntegrityError('Traversal in filesystem path')
    return path if path.is_absolute() else Path.cwd()/path


def safe_path(path, *, kind='directory', fresh=False):
    path=canonical_path(path)
    for ancestor in reversed([path,*path.parents]):
        if ancestor.is_symlink():raise IntegrityError(f'Symbolic link path: {ancestor}')
        if ancestor.exists():
            expected=kind if ancestor==path else 'directory'
            if not (ancestor.is_dir() if expected=='directory' else ancestor.is_file()):
                raise IntegrityError(f'Unexpected path type: {ancestor}')
    if fresh:
        if path.exists():raise IntegrityError(f'Destination already exists: {path}')
        if not path.parent.is_dir():raise IntegrityError('Destination parent must already exist')
    elif not path.exists():raise IntegrityError(f'Missing {kind}: {path}')
    return path


def regular_files(root):
    """Validate the entire tree without following symbolic links."""
    result={}
    def error(cause):raise cause
    for current,directories,files in os.walk(root,followlinks=False,onerror=error):
        for name in directories+files:
            path=Path(current)/name;mode=path.lstat().st_mode
            if stat.S_ISLNK(mode):raise IntegrityError(f'Symbolic link in tree: {path}')
            if name in files:
                if not stat.S_ISREG(mode):raise IntegrityError(f'Nonregular input: {path}')
                result[path.relative_to(root).as_posix()]=path
            elif not stat.S_ISDIR(mode):raise IntegrityError(f'Non-directory input: {path}')
    return result


def member_path(value):
    if not isinstance(value,str) or not value or '\\' in value or '\x00' in value:
        raise IntegrityError('Unsafe archive member name')
    path=PurePosixPath(value)
    if path.is_absolute() or any(p in ('.','..') for p in path.parts) or path.as_posix()!=value:
        raise IntegrityError('Noncanonical archive member name')
    return value


def original_path(value):
    member_path(value);parts=value.split('/')
    if value in ('run.json','inventory/v1.json','coverage.json'):return 'sources'
    if len(parts)==2 and parts[0]=='evidence' and re.fullmatch(r'[0-9a-f]{64}\.json',parts[1]):return 'sources'
    if (len(parts)==4 and parts[0]=='functions' and exporter.address(parts[1])==parts[1]
        and REVISION.fullmatch(parts[2]) and parts[3] in ('metadata.json','manifest.json','pseudocode.c')):
        return 'functions'
    raise IntegrityError(f'Unknown original member path: {value}')


def _unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise IntegrityError(f'Duplicate JSON key: {key}')
        result[key]=value
    return result


def json_value(stream):
    try:return json.load(stream,object_pairs_hook=_unique_object)
    except (ValueError,UnicodeError,TypeError) as cause:raise IntegrityError(f'Invalid JSON document: {cause}') from cause


def read_json(path,limit=MAX_INDEX_BYTES):
    if path.stat().st_size>limit:raise IntegrityError('JSON index exceeds supported size limit')
    with path.open('r',encoding='utf-8') as stream:return json_value(stream)


def descriptor(path,relative):
    info=path.stat()
    return {'path':relative,'bytes':info.st_size,'sha256':exporter.file_sha(path)}


def valid_descriptor(value):
    if (not isinstance(value,dict) or set(value)!={'path','bytes','sha256'}
        or type(value['bytes']) is not int or value['bytes']<0
        or not isinstance(value['sha256'],str) or not DIGEST.fullmatch(value['sha256'])):
        raise IntegrityError('Invalid file descriptor')
    member_path(value['path'])


def file_storage(paths):
    total={'files':0,'logical_bytes':0,'allocated_bytes':0}
    for path in paths:
        info=path.stat();total['files']+=1;total['logical_bytes']+=info.st_size;total['allocated_bytes']+=info.st_blocks*512
    return total


def revision_entry(metadata,archive,members):
    return {key:metadata[key] for key in ('revision','state','partial_pseudocode','warnings','evidence_id','source_sha256')} | {
        'archive':archive,'members':sorted(members)}


def coverage_summary(coverage):
    return {key:value for key,value in coverage.items() if key!='functions'}


def write_json(path,value):
    exporter.durable(path,exporter.encoded(value))


def write_zip(stage,root,name,relatives):
    path=stage/name;path.parent.mkdir(parents=True,exist_ok=True);members=[]
    with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
        for relative in relatives:
            original_path(relative);source=root/relative;info=zipfile.ZipInfo(relative,date_time=(1980,1,1,0,0,0))
            info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED
            digest=hashlib.sha256();size=0
            with source.open('rb') as incoming,archive.open(info,'w',force_zip64=True) as outgoing:
                for block in iter(lambda:incoming.read(BLOCK),b''):
                    outgoing.write(block);digest.update(block);size+=len(block)
            members.append({'path':relative,'bytes':size,'sha256':digest.hexdigest()})
    with path.open('rb') as stream:os.fsync(stream.fileno())
    return descriptor(path,name) | {'kind':original_path(relatives[0]),'members':members}


def _new_stage(output):
    stage=Path(tempfile.mkdtemp(prefix='.'+output.name+'.incomplete-',dir=output.parent))
    write_json(stage/'.incomplete.json',{'format':FORMAT,'destination':str(output),'status':'incomplete'})
    return stage


def _publish(stage,output):
    safe_path(output,fresh=True)
    # Keep the marker through rename. Failed rename leaves explicit staging;
    # interruption after rename leaves an explicitly incomplete destination.
    # Readers accept neither until this final marker removal succeeds.
    os.rename(stage,output)
    fd=os.open(output.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
    fd=os.open(output,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
    # Marker removal is the explicit final commit. No further filesystem commit
    # operation runs after it. Power-loss durability of that removal is untested;
    # an asynchronous signal after success is a committed-result ambiguity.
    (output/'.incomplete.json').unlink()


class ArchiveCorpusReader:
    """Expose verified ZIP members to the exporter's complete read-only authority.

    No extracted corpus or source-envelope cache lives here. The shared exporter
    loads its inventory and retains at most eight parsed source envelopes by
    count, not by bytes. Individual source envelopes can therefore be large.
    """
    def __init__(self,root,index,revision_groups):
        self.root=root;self.index=index;self.revision_groups=revision_groups
    def relative(self,path):
        try:return path.relative_to(self.root).as_posix()
        except ValueError as cause:raise IntegrityError('Authority read outside archive') from cause
    @contextmanager
    def member(self,path):
        relative=self.relative(path)
        if relative not in self.index:raise FileNotFoundError(f'Missing archived authority member: {relative}')
        archive,_=self.index[relative]
        with zipfile.ZipFile(self.root/archive) as bundle,bundle.open(relative) as stream:yield stream
    def read_bytes(self,path):
        with self.member(path) as stream:return stream.read()
    def file_sha(self,path):
        digest=hashlib.sha256()
        with self.member(path) as stream:
            for block in iter(lambda:stream.read(BLOCK),b''):digest.update(block)
        return digest.hexdigest()
    def revision_files(self,path):
        relative=self.relative(path);parts=relative.split('/')
        if len(parts)!=3 or parts[0]!='functions':raise IntegrityError('Invalid virtual revision directory')
        members=self.revision_groups.get((parts[1],parts[2]))
        if members is None:raise IntegrityError('Missing virtual revision directory')
        return {member.rsplit('/',1)[1] for member in members}
    def committed_directories(self,functions):
        result={}
        for entry,revision in self.revision_groups:
            if exporter.address(entry)!=entry or entry not in functions or not REVISION.fullmatch(revision):
                raise IntegrityError('Unknown/noncanonical archived revision')
            result.setdefault(entry,[]).append(self.root/'functions'/entry/revision)
        return result


@integrity_errors
def build(corpus,output,shard_size=250,*,interrupt_before_publish=False):
    corpus=safe_path(corpus);output=safe_path(output,fresh=True)
    if type(shard_size) is not int or not 1<=shard_size<=10000:raise IntegrityError('Shard size must be an integer from 1 to 10000 revisions')
    if output.is_relative_to(corpus):raise IntegrityError('Compact destination must be outside the source corpus')
    files=regular_files(corpus)
    if '.ingest.lock' not in files:raise IntegrityError('Source must have its existing exporter writer lock')
    with exporter.locked(corpus):
        # Re-scan after lock acquisition before authority reads or any output.
        files=regular_files(corpus);coverage=exporter.coverage(corpus,persist=False)
        if exporter.file_sha(corpus/'coverage.json')!=exporter.sha(exporter.encoded(coverage)):
            raise IntegrityError('Source coverage checkpoint is stale or noncanonical; no repair was attempted')
        run=read_json(corpus/'run.json');identity={'run':run,'run_sha256':exporter.file_sha(corpus/'run.json'),
            'inventory_sha256':exporter.file_sha(corpus/'inventory/v1.json'),'coverage_sha256':exporter.file_sha(corpus/'coverage.json')}
        source_paths=['run.json','inventory/v1.json','coverage.json']
        for relative in sorted(files):
            if relative.startswith('evidence/'):
                if original_path(relative)!='sources':raise IntegrityError('Unexpected evidence file')
                if exporter.file_sha(files[relative])!=Path(relative).stem:raise IntegrityError('Evidence filename/content hash mismatch')
                source_paths.append(relative)
        revisions=[];rows=[]
        for row in coverage['functions']:
            if not row['revisions']:continue
            entry={key:row[key] for key in ('address','aliases','classification','state')};entry['revisions']=[];rows.append(entry)
            for revision in row['revisions']:
                directory=corpus/'functions'/row['address']/revision
                names=sorted(path.name for path in directory.iterdir())
                members=[f"functions/{row['address']}/{revision}/{name}" for name in names]
                metadata=read_json(directory/'metadata.json',MAX_METADATA_BYTES)
                revisions.append((entry,metadata,members))
        stage=_new_stage(output)
        archives=[]
        for offset in range(0,len(source_paths),SOURCE_SHARD_FILES):
            name=f'archives/sources-{offset//SOURCE_SHARD_FILES+1:06d}.zip'
            archives.append(write_zip(stage,corpus,name,source_paths[offset:offset+SOURCE_SHARD_FILES]))
        for offset in range(0,len(revisions),shard_size):
            group=revisions[offset:offset+shard_size];name=f'archives/functions-{offset//shard_size+1:06d}.zip'
            archives.append(write_zip(stage,corpus,name,[member for _,_,members in group for member in members]))
            for entry,metadata,members in group:entry['revisions'].append(revision_entry(metadata,name,members))
        summary=coverage_summary(coverage)
        catalog={'schema':1,'format':FORMAT,'source_identity':identity,'coverage':summary,'functions':rows}
        write_json(stage/'catalog.json',catalog)
        archived=[corpus/member['path'] for archive in archives for member in archive['members']]
        manifest={'schema':1,'format':FORMAT,'status':'complete','source_identity':identity,'coverage':summary,
            'catalog':descriptor(stage/'catalog.json','catalog.json'),'archives':archives,'shard_size':shard_size,
            'source_storage':file_storage(archived),
            'method':{'tool_sha256':exporter.file_sha(Path(__file__)),
                      'export_authority_sha256':exporter.file_sha(Path(exporter.__file__))},
            'limitations':['Compact mirror preserves prior evidence bytes and coverage; it adds no decompilation or behavioral proof.',
                           'Allocated bytes count regular files only; directory blocks and filesystem metadata are excluded.']}
        write_json(stage/'manifest.json',manifest)
        # The archive authority reconstructs coverage itself; avoid retaining
        # the first full inventory-sized coverage list during that second pass.
        del coverage
        check(stage,_allow_incomplete=True)
        if interrupt_before_publish:raise InterruptedError('Test interruption: verified unpublished staging retained')
        _publish(stage,output)
    return {'root':str(output),'coverage':summary,'storage':{'source':manifest['source_storage'],
        'compact':file_storage(regular_files(output).values())},'manifest_sha256':exporter.file_sha(output/'manifest.json')}


def _read_member_json(root,index,path,limit=MAX_METADATA_BYTES):
    archive,entry=index[path]
    if entry['bytes']>limit:raise IntegrityError('JSON member exceeds supported size limit')
    with zipfile.ZipFile(root/archive) as bundle,bundle.open(path) as raw,io.TextIOWrapper(raw,encoding='utf-8') as stream:
        return json_value(stream)


def _verify_zip(root,archive,index):
    expected={member['path']:member for member in archive['members']}
    try:
        with zipfile.ZipFile(root/archive['path']) as bundle:
            infos=bundle.infolist();names=[info.filename for info in infos]
            if len(names)!=len(set(names)) or set(names)!=set(expected):raise IntegrityError('ZIP has duplicate/unlisted/missing members')
            for info in infos:
                original_path(info.filename)
                if (info.create_system!=3 or not stat.S_ISREG(info.external_attr>>16) or info.is_dir()
                    or info.flag_bits&1 or info.compress_type not in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED)):
                    raise IntegrityError('ZIP member is not a supported regular file')
                entry=expected[info.filename]
                if info.file_size!=entry['bytes']:raise IntegrityError('ZIP member size mismatch')
                digest=hashlib.sha256();size=0
                with bundle.open(info) as stream:
                    for block in iter(lambda:stream.read(BLOCK),b''):
                        size+=len(block);digest.update(block)
                        if size>entry['bytes']:raise IntegrityError('ZIP member exceeds pinned size')
                if size!=entry['bytes'] or digest.hexdigest()!=entry['sha256']:raise IntegrityError('ZIP member content mismatch')
                index[info.filename]=(archive['path'],entry)
    except (zipfile.BadZipFile,RuntimeError,EOFError,OSError) as cause:raise IntegrityError(f'Invalid ZIP archive: {cause}') from cause


@integrity_errors
def check(root,*,_allow_incomplete=False):
    root=safe_path(root);files=regular_files(root)
    if not _allow_incomplete and '.incomplete.json' in files:raise IntegrityError('Unpublished incomplete archive')
    try:manifest=read_json(root/'manifest.json');catalog_descriptor=manifest['catalog'];archives=manifest['archives']
    except (FileNotFoundError,KeyError,TypeError) as cause:raise IntegrityError('Missing/invalid compact manifest') from cause
    if manifest.get('schema')!=1 or manifest.get('format')!=FORMAT or manifest.get('status')!='complete':raise IntegrityError('Unsupported/incomplete manifest')
    valid_descriptor(catalog_descriptor)
    if catalog_descriptor['path']!='catalog.json' or not isinstance(archives,list):raise IntegrityError('Invalid catalog/archive layout')
    if type(manifest.get('shard_size')) is not int or not 1<=manifest['shard_size']<=10000:raise IntegrityError('Invalid revision shard bound')
    if (set(manifest['method'])!={'tool_sha256','export_authority_sha256'} or
        any(not DIGEST.fullmatch(value) for value in manifest['method'].values())):raise IntegrityError('Invalid method identity')
    expected_files={'manifest.json','catalog.json'};members=set();folded_members=set();index={};revision_groups={}
    for archive in archives:
        if not isinstance(archive,dict) or set(archive)!={'path','bytes','sha256','kind','members'}:raise IntegrityError('Invalid archive descriptor')
        valid_descriptor({key:archive[key] for key in ('path','bytes','sha256')})
        if not re.fullmatch(r'archives/(sources|functions)-[0-9]{6}\.zip',archive['path']):raise IntegrityError('Unsafe archive path')
        if archive['path'] in expected_files or archive['kind'] not in ('sources','functions') or not archive['members']:raise IntegrityError('Duplicate/invalid archive')
        if not archive['path'].startswith('archives/'+archive['kind']+'-'):raise IntegrityError('Archive name/kind mismatch')
        expected_files.add(archive['path'])
        archive_revisions=set()
        for member in archive['members']:
            valid_descriptor(member)
            if original_path(member['path'])!=archive['kind'] or member['path'].casefold() in folded_members:raise IntegrityError('Duplicate/misclassified original member')
            if member['path'] in ('inventory/v1.json','coverage.json') and member['bytes']>MAX_INDEX_BYTES:
                raise IntegrityError('Authority index exceeds supported size limit')
            if (member['path']=='run.json' or member['path'].startswith('functions/') and member['path'].endswith(('/metadata.json','/manifest.json'))) and member['bytes']>MAX_METADATA_BYTES:
                raise IntegrityError('Authority metadata exceeds supported size limit')
            members.add(member['path'])
            folded_members.add(member['path'].casefold())
            if archive['kind']=='functions':
                parts=member['path'].split('/');key=(parts[1],parts[2]);archive_revisions.add(key)
                revision_groups.setdefault(key,[]).append(member['path'])
        if archive['kind']=='functions' and len(archive_revisions)>manifest['shard_size']:raise IntegrityError('Function archive exceeds revision shard bound')
        if archive['kind']=='sources' and len(archive['members'])>SOURCE_SHARD_FILES:raise IntegrityError('Source archive exceeds member bound')
    if _allow_incomplete:expected_files.add('.incomplete.json')
    if set(files)!=expected_files:raise IntegrityError('Compact file set differs from manifest')
    for entry in [catalog_descriptor,*archives]:
        path=files[entry['path']]
        if path.stat().st_size!=entry['bytes'] or exporter.file_sha(path)!=entry['sha256']:raise IntegrityError('Archive/catalog byte hash mismatch')
    for archive in archives:_verify_zip(root,archive,index)
    storage=manifest['source_storage']
    if (set(storage)!={'files','logical_bytes','allocated_bytes'} or any(type(value) is not int or value<0 for value in storage.values())
        or storage['files']!=len(index) or storage['logical_bytes']!=sum(entry['bytes'] for _,entry in index.values())):
        raise IntegrityError('Source logical storage report disagrees with exact members')
    for required in ('run.json','inventory/v1.json','coverage.json'):
        if required not in index:raise IntegrityError('Missing authoritative source member')
    identity=manifest['source_identity'];run=_read_member_json(root,index,'run.json')
    if (identity.get('run')!=run or identity.get('run_sha256')!=index['run.json'][1]['sha256']
        or identity.get('inventory_sha256')!=index['inventory/v1.json'][1]['sha256']
        or identity.get('coverage_sha256')!=index['coverage.json'][1]['sha256']):raise IntegrityError('Source identity does not match archived source bytes')
    inventory_source=f"evidence/{run['inventory_source_sha256']}.json"
    if inventory_source not in index or index[inventory_source][1]['sha256']!=run['inventory_source_sha256']:raise IntegrityError('Missing/corrupt inventory evidence source')
    for path,(_,entry) in index.items():
        if path.startswith('evidence/') and Path(path).stem!=entry['sha256']:raise IntegrityError('Source filename/content digest mismatch')
    catalog=read_json(root/'catalog.json')
    if (catalog.get('schema')!=1 or catalog.get('format')!=FORMAT or catalog.get('source_identity')!=identity
        or catalog.get('coverage')!=manifest['coverage'] or not isinstance(catalog.get('functions'),list)):
        raise IntegrityError('Catalog identity/coverage mismatch')
    # Hashes alone do not establish agreement with retained evidence. Run the
    # same inventory/profile/source/result/code authority used for loose files,
    # through ZIP reads, and require the exact canonical retained checkpoint.
    reader=ArchiveCorpusReader(root,index,revision_groups)
    coverage=exporter.coverage(root,persist=False,reader=reader)
    if exporter.sha(exporter.encoded(coverage))!=index['coverage.json'][1]['sha256']:
        raise IntegrityError('Archived coverage differs from source-authoritative reconstruction')
    if coverage_summary(coverage)!=manifest['coverage']:raise IntegrityError('Coverage summary differs from archived checkpoint')
    if coverage['target_sha256']!=run['target_sha256'] or coverage['inventory_evidence_id']!=run['inventory_evidence_id']:raise IntegrityError('Coverage identity mismatch')
    authority_rows={};all_addresses=set();counts=Counter()
    for row in coverage['functions']:
        entry=exporter.address(row['address'])
        if entry!=row['address'] or entry in all_addresses:raise IntegrityError('Noncanonical/duplicate coverage entry')
        all_addresses.add(entry);counts[row['state']]+=1
        if row['revisions']:authority_rows[entry]=row
    if dict(counts)!=coverage['counts'] or len(all_addresses)!=coverage['unique_functions']:raise IntegrityError('Coverage counts mismatch')
    seen=set();indexed_members=set()
    for row in catalog['functions']:
        entry=exporter.address(row['address'])
        if entry in seen or entry not in authority_rows:raise IntegrityError('Duplicate/unknown catalog function')
        seen.add(entry);source_row=authority_rows[entry]
        if any(row[key]!=source_row[key] for key in ('address','aliases','classification','state')):raise IntegrityError('Catalog row differs from preserved coverage')
        if [revision['revision'] for revision in row['revisions']]!=source_row['revisions']:raise IntegrityError('Catalog revisions differ from preserved coverage')
        for revision in row['revisions']:
            prefix=f"functions/{entry}/{revision['revision']}/"
            paths=sorted(revision_groups.get((entry,revision['revision']),[]))
            if set(paths)!={prefix+'metadata.json',prefix+'manifest.json'} and set(paths)!={prefix+'metadata.json',prefix+'manifest.json',prefix+'pseudocode.c'}:
                raise IntegrityError('Revision member set is incomplete')
            archives_for_revision={index[path][0] for path in paths}
            if len(archives_for_revision)!=1:raise IntegrityError('Revision split across archives')
            archive=next(iter(archives_for_revision));metadata=_read_member_json(root,index,prefix+'metadata.json')
            if metadata['address']!=entry or metadata['revision']!=revision['revision'] or revision_entry(metadata,archive,paths)!=revision:
                raise IntegrityError('Catalog revision differs from exact preserved metadata')
            source=f"evidence/{metadata['source_sha256']}.json"
            if source not in index:raise IntegrityError('Missing revision source capture')
            payload_manifest=_read_member_json(root,index,prefix+'manifest.json')
            expected_payloads={Path(path).name:index[path][1]['sha256'] for path in paths if not path.endswith('/manifest.json')}
            if payload_manifest!=expected_payloads:raise IntegrityError('Original revision manifest differs from preserved bytes')
            indexed_members.update(paths)
    if seen!=set(authority_rows) or indexed_members!={path for path in index if path.startswith('functions/')}:
        raise IntegrityError('Catalog does not index every committed revision')
    return {'root':str(root),'manifest':manifest,'catalog':catalog,'coverage':manifest['coverage'],
        'storage':{'source':manifest['source_storage'],'compact':file_storage(files.values())},
        '_member_index':index,'_archive_index':{archive['path']:archive for archive in archives}}


def iter_members(verified,kind=None):
    """Yield (archive path, original member descriptor) after check()."""
    for archive in verified['manifest']['archives']:
        if kind is None or archive['kind']==kind:
            for member in archive['members']:yield archive['path'],member


@contextmanager
def open_archive(root,verified,name):
    """Open one previously verified archive, rechecking its exact hash once.

    Viewer builders can read a shard's members through this context without
    repeatedly hashing the same ZIP. Consume members to EOF to check their CRC.
    """
    root=safe_path(root)
    archive=verified.get('_archive_index',{}).get(name)
    if archive is None:raise IntegrityError('Unknown verified archive')
    safe_path(root/name,kind='file')
    if exporter.file_sha(root/name)!=archive['sha256']:raise IntegrityError('Archive changed after verification')
    with zipfile.ZipFile(root/name) as bundle:yield bundle


@contextmanager
def open_member(root,verified,path):
    """Stream an indexed member through a freshly hash-checked ZIP archive."""
    original_path(path);member=verified.get('_member_index',{}).get(path)
    if member is None:raise IntegrityError('Unknown indexed member')
    name,_=member
    with open_archive(root,verified,name) as bundle,bundle.open(path) as stream:yield stream


@integrity_errors
def extract(root,address,output,*,revision=None,interrupt_before_publish=False):
    entry=exporter.address(address);root=safe_path(root);output=safe_path(output,fresh=True)
    if output.is_relative_to(root):raise IntegrityError('Extraction destination must be outside compact archive')
    verified=check(root);matches=[row for row in verified['catalog']['functions'] if row['address']==entry]
    if len(matches)!=1:raise IntegrityError('Address has no archived committed revisions')
    revisions=matches[0]['revisions']
    if revision is None:
        if len(revisions)!=1:raise IntegrityError('Multiple revisions require an explicit --revision')
        chosen=revisions[0]
    else:
        if not isinstance(revision,str) or not REVISION.fullmatch(revision):raise IntegrityError('Invalid explicit revision')
        selected=[item for item in revisions if item['revision']==revision]
        if len(selected)!=1:raise IntegrityError('Explicit revision is not archived for this address')
        chosen=selected[0]
    stage=_new_stage(output)
    for relative in chosen['members']:
        path=stage/relative;path.parent.mkdir(parents=True,exist_ok=True)
        with open_member(root,verified,relative) as incoming,path.open('xb') as outgoing:
            for block in iter(lambda:incoming.read(BLOCK),b''):outgoing.write(block)
            outgoing.flush();os.fsync(outgoing.fileno())
    write_json(stage/'extraction.json',{'schema':1,'format':FORMAT,'source_manifest_sha256':exporter.file_sha(root/'manifest.json'),
        'address':entry,'revision':chosen['revision'],'members':chosen['members']})
    for relative in chosen['members']:
        _,member=verified['_member_index'][relative]
        if exporter.file_sha(stage/relative)!=member['sha256']:raise IntegrityError('Extracted bytes differ from pinned member')
    if interrupt_before_publish:raise InterruptedError('Test interruption: unpublished extraction retained')
    _publish(stage,output)
    return {'root':str(output),'address':entry,'revision':chosen['revision'],'members':chosen['members'],'storage':file_storage(regular_files(output).values())}


def main():
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='command',required=True)
    build_args=commands.add_parser('build');build_args.add_argument('--corpus',type=Path,required=True);build_args.add_argument('--output',type=Path,required=True);build_args.add_argument('--shard-size',type=int,default=250)
    check_args=commands.add_parser('check');check_args.add_argument('--root',type=Path,required=True)
    extract_args=commands.add_parser('extract');extract_args.add_argument('--root',type=Path,required=True);extract_args.add_argument('--address',required=True);extract_args.add_argument('--revision');extract_args.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.command=='build':result=build(args.corpus,args.output,args.shard_size)
        elif args.command=='check':
            verified=check(args.root);result={key:verified[key] for key in ('root','coverage','storage')};result['manifest_sha256']=exporter.file_sha(args.root/'manifest.json')
        else:result=extract(args.root,args.address,args.output,revision=args.revision)
    except (IntegrityError,OSError,KeyError,TypeError,IndexError) as cause:parser.exit(1,f'compact corpus error: {cause}\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=='__main__':main()
