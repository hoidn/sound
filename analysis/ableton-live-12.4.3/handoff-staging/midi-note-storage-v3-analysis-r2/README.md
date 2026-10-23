# MIDI note storage v3 corrected final-seal candidate

Metadata-only successor to the frozen first candidate. Only manifest.json and
REVIEW.md differ. All 82 other payload files, including all 78 gzip fixtures,
cases.json, spec.md, AGENTS.md and README.md, remain exact.

[Exact delta](metadata-correction.diff) removes the stale copied v2-to-v1
supersession object, retains the single accurate active v3-to-v2 relationship,
and records the sealed independent content review and pending final-seal gate.
No redundant historical ancestry is retained. The original candidate and its
manifest remain unchanged; no handoff was published.

`python3 -I -B check.py` reuses only the inspected data-only author checker,
redirects its report here, verifies old candidate preservation and the exact
allowed delta, and checks all payload hashes/links in an isolated copy.
The result is [author-validation.json](author-validation.json) plus
[final-seal-author-check.json](final-seal-author-check.json).
Independent final-seal review remains pending. No original/native/candidate
execution, new fixture generation or compatibility grade.
