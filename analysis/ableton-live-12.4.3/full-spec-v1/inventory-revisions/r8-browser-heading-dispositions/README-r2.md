# R8 checker successor

The [original scope and findings](README.md), fourteen dispositions and 46 exact
reference records are unchanged. The first [seal](manifest.json) and all six
payloads remain byte-for-byte intact. Its initial `derive.py --check` rejected
the heading-disposition snapshot because Python HTML attribute tuples serialize
to JSON lists. This is a checker representation defect, not a source discrepancy.
No failed validation was relabeled as a pass.

Inspect [check.py](check.py), then use this successor command:

```sh
python -B analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r8-browser-heading-dispositions/check.py --check
```

It invokes only the sealed analyst derivation as data-processing code, normalizes
the reconstruction through JSON before comparison, and checks all inputs,
source/navigation/outline fixtures, ledgers, old and new seals, links, whitespace
and the complete before/after file hash set. No original capture script runs.
Both checkers are read-only; the original creation mode still refuses after its
seal. The [successor seal](manifest-r2.json) pins the exact old seal and payloads
plus this response and the corrected checker. Independent review remains pending.
