#!/usr/bin/env bash
# Follow-up tests after the scaling series: same-project concurrency, two JVMs on project copies,
# kill-and-resume, C2 determinism and C1+C2 in one invocation.
set -u
. /var/tmp/sound-analysis/scratch/c-tooling/env.sh
M=/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/r2/c-tooling-v1
T=/home/ollie/Documents/sound/tools/ghidra
H=$GHIDRA_INSTALL_DIR/support/analyzeHeadless
job() { # job RUN PROJECT_DIR SCRIPT_ARGS...
  local run=$1 pdir=$2; shift 2
  $M/measure.sh $S/runs/$run $H $pdir Push2C -process Push2DisplayProcess.arm64 -noanalysis -readOnly -scriptPath $T "$@"
}
# 1. Two JVMs, same project directory, disjoint shards.
job multi-same-0 $S/proj -postScript R2BulkDecompile.java out=$S/runs/multi-same/corpus threads=4 chunk=50 shard=0/2 &
sleep 3
job multi-same-1 $S/proj -postScript R2BulkDecompile.java out=$S/runs/multi-same/corpus threads=4 chunk=50 shard=1/2
wait
# 2. Two JVMs, each on its own project copy: proj2 hard-linked (cp -al), proj3 a full copy for its size.
rm -rf $S/proj2 $S/proj3 && mkdir -p $S/proj2 $S/proj3 && cp -al $S/proj/Push2C.gpr $S/proj/Push2C.rep $S/proj2/ && cp -a $S/proj/Push2C.gpr $S/proj/Push2C.rep $S/proj3/
{ du -sb $S/proj; du -sb $S/proj3; du -sb --count-links $S/proj2; df -B1 --output=used $S | tail -1; } > $S/runs/project-copy-bytes.txt
du -sb $S/proj $S/proj2 >> $S/runs/project-copy-bytes.txt
start=$(date +%s.%N)
job multi-copy-0 $S/proj -postScript R2BulkDecompile.java out=$S/runs/multi-copy/corpus threads=8 instances=8 chunk=50 shard=0/2 &
job multi-copy-1 $S/proj2 -postScript R2BulkDecompile.java out=$S/runs/multi-copy/corpus threads=8 instances=8 chunk=50 shard=1/2
wait
echo "$(date +%s.%N) - $start" | bc > $S/runs/multi-copy-wall-seconds.txt
# 3. Kill after 25 s, then resume.
$M/measure.sh $S/runs/resume-a $H $S/proj Push2C -process Push2DisplayProcess.arm64 -noanalysis -readOnly -scriptPath $T \
  -postScript R2BulkDecompile.java out=$S/runs/resume/corpus threads=4 instances=4 chunk=50 &
sleep 25; pkill -KILL -f "out=$S/runs/resume/corpus"; wait
ls $S/runs/resume/corpus/chunks | wc -l > $S/runs/resume-chunks-after-kill.txt
ls -a $S/runs/resume/corpus/chunks | grep -c '^\.' >> $S/runs/resume-chunks-after-kill.txt
job resume-b $S/proj -postScript R2BulkDecompile.java out=$S/runs/resume/corpus threads=4 instances=4 chunk=50
# 4. C1 (all committed, validation only) + C2 in one invocation, then C2 alone for determinism.
job c1c2-same-jvm $S/proj -postScript R2BulkDecompile.java out=$S/runs/c1-t8-i8/corpus threads=8 instances=8 chunk=50 -postScript R2ExportIndexes.java out=$S/runs/indexes-a
job c2-repeat $S/proj -postScript R2ExportIndexes.java out=$S/runs/indexes-b
