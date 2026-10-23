#!/usr/bin/env python3
"""Finite retained-source reconciliation checks; --check writes nothing."""
from pathlib import Path
from html.parser import HTMLParser
import json, hashlib, sys, copy, subprocess
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def identity(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
class Extract(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.active=None;self.text=[];self.blocks=[];self.images=[];self.captions=[];self.links=[];self.headers=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in {'h3','h4','p','figcaption'}:
   assert self.active is None
   self.active=tag;self.text=[]
   if tag in {'h3','h4'}:self.headers.append({'tag':tag,'id':a.get('id'),'number':a.get('data-number')})
  if tag=='img':self.images.append(a)
  if tag=='a':self.links.append(a.get('href'))
 def handle_data(self,text):
  if self.active:self.text.append(text)
 def handle_endtag(self,tag):
  if tag==self.active:
   text=' '.join(''.join(self.text).split())
   if tag=='figcaption':self.captions.append(text)
   else:self.blocks.append({'tag':tag,'text':text})
   self.active=None;self.text=[]
def pointer(obj,p):
 for k in p.split('/')[1:]:obj=obj[int(k)] if isinstance(obj,list) else obj[k.replace('~1','/').replace('~0','~')]
 return obj
def reconcile(selected,ledger,owners,proposals):
 route=load(ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json')
 settings=load(ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/source-blocks.json')
 expected=[x for x in route if 27<=int(x['locator'][-3:])<=47]+[x for x in settings if 50<=int(x['id'][-3:])<=55]
 assert selected['blocks']==expected
 lookup={x.get('locator',x.get('id')):x for x in expected}
 assert len(ledger)==14 and {x['facet'] for x in ledger}=={'RS-F%02d'%i for i in range(1,15)}
 for x in ledger:assert x['source_quote'] in lookup[x['source_block']]['text'] and x['target_applicability']=='U'
 assert len(owners['references'])==11
 for x in owners['references']:
  item=pointer(load(ROOT/x['catalog']),x['pointer'])
  assert item['id']==x['id'] and item[x['quote_field']]==x['quoted_scoped_predicate']
 assert len(proposals['clauses'])==2 and len(proposals['cases'])==3
 for x in proposals['cases']:
  assert x['target_grade']=='U' and x['executed'] is False and x['source_claim_only'] is True
  for k in ['expected','comparison','documentary_expected','documentary_comparator']:assert x[k] is None
  assert set(x['source_blocks'])<=set(lookup)
 assert proposals['cases'][1]['finite_modes']==['Stop and Start','Start Only','Don’t Resync']
def run():
 assert sys.argv[1:] in [['--check'],['--seal']]
 sealing=sys.argv[1:] == ['--seal'];m=P/'manifest.json'
 if sealing:assert not m.exists(),'refuse overwrite sealed packet'
 else:assert m.exists()
 watch={q:sha(q) for q in P.iterdir() if q.is_file()}
 pins=load(P/'input-pins.json');assert len(pins)==22
 for x in pins:assert identity(ROOT/x['path'])=={k:x[k] for k in ['bytes','sha256']}
 external={ROOT/x['path']:sha(ROOT/x['path']) for x in pins}
 selected=load(P/'selected-source.json');ledger=load(P/'ledger.json');owners=load(P/'owner-reconciliation.json');proposals=load(P/'proposals.json')
 reconcile(selected,ledger,owners,proposals)
 context=load(P/'source-context.json');raw=(ROOT/context['raw_selection']['source_path']).read_text();sl=context['raw_selection'];frag=raw[sl['character_start']:sl['character_end_exclusive']]
 assert frag==(P/sl['file']).read_text()
 assert raw[:sl['character_start']].count('\n')+1==sl['html_line_start']
 parsed=Extract();parsed.feed(frag)
 expected=[{'tag':x['kind'],'text':x['text']} for x in selected['blocks'][:21]]
 assert parsed.blocks==expected
 assert {'tag':'h4','id':'sync','number':'17.3.1.2'} in parsed.headers
 assert len(parsed.images)==4 and len(parsed.captions)==4 and parsed.links==[]
 subsection=frag[frag.index('<h4 data-number="17.3.1.2"'):frag.index('<h4 data-number="17.3.1.3"')]
 assert 'preroll' not in subsection.lower() and 'pre-roll' not in subsection.lower()
 fixture=Extract();fixture.feed('<h4 id="sync" data-number="17.3.1.2">17.3.1.2 Sync</h4><p>Stop <em>and</em> Start.</p><figure><img src="not-fetched"><figcaption>Only a caption.</figcaption></figure>')
 assert fixture.blocks[-1]['text']=='Stop and Start.' and fixture.captions==['Only a caption.'] and len(fixture.images)==1
 # Meaningful mutation fixtures must fail before any seal operation.
 mutations=[]
 a=copy.deepcopy(ledger);a[0]['source_quote']='unpublished command';mutations.append((selected,a,owners,proposals))
 a=copy.deepcopy(owners);a['references'][0]['pointer']='/9999';mutations.append((selected,ledger,a,proposals))
 a=copy.deepcopy(proposals);a['cases'][1]['comparison']='invented timing pass';mutations.append((selected,ledger,owners,a))
 a=copy.deepcopy(ledger);a.pop();mutations.append((selected,a,owners,proposals))
 rejected=0
 for args in mutations:
  try:reconcile(*args)
  except (AssertionError,IndexError,KeyError):rejected+=1
 assert rejected==4
 # Consulted current canonicals must match the immutable as-of snapshots; no live wiki hash enters frozen input pins.
 for owner,spec in [('synchronization','spec-r2.md'),('routing-monitoring','spec-r1.md'),('remote-control-workflows','spec-r2.md')]:
  name={'synchronization':'synchronization-workflows','routing-monitoring':'routing-monitoring-latency','remote-control-workflows':'remote-control-workflows'}[owner]
  # This equality is contextual at initial seal only; replay stays on immutable snapshots.
  if sealing:assert (ROOT/'wiki/specs'/f'{name}.md').read_bytes()==(P.parent/owner/spec).read_bytes()
 for q in P.iterdir():
  if q.is_file() and q.suffix in {'.py','.json','.md','.txt'}:
   result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True)
   assert result.returncode in (0,1) and not result.stdout and not result.stderr,q
 if not sealing:
  manifest=load(m);assert set(manifest['files'])=={q.name for q in P.iterdir() if q.is_file() and q!=m}
  for n,x in manifest['files'].items():assert identity(P/n)==x
 assert watch=={q:sha(q) for q in watch} and external=={q:sha(q) for q in external}
 result={'status':'pass','scope':'finite retained source/quote/owner-pointer/proposal identity only','context_blocks':27,'selected_sync_source_blocks':10,'facets':14,'owner_references':11,'proposal_clauses':2,'future_cases':3,'input_pins':22,'images_uninspected':4,'captions_read':4,'links_in_selected_routing_fragment':0,'rejection_fixtures':4,'actual_outcomes':'allnull/U/unexecuted','target_parity':'unknown','runtime':False,'writes':sealing}
 if sealing:
  manifest={'id':'RESYNC-SOURCE-RECONCILIATION-R1','status':'partial source reconciliation awaiting independent review; no owner adoption','counts':result,'files':{q.name:identity(q) for q in sorted(P.iterdir()) if q.is_file()}}
  with m.open('x') as f:json.dump(manifest,f,ensure_ascii=False,indent=2);f.write('\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':run()
