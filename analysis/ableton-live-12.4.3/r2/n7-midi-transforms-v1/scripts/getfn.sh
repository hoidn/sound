#!/bin/sh
# usage: getfn.sh 0xADDR  -> prints code of function from corpus
C=/var/tmp/sound-analysis/corpus/decomp/chunks
f=$(grep -l "\"entry\":\"$1\"" $C/chunk-*.jsonl | head -1)
grep -h "\"entry\":\"$1\"" "$f" | python3 -I -c 'import sys,json; r=json.loads(sys.stdin.readline()); print("//", r["entry"], r.get("name"), r.get("state"), r.get("signature")); print(r.get("code") or r.get("partial_code") or r.get("error"))'
