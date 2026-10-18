#!/usr/bin/env bash
# Analyst-only measurement driver for the C1/C2 tooling tests (Push2 scratch project).
# Usage: measure.sh RUN_DIR COMMAND...   Runs COMMAND in its own process group under
# /usr/bin/time -v and samples the group's summed RSS in KiB (JVM plus decompiler children) and the 1-minute load average every second.
set -euo pipefail
out=$1; shift
mkdir -p "$out"
setsid /usr/bin/time -v -o "$out/time.txt" "$@" > "$out/stdout.txt" 2>&1 &
pid=$!
peak=0
while kill -0 "$pid" 2>/dev/null; do
    rss=$(ps -o rss= -g "$pid" | awk '{s+=$1} END{print s+0}')
    [ "$rss" -gt "$peak" ] && peak=$rss
    echo "$(date +%s) $rss $(cut -d" " -f1 /proc/loadavg)" >> "$out/samples.txt"
    sleep 1
done
wait "$pid" && rc=0 || rc=$?
echo "{\"rc\": $rc, \"peak_group_rss_kb\": $peak}" > "$out/result.json"
