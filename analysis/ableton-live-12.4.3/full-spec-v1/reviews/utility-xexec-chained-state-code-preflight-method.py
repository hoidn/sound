from pathlib import Path
import ast,hashlib,json,re,struct,subprocess,sys,copy,datetime
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-utility-xexec-chained-state-preparation'
def identity(p):
 r=p.read_bytes();return dict(path=str(p),bytes=len(r),sha256=hashlib.sha256(r).hexdigest())
inputs=json.loads((P/'inputs.json').read_text());delta=json.loads((P/'delta.json').read_text());plan=json.loads((P/'plan.json').read_text());seal=json.loads((P/'manifest.json').read_text());paths=sorted({Path(x['path']) for x in inputs['pins']}|set(P.iterdir()));before=[identity(p) for p in paths]
assert identity(P/'manifest.json')['sha256']=='1d1e0a5530f6b31dd37892ffddfd68c92d5f5aacb65b660b2d0f7fa8b74e3ab3'
assert {x['path'] for x in seal['files']}=={p.name for p in P.iterdir() if p.name!='manifest.json'}
for x in seal['files']:
 g=identity(P/x['path']);assert(g['bytes'],g['sha256'])==(x['bytes'],x['sha256'])
for x in inputs['pins']+delta['parent_files']:assert identity(Path(x['path']))==x
reconstructed=[]
for f in delta['files']:
 for k in ('before','after'):assert identity(Path(f[k]['path']))==f[k]
 ls=Path(f['before']['path']).read_text().splitlines(keepends=True)
 for e in reversed(f['edits']):
  a,z=e['old_line_start_zero'],e['old_line_end_exclusive'];assert hashlib.sha256(''.join(ls[a:z]).encode()).hexdigest()==e['old_text_sha256'];ls[a:z]=e['replacement'].splitlines(keepends=True)
 assert ''.join(ls)==Path(f['after']['path']).read_text();reconstructed.append(dict(path=f['after']['path'],edits=len(f['edits'])))
s=(P/'capture-once.py').read_text();t=ast.parse(s);assign={n.targets[0].id:n.value for n in t.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)};fn={n.name:n for n in t.body if isinstance(n,ast.FunctionDef)};code=ast.literal_eval(assign['CODE']);tokens=ast.literal_eval(assign['TOKENS'])
state=bytearray(208)
for off,v in [(0,(1.,1.)),(0x38,(1.,0.)),(0x78,(1.,1.)),(0x80,(.5,.25))]:state[off:off+8]=struct.pack('<ff',*v)
state[0xc8:0xcc]=struct.pack('<I',1)
expected=['--imports','dump','0x104b8c760','13','dump','0x104b8c7b0','920','call','0x104b8c7b0','hex:'+state.hex(),'hex:0000803f000000c0','d:0x1p+0','dump','b0','208','call','0x104b8c7b0','ref:b0','ref:b1','d:0x1p+0','dump','b0','208','call','0x104b8c760','ref:b0','i:1','dump','b0','208','call','0x104b8c7b0','ref:b0','ref:b1','d:0x1p+0','dump','b0','208','dump','b1','8']
assert tokens==expected and plan['argv'][2:]==expected and plan['initial_state']['hex']==state.hex();assert len(state)==208
assert code[0]==('0x104b8c760',13,'554889e54088b7cf0000005dc3')
a=(B/'depth-utility-x86-process-span/process-span-904.bin').read_bytes();b=(B/'depth-utility-x86-mode-table-data/mode-table-16.bin').read_bytes();assert code[1]==('0x104b8c7b0',920,(a+b).hex())
# Only the already fully read current pure parser is instantiated; no collector globals/import/main.
selected=ast.Module(body=[fn['parse_output']],type_ignores=[])
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('open','Popen','write_bytes','write_text') for n in ast.walk(selected))
ns={'re':re,'CODE':code};exec(compile(selected,'<review-current-pure-parser>','exec'),ns);parse=ns['parse_output']
# Deliberately use unknown-looking state and non-hypothesis return words, not predicted numerical values.
rows=['loaded rebases=0 binds-linux=0 binds-trap=0 symbols=0']+['dump '+a+' '+a+' '+h for a,n,h in code]
state0=bytes([0xa5])*208;inp='0123456789abcdef'
def call(i,a):return f'call {i} {a} rax=0xffff rdx=0x1 xmm0=0xffffffffffffffff xmm1=0x1234'
rows +=[call(0,'0x104b8c7b0'),'out b0 0x1000 '+state0.hex(),'out b1 0x2000 '+inp]
for i,a in [(0,None),(1,'0x104b8c7b0'),(2,'0x104b8c760'),(3,'0x104b8c7b0')]:
 if a:rows.append(call(i,a))
 rows.append('dump b0 0x1000 '+bytes([i+1]).hex()*208)
rows+=['dump b1 0x2000 fedcba9876543210'];base='\n'.join(rows)+'\n';v=parse(base,'');assert len(v['calls'])==4 and all(x['xmm0']=='0xffffffffffffffff' for x in v['calls']);assert not any(v['observations'].values());assert all(x['hex']==bytes([i+1]).hex()*208 for i,x in enumerate(v['states_after_each_call']));assert v['new_grade']==0 and v['actual_expected'] is None and v['comparison'] is None
q=rows.copy();q[1]=q[1][:-2]+'90';assert parse('\n'.join(q)+'\n','')['code_matches'] is False
bad=[rows[:-1],rows+[call(4,'0x104b8c7b0')],rows[:-1]+['dump b1 0x2010 '+inp]]
for q in bad:
 try:parse('\n'.join(q)+'\n','')
 except ValueError:pass
 else:raise AssertionError('own malformed control accepted')
r=subprocess.run([sys.executable,'-B',str(P/'check.py'),'--check'],capture_output=True,text=True);assert r.returncode==0,(r.stdout,r.stderr)
f=subprocess.run([sys.executable,'-B',str(P/'check.py'),'--write'],capture_output=True,text=True);assert f.returncode==1
assert before==[identity(p) for p in paths]
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS independent data-only code/method checks',current_manifest=identity(P/'manifest.json'),reconstruction=reconstructed,pins=len(inputs['pins']),preserved_parent_files=len(delta['parent_files']),inventory_payloads=len(seal['files']),own_parser_controls=dict(nonhypothesis_all_four_returns_and_states_retained=True,changed_input_and_automatic_explicit_difference_retained=True,code_mismatch_retained_false=True,malformed_rejected=3),selected_checker=json.loads(r.stdout),write_refusal=dict(exit=f.returncode,stderr=f.stderr),before=before,after=[identity(p) for p in paths],unchanged=True,collector_loader_original_execution=False)
p=B/'reviews/utility-xexec-chained-state-code-preflight-evidence.json'
with p.open('x') as h:json.dump(out,h,indent=2);h.write('\n')
print(json.dumps(dict(evidence=identity(p),checks=out['selected_checker'],watch=len(paths),own_controls=out['own_parser_controls']),indent=2))
