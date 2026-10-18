#!/bin/bash
# Reviewer check log for midi-note-storage-v1 (analyst-side). Writes review-checks.txt next to this script.
# usage: bash run_checks.sh <export copy of the package outside the checkout>
R=$(cd "$(dirname "$0")" && pwd); A=/home/ollie/Documents/sound/analysis/ableton-live-12.4.3
P=$A/handoff-staging/midi-note-storage-v1; S7=$A/r2/s7-midi-notes-v1; N1=$A/r2/n1-transport-state-v1
IMG=$A/derived/Live.arm64; C=/var/tmp/sound-analysis/corpus/decomp/chunks; X=$1
CL="env N1_CACHE=$N1/.entry-map.pickle python3 -I $S7/corpus_lookup.py"
cd /tmp && {
echo "midi-note-storage-v1 handoff review: reviewer checks (analyst-side; not payload). 2026-10-18."
echo "Reviewer: separate review agent (Claude Opus 5.5). Scripts in this directory; run with python3 -I from any directory."
echo "Image: $IMG sha256 $(sha256sum $IMG | cut -d' ' -f1)"
echo
echo "Mapping to the plan's IDs: RVN-01 = I1 established and widened (the +0x2c gate covers every post-read step: note limits,"
echo "MidiNotes post-load, store and list post-loads; the plan said only MNS-014..017). RVN-02 = F10: d4-0001 re-established from"
echo "corpus records byte-identical to its .c files plus an image decode; 16 cases need REQ-014 clause 4/5 (author tagged 10)."
echo "RVN-03 = REQ-009 clause 2 precondition (zero-id pass walks the stored KeyTrack list). RVN-04 = F2 wording (MNS-001 purpose,"
echo "comparator). RVN-05 = manifest magnitude exclusion vs Invalid. RVN-09 = F4. RVN-11 = I2..I7 accepted; I7 leading '-' confirmed."
echo "F3, F5, F6, F7, F9 confirmed; F1 accepted; F8 = 12 new cases accepted."
echo
echo "== 1. Evidence identity =="
sha256sum $S7/manifest.json $N1/manifest.json
python3 -I - <<EOF
import json, hashlib, os
for run in ("$S7", "$N1"):
    fs = json.load(open(run + "/manifest.json"))["files"]
    bad = [k for k, v in fs.items() if hashlib.sha256(open(os.path.join(run, k), "rb").read()).hexdigest() != v["sha256"]]
    print(os.path.basename(run), "files listed", len(fs), "mismatched", bad)
EOF
sha256sum /var/tmp/sound-analysis/query-spool-2/results/d4-0001/queries.json /var/tmp/sound-analysis/query-spool-2/results/d4-0001/functions/*
grep -E '"(program|executable_sha256)"' /var/tmp/sound-analysis/corpus/decomp/run.json
echo "Retained corpus records (review/corpus-excerpts.jsonl, written by corpus_lookup.py excerpt): entry chunk offset line_sha256 code_sha256"
python3 -I - <<EOF
import json, hashlib
for l in open("$R/corpus-excerpts.jsonl"):
    r = json.loads(l); rec = r["record"]
    fh = open("$C/" + r["chunk"], "rb"); fh.seek(r["offset"]); raw = fh.readline().rstrip(b"\n")
    ok = hashlib.sha256(raw).hexdigest() == r["line_sha256"] and hashlib.sha256(rec["code"].encode()).hexdigest() == rec["code_sha256"]
    print(rec["entry"], r["chunk"], r["offset"], r["line_sha256"], rec["code_sha256"], "verified" if ok else "MISMATCH")
EOF
echo "d4-0001 .c files equal corpus code_sha256: 0x10292b9ec 98be02fc..., 0x10292c960 33cdeee5... (see above)."
echo
echo "== 2. RVN-01: post-read gate (+0x2c) for Live Set reads =="
echo "Gate sites (corpus): 0x101487284 (array element), 0x101487310 (compound member), 0x101486fe4 (root), 0x1014868c0 call slot +0xd0"
echo "only when FUN_1015192c0(ctx) = byte ctx+0x2c is nonzero. Slot +0xd0 = note limits 0x1028e2c80, MidiNotes 0x1028f5864,"
echo "store 0x10292cd70, list 0x10292b730 (S7 notes.md, rounds 1-2)."
$CL code 0x101487310 | grep -n 'FUN_1015192c0\|+ 0xd0))'
$CL code 0x1015192b8 0x1015192c0 | grep -v '^\s*$'
echo "-- callers of the only clear (0x1015192b8); indirect and vtable references to it (counts)"
$CL callers 0x1015192b8
grep -c '0x1015192b8' /var/tmp/sound-analysis/corpus/indexes/indirect.jsonl /var/tmp/sound-analysis/corpus/indexes/vtables.jsonl
echo "-- the two callers are undo-history binary streams (magic 0x61622d68 'h-ba'; History.cpp string in 0x101547ef4)"
$CL code 0x101546518 | grep -n '0x61622d68\|FUN_1015192b8'
$CL code 0x101547ef4 | grep -n '0x61622d68\|History.cpp:1892"\|FUN_1015192b8'
echo "-- general XML reader 0x101484108: context from 0x101478258 -> 0x10151e0d8 (+0x2c = 1), passed to root load 0x101486fe4"
$CL code 0x101484108 | grep -n 'FUN_101478258\|FUN_101486fe4'
$CL code 0x101478258 | grep -n 'FUN_10151e0d8'
$CL code 0x10151e0d8 | grep -n '0x2c'
echo "-- second entry 0x10146c258: '<?' branch parses to a node tree only (0x1015289c8) and returns it; 'AB 1E' branch uses 0x101478258"
$CL code 0x10146c258 | grep -n "local_5e == '<'\|FUN_1015289c8\|FUN_101478258"
echo "-- every function naming a context vtable (0x106675f78 base, 0x106676178, 0x106676378) and its +0x2c stores"
python3 -I $R/ctx_scan.py $C | grep -E '0x106675f78|0x106676178|0x106676378'
echo "-- byte stores at +0x2c in 0x101510000-0x101530000, or in any function calling the ctx accessors or reader setup"
python3 -I $R/flag_scan.py $C 0x101510000 0x101530000
echo "-- corpus-wide: functions calling the shared base FUN_10128ed98 and storing a byte at +0x2c. The non-1 stores are other"
echo "   classes: vtable 0x10666fa70 family (+0x18 a string, not a stream pointer), 0x10686f080 and 0x1068768d8 (store at"
echo "   puVar3 + 0x2c words, i.e. +0x160), 0x106a5d938 (Push 2 clip visualisation), 0x106696718 (param_4 store)."
python3 -I $R/ctor_scan.py $C
echo "Ruling: every context constructor stores 1; the clear is reached only from undo-history streams; the Live Set XML read"
echo "uses a freshly constructed context. Residual (accepted): an inlined clear elsewhere is not excluded by exhaustive search."
echo
echo "== 3. RVN-02: REQ-014 clauses 4 and 5 from retained records =="
echo "-- caller in retained S7 disassembly: x0 = store (+0x490), x1 = 0x1028da61c(note) = NoteId (+0x28), d0 = 0x1028dea48(note) = Duration (+8)"
python3 -I $S7/disasm.py $S7/results/s7-0001/functions/0x1028f5864.json 0x1028f5bec 0x1028f5c10
echo "-- 0x10292b9ec early return decoded from the pinned image (first TimeOffset at [x20]; last at [x8,#-0x30]; Duration in q1)"
python3 -I $R/a64.py $IMG 0x10292ba40 0x10292ba74
echo "   => unchanged iff count > 0, first > 0 and last < Duration (strict). Otherwise adjusted (untraced; excluded inputs)."
echo "-- 0x10292c960 (corpus): per NoteId bucket, 0x10292b9ec on each list, then lists whose event count is 0 removed via 0x10156d800"
python3 -I - <<EOF
import json
for l in open("$R/corpus-excerpts.jsonl"):
    r = json.loads(l)["record"]
    if r["entry"] == "0x10292c960":
        c = r["code"]; i = c.find("FUN_10292b9ec(param_1"); print(c[i - 40:i + 200]); j = c.find("FUN_10156d800"); print(c[j - 80:j + 60])
EOF
echo "Cases relying on clause 4 or 5 (traceability 'span'): MNS-039 040 042 044a-c 047 048 049a 049b 050 051a 051b 069 071a 071b"
echo
echo "== 4. RVN-09: Invalid (n1-0006 0x10152bfb8 disassembly, double branch) =="
python3 -I $S7/disasm.py $N1/results/n1-0006/functions/0x10152bfb8.json 0x10152c058 0x10152c088
echo
echo "== 5. Integer converters =="
echo "-- 0x1002fda78 (int, MidiKey/CC/Id): leading '-' accepted"
$CL code 0x1002fda78 | grep -n '0x2d'
echo "-- 0x101524d8c (int64 whole span): record line hash as cited by the author"
python3 -I -c "
import hashlib; f=open('$C/chunk-00813.jsonl','rb'); f.seek(61888); print(hashlib.sha256(f.readline().rstrip(b'\n')).hexdigest())"
echo
echo "== 6. Reviewer's restatement (restate.py, written from spec.md, not mns_model.py) =="
python3 -I $R/restate.py $P
python3 -I $R/restate_selfcheck.py $P $A/handoff-staging/midi-note-storage-v1-analysis
echo
echo "== 7. Fixtures (fixtures.py) =="
python3 -I $R/fixtures.py $P
echo
echo "== 8. Hygiene (hygiene.py over payload text and decompressed fixtures) =="
python3 -I $R/hygiene.py $P
echo
echo "== 9. Export verification (copy outside the checkout: $X) =="
diff -r $X $P && echo "export identical to staging"
python3 -I $A/handoff-staging/midi-note-storage-v1-analysis/build_mns.py verify $X | python3 -I -c "import json,sys;d=json.load(sys.stdin);print({k:d[k] for k in ('cases','case_problems','payload_files','files_including_manifest','hash_or_size_mismatches','inventory_differences','markdown_links','unresolved_links','missing_case_inputs','deny_list_hits','symlinks','manifest_sha256')})"
(cd $X && sha256sum -c <(python3 -I -c "import json;[print(f['sha256']+'  '+f['path']) for f in json.load(open('manifest.json'))['files']]") | grep -c ': OK')
sha256sum $X/manifest.json
} > $R/review-checks.txt 2>&1
