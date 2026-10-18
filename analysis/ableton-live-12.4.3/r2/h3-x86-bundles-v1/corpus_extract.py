#!/usr/bin/env python3
"""Copy selected function records from R2BulkDecompile chunk JSONL to <entry>.c files.

Usage: corpus_extract.py CHUNK_DIR OUT_DIR ENTRY...
Each file starts with a comment holding entry, name, signature, state and source
chunk; the rest is the record's `code` text unchanged. Fails if an entry is absent.
"""
import glob, json, os, sys


def main(chunk_dir, out_dir, *entries):
    want, found = set(entries), set()
    for path in sorted(glob.glob(os.path.join(chunk_dir, 'chunk-*.jsonl'))):
        for line in open(path):
            r = json.loads(line)
            if r['entry'] in want:
                found.add(r['entry'])
                with open(os.path.join(out_dir, r['entry'] + '.c'), 'w') as fh:
                    fh.write(f"// {r['entry']} {r['name']} | {r['signature']} | state={r['state']} | {os.path.basename(path)}\n")
                    fh.write(r.get('code') or '')
    missing = want - found
    if missing:
        sys.exit(f'entries not found: {sorted(missing)}')


if __name__ == '__main__':
    main(*sys.argv[1:])
