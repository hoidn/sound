"""Fixed metadata-only census/row projection; no body/native/provider execution."""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
COMP = HERE.parent / 'component-resolution-v1'
INDEX = Path('/var/tmp/sound-analysis/corpus/indexes')
MODELS = ['ADrumBuss','ATube','AErosion2','AOverdrive','APedal','ARedux2','ARoar','ASaturator','AVinyl']
PROCESSORS = ['ODrumBussProcessor','OTubeProcessor','OErosion2Processor','OOverdriveProcessor','OPedalProcessor','ORedux2Processor','ORoarProcessor','OSaturatorProcessor','OVinylProcessor']
HELPERS = ['TRoarFilterCurveHelper','TRoarLfoCurveHelper','TRoarEnvelopeCurveHelper','TRoarNoiseCurveHelper','TRoarScopeCurveHelper','TRoarShaperCurveHelper','TSaturatorShaperCurveHelper']
WRAPPERS = ['29ODeviceKitSampleRateProcessorIN7ableton7devices8erosion214Erosion2DeviceEE','29ODeviceKitSampleRateProcessorIN7ableton7devices6redux212Redux2DeviceEE','29ODeviceKitSampleRateProcessorIN7ableton7devices4roar10RoarDeviceEE','29ODeviceKitSampleRateProcessorIN7ableton7devices9saturator15SaturatorDeviceEE']
ENCODINGS = {str(len(x))+x for x in MODELS+PROCESSORS+HELPERS} | set(WRAPPERS)
OWNER_RX = re.compile(r'(?<![A-Za-z0-9_])(?:'+ '|'.join(map(re.escape, MODELS+PROCESSORS+HELPERS)) +r')::|ODeviceKitSampleRateProcessor<ableton::devices::(?:erosion2::Erosion2Device|redux2::Redux2Device|roar::RoarDevice|saturator::SaturatorDevice)>::')
METHOD_RX = re.compile(r'::(?:Init|Exit|Reset|NewRate|CalcMain|CalculateCurve|GetCurve|GetShape|ComputeCurve)(?:\(|>)')
UPDATE_RX = re.compile(r'::(?:OnUpdateData|OnVisualizationData|OnLfoDataChanged|OnShaperParameter)(?:>|\()')


def scan(path, predicate):
    offset = 0
    with path.open('rb') as stream:
        for number, raw in enumerate(stream, 1):
            row = json.loads(raw)
            if predicate(row):
                yield row, dict(path=str(path),line=number,byte_start=offset,bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest())
            offset += len(raw)


def compute():
    rows = []
    def retain(kind, row, loc):
        rows.append(dict(kind=kind,locator=loc,record=row))
    tables = []
    for original, loc in scan(COMP/'class-tables.jsonl',lambda r:r['literal_type_encoding'] in ENCODINGS and r['offset_to_top']==0):
        row = dict(original)
        row['available_exported_prefix_slots'] = len(original['slots'])
        model = original['literal_type_encoding'] in {str(len(x))+x for x in MODELS}
        row['slots'] = original['slots'][:3] if model else original['slots']
        row['selection'] = 'leading-three-or-less-primary-model-construction-frontier' if model else 'whole-exported-small-processor-wrapper-curve-prefix'
        row['complete_class_or_processing_interface_established'] = False
        row['actual_public_instance_established'] = False
        tables.append(row)
        retain('table-prefix',row,loc)
    points = {r['address_point'] for r in tables}
    stores = []
    for row,loc in scan(COMP/'class-stores.jsonl',lambda r:r['address_point'] in points):
        stores.append(row);retain('store-candidate',row,loc)
    frontier = {s['target'] for r in tables for s in r['slots']} | {r['entry'] for r in stores}
    named = set(); seeds = set(); updates = set(); aliases = []; broad_aliases = 0
    for row,loc in scan(INDEX/'aliases.jsonl',lambda r:True):
        labels = [row.get('name',''),*[x.get('name','') for x in row.get('symbols',[])]]
        owned = any(OWNER_RX.search(x) for x in labels)
        if owned:
            named.add(row['entry'])
            if any(OWNER_RX.search(x) and METHOD_RX.search(x) for x in labels):seeds.add(row['entry'])
            if any(any(n+'::' in x for n in HELPERS) and UPDATE_RX.search(x) for x in labels):updates.add(row['entry'])
        if owned or row['entry'] in frontier:broad_aliases += 1
        if row['entry'] in seeds or row['entry'] in updates or row['entry'] in frontier:
            aliases.append(row);retain('alias',row,loc)
    seeds |= updates
    aliasentries = {x['entry'] for x in aliases}
    members = []
    broad_members = 0
    for row,loc in scan(COMP/'symbol-memberships.jsonl',lambda r:r.get('entry') in named):
        broad_members += 1
        if row['entry'] not in seeds:continue
        members.append(row);retain('membership',row,loc)
    calls = []
    for row,loc in scan(INDEX/'calls.jsonl',lambda r:r['caller'] in seeds):
        calls.append(row);retain('call',row,loc)
    indirect = []
    for row,loc in scan(INDEX/'indirect.jsonl',lambda r:r.get('function') in seeds or r.get('caller') in seeds):
        indirect.append(row);retain('indirect',row,loc)
    counts = dict(tables=len(tables),selected_slots=sum(len(x['slots']) for x in tables),available_prefix_slots=sum(x['available_exported_prefix_slots'] for x in tables),stores=len(stores),aliases=len(aliases),memberships=len(members),combined_alias_memberships=len(aliases)+len(members),named_alias_entries=len(named),boundary_seeds=len(seeds),call_rows=len(calls),indirect_rows=len(indirect),call_indirect=len(calls)+len(indirect))
    caps = dict(tables=32,selected_slots=512,stores=128,combined_alias_memberships=512,call_indirect=512)
    ok = all(counts[k]<=v for k,v in caps.items()) and len(tables)==29
    census = dict(schema='distortion-fixed29-primary-census-v1',scope_authority='Root approved29primarytable semantic scope and narrowed all95frontier+32boundary+all9visualization-update alias selection before retention; no arbitrary name truncation.',broad_navigation=dict(tables=324,available_prefix_slots=9695,retained=False),broad_exact_owner_alias_census=dict(aliases=broad_aliases,memberships=broad_members,combined=broad_aliases+broad_members,retained=False),models=MODELS,processors=PROCESSORS,wrappers=WRAPPERS,curve_helpers=HELPERS,encodings=sorted(ENCODINGS),counts=counts,caps=caps,within_caps=ok,retained_before_census=False,frontier_entries=sorted(frontier),frontier_without_exact_alias=sorted(frontier-aliasentries),boundary_seeds=sorted(seeds),selected_visualization_updates=sorted(updates),unselected_named_alias_entries=len(named-seeds),seed_rule=METHOD_RX.pattern+' OR helper '+UPDATE_RX.pattern,alias_rule=OWNER_RX.pattern,curve_helper_alias_names=[x['name'] for x in aliases if any(n+'::' in x['name'] for n in HELPERS)],table_summary=[dict(encoding=x['literal_type_encoding'],point=x['address_point'],available=x['available_exported_prefix_slots'],selected=len(x['slots'])) for x in tables],exclusions='Secondary model addresspoints;legacyErosion/Redux candidates;view/proxy/AMember/Push/Python/GUI/Looper classes;other lexical callbacks. Not nativeabsence or publicoutcome exclusions.',selected_successor=None,new_body_native_original_reads=0)
    return census,rows


if __name__ == '__main__':
    if sys.argv[1:] not in [[],['--rows']]:raise SystemExit('Only census default or capped --rows; no bodies/native calls.')
    census,rows=compute()
    if sys.argv[1:]:
        if not census['within_caps']:raise SystemExit('CAP EXCESS: no rows emitted')
        for i,row in enumerate(rows,1):print(json.dumps(dict(id=f'DSM-{i:03}',**row),separators=(',',':')))
    else:print(json.dumps(census,indent=2))
