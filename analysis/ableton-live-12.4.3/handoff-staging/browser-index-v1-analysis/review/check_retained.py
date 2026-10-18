"""Check that retained D2 and addendum records equal the H2 helper corpus records.

Usage: python3 -I check_retained.py CHUNKS_DIR RECORDS.jsonl [...]
"""
import json, sys, os

def main(chunks, files):
    want = {}
    for f in files:
        for line in open(f):
            r = json.loads(line)
            want[(r['chunk'], r['entry'])] = (f, line.rstrip('\n'))
    found = 0
    for chunk in sorted({c for c, _ in want}):
        for line in open(os.path.join(chunks, chunk)):
            r = json.loads(line)
            k = (chunk, r.get('entry'))
            if k in want:
                kept = json.loads(want[k][1]); kept.pop('chunk')  # locator added on retention
                same = kept == r
                print(('same ' if same else 'DIFF ') + k[1] + ' ' + os.path.basename(want[k][0]))
                found += same
    print(f'{found} of {len(want)} records identical to corpus')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
