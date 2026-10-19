"""Map class-descriptor data addresses to class names from FUN_10147e7c4(&desc, L"Name", len, &parent, ...)
registrations in the arm64 corpus pseudocode (read-only; output is data).
usage: python3 -I class_names.py <corpus dir> > class-names.tsv  (desc, name, parent desc, registering function)"""
import glob, json, re, sys
p = re.compile(r'FUN_10147e7c4\(&DAT_([0-9a-f]+),L"([A-Za-z0-9_<>:]+)",(?:0x)?[0-9a-f]+,\s*&DAT_([0-9a-f]+)')
for f in sorted(glob.glob(sys.argv[1] + '/decomp/chunks/*.jsonl')):
    for line in open(f):
        if 'FUN_10147e7c4' not in line: continue
        r = json.loads(line)
        for m in p.finditer(re.sub(r'\s+', ' ', r['code']).replace(', ', ',')):
            print('0x' + m.group(1), m.group(2), '0x' + m.group(3), r['entry'], sep='\t')
