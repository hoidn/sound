# Corpus Ramp Up: two libm sensitivity captures

Author freeze: 2026-10-19 Pacific / 2026-10-20 UTC. Independent review pending.

Exactly two additional original x86_64 Corpus captures ran through the unchanged
retained loader under [ADR 0003](../../../../wiki/decisions/adr-0003-no-reference-execution.md).
Only the existing child setting `XDEV_LIBM_ULP` changed: ASCII `+1` then `-1`.
The complete script bytes, all 38 values, input, 44.1 kHz, blocks 512, stopped
transport `{0,0,120}`, MXCSR `0x1f80`, time seed 0 and ordinary environment
allowlist match the frozen [Ramp packet](../depth-corpus-lfo-ramp-up/README.md).
No default or baseline capture was rerun. The prior two actual X captures remain
unchanged. Core dumps were disabled, child timeout 30 seconds, outputs exclusive.

Both new children exited 0 with 131,072 bytes / 16,384 finite stereo frames,
positive post-impulse energy in both channels, empty stderr, no trap hit and
`cxx-failbits 0`. `raw/` retains scripts, original output, stdout and stderr;
`attempt.json` retains actual environments, limits, providers and initialization.
All 422 watched historical/provider files, including all 22 frozen Ramp packet
files, remained unchanged. Mutable wiki context is preserved as of capture in
`context-asof.json`; checking never requires future wiki bytes to stay frozen.

Measured separately on both channels, directly after binary32-to-binary64 decode:
`sqrt(sum((trial-reference)^2)/sum(reference^2))`, frames 4096 through 16383.
No alignment, gain/phase fitting, window exclusions or demodulation is performed.
Bad lengths, non-finite samples and zero reference/channel energy are rejected.
The frozen Sine wrong-shape contrast is a retained-data calculation, not another
original call. Raw output checksums identify observations, not acceptance grades.

| Observation against frozen Ramp | Left relative RMS | Right relative RMS |
| --- | --- | --- |
| All selected results toward +infinity | 0.007040816883673096 | 0.006448055415935595 |
| All selected results toward -infinity | 0.0070807654465134115 | 0.006357018360077032 |
| Frozen Sine contrast | 1.4420001239754827 | 1.4066972582974695 |

`source-context.json` retains the exact full binding source and selected locators.
The existing `pf`/`pd` wrappers use `nextafterf`/`nextafter` toward numerical signed
infinity. They do **not** test floating-point inexactness: every result of a
selected function is stepped, including exactly representable results. There are
23 ordinary wrapper entries plus four fixed sincos/exp10 wrapper entrypoints.
The fixed sincos wrappers step both returned components. The binding path sets
the shared direction while resolving imports, before the original exports run.
Other floor/modf/ldexp/sqrt/etc bindings remain unchanged.

Both actual logs report selected-family calls to `___sincosf_stret` (180),
`_cbrt` (2), `_cosf` (2654), `_expf` (13), `_logf` (2864), `_sinf` (8988),
and `_tanf` (4). Import counts identify calls, not original Apple algorithms or
measured internal result traces. Declared unused trap slots are not trap hits.
The as-run collector's descriptive metadata initially said 25 ordinary entries;
author readback corrected that unsealed field to the actual 23, retaining the
collector code, source text and capture bytes unchanged. No capture was repeated.

These are two coherent function-family sensitivity directions, not a bound on
mixed per-call rounding errors, a confidence interval, Apple libm, arm64 or Live
behavior. The finite separation from this one Sine vector does not select an
acceptance threshold or characterize every wrong output. No LFO waveform/phase
reconstruction, frequency criterion, candidate execution, full-cycle or absence
of wrap is claimed; the right phase is offset and may wrap inside the vector.
No new normative case, release change, 174-modal grade or completion credit is
added. Q-001's global target remains open; any finite engineering criterion
needs its own explicit proposal and independent review.

The preceding Ramp capture was independently approved only as bounded X evidence
in [its review](../reviews/corpus-lfo-ramp-up-review.json), 24,406 bytes,
SHA-256 `b0005dc91623c1f629664d84dfe0bb3dfa5932e7579555dee2dfa48039cbc70d`.
That review supplies no new tolerance here. Source and prior providers are
immutable as-of inputs; no old runner, capture tool, checker, model, fit,
comparator, build, original application or other provider was executed.

Run only `python3 -B check.py --check`: retained-data verification, independent
metric recomputation and 14 negative fixtures, no original-code calls or writes.
The recorded `capture-once.py` is historical one-shot author code, not a replay
route; its fixed exclusive destination already exists. Checker write/replay
arguments and a repeated collector attempt are rejected before native calls.
