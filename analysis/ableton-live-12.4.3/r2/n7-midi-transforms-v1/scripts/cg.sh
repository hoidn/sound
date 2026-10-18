#!/bin/sh
# cg.sh callees|callers 0xADDR
I=/var/tmp/sound-analysis/corpus/indexes/calls.jsonl
if [ "$1" = callees ]; then grep -F "\"caller\":\"$2\"" $I | python3 -I -c 'import sys,json
for l in sys.stdin:
  r=json.loads(l); print(r["site"], r["kind"], r["callee"], r["callee_name"], r["callee_resolved_name"] or "")'
else grep -F "\"callee\":\"$2\"" $I | python3 -I -c 'import sys,json
for l in sys.stdin:
  r=json.loads(l); print(r["site"], r["kind"], r["caller"], r["caller_name"])'
fi
