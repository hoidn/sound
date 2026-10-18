"""H4 static: flatten out/params.json into out/param_table.tsv and out/param_summary.json.

Usage: python3 -I tables.py <out dir>
Columns of param_table.tsv (one row per device parameter seen in shipped documents):
  device, path, class, docs (occurrences carrying it), kinds (stored text kinds), manual_min, manual_max, distinct,
  range (modal unmapped MidiControllerRange Min..Max; for TimeableBool the MidiCCOnOffThresholds pair),
  range_other (occurrences whose unmapped range differs from the modal one), outside (Manual values outside the
  modal range, floats/ints only), mapped (occurrences with a KeyMidi mapping), automation, modulation (occurrences
  with AutomationTarget / ModulationTarget), default (Manual value in the shipped Core Library/Defaults preset).
The modal unmapped range is a stored property of shipped documents; whether it equals the declared parameter
range is an inference recorded on the research page, not here.
"""
import json, os, sys


def main(outdir):
    P = json.load(open(os.path.join(outdir, "params.json")))
    rows, summary = [], {}
    for dev, r in P.items():
        s = {"occurrences": r["occurrences"], "params": len(r["params"]), "distinct_param_path_sets": r["distinct_param_path_sets"],
             "by_class": {}, "range_other_params": 0, "outside_params": 0, "with_default_preset": 0}
        for path, a in r["params"].items():
            cls = a["declared_class"]["top"][0][0]
            s["by_class"][cls] = s["by_class"].get(cls, 0) + 1
            rk = "MidiCCOnOffThresholds.pair" if cls == "TimeableBool" else "MidiControllerRange.pair"
            rng = a.get(rk)
            modal, other, outside = "", 0, 0
            if rng:
                modal = rng["top"][0][0]
                other = rng["n"] - rng["top"][0][1]
                if cls != "TimeableBool":
                    lo, hi = (float(x) for x in modal.split(".."))
                    outside = sum(c for v, c in a["Manual"]["top"] if v not in ("true", "false") and not lo <= float(v) <= hi)
            s["range_other_params"] += other > 0
            s["outside_params"] += outside > 0
            s["with_default_preset"] += a["default_preset"] is not None
            m = a["Manual"]
            rows.append([dev, path, cls, a["present_in"], "+".join(sorted(m["kinds"])), m["min"], m["max"], m["distinct"],
                         modal, other, outside, a.get("KeyMidi.Channel", {}).get("n", 0),
                         a.get("AutomationTarget.present", {}).get("n", 0), a.get("ModulationTarget.present", {}).get("n", 0),
                         "" if a["default_preset"] is None else a["default_preset"]])
        summary[dev] = s
    head = ["device", "path", "class", "docs", "kinds", "manual_min", "manual_max", "distinct", "range", "range_other",
            "outside", "mapped", "automation", "modulation", "default"]
    with open(os.path.join(outdir, "param_table.tsv"), "w") as f:
        f.write("\t".join(head) + "\n")
        for row in rows:
            f.write("\t".join("" if v is None else str(v) for v in row) + "\n")
    json.dump(summary, open(os.path.join(outdir, "param_summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
