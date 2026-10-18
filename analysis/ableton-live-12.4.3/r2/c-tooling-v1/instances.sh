#!/usr/bin/env bash
# C1 multi-instance series on Push2: threads/instances pairs, fresh output each, chunk=50.
set -u
. /var/tmp/sound-analysis/scratch/c-tooling/env.sh
M=/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/r2/c-tooling-v1
for pair in 4:4 8:8 16:4 16:8 16:16; do
  t=${pair%:*} i=${pair#*:}
  $M/measure.sh $S/runs/c1-t$t-i$i $GHIDRA_INSTALL_DIR/support/analyzeHeadless $S/proj Push2C -process Push2DisplayProcess.arm64 -noanalysis -readOnly \
    -scriptPath /home/ollie/Documents/sound/tools/ghidra -postScript R2BulkDecompile.java out=$S/runs/c1-t$t-i$i/corpus threads=$t instances=$i chunk=50
  echo "$pair $(cat $S/runs/c1-t$t-i$i/result.json) $(grep -o 'R2_INVOCATION.*}' $S/runs/c1-t$t-i$i/stdout.txt) $(grep -c ERROR $S/runs/c1-t$t-i$i/stdout.txt) errors"
done
