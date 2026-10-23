#!/usr/bin/env python3
"""Pinned retained-index lexical inventory; no traversal, binary access or demangling."""
import collections
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
HERE = pathlib.Path(__file__).resolve().parent
INDEX = pathlib.Path('/var/tmp/sound-analysis/corpus/indexes')
MANIFEST = ROOT / 'analysis/ableton-live-12.4.3/r2/c1-live-v1/indexes-manifest.json'
TERMS = re.compile(r'Song|Track|Clip|Sequenc|Transport|Mix|Device|Engine|Document|Audio|Midi|MIDI|Render|Export|Record|Automation|Warp|Sample|File|Session|Arrangement|Scene|Player|Playback')


def digest(b):
    return hashlib.sha256(b).hexdigest()


def encoded_prefix(value):
    """Accept only complete simple length-prefixed name syntax; templates and ABI types stay unknown."""
    s = value[4:] if value.startswith('_ZTS') else value
    nested = s.startswith('N')
    if nested:
        if not s.endswith('E'):
            return None
        s = s[1:-1]
    names = []
    while s:
        m = re.match(r'([1-9][0-9]*)', s)
        if not m:
            return None
        n = int(m.group())
        tail = s[len(m.group()):]
        name = tail[:n]
        if n > len(tail) or not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', name):
            return None
        names.append(name)
        s = tail[n:]
        if not nested and s:
            return None
    return names[0] if names else None



def scope(name):
    """Top-level lexical separators only; owner may be namespace OR class."""
    if '::' not in name:
        return None
    if name.startswith('/'):
        return {'root': name.split('::', 1)[0], 'owner': None, 'category': 'library-path'}
    angle = paren = bracket = 0
    separators = []
    i = 0
    while i < len(name):
        c = name[i]
        if c == '<':
            angle += 1
        elif c == '>':
            angle -= 1
            if angle < 0:
                return {'root': None, 'owner': None, 'category': 'syntax-ambiguous'}
        elif not angle:
            if c == '(':
                paren += 1
            elif c == ')':
                paren -= 1
            elif c == '[':
                bracket += 1
            elif c == ']':
                bracket -= 1
            if name[i:i+2] == '::' and not paren and not bracket:
                separators.append(i)
                i += 1
        i += 1
    if angle or paren or bracket:
        return {'root': None, 'owner': None, 'category': 'syntax-ambiguous'}
    if not separators:
        return {'root': None, 'owner': None, 'category': 'nested-qualifier-only'}
    owner = name[:separators[-1]]
    root = name[:separators[0]]
    if not owner or ' ' in root or root.startswith(('thunk_', '__')):
        return {'root': None, 'owner': owner, 'category': 'owner-ambiguous'}
    return {'root': root, 'owner': owner, 'category': 'lexical-owner'}


def selfcheck():
    assert scope('ableton::audio::Player::Run')['owner'] == 'ableton::audio::Player'
    assert scope('flip::Box<std::string>::Read')['root'] == 'flip'
    assert scope('Box<std::string>')['category'] == 'nested-qualifier-only'
    assert scope('Box<std::string>::Read')['root'] == 'Box<std::string>'
    assert scope('/usr/lib/libc++.1.dylib::operator.delete')['category'] == 'library-path'
    assert scope('FUN_100000000') is None
    assert scope('broken<T::F')['category'] == 'syntax-ambiguous'
    assert scope('Type::operator<')['category'] == 'syntax-ambiguous'
    assert encoded_prefix('N7ableton5audioE') == 'ableton'
    assert encoded_prefix('11AStereoGain') == 'AStereoGain'
    assert encoded_prefix('_ZTS11AStereoGain') == 'AStereoGain'
    assert encoded_prefix('999short') is None
    assert encoded_prefix('12345') is None
    assert encoded_prefix('11AStereoGainEPv') is None
    assert encoded_prefix('N7ableton5audioEgarbage') is None
    assert encoded_prefix('N7ableton3BoxIiEE') is None


def build():
    selfcheck()
    manifest_bytes = MANIFEST.read_bytes()
    manifest = json.loads(manifest_bytes)
    sources = {}
    outputs = {n: [] for n in ('memberships', 'owners', 'string-candidates')}
    counts = collections.Counter()
    names_all = set()
    literal_names = set()
    literal_functions = set()
    entries = set()
    owner_functions = collections.defaultdict(set)
    owner_names = collections.defaultdict(set)
    root_functions = collections.defaultdict(set)
    root_names = collections.defaultdict(set)
    category_functions = collections.defaultdict(set)
    multi_owner = 0
    remainder = collections.Counter()
    scopes = {}
    scope_functions = collections.defaultdict(set)
    scope_names = collections.defaultdict(set)
    vtable_functions = set()
    type_prefixes = collections.Counter()
    raw_root_occurrences = collections.Counter()
    raw_prefix_functions = collections.defaultdict(set)
    raw_prefix_names = collections.defaultdict(set)
    input_paths = [MANIFEST] + [INDEX / n for n in ('aliases.jsonl', 'vtables.jsonl', 'strings.jsonl')]
    initial_stats = {str(p): (p.stat().st_size, p.stat().st_mtime_ns, p.stat().st_ino) for p in input_paths}

    def rows(filename):
        path = INDEX / filename
        before = path.stat()
        h = hashlib.sha256()
        offset = 0
        line = 0
        with path.open('rb') as f:
            for raw in f:
                line += 1
                h.update(raw)
                obj = json.loads(raw)
                yield obj, {'line': line, 'byte': offset, 'length_including_LF': len(raw)}
                offset += len(raw)
        expected = manifest['files'][filename]
        assert (line, offset, h.hexdigest()) == (expected['lines'], expected['bytes'], expected['sha256'])
        after = path.stat()
        assert (before.st_size, before.st_mtime_ns, before.st_ino) == (after.st_size, after.st_mtime_ns, after.st_ino)
        sources[filename] = {'path': str(path), **expected, 'read_passes_this_run': 1, 'stat_unchanged': True}

    for row, loc in rows('aliases.jsonl'):
        entry = row['entry']
        assert entry not in entries
        entries.add(entry)
        counts['alias_rows'] += 1
        counts['external_rows'] += bool(row['external'])
        counts['thunk_rows'] += bool(row['thunk'])
        selected = []
        owners = set()
        counts['primary_name_also_in_symbols_rows'] += any(row['name'] == v['name'] for v in row['symbols'])
        labels = [('name', row['name'])] + [(f'symbols/{i}/name', sym['name']) for i, sym in enumerate(row['symbols'])]
        seen_labels = set()
        for field, name in labels:
            counts['primary_name_literal_qualified_rows'] += field == 'name' and '::' in name
            counts['symbols_literal_qualified_occurrences'] += field != 'name' and '::' in name
            for raw_root in ('ableton', 'flip', 'boost', 'std'):
                if name.startswith(raw_root + '::'):
                    raw_root_occurrences[raw_root] += 1
                    raw_prefix_functions[raw_root].add(entry)
                    raw_prefix_names[raw_root].add(name)
            if name in seen_labels:
                continue
            seen_labels.add(name)
            names_all.add(name)
            counts['distinct_label_occurrences_within_row'] += 1
            found = scope(name)
            if found is None:
                continue
            literal_names.add(name)
            literal_functions.add(entry)
            counts['literal_qualified_symbol_occurrences'] += 1
            category_functions[found['category']].add(entry)
            scope_key = (found['root'], found['owner'], found['category'])
            scope_id = scopes.setdefault(scope_key, len(scopes))
            selected.append([field, scope_id])
            scope_functions[scope_id].add(entry)
            scope_names[scope_id].add(name)
            if found['category'] == 'lexical-owner':
                owner = found['owner']
                root = found['root']
                owners.add(owner)
                owner_functions[owner].add(entry)
                owner_names[owner].add(name)
                root_functions[root].add(entry)
                root_names[root].add(name)
        if selected:
            outputs['memberships'].append({'kind': 'alias_membership', 'entry': entry, 'source': [loc['line'], loc['byte'], loc['length_including_LF']], 'candidates': selected, 'multiple_lexical_owners': len(owners) > 1})
        else:
            reason = 'generated-primary' if re.fullmatch(r'(?:thunk_)?FUN_[0-9a-fA-F]+', row['name']) else 'unqualified-primary'
            remainder[reason] += 1
        multi_owner += len(owners) > 1
    # Unqualified rows remain exactly the pinned alias-source complement, not a duplicate index.
    for (root, owner, category), scope_id in scopes.items():
        outputs['owners'].append({'scope_id': scope_id, 'lexical_root': root, 'lexical_owner': owner, 'category': category, 'namespace_or_class': 'undetermined', 'distinct_functions': len(scope_functions[scope_id]), 'distinct_names': len(scope_names[scope_id]), 't1_name_token_candidate': bool(owner and TERMS.search(owner))})
    for row, loc in rows('vtables.jsonl'):
        slots = []
        for i, slot in enumerate(row['slots']):
            vtable_functions.add(slot['function'])
            slots.append({'slot_index': i, 'physical_export_offset': slot['offset'], 'function': slot['function'], 'name_scope': scope(slot['function_name'])})
        outputs['memberships'].append({'kind': 'exported_vtable_labels', 'address': row['address'], 'source': loc, 'symbols': row['symbols'], 'export_stop': row['stop'], 'slots': slots, 'runtime_class_or_extent_proved': False})
        counts['vtable_rows'] += 1
        counts['exported_vtable_slots'] += len(slots)
    for row, loc in rows('strings.jsonl'):
        counts['string_rows'] += 1
        value = row.get('value', '')
        prefix = encoded_prefix(value)
        if prefix is None and not value.startswith(('_ZTV', '_ZTS')):
            continue
        type_prefixes[prefix or 'unparsed-ZTV-ZTS'] += 1
        outputs['string-candidates'].append({'kind': 'mangled_name_syntax_candidate', 'tuple': [row['address'], loc['line'], loc['byte'], loc['length_including_LF'], digest(value.encode()), len(value), prefix, len(row.get('refs', [])), value[:4] if value.startswith(('_ZTV', '_ZTS')) else None]})
    assert initial_stats == {str(p): (p.stat().st_size, p.stat().st_mtime_ns, p.stat().st_ino) for p in input_paths}
    assert MANIFEST.read_bytes() == manifest_bytes
    assert len(literal_functions) + sum(remainder.values()) == len(entries)
    assert all(len(v) <= len(entries) for v in root_functions.values())
    root_inventory = [{'lexical_root': r, 'distinct_names': len(root_names[r]), 'distinct_functions': len(root_functions[r])} for r in sorted(root_functions, key=lambda r: (-len(root_functions[r]), r))]
    useful = [r for r in outputs['owners'] if r['t1_name_token_candidate'] and r['category'] == 'lexical-owner']
    useful.sort(key=lambda r: (-r['distinct_functions'], r['lexical_owner']))
    summary = {
        'schema': 1, 'claim': 'Observed lexical index inventory only; candidate class memberships are not receiver proofs or semantic components.',
        'manifest': {'path': str(MANIFEST), 'sha256': digest(manifest_bytes), 'program': manifest['program'], 'executable_sha256': manifest['executable_sha256']},
        'sources': sources, 'counts': dict(counts), 'distinct_alias_entries': len(entries), 'distinct_symbol_names': len(names_all),
        'literal_double_colon_distinct_names': len(literal_names), 'literal_double_colon_distinct_functions': len(literal_functions),
        'distinct_lexical_owners': len(owner_functions), 'functions_with_multiple_lexical_owners': multi_owner,
        'category_function_counts_overlapping': {k: len(v) for k, v in sorted(category_functions.items())},
        'remainder_function_counts': dict(sorted(remainder.items())),
        'namespace_roots': root_inventory,
        'raw_primary_plus_symbols_literal_qualified_occurrences': counts['primary_name_literal_qualified_rows'] + counts['symbols_literal_qualified_occurrences'],
        'raw_primary_plus_symbols_requested_root_prefix_occurrences': dict(raw_root_occurrences),
        'requested_literal_prefixes_distinct': {r: {'distinct_functions': len(raw_prefix_functions[r]), 'distinct_names': len(raw_prefix_names[r])} for r in ('ableton', 'flip', 'boost', 'std')},
        'whole_derivation_four_input_stats_unchanged': True,
        'named_requested_roots': {r: {'distinct_names': len(root_names[r]), 'distinct_functions': len(root_functions[r])} for r in ('ableton', 'flip', 'boost', 'std')},
        't1_lexical_owner_candidates_top100': useful[:100], 't1_lexical_owner_candidate_count': len(useful),
        'exported_vtable_distinct_target_values': len(vtable_functions), 'type_name_syntax_candidate_rows': len(outputs['string-candidates']), 'string_rows_outside_selected_simple_name_syntax': counts['string_rows'] - len(outputs['string-candidates']),
        'type_name_first_component_top100': type_prefixes.most_common(100), 'string_candidate_tuple_fields': ['address', 'line', 'byte', 'length_including_LF', 'value_sha256_utf8', 'value_characters', 'length_prefixed_first_component', 'reference_count', 'ZTV_ZTS_prefix_or_null'],
        'definitions': {'name_count': 'distinct exact labels across primary name and symbols[].name; equal labels in one row deduplicated, field provenance retained' , 'function_count': 'distinct aliases entry keys including external and thunk rows; no claim all rows are native function bodies', 'owner': 'prefix before final top-level :: outside templates/parentheses/brackets; class vs namespace undetermined', 'root': 'prefix before first such separator; no demangler, alias equivalence, namespace semantic interpretation or hierarchy inference', 'remainder': 'all alias entries with no primary or symbol label containing literal ::; counts retained, exact entries/labels/locators are the complement of alias_membership rows in pinned aliases.jsonl; not discarded or classified' , 'membership_candidates': 'pairs [label_field, scope_id]; scope_id resolves in symbol-owners.jsonl, no hierarchy or semantic identity implied', 'membership_source_tuple': '[one-based line, zero-based byte, length including LF] in aliases.jsonl', 'source_coordinates': 'one-based JSONL line; zero-based byte; length includes LF; label_field JSON pointer relative to alias row; slot indices zero-based'},
        'limits': ['No call traversal, runtime invocation, instruction/body/binary read or provider execution.', 'Template/operator parse ambiguities stay explicit; no owner guessed for malformed or nested-only separators.', 'Overlapping owner and root counts must not be added as a partition.', 'Library-path qualification is not a C++ namespace.', 'Vtable exporter rows can overrun into adjacent data; labels and slot-like values are observations, not table extent, method or callability proofs.', 'Only whole simple length-prefixed names and explicit _ZTV/_ZTS prefixes are retained as string candidates. Templates and other complex encodings remain the pinned string-source complement. Even whole simple syntax can be a method or fragment: no validated full Itanium type or class/function membership follows.', 'A named method narrows possible class membership only after actual receiver construction, address point, slot ABI and dispatch evidence independently join it.', 'No indirect site newly resolved or behavioral outcome graded by this inventory.'],
        'selfcheck': '16 assertions pass; exact source manifest digest/size/line and stat checks; membership plus remainder cardinality asserted',
    }
    result = {'symbol-summary.json': (json.dumps(summary, indent=2, sort_keys=True) + '\n').encode()}
    for key, records in outputs.items():
        result['symbol-' + key + '.jsonl'] = b''.join((json.dumps(r, separators=(',', ':'), sort_keys=True) + '\n').encode() for r in records)
    return result


if __name__ == '__main__':
    if sys.argv[1:] not in (['--write'], ['--check']):
        raise SystemExit('usage: symbol-build.py --write | --check')
    data = build()
    for name, raw in data.items():
        path = HERE / name
        if sys.argv[1] == '--write':
            with path.open('xb') as f:
                f.write(raw)
        else:
            assert path.read_bytes() == raw, name
    print(json.dumps({'mode': sys.argv[1], 'outputs': {n: {'bytes': len(b), 'sha256': digest(b)} for n, b in data.items()}, 'source_passes_each': 1, 'selfcheck': 'PASS'}))
