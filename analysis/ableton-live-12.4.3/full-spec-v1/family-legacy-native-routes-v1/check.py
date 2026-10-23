"""Read-only owned Legacy map integrity; no old modules/query/body/native/provider execution."""
from pathlib import Path
import json,hashlib,re,collections,copy,sys,struct
P=Path(__file__).resolve().parent;F=P.parent;D=F/'legacy-devices';R=F.parents[2]
J=lambda p:json.loads(p.read_bytes());H=lambda b:hashlib.sha256(b).hexdigest();OH=lambda x:H(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def need(ok,msg):
 if not ok:raise ValueError(msg)
def ptr(obj,pointer):
 need(pointer.startswith('/'),'pointer root')
 for token in pointer.split('/')[1:]:
  token=token.replace('~1','/').replace('~0','~');obj=obj[int(token)] if isinstance(obj,list) else obj[token]
 return obj
def identity(pin):
 p=Path(pin['path']);h=hashlib.sha256();size=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);size+=len(b)
 need(size==pin['bytes'] and h.hexdigest()==pin['sha256'],'selected source/context identity')
def raw_row(row):
 allowed={str(F/'component-resolution-v1'/n) for n in ['class-tables.jsonl','class-rtti.jsonl','class-stores.jsonl','symbol-owners.jsonl','symbol-memberships.jsonl']}|{str(Path('/var/tmp/sound-analysis/corpus/indexes')/n) for n in ['aliases.jsonl','calls.jsonl','indirect.jsonl']}
 need(row['provider'] in allowed,'only selected retained metadata provider')
 with Path(row['provider']).open('rb') as f:
  if row['source_byte']:f.seek(row['source_byte']-1);need(f.read(1)==b'\n','raw line boundary')
  f.seek(row['source_byte']);raw=f.read(row['raw_bytes'])
 need(len(raw)==row['raw_bytes'] and raw.endswith(b'\n') and H(raw)==row['raw_sha256'],'selected exact raw byte/hash')
 original=json.loads(raw)
 if row['kind']=='table-data':
  expected=dict(original);n=len(original['slots']);expected.update(exported_prefix_slot_count=n,slots=original['slots'][:3] if n>16 else original['slots'],selection_policy='large leading3 construction/lifetime frontier only' if n>16 else 'whole small exported prefix',complete_native_table_class_function_or_processing_claim=False)
  need(row['record']==expected,'whole-small/leading3 exact table projection')
 else:need(row['record']==original,'exact selected record')
def metadata(rows,seeds,approval,proposal):
 need(collections.Counter(r['kind'] for r in rows)=={'lexical-owner-data':207,'membership-data':208,'alias-data':208,'RTTI-data':32,'table-data':32,'store-data':56,'call-data':256,'indirect-data':12},'1011row kinds')
 need(len({(r['provider'],r['source_byte']) for r in rows})==1011,'no duplicate raw padding')
 tables=[r['record'] for r in rows if r['kind']=='table-data'];aliases={r['record']['entry']:r for r in rows if r['kind']=='alias-data'}
 need(len(tables)==approval['caps']['primary_tables']==32 and approval['caps']['call_seeds']==208 and approval['exception'].startswith('Packet-specific128'),'explicit208seed exception')
 need({(r['literal_type_encoding'],r['address_point']) for r in tables}=={(r['type'],r['address_point']) for r in approval['classes']} and approval['classes']==proposal['classes'],'exact32class scope')
 need(sum(len(r['slots']) for r in tables)==96<=approval['caps']['selected_slots'] and sum(r['exported_prefix_slot_count'] for r in tables)==1855 and sum(r['exported_prefix_slot_count']>16 for r in tables)==22,'96of1855slots22large10small')
 need([r['entry'] for r in seeds['entries']]==approval['all_208_seed_entries']==proposal['proposed_all_208_seed_entries']==list(aliases) and len(aliases)==208,'whole208 no group omission')
 for s in seeds['entries']:
  rr=rows[s['native_data_line']-1];need(s['selected_outgoing_seed'] and rr['kind']=='alias-data' and rr['record']['entry']==s['entry'] and rr['record']['name']==s['name'],'seed rawalias identity')
 ti={r['record']['address']:r['record'] for r in rows if r['kind']=='RTTI-data'};points={t['address_point'] for t in tables};owners={r['record']['scope_id'] for r in rows if r['kind']=='lexical-owner-data'}
 for t in tables:
  need(t['offset_to_top']==0 and t['native_table_extent'] is None and not t['complete_native_table_class_function_or_processing_claim'],'metadata not native complete')
  need(int(t['address_point'],16)==int(t['table_header'],16)+16 and t['address_point_file_offset']==t['header_file_offset']+16,'addresspoint/header geometry')
  need(struct.unpack('<qQ',bytes.fromhex(t['raw_header16_hex']))==(0,int(t['typeinfo'],16)),'raw header metadata')
  need(ti[t['typeinfo']]['literal_type_encoding']==t['literal_type_encoding'] and bytes.fromhex(ti[t['typeinfo']]['name_NUL_hex'])==t['literal_type_encoding'].encode()+b'\0','RTTI identity')
  for i,s in enumerate(t['slots']):need(s['offset']==8*i and int.from_bytes(bytes.fromhex(s['raw8_hex']),'little')==int(s['target'],16),'raw slot geometry')
 for r in rows:
  x=r['record']
  if r['kind']=='membership-data':need(any(c[1] in owners for c in x['candidates']) and x['entry'] in aliases and x['source']==[aliases[x['entry']]['source_line'],aliases[x['entry']]['source_byte'],aliases[x['entry']]['raw_bytes']],'membership alias locator')
  if r['kind']=='store-data':need(x['address_point'] in points and x['address_point'][2:] in x['quote'],'literal store scope')
  if r['kind']=='call-data':need(x['caller'] in aliases,'only approved outgoing seeds')
  if r['kind']=='indirect-data':need((x.get('function') in aliases or x.get('caller') in aliases) and x['resolved_targets']==[],'unresolved indirect remains unknown')
def owners(spans,ledger,req,spec,packages,schemas):
 need(len(spans)==len(ledger['required_outcomes'])==len(req)==77 and len({r['id'] for r in ledger['required_outcomes']})==77,'77whole clauses unique')
 need(ledger['scoped_routes']=={'X':0,'file_only_S':8,'no_established_target':69} and ledger['application_S_or_X']==0 and ledger['coverage_gate']=='OPEN' and ledger['new_grade_norm_case_release_site_credit']==0,'scoped file8/app69 not grade')
 need(collections.Counter(r['source_annotation'] for r in ledger['required_outcomes'])=={'D11':45,'Dpkg':8,'U':24},'same77 annotations')
 for i,(s,row,r) in enumerate(zip(spans,ledger['required_outcomes'],req,strict=True)):
  need(s['requirement']==row['requirement']==r['id'] and row['source_annotation']==r['provenance'] and row['device']==r['device'] and s['record_sha256']==OH(r) and ptr(req,s['catalog_pointer'])==r,'owner catalog identity')
  loc=s['source'];raw=spec[loc['byte_start']:loc['byte_start']+loc['bytes']];need(raw.decode()==row['predicate']==r['text'] and H(raw)==loc['sha256'],'whole normative text exact')
  need(spec[:loc['byte_start']].count(b'\n')+1==loc['line_start'] and spec[:loc['byte_start']+loc['bytes']].count(b'\n')+1==loc['line_end'],'owner line geometry')
  need(row['unit']=='whole complete clause bundle; not atomic outcome' and row['actual_status']=='U' and row['exact_target_applicability']=='U' and row['public_binding']=='unknown' and not row['grade_changed'] and row['enumeration'] and row['missing_join'],'no grade/public/enumeration loss')
  if r['provenance']=='Dpkg':
   basis=row['route_basis'];pa=ptr(packages,basis['package_pointer']);sc=ptr(schemas,basis['schema_pointer']);need(row['route']=='S-route' and row['route_scope']=='retained-file/schema-only; no application credit' and basis['package_record_sha256']==OH(pa) and basis['schema_record_sha256']==OH(sc),'file-only exact retained basis')
   need(basis['schema_line']==sc['line'] and basis['schema_class']==sc['class']==pa['schema_class'] and basis['root']==pa['locator'] and basis['Creator']==pa['root_attributes']['Creator']=='Ableton Live 12.4d1' and basis['MinorVersion']=='12.0_12402' and not basis['raw_reopened'],'historical file identity not runtime')
  else:need(row['route']=='no-established-route' and row['route_scope']=='exact-target-application-query','D11 orU not targetS')
def cases_check(nav,cases,overlay,old,req,ledger):
 need(len(cases)==len(nav['cases'])==len(overlay)==194 and cases[:178]==old and collections.Counter(c['provenance'] for c in cases)=={'D11':45,'Dpkg':8,'U':141},'194roles/178old exact')
 rr={r['id']:r for r in req};need(len({c['id'] for c in cases})==194,'unique194')
 for i,(n,c,o) in enumerate(zip(nav['cases'],cases,overlay,strict=True)):
  need(ptr(cases,n['pointer'])==c and n['id']==c['id']==o['id'] and n['record_sha256']==OH(c) and n['field_sha256']=={k:OH(v) for k,v in c.items()} and n['keys']==sorted(c),'allcase fields exact')
  need(n['actual_overlay_pointer']==f'/actual_oracles/{i}' and n['actual_overlay_sha256']==OH(o) and n['actual_status']=='U','actual overlay identity')
  need(c['exact_target_expected'] is None and o['actual_expected'] is None and o['actual_comparison'] is None and o['exact_target_expected'] is None and o['target']=='U' and not o['executed'],'all194actualU not source/file grade')
  expected_role='target-U-probe' if c['provenance']=='U' else 'source-content-only' if c['provenance']=='D11' else 'retained-file-only';need(n['role']==expected_role,'194role separation')
  if c['provenance']=='D11':need(rr[c['requirement']]['text']=='Live 11 predecessor only: '+c['expected']+' Target 12.4.3 Legacy applicability is U.','D11 expected exact source wrapper only')
  if c['provenance']=='U':need(c['expected'] is None,'all141target expectationsnull')
  if i>=178:need(c['documentary_expected'] is None and c['actual_expected'] is None and c['actual_comparison'] is None and not c['executed'],'16new allnull')
 for row in ledger['required_outcomes']:need(row['cases_navigation_only']==[c['id'] for c in cases if c['requirement']==row['requirement']],'completecase navigation per clause')
def geometry_check(g,audit,cases,html):
 need(len(g['blocks'])==len(audit['blocks'])==114,'114notmodernRedux')
 for i,(r,b) in enumerate(zip(g['blocks'],audit['blocks'],strict=True)):
  before=html[:r['character_start']];need(r['id']==b['id'] and r['local']==b['legacy_locator'] and r['audit_pointer']==f'/blocks/{i}','source localglobal exact')
  need(r['character_start']==b['raw_start'] and r['character_end']==b['raw_end'] and html[r['character_start']:r['character_end']]==b['raw_html'] and H(b['raw_html'].encode())==r['raw_utf8_sha256'],'source rawspan')
  need(before.count('\n')+1==r['html_line']==b['html_line'] and len(before.rsplit('\n',1)[-1])==r['html_column']==b['html_column'],'Unicode source geometry')
 need(len(g['case_source_joins'])==211,'211source joins')
 for x in g['case_source_joins']:
  need(ptr(cases,x['case_pointer'])==x['literal_reference'],'exactcase reference pointer');b=ptr(audit,x['audit_pointer']);need(x['local']==b['legacy_locator'] and x['block']==b['id'] and x['text_sha256']==H(b['text'].encode()),'exact localglobal source join')
def positives(p):
 need(all(w in p['common']['signal'] for w in ['EACH','BOTH','NONEMPTY','BEFORE','productive']),'productive positives')
 need('remain unknown' in p['common']['lifecycle'] and '45D11' in p['common']['source_roles'] and '141target' in p['common']['source_roles'],'lifecycle/source scopes')
 for code,words in {'AUTO-FILTER':['LegacyMode=false','pre9.5','AutoFilter2','BOTH','EACH','finite','Drive'], 'AUTO-PAN':['not AutoPan2','BOTH','random'], 'CHORUS':['BOTH','Crisp','link-unlink/*20'], 'EROSION':['notErosion2','Width','Sine','BEFORE'], 'FLANGER':['HiQuality','BOTH'], 'FREQUENCY-SHIFTER':['postMixDrive','Mix0','modernShifter','BOTH'], 'PHASER':['notPhaserNew','do not borrow','BOTH'], 'REDUX':['factor1','BitReduction','EACH','Soft/Hard']}.items():need(all(w in p['devices'][code] for w in words),'device guard '+code)
def prefix(info):
 with Path(info['path']).open('rb') as source:raw=source.read(info['bytes'])
 need(len(raw)==info['bytes'] and H(raw)==info['sha256'],'complete historical research prefix unchanged')
def package_history(source,packages):
 c=source['package_history_counts'];entries=[r for p in packages for r in p['folder_presets']]
 need(c==dict(parsed_xml=105,unparsed_companions=105,total_entries=210,retained_exemplars=8,companions_are_presets=False,current_runtime_identity_proved=False),'package history not210presets or runtime identity')
 need(len(packages)==8 and len(entries)==210 and sum(r['roots'] is not None for r in entries)==105 and sum(r['roots'] is None for r in entries)==105,'105parsed105unparsed retained data only')
 need(next(x for x in packages[0]['fields'] if x['field']=='LegacyMode')['xml'].startswith('<LegacyMode Value="false"'),'one retained AutoFilter LegacyModefalse,not modern identity')
def main():
 need(sys.argv[1:]==['--check'],'read-only --check only; refuse before reads')
 need(H((P/'scope-census-proposal.json').read_bytes())=='2dba9910d2676fa51d785c04efcc3d5f43828fdaae08f808516b02489229c60f' and H((P/'scope-approval-root.json').read_bytes())=='5e17b4a1d5003acf06588a91636fce052303c3cb4639de4969f23ae24028fb69','exact pre-retention scope approval')
 pins=J(P/'source-pins.json')['files'];need(len(pins)==32,'32selectedsourcepins')
 for p in pins:identity(p)
 rows=[json.loads(x) for x in (P/'native-data.jsonl').read_bytes().splitlines()];seeds=J(P/'named-seeds.json');a=J(P/'scope-approval-root.json');q=J(P/'scope-census-proposal.json');identity(a['table_census']);identity(a['proposal']);metadata(rows,seeds,a,q)
 for r in rows:raw_row(r)
 req=J(D/'requirements.json');cases=J(D/'cases-r2.json');old=J(D/'cases.json');fi=J(D/'fixtures-r2.json');over=fi['actual_oracles'];spans=J(P/'owner-spans.json');ledger=J(P/'route-ledger.json');spec=(D/'spec-r2.md').read_bytes()
 owners(spans,ledger,req,spec,J(D/'package-observations.json'),J(D/'schema-fields.json'));nav=J(P/'case-navigation.json');cases_check(nav,cases,over,old,req,ledger)
 g=J(P/'source-geometry.json');audit=J(F/'legacy-devices-source-audit/audit.json');html=(D/'manual-11-audio-effects-2026-10-19.html').read_text();geometry_check(g,audit,cases,html)
 source_context=J(P/'sources.json');packages=J(D/'package-observations.json');package_history(source_context,packages)
 p=J(P/'prerequisites.json');positives(p);prefix(J(P/'research-prefix.json'))
 assoc=J(P/'processor-associations.json');batch=J(P/'batch-inputs.json')
 for field,kind,n in [('tables','table-data',32),('stores','store-data',56),('aliases','alias-data',208),('outgoing','call-data',256),('indirect','indirect-data',12)]:
  ids=[x for d in assoc.values() for x in d[field]];need(len(ids)==len(set(ids))==n and all(rows[i-1]['kind']==kind for i in ids),'perdevice partition '+field)
 need(all(x['public_binding']=='unknown' for x in assoc.values()),'associations not actual receivers')
 total=0
 for code,x in batch.items():
  need(x['status']=='NOT SELECTED / not execution-ready' and x['callable_X_leaves_established']==[],'no callableleaf/successor');expected=[(i,c) for i,c in enumerate(cases) if c['device']==code and c['provenance']=='U'];need(len(x['target_input_navigation'])==len(expected),'whole targetnavigation')
  for n,(i,c) in zip(x['target_input_navigation'],expected):need(n['id']==c['id'] and n['pointer']==f'/{i}' and n['action_pointer']==f'/{i}/action' and n['setup_pointer']==f'/{i}/setup','target input/action setup pointers');total+=1
 need(total==141,'141target probes distinctfrom53sourcefile')
 negatives=[]
 def reject(label,action):
  try:action()
  except (ValueError,KeyError,IndexError,TypeError):negatives.append(label)
  else:raise ValueError('negative accepted '+label)
 def own(l):owners(spans,l,req,spec,J(D/'package-observations.json'),J(D/'schema-fields.json'))
 for field,value,label in [('route','S-route','D11 to targetS'),('route','X-route','name toX'),('actual_status','pass','actualU tograde'),('public_binding','known','unprovedreceiver'),('predicate','filter works','wholeclause limits dropped'),('enumeration','','unknownscope omitted')]:
  bad=copy.deepcopy(ledger);next(x for x in bad['required_outcomes'] if x['source_annotation']=='D11')[field]=value;reject(label,lambda bad=bad:own(bad))
 bad=copy.deepcopy(ledger);bad['required_outcomes'].pop();reject('missingwholeclause',lambda:own(bad))
 bad=copy.deepcopy(ledger);bad['application_S_or_X']=8;reject('fileS creditedapplication',lambda:own(bad))
 bad=copy.deepcopy(ledger);bad['required_outcomes'][0]['route_scope']='target application';reject('retainedschema toconstructor',lambda:own(bad))
 bad=copy.deepcopy(ledger);bad['coverage_gate']='COMPLETE';reject('documentarycompletion',lambda:own(bad))
 bad=copy.deepcopy(nav);bad['cases'][0]['role']='target-U-probe';reject('filecase rolepromoted',lambda:cases_check(bad,cases,over,old,req,ledger))
 bad=copy.deepcopy(nav);bad['cases'][0]['pointer']='/cases/0';reject('invalidcasepointer',lambda:cases_check(bad,cases,over,old,req,ledger))
 bad=copy.deepcopy(over);bad[0]['actual_expected']=1;reject('historicalfile actualoracle',lambda:cases_check(nav,cases,bad,old,req,ledger))
 bad=copy.deepcopy(cases);bad[-1]['action']='inspect instead';reject('currentcase fullactionchanged',lambda:cases_check(nav,bad,over,old,req,ledger))
 bad=copy.deepcopy(seeds);bad['entries'].pop();reject('208frontier arbitrarilycut',lambda:metadata(rows,bad,a,q))
 bad=copy.deepcopy(a);bad['caps']['call_seeds']=128;reject('silentstandingcap reuse',lambda:metadata(rows,seeds,bad,q))
 bad=copy.deepcopy(rows);next(x for x in bad if x['kind']=='indirect-data')['record']['resolved_targets']=['0x0'];reject('inventresolvedsite',lambda:metadata(bad,seeds,a,q))
 bad=copy.deepcopy(rows);next(x for x in bad if x['kind']=='call-data')['record']['caller']='0x0';reject('unselectedcallee expansion',lambda:metadata(bad,seeds,a,q))
 bad=copy.deepcopy(next(x for x in rows if x['kind']=='table-data'));bad['record']['slots'][0]['target']='0x0';reject('slot substitution',lambda:raw_row(bad))
 bad=copy.deepcopy(rows[0]);bad['source_byte']+=1;reject('rawrow locatorcorrupt',lambda:raw_row(bad))
 bad=copy.deepcopy(g);bad['blocks'][0]['character_start']+=1;reject('D11geometrycorrupt',lambda:geometry_check(bad,audit,cases,html))
 bad=copy.deepcopy(p);bad['common']['signal']='Flags alone prove output';reject('vacuouspositive',lambda:positives(bad))
 for code,label in [('AUTO-FILTER','nestedLegacyMode conflated'),('EROSION','Noise positiveomitted'),('REDUX','factor1 wholebypass'),('CHORUS','delaypath BOTHomitted')]:
  bad=copy.deepcopy(p);bad['devices'][code]='modern device works';reject(label,lambda bad=bad:positives(bad))
 bad=copy.deepcopy(source_context);bad['package_history_counts']['parsed_xml']=210;reject('companions counted presets',lambda:package_history(bad,packages))
 bad=copy.deepcopy(source_context);bad['package_history_counts']['current_runtime_identity_proved']=True;reject('LegacyModefalse to modernidentity',lambda:package_history(bad,packages))
 bad=copy.deepcopy(J(P/'research-prefix.json'));bad['sha256']='0'*64;reject('canonicalprefix rewritten',lambda:prefix(bad))
 print(json.dumps(dict(status='PASS-data-only-author-integrity',whole_clauses=77,atomic_denominator=False,file_only_S=8,application_none=69,application_S_X=0,annotations_same77=dict(D11=45,Dpkg=8,U=24),case_roles=dict(D11source=45,Dpkgfile=8,targetU=141),all194actualnullU=True,old178exact=True,selected_DATA=1011,tables=32,slots=96,stores=56,aliases_memberships=416,complete_seeds=208,outgoing=256,indirect_unresolved=12,sourcepins=32,sourcegeometry=114,case_source_joins=211,negative_controls=negatives,new_body_native_original_grade_site_norm_case_release=0,coverage='OPEN',writes=False),indent=2))
if __name__=='__main__':main()
