#!/usr/bin/env bash
# C1 scaling series on Push2: fresh output per thread count, chunk=50.
set -u
. /var/tmp/sound-analysis/scratch/c-tooling/env.sh
M=/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/r2/c-tooling-v1
for t in 1 4 8 16; do
  $M/measure.sh $S/runs/c1-t$t $GHIDRA_INSTALL_DIR/support/analyzeHeadless $S/proj Push2C -process Push2DisplayProcess.arm64 -noanalysis -readOnly \
    -scriptPath /home/ollie/Documents/sound/tools/ghidra -postScript R2BulkDecompile.java out=$S/runs/c1-t$t/corpus threads=$t chunk=50
done
