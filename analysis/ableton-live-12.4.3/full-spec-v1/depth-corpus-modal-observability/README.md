# Corpus retained modal observability: first D01 numerical investigation

**New numerical inference; independent review pending as of author freeze.**
The existing captures support a concrete additional *measurement* route for
Membrane mode 1. They also show that four low-pitch exclusions cannot all be
explained by the old estimator's reported bias. No omission is regraded here.

[Diagnostics](diagnostics.json) reconciles exactly the existing 174 omitted
mode/channel/evaluation occurrences across 14 evaluations. Each row points to
its actual traceability record and historical measurement row. It retains the
original reason and ungraded status, with these new descriptive categories:

| Retained numeric evidence | Occurrences |
| --- | ---: |
| Model's own frequency estimate also outside the old band | 168 |
| Reference offset despite small reported model-estimator bias | 4 |
| Historically unresolved: decays before estimator settles | 2 |

The historical release test used **reference estimate / static pole center**
within `1e-4`, not the analyzer's separate model-estimator-bias test. That test,
all 174 omissions, and all frozen release bytes remain unchanged. These counts
are diagnostic classifications, not required-outcome numerators or passes.

## What the two captures add

The new [numerical script](diagnose.py) reads only the two retained headerless
little-endian binary32 stereo captures. Each is 16,384 frames, with 12,288
post-impulse samples nonzero in **each** channel. Source run metadata supplies
44,100 Hz and impulse frame 4096. Released reference bytes equal the retained
historical raw bytes exactly; hashes and paths are in the diagnostic input pins.
This does not rerun the old host or renew its historical x86 provenance.

The estimator forms a Hankel matrix from sampled capture values, obtains an SVD
signal subspace, and estimates frequencies from its shift eigenvalues. No old
model/estimator/comparator function is imported or executed. No static frequency
is supplied to the fit. Frequency intervals only select the resulting rows for
display; they do not initialize or constrain fitted poles. Rank, aperture,
window and stride remain assumptions of this **analysis**, not a proposed
device architecture or behavioral law.

| Observation | New numerical result | Consequence |
| --- | --- | --- |
| Low pitch 009-01, mode 0, both channels | Across all 16 variants per channel: roughly 66.16644–66.16705 Hz, versus historical center 66.14462746 Hz | Corroborates a retained center offset; not merely the old model's approximately `1e-8` relative estimator bias. |
| Low pitch 009-01, mode 1, both channels | Across all variants: roughly 132.25628–132.25840 Hz, versus center 132.23523615 Hz | The old `1e-4` exclusion remains; no relaxed threshold is proposed. |
| Low pitch 009-01, mode 3 | Rank/window-dependent: roughly 264.36958–264.49341 Hz left and 263.93150–264.49168 Hz right | Inconclusive for a stable standalone modal observation; stronger rank assumptions introduce additional fitted poles. |
| Membrane 006-01, mode 1 | Full-window rank 100/120, matched apertures at stride 4/8/16: 279.29230251–279.29249369 Hz left; 279.29233013–279.29238277 Hz right | Both captures contain a repeatably estimable component near the historical 279.29229076-Hz center, unlike the old left estimate 261.44658739 Hz. |

The last row uses a **selected, explicitly disclosed subset** of the 26
Membrane experiments. All 58 total experiments, including the 32 low-pitch
experiments, are retained. Membrane rank-80 and short-aperture controls drift:
the full tested left-channel range reaches 279.36786448 Hz; the right reaches
279.29603409 Hz. These failures prevent a claim that any rank/window is valid.
The variant set followed exploratory scratch calculations; it is not a
preregistered or independent holdout validation.

The historical single-mode demodulator requests a 7.06732254-Hz cutoff for
Membrane mode 1's 17.66830636-Hz nearest-mode gap. Its uncapped length is 20,591
taps, but `fit.py` caps at 4,001. The capture has only 12,288 samples after the
impulse. Both the old reference and old model estimates shift together, with
the left estimate near the stronger neighboring 261.624-Hz component. This
supports **finite-record isolation/neighbor contamination as an inference**;
it does not prove the cap is the sole cause or justify changing its threshold.

For low-pitch modes 0/1, the old reported model bias is tiny while the reference
offset is not. Existing coefficient-sensitivity bounds are context only: these
diagnostics do not establish the coefficient-generation/rounding mechanism,
an application tuning default, a general pitch law or an arm64 result.

## Concrete next evidence dependency

A reviewer can select **006-01 mode 1 left/right frequency** as a bounded new
modal-observation proposal using these existing captures. Before any normative
criterion or eligibility addition, independently check mode identity, rank and
window sensitivity, aliasing/nuisance-component controls, and an explicit
measurement procedure with justified uncertainty. The synthetic five-tone
sanity fixture is not that complete calibration. Do not derive a tolerance
from the successful variant spread or treat a repeated analysis of the same
capture as compatibility evidence. Low-pitch 0/1 additionally need an explicit
decision on measured versus static centers; mode 3 remains unresolved.

This packet creates no requirement, case, expected/comparison oracle, candidate
result, new reference execution or coverage credit. The historical 1,427 eligible
modal occurrences remain a metric-eligibility count, never a required-outcome
numerator. The existing 174 are ungraded until a separately reviewed successor
criterion/evidence decision. No provider/original execution, audio playback,
device implementation, broader binary trace, A1 investigation or source fetch
occurs here. Other twelve omission-bearing evaluations receive only retained
record classification; their captures are not newly analyzed.

## Reproduce read-only

Fully inspect the new script before running:

```sh
OPENBLAS_NUM_THREADS=1 python3 -B analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-modal-observability/diagnose.py --check
```

It imports installed NumPy/SciPy only, reads immutable pins, reproduces 58
experiments and a mathematical five-tone fixture, checks exact original
174-record membership/pointers and preservation, and rejects four mutations.
The `1e-8` relative JSON numerical reproduction allowance is an analyst
reproducibility check, **not** a target audio/frequency/compatibility tolerance.
`--write` is refused before numerical imports. With no argument it prints new
diagnostic JSON to stdout; neither mode writes any file. It does not execute old
source code. `fit.py`, analyzer and staging builder are pinned and read as data
only. Sealed input paths are immutable as-of providers, not evolving wiki gates.
