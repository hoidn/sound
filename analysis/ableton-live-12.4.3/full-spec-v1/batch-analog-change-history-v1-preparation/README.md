# Analog eight-control change-history batch preparation

**Preparation only; no original calls performed.** This selects one whole eight-control local discovery batch after approved Analog route correction v2, manifest`44e0d729932f4d6626641b959d50db9ee178b07d141e666c55127b5ccb1e087d`, review`81b4d1ecccfe20bd7619f75b0fa7258d761e238a55e5e07b7d50fe55de789a10`. [selection.json](selection.json) fixes the inputs/history and [execution-plan.json](execution-plan.json) fixes every script, argv, output, environment, cap and measurement. [identities.json](identities.json) pins selected sources, the existing binary, original bundle/slice and current host libraries/environment. No original/provider/decoder/harness/compiler/model/comparator program has been run or imported in preparing this packet. Only owned stdlib checks ran on input data and fabricated sample bytes.

The legacy loader executes original module initializers and constructs original objects. This is outside the standing self-contained xexec call model. **Independent readiness approval of this exact frozen packet is required before Root invokes the collector.** The route-correction approval alone authorizes no original run. A working source file or existing binary is not a substitute for that setup review.

## One complete finite input family

All eight original retained control tuples are selected together: cutoff(index52→0.6), oscillator level(45→0.6), amplifier level(68→0.6), Volume(2→0.5), pan(71→0), oscillator semitone(31→19), oscillator detune(34→0.6) and amplifier AttackTime(105→0.9). The decimals here describe inputs; [baseline-vector.json](baseline-vector.json) and selection targets contain exact nearest-binary32 values and little-endian hex. All eight targets differ bitwise from baseline. These are eight perturbations/eight pairs, not eight new required predicates or cases.

The complete203-value baseline is selected without importing `an`, `measure` or a retained study driver: it is exactly current released `ANALOG-AUDIO-013-01`, source`handoff/device-analog-v1/cases.json#/cases/11/evaluations/0`, in its explicit parameter order. It enables chain1's saw oscillator, LP12 filter(cutoff0.5/Q0.6), amplifier and two envelopes with sustain1. Global Volume and the selected local controls belong to active paths. Chain2/random/noise/LFO/vibrato/glide are inactive. “Active” is an input-path qualification, not proof every setter changes a held note. AttackTime's held-note response is unknown; no numeric difference is a legitimate discovery.

This is a declared **matched released probe vector**, not a reconstruction of the old protocol probe. In particular its Q0.6 and selected key48 are taken from that released setting. No old13332/13340/13376/13390/17734 result is transferred to the new vector/history. The failed historical4400/two13312 sequence remains the repeated-note history qualified by ANRMAP-001.

For every control, the baseline and changed run each use a fresh process/instance, rate44100, all203values once in index order, stopped transport(position0/tempo120), absent/zero input and one queued note-on at frame8192, key48, velocity100. Process13312frames(26blocks), set that control to its baseline or target value respectively, then process7680frames(15blocks), then destroy. There is no note-off, reset, extra warm-up, unsupported clear-events verb or new harness. Re-sending the baseline value gives the same boundary setter count; it is not assumed to be a state no-op compared with omitting a setter.

## No-replay and grid premises

The original queue persists, but each `process` scans event coordinates using a fresh local counter.8192 lies in process1's interval[0,13312) and outside process2's interval[0,7680), so this note is delivered exactly once. It enters the process1 callback starting8192 at offset0. No queued event is appended between intervals. Both interval lengths are whole512-frame blocks, for41CalcA calls and20992output frames; process2's local-coordinate reset does not reset the original instance.

Under the owner's conditional zero-phase continuous processing rule, P44 gives g8184; because g precedes callback8192, g-prime is8228 and the first possible changed frame is8229. The change boundary13312 similarly gives first grid13332. These are stated source-rule premises, not a measured new onset, host-arrival expectation or trajectory oracle. No exact envelope phase at the change is asserted: one continuously held key does not by itself prove “during sustain.” Actual Live/grid/event/automation/ARM bindings remain unknown.

Each child has203initial setters, one boundary setter, create/rate/destroy and41CalcA calls: **248direct original C-export invocations**, below the256cap. Sixteen children produce3968such export invocations. Original initializer, constructor/destructor internals and import calls are **not** falsely included in248 or claimed bounded by256; they are the distinct setup-gated work this preparation submits for review. Logs retain initializer entries, import bindings and used-import counters. No hard all-internal-function-entry count is established by the unmodified harness.

## Binary, bindings and execution bounds

The existing `/var/tmp/sound-analysis/t12-analog/xdev` is149608bytes, SHA`3eec4ad1cfa0765c9e8267806cf02b7e664a07157043e3a170388cfa4d63cf14`, matching the historical T12 build manifest. All five retained harness source files match that manifest. There is no automatic build, compiler invocation, installation, binary replacement or import of `xdevpy`. Current executable/source correspondence rests on the retained build record; this preparation does not recreate compilation.

The original bundle/slice and file-offset hash are checked from pinned retained offsets, without a decoder. Linux libc/libm/libstdc++/libgcc/dynamic-loader files and `ld.so.cache`, the current Python executable and host/glibc metadata are pinned. Child environment is exactly C locale, UTC, system PATH and `XDEV_TIME=0`; inherited environment, LD_PRELOAD/LD_LIBRARY_PATH, XDEV_LIBM_ULP and other driver overrides are absent. Per-call MXCSR is0x1f80. Original module initializers execute before parsed commands, as the retained loader source states; no false initializer FP/control claim is made.

Substitutions remain existing glibc libm, inferred Park–Miller rand, fixed time0, C-locale/rune and libc++ stream/string shim plus libstdc++ RTTI. Nothing establishes the real Apple random distribution, Apple libm or ARM equivalence. Future import/init/used logs record the actual selected run; standard library target/cache pins are not a new live-loader observation. Unbound imports retain the existing first-call/read trap.

The collector is single-threaded, with one attempt per child and stop on the first fault or invalid result. Per child:20s wall timeout,10s CPU,1GiB address-space ceiling, zero core limit and262144bytes per-file ceiling. Output must be exactly167936bytes(20992interleaved stereo binary32 frames); stdout/stderr is retained in a bounded file. Timeouts/interruption kill that process group, preserve partial artifacts and stop without retry. Null create, nonzero/signal exit, trap/error text, nonzero libc++ failbits, wrong logged command/block counts or invalid output also stop the entire batch. Caps may themselves cause a stopped discovery; the collector does not relax them or rerun.

## Preselected output checks, not a calibrated oracle

Every sample in both outputs must be finite. Each baseline channel must have positive finite full-capture sum of squares. Positive energy is a runtime validity gate, not an already observed new-history fact or calibrated loudness criterion. Baseline and changed first13312frames must be byte-identical, with numeric identity also reported. A signed-zero-only prefix bit difference fails that identity gate but is not called a numeric audio difference.

Report the first numerical binary32 difference cumulatively, separately for left/right and jointly(anychannel), plus its offset from13312. +0 and−0 compare numerically equal. An unchanged capture returns `None` for that channel/joint, which is valid discovery rather than a failed expectation. Full hashes/sizes and positive baseline energies are retained; no fitting, alignment, normalization, frequency/trajectory inference, smoothing duration,100ms settling bound or published comparison metric is introduced.

All captures remain **UNGRADED discovery** until actual-result review and owner reconciliation. The current finite release excludes parameter changes; these new inputs have no retained expected waveform, calibrated eligibility/tolerance or ARM/Live timing oracle. Passing file/energy/prefix checks proves capture validity only.

## Review and Root execution contract

[collector.py](collector.py) has two mutually exclusive modes. Preparation/review uses only:

```sh
python3 analysis/ableton-live-12.4.3/full-spec-v1/batch-analog-change-history-v1-preparation/collector.py --self-check
```

`--report-file` optionally writes the owned selfcheck report. After sealing, reviewers must place that report outside this frozen packet. The owned fixtures test queue replay, output size/finiteness, per-channel energy, prefix identity, signedzero semantics, independent channel/joint differences, call-count metadata and readiness/seal rejection. They use fabricated bytes only and never spawn a child. [preflight.json](preflight.json) records the author run; it is not independent approval or evidence of original output.

For the later Root invocation, the independent readiness receipt must have:

```json
{
  "disposition": "approved-bounded-analog-change-history-preparation",
  "ready_for_root_execution": true,
  "reviewed_manifest": {
    "path": "analysis/ableton-live-12.4.3/full-spec-v1/batch-analog-change-history-v1-preparation/manifest.json",
    "sha256": "THE_EXACT_FROZEN_PREPARATION_MANIFEST_HASH"
  }
}
```

Only after that approval, Root may use `collector.py --execute-after-review /absolute/path/to/receipt.json`. The collector requires this matching receipt and the frozen payload identities, then rechecks source/binary/library/input identities before any original child. Exact original-child argv/input/output paths are already listed for all16runs in the execution plan. It creates only the separate, previously nonexistent sibling `batch-analog-change-history-v1-actual`; an existing result path is rejected. The sealed preparation stays immutable. Full logs, inputs by sealed reference, resource/return records, raw outputs and finite discovery measurements are retained there. No automatic retries, continuation or owner/case/release edit occurs.

Current gates are honest: independent readiness/setup approval is absent; new-history outputs, positive energies and prefix identity have not been observed; any runtime validity failure stops the batch; calibrated trajectory/public-binding gaps remain. No original run is authorized by this author preflight alone.
