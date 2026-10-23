"""Fixed retained-index DATA census. No bodies, providers or inherited imports.

Default mode prints scalar census only. Raw retention requires --rows and all
caps passing; exact alias/seed scope must be agreed before that mode is used.
"""
from pathlib import Path
import collections
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
COMP = HERE.parent / 'component-resolution-v1'
INDEX = Path('/var/tmp/sound-analysis/corpus/indexes')
MODELS = ['AAudioEffectGroupDevice','ADrumGroupDevice','AInstrumentGroupDevice',
    'AMidiEffectGroupDevice','AGroupDevice','ADrumBranch','AInstrumentBranch',
    'AMidiEffectBranch','AAudioEffectBranch','AZoneRange','AZoneSettings',
    'ADrumZoneSettings','AMacroSnapshot','AMacroVariations','AMacroParameterUnit',
    'AMacroMapDataModel','AGroupDeviceZoneEditorModel','AGroupDeviceKeyRangeType',
    'AChainSelectorRangeType','ABranchZoneSettingsModule']
SMALL = ['OBranchInProcessor','OBranchOutProcessor','OMidiBranchOutProcessor',
    'OBranchOutSendSerializer','ODrumZoneSettingsProcessor',
    'ODrumGroupDeviceChokeRepeaterProcessor','ODrumPadTranslator',
    'OMidiRackBypassProcessor','OBranchOutSelectorRangeProcessor',
    'AMacroPotiAdaptiveQuantizer','AMacroMappingStringConverter',
    'AChainSelectorStringConverter']
CAPS = dict(tables=32,slots=512,stores=128,alias_memberships=512,call_indirect=512)

def rows(path):
    offset=0
    with path.open('rb') as f:
        for line,raw in enumerate(f,1):
            yield json.loads(raw),dict(path=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                line=line,byte_start=offset,bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest())
            offset+=len(raw)

def main():
    if sys.argv[1:] not in [[],['--rows']]:raise SystemExit('Only scalar census or --rows after agreed cap-safe selection.')
    model={str(len(x))+x for x in MODELS};small={str(len(x))+x for x in SMALL}
    selected=[];points=set();frontier=set();available=slots=0
    for rec,loc in rows(COMP/'class-tables.jsonl'):
        name=rec['literal_type_encoding']
        if name not in model|small or rec['offset_to_top']!=0:continue
        r=dict(rec);available+=len(r['slots'])
        if name in model:r['slots']=r['slots'][:3]
        slots+=len(r['slots']);points.add(r['address_point'])
        frontier.update(s['target'] for s in r['slots'])
        r.update(available_exported_prefix_slots=len(rec['slots']),selection='leading-three-or-less-model' if name in model else 'whole-exported-small-prefix',
            complete_class_function_or_role_established=False,actual_public_instance_established=False)
        selected.append(dict(kind='table-prefix',locator=loc,record=r))
    stores=[]
    for r,l in rows(COMP/'class-stores.jsonl'):
        if r['address_point'] in points:stores.append(dict(kind='store-candidate',locator=l,record=r));frontier.add(r['entry'])
    pattern=re.compile(r'(?:^|[^A-Za-z0-9_])(?:'+'|'.join(map(re.escape,MODELS+SMALL))+r')::')
    aliases=[];named=set()
    for r,l in rows(INDEX/'aliases.jsonl'):
        is_named=any(pattern.search(n) for n in [r['name']]+[x['name'] for x in r['symbols']])
        if is_named:named.add(r['entry'])
        if is_named or r['entry'] in frontier:aliases.append(dict(kind='alias',locator=l,record=r))
    memberships=[]
    for r,l in rows(COMP/'symbol-memberships.jsonl'):
        if r.get('entry') in named:memberships.append(dict(kind='membership',locator=l,record=r))
    counts=dict(tables=len(selected),slots=slots,available_slots=available,stores=len(stores),aliases=len(aliases),memberships=len(memberships),
        alias_memberships=len(aliases)+len(memberships),named_seed_entries=len(named),slot_store_frontier_entries=len(frontier))
    # Refuse call-index expansion when the prerequisite alias cap already fails.
    calls=[]
    if counts['alias_memberships']<=CAPS['alias_memberships']:
        for filename,kind,key in [('calls.jsonl','call','caller'),('indirect.jsonl','indirect','function')]:
            for r,l in rows(INDEX/filename):
                if r[key] in named:calls.append(dict(kind=kind,locator=l,record=r))
        counts.update(call_indirect=len(calls),calls=sum(x['kind']=='call' for x in calls),indirect=sum(x['kind']=='indirect' for x in calls))
    else:counts.update(call_indirect=None,calls=None,indirect=None)
    within=all(counts[k] is not None and counts[k]<=v for k,v in CAPS.items())
    census=dict(scope='Root-approved 32 primary associations; exact-owner named aliases and slot/store aliases, named-entry memberships and outgoing indexed rows; caps verified before raw retention.',models=MODELS,small=SMALL,
        primary_offset_to_top=0,counts=counts,caps=CAPS,within_caps=within,named_seeds=sorted(named),frontier_entries=sorted(frontier),
        new_native_site_credit=0,actual_public_route=False,selected_successor=None)
    if sys.argv[1:]==['--rows']:
        if not within:raise SystemExit('Caps not met; no rows emitted. Report and agree semantic scope first.')
        for i,r in enumerate(selected+stores+aliases+memberships+calls,1):print(json.dumps(dict(id=f'RCK-M{i:04}',**r),separators=(',',':')))
    else:print(json.dumps(census,indent=2))

if __name__=='__main__':main()
