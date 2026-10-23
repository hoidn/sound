"""Bounded manual semantic ledger; only retained text/data, no application calls.
Hand-selected span boundaries and sufficiency judgments are audit proposals.
--check is read-only; --write is refused once manifest-author-r1.json exists.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from html.parser import HTMLParser
import json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];S=P.parent/'synchronization'
load=lambda q:json.loads(q.read_text())
def digest(q):
 b=q.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(q,role):return dict(path=str(q.relative_to(ROOT)),role=role,**digest(q))
def rid(x):return f'REQ-SYNC-WORKFLOW-{x:03}' if isinstance(x,int) else 'REQ-SYNC-WORKFLOW-'+x
def cid(x):return f'SYNC-{x:03}' if isinstance(x,int) else 'SYNC-'+x
R='represented-partial-source-clause-and-case'
U='documented-but-outcome-U'
G='missing-clause-case-or-context'
M='research-only-protocol-private-or-marketing'
E='editorial'
I='image-or-link-uninspected'
# Each first marker is empty (start of paragraph); subsequent exact markers define
# nonoverlapping source spans. No automatic sentence/title matching or inherited mapping.
# marker, disposition, sufficient requirement IDs, sufficient case IDs, judgment, optional gap.
PLAN={
2:[('',M,[],[],'Overview use contexts; not an exhaustive hardware/product compatibility promise.'),
 ('Ableton Link allows',U,[3],[3],'Tempo/timing role; peer fixture required, all actual timing outcomes U.'),
 ('and Link Audio',U,[9,10],[9,10],'Streaming role; exact-build Audio capability unproven.'),
 ('You can use Tempo Follower',U,[11],[11],'Audio-driven tempo role only, no detector equation.'),
 ('or use MIDI Sync',U,[15,16],[15,16],'External sender/receiver overview; MTC restriction preserved below.')],
4:[('',U,[3],[3],'Beat/tempo/phase and network role only; no distributed-clock implementation.'),
 ('Link Audio extends',U,[10],[10],'Peer streaming role; real-time is not a numerical deadline.'),
 ('without additional hardware',M,[],[],'Convenience claim; not absence of interface/network requirements or a complexity/latency benchmark.')],
5:[('',M,[],[],'All-products/growing third-party availability is broad current marketing, not exact product/firmware enumeration.'),
 ('Any participant',U,[3,4],[4],'Independent transport role; case004 contrasts disabled shared-start option after a paired baseline.'),
 ('and remain in time',U,[3],[3],'Phase continuity role; source prose supplies no measurable tolerance.'),
 ('with playback following',U,[3],[3],'Global launch quantization context; existing finite launch owner not extended across a network.'),
 ('Any participant can adjust',U,[2],[2],'Peer tempo changes; case002 includes each peer and automation contexts.'),
 ('Participants can join',G,[],[],'Remaining-peer continuity is not a clause. Two-peer leave/rejoin cannot observe a surviving synchronized pair.','SA-G01')],
6:[('',U,[14],[14],'Coexistence of Link with Follower or MIDI; separate baselines, not simultaneous-source arbitration.'),
 ('In both cases',U,[14],[14],'External input supplies Link-session tempo; no priority/convergence law.')],
8:[('',R,[5],[5],'Dedicated Link tab is explicitly inspected.')],
9:[('',G,[5],[],'Contract acknowledges a documentary default but case005 explicitly sets visibility; no untouched-preference/default observation.','SA-G02'),
 ('but if you',R,[5],[5],'Show Link Toggle Hide and restore are explicitly proposed; default is separate.')],
10:[('',G,[5],[],'Adjacent menu on/off predicates are contracted, but case005 only uses Configure Link and visibility settings.','SA-G03'),
 ('It also includes a list',G,[5],[],'Menu lists connected Audio-enabled peers; existing case only has a known audio peer, no list inspection/filter contrast.','SA-G04'),
 ('as well as',R,[5],[5],'Configure Link opening the settings tab is explicitly proposed.')],
11:[('',U,[4],[4],'Shared start/stop with option enabled; transport outputs remain null.'),
 ('Note that',U,[4],[4],'Receiving-peer option gating is explicitly varied; not network delivery/enforcement proof.')],
12:[('',E,[],[],'Settings-section transition supplies context for following Link Audio controls.')],
13:[('',R,[6],[6],'Audio enable/disable is varied, with known capabilities and nonzero output.'),
 ('Note that',R,[6],[6],'Link-enabled prerequisite is separately varied; actual streaming remains U.')],
14:[('',R,[6],[6],'Distinct supplied names and remote display are proposed, without codec/collision assumptions.')],
15:[('',R,[7],[7],'Named latency slider/control role and accepted supplied values; exact UI geometry/range not established.'),
 ('As the latency',R,[7],[7],'Inspect peer buffer display while changing latency; no sample/buffer formula.')],
16:[('',U,[8],[8],'Incoming monitored audio/local clips alignment is prose-only; paired audible paths required.'),
 ('This is achieved',U,[8],[8],'Documentary playback-delay role is not a numeric implementation law.'),
 ('Note this option',U,[8],[8],'One-participant guidance; both-enabled behavior has separate U-AUDIO probe, not a failure oracle.')],
17:[('',R,[7],[7],'Peer-list/status/buffer roles are inspected with known peers; not a complete interoperability/count detector proof.')],
19:[('',R,[1],[1],'Same-network prerequisite and admitted peers; no discovery/interface-selection implementation.'),
 ('You can use',R,[1],[1],'Wired/wireless source contexts preserved; no stability or Wi-Fi performance threshold.'),
 ('Then, click',R,[1],[1],'Control Bar enable action is explicit.'),
 ('Live will automatically',R,[1],[1],'Session start/join is a documentary control/state proposal, never a network result.')],
20:[('',R,[1],[1],'Peer-count display inspected; count is not synchronization proof.')],
21:[('',U,[3],[3],'Other-peer and stopped-transport context retained before progress inspection.'),
 ('The progress bar',U,[3],[3],'Global-quantization relation is a source role, not phase arithmetic.'),
 ('After you trigger',U,[3],[3],'Interior-phase playback requests proposed; no wait duration or scheduler oracle.')],
22:[('',G,[2],[],'Initial-tempo predicate is contracted, but case002 begins with an already working two-peer session.','SA-G05'),
 ('Any peer can then',U,[2],[2],'Each-peer tempo changes explicitly varied.'),
 ('If multiple participants',U,[2],[2],'Simultaneous-change source role; ordered-event prerequisite retained, no causal-last algorithm.'),
 ('Tempo changes made',U,[2],[2],'Peer override of active Set automation explicitly contrasted.')],
23:[('',U,[24],[24],'Link-enabled recording count-in boundary; positive eligible count-in with Link off first; recording owner retained.')],
24:[('',M,[],[],'Reliability/most-scenarios language is marketing, not a benchmark or compatibility outcome.'),
 ('If you run',I,[],[],'FAQ referral only; linked target was not opened or inspected in this audit.')],
26:[('',U,[6,9,10],[6,9,10],'Network/peer streaming role; real time does not set latency tolerance, target Audio existence U.'),
 ('This makes',U,[9],[9],'Monitor/record roles are delegated to existing gates, not new audio or storage laws.'),
 ('To use Link Audio',R,[6],[6],'Both features enabled at all participating streaming peers; no arbitrary-peer matrix.')],
27:[('',U,[9],[9],'Peer input source exposure follows enabled features; independently usable incoming source required.'),
 ('To monitor the incoming',U,[9],[9],'Input Type peer plus In, or armed In/Auto, are delegated to recording/routing owners; no default inferred.'),
 ('then select',U,[9],[9],'Source-track Input Channel selection is an explicit case action.'),
 ('To record',U,[9],[9],'Recording is armed plus selected peer/track; recording format and persistence stay with existing owners.')],
28:[('',U,[10],[10],'Audio-output-track eligibility is contracted and source choices/positive outputs proposed; no MIDI-only source promise.'),
 ('Note that in Live',U,[10],[10],'Live/Push directional role with exact peer build/firmware context; not Push3 completion.'),
 ('while other',U,[10],['U-PEERS'],'May-send-only capability caveat; U-PEERS explicitly varies sending-only capability, no arbitrary receiver guarantee.')],
29:[('',I,[],[],'Link Audio FAQ referral only; target not inspected.')],
31:[('',M,[],[],'Unavailable Link/clock and preference examples are use context, not capability failure rules.'),
 ('For example',M,[],[],'Drummer/turntable examples give possible sources, not a supported-source taxonomy or calibration.'),
 ('This is where',E,[],[],'Transition to the following detector description.'),
 ('Tempo Follower analyzes',U,[11],[11],'Incoming audio/tempo interpretation role; detector performance, latency and sample classification unknown.')],
33:[('',U,[11],[11],'Tempo & MIDI Settings input configuration and actual interface/channel source are proposed.'),
 ('For a drum kit',M,[],[],'Microphone example only, not mandatory routing/hardware.'),
 ('For turntables',M,[],[],'Mixer output/effects-loop example only; general routing retains hardware gates.'),
 ('Note that while',M,[],[],'Clear-rhythm optimization and experimenting with sources are context, not rejection grammar, algorithm or performance oracle.')],
34:[('',R,[12],[12],'Show toggle exposes Follow; visibility/hide/restore action is explicit.'),
 ('alongside',G,[],[],'Textual left-hand/tempo-controls placement context is absent from clause/case; no figure label inferred.','SA-G06')],
35:[('',U,[12],[11],'Case011 explicitly records the known audio input before activating Follow; source-defined listening/interpretation remains unmeasured.'),
 ('Note that',R,[12],[12],'Hidden Follow disables running independently from input-unavailable condition.')],
36:[('',R,[12],[12],'Known configured input unavailable is separately proposed after active-input baseline; grayed/disabled role is named.')],
37:[('',U,[13],[13],'Follower/external-sync exclusion; working Follower and MIDI baselines precede comparisons.'),
 ('and the External Sync',U,[13],[13],'EXT disabled while Follower active; transition/restoration policy still U.'),
 ('Live can still send',U,[13],[13],'Outgoing MIDI clock permitted while Follower active.'),
 ('but it cannot receive',U,[13],[13],'Incoming MIDI clock exclusion is separately inspected, not an arbitrary wire/parser rejection law.')],
39:[('',M,[],[],'MIDI as alternative for non-Link devices is use context, not proof of Link absence on a particular device.'),
 ('The MIDI protocol',U,[15,16],[15,16],'Two named synchronization roles; no normative MIDI specification imported.'),
 ('Both protocols work',M,[],[],'Sync-host/device terminology supplies protocol context only; byte/timing laws are not stated.')],
40:[('',M,[],[],'Fast-metronome analogy supplies no tick count or frequency.'),
 ('The rate of the incoming',G,[15],[],'Tempo-dependent tick predicate is contracted, but case015 changes roles/directions without an explicit tempo-change comparison.','SA-G07'),
 ('Changing the tempo',G,[],[],'Receiver following host tempo change is not explicitly in contract015; generic role traffic is insufficient.','SA-G07'),
 ('The MIDI Clock protocol also',U,[15,19],[19],'Song-position message role; case019 explicitly supplies admitted position pointers, no wire encoding.'),
 ('With respect to MIDI Clock',U,[15],[15],'Sender/sync-host and receiver/device directions explicitly configured separately.')],
41:[('',M,[],[],'MIDI/SMPTE industry context does not define this product wire codec.'),
 ('A MIDI Timecode message',U,[16],[16],'Seconds/frames source role; no rate enumeration or frame conversion.'),
 ('Live will interpret',U,[16],[16],'Arrangement-position role; independently valid MTC source and position variation proposed.'),
 ('Timecode messages carry',U,[16],[16],'No meter information and manual Live tempo context; not an observed meter/parser contract.'),
 ('Tempo changes cannot',U,[16],[16],'No tempo tracking from MTC source; case varies source position separately from tempo.'),
 ('Detailed MIDI Timecode',E,[],[],'Internal chapter cross-reference, no separate behavior claim.'),
 ('With respect to MIDI Timecode',G,[16],[],'Receiver-only/not-host predicate is contracted; case016 exercises receiving, not offered MTC-host capability/exclusion.','SA-G08')],
43:[('',U,[17],[17],'Clock output to connected compatible sequencer/drum machine; not device universal compatibility.'),
 ('After connecting',R,[17],[17],'Receive-sync setup and destination Sync enable context are explicit; general port roles stay routing-owned.')],
44:[('',R,[17],[17],'Lower outgoing indicator inspected alongside actual admitted traffic; LED alone not proof of receiver sync.')],
46:[('',U,[18],[18],'External sequencer receiving-sync role; no decoder/timing guarantee.'),
 ('After connecting',R,[18],[18],'External source connection/settings role; general MIDI port selection delegated.')],
47:[('',R,[18],[18],'Source-enabled EXT visibility is inspected.'),
 ('You can then',R,[18],[18],'Button and menu entry points exercised separately.'),
 ('The upper indicator',R,[18],[18],'Upper incoming usable-sync indicator; accepted positive traffic required, no grammar inferred.')],
48:[('',U,[19],[19],'Song-position reception is source-dependent, with independently accepted traffic.'),
 ('If the host jumps',U,[19],[19],'Host jump/Live position role; actual transport positions remain null outcomes.'),
 ('However, if',U,[19],[19],'Control Bar Loop-enabled playback/wrapped pointers context; no modulo/origin/boundary or scheduling law.')],
50:[('',R,[20],[20],'Per-device Timecode controls independently selected, without persistence/default assumptions.'),
 ('Select a MIDI device',R,[20],[20],'MIDI Ports selection exposes settings; two known devices proposed.')],
51:[('',R,[20],[20],'Rate relevant only for MIDI Timecode; do not infer hidden versus disabled.'),
 ('The MIDI Timecode Rate',R,[21],[21],'Rate chooser role inspected; no unsupported enum values.'),
 ('All of the usual',U,[21],[21],'Usual SMPTE rates are not enumerated in source; case records actual offered values, not a guessed rate set.'),
 ('When the Rate',U,[21],['U-MTC'],'SMPTE All detection is prose-only; U-MTC varies actual accepted formats and retains messages/states, not a detector oracle.'),
 ('Note that you can adjust',R,[21],[21],'Arrangement display format separate from incoming format; Options Time Ruler Format context explicit.')],
52:[('',R,[20],[20],'MTC-only Offset applicability; exact disabled presentation U.'),
 ('You can specify',U,[22],[22],'Supplied accepted SMPTE offset, no grammar/range/default/sign.'),
 ('Live will interpret',U,[22],[22],'Arrangement start-time interpretation is prose-only, not arithmetic.')],
54:[('',U,[23],[23],'Per-device Sync Delay and internal-time-base relative role; no numeric correction law.'),
 ('This can be useful',M,[],[],'Transmission-delay compensation motivation, not calibrated lag/default or guaranteed cure.'),
 ('The Sync Delay for',U,[23],[23],'Selecting MIDI Ports device exposes that device delay; case explicitly selects intended device.'),
 ('To adjust the delay',U,[23],[23],'Separate known audible percussive patterns as listening setup, not signal generator or comparison algorithm.'),
 ('While listening',M,[],[],'Perfect sync is qualitative listening guidance, not zero-error/sample/timing acceptance tolerance.')]
}

GAPS=[
 dict(id='SA-G01',title='Remaining-peer continuity on join/leave',kind='missing-source-clause-and-targeted-case',blocks=['SYNC-B005'],existing_context_requirements=[1,3],existing_context_cases=[1,'U-PEERS','U-LOSS'],clause_delta='In a reviewed successor only, add the documentary claim that a participant may join or leave without interrupting synchronization between other remaining peers. Do not assign a wire/phase/jitter or zero-interruption timing bound.',case_delta='Propose a distinct three-peer case: independently establish usable synchronization and nonzero active output at A and B, then admit a compatible C joining and leaving separately while A/B continue. Retain A/B actual timing/audio/transport traces, not membership count alone. No missing peer or silent path can pass.'),
 dict(id='SA-G02',title='Documentary initial Link-toggle visibility context',kind='missing-default-context-case',blocks=['SYNC-B009'],existing_context_requirements=[5],existing_context_cases=[5],clause_delta='Clarify only the source-described displayed-by-default Control Bar Link toggle. Exact-build constructor, prior preferences, custom/default Set, reset and migration remain U.',case_delta='In a successor case, record independently known offered-feature/build and untouched known preference provenance before any explicit Show/Hide edit; inspect initial visible state, then exercise explicit Hide/Show on a separate history. Do not reset/install or presume factory preference identity.'),
 dict(id='SA-G03',title='Adjacent menu feature switches',kind='missing-targeted-case',blocks=['SYNC-B010'],existing_context_requirements=[5],existing_context_cases=[5,6],clause_delta='No new behavior clause necessary: existing005 already includes menu on/off roles. Do not infer extra menu labels or complete enum values from the image.',case_delta='Extend or split005 to explicitly open the adjacent menu and exercise its actually offered Link/Audio on/off controls separately after a known both-enabled peer/nonzero streaming baseline. Retain visible controls/states and source capability; keep actual audio/timing oracles null.'),
 dict(id='SA-G04',title='Adjacent menu Audio-enabled peer list',kind='missing-list-context-case',blocks=['SYNC-B010'],existing_context_requirements=[5],existing_context_cases=[5,6],clause_delta='No new behavior clause necessary: existing005 specifies the Audio-enabled connected-peer list. No discovery deadline or arbitrary-peer filtering algorithm follows.',case_delta='Add explicit menu-list observation with independently connected compatible Audio-enabled peer(s), then a separately known Link-only/not-Audio peer contrast while retaining an Audio-positive baseline. Record actual capabilities and list entries; unavailable/undetected peers stay U and cannot prove exclusion.'),
 dict(id='SA-G05',title='First participant initial-tempo case',kind='missing-initialization-context-case',blocks=['SYNC-B022'],existing_context_requirements=[2],existing_context_cases=[2],clause_delta='No new clause: existing002 already records initial-tempo ownership. Do not define causal ordering or race/convergence arithmetic.',case_delta='Add an explicit newly admitted session history with independently known first participant and valid chosen tempo, then a compatible joining peer with a distinct valid prior tempo. Retain actual membership order and tempo traces before ordinary/simultaneous tempo edits. Numeric/timing outcomes remain null.'),
 dict(id='SA-G06',title='Textual Follow placement context',kind='missing-UI-context',blocks=['SYNC-B034'],existing_context_requirements=[12],existing_context_cases=[12],clause_delta='If this source UI-layout context is adopted, append only that the manual places Follow alongside other tempo-related parameters at the left of the Control Bar. No pixel geometry, icon artwork or all-window-width guarantee.',case_delta='Extend012 visible-toggle observation to retain textual Control Bar placement alongside tempo-related controls with independently known display/layout context. Inspect actual offered controls only; no labels inferred from uninspected figures.'),
 dict(id='SA-G07',title='MIDI Clock tempo-change receive case',kind='missing-source-predicate-and-targeted-case',blocks=['SYNC-B040'],existing_context_requirements=[15],existing_context_cases=[15,14],clause_delta='In a reviewed successor, make explicit the source-described receiver following host tempo changes and retain tempo-dependent tick context. Do not infer ticks-per-quarter, byte grammar, delay, filtering or numerical tempo/convergence law.',case_delta='Add an explicit known MIDI Clock receiver history after admitted bidirectional-role baselines: isolate a single valid host, Link/Follower off, choose two independently accepted host tempos sequentially and retain source traffic plus Live tempo/transport traces. Keep MTC manual-tempo comparison separate; no numeric/byte/timing oracle.'),
 dict(id='SA-G08',title='MTC receiver-only capability case',kind='missing-directional-exclusion-case',blocks=['SYNC-B041'],existing_context_requirements=[16],existing_context_cases=[16,20],clause_delta='No new clause: existing016 already says receiver, not host. Retain that MTC exclusion separately from Clock bidirectional roles; do not invent an absent UI option or transmission error message.',case_delta='Request independently admitted exact-build capability evidence after a working MIDI Clock-host and MTC-receiver baseline. Retain actually offered sync direction/type controls or authoritative source evidence for MTC host exclusion. Do not send guessed MTC bytes or treat missing hardware/capability as a negative pass; absence may remain unresolvable/U.')]

class Markup(HTMLParser):
 def __init__(self):
  super().__init__();self.depth=0;self.anchor=None;self.caption=None;self.link=None;self.inblock=0;self.rows=[];self.unassigned=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='div':
   if d.get('id')=='chapter_content':self.depth=1
   elif self.depth:self.depth+=1
  if not self.depth:return
  if tag in {'h1','h2','h3','h4'}:self.anchor=d.get('id')
  if tag in {'h1','h2','h3','h4','p','li'}:self.inblock+=1
  if tag in {'a','img','figcaption'}:
   row=dict(tag=tag,html_line=self.getpos()[0],html_column=self.getpos()[1],anchor=self.anchor,attributes=d,starttag_sha256=sha256(self.get_starttag_text().encode()).hexdigest())
   self.rows.append(row)
   if tag=='a':self.link=(row,[])
   if tag=='figcaption':self.caption=(row,[])
 def handle_data(self,v):
  if not self.depth:return
  if self.caption is not None:self.caption[1].append(v)
  if self.link is not None:self.link[1].append(v)
  if v.strip() and not self.inblock and self.caption is None:self.unassigned.append(dict(html_line=self.getpos()[0],text=v))
 def handle_endtag(self,tag):
  if not self.depth:return
  if tag=='a' and self.link is not None:
   self.link[0]['text']=' '.join(''.join(self.link[1]).split());self.link=None
  if tag=='figcaption' and self.caption is not None:
   self.caption[0]['text']=' '.join(''.join(self.caption[1]).split());self.caption=None
  if tag in {'h1','h2','h3','h4','p','li'}:self.inblock-=1
  if tag=='div':self.depth-=1

def ref_req(value,reqs):
 id=rid(value);i=next(i for i,r in enumerate(reqs) if r['id']==id);r=reqs[i]
 return dict(path=str((S/'requirements.json').relative_to(ROOT)),pointer=f'/{i}/contract',id=id,contract_sha256=sha256(r['contract'].encode()).hexdigest(),strength=r['strength'],target_applicability=r['target_applicability'])
def ref_case(value,cases):
 id=cid(value);i=next(i for i,c in enumerate(cases) if c['id']==id);c=cases[i]
 return dict(path=str((S/'cases.json').relative_to(ROOT)),pointer=f'/{i}/setup_and_action',id=id,kind=c['kind'],action_sha256=sha256(c['setup_and_action'].encode()).hexdigest(),requirements=c['requirements'],documentary_expected_is_null=c['documentary_expected'] is None,documentary_comparator_is_null=c['documentary_comparator'] is None,expected_is_null=c['expected'] is None,comparison_is_null=c['comparison'] is None,target_grade=c['target_grade'],executed=c['executed'])

def build():
 blocks=load(S/'source-blocks.json');reqs=load(S/'requirements.json');cases=load(S/'cases.json');source=load(S/'source.json');manifest=load(S/'manifest-author-r1.json')
 assert sha256((S/'manifest-author-r1.json').read_bytes()).hexdigest()=='e94dddb2bd443a5a20ffbacc03bc9b0ab48cde0c97cc085c2175481e13ea26d4'
 assert len(blocks)==54 and len(reqs)==26 and len(cases)==36
 assert {int(b['id'][-3:]) for b in blocks if not b['tag'].startswith('h')}==set(PLAN)
 units=[];blockrows=[]
 for bi,b in enumerate(blocks):
  rows=PLAN.get(bi+1,[('',E,[],[],'Retained heading/hierarchy identity; no application input/output claim.')])
  starts=[0]
  for row in rows[1:]:
   pos=b['text'].index(row[0],starts[-1]+1);starts.append(pos)
  starts.append(len(b['text']))
  ids=[]
  for ui,(row,start,end) in enumerate(zip(rows,starts,starts[1:]),1):
   marker,status,rr,cc,note,*gap=row
   assert b['text'][start:].startswith(marker)
   raw=b['text'][start:end];a=start+len(raw)-len(raw.lstrip());z=end-(len(raw)-len(raw.rstrip()));text=b['text'][a:z]
   id=f'SYNC-A{len(units)+1:03}';ids.append(id)
   requirements=[ref_req(x,reqs) for x in rr];case_refs=[ref_case(x,cases) for x in cc]
   for r in requirements:
    req=next(x for x in reqs if x['id']==r['id']);r['existing_evidence_cites_this_block']=any(e['block']==b['id'] for e in req['evidence'])
   units.append(dict(id=id,source_id=source['id'],source_sha256=source['sha256'],source_url=source['url']+'#'+b['anchor'],source_blocks_path=str((S/'source-blocks.json').relative_to(ROOT)),source_pointer=f'/{bi}/text',block_id=b['id'],block_tag=b['tag'],anchor=b['anchor'],html_line=b['html_line'],normalized_block_character_start=a,normalized_block_character_end=z,text=text,text_sha256=sha256(text.encode()).hexdigest(),disposition=status,requirements=requirements,cases=case_refs,judgment=note,gap_ids=gap,target_applicability='U',complete=False,execution=False,semantic_validation='human proposed source sufficiency judgment; not proven by a filled row'))
  blockrows.append(dict(id=b['id'],tag=b['tag'],anchor=b['anchor'],html_line=b['html_line'],source_pointer=f'/{bi}',text_sha256=sha256(b['text'].encode()).hexdigest(),source_units=ids,all_text_accounted_for=True,topic_complete=False,target_applicability='U'))
 # Figure bytes/targets are intentionally not fetched. Caption text is retained,
 # not a reading of image pixels or hidden labels. The old54-block parser excludes captions.
 markup=Markup();markup.feed((S/source['file']).read_text());assert not markup.unassigned,markup.unassigned
 supplemental=[]
 for row in markup.rows:
  row=dict(row);row['id']=f'SYNC-M{len(supplemental)+1:03}';row['source_sha256']=source['sha256'];row['target_applicability']='U';row['complete']=False;row['execution']=False
  if row['tag']=='img':row.update(disposition=I,judgment='Only retained image element/URLs/alt attribute read. Image pixels, labels, palettes and geometry uninspected; no inferred behavior.')
  elif row['tag']=='figcaption':row.update(disposition=E,judgment='Entire retained textual figure caption read as source context. Image remains uninspected; caption does not establish rendering or extra controls.')
  else:
   href=row['attributes']['href'];same=href.startswith('/en/live-manual/12/synchronizing-with-link-tempo-follower-and-midi/#')
   row.update(disposition=E if same else I,target_same_retained_chapter=same,judgment='Internal reference to a heading whose retained text was read; no navigation behavior prescribed.' if same else 'Literal reference/label retained, but destination source was not opened in this audit. No linked semantics imported.')
  supplemental.append(row)
 gaprows=[]
 for g in GAPS:
  row=dict(g);row['source_units']=[u['id'] for u in units if g['id'] in u['gap_ids']]
  row['current_context_only_requirements']=[ref_req(x,reqs) for x in row.pop('existing_context_requirements')]
  row['current_context_only_cases']=[ref_case(x,cases) for x in row.pop('existing_context_cases')]
  row.update(status='audit-proposal-only; not a current normative clause/case and not a finding that partial approval was false',documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False)
  gaprows.append(row)
 # Pin every original packet payload, manifest, review, canonicals and exact parser.
 paths={S/'manifest-author-r1.json': 'audited immutable R1 identity'}
 for name,v in manifest['files'].items():
  q=S/name;assert digest(q)==v;paths[q]='all audited R1 payloads, byte-identical'
 for dep in load(S/'dependencies.json'):
  q=ROOT/dep['path'];assert digest(q)=={k:dep[k] for k in ['bytes','sha256']};paths[q]='retained source parser origin; not recapture'
 for q in ['reviews/synchronization-workflows-review.json']:
  paths[P.parent/q]='independent R1 review identity; partial approval only'
 for name in ['specs','research']:paths[ROOT/f'wiki/{name}/synchronization-workflows.md']='current canonical matches audited R1 snapshot'
 assert (ROOT/'wiki/specs/synchronization-workflows.md').read_bytes()==(S/'spec-r1.md').read_bytes()
 assert (ROOT/'wiki/research/synchronization-workflows.md').read_bytes()==(S/'research-r1.md').read_bytes()
 owners=[('recording-comping','REQ-RECORDING-COMPING-001/002/012','Arm/In/Auto/Off gates and count-in stay authoritative; source027/023 add Link predicates only.'),('routing-monitoring-latency','REQ-RML-012/013/014','Port-role and incoming/outgoing sync indicator contexts; no new Track/Sync/Remote delivery law.'),('clip-launch','finite launch quantization owner','Network phase/launch prose is not an extension of finite released scheduler laws.'),('session-launch-workflows','documentary Session launch owner','No Follow-action/Legato/RNG or scene launch behavior inferred from synchronization.'),('external-hardware-devices','Hardware Latency owner','Sync Delay is distinct; listening guidance does not calibrate either control.'),('settings-learning-workflows','settings-tab routing boundary','Settings owner explicitly routes synchronization tab behavior to this owner; no duplicate preference contract.'),('transport-state','loaded Set transport values owner','No extension of finite loaded loop/tempo/position parsing to MIDI clock, wrapping or runtime transport.')]
 ownerrows=[]
 for name,ids,note in owners:
  q=ROOT/f'wiki/specs/{name}.md';paths[q]='existing canonical owner boundary, read relevant context only';ownerrows.append(dict(path=str(q.relative_to(ROOT)),role=ids,impact=note,adoption='No mutation now; preserve ownership and recheck any reviewed synchronization successor.'))
 # Bounded downstream census: the exact reviewed R4 contains navigation refs to this R1.
 # No claim to scan all evolving shared registers or unrelated packet families.
 R4=P.parent/'inventory-revisions/r4-citation-crosswalk';r4m=load(R4/'manifest.json')
 assert digest(R4/'manifest.json')['sha256']=='82e88e6a8111df62f3b46ef445a5e802087396138481ed331cbd9a964d266fc6'
 for name,v in r4m['files'].items():assert digest(R4/name)==v
 for q in [R4/'manifest.json']+[R4/name for name in r4m['files']]:paths[q]='frozen R4 citation/navigation downstream, not semantic coverage'
 paths[P.parent/'reviews/manual-citation-crosswalk-r4-review.json']='independent downstream navigation review'
 for q in [P.parent/'settings-learning/manifest-author-r1.json',P.parent/'reviews/settings-learning-workflows-review.json']:paths[q]='settings owner identity/review context, not imported requirements'
 def walk(v,p=''):
  if isinstance(v,dict):
   for k,w in v.items():yield from walk(w,p+'/'+k.replace('~','~0').replace('/','~1'))
  elif isinstance(v,list):
   for i,w in enumerate(v):yield from walk(w,p+'/'+str(i))
  elif isinstance(v,str):yield p,v
 downstream=[]
 for name in r4m['files']:
  if not name.endswith('.json'):continue
  refs=[]
  for pointer,value in walk(load(R4/name)):
   if 'synchronization' in value or 'REQ-SYNC-WORKFLOW-' in value or value.startswith('SYNC-') or value=='e94dddb2bd443a5a20ffbacc03bc9b0ab48cde0c97cc085c2175481e13ea26d4':refs.append(dict(pointer=pointer,value=value))
  if refs:downstream.append(dict(path=str((R4/name).relative_to(ROOT)),references=refs,adoption='Retain R4 unchanged. Any approved successor needs a new citation cohort/revision with explicit new identity, not a silent rewrite.'))
 impact=dict(scope='Bounded current canonical owner sections, audited R1, frozen R4 downstream and settings owner identities. Not a whole-repository reverse dependency proof.',owners=ownerrows,downstream=downstream,shared_registers='Root handles indexes, coverage, questions, feature routing and log. No shared edits; later R9 census or evolving catalogs are not claimed reconciled here.',semantic_effect='Eight source/case/context proposals; no contradiction or runtime discrepancy established. Existing R1 partial approval and historical links remain intact; no current clause changed.')
 questions=[dict(id='SA-Q01',topic='Exact target and peer capabilities',status='U',detail='Current Version12 source has no immutable12.4.3 publication identity. Link Audio existence, peer/Push firmware/directional capabilities and platform contexts remain unproven.'),dict(id='SA-Q02',topic='MIDI Start/Stop and port modes',status='U',detail='This retained chapter documents Link Start Stop Sync, not MIDI Start/Stop byte sequences, MIDI Clock Song/Pattern message policy or every port configuration. Do not transfer Link option semantics to MIDI wire behavior.'),dict(id='SA-Q03',topic='Preroll, lag and defaults',status='U',detail='No MIDI preroll policy, calibrated lag, default Sync Delay/MTC Offset/Rate, numeric range/sign or frame list follows. The only explicit Control Bar visibility default is source009; generic lifecycle/boundary probes do not invent these values.'),dict(id='SA-Q04',topic='Detector, timing and continuity',status='U',detail='Real-time/reliable/perfect/clear-rhythm language supplies no algorithm, phase tolerance, tempo tracking error, acquisition/convergence time, packet loss or sample delay comparator. Peer count, name, status, buffer text and LEDs are not sync proof.'),dict(id='SA-Q05',topic='Linked targets and figures',status='uninspected',detail='All caption text and literal image/link markup retained below, but no image pixels or external linked product catalog/FAQ/manual targets inspected; no hidden labels imported.'),dict(id='SA-Q06',topic='Runnable cases and lifecycle',status='U',detail='All cases remain proposals with independently admitted usable source/peer/nonzero-path/owned fixture and paired-positive guards. Malformed, loss, cancellation, undo, persistence, rate, arbitration and teardown remain broad unknowns; no unavailable feature/input passes a negative case.')]
 inputs=dict(audited_manifest_sha256=digest(S/'manifest-author-r1.json')['sha256'],audited_review=str((P.parent/'reviews/synchronization-workflows-review.json').relative_to(ROOT)),source=source,source_parse='all54 original blocks and full textual captions read; exact hand-segmented normalized text offsets; retained HTML only',pins=[pin(q,role) for q,role in sorted(paths.items())])
 reconciliation=dict(requirements=[dict(reference=ref_req(int(r['id'].split('-')[-1]) if r['id'].split('-')[-1].isdigit() else 'U-'+r['id'].split('U-')[1],reqs),source_units=[u['id'] for u in units if any(x['id']==r['id'] for x in u['requirements'])],status='mapped to partial source predicates' if any(any(x['id']==r['id'] for x in u['requirements']) for u in units) else 'generic unsupported obligation; no direct source predicate/evidence') for r in reqs],cases=[dict(reference=ref_case(int(c['id'].split('-')[-1]) if c['id'].split('-')[-1].isdigit() else c['id'][5:],cases),source_units=[u['id'] for u in units if any(x['id']==c['id'] for x in u['cases'])],status='partial source-related proposed action' if any(any(x['id']==c['id'] for x in u['cases']) for u in units) else 'generic future protocol/lifecycle probe; not a source predicate acceptance result') for c in cases],all_target_expected_comparison_null=True,documentary_expected_nonnull_current_cases=sum(c['documentary_expected'] is not None for c in cases),all_cases_unexecuted=True)
 summary=dict(status='frozen-proposed-source-semantic-audit-awaiting-independent-review',original_source_blocks=54,original_headings=sum(b['tag'].startswith('h') for b in blocks),original_substantive_blocks=len(PLAN),source_text_units=len(units),dispositions=dict(Counter(u['disposition'] for u in units)),all_source_text_accounted_for=True,source_normalized_characters=sum(len(b['text']) for b in blocks),supplemental_markup_rows=len(supplemental),supplemental_tags=dict(Counter(x['tag'] for x in supplemental)),gaps=len(gaprows),existing_requirements=26,existing_cases=36,mapped_distinct_requirements=len({r['id'] for u in units for r in u['requirements']}),mapped_distinct_cases=len({c['id'] for u in units for c in u['cases']}),external_pins=len(paths),executed=0,app_or_topic_complete=0,all_target_applicability='U',canonical_mutations=0,source_mutations=0,claim='A filled source ledger is neither application/leaf completeness nor target compatibility; source/case mapping judgments remain independently reviewable proposals.')
 return {'inputs':inputs,'source-block-ledger':blockrows,'source-unit-ledger':units,'supplemental-markup':supplemental,'gap-proposals':gaprows,'context-questions':questions,'owner-impact':impact,'catalog-reconciliation':reconciliation,'summary':summary}

def main():
 assert sys.argv[1:] in (['--write'],['--check']),'choose --check (read-only) or initial --write'
 if sys.argv[1:]==['--write']:
  assert not (P/'manifest-author-r1.json').exists(),'refuse mutation after seal'
  d=build()
  for name,value in d.items():(P/(name+'.json')).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
 else:
  d=build()
  for name,value in d.items():assert load(P/(name+'.json'))==value,name
 print(json.dumps(d['summary'],indent=2))
if __name__=='__main__':main()
