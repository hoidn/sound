#!/usr/bin/env bash
# Analyst-only roadmap revision 2 gate G0.3: import Live.arm64 without analysis, run one
# default full analysis and save, then prove a cold read-only reopen. Sole project writer.
# Never executes the imported bytes. Outputs: $R2_ROOT/g03 (logs, timings, samples, summary).
# ponytail: plain shell plus a 30 s sampler; run_persistent_native.py is macOS-only (libproc).
set -euo pipefail
ROOT=${R2_ROOT:-/var/tmp/sound-analysis}
REPO=$(cd "$(dirname "$0")/.." && pwd)
TARGET=$REPO/analysis/ableton-live-12.4.3/derived/Live.arm64
EXPECT=3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad
GHIDRA=${GHIDRA_INSTALL_DIR:-$HOME/.local/opt/ghidra_12.1.4_PUBLIC}
export JAVA_HOME=${JAVA_HOME:-$HOME/.local/opt/jdk-21.0.12.1+1}
CPUS=${R2_CPUS:-24}
export GHIDRA_HEADLESS_MAXMEM=${R2_HEAP:-32G}
FLOOR=$((6 * 1024 ** 3))            # stop the analyzer below 6 GiB free on the project filesystem
DEADLINE=${R2_DEADLINE:-6h}
OUT=$ROOT/g03 PROJ=$ROOT/projects
mkdir -p "$OUT" "$PROJ" "$ROOT/ghidra-home/config" "$ROOT/ghidra-home/cache" "$ROOT/tmp"
unset JAVA_TOOL_OPTIONS _JAVA_OPTIONS GHIDRA_JAVA_OPTIONS
export PATH=$JAVA_HOME/bin:/usr/bin:/bin
export XDG_CONFIG_HOME=$ROOT/ghidra-home/config XDG_CACHE_HOME=$ROOT/ghidra-home/cache
export GHIDRA_HEADLESS_JAVA_OPTIONS="-Duser.home=$ROOT/ghidra-home -Djava.io.tmpdir=$ROOT/tmp -XX:ParallelGCThreads=8"

[ "$(sha256sum "$TARGET" | cut -d' ' -f1)" = "$EXPECT" ] || { echo "target digest mismatch" >&2; exit 2; }
[ -e "$PROJ/LiveR2.gpr" ] && [ "${1:-}" != "--resume-analysis" ] && { echo "project exists; refusing to overwrite" >&2; exit 3; }

sample() {
    while sleep 30; do
        free=$(df --output=avail -B1 "$ROOT" | tail -1)
        proj=$(du -sb "$PROJ" 2>/dev/null | cut -f1)
        rss=$(ps -C java -o rss=,args= | awk -v p="$PROJ" 'index($0,p){s+=$1} END{print s+0}')
        printf '%s\t%s\t%s\t%s\n' "$(date +%s)" "$free" "$proj" "$rss" >> "$OUT/samples.tsv"
        if [ "$free" -lt "$FLOOR" ]; then
            echo "$(date -Is) disk floor reached: $free bytes free" >> "$OUT/stop.txt"
            pkill -TERM -f "AnalyzeHeadless $PROJ" || true
        fi
    done
}

step() {
    local name=$1; shift
    echo "$(date -Is) start $name" >> "$OUT/steps.txt"
    local rc=0
    /usr/bin/time -v -o "$OUT/$name.time" timeout -s TERM "$DEADLINE" \
        "$GHIDRA/support/analyzeHeadless" "$PROJ" LiveR2 "$@" \
        -log "$OUT/$name.log" -scriptlog "$OUT/$name.script.log" > "$OUT/$name.stdout" 2>&1 || rc=$?
    echo "$(date -Is) end $name rc=$rc" >> "$OUT/steps.txt"
    return $rc
}

printf 'epoch\tfree_bytes\tproject_bytes\tjava_rss_kb\n' > "$OUT/samples.tsv"
sample & SAMPLER=$!
trap 'kill $SAMPLER 2>/dev/null || true' EXIT

[ "${1:-}" = "--resume-analysis" ] || step a-import -import "$TARGET" -noanalysis -max-cpu "$CPUS"
step b-analyze -process Live.arm64 -max-cpu "$CPUS"
step c-reopen -process Live.arm64 -noanalysis -readOnly -max-cpu "$CPUS" \
    -scriptPath "$REPO/tools/ghidra" -postScript R2ProjectSummary.java "$OUT/summary.json"
(cd "$PROJ" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$OUT/project-sha256.txt"
du -sb "$PROJ" > "$OUT/project-bytes.txt"
echo "$(date -Is) done" >> "$OUT/steps.txt"
