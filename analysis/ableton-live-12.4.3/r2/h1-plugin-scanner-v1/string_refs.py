"""List referencing functions for selected strings in a C2 strings.jsonl index.

Analyst-only. Usage: python3 -I string_refs.py <strings.jsonl> <keys.txt>
keys.txt: one key per line; a key matches a string value exactly, or as a
substring when it starts with '~'. Output: TSV address, value (first 90
chars), direct referencing functions, functions one data hop back (via).
"""
import json, sys

def main():
    keys = [k.rstrip('\n') for k in open(sys.argv[2]) if k.strip()]
    for line in open(sys.argv[1]):
        r = json.loads(line)
        v = r.get('value', '')
        if not any(v == k or (k[0] == '~' and k[1:] in v) for k in keys):
            continue
        refs = r.get('refs') or []
        direct = sorted({x['function'] for x in refs if x.get('function')})
        via = sorted({(f['function'] if isinstance(f, dict) else f)
                      for x in refs for f in (x.get('via') or [])})
        print('\t'.join([r['address'], repr(v[:90]), ','.join(direct), ','.join(via)]))

if __name__ == '__main__':
    main()
