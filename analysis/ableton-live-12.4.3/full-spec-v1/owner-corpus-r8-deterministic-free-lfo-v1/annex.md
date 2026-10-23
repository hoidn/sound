
## Finite deterministic Free-LFO observation annex

The [five-member catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r8-deterministic-free-lfo-v1/catalog.json)
contains Sine 0, Square 1, Triangle 2, Ramp Up 3 and Ramp Down 4. DCO-020 and
DCO-029 remain the existing Sine/Ramp Up cases, with no duplicate IDs or transfer
of their criteria. Sample & Hold 5 and Random Ramp 6 remain the separate
clock/seed-dependent U contexts of REQ-011; the five-member class does not mean
all seven shapes are deterministic.

DCO-034–036 use the same explicit 38 host binary32 values as DCO-020/029 except
LfoType at host index18 is respectively1,2,4. The exact bit vectors and input
joins are in the [three draft records](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r8-deterministic-free-lfo-v1/new-cases.json).
Each fixture uses a fresh instance, rate argument44100, parameters in index
order, I1 stereo impulse at4096,16384 frames in512-frame blocks, input flag1,
stopped transport0/0/120, XDEV_TIME0/LIBM_ULP0 and MXCSR1f80. These are supplied
host/test coordinates and substitutions, not proved Live scheduling, stored
value conversion or actual sample-clock/FP-state observations.

| Case ID | Requirement | Kind | Setup | Observation / acceptance criterion | Reference identity |
| --- | --- | --- | --- | --- | --- |
| DCO-034 | 011 | U | Exact annex fixture, LfoType1 Square | X: retained finite stereo output; new waveform expectation and candidate/portable comparator NULL | `b82781c5d6ef5d23…`,131072B; approved partial Square |
| DCO-035 | 011 | U | Exact annex fixture, LfoType2 Triangle | X: retained finite stereo output; new waveform expectation and candidate/portable comparator NULL | `c1741a23aee40b79…`,131072B; approved continuation |
| DCO-036 | 011 | U | Exact annex fixture, LfoType4 Ramp Down | X: retained finite stereo output; new waveform expectation and candidate/portable comparator NULL | `20c4b33c88e6bce0…`,131072B; approved continuation |

The draft now has 36 rows: 29 existing cases with criteria, these three native
observation-only cases, and four existing U cases. The new rows carry X
observations with U acceptance criteria; they are not newly graded renders. Their pre-call native waveform priors remain NULL in the immutable
captures; no new expected waveform, tolerance, Hz/RMS budget, shape fitting or
portable comparator is selected here. No REQ-001 block/rate/reset/clock/FTZ/DAZ,
repeatability, state or lifecycle invariance extends to them. All old 33 rows,
finite objects, criteria and released73 evaluations remain unchanged.

Square's once-only capture exited0 and retained its full output before the
recorder's unsupported Rate-return0 assertion stopped that batch. Its false
completion phases, stale recorder child label and failed guard remain history;
its unused generator's stale tail-index assertion and author-reported assembly
history, without independent durable initial-generation proof, are preserved
in the [history qualifications](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r8-deterministic-free-lfo-v1/history-qualification.json).
Only the two never-launched shapes were captured in the separately approved
continuation. Square was not retried. The continuation records Rate's literal
signed integer with unknown status/clock semantics, rather than requiring0 or
fitting1 as a success oracle.

The owner records use only Root's independently approved full-five summary,
with exact point/hash/output/provenance pointers. They do not re-review or
reopen actual audio, source, providers or original calls. A1, public binding,
ARM/Apple, errors/state/lifecycle, all174+2 modal omissions and parked96-byte
setup remain unchanged. This finite catalog is not a required-outcome
denominator, accepted waveform method, application grade or complete profile.
