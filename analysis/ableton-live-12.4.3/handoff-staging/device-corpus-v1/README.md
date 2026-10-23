# Corpus audio comparison, release 1

**Reviewed handoff.** Read [the contract](spec.md), [cases](cases.json),
[measurement tool](compare.py), [manifest](manifest.json),
[role instructions](AGENTS.md) and [review disposition](REVIEW.md).
Approval covers only the explicit finite scope and measurement criterion.
A fresh restricted implementation workspace remains required.

The package contains 24 case groups, 68 evaluations, 61 distinct reference
renders and nine generated input signals. Seven evaluations vary the processing
protocol and compare with an existing base render. Each output has 16,384 stereo
frames, little-endian binary32 without a header. Reference outputs were made by
executing original x86_64 device code with substituted Linux libraries. Neither
the original application nor an arm64 executable was run. The measurements are
reviewed project acceptance criteria, not measured application compatibility.

This is a finite input/output comparison convention. Parameter vectors use named
comparison-domain values; they do not establish loading a project, the mapping
from stored position controls, the original application's audio chain or an API.
No executable, recovered application code, shipped musical audio or original
project document is included. Inputs were generated mathematically.

To compare candidate outputs, place one headerless stereo file per evaluation
in a directory, named exactly `<evaluation-id>.f32`, then run:

```sh
python compare.py /absolute/path/to/candidate-outputs > result.json
```

The tool uses Python, NumPy and SciPy. Their availability does not authorize an
installation. Exit status 0 means every defined measurement passed; 1 means at
least one failed or was not measurable. Missing, truncated, oversized and
non-finite outputs fail. A failed measurement must never be recorded as unknown
or a pass. A pass covers only the listed inputs and measurements. It does not
establish general sound equivalence or behavior outside the finite scope.
