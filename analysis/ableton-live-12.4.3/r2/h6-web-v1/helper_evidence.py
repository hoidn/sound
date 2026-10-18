"""Extract cited strings and functions from one helper's C1/C2 corpus (read-only).

usage: python3 -I helper_evidence.py HELPER_DIR STRINGS_FILE ENTRIES_FILE > out.json
STRINGS_FILE: one exact string value per line. ENTRIES_FILE: one 0x... entry per line.
Every requested item appears in the output; a missing one is an empty list or
null, never dropped. Function records keep the exact decompiled code.
"""
import glob
import json
import sys


def lines(path):
    return [x.rstrip('\n') for x in open(path, encoding='utf-8') if x.strip()]


def main(helper, strings_file, entries_file):
    summary = json.load(open(f'{helper}/summary.json'))
    want_s, want_f = lines(strings_file), lines(entries_file)
    strings = {s: [] for s in want_s}
    for line in open(f'{helper}/corpus/indexes/strings.jsonl'):
        r = json.loads(line)
        if r['value'] in strings:
            refs = sorted({(x.get('function') or '', x.get('function_name') or '') for x in r.get('refs') or []})
            strings[r['value']].append({'address': r['address'], 'functions': [list(x) for x in refs]})
    functions = {e: None for e in want_f}
    for chunk in sorted(glob.glob(f'{helper}/corpus/decomp/chunks/chunk-*.jsonl')):
        for line in open(chunk):
            r = json.loads(line)
            if r['entry'] in functions:
                functions[r['entry']] = {k: r[k] for k in
                                         ('entry', 'name', 'signature', 'state', 'warnings', 'code_sha256', 'code')}
    json.dump({'program': summary['program'], 'slice_sha256': summary['executable_sha256'],
               'strings': strings, 'functions': functions}, sys.stdout, indent=1)


if __name__ == '__main__':
    main(*sys.argv[1:4])
