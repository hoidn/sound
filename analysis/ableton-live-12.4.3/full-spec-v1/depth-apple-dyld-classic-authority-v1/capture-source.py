#!/usr/bin/env python3
"""Retain only official Apple dyld source at one resolved tag commit."""
from pathlib import Path
import datetime
import hashlib
import json
import urllib.request

HERE=Path(__file__).resolve().parent
records=[]
def get(url,name):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    request=urllib.request.Request(url,headers={'User-Agent':'sound-analyst-source-research','Accept':'application/vnd.github+json' if 'api.github.com' in url else 'text/plain'})
    with urllib.request.urlopen(request,timeout=30) as response:
        data=response.read(2*1024*1024+1)
        assert response.status==200 and len(data)<=2*1024*1024
        row={'requested_url':url,'final_url':response.url,'status':response.status,'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'file':name,'response_headers':dict(response.headers.items())}
    with open(HERE/name,'xb')as f:f.write(data)
    records.append(row)
    return data
ref=json.loads(get('https://api.github.com/repos/apple-oss-distributions/dyld/git/ref/tags/dyld-852.2','tag-ref.json'))
obj=ref['object']
if obj['type']=='tag':
    tag=json.loads(get(obj['url'],'tag-object.json'));obj=tag['object']
assert obj['type']=='commit' and len(obj['sha'])==40
commit=obj['sha']
for path in ['src/ImageLoaderMachOCompressed.cpp','dyld3/MachOAnalyzer.cpp']:
    get('https://raw.githubusercontent.com/apple-oss-distributions/dyld/'+commit+'/'+path,Path(path).name)
with open(HERE/'capture-receipt.json','x')as f:json.dump({'tag':'dyld-852.2','commit':commit,'records':records,'source_only':True,'original_or_parser_execution':0},f,indent=2);f.write('\n')
print(json.dumps({'commit':commit,'records':[{k:r[k]for k in ['file','status','bytes','sha256']}for r in records]},indent=2))
