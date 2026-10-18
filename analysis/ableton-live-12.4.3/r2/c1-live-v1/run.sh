#!/usr/bin/env bash
# Analyst-only: after G0.3, (1) make a hard-linked query copy of LiveR2 with private non-.gbf
# files and start the R2FunctionDossier server on it; (2) run C1 samples, then full C1 plus C2,
# on projects/LiveR2. Each Ghidra project is held by exactly one process. Read-only throughout.
set -euo pipefail
R=/var/tmp/sound-analysis REPO=/home/ollie/Documents/sound
G=$HOME/.local/opt/ghidra_12.1.4_PUBLIC MEASURE=$REPO/analysis/ableton-live-12.4.3/r2/c-tooling-v1/measure.sh
export JAVA_HOME=$HOME/.local/opt/jdk-21.0.12.1+1 PATH=$HOME/.local/opt/jdk-21.0.12.1+1/bin:/usr/bin:/bin
unset JAVA_TOOL_OPTIONS _JAVA_OPTIONS GHIDRA_JAVA_OPTIONS
export XDG_CONFIG_HOME=$R/ghidra-home/config XDG_CACHE_HOME=$R/ghidra-home/cache
export GHIDRA_HEADLESS_JAVA_OPTIONS="-Duser.home=$R/ghidra-home -Djava.io.tmpdir=$R/tmp -XX:ParallelGCThreads=8"
grep -q done $R/g03/steps.txt || { echo "G0.3 not finished" >&2; exit 2; }
[ ! -e $R/projects/LiveR2.lock ] || { echo "LiveR2 is locked" >&2; exit 3; }

# (1) Query copy: hard links for .gbf database files, private copies for everything else.
if [ ! -e $R/query/LiveR2.gpr ]; then
    mkdir -p $R/query $R/query-spool/requests $R/query-spool/results
    cp -al $R/projects/LiveR2.gpr $R/projects/LiveR2.rep $R/query/
    find $R/query -type f ! -name '*.gbf' -exec sh -c 'cp --remove-destination "$1" "$1.tmp" && mv "$1.tmp" "$1"' _ {} \;
fi
GHIDRA_HEADLESS_MAXMEM=24G nohup $G/support/analyzeHeadless $R/query LiveR2 -process Live.arm64 -noanalysis -readOnly \
    -max-cpu 4 -scriptPath $REPO/tools/ghidra -postScript R2FunctionDossier.java --serve $R/query-spool \
    -log $R/query-spool/server.log > $R/query-spool/server.stdout 2>&1 &
echo "query server pid $!"

# (2) Bulk decompile on the main project: two A/B samples, then the full run with indexes.
export GHIDRA_HEADLESS_MAXMEM=48G
mkdir -p $R/corpus/logs
live() { local name=$1; shift
    $MEASURE $R/corpus/logs/$name $G/support/analyzeHeadless $R/projects LiveR2 -process Live.arm64 \
        -noanalysis -readOnly -max-cpu 28 -scriptPath $REPO/tools/ghidra -log $R/corpus/logs/$name/headless.log "$@"
    echo "$(date -Is) $name $(cat $R/corpus/logs/$name/result.json)" >> $R/corpus/steps.txt; }
live sample-i1  -postScript R2BulkDecompile.java out=$R/corpus/decomp threads=28 instances=1  chunk=100 shard=0/40
live sample-i14 -postScript R2BulkDecompile.java out=$R/corpus/decomp threads=28 instances=14 chunk=100 shard=1/40
live full -postScript R2BulkDecompile.java out=$R/corpus/decomp threads=28 instances=14 chunk=100 \
          -postScript R2ExportIndexes.java out=$R/corpus/indexes
python3 $REPO/tools/r2_corpus.py corpus $R/corpus/decomp > $R/corpus/check-decomp.json 2>&1 || true
python3 $REPO/tools/r2_corpus.py indexes $R/corpus/indexes > $R/corpus/check-indexes.json 2>&1 || true
echo "$(date -Is) done" >> $R/corpus/steps.txt
