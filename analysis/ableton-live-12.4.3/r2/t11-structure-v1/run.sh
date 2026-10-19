#!/bin/sh
# Regenerate T1.1 (Live Set structure) evidence. Read-only on the bundle and the corpora;
# nothing from the bundle is executed and no shipped content is copied into fixtures/.
# Requires python3 (3.13.9 used); x-crc/ also needs gcc and the x86_64 slice (tools/xexec, unchanged,
# built to /var/tmp/sound-analysis/xexec-t11/xexec). Traces under traces/ were produced by the
# commands in each trace.txt and are kept as recorded; only traces/a1a2 is regenerated here.
set -eu
H=$(cd "$(dirname "$0")" && pwd)
B="/home/ollie/Ableton Live 12 Suite.app/Contents"
S="$B/App-Resources/Schema/12.0_12402.txt"
cd "$H"
python3 -I t11_survey.py "$B" out
for k in als alc; do
  find "$B/App-Resources" -name "*.$k" -not -name '._*' -print0 | sort -z |
    xargs -0 python3 -I schema_check.py "$S" > "out/schema-check-$k.jsonl"
done
ls ../../../../handoff/*/fixtures/*.xml ../../../../handoff/*/fixtures/*.als 2>/dev/null | sort |
  xargs python3 -I schema_check.py "$S" > out/schema-check-released-fixtures.jsonl
python3 -I make_fixture.py fixtures
python3 -I schema_check.py "$S" fixtures/T11-MIN.als > out/schema-check-fixture.jsonl
python3 -I x-crc/x_crc.py out/x-crc.json
python3 -I -B fixture_audit.py "$S" ../../../../handoff released-fixture-audit.json
sh traces/a1a2/run_a1a2.sh
python3 -I make_manifest.py
