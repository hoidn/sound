# Analog envelope modes — whole P1 finite extracted batch

FROZEN pending one independent actual batch review. Root owns observation adoption, canonical pages, owner revisions and releases. This author packet is not self-approved.

One sweep completed at 2026-10-21T04:11:59.352635+00:00 through 2026-10-21T04:12:00.143447+00:00:21 children, one attempt each,21 exit0, no stderr/timeout/trap/retry,7,408,800 output bytes. All21 outputs have44,100 stereo binary32 frames, are finite and have byte-identical left/right channels. Four of20changed vectors differ from this sweep's baseline;16match it byte-for-byte. Those are observed relations in one fixed history, not a law or complete envelope-mode coverage.

Inputs are the entire frozen P1 selector from batch-high-X-eligibility-v1:four envelope Loop controls at1/2/3 and eight FreeRun/Legato controls at1, separately, plus exact existing DAN028 baseline. All203 parameters remain ordered, including index99=1. Every process has note-on4400/key60/velocity100, note-off35270/velocity64, zero input/flag0, stopped transport(position0/120BPM), rate44100, one44100-frame process request in512-frame blocks, destroy. There is no replay or between-block parameter change. All four envelopes remain in the dataset, including paths that do not change this output. The baseline input is historical DAN028; this batch does not compare its new output with the old reference or apply the old calibrated acceptance metric.

Each child makes87 CalcA calls (last68frames),203 setter calls and Create/Rate/Destroy:293 direct exported calls;6,153 over21children (1,827 CalcA). Constructor/initializer/library/internal call counts are unknown. The T13 256-entry limit is a different harness restriction and is not a total-call cap here.

| Input | Single change | Byte-different frames vs baseline | First numeric difference | Last observed nonzero frame |
| --- | --- | ---: | ---: | ---: |
| baseline-DAN028 | control | 0 | None | 40805 |
| mode-01-i89-v1 | 89=1 | 0 | None | 40805 |
| mode-02-i89-v2 | 89=2 | 0 | None | 40805 |
| mode-03-i89-v3 | 89=3 | 0 | None | 40805 |
| mode-04-i90-v1 | 90=1 | 0 | None | 40805 |
| mode-05-i91-v1 | 91=1 | 0 | None | 40805 |
| mode-06-i101-v1 | 101=1 | 25281 | 15525 | 40805 |
| mode-07-i101-v2 | 101=2 | 25281 | 15525 | 40805 |
| mode-08-i101-v3 | 101=3 | 8855 | 35245 | 44099 |
| mode-09-i102-v1 | 102=1 | 25281 | 15525 | 21085 |
| mode-10-i103-v1 | 103=1 | 0 | None | 40805 |
| mode-11-i172-v1 | 172=1 | 0 | None | 40805 |
| mode-12-i172-v2 | 172=2 | 0 | None | 40805 |
| mode-13-i172-v3 | 172=3 | 0 | None | 40805 |
| mode-14-i173-v1 | 173=1 | 0 | None | 40805 |
| mode-15-i174-v1 | 174=1 | 0 | None | 40805 |
| mode-16-i184-v1 | 184=1 | 0 | None | 40805 |
| mode-17-i184-v2 | 184=2 | 0 | None | 40805 |
| mode-18-i184-v3 | 184=3 | 0 | None | 40805 |
| mode-19-i185-v1 | 185=1 | 0 | None | 40805 |
| mode-20-i186-v1 | 186=1 | 0 | None | 40805 |

Frame indexes are zero-based. The comparison is against the same-batch baseline only, over both channels; bit and numeric differences are separately recorded. Descriptive peak/RMS/mean/difference summaries widen exact binary32 values to Python floats and use host binary64 fsum/sqrt; they are not calibrated acceptance metrics or a deterministic waveform claim. Raw outputs remain authoritative. No pre-capture oracle is applied and no comparison grade is assigned in this packet. Under design12, independent batch approval can admit these finite observations into the next draft owner revision without reviewing the same observations again.

Current owner revision2 REQ016/021 and DAN046 retain the unknown mode/lifecycle scope. These20first-order vectors do not resolve simultaneous modes, overlapping/repeated notes, reset, held/loop stages, FreeRun lifecycle, all settings, actual current defaults or public delivery. Equality does not prove inactivity, no-op or absence of an effect; a difference supplies no general mode semantics. R2 REQ022's withdrawn first-change/100ms settling/trajectory law is not applied. A1/A2, actual Live receiver/clock/output, ARM execution and Apple library equivalence remain unknown. These are finite x86 extracted observations, with ADR0003's ARM inference caveat; no complete family/product closure follows.

The original host is the unchanged recorded /var/tmp/sound-analysis/t12-analog/xdev and exact Analog universal bundle/x86 slice. No build, patch, new original receiver/setup, provider emulation, dependency installation, source frontier or fake Live host identity was introduced. The supplied factory/script model, existing libc/libm/libc++ shims, Park–Miller PRNG/time0/C locale and default MXCSR0x1f80 are inherited model qualifications. Used imports are recorded; their presence is not Apple/ARM or full-Live conformance. Standard runtime library and ld.so.cache custody is pinned, not a claim of independently tracing every dynamic lookup.

inputs.json carries all21 script pins, exact203binary32 bit vectors, whole selector,18source-document pins,8runtime expected identities, slice and environment/resource limits. scripts/ retains every exact input script. results.json records30equal before/after custody entries,21PID/UTC/monotonic/status records, exact argv/environment and stdout/stderr/output identities/import use; the manifest names the source-fixed child cwd. attempts/ retains all63 raw files, including21empty stderr files. Child environment is exactly PATH=/usr/bin:/bin,LC_ALL=C,LANG=C,TZ=UTC,XDEV_TIME=0; stdin DEVNULL, core0, CPU20s, wall timeout20s, new session,1MiB per regular child file. Outer Python is /usr/bin/python3 -I -B; its binary identity is recorded, but its complete ambient outer-shell environment was not retained. Child environment is replaced explicitly. Timeout group-kill/reap code was not exercised; escaped descendants, uncatchable outer death and filesystem failure completeness are not proven.

run_batch.py is inert review source now: **do not run --run**. Its existing exclusive attempts directory refuses replay. It imports no old driver and launches only the selected unchanged xdev children. analyze.py reads retained packet bytes only, never launches the original or a model. To check data, use `/usr/bin/python3 -I -B run_batch.py --check-inputs` and `/usr/bin/python3 -I -B analyze.py --check`. The first has six author negative controls for complete inputs/bits/calls; the second has seven control groups covering signed-zero, channel differences, NaN/Inf, zero origin and frame geometry. check-results.json records those checks. No independent approval is claimed by author checks.

manifest.json is the single review seal and records every child's input/result identities plus the exact harness/image/slice/stub premises and all payload pins. There are no separate preparation/readiness/selection/preflight/receipt approval gates. Mutable owner identity is an as-of scope pin; any later owner changes do not rewrite this frozen batch.
