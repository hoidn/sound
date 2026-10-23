# Mix leaf batch — 2026-10-20

Pending one independent batch review. Selected after the
[approved mix map](../family-mix-routes-v1/manifest.json) and its
[independent review](../reviews/family-mix-routes-v1-review.json), under plan
revision 4's standing existing-harness authorization. This batch changes no
normative requirement, acceptance object, release or application grade.

## Selection and actual execution

[selection.json](selection.json) and [inputs.json](inputs.json) record the finite
set before execution. All 137 unpatched recorded-model command rows nominated
by MXB-01–05 were replayed through the existing T14 loader, SHA256
`188b1197bd69ab4700ae47eade48f00982a2d11139d865f3cee46e64b80d3078`.
The separate base tools/xexec binary lacks `poke` and was not substituted for
this historical model. No loader was compiled or modified. Existing T14 source,
Python driver, manifest and exact x86 image identities are in [pins.json](pins.json).

Seven additional processes call the seven scalar crossfade functions at 43
binary32 positions each: immediate binary32 neighbors of −1, −0.96, −0.95,
−0.94, −0.9375, −0.75, −0.5, 0, 0.5, 0.75, 0.9375, 0.94, 0.95, 0.96 and 1,
restricted to [−1,1]. At zero these include ±2^-149. The complete exact hex
inputs precede results. These are exploratory finite results with no prior
expected value, not a new inferred curve law or application outcome.

[run.py](run.py) invoked 144 existing-harness processes with 20-second timeouts,
core dumps disabled, C locale, no automatic retry and no original-code patches.
[results.jsonl](results.jsonl) retains each exact argv, environment, time,
stdout/stderr and completion. All 144 exited 0, without timeout or reported
trap/fault. They returned 517 direct harness calls: 216 from retained shapes plus
301 boundary calls. That total includes 32 return-only entry calls used to
allocate owned buffers; the other 485 are direct calculation/control entry calls.
Internal calls and callback returns are not independently counted here.

The exact existing return-only callback at `0x101b0ee93` remains in the recorded
switch shapes. Imported math is substituted: `_cos` was called 66 times and
`_cosf` 288 times. The first process retains the complete loader import-binding
list; every process retains used-import counters. These are Linux glibc/libm
results, not measurements of Apple's math functions or arm64 execution.
The [36 allocator-patching rows](withheld-patched-rows.json) were withheld and
remain outside standing authorization. No original constructor beyond the
existing recorded harness model was introduced.

## Finite result analysis

[analyze.py](analyze.py) uses the existing xexec output parser as data processing,
without constructing Runner or executing code. [analysis.json](analysis.json)
records exact equality for all 77 historical dumps and 99 declared scalar return
fields, with zero mismatches. Dumps compare byte for byte; no address
normalization is applied. Only documented return fields are compared: float
low lanes, packed ramp target/length, fade sample count and Bezier double pair.
Unspecified volatile registers are excluded from that comparison.

[boundary-levels.json](boundary-levels.json) retains all 301 binary32 output bit
patterns. Forty-nine repeat historical function/position pairs and match exactly;
252 are distinct new pairs. These counts are evaluations, not required outcomes.
One finite Fast Cut result, at input `0x1.eb851e0000000p-1` (binary32 0.96), is
`0xb33bbd2e`, approximately −4.37113883e−8. This does not support clamping the
helper's computed output to nonnegative values. Its math import is substituted;
no public crossfader/audio or target-platform sign claim follows.

The new boundary rows remain ungraded discovery pending independent review and
canonical-owner reconciliation. The reviewed map's 110 predicates and
17 X / 70 S / 23 no-established-route inventory remain unchanged. Actual
TrackOut receiver, active automation timebase, bus/host/render output and ARM
precision equivalence are still unjoined. This batch supplies no public waveform.

## Checks and next gate

The runner's self-check rejects empty, patched and over-cap inputs. Analysis
controls distinguish a changed low float lane from irrelevant high-lane/volatile
register changes. All selected immutable pins were rechecked after execution.
The frozen packet is reviewed once; do not rerun either collector as an integrity
check. Root owns atlas/catalog/plan/coverage/log adoption. No entire unchanged
released-handoff or predecessor corpus replay was performed.
