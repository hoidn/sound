#!/usr/bin/env bash
# H2 browser-index static evidence: regenerate every file under out/ (analyst-only, read-only inputs).
# Usage: bash run.sh   (from this directory). Requires the Ableton_Index helper corpus and indexes.
set -euo pipefail
H=/var/tmp/sound-analysis/helpers/Ableton_Index
APP="/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources"
LIVE=/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64
SCRATCH=/var/tmp/sound-analysis/scratch/h2-index
mkdir -p out/code "$SCRATCH"
cp "$APP/Database/filerefmap.db" "$SCRATCH/filerefmap.db"   # scratch copy; opened mode=ro
python3 -I strings_region.py "$H/corpus/indexes/strings.jsonl" 0x100c1c850 0x100c40000 out/strings-app-region.tsv
python3 -I strings_region.py "$H/corpus/indexes/strings.jsonl" 0x100d23d00 0x100d24500 out/strings-ipc-events.tsv
python3 -I strings_region.py "$H/corpus/indexes/strings.jsonl" 0x100c5bc00 0x100c5c700 out/strings-xmp-region.tsv
python3 -I sql_inventory.py "$H/corpus/indexes/strings.jsonl" out/sql-strings.jsonl out/sql-summary.json
python3 -I code_of.py "$H/corpus/decomp/chunks" out/code $(cut -d' ' -f1 key-functions.txt)
python3 -I file_types.py out/code/0x10029bb10.c out/file-type-registry.tsv
python3 -I read_ptrs.py "$H/Ableton_Index.arm64" 0x100d92700 16 > out/tfiledatabase-vtable.tsv
python3 -I shipped_inventory.py "$APP" "$SCRATCH/filerefmap.db" out/shipped-inventory.json
LC_ALL=C grep -a -o -E "ipc-channel|db-path|fileref-map-path|usage-data_file|parent-pid|os-events-flags|db-stale-factor|sound-analyzer|auto-keywords|Ableton Index|index->live|live->index|\{\}-files-\{\}\.db|Library\.cfg" "$LIVE" | sort | uniq -c > out/live-arm64-index-strings.txt
python3 -I make_manifest.py . "$H" "$APP" "$LIVE"
