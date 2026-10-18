"""Compare ATransport's persistent member registrations (corpus record of FUN_10275dccc) with the
Transport field order of a shipped schema. Registrations whose flag word is 3 (CONCAT44(3,..) or
0x300000000) are treated as runtime-only. Output is data.
usage: python3 -I check_registry_order.py <corpus-excerpts.jsonl> <Schema/12.0_12402.txt>"""
import json, re, sys
import xml.etree.ElementTree as ET
code = next(json.loads(l)['record']['code'] for l in open(sys.argv[1]) if '"entry": "0x10275dccc"' in l)
calls = [' '.join(c.split()) for c in re.findall(r'FUN_10147e954\((.*?)\);', code, re.S)]
pers = [re.search(r'L"mp(\w+)"', c).group(1) for c in calls if not re.search(r'CONCAT44\(3,|0x300000000', c)]
schema = [f.tag for f in ET.parse(sys.argv[2]).getroot().find('Transport')]
print(len(calls), 'registrations;', len(pers), 'persistent;', len(schema), 'schema fields')
print('identical order:', pers == schema)
sys.exit(0 if pers == schema else 1)
