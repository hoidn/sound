#!/usr/bin/env bash
# Analyst-only: C1 bulk decompile and C2 indexes for Live's x86_64 slice, read-only, one JVM.
set -euo pipefail
R=/var/tmp/sound-analysis H=$R/helpers/Live_x86_64 O=$R/corpus-x86 REPO=/home/ollie/Documents/sound
G=$HOME/.local/opt/ghidra_12.1.4_PUBLIC MEASURE=$REPO/analysis/ableton-live-12.4.3/r2/c-tooling-v1/measure.sh
export JAVA_HOME=$HOME/.local/opt/jdk-21.0.12.1+1 PATH=$HOME/.local/opt/jdk-21.0.12.1+1/bin:/usr/bin:/bin
unset JAVA_TOOL_OPTIONS _JAVA_OPTIONS GHIDRA_JAVA_OPTIONS
export XDG_CONFIG_HOME=$H/home/config XDG_CACHE_HOME=$H/home/cache GHIDRA_HEADLESS_MAXMEM=48G
export GHIDRA_HEADLESS_JAVA_OPTIONS="-Duser.home=$H/home -Djava.io.tmpdir=$H/tmp -XX:ParallelGCThreads=8"
mkdir -p $O/logs
$MEASURE $O/logs/full $G/support/analyzeHeadless $H/project H -process Live_x86_64.x86_64 -noanalysis -readOnly \
    -max-cpu 28 -scriptPath $REPO/tools/ghidra -log $O/logs/full/headless.log \
    -postScript R2BulkDecompile.java out=$O/decomp threads=28 instances=14 chunk=100 \
    -postScript R2ExportIndexes.java out=$O/indexes
echo "$(date -Is) full $(cat $O/logs/full/result.json)" >> $O/steps.txt
python3 $REPO/tools/r2_corpus.py corpus $O/decomp > $O/check-decomp.json 2>&1 || true
python3 $REPO/tools/r2_corpus.py indexes $O/indexes > $O/check-indexes.json 2>&1 || true
echo "$(date -Is) done" >> $O/steps.txt
