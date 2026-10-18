"""Search the strings index: strq.py REGEX [maxrows]. Prints address, value, ref functions."""
import sys, json, re
pat = re.compile(sys.argv[1]); lim = int(sys.argv[2]) if len(sys.argv) > 2 else 200
n = 0
with open('/var/tmp/sound-analysis/corpus/indexes/strings.jsonl') as f:
    for line in f:
        r = json.loads(line)
        if pat.search(r['value']):
            fns = sorted({str(x.get('function_name')) + '@' + x['from'] for x in r['refs']})
            print(r['address'], repr(r['value'][:140]), fns[:8])
            n += 1
            if n >= lim: break
