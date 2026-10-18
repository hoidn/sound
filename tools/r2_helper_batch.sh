#!/usr/bin/env bash
# Analyst-only: analyze Ableton-authored helper executables in parallel, one Ghidra project
# each, independent of the LiveR2 project. Extracts the arm64 slice, imports with default
# analysis, saves, and writes R2ProjectSummary JSON. Never executes the binaries.
# Usage: tools/r2_helper_batch.sh LIST_FILE   (one bundle-relative path per line)
# ponytail: xargs -P fan-out with a free-disk gate per job; no queue/retry layer.
set -euo pipefail
LIST=$1
ROOT=${R2_ROOT:-/var/tmp/sound-analysis}
REPO=$(cd "$(dirname "$0")/.." && pwd)
export BUNDLE=${BUNDLE:-"$HOME/Ableton Live 12 Suite.app/Contents"}
export GHIDRA=${GHIDRA_INSTALL_DIR:-$HOME/.local/opt/ghidra_12.1.4_PUBLIC}
export JAVA_HOME=${JAVA_HOME:-$HOME/.local/opt/jdk-21.0.12.1+1}
export OUT=$ROOT/helpers REPO JOBS=${R2_JOBS:-8} CPUS=${R2_CPUS:-4}
export GHIDRA_HEADLESS_MAXMEM=${R2_HEAP:-8G}
export MIN_FREE=$((15 * 1024 ** 3))   # do not start a job below 15 GiB free (LiveR2 and corpus need room)
mkdir -p "$OUT"

one() {
    rel=$1; slug=$(basename "$rel" | tr -c 'A-Za-z0-9\n' '_')
    d=$OUT/$slug; mkdir -p "$d/project" "$d/home/config" "$d/home/cache" "$d/tmp"
    free=$(df --output=avail -B1 "$OUT" | tail -1)
    if [ "$free" -lt "$MIN_FREE" ]; then echo "$slug skipped: $free bytes free" | tee "$d/skipped.txt"; return 0; fi
    python3 -I - "$BUNDLE/$rel" "$d/$slug.arm64" > "$d/slice.json" <<'PY'
import hashlib, json, struct, sys
src, dst = sys.argv[1], sys.argv[2]
data = open(src, "rb").read()
magic = struct.unpack(">I", data[:4])[0]
if magic == 0xCAFEBABE:
    n = struct.unpack(">I", data[4:8])[0]
    arches = [struct.unpack(">IIIII", data[8 + 20 * i: 28 + 20 * i]) for i in range(n)]
    hit = [a for a in arches if a[0] == 0x100000C]
    if not hit: sys.exit("no arm64 slice")
    _, _, off, size, _ = hit[0]; body = data[off:off + size]
else:
    if struct.unpack("<I", data[4:8])[0] != 0x100000C: sys.exit("thin non-arm64")
    off, size, body = 0, len(data), data
open(dst, "wb").write(body)
print(json.dumps({"source": src, "source_sha256": hashlib.sha256(data).hexdigest(), "slice_offset": off,
                  "slice_size": size, "slice_sha256": hashlib.sha256(body).hexdigest()}))
PY
    env -u JAVA_TOOL_OPTIONS -u _JAVA_OPTIONS PATH="$JAVA_HOME/bin:/usr/bin:/bin" \
        XDG_CONFIG_HOME="$d/home/config" XDG_CACHE_HOME="$d/home/cache" \
        GHIDRA_HEADLESS_JAVA_OPTIONS="-Duser.home=$d/home -Djava.io.tmpdir=$d/tmp" \
        /usr/bin/time -v -o "$d/analyze.time" "$GHIDRA/support/analyzeHeadless" "$d/project" H \
        -import "$d/$slug.arm64" -max-cpu "$CPUS" -scriptPath "$REPO/tools/ghidra" \
        -postScript R2ProjectSummary.java "$d/summary.json" > "$d/analyze.stdout" 2>&1 \
        && echo "$slug ok $(grep -o 'Elapsed.*' "$d/analyze.time")" || echo "$slug FAILED rc=$?"
}
export -f one
grep -v '^\s*$' "$LIST" | tr '\n' '\0' | xargs -0 -P "$JOBS" -I{} bash -c 'one "$@"' _ {}
