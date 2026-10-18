"""H4 static: self-checks over the outputs; writes out/checks.txt and exits non-zero on any failure.

Usage: python3 -I checks.py <out dir> <Devices/Mac dir>
Each check re-derives a claim made on wiki/research/device-bundles-static.md from the outputs (or the bundle bytes).
"""
import hashlib, json, os, plistlib, sys

ENTRY = {"_CalcA", "_CreateInstanceU", "_DestroyInstanceU", "_GetPlugInfoU", "_ResetA", "_SetParameterA", "_SetSampleRateU"}


def main(out, devdir):
    B = json.load(open(os.path.join(out, "bundles.json")))
    P = json.load(open(os.path.join(out, "params.json")))
    S = json.load(open(os.path.join(out, "scan.json")))
    T = json.load(open(os.path.join(out, "param_tables.json")))
    L = json.load(open(os.path.join(out, "live_strings.json")))
    seal = plistlib.load(open(os.path.join(devdir, "../../../_CodeSignature/CodeResources"), "rb"))["files2"]
    exp = lambda b, cpu: next({e["name"] for e in s["exports"]} for s in b["slices"] if s["cpu"] == cpu)
    key = lambda b, rel: f"App-Resources/Devices/Mac/{b['bundle']}/Contents/{rel}"
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(out, "param_table.tsv"))][1:]
    checks = [
        ("7 bundles, each universal x86_64+arm64", len(B) == 7 and all(sorted(s["cpu"] for s in b["slices"]) == ["arm64", "x86_64"] for b in B)),
        ("every slice exports the 7 C entry points", all(ENTRY <= {e["name"] for e in s["exports"]} for b in B for s in b["slices"])),
        ("non-Softube arm64 slices export exactly those 7", all({e["name"] for e in s["exports"]} == ENTRY for b in B if not b["bundle"].startswith(("Amp", "Cab")) for s in b["slices"] if s["cpu"] == "arm64")),
        ("executable SHA-256 recomputes", all(hashlib.sha256(open(os.path.join(devdir, b["executable"]["path"]), "rb").read()).hexdigest() == b["executable"]["sha256"] for b in B)),
        ("app seal hash2 equals each executable SHA-256", all(seal[key(b, "MacOS/" + os.path.basename(b["executable"]["path"]))]["hash2"].hex() == b["executable"]["sha256"] for b in B)),
        ("inner CodeResources identical and list no files", len({b["code_resources"]["sha256"] for b in B}) == 1 and not any(b["code_resources"]["files"] or b["code_resources"]["files2"] for b in B)),
        ("x86_64-only exports are C++ typeinfo symbols", all(n.startswith(("__ZTI", "__ZTS")) for b in B for n in exp(b, "x86_64") - exp(b, "arm64"))),
        ("Live image holds each entry-point name once", all(L["anchors"][n.lstrip("_")]["count"] == 1 for n in ENTRY)),
        ("every device has exactly one parameter path set", all(r["distinct_param_path_sets"] == 1 for r in P.values())),
        ("every declared Timeable field was seen", all(not r["declared_not_seen"] for r in P.values())),
        ("no Manual value outside the modal unmapped range", all(r[10] == "0" for r in rows)),
        ("1,064 device occurrences, 0 parse errors", sum(S["occurrences"].values()) == 1064 and not S["parse_errors"]),
        ("no shipped envelope targets these devices", all(not v for v in json.load(open(os.path.join(out, "envelopes.json"))).values())),
        ("Electric bundle and XML non-unit ranges coincide", not T["Electric"]["range_comparison"]["only_bundle"] and not T["Electric"]["range_comparison"]["only_xml"]),
        ("bundle table indices are unique", all(t["summary"]["entries"] == t["summary"]["distinct_indices"] for t in T.values())),
        ("set/clip target ids unique per document", S["set_clip_docs_with_duplicate_target_ids"] == 0),
    ]
    with open(os.path.join(out, "checks.txt"), "w") as f:
        for name, ok in checks:
            f.write(f"{'PASS' if ok else 'FAIL'} {name}\n")
    print(open(os.path.join(out, "checks.txt")).read(), end="")
    sys.exit(0 if all(ok for _, ok in checks) else 1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
