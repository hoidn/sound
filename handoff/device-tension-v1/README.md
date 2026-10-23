# Tension finite audio release, version 1

**Reviewed local release with finite scope.** Read [the contract](spec.md),
[cases](cases.json), [measurement code](compare.py), [manifest](manifest.json),
[role instructions](AGENTS.md) and [review disposition](REVIEW.md).

27 cases include complete named comparison vectors, generated notes/zero
input, retained mono reference samples and exact signal-measurement settings.
The scope is 26 settings with stable numerical sensitivity and one repeated
strike with a separate waveform criterion. Chaotic settings and outputs
without per-setting calibration are excluded. No application or arm64 run,
candidate compatibility result or general sound-equivalence claim is made.

Write one mono headerless little-endian binary32 output per evaluation,
named `<evaluation-id>.f32`, into a directory, then run:

```sh
python compare.py /absolute/path/to/candidate-outputs > result.json
```

The comparator uses Python, NumPy and SciPy; no installation is authorized.
Exit 0 means every specified measurement passed; exit 1 means a failure or
missing/unmeasurable result. This package contains no executable device,
recovered synthesis code, shipped project or musical recording. A restricted
implementation workspace is required.
