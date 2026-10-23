"""Fixed Root-approved retained-index query. Metadata only; no body/tool imports."""
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
COMPONENT = HERE.parent / 'component-resolution-v1'
INDEX = Path('/var/tmp/sound-analysis/corpus/indexes')
PROPOSAL_SHA = 'b29fadf8ccd7c7fa403aacf58a8d74312c971636e5ada50a2b1ddf6a11768430'
APPROVAL_SHA = 'bbecac079bb0aa6ca570a178f7f8a6d9c92e873fa348b289121352c513d888b9'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def select(path, kind, predicate, project=lambda d: d):
    result = []
    offset = 0
    with path.open('rb') as source:
        for number, raw in enumerate(source, 1):
            row = json.loads(raw)
            if predicate(row):
                result.append(dict(kind=kind, provider=str(path), source_line=number,
                                   source_byte=offset, raw_bytes=len(raw),
                                   raw_sha256=digest(raw), record=project(row)))
            offset += len(raw)
    return result


def table_projection(row):
    result = dict(row)
    size = len(row['slots'])
    result['exported_prefix_slot_count'] = size
    result['slots'] = row['slots'][:3] if size > 16 else row['slots']
    result['selection_policy'] = ('large leading3 construction/lifetime frontier only'
                                  if size > 16 else 'whole small exported prefix')
    result['complete_native_table_class_function_or_processing_claim'] = False
    return result


def main():
    if sys.argv[1:] not in ([], ['--rows']):
        raise SystemExit('Only fixed census or --rows stdout is supported')
    proposal_raw = (HERE / 'census-proposal.json').read_bytes()
    approval_raw = (HERE / 'scope-approval-root.json').read_bytes()
    if digest(proposal_raw) != PROPOSAL_SHA or digest(approval_raw) != APPROVAL_SHA:
        raise SystemExit('Scope identity changed; no metadata selection')
    proposal, approval = json.loads(proposal_raw), json.loads(approval_raw)
    scope = proposal['proposed_classes']['classes']
    pairs = {(x['type'], x['address_point']) for x in scope}
    types = {x['type'] for x in scope}
    names = [re.fullmatch(r'\d+(.+)', x['type'])[1] for x in scope]
    names += ['LAutoPan2', 'LAutoShift', 'LChorus2', 'LPhaserNew',
              'LShifter', 'LTransmute', 'LSpectralTime']
    owner_pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(map(re.escape, names))
                               + r')(?![A-Za-z0-9_])')
    tables = select(COMPONENT / 'class-tables.jsonl', 'table-data',
                    lambda r: (r['literal_type_encoding'], r['address_point']) in pairs
                    and r['offset_to_top'] == 0, table_projection)
    rtti = select(COMPONENT / 'class-rtti.jsonl', 'RTTI-data',
                  lambda r: r['literal_type_encoding'] in types)
    points = {r['record']['address_point'] for r in tables}
    stores = select(COMPONENT / 'class-stores.jsonl', 'store-data',
                    lambda r: r['address_point'] in points)
    owners = select(COMPONENT / 'symbol-owners.jsonl', 'lexical-owner-data',
                    lambda r: bool(owner_pattern.search(r.get('lexical_owner') or ''))
                    and not (r.get('lexical_owner') or '').startswith(('boost::', 'std::', 'flip::')))
    scopes = {r['record']['scope_id'] for r in owners}
    members = select(COMPONENT / 'symbol-memberships.jsonl', 'membership-data',
                     lambda r: any(c[1] in scopes for c in r.get('candidates', [])))
    entries = {r['record']['entry'] for r in members}
    aliases = select(INDEX / 'aliases.jsonl', 'alias-data', lambda r: r['entry'] in entries)
    excluded_method = re.compile(r'::(?:OnActiveViewCountChanged|OnActiveViewCount|'
                                 r'OnAllowTextVisualizationUpdateTimer|OnUpdateDisplay|OnTimer)(?=>)')
    excluded = {r['record']['entry'] for r in aliases if excluded_method.search(r['record']['name'])}
    if excluded != set(approval['exact_seed_exclusions']):
        raise SystemExit('Exact UI method-group exclusions changed')
    seeds = entries - excluded
    calls = select(INDEX / 'calls.jsonl', 'call-data', lambda r: r['caller'] in seeds)
    indirect = select(INDEX / 'indirect.jsonl', 'indirect-data',
                      lambda r: r.get('function') in seeds or r.get('caller') in seeds)
    counts = dict(primary_tables=len(tables), selected_slots=sum(len(r['record']['slots']) for r in tables),
                  stores=len(stores), aliases_plus_memberships=len(aliases)+len(members),
                  named_seeds=len(seeds), outgoing_direct_plus_indirect=len(calls)+len(indirect))
    if counts != approval['counts']:
        raise SystemExit('Approved fixed counts changed; no retained output')
    if [len(owners), len(members), len(aliases), len(rtti), len(calls), len(indirect)] != [120,133,133,32,160,27]:
        raise SystemExit('Selected row-kind counts changed; no retained output')
    all_rows = owners + members + aliases + rtti + tables + stores + calls + indirect
    if sys.argv[1:] == ['--rows']:
        for row in all_rows:
            print(json.dumps(row, ensure_ascii=False, separators=(',', ':')))
    else:
        print(json.dumps(dict(status='fixed-approved-metadata-census', counts=counts,
                              selected_DATA_rows=len(all_rows), lexical_scopes=len(owners),
                              aliases=len(aliases), memberships=len(members), RTTI=len(rtti),
                              direct_outgoing=len(calls), indirect=len(indirect),
                              exported_prefix_slots_metadata_only=sum(r['record']['exported_prefix_slot_count'] for r in tables),
                              large_leading3=sum(r['record']['exported_prefix_slot_count']>16 for r in tables),
                              whole_small=sum(r['record']['exported_prefix_slot_count']<=16 for r in tables),
                              no_incoming_or_transitive_expansion=True, new_C_bodies=0,
                              new_native_windows=0, new_resolved_site_credit=0), indent=2))


if __name__ == '__main__':
    main()
