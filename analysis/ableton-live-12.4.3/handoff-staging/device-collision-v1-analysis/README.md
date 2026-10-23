---
id: ANALYSIS-DEVICE-COLLISION-V1-CANDIDATE
type: research
status: draft
updated: 2026-10-19
access: analysis
---

# Collision candidate provenance and author checks

This analyst-only companion must not enter the implementation export. The clean
sibling is `../device-collision-v1/`. Its review and publication remain pending.
The canonical draft and research are `wiki/specs/device-collision.md` and
`wiki/research/device-collision-dsp.md` from the repository root.

`build.py` reads the immutable 2026-10-18 t12-collision-v1 evidence through its
recovery mapping, verifies all 103 original manifest entries, and extracts the
IEEE binary32 RIFF data chunks of `raw/ctor_c4.wav` and `raw/wg_pipe.wav`
verbatim. It parses their exact `.script` input records as data. It does not
import or execute original functions, recovered code, models or rendering tools.
The N6 conversion table is independently hash checked against the evidence
manifest and used only to assign descriptive control labels to exact vectors.
No stored-value conversion is performed or promised by the candidate.

`source-validation.json` records every logical and recovered physical path,
original digest and byte count. `traceability.json` maps both exported cases to
original WAV/script bytes, result rows and decoded hashes. The current edited
`run_collision.py` and `results/collision.json` paths are never read; their
unknown-provenance extras are not used. The source manifest, recovery inventory,
recovered originals and all current original-packet paths are left unchanged.

Calibration is the original `results/libm_sensitivity.json` `pipe` row.
`libm_sensitivity.py:CASES/main` specifies resonator type 5, decay 1, Q parameters,
C4 velocity 100 on frame 0 held, 44.1 kHz, 32,768 frames, default block/warm-up;
`run_collision.py:Q/run` and `raw/wg_pipe.script` agree on that setup. Its
`rel` function computes joint stereo whole-window relative RMS. The candidate
uses exactly that metric/window; maximum reported perturbation error is
0.0006108612471224301 against proposed 0.003. The calibrated temporary audio
is unretained, limiting independent recalculation of that experiment.
No new original execution or broadened tolerance is used to close this gap.

No modal cases are selected: reported library sensitivity covers onset/frequency,
but not the portable complex-amplitude/log-radius estimator bounds proposed in
the draft. Tube, sampled pitch envelope and unresolved/noise cases are also
excluded. This is a finite first candidate, not full Collision, five-device or
T1 audio completion. The two cases release no exact synthesis law or independent
frequency estimator.

Reproduce packaging and author checks from the repository root:

```sh
python3 analysis/ableton-live-12.4.3/handoff-staging/device-collision-v1-analysis/build.py
python3 -B analysis/ableton-live-12.4.3/handoff-staging/device-collision-v1-analysis/validate.py
```

`author-validation.json` records reference self-comparison, every-case silence
and gain mutations, audible injection for the constructor case, malformed,
nonfinite and wrong-length inputs, missing files, exact inventory, payload links,
source-token exclusion, and isolated copied-export CLI results. Valid silence
and gain scaling remain passes for the absolute effectively-silent boundary;
they fail for the audible Pipe case. Those are tool sensitivity checks, not
independent candidate-rendering or original-application comparisons. Independent
review must inspect behavioral sufficiency and semantic source exclusion, not
only trust a token scan or author report.
