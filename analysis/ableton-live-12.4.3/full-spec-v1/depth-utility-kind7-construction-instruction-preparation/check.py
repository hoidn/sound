"""Read-only preparation assertions; only isolated analyst row predicates on synthetic data."""
from pathlib import Path
import ast,copy,hashlib,json,struct,sys
HERE=Path(__file__).resolve().parent
DEST=HERE.with_name('depth-utility-kind7-construction-instruction-data')
START=0x102311b5c

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
 for s in ['START=0x102311b5c','LENGTH=64',"'pdj 16'",'len(decoded)==16',"len(bytes.fromhex(r['bytes']))==4", "str(r.get('type','')).strip().lower() not in ('invalid','ill')", "r['opcode'].strip().lower() not in ('','invalid','ill','none')", "if DEST.exists():", "'-NN','-n','-x','-f','-a','arm','-b','64'", 'child.communicate(timeout=30)', "assert START+LENGTH==0x102311b9c", "raw=f.read(LENGTH);assert len(raw)==LENGTH"]:assert s in text,s
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
 assert plan['helper']['va']=='0x102311b5c' and plan['helper']['length']==64 and plan['helper']['file_offset']==0x2311b5c
 assert plan['helper']['body_end_exclusive']=='0x102311ba4' and int(plan['helper']['body_end_exclusive'],16)>START+64
 assert plan['decoder_argv']==[plan['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(START),'-s',hex(START),'-q','-c','pdj 16',str(DEST/'construction-64.bin')]
 anchor=plan['source_anchor'];source=json.loads(Path(anchor['provider']['path']).read_text())['full_selected_record']
 assert source['path']==anchor['source_provider'] and source['line_1based']==anchor['line_1based'] and source['raw_sha256']==anchor['raw_sha256']
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
 matched=[s for s in segments if s['vmaddr']<=START and START+64<=s['vmaddr']+min(s['filesize'],s['vmsize'])]
 assert matched==[plan['expected_segment']] and matched[0]['fileoff']+START-matched[0]['vmaddr']==plan['helper']['file_offset']
 test=predicate(text);oldtest=predicate(Path(delta['before']['path']).read_text())
 fixture=json.loads((HERE/'guard-fixtures.json').read_text());good=[dict(offset=START+4*i,size=4,type='mov',opcode='synthetic valid',bytes='00000000') for i in range(16)]
 results=[]
 for case in fixture['cases']:
  rows=copy.deepcopy(good);change=case['change']
  if 'row0' in change:rows[0].update(change['row0'])
  if 'allrows' in change:
   for r in rows:r.update(change['allrows'])
  if 'row0_remove' in change:rows[0].pop(change['row0_remove'])
  if 'row0_offset_delta' in change:rows[0]['offset']+=change['row0_offset_delta']
  if 'row_count' in change:
   rows=rows[:change['row_count']] if change['row_count']<16 else rows+[dict(good[-1],offset=START+64)]
  if 'cancel3_5' in change:rows[0]['bytes']='000000';rows[1]['bytes']='0000000000'
  accepted=accepts(test,rows,b'\0'*64);assert accepted==case['expected_accept'];results.append(accepted)
 oldrows=copy.deepcopy(good[:8]);oldrows[0]['bytes']='000000';oldrows[1]['bytes']='0000000000'
 assert accepts(oldtest,oldrows,b'\0'*32)
 # Old predicate with ONLY row-count8->16 adaptation demonstrates same flaw at new count.
 old16=ast.parse(ast.unparse(oldtest).replace('len(decoded) == 8','len(decoded) == 16'),mode='eval').body
 counter=copy.deepcopy(good);counter[0]['bytes']='000000';counter[1]['bytes']='0000000000'
 assert accepts(old16,counter,b'\0'*64) and not accepts(test,counter,b'\0'*64)
 mutations=[('START=0x102311b5c','START=0x102311b60'),('LENGTH=64','LENGTH=68'),("'pdj 16'","'pdj 17'"),("len(bytes.fromhex(r['bytes']))==4",'True'),("'-x','-f'","'-x'"),('child.communicate(timeout=30)','child.communicate(timeout=31)'),('if DEST.exists():','if False:')]
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
 print(json.dumps(dict(status='PASS64B PREPARATION ONLY',fixtures=len(results),valid_controls=sum(results),rejections=len(results)-sum(results),old8_accepts_cancel=True,old_countadapted16_accepts_cancel=True,new16_rejects_cancel=True,source_mutation_rejections=len(mutations),watched=len(paths),unchanged=True,instruction_window_extracted=False,decoder_children=0,original_execution=False),indent=2))
if __name__=='__main__':main()
