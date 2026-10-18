#!/bin/sh
# Reviewer step (analyst-side): re-hash the staged package, export a copy outside the checkout and
# run every package check on it. Appends to review-checks-static.txt to form review-checks.txt.
# usage: sh run_package_checks.sh <scratch dir>
set -eu
H=$(cd "$(dirname "$0")" && pwd); A="$H/.."; S="$A/../mixer-values-v1"; X="$1/review-export"
python3 -I "$H/finalize_manifest.py" "$S"
rm -rf "$X"; mkdir -p "$X"; cp -a "$S" "$X/"; E="$X/mixer-values-v1"
{
  cat "$H/review-checks-static.txt"
  echo "== 7. Reviewer model on the exported copy =="
  python3 -I "$H/reviewer_model.py" "$E"
  echo
  echo "== 8. Package checks on the exported copy =="
  python3 -I "$H/package_checks.py" "$E"
  echo '$ build_mv1.py verify <export>'
  (cd "$1" && python3 -I "$A/build_mv1.py" verify "$E") | python3 -I -c "import json,sys;r=json.load(sys.stdin);print({k:r[k] for k in ('payload_files','manifest_sha256','hash_or_size_mismatches','inventory_differences','unresolved_links','missing_case_inputs','deny_list_hits')})"
  echo '$ midi-config-v2 reviewer verify_copy.py <export>'
  (cd "$1" && python3 -I "$A/../midi-config-v2-analysis/review/verify_copy.py" "$E")
  echo "export copy identical to staging:"; diff -r "$S" "$E" && echo yes
  echo "staging manifest sha256: $(sha256sum "$S/manifest.json" | cut -d' ' -f1)"
  echo "Note: do not rerun build_mv1.py build or seal on the reviewed package; both regenerate candidate status and the unreviewed manifest."
} > "$H/review-checks.txt" 2>&1
tail -4 "$H/review-checks.txt"
