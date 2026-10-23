"""Offline stdlib preparation controls; no collector main, loader or original call."""
from pathlib import Path
import ast,hashlib,json,re,sys
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
 source=(P/'capture-once.py').read_text();tree=ast.parse(source);fns={x.name:x for x in tree.body if isinstance(x,ast.FunctionDef)}
 assignments={x.targets[0].id:x.value for x in tree.body if isinstance(x,ast.Assign) and len(x.targets)==1 and isinstance(x.targets[0],ast.Name)}
 code=ast.literal_eval(assignments['CODE']);tokens=ast.literal_eval(assignments['TOKENS']);env=ast.literal_eval(assignments['ENV'])
 expected_code=[('0x104b8c760',13,'554889e54088b7cf0000005dc3'),('0x104b8c7b0',16,'0f57c080bfcf000000000f8577030000'),('0x104b8cb37',1,'c3')]
 expected_tokens=['--imports','dump','0x104b8c760','13','dump','0x104b8c7b0','16','dump','0x104b8cb37','1','call','0x104b8c760','buf:208','i:1','dump','b0','208','call','0x104b8c7b0','ref:b0','hex:0000803f000000c0','d:0x1p+0','dump','b0','208']
 assert code==expected_code and tokens==expected_tokens and tokens.count('call')==2 and tokens.count('dump')==5
 assert env==dict(PATH='/usr/bin:/bin',LANG='C',LC_ALL='C')==plan['environment']
 assert plan['argv']==[str(P.parent/'depth-utility-xexec-owned-build/xexec'),'/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64',*tokens]
 assert plan['timeout_seconds']==20 and plan['maximum_child_attempts']==1 and plan['maximum_selected_top_level_original_calls']==2
 assert ast.unparse(assignments['DEST'])=="BASE / 'depth-utility-xexec-mute-zero'" and ast.unparse(assignments['PRE'])=="BASE / 'depth-utility-xexec-mute-zero-preparation'"
 assert ast.unparse(assignments['BIN'])=="BASE / 'depth-utility-xexec-owned-build/xexec'"
 calls=[x for x in ast.walk(tree) if isinstance(x,ast.Call)]
 popen=[x for x in calls if isinstance(x.func,ast.Attribute) and x.func.attr=='Popen'];assert len(popen)==1 and ast.unparse(popen[0].args[0])=='argv'
 assert {x.arg:ast.unparse(x.value) for x in popen[0].keywords}==dict(cwd='DEST',env='ENV',stdin='subprocess.DEVNULL',stdout='subprocess.PIPE',stderr='subprocess.PIPE',preexec_fn='no_core',start_new_session='True')
 assert not any(isinstance(x.func,ast.Attribute) and x.func.attr in ('run','system','execv','execve') for x in calls)
 assert source.index("result['attempts']=1")<source.index('child=subprocess.Popen(')<source.index("result['returned_pid']=child.pid")
 assert 'communicate(timeout=20)' in source and 'DEST.mkdir()' in source and "open('x')" in source and "open('xb')" in source and "RLIMIT_CORE,(0,0)" in source
 # Only the complete new pure parser is evaluated; no imports/main/identity/Popen or old code.
 selected=ast.Module(body=[fns['parse_output']],type_ignores=[]);ns={'re':re,'CODE':code}
 assert not any(isinstance(x,ast.Attribute) and x.attr in ('open','write_text','write_bytes','Popen','system') for x in ast.walk(selected))
 exec(compile(selected,'<new-pure-output-parser>','exec'),ns);parse=ns['parse_output']
 state='00'*207+'01';fake=['loaded rebases=0 binds-linux=2 binds-trap=1 symbols=3','import linux _memcpy slots=1','import linux-data ___stack_chk_guard slots=1','import trap _unselected slots=1']
 fake += ['dump '+a+' '+a+' '+h for a,n,h in code]
 fake += ['call 0 0x104b8c760 rax=0x1 rdx=0x0 xmm0=0x0 xmm1=0x0','out b0 0x70000000 '+state,'dump b0 0x70000000 '+state,'call 1 0x104b8c7b0 rax=0x2 rdx=0x0 xmm0=0x0 xmm1=0x0','out b1 0x70000100 0000803f000000c0','dump b0 0x70000000 '+state]
 positive=parse('\n'.join(fake)+'\n','');assert positive['code_matches'] and positive['observations']['helper_low64_xmm0_zero']
 # Index is derived from known fixture order below, not a live capture.
 ci=next(i for i,line in enumerate(fake) if line.startswith('call 1 '));nonzero=fake.copy();nonzero[ci]=nonzero[ci].replace('xmm0=0x0','xmm0=0x3ff0000000000000')
 assert parse('\n'.join(nonzero)+'\n','')['observations']['helper_low64_xmm0_zero'] is False
 changed=fake.copy();changed[-1]=changed[-1][:-2]+'02';assert parse('\n'.join(changed)+'\n','')['observations']['helper_state_unchanged'] is False
 mismatch=fake.copy();mismatch[4]=mismatch[4][:-2]+'90';assert parse('\n'.join(mismatch)+'\n','')['code_matches'] is False
 bad=[]
 bad.append(('truncation',fake[:-1],''));bad.append(('trap',fake,'TRAP _unselected\n'));bad.append(('fault',fake,'FAULT sig=11 addr=(nil) rip=0x1\n'))
 q=fake.copy();q[1]=q[2];bad.append(('duplicate import',q,''))
 q=fake.copy();q[0]=q[0].replace('binds-linux=2','binds-linux=3');bad.append(('wrong import totals',q,''))
 q=fake.copy();q[4]=q[4][:-2];bad.append(('short code dump',q,''))
 q=fake.copy();q[4]=q[4].replace(' 0x104b8c760 ',' 0x104b8c761 ');bad.append(('wrong mapped address',q,''))
 q=fake.copy();q[ci]=q[ci].replace('0x104b8c7b0','0x104b8c7b1');bad.append(('wrong second call',q,''))
 q=fake.copy();q[ci]=q[ci].replace('xmm0=0x0','xmm0=0x10000000000000000');bad.append(('oversized register',q,''))
 q=fake.copy();q[-1]=q[-1].replace('0x70000000','0x70000010');bad.append(('changed state pointer',q,''))
 q=fake.copy();q[-2]=q[-2][:-2];bad.append(('short input buffer',q,''))
 q=fake.copy();q[-2]=q[-2].replace('0x70000100','0x70000000');bad.append(('overlap buffers',q,''))
 bad.append(('third call',fake+[fake[ci]],''));bad.append(('unknown used symbol',fake+['used _unknown 1'],''));bad.append(('trap used count',fake+['used _unselected 1'],''))
 rejected=[]
 for name,lines,stderr in bad:
  try:parse('\n'.join(lines)+'\n',stderr)
  except ValueError:rejected.append(name)
  else:raise AssertionError(name)
 if (P/'manifest.json').exists():
  manifest=json.loads((P/'manifest.json').read_text());assert {r['path'] for r in manifest['files']}=={q.name for q in P.iterdir() if q.is_file() and q.name!='manifest.json'}
  for row in manifest['files']:
   got=identity(P/row['path']);assert (got['bytes'],got['sha256'])==(row['bytes'],row['sha256'])
 after=[identity(p) for p in sorted(watched)];assert before==after
 print(json.dumps(dict(status='PASS PREPARATION ONLY',pins=len(inputs['pins']),watched=len(watched),unchanged=True,synthetic_positive=1,nonzero_result_and_changed_state_retained=2,posthoc_code_mismatch_detected=True,parser_rejections=rejected,collector_or_loader_or_original_execution=False),indent=2))
if __name__=='__main__':main()
