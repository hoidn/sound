# Collision whole12 Resonator1 enable histories

Root selected this whole finite class under design revision 12 and the unchanged
recorded Collision xdev factory model. This is one actual batch and one later
independent review, not a preparation/approval gate chain. The complete initial
manifest, inputs, scripts and new runner/analyzer are frozen before original
calls. `results.json` preserves that manifest's exact initial serialization and
SHA; the final manifest adds captured payload identities after the one attempt.
A SHA argument identifies the frozen input cut and is not a permission file.

## Whole class and exact protocol

All 8 initial Resonator1/OnOff index25 {0,1} × sent25 {0,1} × held/released
transitions are retained, plus all 4 matched no-setter controls. No path is
selected by expected sound or silence. Audio and difference predictions remain
null. Index58 (Resonator2/OnOff) remains off in every history. The existing
`raw/preset_c4.script` supplies all 139 exact ordered parameter tokens, with only
the initial index25 token changed. No current/concurrent run_collision.py extras,
recovered old runner, model, comparator or general run.sh is executed or imported.

Each fresh child uses original CreateInstanceU, SetSampleRateU(44100), all 139
setters, 11264 silent warm-up frames in blocks512, then queues C4/100 at4097.
The released branch additionally queues note-off at7168; “released” names this
note-message history, not an established envelope phase or cutoff. It processes
8192 frames, optionally sends25, processes4096 more and destroys. Silent input,
input flag0 and transport stopped/position0/tempo120 are the existing model.

The entire current col.py, xdevpy.py and xdev.c were read as inert tooling. The
existing xdev.c resets local `done=0` for each process command; event records persist
and are selected by `done <= frame < done+k`. Warm-up precedes event queue commands.
The first segment [0,8192) admits both coordinates; the second [0,4096) excludes
both strictly. The proposed4096 note-on was changed to4097 to avoid equality at the
second segment's end. No event-clear operation, cumulative counter, driver patch
or new object model is assumed. The device state/grid persists across commands;
output is simply appended. This provides no Live clock/grid binding.

There are46 CalcA calls per child (22+16+8), 189 direct exports per transition
and188 per no-setter control:2264 direct entries total, nested original/library
calls unknown. All12 raw outputs retain23552 stereo binary32 frames including
warm-up,188416 bytes each/2260992 bytes total. The old broad run.sh includes278
CalcA probes and is never run here.

## Capture and retained-data checks

`run_batch.py --check` is inspected data-only input/negative validation. The only
actual invocation is `run_batch.py --run PRECALL_MANIFEST_SHA`, using an exclusive
attempt directory, one attempt per selected child,20-second wall/CPU limits,
core0, new process session, stdinDEVNULL, regular stdout/stderr files and1MiB
per-file limit. PATH/LANG/LC_ALL/TZ and XDEV_TIME=0 are explicitly fixed; no libm
sensitivity switch or ambient HOME/LD settings are inherited. The loader/image
and selected recorded runtime/source identities are checked before/after capture
and after each child. These pins do not prove complete dynamic dependency closure.

Fatal status, timeout, stderr, nonfinite/incomplete data, structural/import anomaly
or custody change stops later children, with partial history retained and no retry.
The unchanged harness trap/fault paths exit86/87; there is no longjmp recovery.
The used-import validation and command checks happen at child end; they cannot
stop before later commands within the same script. Import counters count named
bound-code calls, not every internal/provider action. Timeout group-kill/reap is
unexercised until such a failure; escaped descendants, uncatchable outer failure
and complete filesystem failure retention are not proved covered. Raw/JSON writes
use ordinary close/hash without explicit fsync/crash-durability proof.

Matched transition/control warm-up-plus-first-segment byte identity is a validity
condition for attributing their suffix difference to the changed call history.
A mismatch is retained as discovery and stops further attempts, without a
causality claim. Enabled controls must show a positive first-segment peak larger
than their corresponding disabled control; this productive finite contrast is not
a physical threshold or universal effective-silence oracle. Initial-off branches,
repeated setters, unchanged outputs and both note histories remain mandatory.

`analyze.py --check` tests new data-only metric guards. `analyze.py --analyze`
reads captured binary32 words and reports finite peaks/RMS/channel identities,
segment hashes, all8 matched prefix/suffix differences and productive controls.
It never runs original code, models, old analysis, calibration or a candidate.
Same/different suffixes are finite observations only. No waveform comparator,
general smoothing/no-effect/determinism/automation law or new pass is defined.

The batch contributes to REQ-DEVICE-COLLISION-017's missing same-instance setter
history, under its synthetic host scope. It does not establish Live A1/A2,
public delivery, reset/rate automation, persistence, Apple/ARM results, current
receiver binding, physical calibration or whole-product closure. After independent
actual approval, a separate owner wording adoption may add finite cases. Existing
owner, handoff and shared routing remain untouched by this packet.
