"""Set the reviewed status and review fields in the staged manifest and re-hash every payload file.

Usage: python3 -I finalize_manifest.py STAGE_DIR
"""
import hashlib, json, sys
from pathlib import Path

stage = Path(sys.argv[1])
mp = stage / "manifest.json"
man = json.loads(mp.read_text())
man["release_status"] = "released"
man["release_date"] = "2026-10-18"
man["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVP-01 low: comparison obligation 3 did not attribute loads of entries outside every searched folder (cases 016, 035); clarified; no expectation changed",
        "RVP-02 low: manifest behavior exclusion restated an unreleased ordering clause (VST3 before VST2); reworded to the contract's neutral wording",
        "RVP-03 info: candidate set ruled observable for directory entries; open application-side discovery items are excluded or concern only how a probe starts a scan",
        "RVP-04 low: plain-file candidacy has no established reference observation; obligation 4 now names cases 021 (J.vst3) and 028; expectations unchanged",
        "RVP-05 info: the author's seven proposed draft corrections confirmed; none leaks into the payload",
        "RVP-06 info: three assumptions confirmed by the reviewer's reading, two accepted as stated assumptions; no expectation invented or changed",
        "RVP-07 info: 20 new cases, the candidate-set representation and the subset's usefulness accepted",
        "RVP-08 editorial: payload status wording set to reviewed release; review record added; inventory re-hashed",
        "RVP-09 info: evidence identity re-checked on 2026-10-18; all hashes matched",
        "RVP-10 info: sharing review of folder paths and invented names; acceptable",
    ],
    "disposition": "Approved with listed clarifications (RVP-01, RVP-02, RVP-04), only for the explicit partial clauses; no scope narrowed; expectations static-derived; reference and candidate execution not-run; restricted implementation workspace required",
    "record": "REVIEW.md",
}
man["files"] = [{"path": str(p.relative_to(stage)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                 "bytes": p.stat().st_size}
                for p in sorted(stage.rglob("*")) if p.is_file() and p.name != "manifest.json"]
mp.write_text(json.dumps(man, indent=1) + "\n")
print("files", len(man["files"]), "manifest sha256", hashlib.sha256(mp.read_bytes()).hexdigest())
