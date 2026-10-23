#!/usr/bin/env python3
"""Selected metadata census only; no raw-row retention, code bodies, or traversal."""
from pathlib import Path
import collections, datetime, hashlib, json, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
COMPONENT = HERE.parent / 'component-resolution-v1'
INDEX = Path('/var/tmp/sound-analysis/corpus/indexes')
CORE = {
 'Drift': ['ADrift','LDrift','ADriftModule','ODriftProcessor'],
 'Drum Sampler': ['ADrumSampler','LDrumSampler','ADrumSamplerModule',
                  'ODrumSamplerProcessor','ODrumSamplerSampleHolder'],
 'Meld': ['AInstrumentMeld','LInstrumentMeld','AInstrumentMeldModule','OMeldProcessor'],
 'Operator': ['AOperator','AOperatorSynthesisModule','OInstrumentOperatorProcessor',
              'OOperatorVoiceManagementProcessor','OOperatorOperatorVoiceProcessor',
              'OInstrumentOperatorFilterProcessor','OOperatorLfoControlProcessor'],
 'Wavetable': ['AInstrumentWavetable','LInstrumentWavetable',
               'AInstrumentWavetableModule','OInstrumentWavetableProcessor'],
}
CLASS = {name: family for family, names in CORE.items() for name in names}
BROAD = re.compile(r'Drift|DrumCell|DrumSampler|InstrumentMeld|Meld|Operator|InstrumentVector|Wavetable', re.I)
CORE_TOKEN = re.compile(r'(?<![A-Za-z0-9_])('+'|'.join(CLASS)+r')(?![A-Za-z0-9_])')
METHOD = re.compile(r'::(Init|Exit|Reset|OnOn|CalcMain|Process|Render|OnNoteOn|OnNoteOff|CalculateCurve|CalculateCurves)(?=[>(]|$)')
WT_OWNER = re.compile(r'^ableton::devices::wavetable::(?:WavetableDeviceLfo|WavetableDeviceOscillator|WavetableEnvelope|WavetableModalFilter)<')
HELPER = re.compile(r'^(?:TDriftCyclingEnvelopeCurveHelper|TDriftLfoCurveHelper|TMeldModulationCurveHelper|TInstrumentWavetableLfoCurveHelper|TInstrumentWavetableFilterCurveProvider)::')

def census_rows(path):
    sha = hashlib.sha256(); size = count = 0
    with path.open('rb') as stream:
        for count, raw in enumerate(stream, 1):
            sha.update(raw); size += len(raw)
            yield count, json.loads(raw)
    identities[str(path)] = dict(path=str(path), bytes=size, lines=count, sha256=sha.hexdigest())

identities = {}
tables = []; broad_tables = []; small_targets = set(); large_targets = set()
for line, row in census_rows(COMPONENT/'class-tables.jsonl'):
    literal = row['literal_type_encoding']
    if BROAD.search(literal):
        broad_tables.append((literal, len(row['slots']), row['literal_store_candidate_count']))
    name = next((x for x in CLASS if literal == str(len(x))+x), None)
    typed = literal.startswith('N7ableton7devices9wavetable25WavetableUnisonOscillatorI')
    if row['offset_to_top'] != 0 or not (name or typed):
        continue
    small = len(row['slots']) <= 8
    chosen = row['slots'] if small else row['slots'][:3]
    (small_targets if small else large_targets).update(x['target'] for x in chosen)
    tables.append(dict(class_label=name or literal, family=CLASS.get(name, 'Wavetable'),
                       class_table_line=line, address_point=row['address_point'],
                       literal_type_encoding=literal, offset_to_top=0,
                       exported_prefix_slots=len(row['slots']), proposed_slots=len(chosen),
                       selection='whole small exported prefix' if small else 'leading three construction/lifetime prefix only',
                       literal_store_count_annotation=row['literal_store_candidate_count']))
assert len(tables) == 32 and sum(x['proposed_slots'] for x in tables) == 124
aps = {x['address_point'] for x in tables}
store_entries = set(); store_count = 0
for _, row in census_rows(COMPONENT/'class-stores.jsonl'):
    if row['address_point'] in aps:
        store_count += 1; store_entries.add(row['entry'])

broad_alias = set(); core_alias = set(); named = {}; named_metadata = {}
table_store = small_targets | large_targets | store_entries
entry_metadata = {}
for line, row in census_rows(INDEX/'aliases.jsonl'):
    labels = list(dict.fromkeys([row['name']]+[x['name'] for x in row.get('symbols', [])]))
    if any(BROAD.search(s) for s in labels): broad_alias.add(row['entry'])
    if any(CORE_TOKEN.search(s) for s in labels): core_alias.add(row['entry'])
    candidates = [s for s in labels if ((CORE_TOKEN.search(s) or WT_OWNER.search(s)) and METHOD.search(s)) or HELPER.search(s)]
    if candidates:
        named[row['entry']] = candidates
        named_metadata[row['entry']] = dict(entry=row['entry'], labels=candidates,
                                            alias_line=line, thunk=row['thunk'],
                                            thunk_target=row.get('thunk_target'), external=row['external'])
    if row['entry'] in table_store or candidates:
        entry_metadata[row['entry']] = dict(entry=row['entry'], name=row['name'],
                                            alias_line=line, thunk=row['thunk'],
                                            thunk_target=row.get('thunk_target'), external=row['external'])

all_seeds = table_store | named.keys()
slot_named_seeds = small_targets | large_targets | named.keys()
small_named_seeds = small_targets | named.keys()
memberships = {k: 0 for k in ['all_selected','slot_named','small_named']}
for _, row in census_rows(COMPONENT/'symbol-memberships.jsonl'):
    if row['kind'] != 'alias_membership': continue
    for key, selected in [('all_selected',all_seeds),('slot_named',slot_named_seeds),('small_named',small_named_seeds)]:
        if row['entry'] in selected: memberships[key] += 1

counts = {k: collections.Counter() for k in ['all_selected','slot_named','small_named']}
per_entry = collections.defaultdict(collections.Counter)
for kind, filename, field in [('direct','calls.jsonl','caller'), ('indirect','indirect.jsonl','function')]:
    for _, row in census_rows(INDEX/filename):
        entry = row[field]
        if entry not in all_seeds: continue
        per_entry[entry][kind] += 1
        for key, selected in [('all_selected',all_seeds),('slot_named',slot_named_seeds),('small_named',small_named_seeds)]:
            if entry in selected: counts[key][kind] += 1

source_pins = json.loads((COMPONENT/'packet-inputs.json').read_text())['retained_indexes_verified']
source_pins = {x['path']: x for x in source_pins}
for path, expected in source_pins.items():
    if path in identities:
        actual = identities[path]
        assert actual['bytes'] == expected['bytes'] and actual['sha256'] == expected['sha256']

def seed_summary(selected, key):
    aliases = sum(x in entry_metadata for x in selected)
    return dict(unique_source_entries=len(selected), alias_rows=aliases,
                membership_rows=memberships[key], aliases_plus_memberships=aliases+memberships[key],
                direct=counts[key]['direct'], indirect=counts[key]['indirect'],
                outgoing_plus_indirect=sum(counts[key].values()))

result = dict(
 schema='five-synthesis-family-metadata-census-and-unapproved-scope-v1',
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 status='metadata census only; Root scope decision pending; no raw records retained',
 caps=dict(primary_tables=32,selected_slots=128,stores=128,aliases_plus_memberships=512,
           named_or_call_seeds=128,outgoing_plus_indirect=512),
 broad_census=dict(predicate=BROAD.pattern,address_points=len(broad_tables),
                   distinct_literal_encodings=len({x[0] for x in broad_tables}),
                   exported_prefix_slots=sum(x[1] for x in broad_tables),
                   literal_store_count_annotations=sum(x[2] for x in broad_tables),
                   alias_entries=len(broad_alias),
                   exact_core_token_alias_entries=len(core_alias),
                   limits='Token matches include nested wrappers/UI and unrelated Operator-expression classes; not actual processor/class/function counts.'),
 table_proposal=dict(primary_tables=len(tables),selected_slots=sum(x['proposed_slots'] for x in tables),
                     all_exported_prefix_slots=sum(x['exported_prefix_slots'] for x in tables),
                     large_leading_three=sum(x['selection'].startswith('leading') for x in tables),
                     whole_small_prefixes=sum(x['selection'].startswith('whole') for x in tables),
                     actual_literal_store_rows=store_count,unique_store_entries=len(store_entries),
                     tables=tables,
                     limitation='All recovered address points/slots/stores are metadata candidates only; no receiver, implementation extent, class ABI or public runtime binding.'),
 candidate_seed_censuses={
  'all_selected_tables_stores_named':seed_summary(all_seeds,'all_selected'),
  'all_selected_slots_plus_named_no_store_following':seed_summary(slot_named_seeds,'slot_named'),
  'whole_small_prefix_targets_plus_named_no_large_or_store_following':seed_summary(small_named_seeds,'small_named')},
 named_frontier_rule=dict(core_classes=CORE,method_selector=METHOD.pattern,
                          extra_Wavetable_outer_owner_selector=WT_OWNER.pattern,
                          curve_helper_outer_owner_selector=HELPER.pattern,
                          entries=[named_metadata[e] for e in sorted(named,key=lambda e:int(e,16))],
                          limits='Selectors returned only twelve Operator-qualified wrappers. Missing Drift/Meld/Drum/Wavetable named matches under these exact selectors remain a retained-symbol frontier, not native absence; table metadata supplies separate candidates.'),
 seed_metadata=[dict(entry_metadata.get(e,dict(entry=e,name=None,alias_line=None,thunk=None,thunk_target=None,external=None)), roles=[name for name,ss in [('small-prefix',small_targets),('large-construction-prefix',large_targets),('literal-store-candidate',store_entries),('named-frontier',named)] if e in ss], direct=per_entry[e]['direct'], indirect=per_entry[e]['indirect']) for e in sorted(all_seeds,key=lambda e:int(e,16))],
 metadata_provider_identities=list(identities.values()),
 limitations=['No raw index row retained and no native/C body read; derived metadata summaries only.',
              'No incoming/transitive traversal, encountered-callee expansion, global/slot/native acquisition or original/provider/decoder/harness/model/comparator execution.',
              'No arbitrary first-N seed or slot truncation. Large-prefix restriction is construction/lifetime metadata only; whole typed oscillator specialization set selected coherently.',
              'Call counts are one-hop outgoing and indirect metadata occurrences, not runtime order, resolved dispatch, public routes, new sites or grades.',
              'If all-source seeds exceed cap, stop before retention and request coherent Root selection; narrower semantic alternatives are enumerated, not silently adopted.',
              'All110 requirement IDs/190 actual-U cases remain unchanged; unsupportedU/coverageOPEN/no documentary fallback.'])
out=HERE/'metadata-scope-census.json'
with out.open('x') as stream: json.dump(result,stream,indent=2);stream.write('\n')
print(json.dumps({k:result[k] for k in ['broad_census','candidate_seed_censuses']},indent=2))
print(json.dumps(dict(path=str(out),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest())))
