#!/usr/bin/env python3
"""Shrink macho_inspect.py output and compare export names with Live.

Usage: compact_overlap.py ENGINE_FULL.json LIVE_FULL.json OUT_DIR
Writes OUT_DIR/engine.macho.compact.json (export/symtab lists replaced by counts;
C-linkage exports kept) and OUT_DIR/engine-vs-live-exports.json (name overlap per
Live slice, plus OEngine transport names and whether Live exports them).
"""
import json, sys

LISTS = ('exports', 'symtab_defined_external', 'symtab_imports')


def compact(full):
    for s in full['slices']:
        s['c_linkage_exports'] = [e for e in s['exports'] if not e['name'].startswith('__Z')]
        s['import_counts_by_library'] = {}
        for i in s.get('symtab_imports', []):
            s['import_counts_by_library'][i['library']] = s['import_counts_by_library'].get(i['library'], 0) + 1
        for key in LISTS:
            if key in s:
                s[key + '_count'] = len(s.pop(key))
    return full


def main(engine_path, live_path, out_dir):
    engine, live = json.load(open(engine_path)), json.load(open(live_path))
    names = {e['name'] for e in engine['slices'][0]['exports']}
    oengine = sorted(n for n in names if n.startswith(('__ZN7OEngine', '__ZNK7OEngine')))
    report = {'engine_sha256': engine['sha256'], 'live_sha256': live['sha256'],
              'engine_x86_64_exports': len(names), 'engine_oengine_exports': len(oengine), 'live': []}
    for s in live['slices']:
        lnames = {e['name'] for e in s['exports']}
        report['live'].append({'arch': s['arch'], 'slice_sha256': s['sha256'], 'exports': len(lnames),
                               'common_with_engine': len(names & lnames),
                               'oengine_exports_also_in_live': sum(n in lnames for n in oengine)})
    report['oengine_transport_names'] = [n for n in oengine if any(k in n for k in ('SetPlaying', 'BeatTime', 'Playing'))]
    json.dump(report, open(f'{out_dir}/engine-vs-live-exports.json', 'w'), indent=1)
    json.dump(compact(engine), open(f'{out_dir}/engine.macho.compact.json', 'w'), indent=1, sort_keys=True)


if __name__ == '__main__':
    main(*sys.argv[1:])
