"""Apply the review disposition to the staged browser-index-v1 package (reviewer step).

Order: build_bi.py build -> this script -> build_bi.py seal (re-hashes the inventory).
Usage: python3 -I finalize_bi.py STAGE_DIR
"""
import json, sys
from pathlib import Path

REVIEW = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVB-01 high: cases 016 and 017 expected tags from entries naming a file in a subfolder and a folder; the "
        "reviewer's static check shows a user folder's sidecar applies only to files directly inside the folder, "
        "by name; both cases removed, REQ-005 clause 1 and REQ-003 clause 2 narrowed, inputs excluded",
        "RVB-02 low: an entry naming no file is never applied, and the application then treats the sidecar as "
        "changed without it; whether it rewrites the file is untraced; excluded behavior added; the no-interference "
        "assumption is now supported and removed from the assumption list",
        "RVB-03 low: observation obligations did not say that absence from a view is not an observation; clarified, "
        "and an item not presented or offered makes the comparison inconclusive; no expectation changed",
        "RVB-04 editorial: the factory and built-in cases now state how 'no sidecar written inside' is compared",
        "RVB-05 editorial: payload status wording set to reviewed release; review record added; inventory re-hashed",
        "RVB-06 info: colour entry rule re-derived from the retained evidence and the pinned build; only exactly 1 "
        "to 7, 0, 8 and empty are graded; cases 019 to 021 confirmed",
        "RVB-07 info: written-sidecar comparison is by data model and tolerates extra item fields, empty bags, "
        "informational properties and any serialization; confirmed for cases 023 to 025",
        "RVB-08 info: kind table, four sidecar names and evidence identity re-checked independently; all matched",
        "RVB-09 info: remaining stated assumptions accepted with reasons; no expectation invented",
        "RVB-10 info: fixture and sharing review; 26 authored fixture files, no shipped content; acceptable",
        "RVB-11 info: scope rulings; kind table without a listing claim, override names, ten new cases and the "
        "exclusion in place of the two planned reference observations accepted",
    ],
    "disposition": "Approved with listed narrowing (RVB-01, RVB-02), only for the explicit partial clauses; 26 cases; "
                   "expectations static-derived; reference and candidate execution not-run; restricted "
                   "implementation workspace required",
    "record": "REVIEW.md",
}


def main(stage):
    stage = Path(stage)
    cases = json.loads((stage / "cases.json").read_text())
    cases["status"] = "released-reviewed"
    (stage / "cases.json").write_text(json.dumps(cases, indent=1, ensure_ascii=False) + "\n")
    man = json.loads((stage / "manifest.json").read_text())
    man.update(release_status="released", release_date="2026-10-18", review=REVIEW)
    (stage / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    print("finalized:", man["release_status"], man["release_date"], man["case_count"], "cases")


if __name__ == "__main__":
    main(sys.argv[1])
