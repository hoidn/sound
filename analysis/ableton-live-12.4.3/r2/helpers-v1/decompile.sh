#!/usr/bin/env bash
# Analyst-only: run C1 (R2BulkDecompile) and C2 (R2ExportIndexes) on each analyzed helper
# project, largest first, two JVMs at a time. Read-only on every program.
set -euo pipefail
export REPO=/home/ollie/Documents/sound H=/var/tmp/sound-analysis/helpers
export G=$HOME/.local/opt/ghidra_12.1.4_PUBLIC JAVA_HOME=$HOME/.local/opt/jdk-21.0.12.1+1
one() {
    d=$1; slug=$(basename "$d")
    prog=$(python3 -I -c "import json;print(json.load(open('$d/summary.json'))['program'])")
    env -u JAVA_TOOL_OPTIONS -u _JAVA_OPTIONS PATH="$JAVA_HOME/bin:/usr/bin:/bin" \
        XDG_CONFIG_HOME="$d/home/config" XDG_CACHE_HOME="$d/home/cache" GHIDRA_HEADLESS_MAXMEM=16G \
        GHIDRA_HEADLESS_JAVA_OPTIONS="-Duser.home=$d/home -Djava.io.tmpdir=$d/tmp" \
        /usr/bin/time -v -o "$d/decomp.time" "$G/support/analyzeHeadless" "$d/project" H -process "$prog" \
        -noanalysis -readOnly -max-cpu 16 -scriptPath "$REPO/tools/ghidra" \
        -postScript R2BulkDecompile.java "out=$d/corpus/decomp" threads=16 instances=8 chunk=100 \
        -postScript R2ExportIndexes.java "out=$d/corpus/indexes" > "$d/decomp.stdout" 2>&1 \
        && echo "$slug ok $(grep -o 'Elapsed.*' "$d/decomp.time")" || echo "$slug FAILED"
}
export -f one
python3 -I - "$H" <<'PY' | xargs -P 2 -I{} bash -c 'one "$@"' _ {}
import json, pathlib, sys
rows = []
for d in pathlib.Path(sys.argv[1]).iterdir():
    s = d / "summary.json"
    if d.name == "Live_x86_64" or not s.exists(): continue
    n = json.loads(s.read_text())["functions_nonexternal"]
    if n: rows.append((n, str(d)))
for n, d in sorted(rows, reverse=True): print(d)
PY
