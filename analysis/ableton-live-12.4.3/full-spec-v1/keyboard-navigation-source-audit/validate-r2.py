"""Read-only narrow successor check; historical code/data stay byte-identical."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import contextlib,io,json,subprocess
P=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def tree():return {str(p.relative_to(P)):digest(p) for p in P.rglob('*') if p.is_file()}
def check_pin(p,r):assert digest(p)=={k:r[k] for k in ['bytes','sha256']},str(p)

def successor(old):
 rows=deepcopy(old)
 for i in range(287,292):
  r=rows[i];assert r['binding']['id']==f'BIND-T27-R{i-286:03}' and r['explicit_context_blocks']==['KN2:B350','KN2:B351']
  general=dict(block='KN2:B351',catalog='source-blocks.json',json_pointer='/502',role='general single-letter-plus-Shift context; not a proved prerequisite or forced modifier for this row')
  if i<290:
   r['explicit_context_blocks']=[]
   r['context_scope']='No per-row prerequisite inferred from adjacent B350 or general B351. Empty list does not assert unconditional dispatch; other contexts remain U.'
   r['related_context_blocks']=[dict(block='KN2:B350',catalog='source-blocks.json',json_pointer='/501',role='adjacent enabled Computer MIDI playable-note/octave/velocity explanation; not a prerequisite for this toggle'),general]
  else:
   r['explicit_context_blocks']=['KN2:B350']
   r['context_scope']='B350 supplies supported enabled Computer MIDI octave/velocity use context. B351 is general related text, not a row-specific modifier or precondition. Actual dispatch and full prerequisites remain U.'
   r['related_context_blocks']=[general]
 return rows

def delta(before,after,path=''):
 if before==after:return []
 if isinstance(before,dict) and isinstance(after,dict):
  out=[]
  for k in sorted(before.keys()|after.keys()):
   q=path+'/'+k
   if k not in before:out.append(dict(pointer=q,operation='add',before_present=False,after=after[k]))
   elif k not in after:out.append(dict(pointer=q,operation='remove',before=before[k],after_present=False))
   else:out.extend(delta(before[k],after[k],q))
  return out
 if isinstance(before,list) and isinstance(after,list) and len(before)==len(after):
  return [x for i,(a,b) in enumerate(zip(before,after)) for x in delta(a,b,path+'/'+str(i))]
 return [dict(pointer=path,operation='replace',before=before,after=after)]

def check_roles(rows):
 assert len(rows)==292
 for i in range(287,292):
  r=rows[i];assert r['explicit_context_blocks']==([] if i<290 else ['KN2:B350'])
  assert 'KN2:B351' not in r['explicit_context_blocks']
  related=r['related_context_blocks'];assert [x['block'] for x in related]==(['KN2:B350','KN2:B351'] if i<290 else ['KN2:B351'])
  assert all('not a' in x['role'] for x in related)
  for x in related:
   b=load(P/x['catalog'])[int(x['json_pointer'][1:])];assert b['id']==x['block']
  assert r['normative_command_contract'] is r['command_owner_reconciled'] is r['dispatch_tested'] is r['complete'] is False
  assert r['target']=='U' and r['actual_expected'] is r['actual_comparison'] is None

def main():
 before=tree();history=load(P/'r1-preservation.json');assert len(history['files'])==21
 for name,r in history['files'].items():check_pin(P/name,r)
 assert digest(P/'manifest.json')['sha256']=='e30f1ccd14b34ce7d47de94228b51f1c7a4939fa77c0e832565baba1d5fdce1a'
 check_pin(P/history['review']['copy'],history['review']);check_pin(Path(history['review']['source']),history['review'])
 assert history['review']['sha256']=='cdca5739615d9ccc8828ce9f9c8b680f9aec6248a320f986dc06f05ba210d829'
 review=load(P/'review-r1.json');assert [f['id'] for f in review['findings']]==['KNA-REVIEW-001']
 # Only the obsolete exact inventory comparison changes in memory. All R1 data,
 # derivation, pins, fixtures and source checks are replayed against original paths.
 code=(P/'validate.py').read_text();needle="==set(mf['files'])";assert code.count(needle)==1
 code=code.replace(needle,">=set(mf['files'])")
 ns={'__file__':str(P/'validate.py'),'__name__':'historical_r1_integrity_only'}
 exec(compile(code,str(P/'validate.py')+' [in-memory inventory adaptation]','exec'),ns)
 capture=io.StringIO()
 with contextlib.redirect_stdout(capture):ns['main']()
 old_report=json.loads(capture.getvalue());assert old_report['status']=='pass' and old_report['writes'] is False
 old=load(P/'binding-reconciliation.json');new=load(P/'binding-reconciliation-r2.json');assert new==successor(old)
 changes=delta(old,new);assert changes==load(P/'delta-r2.json') and len(changes)==15
 expected={f'/{i}/{key}' for i in range(287,292) for key in ['explicit_context_blocks','context_scope','related_context_blocks']}
 assert {c['pointer'] for c in changes}==expected and new[:287]==old[:287]
 check_roles(new);assert [x['binding'] for x in new]==[x['binding'] for x in old]
 fixtures=load(P/'fixtures-r2.json');assert fixtures['toggle_rows']==[287,288,289] and fixtures['enabled_range_rows']==[290,291]
 mutations=0
 for kind,indices in [('wrong-toggle-enabled',fixtures['toggle_rows']),('wrong-general-prerequisite',range(287,292)),('remove-range-enabled',fixtures['enabled_range_rows'])]:
  for i in indices:
   x=deepcopy(new)
   if kind=='wrong-toggle-enabled':x[i]['explicit_context_blocks']=['KN2:B350']
   elif kind=='wrong-general-prerequisite':x[i]['explicit_context_blocks'].append('KN2:B351')
   else:x[i]['explicit_context_blocks']=[]
   try:check_roles(x)
   except AssertionError:mutations+=1
   else:raise AssertionError('wrong association was accepted: '+kind)
 assert mutations==10
 response=load(P/'response-r2.json');assert response['field_delta_count']==15 and response['review_sha256']==history['review']['sha256']
 assert response['unchanged_counts']==dict(source_blocks=541,claims=641,bindings=292,requirements=21,cases=42,proposal_groups=23,complete_topics=0)
 for p in P.rglob('*'):
  if p.is_file() and 'canonical-snapshots' not in p.relative_to(P).parts:
   r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True);assert r.returncode in (0,1) and not r.stdout and not r.stderr,(p,r.stdout,r.stderr)
 sealed=(P/'manifest-author-r2.json').exists()
 if sealed:
  mf=load(P/'manifest-author-r2.json');assert set(tree())-{'manifest-author-r2.json'}==set(mf['files'])
  for name,r in mf['files'].items():check_pin(P/name,r)
 assert tree()==before,'readonly successor checker mutated files'
 for name,r in history['files'].items():check_pin(P/name,r)
 print(json.dumps(dict(status='pass',sealed=sealed,scope='focused source-association correction; independent re-review pending',historical_r1_files=21,exact_review_copy=True,original_input_pins=110,changed_rows=5,field_deltas=15,unchanged_rows=287,association_negative_mutations=mutations,range_enabled_context_retained=2,old_integrity_fixtures=4,source_blocks=541,claims=641,bindings=292,requirements=21,cases=42,proposal_groups=23,all_target_U=True,complete_topics=0,writes=False,runtime=False),indent=2))
if __name__=='__main__':main()
