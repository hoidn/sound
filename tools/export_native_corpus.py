#!/usr/bin/env python3
"""Analyst-only immutable REA evidence ingestion. Does not invoke an analyzer."""
import argparse
from collections import Counter, OrderedDict
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile


class IntegrityError(ValueError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)+'\n').encode()


# REA Ghidra canonical address-space syntax (GhidraInventoryValues.js).
# Keep encoded space names encoded: decoding %2F into a path separator is unsafe.
ADDRESS_PATTERN = re.compile(r'(?:(?P<space>(?:[A-Za-z0-9._~-]|%[0-9A-F]{2})+):)?(?P<offset>0[xX][0-9a-fA-F]+)')


def address(value):
    match=ADDRESS_PATTERN.fullmatch(value) if isinstance(value,str) else None
    if not match:
        raise IntegrityError(f'Expected explicit native address with optional encoded space: {value!r}')
    offset=hex(int(match['offset'],16))
    return f"{match['space']}:{offset}" if match['space'] is not None else offset


def address_sort_key(value):
    canonical=address(value)
    space, separator, offset=canonical.partition(':')
    return (space,int(offset,16)) if separator else ('',int(canonical,16))


def safe_destination(root, path, kind):
    """Reject preexisting symlinks and non-directory ancestors before a write.

    The coordinator's exclusive writer lock covers normal use; this is not a
    defense against a hostile process swapping filesystem paths concurrently.
    """
    if root.is_symlink() or (root.exists() and not root.is_dir()):
        raise IntegrityError('Unsafe corpus root')
    try:parts=path.relative_to(root).parts
    except ValueError as cause:raise IntegrityError('Destination outside corpus') from cause
    if any(part in ('.','..') for part in parts):raise IntegrityError('Unsafe destination components')
    current=root
    for index,part in enumerate(parts):
        current=current/part
        if current.is_symlink():raise IntegrityError(f'Symbolic link destination: {current}')
        expected=kind if index==len(parts)-1 else 'directory'
        if current.exists() and not (current.is_dir() if expected=='directory' else current.is_file()):
            raise IntegrityError(f'Unexpected destination type: {current}')


def write_boundaries(root):
    for name in ('functions','.staging','evidence','inventory'):
        safe_destination(root,root/name,'directory')
    for name in ('run.json','coverage.json','.ingest.lock','inventory/v1.json'):
        safe_destination(root,root/name,'file')


def durable(path, data, immutable=True):
    path.parent.mkdir(parents=True, exist_ok=True)
    if immutable and path.exists():
        if path.read_bytes() != data:
            raise IntegrityError(f'Conflicting immutable file: {path}')
        return
    fd, tmp = tempfile.mkstemp(prefix='.'+path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data); stream.flush(); os.fsync(stream.fileno())
        os.replace(tmp, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try: os.fsync(directory)
        finally: os.close(directory)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


@contextmanager
def locked(root):
    write_boundaries(root)
    root.mkdir(parents=True, exist_ok=True)
    with (root/'.ingest.lock').open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def records(value):
    """Admit observed REA bundle, record, or MCP envelope; no recursive data search."""
    if isinstance(value, dict):
        if 'evidence_id' in value and 'normalized_result' in value:
            return [value]
        if isinstance(value.get('records'), list):
            return value['records']
        if value.get('ok') is True and 'result' in value:
            return records(value['result'])
        if isinstance(value.get('structuredContent'), dict):
            return records(value['structuredContent'])
        if isinstance(value.get('content'), list):
            found=[]
            for item in value['content']:
                if item.get('type') == 'text':
                    try: found.extend(records(json.loads(item['text'])))
                    except (json.JSONDecodeError, IntegrityError): pass
            if found: return found
    raise IntegrityError('No supported full REA evidence record; truncated/tool-error responses are not evidence')


def native_profile(record):
    profile=record.get('analysis_profile')
    if not isinstance(profile, dict): raise IntegrityError('Missing analysis profile')
    if record.get('provider', {}).get('id') == 'rea-workflow':
        profile=profile.get('parameters', {}).get('upstream_analysis_profile')
    if not isinstance(profile, dict) or not re.fullmatch('[0-9a-f]{64}', profile.get('digest','')):
        raise IntegrityError('Missing native profile identity')
    return profile


def validate(record, run):
    subject=record.get('subject') or {}
    if subject.get('digest',{}).get('sha256') != run['target_sha256'] or subject.get('architecture') != run['architecture']:
        raise IntegrityError('Target identity mismatch')
    if native_profile(record) != run['analysis_profile']:
        raise IntegrityError('Native provider/profile mismatch')
    if not re.fullmatch(r'ev_[0-9a-f]{64}', record.get('evidence_id','')):
        raise IntegrityError('Invalid evidence identity')


def freeze_inventory(rows):
    groups={}
    path_keys={}
    for row in rows:
        entry=address(row['address'])
        # Corpus volumes can be case-insensitive even though REA spaces are not.
        # Reject ambiguous literal directory names before any corpus writes.
        path_key=entry.casefold()
        if path_key in path_keys and path_keys[path_key]!=entry:
            raise IntegrityError(f'Address-space paths collide on case-insensitive storage: {path_keys[path_key]} and {entry}')
        path_keys[path_key]=entry
        facts=row.get('procedure') or row.get('classification') or {}
        body=row.get('body') or {}
        classification=('external' if facts.get('external') is True else
                        'bodyless' if body.get('available') is True and body.get('total_bytes') == 0 else
                        'eligible' if facts.get('external') is False else 'unclassified')
        old=groups.get(entry)
        if old and (old['classification'] != classification or old['procedure'] != facts or old['body'] != body):
            raise IntegrityError(f'Contradictory duplicate address: {entry}')
        group=groups.setdefault(entry, {'address':entry,'aliases':[], 'classification':classification,'procedure':facts,'body':body})
        name=row.get('value',row.get('name'))
        if name and name not in group['aliases']: group['aliases'].append(name)
    return [groups[key] for key in sorted(groups,key=address_sort_key)]


def retain(root, source):
    data=Path(source).read_bytes();digest=sha(data)
    path=root/'evidence'/f'{digest}.json';safe_destination(root,path,'file');durable(path,data)
    return digest, records(json.loads(data))


def initialize(root, source, target, arch):
    write_boundaries(root)
    if not re.fullmatch('[0-9a-f]{64}',target): raise IntegrityError('Invalid target SHA-256')
    data=Path(source).read_bytes();candidates=[r for r in records(json.loads(data)) if r.get('operation')=='list_procedures']
    if len(candidates)!=1: raise IntegrityError('Supply exactly one list_procedures record')
    rec=candidates[0]
    run={'schema':1,'target_sha256':target,'architecture':arch,'analysis_profile':native_profile(rec),
         'inventory_evidence_id':rec['evidence_id'],'inventory_source_sha256':sha(data)}
    validate(rec,run)
    rows=rec['normalized_result'];groups=freeze_inventory(rows)
    inventory={'schema':1,'rows':rows,'functions':groups,'evidence_id':rec['evidence_id']}
    # Validate old immutable files before any writes on unchanged/rejected initialization.
    for path,value in [(root/'run.json',run),(root/'inventory'/'v1.json',inventory)]:
        if path.exists() and path.read_bytes()!=encoded(value):raise IntegrityError(f'Existing identity/inventory differs: {path}')
    retain(root,source);durable(root/'run.json',encoded(run));durable(root/'inventory'/'v1.json',encoded(inventory))
    return coverage(root)


def extraction(record):
    op=record['operation'];value=record['normalized_result']
    if op=='batch_decompile':
        for i,item in enumerate(value['items']):
            procedure=item.get('procedure') or {}
            entry=address(procedure.get('address') if procedure.get('status')=='resolved' else item['address'])
            if address(item['address']) != entry: raise IntegrityError('Batch selector did not resolve to exact entry')
            error=item.get('error')
            if item.get('status') != 'ok': error=error or {'message':f"Provider item status: {item.get('status')}"}
            yield i,entry,item.get('pseudocode'),error,{'procedure':procedure},[]
    elif op=='procedure_pseudo_code':
        yield 0,address(record['parameters']['procedure']),value,None,{},[]
    elif op=='analyze_function':
        procedure=value['procedure'];entry=address(procedure.get('address',procedure.get('entrypoint')))
        yield 0,entry,value.get('pseudocode'),None,{'procedure':procedure,
            'callers':value.get('callers',[]),'callees':value.get('callees',[]),
            'incoming_references':value.get('incoming_references',[]),'outgoing_references':value.get('outgoing_references',[])},value.get('limitations',[])


class FilesystemCorpusReader:
    """Read interface for the shared source-authority validators.

    Alternative readers must provide exact bytes/hashes and a complete listing
    of committed revisions and regular payload names. They cannot persist a
    coverage checkpoint. Filesystem checks stay here rather than disappearing
    when coverage is requested without writes.
    """
    def __init__(self,root):
        write_boundaries(root)
        self.root=root
    def read_bytes(self,path):return path.read_bytes()
    def file_sha(self,path):return file_sha(path)
    def revision_files(self,path):
        if any(p.is_symlink() or not p.is_file() for p in path.rglob('*')):
            raise IntegrityError('Unexpected directory/symbolic link in revision payload')
        return {str(p.relative_to(path)) for p in path.rglob('*') if p.is_file()}
    def committed_directories(self,functions):return committed_directories(self.root,functions)


def verify_revision(path, *, reader=None):
    reader=FilesystemCorpusReader(path) if reader is None else reader
    names=reader.revision_files(path)
    manifest=json.loads(reader.read_bytes(path/'manifest.json'))
    if 'metadata.json' not in manifest:raise IntegrityError('Missing required metadata payload')
    actual=names-{'manifest.json'}
    if actual != set(manifest):raise IntegrityError(f'Payload set differs: {path}')
    for name,digest in manifest.items():
        if name not in ('metadata.json','pseudocode.c'):raise IntegrityError('Unexpected revision payload')
        if reader.file_sha(path/name)!=digest:raise IntegrityError(f'Corrupt committed payload: {path/name}')
    return json.loads(reader.read_bytes(path/'metadata.json'))


def metadata_for(rec, record_index, source_hash, item):
    index,entry,code,error,details,limitations=item
    if code is not None and not isinstance(code,str):raise IntegrityError('Pseudocode must be string or null')
    error=error or rec.get('error')
    if rec.get('status') not in (None,'ok'):error=error or {'message':'Evidence record reports failure'}
    warnings=[line.strip() for line in (code or '').splitlines() if re.search(r'\bWARNING\b',line,re.I)]
    warnings += [v for v in limitations if 'diagnostic' in v.lower() or 'warning' in v.lower()]
    state=('exported-with-warnings' if warnings else 'exported') if code and not error else 'failed'
    revision=f"{rec['evidence_id']}-{index}"
    return {'address':entry,'revision':revision,'evidence_id':rec['evidence_id'],
      'source_sha256':source_hash,'source_record_index':record_index,'source_item_index':index,
      'state':state,'warnings':warnings,'limitations':rec.get('limitations',[])+limitations,
      'partial_pseudocode':bool(code and error),
      'error':error or (None if code else {'message':'Provider returned null or empty pseudocode'}),
      'details':details,'analysis_profile':rec['analysis_profile']}


def commit_evidence(root, source, context, interrupt_before_commit=False):
    run=context['run'];functions=context['functions']
    data=Path(source).read_bytes();recs=records(json.loads(data));work=[]
    for record_index,rec in enumerate(recs):
        if rec.get('operation') not in ('batch_decompile','procedure_pseudo_code','analyze_function'):continue
        validate(rec,run)
        for index,entry,code,error,details,limitations in extraction(rec):
            if entry not in functions:raise IntegrityError(f'Function outside frozen inventory: {entry}')
            if code and functions[entry]['classification'] in ('external','bodyless'):
                raise IntegrityError('Pseudocode contradicts excluded inventory classification')
            metadata=metadata_for(rec,record_index,sha(data),(index,entry,code,error,details,limitations))
            revision=metadata['revision']
            work.append((entry,revision,code,metadata))
    if not work:raise IntegrityError('No supported pseudocode attempts in evidence')
    # Validate all destinations in this source before retaining or publishing any.
    write_boundaries(root)
    safe_destination(root,root/'evidence'/f'{sha(data)}.json','file')
    for entry,revision,code,metadata in work:
        final=root/'functions'/entry/revision
        safe_destination(root,final,'directory')
        for name in ('metadata.json','manifest.json','pseudocode.c'):
            safe_destination(root,final/name,'file')
    retain(root,source)
    for entry,revision,code,metadata in work:
        final=root/'functions'/entry/revision
        if final.exists():
            previous=verify_revision(final)
            # Same evidence can be retained inside a different source bundle.
            comparable=lambda m:{k:v for k,v in m.items() if k not in ('source_sha256','source_record_index')}
            if comparable(previous)!=comparable(metadata):raise IntegrityError('Evidence identity reused with different result')
            if code and (final/'pseudocode.c').read_bytes()!=code.encode():raise IntegrityError('Evidence identity reused with changed code')
            continue
        stage_root=root/'.staging';stage_root.mkdir(exist_ok=True)
        stage=Path(tempfile.mkdtemp(prefix='revision-',dir=stage_root))
        durable(stage/'metadata.json',encoded(metadata))
        if code:durable(stage/'pseudocode.c',code.encode())
        durable(stage/'manifest.json',encoded({p.name:sha(p.read_bytes()) for p in stage.iterdir()}))
        if interrupt_before_commit:raise InterruptedError('Test interruption: staged files remain uncommitted')
        safe_destination(root,final,'directory')
        final.parent.mkdir(parents=True,exist_ok=True);os.rename(stage,final)
        fd=os.open(final.parent,os.O_RDONLY)
        try:os.fsync(fd)
        finally:os.close(fd)


def file_sha(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()


def inventory_context(root, *, reader=None):
    if reader is None:write_boundaries(root)
    reader=FilesystemCorpusReader(root) if reader is None else reader
    pins={}
    def read_pinned(path):
        raw=reader.read_bytes(path);pins[str(path.relative_to(root))]=sha(raw)
        return json.loads(raw)
    run=read_pinned(root/'run.json');inv=read_pinned(root/'inventory'/'v1.json')
    source=root/'evidence'/f"{run['inventory_source_sha256']}.json"
    source_value=read_pinned(source)
    if pins[str(source.relative_to(root))]!=run['inventory_source_sha256']:raise IntegrityError('Inventory source corrupted')
    rec=next(r for r in records(source_value) if r.get('evidence_id')==run['inventory_evidence_id'])
    validate(rec,run)
    if inv['rows']!=rec['normalized_result'] or inv['functions']!=freeze_inventory(inv['rows']):raise IntegrityError('Frozen inventory corrupted')
    return {'run':run,'inventory':inv,'functions':{g['address']:g for g in inv['functions']},'pins':pins}


def recheck_context(root, context, *, reader=None):
    reader=FilesystemCorpusReader(root) if reader is None else reader
    for relative,digest in context['pins'].items():
        if reader.file_sha(root/relative)!=digest:raise IntegrityError('Pinned inventory context changed')


def ingest(root, source, interrupt_before_commit=False):
    context=inventory_context(root)
    commit_evidence(root,source,context,interrupt_before_commit)
    return coverage(root,context)


def ingest_many(root, sources):
    if not sources:raise IntegrityError('Supply at least one explicit evidence file')
    context=inventory_context(root)
    for source in sources:commit_evidence(root,source,context)
    return coverage(root,context)


def committed_directories(root, functions):
    base=root/'functions'
    if base.is_symlink():raise IntegrityError('Invalid functions directory')
    if not base.exists():return {}
    if not base.is_dir():raise IntegrityError('Invalid functions directory')
    found={}
    for entry_path in base.iterdir():
        if entry_path.is_symlink() or not entry_path.is_dir():raise IntegrityError('Unexpected function directory entry')
        entry=address(entry_path.name)
        if entry!=entry_path.name or entry not in functions:raise IntegrityError('Unknown/noncanonical function directory')
        found[entry]=[]
        for revision in entry_path.iterdir():
            if revision.is_symlink() or not revision.is_dir() or not re.fullmatch(r'ev_[0-9a-f]{64}-[0-9]+',revision.name):
                raise IntegrityError('Unexpected revision directory entry')
            found[entry].append(revision)
    return found


def coverage(root, context=None, *, persist=True, reader=None):
    if reader is not None and persist:raise IntegrityError('Explicit corpus readers cannot persist coverage')
    if reader is None:write_boundaries(root)
    reader=FilesystemCorpusReader(root) if reader is None else reader
    context=inventory_context(root,reader=reader) if context is None else context
    recheck_context(root,context,reader=reader)
    run=context['run'];inv=context['inventory']
    paths=reader.committed_directories(context['functions'])
    source_cache=OrderedDict()
    entries=[]
    for group in inv['functions']:
        entry=group['address'];revisions=[]
        for path in sorted(paths.get(entry,[])):
            metadata=verify_revision(path,reader=reader);digest=metadata['source_sha256']
            if not re.fullmatch('[0-9a-f]{64}',digest):raise IntegrityError('Invalid source digest')
            if digest not in source_cache:
                try:raw=reader.read_bytes(root/'evidence'/f'{digest}.json')
                except FileNotFoundError as cause:raise IntegrityError('Missing authoritative evidence') from cause
                if sha(raw)!=digest:raise IntegrityError('Retained source evidence corrupted')
                source_cache[digest]=records(json.loads(raw))
                if len(source_cache)>8:source_cache.popitem(last=False)
            source_cache.move_to_end(digest)
            source_record=source_cache[digest][metadata['source_record_index']]
            validate(source_record,run)
            items={item[0]:item for item in extraction(source_record)}
            item=items[metadata['source_item_index']]
            expected=metadata_for(source_record,metadata['source_record_index'],digest,item)
            if expected!=metadata or metadata['address']!=entry or metadata['revision']!=path.name:
                raise IntegrityError('Revision metadata disagrees with authoritative evidence')
            code=item[2]
            if code and reader.read_bytes(path/'pseudocode.c')!=code.encode():raise IntegrityError('Pseudocode differs from evidence')
            if not code and 'pseudocode.c' in reader.revision_files(path):raise IntegrityError('Unexpected pseudocode payload')
            revisions.append(metadata)
        statuses={r['state'] for r in revisions}
        state=group['classification'] if group['classification']!='eligible' else (
            'exported' if 'exported' in statuses else 'exported-with-warnings' if 'exported-with-warnings' in statuses else 'failed' if revisions else 'pending')
        entries.append({'address':entry,'aliases':group['aliases'],'classification':group['classification'],
                        'state':state,'attempts':len(revisions),'revisions':[r['revision'] for r in revisions]})
    counts=dict(Counter(e['state'] for e in entries));eligible=sum(g['classification']=='eligible' for g in inv['functions'])
    result={'schema':1,'target_sha256':run['target_sha256'],'inventory_evidence_id':run['inventory_evidence_id'],
        'inventory_rows':len(inv['rows']),'unique_functions':len(entries),'eligible':eligible,'counts':counts,
        'attempted':sum(e['attempts']>0 and e['classification']=='eligible' for e in entries),
        'successful':counts.get('exported',0)+counts.get('exported-with-warnings',0),'functions':entries,
        'limitations':['Inventory is discovered functions, not all original source.',
                      'Nonexternal functions are eligible; body completeness may be unknown until a dossier.',
                      'No decompilation output establishes runtime compatibility.']}
    if persist:durable(root/'coverage.json',encoded(result),immutable=False)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['init','ingest','ingest-many','check','queue'])
    parser.add_argument('--root',type=Path,required=True);parser.add_argument('--evidence',type=Path,action='append')
    parser.add_argument('--target-sha256');parser.add_argument('--architecture',default='arm64');parser.add_argument('--limit',type=int,default=20)
    args=parser.parse_args()
    with locked(args.root):
        if args.command in ('init','ingest') and len(args.evidence or [])!=1:parser.error('init/ingest require exactly one --evidence')
        if args.command=='init':result=initialize(args.root,args.evidence[0],args.target_sha256,args.architecture)
        elif args.command=='ingest':result=ingest(args.root,args.evidence[0])
        elif args.command=='ingest-many':result=ingest_many(args.root,args.evidence)
        else:result=coverage(args.root)
    if args.command=='queue':print(json.dumps([e['address'] for e in result['functions'] if e['state']=='pending'][:args.limit]))
    else:print(json.dumps({k:v for k,v in result.items() if k!='functions'},indent=2))

if __name__=='__main__':main()
