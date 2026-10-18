"""dis.py RESULT_ID ENTRY: print callers, incoming refs and disassembly from a kept dossier in ../results."""
import sys, json, os
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, '..', 'results', sys.argv[1], 'functions', sys.argv[2] + '.json')))
print('# callers', [c['entry'] for c in d['callers']])
print('# incoming', [(r.get('from'), r.get('type')) for r in d['incoming_references_to_entry']][:20])
for ins in d['disassembly']: print(ins['address'], ins.get('text') or ins.get('instruction'))
