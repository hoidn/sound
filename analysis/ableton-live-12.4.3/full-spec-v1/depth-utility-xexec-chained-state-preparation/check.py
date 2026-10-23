"""Offline stdlib checks on fixed protocol/synthetic text; no collector/loader/original run."""
from pathlib import Path
import ast,copy,hashlib,json,re,sys
P=Path(__file__).resolve().parent

def identity(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())

def main():
 if sys.argv[1:]!=['--check']:raise SystemExit('REFUSED: offline --check only')
 inputs=json.loads((P/'inputs.json').read_text());plan=json.loads((P/'plan.json').read_text())
 watched={Path(r['path']) for r in inputs['pins']}|{p for p in P.iterdir() if p.is_file()}
 before=[identity(p) for p in sorted(watched)]
 for row in inputs['pins']:assert identity(Path(row['path']))==row
 assert not Path(plan['destination']).exists() and not Path(plan['destination']).is_symlink()
 source=(P/'capture-once.py').read_text();tree=ast.parse(source)
 functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 assignments={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
 code=ast.literal_eval(assignments['CODE']);tokens=ast.literal_eval(assignments['TOKENS']);env=ast.literal_eval(assignments['ENV'])
 state=bytearray(208)
 for offset,h in [(0,'0000803f0000803f'),(0x38,'0000803f00000000'),(0x78,'0000803f0000803f'),(0x80,'0000003f0000803e'),(0xc8,'01000000')]:state[offset:offset+len(bytes.fromhex(h))]=bytes.fromhex(h)
 assert plan['initial_state']['hex']==state.hex() and len(state)==208 and state[0xcc:0xd0]==bytes(4)
 helper=(P.parent/'depth-utility-x86-process-span/process-span-904.bin').read_bytes()+(P.parent/'depth-utility-x86-mode-table-data/mode-table-16.bin').read_bytes()
 assert len(helper)==920
 expected_code=[('0x104b8c760',13,'554889e54088b7cf0000005dc3'),('0x104b8c7b0',920,helper.hex())]
 expected_tokens=['--imports','dump','0x104b8c760','13','dump','0x104b8c7b0','920','call','0x104b8c7b0','hex:'+state.hex(),'hex:0000803f000000c0','d:0x1p+0','dump','b0','208','call','0x104b8c7b0','ref:b0','ref:b1','d:0x1p+0','dump','b0','208','call','0x104b8c760','ref:b0','i:1','dump','b0','208','call','0x104b8c7b0','ref:b0','ref:b1','d:0x1p+0','dump','b0','208','dump','b1','8']
 assert code==expected_code and tokens==expected_tokens and tokens.count('call')==4 and tokens.count('dump')==7
 assert env==dict(PATH='/usr/bin:/bin',LANG='C',LC_ALL='C')==plan['environment']
 assert plan['argv']==[str(P.parent/'depth-utility-xexec-owned-build/xexec'),'/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64',*tokens]
 assert plan['timeout_seconds']==20 and plan['maximum_child_attempts']==1 and plan['maximum_selected_top_level_original_calls']==4
 assert ast.unparse(assignments['PRE'])=="BASE / 'depth-utility-xexec-chained-state-preparation'" and ast.unparse(assignments['DEST'])=="BASE / 'depth-utility-xexec-chained-state'"
 assert ast.unparse(assignments['BIN'])=="BASE / 'depth-utility-xexec-owned-build/xexec'"
 calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call)]
 popen=[n for n in calls if isinstance(n.func,ast.Attribute) and n.func.attr=='Popen'];assert len(popen)==1 and ast.unparse(popen[0].args[0])=='argv'
 assert {n.arg:ast.unparse(n.value) for n in popen[0].keywords}==dict(cwd='DEST',env='ENV',stdin='subprocess.DEVNULL',stdout='subprocess.PIPE',stderr='subprocess.PIPE',preexec_fn='no_core',start_new_session='True')
 assert not any(isinstance(n.func,ast.Attribute) and n.func.attr in ('run','system','execv','execve') for n in calls)
 assert source.index("result['attempts']=1")<source.index('child=subprocess.Popen(')<source.index("result['returned_pid']=child.pid")
 for token in ['communicate(timeout=20)',"RLIMIT_CORE,(0,0)",'DEST.mkdir()',"open('x')","open('xb')",'maximum_selected_top_level_original_calls=4',"rb'^call ([0-3])"]:assert token in source
 # Only the complete inspected pure new parser is compiled; no collector import/main.
 selected=ast.Module(body=[functions['parse_output']],type_ignores=[])
 assert not any(isinstance(n,ast.Attribute) and n.attr in ('open','write_text','write_bytes','Popen','system') for n in ast.walk(selected))
 ns={'re':re,'CODE':code};exec(compile(selected,'<new-pure-fixed-history-parser>','exec'),ns);parse=ns['parse_output']
 # Fixed synthetic hypothesis encodings are test text, not new math/original measurements.
 s0=bytearray(state);s0[0x48:0x50]=(1).to_bytes(8,'little');s0[0x88:0x90]=(1).to_bytes(8,'little');s0[0x78:0x80]=bytes.fromhex('0000c03f0000a03f')
 s1=bytearray(s0);s1[0x48:0x50]=(2).to_bytes(8,'little');s1[0x88:0x90]=(2).to_bytes(8,'little');s1[0x78:0x80]=bytes.fromhex('000000400000c03f')
 s2=bytearray(s1);s2[0xcf]=1
 fake=['loaded rebases=0 binds-linux=2 binds-trap=1 symbols=3','import linux _memcpy slots=1','import linux-data ___stack_chk_guard slots=1','import trap _unselected slots=1']
 fake+=['dump '+a+' '+a+' '+h for a,n,h in code]
 def returned(i,a,x):return f'call {i} {a} rax=0x8 rdx=0x0 xmm0={x} xmm1=0x0'
 fake += [returned(0,'0x104b8c7b0','0xc00000003f800000'),'out b0 0x70000000 '+s0.hex(),'out b1 0x70000100 0000803f000000c0','dump b0 0x70000000 '+s0.hex(),returned(1,'0x104b8c7b0','0xc02000003fc00000'),'dump b0 0x70000000 '+s1.hex(),returned(2,'0x104b8c760','0x0'),'dump b0 0x70000000 '+s2.hex(),returned(3,'0x104b8c7b0','0x0'),'dump b0 0x70000000 '+s2.hex(),'dump b1 0x70000100 0000803f000000c0']
 positive=parse('\n'.join(fake)+'\n','');assert positive['completed_original_call_rows']==4 and positive['code_matches'] and positive['actual_expected'] is None and positive['comparison'] is None and positive['new_grade']==0
 assert [s['counter48_u64'] for s in positive['states_after_each_call']]==[1,2,2,2]
 ci=[i for i,line in enumerate(fake) if line.startswith('call ')];si=[i for i,line in enumerate(fake) if line.startswith('dump b0 ')];ii=len(fake)-1
 retained=[]
 q=fake.copy();q[ci[3]]=q[ci[3]].replace('xmm0=0x0','xmm0=0x1234');assert parse('\n'.join(q)+'\n','')['observations']['final_helper_low64_xmm0_zero'] is False;retained.append('nonzero final return')
 q=fake.copy();q[si[1]]=q[si[1]][:-2]+'7f';assert parse('\n'.join(q)+'\n','')['states_after_each_call'][1]['flag_cf_u8']==127;retained.append('unexpected intermediate state')
 q=fake.copy();q[si[0]]=q[si[0]][:-2]+'02';assert parse('\n'.join(q)+'\n','')['observations']['automatic_vs_explicit_state0_equal'] is False;retained.append('automatic-explicit state difference')
 q=fake.copy();q[ii]='dump b1 0x70000100 0000000000000000';assert parse('\n'.join(q)+'\n','')['observations']['input_after_history_unchanged'] is False;retained.append('changed input')
 q=fake.copy();q[4]=q[4][:-2]+'90';assert parse('\n'.join(q)+'\n','')['code_matches'] is False
 bad=[('truncation',fake[:-1],''),('trap',fake,'TRAP _unselected\n'),('fault',fake,'FAULT sig=11 addr=(nil) rip=0x1\n')]
 q=fake.copy();q[1]=q[2];bad.append(('duplicate import',q,''))
 q=fake.copy();q[0]=q[0].replace('binds-linux=2','binds-linux=3');bad.append(('wrong import totals',q,''))
 q=fake.copy();q[4]=q[4][:-2];bad.append(('short setter dump',q,''))
 q=fake.copy();q[5]=q[5][:-2];bad.append(('short helper920 dump',q,''))
 q=fake.copy();q[4]=q[4].replace(' 0x104b8c760 ',' 0x104b8c761 ');bad.append(('wrong mapped address',q,''))
 for k in range(4):
  q=fake.copy();q[ci[k]]=q[ci[k]].replace('0x104b8c7b0' if k!=2 else '0x104b8c760','0x104b8c7b1');bad.append(('wrong call'+str(k),q,''))
 q=fake.copy();q[ci[1]]=q[ci[1]].replace('call 1 ','call 2 ');bad.append(('reordered call index',q,''))
 q=fake.copy();q[ci[3]]=q[ci[3]].replace('xmm0=0x0','xmm0=0x10000000000000000');bad.append(('oversized register',q,''))
 q=fake.copy();q[si[3]]=q[si[3]].replace('0x70000000','0x70000010');bad.append(('changed state pointer',q,''))
 q=fake.copy();q[si[2]]=q[si[2]][:-2];bad.append(('short state',q,''))
 q=fake.copy();q[ii]=q[ii][:-2];bad.append(('short input',q,''))
 q=fake.copy();q[ii]=q[ii].replace('0x70000100','0x70000110');bad.append(('changed input pointer',q,''))
 q=fake.copy();q[8]=q[8].replace('0x70000100','0x70000000');bad.append(('overlap buffers',q,''))
 q=fake.copy();del q[8];bad.append(('missing automatic input',q,''))
 bad += [('fifth call',fake+[returned(4,'0x104b8c7b0','0x0')],''),('unknown used symbol',fake+['used _unknown 1'],''),('trap used',fake+['used _unselected 1'],'')]
 rejected=[]
 for name,lines,stderr in bad:
  try:parse('\n'.join(lines)+'\n',stderr)
  except ValueError:rejected.append(name)
  else:raise AssertionError(name)
 if (P/'delta.json').exists():
  for f in json.loads((P/'delta.json').read_text())['files']:
   assert identity(Path(f['before']['path']))==f['before'] and identity(Path(f['after']['path']))==f['after']
   lines=Path(f['before']['path']).read_text().splitlines(keepends=True)
   for e in reversed(f['edits']):
    a,z=e['old_line_start_zero'],e['old_line_end_exclusive'];assert hashlib.sha256(''.join(lines[a:z]).encode()).hexdigest()==e['old_text_sha256'];lines[a:z]=e['replacement'].splitlines(keepends=True)
   assert ''.join(lines)==Path(f['after']['path']).read_text()
 if (P/'manifest.json').exists():
  manifest=json.loads((P/'manifest.json').read_text());assert {r['path'] for r in manifest['files']}=={q.name for q in P.iterdir() if q.is_file() and q.name!='manifest.json'}
  for row in manifest['files']:
   got=identity(P/row['path']);assert (got['bytes'],got['sha256'])==(row['bytes'],row['sha256'])
 assert before==[identity(p) for p in sorted(watched)]
 print(json.dumps(dict(status='PASS PREPARATION ONLY',pins=len(inputs['pins']),watched=len(watched),unchanged=True,synthetic_positive=1,counterevidence_retained=retained,posthoc_code_mismatch_detected=True,parser_rejections=rejected,collector_or_loader_or_original_execution=False),indent=2))
if __name__=='__main__':main()
