"""Retained DATA only: fixed approved scope, census before bounded row retention."""
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
F = HERE.parent
C = F / 'component-resolution-v1'
I = Path('/var/tmp/sound-analysis/corpus/indexes')
NAMES = '''ODelayProcessor OEchoProcessor OFilterDelayProcessor OFilterDelayAddProcessor
OGrainDelayProcessor OReverbProcessor OResonatorProcessor ADelay LDelay ADelayModule
AEcho LEcho AEchoModule TEchoLfoCurveHelper AFilterDelay LFilterDelay AFilterDelayUnit
AGrainDelay LGrainDelay AReverb LReverb AReverbModule AResonator LResonator AResonatorUnit
THybridReverbDevicePyHandle'''.split()
ENC = {str(len(n)) + n for n in NAMES} | {
    'N7ableton15push_live_model18HybridReverbDeviceE',
    'N4flip6VectorIN7ableton15push_live_model18HybridReverbDevice23Vector_ir_category_listEEE',
    'N4flip6VectorIN7ableton15push_live_model18HybridReverbDevice19Vector_ir_file_listEEE'}


def scan(path, kind, select, project=None):
    out, offset = [], 0
    with path.open('rb') as stream:
        for line, raw in enumerate(stream, 1):
            d = json.loads(raw)
            if select(d):
                out.append(dict(kind=kind, provider=str(path), source_line=line,
                                source_byte=offset, raw_bytes=len(raw),
                                raw_sha256=hashlib.sha256(raw).hexdigest(),
                                record=project(d) if project else d))
            offset += len(raw)
    return out


def main():
    def projection(d):
        r = dict(d)
        r['exported_prefix_slot_count'] = len(d['slots'])
        r['selected_slot_policy'] = ('large header/store plus leading3 construction/lifetime prefix only'
                                     if len(d['slots']) > 16 else 'whole small retained exported prefix')
        r['slots'] = d['slots'][:3] if len(d['slots']) > 16 else d['slots']
        r['not_complete_native_extent_or_render_callback'] = True
        return r
    tables = scan(C/'class-tables.jsonl', 'table-data',
                  lambda d:d['literal_type_encoding'] in ENC and d['offset_to_top'] == 0, projection)
    points = {r['record']['address_point'] for r in tables}
    rtti = scan(C/'class-rtti.jsonl', 'RTTI-data', lambda d:d['literal_type_encoding'] in ENC)
    stores = scan(C/'class-stores.jsonl', 'store-data', lambda d:d['address_point'] in points)
    rx = re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(map(re.escape,NAMES))+r')(?![A-Za-z0-9_])')
    owners = scan(C/'symbol-owners.jsonl', 'lexical-owner-data',
                  lambda d:bool(rx.search(d.get('lexical_owner') or '')) and
                  not (d.get('lexical_owner') or '').startswith(('boost::','std::','flip::')))
    scopes = {r['record']['scope_id'] for r in owners}
    members = scan(C/'symbol-memberships.jsonl', 'membership-data',
                   lambda d:any(c[1] in scopes for c in d.get('candidates',[])))
    entries = {r['record']['entry'] for r in members}
    aliases = scan(I/'aliases.jsonl', 'alias-data', lambda d:d['entry'] in entries)
    calls = scan(I/'calls.jsonl', 'call-data',
                 lambda d:d['caller'] in entries or d.get('callee') in entries or d.get('to') in entries)
    indirect = scan(I/'indirect.jsonl', 'indirect-data',
                    lambda d:d.get('function') in entries or d.get('caller') in entries)
    counts = dict(tables=len(tables), selected_slots=sum(len(r['record']['slots']) for r in tables),
                  full_exported_slots_metadata_only=sum(r['record']['exported_prefix_slot_count'] for r in tables),
                  large_header_prefix3=sum(r['record']['exported_prefix_slot_count'] > 16 for r in tables),
                  RTTI_rows=len(rtti),stores=len(stores),owners=len(owners),aliases=len(aliases),
                  memberships=len(members),aliases_plus_memberships=len(aliases)+len(members),
                  calls=len(calls),indirect=len(indirect),calls_plus_indirect=len(calls)+len(indirect))
    within = (counts['tables'] <= 32 and counts['selected_slots'] <= 512 and counts['stores'] <= 128
              and counts['aliases_plus_memberships'] <= 512 and counts['calls_plus_indirect'] <= 512)
    census = dict(schema='delay-reverb-fixed-retained-metadata-census-v1',
                  exact_type_encodings=sorted(ENC), lexical_tokens=NAMES,
                  preliminary_queries=[
                      dict(query='casefold substring delay/reverb/echo/resonator',tables=380,
                           full_prefix_slots=8123,primary=267,retained=False,
                           caveat='Echo substring includes Chooser; not a class-family count'),
                      dict(query='case-sensitive simple token candidate regex',tables=132,
                           full_prefix_slots=4961,policy_slots=465,retained=False,
                           caveat='Regex alone also accepts mangled templates; not exact simple-class count'),
                      dict(query='leading decimal component length equals whole remaining simple name',
                           primary_tables=100,retained=False)],
                  authorization='Root explicitly approved semantic29table/91slot/43store/264alias-membership/195call-indirect scope before retention.',
                  caps=dict(tables=32,selected_slots=512,stores=128,
                            aliases_plus_memberships=512,calls_plus_indirect=512),
                  counts=counts,within_caps=within, new_C_bodies=0,new_traversal=False,
                  selected_table_summary=[dict(type=r['record']['literal_type_encoding'],
                                               address_point=r['record']['address_point'],
                                               exported_slots=r['record']['exported_prefix_slot_count'],
                                               selected_slots=len(r['record']['slots']),source_line=r['source_line'],
                                               raw_sha256=r['raw_sha256']) for r in tables],
                  exclusions='Generic compensation/audio-MIDI delay infrastructure, Looper, Collision/Meld, Push renderers, broad converters and UI view tables. Required UI/compensation/lifecycle joins remain unknown, not excluded outcomes.',
                  Hybrid_limit='PyHandle/push model/list vectors are API/list metadata, not actual Hybrid processor/IR loading/availability or engine binding.')
    predicates = [
        "any(s in literal_type_encoding.lower() for s in ['delay','reverb','echo','resonator']); all offset_to_top values; primary separately offset_to_top==0",
        "offset_to_top==0 and re.fullmatch(r'\\d+[A-Za-z_][A-Za-z0-9_]*',literal_type_encoding) and any(t in literal_type_encoding for t in ['Delay','Reverb','Echo','Resonator'])",
        "offset_to_top==0 and re.match(r'^(\\d+)(.*)$',literal_type_encoding) with len(group2)==int(group1) and case-sensitive Delay/Reverb/Echo/Resonator token inclusion"]
    for query, predicate in zip(census['preliminary_queries'],predicates,strict=True):
        query['exact_predicate'] = predicate
    census['preliminary_provider'] = 'component-resolution-v1/class-tables.jsonl; full identity in source-pins.json'
    if sys.argv[1:] == ['--rows']:
        if not within:
            raise SystemExit('CAP EXCESS: no rows retained; report complete census')
        if [counts[k] for k in ['tables','selected_slots','stores','aliases_plus_memberships','calls_plus_indirect']] != [29,91,43,264,195]:
            raise SystemExit('APPROVED SCOPE CHANGED: stop before retention')
        for r in owners+members+aliases+rtti+tables+stores+calls+indirect:
            print(json.dumps(r,separators=(',',':')))
    elif not sys.argv[1:]:
        print(json.dumps(census,indent=2))
    else:
        raise SystemExit('Only census or fixed approved --rows is supported')


if __name__ == '__main__':
    main()
