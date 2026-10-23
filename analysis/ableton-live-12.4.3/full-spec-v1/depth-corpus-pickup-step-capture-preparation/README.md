# Corpus left pickup step: two-child preparation

**Prepared only. No original calls, measurements or execution selection.**

Both scripts use the exact released CORPUS-AUDIO-006-01 Membrane vector, all38
binary32 values/order, with MIDI pitch/gate and LFO off. A fresh instance receives
one stereo impulse at4096. Both use the unchanged driver's same-instance shape:
`process 8192 512`, one `param 15`, then `process 8192 512`. Control repeats the
initial binary32 0.10000000149011612; left-step uses exactly0.75. All other
commands are identical, including the unchanged right pickup. There are no
MIDI events, info, reset, warm-up, bend or seed perturbations.

[The proposal](proposal.json) pins the unchanged binary, selected source/input,
released vector, immutable owner and earlier independent readiness/accounting
reviews. The [frozen capability record](../depth-corpus-pickup-step-preparation/README.md)
explains input cursor continuation, one append-only outputFILE and the separate
process-local event clock. No new harness, scheduler, loader or export is used.
The existing positive vector motivates a probe; it does not establish ringing
before the new step. No4000-frame movement, right-channel invariance, A1 mapping,
Live/arm64 behavior or numerical criterion is assumed.

Inspect the complete [collector](capture-once.py) and [checker](check.py) before
running only `python3 -B .../check.py --check`. The checker imports no collector;
it compiles only the two inspected pure data guards and selected boolean/count
expressions from the new collector AST. Synthetic log/format/status tests include
two separate16-block process lines,39 parameter bit echoes, exact command order,
12 wrong protocol variants, invalid sizes/nonfinite data, actual traps and four
launch-accounting scenarios. Finite silence, unchanged output and zero return
flags are structurally valid. Lowercase unused `import trap` declarations are
not uppercase actual trap hits. None of these tests calls a native executable.

Only after separate independent preflight and Root's explicit selection may
Root invoke `python3 -B capture-once.py --capture-selected-once EXACT_MANIFEST_SHA`.
The proposal records full absolute argv templates and the complete minimal
PATH/locale/XDEV_TIME=0 environment. Core dumps are disabled; each child has a
30-second timeout. There are at most two launch attempts, control then step,
with no retry or added baseline:74 direct exports per child/148 total, excluding
loader and nested calls. A failed structural first observation stops the pair;
silence or unchanged audio alone never does. The destination is created
exclusively and partial attempts are never deleted or reused.

Full131072-byte finite output, exit0 and exact clean command logs establish
only structural capture validity. The collector separately records attempted
launches, Popen-returned PIDs and valid captures. Launch alone is not proof of
original export execution; failed Popen does not prove no OS child briefly
existed. Timeouts/partial failures remain unknown except for precise log evidence.
All scripts, preflight payloads/seal, stdout/stderr, raw outputs and run records
are retained; before/after preservation maps remain durable even on a failure.

[Preservation inputs](preservation-inputs.json) enumerate811 exact as-of paths,
including existing v1/v2/v3 release bytes and selected retained captures/source.
Mutable wiki paths are deliberately excluded; immutable R6/readiness contexts
supply historical context. No published/current canonical bytes are changed.
Prepared code only writes the separately selected future capture directory.

The author read all new code and the complete existing driver/header and ancestor
R2 collector as data; earlier loader/binder/CXX inspection is carried from the
pinned independent readiness review. This is not independent approval of the
author's ancestor R2; its independent review is separately pinned. Preseal checks
passed without assertion failures; guards were expanded before freeze. No
collector invocation, original call, fit, FFT, model, playback or installation
occurred. Independent review and Root selection remain pending.
