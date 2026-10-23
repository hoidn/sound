# Electric finite audio release, version 2

**Reviewed local release.** See the [review](REVIEW.md). Read [the contract](spec.md),
[cases](cases.json), [comparison measurements](compare.py),
[manifest](manifest.json) and [role instructions](AGENTS.md).

117 finite evaluations contain explicit named parameter vectors, generated
note events and zero input signals, exact retained mono reference samples and
frozen signal measurements. Expectations are extracted original-code outputs
under the stated protocol with substituted libraries. No application or arm64
execution and no candidate compatibility result is claimed. Approval covers
only the stated finite scope and measurements.

Place one mono headerless little-endian binary32 file per evaluation into an
output directory, named `<evaluation-id>.f32`, then run:

```sh
python compare.py /absolute/path/to/candidate-outputs > result.json
```

Python, NumPy and SciPy are required; this does not authorize installation.
Exit 0 means every defined measurement passed; exit 1 means a failure or
missing/unmeasurable output. A pass covers only enumerated inputs and selected
measurements. No executable device, recovered synthesis code, shipped project
or musical recording is included. Notes and zero inputs were authored for
these tests; numeric control vectors and original-code outputs are reviewed
fixtures, not an original API or required candidate design.

This supersedes device-electric-v1 solely to correct a contradictory permission
sentence. All cases, reference data and comparison code are unchanged.
