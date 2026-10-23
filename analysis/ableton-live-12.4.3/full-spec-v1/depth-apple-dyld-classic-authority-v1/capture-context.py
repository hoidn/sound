#!/usr/bin/env python3
"""Exact same-commit Apple source context; source bytes only."""
from pathlib import Path
import datetime,hashlib,json,urllib.request
p=Path(__file__).resolve().parent
commit='3f24a36068a96722cf3acbd5087983ce658e9d70'
rows=[]
for path in ['src/ImageLoader.h','src/ImageLoaderMachO.h','src/ImageLoaderMachOCompressed.h']:
 url='https://raw.githubusercontent.com/apple-oss-distributions/dyld/'+commit+'/'+path
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'sound-analyst-source-research'}),timeout=30)as r:
  b=r.read(1024*1024+1);assert r.status==200 and len(b)<=1024*1024
  row={'requested_url':url,'final_url':r.url,'status':r.status,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file':Path(path).name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 with open(p/Path(path).name,'xb')as f:f.write(b)
 rows.append(row)
with open(p/'context-receipt.json','x')as f:json.dump({'commit':commit,'records':rows,'source_only':True},f,indent=2);f.write('\n')
print(json.dumps(rows,indent=2))
