"""Read-only preparation assertions; only isolated analyst row predicates on synthetic data."""
from pathlib import Path
import ast,copy,hashlib,json,struct,sys
HERE=Path(__file__).resolve().parent
DEST=HERE.with_name('depth-utility-mute-calcmain-instruction-data')
START=0x1021658b0

def ident(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def predicate(text):
 tree=ast.parse(text)
 selected=[n.test for n in ast.walk(tree) if isinstance(n,ast.Assert) and 'len(decoded)' in ast.unparse(n.test)]
 assert len(selected)==1
 return selected[0]
def accepts(test,rows,raw):
 ns=dict(decoded=rows,START=START,all=all,len=len,enumerate=enumerate,str=str,isinstance=isinstance,bytes=bytes)
 try:return bool(eval(compile(ast.Expression(test),'<isolated-synthetic-row-predicate>','eval'),ns)) and len(raw)==len(rows)*4 and b''.join(bytes.fromhex(r['bytes']) for r in rows)==raw
 except (AssertionError,ValueError,KeyError,TypeError):return False

def source_guard(text):
 tree=ast.parse(text)
 assert "START+LENGTH<=int(plan['helper']['body_end_exclusive'],16)" in text
 for s in ['START=0x1021658b0','LENGTH=72',"'pdj 18'",'len(decoded)==18',"len(bytes.fromhex(r['bytes']))==4", "str(r.get('type','')).strip().lower() not in ('invalid','ill')", "r['opcode'].strip().lower() not in ('','invalid','ill','none')", "if DEST.exists():", "'-NN','-n','-x','-f','-a','arm','-b','64'", 'child.communicate(timeout=30)', "assert START+LENGTH==0x1021658f8", "raw=f.read(LENGTH);assert len(raw)==LENGTH"]:assert s in text,s
 launches=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='subprocess']
 assert len(launches)==1 and launches[0].func.attr=='Popen'
 assert text.index("save('before-map.json'")<text.index('f.seek(offset)')
 assert text.index("save('invocation-before.json'")<text.index("state['tool_attempts']=1")<text.index('child=subprocess.Popen')
 assert "state['tool_returned_pid']=child.pid" in text
 assert "except Exception as error:" in text and "save('after-map.json'" in text

def main():
 if sys.argv[1:]!=['--check']:raise SystemExit('Read-only --check only; no extraction/collector/decoder.')
 assert not DEST.exists()
 plan=json.loads((HERE/'plan.json').read_text());delta=json.loads((HERE/'source-delta.json').read_text())
 paths=sorted({Path(r['path']) for r in [plan['image'],plan['tool'],*plan['providers']]}|{p for p in HERE.iterdir() if p.is_file()})
 before=[ident(p) for p in paths]
 for r in [plan['image'],plan['tool'],*plan['providers']]:assert ident(Path(r['path']))==r
 text=(HERE/'extract-decode-once.py').read_text();source_guard(text)
 assert ident(HERE/'extract-decode-once.py')==delta['after']
 restored=text
 for op in reversed(delta['literal_operations']):
  assert restored.count(op['after'])==op['occurrences'];restored=restored.replace(op['after'],op['before'])
 assert restored.encode()==Path(delta['before']['path']).read_bytes()
 for r in delta['old_parent_files']:assert ident(Path(r['path']))==r
 assert plan['helper']['va']=='0x1021658b0' and plan['helper']['length']==72 and plan['helper']['file_offset']==0x21658b0
 assert plan['helper']['body_end_exclusive']=='0x1021658f8' and int(plan['helper']['body_end_exclusive'],16)>=START+72
 assert plan['decoder_argv']==[plan['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(START),'-s',hex(START),'-q','-c','pdj 18',str(DEST/'calcmain-72.bin')]
 anchor=plan['source_anchor'];source=json.loads(Path(anchor['provider']['path']).read_text())['full_selected_records'][1]
 assert source['path']==anchor['source_provider'] and source['line_1based']==anchor['line_1based'] and source['raw_sha256_excluding_LF']==anchor['raw_sha256']
 assert {k:v for k,v in source['record'].items() if k!='code'}==anchor['metadata']
 # Fresh header/load-command metadata only. No selected-window seek/read.
 with Path(plan['image']['path']).open('rb') as f:
  header=f.read(32);v=struct.unpack('<IiiIIIII',header);assert header.hex()==plan['image_header_hex'] and v[4:6]==(53,6944)
  commands=f.read(v[5]);assert hashlib.sha256(commands).hexdigest()==plan['load_commands_sha256']
 segments=[];cursor=0
 for i in range(v[4]):
  cmd,size=struct.unpack_from('<II',commands,cursor);assert size>=8 and cursor+size<=len(commands)
  if cmd==0x19:
   name,va,vs,fo,fs,mp,ip,ns,sf=struct.unpack_from('<16sQQQQiiII',commands,cursor+8);segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip))
  cursor+=size
 assert cursor==len(commands)
 matched=[s for s in segments if s['vmaddr']<=START and START+72<=s['vmaddr']+min(s['filesize'],s['vmsize'])]
 assert matched==[plan['expected_segment']] and matched[0]['fileoff']+START-matched[0]['vmaddr']==plan['helper']['file_offset']
 test=predicate(text);oldtest=predicate(Path(delta['before']['path']).read_text())
 fixture=json.loads((HERE/'guard-fixtures.json').read_text());good=[dict(offset=START+4*i,size=4,type='mov',opcode='synthetic valid',bytes='00000000') for i in range(18)]
 results=[]
 for case in fixture['cases']:
  rows=copy.deepcopy(good);change=case['change']
  if 'row0' in change:rows[0].update(change['row0'])
  if 'allrows' in change:
   for r in rows:r.update(change['allrows'])
  if 'row0_remove' in change:rows[0].pop(change['row0_remove'])
  if 'row0_offset_delta' in change:rows[0]['offset']+=change['row0_offset_delta']
  if 'row_count' in change:
   rows=rows[:change['row_count']] if change['row_count']<18 else rows+[dict(good[-1],offset=START+72)]
  if 'cancel3_5' in change:rows[0]['bytes']='000000';rows[1]['bytes']='0000000000'
  accepted=accepts(test,rows,b'\0'*72);assert accepted==case['expected_accept'];results.append(accepted)
 # Historical legacy8/count-only16 results are carried explicitly, not rerun.
 carried=json.loads(Path(delta['historical_counterexample_provider']['path']).read_text())
 assert carried['result']['legacy8_accepts_cancel'] and carried['result']['legacy_countadapted16_accepts_cancel']
 parentrows=[dict(offset=START+4*i,size=4,type='mov',opcode='synthetic valid',bytes='00000000') for i in range(6)]
 assert accepts(oldtest,parentrows,b'\0'*24)
 parentrows[0]['bytes']='000000';parentrows[1]['bytes']='0000000000'
 assert not accepts(oldtest,parentrows,b'\0'*24)
 newrows=copy.deepcopy(good);newrows[0]['bytes']='000000';newrows[1]['bytes']='0000000000'
 assert not accepts(test,newrows,b'\0'*72)
 # Execute only the actual collector's isolated containment assertion on metadata.
 containment=[n.test for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Assert) and ast.unparse(n.test).startswith("int(plan['helper']['body_start']")]
 assert len(containment)==1
 for length,expected in [(72,True),(76,False)]:
  scope=dict(plan=plan,START=START,LENGTH=length,int=int)
  assert bool(eval(compile(ast.Expression(containment[0]),'<isolated-metadata-containment>','eval'),scope))==expected
 mutations=[('START=0x1021658b0','START=0x1021658b4'),('LENGTH=72','LENGTH=76'),("'pdj 18'","'pdj 17'"),("len(bytes.fromhex(r['bytes']))==4",'True'),("'-x','-f'","'-x'"),('child.communicate(timeout=30)','child.communicate(timeout=31)'),('if DEST.exists():','if False:')]
 for a,b in mutations:
  changed=text.replace(a,b,1);assert changed!=text
  try:source_guard(changed)
  except AssertionError:pass
  else:raise AssertionError('Unsafe source mutation accepted')
 seal=HERE/'manifest-preparation.json'
 if seal.exists():
  files=json.loads(seal.read_text())['files'];assert {r['path'] for r in files}=={p.name for p in HERE.iterdir() if p.is_file() and p!=seal}
  for r in files:
   got=ident(HERE/r['path']);assert (got['bytes'],got['sha256'])==(r['bytes'],r['sha256'])
 for p in HERE.iterdir():
  if p.is_file():
   s=p.read_text();assert s.endswith('\n') and all(l==l.rstrip() for l in s.splitlines())
 assert before==[ident(p) for p in paths]
 print(json.dumps(dict(status='PASS72B PREPARATION ONLY',fixtures=len(results),valid_controls=sum(results),rejections=len(results)-sum(results),historical_legacy_acceptances_carried=True,strengthened_parent6_rejects_cancel=True,strengthened_new18_rejects_cancel=True,containment_controls=2,source_mutation_rejections=len(mutations),watched=len(paths),unchanged=True,instruction_window_extracted=False,decoder_children=0,original_execution=False),indent=2))
if __name__=='__main__':main()
