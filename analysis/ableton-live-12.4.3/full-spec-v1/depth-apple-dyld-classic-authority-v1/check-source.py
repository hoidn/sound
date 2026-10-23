#!/usr/bin/env python3
"""Source-custody/projection checks only; no network or dyld execution."""
import copy
import hashlib
import json
from pathlib import Path

P=Path(__file__).resolve().parent
COMMIT='3f24a36068a96722cf3acbd5087983ce658e9d70'
MAP=json.loads((P/'selected-source-map.json').read_text())
RECEIPTS=[json.loads((P/n).read_text())for n in ['capture-receipt.json','context-receipt.json','helper-context-receipt.json']]

def verify(source_map,receipts,tag_object):
    assert source_map['commit']==COMMIT and source_map['tag']=='dyld-852.2'
    assert tag_object['object']=={'sha':COMMIT,'type':'commit','url':'https://api.github.com/repos/apple-oss-distributions/dyld/git/commits/'+COMMIT}
    rows=[r for rec in receipts for r in rec['records']]
    assert len(rows)==9 and len({r['file']for r in rows})==9
    for r in rows:
        b=(P/r['file']).read_bytes()
        assert r['status']==200 and len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
        assert r['requested_url']==r['final_url']
        assert r['requested_url'].startswith(('https://api.github.com/repos/apple-oss-distributions/dyld/','https://raw.githubusercontent.com/apple-oss-distributions/dyld/'+COMMIT+'/'))
    assert len(source_map['selected_ranges'])==17
    parts=[]
    for r in source_map['selected_ranges']:
        b=(P/r['file']).read_bytes();lines=b.splitlines(keepends=True)
        assert hashlib.sha256(b).hexdigest()==r['source_sha256']
        assert r['lines']==r['last_line']-r['first_line']+1
        selected=b''.join(lines[r['first_line']-1:r['last_line']])
        assert len(selected)==r['selected_bytes'] and hashlib.sha256(selected).hexdigest()==r['selected_sha256']
        title='\n===== '+r['file']+':'+str(r['first_line'])+'-'+str(r['last_line'])+' '+r['scope']+' =====\n'
        parts.append(title.encode()+selected)
    assert b''.join(parts)==(P/'selected-functions.txt').read_bytes()
    return len(rows),sum(r['lines']for r in source_map['selected_ranges'])

tag=json.loads((P/'tag-object.json').read_text())
requests,lines=verify(MAP,RECEIPTS,tag)
controls=[]
for name in ['wrong_commit','changed_line_range','truncated_function_projection','bad_source_hash','nonprimary_URL']:
    sm,rs,tg=copy.deepcopy(MAP),copy.deepcopy(RECEIPTS),copy.deepcopy(tag)
    if name=='wrong_commit':tg['object']['sha']='0'*40
    elif name=='changed_line_range':sm['selected_ranges'][0]['first_line']+=1
    elif name=='truncated_function_projection':sm['selected_ranges'][0]['last_line']-=1
    elif name=='bad_source_hash':rs[0]['records'][2]['sha256']='0'*64
    else:rs[0]['records'][2]['requested_url']=rs[0]['records'][2]['final_url']='https://example.invalid/source'
    try:verify(sm,rs,tg)
    except AssertionError:controls.append(name)
    else:raise AssertionError('accepted control '+name)
print(json.dumps({'status':'PASS','owned_source_data_only':True,'network_or_parser_execution':False,'captured_requests':requests,'selected_lines':lines,'projection_controls':controls,'control_count':len(controls)},indent=2))
