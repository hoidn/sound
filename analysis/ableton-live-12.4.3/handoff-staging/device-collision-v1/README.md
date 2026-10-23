---
id: HANDOFF-DEVICE-COLLISION-V1
type: overview
status: released
updated: 2026-10-19
access: handoff
---

# Collision audio: finite release

**Reviewed local release.** This package defines two bounded output checks
for Ableton Live 12 Suite 12.4.3 Collision. Read the [review](REVIEW.md).
It establishes no application, arm64 or candidate compatibility result.

Read [the contract](spec.md), then [the exact cases](cases.json). To compare an
independent renderer, write `DEVICE-COLLISION-001.f32` and `DEVICE-COLLISION-002.f32` into a directory and run:

```sh
python3 compare.py /absolute/path/to/candidate-outputs
```

Python 3 standard library suffices. Files contain exactly the case's declared
number of interleaved left/right IEEE binary32 little-endian frames, without a
header. Missing, empty, wrong-length, NaN and infinity audio fails. The JSON
report contains each measured error and limit; exit 0 means both checks pass,
exit 1 means at least one fails. A comparator pass only covers the declared
metrics and inputs. Use `python3 compare.py reference` for an integrity and
self-comparison smoke check; that is not a candidate rendering result.

[The manifest](manifest.json) lists SHA-256 digests and byte counts for every
payload file except itself. Audio is losslessly extracted from earlier original
x86_64 output captures; no original execution occurred during packaging. The
measurement program synthesizes no audio. No public source approval is needed
for its Python standard library operations. The package contains no executable,
recovered DSP code or original synthesis algorithm. Reviewer acceptance of the
outputs' sharing suitability remains pending.
