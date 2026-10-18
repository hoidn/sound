#!/bin/sh
# Regenerate S6 static evidence and the native pointer reads. Read-only on the bundle and Live.arm64.
# Query-server results (results/s6-000N) and corpus-excerpts.jsonl are retained copies, not regenerated here.
set -eu
B="/home/ollie/Ableton Live 12 Suite.app/Contents"
H=$(cd "$(dirname "$0")" && pwd)
BIN="$H/../../derived/Live.arm64"
python3 -I "$H/s6_schema.py" "$B/App-Resources/Schema" "$H/schema-survey.json"
python3 -I "$H/s6_documents.py" "$B" "$B/App-Resources/Schema" "$H/documents-survey.json" "$H/inputs-documents.tsv"
python3 -I "$H/curve_check.py" "$B" "$H/documents-survey.json" > "$H/curve-check.json"
# RTTI name -> typeinfo (name pointer at typeinfo+8) -> vtable (typeinfo pointer at vtable-8)
python3 -I "$H/scan_ptrs.py" "$BIN" 0x10587de30 0x10587de4f 0x10587de69 0x1058830f0 0x10587e733 0x10587e138 \
  0x10587f5e6 0x105827749 0x1058492f2 0x1058492d9 0x1058492c6 0x105849312 0x10587f683 0x10587e6a0 > "$H/rtti-scan-1.txt"
python3 -I "$H/scan_ptrs.py" "$BIN" 0x1067b16e0 0x1067b1748 0x1066948f8 0x106758f60 0x106758f78 0x106758f90 \
  0x106758fa8 0x1067b4650 0x1067bb808 0x1067bb8e8 0x1067d0f88 > "$H/rtti-scan-2.txt"
python3 -I "$H/vtable_owner.py" "$BIN" 0x1026f163c 0x1026f23f4 0x1026f23f8 0x102775904 0x102775908 0x1026ec730 \
  0x1026ef674 0x102778870 0x102778828 > "$H/interpolator-owners.txt"
{
  r() { echo "## $1: python3 -I read_ptrs.py <Live.arm64> $2 $3"; python3 -I "$H/read_ptrs.py" "$BIN" "$2" "$3"; }
  r "AFloatEvent (ctor FUN_1027785a0 stores 0x106806830)" 0x106806830 48
  r "AListAutomation (ctor FUN_102561388 stores 0x1067d06b8)" 0x1067d06b8 150
  r "TFloatAutomationInterpolator (typeinfo pointer at vtable-8; rtti-scan-2.txt)" 0x1067b1690 10
  r "TDiscreteAutomationInterpolator (typeinfo pointer at vtable-8; rtti-scan-2.txt)" 0x1067b1708 10
  r "TBezierCurveVector (typeinfo pointer at vtable-8; rtti-scan-2.txt)" 0x1066948d0 6
  r "OFloatAutomationSegmentsEvent (typeinfo pointer at vtable-8; rtti-scan-2.txt)" 0x106758b10 8
  r "TConversionAndInterpolatorProvider primary (typeinfo pointer at vtable-8)" 0x1067b97b8 8
  r "TConversionAndInterpolatorProvider secondary (typeinfo pointer at vtable-8)" 0x1067b9808 8
  r "AConvertCurved primary (typeinfo pointer at vtable-8)" 0x1067bacf8 6
  r "AConvertCurved secondary (typeinfo pointer at vtable-8)" 0x1067bafd0 6
  r "AFloatEvent slots +0x180..+0x228" 0x1068069b0 22
  r "AAutomationEnvelope (ctor FUN_102404910 stores 0x1067b0e98)" 0x1067b0e98 44
  r "AClipEnvelope (ctor FUN_102450330 stores 0x1067b81d0)" 0x1067b81d0 44
  r "APtrBase (ctor FUN_101535bd8 stores 0x1066779d8)" 0x1066779d8 48
} > "$H/vtable-reads.txt"
python3 -I - "$H" "$B" <<'PY'
import hashlib, json, os, platform, sys
h, b = sys.argv[1], sys.argv[2]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
files = {}
for d, _, names in os.walk(h):
    for n in names:
        p = os.path.join(d, n)
        rel = os.path.relpath(p, h)
        if rel != "manifest.json" and not n.endswith(".pickle"):
            files[rel] = {"sha256": sha(p), "bytes": os.path.getsize(p)}
docs = json.load(open(f"{h}/documents-survey.json"))
schema = json.load(open(f"{h}/schema-survey.json"))
m = {
    "id": "S6-AUTOMATION-V1",
    "packet": "S6 automation envelopes (FEAT-AUTOMATION): static half and native reader/evaluator",
    "target": "Ableton Live 12 Suite 12.4.3, Live.arm64",
    "binary": {"path": "../../derived/Live.arm64", "sha256": sha(f"{h}/../../derived/Live.arm64"), "image_base": "0x100000000"},
    "bundle": b, "host": platform.platform(), "python": sys.version.split()[0], "ghidra": "12.1.4",
    "command": "sh run.sh (static outputs, pointer reads, manifest); results/ are query-server copies",
    "sources": {
        "query_server": "R2FunctionDossier.java --serve over query-spool-2 (read-only LiveR2 copy); results copied unchanged into results/<id>/ with request.txt",
        "corpus": "C1/C2 corpus /var/tmp/sound-analysis/corpus (identity: corpus-decomp-run.json, corpus-indexes-manifest.json); records relied on retained in corpus-excerpts.jsonl",
    },
    "inputs": {
        "schema_files": {"count": schema["schema_files"], "digest_list": "schema-survey.json digests"},
        "documents": {"count": docs["inputs"]["files"], "parsed": docs["inputs"]["parsed"],
                      "appledouble_skipped": docs["inputs"]["appledouble_skipped"], "digest_list": "inputs-documents.tsv"},
    },
    "rounds": {"1": ["s6-0001 8 dossiers"], "2": ["s6-0002 8 dossiers"], "3": ["s6-0003 8 dossiers"]},
    "executed_live": False,
    "files": dict(sorted(files.items())),
}
json.dump(m, open(f"{h}/manifest.json", "w"), indent=1)
assert m["binary"]["sha256"] == "3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad"
PY
