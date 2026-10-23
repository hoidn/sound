"""Read-only fixed148B preparation checks, no collector/decoder invocation."""
from pathlib import Path
import ast,copy,hashlib,json,struct,sys
HERE=Path(__file__).resolve().parent
OUT=HERE.parent/'depth-corpus-membrane-builder-prologue-instructions'

def identity(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def source_guard(text):
    tree = ast.parse(text)
    assignments = [n for n in ast.walk(tree) if isinstance(n, ast.Assign) and
                   any(isinstance(t, ast.Tuple) and [v.id for v in t.elts] == ['START', 'LENGTH']
                       for t in n.targets)]
    assert len(assignments) == 1 and ast.literal_eval(assignments[0].value) == (0x243e8, 148)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    launches = [n for n in calls if isinstance(n.func, ast.Attribute) and
                isinstance(n.func.value, ast.Name) and n.func.value.id == 'subprocess']
    assert len(launches) == 1 and launches[0].func.attr == 'Popen'
    assert not any(isinstance(n.func, ast.Name) and n.func.id in ('exec', 'eval', '__import__') for n in calls)
    assert "[str(TOOL), '-NN', '-n', '-x', '-f', '-a', 'arm', '-b', '64'," in text
    assert "'-E', 'little', '-m', hex(START), '-s', hex(START), '-q'," in text
    assert "'-c', 'pdj 37', str(OUT / 'prologue-148.bin')]" in text
    assert "child.communicate(timeout=30)" in text
    assert "stream.seek(metadata['file_offset'])" in text and "raw = stream.read(LENGTH)" in text
    assert "if OUT.exists():" in text and text.index('if OUT.exists():') < text.index('OUT.mkdir()')
    assert "save('before-map.json'" in text and text.index("save('before-map.json'") < text.index("stream.seek(")
    assert text.index("save('attempt.json'") < text.index("status['attempted_decoder_children'] = 1") < text.index('child = subprocess.Popen')
    assert "save('returned-pid.json'" in text and "except BaseException as error:" in text
    assert "save('after-map.json'" in text and "save('status.json', status)" in text
    assert "row.get('type') not in ('invalid', 'ill')" in text
    assert "row['opcode'].strip().lower() not in ('', 'invalid', 'ill', 'none')" in text

def row_metadata_accepts(text, rows):
    tree = ast.parse(text)
    tests = [n.test for n in ast.walk(tree) if isinstance(n, ast.Assert) and
             ((isinstance(n.test, ast.Call) and isinstance(n.test.func, ast.Name) and
               n.test.func.id == 'all' and 'row[' in ast.unparse(n.test)) or
              ast.unparse(n.test) == 'len(rows) == 37')]
    assert len(tests) == 2
    namespace = {'__builtins__': {}, 'rows': rows, 'START': 0x243e8,
                 'all': all, 'len': len, 'enumerate': enumerate,
                 'isinstance': isinstance, 'str': str}
    return all(eval(compile(ast.Expression(test), '<synthetic-row-predicate-only>', 'eval'),
                    namespace) for test in tests)

def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no collector/decoder/extraction.')
    assert not OUT.exists(), 'Future destination must remain absent.'
    pins=json.loads((HERE/'inputs.json').read_text())['pins']
    delta=json.loads((HERE/'delta.json').read_text())
    watched={Path(r['path']) for r in pins} | {Path(r['path']) for r in delta['preserved_parent_files']} | {p for p in HERE.iterdir() if p.is_file()}
    before=[identity(p) for p in sorted(watched)]
    for r in pins+delta['preserved_parent_files']:
        assert identity(Path(r['path'])) == {k:r[k] for k in ('path','bytes','sha256')}
    old=Path(delta['collector_before']['path']).parent
    assert identity(old/'collect-once.py') == delta['collector_before']
    assert identity(HERE/'collect-once.py') == delta['collector_after']
    assert pins[:15] == json.loads((old/'inputs.json').read_text())['pins']
    text=(HERE/'collect-once.py').read_text()
    source_guard(text)
    restored=text
    for op in reversed(delta['collector_literal_operations']):
        assert restored.count(op['after'])==op['occurrences']
        restored=restored.replace(op['after'],op['before'])
    assert restored.encode()==(old/'collect-once.py').read_bytes()
    assert "row.get('type') not in ('invalid', 'ill')" in text
    assert "row['opcode'].strip().lower() not in ('', 'invalid', 'ill', 'none')" in text
    m=json.loads((HERE/'header-map.json').read_text()); previous=json.loads((old/'header-map.json').read_text())
    for key in previous:
        if key not in ('virtual_range_half_open','file_offset','length'):assert m[key]==previous[key]
    assert identity(Path(m['image']['path']))==m['image']
    with Path(m['image']['path']).open('rb') as f:
        header=f.read(32);assert header.hex()==m['header_hex']
        vals=struct.unpack('<IiiIIIII',header);commands=f.read(vals[5])
    assert vals[0]==0xfeedfacf and vals[1]==0x100000c
    assert commands.hex()==m['load_commands_hex'] and hashlib.sha256(commands).hexdigest()==m['load_commands_sha256']
    segments=[];cursor=0
    for i in range(vals[4]):
        cmd,size=struct.unpack_from('<II',commands,cursor);assert size>=8 and cursor+size<=len(commands)
        if cmd==0x19:
            n,va,vs,fo,fs,mp,ip,ns,fl=struct.unpack_from('<16sQQQQiiII',commands,cursor+8)
            segments.append(dict(name=n.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=fl))
        cursor+=size
    assert cursor==len(commands) and segments==m['segments']
    matched=[s for s in segments if s['vmaddr']<=0x243e8 and 0x2447c<=s['vmaddr']+s['filesize']]
    assert matched==[m['selected_segment']] and matched[0]['name']=='__TEXT'
    assert matched[0]['fileoff']+0x243e8-matched[0]['vmaddr']==m['file_offset']==148456
    assert m['length']==148 and m['virtual_range_half_open']==['0x243e8','0x2447c']
    assert m['instruction_window_extracted'] is False
    proposal=json.loads((HERE/'proposal.json').read_text())
    oldargv=json.loads((old/'proposal.json').read_text())['future_invocation']['tool_argv']
    argv=proposal['future_invocation']['tool_argv']
    assert [(i,a,b) for i,(a,b) in enumerate(zip(oldargv,argv)) if a!=b]==[(12,'0x24884','0x243e8'),(14,'0x24884','0x243e8'),(17,'pdj 3','pdj 37'),(18,oldargv[18],str(OUT/'prologue-148.bin'))]
    assert len(argv)==len(oldargv)==19 and 0x243e8+36*4==0x24478
    basepath=next(Path(r['path']) for r in pins if r['role']=='base_query')
    metadata=json.loads(basepath.read_text())['source_locator']['metadata']
    assert metadata['entry']=='0x243e8'
    assert any(r[0]=='0x24478' and any(t['to']=='0x24888' for t in r[2]) for r in metadata['indirect']['items'])
    good=[dict(offset=0x243e8+4*i,size=4,type='nop',opcode='nop',bytes='00000000') for i in range(37)]
    assert row_metadata_accepts(text,good)
    invalid=[]
    for field,value in [('type','invalid'),('type','ill'),('opcode',None),('opcode',''),('opcode','invalid'),('opcode','ill'),('opcode','None'),('opcode',' INVALID ')]:
        rows=copy.deepcopy(good);rows[17][field]=value;invalid.append(rows)
    rows=copy.deepcopy(good);del rows[17]['opcode'];invalid.append(rows)
    rows=copy.deepcopy(good)
    for row in rows:row.update(type='ill',opcode='invalid')
    invalid.append(rows)
    assert all(not row_metadata_accepts(text,r) for r in invalid)
    mutations=[('0x243e8, 148','0x243e4, 148'),('0x243e8, 148','0x243e8, 152'),("'pdj 37'","'pdj 38'"),("'-NN'","'-N'"),("'-x'","'-w'"),("'-x', '-f'","'-x'"),('child.communicate(timeout=30)','child.communicate(timeout=31)'),('if OUT.exists():','if False:')]
    for a,b in mutations:
        changed=text.replace(a,b,1);assert changed!=text
        try:source_guard(changed)
        except AssertionError:pass
        else:raise AssertionError('Unsafe fixedrange/flags mutation accepted')
    seal=HERE/'manifest.json'
    if seal.exists():
        inventory=json.loads(seal.read_text())['files']
        assert {r['path'] for r in inventory}=={p.name for p in HERE.iterdir() if p.is_file() and p!=seal}
        for r in inventory:
            got=identity(HERE/r['path']);assert (got['bytes'],got['sha256'])==(r['bytes'],r['sha256'])
    for p in HERE.iterdir():
        if p.is_file():
            t=p.read_text();assert t.endswith('\n') and all(s==s.rstrip() for s in t.splitlines())
    assert before==[identity(p) for p in sorted(watched)]
    print(json.dumps(dict(status='PASS preparation only',fixed_range=['0x243e8','0x2447c'],future_rows=37,literal_collector_ops_reversible=len(delta['collector_literal_operations']),scope_guard_negatives=8,row_guard_negatives=10,valid_synthetic37rows=True,parent_files_exact=len(delta['preserved_parent_files']),watched=len(watched),unchanged=True,instruction_window_extracted=False,decoder_children=0,original_execution=False),indent=2))


if __name__=='__main__':
    main()
