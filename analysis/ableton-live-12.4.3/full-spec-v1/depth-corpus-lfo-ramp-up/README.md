# Corpus Free Ramp Up: bounded extracted execution

Author freeze: 2026-10-19 Pacific / 2026-10-20 UTC. Independent review pending.

Two selected calls through the unchanged, retained x86 loader actually ran at
05:27:36 UTC on 2026-10-20 under [ADR 0003](../../../../wiki/decisions/adr-0003-no-reference-execution.md).
They called the shipped Corpus x86_64 create/rate/parameter/process/destroy exports.
This is new X evidence of those calls, not a whole-application observation.

The Sine baseline matched the historical capture exactly:
`fadb3e890a943e637f440b83048d80a9153cc428e9c2840775057a0cc383028c`.
Only after that gate passed did the single Ramp Up capture run, yielding
`40b77412adfc4768bd18e76e5df330ecd536544c50553212ba3125a8de7982ec`.
Both files contain 16,384 finite stereo binary32 frames (131,072 bytes), with
productive post-impulse output on both channels; both children exited 0, with
empty stderr, no trap/fault hit, and `cxx-failbits 0`. The loader also lists
unbound **unused** trap slots; these declarations are not executed faults.

`raw/` retains the two complete scripts, original outputs, stdout and stderr.
All 38 parameter values are explicit. The only difference between scripts is
host index 18, Sine 0 versus Ramp Up 3. Both use 44.1 kHz, blocks of 512,
MXCSR `0x1f80`, stopped transport `{0,0,120}`, input flag 1 on every block,
no events/reset/warm-up, and the retained stereo unit impulse at frame 4096.
Position is held constant by this harness. The unchanged loader exposes stereo
device audio, not the LFO's internal value buffer.

`attempt.json` records the complete actual child environment and limits.
Only ordinary PATH/locale values were inherited, with `XDEV_TIME=0`; ULP/trace
and library-injection overrides were absent. This narrows the proposal's ordinary
inherited environment to avoid retaining unrelated credentials. Core dumps were
disabled, timeout was 30 seconds per child, and each output path was new.
No failure, overwrite, cleanup, retry, new binding, rebuild, old runner/model/fit,
other provider, native Live application or arm64 execution occurred.

The binary and loader identities, full input, original baseline and source pins
are retained in `proposal-asof.json`. Four full retained arm64 source bodies
(construct/process/evaluate/control update at `0x1ccd4`, `0x1d1b4`, `0x1d550`,
`0x1d74c`, chunk-00004 lines 77–80) were freshly read as data and are copied in
`source-selected-records.json`. External type 3 selecting scalar `2φ−1` is an S
reading of that source, not a direct new X measurement of internal phase values.
The five harness/header files were fully read before execution, with independent
source/import/dependency review coordinated by Root. Historical libm/libc++/RTTI,
clock and inferred rand substitutions remain qualified. There were 136 `_rand`
uses in each run; call counts do not prove a waveform's seed invariance.

`observations.json` records only finite audio-pair statistics. The L/R
post-impulse RMS differences are about 0.02610 and 0.02304. These numbers are
observations, not accepted thresholds. The duration is shorter than the inferred
free-LFO period: no complete-cycle/left-phase-wrap claim. Ramp repeatability,
seed/block/rate invariance, internal waveform samples and a new instantaneous
frequency criterion were not measured. No Sine tolerance is reused. Sync, Spin,
random shapes, actual Live transport/A1, arm64 behavior, all 174 omitted modal
observations and compatibility remain unresolved. No normative IDs, release
expectations, original-case grades or completion credit are added here.

`context-asof.json` preserves the four canonical/governance contexts as read;
the proposal's no-execution language describes its historical read-only stage.
The selected execution was separately authorized afterward. Both watch files
show all 400 historical source/capture/release/pin files unchanged. The checker
uses retained snapshots for mutable wiki context rather than requiring future
wiki pages to keep their old hashes. Existing packets and releases were untouched.

Run only `python3 -B check.py --check` to verify retained data, hashes, source
locators, exact scripts/logs/statistics, scope and 14 negative fixtures. This
checker never loads or calls original code. `capture-once.py` is the recorded
one-shot author operation; its fixed exclusive destination already exists, so
it refuses another attempt. It is not a regeneration or replay route. Write or
replay arguments to the checker are rejected. The manifest seals all payloads;
no output is rewritten by checking.

Author preseal note: the first data-only check passed its assertions but printed
7 payloads because a local statistics variable reused the counter name. The
report counter was corrected to 21 before freeze; capture data and calls did not
change, and no original execution was repeated.
