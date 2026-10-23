# Analog finite audio-output release, version 1

**Reviewed local release, dated 2026-10-19.** Read the [contract](spec.md),
[cases](cases.json), [comparison tool](compare.py), [manifest](manifest.json)
and [role instructions](AGENTS.md). The [review](REVIEW.md) approves the finite
scope and project metric with two protocol/measurement clarifications.
A fresh restricted workspace is required before clean implementation.
No restricted implementation workspace is provisioned here.

The release has 38 case groups and 42 evaluations, with exact parameter vectors,
note events, generated silent inputs and original-device reference outputs. The
references came from retained extracted execution of original x86_64 Analog code
with substituted Linux libraries. Neither the original application nor arm64 device
code was executed. A passing comparison measures finite contract conformance,
not application compatibility or complete spectral equality.

The package excludes random/statistical outputs, unvalidated pitch-modulation
trajectories, glide, unison, unrendered modes, arbitrary automation and Live/file
integration. All vectors use explicitly defined named comparison-domain values.
They are not a claim about the application's API or stored-value mapping.
No recovered DSP/synthesis code, executable, shipped music or project document
is included. The executable Python tool only measures supplied audio.

Provide one headerless little-endian stereo binary32 file per evaluation, named
`<evaluation-id>.f32`, then run:

```sh
python compare.py /absolute/path/to/candidate-outputs > result.json
```

The tool requires Python, NumPy and SciPy; their use here authorizes no installation.
Exit 0 means every listed measurement passed; exit 1 means a comparison failed or
could not be measured. Missing, malformed, non-finite and silent outputs fail.
